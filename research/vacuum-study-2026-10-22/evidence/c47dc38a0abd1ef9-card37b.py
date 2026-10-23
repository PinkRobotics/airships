#!/usr/bin/env python3
"""MAINLINE-037b: CARD.md, RESULTS.json, NFI.json and INPUTS.json from COMPUTE.json (and 037's pinned RESULTS)."""
import datetime
import hashlib
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(HERE, "COMPUTE.json")))
R037 = json.load(open(C["pins"]["037_results"]["path"]))
JOB_STARTED = "2026-10-20T02:24:33-07:00"   # order read; a measurement, never a limit


def f3(x, n=3):
    return "n/a" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f"{x:.{n}f}"

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    def pin(path, role):
        data = open(path, "rb").read()
        return {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "role": role}
    pins = [dict(v, role="input read; " + k) for k, v in C["pins"].items()]
    for name in ("bond37b.py", "run37b.py", "card37b.py", "COMPUTE.json"):
        pins.append(pin(os.path.join(HERE, name), "this card's own code or intermediate"))
    inputs = {"schema": 1, "card": "MAINLINE-037b", "unit": "vacuum-mainline037b-bond-temperature-1020", "pins": pins,
              "sources_used": C["sources_used"],
              "reports_used": ["rpt-ref-8c5de04c9c33dbcf7447", "rpt-ref-d907de1e97319ecc3f9a",
                               "rpt-ref-2519e14e5d71b9eb18f3"]}
    with open(os.path.join(HERE, "INPUTS.json.tmp"), "w") as fh:
        json.dump(inputs, fh, indent=1)
    os.replace(os.path.join(HERE, "INPUTS.json.tmp"), os.path.join(HERE, "INPUTS.json"))
    print(len(text), "bytes card;", len(nfi["items"]), "NFI;", len(pins), "pins")


if __name__ == "__main__":
    main()
