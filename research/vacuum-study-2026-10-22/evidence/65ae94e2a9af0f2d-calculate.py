"""Auditable arithmetic for a test plan, not a new design optimization or FE solve."""
from pathlib import Path
import csv
import json
import math

HERE = Path(__file__).resolve().parent
I = json.loads((HERE / "INPUTS.json").read_text())
p = I["case"]["p0_Pa"]
R = 10.0
area = 4 * math.pi * R**2
volume = area * R / 3
lift = I["case"]["lift0_kg"]
old = I["P2_021b"]
new = I["P2_028b_routes"]["af015_scarf"]
core = new["core"]
rows = []

def outcome(test, value, unit, affected, sf, reserve=None, note=""):
    rows.append(dict(test=test, measured_or_assumed_value=value, unit=unit,
                     affected_mode=affected, affected_mode_SF=sf,
                     fixed_P2_all_other_named_modes_at_threshold_SF=(
                         min(1., sf) if sf is not None and test.startswith("P2") else None),
                     delta_mass_or_reserve_kg=reserve, note=note))

for value in [.2, .45, new["needed"]["gamma"], .60]:
    outcome("P2 gamma", value, "dimensionless", "global buckling",
            value / new["needed"]["gamma"],
            note="Same 028b geometry, E=290 GPa and core; a surrogate result needs model transfer.")
for value in [.33, new["needed"]["wrinkle"], .61, .82]:
    outcome("P2 wrinkle", value, "dimensionless", "wrinkling",
            value / new["needed"]["wrinkle"],
            note="Coefficient inferred with measured core/face properties, same convention.")
for value in [255., 280., new["face_demand_Pa"] / 1e6, 345.]:
    outcome("P2 compression", value, "MPa", "face compression",
            value * 1e6 / new["face_demand_Pa"],
            note="Post-process strength screen, not a statistical allowable.")
for value in [6., 8., 10., 12.]:
    outcome("P2 scarf", value, "MPa mean shear", "scarf mean-shear screen",
            value / 10., note="Peel, local instability, cyclic damage still unquantified.")
for value in [0., 5., 10., 25.]:
    outcome("P2 added bond/primer mass", value, "g/m2 on EACH of two interfaces",
            "mass closure", None, area * 2 * value / 1000,
            "Same geometry is heavier by this amount; no unused joining allowance on nominal route.")
for value in [0., 2., 10.]:
    outcome("P2 added seam mass", value, "g/m physical coincident seam",
            "mass closure", None, new["joining"]["seam_length_m"] * value / 1000,
            "Increment includes both skins; do not double count coincident seam length.")

scale_rows = []
for name, pt, nu, delta_ratio in [
    ("021b historical", old, .33, old["tolerance_015_at_needed_gamma"]["delta_over_t_eq"]),
    ("028b current", new, new["nu"], old["tolerance_015_at_needed_gamma"]["delta_over_t_eq"]),
]:
    tf = pt["tf_m"]
    tc = pt.get("tc_m", pt.get("core_m"))
    h = tf + tc
    G = core["Gc_Pa"]
    E = 290e9
    sig0 = E * h / (R * math.sqrt(1 - nu**2))
    sigcrimp = h*h*G / (2*tf*tc)
    vc = sig0 / sigcrimp
    kc = 1 - vc/4
    pref = 4 * kc * sig0 * tf / R
    gamma_need = pt.get("needed", pt.get("needed_values"))["gamma"]
    assert abs(pref * gamma_need / p - 1) < 1e-12
    # These are explicit planning floors, not demonstrated supplier minima.
    rmin = R * max(25e-6 / tf, 1e-3 / tc)
    for r_test in [.25, rmin, .5, 1., 2., 20.]:
        k = r_test / R
        for material, et, nut in [("same Be", E, nu), ("Al elastic surrogate", 69e9, .33)]:
            pressure_ratio = et/E * math.sqrt(1-nu**2)/math.sqrt(1-nut**2)
            gt = G * pressure_ratio
            # Set G so Vc is preserved exactly with same geometry ratios.
            vc_test = (et * (h*k) / (r_test * math.sqrt(1-nut**2))) / (
                (h*k)**2 * gt / (2*(tf*k)*(tc*k)))
            row = {
                "reference": name, "material": material, "R_m": r_test,
                "diameter_m": 2*r_test, "scale": k,
                "tf_um": tf*k*1e6, "tc_mm": tc*k*1e3,
                "scaled_cell_mm": core["s_cell_m"]*k*1e3,
                "delta_mm": delta_ratio*math.sqrt(3)*h*k*1e3,
                "delta_over_t_eq": delta_ratio,
                "delta_note": ("021b tolerance-map amplitude" if name.startswith("021b")
                               else "imposed comparison amplitude, NOT a qualified 028b tolerance"),
                "R_over_tc": r_test/(tc*k), "Vc": vc_test,
                "E_GPa": et/1e9, "nu": nut, "Gc_target_MPa": gt/1e6,
                "design_pressure_kPa": p*pressure_ratio/1000,
                "gamma1_reference_kPa": pref*pressure_ratio/1000,
                "pressure_scale_relative_to_Be": pressure_ratio,
                "ambient_101325Pa_max_gamma": 101325/(pref*pressure_ratio),
                "planning_gauge_floors_satisfied": tf*k >= 25e-6*(1-1e-12) and tc*k >= 1e-3*(1-1e-12),
                "conditional_min_R_m": rmin,
                "SR200_0p508mm_sheet_gauge_min_R_m": R*.000508/tf,
                "surrogate_face_stress_at_design_MPa": p*R/(4*tf)*pressure_ratio/1e6,
                "surrogate_face_stress_at_gamma1_MPa": pref*R/(4*tf)*pressure_ratio/1e6,
                "unscaled_cell_dimple_SF": (
                    (old["at_needed_values"]["sfs"]["intracell_dimpling"] if name.startswith("021b")
                     else new["at_needed"]["six_modes"]["intracell_dimpling"]) * k*k
                    if material == "same Be" else None),
            }
            scale_rows.append(row)

P = I["P3_022c"]["projection_019"]["equilateral"]
sigma_mean = P["N_N"] / P["A_m2"]
sigE = P["SF_euler"] * sigma_mean
eta = (P["length_m"]/1000) * P["r_o_m"] / (P["I_m4"]/P["A_m2"])

def perry_sf(sig):
    phi = (sig+(1+eta)*sigE)/2
    # Rationalized small root avoids cancellation.
    return sig*sigE/(phi+math.sqrt(phi*phi-sig*sigE))/sigma_mean

for value in [.38, 1., 1.2, 3.9]:
    perry = perry_sf(value*1e9)
    rows.append(dict(test="P3 compression", measured_or_assumed_value=value, unit="GPa",
                     affected_mode="mean compression and inherited Perry surrogate",
                     affected_mode_SF=value*1e9/sigma_mean,
                     inherited_Perry_SF=perry,
                     conditional_least_scored_SF=min(perry, value*1e9/sigma_mean,
                                                    P["SF_local"], P["SF_film"], P["SF_global"]),
                     note="Global smeared screen unvalidated at this spacing; not installed-hull SF."))
film_demand = p * P["s_m"] / (2*P["t_film_m"])
for value in [.1155, .5, 1., 1.5]:
    outcome("P3 film", value, "GPa effective sustained biaxial strength",
            "film", value*1e9/film_demand,
            note="Fixed filed gauge/density; replacement mass, laminate directionality and sag require recalculation.")

gas_allow = .01 * lift
temperature = I["case"]["T0_K"]
Rd = 287.05
q_limit = gas_allow * Rd * temperature / 86400
vacuum = {
    "gas_mass_allowance_kg": gas_allow,
    "T_reference_K": temperature,
    "dry_air_R_J_kg_K": Rd,
    "derived_q_limit_Pa_m3_s": q_limit,
    "filed_019_q_limit_Pa_m3_s": 46.28072023084111,
    "density_convention_note": "Derived from gas mass and Rd; slight difference from filed 0.01*p*V/day is retained.",
    "pressure_rise_limit_Pa_s": .01*p/86400,
    "full_hull_volume_m3": volume,
    "full_hull_area_m2": area,
    "area_only_q_limit_Pa_m3_s_m2": 46.28072023084111/area,
    "seam_only_q_limit_Pa_m3_s_m": 46.28072023084111/new["joining"]["seam_length_m"],
    "allocation_note": "Area-only and seam-only limits are separate upper bounds, not simultaneous budgets.",
    "panel_area_m2": .6*.6,
    "shared_chamber_volume_m3": .01,
    "panel_area_only_budget_Pa_m3_s": 46.28072023084111/area*.36,
    "panel_chamber_area_only_dpdt_Pa_s": 46.28072023084111/area*.36/.01,
    "q_definition": "Q_ref = T_ref*d(pV/T)/dt, summed by gas species for mass. Subtract blank fixture, not specimen outgas.",
}
for kgday in [1., 10., gas_allow, 100.]:
    vacuum.setdefault("outcomes", []).append({
        "whole_hull_gas_kg_day": kgday,
        "sealed_days_to_1pct_lift_from_zero_initial_gas": gas_allow/kgday,
        "24h_extra_mass_beyond_existing_gas_allowance_kg": max(0., kgday-gas_allow),
        "72h_extra_mass_beyond_existing_gas_allowance_kg": max(0., 3*kgday-gas_allow),
    })

r20 = next(x for x in I["P2_R20_027"]
           if x["mass_model"] == "coupled" and x["mechanical"] == "full_021")
result = {
    "schema": 1, "card": "MAINLINE-038", "status": "QUESTIONABLE/PROJECTION",
    "not_an_optimization": True,
    "P2_current": new,
    "P2_historical": old,
    "P2_zero_core_compression_necessary_MPa": (
        255 / I["P2_255_upper_bound"]["face_SF_upper_bound_even_with_zero_core"]),
    "P2_036_refinement": {
        "R10_full_projected_gamma_wrinkle_min_compression_MPa": 298.906,
        "R20_held_face_demand_MPa": 338.744,
        "R20_held_material_with_eta0p9_MPa": 376.382,
        "R20_reoptimized_handbook_scalar_elasticity_required_MPa": 381.612,
        "R20_historical_379p2MPa_with_handbook_scalar_elasticity_SF": .994817,
        "source": "Pinned MAINLINE-036 report and CARD; quoted precision only.",
    },
    "P2_R20_separate_027_point": r20,
    "P3_current_reference": P,
    "P3_current_reference_note": "Field retained for reproducibility: this is frozen 022c, superseded for procurement by P3_022d below.",
    "P3_current_film_demand_GPa": film_demand/1e9,
    "P3_current_mean_compression_GPa": sigma_mean/1e9,
    "P3_perry_eta": eta,
    "P3_3p9_Perry_reproduction": perry_sf(3.9e9),
    "P3_joint_dimensionless_stiffness": {
        "EI_N_m2": 410e9*P["I_m4"], "EI_over_L_Nm_per_rad": 410e9*P["I_m4"]/P["length_m"],
        "beta_definition": "Ktheta*L/(E*I), measured for both bending axes and member roll",
        "required_beta": None, "why_null": "Requires discrete-frame sweep at actual topology, not an assumed rigid boundary.",
        "N_full_N": P["N_N"], "one_fifth_geometric_N_N": P["N_N"]*.2**2,
        "end_mass_wrap_projection_kg": 5.807e-15*P["N_N"]**2/P["r_o_m"],
        "end_mass_Ti_projection_kg": 2.950e-14*P["N_N"]**2/P["r_o_m"],
        "allowance_per_member_end_kg": P["m_joint"]/(2*P["members"]),
    },
    "film_bulge": {
        "test_triangle_side_m": .3,
        "scaled_film_um_for_same_pressure": P["t_film_m"]*.3/P["s_m"]*1e6,
        "actual_gauge_bulge_required_pressure_MPa": p*P["s_m"]/.3/1e6,
        "actual_gauge_bulge_at_1p5GPa_MPa": 2*1.5e9*P["t_film_m"]/.3/1e6,
        "interpretation": "Assumes measured cap curvature radius equals side; real triangular membrane must use its resolved curvature/tension field.",
    },
    "scaling": scale_rows,
    "outcomes": rows,
    "vacuum": vacuum,
    "mass_sensitivities": {
        "one_g_m2_extra_one_layer_kg": area/1000,
        "one_g_m2_each_of_two_interfaces_kg": 2*area/1000,
        "one_g_m_seam_kg": new["joining"]["seam_length_m"]/1000,
        "extra_10g_node_P3_kg": .01*P["nodes"],
        "extra_10g_each_member_end_P3_kg": .01*2*P["members"],
        "primer_5g_each_interface_kg": .005*2*area,
        "double_nominal_core_bond_film_extra_kg": new["joining"]["bond_kg"],
    },
    "statistical_example": {
        "n_zero_failures_to_bound_failure_prob_below_0p001_at_95pct": math.ceil(math.log(.05)/math.log(.999)),
        "limitations": "Independent identical Bernoulli exposures only; no size, lifetime, multi-mode or confidence-allowable transfer.",
    },
}
latest = []
for x in I["P3_022d_selected"]:
    zylon = x["case"]["family"] == "cfrp_zylon"
    total_strength = 1.74e9 if zylon else 1.5e9
    dfilm = p*x["s_m"]/(2*x["film_total_m"])
    rr = dict(
        key=x["key"], source=x,
        film_effective_total_gauge_demand_GPa=dfilm/1e9,
        film_directional_ply_demand_GPa=(2*dfilm/1e9 if zylon else None),
        small_bulge_actual_gauge_pressure_MPa=p*x["s_m"]/.3/1e6,
        small_bulge_same_pressure_total_gauge_um=x["film_total_m"]*.3/x["s_m"]*1e6,
        joint_scaled_one_fifth_operating_N=x["force_at_pressure_1_N"]*.04,
        joint_scaled_one_fifth_target_N=x["joint"].get("design_force_N", 0)*.04 if zylon else None,
        joint_mass_each_end_kg=x["mass_kg"]["joint"]/(2*x["members"]),
        joint_EI_over_L_Nm_per_rad=410e9*x["inertia_m4"]/x["member_length_m"],
    )
    rrows = []
    for fc in [.38e9, 1e9, 1.2e9, 3.9e9]:
        se = x["euler_stress_Pa"]
        phi = (fc+(1+x["eta"])*se)/2
        psf = fc*se/(phi+math.sqrt(phi*phi-fc*se))/x["axial_stress_at_pressure_1_Pa"]
        rrows.append({"assumed_Fc_GPa":fc/1e9,
                      "mean_compression_SF":fc/x["axial_stress_at_pressure_1_Pa"],
                      "inherited_Perry_SF":psf,
                      "compression_plus_bending_demand_at_pressure_1_GPa":
                          x["stresses"]["operating_pressure"]["max_compression_Pa"]/1e9})
    rr["compression_sensitivities"] = rrows
    rr["film_sensitivities"] = [
        {"effective_total_gauge_strength_GPa": v,
         "film_SF": v*1e9/dfilm,
         "directional_ply_strength_GPa_if_crossply": 2*v if zylon else None}
        for v in ([.5,1.,1.5,1.74] if zylon else [.1155,.5,1.,1.5])]
    assert abs(total_strength/dfilm-x["SF"]["film"]) < 1e-9
    latest.append(rr)
result["P3_022d"] = latest
(HERE/"RESULTS.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
for name, data in [("OUTCOMES.csv", rows), ("SHELL-SCALING.csv", scale_rows)]:
    keys = list(dict.fromkeys(k for row in data for k in row))
    with (HERE/name).open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
print(json.dumps({
    "P2_necessary_strength_MPa": result["P2_zero_core_compression_necessary_MPa"],
    "P3_perry_reproduction_error": perry_sf(3.9e9)-P["SF_perry"],
    "half_metre_models": [x for x in scale_rows if x["R_m"]==.5],
    "vacuum": vacuum, "R20_tf_mm": r20["tf_m"]*1000, "R20_tc_mm": r20["tc_m"]*1000,
    "R20_face_SF": r20["modes"]["face_compression"], "joint": result["P3_joint_dimensionless_stiffness"],
}, indent=2))
