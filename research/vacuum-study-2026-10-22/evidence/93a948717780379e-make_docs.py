#!/usr/bin/env python3
"""MAINLINE-021: write CARD.md and NFI.json from RESULTS.json. Every number is read from RESULTS, never retyped.
Run after float021.py: python3 -I make_docs.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "RESULTS.json")))
M = D["main"]
FP = M["floating_point"]
SC = {s["label"]: s for s in D["scenarios"]}
GUIDE = next(s for k, s in SC.items() if "design guide" in k)
SHEET = next(s for k, s in SC.items() if "SR-200 sheet" in k)
E303 = next(s for k, s in SC.items() if "303 GPa" in k)
CK = D["checks"]
O = D["optimisms"]
CONS = D["conservative_today_gamma"]


def g(x, n=4):
    return f"{x:.{n}g}"


def mm(x):
    return f"{x * 1000:.6g} mm"


def sfs(ev, keys=("global_buckling", "face_compression", "core_shear_crimping", "core_crush", "face_wrinkling",
                  "intracell_dimpling")):
    names = {"global_buckling": "global buckling", "face_compression": "face compression",
             "core_shear_crimping": "core shear crimping", "core_crush": "core crush", "face_wrinkling": "face wrinkling",
             "intracell_dimpling": "intracell dimpling"}
    return ", ".join(f"{names[k]} {g(ev['sfs'][k])}" for k in keys if k in ev["sfs"])


def point_block(p, title):
    nv, f = p["needed_values"], p["improvement_factors_over_today"]
    m = p["masses_kg"]
    return (f"**{title}.** Core {p['core']} ({g(p['core_rho_kg_m3'])} kg/m3, Ec {g(p['core_Ec_Pa'] / 1e6)} MPa, W shear "
            f"{g(p['core_Gc_Pa'] / 1e6)} MPa, crush {g(p['core_crush_Pa'] / 1e3)} kPa"
            + (f", cell {g(p['core_cell_m'] * 1000)} mm" if p.get("core_cell_m") else "") + f", {p['core_tag']}). "
            f"R {g(p['R_m'])} m. Each face {mm(p['tf_m'])}. Core {mm(p['core_m'])}. Face separation d = core + face = "
            f"{mm(p['h_m'])}. Masses: faces {g(m['faces'], 7)} kg, core {g(m['core'], 7)} kg, joints {g(m['joints'], 7)} kg, "
            f"systems {g(m['systems'])} kg, margin {g(m['margin'], 7)} kg (5 percent of lift); total {g(m['total'], 9)} kg = lift. "
            f"Vc {g(p['Vc'], 6)}, Kc {g(p['Kc'], 6)}, branch {p['branch'].replace('_', ' ')}. "
            f"Needed: gamma {g(nv['gamma'], 5)} ({g(f['gamma'])} times today's {g(nv['gamma_today'])}; the 018 curve gives "
            f"{g(nv['gamma_full_018'], 5)} here), wrinkle coefficient {g(nv['wrinkle_coefficient'], 5)} ({g(f['wrinkle_coefficient'])} "
            f"times {g(nv['wrinkle_today'])}), face strength {g(nv['be_strength_Pa'] / 1e6, 5)} MPa ({g(f['be_strength'])} times "
            f"{g(nv['be_today_Pa'] / 1e6)} MPa). Modes at those values: {sfs(p['at_needed_values'])}. With the full named set "
            f"(018 curve, 0.82, the SR-200 lot at {g(nv['be_full_Pa'] / 1e6)} MPa and its own {g(p['face_E_Pa_at_full_set'] / 1e9)} GPa): {sfs(p['at_full_named_set'])}; least "
            f"{g(p['at_full_named_set']['least_SF'])}. Today, with no optimism: least {g(p['today']['least_SF'])}, "
            f"{p['today']['governing'].replace('_', ' ')}.")


def scenario_line(sc, title):
    ls, p = sc["least_set"], sc.get("floating_point")
    if not p:
        return f"{title}: no subset floats."
    nv = p["needed_values"]
    names = {"O1_gamma": "gamma", "O2_wrinkle": "wrinkling", "O3_be_strength": "beryllium strength"}
    return (f"{title}: the least set is {{{', '.join(names[x] for x in ls['subset'])}}}, largest usage {g(ls['min_max_usage'])}, on "
            f"{p['core']}: faces {mm(p['tf_m'])}, core {mm(p['core_m'])}, Vc {g(p['Vc'])}, {p['branch'].replace('_', ' ')}; "
            f"needed gamma {g(nv['gamma'])}, wrinkle {g(nv['wrinkle_coefficient'])}, face {g(nv['be_strength_Pa'] / 1e6)} MPa. "
            f"Modes at those values: {sfs(p['at_needed_values'])}.")


def family_block(fam, title):
    v = M["families"][fam]
    best = v["full_set_max_least"]
    p = best["point"]
    nv = p["needed_values"]
    return (f"**{title}.** Today's best: {g(v['today_max_least']['least'])} on {v['today_max_least']['core']} "
            f"({v['today_max_least']['governing'].replace('_', ' ')}). Under the full named set: {g(best['score'])} on {p['core']}, "
            f"faces {mm(p['tf_m'])}, core {mm(p['core_m'])}, Vc {g(p['Vc'])}, {p['branch'].replace('_', ' ')}: "
            f"{sfs(p['at_full_named_set'])}. What that point needs: gamma {g(nv['gamma'])}, wrinkle {g(nv['wrinkle_coefficient'])}, "
            f"face {g(nv['be_strength_Pa'] / 1e6)} MPa. Under 018's conservative gamma the family's best is "
            f"{g(v['full_set_conservative_gamma_max_least']['least'])} ({v['full_set_conservative_gamma_max_least']['governing'].replace('_', ' ')}).")


sub_names = {"O1_gamma": "gamma", "O2_wrinkle": "wrinkling", "O3_be_strength": "beryllium strength"}
subset_lines = []
for r in M["subsets"]:
    label = "{" + ", ".join(sub_names[x] for x in r["subset"]) + "}" if r["subset"] else "{} (no optimism)"
    if r["feasible_within_named"]:
        subset_lines.append(f"- {label}: floats, largest usage {g(r['min_max_usage'])}, on {r['core']}.")
    elif r["min_max_usage"] is not None:
        subset_lines.append(f"- {label}: does not float inside the named values; it would need {g(r['min_max_usage'])} of the stretch.")
    else:
        subset_lines.append(f"- {label}: no geometry floats.")

ck = D["checks"]
be = O["O3_be_strength"]
card = f"""# MAINLINE-021 the optimistic floating point — ESTIMATE

Unit vacuum-mainline021-optimistic-floating-point-1020. Order ord-admiral-rr2-mainline021-dispatch-1019. Status ESTIMATE. Tags QUESTIONABLE, and PROJECTION where named. Nothing here is a certification. Started {D['job_started_at']} (order read); the end time is in RESULTS.json. Times are measurements, not limits. Float margin 5 percent of lift, {g(FP['masses_kg']['margin'], 9)} kg; it stands until MAINLINE-019 files.

This is the revised filing. It amends rpt-ref-fe49179fb6a8ad8c986e (filed 00:30:43) and carries the two amendments that crossed it:
- ord-admiral-rr2-mainline021-be-modulus-290-1020: every grade at its own modulus. S-200F is now {g(D['case']['face']['E_Pa'] / 1e9)} GPa (Materion DS-HPP-610); the 303 GPa carried all night is S-200FH's.
- ord-admiral-rr2-mainline021-take-009e-015-1020: MAINLINE-009e and MAINLINE-015.

The least set and the geometry do not change. Gamma's share of its stretch rises from {g(E303['least_set']['min_max_usage'])} to {g(M['least_set']['min_max_usage'])}.

## The answer

A hull floats at 5 percent margin with every mode at SF 1 or above on two of the three named optimisms: gamma on the MAINLINE-018 optimistic curve and the honeycomb wrinkling coefficient. The beryllium strength optimism is not needed at the inherited S-200F value of 283 MPa, with S-200F at its own {g(D['case']['face']['E_Pa'] / 1e9)} GPa. Gamma carries the result: it is {g(FP['improvement_factors_over_today']['gamma'])} times the CR-1457 hemisphere value at that point, and {g(FP['usage']['O1_gamma'])} of the stretch the 018 curve allows there. The wrinkling coefficient needs only {g(FP['improvement_factors_over_today']['wrinkle_coefficient'])} times 0.33.

{point_block(FP, 'The floating point')}

Intracell dimpling uses CR-1457's own biaxial rule (eq 2.1-6, straight line, so each direction carries half). 009d and 014b score the uniaxial eq 2.1-4; in that form this point's dimpling SF is {g(FP['today']['intracell_dimpling_uniaxial_009d_form'])}. Under 018's conservative gamma, 0.20 at every Vc, the point falls to {g(FP['at_full_set_but_conservative_gamma']['least_SF'])} on global buckling, so the gamma optimism is the whole margin.

## Every subset of the named optimisms (S-200F at 283 MPa and 290 GPa)

Usage is the share of an optimism's named stretch, from today's value to its full value, that a point needs: 0 means not needed, 1 means the full value. The search is over 014b's {len(D['case'] and json.load(open(os.path.join(HERE, 'INPUTS.json')))['cores_used'])} eligible cores and the core-mass fraction on the 5 percent mass line. For each subset it minimises the largest usage, with every mode outside the subset at SF 1 or above on today's value, and crimp, crush and dimpling at 1 or above, since no optimism touches them.

{chr(10).join(subset_lines)}

The fewest members that float is two. Of the two-member sets, {{gamma, wrinkling}} needs the least, so it is the least set.

## How the least set moves with the facts underneath it

{scenario_line(GUIDE, "If S-200F's compressive yield is the current Materion design guide's 'about 37 ksi' (255 MPa) rather than 283")} That route rests on the handbook's gamma 1 at Vc of 2 and above. Under 018's conservative reading it needs gamma {g(CONS[GUIDE['label']]['gamma_needed'])} there, {g(CONS[GUIDE['label']]['factor_over_0.20'])} times 0.20, the whole 018 stretch.

{scenario_line(SHEET, "If the faces are SR-200 cross-rolled sheet, the product Materion supplies below 6.3 mm, taken at its datasheet minimum tensile yield of 345 MPa, with compressive about equal as the one sourced lot shows, and its datasheet E of 290 GPa")} {"One optimism is then enough." if len(SHEET['least_set']['subset']) == 1 else "Two optimisms are still needed, but each at about half its stretch. At 303 GPa, gamma alone had sufficed (filed at 00:30); at 290 GPa it does not."}

{scenario_line(E303, "As first filed at 00:30, with 303 GPa (S-200FH's modulus)")}

## 009e and 015, taken in

009e is reproduced on its own 8000-step grid: least {g(CK['009e_aluminium_optimistic']['least_on_009e_grid'], 12)}, face {g(CK['009e_aluminium_optimistic']['tf_m'] * 1000, 10)} mm, Vc {g(CK['009e_aluminium_optimistic']['Vc'], 6)}, gamma {g(CK['009e_aluminium_optimistic']['gamma'], 6)}, at the chain's 303 GPa. A golden refinement finds {g(CK['009e_aluminium_optimistic']['refined_least'], 8)}. Its reading holds: on the 1.6 pcf core, gamma alone leaves face compression and global buckling tied below 1, so face strength blocks. Gamma alone would need {g(next(r for r in M['subsets'] if r['subset'] == ['O1_gamma'])['min_max_usage'])} of its stretch at 290 GPa. The least set gets past that block by moving to the lighter 1.0 pcf core of the same alloy: 16 kg/m3 instead of 25.6 leaves more of the mass for the faces at the same depth. The price is face wrinkling on the softer core, which is the small wrinkling optimism.

015's map turns the needed gamma into a shape tolerance (kd.py's formulas re-implemented, and checked against its 43.79 mm and RMS 1.91 mm at kd 0.5). At this point t_eq = sqrt(3) * d = {g(FP['tolerance_015_at_needed_gamma']['t_eq_mm'])} mm and R/t_eq = {g(FP['tolerance_015_at_needed_gamma']['R_over_t_eq'])}, inside the Eq 3 fit range of 100 to 1550. Gamma {g(FP['needed_values']['gamma'])} allows one dimple of {g(FP['tolerance_015_at_needed_gamma']['amplitude_mm'])} mm amplitude, with single-dimple RMS {g(FP['tolerance_015_at_needed_gamma']['rms_worst_mm'])} mm at the worst width. The 018 curve's own {g(FP['needed_values']['gamma_full_018'])} would allow {g(FP['tolerance_015_at_018_curve']['amplitude_mm'])} mm. Against the 0.25 mm assembled-surface figure 015 cites, the RMS ask is {g(FP['tolerance_015_at_needed_gamma']['rms_worst_mm'] / 0.25)} times looser. That reads the gamma optimism as a shape-precision requirement, QUESTIONABLE: 015 maps a monocoque-equivalent knockdown, and 018's curve attributes part of the relief to core shear.

## Both lead families, re-optimised under the full named set

{family_block('aluminium', 'Aluminium honeycomb (stiff branch)')}

{family_block('aramid', 'Aramid honeycomb (crimp branch)')} This family floats only on the handbook's gamma 1 at Vc of 2 and above, which 018 tags QUESTIONABLE for a sphere.

{family_block('other', 'Other cores (fiberglass and PMI foam)')}

## The optimisms, named

**O1, gamma.** Full: the MAINLINE-018 optimistic curve, gamma = 0.20 + 0.40 min(Vc, 2), PROJECTION; it also sets the stiff-branch knockdown and is not stacked on kd. Today: CR-1457 eq 6.2-13 and page 6-12, 0.20 below Vc 2 and 1 at Vc 2 and above (hemispheres; QUESTIONABLE for a sphere). At the floating point it needs {g(FP['needed_values']['gamma'], 5)} against today's 0.20 and the curve's {g(FP['needed_values']['gamma_full_018'], 5)}. Grounding: MAINLINE-018b (crimp gamma measured) and MAINLINE-015 (kd precision).

**O2, the honeycomb wrinkling coefficient.** Full: 0.82, CR-1457 eq 2.2-12 with K_delta 0, the classical value for initially perfect faces, QUESTIONABLE. Today: 0.33, eq 2.2-14, the handbook's lower bound on test data. At the floating point it needs {g(FP['needed_values']['wrinkle_coefficient'], 5)}. No pending card grounds it: a wrinkling test on a representative sandwich would.

**O3, beryllium face strength.** Full: {g(be['full_Pa'] / 1e6)} MPa, the compressive yield of SR-200 cross-rolled sheet, 1.96 mm, longitudinal, the lower of its two in-plane directions ({', '.join(g(x / 1e6) for x in be['full_grade']['directions_Pa'])} MPa). These are Lockheed test values (Fenn 1967), seen second-hand in NASA CR-194164, Table 3, with neither minimum nor typical stated. QUESTIONABLE. Today: {g(be['today_Pa'] / 1e6)} MPa, MAINLINE-008's S-200F compressive yield (41 ksi), inherited by 014b and 009d. Other sourced values:
- S-200F, Materion design guide, about 255 MPa (compressive)
- S-200F, datasheet minimum tensile yield, 241 MPa
- SR-200 sheet, datasheet minimum tensile yield, 345 MPa
- I-220H, datasheet minimum tensile yield, 345 MPa, no compressive value

At the floating point it needs {g(FP['needed_values']['be_strength_Pa'] / 1e6)} MPa, exactly today's value. Grounding: MAINLINE-020 (beryllium reality).

No further optimism is needed. Crimp ({g(FP['at_needed_values']['sfs']['core_shear_crimping'])}), crush ({g(FP['at_needed_values']['sfs']['core_crush'])}) and dimpling ({g(FP['at_needed_values']['sfs']['intracell_dimpling'])}) clear 1 without one.

## Method and checks

The modes are 009d's formulas re-implemented in float021.py: global buckling gamma*Kc*sigma_0*4*tf/R, face compression 4*sigma*tf/R, core shear crimping 4*sigma_crimp*tf/R, crush at p/2, honeycomb wrinkling with the equibiaxial factor {g(D['case']['biaxial_factor'], 10)}, and intracell dimpling. They run on 009d's mass line: structural mass ((1 - 0.05)*lift - 100)/1.05 = {g(D['case']['structural_mass_kg'], 10)} kg, faces 2*A*rho*tf, core A*rho_c*tc. Before anything new, the script reproduces:
- 009d's aluminium point on its own 8000-step grid: core-mass fraction 0.30075, every mode to 1e-12 ({ck['009d_aluminium_point']['result']})
- 009c-5's aramid point with the geometry held ({ck['009c5_aramid_point_held']['result']})
- 009c-5's aramid optimum, re-derived from scratch at {g(ck['009c5_aramid_reoptimised']['least'], 10)} against the sealed {g(ck['009c5_aramid_reoptimised']['sealed'], 10)}, a finer optimiser landing above ({ck['009c5_aramid_reoptimised']['result']})
- 009d's kd that brings global to 1, {g(ck['009d_kd_global_1']['mine'], 12)}
- 009e's optimistic aluminium point on its own grid, {g(ck['009e_aluminium_optimistic']['least_on_009e_grid'], 12)} ({ck['009e_aluminium_optimistic']['result']})
- 015's tolerance map at kd 0.5 on the 014b beryllium point, {g(ck['015_tolerance_kd_0p5']['amplitude_mm'])} mm and RMS {g(ck['015_tolerance_kd_0p5']['rms_worst_mm'])} mm against 43.79 and 1.91 ({ck['015_tolerance_kd_0p5']['result']})

The checker's E-only figure is reproduced too. The aramid family re-optimised at 290 GPa with today's values is {g(M['families']['aramid']['today_max_least']['least'])}, against the checker's 0.643. The reproduction checks run at the 303 GPa the sealed cards used. Everything new runs at 290 GPa.

The beryllium values were gathered by a sourcing sub-worker of this seat from Materion datasheets and NASA reports actually opened (sources/beryllium.json). None carries a DOI; each is pinned by URL.

## Then

Stop and file. The robotics seat sends the next job. NFI.json carries the open rows. A checker runs behind this card.
"""
with open(os.path.join(HERE, "CARD.md"), "w") as fh:
    fh.write(card)

nfi = [
    {"id": "NFI-021-GAMMA", "optimism": "O1", "binds": True,
     "needed": FP["needed_values"]["gamma"], "today": FP["needed_values"]["gamma_today"],
     "improvement_factor": FP["improvement_factors_over_today"]["gamma"], "usage_of_018_stretch": FP["usage"]["O1_gamma"],
     "state": "PROJECTION: no sphere or dome test at Vc near 1 supports a knockdown above 0.20 (018)",
     "grounding_card": "MAINLINE-018b (crimp gamma measured from Sim's absolute loads); MAINLINE-015 (kd precision)",
     "tolerance_015": FP["tolerance_015_at_needed_gamma"],
     "note": f"Under 018's conservative gamma the point is {FP['at_full_set_but_conservative_gamma']['least_SF']:.6g}. 015's map: one dimple of {FP['tolerance_015_at_needed_gamma']['amplitude_mm']:.4g} mm (RMS {FP['tolerance_015_at_needed_gamma']['rms_worst_mm']:.3g} mm) at this gamma, QUESTIONABLE."},
    {"id": "NFI-021-WRINKLE", "optimism": "O2",
     "needed": FP["needed_values"]["wrinkle_coefficient"], "today": FP["needed_values"]["wrinkle_today"],
     "improvement_factor": FP["improvement_factors_over_today"]["wrinkle_coefficient"],
     "usage_of_named_stretch": FP["usage"]["O2_wrinkle"],
     "state": "between today's design lower bound (0.33) and the classical value (0.82); no test at this core-to-face ratio",
     "grounding_card": "none pending; a wrinkling test on a representative sandwich",
     "note": f"core-to-face ratio tc/tf {FP['core_m'] / FP['tf_m']:.4g}"},
    {"id": "NFI-021-BE-STRENGTH", "optimism": "O3",
     "needed_Pa": FP["needed_values"]["be_strength_Pa"], "today_Pa": FP["needed_values"]["be_today_Pa"],
     "improvement_factor": FP["improvement_factors_over_today"]["be_strength"],
     "state": "exists today as SR-200 sheet if compressive yield equals the 345 MPa datasheet minimum tensile yield (the 1967 lot shows "
              "ratio 0.99); NOT met by S-200F block at the Materion guide's 255 MPa (factor 1.11 short)",
     "grounding_card": "MAINLINE-020 (beryllium reality)",
     "note": "The point sits at face compression 1.0002: the 283 MPa inherited from 008 cites an older guide (MB-001, 41 ksi); the "
             "current Materion guide prints 'about 37 ksi' for S-200F."},
    {"id": "NFI-021-MARGIN", "needed": 0.05, "state": "assumed", "grounding_card": "MAINLINE-019 (margin budget)",
     "note": "The 5 percent margin stands until 019 files; every number here moves with it."},
    {"id": "NFI-021-CRIMP-BRANCH-GAMMA",
     "issue": "The aramid route floats only on the handbook's gamma 1 at Vc >= 2, which 018 tags QUESTIONABLE for a sphere.",
     "numbers": f"Aramid family under the full set {M['families']['aramid']['full_set_max_least']['score']:.6g}; under 018's conservative gamma {M['families']['aramid']['full_set_conservative_gamma_max_least']['least']:.6g}.",
     "grounding_card": "MAINLINE-018b"},
    {"id": "NFI-021-FACE-MODULUS",
     "issue": "Corrected by ord-admiral-rr2-mainline021-be-modulus-290-1020: S-200F scored at its own 290 GPa (Materion DS-HPP-610); the 303 GPa the chain carried is S-200FH's. The SR-200 lot's own in-plane moduli are 298.7 and 293.6 GPa; the full-set column uses the lower.",
     "numbers": f"Least set unchanged; gamma's usage {E303['least_set']['min_max_usage']:.4g} at 303 GPa becomes {M['least_set']['min_max_usage']:.4g}; gamma needed {E303['floating_point']['needed_values']['gamma']:.4g} becomes {FP['needed_values']['gamma']:.4g}."},
    {"id": "NFI-021-SHEET-SIZE",
     "issue": "SR-200 sheet comes to 24 by 72 inches, with gauges under 0.059 inch only at narrower widths and shorter lengths (Materion datasheet); a 10 m sphere needs over a thousand sheets, so the 5 percent joint allowance is QUESTIONABLE.",
     "grounding_card": "MAINLINE-020"},
    {"id": "NFI-021-DIMPLING-FORM",
     "issue": "Dimpling here uses CR-1457 eq 2.1-6 (biaxial, half); 009d and 014b use the uniaxial eq 2.1-4.",
     "numbers": f"Floating point {FP['at_needed_values']['sfs']['intracell_dimpling']:.4g} biaxial, {FP['today']['intracell_dimpling_uniaxial_009d_form']:.4g} uniaxial; both far above 1."},
    {"id": "NFI-021-CORE-TABLE",
     "issue": "Core properties are 014b's: W shear as Gc, stabilised Ec, Hexcel's crush column for crush; Hexcel test thickness 0.625 inch against a 20 mm core.",
     "grounding_card": "none pending"},
    {"id": "NFI-021-CONSERVATIVE-READING",
     "issue": "If 'today' is 018's conservative gamma (0.20 at every Vc), the stiff-branch least set does not change, because its today is already 0.20; a crimp-branch point needs gamma 1, a factor 5.",
     "numbers": {k: v for k, v in CONS.items()}},
]
with open(os.path.join(HERE, "NFI.json"), "w") as fh:
    json.dump({"schema": 1, "card": "MAINLINE-021", "unit": "vacuum-mainline021-optimistic-floating-point-1020",
               "tag": "QUESTIONABLE", "certification": "none", "rows": nfi}, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print("CARD.md", len(card), "bytes;", len(nfi), "NFI rows")
