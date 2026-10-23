"""Record admitted scientific invocations; no automatic retry after refusal."""
from pathlib import Path
import sys, json, subprocess, datetime, hashlib, os
ROOT = Path(__file__).resolve().parent
tag, *command = sys.argv[1:]
scratch = Path("unpublished-local-ref:d1b1f2c706a76783")
scratch.mkdir(exist_ok=True)
env = {**os.environ, "TMPDIR": str(scratch), "OMP_NUM_THREADS": "1",
       "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
       "NUMEXPR_NUM_THREADS": "1", "PYTHONDONTWRITEBYTECODE": "1"}
cmd = ["python3", "tools/simjob.py", "run", "--cores", "1", "--mem", "1G", "--", *command]
receipt = {"tag": tag, "command": cmd, "started_at": datetime.datetime.now().astimezone().isoformat(),
           "cores": 1, "memory": "1G", "scratch": str(scratch),
           "source_pins": [{"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                           for p in sorted(set(ROOT.glob("*.py")) | {Path(s) for s in command if Path(s).is_file()})]}
with (ROOT/f"{tag}.stdout").open("w") as out, (ROOT/f"{tag}.stderr").open("w") as err:
    run = subprocess.run(cmd, env=env, stdout=out, stderr=err)
receipt.update(ended_at=datetime.datetime.now().astimezone().isoformat(), exit_code=run.returncode,
               release="simjob run subprocess returned; tool owns scope/reservation lifecycle")
(ROOT/f"{tag}.execution.json").write_text(json.dumps(receipt, indent=2)+"\n")
print(json.dumps(receipt, indent=2))
print((ROOT/f"{tag}.stdout").read_text()[-10000:])
print((ROOT/f"{tag}.stderr").read_text()[-3000:])
sys.exit(run.returncode)
