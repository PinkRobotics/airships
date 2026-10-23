import json
import math
from pathlib import Path
from model61 import *
from source61 import ROOT

checks = []
for r in (10,12,20,30):
    for weather in ("ISA","optimistic"):
        original = next(x for x in CHECK if x["lead"]=="P2" and x["R_m"]==r
                        and x["weather"]==weather and x.get("floor") is False
                        and x["source"]==("048" if r<=15 else "040 with 048 finish transfer"))
        b = next(x["bill"] for x in original["masks"] if x["mask"]==15)
        tf = b["faces"]/(2*4*math.pi*r*r*1850)
        tc = b["core"]/(4*math.pi*r*r*C["rho"])
        point = p2(r,weather,tf,tc,maturity="none",detail=True)
        checks.append({"lead":"P2","R":r,"weather":weather,
                       "witness_payload_error":point["payload_kg"]-(L10*(r/10)**3-sum(b.values())),
                       "mode_min":min(point["modes"].values()),"binding":point["binding"]})
        opt = p2_opt(r,weather,maturity="none",n=260)
        checks[-1]["reoptimized_payload"] = None if opt is None else opt["payload_kg"]
        checks[-1]["upstream_payload"] = L10*(r/10)**3-sum(b.values())
        print(json.dumps(checks[-1]),flush=True)
for r in (10,12,15):
    for weather in ("ISA","optimistic"):
        reference = next(x for x in source("054","RESULTS.json")["capture"]
                         if x["R_m"]==r and x["weather"]==weather and x["account"]=="endpoint"
                         and x["candidate"]=="SIOX" and x["days"]==7)
        new=p3(r,weather,maturity="none")
        checks.append({"lead":"P3","R":r,"weather":weather,
                       "payload_error":new["payload_kg"]-reference["payload_kg"],
                       "capture_error":new["cavity"]["capture_system_kg"]-reference["capture_system_kg"]})
        print(json.dumps(checks[-1]),flush=True)
(ROOT/"REPRODUCTION.json").write_text(json.dumps(checks,indent=2)+"\n")
