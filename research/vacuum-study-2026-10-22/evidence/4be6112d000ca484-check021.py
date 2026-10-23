#!/usr/bin/env python3
"""Independent MAINLINE-021 calculation from pinned input data and CR-1457.

No owner program is executed, imported, or used as a numerical oracle.
The owner CARD is the frozen claim; its RESULTS file changed after filing.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial import Polynomial as Poly
from scipy.optimize import brentq, minimize_scalar

HERE = Path(__file__).resolve().parent
UPSTREAM = json.loads((HERE / "snapshots/p014b_inputs.json").read_text())
CORES = UPSTREAM["cores_eligible"]
P = UPSTREAM["p_ext_Pa"]
LIFT = UPSTREAM["lift_kg"]
R = 10.0
NU = UPSTREAM["nu"]
RHO_F = 1850.0
AREA = 4.0 * math.pi * R**2
MASS = (0.95 * LIFT - 100.0) / 1.05
A_FACE = MASS / (2.0 * AREA * RHO_F)
BETA = brentq(lambda z: z**3 + z - 1.0, 0.0, 1.0, xtol=1e-15)
SQRTNU = math.sqrt(1.0 - NU**2)
NAMES = ("gamma", "wrinkle", "strength")
SUBSETS = [s for n in range(4) for s in itertools.combinations(NAMES, n)]


def geometry(core, fraction):
    return A_FACE * (1.0 - fraction), MASS * fraction / (AREA * core["rho"])


def raw(core, fraction, E=303e9):
    """Return SF for unit gamma, unit wrinkle coefficient, and unit strength."""
    tf, tc = geometry(core, np.asarray(fraction))
    h = tf + tc
    stress = P * R / (4.0 * tf)
    sigma0 = E * h / (R * SQRTNU)
    crimp = core["Gc_Pa"] * h**2 / (2.0 * tf * tc)
    vc = sigma0 / crimp
    kc = np.where(vc <= 2.0, 1.0 - vc / 4.0, 1.0 / vc)
    if core["form"] == "honeycomb":
        wrinkle = BETA * np.sqrt(E * core["Ec_Pa"] * tf / tc)
        c0 = 0.33
    else:
        wrinkle = BETA * (E * core["Ec_Pa"] * core["Gc_Pa"] / (1.0 - NU**2)) ** (1.0 / 3.0)
        c0 = 0.50
    cell = core.get("s_cell_m")
    dimpling = E * (tf / cell) ** 2 / (1.0 - NU**2) / stress if cell else np.full_like(tf, np.inf)
    return dict(
        tf=tf, tc=tc, h=h, stress=stress, Vc=vc, Kc=kc,
        global_raw=sigma0 * kc / stress,
        crimp=crimp / stress,
        crush=np.full_like(tf, 2.0 * core["crush_Pa"] / P),
        wrinkle_per_coefficient=wrinkle / stress,
        dimpling=dimpling, coefficient_today=c0,
        gamma_today=np.where(vc >= 2.0 - 1e-12, 1.0, 0.20),
        gamma_full=0.20 + 0.40 * np.minimum(vc, 2.0),
    )


def modes(core, fraction, E=303e9, sigma=283e6, gamma=None, coefficient=None, conservative=False):
    d = raw(core, fraction, E)
    if gamma is None:
        gamma = 0.20 if conservative else d["gamma_today"]
    if coefficient is None:
        coefficient = d["coefficient_today"]
    return dict(
        global_buckling=float(d["global_raw"] * gamma),
        face_compression=float(sigma / d["stress"]),
        core_shear_crimping=float(d["crimp"]),
        core_crush=float(d["crush"]),
        face_wrinkling=float(d["wrinkle_per_coefficient"] * coefficient),
        intracell_dimpling=float(d["dimpling"]) if np.isfinite(d["dimpling"]) else None,
    )


def usage(required, today, full):
    """Geometric, logarithmic interpolation, inferred from all filed usage values."""
    if abs(full - today) < 1e-12:
        return 0.0 if required <= today * (1.0 + 1e-10) else math.inf
    return max(0.0, math.log(required / today) / math.log(full / today))


def needs(core, fraction, E, strength_today=283e6, strength_full=379.2e6, conservative=False):
    d = raw(core, fraction, E)
    g0 = 0.20 if conservative else float(d["gamma_today"])
    values = {
        "gamma": 1.0 / float(d["global_raw"]),
        "wrinkle": 1.0 / float(d["wrinkle_per_coefficient"]),
        "strength": float(d["stress"]),
    }
    stretches = {
        "gamma": usage(values["gamma"], g0, float(d["gamma_full"])),
        "wrinkle": usage(values["wrinkle"], d["coefficient_today"], 0.82),
        "strength": usage(values["strength"], strength_today, strength_full),
    }
    return values, stretches


def real_roots(poly):
    roots = poly.roots()
    return [float(z.real) for z in roots if abs(z.imag) < 1e-8 and 0 < z.real < 1]


def breakpoints(core, E, strength_today, conservative=False):
    """Every fixed-mode crossing and the gamma discontinuity, using polynomials.

    These partition the feasible fraction domain, so narrow feasible windows do
    not depend on a uniform sampling grid. Extraneous squared roots are harmless:
    each resulting interval is evaluated against the unsquared original modes.
    """
    tf = Poly([A_FACE, -A_FACE])
    tc = Poly([0.0, MASS / (AREA * core["rho"])])
    h = tf + tc
    g = core["Gc_Pa"]
    crimp_numerator = 2.0 * g * h**2 - P * R * tc
    vc_two = 2.0 * E * tf * tc - 2.0 * R * SQRTNU * g * h
    global_stiff = (
        4.0 * E * tf * h / (R**2 * P * SQRTNU)
        - 2.0 * E**2 * tf**2 * tc / (R**3 * P * (1.0 - NU**2) * g)
    )
    global_weak_numerator = (0.20 if conservative else 1.0) * 2.0 * g * h**2 - P * R * tc
    polynomials = [
        crimp_numerator, vc_two, 0.20 * global_stiff - 1.0,
        global_weak_numerator, 4.0 * strength_today * tf - P * R,
    ]
    if core["form"] == "honeycomb":
        polynomials.append(
            16.0 * BETA**2 * 0.33**2 * E * core["Ec_Pa"] * tf**3
            - (P * R) ** 2 * tc
        )
    else:
        w = BETA * 0.50 * (E * core["Ec_Pa"] * g / (1.0 - NU**2)) ** (1.0 / 3.0)
        polynomials.append(4.0 * w * tf - P * R)
    if core.get("s_cell_m"):
        polynomials.append(4.0 * E * tf**3 - P * R * (1.0 - NU**2) * core["s_cell_m"]**2)
    cuts = [1e-10, 1.0 - 1e-10]
    for poly in polynomials:
        cuts.extend(real_roots(poly))
    return sorted(set(cuts))


def is_feasible(core, f, E, strength_today, subset, conservative=False):
    d = modes(core, f, E, strength_today, conservative=conservative)
    fixed = ["core_shear_crimping", "core_crush", "intracell_dimpling"]
    fixed.extend({"gamma": "global_buckling", "wrinkle": "face_wrinkling", "strength": "face_compression"}[n]
                 for n in NAMES if n not in subset)
    return all(d[k] is None or d[k] >= 1.0 - 2e-10 for k in fixed)


def solve_subset(core, subset, E, strength_today, strength_full=379.2e6, conservative=False):
    cuts = breakpoints(core, E, strength_today, conservative)
    feasible_intervals = [
        (lo, hi) for lo, hi in zip(cuts, cuts[1:])
        if is_feasible(core, (lo + hi) / 2.0, E, strength_today, subset, conservative)
    ]

    def objective(x):
        _, u = needs(core, x, E, strength_today, strength_full, conservative)
        return max((u[k] for k in subset), default=0.0)

    candidates = [(objective(x), x) for x in cuts if is_feasible(core, x, E, strength_today, subset, conservative)]
    for lo, hi in feasible_intervals:
        xs = np.linspace(lo, hi, 257)
        ys = [objective(x) for x in xs]
        candidates.extend((y, float(x)) for x, y in zip(xs, ys)
                          if is_feasible(core, x, E, strength_today, subset, conservative))
        for j in range(1, len(xs) - 1):
            if ys[j] <= ys[j - 1] and ys[j] <= ys[j + 1] and (ys[j] < ys[j - 1] or ys[j] < ys[j + 1]):
                opt = minimize_scalar(objective, bounds=(xs[j - 1], xs[j + 1]), method="bounded",
                                      options={"xatol": 1e-14})
                if is_feasible(core, opt.x, E, strength_today, subset, conservative):
                    candidates.append((float(opt.fun), float(opt.x)))
    candidates = [(y, x) for y, x in candidates if math.isfinite(y)]
    if not candidates:
        return None
    y, f = min(candidates)
    values, u = needs(core, f, E, strength_today, strength_full, conservative)
    return dict(core=core["name"], tag=core["tag"], fraction=f, max_usage=y,
                feasible_within_named=y <= 1.0 + 1e-9, needed=values, usage=u,
                feasible_intervals=feasible_intervals)


def point(core, f, E, strength_today=283e6, strength_full=379.2e6):
    d = raw(core, f, E)
    needed, u = needs(core, f, E, strength_today, strength_full)
    g = max(float(d["gamma_today"]), needed["gamma"])
    w = max(d["coefficient_today"], needed["wrinkle"])
    s = max(strength_today, needed["strength"])
    return dict(
        core=core["name"], E_Pa=E, fraction=f, tf_m=float(d["tf"]),
        tc_m=float(d["tc"]), h_m=float(d["h"]), Vc=float(d["Vc"]), Kc=float(d["Kc"]),
        branch="shear_crimping" if d["Vc"] >= 2.0 else "stiff_or_moderate",
        masses_kg={"faces": MASS * (1 - f), "core": MASS * f, "joints": 0.05 * MASS,
                   "systems": 100.0, "margin": 0.05 * LIFT, "total": LIFT},
        needed=needed, usage={k: v if math.isfinite(v) else None for k, v in u.items()},
        no_finite_stretch=[k for k, v in u.items() if not math.isfinite(v)],
        gamma_full=float(d["gamma_full"]),
        today=modes(core, f, E, strength_today),
        needed_set=modes(core, f, E, s, g, w),
        full_set=modes(core, f, E, strength_full, float(d["gamma_full"]), 0.82),
        conservative=modes(core, f, E, strength_full, 0.20, 0.82),
    )


def solve_scenario(label, E, strength_today, strength_full=379.2e6):
    rows = []
    for subset in SUBSETS:
        candidates = [v for core in CORES
                      if (v := solve_subset(core, subset, E, strength_today, strength_full)) is not None]
        best = min(candidates, key=lambda v: v["max_usage"]) if candidates else None
        rows.append({"subset": list(subset), "best": best})
    viable = [v for v in rows if v["best"] and v["best"]["feasible_within_named"]]
    least = min(viable, key=lambda v: (len(v["subset"]), v["best"]["max_usage"])) if viable else None
    floating = None
    if least:
        best = least["best"]
        core = next(c for c in CORES if c["name"] == best["core"])
        floating = point(core, best["fraction"], E, strength_today, strength_full)
    return dict(label=label, E_Pa=E, strength_today_Pa=strength_today,
                subsets=rows, least_set=least, floating_point=floating)


def family(core):
    if core["family"] == "aluminium_honeycomb":
        return "aluminium"
    if "aramid" in core["family"]:
        return "aramid"
    return "other"


def best_family(group, E, strength_today=283e6, setting="full", grid_only=False):
    best = None
    for core in CORES:
        if family(core) != group:
            continue
        def objective(f):
            d = raw(core, f, E)
            gamma = float(d["gamma_full"]) if setting == "full" else (0.20 if setting == "conservative" else None)
            sigma = 379.2e6 if setting != "today" else strength_today
            coefficient = 0.82 if setting != "today" else None
            sf = modes(core, f, E, sigma, gamma, coefficient)
            return -min(v for v in sf.values() if v is not None)
        # Independent grid plus every branch crossing, then refine local maxima.
        xs = np.linspace(1.0 / 8000.0, 7999.0 / 8000.0, 7999)
        d = raw(core, xs, E)
        ga = d["gamma_full"] if setting == "full" else (0.20 if setting == "conservative" else d["gamma_today"])
        coeff = 0.82 if setting != "today" else d["coefficient_today"]
        sig = 379.2e6 if setting != "today" else strength_today
        ys = -np.minimum.reduce([d["global_raw"] * ga, sig / d["stress"],
                                d["wrinkle_per_coefficient"] * coeff, d["crimp"],
                                d["crush"], d["dimpling"]])
        j = int(np.argmin(ys))
        candidate = (float(ys[j]), float(xs[j]))
        if not grid_only:
            for j in np.where((ys[1:-1] <= ys[:-2]) & (ys[1:-1] <= ys[2:]))[0] + 1:
                opt = minimize_scalar(objective, bounds=(xs[j-1], xs[j+1]), method="bounded",
                                      options={"xatol": 1e-14})
                candidate = min(candidate, (float(opt.fun), float(opt.x)))
            for f in breakpoints(core, E, strength_today):
                candidate = min(candidate, (objective(f), f))
        if best is None or -candidate[0] > best["least"]:
            f = candidate[1]
            d = raw(core, f, E)
            ga = float(d["gamma_full"]) if setting == "full" else (0.20 if setting == "conservative" else None)
            sf = modes(core, f, E, 379.2e6 if setting != "today" else strength_today, ga,
                       0.82 if setting != "today" else None)
            best = {"core": core["name"], "fraction": f, "least": -candidate[0], "modes": sf,
                    "point": point(core, f, E, strength_today)}
    return best


def main():
    scenarios = []
    for label, E, strength in (
        ("filed E303 strength283", 303e9, 283e6),
        ("filed E303 strength255 sensitivity", 303e9, 255e6),
        ("filed E303 strength345 sheet sensitivity", 303e9, 345e6),
        ("S200F E290 strength283", 290e9, 283e6),
        ("S200F E290 strength255", 290e9, 255e6),
        ("SR200 E290 strength345", 290e9, 345e6),
        ("SR200 lot E293.6 strength379.2", 293.6e9, 379.2e6),
    ):
        if strength == 379.2e6:
            # No strength stretch is needed when starting at the full value.
            full_strength = strength * (1.0 + 1e-9)
        else:
            full_strength = 379.2e6
        print("scenario", label, flush=True)
        result = solve_scenario(label, E, strength, full_strength)
        scenarios.append(result)
        (HERE / "independent-scenarios.json").write_text(json.dumps(scenarios, indent=2, allow_nan=False) + "\n")
        print(json.dumps(result["least_set"]), flush=True)
    families = {}
    for E in (303e9, 290e9):
        for group in ("aluminium", "aramid", "other"):
            for setting in ("today", "full", "conservative"):
                key = f"{E/1e9:g}GPa/{group}/{setting}"
                families[key] = {"grid8000": best_family(group, E, setting=setting, grid_only=True),
                                 "refined": best_family(group, E, setting=setting)}
                print(key, families[key]["grid8000"]["least"], families[key]["refined"]["least"], flush=True)
    output = dict(constants={"p_Pa": P, "lift_kg": LIFT, "area_m2": AREA, "structural_mass_kg": MASS,
                             "rho_face_kg_m3": RHO_F, "nu": NU, "beta": BETA},
                  scenarios=scenarios, families=families)
    (HERE / "CALCULATIONS.json").write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
