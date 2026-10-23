"""Build concise machine-readable purchasing map, NFI, current P3 targets and figure."""
from pathlib import Path
import csv
import json

HERE = Path(__file__).resolve().parent
I = json.loads((HERE/"INPUTS.json").read_text())
R = json.loads((HERE/"RESULTS.json").read_text())

tests = [
    ("T1", 1, "Finished SR200 compression and specification", [5,15], [0,0],
     ["P2 O3 compression", "P2 O4 sheet size/gauge", "030 ground-first 4", "036 compression"],
     ["E9", "E1012"], "Be-capable sheet producer/fabricator and metals compression laboratory"),
    ("T2", 2, "Weighed curved sealed scarf panel", [12,35], [0,0],
     ["P2 O4 stock panels", "P2 O5 thin bond", "P2 scarf/weld load transfer", "030 ground-first 3"],
     ["C273", "C297", "C365", "custom scarf/load/leak protocol"],
     "Be-capable aerospace sandwich fabricator and bond/mechanical test house"),
    ("T3", 3, "Wrinkle screen and biaxial follow-on", [6,18], [18,45],
     ["P2 O2 wrinkling", "030 ground-first 5"],
     ["C364", "C273", "C365", "D7249 optional", "custom biaxial panel"],
     "Sandwich compression lab with DIC and multiaxial fixture partner"),
    ("T4", 4, "Complete film laminate strength, creep and barrier", [8,25], [15,40],
     ["P3 film 024/030/022d", "P3 sag"],
     ["D882 where applicable", "D1434", "F1249", "custom biaxial bulge/creep"],
     "Structural laminate developer and polymer-barrier/multiaxial lab"),
    ("T9", 5, "Service vacuum hold and hot gas pressure", [4,12], [0,0],
     ["034 vacuum hold", "core/bore evacuation", "019 systems and gas reserve"],
     ["ISO 20485", "E595 optional screen", "calibrated rate-of-rise/throughput"],
     "Vacuum leak-test and thermal-vacuum materials laboratory"),
    ("T6", 6, "P3 axial/moment/roll joint qualification", [5,15], [25,75],
     ["P3 joint 023", "P3 restraint 026", "022d sized joint"],
     ["E1012 supporting", "custom loaded stiffness matrix and component strength"],
     "Bonded-joint development shop and high-load multiaxial structural lab"),
    ("T5", 7, "SiC process compression and tube stubs", [10,25], [25,100],
     ["P3 compression 025", "P3 curved tube manufacture"],
     ["C1424 standard specimens", "custom stub and curved component protocol"],
     "Technical ceramic tube supplier and high-load ceramics/component laboratory"),
    ("T7", 8, "Closed sandwich surrogate shell", [30,90], [0,0],
     ["P2 O1 gamma", "030 ground-first 1", "029 FE physical calibration"],
     ["C273/C297/C365 material witnesses", "custom closed-shell external pressure"],
     "Precision shell/core shop and nonlinear structures pressure laboratory"),
    ("T8", 9, "Closed discrete frame surrogate", [45,130], [0,0],
     ["030 ground-first 2", "026 discrete frame", "022d topology/global stability"],
     ["custom frame/skin pressure protocol", "material and joint witness methods"],
     "Precision curved-frame fabricator and pressure/DIC structural research laboratory"),
]
plan = {
    "schema":1, "card":"MAINLINE-038", "status":"QUESTIONABLE/PROJECTION",
    "contacted_suppliers":False, "purchases_executed":False,
    "cost_currency":"USD", "cost_basis_year":2026, "costs_are_quotes":False,
    "shared_Be_stock_process_allowance_kUSD":[20,90],
    "first_three":["T1","T2","T3"],
    "first_three_initial_incremental_kUSD":[23,68],
    "first_three_with_shared_stock_kUSD":[43,158],
    "excluded_follow_on_biaxial_T3_kUSD":[18,45],
    "physical_measurements_performed":False,
    "test_details":"CARD.md", "equations_and_transfer":"METHOD.md",
    "latest_P3_test_targets":"P3-LATEST.md",
    "tests":[dict(id=t[0],rank=t[1],title=t[2],initial_kUSD=t[3],
                  follow_on_kUSD=t[4],covers=t[5],standards=t[6],provider_type=t[7],
                  tag="PROJECTION", qualification_closed=False)
             for t in tests],
    "ranking_basis":"Ability to falsify a current binding premise per cost, dependencies and shared specimens; no assumed probabilities.",
    "full_size_SiC_arc_campaign_additional_kUSD":[100,400],
    "arc_cost_note":"Or more; manufacturability, tooling and minimum lot remain unknown.",
    "smallest_shell":{
        "absolute_mathematical_minimum":None,
        "fabrication_floors_assumed":{"face_um":25,"core_mm":1},
        "conditional_021b_R_m":.3614032861983396,
        "conditional_028b_R_m":.43034411608332657,
        "suggested_surrogate_R_m":.5,
        "commercial_actual_Be_small_shell_established":False,
    },
    "source_cutoff":I["captured_at"],
    "not_filed_at_last_lookup":["MAINLINE-029"],
    "not_filed_note":"No result assumed; the physical gamma protocol remains valid preparation for a future filed FE comparison.",
}
(HERE/"TEST-PLAN.json").write_text(json.dumps(plan,indent=2,allow_nan=False)+"\n")

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

lines = [
    "**MAINLINE-038 — latest P3 test targets from filed 022d. QUESTIONABLE / PROJECTION.**",
    "",
    "These supersede 022c procurement dimensions. The frozen 022c sensitivities remain in CARD/METHOD/OUTCOMES solely to audit the named 1.5 GPa material premise. Both Zylon plies are included here. No row establishes a full-size allowable or qualified hull SF.",
    "",
    "| Family / reserve / band | Modeled SF | s / arc m | OD / wall mm | Film total / each ply μm | Operating / sized-joint load MN | Film mass kg | Half-wave/member |",
    "|---|---:|---:|---:|---:|---:|---:|---:|",
]
flat=[]
for r in R["P3_022d"]:
    x=r["source"]
    c=x["case"]
    ply=x["film_per_direction_m"]
    jt=x["joint"].get("design_force_N")
    lines.append(
        f"| {c['family']} / {c['reserve']} / {c['band']} | {x['SF_least']:.6f} "
        f"| {x['s_m']:.6f} / {x['member_length_m']:.6f} "
        f"| {2*x['r_o_m']*1000:.3f} / {x['wall_m']*1000:.6f} "
        f"| {x['film_total_m']*1e6:.3f} / {f'{ply*1e6:.3f}' if ply else '—'} "
        f"| {x['force_at_pressure_1_N']/1e6:.6f} / {f'{jt/1e6:.6f}' if jt else 'unknown'} "
        f"| {x['mass_kg']['film']:.3f} | {x['half_wave_over_member']:.6f} |")
    flat.append(dict(key=x["key"],SF=x["SF_least"],s_m=x["s_m"],arc_m=x["member_length_m"],
                     OD_mm=2*x["r_o_m"]*1000,wall_mm=x["wall_m"]*1000,
                     film_total_um=x["film_total_m"]*1e6,film_ply_um=ply*1e6 if ply else None,
                     operating_force_N=x["force_at_pressure_1_N"],joint_design_force_N=jt,
                     film_effective_stress_GPa=r["film_effective_total_gauge_demand_GPa"],
                     ply_stress_GPa=r["film_directional_ply_demand_GPa"],
                     joint_each_end_kg=r["joint_mass_each_end_kg"],
                     bulge_pressure_MPa=r["small_bulge_actual_gauge_pressure_MPa"]))
chosen=next(r for r in R["P3_022d"] if r["key"]=="cap/equilateral/019/cfrp_zylon/in_band")
x=chosen["source"]
lines += [
    "",
    "**Use the 019 screened Zylon point as the procurement reference for this plan, while retaining the overall branch as a separate sensitivity.** This choice carries the larger inherited reserve; it is not a claim of demonstrated conservatism. The one-member half-wave constraint is a requested screen, not a demonstrated homogenization boundary. Its three modes (local/global/film) bind at 1.194121. It still assumes SiC Fc=3.9 GPa and an unqualified complete membrane.",
    "",
    f"T4: total structural gauge is {x['film_total_m']*1e6:.3f} μm, half in each direction. Nominal directional stress is {chosen['film_directional_ply_demand_GPa']:.6f} GPa, not the total-gauge effective {chosen['film_effective_total_gauge_demand_GPa']:.6f} GPa. A 0.30 m same-gauge cap-equivalent bulge needs about {chosen['small_bulge_actual_gauge_pressure_MPa']:.6f} MPa to reproduce service stress; a same-pressure geometrically scaled laminate would be only {chosen['small_bulge_same_pressure_total_gauge_um']:.3f} μm total and is not the production microstructure.",
    "",
    "| Measured effective strength using total two-ply gauge, GPa | Corresponding directional-ply strength, GPa | Film SF, fixed gauge |",
    "|---:|---:|---:|",
]
for y in chosen["film_sensitivities"]:
    lines.append(f"| {y['effective_total_gauge_strength_GPa']:.3f} | {y['directional_ply_strength_GPa_if_crossply']:.3f} | {y['film_SF']:.6f} |")
lines += [
    "",
    "An improvement above the baseline film capacity leaves other modeled modes binding. Barrier, adhesive, UV/moisture protection and seams must be weighed separately; the structural fiber gauge is not the finished laminate gauge. 034's 57.546 kg illustrative barrier/attachment bill demonstrates the kind of missing mass; it is not a measured bill for this geometry.",
    "",
    f"T5: mean and maximum compression at operating load are {x['axial_stress_at_pressure_1_Pa']/1e9:.6f} and {x['stresses']['operating_pressure']['max_compression_Pa']/1e9:.6f} GPa. At the claimed multiplier the maximum is {x['stresses']['at_limit']['max_compression_Pa']/1e9:.6f} GPa. These include the inherited bow model, not contact/fracture qualification. Make representative approximately {2*x['r_o_m']*1000:.3f} mm OD, {x['wall_m']*1000:.6f} mm wall stubs; the eventual arc is {x['member_length_m']:.6f} m long.",
    "",
    "| Assumed Fc, GPa | Mean-compression SF | Inherited Perry SF |",
    "|---:|---:|---:|",
]
for y in chosen["compression_sensitivities"]:
    lines.append(f"| {y['assumed_Fc_GPa']:.2f} | {y['mean_compression_SF']:.6f} | {y['inherited_Perry_SF']:.6f} |")
lines += [
    "",
    "These ratios do not replace the maximum-compression, local wall, global, contact and brittle-failure checks. A coupon that passes mean stress alone is insufficient.",
    "",
    f"T6: operating/sized joint forces are {x['force_at_pressure_1_N']/1e6:.6f}/{x['joint']['design_force_N']/1e6:.6f} MN, or {chosen['joint_scaled_one_fifth_operating_N']/1000:.3f}/{chosen['joint_scaled_one_fifth_target_N']/1000:.3f} kN at 1:5 with the same material and geometric similarity. The modeled wrap overlap is {x['joint']['overlap_m']*1000:.3f} mm and the charged mass is {chosen['joint_mass_each_end_kg']:.6f} kg/end. The actual adhesive and all restraint hardware must be included. An extra 10 g/end costs {2*x['members']*.01:.3f} kg before replacing the fractional member count.",
    "",
    f"At fixed joint section/bond geometry, an observed axial or bond capacity of 0.7 / 1.0 / 1.2 times the claimed target gives the corresponding joint-mode SF {x['target_multiplier']*.7:.6f} / {x['target_multiplier']:.6f} / {x['target_multiplier']*1.2:.6f}. Whole-frame SF remains unknown without rotational/roll data. Here EI/L={chosen['joint_EI_over_L_Nm_per_rad']/1e6:.6f} MN m/rad; report beta=Ktheta/(EI/L).",
    "",
    "T8: the screened branch has a fractional node count near 149. A 162-node frequency-4 mesh is a possible integer candidate for a fresh model, while a 42-node frequency-2 mesh addresses the coarse overall branch. No existing model factor is assigned to either merely by proximity of node count. At R=0.5 m, the screened reference scales to about 13.536 mm OD and 55.277 μm wall; reject or redesign the test if the available tube/joint/skin cannot preserve the intended dimensionless response.",
    "",
    "**No stiffness threshold or allowable was supplied by these arithmetic updates.** First measure real joints and full laminate, then compute the selected integer model. The two-way numerical maxima are excluded from this procurement preference because their in-plane shear stiffness remains unresolved. R20 transfer still requires topology, gauge/process and size-dependent material qualification.",
]
(HERE/"P3-LATEST.md").write_text("\n".join(lines)+"\n")
with (HERE/"P3-LATEST.csv").open("w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)

# Standalone scientific figure; no image-generation tool is needed for calculated data.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
fig, ax=plt.subplots(1,2,figsize=(12,4.8),layout="constrained")
radius=np.geomspace(.2,10,200)
for label,pt,color in [("021b",R["P2_historical"],"#187b9b"),("028b",R["P2_current"],"#a84f2c")]:
    tf=pt["tf_m"];tc=pt.get("tc_m",pt.get("core_m"))
    ax[0].loglog(radius,tf*radius/10*1e3,label=f"{label} face",color=color)
    ax[0].loglog(radius,tc*radius/10*1e3,ls="--",label=f"{label} core",color=color)
ax[0].axhline(.025,color="gray",lw=.8,ls=":",label="face floor 0.025 mm")
ax[0].axhline(1,color="black",lw=.8,ls=":",label="core floor 1 mm")
ax[0].axvline(.5,color="black",lw=.8,ls="-.")
ax[0].set(xlabel="Shell radius (m)",ylabel="Thickness (mm)",
          title="Geometric gauges; floors are planning assumptions")
ax[0].legend(fontsize=8,ncol=2)
ax[0].grid(alpha=.15,which="both")
sel=[x for x in R["scaling"] if x["R_m"]==.5]
names=[x["reference"].split()[0]+"\n"+("Be" if x["material"]=="same Be" else "Al surrogate") for x in sel]
pos=np.arange(4)
ax[1].bar(pos-.18,[x["design_pressure_kPa"] for x in sel],width=.36,label="design equivalent",color="#187b9b")
ax[1].bar(pos+.18,[x["gamma1_reference_kPa"] for x in sel],width=.36,label="γ=1 reference",color="#b4cbd1")
ax[1].axhline(101.325,color="#a84f2c",ls="--",label="sea-level vacuum ceiling")
ax[1].set_xticks(pos,names)
ax[1].set(ylabel="Differential pressure (kPa)",title="Atmospheric evacuation: pressure ceiling")
ax[1].legend(fontsize=8)
fig.suptitle("MAINLINE-038 — conditional shell test scaling, not a qualified Be replica",fontsize=12)
fig.savefig(HERE/"shell-test-scaling.png",dpi=180)
fig.savefig(HERE/"shell-test-scaling.svg")
plt.close(fig)
print(json.dumps({"tests":len(tests),"NFI":len(issues),"latest_P3_rows":len(flat)}))
