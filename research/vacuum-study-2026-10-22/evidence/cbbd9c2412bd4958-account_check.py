"""CHECK-053 independent mechanics, moisture, service gas, mass and searches."""
from pathlib import Path
from functools import lru_cache
import json, math
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from thermal_check import ROOT, RHO, TA, RHO_A, Compare, dump

P0 = 95460.83791390515
L0 = 4889.442150186961
E0, EC, GC = 290e9, 15000*6894.757293168361, 6800*6894.757293168361
CRUSH, SW = 35*6894.757293168361, 25*6894.757293168361
NU, ALPHA, DA = .0768, 11.3e-6, (23.6-11.3)*1e-6
KB, CURE = .5*67e9*RHO/2700, (200-32)*5/9+273.15
SCARF, FILM = 30.34139731914874, .03*.45359237/.09290304
Q70 = .5*RHO_A*(70*1852/3600)**2
RG, MW = 8.31446261815324, .01801528
DRYX = np.array([.78084,.20946,.00934,.0004,5.24e-6,.5e-6])
MDRY = [address]([.028014,.031998,.039948,.04401,.004002602,.002016])/DRYX.sum()
BETA = brentq(lambda x:x**3+x-1, 0, 1)
TABLES = json.loads((ROOT/"THERMAL-INDEPENDENT.json").read_text())
OLD = json.loads((ROOT/"HISTORICAL-INDEPENDENT.json").read_text())["MLCCAg"]
WEATHER = {"ISA":(0., 1.)}
t500 = TA+10
p500 = P0*.99
k = 1-.378*1000/p500
t100 = t500+2.6
p100 = p500*(t100/t500)**(9.80665*k/(287.053*.0065))
WEATHER["optimistic"] = (L0-4*np.pi*1000/3*k*p100/(287.053*t100), p100/P0)

@lru_cache(None)
def lookup(model, radius):
    t = OLD[str(int(radius))] if model=="owner_table" else TABLES[model]["MLCCAg"][str(int(radius))]
    return np.log(t["tc_m"]), {key:np.array(t[key]) for key in (
        "gradient_K", "curvature_temperature_K", "max_outer_K", "min_outer_K")}

def thermal(model, radius, tc):
    xx, t = lookup(model, radius)
    return {key:np.interp(np.log(tc), xx, val) for key,val in t.items()}

def mechanics(case, tf, tc, mask, usage=1., favorable=False):
    R = case["R_m"]
    tf, tc = np.broadcast_arrays(np.asarray(tf),np.asarray(tc))
    u = [usage if mask&(1<<i) else 0. for i in range(4)]
    E = E0*(293.6/290)**u[2]
    F = 345e6*(379.2/345)**u[2]
    Et = E0 if favorable else E
    Q, film = .33*(.82/.33)**u[1], FILM*2**(-u[3])
    p = P0*max(1.01, WEATHER[case["weather"]][1])+Q70
    h = tf+tc
    sp = p*R/(4*tf)
    sigma0 = E*h/(R*np.sqrt(1-NU**2))
    cr = GC*h*h/(2*tf*tc)
    vc = sigma0/cr
    kc = np.where(vc<=2, 1-vc/4, 1/vc)
    gb = np.where(vc<2, .2, 1.)
    gamma = gb*((.2+.4*np.minimum(vc, 2))/gb)**u[0]
    tv = thermal(case["model"], R, tc)
    grad = Et*ALPHA*1.002*tv["gradient_K"]/(2*(1-NU))
    bend = Et*ALPHA*1.002*h*tv["curvature_temperature_K"]/(2*(1-NU**2)*R)
    delta = DA*1.002*np.maximum(abs(CURE-tv["min_outer_K"]), abs(CURE-tv["max_outer_K"]))
    tau = delta*np.sqrt(2*KB*GC)
    wall = 1.2*67e9*delta
    cure_num = KB*DA*1.002*np.maximum(CURE-tv["min_outer_K"],0)*tc/2
    cure = cure_num/tf
    demand = sp+grad+bend+cure
    include = case["cure_in_global"]
    modes = {
        "global":gamma*kc*sigma0/(sp+(cure if include else 0)),
        "compression":F/demand,
        "crimp":cr/(sp+grad+bend+(cure if include else 0)),
        "crush":np.ones_like(tf)*2*CRUSH/p,
        "wrinkle":BETA*Q*np.sqrt(E*EC*tf/tc)/demand,
        "dimple":E*(tf/.009525)**2/((1-NU**2)*demand),
        "scarf":10e6/(demand*SCARF/(1+SCARF**2)),
        "cell_wall":227.53e6/wall,
        "core_edge":SW/tau}
    props = dict(E_Pa=E,strength_Pa=F,Q=Q,film_kg_m2_interface=film,
        gamma=gamma,Vc=vc,pressure_stress_Pa=sp,gradient_stress_Pa=grad,
        pattern_stress_Pa=bend,cure_compression_Pa=cure,demand_Pa=demand,
        **tv,edge_shear_Pa=tau,edge_SF=SW/tau,wall_SF=227.53e6/wall,cure_numerator=cure_num)
    return p,modes,props

@lru_cache(None)
def pad(radius):
    force = .47*Q70*np.pi*radius**2
    area = force/CRUSH
    rad = np.sqrt(area/np.pi)
    thick = np.sqrt(3*1.33*force*np.log(rad/.025)/(2*np.pi*276e6))
    return area*thick*2700

def evaluate(case, tf, tc, mask, usage=1., favorable=False):
    R = case["R_m"]
    tf,tc = np.broadcast_arrays(np.asarray(tf),np.asarray(tc))
    p,modes,props = mechanics(case,tf,tc,mask,usage,favorable)
    area,volume,lift = 4*np.pi*R**2,4*np.pi/3*R**3,L0*(R/10)**3
    seam = area*(1/(.6096-SCARF*tf)+1/(1.8288-SCARF*tf))
    join = dict(film=np.ones_like(tf)*2*area*props["film_kg_m2_interface"],
        scarf=seam*2*tf*np.sqrt(1+SCARF**2)*.07,
        splice=seam*.0005*tc*500,seal=seam*.002)
    faces,core = 2*area*1850*tf,area*RHO*tc
    joining = np.maximum(sum(join.values()),.05*(faces+core)) if case["floor"] else sum(join.values())
    coat,primer = .0075752*1.1*area,.01*area
    seam_poly = join["scarf"]+join["splice"]+join["seal"]
    added_water = .002*join["film"]+.001*core+.01*(primer+coat+seam_poly)
    nominal = .1*(.0485*join["film"]+.001*core+.01*seam_poly)
    retained = added_water*(.1 if case["drying"]=="bake" else 1.)
    bed = (1.1*(added_water+nominal)+.1*(R/10)**3)/.1+2 if case["drying"]=="sorbent" else np.zeros_like(tf)
    ninitial = 10*volume/(RG*TA)
    geom = seam*(.07/1250)/(tf*np.sqrt(1+SCARF**2))
    nperm = 10*3.34645e-16*geom*P0*86400
    nleak = .1*(.001*seam+.01)*86400/(RG*TA)
    nin = nperm+nleak
    mbar = (1-1000/P0)*MDRY+(1000/P0)*MW
    gas = np.maximum(.01*lift, ninitial*MDRY+nin*mbar)
    capture = .95 if case["drying"]=="sorbent" else 0.
    release = (nominal+retained)*(-np.expm1(-1))
    # Incoming humid gas stays in the mass bill; captured incoming water is
    # removed only from the vapor-mole inventory.
    pressure = (ninitial+nin*(1-capture*1000/P0)+(1-capture)*release/MW)*RG*320/volume
    bill = dict(faces=faces,core=core,joining=joining,coating=coat,
        structural_primer=primer,external_water=.1*area,added_material_water=retained,
        sorbent=bed,pad=pad(R),systems=100.,gas=gas,
        contamination=5*(R/10)**2,weather=WEATHER[case["weather"]][0]*(R/10)**3)
    return dict(tf_m=tf,tc_m=tc,mask=mask,usage=usage,
        payload_kg=lift-sum(bill.values()),bill_kg=bill,joining_kg=join,seam_length_m=seam,
        properties=props,modes=modes,pressure_Pa=p,service_pressure_Pa=pressure,
        service_pressure_SF=.01*P0/pressure,lift_kg=lift)

def minimum_faces(case, tc, mask=11, usage=1., favorable=False):
    tc = np.asarray(tc)
    lo = np.full_like(tc,1e-7)
    hi = np.full_like(tc,min(.0195,.008*case["R_m"]/10))
    for _ in range(42):
        tf = (lo+hi)/2
        _,modes,_ = mechanics(case,tf,tc,mask,usage,favorable)
        ok = np.minimum.reduce(np.broadcast_arrays(*list(modes.values())[:7]))>=1
        hi = np.where(ok,tf,hi)
        lo = np.where(ok,lo,tf)
    return hi

def optimize(case, mask=11, usage=1., n=801, favorable=False):
    R = case["R_m"]
    xs = np.linspace(np.log(.0012*R/10), np.log(1.4*R/10), n)
    def at(x, detailed=False):
        tc = np.exp(x)
        tf = minimum_faces(case,tc,mask,usage,favorable)
        ans = evaluate(case,tf,tc,mask,usage,favorable)
        sf = np.minimum.reduce(np.broadcast_arrays(*ans["modes"].values()))
        valid = (sf>=1-2e-9)&(ans["service_pressure_SF"]>=1)
        score = np.where(valid,ans["payload_kg"],-1e90)
        return (score,ans) if detailed else score
    yy = at(xs)
    candidates = [(float(yy[j]),float(xs[j])) for j in (0,len(xs)-1,int(np.argmax(yy)))]
    indices = set((np.where((yy[1:-1]>=yy[:-2])&(yy[1:-1]>=yy[2:])&(yy[1:-1]>-1e80))[0]+1).tolist())
    indices.update(np.where((yy[:-1]>-1e80)!=(yy[1:]>-1e80))[0].tolist())
    for j in indices:
        fit = minimize_scalar(lambda z:-float(at(z)), bounds=(xs[max(j-1,0)],xs[min(j+2,len(xs)-1)]),
            method="bounded", options={"xatol":3e-13,"maxiter":100})
        candidates.append((-float(fit.fun),float(fit.x)))
    best,x = max(candidates)
    if best < -1e80:
        return None
    _,ans = at(x,True)
    return ans

def witness_paths(node, path=""):
    if isinstance(node,dict):
        if all(k in node for k in ("tf_m","tc_m","mask","usage","bill_kg")):
            yield path,node
        else:
            for k,v in node.items():
                yield from witness_paths(v,path+"/"+str(k))
    elif isinstance(node,list):
        for j,v in enumerate(node):
            yield from witness_paths(v,path+"/"+str(j))

def compare_witness(comp, group, path, own, expected):
    for k,v in own.items():
        if k not in expected:
            continue
        if isinstance(v,dict):
            for kk,vv in v.items():
                if kk in expected[k]:
                    comp.add(group,path+"/"+k+"/"+kk,vv,expected[k][kk],atol=2e-7,rtol=3e-10)
        else:
            comp.add(group,path+"/"+k,v,expected[k],atol=2e-7,rtol=3e-10)

def main():
    comp = Compare("ACCOUNT-COMPARISONS")
    config_count = witness_count = 0
    mask11 = []
    for model in ("owner_table","forced_conduction","mixed_conduction","forced_gap","mixed_gap"):
        rows = json.loads((ROOT/f"owner/ACCOUNT-{model}.json").read_text())
        for j,row in enumerate(rows):
            config_count += 1
            for path,witness in witness_paths(row["result"]):
                favorable = witness.get("search",{}).get("favorable_E_bound",False)
                ans = evaluate(row,witness["tf_m"],witness["tc_m"],witness["mask"],witness["usage"],favorable)
                compare_witness(comp,"all_witnesses",f"{model}/{j}{path}",ans,witness)
                witness_count += 1
                if path=="/endpoints/11":
                    mask11.append({k:row[k] for k in ("model","R_m","weather","cure_in_global","floor","drying")}|{"own":ans})
        print("accounted",model,flush=True)
    frozen = []
    crossings = {m:{"scarf":0,"global":0,"minimum_scarf_SF":1e30,"maximum_scarf_SF":0} for m in (
        "forced_conduction","mixed_conduction","forced_gap","mixed_gap")}
    for j,row in enumerate(json.loads((ROOT/"owner/FROZEN-GEOMETRY-CONSEQUENCES.json").read_text())):
        R,w,c,f,d = row["case"]
        case=dict(model=row["model"],R_m=R,weather=w,cure_in_global=c,floor=f,drying=d)
        point = row["original"]
        own = evaluate(case,point["tf_m"],point["tc_m"],point["mask"],point["usage"])
        compare_witness(comp,"frozen",str(j),own,row["revised"])
        s = crossings[row["model"]]
        new = []
        for mode in ("scarf","global"):
            if point["modes"][mode]>=1-2e-7 and own["modes"][mode]<1-2e-7:
                s[mode]+=1
                new.append(mode)
        s["minimum_scarf_SF"]=min(s["minimum_scarf_SF"],float(own["modes"]["scarf"]))
        s["maximum_scarf_SF"]=max(s["maximum_scarf_SF"],float(own["modes"]["scarf"]))
        frozen.append({"model":row["model"],"case":row["case"],"own":own,"new_crossings":new})
    dump("ACCOUNT-INDEPENDENT.json",mask11)
    dump("FROZEN-INDEPENDENT.json",frozen)
    dump("CROSSINGS-INDEPENDENT.json",crossings)
    comp.close("ACCOUNT")
    dump("ACCOUNT-COVERAGE.json",dict(configurations=config_count,witnesses=witness_count,
        stats=comp.stats,mismatches=len(comp.mismatches)))
    print(json.dumps({"stats":comp.stats,"crossings":crossings},indent=2),flush=True)

if __name__=="__main__":
    main()
