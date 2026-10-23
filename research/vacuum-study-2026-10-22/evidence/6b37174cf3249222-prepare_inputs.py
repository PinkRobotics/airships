#!/usr/bin/env python3
"""Pin the filed evidence and extract the numerical inputs; no source code imported."""
import hashlib
import json
import math
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
QUEUE = Path("unpublished-local-ref:ab52dba26d6cc3a7")
PINS = []


def pin(path, role, expected=None):
    path = Path(path)
    data = path.read_bytes()
    row = dict(path=str(path), sha256=hashlib.sha256(data).hexdigest(),
               bytes=len(data), role=role,
               basis="verified filing" if expected else "measured")
    if expected:
        assert row["sha256"] == expected["sha256"], str(path)
        assert row["bytes"] == expected["bytes"], str(path)
    PINS.append(row)
    return data


def report(name, role):
    d = json.loads(pin(QUEUE / (name + ".json"), role + " filing"))
    out = {}
    for a in d.get("artifacts", []):
        b = pin(a["path"], role, a)
        if Path(a["path"]).name in ("INPUTS.json", "RESULTS.json", "POINT.json"):
            out[Path(a["path"]).name] = json.loads(b)
    return out

[withheld: private task or principal quotation; scientific result/status retained elsewhere]