"""Owner bookkeeping audit, not an independent physical or model validation."""
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import csv
import hashlib
import json
import math

BASE = Path(__file__).resolve().parent


def load(name, **kwargs):
    return json.loads((BASE / name).read_text(), **kwargs)


def main():
    checks = []
    inputs = load("INPUTS.json")
    r = load("RESULTS.json")
    rd = load("RESULTS.json", parse_float=Decimal, parse_int=Decimal)
    cfg = load("ASSUMPTIONS.json")
    inherited_nonstandard_literals = []
    for p in BASE.rglob("*.json"):
        try:
            json.loads(p.read_text(), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
        except ValueError as exc:
            if not p.is_relative_to(BASE / "inputs"):
                raise
            json.loads(p.read_text())
            inherited_nonstandard_literals.append({
                "path": str(p.relative_to(BASE)), "nonstandard_literal": str(exc),
                "disposition": "Pinned incoming file preserved verbatim. New results and selected numeric bills contain only finite numbers.",
            })
    checks.append({"check": "strict JSON syntax and finite numeric literals in new outputs",
                   "status": "pass", "inherited_input_exceptions": inherited_nonstandard_literals})

    pins = inputs["brief_and_dependency_pins"] + inputs["primary_source_pins"]
    for item in pins:
        path = Path(item.get("owned_copy", item["path"]))
        data = path.read_bytes()
        assert len(data) == item["bytes"], path
        assert hashlib.sha256(data).hexdigest() == item["sha256"], path
    for name in ["assumptions", "calculation"]:
        p = inputs[name]
        data = Path(p["path"]).read_bytes()
        assert len(data) == p["bytes"]
        assert hashlib.sha256(data).hexdigest() == p["sha256"]
    checks.append({"check": "owned input/source byte pins", "status": "pass", "count": len(pins) + 2})

    mass_errors = []
    mass_csv = defaultdict(dict)
    with (BASE / "MASS-BILL.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            mass_csv[(int(row["R_m"]), row["weather"])][row["item"]] = Decimal(row["kg"])
    for row in rd["whole_mass_bills"]:
        total = sum(row["whole_bill_before_MGA_kg"].values())
        total += row["baseline_concept_MGA_kg"] + row["shape_MGA_added_kg"]
        error = row["lift_reference_kg"] - total - row["payload_with_concept_MGA_kg"]
        mass_errors.append(abs(error))
        assert abs(error) < Decimal("0.00000001")
        table = mass_csv[(int(row["R_m"]), row["weather"])]
        assert table["payload_with_concept_MGA"] == row["payload_with_concept_MGA_kg"]
        for item, value in row["whole_bill_before_MGA_kg"].items():
            assert table[item] == value
        assert row["payload_with_concept_MGA_kg"] < 0
    checks.append({
        "check": "six full mass accounts, CSV agreement and concept payload sign",
        "status": "pass", "cases": len(mass_errors),
        "maximum_decimal_closure_error_kg": str(max(mass_errors)),
    })

    growth = load("inputs/057/mga057.json")
    isa = [x for x in r["whole_mass_bills"] if x["weather"] == "ISA"]
    geom = []
    for s, m in zip(r["scaling"], isa):
        rec = next(x for x in growth["P2_records"] if x["id"] == s["source_case"])
        src = next(x for x in rec["masks"] if x["mask"] == 15)
        assert not rec["floor"] and rec["weather"] == "ISA"
        assert src["bill"] == m["baseline_bill_kg"]
        assert rec["source"] == ("048" if s["R_m"] == 10 else "040 with 048 finish transfer")
        area = 4 * math.pi * s["R_m"]**2
        assert math.isclose(2*area*s["tf_each_mm"]/1000*1850, src["bill"]["faces"], rel_tol=1e-12)
        assert math.isclose(area*s["tc_mm"]/1000*cfg["core_density_kg_m3"], src["bill"]["core"], rel_tol=1e-12)
        assert math.isclose(sum(s["shape_budget_mm"].values()), s["conditional_shop_cap_mm"])
        assert s["conditional_shop_cap_mm"] < s["tolerances"][1]["cure_debited_amplitude_mm"]
        raw = s["face_blanks_total"]*cfg["blank_width_m"]*cfg["blank_length_m"]*s["tf_each_mm"]/1000*1850
        assert math.isclose(raw, s["rectangular_blank_stock_before_process_loss_kg"], rel_tol=1e-12)
        assert raw >= src["bill"]["faces"]
        for t in s["tolerances"]:
            assert math.isclose(t["cure_debited_amplitude_mm"], t["ratio_form_reproduction_mm"], rel_tol=1e-12)
        geom.append({"R_m": s["R_m"], "source": rec["source"], "mask": 15,
                     "rectangular_blank_stock_kg": raw,
                     "net_geometric_yield": src["bill"]["faces"]/raw})
    checks.append({"check": "source selection, geometry reconstruction, shape sums, ratio identity and stock minimum",
                   "status": "pass", "cases": geom})

    cost_csv = defaultdict(dict)
    with (BASE / "COST-BILL.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            cost_csv[(int(row["R_m"]), row["scenario"])][row["item"]] = Decimal(row["USD_2026_planning"])
    cost_errors = []
    for row, s in zip(rd["whole_cost_bills"], r["scaling"]):
        for scenario in row["scenario_range"]:
            rates = cfg["cost_rates"][scenario["scenario"]]
            subtotal = sum(scenario["items_USD"].values())
            error = subtotal + scenario["cost_contingency_USD"] - scenario["total_USD"]
            cost_errors.append(abs(error))
            assert abs(error) < Decimal("0.00001")
            assert abs(subtotal - scenario["subtotal_USD"]) < Decimal("0.00001")
            expected_contingency = subtotal * Decimal(str(rates["cost_contingency_fraction"]))
            assert abs(expected_contingency - scenario["cost_contingency_USD"]) < Decimal("0.00001")
            assert float(scenario["purchased_Be_kg"]) >= s["rectangular_blank_stock_before_process_loss_kg"]
            expected_stock = s["rectangular_blank_stock_before_process_loss_kg"] / rates["purchased_stock_yield"]
            assert math.isclose(float(scenario["purchased_Be_kg"]), expected_stock, rel_tol=1e-12)
            table = cost_csv[(int(row["R_m"]), scenario["scenario"])]
            for item, value in scenario["items_USD"].items():
                assert table[item] == value
            assert table["total_USD"] == scenario["total_USD"]
        assert row["scenario_range"][0]["total_USD"] < row["scenario_range"][1]["total_USD"]
    checks.append({"check": "six cost sums, contingency, full-blank purchase takeoff and CSV agreement",
                   "status": "pass", "maximum_decimal_closure_error_USD": str(max(cost_errors))})

    precedents = load("PRECEDENTS.json")["records"]
    assert len(precedents) == 7
    assert all(x["largest_local_dimple_mm"] is None for x in precedents)
    assert next(x for x in precedents if x["id"] == "P062-STRETCH")["demonstrated_size_in_requested_range"] is False
    for row in precedents:
        for src in row["sources"]:
            p = BASE / src["local_path"]
            assert hashlib.sha256(p.read_bytes()).hexdigest() == src["sha256"]
    nfi = load("NFI.json")
    assert len(nfi["issues"]) == 16 and all(x["status"] == "open" for x in nfi["issues"])
    assert r["FE_runs_performed"] == 0 and r["parameter_optimization_performed"] is False
    checks.append({"check": "precedent source links, explicit unknowns, 16 open NFIs and no new FE claim", "status": "pass"})

    value = {
        "unit": r["unit"], "tag": "QUESTIONABLE / PROJECTION",
        "owner_bookkeeping_status": "pass",
        "external_independent_review": "pending REVIEW-A",
        "physical_qualification": "open",
        "measured_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "limits": "These arithmetic/pin checks do not validate the fixed-C scaling, material laws, fabrication capability, quoted costs or flight feasibility.",
    }
    (BASE / "VERIFICATION.json").write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"owner_bookkeeping_status": "pass", "checks": len(checks), "pins": len(pins)+2}))


if __name__ == "__main__":
    main()
