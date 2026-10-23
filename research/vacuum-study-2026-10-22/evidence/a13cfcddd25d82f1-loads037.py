#!/usr/bin/env python3
"""MAINLINE-037 loads beyond uniform pressure. Own arithmetic. QUESTIONABLE.

Does not import or run an owner script. Inherited safety factors are the
filed 028b and 022c numbers. Temperatures, wind pressure, pad size and the
scaled factors are computed here.
"""
import json
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
ZONE = ZoneInfo("America/Los_Angeles")
STARTED = datetime.now(ZONE).isoformat(timespec="seconds")

# COMMON.md case. The longer 016 pressure is the same value.
R = 10.0
P = 95460.83791390515
RHO = 1.1672683307461802
T_AIR = 284.9
LIFT = 4889.442150186961
MU_AIR = 1.79e-5
K_AIR = 0.0257
PR = 0.71
SIG = 5.670374419e-8
S_SOL = 970.0
T_SKY_DAY = 275.0
T_SKY_NIGHT = 260.0
G = 9.80665

# Beryllium lead, 028b PROPERTY-CHECKS full-named maximum, sheet nu.
# Face demand is p*R/(4*tf). 345 MPa is the tensile yield used in compression.
# 379.2 MPa is the historical compression endpoint that the floated face factor uses.
TF = 0.0007996763438767137
TC = 0.022106790073497733
NU_BE = 0.0752
E_BE = 290.0e9
ALPHA_BE = 11.3e-6
SIGMA_YIELD = 345.0e6
FACE_DEMAND = 298435856.7214987
RHO_CORE = 16.018463373960138
RHO_AL = 2640.0
K_AL = 130.0
ALPHA_AL = 23.6e-6
GC = 46884349.59354485
CRUSH = 241316.50526089262
SHEAR_W = 241316.50526089262
CELL = 0.009525
SF_FULL = {
    "global_buckling": 1.0063580774984726,
    "face_compression": 1.2706247974547864,
    "core_shear_crimping": 2.331434189777838,
    "core_crush": 5.0558220634629825,
    "face_wrinkling": 1.9648678490458737,
    "intracell_dimpling": 6.973752041582777,
    "scarf_mean_shear": 1.0063580718238068,
}
SF_TODAY = {
    "global_buckling": 0.33958237184408885,
    "face_compression": 1.1560273078109213,
    "core_shear_crimping": 2.331434189777838,
    "core_crush": 5.0558220634629825,
    "face_wrinkling": 0.7858766898428499,
    "intracell_dimpling": 6.888242820364461,
    "scarf_mean_shear": 1.0063580718238068,
}
FACE_MODES = {
    "face_compression",
    "core_shear_crimping",
    "face_wrinkling",
    "intracell_dimpling",
}
# Owner 10 MPa mean-shear screen from MAINLINE-028. Not a qualified allowable.
SHEAR_SCREEN = 10.0e6

# 022c cap-branch rows, SAG.md. 022d had not filed.
P3_ROWS = [
    ("projection_5", 6.15, 167.640119605e-3, 1.62308840871e-3, 0.286196977567e-3,
     {"yield": 3.91514055515, "euler": 1.44659814165, "local": 1.37814486994,
      "film": 1.4624665443, "perry": 1.38684321386, "global": 1.37332138578},
     "global", "SiC", "projection"),
    ("projection_019", 6.15, 165.56927728e-3, 1.5764940544e-3, 0.282331413376e-3,
     {"yield": 3.75607531179, "euler": 1.35396688465, "local": 1.29454034466,
      "film": 1.44271351144, "perry": 1.29937293637, "global": 1.30135480413},
     "local", "SiC", "projection"),
    ("mylar_5", 0.55, 85.198285962e-3, 0.311393365654e-3, 0.075648207133e-3,
     {"yield": 0.417168959855, "euler": 53.091074319, "local": 0.414010996767,
      "film": 0.437101571069, "perry": 0.411790451893, "global": 0.765560371986},
     "perry", "SiC", "mylar"),
    ("mylar_019", 0.55, 83.648109219e-3, 0.304960512996e-3, 0.0746264528047e-3,
     {"yield": 0.401119251744, "euler": 49.2082089363, "local": 0.396690072456,
      "film": 0.43119779041, "perry": 0.395851626757, "global": 0.722716927636},
     "perry", "SiC", "mylar"),
    ("ti_kapton_5", 1.85, 103.024994729e-3, 0.696137079109e-3, 0.565062135793e-3,
     {"yield": 3.43562499303, "euler": 5.47468903403, "local": 0.761765644494,
      "film": 0.739113638303, "perry": 3.16415609359, "global": 0.741703542024},
     "film", "Ti", "kapton"),
    ("ti_kapton_019", 1.85, 101.874428848e-3, 0.673496981391e-3, 0.549901019907e-3,
     {"yield": 3.28700995308, "euler": 5.12227941877, "local": 0.708276178104,
      "film": 0.719282566969, "perry": 3.01803070154, "global": 0.701745910728},
     "global", "Ti", "kapton"),
    ("cfrp_zylon_5", 5.5, 166.123869207e-3, 1.59839332382e-3, 0.112682709914e-3,
     {"yield": 4.27236643954, "euler": 1.95142954175, "local": 1.49206896315,
      "film": 1.49375231321, "perry": 1.8504480324, "global": 1.48511637206},
     "global", "CFRP", "zylon"),
    ("cfrp_zylon_019", 5.7, 165.619741842e-3, 1.59177158769e-3, 0.110783474523e-3,
     {"yield": 4.09294415772, "euler": 1.72663320583, "local": 1.42740041766,
      "film": 1.41704657175, "perry": 1.64487373383, "global": 1.41843747897},
     "film", "CFRP", "zylon"),
]
FRAME = {
    "SiC": {"E": 410.0e9, "alpha": 4.5e-6, "nu": 0.17, "rho": 3100.0},
    "Ti": {"E": 113.8e9, "alpha": 8.6e-6, "nu": 0.33, "rho": 4430.0},
    "CFRP": {"E": 150.0e9, "alpha": 0.5e-6, "nu": 0.30, "rho": 1600.0},
}
FILM = {
    "projection": {"E": 10.0e9, "alpha": None, "nu": 0.33, "rho": 970.0,
                   "alpha_note": "unstated; two assumptions, 4.5e-6 and 17e-6"},
    "mylar": {"E": 4.8e9, "alpha": 17.0e-6, "nu": 0.38, "rho": 1400.0},
    "kapton": {"E": 2.5e9, "alpha": 20.0e-6, "nu": 0.34, "rho": 1420.0},
    "zylon": {"E": 180.0e9, "alpha": -6.0e-6, "nu": 0.30, "rho": 1560.0},
}


def whitaker(v, diameter):
    re = RHO * v * diameter / MU_AIR
    nu = 2.0 + (0.4 * re ** 0.5 + 0.06 * re ** (2.0 / 3.0)) * PR ** 0.4
    return nu * K_AIR / diameter


def h_nat(dT):
    # Simplified large-surface natural convection, QUESTIONABLE.
    return 1.32 * max(abs(dT), 0.05) ** 0.25


def h_air(v, diameter, dT):
    return max(whitaker(max(v, 1.0e-6), diameter), h_nat(dT))


def churchill_cylinder(v, diameter):
    re = RHO * max(v, 1.0e-6) * diameter / MU_AIR
    pr = PR
    term = (0.62 * re ** 0.5 * pr ** (1.0 / 3.0)
            / (1.0 + (0.4 / pr) ** (2.0 / 3.0)) ** 0.25)
    return (0.3 + term * (1.0 + (re / 282000.0) ** (5.0 / 8.0)) ** (4.0 / 5.0)) * K_AIR / diameter


def legendre(n, mu):
    if n == 0:
        return 1.0
    if n == 1:
        return mu
    p0, p1 = 1.0, mu
    for k in range(1, n):
        p0, p1 = p1, ((2 * k + 1) * mu * p1 - k * p0) / (k + 1)
    return p1


def project(mus, values, nmax):
    dmu = mus[1] - mus[0]
    coeffs = []
    for n in range(nmax + 1):
        acc = 0.0
        for mu, val in zip(mus, values):
            acc += val * legendre(n, mu)
        coeffs.append((2 * n + 1) / 2.0 * acc * dmu)
    return coeffs


def half_wave_ratio(ro, wall, s):
    ri = ro - wall
    rg = math.sqrt((ro * ro + ri * ri) / 2.0)
    wave = math.pi * math.sqrt(0.75 * rg * R)
    return wave / s, wave, rg


def member_force(s, pressure):
    return pressure * R * s / (2.0 * math.sqrt(3.0))


def film_stress(s, t_film, pressure):
    return pressure * s / (2.0 * t_film)


def bisect(fn, lo, hi, steps=80):
    flo, fhi = fn(lo), fn(hi)
    if flo == 0:
        return lo
    if flo * fhi > 0:
        # Walk outward once if the bracket missed.
        for _ in range(12):
            if flo * fhi <= 0:
                break
            if abs(flo) < abs(fhi):
                lo = lo - 0.6 * (hi - lo)
                flo = fn(lo)
            else:
                hi = hi + 0.6 * (hi - lo)
                fhi = fn(hi)
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        fm = fn(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


def environment(mu, t_sky):
    # Upper hemisphere sees sky. Lower sees ground at the air temperature.
    f_sky = 0.5 * (1.0 + mu)
    t4 = f_sky * t_sky ** 4 + (1.0 - f_sky) * T_AIR ** 4
    return t4


def sandwich_zones(alpha, eps_out, eps_in, wind, solar, t_sky):
    n = 37
    dmu = 2.0 / n
    mus = [-1.0 + (i + 0.5) * dmu for i in range(n)]
    k_eff = K_AL * (RHO_CORE / RHO_AL)
    u_cond = k_eff / TC
    eps_gap = 0.20
    temps_o = [T_AIR] * n
    temps_i = [T_AIR] * n
    for _ in range(25):
        mean_t4 = sum(t ** 4 for t in temps_i) / n
        t_mean = sum(temps_i) / n
        u = u_cond + eps_gap * 4.0 * SIG * t_mean ** 3
        new_o, new_i = [], []
        for mu in mus:
            tenv4 = environment(mu, t_sky)
            absorbed = alpha * solar * max(mu, 0.0)

            def residual(ti):
                q_in = eps_in * SIG * (ti ** 4 - mean_t4)
                to = ti + q_in / u
                h = h_air(wind, 2.0 * R, to - T_AIR)
                q_rad = eps_out * SIG * (to ** 4 - tenv4)
                q_conv = h * (to - T_AIR)
                return absorbed - q_rad - q_conv - q_in

            ti = bisect(residual, 180.0, 900.0)
            q_in = eps_in * SIG * (ti ** 4 - mean_t4)
            to = ti + q_in / u
            new_i.append(ti)
            new_o.append(to)
        temps_o, temps_i = new_o, new_i
    return mus, temps_o, temps_i, k_eff, u_cond


def pattern_stress(mus, t_mean, modulus, alpha, nu, lever):
    coeffs = project(mus, t_mean, 6)
    rest = []
    for mu, temp in zip(mus, t_mean):
        rest.append(temp - coeffs[0] - coeffs[1] * mu)
    # Curvature from the n=2..6 reconstruction only, so a zone-edge kink
    # in the raw samples does not set the stress. kappa = -d^2(w)/dphi^2 / R^2
    # with w = R*alpha*T_rest. n=0 and n=1 are omitted.
    nphi = 721
    phis = [math.pi * i / (nphi - 1) for i in range(nphi)]
    wrest = []
    for phi in phis:
        mu = math.cos(phi)
        tr = 0.0
        for n in range(2, len(coeffs)):
            tr += coeffs[n] * legendre(n, mu)
        wrest.append(R * alpha * tr)
    kappas = []
    for i in range(1, nphi - 1):
        dphi = phis[i] - phis[i - 1]
        d2 = (wrest[i + 1] - 2.0 * wrest[i] + wrest[i - 1]) / dphi ** 2
        kappas.append(-d2 / (R * R))
    kmax = max(abs(k) for k in kappas)
    sigma_b = modulus / (1.0 - nu * nu) * lever * kmax
    t_rest_max = max(abs(v) for v in rest)
    sigma_constrained = modulus * alpha * t_rest_max / (1.0 - nu)
    return {
        "legendre_K": coeffs,
        "T_rest_max_K": t_rest_max,
        "kappa_max_1_per_m": kmax,
        "bending_stress_Pa": sigma_b,
        "constrained_upper_Pa": sigma_constrained,
    }


def gradient_stress(dT):
    return E_BE * ALPHA_BE * dT / (2.0 * (1.0 - NU_BE))


def shear_lag(dT):
    d_eps = (ALPHA_AL - ALPHA_BE) * dT
    lam = math.sqrt(GC / (E_BE * TF * TC))
    tau = d_eps * E_BE * TF * lam
    return {"d_eps": d_eps, "lambda_1_per_m": lam, "tau_Pa": tau,
            "SF_vs_shear_W": SHEAR_W / tau if tau else None}


def scale_p2(base, q, sigma_add):
    out = {}
    for mode, sf in base.items():
        if mode in FACE_MODES:
            demand = FACE_DEMAND * (P + q) / P + sigma_add
            out[mode] = sf * FACE_DEMAND / demand
        else:
            out[mode] = sf * P / (P + q)
    least_mode = min(out, key=lambda m: (out[m], m))
    return out, least_mode, out[least_mode]


def p3_thermal(row, wind, solar, t_sky, alpha_film_override=None):
    name, s, ro, wall, t_film, modes, gov, frame_name, film_name = row
    frame = FRAME[frame_name]
    film = FILM[film_name]
    alpha_f = film["alpha"] if alpha_film_override is None else alpha_film_override
    n = 37
    dmu = 2.0 / n
    mus = [-1.0 + (i + 0.5) * dmu for i in range(n)]
    nodes = 2.0 + 8.0 * math.pi * R * R / (math.sqrt(3.0) * s * s)
    n_members = 3.0 * (nodes - 2.0)
    area = 4.0 * math.pi * R * R
    line_density = n_members * s / area
    shadow = min(0.85, line_density * 2.0 * ro)
    alpha_abs, eps = (0.70, 0.85) if film_name != "mylar" else (0.20, 0.90)
    # Stated coatings. Mylar is taken as a white polymer. The others are bare-class.
    if film_name == "kapton":
        alpha_abs, eps = 0.70, 0.85
    if film_name == "zylon":
        alpha_abs, eps = 0.55, 0.80
    if film_name == "projection":
        alpha_abs, eps = 0.50, 0.80
    tube_alpha, tube_eps = 0.50, 0.80
    if frame_name == "Ti":
        tube_alpha, tube_eps = 0.45, 0.25
    film_T = [T_AIR] * n
    tube_T = [T_AIR] * n
    for _ in range(20):
        mean_t4 = sum(t ** 4 for t in film_T) / n
        new_f, new_t = [], []
        for mu in mus:
            tenv4 = environment(mu, t_sky)
            absorbed = alpha_abs * solar * max(mu, 0.0) * (1.0 - shadow)

            def residual(tf):
                h = h_air(wind, 2.0 * R, tf - T_AIR)
                q_out = eps * SIG * (tf ** 4 - tenv4)
                q_in = eps * SIG * (tf ** 4 - mean_t4)
                q_conv = h * (tf - T_AIR)
                return absorbed - q_out - q_in - q_conv

            tf = bisect(residual, 180.0, 700.0)
            new_f.append(tf)

            def tube_residual(tt):
                h = max(churchill_cylinder(wind, 2.0 * ro), h_nat(tt - T_AIR))
                q_sol = tube_alpha * solar * max(mu, 0.0) / math.pi
                q_rad = tube_eps * SIG * (tt ** 4 - tenv4)
                return q_sol - q_rad - h * (tt - T_AIR)

            new_t.append(bisect(tube_residual, 180.0, 800.0))
        film_T, tube_T = new_f, new_t
    # Subsolar is the last zone (mu near +1). Night-side is the first.
    i_hot = n - 1
    dT_frame = tube_T[i_hot] - T_AIR
    dT_film = film_T[i_hot] - T_AIR
    # Uniform-temperature mismatch from the assembly temperature, member-stiff limit.
    # Film takes (alpha_frame - alpha_film)*dT. dT is the film's own rise; the
    # frame rise enters as an extra term when the two temperatures differ.
    if alpha_f is None:
        mismatch = None
    else:
        eps_m = frame["alpha"] * dT_frame - alpha_f * dT_film
        # Member much stiffer: mechanical film strain equals that difference.
        d_sigma = film["E"] / (1.0 - film["nu"]) * eps_m
        n_film = d_sigma * t_film
        d_force = n_film * s / math.sqrt(3.0)
        mismatch = {"eps_mechanical": eps_m, "film_stress_Pa": d_sigma,
                    "member_force_N": d_force}
    return {
        "T_film_subsolar_K": film_T[i_hot],
        "T_film_antisolar_K": film_T[0],
        "T_tube_subsolar_K": tube_T[i_hot],
        "T_tube_antisolar_K": tube_T[0],
        "shadow_fraction": shadow,
        "mismatch": mismatch,
        "film_alpha_used": alpha_f,
    }


def plate_mass(force, crush, sigma_allow, n_pads):
    # One pad carries force/n_pads. Area restores core crush to SF 1.
    share = force / n_pads
    area = share / crush
    radius = math.sqrt(area / math.pi)
    boss = 0.025
    if radius <= boss * 1.2:
        thickness = share / (math.pi * boss * boss * sigma_allow)
        thickness = max(thickness, 0.001)
    else:
        # Simply-supported circular plate, central boss, uniform core reaction.
        # sigma = 3*(1+nu)*F*ln(a/r0) / (2*pi*t^2). QUESTIONABLE.
        nu = 0.33
        ln = math.log(radius / boss)
        thickness = math.sqrt(3.0 * (1.0 + nu) * share * ln / (2.0 * math.pi * sigma_allow))
    mass_one = area * thickness * 2700.0
    return {"area_one_m2": area, "radius_m": radius, "thickness_m": thickness,
            "mass_one_kg": mass_one, "mass_total_kg": mass_one * n_pads,
            "share_N": share}


def main():
    per_k = gradient_stress(1.0)
    # Temperatures.
    coats = {
        "coated_outer": (0.20, 0.90, 0.20),
        "bare_Be": (0.40, 0.05, 0.20),
    }
    thermal = {}
    for name, (a, e, ei) in coats.items():
        mus, to, ti, k_eff, u_cond = sandwich_zones(a, e, ei, 2.0, S_SOL, T_SKY_DAY)
        _, to_n, ti_n, _, _ = sandwich_zones(a, e, ei, 2.0, 0.0, T_SKY_NIGHT)
        t_mean = [0.5 * (o + i) for o, i in zip(to, ti)]
        pat = pattern_stress(mus, t_mean, E_BE, ALPHA_BE, NU_BE, 0.5 * (TC + TF))
        i_hot = max(range(len(mus)), key=lambda i: to[i] - ti[i])
        dT = to[i_hot] - ti[i_hot]
        swing = max(to) - min(to_n)
        lag_day = shear_lag(max(to) - T_AIR)
        lag_swing = shear_lag(swing)
        thermal[name] = {
            "alpha": a, "epsilon_out": e, "epsilon_in": ei,
            "k_eff_W_per_mK": k_eff, "U_conduction_W_per_m2K": u_cond,
            "T_outer_subsolar_K": to[-1], "T_inner_subsolar_K": ti[-1],
            "T_outer_antisolar_K": to[0], "T_inner_antisolar_K": ti[0],
            "dT_through_at_max_K": dT,
            "gradient_stress_Pa": gradient_stress(dT),
            "day_night_outer_swing_K": swing,
            "pattern": pat,
            "shear_lag_from_day_rise": lag_day,
            "shear_lag_from_swing": lag_swing,
            "T_outer_day_K": to,
            "T_outer_night_K": to_n,
        }
    # Wind.
    knots = 0.514444
    vb = 35.0 * knots
    u_gust = 35.0 * 0.3048
    # q(V+U) - q(V) = rho*V*U + 0.5*rho*U^2, then the stagnation excess is that
    # dynamic pressure (Cp = +1).
    q_flight = RHO * vb * u_gust + 0.5 * RHO * u_gust ** 2
    q_vb = 0.5 * RHO * vb ** 2
    q_20 = 0.5 * RHO * 20.0 ** 2
    q_70 = 0.5 * RHO * (70.0 * knots) ** 2
    q_78 = 0.5 * RHO * (78.0 * knots) ** 2

    def drag(q):
        return 0.47 * q * math.pi * R * R

    f_016 = drag(q_20) * 1.4
    wind = {
        "q_20_Pa": q_20,
        "q_20_over_p": q_20 / P,
        "drag_20_N": drag(q_20),
        "mooring_016_N": f_016,
        "VB_m_s": vb,
        "Ugust_35fps_m_s": u_gust,
        "q_flight_stagnation_Pa": q_flight,
        "q_flight_over_p": q_flight / P,
        "q_VB_only_Pa": q_vb,
        "q_moor_70kn_Pa": q_70,
        "q_moor_70_over_p": q_70 / P,
        "drag_70_N": drag(q_70),
        "q_moor_78kn_Pa": q_78,
        "drag_78_N": drag(q_78),
        "potential_Cp": "1 - 2.25*sin^2(theta); area mean Cp = -0.5",
        "potential_mean_dp_over_q": -0.5,
    }
    # P2 table.
    coated = thermal["coated_outer"]
    bare = thermal["bare_Be"]
    cases = {
        "uniform": (0.0, 0.0),
        "sun_coated_gradient_and_bend": (0.0, coated["gradient_stress_Pa"] + coated["pattern"]["bending_stress_Pa"]),
        "sun_bare_gradient_and_bend": (0.0, bare["gradient_stress_Pa"] + bare["pattern"]["bending_stress_Pa"]),
        "wind_flight_gust_uniform": (q_flight, 0.0),
        "wind_moor_70kn_uniform": (q_70, 0.0),
        "combined_coated_gust": (q_flight, coated["gradient_stress_Pa"] + coated["pattern"]["bending_stress_Pa"]),
        "combined_bare_gust": (q_flight, bare["gradient_stress_Pa"] + bare["pattern"]["bending_stress_Pa"]),
    }
    p2 = {"today_uniform_least": min(SF_TODAY.values()), "full_uniform": {}}
    for cname, (q, sig) in cases.items():
        scaled, least_mode, least = scale_p2(SF_FULL, q, sig)
        # Yield against 345 MPa, same added stress.
        demand = FACE_DEMAND * (P + q) / P + sig
        p2[cname] = {"modes": scaled, "least_mode": least_mode, "least_SF": least,
                     "face_SF_on_345": SIGMA_YIELD / demand,
                     "demand_Pa": demand}
    # Shear lag is not one of the seven screens.
    p2["shear_lag_coated_swing_SF"] = coated["shear_lag_from_swing"]["SF_vs_shear_W"]
    p2["shear_lag_bare_day_SF"] = bare["shear_lag_from_day_rise"]["SF_vs_shear_W"]
    p2["shear_lag_bare_swing_SF"] = bare["shear_lag_from_swing"]["SF_vs_shear_W"]
    scarf_stress = SHEAR_SCREEN / SF_FULL["scarf_mean_shear"]
    p2["scarf_pressure_stress_if_10MPa_Pa"] = scarf_stress
    p2["scarf_SF_if_10MPa_plus_coated_swing_shear"] = SHEAR_SCREEN / (
        scarf_stress + coated["shear_lag_from_swing"]["tau_Pa"])
    # Pads.
    pads = {
        "mooring_016_one_pad_SF1": plate_mass(f_016, CRUSH, 276.0e6, 1),
        "mooring_016_six_pads_SF1": plate_mass(f_016, CRUSH, 276.0e6, 6),
        "mooring_70kn_one_pad_SF1": plate_mass(drag(q_70), CRUSH, 276.0e6, 1),
        "systems_100kg_six_pads": plate_mass(100.0 * G, CRUSH, 276.0e6, 6),
        "reserve_411kg_one_pad": plate_mass(411.2989440716474 * G, CRUSH, 276.0e6, 1),
        "bare_016_patch_0p0707_SF": CRUSH / (f_016 / 0.0707),
    }
    # P3.
    p3 = []
    for row in P3_ROWS:
        name, s, ro, wall, t_film, modes, gov, frame_name, film_name = row
        ratio, wave, rg = half_wave_ratio(ro, wall, s)
        alphas = [None]
        if film_name == "projection":
            alphas = [4.5e-6, 17.0e-6]
        else:
            alphas = [FILM[film_name]["alpha"]]
        for a_f in alphas:
            day = p3_thermal(row, 2.0, S_SOL, T_SKY_DAY, a_f)
            night = p3_thermal(row, 2.0, 0.0, T_SKY_NIGHT, a_f)
            force = member_force(s, P)
            d_force = 0.0 if day["mismatch"] is None else day["mismatch"]["member_force_N"]
            d_sig = 0.0 if day["mismatch"] is None else day["mismatch"]["film_stress_Pa"]
            sig_f = film_stress(s, t_film, P)
            scaled = {}
            for mode, sf in modes.items():
                if mode == "film":
                    # Pressure part grows with p+q; thermal stress is added.
                    stress = sig_f * (P + q_flight) / P + d_sig
                    scaled[mode] = sf * sig_f / stress
                else:
                    load = force * (P + q_flight) / P + d_force
                    scaled[mode] = sf * force / load
            least_mode = min(scaled, key=lambda m: (scaled[m], m))
            # Mass to put the governing pressure mode back to SF 1, thickness
            # scaling of the film if film governs, else tube-wall scaling.
            least = scaled[least_mode]
            factor = 1.0 / least if least < 1.0 else 1.0
            area = 4.0 * math.pi * R * R
            film_mass = area * t_film * FILM[film_name]["rho"]
            ri = ro - wall
            a_tube = math.pi * (ro * ro - ri * ri)
            nodes = 2.0 + 8.0 * math.pi * R * R / (math.sqrt(3.0) * s * s)
            n_members = 3.0 * (nodes - 2.0)
            tube_mass = n_members * s * a_tube * FRAME[frame_name]["rho"]
            if least_mode == "film":
                extra_mass = film_mass * (factor - 1.0)
            elif least < 1.0:
                extra_mass = tube_mass * (factor - 1.0)
            else:
                extra_mass = 0.0
            # Members that keep the mooring add under 5 percent of member force.
            n_share = math.ceil(f_016 / (0.05 * force))
            p3.append({
                "row": name,
                "s_m": s,
                "half_wave_over_s": ratio,
                "half_wave_m": wave,
                "in_band": ratio >= 1.0,
                "governing_filed": gov,
                "uniform": modes,
                "film_alpha": a_f,
                "thermal_day": {k: day[k] for k in day if k != "mismatch"},
                "thermal_night_subsolar_film_K": night["T_film_subsolar_K"],
                "thermal_night_subsolar_tube_K": night["T_tube_subsolar_K"],
                "mismatch": day["mismatch"],
                "member_force_N": force,
                "film_stress_Pa": sig_f,
                "combined_flight_gust": scaled,
                "combined_least_mode": least_mode,
                "combined_least_SF": least,
                "optimism_or_thickness_factor_to_SF1": factor,
                "extra_mass_kg_if_that_part_scales": extra_mass,
                "film_mass_kg": film_mass,
                "tube_mass_kg": tube_mass,
                "members_to_hold_mooring_add_to_5pct": n_share,
            })
    # What restores the P2 lead.
    coated_least = p2["combined_coated_gust"]["least_SF"]
    # Global is pressure-only. Extra gamma is today's gap, not a mass.
    restore = {
        "coated_combined_least_SF": coated_least,
        "coated_combined_least_mode": p2["combined_coated_gust"]["least_mode"],
        "mass_to_restore_coated_combined_kg": 0.0 if coated_least >= 1.0 else None,
        "bare_swing_shear_SF": p2["shear_lag_bare_swing_SF"],
        "coated_swing_shear_SF": p2["shear_lag_coated_swing_SF"],
        "note": "A coated flight gust leaves the floated global factor above 1. "
                "Bare beryllium shear-lag is a coating and assembly-temperature limit.",
    }
    ended = datetime.now(ZONE).isoformat(timespec="seconds")
    out = {
        "unit": "vacuum-mainline037-loads-beyond-pressure-1020",
        "tag": "QUESTIONABLE",
        "started_at": STARTED,
        "ended_at": ended,
        "per_kelvin_gradient_stress_Pa": per_k,
        "face_working_stress_Pa": FACE_DEMAND,
        "face_SF_on_345_uniform": SIGMA_YIELD / FACE_DEMAND,
        "p2_thermal": {k: {kk: vv for kk, vv in val.items() if kk not in ("T_outer_day_K", "T_outer_night_K")}
                       for k, val in thermal.items()},
        "wind": wind,
        "p2": p2,
        "pads": pads,
        "p3": p3,
        "restore": restore,
        "assumptions": [
            "Through-thickness stress is E*alpha*dT/(2*(1-nu)), equal compression and tension.",
            "A through-thickness-uniform temperature on a complete single-material sphere has no membrane stress. Bending uses kappa = -d^2(w)/dphi^2/R^2 with w = R*alpha*T_rest.",
            "The fully constrained pattern stress is an upper bound and is not the table value.",
            "Windward excess is applied as a uniform pressure, the conservative global case. Potential-flow area-mean Cp is -0.5.",
            "FAA-P-8110-2 paragraph 3.9: 35 ft/s at VB, and VB is at least 35 knots. Table 4 mooring wind is 70 knots. The change discussion says 78 knots.",
            "016 mooring is Cd 0.47 times q at 20 m/s times 1.4.",
            "Honeycomb conductance is aluminum conductivity times the core solidity. The cells are evacuated.",
            "022d had not filed. Half-wave uses pi*sqrt((3/4)*rg*R) with rg = sqrt((ro^2+ri^2)/2).",
        ],
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
    print("wrote", ended)
    print("per_k_MPa", per_k / 1e6)
    for name in ("coated_outer", "bare_Be"):
        t = thermal[name]
        print(name, "To", t["T_outer_subsolar_K"], "Ti", t["T_inner_subsolar_K"],
              "dT", t["dT_through_at_max_K"], "swing", t["day_night_outer_swing_K"],
              "sig_g_MPa", t["gradient_stress_Pa"] / 1e6,
              "sig_b_MPa", t["pattern"]["bending_stress_Pa"] / 1e6,
              "Trest", t["pattern"]["T_rest_max_K"],
              "constrained_MPa", t["pattern"]["constrained_upper_Pa"] / 1e6,
              "lag_swing_SF", t["shear_lag_from_swing"]["SF_vs_shear_W"],
              "lag_day_SF", t["shear_lag_from_day_rise"]["SF_vs_shear_W"],
              "tau_swing_kPa", t["shear_lag_from_swing"]["tau_Pa"] / 1e3)
    print("q_flight", q_flight, "q70", q_70, "F016", f_016, "F70", drag(q_70))
    for cname in cases:
        row = p2[cname]
        print(cname, row["least_mode"], row["least_SF"], "face345", row["face_SF_on_345"])
    print("scarf_plus", p2["scarf_SF_if_10MPa_plus_coated_swing_shear"])
    print("pad016", pads["mooring_016_one_pad_SF1"])
    print("pad70", pads["mooring_70kn_one_pad_SF1"])
    for row in p3:
        if row["row"].endswith("_019") and row["film_alpha"] not in (4.5e-6,):
            continue
        print(row["row"], "a", row["film_alpha"], "band", row["in_band"],
              "ratio", round(row["half_wave_over_s"], 3),
              "least", row["combined_least_mode"], round(row["combined_least_SF"], 4),
              "Tfilm", round(row["thermal_day"]["T_film_subsolar_K"], 2),
              "Ttube", round(row["thermal_day"]["T_tube_subsolar_K"], 2),
              "extra", round(row["extra_mass_kg_if_that_part_scales"], 2),
              "nshare", row["members_to_hold_mooring_add_to_5pct"])


if __name__ == "__main__":
    main()
