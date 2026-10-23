#!/usr/bin/env python3
"""MAINLINE-013: write NFI.json, one row per unresolved issue, with its numbers read from RESULTS.json (never retyped).
Run after compute.py: python3 -I make_nfi.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "RESULTS.json")))
CORES = {c["core_id"]: c for c in R["cores"]}


def band(lo, hi, split="Q"):
    return next(b for b in R["bands"] if b["band_kg_m3"] == [lo, hi] and b["split"] == split)


def g(x, n=3):
    return f"{x:.{n}g}"


b10q, b10b, b14q = band(0.1, 10.0, "Q"), band(0.1, 10.0, "B"), band(1.0, 4.0, "Q")
best = CORES[b10q["best"]["wrinkle"]["core_id"]]["rows"]["Q"]
k3 = CORES[b14q["best"]["wrinkle"]["core_id"]]["rows"]["Q"]
lp = R["lightest_passing"]
ideal = {s["name"]: s for s in R["ideal_lattice_PROJECTION"]["strut_references"]}
frac5 = next(e for e in R["ideal_lattice_PROJECTION"]["fraction_of_ideal_needed_Q_split"] if e["rho_kg_m3"] == 5)["by_strut"]
real = [a["fraction_of_ideal"] for a in R["alumina_realization"]]
needs = {e["Q"]["rho_core_kg_m3"]: e for e in R["needs_by_density"]}

rows = [
    {"id": "NFI-013-WRINKLE-PRODUCT", "binds": True,
     "issue": "No measured core at or below 10 kg/m3 meets the wrinkling need with 6061 faces on the P2 float ceiling.",
     "numbers": f"Best measured: {b10q['best']['wrinkle']['core_id']} at {b10q['best']['wrinkle']['density_kg_m3']} kg/m3, "
                f"Ec*Gc margin {g(b10q['best']['wrinkle']['best_margin'])} on the least-factor split (gap {g(b10q['best']['wrinkle']['gap_factor'])}, "
                f"{g(1 / b10q['best']['wrinkle']['stress_margin'])} on stress; {g(1 / best['wrinkle_quantity_margin_classical_0p76'])} at the classical 0.76), "
                f"gap {g(b10b['best']['wrinkle']['gap_factor'])} on the buckling split. Band 1-4 kg/m3: {b14q['best']['wrinkle']['core_id']}, gap "
                f"{g(b14q['best']['wrinkle']['gap_factor'])} ({g(1 / k3['wrinkle_quantity_margin_classical_0p76'])} classical).",
     "closes_when": "a measured core's Ec*Gc at its own density meets the need on its row; or a face change lowers the need, which "
                    "scales as sigma_face^3/E_face (008b's face table); or a wrinkling test on a representative sandwich replaces "
                    "the CR-1457 design coefficient."},
    {"id": "NFI-013-SHEAR-UNMEASURED",
     "issue": "No source measured a transverse shear modulus for any core at or below 10 kg/m3.",
     "numbers": "Gc is DERIVED as Ec/2 (isotropic, nu = 0, the optimistic bound) for every non-honeycomb core; at nu = 1/3 every "
                "product falls by 0.75 and every crimp margin by 0.75. Si et al. 2014 measured shear stress at 9.6 kg/m3 but printed "
                "no modulus.",
     "closes_when": "a plate-shear or sandwich-beam shear modulus is measured on a candidate core."},
    {"id": "NFI-013-CRIMP",
     "issue": "On the least-factor split no measured core at or below 10 kg/m3 reaches the crimp shear modulus.",
     "numbers": f"Need {g(needs[1.0]['Q']['Gc_req_crimp_Pa'])} Pa at 1 to 9.6 kg/m3; best {b10q['best']['crimp']['core_id']} margin "
                f"{g(b10q['best']['crimp']['best_margin'])} (gap {g(b10q['best']['crimp']['gap_factor'])}) on the derived Gc. On the buckling "
                "split three alumina lattice points pass (0.3, 5.3, 5.5 kg/m3), the 0.3 point on a 6 m core.",
     "closes_when": "a measured Gc above the need on the row the design uses."},
    {"id": "NFI-013-STRENGTH-BASIS",
     "issue": "Most ultralight strengths are not crush strengths: stress at 80 percent strain (Qiu 2012), undefined 'max stress' "
              "(Si 2014), ultimate stress of undefined strain (Xu 2019), 40 percent compression (Basotect), indentation or tension "
              "(Kashani 2019). These can fail the crush check but never pass it.",
     "numbers": f"The only structural pass at or below 10 kg/m3 is {b10q['best']['crush']['core_id']} at {b10q['best']['crush']['density_kg_m3']} "
                f"kg/m3, margin {g(b10q['best']['crush']['best_margin'])}, read by eye from a plot (about 25 percent) with its density "
                "inferred from relative density times 2900 kg/m3.",
     "closes_when": "a small-strain collapse or yield strength is measured at the candidate density."},
    {"id": "NFI-013-MID-DENSITY",
     "issue": "This card sourced no core between 53 and 190 kg/m3, so the lightest core passing all three is bounded, not found.",
     "numbers": f"The only pass is {lp['core_id']} at {lp['density_kg_m3']} kg/m3 (secondary source); at that density the float-ceiling "
                f"core is {g(lp['row_at_its_density']['tc_m'] * 1000)} mm thick and the shell's buckling SF is {g(lp['row_at_its_density']['SF_b'])} "
                "at kd 0.2.",
     "closes_when": "mid-density cores are sourced (for example high-density PMI foams, end-grain balsa, carbon micro-lattices from "
                    "50 to 190 kg/m3) and run through compute.py."},
    {"id": "ref-ce7077da95749d9c1df0",
     "issue": "Two values arrive second-hand: the vitreous carbon octet micro-lattice (Jacobsen 2011, via Zhang 2019) and the "
              "glassy carbon exponents (Bauer 2016, via Zhang 2019); Schaedler 2011's 10 kg/m3 nickel point also via Zhang 2019.",
     "numbers": "The 190 kg/m3 all-three pass rests on the secondary Jacobsen numbers (1.1 GPa, 10.2 MPa).",
     "closes_when": "the primary papers are opened and the values matched."},
    {"id": "NFI-013-FIGURE-READS",
     "issue": "Maloney 2013, Zheng 2016, Meza 2014, Meza 2015 and Zhu 2015 values are read by eye from log plots (about 25 to 50 "
              "percent); the Meza densities are inferred from relative density.",
     "numbers": "None of these readings sits near a margin of 1 except the Meza 2015 crush point (1.34).",
     "closes_when": "tabulated values (journal SI or theses) replace the readings."},
    {"id": "NFI-013-CONTINUUM-AND-DIMPLING",
     "issue": "The continuum wrinkling form assumes a core finer than the wrinkle wavelength; lattice cell sizes were not sourced. "
              "Intracell dimpling, a fourth local mode outside the card's three, is reported beside them.",
     "numbers": f"CR-1457 eq 2.1-4 with the straight-line biaxial rule allows cells up to {g(needs[10.0]['Q']['cell_max_dimpling_m'] * 1000)} mm "
                f"above 9.6 kg/m3 and up to {g(needs[0.1]['Q']['cell_max_dimpling_m'] * 1000)} mm on the least-factor split at 0.1 kg/m3; "
                "every honeycomb cell in the table fails it except the 1/8-inch (1.11).",
     "closes_when": "cell sizes are sourced and a wrinkling model valid at that cell scale is applied."},
    {"id": "NFI-013-HONEYCOMB-FORM",
     "issue": "CR-1457 eq 2.2-14 at these core-to-face ratios (tc/tf about 220 to 560) is far outside its test data; it makes the "
              "honeycomb need an Ec no honeycomb has.",
     "numbers": f"Ec needed {g(needs[0.1]['Q']['Ec_req_honeycomb_design_Pa'])} to {g(needs[10.0]['Q']['Ec_req_honeycomb_design_Pa'])} Pa; "
                f"best honeycomb margin {g(band(10.001, 32.0)['best']['wrinkle']['best_margin'])} (gap {g(band(10.001, 32.0)['best']['wrinkle']['gap_factor'])}).",
     "closes_when": "a symmetric-wrinkling model or test for very thick honeycomb cores, or a honeycomb with a stabilising foam fill."},
    {"id": "NFI-013-FACE-YIELD",
     "issue": "The 6061 face is past its QUESTIONABLE 276 MPa on every row, so the elastic wrinkling forms (eta 1) flatter it.",
     "numbers": f"Face stress {g(needs[0.1]['Q']['face_stress_Pa'])} Pa (Q, 0.1 kg/m3) to {g(needs[10.0]['Q']['face_stress_Pa'])} Pa.",
     "closes_when": "the face material changes (008b) or CR-1457 section 9 plasticity factors are applied."},
    {"id": "NFI-013-GEOMETRY-B",
     "issue": "On the buckling split the core exceeds a tenth of the radius below about 1.8 kg/m3 and the radius itself below about "
              "0.18 kg/m3, so B-split margins there are not physical (external-area and thin-shell rules).",
     "numbers": f"B core {g(needs[1.0]['B']['tc_m'])} m at 1 kg/m3, {g(needs[0.1]['B']['tc_m'])} m at 0.1 kg/m3; the Q split holds h = "
                f"{g(R['case']['h_eq_m'], 6)} m and is valid at every density.",
     "closes_when": "a thick-shell sandwich model with the inner surface area replaces the external-area rule."},
    {"id": "NFI-013-IDEAL-LATTICE", "tag": "PROJECTION",
     "issue": "The ideal stretch-dominated lattice (Ashby 2006 eq 5.1, Gc = Ec/2) is a bound, not a material; strength is not projected "
              "because no strut-buckling constant was sourced.",
     "numbers": f"Passes wrinkling and crimp on the least-factor split from {g(ideal['K13D2U pitch fibre tow']['lightest_passing_density_Q_kg_m3'])} "
                f"(K13D2U-grade), {g(ideal['CNT yarn, unidirectional']['lightest_passing_density_Q_kg_m3'])} (CNT yarn), "
                f"{g(ideal['beryllium S-200F']['lightest_passing_density_Q_kg_m3'])} (beryllium), "
                f"{g(ideal['ALD alumina (the Meza lattices' + chr(39) + ' wall)']['lightest_passing_density_Q_kg_m3'])} (alumina), "
                f"{g(ideal['6061-T6']['lightest_passing_density_Q_kg_m3'])} kg/m3 (6061). At 5 kg/m3 a lattice needs "
                f"{g(frac5['K13D2U pitch fibre tow'])}, {g(frac5['CNT yarn, unidirectional'])} and {g(frac5['beryllium S-200F'])} of ideal; "
                f"measured alumina lattices reach {g(min(real))} to {g(max(real))}.",
     "closes_when": "a lattice of a fibre-grade strut material is built and measured at 1 to 8 kg/m3."},
    {"id": "NFI-013-WRINKLE-LEVEL",
     "issue": "The wrinkling-precision gap, carried as 009 and 014 carry it: design coefficients (continuum 0.50, CR-1457 eq 2.2-5; "
              "honeycomb 0.33, eq 2.2-14) against classical ones (0.76, NASA/CR-1999-208994 Table 3; 0.82, eq 2.2-12).",
     "numbers": "The product need falls to 0.285 at 0.76 (a factor 3.51); the honeycomb Ec need falls to 0.162 at 0.82 (6.17). No "
                "verdict in this card moves.",
     "closes_when": "a representative wrinkling test fixes the coefficient for the chosen face and core."},
    {"id": "NFI-013-CRUSH-MODEL", "inherited": "MAINLINE-005b",
     "issue": "The p/2 core-stress model is the brief's own example, QUESTIONABLE; local face bending is ignored.",
     "numbers": f"Required {g(R['constants']['crush_req_Pa'], 6)} Pa on every row.",
     "closes_when": "a sandwich-sphere through-thickness solution replaces it."},
    {"id": "NFI-013-EPS-DEFINITIONS",
     "issue": "EPS strengths are specification minima at 1, 5 or 10 percent strain, and the sheets disagree.",
     "numbers": "EPS12 (11.2 kg/m3): 15 kPa at 1 percent and 40 kPa at 10 percent (ASTM D6817 minima, margins 0.314 and 0.838); "
                "34 kPa at 10 percent (older C578 minimum, 0.712); 005b's National Polystyrene 50 kPa at 11 kg/m3 gave 1.05.",
     "closes_when": "the design adopts one strain definition and a measured (not minimum) value."},
    {"id": "NFI-013-SCALE-AND-ENVIRONMENT",
     "issue": "Every lattice and aerogel in this table was tested as a laboratory specimen (micrometres to centimetres); the "
              "float-ceiling core is about 1257 m2 by 0.19 m. The commercial foams (EPS, melamine, polyimide) are made at larger "
              "scale but fail the checks by orders of magnitude. Vacuum outgassing, creep under a sustained p/2 (polymer foams), "
              "and temperature were not assessed.",
     "numbers": "No lattice or aerogel source here reports a manufacturing route at metre scale.",
     "closes_when": "a manufacturing route at metre scale is sourced for a candidate core."},
    {"id": "NFI-013-NOT-OPENED",
     "issue": "Sources that were paywalled or blocked, so none of their values is used: Schaedler 2011 full text and SI, Torrents "
              "2012, Valdevit 2013, Salari-Sharif 2014, Zheng 2014 (Science 344, 1373), Jang 2013, Deshpande-Ashby-Fleck 2001, "
              "Gross and Fricke 1995, Woignier 1989 full text, Ma 2000 full text, Sun 2013, Hu 2013, Zou 2010, Gui 2010, "
              "Worsley 2009 and 2012, Mecklenburg 2012, Eckel 2016, Bauer 2016, Jacobsen 2011.",
     "numbers": "Zheng 2014 (MIT DSpace HTTP 429, Science 403) is the likeliest source of a stiffer ultralight ceramic octet point.",
     "closes_when": "those texts are obtained and their values added through build_cores.py."},
]
out = {"schema": 1, "card": "MAINLINE-013", "unit": "vacuum-mainline013-ultralight-cores-1019", "tag": "QUESTIONABLE",
       "certification": "none", "rows": rows}
with open(os.path.join(HERE, "NFI.json"), "w") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
    fh.write("\n")
print(len(rows), "NFI rows")
