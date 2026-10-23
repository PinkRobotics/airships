#!/usr/bin/env python3
"""MAINLINE-030: build the merged NFI register from the joined topic rows, the checker's canonical-gap mapping and the
check verdicts. Writes REGISTER.json and REGISTER.md into the 030 output folder. Every source row keeps its card, row id,
report id and file path. Check outcomes on the main gaps are the checker's own reading, cited by check id.
"""
import json
import re
from collections import OrderedDict
from pathlib import Path

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def norm_card(c):
    m = re.search(r"MAINLINE-0*(\d+)([A-Z]?\d?)", c.upper())
    return f"MAINLINE-{int(m.group(1)):03d}{m.group(2)}" if m else c


def main():
    joined = json.loads((OUT / "TOPICS-JOINED.json").read_text())
    canon = json.loads((OUT / "CANON.json").read_text())
    verdicts = json.loads((OUT / "CHECK-VERDICTS.json").read_text())
    checks_by_card = {}
    for v in verdicts:
        for c in v.get("cards_checked") or []:
            checks_by_card.setdefault(norm_card(c), []).append(f"{v['check_id']} ({v.get('verdict')})")
    groups = OrderedDict()
    for r in joined:
        k = r["key"].strip().lower()
        topic, gap = canon.get(k, [r["topic"], r["key"].strip()])
        groups.setdefault((topic, gap), []).append(r)
    # one row the filed NFI files carry only inside a documentation row (NFI-CHK011B-TEXT, M4), now load-bearing for 022b
    m4 = next(r for r in joined if r["card"] == "CHECK-011b" and "TEXT" in str(r["row_id"]))
    groups[("T15", "two-way grid global coefficient 4 assumes isotropy; an unbraced two-way grid has no in-plane shear "
                    "stiffness (022b's two-way rows rest on it)")] = [dict(m4, unknown="Whether a two-way grid without "
                    "diagonals has any smeared global buckling capacity near 4*E*sqrt(I*A)/(s*R^2); the lattice sum gives "
                    "C1212 = 0. 022b's two-way rows (Ti + Kapton 0.986, SiC 1.98) are governed by it.", today="C = 4 (isotropic)",
                    needed="a discrete buckling solve of the two-way frame, or diagonals", state="unknown", direction="optimistic")]
    OUTCOME.append(("two-way grid global coefficient", "OBJECTION, demonstrated (lattice sum, C1212 = 0) by rpt-check011b-opus-"
                    "1020 M4; 022b adopted the 2V-4 count but kept C = 4."))
    order = sorted(groups, key=lambda tg: (tg[0], tg[1].lower()))
    reg, files = [], OrderedDict()
    for i, (topic, gap) in enumerate(order, 1):
        rows = groups[(topic, gap)]
        src_cards = []
        for r in rows:
            c = r["card"]
            if c not in src_cards:
                src_cards.append(c)
            files.setdefault(r["report"], r["file"])

        def distinct(field):
            out = []
            for r in rows:
                v = r.get(field)
                if v and str(v).lower() != "null":
                    s = f"{v} [{r['card']}]"
                    if not any(str(v) in o for o in out):
                        out.append(s)
            return out
        unknown = max((r["unknown"] for r in rows), key=len)
        checked = []
        for c in src_cards:
            for ch in checks_by_card.get(norm_card(c), []):
                if ch not in checked:
                    checked.append(ch)
        outcome = next((o for p, o in OUTCOME if gap.startswith(p) or p in gap), None)
        raised_by_check = [r["card"] for r in rows if r["card"].startswith("CHECK")]
        reg.append({"rid": f"R{i:03d}", "topic": topic, "topic_name": TOPIC[topic], "gap": gap, "unknown": unknown,
                    "today": distinct("today")[:4], "needed": distinct("needed")[:4],
                    "owners": sorted({r["owner"] for r in rows}), "states": sorted({r["state"] for r in rows}),
                    "directions": sorted({r["direction"] for r in rows}), "check_outcome": outcome,
                    "raised_by_checks": sorted(set(raised_by_check)), "source_cards_checked_by": checked[:6],
                    "sources": [{"uid": r["uid"], "card": r["card"], "row_id": r["row_id"], "report": r["report"],
                                 "file": r["file"]} for r in rows]})
    (OUT / "REGISTER.json").write_text(json.dumps({"schema": 1, "rows": reg, "source_files": files}, indent=1))
    md = ["# MAINLINE-030 NFI register — every filed card's and check's NFI rows, merged",
          "",
          "QUESTIONABLE throughout; PROJECTION where a row says so. Nothing here is a certification. Built by build030.py from "
          "TOPICS-JOINED.json (each verbatim row normalised by a sub-worker, completeness-checked), the checker's CANON.json "
          "merge map, and CHECK-VERDICTS.json. Where two cards name the same gap, every id is kept. Report ids and NFI file "
          "paths are in the source table at the end; REGISTER.json carries the same data per row.",
          "",
          f"{len(reg)} register rows from {len(joined)} filed rows in {len(files)} reports.", ""]
    cur = None
    for r in reg:
        if r["topic"] != cur:
            cur = r["topic"]
            md += ["", f"## {cur} {TOPIC[cur]}", ""]
        ids = "; ".join(f"{s['card']} {s['row_id']}" for s in r["sources"])
        md.append(f"**{r['rid']}. {r['gap']}**")
        md.append(f"- Unknown: {r['unknown']}")
        if r["today"]:
            md.append(f"- Today: {' | '.join(r['today'])}")
        if r["needed"]:
            md.append(f"- Needed or settling test: {' | '.join(r['needed'])}")
        md.append(f"- Owner: {', '.join(r['owners'])}. State: {', '.join(r['states'])}.")
        if r["check_outcome"]:
            md.append(f"- Check: {r['check_outcome']}")
        elif r["raised_by_checks"]:
            md.append(f"- Check: raised by {', '.join(r['raised_by_checks'])}.")
        elif r["source_cards_checked_by"]:
            md.append(f"- Check: source cards checked by {', '.join(r['source_cards_checked_by'][:3])}; no objection on this row.")
        else:
            md.append("- Check: no check filed on the source cards yet.")
        md.append(f"- Ids: {ids}")
        md.append("")
    md += ["", "## Sources: report id and NFI file", "", "| report | file |", "|---|---|"]
    for rep, f in files.items():
        md.append(f"| {rep} | {f} |")
    (OUT / "REGISTER.md").write_text("\n".join(md) + "\n")
    print(len(reg), "register rows;", sum(1 for r in reg if r["check_outcome"]), "with a check outcome;",
          len(files), "source files")
    for r in reg:
        print(r["rid"], r["topic"], len(r["sources"]), r["gap"][:100])


if __name__ == "__main__":
    main()
