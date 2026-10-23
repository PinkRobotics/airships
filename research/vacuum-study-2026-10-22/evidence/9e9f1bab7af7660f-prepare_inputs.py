#!/usr/bin/env python3
"""Freeze filed numerical inputs; never execute another seat's programs."""
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
QUEUE = Path("unpublished-local-ref:ab52dba26d6cc3a7")
PINS = []


def pin(path, role, expected=None):
    path = Path(path)
    raw = path.read_bytes()
    got = dict(path=str(path), sha256=hashlib.sha256(raw).hexdigest(),
               bytes=len(raw), role=role)
    if expected:
        assert got["sha256"] == expected["sha256"], str(path)
        assert got["bytes"] == expected["bytes"], str(path)
    PINS.append(got)
    return raw


def report(name, role):
    d = json.loads(pin(QUEUE / f"{name}.json", role + " filing"))
    out = {}
    for a in d["artifacts"]:
        raw = pin(a["path"], role, a)
        if Path(a["path"]).suffix == ".json":
            out[Path(a["path"]).name] = json.loads(raw)
    return out

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def strict_json(value,path=""):
    if isinstance(value,float) and not math.isfinite(value):
        replacement="Infinity" if value>0 else "-Infinity" if value<0 else "NaN"
        normalisations.append(dict(path=path,inherited_nonfinite_value=replacement,
                                   representation="string; raw source retained by its pin"))
        return replacement
    if isinstance(value,dict):
        return {k:strict_json(v,path+"/"+k) for k,v in value.items()}
    if isinstance(value,list):
        return [strict_json(v,path+"/"+str(k)) for k,v in enumerate(value)]
    return value


out=strict_json(out)
out["json_normalisation_notes"]=normalisations
(ROOT / "INPUTS.json").write_text(json.dumps(out, indent=2,allow_nan=False) + "\n")
print("Verified", len(PINS), "pins; cores", len(cores), "nonclimate", out["nonclimate_kg"],
      "climate", climate)
