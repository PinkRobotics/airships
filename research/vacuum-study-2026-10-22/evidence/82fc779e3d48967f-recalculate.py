"""Independent MAINLINE-024 arithmetic, frame optimization and accounting check."""
import json
import math
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "INPUTS.json").read_text())
OWNER = DATA["owner_results"]
C = DATA["frame"]["constants"]
MAT = DATA["frame"]["material"]
R, P, LIFT = C["R_m"], C["p_ext_Pa"], C["lift_mass_kg"]
AREA, VOLUME = 4 * math.pi * R**2, 4 * math.pi * R**3 / 3
S0 = DATA["film_bay_m"]
GAS = DATA["gas_constants"]
BAR = DATA["barrier_inputs"]
comparisons = []


def compare_tree(filed, own, path=""):
    """Check every numeric leaf in the filed record, excluding schema metadata."""
    if isinstance(filed, bool):
        return
    if isinstance(filed, dict):
        for key, value in filed.items():
            if key == "schema":
                continue
            compare_tree(value, own.get(key), f"{path}.{key}" if path else key)
    elif isinstance(filed, list):
        for idx, value in enumerate(filed):
            compare_tree(value, own[idx] if own is not None else None, f"{path}[{idx}]")
    elif isinstance(filed, (int, float)):
        matches = own is not None and math.isclose(filed, own, rel_tol=3e-11, abs_tol=2e-12)
        comparisons.append({
            "field": path, "filed": filed, "checker": own,
            "difference": own - filed if own is not None else None,
            "relative_difference": own / filed - 1 if own is not None and filed != 0 else None,
            "matches": matches,
        })


def frame_mass(s, film_mass):
    vertices = 8 * math.pi * R**2 / (math.sqrt(3) * s**2) + 2
    nodes = C["node_kg"] * vertices
    budget = LIFT - film_mass - nodes - C["systems_kg"]
    tubes = budget / (1 + C["joint_frac"])
    joints = C["joint_frac"] * tubes
    length = (3 * vertices - 6) * s
    cross_section = tubes / (MAT["rho"] * length)
    return nodes, budget, tubes, joints, cross_section


def frame_score(s, ro, film_mass, film_capacity_coefficient):
    nodes, budget, tubes, joints, a = frame_mass(s, film_mass)
    ri = math.sqrt(max(0.0, ro**2 - a / math.pi))
    wall = ro - ri
    inertia = math.pi * (ro**4 - ri**4) / 4
    axial_load = P * R * s / 2
    stress = axial_load / a
    euler_stress = math.pi**2 * MAT["E_Pa"] * inertia / (a * s**2)
    eta = (s / 1000) * ro / (inertia / a)
    summation = MAT["sigma_Pa"] + (1 + eta) * euler_stress
    # Stable form of the smaller root of the Perry quadratic.
    perry = 2 * MAT["sigma_Pa"] * euler_stress / (
        summation + math.sqrt(summation**2 - 4 * MAT["sigma_Pa"] * euler_stress))
    sfs = {
        "global": 0.2 * 4 * math.sqrt(1.5) * MAT["E_Pa"] * math.sqrt(inertia * a) / (s * R**2 * P),
        "film": film_capacity_coefficient / s,
        "yield": MAT["sigma_Pa"] / stress,
        "euler": euler_stress / stress,
        "local": C["C_local"] * MAT["E_Pa"] * wall / ro / stress,
        "perry": perry / stress,
    }
    ranking = sorted(sfs.items(), key=lambda kv: kv[1])
    result = {
        "s_m": s, "r_o_m": ro, "t_w_m": wall,
        "m_nodes_kg": nodes, "m_joint_kg": joints, "m_tube_kg": tubes,
        "m_film_kg": film_mass, "budget_kg": budget,
        "SF_least": ranking[0][1], "governing": ranking[0][0],
        "second": ranking[1][0], "SF_second": ranking[1][1],
        "closure_kg": tubes + joints + nodes + film_mass + C["systems_kg"],
        "A_m2": a, "I_m4": inertia, "sigma_axial_Pa": stress, "eta_Perry": eta,
    }
    result.update({"SF_" + k: v for k, v in sfs.items()})
    return result


def golden_max(function, a, b):
    ratio = (math.sqrt(5) - 1) / 2
    x, y = b - ratio * (b - a), a + ratio * (b - a)
    fx, fy = function(x), function(y)
    for _ in range(85):
        if fx < fy:
            a, x, fx = x, y, fy
            y = a + ratio * (b - a)
            fy = function(y)
        else:
            b, y, fy = y, x, fx
            x = b - ratio * (b - a)
            fx = function(x)
    return max([(function(a), a), (function(b), b), (function((a + b) / 2), (a + b) / 2)])


def best_radius(s, film_mass, film_capacity):
    area = frame_mass(s, film_mass)[-1]
    lo = math.sqrt(area / math.pi) * (1 + 1e-9)
    hi = min(s / 3, 0.25)
    _, ro = golden_max(lambda x: frame_score(s, x, film_mass, film_capacity)["SF_least"], lo, hi)
    return frame_score(s, ro, film_mass, film_capacity)


def optimize(film_mass, film_capacity):
    # Independently cover every prescribed bay; radii are continuous.
    rows = [best_radius(i / 50, film_mass, film_capacity) for i in range(20, 151)]
    best = max(rows, key=lambda row: row["SF_least"])
    s = best["s_m"]
    _, refined_s = golden_max(
        lambda span: best_radius(span, film_mass, film_capacity)["SF_least"],
        max(0.4, s - 0.02), min(3.0, s + 0.02))
    return {
        "bay_grid": "0.40 to 3.00 m in 0.02 m steps",
        "radius_method": "Independent continuous bounded minimax optimization; no owner radius grid or code used.",
        "best_on_bay_grid": best,
        "refined_bay_and_radius": best_radius(refined_s, film_mass, film_capacity),
    }


circum = S0 / math.sqrt(3)
expected = {
    "geometry": {
        "bay_m": S0, "curvature_radius_m": S0,
        "triangle_circumradius_m": circum,
        "cap_rise_m": S0 - math.sqrt(S0**2 - circum**2),
        "hemisphere_not_used_m": circum,
        "line_load_011b_N_per_m": P * S0 / 2,
        "line_load_triangle_share_N_per_m": P * S0 * math.sqrt(3) / 6,
        "pin_stress_at_80um_Pa": P * S0 / (2 * C["t_film_m"]),
        "pin_film_mass_check_kg": AREA * C["t_film_m"] * C["rho_film"],
        "hull_area_m2": AREA,
    },
}
candidate_rows = []
for material in DATA["materials"]:
    allowable = material["ultimate_Pa"] * material["knockdown"]
    plies = 2 if material["form"] == "filament_crossply" else 1
    thickness = plies * P * S0 / (2 * allowable)
    areal = material["density_kg_m3"] * thickness
    candidate_rows.append({
        "key": material["key"],
        **{k: material[k] for k in ["ultimate_Pa", "knockdown", "modulus_Pa", "density_kg_m3"]},
        "design_allowable_Pa": allowable, "thickness_m": thickness,
        "pillow_stress_Pa": P * S0 / (2 * thickness / plies),
        "curvature_radius_m": S0, "areal_kg_m2": areal, "mass_kg": areal * AREA,
        "against_pin_kg": areal * AREA - C["film_kg"],
    })
candidate_rows += [
    {"thickness_m": 12e-6, "pillow_stress_Pa": P * S0 / (2 * 12e-6), "curvature_radius_m": S0},
    {"curvature_radius_m": S0}, {"curvature_radius_m": S0},
]
expected["candidates"] = candidate_rows
by_key = {row["key"]: row for row in candidate_rows if "key" in row}


def cc_mass(volume_cc, species):
    return volume_cc * GAS["M_" + species + "_kg_mol"] / GAS["Vm_STP_cm3_mol"]


def pump_record(load):
    return {"sourced_kg_per_day": load, "allowance_kg_per_day": DATA["pump_allowance_kg_day"],
            "pump_kg_band": DATA["pump_inherited"]["mass_band_kg"]}


kapton, pen = by_key["kapton_hn"], by_key["teonex_q51"]
kb, pb, mb, ab = (BAR[k] for k in ["kapton", "pen", "mylar", "ald"])
kap_gas = {}
for gas, label in [("O2", "o2_kg_day"), ("N2", "n2_kg_day")]:
    volume = kb[gas + "_ml_m2_day_MPa"] * (P * GAS["x_" + gas] / 1e6)
    volume *= kb["reference_thickness_m"] / kapton["thickness_m"] * AREA
    kap_gas[label] = cc_mass(volume, gas)
kap_gas["h2o_kg_day_at_table"] = kb["water_g_m2_day"] / 1000 * AREA * kb["reference_thickness_m"] / kapton["thickness_m"]
kap_gas["sum_o2_n2_kg_day"] = kap_gas["o2_kg_day"] + kap_gas["n2_kg_day"]
kap_gas["pump"] = pump_record(kap_gas["sum_o2_n2_kg_day"] + kap_gas["h2o_kg_day_at_table"])
pen_oxygen_cc_m2_day = (
    pb["O2_cc_cm_cm2_s_cmHg"] * (P * GAS["x_O2"] / GAS["atm_Pa"] * GAS["cmHg_per_atm"])
    / (pen["thickness_m"] * 100) * 1e4 * GAS["seconds_per_day"])
pen_gas = {
    "o2_cc_m2_day": pen_oxygen_cc_m2_day,
    "o2_kg_day": cc_mass(pen_oxygen_cc_m2_day * AREA, "O2"),
    "h2o_kg_day_at_table": pb["water_g_m2_day"] / 1000 * AREA * pb["reference_thickness_m"] / pen["thickness_m"],
}
pen_gas["pump"] = pump_record(pen_gas["o2_kg_day"] + pen_gas["h2o_kg_day_at_table"])
mylar = {
    "metallised_od3_12um": {
        "o2_kg_day": cc_mass(mb["O2_cc_m2_day_metal"] * P * GAS["x_O2"] / GAS["atm_Pa"] * AREA, "O2"),
        "h2o_kg_day_upper_at_38C_90RH": mb["water_g_m2_day_metal_upper"] / 1000 * AREA,
    },
    "plain_12um": {
        "o2_kg_day": cc_mass(mb["O2_cc_m2_day_plain"] * P * GAS["x_O2"] / GAS["atm_Pa"] * AREA, "O2"),
        "h2o_kg_day_at_38C_90RH": mb["water_g_m2_day_plain"] / 1000 * AREA,
    },
}
mylar["pump_metallised"] = pump_record(sum(mylar["metallised_od3_12um"].values()))
ald = {
    "thickness_m": ab["thickness_m"],
    "o2_kg_day_upper": cc_mass(ab["O2_cc_m2_day_upper"] * AREA, "O2"),
    "h2o_kg_day": ab["water_g_m2_day"] / 1000 * AREA,
}
ald["pump"] = pump_record(ald["o2_kg_day_upper"] + ald["h2o_kg_day"])
expected["gas"] = {"kapton_design": kap_gas, "pen_design": pen_gas, "mylar": mylar, "ald_26nm": ald}
expected["allowance_kg_day"] = DATA["pump_allowance_kg_day"]
expected["pump_kg_band"] = DATA["pump_inherited"]["mass_band_kg"]
pin_capacity = 2 * C["sigma_film_Pa"] * C["t_film_m"] / P
filed_pin = OWNER["pin_reproduction"]
expected["pin_reproduction"] = frame_score(filed_pin["s_m"], filed_pin["r_o_m"], C["film_kg"], pin_capacity)
optimizations = {"pin": optimize(C["film_kg"], pin_capacity)}
for field, key in [("lightest_design_row", "zylon_hm_crossply"), ("lightest_biaxial_film", "kapton_hn")]:
    row = by_key[key]
    filed = OWNER[field]["scan"]
    own = frame_score(filed["s_m"], filed["r_o_m"], row["mass_kg"], S0)
    expected[field] = {
        "mass_kg": row["mass_kg"], "areal_kg_m2": row["areal_kg_m2"],
        "film_sf_at_2p04": 1.0, "scan": own,
    }
    optimizations[key] = optimize(row["mass_kg"], S0)
compare_tree(OWNER, expected)

result = {
    "schema": 1, "unit": DATA["unit"], "card": "MAINLINE-024 independent check",
    "tag": "QUESTIONABLE", "design_transfer_tag": "PROJECTION", "certification": False,
    "started_at": DATA["started_at"], "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    "independence": DATA["independence"],
    "comparison_tolerance": {"relative": 3e-11, "absolute": 2e-12},
    "comparison_count": len(comparisons), "comparisons": comparisons,
    "mismatches": [row for row in comparisons if not row["matches"]],
    "recomputed_filed_points": expected,
    "independent_optimizations": optimizations,
    "sag_accounting": {
        "charged_in_filed_card": False,
        "sphere_volume_m3": VOLUME, "gross_lift_kg": LIFT,
        "charged_volume_loss_m3": 0.0, "charged_lift_loss_kg": 0.0,
        "air_density_kg_m3": LIFT / VOLUME,
        "lost_lift_kg_per_mean_radial_mm_linearized": LIFT / VOLUME * AREA / 1000,
        "basis": "Every reported closure equals original L with 50 kg systems. No sag shape integral, displaced-volume correction or lift deduction appears in the numeric record.",
        "limitation": "The cap-rise scalar alone does not define a boundary-compatible pillow over a triangular bay; no unique loss volume is inferred from it.",
    },
    "unbooked_system_terms": {
        "resin_and_barrier_mass_in_zylon_row_kg": None,
        "pump_mass_band_kg": DATA["pump_inherited"]["mass_band_kg"],
        "all_systems_allowance_in_scan_kg": C["systems_kg"],
        "minimum_extra_pump_mass_if_all_systems_allowance_reallocated_kg":
            DATA["pump_inherited"]["mass_band_kg"][0] - C["systems_kg"],
        "pump_reallocation_gap_band_kg":
            [mass - C["systems_kg"] for mass in DATA["pump_inherited"]["mass_band_kg"]],
    },
    "other_checks": {
        "ALD_density_for_one_kg_kg_m3": 1 / (AREA * ab["thickness_m"]),
        "zylon_1e7_minutes_years_at_365p25_days": 1e7 / (60 * 24 * 365.25),
        "lift_allowance_recomputed_full_precision_kg_day": 0.01 * 4889.442150186961,
    },
}
(HERE / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({
    "comparison_count": result["comparison_count"], "mismatches": result["mismatches"],
    "optimizations": {key: {
        "grid_best_s": val["best_on_bay_grid"]["s_m"],
        "grid_best_SF": val["best_on_bay_grid"]["SF_least"],
        "refined_s": val["refined_bay_and_radius"]["s_m"],
        "refined_SF": val["refined_bay_and_radius"]["SF_least"],
    } for key, val in optimizations.items()},
    "sag": result["sag_accounting"], "other_checks": result["other_checks"],
}, indent=2))
