"""Independent reference reconstruction and dimensional/ledger checks for MAINLINE-038."""
from pathlib import Path
from decimal import Decimal as D, localcontext
import csv
import hashlib
import json
import math

HERE=Path(__file__).resolve().parent
I=json.loads((HERE/"INPUTS.json").read_text())
R=json.loads((HERE/"RESULTS.json").read_text())
P=json.loads((HERE/"TEST-PLAN.json").read_text())
checks=[]

def check(name, observed, expected, relative=1e-9, absolute=1e-10):
    good=math.isclose(float(observed),float(expected),rel_tol=relative,abs_tol=absolute)
    checks.append(dict(name=name,observed=observed,expected=expected,passed=good))

def boolean(name, value):
    checks.append(dict(name=name,passed=bool(value)))

for f in HERE.iterdir():
    if f.suffix==".json" and f.name!="VALIDATION.json":
        json.loads(f.read_text(),parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
        boolean("strict JSON "+f.name,True)
for pin in I["pins"]:
    data=Path(pin["path"]).read_bytes()
    boolean("pin "+pin["path"],len(data)==pin["bytes"] and hashlib.sha256(data).hexdigest()==pin["sha256"])
    boolean("filed pin "+pin["path"],pin.get("matches_filed",True))

for name,pt,nu,needs in [
    ("021b",I["P2_021b"],.33,I["P2_021b"]["needed_values"]),
    ("028b",I["P2_028b_routes"]["af015_scarf"],.0752,I["P2_028b_routes"]["af015_scarf"]["needed"]),
]:
    with localcontext() as ctx:
        ctx.prec=48
        tf=D(str(pt["tf_m"]));tc=D(str(pt.get("tc_m",pt.get("core_m"))))
        E=D("290e9");Gc=D(str(R["P2_current"]["core"]["Gc_Pa"]))
        Ec=D(str(R["P2_current"]["core"]["Ec_Pa"]))
        pr=D(str(I["case"]["p0_Pa"]));rad=D(10);nuD=D(str(nu))
        demand=pr*rad/(4*tf)
        vc=2*E*tf*tc/(Gc*rad*(tf+tc)*(1-nuD*nuD).sqrt())
        sigma0=E*(tf+tc)/(rad*(1-nuD*nuD).sqrt())
        gamma=demand/((1-vc/4)*sigma0)
        b=D(".68")
        for _ in range(12):
            b-= (b*b*b+b-1)/(3*b*b+1)
        q=demand/(b*(E*Ec*tf/tc).sqrt())
        check(name+" Vc independent Decimal",float(vc),pt["Vc"])
        check(name+" gamma required",float(gamma),needs["gamma"])
        check(name+" wrinkle required",float(q),needs["wrinkle"])
        if name=="028b":
            check("face demand",float(demand),pt["face_demand_Pa"])
            check("face geometry mass",float(8*D(str(math.pi))*rad*rad*tf*D(1850)),
                  pt["masses_kg"]["faces"])
            m=pt["masses_kg"]
            check("physical mass closure",m["faces"]+m["core"]+max(m["base_joint_allowance"],m["physical_joining"])+m["systems"]+m["fixed_reserve"],I["case"]["lift0_kg"],absolute=1e-7)
            check("joint charge only excess",m["joint_excess"],m["physical_joining"]-m["base_joint_allowance"])
for n,x in enumerate(R["scaling"]):
    r=x["R_m"];tf=x["tf_um"]*1e-6;tc=x["tc_mm"]*1e-3
    v=2*(x["E_GPa"]*1e9)/(x["Gc_target_MPa"]*1e6)*(tf/tc)/(
        (r/tc)*(1+tf/tc)*math.sqrt(1-x["nu"]**2))
    check(f"scale {n} Vc",v,x["Vc"])
    check(f"scale {n} R/tc",r/tc,x["R_over_tc"])
    check(f"scale {n} imperfection",x["delta_mm"]*1e-3/(math.sqrt(3)*(tf+tc)),x["delta_over_t_eq"])
    check(f"scale {n} pressure reference",x["gamma1_reference_kPa"]*1000*x["ambient_101325Pa_max_gamma"],101325.)
    if x["unscaled_cell_dimple_SF"] is not None:
        sf=x["E_GPa"]*1e9/(1-x["nu"]**2)*(tf/.009525)**2/(I["case"]["p0_Pa"]*r/(4*tf))
        check(f"scale {n} actual unscaled-cell dimple",sf,x["unscaled_cell_dimple_SF"])
    if x["R_m"]==x["conditional_min_R_m"]:
        check(f"scale {n} one planning gauge constraint active",min(tf/25e-6,tc/.001),1.)

for rr in R["P3_022d"]:
    x=rr["source"];name=x["key"];ro=x["r_o_m"];ri=x["r_i_m"]
    a=math.pi*(ro-ri)*(ro+ri)
    ii=math.pi/4*(ro-ri)*(ro+ri)*(ro*ro+ri*ri)
    force=I["case"]["p0_Pa"]*10*x["s_m"]/(2*math.sqrt(3))
    check(name+" annular area",a,x["area_m2"])
    check(name+" annular inertia",ii,x["inertia_m4"])
    check(name+" force",force,x["force_at_pressure_1_N"])
    check(name+" arc",20*math.asin(x["s_m"]/20),x["member_length_m"])
    check(name+" tube mass",a*x["members"]*x["member_length_m"]*3100,x["mass_kg"]["tube"])
    check(name+" total closure",sum(x["mass_kg"][k] for k in ["tube","film","joint","nodes","systems","reserve","sag_lift_loss"]),I["case"]["lift0_kg"],absolute=1e-7)
    z=x["case"]["family"]=="cfrp_zylon"
    rho=1560 if z else 970
    check(name+" film mass",4*math.pi*100*x["film_total_m"]*rho,x["mass_kg"]["film"])
    se=math.pi**2*410e9*ii/(a*x["member_length_m"]**2)
    check(name+" Euler",se,x["euler_stress_Pa"])
    for y in rr["compression_sensitivities"]:
        fc=y["assumed_Fc_GPa"]*1e9
        ss=y["inherited_Perry_SF"]*force/a
        resid=(ss*ss-(fc+(1+x["eta"])*se)*ss+fc*se)/(fc*se)
        check(name+f" Perry quadratic Fc{fc}",resid,0,absolute=1e-12)
    check(name+" bulge stress",rr["small_bulge_actual_gauge_pressure_MPa"]*1e6*.3/(2*x["film_total_m"]),rr["film_effective_total_gauge_demand_GPa"]*1e9)
    if z:
        check(name+" both plies",2*x["film_per_direction_m"],x["film_total_m"])
        check(name+" joint target",force*x["target_multiplier"],x["joint"]["design_force_N"])
        check(name+" target mass scaling",x["joint"]["mass_at_multiplier_1_kg"]*x["target_multiplier"]**2,x["mass_kg"]["joint"])
        check(name+" film SF directional",3.48/rr["film_directional_ply_demand_GPa"],x["SF"]["film"])

v=R["vacuum"]
check("gas pressure-rise volume",v["pressure_rise_limit_Pa_s"]*v["full_hull_volume_m3"],v["filed_019_q_limit_Pa_m3_s"])
check("gas mass rate independent",v["derived_q_limit_Pa_m3_s"]*86400/(287.05*284.9),v["gas_mass_allowance_kg"])
check("area allocation sum",v["area_only_q_limit_Pa_m3_s_m2"]*v["full_hull_area_m2"],v["filed_019_q_limit_Pa_m3_s"])
check("seam allocation sum",v["seam_only_q_limit_Pa_m3_s_m"]*R["P2_current"]["joining"]["seam_length_m"],v["filed_019_q_limit_Pa_m3_s"])
check("small fixture derivative",v["panel_chamber_area_only_dpdt_Pa_s"]*.01,v["panel_area_only_budget_Pa_m3_s"])
check("R20 face requirement",379.2/R["P2_R20_separate_027_point"]["modes"]["face_compression"],338.744,absolute=.001)
check("R20 joint requirement",379.2/R["P2_R20_separate_027_point"]["modes"]["joint_net_section"],376.382,absolute=.001)

first=[x for x in P["tests"] if x["id"] in P["first_three"]]
for j in [0,1]:
    check("first three costs "+str(j),sum(x["initial_kUSD"][j] for x in first),P["first_three_initial_incremental_kUSD"][j])
    check("shared stock cost "+str(j),P["first_three_initial_incremental_kUSD"][j]+P["shared_Be_stock_process_allowance_kUSD"][j],P["first_three_with_shared_stock_kUSD"][j])
boolean("no purchase/contact claimed",not P["contacted_suppliers"] and not P["purchases_executed"] and not P["physical_measurements_performed"])
for name in ["OUTCOMES.csv","SHELL-SCALING.csv","P3-LATEST.csv"]:
    with (HERE/name).open() as f:
        csvrows=list(csv.DictReader(f))
    boolean("nonempty CSV "+name,len(csvrows)>0)

out=dict(schema=1,card="MAINLINE-038",checks=len(checks),
         all_passed=all(x["passed"] for x in checks),
         source_pins=len(I["pins"]),items=checks,
         limits="Arithmetic/provenance verification only; no physical tests, design optimization or qualified allowables.")
(HERE/"VALIDATION.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
print(json.dumps({k:out[k] for k in ["checks","all_passed","source_pins"]}))
if not out["all_passed"]:
    print(json.dumps([x for x in checks if not x["passed"]],indent=2))
    raise SystemExit(1)
