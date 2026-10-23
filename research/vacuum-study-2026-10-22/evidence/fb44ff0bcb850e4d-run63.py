"""MAINLINE-063: one-at-a-time handbook reversion of 061's five favorable P2 inputs.

QUESTIONABLE inputs. PROJECTION targets. No qualified hull safety factor.
"""
import json
import math
import os
import time
from datetime import datetime

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

from model61 import p2 as p2_61
from model61 import p2_opt as opt_61
from model63 import p2 as p2_63
from model63 import p2_opt as opt_63
from model63 import single_p2

ROOT_KEYS = ("face_modulus", "face_strength", "Q", "gamma", "bond_film")
CASES = ((20, "ISA"), (20, "optimistic"), (30, "ISA"), (30, "optimistic"))
# 061 CARD / RESULTS concept-closure density factors, for the reproduction gate.
EXPECT_FACTOR = {
    (20, "ISA", "endpoint"): 1.0765995707382916,
    (20, "optimistic", "endpoint"): 1.1183200766737194,
    (30, "ISA", "endpoint"): 1.05931309108432,
    (30, "optimistic", "endpoint"): 1.1001179439361228,
    (20, "ISA", "handbook"): 2.2112584452114,
    (20, "optimistic", "handbook"): 2.320740881690631,
    (30, "ISA", "handbook"): 2.143497037041589,
    (30, "optimistic", "handbook"): 2.24802068463002,
}
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


def payload_of(point):
    if point is None:
        return None
    return point["payload_kg"] if isinstance(point, dict) else float(point[0])


def gate_identity():
    """Unreverted model63 must match model61 on both bases, pointwise and optimized."""
    samples = [(20, "ISA", 0.0016, 0.044), (30, "optimistic", 0.0025, 0.066)]
    for r, weather, tf, tc in samples:
        for basis in ("endpoint", "handbook"):
            a = p2_61(r, weather, tf, tc, basis=basis, maturity="concept")
            b = p2_63(r, weather, tf, tc, basis=basis, maturity="concept")
            if abs(float(a[0]) - float(b[0])) > 1e-6:
                raise SystemExit(f"point mismatch {r} {weather} {basis}: {a[0]} vs {b[0]}")
    t0 = time.perf_counter()
    left = opt_61(30, "ISA", basis="endpoint", maturity="concept", n=80)
    right = opt_63(30, "ISA", basis="endpoint", maturity="concept", n=80)
    dt = time.perf_counter() - t0
    if abs(left["payload_kg"] - right["payload_kg"]) > 1e-4:
        raise SystemExit(f"opt mismatch {left['payload_kg']} vs {right['payload_kg']}")
    # All five reverted on the endpoint basis must match the handbook basis.
    mixed = opt_63(30, "ISA", basis="endpoint", maturity="concept", n=80, revert=ROOT_KEYS)
    pure = opt_63(30, "ISA", basis="handbook", maturity="concept", n=80)
    if abs(mixed["payload_kg"] - pure["payload_kg"]) > 1e-3:
        raise SystemExit(f"revert-all mismatch {mixed['payload_kg']} vs {pure['payload_kg']}")
    return {"one_opt_pair_s": dt, "n80_payload_kg": left["payload_kg"]}


def density_factor(r, weather, revert=(), basis="endpoint"):
    """Smallest face-density divisor that makes concept payload non-negative."""
    def at(factor, n):
        facts = {"face_density": factor}
        return opt_63(r, weather, facts, basis=basis, maturity="concept",
                      n=n, revert=revert)

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


def slim(point):
    if not isinstance(point, dict):
        return None
    return {"payload_kg": point["payload_kg"],
            "geometry": point["geometry"],
            "properties": point["properties"],
            "binding": point["binding"],
            "lift_kg": point["lift_kg"],
            "growth_total_kg": point["growth_total_kg"],
            "mass_before_growth_kg": point["mass_before_growth_kg"]}


def allowances(r, weather, revert=(), basis="endpoint"):
    out = {}
    for maturity in ("concept", "TRL7"):
        point = opt_63(r, weather, basis=basis, maturity=maturity, n=260, revert=revert)
        out[maturity] = slim(point)
    return out


def main():
    started = datetime.now().astimezone().isoformat()
    print("GATE", flush=True)
    gate = gate_identity()
    print("GATE", json.dumps(gate), flush=True)
    rows = []
    for r, weather in CASES:
        for label, basis, revert in (
            ("endpoint", "endpoint", ()),
            ("handbook", "handbook", ()),
        ):
            print(f"REPRO {label} R{r} {weather}", flush=True)
            allow = allowances(r, weather, revert, basis)
            closed = density_factor(r, weather, revert, basis)
            got = allow["concept"]["payload_kg"]
            if label == "endpoint":
                expect = EXPECT_PAYLOAD[(r, weather, "concept")]
                if abs(got - expect) > 1.0:
                    raise SystemExit(f"payload gate {r} {weather}: {got} vs {expect}")
                trl = allow["TRL7"]["payload_kg"]
                expect_trl = EXPECT_PAYLOAD[(r, weather, "TRL7")]
                if abs(trl - expect_trl) > 1.0:
                    raise SystemExit(f"TRL7 gate {r} {weather}: {trl} vs {expect_trl}")
            factor = closed["factor"]
            expect_f = EXPECT_FACTOR[(r, weather, label)]
            if factor is None or abs(factor - expect_f) / expect_f > 0.002:
                raise SystemExit(f"factor gate {r} {weather} {label}: {factor} vs {expect_f}")
            rows.append({"R_m": r, "weather": weather, "swap": label, "basis": basis,
                         "revert": list(revert), "allowances": allow,
                         "density_factor": factor, "density_status": closed["status"],
                         "closure": slim(closed["solution"])})
            print(f"  factor {factor:.6f} concept {got:.1f}", flush=True)
    singles = []
    for r, weather in CASES:
        for key in ROOT_KEYS:
            print(f"SWAP {key} R{r} {weather}", flush=True)
            allow = allowances(r, weather, (key,), "endpoint")
            closed = density_factor(r, weather, (key,), "endpoint")
            row = {"R_m": r, "weather": weather, "swap": key, "basis": "endpoint",
                   "revert": [key], "allowances": allow,
                   "density_factor": closed["factor"], "density_status": closed["status"],
                   "closure": slim(closed["solution"])}
            singles.append(row)
            rows.append(row)
            print(f"  factor {closed['factor']} concept {allow['concept']['payload_kg']:.1f} "
                  f"TRL7 {allow['TRL7']['payload_kg']:.1f}", flush=True)
    interactions = []
    for r, weather in CASES:
        base = next(x["density_factor"] for x in rows
                    if x["R_m"] == r and x["weather"] == weather and x["swap"] == "endpoint")
        full = next(x["density_factor"] for x in rows
                    if x["R_m"] == r and x["weather"] == weather and x["swap"] == "handbook")
        ranked = []
        for key in ROOT_KEYS:
            factor = next(x["density_factor"] for x in singles
                          if x["R_m"] == r and x["weather"] == weather and x["swap"] == key)
            share = math.log(factor / base) / math.log(full / base)
            ranked.append({"input": key, "density_factor": factor, "log_share": share})
        ranked.sort(key=lambda item: item["log_share"], reverse=True)
        pair = tuple(item["input"] for item in ranked[:2])
        print(f"PAIR {pair} R{r} {weather}", flush=True)
        allow = allowances(r, weather, pair, "endpoint")
        closed = density_factor(r, weather, pair, "endpoint")
        fi = ranked[0]["density_factor"]
        fj = ranked[1]["density_factor"]
        both = closed["factor"]
        sum_log = math.log(fi / base) + math.log(fj / base)
        joint_log = math.log(both / base)
        interactions.append({
            "R_m": r, "weather": weather, "ranked": ranked, "pair": list(pair),
            "allowances": allow, "density_factor": both,
            "density_status": closed["status"], "closure": slim(closed["solution"]),
            "sum_of_log_deltas": sum_log, "joint_log_delta": joint_log,
            "interaction_ratio": joint_log / sum_log,
            "log_residual_after_all_five_shares": 1 - sum(item["log_share"] for item in ranked),
        })
        print(f"  pair factor {both:.6f} ratio {joint_log / sum_log:.4f}", flush=True)
    handbook_alone = []
    for weather in ("ISA", "optimistic"):
        for key in ROOT_KEYS:
            print(f"HANDBOOK-ALONE {key} R30 {weather}", flush=True)
            found = single_p2(30, weather, key, basis="handbook")
            handbook_alone.append({
                "R_m": 30, "weather": weather, "property": key,
                "status": found["status"], "factor": found.get("factor"),
                "binding": None if not found.get("solution") else found["solution"].get("binding"),
                "best_binding": None if not isinstance(found.get("best"), dict) else found["best"].get("binding"),
            })
            print(f"  {found['status']} {found.get('factor')}", flush=True)
    out = {"tag": "QUESTIONABLE / PROJECTION", "qualified_hull_SF": None,
           "started": started, "gate": gate, "rows": rows,
           "interactions": interactions, "handbook_alone_R30": handbook_alone,
           "completed": datetime.now().astimezone().isoformat()}
    path = os.path.join(os.path.dirname(__file__), "CALCULATIONS.json")
    with open(path, "w") as stream:
        json.dump(out, stream, indent=2)
        stream.write("\n")
    print("WROTE", path, flush=True)


if __name__ == "__main__":
    main()
