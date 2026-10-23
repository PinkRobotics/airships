"""Admission retries authorized by the MAINLINE-051 resume order.

Only exit 75 is retried. Resources and inner command remain unchanged.
Every retry waits at least 60 seconds after the latest refusal.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import subprocess
import sys
import time

p=argparse.ArgumentParser()
p.add_argument("--root",type=Path,default=Path(__file__).resolve().parent)
p.add_argument("--prefix",required=True)
p.add_argument("--mem",default="1G")
p.add_argument("program")
p.add_argument("arguments",nargs=argparse.REMAINDER)
a=p.parse_args()
while True:
    previous=sorted((a.root/"execution").glob(a.prefix+"-*/END.json"))
    number=max([int(x.parent.name.rsplit("-",1)[1]) for x in previous]+[0])+1
    if previous:
        latest=max((json.loads(x.read_text()) for x in previous),key=lambda x:x["ended_utc"])
        if latest["returncode"]==75:
            age=(datetime.now(timezone.utc)-datetime.fromisoformat(latest["ended_utc"])).total_seconds()
            if age<60:
                time.sleep(60-age)
    command=[sys.executable,str(a.root/"run_job.py"),f"{a.prefix}-{number:02}",
             "--mem",a.mem,a.program,*a.arguments]
    rc=subprocess.call(command)
    if rc!=75:
        sys.exit(rc)
