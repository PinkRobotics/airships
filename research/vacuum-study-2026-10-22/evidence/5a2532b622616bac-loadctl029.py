#!/usr/bin/env python3
"""Load control with cutback (the owner's stated scheme: increments of 0.01/0.02 of p_ref, minimum 1e-6) on the own model,
to see where load control stops compared with the arc-length limit."""
import json, math, sys
import numpy as np
import scipy.sparse.linalg as spla
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402

out, case = sys.argv[1], sys.argv[2]
kv = dict(a.split("=", 1) for a in sys.argv[3:])
m, info = run029.build(case, kv)
pref = float(kv.get("pref", 40.0)); inc = float(kv.get("inc", 0.01)); incmax = float(kv.get("incmax", 0.02))
incmin = float(kv.get("incmin", 1e-6))
fr = m.free
u = np.zeros(m.ndof); t = 0.0; dt = inc
hist = []
while t < 1.0 and dt >= incmin:
    tt = min(1.0, t + dt); p = tt * pref
    uu = u.copy(); ok = False
    for it in range(int(kv.get("maxit", 16))):
        fp, Kp = m.pressure(uu); fi, K = m.internal(uu)
        res = fi[fr] - p * fp[fr]
        if np.linalg.norm(res) / np.linalg.norm(p * fp[fr]) < float(kv.get("tol", 1e-8)):
            ok = True; break
        try:
            uu[fr] += spla.spsolve((K - p * Kp)[fr][:, fr].tocsc(), -res)
        except Exception:
            break
        if not np.all(np.isfinite(uu)):
            break
    if ok:
        u = uu; t = tt; hist.append((p, it)); dt = min(dt * 1.5, incmax)
    else:
        dt *= 0.5
npole = m.nid[0, 2 * m.nt]
rec = {"case": case, "args": kv, "endpoint_MPa": t * pref, "last_increment": dt, "steps": len(hist),
       "pole_outer_dz_mm": float(u[2 * npole + 1]), "history": hist}
json.dump(rec, open(out, "w"), indent=1)
print(json.dumps(rec))
