#!/usr/bin/env python3
"""Finite serial completion stages; stop on any refusal or numerical error."""
import datetime,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent
def main():
    file=ROOT/"NUMERICS-FINALIZATION.json"
    history=json.loads(file.read_text()) if file.exists() else []
    stages=[("exact-target-audit",["exact_target_audit.py"]),
            ("thermal-strength-debit",["refine.py","--cold-governing"]),
            ("endpoint-calibration",["calibrate.py"]),
            ("actual-yield-confirmations",["boundary_checks.py"])]
    for name,args in stages:
        if any(h["stage"]==name and h["status"]=="done" for h in history):
            continue
        record=dict(stage=name,started_at=datetime.datetime.now().astimezone().isoformat(),
                    status="running")
        history.append(record)
        file.write_text(json.dumps(history,indent=2)+"\n")
        result=subprocess.run([sys.executable,str(ROOT/args[0]),*args[1:]])
        record.update(ended_at=datetime.datetime.now().astimezone().isoformat(),
                      returncode=result.returncode,
                      status="done" if result.returncode==0 else "stopped")
        file.write_text(json.dumps(history,indent=2)+"\n")
        if result.returncode:return result.returncode
    return 0
if __name__=="__main__":sys.exit(main())
