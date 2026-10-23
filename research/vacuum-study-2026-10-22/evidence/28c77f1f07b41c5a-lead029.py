#!/usr/bin/env python3
"""Lead-point nonlinear check on the own model: (a) load control with the owner's stated scheme (p_ref 0.35 MPa, increments
0.01/0.02 of p_ref, cutback to 1e-6), (b) pole displacement control to the first critical point, with face stress.
usage: lead029.py OUT.json CASE DIR AMP [nth=512 grading=1.35 nface=1 ncore=4 nu=0.33 width=..]"""
import json
import math
import sys
import time

import numpy as np
import scipy.sparse.linalg as spla

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402

out, case, d, amp = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
kv = {"dir": d, "amp": str(amp), "nth": "512", "grading": "1.35", "nface": "1", "ncore": "4"}
kv.update(dict(a.split("=", 1) for a in sys.argv[5:]))
t0 = time.time()
TOL = float(kv.get("tol", 1e-6))                     # residual floor of the lead model is about 3e-8 (conditioning)
m, info = run029.build(case, kv)
fr = m.free
npole = m.nid[0, 2 * m.nt]
probe = 2 * npole + 1
face_rows = [m.nt - 1 - k for k in range(int(kv["nface"]))]
rec = {"case": case, "dir": d, "amp_mm": amp, "args": kv, "info": info, "dof": int(m.ndof)}

# (a) owner-style load control
pref, inc, incmax, incmin = 0.35, 0.01, 0.02, 1e-6
u = np.zeros(m.ndof); t = 0.0; dt = inc; steps = 0
while t < 1.0 and dt >= incmin:
    tt = min(1.0, t + dt); p = tt * pref
    uu = u.copy(); ok = False
    for it in range(16):
        fp, Kp = m.pressure(uu); fi, K = m.internal(uu)
        res = fi[fr] - p * fp[fr]
        if np.linalg.norm(res) / np.linalg.norm(p * fp[fr]) < TOL:
            ok = True; break
        try:
            uu[fr] += spla.spsolve((K - p * Kp)[fr][:, fr].tocsc(), -res)
        except Exception:
            break
        if not np.all(np.isfinite(uu)):
            break
    if ok:
        u = uu; t = tt; steps += 1; dt = min(dt * 1.5, incmax)
    else:
        dt *= 0.5
vm_lc, where_lc = m.face_von_mises(u, face_rows)
rec["load_control"] = {"endpoint_kPa": t * pref * 1e3, "steps": steps, "pole_dz_mm": float(u[probe]),
                       "outer_face_vm_MPa": vm_lc, "where": where_lc}
print("LC", json.dumps(rec["load_control"]), flush=True)

# (b) pole displacement control from zero, adaptive step, to the first failure (critical point)
u = np.zeros(m.ndof); lam = 0.0; z = 0.0; dz = -float(kv.get("dz0", 0.5)); path = []
best = (0.0, None)
while abs(dz) > 1e-4 and len(path) < 4000:
    res_, u2, lam2 = m.disp_control(probe, [z + dz], 1.0, u0=u, lam0=lam, tol=TOL)
    if res_[0][2]:
        u, lam, z = u2, lam2, z + dz
        path.append((z, lam * 1e3))
        if lam > best[0]:
            best = (lam, u.copy(), z)
        dz = max(dz * 1.3, -float(kv.get("dzmax", 2.0)))
        if lam < 0.85 * best[0]:
            break
    else:
        dz *= 0.5
vm_dc, where_dc = m.face_von_mises(best[1], face_rows) if best[1] is not None else (None, None)
rec["disp_control"] = {"lambda_max_kPa": best[0] * 1e3, "pole_dz_at_max_mm": best[2], "stopped_at_dz_mm": z,
                       "stopped_lambda_kPa": lam * 1e3, "outer_face_vm_at_max_MPa": vm_dc, "where": where_dc,
                       "path": path}
print("DC", json.dumps({k: v for k, v in rec["disp_control"].items() if k != "path"}), flush=True)
rec["elapsed_s"] = time.time() - t0
json.dump(rec, open(out, "w"), indent=1)
