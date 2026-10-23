#!/usr/bin/env python3
"""Independent scalar accounts, thermal convergence, subset bounds and dry costs."""
import hashlib
import itertools
import json
import math
from collections import defaultdict
from dataclasses import replace
from pathlib import Path
import numpy as np
import model48 as m
from thermal48 import evaluate

B=Path(__file__).resolve().parent
tables=json.loads((B/"THERMAL-TABLES.json").read_text())
profiles={x["id"]:x for x in json.loads((B/"COATINGS.json").read_text())}
stats=defaultdict(lambda:dict(count=0,failed=0,max_abs_error=0.))
failures=[]
def check(name,good,evidence=None):
    stats[name]["count"]+=1
    if not good:
        stats[name]["failed"]+=1
        failures.append(dict(name=name,evidence=evidence))
def near(name,value,expected,atol=1e-6,rtol=1e-8):
    error=abs(value-expected)
    stats[name]["max_abs_error"]=max(stats[name]["max_abs_error"],error)
    check(name,error<=atol+rtol*abs(expected),
          dict(actual=value,expected=expected,error=error))

rows=[]
for name in ["MLCCAg","CCAg","AgFEP05","AgFEP1"]:
    data=json.loads((B/f"RESULTS-{name}.json").read_text())
    assert data["complete"], name
    check("complete profile matrix",len(data["rows"])==108,name)
    expected=set(itertools.product([10,12,15],["ISA","optimistic","both"],
                                   [False,True],["dry_gas","bake70","desiccant"],[.1,0.]))
    observed={(x["R_m"],x["weather"],x["floor"],x["drying"],
               x["external_water_kg_m2"]) for x in data["rows"]}
    check("unique expected configurations",expected==observed,name)
    rows.extend(data["rows"])

points=[]
seen=set()
for row in rows:
    for p in ([t["solution"] for t in row["least"]["endpoint_trials"] if t["solution"]]
              +row["least"].get("ties",[])):
        key=json.dumps([p["geometry"],p["settings"],p["mask"],p["usage"]],sort_keys=True)
        if key not in seen:
            points.append(p)
            seen.add(key)
for p in points:
    r=p["R_m"];s=p["settings"];b=p["bill_kg"];v=p["vacuum"];pr=p["properties"]
    tf=p["geometry"]["tf_m"];tc=p["geometry"]["tc_m"]
    a=4*math.pi*r*r;vol=4*math.pi*r**3/3;ratio=s["scarf_ratio"]
    line=a/(.6096-ratio*tf)+a/(1.8288-ratio*tf)
    film=2*a*pr["film_kg_m2_interface"]
    seam=line*(2*tf*math.sqrt(1+ratio**2)*.07+.0005*tc*500+.002)
    core=a*tc*m.C["rho"];face=2*a*1850*tf
    water=s["moisture_scale"]*(s["adhesive_water_fraction"]*film+
           s["core_water_fraction"]*core+
           s["primer_water_fraction"]*a*s["structural_primer_kg_m2"]+
           a*s["finish_water_kg_m2"]+.01*seam)
    inventory=.1*(.0485*film+.001*core+.01*seam)
    near("face mass",b["faces"],face)
    near("core mass",b["core"],core)
    near("explicit joining",p["actual_joining"]["total"],film+seam)
    near("joining floor charged once",b["charged_joining"],
         max(film+seam,.05*(face+core)) if s["floor"] else film+seam)
    near("water separate exterior",b["water"],a*s["external_water_kg_m2"])
    near("extra material water",b["absorbed_water"],water)
    near("primer separate charge",b["structural_primer"],a*s["structural_primer_kg_m2"])
    near("coating mass",b["coating"],a*s["coating"])
    near("ledger closure",sum(b.values())+p["signed_payload_kg"],m.L0*(r/10)**3)
    near("system reserve",b["systems"],100)
    initial=10*vol/(m.RU*m.T0)*m.DRY_M
    e=6000 if s["weather"]=="both" else 1000
    molefrac=e/m.P0
    leakmol=(line*.001+.01)*.1/(m.RU*m.T0)*86400
    area_path=line*(.07/1250)/(tf*math.sqrt(1+ratio**2))
    permmol=10*3.34645e-16*area_path*m.P0*86400
    ingress=(leakmol+permmol)*((1-molefrac)*m.DRY_M+molefrac*.01801528)
    capture=s["desiccant_capture_fraction"] if s["desiccant"] else 0
    released=(inventory+water)*(1-math.exp(-1))*(1-capture)
    pressure=(initial/m.DRY_M+(leakmol+permmol)*(1-molefrac*capture)+
              released/.01801528)*m.RU*320/vol
    near("vapor pressure",v["hot_pressure_24h_upper_Pa"],pressure)
    near("nominal release",v["original_nominal_volatile_release_kg"],inventory*(1-math.exp(-1)))
    near("gas without desorption double charge",v["gas_aboard_counted_kg"],initial+ingress)
    near("gas max reserve",b["gas"],max(.01*m.L0*(r/10)**3,initial+ingress))
    if s["desiccant"]:
        capacity=1.1*(inventory+water)+.1*(r/10)**3
        near("sorbent and cartridge",b["desiccant"],capacity/s["desiccant_capacity_kg_kg"]+2)
        incomingwater=(leakmol+permmol)*molefrac*.01801528
        check("bed covers total inventory and 24h water ingress",capacity>=inventory+water+incomingwater,
              dict(capacity=capacity,required=inventory+water+incomingwater))
    else:
        near("no sorbent charged",b["desiccant"],0)
    table=tables[s["finish_id"]][str(r)]
    grid=np.log(table["tc_m"])
    hot=float(np.interp(math.log(tc),grid,table["max_outer_K"]))
    cold=float(np.interp(math.log(tc),grid,table["min_outer_K"]))
    deps=12.3e-6*1.002*max(abs(s["cure_temperature_K"]-hot),
                          abs(s["cure_temperature_K"]-cold))
    kb=.5*67e9*m.C["rho"]/2700
    tau=deps*math.sqrt(2*kb*m.C["Gc_Pa"])
    residual=kb*12.3e-6*1.002*max(s["cure_temperature_K"]-cold,0)*tc/(2*tf)
    near("free edge shear",pr["thermal_interface_shear_Pa"],tau)
    near("balanced cure compression",pr["added_cure_compression_Pa"],residual)
    E=pr["E_Pa"];nu=s["nu"];sig=p["load_pressure_Pa"]*r/(4*tf)
    sig0=E*(tc+tf)/(r*math.sqrt(1-nu*nu))
    crimp=m.C["Gc_Pa"]*(tc+tf)**2/(2*tf*tc)
    vc=sig0/crimp;kc=1-vc/4 if vc<=2 else 1/vc
    crimpd=sig+pr["added_gradient_stress_Pa"]+pr["added_bending_stress_Pa"]
    demand=crimpd+residual
    values=dict(
        global_buckling=pr["gamma"]*kc*sig0/sig,
        face_compression=pr["Fcy_Pa"]/demand,
        core_shear_crimping=crimp/crimpd,
        core_crush=2*m.C["crush_Pa"]/p["load_pressure_Pa"],
        face_wrinkling=m.BETA*pr["Q"]*math.sqrt(E*m.C["Ec_Pa"]*tf/tc)/demand,
        intracell_dimpling=E*(tf/m.C["s_cell_m"])**2/((1-nu*nu)*demand),
        scarf_average_shear_screen=10e6/(demand*ratio/(1+ratio**2)),
        core_cell_wall_yield_screen=227.53e6/(1.2*67e9*deps),
        thermal_core_interface_screen=25*6894.757293168361/tau)
    for name,value in values.items():
        near("mode "+name,p["modes"][name],value,atol=1e-8)
    check("all retained scalar constraints",min(values.values())>=1-3e-7)
    check("service pressure",pressure<=.01*m.P0*(1+1e-8))
    check("installed hull SF unknown",p["overall_installed_hull_SF"] is None)

# Removing all new charges with the ORIGINAL thermal table reproduces 040.
m.THERMAL=json.loads((m.B/"THERMAL-TABLE.json").read_text())
old=json.loads((m.B/"RESULTS.json").read_text())
for row in old["rows"]:
    if row["R_m"] not in [10,12,15] or row["pad"]!="heavy70" or not row["vented"]:
        continue
    p=row["two_factor_endpoint"]
    new=m.optimize(row["R_m"],11,1,m.Settings(**p["settings"]),n=900)
    near("040 regression",new["signed_payload_kg"],p["signed_payload_kg"],atol=.002)

direct_checks=[]
search=[]
costs=[]
service=[]
bounds=[]
for profile in ["MLCCAg","CCAg","AgFEP05","AgFEP1"]:
    m.THERMAL=tables[profile]
    c=profiles[profile]
    for r in [10,12,15]:
        primary=[x for x in rows if x["profile"]==profile and x["R_m"]==r
                 and x["drying"]=="bake70" and x["external_water_kg_m2"]==.1]
        ps=[x["two_factor_endpoint"] for x in primary]
        tcs=[p["geometry"]["tc_m"] for p in ps]
        direct=evaluate(r,tcs,n=256,alpha_out=c["alpha"],epsilon_out=c["epsilon"])
        table=m.THERMAL[str(r)];grid=np.log(table["tc_m"])
        for j,p in enumerate(ps):
            for q in ["gradient_K","curvature_temperature_K","swing_K"]:
                charged=1.002*np.interp(math.log(tcs[j]),grid,table[q])
                value=direct[q][j]
                check("thermal guard "+q,charged>=value,
                      dict(profile=profile,r=r,charged=charged,direct=value))
                direct_checks.append(dict(profile=profile,R_m=r,quantity=q,
                                          charged=charged,direct_256=value))
        check("thermal energy balance",max(direct[k]["max_energy_residual_W_m2"]
              for k in ["day_diagnostics","night_diagnostics"])<1e-6)
        # Denser geometry searches at every primary endpoint and least point.
        for row in primary:
            for label,p in [("endpoint",row["two_factor_endpoint"]),("least",row["least"]["least"])]:
                if p is None: continue
                fine=m.optimize(r,p["mask"],p["usage"],m.Settings(**p["settings"]),n=2200)
                delta=fine["signed_payload_kg"]-p["signed_payload_kg"]
                check("denser geometry search",abs(delta)<.02,dict(id=row["id"],track=label,delta_kg=delta))
                search.append(dict(id=row["id"],track=label,delta_kg=delta))
    for row in [x for x in rows if x["profile"]==profile]:
        p=row["two_factor_endpoint"];s=m.Settings(**p["settings"])
        r=row["R_m"];tc=p["geometry"]["tc_m"];tf=p["geometry"]["tf_m"]
        v=p["vacuum"];vol=p["geometry"]["volume_m3"]
        free=4*np.pi*(r-2*tf-tc)**3/3+v["pore_volume_m3"]
        corrected=10*320/m.T0+(v["hot_pressure_24h_upper_Pa"]-10*320/m.T0)*vol/free
        zero=m.vacuum(r,tf,tc,p["actual_joining"],replace(s,desiccant_capture_fraction=0))
        unconditioned=zero["hot_pressure_24h_upper_Pa"]+9*v["original_nominal_volatile_release_kg"]/.01801528*m.RU*320/vol
        service.append(dict(id=row["id"],free_volume_m3=float(free),
                            refined_pressure_Pa=float(corrected),
                            no_capture_pressure_Pa=float(zero["hot_pressure_24h_upper_Pa"]),
                            no_nominal_conditioning_pressure_Pa=float(unconditioned)))
        check("refined cavity pressure",corrected<.01*m.P0)
        check("no capture service sensitivity",zero["hot_pressure_24h_upper_Pa"]<.01*m.P0)
        # The E/Fcy optimism axis is not monotone under thermal stress. Bound
        # every lower-cardinality subset with E_full capacity and E_today heat.
        # External water is a constant debit; do this for both conditions.
        count=row["least"]["minimum_axis_count"]
        for trial in row["least"]["endpoint_trials"]:
            mask=trial["mask"]
            if not mask&4 or (count is not None and mask.bit_count()>=count):
                continue
            favorable=m.optimize(r,mask,1,replace(s,thermal_modulus_Pa=m.F["E_today_Pa"]),n=700)
            value=None if favorable is None else favorable["signed_payload_kg"]
            bounds.append(dict(id=row["id"],mask=mask,payload_upper_kg=value))
            check("relaxed E excludes fewer axes",value is None or value<0,
                  dict(id=row["id"],mask=mask,payload_upper_kg=value))
        if row["weather"]!="ISA" or not row["floor"] or row["external_water_kg_m2"]!=.1:
            continue
        original=replace(s,moisture_scale=1)
        initial_by=m.material_water(r,tc,p["actual_joining"],original)
        remaining_by=m.material_water(r,tc,p["actual_joining"],s)
        initial_water=sum(initial_by.values());remaining=sum(remaining_by.values())
        # Explicit engineering assumptions; ideal energy excludes ovens,
        # supports, pumping, desorption enthalpy and all thermal losses.
        dt=343.15-m.T0
        heatcap=(p["bill_kg"]["faces"]*1825+p["bill_kg"]["core"]*900+
                 p["actual_joining"]["total"]*1000+
                 (p["bill_kg"]["coating"]+p["bill_kg"]["structural_primer"])*1000)
        ideal=(heatcap*dt+max(initial_water-remaining,0)*2.45e6)/3.6e6
        purge_volume=5*vol
        nitrogen=purge_volume*m.P0*.0280134/(m.RU*m.T0)
        costs.append(dict(id=row["id"],profile=profile,R_m=r,route=row["drying"],
            water_initial_by_material_kg=initial_by,
            water_remaining_by_material_kg=remaining_by,
            material_water_initial_kg=initial_water,material_water_remaining_kg=remaining,
            material_water_removed_ground_kg=initial_water-remaining,
            external_water_remaining_kg=p["bill_kg"]["water"],
            sorbent_and_cartridge_kg=p["bill_kg"]["desiccant"],
            sorbent_capacity_kg=v["desiccant_water_capacity_kg"],
            ideal_bake_lower_bound_kWh=float(ideal) if row["drying"]=="bake70" else None,
            dry_gas_five_exchanges_m3=float(purge_volume) if row["drying"]=="dry_gas" else None,
            dry_gas_nitrogen_kg=float(nitrogen) if row["drying"]=="dry_gas" else None,
            external_water_max_for_endpoint_float_kg_m2=.1+p["signed_payload_kg"]/(4*np.pi*r*r),
            signed_payload_kg=p["signed_payload_kg"]))
    print(profile,"audited",flush=True)

for pinfile in ["MODEL-PINS.json","UPSTREAM-PINS.json"]:
    data=json.loads((B/pinfile).read_text())
    pins=data if isinstance(data,list) else data.get("pins",[])
    for pin in pins:
        path=Path(pin.get("path",pin.get("source","")))
        if path.is_file() and "sha256" in pin:
            value=path.read_bytes()
            check("immutable input pin",hashlib.sha256(value).hexdigest()==pin["sha256"]
                  and len(value)==pin["bytes"],str(path))

m.dump(B/"THERMAL-VALIDATION.json",direct_checks)
m.dump(B/"SEARCH-VALIDATION.json",search)
m.dump(B/"SUBSET-BOUNDS.json",bounds)
m.dump(B/"SERVICE-AUDIT.json",service)
m.dump(B/"DRYING-COSTS.json",dict(
    tag="PROJECTION",rows=costs,
    heat_capacity_assumptions_J_kg_K=dict(Be=1825,Al_core=900,polymer_and_coating=1000),
    evaporation_energy_assumption_J_kg=2.45e6,
    bake_temperature_K=343.15,initial_temperature_K=m.T0,
    airborne_fraction_after_five_ideal_mixed_exchanges=math.exp(-5),
    dewpoint_at_1kPa_K=1838.675/(5.40221-math.log10(.01))+31.737,
    notes=[
        "No currency cost or achieved bake time is sourced.",
        "Energy is an ideal lower bound, excluding tooling, vacuum work, losses and desorption binding energy.",
        "Five sphere-volume exchanges are a ground-enclosure assumption; panel/glovebox processing changes gas demand.",
        "Desiccant changes phase distribution, not total onboard water mass.",
        "All onboard systems retain their original 100 kg reserve; sorbent is charged additionally."
    ]))
m.dump(B/"VALIDATION.json",dict(
    passed=not failures,configurations=len(rows),unique_points=len(points),
    checks=sum(v["count"] for v in stats.values()),failed=failures,summary=dict(stats)))
print(json.dumps(dict(passed=not failures,configurations=len(rows),points=len(points),
                      checks=sum(v["count"] for v in stats.values()),failures=failures),indent=2))
if failures:
    raise SystemExit(1)
