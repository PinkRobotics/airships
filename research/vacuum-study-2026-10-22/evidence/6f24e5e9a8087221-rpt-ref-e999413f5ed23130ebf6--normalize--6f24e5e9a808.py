#!/usr/bin/env python3
"""Extend 030c's attributed NFI normalization, including nested inherited records."""
import copy
from pathlib import Path
from intake import B, load, save

def pointer_part(key):
    return str(key).replace("~","~0").replace("/","~1")

def collections(value, pointer=""):
    if isinstance(value,list):
        # A finding is a complete row. Its evidence arrays are not separately
        # counted as findings; inherited document wrappers are traversed.
        findings=bool(value) and all(isinstance(x,dict) for x in value) and any(
            any(k in x for k in ("id","nfi_id","row_id","finding","claim","issue","open_issue"))
            for x in value)
        if findings:
            yield pointer,value
        else:
            for i,x in enumerate(value):
                if isinstance(x,(dict,list)):
                    yield from collections(x,f"{pointer}/{i}")
    elif isinstance(value,dict):
        for k,x in value.items():
            if isinstance(x,(dict,list)):
                yield from collections(x,pointer+"/"+pointer_part(k))

old=load(B/"NEW-NFI.json") if (B/"NEW-NFI.json").exists() else []
uids={(r["report"],r["file"],r["source_json_pointer"]):r["uid"] for r in old}
next_uid=max([int(r["uid"][1:]) for r in old]+[0])+1
fresh=[];documents=[]
for report in load(B/"INTAKE.json")["reports"]:
    for a in report["artifacts"]:
        if "nfi" not in Path(a["path"]).name.lower() or not a.get("snapshot"):
            continue
        d=load(Path(a["snapshot"]))
        groups=list(collections(d))
        assert groups,a["path"]
        documents.append(dict(report=report["id"],file=a["path"],snapshot=a["snapshot"],
                              sha256=a["sha256"],collections=[k for k,_ in groups],document=d))
        for key,values in groups:
            for i,fields in enumerate(values):
                pointer=f"{key}/{i}"
                identity=(report["id"],a["path"],pointer)
                uid=uids.get(identity)
                if uid is None:
                    uid=f"D{next_uid:03d}";next_uid+=1
                rowid=next((str(fields[k]) for k in ("id","nfi_id","row_id") if k in fields),pointer)
                fresh.append(dict(
                    uid=uid,report=report["id"],file=a["path"],snapshot=a["snapshot"],
                    source_sha256=a["sha256"],source_json_pointer=pointer,row_id=rowid,
                    fields=copy.deepcopy(fields),
                    inherited_document_tag={k:d[k] for k in ("tag","classification","status")
                                            if isinstance(d,dict) and k in d},
                    register_classification="QUESTIONABLE / PROJECTION",
                    finding_collection=key or "root_list",blocks_progress=False))
save(B/"NEW-NFI.json",fresh)
save(B/"NEW-NFI-SOURCES.json",documents)
print("NEW FINDINGS",len(fresh),"DOCUMENTS",len(documents))
for r in fresh:
    f=r["fields"]
    summary=" | ".join(str(f[k]) for k in
        ("title","topic","issue","finding","claim","open_issue","unknown","note","description","question")
        if k in f) or str(f)
    print(r["uid"],r["row_id"],summary[:300])
