#!/usr/bin/env python3
"""Add findings to the preserved 030b register using its source-identity scheme."""
import copy
from pathlib import Path
from intake import B, load, save

KEYS = ("rows", "findings", "open", "issues", "items",
        "prior_032_findings_retained", "new_findings", "resolved_source_findings",
        "resolved_for_this_card_only", "inherited_037b")
old = load(B / "NEW-NFI.json") if (B / "NEW-NFI.json").exists() else []
uids = {(r["report"], r["file"], r["source_json_pointer"]): r["uid"] for r in old}
next_uid = max([int(r["uid"][1:]) for r in old] + [0]) + 1
fresh, documents = [], []
for report in load(B / "INTAKE.json")["reports"]:
    for a in report["artifacts"]:
        if "nfi" not in Path(a["path"]).name.lower() or not a.get("snapshot"):
            continue
        d = load(Path(a["snapshot"]))
        collections = [("", d)] if isinstance(d, list) else [
            (k, d[k]) for k in KEYS if isinstance(d.get(k), list)]
        assert collections, a["path"]
        documents.append({"report": report["id"], "file": a["path"],
                          "snapshot": a["snapshot"], "sha256": a["sha256"],
                          "collections": [k for k, _ in collections], "document": d})
        for key, values in collections:
            for i, fields in enumerate(values):
                pointer = f"/{key}/{i}" if key else f"/{i}"
                identity = (report["id"], a["path"], pointer)
                uid = uids.get(identity)
                if uid is None:
                    uid = f"C{next_uid:03d}"
                    next_uid += 1
                rowid = next((str(fields[k]) for k in ("id", "nfi_id", "row_id")
                              if isinstance(fields, dict) and k in fields), pointer)
                fresh.append({
                    "uid": uid, "report": report["id"], "file": a["path"],
                    "snapshot": a["snapshot"], "source_sha256": a["sha256"],
                    "source_json_pointer": pointer, "row_id": rowid,
                    "fields": copy.deepcopy(fields),
                    "inherited_document_tag": {k: v for k, v in d.items()
                        if k in ("tag", "classification", "status")} if isinstance(d, dict) else {},
                    "register_classification": "QUESTIONABLE / PROJECTION",
                    "finding_collection": key or "root_list",
                    "blocks_progress": False,
                })
save(B / "NEW-NFI.json", fresh)
save(B / "NEW-NFI-SOURCES.json", documents)
print("NEW FINDINGS", len(fresh), "DOCUMENTS", len(documents))
for r in fresh:
    f = r["fields"]
    summary = " | ".join(str(f[k]) for k in
        ("title", "issue", "finding", "unknown", "note", "description", "question")
        if isinstance(f, dict) and k in f) or str(f)
    print(r["uid"], r["row_id"], summary[:260])
