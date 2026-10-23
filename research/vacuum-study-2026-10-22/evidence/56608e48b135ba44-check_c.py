"""REVIEW-C independent arithmetic. Uses this seat's 065 copy of model63, not 064's files.

QUESTIONABLE inputs. PROJECTION payloads.
"""
import json
import math
import os
import sys
from datetime import datetime
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

MINE = Path("unpublished-local-ref:1e7c72cbab3c5a3f")
sys.path.insert(0, str(MINE))
from model63 import p2_opt  # noqa: E402

OUT = Path(__file__).resolve().parent
CASES = ((20, "ISA"), (20, "optimistic"), (30, "ISA"), (30, "optimistic"))
LAWS = (
    ("Q082_gamma_handbook", None),
    ("Q033_gamma_handbook", 0.33),
)


def slim(point):
    props = point["properties"]
    return {
        "payload_kg": point["payload_kg"],
        "Q": props["Q"],
        "gamma": props["gamma"],
        "Vc": props["Vc"],
        "E_Pa": props["E_Pa"],
        "binding": point["binding"][0][0],
        "tf_m": point["geometry"]["tf_m"],
        "tc_m": point["geometry"]["tc_m"],
    }


def density_factor(r, weather, q):
    factors = {} if q is None else {"Q": q / 0.82}

    def at(factor, n):
        facts = dict(factors)
        facts["face_density"] = factor
        return p2_opt(r, weather, facts, basis="endpoint", maturity="concept",
                      n=n, revert=("gamma",))

    lo, hi = 1.0, 1.02
    point = at(1.0, 200)
    if point is not None and point["payload_kg"] >= 0:
        return 1.0, point
    for _ in range(16):
        point = at(hi, 140)
        if point is not None and point["payload_kg"] >= 0:
            break
        lo, hi = hi, hi * 1.2
        if hi > 6:
            return None, point
    for _ in range(20):
        mid = math.sqrt(lo * hi)
        point = at(mid, 160)
        if point is not None and point["payload_kg"] >= 0:
            hi = mid
        else:
            lo = mid
    final = at(hi * (1 + 1e-7), 320)
    return hi, final


def main():
    started = datetime.now().astimezone().isoformat()
    rows = []
    for r, weather in CASES:
        for label, q in LAWS:
            print(f"{label} R{r} {weather}", flush=True)
            factors = {} if q is None else {"Q": q / 0.82}
            allow = {}
            for maturity in ("concept", "TRL7"):
                point = p2_opt(r, weather, factors, basis="endpoint", maturity=maturity,
                               n=260, revert=("gamma",))
                allow[maturity] = slim(point)
            factor, closed = density_factor(r, weather, q)
            row = {
                "R_m": r, "weather": weather, "law": label,
                "allowances": allow,
                "density_factor": factor,
                "closure_density_kg_m3": None if factor is None else 1850.0 / factor,
                "closure_payload_kg": None if closed is None else closed["payload_kg"],
                "closure_binding": None if closed is None else closed["binding"][0][0],
                "closure_Vc": None if closed is None else closed["properties"]["Vc"],
            }
            rows.append(row)
            c = allow["concept"]
            print(f"  factor {factor} concept {c['payload_kg']:.1f} "
                  f"TRL7 {allow['TRL7']['payload_kg']:.1f} "
                  f"Q {c['Q']} gamma {c['gamma']} Vc {c['Vc']} {c['binding']}", flush=True)
    e = 293.6e3
    specific = {
        "E_MPa": e,
        "at_1850": e / 1850.0,
        "note": "endpoint modulus stays 293.6 GPa when only gamma is reverted",
    }
    path = OUT / "CHECK.json"
    path.write_text(json.dumps({
        "tag": "QUESTIONABLE / PROJECTION",
        "started": started,
        "completed": datetime.now().astimezone().isoformat(),
        "route": "this seat's 065 copy of model63.py, revert gamma only, Q by factor q/0.82",
        "specific_modulus_MPa_per_kg_m3": specific,
        "rows": rows,
    }, indent=2) + "\n")
    print("WROTE", path, flush=True)


if __name__ == "__main__":
    main()
