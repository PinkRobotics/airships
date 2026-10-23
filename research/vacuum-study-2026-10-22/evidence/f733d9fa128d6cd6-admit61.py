"""Record a bounded one-core scientific invocation; retry only unchanged exit 75."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime

root=Path(__file__).resolve().parent
command=[sys.executable,"tools/simjob.py","run","--cores","1","--mem","1G",
         "--",sys.executable,str(root/sys.argv[1]),*sys.argv[2:]]
attempt=0
stamp=datetime.now().astimezone().strftime("%Y%m%dT%H%M%S")
while True:
    attempt+=1
    name=f"{stamp}-{Path(sys.argv[1]).stem}-{attempt}"
    started=datetime.now().astimezone().isoformat()
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.iterdir() if p.is_file() and p.suffix==".py"}
    with (root/(name+".log")).open("w") as output:
        child=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        for line in child.stdout:
            output.write(line); output.flush()
            print(line,end="",flush=True)
        code=child.wait()
    (root/(name+".execution.json")).write_text(json.dumps({
        "started":started,"ended":datetime.now().astimezone().isoformat(),
        "argv":command,"cores":1,"memory":"1G","exit_code":code,
        "source_sha256":hashes,"log":name+".log"},indent=2)+"\n")
    if code!=75:
        raise SystemExit(code)
    print("Admission refused; retaining the identical one-core/1 GiB command.",flush=True)
    time.sleep(30)
