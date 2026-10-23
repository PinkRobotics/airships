"""Coverage, source-input transfers, presentation arithmetic, and model limits."""
import datetime
import json
import math
import csv
import sys
from pathlib import Path
import numpy as np
sys.dont_write_bytecode = True
import independent as m

B = Path(__file__).resolve().parent
D = json.loads((B/"DERIVED.json").read_text())
C = m.C
R = json.loads((B/"owner/RESULTS.json").read_text())
I = json.loads((B/"owner/INPUTS.json").read_text())
ORIGINAL = json.loads((B/"ARITHMETIC.json").read_text())
CHECKS = m.CHECKS
check, compare = m.check, m.compare
DATA = {}


def leaves(x, path="compute"):
    if isinstance(x,dict):
        for k,v in x.items():
            yield from leaves(v,path+"/"+k)
    elif isinstance(x,list):
        for k,v in enumerate(x):
            yield from leaves(v,path+"/"+str(k))
    elif isinstance(x,(int,float)) and not isinstance(x,bool):
        yield path,x


# All scored source inputs are traced into the owner's frozen source register.
# These are provenance checks, not independent certification of their values.
registers={name:json.loads((B/f"owner-sources/{name}.json").read_text())["rows"]
           for name in ["core","adhesive","interlayer"]}
for k,row in C["sources_used"].items():
    if "index" in row:
        source=registers[row["file"].replace(".json","")][row["index"]]
        check("compute/sources_used/"+k+"/value",row["value"],
              source[row.get("field","value")],kind="source-register transfer")
        check("input/sources_used/"+k+"/index",I["sources_used"][k]["index"],
              row["index"],kind="source-register index")
    else:
        value={"cr3_W_min_psi":25,"cr3_L_min_psi":45}[k]
        check("compute/sources_used/"+k+"/value",row["value"],value,
              kind="primary Hexcel Table II")
check("compute/sft_window/service_K/0",C["sft_window"]["service_K"][0],m.COLD)
check("compute/sft_window/service_K/1",C["sft_window"]["service_K"][1],m.HOT)
check("compute/sft_window/swing_K",C["sft_window"]["swing_K"],m.SWING)

# The L branch alone used rounded source-register quantities. This reproduces
# all fourteen precision differences without overwriting the exact-SI check.
rounded=[]
for i,row in enumerate(C["residual"]):
    eps=m.DA*D["residual"][i]["worst_dT_K"]
    tau=2*eps*math.sqrt(m.K2*103.42e6)
    typ=379.21e3/tau
    minimum=45*m.PSI/tau
    rounded.append(dict(case=i,typ=typ,minimum=minimum))
    check(f"rounded_L/{i}/typ",row["SF_edge_L_typ"],typ)
    check(f"rounded_L/{i}/min",row["SF_edge_L_min"],minimum)
DATA["rounded_L_replication"]=rounded

# Direct minimisation of periodic spring energy: q is the internal vertical
# displacement divided by cell-wall length; macro strain is one.
n=np.array([[0.,1.],[math.sqrt(3)/2,-.5],[-math.sqrt(3)/2,-.5]])
weights=np.array([2.,1.,1.])
stiff=sum(w*np.outer(v,v) for w,v in zip(weights,n))
force=sum(w*v for w,v in zip(weights,n))
q=np.linalg.solve(stiff,-force)
strains=1+n@q
energy_ratio=float(sum(weights*strains**2)/sum(weights))
DATA["periodic_cell_equilibrium"]=dict(internal_displacement=q.tolist(),
    wall_strains=strains.tolist(),energy_ratio=energy_ratio,
    force_balance=(sum(w*e*v for w,e,v in zip(weights,strains,n))).tolist())
check("cell/energy_ratio",C["doubled_wall_cell"]["k_biax_ratio"],energy_ratio)
check("cell/single_wall_stress_ratio",C["doubled_wall_cell"]["single_wall_stress_ratio"],float(strains[1]))

# 037b verdict's derived numeric leaves, not merely copying its compute subtree.
v=R["verdict"];t=D["residual"][0];low=D["residual"][2]
derived_verdict={
 "bond_free_core_edge":{"SF_typ":t["SF_edge_typ"],"SF_min":t["SF_edge_min"],
                       "L_typ":t["SF_edge_L_typ"],"L_min":t["SF_edge_L_min"]},
 "bond_037_screen":{"SF_typ":t["SF_037_typ"],"SF_min":t["SF_037_min"],
                   "core_force_ratio_to_wall_yield":D["screen_equilibrium"]["cure_250F"]["ratio"]},
 "face_compression_at_028b_lead_MPa":m.KB*m.DA*(m.T250-m.COLD)*D["baseline"]["tc"]/(2*D["baseline"]["tf"])/1e6,
 "028b_usage_own":D["baseline"]["u_raw"],
 "028b_usage_with_cure_compression":D["fix_searches"][0]["search"]["best"]["u_raw"],
 "037_point_scarf_with_cure_compression":t["p2_037_least_SF"],
 "lightest_change_SF_free_edge":{"typ":low["SF_edge_typ"],"min":low["SF_edge_min"]},
 "lightest_change_028b":{"usage":D["fix_searches"][6]["search"]["best"]["u_raw"],
                       "gamma":D["fix_searches"][6]["search"]["best"]["gamma_need"],
                       "Q":D["fix_searches"][6]["search"]["best"]["Q_need"]},
 "stress_free_ceiling_037_scarf_C":D["037_scarf_ceiling_C"]}
compare("verdict",v,derived_verdict)
DATA["verdict"]=derived_verdict

# Every scalar duplicated into RESULTS.compute is checked, including sentinels.
for path,value in leaves(C):
    cursor=R["compute"]
    for part in path.split("/")[1:]:
        cursor=cursor[int(part)] if isinstance(cursor,list) else cursor[part]
    check("results_duplicate/"+path,cursor,value,kind="duplicate transfer")

# A diagnostic tuple from an infeasible solve is not a physical design.
diagnostics=[]
for i in [8,9]:
    for suffix in ["","/without_residual"]:
        row=C["fixes"][i] if not suffix else C["fixes"][i]["without_residual"]
        diagnostics.append(dict(index=i,suffix=suffix,tf_mm=row["tf_mm"],tc_mm=row["tc_mm"],
            interpretation="no physical design: independent search found no feasible geometry",
            independently_rejected=D["fix_searches"][i]["search"]["best"] is None
                if "best" in D["fix_searches"][i]["search"]
                else not D["fix_searches"][i]["search"]["feasible"]))
check("compute/fixes/9/others/crush",C["fixes"][9]["others"]["crush"],2*m.SW/m.P0)
DATA["failed_solve_diagnostics"]=diagnostics

# Primary-unit conversions used in the card. Tolerances express printed
# rounding; no additional material precision is inferred.
conversion_rows=[
 ("foil_5052_E_GPa",8.2e6*m.PSI/1e9,.0005),
 ("foil_5052_yield_MPa",33e3*m.PSI/1e6,.005),
 ("al_core_cte_thickness",13.2e-6*1.8,1e-12),
 ("glass_cte",8.2e-6*1.8,1e-12),
 ("hrh49_cte",2.7e-6*1.8,1e-12),
 ("hrh10_cte",19.4e-6*1.8,1e-12),
 ("hft_rho",2*m.RHO,.005),
 ("hft_gw",5000*m.PSI/1e6,.0005),
 ("hft_ec",17000*m.PSI/1e6,.005),
 ("hft_stab",170*m.PSI/1e3,.05),
 ("hft_sw",60*m.PSI/1e3,.005),
 ("hrp_rho",3.2*m.RHO,.005),
 ("hrp_gw",5000*m.PSI/1e6,.0005),
 ("hrp_ec",38000*m.PSI/1e6,.05),
 ("hrp_stab",390*m.PSI/1e3,.05),
 ("hrp_sw",110*m.PSI/1e3,.005),
 ("hrh49_rho",2.1*m.RHO,.005),
 ("hrh49_gw",1300*m.PSI/1e6,.00005),
 ("hrh49_ec",25000*m.PSI/1e6,.005),
 ("hrh49_stab",130*m.PSI/1e3,.005),
 ("hrh49_sw",40*m.PSI/1e3,.005),
 ("hrh10_rho",1.5*m.RHO,.005),
 ("hrh10_gw",1500*m.PSI/1e6,.0005),
 ("hrh10_ec",6000*m.PSI/1e6,.0005),
 ("hrh10_stab",105*m.PSI/1e3,.005),
 ("hrh10_sw",35*m.PSI/1e3,.005),
 ("ph_rho",5.1*m.RHO,.001),
 ("be_rho",5.3*m.RHO,.001),
 ("cr3_L_strength_kPa",55*m.PSI/1e3,.005),
 ("cr3_L_modulus_MPa",15000*m.PSI/1e6,.005),
 ("cr3_W_strength_kPa",35*m.PSI/1e3,.005),
 ("cr3_W_modulus_MPa",6800*m.PSI/1e6,.0005),
]
for key,value,tol in conversion_rows:
    check("primary_conversion/"+key,C["sources_used"][key]["value"],value,
          rtol=0,atol=tol,kind="primary printed-unit conversion")
DATA["unit_conversions"]=dict((k,v) for k,v,_ in conversion_rows)

# Finite face stiffness and balanced residual effects remain model questions.
# For the symmetric thermal-only field the correction is small and calculable.
fp=D["finite_face_compatibility"]
for r in fp:
    check("finite_faces/"+r["geometry"]+"/force_equilibrium",0,
          r["wall_force_per_width_N_m"]-2*(m.TF37 if r["geometry"]=="037"
                                          else D["baseline"]["tf"])*r["face_residual_MPa"]*1e6,
          atol=1e-8)
DATA["finite_faces"]=fp

# Explicitly show the two-layer series-compliance sensitivity. The rigid
# inherited screen uses one added interlayer compliance; the symmetric edge and
# global calculations use both. It is a convention issue, not a new pass.
needed=m.GSI*((m.DA*(m.T250-m.COLD))**2*m.EF*m.TF37/m.SW**2-m.TC37/m.GC)
DATA["symmetric_interlayer_sensitivity"]=dict(
    owner_rigid_screen_each_layer_m=needed,
    symmetric_two_interface_each_layer_m=needed/2,
    symmetric_total_mass_kg=2*m.A*m.RHOSI*needed/2,
    note="Changing the old screen to include both interfaces halves its required thickness. Both versions are far over budget.")

# Phrase 'mass alone' is too broad for the lighter nonmetal cores. The 32 kg/m3
# glass rejection depends on its real core mechanics and fixed seam as well.
ideal_hft=m.search(core=m.core_params(32.04,1e12,1e12,1e9,.001))
DATA["ideal_properties_at_HFT_density"]=ideal_hft

# Additional human-readable card checks, independently calculated and rounded
# according to the number of digits actually printed.
present=[
 ("rigid_cure_tau_kPa",1063,t["tau_037_kPa"],.5),
 ("rigid_cure_factor",.227,t["SF_037_typ"],.0005),
 ("face_force_kN_m",351,D["screen_equilibrium"]["cure_250F"]["face_force_N_per_m"]/1000,.5),
 ("core_force_kN_m",703,D["screen_equilibrium"]["cure_250F"]["core_force_needed_N_per_m"]/1000,.5),
 ("wall_yield_force_kN_m",14.9,D["screen_equilibrium"]["cure_250F"]["core_force_at_wall_yield_N_per_m"]/1000,.05),
 ("47_times",47,D["screen_equilibrium"]["cure_250F"]["ratio"],.5),
 ("12_times",12,D["screen_equilibrium"]["swing_037"]["ratio"],.5),
 ("wall_uniform_MPa",102,t["wall_stress_MPa"],.5),
 ("wall_double_MPa",122,t["wall_stress_doubled_single_MPa"],.5),
 ("wall_uniform_factor",2.24,t["wall_SF_on_5052H39_yield"],.005),
 ("wall_double_factor",1.87,t["wall_SF_doubled_single"],.005),
 ("edge_typ",1.17,t["SF_edge_typ"],.005),("edge_min",.83,t["SF_edge_min"],.005),
 ("transfer_mm",16,t["transfer_length_mm"],.5),
 ("transfer_cells",1.7,t["transfer_length_mm"]/9.525,.05),
 ("face_compression_MPa",4.4,derived_verdict["face_compression_at_028b_lead_MPa"],.05),
 ("compression_percent",1.5,100*derived_verdict["face_compression_at_028b_lead_MPa"]/(m.P0*m.R/(4*D["baseline"]["tf"])/1e6),.05),
 ("baseline_usage",.972,D["baseline"]["u_raw"],.0005),
 ("hot_usage",1.052,D["fix_searches"][0]["search"]["best"]["u_raw"],.0005),
 ("hot_gamma",.618,D["fix_searches"][0]["search"]["best"]["gamma_need"],.0005),
 ("hot_Q",.409,D["fix_searches"][0]["search"]["best"]["Q_need"],.0005),
 ("hot_tc_mm",20.9,1000*D["fix_searches"][0]["search"]["best"]["tc"],.05),
 ("scarf_ceiling_C",54,D["037_scarf_ceiling_C"],.5),
 ("fix_mass_kg",.12,D["fix_searches"][6]["mass_change_at_original_lead_kg"],.005),
 ("fix_ratio",30.34,D["constants"]["scarf_ratios"][1],.005),
 ("hot_ratio",30.44,D["constants"]["scarf_ratios"][0],.005),
 ("interlayer25_mass",94,2*m.A*m.RHOSI*25e-6,.5),
 ("interlayer100_mass",374,2*m.A*m.RHOSI*100e-6,.5),
 ("interlayer_required_mm",5.5,needed*1000,.05),
 ("interlayer_required_tonnes",20.6,2*m.A*m.RHOSI*needed/1000,.05),
 ("rigid_window_low_C",.4,D["windows"]["037_screen"]["lo_K"]-273.15,.05),
 ("rigid_window_high_C",25.9,D["windows"]["037_screen"]["hi_K"]-273.15,.05),
 ("rigid_min_low_C",8.4,D["windows"]["037_screen_min"]["lo_K"]-273.15,.05),
 ("rigid_min_high_C",17.9,D["windows"]["037_screen_min"]["hi_K"]-273.15,.05),
 ("free_typ_ceiling_C",142,D["windows"]["free_edge_typ"]["hi_K"]-273.15,.5),
 ("free_min_ceiling_C",101,D["windows"]["free_edge_min"]["hi_K"]-273.15,.5),
]
for name,owner,calc,tol in present:
    check("presentation/"+name,owner,calc,rtol=0,atol=tol,kind="printed rounding")
DATA["presentation_count"]=len(present)

# Computation timestamps are metadata, not a time budget.
elapsed=(datetime.datetime.fromisoformat(C["ended"])-datetime.datetime.fromisoformat(C["started"])).total_seconds()
check("compute/elapsed_s",C["elapsed_s"],elapsed,atol=.001,kind="timestamp cross-check")

# Classify every numeric compute leaf, including pin sizes and non-design
# sentinels. Search-path comparisons are equivalent to the compute path.
direct={r["path"] for r in ORIGINAL+CHECKS}
coverage=[]
for path,value in leaves(C):
    if path in direct:
        mode="direct independent check or declared provenance transfer"
    elif path.replace("compute/fixes","search/fixes",1) in direct:
        mode="independent geometry search"
    elif path.startswith("compute/pins/"):
        mode="input provenance pin metadata (non-code verified separately; five executables excluded)"
    elif path.startswith("compute/sources_used/"):
        mode="source register index metadata"
    elif path.startswith("compute/fixes/9/"):
        mode="infeasible zero-geometry sentinel; interlayer mass alone rejects"
    elif path.startswith("compute/fixes/8/") and path.endswith(("/tf_mm","/tc_mm")):
        mode="nonunique failed-solve trial geometry; all its physical diagnostics and mass evaluated, independent search rejects"
    else:
        mode="UNACCOUNTED"
    coverage.append(dict(path=path,owner=m.clean(value),coverage=mode))
DATA["numeric_leaf_coverage"]=coverage
DATA["unaccounted"]=[r for r in coverage if r["coverage"]=="UNACCOUNTED"]
DATA["count"]=len(coverage)
DATA["checks"]=CHECKS
DATA["summary"]=dict(checks=len(CHECKS),matches=sum(r["match"] for r in CHECKS),
                     mismatches=sum(not r["match"] for r in CHECKS),
                     numeric_leaves=len(coverage),unaccounted=len(DATA["unaccounted"]))
(B/"SUPPLEMENT.json").write_text(json.dumps(m.clean(DATA),indent=2,allow_nan=False)+"\n")
with (B/"EXACT-DIFFERENCES.csv").open("w",newline="") as f:
    fields=["path","owner","independent","independent_minus_owner","classification"]
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for row in ORIGINAL+CHECKS:
        if not row["match"]:
            w.writerow({**{k:row[k] for k in fields[:-1]},
                        "classification":"rounded L strength/modulus versus exact primary-unit conversion"})
    w.writerow(dict(path="fixes/2/HexBond679_total_mass_increment_kg",
                    owner=C["fixes"][2]["mass_change_kg"],
                    independent=D["hexbond_support_correction"]["corrected_increment_kg"],
                    independent_minus_owner=D["hexbond_support_correction"]["missing_mass_kg"],
                    classification="omitted 30 g/m2 support per face; rejection remains"))
print(json.dumps(DATA["summary"],indent=2))
for r in CHECKS:
    if not r["match"]:print(json.dumps(r))
print("UNACCOUNTED",json.dumps(DATA["unaccounted"]))
