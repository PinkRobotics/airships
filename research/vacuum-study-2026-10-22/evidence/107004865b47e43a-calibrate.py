#!/usr/bin/env python3
"""Conditional endpoint-bias transfer, with actual plastic endpoint brackets."""
import json, math
from campaign import execute
from data_tools import ROOT,P0,summary,py_estimate,sampled_boundary,sweep_rows,rms_factor,criterion
from refine import WIDTHS,LABELS

def run_group(label,meridian):
    path=ROOT/f"calibration-{label}-{meridian}.json"
    if path.exists():return json.loads(path.read_text())
    width=WIDTHS[LABELS[label]]
    cache={}
    for r in sweep_rows():
        if r["yield_MPa"]==345 and r["meridian"]==meridian and (
            r["amplitude_mm"]==0 or abs(r["width_mm"]-width)<1e-5):
            cache[r["amplitude_mm"]]=r
    def capacity(r,factor):
        return criterion(r,factor)
    target=P0
    factor=1.1
    tol=.02 if label!="fullwave" else .1
    def evaluate(a):
        a=round(float(a),6)
        if a in cache:return cache[a]
        job=dict(name=f"cal-{label}-{meridian}-a{a:.6f}",amplitude=a,width=width,
                 meridian=meridian,yield_stress=345,ntheta=256,grading=1.5,
                 increment=.02,maximum_increment=.02,cores=4)
        cache[a]=execute(job)
        return cache[a]
    for iteration in range(30):
        points=sorted(cache.items())
        positive=[(a,r) for a,r in points if capacity(r,factor)>=target]
        if not positive:
            result=dict(status="perfect_fails")
            break
        a,lo=max(positive,key=lambda z:z[0])
        upper=[(b,r) for b,r in points if b>a and capacity(r,factor)<target]
        if not upper:
            evaluate(max(a*1.5,a+4*tol))
            continue
        b,hi=min(upper,key=lambda z:z[0])
        pl,ph=capacity(lo,factor),capacity(hi,factor)
        root=a+(target-pl)*(b-a)/(ph-pl)
        if b-a<=tol*1.001:
            result=dict(status="tested_endpoint_bracket",factor=factor,SF=1,
                amplitude_estimate_mm=root,passing_amplitude_mm=a,failing_amplitude_mm=b,
                passing_run=lo["name"],failing_run=hi["name"],
                passing_capacity_kPa=pl,failing_capacity_kPa=ph,
                rms_estimate_mm=root*rms_factor(width),
                rms_bracket_mm=[a*rms_factor(width),b*rms_factor(width)])
            break
        left=max(a,root-.45*tol);right=min(b,root+.45*tol)
        if right-left<.1*tol:evaluate((a+b)/2)
        else:evaluate(left);evaluate(right)
    else:raise RuntimeError(f"calibration boundary not resolved: {label} {meridian}")
    scenarios=[]
    nominal=next(g for g in json.loads((ROOT/"BOUNDARIES.json").read_text())
                 if g["label"]==label and g["meridian"]==meridian)
    for c in [1.,1.0956672714078375,1.0976087904104612,1.1,2.314579767827529,2.458907992895204]:
        for sf in [1,1.05]:
            if c==1:
                ref=next(b for b in nominal["boundaries"] if b["SF"]==sf and b["yield_screen_MPa"]==345)
                b=dict(status="refined_unadjusted_boundary",amplitude_mm=ref["amplitude_estimate_mm"],
                       bracket_mm=[ref["passing_amplitude_mm"],ref["failing_amplitude_mm"]],
                       target_kPa=P0*sf,source="BOUNDARIES.json",
                       note="Use refined target-load results, not coarse yield-bracket midpoint interpolation.")
            else:
                b=sampled_boundary([(a,capacity(r,c)) for a,r in cache.items()],P0*sf)
            scenarios.append(dict(endpoint_divisor=c,SF=sf,**b))
    out=dict(label=label,width_mm=width,meridian=meridian,
             reading="Hypothetical transfer of benchmark pressure-endpoint bias only; first-yield pressure is not recalibrated.",
             refined_10percent_SF1=result,scenarios=scenarios,
             runs=[r["name"] for a,r in sorted(cache.items())])
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(dict(group=f"{label}-{meridian}",result=result)),flush=True)
    return out
if __name__=="__main__":
    rows=[]
    for label in LABELS:
        for m in ["W","L"]:
            rows.append(run_group(label,m))
            (ROOT/"CALIBRATION.json").write_text(json.dumps(rows,indent=2)+"\n")
