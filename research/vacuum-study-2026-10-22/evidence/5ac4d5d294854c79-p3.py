#!/usr/bin/env python3
"""Equilateral P3 on the filed 022b model; independent numerical implementation."""
import json
import math
import time
from pathlib import Path
import numpy as np
from scipy.optimize import differential_evolution, minimize
import atmosphere as at

ROOT=Path(__file__).resolve().parent
I=at.IN
L,A,R,P,V=at.L0,at.A0,at.R,at.P0,at.V0
B=I["nonclimate_kg"]
E,RHO,SIG=410e9,3100.,3900e6
MODES=("yield","euler","local","film","perry","global")


def geometry(s,ro,tf,x,kind="percent",film="projection"):
    filmrho,filmsigma=(970.,1.5e9) if film=="projection" else (1420.,115.5e6)
    nodes=8*math.pi*R*R/(math.sqrt(3)*s*s)+2
    edges=3*nodes-6
    length=2*R*np.arcsin(s/(2*R))
    volume=V*(1-s/(16*R))
    lift=L*volume/V
    C=x*lift
    M=lift-C
    mfilm=A*tf*filmrho
    mnodes=.02*nodes
    ncoef=R*s/(2*math.sqrt(3))
    if kind=="percent":
        assembly=(M-100-B)/1.05
        mjoint=.05*assembly
        mtube=assembly-mfilm-mnodes
    else:
        # Optional load-sized Ti sensitivity. Design load is set by caller.
        q=kind[1]
        mjoint=2*edges*2.950e-14*(P*q*ncoef)**2/ro
        mtube=M-100-B-mjoint-mfilm-mnodes
    area=mtube/(edges*length*RHO)
    valid=(area>0)&(ro*ro>area/math.pi)&(ro<=np.minimum(.25,s/3))
    ri=np.sqrt(np.maximum(1e-24,ro*ro-area/math.pi))
    tw=ro-ri
    iner=.25*math.pi*(ro**4-ri**4)
    return dict(s=s,ro=ro,tf=tf,volume=volume,lift=lift,C=C,carried=M,
                m_film=mfilm,m_nodes=mnodes,m_joint=mjoint,m_tube=mtube,
                nodes=nodes,members=edges,length=length,area=area,I=iner,tw=tw,
                ncoef=ncoef,valid=valid,film_sigma=filmsigma)


def modes(g,sigma=SIG):
    area,iner,ro,tw=g["area"],g["I"],g["ro"],g["tw"]
    with np.errstate(invalid="ignore",divide="ignore",over="ignore"):
        stress=P*g["ncoef"]/area
        euler=math.pi**2*E*(iner/area)/g["length"]**2
        eta=(g["length"]/1000)*ro/(iner/area)
        phi=(sigma+(1+eta)*euler)/2
        # Rationalised Perry root avoids subtraction of nearly equal numbers.
        perry=sigma*euler/(phi+np.sqrt(np.maximum(0.,phi**2-sigma*euler)))
        gamma=1-.901*(1-np.exp(-np.sqrt(np.maximum(0.,ro/tw))/16))
        out={
            "yield":sigma/stress,"euler":euler/stress,
            "local":.6*E*tw/ro*gamma/stress,
            "film":2*g["film_sigma"]*g["tf"]/(g["s"]*P),
            "perry":perry/stress,
            "global":.2*4*math.sqrt(1.5)*E*np.sqrt(np.maximum(0.,iner*area))/(g["s"]*R*R*P),
        }
    return out,gamma


def score(v,x,q,kind="percent",film="projection"):
    s,ro,tf=v
    g=geometry(s,ro,tf,x,kind,film)
    m,_=modes(g)
    z=np.minimum.reduce([m[k] for k in MODES])/q
    return np.where(g["valid"] & np.isfinite(z),z,-1e6)


def optimise(x,q,kind="percent",film="projection",seed=31):
    tmin=8e-5 if film=="projection" else 25e-6
    bounds=[(.4,8.),(.003,.25),(tmin,.0025)]
    result=differential_evolution(
        lambda v:-score(v,x,q,kind,film),bounds,vectorized=True,
        updating="deferred",seed=seed,popsize=22,maxiter=450,tol=2e-9,
        polish=False)
    polish=minimize(lambda v:-float(score(v,x,q,kind,film)),result.x,
                    method="Nelder-Mead",bounds=bounds,
                    options=dict(maxiter=2500,xatol=1e-12,fatol=1e-12))
    v=polish.x if polish.fun<result.fun else result.x
    return v,dict(seed=seed,nfev=int(result.nfev),iterations=int(result.nit),
                  success=bool(result.success),polish_success=bool(polish.success))


def describe(v,x,envelope,kind="percent",film="projection"):
    q=max(1.,float(at.demand(x*L,envelope)[0]))
    g=geometry(*v,x,kind,film)
    m,gamma=modes(g)
    m={k:float(m[k]) for k in MODES}
    volume=float(g["volume"])
    return dict(
        envelope=envelope,film=film,joints=kind,x=x,
        spacing_m=float(g["s"]),outer_radius_m=float(g["ro"]),
        wall_m=float(g["tw"]),film_m=float(g["tf"]),arc_length_m=float(g["length"]),
        rt=float(g["ro"]/g["tw"]),gamma_local=float(gamma),
        section_area_m2=float(g["area"]),section_I_m4=float(g["I"]),
        nodes=float(g["nodes"]),members=float(g["members"]),
        effective_volume_m3=volume,nominal_effective_lift_kg=float(g["lift"]),
        sag_lost_lift_at_ISA_kg=L-float(g["lift"]),
        C_kg=float(g["C"]),nonclimate_kg=B,systems_kg=100.,
        masses_kg={k:float(g[k]) for k in ("m_film","m_nodes","m_joint","m_tube","carried")},
        nominal_required_SF=q,sfs_at_p0=m,
        sfs_at_required_pressure={k:v/q for k,v in m.items()},
        least_SF=min(m.values())/q,
        reserve_kg=B+float(g["C"])+L-float(g["lift"]),
        reserve_fraction=(B+float(g["C"])+L-float(g["lift"]))/L,
        days=[at.row(float(g["carried"]),volume,d,m) for d in at.selected(envelope)])


def held_point(source,label):
    s=source["s_m"]
    volume=V*(1-s/(16*R))
    # reserve includes absent climate and sag; nonclimate lines are carried.
    mass=source["vehicle"]+B
    sf={k:source["SF_"+k] for k in MODES}
    return dict(label=label,source=source,carried_mass_kg=mass,effective_volume_m3=volume,
                nominal_effective_lift_kg=L*volume/V,
                nominal_climate_headroom_kg=L*volume/V-mass,sfs_at_p0=sf,
                days=[at.row(mass,volume,d,sf) for d in at.DAYS])


def main():
    t0=time.monotonic()
    p=I["reference_022b_gamma"]["cases"]["percent_crush_019"]["equilateral"]
    x=I["inherited_climate_allowance_kg"]/(L*(1-p["s_m"]/(16*R)))
    v=[p["s_m"],p["r_o_m"],p["t_film_m"]]
    reproduction=describe(v,x,"optimistic")
    for k in MODES:
        assert abs(reproduction["sfs_at_p0"][k]-p["SF_"+k])<1e-8,(k,reproduction["sfs_at_p0"][k],p["SF_"+k])
    held=[held_point(p,"022b_percent_019_held")]
    for label in ["ti_kapton_019","cfrp_zylon_019"]:
        pp=I["reference_022b_fold"]["cases"][label]["equilateral"]
        # Sized-joint source does not write vehicle, but reserve is explicit.
        if "vehicle" not in pp:
            pp=dict(pp,vehicle=L-pp["reserve"])
        held.append(held_point(pp,"022b_"+label+"_held"))
    rows=[]
    for env in ["optimistic","all_019"]:
        for floor in [None,10.,100.,500.]:
            x=at.floor_C(floor,env)/L
            q=max(1.,float(at.demand(x*L,env)[0]))
            v,details=optimise(x,q)
            row=describe(v,x,env)
            row.update(altitude_floor_m=floor,optimisation=details)
            rows.append(row)
            print(env,floor,"C",round(row["C_kg"],3),"s",round(row["spacing_m"],6),
                  "SF",round(row["least_SF"],6),flush=True)
    # The filed non-projection film/joint pairing remains conditional on 3900 MPa.
    sensitivities=[]
    for env in ["optimistic","all_019"]:
        x=at.floor_C(100.,env)/L
        q=max(1.,float(at.demand(x*L,env)[0]))
        v,details=optimise(x,q,kind=("ti",q),film="kapton",seed=1031)
        row=describe(v,x,env,kind=("ti",q),film="kapton")
        row.update(altitude_floor_m=100.,optimisation=details,
                   caveat="SiC 3900MPa remains PROJECTION; Ti joint sized at peak pressure, not just p0.")
        sensitivities.append(row)
    out=dict(schema=1,card="MAINLINE-031 P3",status="ESTIMATE",tag="QUESTIONABLE",
             projection=True,certification=False,source_reproduction=reproduction,
             source_fixed=held,reoptimised=rows,sensitivities=sensitivities,
             elapsed_s=time.monotonic()-t0)
    (ROOT/"P3.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print("P3 complete",round(out["elapsed_s"],2),"s")


if __name__=="__main__":
    main()
