"""MAINLINE-069 payload ranking at the filed design density.

The design point is already in RUN.json. These rows do not replace it.
A frozen geometry does not change mass when only a margin term changes,
so each unsourced term is removed and the geometry is resized at the
same face density. QUESTIONABLE. PROJECTION. No finite-element run.
"""
import inspect
import json
import os
import sys
from datetime import datetime

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(OUT, "model"))
import model63  # noqa: E402

REVERT = ("Q", "gamma")
RUN = json.load(open(os.path.join(OUT, "RUN.json")))
FACTOR = RUN["design"]["factor_used"]
TF = RUN["design"]["primary"]["geometry"]["tf_m"]
TC = RUN["design"]["primary"]["geometry"]["tc_m"]
BASE = RUN["design"]["primary"]["payload_kg"]
ORIGINAL = inspect.getsource(model63.p2)


def install(source):
    local = {}
    exec(compile(source, "mainline069b_p2.py", "exec"), model63.__dict__, local)
    model63.p2 = local["p2"]


def patched(name):
    pairs = {
        "as_designed": (),
        "no_kc": (("kc = np.where(vc <= 2., 1-vc/4, 1/vc)", "kc = np.ones_like(vc)"),),
        "no_cure": (("cure = kb*12.3e-6*dtc*tc/(2*tf)", "cure = np.zeros_like(tf)"),),
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


def row_from(point, name, route, kind):
    modes = {key: float(value) for key, value in point["modes"].items()}
    payload = float(point["payload_kg"])
    return {
        "id": name,
        "kind": kind,
        "payload_kg": payload,
        "delta_vs_design_payload_kg": payload - BASE,
        "floats": payload >= 0 and min(modes.values()) >= 1 - 1e-8,
        "geometry": {key: float(value) for key, value in point["geometry"].items()},
        "global_buckling": modes["global_buckling"],
        "face_wrinkling": modes["face_wrinkling"],
        "binding": [[n, float(v)] for n, v in point["binding"]],
        "route": route,
        "tag": "QUESTIONABLE",
    }


def main():
    natural = float(model63.BETA)
    if abs(natural - 0.682327803828082) > 1e-9:
        raise SystemExit(f"unexpected natural BETA {natural}")
    model63.BETA = 1.0
    started = datetime.now().astimezone().isoformat()
    factors = {"Q": 1.0, "face_density": FACTOR}
    rows = []
    for name, route in (
        ("as_designed", "control at the design density"),
        ("no_kc", "analysis: source kc=1-Vc/4 in CR-1457 or DOI 10.2514/3.5568 or 10.2514/3.1932"),
        ("no_cure", "analysis: source the cure stress in those same documents"),
        ("no_grad_bend", "analysis: source the 11.3e-6 gradient and bending stress"),
        ("no_pressure", "analysis: source the 1.01 floor and QWIND; 040 names unopened 014b"),
    ):
        print(name, flush=True)
        patched(name)
        frozen = model63.p2(
            30, "optimistic", TF, TC, factors=factors, basis="endpoint",
            maturity="concept", detail=True, revert=REVERT)
        resized = model63.p2_opt(
            30, "optimistic", factors, basis="endpoint", maturity="concept",
            n=200, revert=REVERT)
        if resized is None:
            raise SystemExit(f"{name} did not reoptimize")
        rows.append(row_from(frozen, name + "_frozen_geometry", route, "frozen"))
        rows.append(row_from(resized, name + "_resized", route, "resized"))
        install(ORIGINAL)
    print("today admissible", flush=True)
    today_factors = {"Q": 1.0, "face_density": 1.0}
    for maturity in ("concept", "TRL7"):
        point = model63.p2_opt(
            30, "optimistic", today_factors, basis="endpoint",
            maturity=maturity, n=200, revert=REVERT)
        rows.append(row_from(
            point, f"today_{maturity}_R30_optimistic",
            "admissible line: density 1850, gamma 0.20, Q 0.33",
            "today"))
    doc = {
        "tag": "QUESTIONABLE / PROJECTION",
        "qualified_hull_SF": None,
        "design_payload_kg": BASE,
        "design_factor": FACTOR,
        "started": started,
        "rows": rows,
        "completed": datetime.now().astimezone().isoformat(),
    }
    path = os.path.join(OUT, "PROBES.json")
    with open(path, "w") as handle:
        json.dump(doc, handle, indent=2)
        handle.write("\n")
    for item in rows:
        print(f"{item['id']:40} {item['payload_kg']:12.2f} "
              f"d {item['delta_vs_design_payload_kg']:10.2f} "
              f"buck {item['global_buckling']:.4f} wr {item['face_wrinkling']:.4f}",
              flush=True)


if __name__ == "__main__":
    main()
