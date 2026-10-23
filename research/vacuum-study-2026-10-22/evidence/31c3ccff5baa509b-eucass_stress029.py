#!/usr/bin/env python3
"""Stresses of the elastic EUCASS model at the paper's nonlinear pressures: along the pole displacement-controlled path of
the flat model (imperfect, mu 0.75; and perfect), the maximum Cauchy von Mises in each face and the most compressive
principal Cauchy stress in the foam, so the elastic state at 6.03 MPa (imperfect) and 12.45 MPa (perfect) can be set
against the paper's Fig. 3 foam plateau and Fig. 5 steel curve.
usage: eucass_stress029.py OUT.json CASE AMP [nth=96 nface=2 ncore=4 pmax=13]
StVK in uniaxial compression with nu 0 carries at most E/(3 sqrt 3) Cauchy stress, at stretch 1/sqrt 3 (7.70 MPa for 40 MPa)."""
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402


def layer_stress(m, u, rows):
    """(max von Mises, most compressive principal stress, smallest principal stretch) over Gauss points of elements in the
    given thickness rows."""
    ue = u[m.edofs].reshape(m.ne, 8, 2)
    sel = np.nonzero(np.isin(np.arange(m.ne) % m.nt, rows))[0]
    vm_max = 0.0; smin = 0.0; lmin = 1.0
    for g in m.gp:
        E, _ = m._kin(g, ue)
        S = np.einsum("eij,ej->ei", g["C"], E)
        H11 = np.einsum("ea,ea->e", g["dNr"], ue[:, :, 0]); H12 = np.einsum("ea,ea->e", g["dNz"], ue[:, :, 0])
        H21 = np.einsum("ea,ea->e", g["dNr"], ue[:, :, 1]); H22 = np.einsum("ea,ea->e", g["dNz"], ue[:, :, 1])
        hr = (ue[:, :, 0] @ g["N"]) / g["r"]
        for e in sel:
            F = np.array([[1 + H11[e], H12[e], 0], [H21[e], 1 + H22[e], 0], [0, 0, 1 + hr[e]]])
            Sm = np.array([[S[e, 0], S[e, 3], 0], [S[e, 3], S[e, 1], 0], [0, 0, S[e, 2]]])
            sig = F @ Sm @ F.T / np.linalg.det(F)
            s = sig - np.trace(sig) / 3 * np.eye(3)
            vm_max = max(vm_max, math.sqrt(1.5 * np.sum(s * s)))
            smin = min(smin, float(np.linalg.eigvalsh(sig)[0]))
            lmin = min(lmin, math.sqrt(float(np.linalg.eigvalsh(F.T @ F)[0])))
    return vm_max, smin, lmin


out, case, amp = sys.argv[1], sys.argv[2], float(sys.argv[3])
kv = {"nth": "96", "nface": "2", "ncore": "4", "amp": str(amp)}               # pmax=<MPa> stops the path early
kv.update(dict(a.split("=", 1) for a in sys.argv[4:]))
t0 = time.time()
m, info = run029.build(case, kv)
nf, nc = int(kv["nface"]), int(kv["ncore"])
inner, core, outer = list(range(nf)), list(range(nf, nf + nc)), list(range(nf + nc, 2 * nf + nc))
probe = 2 * m.nid[0, 2 * m.nt] + 1
u = np.zeros(m.ndof); lam = 0.0; z = 0.0; dz = -0.01; path = []; peak = 0.0
while abs(dz) > 1e-6 and len(path) < 2000:
    r_, u2, l2 = m.disp_control(probe, [z + dz], 1.0, u0=u, lam0=lam, tol=1e-8)
    if not r_[0][2]:
        dz *= 0.5
        continue
    u, lam, z = u2, l2, z + dz
    vo, so, lo = layer_stress(m, u, outer); vi, si, li = layer_stress(m, u, inner); vc, sc, lc = layer_stress(m, u, core)
    path.append({"pole_dz_mm": z, "p_MPa": lam, "outer_vm": vo, "inner_vm": vi, "core_min_principal": sc,
                 "core_min_stretch": lc})
    peak = max(peak, lam)
    dz = max(dz * 1.25, -0.05)
    if lam < 0.97 * peak or lam > float(kv.get("pmax", 13.0)):
        break


def at(p):
    for a, b in zip(path, path[1:]):
        if a["p_MPa"] <= p <= b["p_MPa"]:
            f = (p - a["p_MPa"]) / (b["p_MPa"] - a["p_MPa"])
            return {k: a[k] + f * (b[k] - a[k]) for k in a}
    return None


rec = {"case": case, "amp_mm": amp, "args": kv, "dof": int(m.ndof), "peak_MPa": peak,
       "at_6.03": at(6.03), "at_5.63": at(5.63), "at_12.45": at(12.45), "path": path, "elapsed_s": time.time() - t0}
json.dump(rec, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in rec.items() if k != "path"}))
