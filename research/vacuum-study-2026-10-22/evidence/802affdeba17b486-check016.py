#!/usr/bin/env python3
"""MAINLINE-016 check. Own arithmetic. Does not call the owner's script.

Formulas are the ones stated in the card's INPUTS.json. Inherited geometry,
lift and the five mode factors are compared with MAINLINE-009's RESULTS,
not recomputed. Display rounding is half-up.
"""

import json
import math
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

OWN = Path(
    "unpublished-local-ref:e03f642454878b9b"
    "/.ship/work/outputs/ref-81587374594cae9c1e2e-nfi-1019"
)
NINE = Path(
    "unpublished-local-ref:7f7c51a246885c2d"
    "/.ship/work/outputs/vacuum-mainline009-combined-point-1019/RESULTS.json"
)

R = 10.0
P_EXT = 95460.83791390515
T_AIR = 284.9
RHO_AIR = 1.1672683307461802
LIFT = 4889.442150186961
MARGIN = 244.47210750934846
TF = 0.00027215364631557974
TC = 0.04624190488644608
ALLOW = 216.4271448894101
CORE_KG = 2208.1530759247057
RHO_SIC = 3100.0
E_SIC = 410e9
A = 4.0 * math.pi * R * R
V = 4.0 / 3.0 * math.pi * R ** 3

R_AIR = 287.05
M_AIR = 0.02897
R_V = 461.5
GAMMA = 1.4
MU = 1.79e-5
K_AIR = 0.0257
PR = 0.71
SOLAR = 970.0
SIGMA_SB = 5.670374419e-8
P_STD = 101325.0
MOLAR_SCC = 22414.0
GC_CORE = 12e6
ALPHA_SIC = 4.5e-6
ALPHA_PVC = 60e-6
K_CORE = 0.030
CP_CORE = 1300.0
RHO_CORE = 38.0
CD = 0.47
GUST = 1.4
PATCH = 0.0707
CRUSH_KPA = 500.0
WATER = 1000.0


def half_up(value, nd):
    q = Decimal(1).scaleb(-nd)
    return Decimal(format(value, ".20f")).quantize(q, rounding=ROUND_HALF_UP)


def display_equal(token, value):
    if "e" in token.lower():
        mant, exp = token.lower().split("e")
        exp = int(exp)
        nd = len(mant.split(".")[1]) if "." in mant else 0
        scaled = value / (10 ** exp)
        text = f"{half_up(scaled, nd)}e{exp}"
        return text.replace("+", "") == token.lower().replace("+", "")
    nd = len(token.split(".")[1]) if "." in token else 0
    rounded = half_up(value, nd)
    text = format(rounded, "f").split(".")[0] if nd == 0 else format(rounded, f".{nd}f")
    return text == token


def choked_flux(p, t):
    # Upstream stagnation into vacuum. Stated: p*sqrt(gamma/(R T))*(2/(gamma+1))**((gamma+1)/(2(gamma-1)))
    expo = (GAMMA + 1.0) / (2.0 * (GAMMA - 1.0))
    return p * math.sqrt(GAMMA / (R_AIR * t)) * (2.0 / (GAMMA + 1.0)) ** expo


def thermal_balance(alpha, eps, sky, wind, solar):
    """Stated balance. T_env averages sky and air. Whitaker as stated, no viscosity ratio."""
    diameter = 2.0 * R
    re = RHO_AIR * wind * diameter / MU
    nu = 2.0 + (0.4 * re ** 0.5 + 0.06 * re ** (2.0 / 3.0)) * PR ** 0.4
    h = nu * K_AIR / diameter
    t_env = 0.5 * (sky + T_AIR)
    absorbed = alpha * solar / 4.0

    def residual(temp):
        rad = eps * SIGMA_SB * (temp ** 4 - t_env ** 4)
        conv = h * (temp - T_AIR)
        return rad + conv - absorbed

    lo, hi = 200.0, 500.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if residual(mid) > 0.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi), h


def rad_only(alpha, eps, sky, solar):
    t_env = 0.5 * (sky + T_AIR)
    t4 = t_env ** 4 + alpha * solar / (4.0 * eps * SIGMA_SB)
    return t4 ** 0.25


def seam(width, optimistic):
    length = 2.0 * A / width
    b = 0.06 if optimistic else 0.12
    t_adh = 0.0002 if optimistic else 0.0003
    t_splice = 0.0015 if optimistic else 0.0030
    doubler = length * b * TF * RHO_SIC
    adhesive = length * b * t_adh * 1250.0
    splice = length * TC * t_splice * 1100.0
    total = doubler + adhesive + splice
    return {
        "seam_length_m": length,
        "doubler_kg": doubler,
        "adhesive_kg": adhesive,
        "core_splice_kg": splice,
        "total_kg": total,
        "pct_of_5pct_allowance": 100.0 * total / ALLOW,
        "margin_after_kg": MARGIN + ALLOW - total,
    }


def isa_rho(h, rspec):
    t0 = 288.15
    lapse = 0.0065
    g0 = 9.80665
    p0 = 101325.0
    temp = t0 - lapse * h
    expo = g0 / (lapse * rspec)
    pressure = p0 * (temp / t0) ** expo
    return pressure / (rspec * temp), pressure, temp


def main():
    theirs = json.loads((OWN / "RESULTS.json").read_text())
    inputs = json.loads((OWN / "INPUTS.json").read_text())
    nine = json.loads(NINE.read_text())
    mismatches = []

    def check(row, field, card, mine, tol=1e-9):
        scale = max(abs(card), abs(mine), 1e-30)
        rel = abs(card - mine) / scale
        if rel > tol:
            mismatches.append((row, field, card, mine, rel))
        return rel

    print("area", A, "volume", V)
    check("geometry", "A", theirs["base_point"]["A_m2"], A, 0.0)
    check("geometry", "V", theirs["base_point"]["V_m3"], V, 1e-15)

    # Inherited 009 pins, not recomputed.
    modes = theirs["base_point"]["modes_main_kd_0_20"]
    print("009 least", nine["least_SF_main"])
    check("009 pin", "least", modes["global_buckling"], nine["least_SF_main"], 0.0)
    check("009 pin", "margin", theirs["base_point"]["margin_kg"], nine["float"]["payload_kg"], 0.0)
    check("009 pin", "tf", theirs["base_point"]["tf_m"], nine["geometry"]["tf_m"], 0.0)
    check("009 pin", "core", theirs["base_point"]["core_m"], nine["geometry"]["core_m"], 0.0)
    for key, value in nine["modes_main_kd_0_20"].items():
        check("009 pin", key, modes[key], value, 0.0)

    lift_1 = 0.01 * LIFT
    p_int = 0.01 * P_EXT
    q_allow = V * p_int / 86400.0
    m_rate = q_allow / (R_AIR * T_AIR)
    flux = choked_flux(P_EXT, T_AIR)
    a_choke = m_rate / flux
    vbar = math.sqrt(8.0 * R_AIR * T_AIR / math.pi)
    a_mol = 4.0 * q_allow / (P_EXT * vbar)
    d_hole = 2.0 * math.sqrt((a_choke) / math.pi)
    print("leak", lift_1, p_int, q_allow, m_rate, a_choke * 1e6, a_mol * 1e6, "d_mm", d_hole * 1e3, "flux", flux)
    vac = theirs["item1_vacuum"]
    check("vacuum", "lift_1pct", vac["lift_1pct_kg_per_day"], lift_1, 0.0)
    check("vacuum", "p_int", vac["p_int_at_1pct_Pa"], p_int, 0.0)
    check("vacuum", "Q", vac["Q_allow_Pa_m3_s"], q_allow, 1e-15)
    check("vacuum", "m_rate", vac["m_rate_allow_kg_s"], m_rate, 1e-12)
    check("vacuum", "A_choke_mm2", vac["A_choked_equivalent_mm2"], a_choke * 1e6, 1e-12)
    check("vacuum", "A_mol_mm2", vac["A_molecular_equivalent_mm2"], a_mol * 1e6, 1e-12)
    check("vacuum", "flux", vac["choked_flux_kg_s_m2"], flux, 1e-12)

    # Permeance: stated n_dot = permeance * A * dp, scc = 1/22414 mol, air = helium/50.
    # dp is the external pressure as a fraction of 1 atm.
    perm = []
    for permeance in (1e-6, 1e-5):
        scc_s = (permeance / 50.0) * A * (P_EXT / P_STD)
        kg_s = scc_s / MOLAR_SCC * M_AIR
        perm.append(kg_s * 86400.0)
    print("permeation kg/day", perm)
    got = vac["permeation"][2]["kg_per_day"]
    check("permeation", "lo", got[0], perm[0], 1e-12)
    check("permeation", "hi", got[1], perm[1], 1e-12)
    pct = [100.0 * x / lift_1 for x in perm]
    check("permeation", "pct_hi", vac["permeation"][2]["pct_of_1pct_budget"][1], pct[1], 1e-12)

    out_q = [rate * A for rate in (1e-7, 1e-5)]
    print("outgas Q", out_q, "pct", [100.0 * q / q_allow for q in out_q])
    check("outgas", "lo", vac["outgassing_Q_Pa_m3_s"][0], out_q[0], 1e-12)
    check("outgas", "hi", vac["outgassing_Q_Pa_m3_s"][1], out_q[1], 1e-12)

    moist = [frac * CORE_KG for frac in (0.005, 0.03)]
    moist_p = [m * R_V * T_AIR / V for m in moist]
    print("moisture", moist, moist_p)
    check("moisture", "kg_lo", vac["moisture_kg_band"][0], moist[0], 1e-12)
    check("moisture", "p_hi", vac["moisture_pressure_if_released_Pa"][1], moist_p[1], 1e-12)

    vdot = q_allow / 1000.0
    w_ideal = q_allow * math.log(P_EXT / 1000.0)
    w_real = [w_ideal / eff for eff in (0.25, 0.40)]
    pumpdown_j = P_EXT * V * math.log(P_EXT / 1000.0)
    pumpdown_kwh = pumpdown_j / 3.6e6
    pct_m = [100.0 * m / MARGIN for m in (150.0, 400.0)]
    print("pump", vdot, w_ideal, w_real, pumpdown_kwh, pct_m)
    check("pump", "vdot", vac["pump"]["vdot_m3_s"], vdot, 1e-15)
    check("pump", "W", vac["pump"]["W_ideal"], w_ideal, 1e-12)
    check("pump", "W25", vac["pump"]["W_real_band_W"][0], w_real[0], 1e-12)
    check("pump", "W40", vac["pump"]["W_real_band_W"][1], w_real[1], 1e-12)
    check("pump", "kWh", vac["deploy_pumpdown_kWh"], pumpdown_kwh, 1e-12)
    check("pump", "pct150", vac["pump"]["pct_of_margin"][0], pct_m[0], 1e-12)

    seams = {}
    for width, name in ((4.0, "w4"), (2.0, "w2"), (0.5, "w05"), (0.25, "w025")):
        for opt, bound in ((True, "optimistic"), (False, "conservative")):
            row = seam(width, opt)
            seams[(name, bound)] = row
            print(name, bound, row["total_kg"], row["pct_of_5pct_allowance"], row["margin_after_kg"])
    for item in theirs["item2_seams"]:
        key = {
            (4.0, "optimistic"): ("w4", "optimistic"),
            (4.0, "conservative"): ("w4", "conservative"),
            (2.0, "optimistic"): ("w2", "optimistic"),
            (2.0, "conservative"): ("w2", "conservative"),
            (0.5, "optimistic"): ("w05", "optimistic"),
            (0.5, "conservative"): ("w05", "conservative"),
            (0.25, "optimistic"): ("w025", "optimistic"),
            (0.25, "conservative"): ("w025", "conservative"),
        }[(item["panel_w_m"], item["bound"])]
        mine = seams[key]
        for field in ("seam_length_m", "doubler_kg", "adhesive_kg", "core_splice_kg", "total_kg", "pct_of_5pct_allowance", "margin_after_kg"):
            check(f"seam {key}", field, item[field], mine[field], 1e-12)

    lam = math.sqrt(GC_CORE / (E_SIC * TF * TC))
    print("lambda", lam)
    check("cte", "lambda", theirs["item3_thermal"]["cte_mismatch_shear_lag"]["lambda_per_m"], lam, 1e-12)
    for row in theirs["item3_thermal"]["cte_mismatch_shear_lag"]["rows"]:
        dt = row["dT_face_core_K"]
        strain = (ALPHA_PVC - ALPHA_SIC) * dt
        tau = strain * E_SIC * TF * lam
        check(f"cte {dt}", "tau", row["tau_max_Pa"], tau, 1e-12)
        check(f"cte {dt}", "sf40", row["SF_vs_0p40MPa"], 0.40e6 / tau, 1e-12)
        check(f"cte {dt}", "sf55", row["SF_vs_0p55MPa"], 0.55e6 / tau, 1e-12)
    for row in theirs["item3_thermal"]["thermal_imperfection"]:
        w = ALPHA_SIC * row["dT_vertical_K"] * R / 2.0
        check(f"imperfection {row['dT_vertical_K']}", "w", row["w_thermal_m"], w, 1e-15)

    a_diff = K_CORE / (RHO_CORE * CP_CORE)
    tau_core = TC ** 2 / (math.pi ** 2 * a_diff)
    print("core tau", tau_core)
    check("thermal", "tau", theirs["item3_thermal"]["core_tau_s"], tau_core, 1e-12)

    cases = [
        ("coated wind 2 m/s", 0.20, 0.90, 2.0),
        ("coated wind 10 m/s", 0.20, 0.90, 10.0),
        ("bare_SiC wind 2 m/s", 0.70, 0.85, 2.0),
        ("bare_SiC wind 10 m/s", 0.70, 0.85, 10.0),
    ]
    solved = {}
    for name, alpha, eps, wind in cases:
        day, h = thermal_balance(alpha, eps, 275.0, wind, SOLAR)
        night, _ = thermal_balance(alpha, eps, 260.0, wind, 0.0)
        solved[name] = (day, night, day - T_AIR, night - T_AIR, h)
        print(name, "day", day, "night", night, "h", h)
    bound = rad_only(0.70, 0.85, 275.0, SOLAR)
    print("rad bound bare day", bound)
    # Also try coated and sky-only env if the stated average misses.
    print("rad bound sky-only bare", (275.0 ** 4 + 0.70 * SOLAR / (4.0 * 0.85 * SIGMA_SB)) ** 0.25)
    print("rad bound air-env bare", (T_AIR ** 4 + 0.70 * SOLAR / (4.0 * 0.85 * SIGMA_SB)) ** 0.25)
    for alt in (5.67e-8, 5.67e-8):
        t_env = 0.5 * (275.0 + T_AIR)
        alt_bound = (t_env ** 4 + 0.70 * SOLAR / (4.0 * 0.85 * alt)) ** 0.25
        print("sigma", alt, "bound", alt_bound)
    theirs_env = {row["case"]: row for row in theirs["item3_thermal"]["environment"]}
    for name, (day, night, dd, dn, _) in solved.items():
        row = theirs_env[name]
        check(name, "T_day", row["T_face_day_K"], day, 1e-6)
        check(name, "T_night", row["T_face_night_K"], night, 1e-6)
    check("thermal", "rad_bound", theirs["item3_thermal"]["T_rad_only_bound_K"], bound, 1e-6)

    membrane = P_EXT * R / (4.0 * TF) / 1e6
    print("membrane MPa", membrane)

    # Weather. Governing SF scales as 1/p. Their stored margin scales the margin, not the lift.
    sf0 = 0.23515931324953654
    structure = LIFT - MARGIN
    weather_specs = [
        ("diurnal_1hPa", P_EXT + 100.0),
        ("synoptic_3pct", P_EXT * 1.03),
        ("synoptic_minus_3pct", P_EXT * 0.97),
        ("extreme_storm_low_10pct", P_EXT * 0.9),
    ]
    for name, p_case in weather_specs:
        sf = sf0 * P_EXT / p_case
        margin_scaled = MARGIN * p_case / P_EXT
        margin_lift = LIFT * (p_case / P_EXT) - structure
        print(name, "p", p_case, "sf", sf, "margin_x_ratio", margin_scaled, "lift_law", margin_lift)
    for row in theirs["item4_loads"]["weather"]:
        p_case = row["p_case_Pa"]
        check(row["case"], "sf_stored", row["crush_SF_at_case"], sf0 * P_EXT / p_case, 1e-12)
        check(row["case"], "margin_stored", row["lift_margin_kg_at_case"], MARGIN * p_case / P_EXT, 1e-12)

    q = 0.5 * RHO_AIR * 20.0 ** 2
    drag = CD * q * math.pi * R * R
    moor = drag * GUST
    patch_p = moor / PATCH / 1000.0
    sf_patch = CRUSH_KPA / patch_p
    spreader = moor / (CRUSH_KPA * 1000.0 / 1.5)
    added = 0.5 * RHO_AIR * V
    print("gust", q, drag, moor, patch_p, sf_patch, spreader, "added", added, "hull", structure)
    g = theirs["item4_loads"]["gust"]
    check("gust", "q", g["q_Pa"], q, 1e-12)
    check("gust", "drag", g["F_drag_N"], drag, 1e-12)
    check("gust", "moor", g["F_mooring_N"], moor, 1e-12)
    check("gust", "patch", g["patch_p_kPa"], patch_p, 1e-12)
    check("gust", "sf", g["SF_patch"], sf_patch, 1e-12)
    check("gust", "spreader", g["spreader_m2_needed"], spreader, 1e-12)
    check("gust", "added", g["added_air_mass_kg"], added, 1e-12)

    def climate(dt, dp):
        dl = dp / P_EXT - dt / T_AIR
        lift = LIFT * (1.0 + dl)
        return dl, lift, lift - structure

    for dt, dp, name in (
        (25.1, 0.0, "hot"),
        (-11.9, 0.0, "cold"),
        (0.0, 0.02 * P_EXT, "high"),
        (0.0, -0.02 * P_EXT, "low"),
    ):
        print("climate", name, climate(dt, dp))
    for row in theirs["item5_climate"]["rows"]:
        dl, lift, margin = climate(row["dT_K"], row["dp_Pa"])
        check(row["case"], "dl", row["dL_over_L"], dl, 1e-15)
        check(row["case"], "lift", row["lift_kg"], lift, 1e-12)
        check(row["case"], "margin", row["margin_kg"], margin, 1e-12)
    for row in theirs["item5_climate"]["surface_water"]:
        mass = row["film_mm"] * 1e-3 * A * WATER
        check(f"water {row['film_mm']}", "mass", row["mass_kg"], mass, 1e-12)
        check(f"water {row['film_mm']}", "pct", row["pct_of_margin"], 100.0 * mass / MARGIN, 1e-12)

    for rspec, label in ((287.05, "287.05"), (287.053, "287.053")):
        rho500, _, _ = isa_rho(500.0, rspec)
        rho1500, _, _ = isa_rho(1500.0, rspec)
        print("climb", label, "rho500", rho500, "rho1500", rho1500, "pct_per_km", 100.0 * (rho1500 / rho500 - 1.0))
        t = 284.9
        lapse = 0.0065
        g0 = 9.80665
        expo = g0 / (lapse * rspec)
        dln = -(lapse / t) * (expo - 1.0) * 1000.0
        print("  local pct per km", 100.0 * dln)

    # Card display tokens.
    displays = [
        ("card vacuum", "48.894", lift_1),
        ("card vacuum", "954.6", p_int),
        ("card vacuum", "46.28", q_allow),
        ("card vacuum", "2.48", a_choke * 1e6),
        ("card vacuum", "4.25", a_mol * 1e6),
        ("card pump", "46.3", vdot * 1000.0),
        ("card pump", "211", w_ideal),
        ("card pump", "527", w_real[1]),
        ("card pump", "844", w_real[0]),
        ("card pump", "61", pct_m[0]),
        ("card pump", "164", pct_m[1]),
        ("card pump", "506", pumpdown_kwh),
        ("card seam", "89.2", seams[("w4", "optimistic")]["total_kg"]),
        ("card seam", "187.8", seams[("w4", "conservative")]["total_kg"]),
        ("card seam", "178.3", seams[("w2", "optimistic")]["total_kg"]),
        ("card seam", "375.5", seams[("w2", "conservative")]["total_kg"]),
        ("card seam", "713.4", seams[("w05", "optimistic")]["total_kg"]),
        ("card seam", "1502.1", seams[("w05", "conservative")]["total_kg"]),
        ("card seam", "1426.7", seams[("w025", "optimistic")]["total_kg"]),
        ("card seam", "3004.3", seams[("w025", "conservative")]["total_kg"]),
        ("card seam", "966", -seams[("w025", "optimistic")]["margin_after_kg"]),
        ("card seam", "2543", -seams[("w025", "conservative")]["margin_after_kg"]),
        ("card seam", "330", seams[("w05", "optimistic")]["pct_of_5pct_allowance"]),
        ("card seam", "694", seams[("w05", "conservative")]["pct_of_5pct_allowance"]),
        ("card seam", "1388", seams[("w025", "conservative")]["pct_of_5pct_allowance"]),
        ("card thermal", "1.526", lam),
        ("card thermal", "283",  (ALPHA_PVC - ALPHA_SIC) * 30.0 * E_SIC * TF * lam / 1000.0),
        ("card thermal", "567", (ALPHA_PVC - ALPHA_SIC) * 60.0 * E_SIC * TF * lam / 1000.0),
        ("card thermal", "1.41", 0.40e6 / ((ALPHA_PVC - ALPHA_SIC) * 30.0 * E_SIC * TF * lam)),
        ("card thermal", "1.94", 0.55e6 / ((ALPHA_PVC - ALPHA_SIC) * 30.0 * E_SIC * TF * lam)),
        ("card thermal", "313.5", bound),
        ("card thermal", "357", tau_core),
        ("card weather", "0.2283", sf0 / 1.03),
        ("card weather", "0.2425", sf0 / 0.97),
        ("card weather", "0.2613", sf0 / 0.9),
        ("card weather", "219.9", MARGIN * 0.9),
        ("card gust", "233", q),
        ("card gust", "34.5", drag / 1000.0),
        ("card gust", "48.3", moor / 1000.0),
        ("card gust", "0.73", sf_patch),
        ("card gust", "0.145", spreader),
        ("card gust", "2445", added),
        ("card climate", "-186.3", climate(25.1, 0.0)[2]),
        ("card climate", "448.7", climate(-11.9, 0.0)[2]),
        ("card climate", "146.7", climate(0.0, -0.02 * P_EXT)[2]),
        ("card climate", "342.3", climate(0.0, 0.02 * P_EXT)[2]),
        ("card water", "125.6", 0.0001 * A * WATER),
        ("card water", "1257", 0.001 * A * WATER),
        ("card water", "51", 100.0 * 0.0001 * A * WATER / MARGIN),
        ("card membrane", "877", membrane),
    ]
    print("\nDISPLAY")
    for row, token, value in displays:
        ok = display_equal(token, value)
        if not ok:
            nd = len(token.split(".")[1]) if "." in token else 0
            print(f"  MISS {row} card {token} recomputed {value} half-up {half_up(value, nd)}")
        else:
            print(f"  ok {row} {token}")

    print("\nSOURCE REGISTER")
    missing_tag = []
    for row in inputs["sourced_values_new_this_card"] + inputs["inherited_values_used"]:
        if "tag" not in row or "source" not in row:
            missing_tag.append(row.get("name"))
        print(f"  {row['name']}: tag={row.get('tag')} source={row.get('source') is not None}")
    print("rows missing tag or source", missing_tag)
    print("unsourced inputs used by the arithmetic and absent from both registers:")
    print("  patch area 0.0707 m2; spreader target SF 1.5; cradle 250 kPa;")
    print("  pump ceiling 1000 Pa; water density 1000 kg/m3;")
    print("  Stefan-Boltzmann 5.670374419e-8; reference 101325 Pa;")
    print("  22414 cm3/mol appears only inside the formula string.")

    print("\nRESULT MISMATCHES", len(mismatches))
    for row in mismatches:
        print(" ", row)


if __name__ == "__main__":
    main()
