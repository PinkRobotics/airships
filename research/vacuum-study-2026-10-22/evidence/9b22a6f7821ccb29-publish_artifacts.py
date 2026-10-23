#!/usr/bin/env python3
"""Create the review card, equations, open evidence needs, table export and figure."""
import csv
import json
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import atmosphere as at

ROOT=Path(__file__).resolve().parent
P2=json.loads((ROOT/"P2.json").read_text())
P3=json.loads((ROOT/"P3.json").read_text())
AT=json.loads((ROOT/"ATMOSPHERE.json").read_text())
VAL=json.loads((ROOT/"VALIDATION.json").read_text())
I=at.IN


def fmt(x,n=3):
    return f"{x:.{n}f}"


def tab(headers,rows):
    return "\n".join(["| "+" | ".join(headers)+" |",
                      "| "+" | ".join(["---"]*len(headers))+" |"]+
                     ["| "+" | ".join(map(str,r))+" |" for r in rows])+"\n"


def winner(env,floor):
    return next(s for s in P2["least_optimism_searches"]
                if s["envelope"]==env and s["altitude_floor_m"]==floor)


def p3point(env,floor):
    return next(s for s in P3["reoptimised"]
                if s["envelope"]==env and s["altitude_floor_m"]==floor)


def export_csv():
    rows=[]
    def add(branch,label,env,days):
        for r in days:
            d=dict(branch=branch,case=label,envelope=env,
                   **{k:r[k] for k in ("day","z_m","p_Pa","p_over_p0","T_K","relative_humidity",
                                      "mass_kg","volume_m3","ground_clearance_m_at_sea_level",
                                      "below_sea_level","touches_or_below_ground","supersaturated",
                                      "least_SF","governing")})
            for k,v in r["sfs"].items():d["SF_"+k]=v
            rows.append(d)
    for r in P2["source_fixed"]:
        add("P2",r["label"],"all_019",r["days"])
        add("P2",r["label"]+"_full_named","all_019",r["full_named_days"])
    for r in P2["reoptimised"]:
        add("P2",r["label"]+"_floor_"+str(r["altitude_floor_m"]),r["envelope"],r["day_rows"])
    for r in P2["least_optimism_searches"]+P2["reconstructed_021_searches"]:
        if r["winner"]:
            p=r["winner"]["point"]
            add("P2",r["variant"]+"_least_set_floor_"+str(r["altitude_floor_m"]),
                r["envelope"],p["day_rows"])
    for r in P3["source_fixed"]:add("P3",r["label"],"all_019",r["days"])
    for r in P3["reoptimised"]+P3["sensitivities"]:
        add("P3",r["film"]+"_floor_"+str(r["altitude_floor_m"]),r["envelope"],r["days"])
    fields=list(rows[0])
    fields+=sorted(set().union(*(r.keys() for r in rows))-set(fields))
    with (ROOT/"ALL-DAYS.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader();w.writerows(rows)
    return len(rows)


def figure():
    plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,
                         "savefig.facecolor":"white"})
    fig,ax=plt.subplots(2,2,figsize=(13.2,9.4),layout="constrained")
    cs=np.linspace(0,650,500)
    colors=["#20567a","#c35a22","#7a477e"]
    for name,label,c in zip(["ISA","optimistic_hot_low_wet","conservative_hot_low_wet"],
                            ["ISA","Optimistic hot / low pressure / humid",
                             "Conservative hot / low pressure / humid"],colors):
        day=next(d for d in at.DAYS if d["id"]==name)
        z=at.equilibrium_density((at.L0-cs)/at.V0,day)[0]
        ax[0,0].plot(cs,z,label=label,color=c,lw=2)
    ax[0,0].axhspan(-1200,0,color="#f7e4e1")
    ax[0,0].axhline(100,color=".3",ls=":",label="Illustrative 100 m centre floor")
    ax[0,0].axhline(500,color=".5",ls="--",lw=1)
    ax[0,0].set(xlabel="Absent climate mass C (kg), R = 10 m",ylabel="Free-float centre height (m)",
                title="Altitude constrains the mass trade",ylim=(-1150,2200),xlim=(0,650))
    ax[0,0].text(630,-1080,"Below sea-level ground",ha="right",color="#87554d",fontsize=9)
    ax[0,0].legend(fontsize=8,loc="upper left")
    for env,color,label in [("optimistic",colors[1],"Optimistic weather"),
                             ("all_019",colors[2],"Both 019 weather sets")]:
        q,_=at.demand(cs,env)
        ax[0,1].plot(cs,np.maximum(1,q),color=color,lw=2,label=label)
        for floor,marker in [(None,"x"),(10.,"s"),(100.,"o"),(500.,"^")]:
            c=at.floor_C(floor,env);q=float(at.demand(c,env)[0])
            ax[0,1].scatter([c],[max(1,q)],color=color,marker=marker,zorder=4)
        r=[v for v in P2["fixed_factor_frontier"] if v["envelope"]==env and
           v["label"]=="021b_fixed_named_values"]
        ax[1,0].plot([v["C_kg"] for v in r],[v["score"] for v in r],
                     color=color,lw=2,label=label)
        c=at.floor_C(100.,env)
        point=next(v for v in P2["reoptimised"] if v["envelope"]==env and
                   v["altitude_floor_m"]==100 and v["label"]=="021b_fixed_named_values")
        ax[1,0].scatter([c],[point["least_SF"]],color=color,zorder=4)
    ax[0,1].set(xlabel="Absent climate mass C (kg)",ylabel="Required nominal SF at p₀",
                title="Least split at each chosen altitude floor",xlim=(0,650))
    ax[0,1].text(.02,.09,"× no floor    □ 10 m    ○ 100 m    △ 500 m",
                  transform=ax[0,1].transAxes,fontsize=9,
                  bbox=dict(facecolor="white",edgecolor="none",alpha=.9))
    ax[0,1].legend(fontsize=9)
    ax[1,0].axhline(1,color=".2",ls="--")
    ax[1,0].set(xlabel="Absent climate mass C (kg)",ylabel="Least SF after pressure allowance",
                title="021b source factors held; geometry reoptimised",xlim=(0,650),ylim=(.83,1.05))
    ax[1,0].legend(fontsize=9)
    source=I["reference_021b"]["floating_point"]
    opt=winner("optimistic",100.)["winner"]["point"]
    allp=winner("all_019",100.)["winner"]["point"]
    nc=[I["nonclimate_kg"]]*3
    cc=[I["inherited_climate_allowance_kg"],opt["C_kg"],allp["C_kg"]]
    ex=[source["masses_kg"]["joint_excess_in_reserve"],
        opt["masses_kg"]["joint_excess"],allp["masses_kg"]["joint_excess"]]
    positions=np.arange(3)
    ax[1,1].bar(positions,nc,label="Nonclimate inventory",color="#789eac")
    ax[1,1].bar(positions,cc,bottom=nc,label="Climate mass headroom",color="#d69a68")
    ax[1,1].bar(positions,ex,bottom=np.array(nc)+cc,label="Joint / film excess",color="#a29bc1")
    for j,total in enumerate(np.array(nc)+cc+ex):
        ax[1,1].text(j,total+12,f"{total:.1f} kg",ha="center",fontsize=9)
    ax[1,1].set(xticks=positions,xticklabels=["021b filed\noptimistic weather",
                 "031, 100 m floor\noptimistic weather","031, 100 m floor\nboth weather sets"],
                 ylabel="Bookkeeping reserve (kg)",ylim=(0,1200),
                 title="Least named set, then smallest maximum log usage")
    ax[1,1].legend(fontsize=8,loc="upper left")
    fig.suptitle("MAINLINE-031 · Conditional altitude / climate trade\n"
                 "6.5 K/km hydrostatic profiles; constant e/p; QUESTIONABLE / PROJECTION",
                 fontsize=14)
    fig.savefig(ROOT/"altitude-margin.png",dpi=180)
    fig.savefig(ROOT/"altitude-margin.svg")
    plt.close(fig)


def nfi():
    rows=[
        ("REQUIREMENT","QUESTIONABLE",
         "No site elevation, terrain, minimum hull clearance, altitude ceiling or required 500m condition has been authorised. Centre 10m is ground tangency at sea level; 100m is only an illustrative 90m clearance.",
         "Specify centre-height range relative to surveyed terrain, weather set, clearance and whether 500m means ISA free float or a minimum on every design day."),
        ("PROFILE","PROJECTION",
         "019 specifies conditions at one altitude, not a vertical profile. A 6.5K/km lapse and constant e/p were imposed. At the 100m floor, isothermal optimistic climate mass is 11.73kg versus 55.34kg with the chosen lapse; both-weather values are 403.66 versus 441.77kg.",
         "Supply measured or approved temperature, pressure, humidity and inversion profiles, including joint extremes and occurrence probabilities."),
        ("SATURATION","QUESTIONABLE",
         "The conservative high-pressure humid day becomes supersaturated in the all-weather 500m-floor diagnostic. The 0/10/100m-floor main cases are unsaturated in the stated model. Continuing an unsaturated lapse through cloud is not a physical forecast.",
         "Use a moist atmospheric profile with cloud/condensate treatment; do not treat that diagnostic height as an operational guarantee."),
        ("CONTROL","PROJECTION",
         "A fixed evacuated hull has one passive equilibrium per weather profile and carried load. Positive C raises its ISA float altitude; C=0 cannot float at 500m ISA and satisfy the illustrative sea-level-ground clearance on both 019 hot-day extremes. Static equilibrium does not provide station keeping.",
         "Resolve the mission requirement; size active altitude control, tethering, launch, landing, descent-rate and gust response if needed."),
        ("RESERVE-MEANING","QUESTIONABLE",
         "Climate is absent mass; water, contamination and gas are carried mass. 021 rev1 has a 5% placeholder, no separate climate rows or explicit seam budget. Recasting that placeholder is a new budget assumption.",
         "Approve one common itemised gross mass ledger, including payload status, before treating cross-card points as the same vehicle."),
        ("BE-PROPERTIES","QUESTIONABLE",
         "SR-200 345MPa is a tensile minimum transferred to compression. The 379.2MPa endpoint is a historical lot result; continuous interpolated strength is not a procureable design allowable. 021 rev1 inherits 283MPa at E290GPa.",
         "Obtain gauge-, direction-, lot-, temperature- and post-form compression and modulus allowables."),
        ("PANELS","PROJECTION",
         "The least-set P2 points need multi-metre square-equivalent panels at roughly 0.65–0.72mm face gauge. The nominal today 0.9144m seam-equivalent stock size is itself not established at those gauges.",
         "Supplier-confirm formed sheet sizes, gauges, thickness distribution, yield and joining geometry."),
        ("P2-GAMMA","PROJECTION",
         "The hemisphere-derived 0.2/1 branch rule and 018 interpolation to 0.2+0.4min(Vc,2) have not been validated for the complete sphere. Numerical least-set membership is conditional on these bounds.",
         "Correlate full-shell imperfection-sensitive nonlinear analysis and representative structural testing."),
        ("WRINKLE-CORE","QUESTIONABLE",
         "Wrinkle coefficients between 0.33 and 0.82 and published typical core properties are used for a curved sandwich. The catalogue includes transferred moduli and scaled cores; the winner is the sourced light 5056 core, but no assembly allowable exists.",
         "Test curvature, cell depth, orthotropy, face/core bond and biaxial wrinkling/crimp/crush/dimpling at service temperature."),
        ("JOINTS","PROJECTION",
         "P2 seams and bond films are a mass recipe, not checked structural joints. P3 percent joints are an allowance, not strength or rotational stiffness. Folded source joints sized at p0 cannot automatically take a larger float pressure.",
         "Size and qualify seal, splice, node and load-introduction details at the maximum service pressure, including stiffness, eccentricity, fatigue and leakage."),
        ("P3-MATERIAL-FILM","PROJECTION",
         "The passing P3 keeps a 3900MPa SiC tube compression value, 410GPa modulus, 1.5GPa/970kg/m3 film and metre-scale thin curved tubes. These are not a demonstrated assembly or a safe tensile/bending allowable.",
         "Carry tube-scale brittle reliability, post-form flaw statistics, film biaxial/creep/UV/seam/barrier properties and manufacture into the model."),
        ("P3-LOCAL","QUESTIONABLE",
         "FIX-A triangular load sharing is used. FIX-B SP-8007 axial-cylinder knockdown is transferred to curved ceramic members; Perry and k=0.2 global continuum equations remain inherited idealisations.",
         "Validate curved member local buckling, imperfections, ceramic tension/compression interaction and discrete-frame modes with actual node stiffness."),
        ("P3-SAG","PROJECTION",
         "022b's s/(16R) displacement loss is applied as reduced volume at every altitude. Film shape may change with pressure, and the spherical arc/member model is approximate for 6m bays on R10m.",
         "Solve coupled membrane shape, true enclosed volume, pressure and frame load path; verify the global continuum approximation and spacing bounds."),
        ("ENVIRONMENT-LOADS","QUESTIONABLE",
         "Mode scores use uniform centre pressure, no internal-pressure relief and fixed material properties. Local bottom pressure is about a further 0.1% higher, while gradients, thermal mismatch, wind, attached loads and descent transients are unscored.",
         "Set structural design factors and loads independently of the SF=1 screening threshold; include nonuniform pressure and thermal/wind/handling loads."),
        ("SYSTEMS-GAS","PROJECTION",
         "The calculation retains optimistic 019 nonclimate loads and the full 100kg system floor even on conservative weather. This isolates weather; it does not qualify the conservative pump/battery/rain/contamination hardware package.",
         "Qualify 24h sealed service and internal gas inventory, or recalculate with measured leakage, pumping, rain/ice retention and all installed systems."),
    ]
    out=dict(schema=1,card="MAINLINE-031",status="OPEN_EVIDENCE_NEEDS",certification=False,
             rows=[dict(id="NFI-031-"+key,tag=tag,issue=issue,next_evidence=next_)
                   for key,tag,issue,next_ in rows])
    (ROOT/"NFI.json").write_text(json.dumps(out,indent=2)+"\n")
    return len(rows)


def method():
    text=r"""# MAINLINE-031 calculation method

ESTIMATE. QUESTIONABLE material/model transfers and PROJECTION atmosphere/fabrication. This is a uniform-pressure structural screen, not certification.

**Atmosphere and equilibrium.** R=10m, sphere volume 4188.790204786391m³, area 1256.6370614359173m², p₀=95460.83791390515Pa, T₀=284.9K, nominal gross displaced mass L₀=4889.442150186961kg. The reference is 500 geopotential metres. Geometric height is zRₑ/(Rₑ−z), Rₑ=6356660m; the difference is small here but actual terrain clearance needs geometric coordinates. The −6.5K/km lapse and altitude convention follow the standard-atmosphere definition, not a claim that hot days follow a measured standard profile. [NASA Appendix A](https://ntrs.nasa.gov/api/citations/20050207438/downloads/20050207438.pdf)

The moist-air density relation is ρ=(p−0.378e)/(R_d T). This is the ideal-mixture/virtual-temperature approximation used in the inherited climate ledger. [NWS virtual-temperature formula](https://www.weather.gov/media/epz/wxcalc/densityAltitude.pdf)

For each weather day, anchor p_d, T_d, e_d at 500m and impose constant e/p with height. Define k=1−0.378e_d/p_d, a=0.0065K/m, n=gk/(R_d a), R_d=287.053J/(kg K), g=9.80665m/s². Integration of hydrostatic balance gives:

```
T(z) = T_d − a(z−500)
p(z) = p_d [T(z)/T_d]^n
ρ(z) = k p(z)/(R_d T(z))
T_float = T_d [(M/V_eff)/ρ_d]^[1/(n−1)]
z_float = 500 + (T_d−T_float)/a
```

This integration is our calculation from hydrostatic balance; the profile choice is an explicit assumption. [NWS hydrostatic and hypsometric equations](https://www.weather.gov/source/zhu/ZHU_Training_Page/Miscellaneous/Heights_Thicknesses/thickness_temperature.htm)

Optimistic hot days use ΔT=10K, p_d/p₀=0.99 or 1.01, e_d=0 or 1000Pa. Conservative hot days use ΔT=25.1K, p_d/p₀=0.98 or 1.02, e_d=0 or 6000Pa. Also score ISA, heat-only and pressure-only days. These are 15 diagnostic days, with the hot-low-wet corner governing pressure and minimum height for the scored mass range. Cold +6000Pa states are excluded as supersaturated at the anchor. The two envelope sets retain the same optimistic nonclimate vehicle inventory.

Sensitivity profiles are (i) isothermal with constant e/p and (ii) the same lapse with constant e. In case (ii), p(z)=0.378e+(p_d−0.378e)[T(z)/T_d]^[g/(R_d a)]. None is established by the single-level 019 inputs. Supersaturated roots are flagged, not silently clipped.

**Definition of the least split.** C≥0 is absent climate mass relative to L_eff=L₀V_eff/V₀. M=L_eff−C. Positive C is not ballast and cannot be removed from a fixed hull by deleting a label. All calculated heights are passive free equilibria, with no tether or thrust.

For a specified centre-altitude floor z_min:

```
C_floor = max(0, L_eff − V_eff min_day ρ_day(z_min))
q_float(C) = max_day p_day(z_float(C))/p₀
q_required(C) = max(1, q_float(C))
nominal SF reserve = q_required − 1
```

The q≥1 constraint preserves the inherited p₀ structural requirement even when every free-float pressure is below p₀. Every inherited mode is a fixed pressure capacity divided by actual pressure; at fixed geometry, SF_i(z)=SF_i(p₀)p₀/p(z). A geometry is accepted only if all modes meet q_required at p₀ and all relevant float roots satisfy the specified floor. C_floor is an exact lower bound on mass headroom for this profile and displaced volume. Feasible reoptimised points attain it. With no altitude floor C=0 is the mathematical minimum; below-ground roots prevent interpreting it as an aircraft requirement.

The objective is lexicographic: minimum C for the stated floor; then fewest named additional optimisms; then smallest maximum logarithmic usage. Kg and SF are different quantities and have no unique combined minimum without an objective. A separate matched-property calculation reports the hardware mass needed at q_required minus that needed at p₀, reoptimising both geometries. It is an isolated mass-equivalent pressure cost, not an additional debit to the already closed mass budget and not a promise of payload at the same free-float altitude.

**P2 mass and capacities.** The 179.55812764546135kg nonclimate reserve is 125.66370614359174kg retained water, 5kg contamination and 48.89442150186961kg internal gas. Systems remain 100kg. Original optimistic climate is 213.036426543752kg temperature/pressure plus 18.704389882434043kg humidity.

With S the faces-plus-core mass, f the core mass fraction, ρ_f=1850kg/m³:

```
t_f = (1−f) S/(2 A ρ_f);  t_c = f S/(A ρ_c)
m_seam = (2A/w)[2b t_f ρ_f + 2b t_adh ρ_adh + t_c w_splice ρ_splice]
m_film = 2 A μ
m_joint = max(0.05 S, m_seam + m_film)
L₀ = C + 100 + 179.55812764546135 + S + m_joint
reserve = C + 179.55812764546135 + max(0,m_joint−0.05S)
```

Use 019 b=0.06m, t_adh=0.0002m, ρ_adh=1250kg/m³, w_splice=0.0015m, ρ_splice=1100kg/m³. Convert film lb/ft² using 0.45359237/0.09290304. The seam equation is linear in S at fixed f,w; the program solves both joint-floor branches algebraically. The unused system allowance remains reserved.

For h=t_c+t_f, ν=0.33:

```
σ₀ = E h/[R sqrt(1−ν²)]
σ_crimp = h² G_c/(2 t_f t_c)
V_c = σ₀/σ_crimp
K_c = 1−V_c/4 (V_c≤2), otherwise 1/V_c
σ_membrane = pR/(4t_f)
SF_global = γ K_c σ₀/σ_membrane
SF_face = σ_allow/σ_membrane
SF_crimp = σ_crimp/σ_membrane
SF_crush = 2 σ_core_crush/p
SF_wrinkle = b_x k_wr sqrt(E E_c t_f/t_c)/σ_membrane
SF_dimple = [E/(1−ν²)](t_f/cell)²/σ_membrane
b_x³+b_x=1
```

These preserve 021b's six equations and biaxial dimpling. ν and property transfers remain conditional. No additional joint-efficiency factor or joint strength mode is invented; those are open evidence needs.

The five named axes are γ: handbook 0.2 below V_c=2 and 1 at/above 2 → 0.2+0.4min(V_c,2); wrinkle 0.33→0.82; compression transfer 345→379.2MPa; panel seam-equivalent width 0.9144→4m; film 0.03→0.015lb/ft². For an allowed axis, x(u)=x_today(x_full/x_today)^u. E stays 290GPa in the least-set search, as in 021b; a full-grade E293.6GPa case is separate. Unneeded wrinkle/strength/gamma usage is reduced in the reported needed-values column without changing geometry. The constructed max-usage point and its complete SF vector remain in JSON.

All 47 eligible 021b honeycombs are searched. At a given subset and u, favourable panel/film bounds maximise available structural mass; all capacities are nondecreasing with that mass over the inherited branches. Search every subset through the first feasible cardinality; bisect u and optimise f, explicitly checking both sides of V_c=2. Lower-cardinality exclusions use a 32769-point/core verification; winning points use 131073 points/core plus local refinement.

021 rev1's original 5% margin is not a weather line. Fixed-hull rows show the unfilled margin, then add the same 019 nonclimate inventory. Its reconstructed optimisation retains only 5% joints and 100kg systems, uses 283→379.2MPa strength and the same gamma/wrinkle axes. This is an incomplete joint-budget comparator, not a replacement for 021b.

**P3.** Use the filed 022b equilateral, percent-joint 019 point, not the superseded 022 force model. Let n_v=8πR²/(√3s²)+2, n_e=3n_v−6, arc length ℓ=2R asin(s/(2R)), member force N=pRs/(2√3) (FIX-A). The 022b film sag reduces V_eff=V₀[1−s/(16R)] at every altitude. It is lost displacement, not carried mass. C scales with this volume for a fixed density/altitude requirement.

Tube material is the carried SiC E410GPa, density3100kg/m³, compression3900MPa. Projection film is 1.5GPa, 970kg/m³, minimum80µm. With each node20g and joints 5% of film+nodes+tubes, close M=L_eff−C=100+B+1.05(m_tube+m_node+m_film). Actual section area and inertia use exact annulus geometry.

```
SF_yield = σ_allow A_t/N
SF_Euler = π² E I/(ℓ² N)
γ_local = 1−0.901[1−exp(−sqrt(r_o/t_w)/16)]             (FIX-B)
SF_local = 0.6 E (t_w/r_o) γ_local A_t/N
SF_film = 2 σ_film t_film/(s p)
η = (ℓ/1000)r_o/(I/A_t)
σ_E = π² E(I/A_t)/ℓ²
φ = [σ_allow+(1+η)σ_E]/2
σ_Perry = φ−sqrt(φ²−σ_allow σ_E)
SF_Perry = σ_Perry A_t/N
SF_global = 0.2 × 4sqrt(1.5) E sqrt(I A_t)/(s R² p)
```

The local knockdown comes from straight isotropic cylinders; its curved-ceramic transfer remains QUESTIONABLE. [NASA SP-8007](https://ntrs.nasa.gov/api/citations/19690013955/downloads/19690013955.pdf)

Reoptimise s∈[0.4,8]m, r_o≤min(0.25m,s/3), film thickness ≥80µm; the resulting optima lie away from the upper spacing/radius bounds. Two independent differential-evolution seeds and a 3.11-million-point grid per scored case check the maxima. A separate Ti/Kapton sensitivity keeps 022b's SiC value and sizes Ti joint mass at the peak pressure: 2n_e C_end N_peak²/r_o, C_end=2.950e−14kg·m/N². Its film is 115.5MPa and 1420kg/m³, minimum25µm. Other 022b folded points are held-geometry comparisons only.

**Numerical scope.** Decimal scalar calculations independently reconstruct mass and pressure capacities from saved geometry. Direct integration of dp/dz checks analytic float roots. Every source artifact hash is checked. These checks validate arithmetic and search resolution, not the physical assumptions or a completed vehicle.
"""
    (ROOT/"METHOD.md").write_text(text)


def card(csv_count,nfi_count):
    opt=winner("optimistic",100.)
    allp=winner("all_019",100.)
    p_opt,p_all=opt["winner"]["point"],allp["winner"]["point"]
    lines=[
        "# MAINLINE-031 — Altitude as the hot-day margin",
        "",
        "ESTIMATE · QUESTIONABLE inputs and transfers · PROJECTION atmosphere, fabrication and named optimisms · Not certification.",
        "",
        f"**Altitude can replace part of the climate mass allowance, conditional on an explicit altitude range.** "
        f"For the optimistic 019 weather set and an illustrative 100m centre-altitude floor, P2 needs "
        f"{p_opt['C_kg']:.2f}kg climate headroom and nominal SF {p_opt['required_nominal_SF']:.6f}, "
        f"instead of 231.74kg climate headroom at the original 500m floor. The least named set remains "
        f"gamma, wrinkling and panel size; its complete bookkeeping reserve is {p_opt['reserve_kg']:.2f}kg "
        f"({100*p_opt['reserve_fraction']:.3f}% of nominal lift), versus 021b's 775.73kg. "
        f"Covering both 019 weather sets at the same 100m floor requires {p_all['C_kg']:.2f}kg "
        f"climate headroom, nominal SF {p_all['required_nominal_SF']:.6f}, and a fourth named optimism: face strength. "
        f"Its total reserve is {p_all['reserve_kg']:.2f}kg ({100*p_all['reserve_fraction']:.3f}%).",
        "",
        "A hull spending all nominal lift has C=0 and floats at 500m on ISA. On the +10K-only day it floats at "
        "130.743m, a 369.257m descent, with 4.352464% more pressure. With the optimistic low pressure and humidity "
        "included, the mathematical root is −23.190m; the conservative hot/low/humid root is −1015.877m. "
        "Those roots lie below sea-level ground and cannot provide clearance at that assumed site. The rough heat-only estimate was sound; "
        "the complete weather requirement changes the conclusion.",
        "",
        "The atmospheric model is a hydrostatic 6.5K/km lapse with constant vapour mole fraction e/p, anchored to each "
        "019 condition at 500 geopotential metres. It is a stated PROJECTION. A single-level temperature, pressure and "
        "humidity does not determine a float altitude. See [METHOD.md](METHOD.md) for equations, objective, alternatives "
        "and the inherited structural equations. The 100m floor is an illustrative requirements option, not an approval.",
        "",
        "![Atmospheric and structural trade](altitude-margin.png)",
        "",
        "**Frozen source points and mass interpretation.** Deleting a climate budget label does not change an already-built hull. "
        "021b's 231.740816kg climate row is already absent mass: its carried mass is 4657.701334kg. "
        "It therefore floats at 997.232m on ISA and 500m on the optimistic hot/low/humid day. "
        "021 rev1 contains a 244.472108kg undifferentiated 5% margin, not separate climate lines. "
        "Its source hardware with that margin unfilled is 4644.970043kg. Adding 019's water, contamination and gas "
        "makes 4824.528170kg and leaves only 64.913980kg headroom. Those are separate, explicit cases.",
        "",
    ]
    rows=[]
    select_days=["ISA","optimistic_heat_only","optimistic_hot_low_wet","conservative_hot_low_wet"]
    for src in P2["source_fixed"]:
        for d in src["days"]:
            if d["day"] in select_days:
                rows.append([src["label"],d["day"],fmt(src["carried_mass_kg"]),fmt(d["z_m"]),
                             fmt(d["p_over_p0"],6),fmt(d["least_SF"],6)])
    lines.append(tab(["Fixed geometry / load case","Day","Carried kg","Float m","p/p₀","Least SF at needed factors"],rows))
    lines += [
        "The gross-mass rows fill all remaining nominal headroom without giving the original geometry added stiffness. "
        "They diagnose pressure exposure; the redesigned points below explicitly put available mass into new faces/core. "
        "All original needed-factor SFs are evaluated unchanged. Full-named-factor vectors on the same geometry are also "
        "in P2.json and ALL-DAYS.csv.",
        "",
        "**Every inherited P2 mode on every design day.** G=global buckling; F=face compression; Cr=core shear crimping; "
        "Cc=core crush; W=wrinkling; D=biaxial intracell dimpling. Uniform pressure is evaluated at the hull centre. "
        "The two tables are the held 021b point and the 021 rev1 point with the same 019 nonclimate inventory added.",
        "",
    ]
    for label in ["021b_held","021_rev1_plus_019_nonclimate"]:
        src=next(r for r in P2["source_fixed"] if r["label"]==label)
        lines.append(f"**{label}.**\n")
        rows=[[d["day"],fmt(d["z_m"],2),fmt(d["p_Pa"]/1000,3)]+
              [fmt(d["sfs"][k],5) for k in ("global","face","crimp","crush","wrinkle","dimple")]
              for d in src["days"]]
        lines.append(tab(["Day","Float m","p kPa","G","F","Cr","Cc","W","D"],rows))
    lines += [
        "**Least climate split under a stated floor.** C is absent mass; the SF entry is the minimum common nominal "
        "pressure multiplier for every mode, with the original p₀ requirement retained as a floor of 1. "
        "The chosen objective minimises C first, then the number of named optimisms, then their maximum logarithmic usage. "
        "Feasible designs attain the atmosphere-imposed C lower bound. A scalar total in kg cannot be obtained by adding "
        "kg to a safety factor. The matched-property structural mass comparison is given separately.",
        "",
    ]
    rows=[]
    for env in ["optimistic","all_019"]:
        for floor in [None,10.,100.,500.]:
            r=next(x for x in AT["floors"] if x["envelope"]==env and x["profile"]=="lapse_mixing"
                   and x["altitude_floor_m"]==floor)
            rows.append([env,"none (math only)" if floor is None else fmt(floor,0),
                         fmt(r["C_kg"]),fmt(max(1,r["nominal_required_SF"]),6),
                         fmt(r["ISA_float_m"]),fmt(r["minimum_float_m"])])
    lines.append(tab(["Weather","Centre floor m","P2 C kg","Required nominal SF","ISA float m","Worst float m"],rows))
    lines += [
        "The 10m floor is ground tangency for a 10m-radius hull above sea-level ground. The 100m option gives about "
        "90m hull clearance. Actual terrain and dynamics must be specified. The both-weather 500m-floor column is "
        "diagnostic only: its conservative high-pressure humid free-float root becomes supersaturated under this lapse model.",
        "",
        "The first pressure extremes are counterintuitive: the low-pressure hot day governs the pressure at free equilibrium "
        "because the hull descends into warmer, denser air. The high-pressure day does not require the same descent.",
        "",
        "**P2 reoptimisation and reserve.** Each row closes gross mass exactly. The 021b model carries 100kg systems "
        "and 179.558128kg nonclimate reserve. It retains 5% structure as the joint floor and charges only the excess "
        "of actual 019 seam/film mass. Beryllium E is 290GPa in the least-set search. All 47 source cores were searched; "
        "the winning core in every listed 021b case is Hexcel CR-III 5056 3/8-1.0.",
        "",
    ]
    rows=[]
    for s in P2["least_optimism_searches"]:
        p=s["winner"]["point"];v=p["needed_values_at_this_geometry"]
        rows.append([s["envelope"],"none" if s["altitude_floor_m"] is None else fmt(s["altitude_floor_m"],0),
                     fmt(p["C_kg"],2),fmt(p["reserve_kg"],2),fmt(100*p["reserve_fraction"],3),
                     "+".join(s["winner"]["subset"]),fmt(s["winner"]["min_max_log_usage"],6),
                     fmt(v["gamma"],6),fmt(v["wrinkle"],6),fmt(v["strength_Pa"]/1e6,3),fmt(v["panel_m"],4)])
    lines.append(tab(["Weather","Floor m","C kg","Total reserve kg","Reserve %","Least named set","Max log use",
                      "Needed γ","Needed wrinkle","Needed MPa","Panel equiv. m"],rows))
    lines += [
        "Bond film remains 0.03lb/ft² per interface in all these least-set points. Panel width means equal seam length "
        "per area, not a guaranteed square panel product. The printed gamma/wrinkle/strength are only what the saved "
        "geometry needs; any unused improvement in the max-usage construction is removed from that column. "
        "At the optimistic 100m-floor point, each face is "
        f"{p_opt['tf_m']*1000:.6f}mm and core is {p_opt['tc_m']*1000:.6f}mm; the both-weather counterpart is "
        f"{p_all['tf_m']*1000:.6f}mm / {p_all['tc_m']*1000:.6f}mm. "
        "The equality SF is a screening boundary, not an engineering design margin.",
        "",
        "The 500m optimistic reference reoptimises to 775.56kg versus the filed 775.73kg. That 0.165kg difference "
        "is continuous search refinement, not an altitude benefit.",
        "",
        "At the optimistic 100m floor, no one- or two-axis set passes: the best two-axis bound reaches "
        f"{max(r['full_bound_score'] for r in opt['tested_subsets'] if len(r['subset'])<opt['cardinality']):.6f}. "
        "For both weather sets there, no three-axis set passes: its best bound reaches "
        f"{max(r['full_bound_score'] for r in allp['tested_subsets'] if len(r['subset'])<allp['cardinality']):.6f}. "
        "These exclusions are within the named bounds and catalogue, not a universal proof about all architectures.",
        "",
    ]
    rows=[]
    for r in P2["reoptimised"]:
        if r["altitude_floor_m"]==100:
            rows.append([r["envelope"],r["label"],fmt(r["least_SF"],6),fmt(r["reserve_kg"],3),
                         fmt(r["tf_m"]*1000,6),fmt(r["tc_m"]*1000,6)])
    lines.append(tab(["Weather, 100m floor","Factors / budget held","Least SF","Reserve kg","Face mm","Core mm"],rows))
    lines += [
        "Holding 021b's filed needed gamma/wrinkle/strength/panel/film values and changing only geometry already passes "
        "the optimistic 100m requirement. It cannot cover both weather sets with those factors. The full-five row "
        "uses E290GPa and all five named endpoints; 021 rev1 full uses its historical full-grade E293.6GPa and a "
        "5% joint placeholder.",
        "",
        "**021 rev1 budget reconstruction.** With the same 179.558kg nonclimate inventory and only its inherited 5% joints, "
        "holding its original needed gamma 0.595318, wrinkle 0.370681 and 283MPa cannot find a feasible split in the "
        "scanned C=0…650kg range. Reoptimising the three named axes does find points; the needed extra face-strength "
        "optimism was absent from the filed source's least pair. This comparator still omits explicit seam/film excess.",
        "",
    ]
    rows=[]
    for s in P2["reconstructed_021_searches"]:
        if s["altitude_floor_m"] in [None,100.]:
            p=s["winner"]["point"];v=p["needed_values_at_this_geometry"]
            rows.append([s["envelope"],"none" if s["altitude_floor_m"] is None else "100",
                         "+".join(s["winner"]["subset"]),fmt(s["winner"]["min_max_log_usage"],6),
                         fmt(v["gamma"],6),fmt(v["wrinkle"],6),fmt(v["strength_Pa"]/1e6,3),
                         fmt(p["reserve_kg"],3)])
    lines.append(tab(["Weather","Floor m","Least named set (placeholder joints)","Max log use","γ","Wrinkle","MPa","Reserve kg"],rows))
    lines += [
        "**Structural mass corresponding to the SF portion.** These figures hold the source 021b properties, panel and "
        "film fixed and independently minimise faces+core+joint mass at p₀ and at the required weather pressure. "
        "They quantify the pressure allowance; they are not added again to the mass-closed designs.",
        "",
    ]
    rows=[]
    for r in P2["reoptimised"]:
        if r["label"]=="021b_fixed_named_values":
            cost=r["matched_property_sf_mass_cost"]
            rows.append([r["envelope"],"none" if r["altitude_floor_m"] is None else fmt(r["altitude_floor_m"],0),
                         fmt(r["C_kg"],3),fmt(r["required_nominal_SF"],6),
                         fmt(cost["extra_hardware_kg"],3),fmt(cost["C_plus_extra_kg"],3),
                         "yes" if r["least_SF"]>=1-1e-8 else "no"])
    lines.append(tab(["Weather","Floor m","Absent C kg","Nominal SF","Added hardware at fixed properties kg",
                      "C + equivalent hardware kg","Mass-closed design feasible?"],rows))
    lines += [
        "A 4.35% pressure rise is a 4.35% fixed-geometry SF demand for all six modes. It is not a universal 4.35% "
        "structural mass increase: face, global buckling and wrinkle constraints couple face/core allocation and joint mass. "
        "The reoptimised values above replace the linear-face / quadratic-mode rough estimates.",
        "",
        "**P3 uses the filed 022b correction.** Its equilateral percent-joint 019 point is the scored source: "
        "N=pRs/(2√3), SP-8007 local gamma, spherical arc length, k=0.2 and 022b's sag-volume loss. "
        "Its 187.937933kg sag loss is a reduction in displacement, not carried mass. "
        "Climate mass is scaled to effective volume for each new design. The pass remains conditional on 3900MPa SiC, "
        "the 1.5GPa projection film, ideal nodes and the inherited six equations.",
        "",
    ]
    rows=[]
    held=P3["source_fixed"][0]
    for d in held["days"]:
        rows.append([d["day"],fmt(d["z_m"],2),fmt(d["p_Pa"]/1000,3)]+
                    [fmt(d["sfs"][k],5) for k in ("yield","euler","local","film","perry","global")])
    lines.append(tab(["022b held day","Float m","p kPa","Yield","Euler","Local","Film","Perry","Global"],rows))
    rows=[]
    for p in P3["reoptimised"]:
        rows.append([p["envelope"],"none" if p["altitude_floor_m"] is None else fmt(p["altitude_floor_m"],0),
                     fmt(p["C_kg"],3),fmt(p["nominal_required_SF"],6),fmt(p["least_SF"],6),
                     fmt(p["spacing_m"],5),fmt(p["outer_radius_m"]*1000,3),
                     fmt(p["wall_m"]*1000,5),fmt(p["film_m"]*1000,5),fmt(p["reserve_kg"],3)])
    lines.append(tab(["Weather","Floor m","P3 C kg","Nominal SF demand","Least actual SF","s m","rₒ mm","Wall mm","Film mm",
                     "Reserve incl. sag kg"],rows))
    lines += [
        "The no-floor rows remain mathematical despite passing the structural screen. The 100m-floor optimistic "
        f"and both-weather points give least SF {p3point('optimistic',100.)['least_SF']:.6f} and "
        f"{p3point('all_019',100.)['least_SF']:.6f}. "
        "The Ti/Kapton sensitivity sizes its joint mass at peak float pressure and still gives only "
        f"{P3['sensitivities'][0]['least_SF']:.6f} and {P3['sensitivities'][1]['least_SF']:.6f}, respectively; "
        "it retains the questionable SiC compression value. Folded CFRP/Zylon and Ti/Kapton held points are also exported, "
        "with their source joint/load assumptions left visible. No extra confidence is assigned to a material because altitude is allowed to change.",
        "",
        "**Requirement to adopt, if this trade is wanted.** One possible requirement is: “A passive R10m hull, with the "
        "specified carried inventory and no ballast or thrust, may float at about 617.1m on ISA and no lower than 100m "
        "centre altitude on the optimistic 019 weather envelope over sea-level ground.” "
        "For both 019 weather sets the analogous ISA equilibrium is about 1464.5m, not 500m. "
        "The organisation must choose the weather envelope, terrain-relative floor, ceiling, clearance and altitude-control "
        "requirement. A strict 500m ISA free-float condition fixes C=0 and is incompatible with those ground-clearance "
        "requirements in the chosen profiles.",
        "",
        "The 027 optimistic climate-plus-internal-gas lower bound of 5.739617% is therefore specific to the old "
        "500m-every-day lift requirement. At the illustrative optimistic 100m floor, those two rows total "
        f"{100*(p_opt['C_kg']+48.89442150186961)/at.L0:.6f}%. "
        "This does not remove water, contamination, films, joints or systems. The complete least-set reserve remains "
        f"{100*p_opt['reserve_fraction']:.3f}%.",
        "",
        "**Atmospheric sensitivity and evidence limits.**",
        "",
    ]
    rows=[]
    for r in AT["floors"]:
        if r["envelope"] in ["optimistic","all_019"] and r["altitude_floor_m"]==100.:
            rows.append([r["envelope"],r["profile"],fmt(r["C_kg"],3),
                         fmt(max(1,r["nominal_required_SF"]),6),fmt(r["ISA_float_m"],3)])
    lines.append(tab(["Weather, 100m floor","Vertical profile","P2 C kg","Nominal SF","ISA float m"],rows))
    lines += [
        "These alternatives show why a lapse rate or sounding is a required input. They are not equally probable weather forecasts. "
        "The calculations retain no internal-pressure structural relief. Unscored effects include local bottom pressure, "
        "thermal mismatch, wind, concentrated attachments, creep, membrane shape change and dynamics. Near-unity scores "
        "do not establish a deployable vehicle.",
        "",
        f"**Validation and delivery.** {VAL['pins_verified']} artifact pins matched. "
        f"{VAL['p2_geometries']} P2 and {VAL['p3_geometries']} P3 geometries pass independent Decimal mass/capacity checks; "
        f"{VAL['atmosphere_ODE_roots']} direct hydrostatic ODE roots match the analytic atmosphere. "
        f"{len(VAL['p2_lower_cardinality_dense_checks'])} denser subset exclusions and second-seed/grid P3 checks passed. "
        f"[ALL-DAYS.csv](ALL-DAYS.csv) has {csv_count} rows with every mode; full precision is in "
        "[P2.json](P2.json), [P3.json](P3.json) and [ATMOSPHERE.json](ATMOSPHERE.json). "
        f"[NFI.json](NFI.json) records {nfi_count} open evidence needs. "
        "[INPUTS.json](INPUTS.json) pins the assignment and source filings, including 021 rev1, 021b, the independent "
        "011b check and the available 022b amendment. Times are measured, never caps. The brief says stop and file; no successor is named.",
        "",
    ]
    (ROOT/"CARD.md").write_text("\n".join(lines))


def main():
    count=export_csv()
    figure()
    nn=nfi()
    method()
    card(count,nn)
    run=json.loads((ROOT/"RUN.json").read_text())
    end=datetime.now(ZoneInfo("America/Vancouver"))
    run.update(completed_at=end.isoformat(timespec="seconds"),
               elapsed_wall_s=(end-datetime.fromisoformat(run["started_at"])).total_seconds(),
               p2_compute_s=P2["elapsed_s"],p3_compute_s=P3["elapsed_s"],
               validation_s=VAL["elapsed_s"],status="COMPLETE",csv_rows=count,nfi_rows=nn)
    (ROOT/"RUN.json").write_text(json.dumps(run,indent=2)+"\n")
    print("Artifacts built;",count,"CSV rows;",nn,"NFI rows")


if __name__=="__main__":
    main()
