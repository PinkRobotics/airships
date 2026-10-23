#!/usr/bin/env python3
"""Stability of a lead static path on a refined mesh: load control (tolerance 1e-6, small steps) to each target pressure,
then the lowest eigenvalues of the symmetrised tangent K - p K_p on the free DOFs. A negative eigenvalue below the limit
point means the path has passed a bifurcation (for example face wrinkling) before its maximum. For the lowest mode it
records where the outer-face radial motion peaks and the inner/outer face correlation (near -1 = symmetric wrinkling).
usage: stab_lead029.py OUT.json CASE DIR AMP ps=<kPa,...> [nth=2048 grading=1.35 nface=1 ncore=4 dp=<kPa> sigma=-1 k=3]"""
import json
import sys
import time

import numpy as np
import scipy.sparse.linalg as spla

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402

out, case, d, amp = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
kv = {"dir": d, "amp": str(amp), "nth": "2048", "grading": "1.35", "nface": "1", "ncore": "4"}
kv.update(dict(a.split("=", 1) for a in sys.argv[5:]))
targets = [float(x) / 1e3 for x in kv["ps"].split(",")]
dp = float(kv.get("dp", 2.0)) / 1e3
t0 = time.time()
m, info = run029.build(case, kv)
fr = m.free
inner_node = m.nid[:, 0]                  # inner surface nodes along the meridian (index 0 = north pole)
outer_node = m.nid[:, 2 * m.nt]           # outer surface nodes
u = np.zeros(m.ndof); p = 0.0; rows = []
for pt in targets:
    while p < pt - 1e-15:
        step = min(dp, pt - p)
        ok = False
        while not ok and step > 1e-9:
            uu = u.copy(); pn = p + step
            for it in range(25):
                fp, Kp = m.pressure(uu); fi, K = m.internal(uu)
                res = fi[fr] - pn * fp[fr]
                if np.linalg.norm(res) / np.linalg.norm(pn * fp[fr]) < 1e-6:
                    ok = True; break
                uu[fr] += spla.spsolve((K - pn * Kp)[fr][:, fr].tocsc(), -res)
            if not ok:
                step *= 0.5
        if not ok:
            break
        u, p = uu, pn
    if abs(p - pt) > 1e-12:
        rows.append({"p_kPa": pt * 1e3, "converged": False, "reached_kPa": p * 1e3})
        break
    fp, Kp = m.pressure(u); fi, K = m.internal(u)
    KT = (K - p * Kp)[fr][:, fr]
    KS = (0.5 * (KT + KT.T)).tocsc()
    # the k eigenvalues nearest sigma; a sigma far below the spectrum (e.g. -1000) returns the k algebraically lowest
    vals, vecs = spla.eigsh(KS, k=int(kv.get("k", 3)), sigma=float(kv.get("sigma", -1.0)), which="LM")
    order = np.argsort(vals); vals = vals[order]; vecs = vecs[:, order]
    modes = []
    for q in range(vecs.shape[1]):
        phi = np.zeros(m.ndof); phi[fr] = vecs[:, q]
        # normal (radial) motion of the inner and outer surface nodes along the meridian
        def normal_motion(nodes):
            X = m.X[nodes]; nrm = X / np.linalg.norm(X, axis=1)[:, None]
            return phi[2 * nodes] * nrm[:, 0] + phi[2 * nodes + 1] * nrm[:, 1]
        wi, wo = normal_motion(inner_node), normal_motion(outer_node)
        k = int(np.argmax(np.abs(wo)))
        corr = float(np.dot(wi, wo) / (np.linalg.norm(wi) * np.linalg.norm(wo) + 1e-300))
        modes.append({"eig": float(vals[q]), "outer_peak_r_mm": float(m.X[outer_node[k], 0]),
                      "outer_peak_z_mm": float(m.X[outer_node[k], 1]), "inner_outer_corr": corr})
    rows.append({"p_kPa": p * 1e3, "converged": True, "lowest_eigs": vals.tolist(), "pole_dz_mm": float(u[2 * m.nid[0, 2 * m.nt] + 1]),
                 "modes": modes})
    print(json.dumps(rows[-1]), flush=True)
json.dump({"case": case, "dir": d, "amp_mm": amp, "args": kv, "dof": int(m.ndof), "rows": rows, "elapsed_s": time.time() - t0},
          open(out, "w"), indent=1)
