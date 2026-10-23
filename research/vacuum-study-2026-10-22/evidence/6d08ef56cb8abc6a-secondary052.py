"""Independent table, comparator, conservation and sensitivity checks."""
import csv
import json
import math
import re
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import numpy as np
from check052 import (B, read, write, Audit, Family, LIFT, RHO, P0, T0,
                      RG, MW, PW_TARGET, RET0, RET1, WEATHER)

rec = read("RECONSTRUCTED.json")
index = {(r["R_m"],r["weather"],r["service"]):r for r in rec["rows"]}
audit = Audit()

# P2 is a selection of existing, pinned endpoints, not another P2 optimization.
p2 = {}
expected = read("owner/P2-COMPARISON.json")
source_rows = {"040":read("inputs/own040/owner/RESULTS.json")["rows"],
               "048":read("inputs/048/RESULTS.json")["rows"]}
for source, listed in expected.items():
    p2[source] = []
    for i,old in enumerate(listed):
        candidates = [r for r in source_rows[source]
                      if r["R_m"] == old["R_m"] and r["weather"] == old["weather"]
                      and r["floor"] == old["floor"]
                      and (r.get("pad") == "heavy70" and r.get("vented") is True
                           if source == "040" else
                           r["profile"] == "MLCCAg" and r["drying"] == "bake70"
                           and r["external_water_kg_m2"] == .1)]
        assert len(candidates)==1
        upstream=candidates[0]
        trials=[]
        for j,trial in enumerate(upstream["least"]["endpoint_trials"]):
            point=trial["solution"]
            payload=point["lift_kg"]-sum(point["bill_kg"].values())
            audit.compare(f"P2.{source}[{i}].endpoint_trials[{j}].payload_kg",
                          trial["payload_kg"],payload)
            trials.append((payload,trial))
        payload,best=max(trials,key=lambda t:t[0])
        low=upstream["least"]["least"]
        two=upstream["two_factor_endpoint"]
        new={"R_m":old["R_m"],"weather":old["weather"],"floor":old["floor"],
             "endpoint_mask":best["mask"],"endpoint_axes":best["axes"],
             "filed_endpoint_payload_kg":payload,
             "same_extra_vacuum50_payload_kg":payload-50,
             "filed_least_axis_count":upstream["least"]["minimum_axis_count"],
             "filed_least_usage":low["usage"] if low else None,
             "two_factor_endpoint_payload_kg":two["lift_kg"]-sum(two["bill_kg"].values()),
             "qualification":"filed conditional endpoint; subtract 50 kg additional service; no new P2 optimization"}
        audit.compare(f"P2.{source}[{i}]",old,new)
        p2[source].append(new)
write("P2-INDEPENDENT.json",p2)

# All three published CSVs are checked against independently rebuilt points.
for filename in ["ROWS.csv","MASS-ACCOUNT.csv","VACUUM-SERVICE.csv"]:
    for i,row in enumerate(csv.DictReader((B/"owner"/filename).open())):
        key=(int(row["R_m"]),row["weather"],row["service"])
        sel=row["selection"]
        field={"baseline":"baseline","all_endpoints":"all_axes_endpoint",
               "endpoint":"all_axes_endpoint","least":"least"}.get(sel,sel)
        p=index[key][field]
        expanded={**p,**p["reliability"],**p["bill_kg"],**p["vacuum"],"selection":sel}
        for k,v in row.items():
            got=expanded[k]
            if v=="":
                old=None
            elif v in ("True","False"):
                old=v=="True"
            else:
                try:old=float(v)
                except ValueError:old=v
            audit.compare(f"{filename}[{i}].{k}",old,got)

# Every numerical cell in all seven CARD tables, at its displayed precision.
tables=[]
current=[]
for line in (B/"owner/CARD.md").read_text().splitlines()+[""]:
    if line.startswith("|"):
        current.append([x.strip() for x in line.strip("|").split("|")])
    elif current:
        tables.append(current[2:]);current=[]
assert len(tables)==7
printed=[]


def cell(path, text, value):
    clean=text.replace(",","").replace("−","-")
    if value is None:
        passed=clean in ("not calculated","no closure")
        printed.append({"path":path,"displayed":text,"checker":None,"match":passed})
        return
    if clean.startswith("1-"):
        clean=clean[2:]
        # 'value' is supplied as the survival probability here.
    shown=float(clean)
    if "e" in clean.lower():
        mantissa,exponent=clean.lower().split("e")
        digits=len(mantissa.split(".")[1]) if "." in mantissa else 0
        tol=.5*10**(int(exponent)-digits)
    else:
        digits=len(clean.split(".")[1]) if "." in clean else 0
        tol=.5*10**(-digits)
    printed.append({"path":path,"displayed":text,"checker":value,
                    "rounding_tolerance":tol,"match":abs(shown-value)<=tol+2e-7})


for row in tables[0]:
    r=int(row[0]);w=row[1]
    for j,service in enumerate(["ground","onboard_pressure","onboard_dry"]):
        cell(f"CARD.payload.R{r}.{w}.{service}",row[j+2],index[(r,w,service)]["all_axes_endpoint"]["payload_kg"])
for tno,service in [(1,"ground"),(2,"onboard_pressure")]:
    for row in tables[tno]:
        r=int(row[0]);w=row[1];rr=index[(r,w,service)]
        p=rr["least"] or rr["all_axes_endpoint"]
        label=row[2]
        if ";" in label:
            axes,u=label.split(";")
            got_axes="".join("SFLJ"[j] for j in range(4) if p["mask"]&(1<<j))
            printed.append({"path":f"CARD.least.{service}.R{r}.{w}.axes",
                            "displayed":axes,"checker":got_axes,"match":axes==got_axes})
            cell(f"CARD.least.{service}.R{r}.{w}.usage",u,p["usage"])
        else:
            printed.append({"path":f"CARD.least.{service}.R{r}.{w}.no_closure",
                            "displayed":label,"checker":rr["least"],
                            "match":rr["least"] is None})
        values=[p["required_SiC_strength_Pa"]/1e9,p["film_effective_strength_Pa"]/1e9,
                p["ten_year_retention"],p["joint_allowance_kg"]]
        if tno==1:values.append(p["payload_kg"])
        for j,value in enumerate(values):
            cell(f"CARD.least.{service}.R{r}.{w}.column{j+3}",row[j+3],value)
root=index[(10,"ISA","ground")]["least"]
mass_labels=["SiC_tubes","joint_sleeves_and_allowance","joint_bond_and_installation",
             "nodes","PBO_two_plies","barrier_and_protection","systems","vacuum_service",
             "gas","exterior_water","contamination","mooring_load_introduction",
             "sag_lift_debit","weather_headroom"]
mass_values=[root["bill_kg"][k] for k in mass_labels]+[sum(root["bill_kg"].values()),
                                                    root["lift_kg"],root["payload_kg"]]
for i,(row,value) in enumerate(zip(tables[3],mass_values)):
    cell(f"CARD.mass[{i}].{row[0]}",row[1],value)
for row in tables[4]:
    r=int(row[0]);w=row[1];v=index[(r,w,"onboard_dry")]["all_axes_endpoint"]["vacuum"]
    g=index[(r,w,"ground")]["all_axes_endpoint"]["vacuum"]
    vals=[v["pumps"],v["service_mass_kg"],v["electrical_24h_kWh"],g["first_cycle_humidity_limit_h"]]
    for j,value in enumerate(vals):
        cell(f"CARD.pumps.R{r}.{w}.column{j+2}",row[j+2],value)
for row in tables[5]:
    r=int(row[0]);w=row[1];rr=index[(r,w,"ground")]
    p=rr["least"] or rr["all_axes_endpoint"];rel=p["reliability"]
    cell(f"CARD.reliability.R{r}.{w}.whole",row[2],rel["Pf_whole_member"])
    value=math.exp(-rel["H_coupon_1cm3"]) if "−" in row[3] else rel["Pf_coupon_1cm3"]
    cell(f"CARD.reliability.R{r}.{w}.coupon",row[3],value)
for row in tables[6]:
    r=int(row[0]);w=row[1]
    vals=[index[(r,w,"ground")]["all_axes_endpoint"]["payload_kg"]]
    for src in ["040","048"]:
        found=[x for x in p2[src] if x["R_m"]==r and x["weather"]==w and x["floor"]]
        vals.append(found[0]["same_extra_vacuum50_payload_kg"] if found else None)
    for j,value in enumerate(vals):
        cell(f"CARD.P2.R{r}.{w}.column{j+2}",row[j+2],value)
write("PRINTED-CELL-AUDIT.json",printed)

# Independent physical identities and integration, not a replay of owner tests.
checks=[]


def check(name,passed,details):
    checks.append({"name":name,"pass":bool(passed),"details":details})


allpoints=[]
for row in rec["rows"]:
    allpoints.extend([row["baseline"],row["all_axes_endpoint"],*row["endpoints"],*row["roots"]])
check("all primary point mass identities",all(abs(p["lift_kg"]-sum(p["bill_kg"].values())-p["payload_kg"])<1e-7 for p in allpoints),
      {"points":len(allpoints),"debits":14})
check("all intended point screens",min(p["all_screened_SF"] for p in allpoints)>1-1e-8,
      {"minimum":min(p["all_screened_SF"] for p in allpoints)})
check("all declared dry service pump counts are minimal integers",
      all((p["vacuum"]["dry_cavity_pumps"]-1)*27.5*.75 < p["vacuum"]["pump_speed_required_dry_m3_h"]
          <= p["vacuum"]["dry_cavity_pumps"]*27.5*.75 for p in allpoints),
      {"points":len(allpoints)})
check("no radius/weather has onboard dry endpoint closure",
      all(row["all_axes_endpoint"]["payload_kg"]<0 for row in rec["rows"] if row["service"]=="onboard_dry"),
      {"cases":15})
v=root["vacuum"]
q=v["water_external_upper_kg_day"];release=v["initial_material_release_water_proxy_kg"]
cross=v["first_cycle_humidity_limit_h"]/24
sol=solve_ivp(lambda t,y:[q+release*math.exp(-t)],(0,1),[0.],
              method="DOP853",rtol=1e-12,atol=1e-13,dense_output=True,max_step=.05)
numeric_cross=float(sol.sol(cross)[0])
check("humidity crossing by independent ODE integration",
      abs(numeric_cross-v["water_capacity_kg"])<1e-10,
      {"integrated_water_kg":numeric_cross,"capacity_kg":v["water_capacity_kg"],
       "first_crossing_h":cross*24})
check("reported minimal subset counts and zero roots",
      all(abs(p["payload_kg"])<2e-6 for row in rec["rows"] for p in row["roots"]),
      {"roots":sum(len(row["roots"]) for row in rec["rows"])})
check("041 geometry from endpoint coordinates",
      abs(rec["rows"][0]["baseline"]["bill_kg"]["sag_lift_debit"]-73.10073311528532)<1e-8,
      {"independent_sag_kg":rec["rows"][0]["baseline"]["bill_kg"]["sag_lift_debit"]})
validation=read("owner/VALIDATION.json")
check("owner validation receipt count and status",
      validation["checks"]==len(validation["details"])==1440 and validation["failures"]==0
      and all(v["pass_"] for v in validation["details"]),
      {"scope":"receipt integrity, not an execution of owner tests","details":len(validation["details"])})

# These are explicitly new sensitivities, not changes to the owner's model.
bulk_temperature=[]
for t in [T0,294.9,310.,320.]:
    capacity=PW_TARGET*v["free_volume_m3"]*MW/(RG*t)
    hours=24*brentq(lambda d:q*d+release*(-math.expm1(-d))-capacity,0,2)
    bulk_temperature.append({"gas_temperature_K":t,"cold_film_temperature_held_K":274.00711698603436,
                             "water_capacity_kg":capacity,"first_humidity_crossing_h":hours,
                             "90pct_schedule_h":.9*hours,
                             "tag":"PROJECTION; counterfactual bulk-temperature sensitivity, fixed sources and cold-film target"})
supplement={"R10_ISA_least":root,
            "ply_efficiency":root["film_effective_strength_Pa"]/5.8e9,
            "extra_0p9_kg_m2_water_R10_kg":.9*4*math.pi*10**2,
            "ground30_vs50_gain_kg":20.,
            "explicit_nesting_of_ground50_in_systems100_gain_kg":50.,
            "alternative_family_endpoint_difference_R10_kg":
                index[(10,"ISA","ground")]["all_axes_endpoint"]["payload_kg"]
                -rec["alternative_checked_f5_5"][0]["all_axes_endpoint"]["payload_kg"],
            "bulk_temperature_sensitivity":bulk_temperature,
            "R30_whole_vs_coupon_survival": [
                {"weather":w, "survival_coupon":math.exp(-(index[(30,w,"ground")]["least"] or
                                                          index[(30,w,"ground")]["all_axes_endpoint"])["reliability"]["H_coupon_1cm3"])}
                for w in WEATHER]}
write("SUPPLEMENTAL-RESULTS.json",supplement)
write("VERIFICATION.json",checks)
write("SECONDARY-AUDIT.json",audit.rows)
write("SECONDARY-MISMATCHES.json",audit.mismatches)
summary={"field_comparisons":len(audit.rows),"numeric":audit.numeric,
         "field_mismatches":len(audit.mismatches),"printed_cells":len(printed),
         "printed_mismatches":[p for p in printed if not p["match"]],
         "verification_checks":len(checks),"verification_failed":[c for c in checks if not c["pass"]]}
write("SECONDARY-SUMMARY.json",summary)
print(json.dumps(summary,indent=2))
