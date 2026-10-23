"""MAINLINE-022b interface: explicit tensile size effects and two force rules.

All provided SA calibrations are PROJECTION. No qualified compression
allowable is supplied. SI units are used except for dimensionless ratios.
No third-party Python dependency is needed.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def tube_geometry(outer_radius_m, wall_m, member_length_m, member_count):
    if not (outer_radius_m > wall_m > 0 and member_length_m > 0 and member_count > 0):
        raise ValueError("Require radius > wall > 0, positive length and count")
    inner = outer_radius_m - wall_m
    area = math.pi * wall_m * (outer_radius_m + inner)
    inertia = area * (outer_radius_m**2 + inner**2) / 4
    return {
        "outer_radius_m": outer_radius_m, "wall_m": wall_m,
        "inner_radius_m": inner, "member_length_m": member_length_m,
        "member_count": member_count, "A_m2": area, "I_m4": inertia,
        "total_volume_m3": area * member_length_m * member_count,
        "total_inner_area_m2": 2 * math.pi * inner * member_length_m * member_count,
        "total_outer_area_m2": 2 * math.pi * outer_radius_m * member_length_m * member_count,
        "end_annuli_included": False,
    }


def effective_measure(normalized_positive_stress, measure_weights, m):
    """Integrate (sigma_positive / reference_peak)^m dV or dA.

    Weights must be nonnegative and in consistent m^3 or m^2 units. This is
    one uniaxial tensile flaw population, not a general multiaxial CARES model.
    Use a different effective measure for each fitted m when fields vary.
    """
    stresses = list(normalized_positive_stress)
    weights = list(measure_weights)
    if len(stresses) != len(weights) or m <= 0:
        raise ValueError("Matching quadrature lengths and positive m required")
    if any(weight < 0 for weight in weights):
        raise ValueError("Negative quadrature measures are invalid")
    if any(stress > 1 + 1e-12 for stress in stresses):
        raise ValueError("Normalize stresses to the stated maximum tensile stress")
    return sum(max(stress, 0.0)**m * weight for stress, weight in zip(stresses, weights))


def weibull_threshold(characteristic_stress_Pa, m, reference_measure,
                      effective_assembly_measure, failure_probability):
    """Conditional peak tensile stress for one calibrated flaw population.

    Reference/effective measures must share the same units and population.
    None for zero tensile exposure does NOT mean infinite compression strength.
    No confidence bound, aging, proof-test or unknown population is fabricated.
    """
    if not (characteristic_stress_Pa > 0 and m > 0 and reference_measure > 0):
        raise ValueError("Positive calibration values required")
    if effective_assembly_measure < 0 or not 0 < failure_probability < 1:
        raise ValueError("Nonnegative measure and 0 < failure_probability < 1 required")
    if effective_assembly_measure == 0:
        return None
    return characteristic_stress_Pa * (
        -math.log1p(-failure_probability)
        * reference_measure / effective_assembly_measure
    )**(1 / m)


def sa_illustrative_calibration(m, flaw_measure="volume"):
    """Assumed mean380 MPa and unverified40/20 mm four-point bend spans.

    Manufacturer supplied3x4x45 mm bars and m8/m10 alternatives, but did NOT
    establish this mean interpretation, span pair or qualified flaw model.
    """
    if m not in (8, 10):
        raise ValueError("Only the two explicitly documented SA sensitivity cases exist")
    width, depth, outer_span, inner_span = .004, .003, .040, .020
    effective_length = inner_span + (outer_span - inner_span) / (m + 1)
    if flaw_measure == "volume":
        reference = width * depth * effective_length / (2 * (m + 1))
        units = "m3"
    elif flaw_measure == "surface":
        reference = (width + depth / (m + 1)) * effective_length
        units = "m2"
    else:
        raise ValueError("flaw_measure must be volume or surface")
    return {
        "classification": "PROJECTION", "m": m,
        "characteristic_stress_Pa": 380e6 / math.gamma(1 + 1 / m),
        "reference_measure": reference, "measure_units": units,
        "flaw_measure": flaw_measure,
        "assumptions": "380 MPa as mean; spans40/20 mm; same flaw population and finish; no confidence bound",
    }

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def member_demand(geometry, pressure_Pa, sphere_radius_m, node_spacing_m,
                  modulus_Pa, force_factor, bow_over_length=.001):
    area, inertia = geometry["A_m2"], geometry["I_m4"]
    length = geometry["member_length_m"]
    force = force_factor * pressure_Pa * sphere_radius_m * node_spacing_m / 2
    mean = force / area
    euler = math.pi**2 * modulus_Pa * inertia / (area * length**2)
    eta = bow_over_length * length * geometry["outer_radius_m"] * area / inertia
    result = {
        "classification": "QUESTIONABLE surrogate",
        "force_factor_relative_to_pRs_over2": force_factor,
        "N_N": force, "mean_compression_Pa": mean, "Euler_stress_Pa": euler,
        "eta": eta, "N_over_Ne": mean / euler,
        "qualified_compression_allowable_Pa": None,
        "qualified_compression_margin": None,
    }
    if mean >= euler:
        result.update(
            status="Euler capacity exceeded; finite prebuckling fibre stresses refused",
            maximum_compression_Pa=None, opposite_compression_Pa=None,
            maximum_tension_Pa=None,
        )
    else:
        bending = mean * eta / (1 - mean / euler)
        result.update(
            status="elastic stress calculation only; no local/global/contact validation",
            bending_Pa=bending, maximum_compression_Pa=mean + bending,
            opposite_compression_Pa=mean - bending,
            maximum_tension_Pa=max(0.0, bending - mean),
        )
    return result


def assumed_compression_capacity(Fc_Pa, demand):
    """Conditional extreme-compression pressure multiplier; Fc is caller input."""
    if Fc_Pa <= 0:
        raise ValueError("Explicit positive assumed Fc required")
    euler, eta = demand["Euler_stress_Pa"], demand["eta"]
    phi = (Fc_Pa + (1 + eta) * euler) / 2
    mean_at_limit = Fc_Pa * euler / (phi + math.sqrt(phi**2 - Fc_Pa * euler))
    return {
        "classification": "PROJECTION: caller-assumed compression input",
        "assumed_Fc_Pa": Fc_Pa,
        "mean_stress_ratio_only": Fc_Pa / demand["mean_compression_Pa"],
        "extreme_compression_pressure_multiplier": mean_at_limit / demand["mean_compression_Pa"],
        "excludes": "tensile/contact, local shell, global lattice, film and mass feasibility",
        "qualified_allowable": False,
    }


def examples():
    inputs = json.loads((ROOT / "INPUTS.json").read_text())
    reference = inputs["baseline_SiC"]
    case = inputs["case"]
    spacing = reference["s_m"]
    count = 8 * math.pi * math.sqrt(3) * case["R_m"]**2 / spacing**2
    geometry = tube_geometry(reference["r_o_m"], reference["wall_m"], spacing, count)
    screens = uniform_tensile_screens(geometry)
    demands = {}
    for name, factor in (("equilateral_equilibrium", 1/math.sqrt(3)), ("legacy_pRs_over2", 1.0)):
        demand = member_demand(
            geometry, case["p_ext_Pa"], case["R_m"], spacing,
            reference["E_Pa"], factor,
        )
        demand["assumed_compression_capacity"] = [
            assumed_compression_capacity(strength, demand)
            for strength in (100e6, 200e6, 380e6, 1000e6, 3900e6)
        ]
        demand["hypothetical_contact_Ct_caps"] = [
            {
                "m": row["m"], "flaw_measure": row["flaw_measure"],
                "Ct": row["tensile_threshold_Pa"] / demand["mean_compression_Pa"],
                "classification": "PROJECTION for this uniform tensile-field hypothesis only",
            } for row in screens
        ]
        demands[name] = demand
    twice = tube_geometry(reference["r_o_m"], reference["wall_m"], spacing, 2*count)
    double_screens = uniform_tensile_screens(twice)
    checks = []

    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})
        if not condition:
            raise AssertionError(name)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    result = examples()
    (ROOT / "ALLOWABLE-DEMANDS.json").write_text(
        json.dumps(result, indent=2, allow_nan=False) + "\n"
    )
    print(json.dumps({
        "checks_passed": len(result["verification"]),
        "mean_demand_Pa": {
            name: row["mean_compression_Pa"] for name, row in result["two_demands"].items()
        },
        "output": str(ROOT / "ALLOWABLE-DEMANDS.json"),
    }, indent=2))
