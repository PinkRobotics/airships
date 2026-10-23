#!/usr/bin/env python3
"""Admitted adaptive boundary runs; retain tested passing/failing amplitudes."""
import json, math, pathlib, sys
from campaign import execute
from data_tools import ROOT,P0,summary,at_pressure,py_estimate,sampled_boundary,sweep_rows,rms_factor,criterion

WIDTHS=json.loads((ROOT/"WIDTHS.json").read_text())
LABELS={"old021":"old021_mm","current":"current_lambdaI1_mm",
        "old021b":"old021b_mm","fullwave":"full_classical_wavelength_mm"}

def refine_group(label,meridian,config,targets=None,suffix=""):
    width=WIDTHS[LABELS[label]]
    basename=f"boundary{suffix}-{label}-{meridian}"
    completed=ROOT/(basename+".json")
    if completed.exists():
        return json.loads(completed.read_text())
    cache={}
    def evaluate(a):
        a=round(float(a),6)
        if a in cache:return cache[a]
        name=f"tol-{label}-{meridian}-a{a:.6f}" if a else f"tol-perfect-{meridian}"
        job=dict(config,name=name,amplitude=a,width=width,meridian=meridian,
                 yield_stress=10000,pressure=P0*1.05/1000,
                 increment=config.get("increment",1/21),
                 maximum_increment=config.get("maximum_increment",1/21))
        execute(job)
        out=dict(amplitude_mm=a,run=name,at_SF1=at_pressure(name,P0),
                 at_SF105=at_pressure(name,P0*1.05))
        cache[a]=out
        return out
    rows=sweep_rows()
    perfect=next(r for r in rows if r["amplitude_mm"]==0 and r["yield_MPa"]==345 and r["meridian"]==meridian)
    coarse=[(0.,criterion(perfect))]
    coarse += [(r["amplitude_mm"],criterion(r))
               for r in rows if abs(r["width_mm"]-width)<1e-5 and r["meridian"]==meridian and r["yield_MPa"]==345 and r["amplitude_mm"]>0]
    evaluate(0)
    targets=targets or [(1.,345.),(1.05,345.)]
    answers=[]
    tolerance=.02 if label!="fullwave" else .10
    for sf,y in targets:
        field="at_SF1" if sf==1 else "at_SF105"
        def f(point):
            z=point[field]
            return z["max_mises_MPa"]-y if z else math.inf
        if f(cache[0])>0:
            answers.append(dict(SF=sf,yield_screen_MPa=y,status="perfect_fails"))
            continue
        c=sampled_boundary(coarse,P0*sf)
        guess=c.get("amplitude_mm") or .5
        # Two near-boundary trials normally bracket the fine-mesh root.
        evaluate(max(0,guess-2*tolerance))
        evaluate(guess+2*tolerance)
        for iteration in range(30):
            ordered=sorted(cache.values(),key=lambda x:x["amplitude_mm"])
            negative=[p for p in ordered if f(p)<=0]
            positive=[p for p in ordered if f(p)>0]
            lo=max(negative,key=lambda x:x["amplitude_mm"])
            upper=[p for p in positive if p["amplitude_mm"]>lo["amplitude_mm"]]
            if not upper:
                evaluate(max(lo["amplitude_mm"]*1.25,lo["amplitude_mm"]+4*tolerance))
                continue
            hi=min(upper,key=lambda x:x["amplitude_mm"])
            a,b=lo["amplitude_mm"],hi["amplitude_mm"]
            if b-a<=tolerance*1.001:
                estimate=a-f(lo)*(b-a)/(f(hi)-f(lo)) if math.isfinite(f(hi)) else (a+b)/2
                answers.append(dict(SF=sf,yield_screen_MPa=y,status="tested_boundary_bracket",
                    amplitude_estimate_mm=estimate,passing_amplitude_mm=a,failing_amplitude_mm=b,
                    passing_run=lo["run"],failing_run=hi["run"],
                    passing_max_mises_MPa=lo[field]["max_mises_MPa"],
                    failing_max_mises_MPa=hi[field]["max_mises_MPa"] if hi[field] else None,
                    pressure_kPa=P0*sf,rms_estimate_mm=estimate*rms_factor(width),
                    rms_bracket_mm=[a*rms_factor(width),b*rms_factor(width)],
                    interpolation="secant estimate inside tested pass/fail amplitudes; high-yield law is identical before first yield"))
                break
            root=a-f(lo)*(b-a)/(f(hi)-f(lo)) if math.isfinite(f(hi)) else (a+b)/2
            # Evaluate both sides of the predicted root to produce a physical
            # bracket rather than stopping on a small stress residual alone.
            left=max(a,root-.45*tolerance)
            right=min(b,root+.45*tolerance)
            if right-left<.1*tolerance:
                evaluate((a+b)/2)
            else:
                evaluate(left);evaluate(right)
        else:
            raise RuntimeError(f"boundary did not resolve: {label} {meridian} SF {sf}")
    out=dict(label=label,width_mm=width,meridian=meridian,config=config,
             boundaries=answers,evaluations=sorted(cache.values(),key=lambda x:x["amplitude_mm"]))
    completed.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(dict(group=basename,boundaries=answers)),flush=True)
    return out

if __name__=="__main__":
    config=json.loads((ROOT/"REFINE-CONFIG.json").read_text())
    if "--cold-governing" in sys.argv:
        nominal=json.loads((ROOT/"BOUNDARIES.json").read_text())
        selected={}
        for sf in [1.,1.05]:
            options=[(b["amplitude_estimate_mm"],g["label"],g["meridian"])
                     for g in nominal for b in g["boundaries"] if b["SF"]==sf]
            _,label,m=min(options)
            selected.setdefault((label,m),[]).append((sf,341.5897774303177))
        results=[refine_group(label,m,config,targets=targets,suffix="-cold")
                 for (label,m),targets in selected.items()]
        (ROOT/"THERMAL-SENSITIVITY.json").write_text(json.dumps(dict(
            residual_MPa=3.4102225696822703,remaining_yield_screen_MPa=341.5897774303177,
            reading="Conservative local strength debit on the nominal governing width/meridian; no residual-stress stiffness or cure deformation solved. Other widths are not re-optimized under the debit.",
            groups=results),indent=2)+"\n")
        sys.exit(0)
    groups=[]
    for label in LABELS:
        for meridian in ["W","L"]:
            groups.append(refine_group(label,meridian,config))
            (ROOT/"BOUNDARIES.json").write_text(json.dumps(groups,indent=2)+"\n")
