#!/usr/bin/env python3
"""Verify the complete addendum and pin its final files."""
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

B=Path(__file__).resolve().parent
def load(name):
    return json.loads((B/name).read_text(),parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def dump(name,value):
    (B/name).write_text(json.dumps(value,indent=2,allow_nan=False)+"\n")
def pin(path):
    raw=path.read_bytes()
    return dict(path=str(path.resolve()),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw))

assert load("VALIDATION.json")["passed"]
r=load("RESULTS.json")
assert r["complete"] and r["new_configurations"]==len(r["rows"])==648
assert len(r["paired_cure_rows"])==216
assert sum(x["external_water_kg_m2"]==1 for x in r["rows"])==432
assert r["best_one_mm_all_four"]["payload_kg"]<0
assert r["best_one_mm_favorable_upper"]["payload_upper_kg"]<0
assert len(load("RETENTION-BEFORE-AFTER.json"))==648
with (B/"ROWS.csv").open() as f:
    assert len(list(csv.DictReader(f)))==648
verified=[]
for p in load("INPUT-PINS.json"):
    actual=pin(B/p["snapshot"])
    assert actual["sha256"]==p["sha256"] and actual["bytes"]==p["bytes"],p
    verified.append(actual)
for p in load("ORIGINAL-048-PINS.json"):
    actual=pin(Path(p["path"]))
    assert actual["sha256"]==p["sha256"] and actual["bytes"]==p["bytes"],p
    verified.append(actual)
original=Path(load("INPUTS.json")["original_048_directory"])
for p in json.loads((original/"MODEL-PINS.json").read_text()):
    actual=pin(Path(p["path"]))
    assert actual["sha256"]==p["sha256"] and actual["bytes"]==p["bytes"],p
    verified.append(actual)
for path in B.rglob("*.json"):
    if path.name not in ["MANIFEST.json","PACKAGE-VALIDATION.json"]:
        json.loads(path.read_text(),parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
for name in ["CARD.md","RESULTS.json","ROWS.csv","INPUTS.json","NFI.json",
             "METHOD.md","WATER-AND-BOND-SOURCES.md","THERMAL-BOUNDARY.md",
             "CHECK040-REPRODUCTION.json","SEARCH-VALIDATION.json","fold_model.py"]:
    assert (B/name).stat().st_size>0,name
dump("PACKAGE-VALIDATION.json",dict(
    passed=True,verified_pin_records=len(verified),verified=verified,
    new_configurations=648,heavy_water_configurations=432,
    at=datetime.now(timezone.utc).isoformat(),
    notes=["Original filed 048 and 040 artifacts remain byte-identical.",
           "CHECK-040 executable files were not accessed.",
           "No original dry-exterior row is relabeled as a wet-service qualification.",
           "Installed-hull safety factor remains unknown."]))
paths=[p for p in sorted(B.rglob("*")) if p.is_file()
       and p.name!="MANIFEST.json" and not p.name.endswith(".tmp")
       and "__pycache__" not in p.parts]
dump("MANIFEST.json",dict(
    unit="vacuum-mainline048-coating-and-water-1020",
    finished_at=datetime.now(timezone.utc).isoformat(),
    artifact_count=len(paths),artifacts=[pin(p) for p in paths]))
print("Package passed;",len(verified),"verified pins;",len(paths),"artifacts.")
