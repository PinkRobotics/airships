"""Administrative simjob launcher; every scientific invocation receives its own receipt."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

p = argparse.ArgumentParser()
p.add_argument("--label", required=True)
p.add_argument("--mem", default="4G")
p.add_argument("--timeout", default="3600")
p.add_argument("script")
p.add_argument("args", nargs=argparse.REMAINDER)
a = p.parse_args()
root = Path(__file__).resolve().parent
run = root / "execution" / a.label
run.mkdir(parents=True, exist_ok=False)
tmp = run / "scratch"
tmp.mkdir()
env = ["PATH=ref-ccc203c53b7d040ba4dc:/bin", "LANG=C.UTF-8", "TMPDIR=" + str(tmp),
       "MPLCONFIGDIR=" + str(tmp / "matplotlib"), "XDG_CACHE_HOME=" + str(tmp / "cache"),
       "CUDA_VISIBLE_DEVICES=", "OPENBLAS_NUM_THREADS=1", "OMP_NUM_THREADS=1",
       "MKL_NUM_THREADS=1", "NUMEXPR_NUM_THREADS=1", "BLIS_NUM_THREADS=1",
       "VECLIB_MAXIMUM_THREADS=1"]
cmd = ["ref-81e2f24e4e80426e80f0", "unpublished-local-ref:6b66f99ebd630954", "run",
       "--cores", "1", "--mem", a.mem, "--timeout", a.timeout, "--",
       "ref-d9af09a16f3a81bf2ded", "-i", *env, "ref-81e2f24e4e80426e80f0", "-I", "-B",
       str(root / a.script), *a.args]
snapshot = run / "source"
snapshot.mkdir()
pins = []
for path in sorted(root.glob("*.py")):
    b = path.read_bytes()
    (snapshot / path.name).write_bytes(b)
    pins.append({"path": str(path), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
start, mono = datetime.datetime.now(datetime.timezone.utc).isoformat(), time.monotonic()
(run / "START.json").write_text(json.dumps({"at": start, "command": cmd, "source_pins": pins}, indent=2) + "\n")
with (run / "stdout.log").open("w") as out, (run / "stderr.log").open("w") as err:
    result = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=out, stderr=err, cwd=root, check=False)
receipt = {"started_utc": start, "ended_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "elapsed_seconds": time.monotonic() - mono, "returncode": result.returncode,
           "command": cmd, "source_pins": pins, "time_budget": None,
           "timeout_is_technical_watchdog": True}
(run / "END.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"label": a.label, "returncode": result.returncode,
                  "elapsed_seconds": receipt["elapsed_seconds"], "receipt": str(run / "END.json")}))
print((run / "stdout.log").read_text()[-7000:])
print((run / "stderr.log").read_text()[-4000:])
sys.exit(result.returncode)
