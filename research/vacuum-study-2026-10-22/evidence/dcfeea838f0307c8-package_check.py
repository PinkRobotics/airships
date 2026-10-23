"""Assemble the check from independently derived outputs; no owner code is used."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[3]


def read(name):
    return json.loads((ROOT / name).read_text())


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def pin(path):
    data = path.read_bytes()
    return dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))


derived = read("REPRODUCED.json")
correction = read("SOURCE-CORRECTIONS.json")
extra = {r["id"]: r for r in correction["rows"]}
owner = read("intake/owner/RESULTS.json")["analysis"]
comparison = read("NUMERIC-COMPARISON.json")
digitized = read("DIGITIZATION.json")
cylinders = read("DIGITIZATION-CYLINDERS.json")
aux = read("AUXILIARY.json")
leads = read("LEAD-INPUT-CHECK.json")

nfi = []


def issue(key, question, next_step, evidence):
    nfi.append(dict(id=key, status="open", tag="QUESTIONABLE", issue=question,
                    next_evidence=next_step, evidence=evidence, blocks_card=False))


issue("NFI-C035-SII", "S-II core properties, actual geometry, plasticity and thermal reductions are unresolved.",
      "Recover Gonzalez/Patton SDL 468 and specimen-level pressures, faces, core shear, imperfections and reduction method; then compute compatible Vc and KDF.",
      ["E07", "DIGITIZATION.json"])
issue("NFI-C035-BASELINE", "Anisotropic/combined-load SBKF FE ratios are not proven to share the lead sphere's scalar denominator.",
      "Derive matching anisotropic shell baselines and shear corrections, retaining actual load and boundary conditions; compare with the scalar proxy.",
      ["E01", "E04", "E05", "METHOD.md"])
issue("NFI-C035-SCALAR", "Vc depends on scalarization, nominal versus measured thickness and stress-dependent properties.",
      "Publish nominal, as-built and directional conventions separately; recover measured G12 and effective core shear where possible.",
      ["E01", "E02", "SOURCE-CORRECTIONS.json"])
issue("NFI-C035-TRANSFER", "The 0.30–0.34 handbook ratio and SBKF-scaled sphere envelope are projections.",
      "Resolve the lead's closed-sphere geometry, imperfections, loading and shear model directly; retain transfer estimates as PROJECTION.",
      ["E09", "E10", "SOURCE-CORRECTIONS.json"])
issue("NFI-C035-CTA83", "The source's printed 0.864 conflicts with 432000/499246=0.8653048798.",
      "Resolve the precise reference load or rounding convention in NASA/TM-20210024768. Retain both alternatives explicitly until then.",
      ["E05", "AUXILIARY.json"])
issue("ref-196608af78549ed7f1ff", "Primary Baker, FPL, Hexcel and Kazimi specimen reports remain unread.",
      "Acquire the named primary reports and recover dimensions, materials, core shear and test denominators; replace handbook graph estimates.",
      ["E06", "E08", "DIGITIZATION-CYLINDERS.json"])
issue("NFI-C035-BRIX", "Brix 1968 sandwich-dome paper remains an unread experimental lead.",
      "Retrieve Durchschlagen von GFP-Sandwichkuppeln, IfL 7(11), 408–413; extract actual loading, dimensions, moduli and test/prediction values.",
      ["intake/owner/LIT-C.json", "EVIDENCE.md"])
issue("NFI-C035-SIM", "035's Vc≈200, R/rho≈26 and crimp ratios 1.44–1.54 have no independently reconstructed chain here; Sim's uniform-pressure results are FE.",
      "Recover the exact 018b/EUCASS2023-367 inputs and reduction formulas. Keep platen tests separate from uniform-pressure simulations.",
      ["E15", "intake/owner/CARD.md"])
issue("NFI-C035-YANG", "The new egg-shaped vessel has plastic collapse and no compatible scalar Vc established.",
      "Recover effective core shear and local-curvature/denominator definitions; retain its 12.44 MPa physical result without assigning an elastic sphere KDF.",
      ["E17", "AUXILIARY.json"])
issue("NFI-C035-TANG-MARINE", "Tang's 2025 elliptical steel/resin pressure-hull experiment is an abstract-level lead.",
      "Acquire DOI 10.1016/j.marstruc.2025.103855 full text and numerical tables; classify plasticity, curvature and Vc before comparison.",
      ["E18"])
issue("NFI-C035-TANG-JSSM", "Tang's three sandwich ellipsoids use a stronger/stiffer core; applicability to a soft-core model is unresolved.",
      "Acquire DOI 10.1177/10996362251383617 full text and recover geometry, effective properties and independent test/eigenvalue ratios.",
      ["E19"])
issue("NFI-C035-BARATHAN", "The owner's C05 semi-ellipsoid hydrostatic experiment was omitted from its categorical conclusion.",
      "Acquire DOI 10.1080/15376494.2022.2114049 full text and classify test pressures, theory, geometry and effective shear.",
      ["E20", "intake/owner/LIT-C.json"])
issue("NFI-C035-DENARDO", "A documented foam-core cylinder experiment contradicts the card's no-test claim; full thesis access failed.",
      "Retrieve DeNardo 2017 URI thesis 1075 and reconstruct geometry, effective shear and test/perfect-shell ratios.",
      ["E21", "intake/owner/LIT-D.json", "sources/FETCH-04.json"])
issue("NFI-C035-MUC", "Muc's 8.49% eigenvalue overprediction is supported, but an effective measured core-shear Vc is not.",
      "Separate constituent-wall assumptions from homogenized honeycomb shear and recover a specimen-compatible Vc.",
      ["E14"])
issue("NFI-C035-IMPERFECTION", "The record does not establish that required imperfection control exceeds every recorded sandwich dome.",
      "Quantify the lead geometry's admissible measured imperfection distribution; compare like geometry/material/boundary cases before any universal claim.",
      ["E07", "E17", "E18", "E19", "E20"])
issue("NFI-C035-RESTRICTED", "Restricted DESICOS and other abstract-only leads prevent an exhaustive claim about modern cylinder data.",
      "Retain access limitations in the evidence ledger and inspect full specimen data when accessible.",
      ["intake/owner/LIT-B.json", "intake/owner/NFI.json"])

mismatches = []


def mismatch(row, field, old, new, category, evidence, fix, nfi_id=None, **kw):
    item = dict(id=f"C035-M{len(mismatches)+1:03d}", row=row, field=field,
                card_value=old, checker_value=new, category=category,
                tag="QUESTIONABLE", evidence=evidence, proposed_fix=fix,
                blocks_card=False)
    if nfi_id:
        item["nfi"] = nfi_id
    item.update(kw)
    mismatches.append(item)


for p in digitized["points"]:
    for field, old_field, unc in [("gamma", "owner_gamma", .01),
                                 ("R_over_rho", "owner_R_over_rho", 5)]:
        mismatch("RESULTS.json/analysis/SII: " + p["id"], field,
                 p[old_field], p[field], "graph_read_refinement", ["E07", "DIGITIZATION.json"],
                 "Use calibrated rounded graph values; do not report pixel precision as specimen precision.",
                 "NFI-C035-SII", read_uncertainty=unc,
                 within_checker_read_uncertainty=abs(p[field]-p[old_field]) <= unc)

cyl_map = [
    ("FPL1830_low", 0), ("FPL1830_high", 1), ("Baker_180", 2),
    ("Baker_270_high", 3), ("Baker_270_mid", 4), ("Baker_270_low", 5),
    ("Baker_410", 6), ("PE227_high", 7), ("PE227_mid", 8), ("PE227_low", 9)]
by_cyl = {p["id"]: p for p in cylinders["points"]}
for name, i in cyl_map:
    p = by_cyl[name]
    old_r, old_g, _ = owner["CR1457_cylinder_points_eye_read"][i]
    for field, old_value, unc in [("R_over_rho", old_r, .05*p["R_over_rho"]),
                                  ("gamma", old_g, .01)]:
        mismatch("RESULTS.json/analysis/CR1457_cylinder_points_eye_read/" + str(i),
                 field, old_value, p[field], "graph_read_refinement",
                 ["E06", "DIGITIZATION-CYLINDERS.json"],
                 "Retain approximately 5% in R/rho and 0.01 in gamma; these existing points agree at graph precision.",
                 "ref-196608af78549ed7f1ff", read_uncertainty=unc,
                 within_checker_read_uncertainty=abs(p[field]-old_value) <= unc)
missing = by_cyl["Baker_omitted"]
mismatch("CARD §1 / CR-1457 axial set", "cylinder_point_count", 10, 11, "omission",
         ["E06", "DIGITIZATION-CYLINDERS.json"],
         "Add the Baker point near R/rho=121, gamma=0.61.",
         "ref-196608af78549ed7f1ff",
         omitted_point={k: missing[k] for k in ["R_over_rho", "gamma"]})

for group in ["sbkf", "leads"]:
    for i, row in enumerate(derived[group]):
        source = extra[row["id"]]
        mismatch(f"RESULTS-ANALYSIS.json/{group}/{i} ({row['id']})",
                 "CR1457_cyl_curve", row["CR1457_cyl_curve"], source["CR1457_exact"],
                 "source_formula_refinement", ["E06", "SOURCE-CORRECTIONS.json"],
                 "Replace the declared three-node eye fit with CR-1457's 0.75*SP-8007 expression.")
        if group == "sbkf":
            mismatch(f"RESULTS-ANALYSIS.json/{group}/{i} ({row['id']})",
                     "beat_CR1457_curve", row["beat_CR1457_curve"], source["beat_CR1457_exact"],
                     "source_formula_refinement", ["E06", "SOURCE-CORRECTIONS.json"],
                     "Propagate the exact handbook curve; the original division itself reproduces.")
        else:
            mismatch(f"RESULTS-ANALYSIS.json/leads/{i} ({row['id']})",
                     "need_over_SII_hemisphere", row["need_over_SII_hemisphere"],
                     source["revised_need_over_SII_center"], "graph_read_propagation",
                     ["E07", "SOURCE-CORRECTIONS.json"],
                     "Use revised graph centers and display their read uncertainty; this is a numerical comparison, not a transferable allowable.",
                     "NFI-C035-SII",
                     read_envelope=source["revised_need_over_SII_read_envelope"])
            for field, revised in [
                ("old_sandwich_cylinders_interpolated", "revised_old_cylinder_interpolation"),
                ("need_over_old_cylinders", "revised_need_over_old_cylinders")]:
                mismatch(f"RESULTS-ANALYSIS.json/leads/{i} ({row['id']})",
                         field, row[field], source[revised], "graph_read_propagation",
                         ["E06", "SOURCE-CORRECTIONS.json"],
                         "Retain as a two-point log interpolation with graph uncertainty, not a record envelope.",
                         "ref-196608af78549ed7f1ff")

mismatch("CARD §1 CTA8.3", "gamma", .864, aux["cta83_test_over_combined_linear"],
         "source_inconsistency", ["E05", "AUXILIARY.json"],
         "Retain the printed 0.864 and the load-derived 0.865305 as alternatives; do not silently correct the source.",
         "NFI-C035-CTA83")
mismatch("CARD §4 best results", "manufacturing", "Autoclave or AFP",
         "CTA8.1: hand-laid IM7/MTM45, out-of-autoclave; other articles require their own process descriptions.",
         "source_description", ["E01"], "Correct the CTA8.1 fabrication description.")
mismatch("CARD §2 Vc map / CTA8.1", "nominal_vs_measured_ply_in", .0052, .005679,
         "input_qualification", ["E01", "SOURCE-CORRECTIONS.json"],
         "Label the original point nominal. Measured thickness with the same assumed moduli gives Vc_iso=0.573914 and R/rho=331.317.",
         "NFI-C035-SCALAR")
mismatch("CARD §2 Vc conventions / CTA8.1", "Vc_axial",
         derived["sbkf"][0]["Vc_axial"], extra["CTA8.1"]["Vc_axial_reciprocal_nu"],
         "alternative_convention", ["METHOD.md", "SOURCE-CORRECTIONS.json"],
         "State that 0.412724 substitutes nu_xy into an isotropic equation; reciprocal orthotropic denominator gives 0.400216. Neither is a validated anisotropic shell scalar.",
         "NFI-C035-SCALAR")
mismatch("CARD §2 and §3", "SBKF_baseline_equivalence",
         "Shear-inclusive eigenvalue makes gamma directly the same basis; classical baseline and Kc identical.",
         "Isotropic ideal-shell resultant coincidence does not identify anisotropic combined-load FE denominators or shear corrections.",
         "unsupported_inference", ["E01", "E04", "E05", "METHOD.md"],
         "Tag all cross-geometry uses PROJECTION and retain actual specimen denominators.",
         "NFI-C035-BASELINE")
mismatch("CARD §3 handbook sphere/cylinder comparison", "meaning_of_ratio",
         "0.30–0.34 sphere penalty",
         {"021_rev1": extra["021 rev1"]["sphere_to_cylinder"],
          "021b": extra["021b"]["sphere_to_cylinder"],
          "scope": "SP-8032 phi=90 degrees, nu=0.3 cap formula divided by SP-8007; no established sandwich-shell transfer law"},
         "scope_qualification", ["E09", "E10", "METHOD.md"],
         "Preserve the arithmetic; explicitly state cap geometry and label the transfer PROJECTION.",
         "NFI-C035-TRANSFER")
mismatch("CARD §1 TN D-2926", "denominator",
         "Small deflection, about 0.87–0.92; CR-1457 reads 0.62–0.80.",
         "Source uses stiffness at calculated inelastic buckling; test-state stiffness lowers ratios by about 6–20%.",
         "basis_qualification", ["E11"],
         "Identify inelastic normalization before comparing the two reported ranges.",
         "NFI-C035-BASELINE")
mismatch("CARD §1 CR-1457 lateral pressure / FPL", "test_resolution",
         "Five measured/theory ratios 1.00–1.16",
         "The handbook uses 52.5 psi as the midpoint of 50–55 psi onset for four tests; ratios reproduce but do not have independent pressure resolution.",
         "basis_qualification", ["E08", "AUXILIARY.json"],
         "Carry the reported pressure ranges and thick-face qualification.",
         "ref-196608af78549ed7f1ff")
mismatch("CARD §1 Sim / EUCASS", "uniform_pressure_measured_status",
         "Foam-core hemispheres in the test record", "Sim uniform-pressure results are FE; physical validation is platen compression.",
         "misclassification", ["E15"], "Separate measured loading cases from simulated uniform pressure.",
         "NFI-C035-SIM")
for field, value in [("Vc", 200), ("R_over_rho", 26), ("crimp_normalized_ratio", [1.44, 1.54])]:
    mismatch("CARD §1 Sim / EUCASS", field, value, None, "unreproduced_claim",
             ["E15", "intake/owner/CARD.md"],
             "No numerical credit: obtain the missing upstream input/formula chain; do not substitute an invented value.",
             "NFI-C035-SIM")
mismatch("CARD Answer and §4", "universal_absence_at_Vc_0.9_to_2",
         "No measured point exists in any shell form.",
         "This check did not establish a comparable elastic sphere/dome point with recoverable Vc near 1; available evidence cannot establish universal absence.",
         "unsupported_inference", ["E14", "E17", "E18", "E19", "E20", "E21"],
         "Scope the negative result to verified compatible data and retain unresolved leads.",
         "NFI-C035-RESTRICTED")
mismatch("CARD Answer / Spheres", "only_measured_dome_set",
         "Only S-II; nothing else was found.",
         "Additional marine egg-shaped/ellipsoidal hydrostatic experiments exist; their material, curvature and plasticity differ.",
         "literature_omission", ["E17", "E18", "E19", "E20"],
         "Add the new primary sources and preserve the owner's C05; do not assign unverified elastic gamma or Vc.",
         "NFI-C035-YANG")
mismatch("CARD §1 not found", "foam_core_cylinder_test",
         "No foam-core cylinder test found.",
         "DeNardo 2017 documents foam-core double-hull cylinder hydrostatic experiments; already in owner's D14.",
         "literature_omission", ["E21", "intake/owner/LIT-D.json"],
         "Correct the negative claim and retain the full-text acquisition row.",
         "NFI-C035-DENARDO")
mismatch("CARD §1 unread leads", "Anderson_1966_status", "Unread",
         "Full thesis inspected: theoretical, no experimental comparison for complete sandwich spheres.",
         "lead_closed", ["E16"], "Close the unread branch without creating a measured test point.")
mismatch("CARD §4 reading", "required_imperfection_control",
         "Beyond anything recorded for sandwich domes.",
         "Not established by the non-comparable and incomplete record.",
         "unsupported_inference", ["E07", "E17", "E18", "E19", "E20"],
         "Remove the universal assertion; quantify compatible imperfection tolerance.",
         "NFI-C035-IMPERFECTION")
mismatch("CARD §4 S-II construction", "quality_assurance_basis",
         "Production-quality aerospace construction",
         "CR-1457 does not establish a transferable quantified imperfection tolerance for the two hemispheres.",
         "scope_qualification", ["E07"], "Retain test identity while making imperfection quality unresolved.",
         "NFI-C035-SII")

save("NFI.json", dict(unit="vacuum-mainline035-check-1020", count=len(nfi),
                     objections_do_not_stop_work=True, rows=nfi))
save("MISMATCHES.json", dict(count=len(mismatches),
     note="Includes non-material graph refinements and alternative conventions; these are not all arithmetic failures.",
     arithmetic_comparison="NUMERIC-COMPARISON.json",
     categories=dict(Counter(m["category"] for m in mismatches)), rows=mismatches))

lines = ["# Exact differences and qualifications", "",
         "All sourced values are QUESTIONABLE. Transfers are PROJECTION. Stored graph digits identify computations, not experimental precision.",
         "", "| ID / row | Field | Card | Checker | Disposition |",
         "|---|---|---|---|---|"]
for m in mismatches:
    def cell(v):
        return json.dumps(v, ensure_ascii=False).replace("|", "/").replace("\n", " ")
    lines.append(f"| {m['id']} · {m['row']} | {m['field']} | {cell(m['card_value'])} | "
                 f"{cell(m['checker_value'])} | {m['category']}; {m.get('nfi', 'proposed fix')} |")
(ROOT / "MISMATCHES.md").write_text("\n".join(lines) + "\n")

pins = []
for name in ["intake/PINS.json", "intake/SOURCE-PINS.json", "intake/LEAD-PINS.json"]:
    for p in read(name):
        local = Path(p["local_path"]) if "local_path" in p else WORKSPACE / p["copy"]
        got = pin(local)
        assert got["sha256"] == p["sha256"] and got["bytes"] == p["bytes"], local
        pins.append(dict(source_path=p["path"], local_path=str(local), sha256=p["sha256"],
                         bytes=p["bytes"], verified=True, inventory=name))
save("INPUTS.json", dict(unit="vacuum-mainline035-check-1020",
                        tag="QUESTIONABLE", all_cross_geometry_transfers="PROJECTION",
                        pins=pins, primary_sources="EVIDENCE.md",
                        sbkf_transcribed_inputs=correction["rows"][:4],
                        lead_inputs=leads, graph_calibration=["DIGITIZATION.json", "DIGITIZATION-CYLINDERS.json"],
                        owner_script_used=False))

coverage = [
    ("SBKF laminate, Vc, rho, equivalent thickness and guideline ratios",
     "112-field reproduction plus source inputs", "NUMERIC-COMPARISON.json; SOURCE-CORRECTIONS.json"),
    ("021/021b lead geometry, Vc and required gamma", "independently reproduced", "LEAD-INPUT-CHECK.json"),
    ("S-II two hemispheres and six ellipsoids", "calibrated; revised readings", "DIGITIZATION.json"),
    ("CR-1457 eleven cylinders", "ten reproduce at graph precision; one omitted", "DIGITIZATION-CYLINDERS.json"),
    ("CR-1457 two cones", "separately digitized; not used in cylinder interpolation", "DIGITIZATION-CYLINDERS.json; E06"),
    ("CR-1457 lateral pressure seven cylinders", "ratios calculated; FPL midpoint caveat", "AUXILIARY.json; E08"),
    ("TN D-2926 three cylinders", "figure range reproduced; inelastic basis", "E11; sources/d2926-p29.png"),
    ("TN D-7935 three cones", "six measured/predicted ratios calculated", "AUXILIARY.json; E12"),
    ("Pineda five fairing panels", "ten prediction/test errors calculated", "AUXILIARY.json; E13"),
    ("Muc deep cylindrical panels", "8.49% source statement and reciprocal ratio", "AUXILIARY.json; E14"),
    ("Sim / EUCASS high-Vc hemisphere row", "classification corrected; three numeric claims unresolved", "NFI-C035-SIM; E15"),
    ("018 optimistic curve at SBKF and lead points", "reproduced arithmetic; projection", "AUXILIARY.json"),
    ("SBKF scaled-cylinder and sphere envelopes", "reproduced arithmetic; projection", "REPRODUCED.json; NFI-C035-TRANSFER"),
    ("CTA8.3 posttest 0.1% agreement", "431.6/432.0 gives -0.09259%; source chronology retained", "AUXILIARY.json; E05"),
    ("Sphere/cylinder handbook ratio 0.30–0.34", "reproduced under phi=90°, nu=0.3", "SOURCE-CORRECTIONS.json; E09; E10"),
    ("New egg-shaped measured vessel", "two ratios calculated; plastic collapse, Vc unresolved", "AUXILIARY.json; E17"),
]
save("COVERAGE.json", dict(rows=[dict(card_row=a, status=b, record=c) for a,b,c in coverage],
                         claim="Every load-bearing card row has a calculation, source check, or explicit unresolved status. Not every source claim is independently reconstructible."))

[withheld: private task or principal quotation; scientific result/status retained elsewhere]