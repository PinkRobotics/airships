#!/usr/bin/env python3
"""MAINLINE-030: join the sub-workers' topic rows back onto the verbatim NFI rows and print a compact per-topic view.

Inputs (030 output folder): NFI-NORM.json (checker's script), TOPIC-CHUNK-1..3.json (sub-workers, completeness-checked
here). Output: TOPICS-JOINED.json, and a compact listing on stdout for the checker's own merge decisions.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "outputs" / "vacuum-mainline030-design-register-1020"
NAMES = {"T01": "case and atmosphere", "T02": "shell knockdown kd", "T03": "crimp-branch gamma", "T04": "wrinkling and core Ec",
         "T05": "face properties", "T06": "face sheet and panels", "T07": "cores", "T08": "P2 joints, seams, film",
         "T09": "margin items", "T10": "vacuum holding", "T11": "thermal", "T12": "handling, cost, supply",
         "T13": "P3 member force", "T14": "P3 local buckling", "T15": "P3 global lattice", "T16": "P3 Perry",
         "T17": "P3 tube material", "T18": "P3 nodes and joints", "T19": "P3 film", "T20": "tolerance maps",
         "T21": "geometry levers", "T22": "metal strength transfer", "T23": "PROJECTION materials", "T24": "method",
         "T25": "other"}


def main():
    norm = json.loads((OUT / "NFI-NORM.json").read_text())
    by_uid = {n["uid"]: n for n in norm}
    topics = []
    for k in (1, 2, 3):
        topics += json.loads((OUT / f"TOPIC-CHUNK-{k}.json").read_text())
    seen = [t["uid"] for t in topics]
    missing = sorted(set(by_uid) - set(seen))
    dup = sorted({u for u in seen if seen.count(u) > 1})
    bad = [t["uid"] for t in topics if t.get("topic") not in NAMES]
    print("rows", len(norm), "topic rows", len(topics), "missing", missing, "duplicates", dup, "bad topics", bad)
    if missing or dup or bad:
        sys.exit(1)
    joined = []
    for t in topics:
        n = by_uid[t["uid"]]
        joined.append({**t, "report": n["report"], "card": n["card"], "file": n["file"], "row_id": n["row_id"]})
    (OUT / "TOPICS-JOINED.json").write_text(json.dumps(joined, indent=1))
    groups = defaultdict(list)
    for j in joined:
        groups[j["topic"]].append(j)
    for code in sorted(groups):
        print(f"\n## {code} {NAMES[code]} ({len(groups[code])})")
        for j in sorted(groups[code], key=lambda x: x["key"].lower()):
            print(f"{j['uid']} | {j['card']} | {j['row_id']} | {j['key']} | {j['unknown']} | today={j['today']} | "
                  f"need={j['needed']} | {j['state']} | {j['direction']} | owner={j['owner']}")


if __name__ == "__main__":
    main()
