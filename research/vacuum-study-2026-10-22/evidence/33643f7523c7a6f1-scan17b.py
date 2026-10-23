#!/usr/bin/env python3
"""MAINLINE-017b scans: each property alone to SF 1 (re-optimised at every step), and the cheapest combination."""
import math
import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402
from scipy.optimize import minimize  # noqa: E402

import model17b as m  # noqa: E402

# property id -> (plain name, what the factor does, cap or None, family)
P2_PROPS = {
    "face_strength": ("face compressive strength", "sigma x f", None, "face"),
    "face_modulus": ("face modulus", "E x f", None, "face"),
    "face_density": ("face density", "rho_f / f", None, "face"),
    "core_shear_modulus": ("core shear stiffness per density (W shear modulus at fixed density)", "Gc x f", None, "core"),
    "core_density": ("core density at fixed core properties", "rho_c / f", None, "core"),
    "core_tt_modulus": ("core through-thickness modulus", "Ec x f", None, "core"),
    "face_flatness": ("face flatness (CR-1457 waviness parameter K_delta)", "K_delta / f", None, "process"),
    "core_crush": ("core crush strength", "crush x f", None, "core"),
    "cell_size": ("core cell size", "cell / f", None, "core"),
    "sheet_size": ("sheet size (panel dimensions)", "a, b x f", None, "process"),
    "film_mass": ("bond-film areal mass", "film / f", None, "process"),
    "seam_mass": ("seam mass per metre", "seam / f", None, "process"),
    "gamma": ("ANALYSIS: knockdown gamma (handbook 0.20)", "gamma x f, capped at 1", 5.0, "analysis"),
    "wrinkle_Q": ("ANALYSIS: wrinkle coefficient Q (0.33)", "Q x f", 0.82 / 0.33, "analysis"),
}
P3_PROPS = {
    "sic_strength": ("SiC design compressive strength (the tube allowable)", "sigma x f", None, "tube"),
    "sic_modulus": ("SiC modulus", "E x f", None, "tube"),
    "sic_density": ("SiC density", "rho / f", None, "tube"),
    "film_specific_strength": ("film specific strength (allowable over density)", "sigma_film x f", None, "film"),
    "joint_mass": ("end-joint mass (C in m = C N^2 / r)", "C / f", None, "joint"),
    "node_mass": ("node mass (20 g per node)", "m_node / f", None, "joint"),
    "lattice_knockdown": ("ANALYSIS -> lattice precision: global knockdown k (0.2)", "k x f", 5.0, "analysis"),
    "local_knockdown": ("ANALYSIS -> tube wall precision: SP-8007 local gamma", "gamma_local x f", None, "analysis"),
    "straightness": ("member straightness (Perry a0 = L/1000)", "a0 / f", None, "process"),
}


# ----------------------------------------------------------------------------- P2
def p2_best(R, fac, rule="handbook"):
    q = m.p2_apply(m.P2_TODAY, fac)
    q["gamma_rule"] = rule
    return m.p2_optimise(R, q, "019")


def factor_alone(best_fn, prop, f_max=1e4, tol=1e-9):
    """Smallest factor on one property that brings the re-optimised least SF to 1, or 'not alone'."""
    base = best_fn({})
    if base["least"] >= 1.0:
        # already floats: how far the property can fall before SF 1 (factor < 1)
        lo, hi = 1e-4, 1.0
        if best_fn({prop: lo})["least"] >= 1.0:
            return {"alone": True, "factor": None, "slack": "unbounded", "at_factor": base}
        for _ in range(200):
            mid = math.sqrt(lo * hi)
            if best_fn({prop: mid})["least"] >= 1.0:
                hi = mid
            else:
                lo = mid
            if hi / lo - 1.0 < tol:
                break
        return {"alone": True, "factor": hi, "at_factor": best_fn({prop: hi})}
    top = best_fn({prop: f_max})
    if top["least"] < 1.0:
        return {"alone": False, "factor": None, "saturates_at": top["least"], "next_mode": top["governing"],
                "at_f_max": top, "f_max": f_max}
    lo, hi = 1.0, f_max
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if best_fn({prop: mid})["least"] >= 1.0:
            hi = mid
        else:
            lo = mid
        if hi / lo - 1.0 < tol:
            break
    return {"alone": True, "factor": hi, "at_factor": best_fn({prop: hi})}


def p2_scan(R, rule="handbook"):
    out = {}
    fn = lambda fac: p2_best(R, fac, rule)  # noqa: E731
    for prop in P2_PROPS:
        res = factor_alone(fn, prop)
        cap = P2_PROPS[prop][2]
        if res.get("factor") is not None and cap is not None and res["factor"] > cap * (1 + 1e-12):
            res["beyond_cap"] = cap
        out[prop] = res
    return out


# ----------------------------------------------------------------------------- P3
P3_ROWS = {"today": ("kapton", "ti"), "projection": ("zylon", "cfrp")}
RES_P3 = 411.2989440716474


def p3_optimise(q, reserve=RES_P3, s_lo=0.40, s_hi=8.0, ds=0.05, n_t=40, n_ro=240, polish=True):
    """022c's search, finer film grid, then a Nelder-Mead polish in (s, log t, r_o fraction)."""
    s_vals = list(np.round(np.arange(s_lo, s_hi + 1e-9, ds), 6))
    best = None
    while True:
        b = m.p3_grid_search(q, reserve, s_vals, n_t=n_t, n_ro=n_ro)
        if b is None:
            return None
        best = b
        if b["s"] >= s_vals[-1] - ds - 1e-9 and s_vals[-1] < 19.0:
            s_vals = list(np.round(np.arange(s_vals[-1] + ds, s_vals[-1] + 4.0 + 1e-9, ds), 6))
            b2 = m.p3_grid_search(q, reserve, s_vals, n_t=n_t, n_ro=n_ro)
            if b2 is not None and b2["least"] > best["least"]:
                best = b2
                continue
        break
    if not polish:
        return best

    def neg(x):
        s, lt, ro = x
        if s <= 0.2 or s >= 19.5 or ro <= 0.0:
            return 10.0
        ev = m.p3_eval(np.array([s]), np.array([math.exp(lt)]), np.array([ro]), q, reserve)
        v = ev["least"][0]
        if not np.isfinite(v) or math.exp(lt) < q["t_cat"] * (1 - 1e-12):
            return 10.0
        return -float(v)
    x0 = np.array([best["s"], math.log(best["tfilm"]), best["ro"]])
    r = minimize(neg, x0, method="Nelder-Mead",
                 options={"xatol": 1e-10, "fatol": 1e-13, "maxiter": 6000, "maxfev": 12000,
                          "initial_simplex": [x0, x0 + [0.02, 0, 0], x0 + [0, 0.05, 0], x0 + [0, 0, 0.002]]})
    if -r.fun > best["least"]:
        best = {"least": float(-r.fun), "s": float(r.x[0]), "tfilm": float(math.exp(r.x[1])), "ro": float(r.x[2])}
    return best


def p3_best(row, fac, **kw):
    film, joint = P3_ROWS[row]
    q = m.p3_apply(m.P3_TODAY, m.FILMS[film], joint, fac)
    b = p3_optimise(q, **kw)
    if b is None:
        return {"least": -1.0, "governing": "infeasible"}
    full = m.p3_row(q, RES_P3, b["s"], b["tfilm"], b["ro"])
    return full


def p3_scan(row, **kw):
    out = {}
    fn = lambda fac: p3_best(row, fac, **kw)  # noqa: E731
    for prop in P3_PROPS:
        res = factor_alone(fn, prop, f_max=1e3, tol=1e-6)
        cap = P3_PROPS[prop][2]
        if res.get("factor") is not None and cap is not None and res["factor"] > cap * (1 + 1e-12):
            res["beyond_cap"] = cap
        out[prop] = res
    return out
