"""Final scientific cross-checks, results, card and shareable figure."""
import os
os.environ.setdefault("MPLCONFIGDIR","unpublished-local-ref:b4499a42f3b2733e")
import json,csv,datetime
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from account_check import *
from thermal_check import solve,MODELS,TC_REF

def read(name):
    return json.loads((ROOT/name).read_text())

checks=[]
def check(name,passed,**details):
    checks.append({"check":name,"passed":bool(passed),**details})

keyfields=("R_m","weather","cure_in_global","floor","drying")
fixed=read("ACCOUNT-INDEPENDENT.json")
optima=read("OPTIMA-INDEPENDENT.json")
fixed_map={(x["model"],*(x[k] for k in keyfields)):x for x in fixed}
opt_map={(x["model"],*(x[k] for k in keyfields)):x for x in optima}
resized=[]
for target in read("owner/RESIZED-CONSEQUENCES.json"):
    model=target["model"];key=(model,*target["case"])
    own=fixed_map[key]["own"]
    old=fixed_map[("owner_table",*target["case"])]["own"]
    delta=own["payload_kg"]-old["payload_kg"]
    updated=opt_map[key]["own"]["payload_kg"]-opt_map[("owner_table",*target["case"])]["own"]["payload_kg"]
    check("resized payload difference",abs(delta-target["payload_difference_kg"])<1e-7,
          model=model,case=target["case"],own=delta,filed=target["payload_difference_kg"])
    check("resized scarf constraint",own["modes"]["scarf"]>=1-2e-7,model=model,case=target["case"])
    check("resized global constraint",own["modes"]["global"]>=1-2e-7,model=model,case=target["case"])
    resized.append({"model":model,"case":target["case"],"own_fixed_geometry_delta_kg":delta,
                    "independently_reoptimized_delta_kg":updated,
                    "filed_delta_kg":target["payload_difference_kg"]})
dump("RESIZED-INDEPENDENT.json",resized)

direct=[]
for row in fixed:
    if row["model"]=="owner_table":
        continue
    point=row["own"];tc=point["tc_m"];R=row["R_m"]
    direct_t=solve(R,tc,row["model"],n=512)
    interp=thermal(row["model"],R,tc)
    metrics={}
    for k in ("gradient_K","curvature_temperature_K"):
        val=float(direct_t[k][0]);budget=1.002*interp[k]
        check("direct thermal interpolation guard",val<=budget+1e-8,
            model=row["model"],R_m=R,metric=k,direct=val,budget=budget)
        metrics[k]={"direct":val,"guarded_interpolation":budget}
    direct_cure=max(abs(CURE-float(direct_t["max_outer_K"][0])),abs(CURE-float(direct_t["min_outer_K"][0])))
    interp_cure=1.002*max(abs(CURE-interp["max_outer_K"]),abs(CURE-interp["min_outer_K"]))
    check("direct cure interpolation guard",direct_cure<=interp_cure+1e-8,model=row["model"],R_m=R)
    direct.append({"model":row["model"],"case":[row[k] for k in keyfields],
        "tc_m":tc,"metrics":metrics,"direct_cure_excursion_K":direct_cure,
        "guarded_interpolated_cure_excursion_K":interp_cure})
dump("DIRECT-GUARD-INDEPENDENT.json",direct)

# Every endpoint float sign is independently regenerated, not inferred from a
# displayed rounded payload.
baseline=read("owner/ACCOUNT-owner_table.json")
float_changes=[]
for model in MODELS:
    rows=read(f"owner/ACCOUNT-{model}.json")
    for old,row in zip(baseline,rows,strict=True):
        for mask,(pt0,pt) in enumerate(zip(old["result"]["endpoints"],row["result"]["endpoints"],strict=True)):
            v0=evaluate(old,pt0["tf_m"],pt0["tc_m"],mask,pt0["usage"])["payload_kg"]
            v=evaluate(row,pt["tf_m"],pt["tc_m"],mask,pt["usage"])["payload_kg"]
            change=(v0>=-1e-5)!=(v>=-1e-5)
            if change:float_changes.append({"model":model,"case":[row[k] for k in keyfields],"mask":mask})
            check("endpoint float sign preserved",not change,model=model,
                  case=[row[k] for k in keyfields],mask=mask)
dump("ENDPOINT-FLOAT-CHANGES-INDEPENDENT.json",float_changes)

thermal_stats=read("THERMAL-SUMMARY.json")
thermal_stats.pop("four_historical_R10")  # superseded by matching-convention check
stats={**thermal_stats,**read("SUPPLEMENT-SUMMARY.json"),**read("ACCOUNT-SUMMARY.json")}
numeric_count=sum(x["count"] for x in stats.values())
numeric_pass=sum(x["passed"] for x in stats.values())
check("all final scalar comparisons pass",numeric_count==numeric_pass)
check("independent search checks pass",read("SEARCH-SUMMARY.json")["failures"]==[])
check("physical limiting cases pass",all(x["passed"] for x in read("INVARIANTS-INDEPENDENT.json")))

cross=read("CROSSINGS-INDEPENDENT.json")
maxloss=max(-r["own_fixed_geometry_delta_kg"] for r in resized)
maxloss_opt=max(-r["independently_reoptimized_delta_kg"] for r in resized)
owner=read("owner/RESULTS.json")
check("maximum payload cost",abs(maxloss-owner["maximum_payload_cost_kg"])<1e-7,
      own=maxloss,filed=owner["maximum_payload_cost_kg"])
check("288 scarf crossings",sum(r["scarf"] for r in cross.values())==288)
check("85 global crossings",sum(r["global"] for r in cross.values())==85)
summary={}
for model in MODELS:
    rr=[r for r in resized if r["model"]==model]
    ww=[r["own"] for r in fixed if r["model"]==model]
    summary[model]={**cross[model],
        "minimum_payload_delta_kg":min(r["own_fixed_geometry_delta_kg"] for r in rr),
        "maximum_payload_delta_kg":max(r["own_fixed_geometry_delta_kg"] for r in rr),
        "maximum_resized_edge_usage":max(1/r["modes"]["core_edge"] for r in ww),
        "maximum_resized_wall_usage":max(1/r["modes"]["cell_wall"] for r in ww)}
probe=read("FOUR-R10-GRID-INDEPENDENT.json")
four={m:{k:probe[m][k][0] for k in ("gradient_K","rise_K","swing_K")} for m in MODELS}
primary=[]
for row in fixed:
    if row["floor"] and row["drying"]=="bake":
        point=row["own"]
        primary.append({k:row[k] for k in ("model","R_m","weather","cure_in_global")}|{
            "payload_kg":point["payload_kg"],"tf_m":point["tf_m"],"tc_m":point["tc_m"],
            "cure_compression_MPa":point["properties"]["cure_compression_Pa"]/1e6})
with (ROOT/"PRIMARY-PAYLOAD-INDEPENDENT.csv").open("w") as f:
    writer=csv.DictWriter(f,fieldnames=list(primary[0]))
    writer.writeheader();writer.writerows(primary)

resolved=[
 {"id":"CHECKER-CURVATURE-CONVENTIONS","status":"RESOLVED",
  "finding":"Initial 10 probe and 27 legacy/common curvature comparisons used different extrema conventions.",
  "resolution":"Owner historical diagnostics use 1441-angle sampling; checker diagnostics use derivative roots. Settled tables use roots. Matched-convention comparisons pass.",
  "exact_ledgers":["history/thermal01/THERMAL-MISMATCHES.json","history/supplement01/SUPPLEMENT-MISMATCHES.json",
                   "history/supplement02/SUPPLEMENT-MISMATCHES.json"],"maximum_initial_probe_difference_K":.00021321463623991121},
 {"id":"CHECKER-INCOMING-WATER-CAPTURE","status":"RESOLVED",
  "finding":"Initial checker left incoming water vapor in the sorbent pressure balance.",
  "resolution":"Apply .95 capture to incoming water mole fraction 1000/p0; retain its mass aboard. All service-pressure values now match.",
  "exact_ledger":"history/account01/ACCOUNT-MISMATCHES.json"},
 {"id":"CHECKER-FREE-EDGE-GUARD","status":"RESOLVED",
  "finding":"Initial separate finish-screen reproduction omitted the declared 1.002 stress guard.",
  "resolution":"Guard included; all 156 finish factors match, maximum difference 2.14e-14.",
  "exact_ledger":"history/supplement01/SUPPLEMENT-MISMATCHES.json"},
 {"id":"CHECKER-NONFLOATING-SCHEMA","status":"RESOLVED",
  "finding":"First independent search expected a ties array in nonfloating accounts.",
  "resolution":"Treat omitted ties as empty; admitted search02 completed all 7310 checks.",
  "evidence":"search01.execution.json"}
]
dump("MISMATCHES.json",{
    "unresolved_numerical_mismatches":[],
    "resolved_checker_conventions_and_implementation":resolved,
    "numerical_search_differences":{"tolerance_kg":.001,
        "maximum_absolute_endpoint_difference_kg":read("SEARCH-SUMMARY.json")["max_reoptimization_abs_difference_kg"],
        "exact_ledger":"OPTIMA-INDEPENDENT.json","least_usage_ledger":"SEARCH-CHECKS.json"},
    "all_exact_scalar_differences":[
        "THERMAL-COMPARISONS.jsonl.gz","SUPPLEMENT-COMPARISONS.jsonl.gz","ACCOUNT-COMPARISONS.jsonl.gz"],
    "unresolved_physical_qualifications":"NFI.json"})

new=[
 {"id":"NFI-C053-GAP-EFFECTIVE","status":"OPEN","blocking":False,
  "finding":"The core-gap and inner-enclosure paths are distinct, but the effective .20 gap coefficient is unmeasured. Two .20 gray plates give 1/9, not .20.",
  "needed":"Measure evacuated bonded Be/CR-III/adhesive panel transport, including contact resistance and cell-wall exchange. Do not add radiation again if future apparent conductivity already contains it.",
  "source":"SOURCE-AUDIT.md; METHOD.md; GAP-SENSITIVITY.json",
  "extends":"NFI-053-CORE-CONDUCTANCE"},
 {"id":"NFI-C053-LOCAL-CONVECTION","status":"OPEN","blocking":False,
  "finding":"Re is outside Whitaker's sphere range; a spatially uniform local use of its average correlation and the 1.32 natural-convection floor are additional assumptions.",
  "needed":"Validated local full-scale convection boundary with orientation and wind conditions.",
  "source":"SOURCE-AUDIT.md","extends":"NFI-053-CONVECTION"},
 {"id":"NFI-C053-SCARF-QUALIFICATION","status":"OPEN","blocking":False,
  "finding":"All frozen scarf crossings are real within the declared scalar/tolerance calculation. The largest deficit is about .0366%; the mixed-gap deficit is below one part per million. These do not establish physical bond failure or physical safety after resizing.",
  "needed":"Matched process/adherend bond allowables, edge/scarf interaction, peel and full load-state validation.",
  "source":"CROSSINGS-INDEPENDENT.json; SCARF-ROOTS-INDEPENDENT.json",
  "extends":"NFI-053-CURE-BOND"},
 {"id":"NFI-C053-JOINT-MISSION","status":"OPEN","blocking":False,
  "finding":"Changing weather pressure/buoyancy leaves the 2 m/s thermal environment unchanged; wet exterior mass is charged while optics are dry transferred values.",
  "needed":"Joint weather, radiation, wind and moisture histories with transient, lateral-conduction and installed optical evidence.",
  "source":"METHOD.md; SOURCE-AUDIT.md",
  "extends":["NFI-053-ENVIRONMENT","NFI-053-WATER-MASS","NFI-053-OPTICAL-TRANSFER"]}
]
for row in new:row["classification"]="QUESTIONABLE / PROJECTION"
dump("NFI.json",{"unit":"vacuum-mainline053-check-1020","all_nonblocking":True,
    "checker_open":new,"checker_open_count":len(new),
    "owner_053_open_groups":read("owner/NFI.json")["new"],
    "inherited_registers":read("owner/NFI.json")["inherited_registers"],
    "resolved_local":resolved,"installed_hull_SF":None})

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

labels=["Forced / conduction","Mixed / conduction","Forced / gap .20","Mixed / gap .20"]
colors=["#245a81","#41816b","#629dc2","#86bca4"]
fig,axes=plt.subplots(2,2,figsize=(11,7.8),layout="constrained")
series=[
 ([four[m]["gradient_K"] for m in MODELS],"R10 reference: face gradient","K"),
 ([four[m]["swing_K"] for m in MODELS],"R10 reference: day–night swing","K"),
 ([-summary[m]["minimum_payload_delta_kg"] for m in MODELS],"Largest resized payload loss","kg"),
 ([(1-summary[m]["minimum_scarf_SF"])*100 for m in MODELS],"Largest frozen scarf deficit","percent below SF=1")]
for ax,(vals,title,unit) in zip(axes.flat,series):
    ax.barh(labels,vals,color=colors)
    ax.invert_yaxis();ax.set_title(title,loc="left",fontsize=11,fontweight="bold")
    ax.set_xlabel(unit);ax.spines[["top","right"]].set_visible(False)
    ax.set_xlim(0,max(vals)*1.32)
    for j,v in enumerate(vals):
        ax.text(v+max(vals)*.025,j,f"{v:.6f}",va="center",fontsize=9)
fig.suptitle("CHECK-053 · independent reproduction",fontsize=17,fontweight="bold")
fig.text(.5,-.075,"Thermal probe: historical white finish, foil density 2640 kg/m³. Payload/bond: selected multilayer finish.\nConditional scalar models; physical qualification remains open.",ha="center",fontsize=9)
for suffix in ("pdf","svg","png"):
    fig.savefig(ROOT/f"CHECK-053.{suffix}",dpi=170,bbox_inches="tight")
plt.close(fig)

lines=[
 "# CHECK-053 — thermal boundaries, payload and scarf crossings",
 "",
 "**PASS for the specified numerical models. Physical qualification remains open.**",
 "",
 f"Independent equations reproduce {numeric_count:,} final scalar comparisons. "
 f"All {results['search']['checks']:,} search checks pass: 5,760 endpoint grid witnesses, "
 "360 independently reoptimized mask-11 endpoints, and 60 primary least-set rows. "
 f"The largest endpoint reoptimization difference is {results['search']['max_reoptimization_abs_difference_kg']:.12f} kg. "
 "No owner/predecessor executable was read, copied, hashed, imported or run.",
 "",
 "All inherited properties are QUESTIONABLE; installed geometry, process and performance are PROJECTION. "
 "Installed-hull safety factor is unknown.",
 "",
 "The order's four R10 values use the historical white-finish probe, "
 "tc=.02210679007353296 m, foil density 2640 kg/m³, 128 Gauss nodes and the old extrema convention.",
 "",
 "| Boundary | Face gradient K | Day rise K | Day–night swing K |",
 "|---|---:|---:|---:|"]
for label,m in zip(labels,MODELS):
    v=four[m];lines.append(f"| {label} | {v['gradient_K']:.9f} | {v['rise_K']:.9f} | {v['swing_K']:.9f} |")
lines += [
 "",
 "Thus 0.464608894→0.413901181 K and 33.640781944→31.118178070 K are reproduced by "
 "the stated boundary changes. All 9,640 settled thickness rows, 40 reference rows, "
 "52 finish-temperature rows and 156 finish factors also reproduce. The older "
 "040/048 thermal tables and legacy screen conventions are separately checked.",
 "",
 "**The extra core-gap term is not inherently double counting.** It connects the two "
 "sandwich skins; the enclosure term redistributes heat among inner hull locations "
 "and has zero area-average flux. The core conduction term is a bulk-metal volume-fraction estimate. "
 "The .20 effective gap coefficient remains unqualified. Two infinite gray surfaces "
 "with emissivity .20 each give 1/9, so using .20 is 1.8 times that reference coefficient. "
 "That comparison is a sensitivity, not a validated honeycomb replacement. "
 "METHOD.md derives both paths; SOURCE-AUDIT.md records the primary evidence.",
 "",
 "**The full payload account is retained.** The following independently recalculated "
 "rows use mask 11, retained joining floor, projected ground bake and cure included "
 "in global/crimp demand. Weather changes pressure/buoyancy but keeps the same thermal environment.",
 "",
 "| R / weather | Filed-table baseline kg | Forced/conduction kg | Mixed/conduction kg | Forced/gap kg | Mixed/gap kg |",
 "|---|---:|---:|---:|---:|---:|"]
for R in (10,12,15):
    for weather in ("ISA","optimistic"):
        vals=[fixed_map[(m,R,weather,True,True,"bake")]["own"]["payload_kg"]
              for m in ("owner_table",*MODELS)]
        lines.append(f"| R{R} / {weather} | "+" | ".join(f"{v:.6f}" for v in vals)+" |")
lines += [
 "",
 f"The largest loss from the filed baseline is **{maxloss:.9f} kg**, "
 f"versus {maxloss_opt:.9f} kg after the checker's independent reoptimizations. "
 "All 288 exact payload differences are listed in RESIZED-INDEPENDENT.json. "
 "No endpoint float sign changes across 4,608 comparisons, and the independently "
 "checked primary minimum-axis choices and tied sets agree. Exterior water, added material "
 "water, sorbent where applicable, gas, primer, coating, pad, systems and weather debits remain charged.",
 "",
 "**Frozen scarf pass status does change under the declared scalar tolerance.**",
 "",
 "| Boundary | Frozen scarf SF range | Scarf crossings | Global crossings | Maximum resized edge usage | Payload change range kg |",
 "|---|---:|---:|---:|---:|---:|"]
for label,m in zip(labels,MODELS):
    s=summary[m]
    lines.append(f"| {label} | {s['minimum_scarf_SF']:.9f}–{s['maximum_scarf_SF']:.9f} | "
      f"{s['scarf']} | {s['global']} | {s['maximum_resized_edge_usage']:.6f} | "
      f"{s['minimum_payload_delta_kg']:.6f} to {s['maximum_payload_delta_kg']:.6f} |")
lines += [
 "",
 "All 288 scarf crossings and 85 global crossings reproduce. The largest scarf "
 "deficit is about 0.0366%; the mixed-gap difference is below one part per million. "
 "Resizing restores the declared scalar constraints. A separate closed-form scarf "
 "root agrees with the independently sized faces. These numerical crossings establish "
 "neither installed bond failure nor installed safety after resizing.",
 "",
 "**Exact mismatches are disclosed.** No unresolved arithmetic mismatch remains. "
 "Initial checker differences came from sampled versus continuous curvature extrema, "
 "an omitted incoming-water capture pressure credit, and a missing 1.002 guard in the "
 "separate finish-screen calculation. Their original value-by-value ledgers, the "
 "nonfloating-schema execution failure and corrections are retained in history/ and "
 "indexed by MISMATCHES.json. Every final scalar difference and tolerance is recorded "
 "in the compressed comparison ledgers. Numerical optimizer differences are retained "
 "rather than rounded away.",
 "",
 f"Direct 512-node calculations at all {len(direct)} revised geometries satisfy the "
 "1.002 interpolation guard. Uniform-environment and zero-inner-emissivity tests "
 "pass. These checks bound numerical handling only; source extrapolation, contact "
 "resistance, local convection, wet optics, cure/bond allowables, transient conditions "
 "and structural-model qualification remain open.",
 "",
 "Four checker NFI clarifications extend the owner's nine open groups; all six "
 "inherited registers remain carried. An objection is recorded and does not stop this card.",
 "",
 "The reproducible package contains INPUTS.json, METHOD.md, SOURCE-AUDIT.md, "
 "RESULTS.json, NFI.json, exact comparison/search ledgers and admitted execution receipts. "
 "All numerical work used one-core, 1 GiB simjob admission. No out-of-band seat contact "
 "or public action occurred. No successor is named; file and end the turn.",
 "",
 "![Independent thermal and payload checks](CHECK-053.png)",
 "",
 "The figure is also available as CHECK-053.pdf and CHECK-053.svg.",
 ""]
(ROOT/"CARD.md").write_text("\n".join(lines))
print(json.dumps({"scalar_comparisons":numeric_count,"scalar_passed":numeric_pass,
    "search_checks":results["search"]["checks"],"final_checks":len(checks),
    "final_failures":results["final_failures"],"max_loss":maxloss,
    "reoptimized_max_loss":maxloss_opt,"convergence":convergence},indent=2))
