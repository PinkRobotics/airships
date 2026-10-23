#!/usr/bin/env python3
"""Is a negative tangent eigenvalue on a very finely graded lead mesh real? At each target pressure (load control from zero),
take the lowest eigenpair of the symmetrised tangent and report the eigen residual, the Rayleigh quotient of the
unsymmetrised tangent, and its split into material + geometric (K at u) and pressure load stiffness (-p K_p) parts,
plus the same quotient for the small-strain stiffness K0. A negative quotient of K0 would mean the discretisation itself
is indefinite; a negative quotient at a few kPa would mean an artefact rather than a buckling mode.
usage: diag_stab029.py OUT.json CASE DIR AMP ps=<kPa,...> [nth= grading= nface= ncore= dp=<kPa>]"""
import json
import sys
import time

import numpy as np
import scipy.sparse.linalg as spla

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402

out, case, d, amp = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
kv = {"dir": d, "amp": str(amp), "nth": "4096", "grading": "2.0", "nface": "1", "ncore": "4"}
kv.update(dict(a.split("=", 1) for a in sys.argv[5:]))
targets = [float(x) / 1e3 for x in kv["ps"].split(",")]
dp = float(kv.get("dp", 3.0)) / 1e3
t0 = time.time()
m, info = run029.build(case, kv)
fr = m.free
_, K0 = m.internal(np.zeros(m.ndof), linear=True)
K0 = K0[fr][:, fr]
u = np.zeros(m.ndof); p = 0.0; rows = []
for pt in targets:
    while p < pt - 1e-15:
        step = min(dp, pt - p); ok = False
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
        u, p = uu, pn
    fp, Kp = m.pressure(u); fi, K = m.internal(u)
    Km = K[fr][:, fr]; Kl = (-p * Kp)[fr][:, fr]
    KT = Km + Kl
    KS = (0.5 * (KT + KT.T)).tocsc()
    rec = {"p_kPa": p * 1e3}
    for tag, sig in (("sigma_-1", -1.0), ("sigma_-1e-3", -1e-3)):
        vals, vecs = spla.eigsh(KS, k=3, sigma=sig, which="LM")
        i = int(np.argmin(vals)); lam = float(vals[i]); phi = vecs[:, i] / np.linalg.norm(vecs[:, i])
        rec[tag] = {"eigs": sorted(vals.tolist()), "lowest": lam,
                    "residual": float(np.linalg.norm(KS @ phi - lam * phi)),
                    "rayleigh_KT": float(phi @ (KT @ phi)), "rayleigh_K_at_u": float(phi @ (Km @ phi)),
                    "rayleigh_load_stiffness": float(phi @ (Kl @ phi)), "rayleigh_K0": float(phi @ (K0 @ phi))}
    rows.append(rec)
    print(json.dumps(rec), flush=True)
json.dump({"case": case, "dir": d, "amp_mm": amp, "args": kv, "dof": int(m.ndof), "rows": rows, "elapsed_s": time.time() - t0},
          open(out, "w"), indent=1)
