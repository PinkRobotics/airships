#!/usr/bin/env python3
"""Core stress diagnostic along a lead path (the sibling of the card's face stress diagnostic, which the card does not
make). Pole displacement control to the limit point on the card's static mesh; at each state, the core's Cauchy stresses
in the current tangent/normal frame: the largest transverse shear |tau_tn| and the most compressive normal stress
sigma_nn over the core Gauss points, with their location. The pressures at which they reach the card's own Hexcel CR III
Table II strengths (5056, 3/8 in. cell, 1.0 pcf; typical and minimum) are interpolated along the path.
usage: core029.py OUT.json CASE DIR AMP [nth=512 grading=1.35 nface=1 ncore=4]"""
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import run029  # noqa: E402
from axi029 import GP3, q8  # noqa: E402

PSI = 0.00689475729                                     # MPa per psi
STRENGTH_PSI = {"W shear typ": 35, "W shear min": 25, "L shear typ": 55, "L shear min": 45,
                "bare compression typ": 55, "bare compression min": 25, "stabilized compression typ": 60,
                "stabilized compression min": 35, "crush typ": 35}

out, case, d, amp = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
kv = {"dir": d, "amp": str(amp), "nth": "512", "grading": "1.35", "nface": "1", "ncore": "4"}
kv.update(dict(a.split("=", 1) for a in sys.argv[5:]))
t0 = time.time()
m, info = run029.build(case, kv)
nf, nc = int(kv["nface"]), int(kv["ncore"])
core_rows = list(range(nf, nf + nc))
sel = np.nonzero(np.isin(np.arange(m.ne) % m.nt, core_rows))[0]
shape = [q8(xi, eta) for xi in GP3 for eta in GP3]       # same order as m.gp


def core_state(u):
    ue = u[m.edofs].reshape(m.ne, 8, 2)
    xe = m.X[m.conn] + ue
    best_tau, best_sn = (0.0, None), (0.0, None)
    for g, (N, dx, de) in zip(m.gp, shape):
        E, _ = m._kin(g, ue)
        S = np.einsum("eij,ej->ei", g["C"], E)
        H11 = np.einsum("ea,ea->e", g["dNr"], ue[:, :, 0]); H12 = np.einsum("ea,ea->e", g["dNz"], ue[:, :, 0])
        H21 = np.einsum("ea,ea->e", g["dNr"], ue[:, :, 1]); H22 = np.einsum("ea,ea->e", g["dNz"], ue[:, :, 1])
        hr = (ue[:, :, 0] @ g["N"]) / g["r"]
        tr = xe[:, :, 0] @ dx; tz = xe[:, :, 1] @ dx          # current meridional tangent
        for e in sel:
            F = np.array([[1 + H11[e], H12[e], 0], [H21[e], 1 + H22[e], 0], [0, 0, 1 + hr[e]]])
            Sm = np.array([[S[e, 0], S[e, 3], 0], [S[e, 3], S[e, 1], 0], [0, 0, S[e, 2]]])
            sig = F @ Sm @ F.T / np.linalg.det(F)
            a = math.atan2(tz[e], tr[e]); c, s = math.cos(a), math.sin(a)
            srr, szz, srz = sig[0, 0], sig[1, 1], sig[0, 1]
            snn = s * s * srr + c * c * szz - 2 * c * s * srz
            tau = -c * s * srr + c * s * szz + (c * c - s * s) * srz
            where = (int(e), float((m.X[m.conn[e, :4], 0]).mean()))
            if abs(tau) > abs(best_tau[0]):
                best_tau = (float(tau), where)
            if snn < best_sn[0]:
                best_sn = (float(snn), where)
    return best_tau, best_sn


probe = 2 * m.nid[0, 2 * m.nt] + 1
u = np.zeros(m.ndof); lam = 0.0; z = 0.0; dz = -0.5; path = []; peak = 0.0
while abs(dz) > 1e-4 and len(path) < 600:
    r_, u2, l2 = m.disp_control(probe, [z + dz], 1.0, u0=u, lam0=lam, tol=1e-6)
    if not r_[0][2]:
        dz *= 0.5
        continue
    u, lam, z = u2, l2, z + dz
    (tau, wt), (sn, ws) = core_state(u)
    path.append({"pole_dz_mm": z, "p_kPa": lam * 1e3, "core_max_abs_tau_MPa": abs(tau), "tau_where": wt,
                 "core_min_sigma_nn_MPa": sn, "sigma_nn_where": ws})
    peak = max(peak, lam)
    dz = max(dz * 1.25, -2.0)
    if lam < 0.98 * peak:
        break


def first(key, thr, sign=1):
    prev = {"p_kPa": 0.0, key: 0.0}
    for r in path:
        if sign * r[key] >= thr > sign * prev[key]:
            f_ = (thr - sign * prev[key]) / (sign * r[key] - sign * prev[key])
            return prev["p_kPa"] + f_ * (r["p_kPa"] - prev["p_kPa"])
        prev = r
    return None


cross = {}
for name, psi in STRENGTH_PSI.items():
    mpa = psi * PSI
    if "shear" in name:
        cross[name] = {"MPa": mpa, "p_kPa": first("core_max_abs_tau_MPa", mpa)}
    else:
        cross[name] = {"MPa": mpa, "p_kPa": first("core_min_sigma_nn_MPa", mpa, -1)}
at_peak = max(path, key=lambda r: r["p_kPa"])
op = next((r for r in path if r["p_kPa"] >= 95.46083791390515), None)
rec = {"case": case, "dir": d, "amp_mm": amp, "args": kv, "limit_kPa": peak * 1e3, "strength_crossings": cross,
       "at_limit": at_peak, "first_state_at_or_above_operating": op, "path": path, "elapsed_s": time.time() - t0,
       "source": "Hexcel CR III Table II, 5056, 3/8 in. cell, 1.0 pcf row (the card's cited datasheet, owner's pinned copy 0467f718...)"}
json.dump(rec, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in rec.items() if k != "path"}, indent=1))
