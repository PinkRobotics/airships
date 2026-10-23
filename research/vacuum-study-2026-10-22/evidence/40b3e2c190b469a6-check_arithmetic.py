"""Independent CHECK055 scalar arithmetic. No owner executable is used."""
from pathlib import Path
import csv
import json
import math
import numpy as np
from scipy.stats import norm, nct

ROOT = Path(__file__).resolve().parent
OWNER = json.loads((ROOT / "intake/OWNER-RESULTS.json").read_text())
P = 95.4608379139  # kPa; inherited QUESTIONABLE design environment
E = 290000.0  # MPa; QUESTIONABLE
EC = 15000 * 0.006894757293168361
GW = 6800 * 0.006894757293168361
CELL = 9.525
ROWS = []


def compare(path, owner, independent, basis="independent formula", tolerance=1e-8):
    delta = None if owner is None or independent is None else independent - owner
    ROWS.append(dict(path=path, owner=owner, independent=independent, delta=delta,
                     relative_delta=None if delta is None or owner == 0 else delta / owner,
                     agrees=(owner == independent if delta is None else
                             abs(delta) <= tolerance * max(1.0, abs(owner))),
                     basis=basis))


def groups(R, tf, tc, gamma, nu, Ef=E, sy=345):
    h = tf + tc
    teq = math.sqrt(3) * h
    pcl = 4 * Ef * tf * h / (R * R * math.sqrt(1 - nu * nu)) * 1000
    pcrimp = 2 * h * h * GW / (R * tc) * 1000
    vc = pcl / pcrimp
    kc = 1 - vc / 4 if vc <= 2 else 1 / vc
    ph = pcl * kc
    stress = P / 1000 * R / (4 * tf)
    wr = .82 * math.sqrt(Ef * EC * tf / tc)
    dim = 2 * Ef / (1 - nu * nu) * (tf / CELL) ** 2
    wav = 2 * math.pi * (Ef * tf ** 3 * tc / (24 * EC)) ** .25
    return dict(h_mm=h, t_eq_mm=teq, R_over_h=R/h, R_over_teq=R/teq,
                tf_over_h=tf/h, sqrt_R_teq_mm=math.sqrt(R*teq),
                lambda1_width_mm=math.sqrt(R*teq)/(12*(1-.33**2))**.25,
                p_classical_kPa=pcl, p_crimp_kPa=pcrimp, Vc=vc, Kc=kc,
                p_H_kPa=ph, gamma_needed_at_p=P/ph,
                face_stress_at_p_MPa=stress, face_stress_over_yield=stress/sy,
                classical_face_stress_MPa=pcl/1000*R/(4*tf),
                classical_over_yield=pcl/1000*R/(4*tf*sy), E_over_sy=Ef/sy,
                wrinkle_stress_MPa=wr, wrinkle_margin=wr/stress,
                dimpling_stress_MPa=dim, dimpling_margin=dim/stress,
                cell_over_h=CELL/h, wrinkle_wavelength_mm=wav,
                cells_per_wrinkle_wavelength=wav/CELL,
                panel_short_side_over_sqrt_R_teq=609.6/math.sqrt(R*teq),
                panel_long_side_over_sqrt_R_teq=1828.8/math.sqrt(R*teq),
                gamma_line=gamma,
                face_stress_at_collapse_if_gamma_line_MPa=gamma*ph/1000*R/(4*tf),
                collapse_stress_over_yield=gamma*ph/1000*R/(4*tf*sy))


calculated = {}
for name, row in OWNER["scaling"]["designs"].items():
    d = groups(**row["inputs"])
    calculated[name] = d
    for key, value in d.items():
        compare(f"scaling.designs.{name}.{key}", row["groups"][key], value)
base = OWNER["scaling"]["designs"]["R10 lead (028b)"]["inputs"]
g0 = calculated["R10 lead (028b)"]
densities = [1850, 2680, 2680, 2700, 2780, 2810, 4510, 4430, 1550]
standins = {}
for (name, row), density in zip(OWNER["scaling"]["stand_ins"].items(), densities):
    tf = base["tf"] * E / row["E_MPa"] * math.sqrt((1-row["nu"]**2)/(1-base["nu"]**2))
    tc = g0["h_mm"] - tf
    g = groups(base["R"], tf, tc, base["gamma"], row["nu"], row["E_MPa"], row["yield_MPa"])
    data = dict(face_t_mm=tf, core_t_mm=tc, face_kg_per_m2_two_faces=2*tf*.001*density,
                p_classical_ratio_to_Be=g["p_classical_kPa"]/g0["p_classical_kPa"],
                Vc=g["Vc"], face_stress_over_yield_at_p=g["face_stress_over_yield"],
                yield_ratio_vs_Be=g["face_stress_over_yield"]/g0["face_stress_over_yield"],
                biaxial_membrane_stiffness_ratio_vs_Be=
                (row["E_MPa"]*tf/(1-row["nu"]))/(E*base["tf"]/(1-base["nu"])),
                wrinkle_margin=g["wrinkle_margin"],
                wrinkle_margin_ratio_vs_Be=g["wrinkle_margin"]/g0["wrinkle_margin"],
                dimpling_margin=g["dimpling_margin"], E_over_sy=row["E_MPa"]/row["yield_MPa"])
    for key, value in data.items():
        compare(f"scaling.stand_ins.{name}.{key}", row[key], value)
    standins[name] = {**data, "p_H_kPa":g["p_H_kPa"],"Kc":g["Kc"]}

for index, row in enumerate(OWNER["scaling"]["geometric_scales"]):
    s = row["scale"]
    d = dict(R_m=10*s, diameter_m=20*s, Be_face_mm=base["tf"]*s,
             core_mm=base["tc"]*s, cell_needed_mm=CELL*s,
             Be_gauge_ok_min_0p508mm=base["tf"]*s >= .508,
             dimpling_margin_with_stock_3_8_cell=g0["dimpling_margin"]*s*s,
             cells_per_wrinkle_wavelength_stock_cell=g0["cells_per_wrinkle_wavelength"]*s,
             cells_through_core_stock_cell=base["tc"]*s/CELL,
             design_pressure_kPa=P, dimple_amp_mm_at_16p057=16.057295*s)
    for key, value in d.items():
        compare(f"scaling.geometric_scales.{index}.{key}", row[key], value)

caps = []
for index, row in enumerate(OWNER["scaling"]["caps_R10"]):
    a = row["base_radius_m"]
    rise = 10-math.sqrt(100-a*a)
    theta = math.asin(a/10)
    area = 2*math.pi*10*rise
    d = dict(diameter_m=2*a, rise_mm=1000*rise,
             cap_lambda=(12*(1-.33**2))**.25*math.sqrt(2*1000*rise/g0["t_eq_mm"]),
             edge_distance_over_sqrt_R_teq=theta*10000/g0["sqrt_R_teq_mm"],
             edge_distance_over_dimple_width=theta*10000/g0["lambda1_width_mm"],
             shell_area_m2=area, panels_0p61x1p83_per_face=area/(.6096*1.8288))
    for key, value in d.items():
        compare(f"scaling.caps_R10.{index}.{key}",row[key],value)
    caps.append({"base_radius_m":a,**d})
compare("scaling.reis2017_plateau_at_lambda1",OWNER["scaling"]["reis2017_plateau_at_lambda1"],
        (1-.036)*2**(-1.23)+.036)

rig = []
for row, head in zip(OWNER["scaling"]["rig_reach"],[None,0,2,5,10]):
    dp = P if head is None else 101.325-1+9.80665*head
    # Retain the rounded inherited gamma used in the owner's rig arithmetic.
    quoted_basis = dp/P*base["gamma"]
    compare("rig."+row["rig"]+".pressure",row["max_dp_kPa"],dp)
    compare("rig."+row["rig"]+".quoted_Be_gamma",row["max_gamma_R10_section"],quoted_basis)
    rig.append(dict(rig=row["rig"],pressure_kPa=dp,
                    gamma_Be_exact=dp/g0["p_H_kPa"],
                    gamma_5052_article=dp/standins["5052-O"]["p_H_kPa"],
                    card_gamma=row["max_gamma_R10_section"]))

counts = []
for row in OWNER["scaling"]["article_counts"]:
    n=row["n"]
    k=float(nct.ppf(.95,n-1,norm.ppf(.9)*math.sqrt(n))/math.sqrt(n))
    compare(f"article_counts.n{n}.k",row["k_90_95"],k)
    d={"n":n,"k":k}
    for cov in (.05,.1,.15):
        for name,target in (("R10",.564164),("R30",.3865)):
            key=f"mean_needed_{name}_cov{int(100*cov)}"
            value=target/(1-k*cov) if k*cov<1 else None
            compare(f"article_counts.n{n}.{key}",row[key],value)
            d[key]=value
    counts.append(d)

fe_data={}
for p in sorted((ROOT/"intake/owner-runs").glob("*.json")):
    r=json.loads(p.read_text())
    args={k:float(v) for k,v in r["args"].items() if k != "label"}
    g=groups(args["R"],args["tf"],args["tc"],1,args["nuf"],args["Ef"],args["sy"])
    for key in ("p_classical_kPa","p_crimp_kPa","Vc","Kc","p_H_kPa"):
        compare(f"run.{p.stem}.{key}",r[key],g[key])
    path=r["path"]
    peak=max(path,key=lambda row:row["p_kPa"])
    compare(f"run.{p.stem}.limit_kPa",r["limit_kPa"],peak["p_kPa"],"independent reduction of owner path; not independent FE")
    compare(f"run.{p.stem}.gamma",r["gamma_H_elastic_limit"],peak["p_kPa"]/g["p_H_kPa"])
    thresholds={"face yield (outer)":("outer_vm",args["sy"],1),
                "face yield (inner)":("inner_vm",args["sy"],1),
                "W shear typ":("core_tau",35*.006894757293168361,1),
                "W shear min":("core_tau",25*.006894757293168361,1),
                "L shear typ":("core_tau",55*.006894757293168361,1),
                "L shear min":("core_tau",45*.006894757293168361,1),
                "crush typ":("core_min_snn",35*.006894757293168361,-1)}
    cross={}
    for key,(field,threshold,sign) in thresholds.items():
        before={"p_kPa":0,field:0}; crossing=None
        for after in path:
            if sign*after[field]>=threshold:
                crossing=before["p_kPa"]+(after["p_kPa"]-before["p_kPa"])*(threshold-sign*before[field])/(sign*(after[field]-before[field]))
                break
            before=after
        cross[key]=crossing
        compare(f"run.{p.stem}.crossings.{key}",r["crossings_kPa"][key],crossing,
                "independent interpolation of owner stress path; not independent FE",tolerance=2e-3)
    fe_data[p.stem]={"reference":g,"crossings":cross,"path_peak_kPa":peak["p_kPa"]}

for key,row in OWNER["stand_in_check"].items():
    b=row["Be"];al=row["5052-O"]
    for name,field in (("gamma_ratio","gamma_H_elastic"),("limit_ratio","limit_kPa"),
                       ("core_shear_onset_ratio","core_W_shear_typ_kPa"),("face_yield_onset_ratio","face_yield_outer_kPa")):
        compare("stand_in_check."+key+"."+name,row[name],al[field]/b[field],"independent ratio of owner FE outputs")
for row in OWNER["cap_check"]:
    r=OWNER["fe_runs"][row["label"]]
    ref=OWNER["fe_runs"]["S4-al-sphere-d16" if "-al-" in row["label"] else
                        ("R30a-be-sphere" if row["label"].startswith("R30") else "S1-be-sphere-d16")]
    for key,field in (("limit_vs_sphere","limit_kPa"),("core_shear_onset_vs_sphere","core_W_shear_typ_kPa"),
                      ("outer_face_yield_vs_sphere","face_yield_outer_kPa")):
        compare("cap_check."+row["label"]+"."+key,row[key],r[field]/ref[field],"independent ratio of owner FE outputs")

series=OWNER["dimple_series_R10_Be"]
tol={}
for label,field,target in (
    ("elastic gamma_H 0.564164 (R10 need)","gamma_H_elastic",.564164),
    ("outer face below 345 MPa at operating","outer_face_345MPa_at_kPa",P),
    ("core below CR III W typical shear (35 psi) at operating","core_W_typ_shear_at_kPa",P),
    ("core below CR III W minimum shear (25 psi) at operating","core_W_min_shear_at_kPa",P)):
    value=float(np.interp(target,[r[field] for r in series][::-1],[r["dimple_mm"] for r in series][::-1]))
    tol[label]=value
    compare("dimple_tolerance."+label,OWNER["dimple_tolerance_from_fe_mm"][label],value,
            "linear interpolation between owner FE samples; not direct amplitude solve")

b=OWNER["costs"]["B: three full-section stand-in caps, 5 m diameter on R 10 m"]
once=[0,0];each=[0,0]
for key,values in b["items"].items():
    acc=each if key.startswith("per article:") else once
    for j in (0,1): acc[j]+=values[j]
total=[once[j]+3*each[j] for j in (0,1)]
for key,calc in (("once_USD",once),("per_article_USD",each),("USD",total)):
    for j in (0,1):compare(f"costs.B.{key}.{j}",b[key][j],calc[j])
area5=caps[3]["shell_area_m2"]
be_mass=area5*standins["SR-200 Be (design)"]["face_kg_per_m2_two_faces"]
al_mass=area5*standins["5052-O"]["face_kg_per_m2_two_faces"]
costs=dict(B_once_USD=once,B_each_USD=each,B_total_USD=total,
           C_Be_mass_kg=be_mass,C_direct_build_USD=[be_mass*10000+300000+50000,be_mass*50000+1500000+150000],
           D_twice_B_each_USD=[2*x for x in each],D_card_USD=[150000,610000],
           D_allowance_unexplained_USD=[150000-2*each[0],610000-2*each[1]],
           B_aluminium_mass_kg=al_mass,retail_core_GBP_per_m2=158.36/(1.25*.625),
           minimum_Be_scale=.508/base["tf"],pressure_gradient_5mcap_kPa=9.80665*caps[3]["rise_mm"]/1000)
out=dict(designs=calculated,standins=standins,caps=caps,rig=rig,article_counts=counts,
         owner_path_reduction=fe_data,interpolated_tolerances=tol,costs=costs,
         comparisons=len(ROWS),mismatches=[r for r in ROWS if not r["agrees"]])
(ROOT/"ARITHMETIC.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
with (ROOT/"ARITHMETIC-COMPARISONS.csv").open("w") as f:
    writer=csv.DictWriter(f,fieldnames=list(ROWS[0]));writer.writeheader();writer.writerows(ROWS)
print(json.dumps({"comparisons":len(ROWS),"mismatches":out["mismatches"],"rig":rig,"costs":costs},indent=2))
