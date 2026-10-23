#!/usr/bin/env python3
"""Independent fixed-gauge interpretation of the filed +10% area sensitivity."""
from pathlib import Path
import json
import math
from scipy.optimize import brentq

r = Path(__file__).resolve().parent
d = json.loads((r / "INDEPENDENT-RESULTS.json").read_text())
i = json.loads((r / "inputs/034/INPUTS.json").read_text())
e = i["environment"]
R = i["constants"]["R_universal_J_mol_K"]
T, Th = e["T_K"], e["T_hot_K"]
mw = {k: v["M_kg_mol"] for k, v in i["species"].items()}
out = {}
for key in ["P3_Kapton", "P3_Zylon_barrier"]:
    c = d["runs"][key]["area_and_barrier_sensitivity"]
    s, g = c["sources"], d["geometry"][key]
    inv = dict(s["inventory_before_conditioning_kg"])
    if key == "P3_Kapton":
        inv["Kapton_TML_proxy"] *= 1.1
    else:
        inv["Zylon_equilibrium_moisture_proxy"] *= 1.1
        inv["metallized_PET_TML_proxy"] *= 1.1
        b = g["barrier_mass_bill_kg"]
        inv["attachment_and_seals_assumed"] = (
            b["attachment_lamination_assumed"] * 1.1 + b["seam_installation_assumed"]
        ) * i["zylon"]["attachment_TML_assumed"]
    B = sum(inv.values()) * s["retained_fraction"]
    molperday = sum(
        (s["permeation_zero_internal_kg_day"][k] + s["leak_kg_day"][k]) / mw[k]
        for k in mw
    )
    v = g["gas_volume_m3"]
    n0 = e["initial_pressure_Pa"] * v / (R * T)

    def p(t):
        return (n0 + molperday*t + B/mw["H2O"]
                * -math.expm1(-t/s["release_tau_days"])) * R*Th/v

    before = c["times_constant_source_upper_envelope"]["pressure_limit_days_instant_320K_envelope"]
    after = brentq(lambda t: p(t)-d["pressure_ceiling_Pa"], 0, 1000)
    out[key] = {
        "area_multiplier": 1.1,
        "additional_structural_film_mass_kg_at_fixed_gauge": g["structural_film_mass_kg"]*.1,
        "conditioned_release_inventory_filed_kg": sum(s["release_inventory_by_species_kg"].values()),
        "conditioned_release_inventory_area_consistent_kg": B,
        "hot_limit_filed_rate_only_area_case_days": before,
        "hot_limit_with_area_scaled_release_days": after,
        "difference_days": after-before,
        "scope": "Illustration at fixed gauge and gas volume, with the filed transmission multipliers (including Zylon N2 x10); not a structural reoptimization.",
    }
    if key == "P3_Zylon_barrier":
        extra = .1*(b["PET"]+b["Al_assumed_50nm"]+b["attachment_lamination_assumed"])
        low, high = d["systems_ledger"]["P3_Zylon_system_plus_barrier_plus_joint_bond_kg"]
        out[key].update(
            additional_barrier_assembly_kg=extra,
            system_barrier_bond_range_kg_at_10percent_more_area=[low+extra, high+extra],
            remaining_100kg_low_bill=100-low-extra,
            excess_100kg_high_bill=high+extra-100,
        )
(r / "AREA-SENSITIVITY-CHECK.json").write_text(json.dumps(out, indent=2)+"\n")
print("Two area sensitivities calculated; geometry and structural optimization held fixed.")
