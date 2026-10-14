#!/usr/bin/env python3
"""One isolated-air arrangement; conditional hydrostatic/occupancy arithmetic.

Standard library only. No optimizer, native solver, file writes or vehicle trim.
The bottom-filled cap is a volume quadrature surrogate, NOT a membrane solution.
"""
import hashlib
import importlib.util
import json
from math import acos, ceil, cos, exp, factorial, log, pi, sin, sqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent / "R3-I013/calculate.py"
PRIOR_SHA = "a841d9584ce4f5bffc748d0c4138af813f12fc105c903e8dd85973e73b56d8dd"
BASELINE_SHA = "f9a75086e19bca892a6944d9351ca77e082d710afe8b86d5a2f460d8a9bca8fb"
assert hashlib.sha256(PRIOR.read_bytes()).hexdigest() == PRIOR_SHA
assert hashlib.sha256((HERE / "baseline.json").read_bytes()).hexdigest() == BASELINE_SHA
spec = importlib.util.spec_from_file_location("finite_support_i013", PRIOR)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
old, INV, GEO = prior.old, prior.INV, prior.GEO
BASELINE = json.loads((HERE / "baseline.json").read_text())
assert BASELINE["calculator_sha256"] == PRIOR_SHA
G, RA, RU = old.G, old.RA, old.RU
R, RB = prior.R, GEO["bag_radius_m"]
CENTRES, GUIDES = GEO["bag_centres"], prior.GUIDES
MGAS = INV["helium_kg"] + INV["impurity_air_kg"]
RMIX = INV["mol"] * RU / MGAS
REGIONS = {"U0": (0,), "L12": (1, 2), "U3": (3,)}
REGION_FOR = ("U0", "L12", "L12", "U3")
ZH = -R - 2.
HEADERS = {"U0": {"centre": (6., 6., ZH), "diameter_m": 1.1, "length_m": 4., "rating_m3_s": 8.},
           "L12": {"centre": (0., 0., ZH), "diameter_m": 1.5, "length_m": 12., "rating_m3_s": 16.},
           "U3": {"centre": (-6., -6., ZH), "diameter_m": 1.1, "length_m": 4., "rating_m3_s": 8.}}
STARTS = ((6., 6., ZH), (4., -4., ZH), (-4., 4., ZH), (-6., -6., ZH))
D = prior.BASE["pressure_system"]["duct_diameter_m"]
DUCT_AREA = pi * D**2 / 4
KF = 2e6
KBAND = 4*5e9*(.25*prior.BASE["bag_cradle_band_mm"]/1000)/(2*pi*RB)
FREE = BASELINE["bag_free_lengths_m"]
assert max(abs(a-b) for a,b in zip(FREE,prior.HANGER_FREE_LENGTHS)) < 1e-12


def gauss(n=24):
    result = []
    for i in range(1, n+1):
        x = cos(pi*(i-.25)/(n+.5))
        for _ in range(20):
            a, b = 1., x
            for j in range(2,n+1): a,b = b,((2*j-1)*x*b-(j-1)*a)/j
            derivative = n*(x*b-a)/(x*x-1)
            dx = b/derivative
            x -= dx
            if abs(dx)<2e-15: break
        else: raise ArithmeticError("quadrature node bound")
        result.append((x,2/((1-x*x)*derivative*derivative)))
    return result


QUAD = gauss()


def integrate(fun, a, b):
    return (b-a)/2 * sum(w*fun((a+b)/2+x*(b-a)/2) for x,w in QUAD) if b>a else 0.


def disk_overlap(r, t, d):
    if r <= 0 or d >= r+t: return 0.
    if d <= abs(r-t): return pi*min(r,t)**2
    u = max(-1.,min(1.,(d*d+r*r-t*t)/(2*d*r)))
    v = max(-1.,min(1.,(d*d+t*t-r*r)/(2*d*t)))
    return r*r*acos(u)+t*t*acos(v)-.5*sqrt(max(0.,(-d+r+t)*(d+r-t)*(d-r+t)*(d+r+t)))


def cuts(bag):
    centre = CENTRES[bag]
    zs = [centre[2]-RB, centre[2], centre[2]+RB]
    for guide in GUIDES:
        if guide["foreign_bag"] != bag: continue
        h = GEO["hangers"][guide["hanger"]]
        zs += [h["low"][2]+guide[k] for k in ("start_m","end_m")]
        d = sqrt(sum((h["low"][j]-centre[j])**2 for j in (0,1)))
        for radial in (abs(d-.12),d+.12):
            if radial<RB:
                zs += [centre[2]+s*sqrt(RB*RB-radial*radial) for s in (-1,1)]
    return sorted(set(z for z in zs if centre[2]-RB <= z <= centre[2]+RB))


CUTS = [cuts(b) for b in range(4)]


def cap_area(bag,z):
    c = CENTRES[bag]
    r = sqrt(max(0.,RB*RB-(z-c[2])**2))
    area = pi*r*r
    for guide in GUIDES:
        if guide["foreign_bag"] != bag: continue
        h = GEO["hangers"][guide["hanger"]]
        if h["low"][2]+guide["start_m"] <= z <= h["low"][2]+guide["end_m"]:
            d = sqrt(sum((h["low"][j]-c[j])**2 for j in (0,1)))
            area -= disk_overlap(r,.12,d)
    return max(0.,area)


def cap_weight(bag, top, k=0., moment=False):
    zs = [z for z in CUTS[bag] if z<top]+[top]
    return sum(integrate(lambda z: cap_area(bag,z)*exp(-k*z)*(z if moment else 1.),a,b)
               for a,b in zip(zs,zs[1:]))


CAPACITY = [cap_weight(b,CENTRES[b][2]+RB) for b in range(4)]


def fill_top(bag, volume):
    lo,hi = CENTRES[bag][2]-RB,CENTRES[bag][2]+RB
    assert 0 < volume < CAPACITY[bag]
    z = lo+(hi-lo)*volume/CAPACITY[bag]
    for _ in range(30):
        err = cap_weight(bag,z)-volume
        if abs(err)<2e-9: return z
        if err>0: hi=z
        else: lo=z
        slope=cap_area(bag,z)
        candidate=z-err/slope if slope>1e-12 else (lo+hi)/2
        z=candidate if lo<candidate<hi else (lo+hi)/2
    raise ArithmeticError("cap inversion bound")


def sphere_weight(radius,k):
    x=k*radius
    return 4*pi*radius**3/3*sum(6*(j+1)*x**(2*j)/factorial(2*j+3) for j in range(6))


def exp_average(z0,z1,k):
    # Stable analytic axial integral, with small exponent expansion.
    x=k*(z1-z0)/2
    return exp(-k*(z0+z1)/2)*sum(x**(2*j)/factorial(2*j+1) for j in range(6))


def duct_layout():
    rows=[]
    for bag,source in enumerate(GEO["ducts"]):
        points=[STARTS[bag],*source["points"][1:]]
        parts=[]
        for p,q in zip(points,points[1:]):
            length=prior.norm(prior.sub(q,p))
            interval=prior.sphere_interval(p,q,(0.,0.,0.),R)
            lo,hi=interval if interval else (0.,0.)
            for a,b,inside in ((0.,lo,False),(lo,hi,True),(hi,1.,False)):
                if b-a>1e-12:
                    za=p[2]+a*(q[2]-p[2]); zb=p[2]+b*(q[2]-p[2])
                    parts.append({"volume_m3":DUCT_AREA*length*(b-a),"z0_m":za,"z1_m":zb,"inside":inside})
        # Same charged equivalent elbow/tail length, all outside at header datum.
        extra=2.+.5*(len(points)-2)
        parts.append({"volume_m3":DUCT_AREA*extra,"z0_m":ZH,"z1_m":ZH,"inside":False})
        rows.append({"bag":bag,"region":REGION_FOR[bag],"points":points,
                     "length_m":sum(prior.norm(prior.sub(q,p)) for p,q in zip(points,points[1:]))+extra,
                     "parts":parts})
    return rows


DUCTS=duct_layout()
INSIDE_DUCT=sum(p["volume_m3"] for d in DUCTS for p in d["parts"] if p["inside"])
BRANCH_LENGTH=sum(d["length_m"] for d in DUCTS)


def outside_volumes(region):
    h=HEADERS[region]
    upper=region!="L12"
    # Header + two blower stubs + one controlled vent stub + two relief stubs.
    bo,ve=(1.,.8) if upper else (1.4,1.1)
    return {"header_m3":pi*h["diameter_m"]**2/4*h["length_m"],
            "two_blower_stubs_m3":2*2*pi*bo**2/4,
            "three_vent_relief_stubs_m3":3*2*pi*ve**2/4,
            "valve_cavities_m3":1. if upper else 2.}


OUTSIDE={r:outside_volumes(r) for r in REGIONS}


def duct_weight(k,region=None,inside=True):
    return sum(p["volume_m3"]*exp_average(p["z0_m"],p["z1_m"],k)
               for d in DUCTS if region is None or d["region"]==region
               for p in d["parts"] if p["inside"]==inside)


def pressure_params(h,hot):
    pa,ta,rhoa=old.atm(h)
    pg=pa+1000.
    kg=G/(RMIX*(ta+hot)); ka=G/(RA*ta)
    # Independent U0 and U3 each sense air-minus-common-gas at their own centre.
    upper=(pg*exp(-kg*CENTRES[0][2])+450.)*exp(ka*CENTRES[0][2])
    return pa,ta,rhoa,pg,kg,ka,{"U0":upper,"L12":pa+1250.,"U3":upper}


def pressure_state(h,hot):
    pa,ta,rhoa,pg,kg,ka,pzero=pressure_params(h,hot)
    # Exactly 100 m3 non-gas debit, represented at z=0 for mass quadrature.
    # It includes all solid/routing reserves; no additional 50m3 subtraction.
    fixed_weight=sphere_weight(R,kg)-100.-duct_weight(kg)
    target=INV["mol"]*RU*(ta+hot)/pg
    v=(INV["free_m3"]-target-INSIDE_DUCT)/4
    if not 0<v<min(CAPACITY):
        return {"altitude_m":h,"superheat_k":hot,"valid":False,"reason":"sealed inventory cannot fit with non-collapsible internal air","formal_lobe_air_each_m3":v}
    for iteration in range(12):
        tops=[fill_top(b,v) for b in range(4)]
        gas_weight=fixed_weight-sum(cap_weight(b,tops[b],kg) for b in range(4))
        error=gas_weight-target
        if abs(error)<2e-8: break
        v+=error/sum(exp(-kg*z) for z in tops)
        if not 0<v<min(CAPACITY):
            return {"altitude_m":h,"superheat_k":hot,"valid":False,"reason":"hydrostatic volume closure outside installed capacity","formal_lobe_air_each_m3":v}
    else: raise ArithmeticError("sealed gas volume bound")
    bags=[]
    for b in range(4):
        c=CENTRES[b]; reg=REGION_FOR[b]
        def dp(z): return pzero[reg]*exp(-ka*z)-pg*exp(-kg*z)
        bounds=[dp(c[2]+s*RB) for s in (-1,1)]
        weight=cap_weight(b,tops[b],ka)
        mass=pzero[reg]*weight/(RA*ta)
        displaced_gas=pg*cap_weight(b,tops[b],kg)/(RMIX*(ta+hot))
        bags.append({"bag":b,"region":reg,"air_m3":v,"surrogate_fill_top_z_m":tops[b],
                     "air_mass_kg":mass,"air_centroid_z_m":cap_weight(b,tops[b],ka,True)/weight,
                     "gas_displaced_by_air_kg":displaced_gas,"apparent_air_kg":mass-displaced_gas,
                     "full_envelope_dp_min_pa":min(bounds),"full_envelope_dp_max_pa":max(bounds),
                     "occupied_surrogate_dp_min_pa":dp(tops[b]),"centre_dp_pa":dp(c[2])})
    regions=[]
    for reg,indices in REGIONS.items():
        inside=pzero[reg]*duct_weight(ka,reg)/(RA*ta)
        outside=pzero[reg]*(duct_weight(ka,reg,False)+sum(OUTSIDE[reg].values())*exp(-ka*ZH))/(RA*ta)
        bagmass=sum(bags[b]["air_mass_kg"] for b in indices)
        regions.append({"region":reg,"bags":indices,"p_at_zero_pa":pzero[reg],
                        "p_header_pa":pzero[reg]*exp(-ka*ZH),
                        "bag_air_kg":bagmass,"inside_duct_air_kg":inside,
                        "outside_header_tail_air_kg":outside,"total_air_kg":bagmass+inside+outside})
    vg=INV["free_m3"]-INSIDE_DUCT-4*v
    return {"altitude_m":h,"superheat_k":hot,"valid":True,"ambient_pa":pa,"ambient_k":ta,
            "ambient_density_kg_m3":rhoa,"gas_temperature_k":ta+hot,"gas_p_at_zero_pa":pg,
            "gas_inverse_scale_m":kg,"air_inverse_scale_m":ka,"helium_space_m3":vg,
            "inside_duct_air_m3":INSIDE_DUCT,"lobe_air_total_m3":4*v,"bags":bags,"regions":regions,
            "all_air_mass_kg":sum(x["total_air_kg"] for x in regions),
            "helium_kg":INV["helium_kg"],"impurity_air_kg":INV["impurity_air_kg"],
            "volume_closure_m3":vg+INSIDE_DUCT+4*v+100.-INV["external_m3"],
            "gas_mole_residual":pg*gas_weight/(RU*(ta+hot))-INV["mol"],
            "all_nominal_envelope_dp_positive":all(b["full_envelope_dp_min_pa"]>0 for b in bags),
            "closure_iterations":iteration+1}


def hardware():
    p0=prior.BASE["pressure_system"]["parts_kg"]
    # Entire old pressure allowance/overrun replaced once; unchanged helium relief retained.
    parts={"four_upper_blowers_8m3s_3kpa_motors_drives":4*300.,
           "two_lower_blowers_16m3s_3kpa_motors_drives":2*600.,
           "six_blower_shutoffs":4*40.+2*60.,"six_blower_checks":4*25.+2*40.,
           "four_bag_shutoffs":4*50.,"three_region_control_throttles":2*60.+90.,
           "three_modulating_vents":2*35.+50.,"six_independent_reliefs":4*40.+2*60.,
           "twelve_pressure_temperature_channels":12*3.,"four_flowmeters":4*12.,
           "eight_volume_estimation_channels":8*5.,"controllers_and_24v_backup":80.,
           "two_emergency_helium_valves_retained":p0["two_emergency_helium_valves"],
           "new_branch_tubes_1mm_and_rings":BRANCH_LENGTH*(pi*(D+.001)*.001*2700+1.),
           "branch_supports_four_ports":ceil(BRANCH_LENGTH/4)*10+4*15,
           "header_stubs_2mm_aluminium_rings":0.,"header_mount_frames":3*100.,
           "wiring_feeders_breakers":200*.15+6*30*.8+6*10.,
           "two_240kw_supply_converters":2*200.,
           "120kwh_dedicated_buffer_120wh_per_kg":120000/120.,
           "buffer_enclosure_thermal":200.}
    metal=0.
    for region,h in HEADERS.items():
        upper=region!="L12"; bo,ve=(1.,.8) if upper else (1.4,1.1)
        for length,d in ((h["length_m"],h["diameter_m"]),(4.,bo),(6.,ve)):
            # Quoted diameters are clear bores; exact annular metal area.
            metal+=length*(pi*(d+.002)*.002*2700+2.)
    parts["header_stubs_2mm_aluminium_rings"]=metal
    ledger=dict(BASELINE["construction"])
    upper_extra={k:ledger[k]*.5*(.0006/.00025-1.) for k in ("bag_membranes","bag_32_gore_laps")}
    upper_extra["upper_doubler_gauge_increment"]=16*.5*(.0006-.00025)*1400
    for k in ("bag_membranes","bag_32_gore_laps"): ledger[k]+=upper_extra[k]
    ledger["bag_cradle_fittings_doublers"]+=upper_extra["upper_doubler_gauge_increment"]
    old_over=ledger["pressure_hardware_over_2t"]
    ledger["pressure_hardware_over_2t"]=max(0.,sum(parts.values())-2000.)
    return {"pressure_parts_kg":parts,"pressure_hardware_kg":sum(parts.values()),
            "old_pressure_hardware_kg":prior.BASE["pressure_system"]["mass_kg"],
            "upper_membrane_increment_kg":upper_extra,"upper_extra_per_bag_kg":sum(upper_extra.values())/2,
            "construction":ledger,"construction_kg":sum(ledger.values()),
            "construction_delta_kg":sum(ledger.values())-BASELINE["construction_kg"],
            "old_pressure_overrun_removed_kg":old_over,
            "dedicated_usable_buffer_kwh":120*.8,"surviving_converter_kw":240.,
            "region_live_motor_ratings_kw":{"U0":45.,"L12":90.,"U3":45.},
            "total_installed_motor_kw":360.,"simultaneous_live_limit_kw":180.,
            "converter_assumed_efficiency":.95,"30min_at_live_motor_limit_and_controls_kwh":(180.+2.)*.5/.95,
            "inside_new_metal_volume_bound_m3":parts["new_branch_tubes_1mm_and_rings"]/2700.,
            "routing_reserve_m3":50.,"reserve_is_within_100m3_debit":True}


HARDWARE=hardware()


def budget(state,payload):
    gross=state["ambient_density_kg_m3"]*INV["external_m3"]
    total=HARDWARE["construction_kg"]+17000.+payload+MGAS+state["all_air_mass_kg"]
    return {"payload_kg":payload,"construction_kg":HARDWARE["construction_kg"],"equipment_kg":17000.,
            "helium_kg":INV["helium_kg"],"impurity_air_kg":INV["impurity_air_kg"],
            "all_internal_external_air_kg":state["all_air_mass_kg"],"gross_displacement_kg":gross,
            "total_before_water_kg":total,"raw_margin_kg":gross-total}


def flow(state):
    h,t=state["altitude_m"],state["superheat_k"]
    dh,dt=.1,.01
    hm,hp=pressure_state(h-dh,t),pressure_state(h+dh,t)
    tm,tp=pressure_state(h,t-dt),pressure_state(h,t+dt)
    rows=[]
    pa,ta=state["ambient_pa"],state["ambient_k"]
    pin=pa*exp(-state["air_inverse_scale_m"]*ZH)
    rhoin=pin/(RA*ta)
    for i,region in enumerate(state["regions"]):
        reg=region["region"]
        dm_dh=(hp["regions"][i]["total_air_kg"]-hm["regions"][i]["total_air_kg"])/(2*dh)
        dm_dt=(tp["regions"][i]["total_air_kg"]-tm["regions"][i]["total_air_kg"])/(2*dt)
        # dh/dtime=-1m/s and superheat cooling=-10K/hour; ambient lapse included in dh.
        mdot=-dm_dh-dm_dt*10/3600
        qin=mdot/rhoin
        rhoheader=region["p_header_pa"]/(RA*ta)
        qheader=mdot/rhoheader
        branchflows=[]
        for b in region["bags"]:
            q=qheader/len(region["bags"])
            velocity=q/DUCT_AREA
            loss=(.02*DUCTS[b]["length_m"]/D+8.)*rhoheader*velocity**2/2
            branchflows.append({"bag":b,"flow_header_m3_s":q,"velocity_m_s":velocity,"loss_pa":loss})
        hd=HEADERS[reg]["diameter_m"]
        hvel=qheader/(pi*hd**2/4)
        header_loss=(.02*HEADERS[reg]["length_m"]/hd+4.)*rhoheader*hvel*hvel/2
        pout=region["p_header_pa"]+max(b["loss_pa"] for b in branchflows)+header_loss
        # Reversible isothermal compression of ambient air, with stated efficiency.
        ideal=mdot*RA*ta*log(pout/pin)
        rated=HEADERS[reg]["rating_m3_s"]
        ventd=.8 if reg!="L12" else 1.1
        ventq=qheader
        vent_loss=(.02*2/ventd+6.)*rhoheader*(ventq/(pi*ventd**2/4))**2/2
        return_loss=max(b["loss_pa"] for b in branchflows)+header_loss
        available_vent_head=region["p_header_pa"]-pin-return_loss
        rows.append({"region":reg,"dair_dh_kg_m":dm_dh,"dair_dsuperheat_kg_k":dm_dt,
                     "required_air_mass_flow_kg_s":mdot,"ambient_header_inlet_m3_s":qin,
                     "header_density_kg_m3":rhoheader,"header_delivery_m3_s":qheader,
                     "inlet_pressure_pa":pin,"blower_discharge_pa":pout,"actual_rise_pa":pout-pin,
                     "branch_flows":branchflows,"header_loss_pa":header_loss,
                     "one_blower_out_capacity_m3_s":rated,"flow_ok":qin<=rated,
                     "assumed_blower_head_limit_pa":3000.,"head_ok":pout-pin<=3000.,
                     "isothermal_work_w":ideal,"shaft_w":ideal/.65,
                     "vent_path_loss_pa":vent_loss,"return_branch_header_loss_pa":return_loss,
                     "vent_pressure_available_pa":available_vent_head,
                     "single_vent_passive_capacity_screen":vent_loss<=available_vent_head})
    rigid_volume=INSIDE_DUCT+sum(p["volume_m3"] for d in DUCTS for p in d["parts"] if not p["inside"])+sum(sum(v.values()) for v in OUTSIDE.values())
    # Static endpoint inventories are exact within the occupancy model. During flow,
    # extra duct/header pressure is not a hydrostatic field: bound its added mass.
    excess=max(r["blower_discharge_pa"]-state["regions"][i]["p_header_pa"] for i,r in enumerate(rows))
    return {"descent_m_s":1.,"additional_superheat_cooling_k_h":10.,"rows":rows,
            "gas_volume_dh_m3_m":(hp["helium_space_m3"]-hm["helium_space_m3"])/(2*dh),
            "gas_volume_dsuperheat_m3_k":(tp["helium_space_m3"]-tm["helium_space_m3"])/(2*dt),
            "total_inlet_m3_s":sum(r["ambient_header_inlet_m3_s"] for r in rows),
            "total_shaft_kw":sum(r["shaft_w"] for r in rows)/1000.,
            "supply_kw_including_controls_and_converter_loss":(sum(r["shaft_w"] for r in rows)/1000.+2.)/.95,
            "flow_overpressure_air_mass_upper_bound_kg":rigid_volume*excess/(RA*ta),
            "control_kw":2.,"all_one_out_screens_ok":all(r["flow_ok"] and r["head_ok"] for r in rows)}


def controls(state):
    ka,kg=state["air_inverse_scale_m"],state["gas_inverse_scale_m"]
    pg,pa=state["gas_p_at_zero_pa"],state["ambient_pa"]
    rows=[]
    for region in state["regions"]:
        upper=region["region"]!="L12"
        zd=CENTRES[0][2] if upper else 0.
        gauge=.0006 if upper else .00025
        working=2*30e6*.60*gauge/RB
        # Min 50Pa inflation target, and nominal working strip-pressure bound.
        lower,high=-1e20,1e20
        for b in region["bags"]:
            for z in (CENTRES[b][2]-RB,CENTRES[b][2]+RB):
                factor=exp(-ka*(z-zd))
                offset=pg*exp(-kg*zd)*factor-pg*exp(-kg*z)
                lower=max(lower,(50.-offset)/factor)
                high=min(high,(working-offset)/factor)
        nominal=450. if upper else 250.
        band=(425.,475.) if upper else (225.,275.)
        # Two mechanical reliefs per outside header, each to ambient, no cross-header bypass.
        # These are preliminary thresholds, not a claim of adequate failure protection.
        relief=2100. if upper else 1900.
        relief_pzero=(pa*exp(-ka*ZH)+relief)*exp(ka*ZH)
        relief_peak=max(relief_pzero*exp(-ka*(CENTRES[b][2]-RB))-pg*exp(-kg*(CENTRES[b][2]-RB)) for b in region["bags"])
        portdata=[]
        for b in region["bags"]:
            port=(CENTRES[b][0],CENTRES[b][1],CENTRES[b][2]-RB)
            portdata.append({"bag":b,"tap_xyz_m":port,
                             "air_pressure_pa":region["p_at_zero_pa"]*exp(-ka*port[2]),
                             "helium_side_pressure_pa":pg*exp(-kg*port[2])})
        rows.append({"region":region["region"],"control_datum_z_m":zd,"target_differential_pa":nominal,
                     "deadband_pa":band,"inlet_trip_differential_pa":525. if upper else 325.,
                     "admissible_datum_for_50pa_min_and_working_membrane_pa":[lower,high],
                     "deadband_inside_admissible_bounds":lower<=band[0]<band[1]<=high,
                     "fixed_port_sensors":portdata,"nominal_working_pressure_bound_pa":working,
                     "outside_header_relief_above_local_ambient_pa":relief,
                     "no_flow_relief_full_envelope_peak_pa":relief_peak,
                     "relief_static_working_screen_ok":relief_peak<=working,
                     "relief_1p5_limit_screen_ok":1.5*relief_peak<=working,
                     "isolated_bag_relief_available":False})
    return {"regions":rows,"pressure_target_is_not_a_membrane_or_controller_stability_solution":True,
            "failure_result":"FAIL/UNKNOWN: header relief does not protect a bag behind its closed branch valve; relief membrane limit screens also fail. A closed branch is an excluded trapped-air fault state, not nominal operation."}


def cuff_screen(state,contact):
    bagfixed=(prior.BASE["bag_supported_mass_bound_kg"]-prior.BASE["bag_apparent_capacity_kg"])/4
    bagloads=[b["apparent_air_kg"]+bagfixed+(HARDWARE["upper_extra_per_bag_kg"] if b["bag"] in (0,3) else 0.) for b in state["bags"]]
    tensions=[m*G/8 for m in bagloads]
    stiffness,source,foreign=[0.]*4,[0.]*4,[0.]*4
    loads=[]
    for i,hanger in enumerate(GEO["hangers"]):
        owner=hanger["bag"]; tension=tensions[owner]
        guide=next((g for g in GUIDES if g["hanger"]==i),None)
        upper,extension=prior.hanger_axial(FREE[i],tension,guide)
        length=FREE[i]+extension
        a,b=(guide["start_m"]-tension/KBAND,guide["end_m"]-tension/KBAND) if guide else (0.,0.)
        if guide: assert 0<=a<b<=length
        foreignbag=state["bags"][guide["foreign_bag"]] if guide else None
        # Same declared full-envelope pressure cap and full paid span as predecessor.
        q=.24*max(abs(foreignbag["full_envelope_dp_min_pa"]),abs(foreignbag["full_envelope_dp_max_pa"])) if guide and contact else 0.
        force=q*(b-a); r0=force*(1-(a+b)/(2*length))
        keff=1/(length/tension+1/KF+1/KBAND)
        forcing=keff*(force/KF+r0*length/tension)
        stiffness[owner]+=keff; source[owner]+=forcing
        if guide: foreign[guide["foreign_bag"]]+=force
        loads.append((tension,upper,extension,length,guide,a,b,q,force,r0,keff,forcing))
    shifts=[(source[b]-foreign[b])/stiffness[b] for b in range(4)]
    rows=[]; balance=[-f for f in foreign]
    for i,(hanger,load) in enumerate(zip(GEO["hangers"],loads)):
        tension,upper,extension,length,guide,a,b,q,force,r0,keff,forcing=load
        owner=hanger["bag"]
        bottom=forcing-keff*shifts[owner]; top=force-bottom
        balance[owner]+=bottom
        x0=shifts[owner]+bottom/KBAND; xL=top/KF
        def slope(z): return (xL-x0+r0*length/tension)/length-q/tension*max(0.,z-a)+q/tension*max(0.,z-b)
        def x_at(z): return x0+(xL-x0)*z/length+r0*z/tension-q/(2*tension)*max(0.,z-a)**2+q/(2*tension)*max(0.,z-b)**2
        knots=sorted(set((0.,a,b,length)))
        excess=sum((v-u)*(slope(u)**2+slope(u)*slope(v)+slope(v)**2)/6 for u,v in zip(knots,knots[1:]))
        drop=(upper+prior.BAG_ACT["mass_kg"]*G)/KF; rise=tension/KBAND
        vertical=length-excess
        cmd=hanger["length_m"]-drop-rise-vertical-upper/prior.BAG_ACT["axial_stiffness_n_m"]
        maxs=max(abs(slope(z)) for z in knots)
        pts=[(hanger["low"][0]+x_at(z),hanger["low"][1],hanger["low"][2]+rise+vertical*z/length) for z in knots]
        pressure_samples=[]
        if guide:
            fbag=state["bags"][guide["foreign_bag"]]
            preg=next(r for r in state["regions"] if r["region"]==fbag["region"])
            for z in (a,(a+b)/2,b):
                actual_z=hanger["low"][2]+rise+vertical*z/length
                dp=preg["p_at_zero_pa"]*exp(-state["air_inverse_scale_m"]*actual_z)-state["gas_p_at_zero_pa"]*exp(-state["gas_inverse_scale_m"]*actual_z)
                pressure_samples.append({"z_m":actual_z,"dp_pa":dp})
        rows.append({"hanger":i,"bag":owner,"foreign_bag":guide["foreign_bag"] if guide else None,
                     "free_length_m":FREE[i],"paid_liner_length_m":guide["length_m"] if guide else 0.,
                     "lower_vertical_tension_n":tension,"upper_vertical_tension_n":upper,
                     "q_cuff_n_m":q,"cuff_force_n":force,"equal_opposite_foreign_force_n":-force,
                     "cuff_application_xyz_m":(hanger["low"][0]+x_at((a+b)/2),hanger["low"][1],hanger["low"][2]+rise+vertical*(a+b)/(2*length)) if guide else None,
                     "bottom_horizontal_reaction_n":bottom,"top_horizontal_reaction_n":top,
                     "lower_band_offset_m":bottom/KBAND,"top_foundation_offset_m":top/KF,
                     "band_rise_m":rise,"top_drop_m":drop,"axial_extension_m":extension,
                     "maximum_slope":maxs,"small_slope_ok":maxs<=.2,
                     "geometric_excess_m":excess,"actuator_command_m":cmd,"stroke_ok":prior.BAG_MIN<=cmd<=prior.BAG_MAX,
                     "liner_following_stress_pa":70e9*.12*q/tension,
                     "saddle_side_load_n":q*1.5,"actual_line_dp_samples":pressure_samples,"points":pts,
                     "upper_resultant_n":sqrt(upper*upper+top*top)})
    shifted=[prior.add(c,(s,0.,0.)) for c,s in zip(CENTRES,shifts)]
    side_moments=[0.]*4
    for row,hanger in zip(rows,GEO["hangers"]):
        owner=row["bag"]
        side_moments[owner]+=(hanger["low"][2]+row["band_rise_m"]-CENTRES[owner][2])*row["bottom_horizontal_reaction_n"]
        if row["foreign_bag"] is not None:
            foreign_id=row["foreign_bag"]
            side_moments[foreign_id]-=(row["cuff_application_xyz_m"][2]-CENTRES[foreign_id][2])*row["cuff_force_n"]
    gap=min(prior.norm(prior.sub(a,b))-2*RB for i,a in enumerate(shifted) for b in shifted[:i])
    hullgap=min(R-prior.norm(c)-RB for c in shifted)
    firstmoment=sum((state["bags"][b]["air_mass_kg"]+bagfixed+(HARDWARE["upper_extra_per_bag_kg"] if b in (0,3) else 0.))*shifts[b] for b in range(4))
    domain=all(r["small_slope_ok"] for r in rows)
    return {"contact":contact,"bag_vertical_supported_mass_kg":bagloads,"bag_shifts_x_m":shifts,
            "minimum_full_envelope_gap_m":gap,"minimum_full_envelope_hull_gap_m":hullgap,
            "maximum_slope":max(r["maximum_slope"] for r in rows),"within_small_slope_domain":domain,
            "all_strokes_ok":all(r["stroke_ok"] for r in rows),
            "command_range_m":[min(r["actuator_command_m"] for r in rows),max(r["actuator_command_m"] for r in rows)],
            "horizontal_balance_residual_n":max(abs(x) for x in balance),
            "global_side_force_residual_n":sum(r["top_horizontal_reaction_n"] for r in rows),
            "side_load_moment_y_unclosed_nm":side_moments,
            "bag_rotation_and_membrane_moment_balance_solved":False,
            "additional_water_trim_cos_amplitude_kg":-firstmoment/(4*GEO["module_radius_m"]),
            "hanger_limit_kn":1.5*max(r["upper_resultant_n"] for r in rows)/1000.,
            "hanger_working_kn":150e6*prior.HANGER_A/1000.,
            "liner_following_limit_mpa":1.5*max(r["liner_following_stress_pa"] for r in rows)/1e6,
            "represented_contact_clearance_ok":domain and gap>=0 and hullgap>=0,
            "physical_compatibility":"UNKNOWN; cap occupancy, membrane/cuff and beam/string compatibility not solved",
            "rows":rows}


def thermal_transition(h):
    # Cool +10K to 0K at fixed altitude in one hour. No climb/descent overlap.
    def integrand(theta):
        s=pressure_state(h,theta); dt=.01
        a,b=pressure_state(h,theta-dt),pressure_state(h,theta+dt)
        pa,ta=s["ambient_pa"],s["ambient_k"]
        pin=pa*exp(-s["air_inverse_scale_m"]*ZH)
        total=0.
        for i,reg in enumerate(s["regions"]):
            dm=-(b["regions"][i]["total_air_kg"]-a["regions"][i]["total_air_kg"])/(2*dt)
            mdot=dm*10/3600
            rho=reg["p_header_pa"]/(RA*ta); q=mdot/rho
            d=HEADERS[reg["region"]]["diameter_m"]
            branch=max((.02*DUCTS[j]["length_m"]/D+8.)*rho*(q/len(reg["bags"])/DUCT_AREA)**2/2 for j in reg["bags"])
            loss=branch+(.02*HEADERS[reg["region"]]["length_m"]/d+4.)*rho*(q/(pi*d*d/4))**2/2
            total+=dm*RA*ta*log((reg["p_header_pa"]+loss)/pin)/.65
        return total
    # Fixed 8-panel Simpson integration, 9 states, not a pressure/design search.
    step=10/8
    values=[integrand(i*step) for i in range(9)]
    work=step/3*(values[0]+values[-1]+4*sum(values[1:-1:2])+2*sum(values[2:-1:2]))
    cold,hot=pressure_state(h,0.),pressure_state(h,10.)
    return {"altitude_m":h,"cooling_k":10.,"duration_s":3600.,
            "air_added_kg":cold["all_air_mass_kg"]-hot["all_air_mass_kg"],
            "shaft_work_j":work,"shaft_work_kwh":work/3.6e6,"mean_shaft_kw":work/3.6e6,
            "controls_kwh":2.,"heat_transfer_and_motor_transients_unmodelled":True}


def main():
    import resource
    resource.setrlimit(resource.RLIMIT_CPU,(180,180))
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    states=[pressure_state(h,t) for h in (0.,2500.) for t in (0.,10.)]
    for s in states:
        assert s["valid"] and abs(s["gas_mole_residual"])<1e-5 and abs(s["volume_closure_m3"])<1e-7
        s["M20"]=budget(s,3000.); s["P100"]=budget(s,100000.)
        s["flow"]=flow(s)
        s["controls"]=controls(s)
        s["hangers_no_lateral_cuff"]=cuff_screen(s,False)
        s["cuff_contact_screen"]=cuff_screen(s,True)
        assert s["cuff_contact_screen"]["horizontal_balance_residual_n"]<1e-7
        assert abs(s["cuff_contact_screen"]["global_side_force_residual_n"])<1e-7
    water=min(s["M20"]["raw_margin_kg"] for s in states if s["superheat_k"]==0.)
    for s in states:
        s["M20_fixed_water_kg"]=water
        s["M20_residual_after_water_kg"]=s["M20"]["raw_margin_kg"]-water
        s["M20_residual_with_inherited_water_kg"]=s["M20"]["raw_margin_kg"]-BASELINE["fixed_water_ballast_kg"]
    invalid=pressure_state(2500.,15.)
    assert not invalid["valid"]
    output={"calculator_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "predecessor_sha256":PRIOR_SHA,"baseline_sha256":BASELINE_SHA,"inventory":INV,
            "headers":HEADERS,"ducts":DUCTS,"outside_volumes":OUTSIDE,"bag_centres":CENTRES,
            "bag_radius_m":RB,"bag_capacities_excluding_liners_m3":CAPACITY,
            "hardware":HARDWARE,"fixed_comparison":BASELINE,"states":states,
            "same_inventory_15k":invalid,"thermal_cooling_transitions":[thermal_transition(h) for h in (0.,2500.)],
            "bounds":{"cpu_s":180,"memory_mib":512,"outer_volume_iterations":12,"cap_iterations":30,"quadrature_order":24},
            "result":"Conditional pressure/flow arithmetic; contact and vehicle compatibility UNKNOWN/FAIL, P100 FAIL"}
    print(json.dumps(output,indent=2))


if __name__=="__main__": main()
