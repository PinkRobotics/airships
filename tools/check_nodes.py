#!/usr/bin/env python3
"""The computed-node manifest must be present, closed, and match the article graph.

    python3 tools/check_nodes.py

tools/gen_nodes.py grows every joint from one SDF rule and writes STLs plus a manifest.
This gate does NOT regenerate (that is `make nodes`, ~minutes); it verifies the manifest
is self-consistent with the counting the analysis uses: 51 nodes (19 lattice + 24 rim
vertices + 8 hex centres), 96 pipes and 72 ties by member-end count, every mesh CLOSED.
A change to the lattice counting without regenerating the nodes fails here — the same
drift check_figures_fresh runs for figures, applied to geometry.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "research" / "geometry" / "nodes" / "manifest.json"


def main() -> None:
    if not MANIFEST.exists():
        sys.exit("check_nodes: no manifest — run `make nodes` first.")
    m = json.loads(MANIFEST.read_text())
    bad = []
    nodes = m["nodes"]
    if len(nodes) != 51:
        bad.append(f"{len(nodes)} nodes, expected 51")
    roles = {}
    for r in nodes:
        roles[r["role"]] = roles.get(r["role"], 0) + 1
        if not r["closed"]:
            bad.append(f"{r['file']}: mesh not closed")
        if not (MANIFEST.parent / r["file"]).exists():
            bad.append(f"{r['file']}: listed but missing on disk")
    want = {"lattice": 19, "rimVertex": 24, "hexHub": 8}
    if roles != want:
        bad.append(f"roles {roles}, expected {want}")
    arms = sum(r["arms"] for r in nodes)
    if arms != 2 * 216:
        bad.append(f"{arms} member-ends, expected 432 (216 members)")
    if m.get("graph") != {"octet": 60, "rim": 36, "spoke": 48, "tie": 72}:
        bad.append(f"graph {m.get('graph')} does not match the analysis counting")
    # Every boundary node must carry its flat lands. NOT because cells seat face to face on
    # them — they do not, and this comment used to say they did. 108 of the 216 members lie
    # exactly in a face plane and stand 5 mm proud of it (7 mm on the rim), so two finished
    # articles stop on the pipes long before the lands touch. check_assembly's P10 carries the
    # decision in full: an array is a continuous octet lattice partitioned by film, and at even
    # n this whole boundary apparatus does not exist. The lands are the print datum print_frame
    # lands on the bed and the plane the film bonds to, and a boundary node without them is a
    # part with nothing flat to print on.
    lands = {r["role"]: r["lands"] for r in nodes}
    want_lands = {"hexHub": 1, "rimVertex": 3}
    for role, n_l in want_lands.items():
        got = [r["lands"] for r in nodes if r["role"] == role]
        if any(g != n_l for g in got):
            bad.append(f"{role} nodes have lands {sorted(set(got))}, expected {n_l}")
    # SLOT CLEARANCE. A pipe seats in an annular slot; two arms at angle theta have their
    # slots intersect until the slot starts beyond Ro/sin(theta/2). Cut them anyway and the
    # print comes out with each slot bored through its neighbour — the pipe fouls on the
    # remains and never reaches its shoulder, and no render would ever show it. This is the
    # gate for an assembly-time failure, which is the only kind a picture cannot catch.
    for r in nodes:
        if not r.get("slotsClear"):
            bad.append(f"{r['file']}: pipe slots intersect inside the node "
                       f"(min arm angle {r.get('minArmAngleDeg')} deg, slot base "
                       f"{r.get('slotBaseMm')} mm) — the pipes could not be seated")
    if not m.get("totalNodeMassKg", 0) > 0:
        bad.append("totalNodeMassKg missing or zero")
    # The analysis note quotes the measured node mass; hold it to the manifest.
    md = (ROOT / "research" / "analysis" / "vacuum-cell.md").read_text()
    quoted = f"{m['totalNodeMassKg']:.2f}"
    if quoted not in md:
        bad.append(f"vacuum-cell.md does not contain '{quoted}' kg "
                   "(measured node mass) — prose has drifted from the manifest")
    if bad:
        print("check_nodes: FAIL")
        for b in bad:
            print("  " + b)
        sys.exit(1)
    print(f"computed nodes: 51 STLs closed, graph matches the analysis counting "
          f"(96 primaries / 48 spokes / 72 ties), flat lands on every boundary joint, "
          f"measured node mass {m['totalNodeMassKg']} kg at print density.")


if __name__ == "__main__":
    main()
