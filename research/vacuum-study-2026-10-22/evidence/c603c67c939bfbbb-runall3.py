#!/usr/bin/env python3
"""CHECK-047 part B, third batch: face modulus sensitivity (298.7 GPa, NASA CR-194164 Table 2 longitudinal) at the
governing SF 1 pair. Same path as runall.py; its own log fe/batch3.log."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import runall  # noqa: E402

runall.JOBS = [("f-W332-a1.208988-hi-E298.7", [1.208988, runall.W021, "W", 10000], {"ef": 298700.0}),
               ("f-W332-a1.226988-hi-E298.7", [1.226988, runall.W021, "W", 10000], {"ef": 298700.0})]
_open = open


def _redirect(path, *a, **k):
    if isinstance(path, str) and path.endswith(os.path.join("fe", "batch.log")):
        path = path.replace("batch.log", "batch3.log")
    if isinstance(path, str) and path.endswith(os.path.join("fe", "BATCH.json")):
        path = path.replace("BATCH.json", "BATCH3.json")
    return _open(path, *a, **k)


runall.open = _redirect
if __name__ == "__main__":
    runall.main()
