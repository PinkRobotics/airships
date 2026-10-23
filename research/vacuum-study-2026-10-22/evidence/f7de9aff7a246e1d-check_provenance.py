"""Independent source-condition, conservation and headline coverage checks."""
from pathlib import Path
import json
import math
ROOT=Path(__file__).resolve().parent
def load(n):return json.loads((ROOT/n).read_text())
def write(n,x):(ROOT/n).write_text(json.dumps(x,indent=2,allow_nan=False)+"\n")
rs=load("INDEPENDENT-RECORDS.json")
audit=[]
def eq(row,field,owner,independent,tol=1e-6):
    ok=math.isclose(owner,independent,rel_tol=2e-10,abs_tol=tol) if isinstance(owner,(int,float)) and isinstance(independent,(int,float)) else owner==independent
    audit.append(dict(row=row,field=field,owner=owner,independent=independent,pass_=ok))
u40=load("intake/files_read/vacuum-mainline040-common-account-1020/RESULTS.json")["rows"]
u37={x["id"]:x for x in load("intake/files_read/vacuum-mainline040-fold-037b-1020/RESULTS.json")["rows"]}
coating=next(c for c in load("intake/supplement/vacuum-mainline048-coating-and-water-1020/COATINGS.json") if c["id"]=="MLCCAg")
for r in rs:
    for p in r["masks"]:
        row=f'{r["lead"]}/{r["source"]}/R{r["R_m"]}/{r["weather"]}/{r.get("floor",r.get("service"))}/{p["mask"]}'
        eq(row,"lift_mass_conservation",p["payload_kg"]+math.fsum(p["bill"].values()),p["lift_kg"])
        if r["lead"]=="P2":
            eq(row,"coating_recipe_and_existing_10pct",p["bill"]["coating"],4*math.pi*r["R_m"]**2*coating["areal_mass_kg_m2"]*1.1)
            eq(row,"primer_area_10g_m2",p["bill"]["structural_primer"],4*math.pi*r["R_m"]**2*.01)
            eq(row,"exterior_water_area_100g_m2",p["bill"]["water"],4*math.pi*r["R_m"]**2*.1)
        else:
            eq(row,"exterior_water_area_100g_m2",p["bill"]["exterior_water"],4*math.pi*r["R_m"]**2*.1)
for r in u40:
    if r["pad"]!="heavy70" or not r["vented"] or r["weather"] not in ["ISA","optimistic"]:continue
    for t in r["least"]["endpoint_trials"]:
        p=t["solution"];row="040/"+r["id"]+"/"+str(t["mask"])
        eq(row,"cure_temperature_K",p["settings"]["cure_temperature_K"],(200-32)*5/9+273.15)
        eq(row,"fixed_bond_model",p["settings"]["bond_model"],"compliant037b")
        if p["mask"]==u37[r["id"]]["fix"]["endpoint"]["mask"]:
            fix=u37[r["id"]]["fix"]["endpoint"]
            for k,v in fix["bill_kg"].items():eq(row,"037b_fix/bill/"+k,p["bill_kg"][k],v)
            eq(row,"037b_fix/payload_kg",p["signed_payload_kg"],fix["signed_payload_kg"])

base=load("INDEPENDENT-SUMMARIES.json")
claims=load("CARD-AND-ANCILLARY-AUDIT.json")
discrepancies=[]
for x in claims["rows"]:
    if not x["pass_"]:
        xx=dict(x,category="printed-rounding",owner_artifact="CARD.md")
        j=int(x["row"].split("row")[1])
        # The printed table omits the five P3 'both' rows.
        displayed=sorted([v for v in base["flat"] if v["weather"]!="both"],
                         key=lambda v:(v["lead"],v["weather"],v["R_m"]))
        f=displayed[j]
        xx["case"]={k:f[k] for k in ["lead","R_m","weather"]}
        xx["unrounded_independent"]=f[x["field"]]
        eq(x["row"],"discrepancy_locator_rounding",x["independent"],round(xx["unrounded_independent"]))
        discrepancies.append(xx)
discrepancies.extend(dict(x,owner_artifact="RESULTS.json",category="source-selection") for x in load("SOURCE-SELECTION-MISMATCHES.json"))
discrepancies.extend(dict(x,owner_artifact="mga057.json") for x in load("CBE-CREDIT-EXACT-FIELDS.json"))
discrepancies.extend(dict(x,owner_artifact="RESULTS.json") for x in load("DIRECT048-EXACT-FIELDS.json"))
worst=claims["transfer_range"]["largest"]
discrepancies.append(dict(row="CARD/section2/Where-the-bills-come-from",field="transfer_error_absolute_max_kg",
                          owner=9.2,independent=abs(worst["diff_kg"]),case={k:worst[k] for k in ["R_m","weather","mask"]},
                          category="transfer-range-scope",owner_artifact="CARD.md",
                          note="9.2 kg is valid for selected masks11/15, not all96 transfer comparisons."))
direct=next(r for r in rs if r["lead"]=="P2" and r["source"]=="048" and r["R_m"]==10 and r["weather"]=="ISA" and not r["floor"])
discrepancies.append(dict(row="CARD/section4/R10-full-optimism",field="payload_with_mga_kg",
                          owner=-589,independent=direct["evaluated"][15]["payload_sourced_kg"],
                          category="least-set-vs-all-axes",owner_artifact="CARD.md",
                          note="-589 is rounded least-three-axis result; all four axes give about-579."))
counts=load("COUNTS.json")
result=dict(unit="vacuum-mainline057-check-1020",tag="QUESTIONABLE / PROJECTION",completion="independent057-scope-complete",
            scientific_arithmetic_comparisons=counts["comparisons"],
            scientific_arithmetic_mismatches=counts["mismatches"],
            card_and_ancillary_comparisons=claims["comparisons"],card_rounding_mismatches=claims["mismatches"],
            provenance_comparisons=len(audit),provenance_mismatches=sum(not x["pass_"] for x in audit),
            total_comparisons=counts["comparisons"]+claims["comparisons"]+len(audit),
            records=counts["records"],subset_bills=counts["points"],
            discrepancy_fields=len(discrepancies),discrepancy_categories=sorted(set(x["category"] for x in discrepancies)),
            all_stored_cases_negative_after_declared_mga=counts["all_source_scenarios_negative"],
            R10=base["R10"],all_endpoint_cases=claims["all_radii"],
            transfer_error_range=claims["transfer_range"],
            ancillary_thermal=claims["thermal"],ancillary_week_aloft=claims["week_aloft"],
            qualified_hull_SF=None,actual_failure_probability=None,qualified_maturity=None,
            global_continuous_radius_feasibility=None,global_reoptimized_feasibility=None,
            time_budget=None,next="none",owner_executable_access=False)
write("PROVENANCE-CHECK.json",dict(comparisons=len(audit),mismatches=sum(not x["pass_"] for x in audit),rows=audit))
write("DISCREPANCIES.json",dict(fields=len(discrepancies),rows=discrepancies))
write("RESULTS.json",result)
print(json.dumps({k:v for k,v in result.items() if k not in ["R10","all_endpoint_cases","ancillary_thermal","transfer_error_range"]}))
print("PROVENANCE MISMATCHES",json.dumps([x for x in audit if not x["pass_"]][:8]))
print("ROUNDING",json.dumps(discrepancies[:4]))
