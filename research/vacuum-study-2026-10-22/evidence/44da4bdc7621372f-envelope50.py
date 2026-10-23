#!/usr/bin/env python3
"""Pressure-dependent exact account curves and the four-dimensional weather map."""
import csv,itertools,time
from model50 import *

started=time.time()
radii=[10,12,15,20,30]
tables=json.loads((B/"THERMAL50.json").read_text())
pk=np.linspace(PMIN,106500,65)
curves={};checks=[];reference=[]
for r in radii:
    a=Account(r,tables[str(r)])
    curves[str(r)]={}
    for mask in range(16):
        result=a.optimum(pk,mask)
        curves[str(r)][str(mask)]={k:result[k].tolist() for k in
             ("mass_kg","tf_m","tc_m","minimum_SF")}
        if mask==11:
            reference.append(scalar_record(a,result))
            mids=(pk[:-1]+pk[1:])/2
            exact=a.optimum(mids,mask)
            errors=exact["mass_kg"]-np.interp(mids,pk,result["mass_kg"])
            dense=a.optimum(pk[[0,32,64]],mask,grid=3000)
            checks.append({"R_m":r,"midpoint_max_abs_mass_error_kg":float(np.max(abs(errors))),
                "dense_grid_max_abs_mass_error_kg":float(np.max(abs(
                    dense["mass_kg"]-result["mass_kg"][[0,32,64]])))})
        print("curve",r,mask,"seconds",round(time.time()-started,2),flush=True)
save("MASS-CURVES.json",{"p_Pa":pk,"radii_m":radii,"curves":curves,"checks":checks,
                       "reference":reference,"elapsed_seconds":time.time()-started})

z=np.arange(100,1501,50);t=np.arange(-20,21);p=np.arange(-30,31,2);rh=np.linspace(0,1,11)
weather=atmosphere(z[:,None,None,None],t[None,:,None,None],
                   p[None,None,:,None],rh[None,None,None,:])
payloads=[];feasible=[];minsets=[];ranges=[]
count=np.array([m.bit_count() for m in range(16)])
def masses(r,mask,pressure):
    return np.interp(pressure,pk,curves[str(r)][str(mask)]["mass_kg"])
for r in radii:
    a=Account(r,tables[str(r)])
    mass=np.stack([masses(r,m,weather["pressure_load_Pa"]) for m in range(16)])
    payload=weather["rho_kg_m3"]*a.volume-mass
    ok=payload>=0
    possible=np.sum(ok.astype(np.uint16)*(1<<np.arange(16,dtype=np.uint16))[:,None,None,None,None],axis=0,dtype=np.uint16)
    minimum=np.min(np.where(ok,count[:,None,None,None,None],99),axis=0)
    least=np.sum((ok&(count[:,None,None,None,None]==minimum)).astype(np.uint16)*
                 (1<<np.arange(16,dtype=np.uint16))[:,None,None,None,None],axis=0,dtype=np.uint16)
    payloads.append(payload[11]);feasible.append(possible);minsets.append(least)
    ranges.append({"R_m":r,"min_payload_kg":float(payload[11].min()),
                   "max_payload_kg":float(payload[11].max()),
                   "positive_grid_fraction_not_probability":float(np.mean(ok[11])),
                   "observed_least_mask_bitsets":np.unique(least).tolist()})
np.savez_compressed(B/"WEATHER-GRID.npz",radii_m=radii,z_m=z,T_offset_K=t,
    sea_pressure_anomaly_hPa=p,RH_fraction=rh,payload_endpoint11_kg=payloads,
    feasible_endpoint_masks=feasible,least_cardinality_masks=minsets)

# Each of the 16 endpoint zero surfaces is also a change surface for feasibility
# and thus for the set(s) with the smallest number of optimistic axes.
zz,pp,hh=np.meshgrid(z,p,rh,indexing="ij")
boundary=[]
for r in radii:
    a=Account(r,tables[str(r)])
    bymask=[]
    for mask in range(16):
        low=np.full(zz.shape,-60.);high=np.full(zz.shape,60.)
        def margin(temp):
            w=atmosphere(zz,temp,pp,hh)
            return w["rho_kg_m3"]*a.volume-masses(r,mask,w["pressure_load_Pa"])
        for _ in range(42):
            mid=(low+high)/2
            passes=margin(mid)>=0
            low=np.where(passes,mid,low);high=np.where(passes,high,mid)
        root=(low+high)/2
        root=np.where(margin(np.full(zz.shape,-60.))<0,np.nan,root)
        root=np.where(margin(np.full(zz.shape,60.))>=0,np.inf,root)
        bymask.append(root)
    boundary.append(bymask)
np.savez_compressed(B/"ZERO-SURFACES.npz",radii_m=radii,z_m=z,
    sea_pressure_anomaly_hPa=p,RH_fraction=rh,zero_T_offset_K=boundary)
rows=[]
for ri,r in enumerate(radii):
    for zi in [0,8,18,28]:
        for pi in [0,15,30]:
            for hi in [0,5,10]:
                row={"R_m":r,"z_m":int(z[zi]),"pressure_anomaly_hPa":int(p[pi]),
                     "RH_fraction":rh[hi]}
                row.update({f"mask_{m}_zero_offset_K":boundary[ri][m][zi,pi,hi] for m in range(16)})
                rows.append(row)
with (B/"BOUNDARY-SLICES.csv").open("w") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

# Design one actual hull at the ISA reference; retain its geometry at all weather.
fixed=[]
for ref in reference:
    a=Account(ref["R_m"],tables[str(ref["R_m"])])
    for alt in (100,500,1000,1500):
        for anom in (-30,0,30):
            w=atmosphere(alt,0,anom,1)
            sf=float(a.evaluate(ref["tf_m"],ref["tc_m"],w["pressure_load_Pa"])["minimum_SF"])
            fixed.append({"R_m":a.r,"z_m":alt,"T_offset_K":0,
                "anomaly_hPa":anom,"RH_fraction":1,"pressure_load_Pa":float(w["pressure_load_Pa"]),
                "payload_kg":float(w["rho_kg_m3"])*a.volume-ref["mass_kg"],
                "minimum_SF_fixed_reference":sf,"passes_reference_pressure":sf>=1-1e-8})
save("ENVELOPE-SUMMARY.json",{"ranges":ranges,"grid_shape_per_radius":weather["rho_kg_m3"].shape,
    "points_total":len(radii)*weather["rho_kg_m3"].size,
    "grid_fraction_is_not_weather_probability":True,
    "primary_endpoint_mask":11,"all_masks":{m:[AXES[i] for i in range(4) if m&(1<<i)] for m in range(16)},
    "fixed_reference_hull_examples":fixed,"seconds":time.time()-started})
print("DONE",time.time()-started,flush=True)
