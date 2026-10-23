"""Fold completed CHECK-048 evidence without changing any filed MAINLINE-053 byte."""
from pathlib import Path
from datetime import datetime
from collections import Counter
import csv
import hashlib
import json
import math

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def read(path):
    return json.loads(path.read_text())


def save(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, allow_nan=False)+"\n")


def pin(path):
    raw = path.read_bytes()
    return dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw))


def table(headers, rows):
    return "\n".join(["| "+" | ".join(headers)+" |", "| "+" | ".join("---" for _ in headers)+" |"]+
                     ["| "+" | ".join(str(v) for v in row)+" |" for row in rows])


checks = []


def check(label, passed, **detail):
    checks.append(dict(check=label, passed=bool(passed), **detail))


original_report = read(WORKSPACE/".ship/outbox/rpt-ref-3fb9907ba4e1c52825f0.json")
original_manifest = read(PRIOR/"MANIFEST.json")
old_checks = []
for scope, records in [("report", original_report["artifacts"]), ("manifest", original_manifest["files"])]:
    for record in records:
        actual = pin(Path(record["path"]))
        good = all(actual[k] == record[k] for k in ["sha256", "bytes"])
        old_checks.append(dict(scope=scope, path=record["path"], matches=good))
        check("prior filing remains immutable", good, scope=scope, path=record["path"])
save("PRIOR-FILING-VERIFIED.json", old_checks)

selected = ["CARD.md", "SPECIFICATION.md", "METHOD.md", "RESULTS.json", "NFI.json", "EVIDENCE.json",
            "MANIFEST.json", "BOUNDARY-CHOICES.json", "REFERENCE-THERMAL-ROWS.json",
            "RESIZED-CONSEQUENCES.json", "SETTLED-FINISH-SCREEN.json", "ACCOUNT-owner_table.json"]
pins = read(ROOT/"INPUT-PINS.json")
seen = {item["path"] for item in pins}
for name in selected:
    source = PRIOR/name
    destination = ROOT/"inputs/prior053"/name
    destination.parent.mkdir(parents=True, exist_ok=True)
    raw = source.read_bytes()
    if destination.exists():
        assert destination.read_bytes() == raw
    else:
        destination.write_bytes(raw)
    if str(source) not in seen:
        pins.append(dict(**pin(source), snapshot=str(destination.relative_to(ROOT))))
save("INPUT-PINS.json", pins)
for record in pins:
    frozen = pin(ROOT/record["snapshot"])
    current = pin(Path(record["path"]))
    check("input snapshot hash and size", all(frozen[k] == record[k] for k in ["sha256", "bytes"]),
          path=record["snapshot"])
    check("input original hash and size", all(current[k] == record[k] for k in ["sha256", "bytes"]),
          path=record["path"])

upstream = read(ROOT/"inputs/check048/SUMMARY.json")
thermal = read(ROOT/"inputs/check048/THERMAL-RESOLVED-RESULTS.json")
extra = read(ROOT/"inputs/check048/EXTRA-AUDITS.json")
register = read(ROOT/"inputs/check048/NFI.json")
prior = read(PRIOR/"RESULTS.json")
check("completed check", upstream["checker_complete"])
check("full account passes tighter comparison", upstream["account"]["tighter_mismatches"] == 0
      and upstream["account"]["tighter_comparisons"] == 1714368)
check("current thermal mismatches absent",
      all(r["field"].startswith("legacy.") for r in thermal["mismatches"]))
legacy_fixes = [r for r in extra["comparisons"] if r["field"].startswith("legacy.")]
check("all 26 legacy projection entries reconciled",
      len(legacy_fixes) == 26 and all(r["agrees"] for r in legacy_fixes))
check("remaining extra mismatches only null sensitivity fields",
      len(extra["mismatches"]) == 24
      and all(r["field"] in ["least_mask", "least_usage"] and r["owner"] is None
              for r in extra["mismatches"]))

# Compare equivalent already completed outputs; no optimizer or thermal solve reruns.
old = read(PRIOR/"ACCOUNT-owner_table.json")
indexed = {(r["R_m"], r["weather"], r["cure_in_global"], r["drying"]): r
           for r in old if r["floor"]}
route = dict(dry_gas="dry_gas", bake70="bake", desiccant="sorbent")
crosscheck = []
for r in upstream["primary"]:
    if r["weather"] not in ["ISA", "optimistic"]:
        continue
    key = (r["R_m"], r["weather"], r["cure_in_global"], route[r["drying"]])
    ours = indexed[key]["result"]
    point, least = ours["endpoints"][11], ours["chosen"]
    difference = point["payload_kg"]-r["payload_kg"]
    least_same = (least["mask"] if least else None) == r["least_mask"]
    usage_difference = least["usage"]-r["least_usage"] if least and r["least_usage"] is not None else None
    passed = abs(difference) < .002 and least_same and (usage_difference is None or abs(usage_difference) < 2e-6)
    crosscheck.append(dict(case=list(key), completed_checker_payload_kg=r["payload_kg"],
                           mainline053_owner_boundary_payload_kg=point["payload_kg"],
                           difference_kg=difference, least_mask_agrees=least_same,
                           least_usage_difference=usage_difference, passed=passed))
    check("equivalent completed primary accounts agree", passed, case=list(key), difference_kg=difference)
save("COMPLETED-CHECK-CROSSCHECK.json", crosscheck)

# Dimensionless diagnostics use standard gravity, ideal-gas beta and the inherited
# constant air properties. Extremal temperatures do not turn this into a mixed-flow solve.
diagnostics = []
rho, velocity, dynamic_mu, pr, ambient, gravity = 1.1672683307461802, 2., 1.79e-5, .71, 284.9, 9.80665
nu = dynamic_mu/rho
for row in read(PRIOR/"REFERENCE-THERMAL-ROWS.json"):
    if row["profile"] != "MLCCAg":
        continue
    diameter = 2*row["radius_m"]
    v = row["values"]
    delta = max(abs(v["max_outer_K"][0]-ambient), abs(v["min_outer_K"][0]-ambient))
    reynolds = velocity*diameter/nu
    grashof = gravity/ambient*delta*diameter**3/nu**2
    richardson = grashof/reynolds**2
    direct_ri = gravity/ambient*delta*diameter/velocity**2
    check("dimensionless ratio identity", math.isclose(richardson, direct_ri, rel_tol=1e-12),
          model=row["model"], R_m=row["radius_m"])
    diagnostics.append(dict(model=row["model"], R_m=row["radius_m"], representative_delta_K=delta,
                            Re=reynolds, Gr=grashof, Ra=grashof*pr, Ri=richardson,
                            input_classification="QUESTIONABLE / PROJECTION",
                            meaning="Extremum-based regime diagnostic; not a mixed-convection solution or validated criterion."))
save("REGIME-DIAGNOSTICS.json", dict(
    inputs=dict(rho_kg_m3=rho, speed_m_s=velocity, dynamic_viscosity_Pa_s=dynamic_mu,
                Pr=pr, Ta_K=ambient, standard_gravity_m_s2=gravity, beta_K_inverse=1/ambient),
    formulae=dict(Re="vD/nu", Gr="g beta abs(deltaT) D^3/nu^2",
                  Ra="Gr Pr", Ri="Gr/Re^2 = g beta abs(deltaT) D/v^2"),
    rows=diagnostics))

whitaker_url = "https://www.researchgate.net/profile/Stephen-Whitaker-3/publication/229709417_Forced_convection_heat_transfer_correlations_for_flow_in_pipes_past_flat_plates_single_cylinders_single_spheres_and_for_flow_in_packed_beds_and_tube_bundles/links/59d73bda0f7e9b42a6b0694a/Forced-convection-heat-transfer-correlations-for-flow-in-pipes-past-flat-plates-single-cylinders-single-spheres-and-for-flow-in-packed-beds-and-tube-bundles.pdf"
evidence = [
    dict(id="standard_gravity", source="NIST CODATA reference entry: standard acceleration of gravity",
         url="https://physics.nist.gov/cgi-bin/cuu/Value?gn%7Csearch_for=acceleration+of+gravity",
         evidence="Conventional standard gravity is exactly 9.80665 m/s2.",
         inference="Used as a diagnostic reference, not a site-specific gravity measurement.",
         access="Official NIST entry checked through browser search."),
    dict(id="forced_correlation", source="Whitaker (1972), Table 1 and Eq.33", url=whitaker_url,
         evidence="Published sphere Re interval 3.5–76000; average forced-convection relationship.",
         inference="Both owner and CHECK-040 apply it well outside that range, as a local coefficient on a non-isothermal hull.",
         access="Primary author PDF accessed through browser; existing MAINLINE-053 browser record retained."),
    dict(id="forced_transition", source="Will, Kruyt and Venner (2017), DOI 10.1016/j.ijheatmasstransfer.2017.02.018",
         url="https://research.utwente.nl/files/20163165/experimental.pdf",
         evidence="Smooth isothermal-sphere experiments span Re 7800–330000 and observe heat-transfer transition near 290000.",
         inference="This documents regime dependence; the study does not furnish a validated replacement at Re 2.6–7.8 million for the present surface.",
         access="Primary publisher and author-repository text exposed by browser search; raw PDF fetch returned 403."),
    dict(id="large_sphere_natural", source="Rodriguez Maestre et al. (2021), DOI 10.1016/j.ijthermalsci.2021.107061",
         url="https://www.sciencedirect.com/science/article/pii/S1290072921002258",
         evidence="The study reports 48 CFD cases at D 1–40 m and Ra about 4e8–2e14, with substantial disagreement among natural-convection correlations.",
         inference="Large-sphere natural convection needs regime-specific validation; still-air/isothermal averages do not establish the owner's max rule at 2 m/s with nonuniform radiative forcing.",
         access="Primary publisher abstract/highlights and indexed text consulted; full article was not retrieved."),
    dict(id="honeycomb_paths", source="NASA 19680009019, section 3.1, printed pp.65–66",
         url="https://ntrs.nasa.gov/api/citations/19680009019/downloads/19680009019.pdf",
         local=str(PRIOR/"sources/nasa_honeycomb1968.pdf"),
         evidence="Metal conduction, cell radiation and adhesive-interface resistance require separate treatment.",
         inference="Core-gap radiation is distinct from hull-cavity radiation, but neither effective gap coefficient .20 nor zero contact resistance is established for the intended bonded sandwich.",
         access="Previously pinned primary PDF/text inspected; browser refetch size limit recorded."),
    dict(id="SolarWhite", source="ENBIO manufacturer SolarWhite sheet",
         url="https://enbio.eu/wp-content/uploads/2024/07/SolarWhite.pdf",
         evidence="Typical 150 micrometre coating: 285 g/m2, alpha .18 and hemispherical epsilon .89 on Al2024-T3.",
         inference="Corrects missing-source claims; no installed-Be mass/optics qualification or selected multilayer input change follows.",
         access="Completed-check PDF pinned and manufacturer page independently opened."),
    dict(id="classical_CCAg", source="NASA 2015, printed slide19",
         url="https://ntrs.nasa.gov/api/citations/20150018109/downloads/20150018109.pdf",
         evidence="Alpha .08, normal epsilon .72, CCAg/ITO on 3 mil Kapton.",
         inference="Does not substantiate a hemispherical .09/.65 model pair. This differs from the selected multilayer class.",
         access="Primary PDF retrieved; browser text independently checked.")
]
save("PHYSICAL-EVIDENCE.json", evidence)
physical = dict(
    best_supported_installed_boundary=None,
    owner_numerically_correct_for_declared_equations=True,
    owner_physically_selected=False,
    check040_physically_selected=False,
    model_form_judgment="Retain buoyancy and radiative transfer as relevant mechanisms, but require appropriate local flow and measured bonded-panel transport before choosing coefficients.",
    common_limitations=["Forced-correlation Reynolds extrapolation and local use of an average coefficient",
                        "Zero adhesive/contact thermal resistance",
                        "Fixed dry optics and unvalidated joint sky/ground/wind/wetting mission",
                        "No measured full-hull thermal field"],
    owner_specific=["Natural floor coefficient/max-combination lacks full-scale validation",
                    "Effective gap coefficient .20 is not a measured cell transport property"],
    check040_specific=["Forced-only flow has no demonstrated negligibility of buoyancy",
                       "Zero gap augmentation has no demonstrated radiation negligibility"],
    selected_consequence="Carry existing four alternatives. No uniquely justified new table or payload credit.",
    physical_bounds=False, installed_hull_SF=None)
save("PHYSICAL-JUDGMENT.json", physical)

corrections = [
    dict(topic="Thermal comparison coverage", corrected=dict(thermal_comparisons=thermal["comparisons"],
         reconciled_legacy_entries=len(legacy_fixes), full_account_comparisons=upstream["account"]["comparisons"],
         full_account_tighter_tolerance=2e-8),
         disposition="Numerical closure accepted; the 1714368 figure describes full-account comparisons."),
    dict(topic="SolarWhite source coverage", nominal_areal_mass_kg_m2=.285,
         nominal_thickness_m=.000150, substrate="Al2024-T3", alpha=.18,
         hemispherical_emittance=.89, qualified_Be_mass_kg_m2=None,
         disposition="Source fact adopted locally; inherited source-absence/label-ambiguity claims are superseded by this fold."),
    dict(topic="Classical CCAg source", NASA2015=dict(alpha=.08, normal_emittance=.72, substrate="3 mil Kapton"),
         modeled_classical_pair=dict(alpha=.09, emittance=.65),
         disposition="Model pair remains hypothetical; correct attribution is the patent range with unresolved emittance statistic. Selected multilayer .09/.80 is unchanged."),
    dict(topic="Null optical-sensitivity least fields", affected_cases=12, affected_fields=24,
         disposition="Adopt completed check's supplied floating witnesses; null does not mean infeasible. Do not treat these witnesses as repaired finish screens or installed wet/aged optics."),
    dict(topic="Cure treatment versus thermal boundary", checker_lost_float_cases=upstream["lost_float_configurations"],
         checker_changed_axis_counts=upstream["changed_axis_counts"],
         disposition="These are cure-compression model changes, distinct from MAINLINE-053 comparisons at fixed cure treatment; no contradiction with its zero thermal-only float/set flips.")
]
save("CORRECTIONS.json", corrections)
save("NFI.json", dict(
    status="Physical qualifications OPEN; arithmetic status updated",
    new_NFI_count=0, installed_hull_SF=None,
    original053_register="inputs/prior053/NFI.json",
    original053_open_groups_retained=9,
    completed048_register="inputs/check048/NFI.json",
    completed048_status_counts=dict(Counter(r["status"] for r in register["rows"])),
    dispositions=[
        "C01/C02/C03 numerical work, C12 check coverage and C13 execution are resolved as filed by CHECK-048.",
        "C04/C14 source corrections and C17 null-field interpretation are adopted in this fold; original files remain immutable.",
        "All material, substrate, thermal, moisture, cure and structural qualifications carry.",
        "The new convection literature extends evidence for existing NFI-053-CONVECTION; it does not qualify a coefficient set."]))

cases = [(r, w, True, True, "bake") for r in [10, 12, 15] for w in ["ISA", "optimistic"]]
differences = read(PRIOR/"RESIZED-CONSEQUENCES.json")
lookup = {(r["model"], tuple(r["case"])): r for r in differences}
models = ["forced_conduction", "mixed_conduction", "forced_gap", "mixed_gap"]
payload_rows = []
for k in cases:
    old_payload = lookup[(models[0], k)]["old_payload_kg"]
    row = dict(R_m=k[0], weather=k[1], cure_in_global=True, joining="retained_floor", drying="bake",
               original_owner_payload_kg=old_payload)
    for model in models:
        r = lookup[(model, k)]
        row[model+"_payload_kg"] = r["new_payload_kg"]
        row[model+"_change_kg"] = r["payload_difference_kg"]
    payload_rows.append(row)
save("CONSEQUENCES.json", dict(source="inputs/prior053/RESIZED-CONSEQUENCES.json",
                              new_solver_runs=0, reason="Existing complete independent four-boundary matrix already covers the requested readings.",
                              endpoint_float_changes=prior["endpoint_float_changes"],
                              least_axis_choice_changes=prior["least_chosen_mask_changes"],
                              maximum_payload_cost_kg=prior["maximum_payload_cost_kg"],
                              frozen_crossings=prior["frozen_new_screen_crossings"],
                              primary_rows=payload_rows, all_alternatives=prior["model_summary"]))
payload_table = table(
    ["R / weather", "Owner filed kg", "Forced/conduction kg", "Mixed/conduction kg", "Forced/gap kg", "Mixed/gap kg"],
    [[f'R{r["R_m"]} / {r["weather"]}', f'{r["original_owner_payload_kg"]:.6f}']+
     [f'{r[m+"_payload_kg"]:.6f}' for m in models] for r in payload_rows])
regime_table = table(
    ["R m", "Re", "Extremal abs(ΔT) K", "Ra", "Ri"],
    [[r["R_m"], f'{r["Re"]:.5g}', f'{r["representative_delta_K"]:.6f}',
      f'{r["Ra"]:.5g}', f'{r["Ri"]:.6f}']
     for r in diagnostics if r["model"] == "forced_conduction"])
scope = dict(
    unit="vacuum-mainline053-thermal-table-settled-1020", order=ORDER,
    prior_report=original_report["id"], completed_checker_report="rpt-ref-5c8405d45d6cb50633f1",
    step2="Confirmed: the completed independent CHECK-048 reproduces the owner's tables once the previously unwritten convection and conductance terms are supplied.",
    step3=physical, step4="Existing conditional four-model consequences retained without claiming a uniquely better-supported coefficient set.",
    numerical_change_from_prior053=False, source_and_status_addendum=True,
    prior_artifacts_modified=False, numerical_reruns=0,
    crosschecks=len(crosscheck), maximum_crosscheck_payload_difference_kg=max(abs(r["difference_kg"]) for r in crosscheck),
    coverage=dict(thermal=thermal["comparisons"], legacy_reconciled=len(legacy_fixes),
                  account=upstream["account"]["comparisons"]),
    no_time_budget=True)
save("RESULTS.json", scope)

card = f"""# MAINLINE-053 — completed CHECK-048 fold

**Confirmed: the completed independent CHECK-048 reproduces the owner's tables once the previously unwritten convection and conductance terms are supplied.**

**The owner's boundary is not established as the physically best-supported one.**
CHECK-040's forced/conduction reading is also not established as the installed
boundary. The better-supported model form must address local mixed convection,
cell radiation and bonded-interface resistance. The available evidence does
not select the required coefficient set for this hull. All inherited properties
remain QUESTIONABLE; installed performance remains PROJECTION.

| Term | Owner reading | CHECK-040 reading | Physical judgment |
| --- | --- | --- | --- |
| External convection | Max of forced h and 1.32 max(abs(To−Ta),.05)^.25 | Forced h only | Buoyancy can matter, but neither this max rule nor its omission is qualified |
| Core transport | Solid-core conduction plus 4(.20)σ average(Ti)³ | Solid-core conduction alone | Gap radiation is a separate physical path from enclosure radiation; neither .20 nor its omission is measured here |
| Bond/contact resistance | Zero | Zero | Both lack the bonded-panel resistance needed to select installed conductance |
| Inner enclosure | Uniform .20 diffuse empty sphere | Same | The enclosure identity is valid under those assumptions; actual finish and obstruction remain open |
| Weather and optics | Fixed dry optical pair and prescribed sky/ground/wind | Same | Neither is a measured coupled weather/wetting mission |

Both forced branches extrapolate Whitaker's sphere range Re 3.5–76,000.
The hull uses Re 2.61–7.83 million, and treats an average coefficient as local
on a non-isothermal surface. This is a shared limitation, not evidence that
CHECK-040 supplies a uniquely correct replacement.
[Whitaker, Table 1 and Eq.33]({whitaker_url}).

Later isothermal-sphere experiments found a heat-transfer transition near
Re 290,000, within measurements up to 330,000. They support taking flow
regime seriously; they do not validate either inherited branch at the hull
Reynolds numbers. [Will et al., 2017](https://research.utwente.nl/files/20163165/experimental.pdf).
A large-sphere natural-convection study simulated diameters 1–40 m and
Ra approximately 4e8–2e14, finding substantial variation among correlations.
Its still-air averages do not validate a local max rule for the current
nonuniform, 2 m/s case.
[Rodríguez Maestre et al., 2021](https://www.sciencedirect.com/science/article/pii/S1290072921002258).

As an explicitly approximate regime diagnostic, take beta=1/(284.9 K),
nu=1.79e−5/1.1672683307461802 m²/s and standard gravity 9.80665 m/s².
[NIST conventional value](https://physics.nist.gov/cgi-bin/cuu/Value?gn%7Csearch_for=acceleration+of+gravity).
Then Re=vD/nu, Ra=g beta |ΔT| D³ Pr/nu² and
Ri=Gr/Re²=g beta |ΔT| D/v². Using the already solved multilayer
forced/conduction extrema gives:

{regime_table}

These Ri values make an assertion of negligible buoyancy unsupported.
They do not validate the owner's coefficient or combine opposed, cross and
aiding convection into one law. The surface is nonuniform, so the diagnostic
is not a new mixed-flow solution.

NASA's honeycomb analysis distinguishes solid conduction and cell radiation,
and states that adhesive-interface resistance must be considered for bonded
aluminum panels. This supports treating both transport and interface terms,
but supplies no measured parameter for the selected CR-III/AF163/Be assembly.
[NASA, section 3.1, pp.65–66](https://ntrs.nasa.gov/api/citations/19680009019/downloads/19680009019.pdf).
The gap and enclosure terms describe different paths. Accepting that
distinction does not establish the effective gap emissivity .20.

**The consequence remains the already computed four-way comparison.**
No new coefficient set is sufficiently supported to replace it, and no
payload improvement follows from merely declaring the owner numerically
reproduced. Below are the existing cure-inclusive, retained-floor/bake
multilayer endpoints at the 028b gamma/Q/film assumptions, 200°F cure and
30.341397319:1 scarf. Every mass debit is retained.

{payload_table}

The forced/conduction alternative costs {min(-r['forced_conduction_change_kg'] for r in payload_rows):.6f}–{max(-r['forced_conduction_change_kg'] for r in payload_rows):.6f} kg in these six
cases. Across the complete previously filed matrix, thermal-boundary changes
cause no endpoint float-sign or minimum/tied optimism-set change. All four
selected-finish day/cycle screens pass. Frozen scarf checks newly cross one
in 288 comparisons and global checks in 85; resizing restores the stated
limits. Free-edge and cell-wall screens remain passing. These alternatives
are not certified physical bounds; installed hull SF remains unknown.
The original [full card](../vacuum-mainline053-thermal-table-settled-1020/CARD.md)
retains the R10–30 temperature family, both cure branches, all joining/drying
routes and complete witnesses.

**The completed check's qualifications and corrections are incorporated.**
Its thermal ledger contains {thermal["comparisons"]:,} comparisons; 26 legacy
curvature entries are reconciled in its follow-on audit by distinguishing raw
day from mean-removed night projection. The cited 1,714,368 count is its
full account audit at 2e−8. This coverage precision does not change the
numerical closure. Our {len(crosscheck)} equivalent completed-check/053 primary
accounts agree within {scope['maximum_crosscheck_payload_difference_kg']:.9f} kg,
with matching least sets and usages.

CHECK-048's two lost-float cases and multilayer sorbent axis-count changes
come from **including cure compression**, not from choosing a different
thermal boundary. MAINLINE-053's zero-flip statement compares thermal choices
while holding that cure treatment fixed. Both findings stand.

The following source/status corrections apply to interpretation of the
inherited 048 material, without changing the selected multilayer inputs:

- SolarWhite has a manufacturer nominal mass of .285 kg/m² at 150 μm,
  with typical alpha .18 and hemispherical epsilon .89 on Al2024-T3.
  The previous missing-mass/ambiguous-label interpretation is superseded
  locally; installed Be performance is still unknown.
  [ENBIO sheet](https://enbio.eu/wp-content/uploads/2024/07/SolarWhite.pdf).
- NASA 2015 gives classical CCAg/ITO alpha .08 and **normal** epsilon .72
  on 3 mil Kapton. It does not support a hemispherical .09/.65 attribution.
  The classical assumed pair requires its patent citation and transfer
  caveat; the multilayer .09/.80 class is a different source.
  [NASA, slide19](https://ntrs.nasa.gov/api/citations/20150018109/downloads/20150018109.pdf).
- The twelve null sensitivity least fields have independently supplied
  floating witnesses. Their nulls cannot establish no-float conclusions;
  the witnesses do not repair failed finish screens or qualify wet/aged optics.
  The complete witnesses and corrected dispositions are pinned in this fold.

The completed checker resolves C01/C02/C03 arithmetic, C12 coverage and
C13 execution. Its ten open-evidence entries and two source/result corrections
are retained with dispositions. MAINLINE-053's nine physical NFI groups remain.
[PHYSICAL-EVIDENCE.json](PHYSICAL-EVIDENCE.json),
[CORRECTIONS.json](CORRECTIONS.json) and [NFI.json](NFI.json) record the basis.
No repeated optimizer or thermal solve was needed: the existing complete
four-boundary matrix already covers the requested readings. The short
dimensionless arithmetic and output comparisons ran on one process.
All previous filing bytes are verified unchanged. No successor is named.
"""
(ROOT/"CARD.md").write_text(card)
save("VALIDATION.json", dict(at=datetime.now().astimezone().isoformat(),
                             checks=len(checks), passed=sum(r["passed"] for r in checks),
                             failed=sum(not r["passed"] for r in checks), results=checks))
print(json.dumps(dict(checks=len(checks), failed=sum(not r["passed"] for r in checks),
                      inputs=len(pins), crosschecks=len(crosscheck),
                      max_payload_difference_kg=scope["maximum_crosscheck_payload_difference_kg"],
                      regime_Ri_range=[min(r["Ri"] for r in diagnostics), max(r["Ri"] for r in diagnostics)],
                      card_words=len(card.split()))))
assert all(r["passed"] for r in checks)
