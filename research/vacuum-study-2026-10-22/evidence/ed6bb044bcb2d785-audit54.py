"""Independent precision, presentation, source-conditioned and balance audits."""
import collections
import csv
from decimal import Decimal, localcontext
import json
import math
from pathlib import Path
import re
import check54 as c

R = Path(__file__).resolve().parent
O = R/"inputs/owner"
own = c.js(O/"RESULTS.json")
computed = c.js(R/"COMPUTED.json")
spec = c.js(R/"SPECIFICATION.json")
c.PCOLD = spec["cold_pressure052_Pa"]
c.PDES = .8*c.PCOLD
CHECKS = []


def check(name, value, wanted, abs_tol=1e-8, rel_tol=1e-9, **context):
    numeric = isinstance(value,(int,float)) and not isinstance(value,bool)
    if numeric and isinstance(wanted,(int,float)):
        tol=abs_tol+rel_tol*abs(wanted);delta=value-wanted;passed=abs(delta)<=tol
    else:
        tol=None;delta=None;passed=value==wanted
    out=dict(check=name,observed=value,expected=wanted,tolerance=tol,delta=delta,pass_check=passed,**context)
    CHECKS.append(out)
    return out


def select(table, **where):
    rows=[x for x in computed[table] if all(x.get(k)==v for k,v in where.items())]
    assert len(rows)==1,(table,where,len(rows))
    return rows[0]


def display(label, token, expected):
    [credential]
    if "e" in token.lower():
        places=int(token.lower().split("e")[1])-len(token.lower().split("e")[0].partition(".")[2])
    else:
        places=-len(token.partition(".")[2])
    return check(label,float(token),expected,abs_tol=.5*10**places+1e-10,rel_tol=0,
                 displayed=token)


# Precision reconciliation: declared 054 design pressure is an input to this
# diagnostic only. It is not used to manufacture the independent primary results.
primary_cold=c.PCOLD
c.PCOLD=21.87136709931465
c.PDES=.8*c.PCOLD
reconciled=[]
for rec in c.js(R/"ARITHMETIC-MISMATCHES.json"):
    t=rec["table"]; ix=rec["row"]["index"]
    row=(c.js(O/"TRANSPORT.json")["transport"] if t=="transport" else own[t])[ix]
    a=c.getbase(row)
    if t in ["barriers","ground_stress","multilayer_carrier_sensitivity"]:
        scenario=row.get("scenario","")
        mult=float(scenario[5:]) if scenario.startswith("WVTRx") else 1.
        leak=10. if scenario=="leakx10" else 1.
        loss=float(scenario.split("_")[-1]) if scenario.startswith("intactPET_coating_loss_") else 0.
        calc=c.sealed(a,row["candidate"],mult,leak,loss,row.get("assumed_PET_gauge_um"))
    elif t in ["capture","mission_stress"]:
        calc=c.capture(a,row["candidate"],row["days"],row["working_capacity_kg_kg"],
                       row["monitoring_power_W"],row["rate_multiplier"],row["leak_multiplier"])
    elif t=="transport":
        calc=c.transport(a,row["candidate"],row["days"])
    else:
        raise AssertionError(t)
    field=rec["field"]
    rr=check("precision_reconciliation",calc[field],rec["owner"],table=t,row=rec["row"],field=field)
    rr["independent_primary"]=rec["checker"]
    reconciled.append(rr)
c.PCOLD=primary_cold
c.PDES=.8*c.PCOLD
c.dump("PRECISION-RECONCILIATION.json",{
    "owner_cold_limit_Pa":21.87136709931465,
    "upstream052_cold_limit_Pa":primary_cold,
    "difference_Pa":primary_cold-21.87136709931465,
    "primary_046_temperature_K":spec["cold_h2_K"],
    "owner_equivalent_temperature_K":c.root_increasing(lambda t:.05*c.psat(t),21.87136709931465,lo=250,hi=280),
    "checks":reconciled,
    "pass_count":sum(x["pass_check"] for x in reconciled),
    "fail_count":sum(not x["pass_check"] for x in reconciled),
    "classification":"finite input precision; no displayed result, route, closure or payload changes"
})

# Recreate all CSV scientific fields, allowing only the documented precision offset.
csvmap={"BARRIERS.csv":"barriers","CAPTURE.csv":"capture","CHOICES.csv":"choices",
        "FIBRES.csv":"fibres","FIBRE-MISSIONS.csv":"fibre_missions",
        "CREEP.csv":"creep","EQUILIBRIUM.csv":"equilibrium",
        "GROUND-STRESS.csv":"ground_stress","MISSION-STRESS.csv":"mission_stress",
        "CARRIER-STRESS.csv":"multilayer_carrier_sensitivity"}
csv_skipped=[]
for fn, table in csvmap.items():
    rows=list(csv.DictReader((O/fn).open()))
    check("CSV row count",len(rows),len(computed[table]),file=fn)
    for ix,(row,calc) in enumerate(zip(rows,computed[table])):
        for field,expected in calc.items():
            if field not in row:
                csv_skipped.append((fn,field))
                continue
            s=row[field]
            if expected is None:
                actual=None if s=="" else s
            elif isinstance(expected,bool):
                actual={"True":True,"False":False}.get(s,s)
            elif isinstance(expected,(int,float)):
                actual=float(s)
            else:
                actual=s
            check("CSV independent value",actual,expected,abs_tol=2e-7,rel_tol=2e-8,
                  file=fn,row=ix,field=field)

# Parse the card's eight numeric tables and compare displayed rounding exactly.
text=(O/"CARD.md").read_text()
tables=[];current=[]
for line in text.splitlines()+[""]:
    if line.startswith("|"):
        current.append([x.strip() for x in line.strip().strip("|").split("|")])
    elif current:
        tables.append(current[2:]);current=[]
assert len(tables)==8,len(tables)
for row in tables[0]:
    name=re.search(r"\[(.*?)\]",row[0]).group(1)
    rate,mass,tc,rh,_=c.CAND[name]
    display("card barrier WVTR "+name,row[1],rate)
    temp,humidity=row[2].split("/")
    display("card barrier test C "+name,temp,tc)
    display("card barrier RH "+name,humidity.strip().strip("%"),rh*100)
    display("card barrier g/m2 "+name,row[3],mass*1000)
for row in tables[1]:
    for radius,col in zip([10,12,15],row[1:]):
        b=select("barriers",R_m=radius,weather="ISA",account="endpoint",candidate=row[0])
        vals=re.findall(r"[+-]?\d+\.\d+",col)
        assert len(vals)==3
        for token,field in zip(vals,["scheduled_ground_days","scheduled_ground_cold_h2_days","payload_kg"]):
            display(f"card sealed {radius} {row[0]} {field}",token,b[field])
for row in tables[2]:
    for radius,token in zip([10,12,15],row[1:]):
        b=select("barriers",R_m=radius,weather="optimistic",account="endpoint",candidate=row[0])
        display(f"card optimistic {radius} {row[0]}",token,b["payload_kg"])
for row in tables[3]:
    d=int(row[0]);a=select("capture",R_m=10,weather="ISA",account="endpoint",candidate="SIOX",days=d)
    vals=[a["bed_dry_kg"],a["housing_kg"],5+a["battery_kg"],a["capture_system_kg"],
          a["barrier_delta_kg"],a["payload_kg"],a["regeneration_planning_2x_kWh"]]
    for j,(token,value) in enumerate(zip(row[1:],vals)):
        display(f"card SiOx capture {d}d column{j+1}",token,value)
for row in tables[4]:
    for d,token in zip([1,7,30],row[1:]):
        a=select("capture",R_m=10,weather="ISA",account="endpoint",candidate=row[0],days=d)
        display(f"card capture mass {row[0]} {d}d",token,a["capture_system_kg"])
for row in tables[5]:
    radius,weather=row[0].split();radius=int(radius[1:])
    name=row[2].split()[0];d=int(row[1])
    a=select("choices",R_m=radius,weather=weather,account="endpoint",candidate=name,days=d)
    for token,field in zip(row[3:],["capture_system_kg","incremental_bill_kg","payload_kg"]):
        display(f"card mission {radius} {weather} {name} {d}d {field}",token,a[field])
for row in tables[6]:
    for radius,weather,col in zip([10,12,15],["ISA","ISA","optimistic"],row[1:]):
        a=select("fibres",R_m=radius,weather=weather,account="endpoint",fibre=row[0])
        for token,field in zip(col.split("/"),["resized_mass_kg","resized_payload_kg"]):
            display(f"card fibre {row[0]} {radius} {weather} {field}",token,a[field])
for row in tables[7]:
    for d,token in zip([1,7,30],row[1:]):
        a=select("creep",fibre=row[0],days=d)
        display(f"card creep {row[0]} {d}d",token,a["accumulated_percent"])

base=c.ACCOUNTS[10,"ISA","endpoint"]
least=c.ACCOUNTS[10,"ISA","least052"]
headline=[
    ("area m2","1256.637",4*math.pi*100),
    ("permeation kg/day","1.256637",4*math.pi*100/1000),
    ("leak water kg/day","0.001419",c.flow(least,"B0")["leak_water_kg_day"]),
    ("total water kg/day","1.258056",c.flow(least,"B0")["water_kg_day"]),
    ("least free volume m3","4124.742",least["vacuum"]["free_volume_m3"]),
    ("least water headspace kg","1.020035",c.PLIM*least["vacuum"]["free_volume_m3"]*c.MW/(c.RG*c.T0)),
    ("least cold water target Pa","32.516516",c.PLIM),
    ("least material source kg","0.222596",least["vacuum"]["initial_material_release_water_proxy_kg"]),
    ("least crossing d","0.719991",c.sealed(least,"B0")["first_humidity_days"]),
    ("least crossing h","17.279789",24*c.sealed(least,"B0")["first_humidity_days"]),
    ("least schedule h","15.551810",24*c.sealed(least,"B0")["scheduled_ground_days"]),
    ("colder least crossing h","11.47",24*c.sealed(least,"B0")["cold_h2_first_days"]),
    ("least pressure crossing h","450.24",24*c.sealed(least,"B0")["total_pressure_days"]),
    ("endpoint crossing h","17.384694",24*c.sealed(base,"B0")["first_humidity_days"]),
    ("333K uptake percent","8.623",100*c.gsta(333,c.PDES)),
    ("333K usable percent","6.099",100*(c.gsta(333,c.PDES)-.01)*.8),
    ("bed final equilibrium Pa","10.2828",c.transport(base,"SIOX",7)["bed_end_equilibrium_Pa"]),
    ("R10 conductance m3/h","277",c.transport(base,"SIOX",7)["effective_water_conductance_required_m3_h"]),
    ("R10 drive Pa","7.21",c.PDES-c.transport(base,"SIOX",7)["bed_end_equilibrium_Pa"]),
    ("R10 peak heat W","16.54",c.transport(base,"SIOX",7)["peak_adsorption_heat_W"]),
    ("R10 ideal radiation m2","0.235",c.transport(base,"SIOX",7)["ideal_radiating_area_m2"]),
    ("R10 doubled WVTR payload","-15.09",c.capture(base,"SIOX",7,multiplier=2)["payload_kg"]),
    ("R10 four percent payload","-9.69",c.capture(base,"SIOX",7,capacity=.04)["payload_kg"]),
    ("R10 five watt payload","-5.88",c.capture(base,"SIOX",7,power=5)["payload_kg"]),
    ("R10 7d WVTR budget","0.08551",computed["installed_WVTR_budget"][1]["max_installed_WVTR_for_zero_payload_g_m2_day"]),
    ("R10 30d WVTR budget","0.01614",computed["installed_WVTR_budget"][2]["max_installed_WVTR_for_zero_payload_g_m2_day"]),
    ("same gauge aramid SF","0.517",c.fibre(base,"aramid_yarn_limit")["same_gauge_film_SF"]),
    ("same gauge aramid60 SF","0.310",c.fibre(base,"aramid_60pct_laminate")["same_gauge_film_SF"]),
    ("SK99 1pct creep h","39.68",1/(7e-6*3600)),
    ("DM20 1pct creep h","213.68",1/(1.3e-6*3600)),
    ("hot film C","48.79",c.WALLTEMP-273.15),
    ("ML3 max carrier um","28.07",c.js(O/"TRANSPORT.json")["ML3_R10_ISA_max_PET_carrier_um_for_zero_payload"]),
]
for label,token,expected in headline:
    display("card inline "+label,token,expected)

# Explicit report-only rounding discrepancy; card is checked separately.
display("report body R12 ISA FOIL30 payload kg","47.35",
        select("choices",R_m=12,weather="ISA",account="endpoint",candidate="FOIL30",days=30)["payload_kg"])

# Decimal thermodynamic evaluation, completely separate numerical representation.
decimal_rows=[]
with localcontext() as ctx:
    ctx.prec=60
    for row in own["equilibrium"]:
        t=Decimal(str(row["T_K"]));p=Decimal(str(row["water_pressure_Pa"]));rg=Decimal("8.31446261815324")
        hs=[Decimal(x) for x in ["-46600","-125000","-193600","-272200"]]
        ss=[Decimal(x) for x in ["-53.7","-221.1","-356.7","-567.5"]]
        terms=[(-h/(rg*t)+s/rg).exp()*(p/Decimal(100000))**n for n,(h,s) in enumerate(zip(hs,ss),1)]
        q=Decimal(".21")/4*sum(n*x for n,x in enumerate(terms,1))/(1+sum(terms))
        decimal_rows.append(dict(T_K=float(t),p_Pa=float(p),q_decimal=str(q)))
        check("60-digit GSTA",float(q),row["q_equilibrium_kg_kg"],abs_tol=1e-14,rel_tol=1e-12)
c.dump("DECIMAL-GSTA.json",decimal_rows)

# All capture rows must satisfy analytical sizing and mass/energy identities.
for table in ["capture","mission_stress"]:
    for ix,row in enumerate(computed[table]):
        check("bed load margin",row["working_capacity_kg_kg"]*row["bed_dry_kg"],
              1.1*row["captured_water_kg"],table=table,row=ix)
        check("capture bill",row["capture_system_kg"],sum(row[k] for k in
              ["bed_dry_kg","housing_kg","distribution_monitoring_kg","battery_kg"]),table=table,row=ix)
        check("reserve accounts for water",row["reserve_used_kg"],
              c.getbase(row)["vacuum"]["initial_gas_kg"]+
              c.flow(c.getbase(row),row["candidate"],row["rate_multiplier"],row["leak_multiplier"])["dry_kg_day"]*row["days"]+
              row["external_water_retained_kg"]+row["bed_initial_water_kg"],table=table,row=ix)

# Source-conditioned aramid moisture sensitivity, not an installed moisture forecast.
moisture=[]
for a in c.ACCOUNTS.values():
    for name in ["aramid_yarn_limit","aramid_60pct_laminate"]:
        fr=c.fibre(a,name)
        for d in [1,7,30]:
            old=c.fibre_mission(a,name,d)
            f=c.flow(a,"MET")
            vol=a["vacuum"]["free_volume_m3"]-fr["resized_mass_kg"]/1440+a["bill_kg"]["PBO_two_plies"]/1560
            n0=10*vol/(c.RG*c.T0)
            carried=.035*fr["resized_mass_kg"]
            release=max(carried,f["release_kg"])
            def pressure(t):
                return (n0+f["dry_mol_day"]*t+
                        (f["water_kg_day"]*t+release*(-math.expm1(-t)))/c.MW)*c.RG*c.THOT/vol
            charged=max(a["bill_kg"]["gas"],n0*c.MEANMW+(f["dry_kg_day"]+f["water_kg_day"])*d+carried)
            payload=fr["resized_payload_kg"]-f["barrier_delta_kg"]-(charged-a["bill_kg"]["gas"])
            moisture.append(c.ident(a,fibre=name,days=d,moisture_fraction=.035,
                            source="DuPont Kevlar technical guide Table I-1, 24 C/55% RH",
                            projection="Full release in one-day proxy; not coupled sorption prediction",
                            carried_kg=carried,pressure_Pa=pressure(d),
                            scheduled_pressure_interval_days=.9*c.root_increasing(pressure,.01*c.P0),
                            pressure_screen_pass=pressure(d)<=.01*c.P0,
                            payload_kg=payload,owner_1pct_pressure_Pa=old["pressure_Pa"],
                            owner_1pct_payload_kg=old["payload_kg"],
                            payload_delta_kg=payload-old["payload_kg"]))
c.dump("ARAMID-MOISTURE-SENSITIVITY.json",moisture)

critical={
    "r10_SIOX":[c.capture(base,"SIOX",d) for d in [1,7,30]],
    "r10_transport7":c.transport(base,"SIOX",7),
    "333K_capacity":dict(equilibrium=c.gsta(333,c.PDES),after_initial_and_derating=.8*(c.gsta(333,c.PDES)-.01)),
    "353K_capacity":dict(equilibrium=c.gsta(353,c.PDES),after_initial_and_derating=.8*(c.gsta(353,c.PDES)-.01)),
    "r10_7d_WVTR_fraction_margin":computed["installed_WVTR_budget"][1]["max_installed_WVTR_for_zero_payload_g_m2_day"]/.08-1,
    "r10_30d_required_rate_fraction_of_coupon":computed["installed_WVTR_budget"][2]["max_installed_WVTR_for_zero_payload_g_m2_day"]/.08,
    "aramid_moisture":dict(rows=len(moisture),pressure_failures=sum(not x["pressure_screen_pass"] for x in moisture),
                           max_abs_payload_change=max(abs(x["payload_delta_kg"]) for x in moisture),
                           max_pressure_Pa=max(x["pressure_Pa"] for x in moisture)),
    "owner_report_foil30_correct_kg":select("choices",R_m=12,weather="ISA",account="endpoint",candidate="FOIL30",days=30)["payload_kg"],
}
c.dump("CRITICAL-RESULTS.json",critical)
c.dump("AUDIT-CHECKS.json",CHECKS)
bad=[x for x in CHECKS if not x["pass_check"]]
c.dump("AUDIT-DIFFERENCES.json",bad)
summary={"checks":len(CHECKS),"pass_count":len(CHECKS)-len(bad),"difference_count":len(bad),
         "differences_by_check":dict(collections.Counter(x["check"] for x in bad)),
         "by_check":dict(collections.Counter(x["check"] for x in CHECKS)),
         "CSV_absent_fields":sorted(set(csv_skipped))}
c.dump("AUDIT-SUMMARY.json",summary)
print(json.dumps(summary,indent=2))
print("Differences",json.dumps(bad,indent=2))
