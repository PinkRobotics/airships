"""Reproduce both sides, isolate model terms, and publish resolved alternatives."""
from dataclasses import replace, asdict
import json
import gzip
import numpy as np
from thermal53 import ROOT, Boundary, MODELS, evaluate, solve_state, quadrature, write

TC = .02210679007353296
TF = .0007996763438767137
GC = 46884349.59354485
RHO_CORE = 16.018463373960138
FIELDS = ["tc_m", "day_gradient_K", "night_gradient_K",
          "day_curvature_temperature_K", "night_curvature_temperature_K",
          "gradient_K", "swing_K", "rise_K", "curvature_temperature_K",
          "max_outer_K", "min_outer_K"]
OLD_FIELDS = ["gradient_K", "swing_K", "rise_K", "curvature_temperature_K",
              "max_outer_K", "min_outer_K"]
coatings = json.loads((ROOT/"inputs/048/COATINGS.json").read_text())
coatings = [c for c in coatings if c["alpha"] is not None]
legacy_owner = Boundary(convection="legacy_mixed", gap_emissivity=.2,
                        solid_density=2640, quadrature="midpoint", nodes=37,
                        include_poles=False, raw_day_projection=True, curvature="grid")
common_owner = replace(legacy_owner, solid_density=2700, quadrature="gauss",
                       nodes=128, raw_day_projection=False)
legacy_checker = replace(legacy_owner, convection="forced", gap_emissivity=0.,
                         raw_night_projection=True, curvature="roots")
common_checker = replace(common_owner, convection="forced", gap_emissivity=0.,
                         curvature="roots")


def factors(legacy, common):
    coeff = (23.6e-6-11.3e-6)*np.sqrt(290e9*TF*GC/TC)
    kb = .5*67e9*RHO_CORE/2700
    delta = 1.002*max(abs(366.4833333333333-common["max_outer_K"][0]),
                      abs(366.4833333333333-common["min_outer_K"][0]))
    return dict(legacy_037_day_SF=241316.50526089262/(coeff*legacy["rise_K"][0]),
                legacy_037_full_swing_SF=241316.50526089262/(coeff*legacy["swing_K"][0]),
                current_200F_minimum_edge_SF=(25*6894.757293168361)/
                ((23.6e-6-11.3e-6)*delta*np.sqrt(2*kb*GC)))


summary = {}
mismatches = []
comparison_file = gzip.open(ROOT/"THERMAL-REPRODUCTION.jsonl.gz", "wt")


def compare(group, path, expected, actual, atol=2e-7, rtol=2e-7):
    a, e = float(actual), float(expected)
    delta = a-e
    good = abs(delta) <= atol+rtol*abs(e)
    row = dict(group=group, path=path, expected=e, independent=a,
               difference=delta, atol=atol, rtol=rtol, passed=good)
    comparison_file.write(json.dumps(row, allow_nan=False)+"\n")
    s = summary.setdefault(group, dict(count=0, passed=0, max_absolute_difference=0.))
    s["count"] += 1
    s["passed"] += int(good)
    s["max_absolute_difference"] = max(s["max_absolute_difference"], abs(delta))
    if not good:
        mismatches.append(row)


def compare_arrays(group, prefix, expected, actual, fields):
    for key in fields:
        for index, (old, new) in enumerate(zip(expected[key], actual[key])):
            compare(group, f"{prefix}/{key}/{index}", old, new)


old_screens = {r["id"]: r for r in json.loads((ROOT/"inputs/048/THERMAL-SCREEN.json").read_text())}
check_screens = {r["id"]: r for r in json.loads((ROOT/"inputs/048check/THERMAL-RESULTS.json").read_text())["results"]}
screen_reproduction = []
settled_screens = []
for c in coatings:
    name, alpha, eps = c["id"], c["alpha"], c["epsilon"]
    own_legacy = evaluate(10, TC, alpha, eps, legacy_owner)
    own_common = evaluate(10, TC, alpha, eps, common_owner)
    chk_legacy = evaluate(10, TC, alpha, eps, legacy_checker)
    chk_common = evaluate(10, TC, alpha, eps, common_checker)
    own_factors, chk_factors = factors(own_legacy, own_common), factors(chk_legacy, chk_common)
    for group, target, legacy, common, fs in [
        ("owner048_screen", old_screens[name], own_legacy, own_common, own_factors),
        ("checker048_screen", check_screens[name], chk_legacy, chk_common, chk_factors)]:
        states = target.get("states", target)
        compare_arrays(group, name+"/legacy", states["legacy"], legacy, FIELDS)
        compare_arrays(group, name+"/common", states["common"], common, FIELDS)
        for key, value in fs.items():
            compare(group, name+"/"+key, target[key], value)
    screen_reproduction.append(dict(id=name, owner_boundary=dict(legacy=own_legacy, common=own_common, **own_factors),
                                    checker_boundary=dict(legacy=chk_legacy, common=chk_common, **chk_factors)))
    for model, boundary in MODELS.items():
        value = evaluate(10, TC, alpha, eps, boundary)
        ff = factors(value, value)
        settled_screens.append(dict(id=name, model=model, temperatures=value,
                                    # Current converged screen, not the old 37-midpoint value.
                                    day_factor=ff["legacy_037_day_SF"],
                                    cycle_factor=ff["legacy_037_full_swing_SF"],
                                    cure_edge_minimum_factor=ff["current_200F_minimum_edge_SF"],
                                    day_threshold=1.6782827096937059, cycle_threshold=1.,
                                    day_pass=bool(ff["legacy_037_day_SF"] >= 1.6782827096937059),
                                    cycle_pass=bool(ff["legacy_037_full_swing_SF"] >= 1.)))
write("SCREEN-REPRODUCTION.json", screen_reproduction)
write("SETTLED-FINISH-SCREEN.json", settled_screens)

owner040 = json.loads((ROOT/"inputs/040/THERMAL-TABLE.json").read_text())
checker040 = json.loads((ROOT/"inputs/040check/THERMAL-INDEPENDENT.json").read_text())
owner048 = json.loads((ROOT/"inputs/048/THERMAL-TABLES.json").read_text())
for c in coatings:
    for radius, target in owner048[c["id"]].items():
        calculated = evaluate(float(radius), target["tc_m"], c["alpha"], c["epsilon"], common_owner)
        compare_arrays("owner048_full_table", c["id"]+"/"+radius, target, calculated, FIELDS)
        if c["id"] == "reference040":
            calculated["gradient_K"] = calculated["day_gradient_K"]
            calculated["curvature_temperature_K"] = calculated["day_curvature_temperature_K"]
            compare_arrays("owner040_full_table", radius, owner040[radius], calculated, OLD_FIELDS)
            calculated = evaluate(float(radius), target["tc_m"], boundary=common_checker)
            calculated["gradient_K"] = calculated["day_gradient_K"]
            calculated["curvature_temperature_K"] = calculated["day_curvature_temperature_K"]
            compare_arrays("checker040_full_table", radius, checker040[radius], calculated, OLD_FIELDS)
for radius in sorted(set(owner040)-set(owner048["reference040"]), key=float):
    for group, targets, boundary in [("owner040_full_table", owner040, common_owner),
                                      ("checker040_full_table", checker040, common_checker)]:
        calculated = evaluate(float(radius), targets[radius]["tc_m"], boundary=boundary)
        calculated["gradient_K"] = calculated["day_gradient_K"]
        calculated["curvature_temperature_K"] = calculated["day_curvature_temperature_K"]
        compare_arrays(group, radius, targets[radius], calculated, OLD_FIELDS)
comparison_file.close()
write("THERMAL-REPRODUCTION-SUMMARY.json", summary)
write("THERMAL-REPRODUCTION-DIFFERENCES.json", mismatches)

tables = {}
reference_rows = []
for model, boundary in MODELS.items():
    tables[model] = {}
    for profile, alpha, eps in [("reference040", .2, .9), ("MLCCAg", .09, .8)]:
        tables[model][profile] = {}
        for radius in [10, 12, 15, 20, 30]:
            thickness = np.geomspace(.001*radius/10, 1.5*radius/10, 241)
            tables[model][profile][str(radius)] = evaluate(radius, thickness, alpha, eps, boundary)
            row = evaluate(radius, TC*radius/10, alpha, eps, boundary, profiles=True)
            reference_rows.append(dict(model=model, profile=profile, radius_m=radius,
                                       boundary=asdict(boundary), values=row))
write("SETTLED-THERMAL-TABLES.json", tables)
write("REFERENCE-THERMAL-ROWS.json", reference_rows)
write("BOUNDARY-CHOICES.json", {k: asdict(v) for k, v in MODELS.items()})

convergence = []
for model, boundary in MODELS.items():
    for radius in [10, 15, 30]:
        ts = np.array([.002, TC, .2])*radius/10
        a = evaluate(radius, ts, .09, .8, boundary)
        b = evaluate(radius, ts, .09, .8, replace(boundary, nodes=512))
        c = evaluate(radius, ts, .09, .8, replace(boundary, nodes=1024))
        convergence.append(dict(model=model, radius_m=radius, tc_m=ts.tolist(),
                                n256=a, n512=b, n1024=c,
                                changes={key: (np.array(a[key])-c[key]).tolist() for key in OLD_FIELDS}))
write("THERMAL-CONVERGENCE.json", convergence)

invariants = []
for name, b in MODELS.items():
    state = solve_state(10, [.002, TC, .2], .09, .8, 284.9, 0., b)
    error = max(np.max(abs(state["outer"]-284.9)), np.max(abs(state["inner"]-284.9)))
    invariants.append(dict(model=name, check="uniform environment is isothermal", maximum_error_K=float(error),
                           passed=bool(error < 1e-10)))
    x, w = quadrature(b)
    integral = float(np.sum(w*np.maximum(x, 0)))
    invariants.append(dict(model=name, check="sphere-average absorbed beam is alpha*S/4",
                           independent_normalized_integral=integral, passed=abs(integral-.25) < 1e-12))
write("THERMAL-INVARIANTS.json", invariants)
assert all(r["passed"] for r in invariants)
print(json.dumps(dict(reproduction=summary, unresolved_numeric_differences=len(mismatches),
                     settled_tables=40, reference_rows=len(reference_rows),
                     convergence_cases=len(convergence), invariants=len(invariants)), indent=2))
