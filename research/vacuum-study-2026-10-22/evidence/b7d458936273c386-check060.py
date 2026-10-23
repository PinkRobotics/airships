#!/usr/bin/env python3
"""CHECK MAINLINE-060 (P3 carbon frame): my own arithmetic from the pinned inputs, compared with the card's printed values.

Inputs read as data (no owner code read or run): 051 MATERIAL-MODELS.json (ply stiffnesses, layups), WITNESSES.json (019
witness tube masses, peak stresses, areas, member forces), GAPS.json (required whole-member scales by m), HAIL-DESIGN.csv;
052 RESULTS.json (ground, all-endpoint bills R10-30, ISA and optimistic, baseline axes); 054 MASS-ACCOUNT.csv. Sourced
values were re-read from the primary PDFs (see SOURCES in the output). Writes RESULTS-CHECK.json."""
import csv
import json
import math
from pathlib import Path

import numpy as np

W = Path("unpublished-local-ref:7a5bf1cec24b249e")
D51 = W / "ref-70f7af6d0a8d64c42272/.ship/work/outputs/vacuum-mainline051-p3-frame-targets-complete-1020"
D52 = W / "ref-baa4584cf36c531365e7/.ship/work/outputs/vacuum-mainline052-p3-common-account-1020"
D54 = W / "ref-baa4584cf36c531365e7/.ship/work/outputs/vacuum-mainline054-p3-dry-cavity-1020"
OUT = W / "ref-55cff924be25afe6f9dd/.ship/work/outputs/vacuum-mainline060-check-1020/RESULTS-CHECK.json"
RADII = (10, 12, 15, 20, 30)
LN = -math.log(1 - 1e-3)                      # 0.0010005003...
V_COUPON = 0.32e-6                            # the card's compression gauge, m3 (PROJECTION)
# sourced compression (verified in the primary PDFs, MPa)
XC = {"K13D2U": 340.0, "M55J": 890.0, "T700S": 1450.0}
CONS = ["K13D2U-50-20-20-10", "K13D2U-70-10-10-10", "K13D2U-UD", "M55J-50-20-20-10", "M55J-70-10-10-10", "M55J-UD",
        "T700S-50-20-20-10", "T700S-70-10-10-10", "T700S-UD"]
CARD1 = {  # card section 1: ratio, lam mean GPa, tubes kg, peak GPa, mean SF, wall mean, wall Pf CV5.2, CV6, size CV6, Pf witness
    "K13D2U-50-20-20-10": (1.787, 0.190, 3610, 0.695, 0.274, 3.65, 6.21, 6.69, 11.90, 1.0),
    "K13D2U-70-10-10-10": (1.355, 0.251, 4267, 0.584, 0.430, 2.33, 3.96, 4.26, 7.46, 1.0),
    "K13D2U-UD": (1.000, 0.340, 8689, 0.285, 1.193, 1.00, 1.43, 1.54, 2.65, 0.995),
    "M55J-50-20-20-10": (1.774, 0.502, 4704, 0.484, 1.037, 1.00, 1.64, 1.76, 2.98, 1.0),
    "M55J-70-10-10-10": (1.352, 0.658, 4775, 0.474, 1.390, 1.00, 1.22, 1.32, 2.19, 0.216),
    "M55J-UD": (1.000, 0.890, 8725, 0.257, 3.463, 1.00, 1.00, 1.00, 1.00, 2.94e-09),
    "T700S-50-20-20-10": (1.700, 0.853, 11024, 0.199, 4.292, 1.00, 1.00, 1.00, 1.00, 3.9e-11),
    "T700S-70-10-10-10": (1.329, 1.091, 8876, 0.246, 4.430, 1.00, 1.00, 1.00, 1.00, 2.03e-11),
    "T700S-UD": (1.000, 1.450, 8849, 0.245, 5.906, 1.00, 1.00, 1.00, 1.00, 6.51e-14)}


def qbar(Q, theta):
    """Rotated reduced stiffness (engineering shear strain convention)."""
    c, s = math.cos(theta), math.sin(theta)
    q11, q12, q22, q66 = Q[0][0], Q[0][1], Q[1][1], Q[2][2]
    return np.array([
        [q11 * c**4 + 2 * (q12 + 2 * q66) * s * s * c * c + q22 * s**4, (q11 + q22 - 4 * q66) * s * s * c * c + q12 * (s**4 + c**4),
         (q11 - q12 - 2 * q66) * s * c**3 + (q12 - q22 + 2 * q66) * s**3 * c],
        [(q11 + q22 - 4 * q66) * s * s * c * c + q12 * (s**4 + c**4), q11 * s**4 + 2 * (q12 + 2 * q66) * s * s * c * c + q22 * c**4,
         (q11 - q12 - 2 * q66) * s**3 * c + (q12 - q22 + 2 * q66) * s * c**3],
        [(q11 - q12 - 2 * q66) * s * c**3 + (q12 - q22 + 2 * q66) * s**3 * c,
         (q11 - q12 - 2 * q66) * s**3 * c + (q12 - q22 + 2 * q66) * s * c**3,
         (q11 + q22 - 2 * q12 - 2 * q66) * s * s * c * c + q66 * (s**4 + c**4)]])


def lamina_Q(E1, E2, G12, nu12):
    nu21 = nu12 * E2 / E1
    d = 1 - nu12 * nu21
    return [[E1 / d, nu12 * E2 / d, 0.0], [nu12 * E2 / d, E2 / d, 0.0], [0.0, 0.0, G12]]


def zero_ply_ratio(Q, layup):
    """Fibre-direction stress in the 0 deg ply per unit uniaxial laminate compression (sigma_x = -1, sigma_y = tau = 0)."""
    A = sum(f * qbar(Q, math.radians(a)) for a, f in layup)
    eps = np.linalg.solve(A, np.array([-1.0, 0.0, 0.0]))
    s0 = np.array(Q) @ eps
    return -float(s0[0]), A


def recover_ply(Qm):
    """E1, E2, G12, nu12 from a lamina reduced-stiffness matrix."""
    q11, q12, q22, q66 = Qm[0][0], Qm[0][1], Qm[1][1], Qm[2][2]
    nu12 = q12 / q22
    nu21 = q12 / q11
    d = 1 - nu12 * nu21
    return q11 * d, q22 * d, q66, nu12


def interp_k(ks, m):
    """k(m) between 051's tabulated m: ln S(m) linear in m, S = LN k^m (S = sum of (sigma_i/peak)^m)."""
    ms = sorted(ks)
    lo = max(x for x in ms if x <= m)
    hi = min(x for x in ms if x >= m)
    if lo == hi:
        return ks[lo]
    sl, sh = math.log(LN) + lo * math.log(ks[lo]), math.log(LN) + hi * math.log(ks[hi])
    s = sl + (sh - sl) * (m - lo) / (hi - lo)
    return math.exp((s - math.log(LN)) / m)


def gam(m):
    return math.gamma(1 + 1 / m)


def main():
    mm = {x["id"]: x for x in json.loads((D51 / "MATERIAL-MODELS.json").read_text())}
    wit = {r["material"]: r for r in json.loads((D51 / "WITNESSES.json").read_text())["rows"] if r["reserve"] == "019"}
    gaps = {x["material"]: x for x in json.loads((D51 / "GAPS.json").read_text())["rows"]
            if x["reserve"] == "019" and x["section_policy"] == "verified_q1_1" and x["load_case"] == "operating"}
    ref_tubes = wit["041-reference"]["comparison_geometry"]["frame_tubes_kg"]
    L_mean = 1799.676624 / 750                 # 051 member arc lengths: total / count
    out = {"unit": "vacuum-mainline060-check-1020", "tag": "QUESTIONABLE / PROJECTION", "ref_tubes_kg": ref_tubes, "rows": {}}
    # ---------------- 1. ply ratios, first-ply, constructions
    sec1 = {}
    for cid in CONS:
        fib = cid.split("-")[0]
        mat = mm[cid]
        Qm = mat["lamina_Q_Pa"]
        E1, E2, G12, nu12 = recover_ply(Qm)
        layup = [(a, f) for a, f in mat["layup"]]
        ratio, A = zero_ply_ratio(lamina_Q(E1, E2, G12, nu12), layup)
        lam = XC[fib] / ratio / 1000                                        # GPa, laminate first-ply mean
        cg, fe = wit[cid]["comparison_geometry"], wit[cid]["FE"]
        peak_cg, peak_fe = cg["q1_peak_compression_Pa"] / 1e9, fe["q1_peak_compression_Pa"] / 1e9
        ks = {t["m"]: t["whole_member_scale_needed_Pa"] / gaps[cid]["peak_Pa"] for t in gaps[cid]["targets"] if t["Pf"] == 1e-3}
        rec = {"E1_GPa": E1 / 1e9, "E2_GPa": E2 / 1e9, "G12_GPa": G12 / 1e9, "nu12": nu12, "ratio": ratio,
               "ratio_051": -mat["ply_ratios"][0]["stress_per_unit_global_compression"][0], "lam_mean_GPa": lam,
               "tubes_kg": cg["frame_tubes_kg"], "peak_cg_GPa": peak_cg, "peak_fe_GPa": peak_fe,
               "mean_SF": lam / peak_cg, "mean_SF_fe": lam / peak_fe, "wall_mean": max(1.0, peak_cg / lam), "k": ks}
        vt = cg["area_m2"] * L_mean
        for tag, cv in (("cv52", 0.052), ("cv6", 0.06)):
            m = 1.2 / cv
            k = interp_k(ks, m)
            scale = lam / gam(m)
            for pk, pkv in (("cg", peak_cg), ("fe", peak_fe)):
                f = max(1.0, k * pkv / scale)
                rec[f"wall_Pf_{tag}_{pk}"] = f
                # size scaling: tube scale = coupon scale (Vc / Vt(f))^(1/m), Vt grows with the wall
                g = (k * pkv / (scale * (V_COUPON / vt) ** (1 / m))) ** (m / (m - 1))
                rec[f"wall_Pf_size_{tag}_{pk}"] = max(1.0, g)
                H = LN * (k * pkv / scale) ** m
                rec[f"Pf_witness_{tag}_{pk}"] = -math.expm1(-H)
            rec[f"m_{tag}"] = m
            rec[f"k_{tag}"] = k
            rec[f"size_factor_{tag}"] = (V_COUPON / vt) ** (1 / m)
        rec["member_volume_cm3"] = vt * 1e6
        rec["max_axial_kN"] = fe["max_axial_N"] / 1e3
        rec["peak_times_area_kN"] = peak_cg * 1e9 * cg["area_m2"] / 1e3
        rec["wall_mm"] = cg["wall_m"] * 1e3
        c = CARD1[cid]
        rec["card"] = dict(zip(("ratio", "lam_mean", "tubes", "peak", "mean_SF", "wall_mean", "wall_cv52", "wall_cv6", "wall_size_cv6",
                                "Pf_witness"), c))
        sec1[cid] = rec
    out["sec1"] = sec1
    k5 = sec1["K13D2U-50-20-20-10"]
    out["first_ply"] = {"lam_mean_GPa": k5["lam_mean_GPa"], "scale_m10_GPa": k5["lam_mean_GPa"] / gam(10),
                        "scale_m20_GPa": k5["lam_mean_GPa"] / gam(20), "ratio_to_2p16_mean": 2.16 / k5["lam_mean_GPa"],
                        "ratio_to_2p16_scale_m10": 2.16 / (k5["lam_mean_GPa"] / gam(10)),
                        "ply_strength_for_2p16_scale_m10_GPa": 2.16 * gam(10) * k5["ratio"],
                        "mean_SF_at_witness": k5["mean_SF"],
                        "sensitivity_E2_5GPa_DIALEAD_sheet": None}
    # sensitivity: the DIALEAD K13D2U sheet's transverse modulus 5.0 GPa instead of 051's assumed 8 GPa
    E1, E2, G12, nu12 = recover_ply(mm["K13D2U-50-20-20-10"]["lamina_Q_Pa"])
    r5, _ = zero_ply_ratio(lamina_Q(E1, 5.0e9, G12, nu12), [(a, f) for a, f in mm["K13D2U-50-20-20-10"]["layup"]])
    r_sheetE1, _ = zero_ply_ratio(lamina_Q(560e9, 5.0e9, G12, nu12), [(a, f) for a, f in mm["K13D2U-50-20-20-10"]["layup"]])
    out["first_ply"]["sensitivity_E2_5GPa_DIALEAD_sheet"] = {"ratio": r5, "lam_mean_GPa": 0.340 / r5,
                                                            "ratio_with_E1_560": r_sheetE1, "lam_mean_with_E1_560": 0.340 / r_sheetE1}
    # ---------------- 2. whole bill from 052 rows
    d52 = json.loads((D52 / "RESULTS.json").read_text())["rows"]
    base = {}
    for r in d52:
        if r["service"] != "ground":
            continue
        base[(r["R_m"], r["weather"], "endpoint")] = r["all_axes_endpoint"]
        base[(r["R_m"], r["weather"], "baseline")] = r["baseline"]
    rows54 = list(csv.DictReader(open(D54 / "MASS-ACCOUNT.csv")))
    inc = {}
    for R in (10, 12, 15):
        p0 = base[(R, "ISA", "endpoint")]["payload_kg"]
        r1 = next(r for r in rows54 if int(r["R_m"]) == R and r["weather"] == "ISA" and r["account"] == "endpoint" and r["days"] == "1"
                  and r["candidate"] == "MET" and r["route"] == "barrier_only")
        r7 = next(r for r in rows54 if int(r["R_m"]) == R and r["weather"] == "ISA" and r["account"] == "endpoint" and r["days"] == "7"
                  and r["candidate"] == "SIOX" and r["route"] == "barrier_plus_3A")
        inc[R] = (p0 - float(r1["payload_kg"]), p0 - float(r7["payload_kg"]))
    # extrapolate: 1-day as R^2 from R10; 7-day as a + b R^2 through R10 and R15
    b7 = (inc[15][1] - inc[10][1]) / (225 - 100)
    a7 = inc[10][1] - 100 * b7
    for R in (20, 30):
        inc[R] = (inc[10][0] * (R / 10) ** 2, a7 + b7 * R * R)
    out["dry_cavity_increments_kg"] = {str(R): inc[R] for R in RADII}

    def payload(R, cid, f, weather="ISA", axes="endpoint", fittings=None):
        b = base[(R, weather, axes)]
        lift = b["payload_kg"] + sum(b["bill_kg"].values())
        tubes = b["bill_kg"]["SiC_tubes"] * sec1[cid]["tubes_kg"] / ref_tubes * f if cid else b["bill_kg"]["SiC_tubes"]
        bill = sum(v for k, v in b["bill_kg"].items() if k != "SiC_tubes") + tubes
        if fittings is not None:
            bill += fittings * tubes - b["bill_kg"]["joint_sleeves_and_allowance"]
        return lift - bill, tubes, lift

    walls = {"K13D2U-50-20-20-10:stiffness": ("K13D2U-50-20-20-10", 1.0),
             "K13D2U-50-20-20-10:mean": ("K13D2U-50-20-20-10", sec1["K13D2U-50-20-20-10"]["wall_mean"]),
             "K13D2U-50-20-20-10:Pf_cv6": ("K13D2U-50-20-20-10", sec1["K13D2U-50-20-20-10"]["wall_Pf_cv6_cg"]),
             "M55J-50-20-20-10:stiffness": ("M55J-50-20-20-10", 1.0),
             "M55J-70-10-10-10:Pf_cv6": ("M55J-70-10-10-10", sec1["M55J-70-10-10-10"]["wall_Pf_cv6_cg"]),
             "M55J-70-10-10-10:Pf_cv6_fe": ("M55J-70-10-10-10", sec1["M55J-70-10-10-10"]["wall_Pf_cv6_fe"]),
             "M55J-UD:Pf_size_cv6": ("M55J-UD", sec1["M55J-UD"]["wall_Pf_size_cv6_cg"]),
             "T700S-70-10-10-10:stiffness": ("T700S-70-10-10-10", 1.0)}
    sec2 = {"SiC": {str(R): payload(R, None, 1.0)[0] for R in RADII}}
    for key, (cid, f) in walls.items():
        sec2[key] = {str(R): payload(R, cid, f)[0] for R in RADII}
        sec2[key + ":wall"] = f
        sec2[key + ":tubes_R10"] = payload(10, cid, f)[1]
    sec2["M55J-70-10-10-10:Pf_cv6:optimistic_R10"] = payload(10, "M55J-70-10-10-10", sec1["M55J-70-10-10-10"]["wall_Pf_cv6_cg"], "optimistic")[0]
    sec2["M55J-70-10-10-10:Pf_cv6:baseline_axes_R10"] = payload(10, "M55J-70-10-10-10", sec1["M55J-70-10-10-10"]["wall_Pf_cv6_cg"], "ISA", "baseline")[0]
    out["sec2_payload_kg"] = sec2
    # cubic penalty
    out["float_limit_tube_multiplier"] = {str(R): (base[(R, "ISA", "endpoint")]["bill_kg"]["SiC_tubes"] + base[(R, "ISA", "endpoint")]["payload_kg"])
                                          / base[(R, "ISA", "endpoint")]["bill_kg"]["SiC_tubes"] for R in RADII}
    out["tube_multiplier"] = {cid: sec1[cid]["tubes_kg"] / ref_tubes for cid in CONS}
    # joints: Messinger 44K strut (13.31 body, 1.20 insert, 1.50 ball, 16.01 lb total); 110K strut (23.28, 3.56, 5.40, 32.24)
    s44 = (1.20 + 1.50) / 16.01
    s110 = (3.56 + 5.40) / 32.24
    out["joints"] = {"share_44K": s44, "per_tube_44K": s44 / (1 - s44), "share_110K": s110, "per_tube_110K": s110 / (1 - s110),
                     "per_tube_70pct": 0.7 / 0.3,
                     "K13D2U-50-20-20-10_stiffness_44K": {str(R): payload(R, "K13D2U-50-20-20-10", 1.0, fittings=s44 / (1 - s44))[0] for R in RADII},
                     "K13D2U-50-20-20-10_stiffness_110K": {str(R): payload(R, "K13D2U-50-20-20-10", 1.0, fittings=s110 / (1 - s110))[0] for R in RADII},
                     "max_axial_kN_K13D2U-50": sec1["K13D2U-50-20-20-10"]["max_axial_kN"],
                     "peak_times_area_kN_K13D2U-50": sec1["K13D2U-50-20-20-10"]["peak_times_area_kN"],
                     "NG2_kN": 121.7 * 4.4482216,
                     "ratio_axial_to_NG2": sec1["K13D2U-50-20-20-10"]["max_axial_kN"] / (121.7 * 4.4482216),
                     "ratio_card_775_to_NG2": 775 / (121.7 * 4.4482216)}
    # ---------------- 4. light frame requirements
    sec4 = {}
    k5 = sec1["K13D2U-50-20-20-10"]
    for R in RADII:
        for svc, dk in (("ground", 0.0), ("one", inc[R][0]), ("seven", inc[R][1])):
            p, t, _ = payload(R, "K13D2U-50-20-20-10", 1.0)
            p -= dk
            fmax = 1 + p / t
            row = {"payload": p, "fmax": fmax}
            for pk, pkv in (("cg", k5["peak_cg_GPa"]), ("fe", k5["peak_fe_GPa"])):
                lam_need = pkv / fmax
                row[f"lam_mean_{pk}"] = lam_need
                row[f"UD_mean_{pk}"] = lam_need * k5["ratio"]
                for tag in ("cv52", "cv6"):
                    m = k5[f"m_{tag}"]
                    kk = k5[f"k_{tag}"]
                    scale_need = kk * pkv / fmax
                    row[f"UD_Pf_{tag}_{pk}"] = scale_need * gam(m) * k5["ratio"]
                    vt = k5["member_volume_cm3"] * 1e-6 * fmax
                    row[f"UD_Pf_size_{tag}_{pk}"] = scale_need * gam(m) * k5["ratio"] / (V_COUPON / vt) ** (1 / m)
                row[f"scale_m20_{pk}"] = interp_k(k5["k"], 20) * pkv / fmax
            sec4[f"{R}:{svc}"] = row
    out["sec4"] = sec4
    # ---------------- hail
    vol = math.pi / 6 * 0.0508 ** 3
    ke = {str(rho): 0.5 * rho * vol * 32.0 ** 2 for rho in (810, 900, 920)}
    t = np.array([1.59, 3.11, 4.66])
    e = np.array([254.0, 453.0, 666.0])
    slope, icpt = np.polyfit(t, e, 1)
    hail = {"KE_J": ke, "Kim_1p59_lower_J": 254.0, "ratio_254_to_upper": 254.0 / ke["920"],
            "fit_J_per_mm": slope, "fit_intercept_J": icpt, "threshold_1p45_J": icpt + slope * 1.45,
            "ratio_1p45_to_upper": (icpt + slope * 1.45) / ke["920"], "ratio_1p45_to_mid": (icpt + slope * 1.45) / ke["900"],
            "greenfeld_implied_density": 29.80 / (0.5 * 32.0 ** 2 * math.pi / 6 * 0.051 ** 3)}
    hrows = list(csv.DictReader(open(D51 / "HAIL-DESIGN.csv")))
    sh = {r["material"]: float(r["stress_Shi_MPa"]) for r in hrows if r["reserve"] == "019" and r["section_policy"] == "verified_q1_1"}
    m70 = sec1["M55J-70-10-10-10"]
    pts = sorted({(float(r["wall_mm"]), float(r["stress_Shi_MPa"])) for r in hrows if r["material"] == "M55J-70-10-10-10" and r["reserve"] == "019"})
    lw = np.log([p[0] for p in pts]); ls = np.log([p[1] for p in pts])
    expo, c0 = np.polyfit(lw, ls, 1)
    f70 = m70["wall_Pf_cv6_cg"]
    s70 = math.exp(c0 + expo * math.log(m70["wall_mm"] * f70))
    left70 = m70["lam_mean_GPa"] * 1000 - m70["peak_cg_GPa"] * 1000 / f70
    m50 = sec1["M55J-50-20-20-10"]
    left50 = m50["lam_mean_GPa"] * 1000 - m50["peak_cg_GPa"] * 1000
    hail.update({"Shi_K13D2U-50_MPa": sh["K13D2U-50-20-20-10"], "Shi_M55J-50_MPa": sh["M55J-50-20-20-10"],
                 "M55J-50_left_MPa": left50, "M55J-50_exceed": sh["M55J-50-20-20-10"] / left50,
                 "M55J-70_Pf_wall_mm": m70["wall_mm"] * f70, "M55J-70_Shi_at_Pf_wall_MPa": s70, "M55J-70_left_MPa": left70,
                 "M55J-70_fraction": s70 / left70, "M55J-70_power_exponent": expo})
    out["hail"] = hail
    OUT.write_text(json.dumps(out, indent=1, default=float))
    # ---------------- print comparison
    for cid, r in sec1.items():
        c = r["card"]
        print(f"{cid:20s} ratio {r['ratio']:.4f} (051 {r['ratio_051']:.4f}, card {c['ratio']}) lam {r['lam_mean_GPa']:.4f} ({c['lam_mean']}) "
              f"tubes {r['tubes_kg']:.1f} ({c['tubes']}) peak {r['peak_cg_GPa']:.4f}/{r['peak_fe_GPa']:.4f} ({c['peak']}) SF {r['mean_SF']:.4f} ({c['mean_SF']}) "
              f"wmean {r['wall_mean']:.3f} ({c['wall_mean']}) wPf52 {r['wall_Pf_cv52_cg']:.3f}/{r['wall_Pf_cv52_fe']:.3f} ({c['wall_cv52']}) "
              f"wPf6 {r['wall_Pf_cv6_cg']:.3f}/{r['wall_Pf_cv6_fe']:.3f} ({c['wall_cv6']}) size6 {r['wall_Pf_size_cv6_cg']:.3f}/{r['wall_Pf_size_cv6_fe']:.3f} ({c['wall_size_cv6']}) "
              f"Pf6 {r['Pf_witness_cv6_cg']:.3g}/{r['Pf_witness_cv6_fe']:.3g} ({c['Pf_witness']}) sizefac6 {r['size_factor_cv6']:.3f} k6 {r['k_cv6']:.4f} k52 {r['k_cv52']:.4f}")
    print("first ply", json.dumps(out["first_ply"], default=float))
    for k, v in sec2.items():
        print("sec2", k, v if not isinstance(v, dict) else {a: round(b, 1) for a, b in v.items()})
    print("float limit", {k: round(v, 4) for k, v in out["float_limit_tube_multiplier"].items()}, "tube mult",
          {k: round(v, 4) for k, v in out["tube_multiplier"].items()})
    print("joints", json.dumps(out["joints"], default=lambda x: round(float(x), 2)))
    print("cavity", {k: (round(a, 3), round(b, 3)) for k, (a, b) in out["dry_cavity_increments_kg"].items()})
    for k, v in sec4.items():
        print("sec4", k, {a: round(b, 4) for a, b in v.items()})
    print("hail", json.dumps(hail, default=float))


if __name__ == "__main__":
    main()
