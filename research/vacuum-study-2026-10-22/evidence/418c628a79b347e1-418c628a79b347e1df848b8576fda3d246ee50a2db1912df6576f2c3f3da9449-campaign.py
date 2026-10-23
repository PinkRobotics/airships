#!/usr/bin/env python3
"""Serial run list. Resume skips completed native results; no solver bypass."""
import json, pathlib, subprocess, sys, time
from collect import collect
from run_job import run
ROOT=pathlib.Path(__file__).resolve().parent
def execute(job):
    name=job["name"]; d=ROOT/"runs"/name
    if (d/"SUMMARY.json").exists() and (d/"SOLVER.json").exists():
        return json.loads((d/"SUMMARY.json").read_text())
    if not (d/"MODEL.json").exists():
        cmd=[sys.executable,str(ROOT/"axisymmetric.py"),name,"--case","lead028b",
             "--analysis","static","--ntheta","128","--grading","2",
             "--meridian","W","--yield-stress","345","--pressure","0.18",
             "--increment","0.02","--maximum-increment","0.02"]
        for k,v in job.items():
            if k not in ["name","note"]:cmd += ["--"+k.replace("_","-"),str(v)]
        subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL)
    if not (d/"SOLVER.json").exists():
        r=run(name)
        if r["returncode"] in [69,75,124] or not (d/"SOLVER.json").exists():
            raise RuntimeError(f"admission or timeout, inspect without silent retry: {name} {r['returncode']}")
    r=collect(name)
    print(json.dumps(r),flush=True)
    return r
if __name__=="__main__":
    jobs=json.loads(pathlib.Path(sys.argv[1]).read_text())
    for j in jobs:execute(j)
