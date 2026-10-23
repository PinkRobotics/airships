#!/usr/bin/env python3
"""CHECK-029 fold: native target controls for a stated regularized core law."""
import csv,json,math
from campaign import execute
from core_collect import collect_core
from data_tools import ROOT,P0,at_pressure,rms_factor

CONFIG=dict(ntheta=512,grading=2,nface=2,ncore=6,cores=4,inplane=1,
            core_output=1,increment=.2,maximum_increment=.2,service_fraction=.8)
def core_at(name,p):
    d=ROOT/"runs"/name
    if not (d/"CORE-SUMMARY.json").exists():collect_core(d)
    rows=list(csv.DictReader((d/"CORE-PATH.csv").open()))
    for row in rows:
        if abs(float(row["p_kPa"])-p)<1e-4:
            return {k:float(v) for k,v in row.items() if v!=""}
    return None

def group(old,cold=False):
    label,m,w=old["label"],old["meridian"],old["width_mm"]
    file=ROOT/f"core-boundary-{'cold-' if cold else ''}{label}-{m}.json"
    if file.exists():return json.loads(file.read_text())
    cache={}
    def evaluate(a):
        a=round(float(a),6)
        if a in cache:return cache[a]
        name=f"crt-{label}-{m}-a{a:.6f}" if a else f"crt-perfect-{m}"
        job=dict(CONFIG,name=name,amplitude=a,width=w,meridian=m,
                 yield_stress=10000,pressure=P0*1.05/1000)
        execute(job)
        out=dict(amplitude_mm=a,run=name,targets={})
        for sf in [1.,1.05]:
            target=P0*sf;n=name
            face=at_pressure(n,target);core=core_at(n,target)
            if face is None or core is None or not face["interpolation"].startswith("native"):
                direct=dict(job,name=name+f"-SF{sf:g}",pressure=target/1000)
                direct.pop("service_fraction",None)
                execute(direct);n=direct["name"]
                face=at_pressure(n,target);core=core_at(n,target)
            assert face and core and face["interpolation"].startswith("native")
            out["targets"][str(sf)]=dict(run=n,face=face,core=core)
        cache[a]=out
        return out
    evaluate(0)
    y=341.5897774303177 if cold else 345.
    answers=[]
    tolerance=.02 if label!="fullwave" else .1
    for sf in [1.,1.05]:
        oldb=next(b for b in old["boundaries"] if b["SF"]==sf)
        evaluate(oldb["passing_amplitude_mm"]);evaluate(oldb["failing_amplitude_mm"])
        for strength in ["minimum_average","typical"]:
            def f(point):
                t=point["targets"][str(sf)]
                return max(t["face"]["max_mises_MPa"]/y,t["core"][strength+"_index"])-1
            assert f(cache[0])<0,"Perfect target fails"
            for iteration in range(30):
                lo=max((p for p in cache.values() if f(p)<=0),key=lambda p:p["amplitude_mm"])
                ups=[p for p in cache.values() if f(p)>0 and p["amplitude_mm"]>lo["amplitude_mm"]]
                if not ups:
                    evaluate(lo["amplitude_mm"]*1.1+2*tolerance);continue
                hi=min(ups,key=lambda p:p["amplitude_mm"])
                a,b=lo["amplitude_mm"],hi["amplitude_mm"]
                estimate=a-f(lo)*(b-a)/(f(hi)-f(lo))
                if b-a<=tolerance*1.001:
                    lp,hp=lo["targets"][str(sf)],hi["targets"][str(sf)]
                    governing="face_yield" if hp["face"]["max_mises_MPa"]/y>=hp["core"][strength+"_index"] else "core_shear"
                    answers.append(dict(SF=sf,face_yield_MPa=y,strength_basis=strength,
                        status="tested_three_limit_boundary",governing=governing,
                        amplitude_estimate_mm=estimate,passing_amplitude_mm=a,failing_amplitude_mm=b,
                        passing_run=lp["run"],failing_run=hp["run"],
                        passing_face_MPa=lp["face"]["max_mises_MPa"],failing_face_MPa=hp["face"]["max_mises_MPa"],
                        passing_core_shear_MPa=lp["core"]["max_core_shear_MPa"],
                        failing_core_shear_MPa=hp["core"]["max_core_shear_MPa"],
                        passing_core_index=lp["core"][strength+"_index"],failing_core_index=hp["core"][strength+"_index"],
                        passing_core_compression_MPa=lp["core"]["max_core_compression_MPa"],
                        pressure_kPa=P0*sf,rms_estimate_mm=estimate*rms_factor(w),
                        rms_bracket_mm=[a*rms_factor(w),b*rms_factor(w)]))
                    break
                left=max(a,estimate-.45*tolerance);right=min(b,estimate+.45*tolerance)
                if right-left<.1*tolerance:evaluate((a+b)/2)
                else:evaluate(left);evaluate(right)
            else:raise RuntimeError("Unresolved core/face boundary")
    out=dict(label=label,meridian=m,width_mm=w,config=CONFIG,
        criterion="min(endpoint,first face yield,first core shear failure); target load cap reached on pre-yield branch",
        core_law="orthotropic StVK; Ein=1 MPa, Gin=.5 MPa; En=GL=103.4213594, GW=46.88434959 MPa; zero Poisson",
        boundaries=answers,evaluations=sorted(cache.values(),key=lambda p:p["amplitude_mm"]))
    file.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(dict(group=file.name,boundaries=answers)),flush=True)
    return out
def main():
    old=json.loads((ROOT/"BOUNDARIES.json").read_text());groups=[]
    for g in old:
        groups.append(group(g))
        (ROOT/"CORE-BOUNDARIES.json").write_text(json.dumps(groups,indent=2)+"\n")
    governing=min(groups,key=lambda g:min(b["amplitude_estimate_mm"] for b in g["boundaries"] if b["SF"]==1))
    cold=group(governing,cold=True)
    (ROOT/"CORE-THERMAL.json").write_text(json.dumps(cold,indent=2)+"\n")
if __name__=="__main__":main()
