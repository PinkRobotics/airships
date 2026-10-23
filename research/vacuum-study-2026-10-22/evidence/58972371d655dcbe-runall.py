#!/usr/bin/env python3
"""CHECK-047 part B batch: build, solve (serially, through simjob via simretry.sh), parse and compress each run.

Each solve is ccx on 4 cores under simjob; a refusal (exit 75) is retried unchanged at least 60 s apart by simretry.sh.
A run whose result.json already exists is skipped, so the batch can be resumed. Writes fe/BATCH.json at the end."""
import gzip
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fe047  # noqa: E402

W021, W021B = 332.2164186283597, 401.8559050423529
SF = "SF1,SF105"
JOBS = [
    # governing W 332.216 brackets on the identical pre-yield branch (10,000 MPa), then at a real 345 MPa
    ("g-W332-a1.208988-hi", [1.208988, W021, "W", 10000], {}),
    ("g-W332-a1.226988-hi", [1.226988, W021, "W", 10000], {}),
    ("g-W332-a0.737936-hi", [0.737936, W021, "W", 10000], {}),
    ("g-W332-a0.755936-hi", [0.755936, W021, "W", 10000], {}),
    ("p-W332-a1.208988-345", [1.208988, W021, "W", 345], {}),
    ("p-W332-a1.226988-345", [1.226988, W021, "W", 345], {}),
    ("p-W332-a0.737936-345", [0.737936, W021, "W", 345], {}),
    ("p-W332-a0.755936-345", [0.755936, W021, "W", 345], {}),
    # L 332.216 and W 401.856 SF 1 brackets
    ("g-L332-a1.79559-hi", [1.79559, W021, "L", 10000], {}),
    ("g-L332-a1.810809-hi", [1.810809, W021, "L", 10000], {}),
    ("g-W402-a1.284271-hi", [1.284271, W021B, "W", 10000], {}),
    ("g-W402-a1.302271-hi", [1.302271, W021B, "W", 10000], {}),
    # cure-debit brackets (341.59 MPa screen) on the governing footprint
    ("g-W332-a1.117424-hi", [1.117424, W021, "W", 10000], {}),
    ("g-W332-a1.135424-hi", [1.135424, W021, "W", 10000], {}),
    ("g-W332-a0.65274-hi", [0.65274, W021, "W", 10000], {}),
    ("g-W332-a0.67074-hi", [0.67074, W021, "W", 10000], {}),
    # endpoint division by 1.10: the limiting W 401.856 pair, at 345 MPa, run on to the numerical endpoint
    ("e-W402-a0.520967-345", [0.520967, W021B, "W", 345], {"pressures": [95.46083791390515], "endpoint": 112.0}),
    ("e-W402-a0.538967-345", [0.538967, W021B, "W", 345], {"pressures": [95.46083791390515], "endpoint": 112.0}),
    # perfect-sphere endpoints
    ("e-perfect-345", [0.0, W021, "W", 345], {"pressures": [95.46083791390515], "endpoint": 115.0}),
    ("e-perfect-300", [0.0, W021, "W", 300], {"pressures": [90.0], "endpoint": 100.0}),
    ("e-perfect-255", [0.0, W021, "W", 255], {"pressures": [75.0], "endpoint": 85.0}),
    # mesh control on the governing SF 1 pair: 2 mm angular, three elements a face, eight in the core
    ("m-W332-a1.208988-hi", [1.208988, W021, "W", 10000], {"hfine": 2.0, "nf": 3, "nc": 8}),
    ("m-W332-a1.226988-hi", [1.226988, W021, "W", 10000], {"hfine": 2.0, "nf": 3, "nc": 8}),
    # one larger dimple: first core shear and first face yield (pre-yield branch), and the 345 MPa endpoint
    ("s-W332-a11.8-hi", [11.8, W021, "W", 10000], {"pressures": [20.0, 21.6, 22.0, 23.0, 24.0, 25.2, 58.0, 60.0, 61.0, 62.0, 63.0, 64.0]}),
    ("s-W332-a11.8-345", [11.8, W021, "W", 345], {"pressures": [40.0], "endpoint": 80.0}),
]


def main():
    log = open(os.path.join(HERE, "fe", "batch.log"), "a")
    done = []
    for name, (a, w, mer, ys), kw in JOBS:
        d = os.path.join(HERE, "fe", name)
        if os.path.exists(os.path.join(d, "result.json")):
            done.append(name)
            continue
        pressures = kw.pop("pressures", [fe047.P_SERVICE, 1.05 * fe047.P_SERVICE])
        endpoint = kw.pop("endpoint", None)
        fe047.build(name, a, w, mer, ys, pressures, endpoint, **kw)
        t0 = time.time()
        print(f"{time.strftime('%H:%M:%S')} start {name}", file=log, flush=True)
        rc = subprocess.run([os.path.join(HERE, "simretry.sh"), "run.log", "4", "8G", "env", "OPENBLAS_NUM_THREADS=1", "OMP_NUM_THREADS=4",
                             "CCX_NPROC_EQUATION_SOLVER=4", "ccx", "-i", "job"], cwd=d, stdout=open(os.path.join(d, "ccx.out"), "w"),
                            stderr=subprocess.STDOUT).returncode
        el = time.time() - t0
        try:
            res = fe047.parse(name)
            res["solver_returncode"] = rc
            res["wall_s"] = el
            json.dump(res, open(os.path.join(d, "result.json"), "w"), indent=1, default=float)
            ok = True
        except Exception as e:          # keep going; the failure is recorded
            json.dump({"error": repr(e), "solver_returncode": rc, "wall_s": el}, open(os.path.join(d, "result.json"), "w"))
            ok = False
        for f in ("job.dat",):
            p = os.path.join(d, f)
            if os.path.exists(p):
                with open(p, "rb") as src, gzip.open(p + ".gz", "wb", compresslevel=6) as dst:
                    shutil.copyfileobj(src, dst)
                os.remove(p)
        for f in ("job.frd", "job.12d", "spooles.out"):
            p = os.path.join(d, f)
            if os.path.exists(p):
                os.remove(p)
        print(f"{time.strftime('%H:%M:%S')} end {name} rc {rc} parsed {ok} {el:.0f} s", file=log, flush=True)
        done.append(name)
    json.dump({"done": done, "jobs": [j[0] for j in JOBS], "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")},
              open(os.path.join(HERE, "fe", "BATCH.json"), "w"), indent=1)
    print("__BATCH_DONE__", file=log, flush=True)


if __name__ == "__main__":
    main()
