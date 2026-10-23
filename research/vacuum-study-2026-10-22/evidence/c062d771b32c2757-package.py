"""Hash and package the partial filing; never run numerical drafts."""
from pathlib import Path
from datetime import datetime,timezone
import ast
import hashlib
import json
import tarfile

R=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes()
    return dict(path=str(p.resolve()),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def save(p,data):
    p.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")

syntax=[]
for p in sorted(R.glob("*.py")):
    ast.parse(p.read_text())
    syntax.append(dict(file=p.name,syntax_valid=True,
        validation="completed target calculation" if p.name=="targets.py" else
        "metadata operation" if p.name in ["package.py","build_documents.py","run_job.py"] else "unexecuted numerical draft/copied core"))
save(R/"DRAFT-SYNTAX.json",syntax)
inputs=json.loads((R/"INPUTS.json").read_text())
checks=[]
for x in inputs:
    p=Path(x["local"]);a=pin(p)
    checks.append(dict(kind="input_copy",path=str(p),passed=a["sha256"]==x["sha256"] and a["bytes"]==x["bytes"]))
    orig=Path(x["path"]);a=pin(orig)
    checks.append(dict(kind="original_pinned_artifact_unchanged",path=str(orig),passed=a["sha256"]==x["sha256"] and a["bytes"]==x["bytes"],
        expected_sha256=x["sha256"],observed_sha256=a["sha256"],
        expected_bytes=x["bytes"],observed_bytes=a["bytes"]))
target=json.loads((R/"TARGETS.json").read_text())
checks += [
    dict(kind="target_row_count",actual=len(target["rows"]),expected=288,passed=len(target["rows"])==288),
    dict(kind="target_check_count",actual=len(target["checks"]),expected=592,passed=len(target["checks"])==592),
    dict(kind="target_checks_pass",passed=all(x["passed"] for x in target["checks"])),
    dict(kind="no_comparison_result_claimed",passed=not (R/"FRAME-COMPARE.json").exists()),
    dict(kind="no_extra_execution",passed=sorted(x.name for x in (R/"execution").iterdir())==["compare-01","targets-01"]),
]
result=json.loads((R/"RESULTS.json").read_text())
checks.append(dict(kind="partial_status_explicit",passed=result["work_complete"] is False and result["status"]=="PARTIAL_HELD_RESOURCE_ADMISSION"))
drift=[x for x in checks if x["kind"]=="original_pinned_artifact_unchanged" and not x["passed"]]
critical=[x for x in checks if x["kind"]!="original_pinned_artifact_unchanged"]
assert all(x["passed"] for x in critical),[x for x in critical if not x["passed"]]
save(R/"INPUT-CHECK.json",dict(checks=checks,all_passed=all(x["passed"] for x in checks),
    frozen_copies_and_completed_results_passed=True,live_original_drift=drift,
    interpretation="Pinned intake copies remain authoritative for this report; original source changes are disclosed, not overwritten."))
time=json.loads((R/"TIMING.json").read_text())
time.update(ended_at=datetime.now(timezone.utc).isoformat(),status="partial; held after host admission refusal",timing_is="measured clocks, not work limits")
save(R/"TIMING.json",time)
with tarfile.open(R/"CODE.tar.gz","w:gz") as archive:
    for p in sorted(R.glob("*.py")):archive.add(p,arcname=p.name)
manifest=[]
for p in sorted(R.rglob("*")):
    if p.is_file() and p.name not in ["MANIFEST-051.json","PACKAGE-CHECK.json"]:
        manifest.append(dict(relative=str(p.relative_to(R)),**pin(p)))
save(R/"MANIFEST-051.json",dict(unit="vacuum-mainline051-p3-frame-targets-1020",
    status="PARTIAL_HELD_RESOURCE_ADMISSION",files=manifest))
integrity=[]
for row in manifest:
    a=pin(Path(row["path"]))
    integrity.append(dict(path=row["relative"],passed=a["sha256"]==row["sha256"] and a["bytes"]==row["bytes"]))
assert all(x["passed"] for x in integrity)
save(R/"PACKAGE-CHECK.json",dict(file_count=len(manifest),all_passed=True,
    checks=integrity,input_checks=len(checks),completed_target_arithmetic_checks=592,
    live_original_drift_count=len(drift),unexecuted_drafts_not_numerically_validated=True))
print(json.dumps(dict(inputs=len(inputs),input_checks=len(checks),package_files=len(manifest),package_integrity_passed=True,live_original_drift=drift)))
