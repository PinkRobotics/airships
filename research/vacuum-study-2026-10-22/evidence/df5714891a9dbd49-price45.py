#!/usr/bin/env python3
"""MAINLINE-045 pricing: 028b's least set (037b's replica) re-found with an added damage-tolerance mode."""
import math
import os
import sys

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.path.insert(0, "unpublished-local-ref:d49761785f6805ea"
                   "vacuum-mainline037b-bond-temperature-1020")
import bond37b as b  # noqa: E402
import dt45 as d  # noqa: E402

_ORIG = b._point_028b


def with_patch(D, edge, E=290e9, nu=0.0752):
    """028b's point with one more face-local mode: a face patch of diameter D that has lost its core must not
    buckle at the working face stress (patch stress / membrane stress >= 1)."""
    lam2 = d.special.jn_zeros(1, 1)[0] ** 2 if edge == "clamped" else d.ss_root(nu) ** 2

    def point(F, q, sigma_today):
        pt = _ORIG(F, q, sigma_today)
        tf = pt["tf"]
        if tf <= 0:
            return pt
        Dp = E * tf ** 3 / (12.0 * (1.0 - nu * nu))
        a = D / 2.0
        sm = b.m.P0 * 10.0 / (4.0 * tf)
        pt["others"]["patch"] = lam2 * Dp / (a * a * tf) / sm
        pt["others_min"] = min(pt["others"].values())
        return pt
    return point


def usage_with_patch(D, edge):
    b._point_028b = with_patch(D, edge)
    try:
        return b.usage_028b(b.base_q())
    finally:
        b._point_028b = _ORIG


def usage_denser_core(k, extra_mass=0.0):
    """028b's least set on a core k times denser, with shear and compressive moduli scaled by k and crush strength by
    k^(5/3) (PROJECTION: cell-wall stretching and buckling scalings, not Hexcel table values)."""
    q = b.base_q()
    q["rho_c"] *= k
    q["Gc"] *= k
    q["Ec"] *= k
    q["crush"] *= k ** (5.0 / 3.0)
    if extra_mass:
        q["extra_mass"] = extra_mass
    return b.usage_028b(q)


def usage_extra_mass(m):
    q = b.base_q()
    q["extra_mass"] = m
    return b.usage_028b(q)
