#!/usr/bin/env python3
"""Freeze a manifest after numerical review; never submits a report."""
import hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()
def main():
    checks=json.loads((ROOT/"EVIDENCE-CHECKS.json").read_text())
    run=json.loads((ROOT/"RUN.json").read_text())
    assert checks["failed"]==0 and run.get("ended_at")
    target=ROOT/"ARTIFACT-MANIFEST.json"
    assert not target.exists(),"Never overwrite a filed/frozen manifest"
    rows=[]
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts or p==target:continue
        rows.append(dict(path=str(p),relative_path=str(p.relative_to(ROOT)),
                         sha256=digest(p),bytes=p.stat().st_size))
    target.write_text(json.dumps(dict(schema=1,unit=run["unit"],artifacts=rows,
        file_count=len(rows),total_bytes=sum(x["bytes"] for x in rows),
        note="Manifest excludes itself and Python bytecode caches. Source inputs, native runs, failed controls and admission-refusal evidence are retained."),indent=2)+"\n")
    print(json.dumps(dict(manifest=str(target),file_count=len(rows),
                         total_bytes=sum(x["bytes"] for x in rows))))
if __name__=="__main__":main()
