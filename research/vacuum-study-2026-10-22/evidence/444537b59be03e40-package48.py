#!/usr/bin/env python3
"""Strict artifact/input integrity check, then pin the final source state."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

B=Path(__file__).resolve().parent
def pin(path):
    raw=path.read_bytes()
    return dict(path=str(path.resolve()),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))
def load(name): return json.loads((B/name).read_text())
def dump(name,value):
    (B/name).write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")

assert load("VALIDATION.json")["passed"]
assert load("ADDITIONAL-AUDIT.json")["passed"]
assert load("RESULTS.json")["complete"] and len(load("RESULTS.json")["rows"])==432
assert load("SENSITIVITIES.json")["complete"]
checks=[]
for name in ["MODEL-PINS.json","UPSTREAM-PINS.json","BRIEF-PINS.json"]:
    for p in load(name):
        path=Path(p["path"]);actual=pin(path)
        assert actual["sha256"]==p["sha256"] and actual["bytes"]==p["bytes"],str(path)
        checks.append(dict(type="original input",**actual))
        if "snapshot" in p:
            snap=pin(B/p["snapshot"])
            assert snap["sha256"]==p["sha256"] and snap["bytes"]==p["bytes"],p["snapshot"]
            checks.append(dict(type="local input snapshot",**snap))
        elif name=="BRIEF-PINS.json":
            snap=pin(B/"snapshots"/path.name)
            assert snap["sha256"]==p["sha256"] and snap["bytes"]==p["bytes"],path.name
            checks.append(dict(type="local brief snapshot",**snap))
for name in ["SOURCE-DOWNLOADS.json","SOURCE-DOWNLOADS-2.json","SOURCE-DOWNLOADS-3.json"]:
    for p in load(name):
        if p.get("ok") and "sha256" in p:
            actual=pin(B/"sources"/p["name"])
            assert actual["sha256"]==p["sha256"] and actual["bytes"]==p["bytes"],p["name"]
            checks.append(dict(type="downloaded primary source",**actual))
for path in sorted(B.rglob("*.json")):
    if path.name in ["MANIFEST.json","PACKAGE-VALIDATION.json"]: continue
    # parse_constant rejects NaN and Infinity extensions as well as output
    # writers' allow_nan=False checks; sources are checked without mutation.
    json.loads(path.read_text(),parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
for name in ["CARD.md","RESULTS.json","ROWS.csv","INPUTS.json","NFI.json",
             "METHOD.md","SOURCE-AUDIT.md","COATING-EVIDENCE.md","ACCOUNT.png","ACCOUNT.pdf"]:
    assert (B/name).stat().st_size>0,name
assert abs(load("R10-RECONCILIATION.json")["closure_error_kg"])<1e-6
dump("PACKAGE-VALIDATION.json",dict(
    passed=True,verified_pin_records=len(checks),checks=checks,
    at=datetime.now(timezone.utc).isoformat(),
    notes=["All writes are in this seat's .ship directory.",
           "Original filed 040 input artifacts remain byte-identical.",
           "Failed HTTP downloads are recorded as failures; selected web facts are separately identified.",
           "No computation changes or source edits occur after manifest creation."]))
paths=[p for p in sorted(B.rglob("*")) if p.is_file() and p.name!="MANIFEST.json"
       and not p.name.endswith(".tmp") and "__pycache__" not in p.parts]
dump("MANIFEST.json",dict(
    unit="vacuum-mainline048-coating-and-water-1020",
    finished_at=datetime.now(timezone.utc).isoformat(),
    artifact_count=len(paths),artifacts=[pin(p) for p in paths]))
print("Package validation passed;",len(checks),"verified pin records;",len(paths),"artifacts pinned.")
