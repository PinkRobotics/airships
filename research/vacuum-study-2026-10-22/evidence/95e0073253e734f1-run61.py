import json
import math
from datetime import datetime
from model61 import *
from source61 import ROOT

results={"tag":"QUESTIONABLE / PROJECTION","qualified_hull_SF":None,
         "p2":[],"p3":[],"frozen_check057":[]}
for r in (12,20,30):
    for w in ("ISA","optimistic"):
        origin=next(x for x in CHECK if x["lead"]=="P2" and x["R_m"]==r and x["weather"]==w
                    and x.get("floor") is False and
                    x["source"]==("048" if r==12 else "040 with 048 finish transfer"))
        b=next(x["bill"] for x in origin["masks"] if x["mask"]==15)
        results["frozen_check057"].append({
            "lead":"P2","R_m":r,"weather":w,"source":origin["source"],"bill_kg":b,
            "payloads_kg":{m:L10*(r/10)**3-sum(b.values())-sum(growth(b,"P2",m).values())
                           for m in ("none","TRL7","concept")}})
        cases={m:p3(r,w,maturity=m) for m in ("none","TRL7","concept")}
        single=[]
        for prop in ("SiC_strength","ply_strength","retention","film_mass","node_mass"):
            cap=1/cases["concept"]["retention"] if prop=="retention" else 1e12
            end=p3(r,w,{prop:cap})
            single.append({"property":prop,"status":"not alone" if end["payload_kg"]<0 else "root needed",
                           "factor":None,"limit_factor":cap,"limit_payload_kg":end["payload_kg"],
                           "next_mode":"local tube-shell compression and remaining complete mass bill",
                           "solution":end})
        freefilm=p3(r,w,{"SiC_strength":1e12,"ply_strength":1e12,
                         "retention":1/cases["concept"]["retention"],
                         "film_mass":1e12,"node_mass":1e12})
        # Favorable impossibility certificate: remove every film, node, joint and
        # cavity gram as well. The unchanged minimum SiC tube area still binds.
        baseline=cases["concept"]
        irreducible_names=("SiC_tubes","systems","vacuum_service","gas","exterior_water",
                           "contamination","mooring_load_introduction","sag_lift_debit",
                           "weather_headroom")
        irreducible=sum(baseline["bill_kg"][k]+baseline["growth_kg"][k] for k in irreducible_names)
        tube_weight=baseline["bill_kg"]["SiC_tubes"]*1.15
        remainder=sum(baseline["bill_kg"].values())+sum(baseline["growth_kg"].values())-tube_weight
        missing=tube_weight/(baseline["lift_kg"]-remainder)
        results["p3"].append({"R_m":r,"weather":w,"deficit":cases,"single":single,
                              "combination":{"status":"no finite product within the named levers and inherited family",
                                             "factor_product":None,"infinite_improvements":freefilm,
                                             "irreducible_mass_kg":irreducible,
                                             "irreducible_payload_upper_bound_kg":baseline["lift_kg"]-irreducible},
                              "additional_tube_mass_reduction_factor_if_other_items_fixed":missing})
for basis in ("endpoint","handbook"):
    for r in (12,20,30):
        for w in ("ISA","optimistic"):
            entry={"R_m":r,"weather":w,"basis":basis}
            entry["deficit"]={m:p2_opt(r,w,basis=basis,maturity=m,n=260)
                              for m in ("none","TRL7","concept")}
            entry["single"]=[]
            for prop in P2PROPS:
                s=single_p2(r,w,prop,basis)
                entry["single"].append(s)
                print(f"P2 {basis} R{r} {w} {prop}: {s['status']} {s.get('factor')}",flush=True)
            entry["combination"]=combination_p2(r,w,basis,entry["single"])
            entry["without_growth_single"]=[single_p2(r,w,p,basis,"none")
                                            for p in ("face_density","face_modulus","gamma")]
            results["p2"].append(entry)
            (ROOT/"CALCULATIONS.json").write_text(json.dumps(results,indent=2,allow_nan=False)+"\n")
            print(f"COMBINED {basis} R{r} {w}: {entry['combination']['factor_product']}",flush=True)
results["completed"]=datetime.now().astimezone().isoformat()
(ROOT/"CALCULATIONS.json").write_text(json.dumps(results,indent=2,allow_nan=False)+"\n")
