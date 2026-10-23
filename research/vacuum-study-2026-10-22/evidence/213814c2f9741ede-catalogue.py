#!/usr/bin/env python3
"""Additional family envelope over inherited fully scored aluminium rows."""
import json
from pathlib import Path
import numpy as np
from compute import I, optimum, payload_at_one, evaluate

ROOT=Path(__file__).resolve().parent
original=I["cores"]["aluminium"]
rows=[]
scores=[]
checks=[]
try:
    for scenario,mass in (("optimistic","coupled"),("conservative","coupled"),
                          ("conservative","coupled_pump_scaled")):
        for r in I["radii_m"]:
            for mechanical in ("chain_design","full_021"):
                trials=[]
                payloads=[]
                for core in I["aluminium_candidates"]:
                    I["cores"]["aluminium"]=core
                    p=optimum(r,scenario,"aluminium",mechanical,mass)
                    trials.append(p)
                    scores.append(dict(radius_m=r,scenario=scenario,mass_model=mass,
                                       mechanical=mechanical,core=core["name"],
                                       feasible=p["feasible"],least_SF=p.get("least_SF")))
                    if p["feasible"] and p["least_SF"]>=1:
                        py=payload_at_one(r,scenario,"aluminium",mechanical,mass)
                        py["core"]=core["name"]
                        payloads.append(py)
                feasible=[p for p in trials if p["feasible"]]
                if not feasible:
                    rows.append(trials[0])
                    continue
                best=max(feasible,key=lambda x:x["least_SF"])
                core=next(c for c in I["aluminium_candidates"] if c["name"]==best["core"])
                best["core_property_basis"]=core["source"]
                I["cores"]["aluminium"]=core
                dense=evaluate(np.linspace(1e-8,1-1e-8,100001),r,scenario,"aluminium",mechanical,mass)
                assert best["least_SF"]>=float(dense["least"].max())-1e-8
                best["family_payload_at_SF1"]=max(payloads,key=lambda p:p["maximum_payload_kg"]) if payloads else dict(
                    reaches_SF1=False,maximum_payload_kg=None)
                checks.append(dict(radius_m=r,scenario=scenario,mass_model=mass,mechanical=mechanical,
                                   core=best["core"],dense_SF=float(dense["least"].max()),best_SF=best["least_SF"]))
                rows.append(best)
finally:
    I["cores"]["aluminium"]=original
out=dict(schema=1,tag="QUESTIONABLE",mechanical_and_fabrication_tag="PROJECTION",
         scope="Full sourced aluminium family sensitivity; main tables retain the ordered021 core.",
         candidate_count=len(I["aluminium_candidates"]),
         same_sheet_modulus_count=sum(c.get("ec_source")=="sheet" for c in I["aluminium_candidates"]),
         property_transfer_warning="Plascore rows transfer Ec from corresponding Hexcel cores and substitute bare compression for crush; included only as QUESTIONABLE sensitivities.",
         candidates=[c["name"] for c in I["aluminium_candidates"]],
         best_points=rows,all_scores=scores,dense_checks=checks)
(ROOT/"CATALOGUE.json").write_text(json.dumps(out,indent=2)+"\n")
print("Candidates",len(I["aluminium_candidates"]),"geometry searches",len(scores),"best rows",len(rows))
for x in rows:
    if x["scenario"]=="optimistic":
        print(x["radius_m"],x["mechanical"],x["core"],x["least_SF"],
              x["family_payload_at_SF1"]["maximum_payload_kg"])
