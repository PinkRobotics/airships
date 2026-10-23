"""Verify and package the completed card; stage one atomic queue report."""
from pathlib import Path
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
import ast
import hashlib
import json
import shutil
import tarfile

ROOT=Path(__file__).resolve().parent
OLD=ROOT.with_name("vacuum-mainline051-p3-frame-targets-1020")
OUTBOX=ROOT.parents[2]/"outbox"
REPORT="rpt-ref-17635c55001d23054259"
def read(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,allow_nan=False)+"\n")
def pin(p):return dict(path=str(p.resolve()),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
def matches(p,x):
    return p.is_file() and p.stat().st_size==x["bytes"] and hashlib.sha256(p.read_bytes()).hexdigest()==x["sha256"]

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

executions=[]
sources=[]
for origin in [OLD,ROOT]:
    for folder in sorted((origin/"execution").iterdir()):
        if not folder.is_dir():continue
        assert (folder/"END.json").exists(),f"unclosed job {folder}"
        start=read(folder/"START.json");end=read(folder/"END.json")
        cmd=start["command"]
        assert cmd[cmd.index("--cores")+1]=="1"
        assert cmd[cmd.index("--mem")+1]=="1G"
        assert not end["admitted"] or end["released"]
        for item in start["source_pins"]:
            ok=matches(Path(item["path"]),item)
            sources.append(dict(path=item["path"],passed=ok))
            assert ok
        executions.append(dict(origin=str(origin),**end,command=cmd,
            start_receipt=pin(folder/"START.json"),end_receipt=pin(folder/"END.json"),
            stderr=pin(folder/"stderr.txt")))
executions.sort(key=lambda x:x["started_utc"])
last={}
spacing=[]
for e in executions:
    key=json.dumps(e["command"])
    prev=last.get(key)
    if prev is not None and prev["returncode"]==75:
        seconds=(datetime.fromisoformat(e["started_utc"])-datetime.fromisoformat(prev["ended_utc"])).total_seconds()
        spacing.append(dict(previous=prev["label"],next=e["label"],origin=e["origin"],seconds=seconds,
                            at_least_60_seconds=seconds>=60))
    last[key]=e
deviations=[x for x in spacing if not x["at_least_60_seconds"]]
assert len(deviations)==1 and deviations[0]["next"]=="compare-03"
dump(ROOT/"EXECUTION.json",dict(records=executions,source_pin_checks=sources,retry_intervals=spacing,
    retry_interval_deviations=deviations,
    deviation_disposition="One inadvertent 29-second manual retry disclosed; later wrapper enforces >=60 seconds.",
    all_admitted_released=True,all_commands_one_core_one_GiB=True,live_jobs=0,
    refused=sum(x["returncode"]==75 for x in executions),
    completed_successfully=sum(x["returncode"]==0 for x in executions),
    retained_noncapacity_failures=[x["label"] for x in executions if x["returncode"] not in [0,75]]))
now=datetime.now(timezone.utc).isoformat()
dump(ROOT/"TIMING.json",dict(resume_started_at=read(ROOT/"TIMING-START.json")["resumed_at"],
    completed_utc=now,original_started_at=read(OLD/"TIMING.json"),
    task_time_limit=None,phase_time_limit=None))
result=read(ROOT/"RESULTS.json");result["completed_utc"]=now
result["execution"]=dict(records=len(executions),all_admitted_released=True,
    all_one_core_one_GiB=True,live_jobs=0,retry_interval_deviations=deviations)
dump(ROOT/"RESULTS.json",result)

with tarfile.open(ROOT/"CODE.tar.gz","w:gz") as archive:
    for p in sorted(ROOT.glob("*.py")):archive.add(p,arcname=p.name)
    for name in ["METHOD.md","INPUTS.json","EXECUTION.json"]:
        archive.add(ROOT/name,arcname=name)
manifest=[]
for p in sorted(ROOT.rglob("*")):
    if p.is_file() and p.name not in ["MANIFEST-051-COMPLETE.json","PACKAGE-CHECK.json"]:
        manifest.append(dict(relative=str(p.relative_to(ROOT)),**pin(p)))
dump(ROOT/"MANIFEST-051-COMPLETE.json",dict(unit="vacuum-mainline051-p3-frame-targets-1020",
    status="COMPLETE",files=manifest))
verified=[dict(relative=x["relative"],passed=matches(ROOT/x["relative"],x)) for x in manifest]
assert all(x["passed"] for x in verified)
assert len(read(ROOT/"DAMAGE.json")["rows"])==72
assert all(x["conditional_second_failure_trigger"] for x in read(ROOT/"DAMAGE.json")["rows"])
assert all(x["FE"]["conditional_SF_or_ceiling"]>=1 for x in read(ROOT/"WITNESSES.json")["rows"])
dump(ROOT/"PACKAGE-CHECK.json",dict(manifest_files=len(manifest),all_manifest_pins_match=True,
    passed_input_and_prior_checks=len(checks),source_snapshot_checks=len(sources),
    all_admitted_jobs_released=True,live_jobs=0,
    FE_checks=read(ROOT/"FE-CHECKS.json")["passed"],FE_failures=read(ROOT/"FE-CHECKS.json")["failed"],
    target_checks=len(read(ROOT/"TARGETS.json")["checks"]),
    hail_checks=len(read(ROOT/"HAIL.json")["checks"]),
    witnesses=36,damaged_same_budget_cases=72,
    visual_review="Target surface reviewed in partial turn; material chart reviewed and missing-Al-row axis alignment corrected.",
    verified_files=verified))
body="""MAINLINE-051 COMPLETE. QUESTIONABLE / PROJECTION. Resume finished; prior partial and all its pins preserved.

Delivered m5–40 target surfaces, 18 material/layup models, frame masses and SFs, explicit q≥1 mechanical witnesses, numerical strength/m gaps, 980 hail scenarios and 72 same-budget member-loss cases. 182 FE solves; 592 target, six regression, 145 hail and 560 FE/mesh checks pass.

At 5% reserve, Hexoloy's same-mass mechanical SF is 1.05399. Required whole-member compression scale at m10/Pf1e-3 is 3.72734 GPa; assuming 3.9 GPa gives Pf0.00063595. This is hypothetical, not a measured distribution. At the original higher 041 screens, scale improvements remain 1.09710×/1.07925×.

K13D2U 50/20/20/10 has same-mass mechanical ceilings 1.13574/1.07598 and required scales 2.16141/2.24573 GPa; compression data are absent. Its 5% q≥1 witness totals 4282 kg including reserve/sag, versus 5249 kg for M55J's best modeled layup and 21179 kg for aluminium.

The transferred SiC hail estimates are 1.153–5.393% at the 5% section; actual break probabilities remain unidentified. All sampled member losses trigger secondary overload; dynamic cascade is not proven. Joints and film need redesign as well as tubes.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]