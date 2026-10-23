"""CHECK-040 independent equations and search.

The temperature lookup is explicitly an owner numerical input until separately
reproduced. All stresses, gas, joining, mass and search are reconstructed here.
No upstream executable has been accessed.
"""
from pathlib import Path
import json, math
from functools import lru_cache
import numpy as np
from scipy.optimize import minimize_scalar, brentq

ROOT=Path(__file__).resolve().parent
TABLE=json.loads((ROOT/"owner/THERMAL-TABLE.json").read_text())
P0=95460.83791390515; L0=4889.442150186961; TA=284.9
RHO=16.018463373960138; RF=1850.; E0=290e9; EC=15000*6894.757293168361
GC=6800*6894.757293168361; FC=35*6894.757293168361
SW=25*6894.757293168361; KB=.5*67e9*RHO/2700; ALPHA=11.3e-6
DA=23.6e-6-ALPHA; RHO_A=L0/(4*np.pi*1000/3)
RG=8.31446261815324; MW=.01801528; BETA=brentq(lambda b:b**3+b-1,0,1)
FILM=.03*.45359237/.09290304
Q70=.5*RHO_A*(70*1852/3600)**2
QG=.5*RHO_A*(35*1852/3600+35*.3048)**2
WEATHER={"ISA":(0.,1.)}
for name,dt,ps,e in [("optimistic",10,.99,1000),("both",25.1,.98,6000)]:
    t=TA+dt; p=P0*ps; k=1-.378*e/p
    t100=t+2.6; p100=p*(t100/t)**(9.80665*k/(287.053*.0065))
    WEATHER[name]=(L0-4*np.pi*1000/3*k*p100/(287.053*t100),p100/P0)
DRYX=np.array([.78084,.20946,.00934,.0004,5.24e-6,.5e-6])
MASS=np.array([.028014,.031998,.039948,.04401,.004002602,.002016])
MDRY=DRYX@MASS/DRYX.sum()
DEFAULT=dict(weather="ISA",floor=False,pad="heavy70",vented=True,coating=.2,
 thermal=True,cure_fraction=1.,pressure_factor_floor=1.01,nu=.0768,wind="envelope",
 systems=100.,charge_joining=True,water=True,contamination=True,gas=True,
 weather_pressure=True,extra_service=0.,legacy_climate=False,thermal_modulus_Pa=None,
 bond_model="compliant037b",cure_temperature_K=(200-32)*5/9+273.15,
 scarf_ratio=30.34139731914874,edge_scarf_interaction=False)

def thermal_values(R,tc,table=None):
    a=(TABLE if table is None else table)[str(int(R))]
    x=np.log(tc); xx=np.log(a["tc_m"])
    return {k:np.interp(x,xx,a[k]) for k in
            ["gradient_K","swing_K","rise_K","curvature_temperature_K","max_outer_K","min_outer_K"]}

def usage_vector(mask,u):
    a=np.broadcast_to(np.array(u,dtype=float),(4,)).copy()
    return a*np.array([bool(mask&(1<<i)) for i in range(4)])

def loads(R,tf,tc,mask,u,settings,wind=None,table=None):
    s={**DEFAULT,**settings}
    tf,tc=np.broadcast_arrays(tf,tc)
    a=usage_vector(mask,u)
    E=E0*(293.6/290)**a[2]; F=345e6*(379.2/345)**a[2]
    Q=.33*(.82/.33)**a[1]; film=FILM*2**(-a[3])
    p=P0*max(s["pressure_factor_floor"],WEATHER[s["weather"]][1] if s["weather_pressure"] else 1)
    wind=s["wind"] if wind is None else wind
    p+=Q70 if wind=="envelope" or wind=="70kn" else QG if wind=="gust35" else 0
    nu=s["nu"]; h=tf+tc; sp=p*R/(4*tf)
    sigma0=E*h/(R*np.sqrt(1-nu**2)); cr=GC*h*h/(2*tf*tc)
    vc=sigma0/cr; kc=np.where(vc<=2,1-vc/4,1/vc)
    gf=.2+.4*np.minimum(vc,2); gbase=np.where(vc<2,.2,1.)
    gamma=gbase*(gf/gbase)**a[0]
    Et=s["thermal_modulus_Pa"] or E
    grad=np.zeros_like(tf); bend=grad.copy(); cure=grad.copy(); tau=grad.copy(); wall=grad.copy()
    allow=SW if s["thermal"] and s["bond_model"]!="rigid037" else FC
    if s["thermal"]:
        # Superseded 037 comparison used 2640 for solid density. Equal U maps
        # to tc*2640/2700 in the current lookup; this is only an interpolated
        # reconstruction, and its differences are reported separately.
        t=thermal_values(R,tc*(2640/2700 if s["bond_model"]=="rigid037" else 1),table)
        grad=Et*ALPHA*t["gradient_K"]*1.002/(2*(1-nu))
        bend=Et*h*ALPHA*t["curvature_temperature_K"]*1.002/R/(2*(1-nu**2))
        if s["bond_model"]!="rigid037":
            delta=1.002*DA*np.maximum(abs(s["cure_temperature_K"]-t["min_outer_K"]),
                                      abs(s["cure_temperature_K"]-t["max_outer_K"]))
            tau=delta*np.sqrt(2*KB*GC)
            wall=1.2*67e9*delta
            cure=s["cure_fraction"]*KB*DA*np.maximum(s["cure_temperature_K"]-t["min_outer_K"],0)*tc/(2*tf)*1.002
            if s["bond_model"]=="rigid_cure_constraint":
                tau=delta*np.sqrt(Et*tf*GC/tc)
            if s["bond_model"]=="rigid_swing_constraint":
                tau=DA*t["swing_K"]*1.002*np.sqrt(Et*tf*GC/tc)
        else:
            delta=DA*t["swing_K"]*1.002
            tau=delta*np.sqrt(Et*tf*GC/tc)
            allow=FC
    st=sp+grad+bend; sd=st+cure
    r=s["scarf_ratio"]; scarf=sd*r/(1+r*r)+(tau if s["edge_scarf_interaction"] or s["bond_model"]=="rigid037" else 0)
    global_demand=sp+(cure if s.get("cure_in_global",False) else 0)
    crimp_demand=st+(cure if s.get("cure_in_global",False) else 0)
    modes=dict(global_buckling=gamma*kc*sigma0/global_demand,face_compression=F/sd,
      core_shear_crimping=cr/crimp_demand,core_crush=np.full_like(tf,2*FC/p),
      face_wrinkling=BETA*Q*np.sqrt(E*EC*tf/tc)/sd,
      intracell_dimpling=E*(tf/.009525)**2/((1-nu**2)*sd),
      scarf_average_shear_screen=10e6/scarf,
      core_cell_wall_yield_screen=np.where(wall>0,227.53e6/np.maximum(wall,1e-30),1e30),
      thermal_core_interface_screen=allow/np.maximum(tau,1e-30))
    props=dict(E_Pa=E,Fcy_Pa=F,Q=Q,film_kg_m2_interface=film,gamma=gamma,
      gamma_full=gf,Vc=vc,pressure_face_stress_Pa=sp,added_gradient_stress_Pa=grad,
      added_bending_stress_Pa=bend,added_cure_compression_Pa=cure,
      thermal_interface_shear_Pa=tau,thermal_shear_allowable_Pa=allow,scarf_shear_Pa=scarf)
    return p,modes,props

def pad(R,kind):
    F70=.47*Q70*np.pi*R*R
    if kind=="none":
        return dict(mass_kg=0.,SF_70kn=0.,area_m2=0.,thickness_m=0.,force_N=0.)
    F=F70 if kind=="heavy70" else 1.4*.47*.5*RHO_A*20**2*np.pi*R*R
    A=F/FC; radius=np.sqrt(A/np.pi)
    thick=np.sqrt(3*1.33*F*np.log(radius/.025)/(2*np.pi*276e6))
    return dict(mass_kg=A*thick*2700,SF_70kn=F/F70,area_m2=A,thickness_m=thick,force_N=F)

def gas(R,tf,tc,joining,s,free_volume=False,leak=.001,conditioning=.1):
    A=4*np.pi*R*R; V=A*R/3
    pore=A*tc*(1-RHO/(2640 if s["bond_model"]=="rigid037" else 2700))
    trapped=0.*tc if s["vented"] else RHO_A*pore
    vf=4*np.pi/3*(R-2*tf-tc)**3+(pore if s["vented"] else 0)
    vol=vf if free_volume else V
    mbar=(1-(6000 if s["weather"]=="both" else 1000)/P0)*MDRY+(6000 if s["weather"]=="both" else 1000)/P0*MW
    ninitial=10*vol/(RG*TA); initial=ninitial*MDRY
    geom=joining["length_m"]*(.07/1250)/(tf*np.sqrt(1+s["scarf_ratio"]**2))
    nperm=10*3.34645e-16*geom*P0*86400
    nleak=.1*(leak*joining["length_m"]+.01)*86400/(RG*TA)
    nin=nperm+nleak; external=nin*mbar
    desorb=conditioning*(-np.expm1(-1))*(joining["film"]*.0485+A*tc*RHO*.001
                   +(joining["scarf"]+joining["splice"]+joining["seal"])*.01)
    aboard=initial+external+trapped
    pressure=(ninitial+nin+desorb/MW)*RG*320/vol
    late=pressure+trapped/MDRY*RG*320/vol
    limit=.01*P0
    return dict(pore_volume_m3=pore,trapped_air_kg=trapped,tube_bore_volume_m3=0.,
     initial_gas_kg=initial,external_ingress_24h_upper_kg=external,desorbed_24h_kg=desorb,
     gas_aboard_counted_kg=aboard,charged_gas_kg=np.maximum(.01*L0*(R/10)**3,aboard) if s["gas"] else 0.,
     hot_pressure_24h_upper_Pa=pressure,hot_pressure_after_late_vent_upper_Pa=late,
     pressure_limit_Pa=limit,pressure_SF=limit/pressure,late_vent_pressure_SF=limit/late,
     service_hardware_band_kg=[30,50],service_extra_charge_kg=s["extra_service"],
     battery_required_24h_kg=5*24/(150*.8*.9))

def evaluate(R,tf,tc,mask=11,u=1.,settings=None,full=True,table=None):
    s={**DEFAULT,**(settings or {})}
    tf,tc=np.broadcast_arrays(tf,tc)
    p,modes,prop=loads(R,tf,tc,mask,u,s,table=table)
    A=4*np.pi*R*R; V=A*R/3; L=L0*(R/10)**3; r=s["scarf_ratio"]
    length=A*(1/(.6096-r*tf)+1/(1.8288-r*tf))
    join=dict(film=2*A*prop["film_kg_m2_interface"],scarf=length*2*tf*np.sqrt(1+r*r)*.07,
              splice=length*.0005*tc*500,seal=length*.002)
    join["total"]=sum(join.values());join["length_m"]=length
    mf=2*A*RF*tf;mc=A*RHO*tc;floor=.05*(mf+mc)
    j=np.maximum(join["total"],floor) if s["floor"] else join["total"]
    pd=pad(R,s["pad"]);vac=gas(R,tf,tc,join,s)
    if s["legacy_climate"]:
        climate=(213.036426543752+18.704389882434043)*(R/10)**3
    else:climate=WEATHER[s["weather"]][0]*(R/10)**3
    bill=dict(faces=mf,core=mc,charged_joining=j if s["charge_joining"] else 0.,
       coating=s["coating"]*A,mooring_pad=pd["mass_kg"],
       gas=vac["charged_gas_kg"] if s["gas"] else 0.,systems=s["systems"],
       extra_service=s["extra_service"],water=.1*A if s["water"] else 0.,
       contamination=5*(R/10)**2 if s["contamination"] else 0.,weather_headroom=climate)
    least=np.min(np.broadcast_arrays(*modes.values()),axis=0)
    ans=dict(properties=prop,load_pressure_Pa=p,modes=modes,least_shell_and_thermal_SF=least,
      actual_joining=join,floor_allowance_kg=floor if s["floor"] else 0.,bill_kg=bill,lift_kg=L,
      signed_payload_kg=L-sum(bill.values()),vacuum=vac,pad=pd)
    if full:
        ans["geometry"]=dict(tf_m=tf,tc_m=tc,area_m2=A,volume_m3=V)
        ans["loadcases"]={w:loads(R,tf,tc,mask,u,s,w,table)[1] for w in ["70kn","gust35"]}
        ans["shell_and_thermal_pass"]=least>=1-1e-7
        ans["service_pressure_pass"]=vac["hot_pressure_24h_upper_Pa"]<=vac["pressure_limit_Pa"]
        ans["modeled_assembly_pass"]=ans["shell_and_thermal_pass"] & ans["service_pressure_pass"] & (pd["SF_70kn"]>=1-1e-9) & s["vented"] & (ans["signed_payload_kg"]>=-1e-3)
    return ans

def minimum_faces(R,tc,mask,u,settings,table=None):
    tc=np.asarray(tc,dtype=float)
    lo=np.full_like(tc,1e-7);hi=np.full_like(tc,.6096/settings.get("scarf_ratio",DEFAULT["scarf_ratio"])*.999)
    for it in range(43):
        mid=(lo+hi)/2
        _,m,_=loads(R,mid,tc,mask,u,settings,table=table)
        sf=np.min(np.broadcast_arrays(*list(m.values())[:7]),axis=0)
        ok=sf>=1
        hi=np.where(ok,mid,hi);lo=np.where(ok,lo,mid)
    return hi

def optimize(R,mask=11,u=1.,settings=None,n=501,table=None):
    s={**DEFAULT,**(settings or {})}
    lo=np.log(.001*R/10);hi=np.log(1.5*R/10)
    xs=np.linspace(lo,hi,n)
    def calc(x,details=False):
        tc=np.exp(x);tf=minimum_faces(R,tc,mask,u,s,table)
        e=evaluate(R,tf,tc,mask,u,s,False,table)
        valid=(e["least_shell_and_thermal_SF"]>=1-1e-7)&(e["vacuum"]["pressure_SF"]>=1)
        score=np.where(valid,e["signed_payload_kg"],-1e100)
        return (score,tf,tc,e) if details else score
    y=calc(xs)
    indices=list(np.where((y[1:-1]>=y[:-2])&(y[1:-1]>=y[2:])&(y[1:-1]>-1e90))[0]+1)
    indices+=list(np.where((y[:-1]>-1e90)!=(y[1:]>-1e90))[0])
    indices+= [int(np.argmax(y)),0,len(xs)-1]
    candidates=[(float(y[i]),float(xs[i])) for i in set(indices) if y[i]>-1e90]
    for i in set(indices):
        a=xs[max(0,i-1)];b=xs[min(n-1,i+2)]
        fit=minimize_scalar(lambda x:-float(calc(x)),bounds=(a,b),method="bounded",
                            options={"xatol":2e-13,"maxiter":100})
        if -fit.fun>-1e90:candidates.append((-float(fit.fun),float(fit.x)))
    if not candidates:return dict(status="no feasible geometry",signed_payload_kg=-1e100)
    score,x=max(candidates);y,tf,tc,e=calc(x,True)
    return dict(status="feasible",R_m=R,mask=mask,usage=u,settings=s,tf_m=float(tf),tc_m=float(tc),
                signed_payload_kg=float(y),least_SF=float(e["least_shell_and_thermal_SF"]))

def serial(o):
    if isinstance(o,np.ndarray):return o.tolist()
    if isinstance(o,np.generic):return o.item()
    raise TypeError(type(o))

if __name__=="__main__":
    point=json.loads((ROOT/"owner/RESULTS.json").read_text())["rows"][0]["two_factor_endpoint"]
    ans=evaluate(point["R_m"],point["geometry"]["tf_m"],point["geometry"]["tc_m"],
                 point["mask"],point["usage"],point["settings"])
    print(json.dumps(ans,default=serial,indent=2))
    print(optimize(10,n=1001))
