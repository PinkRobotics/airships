"""MAINLINE-061: independently evaluated pinned scalar accounts, no owner imports.

Units: metres, Pa, kg. All physics and material transfers are QUESTIONABLE;
improvements, mass growth and service extrapolations are PROJECTION.
"""
import math
from functools import lru_cache

import numpy as np
from scipy.optimize import brentq, minimize, minimize_scalar

from source61 import source

I = source("040", "INPUTS.json")
C = I["core"]
F = I["face"]
CASE = I["case"]
P0, L10 = CASE["p0_Pa"], CASE["lift0_kg"]
NU = CASE["nu"]
AIR = L10 / (4 * math.pi * 10**3 / 3)
QWIND = max(.5 * AIR * (70 * 1852 / 3600)**2,
            .5 * AIR * (35 * 1852 / 3600 + 35 * .3048)**2)
QWEATHER = {"ISA": 1., "optimistic": 1.0365529619839071}
CF = {"ISA": 0., "optimistic": .011318450493548677}
THERMAL48 = source("048", "THERMAL-TABLES.json")["MLCCAg"]
THERMAL40 = source("040", "THERMAL-TABLE.json")
CHECK = source("check057", "INDEPENDENT-RECORDS.json")
P3DATA = source("052", "RESULTS.json")
CLASSES = source("057", "RESULTS.json")["classification"]
SPECIES = source("034", "INPUTS.json")["species"]
DRY_M = sum(x["dry_x"]*x["M_kg_mol"] for x in SPECIES.values())/sum(x["dry_x"] for x in SPECIES.values())
RU = 8.31446261815324
BETA = brentq(lambda b: b**3+b-1, 0., 1.)
SCARF = I["joining"]["scarf_ratio"]
COAT = .00833272
P2PROPS = ("face_strength", "face_modulus", "face_density", "gamma", "Q",
           "core_specific_shear", "bond_film", "finish")


def growth(bill, lead, maturity="concept", sleeves=None):
    result = {}
    for key, mass in bill.items():
        c = CLASSES[lead].get(key)
        if key == "cavity_capture":
            c = {"type": "hardware", "maturity": "estimated", "own_margin": 0}
        elif key == "cavity_barrier_delta":
            c = {"type": "thermal", "maturity": "calculated", "own_margin": 0}
        elif key == "cavity_battery":
            c = {"type": "battery", "maturity": "estimated", "own_margin": 0}
        if c is None or c["type"] is None or maturity == "none":
            rate = 0.
        elif maturity == "TRL7":
            # NASA Table VI-1: hardware 5%; adjacent battery column 6%.
            rate = .06 if c["type"] == "battery" else .05
        else:
            rate = {"structure": .15, "hardware": .30, "thermal": .20, "battery": .25}[c["type"]]
        if lead == "P2" and key == "coating":
            extra = mass / 1.1 * max(0., rate-.1)
        elif lead == "P3" and key == "joint_sleeves_and_allowance":
            extra = max(0., (mass if sleeves is None else sleeves)*(1+rate)-mass)
        else:
            extra = mass * rate
        result[key] = extra
    return result


def pad_mass(r):
    q = .5 * AIR * (70 * 1852 / 3600)**2
    force = .47*q*math.pi*r*r
    area = force/C["crush_Pa"]
    radius = math.sqrt(area/math.pi)
    t = math.sqrt(3*1.33*force*math.log(radius/.025)/(2*math.pi*276e6))
    return area*t*2700.


def thermal(r, tc, finish="inherited"):
    table = THERMAL48[str(r)] if r in (10, 12, 15) else THERMAL40[str(r)]
    x = np.log(tc)
    xp = np.log(table["tc_m"])
    vals = {k: np.interp(x, xp, table[k]) for k in (
        "gradient_K", "curvature_temperature_K", "max_outer_K", "min_outer_K")}
    return vals


def p2(r, weather, tf, tc, factors=None, basis="endpoint", maturity="concept",
       floor=False, detail=False, pressure_override=None, revert=()):
    """Direct equations, with all factor-dependent masses re-priced before MGA.

    revert names assumptions taken at the handbook value while basis stays endpoint.
    A handbook basis, or any basis other than endpoint, keeps 061's else-branch.
    """
    f = factors or {}
    rev = set(revert or ())
    def handbook(name):
        return name in rev or basis != "endpoint"
    tf, tc = np.broadcast_arrays(np.asarray(tf), np.asarray(tc))
    e0 = F["E_today_Pa"] if handbook("face_modulus") else F["E_full_Pa"]
    s0 = F["strength_today_Pa"] if handbook("face_strength") else F["strength_full_Pa"]
    E = e0*f.get("face_modulus", 1.)
    strength = s0*f.get("face_strength", 1.)
    rho = F["rho"]/f.get("face_density", 1.)
    Q = min(.82, (.33 if handbook("Q") else .82)*f.get("Q", 1.))
    G = C["Gc_Pa"]*f.get("core_specific_shear", 1.)
    film = I["film"]["baseline_kg_m2_interface" if handbook("bond_film")
                      else "favorable_kg_m2_interface"]/f.get("bond_film", 1.)
    p = P0*max(1.01, QWEATHER[weather])+QWIND if pressure_override is None else pressure_override
    A, lift = 4*math.pi*r*r, L10*(r/10)**3
    h = tc+tf
    sigp = p*r/(4*tf)
    sig0 = E*h/(r*math.sqrt(1-NU**2))
    crimp = G*h*h/(2*tf*tc)
    vc = sig0/crimp
    kc = np.where(vc <= 2., 1-vc/4, 1/vc)
    gamma0 = np.where(vc < 2., .2, 1.) if handbook("gamma") else .2+.4*np.minimum(vc, 2.)
    gamma = np.minimum(1., gamma0*f.get("gamma", 1.))
    t = thermal(r, tc)
    grad = E*11.3e-6*(1.002*t["gradient_K"])/(2*(1-NU))
    bend = E/(1-NU**2)*h/2*11.3e-6/r*(1.002*t["curvature_temperature_K"])
    kb = .5*67e9*C["rho"]/2700.
    dt = 1.002*np.maximum(abs(366.4833333333333-t["max_outer_K"]),
                          abs(366.4833333333333-t["min_outer_K"]))
    dtc = 1.002*np.maximum(366.4833333333333-t["min_outer_K"], 0.)
    cure = kb*12.3e-6*dtc*tc/(2*tf)
    tau = 12.3e-6*dt*np.sqrt(2*kb*G)
    demand = sigp+grad+bend+cure
    modes = {
        "global_buckling": gamma*kc*sig0/(sigp+cure),
        "face_compression": strength/demand,
        "core_shear_crimping": crimp/demand,
        "face_wrinkling": BETA*Q*np.sqrt(E*C["Ec_Pa"]*tf/tc)/demand,
        "intracell_dimpling": E*(tf/C["s_cell_m"])**2/((1-NU**2)*demand),
        "core_crush": np.full_like(tf, 2*C["crush_Pa"]/p),
        "scarf_average_shear": 10e6/(demand*SCARF/(1+SCARF**2)),
        "core_wall_yield": 227.53e6/(1.2*67e9*12.3e-6*dt),
        "thermal_interface": 25*6894.757293168361/tau,
    }
    length = A*(1/(.6096-SCARF*tf)+1/(1.8288-SCARF*tf))
    joint = {"film": 2*A*film,
             "scarf": length*2*tf*math.sqrt(1+SCARF**2)*.07,
             "splice": length*.0005*tc*500,
             "seal": length*.002}
    faces, core = 2*A*rho*tf, A*C["rho"]*tc
    actual = sum(joint.values())
    charged = np.maximum(actual, .05*(faces+core)) if floor else actual
    coating = A*COAT/f.get("finish", 1.)
    water = .1*(.002*joint["film"]+.001*core+.01*A*.01+
                 .01*coating+.01*(joint["scarf"]+joint["splice"]+joint["seal"]))
    if r not in (10, 12, 15):
        # CHECK-057's declared large-R transfer uses the R10 water allocation.
        direct10 = next(x for x in CHECK if x["source"] == "048" and x["R_m"] == 10
                        and x["weather"] == "ISA" and not x["floor"])
        reference = next(x["bill"]["absorbed_water"] for x in direct10["masks"] if x["mask"] == 11)
        # New candidates use a resized water account; exact frozen transfer is separately tabulated.
        if basis == "frozen_transfer":
            water = np.full_like(tf, reference*(r/10)**2)
    volume = 4*math.pi*r**3/3
    initial = 10*volume/(RU*284.9)*DRY_M
    leak_mol = (length*.001+.01)*.1/(RU*284.9)*86400
    path_area = length*(.07/1250)/(tf*math.sqrt(1+SCARF**2))
    perm_mol = 10*3.34645e-16*path_area*P0*86400
    molmass = (1-1000/P0)*DRY_M+1000/P0*.01801528
    ingress = (leak_mol+perm_mol)*molmass
    release = .1*(.0485*joint["film"]+.001*core+
                    .01*(joint["scarf"]+joint["splice"]+joint["seal"]))
    hot_pressure = (initial/DRY_M+leak_mol+perm_mol+
                    (release+water)*(1-np.exp(-1))/.01801528)*RU*320/volume
    modes["vacuum_pressure"] = .01*P0/hot_pressure
    gas = np.maximum(.01*lift,initial+ingress)
    bill = {"faces": faces, "core": core, "charged_joining": charged,
            "coating": coating, "mooring_pad": pad_mass(r), "gas": gas,
            "systems": 100., "extra_service": 0., "water": .1*A,
            "contamination": 5*(r/10)**2, "weather_headroom": CF[weather]*lift,
            "absorbed_water": water, "structural_primer": .01*A, "desiccant": 0.}
    extra = growth(bill, "P2", maturity)
    payload = lift-sum(bill.values())-sum(extra.values())
    if not detail:
        return payload, modes
    cast = lambda x: float(np.asarray(x))
    binding = sorted(((k,cast(v)) for k,v in modes.items()), key=lambda x:x[1])
    return {"R_m": r, "weather": weather, "basis": basis, "maturity": maturity,
            "geometry": {"tf_m": cast(tf), "tc_m": cast(tc)}, "factors": f,
            "properties": {"E_Pa": E, "strength_Pa": strength, "density_kg_m3": rho,
                           "Q": Q, "Gc_Pa": G, "gamma": cast(gamma),
                           "Vc": cast(vc), "film_kg_m2_interface": film},
            "pressure_Pa": p, "bill_kg": {k:cast(v) for k,v in bill.items()},
            "growth_kg": {k:cast(v) for k,v in extra.items()},
            "lift_kg": lift, "payload_kg": cast(payload),
            "mass_before_growth_kg": cast(sum(bill.values())),
            "growth_total_kg": cast(sum(extra.values())),
            "modes": {k:cast(v) for k,v in modes.items()}, "binding": binding[:3],
            "vacuum": {"hot_pressure_24h_Pa":cast(hot_pressure),
                       "pressure_limit_Pa":.01*P0,"gas_charge_kg":cast(gas)},
            "floor": floor, "revert": sorted(rev), "qualified_hull_SF": None, "tag": "PROJECTION"}


def p2_opt(r, weather, factors=None, basis="endpoint", maturity="concept", floor=False, n=180, revert=()):
    kw = dict(factors=factors, basis=basis, maturity=maturity, floor=floor, revert=tuple(revert))

    def at(tc):
        tc = np.atleast_1d(tc)
        lo = np.full_like(tc, 1e-6)
        hi = np.full_like(tc, min(.0195, .008*r/10))
        # Face feasibility can jump at Vc=2; the two branches are handled below.
        for _ in range(36):
            mid = (lo+hi)/2
            _, modes = p2(r, weather, mid, tc, **kw)
            active = [v for k,v in modes.items() if k not in ("thermal_interface","core_wall_yield","core_crush")]
            good = np.minimum.reduce(active) >= 1.
            hi = np.where(good, mid, hi)
            lo = np.where(good, lo, mid)
        tf = hi*(1+2e-10)
        val, modes = p2(r, weather, tf, tc, **kw)
        valid = np.minimum.reduce(list(modes.values())) >= 1-1e-8
        return np.where(valid, val, -1e25), tf

    grid = np.geomspace(.0012*r/10, 1.4*r/10, n)
    v, _ = at(grid)
    picks = [int(np.argmax(v))]
    picks += list(np.flatnonzero((v[1:-1] >= v[:-2]) & (v[1:-1] >= v[2:]) & (v[1:-1] > -1e24))+1)
    trials = [(float(v[j]), float(grid[j])) for j in set(picks)]
    for j in set(picks):
        if j == 0 or j == len(grid)-1:
            continue
        fit = minimize_scalar(lambda x: -at(np.exp(x))[0][0],
                              bounds=(np.log(grid[j-1]),np.log(grid[j+1])),
                              method="bounded", options={"xatol": 2e-10})
        trials.append((-fit.fun, float(np.exp(fit.x))))
    # Boundary of the thermal screen is sometimes the optimum.
    valid = v > -1e24
    for j in np.flatnonzero(valid[:-1] != valid[1:]):
        a,b = grid[j],grid[j+1]
        for _ in range(30):
            mid = math.sqrt(a*b)
            if (at(mid)[0][0] > -1e24) == bool(valid[j]):
                a = mid
            else:
                b = mid
        tc = a if valid[j] else b
        trials.append((float(at(tc)[0][0]),tc))
    value, tc = max(trials)
    if value < -1e24:
        return None
    tf = float(at(tc)[1][0])
    return p2(r, weather, tf, tc, **kw, detail=True)


def single_p2(r, weather, prop, basis="endpoint", maturity="concept"):
    base = p2_opt(r,weather,basis=basis,maturity=maturity)
    if base and base["payload_kg"] >= 0:
        return {"property":prop,"status":"already closes","factor":1.,"solution":base}
    cap = {"gamma": 5., "Q": .82/.33 if basis != "endpoint" else 1.}.get(prop, 1e4)
    grid = sorted(set([1., min(cap,1.05),min(cap,1.1),min(cap,1.2),min(cap,1.5),
                       min(cap,2.),min(cap,3.),min(cap,5.),min(cap,10.),
                       min(cap,30.),min(cap,100.),min(cap,1000.),cap]))
    best = base
    previous = 1.
    for f in grid[1:]:
        point = p2_opt(r,weather,{prop:f},basis,maturity)
        if point is not None and (best is None or point["payload_kg"] > best["payload_kg"]):
            best = point
        if point is not None and point["payload_kg"] >= 0:
            lo,hi = previous,f
            for _ in range(24):
                mid = math.sqrt(lo*hi)
                point = p2_opt(r,weather,{prop:mid},basis,maturity,n=160)
                if point is not None and point["payload_kg"] >= 0: hi = mid
                else: lo = mid
            final=p2_opt(r,weather,{prop:hi*(1+1e-7)},basis,maturity,n=320)
            return {"property":prop,"status":"conditional closure","factor":hi,
                    "solution":final,"root_bracket":[lo,hi]}
        previous=f
    return {"property":prop,"status":"not alone in declared domain","factor":None,
            "tested_factor_cap":cap,"best":best,
            "next_mode": None if best is None else best["binding"]}


def combination_p2(r, weather, basis, singles, maturity="concept"):
    """Search factor product in joint geometry/property space, then reopt geometry."""
    names=list(P2PROPS)
    caps=np.array([1e3,1e3,1e3,5.,.82/(.82 if basis=="endpoint" else .33),1e3,1e4,1e4])
    base=p2_opt(r,weather,basis=basis,maturity=maturity)
    bounds=[(math.log(1e-6),math.log(min(.0195,.008*r/10))),
            (math.log(.0012*r/10),math.log(1.4*r/10))]
    bounds += [(0.,math.log(x)) for x in caps]
    starts=[]
    for s in singles:
        if s.get("factor") and s.get("solution"):
            point=s["solution"]
            x=[math.log(point["geometry"]["tf_m"]),math.log(point["geometry"]["tc_m"])]
            x += [math.log(s["factor"]) if n==s["property"] else 0. for n in names]
            starts.append(x)
    if not starts:
        return {"status":"no feasible single-property seed","factor_product":None}
    starts += [[math.log(base["geometry"]["tf_m"]),math.log(base["geometry"]["tc_m"])]+
               [min(math.log(1.2),b[1]) for b in bounds[2:]]]

    def evaluate(x):
        facts={n:math.exp(z) for n,z in zip(names,x[2:])}
        payload,modes=p2(r,weather,math.exp(x[0]),math.exp(x[1]),facts,basis,maturity)
        return np.array([float(payload)/(L10*(r/10)**3)]+
                        [math.log(max(float(v),1e-30)) for v in modes.values()])
    candidates=[]
    for seed in starts:
        fit=minimize(lambda x: sum(x[2:]),seed,method="SLSQP",bounds=bounds,
                     constraints={"type":"ineq","fun":evaluate},
                     options={"ftol":2e-11,"maxiter":450})
        c=evaluate(fit.x)
        if np.min(c) >= -2e-7:
            facts={n:math.exp(z) for n,z in zip(names,fit.x[2:])}
            point=p2_opt(r,weather,facts,basis,maturity,n=500)
            if point is not None and point["payload_kg"] >= -.03:
                candidates.append({"factor_product":math.exp(sum(fit.x[2:])),
                                   "factors":facts,"solution":point,
                                   "optimizer_success":bool(fit.success),
                                   "min_constraint":float(c.min())})
    # The exactly bracketed single-property points remain valid candidates.
    for s in singles:
        if s.get("factor") and s.get("solution") and s["solution"]["payload_kg"] >= -.03:
            candidates.append({"factor_product":s["factor"],
                               "factors":{s["property"]:s["factor"]},
                               "solution":s["solution"],"optimizer_success":True})
    if not candidates:
        return {"status":"no verified candidate","factor_product":None}
    best=min(candidates,key=lambda x:x["factor_product"])
    best["status"]="best feasible product found; numerical, not proof of global optimum"
    best["starts"]=len(starts)
    best["feasible_candidates"]=len(candidates)
    return best


def p3(r, weather, factors=None, maturity="concept", cavity=True):
    f=factors or {}
    row=next(x for x in P3DATA["rows"] if x["R_m"]==r and x["weather"]==weather
             and x["service"]=="ground")
    point=row["all_axes_endpoint"]
    bill=dict(point["bill_kg"])
    fstrength=point["film_effective_strength_Pa"]*f.get("ply_strength",1.)
    retention=min(1.,point["ten_year_retention"]*f.get("retention",1.))
    p=point["applied_pressure_Pa"]
    gauge=p*(2.6159809746514977*r/10)/(fstrength*retention*.964012200518-90.501688129e6)
    area=4*math.pi*r*r
    membrane_factor=f.get("film_mass",1.)
    bill["PBO_two_plies"]=area*gauge*1560/membrane_factor
    bill["barrier_and_protection"]/=membrane_factor
    bill["nodes"]/=f.get("node_mass",1.)
    # The full-member strength endpoint is already above the active local-shell
    # requirement; an increase cannot reduce the minimum section in this family.
    vac=point["vacuum"]
    gas_extra=0.
    cavity_data=None
    if cavity:
        barrier_delta=.002*area/membrane_factor
        S0=vac["initial_material_release_water_proxy_kg"]
        S0 += .1*.006*(bill["PBO_two_plies"]-point["bill_kg"]["PBO_two_plies"])
        # Preserve unmodelled protection outgassing when reducing its mass:
        # favorable omission of that reduction is conservative by a small amount.
        S0 += .001*barrier_delta
        incoming=7*(.08*area/1000+
                    (vac["water_external_upper_kg_day"]-area/1000))
        release=S0*(-math.expm1(-7))
        def residual(bed):
            hardware=5+max(1,.25*bed)
            return .06*bed-1.1*(incoming+release+.001*hardware*(-math.expm1(-7)))
        bed=brentq(residual,0.,1e6)
        hardware=5+max(1,.25*bed)
        capture=bed+hardware+.5*24*7/108
        retained=vac["initial_gas_kg"]+7*vac["dry_external_kg_day"]+incoming+.01*bed
        gas_extra=max(0.,retained-bill["gas"])
        bill["gas"]+=gas_extra
        bill["cavity_barrier_delta"]=barrier_delta
        bill["cavity_capture"]=capture-.5*24*7/108
        bill["cavity_battery"]=.5*24*7/108
        cavity_data={"days":7,"route":"SIOX/3A","WVTR_g_m2_day":.08,
                     "net_capacity_kg_kg":.06,"bed_dry_kg":bed,"capture_system_kg":capture,
                     "barrier_delta_kg":barrier_delta,"retained_external_water_kg":incoming,
                     "reserve_extra_kg":gas_extra,"extrapolated_beyond_054":r>15}
    extra=growth(bill,"P3",maturity,sleeves=point["joint_actual_sleeves_kg"])
    payload=point["lift_kg"]-sum(bill.values())-sum(extra.values())
    return {"R_m":r,"weather":weather,"maturity":maturity,"tag":"PROJECTION",
            "payload_kg":payload,"bill_kg":bill,"growth_kg":extra,
            "mass_before_growth_kg":sum(bill.values()),"growth_total_kg":sum(extra.values()),
            "lift_kg":point["lift_kg"],"factors":f,"cavity":cavity_data,
            "section_area_m2":point["section_area_m2"],"gyration_m":point["gyration_m"],
            "film_total_m":gauge,"effective_ply_strength_Pa":fstrength,
            "retention":retention,"required_SiC_strength_Pa":point["required_SiC_strength_Pa"],
            "SiC_strength_target_Pa":point["assumed_SiC_strength_Pa"]*f.get("SiC_strength",1.),
            "next_mode":"local tube-shell compression at constant g/R",
            "qualified_hull_SF":None}
