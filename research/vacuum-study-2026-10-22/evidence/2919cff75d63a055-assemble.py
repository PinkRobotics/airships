"""Validate and package the MAINLINE-025 research outputs.

Run after research/model.py, supplement.py and allowable.py. This does not file a report,
contact anyone, fetch sources or alter the inherited input artifacts.
"""

import ast
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT / name).read_text())


def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}


def assert_close(name, observed, expected, checks, rel=1e-10, absolute=1e-9):
    passed = math.isclose(observed, expected, rel_tol=rel, abs_tol=absolute)
    checks.append({
        "name": name, "observed": observed, "expected": expected,
        "relative_tolerance": rel, "absolute_tolerance": absolute, "passed": passed,
    })
    if not passed:
        raise ValueError(checks[-1])


def assemble():
    inputs = read("INPUTS.json")
    start = read("START.json")
    model = read("research/model-results.json")
    supplement = read("SUPPLEMENT.json")
    reliability = read("research/reliability.json")
    manufacturing = read("research/manufacturing.json")
    allowable = read("ALLOWABLE-DEMANDS.json")
    nfi = read("NFI.json")
    checks = []

    for expected in inputs["pins"]:
        measured = pin(expected["path"])
        if measured["sha256"] != expected["sha256"] or measured["bytes"] != expected["bytes"]:
            raise ValueError(f"Source pin changed: {expected['path']}")
    checks.append({
        "name": "all inherited and amendment artifact SHA256/byte pins",
        "count": len(inputs["pins"]), "passed": True,
    })
    for filename in ("research/model.py", "supplement.py", "allowable.py", "assemble.py"):
        ast.parse((ROOT / filename).read_text(), filename=filename)
    checks.append({"name": "four delivered Python programs parse", "passed": True})

    if not all(row["passed"] for row in model["verification"]):
        raise ValueError("A numerical model check failed")
    checks.append({
        "name": "recorded numerical model checks",
        "count": len(model["verification"]), "passed": True,
    })
    if not all(row["passed"] for row in allowable["verification"]):
        raise ValueError("A size/demand interface check failed")
    checks.append({
        "name": "recorded standalone size/demand interface checks",
        "count": len(allowable["verification"]), "passed": True,
    })
    baseline = model["baseline_exact_point"]
    parent_geometry = supplement["baseline_geometry"]
    assert_close("independent mean compression", parent_geometry["inherited_axial_stress_Pa"],
                 baseline["mean_compression_Pa"], checks, absolute=.001)
    assert_close("independent total mass", parent_geometry["closed_mass_kg"],
                 baseline["total_kg"], checks, absolute=1e-7)
    assert_close("independent exact annulus inertia", parent_geometry["I_m4"],
                 baseline["I_m4"], checks, absolute=1e-16)
    assert_close("independent original end force", parent_geometry["inherited_axial_force_N"],
                 baseline["full_pressure"]["N_N"], checks, absolute=1e-6)
    for branch, full in (
        ("legacy_pRs_over2", baseline["full_pressure"]),
        ("equilateral_equilibrium", model["equilateral_force_fixed"][0]["full_pressure"]),
    ):
        demand = allowable["two_demands"][branch]
        for key in ("N_N", "mean_compression_Pa", "maximum_compression_Pa"):
            assert_close("independent interface " + branch + " " + key,
                         demand[key], full[key], checks, absolute=.001)
        if demand["qualified_compression_allowable_Pa"] is not None:
            raise ValueError("Interface invented a qualified compression allowable")
    assert_close(
        "independent array material volume",
        allowable["geometry"]["total_volume_m3"],
        baseline["size_stress_interface"]["total_tube_material_volume_m3"],
        checks, absolute=1e-12,
    )

    for scenario in reliability["illustrative_scenarios"]:
        for point in scenario["results"]:
            sigma = point["illustrative_tensile_threshold_mpa"]
            characteristic = scenario["coupon_characteristic_mpa_derived"]
            hazard = scenario["assembly_to_reference_size_ratio"] * (sigma / characteristic)**scenario["m"]
            probability = -math.expm1(-hazard)
            assert_close(
                "tensile illustration inversion " + scenario["id"],
                probability, point["assembly_failure_probability_target"], checks,
                rel=1e-10, absolute=1e-15,
            )

    ids = [row["id"] for row in nfi["rows"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate NFI ids")
    if reliability["design_allowable_established"] or reliability["compression_failure_probability_established"]:
        raise ValueError("Unjustified allowable or compression reliability claim")
    checks.append({"name": "explicit unknown compression allowable and unique NFI ids", "passed": True})

    inputs["geometry_bounds"]["r_o_additional_cap"] = "s/3, inherited from 011b"
    inputs["source_catalogues"] = {
        "reliability": reliability["sources"],
        "manufacturing": manufacturing["sources"],
        "local_buckling": [{
            "id": "NASA_SP8007_REV2",
            "url": model["source_references"]["SP8007"],
            "title": "NASA SP-8007 Rev.2, Buckling of Thin-Walled Circular Cylinders",
            "locator": "printed pp.23–25, Eqs.9–10 and length-range caution",
            "retrieved_on": "2026-10-20",
            "scope": "QUESTIONABLE transfer to long curved ceramic and CMC struts",
        }],
    }
    inputs["external_sources"] = list({
        source["url"] for catalogue in inputs["source_catalogues"].values()
        for source in catalogue if isinstance(source.get("url"), str)
    })
    inputs["external_sources"].sort()
    inputs["material_datasets"] = reliability["material_datasets"]
    inputs["CMC_measured_sets"] = manufacturing["cmc_measured_property_sets"]
    inputs["CMC_screening"] = manufacturing["scalar_screening_surrogate"]
    inputs["computational_assumptions"] = {
        "status": "QUESTIONABLE / PROJECTION",
        "SiC_Fc_assumed_Pa": [100e6, 200e6, 380e6, 1000e6, 3900e6],
        "CMC_Fc_assumed_Pa": [128e6, 300e6, 580e6],
        "CMC_Ft_assumed_Pa": 128e6,
        "local_gamma_sensitivities": [.3, .5, .7, 1, "NASA SP-8007 axial curve"],
        "global_k": .2,
        "local_stress_coefficient": .6,
        "force_factors": [1, 1 / math.sqrt(3)],
        "force_factor_scope": "amendment-corrected equilateral equilibrium and inherited two-way comparison, both fully scored",
        "equilibrium_amendment": inputs["amendment_order"],
        "film_sag_lift_charge": "not included; pinned note assigns changed film geometry and lift accounting to MAINLINE-024/022b",
        "qualified_compression_size_law": None,
        "tensile_size_interface": "allowable.py and ALLOWABLE-INTERFACE.md; supplied calibration hypotheses are PROJECTION",
        "contact_model": "unknown; hypothetical sigma_t=Ct*N/A",
        "assumed_bend_spans_m": [.040, .020],
        "assumed_380MPa_mean": True,
        "target_exposure": inputs["reliability_target"]["exposure"],
        "film_strength_Pa": 1.5e9,
        "film_wall_m": 80e-6,
        "film_property_source": "inherited 011b; no qualifying datasheet supplied",
        "borrowed_wall_constraints_m": [.002, .004],
        "borrowed_wall_scope": "SiSiC catalogue geometric sensitivities; not SA product limits",
    }
    inputs["own_evidence_pins"] = [
        pin(ROOT / filename) for filename in (
            "research/model.py", "research/model-results.json", "research/model-notes.md",
            "research/reliability.json", "research/reliability.md",
            "research/manufacturing.json", "research/manufacturing.md",
            "supplement.py", "SUPPLEMENT.json",
            "allowable.py", "ALLOWABLE-DEMANDS.json", "ALLOWABLE-INTERFACE.md",
            "assemble.py",
        )
    ]
    (ROOT / "INPUTS.json").write_text(json.dumps(inputs, indent=2, allow_nan=False) + "\n")

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    assemble()
