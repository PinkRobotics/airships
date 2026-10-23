#!/usr/bin/env python3
"""Initial independent thermal, fixed-point mass and mode comparison."""
import time
import numpy as np
from check_model import *

started=time.time();rows=[]
oldthermal=read("owner-data/THERMAL50.json")
reference=read("owner-data/MASS-CURVES.json")["reference"]
fixed=read("owner-data/RESULTS.json")["fixed_builds"]
for old in reference:
    R=old["R_m"]
    table=thermal_table(float(R))
    differences={}
    for key in ("gradient_K","curvature_temperature_K","max_outer_K","min_outer_K","swing_K"):
        differences[key]=float(np.max(abs(np.asarray(table[key])-oldthermal[str(R)][key])))
    point=evaluate(R,old["tf_m"],old["tc_m"],old["pressure_Pa"],old["mask"])
    opt=optimize(R,old["pressure_Pa"],old["mask"])
    row=dict(R_m=R,thermal_max_differences=differences,point=point,
        mass_difference_kg=point["mass_kg"]-old["mass_kg"],
        mode_differences={k:float(v)-old["modes"][k] for k,v in point["modes"].items()},
        independent_optimum=opt,optimized_mass_difference_kg=opt["mass_kg"]-old["mass_kg"])
    oldfixed=next(x for x in fixed if x["R_m"]==R)
    fp=evaluate(R,oldfixed["tf_m"],oldfixed["tc_m"],oldfixed["pressure_Pa"],
                oldfixed["mask"],air=oldfixed["design_temperature_K"])
    row["fixed_point"]=fp;row["fixed_mass_difference_kg"]=fp["mass_kg"]-oldfixed["mass_kg"]
    row["fixed_mode_differences"]={k:float(v)-oldfixed["modes"][k] for k,v in fp["modes"].items()}
    rows.append(row)
    print(R,"thermal",max(differences.values()),"mass",row["mass_difference_kg"],
          "optimized",row["optimized_mass_difference_kg"],"minSF",point["minimum_SF"],flush=True)
    save("INITIAL-CHECK.json",dict(rows=rows,elapsed_seconds=time.time()-started))
print("completed",time.time()-started,flush=True)
