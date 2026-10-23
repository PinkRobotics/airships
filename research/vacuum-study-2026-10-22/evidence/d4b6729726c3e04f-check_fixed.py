#!/usr/bin/env python3
"""Recompute fixed hulls, their complete grids and continuous mass boundaries."""
from check_model import *
import time

def scalar_core_thermal(R,core,air):
    knots=np.geomspace(.001*R/10,1.5*R/10,241)
    index=np.clip(np.searchsorted(knots,core)-1,0,239)
    pair=knots[index:index+2]
    data=thermal(R,pair,air)
    fraction=(np.log(core)-np.log(pair[0]))/(np.log(pair[1])-np.log(pair[0]))
    return {k:float(v[0]*(1-fraction)+v[1]*fraction)
            for k,v in data.items() if k in
            ("gradient_K","curvature_temperature_K","max_outer_K","min_outer_K")}

def vector_root(function,shape,lo=-60.,hi=100.):
    lower=np.full(shape,lo);upper=np.full(shape,hi)
    initial_low=function(lower);initial_high=function(upper)
    for _ in range(48):
        midpoint=(lower+upper)/2
        positive=function(midpoint)>=0
        lower=np.where(positive,midpoint,lower)
        upper=np.where(positive,upper,midpoint)
    return np.where((initial_low>=0)&(initial_high<=0),(lower+upper)/2,np.nan)

def run():
    start=time.time()
    old=read("owner-data/FIXED-HULLS.json")
    source=np.load(B/"owner-data/FIXED-HULL-WEATHER-GRID.npz")
    surfaces=np.load(B/"owner-data/FIXED-HULL-ZERO-SURFACES.npz")
    z=source["z_m"];offset=source["T_offset_K"]
    anomaly=source["sea_pressure_anomaly_hPa"];rh=source["RH_fraction"]
    T,p,e,rho=atmosphere(z[:,None,None,None],offset[None,:,None,None],
                       anomaly[None,None,:,None],rh[None,None,None,:])
    pressure=load_pressure(p)
    maxpressure=float(np.max(pressure))
    required=T_CURE-W_MIN/(GUARD*abs(ALPHA_AL-ALPHA_BE)*np.sqrt(2*K_BIAX*GC))
    rows=[];comparisons=[];builds=[];payloads=[];scores=[];zerorows=[]
    for ir,R in enumerate(source["radii_m"]):
        R=int(R);V=4/3*np.pi*R**3
        cut=brentq(lambda air:float(thermal(R,[.001*R/10],air)["min_outer_K"][0])-required,270,285,xtol=1e-11)
        design_air=cut+.05
        design=optimize(R,maxpressure,11,air=design_air,points=1500)
        builds.append(design)
        filed=old["reference_builds"][ir]
        comparisons.append(dict(row=f"fixed/R{R}",field="mass_kg",owner=filed["mass_kg"],
            checker=design["mass_kg"],difference=design["mass_kg"]-filed["mass_kg"]))
        # Isolate arithmetic at the same filed geometry before considering optimization differences.
        unique,index=np.unique(np.round(T[:,:,0,0],9),return_inverse=True)
        values={k:[] for k in ("gradient_K","curvature_temperature_K","max_outer_K","min_outer_K")}
        for air in unique:
            tt=scalar_core_thermal(R,filed["tc_m"],float(air))
            for k in values:values[k].append(tt[k])
        fields={k:np.asarray(v)[index].reshape(len(z),len(offset),1,1) for k,v in values.items()}
        allmodes=modes(R,filed["tf_m"],filed["tc_m"],pressure,11,temperature=fields)
        sf=np.minimum.reduce([np.broadcast_to(v,pressure.shape) for v in allmodes.values()])
        fullmass=float(sum(bill(R,filed["tf_m"],filed["tc_m"],11).values()))
        pay=rho*V-fullmass
        payloads.append(pay);scores.append(sf)
        oldsf=source["minimum_SF"][ir];oldpay=source["payload_kg"][ir]
        dp=pay-oldpay;ds=sf-oldsf
        comparisons.extend([
            dict(row=f"fixed-grid/R{R}",field="payload_kg",max_abs_difference=float(np.max(abs(dp))),
                 differing_over_1e_6=int(np.count_nonzero(abs(dp)>1e-6)),points=pay.size),
            dict(row=f"fixed-grid/R{R}",field="minimum_SF",max_abs_difference=float(np.max(abs(ds))),
                 differing_over_1e_6=int(np.count_nonzero(abs(ds)>1e-6)),points=pay.size)])
        zz=z[:,None,None];aa=anomaly[None,:,None];hh=rh[None,None,:]
        roots=vector_root(lambda off:atmosphere(zz,off,aa,hh)[3]*V-fullmass,(len(z),len(anomaly),len(rh)))
        zerorows.append(roots)
        prev=surfaces["upper_mass_zero_offset_K"][ir]
        comparisons.append(dict(row=f"fixed-zeros/R{R}",field="upper_mass_zero_offset_K",
            max_abs_difference_K=float(np.nanmax(abs(roots-prev))),
            finite_status_disagreement=int(np.count_nonzero(np.isfinite(roots)!=np.isfinite(prev))),points=roots.size))
        for iz,height in enumerate(z):
            rows.append(dict(R_m=R,z_m=float(height),cold_cutoff_offset_K=cut-(288.15-LAPSE*height),
                conservative_cold_offset_K=design_air-(288.15-LAPSE*height),
                worst_P_RH_upper_offset_K=float(np.nanmin(roots[iz])),
                best_P_RH_upper_offset_K=float(np.nanmax(roots[iz])),
                entire_rectangle_has_conservative_band=bool(np.nanmin(roots[iz])>=design_air-(288.15-LAPSE*height))))
        for row in old["boundary_slices"]:
            if row["R_m"]!=R:continue
            iz=int(np.flatnonzero(z==row["z_m"])[0]);ip=int(np.flatnonzero(anomaly==row["sea_pressure_anomaly_hPa"])[0])
            for field,j in (("RH0_upper_offset_K",0),("RH100_upper_offset_K",-1)):
                value=float(roots[iz,ip,j])
                comparisons.append(dict(row=f"fixed-slice/R{R}/z{row['z_m']}/p{row['sea_pressure_anomaly_hPa']}",
                    field=field,owner=row[field],checker=value,difference=value-row[field]))
        print("fixed radius",R,"root",cut,"mass",design["mass_kg"],"SF maxdiff",np.max(abs(ds)),flush=True)
    np.savez_compressed(B/"CHECKED-FIXED-GRID.npz",payload_kg=np.stack(payloads),minimum_SF=np.stack(scores),
                        upper_mass_zero_offset_K=np.stack(zerorows))
    save("FIXED-CHECK.json",dict(required_night_skin_minimum_K=required,
        grid_maximum_pressure_Pa=maxpressure,
        design_pressure_difference_Pa=maxpressure-old["design_pressure_Pa"],
        builds=builds,boundaries=rows,comparisons=comparisons,seconds=time.time()-start,
        cold_domain="Thermal table minimum core .001 R/10; no architecture-wide impossibility claim."))
    print("fixed complete",time.time()-start,flush=True)

if __name__=="__main__":run()
