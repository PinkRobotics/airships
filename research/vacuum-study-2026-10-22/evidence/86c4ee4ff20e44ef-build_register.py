#!/usr/bin/env python3
"""Additive 030c synthesis, extending 030b's schema and selector arithmetic."""
import copy
import math
from pathlib import Path
from datetime import datetime, timezone
from intake import B, load, save, pin

BASE = B / "baseline030b"
UNIT = "vacuum-mainline030c-design-register-1020"
REPORT = "rpt-1228-mainline030c-design-register-1020"
TAG = "QUESTIONABLE / PROJECTION"
intake = load(B / "INTAKE.json")
reports = {r["id"]: r for r in intake["reports"]}
ALIASES = {
    "029": "rpt-1228-mainline029-crimp-gamma-fe-1020",
    "037b": "rpt-ref-d6eac96dde8db1968e86",
    "039": "rpt-mainline039-opus-stiffened-sandwich-1020",
    "042": "rpt-mainline042-opus-build-route-1020",
    "041": "rpt-ref-c7dfc45babe1b96007db",
    "040": "rpt-ref-b10363665c6202d8ef75",
    "043": "rpt-ref-8cb22d2e233e57207cf6",
    "044": "rpt-ref-29830021a6e140ff7411",
    "CHECK037b": "rpt-ref-4bf25e71ae0c2ca315e2",
    "CHECK022d": "rpt-ref-4b8e7b08241bb7a45536",
    "CHECK026b": "rpt-ref-b92330879d6ba35bd62c",
    "CHECK033": "rpt-ref-d2ffe81a7858ecabf149",
    "CHECK034": "rpt-ref-025def9d3634f5e320d7",
    "CHECK037": "rpt-ref-bba592d71d65b13cc2e5",
    "CHECK038": "rpt-ref-2beb70a569266cf0297d",
    "CHECK039": "rpt-ref-20ab4b33b504a00ad3b6",
}


def source(alias, name):
    return load(B / "snapshots" / ALIASES[alias] / name)


def ref(alias, name, pointer):
    a = next(a for a in reports[ALIASES[alias]]["artifacts"]
             if Path(a["path"]).name == name)
    return {"report": ALIASES[alias], "file": a["snapshot"],
            "original_file": a["path"], "sha256": a["sha256"], "selector": pointer}


# Every original register field remains intact; current annotations are additive.
register = copy.deepcopy(load(BASE / "REGISTER.json"))
newtopics = [
    ("R095", "Native numerical evidence", "Unresolved FE benchmark, load-control endpoints and excluded spectra"),
    ("R096", "Stiffened sandwich", "Frame/bay adequacy, cap knockdown and coupled modes"),
    ("R097", "Build route and inspection", "Full-blank forming, in-place seams, closure tooling and inspection"),
    ("R098", "Cure residual state", "Stress-free temperature, cellular force balance and residual-stress stability"),
]
for rid, topic, gap in newtopics:
    register["rows"].append({"rid": rid, "topic": "T030C", "topic_name": topic,
                            "gap": gap, "sources": [], "updates_030b": [],
                            "states": ["QUESTIONABLE", "PROJECTION"]})
byrid = {r["rid"]: r for r in register["rows"]}
for r in register["rows"]:
    r["updates_030c"] = []
new = load(B / "NEW-NFI.json")
routing = load(B / "ROUTING.json")["assignments"]
assert set(routing) == {r["uid"] for r in new}
for n in new:
    byrid[routing[n["uid"]]]["updates_030c"].append(copy.deepcopy(n))

own_rows = [
    ("S001", "NFI-030C-GAMMA-GEOMETRY", "R007",
     "029 is adverse numerical evidence at 021/021b, not a solved 028b/037b hull.",
     "Weak-meridian endpoints at 11.8/46 mm are below operating pressure. The working shape target must be tighter than those 015 amplitudes within that model. Benchmark and collapse validation are absent; no quantitative physical tolerance or current joined-hull SF is established."),
    ("S002", "NFI-030C-042-MAP", "R070",
     "042's permissive dimple map must not override 029.",
     "Keep 042's 9.3–16.1 mm allowance and mapped gamma .69–.95 as conditional monocoque transfers. 029 supplies contradictory numerical evidence at related sandwich points. Neither historical S-II gamma about .2 nor a fabrication tolerance qualifies the new Be hull."),
    ("S003", "NFI-030C-THERMAL-DEPENDENCY", "R098",
     "037b uses 037 temperatures whose recovery remains open.",
     "The 200 F/30.3414:1 fix supplies the selected P2 construction model used by 040's common account. CHECK-037's 84 missing thermal/projection inputs remain open; a mechanical reinterpretation does not supply them. Balanced residual compression is not independently established as harmless to global stability."),
    ("S004", "NFI-030C-COMMON-ACCOUNT", "R083",
     "040's common scalar account retains model and installed-qualification gaps.",
     "040 recomputes the 037b construction with its own loads, coating, pad and service bill. R10 does not float; R30 ranks least optimism among tested radii. Coating+primer at an assumed .20 kg/m2 and retained water are the largest assumed debits. Keep this account distinct from old 028b/033/037/034 variants and the 044 life spectrum. The original +0.120151 kg is a fixed-geometry allowance; 040 recomputes joining. Neither mass closure nor scalar SF closes installed qualification."),
    ("S005", "NFI-030C-SEAM-PROCESS", "R025",
     "042 changes the in-place seam process without qualifying its mass and strength.",
     "Its 200 F panel bond and proposed room-temperature Be scarf are distinct cures. Do not transfer AF film weight or the 10 MPa scarf screen to the proposed seam paste as measured capability. F1 expands the existing T2 evidence route; it does not certify gamma."),
    ("S006", "NFI-030C-SNAPSHOT", "R094",
     "This register is a bounded filing snapshot.",
     "All discovered canonical mainline/check reports after the 030b snapshot are incorporated or explicitly dispositioned. Running work supplies no results. Later filings belong to 030d; no seat is polled, restored or contacted out of band."),
    ("S007", "NFI-030C-NONFINITE-SOURCE", "R079",
     "Some 037b infeasible alternatives contain nonstandard JSON Infinity/NaN.",
     "Original source bytes remain pinned verbatim. The current selected finite points are exported as strict JSON. Infeasible alternatives remain referenced with their explicit source disposition; nonfinite entries are not interpreted as capabilities."),
    ("S008", "NFI-030C-LIFE-AND-COMMON-BASIS", "R047",
     "040 common static/service account does not close 044 life or 043 reliability.",
     "040 adopts 037b but uses its own resized one-pad/wind/weather models. 044's six-pad spectrum and 60:1 scarf option belong to older R10 geometries, so its 36.661 kg cannot simply be added as a validated R30 retrofit. 043 uses 022d/026b stress/count cases, not 041's 750-member f5 frame. Carry each as an unresolved geometry-dependent requirement."),
]
authored = {"schema": 1, "unit": UNIT, "tag": TAG, "rows": [
    {"id": rowid, "title": title, "finding": finding, "status": "OPEN",
     "blocks_progress": False, "tag": TAG}
    for _, rowid, _, title, finding in own_rows]}
save(B / "AUTHORED-NFI.json", authored)
authpin = pin(B / "AUTHORED-NFI.json")
own = []
for i, ((uid, rowid, rid, _, _), fields) in enumerate(zip(own_rows, authored["rows"])):
    n = {"uid": uid, "report": REPORT, "card": "MAINLINE-030c",
         "file": str(B / "AUTHORED-NFI.json"), "snapshot": str(B / "AUTHORED-NFI.json"),
         "row_id": rowid, "fields": fields, "source_sha256": authpin["sha256"],
         "source_json_pointer": f"/rows/{i}", "register_classification": TAG}
    own.append(n)
    byrid[rid]["updates_030c"].append(copy.deepcopy(n))

notes = {
    "R007": "029 is filed: paper benchmark not reproduced; weak-meridian endpoints at 015's 11.8/46 mm defects are 78.627/90.722 kPa against 95.461 kPa. These do not support the target. Any workable shape target must be tighter within that model, but physical tolerance remains uncalibrated. Current 028b+037b needs gamma .564288; 029 did not solve that joined geometry.",
    "R010": "Selected 028b+037b 200 F/30.3414:1 point requires Q=.439513 (1.331859× .33); no matched Be/core/bond wrinkle-band evidence. Prior .434628 belongs to the no-residual 028b point.",
    "R018": "CHECK-038 and 042 retain the thin-stock restriction: .6096×1.8288 m at about .8 mm is not established by the maker's stock envelope. No panel enlargement is chosen, but factor one is not demonstrated supply.",
    "R025": "Selected scarf ratio is 30.341397:1 with 037b's 200 F panel cure, conditional 10 MPa screen and +.120151 kg joining allowance. As-designed 250 F/30:1 requires gamma .618429, beyond its named stretch, and free-edge minimum-strength factor .833325. 042 proposes a distinct room-temperature seam process that remains unqualified.",
    "R044": "CHECK-034: 30–50 kg is daily ground-serviced sealed planning, not continuous pumping. Edwards continuous 24 h installation is 292.333 kg; ten kg battery supports at most nine days at 5 W. Retain 100 kg systems and no payload credit; inventories are older geometries.",
    "R047": "037b changes the mechanical interpretation of cure mismatch; minimum free-edge factor is .833325 at 250 F and 1.075947 at 200 F. Sustained shear, cyclic life and the actual stress-free state remain unmeasured.",
    "R052": "CHECK-037 corrects ten tube-mass fields to SiC density 3100 kg/m3 and arc lengths. Exact card/check pairs are in P3-TUBE-MASS-CORRECTIONS.json and LEDGER. They apply to historical 022c rows, not the already separate 022d lead.",
    "R055": "041 directly models the selected 022d section: f4 gives .2-times-linear SF1.133451 but exceeds closure mass by174.444kg. Its resized f5 witnesses give1.143285/1.083205 at5%/019 reserves; local peak-compression sensitivities1.033223/.978132. These replace the transferred1.067 shortcut for these designs. Frozen026b rise8/nonlinear paths remain unverified.",
    "R059": "All eight 022c tube families are SiC; Ti/CFRP labels fittings. CHECK-037's ten corrections include two repeated projection rows with alternate film CTE. See the exact correction table.",
    "R069": "029 changes the evidence state of the tolerance map: named 015 amplitudes do not support operating pressure in the weak-meridian model. No new validated amplitude limit is inferred.",
    "R070": "042's map says 9.3–16.1 mm for the old 028b gamma; carry only as a PROJECTION, alongside 029's adverse numerical evidence and CHECK-035's unmatched S-II precedent. Shape control by itself does not establish knockdown.",
    "R082": "CHECK-039 supplies constructive points better than the filed grid: C2b/O6 fixed-mass SF .699691806 and +1127.071353 kg to SF 1.00000108. These are attained values, not certified global optima or a proof of impossibility.",
    "R086": "CHECK-037: pad masses depend on support and boss assumptions; preload/load direction can change sizing. Preserve proposed alternatives as sensitivities, not an installed load path.",
    "R088": "The matched wavelength remains essential: panel RMS, fit gap, dimple amplitude and wrinkle-band amplitude are distinct. 042's reflector precedents are other-material transfers; cure waviness remains open.",
    "R089": "CHECK-037 leaves 84 thermal/projection fields unrecovered. Its supplied polynomial maxima are 8.292853/14.851720 K; total flight pressure 479.847608 Pa gives conditional P2 minimum 1.001324769. 037b inherits the unresolved temperatures.",
    "R093": "CHECK-038 preserves first T1 finished-sheet compression/specification, T2 weighed curved sealed scarf, T3 same-batch wrinkle. 042 F1 expands T2 to a full-blank forming-and-seam article after T1; it can supply T3 coupons. Costs remain projections, no purchases.",
    "R094": "Current coverage and pending jobs are recorded at INTAKE.sampled_at. Old pending statements inside source history are superseded by this register's PENDING.json.",
    "R095": "029: 79 native runs; benchmark unresolved, StVK/foam/defect differences explicit, load-control endpoints not proven collapse. CAX8R, initial shift/load-scale spectra and multicore eigen spectra excluded; physical capacity is null.",
    "R096": "039 frame-bay optimism is renamed P2-O6 to avoid P2-O5 bond-film collision. CHECK-039 improves attained C2b points but none floats at fixed lift. Clamping threshold and equal-area cap mapping remain unvalidated; the no-solution claim is finite-search scope.",
    "R097": "042 builds a chain of smaller/other-material precedents. Full-blank Be forming, kilometre-scale room-temperature scarfs, assembly closure and Be-specific seam/bond inspection remain projections. Carry F1 through the existing grounding sequence.",
    "R098": "037b's continuous-core force balance/free-edge model replaces the rigid thermal screen only conditionally. Its foil transfer, cellular stiffness, actual stress-free temperature and effect of balanced residual stress on stability remain open; CHECK-037b is pending unless listed filed.",
}
notes.update({
    "R025": notes["R025"] + " CHECK-037b reproduces the selected numbers but does not qualify2U/Be/honeycomb low-cure transfer. 044's combined-load scarf screen falls to.9891 on its R10fix scenario.",
    "R040": "040 common bill: no R10 float in named ranges; ISA/optimistic/both-weather full gamma/Q endpoint deficits 109.649/257.973/596.529 kg (actual joining). First ISA floats occur at R12–15. R30 ranks least optimism among tested radii; ISA/optimistic usage .601233/.789568, conditional SF 1. Both-weather has no float. Coating+primer, assumed .20 kg/m2, and retained water are the largest assumed debits. Static/service closure is not qualified life.",
    "R047": "044: original six-pad core static screen .7143; plate-only damage-one index949.846days is not hull life. 037b thermal-only core projection18816days uses dense-core/mean-stress transfers. A+36.661kg pad/scarf scenario does not close Be/scarf life or mass. Qualified hull life remains null.",
    "R060": "043 supplies conditional weakest-link requirements, not frame probability: no matched compression m/scale/reference size for finished arcs. Its433-member022d bookkeeping is not041's750-member resized frame. Qualified Pf and lifetime remain null.",
    "R089": notes["R089"] + " 040 introduces its own resolved thermal balances and corrected128/256-zone projection; it does not retrospectively recover037's missing inputs.",
    "R098": "CHECK-037b reproduces principal residual/free-edge/scarf values;9 checker NFI remain. HexBond679 omitted30g/m2 support: corrected rejected-option mass519.653569kg, +75.398224kg. The selected200F/30.3414 fix remains conditional on product/cure/tooling and residual-state transfers.",
})
for rid, text in notes.items():
    byrid[rid]["current_030c"] = {"tag": TAG, "text": text}

# Selected P2 finite points. We inherit source optimizations, not rerun them.
r37b = source("037b", "RESULTS.json")
fixes = r37b["compute"]["fixes"]
nominal = fixes[0]
fixed = fixes[6]
scarf = r37b["compute"]["scarf_fix"][1]
p0 = source("029", "RESULTS.json")["operating_pressure_MPa"] * 1e6


def p2point(p, i, selected, ratio, edge_min):
    modes = {"global_buckling_at_needed_gamma": 1.0, "wrinkling_at_needed_Q": 1.0,
             **p["others"]}
    structural = min(modes.values())
    combined = min(structural, edge_min)
    gamma_factor = p["gamma_need"] / .20
    q_factor = p["Q_need"] / .33
    today = min(.20 / p["gamma_need"], .33 / p["Q_need"],
                min(p["others"].values()), edge_min)
    return {
        "id": "028b+037b-200F-scarf-fix" if selected else "028b+037b-250F-as-designed",
        "selected_lead": selected, "tag": TAG, "R_m": 10.0,
        "source": ref("037b", "RESULTS.json", f"/compute/fixes/{i}"),
        "basis": "028b p0, nu=.0752, 019 reserve and retained joining floor; 037b residual model",
        "gamma": p["gamma_need"], "Q": p["Q_need"],
        "gamma_factor": gamma_factor, "Q_factor": q_factor,
        "usage": p["max_usage"], "within_named_stretch": p["max_usage"] <= 1,
        "scarf_ratio": ratio, "tf_m": p["tf_mm"] / 1000,
        "tc_m": p["tc_mm"] / 1000, "residual_compression_MPa": p["sigma_res_MPa"],
        "face_pressure_plus_residual_MPa": p0 * 10 / (4 * (p["tf_mm"] / 1000)) / 1e6 + p["sigma_res_MPa"],
        "joining_allowance_delta_kg": p["mass_change_kg"],
        "modes_at_required_values": modes, "least_structural_screen_SF": structural,
        "free_edge_typical_SF": p["SF_free_edge"], "free_edge_minimum_average_SF": edge_min,
        "least_including_minimum_free_edge_SF": combined,
        "least_at_handbook_gamma_Q_same_geometry": today,
        "qualified_installed_hull_SF": None,
        "original_source_point": p,
        "formulas": {"gamma_factor": "gamma/.20", "Q_factor": "Q/.33",
                     "combined_screen": "min(source structural factors, source minimum-average free-edge factor)",
                     "same_geometry_handbook_screen": "min(.20/gamma_needed,.33/Q_needed,other source modes,free_edge_min)",
                     "face_demand": "p0*R/(4*tf)+sigma_res"},
        "mass_note": "Source delta is evaluated at its lead geometry; no new complete installed bill is inferred.",
    }


current = p2point(fixed, 6, True, scarf["r_need"], r37b["verdict"]["lightest_change_SF_free_edge"]["min"])
current["selection_scope"] = "Selected construction module only; 040 defines the current complete hull account."
asdesigned = p2point(nominal, 0, False, 30.0, r37b["verdict"]["bond_free_core_edge"]["SF_min"])

r29 = source("029", "RESULTS.json")
r41 = source("041", "RESULTS.json")
r40 = source("040", "RESULTS.json")
q40 = [x for x in source("040", "QUALIFICATION-AUDIT.json")
       if x["type"] == "necessary_at_selected_geometry"]
primary40 = [x for x in r40["rows"] if x["pad"] == "heavy70" and x["vented"]]
common40 = {"source": ref("040", "RESULTS.json", "/rows"),
            "necessary_source": ref("040", "QUALIFICATION-AUDIT.json", "type=necessary_at_selected_geometry"),
            "primary_rows": [], "necessary_points": copy.deepcopy(q40),
            "overall_installed_hull_SF": None,
            "basis": "037b construction; nu=.0768; wind envelope; .20 kg/m2 coating+primer; heavy70 pad; vented cells; daily sealed service nested within 100 kg systems; weather/floor as labeled",
            "largest_assumed_debits": ["coating+primer at assumed .20 kg/m2", "retained water"],
            "current_lead_point_ids": ["R30-ISA-actual-heavy70-vented", "R30-optimistic-actual-heavy70-vented"],
            "selection_scope": "Least named optimism among the five tested radii; conditional mass and scalar-screen witnesses, not qualified hulls."}
for x in primary40:
    p = x["two_factor_endpoint"]
    l = x["least"]["least"]
    common40["primary_rows"].append({
        "id": x["id"], "R_m": x["R_m"], "weather": x["weather"], "floor": x["floor"],
        "full_gamma_Q_endpoint_payload_kg": p["signed_payload_kg"],
        "endpoint_least_modeled_SF": min(p["modes"].values()),
        "endpoint_bill_kg": p["bill_kg"], "endpoint_lift_kg": p["lift_kg"],
        "least_status": x["least"]["status"], "minimum_axis_count": x["least"]["minimum_axis_count"],
        "least_axes": l["selected_axes"] if l else None,
        "least_usage": l["usage"] if l else None,
        "least_modeled_SF": min(l["modes"].values()) if l else None,
        "qualified_installed_hull_SF": None, "tag": TAG})
r39c = source("CHECK039", "CONSTRUCTIVE-POINTS.json")
constructive = copy.deepcopy(r39c)
for x in constructive:
    x["register_optimism_id"] = "P2-O6"
    x["source_optimism_id"] = "039/O5"
    x["bay_factor_over_020"] = x["design"]["today_full"]["gamma_p_O5"][0] / .20
    x["tag"] = TAG
    x["qualified_installed_hull_SF"] = None

audit37 = source("CHECK037", "AUDIT.json")
massrows = [x for x in audit37 if x.get("field") == "tube_mass_kg" and x.get("status") == "MISMATCH"]
assert len(massrows) == 10
p3check = source("CHECK037", "RESULTS.json")["p3"]
masscorrections = []
for a in massrows:
    idx = int(a["row"].split("/")[-1])
    masscorrections.append({**a, "case": p3check[idx]["row"],
                            "film_alpha": p3check[idx]["film_alpha"],
                            "source": ref("CHECK037", "AUDIT.json", f"row={a['row']},field=tube_mass_kg"),
                            "tag": TAG})
save(B / "P3-TUBE-MASS-CORRECTIONS.json", masscorrections)

pending_specs = [
    ("040 common account", "vacuum-mainline040", False),
    ("041 P3 discrete frame", "vacuum-mainline041", False),
    ("042 build route", "vacuum-mainline042-build-route", False),
    ("043 SiC reliability", "vacuum-mainline043", False),
    ("044 fatigue", "vacuum-mainline044", False),
    ("045 damage tolerance", "vacuum-mainline045", False),
    ("CHECK-029", "mainline029-check", True),
    ("CHECK-037b", "mainline037b-check", True),
    ("CHECK-039", "mainline039-check", True),
    ("CHECK-040", "mainline040-check", True),
    ("CHECK-041", "mainline041-check", True),
    ("CHECK-042", "mainline042-check", True),
]
pending = []
for label, needle, _ in pending_specs:
    found = [r["id"] for r in intake["reports"] if needle in r.get("unit", "")]
    pending.append({"item": label, "status": "FILED" if found else "PENDING",
                    "reports": found, "snapshot_at": intake["sampled_at"],
                    "next": "Folded here if filed; otherwise next register 030d."})
save(B / "PENDING.json", pending)

results = copy.deepcopy(load(BASE / "RESULTS.json"))
results["previous_030b_metadata"] = {
    k: copy.deepcopy(results[k]) for k in ("card", "unit", "snapshot_at", "coverage", "pending")}
results.update({"schema": 3, "card": "MAINLINE-030c", "unit": UNIT,
                "tag": TAG, "snapshot_at": intake["sampled_at"],
                "source_aliases": ALIASES,
                "measurement_start": load(B / "START.json"),
                "measurement_end": {"at": datetime.now(timezone.utc).isoformat(),
                                    "meaning": "synthesis build completed; measurement only"},
                "overall_installed_hull_SF": None, "certification": False,
                "P2_selected_lead": current, "P2_as_designed_250F": asdesigned,
                "P2_030b_points_status": "Preserved separate-basis variants; old nominal is superseded as selected lead by 037b fix. Larger hulls have no transferred cure closure.",
                "P3_selected_lead_041": copy.deepcopy(r41["best_closure_by_reserve"]["5"]),
                "P3_019_variant_041": copy.deepcopy(r41["best_closure_by_reserve"]["019"]),
                "P3_direct_discrete_041": r41,
                "P2_common_account_040": common40,
                "P2_selected_construction_scope": "028b+037b retained as selected construction. The current P2 hull lead is 040's common bill: no R10 float; first ISA floats at R12–15; R30 ISA/optimistic conditional points need least optimism among tested radii. Both-weather has no float. 044 fatigue remains separate.",
                "P2_current_hull_account": "P2_common_account_040",
                "reliability_043": {"source": ref("043", "RESULTS.json", "/"),
                    "qualified_frame_failure_probability": None, "qualified_lifetime_probability": None,
                    "scope": "022d433-member bookkeeping and026b cases; not a qualified probability for041f5"},
                "fatigue_044": {"source": ref("044", "RESULTS.json", "/"),
                    "qualified_hull_life_days": None,
                    "pad_plate_only_life_days": source("044", "RESULTS.json")["pad_plate_only_life_days"],
                    "scope": "Declared R10spectrum and separate source geometries; not a life qualification for040 resized hulls"},
                "P3_030b_points_status": "Preserved continuum and transferred-sensitivity history. 041 supplies directly modeled selected-section and resized closure witnesses; physical capacity remains unknown.",
                "P3_tube_mass_corrections_CHECK037": masscorrections,
                "gamma_FE_029": {k: copy.deepcopy(r29[k]) for k in
                    ("disposition", "operating_pressure_MPa", "benchmark", "lead_specified_defects",
                     "amplitude_sweep", "outer_face_stress_diagnostics", "physical_collapse_measurement",
                     "run_count", "normalizations")},
                "gamma_FE_current_lead_transfer": "No 028b/037b solve; no calibrated collapse gamma or physical shape tolerance.",
                "stiffened_039_checked_constructive_points": constructive,
                "stiffened_039_owner": ref("039", "RESULTS.json", "/"),
                "cure_037b": ref("037b", "RESULTS.json", "/"),
                "build_route_042": source("042", "RESULTS.json"),
                "new_check_evidence": {a: ref(a, "CARD.md", "whole card") for a in ALIASES if a.startswith("CHECK")},
                "pending": pending,
                "next": "none; stop and file; robotics seat sends next job"})
save(B / "RESULTS.json", results)

# Preserve all 711 old findings, including resolutions, and every original row.
nfi = copy.deepcopy(load(BASE / "NFI.json"))
nfi["schema"] = 3
nfi["unit"] = UNIT
nfi["tag"] = TAG
nfi["rows"] += new + own
nfi["note"] = "Attributed source records, including repeated and resolved findings, are preserved. Count is not a count of independent open physical gaps. Current 030c annotations govern over historical summaries."
nfi["auxiliary_source_documents"] = "NEW-NFI-SOURCES.json"
coverage = {
    "baseline_register_rows_preserved": 94,
    "baseline_findings_preserved": 711,
    "new_register_rows": len(newtopics),
    "new_source_findings": len(new),
    "new_authored_findings": len(own),
    "total_register_rows": len(register["rows"]),
    "total_attributed_findings": len(nfi["rows"]),
    "new_canonical_reports": len(intake["reports"]),
    "new_report_artifact_pins": sum(len(r["artifacts"]) for r in intake["reports"]),
    "original_030_rows": 86, "original_030_unique_findings": 362,
    "original_030_source_pointers": 363,
}
register["schema"] = 3
register["tag"] = TAG
register["previous_030b_coverage"] = copy.deepcopy(register["coverage"])
register["coverage"] = coverage
results["coverage"] = coverage
save(B / "REGISTER.json", register)
save(B / "NFI.json", nfi)
save(B / "REGISTER-COVERAGE.json", coverage)
save(B / "RESULTS.json", results)

# Preserve correction ledger entries; append scoped corrections with exact evidence.
ledger = copy.deepcopy(load(BASE / "LEDGER.json"))
corrections = [
    ("Selected P2 lead includes cure", ["037b"], "028b no-residual gamma .564164/Q .434628",
     "200 F + 30.341397:1 scarf, gamma .564287956/Q .439513308, usage .972190149; +.120150655 kg source allowance"),
    ("Keep as-designed 250 F case", ["037b"], "Nominal 028b called current without cure",
     "30:1 case gamma .618429128, usage 1.052281584; minimum-strength edge SF .833325314; not within named stretch"),
    ("Gamma evidence state", ["029"], "029 pending; 015 amplitudes used as tolerance map",
     "Benchmark not reproduced; 78.627395/90.722275 kPa endpoints below 95.460838 kPa. Not collapse limits or current-hull SF"),
    ("Gamma denominator", ["029"], "Handbook and crimp ratios conflated",
     "Both lead points Vc<2; required handbook .595318/.468229 versus W crimp .464110/.323009"),
    ("Optimism label collision", ["039"], "039 calls frame-bay cap transfer O5",
     "Rename to P2-O6 (source alias 039/O5); preserve P2-O5 as .015/.030 bond-film mass reduction"),
    ("Stiffened constructive improvement", ["CHECK039"], "Grid .689107645 / +1329.818726 kg claimed best",
     "Attained .699691806 at fixed mass; +1127.071353 kg at SF 1.000001080. Finite-search scope, not global proof"),
    ("Stiffened source gates and point distinctions", ["CHECK039"], "psi>=28 handbook gate; mass-added Q/scarf/tubes said to require change",
     "psi>=28 and gamma_s>=10 are unvalidated gates; at owner's mass-added point Q/scarf/local already pass. Cap factor .601013192, not .603"),
    ("Stiffened source ratios", ["CHECK039"], "Ti ratio .33 and STA8.1 predictions conflated",
     "317/917=.345692475 while printed 33% remains a source inconsistency; 759000 and 754000 lb are sequential model levels"),
    ("P3 checked continuum point", ["CHECK022d"], "Primary 022d not yet checked in 030b",
     "All primary witnesses reproduce; 50 sensitivity-field differences from coefficient precision, maximum SF change 3.98e-9"),
    ("P3 rise/nonlinear verification", ["CHECK026b"], "Rise8 and raw first-loss labels potentially read as checked",
     "Rise8 independent solve refused; first-loss null/verified_first_loss=false overrides raw labels. Linear/mass/baseline forces reproduce"),
    ("033 crossing precision", ["CHECK033"], "103.892275563 and 40.470112218 m",
     "Active roots 103.892078332461 and 40.470082164560 m; retain 241 exact path findings and basis distinctions"),
    ("Vacuum mission distinction", ["CHECK034"], "30–50 kg generalized to continuous installation",
     "Daily ground-serviced sealed estimate; Edwards continuous 24 h 292.333 kg, 2.307% speed shortfall for stated Kapton envelope"),
    ("Vacuum area and reconstruction", ["CHECK034"], "10% transmission sensitivity treated as complete area increase",
     "Charge gauge/mass/release consistently; +10% Zylon vacuum/barrier/bond subtotal 96.878937–116.878937 kg plus structural fiber"),
    ("Thermal inputs remain missing", ["CHECK037"], "Filed temperatures and projection coefficients treated as independently recovered",
     "84 fields unrecovered: 60 P3 temperatures, 10 P2 temperatures/swings, 14 coefficients. 037b does not supply missing inputs"),
    ("Thermal polynomial and total flight", ["CHECK037"], "Residual maxima 5.788444/17.145083 K; increment-only flight",
     "Filed-polynomial maxima 8.292853/14.851720 K. Include steady pressure: 479.847608 Pa, conditional minimum 1.001324769"),
    ("038 test plan and procurement", ["CHECK038"], "Historical end-mass precision and full-envelope thin sheet assumed",
     "Two coefficient-rounding differences retained; current targets and first-three ordering survive. Thin stock and prices unqualified; cited F1249-20 superseded by -25"),
    ("042 build-map applicability", ["042", "029"], "Plausible process precision interpreted as gamma support",
     "Conditional map only; retain adverse 029 evidence. No matched Be process, full-scale gamma or inspection qualification"),
    ("041 direct P3 replaces transferred shortcut", ["041"], "1.067 cross-geometry sensitivity used as current estimate",
     "Selected-section f4 directly gives1.133451 but +174.444kg closure deficit. Resized f5 gives1.143285/1.083205, local sensitivities1.033223/.978132 at5%/019 reserve."),
    ("041 nonlinear evidence scope", ["041"], "Earlier nearest-zero first-loss ambiguity",
     "New selected f4 smallest-algebraic sampled first loss5.430902 is source-audited; old026b paths remain unverified. Resized witnesses keep k=.2 times linear; no calibrated nonlinear knockdown."),
    ("040 common bill supersedes R10 float interpretation", ["040"], "028b+037b conditional structural point treated as installed R10float",
     "No R10float within named ranges; full gamma/Q endpoint ISA deficit109.649kg. R30ISA/optimistic minimum sets gamma+Q, usage.601233/.789568; both-weather no float."),
    ("040 film and favorable tuple definitions", ["040"], "Same film multiplier or compression-only improvement assumed across all points",
     "R30minimum uses.030film (O5factor1), endpoint payload uses.015(factor2). Face tuple couples E/Fcy; Fcy alone is nonbinding and does not recover marginal tuple-dependent floats."),
    ("CHECK037b HexBond support mass", ["CHECK037b"], "Rejected HexBond679 increment444.255345188kg",
     "Add30g/m2support at both interfaces:519.653568874kg, +75.398223686kg; rejection stands.16 L-precision path differences retained."),
    ("CHECK037b product/cure scope", ["CHECK037b"], "200F family/2K evidence treated as qualification of light2UBe/core",
     "Principal numbers reproduce; light2U substrate/core/cure,50psi tooling and residual-state transfer remain open."),
    ("043 reliability evidence", ["043"], "Typical3.9GPa divided by stress treated as survival probability",
     "No matched compression Weibull distribution/reference size; qualified framePf/lifetime null.Conditional433-member m10 requirements4.38651/8.75267GPa are hypotheses, not demonstrated factors."),
    ("044 life and combined loads", ["044"], "Small037bfix taken to establish ten-year service",
     "Original pad core static.7143; plate-only949.846day index not hull life. Fix combined-load scarf.9891.Conditional pad+60:1scarf addition36.661kg does not float or qualify Be/scarf life."),
]
for title, aliases, old, newtext in corrections:
    ledger["rows"].append({"correction": title, "by": [ALIASES[a] for a in aliases],
                           "old": old, "new": newtext, "effect_on_lead": newtext,
                           "lead_relevant": True, "register_version": "030c", "tag": TAG})
for row in masscorrections:
    ledger["rows"].append({"correction": f"CHECK-037 {row['row']}/tube_mass_kg ({row['case']})",
                           "by": [ALIASES["CHECK037"]], "old": row["card_value"],
                           "new": row["check_value"], "delta_kg": row["delta"],
                           "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
                           "source": row["source"], "register_version": "030c", "tag": TAG})
ledger["schema"] = 3
ledger["previous_rows"] = 118
save(B / "LEDGER.json", ledger)

optimism = copy.deepcopy(load(BASE / "OPTIMISM-LEDGER.json"))
for row in optimism["rows"]:
    if row["id"] == "P2-O1":
        row["current_evidence_030c"] = notes["R007"]
    if row["id"] == "P2-L":
        row["current_evidence_030c"] = notes["R089"]
    if row["id"] == "P2-V":
        row["current_evidence_030c"] = notes["R044"]
optimism["previous_030b_rows"] = 79
for p in (current, asdesigned):
    for oid, name, factor, ev, route in [
        ("P2-O1", "gamma", p["gamma_factor"], notes["R007"], "G1"),
        ("P2-O2", "wrinkling Q", p["Q_factor"], "Handbook inverse; actual Be/core/bond wrinkle-band qualification absent", "G5"),
        ("P2-O3", "face strength", 1.0, "345 MPa tensile proxy; formed-sheet compressive minimum unknown", "G4"),
        ("P2-O4", "panel enlargement", 1.0, "No enlargement; thin full-envelope supply not demonstrated", "G4"),
        ("P2-O5", "bond-film mass reduction", 2.0, ".015 instead of .030 lb/ft2; installed process mass and strength unknown", "G3"),
        ("P2-J", "scarf and residual-state model", None, f"{p['scarf_ratio']:.9f}:1, 10 MPa screen; 037b cellular model unqualified", "G3"),
        ("P2-W", "weather/clearance", None, "Mission choice and geometry-specific mass reclosure open", "G0"),
        ("P2-L", "coating, loads, cure, hardpoints", None, notes["R089"], "G6"),
        ("P2-V", "sealed service", None, notes["R044"], "G7"),
    ]:
        optimism["rows"].append({"lead": p["id"], "id": oid, "name": name,
                                 "factor": factor, "tag": TAG, "evidence_state": ev,
                                 "evidence_category": "unvalidated transfer",
                                 "grounding_route": route,
                                 "physical_tests_038": {"G1": ["T7"], "G5": ["T3"], "G4": ["T1"],
                                   "G3": ["T2"], "G0": [], "G6": ["T2", "T9"], "G7": ["T9"]}[route]})
for x in constructive:
    optimism["rows"].append({
        "lead": "039-C2b-checked-" + x["mode"], "id": "P2-O6",
        "source_alias": "MAINLINE-039 O5", "name": "frame-bay cap knockdown",
        "factor": x["bay_factor_over_020"],
        "cap_gamma": x["design"]["today_full"]["gamma_p_O5"][0],
        "tag": "PROJECTION", "evidence_category": "unvalidated transfer",
        "evidence_state": "Equal-area circular-cap and gamma_s>=10 assumptions; no demonstrated bay clamping. Separate from bond-film O5.",
        "grounding_route": "G10", "physical_tests_038": ["T7"],
        "source": ref("CHECK039", "CONSTRUCTIVE-POINTS.json", f"mode={x['mode']}")})
for reserve, p in r41["best_closure_by_reserve"].items():
    for oid, name, factor, ev, route in [
        ("P3-F", "complete Zylon membrane specific-strength comparison", 13.712953712953714,
         "Two-direction fiber transfer; full gas-tight laminate remains unqualified. No stiffness credit in primary resize.", "G8"),
        ("P3-C", "SiC crush/flexural numeric comparison", 3900 / 380,
         "3.9GPa typical crush versus380MPa flexural proxy is not an allowable conversion; full-size reliability unknown.", "G9"),
        ("P3-G", "global factor", .20,
         "Direct discrete linear eigenvalue now replaces transferred026b ratio; k=.2 is still uncalibrated.", "G2"),
        ("P3-local", "local axial/bending interaction", None,
         f"Axial convention inherited. Peak-compression sensitivity reduces least SF to{p['least_including_local_max_compression_sensitivity']:.9f}; no calibrated interaction law.", "G2"),
        ("P3-J", "multiaxial end joints and rigidity", None,
         f"Correlated end demands included; source joint mass{p['mass_kg']['joint']:.6f}kg. Scalar strength sizing does not establish rotational stiffness or installed mass.", "G2"),
        ("P3-T", "tensile ceiling Pa", 15586000.0,
         "Fixed probabilistic projection, not a qualified full-size tensile allowable.", "G9"),
        ("P3-M", "manufactured arc, sag and complete account", None,
         "Integer geometry is modeled; pressure fan, cap sag and complete assembly remain projections.", "G2"),
    ]:
        optimism["rows"].append({"lead": "P3-041-f5-" + reserve, "id": oid, "name": name,
            "factor": factor, "tag": TAG, "evidence_state": ev, "evidence_category": "unvalidated transfer",
            "grounding_route": route, "physical_tests_038": ["T4"] if route == "G8" else ["T5", "T6"] if route == "G9" else ["T6", "T8"]})
for x in q40:
    p = x["point"]
    for oid, name, factor, ev, route in [
        ("P2-O1", "gamma", p["properties"]["gamma"]/.20, notes["R007"], "G1"),
        ("P2-O2", "wrinkling Q", p["properties"]["Q"]/.33, "Necessary Q with slack removed at selected040geometry; unmatched physical wrinkle evidence.", "G5"),
        ("P2-O3", "compression proxy", p["properties"]["Fcy_Pa"]/345e6, "Coupled face tuple where selected; Fcy alone nonbinding. No qualified finished compression allowable.", "G4"),
        ("P2-E", "coupled face modulus", p["properties"]["E_Pa"]/290e9, "Moves with033face tuple; not a free compression-only axis.", "G4"),
        ("P2-O4", "panel enlargement", 1., "Stock-envelope geometry assumed; thin-gauge restriction retained where applicable.", "G4"),
        ("P2-O5", "bond-film mass reduction", .1464728290914915/p["properties"]["film_kg_m2_interface"], "Point-specific film mass; full endpoint and minimum-usage choices differ; bond process remains unqualified.", "G3"),
        ("P2-J", "scarf, coating, pad and service account", None, "040recomputes mass and scalar screens with037bmodel;044life and installed qualification remain open.", "G6")]:
        optimism["rows"].append({"lead":"040-"+x["id"],"id":oid,"name":name,"factor":factor,"tag":TAG,
            "evidence_state":ev,"evidence_category":"unvalidated transfer","grounding_route":route,
            "physical_tests_038":["T7"] if route=="G1" else ["T3"] if route=="G5" else ["T1"] if route=="G4" else ["T2","T9"]})
optimism["label_map"] = {"P2-O5": "bond film .015/.030 lb/ft2", "P2-O6": "039 frame-bay cap, formerly source O5"}
save(B / "OPTIMISM-LEDGER.json", optimism)

ground = copy.deepcopy(load(BASE / "GROUND-FIRST.json"))
ground["previous_030b_routes"] = copy.deepcopy(ground["routes"])
for route in ground["routes"]:
    if route["id"] == "G1":
        route["status"] = "029 FILED; benchmark unresolved; physical gamma still unvalidated"
        route["evidence"] += "; 029 adverse endpoint evidence, not collapse"
    if route["id"] == "G2":
        route["status"] = "041 FILED; direct integer frame modeled, physical qualification unresolved"
        route["evidence"] += "; 041 direct f4 and resized f5 witnesses"
        route["target"] = "Resolve local-shell bending interaction, joint rotational stiffness, imperfections and complete membrane/mass account on actual f5 geometry. Local sensitivity at019 reserve is below one."
    if route["id"] == "G3":
        route["evidence"] += "; 037b; CHECK-038; 042 F1 full-blank extension"
        route["target"] += " Include the 200 F panel bond and separately specified in-place seam cure."
    if route["id"] == "G6":
        route["evidence"] += "; CHECK-037's 84 missing inputs and 037b cure model"
        route["evidence"] += "; 040 common bill and044 declared life spectrum"
        route["target"] += " Resolve044pad static/cyclic failure and combined scarf loads on the actual selected common-account geometry."
    if route["id"] == "G7":
        route["evidence"] += "; CHECK-034 daily ground-service and installed pump distinctions"
    if route["id"] == "G9":
        route["evidence"] += "; 043 qualifiedPf remains null; direct041f5 geometry needs its own allocation"
ground["routes"].append({"id": "G10", "rank": None, "route": "Optional frame-bay cap adequacy test",
    "status": "PROJECTION, not a current floating lead", "evidence": "039 and CHECK-039",
    "target": "Measure frame/bay coupling and clamping under the actual load path before O6 credit.",
    "physical_tests_038": ["T7"], "original_030_priority": None})
ground["first_three_030c"] = ["T1", "T2", "T3"]
ground["042_F1_note"] = "After T1, expand T2 to full-size forming-and-seam article; can supply T3 coupons. No additional independent cost or qualification is inferred."
ground["check_038"] = ref("CHECK038", "CARD.md", "whole card")
save(B / "GROUND-FIRST.json", ground)

checks = copy.deepcopy(load(BASE / "CHECK-VERDICTS.json"))
for alias in ALIASES:
    if not alias.startswith("CHECK"):
        continue
    r = reports[ALIASES[alias]]
    checks.append({"check_id": r["id"], "at": r["at"],
                   "register_version": "030c", "verdict": r["body"],
                   "source": ref(alias, "CARD.md", "whole card"),
                   "qualified_installed_hull_SF": None, "tag": TAG})
save(B / "CHECK-VERDICTS.json", checks)
index = copy.deepcopy(load(BASE / "SOURCE-INDEX.json"))
index["additions_030c"] = intake["reports"]
index["baseline_030b_report"] = pin(BASE / "report.json")
index["snapshot_at_030c"] = intake["sampled_at"]
index["pending_dispatches_030c"] = load(B / "PENDING-DISPATCHES.json")
index["supplemental_orders_030c"] = load(B / "SUPPLEMENTAL-ORDERS.json")
save(B / "SOURCE-INDEX.json", index)
save(B / "INPUTS.json", {"schema": 1, "unit": UNIT, "tag": TAG,
    "brief_pins": load(B / "BRIEF-PINS.json"),
    "baseline_pins_file": pin(B / "BASELINE-PINS.json"),
    "source_index": pin(B / "SOURCE-INDEX.json"), "intake": pin(B / "INTAKE.json"),
    "pending_dispatches": pin(B / "PENDING-DISPATCHES.json"),
    "supplemental_orders": pin(B / "SUPPLEMENTAL-ORDERS.json"),
    "code_ancestry": "030b intake.py/normalize.py/build_register.py/write_docs.py are preserved under baseline030b; this additive implementation extends their snapshot, identity, routing and ledger schemas.",
    "source_scope": "Filed local evidence; no new literature or supplier evidence claimed.",
    "arithmetic_scope": "Ratio conversion, selected mode minima, source projection comparison and exact field correction; no solver, optimization or physical test rerun.",
    "overall_installed_hull_SF": None})
print("BUILT", coverage)
