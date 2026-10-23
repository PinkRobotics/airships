#!/usr/bin/env python3
"""Independent scalar Decimal pressure/mass verification; scientific plot.

Does not import compute.py or frame.py. Dense optimiser comparisons are recorded
by those programs; this verifies delivered geometry using pressure capacities.
"""
import hashlib
import json
import math
import os
from decimal import Decimal as D, getcontext
from pathlib import Path

ROOT=Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR",str(ROOT/"mpl-cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

getcontext().prec=45
I=json.loads((ROOT/"INPUTS.json").read_text())
R=json.loads((ROOT/"RESULTS.json").read_text())
F=json.loads((ROOT/"FRAME.json").read_text())
CAT=json.loads((ROOT/"CATALOGUE.json").read_text())
PI=D("3.141592653589793238462643383279502884197169399")
NU=D(str(I["case"]["nu"]))
P=D(str(I["case"]["p0_Pa"]))
T=D(str(I["case"]["T0_K"]))
L0=D(str(I["case"]["lift0_kg"]))
q=D(".68")
for _ in range(20): q-=(q**3+q-1)/(3*q*q+1)


def dec(x):return D(str(x))


def capacities(r,tf,tc,core,E,sig,cw,gamma=None,eta=1):
    r,tf,tc,E,sig,cw=map(dec,(r,tf,tc,E,sig,cw))
    gc,ec,crush,cell=[dec(core[k]) for k in ("Gc_Pa","Ec_Pa","crush_Pa","s_cell_m")]
    h=tf+tc
    s0=E*h/(r*(1-NU**2).sqrt())
    sc=h*h*gc/(2*tf*tc)
    vc=s0/sc
    kc=1/vc if vc>=2 else 1-vc/4
    gamma=dec(gamma)
    return dict(global_buckling=4*tf*gamma*kc*s0/r,
                face_compression=4*tf*sig/r,
                core_crush=2*crush,
                core_shear_crimping=2*h*h*gc/(r*tc),
                face_wrinkling=4*q*cw*(E*ec*tf**3/tc).sqrt()/r,
                intracell_dimpling=4*E*tf**3/((1-NU*NU)*cell**2*r),
                joint_net_section=4*dec(eta)*sig*tf/r)


max_pressure_error=0.
max_mass_error=0.
p2_checked=0
all_p2=[x for x in R["P2"] if x["feasible"]]
all_p2 += [x["payload_at_SF1"]["point"] for x in R["P2"] if x["payload_at_SF1"]["reaches_SF1"]]
all_p2 += [x for x in CAT["best_points"] if x["feasible"]]
all_p2 += [x["family_payload_at_SF1"]["point"] for x in CAT["best_points"]
           if x["feasible"] and x["family_payload_at_SF1"]["reaches_SF1"]]
core_map={c["name"]:c for c in [*I["cores"].values(),*I["aluminium_candidates"]]}
for x in all_p2:
    c=core_map[x["core"]]; sc=I["scenarios"][x["scenario"]]; me=I["mechanical_sets"][x["mechanical"]]
    cap=capacities(x["radius_m"],x["tf_m"],x["tc_m"],c,me["E_Pa"],me["sigma_Pa"],
                   me["wrinkle_coefficient"],x["gamma"],sc["joint_efficiency"])
    pressure=P*(1+dec(sc["pressure_swing_fraction"]))
    for k,v in cap.items():
        err=abs(float(v/pressure)-x["modes"][k])/max(1.,abs(x["modes"][k]))
        max_pressure_error=max(max_pressure_error,err)
        assert err<1e-10,(x["radius_m"],x["family"],k,err)
    area=4*PI*dec(x["radius_m"])**2
    faces=2*area*dec(I["face"]["rho"])*dec(x["tf_m"])
    core=area*dec(c["rho"])*dec(x["tc_m"])
    structural=faces+core
    if x["mass_model"]=="fixed_areal":
        joining=area*dec(sc["total_joining_kg_m2_frozen_020"])
    else:
        length=area*(1/dec(sc["panel_a_m"])+1/dec(sc["panel_b_m"]))
        joining=length*(2*dec(I["face"]["rho"])*dec(x["tf_m"])*dec(sc["splice_width_m"])
                        +2*dec(sc["film_kg_m2_per_interface"])*dec(sc["splice_width_m"])
                        +1100*dec(sc["core_gap_m"])*dec(x["tc_m"])
                        +1100*dec(sc["sealant_area_m2"]))+2*area*dec(sc["film_kg_m2_per_interface"])
    lift=L0*(dec(x["radius_m"])/10)**3
    hot=T+dec(sc["temperature_rise_K"])
    moist=lift*((1-dec(sc["pressure_swing_fraction"]))-D(".378")*dec(sc["water_vapour_Pa"])/P)*T/hot
    physical=structural+max(D(".05")*structural,joining)+max(D(100),dec(x["environment"]["systems"]["total_kg"]))
    physical+=area*(1000*dec(sc["water_film_m"])+dec(sc["contamination_kg_m2"])+dec(sc["extra_coating_kg_m2"]))
    physical+=D(".01")*lift+dec(x["payload_kg"])
    err=abs(float(physical-moist))
    max_mass_error=max(max_mass_error,err)
    assert err<2e-7,(x["radius_m"],x["family"],err)
    p2_checked+=1

reproductions=[]
pts=[I["reference_021"]["main"]["floating_point"]]
pts += [I["reference_021"]["main"]["families"][f]["full_set_max_least"]["point"] for f in ("aluminium","aramid")]
for p in pts:
    c=I["cores"][p["family"]]
    full=p["at_full_named_set"]
    cap=capacities(10,p["tf_m"],p["core_m"],c,p["face_E_Pa_at_full_set"],379.2e6,.82,full["gamma"])
    errors=[abs(float(cap[k]/P)-v) for k,v in full["sfs"].items()]
    assert max(errors)<1e-10
    reproductions.append(dict(core=p["core"],max_SF_error=max(errors),passed=True))

# Rebuild 020's joining masses at its frozen 009c5 dimensions.
ref=I["reference_020"]["baseline"]
tf=D("0.000752430055433027");tc=D("0.020642305866854553")
join_checks=[]
for label,sc in I["scenarios"].items():
    area=400*PI
    mu=(2*1850*tf*dec(sc["splice_width_m"])+2*dec(sc["film_kg_m2_per_interface"])*dec(sc["splice_width_m"])
        +1100*dec(sc["core_gap_m"])*tc+1100*dec(sc["sealant_area_m2"]))
    mass=area*(1/dec(sc["panel_a_m"])+1/dec(sc["panel_b_m"]))*mu+2*area*dec(sc["film_kg_m2_per_interface"])
    expected=area*dec(sc["total_joining_kg_m2_frozen_020"])
    err=abs(float(mass-expected))
    assert err<1e-8
    join_checks.append(dict(scenario=label,total_kg=float(mass),mass_error_kg=err))

frame_error=0.
frame_mass_error=0.
frame_rows=F["P3"]+[p["payload_at_SF1"]["point"] for p in F["P3"] if p["payload_at_SF1"]["reaches_SF1"]]
for x in frame_rows:
    if not x["feasible"]:continue
    r,s,ro,ri,a=map(dec,(x["radius_m"],x["s_m"],x["ro_m"],x["r_i_m"],x["A_m2"]))
    inertia=PI*(ro**4-ri**4)/4
    E=D("410e9");sig=dec(x["sigma_Pa"])
    pc=P*(1+dec(I["scenarios"][x["scenario"]]["pressure_swing_fraction"]))
    axial=pc*r*s/(2*a)
    se=PI**2*E*inertia/(a*s*s)
    eta=s*ro*a/(1000*inertia)
    phi=(sig+(1+eta)*se)/2
    perry=phi-(phi**2-sig*se).sqrt()
    expected=dict(compression=2*sig*a/(r*s*pc),Euler=2*PI**2*E*inertia/(r*s**3*pc),
                  local_tube_buckling=2*D(".6")*E*(ro-ri)*a/(ro*r*s*pc),
                  film=2*D("1.5e9")*D(".00008")/(s*pc),Perry=perry/axial,
                  global_lattice=D(".2")*4*D("1.5").sqrt()*E*(inertia*a).sqrt()/(s*r*r*pc))
    er=max(abs(float(v)-x["modes"][k]) for k,v in expected.items())
    frame_error=max(frame_error,er)
    assert er<1e-9
    sc=I["scenarios"][x["scenario"]];area=4*PI*r*r
    lift=L0*(r/10)**3
    moist=lift*((1-dec(sc["pressure_swing_fraction"]))-D(".378")*dec(sc["water_vapour_Pa"])/P)*T/(T+dec(sc["temperature_rise_K"]))
    mass=sum(dec(x["masses_kg"][k]) for k in ("film","nodes","tubes","joints"))
    mass+=max(D(50),dec(x["environment"]["systems"]["total_kg"]))
    mass+=area*(1000*dec(sc["water_film_m"])+dec(sc["contamination_kg_m2"]))
    mass+=D(".01")*lift+dec(x["payload_kg"])
    er=abs(float(mass-moist));frame_mass_error=max(frame_mass_error,er)
    assert er<2e-7

pin_errors=[]
for p in I["pins"]:
    b=Path(p["path"]).read_bytes()
    if len(b)!=p["bytes"] or hashlib.sha256(b).hexdigest()!=p["sha256"]:
        pin_errors.append(p["path"])
assert not pin_errors,pin_errors
valid=dict(schema=1,passed=True,method="Independent 45-digit scalar pressure capacities and physical wet/hot mass balance; no solver imports.",
           p2_points_including_payload=p2_checked,max_P2_relative_SF_error=max_pressure_error,
           max_P2_mass_error_kg=max_mass_error,source021_reproductions=reproductions,
           source020_joining_reproductions=join_checks,source011b_error=F["reproduction_max_error"],
           frame_points_including_payload=len(frame_rows),max_P3_absolute_SF_error=frame_error,
           max_P3_mass_error_kg=frame_mass_error,pins_reverified=len(I["pins"]),
           P2_dense_grid_checks=len(R["dense_grid_checks"]),P3_dense_grid_checks=len(F["dense_checks"]),
           catalogue_geometry_searches=len(CAT["all_scores"]),catalogue_dense_grid_checks=len(CAT["dense_checks"]),
           limitations="Arithmetic and search checks do not validate physical knockdown, brittle strength, joints, leakage or fabrication.")
(ROOT/"VALIDATION.json").write_text(json.dumps(valid,indent=2)+"\n")

plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
fig,axs=plt.subplots(2,2,figsize=(12,8.2),constrained_layout=True)
colors={"aluminium":"#126d99","aramid":"#bd6a27"}
for fam in ("aluminium","aramid"):
    for mech,style in (("chain_design","--"),("full_021","-")):
        rows=[p for p in R["P2"] if p["mass_model"]=="coupled" and p["scenario"]=="optimistic" and p["family"]==fam and p["mechanical"]==mech]
        axs[0,0].plot([p["radius_m"] for p in rows],[p["least_SF"] for p in rows],style,marker="o",
                      color=colors[fam],label=f"{fam}, {'021 full' if mech=='full_021' else 'design'}")
    for mass,style in (("coupled","-"),("fixed_areal",":")):
        rows=[p for p in R["P2"] if p["mass_model"]==mass and p["scenario"]=="optimistic" and p["family"]==fam and p["mechanical"]=="full_021"]
        axs[0,1].plot([p["radius_m"] for p in rows],[100*p["reserve_fraction"] for p in rows],style,marker="o",
                      color=colors[fam],label=f"{fam}, {'resized seams' if mass=='coupled' else 'frozen kg/m²'}")
axs[0,0].axhline(1,color="#444",lw=1);axs[0,0].set(title="P2: optimistic budget; high-pressure least SF",ylabel="Least safety factor")
axs[0,0].legend(fontsize=8,loc="lower right")
floor=100*R["floor_proof"]["optimistic"]["volume_proportional_reserve_floor"]
axs[0,1].axhline(floor,color="#555",lw=1,label=f"Climate + gas floor {floor:.2f}%")
axs[0,1].axhline(5,color="#999",ls="--");axs[0,1].set(title="P2: reserve does not fall below 5%",ylabel="Reserve / reference lift (%)")
axs[0,1].legend(fontsize=8)
for mass,style in (("coupled","--"),("coupled_pump_scaled","-")):
    for fam in ("aluminium","aramid"):
        rows=[p for p in R["P2"] if p["mass_model"]==mass and p["scenario"]=="conservative" and p["family"]==fam and p["mechanical"]=="chain_design"]
        axs[1,0].plot([p["radius_m"] for p in rows],[p["least_SF"] for p in rows],style,marker="o",
                      color=colors[fam],label=f"{fam}, {'scaled pump bank' if mass.endswith('scaled') else 'one pump'}")
axs[1,0].set(title="P2: conservative budget, design properties",ylabel="Least safety factor")
axs[1,0].legend(fontsize=8)
for label,scaled,color,linestyle in (("optimistic",False,"#24664f","-"),("conservative",False,"#825f9b","--"),("conservative",True,"#825f9b","-")):
    rows=[p for p in F["P3"] if p["scenario"]==label and p["pump_scaled"]==scaled]
    axs[1,1].plot([p["radius_m"] for p in rows],[p["least_SF"] for p in rows],linestyle,marker="o",color=color,
                  label=label+(", pump bank" if scaled else ""))
axs[1,1].plot([p["radius_m"] for p in F["similarity"]],[p["least_SF"] for p in F["similarity"]],":",color="#777",label="Similar frame, fixed film (no budget)")
axs[1,1].axhline(1,color="#444",lw=1)
axs[1,1].set(title="P3: 011b arc model, fixed member bounds",ylabel="Least safety factor")
axs[1,1].legend(fontsize=8)
for ax in axs.flat:
    ax.set_xlabel("Radius (m)")
    ax.set_xticks([10,15,20,30,50])
    ax.grid(alpha=.2)
fig.suptitle("MAINLINE-027 — size helps surface budgets, not every failure mode\nQUESTIONABLE inputs / PROJECTION fabrication and mechanical optimisms",fontsize=13)
fig.savefig(ROOT/"size-as-lever.png",dpi=180)
fig.savefig(ROOT/"size-as-lever.svg")
print(json.dumps(valid,indent=2))
