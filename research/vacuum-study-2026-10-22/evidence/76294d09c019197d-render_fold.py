#!/usr/bin/env python3
"""Reviewable addendum, complete rows and attributed unresolved findings."""
import csv
import json
from pathlib import Path
from datetime import datetime,timezone

B=Path(__file__).resolve().parent
def load(name):return json.loads((B/name).read_text())
def dump(name,obj):(B/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+"\n")
I=load("INPUTS.json");v=load("VALIDATION.json")
assert v["passed"]
datasets=[load(f"RESULTS-{n}.json") for n in I["profiles"]]
assert all(x["complete"] for x in datasets)
rows=[r for d in datasets for r in d["rows"]]
pairs=[r for d in datasets for r in d["pairs"]]
bounds=[r for d in datasets for r in d["bounds"]]
ix={(r["profile"],r["R_m"],r["weather"],r["floor"],r["drying"],
     r["external_water_kg_m2"],r["cure_in_global"]):r for r in rows}
px={p["id"]:p for p in pairs}
def get(name="MLCCAg",r=10,w="ISA",floor=True,dry="bake70",water=.1,cure=True):
    return ix[name,r,w,floor,dry,water,cure]
def full(row):return next(t["solution"] for t in row["least"]["endpoint_trials"] if t["mask"]==15)
def label(p):
    if p is None:return "none"
    names=["G","Q","E/Fcy","film"]
    return "+".join(x for j,x in enumerate(names) if p["mask"]&(1<<j))+f" {p['usage']:.6f}"
def pair(row):return px[row["id"].removesuffix("-cure_included")]
lost=[p["id"] for p in pairs if p["original_least"] is not None and p["cure_least"] is None]
changed=[dict(id=p["id"],original=label(p["original_least"]),new=label(p["cure_least"]))
         for p in pairs if p["original_least"] is not None and p["cure_least"] is not None
         and p["original_least"]["mask"].bit_count()!=p["cure_least"]["mask"].bit_count()]
heavy=[r for r in rows if r["external_water_kg_m2"]==1]
best=max(heavy,key=lambda r:full(r)["signed_payload_kg"])
upper=max(heavy,key=lambda r:r["favorable_payload_upper_kg"])
assert len(heavy)==432 and all(full(r)["signed_payload_kg"]<0 for r in heavy)
dump("RESULTS.json",dict(
    tag="QUESTIONABLE / PROJECTION",complete=True,new_configurations=648,
    rows=rows,paired_cure_rows=pairs,exclusion_bounds=bounds,
    lost_float_configurations=lost,changed_axis_count=changed,
    best_one_mm_all_four=dict(id=best["id"],payload_kg=full(best)["signed_payload_kg"]),
    best_one_mm_favorable_upper=dict(id=upper["id"],payload_upper_kg=upper["favorable_payload_upper_kg"]),
    original_048_directory=I["original_048_directory"],overall_installed_hull_SF=None))
fields=["id","profile","R_m","weather","floor","drying","external_water_kg_m2",
        "cure_in_global","endpoint_payload_kg","all_four_payload_kg",
        "least_set","least_usage","tf_mm","tc_mm","global_SF","crimp_SF",
        "edge_SF","external_water_kg","extra_material_water_kg","sorbent_kg",
        "favorable_one_mm_upper_kg","installed_hull_SF"]
with (B/"ROWS.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for r in rows:
        p=r["two_factor_endpoint"];l=r["least"]["least"];b=p["bill_kg"]
        d={k:r[k] for k in fields[:8]}
        d.update(endpoint_payload_kg=p["signed_payload_kg"],all_four_payload_kg=full(r)["signed_payload_kg"],
                 least_set=label(l),least_usage=None if l is None else l["usage"],
                 tf_mm=p["geometry"]["tf_m"]*1000,tc_mm=p["geometry"]["tc_m"]*1000,
                 global_SF=p["modes"]["global_buckling"],crimp_SF=p["modes"]["core_shear_crimping"],
                 edge_SF=p["modes"]["thermal_core_interface_screen"],
                 external_water_kg=b["water"],extra_material_water_kg=b["absorbed_water"],
                 sorbent_kg=b["desiccant"],
                 favorable_one_mm_upper_kg=r.get("favorable_payload_upper_kg"),
                 installed_hull_SF=None)
        w.writerow(d)
retention=[]
for r in rows:
    p=r["two_factor_endpoint"];s=p["settings"];b=p["bill_kg"]
    retention.append(dict(
        id=r["id"],route=r["drying"],profile=r["profile"],R_m=r["R_m"],
        external_before_process_measured_kg=None,external_after_process_measured_kg=None,
        external_retention_source="016/019 planning scenario; no measured finish/process limit",
        service_retention_assumption_mm=r["external_water_kg_m2"],
        service_retention_charge_kg=b["water"],
        external_service_charge_reduction_credited_by_route_kg=0.,
        added_material_water_before_conditioning_kg=b["absorbed_water"]/s["moisture_scale"],
        added_material_water_remaining_aboard_kg=b["absorbed_water"],
        added_sorbent_and_cartridge_kg=b["desiccant"],
        note="Ground evaporation of accessible liquid and later outdoor rewetting are separate events."))
dump("RETENTION-BEFORE-AFTER.json",retention)
oldnfi=load("inputs/048/NFI.json")
checknfi=load("inputs/check040/NFI.json")
nfi=[
 dict(id="048A-WATER-SCENARIO",tag="PROJECTION",status="OPEN",
      finding="0.1 mm is the optimistic 019 retained-water scenario; 1 mm is a separate conservative scenario. Neither is a measured retained layer or bound for the finish before/after any drying route.",
      grounding="Measure exterior liquid before/after processing and rain/dew/frost retention, drainage and optics during the chosen mission; retain both scenarios meanwhile."),
 dict(id="048A-CURE-GLOBAL-CRIMP",tag="QUESTIONABLE",status="OPEN",
      finding="Cure compression is now explicitly included in alternate global/crimp rows without double counting local demand. Including it is an unresolved structural premise, not a new measured load.",
      grounding="Establish the residual field and its effect on global/crimp eigenmodes with matched curved panels and a cell/layer model.",
      evidence="RESULTS.json; CHECK040-REPRODUCTION.json; METHOD.md"),
 dict(id="048A-200F-2U015-BOND",tag="QUESTIONABLE",status="OPEN",
      finding="The detailed 200 F source tests use AF163-2K .060 lb/ft2 metal joints with EC-3924B and 50 psi. They do not qualify 2U .015 lb/ft2 Be/5056 honeycomb or the assumed structural-primer process.",
      grounding="Qualify exact film weight, primer, adherends, tooling pressure, cure cycle, strength/peel/creep/life and actual stress-free temperature. Do not equate oven setpoint with stress-free temperature.",
      evidence="WATER-AND-BOND-SOURCES.md; inputs/048/AF163-SOURCE.pdf printed page 15"),
 dict(id="048A-THERMAL-REPRODUCTION",tag="QUESTIONABLE / PROJECTION",status="OPEN",
      finding="CHECK-040's independent temperature solve differs from the owner's table. Existing tables are held fixed; an exact non-code boundary statement is now supplied, including natural-convection selection and the U approximation.",
      grounding="Independently reproduce that statement and validate the real combined weather/thermal/wetting boundary; internal numerical convergence does not close physical or independent reproduction.",
      evidence="THERMAL-BOUNDARY.md; inputs/check040/THERMAL-CLOSURE.json")
]
dump("NFI.json",dict(
    unit=I["unit"],overall_installed_hull_SF=None,findings=nfi,
    inherited_048=oldnfi,inherited_CHECK040=checknfi,
    note="Collections are attributed and may repeat upstream findings. No physical NFI is closed by this addendum."))

r10=["| Finish | Dry gas: original → cure included | Bake: original → cure included | Sorbent: original → cure included |",
     "|---|---:|---:|---:|"]
for name in I["profiles"]:
    cells=[]
    for dry in I["routes"]:
        p=pair(get(name,dry=dry))
        cells.append(f"{p['original_endpoint']['signed_payload_kg']:+.3f} → {p['cure_endpoint']['signed_payload_kg']:+.3f}")
    r10.append(f"| {name} | "+" | ".join(cells)+" |")
main=["| R, m | Weather | Named endpoint: actual / floor | All-four endpoint: actual / floor | Least set, retained floor |",
      "|---:|---|---:|---:|---|"]
for r in I["radii_m"]:
    for w in I["weather"]:
        a=get(r=r,w=w,floor=False);f=get(r=r,w=w)
        main.append(f"| {r} | {w} | {a['two_factor_endpoint']['signed_payload_kg']:+.3f} / "
                    f"{f['two_factor_endpoint']['signed_payload_kg']:+.3f} | "
                    f"{full(a)['signed_payload_kg']:+.3f} / {full(f)['signed_payload_kg']:+.3f} | "
                    f"{label(f['least']['least'])} |")
watertable=["| Finish | R, m | Best all-four payload, original cure treatment | Best all-four payload, cure included | Best favorable upper bound across both |",
            "|---|---:|---:|---:|---:|"]
for name in I["profiles"]:
    for r in I["radii_m"]:
        sub=[x for x in heavy if x["profile"]==name and x["R_m"]==r]
        vals=[max(full(x)["signed_payload_kg"] for x in sub if x["cure_in_global"]==c)
              for c in [False,True]]
        ub=max(x["favorable_payload_upper_kg"] for x in sub)
        watertable.append(f"| {name} | {r} | {vals[0]:+.3f} | {vals[1]:+.3f} | {ub:+.3f} |")
watercost=["| Route | Modeled added material water, before → aboard at R10 | Exterior service debit at 0.1 / 1 mm | Source-supported measured exterior limit after route |",
           "|---|---:|---:|---|"]
for dry in I["routes"]:
    p=get(dry=dry)["two_factor_endpoint"];b=p["bill_kg"];s=p["settings"]
    watercost.append(f"| {dry} | {b['absorbed_water']/s['moisture_scale']:.3f} → "
                     f"{b['absorbed_water']:.3f} kg | 125.664 / 1256.637 kg | none established |")
losttext=("\n".join("- `"+x+"`" for x in lost) if lost else "No previously floating 0.1 mm configuration loses every allowed optimism set.")
repro=load("CHECK040-REPRODUCTION.json")
maxdelta=max(abs(x["delta_kg"]) for x in repro)
card=f"""# MAINLINE-048 addendum — CHECK-040 findings

**QUESTIONABLE / PROJECTION. The requested three findings are carried. At 1 mm retained exterior water, all 432 new R10–15 heavy-water cases are negative, including every all-four endpoint and the deliberately favorable interior-optimism bound. Adding cure compression to global/crimp demand reduces the 0.1 mm margins. The proposed 200 °F, 2U .015 Be/honeycomb bond remains unqualified.**

This is an addendum to the [filed 048 card](../vacuum-mainline048-coating-and-water-1020/CARD.md). Its artifacts remain unchanged. Authority: `ord-admiral-rr2-mainline048-fold-chk040-1020`, incorporating `rpt-ref-593068c3ed82fd458128`. There are **648 new configurations**: 216 cure-included rows at 0.1 mm and 432 rows at 1 mm across both cure-demand treatments. [RESULTS.json](RESULTS.json) and [ROWS.csv](ROWS.csv) contain the full matrix, both endpoints, least sets and all subset trials.

## Retention supported by the sources

016 calls 0.1–1 mm an assumed equivalent retained surface-film band. 019 selects 0.1 mm for its optimistic planning scenario and 1 mm for a separate conservative scenario. **Neither source measures either retention for these finishes or establishes an upper bound.** The atmospheric `both` weather set does not automatically change the selected vehicle-water charge.

Before processing, actual exterior liquid is unmeasured. After each listed dry-out route, no measured exterior-retention limit is established. A bake can evaporate accessible liquid already present, and a controlled dry environment can support a dry release; neither proves subsequent rain/dew/frost retention. Internal sorbent changes internal vapor distribution and keeps captured mass aboard. No route earns an in-service exterior-water reduction.

{chr(10).join(watercost)}

The material values above use the multilayer coating, cure included, ISA and retained joining floor. They are assumed inventory/conditioning values, not observations. The bake removal target is still 90% of added material water; it does not remove a future exterior film. [RETENTION-BEFORE-AFTER.json](RETENTION-BEFORE-AFTER.json) records measured fields as unknown and keeps the scenario charges separate for every new row. Full provenance and process distinctions are in [WATER-AND-BOND-SOURCES.md](WATER-AND-BOND-SOURCES.md).

Going from 0.1 to 1 mm adds **1130.973, 1628.602 and 2544.690 kg** at R10, R12 and R15. Every row below is the best payload over the three weather states, both joining conventions and all drying routes for that finish/radius. The final column additionally permits full elastic E with the smaller thermal E, an intentionally favorable combination outside the allowed coupled tuple.

{chr(10).join(watertable)}

The least-negative all-four endpoint is **{full(best)['signed_payload_kg']:+.3f} kg**, at `{best['id']}`. Even the best favorable bound is **{upper['favorable_payload_upper_kg']:+.3f} kg**. No hidden lower-count or interior-E float remains within the stated scalar model. These rows hold dry optical inputs fixed; they do not qualify the wet thermal state.

CHECK-040's −594.989 kg R30 example is reproduced as a check of its original 0.20 kg/m² coating account. New-finish R30 at 1 mm is outside this addendum's R10–15 scope and is not inferred from that number.

## Cure compression in global and crimp demand

The added row uses `σpressure + σcure` for global demand and `σpressure + σgradient + σbend + σcure` for crimp demand. Local face/scarf demand already included cure compression and is unchanged. No cure term is counted twice. All original free-edge, cell-wall, service, pad, joining and mass conditions remain.

At R10 ISA, 0.1 mm exterior water and retained joining floor, named-endpoint payloads in kg are:

{chr(10).join(r10)}

The newly coated multilayer R10 bake case remains **{get()['two_factor_endpoint']['signed_payload_kg']:+.3f} kg** under this alternative; its least set is **{label(get()['least']['least'])}**. That is still conditional on coating optics/mass, gamma/Q/film, the 200 °F stress-free assumption and the unqualified bond.

For the multilayer coating with the bake target and cure compression included, the full radius/weather comparison is:

{chr(10).join(main)}

G is the effective global coefficient, Q the wrinkling factor, film the adhesive-weight axis, and E/Fcy the coupled face tuple. Usage is the same minimum-axis-count then common-logarithmic-usage objective as 048. Both joining conventions and every dry-out route are present in the machine-readable rows.

The added demand eliminates all allowed floats in **{len(lost)}** previously floating 0.1 mm configurations:

{losttext}

An additional **{len(changed)}** still-floating configurations need a different minimum axis count. The exact transitions are in RESULTS.json. CHECK-040's R15 optimistic/actual all-four result of −1.821165598 kg was independently reproduced using its original bill; it is not substituted for the lighter-coating rows.

## Exact bond-qualification gap

The detailed 200 °F source test uses **AF163-2K .060 lb/ft², EC-3924B primer, metal-to-metal joints and 50 psi cure pressure**. It does not qualify **AF163-2U .015 lb/ft² on Be/5056 honeycomb**, its primer or its tooling load path. The 200 °F model reference does not establish actual stress-free temperature. This explicit finding is `048A-200F-2U015-BOND` in [NFI.json](NFI.json), with the primary sheet and page recorded in [WATER-AND-BOND-SOURCES.md](WATER-AND-BOND-SOURCES.md).

All original 048 and CHECK-040 findings are retained with attribution, including cell-scale edge transfer, cure tooling, wet optics and physical thermal-boundary questions. The complete existing solver boundary is supplied in [THERMAL-BOUNDARY.md](THERMAL-BOUNDARY.md); independent reproduction and selection of the real mission boundary remain open. This fold does not claim that the earlier internal numerical checks closed CHECK-040's separate thermal result.

## Verification and filing

**{v['checks']:,} checks pass across {v['unique_points']:,} distinct stored points and 648 new configurations.** The changed demands, exact exterior-water offsets, ledgers, pass flags, denser searches and optimism bounds are verified. All 43 independent CHECK-040 cure endpoint targets reproduce within {maxdelta:.6f} kg, against a 0.005 kg tolerance. Original filed 048 and 040 pins are unchanged.

[VALIDATION.json](VALIDATION.json) and [METHOD.md](METHOD.md) give the evidence and reconstruction rules. The original dry-exterior sensitivities remain separate conditional operations; no drying-route credit is assigned to future exterior wetting. **Installed-hull SF remains unknown.**

The requested fold is complete. Stop and file.
"""
(B/"CARD.md").write_text(card)
dump("SUMMARY.json",dict(
    tag="QUESTIONABLE / PROJECTION",new_configurations=len(rows),
    heavy_water_configurations=len(heavy),lost_float_configurations=lost,
    changed_axis_count=changed,primary_R10_bake=get()["two_factor_endpoint"],
    best_one_mm_all_four_kg=full(best)["signed_payload_kg"],
    best_one_mm_favorable_upper_kg=upper["favorable_payload_upper_kg"],
    validation_checks=v["checks"],finished_at=datetime.now(timezone.utc).isoformat()))
print("Rendered addendum;",len(rows),"rows;",len(lost),"lost float cases.")
