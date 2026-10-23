#!/usr/bin/env python3
"""MAINLINE-017b: the cheapest combination, the smallest product of improvement factors that reaches SF 1.

Minimise sum(ln f) over the chosen levers and the geometry, with every mode's ln SF >= 0 (SLSQP, many starts).
P2's handbook gamma steps from 0.20 to 1 at Vc 2, so each branch is solved separately with its own Vc constraint.
Every answer is then re-checked by re-optimising the geometry at the found factors with the scan optimisers.
"""
import math
import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from scipy.optimize import minimize  # noqa: E402

import model17b as m  # noqa: E402
import scan17b as sc  # noqa: E402

LN_MAX = math.log(1e3)


# ----------------------------------------------------------------------------- P2
def p2_point(R, fac, F, branch):
    q = m.p2_apply(m.P2_TODAY, fac)
    g = m.p2_geometry(R, np.array([F]), q, "019")
    if branch == "stiff":
        q["gamma_rule"] = "conservative"     # gamma = min(1, 0.20 f) at the point; Vc <= 2 is a constraint
    ev, aux = m.p2_modes(R, g["tf"], g["tc"], q,
                         gamma_override=(1.0 if branch == "crimp" else None))
    return ev, aux, g


def p2_combo(R, levers, caps=None, branch="stiff", starts=None, seed=1):
    caps = caps or {}
    n = len(levers)
    ub = [math.log(caps[k]) if k in caps else LN_MAX for k in levers]

    def unpack(x):
        return {k: math.exp(v) for k, v in zip(levers, x[:n])}, math.exp(x[n])

    def cons(x):
        fac, F = unpack(x)
        ev, aux, g = p2_point(R, fac, F, branch)
        c = [math.log(max(ev[k][0], 1e-300)) for k in m.P2_MODES]
        vc = aux["Vc"][0]
        c.append(math.log(2.0 / vc) if branch == "stiff" else math.log(vc / 2.0))
        return np.array(c)

    bounds = [(0.0, u) for u in ub] + [(math.log(1e-6), math.log(0.9999))]
    rng = np.random.default_rng(seed)
    x0s = list(starts or [])
    for _ in range(24):
        x0s.append(np.concatenate([rng.uniform(0, 1.0, n) * np.minimum(ub, 2.0), [math.log(rng.uniform(0.05, 0.5))]]))
    best = None
    for x0 in x0s:
        x0 = np.clip(np.asarray(x0, dtype=float), [b[0] for b in bounds], [b[1] for b in bounds])
        try:
            r = minimize(lambda x: float(np.sum(x[:n])), x0, method="SLSQP", bounds=bounds,
                         constraints=[{"type": "ineq", "fun": cons}],
                         options={"maxiter": 600, "ftol": 1e-12})
        except Exception:  # noqa: BLE001 - a failed start is skipped, never fatal
            continue
        if not r.success and r.status not in (8, 9):
            continue
        if np.min(cons(r.x)) < -1e-7:
            continue
        val = float(np.sum(r.x[:n]))
        if best is None or val < best["ln_product"] - 1e-10:
            fac, F = unpack(r.x)
            best = {"ln_product": val, "product": math.exp(val), "factors": fac, "F": F, "branch": branch}
    return best


def p2_verify(R, fac, F=None):
    """Re-optimise the geometry at the found factors with the handbook rule; also score the combination's own
    point, since a crimp-branch answer can sit on a sliver of fractions next to Vc 2 that a grid can miss."""
    best = sc.p2_best(R, fac, "handbook")
    if F is not None:
        q = m.p2_apply(m.P2_TODAY, fac)
        g = m.p2_geometry(R, np.array([F]), q, "019")
        ev, aux = m.p2_modes(R, g["tf"], g["tc"], q)
        own = float(m.p2_least(ev)[0])
        if own > best["least"]:
            best = {"least": own, "F": F, "governing": min(m.P2_MODES, key=lambda k: ev[k][0]),
                    "Vc": float(aux["Vc"][0]), "tf": float(g["tf"][0]), "tc": float(g["tc"][0]), "own_point": True}
    return best


# ----------------------------------------------------------------------------- P3
def p3_point(row, fac, x):
    film, joint = sc.P3_ROWS[row]
    q = m.p3_apply(m.P3_TODAY, m.FILMS[film], joint, fac)
    s, lt, ro = x
    ev = m.p3_eval(np.array([s]), np.array([math.exp(lt)]), np.array([ro]), q, sc.RES_P3)
    return q, ev


def p3_combo(row, levers, caps=None, starts=None, seed=1):
    caps = caps or {}
    n = len(levers)
    ub = [math.log(caps[k]) if k in caps else LN_MAX for k in levers]
    film = m.FILMS[sc.P3_ROWS[row][0]]

    def unpack(x):
        return {k: math.exp(v) for k, v in zip(levers, x[:n])}, x[n:]

    def cons(x):
        fac, g = unpack(x)
        q, ev = p3_point(row, fac, g)
        s, lt, ro = g
        area = float(ev["area"][0])
        c = []
        for k in m.P3_MODES:
            v = float(np.broadcast_to(ev["sfs"][k], (1,))[0])
            c.append(math.log(v) if v > 0 and np.isfinite(v) else -50.0)
        c.append(min(0.25, s / 3.0) - ro)                       # r_o within 022c's cap
        c.append((ro * ro - area / math.pi) / (ro * ro) - 1e-9)  # a real wall
        c.append(float(ev["m_tube"][0]) / 1000.0)               # tubes have mass
        c.append(lt - math.log(film["t_cat"]))                  # film no thinner than the catalogue gauge
        return np.array(c)

    bounds = [(0.0, u) for u in ub] + [(0.4, 19.0), (math.log(film["t_cat"]), math.log(0.01)), (0.005, 0.25)]
    rng = np.random.default_rng(seed)
    x0s = list(starts or [])
    for _ in range(24):
        s0 = rng.uniform(0.6, 8.0)
        x0s.append(np.concatenate([rng.uniform(0, 1.0, n) * np.minimum(ub, 1.5),
                                   [s0, math.log(rng.uniform(film["t_cat"], 1e-3)), rng.uniform(0.05, min(0.25, s0 / 3))]]))
    best = None
    for x0 in x0s:
        x0 = np.clip(np.asarray(x0, dtype=float), [b[0] for b in bounds], [b[1] for b in bounds])
        try:
            r = minimize(lambda x: float(np.sum(x[:n])), x0, method="SLSQP", bounds=bounds,
                         constraints=[{"type": "ineq", "fun": cons}],
                         options={"maxiter": 800, "ftol": 1e-12})
        except Exception:  # noqa: BLE001
            continue
        if np.min(cons(r.x)) < -1e-7:
            continue
        val = float(np.sum(r.x[:n]))
        if best is None or val < best["ln_product"] - 1e-10:
            fac, g = unpack(r.x)
            best = {"ln_product": val, "product": math.exp(val), "factors": fac,
                    "s": float(g[0]), "tfilm": float(math.exp(g[1])), "ro": float(g[2])}
    return best


def p3_verify(row, fac):
    return sc.p3_best(row, fac)
