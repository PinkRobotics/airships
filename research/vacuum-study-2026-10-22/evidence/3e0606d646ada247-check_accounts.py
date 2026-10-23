#!/usr/bin/env python3
"""Direct headline roots, continuous optimism usage, dew account, exact heater integral."""
from check_model import *
from check_dew import heating,night_h
import time

def heater_exact(R,tf,tc,ta,sky,rh,wind):
    dew=brentq(lambda t:float(es_water(t))-rh*float(es_water(ta)),200,340)
    setpoint=max(273.2,dew+.05)
    h=night_h(R,setpoint,ta,rh,wind)
    aa=.8*SIGMA*(setpoint**4-(sky**4+ta**4)/2)+h*(setpoint-ta)
    bb=.8*SIGMA*(ta**4-sky**4)/2
    b=abs(bb)
    power=0. if aa<=-b else float(aa) if aa>=b else (aa+b)**2/(4*b)
    startup=(2*RHO_FACE*tf*1825+RHO_CORE*tc*900)*max(setpoint-ta,0)/3600
    energy=12*power+startup;area=4*np.pi*R**2
    return dict(dewpoint_K=dew,uniform_setpoint_K=setpoint,mean_power_W_m2=power,
        total_power_kW=power*area/1000,energy_Wh_m2_12h=energy,
        energy_kWh_12h=energy*area/1000,battery_mass_kg=energy*area/108,
        startup_Wh_m2=startup,integral="Analytic mean of positive affine function in cos(theta).")

def run():
    start=time.time()
    reference={int(x["R_m"]):x for x in read("owner-data/MASS-CURVES.json")["reference"]}
    ownerdew=read("owner-data/DEW-FROST.json")
    dew=read("DEW-CHECK.json");accounts=[];heater=[];comparisons=[]
    oldaccounts=read("owner-data/RESULTS.json")["dew_account"]
    def compare(label,old,new):
        for k,v in new.items():
            if k in old and isinstance(v,(float,int)) and isinstance(old[k],(float,int)):
                comparisons.append(dict(row=label,field=k,owner=old[k],checker=v,difference=v-old[k]))
    for row in dew["base"]:
        R=int(row["R_m"]);case=row["case"];g=reference[R]
        params=ownerdew["cases"][case]
        T=params["ta"];p=P_REF;e=params["rh"]*es_water(T)
        rho=(p-.378*e)/(RD*T)
        A=4*np.pi*R**2;V=4/3*np.pi*R**3
        mass=sum(bill(R,g["tf_m"],g["tc_m"],11).values())
        deposit=row["mean_deposit_kg_m2"]
        original=next(x for x in oldaccounts if x["R_m"]==R and x["case"]==case)
        # Extra names are mapped below after preserving explicit arithmetic.
        new=dict(R_m=R,case=case,rho_kg_m3=float(rho),actual_lift_kg=float(rho*V),
            total_water_capacity_kg_m2=.1+(float(rho*V)-mass)/A,
            dry_start_payload_kg=float(rho*V)-mass+.1*A-deposit*A,
            preexisting_0p1_payload_kg=float(rho*V)-mass-deposit*A,
            deposit_kg_m2=deposit,ISA_water_capacity_kg_m2=.1+(LIFT_REF*(R/10)**3-mass)/A)
        accounts.append(dict(checker=new,owner=original))
        exact=heater_exact(R,g["tf_m"],g["tc_m"],**params)
        old=next(x for x in ownerdew["mitigations"] if x["R_m"]==R and x["case"]==case)["heating"]
        compare(f"heater_exact/R{R}/{case}",old,exact)
        # Check the reported Gauss quadrature convention without fitting it.
        quads={}
        for n in (64,128,256,512):
            mu,w,_,_=quadrature(n)
            h=night_h(R,exact["uniform_setpoint_K"],params["ta"],params["rh"],params["wind"])
            env=(1+mu)/2*params["sky"]**4+(1-mu)/2*params["ta"]**4
            q=.8*SIGMA*(exact["uniform_setpoint_K"]**4-env)+h*(exact["uniform_setpoint_K"]-params["ta"])
            quads[str(n)]=float([address](q,0))
        heater.append(dict(R_m=R,case=case,exact=exact,owner=old,quadrature_power_W_m2=quads))
    usages=[];endpoints=[];direct=[]
    owners=read("owner-data/RESULTS.json")["ISA_least_cardinality_usage"]
    for R in (10,12,15,20,30):
        lift=LIFT_REF*(R/10)**3;pressure=float(load_pressure(P_REF))
        points=[optimize(R,pressure,m,points=1500) for m in range(16)]
        feasible=[m for m in range(16) if points[m] and points[m]["mass_kg"]<=lift]
        least=[m for m in feasible if m.bit_count()==min(x.bit_count() for x in feasible)]
        endpoints.append(dict(R_m=R,feasible_masks=feasible,least_masks=least,
            payload_by_mask=[lift-x["mass_kg"] if x else None for x in points]))
        for mask in least:
            def f(u):return optimize(R,pressure,mask,usage=u,points=1500)["mass_kg"]-lift
            usage=brentq(f,0,1,xtol=1e-10)
            old=next(x for x in owners if x["R_m"]==R and x["mask"]==mask)
            new=dict(R_m=R,mask=mask,common_log_usage=usage,endpoint_payload_kg=lift-points[mask]["mass_kg"])
            compare(f"usage/R{R}/mask{mask}",old,new);usages.append(new)
        cold=next(x["air_K"] for x in read("FIXED-CHECK.json")["builds"] if x["R_m"]==R)
        for z in (100,500):
            def net(off):
                t,p,e,rho=atmosphere(z,off,-30,1)
                result=optimize(R,float(load_pressure(p)),11,air=float(t),points=1500)
                return float(rho)*4/3*np.pi*R**3-result["mass_kg"] if result else -1e30
            lower=cold-(288.15-LAPSE*z)+1e-5
            root=brentq(net,lower,40,xtol=1e-8) if net(lower)>0 else None
            old=next(x for x in read("owner-data/RESULTS.json")["design_family_boundaries"] if x["R_m"]==R and x["z_m"]==z)
            direct.append(dict(R_m=R,z_m=z,owner_interpolated_offset_K=old["worst_P_RH_upper_offset_K"],
                checker_direct_offset_K=root,difference_K=root-old["worst_P_RH_upper_offset_K"] if root is not None else None))
        print("usage and boundary",R,"complete",flush=True)
    save("ACCOUNTS-CHECK.json",dict(dew_accounts=accounts,heater_exact=heater,
        ISA_usage=usages,ISA_endpoints=endpoints,direct_family_boundaries=direct,
        comparisons=comparisons,seconds=time.time()-start))
    print("accounts complete",time.time()-start,flush=True)

if __name__=="__main__":run()
