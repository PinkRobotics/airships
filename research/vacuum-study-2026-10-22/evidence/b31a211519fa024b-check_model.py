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

def qi(E1,E2=5.56e9,G=4.10e9,nu12=.39):
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
    nominal=.1*(joins["film"]*.0485+mc*c["core_outgas_fraction"]+.01*seam)
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
