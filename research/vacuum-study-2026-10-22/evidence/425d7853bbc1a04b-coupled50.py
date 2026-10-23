#!/usr/bin/env python3
"""Weather-coupled extension of the frozen 048-account comparison.

Sky temperatures track ambient with inherited 9.9/24.9 K depressions, solar=970,
wind=2 m/s. This is one declared dry-surface scenario, not an all-weather thermal
qualification. The full 16 endpoint subsets are retained.
"""
import time
from concurrent.futures import ProcessPoolExecutor
from model50 import *

def radius_run(r):
    start=time.time();pk=np.linspace(PMIN,106500,17)
    grid=np.geomspace(.001*r/10,1.5*r/10,241)
    required_cold=CURE-COREMIN/(1.002*(ALPHAC-ALPHAF)*math.sqrt(2*KBIAX*GC))
    # The warmest possible night temperature across the core grid is an optimistic
    # lower bound for interface feasibility; actual optimized geometries are checked.
    lo=260.;hi=290.
    for _ in range(26):
        ta=(lo+hi)/2
        th=inherited_thermal(r,grid,ta=ta,day_sky=ta-9.9,night_sky=ta-24.9)
        if max(th["min_outer_K"])>=required_cold:hi=ta
        else:lo=ta
    threshold=(lo+hi)/2
    ts=np.unique(np.r_[np.arange(258,326.01,2),TREF,
                      threshold+np.array([0,.05,.1,.2,.5,1.])])
    masses=[];tfs=[];tcs=[];sfmin=[];counts=[]
    for ta in ts:
        th=inherited_thermal(r,grid,ta=ta,day_sky=ta-9.9,night_sky=ta-24.9)
        a=Account(r,th)
        if max(th["min_outer_K"])<required_cold:
            masses.append(np.full((16,len(pk)),np.inf));tfs.append(np.full((16,len(pk)),np.nan))
            tcs.append(np.full((16,len(pk)),np.nan));sfmin.append(np.full((16,len(pk)),np.nan))
            counts.append(0)
        else:
            rows=[a.optimum(pk,m) for m in range(16)]
            masses.append(np.stack([x["mass_kg"] for x in rows]))
            tfs.append(np.stack([x["tf_m"] for x in rows]))
            tcs.append(np.stack([x["tc_m"] for x in rows]))
            sfmin.append(np.stack([x["minimum_SF"] for x in rows]))
            counts.append(sum(np.isfinite(x["mass_kg"]).sum() for x in rows))
        print("coupled",r,round(ta,4),round(time.time()-start,1),flush=True)
    np.savez_compressed(B/f"COUPLED-R{r}.npz",T_K=ts,p_Pa=pk,
        mass_kg=masses,tf_m=tfs,tc_m=tcs,minimum_SF=sfmin)
    return {"R_m":r,"thermal_no_core_feasible_below_K":threshold,
            "required_night_skin_minimum_K":required_cold,
            "temperatures_K":ts.tolist(),"finite_geometry_count_by_T":counts,
            "seconds":time.time()-start}

if __name__=="__main__":
    start=time.time()
    with ProcessPoolExecutor(max_workers=4) as pool:
        records=list(pool.map(radius_run,[10,12,15,20,30]))
    save("COUPLED-METADATA.json",{"radii":records,"seconds":time.time()-start,
         "tag":"PROJECTION","model":"Dry 048 thermal equations with ambient and sky shifted together.",
         "sky_day_depression_K":9.9,"sky_night_depression_K":24.9,
         "solar_W_m2":970,"wind_m_s":2,
         "limitation":"Independent cloud, solar, wet emissivity and wind dependence is outside this single thermal scenario."})
    print("DONE",time.time()-start,flush=True)
