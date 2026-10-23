#!/usr/bin/env python3
"""Independent MAINLINE-034 arithmetic; no owner/predecessor code imported.

Reconstruct physical quantities from pinned INPUTS. Solve species balances by
an augmented matrix exponential, including an independent external-mass state.
Read owner RESULTS only after constructing the independent result.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import math
import sys
import platform
import numpy as np
import scipy
from scipy.linalg import expm
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
I = json.loads((ROOT / "inputs/034/INPUTS.json").read_text())
RECON = json.loads((ROOT / "RECONSTRUCTION-ASSUMPTIONS.json").read_text())
E, C = I["environment"], I["constants"]
R, T, TH = C["R_universal_J_mol_K"], E["T_K"], E["T_hot_K"]
DAY, P, P0 = C["seconds_per_day"], E["p_external_Pa"], E["initial_pressure_Pa"]
AREA = 4 * math.pi * E["R_m"] ** 2
VSPHERE = AREA * E["R_m"] / 3
MLIMIT = E["lift_reference_kg"] * E["gas_mass_fraction_limit"]
PLIMIT = P * E["pressure_ceiling_fraction"]
SP = tuple(I["species"])
M = np.array([I["species"][s]["M_kg_mol"] for s in SP])
XDRY = np.array([I["species"][s]["dry_x"] for s in SP])
XDRY /= sum(XDRY)
PEXT = XDRY * (P - E["water_partial_external_Pa"])
PEXT[SP.index("H2O")] = E["water_partial_external_Pa"]
XEXT = PEXT / P
RHOEXT = sum(PEXT * M) / (R * T)
SYS = I["systems"]
POWER_DENSITY = (SYS["battery_Wh_kg"] * SYS["battery_usable_fraction"]
                 * SYS["power_conversion_efficiency"])


def species_dict(x):
    return {s: float(v) for s, v in zip(SP, x)}


def write_json(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")


def geometry():
    p = I["P2"]
    clear = p["panel_width_m"] - p["scarf_run_ratio"] * p["face_thickness_m"]
    seam = 2 * AREA / clear
    path = math.hypot(p["face_thickness_m"],
                      p["face_thickness_m"] * p["scarf_run_ratio"])
    gap = p["scarf_film_kg_m2"] / p["scarf_density_assumed_kg_m3"]
    bond = 2 * AREA * p["bond_film_kg_m2_per_face"]
    scarf = 2 * seam * path * p["scarf_film_kg_m2"]
    splice = seam * p["core_thickness_m"] * p["core_splice_gap_m"] * p["core_splice_density_kg_m3"]
    seal = seam * p["seal_mass_kg_per_unique_m"]
    face_volume = 2 * AREA * p["face_thickness_m"]
    core_volume = p["core_mass_kg"] / p["core_metal_density_kg_m3"]
    bond_volume = bond / RECON["AF163_density_assumed_kg_m3"]
    splice_volume = splice / p["core_splice_density_kg_m3"]
    solids = (face_volume + core_volume
              + bond_volume + scarf / p["scarf_density_assumed_kg_m3"]
              + splice / p["core_splice_density_kg_m3"])
    void = AREA * p["core_thickness_m"] - core_volume
    if RECON["core_void_subtract_full_bond_and_splice_volumes"]:
        void -= bond_volume + splice_volume
    g = {"P2": {
        "gas_volume_m3": VSPHERE - solids,
        "area_per_face_m2": AREA,
        "faces_total_area_m2": 2 * AREA,
        "face_thickness_m": p["face_thickness_m"],
        "core_thickness_m": p["core_thickness_m"],
        "seam_m": seam,
        "nodes": AREA / clear ** 2 + 2,
        "bond_film_mass_kg": bond,
        "scarf_both_faces_mass_kg": scarf,
        "core_splice_mass_kg": splice,
        "seal_mass_kg": seal,
        "scarf_path_m": path,
        "scarf_gap_m": gap,
        "scarf_diffusion_area_over_length_m": seam * gap / path,
        "core_wall_area_estimate_m2": 4 * AREA * p["core_thickness_m"] / p["core_cell_m"],
        "core_void_m3": void,
        "unvented_core_air_kg": void * RHOEXT,
        "known_solids_volume_m3": solids,
    }}
    for label, key, density in [
        ("P3_Kapton", "kapton", 1420),
        ("P3_Zylon_barrier", "zylon_barrier", 1560),
    ]:
        v = I["P3"][key]
        nodes = AREA / (math.sqrt(3) * v["s_m"] ** 2 / 2) + 2
        members = 3 * nodes - 6
        length = 2 * E["R_m"] * math.asin(v["s_m"] / (2 * E["R_m"]))
        total_length = members * length
        outer = v["r_o_m"]
        inner = outer - v["t_w_m"]
        tube_volume = math.pi * (outer ** 2 - inner ** 2) * total_length
        bore = math.pi * inner ** 2 * total_length
        surface = 2 * math.pi * (outer + inner) * total_length
        sag = v["sag_kg"] * VSPHERE / E["lift_reference_kg"]
        adhesive = I["P3"]["joint_adhesive"]
        joint_area = 2 * members * v["N_N"] / adhesive["tau_Pa_from_023"]
        bond_mass = joint_area * adhesive["gap_m_assumed"] * adhesive["density_kg_m3_assumed"]
        g[label] = {
            "gas_volume_m3": VSPHERE - sag,
            "sag_loss_m3": sag,
            "sag_loss_kg": v["sag_kg"],
            "area_m2": AREA,
            "film_thickness_m": v["t_film_m"],
            "structural_film_mass_kg": AREA * v["t_film_m"] * density,
            "tube_mass_kg": 3100 * tube_volume,
            "joint_mass_kg": 2 * members * v["m_end"],
            "tube_density_from_geometry_kg_m3": v["m_tube"] / tube_volume,
            "tube_inner_and_outer_surface_m2": surface,
            "tube_solid_volume_m3": tube_volume,
            "hollow_bore_volume_m3": bore,
            "unvented_tube_air_kg": bore * RHOEXT,
            "joint_bond_area_m2": joint_area,
            "additional_joint_adhesive_kg": bond_mass,
            "seam_m": total_length,
            "nodes": nodes,
            # Structural safety is inherited, not recomputed by a vacuum check.
            "filed_structural_SF": v["SF_least"],
        }
    z = I["zylon"]
    g["P3_Zylon_barrier"]["barrier_mass_bill_kg"] = {
        "PET": AREA * z["barrier_PET_thickness_m"] * z["barrier_PET_density_kg_m3"],
        "Al_assumed_50nm": AREA * z["barrier_Al_thickness_assumed_m"] * z["barrier_Al_density_kg_m3"],
        "attachment_lamination_assumed": AREA * z["attachment_assumed_kg_m2"],
        "seam_installation_assumed": z["seam_installation_allowance_kg"],
    }
    return g


G = geometry()


def gas_sources(material, options):
    g = G[material]
    perm = np.zeros(len(SP))  # kg/day at zero internal partial pressures
    active_area = AREA * options.get("area_multiplier", 1)
    if material == "P2":
        p = I["P2"]
        permeability = options.get("scarf_Barrer", p["scarf_gas_Barrer_assumed"])
        perm = (permeability * C["Barrer_mol_m_m2_s_Pa"] * DAY
                * g["scarf_diffusion_area_over_length_m"] * PEXT * M)
        inv = {
            "AF163_full_bondlines": g["bond_film_mass_kg"] * options.get("AF_TML", p["AF163_TML_high"]),
            "core_foil_coating_and_nodes_assumed": p["core_mass_kg"] * p["core_release_fraction_assumed"],
            "scarf_splice_and_seal_polymers_assumed": (
                g["scarf_both_faces_mass_kg"] + g["core_splice_mass_kg"] + g["seal_mass_kg"]
            ) * p["other_polymers_release_fraction_assumed"],
        }
    elif material == "P3_Kapton":
        v, k = I["P3"]["kapton"], I["kapton"]
        scale = k["reference_thickness_m"] / v["t_film_m"]
        for n, s in enumerate(SP[:-1]):
            cc = k["gas_ml_m2_day_MPa"][s] * active_area * scale * PEXT[n] / 1e6
            perm[n] = cc / C["Vm_STP_cc_mol"] * M[n]
        perm[-1] = k["water_g_m2_day"] * active_area * scale / 1000
        tml = k["moisture_fraction_50RH"] if options.get("wet_film") else k["outgas_TML_proxy"]
        inv = {
            "Kapton_TML_proxy": g["structural_film_mass_kg"] * tml,
            # Declared in owner RESULTS, absent as a configurable INPUTS scalar.
            # Explicit reconstruction assumption; separately reported as NFI.
            "unmeasured_seals_and_titanium_surfaces_assumed": RECON["Kapton_unmeasured_seals_and_titanium_surfaces_inventory_kg"],
            "SiC_surface_inventory_assumed": g["tube_inner_and_outer_surface_m2"] * I["P3"]["SiC_surface_release_kg_m2_assumed"],
            "EA9394_joint_bonds_TML_proxy": g["additional_joint_adhesive_kg"] * I["P3"]["joint_adhesive"]["TML_proxy"],
        }
    else:
        z, my = I["zylon"], I["mylar"]
        for n, s in enumerate(SP[:-1]):
            ratio = my["permeance_ratios_to_O2_assumed"][s]
            if s == "N2":
                ratio *= options.get("barrier_N2_multiplier", 1)
            cc = my["O2_cc_m2_day_pure_O2"] * active_area * PEXT[n] / C["atm_Pa"] * ratio
            perm[n] = cc / C["Vm_STP_cc_mol"] * M[n]
        perm[-1] = my["water_g_m2_day_upper"] * active_area / 1000
        bill = g["barrier_mass_bill_kg"]
        inv = {
            "Zylon_equilibrium_moisture_proxy": g["structural_film_mass_kg"] * z["moisture_fraction"],
            "unmatched_CFRP_end_wrap_TML_proxy": g["joint_mass_kg"] * options.get("CFRP_TML", z["cfrp_TML_proxy"]),
            "SiC_surface_inventory_assumed": g["tube_inner_and_outer_surface_m2"] * I["P3"]["SiC_surface_release_kg_m2_assumed"],
            "EA9394_joint_bonds_TML_proxy": g["additional_joint_adhesive_kg"] * I["P3"]["joint_adhesive"]["TML_proxy"],
            "metallized_PET_TML_proxy": bill["PET"] * z["PET_TML_proxy"],
            "attachment_and_seals_assumed": (
                bill["attachment_lamination_assumed"] + bill["seam_installation_assumed"]
            ) * z["attachment_TML_assumed"],
        }
    perm[-1] *= options.get("water_multiplier", 1)
    leak_spec = I["leak_model"]
    lr = options.get("leak_rate", leak_spec["seam_rates_mbar_l_s_per_m"][leak_spec["reference_index"]])
    q_leak = (lr * (g["seam_m"] + g["nodes"]) + leak_spec["ports_mbar_l_s"]) * 0.1
    leak = q_leak * DAY / (R * T) * XEXT * M
    retained = options.get("retained_fraction", I["release_model"]["conditioned_retained_fraction"])
    release = np.zeros(len(SP))
    hydrogen_fraction = options.get("outgas_hydrogen_mass_fraction", 0)
    release[SP.index("H2")] = sum(inv.values()) * retained * hydrogen_fraction
    release[-1] = sum(inv.values()) * retained * (1 - hydrogen_fraction)
    tau = options.get("tau_days", I["release_model"]["tau_days"])
    return perm, leak, release, {
        "permeation_zero_internal_kg_day": species_dict(perm),
        "leak_kg_day": species_dict(leak),
        "leak_Pa_m3_s": q_leak,
        "inventory_before_conditioning_kg": inv,
        "release_inventory_by_species_kg": species_dict(release),
        "retained_fraction": retained,
        "release_tau_days": tau,
    }


class Balance:
    """Ten states: seven gas inventories, release driver, constant, external kg."""
    def __init__(self, volume, perm, leak, release, tau, feedback):
        self.volume, self.release, self.tau = volume, release, tau
        self.initial_moles = P0 * volume / (R * T) * XDRY
        q, l, b = perm / M, leak / M, release / M
        k = q * R * T / (volume * PEXT) if feedback else np.zeros(len(SP))
        a = np.zeros((10, 10))
        a[:7, :7] = -np.diag(k)
        a[:7, 7] = b / tau
        a[:7, 8] = q + l
        a[7, 7] = -1 / tau
        # Separate integrated external flux, not inferred by subtracting release.
        a[9, :7] = -k * M
        a[9, 8] = sum(perm + leak)
        self.a = a
        self.y0 = np.r_[self.initial_moles, 1, 1, 0]
        self.cache = {}

    def sample(self, day):
        if day in self.cache:
            return self.cache[day]
        y = expm(self.a * day) @ self.y0
        gas = y[:7] * M
        pressure = y[:7] * R * T / self.volume
        released = sum(self.release) * -math.expm1(-day / self.tau)
        out = {
            "days": day,
            "pressure_Pa": float(sum(pressure)),
            "pressure_after_instant_heat_to_320K_Pa": float(sum(pressure) * TH / T),
            "gas_mass_kg": float(sum(gas)),
            "external_net_mass_added_kg": float(y[9]),
            "existing_material_released_kg": float(released),
            "species_gas_mass_kg": species_dict(gas),
            "species_pressure_Pa": species_dict(pressure),
        }
        self.cache[day] = out
        return out

    def crossing(self, key, limit):
        high = 1.
        while self.sample(high)[key] < limit:
            high *= 2
            if high > 1e8:
                return None
        return brentq(lambda t: self.sample(t)[key] - limit, 0, high, xtol=1e-10, rtol=1e-13)

    def times(self):
        return {
            "gas_inventory_limit_days": self.crossing("gas_mass_kg", MLIMIT),
            "external_added_mass_limit_days": self.crossing("external_net_mass_added_kg", MLIMIT),
            "pressure_limit_days_at_284p9K": self.crossing("pressure_Pa", PLIMIT),
            "pressure_limit_days_instant_320K_envelope": self.crossing("pressure_after_instant_heat_to_320K_Pa", PLIMIT),
        }


def maximum_leak(g, perm, release, tau):
    released = release * -math.expm1(-1 / tau)
    v = g["gas_volume_m3"]
    n0 = P0 * v / (R * T) * XDRY
    # Candidate leak limits in mol/day; select limiting mass or hot pressure.
    mass_per_mole = sum(XEXT * M)
    nlimit_mass = (MLIMIT - sum(n0 * M + perm + released)) / mass_per_mole
    nlimit_external = (MLIMIT - sum(perm)) / mass_per_mole
    nlimit_hot = PLIMIT * v / (R * TH) - sum(n0 + (perm + released) / M)
    nlimit = max(0, min(nlimit_mass, nlimit_external, nlimit_hot))
    q = nlimit * R * T / DAY
    return {
        "total_leak_Pa_m3_s": q,
        "total_leak_mbar_l_s": q * 10,
        "air_sccm_at_STP": nlimit * C["Vm_STP_cc_mol"] / (24 * 60),
        "equal_seam_and_node_rate_mbar_l_s": max(
            0, (q * 10 - I["leak_model"]["ports_mbar_l_s"]) / (g["seam_m"] + g["nodes"])
        ),
    }


COMMON_CASES = {
    "conditioned_reference": {},
    "unconditioned": {"retained_fraction": 1.},
    "low_leak": {"leak_rate": 1e-5},
    "high_leak": {"leak_rate": .1},
    "unconditioned_high_leak": {"retained_fraction": 1., "leak_rate": .1},
    "water_rate_one_tenth": {"water_multiplier": .1},
    "slow_unconditioned_release": {"retained_fraction": 1., "tau_days": 10.},
    "area_and_barrier_sensitivity": {"area_multiplier": 1.1, "barrier_N2_multiplier": 10.},
    "outgas_5percent_H2": {"outgas_hydrogen_mass_fraction": .05},
}
CASE_EXTRAS = {
    "P2": {"AF_low_TML": {"AF_TML": .0259}, "scarf_100Barrer": {"scarf_Barrer": 100.}},
    "P3_Kapton": {"wet_unconditioned_film": {"retained_fraction": 1., "wet_film": True}},
    "P3_Zylon_barrier": {"CFRP_one_percent_unconditioned": {"retained_fraction": 1., "CFRP_TML": .01}},
}
DAYS = [0, 1, 7, 14, 30, 90, 365]
RUNS = {}
CONSERVATION = []
for material, g in G.items():
    RUNS[material] = {}
    for name, options in (COMMON_CASES | CASE_EXTRAS[material]).items():
        perm, leak, release, src = gas_sources(material, options)
        models = [Balance(g["gas_volume_m3"], perm, leak, release, src["release_tau_days"], b)
                  for b in [True, False]]
        samples = [[m.sample(d) for d in DAYS] for m in models]
        for j, ss in enumerate(samples):
            for s in ss:
                difference = (s["gas_mass_kg"] - ss[0]["gas_mass_kg"]
                              - s["existing_material_released_kg"] - s["external_net_mass_added_kg"])
                CONSERVATION.append({"material": material, "case": name, "feedback": j == 0,
                                     "day": s["days"], "mass_balance_residual_kg": difference})
        RUNS[material][name] = {
            "assumptions": options,
            "sources": src,
            "times_partial_pressure": models[0].times(),
            "times_constant_source_upper_envelope": models[1].times(),
            "samples": samples[0],
            "samples_constant_upper": [models[1].sample(d) for d in [1, 7, 30]],
            "max_total_leak_24h": maximum_leak(g, perm, release, src["release_tau_days"]),
        }


def equipment():
    result = {}
    for material in G:
        perm, leak, release, src = gas_sources(material, {})
        mdot = perm + leak
        throughput = sum(mdot / M) * R * T / DAY
        hot = throughput * TH / T
        speed = throughput * 3600 / PLIMIT
        hot_speed = hot * 3600 / PLIMIT
        rec = {
            "steady_source_upper_kg_day": float(sum(mdot)),
            "steady_source_upper_Pa_m3_s_at_T": float(throughput),
            "steady_source_upper_Pa_m3_s_at_320K": float(hot),
            "required_effective_speed_m3_h_at_T": float(speed),
            "required_effective_speed_m3_h_at_320K": float(hot_speed),
            "reversible_isothermal_power_floor_W_at_T": float(throughput * math.log(P / PLIMIT)),
        }
        for pump_name in ["KNF_N920_APDCB", "Edwards_E2M28"]:
            p = SYS[pump_name]
            raw_speed = p.get("speed_at_10mbar_m3_h_chart_read", p.get("nominal_speed_50Hz_m3_h"))
            effective = raw_speed * SYS["installed_speed_fraction_assumed"]
            power = p.get("input_W", p.get("input_W_assumed"))
            battery = (power + SYS["monitoring_W"]) * 24 / POWER_DENSITY
            installed = (SYS["sealed_vacuum_hardware_kg"] + SYS["sealed_controls_kg"]
                         + SYS["continuous_pump_plumbing_filters_oil_allowance_kg"]
                         + p["pump_kg"] + battery)
            rec[pump_name] = {
                "effective_speed_m3_h_assumed": effective,
                "pump_kg": p["pump_kg"],
                "electrical_W": power,
                "battery_24h_continuous_kg": battery,
                "installed_system_kg_continuous_24h": installed,
                "excess_over_100kg": max(0, installed - SYS["retained_allowance_kg"]),
                "steady_speed_ratio_at_T": float(effective / speed),
                "steady_speed_ratio_at_320K": float(effective / hot_speed),
            }
        water = mdot[-1] + release[-1] * -math.expm1(-1 / src["release_tau_days"])
        dry_bed = water / I["getters"]["water_capacity_kg_kg_assumed"]
        dry_system = (SYS["sealed_vacuum_hardware_kg"] + SYS["sealed_controls_kg"]
                      + SYS["sealed_power_package_kg"] + I["getters"]["cartridge_kg"] + dry_bed)
        rec["water_sorbent_only_24h"] = {
            "water_captured_kg_upper": float(water),
            "catalog_dry_bed_kg": float(water / I["getters"]["water_capacity_kg_kg_catalog"]),
            "assumed_vacuum_usable_dry_bed_kg": float(dry_bed),
            "dry_system_kg_assumed": float(dry_system),
            "loaded_system_kg_assumed": float(dry_system + water),
        }
        result[material] = rec
    return result


EQUIP = equipment()
GETTERS = {}
for species, capacity in I["getters"]["NEXTorr_capacity_Torr_l_single_run"].items():
    mol = capacity * C["torr_Pa"] * .001 / (R * I["getters"]["NEXTorr_temperature_K"])
    kg = mol * I["species"][species]["M_kg_mol"]
    GETTERS[species] = {
        "single_run_gas_capacity_kg": kg,
        "kg_getter_per_kg_gas": I["getters"]["NEXTorr_D100_5_getter_kg"] / kg,
    }
base = SYS["sealed_vacuum_hardware_kg"] + SYS["sealed_controls_kg"] + SYS["sealed_power_package_kg"]
band = [base + v for v in SYS["sealed_extra_installation_band_kg"]]
barrier = sum(G["P3_Zylon_barrier"]["barrier_mass_bill_kg"].values())
zbond = G["P3_Zylon_barrier"]["additional_joint_adhesive_kg"]
LEDGER = {
    "passive_identified_system_kg": base,
    "passive_installation_range_kg": band,
    "reserved_systems_line_each_lead_kg": SYS["retained_allowance_kg"],
    "monitoring_power_W": SYS["monitoring_W"],
    "monitoring_days_if_all_10kg_is_usable_battery": SYS["sealed_power_package_kg"] * POWER_DENSITY / (SYS["monitoring_W"] * 24),
    "sealed_system_mass_vs_duration": [{
        "days": d,
        "minimum_battery_kg_at_assumed_pack_factors": SYS["monitoring_W"] * 24 * d / POWER_DENSITY,
        "identified_system_kg_retaining_at_least_10kg_power_package": (
            SYS["sealed_vacuum_hardware_kg"] + SYS["sealed_controls_kg"]
            + max(SYS["sealed_power_package_kg"], SYS["monitoring_W"] * 24 * d / POWER_DENSITY)
        ),
    } for d in [1, 7, 30, 365]],
    "P3_Zylon_added_barrier_attachment_bill_kg": barrier,
    "P3_Zylon_additional_joint_bond_kg": zbond,
    "P3_Kapton_additional_joint_bond_kg": G["P3_Kapton"]["additional_joint_adhesive_kg"],
    "P3_Zylon_vacuum_system_plus_barrier_kg": [x + barrier for x in band],
    "P3_Zylon_system_plus_barrier_plus_joint_bond_kg": [x + barrier + zbond for x in band],
    "P3_Zylon_remaining_of_100kg_at_low_bill": SYS["retained_allowance_kg"] - band[0] - barrier - zbond,
    "P3_Zylon_excess_over_100kg_at_high_bill": band[1] + barrier + zbond - SYS["retained_allowance_kg"],
    "P2_unvented_core_fraction_of_internal_gas_row": G["P2"]["unvented_core_air_kg"] / MLIMIT,
    "P3_Kapton_E2M28_minimum_speed_fraction_hot_source_envelope": EQUIP["P3_Kapton"]["required_effective_speed_m3_h_at_320K"] / SYS["Edwards_E2M28"]["nominal_speed_50Hz_m3_h"],
}
INDEPENDENT = {
    "reference_area_m2": AREA,
    "reference_volume_m3": VSPHERE,
    "gas_mass_limit_kg": MLIMIT,
    "pressure_ceiling_Pa": PLIMIT,
    "external_partial_pressures_Pa": species_dict(PEXT),
    "geometry": G,
    "runs": RUNS,
    "equipment": EQUIP,
    "getter_conversion": GETTERS,
    "systems_ledger": LEDGER,
}
write_json("INDEPENDENT-RESULTS.json", INDEPENDENT)
write_json("CONSERVATION.json", CONSERVATION)

# Comparison begins only after independent model construction and solution.
OWNER = json.loads((ROOT / "inputs/034/RESULTS.json").read_text())


def flatten_numbers(obj, prefix=""):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out.update(flatten_numbers(v, f"{prefix}/{k}"))
        return out
    if isinstance(obj, list):
        out = {}
        for k, v in enumerate(obj):
            out.update(flatten_numbers(v, f"{prefix}/{k}"))
        return out
    if isinstance(obj, (int, float)) and not isinstance(obj, bool):
        return {prefix: obj}
    return {}


expected, actual = flatten_numbers(OWNER), flatten_numbers(INDEPENDENT)
checks = []
for path, value in actual.items():
    if path not in expected:
        raise ValueError(f"Independent quantity has no filed counterpart: {path}")
    filed = expected[path]
    # Fixed before first run: relative 2e-9 with absolute 2e-8 numerical floor.
    # Strict enough for displayed precision while allowing distinct solvers.
    tolerance = 2e-8 + 2e-9 * abs(filed)
    diff = value - filed
    category = "independently_derived"
    if "/assumptions/" in path or path.endswith("/days"):
        category = "scenario_definition"
    if any(path.endswith("/" + k) for k in [
        "face_thickness_m", "core_thickness_m", "film_thickness_m", "filed_structural_SF",
        "sag_loss_kg", "retained_fraction", "release_tau_days", "pump_kg", "electrical_W",
        "reserved_systems_line_each_lead_kg", "monitoring_power_W",
    ]):
        category = "inherited_or_declared_input"
    checks.append({
        "path": path, "owner": filed, "independent": value,
        "difference_independent_minus_owner": diff,
        "tolerance": tolerance, "pass": bool(abs(diff) <= tolerance), "category": category,
    })
uncovered = {p: v for p, v in expected.items() if p not in actual and p != "/schema"}
failures = [c for c in checks if not c["pass"]]
summary = {
    "schema": 1,
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "owner_code_read": False, "owner_code_run": False,
    "method": "Independent geometry and source conversion; augmented 10-state matrix exponential; separately integrated external flux; bracketed threshold roots.",
    "tolerance": "2e-8 + 2e-9*abs(owner), fixed before first run",
    "numeric_comparisons": len(checks),
    "passed": len(checks) - len(failures),
    "failed": len(failures),
    "uncovered_numeric_fields": uncovered,
    "categories": {k: sum(c["category"] == k for c in checks) for k in set(c["category"] for c in checks)},
    "mass_conservation_comparisons": len(CONSERVATION),
    "maximum_mass_conservation_residual_kg": max(abs(c["mass_balance_residual_kg"]) for c in CONSERVATION),
    "python": sys.version,
    "numpy": np.__version__, "scipy": scipy.__version__, "platform": platform.platform(),
}
write_json("NUMERICAL-CHECKS.json", {"summary": summary, "checks": checks})
write_json("NUMERICAL-MISMATCHES.json", {"summary": summary, "mismatches": failures})
print(json.dumps(summary, indent=2))
for item in failures[:20]:
    print(json.dumps(item))
sys.exit(bool(failures or uncovered))
