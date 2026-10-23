#!/usr/bin/env python3
"""Independent climatic-marker atmosphere and all endpoint optima; frozen curve knots."""
from check_model import *
import time,csv

def state(old):
    z=old["z_m"];pct=old["percent"];family=old["family"]
    if family in ("hot","joint_hot_humid"):
        if family=="hot":
            sea=273.15+{1:49,5:46,10:45}[pct];ps=101325.
            ratio=.03*es_water(sea)/ps
        else:
            sea=273.15+43.3;ps=100000.
            ratio=es_water(273.15+{1:27.8,5:24.4,10:20}[pct])/ps
        temp=sea-LAPSE*z
        pressure=ps*(temp/sea)**(GRAV*(1-.378*ratio)/(RD*LAPSE))
        vapor=pressure*ratio;humidity=vapor/es_water(temp)
        anomaly=(ps-101325)/100
    elif family=="absolute_humidity_conditional":
        dew=273.15+{1:31,5:30,10:29}[pct]
        temp=314.15 if old["name"].endswith("T41") else dew
        vapor=es_water(dew);humidity=vapor/es_water(temp);anomaly=-13.25
        _,pressure,_,_=atmosphere(z,temp-(288.15-LAPSE*z),anomaly,humidity)
    else:
        temp=288.15-LAPSE*z;pressure={1:84700.,5:85600.,10:86100.}[pct]
        humidity=1. if old["name"].endswith("RH100") else 0.
        vapor=humidity*es_water(temp)
        ps=pressure/(temp/288.15)**(GRAV*(1-.378*vapor/pressure)/(RD*LAPSE))
        anomaly=(ps-101325)/100
    return dict(T_K=float(temp),p_Pa=float(pressure),e_Pa=float(vapor),RH=float(humidity),
        rho_kg_m3=float((pressure-.378*vapor)/(RD*temp)),
        pressure_load_Pa=float(load_pressure(pressure)),surface_pressure_anomaly_hPa=float(anomaly))

def run():
    start=time.time();days=[];comparisons=[]
    owner=read("owner-data/DESIGN-DAYS.json")["cases"]
    for case in owner:
        air=state(case);sizes=[]
        for field,value in air.items():
            comparisons.append(dict(row=case["name"],field=field,owner=case[field],checker=value,difference=value-case[field]))
        for old in case["sizes"]:
            R=old["R_m"];V=4/3*np.pi*R**3
            payload=[]
            for mask in range(16):
                p=optimize(R,air["pressure_load_Pa"],mask,air=air["T_K"],points=800)
                new=air["rho_kg_m3"]*V-p["mass_kg"] if p else -math.inf
                payload.append(new)
                prev=old["payload_by_mask_kg"][mask]
                comparisons.append(dict(row=f"{case['name']}/R{R}/mask{mask}",field="payload_kg",
                    owner=prev,checker=new,difference=new-prev if prev is not None else None))
            feasible=[m for m in range(16) if payload[m]>=0]
            least=[m for m in feasible if m.bit_count()==min(x.bit_count() for x in feasible)] if feasible else []
            frozen=optimize(R,air["pressure_load_Pa"],11,points=800)
            fp=air["rho_kg_m3"]*V-frozen["mass_kg"]
            comparisons.append(dict(row=f"{case['name']}/R{R}",field="frozen_mask11_payload_kg",
                owner=old["frozen_mask11_payload_kg"],checker=fp,difference=fp-old["frozen_mask11_payload_kg"]))
            sizes.append(dict(R_m=R,payload_by_mask_kg=payload,least_cardinality_masks=least,
                owner_least_masks=old["least_cardinality_masks"],frozen_mask11_payload_kg=fp))
        floating=[s["R_m"] for s in sizes if s["least_cardinality_masks"]]
        days.append(dict(name=case["name"],state=air,sizes=sizes,
            smallest_floating_sampled_radius_m=min(floating) if floating else None,
            owner_smallest_floating_sampled_radius_m=case["smallest_floating_sampled_radius_m"]))
        save("DESIGN-DAY-PROGRESS.json",dict(cases=days,comparisons=comparisons,seconds=time.time()-start))
        print("design day",case["name"],"complete",flush=True)
    save("DESIGN-DAY-CHECK.json",dict(cases=days,comparisons=comparisons,seconds=time.time()-start))
    run_frozen()

def run_frozen():
    start=time.time()
    source=read("owner-data/MASS-CURVES.json");pressure=np.asarray(source["p_Pa"]);radii=source["radii_m"]
    matrices=[];frozen_comparisons=[]
    for R in radii:
        table=np.zeros((16,len(pressure)))
        for m in range(16):
            for j,p in enumerate(pressure):
                point=optimize(R,float(p),m,points=800)
                table[m,j]=point["mass_kg"] if point else np.inf
                prev=source["curves"][str(R)][str(m)]["mass_kg"][j]
                frozen_comparisons.append(dict(R_m=R,mask=m,p_Pa=p,owner_mass_kg=prev,
                    checker_mass_kg=table[m,j],difference_kg=table[m,j]-prev))
        matrices.append(table)
        np.savez_compressed(B/f"CHECKED-FROZEN-R{R}.npz",p_Pa=pressure,mass_kg=table)
        print("frozen",R,"complete",flush=True)
    save("FROZEN-KNOT-CHECK.json",dict(comparisons=frozen_comparisons,seconds=time.time()-start))
    print("complete",time.time()-start,flush=True)

if __name__=="__main__":
    import sys
    run_frozen() if "--frozen-only" in sys.argv else run()
