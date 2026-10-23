"""MAINLINE-065 driver. model61.py and model63.py are copied unchanged.

QUESTIONABLE inputs. PROJECTION payloads. No qualified hull safety factor.
Supported Q is the model's handbook coefficient 0.33. Gamma is either the
handbook step or 063's favorable ramp. The classical cap 0.82 is the
endpoint anchor, recorded for comparison.
"""
import hashlib
import json
import math
import os
import time
from datetime import datetime
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

ROOT = Path(__file__).resolve().parent

PINS = json.loads((ROOT / "MODEL-PINS.json").read_text())
for name in ("model63.py", "model61.py", "source61.py", "SOURCE-INDEX.json"):
    data = (ROOT / name).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != PINS[name]["sha256"] or len(data) != PINS[name]["bytes"]:
        raise SystemExit(f"pin mismatch {name}")

from model61 import p2_opt as opt_61
from model63 import BETA
from model63 import p2_opt as opt_63

CASES = ((20, "ISA"), (20, "optimistic"), (30, "ISA"), (30, "optimistic"))
EXPECT_PAYLOAD = {
    (20, "ISA", "concept"): -2473.5,
    (20, "optimistic", "concept"): -3772.7,
    (30, "ISA", "concept"): -6582.7,
    (30, "optimistic", "concept"): -10973.6,
    (20, "ISA", "TRL7"): 1194.6,
    (20, "optimistic", "TRL7"): -29.9,
    (30, "ISA", "TRL7"): 5594.8,
    (30, "optimistic", "TRL7"): 1456.5,
}
LAWS = (
    ("supported_Q_favorable_ramp", ("Q",)),
    ("supported_Q_handbook_gamma", ("Q", "gamma")),
)


def slim(point):
    if not isinstance(point, dict):
        return None
    props = point["properties"]
    return {
        "payload_kg": point["payload_kg"],
        "geometry": point["geometry"],
        "properties": {
            "Q": props["Q"],
            "gamma": props["gamma"],
            "Vc": props["Vc"],
            "E_Pa": props["E_Pa"],
            "density_kg_m3": props["density_kg_m3"],
        },
        "binding": point["binding"],
        "modes_face_wrinkling": point["modes"]["face_wrinkling"],
        "lift_kg": point["lift_kg"],
        "growth_total_kg": point["growth_total_kg"],
        "mass_before_growth_kg": point["mass_before_growth_kg"],
    }


def density_factor(r, weather, revert=(), basis="endpoint"):
    """Smallest face-density divisor that makes concept payload non-negative."""
    def at(factor, n):
        return opt_63(r, weather, {"face_density": factor}, basis=basis,
                      maturity="concept", n=n, revert=revert)

    base = at(1.0, 200)
    if base is not None and base["payload_kg"] >= 0:
        return {"factor": 1.0, "status": "already closes", "solution": base,
                "root_bracket": None}
    lo, hi = 1.0, 1.02
    point = None
    for _ in range(16):
        point = at(hi, 140)
        if point is not None and point["payload_kg"] >= 0:
            break
        lo, hi = hi, hi * 1.2
        if hi > 6:
            return {"factor": None, "status": "not closed below factor 6",
                    "solution": point, "root_bracket": [lo, hi]}
    for _ in range(20):
        mid = math.sqrt(lo * hi)
        point = at(mid, 160)
        if point is not None and point["payload_kg"] >= 0:
            hi = mid
        else:
            lo = mid
    final = at(hi * (1 + 1e-7), 320)
    return {"factor": hi, "status": "conditional closure", "solution": final,
            "root_bracket": [lo, hi]}


def allowances(r, weather, revert=(), basis="endpoint"):
    out = {}
    for maturity in ("concept", "TRL7"):
        point = opt_63(r, weather, basis=basis, maturity=maturity, n=260, revert=revert)
        out[maturity] = slim(point)
    return out


def gate_identity():
    t0 = time.perf_counter()
    left = opt_61(30, "ISA", basis="endpoint", maturity="concept", n=80)
    right = opt_63(30, "ISA", basis="endpoint", maturity="concept", n=80)
    dt = time.perf_counter() - t0
    if abs(left["payload_kg"] - right["payload_kg"]) > 1e-4:
        raise SystemExit(f"opt mismatch {left['payload_kg']} vs {right['payload_kg']}")
    return {"one_opt_pair_s": dt, "n80_payload_kg": left["payload_kg"],
            "beta": BETA}


def main():
    started = datetime.now().astimezone().isoformat()
    print("GATE", flush=True)
    gate = gate_identity()
    print("GATE", json.dumps(gate), flush=True)
    anchors = []
    for r, weather in CASES:
        print(f"ANCHOR endpoint R{r} {weather}", flush=True)
        allow = allowances(r, weather, (), "endpoint")
        got = allow["concept"]["payload_kg"]
        expect = EXPECT_PAYLOAD[(r, weather, "concept")]
        if abs(got - expect) > 1.0:
            raise SystemExit(f"payload gate {r} {weather}: {got} vs {expect}")
        trl = allow["TRL7"]["payload_kg"]
        expect_trl = EXPECT_PAYLOAD[(r, weather, "TRL7")]
        if abs(trl - expect_trl) > 1.0:
            raise SystemExit(f"TRL7 gate {r} {weather}: {trl} vs {expect_trl}")
        anchors.append({"R_m": r, "weather": weather, "law": "classical_cap_Q_favorable_ramp",
                        "basis": "endpoint", "revert": [], "allowances": allow,
                        "tag": "comparison anchor; Q=0.82 is not an installed test value"})
        print(f"  concept {got:.1f} TRL7 {trl:.1f} Q {allow['concept']['properties']['Q']} "
              f"gamma {allow['concept']['properties']['gamma']}", flush=True)
    rows = []
    for r, weather in CASES:
        for label, revert in LAWS:
            print(f"LAW {label} R{r} {weather}", flush=True)
            allow = allowances(r, weather, revert, "endpoint")
            closed = density_factor(r, weather, revert, "endpoint")
            row = {"R_m": r, "weather": weather, "law": label, "basis": "endpoint",
                   "revert": list(revert), "allowances": allow,
                   "density_factor": closed["factor"], "density_status": closed["status"],
                   "closure": slim(closed["solution"]),
                   "root_bracket": closed["root_bracket"]}
            rows.append(row)
            concept = allow["concept"]
            print(f"  factor {closed['factor']} concept {concept['payload_kg']:.1f} "
                  f"TRL7 {allow['TRL7']['payload_kg']:.1f} "
                  f"Q {concept['properties']['Q']} gamma {concept['properties']['gamma']} "
                  f"Vc {concept['properties']['Vc']}", flush=True)
    out = {"tag": "QUESTIONABLE / PROJECTION", "qualified_hull_SF": None,
           "started": started, "gate": gate, "anchors": anchors, "rows": rows,
           "completed": datetime.now().astimezone().isoformat()}
    path = ROOT / "CALCULATIONS.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print("WROTE", path, flush=True)


if __name__ == "__main__":
    main()
