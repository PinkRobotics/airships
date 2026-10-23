"""Explicit fresh-FE sections at mechanical SF >= 1; no optimality claim."""
from pathlib import Path
import gc
import json
from material_models import models
from frame_fe import solve
from frame_compare import BASE,score,load_data

ROOT=Path(__file__).resolve().parent
rows=[]
for mat in models():
    for reserve in ["5","019"]:
        x=solve(mat,reserve,6,"minimum_wall_q1_screen")
        attempt=0
        while x["conditional_SF_or_ceiling"]<1.00001:
            attempt+=1
            wall=x["wall_m"]*1.01/x["conditional_SF_or_ceiling"]
            assert wall<.1,"Thin-tube witness search has left its geometric domain"
            x=solve(mat,reserve,6,f"verified_q1_{attempt}",wall_override=wall)
            gc.collect()
        d,L,_=load_data(reserve)
        y=score(mat,BASE[reserve],d,L,x["radius_m"],x["wall_m"],x["linear_multipliers"][0])
        y["section_policy"]=x["section_policy"]
        rows.append(dict(tag="QUESTIONABLE / PROJECTION",material=mat["id"],reserve=reserve,
            FE=x,comparison_geometry=y,
            actual_strength_qualified=False,
            label="fresh-FE mechanical screen witness or ceiling; not minimum mass; missing composite failure modes remain"))
        gc.collect()
(ROOT/"WITNESSES.json").write_text(json.dumps(dict(rows=rows),indent=2,allow_nan=False)+"\n")
