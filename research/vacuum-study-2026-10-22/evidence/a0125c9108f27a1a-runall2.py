#!/usr/bin/env python3
"""CHECK-047 part B, second batch: core in-plane regularisation sensitivity at the governing passing amplitude.
Same build/solve/parse path as runall.py (imported); its own log fe/batch2.log and marker."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import runall  # noqa: E402

W021 = runall.W021
runall.JOBS = [
    ("c-W332-a1.208988-hi-ein0.01", [1.208988, W021, "W", 10000], {"ein": 0.01, "gin": 0.005}),
    ("c-W332-a1.208988-hi-ein10", [1.208988, W021, "W", 10000], {"ein": 10.0, "gin": 5.0}),
]
_open = open


def _redirect(path, *a, **k):
    if isinstance(path, str) and path.endswith(os.path.join("fe", "batch.log")):
        path = path.replace("batch.log", "batch2.log")
    if isinstance(path, str) and path.endswith(os.path.join("fe", "BATCH.json")):
        path = path.replace("BATCH.json", "BATCH2.json")
    return _open(path, *a, **k)


runall.open = _redirect
if __name__ == "__main__":
    runall.main()
