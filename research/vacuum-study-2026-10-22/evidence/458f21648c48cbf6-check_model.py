"""Independent CHECK-049 equations from the written methods; no owner code."""
from pathlib import Path
import json
import math
import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT=Path(__file__).resolve().parent
def read(name):
    return json.loads((ROOT/"intake"/name).read_text())
BASE=read("upstream/040_inputs.json")
FOLD=read("owner/FOLD.json")
COMP=read("owner/COMPUTE.json")
ROWS=FOLD["rows"]
CONS={c["key"]:c for c in FOLD["constructions"]}
LABELS={c["label"]:c["key"] for c in CONS.values()}
P0=BASE["case"]["p0_Pa"]
T0=BASE["case"]["T0_K"]
L0=BASE["case"]["lift0_kg"]
AIR=L0/(4*np.pi*10**3/3)
RGAS=8.31446261815324
WIND=.5*AIR*(70*1852/3600)**2
SCARF=BASE["joining"]["scarf_ratio"]
BETA=brentq(lambda b:b**3+b-1,0,1,xtol=1e-15)
F0=.03*.45359237/.3048**2
F1=F0/2
GUARD=1.002
SPECIES=read("upstream/040_034_inputs.json")["species"]

def qi(E1,E2=.806*6894.757293168361e6,G=.595*6894.757293168361e6,nu12=.39):
    d=1-nu12**2*E2/E1
    q1=E1/d;q2=E2/d;q12=nu12*E2/d
    a=(3*q1+3*q2+2*q12+4*G)/8
    b=(q1+q2+6*q12-4*G)/8
    return (a*a-b*b)/a,b/a

def props(key,override=None):
    c=dict(CONS[key]);core=dict(COMP["cores"][c["core"]]["core"])
    if c["face"]=="Be SR-200":
        c.update(Fc0=345e6,Fc1=379.2e6,E1=293.6e9,fibre_w=0)
    elif c["face"]=="AlBeMet AM162":
        c.update(Fc0=276e6,Fc1=314e6,E1=193e9,fibre_w=0)
    else:
        fc=313e6 if c["face"]=="M55J QI" else 220e6
        c.update(Fc0=fc,Fc1=fc/(1-c["nu"]),E1=c["E_today_Pa"],
                 fibre_w=.6*1910/1626 if c["face"]=="M55J QI" else .67)
    if c["core"].startswith("CR-III"):
        c.update(wall_E=67e9,wall_rho=2700,wall_yield=227.53e6,
                 edge_allow=25*6894.757293168361,k=130*core["rho"]/2700,
                 core_outgas_fraction=.001)
    else:
        c.update(COMP["cores"][c["core"]]["mat"])
        c["k"]=COMP["cores"][c["core"]]["k_W_mK"]
    c["coredata"]=core
    if override:c.update(override)
    return c

def weather(name,R):
    return (0.,1.) if name=="ISA" else (55.340908918*(R/10)**3,1.036552961984)

def pad(R,crush):
    force=.47*WIND*np.pi*R**2
    area=force/crush
    radius=np.sqrt(area/np.pi)
    thick=np.sqrt(3*(1+.33)*force*np.log(radius/.025)/(2*np.pi*276e6))
    return area*thick*2700

def axes(c,mask,u,Vc=None):
    E=c["E_today_Pa"]*(c["E1"]/c["E_today_Pa"])**(u if mask&4 else 0)
    Fc=c["Fc0"]*(c["Fc1"]/c["Fc0"])**(u if mask&4 else 0)
    Q=.33*(.82/.33)**(u if mask&2 else 0)
    film=F0*.5**(u if mask&8 else 0)
    if Vc is None:return E,Fc,Q,film
    g0=np.where(Vc<2,.2,1.)
    g1=.2+.4*np.minimum(Vc,2)
    gamma=g0*(g1/g0)**(u if mask&1 else 0)
    return E,Fc,Q,film,gamma

def bill(c,R,tf,tc,mask=15,u=1,finish="MLCCAg",variant="primary",
         climate="ISA",floor=False):
    a=4*np.pi*R**2;v=4*np.pi*R**3/3;lift=L0*(R/10)**3
    _,_,_,film=axes(c,mask,u)
    finishdata=FOLD["finishes"][finish]
    core=c["coredata"];heads,_=weather(climate,R)
    faces=2*a*c["rho_f"]*tf;mc=a*core["rho"]*tc
    length=a*(1/(.6096-SCARF*tf)+1/(1.8288-SCARF*tf))
    joins=dict(film=2*a*film,scarf=length*2*tf*np.sqrt(1+SCARF**2)*c["seam_film"],
               splice=length*.0005*tc*500,seal=length*.002)
    seam=joins["scarf"]+joins["splice"]+joins["seal"]
    joining=sum(joins.values())
    primer=a*finishdata["primer"];coating=a*finishdata["installed"]
    water0=(faces*c["face_water_fraction"]+mc*c["core_water_fraction"]+
            joins["film"]*.002+seam*c["seam_water_fraction"]+
            primer*.01+coating*.01)
    # 040 paint comparator does not add a separate absorbed-water inventory.
    water=(water0 if variant=="dry_gas" else .1*water0) if finish!="reference040" else 0.*water0
    release_fraction=c["core_outgas_fraction"] if finish=="reference040" else .001
    nominal=.1*(joins["film"]*.0485+mc*release_fraction+.01*seam)
    released=(nominal+water)*(1-math.exp(-1))
    leak=(.001*length+.01)*.1*86400/(RGAS*T0)
    # Only outer scarf is counted in the inherited permeation screen.
    perm=10*3.34645e-16*length*(c["seam_film"]/1250)/(tf*np.sqrt(1+SCARF**2))*P0*86400
    initial=10*v/(RGAS*T0)
    dry=SPECIES
    total=sum(x["dry_x"] for x in dry.values())
    mdry=sum(x["dry_x"]*x["M_kg_mol"] for x in dry.values())/total
    mwet=mdry*(1-1000/P0)+.01801528*1000/P0
    ingas=initial*mdry+(leak+perm)*mwet
    gas=np.maximum(.01*lift,ingas)
    pressure=(initial+leak+perm+released/.01801528)*RGAS*320/v
    ledger=dict(faces=faces,core=mc,charged_joining=np.maximum(joining,.05*(faces+mc)) if floor else joining,
                coating=coating,mooring_pad=pad(R,core["crush_Pa"]),gas=gas,systems=100.,
                extra_service=0.,water=a*(1. if variant=="water_1mm" else .1),
                contamination=5*(R/10)**2,weather_headroom=heads,absorbed_water=water,
                structural_primer=primer,desiccant=0.)
    return dict(payload_kg=lift-sum(ledger.values()),bill_kg=ledger,
                joining={**joins,"total":joining,"length_m":length},
                vacuum=dict(added_material_water_kg=water,desorbed_24h_kg=released,
                            pressure_SF=.01*P0/pressure),lift_kg=lift)

THERMAL_CACHE={}
def temperatures(c,R,tc,finish,thermal_mode="independent"):
    """Interpolate independent tables, or an explicitly pinned upstream table."""
    if thermal_mode=="pinned":
        if finish=="reference040":
            table=read("upstream/040_thermal_table.json")[str(R)]
        elif c["core"].startswith("CR-III") and R in [10,15]:
            table=read("upstream/048_thermal_tables.json")[finish][str(R)]
        else:raise ValueError("No pinned thermal table for this case")
    else:
        if not THERMAL_CACHE:
            THERMAL_CACHE.update(json.loads((ROOT/"THERMAL-INDEPENDENT-TABLES.json").read_text()))
        table=THERMAL_CACHE[f'{c["core"]}|{finish}|{R}']
    keys=["gradient_K","curvature_temperature_K","min_outer_K","max_outer_K","swing_K","rise_K"]
    t={k:np.interp(np.log(tc),np.log(table["tc_m"]),table[k]) for k in keys}
    if finish=="reference040" and thermal_mode=="independent":
        # 040 uses day gradient and curvature, whereas 048 uses max(day,night).
        for key in ["gradient_K","curvature_temperature_K"]:
            t[key]=np.interp(np.log(tc),np.log(table["tc_m"]),table["day_"+key])
    return t

def mechanics(c,R,tf,tc,mask=15,u=1,finish="MLCCAg",variant="primary",
              climate="ISA",floor=False,thermal=None,thermal_mode="independent"):
    tf=np.asarray(tf);tc=np.asarray(tc)
    therm=thermal if thermal is not None else temperatures(c,R,tc,finish,thermal_mode)
    core=c["coredata"];nu=c["nu"]
    E,Fc,Q,film=axes(c,mask,u)
    _,w=weather(climate,R);p=P0*max(1.01,w)+WIND
    h=tf+tc;sp=p*R/(4*tf)
    s0=E*h/(R*np.sqrt(1-nu**2));scr=core["Gc_Pa"]*h*h/(2*tf*tc)
    vc=s0/scr;kc=np.where(vc<=2,1-vc/4,1/vc)
    *_,gamma=axes(c,mask,u,vc)
    gradient=E*abs(c["alpha_f"])*therm["gradient_K"]*GUARD/(2*(1-nu))
    bending=E*h*abs(c["alpha_f"])*therm["curvature_temperature_K"]*GUARD/(2*(1-nu**2)*R)
    mismatch=abs(c["alpha_c"]-c["alpha_f"])*GUARD*np.maximum(
        abs(c["cure_K"]-therm["min_outer_K"]),abs(c["cure_K"]-therm["max_outer_K"]))
    K=.5*c["wall_E"]*core["rho"]/c["wall_rho"]
    edge=mismatch*np.sqrt(2*K*core["Gc_Pa"])
    cure=GUARD*K*(c["alpha_c"]-c["alpha_f"])*np.maximum(c["cure_K"]-therm["min_outer_K"],0)*tc/(2*tf)
    cure=np.maximum(cure,0)
    st=sp+gradient+bending;sd=st+cure
    global_demand=sp+cure if variant=="cure_in_global" else sp
    crimp_demand=sd if variant=="cure_in_global" else st
    scarf=sd*SCARF/(1+SCARF**2)+(edge if variant=="edge_scarf" else 0)
    modes=dict(global_buckling=gamma*kc*s0/global_demand,face_compression=Fc/sd,
               core_shear_crimping=scr/crimp_demand,core_crush=np.ones_like(tf)*2*core["crush_Pa"]/p,
               face_wrinkling=BETA*Q*np.sqrt(E*core["Ec_Pa"]*tf/tc)/sd,
               intracell_dimpling=E*(tf/core["s_cell_m"])**2/((1-nu*nu)*sd),
               scarf_average_shear_screen=c["seam_screen"]/scarf,
               core_cell_wall_yield_screen=c["wall_yield"]/(1.2*c["wall_E"]*mismatch),
               thermal_core_interface_screen=c["edge_allow"]/edge)
    return dict(modes=modes,Vc=vc,gamma=gamma,Q=Q,E_Pa=E,Fcy_Pa=Fc,film_kg_m2=film,
                cure_compression_Pa=cure,edge_shear_Pa=edge,thermal=therm)

def minimum_gauge(c,R,tc,mask,u,finish,variant,climate,thermal_mode="independent"):
    tc=np.asarray(tc)
    thermal=temperatures(c,R,tc,finish,thermal_mode)
    low=np.full_like(tc,max(c["tf_min"],1e-7));high=np.full_like(tc,min(.0195,.008*R/10))
    # Solve only gauge-dependent screens. Edge/cell-wall are checked separately.
    names=["global_buckling","face_compression","core_shear_crimping","core_crush",
           "face_wrinkling","intracell_dimpling","scarf_average_shear_screen"]
    def valid(tf):
        modes=mechanics(c,R,tf,tc,mask,u,finish,variant,climate,thermal=thermal)["modes"]
        return np.minimum.reduce([modes[k]+np.zeros_like(tc) for k in names])>=1
    any_feasible=valid(high)
    for _ in range(42):
        mid=(low+high)/2
        ok=valid(mid)
        high=np.where(ok,mid,high);low=np.where(ok,low,mid)
    mech=mechanics(c,R,high,tc,mask,u,finish,variant,climate,thermal=thermal)
    m=mech["modes"]
    feasible=any_feasible&(m["thermal_core_interface_screen"]>=1)&(m["core_cell_wall_yield_screen"]>=1)
    return high,feasible,mech

def optimize(c,R,mask=15,u=1,finish="MLCCAg",variant="primary",
             climate="ISA",floor=False,n=180,thermal_mode="independent"):
    loggrid=np.linspace(np.log(.0012*R/10),np.log(1.4*R/10),n)
    def evaluate(z,full=False):
        tc=np.exp(np.atleast_1d(z))
        tf,feasible,mech=minimum_gauge(c,R,tc,mask,u,finish,variant,climate,thermal_mode)
        account=bill(c,R,tf,tc,mask,u,finish,variant,climate,floor)
        feasible=feasible&(account["vacuum"]["pressure_SF"]>=1)
        score=np.where(feasible,account["payload_kg"],-np.inf)
        return (score,tf,tc,account,mech) if full else score
    scores=evaluate(loggrid);finite=np.isfinite(scores)
    if not np.any(finite):return None
    candidates=[(float(scores[i]),float(loggrid[i])) for i in [int(np.argmax(scores))]]
    for i in range(1,n-1):
        if finite[i] and scores[i]>=scores[i-1] and scores[i]>=scores[i+1]:
            opt=minimize_scalar(lambda z:-float(evaluate(z)[0]),bounds=(loggrid[i-1],loggrid[i+1]),
                                method="bounded",options=dict(xatol=2e-11))
            if np.isfinite(opt.fun):candidates.append((-float(opt.fun),float(opt.x)))
    for i in np.flatnonzero(finite[:-1]!=finite[1:]):
        lo=loggrid[i];hi=loggrid[i+1];left=finite[i]
        for _ in range(32):
            mid=(lo+hi)/2;ok=np.isfinite(evaluate(mid)[0])
            if ok==left:lo=mid
            else:hi=mid
        z=lo if left else hi;candidates.append((float(evaluate(z)[0]),float(z)))
    _,z=max(candidates)
    score,tf,tc,account,mech=evaluate(z,True)
    def scalar(x):
        if isinstance(x,dict):return {k:scalar(v) for k,v in x.items()}
        a=np.asarray(x)
        return float(a.ravel()[0])
    result=scalar(dict(tf_m=tf,tc_m=tc,**account,**mech))
    result["binding"]=[k for k,v in result["modes"].items() if abs(v-1)<2e-5]
    return result

def least(c,R,**kwargs):
    from itertools import combinations
    for count in range(5):
        found=[]
        for subset in combinations([1,2,4,8],count):
            mask=sum(subset);endpoint=optimize(c,R,mask,1,**kwargs)
            if endpoint is None or endpoint["payload_kg"]<0:continue
            lo=0.;hi=1.
            for _ in range(25):
                mid=(lo+hi)/2;test=optimize(c,R,mask,mid,**kwargs)
                if test is None or test["payload_kg"]<0:lo=mid
                else:hi=mid
            point=optimize(c,R,mask,hi,**kwargs)
            found.append(dict(mask=mask,usage=hi,point=point))
        if found:return min(found,key=lambda x:x["usage"])
    return None
