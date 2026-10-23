#!/usr/bin/env python3
"""Lowest eigenvalues of the (symmetrised) tangent stiffness along a load-controlled path: a negative value means the
equilibrium is unstable (past a limit or bifurcation)."""
import json, sys
import numpy as np
import scipy.sparse.linalg as spla
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402

out, case = sys.argv[1], sys.argv[2]
kv = dict(a.split("=", 1) for a in sys.argv[3:])
m, info = run029.build(case, kv)
fr = m.free
targets = [float(x) for x in kv["ps"].split(",")]
u = np.zeros(m.ndof)
rows = []
p_prev = 0.0
for p_target in targets:
    # small load steps to stay on the primary path
    n = max(1, int((p_target - p_prev) / float(kv.get("dp", 0.05))))
    for k in range(1, n + 1):
        p = p_prev + (p_target - p_prev) * k / n
        for it in range(30):
            fp, Kp = m.pressure(u); fi, K = m.internal(u)
            res = fi[fr] - p * fp[fr]
            if np.linalg.norm(res) / np.linalg.norm(p * fp[fr]) < 1e-10:
                break
            u[fr] += spla.spsolve((K - p * Kp)[fr][:, fr].tocsc(), -res)
    p_prev = p_target
    fp, Kp = m.pressure(u); fi, K = m.internal(u)
    KT = (K - p_target * Kp)[fr][:, fr]
    KS = 0.5 * (KT + KT.T)
    asym = spla.norm(KT - KT.T) / spla.norm(KT)
    vals = spla.eigsh(KS.tocsc(), k=3, sigma=-1.0, which="LM", return_eigenvectors=False)
    npole = m.nid[0, 2 * m.nt]
    rec = {"p_MPa": p_target, "lowest_eigs": sorted(vals.tolist()), "pole_dz_mm": float(u[2 * npole + 1]), "asym": float(asym)}
    rows.append(rec)
    print(json.dumps(rec), flush=True)
json.dump({"case": case, "args": kv, "rows": rows}, open(out, "w"), indent=1)
