#!/usr/bin/env python3
"""049: classical laminate theory for a quasi-isotropic face from sourced lamina properties (this seat's code).

In-plane only: A = sum Qbar_k t_k. A balanced, symmetric quasi-isotropic layup ([0/+-60] or [0/+-45/90]) gives an
isotropic in-plane modulus and expansion. Strength is a first-ply estimate on maximum strain: the laminate fails in
equal-biaxial or uniaxial compression when a ply reaches its fibre-direction or transverse compressive strain.
"""
import math

import numpy as np


def qbar(E1, E2, G12, nu12, theta):
    nu21 = nu12 * E2 / E1
    d = 1.0 - nu12 * nu21
    Q11, Q22, Q12, Q66 = E1 / d, E2 / d, nu12 * E2 / d, G12
    c, s = math.cos(theta), math.sin(theta)
    T = np.array([[c * c, s * s, 2 * c * s], [s * s, c * c, -2 * c * s], [-c * s, c * s, c * c - s * s]])
    Q = np.array([[Q11, Q12, 0.0], [Q12, Q22, 0.0], [0.0, 0.0, Q66]])
    Tinv = np.linalg.inv(T)
    R = np.diag([1.0, 1.0, 2.0])
    return Tinv @ Q @ R @ T @ np.linalg.inv(R)


def quasi_iso(E1, E2, G12, nu12, a1=None, a2=None, angles=(0.0, 60.0, -60.0)):
    """Laminate modulus, Poisson ratio and expansion for equal plies at the given angles (degrees)."""
    A = sum(qbar(E1, E2, G12, nu12, math.radians(t)) for t in angles) / len(angles)
    S = np.linalg.inv(A)
    Ex = 1.0 / S[0, 0]
    nu = -S[0, 1] / S[0, 0]
    out = {"E_Pa": Ex, "nu": nu, "A_per_t": A}
    if a1 is not None and a2 is not None:
        # thermal force per thickness: sum Qbar (alpha_ply in laminate axes); alpha_lam = A^-1 N_T
        NT = np.zeros(3)
        for t in angles:
            th = math.radians(t)
            c, s = math.cos(th), math.sin(th)
            alpha_xy = np.array([a1 * c * c + a2 * s * s, a1 * s * s + a2 * c * c, 2 * (a1 - a2) * c * s])
            NT += qbar(E1, E2, G12, nu12, th) @ alpha_xy / len(angles)
        out["alpha"] = float((S @ NT)[0])
    return out


def compression_first_ply(E1, E2, G12, nu12, Xc, Yc, angles=(0.0, 60.0, -60.0), biaxial=True):
    """Laminate compressive stress at first ply failure on maximum strain in ply axes, for equal-biaxial
    (biaxial=True) or uniaxial laminate compression."""
    A = sum(qbar(E1, E2, G12, nu12, math.radians(t)) for t in angles) / len(angles)
    S = np.linalg.inv(A)
    sig = np.array([1.0, 1.0 if biaxial else 0.0, 0.0])
    eps = S @ sig                                  # laminate strain per unit (compressive) stress
    worst = 0.0
    for t in angles:
        th = math.radians(t)
        c, s = math.cos(th), math.sin(th)
        e1 = eps[0] * c * c + eps[1] * s * s + eps[2] * c * s
        e2 = eps[0] * s * s + eps[1] * c * c - eps[2] * c * s
        worst = max(worst, abs(e1) / (Xc / E1), abs(e2) / (Yc / E2))
    return 1.0 / worst
