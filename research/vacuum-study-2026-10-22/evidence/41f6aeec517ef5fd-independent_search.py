"""Independent one-dimensional minimum-mass search conditional on thermal inputs.

Vector bisection finds the minimum feasible face thickness at each core
thickness. A dense log-core grid brackets local optima, which are refined.
No owner implementation is read or imported.
"""
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from scipy.optimize import brentq, minimize_scalar

import account_model as m


def face_at_core(radius, tc, mask, usage, settings):
    tc = np.atleast_1d(np.asarray(tc, dtype=float))
    # Precompute everything independent of face thickness.
    p = m.properties(mask, usage)
    e, nu = p["E"], settings.get("nu", .0768)
    et = settings.get("thermal_modulus_Pa") or e
    _, qp = m.CLIMATE[settings["weather"]]
    factor = max(settings.get("pressure_factor_floor", 1.01), qp)
    pressure = m.P0*factor+max(m.wind_pressures().values())
    therm = m.thermal_values(radius, tc, settings)
    guard = 1.002
    gradient = guard*et*m.AB*therm["gradient_K"]/(2*(1-nu))
    curvature = guard*et*m.AB*therm["curvature_temperature_K"]/(2*radius*(1-nu**2))
    cure = settings.get("cure_temperature_K", 366.4833333333333)
    cure_delta = np.maximum(abs(cure-therm["min_outer_K"]),abs(cure-therm["max_outer_K"]))
    mismatch = guard*(m.AA-m.AB)*cure_delta
    edge = mismatch*math.sqrt(2*m.KB*m.GC)
    wall = 1.2*67e9*mismatch
    balanced = guard*m.KB*(m.AA-m.AB)*np.maximum(cure-therm["min_outer_K"],0)*tc/2
    ratio = settings.get("scarf_ratio",m.BASE["joining"]["scarf_ratio"])

    def smallest(tf):
        axial = pressure*radius/(4*tf)
        sigma0 = e*(tf+tc)/(radius*math.sqrt(1-nu**2))
        crimp = m.GC*(tf+tc)**2/(2*tf*tc)
        vc = sigma0/crimp
        kc = np.where(vc<=2,1-vc/4,1/vc)
        g0 = np.where(vc<2,.2,1.)
        gamma = g0*((.2+.4*np.minimum(vc,2))/g0)**p["gamma_usage"]
        st = axial+gradient+curvature*(tf+tc)
        demand = st+balanced/tf
        scarf = demand*ratio/(1+ratio**2)
        if settings.get("edge_scarf_interaction"):
            scarf += edge
        vals = [
            gamma*kc*sigma0/(axial+balanced/tf if settings.get("cure_in_global") else axial),
            p["Fcy"]/demand,
            crimp/(st+balanced/tf if settings.get("cure_in_global") else st),
            m.BETA*p["Q"]*np.sqrt(e*m.EC*tf/tc)/demand,
            e*(tf/m.CORE["s_cell_m"])**2/((1-nu**2)*demand),
            10e6/scarf,
        ]
        return np.minimum.reduce(vals)

    low = np.full_like(tc,1e-8)
    high = np.full_like(tc,min(.0195,.008*radius/10))
    feasible = (smallest(high)>=1)&(edge<=m.W_MIN)&(wall<=m.BASE["bond_fix_037b"]["foil_yield_proxy_Pa"])
    feasible &= 2*m.CORE["crush_Pa"]>=pressure
    for _ in range(43):
        mid = (low+high)/2
        ok = smallest(mid)>=1
        high = np.where(ok,mid,high)
        low = np.where(ok,low,mid)
    return np.where(feasible,high,np.nan)


def payload_many(radius, tf, tc, mask, usage, settings):
    area = 4*math.pi*radius**2
    props = m.properties(mask,usage)
    fm,cm = 2*area*tf*1850,area*tc*m.RC
    ratio=settings.get("scarf_ratio",m.BASE["joining"]["scarf_ratio"])
    ls=area*(1/(.6096-ratio*tf)+1/(1.8288-ratio*tf))
    film=2*area*props["film"]
    scarf=ls*2*tf*math.sqrt(1+ratio**2)*.07
    splice=ls*.0005*tc*500
    seal=ls*.002
    joining=film+scarf+splice+seal
    charged=np.maximum(joining,.05*(fm+cm)) if settings.get("floor") else joining
    primer=area*settings.get("structural_primer_kg_m2",.01)
    water0=(settings.get("adhesive_water_fraction",.002)*film+.001*cm+
            .01*primer+area*settings.get("finish_water_kg_m2",0)+.01*(scarf+splice+seal))
    nominal=.1*(.0485*film+.001*cm+.01*(scarf+splice+seal))
    water=water0*settings.get("moisture_scale",1.)
    sorbent=(1.1*(water0+nominal)+.1*(radius/10)**3)/settings.get("desiccant_capacity_kg_kg",.1)+2 if settings.get("desiccant") else 0
    fixed=(area*(settings["coating"]+settings.get("external_water_kg_m2",.1))+
           m.pad(radius,settings)["mass_kg"]+.01*m.LIFT0*(radius/10)**3+
           settings.get("systems",100)+settings.get("extra_service",0)+5*(radius/10)**2+
           m.CLIMATE[settings["weather"]][0]*(radius/10)**3+primer)
    return m.LIFT0*(radius/10)**3-(fm+cm+charged+water+sorbent+fixed)


def optimize(radius,mask,usage,settings,n=901):
    grid=np.linspace(math.log(.0012*radius/10),math.log(1.4*radius/10),n)
    tc=np.exp(grid)
    tf=face_at_core(radius,tc,mask,usage,settings)
    pay=payload_many(radius,tf,tc,mask,usage,settings)
    pay=np.where(np.isfinite(pay),pay,-1e30)
    candidates=[]
    if not np.any(pay>-1e29):
        return None
    peak=np.flatnonzero((pay>=np.r_[-np.inf,pay[:-1]])&(pay>=np.r_[pay[1:],-np.inf])&(pay>-1e29))

    def objective(logc):
        c=math.exp(logc)
        f=face_at_core(radius,c,mask,usage,settings)
        if not np.isfinite(f[0]):
            return 1e25
        return -float(payload_many(radius,f,np.array([c]),mask,usage,settings)[0])

    for i in peak:
        candidates.append((pay[i],grid[i]))
        lo,hi=grid[max(0,i-1)],grid[min(n-1,i+1)]
        if hi>lo:
            opt=minimize_scalar(objective,bounds=(lo,hi),method="bounded",options={"xatol":2e-12})
            if opt.fun<1e24:
                candidates.append((-opt.fun,opt.x))
    value, logc=max(candidates)
    core=math.exp(logc)
    face=float(face_at_core(radius,core,mask,usage,settings)[0])
    point=m.evaluate(radius,face,core,mask,usage,settings)
    # This reduced search always verifies the full vacuum/mass calculation.
    assert abs(point["signed_payload_kg"]-value)<1e-7,(point["signed_payload_kg"],value)
    assert point["least_shell_and_thermal_SF"]>=1-2e-9
    assert point["vacuum"]["pressure_SF"]>1
    return dict(payload_kg=point["signed_payload_kg"],tf_m=face,tc_m=core,
                least_SF=point["least_shell_and_thermal_SF"],pressure_SF=point["vacuum"]["pressure_SF"],
                grid_points=n)


def main():
    import sys,time
    profile=sys.argv[1]
    source=json.loads((m.ROOT/"intake/owner/RESULTS.json").read_text())
    rows=[x for x in source["rows"] if x["profile"]==profile]
    output=[]
    t0=time.monotonic()
    for index,row in enumerate(rows):
        r=row["R_m"]
        s=row["two_factor_endpoint"]["settings"]
        endpoint_checks=[]
        for trial in row["least"]["endpoint_trials"]:
            mask=trial["mask"]
            got=optimize(r,mask,1.,s)
            old=trial["payload_kg"]
            delta=None if got is None or old is None else got["payload_kg"]-old
            endpoint_checks.append(dict(mask=mask,owner_payload_kg=old,independent=got,delta_kg=delta))
        tfpoint=optimize(r,11,1.,s)
        selected=row["least"]["least"]
        least=None
        if selected is not None:
            mask=selected["mask"]
            # Root bracket is independent; recorded owner's usage is comparison only.
            f0=optimize(r,mask,0.,s,n=501)
            f1=optimize(r,mask,1.,s,n=501)
            if f0 is not None and f0["payload_kg"]>=0:
                u=0.
            else:
                def fun(u):
                    p=optimize(r,mask,u,s,n=501)
                    return p["payload_kg"] if p is not None else -1e12
                u=brentq(fun,0,1,xtol=2e-10)
            optimal=optimize(r,mask,u,s)
            least=dict(mask=mask,owner_usage=selected["usage"],usage=u,
                       usage_delta=u-selected["usage"],optimal=optimal)
        nfloat=[x["mask"].bit_count() for x in endpoint_checks
                if x["independent"] is not None and x["independent"]["payload_kg"]>=-1e-4]
        cardinality=min(nfloat) if nfloat else None
        output.append(dict(id=row["id"],endpoint_checks=endpoint_checks,
                           two_factor= tfpoint, two_factor_delta_kg=None if tfpoint is None else tfpoint["payload_kg"]-row["two_factor_endpoint"]["signed_payload_kg"],
                           least=least,independent_minimum_endpoint_axis_count=cardinality,
                           owner_minimum_axis_count=row["least"]["minimum_axis_count"]))
        if index%12==0:
            print(json.dumps(dict(profile=profile,done=index+1,total=len(rows),elapsed_seconds=time.monotonic()-t0)),flush=True)
    (m.ROOT/("SEARCH-"+profile+".json")).write_text(json.dumps(dict(
        profile=profile,tag="QUESTIONABLE / PROJECTION",thermal_scope="Conditional on pinned thermal tables",
        rows=output,elapsed_seconds=time.monotonic()-t0),indent=2,allow_nan=False)+"\n")
    print(json.dumps(dict(profile=profile,done=len(rows),elapsed_seconds=time.monotonic()-t0)),flush=True)


if __name__=="__main__":
    main()
