#!/usr/bin/env python3
"""Independent scalar implementation of the received equation-only clarification.

The gas calculation takes existing geometry as input. It does not optimize a
geometry, integrate a weather history, or import owner implementation modules.
"""

import csv
import hashlib
import json
import math
import platform
from pathlib import Path

import numpy as np


BASE = Path(__file__).resolve().parent
RG = 8.31446261815324
SCARF_RATIO = 30.34139731914874
CORE_DENSITY = 16.018463373960138


def read(name):
    return json.loads((BASE / "inputs" / name).read_text())


def gas_candidate(radius, mask, knot, pressure, face, core):
    area = 4 * math.pi * radius**2
    sphere = 4 * math.pi * radius**3 / 3
    overlap = SCARF_RATIO * face
    seams = area * (1 / (0.6096 - overlap) + 1 / (1.8288 - overlap))
    film_areal = 0.030 * 0.45359237 / 0.3048**2
    mass = {
        "faces": 2 * area * face * 1850,
        "core": area * core * CORE_DENSITY,
        "film": 2 * area * film_areal * (0.5 if mask & 8 else 1),
        "scarf": 2 * seams * math.sqrt(overlap**2 + face**2) * 0.070,
        "splice": seams * core * 0.0005 * 500,
        "seal": 0.002 * seams,
        "primer": 0.010 * area,
        "coating": 0.00833272 * area,
    }
    connected = (
        sphere
        - mass["faces"] / 1850
        - mass["core"] / 2700
        - (mass["film"] + mass["scarf"] + mass["seal"]) / 1250
        - mass["splice"] / 500
    )
    joint_mass = mass["scarf"] + mass["splice"] + mass["seal"]
    water = 0.1 * (
        0.002 * mass["film"] + 0.001 * mass["core"]
        + 0.01 * mass["primer"] + 0.01 * mass["coating"] + 0.01 * joint_mass
    )
    inventory = 0.1 * (
        0.0485 * mass["film"] + 0.001 * mass["core"] + 0.01 * joint_mass
    ) + water
    initial = 10 * connected / (RG * 258)
    leak = (0.001 * seams + 0.01) * 0.1 * 86400 / (RG * 258)
    diffusion_area = seams * 0.070 / 1250
    permeation = 10 * 3.34645e-16 * diffusion_area / overlap * 106500 * 86400
    air_moles = initial + leak + permeation
    final_pressure = (air_moles + inventory / 0.01801528) * RG * 326 / connected
    final_mass = 0.029 * air_moles + inventory
    allowance = 0.01 * 4889.442150186961 * (radius / 10)**3
    assert connected > 0 and overlap < 0.6096
    return {
        "R_m": radius, "mask": mask, "pressure_knot_index": knot,
        "design_pressure_Pa": pressure, "tf_m": face, "tc_m": core,
        "joint_length_m": seams, "volume_m3": connected,
        "inventory_kg": inventory, "absorbed_water_kg": water,
        "initial_gas_mol": initial, "leak_mol_24h": leak,
        "permeation_mol_24h": permeation,
        "diffusion_area_m2": diffusion_area, "diffusion_path_m": overlap,
        "pressure_Pa": final_pressure, "mass_kg": final_mass,
        "gas_allowance_kg": allowance, "pressure_ceiling_Pa": 800.0,
        "passes": final_pressure < 800 and final_mass <= allowance,
        "component_masses_kg": mass,
    }


def saturation(temperature):
    celsius = temperature - 273.15
    return 611.21 * math.exp(
        (18.678 - celsius / 234.5) * celsius / (257.14 + celsius)
    )


def convection(case, temperature, humidity, wind):
    density = (95460.83791390515 - 0.378 * humidity * saturation(temperature))
    density /= 287.053 * temperature
    reynolds = density * wind * 20 / 1.79e-5
    coefficient = 0.0257 / 20 * (
        2 + (0.4 * math.sqrt(reynolds) + 0.06 * reynolds**(2 / 3)) * 0.71**0.4
    )
    return {
        "case": case, "R_m": 10, "Ta_K": temperature, "RH_water": humidity,
        "wind_m_s": wind, "density_kg_m3": density, "Re": reynolds,
        "h_forced_W_m2K": coefficient,
    }


def main():
    pins = json.loads((BASE / "INPUT-PINS.json").read_text())["inputs"]
    for pin in pins:
        data = (BASE / pin["snapshot"]).read_bytes()
        assert len(data) == pin["bytes"] and hashlib.sha256(data).hexdigest() == pin["sha256"]
    geometry = read("MASS-CURVES.json")
    assert len(geometry["p_Pa"]) == 65
    assert geometry["p_Pa"][0] == 97172.30184301017
    assert geometry["p_Pa"][-1] == 106500.0
    candidates = []
    selected = []
    for radius in (10, 12, 15, 20, 30):
        rows = []
        for mask in range(16):
            curve = geometry["curves"][str(radius)][str(mask)]
            for knot in (0, 64):
                rows.append(gas_candidate(
                    radius, mask, knot, geometry["p_Pa"][knot],
                    curve["tf_m"][knot], curve["tc_m"][knot],
                ))
        candidates.extend(rows)
        pressure_row = max(rows, key=lambda row: row["pressure_Pa"])
        mass_row = max(rows, key=lambda row: row["mass_kg"])
        selected.append({
            "selected": pressure_row, "candidate_count": len(rows),
            "maximum_mass_candidate": {
                key: mass_row[key]
                for key in ("mask", "pressure_knot_index", "mass_kg")
            },
            "mass_and_pressure_maxima_same_candidate": pressure_row is mass_row,
        })
    assert len(candidates) == 160
    default_rh = saturation(280) / saturation(284.9)
    convection_rows = [
        convection("clear_calm_reference", 284.9, default_rh, 0.2),
        convection("overcast_humid", 284.9, 0.95, 0.5),
        convection("clear_saturated", 284.9, 1.0, 0.2),
        convection("clear_cold_frost", 268.15, 0.9, 0.2),
        convection("dry_reference_regression", 284.9, default_rh, 2.0),
    ]
    low, high = 200.0, 284.9
    vapor_pressure = default_rh * saturation(284.9)
    for _ in range(60):
        middle = (low + high) / 2
        if saturation(middle) < vapor_pressure:
            low = middle
        else:
            high = middle
    target = max((low + high) / 2, 273.15) + 0.05
    coefficient = max(
        convection_rows[0]["h_forced_W_m2K"],
        1.32 * max(abs(target - 284.9), 0.05)**0.25,
    )
    a = 0.8 * 5.670374419e-8 * (target**4 - (260**4 + 284.9**4) / 2)
    a += coefficient * (target - 284.9)
    b = 0.8 * 5.670374419e-8 * (284.9**4 - 260**4) / 2
    exact = 0.0 if a <= -b else a if a >= b else (a + b)**2 / (4 * b)
    nodes, weights = np.polynomial.legendre.leggauss(128)
    quadrature = float(np.dot(weights, np.maximum(a + b * nodes, 0)) / 2)
    heating = {
        "setpoint_K": target, "a_W_m2": a, "b_W_m2": b,
        "filed_128_Gauss_W_m2": quadrature,
        "analytic_positive_part_W_m2": exact,
        "difference_W_m2": quadrature - exact,
    }

    # Comparison answers are first consumed after the independent calculations.
    filed = read("SUPPLEMENTAL-RESULTS.json")["gas_24h_bounds"]
    clarified = read("SCALAR-REPLAY.json")
    gas_fields = {
        "pressure_Pa": "pressure_Pa_upper", "mass_kg": "mass_kg_upper",
        "volume_m3": "connected_gas_volume_m3", "inventory_kg": "inventory_kg",
    }
    differences = []
    for record, expected in zip(selected, filed, strict=True):
        row = record["selected"]
        assert row["R_m"] == expected["R_m"]
        delta = {key: row[key] - expected[value] for key, value in gas_fields.items()}
        differences.append({
            "R_m": row["R_m"], "delta_checker_minus_original": delta,
            "selected_mask_matches": row["mask"] == expected["mask"],
            "all_within_1e-9": all(abs(value) <= 1e-9 for value in delta.values()),
        })
    convection_differences = []
    for row, expected in zip(convection_rows, clarified["R10_convection_constants"], strict=True):
        assert row["case"] == expected["case"]
        convection_differences.append({
            "case": row["case"],
            "delta_checker_minus_clarification": {
                key: row[key] - expected[key]
                for key in ("density_kg_m3", "Re", "h_forced_W_m2K")
            },
        })
    heating_differences = {
        key: value - clarified["heating_quadrature"][key]
        for key, value in heating.items()
    }
    comparisons = {
        "gas": differences, "convection": convection_differences,
        "heating_delta_checker_minus_clarification": heating_differences,
        "gas_max_abs_difference_by_quantity": {
            key: max(abs(row["delta_checker_minus_original"][key]) for row in differences)
            for key in gas_fields
        },
    }
    assert all(row["all_within_1e-9"] and row["selected_mask_matches"] for row in differences)
    assert all(row["passes"] for row in candidates)
    assert all(row["mass_and_pressure_maxima_same_candidate"] for row in selected)
    assert all(
        abs(value) <= 1e-8
        for row in convection_differences
        for value in row["delta_checker_minus_clarification"].values()
    )
    assert all(abs(value) <= 1e-10 for value in heating_differences.values())
    result = {
        "scope": "160 supplied frozen-thermal endpoint geometries; scalar equations only",
        "status": "QUESTIONABLE / PROJECTION",
        "owner_executable_access": False,
        "gas_candidate_count": len(candidates), "gas_selected_rows": selected,
        "all_sampled_candidates_pass_declared_reserve": True,
        "convection": convection_rows, "heating": heating,
        "comparisons": comparisons, "all_numerical_comparisons_pass": True,
        "qualified_installed_hull_SF": None,
        "qualified_sealed_life": None, "qualified_operational_availability": None,
        "environment": {"python": platform.python_version(), "numpy": np.__version__},
    }
    (BASE / "RESULTS.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    (BASE / "GAS-CANDIDATES.json").write_text(json.dumps(candidates, indent=2, allow_nan=False) + "\n")
    csv_keys = [key for key in candidates[0] if key != "component_masses_kg"]
    with (BASE / "GAS-CANDIDATES.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(candidates)
    print(json.dumps({
        "candidate_count": len(candidates),
        "all_comparisons_pass": result["all_numerical_comparisons_pass"],
        "gas_max_abs_differences": comparisons["gas_max_abs_difference_by_quantity"],
        "selected": [
            {key: record["selected"][key] for key in
             ("R_m", "mask", "pressure_knot_index", "pressure_Pa", "mass_kg")}
            for record in selected
        ],
        "heating": heating,
    }, indent=2))


if __name__ == "__main__":
    main()
