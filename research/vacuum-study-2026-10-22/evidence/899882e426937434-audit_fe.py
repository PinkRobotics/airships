from pathlib import Path
import csv,json
import numpy as np

ROOT=Path(__file__).resolve().parent
owner=json.loads((ROOT/"intake/OWNER-RESULTS.json").read_text())
aliases=json.loads((ROOT/"FE-ALIASES.json").read_text())
rows=[];paths=[]

def append(row,field,a,b,category):
    rows.append(dict(row=row,field=field,owner=a,independent=b,
                     delta=None if a is None or b is None else b-a,
                     relative_delta=None if a is None or b is None or a==0 else b/a-1,
                     category=category))

for label,a in owner["fe_runs"].items():
    b=json.loads((ROOT/"fe-runs"/(aliases.get(label,label)+".json")).read_text())
    assert b["status"]=="complete"
    raw=json.loads((ROOT/"intake/owner-runs"/(label+".json")).read_text())
    for field in ("p_H_kPa","Vc"):
        append(label,field,a[field],b["reference"][field],"reference")
    for field in ("limit_kPa","gamma_H_elastic"):
        append(label,field,a[field],b[field],"independent FE")
    for own,ours in (("face_yield_outer_kPa","face_yield_outer"),
                     ("face_yield_inner_kPa","face_yield_inner"),
                     ("core_W_shear_typ_kPa","core_W_shear_typ"),
                     ("core_W_shear_min_kPa","core_W_shear_min"),
                     ("core_crush_typ_kPa","core_crush_typ")):
        append(label,own,a[own],b["crossings_kPa"][ours],"independent FE stress crossing")
    assert len(raw["path"])==len(b["path"])
    for i,(op,cp) in enumerate(zip(raw["path"],b["path"])):
        assert abs(op["pole_dz_mm"]-cp["pole_dz_mm"])<1e-7
        for field in ("p_kPa","outer_vm","inner_vm","core_tau","core_min_snn"):
            paths.append(dict(row=label,index=i,pole_dz_mm=cp["pole_dz_mm"],field=field,
                              owner=op[field],independent=cp[field],delta=cp[field]-op[field],
                              relative_delta=cp[field]/op[field]-1))
for name,data in (("FE-COMPARISONS.csv",rows),("FE-PATH-COMPARISONS.csv",paths)):
    with (ROOT/name).open("w") as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
summary={}
for field in {r["field"] for r in rows}:
    good=[r for r in rows if r["field"]==field and r["relative_delta"] is not None]
    summary[field]=max(good,key=lambda r:abs(r["relative_delta"]))
pathsummary={field:max([r for r in paths if r["field"]==field],key=lambda r:abs(r["relative_delta"]))
             for field in {r["field"] for r in paths}}
data=dict(distinct_models=20,exact_input_aliases=aliases,reported_run_count=23,
          scalar_comparisons=len(rows),path_comparisons=len(paths),
          max_relative_by_field=summary,path_max_relative_by_field=pathsummary,
          capacity_validated=False,
          interpretation="Agreement refers to conditional equilibrium branches. All delta values retained, including stress diagnostics differences.")
(ROOT/"FE-SUMMARY.json").write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")
print(json.dumps(data,indent=2))
