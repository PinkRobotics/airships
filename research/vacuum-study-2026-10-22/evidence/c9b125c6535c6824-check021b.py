#!/usr/bin/env python3
"""Independent MAINLINE-021b arithmetic. No owner program is read or run.

The core catalogue supplies material inputs only. Equations come from CR-1457
and the declared 019 mass takeoff. Owner results are comparison targets, never
numerical inputs to the independent search.
"""
from __future__ import annotations

import itertools
import json
import math
import time
from pathlib import Path

import numpy as np
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
CAT = json.loads((HERE / "snapshots/014b_inputs.json").read_text())
BUDGET = json.loads((HERE / "snapshots/019_inputs.json").read_text())
CORES = [c for c in CAT["cores_eligible"] if c["form"] == "honeycomb"]
R = BUDGET["case"]["radius_m"]
P = BUDGET["case"]["p0_Pa"]
LIFT = BUDGET["case"]["lift0_kg"]
T0 = BUDGET["case"]["T0_K"]
NU = CAT["nu"]
RHO = 1850.0
AREA = 4 * math.pi * R**2
OPT = BUDGET["scenarios"]["optimistic"]
BETA = brentq(lambda z: z**3 + z - 1, 0, 1, xtol=1e-15)
W0 = 2 * (24 * .0254) * (72 * .0254) / ((24 + 72) * .0254)
W1 = 4.0
F0, F1 = .030, .015
FILM_CONV = .45359237 / .3048**2
NAMES = ["O1_gamma", "O2_wrinkle", "O3_face_strength", "O4_panel_size", "O5_bond_film"]
FIXED_LINES = {
    "systems_excess_kg": max(0, OPT["vacuum_hardware_kg"] + OPT["power_package_kg"] + OPT["controls_kg"] - 100),
    "retained_water_kg": AREA * OPT["water_film_m"] * OPT["rho_water_kg_m3"],
    "contamination_kg": OPT["contamination_kg"],
    "temperature_pressure_loss_kg": LIFT * (1 - (1 - OPT["pressure_swing_fraction"]) * T0 / (T0 + OPT["temperature_rise_K"])),
    "humidity_loss_kg": LIFT * .378 * OPT["water_vapour_Pa"] / P * T0 / (T0 + OPT["temperature_rise_K"]),
    "internal_gas_kg": LIFT * OPT["pressure_internal_fraction_of_p0"],
    "payload_kg": OPT["payload_kg"],
}
FIXED = sum(FIXED_LINES.values())
CARR = {k: np.array([c[k] for c in CORES])[:, None]
        for k in ["rho", "Ec_Pa", "Gc_Pa", "crush_Pa", "s_cell_m"]}
MODE_NAMES = ["global_buckling", "face_compression", "core_shear_crimping",
              "core_crush", "face_wrinkling", "intracell_dimpling"]


def family(core):
    if core["family"] == "aluminium_honeycomb":
        return "aluminium"
    return "aramid" if "aramid" in core["family"] else "other"


def mass(core, f, w, film, fixed=FIXED):
    """Solve both linear allowance branches, then take the smaller ceiling."""
    coeff = (2 / w) * (OPT["strip_width_m"] * (1 - f)
                       + OPT["core_splice_width_m"] * OPT["rho_splice_kg_m3"] * f / core["rho"])
    seam_adh = (2 * AREA / w) * 2 * OPT["strip_width_m"] * OPT["seam_adhesive_m"] * OPT["rho_adhesive_kg_m3"]
    films = 2 * AREA * film * FILM_CONV
    s = np.minimum((LIFT - 100 - fixed) / 1.05,
                   (LIFT - 100 - fixed - seam_adh - films) / (1 + coeff))
    seams = coeff * s + seam_adh
    excess = np.maximum(0, seams + films - .05 * s)
    return s, seams, films, fixed + excess


def raw(core, f, w=W0, film=F0, E=290e9, nu=NU, fixed=FIXED, structural=None):
    f = np.asarray(f)
    if structural is None:
        s, seams, films, reserve = mass(core, f, w, film, fixed)
    else:
        s = np.broadcast_to(structural, np.broadcast_shapes(np.shape(f), np.shape(core["rho"])))
        seams = films = reserve = np.nan
    tf = s * (1 - f) / (2 * AREA * RHO)
    tc = s * f / (AREA * core["rho"])
    h = tf + tc
    stress = P * R / (4 * tf)
    sigma0 = E * h / (R * np.sqrt(1 - nu**2))
    sigma_crimp = core["Gc_Pa"] * h**2 / (2 * tf * tc)
    vc = sigma0 / sigma_crimp
    kc = np.where(vc <= 2, 1 - vc / 4, 1 / vc)
    return dict(
        S=s, seams=seams, films=films, reserve=reserve, tf=tf, tc=tc, h=h,
        stress=stress, Vc=vc, Kc=kc,
        global_raw=kc * sigma0 / stress,
        crimp=sigma_crimp / stress,
        crush=np.broadcast_to(2 * core["crush_Pa"] / P, np.shape(tf)),
        wrinkle_raw=BETA * np.sqrt(E * core["Ec_Pa"] * tf / tc) / stress,
        dimpling=E * (tf / core["s_cell_m"])**2 / ((1 - nu**2) * stress),
        gamma_today=np.where(vc >= 2, 1., .2),
        gamma_full=.2 + .4 * np.minimum(vc, 2),
    )


def modes(d, gamma=None, wrinkle=.33, strength=345e6):
    if gamma is None:
        gamma = d["gamma_today"]
    return [d["global_raw"] * gamma, strength / d["stress"], d["crimp"],
            d["crush"], wrinkle * d["wrinkle_raw"], d["dimpling"]]


def mode_dict(d, gamma=None, wrinkle=.33, strength=345e6):
    return dict(zip(MODE_NAMES, map(float, modes(d, gamma, wrinkle, strength))))


def usages(d):
    with np.errstate(divide="ignore", invalid="ignore"):
        ug = np.where(d["gamma_full"] > d["gamma_today"],
                      np.maximum(0, np.log(1 / (d["global_raw"] * d["gamma_today"]))
                                 / np.log(d["gamma_full"] / d["gamma_today"])),
                      np.where(d["global_raw"] * d["gamma_today"] >= 1 - 1e-12, 0, np.inf))
    uw = np.maximum(0, np.log(1 / (.33 * d["wrinkle_raw"])) / math.log(.82 / .33))
    us = np.maximum(0, np.log(d["stress"] / 345e6) / math.log(379.2 / 345))
    return [ug, uw, us]


def point(core, f, w, film, nu=NU):
    d = raw(core, f, w, film, nu=nu)
    full = raw(core, f, w, film, E=293.6e9, nu=nu)
    gamma = max(float(d["gamma_today"]), 1 / float(d["global_raw"]))
    coeff = max(.33, 1 / float(d["wrinkle_raw"]))
    strength = max(345e6, float(d["stress"]))
    u = list(map(float, usages(d))) + [math.log(w / W0) / math.log(W1 / W0),
                                      math.log(F0 / film) / math.log(F0 / F1)]
    # Frozen geometry: replace seam length and films without re-solving thickness.
    seams_at_w0 = float(d["seams"]) * w / W0
    reserve_today = FIXED + max(0, seams_at_w0 + 2 * AREA * F0 * FILM_CONV - .05 * float(d["S"]))
    return dict(
        core=core["name"], fraction=f, panel_width_m=w, bond_film_lb_ft2=film,
        tf_m=float(d["tf"]), core_m=float(d["tc"]), h_m=float(d["h"]),
        Vc=float(d["Vc"]), Kc=float(d["Kc"]), stress_Pa=float(d["stress"]),
        masses_kg=dict(faces=float(d["S"] * (1 - f)), core=float(d["S"] * f),
                       joint_allowance_0_05S=float(.05 * d["S"]), joint_seams=float(d["seams"]),
                       joint_bond_films=float(d["films"]), reserve_total=float(d["reserve"]),
                       joint_excess_in_reserve=float(d["reserve"] - FIXED),
                       reserve_fixed_items=FIXED, systems_allowance=100.,
                       total=float(1.05 * d["S"] + 100 + d["reserve"])),
        needed_values=dict(gamma=gamma, wrinkle=coeff, face_strength_Pa=strength),
        usage=dict(zip(NAMES, u)), gamma_full=float(d["gamma_full"]),
        today=mode_dict(d), at_needed_values=mode_dict(d, gamma, coeff, strength),
        at_full_named_set=mode_dict(full, full["gamma_full"], .82, 379.2e6),
        at_full_set_conservative_gamma=mode_dict(full, .2, .82, 379.2e6),
        reserve_at_today_panel_and_film_same_geometry_kg=reserve_today,
    )


def grid_subsets(n=2000, divisions=24, strength_E=290e9):
    """Exhaustive 47-core search on the stated grid; all 32 subsets at once.

    Strength_E=290 reproduces the stated present-grade mechanics. A separate
    run can couple the alternate lot's modulus to selecting its strength.
    """
    f = np.arange(1, n)[None, :] / n
    best = [None] * 32
    for i in range(divisions + 1):
        w = W0 * (W1 / W0)**(i / divisions)
        for j in range(divisions + 1):
            film = F0 * (F1 / F0)**(j / divisions)
            d0 = raw(CARR, f, w, film)
            d1 = raw(CARR, f, w, film, E=strength_E) if strength_E != 290e9 else d0
            for mech in range(8):
                d = d1 if mech & 4 else d0
                u = usages(d)
                good = (d["crimp"] >= 1 - 1e-12) & (d["crush"] >= 1 - 1e-12) & (d["dimpling"] >= 1 - 1e-12)
                objective = np.zeros_like(d["stress"])
                for k in range(3):
                    if mech & (1 << k):
                        objective = np.maximum(objective, u[k])
                    else:
                        good &= u[k] <= 1e-12
                objective = np.where(good, objective, np.inf)
                flat = int(np.argmin(objective))
                ci, fi = np.unravel_index(flat, objective.shape)
                value = float(objective[ci, fi])
                if not math.isfinite(value):
                    continue
                for panel in [0, 8]:
                    if i and not panel:
                        continue
                    for bond in [0, 16]:
                        if j and not bond:
                            continue
                        mask = mech | panel | bond
                        score = max(value, i / divisions if panel else 0, j / divisions if bond else 0)
                        if best[mask] is None or score < best[mask]["max_usage"]:
                            best[mask] = dict(max_usage=score, core=CORES[ci]["name"],
                                              fraction=float(f[0, fi]), panel_width_m=w,
                                              bond_film_lb_ft2=film, i=i, j=j)
        if i % 6 == 0:
            print(f"grid E_strength={strength_E:g}: panel row {i}/{divisions}", flush=True)
    return [dict(subset=[name for k, name in enumerate(NAMES) if mask & (1 << k)],
                 mask=mask, best=row, feasible_within_named=bool(row and row["max_usage"] <= 1 + 1e-10))
            for mask, row in enumerate(best)]


def maximize_minimum(mask, u=1., n=4000, nu=NU, strength_E=290e9, group=None,
                     fixed=FIXED, structural=None, E_override=None, strength_today=345e6):
    """Maximise the weakest mode at a common logarithmic optimism usage.

    Larger panels and lighter films increase structural mass and every scored
    factor. Their optimum is therefore their allowed bound at the chosen u.
    A dense grid locates all local maxima and branch crossings for refinement.
    """
    w = W0 * (W1 / W0)**min(u, 1) if mask & 8 else W0
    film = F0 * (F1 / F0)**min(u, 1) if mask & 16 else F0
    E = E_override if E_override else (strength_E if mask & 4 else 290e9)
    sigma = strength_today * (379.2e6 / strength_today)**u if mask & 4 else strength_today
    coeff = .33 * (.82 / .33)**u if mask & 2 else .33

    def score(core, f):
        d = raw(core, f, w, film, E=E, nu=nu, fixed=fixed, structural=structural)
        gamma = d["gamma_today"] * (d["gamma_full"] / d["gamma_today"])**u if mask & 1 else d["gamma_today"]
        return np.minimum.reduce(modes(d, gamma, coeff, sigma))

    xs = np.arange(1, n) / n
    all_best = []
    for core in CORES:
        if group and family(core) != group:
            continue
        ys = score(core, xs)
        j = int(np.argmax(ys))
        candidates = [(float(ys[j]), float(xs[j]))]
        peaks = np.nonzero((ys[1:-1] >= ys[:-2]) & (ys[1:-1] >= ys[2:])
                           & ((ys[1:-1] > ys[:-2]) | (ys[1:-1] > ys[2:])))[0] + 1
        for j in peaks:
            opt = minimize_scalar(lambda f: -float(score(core, f)), bounds=(xs[j - 1], xs[j + 1]),
                                  method="bounded", options={"xatol": 2e-14})
            candidates.append((-float(opt.fun), float(opt.x)))
        # Include the exact CR-1457 branch boundary and its two one-sided limits.
        vc = raw(core, xs, w, film, E=E, nu=nu, fixed=fixed, structural=structural)["Vc"] - 2
        for j in np.nonzero(vc[:-1] * vc[1:] < 0)[0]:
            root = brentq(lambda f: float(raw(core, f, w, film, E=E, nu=nu, fixed=fixed,
                                             structural=structural)["Vc"] - 2), xs[j], xs[j + 1])
            for f in [root - 1e-12, root, root + 1e-12]:
                candidates.append((float(score(core, f)), float(f)))
        value, f = max(candidates)
        all_best.append(dict(core=core["name"], least_SF=value, fraction=f,
                             panel_width_m=w, bond_film_lb_ft2=film, E_Pa=E, common_usage=u))
    return sorted(all_best, key=lambda row: row["least_SF"], reverse=True)


def continuous_usage(mask, strength_E=290e9, nu=NU):
    if maximize_minimum(mask, 1., strength_E=strength_E, nu=nu)[0]["least_SF"] < 1:
        return None
    root = brentq(lambda u: maximize_minimum(mask, u, n=1200, strength_E=strength_E,
                                             nu=nu)[0]["least_SF"] - 1, 0., 1., xtol=2e-11)
    best = maximize_minimum(mask, root, n=8000, strength_E=strength_E, nu=nu)[0]
    core = next(c for c in CORES if c["name"] == best["core"])
    return dict(max_usage=root, best=best,
                point=point(core, best["fraction"], best["panel_width_m"], best["bond_film_lb_ft2"], nu))


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, (float, np.floating)) and not math.isfinite(value):
        return None
    if isinstance(value, np.generic):
        return value.item()
    return value


def main():
    start = time.time()
    core = next(c for c in CORES if c["name"] == "Hexcel CR-III 5056 3/8-1.0")
    result = dict(method="Independent declared equations; no owner code execution/import",
                  fixed_lines_kg=FIXED_LINES, fixed_kg=FIXED, beta=BETA,
                  declared_point=point(core, .1586, W0 * (W1 / W0)**(20 / 24), F0))
    result["grid_32"] = grid_subsets()
    result["full_bounds_32"] = []
    for mask in range(32):
        rows = maximize_minimum(mask)
        result["full_bounds_32"].append(dict(mask=mask, best=rows[0], by_core=rows))
    print("32 full-bound searches done", flush=True)
    result["continuous_least_set"] = continuous_usage(1 | 2 | 8)
    result["families"] = {}
    for group in ["aramid", "aluminium", "other"]:
        result["families"][group] = maximize_minimum(31, strength_E=293.6e9, group=group)[0]
        result["families"][group + "_today"] = maximize_minimum(0, group=group)[0]
    result["elapsed_seconds"] = time.time() - start
    (HERE / "CALCULATIONS.json").write_text(json.dumps(clean(result), indent=2, allow_nan=False) + "\n")
    print(json.dumps(clean({k: result[k] for k in ["fixed_kg", "continuous_least_set", "families", "elapsed_seconds"]}), indent=2))


if __name__ == "__main__":
    main()
