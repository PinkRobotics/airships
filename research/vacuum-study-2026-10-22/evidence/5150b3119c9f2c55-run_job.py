"""One admitted scientific postprocessing job; technical watchdog, no task cap."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys
import time

root=Path(__file__).resolve().parent
work=root.parents[3]
label=sys.argv[1]
directory=root/"execution"/label
directory.mkdir(parents=True,exist_ok=False)
code=root/"reliability.py"
command=[sys.executable,str(work/"tools/simjob.py"),"run","--cores","1","--mem","1G",
         "--",sys.executable,str(code)]
env=os.environ.copy()
env.update(OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1",
           NUMEXPR_NUM_THREADS="1",CUDA_VISIBLE_DEVICES="",TMPDIR="unpublished-local-ref:1ffe4110219d37c0")
start=datetime.now(timezone.utc).isoformat()
clock=time.monotonic()
(directory/"START.json").write_text(json.dumps(dict(command=command,started_utc=start,
    source_sha256=hashlib.sha256(code.read_bytes()).hexdigest(),
    source_bytes=code.stat().st_size,
    source_data_sha256=hashlib.sha256((root/"SOURCE-DATA.json").read_bytes()).hexdigest(),
    task_time_budget=None),indent=2)+"\n")
with (directory/"stdout.txt").open("w") as out,(directory/"stderr.txt").open("w") as err:
    proc=subprocess.run(command,env=env,stdout=out,stderr=err)
stderr=(directory/"stderr.txt").read_text()
receipt=dict(label=label,returncode=proc.returncode,started_utc=start,
    ended_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-clock,
    admitted="simjob: ADMITTED" in stderr,refused="simjob: REFUSED" in stderr,
    released="reservation released" in stderr)
(directory/"END.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt))
if proc.returncode:
    print((directory/"stdout.txt").read_text())
    print(stderr)
sys.exit(proc.returncode)
