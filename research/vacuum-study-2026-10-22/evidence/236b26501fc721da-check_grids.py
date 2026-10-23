#!/usr/bin/env python3
"""Rebuild complete weather grids and zero surfaces from checker-computed knots."""
from check_model import *
import sys,time

def coupled_mass(table,mask,temp,pressure,cold):
    t,p=np.broadcast_arrays(temp,pressure)
    ta=table["T_K"];pa=table["p_Pa"];m=table["mass_kg"][:,mask,:]
    i=np.clip(np.searchsorted(ta,t,side="right")-1,0,len(ta)-2)
    j=np.clip(np.searchsorted(pa,p,side="right")-1,0,len(pa)-2)
    a=np.clip((t-ta[i])/(ta[i+1]-ta[i]),0,1)
    b=np.clip((p-pa[j])/(pa[j+1]-pa[j]),0,1)
    v00=m[i,j];v01=m[i,j+1];v10=m[i+1,j];v11=m[i+1,j+1]
    finite=np.isfinite(v00)&np.isfinite(v01)&np.isfinite(v10)&np.isfinite(v11)
    with np.errstate(invalid="ignore"):
        out=(v00*(1-b)+v01*b)*(1-a)+(v10*(1-b)+v11*b)*a
    return np.where(finite&(t>=cold),out,np.inf)

def upper_root(fun,lower,upper):
    lo,hi=np.broadcast_arrays(lower,upper)
    lo=lo.copy();hi=hi.copy()
    bracket=(fun(lo)>=0)&(fun(hi)<=0)
    for _ in range(45):
        mid=(lo+hi)/2
        positive=fun(mid)>=0
        lo=np.where(positive,mid,lo);hi=np.where(positive,hi,mid)
    return np.where(bracket,(lo+hi)/2,np.nan)

def run(R,frozen=False):
    start=time.time()
    label="FROZEN" if frozen else "COUPLED"
    original=np.load(B/("owner-data/WEATHER-GRID.npz" if frozen else "owner-data/COUPLED-WEATHER-GRID.npz"))
    source=np.load(B/f"CHECKED-{label}-R{R}.npz")
    ir=int(np.flatnonzero(original["radii_m"]==R)[0])
    z=original["z_m"];o=original["T_offset_K"];a=original["sea_pressure_anomaly_hPa"];h=original["RH_fraction"]
    T,p,e,rho=atmosphere(z[:,None,None,None],o[None,:,None,None],a[None,None,:,None],h[None,None,None,:])
    pressure=load_pressure(p);V=4/3*np.pi*R**3
    cold=next(x["air_K"] for x in read("FIXED-CHECK.json")["builds"] if x["R_m"]==R)
    if not frozen:
        # The filed interpolation domain begins at its first warm knot.
        # Independent critical T agrees within 5e-7 K, but interpolating a
        # sliver toward the exploratory marginal root would be a different map.
        cold=float(source["T_K"][np.searchsorted(source["T_K"],cold-.025)])
    def mass(mask,temp,pressure):
        if frozen:return np.interp(pressure,source["p_Pa"],source["mass_kg"][mask])
        return coupled_mass(source,mask,temp,pressure,cold)
    feasible=np.zeros(T.shape,dtype=np.uint16);least=feasible.copy();card=np.full(T.shape,99,dtype=np.uint8)
    allpayload=[]
    for mask in range(16):
        pay=rho*V-mass(mask,T,pressure)
        if mask==11:primary=pay
        ok=pay>=0
        feasible|=np.where(ok,np.uint16(1<<mask),np.uint16(0))
        count=mask.bit_count()
        better=ok&(count<card)
        least=np.where(better,0,least)
        card=np.where(better,count,card)
        least|=np.where(ok&(count==card),np.uint16(1<<mask),np.uint16(0))
    previous=original["payload_endpoint11_kg"][ir]
    both=np.isfinite(primary)&np.isfinite(previous)
    with np.errstate(invalid="ignore"):
        diffs=np.where(both,primary-previous,0)
    finite_disagreement=np.isfinite(primary)!=np.isfinite(previous)
    summaries=dict(payload_max_abs_difference_kg=float(np.max(abs(diffs))),
        payload_finite_disagreements=int(np.count_nonzero(finite_disagreement)),
        payload_over_0p05_kg=int(np.count_nonzero(abs(diffs)>.05)),
        feasible_mask_disagreements=int(np.count_nonzero(feasible!=original["feasible_endpoint_masks"][ir])),
        least_mask_disagreements=int(np.count_nonzero(least!=original["least_cardinality_masks"][ir])),
        points=int(primary.size),positive_grid_fraction_not_probability=float(np.mean(primary>=0)))
    mismatches=[]
    any_bad=(abs(diffs)>.05)|finite_disagreement|(feasible!=original["feasible_endpoint_masks"][ir])|(least!=original["least_cardinality_masks"][ir])
    for index in np.argwhere(any_bad):
        key=tuple(index)
        mismatches.append(dict(R_m=R,z_m=z[key[0]],T_offset_K=o[key[1]],sea_pressure_anomaly_hPa=a[key[2]],
            RH=h[key[3]],owner_payload_kg=previous[key],checker_payload_kg=primary[key],
            owner_feasible_masks=original["feasible_endpoint_masks"][ir][key],checker_feasible_masks=feasible[key],
            owner_least_masks=original["least_cardinality_masks"][ir][key],checker_least_masks=least[key]))
    zz=z[:,None,None];aa=a[None,:,None];hh=h[None,None,:]
    shape=(len(z),len(a),len(h));roots=[]
    for mask in range(16):
        def payload(off):
            temp,pres,vap,density=atmosphere(zz,off,aa,hh)
            return density*V-mass(mask,temp,load_pressure(pres))
        low=np.full(shape,-60.) if frozen else np.broadcast_to(cold-(288.15-LAPSE*zz),shape)+1e-9
        high=np.full(shape,60.) if frozen else np.broadcast_to(326-(288.15-LAPSE*zz),shape)
        roots.append(upper_root(payload,low,high))
    roots=np.stack(roots)
    oldzero=np.load(B/("owner-data/ZERO-SURFACES.npz" if frozen else "owner-data/COUPLED-ZERO-SURFACES.npz"))
    key="zero_T_offset_K" if frozen else "upper_zero_T_offset_K"
    prev=oldzero[key][ir]
    common=np.isfinite(roots)&np.isfinite(prev)
    delta=np.where(common,roots-prev,0)
    summaries.update(zero_surface_points=int(roots.size),zero_max_abs_difference_K=float(np.max(abs(delta))),
        zero_finite_disagreements=int(np.count_nonzero(np.isfinite(roots)!=np.isfinite(prev))),
        zero_over_1e_3_K=int(np.count_nonzero(abs(delta)>.001)))
    for index in np.argwhere((np.isfinite(roots)!=np.isfinite(prev))|(abs(delta)>.001)):
        m,iz,ip,ih=map(int,index)
        mismatches.append(dict(kind="zero",R_m=R,mask=m,z_m=z[iz],sea_pressure_anomaly_hPa=a[ip],RH=h[ih],
            owner_offset_K=prev[m,iz,ip,ih],checker_offset_K=roots[m,iz,ip,ih]))
    bounds=[]
    for iz,height in enumerate(z):
        values=roots[11,iz];bounds.append(dict(R_m=R,z_m=height,
            worst_P_RH_upper_offset_K=float(np.min(values)),
            any_P_RH_best_upper_offset_K=float(np.nanmax(values)) if np.any(np.isfinite(values)) else None,
            P0_RH0_upper_offset_K=float(values[len(a)//2,0]),
            P0_RH100_upper_offset_K=float(values[len(a)//2,-1])))
    np.savez_compressed(B/f"CHECKED-{label}-GRID-R{R}.npz",payload_endpoint11_kg=primary,
        feasible_endpoint_masks=feasible,least_cardinality_masks=least,upper_zero_T_offset_K=roots)
    save(f"{label}-GRID-CHECK-R{R}.json",dict(R_m=R,kind=label,summary=summaries,mismatches=mismatches,
        boundaries=bounds,elapsed_seconds=time.time()-start,
        interpolation="Independent pressure/temperature bilinear interpolation; conservative cold exclusion at checker root+0.05 K."))
    print(label,R,summaries,"elapsed",time.time()-start,flush=True)

if __name__=="__main__":
    if "--all-available" in sys.argv:
        for frozen in (False,True):
            label="FROZEN" if frozen else "COUPLED"
            for R in (10,12,15,20,30):
                if (B/f"CHECKED-{label}-R{R}.npz").exists() and not (B/f"{label}-GRID-CHECK-R{R}.json").exists():
                    run(R,frozen)
    else:
        run(int(sys.argv[1]),"--frozen" in sys.argv)
