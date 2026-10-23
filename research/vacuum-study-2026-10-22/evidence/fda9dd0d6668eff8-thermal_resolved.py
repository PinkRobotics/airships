"""Independent coupled Newton solution of the supplied non-code thermal boundary.

Two global enclosure moments (mean Ti and mean Ti**4) are solved with the local
outer/inner equations. This is independent of the owner's fixed-point code.
"""
import csv
import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial import legendre as lg
from numpy.polynomial import polynomial as poly

ROOT=Path(__file__).resolve().parent
SIGMA=5.670374419e-8
TA=284.9
RHO=1.1672683307461802
RC=16.018463373960138


def forced_h(radius):
    re=RHO*2*(2*radius)/1.79e-5
    return (2+(.4*math.sqrt(re)+.06*re**(2/3))*.71**.4)*.0257/(2*radius)


def state(radius,tc,alpha,epsilon,day=True,nodes=128,legacy=False):
    tc=np.atleast_1d(np.asarray(tc,dtype=float))
    if legacy:
        mu=-1+(np.arange(37)+.5)*2/37
        weights=np.full(37,2/37)
    else:
        mu,weights=lg.leggauss(nodes)
    w=weights/2
    k=130*RC/(2640 if legacy else 2700)
    solar=alpha*(970 if day else 0)*np.maximum(mu,0)
    env=(1+mu)/2*(275 if day else 260)**4+(1-mu)/2*TA**4
    outer=np.full((len(tc),len(mu)),TA)
    inner=outer.copy()
    m1=np.full(len(tc),TA)
    m4=np.full(len(tc),TA**4)
    hf=forced_h(radius)

    def residual_jacobian():
        dt=outer-TA
        hn=1.32*np.maximum(abs(dt),.05)**.25
        h=np.maximum(hf,hn)
        # d[h(T-To_air)]/dT, including the natural-convection derivative.
        dh_flux=np.where((hn>hf)&(abs(dt)>.05),1.25*hn,h)
        u=k/tc[:,None]+.8*SIGMA*m1[:,None]**3
        du=2.4*SIGMA*m1[:,None]**2
        fo=solar-h*dt+epsilon*SIGMA*(env-outer**4)+u*(inner-outer)
        fi=u*(outer-inner)+.2*SIGMA*(m4[:,None]-inner**4)
        a=-dh_flux-4*epsilon*SIGMA*outer**3-u
        d=-u-.8*SIGMA*inner**3
        det=a*d-u**2
        yo=(u*fo-a*fi)/det
        ym1=(u*du*(inner-outer)-a*du*(outer-inner))/det
        ym4=-a*.2*SIGMA/det
        return fo,fi,a,u,du,yo,ym1,ym4

    for iteration in range(60):
        fo,fi,a,u,du,yo,ym1,ym4=residual_jacobian()
        g1=m1-inner@w
        g4=m4-inner**4@w
        grad4=4*inner**3
        a11=1-ym1@w
        a14=-ym4@w
        a41=-(grad4*ym1)@w
        a44=1-(grad4*ym4)@w
        rhs1=-g1+yo@w
        rhs4=-g4+(grad4*yo)@w
        det=a11*a44-a14*a41
        dm1=(rhs1*a44-a14*rhs4)/det
        dm4=(a11*rhs4-rhs1*a41)/det
        di=yo+ym1*dm1[:,None]+ym4*dm4[:,None]
        do=(-fo-u*di-du*(inner-outer)*dm1[:,None])/a
        inner+=di
        outer+=do
        m1+=dm1
        m4+=dm4
        if max(abs(di).max(),abs(do).max())<2e-11:
            break
    else:
        raise ArithmeticError("Thermal Newton iteration failed to converge")
    fo,fi,*_=residual_jacobian()
    pattern=(outer+inner)/2
    # Legacy raw midpoint projection retained to expose its constant-field issue.
    projected=pattern if legacy else pattern-(pattern@w)[:,None]
    coefficients=np.stack([(2*j+1)*(projected*lg.legval(mu,[0]*j+[1]))@w for j in range(7)],axis=1)
    coefficients[:,:2]=0
    angle=np.linspace(0,math.pi,1441)
    cos=np.cos(angle)
    exact,sampled=[],[]
    for coeff in coefficients:
        polynomial=lg.leg2poly(coeff)
        d1,d2=poly.polyder(polynomial),poly.polyder(polynomial,2)
        curvature=poly.polysub(poly.polymul([1,0,-1],d2),poly.polymul([0,1],d1))
        sampled.append(float(abs(poly.polyval(cos,curvature)).max()))
        roots=poly.polyroots(poly.polyder(curvature))
        points=[-1.,1.]+[float(z.real) for z in roots if abs(z.imag)<1e-8 and abs(z.real)<=1]
        exact.append(float(abs(poly.polyval(points,curvature)).max()))
    return dict(outer=outer,inner=inner,curvature=np.array(sampled),curvature_exact=np.array(exact),
                iterations=iteration+1,max_energy_residual_W_m2=float(max(abs(fo).max(),abs(fi).max())),
                mean_constraint_K=float(abs(m1-inner@w).max()),
                fourth_moment_constraint_relative=float((abs(m4-inner**4@w)/m4).max()),
                min_convection_W_m2K=float(np.maximum(hf,1.32*np.maximum(abs(outer-TA),.05)**.25).min()),
                max_convection_W_m2K=float(np.maximum(hf,1.32*np.maximum(abs(outer-TA),.05)**.25).max()))


def thermal(radius,tc,alpha,epsilon,nodes=128,legacy=False):
    day=state(radius,tc,alpha,epsilon,True,nodes,legacy)
    night=state(radius,tc,alpha,epsilon,False,nodes,legacy)
    dg=abs(day["outer"]-day["inner"]).max(axis=1)
    ng=abs(night["outer"]-night["inner"]).max(axis=1)
    hi=day["outer"].max(axis=1)
    lo=night["outer"].min(axis=1)
    diagnostics=lambda x:{k:v for k,v in x.items() if k not in ("outer","inner","curvature","curvature_exact")}
    return dict(tc_m=np.atleast_1d(tc).tolist(),day_gradient_K=dg.tolist(),night_gradient_K=ng.tolist(),
                day_curvature_temperature_K=day["curvature"].tolist(),
                night_curvature_temperature_K=night["curvature"].tolist(),
                gradient_K=np.maximum(dg,ng).tolist(),rise_K=(hi-TA).tolist(),swing_K=(hi-lo).tolist(),
                curvature_temperature_K=np.maximum(day["curvature"],night["curvature"]).tolist(),
                exact_curvature_temperature_K=np.maximum(day["curvature_exact"],night["curvature_exact"]).tolist(),
                max_outer_K=hi.tolist(),min_outer_K=lo.tolist(),
                day_diagnostics=diagnostics(day),night_diagnostics=diagnostics(night))


def main():
    coatings=json.loads((ROOT/"intake/owner/COATINGS.json").read_text())
    published=json.loads((ROOT/"intake/owner/THERMAL-TABLES.json").read_text())
    screens=json.loads((ROOT/"intake/owner/THERMAL-SCREEN.json").read_text())
    geometry=next(x for x in json.loads((ROOT/"intake/base040/inputs/028b/PROPERTY-CHECKS.json").read_text())["full_named_maxima"]
                  if x["route"]=="af015_scarf" and x["material"]=="SR200")["point"]
    comparisons=[]

    def compare(row,field,old,new,rtol=2e-6,atol=3e-8):
        comparisons.append(dict(row=row,field=field,owner=old,independent=new,delta=new-old,
                                agrees=math.isclose(old,new,rel_tol=rtol,abs_tol=atol),rtol=rtol,atol=atol))

    independent={}
    source_screens=[]
    for coating in coatings:
        if coating["alpha"] is None:continue
        key=coating["id"];independent[key]={}
        for radius in (10,12,15):
            tab=published[key][str(radius)]
            own=thermal(radius,tab["tc_m"],coating["alpha"],coating["epsilon"])
            independent[key][str(radius)]=own
            for field,old in tab.items():
                if isinstance(old,list) and field in own:
                    for i,(a,b) in enumerate(zip(old,own[field])):
                        compare(f"{key}-R{radius}",f"{field}[{i}]",a,b)
        legacy=thermal(10,[geometry["tc_m"]],coating["alpha"],coating["epsilon"],legacy=True)
        common=thermal(10,[geometry["tc_m"]],coating["alpha"],coating["epsilon"])
        lag=(23.6e-6-11.3e-6)*math.sqrt(290e9*geometry["tf_m"]*46884349.59354485/geometry["tc_m"])
        kb=.5*67e9*RC/2700
        cure=max(abs(366.4833333333333-common["min_outer_K"][0]),
                 abs(366.4833333333333-common["max_outer_K"][0]))
        own=dict(id=key,legacy=legacy,common=common,
                 legacy_037_day_SF=241316.50526089262/(lag*legacy["rise_K"][0]),
                 legacy_037_full_swing_SF=241316.50526089262/(lag*legacy["swing_K"][0]),
                 current_200F_minimum_edge_SF=172368.93232920903/(1.002*(23.6e-6-11.3e-6)*cure*math.sqrt(2*kb*46884349.59354485)))
        source_screens.append(own)
        old=next(x for x in screens if x["id"]==key)
        for field in ("legacy_037_day_SF","legacy_037_full_swing_SF","current_200F_minimum_edge_SF"):
            compare(key,field,old[field],own[field])
        for kind in ("legacy","common"):
            for field,value in old[kind].items():
                if isinstance(value,list) and field in own[kind]:
                    for i,(a,b) in enumerate(zip(value,own[kind][field])):
                        compare(key,kind+"."+field+f"[{i}]",a,b)
        print(json.dumps(dict(finish=key,done=True)),flush=True)

    supplemental={}
    for key,a,e in [("wet_optics_assumed",.2,.95),("aged_alpha015_assumed",.15,.8),
                    ("aged_alpha020_assumed",.2,.8),("classical_low_emittance",.09,.4)]:
        supplemental[key]={}
        for radius in (10,12,15):
            supplemental[key][str(radius)]=thermal(radius,published["MLCCAg"][str(radius)]["tc_m"],a,e)
    (ROOT/"INDEPENDENT-THERMAL-TABLES.json").write_text(json.dumps(independent,indent=2,allow_nan=False)+"\n")
    (ROOT/"SUPPLEMENTAL-THERMAL-TABLES.json").write_text(json.dumps(supplemental,indent=2,allow_nan=False)+"\n")
    with (ROOT/"THERMAL-RESOLVED-COMPARISONS.csv").open("w") as f:
        writer=csv.DictWriter(f,fieldnames=list(comparisons[0]));writer.writeheader();writer.writerows(comparisons)
    bad=[x for x in comparisons if not x["agrees"]]
    (ROOT/"THERMAL-RESOLVED-RESULTS.json").write_text(json.dumps(dict(
        independent_method="Coupled local Newton plus simultaneous first/fourth enclosure moments",
        boundary_source="intake/addendum048/9-THERMAL-BOUNDARY.md",
        comparisons=len(comparisons),mismatches=bad,screens=source_screens,
        owner_code_accessed=False),indent=2,allow_nan=False)+"\n")
    print(json.dumps(dict(comparisons=len(comparisons),mismatches=len(bad),first=bad[:8])),flush=True)


if __name__=="__main__":
    main()
