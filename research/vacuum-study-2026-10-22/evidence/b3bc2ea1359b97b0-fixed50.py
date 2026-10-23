#!/usr/bin/env python3
"""One build per radius, sized for the full rectangular weather pressure range."""
import time
from analyze50 import Curves,writecsv,safe
from model50 import *

if __name__=="__main__":
    start=time.time();radii=[10,12,15,20,30]
    z=np.arange(100,1501,50);t=np.arange(-20,21);p=np.arange(-30,31,2);rh=np.linspace(0,1,11)
    w=atmosphere(z[:,None,None,None],t[None,:,None,None],p[None,None,:,None],rh[None,None,None,:])
    designp=float(w["pressure_load_Pa"].max())
    refs=[];summaries=[];payloads=[];sfs=[];boundaries=[];dewrows=[];checks=[]
    dew=json.loads((B/"DEW-FROST.json").read_text())
    for r in radii:
        c=Curves(r);designT=c.minimum_tabulated_safe_t(11)
        table=inherited_thermal(r,np.geomspace(.001*r/10,1.5*r/10,241),
                  ta=designT,day_sky=designT-9.9,night_sky=designT-24.9)
        a=Account(r,table);o=a.optimum([designp],11,grid=1600);ref=scalar_record(a,o)
        ref["design_temperature_K"]=designT;refs.append(ref)
        ts=np.unique(np.r_[np.arange(258,328,1),designT])
        thermal={k:[] for k in ["gradient_K","curvature_temperature_K","max_outer_K","min_outer_K"]}
        for ta in ts:
            th=inherited_thermal(r,[ref["tc_m"]],ta=ta,day_sky=ta-9.9,night_sky=ta-24.9)
            for k in thermal:thermal[k].append(float(th[k][0]))
        def fixed_evaluate(weather):
            th={k:np.interp(weather["T_K"],ts,v) for k,v in thermal.items()}
            return a.evaluate(ref["tf_m"],ref["tc_m"],weather["pressure_load_Pa"],11,thermal=th)
        check=fixed_evaluate(w)
        payload=w["rho_kg_m3"]*a.volume-ref["mass_kg"]
        sf=check["minimum_SF"];payloads.append(payload);sfs.append(sf)
        zz,pp,hh=np.meshgrid(z,p,rh,indexing="ij")
        low=np.full(zz.shape,-60.);high=np.full(zz.shape,60.)
        for _ in range(42):
            mid=(low+high)/2;ww=atmosphere(zz,mid,pp,hh)
            yes=ww["rho_kg_m3"]*a.volume>=ref["mass_kg"]
            low=np.where(yes,mid,low);high=np.where(yes,high,mid)
        root=(low+high)/2;boundaries.append(root)
        for zi,alt in enumerate(z):
            for pi,anom in enumerate(p):
                # Root describes mass only. The conservative design cold limit
                # and a full-grid SF test are also supplied, never silently erased.
                if anom in (-30,0,30) and alt in (100,500,1000,1500):
                    summaries.append({"R_m":r,"z_m":int(alt),"sea_pressure_anomaly_hPa":int(anom),
                        "conservative_cold_offset_K":designT-(288.15-LAPSE*alt),
                        "RH0_upper_offset_K":float(root[zi,pi,0]),
                        "RH100_upper_offset_K":float(root[zi,pi,-1]),
                        "any_humidity_nonempty_conservative_window":bool(root[zi,pi,-1]>=designT-(288.15-LAPSE*alt))})
        warm=(w["T_K"]>=designT)
        checks.append({"R_m":r,"minimum_SF_above_design_cold_limit":float(sf[warm].min()),
            "max_full_bill_variation_kg":float(np.max(abs(check["mass_kg"]-ref["mass_kg"]))),
            "pmax_within_sizing":bool(np.max(w["pressure_load_Pa"])<=designp+1e-6),
            "positive_grid_fraction_with_SF_not_probability":float(np.mean((payload>=0)&(sf>=1-1e-8)))})
        for row in dew["rows"]:
            if row["R_m"]!=r:continue
            rho=(P0-.378*row["RH_water_fraction"]*es_water(row["Ta_K"]))/(RD*row["Ta_K"])
            threshold=.1+(rho*a.volume-ref["mass_kg"])/a.area
            dewrows.append({"R_m":r,"case":row["case"],
                "fixed_full_range_hull_water_threshold_at_500m_kg_m2":float(threshold),
                "using_original_reference_hull_deposition_kg_m2":row["mean_deposit_kg_m2"],
                "deposition_transfer_note":"Only a comparison; extra thermal mass was not re-solved for this hull.",
                "dry_payload_kg":float(threshold*a.area)})
        print("fixed",r,time.time()-start,flush=True)
    np.savez_compressed(B/"FIXED-HULL-WEATHER-GRID.npz",radii_m=radii,z_m=z,T_offset_K=t,
        sea_pressure_anomaly_hPa=p,RH_fraction=rh,payload_kg=payloads,minimum_SF=sfs)
    np.savez_compressed(B/"FIXED-HULL-ZERO-SURFACES.npz",radii_m=radii,z_m=z,
        sea_pressure_anomaly_hPa=p,RH_fraction=rh,upper_mass_zero_offset_K=boundaries)
    writecsv("FIXED-HULL-BOUNDARIES.csv",summaries)
    save("FIXED-HULLS.json",safe({"design_pressure_Pa":designp,"reference_builds":refs,
        "checks":checks,"boundary_slices":summaries,"dew_comparisons":dewrows,"seconds":time.time()-start,
        "scope":"One immutable geometry per radius, sized at simultaneous maximum pressure and cold design temperature; projected temperature-dependent SF checked across the grid.",
        "warning":"A zero-payload boundary alone is not a feasible window when it lies below the cold screen."}))
    print("DONE",time.time()-start,flush=True)
