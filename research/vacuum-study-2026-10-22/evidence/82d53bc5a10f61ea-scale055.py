#!/usr/bin/env python3
"""MAINLINE-055 arithmetic: similarity groups of the two P2 design points, face stand-ins, geometric scales, cap size,
pressure reach of the rigs and the article-count statistics. Every input is QUESTIONABLE and named with its source in
SRC below; outputs are written to scale055.json next to the card. Own arithmetic; no owner code."""
import json
import math
from pathlib import Path

from scipy import stats

OUT = Path("unpublished-local-ref:34d73948944acbff")
P = 95460.8379139e-6                          # MPa, the case (COMMON)
R10 = 10000.0                                 # mm
PSI = 0.00689475729

SRC = {
    "028b": "028b nominal AF/scarf least set (CARD.md): tf 0.794624 mm, tc 23.2372 mm, gamma 0.564164, wrinkle 0.434628",
    "040": "040 common account RESULTS.json, R30 ISA actual heavy70 vented least set {gamma, Q}",
    "core": "Hexcel CR III Table II, 5056 3/8 in. 1.0 pcf (owner-pinned copy 0467f718..., read in CHECK-029)",
    "Be": "Materion SR-200 sheet: 290 GPa, 345 MPa tensile minimum used as compression proxy (028b/038); sheet 0.020-0.250 in.",
    "5052-O": "Gabrian 5052 datasheet: 5052-O yield 89.6 MPa (13 ksi), E 70.3 GPa; MakeItFrom lists 79 MPa (range 65-90)",
    "handbook": "MMPDS / MIL-HDBK-5J typical values (not opened this session): 5052-H32, 2024-T3, 7075-T6, CP-Ti Gr 2, Ti-6Al-4V",
    "CFRP": "CMH-17 class typical quasi-isotropic carbon/epoxy (not opened): E about 55 GPa, compressive strength about 500 MPa",
    "reis2017": "Lopez Jimenez, Marthelot, Lee, Hutchinson, Reis, J. Appl. Mech. 84 (2017) 034501, doi 10.1115/1.4035665",
    "042": "042 / CHECK-042: dimple tolerance 9.318267-16.057295 mm over the 015b width, waviness 0.0751-0.1288 mm",
    "038": "038 T7: three R 0.5 m surrogate shells, USD 30-90k; 0.4303 m conditional minimum radius; 6.143% sea-level overload",
}

# ---- the two design points ------------------------------------------------------------------------------------------
CORE = {"En": 103.42135939752539, "GW": 46.88434959354485, "GL": 103.4213593975254, "cell": 9.525, "rho": 16.0185,
        "tauW_typ": 35 * PSI, "tauW_min": 25 * PSI, "tauL_typ": 55 * PSI, "tauL_min": 45 * PSI, "crush": 35 * PSI}
DESIGNS = {
    "R10 lead (028b)": {"R": 10000.0, "tf": 0.794624067, "tc": 23.237217906, "gamma": 0.564164, "nu": 0.0752},
    "R30 ISA (040)": {"R": 30000.0, "tf": 2.4649, "tc": 102.59, "gamma": 0.3865, "nu": 0.0768},
}
E_BE, SY_BE = 290000.0, 345.0


def groups(R, tf, tc, E, nu, sy, G=CORE["GW"], En=CORE["En"], cell=CORE["cell"], p=P):
    h = tf + tc
    teq = math.sqrt(3) * h
    p_cl = 2 * E * h * 2 * tf / (R ** 2 * math.sqrt(1 - nu ** 2))
    p_cr = 2 * h ** 2 * G / (R * tc)
    Vc = p_cl / p_cr
    Kc = 1 - Vc / 4 if Vc <= 2 else 1 / Vc
    s_face = p * R / (4 * tf)
    s_cl = p_cl * R / (4 * tf)
    wr = 0.82 * math.sqrt(E * En * tf / tc)                    # symmetric wrinkling, antiplane honeycomb (0.82 form)
    dimp = 2 * E / (1 - nu ** 2) * (tf / cell) ** 2            # intracell dimpling
    k = (12 * (1 - 0.33 ** 2)) ** 0.25                          # 015b width convention, nu 0.33
    return {"h_mm": h, "t_eq_mm": teq, "R_over_h": R / h, "R_over_teq": R / teq, "tf_over_h": tf / h,
            "sqrt_R_teq_mm": math.sqrt(R * teq), "lambda1_width_mm": math.sqrt(R * teq) / k,
            "p_classical_kPa": p_cl * 1e3, "p_crimp_kPa": p_cr * 1e3, "Vc": Vc, "Kc": Kc, "p_H_kPa": Kc * p_cl * 1e3,
            "gamma_needed_at_p": p / (Kc * p_cl), "face_stress_at_p_MPa": s_face, "face_stress_over_yield": s_face / sy,
            "classical_face_stress_MPa": s_cl, "classical_over_yield": s_cl / sy,
            "E_over_sy": E / sy, "wrinkle_stress_MPa": wr, "wrinkle_margin": wr / s_face, "dimpling_stress_MPa": dimp,
            "dimpling_margin": dimp / s_face, "cell_over_h": cell / h,
            "wrinkle_wavelength_mm": 2 * math.pi * ((E * tf ** 3 / 12) / (2 * En / tc)) ** 0.25,
            "cells_per_wrinkle_wavelength": 2 * math.pi * ((E * tf ** 3 / 12) / (2 * En / tc)) ** 0.25 / cell,
            "panel_short_side_over_sqrt_R_teq": 609.6 / math.sqrt(R * teq),
            "panel_long_side_over_sqrt_R_teq": 1828.8 / math.sqrt(R * teq)}


res = {"schema": 1, "sources": SRC, "designs": {}}
for name, d in DESIGNS.items():
    g = groups(d["R"], d["tf"], d["tc"], E_BE, d["nu"], SY_BE)
    g["gamma_line"] = d["gamma"]
    g["face_stress_at_collapse_if_gamma_line_MPa"] = d["gamma"] * g["Kc"] * g["classical_face_stress_MPa"]
    g["collapse_stress_over_yield"] = g["face_stress_at_collapse_if_gamma_line_MPa"] / SY_BE
    res["designs"][name] = {"inputs": d, "groups": g}

# ---- face stand-ins matched to the classical buckling stiffness E t / sqrt(1 - nu^2), face separation h held ----------
MATS = {  # E MPa, nu, yield (or compressive strength) MPa, density kg/m3, behaviour after yield, source key
    "SR-200 Be (design)": (290000.0, 0.0752, 345.0, 1850.0, "low ductility (about 2-3% elongation)", "Be"),
    "5052-O": (70300.0, 0.33, 89.6, 2680.0, "ductile, strain-hardening (about 25% elongation)", "5052-O"),
    "5052-H32": (70300.0, 0.33, 193.0, 2680.0, "ductile", "handbook"),
    "6061-T6": (68900.0, 0.33, 276.0, 2700.0, "ductile", "COMMON"),
    "2024-T3": (73100.0, 0.33, 345.0, 2780.0, "ductile", "handbook"),
    "7075-T6": (71700.0, 0.33, 503.0, 2810.0, "limited ductility", "handbook"),
    "CP-Ti grade 2": (105000.0, 0.37, 275.0, 4510.0, "ductile", "handbook"),
    "Ti-6Al-4V": (113800.0, 0.342, 880.0, 4430.0, "moderate ductility", "handbook"),
    "CFRP quasi-isotropic": (55000.0, 0.30, 500.0, 1550.0, "linear to brittle failure, no yield", "CFRP"),
}
lead = DESIGNS["R10 lead (028b)"]
gB = groups(lead["R"], lead["tf"], lead["tc"], E_BE, lead["nu"], SY_BE)
stand = {}
for name, (E, nu, sy, rho, post, src) in MATS.items():
    t = lead["tf"] * (E_BE / math.sqrt(1 - lead["nu"] ** 2)) / (E / math.sqrt(1 - nu ** 2))
    tc = gB["h_mm"] - t
    g = groups(lead["R"], t, tc, E, nu, sy)
    stand[name] = {"E_MPa": E, "nu": nu, "yield_MPa": sy, "source": src, "post_yield": post, "face_t_mm": t, "core_t_mm": tc,
                   "face_kg_per_m2_two_faces": 2 * t * 1e-3 * rho,
                   "p_classical_ratio_to_Be": g["p_classical_kPa"] / gB["p_classical_kPa"], "Vc": g["Vc"],
                   "face_stress_over_yield_at_p": g["face_stress_over_yield"],
                   "yield_ratio_vs_Be": g["face_stress_over_yield"] / gB["face_stress_over_yield"],
                   "biaxial_membrane_stiffness_ratio_vs_Be": (E * t / (1 - nu)) / (E_BE * lead["tf"] / (1 - lead["nu"])),
                   "wrinkle_margin": g["wrinkle_margin"], "wrinkle_margin_ratio_vs_Be": g["wrinkle_margin"] / gB["wrinkle_margin"],
                   "dimpling_margin": g["dimpling_margin"], "E_over_sy": E / sy}
res["stand_ins"] = stand

# ---- geometric scales with the same materials (038's homothety), and what the stock forbids --------------------------
scales = []
for s in (1.0, 0.75, 0.639, 0.5, 0.25, 0.1, 0.05, 0.0430344):
    tf, tc, cell_needed = lead["tf"] * s, lead["tc"] * s, CORE["cell"] * s
    g_stock = groups(R10 * s, tf, tc, E_BE, lead["nu"], SY_BE, cell=CORE["cell"])
    scales.append({"scale": s, "R_m": 10 * s, "diameter_m": 20 * s, "Be_face_mm": tf, "core_mm": tc,
                   "cell_needed_mm": cell_needed, "Be_gauge_ok_min_0p508mm": tf >= 0.508,
                   "dimpling_margin_with_stock_3_8_cell": g_stock["dimpling_margin"],
                   "cells_per_wrinkle_wavelength_stock_cell": g_stock["cells_per_wrinkle_wavelength"],
                   "cells_through_core_stock_cell": tc / CORE["cell"],
                   "design_pressure_kPa": P * 1e3, "dimple_amp_mm_at_16p057": 16.057295 * s})
res["geometric_scales"] = scales
res["hex_honeycomb_lightest_per_cell_pcf"] = {"1/8": 3.1, "5/32": 2.6, "3/16": 2.0, "1/4": 1.6, "3/8": 1.0,
                                              "source": "Hexcel CR III Tables I and II (owner-pinned copy)"}

# ---- caps on the true curvature: rise, Koga-Hoff/Reis parameter of the cap, edge distance -----------------------------
caps = []
for a in (1000.0, 1500.0, 2000.0, 2500.0, 3000.0, 4000.0):
    H = R10 - math.sqrt(R10 ** 2 - a ** 2)
    lam_cap = 2 * (3 * (1 - 0.33 ** 2)) ** 0.25 * math.sqrt(H / gB["t_eq_mm"])
    arc = R10 * math.asin(a / R10)
    caps.append({"base_radius_m": a / 1000, "diameter_m": 2 * a / 1000, "rise_mm": H, "cap_lambda": lam_cap,
                 "edge_distance_over_sqrt_R_teq": arc / gB["sqrt_R_teq_mm"],
                 "edge_distance_over_dimple_width": arc / gB["lambda1_width_mm"],
                 "shell_area_m2": 2 * math.pi * R10 * H / 1e6, "panels_0p61x1p83_per_face": 2 * math.pi * R10 * H / 1e6 / (0.6096 * 1.8288)})
res["caps_R10"] = caps

# ---- Reis 2017 plateau knockdown for a homogeneous elastic sphere at the specified width (lambda = 1) ----------------
lam_I = 1.0
res["reis2017_plateau_at_lambda1"] = (1 - 0.036) / (1 + lam_I) ** 1.23 + 0.036

# ---- pressure reach of rigs: what gamma can a full-section article be driven to ------------------------------------
reach = []
for name, dp in (("evacuation at the 500 m design ambient", P * 1e3), ("evacuation at sea level, 1 kPa residual", 101.325 - 1.0),
                 ("sea level evacuation + 2 m water", 101.325 - 1.0 + 2 * 9.80665),
                 ("sea level evacuation + 5 m water", 101.325 - 1.0 + 5 * 9.80665),
                 ("sea level evacuation + 10 m water", 101.325 - 1.0 + 10 * 9.80665)):
    reach.append({"rig": name, "max_dp_kPa": dp, "max_gamma_R10_section": lead["gamma"] * dp / (P * 1e3)})
res["rig_reach"] = reach

# ---- article counts: one-sided tolerance factors (normal), 90% coverage at 95% confidence --------------------------
counts = []
for n in (2, 3, 4, 5, 6, 8, 10, 15):
    zp = stats.norm.ppf(0.90)
    k = stats.nct.ppf(0.95, df=n - 1, nc=zp * math.sqrt(n)) / math.sqrt(n)
    row = {"n": n, "k_90_95": k}
    for cov in (0.05, 0.10, 0.15):
        f = 1 - k * cov
        row[f"mean_needed_R10_cov{int(cov * 100)}"] = lead["gamma"] / f if f > 0 else None
        row[f"mean_needed_R30_cov{int(cov * 100)}"] = DESIGNS["R30 ISA (040)"]["gamma"] / f if f > 0 else None
    counts.append(row)
res["article_counts"] = counts
(OUT / "scale055.json").write_text(json.dumps(res, indent=1))
for k, v in res["designs"].items():
    print(k, {a: round(b, 4) for a, b in v["groups"].items()})
print()
for k, v in stand.items():
    print(f"{k:22s} t {v['face_t_mm']:.3f} tc {v['core_t_mm']:.3f} sig/sy {v['face_stress_over_yield_at_p']:.3f} (x{v['yield_ratio_vs_Be']:.2f}) "
          f"wrinkle x{v['wrinkle_margin_ratio_vs_Be']:.2f} biax x{v['biaxial_membrane_stiffness_ratio_vs_Be']:.2f} kg/m2 {v['face_kg_per_m2_two_faces']:.2f}")
print()
for c in caps:
    print({k: round(v, 3) for k, v in c.items()})
print("plateau", res["reis2017_plateau_at_lambda1"])
for r in reach:
    print(r)
for r in counts:
    print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
