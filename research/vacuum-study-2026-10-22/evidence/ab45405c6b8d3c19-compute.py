#!/usr/bin/env python3
"""MAINLINE-027: analytic budget closure, independent P2 mode calculation.

Only INPUTS.json is read. No predecessor executable is imported.
Run prepare_inputs.py before this file.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parent
I = json.loads((ROOT / "INPUTS.json").read_text())
C = I["case"]
P, L0, T0 = C["p0_Pa"], C["lift0_kg"], C["T0_K"]
RHO_F, NU = I["face"]["rho"], C["nu"]
A0, V0 = 400*math.pi, 4000*math.pi/3
BX = brentq(lambda x: x*x*x+x-1, 0., 1., xtol=1e-15)
MODES = ("global_buckling", "face_compression", "core_crush",
         "core_shear_crimping", "face_wrinkling", "intracell_dimpling",
         "joint_net_section")


def environment(radius, label, pump_scaled=False, system_floor=100., coating=0.):
    sc = I["scenarios"][label]
    x = radius/10.
    area, volume, lift = A0*x*x, V0*x**3, L0*x**3
    dry = lift*(1-sc["pressure_swing_fraction"])*T0/(T0+sc["temperature_rise_K"])
    moist = lift*((1-sc["pressure_swing_fraction"])-.378*sc["water_vapour_Pa"]/P)*T0/(T0+sc["temperature_rise_K"])
    flow = volume/24.*320./T0
    n = max(1, math.ceil(flow/240.)) if pump_scaled else 1
    if label == "optimistic":
        hardware, power, controls, watts = 15., 10., 5., 5.
        n = 0
    else:
        hardware, controls, watts = 223.*n, 20., 5500.*n+5.
        power = watts*24./(150.*.8*.9)
    total_system = hardware+power+controls
    lines = dict(
        systems_excess_kg=max(0., total_system-system_floor),
        retained_water_kg=area*1000.*sc["water_film_m"],
        contamination_kg=area*sc["contamination_kg_m2"],
        coating_kg=area*(sc["extra_coating_kg_m2"]+coating),
        temperature_pressure_loss_kg=lift-dry,
        humidity_loss_kg=dry-moist,
        internal_gas_kg=.01*lift,
    )
    return dict(radius_m=radius, area_m2=area, volume_m3=volume, lift_kg=lift,
                high_pressure_Pa=P*(1+sc["pressure_swing_fraction"]),
                moist_lift_kg=moist, lines=lines, other_reserve_kg=sum(lines.values()),
                systems=dict(modules=n, hardware_kg=hardware, battery_or_power_kg=power,
                             controls_kg=controls, total_kg=total_system, power_W=watts,
                             system_floor_kg=system_floor,
                             hot_required_speed_m3_h=flow, module_rated_speed_m3_h=240.,
                             rated_speed_sufficient=(label=="optimistic" or 240*n>=flow),
                             fixed_systems_qualification="Passive is conditional on leak/thermal acceptance; active installed speed is unverified."),
                passive_hot_normalized_gas_load_limit_Pa_m3_s=
                    volume*(.01*P*T0/320.-10.)/86400.,
                gas_load_at_one_percent_volume_per_day_Pa_m3_s=.01*P*volume/86400.)


def joint_coefficients(f, core, sc, mass_model, area):
    """Actual joining = u(f)*structural_mass + v. Both skins included."""
    if mass_model == "fixed_areal":
        return np.zeros_like(f), area*sc["total_joining_kg_m2_frozen_020"]
    lam = 1/sc["panel_a_m"]+1/sc["panel_b_m"]
    u = lam*(sc["splice_width_m"]*(1-f) +
             1100.*sc["core_gap_m"]/core["rho"]*f)
    v = area*(2*sc["film_kg_m2_per_interface"] +
              lam*(2*sc["film_kg_m2_per_interface"]*sc["splice_width_m"] +
                   1100.*sc["sealant_area_m2"]))
    return u, v


def evaluate(f, radius, label, family, mechanical, mass_model,
             payload=0., coating=0., joint_efficiency=None):
    f = np.asarray(f)
    sc, core, mech = I["scenarios"][label], I["cores"][family], I["mechanical_sets"][mechanical]
    env = environment(radius, label, mass_model=="coupled_pump_scaled", coating=coating)
    area, lift, pressure = env["area_m2"], env["lift_kg"], env["high_pressure_Pa"]
    u, v = joint_coefficients(f, core, sc, mass_model, area)
    rem = lift-100-env["other_reserve_kg"]-payload
    s_floor = rem/1.05
    # If the actual joint exceeds the retained allowance, its exact formula replaces it.
    s = np.where(u*s_floor+v <= .05*s_floor, s_floor, (rem-v)/(1+u))
    valid = s > 0
    s_safe = np.where(valid, s, 1e-10)
    tf = (1-f)*s_safe/(2*area*RHO_F)
    tc = f*s_safe/(area*core["rho"])
    young, sigma = mech["E_Pa"], mech["sigma_Pa"]
    h = tf+tc
    s0 = young*h/(radius*math.sqrt(1-NU*NU))
    scr = h*h*core["Gc_Pa"]/(2*tf*tc)
    vc = s0/scr
    kc = np.where(vc >= 2, 1/vc, 1-vc/4)
    if mech["gamma"] == "018_curve":
        gamma = .2+.4*np.minimum(vc, 2)
    elif mech["gamma"] == "constant_0.2":
        gamma = np.full_like(f, .2)
    else:
        gamma = np.where(vc >= 2, 1., .2)
    eta = sc["joint_efficiency"] if joint_efficiency is None else joint_efficiency
    stress = pressure*radius/(4*tf)
    values = np.stack([
        gamma*kc*s0/stress,
        sigma/stress,
        np.ones_like(f)*core["crush_Pa"]/(pressure/2),
        scr/stress,
        BX*mech["wrinkle_coefficient"]*np.sqrt(young*core["Ec_Pa"]*tf/tc)/stress,
        # 021 correction: half the old uniaxial allowable for equal biaxial demand.
        young/(1-NU*NU)*(tf/core["s_cell_m"])**2/stress,
        eta*sigma/stress,
    ])
    least = np.where(valid, values.min(axis=0), -1.)
    return dict(least=least, values=values, tf=tf, tc=tc, Vc=vc, Kc=kc,
                gamma=gamma, structural=s, joining=u*s+v, env=env, valid=valid)


def optimum(radius, label, family, mechanical, mass_model, payload=0.,
            coating=0., grid_n=4001, joint_efficiency=None):
    args = (radius, label, family, mechanical, mass_model, payload, coating, joint_efficiency)
    def ev(f):
        return evaluate(f, *args)
    grid = np.linspace(1e-8, 1-1e-8, grid_n)
    e = ev(grid)
    y = e["least"]
    if np.max(y) < 0:
        return dict(feasible=False, radius_m=radius, scenario=label, family=family,
                    mechanical=mechanical, mass_model=mass_model, payload_kg=payload,
                    reason="No positive structural mass after prescribed budget.",
                    environment=e["env"])
    candidates = [float(grid[0]), float(grid[-1]), float(grid[np.argmax(y)])]
    peaks = np.where((y[1:-1]>=y[:-2]) & (y[1:-1]>=y[2:]) & (y[1:-1]>0))[0]+1
    for j in peaks:
        opt = minimize_scalar(lambda f: -float(ev(f)["least"]),
                              bounds=(grid[j-1], grid[j+1]), method="bounded",
                              options={"xatol":1e-14})
        candidates.append(float(opt.x))
    z = e["Vc"]-2
    for j in np.where(z[:-1]*z[1:]<0)[0]:
        root = brentq(lambda f: float(ev(f)["Vc"])-2, grid[j], grid[j+1], xtol=1e-15)
        candidates += [root-1e-11, root, root+1e-11]
    f = max(candidates, key=lambda x: float(ev(x)["least"]))
    q = ev(f)
    vals = dict(zip(MODES, map(float, q["values"])))
    sf, s = min(vals.values()), float(q["structural"])
    env = q["env"]
    jo = float(q["joining"])
    lines = dict(env["lines"])
    lines["joining_excess_kg"] = max(0., jo-.05*s)
    reserve = sum(lines.values())
    tf, tc = float(q["tf"]), float(q["tc"])
    sc = I["scenarios"][label]
    seamlength = env["area_m2"]*(1/sc["panel_a_m"]+1/sc["panel_b_m"])
    return dict(
        feasible=True, status="ESTIMATE", tag=I["mechanical_sets"][mechanical]["tag"],
        geometry_tag="PROJECTION", radius_m=radius, scenario=label, family=family,
        mechanical=mechanical, mass_model=mass_model, payload_kg=payload,
        core=I["cores"][family]["name"], core_mass_fraction=f,
        tf_m=tf, tc_m=tc, Vc=float(q["Vc"]), Kc=float(q["Kc"]), gamma=float(q["gamma"]),
        branch="crimp" if q["Vc"]>=2 else "stiff_or_moderate",
        near_branch_switch=bool(abs(q["Vc"]-2)<1e-6),
        pressure_basis="maximum external pressure, no internal-pressure load credit",
        least_SF=sf, modes=vals,
        governs=[k for k,vv in vals.items() if abs(vv-sf)<max(1e-8,1e-6*sf)],
        reserve_kg=reserve, reserve_fraction=reserve/env["lift_kg"],
        budget_lines_kg=lines, environment=env,
        masses_kg=dict(faces=(1-f)*s, core=f*s, structural=s,
                       joint_allowance=.05*s, actual_joining=jo, charged_joining=max(.05*s, jo),
                       systems_floor=100., unused_system_allowance=max(0.,100-env["systems"]["total_kg"]),
                       design_envelope_total=1.05*s+100+reserve+payload),
        panel=dict(a_m=sc["panel_a_m"], b_m=sc["panel_b_m"],
                   count_per_skin_lower_bound=math.ceil(env["area_m2"]/(sc["panel_a_m"]*sc["panel_b_m"])),
                   coincident_seam_m=seamlength,
                   bond_films_kg=2*env["area_m2"]*sc["film_kg_m2_per_interface"],
                   corner_sag_m=radius-math.sqrt(radius**2-(sc["panel_a_m"]**2+sc["panel_b_m"]**2)/4)),
    )


def payload_at_one(radius, label, family, mechanical, mass_model):
    zero = optimum(radius, label, family, mechanical, mass_model)
    if not zero["feasible"] or zero["least_SF"]<1:
        return dict(reaches_SF1=False, maximum_payload_kg=None,
                    reason="Zero-payload point below SF1 or no positive structural mass.")
    lo, hi = 0., zero["environment"]["lift_kg"]
    for _ in range(42):
        mid = (lo+hi)/2
        pt = optimum(radius, label, family, mechanical, mass_model, payload=mid)
        if pt["feasible"] and pt["least_SF"]>=1:
            lo = mid
        else:
            hi = mid
    p = optimum(radius, label, family, mechanical, mass_model, payload=lo)
    return dict(reaches_SF1=True, maximum_payload_kg=lo, point=p,
                tag="PROJECTION", condition="Every modelled mode including joint net section at high pressure; unmodelled hardware excluded.")


def main():
    results = []
    checks = []
    for mass_model in I["mass_models"]:
        for scenario in I["scenarios"]:
            for radius in I["radii_m"]:
                for family in I["cores"]:
                    for mechanical in ("chain_design", "full_021"):
                        point = optimum(radius, scenario, family, mechanical, mass_model)
                        point["payload_at_SF1"] = payload_at_one(radius, scenario, family, mechanical, mass_model)
                        results.append(point)
                        if point["feasible"]:
                            dense = evaluate(np.linspace(1e-8, 1-1e-8, 100001),
                                             radius, scenario, family, mechanical, mass_model)
                            best = float(np.max(dense["least"]))
                            assert point["least_SF"] >= best-1e-8, point
                            err = point["masses_kg"]["design_envelope_total"]-point["environment"]["lift_kg"]
                            assert abs(err)<1e-7
                            checks.append(dict(radius_m=radius, scenario=scenario, family=family,
                                               mechanical=mechanical, mass_model=mass_model,
                                               dense_best=best, refined_best=point["least_SF"],
                                               mass_error_kg=err))
    sensitivities = []
    for radius in I["radii_m"]:
        for family in I["cores"]:
            sensitivities.append(optimum(radius, "optimistic", family, "full_021_flat_gamma", "coupled"))
            pt = optimum(radius, "optimistic", family, "full_021", "coupled", coating=.1)
            pt["sensitivity"] = "0.1 kg/m2 extra coating"
            sensitivities.append(pt)
            pt = optimum(radius, "optimistic", family, "full_021", "coupled", joint_efficiency=1.)
            pt["sensitivity"] = "No joint net-section derating; mass unchanged"
            sensitivities.append(pt)
    floors = {}
    for scenario in I["scenarios"]:
        en = environment(10., scenario)
        floor = sum(en["lines"][k] for k in ("temperature_pressure_loss_kg","humidity_loss_kg","internal_gas_kg"))/L0
        floors[scenario] = dict(volume_proportional_reserve_floor=floor,
                                 radius_below_5pct_for_either_P2=None,
                                 proof="These nonnegative R^3 rows alone exceed 5% of lift; all other charged reserve rows are nonnegative.")
    # Pure similar shell, fixed material/core cell: crimp has no intrinsic R loss.
    scale_checks = []
    for family in I["cores"]:
        p = next(x for x in results if x["feasible"] and x["radius_m"]==10 and
                 x["scenario"]=="optimistic" and x["family"]==family and
                 x["mechanical"]=="chain_design" and x["mass_model"]=="coupled")
        core = I["cores"][family]
        for radius in I["radii_m"]:
            scale=radius/10.
            tf,tc=p["tf_m"]*scale,p["tc_m"]*scale
            crimp_pressure=2*(tf+tc)**2*core["Gc_Pa"]/(radius*tc)
            ref=2*(p["tf_m"]+p["tc_m"])**2*core["Gc_Pa"]/(10*p["tc_m"])
            assert abs(crimp_pressure/ref-1)<1e-12
            scale_checks.append(dict(family=family,radius_m=radius,crimp_pressure_ratio=crimp_pressure/ref,
                                      dimpling_pressure_ratio=scale**2))
    out = dict(schema=1, card="MAINLINE-027", status="ESTIMATE", tag="QUESTIONABLE",
               certification=False, P2=results, sensitivities=sensitivities,
               floor_proof=floors, dense_grid_checks=checks, similarity_checks=scale_checks)
    (ROOT/"RESULTS.json").write_text(json.dumps(out, indent=2)+"\n")
    print("P2 rows", len(results), "checks", len(checks), "floors", floors)
    for pt in results:
        if pt["mass_model"]=="coupled" and pt["mechanical"]=="full_021":
            print(pt["scenario"],pt["radius_m"],pt["family"],
                  f"SF {pt.get('least_SF',0):.6f}",
                  f"reserve {pt.get('reserve_fraction',0)*100:.4f}%",
                  "payload",pt["payload_at_SF1"].get("maximum_payload_kg"))


if __name__ == "__main__":
    main()
