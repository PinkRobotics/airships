#!/usr/bin/env python3
"""Independent scalar Decimal capacities; ODE atmosphere; denser optimiser checks."""
import hashlib
import json
import math
import time
from decimal import Decimal as D, localcontext
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import atmosphere as at
import p2
import p3

ROOT=Path(__file__).resolve().parent
P2=json.loads((ROOT/"P2.json").read_text())
P3=json.loads((ROOT/"P3.json").read_text())
dd=lambda x:D(str(x))
MAX={}
COUNTS={}


def close(got,want,label,rtol=2e-8,atol=2e-9):
    error=abs(float(got)-float(want))
    rel=error/max(abs(float(want)),1e-30)
    MAX[label]=max(MAX.get(label,0.),rel)
    COUNTS[label]=COUNTS.get(label,0)+1
    assert error<=atol+rtol*abs(float(want)),(label,got,want,error)


def scalar_p2(row):
    c=next(c for c in at.IN["cores"] if c["name"]==row["core"])
    par=row["parameters"]
    with localcontext() as ctx:
        ctx.prec=45
        tf,tc=dd(row["tf_m"]),dd(row["tc_m"])
        r,pp,nu=dd(at.R),dd(at.P0),dd(at.IN["case"]["nu"])
        e,sigma=dd(par["E"]),dd(par["sigma"])
        area=dd(at.A0);rhof=D(1850)
        mf=2*area*tf*rhof;mc=area*tc*dd(c["rho"])
        w=dd(par["panel"])
        seams=2*area/w*(D(".12")*tf*rhof+D(".000024")*1250+tc*D(".0015")*1100)
        films=2*area*dd(par["film"])*D(".45359237")/D(".09290304")
        floor=D(".05")*(mf+mc)
        joint=max(floor,seams+films) if row["mass_rule"]=="explicit" else floor
        mass=mf+mc+joint+100+dd(at.IN["nonclimate_kg"])
        close(mass,row["masses_kg"]["carried"],"p2_mass")
        close(mass+dd(row["C_kg"]),at.L0,"p2_mass_closure")
        h=tf+tc
        s0=e*h/(r*(1-nu*nu).sqrt())
        sc=h*h*dd(c["Gc_Pa"])/(2*tf*tc)
        vc=s0/sc
        kc=1-vc/4 if vc<=2 else 1/vc
        gt=D(".2") if vc<2 else D(1)
        gf=D(".2")+D(".4")*min(vc,D(2))
        if "gamma_value" in par:
            gam=dd(par["gamma_value"]) if vc<2 else D(1)
        else:
            gam=gt*((gf/gt).ln()*dd(par["gamma_usage"])).exp()
        bx=D(".68")
        for _ in range(15):
            bx-= (bx**3+bx-1)/(3*bx**2+1)
        stresses=dict(
            global_=gam*kc*s0,face=sigma,crimp=sc,
            crush=dd(c["crush_Pa"])*r/(2*tf),
            wrinkle=bx*dd(par["wrinkle"])*(e*dd(c["Ec_Pa"])*tf/tc).sqrt(),
            dimple=e/(1-nu*nu)*(tf/dd(c["s_cell_m"]))**2)
        stresses["global"]=stresses.pop("global_")
        # Convert all six capacities from face-stress coordinates back to pressure.
        m={k:float(v*4*tf/(r*pp)) for k,v in stresses.items()}
        for k in p2.MODES:
            close(m[k],row["sfs_at_p0"][k],"p2_modes")
        return m


def scalar_p3(row):
    with localcontext() as ctx:
        ctx.prec=45
        s,ro,tw,tf=map(dd,[row["spacing_m"],row["outer_radius_m"],row["wall_m"],row["film_m"]])
        ri=ro-tw
        pi=dd(math.pi);r=dd(at.R);pp=dd(at.P0);e=D(410_000_000_000)
        area=pi*(ro*ro-ri*ri)
        iner=pi*(ro**4-ri**4)/4
        length=dd(2*at.R*math.asin(float(s)/(2*at.R)))
        nodes=8*pi*r*r/(D(3).sqrt()*s*s)+2
        members=3*nodes-6
        mtube=members*length*D(3100)*area
        rho_f=D(970) if row["film"]=="projection" else D(1420)
        sigma_f=D(1_500_000_000) if row["film"]=="projection" else D(115_500_000)
        mf=dd(at.A0)*tf*rho_f;mn=D(".02")*nodes
        loadcoef=r*s/(2*D(3).sqrt())
        if row["joints"]=="percent":
            mj=D(".05")*(mtube+mf+mn)
        else:
            q=dd(row["joints"][1])
            mj=2*members*D("2.950e-14")*(pp*q*loadcoef)**2/ro
        total=mtube+mf+mn+mj+100+dd(at.IN["nonclimate_kg"])
        close(total,row["masses_kg"]["carried"],"p3_mass")
        close(total+dd(row["C_kg"]),row["nominal_effective_lift_kg"],"p3_mass_closure")
        force=pp*loadcoef
        sigma=D(3_900_000_000)
        elastic=pi*pi*e*iner/(area*length*length)
        eta=length*ro*area/(1000*iner)
        phi=(sigma+(1+eta)*elastic)/2
        perry=phi-(phi*phi-sigma*elastic).sqrt()
        gamma=1-D(".901")*(1-(-(ro/tw).sqrt()/16).exp())
        sf=dict(yield_=sigma*area/force,euler=pi*pi*e*iner/(length*length*force),
                local=D(".6")*e*tw/ro*gamma*area/force,
                film=2*sigma_f*tf/(s*pp),perry=perry*area/force,
                global_=D(".2")*4*D("1.5").sqrt()*e*(iner*area).sqrt()/(s*r*r*pp))
        sf["yield"]=sf.pop("yield_");sf["global"]=sf.pop("global_")
        for k in p3.MODES:
            close(sf[k],row["sfs_at_p0"][k],"p3_modes")
        return {k:float(v) for k,v in sf.items()}


def atmosphere_checks():
    # Direct integration of dp/dz, independent of the closed-form exponent.
    roots=0
    for day in at.DAYS:
        t500,p500,e500=day["T500_K"],day["p500_Pa"],day["e500_Pa"]
        def ode(z,y):
            t=t500-.0065*(z-500)
            vap=e500*y[0]/p500
            return [-9.80665*(y[0]-.378*vap)/(287.053*t)]
        down=solve_ivp(ode,(500.,-2500.),[p500],rtol=2e-12,atol=1e-9,dense_output=True,max_step=25)
        up=solve_ivp(ode,(500.,3500.),[p500],rtol=2e-12,atol=1e-9,dense_output=True,max_step=25)
        def dens(z):
            p=float((down if z<500 else up).sol(z)[0])
            return p*(1-.378*e500/p500)/(287.053*(t500-.0065*(z-500)))
        for C in [0.,14.957376125557857,55.340908917961315,231.74081642618603,
                  407.30666610434764,441.77010544583845,592.5180219336717]:
            target=(at.L0-C)/at.V0
            root=brentq(lambda z:dens(z)-target,-2500.,3500.,xtol=1e-8)
            expected=at.row(at.L0-C,at.V0,day)
            close(root,expected["z_m"],"atmosphere_altitude_ODE",atol=2e-7)
            pp=float((down if root<500 else up).sol(root)[0])
            close(pp,expected["p_Pa"],"atmosphere_pressure_ODE",rtol=2e-10)
            close(dens(root)*at.V0,at.L0-C,"buoyancy",rtol=1e-11)
            # These lapse profiles have decreasing density and hence stable passive equilibrium.
            assert dens(root-.1)>target>dens(root+.1)
            roots+=1
    return roots


def main():
    t0=time.monotonic()
    for pin in at.IN["pins"]:
        raw=Path(pin["path"]).read_bytes()
        assert len(raw)==pin["bytes"]
        assert hashlib.sha256(raw).hexdigest()==pin["sha256"],pin["path"]
    for source_key,key in p2.SOURCE_MAP.items():
        close(P2["source_reproduction"]["sfs_at_p0"][key],
              at.IN["reference_021b"]["floating_point"]["at_needed_values"]["sfs"][source_key],
              "021b_source_mode_reproduction",rtol=2e-9)
    rows2=[P2["source_reproduction"]]+P2["reoptimised"]
    for search in P2["least_optimism_searches"]+P2["reconstructed_021_searches"]:
        rows2.extend(r["point"] for r in search["tested_subsets"] if "point" in r)
    rows3=[P3["source_reproduction"]]+P3["reoptimised"]+P3["sensitivities"]
    for row in rows2:
        scalar_p2(row)
        for day in row["day_rows"]:
            for mode,sf in day["sfs"].items():
                close(sf*day["p_Pa"],row["sfs_at_p0"][mode]*at.P0,"p2_day_capacity")
    for row in rows3:
        scalar_p3(row)
        for day in row["days"]:
            for mode,sf in day["sfs"].items():
                close(sf*day["p_Pa"],row["sfs_at_p0"][mode]*at.P0,"p3_day_capacity")
    roots=atmosphere_checks()
    dense=[]
    for search in P2["least_optimism_searches"]+P2["reconstructed_021_searches"]:
        q=max(1.,float(at.demand(search["C_kg"],search["envelope"])[0]))
        variant=search["variant"]
        rule="placeholder" if variant=="021_rev1" else "explicit"
        # All lower-cardinality alternatives at their full named bounds.
        for r in search["tested_subsets"]:
            if len(r["subset"])<search["cardinality"]:
                b=p2.best_catalogue(search["C_kg"],p2.search_params(r["subset"],1,variant),q,n=32769,rule=rule)
                assert b["score"]<1.-1e-4,(search["envelope"],search["altitude_floor_m"],r["subset"],b)
                assert b["score"]<=r["full_bound_score"]+2e-7
                dense.append(dict(envelope=search["envelope"],floor=search["altitude_floor_m"],
                                  variant=variant,subset=r["subset"],dense_score=b["score"]))
        win=search["winner"];u=win["min_max_log_usage"]
        b=p2.best_catalogue(search["C_kg"],p2.search_params(win["subset"],u,variant),q,n=131073,rule=rule)
        close(b["score"],win["point"]["least_SF"],"p2_dense_winner",rtol=3e-7)
        if search["altitude_floor_m"] is not None:
            assert win["point"]["minimum_float_m"]>=search["altitude_floor_m"]-1e-7
        assert win["point"]["least_SF"]>=1.-2e-8
    # Independent seed and a vector grid around each P3 maximum.
    frame_checks=[]
    for row in P3["reoptimised"]+P3["sensitivities"]:
        x,q=row["x"],row["nominal_required_SF"]
        kind=row["joints"]
        if isinstance(kind,list):kind=tuple(kind)
        v,details=p3.optimise(x,q,kind,row["film"],seed=7020)
        second=float(p3.score(v,x,q,kind,row["film"]))
        close(second,row["least_SF"],"p3_second_seed",rtol=1e-6)
        svals=np.linspace(.4,8.,153)
        tmin=8e-5 if row["film"]=="projection" else 25e-6
        tvals=np.geomspace(tmin,.0025,81)
        rvals=np.linspace(.01,.25,251)
        best=-1
        for s in svals:
            ss=np.full((len(tvals),len(rvals)),s)
            rr=np.broadcast_to(rvals,ss.shape)
            tt=np.broadcast_to(tvals[:,None],ss.shape)
            best=max(best,float(np.max(p3.score((ss,rr,tt),x,q,kind,row["film"]))))
        assert best<=row["least_SF"]+2e-7
        assert row["spacing_m"]<7.9 and row["outer_radius_m"]<.249
        frame_checks.append(dict(envelope=row["envelope"],floor=row["altitude_floor_m"],
                                 film=row["film"],second_seed_score=second,
                                 independent_grid_best=best,grid_points=153*81*251))
    out=dict(status="PASS",pins_verified=len(at.IN["pins"]),
             p2_geometries=len(rows2),p3_geometries=len(rows3),
             atmosphere_ODE_roots=roots,counts=COUNTS,max_relative_errors=MAX,
             p2_lower_cardinality_dense_checks=dense,p3_checks=frame_checks,
             elapsed_s=time.monotonic()-t0,
             limits="Numerical and algebraic validation only; no material, fabrication, nonlinear buckling, joint, leakage or weather qualification.")
    (ROOT/"VALIDATION.json").write_text(json.dumps(out,indent=2)+"\n")
    print("PASS",len(rows2),"P2",len(rows3),"P3",roots,"ODE roots",
          len(dense),"dense subset exclusions",round(out["elapsed_s"],2),"s")


if __name__=="__main__":
    main()
