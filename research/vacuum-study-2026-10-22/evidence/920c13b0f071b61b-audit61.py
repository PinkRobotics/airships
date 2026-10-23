"""Focused arithmetic, optimizer-domain and operational-reference checks."""
import json
import math
from datetime import datetime
from scipy.optimize import brentq, minimize_scalar
from model61 import *
from source61 import ROOT, source

old=ROOT/"CALCULATIONS.json"
archive=ROOT/"CALCULATIONS-before-source-correction.json"
if not archive.exists():
    archive.write_bytes(old.read_bytes())
d=json.loads(archive.read_text())
audit=[]
fixes=[]

for x in d["frozen_check057"]:
    b=x["bill_kg"]
    x["previous_declared_TRL7_payload_kg"]=x["payloads_kg"]["TRL7"]
    x["payloads_kg"]["TRL7"]=L10*(x["R_m"]/10)**3-sum(b.values())-sum(growth(b,"P2","TRL7").values())

for x in d["p2"]:
    r,w,basis=x["R_m"],x["weather"],x["basis"]
    x["deficit"]={m:p2_opt(r,w,basis=basis,maturity=m,n=400) for m in ("none","TRL7","concept")}
    # Modulus is not monotonic once thermal and scarf stresses are retained.
    egrid=np.geomspace(1.,5.,25)
    vals=[]
    for f in egrid:
        pt=p2_opt(r,w,{"face_modulus":float(f)},basis,n=100)
        vals.append(-1e20 if pt is None else pt["payload_kg"])
    j=int(np.argmax(vals))
    ebest=(float(vals[j]),float(egrid[j]))
    if 0<j<len(egrid)-1:
        def loss(logf):
            pt=p2_opt(r,w,{"face_modulus":math.exp(logf)},basis,n=180)
            return 1e20 if pt is None else -pt["payload_kg"]
        fit=minimize_scalar(loss,bounds=(math.log(egrid[j-1]),math.log(egrid[j+1])),
                            method="bounded",options={"xatol":1e-7})
        if -fit.fun>ebest[0]:ebest=(-float(fit.fun),math.exp(fit.x))
    es=next(z for z in x["single"] if z["property"]=="face_modulus")
    x["modulus_nonmonotonic_scan"]={"factors":egrid.tolist(),"payloads_kg":vals,
                                   "refined_peak_payload_kg":ebest[0],"peak_factor":ebest[1]}
    if es["factor"] is None and ebest[0]>0:
        def target(logf):
            pt=p2_opt(r,w,{"face_modulus":math.exp(logf)},basis,n=260)
            return -1e20 if pt is None else pt["payload_kg"]
        root=math.exp(brentq(target,0.,math.log(ebest[1]),xtol=2e-8))
        es.update(status="conditional closure",factor=root,
                  solution=p2_opt(r,w,{"face_modulus":root*(1+1e-6)},basis,n=800))
        fixes.append({"R_m":r,"weather":w,"basis":basis,
                      "finding":"coarse monotonic bracket missed a bounded modulus feasibility interval",
                      "corrected_factor":root,"fix_review":"not independently reviewed"})
        x["combination"]=combination_p2(r,w,basis,x["single"])
    # A fresh dense geometry search verifies every actual closure witness.
    for s in x["single"]:
        if s.get("factor") is None: continue
        factor=s["factor"]
        pt=p2_opt(r,w,{s["property"]:factor},basis,n=1000)
        audit.append({"check":"single closure dense geometry and gas service","R_m":r,"weather":w,
                      "basis":basis,"property":s["property"],
                      "payload_kg":None if pt is None else pt["payload_kg"],
                      "mode_min":None if pt is None else min(pt["modes"].values())})
        if pt is None or pt["payload_kg"]<-.1:
            raise AssertionError(audit[-1])
        s["solution"]=pt
    combo=x["combination"]
    cp=p2_opt(r,w,combo["factors"],basis,n=1000)
    if cp is None or cp["payload_kg"]<-.1: raise AssertionError(("combo",r,w,basis,cp))
    combo["solution"]=cp
    x["marginal_10pct"]=[]
    for prop in P2PROPS:
        pt=p2_opt(r,w,{prop:1.1},basis,n=240)
        x["marginal_10pct"].append({"property":prop,"factor":1.1,
                                   "gain_kg":None if pt is None else pt["payload_kg"]-x["deficit"]["concept"]["payload_kg"],
                                   "payload_kg":None if pt is None else pt["payload_kg"],
                                   "physical_cap_applied":prop in ("Q","gamma")})
    if basis=="endpoint":
        def floor_payload(logf):
            p=p2_opt(r,w,{"face_density":math.exp(logf)},basis,floor=True,n=240)
            return -1e20 if p is None else p["payload_kg"]
        root=math.exp(brentq(floor_payload,0.,math.log(3),xtol=2e-8))
        x["retained_joining_floor"]={"face_density_factor":root,
                                    "solution":p2_opt(r,w,{"face_density":root},basis,floor=True,n=700)}
    print("AUDIT P2",r,w,basis,"product",combo["factor_product"],flush=True)

for x in d["p3"]:
    r,w=x["R_m"],x["weather"]
    x["deficit"]={m:p3(r,w,maturity=m) for m in ("none","TRL7","concept")}
    for s in x["single"]:
        s["solution"]=p3(r,w,{s["property"]:s["limit_factor"]})
        s["limit_payload_kg"]=s["solution"]["payload_kg"]
    free=p3(r,w,{"SiC_strength":1e12,"ply_strength":1e12,"retention":1/.9511101304657719,
                "film_mass":1e12,"node_mass":1e12})
    x["combination"]["infinite_improvements"]=free
    x["marginal_10pct"]=[{"property":p,"gain_kg":p3(r,w,{p:1.1})["payload_kg"]-x["deficit"]["concept"]["payload_kg"]}
                         for p in ("SiC_strength","ply_strength","retention","film_mass","node_mass")]

# Re-price the actually filed 058 relief/finish hulls, rather than subtracting
# the full-range-to-relieved saving a second time from the lighter 057 bill.
ops=source("058runs","levers058.json")
ops3=source("058runs","p3_058.json")
operation=[]
for r in (12,20,30):
    for h in ops["hulls"]:
        if h["R_m"]!=r or h["mask"]!=15 or h["id"] not in (
            "full","trim-30","finish_AlAOC","finish_lowe_night_0.05"):continue
        for w in ("ISA","optimistic"):
            b=dict(h["bill_kg"])
            b["weather_headroom"]=L10*(r/10)**3*CF[w]
            # Omit bladder mass and admitted-air lift loss deliberately to form
            # a favorable mass upper bound, not an operational flight claim.
            if h["id"]!="full": b["relief_valve"]=5.
            allowance=growth(b,"P2","concept")
            if "relief_valve" in b: allowance["relief_valve"]=1.5
            payload=L10*(r/10)**3-sum(b.values())-sum(allowance.values())
            nominal=next(x for x in d["p2"] if x["R_m"]==r and x["weather"]==w and x["basis"]=="endpoint")
            operation.append({"lead":"P2","R_m":r,"weather_reference":w,"variant":h["id"],
                              "finish":h["finish"],"design_pressure_Pa":h["design_load_Pa"],
                              "payload_upper_bound_kg":payload,
                              "difference_from_061_nominal_kg":payload-nominal["deficit"]["concept"]["payload_kg"],
                              "mass_basis":"058 fixed hull and its retained 5% joining floor",
                              "omitted_nonnegative_debits":["ballast bladder","admitted-air mass/lost lift"],
                              "operational_qualification":None})
for x in d["p3"]:
    r=x["R_m"]
    op=next(y for y in ops3["rows"] if y["R_m"]==r and y["selection"]=="mask15")
    fraction=1-op["bill_trim"]["SiC_tubes"]/op["bill_full"]["SiC_tubes"]
    generous=x["combination"]["irreducible_payload_upper_bound_kg"]+fraction*1.15*x["deficit"]["concept"]["bill_kg"]["SiC_tubes"]
    x["combination"]["058_full_relief_fraction_given_for_free"]=fraction
    x["combination"]["relief_generous_payload_upper_bound_kg"]=generous
    if generous>=0: raise AssertionError(("P3 relief certificate",r,x["weather"],generous))
    # Give the entire 058 full-to-trim tube saving to an already lighter 057
    # frame. All film, sleeves, nodes and cavity hardware have already been
    # removed in this impossibility bound; real designs are heavier.

d["058_repricing"]=operation
d["source_corrections"]=[
 {"id":"SC061-TRL7","tag":"QUESTIONABLE","source":"NASA GSFC IDC Table VI-1, NTRS 20120013284, PDF p10",
  "finding":"TRL7 brackets/clips/hardware is 5%; 6% is the adjacent battery column.",
  "previous_057_CHECK057_hardware_rate":.06,"correct_hardware_rate":.05,
  "correct_battery_rate":.06,"scope":"only maturity results; primary concept factors unchanged",
  "evidence":"sources/NASA2012.pdf and sources/NASA2012-table.png",
  "independent_review":"pending REVIEW-A"},
 {"id":"SC061-LARGE-R","tag":"PROJECTION","finding":"R20/R30 040-transfer geometry omits cure compression from global demand; 061 includes it, as direct048 does.",
  "effect":"new scalar-model scenario, not a claim of validated residual-field mechanics",
  "independent_review":"pending REVIEW-A"}]
d["numerical_fixes"]=fixes
d["arithmetic_audit"]=audit
d["beryllium"]=[]
for x in d["p2"]:
    if x["basis"]!="endpoint" or x["R_m"] not in (20,30):continue
    p=x["deficit"]["none"]
    mass=p["bill_kg"]["faces"]
    d["beryllium"].append({"R_m":x["R_m"],"weather":x["weather"],"nominal_face_Be_kg":mass,
                          "concept_face_budget_kg":1.15*mass,
                          "world_mine_output_2025_kg_Be":430000.,
                          "nominal_share_percent":100*mass/430000,
                          "concept_face_budget_share_percent":100*1.15*mass/430000,
                          "source":"USGS Mineral Commodity Summaries 2026, Beryllium",
                          "tag":"QUESTIONABLE / PROJECTION",
                          "excludes":"fabrication scrap, yield loss, spare stock; denominator is not sheet supply"})
d["completed"]=datetime.now().astimezone().isoformat()
(ROOT/"CALCULATIONS.json").write_text(json.dumps(d,indent=2,allow_nan=False)+"\n")
print("AUDIT COMPLETE",len(audit),"closure witnesses;",len(fixes),"numerical fixes",flush=True)
