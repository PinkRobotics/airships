"""Assemble this review's documents from its completed evidence."""
from pathlib import Path
import datetime as dt
import hashlib
import json

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def read(name):
    return json.loads((B/name).read_text())


def write(name, data):
    (B/name).write_text(json.dumps(data, indent=2, allow_nan=False)+"\n")


def pin(p):
    data = p.read_bytes()
    return {"path": str(p.resolve()), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


weather = read("checks/058-COVERAGE-height27.29-humidityTrue.json")
edges = read("checks/058-EDGES.json")
thermal = read("checks/058-THERMAL-MIXED-CONVECTION.json")
arithmetic = read("checks/061-ARITHMETIC.json")

fixes = [
    {
        "id": "F-A2-058-P2-HARDWARE",
        "card": "MAINLINE058",
        "owner": "ref-55cff924be25afe6f9dd",
        "field": "CARD.md Heathrow coverage headlines/table; RESULTS.levers/finish_heathrow; days058b mass_kg and full_day_fraction",
        "finding": "The site-coverage configurations include relief and ballast operationally but use hull mass without the separately declared valve/bladder hardware.",
        "status": "unreviewed",
        "meaning": "Demonstrated accounting omission; proposed corrected rows have not undergone a fix-review round.",
        "rows": [],
        "proposed_fix": "Carry the exact configuration hardware into the site lift test and update the named coverage rows. Recompute the least-optimism/radius selections before using them; this review does not choose a replacement minimum radius.",
        "evidence": ["checks/058-COVERAGE-height27.29-humidityTrue.json", "inputs/058/RESULTS.json", "sources/days058b.json"],
    },
    {
        "id": "F-A2-058-P3-HARDWARE",
        "card": "MAINLINE058",
        "owner": "ref-55cff924be25afe6f9dd",
        "field": "CARD.md P3 standard-pressure climb+ballast coverage; days058b P3 design+0/mask15 mass_kg",
        "finding": "The standard-pressure P3 coverage likewise uses hull mass. It omits at least the declared common 5 kg valve, and no matched bladder mass is present in the coverage row.",
        "status": "unreviewed",
        "meaning": "The valve-only recount is an upper bound, not a complete repaired P3 bill.",
        "rows": [],
        "proposed_fix": "Specify the standard-pressure configuration's ballast capacity and associated hardware, add its mass, and update the P3 coverage and target witnesses. Preserve the missing cold-screen and operation limits.",
        "evidence": ["checks/058-COVERAGE-height27.29-humidityTrue.json", "inputs/058/RESULTS.json", "sources/days058b.json"],
    },
]
for row in weather["selected_cases"]:
    if row["lead"] == "P2" and row["added_hardware_kg"] > 0:
        fixes[0]["rows"].append({
            "R_m": row["R_m"], "finish": row["finish"], "hull": row["hull"],
            "operation": row["operation"], "owner_mass_kg": row["owner_mass_kg"],
            "added_hardware_kg": row["added_hardware_kg"],
            "review_mass_kg": row["owner_mass_kg"]+row["added_hardware_kg"],
            "owner_fraction": row["owner_day_fraction"],
            "review_fraction": row["independent_with_hardware"]["full_day_fraction"],
            "owner_days": row["independent_at_owner_mass"]["days_count"],
            "review_days": row["independent_with_hardware"]["days_count"],
            "denominator_days": 3559,
        })
    elif row["lead"] == "P3":
        fixes[1]["rows"].append({
            "R_m": row["R_m"], "hull": row["hull"], "selection": "mask15",
            "owner_mass_kg": row["owner_mass_kg"], "minimum_added_hardware_kg": 5,
            "owner_fraction": row["owner_day_fraction"],
            "review_valve_only_upper_fraction": row["independent_with_valve_only"]["full_day_fraction"],
            "owner_days": row["independent_at_owner_mass"]["days_count"],
            "review_valve_only_days": row["independent_with_valve_only"]["days_count"],
            "denominator_days": 3559,
        })
write("FIXES.json", {"unit": UNIT, "one_round": True, "owner_files_changed": False, "rows": fixes})

nfi = [
    {
        "id": "N-A2-058-RADIUS",
        "card": "058",
        "state": "unresolved",
        "claim": "A2-09",
        "missing_source_or_test": "A complete per-configuration valve/bladder bill and an independent coverage/selection check after carrying it into the named least-optimism witnesses.",
        "detail": "P2's R12/95% witness uses lowe_night at design -10 hPa, and R20/99% uses mask3 lowe_night at -20 hPa. They differ from the static AlAOC rows repriced here. Those AlAOC rows fall to 94.156% and 98.960%, but this does not prove a new minimum radius across all finishes/subsets. P3 also needs its matched standard-pressure bladder.",
    },
    {
        "id": "N-A2-061-PRODUCT-RANKING",
        "card": "061",
        "state": "unresolved",
        "claim": "A2-13",
        "missing_source_or_test": "An independent constrained-search comparison over the stated eight factors and two thicknesses, with feasible witnesses and numerical tolerances.",
        "detail": "The all-density candidate independently closes the supplied bill and its factor product matches. This spot review does not reproduce the ranking against every mixed candidate. 061 itself correctly labels the result best feasible found, not a global-optimality certificate; this is not a demonstrated owner error.",
    },
    {
        "id": "N-A2-061-CURE",
        "card": "061",
        "state": "carried",
        "claim": "A2-17",
        "missing_source_or_test": "A validated residual-stress field and buckling calculation establishing how cure mismatch enters global demand.",
        "detail": "The frozen and new numerical accounts reproduce separately. Treat the cure-compression denominator as the declared scenario, not a proved correction to installed-hull mechanics.",
    },
    {
        "id": "N-A2-058-FINISH",
        "card": "058",
        "state": "carried",
        "claim": "A2-04",
        "missing_source_or_test": "Installed Be-skin optical, mass, adhesion, aging, wet-surface and thermal-cycle evidence, including the switchable finish.",
        "detail": "Sheldahl's alpha<=0.14 and epsilon<=0.05 specifications concern an aluminized polyimide film with acrylic protection. Holding 8.33 g/m2 while transferring those optics to Be is already disclosed as a projection. The numerical thermal shift is reproducible, not qualified hardware.",
    },
    {
        "id": "N-A2-058-OPERATIONS",
        "card": "058",
        "state": "carried",
        "missing_source_or_test": "A chronological air-admission/ballast/ground-service mission model and corresponding physical evidence, plus P3's cold and humidity limits.",
        "detail": "The independent recount preserves the hourly best-of-trim/climb rule. Admitted air cannot be removed in flight, so independent hourly feasibility is not mission availability. Gusts outside the design, precipitation, hail, icing and lightning are excluded. Missing weather days are excluded from the denominator.",
    },
    {
        "id": "N-A2-061-MATERIAL",
        "card": "061",
        "state": "carried",
        "missing_source_or_test": "Qualified replacement-face, core, joints and full-member/frame data, including coupled thermal and density properties.",
        "detail": "A lower face-density factor is a synthetic material target at fixed mechanics and thermal constants, not a reduction in elemental Be density. The P3 impossibility bound applies only to the named levers and constant-g/R family.",
    },
    {
        "id": "N-A2-058-WEATHER-QC",
        "card": "058",
        "state": "review_limit",
        "missing_source_or_test": "A full independent raw-record selection and quality-flag audit if the processed ten-year dataset is to be qualified.",
        "detail": "This review checks all processed-hour/day counts and 24 raw NOAA observations. It does not claim to independently reproduce the complete NOAA conversion pipeline.",
    },
]
write("NFI.json", {"unit": UNIT, "tag": "QUESTIONABLE / PROJECTION", "rows": nfi})

rows = read("LOAD-BEARING.json")["claims"]
answers = {
 "A2-01": ("it reproduces", "103953.19780784745 and 98019.41905822608 Pa, independently from the stated hot/saturated maximum-pressure corner.", ["checks/058-EDGES.json"]),
 "A2-02": ("it reproduces", "P2 R10/R30 gains are 11.920908/12.025678 K at the saturated -30 hPa corner, using the fixed hull bills before added hardware.", ["checks/058-EDGES.json"]),
 "A2-03": ("it reproduces", "P3 R10/R30 gains are 6.555232/6.406881 K, retaining the saved sag-volume debit.", ["checks/058-EDGES.json"]),
 "A2-04": ("it reproduces", "Independent R10 cold roots are 276.958501 K (MLCCAg) and 265.835307 K (epsilon .05): a shift of 11.123194 K. Source transfer to Be remains NFI.", ["checks/058-THERMAL-MIXED-CONVECTION.json", "SOURCE-AUDIT.json"]),
 "A2-05": ("it reproduces", "R10 band is 4.029782 K baseline and 25.727676 K with the declared whole bill; substituting the independent thermal root changes the latter by only -0.000116 K.", ["checks/058-EDGES.json", "checks/058-THERMAL-MIXED-CONVECTION.json"]),
 "A2-06": ("it reproduces", "R30 band is 13.846685 K baseline and 34.626234 K with the whole bill. The independent thermal roots preserve the displayed 13.8/34.6 K.", ["checks/058-EDGES.json", "checks/058-THERMAL-MIXED-CONVECTION.json"]),
 "A2-07": ("it differs", "The original counts reproduce exactly at hull-only mass. With the same report's hardware, R10 MLCCAg 63.979% becomes 61.253%; R10 AlAOC 83.647% becomes 79.854%; R12 AlAOC 95.785% becomes 94.156%. Baseline 33.802% is unchanged. See F-A2-058-P2-HARDWARE.", ["FIXES.json", "checks/058-COVERAGE-height27.29-humidityTrue.json"]),
 "A2-08": ("it differs", "P3 original 77.747%/96.994% reproduce at hull-only mass. Even adding only the 5 kg valve yields upper bounds 76.482%/96.881% at R10/R12; a matched bladder still needs pricing. See F-A2-058-P3-HARDWARE.", ["FIXES.json", "checks/058-COVERAGE-height27.29-humidityTrue.json"]),
 "A2-09": ("it cannot be checked without a source or a test", "The declared minimum-radius/least-optimism selection needs complete hardware bills for its specific lowe/design-pressure and P3 witnesses, followed by a selection check. The sampled static-finish rows do not establish new minima. N-A2-058-RADIUS.", ["FIXES.json", "NFI.json"]),
 "A2-10": ("it reproduces", "All 87648 processed hours give 87354 complete T/Tdew/SLP hours and 3559 complete 24-hour UTC days; 93 calendar days are excluded. All eight sampled original hour/day counts match exactly. The 24 raw NOAA spot observations also match. Exclusions remain explicit.", ["checks/058-COVERAGE-height27.29-humidityTrue.json", "NFI.json"]),
 "A2-11": ("it reproduces", "All six favorable density factors reproduce within 1.09e-8: 1.122180/1.076600/1.059313 ISA, 1.166365/1.118320/1.100118 optimistic. These use concept growth and actual joining, not the TRL7 or retained-floor account.", ["checks/061-ARITHMETIC.json"]),
 "A2-12": ("it reproduces", "R30 handbook factors independently give 2.143497010 ISA and 2.248020659 optimistic, within 2.72e-8 of the saved roots.", ["checks/061-ARITHMETIC.json"]),
 "A2-13": ("it cannot be checked without a source or a test", "The all-density witness independently closes mass and matches the reported product, but this spot review does not independently compare the full constrained multistart search. The best-found ranking remains N-A2-061-PRODUCT-RANKING, with no global-optimum inference.", ["checks/061-ARITHMETIC.json", "NFI.json"]),
 "A2-14": ("it reproduces", "The irreducible fixed-family P3 bounds are all negative. R30 ISA is -3681.927506 kg; even giving the full stated tube-relief fraction free leaves -329.452553 kg. This is a certificate only for the specified family, named levers and inherited tube lower bound.", ["checks/061-ARITHMETIC.json"]),
 "A2-15": ("it reproduces", "NASA Table VI-1 distinguishes 5% TRL7 hardware from 6% battery. R12 ISA P2 growth is 383.648403 kg and payload +4.615730 kg under the declared account.", ["checks/061-ARITHMETIC.json", "SOURCE-AUDIT.json", "sources/NASA-table-VI-1.png"]),
 "A2-16": ("it reproduces", "R30 nominal Be faces are 102229.721909/104852.395618 kg: 23.774354%/24.384278% of USGS's 430000 kg estimated 2025 world mine Be content. This is not finished-sheet capacity.", ["checks/061-ARITHMETIC.json", "SOURCE-AUDIT.json"]),
 "A2-17": ("it reproduces", "At R20 optimistic, the frozen earlier geometry with corrected hardware rate gives +14.701407 kg TRL7; the declared 061 cure/geometry scenario gives -29.884305 kg. Both accounts re-sum correctly; physical validity of global cure demand remains NFI.", ["checks/061-ARITHMETIC.json", "NFI.json"]),
}
for row in rows:
    outcome, finding, evidence = answers[row["id"]]
    row.update({"outcome": outcome, "finding": finding, "evidence": evidence})

source_audit = {
    "unit": UNIT,
    "inspection_date_UTC": dt.datetime.now(dt.timezone.utc).date().isoformat(),
    "sources": [
        {
            "title": "NASA GSFC IDC mass growth guidance, Table VI-1",
            "url": "https://ntrs.nasa.gov/api/citations/20120013284/downloads/20120013284.pdf",
            "method": "Primary PDF and rendered page 10 visually inspected in this review.",
            "copies": ["sources/NASA2012.pdf", "sources/NASA-table-VI-1.png"],
            "finding": {"TRL7_hardware_fraction": .05, "TRL7_battery_fraction": .06},
            "scope": "Rates validate the column correction; application and additional system margin remain the declared project scenario."
        },
        {
            "title": "USGS Mineral Commodity Summaries 2026, Beryllium",
            "url": "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-beryllium.pdf",
            "method": "Official-source indexed table inspected with web search; direct PDF request was refused. No locally archived USGS PDF is claimed.",
            "corroborating_primary_url": "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf",
            "finding": {"world_mine_Be_content_2024_tonnes": 433, "estimated_world_mine_Be_content_2025_tonnes": 430},
            "scope": "World mine-production estimate, rounded, expressed as Be content; not sheet supply."
        },
        {
            "title": "Sheldahl Red Book Rev E, aluminized polyimide with acrylic overcoat",
            "url": "https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf",
            "method": "Pinned primary vendor PDF and extracted table inspected.",
            "copies": ["sources/RedBook.pdf", "sources/RedBook.txt"],
            "finding": {"specified_maximum_solar_absorptance": .14, "specified_maximum_hemispherical_emittance": .05},
            "scope": "Film product limits do not qualify an 8.33 g/m2 coating deposited on Be."
        }
    ],
    "061_original_process": {
        "copy": "sources/061-dispatched-PROCESS-v2.md",
        "sha256": "be858ac11e1e4adc8e164157752df002a8edce54b62f077eb6b95f89d3e7c11a",
        "finding": "Recovered originally dispatched bytes verified; later v2.1 in-place replacement is not an owner defect."
    },
}
write("SOURCE-AUDIT.json", source_audit)

outcomes = {label: sum(r["outcome"] == label for r in rows) for label in [
    "it reproduces", "it differs", "it cannot be checked without a source or a test"
]}
write("RESULTS.json", {
    "schema": 1, "unit": UNIT, "order": ORDER, "reviewer": SEAT,
    "reviewed_cards": ["058", "061"], "excluded_own_cards": ["056", "062"],
    "tag": "QUESTIONABLE / PROJECTION", "qualified_installed_hull_SF": None,
    "counts": outcomes, "claims": rows, "fix_register": "FIXES.json",
    "nfi_register": "NFI.json", "fixes_review_status": "unreviewed",
    "independence": {"owner_code_read_imported_or_executed": False, "new_FE_solve": False,
                     "scope": "Load-bearing numerical spot checks; no whole-table rederivation."},
    "authority_note": "061 evaluated against its recovered original PROCESS-v2 pin, not the later in-place v2.1 bytes.",
    "measured_start": read("INTAKE.json")["measured_start"],
    "measured_end": dt.datetime.now(dt.timezone.utc).isoformat(),
    "active_jobs": [],
})

review_lines = [
    "# REVIEW-A2 — MAINLINE058 and MAINLINE061",
    "",
    "The selected arithmetic reproduces except for two hardware-accounting omissions in 058's weather-coverage claims. No numerical correction was demonstrated in the selected 061 rows. Two ranking claims need further evidence. All results remain QUESTIONABLE / PROJECTION; no installed-hull safety factor is qualified.",
    "",
    "Seventeen load-bearing claims were listed before calculation in `LOAD-BEARING.json`. This review reads neither owner's implementation, runs no new FE solution and changes no owner artifact.",
    "",
    "| Claim | Card | Outcome | Finding |",
    "|---|---|---|---|",
]
for row in rows:
    review_lines.append(f"| {row['id']} | {row['card']} | {row['outcome']} | {row['finding']} |")
review_lines += [
    "",
    "The two proposed fixes remain **unreviewed** in `FIXES.json`. This review does not perform a fix-review or assign the next unit.",
    "",
    "The P2 hardware-only recount is particularly consequential: the sampled R12 AlAOC configuration falls below 95%, and R20 AlAOC falls below 99%. The separate least-optimism selections use other finishes/design pressures; no new minimum radius is inferred from these spot checks.",
    "",
    "The full methodology, conventions and review limits are in `METHOD.md`; numerical evidence is in `checks/`. The authoritative weather recount is `058-COVERAGE-height27.29-humidityTrue.json`, which reproduces all eight sampled original hour/day counts exactly before adding hardware.",
    "",
    "The [NASA source](https://ntrs.nasa.gov/api/citations/20120013284/downloads/20120013284.pdf) confirms the 5% hardware / 6% battery distinction. The [USGS source](https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-beryllium.pdf) supports the 430 t mine-Be denominator. The [Sheldahl source](https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf) supports the film optical limits, with the transfer caveat retained. Details and access limits are in `SOURCE-AUDIT.json`.",
    "",
    "061's originally dispatched PROCESS-v2 bytes were verified. The later file replacement does not count against that owner.",
]
(B/"REVIEW.md").write_text("\n".join(review_lines)+"\n")

card = """# REVIEW-A2 — 058 / 061

058 needs two coverage-accounting fixes. Its pressure loads, temperature
gains and displayed whole-bill bands reproduce. The saved site counts
also reproduce exactly, but use hull mass without the hardware required
by the named relief/ballast configurations.

| Configuration | Filed full-day coverage | With declared P2 hardware |
|---|---:|---:|
| P2 R10, MLCCAg relief/ballast | 63.979% | 61.253% |
| P2 R10, AlAOC relief/ballast | 83.647% | 79.854% |
| P2 R12, AlAOC relief/ballast | 95.785% | 94.156% |
| P2 R20, AlAOC relief/ballast | 99.269% | 98.960% |

For P3 standard-pressure climb, adding only its 5 kg valve changes R10
77.747% to at most 76.482%, and R12 96.994% to at most 96.881%.
The matched bladder still needs a mass specification.

No correction was demonstrated in 061's selected arithmetic. Its six
favorable density factors, two R30 handbook factors, fixed-family P3
negative mass bound, TRL7 column correction and Be-content comparison
reproduce. R12 ISA P2 has +4.616 kg under the declared TRL7 account.

Thirteen claims reproduce, two differ, and two cannot be checked without
further evidence: the complete-hardware minimum-radius selection and the
best-product ranking. Density-only is independently mass-closing at the
supplied witness; no global-optimality claim is made.

Proposed fixes remain **unreviewed**. Physical qualification, P3's cold
screen, chronological trim operation and installed finish properties
remain open. The original 061 PROCESS-v2 pin was verified; the later
replacement is not an owner fault. No owner code was read or run.

Full claim register: `REVIEW.md` / `RESULTS.json`. Fixes: `FIXES.json`.
Limits and evidence needed: `NFI.json`. All conclusions retain
QUESTIONABLE / PROJECTION status.
"""
(B/"CARD.md").write_text(card)

write("INPUTS.json", {
    "unit": UNIT, "brief_pins": "INPUT-PINS.json", "dependency_pins": "DEPENDENCY-PINS.json",
    "source_audit": "SOURCE-AUDIT.json", "claims_listed_before_derivation": "LOAD-BEARING.json",
    "own_implementations": ["independent_review.py", "independent_thermal.py"],
    "owner_code_policy": "No owner code read, imported or executed; paths in provenance metadata are not executions.",
    "authoritative_check_files": [
        "checks/058-EDGES.json", "checks/058-THERMAL-MIXED-CONVECTION.json",
        "checks/058-COVERAGE-height27.29-humidityTrue.json", "checks/061-ARITHMETIC.json"
    ],
    "diagnostic_files": "Other thermal/height weather outputs are retained diagnostics, not authoritative findings.",
})

jobs = [
    ("simjob-20261020t101053-ae8eed18b616.scope", "initial arithmetic and weather", "exit 0"),
    ("simjob-20261020t101245-f55585103117.scope", "station convention diagnostics", "exit 0"),
    ("simjob-20261020t101246-21f80f3293ae.scope", "forced-only thermal diagnostic", "exit 0"),
    ("simjob-20261020t101345-6c284a29d062.scope", "final station mapping recount", "exit 0"),
    ("simjob-20261020t101345-05e72a2697c7.scope", "mixed-convection thermal roots", "exit 0"),
]
write("EXECUTION.json", {
    "unit": UNIT, "jobs": [{"scope": name, "purpose": purpose, "result": result,
                           "cores": 1, "memory_GiB": 1, "reservation": "released"} for name, purpose, result in jobs],
    "host_timeout_seconds": 7200, "work_time_budget": None, "active_jobs": [],
    "note": "Scope IDs/results transcribed from returned simjob receipts; measured calculation intervals are also in checks/*EXECUTION.json and the thermal result."
})

checks = {}
for row in weather["selected_cases"]:
    assert row["owner_day_fraction"] == row["independent_at_owner_mass"]["full_day_fraction"]
    assert row["owner_hour_fraction"] == row["independent_at_owner_mass"]["hours_fraction"]
checks["eight_original_weather_cases_exactly_reproduce"] = True
assert weather["complete_hours"] == 87354 and weather["complete_24h_UTC_days"] == 3559
checks["weather_denominator"] = [87354, 3559]
assert all(r["max_absolute_difference"] == 0 for r in weather["raw_NOAA_spot_checks"])
checks["raw_NOAA_spot_observations_exact"] = len(weather["raw_NOAA_spot_checks"])
max_density_error = max(abs(r["difference"]) for r in arithmetic["density"])
assert max_density_error < 2.72e-8
checks["maximum_density_factor_difference"] = max_density_error
max_thermal_error = max(abs(r["difference_K"]) for r in thermal["rows"])
assert max_thermal_error < .00345
checks["maximum_cold_edge_difference_K"] = max_thermal_error
assert all(r["independent_payload_upper_bound_kg"] < 0 and r["generous_upper_bound_kg"] < 0 for r in arithmetic["P3_certificate"])
checks["all_six_P3_upper_bounds_negative_even_with_free_relief"] = True
assert len(rows) == 17 and sum(outcomes.values()) == 17
assert all(r["status"] == "unreviewed" for r in fixes)
checks["claim_and_fix_register_consistent"] = True
verified = []
for p in read("DEPENDENCY-PINS.json"):
    name = p.get("owned_copy", p.get("copy"))
    if not name:
        raise ValueError(f"Pin lacks copied path: {p}")
    local = Path(name)
    if not local.is_absolute():
        local = B/local
    actual = pin(local)
    assert actual["sha256"] == p["sha256"], str(local)
    if "bytes" in p:
        assert actual["bytes"] == p["bytes"], str(local)
    verified.append(str(local.relative_to(B)))
checks["dependency_copies_verified"] = len(verified)
assert hashlib.sha256((B/"sources/061-dispatched-PROCESS-v2.md").read_bytes()).hexdigest() == source_audit["061_original_process"]["sha256"]
checks["061_original_dispatched_process_bytes_verified"] = True
write("VERIFICATION.json", {
    "unit": UNIT, "measured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    "checks": checks, "failures": [], "scope": "Arithmetic and artifact checks, not physical qualification."
})
print(json.dumps({"claims": outcomes, "fixes": len(fixes), "dependency_copies_verified": len(verified)}, indent=2))
