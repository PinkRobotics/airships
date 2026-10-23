#!/usr/bin/env python3
"""MAINLINE-017b trends: today's best sourced value, the best value about 10, 20 and 30 years ago, the implied
annual rate, and the years to close the gap if that rate held (PROJECTION). Every value is drawn from this seat's
sourcing files (.ship/work/sources/017b/*.json) by property, year and product, and asserted, so nothing is retyped."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "unpublished-local-ref:6e94df3272e3fba2"
FILES = {k: json.load(open(f"{SRC}/{k}.json")) for k in ("be-face", "core-film", "knockdown", "p3-materials")}
C = json.load(open(os.path.join(HERE, "COMPUTE.json")))


def row(f, pid, year, text, value, tol=1e-6):
    """The one row with this property, year and product text; its value must be the one asserted."""
    hits = [(i, r) for i, r in enumerate(FILES[f]["rows"])
            if r["property_id"] == pid and r["year"] == year and text in r["material_or_product"]]
    if len(hits) > 1:   # L and W rows share a product and year: the asserted value picks one
        hits = [(i, r) for i, r in hits if r["value"] is not None and abs(r["value"] - value) <= tol * max(1.0, abs(value))]
    assert len(hits) == 1, (f, pid, year, text, len(hits))
    i, r = hits[0]
    assert r["value"] is not None and abs(r["value"] - value) <= tol * max(1.0, abs(value)), (f, pid, year, r["value"])
    s = r["source"]
    return {"file": f"{f}.json", "index": i, "year": year, "value": r["value"], "units": r["units"],
            "product": r["material_or_product"], "basis": r["basis"], "state": r["state"], "tag": r["tag"],
            "source": {"title": s.get("title"), "by": s.get("org_or_authors"), "url": s.get("url"), "doi": s.get("doi"),
                       "location": s.get("location")}}


def limit(f, pid, value):
    hits = [(i, r) for i, r in enumerate(FILES[f]["limits"])
            if r["property_id"] == pid and r["limit_value"] is not None and abs(r["limit_value"] - value) < 1e-6 * max(1, value)]
    assert len(hits) >= 1, (f, pid, value)
    i, r = hits[0]
    s = r["source"]
    return {"file": f"{f}.json", "limits_index": i, "value": r["limit_value"], "units": r["units"], "what": r["what"],
            "source": {"title": s.get("title"), "by": s.get("org_or_authors"), "url": s.get("url"), "doi": s.get("doi")}}


def rate(then, now, higher_better=True):
    y = now["year"] - then["year"]
    ratio = now["value"] / then["value"] if higher_better else then["value"] / now["value"]
    return {"from": [then["year"], then["value"]], "to": [now["year"], now["value"]], "years": y,
            "per_year": ratio ** (1.0 / y) - 1.0}


def years_to_close(gap, r):
    if gap <= 1.0:
        return 0.0
    if r is None or r <= 1e-6:
        return None
    return math.log(gap) / math.log(1.0 + r)


P2, P3 = C["p2"], C["p3"]
TRENDS = []

# ---------------------------------------------------------------- P2: face specific stiffness (the 'face density' lever)
be_now = row("be-face", "face_specific_stiffness_best", 2024, "SR-200 sheet", 156.8, 1e-3)
be_1966 = row("be-face", "face_specific_stiffness_best", 1966, "Beryllium (survey)", 164.0, 1e-3)
be_1971 = row("be-face", "face_specific_stiffness_best", 1971, "cross-rolled sheet", 158.4, 1e-3)
p120 = row("be-face", "face_specific_stiffness_best", 1992, "P-120", 387.1, 1e-3)
k1100 = row("be-face", "face_specific_stiffness_best", 2007, "K1100", 423.2, 1e-3)
qi75 = row("be-face", "face_specific_stiffness_best", 1994, "P75 carbon/epoxy 2D quasi-isotropic", 51.0, 1e-3)
fib_lim = limit("be-face", "face_specific_stiffness_best", 423)
need = {k: P2[k]["alone"]["face_density"]["factor"] for k in ("R10", "R20")}
TRENDS.append({
    "id": "face_specific_stiffness", "case": "P2", "lever": "face_density",
    "property": "Face specific stiffness E/rho of a thin in-plane-isotropic face, at beryllium's strength",
    "units": "MPa per kg/m3", "model_today": 290e9 / 1850 / 1e6,
    "needed": {k: 290e9 / 1850 / 1e6 * v for k, v in need.items()}, "factor": need,
    "today_best": be_now, "history": [be_1966, be_1971, qi75, p120, k1100],
    "rate": rate(be_1966, be_now), "rate_note": "beryllium, the best thin isotropic face in every era; the drop is the "
    "printed modulus (303 to 290 GPa), not a material change. Carbon fibre rose 387 to 423 along the fibre (1992-2007) "
    "but a quasi-isotropic laminate sits near 51 (P75, 1994) to about 100 (K13D2U, a PROJECTION estimate).",
    "limit": fib_lim, "verdict": "flat for 58 years; nothing has passed beryllium as a thin isotropic face; needs a step "
    "change (a new face material class)",
})
TRENDS[-1]["years_to_close"] = {k: years_to_close(v, None) for k, v in need.items()}

# ---------------------------------------------------------------- P2: face modulus at beryllium's density
mods = [row("be-face", "be_sheet_modulus", 1967, "SR-200 cross-rolled sheet 1.96 mm", 298.7, 1e-3),
        row("be-face", "be_sheet_modulus", 1971, "Beryllium cross-rolled sheet", 293.0),
        row("be-face", "be_sheet_modulus", 1991, "SR-200 cross-rolled beryllium sheet", 297.0),
        row("be-face", "be_sheet_modulus", 2001, "Electrofusion", 303.0),
        row("be-face", "be_sheet_modulus", 2020, "Materion design guide", 303.0)]
mod_now = row("be-face", "be_sheet_modulus", 2024, "SR-200 sheet (Materion)", 290.0)
need = {k: P2[k]["alone"]["face_modulus"]["factor"] for k in ("R10", "R20")}
TRENDS.append({
    "id": "face_modulus", "case": "P2", "lever": "face_modulus", "property": "Face Young's modulus at beryllium's density",
    "units": "GPa", "model_today": 290.0, "needed": {k: 290.0 * v for k, v in need.items()}, "factor": need,
    "only_via_vc2_step": True, "today_best": mod_now, "history": mods, "rate": rate(mods[0], mod_now),
    "limit": limit("be-face", "be_sheet_modulus", 306.9),
    "verdict": "flat (293-303 GPa since 1967); the ideal polycrystal is 307 GPa, so the needed 559-592 GPa is beyond the "
               "element; and the factor only works by crossing the Vc 2 step",
})
TRENDS[-1]["years_to_close"] = {k: None for k in need}

# ---------------------------------------------------------------- P2: gamma, the knockdown (shape precision)
kd = {"carlson": row("knockdown", "sphere_knockdown_best_test", 1966, "electroformed NICKEL", 0.86),
      "kaplan": row("knockdown", "sphere_knockdown_best_test", 1954, "shallow spherical domes", 0.85),
      "sp8032": row("knockdown", "sphere_knockdown_best_test", 1969, "isotropic thin spherical caps", 0.14),
      "lee2016": row("knockdown", "sphere_knockdown_best_test", 2016, "VPS", 0.69),
      "num2024": row("knockdown", "sphere_knockdown_best_test", 2024, "elastic hemispherical", 0.8),
      "cr1457": row("knockdown", "sandwich_dome_knockdown", 1969, "Saturn S-I", 0.2),
      "cta81": row("knockdown", "sandwich_dome_knockdown", 2018, "8-ft diameter, 120 in long", 0.87),
      "cta82": row("knockdown", "sandwich_dome_knockdown", 2024, "8-ft diameter, 100 in long", 0.721),
      "nesc2020": row("knockdown", "cylinder_knockdown_design", 2020, "uniform thin cylinders", 0.9)}
need = {k: P2[k]["gamma_translation"]["needed_gamma"] for k in ("R10", "R20")}
TRENDS.append({
    "id": "gamma_shape_precision", "case": "P2", "lever": "gamma",
    "property": "Global knockdown gamma (handbook 0.20), read as large-shell shape precision through MAINLINE-015's map",
    "units": "ratio to classical", "model_today": 0.20, "needed": need,
    "factor": {k: P2[k]["alone"]["gamma"]["factor"] for k in ("R10", "R20")},
    "map_015": {k: P2[k]["gamma_translation"]["map_015_at_gamma_alone_point"] for k in ("R10", "R20")},
    "today_best": kd["carlson"], "history": [kd["kaplan"], kd["cr1457"], kd["sp8032"], kd["lee2016"], kd["cta81"],
                                             kd["cta82"], kd["num2024"], kd["nesc2020"]],
    "rate": None, "rate_note": "the best sphere test is still 0.86 (1966, small electroformed nickel spheres); the "
    "sandwich-dome design value 0.20 (CR-1457, 1969, two 1964 hemisphere tests) has not moved. Cylinders are the one "
    "precedent: test-validated analysis lifted sandwich-cylinder test/perfect to 0.72-0.87 (2018-2024) against SP-8007's "
    "0.56-0.61.",
    "limit": limit("knockdown", "sphere_knockdown_best_test", 1.0),
    "verdict": "near the limit: R 10 needs 0.81, 94 percent of the best sphere test ever; no trend in 60 years; needs a "
               "step change, a test-validated knockdown for large sandwich spheres",
})
TRENDS[-1]["years_to_close"] = {k: None for k in need}

# ---------------------------------------------------------------- P2: core properties (alone not enough; the Be-kept material combination)
gw = [row("core-film", "core_shear_modulus_per_density", 1998, "3/8 in cell, 1.0", 2.927, 1e-3),
      row("core-film", "core_shear_modulus_per_density", 2004, "3/8 in cell, 1.0", 2.927, 1e-3),
      row("core-film", "core_shear_modulus_per_density", 2016, "3/8 in cell, 1.0", 2.927, 1e-3)]
gw_now = row("core-film", "core_shear_modulus_per_density", 2017, "3/8 in cell, 1.0", 2.927, 1e-3)
gw_1986 = row("core-film", "core_shear_modulus_per_density", 1986, "114-5052-0.0007", 2.917, 1e-3)
ultracor_w = row("core-film", "core_shear_modulus_per_density_best_any", 2023, "UCF-145-3/8-0.8", 6.463, 1e-3)
combo10 = P2["R10"]["combos"]["be_kept_material_only|stiff"]["factors"]
combo20 = P2["R20"]["combos"]["be_kept_material_only|stiff"]["factors"]
TRENDS.append({
    "id": "core_shear_stiffness_per_density", "case": "P2", "lever": "core_shear_modulus (and core_density)",
    "property": "Core W shear modulus per density (the brief's translation of gamma)", "units": "MPa per kg/m3",
    "model_today": 46.884349593e6 / 16.018463374 / 1e6,
    "alone": {k: P2[k]["alone"]["core_shear_modulus"] for k in ("R10", "R20")},
    "needed_in_be_kept_material_combination": {"R10": 2.927 * combo10.get("core_density", 1.0) * combo10.get("core_shear_modulus", 1.0),
                                               "R20": 2.927 * combo20.get("core_density", 1.0) * combo20.get("core_shear_modulus", 1.0)},
    "today_best": ultracor_w, "history": [gw_1986] + gw + [gw_now], "rate": rate(gw[0], gw_now),
    "limit": limit("core-film", "core_shear_modulus_per_density", 9.259),
    "verdict": "aluminium flat since at least 1986-1998 (identical Hexcel rows); carbon honeycomb (Ultracor, 2.2x in W) "
               "exists; not a lever alone (Kc caps global at 0.60/0.66)",
})
ec = [row("core-film", "core_compressive_modulus_per_density", 1998, "3/8 in cell, 1.0", 6.456, 1e-3),
      row("core-film", "core_compressive_modulus_per_density", 2004, "3/8 in cell, 1.0", 6.456, 1e-3),
      row("core-film", "core_compressive_modulus_per_density", 2016, "3/8 in cell, 1.0", 6.456, 1e-3)]
ec_now = row("core-film", "core_compressive_modulus_per_density", 2017, "3/8 in cell, 1.0", 6.456, 1e-3)
ec_best = row("core-film", "core_compressive_modulus_per_density", 2017, "1/8 in cell, 3.1", 13.47, 1e-3)
TRENDS.append({
    "id": "core_tt_stiffness_per_density", "case": "P2", "lever": "core_tt_modulus (and core_density)",
    "property": "Core through-thickness (stabilised compressive) modulus per density (Q's translation, route b)",
    "units": "MPa per kg/m3", "model_today": 103.421359e6 / 16.018463374 / 1e6,
    "alone": {k: P2[k]["alone"]["core_tt_modulus"] for k in ("R10", "R20")},
    "needed_in_be_kept_material_combination": {"R10": 6.456 * combo10.get("core_density", 1.0) * combo10.get("core_tt_modulus", 1.0),
                                               "R20": 6.456 * combo20.get("core_density", 1.0) * combo20.get("core_tt_modulus", 1.0)},
    "today_best": ec_best, "history": ec + [ec_now], "rate": rate(ec[0], ec_now),
    "limit": limit("core-film", "core_compressive_modulus_per_density", 24.81),
    "verdict": "aluminium flat since 1998; the Be-kept material combination needs 41-57 MPa per kg/m3, beyond "
               "aluminium's own 24.8 limit; no carbon-honeycomb compressive modulus was sourced",
})
TRENDS.append({
    "id": "face_flatness", "case": "P2", "lever": "face_flatness",
    "property": "Face flatness, the CR-1457 waviness parameter K_delta = delta Ec/(tc Fc) (Q's translation, route a)",
    "units": "mm of initial waviness at the design point",
    "today_equivalent_mm": {k: P2[k]["today_flatness_mm"] for k in ("R10", "R20")},
    "alone": {k: P2[k]["alone"]["face_flatness"] for k in ("R10", "R20")},
    "needed_in_be_kept_material_combination_mm": {
        "R10": P2["R10"]["combos"]["be_kept_material_only|stiff"]["point"]["flatness_mm"],
        "R20": P2["R20"]["combos"]["be_kept_material_only|stiff"]["point"]["flatness_mm"]},
    "today_best": row("knockdown", "wrinkle_coefficient_test", 1953, "tempered steel", 0.82),
    "history": [row("knockdown", "wrinkle_coefficient_test", 1945, "papreg", 0.5),
                row("knockdown", "wrinkle_coefficient_test", 1959, "aluminium and stainless", 0.125),
                row("knockdown", "wrinkle_coefficient_test", 1969, "FPL 1810-A", 0.33)],
    "rate": None, "limit": limit("knockdown", "wrinkle_coefficient_test", 0.82),
    "verdict": "no trend: the design 0.33 and classical 0.82 are unchanged since 1969 and no waviness history was found",
})

# ---------------------------------------------------------------- P2: sheet size, film, face strength (not levers alone)
TRENDS.append({
    "id": "sheet_size", "case": "P2", "lever": "sheet_size", "property": "Beryllium sheet length (largest listed)",
    "units": "mm", "alone": {k: P2[k]["alone"]["sheet_size"] for k in ("R10", "R20")},
    "today_best": row("be-face", "be_sheet_max_size", 2024, "SR-200 sheet (Materion)", 1829.0),
    "history": [row("be-face", "be_sheet_max_size", 1966, "Cross-rolled beryllium sheet", 2438.0),
                row("be-face", "be_sheet_max_size", 1972, "Kawecki Berylco", 2032.0)],
    "rate": rate(row("be-face", "be_sheet_max_size", 1966, "Cross-rolled beryllium sheet", 2438.0),
                 row("be-face", "be_sheet_max_size", 2024, "SR-200 sheet (Materion)", 1829.0)),
    "verdict": "shrinking (2438 mm in 1966, 1829 mm today); with 028's joining it is not a lever: a seamless shell lifts "
               "R 10 only from 0.528 to 0.536",
})
f1954 = row("core-film", "film_adhesive_areal_mass", 1954, "FM-47 adhesive tape (", 244.1, 1e-3)
f1975 = row("core-film", "film_adhesive_areal_mass", 1975, "3M AF-453", 146.5, 1e-3)
f2009 = row("core-film", "film_adhesive_areal_mass", 2009, "AF 163-2U", 73.24, 1e-3)
TRENDS.append({
    "id": "bond_film_mass", "case": "P2", "lever": "film_mass", "property": "Lightest structural film adhesive per bond line",
    "units": "g/m2", "alone": {k: P2[k]["alone"]["film_mass"] for k in ("R10", "R20")},
    "today_best": f2009, "history": [f1954, f1975, row("core-film", "film_adhesive_areal_mass", 2006, "Redux 312", 73.24, 1e-3),
                                     row("core-film", "film_adhesive_areal_mass", 2008, "EH84", 8.0, 1e-3)],
    "rate": rate(f1975, f2009, higher_better=False),
    "limit": limit("core-film", "film_adhesive_areal_mass", 11.54),
    "verdict": "halved 1954-2009 (about 2 percent a year), flat since; lab cell-edge deposition reached 8 g/m2; not a "
               "lever alone (a weightless bond lifts R 10 only to 0.560)",
})
TRENDS.append({
    "id": "face_strength", "case": "P2", "lever": "face_strength", "property": "Beryllium sheet minimum tensile yield (compression proxy)",
    "units": "MPa", "alone": {k: P2[k]["alone"]["face_strength"] for k in ("R10", "R20")},
    "today_best": row("be-face", "be_sheet_tensile_yield_min", 2024, "SR-200 sheet (Materion)", 345.0),
    "history": [row("be-face", "be_sheet_tensile_yield_min", 1966, "Commercial beryllium cross-rolled sheet", 345.0),
                row("be-face", "be_sheet_tensile_yield_min", 1992, "SR-200 hot rolled", 345.0),
                row("be-face", "be_sheet_compressive_yield", 1967, "SR-200 cross-rolled sheet, 1.96 mm", 379.2)],
    "rate": rate(row("be-face", "be_sheet_tensile_yield_min", 1966, "Commercial beryllium cross-rolled sheet", 345.0),
                 row("be-face", "be_sheet_tensile_yield_min", 2024, "SR-200 sheet (Materion)", 345.0)),
    "verdict": "flat since 1966; not a lever (face compression is not binding today)",
})

# ---------------------------------------------------------------- P3: tube specific stiffness
sic_hist = [row("p3-materials", "sic_modulus", 1988, "Hexoloy SA (Sohio)", 427.0),
            row("p3-materials", "sic_modulus", 1997, "Sintered alpha-SiC", 415.0),
            row("p3-materials", "sic_modulus", 2003, "Cercom SiC-N", 460.0),
            row("p3-materials", "sic_modulus", 2012, "Hexoloy SA (Saint-Gobain)", 430.0),
            row("p3-materials", "sic_modulus", 2024, "Hexoloy SA (Saint-Gobain) brochure", 430.0)]
sic_cvd = row("p3-materials", "sic_modulus", 2019, "PremaTech CVD SiC", 466.0)


def spec(r):
    rho = FILES["p3-materials"]["rows"][r["index"]]["density_kg_m3"]
    return {"year": r["year"], "value": r["value"] * 1e3 / rho, "product": r["product"], "E_GPa": r["value"], "rho": rho}


need3 = {"sic_density": P3["today"]["alone"]["sic_density"]["factor"], "sic_modulus": P3["today"]["alone"]["sic_modulus"]["factor"]}
spec_hist = [spec(r) for r in sic_hist]
spec_best = spec(sic_cvd)
needed_spec = 410e9 / 3100 / 1e6 * need3["sic_density"]
r_spec = rate(spec_hist[0], spec_best)
TRENDS.append({
    "id": "tube_specific_stiffness", "case": "P3 today", "lever": "sic_density / sic_modulus",
    "property": "Tube specific stiffness E/rho (SiC today)", "units": "MPa per kg/m3", "model_today": 410e9 / 3100 / 1e6,
    "needed": needed_spec, "factor": need3, "today_best": {**sic_cvd, "specific": spec_best}, "history": sic_hist,
    "specific_history": spec_hist, "rate": r_spec,
    "gap_over_best": needed_spec / spec_best["value"],
    "years_to_close": years_to_close(needed_spec / spec_best["value"], r_spec["per_year"]),
    "verdict": "SiC near-flat (0.2 percent a year across grades, 1988-2019); the needed 186 is 1.28 times the best SiC "
               "(CVD, 145); at that rate about a century (PROJECTION): a different tube material, a step change",
})

# ---------------------------------------------------------------- P3: film specific strength
fk75 = row("p3-materials", "film_specific_strength", 1975, "Kapton H film", 179.0)
fm99 = row("p3-materials", "film_specific_strength", 1999, "Mylar polyester film, type 92A", 196.0)
ft13 = row("p3-materials", "film_specific_strength", 2013, "Teonex Q51", 310.0)
fkh19 = row("p3-materials", "film_specific_strength", 2019, "Kapton HN", 231.0)
fu22 = row("p3-materials", "film_specific_strength", 2022, "UPILEX-S", 520.0)
zylon = row("p3-materials", "film_specific_strength", 2023, "Zylon HM (PBO) fibre", 5800.0)
dens = {"Kapton H film": 1420.0}   # the 1975 row prints no density: Kapton HN's 1420 kg/m3 (same polyimide) is used


def fspec(r):
    rho = FILES["p3-materials"]["rows"][r["index"]]["density_kg_m3"] or dens[[k for k in dens if k in r["product"]][0]]
    return {"year": r["year"], "value": r["value"] * 1e3 / rho, "product": r["product"], "MPa": r["value"], "rho": rho}


env = [fspec(r) for r in (fk75, fm99, ft13, fu22)]
model_design = 115.5e6 / 1420 / 1e3                     # kN m/kg: 024's Kapton HN at half of 231 MPa
f_need = P3["today"]["alone"]["film_specific_strength"]["factor"]
need_design = model_design * f_need
need_raw = need_design * 2.0                            # the same 0.5 design factor as 024's Kapton
gap = need_raw / env[-1]["value"]
r_long = rate(env[0], env[-1])
r_short = rate(env[1], env[-1])
TRENDS.append({
    "id": "film_specific_strength", "case": "P3 today", "lever": "film_specific_strength",
    "property": "Film tensile strength over density (best real film by year; design uses half, as 024)",
    "units": "kN m/kg", "model_today_design": model_design, "needed_design": need_design, "needed_raw": need_raw,
    "factor": f_need, "today_best": {**fu22, "specific": env[-1]}, "history": [fk75, fm99, ft13, fkh19],
    "envelope": env, "rate_long": r_long, "rate_recent": r_short, "gap_over_best": gap,
    "years_to_close": {"at_long_rate": years_to_close(gap, r_long["per_year"]),
                       "at_recent_rate": years_to_close(gap, r_short["per_year"])},
    "fibre_reference": fspec(zylon),
    "verdict": "the one P3 property still moving (about 2.2 percent a year since 1975, 4.1 since 1999); Upilex-S already "
               "gives 2.17 of the 3.79; the rest at 14-25 years if the trend held (PROJECTION)",
})

# ---------------------------------------------------------------- P3: SiC design compressive strength (the tube allowable)
TRENDS.append({
    "id": "sic_design_compressive_strength", "case": "P3", "lever": "sic_strength",
    "property": "SiC tube design compressive strength (the allowable)", "units": "MPa",
    "needed": {"projection_row_SF1": 3900.0 * P3["projection"]["alone"]["sic_strength"]["factor"],
               "today_row_kept": P3["today"]["strength_the_design_uses_MPa"]},
    "today_best": row("p3-materials", "sic_compressive_strength", 2012, "Hexoloy SA (Saint-Gobain)", 3900.0),
    "history": [row("p3-materials", "sic_flexural_strength", 1988, "Hexoloy SA (Sohio Engineered", 402.0),
                row("p3-materials", "sic_flexural_strength", 1995, "Hexoloy SA (Carborundum Company)", 395.0),
                row("p3-materials", "sic_flexural_strength", 2024, "SE grade", 380.0),
                row("p3-materials", "sic_compressive_strength", 2004, "Hexoloy SA (Saint-Gobain)", 3900.0)],
    "rate": rate(row("p3-materials", "sic_flexural_strength", 1988, "Hexoloy SA (Sohio Engineered", 402.0),
                 row("p3-materials", "sic_flexural_strength", 2024, "SE grade", 380.0)),
    "limit": limit("p3-materials", "sic_flexural_strength", 50.8),
    "verdict": "flat (flexure 380-402 MPa since 1988; vendor compression 3900 MPa since 2004); no design compressive "
               "allowable exists; every P3 route to SF 1 needs 0.83-1.20 GPa qualified: a qualification step, not a "
               "material one",
})

# ---------------------------------------------------------------- P3: lattice knockdown, local, joints, straightness
TRENDS.append({
    "id": "lattice_knockdown", "case": "P3 today", "lever": "lattice_knockdown",
    "property": "Global lattice knockdown k (0.2), read as frame precision", "units": "ratio",
    "needed": 0.2 * P3["today"]["alone"]["lattice_knockdown"]["factor"], "factor": P3["today"]["alone"]["lattice_knockdown"]["factor"],
    "today_best": row("knockdown", "lattice_dome_knockdown", 2001, "single-layer lattice", 0.65),
    "history": [row("knockdown", "lattice_dome_knockdown", 2020, "geodesic and lamella", 0.7)],
    "rate": None, "verdict": "no sourced trend; 0.65-0.70 are perfect-geometry or FE values, 0.2 and Wright's 0.4 are "
                             "unconfirmed; the needed 0.40 needs lattice-dome tests",
})
TRENDS.append({
    "id": "end_joint_mass", "case": "P3", "lever": "joint_mass", "property": "End-fitting compressive strength (CFRP)",
    "units": "MPa", "alone": P3["today"]["alone"]["joint_mass"],
    "today_best": row("p3-materials", "end_fitting_specific_strength", 2025, "T1100G carbon fibre in epoxy", 1870.0),
    "history": [row("p3-materials", "end_fitting_specific_strength", 2002, "T300 carbon fibre in epoxy", 1470.0),
                row("p3-materials", "end_fitting_specific_strength", 2000, "Ti-6Al-4V annealed", 827.0)],
    "rate": rate(row("p3-materials", "end_fitting_specific_strength", 2002, "T300 carbon fibre in epoxy", 1470.0),
                 row("p3-materials", "end_fitting_specific_strength", 2025, "T1100G carbon fibre in epoxy", 1870.0)),
    "verdict": "slowly rising (about 1 percent a year); not a lever alone (weightless joints lift today's row only to 0.753)",
})
TRENDS.append({
    "id": "local_knockdown", "case": "P3", "lever": "local_knockdown", "property": "Thin-cylinder local knockdown (SP-8007)",
    "units": "ratio", "alone": P3["today"]["alone"]["local_knockdown"],
    "today_best": kd["nesc2020"], "history": [],
    "rate": None, "verdict": "design rule unchanged since 1968; modern tests reach 0.7-0.9; not a lever alone (a perfect "
                             "wall lifts today's row only to 0.848)",
})
TRENDS.append({
    "id": "member_straightness", "case": "P3", "lever": "straightness", "property": "Member out-of-straightness",
    "units": "fraction of length", "alone": P3["today"]["alone"]["straightness"],
    "today_best": row("knockdown", "member_straightness", 2005, "structural steel members", 0.001),
    "history": [], "rate": None, "verdict": "not a lever in either row",
})

out = {"schema": 1, "trends": TRENDS}
tmp = os.path.join(HERE, "TRENDS.json.tmp")
with open(tmp, "w") as fh:
    json.dump(out, fh, indent=1, default=float)
os.replace(tmp, os.path.join(HERE, "TRENDS.json"))
for t in TRENDS:
    r = t.get("rate") or t.get("rate_long")
    print(t["id"], "|", round(r["per_year"] * 100, 3) if r else None, "%/yr |", t.get("years_to_close"), "|", t["verdict"][:90])
