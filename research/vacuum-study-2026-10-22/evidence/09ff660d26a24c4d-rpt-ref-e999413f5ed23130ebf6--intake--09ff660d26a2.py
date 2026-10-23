#!/usr/bin/env python3
"""030d extension of 030c's immutable intake and source-preserving workflow."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def load(p):
    return json.loads(p.read_text())


def save(p, value):
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n")


def pin(p):
    h = hashlib.sha256()
    n = 0
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
            n += len(block)
    return {"path": str(p), "sha256": h.hexdigest(), "bytes": n}


def check(a):
    actual = pin(Path(a["path"]))
    assert actual["sha256"] == a["sha256"] and actual["bytes"] == a["bytes"], (a, actual)
    return {**a, "matches": True}


def bootstrap():
    marker = B / "BASELINE-PINS.json"
    if marker.exists():
        return
    report = load(Q / f"{PREDECESSOR}.json")
    pins = [check(a) for a in report["artifacts"]]
    src = Path(report["artifacts"][0]["path"]).parent
    dest = B / "baseline030c"
    dest.mkdir()
    (dest / "report.json").write_bytes((Q / f"{PREDECESSOR}.json").read_bytes())
    for a in load(src / "MANIFEST.json")["artifacts"]:
        item = check(a)
        p = Path(a["path"])
        target = dest / p.relative_to(src)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(p.read_bytes())
        item["snapshot"] = str(target)
        pins.append(item)
    (dest / "MANIFEST.json").write_bytes((src / "MANIFEST.json").read_bytes())
    save(marker, {"predecessor": PREDECESSOR, "original_root": str(src),
                  "snapshot_root": str(dest), "pins": pins})
    order = load(Q / f"{ORDER}.json")
    briefdir = B / "brief"
    briefdir.mkdir()
    (briefdir / "order.json").write_bytes((Q / f"{ORDER}.json").read_bytes())
    briefpins = []
    for a in order["artifacts"]:
        item = check(a)
        target = briefdir / Path(a["path"]).name
        target.write_bytes(Path(a["path"]).read_bytes())
        item["snapshot"] = str(target)
        briefpins.append(item)
    save(B / "BRIEF-PINS.json", briefpins)


def refresh():
    assert not (B / "SNAPSHOT-FROZEN.json").exists(), "Final source snapshot is frozen; later filings belong to the next register."
    base = load(B / "baseline030c/SOURCE-INDEX.json")
    known = {PREDECESSOR}
    for group in ("baseline", "additions", "additions_030c"):
        known.update(x["id"] for x in base[group])
    previous = load(B / "INTAKE.json") if (B / "INTAKE.json").exists() else {"reports": []}
    old = {x["id"]: x for x in previous["reports"]}
    names = subprocess.check_output([
        "rg", "--files", str(Q), "-g", "rpt-*mainline*.json",
        "-g", "rpt-*check0*-1020.json"], text=True).splitlines()
    reports, exclusions = [], []
    for name in names:
        p = Path(name)
        r = load(p)
        if r.get("kind") != "report" or r["id"] in known:
            continue
        at = datetime.fromisoformat(r.get("ingested", r["at"]).replace("Z", "+00:00"))
        if at < CUTOFF:
            continue
        if "mainline" not in ((r.get("unit") or "") + (r.get("body") or "")).lower():
            exclusions.append({"id": r["id"], "reason": "not mainline"})
            continue
        if r["id"].startswith("rpt-lead-sciences-mainline030d-"):
            continue
        reports.append((at, p, r))
    reports.sort(key=lambda x: (x[0], x[2]["id"]))
    rows = []
    for at, p, r in reports:
        rid = r["id"]
        if rid in old:
            assert pin(p)["sha256"] == old[rid]["report_sha256"], rid
            rows.append(old[rid])
            continue
        folder = B / "snapshots" / rid
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / "report.json"
        target.write_bytes(p.read_bytes())
        pp = pin(p)
        row = {"id": rid, "at": r["at"], "ingested": r.get("ingested"),
               "unit": r.get("unit"), "body": r.get("body"),
               "report_path": str(p), "report_snapshot": str(target),
               "report_sha256": pp["sha256"], "report_bytes": pp["bytes"],
               "artifacts": [], "pin_failures": []}
        for i, a in enumerate(r.get("artifacts", [])):
            item = check(a)
            source = Path(a["path"])
            if source.suffix.lower() in (".md", ".json", ".csv", ".txt") and a["bytes"] < 256_000_000:
                target = folder / source.name
                if target.exists():
                    target = folder / f"{i:02d}-{source.name}"
                target.write_bytes(source.read_bytes())
                item["snapshot"] = str(target)
            row["artifacts"].append(item)
        rows.append(row)
        print("ADDED", rid, "artifacts", len(row["artifacts"]))
    result = {"schema": 1, "sampled_at": datetime.now(timezone.utc).isoformat(),
              "since": CUTOFF.isoformat(), "predecessor": PREDECESSOR,
              "discovery": "canonical queue report files; mainline/check filename patterns; ingested timestamps; baseline source IDs excluded",
              "reports": rows, "exclusions": exclusions, "pin_failures": 0}
    save(B / "INTAKE.json", result)
    print("REPORTS", len(rows), "ARTIFACTS", sum(len(r["artifacts"]) for r in rows),
          "AT", result["sampled_at"])


if __name__ == "__main__":
    bootstrap()
    refresh()
