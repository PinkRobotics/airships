#!/usr/bin/env python3
"""Cross-check all slices, least-set intervals, fixed reference examples and summaries."""
from check_model import *
from check_grids import coupled_mass
import csv

def run():
    comparisons=[];transitions=[];slices=[]
    base=np.load(B/"owner-data/COUPLED-WEATHER-GRID.npz")
    z=base["z_m"];a=base["sea_pressure_anomaly_hPa"];rh=base["RH_fraction"]
    tables={R:np.load(B/f"CHECKED-COUPLED-R{R}.npz") for R in (10,12,15,20,30)}
    maps={R:np.load(B/f"CHECKED-COUPLED-GRID-R{R}.npz") for R in tables}
    fixed=read("FIXED-CHECK.json")
    cold={R:float(tables[R]["T_K"][np.searchsorted(tables[R]["T_K"],
        next(x["air_K"] for x in fixed["builds"] if x["R_m"]==R)-.025)]) for R in tables}
    for i,old in enumerate(read("owner-data/LEAST-SET-TRANSITIONS.json")):
        R=old["R_m"];height=old["z_m"];anomaly=old["sea_pressure_anomaly_hPa"];hum=old["RH"]
        mid=(old["from_offset_K"]+old["to_offset_K"])/2
        t,p,e,rho=atmosphere(height,mid,anomaly,hum);V=4/3*np.pi*R**3
        feasible=[m for m in range(16) if float(rho*V-coupled_mass(tables[R],m,t,load_pressure(p),cold[R]))>=0]
        least=[m for m in feasible if m.bit_count()==min(q.bit_count() for q in feasible)] if feasible else []
        iz=int(np.flatnonzero(z==height)[0]);ip=int(np.flatnonzero(a==anomaly)[0]);ih=int(np.argmin(abs(rh-hum)))
        roots=maps[R]["upper_zero_T_offset_K"][:,iz,ip,ih]
        candidates=[-20.,20.,cold[R]-(288.15-LAPSE*height)]+roots[np.isfinite(roots)].tolist()
        boundary=[]
        for name in ("from_offset_K","to_offset_K"):
            new=min(candidates,key=lambda value:abs(value-old[name]))
            boundary.append(dict(field=name,owner=old[name],checker=new,difference=new-old[name]))
        transitions.append(dict(row=i,R_m=R,z_m=height,RH=hum,owner_masks=old["masks"],checker_masks=least,
            masks_match=old["masks"]==least,boundaries=boundary))
    for prefix,filename in (("FROZEN","BOUNDARY-SLICES.csv"),("COUPLED","COUPLED-BOUNDARY-SLICES.csv")):
        for i,old in enumerate(csv.DictReader((B/"owner-data"/filename).open())):
            R=int(old["R_m"]);height=float(old["z_m"]);anomaly=float(old["pressure_anomaly_hPa"])
            hum=float(old.get("RH",old.get("RH_fraction")))
            iz=int(np.flatnonzero(z==height)[0]);ip=int(np.flatnonzero(a==anomaly)[0]);ih=int(np.argmin(abs(rh-hum)))
            grid=np.load(B/f"CHECKED-{prefix}-GRID-R{R}.npz")
            values=grid["upper_zero_T_offset_K"][:,iz,ip,ih]
            for m in range(16):
                field=f"mask_{m}_{'zero' if prefix=='FROZEN' else 'upper'}_offset_K"
                previous=float(old[field]);current=float(values[m])
                slices.append(dict(row=f"{filename}/{i}",field=field,owner=previous,checker=current,
                    difference=current-previous if math.isfinite(current) and math.isfinite(previous) else None,
                    finite_status_agrees=math.isfinite(current)==math.isfinite(previous)))
    for old in read("owner-data/COUPLED-ENVELOPE-SUMMARY.json")["rows"]:
        R=old["R_m"];height=old["z_m"]
        new=next(x for x in read(f"COUPLED-GRID-CHECK-R{R}.json")["boundaries"] if x["z_m"]==height)
        for field in ("worst_P_RH_upper_offset_K","any_P_RH_best_upper_offset_K","P0_RH0_upper_offset_K","P0_RH100_upper_offset_K"):
            left=old[field];right=new[field]
            comparisons.append(dict(row=f"family-summary/R{R}/z{height}",field=field,owner=left,checker=right,
                difference=right-left if left is not None and right is not None else None,
                finite_status_agrees=(left is None)==(right is None)))
    references={x["R_m"]:x for x in read("owner-data/MASS-CURVES.json")["reference"]}
    for i,old in enumerate(read("owner-data/ENVELOPE-SUMMARY.json")["fixed_reference_hull_examples"]):
        R=old["R_m"];g=references[R]
        t,p,e,rho=atmosphere(old["z_m"],old["T_offset_K"],old["anomaly_hPa"],old["RH_fraction"])
        load=float(load_pressure(p));witness=evaluate(R,g["tf_m"],g["tc_m"],load,11)
        new=dict(pressure_load_Pa=load,payload_kg=float(rho)*4/3*np.pi*R**3-witness["mass_kg"],
            minimum_SF_fixed_reference=witness["minimum_SF"])
        for field,value in new.items():
            comparisons.append(dict(row=f"original-reference/{i}",field=field,owner=old[field],checker=value,difference=value-old[field]))
    checked_fixed=np.load(B/"CHECKED-FIXED-GRID.npz")
    original_fixed=np.load(B/"owner-data/FIXED-HULL-WEATHER-GRID.npz")
    fixed_valid=(checked_fixed["payload_kg"]>=0)&(checked_fixed["minimum_SF"]>=1-1e-8)
    original_valid=(original_fixed["payload_kg"]>=0)&(original_fixed["minimum_SF"]>=1-1e-8)
    save("EXTRAS-CHECK.json",dict(transitions=transitions,slices=slices,comparisons=comparisons,
        fixed_grid_classification_disagreements=int(np.count_nonzero(fixed_valid!=original_valid)),
        fixed_grid_SF_comparison_tolerance=1e-8,
        transition_count=len(transitions),transition_mask_mismatches=sum(not x["masks_match"] for x in transitions),
        largest_transition_boundary_difference_K=max(abs(r["difference"]) for x in transitions for r in x["boundaries"]),
        slice_count=len(slices),slice_finite_mismatches=sum(not r["finite_status_agrees"] for r in slices),
        largest_slice_difference_K=max(abs(x["difference"]) for x in slices if x["difference"] is not None)))
    print("extras complete",len(transitions),len(slices),len(comparisons),flush=True)

if __name__=="__main__":run()
