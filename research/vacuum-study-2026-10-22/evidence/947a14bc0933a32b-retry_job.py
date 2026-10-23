"""Authorized administrative retry: unchanged payload/resources, >=60 seconds apart."""
import argparse
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
import time

p=argparse.ArgumentParser()
p.add_argument("--prefix",required=True)
p.add_argument("--mem",default="3G")
p.add_argument("--timeout",default="900")
p.add_argument("script")
p.add_argument("args",nargs=argparse.REMAINDER)
a=p.parse_args()
r=Path(__file__).resolve().parent
attempt=0
while True:
    attempt+=1
    label=f"{a.prefix}-retry{attempt:02d}"
    status=subprocess.run(["ref-81e2f24e4e80426e80f0","unpublished-local-ref:6b66f99ebd630954","status"],
                          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,check=False)
    (r/(label+"-admission-status.txt")).write_text(status.stdout)
    print(json.dumps(dict(at=dt.datetime.now(dt.timezone.utc).isoformat(),label=label,action="admission_attempt")),flush=True)
    result=subprocess.run(["ref-81e2f24e4e80426e80f0","-B",str(r/"run_job.py"),
                           "--label",label,"--mem",a.mem,"--timeout",a.timeout,a.script,*a.args],check=False)
    if result.returncode!=75:
        sys.exit(result.returncode)
    print(json.dumps(dict(label=label,action="authorized_retry_wait",seconds=61)),flush=True)
    time.sleep(61)
