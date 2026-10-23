#!/usr/bin/env python3
"""MAINLINE-055: NFI.json and INPUTS.json from RESULTS.json; prints the artifact pins for the report."""
import hashlib
import json
from pathlib import Path

ME = Path("unpublished-local-ref:b4008749caf12a44")
O = ME / "work/outputs/vacuum-mainline055-gamma-test-1020"
S = ME / "work/scripts/gamma055"
W = Path("unpublished-local-ref:7a5bf1cec24b249e")
SUB = Path("unpublished-local-ref:ab52dba26d6cc3a7")


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
