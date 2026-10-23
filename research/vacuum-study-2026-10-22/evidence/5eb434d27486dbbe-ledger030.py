#!/usr/bin/env python3
"""MAINLINE-030 corrections ledger: every correction a check or the robotics seat made tonight, with its effect on the
lead. Check corrections come from CHECK-VERDICTS.json (sub-worker extraction of the 35 checks); robotics-seat corrections
are the named orders, read from the queue store by id. Effects on the lead are the checker's own reading.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "outputs" / "vacuum-mainline030-design-register-1020"
SUB = Path("unpublished-local-ref:ab52dba26d6cc3a7")

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def body(i):
    p = SUB / f"{i}.json"
    return json.loads(p.read_text())["body"] if p.exists() else None


def main():
    verdicts = json.loads((OUT / "CHECK-VERDICTS.json").read_text())
    rows = []
    for what, ids, effect in LEAD:
        rows.append({"correction": what, "by": ids, "effect_on_lead": effect, "lead_relevant": True,
                     "ids_in_store": {i: (SUB / f"{i}.json").exists() for i in ids}})
    for v in verdicts:
        for c in v.get("corrections") or []:
            rows.append({"correction": c.get("what"), "old": c.get("old"), "new": c.get("new"), "by": [v["check_id"]],
                         "cards": v.get("cards_checked"), "effect_on_lead": None, "lead_relevant": False})
    (OUT / "LEDGER.json").write_text(json.dumps({"schema": 1, "rows": rows}, indent=1))
    missing = [i for r in rows if r.get("ids_in_store") for i, ok in r["ids_in_store"].items() if not ok]
    print(len(rows), "ledger rows;", sum(r["lead_relevant"] for r in rows), "lead-relevant; ids missing from store:", missing)


if __name__ == "__main__":
    main()
