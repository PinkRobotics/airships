#!/usr/bin/env python3
"""Independent mass closure, six-mode P2 calculation and named-optimism search."""
import itertools
import json
import math
import time
from pathlib import Path
import numpy as np
from scipy.optimize import brentq, minimize_scalar
import atmosphere as at

ROOT = Path(__file__).resolve().parent
I = at.IN
L, A, R, P = at.L0, at.A0, at.R, at.P0
NU, RHOF, E = I["case"]["nu"], 1850., 290e9
B = I["nonclimate_kg"]
SYS, J = 100., .05
LBFT = .45359237/.09290304
BX = brentq(lambda x:x*x*x+x-1,0,1,xtol=1e-15)
CORES = I["cores"]
LIGHT = next(c for c in CORES if c["name"]=="Hexcel CR-III 5056 3/8-1.0")
NAMES = ("gamma","wrinkle","strength","panel","film")
MODES = ("global","face","crimp","crush","wrinkle","dimple")
SOURCE_MAP = dict(global_buckling="global",face_compression="face",
                  core_shear_crimping="crimp",core_crush="crush",
                  face_wrinkling="wrinkle",intracell_dimpling="dimple")


def params(subset=(), u=0., **overrides):
    d = dict(E=E, sigma=345e6*(379.2/345)**(u if "strength" in subset else 0),
             gamma_usage=u if "gamma" in subset else 0.,
             wrinkle=.33*(.82/.33)**(u if "wrinkle" in subset else 0),
             panel=.9144*(4/.9144)**(u if "panel" in subset else 0),
             film=.03*(.015/.03)**(u if "film" in subset else 0))
    d.update(overrides)
    return d


def join_coeff(core,f,par):
    j = I["joint_parameters"]
    k = (2*j["strip_width_m"]*(1-f)/par["panel"]
         + 2*j["core_splice_width_m"]*j["rho_splice_kg_m3"]*f/(par["panel"]*core["rho"]))
    const = (4*A*j["strip_width_m"]*j["seam_adhesive_m"]*j["rho_adhesive_kg_m3"]/par["panel"]
             + 2*A*par["film"]*LBFT)
    return k,const


def geometry(core,f,C,par,rule="explicit",S=None):
    f = np.asarray(f)
    k,c = join_coeff(core,f,par)
    if S is None:
        available = L-SYS-B-C
        floor = available/(1+J)
        S = np.where(k*floor+c > J*floor,(available-c)/(1+k),floor) if rule=="explicit" else floor+np.zeros_like(f)
    S=np.asarray(S)+np.zeros_like(f)
    tf=(1-f)*S/(2*A*RHOF)
    tc=f*S/(A*core["rho"])
    joint_actual=k*S+c
    joint=np.maximum(J*S,joint_actual) if rule=="explicit" else J*S
    return dict(S=S,tf=tf,tc=tc,joint=joint,joint_actual=joint_actual,
                joint_floor=J*S,excess=np.maximum(0.,joint-J*S),
                film_kg=2*A*par["film"]*LBFT,
                seam_kg=joint_actual-2*A*par["film"]*LBFT,
                carried=S+joint+SYS+B)


def modes(core,tf,tc,par):
    h=tf+tc
    sig0=par["E"]*h/(R*math.sqrt(1-NU**2))
    crimp=h*h*core["Gc_Pa"]/(2*tf*tc)
    vc=sig0/crimp
    kc=np.where(vc<=2,1-vc/4,1/vc)
    today=np.where(vc<2,.2,1.)
    full=.2+.4*np.minimum(vc,2.)
    if "gamma_value" in par:
        gamma=np.where(vc<2,par["gamma_value"],1.)
    else:
        gamma=today*(full/today)**par["gamma_usage"]
    stress=P*R/(4*tf)
    out=dict(global_=4*gamma*kc*sig0*tf/(R*P),
             face=par["sigma"]/stress,
             crimp=crimp/stress,
             crush=np.zeros_like(vc)+2*core["crush_Pa"]/P,
             wrinkle=BX*par["wrinkle"]*np.sqrt(par["E"]*core["Ec_Pa"]*tf/tc)/stress,
             dimple=par["E"]/(1-NU**2)*(tf/core["s_cell_m"])**2/stress)
    out["global"]=out.pop("global_")
    return out,dict(Vc=vc,Kc=kc,gamma=gamma,stress_Pa=stress)


def score(core,f,C,par,rule="explicit",q=1.):
    g=geometry(core,f,C,par,rule)
    m,_=modes(core,g["tf"],g["tc"],par)
    sf=np.minimum.reduce([m[k] for k in MODES])/q
    return np.where(g["S"]>0,sf,-np.inf)


def optimum(core,C,par,rule="explicit",q=1.,n=2049,refine=True):
    f=np.linspace(1e-7,1-1e-7,n)
    vals=score(core,f,C,par,rule,q)
    idx=np.argsort(vals)[-3:]
    candidates=[float(f[j]) for j in idx]
    if refine:
        for j in idx:
            a,b=f[max(0,j-1)],f[min(n-1,j+1)]
            res=minimize_scalar(lambda x:-float(score(core,x,C,par,rule,q)),
                                bounds=(a,b),method="bounded",
                                options=dict(xatol=2e-13))
            candidates.append(float(res.x))
        # Include both sides of the CR-1457 branch boundary explicitly.
        g=geometry(core,f,C,par,rule)
        _,meta=modes(core,g["tf"],g["tc"],par)
        crossing=np.where(np.diff(meta["Vc"]>=2))[0]
        for j in crossing:
            def vc(x):
                g=geometry(core,x,C,par,rule)
                return float(modes(core,g["tf"],g["tc"],par)[1]["Vc"])-2
            z=brentq(vc,f[j],f[j+1],xtol=1e-15)
            candidates.extend([z,np.nextafter(z,0.),np.nextafter(z,1.)])
    val=[float(score(core,x,C,par,rule,q)) for x in candidates]
    j=int(np.argmax(val))
    return dict(core=core["name"],fraction=candidates[j],score=val[j])


def best_catalogue(C,par,q=1.,n=2049,rule="explicit"):
    coarse=[optimum(core,C,par,rule,q=q,n=n,refine=False) for core in CORES]
    leaders=sorted(coarse,key=lambda x:x["score"],reverse=True)[:4]
    refined=[]
    for r in leaders:
        core=next(c for c in CORES if c["name"]==r["core"])
        refined.append(optimum(core,C,par,rule,q=q,n=n,refine=True))
    return max(refined,key=lambda x:x["score"])


def describe(best,C,par,envelope,rule="explicit"):
    core=next(c for c in CORES if c["name"]==best["core"])
    f=best["fraction"]
    g=geometry(core,f,C,par,rule)
    m,meta=modes(core,g["tf"],g["tc"],par)
    m={k:float(m[k]) for k in MODES}
    q,zmin=at.demand(C,envelope)
    demand=max(1.,float(q))
    result=dict(
        core=core["name"],core_tag=core["tag"],core_mass_fraction=f,
        C_kg=float(C),envelope=envelope,mass_rule=rule,
        parameters=par,tf_m=float(g["tf"]),tc_m=float(g["tc"]),
        masses_kg=dict(faces=float((1-f)*g["S"]),core=float(f*g["S"]),
                       structure=float(g["S"]),joint=float(g["joint"]),
                       joint_floor=float(g["joint_floor"]),joint_excess=float(g["excess"]),
                       joint_actual_screen=float(g["joint_actual"]),
                       films=float(g["film_kg"]),seams=float(g["seam_kg"]),
                       systems=SYS,nonclimate=B,carried=float(g["carried"])),
        metadata={k:float(v) for k,v in meta.items()},sfs_at_p0=m,
        peak_float_pressure_ratio=float(q),required_nominal_SF=demand,
        sfs_at_required_pressure={k:v/demand for k,v in m.items()},
        least_SF=float(min(m.values())/demand),minimum_float_m=float(zmin),
        reserve_kg=B+C+float(g["excess"]),
        reserve_fraction=(B+C+float(g["excess"]))/L,
        day_rows=[at.row(float(g["carried"]),at.V0,d,m) for d in at.selected(envelope)],
    )
    gt=.2 if float(meta["Vc"])<2 else 1.
    gf=.2+.4*min(float(meta["Vc"]),2.)
    needed=dict(
        gamma=max(gt,float(meta["gamma"])*demand/m["global"]),
        wrinkle=max(.33,par["wrinkle"]*demand/m["wrinkle"]),
        strength_Pa=max(345e6 if rule=="explicit" else 283e6,par["sigma"]*demand/m["face"]),
        panel_m=par["panel"],film_lb_ft2=par["film"])
    result["needed_values_at_this_geometry"]=needed
    result["needed_log_usage"]=dict(
        gamma=math.log(needed["gamma"]/gt)/math.log(gf/gt) if gf>gt else 0.,
        wrinkle=math.log(needed["wrinkle"]/.33)/math.log(.82/.33),
        strength=math.log(needed["strength_Pa"]/345e6)/math.log(379.2/345)
                 if rule=="explicit" else math.log(needed["strength_Pa"]/283e6)/math.log(379.2/283),
        panel=math.log(par["panel"]/.9144)/math.log(4/.9144),
        film=math.log(par["film"]/.03)/math.log(.015/.03))
    return result


def search_params(subset,u,variant):
    if variant=="021_rev1":
        return params(subset,u,sigma=283e6*(379.2/283)**(u if "strength" in subset else 0))
    return params(subset,u)


def least_optimisms(C,envelope,variant="021b"):
    q=max(1.,float(at.demand(C,envelope)[0]))
    rule="placeholder" if variant=="021_rev1" else "explicit"
    names=NAMES[:3] if variant=="021_rev1" else NAMES
    tested=[]
    feasible=[]
    for cardinality in range(len(names)+1):
        for subset in itertools.combinations(names,cardinality):
            best=best_catalogue(C,search_params(subset,1.,variant),q,rule=rule)
            row=dict(subset=list(subset),full_bound_score=best["score"],full_bound_best=best)
            tested.append(row)
            if best["score"] >= 1.-1e-9:
                feasible.append((subset,row))
        if feasible:
            break
    for subset,row in feasible:
        lo,hi=0.,1.
        for _ in range(28):
            mid=(lo+hi)/2
            best=best_catalogue(C,search_params(subset,mid,variant),q,n=2049,rule=rule)
            if best["score"]>=1.:
                hi=mid
            else:
                lo=mid
        # A tiny numerical construction allowance keeps rounded JSON safely >=1.
        u=min(1.,hi+2e-8)
        best=best_catalogue(C,search_params(subset,u,variant),q,n=8193,rule=rule)
        row["min_max_log_usage"]=u
        row["point"]=describe(best,C,search_params(subset,u,variant),envelope,rule)
    winner=min((r for _,r in feasible),key=lambda r:r["min_max_log_usage"]) if feasible else None
    return dict(C_kg=C,envelope=envelope,variant=variant,cardinality=cardinality if feasible else None,
                tested_subsets=tested,winner=winner)


def minimum_hardware(core,par,q,rule="explicit"):
    """Mass needed at a prescribed uniform pressure. An isolated cost comparison."""
    def at_fraction(f):
        f=np.asarray(f)
        lo=np.zeros_like(f)+1e-4
        hi=np.zeros_like(f)+2*L
        for _ in range(50):
            mid=(lo+hi)/2
            g=geometry(core,f,0,par,rule,S=mid)
            m,_=modes(core,g["tf"],g["tc"],par)
            sf=np.minimum.reduce([m[k] for k in MODES])
            good=sf>=q
            hi=np.where(good,mid,hi)
            lo=np.where(good,lo,mid)
        g=geometry(core,f,0,par,rule,S=hi)
        m,_=modes(core,g["tf"],g["tc"],par)
        good=np.minimum.reduce([m[k] for k in MODES])>=q*(1-1e-10)
        return np.where(good,hi+g["joint"],np.inf),hi
    fs=np.linspace(.00005,.99995,8193)
    costs,_=at_fraction(fs)
    j=int(np.argmin(costs))
    if not np.isfinite(costs[j]):
        return None
    res=minimize_scalar(lambda f:float(at_fraction(f)[0]),
                        bounds=(fs[max(j-1,0)],fs[min(j+1,len(fs)-1)]),
                        method="bounded",options=dict(xatol=1e-12))
    cost,S=at_fraction(res.x)
    g=geometry(core,res.x,0,par,rule,S=S)
    return dict(hardware_kg=float(cost),structural_kg=float(S),
                joint_kg=float(g["joint"]),fraction=float(res.x),
                tf_m=float(g["tf"]),tc_m=float(g["tc"]),required_SF=q)


def source_fixed():
    points=[]
    p=I["reference_021b"]["floating_point"]
    sf={SOURCE_MAP[k]:v for k,v in p["at_needed_values"]["sfs"].items()}
    points.append(("021b_held",L-I["inherited_climate_allowance_kg"],sf,p))
    points.append(("021b_gross_mass_diagnostic",L,sf,p))
    p=I["reference_021"]["main"]["floating_point"]
    sf={SOURCE_MAP[k]:v for k,v in p["at_needed_values"]["sfs"].items()}
    base=L-p["masses_kg"]["margin"]
    points.append(("021_rev1_original_unfilled_margin",base,sf,p))
    points.append(("021_rev1_plus_019_nonclimate",base+B,sf,p))
    points.append(("021_rev1_gross_mass_diagnostic",L,sf,p))
    out=[]
    for label,mass,sfs,p in points:
        full={SOURCE_MAP[k]:v for k,v in p["at_full_named_set"]["sfs"].items()}
        out.append(dict(label=label,carried_mass_kg=mass,nominal_headroom_kg=L-mass,
                        tf_m=p["tf_m"],tc_m=p["core_m"],
                        sfs_at_p0=sfs,full_named_sfs_at_p0=full,
                        days=[at.row(mass,at.V0,d,sfs) for d in at.DAYS],
                        full_named_days=[at.row(mass,at.V0,d,full) for d in at.DAYS]))
    return out


def main():
    started=time.monotonic()
    p21b=I["reference_021b"]["floating_point"]
    p21=I["reference_021"]["main"]["floating_point"]
    par21b=params(gamma_value=p21b["needed_values"]["gamma"],
                 wrinkle=p21b["needed_values"]["wrinkle"],
                 panel=p21b["panel_width_m"],film=p21b["bond_film_lb_ft2"])
    par21=params(gamma_value=p21["needed_values"]["gamma"],
                wrinkle=p21["needed_values"]["wrinkle_coefficient"],sigma=283e6)
    parfull=params(NAMES,1.)
    # Verify the inherited point before optimising any new one.
    check=describe(dict(core=LIGHT["name"],fraction=p21b["core_mass_fraction"]),
                   I["inherited_climate_allowance_kg"],par21b,"optimistic")
    assert abs(check["tf_m"]-p21b["tf_m"])<2e-12
    assert abs(check["tc_m"]-p21b["core_m"])<2e-10
    targets=[]
    for env in ["optimistic","all_019"]:
        for floor in [None,10.,100.,500.]:
            C=at.floor_C(floor,env)
            targets.append((env,floor,C))
    reoptimised=[]
    for env,floor,C in targets:
        q=max(1.,float(at.demand(C,env)[0]))
        for label,par,rule in [
            ("021b_fixed_named_values",par21b,"explicit"),
            ("021_rev1_fixed_named_values",par21,"placeholder"),
            ("021_rev1_full_named_values",params(NAMES[:3],1.,sigma=379.2e6,E=293.6e9),"placeholder"),
            ("021b_all_five_full",parfull,"explicit"),
        ]:
            best=optimum(LIGHT,C,par,rule,q,n=16385)
            d=describe(best,C,par,env,rule)
            d.update(label=label,altitude_floor_m=floor)
            if label=="021b_fixed_named_values":
                nominal=minimum_hardware(LIGHT,par,1.,rule)
                weather=minimum_hardware(LIGHT,par,q,rule)
                d["matched_property_sf_mass_cost"]=dict(
                    nominal=nominal,weather=weather,
                    extra_hardware_kg=weather["hardware_kg"]-nominal["hardware_kg"],
                    C_plus_extra_kg=C+weather["hardware_kg"]-nominal["hardware_kg"])
            reoptimised.append(d)
    searches=[]
    for env,floor,C in targets:
        d=least_optimisms(C,env)
        d["altitude_floor_m"]=floor
        if d["winner"]:
            p=d["winner"]["point"]
            core=next(c for c in CORES if c["name"]==p["core"])
            nom=minimum_hardware(core,p["parameters"],1.)
            high=minimum_hardware(core,p["parameters"],p["required_nominal_SF"])
            d["mass_equivalent_sf_allowance"]=dict(
                ISA_minimum=nom,weather_minimum=high,
                extra_hardware_kg=high["hardware_kg"]-nom["hardware_kg"],
                C_plus_extra_hardware_kg=C+high["hardware_kg"]-nom["hardware_kg"],
                definition="Matched properties and core, independently reoptimised geometry at p0 and required weather pressure. Not extra mass charged twice.")
        searches.append(d)
        print("search",env,floor,"C",round(C,4),"least set",
              d["winner"]["subset"] if d["winner"] else None,
              d["winner"]["min_max_log_usage"] if d["winner"] else None,flush=True)
    searches21=[]
    for env,floor,C in targets:
        d=least_optimisms(C,env,variant="021_rev1")
        d["altitude_floor_m"]=floor
        searches21.append(d)
        print("021 reconstructed",env,floor,
              d["winner"]["subset"] if d["winner"] else None,
              d["winner"]["min_max_log_usage"] if d["winner"] else None,flush=True)
    # Fixed-source factor feasibility frontier; this also exposes any nonmonotone split.
    frontier=[]
    for env in ["optimistic","all_019"]:
        for C in np.linspace(0.,650.,131):
            q=max(1.,float(at.demand(C,env)[0]))
            for label,par,rule in [("021b_fixed_named_values",par21b,"explicit"),
                                   ("021_rev1_fixed_named_values",par21,"placeholder")]:
                b=optimum(LIGHT,float(C),par,rule,q,n=2049)
                frontier.append(dict(envelope=env,C_kg=float(C),label=label,**b))
    out=dict(schema=1,card="MAINLINE-031 P2",status="ESTIMATE",tag="QUESTIONABLE",
             projection=True,certification=False,source_reproduction=check,
             source_fixed=source_fixed(),reoptimised=reoptimised,
             least_optimism_searches=searches,fixed_factor_frontier=frontier,
             reconstructed_021_searches=searches21,
             elapsed_s=time.monotonic()-started)
    (ROOT/"P2.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print("P2 complete",round(out["elapsed_s"],2),"s")


if __name__=="__main__":
    main()
