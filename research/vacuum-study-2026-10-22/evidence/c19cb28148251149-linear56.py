"""Radius-reading and meridional convergence of the unchanged linear problem."""
import json
from pathlib import Path
import time
from fem56 import PlasticModel

ROOT=Path(__file__).resolve().parent
out=[]
for radius in ["outer","mid"]:
    for nth in [96,192,384]:
        t=time.monotonic()
        m=PlasticModel(ntheta=nth,ncore=8,nface=2,radius=radius,amplitude=0.)
        dead,_,_=m.linear_buckling(nev=4)
        follower,_,_=m.linear_buckling(nev=4,load_stiffness=True)
        rec={"radius_reading":radius,"radius_outer_mm":m.Ro,"ntheta":nth,
             "ncore":8,"nface":2,"elements":m.ne,"free_dofs":len(m.free),
             "dead_pressure_MPa":dead.tolist(),"follower_pressure_MPa":follower.tolist(),
             "paper_linear_MPa":27.53,"dead_gap_percent":100*(float(dead[0])/27.53-1),
             "elapsed_s":time.monotonic()-t,"tag":"QUESTIONABLE"}
        out.append(rec);print(json.dumps(rec),flush=True)
        (ROOT/"LINEAR.json").write_text(json.dumps(out,indent=2)+"\n")
