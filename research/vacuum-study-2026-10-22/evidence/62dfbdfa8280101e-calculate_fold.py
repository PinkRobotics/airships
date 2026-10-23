#!/usr/bin/env python3
"""Cure-demand reoptimization plus the exact additional exterior-water debit."""
import json
import sys
import time
from datetime import datetime,timezone
from dataclasses import replace
from pathlib import Path
import fold_model as m

B=Path(__file__).resolve().parent
inputs=json.loads((B/"INPUTS.json").read_text())
BASE=Path(inputs["original_048_directory"])
name=sys.argv[1]
m.THERMAL=json.loads((B/"inputs/048/THERMAL-TABLES.json").read_text())[name]
original=json.loads((BASE/f"RESULTS-{name}.json").read_text())
rows=[x for x in original["rows"] if x["external_water_kg_m2"]==.1]
output=[];pairs=[];bounds=[]
started=datetime.now(timezone.utc).isoformat();clock=time.monotonic()

def trials_water(source,cure):
    out=[]
    for trial in source["least"]["endpoint_trials"]:
        p=trial["solution"]
        if p is None:
            out.append(trial);continue
        s=replace(m.Settings(**p["settings"]),external_water_kg_m2=1.,cure_in_global=cure)
        point=m.payload_at(p["R_m"],p["geometry"]["tf_m"],p["geometry"]["tc_m"],
                           p["mask"],p["usage"],s,True)
        out.append(dict(mask=trial["mask"],axes=trial["axes"],
                        payload_kg=point["signed_payload_kg"],solution=point))
    return out

for source in rows:
    r=source["R_m"]
    s=replace(m.Settings(**source["two_factor_endpoint"]["settings"]),cure_in_global=True)
    result=m.least(r,s)
    point=next(x["solution"] for x in result["endpoint_trials"] if x["mask"]==11)
    current={**{k:source[k] for k in ["profile","R_m","weather","floor","drying","external_water_kg_m2"]},
             "id":source["id"]+"-cure_included",
             "cure_in_global":True,"least":result,"two_factor_endpoint":point}
    output.append(current)
    all4=next(x["solution"] for x in result["endpoint_trials"] if x["mask"]==15)
    oldall4=next(x["solution"] for x in source["least"]["endpoint_trials"] if x["mask"]==15)
    pairs.append(dict(id=source["id"],original_endpoint=source["two_factor_endpoint"],
                      cure_endpoint=point,original_all4=oldall4,cure_all4=all4,
                      original_least=source["least"]["least"],cure_least=result["least"],
                      delta_endpoint_kg=point["signed_payload_kg"]-source["two_factor_endpoint"]["signed_payload_kg"],
                      delta_all4_kg=all4["signed_payload_kg"]-oldall4["signed_payload_kg"]))
    # Lower-cardinality E subsets need a favorable capacity/thermal bound.
    count=result["minimum_axis_count"]
    for trial in result["endpoint_trials"]:
        mask=trial["mask"]
        if not mask&4 or (count is not None and mask.bit_count()>=count):
            continue
        upper=m.optimize(r,mask,1,replace(s,thermal_modulus_Pa=m.F["E_today_Pa"]),n=700)
        val=None if upper is None else upper["signed_payload_kg"]
        bounds.append(dict(id=current["id"],type="fewer_axes_relaxed_E",mask=mask,
                           payload_upper_kg=val,excludes_float=val is None or val<0))
    # All 1-mm endpoints retain their existing optimum because water's
    # change is constant in tf,tc. The favorable full-tuple bound also
    # excludes intermediate E/thermal choices and every smaller subset.
    for old,cure in [(source,False),(current,True)]:
        heavytrials=trials_water(old,cure)
        hs=replace(s,cure_in_global=cure,external_water_kg_m2=1.,
                   thermal_modulus_Pa=m.F["E_today_Pa"])
        upper=m.optimize(r,15,1,hs,n=800)
        value=None if upper is None else upper["signed_payload_kg"]
        assert value is None or value<0,(source["id"],cure,value)
        assert all(t["payload_kg"] is None or t["payload_kg"]<0 for t in heavytrials)
        hid=source["id"].replace("retained_water","one_mm_water")+("-cure_included" if cure else "-original_cure_treatment")
        bounds.append(dict(id=hid,type="one_mm_all_axes_upper_bound",mask=15,
                           payload_upper_kg=value,excludes_float=True))
        heavy={**{k:source[k] for k in ["profile","R_m","weather","floor","drying"]},
               "id":hid,"external_water_kg_m2":1.,"cure_in_global":cure,
               "two_factor_endpoint":next(t["solution"] for t in heavytrials if t["mask"]==11),
               "least":dict(status="no float: all endpoints and favorable all-axis bound negative",
                            minimum_axis_count=None,least=None,endpoint_trials=heavytrials),
               "extra_exterior_water_kg":.9*4*m.np.pi*r*r,
               "favorable_payload_upper_kg":value}
        output.append(heavy)
    m.dump(B/f"RESULTS-{name}.json",dict(complete=False,rows=output,pairs=pairs,bounds=bounds))
    l=result["least"]
    print(current["id"],"payload",round(point["signed_payload_kg"],4),
          "least",None if l is None else (l["mask"],round(l["usage"],6)),flush=True)

assert all(x["excludes_float"] for x in bounds)
m.dump(B/f"RESULTS-{name}.json",dict(
    tag="QUESTIONABLE / PROJECTION",complete=True,rows=output,pairs=pairs,bounds=bounds,
    started_at=started,finished_at=datetime.now(timezone.utc).isoformat(),
    elapsed_s=time.monotonic()-clock,profile=name,
    notes=["Temperature tables are the filed 048 inputs; no thermal-boundary closure is asserted.",
           "The water scenarios are retained service liquid; none of the three material dry-out routes proves an exterior retention limit.",
           "Original filed 048 artifacts remain unchanged."]))
print("complete",name,len(output),flush=True)
