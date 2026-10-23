"""Independent dimensional, load-path and reliability-budget arithmetic.

Run with Python 3 from any directory. Writes only beside this script.
All inherited inputs are QUESTIONABLE. Manufacturing comparisons are
geometric comparisons, not procurement or process capability guarantees.
"""

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def calculate(inputs):
    case = inputs["case"]
    mass = inputs["mass_model"]
    material = inputs["baseline_SiC"]
    target = inputs["reliability_target"]
    radius = case["R_m"]
    pressure = case["p_ext_Pa"]
    spacing = material["s_m"]
    outer = material["r_o_m"]
    thickness = material["wall_m"]
    inner = outer - thickness
    density = material["rho_kg_m3"]
    modulus = material["E_Pa"]
    area = math.pi * (outer**2 - inner**2)
    inertia = math.pi * (outer**4 - inner**4) / 4
    vertices = 8 * math.pi * radius**2 / (math.sqrt(3) * spacing**2) + 2
    edges = 3 * vertices - 6
    total_length = edges * spacing
    tube_mass = density * area * total_length
    node_mass = mass["node_kg_each"] * vertices
    joint_mass = mass["joint_mass_fraction_of_tubes"] * tube_mass
    closed_mass = tube_mass + node_mass + joint_mass + mass["film_kg"] + mass["systems_kg"]
    axial_force = pressure * radius * spacing / 2
    axial_stress = axial_force / area
    ideal_sag = radius - math.sqrt(radius**2 - (spacing / 2)**2)
    arc_length = 2 * radius * math.asin(spacing / (2 * radius))
    maximum_tube_mass_ignoring_nodes = (
        case["lift_mass_kg"] - mass["film_kg"] - mass["systems_kg"]
    ) / (1 + mass["joint_mass_fraction_of_tubes"])
    stress_per_density_ignoring_nodes = (
        4 * math.pi * math.sqrt(3) * pressure * radius**3
        / maximum_tube_mass_ignoring_nodes
    )
    reliability_budget = []
    for system_probability in (
        target["system_failure_probability"],
        target["sensitivity_system_failure_probability"],
    ):
        count = target["member_count_for_integer_allocation"]
        reliability_budget.append({
            "system_probability": system_probability,
            "members": count,
            "union_bound_budget_per_member": system_probability / count,
            "equal_independent_series_probability_per_member": -math.expm1(
                math.log1p(-system_probability) / count
            ),
            "status": "QUESTIONABLE analyst-selected target; no qualified distribution",
        })
    wall_comparisons = []
    for wall in (0.002, 0.004):
        new_area = math.pi * (outer**2 - (outer - wall)**2)
        new_tube_mass = density * new_area * total_length
        new_mass = (
            (1 + mass["joint_mass_fraction_of_tubes"]) * new_tube_mass
            + node_mass + mass["film_kg"] + mass["systems_kg"]
        )
        wall_comparisons.append({
            "wall_m": wall,
            "wall_ratio_to_proposal": wall / thickness,
            "annular_area_and_tube_mass_ratio_same_OD": new_area / area,
            "assembly_mass_kg_same_OD_spacing_density": new_mass,
            "mass_to_lift_ratio": new_mass / case["lift_mass_kg"],
            "status": "PROJECTION: borrowed SiSiC wall envelope applied geometrically to inherited SA density",
        })
    upper_bounds = []
    for rho, strengths, label in (
        (density, (100e6, 200e6, 380e6, 1000e6, 3900e6), "SiC conditional compression"),
        (2440.0, (128e6, 300e6, 580e6), "CVI CMC mixed scalar screening"),
    ):
        minimum_stress = stress_per_density_ignoring_nodes * rho
        for strength in strengths:
            upper_bounds.append({
                "scenario": label,
                "rho_kg_m3": rho,
                "assumed_Fc_Pa": strength,
                "minimum_mean_stress_Pa_inherited_load_path": minimum_stress,
                "maximum_strength_only_SF_inherited_load_path": strength / minimum_stress,
                "maximum_strength_only_SF_triangular_equilibrium": math.sqrt(3) * strength / minimum_stress,
                "status": "PROJECTION: excludes positive node mass, bending, contact and buckling",
            })
    output = {
        "schema": 1,
        "status": "QUESTIONABLE; analytical sensitivities are PROJECTION",
        "formulas": {
            "nodes": "V=8*pi*R^2/(sqrt(3)*s^2)+2",
            "edges": "n=3V-6; total length=n*s=8*pi*sqrt(3)*R^2/s",
            "section": "A=pi*(ro^2-ri^2); I=pi*(ro^4-ri^4)/4",
            "inherited_force": "N=p*R*s/2",
            "triangular_force": "Each of 3 edge families has line density2/(sqrt(3)*s); sum cos(theta)^2=3/2; membrane resultant=sqrt(3)*N/s=pR/2; N=pRs/(2sqrt(3))",
            "mean_stress": "N/A=4*pi*sqrt(3)*rho*p*R^3/Mtube for inherited N",
            "maximum_tube_mass": "(lift-film-systems)/(1+joint_fraction), neglecting positive node mass",
            "cold_bend": "epsilon_max=ro/R; linear elastic sigma=E*ro/R (kinematic warning, not valid past fracture)",
            "sag": "R-sqrt(R^2-(s/2)^2), if s is chord length",
            "arc_length": "2R*asin(s/(2R)), if s is chord length",
            "union_bound": "P(any failure)<=sum(P_i); uniform budget P_i<=P_system/n",
            "independent_series": "P_i=1-(1-P_system)^(1/n)",
        },
        "baseline_geometry": {
            "diameter_m": 2 * outer, "wall_m": thickness, "spacing_m": spacing,
            "radius_to_wall_outer": outer / thickness,
            "vertices_continuum": vertices, "members_continuum": edges,
            "integer_budget_members": math.ceil(edges),
            "total_length_m": total_length, "volume_m3": area * total_length,
            "inside_plus_outside_surface_area_m2": 2 * math.pi * (outer + inner) * total_length,
            "A_m2": area, "I_m4": inertia,
            "tube_mass_kg": tube_mass, "node_mass_kg": node_mass,
            "joint_mass_kg": joint_mass, "closed_mass_kg": closed_mass,
            "inherited_axial_force_N": axial_force, "inherited_axial_stress_Pa": axial_stress,
            "triangular_equilibrium_force_N": axial_force / math.sqrt(3),
            "triangular_equilibrium_mean_stress_Pa": axial_stress / math.sqrt(3),
            "sag_from_chord_m": ideal_sag, "arc_length_from_chord_m": arc_length,
            "arc_length_to_inherited_s_ratio": arc_length / spacing,
            "cold_elastic_bend_outer_fiber_strain": outer / radius,
            "cold_elastic_bend_extreme_stress_Pa": modulus * outer / radius,
            "cold_bend_stress_to_typical_380MPa_ratio": modulus * outer / radius / material["flexural_typical_Pa"],
            "total_joint_budget_per_member_end_kg": joint_mass / (2 * edges),
        },
        "probability_budgets": reliability_budget,
        "manufacturing_dimensional_comparisons": {
            "SA_one_piece_1p4m_length_factor": spacing / 1.4,
            "CVD_202mm_OD_example_required_diameter_factor": 2 * outer / .202,
            "CVD_1p5m_length_example_required_length_factor": spacing / 1.5,
            "CVD_1mm_wall_example_to_required_wall_factor": .001 / thickness,
            "wall_comparisons": wall_comparisons,
            "status": "QUESTIONABLE public examples; not a proven simultaneous product envelope",
        },
        "geometry_free_strength_upper_bounds": upper_bounds,
        "numerical_checks": {
            "mass_balance_absolute_error_kg": abs(closed_mass - case["lift_mass_kg"]),
            "triangular_sum_cos_squared": sum(math.cos(theta)**2 for theta in (0, math.pi/3, 2*math.pi/3)),
            "edge_length_identity_absolute_error_m": abs(total_length - 8*math.pi*math.sqrt(3)*radius**2/spacing),
            "comment": "These are arithmetic identities, not validation of structural behavior.",
        },
    }
    if output["numerical_checks"]["mass_balance_absolute_error_kg"] > 1e-7:
        raise ValueError("Input baseline fails inherited mass closure")
    return output


if __name__ == "__main__":
    result = calculate(json.loads((ROOT / "INPUTS.json").read_text()))
    path = ROOT / "SUPPLEMENT.json"
    path.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "output": str(path), "baseline": result["baseline_geometry"],
        "checks": result["numerical_checks"],
    }, indent=2))
