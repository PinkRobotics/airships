"""Build the independent check package from completed numerical work."""
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

import check021 as c

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

source_rows = [
    {
        "id": "SRC-S200", "source": F, "location": "DS-HPP-610 pp.1-2",
        "verified": {"rho_kg_m3": 1850, "E_GPa_typical": 290, "S200F_min_tensile_yield_MPa": 241},
        "tag": "QUESTIONABLE", "note": "No compressive minimum in the datasheet. Its physical-property row is shared by F/FC/FH.",
    },
    {
        "id": "SRC-GUIDE", "source": G, "location": "p.4; rendered page read",
        "verified": {"S200F_compressive_yield_about_MPa": 255},
        "tag": "QUESTIONABLE", "note": "Manufacturer narrative, not a minimum or lot acceptance value.",
    },
    {
        "id": "SRC-SR200", "source": S, "location": "DS-HPP-613 pp.1-2",
        "verified": {"rho_kg_m3": 1850, "E_GPa_typical": 290, "min_tensile_yield_MPa": 345,
                     "max_sheet_inches": [24, 72], "thin_smaller_sheet_range_inches": [.020, .058]},
        "tag": "QUESTIONABLE", "note": "Compression is not specified. The printed inch/mm range contains an inconsistency.",
    },
    {
        "id": "SRC-SHEET-LOT", "source": N, "location": "PDF p.22, Tables 2-3, visually checked",
        "verified": {"compressive_yield_MPa": [379.2, 382.7], "tensile_yield_MPa": [383.4, 386.1],
                     "in_plane_E_GPa": [298.7, 293.6], "in_plane_nu": [.0768, .0752], "thickness_mm": 1.96},
        "tag": "QUESTIONABLE", "note": "NASA's report quotes the Fenn et al. 1967 measurements. The original Fenn report was not opened; the card properly calls this second-hand. A guaranteed minimum at 0.84 mm is not established.",
    },
    {
        "id": "SRC-I220", "source": "https://hkvxni.files.cmp.optimizely.com/download/a0b9e6e0f75f11eebf51367a729f0e29",
        "location": "manufacturer datasheet accessed through its product-page link",
        "verified": {"I220H_min_tensile_yield_MPa": 345, "E_GPa_typical": 290},
        "tag": "QUESTIONABLE", "note": "No compressive value; the card correctly avoids treating this tensile minimum as a sourced compressive strength.",
    },
    {
        "id": "SRC-TUBES", "source": T, "location": "PDF p.35, Table VIII, visually checked",
        "verified": {"type_A_compressive_yield_MPa": 450, "type_PS_compressive_yield_MPa": 544},
        "tag": "QUESTIONABLE", "note": "Tube observations correct the scope of 'strongest'; they are not substituted into the face model.",
    },
    {
        "id": "SRC-HEXCEL", "source": H, "location": "Table II, 5056 3/8-1.0 and 1/4-1.6",
        "verified": {"3/8-1.0": {"rho_pcf": 1, "Ec_ksi": 15, "Gc_W_ksi": 6.8, "crush_psi": 35},
                     "1/4-1.6": {"rho_pcf": 1.6, "Ec_ksi": 30, "Gc_W_ksi": 10.5, "crush_psi": 50}},
        "tag": "QUESTIONABLE", "note": "These reproduce the pinned leading core inputs. Core-wide search uses all 51 pinned rows; it is not a fresh validation of every core manufacturer's test data.",
    },
    {
        "id": "SRC-CR1457", "source": CR, "location": "pp.2-5, 2-7, 2-26, 2-33, 6-5, 6-12",
        "verified": {"wrinkle_coefficients": [.33, .82], "beta": c.BETA, "gamma_below_Vc2": .2,
                     "gamma_at_or_above_Vc2": 1},
        "tag": "QUESTIONABLE hemisphere-to-sphere and homogenized-core transfers",
        "note": "The continuous gamma curve is MAINLINE-018's PROJECTION, not a handbook equation. Formula checks use the supplied hash-verified primary PDF.",
    },
]

def pin(path):
    p = Path(path)
    b = p.read_bytes()
    return {"path": str(p.resolve()), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

brief_paths = [
    "withheld-source:1577f21d44c55eff",
    "withheld-source:b528d6a62c81ce0b",
]
inputs = {
    "schema": 1, "unit": meta["unit"], "order": meta["authority"], "brief_pins": [pin(p) for p in brief_paths],
    "target_report": pin(ROOT / "snapshots/owner-report.json"),
    "target_card": pin(ROOT / "snapshots/CARD.md"), "original_artifact_pin_audit": pin_audit,
    "upstream_pins": upstream_pins, "independent_sources": source_rows,
    "source_downloads": [
        row for filename in ("MANIFEST.json", "MANIFEST-retry.json")
        for row in json.loads((ROOT / "sources" / filename).read_text())
    ],
    "scope": "Arithmetic on all 51 pinned core rows; primary beryllium/source audit. The original owner script was not read for its implementation, executed, or imported. It was copied only as bytes for the pin audit.",
    "model_inputs": {
        "R_m": {"value": 10, "tag": "PINNED case"}, "p_Pa": {"value": c.P, "tag": "PINNED ISA case"},
        "lift_kg": {"value": c.LIFT, "tag": "PINNED ISA case"},
        "face_density_kg_m3": {"value": 1850, "tag": "QUESTIONABLE", "source": F},
        "original_E_Pa": {"value": 303e9, "tag": "QUESTIONABLE inherited; current source differs",
                          "source": "Pinned MAINLINE-014b INPUTS.json Be row"},
        "original_strength_Pa": {"value": 283e6, "tag": "QUESTIONABLE inherited; current source differs",
                                 "source": "Pinned MAINLINE-014b INPUTS.json Be row, inherited from MAINLINE-008"},
        "original_nu": {"value": .33, "tag": "QUESTIONABLE inherited Al value; not independently sourced for Be",
                        "source": "Pinned COMMON.md aluminium tuple and MAINLINE-014b global nu"},
        "margin_fraction": {"value": .05, "tag": "ASSUMPTION pending MAINLINE-019"},
        "systems_kg": {"value": 100, "tag": "ASSUMPTION common mass rule"},
        "joints_fraction": {"value": .05, "tag": "ASSUMPTION common mass rule"},
    },
    "numeric_libraries": {"numpy": np_version if (np_version := __import__("numpy").__version__) else None,
                          "scipy": __import__("scipy").__version__},
}
results = {
    "schema": 1, "card": "CHECK-MAINLINE-021", "unit": meta["unit"], "authority": meta["authority"],
    "status": "ARITHMETIC_REPRODUCED_WITH_SOURCE_GAPS", "tag": "QUESTIONABLE",
    "certification": "none", "started_at": meta["started_at"], "ended_at": ended,
    "times_are": "measurements only, not limits",
    "scope": inputs["scope"], "calculations": calc, "supplemental": extra,
    "source_audit": source_rows,
    "observed_pin_mismatches": [r for r in pin_audit if not r["matches_pin"]],
    "nfi_ids": [row["id"] for row in nfi],
    "next": NEXT,
}
(ROOT / "INPUTS.json").write_text(json.dumps(inputs, indent=2) + "\n")
(ROOT / "RESULTS.json").write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
(ROOT / "NFI.json").write_text(json.dumps({"schema": 1, "unit": meta["unit"], "tag": "QUESTIONABLE",
                                         "rows": nfi, "objections_do_not_stop_next_cards": True}, indent=2) + "\n")

source_text = f"""# MAINLINE-021 source check

All material observations below remain QUESTIONABLE when transferred to this hull. The gamma interpolation remains PROJECTION. The arithmetic uses the exact pinned case and core catalogue; source changes are separate sensitivities.

S-200F: the current datasheet gives density 1850 kg/m³, typical E 290 GPa, and minimum tensile yield 241 MPa. It does not specify a compressive minimum. Its footnote offers SR-200 and PS-200 below 6.3 mm as additional options; it does not require that substitution. [Materion DS-HPP-610]({F}).

The design guide's page 4 gives S-200F compression about 255 MPa. That verifies the owner's sensitivity value, not its inherited 283-MPa starting strength. [Materion design guide]({G}).

SR-200: density 1850 kg/m³, typical E 290 GPa and minimum tensile yield 345 MPa are reproduced. Compression is unspecified. Maximum sheet dimensions are 24 by 72 inches; thinner stock from 0.020 to 0.058 inch has reduced dimensions. The printed inch/mm range has a unit inconsistency: 0.059 inch is 1.4986 mm, not 0.5 mm. [Materion DS-HPP-613]({S}).

The sheet lot: Table 3 confirms 379.2/382.7 MPa compressive and 383.4/386.1 MPa tensile yield. Table 2 gives in-plane E 298.7/293.6 GPa and Poisson ratios 0.0768/0.0752. The 1.96-mm sheet measurements are quoted from Fenn et al. (1967); the original Fenn report was not opened. Neither a modern minimum nor transfer to the 0.84-mm faces is established. [NASA CR-194164, PDF p.22]({N}).

I-220H's 345-MPa number is a tensile minimum, not sourced compression. The owner correctly kept this distinction. [Materion instrument-grade datasheet](https://hkvxni.files.cmp.optimizely.com/download/a0b9e6e0f75f11eebf51367a729f0e29).

The wording “strongest sourced beryllium” needs a product-form scope. Table VIII also reports 450 MPa compression for type A tubing and 544 MPa for type PS tubing. These are not interchangeable with sheet face properties. [NASA TN D-4833, PDF p.35]({T}).

The leading aluminium cores match Hexcel Table II. For 5056 3/8-1.0: 1 pcf, stabilized Ec 15 ksi, W shear modulus 6.8 ksi and crush strength 35 psi. For 1/4-1.6: 1.6 pcf, 30 ksi, 10.5 ksi and 50 psi. These are typical table values; the transfer to the shell remains QUESTIONABLE. [Hexcel CR III]({H}).

The handbook supports the six equations cited in CHECK.md. In particular, equibiaxial honeycomb dimpling is half its uniaxial value; the wrinkle interaction gives β³+β=1. The smooth gamma curve is the owner's explicitly tagged projection. [NASA CR-1457]({CR}).

The input audit confirms a QUESTIONABLE or PROJECTION tag and an inherited source reference for every eligible core row. Rechecking the whole vendor catalogue is outside this independent arithmetic check; the selected leading core values were checked directly. Source download hashes and access results are in INPUTS.json. Initial direct downloads failed; subsequent ordinary browser-header downloads succeeded for the three Materion PDFs. NASA PDFs were downloaded directly. The primary tables and guide page were visually read.
"""
(ROOT / "SOURCE-AUDIT.md").write_text(source_text)

lines = [
    "# Independent CHECK of the filed MAINLINE-021",
    "",
    f"Authority {meta['authority']}. Started {meta['started_at']}; completed {ended}. Times are measurements. This is a QUESTIONABLE estimate check, not certification.",
    "",
    "The filed floating point and all eight subset outcomes reproduce. Its material-source conclusions remain conditional. The independent calculation used no owner program. Two filed byte pins had already changed; the original CARD was intact when snapshotted. INPUTS.json and PIN-AUDIT.json preserve that distinction.",
    "",
    "**Calculation.** Let f be the core share of sandwich mass. A=4πR²; M=(0.95L−100)/1.05; tf=M(1−f)/(2Aρf); tc=Mf/(Aρc); h=tf+tc. These give M=4328.542897788202 kg. Applied face stress s=pR/(4tf). The independent program uses the following equations with elastic reduction η=1:",
    "",
    "| Quantity | Equation |",
    "|---|---|",
    "| Reference stress | σ₀=E h/[R√(1−ν²)] |",
    "| Bare crimp stress | σc=Gc h²/(2 tf tc) |",
    "| Branch parameter | Vc=σ₀/σc; Kc=1−Vc/4 for Vc≤2, otherwise 1/Vc |",
    "| Global SF | γ Kc σ₀/s |",
    "| Face compression SF | σface/s |",
    "| Crimp SF | σc/s |",
    "| Crush SF | 2 σcrush/p, as pinned |",
    "| Honeycomb wrinkle SF | β C √(E Ec tf/tc)/s |",
    "| Foam wrinkle SF | β C [E Ec Gc/(1−ν²)]^(1/3)/s |",
    "| Biaxial dimpling SF | E(tf/cell)²/[(1−ν²)s] |",
    "",
    f"β={c.BETA:.15f} solves β³+β=1. The dimpling expression applies the straight-line biaxial interaction. [CR-1457 equations 2.1-4/6, 2.2-5/6/12/14/15 and 6.2-1 through 6]({CR}). The hemisphere step is γ=.2 below Vc=2 and 1 at or above 2. O1 replaces that with .2+.4 min(Vc,2); it is not multiplied by another knockdown.",
    "",
    "**Filed geometry.** At f=.094, tf=0.843448044193 mm, tc=20.213376387492 mm, h=21.056824431685 mm, Vc=1.108627964228 and Kc=.722843008943. Faces weigh 3921.659865396 kg; core 406.883032392; joints 216.427144889; systems 100. The 244.472107509-kg unused-lift allowance makes their sum 4889.442150187 kg. Hardware mass alone is 4644.970042678 kg.",
    "",
    "| Mode | Filed rounded value at required settings | Independent | Full named set, independent |",
    "|---|---:|---:|---:|",
]
claimed_modes = {"global_buckling": "1", "face_compression": "1 (report 1.0002)",
                 "core_shear_crimping": "2.155", "core_crush": "5.056",
                 "face_wrinkling": "1", "intracell_dimpling": "9.423"}
for mode, printed in claimed_modes.items():
    lines.append(f"| {mode} | {printed} | {main['needed_set'][mode]:.12f} | {main['full_set'][mode]:.12f} |")
lines += [
    "",
    f"Required γ={main['needed']['gamma']:.15f}, required C={main['needed']['wrinkle']:.15f}; their multipliers over .2/.33 are {main['needed']['gamma']/.2:.12f} and {main['needed']['wrinkle']/.33:.12f}. The minimum required face strength is {main['needed']['strength']/1e6:.12f} MPa. The card's 283 MPa is its retained available strength, rounded up from the demand; it is not an exact equality at the grid geometry. Hence compression SF is 1.000183118954. With no optimism the least SF is .345334007240, global. Uniaxial dimpling is 18.846294251648; the stated biaxial correction is correct.",
    "",
    "**Subset search.** The reported usage values use a geometric scale: u=max(0, ln(required/today)/ln(full/today)). They are not ordinary linear shares of the value difference. For γ on the crimp branch, today=full=1 and there is no stretch. The objective is min max(u) among the selected optimisms, with every unselected and fixed mode ≥1. An independent 4,000-step search across all 51 cores reproduces every filed outcome. A second search partitions the domain using polynomial roots of all fixed-mode boundaries and Vc=2, then refines the objective within each feasible interval.",
    "",
    "| Subset | Filed usage | Independent 4000-step usage | Refined usage | Fits named range? |",
    "|---|---:|---:|---:|---|",
]
filed_usage = ["none", "1.017", "none", "none", ".9099", ".9991", ".9752", ".5286"]
for index, row in enumerate(extra["grid4000_subsets"]["E303-sigma283"]):
    grid = row["best"]
    refined = calc["scenarios"][0]["subsets"][index]["best"]
    label = ", ".join(row["subset"]) or "{}"
    gv = f"{grid['usage']:.12f}" if grid else "no feasible geometry"
    rv = f"{refined['max_usage']:.12f}" if refined else "no feasible geometry"
    fits = "yes" if refined and refined["feasible_within_named"] else "no"
    lines.append(f"| {label} | {filed_usage[index]} | {gv} | {rv} | {fits} |")
refined = calc["scenarios"][0]["floating_point"]
lines += [
    "",
    f"The minimum cardinality remains two. Gamma plus wrinkling remains the least two-member set under the inherited tuple. Its refined point is f={refined['fraction']:.15f}, tf={refined['tf_m']*1000:.12f} mm, tc={refined['tc_m']*1000:.12f} mm, γ={refined['needed']['gamma']:.12f}, C={refined['needed']['wrinkle']:.12f}, and σrequired=283 MPa. The .9099 to .908635413226 difference is grid resolution, not a failed floating point.",
    "",
    "**Family checks.** All reported mode values at the three full-set geometries reproduce to the displayed precision. Refining the geometry gives small improvements. Today's and conservative-grid values likewise differ from continuous maxima by grid resolution.",
    "",
    "| Family | Setting | Filed least SF | Independent refined maximum |",
    "|---|---|---:|---:|",
]
filed_families = {"aluminium": [.6167, 1.309, .8779], "aramid": [.6497, 1.010, .3622], "other": [.4782, 1.156, .539]}
for group, printed in filed_families.items():
    for setting, claimed in zip(("today", "full", "conservative"), printed):
        best = calc["families"][f"303GPa/{group}/{setting}"]["refined"]
        lines.append(f"| {group} | {setting} | {claimed:g} | {best['least']:.12f} |")
lines += [
    "",
    "The full-set geometry checks are stored in RESULTS.json: aluminium f=.115, aramid f=.308, fiberglass f=.21875. Para-aramid Kevlar belongs to the aramid family. The other family is fiberglass plus PMI foam. The aluminium 1/4-1.6 and 3/8-1.6 rows tie on the active modes; smaller cells improve dimpling.",
    "",
    "**Source changes and exact mismatches.**",
    "",
    "| Row / field | Filed value | Independent source or calculation | Disposition |",
    "|---|---|---|---|",
    f"| S-200F/SR-200 E | 303 GPa | Datasheets: 290 GPa typical | NFI MODULUS; [S-200F]({F}), [SR-200]({S}) |",
    f"| Same main geometry, required gamma/C at E290 | .579149449 / .362641644 in headline | {corrected['needed']['gamma']:.12f} / {corrected['needed']['wrinkle']:.12f} | Headline tuple needs revision; its E290 sensitivity reproduces |",
    "| SR-200 minimum-strength sensitivity, fewest optimisms | gamma alone at E303 | At E290, gamma-only refined usage 1.068036393540 (outside named range); two are needed | The material-coupled sheet claim changes |",
    f"| Same sheet geometry under full gamma, C=.33 | global 1, wrinkle 1 | global {sheet['full_set']['global_buckling']:.12f}, wrinkle {sheet['today']['face_wrinkling']:.12f} at E290 | Both fall below 1 |",
    f"| S-200F compression starting value | inherited 283 MPa | Guide: about 255 MPa; required here 282.948186824 MPa | {main['needed']['strength']/255e6:.9f}× uplift over that source; [guide]({G}) |",
    f"| Be Poisson ratio | inherited .33 | Sheet ν12=.0768, ν21=.0752 | Orthotropic source; [Table 2]({N}) |",
    f"| Main fixed geometry, full gamma, E290 and ν=.0768 surrogate | source-consistent claim not supplied | global SF {nu_case['full_set']['global_buckling']:.12f}; gamma needed {nu_case['needed']['gamma']:.12f} versus curve {nu_case['gamma_full']:.12f} | Sensitivity only, not an orthotropic solution |",
    f"| Strongest sourced Be | 379.2 MPa | Supported sheet value; tube source also gives 450/544 MPa | Restrict claim to applicable sheet; [tube Table VIII]({T}) |",
    "| Required strength exactly 283 MPa | 283 MPa | 282.948186824 MPa demand; 283 MPa supplied | Harmless rounding/operating-value distinction |",
    "",
    "The strength-255/E303 sensitivity and E303 sheet-345 sensitivity reproduce the filed subset choices. At E290/255 with a grade change to SR-200 at its weaker measured in-plane E=293.6 GPa, the least pair is wrinkling plus strength: C=.813883456390, σrequired=368.627416938 MPa, usage .991774266810 on HRH-10. That still uses the questionable gamma=1 crimp exception. It is a conditional alternative, not proof of the original aluminium route.",
    "",
    "Using ν=.0768 as an isotropic sensitivity changes the E290/283 least pair to wrinkling plus strength on HRH-10. This does not certify an isotropic substitute for orthotropic sheet. It demonstrates why the inherited .33 must be visible as a separate material assumption.",
    "",
    "**Validation and carry.** The 20 recorded checks pass: the 009d five common modes plus uniaxial dimpling, all five 009c-5 held-geometry modes, the .324125581629 gamma requirement, the wrinkle interaction root, and all seven optimized scenario points. The independently rebuilt 4000-point search reproduces the reported eight subsets. The 009c-5 continuously reoptimized least is .650413021166, within 1.3e-9 of the owner's .650413022410. The separate 009d held-point dimpling difference is the card's declared factor of two.",
    "",
    "Five NFI rows record the pin, modulus, Poisson-ratio, strength/form, and strongest-source-scope issues. They do not stop any next card. Gamma's experimental grounding, the wrinkle coefficient, the five-percent mass allowance and joints remain the owner's existing pending work. Reproduce with `python3 check021.py`, then `python3 supplemental.py`, from this directory. The original owner program is neither required nor run.",
    "",
    "Next: the queue now assigns MAINLINE-021b under ord-admiral-rr2-check021b-after-021-codex-1020, starting after this report is filed. The frozen original 021 card is checked; the changed result snapshot is preserved but not approved as a revised release.",
]
# The source-correct sheet gamma-only result is read from the calculation, not
# hand-maintained in the report.
sheet_gamma_usage = calc["scenarios"][5]["subsets"][1]["best"]["max_usage"]
text = "\n".join(lines).replace("1.068036393540", f"{sheet_gamma_usage:.12f}") + "\n"
(ROOT / "CHECK.md").write_text(text)

card = f"""# CHECK MAINLINE-021 — arithmetic reproduced; source gaps remain

Order {meta['authority']}. Started {meta['started_at']}; completed {ended}. QUESTIONABLE, with gamma interpolation PROJECTION. No certification.

The original 0.843448-mm Be / CR-III 5056 3/8-1.0 point reproduces. At gamma .579149448960 and wrinkle coefficient .362641644309, the six SFs are 1, 1.000183118954, 2.154663914751, 5.055822063463, 1 and 9.423147125824. Faces, core, joints, systems and the five-percent unused-lift allowance close the 4889.442150187-kg budget. Minimum face-strength demand is 282.948186824 MPa; 283 MPa is the retained available input.

All eight subset outcomes reproduce on an independent 4000-step search. Boundary refinement retains gamma plus wrinkling as the least pair under E303/283 MPa/nu .33, reducing usage from .909899005721 to .908635413226. Full-set family mode scores at the filed geometries reproduce; their continuous optima improve slightly.

The material conclusions are conditional. Current S-200F and SR-200 datasheets give typical E=290 GPa. The main E290 sensitivity still floats with two optimisms; the gamma-only SR-200 claim does not survive E290. The guide's S-200F compression is about 255 MPa, not the inherited 283. The cited sheet tests have in-plane nu about .076, whereas the model carries .33. An explicitly limited isotropic sensitivity changes the preferred pair to wrinkling plus strength on aramid. Those observations are NFI rows, not stops.

Five NFI rows cover changed filing pins, modulus, Poisson ratio, strength/product form, and the scope of “strongest sourced Be.” RESULTS.json and float021.py no longer matched the original report's byte pins when checked; the original CARD and inputs did match and are snapshotted. No owner program was executed or imported. CHECK.md contains exact comparisons, formulas and 20 passing checks; SOURCE-AUDIT.md gives the primary source readings.

The report goes once to sciences, cc co, xo and admiral-robotics-review-v2. The next queue order is ord-admiral-rr2-check021b-after-021-codex-1020; begin that independent check after this filing.
"""
(ROOT / "CARD.md").write_text(card)
print(json.dumps({"ended_at": ended, "nfi_rows": len(nfi), "validation_passes": len(extra["validation"]),
                  "sheet_gamma_only_E290_usage": sheet_gamma_usage}, indent=2))
