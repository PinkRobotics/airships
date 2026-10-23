"""Independent algebra, polynomial extrema, and explicit alternative load models.

Only JSON evidence is read. No owner executable is loaded. Reproduction of a
number is separated from validation of its physical assumptions.
"""
from pathlib import Path
import csv
import json
import math
from collections import Counter
import numpy as np
from numpy.polynomial import Polynomial, Legendre
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
D = json.loads((ROOT / "INPUTS.json").read_text())
O = D["owner_results"]
X = D["explicit_check_assumptions"]
P = D["P2_028b_selected"]["point"]
C = P["core"]
CASE = D["P2_028b_case"]
p = CASE["p0_Pa"]
R = CASE["R_m"]
Ta = D["atmosphere_016"]["T_K"]
rho = D["atmosphere_016"]["rho_air"]
tf, tc, nu = P["tf_m"], P["tc_m"], P["nu"]
E, alpha = X["Be_E_thermal_Pa"], X["Be_alpha_per_K"]
SB = X["thermal_countermodel"]["sigma_SB"]
rows, corrections, checks = [], [], []
seen = set()


def value(path):
    v = O
    for part in path.strip("/").split("/"):
        v = v[int(part)] if isinstance(v, list) else v[part]
    return v


def audit(path, check=None, basis="", status=None):
    assert path not in seen, path
    seen.add(path)
    old = value(path)
    if status is None:
        if check is None:
            status = "UNRESOLVED"
        elif isinstance(old, (int, float)) and not isinstance(old, bool):
            status = "MATCH" if math.isclose(old, check, rel_tol=1e-8, abs_tol=1e-9) else "MISMATCH"
        else:
            status = "MATCH" if old == check else "MISMATCH"
    rows.append({"row": path.rsplit("/", 1)[0], "field": path.rsplit("/", 1)[1],
                 "card_value": old, "check_value": check, "status": status,
                 "delta": check - old if isinstance(old, (int, float)) and not isinstance(old, bool)
                 and isinstance(check, (int, float)) else None, "basis": basis})
    return check


def correction(row, field, old, new, basis, kind="CONDITIONAL_FIX"):
    corrections.append({"row": row, "field": field, "card_value": old,
                        "check_value": new, "kind": kind, "basis": basis})


def verify(name, actual, expected, rtol=1e-9, atol=1e-8):
    ok = math.isclose(actual, expected, rel_tol=rtol, abs_tol=atol)
    checks.append({"check": name, "actual": actual, "expected": expected, "passed": ok})


def p2_capacities(modulus, full=True):
    h = tc + tf
    sigma0 = modulus * h / (R * math.sqrt(1 - nu * nu))
    crimp = h * h * C["Gc_Pa"] / (2 * tf * tc)
    Vc = sigma0 / crimp
    Kc = 1 - Vc / 4 if Vc <= 2 else 1 / Vc
    gamma = .2 + .4 * min(Vc, 2) if full else (.2 if Vc < 2 else 1)
    b = brentq(lambda x: x**3 + x - 1, 0, 1, xtol=1e-15)
    return {
        "global_buckling": gamma * Kc * sigma0,
        "face_compression": 379.2e6 if full else 345e6,
        "core_shear_crimping": crimp,
        "core_crush": C["crush_Pa"],
        "face_wrinkling": b * (.82 if full else .33)
        * math.sqrt(modulus * C["Ec_Pa"] * tf / tc),
        "intracell_dimpling": modulus * (tf / C["s_cell_m"])**2 / (1 - nu**2),
        "scarf_mean_shear": 10e6 * 901 / 30
    }


caps = p2_capacities(X["Be_E_full_endpoint_Pa"])
sigma_p = p * R / (4 * tf)
gradient_per_K = E * alpha / (2 * (1 - nu))
audit("/per_kelvin_gradient_stress_Pa", gradient_per_K, "Declared E, alpha and nu")
audit("/face_working_stress_Pa", sigma_p, "p R / (4 tf)")
audit("/face_SF_on_345_uniform", 345e6 / sigma_p, "345 MPa tensile proxy / pressure stress")
today = p2_capacities(E, False)
audit("/p2/today_uniform_least", min(v / (p / 2 if k == "core_crush" else sigma_p)
      for k, v in today.items()), "Independent 028b today-property equations")
keff = X["Al_k_W_mK"] * C["rho"] / X["Al_rho_kg_m3"]
conductance = keff / tc
lag_lambda = math.sqrt(C["Gc_Pa"] / (E * tf * tc))
tau_per_K = (X["Al_alpha_per_K"] - alpha) * E * tf * lag_lambda
thermal = {}


def polynomial_extrema(poly):
    roots = poly.deriv().roots()
    x = [-1., 1.] + [float(z.real) for z in roots
                     if abs(z.imag) < 1e-9 and -1 < z.real < 1]
    y = poly(np.array(x))
    j = int(np.argmax(abs(y)))
    return {"min": float(min(y)), "max": float(max(y)),
            "max_abs": float(abs(y[j])), "mu_at_max_abs": x[j]}


for name, item in O["p2_thermal"].items():
    base = "/p2_thermal/" + name
    for key, expected in [("alpha", .2 if name == "coated_outer" else .4),
                          ("epsilon_out", .9 if name == "coated_outer" else .05),
                          ("epsilon_in", .2)]:
        audit(base + "/" + key, expected, "Declared optical assumption; not a measured property",
              "DECLARED_INPUT")
    audit(base + "/k_eff_W_per_mK", keff, "Al conductivity times solidity; PROJECTION")
    audit(base + "/U_conduction_W_per_m2K", conductance, "keff / tc; conduction only")
    for field in ["T_outer_subsolar_K", "T_inner_subsolar_K",
                  "T_outer_antisolar_K", "T_inner_antisolar_K",
                  "day_night_outer_swing_K"]:
        audit(base + "/" + field, basis="Missing heat-transfer speed, complete boundary conditions, angular samples and night temperature")
    dT = item["T_outer_subsolar_K"] - item["T_inner_subsolar_K"]
    audit(base + "/dT_through_at_max_K", dT, "Conditional on filed subsolar temperatures; global maximum not recoverable")
    audit(base + "/gradient_stress_Pa", gradient_per_K * dT, "Conditional on filed temperature difference")
    coeff = item["pattern"]["legendre_K"]
    for i in range(len(coeff)):
        audit(base + f"/pattern/legendre_K/{i}", basis="Angular temperature samples and projection quadrature absent")
    poly = Legendre([0., 0.] + coeff[2:]).convert(kind=Polynomial)
    ext = polynomial_extrema(poly)
    mu = Polynomial([0, 1])
    d2phi = (1 - mu * mu) * poly.deriv(2) - mu * poly.deriv()
    curvature = -alpha / R * d2phi
    kext = polynomial_extrema(curvature)
    analytic_bend = E * (tc + tf) * kext["max_abs"] / (2 * (1 - nu**2))
    audit(base + "/pattern/T_rest_max_K", ext["max_abs"],
          "Exact maximum absolute n=2..6 reconstruction; if field means untruncated residual, samples are required",
          "RECONSTRUCTION_MISMATCH")
    audit(base + "/pattern/kappa_max_1_per_m", kext["max_abs"],
          "Analytic angular derivative and stationary points of filed polynomial",
          "DISCRETIZATION_DIFFERENCE")
    audit(base + "/pattern/bending_stress_Pa", analytic_bend,
          "Same scalar bending screen, analytic curvature; not a shell equilibrium solution",
          "DISCRETIZATION_DIFFERENCE")
    bound_from_filed = E * alpha * item["pattern"]["T_rest_max_K"] / (1 - nu)
    audit(base + "/pattern/constrained_upper_Pa", bound_from_filed,
          "Arithmetic on filed residual maximum only; reconstruction discrepancy remains")
    correction(name, "constrained_upper_Pa_on_filed_polynomial",
               item["pattern"]["constrained_upper_Pa"],
               E * alpha * ext["max_abs"] / (1 - nu),
               "Same declared n=2..6 reconstruction; absolute maximum", "RECONSTRUCTION_MISMATCH")
    shears = {}
    for label, delta in [("day_rise", item["T_outer_subsolar_K"] - Ta),
                         ("swing", item["day_night_outer_swing_K"])]:
        bpath = base + "/shear_lag_from_" + label
        eps = (X["Al_alpha_per_K"] - alpha) * delta
        tau = eps * E * tf * lag_lambda
        sf = C["shear_strength_W_Pa"] / abs(tau)
        for field, v in [("d_eps", eps), ("lambda_1_per_m", lag_lambda),
                         ("tau_Pa", tau), ("SF_vs_shear_W", sf)]:
            audit(bpath + "/" + field, v, "Shear-lag algebra conditional on filed temperature and prescribed differential strain")
        shears[label] = {"tau_Pa": tau, "SF_typical": sf, "SF_min_average": sf * 25 / 35}
    # Energy residuals are diagnostic under this specified environment, not a
    # claim that the undocumented owner boundary conditions were recovered.
    residuals = {}
    for side in ["subsolar", "antisolar"]:
        To, Ti = item[f"T_outer_{side}_K"], item[f"T_inner_{side}_K"]
        absorbed = item["alpha"] * 970 * (side == "subsolar")
        qcond = conductance * (To - Ti)
        env4 = .5 * (275**4 + Ta**4)
        qrad = item["epsilon_out"] * SB * (To**4 - env4)
        residuals[side] = {
            "conduction_out_to_in_W_m2": qcond,
            "radiation_out_W_m2_equal_sky_ground_views": qrad,
            "required_h_W_m2K": (absorbed - qcond - qrad) / (To - Ta)
        }
    thermal[name] = {
        "gradient_stress_Pa": gradient_per_K * dT,
        "polynomial_extrema_K": ext, "curvature_extrema_1_m": kext,
        "analytic_bending_stress_Pa": analytic_bend,
        "implied_night_outer_K": item["T_outer_subsolar_K"] - item["day_night_outer_swing_K"],
        "shears": shears, "boundary_diagnostic": residuals,
        "maximum_admissible_temperature_change_K_typical": C["shear_strength_W_Pa"] / tau_per_K,
        "maximum_admissible_temperature_change_K_min_average": C["shear_strength_W_Pa"] * 25 / 35 / tau_per_K
    }

knot = X["owner_knot_m_s_for_replication"]
VB, U = 35 * knot, 35 * X["foot_m"]
q20, qVB = rho * 20**2 / 2, rho * VB**2 / 2
qgust = rho * VB * U + rho * U**2 / 2
q70, q78 = rho * (70 * knot)**2 / 2, rho * (78 * knot)**2 / 2
drag = lambda q: .47 * q * math.pi * R * R
Fmoor = 1.4 * drag(q20)
wind = {
    "q_20_Pa": q20, "q_20_over_p": q20 / p, "drag_20_N": drag(q20),
    "mooring_016_N": Fmoor, "VB_m_s": VB, "Ugust_35fps_m_s": U,
    "q_flight_stagnation_Pa": qgust, "q_flight_over_p": qgust / p,
    "q_VB_only_Pa": qVB, "q_moor_70kn_Pa": q70, "q_moor_70_over_p": q70 / p,
    "drag_70_N": drag(q70), "q_moor_78kn_Pa": q78, "drag_78_N": drag(q78),
    "potential_mean_dp_over_q": 1 - 2.25 * 2 / 3
}
for key, v in wind.items():
    audit("/wind/" + key, v, "Independent dynamic pressure, drag and analytic sphere area integral; owner's rounded knot conversion")
wind["total_aligned_flight_stagnation_Pa"] = qVB + qgust
verify("gust increment plus baseline equals full dynamic pressure", qVB + qgust,
       rho * (VB + U)**2 / 2)
wind["exact_unit_conversion"] = {
    "VB_m_s": 35 * 1852 / 3600,
    "q_gust_increment_Pa": rho * (35 * 1852 / 3600) * U + rho * U**2 / 2,
    "q_70_Pa": rho * (70 * 1852 / 3600)**2 / 2
}


def p2_modes(dp, extra_stress):
    pressure_stress = (p + dp) * R / (4 * tf)
    stress = pressure_stress + extra_stress
    modes = {name: capacity / ((p + dp) / 2 if name == "core_crush"
             else pressure_stress if name in ["global_buckling", "scarf_mean_shear"]
             else stress) for name, capacity in caps.items()}
    return {"modes": modes, "least_mode": min(modes, key=modes.get),
            "least_SF": min(modes.values()), "face_SF_on_345": 345e6 / stress,
            "demand_Pa": stress}


p2_variants = {}
cases = {
    "uniform": (0, None), "sun_coated_gradient_and_bend": (0, "coated_outer"),
    "sun_bare_gradient_and_bend": (0, "bare_Be"),
    "wind_flight_gust_uniform": (qgust, None), "wind_moor_70kn_uniform": (q70, None),
    "combined_coated_gust": (qgust, "coated_outer"), "combined_bare_gust": (qgust, "bare_Be")
}
for label, (dp, thermal_name) in cases.items():
    # Reproduce the seven-mode table with supplied thermal stresses. Its thermal
    # field and omitted bond modes remain separate findings.
    extra = 0 if thermal_name is None else (
        thermal[thermal_name]["gradient_stress_Pa"]
        + O["p2_thermal"][thermal_name]["pattern"]["bending_stress_Pa"])
    computed = p2_modes(dp, extra)
    p2_variants[label] = computed
    for mode, sf in computed["modes"].items():
        audit(f"/p2/{label}/modes/{mode}", sf,
              "Independent 028b capacities; filed thermal bending accepted only as conditional input")
    for field in ["least_mode", "least_SF", "face_SF_on_345", "demand_Pa"]:
        audit(f"/p2/{label}/{field}", computed[field], "Minimum and stress of independently evaluated seven screens")
    if thermal_name:
        verify(label + " gradient+bending decomposition", computed["demand_Pa"],
               (p + dp) * R / (4 * tf) + extra)
for field, name, case in [
    ("shear_lag_coated_swing_SF", "coated_outer", "swing"),
    ("shear_lag_bare_day_SF", "bare_Be", "day_rise"),
    ("shear_lag_bare_swing_SF", "bare_Be", "swing")
]:
    audit("/p2/" + field, thermal[name]["shears"][case]["SF_typical"], "Repeated conditional shear result")
scarf = sigma_p * 30 / 901
audit("/p2/scarf_pressure_stress_if_10MPa_Pa", scarf, "Projection of face compression onto 30:1 scarf")
audit("/p2/scarf_SF_if_10MPa_plus_coated_swing_shear",
      10e6 / (scarf + thermal["coated_outer"]["shears"]["swing"]["tau_Pa"]),
      "Scalar same-sign sum, conditional only; core shear and scarf shear require a load-path mapping")
coated_extra = thermal["coated_outer"]["gradient_stress_Pa"] + thermal["coated_outer"]["analytic_bending_stress_Pa"]
p2_fixed = p2_modes(qVB + qgust, coated_extra)
correction("P2 flight + coated", "seven_screen_least_SF",
           O["p2"]["combined_coated_gust"]["least_SF"], p2_fixed["least_SF"],
           "Include steady-flight qVB and gust increment at the owner's stated local-density/speed basis")
restore = O["restore"]
for field, val in [
    ("coated_combined_least_SF", p2_variants["combined_coated_gust"]["least_SF"]),
    ("coated_combined_least_mode", p2_variants["combined_coated_gust"]["least_mode"]),
    ("mass_to_restore_coated_combined_kg", 0.0),
    ("bare_swing_shear_SF", thermal["bare_Be"]["shears"]["swing"]["SF_typical"]),
    ("coated_swing_shear_SF", thermal["coated_outer"]["shears"]["swing"]["SF_typical"])
]:
    audit("/restore/" + field, val, "Seven-screen restoration only; all-mode restoration is unresolved")

pad_a = X["pad_replication"]
pad_loads = {
    "mooring_016_one_pad_SF1": (Fmoor, 1),
    "mooring_016_six_pads_SF1": (Fmoor, 6),
    "mooring_70kn_one_pad_SF1": (drag(q70), 1),
    "systems_100kg_six_pads": (100 * X["g_m_s2"], 6),
    "reserve_411kg_one_pad": (CASE["reserve_fixed_items_kg"] * X["g_m_s2"], 1)
}
pads = {}


def pad_size(force, count, available, exact_patch=False):
    share = force / count
    b = pad_a["boss_radius_m"]
    area = share / available
    if exact_patch:
        area = max(area, math.pi * b * b)
    a = math.sqrt(area / math.pi)
    coefficient = (1 + pad_a["nu"]) * math.log(a / b)
    if exact_patch:
        coefficient += 1 - (1 - pad_a["nu"]) * b * b / (4 * a * a)
    t = max(pad_a["minimum_t_m"], math.sqrt(max(0, 3 * share * coefficient
            / (2 * math.pi * pad_a["yield_Pa"]))))
    return {"area_one_m2": area, "radius_m": a, "thickness_m": t,
            "mass_one_kg": area * t * pad_a["rho"],
            "mass_total_kg": count * area * t * pad_a["rho"], "share_N": share}


for name, (force, count) in pad_loads.items():
    log_only = pad_size(force, count, C["crush_Pa"])
    patch = pad_size(force, count, C["crush_Pa"], True)
    pressure_patch = pad_size(force, count, C["crush_Pa"] - p / 2, True)
    for field, v in log_only.items():
        audit(f"/pads/{name}/{field}", v,
              "Recovered log-only expression with inferred boss radius, yield, nu and density; not a verified simply-supported solution")
    for field in ["area_one_m2", "radius_m", "thickness_m", "mass_total_kg"]:
        correction(name, field, log_only[field], patch[field],
                   "Uniform circular boss loading, simply supported edge; enforce pad radius >= boss radius",
                   "MODEL_DIFFERENCE")
    pads[name] = {"log_only_reproduction": log_only, "simply_supported_uniform_boss": patch,
                  "same_model_with_pressure_headroom": pressure_patch,
                  "original_radius_contains_boss": log_only["radius_m"] >= pad_a["boss_radius_m"],
                  "old_area_core_SF_if_p_over_2_adds": C["crush_Pa"] / (p / 2 + force / count / log_only["area_one_m2"])}
    verify(name + " force-area identity", log_only["area_one_m2"] * C["crush_Pa"], force / count)
audit("/pads/bare_016_patch_0p0707_SF", C["crush_Pa"] * .0707 / Fmoor, "Load-only core bearing screen")


def p3_baseline(s, ro, tw, film_t, material):
    A = math.pi * (ro**2 - (ro - tw)**2)
    I = math.pi / 4 * (ro**4 - (ro - tw)**4)
    length = 2 * R * math.asin(s / (2 * R))
    force = p * R * s / (2 * math.sqrt(3))
    frame_E = 410e9
    Fc = .38e9 if material == "mylar" else 3.9e9
    axial = force / A
    sigmaE = math.pi**2 * frame_E * I / (A * length**2)
    gamma = 1 - .901 * (1 - math.exp(-math.sqrt(ro / tw) / 16))
    sigmaL = .6 * frame_E * tw / ro * gamma
    eta = (length / 1000) * ro / (I / A)
    B = Fc + (1 + eta) * sigmaE
    perry = 2 * Fc * sigmaE / (B + math.sqrt(B**2 - 4 * Fc * sigmaE))
    film_stress = p * s / (2 * film_t)
    mode = {"yield": Fc / axial, "euler": sigmaE / axial, "local": sigmaL / axial,
            "film": X["film_properties"][material]["strength_Pa"] / film_stress,
            "perry": perry / axial,
            "global": .2 * 4 * math.sqrt(1.5) * frame_E * math.sqrt(I * A) / (s * R * R * p)}
    members = 24 * math.pi * R * R / (math.sqrt(3) * s * s)
    tube_mass = 3100 * A * length * members
    film_mass = 4 * math.pi * R * R * film_t * X["film_properties"][material]["rho"]
    return mode, force, film_stress, tube_mass, film_mass, A, I, length, members


p3 = []
for index, item in enumerate(O["p3"]):
    label = item["row"]
    material = label.rsplit("_", 1)[0]
    upstream = D["P3_022c_selected"][label]
    s, ro, tw, ft = [upstream[k] for k in ["s_m", "r_o_m", "t_w_m", "t_film_m"]]
    modes, force, film_stress, mtube, mfilm, area, inertia, length, members = p3_baseline(s, ro, tw, ft, material)
    base = f"/p3/{index}"
    audit(base + "/s_m", s, "022c cap geometry")
    half_wave = math.pi * math.sqrt(.75 * math.sqrt((ro**2 + (ro - tw)**2) / 2) * R)
    audit(base + "/half_wave_m", half_wave, "Declared formula; polar-radius definition retained")
    audit(base + "/half_wave_over_s", half_wave / s, "Declared half-wave / spacing")
    audit(base + "/in_band", half_wave / s >= 1, "Declared half-wave test")
    audit(base + "/governing_filed", min(modes, key=modes.get), "Independent minimum of 022c cap modes")
    for mode, sf in modes.items():
        audit(base + "/uniform/" + mode, sf, "Independent annular section, arc length, SiC and 022c mode equations")
    film_alpha = item["film_alpha"]
    audit(base + "/film_alpha", film_alpha, "Declared thermal material assumption", "DECLARED_INPUT")
    audit(base + "/thermal_day/film_alpha_used", film_alpha, "Selected film CTE")
    shadow = min(.85, 4 * math.sqrt(3) * ro / s)
    audit(base + "/thermal_day/shadow_fraction", shadow,
          "Projected member strip fraction, clipped at .85 (clip inferred from Mylar outputs)")
    for field in ["T_film_subsolar_K", "T_film_antisolar_K", "T_tube_subsolar_K", "T_tube_antisolar_K"]:
        audit(base + "/thermal_day/" + field, basis="Missing film/tube optical properties, heat balances, speed and complete view factors")
    for field in ["thermal_night_subsolar_film_K", "thermal_night_subsolar_tube_K"]:
        audit(base + "/" + field, basis="Night thermal boundary-value problem unspecified")
    film = X["film_properties"][material]
    frame_alpha_owner = {"projection": 4.5e-6, "mylar": 4.5e-6,
                         "ti_kapton": 8.6e-6, "cfrp_zylon": .5e-6}[material]
    Ttube = item["thermal_day"]["T_tube_subsolar_K"]
    Tfilm = item["thermal_day"]["T_film_subsolar_K"]
    eps_old = frame_alpha_owner * (Ttube - Ta) - film_alpha * (Tfilm - Ta)
    eps_sic = 4.5e-6 * (Ttube - Ta) - film_alpha * (Tfilm - Ta)

    def increment(eps):
        stress = film["E_Pa"] * eps / (1 - film["nu"])
        return {"eps_mechanical": eps, "film_stress_Pa": stress,
                "member_force_N": stress * ft * s / math.sqrt(3)}

    inc_old, inc_sic = increment(eps_old), increment(eps_sic)
    for field, v in inc_old.items():
        audit(base + "/mismatch/" + field, v,
              "Conditional on filed temperatures, owner frame CTE and inferred film nu; source material correction separate")
        if material in ["ti_kapton", "cfrp_zylon"]:
            correction(label, "mismatch." + field, item["mismatch"][field], inc_sic[field],
                       "Use SiC CTE for all tubes, holding unreproduced temperatures fixed")
    audit(base + "/member_force_N", force, "p R s / (2 sqrt(3))")
    audit(base + "/film_stress_Pa", film_stress, "p s / (2 film thickness)")
    audit(base + "/film_mass_kg", mfilm, "Full spherical area times gauge and inherited film density")
    audit(base + "/tube_mass_kg", mtube,
          "All 022c rows use SiC 3100 kg/m3 and arc length, not joint material density or chord length")
    old_combined = {key: sf / (1 + qgust / p + (
        inc_old["film_stress_Pa"] / film_stress if key == "film"
        else inc_old["member_force_N"] / force)) for key, sf in modes.items()}
    corrected_combined = {key: sf / (1 + (qgust + qVB) / p + (
        inc_sic["film_stress_Pa"] / film_stress if key == "film"
        else inc_sic["member_force_N"] / force)) for key, sf in modes.items()}
    for mode, sf in old_combined.items():
        audit(base + "/combined_flight_gust/" + mode, sf,
              "Reproduce declared scalar load multiplier on independent baseline; temperatures and CTE remain conditional")
        correction(label + f" alpha={film_alpha:g}", "combined_flight_gust." + mode,
                   item["combined_flight_gust"][mode], corrected_combined[mode],
                   "SiC CTE and total steady+gust dynamic pressure; frozen filed thermal fields")
    least = min(old_combined.values())
    mode = min(old_combined, key=old_combined.get)
    factor = max(1., 1 / least)
    audit(base + "/combined_least_SF", least, "Minimum of reproduced conditional modes")
    audit(base + "/combined_least_mode", mode, "Minimum of reproduced conditional modes")
    audit(base + "/optimism_or_thickness_factor_to_SF1", factor, "Reciprocal SF; not proof of proportional wall scaling")
    # This field can be reproduced using the owner's mass, but correcting mass
    # does not establish that increasing walls by 1/SF restores every mode.
    owner_part_mass = item["film_mass_kg"] if mode == "film" else item["tube_mass_kg"]
    audit(base + "/extra_mass_kg_if_that_part_scales", (factor - 1) * owner_part_mass,
          "Conditional proportional-mass arithmetic with filed mass; not a re-sized mass-closed design")
    corrected_least = min(corrected_combined.values())
    corrected_mode = min(corrected_combined, key=corrected_combined.get)
    corrected_factor = max(1., 1 / corrected_least)
    corrected_mass_screen = (corrected_factor - 1) * (mfilm if corrected_mode == "film" else mtube)
    correction(label, "extra_mass_kg_if_that_part_scales", item["extra_mass_kg_if_that_part_scales"],
               corrected_mass_screen, "Correct SiC/arc mass, SiC CTE and total flight q; proportional sensitivity only")
    audit(base + "/members_to_hold_mooring_add_to_5pct", math.ceil(Fmoor / (.05 * force)),
          "Scalar sharing count only; no attachment direction, equilibrium, capacity or fitting mass established")
    verify(label + " arc mass equals upstream", mtube, upstream["m_tube"])
    verify(label + " Euler independently implies SiC modulus",
           upstream["SF_euler"] * force * length**2 / (math.pi**2 * inertia), 410e9)
    p3.append({"row": label, "film_alpha": film_alpha, "baseline": modes,
               "tube_mass_kg": mtube, "film_mass_kg": mfilm,
               "owner_chord_implied_density_kg_m3": item["tube_mass_kg"] / (members * area * s),
               "arc_length_m": length, "chord_m": s, "corrected_mismatch_at_filed_temperatures": inc_sic,
               "corrected_combined_at_filed_temperatures": corrected_combined,
               "corrected_least": corrected_least, "corrected_mode": corrected_mode,
               "corrected_proportional_mass_sensitivity_kg": corrected_mass_screen})

correction("CARD.md P3 paragraph", "ti_kapton_5 uniform least",
           .74170, min(p3[6]["baseline"].values()),
           "Card quotes global as uniform least, but upstream film governs", "TEXT_MISMATCH")
correction("CARD.md Sun", "coated shear remains above 1", "coating keeps this mode above 1",
           "1.678 day-rise basis; 0.917 cold-night stress-free basis",
           "The same card's swing case is below unity", "TEXT_SCOPE")
correction("CARD.md Wind", "VB minimum rule", "VB at least 35 knots",
           "VB lower bound is min(35 knots, 0.65 VH), with design speeds EAS",
           "FAA-P-8110-2 §3.6(b), printed p12", "SOURCE_MISMATCH")
correction("CARD.md/NFI mooring", "78-knot ambiguity", "decision between 70 and 78",
           "Appendix explains old 78 was reduced to 70",
           "FAA-P-8110-2 Appendix B printed pp121–122; 78 remains optional sensitivity", "SOURCE_MISMATCH")
correction("INPUTS.json properties_QUESTIONABLE", "Be_sources alpha provenance",
           "11.3e-6 from S-200-F class, not a separate SR-200 coupon",
           "Current SR-200 manufacturer sheet itself lists typical 11.3 ppm/K at 25–100 C",
           "Pinned Materion SR-200 primary sheet; this improves attribution, not thin formed-sheet qualification",
           "SOURCE_IMPROVEMENT")


def numeric_paths(v, path=""):
    if isinstance(v, dict):
        for k, item in v.items():
            yield from numeric_paths(item, path + "/" + k)
    elif isinstance(v, list):
        for i, item in enumerate(v):
            yield from numeric_paths(item, path + "/" + str(i))
    elif isinstance(v, (int, float)) and not isinstance(v, bool):
        yield path


numeric = set(numeric_paths(O))
uncovered = sorted(numeric - seen)
assert not uncovered, uncovered
summary = {
    "numeric_fields": len(numeric), "numeric_fields_covered": len(numeric & seen),
    "audit_rows_including_labels": len(rows), "status_counts": dict(Counter(r["status"] for r in rows)),
    "checks": len(checks), "checks_passed": sum(c["passed"] for c in checks),
    "rtol": 1e-8, "atol": 1e-9,
    "unknown_policy": "Unspecified inputs are UNRESOLVED, never invented to force a match."
}
assert all(c["passed"] for c in checks)
result = {
    "schema": 1, "tag": "QUESTIONABLE / PROJECTION", "summary": summary,
    "gradient_coefficient_Pa_per_K": gradient_per_K,
    "core_conductance_W_m2K": conductance, "shear_lag_per_K_Pa": tau_per_K,
    "thermal": thermal, "wind": wind, "p2_reproduced_conditional": p2_variants,
    "p2_total_flight_and_analytic_coated_bending": p2_fixed,
    "mooring70_capacity_multiplier_to_SF1": 1 / p2_variants["wind_moor_70kn_uniform"]["least_SF"],
    "pads": pads, "p3": p3, "checks": checks
}
(ROOT / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
(ROOT / "AUDIT.json").write_text(json.dumps(rows, indent=2) + "\n")
(ROOT / "CORRECTIONS.json").write_text(json.dumps(corrections, indent=2) + "\n")
for name, entries in [("AUDIT.csv", rows), ("CORRECTIONS.csv", corrections)]:
    with (ROOT / name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(entries[0]))
        writer.writeheader()
        writer.writerows(entries)
print(json.dumps(summary, indent=2))
