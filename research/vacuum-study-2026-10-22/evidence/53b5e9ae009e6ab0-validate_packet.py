#!/usr/bin/env python3
"""Validate preservation, transcription and arithmetic; no source solver reruns."""
import json
import math
import re
from pathlib import Path
from datetime import datetime, timezone
from intake import B, load, save, pin

checks = []


def check(name, ok, detail=None):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})


def eq(name, a, b):
    check(name, a == b, None if a == b else {"actual": sorted(a) if isinstance(a, set) else a,
                                            "expected": sorted(b) if isinstance(b, set) else b})


def close(name, a, b, atol=1e-9, rtol=1e-10):
    check(name, math.isclose(a, b, abs_tol=atol, rel_tol=rtol),
          {"actual": a, "expected": b, "atol": atol, "rtol": rtol})


def deref(d, pointer):
    for part in pointer.strip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        d = d[int(part)] if isinstance(d, list) else d[part]
    return d


base = B / "baseline030b"
register = load(B / "REGISTER.json")
oldreg = load(base / "REGISTER.json")
byrid = {x["rid"]: x for x in register["rows"]}
for row in oldreg["rows"]:
    for key, value in row.items():
        eq(f"preserved {row['rid']}/{key}", byrid[row["rid"]].get(key), value)
nfi = load(B / "NFI.json")
oldnfi = load(base / "NFI.json")
eq("all711 baseline findings exact", nfi["rows"][:len(oldnfi["rows"])], oldnfi["rows"])
byuid = {x["uid"]: x for x in nfi["rows"]}
eq("unique finding IDs", len(byuid), len(nfi["rows"]))
for n in oldnfi["rows"]:
    eq("preserved finding " + n["uid"], byuid[n["uid"]], n)
for name, count in [("LEDGER.json", 118), ("OPTIMISM-LEDGER.json", 79)]:
    old = load(base / name)["rows"]
    now = load(B / name)["rows"]
    eq(name + " baseline count", len(old), count)
    for i, row in enumerate(old):
        for key, value in row.items():
            eq(f"{name}/{i}/{key} preserved", now[i].get(key), value)
eq("original ground-first route list",
   load(B / "GROUND-FIRST.json")["previous_030b_routes"],
   load(base / "GROUND-FIRST.json")["routes"])
for name in ("original_030_ground_first", "original_030_list", "original_030_priorities"):
    if name in load(base / "GROUND-FIRST.json"):
        eq("ground-first original " + name,
           load(B / "GROUND-FIRST.json")[name], load(base / "GROUND-FIRST.json")[name])

# Verify copied sealed baseline bytes against its filed manifest.
bp = load(B / "BASELINE-PINS.json")
for a in bp["pins"]:
    if a.get("snapshot"):
        p = pin(Path(a["snapshot"]))
        check("baseline snapshot " + a["path"],
              p["sha256"] == a["sha256"] and p["bytes"] == a["bytes"])
for a in load(B / "BRIEF-PINS.json"):
    p = pin(Path(a["snapshot"]))
    check("brief snapshot " + a["path"],
          p["sha256"] == a["sha256"] and p["bytes"] == a["bytes"])
for a in load(B / "SUPPLEMENTAL-ORDERS.json")["orders"]:
    p = pin(Path(a["snapshot"]))
    check("supplemental order snapshot " + a["id"],
          p["sha256"] == a["sha256"] and p["bytes"] == a["bytes"])
    eq("supplemental order identity " + a["id"],
       load(Path(a["snapshot"]))["id"], a["id"])

intake = load(B / "INTAKE.json")
for r in intake["reports"]:
    p = pin(Path(r["report_snapshot"]))
    check("canonical report snapshot " + r["id"],
          p["sha256"] == r["report_sha256"] and p["bytes"] == r["report_bytes"])
    eq("no artifact refusals " + r["id"], r["pin_failures"], [])
    for a in r["artifacts"]:
        check("intake pin checked " + a["path"], a.get("matches") is True)
        if a.get("snapshot"):
            p = pin(Path(a["snapshot"]))
            check("new artifact snapshot " + a["path"],
                  p["sha256"] == a["sha256"] and p["bytes"] == a["bytes"])

routing = load(B / "ROUTING.json")["assignments"]
fresh = load(B / "NEW-NFI.json")
eq("new finding routing complete", set(routing), {r["uid"] for r in fresh})
doc_cache = {}
for n in fresh:
    path = n["snapshot"]
    if path not in doc_cache:
        doc_cache[path] = load(Path(path))
    eq("raw new source fields " + n["uid"],
       n["fields"], deref(doc_cache[path], n["source_json_pointer"]))
    check("routed once " + n["uid"],
          sum(x["uid"] == n["uid"] for row in register["rows"] for x in row["updates_030c"]) == 1)
    check("correct primary row " + n["uid"],
          any(x["uid"] == n["uid"] for x in byrid[routing[n["uid"]]]["updates_030c"]))
referenced = {x["uid"] for row in register["rows"]
              for key in ("sources", "updates_030b", "updates_030c")
              for x in row.get(key, [])}
eq("every source finding rendered under a row", referenced, set(byuid))

R = load(B / "RESULTS.json")
eq("installed capacity remains null", R["overall_installed_hull_SF"], None)
eq("baseline P2 variants preserved", R["P2_leads"], load(base / "RESULTS.json")["P2_leads"])
eq("baseline P3 preserved", R["P3_lead"], load(base / "RESULTS.json")["P3_lead"])
eq("baseline ordered sensitivity preserved", R["P3_ordered_fold"], load(base / "RESULTS.json")["P3_ordered_fold"])

for field, idx in (("P2_selected_lead", 6), ("P2_as_designed_250F", 0)):
    p = R[field]
    s = load(Path(p["source"]["file"]))["compute"]["fixes"][idx]
    for out, ink in (("gamma", "gamma_need"), ("Q", "Q_need"), ("usage", "max_usage"),
                     ("joining_allowance_delta_kg", "mass_change_kg")):
        eq(field + "/" + out, p[out], s[ink])
    close(field + " gamma factor", p["gamma_factor"], p["gamma"] / .20)
    close(field + " Q factor", p["Q_factor"], p["Q"] / .33)
    close(field + " compression check", 345 / p["face_pressure_plus_residual_MPa"],
          p["modes_at_required_values"]["face_345"], atol=1e-7)
    close(field + " combined screen", p["least_including_minimum_free_edge_SF"],
          min(1.0, *s["others"].values(), p["free_edge_minimum_average_SF"]))
    eq(field + " no physical SF", p["qualified_installed_hull_SF"], None)
check("as-designed exceeds named usage", R["P2_as_designed_250F"]["usage"] > 1)
check("selected within named usage", R["P2_selected_lead"]["usage"] < 1)
check("as-designed minimum edge fails", R["P2_as_designed_250F"]["free_edge_minimum_average_SF"] < 1)

for row in R["gamma_FE_029"]["lead_specified_defects"]:
    close("029 endpoint ratio " + row["case"] + row["direction"],
          row["endpoint_over_operating_pressure"],
          row["endpoint_MPa"] / R["gamma_FE_029"]["operating_pressure_MPa"])
    eq("029 no validated capacity " + row["case"] + row["direction"], row["capacity_validated"], False)
    if row["direction"] == "W":
        check("029 named weak defect below p0 " + row["case"], row["endpoint_over_operating_pressure"] < 1)
eq("029 no physical collapse measurement", R["gamma_FE_029"]["physical_collapse_measurement"], False)

mass = load(B / "P3-TUBE-MASS-CORRECTIONS.json")
eq("ten mass corrections", len(mass), 10)
for x in mass:
    close("mass delta " + x["row"], x["check_value"] - x["card_value"], x["delta"])
    idx = int(x["row"].split("/")[-1])
    source = load(B / "snapshots" / R["source_aliases"]["CHECK037"] / "RESULTS.json")["p3"][idx]
    eq("mass correction source " + x["row"], x["check_value"], source["tube_mass_kg"])
for x in R["stiffened_039_checked_constructive_points"]:
    close("O6 ratio " + x["mode"], x["bay_factor_over_020"],
          x["design"]["today_full"]["gamma_p_O5"][0] / .20)
    close("039 mode minimum " + x["mode"], x["least_SF"], min(x["SF"].values()))
    close("039 total " + x["mode"], x["design"]["masses"]["total"],
          4889.442150186961 + x["mass_shift_kg"], atol=1e-7)
    eq("O6 register label " + x["mode"], x["register_optimism_id"], "P2-O6")
o = load(B / "OPTIMISM-LEDGER.json")
eq("O5/O6 namespace", o["label_map"],
   {"P2-O5": "bond film .015/.030 lb/ft2", "P2-O6": "039 frame-bay cap, formerly source O5"})

for key in ("P3_selected_lead_041", "P3_019_variant_041"):
    x = R[key]
    m = x["mass_kg"]
    close("041 mass closure " + key,
          sum(m[k] for k in ("tube", "film", "joint", "nodes", "systems", "sag_lift_loss", "reserve")),
          m["total_with_reserve_and_sag"], atol=1e-7)
    close("041 lift account " + key, m["total_with_reserve_and_sag"], 4889.44215019, atol=1e-7)
    close("041 screen minimum " + key, x["least_screened_SF"],
          min(v for k, v in x["modes"].items() if k != "global_perfect_linear"))
    close("041 k=.2 " + key, x["modes"]["global_k0p2"], .2 * x["modes"]["global_perfect_linear"])
    check("041 sensitivity lowers screen " + key,
          x["least_including_local_max_compression_sensitivity"] < x["least_screened_SF"])
    eq("041 no qualified structural SF " + key, x["qualified_structural_SF"], None)
check("041 019 local sensitivity below unity",
      R["P3_019_variant_041"]["least_including_local_max_compression_sensitivity"] < 1)

for x in R["P2_common_account_040"]["primary_rows"]:
    close("040 endpoint bill " + x["id"],
          sum(x["endpoint_bill_kg"].values()) + x["full_gamma_Q_endpoint_payload_kg"],
          x["endpoint_lift_kg"], atol=1e-6)
    if x["R_m"] == 10:
        eq("040 R10 no float " + x["id"], x["minimum_axis_count"], None)
        check("040 R10 deficit " + x["id"], x["full_gamma_Q_endpoint_payload_kg"] < 0)
    if x["weather"] == "both":
        eq("040 both-weather no float " + x["id"], x["minimum_axis_count"], None)
for x in R["P2_common_account_040"]["necessary_points"]:
    p = x["point"]
    close("040 necessary mass closure " + x["id"],
          sum(p["bill_kg"].values()) + p["signed_payload_kg"], p["lift_kg"], atol=1e-6)
    close("040 necessary minimum " + x["id"],
          min(p["modes"].values()), p["least_shell_and_thermal_SF"])
    check("040 necessary modes at least one " + x["id"], min(p["modes"].values()) >= 1 - 1e-7)
    check("040 service nested " + x["id"],
          p["bill_kg"]["systems"] == 100 and p["vacuum"]["service_extra_charge_kg"] == 0)
for alias, field in (("043", "qualified_frame_failure_probability"), ("044", "qualified_hull_life_days")):
    eq(alias + " qualified result null", load(B / "snapshots" / R["source_aliases"][alias] / "RESULTS.json")[field], None)
close("044 plate-only index copied", R["fatigue_044"]["pad_plate_only_life_days"],
      load(B / "snapshots" / R["source_aliases"]["044"] / "RESULTS.json")["pad_plate_only_life_days"])
if (B / "SNAPSHOT-FROZEN.json").exists():
    frozen = load(B / "SNAPSHOT-FROZEN.json")
    eq("final snapshot immutable", frozen["snapshot_at"], intake["sampled_at"])
    eq("all frozen reports incorporated", frozen["report_ids"], [r["id"] for r in intake["reports"]])
authored = load(B / "AUTHORED-NFI.json")
for n in nfi["rows"]:
    if n["uid"].startswith("S"):
        eq("own finding source " + n["uid"], n["fields"], deref(authored, n["source_json_pointer"]))

# Current output links only; source snapshots remain verbatim archival documents.
for name in ("CARD.md", "GROUND-FIRST.md", "OPTIMISM-LEDGER.md", "REPORTS.md"):
    for target in re.findall(r"\]\(([^)]+)\)", (B / name).read_text()):
        if target.startswith(("http:", "https:", "#")):
            continue
        p = (B / target.split("#")[0]).resolve()
        check("current link " + name + " -> " + target, p.exists())
for name in ("RESULTS.json", "REGISTER.json", "NFI.json", "LEDGER.json",
             "OPTIMISM-LEDGER.json", "GROUND-FIRST.json", "SOURCE-INDEX.json"):
    try:
        json.loads((B / name).read_text(), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        check("strict JSON " + name, True)
    except ValueError as exc:
        check("strict JSON " + name, False, str(exc))
eq("first three preserved", load(B / "GROUND-FIRST.json")["first_three_030c"], ["T1", "T2", "T3"])
eq("snapshot consistent", R["snapshot_at"], intake["sampled_at"])
eq("coverage source findings", R["coverage"]["new_source_findings"], len(fresh))
eq("coverage all findings", R["coverage"]["total_attributed_findings"], len(nfi["rows"]))
eq("coverage canonical reports", R["coverage"]["new_canonical_reports"], len(intake["reports"]))
for row in R["pending"]:
    for rid in row["reports"]:
        check("filed status source " + rid, rid in {r["id"] for r in intake["reports"]})

failed = [c for c in checks if not c["pass"]]
result = {"schema": 1, "unit": R["unit"], "at": datetime.now(timezone.utc).isoformat(),
          "scope": "Source-preservation, transcription, current synthesis arithmetic and provenance. No independent owner-model rerun or physical qualification.",
          "checks": checks, "counts": {"total": len(checks), "passed": len(checks) - len(failed), "failed": len(failed)},
          "all_pass": not failed}
save(B / "VALIDATION.json", result)
print(result["counts"])
for item in failed:
    print(json.dumps(item, ensure_ascii=False)[:1500])
raise SystemExit(bool(failed))
