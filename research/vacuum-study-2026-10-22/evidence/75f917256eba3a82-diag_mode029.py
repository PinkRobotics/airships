#!/usr/bin/env python3
"""Where does a negative tangent mode live? Load control to one pressure, take the lowest eigenpair of the symmetrised
tangent (shift -1), and split phi^T K phi by element into material (B^T C B at u), initial-stress (geometric) and
small-strain (B0^T C B0) parts. Reports the elements with the most negative total, with their location, layer and
stresses, and the totals by layer.
usage: diag_mode029.py OUT.json CASE DIR AMP P_kPa [nth= grading= nface= ncore= dp=<kPa> sigma=-1 ein= gin=]"""
import json
import sys
import time

import numpy as np
import scipy.sparse.linalg as spla

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402

out, case, d, amp, pt = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5]) / 1e3
kv = {"dir": d, "amp": str(amp), "nth": "4096", "grading": "2.0", "nface": "1", "ncore": "4"}
kv.update(dict(a.split("=", 1) for a in sys.argv[6:]))
dp = float(kv.get("dp", 3.0)) / 1e3
t0 = time.time()
m, info = run029.build(case, kv)
fr = m.free
u = np.zeros(m.ndof); p = 0.0
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
KT = (K - p * Kp)[fr][:, fr]
vals, vecs = spla.eigsh((0.5 * (KT + KT.T)).tocsc(), k=1, sigma=float(kv.get("sigma", -1.0)), which="LM")
phi = np.zeros(m.ndof); phi[fr] = vecs[:, 0] / np.linalg.norm(vecs[:, 0])
# normal motion of the outer and inner surface nodes along the meridian; wavelength from zero crossings where it is large
def normal_motion(nodes):
    X = m.X[nodes]; nrm = X / np.linalg.norm(X, axis=1)[:, None]
    return phi[2 * nodes] * nrm[:, 0] + phi[2 * nodes + 1] * nrm[:, 1]
wo = normal_motion(m.nid[:, 2 * m.nt]); wi = normal_motion(m.nid[:, 0])
ro = m.X[m.nid[:, 2 * m.nt], 0]
act = np.nonzero(np.abs(wo) > 0.1 * np.abs(wo).max())[0]
seg = wo[act.min():act.max() + 1]; rseg = ro[act.min():act.max() + 1]
zc = int(np.sum(np.sign(seg[1:]) * np.sign(seg[:-1]) < 0))
shape = {"active_r_mm": [float(rseg.min()), float(rseg.max())], "zero_crossings": zc,
         "wavelength_mm": float(2 * (rseg.max() - rseg.min()) / zc) if zc else None,
         "outer_inner_corr_active": float(np.dot(wo[act], wi[act]) / (np.linalg.norm(wo[act]) * np.linalg.norm(wi[act]) + 1e-300)),
         "outer_peak_r_mm": float(ro[int(np.argmax(np.abs(wo)))])}
ue = u[m.edofs].reshape(m.ne, 8, 2)
pe = phi[m.edofs]                                          # (ne, 16)
em = np.zeros(m.ne); eg = np.zeros(m.ne); e0 = np.zeros(m.ne)
Smin = np.full(m.ne, np.inf); Smax = np.full(m.ne, -np.inf)
for g in m.gp:
    E, B = m._kin(g, ue)
    S = np.einsum("eij,ej->ei", g["C"], E)
    _, B0 = m._kin(g, np.zeros_like(ue))
    Bp = np.einsum("eij,ej->ei", B, pe); B0p = np.einsum("eij,ej->ei", B0, pe)
    em += np.einsum("ei,eij,ej->e", Bp, g["C"], Bp) * g["w"]
    e0 += np.einsum("ei,eij,ej->e", B0p, g["C"], B0p) * g["w"]
    G = m._geo(g, S)
    eg += np.einsum("ei,eij,ej->e", pe, G, pe) * g["w"]
    Smin = np.minimum(Smin, S.min(axis=1)); Smax = np.maximum(Smax, S.max(axis=1))
tot = em + eg
row = np.arange(m.ne) % m.nt; col = np.arange(m.ne) // m.nt
cent = m.X[m.conn[:, :4]].mean(axis=1)
order = np.argsort(tot)[:12]
worst = [{"element": int(e), "meridional_index": int(col[e]), "layer_row": int(row[e]), "r_mm": float(cent[e, 0]),
          "z_mm": float(cent[e, 1]), "material": float(em[e]), "geometric": float(eg[e]), "small_strain": float(e0[e]),
          "S_min": float(Smin[e]), "S_max": float(Smax[e]),
          "length_mm": float(np.linalg.norm(m.X[m.conn[e, 1]] - m.X[m.conn[e, 0]])),
          "thickness_mm": float(np.linalg.norm(m.X[m.conn[e, 3]] - m.X[m.conn[e, 0]]))} for e in order]
by_layer = {int(k): {"material": float(em[row == k].sum()), "geometric": float(eg[row == k].sum()),
                     "small_strain": float(e0[row == k].sum())} for k in range(m.nt)}
share = np.abs(tot) / np.abs(tot).sum()
top = np.argsort(-share)[:50]
rec = {"case": case, "dir": d, "amp_mm": amp, "args": kv, "p_kPa": p * 1e3, "eig": float(vals[0]), "shape": shape,
       "totals": {"material": float(em.sum()), "geometric": float(eg.sum()), "small_strain": float(e0.sum()),
                  "load_stiffness": float(phi[fr] @ ((-p * Kp)[fr][:, fr] @ phi[fr]))},
       "by_layer": by_layer, "worst_elements": worst,
       "energy_share_top50_elements": float(share[top].sum()),
       "top50_meridional_index_range": [int(col[top].min()), int(col[top].max())],
       "top50_r_mm_range": [float(cent[top, 0].min()), float(cent[top, 0].max())], "elapsed_s": time.time() - t0}
json.dump(rec, open(out, "w"), indent=1)
print(json.dumps(rec, indent=1))
