"""Independent MAINLINE-054 arithmetic from published methods and non-code inputs.

No owner's implementation is accessed. Only 052 result inputs are inherited;
054 result fields are comparison targets, never numerical model inputs.
"""
from pathlib import Path
import collections
import csv
import datetime
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
I = ROOT / "inputs/owner"
RG = 8.31446261815324
MW = 0.01801528
T0 = 284.9
THOT = 320.0
P0 = 95460.83791390515
PHOT = 0.964012200518
STHERM = 90.501688129e6
RC10 = 2.6159809746514977
L10 = 1799.6766239090878
SIGMA = 5.670374419e-8
EPS = 0.8
BEDTEMP = 333.0
WALLTEMP = 321.940239586
COOLDOWN_K = 325.0


def js(p):
    return json.loads(p.read_text())


def dump(name, obj):
    (ROOT/name).write_text(json.dumps(obj, indent=2, allow_nan=False)+"\n")


def psat(t):
    c = t-273.15
    return 611.21*math.exp((18.678-c/234.5)*c/(257.14+c))


PLIM = 0.05*psat(274.007116986)
PCOLD = 0.05*psat(268.630060911)  # independently checked against inherited 046 below
PDES = 0.8*PCOLD


def root_increasing(func, value=0.0, lo=0.0, hi=1.0):
    while func(hi) < value:
        hi *= 2
        if hi > 1e12:
            raise ValueError("No finite crossing below 1e12.")
    for _ in range(100):
        mid = (lo+hi)/2
        if func(mid) < value:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def gsta(t, p):
    # Eq.1 and Table 2 transcribed from source page 8 and page 11.
    hs = [-46600., -125000., -193600., -272200.]
    ss = [-53.7, -221.1, -356.7, -567.5]
    terms = [math.exp(-h/(RG*t)+s/RG)*(p/100000.)**n
             for n, (h, s) in enumerate(zip(hs, ss), 1)]
    return 0.21/4 * sum(n*x for n, x in enumerate(terms, 1))/(1+sum(terms))


CAND = {
    "B0": (1.0, 12e-6*1390+100e-9*2700, 38., .9, "QUESTIONABLE"),
    "MET": (.1, 1/59.52+100e-9*2700, 38., .5, "QUESTIONABLE"),
    "SIOX": (.08, 12e-6*1390+.002+100e-9*2700, 40., .9, "QUESTIONABLE"),
    "ALD": (.0008, 12e-6*1390+30e-9*3000+100e-9*2700, 38., 1., "PROJECTION"),
    "ML3": (.00005, 12e-6*1390+3*(30e-9*3000+500e-9*1300)+100e-9*2700, 38., 1., "PROJECTION"),
    "VERREAL": (.001, 50e-6*1390+.002+100e-9*2700, 40., .9, "QUESTIONABLE"),
    "FOIL30": (.001, 30e-6*2700+25e-6*1390+.003, 40., .9, "QUESTIONABLE"),
    "FOIL9": (.01, 9e-6*2700+12e-6*1390+.003, 38., .9, "PROJECTION"),
    "PVDC": (.065/(100*.0254**2), .45359237/(39.2*.3048**2)+100e-9*2700, (100-32)*5/9, .9, "QUESTIONABLE"),
}

UP = js(I/"inputs/052/RESULTS.json")
GAS = js(I/"inputs/034/INPUTS.json")
SP = GAS["species"]
NORM = sum(x["dry_x"] for x in SP.values())
MEANMW = sum(x["M_kg_mol"]*x["dry_x"]/NORM for x in SP.values())
ACCOUNTS = {}
for row in UP["rows"]:
    if row["service"] != "ground" or row["R_m"] not in [10, 12, 15]:
        continue
    for kind, field in [("endpoint", "all_axes_endpoint"), ("least052", "least")]:
        if row[field] is not None:
            a = dict(row[field])
            a["account"] = kind
            ACCOUNTS[(a["R_m"], a["weather"], kind)] = a


def ident(a, **kwargs):
    return dict(R_m=a["R_m"], weather=a["weather"], account=a["account"], **kwargs)


def getbase(row):
    return ACCOUNTS[row["R_m"], row["weather"], row.get("account", "endpoint")]


def flow(a, name, multiplier=1., leak_multiplier=1., loss=0., carrier_um=None):
    k = a["R_m"]/10
    area = 4*math.pi*a["R_m"]**2
    rate, am, tc, rh, tag = CAND[name]
    if carrier_um is not None:
        am += (carrier_um-12)*1e-6*1390
    w = UP["weather"][a["weather"]]
    pe = P0*w["pressure_factor"]
    yw = w["pw_Pa"]/pe
    rhfactor = max(1., w["pw_Pa"]/(rh*psat(tc+273.15)))
    # Scale the complete seam+node+port source uniformly in leakage sensitivity.
    nleak = (.001*(L10*k+252)+.01)*.1*86400/(RG*T0)*leak_multiplier
    leakwater = nleak*yw*MW
    drymol = drymass = 0.
    for name_sp, s in SP.items():
        if name_sp == "H2O":
            continue
        frac = s["dry_x"]/NORM
        nperm = (area*.5*GAS["mylar"]["permeance_ratios_to_O2_assumed"][name_sp]
                 * (pe-w["pw_Pa"])*frac/101325./22414.)
        n = nleak*(1-yw)*frac+nperm
        drymol += n
        drymass += n*s["M_kg_mol"]
    actual_rate = (rate*rhfactor*(1-loss)+40.*loss)*multiplier
    permwater = area*actual_rate/1000
    delta = area*(am-CAND["B0"][1])
    release = a["vacuum"]["initial_material_release_water_proxy_kg"] + max(0., delta)*.001
    return dict(area_m2=area, wvtr_g_m2_day=actual_rate, rh_factor=rhfactor,
                permeation_water_kg_day=permwater, leak_water_kg_day=leakwater,
                water_kg_day=permwater+leakwater, release_kg=release,
                dry_mol_day=drymol, dry_kg_day=drymass,
                barrier_delta_kg=delta, barrier_mass_kg=area*am)


def sealed(a, name, multiplier=1., leak_multiplier=1., loss=0., carrier_um=None):
    f = flow(a, name, multiplier, leak_multiplier, loss, carrier_um)
    vol = a["vacuum"]["free_volume_m3"]
    n0 = 10*vol/(RG*T0)
    def water(d):
        return f["water_kg_day"]*d + f["release_kg"]*(-math.expm1(-d))
    def pressure(d):
        return (n0+f["dry_mol_day"]*d+water(d)/MW)*RG*THOT/vol
    hum = root_increasing(water, PLIM*vol*MW/(RG*T0))
    cold = root_increasing(water, PCOLD*vol*MW/(RG*T0))
    pres = root_increasing(pressure, .01*P0)
    sched = .9*min(hum, pres)
    scold = .9*min(cold, pres)
    charged = max(a["bill_kg"]["gas"], n0*MEANMW + (f["dry_kg_day"]+f["water_kg_day"])*sched)
    return ident(a, candidate=name, tag=CAND[name][-1], **f,
                 first_humidity_days=hum, cold_h2_first_days=cold,
                 total_pressure_days=pres, scheduled_ground_days=sched,
                 scheduled_ground_cold_h2_days=scold, charged_gas_kg=charged,
                 payload_kg=a["payload_kg"]-f["barrier_delta_kg"]-(charged-a["bill_kg"]["gas"]),
                 qualified_service_days=None)


def capture(a, name, d, capacity=.06, power=.5, multiplier=1., leak_multiplier=1.):
    f = flow(a, name, multiplier, leak_multiplier)
    release_fraction = -math.expm1(-d)
    external = f["water_kg_day"]*d
    material = f["release_kg"]*release_fraction
    # Solve both housing branches analytically; select the self-consistent one.
    low = 1.1*(external+material+.001*6*release_fraction)/capacity
    if low <= 4:
        bed = low
        housing = 1.
    else:
        bed = 1.1*(external+material+.001*5*release_fraction)/(capacity-1.1*.001*.25*release_fraction)
        housing = .25*bed
    hardware = housing+5
    released = material+.001*hardware*release_fraction
    captured = external+released
    battery = power*24*d/108
    system = bed+hardware+battery
    vol0 = a["vacuum"]["free_volume_m3"]
    # Effective hardware density of 1000 kg/m3 is a reconstructed undocumented
    # numerical convention; bed bulk density 600 is documented in SOURCE-AUDIT.
    vol = vol0-bed/600-hardware/1000
    n0 = 10*vol0/(RG*T0)
    retained = n0*MEANMW + f["dry_kg_day"]*d + external + .01*bed
    charged = max(a["bill_kg"]["gas"], retained)
    excess = charged-a["bill_kg"]["gas"]
    bill = f["barrier_delta_kg"]+system+excess
    payload = a["payload_kg"]-bill
    dp = (n0+f["dry_mol_day"]*d)*RG*THOT/vol
    pressure = dp+PDES
    energy = ((bed+hardware)*1000*COOLDOWN_K+captured*4.4e6)/3.6e6
    return ident(a, candidate=name, days=d, tag="PROJECTION",
                 rate_multiplier=multiplier, leak_multiplier=leak_multiplier,
                 working_capacity_kg_kg=capacity, external_water_retained_kg=external,
                 material_water_redistributed_kg=released, bed_dry_kg=bed,
                 bed_initial_water_kg=.01*bed, housing_kg=housing,
                 distribution_monitoring_kg=5., monitoring_power_W=power,
                 battery_kg=battery, capture_system_kg=system,
                 barrier_delta_kg=f["barrier_delta_kg"], barrier_mass_kg=f["barrier_mass_kg"],
                 captured_water_kg=captured, charged_gas_and_retained_external_mass_kg=charged,
                 reserve_used_kg=retained, reserve_extra_kg=excess, incremental_bill_kg=bill,
                 payload_kg=payload, pressure_Pa=pressure, dry_pressure_Pa=dp,
                 pressure_SF=.01*P0/pressure, humidity_pressure_design_Pa=PDES,
                 free_volume_m3=vol, bed_bulk_volume_L=bed/600*1000,
                 regeneration_ideal_kWh=energy, regeneration_planning_2x_kWh=2*energy,
                 adsorption_average_heat_W=captured*4.4e6/(86400*d),
                 capacity_screen_pass=(gsta(BEDTEMP, PDES)-.01)*.8 >= capacity,
                 pressure_screen_pass=pressure <= .01*P0,
                 algebraic_closure=payload >= -1e-8 and pressure <= .01*P0,
                 installed_dryness_verified=False, qualified_hull_SF=None)


FIBRES = {
    "aramid_yarn_limit": (3e9, 1., .95, 1440., None),
    "aramid_60pct_laminate": (3e9, .6, .95, 1440., None),
    "SK99_yarn_limit": (42.5*100000*970, 1., .99599466459, 970., 7e-6),
    "DM20_yarn_limit": (32*100000*970, 1., .99599466459, 970., 1.3e-6),
    "UHMWPE_900MPa_creep_screen": (9e8, 1., 1., 970., None),
}


def fibre(a, name):
    strength, eff, ret, rho, creep = FIBRES[name]
    load = a["applied_pressure_Pa"]*RC10*a["R_m"]/10
    allowable = strength*eff*ret*PHOT
    gauge = load/(allowable-STHERM)
    mass = 4*math.pi*a["R_m"]**2*gauge*rho
    delta = mass-a["bill_kg"]["PBO_two_plies"]
    oldstress = load/a["film_total_m"]+STHERM
    return ident(a, fibre=name, tag="PROJECTION", yarn_strength_Pa=strength,
                 efficiency=eff, assumed_retention=ret,
                 strength_ratio_to052=strength*eff/a["film_effective_strength_Pa"],
                 density_kg_m3=rho, same_gauge_film_SF=allowable/oldstress,
                 resized_gauge_m=gauge, resized_mass_kg=mass, film_mass_delta_kg=delta,
                 resized_payload_kg=a["payload_kg"]-delta,
                 resized_film_SF=allowable/(load/gauge+STHERM),
                 resized_P3_screen_SF=min(1., a["all_screened_SF"]),
                 creep_1pct_hours_at900MPa_30C=None if creep is None else 1/creep/3600,
                 installed_service_days=None, qualified_SF=None)


def fibre_mission(a, name, d):
    fr = fibre(a, name)
    f = flow(a, "MET")
    vol = (a["vacuum"]["free_volume_m3"] -
           (fr["resized_mass_kg"]/fr["density_kg_m3"]-a["bill_kg"]["PBO_two_plies"]/1560))
    n0 = 10*vol/(RG*T0)
    allowance = .01*fr["resized_mass_kg"]
    source = max(allowance, f["release_kg"])
    def pressure(t):
        return (n0+f["dry_mol_day"]*t+
                (f["water_kg_day"]*t+source*(-math.expm1(-t)))/MW)*RG*THOT/vol
    charged = max(a["bill_kg"]["gas"],
                  n0*MEANMW+(f["dry_kg_day"]+f["water_kg_day"])*d+allowance)
    payload = fr["resized_payload_kg"]-f["barrier_delta_kg"]-(charged-a["bill_kg"]["gas"])
    return ident(a, fibre=name, days=d, tag="PROJECTION", barrier="MET",
                 pressure_Pa=pressure(d), pressure_interval_days=.9*root_increasing(pressure, .01*P0),
                 carried_film_water_allowance_kg=allowance, charged_external_mass_kg=charged,
                 payload_kg=payload, pressure_pass=pressure(d) <= .01*P0,
                 frame_and_resized_film_screen_SF=fr["resized_P3_screen_SF"],
                 humidity_tolerance_verified=False, creep_service_qualified=False, qualified_SF=None)


def choice(a, name, d):
    b = sealed(a, name)
    c = capture(a, name, d)
    f = flow(a, name)
    if d <= b["scheduled_ground_cold_h2_days"]:
        vol = a["vacuum"]["free_volume_m3"]
        retained = 10*vol/(RG*T0)*MEANMW+(f["dry_kg_day"]+f["water_kg_day"])*d
        extra = max(0., retained-a["bill_kg"]["gas"])
        bill = f["barrier_delta_kg"]+extra
        payload = a["payload_kg"]-bill
        system = 0.
        route = "barrier_only"
        pressure_ok = True
    else:
        bill, payload, system = c["incremental_bill_kg"], c["payload_kg"], c["capture_system_kg"]
        route = "barrier_plus_3A"
        pressure_ok = c["pressure_screen_pass"]
    return ident(a, days=d, candidate=name, tag=CAND[name][-1], route=route,
                 payload_kg=payload, capture_system_kg=system, incremental_bill_kg=bill,
                 cold_h2_screen_pass=True, pressure_screen_pass=pressure_ok,
                 algebraic_closure=payload >= -1e-8 and pressure_ok,
                 measured_installed_dryness=False, qualified_hull=False)


def transport(a, name, d):
    c = capture(a, name, d)
    f = flow(a, name)
    peak = f["water_kg_day"]+f["release_kg"]+.001*(c["housing_kg"]+5)
    loading = .01+c["captured_water_kg"]/c["bed_dry_kg"]
    eqp = root_increasing(lambda p: gsta(BEDTEMP, p), loading, hi=1.)
    conductance = peak/MW*RG*THOT/(24*(PDES-eqp))
    heat = peak*4.4e6/86400
    arad = heat/(EPS*SIGMA*(BEDTEMP**4-WALLTEMP**4))
    return dict(R_m=a["R_m"], weather=a["weather"], candidate=name, days=d,
                tag="PROJECTION", water_peak_kg_day=peak, bed_end_loading_kg_kg=loading,
                bed_end_equilibrium_Pa=eqp, chamber_water_design_Pa=PDES,
                effective_water_conductance_required_m3_h=conductance,
                peak_adsorption_heat_W=heat, ideal_radiating_area_m2=arad,
                hardware_realisation_qualified=False)


CHECKS = []
MISMATCH = []
COMPUTED = collections.defaultdict(list)


def compare(table, rowid, field, owner, ours, atol=1e-8, rtol=1e-9):
    numeric = isinstance(owner, (int, float)) and not isinstance(owner, bool)
    if numeric and isinstance(ours, (int, float)):
        delta = ours-owner
        limit = atol+rtol*abs(owner)
        ok = abs(delta) <= limit
    else:
        delta, limit = None, None
        ok = owner == ours
    rec = dict(table=table, row=rowid, field=field, owner=owner, checker=ours,
               delta=delta, tolerance=limit, pass_check=ok)
    CHECKS.append(rec)
    if not ok:
        MISMATCH.append(rec)


def compare_row(table, idx, own, calc):
    rowid = {k:own[k] for k in ["R_m", "weather", "account", "candidate", "fibre", "days", "scenario", "T_K", "water_pressure_Pa", "assumed_PET_gauge_um"] if k in own}
    rowid["index"] = idx
    for field, value in calc.items():
        if field in own:
            compare(table, rowid, field, own[field], value)
    COMPUTED[table].append(calc)


def main():
    global PCOLD, PDES
    # Inherit 052's humidity design input, independently recovered from its
    # published crossing/inventory equation. 046 temperature is a crosscheck.
    spec = js(ROOT/"SPECIFICATION.json")
    PCOLD = spec["cold_pressure052_Pa"]
    PDES = .8*PCOLD
    owner = js(I/"RESULTS.json")
    trans = js(I/"TRANSPORT.json")
    for idx, row in enumerate(js(I/"CANDIDATES.json")):
        rate, mass, tc, rh, tag = CAND[row["id"]]
        compare_row("candidates", idx, row, dict(id=row["id"], coupon_WVTR_g_m2_day=rate,
                    charged_barrier_kg_m2=mass, test_temperature_C=tc, test_RH=rh, tag=tag))
    for key, a in ACCOUNTS.items():
        f = flow(a, "B0")
        v = a["vacuum"]
        old_water = f["area_m2"]/1000+f["leak_water_kg_day"]
        compare("baseline052", str(key), "water_external_upper_kg_day", v["water_external_upper_kg_day"], old_water)
        compare("baseline052", str(key), "dry_external_kg_day", v["dry_external_kg_day"], f["dry_kg_day"])
        compare("baseline052", str(key), "initial_gas_kg", v["initial_gas_kg"], 10*v["free_volume_m3"]/(RG*T0)*MEANMW)
        compare("baseline052", str(key), "payload_kg", a["payload_kg"], a["lift_kg"]-sum(a["bill_kg"].values()))
        # 052 lacked 054's deliberate RH correction in "both" weather.
        b = sealed(a, "B0", multiplier=1/f["rh_factor"])
        for field, dest in [("first_cycle_humidity_limit_h","first_humidity_days"),
                            ("cold_h2_humidity_limit_h","cold_h2_first_days"),
                            ("total_pressure_limit_h","total_pressure_days")]:
            compare("baseline052", str(key), field, v[field], 24*b[dest])
    for idx, row in enumerate(owner["trace"]):
        a = ACCOUNTS[10, "ISA", row["account"]]
        calc = flow(a, "B0")
        vol = a["vacuum"]["free_volume_m3"]
        calc.update(account=row["account"], water_capacity_kg=PLIM*vol*MW/(RG*T0),
                    humidity_target_Pa=PLIM, free_volume_m3=vol,
                    frozen_first_crossing_h=a["vacuum"]["first_cycle_humidity_limit_h"],
                    recomputed_first_crossing_h=24*sealed(a,"B0")["first_humidity_days"],
                    cold_film_temperature_K=274.007116986, hot_film_temperature_K=WALLTEMP)
        compare_row("trace",idx,row,calc)
    for table in ["barriers", "ground_stress", "multilayer_carrier_sensitivity"]:
        for idx, row in enumerate(owner[table]):
            scenario=row.get("scenario","")
            mult = float(scenario[5:]) if scenario.startswith("WVTRx") else 1.
            leak = 10. if scenario == "leakx10" else 1.
            loss = float(scenario.split("_")[-1]) if scenario.startswith("intactPET_coating_loss_") else 0.
            calc = sealed(getbase(row), row["candidate"], mult, leak, loss, row.get("assumed_PET_gauge_um"))
            compare_row(table,idx,row,calc)
    for table in ["capture", "mission_stress"]:
        for idx, row in enumerate(owner[table]):
            calc = capture(getbase(row),row["candidate"],row["days"],
                           row["working_capacity_kg_kg"],row["monitoring_power_W"],
                           row["rate_multiplier"],row["leak_multiplier"])
            compare_row(table,idx,row,calc)
    for idx, row in enumerate(owner["choices"]):
        compare_row("choices",idx,row,choice(getbase(row),row["candidate"],row["days"]))
    for idx, row in enumerate(owner["fibres"]):
        compare_row("fibres",idx,row,fibre(getbase(row),row["fibre"]))
    for idx, row in enumerate(owner["fibre_missions"]):
        compare_row("fibre_missions",idx,row,fibre_mission(getbase(row),row["fibre"],row["days"]))
    for idx, row in enumerate(owner["creep"]):
        rate = {"SK99":7e-6, "DM20":1.3e-6}[row["fibre"]]
        pct = rate*86400*row["days"]
        calc = dict(fibre=row["fibre"],days=row["days"],stress_Pa=9e8, temperature_C=30.,
                    rate_percent_s=rate,accumulated_percent=pct,
                    max_rate_for_1pct_percent_s=1/(86400*row["days"]),
                    below_1pct_at_test_condition=pct<=1.,
                    applicable_to_resized_high_strength_film=False)
        compare_row("creep",idx,row,calc)
    for idx, row in enumerate(owner["equilibrium"]):
        q = gsta(row["T_K"],row["water_pressure_Pa"])
        compare_row("equilibrium",idx,row,dict(T_K=row["T_K"],water_pressure_Pa=row["water_pressure_Pa"],
                    q_equilibrium_kg_kg=q,usable_after_1pct_residual_and_20pct_derating=max(0.,q-.01)*.8))
    for idx, row in enumerate(trans["transport"]):
        compare_row("transport",idx,row,transport(getbase(row),row["candidate"],row["days"]))
    for idx, row in enumerate(trans["installed_WVTR_budget"]):
        a = getbase(row); d=row["days"]; f=flow(a,"SIOX")
        budget=(a["payload_kg"]-f["barrier_delta_kg"]-5-.5*24*d/108)/1.25
        release=(f["release_kg"]+.001*(5+.25*budget))*(-math.expm1(-d))
        rate=((.06*budget/1.1-release)/d-f["leak_water_kg_day"])*1000/f["area_m2"]
        compare_row("installed_WVTR_budget",idx,row,dict(bed_dry_mass_budget_kg=budget,
                    max_installed_WVTR_for_zero_payload_g_m2_day=rate))
    a=ACCOUNTS[10,"ISA","endpoint"]
    carrier=12+sealed(a,"ML3")["payload_kg"]/(4*math.pi*100*1390*1e-6)
    compare("transport_summary","R10ISA","ML3_R10_ISA_max_PET_carrier_um_for_zero_payload",
            trans["ML3_R10_ISA_max_PET_carrier_um_for_zero_payload"],carrier)
    # Independent complete bills of every route exported by owner.
    for idx, row in enumerate(csv.DictReader((I/"MASS-ACCOUNT.csv").open())):
        a=ACCOUNTS[int(row["R_m"]),row["weather"],row["account"]]
        name=row["candidate"]; d=int(row["days"]); ch=choice(a,name,d)
        f=flow(a,name); cap=capture(a,name,d)
        bill=dict(a["bill_kg"])
        bill["barrier_and_protection"]+=f["barrier_delta_kg"]
        if ch["route"]=="barrier_only":
            for field in ["bed_dry_kg","housing_kg","distribution_monitoring_kg","battery_kg"]:
                bill[field]=0.
            bill["gas"]+=ch["incremental_bill_kg"]-f["barrier_delta_kg"]
        else:
            for field in ["bed_dry_kg","housing_kg","distribution_monitoring_kg","battery_kg"]:
                bill[field]=cap[field]
            bill["gas"]=cap["charged_gas_and_retained_external_mass_kg"]
        bill.update(lift_kg=a["lift_kg"],total_charged_kg=sum(bill.values()),payload_kg=ch["payload_kg"])
        parsed={k:float(v) if k in bill else v for k,v in row.items()}
        compare_row("mass_account",idx,parsed,bill)
        compare("mass_identity",idx,"payload_kg",ch["payload_kg"],a["lift_kg"]-bill["total_charged_kg"])
    numeric=sum(isinstance(x["owner"],(int,float)) and not isinstance(x["owner"],bool) for x in CHECKS)
    summary={"checks":len(CHECKS),"numeric_checks":numeric,"mismatches":len(MISMATCH),
             "by_table":dict(collections.Counter(x["table"] for x in CHECKS)),
             "mismatches_by_field":dict(collections.Counter(x["table"]+"."+x["field"] for x in MISMATCH)),
             "input_accounts":len(ACCOUNTS),"cold_h2_K":spec["cold_h2_K"],"PCOLD_Pa":PCOLD,
             "PLIM_Pa":PLIM,"PDES_Pa":PDES,"started":js(ROOT/"START.json")["at"],
             "calculated_at":datetime.datetime.now().astimezone().isoformat(),
             "owner_executable_read_or_run":False}
    dump("COMPUTED.json",dict(COMPUTED))
    dump("ARITHMETIC-CHECKS.json",CHECKS)
    dump("ARITHMETIC-MISMATCHES.json",MISMATCH)
    dump("ARITHMETIC-SUMMARY.json",summary)
    print(json.dumps(summary,indent=2))


if __name__ == "__main__":
    main()
