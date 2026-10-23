"""Additional numerical and provenance verification; no predecessor code execution."""
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from calculate import Model, I

ROOT = Path(__file__).resolve().parent
R = json.loads((ROOT/"RESULTS.json").read_text())
checks = []
def check(name, ok, **detail):
    checks.append(dict(name=name,pass_=bool(ok),**detail))
    assert ok,(name,detail)

for pin in json.loads((ROOT/"intake/PINS.json").read_text()):
    data=Path(pin["local_path"]).read_bytes()
    check("pin_"+Path(pin["path"]).name,len(data)==pin["bytes"] and hashlib.sha256(data).hexdigest()==pin["sha256"])

chosen=[
    ("R10_af015_scarf_catalog_E_full",10,"af015_scarf",290e9,.0752),
    ("R10_af015_scarf_primer5_catalog_E_full",10,"af015_scarf_primer5",290e9,.0752),
    ("R10_lab8_eb_eta1_catalog_E_full",10,"lab8_eb_eta1",290e9,.0752),
    ("R20_027_full",20,"027_coupled_eta09",293.6e9,.33),
    ("R20_handbook_elastic",20,"027_coupled_eta09",42.5e6*6894.757293168361,.10)]
grid=np.linspace(1e-7,1-1e-7,20001)
for name,rad,route,E,nu in chosen:
    row=next(x for x in R["models"] if x["id"]==name)
    m=Model(rad,route,"full",E,nu)
    Fcy=row["threshold"]["Fcy_Pa"]
    best=-1.
    for core in m.cores:
        e=m.evaluate(grid,core,Fcy)
        best=max(best,float(e["least"].max()))
    check(name+"_dense_20001_all_cores",best<=1+1e-7 and best>1-.002,dense_best_SF=best,
          threshold_MPa=Fcy/1e6,cores=len(m.cores))
    # Uniaxial/axisymmetric membrane force balance is independent of the implementation's SF.
    p=row["threshold"]
    direct_force=m.p*math.pi*m.R**2
    edge_capacity=2*(2*math.pi*m.R*p["tf_m"]*p["demand_Pa"])
    check(name+"_membrane_force_balance",abs(direct_force-edge_capacity)/direct_force<1e-12)

f1,f2,f11,f22,f12=-2.394e-3,-7.800e-4,3.521e-4,2.889e-4,-2.726e-4
q=R["NASA4397_unqualified_polynomial_extrapolation"]["compression_ksi"]
check("NASA_polynomial_axis_reproduction",
      abs(f1*(-50)+f11*50**2-1)<1e-3 and abs(f2*(-57.5)+f22*57.5**2-1)<1e-3)
check("NASA_polynomial_equal_compression_root",abs(-(f1+f2)*q+(f11+f22+f12)*q*q-1)<1e-12)
for p in R["thickness"]:
    check("gauge_monotonic_"+p["id"],0<p["face_SF_multiplier"]<1)
check("all_thresholds_choose_same_core",all(x["threshold"]["core"]=="Hexcel CR-III 5056 3/8-1.0" for x in R["models"]))
original=json.loads((ROOT/"VALIDATION.json").read_text())
result=dict(calculation_checks=len(original),additional_checks=len(checks),
            all_pass=all(x["pass_"] for x in original+checks),checks=checks)
(ROOT/"VERIFICATION.json").write_text(json.dumps(result,indent=2)+"\n")
print({k:v for k,v in result.items() if k!="checks"})
