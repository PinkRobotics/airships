"""Compare unchanged witnesses, resized points and least sets; audit closure."""
from pathlib import Path
from dataclasses import replace
import csv
import json
import numpy as np
from account53 import ROOT, Account, CORE, KB, DA, SCARF, NU, parameters, save
from thermal53 import MODELS, evaluate

models = ["owner_table", "forced_conduction", "mixed_conduction", "forced_gap", "mixed_gap"]
accounts = {m: json.loads((ROOT/("ACCOUNT-"+m+".json")).read_text()) for m in models}
settled_tables = json.loads((ROOT/"SETTLED-THERMAL-TABLES.json").read_text())
owner_tables = json.loads((ROOT/"inputs/048/THERMAL-TABLES.json").read_text())["MLCCAg"]
route_map = {"dry_gas": "dry_gas", "bake70": "bake", "desiccant": "sorbent"}


def key(row):
    return tuple(row[k] for k in ["R_m", "weather", "cure_in_global", "floor", "drying"])


indexed = {model: {key(row): row for row in rows} for model, rows in accounts.items()}
filed = {}
for folder, cure in [("048", False), ("048fold", True)]:
    for row in csv.DictReader((ROOT/"inputs"/folder/"ROWS.csv").open()):
        if (row["profile"] != "MLCCAg" or row["weather"] not in ["ISA", "optimistic"]
                or abs(float(row["external_water_kg_m2"])-.1) > 1e-12):
            continue
        if cure and row["cure_in_global"] != "True":
            continue
        k = (int(row["R_m"]), row["weather"], cure, row["floor"] == "True", route_map[row["drying"]])
        filed[k] = row
assert len(filed) == 72, len(filed)

baseline_comparisons = []
fixed = []
differences = []
flips = []
least_changes = []
validation = []


def check(name, good, **values):
    validation.append(dict(check=name, passed=bool(good), **values))


for k, row in indexed["owner_table"].items():
    old = row["result"]["endpoints"][11]
    source = filed[k]
    expected = float(source["endpoint_payload_kg"])
    baseline_comparisons.append(dict(case=list(k), owner=expected, independent=old["payload_kg"],
                                    difference=old["payload_kg"]-expected))
    check("original endpoint reproduction", abs(old["payload_kg"]-expected) < .005,
          case=list(k), difference_kg=old["payload_kg"]-expected)
    raw_tf = float(source["tf_mm" if k[2] else "endpoint_tf_mm"])/1000
    raw_tc = float(source["tc_mm" if k[2] else "endpoint_tc_mm"])/1000
    original_account = Account(owner_tables[str(k[0])], k[0], k[1], k[2])
    frozen_original = original_account.bill(np.array([raw_tf]), np.array([raw_tc]),
                                            11, 1., k[3], k[4], True)
    for model in models[1:]:
        modified = indexed[model][k]
        point = modified["result"]["endpoints"][11]
        account = Account(settled_tables[model]["MLCCAg"][str(k[0])], k[0], k[1], k[2])
        frozen = account.bill(np.array([raw_tf]), np.array([raw_tc]), 11, 1., k[3], k[4], True)
        crossed = [name for name, sf in frozen["modes"].items()
                   if frozen_original["modes"][name] >= 1-2e-7 and sf < 1-2e-7]
        fixed.append(dict(model=model, case=list(k), original=frozen_original,
                          revised=frozen, newly_failed_screens=crossed))
        chosen = modified["result"]["chosen"]
        previous = row["result"]["chosen"]
        differences.append(dict(model=model, case=list(k),
                                old_payload_kg=old["payload_kg"], new_payload_kg=point["payload_kg"],
                                payload_difference_kg=point["payload_kg"]-old["payload_kg"],
                                added_face_thickness_m=point["tf_m"]-old["tf_m"],
                                core_thickness_difference_m=point["tc_m"]-old["tc_m"],
                                old_cure_compression_Pa=old["properties"]["cure_compression_Pa"],
                                new_cure_compression_Pa=point["properties"]["cure_compression_Pa"],
                                old_edge_usage=1/old["modes"]["core_edge"],
                                new_edge_usage=1/point["modes"]["core_edge"],
                                new_wall_usage=1/point["modes"]["cell_wall"],
                                new_scarf_usage=1/point["modes"]["scarf"],
                                old_least_mask=previous["mask"] if previous else None,
                                new_least_mask=chosen["mask"] if chosen else None,
                                old_least_usage=previous["usage"] if previous else None,
                                new_least_usage=chosen["usage"] if chosen else None,
                                usage_difference=chosen["usage"]-previous["usage"] if previous and chosen else None))
        if (chosen["mask"] if chosen else None) != (previous["mask"] if previous else None):
            least_changes.append(dict(model=model, case=list(k), old=previous, new=chosen))
        for mask, (p, q) in enumerate(zip(row["result"]["endpoints"], modified["result"]["endpoints"])):
            if (p is not None and p["payload_kg"] >= 0) != (q is not None and q["payload_kg"] >= 0):
                flips.append(dict(model=model, case=list(k), mask=mask,
                                  old_payload_kg=p["payload_kg"] if p else None,
                                  new_payload_kg=q["payload_kg"] if q else None))

for model, rows in accounts.items():
    for row in rows:
        points = row["result"]["endpoints"]+row["result"].get("ties", [])
        for point in points:
            if point is None:
                continue
            identity = dict(model=model, case=list(key(row)), mask=point["mask"], usage=point["usage"])
            check("mass conservation", abs(point["lift_kg"]-sum(point["bill_kg"].values())-point["payload_kg"]) < 1e-8,
                  **identity)
            check("all resized scalar screens", min(point["modes"].values()) >= 1-2e-7, **identity,
                  minimum_SF=min(point["modes"].values()))
            check("service pressure", point["service_pressure_SF"] >= 1-2e-7, **identity)
            tf, tc = point["tf_m"], point["tc_m"]
            rho = point["properties"]
            tcold = rho["min_outer_K"]
            force = KB*DA*1.002*max(366.4833333333333-tcold, 0)*tc
            check("balanced cure force across both skins",
                  abs(2*tf*rho["cure_compression_Pa"]-force) < 1e-6, **identity)
            # Independent closed root of the scarf demand quadratic.
            E = rho["E_Pa"]
            pressure_constant = point["pressure_Pa"]*row["R_m"]/4
            g = rho["gradient_stress_Pa"]
            b = rho["pattern_stress_Pa"]/(tf+tc)
            limit = 10e6*(1+SCARF**2)/SCARF
            linear = limit-g-b*tc
            constant = pressure_constant+force/2
            discriminant = linear*linear-4*b*constant
            minimum_face = 2*constant/(linear+np.sqrt(discriminant))
            check("closed-form scarf lower face bound", tf >= minimum_face*(1-1e-9),
                  **identity, minimum_face_m=float(minimum_face), actual_face_m=tf)
        for bound in row["result"]["favorable_bounds"]:
            check("lower-cardinality favorable E bound",
                  bound["favorable_payload_upper_kg"] is None or bound["favorable_payload_upper_kg"] < 0,
                  model=model, case=list(key(row)), **bound)

direct_checks = []
for model, boundary in MODELS.items():
    for radius in [10, 12, 15]:
        selected = [r for r in accounts[model] if r["R_m"] == radius]
        points = [r["result"]["endpoints"][11] for r in selected]
        thickness = [p["tc_m"] for p in points]
        exact = evaluate(radius, thickness, .09, .8, replace(boundary, nodes=512))
        for j, (row, point) in enumerate(zip(selected, points)):
            props = point["properties"]
            kt_guarded = 1.002*props["curvature_temperature_K"]
            grad_guarded = 1.002*props["gradient_K"]
            cold_direct = exact["min_outer_K"][j]
            guarded_cure_drop = 1.002*(366.4833333333333-props["min_outer_K"])
            direct_cure_drop = 366.4833333333333-cold_direct
            good = (kt_guarded >= exact["curvature_temperature_K"][j]-1e-8
                    and grad_guarded >= exact["gradient_K"][j]-1e-8
                    and guarded_cure_drop >= direct_cure_drop-1e-8)
            direct_checks.append(dict(model=model, case=list(key(row)), tc_m=point["tc_m"],
                                       passed=bool(good), guarded_gradient_K=grad_guarded,
                                       direct_gradient_K=exact["gradient_K"][j],
                                       guarded_curvature_K=kt_guarded,
                                       direct_curvature_K=exact["curvature_temperature_K"][j],
                                       guarded_cure_drop_K=guarded_cure_drop,
                                       direct_cure_drop_K=direct_cure_drop))
            check("direct thermal guard", good, model=model, case=list(key(row)))

refinements = []
for model in models:
    tables = owner_tables if model == "owner_table" else settled_tables[model]["MLCCAg"]
    for row in accounts[model]:
        if row["floor"] and row["drying"] == "bake":
            account = Account(tables[str(row["R_m"])], row["R_m"], row["weather"], row["cure_in_global"])
            account.scan = np.geomspace(.0012*row["R_m"]/10, 1.4*row["R_m"]/10, 1120)
            repeated = account.optimize(11, 1., True, "bake")
            prior = row["result"]["endpoints"][11]
            diff = repeated["payload_kg"]-prior["payload_kg"]
            refinements.append(dict(model=model, case=list(key(row)), n560_payload_kg=prior["payload_kg"],
                                     n1120_payload_kg=repeated["payload_kg"], difference_kg=diff))
            check("denser core search", abs(diff) < .005, model=model, case=list(key(row)), difference_kg=diff)

save("ACCOUNT-BASELINE-COMPARISONS.json", baseline_comparisons)
save("FROZEN-GEOMETRY-CONSEQUENCES.json", fixed)
save("RESIZED-CONSEQUENCES.json", differences)
save("ENDPOINT-FLOAT-CHANGES.json", flips)
save("LEAST-SET-CHANGES.json", least_changes)
save("DIRECT-THERMAL-CHECKS.json", direct_checks)
save("DENSER-SEARCH-CHECKS.json", refinements)
save("ACCOUNT-AUDIT.json", validation)
save("ACCOUNT-AUDIT-DIFFERENCES.json", [r for r in validation if not r["passed"]])
print(json.dumps(dict(cases=360, endpoint_witnesses=5760, frozen_rechecks=len(fixed),
                      resized_comparisons=len(differences), endpoint_float_changes=len(flips),
                      least_set_changes=len(least_changes), audit_checks=len(validation),
                      audit_failed=sum(not r["passed"] for r in validation),
                      frozen_geometry_scarf_crossings=sum("scarf" in r["newly_failed_screens"] for r in fixed),
                      largest_endpoint_payload_change_kg=max(abs(r["payload_difference_kg"]) for r in differences)),
                 indent=2))
