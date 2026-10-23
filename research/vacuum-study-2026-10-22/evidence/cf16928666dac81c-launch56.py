"""Owned simjob launcher: measured resource receipts; unchanged 75 retries."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
a=argparse.ArgumentParser()
a.add_argument("name")
a.add_argument("--mem",default="4G")
a.add_argument("--timeout",type=int,default=7200)
a.add_argument("command",nargs=argparse.REMAINDER)
args=a.parse_args()
command=args.command
if command and command[0]=="--":command=command[1:]
assert command
logdir=ROOT/"logs"/args.name
logdir.mkdir(parents=True,exist_ok=False)
source_pins=[]
for source in [*ROOT.glob("*.py"),*ROOT.glob("reuse/*.py")]:
    blob=source.read_bytes()
    snap=logdir/"source"/source.relative_to(ROOT)
    snap.parent.mkdir(parents=True,exist_ok=True)
    snap.write_bytes(blob)
    source_pins.append({"path":str(source),"snapshot":str(snap),
                        "sha256":hashlib.sha256(blob).hexdigest(),"bytes":len(blob)})
(logdir/"SOURCE-PINS.json").write_text(json.dumps(source_pins,indent=2)+"\n")
argv=["python3","unpublished-local-ref:6b66f99ebd630954","run","--cores","1",
      "--mem",args.mem,"--timeout",str(args.timeout),"--","ref-c5feaeda041c435960d7",
      "-v","-o",str(logdir/"resource.txt"),*command]
env=os.environ.copy()
env["OPENBLAS_NUM_THREADS"]="1";env["OMP_NUM_THREADS"]="1"
env["NUMBA_NUM_THREADS"]="1"
env["NUMBA_CACHE_DIR"]=str(ROOT/"scratch/numba")
env["MPLCONFIGDIR"]=str(ROOT/"scratch/matplotlib")
for key in ["NUMBA_CACHE_DIR","MPLCONFIGDIR"]:Path(env[key]).mkdir(parents=True,exist_ok=True)
records=[];attempt=0
while True:
    attempt+=1
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick=time.monotonic()
    with (logdir/f"attempt-{attempt}.log").open("x") as out:
        p=subprocess.Popen(argv,cwd=ROOT,env=env,stdout=out,stderr=subprocess.STDOUT)
        rc=p.wait()
    end=datetime.datetime.now(datetime.timezone.utc).isoformat()
    record={"attempt":attempt,"argv":argv,"started_at":start,"ended_at":end,
            "elapsed_s":time.monotonic()-tick,"exit_code":rc,"cores":1,
            "memory_cap":args.mem,"timeout_s":args.timeout,
            "retry_authority":"CARD056 pinned COMMON.md: unchanged exit75 retries permitted"}
    records.append(record)
    (logdir/"RECEIPTS.json").write_text(json.dumps(records,indent=2)+"\n")
    print(json.dumps({"name":args.name,"attempt":attempt,"exit_code":rc,
                      "elapsed_s":record["elapsed_s"],"log":str(logdir/f"attempt-{attempt}.log")}),flush=True)
    if rc!=75:break
    # A retry delay is an admission wait, never a task cap.
    time.sleep(45)
raise SystemExit(rc)
