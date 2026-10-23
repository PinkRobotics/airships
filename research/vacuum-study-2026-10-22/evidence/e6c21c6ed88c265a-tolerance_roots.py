from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import brentq,minimize_scalar
from independent_fe import Model
from fe_check import reference

ROOT=Path(__file__).resolve().parent
original=json.loads((ROOT/"intake/owner-runs/S1-be-sphere-d16.json").read_text())
base={k:float(v) for k,v in original["args"].items() if k!="label"}
base["nth"]=512
P=.0954608379139
records=[]
def operating(amp):
    a={**base,"amp":float(amp)}
    m=Model(**a);u=None
    for p in np.linspace(P/12,P,12):u,info=m.solve_load(float(p),u)
    *_,diag=m.evaluate(u,True)
    record=dict(amplitude_mm=float(amp),p_kPa=P*1000,**diag,solver=info)
    records.append(record)
    (ROOT/"TOLERANCE-OPERATING-TRIALS.json").write_text(json.dumps(records,indent=2)+"\n")
    print("operating",amp,diag["outer_vm"],diag["core_tau"],flush=True)
    return diag

roots={}
for label,field,target,bracket in [
    ("outer_face_345MPa","outer_vm",345.,(.5,2)),
    ("core_W_typ_35psi","core_tau",35*.006894757293168361,(1,4)),
    ("core_W_min_25psi","core_tau",25*.006894757293168361,(1,3))]:
    start=time.monotonic()
    amp=brentq(lambda v:operating(v)[field]-target,*bracket,xtol=2e-6)
    roots[label]={"amplitude_mm":float(amp),"diagnostic_at_root":operating(amp),
                  "elapsed_seconds":time.monotonic()-start}
    (ROOT/"TOLERANCE-ROOTS.json").write_text(json.dumps(roots,indent=2)+"\n")

peaktrials=[]
def peak(amp):
    m=Model(**{**base,"amp":float(amp)})
    u=np.zeros(m.ndof);p=0
    states=[]
    for target in np.arange(-2.,-74.,-2.):
        u,p,info=m.solve_control(float(target),u,p)
        states.append((target,u.copy(),p))
        if len(states)>4 and p<max(s[2] for s in states)*.995:break
    j=int(np.argmax([s[2] for s in states]));assert 0<j<len(states)-1
    startstate=states[j-1]
    def objective(target):
        un,pn,info=m.solve_control(float(target),startstate[1],startstate[2])
        return -pn
    fit=minimize_scalar(objective,bounds=(states[j+1][0],states[j-1][0]),method="bounded",
                        options={"xatol":2e-5})
    result=dict(amplitude_mm=float(amp),peak_pressure_kPa=float(-fit.fun*1000),
                pole_displacement_mm=float(fit.x),gamma=float(-fit.fun*1000/reference(base)["p_H_kPa"]))
    peaktrials.append(result)
    (ROOT/"TOLERANCE-PEAK-TRIALS.json").write_text(json.dumps(peaktrials,indent=2)+"\n")
    print("peak",result,flush=True)
    return -fit.fun

amp=brentq(lambda v:peak(v)-P,4.,6.,xtol=2e-5)
roots["elastic_pressure_maximum_at_operating"]={"amplitude_mm":float(amp),"pressure_kPa":float(peak(amp)*1000)}
roots["scope"]="Conditional coarse-mesh axisymmetric elastic paths; not physical capacities or qualified tolerances."
(ROOT/"TOLERANCE-ROOTS.json").write_text(json.dumps(roots,indent=2,allow_nan=False)+"\n")
print(json.dumps(roots,indent=2),flush=True)
