"""Audit completed evidence against raw paths, saved states and resource receipts."""
import datetime
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def audit():
    result=read(ROOT/"RESULTS.json")
    assert result["work_complete"]
    checks=[]

    def check(name,ok,detail=None):
        checks.append({"name":name,"passed":bool(ok),"detail":detail})

    for case in result["pressure_cases"]:
        name=case["name"]
        directory=ROOT/"runs"/name
        history=[json.loads(s) for s in (directory/"PATH.jsonl").read_text().splitlines()]
        p=np.array([r["pressure_MPa"] for r in history])
        u=np.array([r["outer_pole_mm"] for r in history])
        residual=np.array([r["relative_residual"] for r in history])
        jac=np.array([r["minimum_J"] for r in history])
        k=np.array([r["core_equivalent_plastic_strain"] for r in history])
        peak=case["peak"]
        check(name+": path length and step numbers",
              len(history)==case["steps"] and
              [r["step"] for r in history]==list(range(1,len(history)+1)))
        check(name+": finite positive J and accepted residual",
              np.all(np.isfinite(p)) and np.all(np.isfinite(u)) and
              jac.min()>0 and residual.max()<=case["tolerance"],
              {"minimum_J":float(jac.min()),"max_relative_residual":float(residual.max())})
        check(name+": monotone controlled displacement and accumulated plastic strain",
              np.all(np.diff(u)<0) and np.all(np.diff(k)>=-1e-12))
        check(name+": raw global maximum and final fall",
              abs(p.max()-peak["pressure_MPa"])<1e-12 and
              int(p.argmax())+1==peak["step"] and p[-1]<.88*p.max())
        z=np.load(directory/"PEAK.npz")
        m=np.load(directory/"MESH.npz")
        check(name+": saved peak pressure and material states",
              abs(float(z["pressure"])-p.max())<1e-12 and
              abs(float(z["kap"][:,m["kinds"]==0].max())-
                  peak["core_equivalent_plastic_strain"])<1e-12 and
              abs(float(z["kap"][:,m["kinds"]==1].max())-
                  peak["face_equivalent_plastic_strain"])<1e-12)
        tests={
            "core_yield":lambda r:r["core_equivalent_plastic_strain"]>1e-9,
            "face_yield":lambda r:r["face_equivalent_plastic_strain"]>1e-9,
            "core_shear_screen":lambda r:r["core_shear_initial_strength_index"]>=1,
            "foam_extrapolation":lambda r:r["core_extrapolated_points"]>0,
        }
        for key,test in tests.items():
            first=next((i for i,r in enumerate(history) if test(r)),None)
            event=case["first_events"].get(key)
            check(name+": first "+key,
                  (first is None and event is None) or
                  (first is not None and event is not None and
                   event["first_above"]["step"]==first+1 and
                   event["last_below"].get("step",0)==first))
        if case.get("plastic_step_cap") is not None:
            largest=max(r["maximum_core_plastic_increment"] for r in history)
            check(name+": accepted local plastic increment cap",
                  largest<=case["plastic_step_cap"]*(1+1e-10),largest)
    for case in result["indentation_cases"]:
        name=case["name"]
        path=ROOT/"runs"/name
        z=np.load(path/"END.npz")
        check(name+": achieved indentation with positive J",
              case["reason"]=="prescribed indentation completed" and
              abs(float(z["depth"])-case["target_depth_mm"])<1e-10 and
              case["last"]["minimum_J"]>0 and
              case["last"]["relative_residual"]<2e-8)
    material_hashes=set()
    for pinfile in sorted((ROOT/"logs").glob("*/SOURCE-PINS.json")):
        for entry in read(pinfile):
            blob=Path(entry["snapshot"]).read_bytes()
            if Path(entry["snapshot"]).name=="material56.py":
                material_hashes.add(entry["sha256"])
            check("source snapshot: "+str(Path(entry["snapshot"]).relative_to(ROOT)),
                  len(blob)==entry["bytes"] and
                  hashlib.sha256(blob).hexdigest()==entry["sha256"])
    for receipt_path in sorted((ROOT/"logs").glob("*/RECEIPTS.json")):
        receipts=read(receipt_path)
        last=receipts[-1]
        log=(receipt_path.parent/f"attempt-{last['attempt']}.log").read_text()
        check(receipt_path.parent.name+": admitted scope ended and reservation released",
              "simjob: ADMITTED" in log and "reservation released" in log)
        expected=1 if receipt_path.parent.name in ["verification","verification-fixed"] else 0
        check(receipt_path.parent.name+": expected process status",last["exit_code"]==expected,
              {"actual":last["exit_code"],"expected":expected})
    check("same constitutive implementation and tables in all captured job-source snapshots",
          len(material_hashes)==1,sorted(material_hashes))
    for entry in read(ROOT/"INPUT-CUSTODY.json"):
        blob=Path(entry["path"]).read_bytes()
        check("input pin: "+str(Path(entry["path"]).relative_to(ROOT)),
              len(blob)==entry["bytes"] and hashlib.sha256(blob).hexdigest()==entry["sha256"])
    output={"checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "scope":"Raw evidence consistency; not independent material or experimental validation.",
            "checks":checks,"count":len(checks),"all_passed":all(r["passed"] for r in checks)}
    (ROOT/"EVIDENCE-AUDIT.json").write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({"count":len(checks),"all_passed":output["all_passed"],
                      "failures":[r for r in checks if not r["passed"]]},indent=2))
    assert output["all_passed"]


if __name__=="__main__":
    audit()
