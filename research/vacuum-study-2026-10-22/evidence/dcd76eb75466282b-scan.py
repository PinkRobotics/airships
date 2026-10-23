#!/usr/bin/env python3
"""MAINLINE-022d: an independently implemented, coupled P3 search.

All physics, materials and feasible witnesses remain QUESTIONABLE.
No source-seat code is imported or executed. The fixed tensile ceiling is a
PROJECTION, not a measured allowable or an assembly reliability calculation.
"""

from dataclasses import asdict, dataclass, replace
from datetime import datetime
import itertools
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.optimize import differential_evolution, minimize, NonlinearConstraint

ROOT = Path(__file__).resolve().parent
R, P, LIFT = 10.0, 95460.8379139, 4889.44215019
E, RHO, SYSTEMS, NODE = 410e9, 3100.0, 100.0, .02
SURFACE = 4 * math.pi * R**2
RESERVES = {"5": .05 * LIFT, "019": 411.2989440716474}
FT = 15.586e6
FILMS = {
    # density, directional stress allowable after cross-ply charge, total floor
    "projection": (970., 1.5e9, 80e-6),
    "mylar": (1400., 22 * 6894757.293178, 48 * 2.54e-7),
    "kapton": (1420., 115.5e6, 25e-6),
    "zylon": (1560., 3.48e9 / 2, 12e-6),
}
JOINTS = {
    # density, axial compression, adhesive shear (not qualified on SiC)
    "ti": (4430., 827e6, 28.9e6),
    "cfrp": (1550., 1470e6, 28.9e6),
}
FAMILIES = {
    "projection": ("projection", "percent", 3900e6),
    "mylar": ("mylar", "percent", 380e6),
    "ti_kapton": ("kapton", "ti", 3900e6),
    "cfrp_zylon": ("zylon", "cfrp", 3900e6),
}
MODES = ("compression", "euler", "local", "perry", "global", "tension")
BOUNDS = ((.4, 8.), (.03, 2.5), (.001, 5.))  # s, 10*r_o, multiplier


@dataclass(frozen=True)
class Case:
    family: str
    grid: str
    branch: str
    reserve: str
    band: str
    Ft: float = FT
    square_geometry: bool = False
    wave_ratio_DY: float | None = None
    spacing_screen: bool = False

    @property
    def key(self):
        return "/".join((self.branch, self.grid, self.reserve, self.family, self.band))


def square_membrane_coefficient(terms=240):
    """Mean w/(s²/rho) for -laplacian(w)=2/rho, zero on a square.

    Double sine series, positive terms; not source-seat code.
    The finite sum approaches the exact linear membrane value from below.
    """
    odd = np.arange(1., 2 * terms, 2.)
    m, n = odd[:, None], odd[None, :]
    return float(128 / math.pi**6 * np.sum(1 / (m*m*n*n*(m*m+n*n))))


SQUARE_MEAN = square_membrane_coefficient()


def geometry(s, grid):
    if grid == "equilateral":
        faces = SURFACE / (math.sqrt(3) * s*s / 4)
        members, nodes = 1.5 * faces, .5 * faces + 2
        force, coeff = P * R * s / (2 * math.sqrt(3)), 4 * math.sqrt(1.5)
    elif grid == "two_way":
        faces = SURFACE / (s*s)
        members, nodes = 2 * faces, faces + 2
        force, coeff = P * R * s / 2, 4.
    else:
        raise ValueError(grid)
    return members, nodes, force, coeff, 2 * R * math.asin(s / (2 * R))


def sag_mean(s, case):
    curvature_radius = s
    square = case.square_geometry and case.grid == "two_way"
    if case.branch == "membrane":
        return (SQUARE_MEAN if square else 1 / 40) * s*s / curvature_radius
    base = (.5 if square else 1 / (2 * math.sqrt(3))) * s
    # Stable cap crown, then cap volume / circular projected area.
    crown = base*base / (curvature_radius + math.sqrt(curvature_radius**2 - base**2))
    return crown*crown * (curvature_radius - crown / 3) / (base*base)


def score(x, case, *, details=False):
    """Charge film and joints at target lambda before closing the tube mass.

    Three-variable calls use the least film satisfying lambda as starting
    witnesses. The final four-variable search frees the film gauge as well,
    including any effect of tube mass redistribution on the half-wave.
    """
    s, ro10, target = map(float, x[:3])
    ro = ro10 / 10
    film, joint, Fc = FAMILIES[case.family]
    rho_f, sigma_f, floor = FILMS[film]
    members, nodes, force, coeff, length = geometry(s, case.grid)
    film_required = target * P * s / (2 * sigma_f)
    tf = float(x[3]) / 10000 if len(x) == 4 else max(floor, film_required)
    mean_sag = sag_mean(s, case)
    sag = LIFT * 3 * mean_sag / R
    film_mass, node_mass = SURFACE * rho_f * tf, NODE * nodes
    available = LIFT - RESERVES[case.reserve] - sag - SYSTEMS
    if joint == "percent":
        assembly = available / 1.05
        mj = .05 * assembly
        mt = assembly - film_mass - node_mass
        end = mj / (2 * members)
    else:
        rho_j, sigma_j, tau_j = JOINTS[joint]
        joint_C = rho_j / (2 * math.pi * sigma_j * tau_j)
        end = joint_C * (target * force)**2 / ro
        mj = 2 * members * end
        mt = available - film_mass - node_mass - mj
    area_raw = mt / (RHO * members * length)
    solid_area = math.pi * ro*ro
    # Clipping only supplies a finite search penalty for infeasible iterates.
    # Every accepted result checks unclipped area independently.
    area = min(max(area_raw, 1e-14), solid_area * (1 - 1e-12))
    ri = math.sqrt(ro*ro - area / math.pi)
    wall = area / (math.pi * (ro + ri))
    inertia = area * (ro*ro + ri*ri) / 4
    mean = force / area
    euler = math.pi**2 * E * inertia / (area * length*length)
    eta = .001 * length * ro * area / inertia
    phi = (Fc + (1 + eta) * euler) / 2
    perry_stress = Fc * euler / (phi + math.sqrt(max(0., phi*phi - Fc * euler)))
    gamma = .099 + .901 * math.exp(-math.sqrt(ro / wall) / 16)
    b = euler * (eta - 1) + case.Ft
    d = math.sqrt(b*b + 4 * case.Ft * euler)
    tensile_stress = (2 * case.Ft * euler / max(d + b, 1e-300)
                      if b >= 0 else (d - b) / 2)
    values = {
        "compression": Fc / mean,
        "euler": euler / mean,
        "local": gamma * .6 * E * wall / ro / mean,
        "perry": perry_stress / mean,
        "global": .2 * coeff * E * math.sqrt(inertia * area) / (s * R*R * P),
        "tension": tensile_stress / mean,
        "film": 2 * sigma_f * tf / (P * s),
    }
    rg = math.sqrt(inertia / area)
    wave_DY = 1.125 if case.wave_ratio_DY is None else case.wave_ratio_DY
    half_wave = math.pi * math.sqrt(math.sqrt(wave_DY) * rg * R)
    denominator = s if case.spacing_screen else length
    constraints = [values[k] - target for k in MODES]
    constraints += [mt / 1000, (solid_area - area_raw) / solid_area, (s / 3 - ro) * 10]
    if len(x) == 4:
        constraints += [values["film"] - target]
    if case.band == "in_band":
        constraints.append(half_wave / denominator - 1)
    if not details:
        return np.asarray(constraints)
    bindings = [k for k, value in values.items() if abs(value - target) <= 2e-6]
    joint_details = {"type": joint, "strength_status": "UNKNOWN; mass allowance only"}
    if joint != "percent":
        rho_j, sigma_j, tau_j = JOINTS[joint]
        force_j = target * force
        aj = force_j / sigma_j
        overlap = force_j / (2 * math.pi * ro * tau_j)
        joint_details = {
            "type": joint, "strength_status": "PROJECTION; equal-stress axial and bond sizing",
            "design_force_N": force_j, "section_area_m2": aj,
            "overlap_m": overlap, "coefficient_kg_m_per_N2": joint_C,
            "mass_at_multiplier_1_kg": mj / target**2,
            "axial_SF": sigma_j * aj / force,
            "bond_SF": tau_j * 2 * math.pi * ro * overlap / force,
            "density_kg_m3": rho_j, "axial_allowable_Pa": sigma_j, "bond_allowable_Pa": tau_j,
        }
    stresses = {}
    for label, multiplier in (("operating_pressure", 1.), ("at_limit", target)):
        stress = multiplier * mean
        if stress >= euler:
            stresses[label] = {"status": "Euler pole reached; finite stress refused"}
        else:
            bend = stress * eta / (1 - stress / euler)
            stresses[label] = {
                "multiplier": multiplier, "mean_compression_Pa": stress,
                "bending_Pa": bend, "max_compression_Pa": stress + bend,
                "max_tension_Pa": max(0., bend - stress),
            }
    physical_mass = SYSTEMS + node_mass + mj + mt + film_mass
    result = {
        "case": asdict(case), "key": case.key, "status": "QUESTIONABLE",
        "x": list(map(float, x)), "target_multiplier": target,
        "SF_least": min(values.values()),
        "SF_least_with_sized_joint": min(target, min(values.values())) if joint != "percent" else None,
        "SF": values, "binding_modes": bindings,
        "s_m": s, "r_o_m": ro, "r_i_m": ri, "wall_m": wall, "film_total_m": tf,
        "film_per_direction_m": tf / 2 if film == "zylon" else None,
        "film_required_m": film_required, "film_floor_m": floor,
        "film_floor_active": floor >= film_required,
        "members": members, "nodes": nodes, "member_length_m": length,
        "force_at_pressure_1_N": force, "area_m2": area_raw, "inertia_m4": inertia,
        "tube_volume_m3": mt / RHO, "gamma": gamma, "eta": eta,
        "axial_stress_at_pressure_1_Pa": mean, "euler_stress_Pa": euler,
        "Fc_assumed_Pa": Fc, "Ft_projection_Pa": case.Ft,
        "NASA_L_over_midradius": length / ((ro + ri) / 2),
        "sag_mean_m": mean_sag, "curvature_radius_m": s,
        "mass_kg": {"tube": mt, "film": film_mass, "joint": mj, "nodes": node_mass,
                    "systems": SYSTEMS, "vehicle": physical_mass, "reserve": RESERVES[case.reserve],
                    "sag_lift_loss": sag, "closure": physical_mass + sag + RESERVES[case.reserve]},
        "joint": joint_details, "stresses": stresses,
        "radius_of_gyration_m": rg, "half_wave_D_over_Y_over_rg2": wave_DY,
        "half_wave_m": half_wave, "half_wave_over_spacing": half_wave / s,
        "half_wave_over_member": half_wave / length,
        "passes_member_screen": half_wave / length >= 1 - 2e-8,
        "in_band_binding": case.band == "in_band" and abs(half_wave / denominator - 1) <= 2e-6,
        "constraints": list(map(float, constraints)), "min_constraint": float(min(constraints)),
        "radius_cap_active": ro >= .25 - 1e-7 or ro >= s / 3 - 1e-7,
        "spacing_bound_active": min(abs(s - BOUNDS[0][0]), abs(s - BOUNDS[0][1])) <= 1e-6,
    }
    return result


def objective(x):
    return -x[2]


def optimize(case, *, seed=148, starts=(), run_de=True, bounds=None, free_film=True):
    """DE exploration plus SLSQP constrained refinement; no global certificate."""
    started = time.monotonic()
    film = FAMILIES[case.family][0]
    rho_f, sigma_f, floor = FILMS[film]
    if bounds is None:
        bounds = BOUNDS
    if free_film and len(bounds) == 3:
        upper = (LIFT - SYSTEMS - RESERVES[case.reserve]) / (SURFACE * rho_f)
        bounds = (*bounds, (floor * 10000, upper * 10000))
    def expand(x):
        x = list(map(float, x))
        if free_film and len(x) == 3:
            x.append(10000 * max(floor, x[2] * P * x[0] / (2 * sigma_f)))
        return np.asarray(x)
    cons = lambda x: score(x, case)
    seeds = [expand(x) for x in starts]
    history = []
    if run_de:
        de = differential_evolution(
            objective, bounds, constraints=(NonlinearConstraint(cons, 0, np.inf),),
            seed=seed, maxiter=850, popsize=16, tol=1e-10, atol=1e-11,
            polish=False, updating="immediate",
        )
        seeds.insert(0, de.x)
        history.append({"method": "differential_evolution", "seed": seed,
                        "success": bool(de.success), "message": str(de.message),
                        "iterations": int(de.nit), "objective_evaluations": int(de.nfev),
                        "x": list(map(float, de.x)), "max_constraint_violation": float(de.maxcv)})
    # Deliberately distinct section/spacing starts, in addition to DE and any
    # neighbouring-case witnesses. These are trial points, not assumed feasible.
    seeds += [expand([s, ro * 10, lam]) for s, ro, lam in
              ((.55, .08, .35), (1.6, .10, .65), (3.0, .13, 1.0),
               (6.0, .17, 1.3), (7.8, .22, .7))]
    candidates = []
    for x0 in seeds:
        fit = minimize(objective, x0, method="SLSQP", bounds=bounds,
                       constraints=({"type": "ineq", "fun": cons},),
                       options={"ftol": 2e-12, "maxiter": 800})
        residual = float(min(cons(fit.x)))
        history.append({"method": "SLSQP", "success": bool(fit.success),
                        "message": str(fit.message), "iterations": int(fit.nit),
                        "x": list(map(float, fit.x)), "min_constraint": residual})
        if residual >= -2e-9:
            candidates.append(fit.x)
        if float(min(cons(x0))) >= -2e-9:
            candidates.append(x0)
    if not candidates:
        raise RuntimeError((case.key, history))
    x = max(candidates, key=lambda x: x[2])
    row = score(x, case, details=True)
    row["search"] = {"bounds_s_ro10_lambda_film10000": bounds, "free_film": free_film,
                     "best_found_not_certified_global": True,
                     "elapsed_seconds": time.monotonic() - started, "history": history}
    return row


def cases():
    for branch, grid, reserve, family in itertools.product(
        ("cap", "membrane"), ("equilateral", "two_way"), ("5", "019"), FAMILIES
    ):
        yield Case(family, grid, branch, reserve, "overall")


def run():
    start = time.monotonic()
    rows = []
    old = ROOT / "SEED-SCAN.json"
    seeds = {r["key"]: r for r in json.loads(old.read_text())["rows"]} if old.exists() else {}
    for index, case in enumerate(cases()):
        first = optimize(case, seed=1634 + index,
                         starts=[seeds[case.key]["x"]] if case.key in seeds else [])
        rows.append(first)
        constrained = replace(case, band="in_band")
        starts = [first["x"]]
        if constrained.key in seeds:
            starts.append(seeds[constrained.key]["x"])
        second = optimize(constrained, seed=6823 + index, starts=starts)
        rows.append(second)
        (ROOT / "SCAN.json").write_text(json.dumps({
            "status": "QUESTIONABLE", "complete": len(rows) == 64,
            "elapsed_seconds": time.monotonic() - start, "rows": rows,
        }, indent=2, allow_nan=False) + "\n")
        print(case.key, f"overall={first['target_multiplier']:.10f}",
              f"in_band={second['target_multiplier']:.10f}",
              f"s={second['s_m']:.8f}",
              f"half/L={second['half_wave_over_member']:.8f}", flush=True)


if __name__ == "__main__":
    run()
