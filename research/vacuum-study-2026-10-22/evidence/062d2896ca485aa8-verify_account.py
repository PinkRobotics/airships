"""Compare every distinct MAINLINE-048 main point with independent account equations."""
import collections
import csv
import gzip
import json
import math
from pathlib import Path
import sys

R = Path(__file__).resolve().parent
sys.path.insert(0, str(R))
import account_model as model
import numpy as np

model.THERMAL=json.loads((R/"INDEPENDENT-THERMAL-TABLES.json").read_text())
supplemental=json.loads((R/"SUPPLEMENTAL-THERMAL-TABLES.json").read_text())
owner = json.loads((R/"intake/owner/RESULTS.json").read_text())
seen, points = set(), []


def collect(x, path, thermal_key=None):
    if isinstance(x, dict):
        thermal_key=x.get("type",thermal_key) if x.get("type") in supplemental else thermal_key
        if "classical_low_emittance_sensitivity" in path:thermal_key="classical_low_emittance"
        if all(k in x for k in ("R_m", "geometry", "settings", "bill_kg", "mask", "usage")):
            key = json.dumps([x["R_m"],x["geometry"],x["settings"],x["mask"],x["usage"],thermal_key],sort_keys=True)
            if key not in seen:
                seen.add(key);points.append((path,x,thermal_key))
            return
        for k,v in x.items():
            collect(v,path+"."+k,thermal_key)
    elif isinstance(x,list):
        for i,v in enumerate(x):
            collect(v,path+f"[{i}]",thermal_key)


collect(owner,"main")
main_points = len(points)
for name in ("SENSITIVITIES", "ADDITIONAL-AUDIT"):
    collect(json.loads((R/"intake/owner"/(name+".json")).read_text()), name)
original_and_supplemental_points=len(points)
collect(json.loads((R/"intake/addendum048/2-RESULTS.json").read_text()),"addendum048")
mismatches, totals, largest = [],collections.Counter(),{}
count=0
output=gzip.open(R/"ACCOUNT-COMPARISONS.csv.gz","wt",newline="")
writer=csv.DictWriter(output,fieldnames=["point","field","owner","independent","delta","agrees","rtol","atol"])
writer.writeheader()


def compare(point,field,old,new,rtol=3e-6,atol=3e-7):
    global count
    if isinstance(new,np.generic):new=new.item()
    if isinstance(new,np.ndarray):new=new.item()
    if not isinstance(new,(int,float)) or isinstance(new,bool):return
    passed=math.isclose(old,new,rel_tol=rtol,abs_tol=atol)
    row=dict(point=point,field=field,owner=old,independent=new,delta=new-old,agrees=passed,rtol=rtol,atol=atol)
    writer.writerow(row);count+=1
    if not passed:
        mismatches.append(row);totals[field]+=1
        if field not in largest or abs(row["delta"])>abs(largest[field]["delta"]):largest[field]=row


def tree(point,path,old,new):
    for k,v in new.items():
        if k not in old:continue
        field=path+"."+k if path else k
        if isinstance(v,dict):tree(point,field,old[k],v)
        elif isinstance(v,list):
            for i,item in enumerate(v):compare(point,field+f"[{i}]",old[k][i],item)
        else:compare(point,field,old[k],v)


primary=[]
for label,p,thermal_key in points:
    override=None if thermal_key is None else supplemental[thermal_key][str(int(p["R_m"]))]
    q=model.evaluate(p["R_m"],p["geometry"]["tf_m"],p["geometry"]["tc_m"],
                     p["mask"],p["usage"],p["settings"],tab=override)
    tree(label,"",p,q)
    if label.endswith("two_factor_endpoint"):
        primary.append(dict(point=label,R_m=p["R_m"],settings=p["settings"],
                            signed_payload_kg=q["signed_payload_kg"],
                            least_shell_and_thermal_SF=q["least_shell_and_thermal_SF"],
                            material_water_initial_by_material_kg=q["material_water_initial_by_material_kg"],
                            material_water_remaining_by_material_kg=q["material_water_remaining_by_material_kg"]))
output.close()
(R/"ACCOUNT-MISMATCHES.json").write_text(json.dumps(mismatches,indent=2,allow_nan=False)+"\n")
(R/"ACCOUNT-RESULTS.json").write_text(json.dumps(dict(
    tag="QUESTIONABLE / PROJECTION",main_distinct_points=main_points,
    distinct_points=len(points),original_and_supplemental_points=original_and_supplemental_points,comparison_count=count,
    mismatch_count=len(mismatches),mismatch_counts_by_field=dict(totals),
    largest_difference_by_field=largest,primary_endpoints=primary,
    scope="Independent equations and independently reconstructed thermal tables; no owner code. Numeric mechanical tolerance 3e-6 relative reflects independent enclosure convergence; all raw differences retained.",
    owner_code_read=False,owner_code_executed=False),indent=2,allow_nan=False)+"\n")
print(json.dumps(dict(points=len(points),comparisons=count,mismatches=len(mismatches),
                     mismatch_counts_by_field=dict(totals),largest=list(largest.values())[:14])))
