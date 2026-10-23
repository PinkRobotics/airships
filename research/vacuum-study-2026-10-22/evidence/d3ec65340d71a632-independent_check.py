"""Independent MAINLINE-036 check; reads pinned JSON data, never owner code."""
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parent
I = json.loads((ROOT / "inputs/036/INPUTS.json").read_text())
PUBLISHED = json.loads((ROOT / "inputs/036/RESULTS.json").read_text())
PI = math.pi
RHO = 1850.0
B = brentq(lambda x: x**3+x-1, 0, 1, xtol=1e-15)
PSI = 0.45359237 * 9.80665 / 0.0254**2
P0 = I["R10"]["case"]["p0_Pa"]
L0 = I["R10"]["case"]["lift0_kg"]
ROUTES = {v["id"]: v for v in I["R10"]["routes"]}
HELD = {v["route"]: v for v in I["R10"]["held"]}
C10 = I["R10"]["cores"]
C20 = I["R20"]["cores"]
SC = I["R20"]["scenario"]
T0 = I["R20"]["case"]["T0_K"]


def environmental(radius):
    area = 4*PI*radius**2
    lift = L0*(radius/10)**3
    dry = lift*(1-SC["pressure_swing_fraction"])*T0/(T0+SC["temperature_rise_K"])
    humid_loss = lift*.378*SC["water_vapour_Pa"]/P0*T0/(T0+SC["temperature_rise_K"])
    lines = {
        "retained_water_kg": area*SC["rho_water_kg_m3"]*SC["water_film_m"],
        "contamination_kg": area*SC["contamination_kg_m2"],
        "temperature_pressure_loss_kg": lift-dry,
        "humidity_loss_kg": humid_loss,
        "internal_gas_kg": SC["pressure_internal_fraction_of_p0"]*lift,
        "coating_kg": area*SC["extra_coating_kg_m2"],
        "systems_excess_kg": max(0, SC["vacuum_hardware_kg"]+SC["power_package_kg"]+SC["controls_kg"]-100),
    }
    return dict(radius_m=radius, area_m2=area, volume_m3=area*radius/3,
                lift_kg=lift, high_pressure_Pa=P0*(1+SC["pressure_swing_fraction"]),
                moist_lift_kg=dry-humid_loss, lines=lines, other_reserve_kg=sum(lines.values()))


ENV = environmental(20)


def config(radius, route, mechanics, E, nu, wrinkle, gamma=None):
    return dict(radius_m=radius, route=route, mechanics=mechanics, E_Pa=E,
                nu=nu, wrinkle=wrinkle, gamma_constant=gamma)


MODELS = {}
for route in ROUTES:
    held = HELD[route]
    MODELS[f"R10_{route}_held"] = config(10, route, "held", 290e9, .0752,
                                                    held["wrinkle"], held["gamma_constant"])
    MODELS[f"R10_{route}_full"] = config(10, route, "full", 293.6e9, .0752, .82)
    MODELS[f"R10_{route}_catalog_E_full"] = config(10, route, "full", 290e9, .0752, .82)
MODELS["R20_027_full"] = config(20, "027_coupled_eta09", "full", 293.6e9, .33, .82)
MODELS["R20_SR200_nu0752"] = config(20, "027_coupled_eta09", "full", 293.6e9, .0752, .82)
MODELS["R20_handbook_elastic"] = config(20, "027_coupled_eta09", "full", 42.5e6*PSI, .1, .82)


def mass_geometry(cfg, core, fraction, payload=0):
    """Solve closure with Newton in mass; R20 affine solution; vector/scalar."""
    f = np.asarray(fraction, dtype=float)
    radius = cfg["radius_m"]
    area = 4*PI*radius**2
    lift = L0*(radius/10)**3
    fixed = ENV["other_reserve_kg"] if radius == 20 else environmental(10)["other_reserve_kg"]
    available = lift-fixed-100-payload
    af = (1-f)/(2*area*RHO)
    ac = f/(area*core["rho"])
    floor_mass = np.zeros_like(f)+available/1.05
    if radius == 20:
        lam = 1/SC["panel_a_m"]+1/SC["panel_b_m"]
        mu, w, gap = SC["film_kg_m2_per_interface"], SC["splice_width_m"], SC["core_gap_m"]
        u = lam*(w*(1-f)+SC["rho_splice_kg_m3"]*gap*f/core["rho"])
        v = area*(lam*(2*mu*w+SC["rho_splice_kg_m3"]*SC["sealant_area_m2"])+2*mu)
        S = np.minimum(floor_mass, (available-v)/(1+u))
        Q = u*S+v
    else:
        rt = ROUTES[cfg["route"]]
        scarf = rt["seam"] == "scarf"
        a, bb = .6096, 1.8288
        c = I["R10"]["constants"]
        overlap_per_mass = c["scarf_ratio"]*af if scarf else 0*af
        joint_per_mass = c["core_splice_gap_m"]*c["core_splice_density_kg_m3"]*ac
        if scarf:
            joint_per_mass = joint_per_mass+2*af*math.hypot(1,c["scarf_ratio"])*c["scarf_film_kg_m2"]
        fixed_film = 2*area*(rt["bond_kg_m2"]+rt.get("primer_kg_m2",0))

        def joining(S):
            overlap = overlap_per_mass*S
            length = area*(1/(a-overlap)+1/(bb-overlap))
            line_mass = joint_per_mass*S+c["seal_both_faces_kg_m"]
            q = fixed_film+length*line_mass
            derivative = area*overlap_per_mass*(1/(a-overlap)**2+1/(bb-overlap)**2)*line_mass+length*joint_per_mass
            return q, derivative

        S = floor_mass.copy()
        for _ in range(16):
            q, dq = joining(S)
            step = (S+q-available)/(1+dq)
            S = np.minimum(floor_mass, S-step)
        Q, _ = joining(S)
    tf, tc = af*S, ac*S
    charged = np.maximum(.05*S,Q)
    masses = dict(structural=S, faces=(1-f)*S, core=f*S, physical_joining=Q,
                  charged_joining=charged, fixed_reserve=fixed+payload, systems=100.,
                  lift=lift, residual=S+charged+fixed+100+payload-lift)
    return tf, tc, masses


def evaluate(cfg, core, f, strength, payload=0):
    tf, tc, masses = mass_geometry(cfg, core, f, payload)
    radius, E, nu = cfg["radius_m"], cfg["E_Pa"], cfg["nu"]
    pressure = P0 if radius == 10 else ENV["high_pressure_Pa"]
    demand = pressure*radius/(4*tf)
    h = tf+tc
    ideal = E*h/(radius*math.sqrt(1-nu**2))
    crimp = h*h*core["Gc_Pa"]/(2*tf*tc)
    vc = ideal/crimp
    kc = np.where(vc <= 2, 1-vc/4, 1/vc)
    if cfg["mechanics"] == "held":
        gamma = np.zeros_like(vc)+cfg["gamma_constant"]
    elif cfg["mechanics"] == "today":
        gamma = np.where(vc < 2,.2,1.)
    else:
        gamma = .2+.4*np.minimum(vc,2)
    if radius == 20:
        eta = .9
        joint = eta*strength/demand
    elif ROUTES[cfg["route"]]["seam"] == "scarf":
        eta = 1
        joint = 10e6*(30**2+1)/30/demand
    else:
        eta = ROUTES[cfg["route"]].get("weld_retention",1)
        joint = eta*strength/demand
    modes = dict(
        global_=gamma*kc*ideal/demand,
        face=strength/demand,
        crimp=crimp/demand,
        crush=np.zeros_like(demand)+core["crush_Pa"]/(pressure/2),
        wrinkle=B*cfg["wrinkle"]*np.sqrt(E*core["Ec_Pa"]*tf/tc)/demand,
        dimple=E/(1-nu**2)*(tf/core["s_cell_m"])**2/demand,
        joint=joint,
    )
    modes["global"] = modes.pop("global_")
    least = np.minimum.reduce(list(modes.values()))
    return dict(radius_m=radius,route=cfg["route"],mechanics=cfg["mechanics"],
                E_Pa=E,nu=nu,wrinkle=cfg["wrinkle"],Fcy_Pa=strength,core=core["name"],
                fraction=f,tf_m=tf,tc_m=tc,demand_Pa=demand,required_Fcy_Pa=demand/eta,
                gamma=gamma,Vc=vc,Kc=kc,least_SF=least,modes=modes,masses_kg=masses,
                tag="PROJECTION",overall_installed_SF=None)


def native(x):
    if isinstance(x, dict): return {k:native(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [native(v) for v in x]
    if isinstance(x,np.ndarray): return x.tolist()
    if isinstance(x,np.generic): return x.item()
    return x


GRID = np.unique(np.r_[np.geomspace(1e-7,.01,96),np.linspace(.01,.99,2049),
                       1-np.geomspace(1e-7,.01,96)])


def maximize_core(cfg, core, strength, payload=0):
    ev = evaluate(cfg,core,GRID,strength,payload)
    y = ev["least_SF"]
    candidates = [float(GRID[0]),float(GRID[-1])]
    peaks = np.flatnonzero((y[1:-1]>=y[:-2]) & (y[1:-1]>=y[2:]))+1
    # Constant modes can make wide plateaux; retain endpoints and central point.
    groups = np.split(peaks,np.flatnonzero(np.diff(peaks)>1)+1)
    for group in groups:
        if len(group)==0: continue
        for j in set([int(group[0]),int(group[len(group)//2]),int(group[-1])]):
            res = minimize_scalar(lambda f:-float(evaluate(cfg,core,f,strength,payload)["least_SF"]),
                                  bounds=(float(GRID[j-1]),float(GRID[j+1])),
                                  method="bounded",options={"xatol":1e-14,"maxiter":100})
            candidates += [float(res.x),float(GRID[j])]
    # Explicit one-sided evaluation at the Vc=2 jump in today's convention.
    switches = np.flatnonzero(np.diff(np.sign(ev["Vc"]-2)))
    for j in switches:
        root = brentq(lambda f:float(evaluate(cfg,core,f,strength,payload)["Vc"]-2),
                      GRID[j],GRID[j+1],xtol=5e-15)
        candidates += [root, max(1e-7,root-1e-12), min(1-1e-7,root+1e-12)]
    values = [native(evaluate(cfg,core,f,strength,payload)) for f in candidates]
    best = max(values,key=lambda p:p["least_SF"])
    # A bounded minimizer has a sqrt(epsilon)*x stopping term. Refine active
    # mode intersections directly so that payload roots do not inherit it.
    near = [k for k,v in best["modes"].items() if v <= best["least_SF"]+1e-5]
    j = int(np.searchsorted(GRID,best["fraction"]))
    lo,hi = GRID[max(0,j-2)],GRID[min(len(GRID)-1,j+1)]
    for n,k in enumerate(near):
        for other in near[n+1:]:
            def difference(f):
                modes=evaluate(cfg,core,f,strength,payload)["modes"]
                return float(modes[k]-modes[other])
            if difference(lo)*difference(hi)<0:
                f=brentq(difference,lo,hi,xtol=5e-15)
                values.append(native(evaluate(cfg,core,f,strength,payload)))
    return max(values,key=lambda p:p["least_SF"])


def maximize(cfg, strength, payload=0):
    cores = C10 if cfg["radius_m"]==10 else C20
    rows = [maximize_core(cfg,c,strength,payload) for c in cores]
    return max(rows,key=lambda p:p["least_SF"])


def threshold(cfg):
    """All mode=1 boundary roots, then smallest required material limit."""
    candidates=[]
    cores = C10 if cfg["radius_m"]==10 else C20
    for core in cores:
        ev=evaluate(cfg,core,GRID,1e15)
        fs=[float(GRID[0]),float(GRID[-1])]
        use=[k for k in ev["modes"] if k!="face" and
             not(k=="joint" and (cfg["radius_m"]==20 or ROUTES[cfg["route"]]["seam"]=="eb"))]
        for mode in use:
            vals=ev["modes"][mode]-1
            roots=np.flatnonzero(vals[:-1]*vals[1:]<0)
            for j in roots:
                fs.append(brentq(lambda f:float(evaluate(cfg,core,f,1e15)["modes"][mode]-1),
                                 GRID[j],GRID[j+1],xtol=5e-15))
        for f in fs:
            p=native(evaluate(cfg,core,f,1e15))
            if min(p["modes"][k] for k in use)>=1-3e-11:
                candidates.append(native(evaluate(cfg,core,f,p["required_Fcy_Pa"])))
    return min(candidates,key=lambda p:p["required_Fcy_Pa"]) if candidates else None


CHECKS=[]
def check(label, actual, expected, rtol=1e-8, atol=1e-9):
    delta=float(actual)-float(expected)
    CHECKS.append(dict(item=label,published=float(expected),independent=float(actual),
                       delta=delta,tolerance=atol+rtol*abs(float(expected)),
                       pass_=abs(delta)<=atol+rtol*abs(float(expected))))


def compare(label, a, b):
    for k,v in b.items():
        if k not in a: continue
        if isinstance(v,dict): compare(label+"/"+k,a[k],v)
        elif isinstance(v,(float,int)) and not isinstance(v,bool):
            check(label+"/"+k,a[k],v,atol=1e-5 if k=="residual" else 1e-9)


def main():
    rederived=[]
    for model in PUBLISHED["models"]:
        cfg=MODELS[model["id"]]
        cores={c["name"]:c for c in (C10 if cfg["radius_m"]==10 else C20)}
        for label,point in [("threshold",model["threshold"])]+[(f"points/{j}",p) for j,p in enumerate(model["points"])]:
            if point is None: continue
            own=native(evaluate(cfg,cores[point["core"]],point["fraction"],point["Fcy_Pa"]))
            compare(model["id"]+"/"+label,own,point)
            rederived.append(dict(id=model["id"]+"/"+label,point=own))
    for held in PUBLISHED["held_geometry"]:
        p=held["point"]
        cfg=MODELS["R20_027_full"] if p["radius_m"]==20 else MODELS[f'R10_{p["route"]}_held']
        cores={c["name"]:c for c in (C10 if p["radius_m"]==10 else C20)}
        own=native(evaluate(cfg,cores[p["core"]],p["fraction"],p["Fcy_Pa"]))
        compare("held/"+held["id"],own,p)
    for j,p in enumerate(PUBLISHED["today_infinite_strength_screens"]):
        cfg=config(p["radius_m"],p["route"],"today",290e9,p["nu"],.33)
        cores={c["name"]:c for c in (C10 if p["radius_m"]==10 else C20)}
        own=native(evaluate(cfg,cores[p["core"]],p["fraction"],p["Fcy_Pa"]))
        compare(f"today/{j}",own,p)
    held_geometry={v["id"]:v["point"] for v in PUBLISHED["held_geometry"]}
    thickness=[]
    for j,row in enumerate(PUBLISHED["thickness"]):
        p=held_geometry[row["id"]]
        # Recompute nominal gauge from original frozen f and mass closure first.
        cfg=MODELS["R20_027_full"] if p["radius_m"]==20 else MODELS[f'R10_{p["route"]}_held']
        cores={c["name"]:c for c in (C10 if p["radius_m"]==10 else C20)}
        p0=native(evaluate(cfg,cores[p["core"]],p["fraction"],p["Fcy_Pa"]))
        loss=row.get("additional_total_loss_m",row.get("minus_tolerance_m"))
        tf=p0["tf_m"]-loss
        d=(P0 if p["radius_m"]==10 else ENV["high_pressure_Pa"])*p["radius_m"]/(4*tf)
        t=dict(finished_m=tf,membrane_demand_Pa=d,effective_Fcy_need_Pa=d/(.9 if p["radius_m"]==20 else 1),
               face_SF_multiplier=tf/p0["tf_m"])
        compare(f"thickness/{j}",t,row)
        thickness.append(dict(id=row["id"],loss_m=loss,**t))
    max_tf=(L0-environmental(10)["other_reserve_kg"]-100)/1.05/(2*4*PI*10**2*RHO)
    bound=dict(max_tf_m=max_tf,Fcy_at_SF1_Pa=P0*10/(4*max_tf),SF255=255e6/(P0*10/(4*max_tf)))
    compare("zero_core_bound",bound,PUBLISHED["R10_zero_core_face_bound"])
    # Stable quadratic positive root; coefficient table's F12 already includes cross-term convention.
    qa=(3.521+2.889-2.726)*1e-4
    qb=(2.394+.780)*1e-3
    root=2/(qb+math.sqrt(qb**2+4*qa))
    polynomial=dict(compression_ksi=root,compression_MPa=root*PSI/1000)
    compare("polynomial",polynomial,PUBLISHED["NASA4397_unqualified_polynomial_extrapolation"])
    compare("environment20",ENV,I["R20"]["reference"]["environment"])
    opt=[]
    for model in PUBLISHED["models"]:
        cfg=MODELS[model["id"]]
        th=threshold(cfg)
        if th is None: raise RuntimeError("no threshold "+model["id"])
        check(model["id"]+"/independent_threshold_strength",th["required_Fcy_Pa"],model["threshold"]["required_Fcy_Pa"],rtol=2e-7)
        points=[]
        for p in model["points"]:
            own=maximize(cfg,p["Fcy_Pa"])
            check(model["id"]+f'/optimized_SF/{p["Fcy_Pa"]}',own["least_SF"],p["least_SF"],rtol=2e-7)
            points.append(own)
        opt.append(dict(id=model["id"],threshold=th,points=points))
        print(model["id"],"threshold MPa",th["required_Fcy_Pa"]/1e6,flush=True)
    today=[]
    for j,p in enumerate(PUBLISHED["today_infinite_strength_screens"]):
        cfg=config(p["radius_m"],p["route"],"today",290e9,p["nu"],.33)
        own=maximize(cfg,1e15)
        check(f"today/{j}/independent_optimized_SF",own["least_SF"],p["least_SF"],rtol=2e-7)
        today.append(own)
    # Independent payload boundary on selected original R20 core.
    cfg=MODELS["R20_027_full"]
    core=I["R20"]["selected_core"]
    payload=brentq(lambda y:maximize_core(cfg,core,379.2e6,y)["least_SF"]-1,0,600,xtol=1e-7)
    point=maximize_core(cfg,core,379.2e6,payload)
    payload_row=dict(payload_kg=payload,tf_m=point["tf_m"],face_demand_Pa=point["demand_Pa"],
                     required_Fcy_Pa=point["required_Fcy_Pa"],point=point)
    # Payload is checked against a direct active-mode intersection, with a
    # separate absolute mass tolerance as well as the relative tolerance.
    for k,v in PUBLISHED["R20_payload_held"].items():
        check("payload/"+k,payload_row[k],v,rtol=2e-7,atol=1e-5 if k=="payload_kg" else 1e-10)
    result=dict(tag="PROJECTION",overall_installed_SF=None,biaxial_root=B,psi_Pa=PSI,
                environmental=ENV,rederived_published_points=rederived,models=opt,thickness=thickness,
                zero_core_bound=bound,polynomial=polynomial,today=today,payload=payload_row)
    (ROOT/"RECOMPUTED.json").write_text(json.dumps(native(result),indent=2)+"\n")
    failed=[x for x in CHECKS if not x["pass_"]]
    (ROOT/"NUMERICAL-CHECKS.json").write_text(json.dumps(dict(count=len(CHECKS),passed=len(CHECKS)-len(failed),
        failed=len(failed),tolerances="1e-8 relative arithmetic; 2e-7 relative optimization; explicit absolute mass residual tolerance",
        mismatches=failed,checks=CHECKS),indent=2)+"\n")
    print("CHECKS",len(CHECKS),"MISMATCHES",len(failed),json.dumps(failed[:10]),flush=True)


if __name__=="__main__":
    main()
