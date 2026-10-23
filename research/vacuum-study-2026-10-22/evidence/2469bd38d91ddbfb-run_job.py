"""Record and admit one checker computation; never bypass a capacity refusal."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument("label")
p.add_argument("--mem",default="6G")
p.add_argument("program")
p.add_argument("arguments",nargs=argparse.REMAINDER)
a=p.parse_args()
folder=ROOT/"execution"/a.label
folder.mkdir(parents=True,exist_ok=False)
(folder/"source").mkdir()
pins=[]
for source in sorted(ROOT.glob("*.py")):
    dst=folder/"source"/source.name
    shutil.copyfile(source,dst)
    pins.append(dict(path=str(dst),sha256=hashlib.sha256(dst.read_bytes()).hexdigest(),bytes=dst.stat().st_size))
command=[sys.executable,str(ROOT.parents[3]/"tools/simjob.py"),"run","--cores","1","--mem",a.mem,
         "--",sys.executable,str(ROOT/a.program),*a.arguments]
env=os.environ.copy()
env.update(OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1",NUMEXPR_NUM_THREADS="1",
           CUDA_VISIBLE_DEVICES="",TMPDIR="unpublished-local-ref:1ffe4110219d37c0",PYTHONDONTWRITEBYTECODE="1")
start=datetime.now(timezone.utc).isoformat();clock=time.monotonic()
(folder/"START.json").write_text(json.dumps(dict(command=command,source_pins=pins,started_utc=start,
    task_time_limit=None,phase_time_limit=None),indent=2)+"\n")
with (folder/"stdout.txt").open("w") as out,(folder/"stderr.txt").open("w") as err:
    proc=subprocess.run(command,env=env,stdout=out,stderr=err)
stderr=(folder/"stderr.txt").read_text()
result=dict(label=a.label,returncode=proc.returncode,started_utc=start,
    ended_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,
    admitted="simjob: ADMITTED" in stderr,refused="simjob: REFUSED" in stderr,
    released="reservation released" in stderr)
(folder/"END.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result),flush=True)
if proc.returncode:
    print((folder/"stdout.txt").read_text())
    print(stderr)
sys.exit(proc.returncode)
