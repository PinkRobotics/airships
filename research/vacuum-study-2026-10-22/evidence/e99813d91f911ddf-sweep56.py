"""Sequential material/mesh scenarios within a single admitted simjob."""
import argparse
import json
from pathlib import Path
import time
from fem56 import PlasticModel,trace

ROOT=Path(__file__).resolve().parent
groups={
    "mesh":[
        ("base96c4",dict(ntheta=96,ncore=4,nface=2),.02,.04),
        ("base192c4",dict(ntheta=192,ncore=4,nface=2),.02,.04),
        ("base192c8",dict(ntheta=192,ncore=8,nface=2),.02,.04),
        ("base192c12",dict(ntheta=192,ncore=12,nface=3),.02,.04),
        ("base384c8",dict(ntheta=384,ncore=8,nface=2),.02,.04),
    ],
    "sensitivity":[
        ("mid96c8",dict(ntheta=96,ncore=8,nface=2,radius="mid"),.02,.04),
        ("alpha1p5-96c8",dict(ntheta=96,ncore=8,nface=2,alpha=1.5),.02,.04),
        ("alpha3-96c8",dict(ntheta=96,ncore=8,nface=2,alpha=3.),.02,.04),
        ("foam090-96c8",dict(ntheta=96,ncore=8,nface=2,foam_scale=.9),.02,.04),
        ("foam110-96c8",dict(ntheta=96,ncore=8,nface=2,foam_scale=1.1),.02,.04),
        ("steel-literal-96c8",dict(ntheta=96,ncore=8,nface=2,steel_scale=10.),.02,.04),
    ],
}
a=argparse.ArgumentParser();a.add_argument("group",choices=list(groups))
args=a.parse_args();out=[]
for name,pars,step,maximum in groups[args.group]:
    print(json.dumps({"starting":name,"parameters":pars}),flush=True)
    m=PlasticModel(**pars)
    r=trace(m,ROOT/"runs"/name,step=step,max_step=maximum,end_displacement=10.)
    out.append(r)
    (ROOT/f"SWEEP-{args.group}.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"completed":name,"peak_MPa":r["peak"]["pressure_MPa"] if r["peak"] else None,
                      "reason":r["reason"],"elapsed_s":r["elapsed_s"]}),flush=True)
