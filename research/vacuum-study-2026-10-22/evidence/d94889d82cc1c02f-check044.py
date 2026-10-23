#!/usr/bin/env python3
"""Independent scalar reconstruction of the filed 044 method; no owner imports."""
import csv
import json
import math
from pathlib import Path
from datetime import datetime, timezone

B = Path(__file__).resolve().parent
I = B / "inputs/inputs"
def load(p): return json.loads(p.read_text())
def save(name, value):
    (B / name).write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
def rows(name): return list(csv.DictReader((B / "owner" / name).open()))
O = load(B / "owner/RESULTS.json")
D = load(B / "owner/SOURCE-DATA.json")
SP = load(B / "owner/SPECTRUM.json")
R37 = load(I / "037/RESULTS.json")
P37 = load(I / "037/INPUTS.json")["properties_QUESTIONABLE"]
R37B = load(I / "037b/COMPUTE.json")
P28 = next(x["point"] for x in load(I / "028b/PROPERTY-CHECKS.json")["full_named_maxima"]
           if x["route"] == "af015_scarf" and x["material"] == "SR200")
G34 = load(I / "034-check/inputs/034/INPUTS.json")

AUDIT = []
def compare(row, field, actual, expected, atol=1e-9, rtol=2e-9):
    if isinstance(expected, str):
        try: expected = float(expected) if expected else None
        except ValueError: pass
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        ok = math.isclose(actual, expected, rel_tol=rtol, abs_tol=atol)
        delta = actual - expected
    else:
        ok = actual == expected
        delta = None
    AUDIT.append({"row": row, "field": field, "card_value": expected,
                  "check_value": actual, "delta": delta,
                  "status": "MATCH" if ok else "MISMATCH", "atol": atol, "rtol": rtol})
def compare_fields(row, actual, expected, keys=None):
    for k in (keys if keys is not None else actual):
        if k not in expected: continue
        if isinstance(actual[k], dict) and isinstance(expected[k], dict):
            compare_fields(row + "/" + k, actual[k], expected[k])
        else:
            compare(row, k, actual[k], expected[k])

# Original inputs, exact unit conversions and catalogue table entries.
R = 10.0
A = 4 * math.pi * R**2
p0 = G34["environment"]["p_external_Pa"]
lift = G34["environment"]["lift_reference_kg"]
E = P37["Be_E_Pa"]
nu = P37["Be_nu"]
alpha_f = P37["Be_alpha_1_per_K"]
alpha_c = P37["Al_5056_alpha"]
da = alpha_c-alpha_f
psi = 6894.757293168361
rho_core = 0.45359237 / 0.3048**3
rho_face = 1850.0
rho_foil = R37B["sources_used"]["foil_5056_rho"]["value"]
Efoil = R37B["sources_used"]["foil_5056_E_GPa"]["value"] * 1e9
Kb = Efoil * rho_core / rho_foil / 2
G = {"W": 6.8e3 * psi, "L": 15e3 * psi}
S = {"typical_W": 35*psi, "minimum_average_W":25*psi,
     "typical_L":55*psi, "minimum_average_L":45*psi}
Th = R37["p2_thermal"]["coated_outer"]["T_outer_subsolar_K"]
swing = R37["p2_thermal"]["coated_outer"]["day_night_outer_swing_K"]
Tl = Th - swing
Tm = (Th + Tl)/2
Tamb = G34["environment"]["T_K"]
T200 = (200-32)*5/9 + 273.15
T250 = (250-32)*5/9 + 273.15
local_thermal = (R37["p2_thermal"]["coated_outer"]["gradient_stress_Pa"] +
                 R37["p2_thermal"]["coated_outer"]["pattern"]["bending_stress_Pa"])
pressure_flight = p0 + R37["wind"]["q_VB_only_Pa"]
tf0, tc0 = P28["tf_m"], P28["tc_m"]
fix = R37B["fixes"][6]
tff, tcf = fix["tf_mm"]/1000, fix["tc_mm"]/1000
rf = R37B["scarf_fix"][1]["r_need"]
geometries = {"base": (tf0,tc0,30), "fix": (tff,tcf,rf)}

def geometry(tf,tc,ratio):
    lap = ratio*tf
    seam = A*(1/(.6096-lap) + 1/(1.8288-lap))
    nodes = A/((.6096-lap)*(1.8288-lap))
    m = {"faces":2*A*tf*rho_face, "core":A*tc*rho_core,
         "bond":2*A*.015*.45359237/.3048**2,
         "scarf":2*seam*math.hypot(lap,tf)*.070,
         "splice":seam*tc*.0005*500, "seal":seam*.002}
    return {"tf_m":tf,"tc_m":tc,"scarf_ratio":ratio,"lap_m":lap,"seam_m":seam,
            "nodes":nodes,"masses_kg":m,"physical_structural_joining_kg":sum(m.values())}
geo = {name:geometry(*value) for name,value in geometries.items()}
compare_fields("/geometry_028b_full_named",geo["base"],O["geometry_028b_full_named"])
compare_fields("/geometry_037b_fix",geo["fix"],O["geometry_037b_fix"])

# Refit the reported measured ordinates, using an independent normal-equation fit.
def regression(points):
    x=[math.log10(a) for a,b in points]; y=[b for a,b in points]
    mx=sum(x)/len(x); my=sum(y)/len(y)
    slope=sum((a-mx)*(b-my) for a,b in zip(x,y))/sum((a-mx)**2 for a in x)
    return {"a":my-slope*mx,"b":-slope}
fits={}
for direction in ("W","L"):
    points=[(r["N_graphical"],r["normalized_amplitude"]) for r in D["core"]["digitized"]
            if r["direction"]==direction]
    f=regression(points)
    f.update({"minimum_test_level":min(y for x,y in points),
              "maximum_test_level":max(y for x,y in points),
              "cap_N":718394.0 if direction=="W" else max(x for x,y in points)})
    fits[direction]=f
    compare_fields("/core_fits/"+direction,f,O["core_fits"][direction])

def fatigue(t1,t2,strength,direction="W",shift=0):
    amp=abs(t2-t1)/2; mean=(t1+t2)/2; peak=max(abs(t1),abs(t2))
    sf=strength/peak if peak else None
    if abs(mean)>=strength:
        return {"N":None,"equivalent_fraction":None,"static_SF":sf,
                "classification":"mean_over_static_strength"}
    q=amp/(strength-abs(mean))
    f=fits[direction]
    n=max(1.0,10**((f["a"]+shift-q)/f["b"]))
    classification=("low_stress_extrapolation" if q<f["minimum_test_level"] else
                    "high_stress_extrapolation" if q>f["maximum_test_level"] else "interpolation")
    if sf is not None and sf < 1:
        classification += ";static_overload"
    return {"N":n,"test_horizon_capped_N":min(n,f["cap_N"]),
            "equivalent_fraction":q,"static_SF":sf,"classification":classification}

def coupled(T,tsf,pressure,tf,tc,direction="W",kb=Kb):
    kf=E/(1-nu)
    resultant=-pressure*R/2
    eps=((2*kf*tf*alpha_f+kb*tc*alpha_c)*(T-tsf)+resultant)/(2*kf*tf+kb*tc)
    sf=kf*(eps-alpha_f*(T-tsf))
    sc=kb*(eps-alpha_c*(T-tsf))
    edge=math.sqrt(2*kb*G[direction])*(eps-alpha_c*(T-tsf))
    return {"epsilon":eps,"face":sf,"core":sc,"edge":edge,
            "balance_error_N_per_m":2*tf*sf+tc*sc-resultant}

def thermal_ends(model,tsf,tf,tc,direction):
    if model=="037_rigid_thermal":
        c=da*math.sqrt(E*tf*G[direction]/tc)
        return c*(Tl-tsf),c*(Th-tsf)
    if model=="037b_free_edge_thermal":
        c=da*math.sqrt(2*Kb*G[direction])
        return c*(tsf-Tl),c*(tsf-Th)
    return (coupled(Tl,tsf,pressure_flight,tf,tc,direction)["edge"],
            coupled(Th,tsf,pressure_flight,tf,tc,direction)["edge"])

thermal=[]
for idx,row in enumerate(O["thermal_cases"]):
    tf,tc,_=geometries["fix" if row["point"].startswith("037b") else "base"]
    t1,t2=thermal_ends(row["model"],row["T_stressfree_K"],tf,tc,row["basis"][-1])
    f=fatigue(t1,t2,S[row["basis"]],row["basis"][-1])
    out={k:row[k] for k in ("point","model","T_stressfree_K","basis")}
    out.update({"tau_cold_Pa":t1,"tau_hot_Pa":t2,"amplitude_Pa":abs(t2-t1)/2,
                "mean_Pa":(t1+t2)/2,**f,
                "thermal_only_damage_year":365/f["N"] if f["N"] else None,
                "thermal_only_life_days":f["N"]})
    compare_fields("/thermal_cases/"+str(idx),out,row)
    thermal.append(out)
save("THERMAL-INDEPENDENT.json",thermal)

# Interpolate the maximum-mean column observed in the original Yahr Table 1.
yahrN=[100,200,500,1000,2000,5000,7000,10000,20000,50000,100000,200000,
       500000,1e6,2e6,5e6,1e7,2e7,5e7,1e8,2e8,5e8,1e9]
yahrS=[420.28,325.43,239.94,184.71,137.89,95.01,75.36,63.02,53.37,49.5,
       47.5,37.68,30.06,26.68,24.48,22.68,21.79,21.18,20.66,20.39,20.21,20.06,19.97]
for i,(n,s) in enumerate(zip(yahrN,yahrS)):
    compare("/source/Yahr/"+str(i),"N",n,D["pad"]["N"][i])
    compare("/source/Yahr/"+str(i),"Sa_maximum_mean_MPa",s,D["pad"]["Sa_maximum_mean_MPa"][i])
def plateN(sa):
    if sa <= yahrS[-1]:return yahrN[-1]
    for i in range(len(yahrS)-1):
        if yahrS[i]>=sa>=yahrS[i+1]:
            u=(sa-yahrS[i])/(yahrS[i+1]-yahrS[i])
            return 10**(math.log10(yahrN[i])+u*math.log10(yahrN[i+1]/yahrN[i]))
    return None
def pad_shape(force,n,area_each,peak_MPa):
    radius=math.sqrt(area_each/math.pi)
    t=math.sqrt(3*(force/n)*((1+.33)*math.log(radius/.025)+1-(1-.33)*.025**2/(4*radius**2))
                /(2*math.pi*peak_MPa*1e6))
    return {"n_pads":n,"area_each_m2":area_each,"radius_m":radius,"t_m":t,
            "total_plate_mass_kg":n*area_each*t*2700}
def pad_damage(plate_peak,core_peak):
    result=[]
    for row in SP["pad_rows"]:
        lo,hi=row["f_low"],row["f_high"]
        sa=plate_peak*(hi-lo)/2
        pn=plateN(sa)
        f=fatigue(core_peak*lo,core_peak*hi,S["minimum_average_W"]-p0/2)
        result.append({"case":row["id"],"count":row["count"],"Sa_MPa":sa,"N_pad":pn,
            "D_pad":row["count"]/pn,"core_tau_peak_Pa":core_peak*hi,"core_N":f["N"],
            "core_SF_shear_alone":S["minimum_average_W"]/(core_peak*hi),
            "core_SF_with_scalar_pressure_reserve":(S["minimum_average_W"]-p0/2)/(core_peak*hi),
            "D_core":row["count"]/f["N"] if f["N"] else None})
    return result
force20=R37["wind"]["mooring_016_N"]
force70=R37["wind"]["drag_70_N"]
basepad=pad_shape(force20,6,force20/6/S["typical_W"],276)
padcycles=pad_damage(276,S["typical_W"])
compare_fields("/pad_base_geometry",basepad,O["pad_base_geometry"])
for i,(mine,owner) in enumerate(zip(padcycles,rows("PAD-BASE-CYCLES.csv"))):
    compare_fields("/PAD-BASE-CYCLES/"+str(i),mine,owner)
Dp=sum(x["D_pad"] for x in padcycles)
Dc=sum(x["D_core"] for x in padcycles)
compare_fields("/pad_base_damage",{"plate_D_year":Dp,"core_D_year":Dc,
               "core_peak_Pa":S["typical_W"],"peak_plate_MPa":276},O["pad_base_damage"])
compare("/","pad_plate_only_life_days",365/Dp,O["pad_plate_only_life_days"])
save("PAD-BASE-INDEPENDENT.json",{"geometry":basepad,"cycles":padcycles,"D_year":Dp,
     "life_index_days":365/Dp,"static_core_SF":S["minimum_average_W"]/S["typical_W"]})
restored=[]
for idx,row in enumerate(load(B/"owner/PAD-RESTORE.json")):
    corepeak=(S["minimum_average_W"]-p0/2)/2
    force=force20 if row["force_case"]=="20m_s" else force70
    low,high=1.0,276.0
    target=row["target_combined_D10"]
    for _ in range(100):
        mid=(low+high)/2
        damages=pad_damage(mid,corepeak)
        if 10*sum(x["D_pad"]+x["D_core"] for x in damages)>target:high=mid
        else:low=mid
    peak=(low+high)/2
    damages=pad_damage(peak,corepeak)
    out={"force_case":row["force_case"],"target_combined_D10":target,
         **pad_shape(force,row["n_pads"],force/row["n_pads"]/corepeak,peak),
         "plate_D_year":sum(x["D_pad"] for x in damages),
         "core_D_year":sum(x["D_core"] for x in damages),
         "core_peak_Pa":corepeak,"peak_plate_MPa":peak}
    out["addition_vs_corrected_six_pad20_kg"]=out["total_plate_mass_kg"]-basepad["total_plate_mass_kg"]
    compare_fields("/PAD-RESTORE/"+str(idx),out,row)
    restored.append(out)
save("PAD-RESTORE-INDEPENDENT.json",restored)

def gas(geom):
    m=geom["masses_kg"]
    volume=4*math.pi*R**3/3-m["faces"]/rho_face-m["core"]/rho_foil-(
        m["bond"]+m["scarf"])/1250-m["splice"]/500
    inventory=.1*(m["bond"]*.0485+m["core"]*.001+
                   (m["scarf"]+m["splice"]+m["seal"])*.01)
    leak=.001*(geom["seam_m"]+geom["nodes"])+.01
    dpleak=.1*leak*86400/volume
    # Outer scarf: diffusion path is lap; area normal to path is length*film thickness.
    molflow=10*G34["constants"]["Barrer_mol_m_m2_s_Pa"]*geom["seam_m"]*(.070/1250)/geom["lap_m"]*p0
    dpperm=molflow*G34["constants"]["R_universal_J_mol_K"]*Tamb*86400/volume
    total_inventory_dp=inventory/.01801528*G34["constants"]["R_universal_J_mol_K"]*Tamb/volume
    daily=[dpleak+dpperm+total_inventory_dp*(math.exp(-(d-1))-math.exp(-d)) for d in range(1,366)]
    return {"volume_m3":volume,"conditioned_B_kg":inventory,"leak_mbar_l_s":leak,
            "leak_dp_Pa_day":dpleak,"permeation_dp_Pa_day":dpperm,
            "first_day_Pa":daily[0],"day_365_Pa":daily[-1]},daily
gasout={};daily={}
for label in geo:
    gasout[label],daily[label]=gas(geo[label])
    compare_fields("/gas_topup"+("_fix" if label=="fix" else ""),gasout[label],
                   O["gas_topup_fix" if label=="fix" else "gas_topup"])
for i,row in enumerate(rows("DAILY-TOPUP.csv")):
    compare_fields("/DAILY-TOPUP/"+str(i),{"day":i+1,"pressure_range_Pa":daily["base"][i],
        "pressure_low_Pa":10,"pressure_high_Pa":10+daily["base"][i]},row)
save("GAS-INDEPENDENT.json",{"summaries":gasout,"daily_ranges_Pa":daily})

# Reconstruct every component-cycle record from occurrence inputs and mechanics.
pointsettings={"028b_250F":(tf0,tc0,30,T250,"base"),
               "028b_200F":(tf0,tc0,30,T200,"base"),
               "037b_fix":(tff,tcf,rf,T200,"fix")}
cycles=[]
def cycle(point,case,kind,count,tf,tc,ratio,tsf,plo=None,phi=None,base_pressure=pressure_flight):
    # The filed records use the steady flight pressure in every coupled cycle.
    # Face stress separately uses the 037b thin-face residual envelope at the
    # cold endpoint, rather than the coupled model's pressure-carrying face.
    face_residual_cold=Kb*tc/(2*tf)*da*(tsf-Tl)
    face_nominal=base_pressure*R/(4*tf)+face_residual_cold
    if kind=="thermal":
        c=coupled(Tl,tsf,base_pressure,tf,tc); h=coupled(Th,tsf,base_pressure,tf,tc)
        ba=Kb*tc/(2*tf)*da*swing/2+local_thermal
        bp=face_nominal+ba
    else:
        c=coupled(Tm,tsf,base_pressure+plo,tf,tc); h=coupled(Tm,tsf,base_pressure+phi,tf,tc)
        ba=abs(phi-plo)*R/(8*tf)
        bp=face_nominal+max(plo,phi)*R/(4*tf)
    low,high=c["edge"],h["edge"]
    f=fatigue(low,high,S["minimum_average_W"])
    afpeak=max(abs(low),abs(high))
    bn=1e7 if ba<=262e6 else None
    an=1e7 if afpeak<=1500*psi else None
    return {"point":point,"case":case,"kind":kind,"count":count,
            "Be_amplitude_MPa":ba/1e6,"Be_peak_compression_MPa":bp/1e6,
            "Be_proxy_N":bn,"Be_proxy_damage":count/bn if bn else None,
            "core_amplitude_kPa":abs(high-low)/2000,"core_mean_kPa":(low+high)/2000,
            "core_N":f["N"],"core_static_SF":f["static_SF"],
            "core_damage":count/f["N"] if f["N"] else None,
            "AF163_peak_shear_kPa":afpeak/1000,"AF163_proxy_N":an,
            "AF163_proxy_damage":count/an if an else None,
            "scarf_amplitude_MPa":ba/(ratio+1/ratio)/1e6,
            "scarf_peak_shear_MPa":bp/(ratio+1/ratio)/1e6,
            "scarf_N":None,"scarf_damage":None}
for point,(tf,tc,ratio,tsf,geom) in pointsettings.items():
    cycles.append(cycle(point,"thermal_daily","thermal",365,tf,tc,ratio,tsf))
    for x in SP["pressure_rows"]:
        cycles.append(cycle(point,x["id"],"pressure",x["count"],tf,tc,ratio,tsf,x["dp_low"],x["dp_high"]))
    for day,dp in enumerate(daily[geom],1):
        cycles.append(cycle(point,f"topup_day_{day}","topup",1,tf,tc,ratio,tsf,-dp,0))
owner_cycles=rows("COMPONENT-CYCLES.csv")
compare("/COMPONENT-CYCLES","row_count",len(cycles),len(owner_cycles))
for i,(mine,owner) in enumerate(zip(cycles,owner_cycles)):
    compare_fields("/COMPONENT-CYCLES/"+str(i),mine,owner)
save("CYCLES-INDEPENDENT.json",cycles)

summaries={}
vent_records=[]
for point,(tf,tc,ratio,tsf,geom) in pointsettings.items():
    annual=[x for x in cycles if x["point"]==point]
    vent=cycle(point,"full_vent","pressure",1,tf,tc,ratio,tsf,-(p0-10),0,base_pressure=p0-10)
    endpoints=[coupled(Tm,tsf,p,tf,tc)["edge"] for p in (0,p0-10)]
    vent_records.append({"point":point,"tag":"PROJECTION",
        "temperature_K":Tm,"pressure_endpoints_Pa":[0,p0-10],
        "core_edge_endpoints_Pa":endpoints,
        "core_response":fatigue(*endpoints,S["minimum_average_W"]),
        "one_full_cycle":vent,
        "commissioning_half_cycle":{k:v/2 if v is not None else None
            for k,v in vent.items() if k.endswith("_damage")},
        "annual_count_alternatives":[0,12,365],
        "qualified_hull_life_days":None})
    for nv in [0,12,365]:
        summary={}
        for c,n in [("Be_proxy","Be_proxy_damage"),("core","core_damage"),("AF163_proxy","AF163_proxy_damage")]:
            damage=sum(x[n] for x in annual)+nv*vent[n]
            summary[c]={"D_year":damage,"life_days":365/damage}
        summary["commissioning_core_damage"]=vent["core_damage"]/2
        summary["scarf"]={"D_year":None,"life_days":None}
        key=point+"_vents_"+str(nv)
        summaries[key]=summary
        compare_fields("/component_summaries/"+key,summary,O["component_summaries"][key])
save("COMPONENT-SUMMARIES-INDEPENDENT.json",summaries)
save("VENT-CYCLES-INDEPENDENT.json",vent_records)

# Static load screens and mass-only alternatives.
static=[]
scarf_capacity=10e6*(30+1/30)*4*tf0/R
static_pressures=[p0,p0+100+R37["wind"]["q_VB_only_Pa"]+
                 R37["wind"]["q_flight_stagnation_Pa"],p0+2000,101325,
                 p0+R37["wind"]["q_moor_70kn_Pa"]]
for i,row in enumerate(O["static_cases"]):
    pressure=static_pressures[i]
    sf=scarf_capacity/pressure
    compare("/static_cases/"+str(i),"pressure_Pa",pressure,row["pressure_Pa"])
    compare("/static_cases/"+str(i),"least_028b_projected_SF",sf,row["least_028b_projected_SF"])
    compare("/static_cases/"+str(i),"passes_screen",sf>=1,row["passes_screen"])
    static.append({"case":row["case"],"pressure_Pa":row["pressure_Pa"],"least_SF":sf})
compare("/","pressure_headroom_Pa",scarf_capacity-p0,O["pressure_headroom_Pa"])
combined=[]
for i,row in enumerate(load(B/"owner/COMBINED-STATIC.json")):
    if row["point"]=="037b_fix_200F":tf,tc,ratio,tsf=tff,tcf,rf,T200
    elif row["point"]=="028b_200F_scarf60":tf,tc,ratio,tsf=tf0,tc0,60,T200
    else:tf,tc,ratio,tsf=tf0,tc0,30,T250
    pressure={"vacuum_only":p0,"weather_flight_limit":p0+100+R37["wind"]["q_VB_only_Pa"]+
              R37["wind"]["q_flight_stagnation_Pa"],"sea_level":101325.0}[row["loading"]]
    # Filed residual-only envelope ignores beneficial pressure contraction of the core.
    residual=Kb*tc/(2*tf)*da*(tsf-Tl)
    demand=pressure*R/(4*tf)+residual+local_thermal
    tau=demand/(ratio+1/ratio)
    out={"point":row["point"],"loading":row["loading"],"face_compression_MPa":demand/1e6,
         "scarf_shear_MPa":tau/1e6,"scarf_screen_SF":10e6/tau}
    compare_fields("/COMBINED-STATIC/"+str(i),out,row);combined.append(out)
save("COMBINED-STATIC-INDEPENDENT.json",combined)
g60=geometry(tf0,tc0,60)
joinadd=g60["physical_structural_joining_kg"]-geo["base"]["physical_structural_joining_kg"]
strict=next(x for x in restored if x["n_pads"]==6 and x["force_case"]=="20m_s" and x["target_combined_D10"]==.1)
addition=joinadd+strict["addition_vs_corrected_six_pad20_kg"]
comparison037b=R37B["baseline_usage"]
mass={"scarf_60_to_1":{"added_joining_kg":joinadd,"new_overlap_m":60*tf0,
                     "pressure_mean_shear_MPa":p0*R/(4*tf0)/(60+1/60)/1e6},
      "037b_filed_fix":{
          "filed_added_join_kg":geometry(comparison037b["tf"],comparison037b["tc"],rf)["physical_structural_joining_kg"]-
              geometry(comparison037b["tf"],comparison037b["tc"],30)["physical_structural_joining_kg"],
          "independently_recomputed_physical_total_delta_kg":
              geo["fix"]["physical_structural_joining_kg"]-geo["base"]["physical_structural_joining_kg"]},
      "AF015_to_AF030":{"added_kg":geo["base"]["masses_kg"]["bond"]},
      "AF015_to_AF060":{"added_kg":3*geo["base"]["masses_kg"]["bond"]},
      "scarf60_plus_six_pad_D10_01":{"added_kg":addition,"gross_with_unchanged_budget_kg":lift+addition},
      "inspection_repair":{"replacement_patch_kg_m2":2*tf0*rho_face+tc0*rho_core+2*.015*.45359237/.3048**2}}
compare_fields("/mass_options",mass,O["mass_options"])
save("MASS-INDEPENDENT.json",mass)

# Thermal targets, shifted curves, directional sensitivity and catalogue alternatives.
for i,row in enumerate(load(B/"owner/THERMAL-RESTORE.json")):
    model=row["model"]
    tsf=Tamb if model=="037_rigid_thermal" else T200
    tf,tc=(tf0,tc0) if model=="037_rigid_thermal" else (tff,tcf)
    ends=thermal_ends(model,tsf,tf,tc,"W")
    mean=sum(ends)/2
    n=3650/row["target_thermal_D10"]
    amp=(fits["W"]["a"]-fits["W"]["b"]*math.log10(n))*(S["minimum_average_W"]-abs(mean))
    target=2*amp/(abs(ends[1]-ends[0])/swing)
    compare_fields("/THERMAL-RESTORE/"+str(i),{"allowable_daily_amplitude_kPa":amp/1000,
        "fixed_mean_allowable_swing_K":target,"mean_held_kPa":mean/1000},row)
for i,row in enumerate(load(B/"owner/LIFE-SENSITIVITY.json")):
    tsf=Tamb if row["model"]=="037_rigid_thermal" else T200
    tf,tc=(tf0,tc0) if row["model"]=="037_rigid_thermal" else (tff,tcf)
    ends=thermal_ends(row["model"],tsf,tf,tc,row["direction"])
    f=fatigue(*ends,S["minimum_average_"+row["direction"]],row["direction"],row["curve_shift"])
    compare_fields("/LIFE-SENSITIVITY/"+str(i),{"life_days":f["N"]/row["cycles_per_day"],
        "static_SF":f["static_SF"],"classification":f["classification"]},row)
for i,row in enumerate(rows("CORE-SENSITIVITY.csv")):
    amp=math.sqrt(2*Kb*G["W"])*da*float(row["swing_K"])/2
    mean=math.sqrt(2*Kb*G["W"])*da*(T200-Tm)
    f=fatigue(mean-amp,mean+amp,S["typical_W" if row["basis"]=="typ_W" else "minimum_average_W"],
              "W",float(row["curve_vertical_shift"]))
    compare_fields("/CORE-SENSITIVITY/"+str(i),{**f,"thermal_only_life_days":f["N"]},row)
densers=[]
for i,(pcf,gw,styp,smin) in enumerate([(1,6.8,35,25),(1.6,10.5,60,38),(2.3,15,95,62),(3,19,145,100)]):
    kb=Kb*pcf; gw=gw*1000*psi
    amp=math.sqrt(2*kb*gw)*da*swing/2
    mean=math.sqrt(2*kb*gw)*da*(T200-Tm)
    out={"additional_core_kg":A*tc0*rho_core*(pcf-1),
         "rigid_thermal_amplitude_kPa":da*math.sqrt(E*tf0*gw/tc0)*swing/2000,
         "free_edge_thermal_amplitude_kPa":amp/1000,"free_edge_thermal_mean_kPa":mean/1000,
         "typical_W_Pa":styp*psi,"minimum_average_W_Pa":smin*psi,
         "minimum_basis":fatigue(mean-amp,mean+amp,smin*psi),
         **fatigue(mean-amp,mean+amp,styp*psi)}
    compare_fields("/DENSER-CORE/"+str(i),out,load(B/"owner/DENSER-CORE.json")[i])
    densers.append(out)
save("DENSER-CORE-INDEPENDENT.json",densers)
for i,row in enumerate(load(B/"owner/BOND-CONTACT.json")):
    nominal=(math.sqrt(2*Kb*G["W"])*da*(T200-Tl) if i==0 else
             math.sqrt(2*Kb*G["W"])*da*(T250-Tl) if i==1 else
             da*math.sqrt(E*tf0*G["W"]/tc0)*(Th-Tamb))
    fraction=rho_core/rho_foil
    compare_fields("/BOND-CONTACT/"+str(i),{"nominal_gross_shear_kPa":nominal/1000,
        "ideal_bare_wall_contact_fraction":fraction,
        "no_fillet_contact_area_average_MPa":nominal/fraction/1e6,
        "minimum_effective_area_fraction_for_1500psi":nominal/(1500*psi)},row)

# Card prose values are compared at their stated display precision.
claims=[]
def claim(row,field,filed,actual,tolerance):
    compare("/CARD/"+row,field,actual,filed,atol=tolerance,rtol=0)
    claims.append(AUDIT[-1])
claim("geometry","baseline_face_mm",.799676,tf0*1000,.0000005)
claim("geometry","baseline_core_mm",22.106790,tc0*1000,.0000005)
claim("geometry","fixed_face_mm",.794622,tff*1000,.0000005)
claim("geometry","fixed_core_mm",23.231909,tcf*1000,.0000005)
claim("geometry","fixed_scarf_ratio",30.341397,rf,.0000005)
gradient=R37["p2_thermal"]["coated_outer"]["dT_through_at_max_K"]
inner_ends=[Tl+gradient,Th-gradient]
for i in range(2):
    compare("/SPECTRUM/inner_T_K",str(i),inner_ends[i],SP["inner_T_K"][i])
    compare("/SPECTRUM/outer_T_K",str(i),(Tl,Th)[i],SP["outer_T_K"][i])
claim("spectrum","inner_range_K",29.695,inner_ends[1]-inner_ends[0],.0005)
claim("spectrum","outer_range_K",30.493,swing,.0005)
claim("spectrum","through_core_K",.3992,gradient,.00005)
claim("spectrum","mooring_kN",48.259,force20/1000,.0005)
claim("vacuum","seam_m",2842.13,geo["base"]["seam_m"],.005)
claim("vacuum","first_day_pressure_high_Pa",37.562,10+daily["base"][0],.0005)
claim("vacuum","late_year_pressure_high_Pa",18.340,10+daily["base"][-1],.0005)
claim("vacuum","topup_Be_range_MPa",.086,daily["base"][0]*R/(4*tf0)/1e6,.0005)
vent_be_amplitude=(p0-10)*R/(8*tf0)
claim("vacuum","full_vent_Be_range_MPa",298.4,vent_be_amplitude*2/1e6,.05)
claim("vacuum","Be_local_factor",1.76,262e6/vent_be_amplitude,.005)
claim("pad","life_days",949.85,365/Dp,.005)
claim("pad","static_core_SF",.7143,S["minimum_average_W"]/S["typical_W"],.00005)
claim("pad","base_mass_kg",3.414,basepad["total_plate_mass_kg"],.0005)
claim("pad","base_thickness_mm",6.323,basepad["t_m"]*1000,.0005)
claim("pad","strict_plate_D10",.03681,10*strict["plate_D_year"],.000005)
claim("pad","strict_core_D10",.06319,10*strict["core_D_year"],.000005)
claim("repair","90_day_plate_damage",.0948,Dp*90/365,.00005)
claim("repair","40_replacement_mass_kg",136.56,40*basepad["total_plate_mass_kg"],.005)
pad_annual=sum(x["count"] for x in SP["pad_rows"])
claim("pad","test_horizon_index_years",6.43,718394/pad_annual,.005)
claim("proxy","Be_AF_annual_damage",.01112,sum(x["count"] for x in cycles if
      x["point"]=="028b_250F")/1e7,.000005)
claim("proxy","Be_AF_index_days",32822,365/summaries["028b_250F_vents_0"]["Be_proxy"]["D_year"],.5)
claim("mass","strict_plus_scarf_added_kg",36.661,addition,.0005)
claim("mass","strict_plus_scarf_gross_kg",4926.103,lift+addition,.0005)
claim("mass","bare_patch_kg_m2",3.459,mass["inspection_repair"]["replacement_patch_kg_m2"],.0005)
save("CARD-CLAIMS.json",claims)
save("SUPPLEMENTAL-RESULTS.json",{
    "tag":"QUESTIONABLE / PROJECTION","inner_T_K":inner_ends,
    "plate_replacement_90_day_damage":Dp*90/365,
    "plate_40_replacements_offboard_kg":40*basepad["total_plate_mass_kg"],
    "Be_full_vent_amplitude_MPa":vent_be_amplitude/1e6,
    "Be_full_vent_threshold_concentration":262e6/vent_be_amplitude,
    "annual_component_cycles_each_point":sum(x["count"] for x in cycles if x["point"]=="028b_250F"),
    "annual_pad_cycles":pad_annual,"decade_pad_cycles":10*pad_annual,
    "core_test_horizon_only_pad_index_years":718394/pad_annual,
    "S200F255_nominal_compression_SF":255e6/(p0*R/(4*tf0)),
    "baseline_bill":P28["masses_kg"],
    "037b_fixed_geometry_join_comparison_tf_m":comparison037b["tf"],
    "037b_fixed_geometry_join_comparison_tc_m":comparison037b["tc"],
    "old_plate_credit_kg":basepad["total_plate_mass_kg"],
    "without_old_plate_credit_added_kg":strict["total_plate_mass_kg"]+joinadd,
    "without_old_plate_credit_gross_kg":lift+strict["total_plate_mass_kg"]+joinadd,
    "mass_accounting_status":"Conditional alternative, not an arithmetic mismatch: establish whether original plates occupy part of the retained 100 kg systems line."})

# Physical identities and separate evidence checks, rather than tests of syntax.
verification=[]
def verify(name,ok,details):
    verification.append({"name":name,"status":"PASS" if ok else "FAIL","details":details})
errors=[abs(coupled(t,tsf,p,tf,tc)["balance_error_N_per_m"])
        for tf,tc,tsf in [(tf0,tc0,T250),(tff,tcf,T200)]
        for t in (Tl,Tm,Th) for p in (0,p0,pressure_flight)]
verify("Membrane force conservation over 18 independent states",
       max(errors)<1e-7,{"maximum_residual_N_per_m":max(errors),"states":len(errors)})
release=sum(dp-gasout["base"]["leak_dp_Pa_day"]-
            gasout["base"]["permeation_dp_Pa_day"] for dp in daily["base"])
expected_release=gasout["base"]["conditioned_B_kg"]/.01801528*G34["constants"]["R_universal_J_mol_K"]*Tamb/gasout["base"]["volume_m3"]*(1-math.exp(-365))
verify("Finite release conservation over 365 topups",abs(release-expected_release)<1e-9,
       {"release_Pa":release,"inventory_Pa":expected_release})
totals={p:sum(x["count"] for x in cycles if x["point"]==p) for p in pointsettings}
verify("Occurrence conservation without duplicating inner/outer thermal cycles",
       len(cycles)==1113 and set(totals.values())=={111207} and pad_annual==111730,
       {"component_rows":len(cycles),"component_cycle_totals":totals,"pad_annual_cycles":pad_annual})
allocations=[10*(x["plate_D_year"]+x["core_D_year"])-x["target_combined_D10"] for x in restored]
verify("All eight independent pad allocations close",max(abs(x) for x in allocations)<1e-10,
       {"maximum_absolute_D10_residual":max(abs(x) for x in allocations)})
verify("Mass bill closes with systems and fixed reserve still charged",
       abs(geo["base"]["physical_structural_joining_kg"]+100+P28["masses_kg"]["fixed_reserve"]-lift)<1e-8,
       {"physical_structural_joining_kg":geo["base"]["physical_structural_joining_kg"],
        "systems_kg":100,"fixed_reserve_kg":P28["masses_kg"]["fixed_reserve"],"lift_kg":lift})
own_digits=load(B/"INDEPENDENT-DIGITIZATION.json")
fit_differences={}
for direction in ("L","W"):
    f=own_digits["directions"][direction]
    fit_differences[direction]=max(abs((f["a"]-f["b"]*x)-
        (fits[direction]["a"]-fits[direction]["b"]*x)) for x in [3+i*.1 for i in range(38)])
verify("Independent Fig10 reading agrees within declared 0.03 reading band",
       max(fit_differences.values())<.03,{"max_normalized_curve_difference":fit_differences,
       "meaning":"Digitization agreement only; not density transfer validation."})
verify("Static-invalid cycle remains marked despite finite extrapolated N",
       "static_overload" in vent_records[0]["core_response"]["classification"],
       {"250F_vent_core_response":vent_records[0]["core_response"]})
save("VERIFICATION.json",verification)
assert all(x["status"]=="PASS" for x in verification),verification

save("AUDIT.json",AUDIT)
mismatches=[x for x in AUDIT if x["status"]=="MISMATCH"]
save("MISMATCHES.json",mismatches)
result={"unit":"vacuum-mainline044-check-1020","tag":"QUESTIONABLE / PROJECTION",
    "started_at":load(B/"START.json")["started_at"],"arithmetic_completed_at":datetime.now(timezone.utc).isoformat(),
    "owner_code_read":False,"owner_code_run":False,"qualified_hull_life_days":None,
    "counts":{"total":len(AUDIT),"matched":len(AUDIT)-len(mismatches),"mismatched":len(mismatches)},
    "core_fits":fits,"pad_plate_life_index_days":365/Dp,"pad_core_static_SF":S["minimum_average_W"]/S["typical_W"],
    "mass_options":mass,"thermal_cases":thermal,"component_summaries":summaries,
    "independent_geometry":geo,"static_cases":static,
    "method":"Own standard-library arithmetic from pinned inputs and stated formulas. No owner calculation code read, imported or executed."}
save("ARITHMETIC-RESULTS.json",result)
print(json.dumps(result["counts"]))
for x in mismatches[:30]:print(json.dumps(x,ensure_ascii=False))
