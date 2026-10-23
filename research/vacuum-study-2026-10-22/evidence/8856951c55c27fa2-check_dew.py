#!/usr/bin/env python3
"""Independent enthalpy integration; clarified noncode conventions pinned separately."""
from check_model import *
import time

def night_h(R,temperature,air,rh,wind,multiplier=1.):
    rho=(P_REF-.378*rh*float(es_water(air)))/(RD*air)
    reynolds=rho*wind*2*R/1.79e-5
    forced=.0257/(2*R)*(2+(.4*np.sqrt(reynolds)+.06*reynolds**(2/3))*.71**.4)
    natural=1.32*np.maximum(abs(np.asarray(temperature)-air),.05)**.25
    return multiplier*np.maximum(forced,natural)

def night(R, tf, tc, ta, sky, rh, wind, hours=12., dt=5., n=64,
          eps=.8, h_multiplier=1., condense=True, second_order=False):
    mu,w,_,_=quadrature(n)
    capacity=RHO_FACE*tf*1825 + .5*RHO_CORE*tc*900
    environment4=(1+mu)/2*sky**4+(1-mu)/2*ta**4
    vapor_pressure=rh*float(es_water(ta))
    vapor_enthalpy=2835000+1860*(ta-273.15)
    # Ice at freezing is the enthalpy zero; the dry skin has the same zero.
    enthalpy=np.full(n,capacity*(ta-273.15))
    inner=np.full(n,ta)
    deposit=np.zeros(n)
    outside_energy=0.; added_enthalpy=0.
    initial_energy=2*capacity*(ta-273.15)
    def decode(H,m):
        below=H<0
        above=H>334000*m
        delta=np.where(below,H/(capacity+2100*m),
                       np.where(above,(H-334000*m)/(capacity+4180*m),0.))
        melt=np.where(below,0.,np.where(above,m,H/334000))
        return 273.15+delta,melt
    def rhs(H,ti,m):
        to,_=decode(H,m)
        h=night_h(R,to,ta,rh,wind,h_multiplier)
        external=eps*SIGMA*(environment4-to**4)+h*(ta-to)
        conductance=130*RHO_CORE/2700/tc+4*.2*SIGMA*float(w@ti)**3
        inward=conductance*(to-ti)
        cavity=.2*SIGMA*(ti**4-w@(ti**4))
        saturation=np.where(to<273.15,es_ice(to),es_water(to))
        mdot=np.maximum(vapor_pressure-saturation,0)*h*(RD/RV)*.87**(-2/3)/(1005*P_REF)
        if not condense: mdot*=0
        return external-inward+vapor_enthalpy*mdot,(inward-cavity)/capacity,mdot,external
    count=int(round(hours*3600/dt))
    for i in range(count):
        dH,dti,dm,external=rhs(enthalpy,inner,deposit)
        if second_order:
            dH,dti,dm,external=rhs(enthalpy+.5*dt*dH,inner+.5*dt*dti,deposit+.5*dt*dm)
        enthalpy+=dt*dH;inner+=dt*dti;deposit+=dt*dm
        outside_energy+=dt*float(w@external)
        added_enthalpy+=dt*float(w@dm)*vapor_enthalpy
    outer,liquid=decode(enthalpy,deposit)
    delta_energy=float(w@(enthalpy+capacity*(inner-273.15)))-initial_energy
    return dict(R_m=R,Ta_K=ta,sky_K=sky,RH_water_fraction=rh,wind_m_s=wind,
        hours=hours,dt_seconds=dt,zones=n,eps=eps,h_multiplier=h_multiplier,
        mean_deposit_kg_m2=float(w@deposit),mean_liquid_kg_m2=float(w@liquid),
        mean_ice_kg_m2=float(w@(deposit-liquid)),peak_local_deposit_kg_m2=float(max(deposit)),
        deposit_total_kg=float(w@deposit)*4*np.pi*R**2,
        minimum_outer_K=float(min(outer)),maximum_outer_K=float(max(outer)),
        net_radiative_convective_energy_J_m2=outside_energy,
        vapor_enthalpy_added_J_m2=added_enthalpy,
        stored_energy_change_J_m2=delta_energy,
        energy_closure_J_m2=delta_energy-outside_energy-added_enthalpy,
        dry_capacity_each_skin_J_m2_K=capacity,second_order=second_order)

def heating(R,tf,tc,ta,sky,rh,wind,hours=12):
    mu,w,_,_=quadrature(128)
    dew=brentq(lambda t:float(es_water(t))-rh*float(es_water(ta)),200,340)
    setpoint=max(dew+.05,273.20)
    h=night_h(R,setpoint,ta,rh,wind)
    environment4=(1+mu)/2*sky**4+(1-mu)/2*ta**4
    watts=float([address](.8*SIGMA*(setpoint**4-environment4)+h*(setpoint-ta),0))
    startup=(2*RHO_FACE*tf*1825+RHO_CORE*tc*900)*max(setpoint-ta,0)/3600
    energy=watts*hours+startup
    area=4*np.pi*R**2
    return dict(dewpoint_K=dew,uniform_setpoint_K=setpoint,mean_power_W_m2=watts,
        total_power_kW=watts*area/1000,energy_Wh_m2_12h=energy,
        energy_kWh_12h=energy*area/1000,battery_mass_kg=energy*area/108,
        startup_Wh_m2=startup)

def run():
    start=time.time()
    original=read("owner-data/DEW-FROST.json")
    reference={int(x["R_m"]):x for x in read("owner-data/MASS-CURVES.json")["reference"]}
    cases=original["cases"]; comparisons=[];base=[];refined=[];mitigations=[]
    def compare(label,owner,check):
        for key,value in check.items():
            if key in owner and isinstance(value,(float,int)) and not isinstance(value,bool):
                if isinstance(owner[key],(float,int)):
                    comparisons.append(dict(row=label,field=key,owner=owner[key],checker=value,difference=value-owner[key]))
    for old in original["rows"]:
        R=int(old["R_m"]);c=cases[old["case"]];g=reference[R]
        kw=dict(R=R,tf=g["tf_m"],tc=g["tc_m"],**c)
        row=night(**kw);row["case"]=old["case"];base.append(row)
        compare(f"base/R{R}/{old['case']}",old,row)
        finer=night(**kw,dt=2.5,n=128,second_order=True)
        finer["case"]=old["case"];refined.append(finer)
        oldmit=next(x for x in original["mitigations"] if x["R_m"]==R and x["case"]==old["case"])
        low=night(**kw,eps=.05)
        heat=heating(**kw)
        compare(f"lowe/R{R}/{old['case']}",oldmit["low_e_0p05_night"],low)
        compare(f"heating/R{R}/{old['case']}",oldmit["heating"],heat)
        area=4*np.pi*R**2
        energy=row["mean_deposit_kg_m2"]*2.45e6/3600
        mitigations.append(dict(R_m=R,case=old["case"],heating=heat,low_e_0p05_night=low,
            cover_sensitivity_10_to_50_g_m2_kg=[area*.01,area*.05],
            solar_only_evaporation_energy_Wh_m2=energy,
            solar_only_ideal_hours_at_970_W_m2=energy/(.09*970/4)))
        print("night",R,old["case"],"deposit",row["mean_deposit_kg_m2"],
              "difference",row["mean_deposit_kg_m2"]-old["mean_deposit_kg_m2"],flush=True)
    sensitivities=[]
    for old in original["sensitivities_R10"]:
        g=reference[10]
        kw=dict(R=10,tf=g["tf_m"],tc=g["tc_m"],ta=old["Ta_K"],sky=old["sky_K"],
            rh=old["RH_water_fraction"],wind=old["wind_m_s"],hours=old["hours"],
            dt=old["dt_seconds"],n=old["zones"],eps=old["eps"],h_multiplier=old["h_multiplier"])
        row=night(**kw);sensitivities.append(row)
        compare(f"sensitivity/{len(sensitivities)-1}",old,row)
    g=reference[10];c=cases["clear_calm_reference"].copy();c["wind"]=2.
    dry=night(10,g["tf_m"],g["tc_m"],**c,condense=False,dt=2.5,n=128)
    compare("dry_reference",original["dry_reference_regression"],dry)
    save("DEW-CHECK.json",dict(base=base,refined=refined,mitigations=mitigations,
        sensitivities=sensitivities,dry_reference=dry,comparisons=comparisons,
        elapsed_seconds=time.time()-start,
        conventions="clarifications/CONVENTIONS.md: equal core capacity split; no coatings heat capacity; mean inner T conductance; P_REF mass transfer; humid-night forced-convection density"))
    print("complete",time.time()-start,flush=True)

if __name__=="__main__":run()
