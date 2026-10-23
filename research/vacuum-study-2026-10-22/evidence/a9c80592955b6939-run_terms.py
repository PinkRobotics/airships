"""DELTA-D: face-density factors with each unsourced margin term removed.

QUESTIONABLE inputs. PROJECTION targets. No qualified hull safety factor.
The pinned model files are not edited. Each variant rebinds p2 after import.
BETA is 1. Revert is Q and gamma. Basis is endpoint. The rows are UNREVIEWED.
"""
import hashlib
import inspect
import json
import math
import os
import sys
import time
from datetime import datetime

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

MODEL = (
    "unpublished-local-ref:2f846ae958082233"
    "/.ship/work/outputs/vacuum-mainline066-improvement-vector-1020/model"
)
FILED = (
    "unpublished-local-ref:2f846ae958082233"
    "/.ship/work/outputs/vacuum-mainline066-improvement-vector-1020/RESULTS.json"
)
sys.path.insert(0, MODEL)
import model63  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
CASES = ((20, "ISA"), (20, "optimistic"), (30, "ISA"), (30, "optimistic"))
MATURITIES = ("concept", "TRL7")
REVERT = ("Q", "gamma")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def install(source):
    local = {}
    exec(compile(source, "delta_d_p2.py", "exec"), model63.__dict__, local)
    model63.p2 = local["p2"]


ORIGINAL = inspect.getsource(model63.p2)
VARIANTS = (
    ("control", ()),
    ("no_kc", (
        ("kc = np.where(vc <= 2., 1-vc/4, 1/vc)", "kc = np.ones_like(vc)"),
    )),
    ("no_cure", (
        ("cure = kb*12.3e-6*dtc*tc/(2*tf)", "cure = np.zeros_like(tf)"),
    )),
    ("no_grad_bend", (
        ('grad = E*11.3e-6*(1.002*t["gradient_K"])/(2*(1-NU))',
         "grad = np.zeros_like(tf)"),
        ('bend = E/(1-NU**2)*h/2*11.3e-6/r*(1.002*t["curvature_temperature_K"])',
         "bend = np.zeros_like(tf)"),
    )),
    ("no_pressure_augmentation", (
        ("p = P0*max(1.01, QWEATHER[weather])+QWIND if pressure_override is None else pressure_override",
         "p = P0"),
    )),
)


def patched(name):
    source = ORIGINAL
    pairs = dict(VARIANTS)[name]
    for old, new in pairs:
        if old not in source:
            raise SystemExit(f"patch miss in {name}: {old}")
        source = source.replace(old, new, 1)
    install(source)


def slim(point):
    if point is None:
        return None
    modes = {key: float(value) for key, value in point["modes"].items()}
    binding = sorted(modes, key=modes.get)
    props = point["properties"]
    return {
        "payload_kg": float(point["payload_kg"]),
        "density_kg_m3": float(props["density_kg_m3"]),
        "Q": float(props["Q"]),
        "gamma": float(props["gamma"]),
        "Vc": float(props["Vc"]),
        "E_Pa": float(props["E_Pa"]),
        "strength_Pa": float(props["strength_Pa"]),
        "binding": binding[:3],
        "global_buckling": modes["global_buckling"],
        "face_wrinkling": modes["face_wrinkling"],
        "geometry": {key: float(value) for key, value in point["geometry"].items()},
    }


def admissible(point):
    props = point["properties"]
    return (abs(float(props["Q"]) - 0.33) < 1e-6
            and abs(float(props["gamma"]) - 0.20) < 1e-6
            and float(props["Vc"]) < 2.0)


def density_factor(r, weather, maturity):
    def at(factor, n):
        return model63.p2_opt(
            r, weather, {"Q": 1.0, "face_density": factor},
            basis="endpoint", maturity=maturity, n=n, revert=REVERT)

    base = at(1.0, 200)
    if base is not None and base["payload_kg"] >= 0:
        return {"factor": 1.0, "status": "already closes", "solution": base}
    lo, hi = 1.0, 1.02
    point = base
    closed = False
    for _ in range(16):
        point = at(hi, 140)
        if point is not None and point["payload_kg"] >= 0:
            closed = True
            break
        lo, hi = hi, hi * 1.2
        if hi > 8:
            break
    if not closed:
        return {"factor": None, "status": "not closed below factor 8", "solution": point}
    for _ in range(22):
        mid = math.sqrt(lo * hi)
        point = at(mid, 160)
        if point is not None and point["payload_kg"] >= 0:
            hi = mid
        else:
            lo = mid
    final = at(hi * (1 + 1e-7), 320)
    return {"factor": hi, "status": "conditional closure", "solution": final,
            "root_bracket": [lo, hi]}


def decompose():
    filed = json.loads(open(FILED).read())
    rows = []
    for r, weather in CASES:
        key = f"concept:{r}:{weather}"
        geom = filed["base"]["rows"][key]["point"]["geometry"]
        tf, tc = float(geom["tf_m"]), float(geom["tc_m"])
        point = model63.p2(
            r, weather, tf, tc, basis="endpoint", maturity="concept",
            revert=REVERT, detail=True)
        E = float(point["properties"]["E_Pa"])
        G = float(point["properties"]["Gc_Pa"])
        Q = float(point["properties"]["Q"])
        gamma = float(point["properties"]["gamma"])
        p = float(point["pressure_Pa"])
        nu = float(model63.NU)
        h = tc + tf
        sigp = p * r / (4 * tf)
        sig0 = E * h / (r * math.sqrt(1 - nu ** 2))
        crimp = G * h * h / (2 * tf * tc)
        vc = sig0 / crimp
        kc = (1 - vc / 4) if vc <= 2 else (1 / vc)
        thermal = model63.thermal(r, tc)
        grad = E * 11.3e-6 * (1.002 * float(thermal["gradient_K"])) / (2 * (1 - nu))
        bend = (E / (1 - nu ** 2) * h / 2 * 11.3e-6 / r
                * (1.002 * float(thermal["curvature_temperature_K"])))
        kb = 0.5 * 67e9 * float(model63.C["rho"]) / 2700.0
        dtc = 1.002 * max(366.4833333333333 - float(thermal["min_outer_K"]), 0.0)
        cure = kb * 12.3e-6 * dtc * tc / (2 * tf)
        demand = sigp + grad + bend + cure
        ec = float(model63.C["Ec_Pa"])
        wrinkle = model63.BETA * Q * math.sqrt(E * ec * tf / tc) / demand
        buckle = gamma * kc * sig0 / (sigp + cure)
        if abs(buckle - float(point["modes"]["global_buckling"])) > 1e-6:
            raise SystemExit(f"buckling attribution mismatch {key}")
        if abs(wrinkle - float(point["modes"]["face_wrinkling"])) > 1e-6:
            raise SystemExit(f"wrinkling attribution mismatch {key}")
        sigp0 = float(model63.P0) * r / (4 * tf)
        sig0_common = E * h / (r * math.sqrt(1 - 0.33 ** 2))
        rows.append({
            "case": key,
            "tf_m": tf,
            "tc_m": tc,
            "Vc": vc,
            "kc": kc,
            "model_pressure_Pa": p,
            "P0_Pa": float(model63.P0),
            "model_global_buckling": buckle,
            "model_face_wrinkling": wrinkle,
            "buckling_common_nu_P0": 0.20 * sig0_common / sigp0,
            "buckling_model_nu_P0": 0.20 * sig0 / sigp0,
            "buckling_model_p_no_kc_no_cure": gamma * sig0 / sigp,
            "buckling_model_p_kc_no_cure": gamma * kc * sig0 / sigp,
            "buckling_model_p_no_kc_cure": gamma * sig0 / (sigp + cure),
            "wrinkling_P0_sigp_only": 0.33 * math.sqrt(E * ec * tf / tc) / sigp0,
            "wrinkling_model_p_sigp_only": Q * math.sqrt(E * ec * tf / tc) / sigp,
            "thermal_share_of_demand": (grad + bend + cure) / demand,
            "cure_over_sigp": cure / sigp,
        })
    return rows


def main():
    natural = float(model63.BETA)
    if abs(natural - 0.682327803828082) > 1e-9:
        raise SystemExit(f"unexpected natural BETA {natural}")
    model63.BETA = 1.0
    started = datetime.now().astimezone().isoformat()
    t0 = time.perf_counter()
    install(ORIGINAL)
    margins = decompose()
    print("margins", flush=True)
    for row in margins:
        print(f"  {row['case']} buck {row['model_global_buckling']:.6f} "
              f"common {row['buckling_common_nu_P0']:.4f} "
              f"wrinkle {row['model_face_wrinkling']:.6f} "
              f"p0 {row['wrinkling_P0_sigp_only']:.4f}", flush=True)
    if os.environ.get("CHECK_ONLY") == "1":
        print("check ok", flush=True)
        return
    filed = {item["case"]: item for item in json.loads(open(FILED).read())["density_only"]}
    rho0 = float(model63.F["rho"])
    variants = []
    for name, _pairs in VARIANTS:
        print(f"variant {name}", flush=True)
        patched(name)
        rows = []
        for maturity in MATURITIES:
            for r, weather in CASES:
                case = f"{maturity}:{r}:{weather}"
                found = density_factor(r, weather, maturity)
                solution = found["solution"]
                factor = found["factor"]
                row = {
                    "case": case,
                    "numerical_status": "unreviewed",
                    "filed_066_factor": filed[case]["factor"],
                    "filed_066_density_kg_m3": filed[case]["density_kg_m3"],
                    "recomputed_factor": factor,
                    "recomputed_density_kg_m3": None if factor is None else rho0 / factor,
                    "status": found["status"],
                    "admissible_line": bool(solution is not None and admissible(solution)),
                    "solution": slim(solution),
                }
                if name == "control" and maturity == "concept" and factor is not None:
                    if abs(factor - filed[case]["factor"]) > 0.01:
                        print(f"  control offset {case} {factor} filed {filed[case]['factor']}",
                              flush=True)
                rows.append(row)
                print(f"  {case} {found['status']} {factor}", flush=True)
        variants.append({"id": name, "rows": rows})
        install(ORIGINAL)
    doc = {
        "tag": "QUESTIONABLE / PROJECTION",
        "qualified_hull_SF": None,
        "numerical_status": "unreviewed",
        "beta_natural": natural,
        "beta_run": 1.0,
        "revert": list(REVERT),
        "basis": "endpoint",
        "method": "DELTA-C binary search of face_density on p2_opt. Concept and TRL7. "
                  "Pins are not edited. kc, cure, grad, bend, or the pressure adders "
                  "are removed one variant at a time.",
        "model63": os.path.join(MODEL, "model63.py"),
        "model63_sha256": sha256(os.path.join(MODEL, "model63.py")),
        "model61_sha256": sha256(os.path.join(MODEL, "model61.py")),
        "started": started,
        "fixed_geometry_margins": margins,
        "variants": variants,
        "completed": datetime.now().astimezone().isoformat(),
        "elapsed_s": time.perf_counter() - t0,
    }
    path = os.path.join(OUT, "RUN.json")
    with open(path, "w") as handle:
        json.dump(doc, handle, indent=2)
        handle.write("\n")
    print(f"wrote {path} in {doc['elapsed_s']:.1f}s", flush=True)


if __name__ == "__main__":
    main()
