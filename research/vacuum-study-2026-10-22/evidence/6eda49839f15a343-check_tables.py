#!/usr/bin/env python3
"""Recompute every coupled pressure/temperature/subset optimization knot."""
import csv
import time
from datetime import datetime,timezone
from check_model import *

start=time.time()
for R in (10,12,15,20,30):
    destination=B/f"CHECKED-COUPLED-R{R}.npz"
    if destination.exists():
        print("resuming: already complete",R,flush=True)
        continue
    source=np.load(B/f"owner-data/COUPLED-R{R}.npz")
    temperatures=source["T_K"];pressures=source["p_Pa"]
    shape=source["mass_kg"].shape
    calculated=np.full(shape,np.inf)
    faces=np.full(shape,np.nan);cores=np.full(shape,np.nan)
    scores=np.full(shape,np.nan)
    mismatches=[];records=[];point_count=0
    for it,air in enumerate(temperatures):
        tt=thermal_table(float(R),float(air))
        for mask in range(16):
            for ip,pressure in enumerate(pressures):
                key=(it,mask,ip)
                oldmass=float(source["mass_kg"][key])
                if np.isfinite(oldmass):
                    oldface=float(source["tf_m"][key]);oldcore=float(source["tc_m"][key])
                    witness=evaluate(R,oldface,oldcore,float(pressure),mask,air=float(air))
                    point_count+=1
                    md=witness["mass_kg"]-oldmass
                    sd=witness["minimum_SF"]-float(source["minimum_SF"][key])
                    if abs(md)>.00001 or abs(sd)>1e-7:
                        mismatches.append(dict(kind="filed_geometry",R_m=R,T_K=air,mask=mask,p_Pa=pressure,
                            owner_mass_kg=oldmass,checker_mass_kg=witness["mass_kg"],
                            owner_SF=source["minimum_SF"][key],checker_SF=witness["minimum_SF"]))
                point=optimize(R,float(pressure),mask,air=float(air),points=800)
                newmass=np.inf if point is None else point["mass_kg"]
                calculated[key]=newmass
                if point:
                    faces[key]=point["tf_m"];cores[key]=point["tc_m"];scores[key]=point["minimum_SF"]
                diff=newmass-oldmass if np.isfinite(newmass) and np.isfinite(oldmass) else None
                finite_equal=np.isfinite(newmass)==np.isfinite(oldmass)
                records.append([it,float(air),mask,float(pressure),oldmass,newmass,diff,finite_equal])
                if not finite_equal or (diff is not None and abs(diff)>.05):
                    mismatches.append(dict(kind="independent_optimum",R_m=R,T_K=air,mask=mask,p_Pa=pressure,
                        owner_mass_kg=oldmass,checker_mass_kg=newmass,difference_kg=diff,
                        owner_feasible=bool(np.isfinite(oldmass)),checker_feasible=point is not None,
                        checker_geometry=point))
        print("completed coupled",R,it+1,len(temperatures),"T",air,
              "elapsed",round(time.time()-start,1),"mismatches",len(mismatches),flush=True)
        save(f"TABLE-PROGRESS-R{R}.json",dict(temperature_index_complete=it,at=datetime.now(timezone.utc).isoformat(),
             mismatches=mismatches,elapsed_seconds=time.time()-start))
    np.savez_compressed(destination,T_K=temperatures,p_Pa=pressures,mass_kg=calculated,
                        tf_m=faces,tc_m=cores,minimum_SF=scores)
    with (B/f"TABLE-COMPARISONS-R{R}.csv").open("w") as f:
        writer=csv.writer(f);writer.writerow(["temperature_index","T_K","mask","p_Pa","owner_mass_kg",
                          "checker_mass_kg","difference_kg","finite_status_agrees"]);writer.writerows(records)
    finite_diffs=[abs(r[6]) for r in records if r[6] is not None]
    save(f"TABLE-CHECK-R{R}.json",dict(R_m=R,knots=len(records),fixed_geometry_checks=point_count,
         max_finite_mass_difference_kg=max(finite_diffs,default=0),mismatch_count=len(mismatches),
         mismatches=mismatches,elapsed_seconds=time.time()-start,
         thresholds=dict(fixed_mass_kg=1e-5,fixed_SF=1e-7,optimized_mass_kg=.05),
         owner_code_read=False,owner_code_run=False))
print("all coupled knots complete",time.time()-start,flush=True)
