#!/usr/bin/env python3
"""Preserve every source issue verbatim and expose stable register references."""
import copy
import hashlib
import json
from pathlib import Path

B=Path(__file__).resolve().parent
intake=json.loads((B/"INTAKE.json").read_text())
baseline=json.loads((B/"snapshots/baseline030/NFI-NORM.json").read_text())
previous=json.loads((B/"NFI-NORM.json").read_text()) if (B/"NFI-NORM.json").exists() else baseline
existing={(r["report"],r["file"],r["row_id"]):r["uid"] for r in previous}
next_uid=max(int(r["uid"][1:]) for r in previous)+1
rows=copy.deepcopy(baseline)
sources=[]
extra=[]
def add(report,path,source_path,pinned_hash):
    global next_uid
    document=json.loads(path.read_text())
    if isinstance(document,list):
        collections=[("$",document)]
    else:
        keys=[k for k in ["rows","findings","open","issues","items",
                         "prior_032_findings_retained","new_findings"] if isinstance(document.get(k),list)]
        assert keys,(path,keys)
        collections=[(key,document[key]) for key in keys]
    sources.append(dict(report=report,file=source_path,snapshot=str(path),
                        sha256=pinned_hash,count=sum(len(v) for _,v in collections),
                        collection=[k for k,_ in collections],
                        document=document))
    for key,i,field in [(key,i,field) for key,collection in collections
                        for i,field in enumerate(collection)]:
        rowid=field.get("id",field.get("nfi_id",field.get("row_id"))) if isinstance(field,dict) else None
        if not rowid:
            rowid=f"{key}[{i}]"
        identity=(report,source_path,str(rowid))
        uid=existing.get(identity)
        if uid is None:
            uid=f"N{next_uid:03d}"
            next_uid+=1
        item=dict(uid=uid,report=report,
                  card=document.get("card",report) if isinstance(document,dict) else report,
                  file=source_path,snapshot=str(path),source_sha256=pinned_hash,
                  source_json_pointer=f"/{key}/{i}" if key!="$" else f"/{i}",
                  row_id=str(rowid),fields=copy.deepcopy(field),
                  inherited_document_tag={k:v for k,v in document.items()
                                          if k in ["tag","classification","status","overall_installed_hull_SF"]}
                                         if isinstance(document,dict) else {})
        rows.append(item);extra.append(item)

old_path=B/"snapshots/baseline030/NFI.json"
basepin=next(x for x in json.loads((B/"BASELINE-PINS.json").read_text()) if Path(x["path"]).name=="NFI.json")
add("rpt-mainline030-opus-register-1020",old_path,basepin["path"],basepin["sha256"])
for report in intake["reports"]:
    if report["at"].startswith("2026-10-19"):
        continue
    for art in report["artifacts"]:
        if "nfi" in Path(art["path"]).name.lower() and art.get("snapshot"):
            assert art["matches"],art
            add(report["id"],Path(art["snapshot"]),art["path"],art["sha256"])
keys=[(r["report"],r["file"],r["row_id"]) for r in rows]
assert len(keys)==len(set(keys)), "Duplicate source identities"
(B/"NFI-NORM.json").write_text(json.dumps(rows,indent=2)+"\n")
(B/"NEW-NFI-SOURCES.json").write_text(json.dumps(sources,indent=2)+"\n")
(B/"NEW-NFI.json").write_text(json.dumps(extra,indent=2)+"\n")
for r in extra:
    f=r["fields"]
    summary=(str(f) if not isinstance(f,dict) else " | ".join(
        str(f[k]) for k in ["title","topic","issue","finding","unknown","question","note","description","need","action","objection","correction"]
        if k in f))
    if not summary:
        summary=json.dumps(f)
    print(r["uid"],r["row_id"],summary[:430])
print("BASE",len(baseline),"ADDED",len(extra),"TOTAL",len(rows),"SOURCE_FILES",len(sources))
