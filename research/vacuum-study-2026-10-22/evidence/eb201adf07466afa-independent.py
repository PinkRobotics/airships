"""Independent MAINLINE-033 arithmetic and shape-based optimizer.

Only frozen non-code INPUTS.json is read. No owner implementation is used.
The search variable is the face/core mass split; required face thickness is
derived from the independent ratio tc/tf, rather than a shell-mass solver.
"""
from pathlib import Path
from functools import lru_cache
import json
import math

import numpy as np
from scipy.optimize import brentq, minimize_scalar

ROOT = Path(__file__).resolve().parent
INPUT = json.loads((ROOT / "INPUTS.json").read_text())
CORES = INPUT["cores"]
BY_NAME = {c["name"]: c for c in CORES}
P0 = INPUT["case"]["p0_Pa"]
L0 = INPUT["case"]["lift0_kg"]
T0 = INPUT["case"]["T0_K"]
FACE_RHO = INPUT["face"]["rho"]
E0, E1 = INPUT["face"]["E_today_Pa"], INPUT["face"]["E_full_Pa"]
S0, S1 = INPUT["face"]["strength_today_Pa"], INPUT["face"]["strength_full_Pa"]
BETA = brentq(lambda b: b*b*b+b-1, 0, 1, xtol=5e-15)
DEFAULT = dict(nu=.0768, pressure_factor=1.01, joint_floor=False,
               scarf_screen=False, flat_gamma=False, primer_kg_m2=0.)


def reserves(radius):
    a = 4 * math.pi * radius**2
    lift = L0 * (radius / 10)**3
    w = INPUT["weather"]
    hot_dry = lift * (1-w["pressure_swing_fraction"]) * T0/(T0+w["temperature_rise_K"])
    humidity = lift * .378 * w["water_vapour_Pa"]/P0 * T0/(T0+w["temperature_rise_K"])
    rows = dict(temperature_pressure_loss=lift-hot_dry, humidity_loss=humidity,
                internal_air=w["pressure_internal_fraction_of_p0"]*lift,
                retained_water=a*w["rho_water_kg_m3"]*w["water_film_m"],
                contamination=w["contamination_kg"]*(radius/10)**2,
                systems_excess=max(0., sum(w[k] for k in
                    ["vacuum_hardware_kg", "power_package_kg", "controls_kg"])-100))
    return lift, a, rows


def face_properties(mask, usage):
    u = usage if mask & 4 else 0.
    return E0*(E1/E0)**u, S0*(S1/S0)**u


def joining(radius, tf, tc, settings):
    area = 4*math.pi*radius**2
    r = INPUT["joining"]["scarf_ratio"]
    a, b = INPUT["stock_panel"]["a_m"], INPUT["stock_panel"]["b_m"]
    if a-r*tf <= 0 or b-r*tf <= 0:
        return dict(total=math.inf, valid=False)
    length = area*(1/(a-r*tf)+1/(b-r*tf))
    rows = dict(
        film=2*area*INPUT["bond"]["kg_m2"],
        primer=2*area*settings["primer_kg_m2"],
        scarf=length*2*tf*math.hypot(1,r)*INPUT["joining"]["scarf_seam_adhesive_kg_m2"],
        splice=length*tc*INPUT["joining"]["core_splice_gap_m"]*INPUT["joining"]["core_splice_density_kg_m3"],
        sealing=length*INPUT["joining"]["sealing_total_both_faces_kg_m"],
    )
    return dict(total=sum(rows.values()), **rows, hull_seam_length_m=length,
                scarf_overlap_m=r*tf, valid=True)


def direct(radius, core, tf, tc, mask=3, usage=1., settings=None, reduced=False):
    """Critical pressures and direct mass takeoff at a supplied witness."""
    settings = DEFAULT | (settings or {})
    c = BY_NAME[core] if isinstance(core,str) else core
    p = P0*settings["pressure_factor"]
    E, strength = face_properties(mask,usage)
    nu = settings["nu"]
    h = tf+tc
    sigma = p*radius/(4*tf)
    sigma0 = E*h/(radius*math.sqrt(1-nu**2))
    crimp = c["Gc_Pa"]*h*h/(2*tf*tc)
    vc = sigma0/crimp
    kc = 1-vc/4 if vc <= 2 else 1/vc
    gb = .2 if settings["flat_gamma"] or vc < 2 else 1.
    gf = .2+.4*min(vc,2.)
    gamma = gb*(gf/gb)**usage if mask & 1 and not settings["flat_gamma"] else gb
    q = .33*(.82/.33)**usage if mask & 2 else .33
    wrinkle0 = BETA*math.sqrt(E*c["Ec_Pa"]*tf/tc)
    if reduced:
        if mask & 1:
            gamma = max(gb,sigma/(kc*sigma0))
        if mask & 2:
            q = max(.33,sigma/wrinkle0)
    r = INPUT["joining"]["scarf_ratio"]
    shear = sigma*r/(1+r*r)
    modes = dict(global_buckling=gamma*kc*sigma0/sigma,
                 face_compression=strength/sigma,
                 core_shear_crimping=crimp/sigma,
                 core_crush=2*c["crush_Pa"]/p,
                 face_wrinkling=q*wrinkle0/sigma,
                 intracell_dimpling=E*(tf/c["s_cell_m"])**2/((1-nu*nu)*sigma),
                 scarf_average_shear_screen=INPUT["joining"]["scarf_average_shear_screen_Pa"]/shear)
    lift, area, res = reserves(radius)
    faces = 2*area*tf*FACE_RHO
    core_mass = area*tc*c["rho"]
    structural = faces+core_mass
    j = joining(radius,tf,tc,settings)
    floor = .05*structural if settings["joint_floor"] else 0.
    charged = max(j["total"],floor)
    budget = sum(res.values())
    payload = lift-100-budget-structural-charged
    masses = dict(lift=lift,faces=faces,core=core_mass,structural=structural,
                  actual_joining=j["total"],joint_allowance_floor=floor,
                  unspent_joint_floor=max(0.,floor-j["total"]),charged_joining=charged,
                  systems_allowance=100.,fixed_reserve=budget,**res,payload=payload,
                  accounted_total=100+budget+structural+charged+payload)
    actual = dict(gamma=math.log(gamma/gb)/math.log(gf/gb) if gf>gb else 0.,
                  Q=math.log(q/.33)/math.log(.82/.33),
                  face_strength=math.log(strength/S0)/math.log(S1/S0))
    scored = [v for k,v in modes.items() if settings["scarf_screen"] or
              k != "scarf_average_shear_screen"]
    return dict(
        R_m=radius,core=c["name"],mask=mask,common_usage=usage,f=core_mass/structural,
        geometry=dict(tf_m=tf,tc_m=tc,separation_m=h,Vc=vc,
                      branch="stiff/moderate" if vc < 2 else "crimp",
                      nominal_panel_a_m=INPUT["stock_panel"]["a_m"],
                      nominal_panel_b_m=INPUT["stock_panel"]["b_m"],
                      published_standard_gauge_range=.0014986 <= tf <= .00635),
        properties=dict(E_Pa=E,strength_Pa=strength,nu=nu,gamma=gamma,Q=q,
                        gamma_full=gf,face_stress_Pa=sigma,scarf_average_shear_Pa=shear),
        improvement_factors=dict(gamma=gamma/gb,Q=q/.33,
                                 face_strength=strength/S0,coupled_E=E/E0),
        modes=modes,scored_least_SF=min(scored),masses_kg=masses,joining=j,
        settings=settings,actual_usage=actual)


def _arrays(fraction, core=None):
    f = np.asarray(fraction,dtype=float)
    if core is None:
        f = np.atleast_1d(f)[None,:]
        c = {k:np.asarray([x[k] for x in CORES])[:,None]
             for k in ["rho","Ec_Pa","Gc_Pa","crush_Pa","s_cell_m"]}
    else:
        c = BY_NAME[core] if isinstance(core,str) else core
    ratio = 2*FACE_RHO*f/(c["rho"]*(1-f))
    return f,ratio,c


def thickness_bounds(fraction, mask, usage, settings, core=None):
    """Bounds on tf/R at fixed y=tc/tf. Global uses a separate monotone root."""
    f,y,c = _arrays(fraction,core)
    p = P0*settings["pressure_factor"]
    nu = settings["nu"]
    E,strength = face_properties(mask,usage)
    rootnu = math.sqrt(1-nu*nu)
    vc_per_lambda = 2*E*y/(c["Gc_Pa"]*(1+y)*rootnu)
    global_coefficient = 4*E*(1+y)/(p*rootnu)
    crimp_bound = p*y/(2*c["Gc_Pa"]*(1+y)**2)
    lo = np.zeros_like(y)
    hi = np.maximum(2/vc_per_lambda,crimp_bound)
    if settings["flat_gamma"]:
        hi = np.maximum(2/vc_per_lambda,crimp_bound/.2)
    for _ in range(54):
        lam = (lo+hi)/2
        vc = vc_per_lambda*lam
        kc = np.where(vc<=2,1-vc/4,1/np.maximum(vc,1e-300))
        gb = np.where(vc<2,.2,1.)
        if settings["flat_gamma"]:
            g = .2
        elif mask & 1:
            g = gb*((.2+.4*np.minimum(vc,2))/gb)**usage
        else:
            g = gb
        safe = global_coefficient*lam**2*g*kc >= 1
        hi = np.where(safe,lam,hi)
        lo = np.where(safe,lo,lam)
    q = .33*(.82/.33)**usage if mask & 2 else .33
    bounds = np.maximum(hi,crimp_bound)
    bounds = np.maximum(bounds,p/(4*strength))
    bounds = np.maximum(bounds,p/(4*BETA*q*np.sqrt(E*c["Ec_Pa"]/y)))
    if settings["scarf_screen"]:
        r = INPUT["joining"]["scarf_ratio"]
        cap = INPUT["joining"]["scarf_average_shear_screen_Pa"]*(1+r*r)/r
        bounds = np.maximum(bounds,p/(4*cap))
    bounds = np.where(2*c["crush_Pa"]/p >= 1,bounds,np.inf)
    dimple = p*c["s_cell_m"]**2*(1-nu*nu)/(4*E)
    return bounds,dimple,y,c


def _mass_from_bounds(radius, bounds, dimple, y, coredata, settings):
    # Dimpling is the only shell-mode constraint that changes this similarity.
    lam = np.maximum(bounds,np.cbrt(dimple/radius**2))
    tf = radius*lam
    tc = tf*y
    lift,area,res = reserves(radius)
    a,b = INPUT["stock_panel"]["a_m"],INPUT["stock_panel"]["b_m"]
    r = INPUT["joining"]["scarf_ratio"]
    valid = (a-r*tf>0)&(b-r*tf>0)&np.isfinite(tf)
    with np.errstate(divide="ignore",invalid="ignore",over="ignore"):
        length = area*(1/(a-r*tf)+1/(b-r*tf))
        j = 2*area*(INPUT["bond"]["kg_m2"]+settings["primer_kg_m2"])
        j = j + length*(2*tf*math.hypot(1,r)*INPUT["joining"]["scarf_seam_adhesive_kg_m2"]
                       +tc*INPUT["joining"]["core_splice_gap_m"]*INPUT["joining"]["core_splice_density_kg_m3"]
                       +INPUT["joining"]["sealing_total_both_faces_kg_m"])
        s = area*tf*(2*FACE_RHO+y*coredata["rho"])
        charged = np.maximum(j,.05*s) if settings["joint_floor"] else j
        payload = lift-100-sum(res.values())-s-charged
    return np.where(valid,payload,-np.inf),tf,tc


def at_fraction(radius, fraction, core, mask, usage, settings):
    b,d,y,c = thickness_bounds(fraction,mask,usage,settings,core)
    return _mass_from_bounds(radius,b,d,y,c,settings)


def grid_fractions(n=4097, fraction_min=None):
    if fraction_min is not None:
        return np.linspace(fraction_min,1-fraction_min,n)
    return np.unique(np.r_[np.geomspace(1e-8,1e-3,31),
                           np.linspace(.001,.999,n),
                           1-np.geomspace(1e-8,1e-3,31)])


@lru_cache(maxsize=24)
def _grid_bounds(mask,usage,settings_json,n,fraction_min=None):
    settings = json.loads(settings_json)
    fractions = grid_fractions(n,fraction_min)
    return fractions,thickness_bounds(fractions,mask,usage,settings)


def optimize(radius,mask,usage=1.,settings=None,n=4097,refine_all=True,fraction_min=None):
    settings = DEFAULT | (settings or {})
    f,(b,d,y,c) = _grid_bounds(mask,float(usage),json.dumps(settings,sort_keys=True),n,fraction_min)
    vals,_,_ = _mass_from_bounds(radius,b,d,y,c,settings)
    winners=[]
    for ci,core in enumerate(CORES):
        v=vals[ci]
        best_index=int(np.argmax(v))
        candidates=[(float(v[best_index]),float(f[best_index]))]
        if not np.isfinite(v[best_index]):
            winners.append(dict(core=core["name"],payload_kg=None,f=None))
            continue
        peaks=np.flatnonzero((v[1:-1]>=v[:-2])&(v[1:-1]>=v[2:])&np.isfinite(v[1:-1]))+1
        if not refine_all:
            peaks=np.array([best_index])
        for ix in peaks:
            if ix<=0 or ix>=len(f)-1:
                continue
            def cost(z):
                a,_,_=at_fraction(radius,z,core,mask,usage,settings)
                return -float(a)
            opt=minimize_scalar(cost,bounds=(f[ix-1],f[ix+1]),method="bounded",
                                options={"xatol":2e-13,"maxiter":100})
            candidates.append((-float(opt.fun),float(opt.x)))
        val,frac=max(candidates)
        winners.append(dict(core=core["name"],payload_kg=val,f=frac))
    finite=[r for r in winners if r["payload_kg"] is not None]
    if not finite:
        return dict(R_m=radius,mask=mask,common_usage=usage,settings=settings,
                    payload_kg=None,per_core=winners)
    best=max(finite,key=lambda z:z["payload_kg"])
    _,tf,tc=at_fraction(radius,best["f"],best["core"],mask,usage,settings)
    point=direct(radius,best["core"],float(tf),float(tc),mask,usage,settings)
    point["per_core_optima"]=sorted(winners,key=lambda x:x["payload_kg"] if
                                   x["payload_kg"] is not None else -math.inf,reverse=True)
    return point


def ideal_at_fraction(f,core,mask,settings,usage=1.):
    """Ideal envelope at the volume-limited structural fraction, no dimpling."""
    lift,a,res=reserves(10.)
    volume_loss=sum(res[k] for k in ["temperature_pressure_loss","humidity_loss","internal_air"])
    cap=(1-volume_loss/lift)/(1.05 if settings["joint_floor"] else 1)
    structural=cap*lift
    tf=structural*(1-f)/(2*a*FACE_RHO)
    tc=structural*f/(a*core["rho"])
    point=direct(10.,core,tf,tc,mask,usage,settings)
    vals=[v for k,v in point["modes"].items() if k!="intracell_dimpling"
          and (settings["scarf_screen"] or k!="scarf_average_shear_screen")]
    return cap,min(vals)


def optimize_ideal(mask,settings,n=8193,fraction_min=None):
    """Independent broad grid and local refinements of the ideal envelope."""
    f=grid_fractions(n,fraction_min)[None,:]
    lift,area,res=reserves(10.)
    volume_loss=sum(res[k] for k in ["temperature_pressure_loss","humidity_loss","internal_air"])
    cap=(1-volume_loss/lift)/(1.05 if settings["joint_floor"] else 1)
    E,strength=face_properties(mask,1.)
    p=P0*settings["pressure_factor"]
    nu=settings["nu"]
    data={k:np.array([c[k] for c in CORES])[:,None]
          for k in ["rho","Gc_Pa","Ec_Pa","crush_Pa"]}
    tf=cap*lift*(1-f)/(2*area*FACE_RHO)
    tc=cap*lift*f/(area*data["rho"])
    h=tf+tc
    sig=p*10/(4*tf)
    sig0=E*h/(10*math.sqrt(1-nu*nu))
    crimp=data["Gc_Pa"]*h*h/(2*tf*tc)
    vc=sig0/crimp
    kc=np.where(vc<=2,1-vc/4,1/vc)
    if settings["flat_gamma"]:
        gamma=.2
    elif mask&1:
        gamma=.2+.4*np.minimum(vc,2)
    else:
        gamma=np.where(vc<2,.2,1.)
    q=.82 if mask&2 else .33
    val=np.minimum(gamma*kc*sig0/sig,strength/sig)
    val=np.minimum(val,crimp/sig)
    val=np.minimum(val,2*data["crush_Pa"]/p)
    val=np.minimum(val,BETA*q*np.sqrt(E*data["Ec_Pa"]*tf/tc)/sig)
    if settings["scarf_screen"]:
        val=np.minimum(val,(10e6*901/30)/sig)
    ff=f[0]
    rows=[]
    for ci,core in enumerate(CORES):
        v=val[ci]
        ix=int(np.argmax(v))
        candidates=[(float(v[ix]),float(ff[ix]))]
        peaks=np.flatnonzero((v[1:-1]>=v[:-2])&(v[1:-1]>=v[2:]))+1
        # Crush plateaux have a continuum of equal optima; their endpoints suffice.
        if len(peaks)>20:
            peaks=np.unique([peaks[0],peaks[-1],ix])
        for j in peaks:
            opt=minimize_scalar(lambda z:-ideal_at_fraction(z,core,mask,settings)[1],
                                bounds=(ff[j-1],ff[j+1]),method="bounded",
                                options={"xatol":2e-13})
            candidates.append((-float(opt.fun),float(opt.x)))
        best,frac=max(candidates)
        rows.append(dict(core=core["name"],largest_least_SF=best,f=frac))
    return dict(structural_mass_fraction_ceiling=cap,
                best=max(rows,key=lambda x:x["largest_least_SF"]),per_core=rows)


if __name__ == "__main__":
    s=DEFAULT.copy()
    for radius in [10,30,50]:
        point=optimize(radius,3,settings=s)
        print(radius,point["core"],point["masses_kg"]["payload"],flush=True)
