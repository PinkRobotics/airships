#!/usr/bin/env python3
"""MAINLINE-019: independent mass budget and two-family margin optimisation.

Run prepare_inputs.py once, then this file. No predecessor code is imported.
Only this directory is written. Formulas and numeric checks are recorded below.
"""
from __future__ import annotations

import copy
import json
import math
from datetime import datetime
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parent
I = json.loads((ROOT / "INPUTS.json").read_text())
C = I["case"]
R, P, L, T = C["radius_m"], C["p0_Pa"], C["lift0_kg"], C["T0_K"]
A, V = 4 * math.pi * R**2, 4 * math.pi * R**3 / 3
NU, KD, J, SYS = C["nu"], C["kd"], C["joint_fraction"], C["system_allowance_kg"]
FACE = I["face"]
BX = brentq(lambda x: x**3 + x - 1, 0, 1, xtol=1e-15)
LB_FT2_TO_KG_M2 = 0.45359237 / 0.3048**2
MODES = ("global_buckling", "face_compression", "core_crush",
         "core_shear_crimping", "face_wrinkling", "intracell_dimpling")


def structure(margin):
    return (L - SYS - margin) / (1 + J)


def evaluate(fraction, margin, core, young=None):
    """Scalar/array scoring; exactly the inherited branch rule, plus dimpling."""
    f = np.asarray(fraction)
    young = FACE["E_Pa"] if young is None else young
    s = structure(margin)
    tf = (1 - f) * s / (2 * A * FACE["rho"])
    tc = f * s / (A * core["rho"])
    h = tf + tc
    sig0 = young * h / (R * math.sqrt(1 - NU**2))
    sigcr = h**2 * core["Gc_Pa"] / (2 * tf * tc)
    vc = sig0 / sigcr
    crimp_branch = vc > 2
    kc = np.where(crimp_branch, 1 / vc, 1 - vc / 4)
    gamma = np.where(crimp_branch, 1., KD)
    membrane = P * R / (4 * tf)
    values = np.stack([
        gamma * kc * 4 * sig0 * tf / R / P,
        4 * FACE["sigma_Pa"] * tf / R / P,
        np.ones_like(f) * core["crush_Pa"] / (P / 2),
        4 * sigcr * tf / R / P,
        BX * 0.33 * np.sqrt(young * core["Ec_Pa"] * tf / tc) / membrane,
        2 * young / (1 - NU**2) * (tf / core["s_cell_m"])**2 / membrane,
    ])
    return dict(tf=tf, tc=tc, Vc=vc, Kc=kc, gamma=gamma,
                values=values, least=values.min(axis=0))


def optimum(margin, family, young=None, grid_n=2001):
    """Scan every local peak; refine peaks and both sides of Vc=2 explicitly."""
    if not 0 <= margin < L - SYS:
        return dict(feasible=False, reason="No positive structural mass", margin_kg=margin)
    core = I["cores"][family]
    fs = np.linspace(1e-7, 1 - 1e-7, grid_n)
    ev = evaluate(fs, margin, core, young)
    y = ev["least"]
    candidate_fs = [float(fs[0]), float(fs[-1]), float(fs[np.argmax(y)])]
    maxima = np.where((y[1:-1] >= y[:-2]) & (y[1:-1] >= y[2:]))[0] + 1
    for j in maxima:
        result = minimize_scalar(
            lambda f: -float(evaluate(f, margin, core, young)["least"]),
            bounds=(fs[j-1], fs[j+1]), method="bounded",
            options={"xatol": 1e-14},
        )
        candidate_fs.append(float(result.x))
    v = ev["Vc"] - 2
    for j in np.where(v[:-1] * v[1:] < 0)[0]:
        root = brentq(lambda f: float(evaluate(f, margin, core, young)["Vc"]) - 2,
                      fs[j], fs[j+1], xtol=1e-15)
        candidate_fs.extend([root - 1e-11, root, root + 1e-11])
    fraction = max(candidate_fs, key=lambda f: float(evaluate(f, margin, core, young)["least"]))
    e = evaluate(fraction, margin, core, young)
    vals = {name: float(v) for name, v in zip(MODES, e["values"])}
    least = min(vals.values())
    governing = [name for name, value in vals.items() if abs(value - least) <= 1e-7 * max(least, 1e-20)]
    s = structure(margin)
    return dict(
        feasible=True, tag="QUESTIONABLE",
        geometry_tag="PROJECTION: fabrication of these thin curved Be sandwich faces is unqualified",
        family=family, core=core["name"],
        margin_kg=margin, margin_fraction=margin/L, tf_m=float(e["tf"]),
        core_m=float(e["tc"]), core_mass_fraction=fraction,
        Vc=float(e["Vc"]), Kc=float(e["Kc"]), gamma_d=float(e["gamma"]),
        branch="shear_crimping" if float(e["Vc"]) > 2 else "stiff_or_moderate_core",
        near_branch_switch=bool(abs(float(e["Vc"]) - 2) < 1e-6),
        modes=vals, least_SF=least, governing=governing,
        factor_to_1_on_governing_only=1/least,
        masses_kg=dict(faces=(1-fraction)*s, core=fraction*s, structural=s,
                       joint_allowance=J*s, system_allowance=SYS,
                       base_hull=(1+J)*s+SYS),
    )


def systems(scenario):
    if "power_package_kg" in scenario:
        power = scenario["power_package_kg"]
    else:
        power = ((scenario["pumping_W"] + scenario["monitoring_W"]) * scenario["mission_hours"]
                 / (scenario["battery_pack_Wh_kg"] * scenario["usable_fraction"]
                    * scenario["electrical_efficiency"]))
    return dict(vacuum_hardware_kg=scenario["vacuum_hardware_kg"],
                power_package_kg=power, controls_kg=scenario["controls_kg"],
                total_kg=scenario["vacuum_hardware_kg"]+power+scenario["controls_kg"])


def climate(scenario):
    swing = scenario["pressure_swing_fraction"]
    dry = L * (1-swing) * T/(T+scenario["temperature_rise_K"])
    moist = L * ((1-swing) - 0.378 * scenario["water_vapour_Pa"]/P) * T/(T+scenario["temperature_rise_K"])
    return dict(dry_lift_kg=dry, moist_lift_kg=moist,
                dry_loss_kg=L-dry, additional_humidity_loss_kg=dry-moist,
                total_loss_kg=L-moist, low_pressure_Pa=P*(1-swing),
                high_pressure_Pa=P*(1+swing), hot_temperature_K=T+scenario["temperature_rise_K"])


def joints(point, scenario):
    """Two face splices, one core splice, two full-area face/core bond films."""
    length = 2 * A/scenario["panel_width_m"]
    b = scenario["strip_width_m"]
    strips_per_m = 2*b*point["tf_m"]*FACE["rho"]
    adhesive_per_m = 2*b*scenario["seam_adhesive_m"]*scenario["rho_adhesive_kg_m3"]
    splice_per_m = point["core_m"]*scenario["core_splice_width_m"]*scenario["rho_splice_kg_m3"]
    seam = length*(strips_per_m+adhesive_per_m+splice_per_m)
    film = 2*A*scenario["bondfilm_lb_ft2"]*LB_FT2_TO_KG_M2
    return dict(length_m=length, strip_kg_m=strips_per_m,
                adhesive_kg_m=adhesive_per_m, core_splice_kg_m=splice_per_m,
                seam_kg=seam, full_area_bondfilm_kg=film, total_kg=seam+film,
                allowance_kg=point["masses_kg"]["joint_allowance"],
                excess_kg=max(0., seam+film-point["masses_kg"]["joint_allowance"]))


def budget(point, scenario):
    sy, jo, cl = systems(scenario), joints(point, scenario), climate(scenario)
    water = A * scenario["rho_water_kg_m3"] * scenario["water_film_m"]
    # Same air, T_inside >= reference T, internal pressure at/below the cap.
    gas = scenario["pressure_internal_fraction_of_p0"] * L
    lines = dict(
        systems_excess_kg=max(0., sy["total_kg"]-SYS),
        joints_and_bondfilm_excess_kg=jo["excess_kg"],
        retained_water_kg=water, contamination_kg=scenario["contamination_kg"],
        temperature_pressure_loss_kg=cl["dry_loss_kg"],
        humidity_loss_kg=cl["additional_humidity_loss_kg"],
        internal_gas_kg=gas, payload_kg=scenario["payload_kg"],
    )
    return dict(lines=lines, total_margin_kg=sum(lines.values()),
                systems=sy, joints=jo, climate=cl,
                allowance_credit_rule="Only excess is charged; unused 100 kg / 5% allowances are retained, not refunded.")


def solve_common_margin(scenario):
    """Find a sufficient common mass line for BOTH independently optimised cores.

    Seams and the 5% allowance are recalculated on every resized geometry.
    First coarse pass brackets the first observed feasible interval; boolean
    bisection keeps the sufficient side even across the inherited branch step.
    """
    def at(m):
        points = {f: optimum(m, f) for f in I["cores"]}
        budgets = {f: budget(pt, scenario) for f, pt in points.items()}
        need = max(b["total_margin_kg"] for b in budgets.values())
        return m-need, points, budgets
    previous = 0.
    bracket = None
    for m in np.linspace(0., L-SYS-1e-4, 161):
        residual, _, _ = at(float(m))
        if residual >= 0:
            bracket = (previous, float(m))
            break
        previous = float(m)
    if bracket is None:
        return dict(feasible=False, reason="Neither positive-mass common line fits the declared scenario.")
    lo, hi = bracket
    for _ in range(45):
        mid = (lo+hi)/2
        if at(mid)[0] >= 0:
            hi = mid
        else:
            lo = mid
    residual, points, budgets = at(hi)
    for f, pt in points.items():
        pt["worst_pressure_least_SF"] = pt["least_SF"]/(1+scenario["pressure_swing_fraction"])
        pt["budget_slack_kg"] = hi-budgets[f]["total_margin_kg"]
    return dict(feasible=True, tag=scenario["tag"], margin_kg=hi, margin_pct=100*hi/L,
                surplus_over_5pct_kg=hi-.05*L, controlling_residual_kg=residual,
                controlling_family=max(budgets, key=lambda f: budgets[f]["total_margin_kg"]),
                points=points, budgets=budgets)


def panels(point):
    result = {}
    allowance = point["masses_kg"]["joint_allowance"]
    for level, scenario in I["scenarios"].items():
        jo = joints(point, scenario)
        mu = jo["strip_kg_m"] + jo["adhesive_kg_m"] + jo["core_splice_kg_m"]
        remaining = allowance-jo["full_area_bondfilm_kg"]
        result[level] = dict(
            tag="PROJECTION", seam_only_min_square_width_m=2*A*mu/allowance,
            all_joint_min_square_width_m=2*A*mu/remaining if remaining > 0 else None,
            all_joint_feasible=remaining > 0, allowance_kg=allowance,
            bondfilm_kg=jo["full_area_bondfilm_kg"], seam_kg_m=mu,
            reason="No finite panel width can fit if continuous bond film alone exceeds the allowance.",
            widths={str(w): dict(seam_kg=2*A*mu/w, total_joint_kg=2*A*mu/w+jo["full_area_bondfilm_kg"])
                    for w in [0.6, 1.2, 2., 4., 10., 20.]},
        )
    return result


def main():
    ref = I["reference_009c5"]
    ref_core = I["cores"]["aramid"]
    direct = evaluate(ref["core_mass_fraction"], .05*L, ref_core)
    assert abs(float(direct["least"])-ref["least_SF"]) < 1e-12
    baseline = {f: {str(p): optimum(p*L, f) for p in [0., .05, .10, .20, .30]} for f in I["cores"]}
    assert abs(baseline["aramid"]["0.05"]["least_SF"]-ref["least_SF"]) < 1e-5
    # Reproduce 014b's actual 8,000-cell search before continuous refinement.
    grid = np.arange(1, 8000)/8000
    al_grid = evaluate(grid, 0., I["cores"]["aluminium"])
    al_grid_sf = float(al_grid["least"].max())
    assert abs(al_grid_sf-I["reference_014b_metal_sf"]) < 1e-12

    answers = {name: solve_common_margin(sc) for name, sc in I["scenarios"].items()}
    variants = {}
    passive = copy.deepcopy(I["scenarios"]["conservative"])
    passive.update(systems_route="ground_evacuated_sealed", vacuum_hardware_kg=25.,
                   power_package_kg=10., controls_kg=15., pumping_W=0.)
    variants["conservative_environment_passive_service"] = solve_common_margin(passive)
    short = copy.deepcopy(I["scenarios"]["conservative"])
    short["mission_hours"] = 8.
    variants["conservative_environment_8h_active"] = solve_common_margin(short)
    pay = copy.deepcopy(I["scenarios"]["optimistic"])
    pay["payload_kg"] = 100.
    variants["optimistic_plus_100kg_payload"] = solve_common_margin(pay)

    checked = []
    for case, ans in {**answers, **variants}.items():
        assert ans["feasible"]
        for family, pt in ans["points"].items():
            dense = evaluate(np.linspace(1e-7, 1-1e-7, 100001), ans["margin_kg"], I["cores"][family])
            dense_sf = float(dense["least"].max())
            assert pt["least_SF"] >= dense_sf-1e-8
            assert abs(pt["masses_kg"]["base_hull"]+ans["margin_kg"]-L) < 1e-8
            assert pt["budget_slack_kg"] > -1e-7
            assert ans["budgets"][family]["joints"]["total_kg"] >= 0
            checked.append(dict(case=case, family=family, dense_grid_best=dense_sf,
                                refined_best=pt["least_SF"], mass_identity="PASS",
                                budget_sufficiency="PASS", dense_grid_100001="PASS"))
    refpoints = {f: baseline[f]["0.05"] for f in I["cores"]}
    panel_result = {f: panels(pt) for f, pt in refpoints.items()}

    q = .01*P*V/86400
    cap = .01*P
    p_start = 10.
    q_allow = (cap-p_start)*V/86400
    gas_max_T = 320.  # Explicit thermal acceptance condition, not a measured hull temperature.
    q_allow_hot = (cap*T/gas_max_T-p_start)*V/86400
    pump_flow = q/cap*3600
    hot_pump_flow = pump_flow*gas_max_T/T
    assert abs(pump_flow - V/24) < 1e-10
    ideal_power = q*math.log(P/cap)
    # Reversible pump-down integrates the changing chamber pressure.
    ratio = cap/P
    ideal_pumpdown_kwh = P*V*(1-ratio*(1+math.log(1/ratio)))/3.6e6
    corrected_hot_only_loss = L*(1-T/(T+25.1))
    slope = {
        family: dict(loss_per_100kg_0_to_5=100*(rows["0.0"]["least_SF"]-rows["0.05"]["least_SF"])/(.05*L),
                     loss_per_100kg_0_to_30=100*(rows["0.0"]["least_SF"]-rows["0.3"]["least_SF"])/(.30*L))
        for family, rows in baseline.items()
    }
    curve = [{"margin_kg": float(m), **{f: optimum(float(m), f)["least_SF"] for f in I["cores"]}}
             for m in np.linspace(0., .90*L, 181)]
    e_sensitivity = {
        name: {f: optimum(ans["margin_kg"], f, young=290e9) for f in I["cores"]}
        for name, ans in answers.items()
    }
    result = dict(
        schema=1, card="MAINLINE-019", unit="vacuum-mainline019-margin-budget-1019",
        status="ESTIMATE", tag="QUESTIONABLE", certification=False,
        started_at=json.loads((ROOT/"RUN.json").read_text())["started_at"],
        time_measurement_scope=json.loads((ROOT/"RUN.json").read_text())["measurement_scope"],
        area_m2=A, volume_m3=V, biaxial_factor=BX,
        reproduction=dict(aramid009c5_direct=float(direct["least"]), filed_aramid009c5=ref["least_SF"],
                          metal014b_original_grid=al_grid_sf,
                          filed_metal014b=I["reference_014b_metal_sf"],
                          note="Continuous refinement slightly improves grid-filed values; pinned material properties remain unchanged."),
        baseline_margin_sweep=baseline, scenarios=answers, variants=variants,
        scenario_definitions=I["scenarios"], slope_check=dict(this_card=slope, card006=I["reference_006_slopes"]),
        panel_limits_at_common_5pct=panel_result,
        systems_routes=dict(
            lightest_candidate="ground-evacuated sealed service, conditional on measured whole-hull leak/outgassing",
            passive=dict(onboard_estimate_kg=[30,50], pumping_W=0., monitoring_W=5.,
                         held_pressure="<=1% of reference external pressure for 24h if internal gas stays <=320 K and the specified normalized gas-load limit is measured",
                         start_pressure_Pa=p_start, maximum_pressure_Pa=cap,
                         maximum_gas_temperature_K=gas_max_T,
                         maximum_total_gas_throughput_at_T0_Pa_m3_s=q_allow_hot,
                         isothermal_T0_only_limit_Pa_m3_s=q_allow,
                         air_mass_reserve_kg=.01*L,
                         capacity_mbar_L_per_day=q_allow_hot*86400*10,
                         measurement_required="leak + outgassing + desorption through all panels, bonds, valves and core vents"),
            inherited_one_percent_day=dict(Q_Pa_m3_s=q, Q_mbar_L_per_s=10*q,
                                           Q_mbar_L_per_day=10*q*86400,
                                           gas_kg_per_day=.01*L, required_pumping_m3_h_at_cap=pump_flow),
            active_catalog=dict(model="SV 300 B, 50 Hz", pump_kg=223., maximum_motor_W=5500., catalog_speed_m3_h=240.,
                                required_m3_h_at_320K=hot_pump_flow,
                                ideal_compression_W_at_T0=ideal_power,
                                rated_speed_headroom_fraction_at_320K=240/hot_pump_flow-1,
                                rejected_smaller_reference="SV220B 180 m3/h has only 3.13% headroom at T0 and cannot meet the 320 K gas duty at this cap.",
                                actual_installed_power_and_speed="UNMEASURED; the catalog rating is not a performance guarantee"),
            getters=dict(status="UNSIZED", tag="QUESTIONABLE",
                         note="Room-temperature nitrogen getters exist. No capacity/rate data justify a kg estimate for this leak. Getter-only all-air pumping is not established; noble gases require another mechanism. Passive sealing does not require getters."),
            commissioning=dict(reversible_minimum_to_one_percent_kWh=ideal_pumpdown_kwh,
                               inherited_formula_kWh=P*V*math.log(1/ratio)/3.6e6,
                               note="Variable-pressure reversible integral; actual ground energy is larger and unmeasured."),
        ),
        climate_correction=dict(hot_only_delta_T_K=25.1, exact_loss_kg=corrected_hot_only_loss,
                                linearized_loss_kg=L*25.1/T,
                                margin_remaining_on_old_5pct_kg=.05*L-corrected_hot_only_loss),
        material_modulus_sensitivity_290GPa_same_margins=e_sensitivity,
        curve=curve, verification=checked,
        formulas=dict(
            mass_line="S=(L0-100-M)/1.05; tf=(1-f)S/(2*A*rho_f); tc=f*S/(A*rho_c)",
            climate="Lday=L0*[1-dp-0.378*e/p0]*T0/(T0+dT); dry component sets e=0",
            joints="(2A/w)*[2*b*tf*rho_f + 2*b*tadh*rho_adh + tc*wsplice*rho_splice] + 2A*film_areal_mass",
            budget="M >= max(0,systems-100)+max(0,joints-0.05*S)+water+contamination+climate_loss+internal_gas+payload, for each core",
            sigma0="E*(tc+tf)/(R*sqrt(1-nu^2))",
            sigma_crimp="(tc+tf)^2*Gc/(2*tf*tc)",
            branch="Vc=sigma0/sigma_crimp; Vc<=2: Kc=1-Vc/4,gamma=kd; Vc>2: Kc=1/Vc,gamma=1",
            global_buckling="4*gamma*Kc*sigma0*tf/(R*p0)",
            compression="4*sigma_y*tf/(R*p0)",
            crush="core_crush/(p0/2)",
            crimp="4*sigma_crimp*tf/(R*p0)",
            wrinkle="b*0.33*sqrt(E*Ec*tf/tc)/(p0*R/(4tf)); b^3+b=1",
            dimple="[2E/(1-nu^2)*(tf/cell)^2]/[p0*R/(4tf)]",
            pressure_check="Each fixed-geometry SF divided by 1+dp for max external pressure at p_inside=0",
            passive="Q <= V*(pmax-pstart)/duration; internal retained air is charged once as mass",
            battery="mass=(Ppump+Pmonitor)*hours/(Wh_per_kg*usable_fraction*conversion_efficiency)",
        ),
        ended_at=datetime.now().astimezone().isoformat(timespec="seconds"),
    )
    (ROOT/"RESULTS.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    (ROOT/"VALIDATION.json").write_text(json.dumps(dict(
        status="PASS", checks=checked, reproduction=result["reproduction"],
        numerical_scope="Arithmetic and mass closure, not structural, environmental or manufacturing qualification.",
    ), indent=2)+"\n")
    print(json.dumps({name: dict(
        margin_kg=ans["margin_kg"], margin_pct=ans["margin_pct"],
        points={f: dict(SF=pt["least_SF"], branch=pt["branch"], Vc=pt["Vc"],
                       tf_mm=1000*pt["tf_m"], core_mm=1000*pt["core_m"])
                for f,pt in ans["points"].items()},
        budgets={f: b["lines"] for f,b in ans["budgets"].items()},
    ) for name,ans in answers.items()},indent=2))


if __name__ == "__main__":
    main()
