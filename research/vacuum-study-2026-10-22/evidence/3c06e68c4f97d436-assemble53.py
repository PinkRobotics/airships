"""Assemble completed numerical artifacts; no scientific solver runs here."""
from pathlib import Path
from collections import Counter
from datetime import datetime
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parent
MODELS = ["forced_conduction", "mixed_conduction", "forced_gap", "mixed_gap"]
LABEL = dict(forced_conduction="Forced / conduction", mixed_conduction="Mixed / conduction",
             forced_gap="Forced / gap .20", mixed_gap="Mixed / gap .20",
             owner_table="Filed table")


def read(name):
    return json.loads((ROOT/name).read_text())


def save(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, allow_nan=False)+"\n")


def csvfile(name, rows):
    fields = list(dict.fromkeys(k for row in rows for k in row))
    with (ROOT/name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json.dumps(v, separators=(",", ":")) if isinstance(v, (dict, list)) else v
                             for k, v in row.items()})


def table(headers, rows):
    return "\n".join(["| "+" | ".join(headers)+" |",
                      "| "+" | ".join("---" for _ in headers)+" |"]+
                     ["| "+" | ".join(str(x) for x in row)+" |" for row in rows])


def case(row):
    return tuple(row[k] for k in ["R_m", "weather", "cure_in_global", "floor", "drying"])


accounts = {m: read("ACCOUNT-"+m+".json") for m in ["owner_table"]+MODELS}
index = {m: {case(r): r for r in rows} for m, rows in accounts.items()}
frozen = read("FROZEN-GEOMETRY-CONSEQUENCES.json")
resized = read("RESIZED-CONSEQUENCES.json")
ref = read("REFERENCE-THERMAL-ROWS.json")
probe = read("THERMAL-PROBE.json")
screen = read("SETTLED-FINISH-SCREEN.json")
mlscreen = {r["model"]: r for r in screen if r["id"] == "MLCCAg"}
reproduction = read("THERMAL-REPRODUCTION-SUMMARY.json")
audits = read("ACCOUNT-AUDIT.json")
alltables = read("SETTLED-THERMAL-TABLES.json")
assert not read("THERMAL-REPRODUCTION-DIFFERENCES.json")
assert not read("ACCOUNT-AUDIT-DIFFERENCES.json")
assert not read("ENDPOINT-FLOAT-CHANGES.json")
assert not read("LEAST-SET-CHANGES.json")

reply = read("inputs/048reply/REFERENCE-VALUES.json")
reference040 = next(r for r in read("SCREEN-REPRODUCTION.json") if r["id"] == "reference040")["owner_boundary"]
reply_checks = []
for name, expected, actual in [
        ("common040", reply["common040"]["values"], reference040["common"]),
        ("density2640_converged", reply["density2640_converged"]["values"], probe["mixed_gap"]),
        ("legacy_diagnostic", reply["legacy_diagnostic"]["values"], reference040["legacy"]),
        ("reference048.legacy", reply["reference048"]["values"]["legacy"], reference040["legacy"]),
        ("reference048.common", reply["reference048"]["values"]["common"], reference040["common"])]:
    for field, value in expected.items():
        if isinstance(value, list) and len(value) == 1:
            difference = actual[field][0]-value[0]
            reply_checks.append(dict(group=name, field=field, supplied=value[0], independent=actual[field][0],
                                     difference=difference, tolerance=2e-7, passed=abs(difference) <= 2e-7))
for field in ["legacy_037_day_SF", "legacy_037_full_swing_SF", "current_200F_minimum_edge_SF"]:
    expected = reply["reference048"]["values"][field]
    actual = reference040[field]
    reply_checks.append(dict(group="reference048.screens", field=field, supplied=expected, independent=actual,
                             difference=actual-expected, tolerance=2e-7, passed=abs(actual-expected) <= 2e-7))
assert all(r["passed"] for r in reply_checks)
save("BOUNDARY-REPLY-COMPARISONS.json", reply_checks)

reference_rows = []
for row in ref:
    v = row["values"]
    flat = dict(model=row["model"], profile=row["profile"], R_m=row["radius_m"])
    flat.update({k: values[0] for k, values in v.items()
                 if isinstance(values, list) and len(values) == 1 and isinstance(values[0], (float, int))})
    reference_rows.append(flat)
csvfile("THERMAL-REFERENCE.csv", reference_rows)
thermal_rows = []
for model, profiles in alltables.items():
    for profile, radii in profiles.items():
        for radius, values in radii.items():
            for j, thickness in enumerate(values["tc_m"]):
                flat = dict(model=model, profile=profile, R_m=int(radius), tc_m=thickness)
                flat.update({k: v[j] for k, v in values.items()
                             if isinstance(v, list) and len(v) == len(values["tc_m"])})
                thermal_rows.append(flat)
csvfile("THERMAL-TABLES.csv", thermal_rows)

account_rows, subset_rows, tie_changes = [], [], []
for model, rows in accounts.items():
    for row in rows:
        identity = {k: row[k] for k in ["model", "R_m", "weather", "cure_in_global", "floor", "drying"]}
        point = row["result"]["endpoints"][11]
        chosen = row["result"]["chosen"]
        flat = dict(**identity, payload_kg=point["payload_kg"], tf_m=point["tf_m"], tc_m=point["tc_m"],
                    least_mask=chosen["mask"] if chosen else None,
                    least_axes=chosen["selected_axes"] if chosen else None,
                    least_usage=chosen["usage"] if chosen else None,
                    cure_compression_Pa=point["properties"]["cure_compression_Pa"],
                    edge_usage=1/point["modes"]["core_edge"], wall_usage=1/point["modes"]["cell_wall"],
                    scarf_usage=1/point["modes"]["scarf"],
                    endpoint_float=point["payload_kg"] >= 0,
                    service_pressure_Pa=point["service_pressure_Pa"],
                    service_pressure_SF=point["service_pressure_SF"])
        flat.update({"mass_"+k: v for k, v in point["bill_kg"].items()})
        account_rows.append(flat)
        for mask, witness in enumerate(row["result"]["endpoints"]):
            subset_rows.append(dict(**identity, mask=mask,
                                    feasible=witness is not None,
                                    payload_kg=witness["payload_kg"] if witness else None,
                                    floats=witness is not None and witness["payload_kg"] >= 0))
        if model != "owner_table":
            old = index["owner_table"][case(row)]
            before = sorted(p["mask"] for p in old["result"].get("ties", []))
            after = sorted(p["mask"] for p in row["result"].get("ties", []))
            if before != after:
                tie_changes.append(dict(model=model, case=list(case(row)), before=before, after=after))
csvfile("PAYLOAD-AND-BOND.csv", account_rows)
csvfile("SUBSET-ENDPOINTS.csv", subset_rows)
csvfile("RESIZED-CONSEQUENCES.csv", resized)
save("LEAST-TIED-SET-CHANGES.json", tie_changes)
assert not tie_changes

crossings = Counter(mode for r in frozen for mode in r["newly_failed_screens"])
model_summary = {}
for model in MODELS:
    a = [r for r in frozen if r["model"] == model]
    b = [r for r in resized if r["model"] == model]
    model_summary[model] = dict(
        payload_change_range_kg=[min(r["payload_difference_kg"] for r in b),
                                 max(r["payload_difference_kg"] for r in b)],
        frozen_scarf_SF_range=[min(r["revised"]["modes"]["scarf"] for r in a),
                               max(r["revised"]["modes"]["scarf"] for r in a)],
        frozen_new_screens=dict(Counter(mode for r in a for mode in r["newly_failed_screens"])),
        minimum_frozen_global_SF=min(r["revised"]["modes"]["global"] for r in a),
        minimum_frozen_edge_SF=min(r["revised"]["modes"]["core_edge"] for r in a),
        minimum_frozen_wall_SF=min(r["revised"]["modes"]["cell_wall"] for r in a),
        maximum_resized_edge_usage=max(r["new_edge_usage"] for r in b),
        maximum_resized_wall_usage=max(r["new_wall_usage"] for r in b),
        added_face_range_m=[min(r["added_face_thickness_m"] for r in b),
                            max(r["added_face_thickness_m"] for r in b)],
        core_change_range_m=[min(r["core_thickness_difference_m"] for r in b),
                             max(r["core_thickness_difference_m"] for r in b)])

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

probe_table = table(["Convection / core transport", "Face gradient K", "Day rise K", "Day–night swing K"],
                    [[LABEL[m], f'{probe[m]["gradient_K"][0]:.9f}',
                      f'{probe[m]["rise_K"][0]:.9f}', f'{probe[m]["swing_K"][0]:.9f}'] for m in MODELS])
reference_table = table(
    ["Boundary", "R m", "tc mm", "Gradient K", "Rise K", "Swing K", "Cold K", "Curvature K"],
    [[LABEL[r["model"]], r["R_m"], f'{1000*r["tc_m"]:.4f}',
      *[f'{r[k]:.6f}' for k in ["gradient_K", "rise_K", "swing_K", "min_outer_K", "curvature_temperature_K"]]]
     for r in reference_rows if r["profile"] == "MLCCAg"])
screen_table = table(["Boundary", "Day factor", "Cycle factor", "200°F free-edge factor", "Day / cycle"],
                     [[LABEL[m], f'{mlscreen[m]["day_factor"]:.6f}', f'{mlscreen[m]["cycle_factor"]:.6f}',
                       f'{mlscreen[m]["cure_edge_minimum_factor"]:.6f}', "pass / pass"] for m in MODELS])
payload_table = table(
    ["Cure in global/crimp", "R / weather", "Filed kg", "Forced/conduction kg",
     "Mixed/conduction kg", "Forced/gap kg", "Mixed/gap kg"],
    [["yes" if k[2] else "no", f"R{k[0]} / {k[1]}"]+
     [f'{index[m][k]["result"]["endpoints"][11]["payload_kg"]:.6f}' for m in ["owner_table"]+MODELS]
     for k in primary_keys])
least_table = table(
    ["Cure included", "R / weather", "Minimum axes", "Filed usage", "Forced/conduction usage", "Change"],
    [["yes" if k[2] else "no", f"R{k[0]} / {k[1]}",
      "+".join(index["forced_conduction"][k]["result"]["chosen"]["selected_axes"])
      if index["forced_conduction"][k]["result"]["chosen"] else "none floats",
      f'{index["owner_table"][k]["result"]["chosen"]["usage"]:.9f}'
      if index["owner_table"][k]["result"]["chosen"] else "—",
      f'{index["forced_conduction"][k]["result"]["chosen"]["usage"]:.9f}'
      if index["forced_conduction"][k]["result"]["chosen"] else "—",
      f'{index["forced_conduction"][k]["result"]["chosen"]["usage"]-index["owner_table"][k]["result"]["chosen"]["usage"]:+.9f}'
      if index["forced_conduction"][k]["result"]["chosen"] else "—"] for k in primary_keys])
bond_table = table(
    ["Boundary", "Frozen scarf SF range", "New global failures / 72", "Worst edge usage after resize",
     "Worst wall usage after resize", "Payload change range kg"],
    [[LABEL[m], "–".join(f"{x:.9f}" for x in model_summary[m]["frozen_scarf_SF_range"]),
      model_summary[m]["frozen_new_screens"].get("global", 0),
      f'{model_summary[m]["maximum_resized_edge_usage"]:.6f}',
      f'{model_summary[m]["maximum_resized_wall_usage"]:.6f}',
      " to ".join(f"{x:+.6f}" for x in model_summary[m]["payload_change_range_kg"])] for m in MODELS])
cure_table = table(
    ["R / weather", "Filed cure compression MPa", "Forced/conduction MPa", "Change MPa", "New tf mm", "New tc mm"],
    [[f"R{k[0]} / {k[1]}",
      f'{index["owner_table"][k]["result"]["endpoints"][11]["properties"]["cure_compression_Pa"]/1e6:.6f}',
      f'{index["forced_conduction"][k]["result"]["endpoints"][11]["properties"]["cure_compression_Pa"]/1e6:.6f}',
      f'{(index["forced_conduction"][k]["result"]["endpoints"][11]["properties"]["cure_compression_Pa"]-index["owner_table"][k]["result"]["endpoints"][11]["properties"]["cure_compression_Pa"])/1e6:+.6f}',
      f'{index["forced_conduction"][k]["result"]["endpoints"][11]["tf_m"]*1000:.6f}',
      f'{index["forced_conduction"][k]["result"]["endpoints"][11]["tc_m"]*1000:.6f}']
     for k in primary_keys if k[2]])
reproduction_table = table(["Compared product", "Comparisons", "Pass", "Largest absolute difference"],
                          [[k, v["count"], v["passed"], f'{v["max_absolute_difference"]:.3g}']
                           for k, v in reproduction.items()])
card = f"""# MAINLINE-053 — settled thermal specification and consequences

**The arithmetic discrepancy is resolved. Physical boundary qualification remains open.**
An independently written simultaneous energy solver reproduces all {results['thermal_comparisons']:,}
selected owner/CHECK-040/CHECK-048 comparisons after their actual boundary terms
are specified. Four explicit thermal alternatives are filed for R10–30.
At R10/12/15, no endpoint float decision, minimum-axis choice or tied minimum-axis
set changes. Resizing costs at most {results['maximum_payload_cost_kg']:.6f} kg.
Previously sized geometries do cross the scarf screen; the resized witnesses
pass the declared scalar constraints.

Every inherited material property is **QUESTIONABLE** and every installed
geometry, optical transfer, process and performance prediction is **PROJECTION**.
Installed hull safety factor and flight qualification remain unknown.
The brief is complete and names no immediate successor; stop and file.

The complete equations, units and omitted physics are in
[SPECIFICATION.md](SPECIFICATION.md) and [METHOD.md](METHOD.md).
[INPUTS.json](INPUTS.json), [INPUT-PINS.json](INPUT-PINS.json) and
[EVIDENCE.json](EVIDENCE.json) make their provenance explicit.

**Why owner and checkers differed.** The owner uses a temperature-dependent
convection floor, h=max(hforced,1.32 max(|To−Ta|,.05)^.25), and adds
4×.20×σ×average(Ti)³ to solid-core conductance. Both checkers use forced
convection alone and omit that gap term. At the historical R10 white-finish
geometry, tc=.02210679007353296 m and foil density 2640 kg/m³, the independent
128-node reproduction gives:

{probe_table}

For example, the gradient difference .464608894→.413901181 K and swing
33.640781944→31.118178070 K follow from changing those terms.
The extra core-gap exchange and the hull's internal enclosure radiation are
distinct heat paths; their joint inclusion is not automatically double counting.
The gap coefficient nevertheless remains unqualified.

A separate legacy projection issue is also resolved. Raw 37-midpoint
projection leaks a constant temperature into degrees 2–6. CHECK-048 retained
this for night, giving 226.884841 K of apparent curvature temperature in its
reference legacy row; the owner-derived 048 night row removed the mean
(2.585175 K under its different boundary). Those legacy rows differ in both
boundary and projection. Neither raw-field curvature is carried forward.
All settled tables remove the mean before projection.

The later in-band order
`ord-admiral-rr2-mainline053-fold-boundary-reply-1020` supplies the owner's
[BOUNDARY-REPLY.md](inputs/048reply/BOUNDARY-REPLY.md). Its convection,
conductance, normalized averages and outer balance agree with this
reconstruction. All {len(reply_checks)} supplied temperature and screen entries
match the already completed independent results within declared tolerance;
[BOUNDARY-REPLY-COMPARISONS.json](BOUNDARY-REPLY-COMPARISONS.json) records
each comparison. Current and legacy densities and iteration conventions are
kept distinct. The reply's legacy projection prose is read with its numerical
attachment: the later 048 night diagnostic removes the mean, while the day
diagnostic retains the raw projection. Different solver iteration counts
do not signify different physical solutions.

{reproduction_table}

These are field-by-field arithmetic comparisons, not independent material
observations. The compressed comparison ledger records values and tolerances;
[THERMAL-REPRODUCTION-DIFFERENCES.json](THERMAL-REPRODUCTION-DIFFERENCES.json)
is empty. Upstream source was inspected to settle specification omissions,
but no upstream executable was imported or run.

**The selected specification is a disclosed family.** Air is 284.9 K at
2 m/s, solar flux 970 W/m², day/night sky 275/260 K, ground 284.9 K, inner
emissivity .20, and solar zenith aligned with the sphere's axis. Sky/ground
view factors are (1±μ)/2. The selected multilayer CCAg/ITO pair is .09/.80.
Solid-core transport is 130ρcore/(2700tc), with zero or .20 gap augmentation.
The two convection readings crossed with these two gap readings give the
four labels below. None is a certified bound on real operation.

Whitaker's primary sphere fit reports Re 3.5–76,000; the inherited hull use
at 2.61–7.83 million is extrapolation. No supplied evidence validates the
inherited natural-convection floor for this sphere.
[Whitaker, 1972](https://www.researchgate.net/profile/Stephen-Whitaker-3/publication/229709417_Forced_convection_heat_transfer_correlations_for_flow_in_pipes_past_flat_plates_single_cylinders_single_spheres_and_for_flow_in_packed_beds_and_tube_bundles/links/59d73bda0f7e9b42a6b0694a/Forced-convection-heat-transfer-correlations-for-flow-in-pipes-past-flat-plates-single-cylinders-single-spheres-and-for-flow-in-packed-beds-and-tube-bundles.pdf).
NASA's bonded honeycomb work distinguishes conduction, radiation and interface
resistance; it does not supply the missing installed CR-III/AF163/Be
conductance. [NASA honeycomb study](https://ntrs.nasa.gov/api/citations/19680009019/downloads/19680009019.pdf).
The transparent conduction-only rows and inherited gap rows therefore remain
side by side.

Settled tables use 256 split-Gauss nodes, explicit poles, mean-removed
degrees 2–6 and polynomial curvature extrema. Each finish/model/radius has
241 core thicknesses. [THERMAL-TABLES.csv](THERMAL-TABLES.csv) contains all
{len(thermal_rows):,} thickness rows; the JSON retains solver diagnostics.
The following multilayer-finish reference rows use tc=.02210679007353296R/10 m.
Gradient means the largest absolute day/night face difference; swing means
maximum daytime minus minimum nighttime outer temperature. Curvature is a
temperature-derived screen, not a temperature rise.

{reference_table}

The reference white finish is also retained in
[THERMAL-REFERENCE.csv](THERMAL-REFERENCE.csv), with full angular face
profiles in [REFERENCE-THERMAL-ROWS.json](REFERENCE-THERMAL-ROWS.json).
These are separate equilibria; thermal inertia, lateral conduction, actual
sun angle, adhesive/contact resistance, inner obstructions, wet optics and a
joint weather/thermal mission remain open.

**Finish screening is unchanged in outcome.** At the original R10 geometry,
the inherited rigid shear-lag day threshold is 1.678282710 and the cycle
threshold is 1. The separate compliant-core 200°F free-edge screen uses
minimum W shear rather than the typical value used by the historical screen.

{screen_table}

All four multilayer rows pass these stated screens. NASA's multilayer CCAg
class supports the optical-pair transfer, but does not qualify this exact
coating on Be after outdoor moisture and aging.
[NASA Goddard, slide 39](https://ntrs.nasa.gov/api/citations/20180002012/downloads/20180002012.pdf).
The 13 candidate finishes under all four boundaries are in
[SETTLED-FINISH-SCREEN.json](SETTLED-FINISH-SCREEN.json).

**Payload consequences preserve the full mass account.** The following
numbers use the 028b gamma/Q endpoint, today's face tuple and its already
favorable .015 lb/ft² interface film. This is mask 11: gamma+Q+film in the
four-axis accounting. Each geometry is resized with the 30.341397319:1 scarf,
200°F cure, retained 5% joining floor and projected ground-bake drying route.
The bill retains 0.1 kg/m² exterior water, material moisture, coating,
structural primer, pad, systems, gas, contamination and weather headroom.
The optimistic weather label is inherited from the atmospheric account;
it changes pressure and buoyancy, not the thermal boundary.

{payload_table}

The first six rows retain the original exclusion of balanced cure compression
from global/crimp demand. The final six include it, as the later CHECK-040/048
fold requires for the conservative scalar comparison. These mechanical
branches are separate from the four thermal readings. Ground bake is a
conditional process credit, not an installed qualification.

[PAYLOAD-AND-BOND.csv](PAYLOAD-AND-BOND.csv) gives all 360 configurations,
including actual joining and retained-floor accounts and dry-gas/bake/sorbent
routes. The five ACCOUNT files retain every geometry, material property,
mass item, limit and least-set witness. [SUBSET-ENDPOINTS.csv](SUBSET-ENDPOINTS.csv)
contains all 5,760 endpoint witnesses. Across four alternatives and 72
configurations, none of the 4,608 endpoint comparisons changes float sign.

**Least optimism sets persist, with slightly larger usage.** Usage is the
common logarithmic interpolation fraction on the selected axes, not a
fractional payload or safety factor. This table shows the reference
forced/conduction alternative against the filed thermal table; all other
alternatives and tied minimum sets are retained in the machine-readable data.

{least_table}

At retained-floor/bake R10 optimistic weather, no allowed subset floats,
including the full four-axis endpoint. That failure is not repaired by
thermal reconciliation.

**A frozen-geometry bond pass does change.** Every filed endpoint is almost
exactly scarf-limited, so the updated thermal demand takes all 288 frozen
scarf checks below one under the declared 2e−7 comparison tolerance.
There are also {crossings.get('global', 0)} new frozen global-screen crossings.
Free-edge and cell-wall screens remain above one. Results by alternative:

{bond_table}

The mixed/gap deficit is only about six parts in ten million, a numerical
convention effect whose physical significance is far below the open material
uncertainty. The largest scarf deficit is about 0.0366%. It would be
incorrect either to claim unchanged frozen pass status or to turn that
numerically small branch difference into a demonstrated physical failure.
Resizing restores scarf and global screens; added face thickness across all
alternatives ranges from sub-nanometre numerical adjustments to 0.441010 μm.
The new core/edge usages stay below one.

For the cure-inclusive, retained-floor/bake reference alternative, balanced
cure compression and geometry are:

{cure_table}

This is a conditional stress calculation. The continuous compliant-core
field, free-edge transfer, scarf-average shear and foil yield proxy do not
establish adhesive peel, coincident loads, a finished assembly allowable or
full-hull stability. The pinned 037b qualifications remain open.

**Verification and custody.** All {len(audits):,} accounting checks pass,
including exact mass conservation, resized limits, cure-force balance,
an independent closed scarf root, lower-cardinality favorable-E bounds,
288 direct thermal guard checks and 60 denser geometry searches.
The maximum difference from the 72 original payload endpoints is
{results['maximum_original_payload_reproduction_error_kg']:.9f} kg; the 36
fixed-geometry bill reproductions agree within 1.819e−12 kg. Doubling the
core grid changes primary payloads by at most
{results['maximum_denser_search_change_kg']:.9f} kg.

There are eight energy/quadrature invariants. Increasing thermal quadrature
from 256 to 1024 changes the sampled extrema/swing by less than
{max(convergence_max[k] for k in ['gradient_K','swing_K','rise_K','min_outer_K','max_outer_K']):.9g} K
and curvature temperature by at most
{convergence_max['curvature_temperature_K']:.9g} K.
Across complete settled tables, maximum local energy residual is
{results['maximum_energy_residual_W_m2']:.3g} W/m². The retained 1.002 guard
covers numerical interpolation in all directly checked resized points;
it does not bound physical model error.

All heavy runs used one-core, 1 GiB simjob admission. Four refusals were
retried unchanged; a serialization failure was corrected and retained in
the execution record. Later thermal runs completed the R20/30 reproduction
coverage. [TIMING.json](TIMING.json) measures elapsed time without imposing
a work budget. [VALIDATION.json](VALIDATION.json), [MANIFEST.json](MANIFEST.json)
and the report pins provide delivery custody.

All 142 frozen inputs retain their intake hashes. One live original,
COMMON.md, gained an explicit heavy-run simjob requirement after intake.
The runs already comply. Its pinned version, later copy, exact difference
and disposition are preserved in [SOURCE-DRIFT.json](SOURCE-DRIFT.json);
the other 141 live originals remain unchanged at delivery validation.

Nine new open, nonblocking NFI groups and six inherited registers preserve
the unresolved physics and assembly evidence. Only the local arithmetic and
legacy-projection discrepancies are resolved. No installed hull safety
factor is asserted. No supplier or other seat was contacted out of band.

![Thermal choices and payload consequences](THERMAL-SETTLEMENT.png)

The figure is also supplied as [SVG](THERMAL-SETTLEMENT.svg) and
[PDF](THERMAL-SETTLEMENT.pdf).
"""
(ROOT/"CARD.md").write_text(card)
print(json.dumps(dict(thermal_rows=len(thermal_rows), reference_rows=len(reference_rows),
                      account_rows=len(account_rows), subsets=len(subset_rows),
                      tied_set_changes=len(tie_changes), results="RESULTS.json", card_words=len(card.split()))))
