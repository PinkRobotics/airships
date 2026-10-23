from pathlib import Path
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parent
a=json.loads((ROOT/"ARITHMETIC.json").read_text())
o=json.loads((ROOT/"intake/OWNER-RESULTS.json").read_text())
g=a["designs"]["R10 lead (028b)"]
factor=(69000/290000)*math.sqrt(1-.0752**2)/math.sqrt(1-.33**2)
mini=dict(scale=.05,face_um=.794624067*.05*1000,core_mm=23.237217906*.05,
          stiffness_factor=factor,G_MPa=factor*6800*.006894757293168361,
          p_design_kPa=factor*95.4608379139,p_gamma1_kPa=factor*g["p_H_kPa"],
          fabrication_radius_min_m=10*max(.025/.794624067,1/23.237217906),
          full_vacuum_sea_level_overload=(101.325/95.4608379139-1))
areas=[x["shell_area_m2"] for x in a["caps"]]
tfD=json.loads((ROOT/"PHYSICAL-CHECKS.json").read_text())["r30_scaled"]["face_5052_mm"]
rig=dict(B_article_diameter_m=5,B_mould_diameter_m=5.4,B_tank_diameter_m=5,
         D_article_required_diameter_m=6,D_fits_B_mould=False,D_fits_B_tank=False,
         area5_m2=areas[3],area6_m2=areas[4],area_multiplier=areas[4]/areas[3],
         D_face_mass_kg=areas[4]*2*tfD*.001*2680,
         D_face_mass_over_B=(areas[4]*2*tfD*.001*2680)/a["costs"]["B_aluminium_mass_kg"],
         gamma_5m_water_if_head_from_pole=149.35825/a["standins"]["5052-O"]["p_H_kPa"],
         gamma_5m_water_if_head_from_base=(149.35825-a["costs"]["pressure_gradient_5mcap_kPa"])/a["standins"]["5052-O"]["p_H_kPa"])
crosses={}
for label in ("S1-be-sphere-d16","S2-be-sphere-d9"):
    r=json.loads((ROOT/"intake/owner-runs"/(label+".json")).read_text())
    crosses[label]=float(np.interp(.088,[0]+[v["core_tau"] for v in r["path"]],
                                  [0]+[v["p_kPa"] for v in r["path"]]))
refinement=[]
for label,original in (("refined-S1","S1-be-sphere-d16"),("refined-C3","C3-be-cap2500-d16")):
    b=json.loads((ROOT/"fe-runs"/(label+".json")).read_text())
    c=json.loads((ROOT/"fe-runs"/(original+".json")).read_text())
    r=dict(label=label,coarse_label=original,coarse_peak_kPa=c["limit_kPa"],
           refined_sample_peak_kPa=max(x["p_kPa"] for x in b["path"]),
           refined_peak_search_kPa=b["limit_kPa"],
           peak_mesh_change_relative=max(x["p_kPa"] for x in b["path"])/c["limit_kPa"]-1,
           coarse_crossings=c["crossings_kPa"],refined_crossings=b["crossings_kPa"])
    refinement.append(r)
caps=[]
for diameter in (3,4,5,6):
    for mat,label in (("Be",{3:"C1",4:"C2",5:"C3",6:"C4"}[diameter]),
                      ("5052-O",{3:"C8",4:"C5",5:"C6",6:"C7"}[diameter])):
        name=next(k for k in o["fe_runs"] if k.startswith(label+"-"))
        b=json.loads((ROOT/"fe-runs"/(name+".json")).read_text())
        base=json.loads((ROOT/"fe-runs"/("S1-be-sphere-d16.json" if mat=="Be" else "S4-al-sphere-d16.json")).read_text())
        caps.append(dict(diameter_m=diameter,material=mat,limit_kPa=b["limit_kPa"],
                         limit_ratio=b["limit_kPa"]/base["limit_kPa"],
                         core_shear_onset_ratio=b["crossings_kPa"]["core_W_shear_typ"]/base["crossings_kPa"]["core_W_shear_typ"]))
out=dict(miniature=mini,rig_and_cost_scope=rig,
         owner_path_tau088_crossing_kPa=crosses,refinement=refinement,caps=caps)
(ROOT/"SUPPLEMENT.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
print(json.dumps(out,indent=2))
