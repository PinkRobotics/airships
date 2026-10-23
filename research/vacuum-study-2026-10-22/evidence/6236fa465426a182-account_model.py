"""Independent algebraic reconstruction of the documented 040/048 account.

Thermal tables are explicit inputs here. Their independent boundary-condition
reconstruction is audited separately in thermal_check.py.
"""
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
BASE = json.loads((ROOT/"intake/base040/02/INPUTS.json").read_text())
THERMAL = json.loads((ROOT/"intake/owner/THERMAL-TABLES.json").read_text())
SERVICE = json.loads((ROOT/"intake/base040/07/INPUTS.json").read_text())
ATMOS = json.loads((ROOT/"intake/base040/06/ATMOSPHERE.json").read_text())
P0 = BASE["case"]["p0_Pa"]
LIFT0 = BASE["case"]["lift0_kg"]
TA = 284.9
RHO = 1.1672683307461802
RU = SERVICE["constants"]["R_universal_J_mol_K"]
CORE = BASE["core"]
GC, EC, RC = CORE["Gc_Pa"], CORE["Ec_Pa"], CORE["rho"]
BETA = brentq(lambda b:b**3+b-1, 0, 1)
AB, AA = 11.3e-6, 23.6e-6
KB = .5*67e9*RC/2700
W_MIN = BASE["bond_fix_037b"]["W_minimum_strength_Pa"]
AXES = BASE["axes"]
CLIMATE = {"ISA": (0., 1.)}
for key, name in [("optimistic", "optimistic"), ("both", "conservative")]:
    row = next(x for x in ATMOS["floors"] if x["envelope"] == name
               and x["profile"] == "lapse_mixing" and x["altitude_floor_m"] == 100)
    CLIMATE[key] = (row["C_kg"], row["nominal_required_SF"])


def properties(mask, usage):
    u = np.full(4, usage) if np.ndim(usage) == 0 else np.asarray(usage)
    u = u*np.asarray([(mask >> i) & 1 for i in range(4)])
    return dict(E=290e9*(293.6/290)**u[2], Fcy=345e6*(379.2/345)**u[2],
                Q=.33*(.82/.33)**u[1], film=BASE["film"]["baseline_kg_m2_interface"]*.5**u[3],
                gamma_usage=u[0], axis_usage=u)


def thermal_values(radius, tc, settings, override=None):
    tab = THERMAL[settings.get("finish_id", "reference040")][str(int(radius))] if override is None else override
    x = np.log(np.asarray(tab["tc_m"]))
    logtc = np.log(tc)
    return {key: np.interp(logtc, x, tab[key]) for key in
            ("gradient_K", "curvature_temperature_K", "max_outer_K", "min_outer_K", "swing_K", "rise_K")}


def wind_pressures():
    return {"70kn": .5*RHO*(70*1852/3600)**2,
            "gust35": .5*RHO*(35*1852/3600+35*.3048)**2}


def mechanical(radius, tf, tc, mask, usage, settings, tab=None, wind=None):
    tf, tc = np.asarray(tf), np.asarray(tc)
    p = properties(mask, usage)
    e, nu = p["E"], settings.get("nu", .0768)
    et = settings.get("thermal_modulus_Pa") or e
    climate, qp = CLIMATE[settings["weather"]]
    factor = max(settings.get("pressure_factor_floor", 1.01), qp) if settings.get("weather_pressure", True) else settings.get("pressure_factor_floor", 1.01)
    winds = wind_pressures()
    wp = winds[wind] if wind else max(winds.values()) if settings.get("wind", "envelope") != "none" else 0.
    pressure = P0*factor+wp
    t = thermal_values(radius, tc, settings, tab)
    thermal_on = settings.get("thermal", True)
    thermal_factor = 1.002 if thermal_on else 0.
    gradient = thermal_factor*et*AB*t["gradient_K"]/(2*(1-nu))
    curvature = thermal_factor*et*(tf+tc)*AB*t["curvature_temperature_K"]/(2*radius*(1-nu**2))
    cure = settings.get("cure_temperature_K", 366.4833333333333)
    cure_fraction = settings.get("cure_fraction", 1.)
    mismatch = thermal_factor*cure_fraction*(AA-AB)*np.maximum(np.abs(cure-t["min_outer_K"]),
                                                              np.abs(cure-t["max_outer_K"]))
    edge = mismatch*math.sqrt(2*KB*GC)
    balanced = thermal_factor*cure_fraction*KB*(AA-AB)*np.maximum(cure-t["min_outer_K"], 0)*tc/(2*tf)
    wall = 1.2*67e9*mismatch
    axial = pressure*radius/(4*tf)
    sigma0 = e*(tf+tc)/(radius*math.sqrt(1-nu**2))
    sigmacr = GC*(tf+tc)**2/(2*tf*tc)
    vc = sigma0/sigmacr
    kc = np.where(vc<=2, 1-vc/4, 1/vc)
    g0 = np.where(vc<2, .2, 1.)
    gfull = .2+.4*np.minimum(vc, 2.)
    gamma = g0*(gfull/g0)**p["gamma_usage"]
    st = axial+gradient+curvature
    demand = st+balanced
    scarf_ratio = settings.get("scarf_ratio", BASE["joining"]["scarf_ratio"])
    scarf = demand*scarf_ratio/(1+scarf_ratio**2)
    if settings.get("edge_scarf_interaction"):
        scarf = scarf+edge
    modes = dict(
        global_buckling=gamma*kc*sigma0/(axial+balanced if settings.get("cure_in_global") else axial),
        face_compression=p["Fcy"]/demand,
        core_shear_crimping=sigmacr/(st+balanced if settings.get("cure_in_global") else st),
        core_crush=np.broadcast_to(2*CORE["crush_Pa"]/pressure, np.shape(demand)),
        face_wrinkling=BETA*p["Q"]*np.sqrt(e*EC*tf/tc)/demand,
        intracell_dimpling=e*(tf/CORE["s_cell_m"])**2/((1-nu**2)*demand),
        scarf_average_shear_screen=10e6/scarf,
        core_cell_wall_yield_screen=BASE["bond_fix_037b"]["foil_yield_proxy_Pa"]/np.maximum(wall, 1e-300),
        thermal_core_interface_screen=W_MIN/np.maximum(edge, 1e-300),
    )
    props = dict(E_Pa=e, Fcy_Pa=p["Fcy"], Q=p["Q"],
                 film_kg_m2_interface=p["film"], gamma=gamma, gamma_full=gfull, Vc=vc,
                 pressure_face_stress_Pa=axial, added_gradient_stress_Pa=gradient,
                 added_bending_stress_Pa=curvature, added_cure_compression_Pa=balanced,
                 thermal_interface_shear_Pa=edge, thermal_shear_allowable_Pa=W_MIN,
                 scarf_shear_Pa=scarf)
    return props, modes, pressure, t


def joining(radius, tf, tc, film, settings):
    area = 4*math.pi*radius**2
    ratio = settings.get("scarf_ratio", BASE["joining"]["scarf_ratio"])
    width, length = .6096-ratio*tf, 1.8288-ratio*tf
    seam = area*(1/width+1/length)
    masses = dict(film=2*area*film,
                  scarf=seam*2*tf*math.sqrt(1+ratio**2)*.07,
                  splice=seam*.0005*tc*500, seal=seam*.002)
    return dict(**masses, total=sum(masses.values()), length_m=seam)


def pad(radius, settings):
    wind = wind_pressures()
    force = .47*wind["70kn"]*math.pi*radius**2
    if settings.get("pad") == "light20":
        force = 1.4*.47*(.5*RHO*20**2)*math.pi*radius**2
    area = force/CORE["crush_Pa"]
    disc_radius = math.sqrt(area/math.pi)
    thickness = math.sqrt(3*(1+.33)*force*math.log(disc_radius/.025)/(2*math.pi*276e6))
    return dict(mass_kg=area*thickness*2700,
                SF_70kn=force/(.47*wind["70kn"]*math.pi*radius**2),
                area_m2=area, thickness_m=thickness, force_N=force)


def water_inventory(area, core_mass, join, settings):
    primer = area*settings.get("structural_primer_kg_m2", .01)
    initial = dict(
        AF163_2U=settings.get("adhesive_water_fraction", .002)*join["film"],
        coated_5056_core=settings.get("core_water_fraction", .001)*core_mass,
        structural_primer=settings.get("primer_water_fraction", .01)*primer,
        finish=area*settings.get("finish_water_kg_m2", 0.),
        seam_polymers=.01*(join["scarf"]+join["splice"]+join["seal"]),
    )
    nominal = .1*(.0485*join["film"]+.001*core_mass+
                  .01*(join["scarf"]+join["splice"]+join["seal"]))
    remaining = {k:v*settings.get("moisture_scale", 1.) for k,v in initial.items()}
    return initial, remaining, nominal


def vacuum(radius, tf, tc, join, initial_water, remaining_water, nominal, settings):
    area, volume = 4*math.pi*radius**2, 4*math.pi/3*radius**3
    pore = area*tc*(1-RC/2700)
    trapped = 0. if settings.get("vented", True) else pore*RHO
    dry = SERVICE["species"]
    norm = sum(x["dry_x"] for x in dry.values())
    ewater = 6000 if settings["weather"] == "both" else 1000
    xw = ewater/P0
    mdry = sum(x["dry_x"]*x["M_kg_mol"] for x in dry.values())/norm
    initial_gas = 10*volume*mdry/(RU*TA)
    mean_mass = mdry*(1-xw)+.01801528*xw
    leak_moles = .1*(.001*join["length_m"]+.01)*86400/(RU*TA)
    ratio = settings.get("scarf_ratio", BASE["joining"]["scarf_ratio"])
    path = tf*math.sqrt(1+ratio**2)
    permeation_moles = 10*3.34645e-16*join["length_m"]*(.07/1250)/path*P0*86400
    ingress_moles = leak_moles+permeation_moles
    ingress = ingress_moles*mean_mass
    release = -math.expm1(-1)
    nominal_release = nominal*release
    desorbed = (nominal+remaining_water)*release
    capacity = 1.1*(initial_water+nominal)+.1*(radius/10)**3 if settings.get("desiccant") else 0.
    capture_fraction = settings.get("desiccant_capture_fraction", .95) if settings.get("desiccant") else 0.
    captured = min(capacity, capture_fraction*(desorbed+ingress_moles*xw*.01801528))
    nmol = 10*volume/(RU*TA)+ingress_moles+(desorbed-captured)/.01801528
    pressure = nmol*RU*320/volume
    late = pressure+trapped/RHO*P0/TA*320/volume
    gas_counted = initial_gas+ingress+trapped
    return dict(
        pore_volume_m3=pore, trapped_air_kg=trapped, tube_bore_volume_m3=0.,
        initial_gas_kg=initial_gas, external_ingress_24h_upper_kg=ingress,
        desorbed_24h_kg=desorbed-min(capacity,capture_fraction*desorbed),
        added_material_water_kg=remaining_water,
        original_nominal_volatile_release_kg=nominal_release,
        desiccant_water_capacity_kg=capacity, desiccant_capture_fraction=capture_fraction,
        gas_aboard_counted_kg=gas_counted,
        charged_gas_kg=max(.01*LIFT0*(radius/10)**3, gas_counted),
        hot_pressure_24h_upper_Pa=pressure, hot_pressure_after_late_vent_upper_Pa=late,
        pressure_limit_Pa=.01*P0, pressure_SF=.01*P0/pressure,
        late_vent_pressure_SF=.01*P0/late,
        service_hardware_band_kg=[30., 50.],
        service_extra_charge_kg=settings.get("extra_service", 0.),
        battery_required_24h_kg=5*24/(150*.8*.9),
    )


def evaluate(radius, tf, tc, mask, usage, settings, tab=None):
    props, modes, pressure, temperatures = mechanical(radius, tf, tc, mask, usage, settings, tab)
    area, volume = 4*math.pi*radius**2, 4*math.pi/3*radius**3
    face_mass, core_mass = 2*area*tf*1850, area*tc*RC
    join = joining(radius, tf, tc, props["film_kg_m2_interface"], settings)
    water0, water1, nominal = water_inventory(area, core_mass, join, settings)
    vac = vacuum(radius, tf, tc, join, sum(water0.values()), sum(water1.values()), nominal, settings)
    pad_mass = pad(radius, settings)
    floor = .05*(face_mass+core_mass) if settings.get("floor") else 0.
    bill = dict(faces=face_mass, core=core_mass,
                charged_joining=max(join["total"],floor) if settings.get("charge_joining",True) else 0.,
                coating=area*settings["coating"], mooring_pad=pad_mass["mass_kg"],
                gas=vac["charged_gas_kg"] if settings.get("gas",True) else 0.,
                systems=settings.get("systems",100.), extra_service=settings.get("extra_service",0.),
                water=area*settings.get("external_water_kg_m2",.1) if settings.get("water",True) else 0.,
                contamination=5*(radius/10)**2 if settings.get("contamination",True) else 0.,
                weather_headroom=CLIMATE[settings["weather"]][0]*(radius/10)**3,
                absorbed_water=sum(water1.values()),
                structural_primer=area*settings.get("structural_primer_kg_m2",.01),
                desiccant=(vac["desiccant_water_capacity_kg"]/settings.get("desiccant_capacity_kg_kg",.1)+2)
                    if settings.get("desiccant") else 0.)
    least = min(float(x) for x in modes.values())
    lift = LIFT0*(radius/10)**3
    return dict(
        geometry=dict(tf_m=tf,tc_m=tc,area_m2=area,volume_m3=volume),
        properties=props, load_pressure_Pa=pressure,modes=modes,
        loadcases={name:mechanical(radius,tf,tc,mask,usage,settings,tab,wind=name)[1]
                   for name in ("70kn","gust35")},
        least_shell_and_thermal_SF=least,pad=pad_mass,vacuum=vac,
        actual_joining=join,floor_allowance_kg=floor,bill_kg=bill,
        lift_kg=lift,signed_payload_kg=lift-sum(bill.values()),
        material_water_initial_by_material_kg=water0,
        material_water_remaining_by_material_kg=water1,
        nominal_volatile_inventory_kg=nominal, temperatures=temperatures,
    )
