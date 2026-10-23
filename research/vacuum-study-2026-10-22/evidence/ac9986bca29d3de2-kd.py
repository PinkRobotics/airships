#!/usr/bin/env python3
"""MAINLINE-015. Knockdown against shape precision.

Own arithmetic. The glm compute.py and the 014b honeycomb.py are not executed.
Formulas are stated here. Nothing is a certification.
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parent
T0 = datetime.now(ZONE).isoformat(timespec="seconds")

# Case, COMMON.md. Full atmosphere pin, same value the 014b card used.
R = 10.0
P_EXT = 95460.83791390515
LIFT = 4889.442150186961
E_AL = 68.9e9
NU = 0.33
SYSTEMS = 100.0
JOINT = 0.05
AREA = 4.0 * math.pi * R * R
M_STRUCT = (LIFT - SYSTEMS) / (1.0 + JOINT)

# 002/003 rows, as carried by the partial (tf, core depth).
ROWS_002 = {
    "P2": (0.0002, 0.1),
    "P2-A": (0.000375893644493, 0.1),
    "P2-C": (0.0002, 0.159364105016),
    "P2-K": (0.000270882513452, 0.135441256726),
    "P2-E": (0.000336094970395, 0.113432052508),
}

# 014 filed separations h = core + tf, kd 0.20 optima, HRH-10-4.8-32 except as named.
# Taken from that card's RESULTS optima, not recomputed. Crimp branch, gamma = 1.
H_014 = {
    "014-CNT-HRH10": 0.024508453356494708,
    "014-graphene-HRH10": 0.02208325446776471,
    "014-Be-HRH10": 0.022543516772786033,
}

# Beryllium S-200F, 008 candidate row. QUESTIONABLE.
BE = {"E_Pa": 303.0e9, "sigma_Pa": 283.0e6, "rho": 1850.0}
# Hexcel CR-III 5056, 1/4-1.6 and 3/8-1.6. Same sheet moduli, W shear is Gc.
# Typical columns: Ec 30 ksi, crush 50 psi, W modulus 10.5 ksi. QUESTIONABLE.
PSI = 6894.757293168361
KSI = PSI * 1000.0
PCF_TO_KG = 0.45359237 / (0.3048 ** 3)
K_HONEY = 0.33
GRID = 8000
CRIII_5056_1_6 = {
    "name": "Hexcel CR-III 5056 1.6 pcf",
    "rho": 1.6 * PCF_TO_KG,
    "Ec_Pa": 30.0 * KSI,
    "Gc_Pa": 10.5 * KSI,
    "crush_Pa": 50.0 * PSI,
    "cells_m": {"1/4": 0.0254 / 4.0, "3/8": 0.0254 * 3.0 / 8.0},
}

# Sourced curve coefficients. QUESTIONABLE. Carried from the partial's stated fits.
# Baizhikova 2026 Eq 3, lambda_I = 1, R/t 100-1550: kappa = 0.45 + 0.51 exp(-3.88 delta_bar).
K0, A_EQ, B_EQ = 0.45, 0.51, 3.88
# Jimenez 2017 plateau: rho = (1-b)(1+k)^a + b, worst width k = 2.625.
A_JIM, B_JIM, K_WORST = -1.23, 0.036, 2.625
# NASA SP-8032 form quoted by Hutchinson-Thompson 2018.
# PNAS 2024 design fit, verified against their printed 0.278 and 0.320.
PNAS = {"k0": 0.235, "m": 3.39, "s": 1.24, "N0": 20.0, "r": 2.0, "N100": 90.0}

LEVELS = (0.2, 0.3, 0.5, 0.7, 0.9)
MFG = {
    "GBT panels 50 um": 50e-6,
    "DVA-C panels 200 um": 200e-6,
    "SKA-1 260 um": 260e-6,
    "GBT assembled 250 um": 250e-6,
    "MeerKAT 900 um": 900e-6,
    "UG-81 inside 125 mm": 0.00625 * 20.0,
    "UG-81 outside 250 mm": 0.0125 * 20.0,
}


def half_up(value: float, places: int) -> str:
    quant = Decimal("1").scaleb(-places)
    return str(Decimal(format(value, ".20f")).quantize(quant, rounding=ROUND_HALF_UP))


def biaxial() -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if mid ** 3 + mid > 1.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


BIAX = biaxial()


def kappa_eq3(delta_bar: float) -> float:
    return K0 + A_EQ * math.exp(-B_EQ * delta_bar)


def delta_bar_eq3(kappa: float):
    ratio = (kappa - K0) / A_EQ
    if ratio <= 0.0 or ratio >= 1.0:
        return None
    return -math.log(ratio) / B_EQ


def rho_plateau(k: float) -> float:
    return (1.0 - B_JIM) * (1.0 + k) ** A_JIM + B_JIM


def nasa(r_over_t: float) -> float:
    return 1.0 - 0.901 * (1.0 - math.exp(-math.sqrt(r_over_t) / 16.0))


def pnas_design(r_over_t: float, p0: float) -> float:
    m = PNAS["m"]
    return (
        PNAS["k0"]
        + PNAS["s"]
        * (p0 ** (1.0 / m))
        * ((20.0 * math.pi / 7.0) ** (-1.0 / m))
        * (r_over_t ** (-1.0 / (2.0 * m)))
    )


def t_eq_of(h: float) -> float:
    """sqrt(3)*(d+tf). Matches i^2, not the bending-only thickness."""
    return math.sqrt(3.0) * h


def widths(t_eq: float) -> dict:
    # Sources use nu = 0.3 in the Koga-Hoff width. Stated, not the face's 0.33.
    g = R / t_eq
    root = (12.0 * (1.0 - 0.3 ** 2)) ** 0.25 * math.sqrt(g)
    beta_l1 = 1.0 / root
    beta_w = K_WORST / root
    rt = math.sqrt(R * t_eq)
    return {
        "sqrt_R_t_eq_m": rt,
        "width_lambda_I_1_m": R * beta_l1,
        "width_worst_m": R * beta_w,
        "beta0_lambda_I_1_rad": beta_l1,
        "beta0_worst_rad": beta_w,
        "l_c_m": 2.0 * math.pi * (12.0 * (1.0 - 0.3 ** 2)) ** (-0.25) * rt,
    }


def rms_mm(delta_m: float, beta0: float) -> float:
    """Single Gaussian dimple, small angle. RMS = delta * beta0 / sqrt(8)."""
    return delta_m * beta0 / math.sqrt(8.0) * 1000.0


def shell_block(name: str, h: float, tf: float | None, core: float | None) -> dict:
    t_eq = t_eq_of(h)
    w = widths(t_eq)
    i_sand = h ** 2 / 4.0
    i_mono = t_eq ** 2 / 12.0
    block = {
        "h_m": h,
        "tf_m": tf,
        "core_m": core,
        "t_eq_m": t_eq,
        "R_over_t_eq": R / t_eq,
        "i2_sandwich_m2": i_sand,
        "i2_monocoque_m2": i_mono,
        "i2_match": abs(i_sand - i_mono) < 1e-15,
        "widths": w,
        "one_thickness_mm": t_eq * 1000.0,
        "levels": {},
    }
    for kd in LEVELS:
        dbar = delta_bar_eq3(kd)
        if dbar is None:
            block["levels"][f"{kd:.1f}"] = {
                "status": "below_eq3_floor_0.45",
                "delta_bar_lambda1": None,
                "amplitude_upper_bound_mm": t_eq * 1000.0,
                "bound": "below one t_eq; worst-width one-thickness statement puts kd near 0.20-0.25 at delta = t_eq",
                "rms_at_one_thickness_worst_mm": rms_mm(t_eq, w["beta0_worst_rad"]),
            }
        else:
            delta = dbar * t_eq
            block["levels"][f"{kd:.1f}"] = {
                "status": "lambda_I_1_inversion",
                "delta_bar_lambda1": dbar,
                "amplitude_mm": delta * 1000.0,
                "rms_worst_single_mm": rms_mm(delta, w["beta0_worst_rad"]),
                "rms_narrow_single_mm": rms_mm(delta, w["beta0_lambda_I_1_rad"]),
            }
    g = R / t_eq
    n_scaled = PNAS["N100"] * math.sqrt(g / 100.0)
    block["cross"] = {
        "nasa_kd": nasa(g),
        "R_over_800_mm": R / 800.0 * 1000.0,
        "kappa_eq3_at_R_over_800": kappa_eq3((R / 800.0) / t_eq),
        "pnas_N": n_scaled,
        "pnas_mean": PNAS["k0"] * math.sqrt(1.0 + PNAS["N0"] / n_scaled),
        "pnas_design_1e-3": pnas_design(g, 1e-3),
        "pnas_design_1e-2": pnas_design(g, 1e-2),
    }
    return block


def modes(tf: float, tc: float, kd: float, s_cell: float) -> dict:
    """014b reading of CR-1457, plus honeycomb wrinkling and intracell dimpling."""
    h = tc + tf
    root = math.sqrt(1.0 - NU * NU)
    young = BE["E_Pa"]
    sigma_0 = young * h / (R * root)
    sigma_crimp = h * h * CRIII_5056_1_6["Gc_Pa"] / (2.0 * tf * tc)
    vc = sigma_0 / sigma_crimp
    if vc <= 2.0:
        kc = 1.0 - vc / 4.0
        gamma = kd
        branch = "stiff_or_moderate_core"
    else:
        kc = 1.0 / vc
        gamma = 1.0
        branch = "shear_crimping"
    membrane = P_EXT * R / (4.0 * tf)
    sfs = {
        "global_buckling": (4.0 * gamma * kc * sigma_0 * tf / R) / P_EXT,
        "face_yield": (4.0 * BE["sigma_Pa"] * tf / R) / P_EXT,
        "core_shear_crimping": (4.0 * sigma_crimp * tf / R) / P_EXT,
        "core_crush": CRIII_5056_1_6["crush_Pa"] / (P_EXT / 2.0),
    }
    uni = K_HONEY * young * math.sqrt(CRIII_5056_1_6["Ec_Pa"] * tf / (young * tc))
    sfs["face_wrinkling"] = BIAX * uni / membrane
    sigma_d = 2.0 * young / (1.0 - NU * NU) * (tf / s_cell) ** 2
    sfs["intracell_dimpling"] = sigma_d / membrane
    ordered = sorted(sfs.items(), key=lambda item: (item[1], item[0]))
    return {
        "tf_m": tf,
        "core_m": tc,
        "h_m": h,
        "Vc": vc,
        "Kc": kc,
        "gamma": gamma,
        "branch": branch,
        "sfs": sfs,
        "governing": ordered[0][0],
        "least_SF": ordered[0][1],
        "second_mode": ordered[1][0],
        "second_SF": ordered[1][1],
    }


def optimize(kd: float, s_cell: float) -> dict:
    best = None
    rho = CRIII_5056_1_6["rho"]
    for step in range(1, GRID):
        fraction = step / GRID
        tc = (fraction * M_STRUCT) / (AREA * rho)
        tf = ((1.0 - fraction) * M_STRUCT) / (2.0 * AREA * BE["rho"])
        ev = modes(tf, tc, kd, s_cell)
        key = (ev["least_SF"], ev["second_SF"])
        if best is None or key > best["key"]:
            best = {"key": key, "fraction": fraction, "ev": ev}
    ev = best["ev"]
    ev["core_mass_fraction"] = best["fraction"]
    return ev


def shear_reduction(e_face: float, tf: float, gc: float) -> dict:
    """Classical sandwich pressure with a shear-flexible mode at l_c.
    p_cr/p_c = (1 + E*tf*sqrt(1-nu^2)/(Gc*R))^(-1/2). DERIVED, QUESTIONABLE.
    """
    ds = e_face * tf * math.sqrt(1.0 - NU * NU) / (gc * R)
    ratio = (1.0 + ds) ** -0.5
    return {"delta_shear": ds, "p_cr_over_p_c": ratio, "reduction": 1.0 - ratio}


def gap_row(amp_mm: float | None, rms_mm_value: float | None) -> dict:
    out = {}
    for name, achieved in MFG.items():
        out[name] = {
            "achieved_m": achieved,
            "amplitude_over_achieved": None if amp_mm is None else (amp_mm / 1000.0) / achieved,
            "rms_over_achieved": None if rms_mm_value is None else (rms_mm_value / 1000.0) / achieved,
        }
    return out


def main() -> None:
    checks = []
    shells = {}
    for name, (tf, core) in ROWS_002.items():
        shells[name] = shell_block(name, core + tf, tf, core)
        if name == "P2-E":
            tf_e, d_e = tf, core
            t_bend = (6.0 * tf_e * d_e ** 2) ** (1.0 / 3.0)
            lam = 2.0 * (12.0 * (1.0 - NU * NU)) ** 0.25 * math.sqrt(R / t_bend)
            p_sand = 4.0 * tf_e * (d_e + tf_e) * E_AL / (R ** 2 * math.sqrt(1.0 - NU * NU))
            t_eq = shells[name]["t_eq_m"]
            p_zoelly = 2.0 * E_AL * t_eq ** 2 / (R ** 2 * math.sqrt(3.0 * (1.0 - NU * NU)))
            shells[name]["transfer"] = {
                "t_eq_bending_only_m": t_bend,
                "t_eq_over_bending": t_eq / t_bend,
                "lambda_004b_convention": lam,
                "lambda_sealed": 66.4045460271,
                "p_sandwich_Pa": p_sand,
                "p_zoelly_at_t_eq_Pa": p_zoelly,
                "p_sandwich_over_zoelly": p_sand / p_zoelly,
                "zoelly_over_sandwich": p_zoelly / p_sand,
            }
    for name, h in H_014.items():
        shells[name] = shell_block(name, h, None, None)
        shells[name]["note"] = "014 optimum on the crimp branch; gamma = 1, so kd does not enter the governing factor"

    s_cell = CRIII_5056_1_6["cells_m"]["1/4"]
    s_38 = CRIII_5056_1_6["cells_m"]["3/8"]
    be_frozen = optimize(0.20, s_cell)
    be_38 = optimize(0.20, s_38)
    be_at_03 = optimize(0.30, s_cell)
    # Frozen geometry, kd raised with the mass split held.
    frozen_scan = {}
    for kd in (0.20, 0.2991102504185387, 0.30):
        frozen_scan[f"{kd:.4f}"] = modes(be_frozen["tf_m"], be_frozen["core_m"], kd, s_cell)
    # Re-optimised least versus kd. First grid point at or above 1, and the point below.
    crossing = None
    prev = None
    for step in range(200, 1001):
        kd = step / 1000.0
        ev = optimize(kd, s_cell)
        row = {"kd": kd, "least_SF": ev["least_SF"], "governing": ev["governing"], "h_m": ev["h_m"], "tf_m": ev["tf_m"], "core_m": ev["core_m"]}
        if ev["least_SF"] >= 1.0:
            crossing = {"first_at_or_above_1": row, "previous": prev}
            break
        prev = row

    be_shell = shell_block("014b-Be-CRIII-1.6", be_frozen["h_m"], be_frozen["tf_m"], be_frozen["core_m"])
    shells["014b-Be-CRIII-1.6"] = be_shell

    # Core shear. P2-E against the partial's three catalog moduli, and the aluminium core.
    tf_e, d_e = ROWS_002["P2-E"]
    shear = {
        "P2-E": {
            "Gc_9e6": shear_reduction(E_AL, tf_e, 9.0e6),
            "Gc_14e6": shear_reduction(E_AL, tf_e, 14.0e6),
            "Gc_137.9e6": shear_reduction(E_AL, tf_e, 137.895145863e6),
        },
        "014b-Be-CRIII": shear_reduction(BE["E_Pa"], be_frozen["tf_m"], CRIII_5056_1_6["Gc_Pa"]),
    }

    # Other drivers, at P2-E and at the aluminium point.
    def drivers(tf: float, h: float, t_eq: float) -> dict:
        out = {
            "thickness_dpc_over_pc_per_face": 1.0 + tf / h,
            "hydrostatic_Pa": 1.225 * 9.80665 * 2.0 * R,
        }
        out["hydrostatic_over_p"] = out["hydrostatic_Pa"] / P_EXT
        seams = {}
        for mm in (1.0, 3.0, 10.0):
            dbar = (mm / 1000.0) / t_eq
            seams[f"{mm:g}mm"] = {"delta_bar": dbar, "kappa_eq3": kappa_eq3(dbar)}
        out["seam_step_narrow_branch"] = seams
        return out

    driver = {
        "P2-E": drivers(tf_e, tf_e + d_e, shells["P2-E"]["t_eq_m"]),
        "014b-Be-CRIII": drivers(be_frozen["tf_m"], be_frozen["h_m"], be_shell["t_eq_m"]),
    }

    gaps = {}
    for label in ("P2-E", "014b-Be-CRIII-1.6"):
        gaps[label] = {}
        for kd in LEVELS:
            level = shells[label]["levels"][f"{kd:.1f}"]
            if level["delta_bar_lambda1"] is None:
                gaps[label][f"{kd:.1f}"] = {
                    "note": "no sourced amplitude; upper bound is one t_eq, and the true allowance is smaller",
                    "bound": gap_row(level["amplitude_upper_bound_mm"], level["rms_at_one_thickness_worst_mm"]),
                }
            else:
                gaps[label][f"{kd:.1f}"] = gap_row(level["amplitude_mm"], level["rms_worst_single_mm"])

    target = 0.668649769508548
    checks.append({"name": "i2 match P2-E", "pass": shells["P2-E"]["i2_match"]})
    checks.append({
        "name": "014b Be CR-III 1.6 least SF reproduces 0.668649769508548",
        "pass": be_frozen["least_SF"] == target,
        "got": be_frozen["least_SF"],
    })
    checks.append({
        "name": "1/4 and 3/8 cell tie on the least factor",
        "pass": be_38["least_SF"] == be_frozen["least_SF"] and abs(be_38["tf_m"] - be_frozen["tf_m"]) < 1e-15,
    })
    checks.append({
        "name": "PNAS 0.278 at R/t 100, P0 1e-3, within 0.003",
        "pass": abs(pnas_design(100.0, 1e-3) - 0.278) < 0.003,
        "got": pnas_design(100.0, 1e-3),
    })
    checks.append({
        "name": "PNAS 0.320 at R/t 100, P0 1e-2, within 0.003",
        "pass": abs(pnas_design(100.0, 1e-2) - 0.320) < 0.003,
        "got": pnas_design(100.0, 1e-2),
    })
    lam = shells["P2-E"]["transfer"]["lambda_004b_convention"]
    checks.append({
        "name": "004b lambda reproduced within 1 percent",
        "pass": abs(lam - 66.4045460271) / 66.4045460271 < 0.01,
        "got": lam,
    })
    checks.append({
        "name": "Eq 3 cannot invert kd 0.3 or 0.2",
        "pass": delta_bar_eq3(0.3) is None and delta_bar_eq3(0.2) is None,
    })

    display = {
        "P2-E_t_eq_m": half_up(shells["P2-E"]["t_eq_m"], 6),
        "P2-E_R_over_t": half_up(shells["P2-E"]["R_over_t_eq"], 2),
        "P2-E_wavelength_m": half_up(shells["P2-E"]["widths"]["sqrt_R_t_eq_m"], 3),
        "Be_tf_mm": half_up(be_frozen["tf_m"] * 1000.0, 3),
        "Be_core_mm": half_up(be_frozen["core_m"] * 1000.0, 2),
        "Be_t_eq_mm": half_up(be_shell["t_eq_m"] * 1000.0, 2),
        "Be_R_over_t": half_up(be_shell["R_over_t_eq"], 1),
        "Be_wavelength_m": half_up(be_shell["widths"]["sqrt_R_t_eq_m"], 3),
        "kd_global_SF1": half_up(0.20 / be_frozen["sfs"]["global_buckling"], 4),
        "wrinkling_SF": half_up(be_frozen["sfs"]["face_wrinkling"], 4),
        "least_at_kd_0_3_reopt": half_up(be_at_03["least_SF"], 4),
        "plateau_worst": half_up(rho_plateau(K_WORST), 4),
        "plateau_lambda1": half_up(rho_plateau(1.0), 4),
        "zoelly_over_sandwich": half_up(shells["P2-E"]["transfer"]["zoelly_over_sandwich"], 1),
    }
    for label, places in (("P2-E", (2, 1, 0, 2, 1, 1)), ("014b-Be-CRIII-1.6", (2, 2, 2, 2, 2, 2))):
        for kd, p_amp in zip((0.9, 0.7, 0.5), places[:3]):
            level = shells[label]["levels"][f"{kd:.1f}"]
            display[f"{label}_kd{kd}_amp_mm"] = half_up(level["amplitude_mm"], p_amp)
            display[f"{label}_kd{kd}_rms_mm"] = half_up(level["rms_worst_single_mm"], 2)

    out = {
        "schema": 1,
        "card": "MAINLINE-015",
        "unit": "vacuum-mainline015-kd-precision-1019",
        "started_at": T0,
        "ended_at": datetime.now(ZONE).isoformat(timespec="seconds"),
        "certification": False,
        "tag": "QUESTIONABLE",
        "biaxial_factor": BIAX,
        "structural_mass_kg": M_STRUCT,
        "plateau": {
            "k_1": rho_plateau(1.0),
            "k_worst_2_625": rho_plateau(K_WORST),
            "eq3_floor": K0,
        },
        "shells": shells,
        "be_aluminium": {
            "density_kg_m3": CRIII_5056_1_6["rho"],
            "Gc_Pa": CRIII_5056_1_6["Gc_Pa"],
            "Ec_Pa": CRIII_5056_1_6["Ec_Pa"],
            "frozen_kd_0_20": be_frozen,
            "cell_3_8_least_SF": be_38["least_SF"],
            "kd_for_global_SF_1": 0.20 / be_frozen["sfs"]["global_buckling"],
            "frozen_at_raised_kd": frozen_scan,
            "reoptimised_at_kd_0_30": be_at_03,
            "reoptimised_SF1_crossing": crossing,
            "note": "Wrinkling has no kd. The frozen least factor does not follow the global mode up to 1.",
        },
        "core_shear": shear,
        "drivers": driver,
        "gaps_required_over_achieved": gaps,
        "display_half_up": display,
        "checks": checks,
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    failed = [c for c in checks if not c["pass"]]
    print("checks", len(checks), "failed", len(failed))
    for c in checks:
        print(("PASS " if c["pass"] else "FAIL ") + c["name"])
    print("display", json.dumps(display, indent=1))
    print("crossing", json.dumps(crossing, indent=1)[:800])
    print("reopt 0.3 least", be_at_03["least_SF"], be_at_03["governing"], "h", be_at_03["h_m"])
    print("shear Be", shear["014b-Be-CRIII"]["reduction"])
    print("wrote", ROOT / "RESULTS.json")


if __name__ == "__main__":
    main()
