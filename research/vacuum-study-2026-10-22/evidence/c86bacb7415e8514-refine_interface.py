#!/usr/bin/env python3
"""Repair the checker-only 1e-9 interface relaxation at every affected finite knot."""
from check_model import *
import csv

corrections=[]
for R in (10,12,15,20,30):
    target=B/f"CHECKED-COUPLED-R{R}.npz"
    data={k:v for k,v in np.load(target).items()}
    original=np.load(B/f"owner-data/COUPLED-R{R}.npz")
    bad=np.isfinite(data["mass_kg"])&(data["minimum_SF"]<1-1e-12)
    if (B/"REFINEMENT-TARGETS.json").exists():
        for target_row in read("REFINEMENT-TARGETS.json")["targets"]:
            if target_row["R_m"]==R:
                it=int(np.flatnonzero(data["T_K"]==target_row["T_K"])[0])
                ip=int(np.flatnonzero(data["p_Pa"]==target_row["p_Pa"])[0])
                bad[it,target_row["mask"],ip]=True
    if not np.any(bad):continue
    for it,mask,ip in np.argwhere(bad):
        key=(int(it),int(mask),int(ip))
        old=float(data["mass_kg"][key])
        point=optimize(R,float(data["p_Pa"][ip]),int(mask),air=float(data["T_K"][it]),points=1500)
        data["mass_kg"][key]=point["mass_kg"] if point else np.inf
        data["tf_m"][key]=point["tf_m"] if point else np.nan
        data["tc_m"][key]=point["tc_m"] if point else np.nan
        data["minimum_SF"][key]=point["minimum_SF"] if point else np.nan
        corrections.append(dict(R_m=R,T_K=float(data["T_K"][it]),mask=int(mask),p_Pa=float(data["p_Pa"][ip]),
            checker_before_kg=old,checker_strict_kg=point["mass_kg"] if point else None,
            owner_mass_kg=float(original["mass_kg"][key]),
            difference_kg=point["mass_kg"]-float(original["mass_kg"][key]) if point and np.isfinite(original["mass_kg"][key]) else None,
            strict_minimum_SF=point["minimum_SF"] if point else None))
    np.savez_compressed(target,**data)
    records=[];mismatches=[]
    for it in range(len(data["T_K"])):
        for m in range(16):
            for ip,p in enumerate(data["p_Pa"]):
                key=(it,m,ip);left=float(original["mass_kg"][key]);right=float(data["mass_kg"][key])
                finite_equal=math.isfinite(left)==math.isfinite(right)
                delta=right-left if math.isfinite(left) and math.isfinite(right) else None
                records.append([it,float(data["T_K"][it]),m,float(p),left,right,delta,finite_equal])
                if not finite_equal or (delta is not None and abs(delta)>.05):
                    mismatches.append(dict(kind="independent_optimum",R_m=R,T_K=float(data["T_K"][it]),mask=m,p_Pa=float(p),
                        owner_mass_kg=left,checker_mass_kg=right,difference_kg=delta,
                        owner_feasible=math.isfinite(left),checker_feasible=math.isfinite(right)))
    with (B/f"TABLE-COMPARISONS-R{R}.csv").open("w") as f:
        writer=csv.writer(f);writer.writerow(["temperature_index","T_K","mask","p_Pa","owner_mass_kg",
            "checker_mass_kg","difference_kg","finite_status_agrees"]);writer.writerows(records)
    result=read(f"TABLE-CHECK-R{R}.json")
    result.update(mismatches=mismatches,mismatch_count=len(mismatches),
        max_finite_mass_difference_kg=max(abs(x[6]) for x in records if x[6] is not None),
        strict_interface_rechecks=int(np.count_nonzero(bad)),
        interface_correction="Strict interface inequality; initial looser run retained under exploratory/loose-interface-tolerance.")
    save(f"TABLE-CHECK-R{R}.json",result)
    from check_grids import run
    run(R)
save("INTERFACE-TOLERANCE-CHECK.json",dict(corrected_knots=len(corrections),rows=corrections,
    disposition="Checker-only relaxation removed. Same-input strict comparisons replace exploratory differences."))
print("strict interface rows",len(corrections),flush=True)
