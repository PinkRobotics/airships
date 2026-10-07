#!/usr/bin/env python3
"""Replay the per-block motion-inventory review into the shared disposition catalogue.

This script writes review decisions only. Run tools/update_float_records.py twice
for the deterministic record migration and idempotence check.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REVIEWED = [
    {
        "file": "concept/index.html",
        "key": "04f51f8534ed6b95",
        "class": "deferred",
        "reason": "Proposed weather recovery is explicitly undemonstrated; its flight operations have no exact generated-region binding.",
        "owner": "energy-model"
    },
    {
        "file": "docs/OPEN-QUESTIONS.md",
        "key": "066a308c4c261b07",
        "class": "deferred",
        "reason": "ISA and altitude-dependent simulated lift are flight-model arithmetic, without an exact generated-region binding for this paragraph.",
        "owner": "energy-model"
    },
    {
        "file": "docs/OPEN-QUESTIONS.md",
        "key": "1c5c79d4d408a6e8",
        "class": "deferred",
        "reason": "Resize and cycle comparisons concern the simulated energy model; this paragraph has no exact generated-region binding.",
        "owner": "energy-model"
    },
    {
        "file": "index.html",
        "key": "cc0bb6069996e890",
        "class": "flight-model",
        "reason": "The concept render depicts the simulated fleet under the existing bound flight assumption in this same page.",
        "assumption": "22491643fb810667"
    },
    {
        "file": "research/analysis/helium.md",
        "key": "2b3268716b38817f",
        "class": "other-quantity",
        "reason": "Sealed-volume behaviour and ballonet/ballast trade do not establish positive static lift for the drawn structure."
    },
    {
        "file": "research/analysis/payload-exchange.md",
        "key": "e75301d417614ed1",
        "class": "deferred",
        "reason": "Lake ballast and powered hover bounds belong to the simulated energy model; no exact generated-region binding covers this paragraph.",
        "owner": "energy-model"
    },
    {
        "file": "research/analysis/water-availability.md",
        "key": "7752c3f62e50c121",
        "class": "conditional",
        "reason": "Lake depth is a qualified operational scenario, explicitly not a conclusion that any vehicle can hover at a particular lake."
    },
    {
        "file": "research/notes/barrier-and-permeation.md",
        "key": "bd9d48195b5a09aa",
        "class": "method",
        "reason": "Permeation processing and pressure-rise leak tests are research methods, not vehicle ascent; quoted figures remain context.",
        "context": [
            "0.0034",
            "0.84",
            "1.6",
            "2",
            "4"
        ]
    },
    {
        "file": "research/reports/02-paper.md",
        "key": "92780909e7bfc850",
        "class": "deferred",
        "reason": "Displacement is a flight-model scenario that assumes ascent; it does not establish a float result for the drawn hull.",
        "owner": "energy-model"
    },
    {
        "file": "ship/index.html",
        "key": "e836e05fd9c34bec",
        "class": "conditional",
        "reason": "Rotor placement is explicitly marked SCOPING and describes a hypothetical water cycle, not demonstrated static lift."
    },
    {
        "file": "ship/index.html",
        "key": "3e04c805720a2451",
        "class": "other-quantity",
        "reason": "Hovering describes the viewer camera over the displayed surface, not the ship flying."
    },
    {
        "file": "ship/index.html",
        "key": "565c7d45e18a7acc",
        "class": "other-quantity",
        "reason": "Joint seating and printed support motion concern cell geometry, not a claim that a hull can fly."
    }
]


def main():
    args = sys.argv[1:]
    if args not in ([], ['--check']):
        print('Usage: python3 tools/review_gate_motion.py [--check]', file=sys.stderr)
        return 2
    path = ROOT / 'tools/float_dispositions.json'
    if args and not path.exists():
        print('tools/float_dispositions.json: missing generated output', file=sys.stderr)
        return 1
    doc = json.loads(path.read_text())
    reviewed = {(e['file'], e['key']): e for e in REVIEWED}
    found = set()
    for i, entry in enumerate(doc['entries']):
        key = (entry['file'], entry['key'])
        if key in reviewed:
            doc['entries'][i] = reviewed[key]
            found.add(key)
    doc['entries'].extend(e for e in REVIEWED if (e['file'], e['key']) not in found)
    text = json.dumps(doc, ensure_ascii=False, indent=1) + '\n'
    if args:
        if path.read_bytes() != text.encode():
            print('tools/float_dispositions.json: stale generated output', file=sys.stderr)
            return 1
    elif path.read_text() != text:
        path.write_text(text)
    print(f'Motion review: {len(REVIEWED)} explicit per-block decisions')
    return 0


if __name__ == '__main__':
    sys.exit(main())
