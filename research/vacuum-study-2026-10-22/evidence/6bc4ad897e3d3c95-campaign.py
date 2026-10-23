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
            if k not in ["name","note","cores"]:cmd += ["--"+k.replace("_","-"),str(v)]
        subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL)
    original=None
    while not (d/"SOLVER.json").exists():
        r=run(name,cores=job.get("cores",1))
        if original is None:original=r
        assert r["argv"]==original["argv"] and r["deck_sha256"]==original["deck_sha256"]
        assert r["cores"]==original["cores"] and r["mem"]==original["mem"]
        if r["returncode"]==75:
            from archive_refusal import main as archive_refusal
            policy=json.loads((ROOT/"RETRY-POLICY.json").read_text())
            assert policy["minimum_wait_seconds"]>=60
            archive_refusal(name)
            print(json.dumps(dict(run=name,status="waiting_for_admission",
                authority=policy["authority"],wait_seconds=60)),flush=True)
            # Standing order: wait at least a minute, retry the same command.
            # Two short sleeps keep individual waits bounded.
            time.sleep(30);time.sleep(30)
            continue
        if r["returncode"] in [69,124] or not (d/"SOLVER.json").exists():
            raise RuntimeError(f"admission or timeout, inspect without silent retry: {name} {r['returncode']}")
    r=collect(name)
    print(json.dumps(r),flush=True)
    return r
if __name__=="__main__":
    jobs=json.loads(pathlib.Path(sys.argv[1]).read_text())
    for j in jobs:execute(j)
