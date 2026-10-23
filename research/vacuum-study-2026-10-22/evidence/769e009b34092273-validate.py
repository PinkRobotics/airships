#!/usr/bin/env python3
"""Validation of axi029 against closed forms: membrane state and classical buckling of a homogeneous complete sphere."""
import math
import sys
import time

import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from axi029 import Model  # noqa: E402

E, nu = 210000.0, 0.3
R, t = 1000.0, 10.0                                       # R/t 100 (outer radius 1000 mm)
t0 = time.time()
m = Model(R, [{"t": t, "n": 4, "mat": ("iso", E, nu)}], math.pi, 240, grading=1.0, fix_south_inner_z=True)
print("nodes", m.nn, "dof", m.ndof, "elements", m.ne)
# membrane check: hoop stress at the equator from linear static under p = 1
vals, vecs, u1 = m.linear_buckling(nev=4)
Rm = R - t / 2
pcl = 2 * E * t ** 2 / (Rm ** 2 * math.sqrt(3 * (1 - nu ** 2)))
print("classical (mid radius) MPa", pcl, "eigen (no load stiffness)", vals[:4], "ratio", vals[0] / pcl)
vals2, _, _ = m.linear_buckling(nev=4, load_stiffness=True)
print("eigen with follower load stiffness", vals2[:4], "ratio", vals2[0] / pcl)
# radial displacement of the outer equator under p = 1 vs membrane: w = p R^2 (1 - nu) / (2 E t)
n_eq = m.nid[m.nth, 2 * m.nt]
print("equator outer u_r", u1[2 * n_eq], "membrane", -1 * Rm ** 2 * (1 - nu) / (2 * E * t))
print("elapsed", time.time() - t0)
