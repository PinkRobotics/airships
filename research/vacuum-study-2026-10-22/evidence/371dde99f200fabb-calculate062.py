"""MAINLINE062: fixed-case closed-form estimates, not an FE or optimization run."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import json
import math

BASE = Path(__file__).resolve().parent


def read(path):
    return json.loads((BASE / path).read_text())


def save(name, data):
    (BASE / name).write_text(
        json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    )


def calculate():
    cfg = read("ASSUMPTIONS.json")
    original = read("inputs/047/INPUTS.json")
    growth = read("inputs/057/mga057.json")
    p = original["pressure_kPa"] * 1000
    tf0 = original["model"]["tf_each_mm"] / 1000
    tc0 = original["model"]["tc_mm"] / 1000
    d0 = tf0 + tc0
    residual0 = original["thermal_sensitivity"]["face_residual_compression_MPa"]
    fy = cfg["assumed_face_compressive_yield_MPa"]
    calibration = []
    for sf, amplitude in [(1, 1.2179), (1.05, 0.7469)]:
        stress0 = sf * p * 10 / (4 * tf0) / 1e6
        coefficient = (fy / stress0 - 1) * d0 / (amplitude / 1000)
        calibration.append({
            "SF": sf, "CHECK047_reference_amplitude_mm": amplitude,
            "reference_membrane_MPa": stress0, "C": coefficient,
            "reference_tf_mm": tf0 * 1000, "reference_tc_mm": tc0 * 1000,
            "reference_face_separation_mm": d0 * 1000,
        })
    selected = [
        r for r in growth["P2_records"]
        if r["R_m"] in [10, 20, 30] and not r["floor"]
        and (r["R_m"] != 10 or r["source"] == "048")
    ]
    assert len(selected) == 6
    mass_rows, scaling, cost_rows = [], [], []
    for record in selected:
        radius = record["R_m"]
        area = 4 * math.pi * radius**2
        entry = next(m for m in record["masks"] if m["mask"] == 15)
        evaluated = next(m for m in record["evaluated"] if m["mask"] == 15)
        bill = dict(entry["bill"])
        assert math.isclose(
            entry["lift_kg"] - sum(bill.values()), entry["payload_kg"],
            rel_tol=0, abs_tol=1e-8,
        )
        tf = bill["faces"] / (2 * area * cfg["Be_density_kg_m3"])
        tc = bill["core"] / (area * cfg["core_density_kg_m3"])
        d = tf + tc
        retained = cfg["retained_shape_hardware_kg_m2"] * area
        increment_mga = cfg["shape_hardware_MGA_fraction"] * retained
        new_bill = {**bill, "retained_shape_hardware": retained}
        mass_row = {
            "R_m": radius, "weather": record["weather"], "source_case": record["id"],
            "source": record["source"], "mask": 15, "joining_rule": "actual",
            "area_m2": area, "lift_reference_kg": entry["lift_kg"],
            "baseline_bill_kg": bill, "baseline_account_total_kg": sum(bill.values()),
            "baseline_payload_kg": entry["payload_kg"],
            "baseline_hardware_kg": evaluated["hardware_kg"],
            "baseline_concept_MGA_kg": evaluated["mga_sourced_kg"],
            "baseline_concept_payload_kg": evaluated["payload_sourced_kg"],
            "shape_mass_added_kg": retained,
            "shape_MGA_added_kg": increment_mga,
            "whole_bill_before_MGA_kg": new_bill,
            "whole_account_total_before_MGA_kg": sum(new_bill.values()),
            "payload_before_MGA_kg": entry["payload_kg"] - retained,
            "whole_concept_account_total_kg": (
                sum(new_bill.values()) + evaluated["mga_sourced_kg"] + increment_mga
            ),
            "payload_with_concept_MGA_kg": (
                evaluated["payload_sourced_kg"] - retained - increment_mga
            ),
            "payload_at_flat_5pct_hardware_MGA_kg": (
                entry["payload_kg"] - 0.05 * evaluated["hardware_kg"] - 1.05 * retained
            ),
            "mass_bill_scope": (
                "Hardware and allocations plus inherited weather headroom debit. "
                "Weather headroom is not an additional physical mass."
            ),
            "tag": "QUESTIONABLE / PROJECTION",
        }
        assert math.isclose(
            mass_row["lift_reference_kg"] - mass_row["whole_concept_account_total_kg"],
            mass_row["payload_with_concept_MGA_kg"], abs_tol=1e-8,
        )
        mass_rows.append(mass_row)
        if record["weather"] != "ISA":
            continue
        residual = residual0 * (tc / tf) / (tc0 / tf0)
        width = 0.332216 * math.sqrt(radius * d / (10 * d0))
        tolerance_rows = []
        for cal in calibration:
            sf, c = cal["SF"], cal["C"]
            stress = sf * p * radius / (4 * tf) / 1e6
            bare = 1000 * d / c * (fy / stress - 1)
            cured = 1000 * d / c * ((fy - residual) / stress - 1)
            ratio_route = (
                cal["CHECK047_reference_amplitude_mm"] * d / d0
                * ((fy - residual) / stress - 1)
                / (fy / cal["reference_membrane_MPa"] - 1)
            )
            assert math.isclose(cured, ratio_route, rel_tol=1e-12)
            tolerance_rows.append({
                "SF": sf, "membrane_MPa": stress,
                "no_cure_amplitude_mm": bare, "cure_debited_amplitude_mm": cured,
                "amplitude_sensitivity_mm_per_MPa": 1000 * d / (c * stress),
                "ratio_form_reproduction_mm": ratio_route,
            })
        target = cfg["conditional_shop_caps_mm"][str(radius)]
        assert target < tolerance_rows[1]["cure_debited_amplitude_mm"]
        allocations = {
            k: target * fraction for k, fraction in cfg["shape_budget_fractions"].items()
        }
        assert math.isclose(sum(allocations.values()), target, abs_tol=1e-12)
        ell = cfg["scarf_ratio"] * tf
        covered_panel_area = (
            (cfg["blank_width_m"] - ell) * (cfg["blank_length_m"] - ell)
        )
        panels = math.ceil(area / covered_panel_area)
        line_length = area * (
            1 / (cfg["blank_width_m"] - ell)
            + 1 / (cfg["blank_length_m"] - ell)
        )
        rectangular_blank_stock = (
            2 * panels * cfg["blank_width_m"] * cfg["blank_length_m"]
            * tf * cfg["Be_density_kg_m3"]
        )
        assert rectangular_blank_stock >= bill["faces"]
        scaling.append({
            "R_m": radius, "source_case": record["id"],
            "tf_each_mm": 1000 * tf, "tc_mm": 1000 * tc, "d_mm": 1000 * d,
            "core_to_face_thickness_ratio": tc / tf,
            "cure_compression_debit_MPa": residual,
            "Gaussian_e_fold_width_m": width,
            "small_patch_single_Gaussian_RMS_at_shop_cap_mm": target * width / (math.sqrt(8) * radius),
            "conditional_shop_cap_mm": target, "shape_budget_mm": allocations,
            "max_scan_spacing_m": width / 8,
            "tolerances": tolerance_rows,
            "homothetic_SF1_mm": 1.2179 * radius / 10,
            "homothetic_SF105_mm": 0.7469 * radius / 10,
            "panels_per_skin_with_ideal_tiling": panels,
            "face_blanks_total": 2 * panels, "unique_joint_length_m": line_length,
            "two_face_scarf_length_m": 2 * line_length,
            "rectangular_blank_stock_before_process_loss_kg": rectangular_blank_stock,
            "net_face_to_rectangular_blank_yield": bill["faces"] / rectangular_blank_stock,
            "tag": "QUESTIONABLE / PROJECTION",
        })
        amounts = []
        for side in ["low", "high"]:
            rates = cfg["cost_rates"][side]
            stock = rectangular_blank_stock / rates["purchased_stock_yield"]
            jig_mass = area * rates["temporary_jig_kg_m2"]
            items = {
                "flat_Be_stock_including_purchase_loss": stock * rates["Be_USD_kg"],
                "face_forming_and_supplier_preparation": 2 * panels * rates["forming_hours_per_face"] * rates["labor_USD_hour"],
                "core_material_and_profile_machining": area * tc * rates["core_USD_m3"],
                "joining_materials": bill["charged_joining"] * rates["joining_USD_kg"],
                "panel_bond_cure_labor": panels * rates["bond_hours_per_panel"] * rates["labor_USD_hour"],
                "two_face_scarf_assembly_labor": 2 * line_length * rates["seam_hours_per_m"] * rates["labor_USD_hour"],
                "retained_shape_hardware_materials": retained * rates["shape_hardware_USD_kg"],
                "temporary_jig_fabrication": jig_mass * rates["jig_USD_kg"],
                "metrology_and_NDE": rates["metrology_fixed_USD"] + area * rates["metrology_USD_m2"],
                "finish_and_primer": area * rates["finish_USD_m2"],
                "mooring_pad_fabrication": bill["mooring_pad"] * rates["pad_USD_kg"],
                "systems_ground_vacuum_and_consumables": rates["systems_and_service_USD"],
                "assembly_hall_provision": rates["hall_R10_USD"] * (radius / 10)**2.5,
                "handling_transport_and_setup": rates["handling_R10_USD"] * (radius / 10)**2,
                "coupon_process_and_subscale_qualification_allowance": rates["qualification_USD"],
            }
            subtotal = sum(items.values())
            contingency = subtotal * rates["cost_contingency_fraction"]
            amounts.append({
                "scenario": side, "items_USD": items, "subtotal_USD": subtotal,
                "cost_contingency_USD": contingency, "total_USD": subtotal + contingency,
                "total_USD_per_shell_m2": (subtotal + contingency) / area,
                "purchased_Be_kg": stock, "temporary_jig_mass_kg": jig_mass,
                "stock_takeoff": "Full rectangular blanks before scarf trimming, divided by additional process/procurement yield; no scrap credit.",
                "non_stock_subtotal_before_contingency_USD": subtotal - items["flat_Be_stock_including_purchase_loss"],
                "tag": "PROJECTION; planning rates, not quotations",
            })
        cost_rows.append({
            "R_m": radius, "area_m2": area, "weather_geometry": "ISA",
            "scenario_range": amounts,
            "scope": cfg["cost_scope"],
        })
    assert all(r["payload_with_concept_MGA_kg"] < 0 for r in mass_rows)
    assert [r["R_m"] for r in scaling] == [10, 20, 30]
    results = {
        "unit": "vacuum-mainline062-buildable-shape-1020",
        "status": "QUESTIONABLE / PROJECTION", "physical_qualification": "open",
        "model_admissibility": "not admissible for a physical hull tolerance",
        "FE_runs_performed": 0, "parameter_optimization_performed": False,
        "calibration": calibration, "scaling": scaling,
        "whole_mass_bills": mass_rows, "whole_cost_bills": cost_rows,
        "ALMA_reference_cost_USD2000_per_projected_m2": 137e6 / (25 * math.pi * 6**2),
        "ALMA_AEC_total_system_kg_per_projected_m2": 80000 / (math.pi * 6**2),
        "ALMA_Vertex_total_system_kg_per_projected_m2": 108000 / (math.pi * 6**2),
        "GBT_whole_system_kg_per_projected_m2": 7.7e6 / 7854,
        "Keck_mirror_segments_kg_per_nominal_aperture_m2": 36 * 400 / (math.pi * 5**2),
        "Webb_mirror_only_kg_per_unobscured_collecting_m2": 18 * 20 / 25,
        "sourced_shop_quote": None, "demonstrated_cheapest_feasible_route": None,
        "selected_conditional_route": "Supplier-formed panels, panel-level cure, temporary ground adjusters, metrology, passive closure",
        "measured_times": {
            "start": cfg["measured_intake_at"],
            "calculation_end": datetime.now(timezone.utc).isoformat(),
            "start_definition": "Recorded initial brief-intake state time; not a budget",
            "filing_time": "See admitted queue report",
        },
        "usage_measurements": {
            "attributed_tokens": None, "codex_points_before": None,
            "codex_points_after": None,
            "reason": "No measured provider quota telemetry available to this calculation; no estimate substituted",
        },
        "piece_review": "External REVIEW-A pending; this card does not claim its own independent review",
    }
    save("RESULTS.json", results)
    with (BASE / "MASS-BILL.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["R_m", "weather", "item", "kg", "scope"])
        for row in mass_rows:
            for item, value in row["whole_bill_before_MGA_kg"].items():
                writer.writerow([row["R_m"], row["weather"], item, value, "baseline plus retained shape hardware"])
            writer.writerow([row["R_m"], row["weather"], "concept_MGA", row["baseline_concept_MGA_kg"] + row["shape_MGA_added_kg"], "allowance"])
            writer.writerow([row["R_m"], row["weather"], "payload_with_concept_MGA", row["payload_with_concept_MGA_kg"], "lift less complete account"])
    with (BASE / "COST-BILL.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["R_m", "scenario", "item", "USD_2026_planning"])
        for row in cost_rows:
            for scenario in row["scenario_range"]:
                for item, value in scenario["items_USD"].items():
                    writer.writerow([row["R_m"], scenario["scenario"], item, value])
                for item in ["cost_contingency_USD", "total_USD"]:
                    writer.writerow([row["R_m"], scenario["scenario"], item, scenario[item]])
    print(json.dumps({
        "conditional_tolerances_mm": [
            {"R": row["R_m"], "SF1": row["tolerances"][0]["cure_debited_amplitude_mm"],
             "SF105": row["tolerances"][1]["cure_debited_amplitude_mm"]}
            for row in scaling
        ],
        "cost_ranges_USD": [
            {"R": row["R_m"], "low": row["scenario_range"][0]["total_USD"],
             "high": row["scenario_range"][1]["total_USD"]}
            for row in cost_rows
        ],
        "ISA_concept_payload_kg": [
            {"R": row["R_m"], "payload": row["payload_with_concept_MGA_kg"]}
            for row in mass_rows if row["weather"] == "ISA"
        ],
    }, indent=2))


if __name__ == "__main__":
    calculate()
