"""Check the finished review's evidence, dispositions and numerical agreements."""
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def read(name):
    return json.loads((ROOT/name).read_text())
checks=[]
def check(name,condition,evidence):
    checks.append({"check":name,"passed":bool(condition),"evidence":evidence})
    assert condition,(name,evidence)

r=read("RESULTS.json")
f=read("FIELD-CHECK.json")
l=read("LINEAR-CHECK.json")
a=read("ACCOUNT-CHECK.json")
o=read("sources/062--RESULTS.json")
b=f["best_reconstruction"]
check("Independent pressure/state equilibrium agrees",
      abs(b["pressure_difference_MPa"])<1e-7 and b["relative_free_force_residual"]<1e-7,
      {"difference_MPa":b["pressure_difference_MPa"],"relative_residual":b["relative_free_force_residual"]})
check("State layout and material surface consistent",
      min(x["relative_free_force_residual"] for x in f["layout_checks"] if x["relative_free_force_residual"]>1e-7)>20
      and b["max_foam_yield_surface_ratio"]<1+1e-8,
      {"other_conventions_min_residual":min(x["relative_free_force_residual"] for x in f["layout_checks"] if x["relative_free_force_residual"]>1e-7),
       "foam_yield_ratio":b["max_foam_yield_surface_ratio"],"extrapolated_points":b["core_extrapolated_points"]})
check("Four raw path maxima are followed by lower pressure samples",
      len(f["pressure_path_checks"])==4 and all(x["three_following_lower"] for x in f["pressure_path_checks"]),
      {"scope":"Sampled peak, not physical/stability qualification"})
check("Both independent linear anchors agree",
      len(l["cases"])==2 and all(abs(x["difference_MPa"])<1e-8 and x["eigen_relative_residual"]<1e-8 for x in l["cases"]),
      {"max_difference_MPa":max(abs(x["difference_MPa"]) for x in l["cases"]),
       "max_eigen_residual":max(x["eigen_relative_residual"] for x in l["cases"])})
errors=[]
for row in a["shape"]:
    ref=next(x for x in o["scaling"] if x["R_m"]==row["R_m"])
    for z in row["tolerances"]:
        original=next(x for x in ref["tolerances"] if x["SF"]==z["SF"])
        key="cure_debited_amplitude_mm" if z["with_cure"] else "no_cure_amplitude_mm"
        errors.append(abs(z["amplitude_mm"]-original[key]))
check("Three shape targets and their no-cure/calibration controls reproduce",
      max(errors)<1e-9,{"max_difference_mm":max(errors),"comparisons":len(errors)})
check("Cost endpoints reproduce conditional arithmetic",
      len(a["cost"])==6 and max(abs(x["difference_USD"]) for x in a["cost"])<.01,
      {"max_total_difference_USD":max(abs(x["difference_USD"]) for x in a["cost"]),
       "hall_and_handling":"Supplied allowances; source/scale gap retained as NFI"})
fix=read("FIXES.json")["items"]
check("Six payload corrections preserve no-float sign and remain unreviewed",
      len(fix)==6 and all(x["no_float_sign_preserved"] for x in a["mass"])
      and all(x["review_status"].startswith("unreviewed") for x in fix),
      {"payload_increase_kg":[x["corrected_minus_owner_kg"] for x in a["mass"]],
       "independent_second_review":False})
allowed={"reproduces","differs","cannot be checked without a source or a test"}
check("Exactly one permitted disposition per prelisted claim",
      len(r["claims"])==17 and len({x["id"] for x in r["claims"]})==17
      and all(x["disposition"] in allowed for x in r["claims"])
      and sum(x["disposition"]=="reproduces" for x in r["claims"])==16,
      r["counts"])

pin_count=0
for label,data in read("SOURCE-INDEX.json").items():
    for name,e in data["artifacts"].items():
        raw=Path(e["local_path"]).read_bytes()
        assert len(raw)==e["bytes"] and hashlib.sha256(raw).hexdigest()==e["sha256"]
        pin_count+=1
for e in read("EVIDENCE-PINS.json").values():
    path=Path(e["local_path"])
    assert path.suffix not in (".py",".sh",".pyc",".ipynb")
    raw=path.read_bytes()
    assert len(raw)==e["bytes"] and hashlib.sha256(raw).hexdigest()==e["sha256"]
    pin_count+=1
for e in read("BRIEF-PINS.json"):
    raw=Path(e["local_path"]).read_bytes()
    assert len(raw)==e["original"]["bytes"] and hashlib.sha256(raw).hexdigest()==e["original"]["sha256"]
    pin_count+=1
check("Filed source, evidence and dispatch pins match; no owner executable copied",
      True,{"verified_pins":pin_count})
n=read("NFI.json")["items"]
check("Unresolved physical/source claims separate from fixes",
      len({x["id"] for x in n})==len(n)==11 and all(x["status"]=="open" for x in n),
      {"NFI_rows":len(n),"physical_qualification":"open"})
out={"unit":r["unit"],"status":"PASS","scope":"Review-package consistency; not a second review of corrections or physical qualification",
     "measured_at":datetime.now().astimezone().isoformat(),"checks":checks}
(ROOT/"VALIDATION.json").write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
print(f"PASS: {len(checks)} checks; {pin_count} source pins; 17 dispositions; six unreviewed correction rows.")
