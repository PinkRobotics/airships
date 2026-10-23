#!/usr/bin/env python3
"""Actual-yield-law confirmation at governing tolerance edges, plus endpoint controls."""
import json
from campaign import execute
from data_tools import ROOT,P0,summary

def main():
    bounds=json.loads((ROOT/"BOUNDARIES.json").read_text())
    config=json.loads((ROOT/"REFINE-CONFIG.json").read_text())
    checks=[]
    for sf in [1.,1.05]:
        candidates=[(b["amplitude_estimate_mm"],g,b) for g in bounds
                    for b in g["boundaries"] if b["SF"]==sf and b["yield_screen_MPa"]==345]
        _,g,b=min(candidates,key=lambda x:x[0])
        for side in ["passing","failing"]:
            job=dict(config,name=f"native-boundary-SF{sf:g}-{side}",
                     amplitude=b[side+"_amplitude_mm"],width=g["width_mm"],
                     meridian=g["meridian"],yield_stress=345,pressure=P0*sf/1000,
                     increment=.05,maximum_increment=.05)
            job.pop("service_fraction",None)
            r=execute(job)
            reached=r["endpoint_kind"]=="load_cap"
            yielded=r["endpoint_max_peeq"]>1e-10
            ok=reached and (not yielded if side=="passing" else yielded)
            checks.append(dict(kind="native_actual_yield_law",SF=sf,side=side,
                run=r["name"],passed=ok,target_kPa=P0*sf,
                endpoint_kPa=r["endpoint_kPa"],max_peeq=r["endpoint_max_peeq"],
                amplitude_mm=job["amplitude"],width_mm=job["width"]))
    cal=json.loads((ROOT/"CALIBRATION.json").read_text())
    g=min(cal,key=lambda g:g["refined_10percent_SF1"]["amplitude_estimate_mm"])
    base=g["refined_10percent_SF1"]["passing_run"]
    m=json.loads((ROOT/"runs"/base/"MODEL.json").read_text())
    old=summary(base)
    for mode in ["step","mesh"]:
        job={k:v for k,v in m["args"].items() if v is not None}
        job["name"]="endpoint-check-"+mode
        job["cores"]=4
        if mode=="step":
            job["increment"]=.005;job["maximum_increment"]=.005
        else:
            job["ntheta"]=max(512,2*m["ntheta"]);job["nface"]=2;job["ncore"]=6
        r=execute(job)
        rel=(r["endpoint_kPa"]/old["endpoint_kPa"]-1)
        checks.append(dict(kind="endpoint_"+mode,run=r["name"],reference=base,
            passed=abs(rel)<.01,relative_difference=rel,
            reference_endpoint_kPa=old["endpoint_kPa"],endpoint_kPa=r["endpoint_kPa"],
            note="The actual difference is retained; a <1% check is not a physical calibration or a tolerance error bound."))
    (ROOT/"BOUNDARY-CHECKS.json").write_text(json.dumps(checks,indent=2)+"\n")
    print(json.dumps(checks))
    assert all(c["passed"] for c in checks)
if __name__=="__main__":main()
