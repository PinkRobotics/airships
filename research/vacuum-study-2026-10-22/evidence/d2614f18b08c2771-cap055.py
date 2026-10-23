#!/usr/bin/env python3
"""MAINLINE-055: elastic limit point, face first yield and core shear along the path of a lead sandwich section, for a full
sphere or a clamped spherical cap, with a stress-free Gaussian dimple at the pole. Uses the CHECK-029 axisymmetric model
(check029/axi029.py: 8-node total-Lagrangian St. Venant-Kirchhoff, follower pressure). Pole displacement control to the
limit point; at each state the outer/inner face Cauchy von Mises maxima and the core's largest transverse shear and most
compressive normal stress (current tangent/normal frame). Elastic: no plasticity, so the limit point is an elastic one.

usage: cap055.py OUT.json key=value ...
  section: tf, tc (mm), Ef (MPa), nuf, sy (face yield, MPa), En, G (core, MPa), Ein, Gin
  geometry: R (mm), a (cap base radius, mm; 0 = full sphere), amp (mm), width (mm)
  mesh: nth, grading, nface, ncore"""
import json
import math
import sys
import time

import numpy as np

sys.path.insert(0, "unpublished-local-ref:a48c891263300bfb")
from axi029 import GP3, Model, q8  # noqa: E402

PSI = 0.00689475729
CORE_STRENGTH = {"W shear typ": 35 * PSI, "W shear min": 25 * PSI, "L shear typ": 55 * PSI, "L shear min": 45 * PSI,
                 "crush typ": 35 * PSI}

out = sys.argv[1]
kv = dict(a.split("=", 1) for a in sys.argv[2:])
f = {k: float(v) for k, v in kv.items() if k not in ("label",)}
t0 = time.time()
R, a = f["R"], f.get("a", 0.0)
face = ("iso", f["Ef"], f["nuf"])
core = ("core", f.get("En", 103.42135939752539), f.get("G", 46.88434959354485), f.get("Ein", 0.01), f.get("Gin", 0.005))
layers = [{"t": f["tf"], "n": int(f.get("nface", 1)), "mat": face}, {"t": f["tc"], "n": int(f.get("ncore", 4)), "mat": core},
          {"t": f["tf"], "n": int(f.get("nface", 1)), "mat": face}]
if a > 0:
    m = Model(R, layers, math.asin(a / R), int(f.get("nth", 256)), grading=f.get("grading", 1.35),
              dimple=(f["amp"], f["width"]) if f.get("amp", 0) > 0 else None, clamp_equator=True)
else:
    m = Model(R, layers, math.pi, int(f.get("nth", 512)), grading=f.get("grading", 1.35),
              dimple=(f["amp"], f["width"]) if f.get("amp", 0) > 0 else None, fix_south_inner_z=True)
nf, nc = layers[0]["n"], layers[1]["n"]
outer_rows, inner_rows, core_rows = [nf + nc + k for k in range(nf)], list(range(nf)), list(range(nf, nf + nc))
shape = [q8(xi, eta) for xi in GP3 for eta in GP3]
rowj = np.arange(m.ne) % m.nt


def state(u):
    ue = u[m.edofs].reshape(m.ne, 8, 2)
    xe = m.X[m.conn] + ue
    vm_o = vm_i = tau = 0.0; sn = 0.0; w_tau = w_o = w_i = w_sn = None
    for g, (N, dx, de) in zip(m.gp, shape):
        E, _ = m._kin(g, ue)
        S = np.einsum("eij,ej->ei", g["C"], E)
        H11 = np.einsum("ea,ea->e", g["dNr"], ue[:, :, 0]); H12 = np.einsum("ea,ea->e", g["dNz"], ue[:, :, 0])
        H21 = np.einsum("ea,ea->e", g["dNr"], ue[:, :, 1]); H22 = np.einsum("ea,ea->e", g["dNz"], ue[:, :, 1])
        hr = (ue[:, :, 0] @ g["N"]) / g["r"]
        tr = xe[:, :, 0] @ dx; tz = xe[:, :, 1] @ dx
        for e in range(m.ne):
            F = np.array([[1 + H11[e], H12[e], 0], [H21[e], 1 + H22[e], 0], [0, 0, 1 + hr[e]]])
            Sm = np.array([[S[e, 0], S[e, 3], 0], [S[e, 3], S[e, 1], 0], [0, 0, S[e, 2]]])
            sig = F @ Sm @ F.T / np.linalg.det(F)
            rj = rowj[e]
            if rj in core_rows:
                al = math.atan2(tz[e], tr[e]); c, s = math.cos(al), math.sin(al)
                srr, szz, srz = sig[0, 0], sig[1, 1], sig[0, 1]
                snn = s * s * srr + c * c * szz - 2 * c * s * srz
                t_ = abs(-c * s * srr + c * s * szz + (c * c - s * s) * srz)
                if t_ > tau:
                    tau = t_; w_tau = float(m.X[m.conn[e, :4], 0].mean())
                if snn < sn:
                    sn = snn; w_sn = float(m.X[m.conn[e, :4], 0].mean())
            else:
                dev = sig - np.trace(sig) / 3 * np.eye(3)
                vm = math.sqrt(1.5 * np.sum(dev * dev))
                if rj in outer_rows:
                    if vm > vm_o:
                        vm_o = vm; w_o = float(m.X[m.conn[e, :4], 0].mean())
                elif vm > vm_i:
                    vm_i = vm; w_i = float(m.X[m.conn[e, :4], 0].mean())
    return {"outer_vm": vm_o, "outer_vm_r_mm": w_o, "inner_vm": vm_i, "inner_vm_r_mm": w_i, "core_tau": tau,
            "core_tau_r_mm": w_tau, "core_min_snn": sn, "core_min_snn_r_mm": w_sn}


probe = 2 * m.nid[0, 2 * m.nt] + 1
u = np.zeros(m.ndof); lam = 0.0; z = 0.0; dz = -float(f.get("dz0", 0.5)); path = []; best = (0.0, None)
while abs(dz) > 1e-4 and len(path) < 800:
    r_, u2, l2 = m.disp_control(probe, [z + dz], 1.0, u0=u, lam0=lam, tol=1e-6)
    if not r_[0][2]:
        dz *= 0.5
        continue
    u, lam, z = u2, l2, z + dz
    st = state(u)
    st.update({"pole_dz_mm": z, "p_kPa": lam * 1e3})
    path.append(st)
    if lam > best[0]:
        best = (lam, z)
    dz = max(dz * 1.3, -float(f.get("dzmax", 2.0)))
    if lam < 0.98 * best[0]:                  # stop just past the first limit point (a cap can restiffen after snapping)
        break


def first(key, thr, sign=1):
    prev = {"p_kPa": 0.0, key: 0.0}
    for r in path:
        if sign * r[key] >= thr > sign * prev[key]:
            fr = (thr - sign * prev[key]) / (sign * r[key] - sign * prev[key])
            return prev["p_kPa"] + fr * (r["p_kPa"] - prev["p_kPa"])
        prev = r
    return None


cross = {"face yield (outer)": first("outer_vm", f["sy"]), "face yield (inner)": first("inner_vm", f["sy"])}
for k, v in CORE_STRENGTH.items():
    cross[k] = first("core_min_snn", v, -1) if k.startswith("crush") else first("core_tau", v)
h = f["tc"] + f["tf"]
nu = f["nuf"]
p_cl = 2 * f["Ef"] * h * 2 * f["tf"] / (R ** 2 * math.sqrt(1 - nu ** 2))          # MPa, line convention (R = outer)
p_cr = 2 * h ** 2 * f.get("G", 46.88434959354485) / (R * f["tc"])
Vc = p_cl / p_cr
Kc = 1 - Vc / 4 if Vc <= 2 else 1 / Vc
rec = {"label": kv.get("label", ""), "args": kv, "dof": int(m.ndof), "elements": int(m.ne),
       "limit_kPa": best[0] * 1e3, "pole_dz_at_limit_mm": best[1], "stopped_kPa": lam * 1e3,
       "p_classical_kPa": p_cl * 1e3, "p_crimp_kPa": p_cr * 1e3, "Vc": Vc, "Kc": Kc, "p_H_kPa": Kc * p_cl * 1e3,
       "gamma_H_elastic_limit": best[0] / (Kc * p_cl), "crossings_kPa": cross, "path": path, "elapsed_s": time.time() - t0}
json.dump(rec, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in rec.items() if k != "path"}))
