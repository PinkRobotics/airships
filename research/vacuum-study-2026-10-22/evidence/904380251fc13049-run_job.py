"""Admit one single-core reliability postprocessing job with no task/phase cap."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

root = Path(__file__).resolve().parent
label = sys.argv[1]
directory = root / "execution" / label
directory.mkdir(parents=True, exist_ok=False)
command = [sys.executable, str(root.parents[3] / "tools/simjob.py"),
           "run", "--cores", "1", "--mem", "1G", "--", sys.executable, str(root / "fold.py")]
env = os.environ.copy()
env.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
           NUMEXPR_NUM_THREADS="1", CUDA_VISIBLE_DEVICES="", TMPDIR="unpublished-local-ref:1ffe4110219d37c0")
start = datetime.now(timezone.utc).isoformat()
clock = time.monotonic()
pins = []
for name in ["fold.py", "run_job.py", "INPUTS.json"]:
    p = root / name
    pins.append(dict(path=str(p), bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(directory / "START.json").write_text(json.dumps(dict(
    label=label, started_utc=start, command=command, source_pins=pins,
    task_time_limit=None, phase_time_limit=None), indent=2) + "\n")
with (directory / "stdout.txt").open("w") as out, (directory / "stderr.txt").open("w") as err:
    proc = subprocess.run(command, env=env, stdout=out, stderr=err)
stderr = (directory / "stderr.txt").read_text()
receipt = dict(label=label, returncode=proc.returncode, started_utc=start,
    ended_utc=datetime.now(timezone.utc).isoformat(), elapsed_seconds=time.monotonic()-clock,
    admitted="simjob: ADMITTED" in stderr, refused="simjob: REFUSED" in stderr,
    released="reservation released" in stderr)
(directory / "END.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
if proc.returncode:
    print((directory / "stdout.txt").read_text())
    print(stderr)
sys.exit(proc.returncode)
