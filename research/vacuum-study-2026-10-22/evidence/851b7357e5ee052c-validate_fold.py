#!/usr/bin/env python3
"""Verify the changed demands, exact water offsets and independent check targets."""
import hashlib
import json
import math
from collections import defaultdict
from dataclasses import replace
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
import fold_model as m

B=Path(__file__).resolve().parent
I=json.loads((B/"INPUTS.json").read_text())
BASE=Path(I["original_048_directory"])
tables=json.loads((B/"inputs/048/THERMAL-TABLES.json").read_text())
stats=defaultdict(lambda:dict(count=0,failed=0,max_absolute_error=0.))
failures=[]
def check(label,good,evidence=None):
    stats[label]["count"]+=1
    if not good:
        stats[label]["failed"]+=1;failures.append(dict(check=label,evidence=evidence))
def near(label,value,target,atol=1e-6,rtol=1e-8):
    delta=abs(value-target)
    stats[label]["max_absolute_error"]=max(stats[label]["max_absolute_error"],delta)
    check(label,delta<=atol+rtol*abs(target),dict(value=value,target=target,delta=delta))

# CHECK-040's independently written model was not accessed. Reconstruct the
# scalar alternatives from its non-code rows using this seat's model.
checkrows=json.loads((B/"inputs/check040/MODEL-DEPENDENCE.json").read_text())
marginal=json.loads((B/"inputs/check040/MARGINAL-MODELS.json").read_text())
reproduction=[]
for label,rows in [("two_factor",checkrows),("all_four",marginal)]:
    for row in rows:
        target=(row["cases"]["include_cure_in_global_and_crimp"]["reoptimized"]
                if label=="two_factor" else row["cases"]["cure_in_global"])
        p=m.optimize(target["R_m"],target["mask"],1,m.Settings(**target["settings"]),n=1400)
        delta=p["signed_payload_kg"]-target["signed_payload_kg"]
        near("independent CHECK040 cure reproduction",p["signed_payload_kg"],target["signed_payload_kg"],atol=.005)
        reproduction.append(dict(id=row["id"],track=label,check040_kg=target["signed_payload_kg"],
                                  reproduced_kg=p["signed_payload_kg"],delta_kg=delta))
old040=json.loads((m.B/"RESULTS.json").read_text())
oldindex={x["id"]:x for x in old040["rows"]}
for w in json.loads((B/"inputs/check040/WATER-ONE-MM-SENSITIVITY.json").read_text()):
    old=oldindex[w["id"]]
    r=old["R_m"];extra=.9*4*math.pi*r*r
    full=next(t["solution"] for t in old["least"]["endpoint_trials"] if t["mask"]==15)
    near("CHECK040 1mm extra water",w["extra_water_kg"],extra)
    near("CHECK040 1mm named endpoint",w["endpoint_11_payload_kg"],
         old["two_factor_endpoint"]["signed_payload_kg"]-extra,atol=.005)
    near("CHECK040 1mm all-four endpoint",w["all_four_full_endpoint_payload_kg"],
         full["signed_payload_kg"]-extra,atol=.005)

allrows=[];dense=[];echecks=[];unique=set();pointcount=0
for name in I["profiles"]:
    data=json.loads((B/f"RESULTS-{name}.json").read_text())
    assert data["complete"],name
    check("profile row count",len(data["rows"])==162,name)
    check("paired cure configurations",len(data["pairs"])==54,name)
    check("all excluded subset bounds",all(x["excludes_float"] for x in data["bounds"]),name)
    allrows.extend(data["rows"])
    original=json.loads((BASE/f"RESULTS-{name}.json").read_text())
    oi={x["id"]:x for x in original["rows"]}
    m.THERMAL=tables[name]
    for x in data["rows"]:
        ps=[t["solution"] for t in x["least"]["endpoint_trials"] if t["solution"]]
        ps+=x["least"].get("ties",[])
        for p in ps:
            key=json.dumps([p["geometry"],p["settings"],p["mask"],p["usage"]],sort_keys=True)
            if key in unique:continue
            unique.add(key);pointcount+=1
            r=p["R_m"];s=p["settings"];a=4*math.pi*r*r
            tf=p["geometry"]["tf_m"];tc=p["geometry"]["tc_m"]
            b=p["bill_kg"];pr=p["properties"]
            E=pr["E_Pa"];nu=s["nu"];sig=p["load_pressure_Pa"]*r/(4*tf)
            cure=pr["added_cure_compression_Pa"]
            gradient=pr["added_gradient_stress_Pa"];bend=pr["added_bending_stress_Pa"]
            global_demand=sig+(cure if s["cure_in_global"] else 0)
            crimp_demand=sig+gradient+bend+(cure if s["cure_in_global"] else 0)
            local=sig+gradient+bend+cure
            crimp=m.C["Gc_Pa"]*(tc+tf)**2/(2*tf*tc)
            sig0=E*(tc+tf)/(r*math.sqrt(1-nu*nu));vc=sig0/crimp
            kc=1-vc/4 if vc<=2 else 1/vc
            near("global demand cure included exactly once",pr["global_compressive_demand_Pa"],global_demand)
            near("crimp demand cure included exactly once",pr["crimp_compressive_demand_Pa"],crimp_demand)
            near("global factor",p["modes"]["global_buckling"],pr["gamma"]*kc*sig0/global_demand,atol=1e-8)
            near("crimp factor",p["modes"]["core_shear_crimping"],crimp/crimp_demand,atol=1e-8)
            near("local compression unchanged",p["modes"]["face_compression"],pr["Fcy_Pa"]/local,atol=1e-8)
            near("scarf cure not doubled",p["modes"]["scarf_average_shear_screen"],
                 10e6/(local*s["scarf_ratio"]/(1+s["scarf_ratio"]**2)),atol=1e-8)
            near("exterior water charge",b["water"],s["external_water_kg_m2"]*a)
            near("mass ledger closes",sum(b.values())+p["signed_payload_kg"],p["lift_kg"])
            check("all retained mechanical constraints",min(p["modes"].values())>=1-3e-7,x["id"])
            check("service constraint",p["vacuum"]["pressure_SF"]>=1-2e-7,x["id"])
            check("installed hull SF remains unknown",p["overall_installed_hull_SF"] is None)
            if s["external_water_kg_m2"]==1:
                check("1mm has no false assembly pass",not p["modeled_assembly_pass"])
        if x["external_water_kg_m2"]==1:
            check("1mm excluded with favorable upper bound",x["favorable_payload_upper_kg"]<0,x["id"])
            near("0.9mm additional water",x["extra_exterior_water_kg"],.9*4*math.pi*x["R_m"]**2)
            baseid=x["id"].split("-cure_included")[0].split("-original_cure_treatment")[0].replace("one_mm_water","retained_water")
            source=(next(y for y in data["rows"] if y["id"]==baseid+"-cure_included")
                    if x["cure_in_global"] else oi[baseid])
            for p,t in zip(x["least"]["endpoint_trials"],source["least"]["endpoint_trials"]):
                if p["solution"] and t["solution"]:
                    near("constant water debit preserves optimum",
                         p["payload_kg"],t["payload_kg"]-x["extra_exterior_water_kg"])
            continue
        # Denser searches cover every bake condition and all near-zero
        # endpoint cases where a sign change matters.
        endpoint=x["two_factor_endpoint"]
        all4=next(t["solution"] for t in x["least"]["endpoint_trials"] if t["mask"]==15)
        if x["drying"]=="bake70" or min(abs(endpoint["signed_payload_kg"]),abs(all4["signed_payload_kg"]))<50:
            for label,p in [("endpoint",endpoint),("all4",all4),("least",x["least"]["least"])]:
                if p is None:continue
                q=m.optimize(x["R_m"],p["mask"],p["usage"],m.Settings(**p["settings"]),n=2000)
                delta=q["signed_payload_kg"]-p["signed_payload_kg"]
                near("denser geometry optimum",q["signed_payload_kg"],p["signed_payload_kg"],atol=.02,rtol=0)
                dense.append(dict(id=x["id"],track=label,delta_kg=delta))
        p=x["least"]["least"]
        if p is not None and p["mask"]&4:
            ceiling=p["usage"];s=m.Settings(**p["settings"])
            def value(uE):
                q=m.optimize(x["R_m"],p["mask"],[ceiling,ceiling,uE,ceiling],s,n=800,detail=False)
                return -1e20 if q is None else q
            samples=[value(u) for u in np.linspace(0,ceiling,9)]
            q=minimize_scalar(lambda u:-value(u),bounds=(0,ceiling),method="bounded",options={"xatol":1e-7})
            best=max(*samples,-q.fun);delta=best-p["signed_payload_kg"]
            check("independent E ceiling optimum",delta<.002,dict(id=x["id"],improvement_kg=delta))
            echecks.append(dict(id=x["id"],improvement_kg=float(delta)))
    print(name,"validated",flush=True)

expected={(name,r,w,f,d,water,cure) for name in I["profiles"] for r in I["radii_m"]
          for w in I["weather"] for f in [False,True] for d in I["routes"]
          for water,cure in [(.1,True),(1.,False),(1.,True)]}
seen={(x["profile"],x["R_m"],x["weather"],x["floor"],x["drying"],
       x["external_water_kg_m2"],x["cure_in_global"]) for x in allrows}
check("all 648 unique required new configurations",seen==expected and len(allrows)==648)
for pin in json.loads((B/"INPUT-PINS.json").read_text()):
    raw=(B/pin["snapshot"]).read_bytes()
    check("pinned source snapshot",hashlib.sha256(raw).hexdigest()==pin["sha256"] and len(raw)==pin["bytes"],pin["snapshot"])
for p in json.loads((B/"ORIGINAL-048-PINS.json").read_text()):
    raw=Path(p["path"]).read_bytes()
    check("original 048 immutable",hashlib.sha256(raw).hexdigest()==p["sha256"] and len(raw)==p["bytes"],p["path"])
for p in json.loads((BASE/"MODEL-PINS.json").read_text()):
    raw=Path(p["path"]).read_bytes()
    check("original 040 immutable",hashlib.sha256(raw).hexdigest()==p["sha256"] and len(raw)==p["bytes"],p["path"])

m.dump(B/"CHECK040-REPRODUCTION.json",reproduction)
m.dump(B/"SEARCH-VALIDATION.json",dense)
m.dump(B/"E-USAGE-VALIDATION.json",echecks)
result=dict(passed=not failures,configurations=len(allrows),unique_points=pointcount,
            checks=sum(v["count"] for v in stats.values()),summary=dict(stats),failed=failures)
m.dump(B/"VALIDATION.json",result)
print(json.dumps({k:v for k,v in result.items() if k!="summary"},indent=2))
if failures:raise SystemExit(1)
