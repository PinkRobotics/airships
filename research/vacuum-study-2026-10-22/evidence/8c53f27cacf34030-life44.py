"""MAINLINE-044. Independent, explicitly conditional fatigue and mass screen.

Run from anywhere: TMPDIR=unpublished-local-ref:1ffe4110219d37c0 python3 /absolute/path/life44.py
No owner code is imported. All writable outputs stay beside this script.
"""
from pathlib import Path
import csv
import datetime as dt
import json
import math
import os
import numpy as np

ROOT = Path(__file__).resolve().parent
START = dt.datetime.now(dt.timezone.utc).isoformat()


def read(name):
    return json.loads((ROOT / name).read_text())


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def csvwrite(name, rows):
    with (ROOT / name).open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


p2 = read("inputs/037-check/INPUTS.json")["P2_028b_selected"]["point"]
inp = read("inputs/028b/INPUTS.json")
load37 = read("inputs/037/RESULTS.json")
b37 = read("inputs/037b/COMPUTE.json")
vac = read("inputs/034-check/inputs/034/INPUTS.json")
R = 10.0
A = 4 * math.pi * R**2
p = vac["environment"]["p_external_Pa"]
tf, tc = p2["tf_m"], p2["tc_m"]
Ef, nu, da = 290e9, 0.0752, (23.6 - 11.3) * 1e-6
rho_c, Gc, Gl = (p2["core"][k] for k in ["rho", "Gc_Pa", "Gl_Pa"])
psi = 6894.757293168361
Wtyp, Wmin, Ltyp, Lmin = [x * psi for x in [35, 25, 55, 45]]
Kc = 67e9 * (rho_c / 2700) / 2
Sf = Ef / (1 - nu)
rho_pad, Sy_pad = 2700.0, 276e6
Tlo, Thi = b37["service"]["t_cold_K"], b37["service"]["t_hot_K"]
dT = Thi - Tlo
Tmid = (Thi + Tlo) / 2
Tair = 284.9
cold_cure, hot_cure = 366.4833333333333, 394.2611111111111
qsteady = 0.5 * 1.16726833074618 * (35 * 0.514444)**2
gust_limit = load37["wind"]["gust_pressure_increment_Pa"] if "gust_pressure_increment_Pa" in load37["wind"] else 290.63372090048773
Fpad = 48258.794022345304

# Source facts and transparent graphical extraction. Normalized core strength
# coordinates are measured in the retained 840x590 Fig.10 crop, not invented S-N.
core_pixels = {
    "W": [[249,100],[255,100],[378,180],[406,180],[497,278],[512,278],[633,352]],
    "L": [[252,182],[267,182],[409,268],[436,268],[446,268],[591,357],[596,357],[749,421]],
}
fits = {}
digitized = []
for direction, coords in core_pixels.items():
    logs, levels = [], []
    for x,y in coords:
        logn = 2 + 5 * (x - 40) / (808 - 40)
        s = (522 - y) / (522 - 32)
        logs.append(logn)
        levels.append(s)
        digitized.append(dict(direction=direction, x_pixel=x, y_pixel=y,
                              N_graphical=10**logn, normalized_amplitude=s))
    slope, intercept = np.polyfit(logs, levels, 1)
    fits[direction] = dict(a=float(intercept), b=float(-slope),
                          minimum_test_level=min(levels), maximum_test_level=max(levels),
                          shortest_test_N=10**min(logs), longest_test_N=10**max(logs))
# The article supplies the precise cycle count for the last W coupon.
fits["W"]["cap_N"] = 718394.0
fits["L"]["cap_N"] = fits["L"]["longest_test_N"]

yahr_n = [100,200,500,1000,2000,5000,7000,10000,20000,50000,100000,
          200000,500000,1e6,2e6,5e6,1e7,2e7,5e7,1e8,2e8,5e8,1e9]
yahr_sa = [420.28,325.43,239.94,184.71,137.89,95.01,75.36,63.02,53.37,
           49.50,47.50,37.68,30.06,26.68,24.48,22.68,21.79,21.18,
           20.66,20.39,20.21,20.06,19.97]
source_data = {
    "core": {
        "source": "Bianchi, Aglietti, Richardson (2012), doi:10.1007/s10443-010-9184-5",
        "url": "https://link.springer.com/article/10.1007/s10443-010-9184-5",
        "page": "printed 107, PDF page 11, Fig.10",
        "test": "5056 honeycomb 5.3 pcf, R=-1, room temperature, shear ultimate failure",
        "transfer": "PROJECTION: normalized strength transfer to 1.0 pcf CR-III; not an allowable",
        "digitization_uncertainty_absolute_fraction": 0.03,
        "fits": fits, "digitized": digitized,
        "low_stress_policy": "finite semilog extrapolation, explicitly marked; also retain tested-horizon cap. Neither is an installed-life guarantee.",
        "high_stress_policy": "report fit extrapolation explicitly; static overload is separate",
        "mean_stress_policy": "Goodman using absolute shear mean and static shear strength, PROJECTION"
    },
    "pad": {
        "source": "G.T. Yahr, Fatigue Design Curves for 6061-T6 Aluminum, Table 1",
        "url": "https://www.osti.gov/servlets/purl/10157028",
        "page": "PDF page 12",
        "N": yahr_n, "Sa_maximum_mean_MPa": yahr_sa,
        "note": "Original ORNL design-curve construction; factors on stress/life already included. No further Goodman correction to this column. Local notch, finish, corrosion and pad support remain unqualified.",
        "best_fit_zero_mean": "Sa_MPa=14479/sqrt(N)+96.5; not used as the design curve"
    },
    "Be": {
        "source": "Brush Wellman author D.E. Dombrowski et al., IAEA vol.5, printed pp60-61, Figs29-30",
        "url": "https://www-pub.iaea.org/MTCD/Publications/PDF/Pub23vol5_web.pdf",
        "manufacturer_record": "TM-778 (1985), reported by its manufacturer; original internal report not obtained",
        "grade_form": "smooth S-200F VHP block specimen, R=-1 rotating beam",
        "runout_screen_MPa": 262.0, "cap_N": 1e7,
        "qualification": "NOT an SR200 sheet curve; cap is a conditional bookkeeping rule, not a confidence bound. Figure directions override inconsistent adjacent prose."
    },
    "AF163": {
        "url": "https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf?fn=TDS_AF163-2_R1.pdf",
        "page": "printed p9 / PDF p9",
        "wide_area_maximum_psi": 1500, "wide_area_R": 0.1, "wide_area_runout_N": 1e7,
        "double_lap_Ti_AF163_2K_006": [[4500,1.58e4],[4000,5.28e4],[3500,4.75e5],[3000,2.67e6]],
        "double_lap_runout": [2200,1.03e7],
        "transfer": "Not the 0.015 lb/ft2 U-film Be/honeycomb joint; no peel or environmental life qualification."
    },
    "scarf": {
        "url": "https://www.hexcel.com/wp-content/uploads/2025/12/HexBond_312_DataSheet_eu.pdf",
        "product": "HexBond312 unsupported 70 g/m2",
        "cure_C": 120, "room_temperature_Al_lap_shear_MPa": 37,
        "SN": None, "note": "No S-N in opened datasheet; static 10 MPa seam screen is not a fatigue curve."
    }
}
write("SOURCE-DATA.json", source_data)
csvwrite("CORE-DIGITIZATION.csv", digitized)


def core_life(amplitude, mean, strength, direction="W", shift=0.0):
    peak = abs(mean) + amplitude
    if abs(mean) >= strength:
        return dict(N=None, equivalent_fraction=None, static_SF=strength/peak,
                    classification="mean_over_static_strength")
    eq = amplitude / (strength - abs(mean))
    f = fits[direction]
    logn = (f["a"] + shift - eq) / f["b"]
    # Extrapolation is indispensable for the declared million-cycle decade.
    # Retain a separate horizon-limited N so that extrapolated compliance
    # cannot be mistaken for demonstrated coverage.
    n = max(1.0, 10 ** max(-5, min(15, logn)))
    status = "interpolation"
    if eq < f["minimum_test_level"]:
        status = "low_stress_extrapolation"
    elif eq > f["maximum_test_level"]:
        status = "high_stress_extrapolation"
    if peak > strength:
        status += ";static_overload"
    return dict(N=n, test_horizon_capped_N=min(n,f["cap_N"]),
                equivalent_fraction=eq, static_SF=strength/peak if peak else None,
                classification=status)


def pad_life(sa_MPa):
    if sa_MPa <= yahr_sa[-1]:
        return 1e9, "low_stress_table_horizon_cap"
    if sa_MPa > yahr_sa[0]:
        return None, "outside_table_high_stress"
    return float(10**np.interp(sa_MPa, yahr_sa[::-1], np.log10(yahr_n[::-1]))), "table_interpolation"


def pointgeom(face, core, scarf, coreobj=None):
    co = coreobj or p2["core"]
    lap = scarf * face
    aa, bb = .6096-lap, 1.8288-lap
    assert aa > 0 and bb > 0
    seam = A * (1/aa + 1/bb)
    nodes = A/(aa*bb)
    mass = dict(faces=2*A*face*1850, core=A*core*co["rho"],
                bond=2*A*.015*4.88242763638305,
                scarf=2*seam*math.hypot(lap,face)*.07,
                splice=seam*core*.0005*500, seal=seam*.002)
    return dict(tf_m=face,tc_m=core,scarf_ratio=scarf,lap_m=lap,seam_m=seam,
                nodes=nodes,masses_kg=mass,physical_structural_joining_kg=sum(mass.values()))


geo = pointgeom(tf,tc,30)
fix_record = next(x for x in b37["fixes"] if "200 F" in x["fix"] and "30.34:1" in x["fix"])
fix_ratio = b37["scarf_fix"][1]["r_need"]
fixgeo = pointgeom(fix_record["tf_mm"]/1000,fix_record["tc_mm"]/1000,fix_ratio)


def gas_topup(g):
    # 034 law, resized seam/nodes/polymer inventory. No perpetual TML reset.
    m = g["masses_kg"]
    volume = 4*math.pi*R**3/3 - m["faces"]/1850 - m["core"]/2700
    volume -= (m["bond"]+m["scarf"])/1250 + m["splice"]/500
    q_mbar_l_s = .001*(g["seam_m"]+g["nodes"])+.01
    dp_leak = q_mbar_l_s*.1*86400/volume
    B = .1*(.0485*m["bond"]+.001*m["core"]+.01*(m["scarf"]+m["splice"]+m["seal"]))
    # Source's deliberately assumed 10 Barrer polymer permeation. Dry gas
    # fractions normalized; water partial pressure separately specified.
    dry_sum = sum(v["dry_x"] for v in vac["species"].values())
    partials = {k: (1000 if k=="H2O" else (p-1000)*v["dry_x"]/dry_sum)
                for k,v in vac["species"].items()}
    h = .07/1250
    permeation_mol_d = sum(10*3.34645e-16*(g["seam_m"]*h/g["lap_m"])*pp*86400 for pp in partials.values())
    dp_perm = permeation_mol_d*8.31446261815324*Tair/volume
    outg_dp_inventory = B/.01801528*8.31446261815324*Tair/volume
    rows = []
    for day in range(1,366):
        dp = dp_leak+dp_perm+outg_dp_inventory*(math.exp(-(day-1))-math.exp(-day))
        rows.append(dict(day=day,pressure_range_Pa=dp,pressure_low_Pa=10,pressure_high_Pa=10+dp))
    return dict(volume_m3=volume,conditioned_B_kg=B,leak_mbar_l_s=q_mbar_l_s,
                leak_dp_Pa_day=dp_leak,permeation_dp_Pa_day=dp_perm,rows=rows,
                first_day_Pa=rows[0]["pressure_range_Pa"],day_365_Pa=rows[-1]["pressure_range_Pa"],
                note="Re-sized PROJECTION from 034; daily top-ups do not vent. 90% conditioning and leak rates unmeasured. Constant 284.9 K; thermal gas-pressure cycling is a separate small envelope.")


gas = gas_topup(geo)
gas_fix = gas_topup(fixgeo)
csvwrite("DAILY-TOPUP.csv", gas["rows"])

# Deliberate spectrum, not a climatological measurement or FAA occurrence table.
# Pressure cycle low/high are increments above the reference external pressure.
dp_up = 101325*((1-.0065*500/288.15)**5.2558797 -
               (1-.0065*1000/288.15)**5.2558797)
pressure_rows = [
    dict(id="weather_restricted",count=365,dp_low=-100,dp_high=100,kind="weather"),
    dict(id="altitude_500_to_1000_m",count=12,dp_low=-dp_up,dp_high=0,kind="altitude"),
    dict(id="gust_small",count=100000,dp_low=0,dp_high=25,kind="gust"),
    dict(id="gust_medium",count=10000,dp_low=0,dp_high=100,kind="gust"),
    dict(id="gust_limit",count=100,dp_low=0,dp_high=gust_limit,kind="gust"),
]
pad_rows = [
    dict(id="moor_small",count=100000,f_low=0,f_high=.10),
    dict(id="moor_medium",count=10000,f_low=.10,f_high=.30),
    dict(id="moor_large",count=1000,f_low=.30,f_high=.60),
    dict(id="dock_handling",count=730,f_low=0,f_high=1),
]
spectrum = dict(tag="PROJECTION",year_days=365,
                thermal_cycles=365,outer_T_K=[Tlo,Thi],
                inner_T_K=[Tlo+load37["p2_thermal"]["coated_outer"]["dT_through_at_max_K"],
                            load37["p2_thermal"]["coated_outer"]["T_inner_subsolar_K"]],
                inner_night_basis="PROJECTION: equal and opposite maximum through-core gradient; 037 did not file night inner T",
                gradient_T_K=[-load37["p2_thermal"]["coated_outer"]["dT_through_at_max_K"],
                               load37["p2_thermal"]["coated_outer"]["dT_through_at_max_K"]],
                pressure_rows=pressure_rows,pad_rows=pad_rows,daily_topup_count=365,
                scheduled_full_vent_count=0,commissioning_pressure_half_cycles=1,
                full_vent_sensitivity_cycles_per_year=[0,12,365],
                count_multipliers=[.1,1,10],
                restrictions="Reference residence/mooring at 500m; flights only upward; weather excursion restricted to +/-100Pa; gust severity follows 037, occurrences are assumptions. Broad-weather, descent-to-sea-level and 70kn mooring scenarios are separate static rejections.")
write("SPECTRUM.json",spectrum)


def thermal_case(g, Tstressfree, label):
    f,c = g["tf_m"],g["tc_m"]
    rigid_k = da*Ef*f*math.sqrt(Gc/(Ef*f*c))
    edge_k = math.sqrt(2*Kc*Gc)
    total_k = 2*Sf*f+Kc*c
    coupled_kT = -da*(2*Sf*f/total_k)
    coupled_kp = -R/(2*total_k)
    pc = p+qsteady
    cases=[]
    for model in ["037_rigid_thermal","037b_free_edge_thermal","044_coupled_free_edge"]:
        if model=="037_rigid_thermal":
            vals=[rigid_k*(T-Tstressfree) for T in [Tlo,Thi]]
        elif model=="037b_free_edge_thermal":
            vals=[edge_k*da*(Tstressfree-T) for T in [Tlo,Thi]]
        else:
            vals=[edge_k*(coupled_kT*(T-Tstressfree)+coupled_kp*pc) for T in [Tlo,Thi]]
        mean=sum(vals)/2; amp=abs(vals[1]-vals[0])/2
        for strength_name,strength,direction in [("typical_W",Wtyp,"W"),("minimum_average_W",Wmin,"W"),
                                                  ("typical_L",Ltyp,"L"),("minimum_average_L",Lmin,"L")]:
            scale=1 if direction=="W" else math.sqrt(Gl/Gc)
            aa,mm=amp*scale,mean*scale
            ans=core_life(aa,mm,strength,direction)
            cases.append(dict(point=label,model=model,T_stressfree_K=Tstressfree,basis=strength_name,
                              tau_cold_Pa=vals[0]*scale,tau_hot_Pa=vals[1]*scale,amplitude_Pa=aa,mean_Pa=mm,
                              thermal_only_damage_year=None if ans["N"] is None else 365/ans["N"],
                              thermal_only_life_days=ans["N"],**ans))
    return cases


thermal=[]
for Tref,name in [(Tair,"028b_ambient_reference"),(Tmid,"028b_mid_swing"),
                  (Tlo,"028b_cold_reference"),(hot_cure,"028b_250F_cure"),
                  (cold_cure,"028b_200F_cure")]:
    thermal.extend(thermal_case(geo,Tref,name))
thermal.extend(thermal_case(fixgeo,cold_cure,"037b_200F_plus_scarf_fix"))
csvwrite("THERMAL-LIFE.csv",thermal)


def component_spectrum(g, name, Tref, fullvents=0, notch=1.0):
    f,c=g["tf_m"],g["tc_m"]
    total_k=2*Sf*f+Kc*c
    edge_k=math.sqrt(2*Kc*Gc)
    # This is a new force-balanced membrane/edge sensitivity, not a finding
    # that the as-built shell necessarily realizes these local boundary conditions.
    edge_kp=-edge_k*R/(2*total_k)
    edge_kT=-edge_k*da*2*Sf*f/total_k
    base_edge=edge_kT*(Tmid-Tref)+edge_kp*(p+qsteady)
    face_kp=R/(4*f)
    face_kT=Kc*c*da/(2*f)
    thermal_face_amp=load37["p2_thermal"]["coated_outer"]["gradient_stress_Pa"]
    thermal_face_amp+=load37["p2_thermal"]["coated_outer"]["pattern"]["bending_stress_Pa"]
    thermal_face_amp+=face_kT*dT/2
    scarf_den=g["scarf_ratio"]+1/g["scarf_ratio"]
    local=[]
    def row(id,count,faceamp,edgelo,edgehi,face_peak,kind):
        em=(edgelo+edgehi)/2; ea=abs(edgehi-edgelo)/2
        beamp=notch*faceamp
        beN=1e7 if beamp<=262e6 else None
        # Cap applied only as a transfer scenario. Bond peel remains unmapped.
        bond_peak=max(abs(edgelo),abs(edgehi))
        bondN=1e7 if bond_peak<=1500*psi else None
        core=core_life(ea,em,Wmin)
        local.append(dict(point=name,case=id,kind=kind,count=count,
            Be_amplitude_MPa=beamp/1e6,Be_peak_compression_MPa=face_peak/1e6,
            Be_proxy_N=beN,Be_proxy_damage=None if beN is None else count/beN,
            core_amplitude_kPa=ea/1000,core_mean_kPa=em/1000,
            core_N=core["N"],core_status=core["classification"],
            core_static_SF=core["static_SF"],
            core_damage=None if core["N"] is None else count/core["N"],
            AF163_peak_shear_kPa=bond_peak/1000,AF163_proxy_N=bondN,
            AF163_proxy_damage=None if bondN is None else count/bondN,
            scarf_amplitude_MPa=faceamp/scarf_den/1e6,
            scarf_peak_shear_MPa=face_peak/scarf_den/1e6,
            scarf_N=None,scarf_damage=None))
    residual=face_kT*(Tref-Tlo)
    facepeak=face_kp*(p+qsteady)+residual+thermal_face_amp
    row("thermal_daily",365,thermal_face_amp,base_edge-edge_kT*dT/2,
        base_edge+edge_kT*dT/2,facepeak,"thermal")
    for r in pressure_rows:
        dpl,dph=r["dp_low"],r["dp_high"]
        row(r["id"],r["count"],face_kp*(dph-dpl)/2,
            base_edge+edge_kp*dpl,base_edge+edge_kp*dph,
            face_kp*(p+qsteady+dph)+residual,"pressure")
    gg=gas_topup(g)
    for rr in gg["rows"]:
        dp=rr["pressure_range_Pa"]
        row(f"topup_day_{rr['day']}",1,face_kp*dp/2,base_edge-edge_kp*dp,base_edge,
            face_kp*(p+qsteady)+residual,"topup")
    if fullvents:
        # At Tmid; no flight-q during full vent. Return cycle is counted once.
        edge_vent=edge_kT*(Tmid-Tref)
        edge_vac=edge_vent+edge_kp*(p-10)
        row("full_vent_and_evacuate",fullvents,face_kp*(p-10)/2,
            edge_vent,edge_vac,face_kp*(p-10)+residual,"full_vent")
    sums={}
    for prefix in ["Be_proxy","core","AF163_proxy"]:
        vv=[x[prefix+"_damage"] for x in local]
        damage=None if any(v is None for v in vv) else sum(vv)
        sums[prefix]=dict(D_year=damage,life_days=None if not damage else 365/damage)
    # One commissioning half cycle, not a recurring annual full evacuation.
    edge_vent=edge_kT*(Tmid-Tref); edge_vac=edge_vent+edge_kp*(p-10)
    core_init=core_life(abs(edge_vac-edge_vent)/2,(edge_vac+edge_vent)/2,Wmin)
    sums["commissioning_core_damage"]=None if core_init["N"] is None else .5/core_init["N"]
    sums["scarf"]=dict(D_year=None,life_days=None,reason="HexBond312 Be-scarf S-N and peel unavailable")
    sums["qualification"]="None: material, mean-stress, boundary and environmental transfers are PROJECTION"
    return local,sums


all_component_rows=[]
components={}
for name,g,tref in [("028b_250F",geo,hot_cure),("028b_200F",geo,cold_cure),
                    ("037b_fix",fixgeo,cold_cure)]:
    for vents in [0,12,365]:
        rows,sums=component_spectrum(g,name,tref,vents)
        components[f"{name}_vents_{vents}"]=sums
        if vents==0: all_component_rows.extend(rows)
csvwrite("COMPONENT-CYCLES.csv",all_component_rows)


def pad_damage(peak_MPa, area, n_pads=6, force=Fpad):
    out=[]
    # Extra conservative scalar reserve for ambient pressure/2. It is NOT a
    # validated multiaxial criterion; output also reports shear alone.
    strength_eff=Wmin-p/2
    tau_peak=force/(area*n_pads)
    for row in pad_rows:
        lo,hi=row["f_low"],row["f_high"]
        sa=peak_MPa*(hi-lo)/2
        N,status=pad_life(sa)
        cm=tau_peak*(hi+lo)/2
        ca=tau_peak*(hi-lo)/2
        core=core_life(ca,cm,strength_eff)
        out.append(dict(case=row["id"],count=row["count"],Sa_MPa=sa,N_pad=N,pad_status=status,
                        D_pad=None if N is None else row["count"]/N,
                        core_tau_peak_Pa=tau_peak*hi,
                        core_N=core["N"],core_status=core["classification"],
                        core_SF_shear_alone=Wmin/(tau_peak*hi),
                        core_SF_with_scalar_pressure_reserve=core["static_SF"],
                        D_core=None if core["N"] is None else row["count"]/core["N"]))
    def dmg(k):
        return None if any(x[k] is None for x in out) else sum(x[k] for x in out)
    return out,dict(plate_D_year=dmg("D_pad"),core_D_year=dmg("D_core"),
                   core_peak_Pa=tau_peak,peak_plate_MPa=peak_MPa)


def pad_geometry(n_pads,area,peak_MPa,force=Fpad):
    a=math.sqrt(area/math.pi);b=.025;nu_al=.33;F=force/n_pads
    t2=3*F*((1+nu_al)*math.log(a/b)+1-(1-nu_al)*b*b/(4*a*a))/(2*math.pi*peak_MPa*1e6)
    t=math.sqrt(t2)
    return dict(n_pads=n_pads,area_each_m2=area,radius_m=a,t_m=t,
                total_plate_mass_kg=n_pads*area*t*rho_pad,
                plate_model="simply supported circle, finite uniform boss; no lugs, bolts or backing included")


pad_area0=Fpad/(6*Wtyp)
pad0=pad_geometry(6,pad_area0,276)
pad0rows,pad0damage=pad_damage(276,pad_area0)
csvwrite("PAD-BASE-CYCLES.csv",pad0rows)
pad_restore=[]
for n in [1,6]:
    for force_name,force in [("20m_s",Fpad),("70kn",111753.39627328068)]:
        # Peak shear = half the strength left after the scalar p/2 reservation.
        area=force/(n*.5*(Wmin-p/2))
        for D10 in [1.0,.1]:
            lo,hi=1.0,262.0
            for _ in range(70):
                mid=(lo+hi)/2
                _,dd=pad_damage(mid,area,n,force)
                if 10*(dd["plate_D_year"]+dd["core_D_year"])>D10: hi=mid
                else: lo=mid
            peak=lo
            geom=pad_geometry(n,area,peak,force)
            rows,damage=pad_damage(peak,area,n,force)
            feasible=10*(damage["plate_D_year"]+damage["core_D_year"])<=D10*(1+1e-10)
            pad_restore.append(dict(force_case=force_name,target_combined_D10=D10,feasible_in_projection=feasible,
                                    **geom,**damage,
                                    addition_vs_corrected_six_pad20_kg=geom["total_plate_mass_kg"]-pad0["total_plate_mass_kg"]))
write("PAD-RESTORE.json",pad_restore)

# Interpolation/projection sensitivity: mean stress, density, notch, counts.
thermal_sens=[]
for swing in [5,10,20,dT,40,50,74.16485740453288]:
    for strength_name,strength in [("typ_W",Wtyp),("min_W",Wmin)]:
        k=da*math.sqrt(2*Kc*Gc)
        mean=k*(cold_cure-Tmid)
        for shift in [-.03,0,.03]:
            c=core_life(k*swing/2,mean,strength,shift=shift)
            thermal_sens.append(dict(swing_K=swing,basis=strength_name,curve_vertical_shift=shift,
                                     **c,thermal_only_life_days=c["N"]))
csvwrite("CORE-SENSITIVITY.csv",thermal_sens)
denser=[]
for co in inp["cores"]:
    if co["name"].startswith("Hexcel CR-III 5056 3/8"):
        kb=67e9*co["rho"]/2700/2
        amp_r=da*dT/2*math.sqrt(Ef*tf*co["Gc_Pa"]/tc)
        amp_e=da*dT/2*math.sqrt(2*kb*co["Gc_Pa"])
        mean_e=da*(cold_cure-Tmid)*math.sqrt(2*kb*co["Gc_Pa"])
        s=co["shear_strength_W_Pa"]
        ans=core_life(amp_e,mean_e,s)
        smin={1.0:25,1.6:38,2.3:62,3.0:100}[co["pcf"]]*psi
        ansmin=core_life(amp_e,mean_e,smin)
        denser.append(dict(core=co["name"],additional_core_kg=A*tc*(co["rho"]-rho_c),
                           rigid_thermal_amplitude_kPa=amp_r/1000,
                           free_edge_thermal_amplitude_kPa=amp_e/1000,
                           free_edge_thermal_mean_kPa=mean_e/1000,
                           typical_W_Pa=s,minimum_average_W_Pa=smin,
                           minimum_basis=ansmin,**ans))
write("DENSER-CORE.json",denser)

scarf60=pointgeom(tf,tc,60)
static_base=p2["at_full_named"]["least_seven_screen_SF"]*p
static_cases=[]
for label,addition in [
    ("reference_broad_pressure_only",0),
    ("restricted_weather_plus_flight_limit",100+qsteady+gust_limit),
    ("weather_plus_2kPa",2000),
    ("descent_500m_to_sea_level",101325-p),
    ("70kn_uniform_pressure",756.8555499659582)]:
    sf=static_base/(p+addition)
    static_cases.append(dict(case=label,pressure_Pa=p+addition,
                             least_028b_projected_SF=sf,passes_screen=sf>=1,
                             qualified_life_days=None,
                             completed_qualified_cycles=0 if sf<1 else None))
pressure_headroom=static_base-p
pad_design=next(x for x in pad_restore if x["n_pads"]==6 and x["force_case"]=="20m_s" and x["target_combined_D10"]==.1)
join_delta=scarf60["physical_structural_joining_kg"]-geo["physical_structural_joining_kg"]
mass_options={
    "037b_filed_fix": dict(filed_added_join_kg=fix_record["mass_change_kg"],
                          independently_recomputed_physical_total_delta_kg=fixgeo["physical_structural_joining_kg"]-geo["physical_structural_joining_kg"],
                          note="Different geometry from 037 full-named point; compare like-for-like via totals, not the 0.12kg label alone."),
    "scarf_60_to_1": dict(added_joining_kg=join_delta,new_overlap_m=scarf60["lap_m"],
                          pressure_mean_shear_MPa=(p*R/(4*tf))/(60+1/60)/1e6,
                          qualification="Stress reduction only; no sourced HexBond312 Be-scarf fatigue life."),
    "AF015_to_AF030": dict(added_kg=geo["masses_kg"]["bond"]),
    "AF015_to_AF060": dict(added_kg=3*geo["masses_kg"]["bond"],
                          qualification="Matches U-film weight in one fatigue test, still not substrate/cure/peel geometry."),
    "six_pad_20m_s_D10_01": pad_design,
    "scarf60_plus_six_pad_D10_01": dict(added_kg=join_delta+pad_design["addition_vs_corrected_six_pad20_kg"],
                                     gross_with_unchanged_budget_kg=4889.442150186961+join_delta+pad_design["addition_vs_corrected_six_pad20_kg"],
                                     qualification="Necessary candidate stress reductions, NOT a demonstrated ten-year hull. Fixed reserve and 100kg systems remain charged. No payload or float credit."),
    "inspection_repair": dict(installed_monitoring_kg=None,replacement_patch_kg_m2=2*tf*1850+tc*rho_c+2*.015*4.88242763638305,
                              recurring_annual_kg=None,
                              qualification="NDE detection limit and crack/debond growth absent; interval cannot be validated from bulk S-N. Replacing metal pad plates does not reset core, scarf or Be fatigue.")
}
combined_static=[]
for label,g,Tref in [("028b_full_named_250F",geo,hot_cure),
                      ("037b_fix_200F",fixgeo,cold_cure),
                      ("028b_200F_scarf60",scarf60,cold_cure)]:
    for loading,dp in [("vacuum_only",0),("weather_flight_limit",100+qsteady+gust_limit),
                        ("sea_level",101325-p)]:
        f,c=g["tf_m"],g["tc_m"]
        pressure_stress=(p+dp)*R/(4*f)
        cure_stress=Kc*c*da*(Tref-Tlo)/(2*f)
        local_thermal=load37["p2_thermal"]["coated_outer"]["gradient_stress_Pa"]+load37["p2_thermal"]["coated_outer"]["pattern"]["bending_stress_Pa"]
        s=(pressure_stress+cure_stress+local_thermal)/(g["scarf_ratio"]+1/g["scarf_ratio"])
        combined_static.append(dict(point=label,loading=loading,
                                    face_compression_MPa=(pressure_stress+cure_stress+local_thermal)/1e6,
                                    scarf_shear_MPa=s/1e6,scarf_screen_SF=10e6/s,
                                    note="Absolute envelope; pressure, residual and local thermal peaks may not coincide. Does not establish a complete local stress field."))
write("COMBINED-STATIC.json",combined_static)
sens=[]
for mode in ["037_rigid_thermal","037b_free_edge_thermal"]:
    label="028b_ambient_reference" if mode=="037_rigid_thermal" else "037b_200F_plus_scarf_fix"
    for direction,strength in [("W",Wmin),("L",Lmin)]:
        x=next(x for x in thermal if x["point"]==label and x["model"]==mode and x["basis"]=="minimum_average_"+direction)
        for shift in [-.03,0,.03]:
            v=core_life(x["amplitude_Pa"],x["mean_Pa"],strength,direction,shift=shift)
            for cycles_day in [.1,1,10]:
                sens.append(dict(point=label,model=mode,direction=direction,curve_shift=shift,cycles_per_day=cycles_day,
                                 life_days=v["N"]/cycles_day,static_SF=v["static_SF"],
                                 classification=v["classification"]))
write("LIFE-SENSITIVITY.json",sens)
stress_targets=[]
for mode,label in [("037_rigid_thermal","028b_ambient_reference"),
                    ("037b_free_edge_thermal","037b_200F_plus_scarf_fix")]:
    x=next(x for x in thermal if x["point"]==label and x["model"]==mode and x["basis"]=="minimum_average_W")
    for D10 in [1,.1]:
        N=3650/D10
        allowed_fraction=fits["W"]["a"]-fits["W"]["b"]*math.log10(N)
        allowed_amplitude=allowed_fraction*(Wmin-abs(x["mean_Pa"]))
        stress_targets.append(dict(model=mode,target_thermal_D10=D10,
                                   allowable_daily_amplitude_kPa=allowed_amplitude/1000,
                                   fixed_mean_allowable_swing_K=dT*allowed_amplitude/x["amplitude_Pa"],
                                   mean_held_kPa=x["mean_Pa"]/1000,
                                   note="Thermal damage only; changing mean temperature requires a new calculation. Climate/coating implementation mass unknown."))
write("THERMAL-RESTORE.json",stress_targets)
contact_fraction=rho_c/2700
bond_contact=[]
for name,macro in [("037b_200F_cold_thermal",160202.13582979508),
                    ("037b_250F_cold_thermal",206844.70927092925),
                    ("037_rigid_ambient_hot",143787.7618694373)]:
    bond_contact.append(dict(case=name,nominal_gross_shear_kPa=macro/1000,
                             ideal_bare_wall_contact_fraction=contact_fraction,
                             no_fillet_contact_area_average_MPa=macro/contact_fraction/1e6,
                             minimum_effective_area_fraction_for_1500psi=macro/(1500*psi),
                             note="Geometric contact-area sensitivity only, not a resolved fillet stress. Actual wetted fillet area, peel and edge concentrations are unknown."))
write("BOND-CONTACT.json",bond_contact)
results=dict(schema=1,unit="vacuum-mainline044-fatigue-and-life-1020",status="ESTIMATE",
             tags=["QUESTIONABLE","PROJECTION"],qualified_hull_life_days=None,
             geometry_028b_full_named=geo,geometry_037b_fix=fixgeo,
             gas_topup={k:v for k,v in gas.items() if k!="rows"},
             gas_topup_fix={k:v for k,v in gas_fix.items() if k!="rows"},
             thermal_cases=thermal,component_summaries=components,
             pad_base_geometry=pad0,pad_base_damage=pad0damage,
             pad_plate_only_life_days=365/pad0damage["plate_D_year"],
             static_cases=static_cases,pressure_headroom_Pa=pressure_headroom,
             combined_static=combined_static,thermal_restore=stress_targets,
             bond_contact_sensitivity=bond_contact,
             core_fits=fits,mass_options=mass_options,
             commissioning_note="One pressure half-cycle; not multiplied by years. Life days from annual D omit its tiny one-time debit; recorded separately.",
             methodology="Miner sum n/N; no statistical reliability claimed. SF failure overrides fatigue extrapolation. Censored/horizon-capped and extrapolated curve use identified in row files.",
             started_at=START,ended_at=dt.datetime.now(dt.timezone.utc).isoformat())
write("RESULTS.json",results)

# Independent source / invariant checks, not a test suite mirroring every line.
checks=[]
def check(name,a,b,rtol=1e-9,atol=1e-8):
    ok=math.isclose(a,b,rel_tol=rtol,abs_tol=atol)
    checks.append(dict(check=name,calculated=a,reference=b,pass_=ok))
check("037 face pressure MPa",p*R/(4*tf),298435856.7214987)
check("028b face mass",geo["masses_kg"]["faces"],p2["masses_kg"]["faces"])
check("028b core mass",geo["masses_kg"]["core"],p2["masses_kg"]["core"])
check("028b scarf mass",geo["masses_kg"]["scarf"],p2["joining"]["scarf_film_kg"])
check("028b seam length",geo["seam_m"],p2["joining"]["seam_length_m"])
check("037 rigid swing shear",da*dT*math.sqrt(Ef*tf*Gc/tc),263037.29582667246)
check("037b free edge 200F cold",da*(cold_cure-Tlo)*math.sqrt(2*Kc*Gc),160202.13582979508)
check("037b biaxial core modulus",Kc,b37["k_biax_al_MPa"]*1e6)
check("037-check six pad plate corrected mass",pad0["total_plate_mass_kg"],3.414034,rtol=2e-6)
check("Yahr tabulated 2000-cycle ordinate inversion",pad_life(137.89)[0],2000)
check("finite outgassing first+tail inventory",sum(math.exp(-(i-1))-math.exp(-i) for i in range(1,366)),1)
check("core pcf conversion",rho_c,16.018463373960138)
for temp in [Tlo,Tmid,Thi]:
    for pressure in [0,p/2,p]:
        # Check force balance independently from the edge coefficient formulas.
        delta=temp-cold_cure
        common_strain=((2*Sf*tf*11.3e-6+Kc*tc*23.6e-6)*delta-pressure*R/2)/(2*Sf*tf+Kc*tc)
        nf=2*tf*Sf*(common_strain-11.3e-6*delta)
        nc=tc*Kc*(common_strain-23.6e-6*delta)
        check(f"coupled membrane force balance T={temp:.3f} p={pressure:.3f}",nf+nc,-pressure*R/2,atol=1e-6)
assert all(c["pass_"] for c in checks),checks
assert all((v["D_pad"] or 0)>=0 for v in pad0rows)
assert all(x["pressure_range_Pa"]>=0 for x in gas["rows"])
assert all(x["total_plate_mass_kg"]>pad0["total_plate_mass_kg"] and x["feasible_in_projection"] for x in pad_restore)
assert all(not x["passes_screen"] for x in static_cases[2:])
assert all(x["scarf_screen_SF"]<1 for x in combined_static if x["point"]=="037b_fix_200F")
write("VALIDATION.json",dict(status="PASS",numerical_checks=checks,
                             checks_passed=len(checks),physical_assertions=5,
                             note="Verifies arithmetic and documented units/sources. Does not validate transferred fatigue laws or installed geometry."))

# Standalone report figure; CSVs contain all numerical inputs.
os.environ["MPLCONFIGDIR"] = "unpublished-local-ref:0f195fac91786b1b"
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig,axs=plt.subplots(1,2,figsize=(12,4.8),layout="constrained")
ns=np.geomspace(1000,1e7,400)
for direction,color in [("W","#16658c"),("L","#b45b26")]:
    f=fits[direction]
    ys=f["a"]-f["b"]*np.log10(ns)
    inside=(ns>=f["shortest_test_N"]) & (ns<=f["longest_test_N"])
    axs[0].semilogx(ns,ys,color=color,linestyle="--",alpha=.55)
    axs[0].semilogx(ns[inside],ys[inside],label=f"5.3 pcf {direction} fit (dashed: extrapolation)",color=color)
    pts=[x for x in digitized if x["direction"]==direction]
    axs[0].scatter([x["N_graphical"] for x in pts],[x["normalized_amplitude"] for x in pts],
                   s=22,color=color)
axs[0].axvline(3650,color="#555",linestyle=":",label="10 years, one cycle/day")
axs[0].set(xlabel="Cycles to ultimate failure",ylabel="Shear amplitude / static strength",
           title="Measured dense-core data; transfer is a projection",ylim=(0,1))
axs[0].legend(fontsize=8);axs[0].grid(alpha=.2)
axs[1].loglog(yahr_n,yahr_sa,color="#16658c",label="6061-T6, maximum mean design curve")
axs[1].axhline(138,color="#b45b26",linestyle="--",label="037 pad, 0–276 MPa cycle")
axs[1].axhline(pad_design["peak_plate_MPa"]/2,color="#3a8050",linestyle="--",label="Resized pad candidate")
axs[1].axvline(7300,color="#555",linestyle=":",label="10 years, two handling cycles/day")
axs[1].set(xlabel="Cycles",ylabel="Alternating stress (MPa)",title="Plate life excludes the core and attachment")
axs[1].legend(fontsize=8);axs[1].grid(alpha=.2)
fig.savefig(ROOT/"fatigue-evidence.png",dpi=170)
fig.savefig(ROOT/"fatigue-evidence.svg")
print(json.dumps({"validation":"PASS","pressure_headroom_Pa":pressure_headroom,
                  "pad_plate_only_life_days":results["pad_plate_only_life_days"],
                  "pad_restore_D10_01":pad_design,
                  "gas_first_Pa":gas["first_day_Pa"],"gas_365_Pa":gas["day_365_Pa"],
                  "scarf_delta_kg":join_delta,"core_fits":fits},indent=2))
