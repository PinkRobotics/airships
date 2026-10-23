#!/usr/bin/env python3
"""Transfer40 axisymmetric runs not covered by transfer029.py, one mesh per call, on the owner's declared meshes.
mode=eigen: dead-load linear eigenpressures. mode=static: owner-style load control (p_ref 15 MPa, increments 0.01/0.02,
cutback to 1e-6) and pole displacement control to the first critical point.
usage: transfer029b.py OUT.json mode=eigen|static nth=<n> nface=<n> ncore=<n> [amp=1.97 grading=1.0]"""
import json
import sys
import time

import numpy as np
import scipy.sparse.linalg as spla

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402

out = sys.argv[1]
kv = dict(a.split("=", 1) for a in sys.argv[2:])
mode = kv.pop("mode")
t0 = time.time()
m, info = run029.build("transfer40", kv)
rec = {"args": dict(kv, mode=mode), "info": info, "dof": int(m.ndof), "elements": int(m.ne)}
if mode == "eigen":
    vd, _, _ = m.linear_buckling(nev=4)
    rec["eigen_dead_MPa"] = vd[:4].tolist()
else:
    fr = m.free
    probe = 2 * m.nid[0, 2 * m.nt] + 1
    pref = 15.0; u = np.zeros(m.ndof); t = 0.0; dt = 0.01
    while t < 1.0 and dt >= 1e-6:
        tt = min(1.0, t + dt); p = tt * pref; uu = u.copy(); ok = False
        for it in range(16):
            fp, Kp = m.pressure(uu); fi, K = m.internal(uu)
            res = fi[fr] - p * fp[fr]
            if np.linalg.norm(res) / np.linalg.norm(p * fp[fr]) < 1e-8:
                ok = True; break
            try:
                uu[fr] += spla.spsolve((K - p * Kp)[fr][:, fr].tocsc(), -res)
            except Exception:
                break
            if not np.all(np.isfinite(uu)):
                break
        if ok:
            u = uu; t = tt; dt = min(dt * 1.5, 0.02)
        else:
            dt *= 0.5
    rec["load_control_endpoint_MPa"] = t * pref
    u = np.zeros(m.ndof); lam = 0.0; z = 0.0; dz = -0.02; best = (0.0, 0.0); path = []
    while abs(dz) > 1e-5 and len(path) < 3000:
        r_, u2, l2 = m.disp_control(probe, [z + dz], 1.0, u0=u, lam0=lam)
        if r_[0][2]:
            u, lam, z = u2, l2, z + dz; path.append((z, lam))
            if lam > best[0]:
                best = (lam, z)
            dz = max(dz * 1.3, -0.2)
            if lam < 0.85 * best[0]:
                break
        else:
            dz *= 0.5
    rec.update({"disp_control_lambda_max_MPa": best[0], "pole_dz_at_max_mm": best[1], "stopped_dz_mm": z,
                "stopped_lambda_MPa": lam})
rec["elapsed_s"] = time.time() - t0
json.dump(rec, open(out, "w"), indent=1)
print(json.dumps(rec))
