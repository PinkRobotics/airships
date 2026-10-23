"""Write the evidence index and presentation for the fixed-case 062 calculation."""
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent


def read(name):
    return json.loads((BASE / name).read_text())


def save(name, value):
    (BASE / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def pin(path):
    path = Path(path)
    content = path.read_bytes()
    return {"path": str(path), "sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}


def main():
    r = read("RESULTS.json")
    cfg = read("ASSUMPTIONS.json")
    access = read("sources/ACCESS.json") + read("sources/ACCESS-2.json")
    source_by_name = {x["file"]: x for x in access}

    def source(name, pages):
        row = source_by_name[name]
        return {
            "url": row["url"], "local_path": "sources/" + name,
            "locator": pages, "sha256": row["sha256"], "bytes": row["bytes"],
        }

    precedents = [
        {
            "id": "P062-ALMA", "category": "adjustable radio reflector",
            "build": "ALMA 12 m AEC and VertexRSI prototypes",
            "diameter_m": 12, "demonstrated_size_in_requested_range": True,
            "RMS_mm": {"AEC_summary": 0.017, "Vertex_summary": 0.016,
                       "summary_uncertainty": 0.005, "AEC_best_faulty_panel_excluded": 0.014},
            "accuracy_scope": "Holographically adjusted reflector; the best AEC figure excludes a faulty panel. No conversion to a maximum defect or full unmasked acceptance.",
            "largest_local_dimple_mm": None,
            "local_dimple_span_m": None,
            "missing_metric_reason": "No largest inward dimple with its spatial span established from this record.",
            "mechanism": "AEC: 120 nickel-skin aluminum-honeycomb panels, five adjusters each; Vertex: 264 machined aluminum panels, eight adjusters. Ground-supported backup structures.",
            "areal_mass_kg_m2": {
                "AEC_whole_antenna": r["ALMA_AEC_total_system_kg_per_projected_m2"],
                "Vertex_whole_antenna": r["ALMA_Vertex_total_system_kg_per_projected_m2"],
            },
            "mass_basis": "80 t and 108 t whole antennas divided by pi*6^2 projected m2; panel-only mass not established.",
            "cost_per_m2": r["ALMA_reference_cost_USD2000_per_projected_m2"],
            "cost_currency_year": "USD, year 2000",
            "cost_basis": "NSF 2006 review: 137M USD2000, no contingency, for 25 North American antennas. Whole-antenna procurement, not the AEC prototype or a panel quote.",
            "transfer": "Transfers panel metrology and adjustable assembly methods. Accuracy relies on support; does not show that an unsupported bonded Be pressure sphere keeps the shape.",
            "sources": [source("alma-prototypes.pdf", "PDF pp.6, 8, 12, 14"),
                        source("alma-cost-review.pdf", "PDF pp.15, 20")],
        },
        {
            "id": "P062-GBT", "category": "active radio reflector",
            "build": "Green Bank Telescope",
            "diameter_m": 100, "physical_aperture_axes_m": [100, 110],
            "demonstrated_size_in_requested_range": "100 m effective diameter; one physical axis is 110 m",
            "RMS_mm": 0.220,
            "accuracy_scope": "Ruze-equivalent surface RMS inferred from measured efficiency; not a bound on each local defect.",
            "largest_local_dimple_mm": None, "local_dimple_span_m": None,
            "missing_metric_reason": "No maximum inward deviation and corresponding span established.",
            "mechanism": "2004 panels with active surface on a large ground-supported moving structure.",
            "areal_mass_kg_m2": r["GBT_whole_system_kg_per_projected_m2"],
            "mass_basis": "7.7 million kg moving structure divided by 7854 projected m2; not reflector skin mass.",
            "cost_per_m2": None, "cost_currency_year": None,
            "cost_basis": "A comparable primary-source procurement breakdown was not established in the inspected sources; unknown, not zero.",
            "transfer": "Transfers active measurement/correction concepts. Directly carrying the supporting structure is incompatible with the inherited flight bill. Passive retention after removal is unproved.",
            "sources": [source("gbt-performance.html", "Surface accuracy and aperture efficiency sections"),
                        source("gbt-facts.pdf", "Telescope specifications")],
        },
        {
            "id": "P062-SII", "category": "launch-vehicle sandwich dome",
            "build": "Saturn S-II common bulkhead",
            "diameter_m": 10.06, "demonstrated_size_in_requested_range": True,
            "RMS_mm": None, "largest_local_dimple_mm": None,
            "local_dimple_span_m": None,
            "other_accuracy_mm": {"core_to_face_fit": 0.254},
            "accuracy_scope": "0.010 inch fit of machined core to face sheets; not a global contour RMS or an external-surface local-dimple maximum.",
            "missing_metric_reason": "No admissible conversion from bond fit to a free-standing shell shape bound.",
            "mechanism": "Matched core profiling and bonded dome assembly.",
            "areal_mass_kg_m2": None, "mass_basis": "Matched complete bulkhead mass and area not established from the inspected passage.",
            "cost_per_m2": None, "cost_currency_year": None,
            "cost_basis": "No matched production cost established.",
            "transfer": "Useful manufacturing fit precedent, but its material, bond, thermal history, supports and loads differ. The 042 gamma 0.21–0.22 belongs to a separate hemisphere evidence chain, not automatically this flight bulkhead.",
            "sources": [source("sii-lessons.pdf", "PDF p.296, printed p.4-45")],
        },
        {
            "id": "P062-SPIN", "category": "spun dome",
            "build": "NASA spun aluminum/FSW production examples and Orion dome fabrication",
            "diameter_m": 5.5, "demonstrated_size_in_requested_range": True,
            "RMS_mm": None, "largest_local_dimple_mm": None,
            "local_dimple_span_m": None,
            "accuracy_scope": "2012 presentation identifies applications up to 5.5 m. The separate 2016 fabrication record reports template/profile inspection without a numerical RMS or local-dimple bound.",
            "missing_metric_reason": "No sourced 0.1–5 mm maximum deviation proved for the 5.5 m example. Separate records are not one measured article.",
            "mechanism": "Spinning/stretching and friction-stir welded aluminum blanks, followed by contour inspection.",
            "areal_mass_kg_m2": None, "mass_basis": "Matched finished mass/area not established.",
            "cost_per_m2": None, "cost_currency_year": None,
            "cost_basis": "Matched production price not established.",
            "transfer": "Supports large-dome forming capability only. Aluminum forming performance does not establish Be sheet ductility, springback, gauge loss or sandwich cure shape.",
            "sources": [source("spin-2012.pdf", "PDF p.23"),
                        source("spin-2016.pdf", "PDF pp.32, 36")],
        },
        {
            "id": "P062-STRETCH", "category": "stretch-formed dome, scale exclusion",
            "build": "NASA 1974 gore development for an 8.387 m dome",
            "diameter_m": 3.048, "target_full_scale_diameter_m": 8.387,
            "demonstrated_size_in_requested_range": False,
            "RMS_mm": None, "largest_local_dimple_mm": None,
            "local_dimple_span_m": None,
            "other_accuracy_mm": {"trimmed_gore_A_base_die_gap": 12.7,
                                  "trimmed_gore_A_nose_die_gap": 0.7874},
            "accuracy_scope": "A 36.3%-scale test article, not a demonstrated 8.387 m shell. Reported local die-fit gaps are not surface RMS or inward-dimple bounds.",
            "missing_metric_reason": "This test is below the requested 5 m lower bound and does not establish full-size retained shape.",
            "mechanism": "Stretch-forming dome gores, trimming and die-fit assessment.",
            "areal_mass_kg_m2": None, "mass_basis": "Comparable full-size finished hull mass not established.",
            "cost_per_m2": None, "cost_currency_year": None,
            "cost_basis": "The study includes a production cost analysis, but no directly comparable qualified finished sphere cost is extracted; this field remains unknown.",
            "transfer": "Shows springback and trimming must be measured. It cannot justify a blanket 1–5 mm full-size dome claim.",
            "sources": [source("stretch-1974.pdf", "PDF pp.11, 22; printed p.2-15 for die-fit results")],
        },
        {
            "id": "P062-WEBB", "category": "segmented beryllium mirror",
            "build": "JWST 6.5 m primary, 18 segments",
            "diameter_m": 6.5, "segment_flat_to_flat_m": 1.32,
            "demonstrated_size_in_requested_range": True,
            "RMS_mm": 0.000020,
            "accuracy_scope": "20 nm RMS cryogenic segment figure, not a whole-hull geometric RMS or local-dimple bound. This is far better than 0.1 mm but under a different metric and support arrangement.",
            "largest_local_dimple_mm": None, "local_dimple_span_m": None,
            "missing_metric_reason": "No applicable maximum pressure-hull defect/span reported.",
            "mechanism": "Lightweighted Be mirror bodies with segment positioning and curvature control.",
            "areal_mass_kg_m2": r["Webb_mirror_only_kg_per_unobscured_collecting_m2"],
            "mass_basis": "18*20 kg mirror bodies / 25 m2 unobscured collecting area; excludes actuators and backplane.",
            "cost_per_m2": None, "cost_currency_year": None,
            "cost_basis": "Mirror fabrication cost not established. Total mission budget is not treated as a mirror price.",
            "transfer": "Shows precision Be metrology and fabrication. Ribbed mirror bodies differ from SR-200 bonded thin faces, and the uncharged supports/control do not disappear on transfer.",
            "sources": [source("webb-mission.pdf", "PDF p.4"),
                        source("webb-media.pdf", "Mirror segment specifications"),
                        source("webb-mirrors.html", "Primary mirror and segment descriptions")],
        },
        {
            "id": "P062-KECK", "category": "segmented optical mirror",
            "build": "Keck 10 m, 36 primary segments",
            "diameter_m": 10, "segment_span_m": 1.8,
            "demonstrated_size_in_requested_range": True,
            "RMS_mm": None, "largest_local_dimple_mm": None, "local_dimple_span_m": None,
            "accuracy_scope": "The inspected operator record supplies segmentation and mass, not a suitable complete contour RMS/local-dimple pair. Relative alignment precision is not substituted for surface RMS.",
            "missing_metric_reason": "No applicable maximum defect/span established.",
            "mechanism": "Actively aligned segments on a ground-supported telescope.",
            "areal_mass_kg_m2": r["Keck_mirror_segments_kg_per_nominal_aperture_m2"],
            "mass_basis": "36*400 kg / (pi*5^2) nominal aperture area; segments only, excluding the supporting telescope.",
            "cost_per_m2": None, "cost_currency_year": None,
            "cost_basis": "Foundation gifts in the annual report are funding amounts, not a segmented-mirror procurement breakdown; no price/m2 inferred.",
            "transfer": "Transfers segment measurement/alignment practice. Direct mass and continuous pressure-boundary requirements rule out simple copying.",
            "sources": [source("keck-mirrors.html", "Segment count, size and mass"),
                        source("keck-report2012.pdf", "PDF p.14, founding gifts")],
        },
    ]
    for row in precedents:
        row["assessment_tag"] = "QUESTIONABLE transfer / PROJECTION application"
        row["null_policy"] = "Unknown or not established in the inspected record; never zero."
    save("PRECEDENTS.json", {"unit": r["unit"], "tag": r["status"], "records": precedents})

    nfi_specs = [
        ("face-compression", "critical", "345 MPa is a tensile proxy; processed thin-sheet compression is unqualified.",
         "Obtain L/LT/off-axis and biaxial compression at finished gauges, lots, forming/cure histories and service temperatures.", ["036", "047"], "ADMISSIBILITY.md"),
        ("sheet-procurement", "critical", "R10 24x72 inch blank plan conflicts with the maker's smaller thin-sheet size class; all sizes lack a quote.",
         "Supplier to confirm actual usable blanks, finished minimum gauge, forming/etch yield and deliveries; rebill seam length and hardware.", ["036", "057", "SR-200 datasheet"], "BUILD-ROUTE.md"),
        ("core-elastic", "high", "E1/E2/G12 and Poisson couplings are not matched CR III data.",
         "Measure directional elastic response or validate a reciprocal homogenized tensor against coupon data.", ["056", "047", "Hexcel Table II"], "ADMISSIBILITY.md"),
        ("core-nonlinear", "critical", "Peak/crush scalars do not provide peak-to-densification, unloading, mixed loading or damage laws.",
         "Supply CR III normal/shear cycles and mixed tests at actual thickness, ribbon direction, venting and bonded/cured condition.", ["056"], "FE-NEXT.md"),
        ("processed-bond", "critical", "2U light-film identity is sourced, but proposed Be/CR III bond behavior after the selected cure is not.",
         "Qualify exact surfaces, primer, carrier/weight, cure and defects with flatwise, shear, peel and mixed-mode tests and aging.", ["037b", "3M guide"], "ADMISSIBILITY.md"),
        ("cure-state", "critical", "Scalar cure stress debit is not a measured residual stress/shape state.",
         "Measure cure locking and relaxation, temperature histories and strain/shape before and after release; carry the state into FE.", ["037b", "047"], "FE-NEXT.md"),
        ("scarf-closure", "critical", "30.3414:1 overlap and room-temperature closure lack processed Be seam proof.",
         "Build panel-pair and curved closure specimens, demonstrate strength, peel resistance, sealing, distortion and inspected defect limits.", ["037b", "042", "057"], "BUILD-ROUTE.md"),
        ("scaled-C", "high", "Holding calibrated C across the changed 057 face/core ratios and shear compliance is unvalidated.",
         "After material release, predict measured articles and compare fixed scaled cases with identical nondimensional defect definitions.", ["047", "CHECK047", "CHECK055", "057"], "METHOD.md"),
        ("defect-spectrum", "critical", "One Gaussian and telescope RMS do not bound local dents, seams, wrinkles or interacting defects.",
         "Measure full-field shape with inward peak/span and spectral bands, seam maps and gauge; establish pressure response for the measured field.", ["042", "047"], "BUILD-ROUTE.md"),
        ("passive-retention", "critical", "No demonstrated free-standing Be sandwich sphere keeps the proposed shape after jig removal, thermal cycling and evacuation.",
         "Validate panel, joined-sector and closed-shell release/cycle tests without uncharged distributed supports or active correction.", ["042", "062 route"], "BUILD-ROUTE.md"),
        ("retained-shape-mass", "high", "0.020 kg/m2 for targets/shims/filler and no flight frame are unverified allowances.",
         "Weigh as-built items, count seal/repair material and any retained adjusters/back structure; retain or increase applicable mass growth.", ["057", "062 assumptions"], "BUILD-ROUTE.md"),
        ("MGA-float", "critical", "All six selected mass accounts remain negative with inherited concept growth.",
         "Close measured hardware/process masses and justified maturity-specific growth before making a payload or flight-feasibility claim; no silent 5% substitution.", ["057", "062 mass bills"], "CARD.md"),
        ("pricing-capacity", "high", "All route prices are unquoted assumptions; cheapest achievable route and supplier capacity are unproved.",
         "Obtain competitive stock, forming, machining, bond, metrology, facilities and scrap/yield quotations at the stated quantities.", ["042", "062 assumptions"], "BUILD-ROUTE.md"),
        ("qualification-total", "high", "Full-scale destructive qualification/replacement hull, land, financing, taxes and operation are not priced.",
         "Define the required program and article count, price these unknown costs, and add them to any procurement total.", ["062 assumptions"], "BUILD-ROUTE.md"),
        ("precedent-metrics", "medium", "Published RMS, bond fit and relative alignment usually omit the largest local dimple and its span.",
         "Obtain unmasked spatial maps and scope-matched mass and cost records if using a precedent as a quantitative hull acceptance claim.", ["042", "062 primary sources"], "PRECEDENTS.md"),
        ("external-review", "high", "REVIEW-A has not been performed as part of this card.",
         "Include these pinned claims in the brief's piece review after filing. No new seat contact, checker or follow-on work is initiated here.", ["PROCESS-v2"], "REVIEW.md"),
    ]
    issues = [
        {"id": f"NFI-062-{i:02d}", "key": key, "status": "open",
         "tag": "QUESTIONABLE / PROJECTION", "severity": severity,
         "issue": issue, "closure_evidence": closure, "inputs": inp, "detail": detail}
        for i, (key, severity, issue, closure, inp, detail) in enumerate(nfi_specs, 1)
    ]
    save("NFI.json", {
        "unit": r["unit"], "status": r["status"],
        "work_completion_is_not_physical_qualification": True, "issues": issues,
        "limited_source_clarifications": [
            {"claim": "290 GPa appears in the current SR-200 sheet datasheet",
             "effect": "Resolves blanket unsourced-scalar wording only; compression and orthotropy remain open."},
            {"claim": "AF 163-2U 0.015 lb/ft2 is a listed product",
             "effect": "No automatic heavy-film substitution; installed weight and processed bond remain open."},
        ],
    })

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    mass_header = "| Item, kg | R10 ISA | R20 ISA | R30 ISA |\n| --- | ---: | ---: | ---: |\n"
    isa = [x for x in r["whole_mass_bills"] if x["weather"] == "ISA"]
    keys = list(dict.fromkeys(k for x in isa for k in x["whole_bill_before_MGA_kg"]))
    mass_table = mass_header + "".join(
        "| " + k + " | " + " | ".join(f'{x["whole_bill_before_MGA_kg"].get(k, 0):,.3f}' for x in isa) + " |\n"
        for k in keys
    )
    mass_table += "| Concept mass-growth allowance | " + " | ".join(
        f'{x["baseline_concept_MGA_kg"] + x["shape_MGA_added_kg"]:,.3f}' for x in isa
    ) + " |\n"
    for label, key in [
        ("Whole charged account including growth", "whole_concept_account_total_kg"),
        ("Reference displaced-air lift", "lift_reference_kg"),
        ("Residual payload with concept growth", "payload_with_concept_MGA_kg"),
    ]:
        mass_table += "| " + label + " | " + " | ".join(f"{x[key]:,.3f}" for x in isa) + " |\n"
    (BASE / "MASS-TABLE.md").write_text(
        "# MAINLINE062 whole mass account\n\n**QUESTIONABLE / PROJECTION.** "
        "ISA cases shown; all six weather accounts are in `MASS-BILL.csv` and `RESULTS.json`. "
        "Zeros retain the inherited endpoint assumptions. Weather headroom, when nonzero, is a lift debit.\n\n"
        + mass_table
    )

    cost_table = "| Cost line, million 2026 USD (low–high) | R10 | R20 | R30 |\n| --- | ---: | ---: | ---: |\n"
    costs = r["whole_cost_bills"]
    for key in costs[0]["scenario_range"][0]["items_USD"]:
        cost_table += "| " + key + " | " + " | ".join(
            f'{x["scenario_range"][0]["items_USD"][key]/1e6:,.3f}–{x["scenario_range"][1]["items_USD"][key]/1e6:,.3f}'
            for x in costs
        ) + " |\n"
    for label, key in [("Subtotal", "subtotal_USD"), ("Cost contingency", "cost_contingency_USD"), ("Total", "total_USD")]:
        cost_table += "| " + label + " | " + " | ".join(
            f'{x["scenario_range"][0][key]/1e6:,.3f}–{x["scenario_range"][1][key]/1e6:,.3f}'
            for x in costs
        ) + " |\n"
    (BASE / "COST-TABLE.md").write_text(
        "# MAINLINE062 cost account\n\n**PROJECTION: every rate is an unquoted planning assumption.** "
        "Ranges are paired low/high scenarios, not a confidence interval. Rates and quantities are explicit "
        "in `ASSUMPTIONS.json`, `RESULTS.json` and `COST-BILL.csv`.\n\n" + cost_table
        + "\n" + cfg["cost_scope"] + "\n"
    )


if __name__ == "__main__":
    main()
