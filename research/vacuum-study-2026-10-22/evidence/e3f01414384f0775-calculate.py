"""MAINLINE-034: fresh species/inventory calculation; no upstream code imports."""
import json
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

BASE = Path(__file__).resolve().parent
I = json.loads((BASE / "INPUTS.json").read_text())
E, C, SP = I["environment"], I["constants"], I["species"]
RU, DAY = C["R_universal_J_mol_K"], C["seconds_per_day"]
T, PH = E["T_K"], E["p_external_Pa"]
A = 4 * math.pi * E["R_m"] ** 2
V0 = 4 * math.pi * E["R_m"] ** 3 / 3
RHO = E["lift_reference_kg"] / V0
LIMIT = E["gas_mass_fraction_limit"] * E["lift_reference_kg"]
PCEIL = E["pressure_ceiling_fraction"] * PH
M = {k: v["M_kg_mol"] for k, v in SP.items()}
dry_total = sum(v["dry_x"] for v in SP.values())
DRY_X = {k: v["dry_x"] / dry_total for k, v in SP.items()}
WET_X = {k: x * (1 - E["water_partial_external_Pa"] / PH)
         for k, x in DRY_X.items()}
WET_X["H2O"] = E["water_partial_external_Pa"] / PH
PEXT = {k: x * PH for k, x in WET_X.items()}
NAMES = list(SP)


def geometry():
    p = I["P2"]
    tf, tc, w, r = (p[k] for k in
                    ["face_thickness_m", "core_thickness_m",
                     "panel_width_m", "scarf_run_ratio"])
    seam = 2 * A / (w - r * tf)
    scarf_path = tf * math.sqrt(1 + r * r)
    scarf_gap = p["scarf_film_kg_m2"] / p["scarf_density_assumed_kg_m3"]
    scarf_mass = 2 * seam * scarf_path * p["scarf_film_kg_m2"]
    bond_mass = 2 * A * p["bond_film_kg_m2_per_face"]
    fill_mass = seam * p["core_splice_gap_m"] * tc * p["core_splice_density_kg_m3"]
    seal_mass = seam * p["seal_mass_kg_per_unique_m"]
    solid_volume = (p["face_mass_kg"] / p["face_density_kg_m3"]
                    + p["core_mass_kg"] / p["core_metal_density_kg_m3"]
                    + (bond_mass + scarf_mass) / p["scarf_density_assumed_kg_m3"]
                    + fill_mass / p["core_splice_density_kg_m3"])
    core_void = (A * tc - p["core_mass_kg"] / p["core_metal_density_kg_m3"]
                 - bond_mass / p["scarf_density_assumed_kg_m3"]
                 - fill_mass / p["core_splice_density_kg_m3"])
    g = {
        "P2": {
            "gas_volume_m3": V0 - solid_volume,
            "area_per_face_m2": A, "faces_total_area_m2": 2 * A,
            "face_thickness_m": tf, "core_thickness_m": tc,
            "seam_m": seam, "nodes": A / (w - r * tf) ** 2 + 2,
            "bond_film_mass_kg": bond_mass,
            "scarf_both_faces_mass_kg": scarf_mass,
            "core_splice_mass_kg": fill_mass, "seal_mass_kg": seal_mass,
            "scarf_path_m": scarf_path, "scarf_gap_m": scarf_gap,
            "scarf_diffusion_area_over_length_m": seam * scarf_gap / scarf_path,
            "core_wall_area_estimate_m2": 4 * A * tc / p["core_cell_m"],
            "core_void_m3": core_void,
            "unvented_core_air_kg": core_void * PH / (RU * T)
                * sum(WET_X[k] * M[k] for k in NAMES),
            "known_solids_volume_m3": solid_volume,
            "note": "Vented honeycomb shares hull vacuum. Surface and count models are approximate.",
        }
    }
    for out, key in [("P3_Kapton", "kapton"), ("P3_Zylon_barrier", "zylon_barrier")]:
        p = I["P3"][key]
        length = p["members"] * p["length_m"]
        ri = p["r_o_m"] - p["t_w_m"]
        bore = math.pi * ri ** 2 * length
        tube_volume = p["A_m2"] * length
        j = I["P3"]["joint_adhesive"]
        bond_area = 2 * p["members"] * p["N_N"] / j["tau_Pa_from_023"]
        adhesive_mass = bond_area * j["gap_m_assumed"] * j["density_kg_m3_assumed"]
        g[out] = {
            "gas_volume_m3": V0 - p["sag_kg"] / RHO,
            "sag_loss_m3": p["sag_kg"] / RHO,
            "sag_loss_kg": p["sag_kg"],
            "area_m2": A, "film_thickness_m": p["t_film_m"],
            "structural_film_mass_kg": p["m_film"],
            "tube_mass_kg": p["m_tube"],
            "tube_material": "SiC",
            "joint_material": "titanium sleeve" if out == "P3_Kapton" else "CFRP end wrap",
            "joint_mass_kg": p["m_joint"],
            "tube_density_from_geometry_kg_m3": p["m_tube"] / tube_volume,
            "tube_inner_and_outer_surface_m2": 2 * math.pi * (p["r_o_m"] + ri) * length,
            "tube_solid_volume_m3": tube_volume,
            "hollow_bore_volume_m3": bore,
            "unvented_tube_air_kg": bore * PH / (RU * T)
                * sum(WET_X[k] * M[k] for k in NAMES),
            "joint_bond_area_m2": bond_area,
            "additional_joint_adhesive_kg": adhesive_mass,
            "seam_m": length,
            "nodes": p["nodes"],
            "filed_structural_SF": p["SF_least"],
            "note": "022c cap volume accepted as input; true pillow area and internal occupied volume unverified.",
        }
    z = I["zylon"]
    g["P3_Zylon_barrier"]["barrier_mass_bill_kg"] = {
        "PET": A * z["barrier_PET_thickness_m"] * z["barrier_PET_density_kg_m3"],
        "Al_assumed_50nm": A * z["barrier_Al_thickness_assumed_m"]
            * z["barrier_Al_density_kg_m3"],
        "attachment_lamination_assumed": A * z["attachment_assumed_kg_m2"],
        "seam_installation_assumed": z["seam_installation_allowance_kg"],
    }
    return g


G = geometry()


def sources(lead, config):
    """Rates at zero internal partial pressure, plus finite release inventories."""
    area = A * config.get("area_multiplier", 1.0)
    q0 = {k: 0.0 for k in NAMES}  # kg/day, not pV throughput
    inventories = {}
    if lead == "P2":
        p = I["P2"]
        geom = G[lead]["scarf_diffusion_area_over_length_m"]
        coeff = config.get("scarf_Barrer", p["scarf_gas_Barrer_assumed"])
        for k in NAMES:
            q0[k] = coeff * C["Barrer_mol_m_m2_s_Pa"] * geom * PEXT[k] * DAY * M[k]
        inventories["AF163_full_bondlines"] = (
            G[lead]["bond_film_mass_kg"] * config.get("AF_TML", p["AF163_TML_high"]))
        inventories["core_foil_coating_and_nodes_assumed"] = (
            p["core_mass_kg"] * p["core_release_fraction_assumed"])
        inventories["scarf_splice_and_seal_polymers_assumed"] = (
            G[lead]["scarf_both_faces_mass_kg"] + G[lead]["core_splice_mass_kg"]
            + G[lead]["seal_mass_kg"]) * p["other_polymers_release_fraction_assumed"]
    elif lead == "P3_Kapton":
        p = I["kapton"]
        scale = p["reference_thickness_m"] / G[lead]["film_thickness_m"]
        for k in NAMES:
            if k != "H2O":
                cc = p["gas_ml_m2_day_MPa"][k] * PEXT[k] / 1e6 * area * scale
                q0[k] = cc / C["Vm_STP_cc_mol"] * M[k]
        q0["H2O"] = p["water_g_m2_day"] / 1000 * area * scale
        inventories["Kapton_TML_proxy"] = G[lead]["structural_film_mass_kg"] * (
            p["moisture_fraction_50RH"] if config.get("wet_film")
            else p["outgas_TML_proxy"])
        inventories["unmeasured_seals_and_titanium_surfaces_assumed"] = 0.1
        inventories["SiC_surface_inventory_assumed"] = (
            G[lead]["tube_inner_and_outer_surface_m2"]
            * I["P3"]["SiC_surface_release_kg_m2_assumed"])
        inventories["EA9394_joint_bonds_TML_proxy"] = (
            G[lead]["additional_joint_adhesive_kg"]
            * I["P3"]["joint_adhesive"]["TML_proxy"])
    else:
        p, z = I["mylar"], I["zylon"]
        for k in NAMES:
            if k != "H2O":
                ratio = p["permeance_ratios_to_O2_assumed"][k]
                if k == "N2":
                    ratio *= config.get("barrier_N2_multiplier", 1.0)
                cc = p["O2_cc_m2_day_pure_O2"] * ratio * PEXT[k] / C["atm_Pa"] * area
                q0[k] = cc / C["Vm_STP_cc_mol"] * M[k]
        q0["H2O"] = p["water_g_m2_day_upper"] / 1000 * area
        bill = G[lead]["barrier_mass_bill_kg"]
        inventories["Zylon_equilibrium_moisture_proxy"] = (
            G[lead]["structural_film_mass_kg"] * z["moisture_fraction"])
        inventories["unmatched_CFRP_end_wrap_TML_proxy"] = (
            G[lead]["joint_mass_kg"] * config.get("CFRP_TML", z["cfrp_TML_proxy"]))
        inventories["SiC_surface_inventory_assumed"] = (
            G[lead]["tube_inner_and_outer_surface_m2"]
            * I["P3"]["SiC_surface_release_kg_m2_assumed"])
        inventories["EA9394_joint_bonds_TML_proxy"] = (
            G[lead]["additional_joint_adhesive_kg"]
            * I["P3"]["joint_adhesive"]["TML_proxy"])
        inventories["metallized_PET_TML_proxy"] = bill["PET"] * z["PET_TML_proxy"]
        inventories["attachment_and_seals_assumed"] = (
            bill["attachment_lamination_assumed"] + bill["seam_installation_assumed"]
        ) * z["attachment_TML_assumed"]
    q0["H2O"] *= config.get("water_multiplier", 1.0)
    lam = config.get("leak_rate", 1e-3)
    # 1 mbar L/s = 0.1 Pa m3/s. Quoted at T, not STP.
    q_leak_PV = 0.1 * (lam * (G[lead]["seam_m"] + G[lead]["nodes"])
                       + I["leak_model"]["ports_mbar_l_s"])
    leak = {k: q_leak_PV * DAY / (RU * T) * WET_X[k] * M[k] for k in NAMES}
    retained = config.get("retained_fraction", 0.1)
    Btotal = sum(inventories.values()) * retained
    B = {k: 0.0 for k in NAMES}
    hf = config.get("outgas_hydrogen_mass_fraction", 0.0)
    B["H2O"], B["H2"] = Btotal * (1 - hf), Btotal * hf
    return {
        "permeation_zero_internal_kg_day": q0,
        "leak_kg_day": leak, "leak_Pa_m3_s": q_leak_PV,
        "inventory_before_conditioning_kg": inventories,
        "release_inventory_by_species_kg": B,
        "retained_fraction": retained,
        "release_tau_days": config.get("tau_days", 1.0),
        "tag": "PROJECTION",
    }


def phi(k, t):
    return t if abs(k) < 1e-14 else -math.expm1(-k * t) / k


def state(lead, src, t, constant_upper=False):
    volume, tau = G[lead]["gas_volume_m3"], src["release_tau_days"]
    n0 = {k: E["initial_pressure_Pa"] * volume / (RU * T) * DRY_X[k] for k in NAMES}
    ns, released = {}, {}
    for key in NAMES:
        q0 = src["permeation_zero_internal_kg_day"][key] / M[key]
        leak = src["leak_kg_day"][key] / M[key]
        B = src["release_inventory_by_species_kg"][key] / M[key]
        k = 0.0 if constant_upper else q0 * RU * T / (volume * PEXT[key])
        ek, et = math.exp(-k * t), math.exp(-t / tau)
        if abs(k - 1 / tau) < 1e-10:
            og = B / tau * t * ek
        else:
            og = B / tau * (et - ek) / (k - 1 / tau)
        ns[key] = n0[key] * ek + (q0 + leak) * phi(k, t) + og
        released[key] = B * M[key] * (-math.expm1(-t / tau))
    pressure = sum(ns.values()) * RU * T / volume
    initial_mass = sum(n0[k] * M[k] for k in NAMES)
    gas_mass = sum(ns[k] * M[k] for k in NAMES)
    return {
        "days": t,
        "pressure_Pa": pressure,
        "pressure_after_instant_heat_to_320K_Pa": pressure * E["T_hot_K"] / T,
        "gas_mass_kg": gas_mass,
        "external_net_mass_added_kg": gas_mass - initial_mass - sum(released.values()),
        "existing_material_released_kg": sum(released.values()),
        "species_gas_mass_kg": {k: ns[k] * M[k] for k in NAMES},
        "species_pressure_Pa": {k: ns[k] * RU * T / volume for k in NAMES},
    }


def first_crossing(fun, limit):
    prev_t, prev = 0.0, fun(0.0) - limit
    if prev >= 0:
        return 0.0
    for t in np.geomspace(1e-6, 1e5, 500):
        value = fun(float(t)) - limit
        if value >= 0 and prev < 0:
            return float(brentq(lambda x: fun(x) - limit, prev_t, float(t),
                               xtol=1e-11, rtol=1e-13))
        prev_t, prev = float(t), value
    return None


def times(lead, src, upper=False):
    f = lambda t: state(lead, src, t, upper)
    return {
        "gas_inventory_limit_days": first_crossing(lambda t: f(t)["gas_mass_kg"], LIMIT),
        "external_added_mass_limit_days": first_crossing(
            lambda t: f(t)["external_net_mass_added_kg"], LIMIT),
        "pressure_limit_days_at_284p9K": first_crossing(
            lambda t: f(t)["pressure_Pa"], PCEIL),
        "pressure_limit_days_instant_320K_envelope": first_crossing(
            lambda t: f(t)["pressure_after_instant_heat_to_320K_Pa"], PCEIL),
    }


def max_leak_24h(lead, config):
    src = sources(lead, {**config, "leak_rate": 0.0})
    zero = dict(src)
    zero["leak_kg_day"] = {k: 0.0 for k in NAMES}
    zero["leak_Pa_m3_s"] = 0.0
    def at_q(q):
        modified = dict(zero)
        modified["leak_kg_day"] = {k: q * DAY / (RU * T) * WET_X[k] * M[k]
                                  for k in NAMES}
        return state(lead, modified, 1.0, True)
    def excess(q):
        s = at_q(q)
        return max(s["pressure_after_instant_heat_to_320K_Pa"] / PCEIL,
                   s["gas_mass_kg"] / LIMIT,
                   s["external_net_mass_added_kg"] / LIMIT) - 1
    if excess(0.0) >= 0:
        return {"total_leak_Pa_m3_s": 0.0, "reason": "inventory alone exceeds chosen limit"}
    qmax = brentq(excess, 0, 1e4, xtol=1e-11)
    return {"total_leak_Pa_m3_s": qmax,
            "total_leak_mbar_l_s": qmax * 10,
            "air_sccm_at_STP": qmax / (RU * T) * C["Vm_STP_cc_mol"] * 60,
            "equal_seam_and_node_rate_mbar_l_s": max(
                0, (qmax * 10 - I["leak_model"]["ports_mbar_l_s"])
                / (G[lead]["seam_m"] + G[lead]["nodes"])),
            "basis": "24 h, constant source-rate upper envelope, instantaneous heat to 320 K; no backpressure credit."}


CONFIGS = {
    "conditioned_reference": {},
    "unconditioned": {"retained_fraction": 1.0},
    "low_leak": {"leak_rate": 1e-5},
    "high_leak": {"leak_rate": 0.1},
    "unconditioned_high_leak": {"retained_fraction": 1.0, "leak_rate": 0.1},
    "water_rate_one_tenth": {"water_multiplier": 0.1},
    "slow_unconditioned_release": {"retained_fraction": 1.0, "tau_days": 10.0},
    "area_and_barrier_sensitivity": {"area_multiplier": 1.1, "barrier_N2_multiplier": 10.0},
    "outgas_5percent_H2": {"outgas_hydrogen_mass_fraction": 0.05},
}


def equipment(lead, src):
    sys = I["systems"]
    initial_rates = {k: src["permeation_zero_internal_kg_day"][k]
                     + src["leak_kg_day"][k] for k in NAMES}
    qpv = sum(initial_rates[k] / M[k] for k in NAMES) * RU * T / DAY
    q_hot = qpv * E["T_hot_K"] / T
    out = {
        "steady_source_upper_kg_day": sum(initial_rates.values()),
        "steady_source_upper_Pa_m3_s_at_T": qpv,
        "steady_source_upper_Pa_m3_s_at_320K": q_hot,
        "required_effective_speed_m3_h_at_T": qpv / PCEIL * 3600,
        "required_effective_speed_m3_h_at_320K": q_hot / PCEIL * 3600,
        "reversible_isothermal_power_floor_W_at_T": qpv * math.log(PH / PCEIL),
        "note": "Steady zero-internal-permeation envelope excludes transient release. Gas storage buffers release; pump operating curves and conductance remain qualification items.",
    }
    for key in ["KNF_N920_APDCB", "Edwards_E2M28"]:
        p = sys[key]
        speed = p.get("speed_at_10mbar_m3_h_chart_read", p.get("nominal_speed_50Hz_m3_h"))
        effective = speed * sys["installed_speed_fraction_assumed"]
        input_W = p.get("input_W", p.get("input_W_assumed"))
        battery = (input_W + sys["monitoring_W"]) * 24 / (
            sys["battery_Wh_kg"] * sys["battery_usable_fraction"]
            * sys["power_conversion_efficiency"])
        # Replace the passive 10 kg power package with the sized battery.
        total = (sys["sealed_vacuum_hardware_kg"] + sys["sealed_controls_kg"]
                 + sys["continuous_pump_plumbing_filters_oil_allowance_kg"]
                 + p["pump_kg"] + battery)
        out[key] = {
            "effective_speed_m3_h_assumed": effective, "pump_kg": p["pump_kg"],
            "electrical_W": input_W, "battery_24h_continuous_kg": battery,
            "installed_system_kg_continuous_24h": total,
            "excess_over_100kg": max(0, total - sys["retained_allowance_kg"]),
            "steady_speed_ratio_at_T": effective / out["required_effective_speed_m3_h_at_T"],
            "steady_speed_ratio_at_320K": effective / out["required_effective_speed_m3_h_at_320K"],
        }
    water_one_day = (initial_rates["H2O"]
                     + src["release_inventory_by_species_kg"]["H2O"]
                     * (-math.expm1(-1 / src["release_tau_days"])))
    getter = I["getters"]
    out["water_sorbent_only_24h"] = {
        "water_captured_kg_upper": water_one_day,
        "catalog_dry_bed_kg": water_one_day / getter["water_capacity_kg_kg_catalog"],
        "assumed_vacuum_usable_dry_bed_kg": water_one_day / getter["water_capacity_kg_kg_assumed"],
        "dry_system_kg_assumed": 30 + getter["cartridge_kg"]
            + water_one_day / getter["water_capacity_kg_kg_assumed"],
        "loaded_system_kg_assumed": 30 + getter["cartridge_kg"]
            + water_one_day / getter["water_capacity_kg_kg_assumed"] + water_one_day,
        "note": "Dry gas still accumulates. Getter increases retained external mass and can increase water inflow by keeping water partial pressure low. Existing-material water capture transfers, rather than adds, vehicle mass.",
    }
    return out


def independent_checks(runs):
    checks = []
    def check(name, actual, expected, rtol=2e-10, atol=1e-10):
        ok = math.isclose(actual, expected, rel_tol=rtol, abs_tol=atol)
        checks.append({"name": name, "actual": actual, "expected": expected,
                       "difference": actual - expected, "pass": ok})
        assert ok, f"{name}: actual={actual:.17g}, expected={expected:.17g}, difference={actual-expected:.17g}"
    # Earlier independently checked source conversion, at original 843 um gauge.
    th = 0.0008430307763824935
    o = 3800 * (PH * .20946 / 1e6) * A * 25e-6 / th / 22414 * .031998
    n = 910 * (PH * .78084 / 1e6) * A * 25e-6 / th / 22414 * .028014
    w = 54 / 1000 * A * 25e-6 / th
    check("prior_024_Kapton_conversion", o + n + w,
          I["prior_024_check"]["kapton_843um_mass_rate_kg_day"])
    check("019_internal_air_1pct", LIMIT, 48.89442150186961)
    check("021b_bond_mass", G["P2"]["bond_film_mass_kg"], 368.1263710594744)
    check("leak_unit_mbar_l_s", 100 * .001, .1)
    for lead in ["P3_Kapton", "P3_Zylon_barrier"]:
        check(f"{lead}_tube_density_is_SiC", G[lead]["tube_density_from_geometry_kg_m3"],
              3100.0)
    for lead in G:
        src = runs[lead]["conditioned_reference"]["sources"]
        vol, tau = G[lead]["gas_volume_m3"], src["release_tau_days"]
        n0 = [E["initial_pressure_Pa"] * vol / (RU * T) * DRY_X[k] for k in NAMES]
        q0 = np.array([src["permeation_zero_internal_kg_day"][k] / M[k] for k in NAMES])
        leak = np.array([src["leak_kg_day"][k] / M[k] for k in NAMES])
        B = np.array([src["release_inventory_by_species_kg"][k] / M[k] for k in NAMES])
        pe = np.array([PEXT[k] for k in NAMES])
        def rhs(t, n):
            return q0 * (1 - n * RU * T / (vol * pe)) + leak + B / tau * np.exp(-t / tau)
        integration = solve_ivp(rhs, (0, 30), n0, method="DOP853",
                                rtol=1e-12, atol=1e-13, max_step=.25,
                                dense_output=True)
        assert integration.success
        for day in [1, 7, 30]:
            ni = integration.sol(day)
            ana = state(lead, src, day)
            check(f"{lead}_ODE_vs_closed_form_pressure_day{day}",
                  float(sum(ni) * RU * T / vol), ana["pressure_Pa"], rtol=5e-10, atol=1e-7)
        check(f"{lead}_initial_pressure", state(lead, src, 0)["pressure_Pa"], 10)
        st = state(lead, src, 7)
        initial = state(lead, src, 0)["gas_mass_kg"]
        check(f"{lead}_mass_conservation", st["gas_mass_kg"],
              initial + st["external_net_mass_added_kg"] + st["existing_material_released_kg"])
        # Numerical quadrature of net external flux is independent of inventory subtraction.
        def full_rhs(t, y):
            n = y[:len(NAMES)]
            flow = q0 * (1 - n * RU * T / (vol * pe)) + leak
            return np.r_[flow + B / tau * np.exp(-t / tau),
                         sum(flow[j] * M[k] for j, k in enumerate(NAMES))]
        integrated = solve_ivp(full_rhs, (0, 7), np.r_[n0, 0.], method="DOP853",
                               rtol=1e-12, atol=1e-13, max_step=.25)
        check(f"{lead}_external_flux_integral", float(integrated.y[-1, -1]),
              st["external_net_mass_added_kg"], rtol=1e-9)
        for name, val in runs[lead]["conditioned_reference"]["times_partial_pressure"].items():
            if val is None:
                continue
            st = state(lead, src, val)
            key = {"gas_inventory_limit_days": "gas_mass_kg",
                   "external_added_mass_limit_days": "external_net_mass_added_kg",
                   "pressure_limit_days_at_284p9K": "pressure_Pa",
                   "pressure_limit_days_instant_320K_envelope":
                       "pressure_after_instant_heat_to_320K_Pa"}[name]
            check(f"{lead}_{name}_root", st[key],
                  PCEIL if key.endswith("_Pa") else LIMIT, rtol=1e-10)
    return checks


def main():
    runs = {}
    for lead in G:
        runs[lead] = {}
        configs = dict(CONFIGS)
        if lead == "P3_Kapton":
            configs["wet_unconditioned_film"] = {"retained_fraction": 1., "wet_film": True}
        if lead == "P3_Zylon_barrier":
            configs["CFRP_one_percent_unconditioned"] = {"retained_fraction": 1., "CFRP_TML": .01}
        if lead == "P2":
            configs["AF_low_TML"] = {"AF_TML": .0259}
            configs["scarf_100Barrer"] = {"scarf_Barrer": 100.}
        for name, cfg in configs.items():
            src = sources(lead, cfg)
            runs[lead][name] = {
                "assumptions": cfg, "sources": src,
                "times_partial_pressure": times(lead, src),
                "times_constant_source_upper_envelope": times(lead, src, True),
                "samples": [state(lead, src, t) for t in [0, 1, 7, 14, 30, 90, 365]],
                "samples_constant_upper": [state(lead, src, t, True) for t in [1, 7, 30]],
                "max_total_leak_24h": max_leak_24h(lead, cfg),
            }
    equipment_rows = {lead: equipment(lead, runs[lead]["conditioned_reference"]["sources"])
                      for lead in G}
    get = I["getters"]
    getter_conversion = {}
    for gas, pv in get["NEXTorr_capacity_Torr_l_single_run"].items():
        kg_gas = pv * C["torr_Pa"] * .001 / (RU * get["NEXTorr_temperature_K"]) * M[gas]
        getter_conversion[gas] = {
            "single_run_gas_capacity_kg": kg_gas,
            "kg_getter_per_kg_gas": get["NEXTorr_D100_5_getter_kg"] / kg_gas,
            "note": "Pure-gas UHV capacity screen, not a mixed-gas rough-vacuum selection."}
    sys = I["systems"]
    useful_Wh_kg = (sys["battery_Wh_kg"] * sys["battery_usable_fraction"]
                   * sys["power_conversion_efficiency"])
    monitoring_days = (sys["sealed_power_package_kg"] * useful_Wh_kg
                       / sys["monitoring_W"] / 24)
    barrier = sum(G["P3_Zylon_barrier"]["barrier_mass_bill_kg"].values())
    joint_bond = G["P3_Zylon_barrier"]["additional_joint_adhesive_kg"]
    systems_ledger = {
        "selected_route": "24 h sealed service and periodic ground re-evacuation, conditional on assembly acceptance",
        "passive_identified_system_kg": 30.0,
        "passive_installation_range_kg": [30.0, 50.0],
        "reserved_systems_line_each_lead_kg": 100.0,
        "monitoring_power_W": sys["monitoring_W"],
        "monitoring_days_if_all_10kg_is_usable_battery": monitoring_days,
        "monitoring_note": "Nine days is optimistic for the entire 10 kg package being battery; packaging/control supply losses beyond the stated factors are unmeasured.",
        "sealed_system_mass_vs_duration": [
            {"days": d, "minimum_battery_kg_at_assumed_pack_factors":
             sys["monitoring_W"] * d * 24 / useful_Wh_kg,
             "identified_system_kg_retaining_at_least_10kg_power_package":
             20 + max(10, sys["monitoring_W"] * d * 24 / useful_Wh_kg)}
            for d in [1, 7, 30, 365]],
        "P3_Zylon_added_barrier_attachment_bill_kg": barrier,
        "P3_Zylon_additional_joint_bond_kg": joint_bond,
        "P3_Kapton_additional_joint_bond_kg": G["P3_Kapton"]["additional_joint_adhesive_kg"],
        "P3_Zylon_vacuum_system_plus_barrier_kg": [30 + barrier, 50 + barrier],
        "P3_Zylon_system_plus_barrier_plus_joint_bond_kg": [
            30 + barrier + joint_bond, 50 + barrier + joint_bond],
        "P3_Zylon_remaining_of_100kg_at_low_bill": 100 - 30 - barrier - joint_bond,
        "P3_Zylon_excess_over_100kg_at_high_bill": max(0, 50 + barrier + joint_bond - 100),
        "allocation_note": "The barrier is a separate structural assembly cost. Funding it from the unallocated systems line is an explicit reallocation, not proof that omitted hardware, weather protection and laminate manufacture fit. Keep 100 kg reserved and do not award payload credit.",
        "P2_unvented_core_fraction_of_internal_gas_row": G["P2"]["unvented_core_air_kg"] / LIMIT,
        "P3_Kapton_E2M28_minimum_speed_fraction_hot_source_envelope":
            equipment_rows["P3_Kapton"]["required_effective_speed_m3_h_at_320K"]
            / sys["Edwards_E2M28"]["nominal_speed_50Hz_m3_h"],
    }
    checks = independent_checks(runs)
    result = {
        "schema": 1, "card": "MAINLINE-034", "unit": I["unit"], "tag": "QUESTIONABLE",
        "scenario_tag": "PROJECTION", "certification": False,
        "started_at": I["started_at"],
        "calculated_at": datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds"),
        "reference_area_m2": A, "reference_volume_m3": V0,
        "gas_mass_limit_kg": LIMIT, "pressure_ceiling_Pa": PCEIL,
        "external_partial_pressures_Pa": PEXT, "geometry": G, "runs": runs,
        "equipment": equipment_rows, "getter_conversion": getter_conversion,
        "systems_ledger": systems_ledger,
        "source_condition_note": "Constant rates are bounding calculations, not claimed flight measurements. Partial-pressure decay maps source water rates to 1 kPa external water as an explicit projection.",
        "ledger_note": "Outgassing changes phase of existing vehicle mass. Only net external ingress adds mass. Passive getters retain external gas; pumping can remove it. The 48.894 kg free-gas operating criterion is reported separately from net added mass.",
    }
    (BASE / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    validation = {"checks": checks, "passed": all(x["pass"] for x in checks),
                  "count": len(checks), "method": "Source conversion reproduction; independent adaptive ODE integration against analytic solutions; integrated external flux; threshold residuals."}
    (BASE / "VALIDATION.json").write_text(json.dumps(validation, indent=2) + "\n")
    concise = {}
    for lead, cases in runs.items():
        r = cases["conditioned_reference"]
        concise[lead] = {
            "source_permeation_kg_day": sum(r["sources"]["permeation_zero_internal_kg_day"].values()),
            "leak_kg_day": sum(r["sources"]["leak_kg_day"].values()),
            "retained_release_inventory_kg": sum(r["sources"]["release_inventory_by_species_kg"].values()),
            "partial_pressure_times": r["times_partial_pressure"],
            "upper_envelope_times": r["times_constant_source_upper_envelope"],
            "p_day1_hot_Pa": r["samples"][1]["pressure_after_instant_heat_to_320K_Pa"],
            "max_total_leak_24h_Pa_m3_s": r["max_total_leak_24h"]["total_leak_Pa_m3_s"],
        }
    print(json.dumps({"checks_passed": len(checks), "reference_cases": concise,
                      "getter": getter_conversion}, indent=2))


if __name__ == "__main__":
    main()
