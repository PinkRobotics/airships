#!/usr/bin/env python3
"""Pressure at which the outer face's maximum Cauchy von Mises first reaches 345 MPa (SR-200 tensile yield used as the line's
compression proxy) and 379.2 MPa (one historical lot), along the pole displacement-controlled path of a lead case.
usage: yield029.py OUT.json CASE DIR AMP"""
import json
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402

out, case, d, amp = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
kv = {"dir": d, "amp": str(amp), "nth": "512", "grading": "1.35", "nface": "1", "ncore": "4"}
t0 = time.time()
m, info = run029.build(case, kv)
probe = 2 * m.nid[0, 2 * m.nt] + 1
rows = [m.nt - 1]
u = np.zeros(m.ndof); lam = 0.0; z = 0.0; dz = -0.5
path = []
first = {}
peak = 0.0
while abs(dz) > 1e-4 and len(path) < 600:
    r_, u2, l2 = m.disp_control(probe, [z + dz], 1.0, u0=u, lam0=lam, tol=1e-6)
    if not r_[0][2]:
        dz *= 0.5
        continue
    u, lam, z = u2, l2, z + dz
    vm, where = m.face_von_mises(u, rows)
    path.append({"pole_dz_mm": z, "p_kPa": lam * 1e3, "outer_face_vm_MPa": vm, "where": where})
    for thr in (345.0, 379.2):
        if thr not in first and vm >= thr:
            a = path[-2] if len(path) > 1 else {"p_kPa": 0.0, "outer_face_vm_MPa": 0.0}
            f = (thr - a["outer_face_vm_MPa"]) / (vm - a["outer_face_vm_MPa"])
            first[thr] = a["p_kPa"] + f * (lam * 1e3 - a["p_kPa"])
    peak = max(peak, lam)
    dz = max(dz * 1.25, -2.0)
    if lam < 0.98 * peak:
        break
rec = {"case": case, "dir": d, "amp_mm": amp, "first_yield_kPa": {str(k): v for k, v in first.items()},
       "limit_kPa": peak * 1e3, "path": path, "elapsed_s": time.time() - t0}
json.dump(rec, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in rec.items() if k != "path"}))
