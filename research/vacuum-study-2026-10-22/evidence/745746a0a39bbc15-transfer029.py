#!/usr/bin/env python3
"""Transfer40 shell (R_outer 125.97 mm, faces 0.42, core 3.1, clamped hemisphere, defect 1.97 mm, width 12.597 mm):
linear eigenpressure (dead load) at 384 x (2 face, 4 core); nonlinear first critical point by pole displacement control,
and the owner-style load-control endpoint (p_ref 15 MPa, increments 0.01/0.02, cutback 1e-6)."""
import json, sys, time
import numpy as np
import scipy.sparse.linalg as spla
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402

out = sys.argv[1]
t0 = time.time()
rec = {}
m, _ = run029.build("transfer40", {"nth": "384", "nface": "2", "ncore": "4"})
vd, _, _ = m.linear_buckling(nev=4)
rec["eigen384_dead_MPa"] = vd[:4].tolist()
print("eigen", vd[:3], flush=True)
for tag, kv in (("static384", {"nth": "384", "nface": "2", "ncore": "4", "amp": "1.97"}),
                ("static48graded", {"nth": "48", "nface": "1", "ncore": "2", "amp": "1.97", "grading": "1.5"})):
    m, _ = run029.build("transfer40", kv)
    fr = m.free
    probe = 2 * m.nid[0, 2 * m.nt] + 1
    # load control, owner scheme
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
    lc = t * pref
    # displacement control
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
    rec[tag] = {"load_control_endpoint_MPa": lc, "disp_control_lambda_max_MPa": best[0], "pole_dz_at_max_mm": best[1],
                "stopped_dz_mm": z, "stopped_lambda_MPa": lam, "dof": int(m.ndof)}
    print(tag, json.dumps(rec[tag]), flush=True)
rec["elapsed_s"] = time.time() - t0
json.dump(rec, open(out, "w"), indent=1)
