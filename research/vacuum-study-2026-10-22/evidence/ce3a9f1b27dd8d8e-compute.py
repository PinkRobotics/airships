#!/usr/bin/env python3
"""MAINLINE-008 material gap table. Own arithmetic from pinned 002/003 RESULTS.

At equal face mass tf_new = tf_Al * rho_Al / rho_new (core, separation d, joints,
systems held at each row's pinned values). To first order, since tf << d in
every row (tf/d <= 0.0034 for aluminium, <= 0.0062 for the lightest candidate):
  SF_b = SF_b,Al * (E/rho)/(E/rho)_Al      [p_b ~ tf*(d+tf)*E ~ tf*d*E]
  SF_y = SF_y,Al * (sigma_c/rho)/(sigma_c/rho)_Al  [p_y = 4*sigma_c*tf/R]
  gap  = 1/min(SF_b, SF_y)
All buckling SFs carry kd=0.2 from the pinned rows and scale linearly with kd
(p_b ~ kd); MAINLINE-004 replaces kd by one multiplication per row.
"""
import hashlib, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]  # workspace root (outputs/<unit>/file -> up: outputs, work, .ship, root is 4? fixed below)
# __file__ = <ws>/.ship/work/outputs/<unit>/compute.py ; workspace = parents[4]
WS = pathlib.Path(__file__).resolve().parents[4]
OUT = pathlib.Path(__file__).resolve().parent
STARTED = "2026-10-19T22:42:07-07:00"

PIN_BASE = "unpublished-local-ref:768b7b34f9cac6c4"
XO_REVIEW = "evidence/dcfa7ae3942a9e4f-UNA600-MAINLINE003-REVIEW.md"
BRIEF_DIR = "unpublished-local-ref:792ada9d1fcd5e54"
PROGRESS_DIR = "unpublished-local-ref:b6b93a5170dc3dc2"

def pin(path):
    b = pathlib.Path(path).read_bytes()
    return {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

r002 = json.loads(pathlib.Path(f"{PIN_BASE}/vacuum-mainline002-strength-owner1200-1019/RESULTS.json").read_text())
r003 = json.loads(pathlib.Path(f"{PIN_BASE}/vacuum-mainline003-p2-targets-owner1200-1019/RESULTS.json").read_text())

# P2 rows: point_id -> (SF_b_Al, SF_y_Al, tf_Al_m, d_m)
ROWS = {}
for row in r002["rows"]:
    if row["point_id"] == "P2-A":
        ROWS["P2-A"] = {"SF_b_Al": row["crush_safety_factor"], "SF_y_Al": row["factors"]["aluminum_yield"]["pressure_Pa"] and (row["limits_Pa"]["aluminum_yield"] / row["external_pressure_Pa"]),
                        "tf_Al_m": row["extra"]["tf_m"], "d_m": row["extra"]["d_m"], "source": "MAINLINE-002 RESULTS P2-A"}
for row in r003["rows"]:
    ROWS[row["point_id"]] = {"SF_b_Al": row["buckling_SF"], "SF_y_Al": row["strength_SF_QUESTIONABLE"],
                             "tf_Al_m": row["geometry"]["tf_m"], "d_m": row["geometry"]["d_m"], "source": f"MAINLINE-003 RESULTS {row['point_id']}"}
ROW_ORDER = ["P2-A", "P2-C", "P2-K", "P2-E"]
P_EXT = 95460.83791390515

AL = {"rho": 2700.0, "E_GPa": 68.9, "sigma_c_MPa": 276.0}
AL_E_RHO = AL["E_GPa"] * 1e9 / AL["rho"]      # Pa/(kg/m3) = J/kg
AL_S_RHO = AL["sigma_c_MPa"] * 1e6 / AL["rho"]

# rho kg/m3, E GPa, sigma_c MPa. tag QUESTIONABLE unless PROJECTION.
# sigma_c_basis states whether the value is a measured compressive value or a
# tensile yield transferred to compression; composites are QI laminate values.
CANDIDATES = [
 {"name": "6061-T6 (baseline)", "rho": 2700, "E_GPa": 68.9, "sigma_c_MPa": 276, "tag": "QUESTIONABLE",
  "sigma_c_basis": "typical tensile yield transferred to compression, per pinned COMMON.md",
  "source": "Pinned COMMON.md (MAINLINE-001/002); ASM MatWeb 6061-T6 data sheet (AA typical values)"},
 {"name": "7075-T6", "rho": 2810, "E_GPa": 71.7, "sigma_c_MPa": 503, "tag": "QUESTIONABLE",
  "sigma_c_basis": "tensile yield transferred to compression; no compressive yield retrieved",
  "source": "ASM MatWeb 7075-T6 data sheet; density 2.81 g/cc, E 71.7 GPa, tensile yield 503 MPa"},
 {"name": "Al-Li 2195-T8", "rho": 2710, "E_GPa": 76.0, "sigma_c_MPa": 560, "tag": "QUESTIONABLE",
  "sigma_c_basis": "tensile yield (L direction) transferred to compression",
  "source": "MatWeb 2195 composition/density sheet https://www.matweb.com/search/datasheet_print.aspx?matguid=4363dafc7f5545688506d8b4af1e9468 ; MakeItFrom 2195-T8 https://www.makeitfrom.com/compare/2195-2195-T8-Aluminum/B390.0-B390.0-F-SC174B-A23900-Cast-Aluminum (E 76 GPa, yield 560 MPa)"},
 {"name": "Ti-6Al-4V (annealed)", "rho": 4430, "E_GPa": 113.8, "sigma_c_MPa": 970, "tag": "QUESTIONABLE",
  "sigma_c_basis": "compressive yield, typical annealed value",
  "source": "ASM MatWeb Ti-6Al-4V annealed data sheet (density 4.43 g/cc, E 113.8 GPa, compressive yield 970 MPa)"},
 {"name": "Mg AZ31B", "rho": 1770, "E_GPa": 45.0, "sigma_c_MPa": 97, "tag": "QUESTIONABLE",
  "sigma_c_basis": "compressive yield 97 MPa (rolled/extruded AZ31; tension-compression asymmetry retained, tensile yield not used)",
  "source": "AZ31 property table in https://zenodo.org/records/5519242/files/E27900610521.pdf (compressive yield 97 MPa); density 1.77 g/cc, E 45 GPa (ASM MatWeb AZ31B)"},
 {"name": "Beryllium S-200F", "rho": 1850, "E_GPa": 303.0, "sigma_c_MPa": 283, "tag": "QUESTIONABLE",
  "sigma_c_basis": "compressive yield 41 ksi = 283 MPa (tensile yield 37 ksi on the same page)",
  "source": "Materion beryllium data sheet https://hkvxni.files.cmp.optimizely.com/download/c3141b9ea04211ee9a7b2a5d2cb825d4 (S-200F density 1.85 g/cc, E 303 GPa); Brush/Materion Beryllium Guide MB-001 compressive-yield note"},
 {"name": "AlBeMet 162 (AM162, HIP)", "rho": 2071, "E_GPa": 193.0, "sigma_c_MPa": 193, "tag": "QUESTIONABLE",
  "sigma_c_basis": "HIP tensile yield transferred to compression",
  "source": "Materion AlBeMet technical data sheet https://web.archive.org/web/20171024043552/https://materion.com/[private path] (density 2.071 g/cc, E 193 GPa, HIP yield 193 MPa)"},
 {"name": "CFRP quasi-isotropic T700/epoxy", "rho": 1550, "E_GPa": 54.0, "sigma_c_MPa": 520, "tag": "QUESTIONABLE",
  "sigma_c_basis": "QI laminate estimate: E_QI ~ 0.40 x UD composite E (134 GPa, Toray T700S composite), sigma_c_QI ~ 0.33 x UD compressive strength; not fibre properties",
  "source": "Toray T700S data sheet https://www.rockwestcomposites.com/downloads/T700SDataSheet.pdf (fibre 230 GPa, 1.80 g/cc; composite tensile modulus 134 GPa); QI reduction stated in sigma_c_basis"},
 {"name": "CFRP quasi-isotropic M55J/epoxy", "rho": 1640, "E_GPa": 135.0, "sigma_c_MPa": 350, "tag": "QUESTIONABLE",
  "sigma_c_basis": "QI laminate estimate: UD E ~ 325 GPa (Vf 0.6 rule of mixtures on 540 GPa fibre), E_QI ~ 0.42 x UD; sigma_c_QI ~ 0.35 x estimated UD compressive strength; not fibre properties",
  "source": "Toray M55J data sheet https://www.toraycma.com/wp-content/uploads/M55J-Technical-Data-Sheet-1.pdf.pdf (fibre 540 GPa, 1.93 g/cc in Toray carbon-fibre card); QI reduction stated in sigma_c_basis"},
 {"name": "CFRP quasi-isotropic K13D2U pitch/epoxy", "rho": 1750, "E_GPa": 210.0, "sigma_c_MPa": 220, "tag": "QUESTIONABLE",
  "sigma_c_basis": "QI laminate estimate: UD E ~ 515 GPa (Vf 0.55 rule of mixtures on 935 GPa fibre), E_QI ~ 0.41 x UD; sigma_c_QI low, pitch high-modulus laminates are compression-weak; not fibre properties",
  "source": "Mitsubishi Chemical K13D2U tow data https://www.m-chemical.co.jp/carbon-fiber/en/product/tow/ (935 GPa, 3.70 GPa, 2.20 g/cc); QI reduction stated in sigma_c_basis"},
 {"name": "Boron/epoxy quasi-isotropic", "rho": 2000, "E_GPa": 86.0, "sigma_c_MPa": 850, "tag": "QUESTIONABLE",
  "sigma_c_basis": "QI laminate estimate: E_QI ~ 0.42 x UD E1 (204 GPa); sigma_c_QI ~ 0.34 x UD longitudinal compressive strength (2500 MPa); not fibre properties",
  "source": "Boron fibre review https://www.compositesworld.com/articles/boron-fiber-the-original-high-performance-fiber ; unidirectional boron/epoxy property table (E1 204 GPa, compressive 2500 MPa) in composites textbook extract https://structures.dhu.edu.cn/_upload/article/files/79/64/d90aa6424b14824d25a678e990c0/4ff4b286-e563-4c01-a7f0-ac45163b28a4.pdf"},
 {"name": "SiC (monolithic alpha SiC, Hexoloy SA type)", "rho": 3100, "E_GPa": 410.0, "sigma_c_MPa": 3900, "tag": "QUESTIONABLE",
  "sigma_c_basis": "measured compressive strength of sintered SiC; flexural strength is only ~380 MPa and governs any bending/tension path (NFI)",
  "source": "Saint-Gobain Hexoloy SA data https://www.ceramicsrefractories.saint-gobain.com/pt/files/4731/view (compressive 3900 MPa, flexural 380 MPa); MatWeb alpha SiC https://www.matweb.com/search/datasheet_print.aspx?matguid=dd2598e783ba4457845586b58c8ea9fb (density 3.10 g/cc, E 410 GPa)"},
 {"name": "Metallic glass Vitreloy 1 (Zr41.2Ti13.8Cu12.5Ni10Be22.5)", "rho": 6120, "E_GPa": 96.0, "sigma_c_MPa": 1900, "tag": "QUESTIONABLE",
  "sigma_c_basis": "compressive ultimate strength (bulk metallic glass has no distinct compressive yield; failure is shear-band fracture)",
  "source": "Review of Zr-based bulk metallic glasses https://www.mdpi.com/2075-4701/5/3/1262 (E 70-96 GPa, compressive ultimate 1400-1900 MPa for Vitreloy 1); density 6.12 g/cc typical for Vitreloy 1"},
 {"name": "CNT-yarn composite quasi-isotropic", "rho": 1400, "E_GPa": 180.0, "sigma_c_MPa": 1200, "tag": "PROJECTION",
  "sigma_c_basis": "PROJECTION scenario: QI laminate retaining ~50% of reported UD CNT-laminate specific modulus and a compressive strength below its reported UD tensile specific strength; no such QI structural laminate is available today",
  "source": "PROJECTION from UD CNT-yarn laminate report https://chemrxiv.org/engage/chemrxiv/article-details/639c91d7e8047a61d0eb2d2f (specific modulus 256 GPa per g/cc, specific tensile strength 1.71 GPa per g/cc, unidirectional)"},
 {"name": "Graphene composite quasi-isotropic", "rho": 1500, "E_GPa": 150.0, "sigma_c_MPa": 900, "tag": "PROJECTION",
  "sigma_c_basis": "PROJECTION scenario: graphene-reinforced laminate at a small fraction of monolayer graphene properties (E ~1 TPa); no structural graphene QI laminate is available today",
  "source": "PROJECTION; monolayer basis in Lee et al., Science 2008 (graphene E ~1.0 TPa, DOI 10.1126/science.1157996) and graphene-reinforced carbon fibre https://www.science.org/doi/10.1126/sciadv.aaz4191"},
]

results = []
for c in CANDIDATES:
    e_rho = c["E_GPa"] * 1e9 / c["rho"]
    s_rho = c["sigma_c_MPa"] * 1e6 / c["rho"]
    entry = dict(c)
    entry["E_over_rho_Pa_per_kg_m3"] = e_rho
    entry["sigma_c_over_rho_Pa_per_kg_m3"] = s_rho
    entry["E_over_rho_GPa_per_g_cc"] = c["E_GPa"] / (c["rho"] / 1000.0)
    entry["sigma_c_over_rho_MPa_per_g_cc"] = c["sigma_c_MPa"] / (c["rho"] / 1000.0)
    entry["rows"] = {}
    for pid in ROW_ORDER:
        r = ROWS[pid]
        sf_b = r["SF_b_Al"] * e_rho / AL_E_RHO
        sf_y = r["SF_y_Al"] * s_rho / AL_S_RHO
        least = min(sf_b, sf_y)
        entry["rows"][pid] = {
            "tf_at_equal_face_mass_m": r["tf_Al_m"] * AL["rho"] / c["rho"],
            "tf_over_d": (r["tf_Al_m"] * AL["rho"] / c["rho"]) / r["d_m"],
            "SF_b": sf_b, "SF_y": sf_y, "least_SF": least,
            "gap_1_over_least_SF": 1.0 / least,
            "limiting_figure": "E/rho" if sf_b < sf_y else ("sigma_c/rho" if sf_y < sf_b else "equal"),
            "factor_E_over_rho_for_its_SF1": 1.0 / sf_b,
            "factor_sigma_c_over_rho_for_its_SF1": 1.0 / sf_y,
        }
    results.append(entry)

ranked = sorted(results, key=lambda e: e["rows"]["P2-E"]["least_SF"], reverse=True)
for i, e in enumerate(ranked, 1):
    e["rank_by_least_SF_P2E"] = i

def direction(e):
    r = e["rows"]["P2-E"]
    return {"name": e["name"], "tag": e["tag"], "rank_P2E": e["rank_by_least_SF_P2E"],
            "SF_b_P2E": r["SF_b"], "SF_y_P2E": r["SF_y"], "least_SF_P2E": r["least_SF"],
            "limiting_figure": r["limiting_figure"], "gap": r["gap_1_over_least_SF"],
            "factor_limiting_figure_for_its_mode_SF1": r["gap_1_over_least_SF"],
            "factor_E_over_rho_for_buckling_SF1": r["factor_E_over_rho_for_its_SF1"],
            "factor_sigma_c_over_rho_for_yield_SF1": r["factor_sigma_c_over_rho_for_its_SF1"],
            "note": "gap is the factor for the limiting figure's own mode; if the other mode is also below 1, both figures need their own factors (listed) to meet both modes at once."}

best3_overall = [direction(e) for e in ranked[:3]]
best3_available = [direction(e) for e in ranked if e["tag"] != "PROJECTION"][:3]

checks = {
    "aluminium_candidate_reproduces_pinned_rows": all(
        abs(next(e for e in results if e["name"].startswith("6061"))["rows"][p]["SF_b"] - ROWS[p]["SF_b_Al"]) < 1e-12 and
        abs(next(e for e in results if e["name"].startswith("6061"))["rows"][p]["SF_y"] - ROWS[p]["SF_y_Al"]) < 1e-12
        for p in ROW_ORDER),
    "tf_much_smaller_than_d_all_candidates_rows": max(
        e["rows"][p]["tf_over_d"] for e in results for p in ROW_ORDER),
    "candidate_count": len(results),
    "row_count": len(ROW_ORDER),
    "pins_verified": len(PINS),
}
assert checks["aluminium_candidate_reproduces_pinned_rows"]
assert checks["tf_much_smaller_than_d_all_candidates_rows"] < 0.01

nfi = [
 {"id": "NFI-008-QI-LAMINATE", "issue": "QI laminate E and compressive strength for T700, M55J, K13D2U and boron/epoxy are estimates from UD/fibre data with the stated reduction factors, not measured laminate cards.", "effect": "Those four rows move with the assumed QI factors; fibre properties were not used, per the brief.", "needed": "Measured QI laminate modulus and compressive strength for each system at the intended fibre volume fraction."},
 {"id": "NFI-008-SIGMA-TRANSFER", "issue": "6061-T6, 7075-T6, 2195-T8 and AlBeMet 162 compressive strengths are tensile yields transferred to compression; AZ31 uses a compressive yield, Ti-6Al-4V and Be S-200F use compressive values, SiC a compressive ultimate, Vitreloy 1 a compressive ultimate.", "effect": "SF_y for transferred rows is QUESTIONABLE; the 6061 baseline itself is the pinned transfer, so ratios are consistent with 002/003.", "needed": "Measured compressive yield for each metal temper and product form."},
 {"id": "NFI-008-BRITTLE-FACES", "issue": "SiC and beryllium rank on compressive membrane modes only. SiC flexural strength (~380 MPa) and fracture toughness, and beryllium toxicity, joining and low ductility, are outside both formulas.", "effect": "A high least-SF here is not a buildable face; bending, impact, attachment and thermal paths can govern.", "needed": "A fracture/joining assessment before either is carried as a face material."},
 {"id": "NFI-008-OMITTED-MODES", "issue": "Core shear, face wrinkling, core crush, laminate anisotropy (nu, shear), face-core bond and thermal stress are omitted, as in 002/003; equal face mass holds the pinned core and separation fixed.", "effect": "SF_b is a first-order tf<<d scaling; a candidate whose tf approached d, or whose nu differs strongly, would need the full sandwich formulas.", "needed": "MAINLINE-004 knockdown for kd rescaling, and a sandwich failure check per candidate."},
 {"id": "NFI-008-PROJECTIONS", "issue": "CNT-yarn and graphene QI rows are PROJECTION scenarios, not available materials; their assumed values are stated per row.", "effect": "They bound a direction, not a procurement option; the available-only best three are listed separately.", "needed": "A demonstrated QI CNT-yarn or graphene laminate card."},
 {"id": "NFI-008-KD", "issue": "All buckling SFs inherit kd=0.2; required E scales as 1/kd (Una's 003 correction), so every SF_b scales linearly with kd/0.2.", "effect": "MAINLINE-004's knockdown rescales every buckling column by one multiplication, as COMMON.md states.", "needed": "MAINLINE-004 filed values (next job 008c)."},
]

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

results_doc = {
 "schema": 1, "card": "MAINLINE-008", "unit": "vacuum-mainline008-material-gap-1019",
 "status": "ESTIMATE_PENDING_CHECKER", "started_at": STARTED, "ended_at": __import__("datetime").datetime.now().astimezone().isoformat(timespec="seconds"),
 "case": inputs["case"], "formulas": inputs["formulas"], "checks": checks,
 "baseline_figures_6061": {"E_over_rho_Pa_per_kg_m3": AL_E_RHO, "sigma_c_over_rho_Pa_per_kg_m3": AL_S_RHO},
 "candidates_ranked_by_least_SF_P2E": ranked,
 "best_three_overall_P2E": best3_overall,
 "best_three_available_P2E": best3_available,
 "NFI": [n["id"] for n in nfi],
}
pathlib.Path(OUT / "RESULTS.json").write_text(json.dumps(results_doc, indent=1) + "\n")
pathlib.Path(OUT / "NFI.json").write_text(json.dumps(nfi, indent=1) + "\n")

[withheld: private task or principal quotation; scientific result/status retained elsewhere]