#!/usr/bin/env python3
"""Validation record for axi029: homogeneous complete sphere, membrane displacement and classical buckling at R/t 100 and
1000 (E 210 GPa, nu 0.3). Classical p = 2 E t^2 / (R_mid^2 sqrt(3(1 - nu^2))); membrane w = p R_mid^2 (1 - nu) / (2 E t).
usage: validate_rec.py OUT.json"""
import json
import math
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from axi029 import Model  # noqa: E402

E, nu = 210000.0, 0.3
rows = []
for R, t, nth in ((1000.0, 10.0, 240), (1000.0, 1.0, 960)):
    t0 = time.time()
    m = Model(R, [{"t": t, "n": 4, "mat": ("iso", E, nu)}], math.pi, nth, grading=1.0, fix_south_inner_z=True)
    vals, _, u1 = m.linear_buckling(nev=2)
    vf, _, _ = m.linear_buckling(nev=2, load_stiffness=True)
    Rm = R - t / 2
    pcl = 2 * E * t ** 2 / (Rm ** 2 * math.sqrt(3 * (1 - nu ** 2)))
    n_eq = m.nid[m.nth, 2 * m.nt]
    w = -Rm ** 2 * (1 - nu) / (2 * E * t)
    rows.append({"R_outer_mm": R, "t_mm": t, "R_over_t": R / t, "ntheta": nth, "classical_MPa": pcl, "eigen_dead_MPa": vals[0],
                 "eigen_follower_MPa": vf[0], "ratio_dead": vals[0] / pcl, "ratio_follower": vf[0] / pcl,
                 "equator_outer_ur_mm_per_MPa": float(u1[2 * n_eq]), "membrane_mm_per_MPa": w,
                 "ur_ratio": float(u1[2 * n_eq]) / w, "s": time.time() - t0})
    print(json.dumps(rows[-1]), flush=True)
json.dump(rows, open(sys.argv[1], "w"), indent=1)
