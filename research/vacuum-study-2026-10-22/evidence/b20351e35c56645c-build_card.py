#!/usr/bin/env python3
"""Render the filed account from completed computations; no result hand-entry."""
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from thermal48 import evaluate

B=Path(__file__).resolve().parent
def load(name): return json.loads((B/name).read_text())
def dump(name,obj): (B/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+"\n")
profiles={x["id"]:x for x in load("COATINGS.json")}
thermal={x["id"]:x for x in load("THERMAL-SCREEN.json")}
inputs=load("INPUTS.json")
validation=load("VALIDATION.json")
assert validation["passed"]
additional=load("ADDITIONAL-AUDIT.json")
assert additional["passed"]
data={name:load("RESULTS-"+name+".json") for name in ["MLCCAg","CCAg","AgFEP05","AgFEP1"]}
assert all(x["complete"] for x in data.values())
rows=[row for d in data.values() for row in d["rows"]]
index={(x["profile"],x["R_m"],x["weather"],x["floor"],x["drying"],
        x["external_water_kg_m2"]):x for x in rows}
def row(name="MLCCAg",r=10,weather="ISA",floor=True,route="bake70",water=.1):
    return index[name,r,weather,floor,route,water]
def point(*args,**kw): return row(*args,**kw)["two_factor_endpoint"]
def leastlabel(x):
    p=x["least"]["least"]
    if p is None: return "none"
    letters={0:"G",1:"Q",2:"E/F",3:"F"}
    name="+".join(letters[j] for j in range(4) if p["mask"]&(1<<j))
    return f"{name} {p['usage']:.6f}"
def fmt(n,d=3): return "unknown" if n is None else f"{n:,.{d}f}"

# Full flat review table, including actual/floor, weather and dry-exterior rows.
fields=["id","profile","R_m","weather","floor","drying","external_water_kg_m2",
        "endpoint_payload_kg","endpoint_tf_mm","endpoint_tc_mm",
        "endpoint_edge_SF","endpoint_pressure_Pa","least_axes","least_usage",
        "least_gamma","least_Q","least_E_GPa","least_film_kg_m2_interface",
        "least_tf_mm","least_tc_mm","least_installed_SF"]
with (B/"ROWS.csv").open("w",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
    for x in rows:
        p=x["two_factor_endpoint"];l=x["least"]["least"]
        d={k:x[k] for k in fields[:7]}
        d.update(endpoint_payload_kg=p["signed_payload_kg"],
                 endpoint_tf_mm=p["geometry"]["tf_m"]*1000,
                 endpoint_tc_mm=p["geometry"]["tc_m"]*1000,
                 endpoint_edge_SF=p["modes"]["thermal_core_interface_screen"],
                 endpoint_pressure_Pa=p["vacuum"]["hot_pressure_24h_upper_Pa"],
                 least_axes="none" if l is None else "+".join(l["selected_axes"]),
                 least_usage=None if l is None else l["usage"],
                 least_gamma=None if l is None else l["properties"]["gamma"],
                 least_Q=None if l is None else l["properties"]["Q"],
                 least_E_GPa=None if l is None else l["properties"]["E_Pa"]/1e9,
                 least_film_kg_m2_interface=None if l is None else l["properties"]["film_kg_m2_interface"],
                 least_tf_mm=None if l is None else l["geometry"]["tf_m"]*1000,
                 least_tc_mm=None if l is None else l["geometry"]["tc_m"]*1000,
                 least_installed_SF=None)
        writer.writerow(d)
dump("RESULTS.json",dict(
    tag="QUESTIONABLE / PROJECTION",complete=True,configurations=len(rows),
    started_at=inputs["started_at"],calculation_finished_at=max(x["finished_at"] for x in data.values()),
    rows=rows,model_scope="040 account with finish-specific thermal tables, explicit structural primer and extra material water.",
    installed_hull_SF=None))

sens=load("SENSITIVITIES.json")
screen_sens=[]
for label,alpha,epsilon in [
        ("wet_optics_assumed",.20,.95),
        ("aged_alpha015_assumed",.15,.80),
        ("aged_alpha020_assumed",.20,.80)]:
    t=evaluate(10,[.022106790073532958],n=37,midpoint=True,
               fixed_iterations=25,legacy_project=True,solid_density=2640,
               alpha_out=alpha,epsilon_out=epsilon)
    factor=12.3e-6*math.sqrt(290e9*.000799676281908861*46884349.59354485/.022106790073532958)
    day=241316.50526089262/(factor*abs(t["rise_K"][0]))
    cycle=241316.50526089262/(factor*abs(t["swing_K"][0]))
    screen_sens.append(dict(id=label,alpha=alpha,epsilon=epsilon,
                           legacy_day_SF=day,legacy_cycle_SF=cycle,
                           meets_finish_screen=day>=1.678 and cycle>=1))
dump("OPTICAL-SENSITIVITY-SCREEN.json",screen_sens)

old=json.loads((Path(inputs["base_model"])/"RESULTS.json").read_text())
oldindex={(x["R_m"],x["weather"],x["floor"]):x for x in old["rows"]
          if x["pad"]=="heavy70" and x["vented"]}
base=oldindex[10,"ISA",True]["two_factor_endpoint"]
p=point()
delta={k:base["bill_kg"].get(k,0)-p["bill_kg"].get(k,0)
       for k in set(base["bill_kg"])|set(p["bill_kg"])}
dump("R10-RECONCILIATION.json",dict(
    original040_payload_kg=base["signed_payload_kg"],
    new_payload_kg=p["signed_payload_kg"],payload_gains_by_bill_term_kg=delta,
    total_gain_kg=sum(delta.values()),
    closure_error_kg=(p["signed_payload_kg"]-base["signed_payload_kg"])-sum(delta.values())))

cost=load("DRYING-COSTS.json")
costindex={(x["profile"],x["R_m"],x["route"]):x for x in cost["rows"]}
coating_table=[
 "| Finish | α / ε used | Nominal added mass, g/m² | 037 day SF | Full-cycle SF | Current 200 °F edge SF |",
 "|---|---:|---:|---:|---:|---:|"]
for c in profiles.values():
    t=thermal[c["id"]]
    if c["alpha"] is None:
        coating_table.append(f"| {c['name']} | unknown | unknown | unscored | unscored | unscored |")
    else:
        coating_table.append(f"| [{c['name']}]({c['source']}) | {c['alpha']:.3f} / {c['epsilon']:.3f} | "
          f"{fmt(None if c['areal_mass_kg_m2'] is None else 1000*c['areal_mass_kg_m2'],3)} | "
          f"{t['legacy_037_day_SF']:.3f} | {t['legacy_037_full_swing_SF']:.3f} | "
          f"{t['current_200F_minimum_edge_SF']:.3f} |")
comparison=["| Finish | Applied optical finish, kg at R10 | Dry-gas payload | Bake payload | Onboard-sorbent payload |",
            "|---|---:|---:|---:|---:|"]
for name in data:
    values=[point(name,route=route)["signed_payload_kg"] for route in ["dry_gas","bake70","desiccant"]]
    comparison.append(f"| {name} | {point(name)['bill_kg']['coating']:.3f} | "+" | ".join(f"{v:+.3f}" for v in values)+" |")
matrix=["| R, m | Weather | Dry gas: actual / floor | Bake: actual / floor | Sorbent: actual / floor |",
        "|---:|---|---:|---:|---:|"]
leasttable=["| R, m | Weather | Dry gas | Bake | Sorbent |",
            "|---:|---|---|---|---|"]
for r in [10,12,15]:
    for weather in ["ISA","optimistic","both"]:
        vals=[]
        for route in ["dry_gas","bake70","desiccant"]:
            vals.append(" / ".join(f"{point(r=r,weather=weather,floor=f,route=route)['signed_payload_kg']:+.3f}"
                                    for f in [False,True]))
        matrix.append(f"| {r} | {weather} | "+" | ".join(vals)+" |")
        leasttable.append(f"| {r} | {weather} | "+" | ".join(
            leastlabel(row(r=r,weather=weather,route=route))
            for route in ["dry_gas","bake70","desiccant"])+" |")

costtable=["| R, m | Route | Material water before → aboard, kg | Exterior water aboard, kg | Added bed/cartridge, kg | Ground resource scenario |",
           "|---:|---|---:|---:|---:|---|"]
for r in [10,12,15]:
    for route in ["dry_gas","bake70","desiccant"]:
        x=costindex["MLCCAg",r,route]
        ground=(f"{x['dry_gas_five_exchanges_m3']:,.0f} m³ / {x['dry_gas_nitrogen_kg']:,.0f} kg N₂"
                if route=="dry_gas" else
                f"≥{x['ideal_bake_lower_bound_kWh']:.1f} kWh ideal heat"
                if route=="bake70" else "regeneration/equipment unsourced")
        costtable.append(f"| {r} | {route} | {x['material_water_initial_kg']:.3f} → "
            f"{x['material_water_remaining_kg']:.3f} | {x['external_water_remaining_kg']:.3f} | "
            f"{x['sorbent_and_cartridge_kg']:.3f} | {ground} |")

evidence=load("COATING-EVIDENCE.json")
evlines=["# Finish durability and Be adhesion evidence",
         "",
         "QUESTIONABLE / PROJECTION. “Unknown” is not a pass. Exact source links and optical/mass values are in COATINGS.json and SOURCE-AUDIT.md.",
         "",
         "| Finish | UV evidence | Humidity / water evidence | Be adhesion |",
         "|---|---|---|---|"]
for x in evidence:
    evlines.append(f"| [{x['id']}]({x['source']}) | {x['UV']} | {x['humidity']} | {x['adhesion_on_Be']} |")
(B/"COATING-EVIDENCE.md").write_text("\n".join(evlines)+"\n")

drycondition=["| Finish | R10 ISA, no exterior water | R10 optimistic, no exterior water | R10 both, no exterior water |",
              "|---|---:|---:|---:|"]
for name in data:
    drycondition.append(f"| {name} | "+" | ".join(
        f"{point(name,weather=w,water=0)['signed_payload_kg']:+.3f}"
        for w in ["ISA","optimistic","both"])+" |")
internal=costindex["MLCCAg",10,"bake70"]
bed=costindex["MLCCAg",10,"desiccant"]
limits=sens["optical_limits_at_037_geometry"]
screenrows=["| Assumed optical case | 037 day / full-cycle SF | R10 ISA endpoint, kg | Meets both finish screens? |",
            "|---|---:|---:|---|"]
for t in screen_sens:
    x=next(x for x in sens["rows"] if x["type"]==t["id"] and x["R_m"]==10 and x["weather"]=="ISA")
    screenrows.append(f"| {t['id']} ({t['alpha']}/{t['epsilon']}) | {t['legacy_day_SF']:.3f} / "
         f"{t['legacy_cycle_SF']:.3f} | {x['endpoint']['signed_payload_kg']:+.3f} | "
         f"{'yes, in this model' if t['meets_finish_screen'] else 'no'} |")
nf=load("NFI.json")

card=f"""# MAINLINE-048 — coating and retained water

**QUESTIONABLE / PROJECTION. R10 floats again in the selected ISA account if a sufficiently light finish achieves the assumed optics and the 037b cure repair works. The mass recovery comes chiefly from replacing the 0.20 kg/m² coating allowance. The existing exterior-water debit remains aboard. No installed-hull safety factor is established.**

The lightest source-described recipe screened here is multilayer CCAg/ITO, calculated at 7.5752 g/m² before an assumed 10% application allowance. Its optical pair is transferred from NASA's coating class to this recipe and Be, so it is a candidate, not a qualified lightest finish. The more directly paired classical CCAg recipe is 9.326–11.179 g/m²; a catalog Ag/FEP tape including adhesive is 88 g/m² at 0.5 mil. White-paint thickness data do not establish their installed mass. Sources and unresolved transfers are detailed in [SOURCE-AUDIT.md](SOURCE-AUDIT.md).

The three drying routes below share R10 ISA, the retained joining floor, heavy pad, vented core, 100 kg systems and 10 g/m² additional structural primer. Only the bake column assumes 90% removal of added material water:

{chr(10).join(comparison)}

Payloads are kilograms at 028b's endpoints. The original 040 row was **{base['signed_payload_kg']:+.3f} kg**. The selected multilayer case is **{p['signed_payload_kg']:+.3f} kg**; its exterior water is still **{p['bill_kg']['water']:.3f} kg**. Coating replacement saves {delta['coating']:.3f} kg, the new structural primer costs {-delta['structural_primer']:.3f} kg, added residual material water costs {-delta['absorbed_water']:.3f} kg, and the changed thermal/geometry/joining terms supply the remaining {sum(delta[k] for k in ['faces','core','charged_joining']):+.3f} kg. Exact closure is in [R10-RECONCILIATION.json](R10-RECONCILIATION.json).

## Finish screen

{chr(10).join(coating_table)}

Masses above are nominal coating/tape values, before the declared application allowance and separate structural primer. Structural primer is charged outside the original four-component joining/floor bill. Classical CCAg's full recipe band is 9.326–11.179 g/m². The SolarWhite α interpretation is unresolved because its web heading says reflectance. The SiOx/polyimide construction has no sourced installed mass. Bare Be is the historical chemically polished surface, not a durable outdoor optical specification.

The first factor reproduces 037's day comparison at its original geometry and typical shear strength. The second explicitly spans the hot day to cold night. The last uses the current 037b 200 °F cure-reference model and minimum-strength core shear; these factors are not interchangeable. The declared finish screen is day ≥1.678 **and** full-cycle ≥1. Only the sourced optical assumptions, not qualification, are being screened. Full UV, humidity and Be-adhesion findings for every candidate are in [COATING-EVIDENCE.md](COATING-EVIDENCE.md). Space heritage or base-film weathering does not establish complete atmospheric-hull life.

## What the water account represents

040 → 033 → 028b/019 → 016 traces the exterior debit to an **assumed 0.1 mm retained liquid film**, selected from 016's 0.1–1 mm band. At water density 1000 kg/m³, this is 0.1 kg/m²: 125.664, 180.956 and 282.743 kg at R10, R12 and R15. It is not adhesive moisture. Baking or an internal bed cannot remove later exterior dew or rain.

Historical AF163-2U records have WVR 0.09–0.20%, distinct from TML 2.59–4.85%. WVR follows a specified vacuum test and 24-hour humidity exposure; it is not the chosen 200 °F cure's equilibrium moisture uptake. The main added-water proxy uses 0.20%. Core, structural-primer, seam-polymer and deposited-finish uptake remain assumed. FEP base-film absorption is sourced below 0.01%; the complete PSA construction is not. The severe 9.16% adhesive sensitivity comes from different AF163-2M specimens immersed at 70 °C and is not treated as 2U room-humidity data. [Moisture sources and definitions](SOURCE-AUDIT.md).

The new material inventory is charged above nominal dry/reference masses without removing nominal adhesive TML. It also retains 040's nominal volatile-pressure allowance; nominal mass/moisture baselines still need measurement.

{chr(10).join(costtable)}

These are primary multilayer ISA endpoint geometries with the retained joining floor. At R10, the bake scenario removes only {internal['material_water_removed_ground_kg']:.3f} kg of this added material water, leaving {internal['material_water_remaining_kg']:.3f} kg. The onboard bed adds {bed['sorbent_and_cartridge_kg']:.3f} kg while retaining the water aboard. External film dominates both.

The bake's 90% reduction is an **acceptance target requiring measurement**, not a demonstrated duration or process. Heat figures are ideal lower bounds with stated engineering heat-capacity assumptions, excluding tooling, pumping, losses and binding energy. Five hull-volume nitrogen exchanges are a hypothetical ground-enclosure cost; smaller panel/glovebox assembly changes it. Dry-gas assembly receives no removal credit for pre-existing material water. Bed capacity/capture at vacuum are projections. No financial quote or achieved cycle time is sourced. Details and by-material inventories are in [DRYING-COSTS.json](DRYING-COSTS.json).

## R10, R12 and R15 account

The following uses the lightest recipe candidate, retains 0.1 kg/m² exterior water, and carries every 040 primary debit. Each cell gives **actual joining / retained joining floor** endpoint payload in kg.

{chr(10).join(matrix)}

Least named optimism sets with the retained floor follow. G=global coefficient, Q=wrinkling factor, F=film weight, E/F=coupled face-material tuple. Numbers are the common normalized logarithmic usage, with 0=today and 1=declared endpoint. Selection minimizes axis count first, then common usage. `none` means no floating solution within the four stated endpoints, not impossibility under every design.

{chr(10).join(leasttable)}

For R10 ISA bake, the least point uses {leastlabel(row())}: gamma={row()['least']['least']['properties']['gamma']:.6f}, Q={row()['least']['least']['properties']['Q']:.6f}, film={row()['least']['least']['properties']['film_kg_m2_interface']:.8f} kg/m²/interface, E=290 GPa. The selected geometry and every individual coefficient are in [ROWS.csv](ROWS.csv) and [RESULTS.json](RESULTS.json). Those files include all 432 configurations, both joining conventions, all three drying routes, all four selected finishes, weather cases, endpoints, subset trials and least sets.

R10's retained-water optimistic-weather and both-weather rows remain negative even with the light deposited finish. R12's optimistic-weather rows can become positive; both-weather remains negative throughout R10–15 in this account. These remain coupled mass/scalar-model statements, not mission qualification.

## Conditional dry operations and robustness

Deleting the exterior-water layer is a separate dry-operating assumption. It is **not** a result of the bake. Under the bake route and retained joining floor, it gives:

{chr(10).join(drycondition)}

At R10 ISA the multilayer bake endpoint can carry up to {internal['external_water_max_for_endpoint_float_kg_m2']:.6f} kg/m² exterior water within the same dry-optics model, equivalent to {internal['external_water_max_for_endpoint_float_kg_m2']:.6f} mm of water. That is a mass threshold, not a drainage prediction. The inherited 1 kPa vapor pressure gives a dew point of {cost['dewpoint_at_1kPa_K']:.2f} K; the modeled dry-night surfaces are colder. Condensation/frost and wet optical properties therefore remain explicit open issues.

{chr(10).join(screenrows)}

A positive current-account payload in the table does not cure a failed legacy full-cycle finish screen. At ε=.80, the source-geometry day/full-cycle screen permits α only up to about {next(x['maximum_alpha_for_day_and_cycle'] for x in limits if x['epsilon']==.8):.6f}. That is a model aging limit, not an observed lifetime.

Other R10 ISA sensitivities are in [SENSITIVITIES.json](SENSITIVITIES.json). The multilayer margin survives 50 g/m² structural primer and the declared scalar scarf/edge interaction, but the 0.5 mil tape margin does not. At the high-uptake/no-extra-drying sensitivity, that tape is slightly negative. The maximum classical recipe remains positive. Changing back to the original 250 °F cure and 30:1 scarf produces no geometry passing the retained minimum-strength edge screen for any of the four finishes; optical improvement does not replace the 037b cure fix.

Using an assumed hemispherical ε=.40 for classical CCAg, while keeping its deposited mass, gives R10 ISA payload {additional['classical_low_emittance_sensitivity']['endpoint']['signed_payload_kg']:+.3f} kg. This is a robustness sensitivity for the unresolved emittance statistic, not a measured CCAg property.

## Verification and remaining qualifications

Validation passed **{validation['checks']:,} checks** across **{validation['unique_points']:,} distinct stored points** and 432 configurations: independent mass/pressure/mode calculations, original-040 regression, denser primary geometry searches, direct 256-point thermal solves and favorable bounds for the nonmonotone face-material axis. [VALIDATION.json](VALIDATION.json) records tolerances and failures; [METHOD.md](METHOD.md) gives equations, conventions and reproduction steps.

All eight selected four-axis points also underwent an independent E-usage scan and bounded refinement at their minimax ceilings. None improved payload by 0.002 kg; numerical search scope is recorded in [ADDITIONAL-AUDIT.json](ADDITIONAL-AUDIT.json).

The service audit checks refined cavity volume, zero sorbent capture and removal of the inherited nominal-conditioning assumption. These calculations do not validate leaks, cure, sorption or process performance. All 040 qualifications remain, along with {len(nf['findings'])} new material/process findings in [NFI.json](NFI.json). The relevant gates are matched coating mass/optics and life, Be adhesion, actual material-water inventory, the 200 °F cure/primer process, gamma/Q/film qualification, joints, venting and the combined weather/thermal/water mission. **Installed-hull SF remains unknown.**

![Conditional payload and onboard water accounting](ACCOUNT.png)

The brief is complete. Stop and file; the robotics seat supplies any next job.
"""
(B/"CARD.md").write_text(card)

plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
fig,axes=plt.subplots(1,2,figsize=(12,5.4))
colors={"040":"#6b7280","MLCCAg":"#0f766e","CCAg":"#2563eb","AgFEP05":"#b45309","AgFEP1":"#a21caf"}
for name in ["040","MLCCAg","CCAg","AgFEP05","AgFEP1"]:
    ys=[oldindex[r,"ISA",True]["two_factor_endpoint"]["signed_payload_kg"] if name=="040"
        else point(name,r=r)["signed_payload_kg"] for r in [10,12,15]]
    axes[0].plot([10,12,15],ys,marker="o",label=name,color=colors[name],
                 linestyle="--" if name=="040" else "-")
axes[0].axhline(0,color="#111827",lw=.8)
axes[0].set(xlabel="Radius (m)",ylabel="Endpoint payload (kg)",
            title="ISA · bake assumption · retained joining floor\nExterior water: 0.1 kg/m²")
axes[0].set_xticks([10,12,15]);axes[0].legend(frameon=False)
labels=["Dry-gas\nassembly","70 °C bake\nassumption","Onboard\nsorbent"]
cs=[costindex["MLCCAg",10,route] for route in ["dry_gas","bake70","desiccant"]]
x=np.arange(3);outer=np.array([c["external_water_remaining_kg"] for c in cs])
inside=np.array([c["material_water_remaining_kg"] for c in cs])
bedmass=np.array([c["sorbent_and_cartridge_kg"] for c in cs])
axes[1].bar(x,outer,color="#93c5fd",label="Exterior liquid")
axes[1].bar(x,inside,bottom=outer,color="#1d4ed8",label="Extra material water")
axes[1].bar(x,bedmass,bottom=outer+inside,color="#7c3aed",label="Dry bed + cartridge")
axes[1].set_xticks(x,labels);axes[1].set(ylabel="Carried mass (kg)",
        title="R10 multilayer finish · water stays separate")
axes[1].legend(frameon=False,loc="upper left")
axes[1].set_ylim(0,210)
fig.suptitle("MAINLINE-048 — conditional model results, installed qualification open",fontsize=13)
fig.text(.5,.015,"Bake energy/equipment are ground costs. Source-recipe optics and Be installation remain projections.",
         ha="center",fontsize=9,color="#374151")
fig.tight_layout(rect=(0,.05,1,.94))
fig.savefig(B/"ACCOUNT.png",dpi=180)
fig.savefig(B/"ACCOUNT.pdf")
plt.close(fig)
dump("SUMMARY.json",dict(
    tag="QUESTIONABLE / PROJECTION",primary_R10_ISA_floor_endpoint=p,
    primary_R10_ISA_floor_least=row()["least"]["least"],
    configurations=len(rows),validation=validation,
    source_recipe_lightest_qualified=False,overall_installed_hull_SF=None,
    finished_at=datetime.now(timezone.utc).isoformat()))
print("Rendered CARD, RESULTS, ROWS, evidence, reconciliation, summary and figure.")
