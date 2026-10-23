"""Record one simjob attempt; retries retain identical scientific argv/resources."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
label, *scientific = sys.argv[1:]
assert label and scientific
directory = ROOT/"execution"/label
directory.mkdir(parents=True, exist_ok=True)
attempt = len(list(directory.glob("attempt-*.json")))+1
argv = [sys.executable, str(Path("tools/simjob.py").resolve()), "run",
        "--cores", "1", "--mem", "1G", "--timeout", "7200", "--",
        sys.executable, *scientific]
environment = dict(os.environ, TMPDIR="unpublished-local-ref:1ffe4110219d37c0", PYTHONDONTWRITEBYTECODE="1",
                   OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1",
                   NUMEXPR_NUM_THREADS="1", CUDA_VISIBLE_DEVICES="")
sources = []
for p in sorted(ROOT.glob("*.py")):
    raw = p.read_bytes()
    sources.append(dict(path=str(p), sha256=hashlib.sha256(raw).hexdigest(), bytes=len(raw)))
start = datetime.now(timezone.utc).isoformat()
before = time.monotonic()
stdout_path = directory/f"attempt-{attempt:03d}.stdout.log"
stderr_path = directory/f"attempt-{attempt:03d}.stderr.log"
with stdout_path.open("w") as out, stderr_path.open("w") as err:
    done = subprocess.run(argv, env=environment, stdout=out, stderr=err)
record = dict(started=start, finished=datetime.now(timezone.utc).isoformat(),
              elapsed_seconds=time.monotonic()-before, returncode=done.returncode,
              argv=argv, argv_sha256=hashlib.sha256(json.dumps(argv).encode()).hexdigest(),
              resources=dict(cores=1, memory="1G", timeout_seconds=7200),
              source_pins=sources, stdout=str(stdout_path), stderr=str(stderr_path),
              no_time_budget=True)
(directory/f"attempt-{attempt:03d}.json").write_text(json.dumps(record, indent=2)+"\n")
print(stderr_path.read_text())
print(stdout_path.read_text())
print(json.dumps({"label": label, "attempt": attempt, "returncode": done.returncode,
                  "elapsed_seconds": record["elapsed_seconds"]}))
raise SystemExit(done.returncode)
