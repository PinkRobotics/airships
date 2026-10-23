"""Local continuous checks of the filed C2b O5 grid point.

The adequate, cap-like, non-heavy branch is held explicitly. These are
constructive feasible points, not proofs of global optimality.
"""
import json
import numpy as np
from scipy.optimize import minimize, brentq
from rederive import OUT, OWNER, model, score, LIFT


def design(x):
    f,c,m,s=map(float,x[:4])
    return model("C2b",2.04,f/1000,c/1000,m*1000,s*100,0.)


def constraints(x, target=1, budget=None):
    v=design(x)
    sf=score(v,True,True)
    z=x[4] if budget else target
    result=[s-z for s in sf.values()]
    result += [v["gamma_s"]/10-1,v["lam_panel"]-2.000001,28-v["psi"]]
    if budget:
        result += [(budget-v["masses"]["total"])/1000]
    return np.array(result)


def run():
    filed=json.loads((OWNER/"RUNS.json").read_text())["concepts"][-1]
    starts=[filed["lift_shift_kg"]["today_O5"]["design"],filed["best_today_O5"]]
    result=[]
    for mode in ["mass","float"]:
        for i,s in enumerate(starts):
            x=[s["tf_mm"],s["tc_mm"],s["lattice_kg"]/1000,s["section"]["shape_param"]/100]
            bounds=[(.25,2),(2,100),(.02,3),(.3,3)]
            if mode=="float":
                x += [.5];bounds += [(0,2)]
            res=minimize((lambda v:design(v)["masses"]["total"]/1000) if mode=="mass" else (lambda v:-v[4]),
                         x,method="SLSQP",bounds=bounds,
                         constraints=[dict(type="ineq",fun=lambda v:constraints(v,budget=LIFT if mode=="float" else None))],
                         options=dict(maxiter=1000,ftol=2e-12))
            d=design(res.x)
            # Re-evaluate the unmodified thresholded model, slightly inside the boundary.
            # SLSQP's boundary may be 1e-12 below gamma_s=10; report this rounding issue.
            sf=score(d,True,True)
            result.append(dict(mode=mode,start=i,success=bool(res.success),message=res.message,
                               iterations=res.nit,least_SF=min(sf.values()),SF=sf,
                               min_constraint=float(min(constraints(res.x,budget=LIFT if mode=="float" else None))),
                               mass_shift_kg=d["masses"]["total"]-LIFT,design=d))
    (OUT/"CONTINUOUS-CHECK.json").write_text(json.dumps(result,indent=2)+"\n")
    constructive=[]
    for mode in ["mass","float"]:
        d=next(x["design"] for x in result if x["mode"]==mode)
        # Move inside gamma_s >= 10, and evaluate using the original branch rule.
        scale=1.000001
        f=d["tf_mm"]/1000*scale
        c=d["tc_mm"]/1000*scale
        ml=d["lattice_kg"]*scale**2
        shape=d["shape"]
        if mode=="float":
            f=brentq(lambda t:model("C2b",2.04,t,c,ml,shape,10.)["masses"]["total"]-LIFT,
                     f*.99,f*1.01,xtol=1e-16)
        v=model("C2b",2.04,f,c,ml,shape,10.)
        sf=score(v,True,True)
        assert v["adequate"] and v["cap_regime"] and not v["heavy"]
        assert min(sf.values()) >= 1 if mode=="mass" else abs(v["masses"]["total"]-LIFT)<1e-6
        constructive.append(dict(mode=mode,least_SF=min(sf.values()),SF=sf,
                                 mass_shift_kg=v["masses"]["total"]-LIFT,design=v))
    (OUT/"CONSTRUCTIVE-POINTS.json").write_text(json.dumps(constructive,indent=2)+"\n")
    print(json.dumps([{k:v for k,v in x.items() if k not in ["SF","design"]} for x in result],indent=2))
    print(json.dumps([{k:v for k,v in x.items() if k not in ["SF","design"]} for x in constructive],indent=2))


if __name__=="__main__":
    run()
