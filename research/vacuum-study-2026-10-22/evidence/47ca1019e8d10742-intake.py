#!/usr/bin/env python3
"""Snapshot relevant filed reports and pin their reviewable artifacts."""
import hashlib
import json
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

B = Path(__file__).resolve().parent
Q = Path("unpublished-local-ref:ab52dba26d6cc3a7")
BASE = "rpt-mainline030-opus-register-1020"
baseline = json.loads((B/"snapshots/baseline030/INDEX.json").read_text())
known = {r["id"] for r in baseline}
cutoff = datetime.fromisoformat("2026-10-20T01:15:00-07:00")
paths = subprocess.check_output([
    "rg","--files",str(Q),"-g","rpt-*mainline*.json","-g","rpt-*check0*-1020.json"
],text=True).splitlines()
reports = []
for name in paths:
    p = Path(name)
    r = json.loads(p.read_text())
    if r.get("kind") != "report" or r.get("id") == BASE:
        continue
    at = datetime.fromisoformat(r["at"].replace("Z","+00:00"))
    if at < cutoff and r["id"] in known:
        continue
    # Do not pull unrelated older programme reports into this night's register.
    if at < datetime.fromisoformat("2026-10-19T18:00:00-07:00"):
        continue
    if not ("mainline" in r.get("unit","").lower()
            or "mainline" in r.get("body","").lower()):
        continue
    reports.append((at, p, r))
reports.sort(key=lambda x:(x[0],x[2]["id"]))
old = json.loads((B/"INTAKE.json").read_text()) if (B/"INTAKE.json").exists() else {"reports":[]}
old_by_id = {r["id"]:r for r in old["reports"]}
rows = []
for at, path, report in reports:
    rid = report["id"]
    if rid in old_by_id:
        rows.append(old_by_id[rid])
        continue
    folder = B/"snapshots"/rid
    folder.mkdir(exist_ok=True)
    data = path.read_bytes()
    (folder/"report.json").write_bytes(data)
    row = dict(id=rid, at=report["at"], report_snapshot=str(folder/"report.json"),
               report_sha256=hashlib.sha256(data).hexdigest(),
               report_bytes=len(data), baseline_index_included=rid in known,
               unit=report.get("unit"), body=report.get("body"),
               artifacts=[], pin_failures=[])
    for i, art in enumerate(report.get("artifacts",[])):
        source = Path(art["path"])
        try:
            digest = hashlib.sha256()
            size = 0
            with source.open("rb") as handle:
                for chunk in iter(lambda:handle.read(1024*1024), b""):
                    digest.update(chunk)
                    size += len(chunk)
            item = dict(**art, observed_sha256=digest.hexdigest(),
                        observed_bytes=size, matches=digest.hexdigest()==art.get("sha256")
                        and size==art.get("bytes"))
            # Readable record snapshots. Code, binary output and raw solver
            # files remain pinned at source, without importing or executing.
            if source.suffix.lower() in [".md",".json",".csv"] and size < 16_000_000:
                target = folder/source.name
                if target.exists():
                    target = folder/f"{i:02d}-{source.name}"
                target.write_bytes(source.read_bytes())
                item["snapshot"] = str(target)
            if not item["matches"]:
                row["pin_failures"].append(item)
            row["artifacts"].append(item)
        except OSError as exc:
            item = dict(**art, matches=False, error=str(exc))
            row["artifacts"].append(item)
            row["pin_failures"].append(item)
    rows.append(row)
result = dict(schema=1, sampled_at=datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds"),
              discovery="Named queue submission directory, rpt-*mainline*.json and rpt-*check0*-1020.json; aware timestamps; additions beyond baseline INDEX retained.",
              baseline_reports=len(known), reports=rows,
              pin_failures=sum(len(x["pin_failures"]) for x in rows))
(B/"INTAKE.json").write_text(json.dumps(result,indent=2)+"\n")
for row in rows:
    if row["id"] not in old_by_id:
        print(json.dumps(dict(id=row["id"],at=row["at"],baseline=row["baseline_index_included"],
                              body=row["body"],files=[Path(x.get("snapshot",x["path"])).name for x in row["artifacts"]],
                              pin_failures=row["pin_failures"]),indent=2))
print("REPORTS",len(rows),"PIN_FAILURES",result["pin_failures"],"AT",result["sampled_at"])
