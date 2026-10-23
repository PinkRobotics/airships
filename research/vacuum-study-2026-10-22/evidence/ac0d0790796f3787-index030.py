#!/usr/bin/env python3
"""MAINLINE-030 index: every filed vacuum-mainline card and check, and every NFI row they pinned, verbatim.

Reads only named files: the queue submissions whose ids are listed (one directory listing, no walk), and the artifact
paths those submissions name. Writes INDEX.json and NFI-RAW.json into the 030 output folder.
"""
import hashlib
import json
import re
from pathlib import Path

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def main():
    ids = sorted({p.name[:-5] for p in SUB.iterdir() if p.name.startswith("rpt-") and p.name.endswith(".json")})
    ids = [i for i in ids if KEEP.search(i) and not DROP.search(i) and re.search(r"10(19|20)$", i)]
    index, nfi_rows = [], []
    for rid in ids:
        r = json.loads((SUB / f"{rid}.json").read_text())
        arts = r.get("artifacts") or []
        entry = {"id": rid, "at": r.get("at"), "from_seat": r.get("from_seat"), "unit": r.get("unit"), "re": r.get("re"),
                 "body": r.get("body"), "artifacts": [], "nfi_rows": 0}
        for a in arts:
            p = Path(a["path"])
            ok = None
            try:
                b = p.read_bytes()
                ok = hashlib.sha256(b).hexdigest() == a.get("sha256")
            except OSError:
                b = None
            entry["artifacts"].append({"path": str(p), "sha256": a.get("sha256"), "bytes": a.get("bytes"), "match": ok})
            if p.name.upper().startswith("NFI") and p.suffix == ".json" and b is not None:
                try:
                    d = json.loads(b)
                except ValueError:
                    continue
                rows = d.get("rows") if isinstance(d, dict) else d
                if isinstance(d, dict) and rows is None:
                    rows = d.get("nfi") or d.get("items") or d.get("NFI") or []
                for row in rows or []:
                    if not isinstance(row, dict):
                        continue
                    nfi_rows.append({"report": rid, "file": str(p), "row": row})
                    entry["nfi_rows"] += 1
        index.append(entry)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "INDEX.json").write_text(json.dumps(index, indent=1))
    (OUT / "NFI-RAW.json").write_text(json.dumps(nfi_rows, indent=1))
    print(len(index), "reports;", len(nfi_rows), "NFI rows;",
          sum(1 for e in index for a in e["artifacts"] if a["match"] is False), "changed artifacts;",
          sum(1 for e in index for a in e["artifacts"] if a["match"] is None), "unreadable artifacts")
    for e in index:
        print(f"{e['at'] or '':25s} {e['id']:75s} nfi={e['nfi_rows']:3d} arts={len(e['artifacts'])}")


if __name__ == "__main__":
    main()
