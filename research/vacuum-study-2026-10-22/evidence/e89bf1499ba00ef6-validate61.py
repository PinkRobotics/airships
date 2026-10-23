"""Independent accounting/pin invariants for the delivered calculation records."""
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


d = read("RESULTS.json")
checks = []


def check(name, condition, evidence):
    checks.append({"check": name, "passed": bool(condition), "evidence": evidence})
    assert condition, (name, evidence)


points = []
finite = True


def visit(x):
    global finite
    if isinstance(x, dict):
        if {"bill_kg", "growth_kg", "lift_kg", "payload_kg"} <= set(x):
            points.append(x)
        for v in x.values():
            visit(v)
    elif isinstance(x, list):
        for v in x:
            visit(v)
    elif isinstance(x, float):
        finite &= math.isfinite(x)


visit(d)
check("No NaN/Infinity in delivered numerical data", finite, "All numeric leaves visited.")
max_balance = max(abs(x["lift_kg"] - sum(x["bill_kg"].values()) -
                      sum(x["growth_kg"].values()) - x["payload_kg"]) for x in points)
check("Itemized mass plus growth closes each payload account", max_balance < 1e-7,
      {"records": len(points), "max_error_kg": max_balance})
check("Nominal mass and growth entries are nonnegative",
      all(v >= 0 for x in points for f in ("bill_kg", "growth_kg") for v in x[f].values()),
      "Every item, including reserves and growth.")

classes = read("sources/057--RESULTS.json")["classification"]
growth_error = 0.
for x in points:
    lead = "P2" if "faces" in x["bill_kg"] else "P3"
    for name, mass in x["bill_kg"].items():
        c = classes[lead].get(name, {}).get("type")
        if name == "cavity_capture":
            c = "hardware"
        if name == "cavity_barrier_delta":
            c = "thermal"
        if name == "cavity_battery":
            c = "battery"
        if x["maturity"] == "none" or c is None:
            rate = 0.
        elif x["maturity"] == "TRL7":
            rate = .06 if c == "battery" else .05
        else:
            rate = {"structure": .15, "hardware": .30, "thermal": .20, "battery": .25}[c]
        if name == "coating":
            expected = (mass / 1.1) * max(0., rate - .1)
        elif name == "joint_sleeves_and_allowance":
            # Existing allowance cannot be charged twice; the exact actual
            # sleeve number is checked below against the independently pinned row.
            row = next(z for z in read("sources/052--RESULTS.json")["rows"]
                       if z["R_m"] == x["R_m"] and z["weather"] == x["weather"] and z["service"] == "ground")
            expected = max(0., row["all_axes_endpoint"]["joint_actual_sleeves_kg"] * (1 + rate) - mass)
            if x["maturity"] == "none":
                expected = 0.
        else:
            expected = rate * mass
        growth_error = max(growth_error, abs(expected - x["growth_kg"][name]))
check("Correct NASA columns and embedded-margin arithmetic", growth_error < 1e-7,
      {"maximum_line_error_kg": growth_error, "TRL7_hardware": .05, "TRL7_battery": .06,
       "concept_battery": .25, "checked_against": "pinned source classifications and actual sleeves"})

witnesses = [s["solution"] for x in d["p2"] for s in x["single"] if s.get("factor") is not None]
combined = [x["combination"]["solution"] for x in d["p2"]]
check("All 16 finite single-variable targets meet the scalar constraints",
      len(witnesses) == 16 and min(x["payload_kg"] for x in witnesses) >= -.1
      and min(min(x["modes"].values()) for x in witnesses) >= 1 - 1e-8,
      {"count": len(witnesses), "min_payload_kg": min(x["payload_kg"] for x in witnesses),
       "min_constraint_ratio": min(min(x["modes"].values()) for x in witnesses)})
check("All 12 combination witnesses meet the same constraints",
      len(combined) == 12 and min(x["payload_kg"] for x in combined) >= -.1
      and min(min(x["modes"].values()) for x in combined) >= 1 - 1e-8,
      {"count": len(combined), "min_payload_kg": min(x["payload_kg"] for x in combined),
       "min_constraint_ratio": min(min(x["modes"].values()) for x in combined)})
check("Product values match their factors and do not exceed best single",
      all(abs(math.prod(x["combination"]["factors"].values()) - x["combination"]["factor_product"]) < 1e-10
          and x["combination"]["factor_product"] <= min(s["factor"] for s in x["single"] if s["factor"] is not None) + 1e-6
          for x in d["p2"]), "Twelve case/basis products.")
check("P2 vacuum pressure and factor physical caps retained",
      all(x["vacuum"]["hot_pressure_24h_Pa"] <= x["vacuum"]["pressure_limit_Pa"]*(1+1e-8)
          and x["properties"]["gamma"] <= 1+1e-12 and x["properties"]["Q"] <= .82+1e-12
          for x in witnesses+combined), "24-hour vacuum screen, gamma≤1 and Q≤0.82.")
check("P3 retention capped and battery explicit",
      all(x["retention"] <= 1 and abs(x["bill_kg"]["cavity_battery"] - 7/9) < 1e-12
          for x in points if "retention" in x), "Perfect retention is a cap, not an extrapolation above one.")
check("P3 named-lever and stronger relief bounds remain negative",
      all(x["combination"]["infinite_improvements"]["payload_kg"] < 0
          and x["combination"]["irreducible_payload_upper_bound_kg"] < 0
          and x["combination"]["relief_generous_payload_upper_bound_kg"] < 0 for x in d["p3"]),
      {"least_negative_relief_bound_kg": max(x["combination"]["relief_generous_payload_upper_bound_kg"] for x in d["p3"]),
       "scope": "inherited constant-g/R family only"})

repro = read("REPRODUCTION.json")
direct = [x for x in repro if x["lead"] == "P2" and x["R"] in (10, 12)]
p3 = [x for x in repro if x["lead"] == "P3"]
check("Reproduce four direct P2 frozen bills",
      len(direct) == 4 and max(abs(x["witness_payload_error"]) for x in direct) < 1e-8,
      {"max_fixed_geometry_error_kg": max(abs(x["witness_payload_error"]) for x in direct),
       "max_optimizer_difference_kg": max(abs(x["reoptimized_payload"] - x["upstream_payload"]) for x in direct)})
check("Reproduce six seven-day P3 source rows",
      len(p3) == 6 and max(abs(x["payload_error"]) for x in p3) < 2e-10,
      {"max_payload_error_kg": max(abs(x["payload_error"]) for x in p3),
       "max_capture_error_kg": max(abs(x["capture_error"]) for x in p3)})

pins = read("INPUTS.json")
count = 0
for x in pins["upstream_files_actually_copied_or_inspected"]:
    p = x["local_copy"]
    raw = Path(p["path"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == x["upstream"]["sha256"]
    assert len(raw) == x["upstream"]["bytes"]
    count += 1
for x in pins["brief_integrity_and_authority_pins"]:
    raw = Path(x["recovered_copy"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == x["declared"]["sha256"]
    assert len(raw) == x["declared"]["bytes"]
    count += 1
check("All used local data and dispatch brief/authority pins match", True,
      {"verified_files": count, "PROCESS_v2_current_source_drift": "recovered original bytes match declared dispatch pin"})
nfi = read("NFI.json")["items"]
check("NFI identifiers are unique and review is explicitly pending",
      len({x["id"] for x in nfi}) == len(nfi) and "pending" in d["review"]["independent"].lower()
      and d["qualified_hull_SF"] is None,
      {"nfi_count": len(nfi), "independent_review": d["review"]["independent"]})
for x in d["beryllium"]:
    assert abs(x["nominal_share_percent"] - 100*x["nominal_face_Be_kg"]/430000) < 1e-12
check("Be shares use mine-content denominator and separate nominal/budget", True,
      {"denominator_kg_Be": 430000, "rows": len(d["beryllium"])})

output = {"schema": "mainline061-validation-v1", "unit": d["unit"], "status": "PASS",
          "performed_by": "author arithmetic checks; not independent REVIEW-A",
          "measured_at": datetime.now().astimezone().isoformat(), "checks": checks}
(ROOT / "VALIDATION.json").write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
print(f"PASS: {len(checks)} accounting, closure, source and handoff checks; {len(points)} itemized accounts.")
