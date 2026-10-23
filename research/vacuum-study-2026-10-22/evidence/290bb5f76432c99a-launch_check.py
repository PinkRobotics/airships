"""Launch one independent check job through the shared host admission tool."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[3]
ap=argparse.ArgumentParser()
ap.add_argument("label")
ap.add_argument("solver_args",nargs=argparse.REMAINDER)
args=ap.parse_args()
directory=ROOT/"execution"/args.label
directory.mkdir(parents=True,exist_ok=False)
code=ROOT/"frame_check.py"
command=[sys.executable,str(WORKSPACE/"tools/simjob.py"),"run","--cores","1","--mem","6G",
         "--",sys.executable,str(code),"--output",str(ROOT/"runs"/args.label),*args.solver_args]
env=os.environ.copy()
env.update(OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1",
           NUMEXPR_NUM_THREADS="1",VECLIB_MAXIMUM_THREADS="1",CUDA_VISIBLE_DEVICES="",
           TMPDIR="unpublished-local-ref:1ffe4110219d37c0")
start=datetime.now(timezone.utc).isoformat()
stamp=time.monotonic()
(directory/"START.json").write_text(json.dumps(dict(command=command,started_utc=start,
    source_sha256=hashlib.sha256(code.read_bytes()).hexdigest(),
    source_bytes=code.stat().st_size,task_time_budget=None),indent=2)+"\n")
with (directory/"stdout.txt").open("w") as stdout,(directory/"stderr.txt").open("w") as stderr:
    proc=subprocess.run(command,env=env,stdout=stdout,stderr=stderr)
text=(directory/"stderr.txt").read_text()
receipt=dict(label=args.label,returncode=proc.returncode,started_utc=start,
    ended_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-stamp,
    admitted="simjob: ADMITTED" in text,refused="simjob: REFUSED" in text,
    released="reservation released" in text)
(directory/"END.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt))
print((directory/"stdout.txt").read_text())
if proc.returncode:
    print(text)
sys.exit(proc.returncode)
