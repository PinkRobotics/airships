#!/usr/bin/env python3
"""MAINLINE-057: RESULTS.json, NFI.json and INPUTS.json from mga057.json; prints the R10 item tables and the artifact pins."""
import datetime
import hashlib
import json
from pathlib import Path

W = Path("unpublished-local-ref:7a5bf1cec24b249e")
ME = W / "ref-55cff924be25afe6f9dd/.ship"
O = ME / "work/outputs/vacuum-mainline057-mass-growth-1020"
S = ME / "work/scripts/mga057"
SUB = Path("unpublished-local-ref:ab52dba26d6cc3a7")


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
