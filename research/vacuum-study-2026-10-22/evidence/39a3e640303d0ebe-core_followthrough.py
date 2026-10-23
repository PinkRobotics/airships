#!/usr/bin/env python3
"""Serial native confirmation, global conditional calibration, and core-aware sweep."""
import json,math
from campaign import execute
from core_collect import collect_core
from core_refine import CONFIG,core_at
from data_tools import ROOT,P0,summary,py_estimate,rms_factor

def core_summary(name):
    p=ROOT/"runs"/name/"CORE-SUMMARY.json"
    return json.loads(p.read_text()) if p.exists() else collect_core(p.parent)
def full(label,m,w,a,y=345,nu=.0768):
    name=f"cfull-{label}-{m}-y{y:g}-a{a:.6f}-nu{nu:g}"
    job=dict(name=name,amplitude=round(a,6),width=w,meridian=m,nu=nu,
        yield_stress=y,pressure=.18,increment=.02,maximum_increment=.02,
        ntheta=256,grading=1.5,nface=1,ncore=4,cores=4,inplane=1,core_output=1)
    s=execute(job);cs=core_summary(name)
    return s,cs
def capacity(s,c,factor=1):
    pc=c["strength_crossings"]["minimum_average"].get("estimate_kPa",math.inf)
    return min(s["endpoint_kPa"]/factor,py_estimate(s) or math.inf,pc)

def main():
    groups=json.loads((ROOT/"CORE-BOUNDARIES.json").read_text())
    checks=[]
    for sf in [1.,1.05]:
        options=[(b["amplitude_estimate_mm"],g,b) for g in groups for b in g["boundaries"]
                 if b["SF"]==sf and b["strength_basis"]=="minimum_average"]
        _,g,b=min(options,key=lambda q:q[0])
        for side in ["passing","failing"]:
            job=dict(CONFIG,name=f"cnative-SF{sf:g}-{side}",amplitude=b[side+"_amplitude_mm"],
                width=g["width_mm"],meridian=g["meridian"],yield_stress=345,
                pressure=P0*sf/1000,increment=.05,maximum_increment=.05)
            job.pop("service_fraction",None)
            s=execute(job);c=core_summary(s["name"])
            yielded=s["endpoint_max_peeq"]>1e-10;core_failed=c["endpoint"]["minimum_average_index"]>1
            ok=s["endpoint_kind"]=="load_cap" and ((not yielded and not core_failed) if side=="passing" else (yielded or core_failed))
            checks.append(dict(kind="native_boundary",SF=sf,side=side,run=s["name"],passed=ok,
                yielded=yielded,core_failed=core_failed,amplitude_mm=job["amplitude"],
                core_index=c["endpoint"]["minimum_average_index"]))
        if sf==1:
            for n in ["angular","layers","inherited"]:
                job=dict(CONFIG,name="core-control-"+n,amplitude=b["passing_amplitude_mm"],
                    width=g["width_mm"],meridian=g["meridian"],yield_stress=10000,
                    pressure=P0/1000)
                job.pop("service_fraction",None)
                if n=="angular":job["ntheta"]=1024
                if n=="layers":job.update(nface=4,ncore=8)
                if n=="inherited":job["inplane"]=.01
                s=execute(job);c=core_summary(s["name"])
                checks.append(dict(kind="control_"+n,run=s["name"],passed=True,
                    reference=b["passing_run"],face_MPa=s["endpoint_max_mises_MPa"],
                    core_shear_MPa=c["endpoint"]["max_core_shear_MPa"],
                    core_index=c["endpoint"]["minimum_average_index"],
                    note="Measured sensitivity, not a universal error bound. Inherited law is not reinstated."))
    (ROOT/"CORE-CHECKS.json").write_text(json.dumps(checks,indent=2)+"\n")
    assert all(c["passed"] for c in checks)
    # Perfect lower-strength runs and a zero for endpoint transfer, same stated core.
    for m in ["W","L"]:
        for y in [255,300,345]:full("perfect",m,groups[0]["width_mm"],0,y)

    # A common-amplitude bracket over all eight footprints needs one failing
    # footprint and a passing native solve for every footprint.
    old=json.loads((ROOT/"CALIBRATION.json").read_text())
    initial=min(old,key=lambda g:g["refined_10percent_SF1"]["amplitude_estimate_mm"])
    candidate=next(g for g in groups if (g["label"],g["meridian"])==(initial["label"],initial["meridian"]))
    cache={}
    def evalg(g,a):
        a=round(float(a),6);key=(g["label"],g["meridian"],a)
        if key not in cache:
            s,c=full(*key[:2],g["width_mm"],a)
            cache[key]=dict(run=s["name"],amplitude_mm=a,capacity_kPa=capacity(s,c,1.1),
                           endpoint_kPa=s["endpoint_kPa"],face_yield_bracket=s["first_yield_bracket_kPa"],
                           core_shear_crossing=c["strength_crossings"]["minimum_average"])
        return cache[key]
    def resolve(g,seed):
        points=[dict(amplitude_mm=0,capacity_kPa=capacity(*full("perfect",g["meridian"],g["width_mm"],0),1.1))]
        assert points[0]["capacity_kPa"]>=P0
        for a in seed:points.append(evalg(g,a))
        for i in range(30):
            lo=max((p for p in points if p["capacity_kPa"]>=P0),key=lambda p:p["amplitude_mm"])
            hi=min((p for p in points if p["capacity_kPa"]<P0 and p["amplitude_mm"]>lo["amplitude_mm"]),
                   key=lambda p:p["amplitude_mm"],default=None)
            if hi is None:points.append(evalg(g,lo["amplitude_mm"]+.04));continue
            a,b=lo["amplitude_mm"],hi["amplitude_mm"]
            estimate=a+(P0-lo["capacity_kPa"])*(b-a)/(hi["capacity_kPa"]-lo["capacity_kPa"])
            if b-a<=.02001:return dict(group=g["label"],meridian=g["meridian"],width_mm=g["width_mm"],
                passing=lo,failing=hi,estimate_mm=estimate,rms_estimate_mm=estimate*rms_factor(g["width_mm"]))
            for value in [max(a,estimate-.009),min(b,estimate+.009)]:
                point=evalg(g,value)
                if point not in points:points.append(point)
        raise RuntimeError("Calibration bracket not resolved")
    seed=initial["refined_10percent_SF1"]
    result=resolve(candidate,[seed["passing_amplitude_mm"],seed["failing_amplitude_mm"]])
    for iteration in range(8):
        passing=[];failure=None
        for g in groups:
            p=evalg(g,result["passing"]["amplitude_mm"])
            passing.append(dict(label=g["label"],meridian=g["meridian"],width_mm=g["width_mm"],**p))
            if p["capacity_kPa"]<P0:failure=g;break
        if failure is None:break
        candidate=failure
        result=resolve(candidate,[result["passing"]["amplitude_mm"]])
    else:raise RuntimeError("Global calibration did not resolve")
    out=dict(factor=1.1,SF=1,criterion="min(endpoint/1.1,first face yield,first minimum-average core shear)",
        global_bracket=result,common_passing_checks=passing,
        caveat="Conditional transfer only; CHECK-029 identifies predecessor foam-law artifacts. This is not physical calibration.")
    (ROOT/"CORE-CALIBRATION.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(dict(stage="core_calibration_done",result=result)),flush=True)
    rows=[]
    for g in groups:
        for a in [1,11.8,46]:
            s,c=full(g["label"],g["meridian"],g["width_mm"],a)
            rows.append(dict(label=g["label"],meridian=g["meridian"],width_mm=g["width_mm"],
                amplitude_mm=a,run=s["name"],endpoint_kPa=s["endpoint_kPa"],
                first_face_yield_bracket_kPa=s["first_yield_bracket_kPa"],
                first_face_yield_estimate_kPa=py_estimate(s),
                first_core_shear=c["strength_crossings"],
                three_limit_estimate_kPa=capacity(s,c),
                endpoint_core_shear_MPa=c["endpoint"]["max_core_shear_MPa"],
                endpoint_core_crush_MPa=c["endpoint"]["max_core_compression_MPa"]))
            (ROOT/"CORE-SWEEP.json").write_text(json.dumps(rows,indent=2)+"\n")
    print(json.dumps(dict(stage="core_followthrough_done",runs=len(rows))),flush=True)
if __name__=="__main__":main()
