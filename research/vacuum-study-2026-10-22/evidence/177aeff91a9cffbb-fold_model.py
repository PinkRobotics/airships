#!/usr/bin/env python3
"""040: one pinned P2 grade, geometry optimization, explicit bill and load cases.

The six 033 shell equations and 028 joining equations are retained. Thermal
and gas equations are independently implemented from 037 and 034.
"""
import json
import math
from dataclasses import dataclass, replace, asdict
from pathlib import Path
from functools import lru_cache
import numpy as np
from scipy.optimize import minimize_scalar, brentq

B = Path('unpublished-local-ref:83b9d73c8c812fc2')
I = json.loads((B/"INPUTS.json").read_text())
C = I["core"]
F = I["face"]
P0 = I["case"]["p0_Pa"]
L0 = I["case"]["lift0_kg"]
T0 = I["case"]["T0_K"]
RHOAIR = L0/(4*np.pi*10**3/3)
BETA = brentq(lambda x: x**3+x-1, 0, 1)
THERMAL = json.loads((B/"THERMAL-TABLE.json").read_text())
ATMOS = json.loads((B/"inputs/031/ATMOSPHERE.json").read_text())
NAMES = I["axes"]
RU = 8.31446261815324
SPEC = json.loads((B/"inputs/034/INPUTS.json").read_text())["species"]
DRY_M = sum(s["dry_x"]*s["M_kg_mol"] for s in SPEC.values())/sum(s["dry_x"] for s in SPEC.values())


def dump(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2, allow_nan=False)+"\n")


@dataclass(frozen=True)
class Settings:
    weather: str = "ISA"
    floor: bool = True
    pad: str = "heavy70"
    vented: bool = True
    coating: float = .20
    thermal: bool = True
    cure_fraction: float = 1.
    pressure_factor_floor: float = 1.01
    nu: float = .0768
    wind: str = "envelope"
    systems: float = 100.
    charge_joining: bool = True
    water: bool = True
    contamination: bool = True
    gas: bool = True
    weather_pressure: bool = True
    extra_service: float = 0.
    legacy_climate: bool = False
    thermal_modulus_Pa: float | None = None
    bond_model: str = "compliant037b"
    cure_temperature_K: float = 366.4833333333333
    scarf_ratio: float = 30.34139731914874

    edge_scarf_interaction: bool = False
    cure_in_global: bool = False
    finish_id: str = "reference040"
    external_water_kg_m2: float = .1
    structural_primer_kg_m2: float = 0.
    moisture_scale: float = 0.
    adhesive_water_fraction: float = .002
    core_water_fraction: float = .001
    primer_water_fraction: float = .01
    finish_water_kg_m2: float = 0.
    desiccant: bool = False
    desiccant_capacity_kg_kg: float = .10
    desiccant_capture_fraction: float = .95



def weather_basis(weather):
    if weather == "ISA":
        return 0., 1., 500.
    envelope = "optimistic" if weather == "optimistic" else "all_019"
    candidates = [x for x in ATMOS["floors"] if x["envelope"] == envelope
                  and x["profile"] == "lapse_mixing" and x["altitude_floor_m"] == 100]
    assert len(candidates) == 1, (weather, [x["envelope"] for x in ATMOS["floors"]])
    x = candidates[0]
    return x["C_fraction"], x["nominal_required_SF"], x["ISA_float_m"]


def coefficients(mask, u):
    uses = [u]*4 if np.ndim(u) == 0 else u
    us = uses[2] if mask & 4 else 0.
    return (F["E_today_Pa"]*(F["E_full_Pa"]/F["E_today_Pa"])**us,
            F["strength_today_Pa"]*(F["strength_full_Pa"]/F["strength_today_Pa"])**us,
            .33*(.82/.33)**(uses[1] if mask & 2 else 0.),
            I["film"]["baseline_kg_m2_interface"]*2**(-(uses[3] if mask & 8 else 0.)))


def thermal_values(r, tc):
    table = THERMAL[str(int(r))]
    grid = np.log(table["tc_m"])
    return [1.002*np.interp(np.log(tc), grid, table[k]) for k in
            ["gradient_K", "swing_K", "curvature_temperature_K", "rise_K"]]


def thermal_extremes(r, tc):
    table=THERMAL[str(int(r))]
    grid=np.log(table["tc_m"])
    return [np.interp(np.log(tc),grid,table[k]) for k in ["max_outer_K","min_outer_K"]]


def pressure(r, s, wind=None):
    cf, qweather, _ = weather_basis(s.weather)
    # Ground/moored wind conservatively uses ISA density even when free flight
    # in a weather-reserved vehicle occurs at lower density.
    q70 = .5*RHOAIR*(70*1852/3600)**2
    # 037 reports the gust increment. A complete gust load case also carries
    # the steady 35-knot dynamic pressure.
    qgust = .5*RHOAIR*((35*1852/3600)+(35*.3048))**2
    selected = wind or s.wind
    q = {"envelope": max(q70, qgust), "70kn": q70, "gust35": qgust, "none": 0.}[selected]
    factor = max(s.pressure_factor_floor, qweather if s.weather_pressure else 1.)
    return P0*factor+q, q, factor


def mechanical(r, tf, tc, mask, u, s):
    E, strength, Q, film = coefficients(mask, u)
    p, _, _ = pressure(r, s)
    h = tf+tc
    stress = p*r/(4*tf)
    sig0 = E*h/(r*np.sqrt(1-s.nu**2))
    sigcr = C["Gc_Pa"]*h*h/(2*tf*tc)
    vc = sig0/sigcr
    kc = np.where(vc <= 2, 1-vc/4, 1/vc)
    g0 = np.where(vc < 2, .2, 1.)
    gfull = .2+.4*np.minimum(vc, 2)
    ug = u if np.ndim(u) == 0 else u[0]
    gamma = g0*(gfull/g0)**(ug if mask & 1 else 0.)
    if s.thermal:
        grad, swing, kt, rise = thermal_values(r, tc)
        Et = E if s.thermal_modulus_Pa is None else s.thermal_modulus_Pa
        gradient = Et*11.3e-6*grad/(2*(1-s.nu))
        bend = Et/(1-s.nu**2)*h/2*11.3e-6/r*kt
        if s.bond_model == "rigid037":
            tau = (23.6e-6-11.3e-6)*swing*s.cure_fraction*np.sqrt(Et*tf*C["Gc_Pa"]/tc)
            residual=np.zeros_like(tf+tc)
            wall_sf=np.full_like(tf+tc,1e30)
            shear_allow=C["shear_strength_W_Pa"]
        else:
            hot,cold=thermal_extremes(r,tc)
            dt=1.002*np.maximum(abs(s.cure_temperature_K-hot),abs(s.cure_temperature_K-cold))
            comp_dt=1.002*np.maximum(s.cure_temperature_K-cold,0.)
            deps=(23.6e-6-11.3e-6)*dt
            kb=.5*67e9*C["rho"]/2700
            tau=deps*np.sqrt(2*kb*C["Gc_Pa"])
            residual=kb*(23.6e-6-11.3e-6)*comp_dt*tc/(2*tf)
            wall_sf=227.53e6/np.maximum(1.2*67e9*deps,1e-30)
            shear_allow=25*6894.757293168361
    else:
        gradient = bend = tau = np.zeros_like(tf+tc)
        residual=np.zeros_like(tf+tc)
        wall_sf=np.full_like(tf+tc,1e30)
        shear_allow=C["shear_strength_W_Pa"]
    demand = stress+gradient+bend+residual
    crimp_demand=stress+gradient+bend+(residual if s.cure_in_global else 0.)
    global_demand=stress+(residual if s.cure_in_global else 0.)
    # The thermal interface shear and mean scarf shear are added in the worst
    # scalar direction. This is an explicit interaction screen, not a joint law.
    ratio=s.scarf_ratio
    scarf = demand*ratio/(1+ratio**2)
    if s.bond_model=="rigid037" or s.edge_scarf_interaction:
        scarf=scarf+tau
    shape = np.broadcast(tf, tc).shape
    modes = dict(global_buckling=gamma*kc*sig0/global_demand,
                 face_compression=strength/demand,
                 core_shear_crimping=sigcr/crimp_demand,
                 core_crush=np.full(shape, 2*C["crush_Pa"]/p),
                 face_wrinkling=BETA*Q*np.sqrt(E*C["Ec_Pa"]*tf/tc)/demand,
                 intracell_dimpling=E*(tf/C["s_cell_m"])**2/((1-s.nu**2)*demand),
                 scarf_average_shear_screen=10e6/scarf,
                 core_cell_wall_yield_screen=wall_sf)
    thermal_sf = shear_allow/np.maximum(tau, 1e-30)
    return modes, thermal_sf, dict(E_Pa=E, Fcy_Pa=strength, Q=Q, film_kg_m2_interface=film,
                                  gamma=gamma, gamma_full=gfull, Vc=vc,
                                  pressure_face_stress_Pa=stress,
                                  added_gradient_stress_Pa=gradient, added_bending_stress_Pa=bend,
                                  added_cure_compression_Pa=residual,
                                  thermal_interface_shear_Pa=tau, thermal_shear_allowable_Pa=shear_allow,
                                  scarf_shear_Pa=scarf, global_compressive_demand_Pa=global_demand,
                                  crimp_compressive_demand_Pa=crimp_demand)


def joining(r, tf, tc, film, s=None):
    area = 4*np.pi*r*r
    ratio=I["joining"]["scarf_ratio"] if s is None else s.scarf_ratio
    length = area*(1/(.6096-ratio*tf)+1/(1.8288-ratio*tf))
    out = dict(film=2*area*film,
               scarf=length*2*tf*np.sqrt(1+ratio**2)*.07,
               splice=length*.0005*tc*500,
               seal=length*.002)
    out["total"] = sum(out.values())
    out["length_m"] = length
    return out


@lru_cache(None)
def pad(r, choice):
    if choice == "none":
        return dict(mass_kg=0., SF_70kn=None, area_m2=0., thickness_m=0., force_N=0.)
    q70 = .5*RHOAIR*(70*1852/3600)**2
    f70 = .47*q70*np.pi*r*r
    force = f70 if choice == "heavy70" else 1.4*.47*.5*RHOAIR*20**2*np.pi*r*r
    area = force/C["crush_Pa"]
    radius = np.sqrt(area/np.pi)
    thickness = np.sqrt(3*1.33*force*np.log(radius/.025)/(2*np.pi*276e6))
    return dict(mass_kg=float(area*thickness*2700), SF_70kn=float(force/f70),
                area_m2=float(area), thickness_m=float(thickness), force_N=float(force))


def material_water(r, tc, joint, s):
    area = 4*np.pi*r*r
    # Extra water relative to the nominal structural/finish bill. Historical
    # WVR is a proxy, not an equilibrium isotherm for the 200 F cured assembly.
    by_material = dict(
        AF163_2U=s.adhesive_water_fraction*joint["film"],
        coated_5056_core=s.core_water_fraction*area*tc*C["rho"],
        structural_primer=s.primer_water_fraction*area*s.structural_primer_kg_m2,
        finish=area*s.finish_water_kg_m2,
        seam_polymers=.01*(joint["scarf"]+joint["splice"]+joint["seal"]))
    return {k: v*s.moisture_scale for k,v in by_material.items()}


def drying_bill(r, tc, joint, s):
    area = 4*np.pi*r*r
    water = sum(material_water(r, tc, joint, s).values())
    # Original 040 release inventory remains in the nominal material masses.
    # No TML mass is credited as water removal. It is a separate pressure bound.
    nominal_volatiles = (.0485*joint["film"]+.001*area*tc*C["rho"]
                         +.01*(joint["scarf"]+joint["splice"]+joint["seal"]))*0.1
    capacity = 1.1*(water+nominal_volatiles)+.1*(r/10)**3
    dry_bed = capacity/s.desiccant_capacity_kg_kg if s.desiccant else np.zeros_like(tc)
    cartridge = 2. if s.desiccant else 0.
    return dict(absorbed_water=water,
                structural_primer=area*s.structural_primer_kg_m2,
                desiccant=dry_bed+cartridge)

def vacuum(r, tf, tc, joint, s):
    area = 4*np.pi*r*r
    volume = 4*np.pi*r**3/3
    # Same nominal sphere/midsurface volume convention as 033. Exact mouldline
    # and wall displacement remain an explicit geometry NFI.
    pore = area*tc*(1-C["rho"]/2700)
    trapped = np.zeros_like(tc) if s.vented else RHOAIR*pore
    initial = 10*volume/(RU*T0)*DRY_M
    e = 6000. if s.weather == "both" else 1000.
    water_x = e/P0
    molmass = (1-water_x)*DRY_M+water_x*.01801528
    leak_mol = (joint["length_m"]*.001+.01)*.1/(RU*T0)*86400
    # Upper bound ignoring backpressure; P2 intact metallic faces do not expose
    # the full film area to atmosphere.
    area_path = joint["length_m"]*(.07/1250)/(tf*np.sqrt(1+s.scarf_ratio**2))
    perm_mol = 10*3.34645e-16*area_path*P0*86400
    ingress = (leak_mol+perm_mol)*molmass
    inventory = (.0485*joint["film"]+.001*area*tc*C["rho"]
                 +.01*(joint["scarf"]+joint["splice"]+joint["seal"]))*0.1
    extra_water = sum(material_water(r, tc, joint, s).values())
    released_nominal = inventory*(1-np.exp(-1))
    released_extra_water = extra_water*(1-np.exp(-1))
    capture = s.desiccant_capture_fraction if s.desiccant else 0.
    released = (released_nominal+released_extra_water)*(1-capture)
    # Desorption is material already aboard: it is charged to pressure, not
    # added a second time to vehicle mass.
    gas_aboard = initial+trapped+ingress
    # Keep all gas and incoming mass on board even if water is adsorbed.
    # Only its water partial pressure receives the explicit capture scenario.
    dry_ingress_mol = (leak_mol+perm_mol)*(1-water_x*capture)
    hotpressure = (initial/DRY_M+dry_ingress_mol+released/.01801528)*RU*320/volume
    lateventpressure = hotpressure+trapped/DRY_M*RU*320/volume
    charged = np.maximum(.01*L0*(r/10)**3, gas_aboard) if s.gas else np.zeros_like(tc)
    return dict(pore_volume_m3=pore, trapped_air_kg=trapped,
                tube_bore_volume_m3=np.zeros_like(tc), initial_gas_kg=initial,
                external_ingress_24h_upper_kg=ingress, desorbed_24h_kg=released,
                added_material_water_kg=extra_water,
                original_nominal_volatile_release_kg=released_nominal,
                desiccant_water_capacity_kg=(1.1*(inventory+extra_water)+.1*(r/10)**3) if s.desiccant else 0.,
                desiccant_capture_fraction=capture,
                gas_aboard_counted_kg=gas_aboard, charged_gas_kg=charged,
                hot_pressure_24h_upper_Pa=hotpressure,
                hot_pressure_after_late_vent_upper_Pa=lateventpressure,
                pressure_limit_Pa=.01*P0,
                pressure_SF=.01*P0/hotpressure,
                late_vent_pressure_SF=.01*P0/lateventpressure,
                service_hardware_band_kg=[30., 50.], service_extra_charge_kg=s.extra_service,
                battery_required_24h_kg=5*24/(150*.8*.9))


def payload_at(r, tf, tc, mask, u, s, detail=False):
    area = 4*np.pi*r*r
    lift = L0*(r/10)**3
    E, strength, Q, film = coefficients(mask, u)
    joint = joining(r, tf, tc, film, s)
    faces, core = 2*area*1850*tf, area*C["rho"]*tc
    structural = faces+core
    charged_joining = np.maximum(joint["total"], .05*structural) if s.floor else joint["total"]
    if not s.charge_joining:
        charged_joining = np.zeros_like(structural)
    vac = vacuum(r, tf, tc, joint, s)
    cf, _, _ = weather_basis(s.weather)
    climate = lift*cf
    if s.legacy_climate:
        climate = lift*((1-.99*T0/(T0+10))+.378*1000/P0*T0/(T0+10))
    bill = dict(faces=faces, core=core, charged_joining=charged_joining,
                coating=area*s.coating, mooring_pad=pad(r, s.pad)["mass_kg"],
                gas=vac["charged_gas_kg"], systems=s.systems, extra_service=s.extra_service,
                water=area*s.external_water_kg_m2 if s.water else 0.,
                contamination=area*5/(400*np.pi) if s.contamination else 0.,
                weather_headroom=climate)
    bill.update(drying_bill(r, tc, joint, s))
    payload = lift-sum(bill.values())
    if not detail:
        return payload
    modes, thermalsf, props = mechanical(r, tf, tc, mask, u, s)
    loadcases = {}
    for name in ["70kn", "gust35"]:
        ms, th, _ = mechanical(r, tf, tc, mask, u, replace(s, wind=name))
        loadcases[name] = {k: float(v) for k,v in ms.items()}
        loadcases[name]["thermal_core_interface_screen"] = float(th)
    scalar = lambda d: {k: (v if isinstance(v, (str, list, bool)) else float(v)) for k,v in d.items()}
    modes = scalar(modes)
    modes["thermal_core_interface_screen"] = float(thermalsf)
    modeled = min(modes.values())
    pressure_ok = float(vac["pressure_SF"]) >= 1-1e-7
    return dict(tag="QUESTIONABLE / PROJECTION", R_m=r, settings=asdict(s), mask=mask,
                selected_axes=[name for j,name in enumerate(NAMES) if mask & (1 << j)], usage=u,
                geometry=dict(tf_m=float(tf), tc_m=float(tc), area_m2=area,
                              volume_m3=4*np.pi*r**3/3, core=C["name"]),
                properties=scalar(props), load_pressure_Pa=pressure(r,s)[0],
                modes=modes, loadcases=loadcases, least_shell_and_thermal_SF=modeled,
                pad=pad(r,s.pad), vacuum=scalar(vac), actual_joining=scalar(joint),
                floor_allowance_kg=float(.05*structural if s.floor else 0.),
                bill_kg=scalar(bill), lift_kg=lift, signed_payload_kg=float(payload),
                shell_and_thermal_pass=modeled >= 1-2e-7, service_pressure_pass=bool(pressure_ok),
                modeled_assembly_pass=bool(modeled >= 1-2e-7 and pressure_ok
                                          and s.pad == "heavy70" and s.vented and payload >= -.01),
                overall_installed_hull_SF=None)


def geometry_at_tc(r, tc, mask, u, s):
    tc = np.atleast_1d(tc)
    lo = np.full_like(tc, 1e-6)
    hi = np.full_like(tc, min(.0195, .008*r/10))
    def minimum(tf):
        modes, _, _ = mechanical(r, tf, tc, mask, u, s)
        return np.minimum.reduce(list(modes.values()))
    upper_good = minimum(hi) >= 1
    for _ in range(44):
        mid = (lo+hi)/2
        good = minimum(mid) >= 1
        hi = np.where(good, mid, hi)
        lo = np.where(good, lo, mid)
    tf = hi*(1+3e-12)
    modes, thermalsf, props = mechanical(r, tf, tc, mask, u, s)
    feasible = upper_good & (thermalsf >= 1-2e-10)
    value = payload_at(r, tf, tc, mask, u, s)
    # Service pressure is an independent performance condition. The additional
    # late-vent calculation is a counterfactual for sealed cells, not a second
    # charge or a claim that their pressure load path has been qualified.
    joint = joining(r, tf, tc, coefficients(mask,u)[3],s)
    vac = vacuum(r, tf, tc, joint, s)
    feasible &= vac["pressure_SF"] >= 1-2e-10
    return np.where(feasible, value, -np.inf), tf, thermalsf, vac["pressure_SF"]


def optimize(r, mask, u, s, n=440, detail=True):
    grid = np.geomspace(.0012*r/10, 1.4*r/10, n)
    vals, tfs, ths, vs = geometry_at_tc(r, grid, mask, u, s)
    valid = np.isfinite(vals)
    if not np.any(valid):
        return None
    trials = [(float(vals[j]), float(grid[j])) for j in [int(np.argmax(vals))]]
    peaks = np.where(valid[1:-1] & (vals[1:-1] >= vals[:-2]) & (vals[1:-1] >= vals[2:]))[0]+1
    def value(tc):
        return float(geometry_at_tc(r, np.array([tc]), mask, u, s)[0][0])
    for j in peaks:
        opt = minimize_scalar(lambda t: min(1e30, -value(t)), bounds=(grid[j-1], grid[j+1]),
                              method="bounded", options={"xatol": 2e-11})
        if np.isfinite(opt.fun):
            trials.append((-float(opt.fun), float(opt.x)))
    # A thermal/service boundary may be the best point in a valid interval.
    for j in np.where(valid[:-1] != valid[1:])[0]:
        left, right = grid[j], grid[j+1]
        isleft = bool(valid[j])
        for _ in range(34):
            mid = (left+right)/2
            good = np.isfinite(value(mid))
            if good == isleft:
                left = mid
            else:
                right = mid
        t = left if isleft else right
        trials.append((value(t), t))
    best, tc = max(trials)
    if not detail:
        return best
    tf = float(geometry_at_tc(r, np.array([tc]), mask, u, s)[1][0])
    return payload_at(r, tf, tc, mask, u, s, True)


def least(r, s, n=440):
    endpoints = []
    feasible = []
    for mask in range(16):
        point = optimize(r, mask, 1. if mask else 0., s, n=n)
        endpoints.append(dict(mask=mask, axes=[name for j,name in enumerate(NAMES) if mask & (1 << j)],
                              payload_kg=None if point is None else point["signed_payload_kg"],
                              solution=point))
        if point is not None and point["signed_payload_kg"] >= 0:
            feasible.append(mask)
    if not feasible:
        return dict(status="no floating solution within stated endpoints",
                    minimum_axis_count=None, least=None, endpoint_trials=endpoints)
    count = min(m.bit_count() for m in feasible)
    candidates = []
    for mask in feasible:
        if mask.bit_count() != count:
            continue
        if mask == 0:
            point = optimize(r,0,0,s,n=n)
        else:
            def target(u):
                v = optimize(r,mask,u,s,n=n,detail=False)
                return -1e10 if v is None else v
            usage = brentq(target,0,1,xtol=2e-9)
            point = optimize(r,mask,min(1,usage+2e-9),s,n=n)
        candidates.append(point)
    chosen = min(candidates, key=lambda x: (x["usage"],x["mask"]))
    return dict(status="conditional modeled float" if s.vented and s.pad=="heavy70"
                else "shell/mass sensitivity only; assembly condition open or failed",
                minimum_axis_count=count, least=chosen, ties=candidates,
                endpoint_trials=endpoints)
