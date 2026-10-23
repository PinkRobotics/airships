"""MAINLINE-069: R30 optimistic design point, written once.

QUESTIONABLE inputs. PROJECTION payloads. No finite-element run.
No qualified hull safety factor. The copied model files are not edited.
BETA is 1. Revert is Q and gamma. Basis is endpoint.
kc, cure, gradient, bending and the pressure adder stay in the model.
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

OUT = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(OUT, "model")
sys.path.insert(0, MODEL)
import model63  # noqa: E402

GRAPHITE = (
    "unpublished-local-ref:2f846ae958082233"
    "/.ship/work/outputs/vacuum-mainline070-graphite-face-1020/RESULTS.json"
)
REVERT = ("Q", "gamma")
F066 = 1.824771768877316
RHO066 = 1013.8254172675006
GAMMA_FACTOR_066 = 2.7669873295303313
DELTA_D_R30_OPT = {
    "filed_control": 1.824771768877316,
    "no_kc": 1.4591468390294113,
    "no_cure": 1.7694119150252845,
    "no_grad_bend": 1.8092731638452857,
    "no_pressure": 1.7397410734805205,
}
LAWS = {
    "global_buckling": "gamma*kc*sig0/(sigp+cure); gamma 0.20 is the CR-1457 hemisphere floor for Vc<2; kc=1-Vc/4 is unsourced",
    "face_wrinkling": "BETA*Q*sqrt(E*Ec*tf/tc)/demand; Q=0.33 is CR-1457 eq 2.2-14; BETA=1 by the 066 line; demand includes unsourced grad, bend and cure",
    "intracell_dimpling": "E*(tf/s_cell)^2/((1-nu^2)*demand); model equation, unsourced as a hull test",
    "core_shear_crimping": "crimp/demand; Gc from the Hexcel CR-III citation in 040; demand includes unsourced thermal stress",
    "core_crush": "2*crush_Pa/p; crush from the 040 core record; pressure includes the unsourced adder",
    "face_compression": "strength/demand; strength_full 379.2 MPa is 040's historical tuple",
    "thermal_interface": "25 psi / tau; tau uses unsourced 12.3e-6, kb and the cure-temperature window",
    "scarf_average_shear": "10 MPa / (demand*scarf/(1+scarf^2)); scarf ratio from 040 joining",
    "core_wall_yield": "227.53 MPa / (1.2*67 GPa*12.3e-6*dt); coefficients unsourced",
    "vacuum_pressure": "0.01*P0/hot_pressure_24h; model leak and desorption account",
}


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


ORIGINAL = inspect.getsource(model63.p2)


def install(source):
    local = {}
    exec(compile(source, "mainline069_p2.py", "exec"), model63.__dict__, local)
    model63.p2 = local["p2"]


def patched(name):
    pairs = {
        "no_kc": (
            ("kc = np.where(vc <= 2., 1-vc/4, 1/vc)", "kc = np.ones_like(vc)"),
        ),
        "no_cure": (
            ("cure = kb*12.3e-6*dtc*tc/(2*tf)", "cure = np.zeros_like(tf)"),
        ),
        "no_grad_bend": (
            ('grad = E*11.3e-6*(1.002*t["gradient_K"])/(2*(1-NU))',
             "grad = np.zeros_like(tf)"),
            ('bend = E/(1-NU**2)*h/2*11.3e-6/r*(1.002*t["curvature_temperature_K"])',
             "bend = np.zeros_like(tf)"),
        ),
        "no_pressure": (
            ("p = P0*max(1.01, QWEATHER[weather])+QWIND if pressure_override is None else pressure_override",
             "p = P0"),
        ),
    }[name]
    source = ORIGINAL
    for old, new in pairs:
        if old not in source:
            raise SystemExit(f"patch miss in {name}")
        source = source.replace(old, new, 1)
    install(source)


def floats(point):
    if point is None:
        return False
    if float(point["payload_kg"]) < 0:
        return False
    return min(float(v) for v in point["modes"].values()) >= 1 - 1e-8


def optimize(weather, factors, maturity, n):
    return model63.p2_opt(
        30, weather, factors, basis="endpoint", maturity=maturity,
        n=n, revert=REVERT)


def both(factors, maturity, n):
    points = {}
    ok = True
    for weather in ("ISA", "optimistic"):
        point = optimize(weather, factors, maturity, n)
        points[weather] = point
        if not floats(point):
            ok = False
    return ok, points


def search_factor(start, key, maturity, extra, cap):
    """Smallest factor at or above start that floats both weathers."""
    factors = dict(extra)
    factors[key] = start
    ok, _points = both(factors, maturity, 160)
    if ok:
        return start, "start already floats"
    lo, hi = start, min(cap, start * 1.02)
    closed = False
    for _ in range(12):
        factors[key] = hi
        ok, _points = both(factors, maturity, 140)
        if ok:
            closed = True
            break
        lo, hi = hi, min(cap, hi * 1.15)
        if hi >= cap - 1e-12:
            break
    if not closed:
        raise SystemExit(f"{key} did not close by {hi}")
    for _ in range(18):
        mid = math.sqrt(lo * hi)
        factors[key] = mid
        ok, _points = both(factors, maturity, 160)
        if ok:
            hi = mid
        else:
            lo = mid
    return hi * (1 + 1e-7), "searched above the filed factor"


def joints(point):
    r = float(point["R_m"])
    tf = float(point["geometry"]["tf_m"])
    tc = float(point["geometry"]["tc_m"])
    film = float(point["properties"]["film_kg_m2_interface"])
    scarf = float(model63.SCARF)
    area = 4 * math.pi * r * r
    length = area * (1 / (0.6096 - scarf * tf) + 1 / (1.8288 - scarf * tf))
    parts = {
        "film_kg": 2 * area * film,
        "scarf_kg": length * 2 * tf * math.sqrt(1 + scarf * scarf) * 0.07,
        "splice_kg": length * 0.0005 * tc * 500,
        "seal_kg": length * 0.002,
    }
    parts["sum_kg"] = sum(parts.values())
    charged = float(point["bill_kg"]["charged_joining"])
    if abs(parts["sum_kg"] - charged) > 1e-3:
        raise SystemExit(
            f"joint sum {parts['sum_kg']} != charged_joining {charged}")
    parts["scarf_ratio"] = scarf
    parts["charged_joining_kg"] = charged
    return parts


def pack(point, role):
    modes = {key: float(value) for key, value in point["modes"].items()}
    crushing = []
    for name, law in LAWS.items():
        if name not in modes:
            continue
        crushing.append({
            "mode": name,
            "value": modes[name],
            "source_law": law,
            "tag": "QUESTIONABLE",
        })
    props = point["properties"]
    return {
        "role": role,
        "R_m": float(point["R_m"]),
        "weather": point["weather"],
        "maturity": point["maturity"],
        "basis": point["basis"],
        "revert": point["revert"],
        "factors": point["factors"],
        "geometry": {key: float(value) for key, value in point["geometry"].items()},
        "joints": joints(point),
        "properties": {key: float(value) if isinstance(value, (int, float)) else value
                       for key, value in props.items()},
        "pressure_Pa": float(point["pressure_Pa"]),
        "lift_kg": float(point["lift_kg"]),
        "payload_kg": float(point["payload_kg"]),
        "mass_before_growth_kg": float(point["mass_before_growth_kg"]),
        "growth_total_kg": float(point["growth_total_kg"]),
        "bill_kg": {key: float(value) for key, value in point["bill_kg"].items()},
        "growth_kg": {key: float(value) for key, value in point["growth_kg"].items()},
        "modes": modes,
        "crushing_margins": crushing,
        "binding": [[name, float(value)] for name, value in point["binding"]],
        "floats": floats(point),
        "qualified_hull_SF": None,
        "tag": "PROJECTION",
    }


def fixed(weather, maturity, factors, tf, tc, revert=REVERT):
    point = model63.p2(
        30, weather, tf, tc, factors=factors, basis="endpoint",
        maturity=maturity, detail=True, revert=revert)
    return pack(point, "fixed-geometry")


def graphite_extract():
    doc = json.loads(open(GRAPHITE).read())
    rows = doc["gamma_held_0_20"]["rows"]
    concept = [row for row in rows if row["maturity"] == "concept"]
    r30 = [row for row in concept if row["R_m"] == 30]
    family = max(concept, key=lambda row: row["density_factor_to_float"])
    r30_both = max(r30, key=lambda row: row["density_factor_to_float"])
    r30_best = min(r30, key=lambda row: row["density_factor_to_float"])
    keep = (
        "maturity", "R_m", "weather", "payload_kg", "tf_m", "tc_m",
        "E_GPa", "rho_kg_m3", "strength_MPa", "gamma", "Q", "Vc",
        "co_binding", "binding", "floats", "density_factor_to_float",
        "closed_rho_kg_m3",
    )
    def slim(row):
        return {key: row[key] for key in keep}
    return {
        "source": GRAPHITE,
        "source_sha256": sha256(GRAPHITE),
        "law": "gamma held at 0.20, the card case. Version-7 gamma step is not this case.",
        "family_witness": slim(family),
        "r30_both_weathers": slim(r30_both),
        "r30_least_remaining_factor": slim(r30_best),
        "r30_concept": [slim(row) for row in r30],
        "note": "No graphite row floats at the stated 2250 kg/m3. Factors are still required.",
    }


def main():
    natural = float(model63.BETA)
    if abs(natural - 0.682327803828082) > 1e-9:
        raise SystemExit(f"unexpected natural BETA {natural}")
    model63.BETA = 1.0
    install(ORIGINAL)
    started = datetime.now().astimezone().isoformat()
    t0 = time.perf_counter()
    rho0 = float(model63.F["rho"])
    if abs(rho0 - 1850) > 1e-6:
        raise SystemExit(f"unexpected face density {rho0}")

    print("design check at filed factor", flush=True)
    design_factors = {"Q": 1.0, "face_density": F066}
    ok, _preview = both(design_factors, "concept", 180)
    design_status = "066 factor floats both concept weathers"
    design_factor = F066
    if not ok:
        print("filed factor does not close; searching", flush=True)
        design_factor, design_status = search_factor(
            F066, "face_density", "concept", {"Q": 1.0}, 8.0)
        design_factors = {"Q": 1.0, "face_density": design_factor}
    print(f"design factor {design_factor} {design_status}", flush=True)

    print("design optima n=320", flush=True)
    optimistic = optimize("optimistic", design_factors, "concept", 320)
    isa_reopt = optimize("ISA", design_factors, "concept", 320)
    if not floats(optimistic) or not floats(isa_reopt):
        print("n=320 missed the coarse close; bumping the factor", flush=True)
        for _ in range(8):
            design_factor *= 1.002
            design_factors = {"Q": 1.0, "face_density": design_factor}
            optimistic = optimize("optimistic", design_factors, "concept", 320)
            isa_reopt = optimize("ISA", design_factors, "concept", 320)
            if floats(optimistic) and floats(isa_reopt):
                design_status += "; n=320 needed a slightly lighter face"
                break
        else:
            raise SystemExit("design point does not float at n=320")
    tf = float(optimistic["geometry"]["tf_m"])
    tc = float(optimistic["geometry"]["tc_m"])
    same = {}
    for maturity in ("concept", "TRL7"):
        for weather in ("ISA", "optimistic"):
            key = f"{maturity}:{weather}"
            same[key] = fixed(weather, maturity, design_factors, tf, tc)
            print(f"  same geometry {key} payload {same[key]['payload_kg']:.3f}",
                  flush=True)

    print("TRL7 gamma alternative", flush=True)
    gamma_factors = {"Q": 1.0, "face_density": 1.0, "gamma": GAMMA_FACTOR_066}
    g_ok, _gprev = both(gamma_factors, "TRL7", 180)
    gamma_factor = GAMMA_FACTOR_066
    gamma_status = "066 realized-gamma factor floats both TRL7 weathers"
    if not g_ok:
        print("filed gamma factor does not close; searching", flush=True)
        gamma_factor, gamma_status = search_factor(
            GAMMA_FACTOR_066, "gamma", "TRL7",
            {"Q": 1.0, "face_density": 1.0}, 5.0)
        gamma_factors = {"Q": 1.0, "face_density": 1.0, "gamma": gamma_factor}
    gamma_opt = optimize("optimistic", gamma_factors, "TRL7", 320)
    gamma_isa = optimize("ISA", gamma_factors, "TRL7", 320)
    if not floats(gamma_opt) or not floats(gamma_isa):
        print("n=320 missed the gamma close; bumping the factor", flush=True)
        for _ in range(8):
            gamma_factor *= 1.002
            gamma_factors = {"Q": 1.0, "face_density": 1.0, "gamma": gamma_factor}
            gamma_opt = optimize("optimistic", gamma_factors, "TRL7", 320)
            gamma_isa = optimize("ISA", gamma_factors, "TRL7", 320)
            if floats(gamma_opt) and floats(gamma_isa):
                gamma_status += "; n=320 needed a slightly higher gamma"
                break
        else:
            raise SystemExit("TRL7 gamma alternative does not float")
    gtf = float(gamma_opt["geometry"]["tf_m"])
    gtc = float(gamma_opt["geometry"]["tc_m"])
    gamma_same_isa = fixed("ISA", "TRL7", gamma_factors, gtf, gtc)
    gamma_admissible = fixed(
        "optimistic", "TRL7",
        {"Q": 1.0, "face_density": 1.0, "gamma": 1.0}, gtf, gtc)

    print("payload probes", flush=True)
    probes = []
    base_payload = same["concept:optimistic"]["payload_kg"]

    def add_probe(name, packed, route):
        delta = float(packed["payload_kg"]) - base_payload
        probes.append({
            "id": name,
            "payload_kg": float(packed["payload_kg"]),
            "delta_payload_kg": delta,
            "abs_delta_payload_kg": abs(delta),
            "floats": packed["floats"],
            "binding": packed["binding"],
            "route": route,
            "tag": "QUESTIONABLE",
        })

    add_probe(
        "face_density_back_to_1850",
        fixed("optimistic", "concept", {"Q": 1.0, "face_density": 1.0}, tf, tc),
        "068 mirror-like graphite film, first coupon an in-plane compression stack near 2.1 mm; T1 is 038 SR-200 compression. The design density is not a published sheet.",
    )
    for name, route in (
        ("no_kc", "analysis: open CR-1457 and DOIs 10.2514/3.5568 and 10.2514/3.1932 for kc=1-Vc/4. No named copy was in SOURCE-INDEX."),
        ("no_cure", "analysis: same sources, for the cure stress kb*12.3e-6*dtc*tc/(2*tf)."),
        ("no_grad_bend", "analysis: same sources, for the 11.3e-6 gradient and bending stress."),
        ("no_pressure", "analysis: the 1.01 floor and QWIND are not in COMMON.md. 040 names unopened pinned 014b."),
    ):
        patched(name)
        add_probe(name, fixed("optimistic", "concept", design_factors, tf, tc), route)
        install(ORIGINAL)
    add_probe(
        "baseline_film",
        fixed("optimistic", "concept", design_factors, tf, tc,
              revert=("Q", "gamma", "bond_film")),
        "analysis: weigh the installed film. Favorable film is half the 040 baseline. 067 read AF 163-2U at 0.015 lb/ft2 as a thin product, not a hull measurement.",
    )
    add_probe(
        "modulus_today_290_GPa",
        fixed("optimistic", "concept", design_factors, tf, tc,
              revert=("Q", "gamma", "face_modulus")),
        "analysis: 067 normalizes the face to 290 GPa. The design uses 040 E_full 293.6 GPa.",
    )
    add_probe(
        "strength_today_345_MPa",
        fixed("optimistic", "concept", design_factors, tf, tc,
              revert=("Q", "gamma", "face_strength")),
        "T1: 038 measures SR-200 compression. The design uses 040 strength_full 379.2 MPa.",
    )
    add_probe(
        "ISA_weather_same_geometry",
        same["concept:ISA"],
        "analysis: optimistic weather is QWEATHER 1.03655 plus QWIND and the mass headroom. ISA is the admissible weather.",
    )
    probes.sort(key=lambda row: row["abs_delta_payload_kg"], reverse=True)

    film = model63.I["film"]
    doc = {
        "tag": "QUESTIONABLE / PROJECTION",
        "qualified_hull_SF": None,
        "fe_run": False,
        "beta_natural": natural,
        "beta_run": 1.0,
        "revert": list(REVERT),
        "basis": "endpoint",
        "radius_m": 30,
        "why_R30": "066 concept closure density is 1013.8 kg/m3 at R30 optimistic and 993.2 at R20 optimistic. R30 needs the smaller improvement and still clears both weathers.",
        "model63_sha256": sha256(os.path.join(MODEL, "model63.py")),
        "model61_sha256": sha256(os.path.join(MODEL, "model61.py")),
        "started": started,
        "sourcing": {
            "kc": "unsourced; kept; form 1-Vc/4 below Vc 2, meeting 1/Vc at Vc 2",
            "cure": "unsourced; kept; 12.3e-6, kb, 366.4833333333333 K",
            "gradient_bending": "unsourced; kept; 11.3e-6",
            "pressure_adder": "unsourced; kept; P0*max(1.01, QWEATHER)+QWIND",
            "opened": [
                "COMMON.md states the simpler kd buckling law and does not state these four equations",
                "knockdown.md states CR-1457 gamma 0.20 and Q 0.33 and does not state these four equations",
                "SOURCE-INDEX.json has no path for CR-1457, 014b, 10.2514/3.5568 or 10.2514/3.1932",
                "CARD-065 states CR-1457 wrinkling equations 2.2-8 and 2.2-14, not these four terms",
                "040 INPUTS stores external_pressure_factor_floor 1.01 and names pinned 014b, which is not in the index",
            ],
            "private_papers": "Cite 10.2514/3.5568 and 10.2514/3.1932 by DOI only. No named copy was opened.",
        },
        "design": {
            "filed_066_factor": F066,
            "filed_066_density_kg_m3": RHO066,
            "factor_used": design_factor,
            "density_kg_m3": rho0 / design_factor,
            "status": design_status,
            "primary": pack(optimistic, "concept-optimistic-optimum"),
            "isa_reoptimized_same_density": pack(isa_reopt, "concept-ISA-reoptimized"),
            "same_geometry": same,
        },
        "trl7_alternative": {
            "face_density_kg_m3": rho0,
            "face_density_factor": 1.0,
            "filed_066_gamma_factor": GAMMA_FACTOR_066,
            "filed_066_realized_gamma": 0.20 * GAMMA_FACTOR_066,
            "gamma_factor_used": gamma_factor,
            "status": gamma_status,
            "note": "Optimism of this alternative only. The design point keeps gamma 0.20.",
            "primary": pack(gamma_opt, "TRL7-optimistic-optimum"),
            "isa_reoptimized": pack(gamma_isa, "TRL7-ISA-reoptimized"),
            "same_geometry_ISA": gamma_same_isa,
            "same_geometry_gamma_0.20_payload_kg": gamma_admissible["payload_kg"],
            "gamma_optimism_payload_delta_kg": (
                float(gamma_opt["payload_kg"]) - gamma_admissible["payload_kg"]),
        },
        "graphite_film_070": graphite_extract(),
        "delta_d_concept_R30_optimistic_factors_without_term": DELTA_D_R30_OPT,
        "probes_at_design_geometry": probes,
        "admissible_reference": {
            "face_density_kg_m3": rho0,
            "E_today_Pa": float(model63.F["E_today_Pa"]),
            "E_full_Pa": float(model63.F["E_full_Pa"]),
            "strength_today_Pa": float(model63.F["strength_today_Pa"]),
            "strength_full_Pa": float(model63.F["strength_full_Pa"]),
            "film_baseline_kg_m2": float(film["baseline_kg_m2_interface"]),
            "film_favorable_kg_m2": float(film["favorable_kg_m2_interface"]),
            "gamma": 0.20,
            "Q": 0.33,
            "beta_natural": natural,
        },
        "completed": datetime.now().astimezone().isoformat(),
        "elapsed_s": time.perf_counter() - t0,
    }
    path = os.path.join(OUT, "RUN.json")
    with open(path, "w") as handle:
        json.dump(doc, handle, indent=2)
        handle.write("\n")
    print(f"wrote {path} in {doc['elapsed_s']:.1f}s", flush=True)
    primary = doc["design"]["primary"]
    print(
        f"FLOAT tf {primary['geometry']['tf_m']:.6f} "
        f"tc {primary['geometry']['tc_m']:.6f} "
        f"payload {primary['payload_kg']:.4f} "
        f"rho {doc['design']['density_kg_m3']:.4f}",
        flush=True)


if __name__ == "__main__":
    main()
