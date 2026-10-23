#!/usr/bin/env python3
"""CHECK-060: RESULTS.json (card value against my value for every checked number, with verdicts), NFI.json and INPUTS.json;
prints the artifact pins."""
import datetime
import hashlib
import json
from pathlib import Path

ME = Path("unpublished-local-ref:b4008749caf12a44")
O = ME / "work/outputs/vacuum-mainline060-check-1020"
S = ME / "work/scripts/check060"
W = Path("unpublished-local-ref:7a5bf1cec24b249e")
SUB = Path("unpublished-local-ref:ab52dba26d6cc3a7")
SCR = Path("unpublished-local-ref:328c3cdb361f38a6"
           "62008c44-5149-4121-bd7d-8db0f4ad70e6/scratchpad")


def pin(p):
    b = Path(p).read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def row(section, field, card, mine, verdict, note=""):
    return {"section": section, "field": field, "card": card, "mine": mine, "verdict": verdict, "note": note}

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
