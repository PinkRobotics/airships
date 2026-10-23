#!/usr/bin/env python3
"""Preserve a verified no-start refusal before an explicitly reviewed retry."""
import json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parent
def main(name):
    d=ROOT/"runs"/name
    launch=json.loads((d/"LAUNCH.json").read_text())
    reason=(d/"simjob.stderr").read_text()
    assert launch["returncode"]==75 and "nothing was started" in reason
    assert not (d/"SOLVER.json").exists() and not (d/"ccx.stdout").exists()
    number=1
    while (d/f"ADMISSION-REFUSED-{number}-LAUNCH.json").exists():number+=1
    for n in ["LAUNCH.json","simjob.stdout","simjob.stderr"]:
        (d/n).rename(d/f"ADMISSION-REFUSED-{number}-{n}")
    file=ROOT/"ADMISSION-REFUSALS.json"
    rows=json.loads(file.read_text()) if file.exists() else []
    rows.append(dict(run=name,attempt=number,returncode=75,solver_started=False,
        reason=reason,record=str(d/f"ADMISSION-REFUSED-{number}-LAUNCH.json")))
    file.write_text(json.dumps(rows,indent=2)+"\n")
    print(json.dumps(rows[-1]))
if __name__=="__main__":main(sys.argv[1])
