"""Independent MAINLINE-022b arithmetic audit.

Owner code is never imported or executed. Equations are independently written
from the stated geometry, mass balances, Euler/bending relations and contracts.
NumPy evaluates the published lattice of candidates; SciPy independently
refines its search. All material/structural inputs remain QUESTIONABLE.
"""

from dataclasses import dataclass, replace
from datetime import datetime
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution, minimize


ROOT = Path(__file__).resolve().parent
R, P, LIFT = 10.0, 95460.8379139, 4889.44215019
E, RHO, SYS, NODE = 410e9, 3100.0, 100.0, .02
SURFACE = 4 * math.pi * R**2
RESERVES = {"5": .05 * LIFT, "019": 411.2989440716474}
FILMS = {
    "projection": (970., 1.5e9, 80e-6),
    "mylar": (1400., 22 * 6894757.293178, 48 * 2.54e-7),
    "kapton": (1420., 115.5e6, 25e-6),
    "zylon": (1560., 3.48e9, 12e-6),
}
JOINTS = {"cfrp": 5.807e-15, "ti": 2.950e-14}
MODES = ("yield", "euler", "local", "film", "perry", "global")


@dataclass(frozen=True)
class Case:
    name: str
    film: str
    Fc: float
    reserve: float
    joint: str = "percent"
    gamma: bool = True
    sag: str = "linear022b"
    film_direction_factor: float = 1.0
    Ft: float | None = None
    gamma_radius: str = "outer"


def case_for(name, stage):
    film = next((f for f in ("mylar", "kapton", "zylon") if f in name), "projection")
    joint = next((j for j in JOINTS if name.startswith(j + "_")), "percent")
    reserve = RESERVES["019" if name.endswith(("019", "optimistic")) else "5"]
    sag = {"022c_cap": "cap024_triangle_both", "022c_membrane": "membrane"}.get(stage, "linear022b")
    return Case(name, film, 380e6 if film == "mylar" else 3900e6,
                reserve, joint, stage != "EQUILIBRIUM", sag=sag)


def cap_loss(s, grid="equilateral"):
    """024's inradius circular-cap approximation; not a full triangle solution."""
    base_ratio = 1 / (2 * math.sqrt(3)) if grid == "equilateral" else .5
    crown_ratio = 1 - math.sqrt(1 - base_ratio**2)
    mean_ratio = crown_ratio**2 * (1 - crown_ratio / 3) / base_ratio**2
    return LIFT * 3 * s * mean_ratio / R


def geometry(s, grid):
    if grid == "equilateral":
        faces = SURFACE / (math.sqrt(3) * s**2 / 4)
        edges, vertices = 1.5 * faces, .5 * faces + 2
        force, coeff = P * R * s / (2 * math.sqrt(3)), 4 * math.sqrt(1.5)
    elif grid == "two_way":
        faces = SURFACE / s**2
        edges, vertices = 2 * faces, faces + 2
        force, coeff = P * R * s / 2, 4.
    else:
        raise ValueError(grid)
    return edges, vertices, force, coeff, 2 * R * np.arcsin(s / (2 * R))


def score(s, ro, tf, case, grid, *, details=False):
    """Exact annulus and mass balance; independent stable quadratic roots."""
    s, ro, tf = np.asarray(s), np.asarray(ro), np.asarray(tf)
    edges, vertices, force, coeff, length = geometry(s, grid)
    rho_f, sigma_f, _ = FILMS[case.film]
    film_mass, node_mass = SURFACE * rho_f * tf, NODE * vertices
    if case.sag == "linear022b":
        sag = LIFT * s / (16 * R)
    elif case.sag == "cap024":
        sag = cap_loss(s, grid)
    elif case.sag == "cap024_triangle_both":
        sag = cap_loss(s, "equilateral")
    elif case.sag == "membrane":
        sag = LIFT * 3 * s / (40 * R)
    else:
        raise ValueError(case.sag)
    vehicle = LIFT - case.reserve - sag
    if case.joint == "percent":
        assembly = (vehicle - SYS) / 1.05
        joint_mass = .05 * assembly
        tube_mass = assembly - film_mass - node_mass
        end_mass = joint_mass / (2 * edges)
    else:
        end_mass = JOINTS[case.joint] * force**2 / ro
        joint_mass = 2 * edges * end_mass
        tube_mass = vehicle - SYS - film_mass - node_mass - joint_mass
    area = tube_mass / (RHO * edges * length)
    valid = (tube_mass > 0) & (area > 0) & (ro**2 > area / np.pi)
    with np.errstate(invalid="ignore", divide="ignore"):
        ri = np.sqrt(np.maximum(0, ro**2 - area / np.pi))
        wall = area / (np.pi * (ro + ri))
        inertia = area * (ro**2 + ri**2) / 4
        mean = force / area
        euler = np.pi**2 * E * inertia / (area * length**2)
        eta = .001 * length * ro * area / inertia
        phi = (case.Fc + (1 + eta) * euler) / 2
        compression = case.Fc * euler / (
            phi + np.sqrt(np.maximum(0, phi**2 - case.Fc * euler)))
        radius = ro if case.gamma_radius == "outer" else (ro + ri) / 2
        gamma = .099 + .901 * np.exp(-np.sqrt(radius / wall) / 16) if case.gamma else 1.0
        local_ideal = .6 * E * wall / ro / mean
        values = {
            "yield": case.Fc / mean,
            "euler": euler / mean,
            "local": gamma * local_ideal,
            "film": 2 * sigma_f * case.film_direction_factor * tf / (P * s),
            "perry": compression / mean,
            "global": .2 * coeff * E * np.sqrt(inertia * area) / (s * R**2 * P),
        }
        if case.Ft is not None:
            b = euler * (eta - 1) + case.Ft
            d = np.sqrt(b**2 + 4 * case.Ft * euler)
            tensile_limit = np.where(
                b >= 0, 2 * case.Ft * euler / np.maximum(d + b, 1e-300),
                (d - b) / 2)
            values["tension"] = tensile_limit / mean
        least = np.minimum.reduce(np.broadcast_arrays(*values.values()))
        least = np.where(valid & np.isfinite(least), least, -1e6)
    if not details:
        return least
    row = {
        "nodes": vertices, "members": edges, "n_coef": force / P,
        "m_nodes": node_mass, "m_film": film_mass, "m_joint": joint_mass,
        "m_tube": tube_mass, "m_end": end_mass, "reserve": case.reserve + sag,
        "sag_kg": sag, "vehicle": vehicle, "s_m": s, "r_o_m": ro,
        "t_film_m": tf, "t_w_m": wall, "rt": ro / wall,
        "A_m2": area, "I_m4": inertia, "length_m": length, "N_N": force,
        "sigma_axial_Pa": mean, "k": .2, "gamma": gamma,
        "SF_local_gamma1": local_ideal, "SF_least": least,
        "eta": eta, "Euler_stress_Pa": euler,
        "mass_closure_kg": SYS + node_mass + joint_mass + tube_mass + film_mass + sag + case.reserve,
        "radius_cap_fraction": ro / min(.25, float(s) / 3),
        "NASA_L_over_midradius": length / ((ro + ri) / 2),
    }
    row.update({"SF_" + name: value for name, value in values.items()})
    row = {k: float(v) for k, v in row.items()}
    row["governing"] = min(values, key=lambda name: (float(values[name]), name))
    modes4 = {k: float(v) * (2 if k == "global" else 1) for k, v in values.items()}
    row["k04_governing"] = min(modes4, key=lambda name: (modes4[name], name))
    row["k04_SF_least"] = min(modes4.values())
    row["k04_SF_global"] = modes4["global"]
    row["on_ro_cap_0_25"] = row["r_o_m"] >= .249
    for label, multiplier in (("full_pressure", 1.), ("reported_limit", row["SF_least"])):
        stress = row["sigma_axial_Pa"] * multiplier
        if stress >= row["Euler_stress_Pa"]:
            row[label] = {"status": "Euler pole reached; finite elastic stress refused"}
        else:
            bend = stress * row["eta"] / (1 - stress / row["Euler_stress_Pa"])
            row[label] = {
                "pressure_multiplier": multiplier, "mean_compression_Pa": stress,
                "bending_Pa": bend, "maximum_compression_Pa": stress + bend,
                "opposite_signed_compression_Pa": stress - bend,
                "maximum_tension_Pa": max(0., bend - stress),
            }
    return row


def film_grid(case):
    rho, _, lower = FILMS[case.film]
    assembly = (LIFT - SYS - case.reserve) / 1.05
    upper = .75 * assembly / (SURFACE * rho)
    return lower * (upper / lower)**(np.arange(12) / 11)


def grid_reproduction(case, grid, top=8., radius_cap=.25):
    """Recreate specified candidate coordinates, independently score all of them."""
    s = np.round(np.arange(.4, top + .025, .05), 3)[:, None, None]
    tf = film_grid(case)[None, :, None]
    edges, vertices, force, _, length = geometry(s, grid)
    rho_f = FILMS[case.film][0]
    sag = LIFT * s / (16 * R)
    if case.sag == "membrane":
        sag = LIFT * 3 * s / (40 * R)
    elif case.sag != "linear022b":
        sag = cap_loss(s, grid if case.sag == "cap024" else "equilateral")
    available = LIFT - case.reserve - sag - SYS
    film_mass, node_mass = SURFACE * rho_f * tf, NODE * vertices
    maximum = np.minimum(radius_cap, s / 3)
    if case.joint == "percent":
        tube_hi = available / 1.05 - film_mass - node_mass
    else:
        tube_hi = available - film_mass - node_mass - 2 * edges * JOINTS[case.joint] * force**2 / maximum
    minimum = np.sqrt(np.maximum(tube_hi, 0) / (RHO * edges * length * np.pi)) * 1.0001
    radii = minimum + (maximum - minimum) * np.linspace(0, 1, 480)[None, None, :]
    scores = score(s, radii, tf, case, grid)
    scores = np.where((tube_hi > 0) & (maximum > minimum), scores, -1e6)
    index = np.unravel_index(int(np.argmax(scores)), scores.shape)
    selected = (float(s[index[0], 0, 0]), float(radii[index]), float(tf[0, index[1], 0]))
    row = score(*selected, case, grid, details=True)
    row["coordinates"] = {"s_index": int(index[0]), "film_index": int(index[1]), "radius_index": int(index[2])}
    row["candidates_evaluated"] = int(scores.size)
    return row


def refine(case, grid, *, top=8., cap=.25, seed=148,
           iterations=700, popsize=16):
    """Independent continuous search with no owner's code or candidate reuse."""
    lower = FILMS[case.film][2]
    upper = (LIFT - SYS - case.reserve) / (SURFACE * FILMS[case.film][0])
    bounds = [(.4, top), (.003, cap), (math.log(lower), math.log(upper))]

    def objective(x):
        s, ro, logt = x
        if ro >= s / 3:
            return 1e3 + ro - s / 3
        return -float(score(s, ro, math.exp(logt), case, grid))

    result = differential_evolution(
        objective, bounds, seed=seed, popsize=popsize, maxiter=iterations,
        tol=2e-10, atol=1e-10, polish=False, updating="immediate",
    )
    polished = minimize(objective, result.x, method="Nelder-Mead",
                         options={"maxiter": 3000, "xatol": 1e-10, "fatol": 1e-11})
    x = result.x
    if (all(lo <= xi <= hi for xi, (lo, hi) in zip(polished.x, bounds))
            and polished.fun < result.fun):
        x = polished.x
    row = score(float(x[0]), float(x[1]), math.exp(x[2]), case, grid, details=True)
    row["search"] = {
        "method": "independent differential evolution plus bounded-accepted simplex",
        "seed": seed, "spacing_upper_m": top, "outer_radius_upper_m": cap,
        "evaluations": int(result.nfev + polished.nfev),
        "DE_success": bool(result.success), "DE_message": str(result.message),
        "certified_global_optimum": False,
    }
    return row


def compare(table, row_id, expected, observed, comparisons):
    for key, value in expected.items():
        if key not in observed:
            continue
        other = observed[key]
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            passed = math.isclose(value, other, rel_tol=2e-9, abs_tol=2e-10)
            delta = other - value
            comparisons.append({
                "table": table, "row": row_id, "field": key, "owner": value,
                "checker": other, "delta": delta, "passed": passed,
            })
        elif isinstance(value, (str, bool)):
            comparisons.append({
                "table": table, "row": row_id, "field": key, "owner": value,
                "checker": other, "passed": value == other,
            })


def auxiliary():
    s, h, ro, wall = 1.1, .121, .1825, .000240
    ri = ro - wall
    area = math.pi * wall * (ro + ri)
    inertia = area * (ro**2 + ri**2) / 4
    sag = (s / 2)**2 / (R + math.sqrt(R**2 - (s / 2)**2))
    force = P * R * s / (2 * math.sqrt(3))
    moment = force * (h - sag)
    axial, bend = force / area, moment * ro / inertia
    crown = {
        "sagitta_m": sag, "N_N": force, "moment_Nm": moment,
        "sigma_axial_Pa": axial, "sigma_bending_Pa": bend,
        "yield_SF_before_bending": 380e6 / axial,
        "yield_SF_with_bending": 380e6 / (axial + bend),
    }
    s, ro = 2.04, .123688362374
    edges, _, force, _, _ = geometry(s, "equilateral")
    pins = {
        "gamma_rt_140_5": .099 + .901 * math.exp(-math.sqrt(140.5) / 16),
        "m_cfrp_kg": 2 * edges * JOINTS["cfrp"] * force**2 / ro,
        "m_ti_kg": 2 * edges * JOINTS["ti"] * force**2 / ro,
        "N_N": force,
    }
    s, tube = 3., 4140.83666694
    edges, _, force, coeff, length = geometry(s, "equilateral")
    area = tube / (RHO * edges * length)
    radii = np.linspace(math.sqrt(area / math.pi) * 1.0001, .25, 4000)
    ri = np.sqrt(radii**2 - area / math.pi)
    wall = area / (math.pi * (radii + ri))
    inertia = area * (radii**2 + ri**2) / 4
    local = .6 * E * wall / radii * area / force
    glob = .2 * coeff * E * np.sqrt(inertia * area) / (s * R**2 * P)
    index = int(np.argmax(np.minimum(local, glob)))
    rebalance = {
        "SF": float(min(local[index], glob[index])),
        "r_o_m": float(radii[index]), "SF_local": float(local[index]),
        "SF_global": float(glob[index]),
    }
    return {"crown_example": crown, "gamma_pins": pins,
            "fixed_mass_rebalance": rebalance,
            "legacy_N_at_2p04_N": P * R * 2.04 / 2,
            "linear_sag_at_2p04_kg": LIFT * 2.04 / (16 * R),
            "exact_cap_at_2p04_kg": cap_loss(2.04)}


def main():
    comparisons, grids, details = [], {}, {}
    docs = {}
    stages = []
    for table in ("EQUILIBRIUM", "GAMMA", "FOLD"):
        stages.append((table, json.loads((ROOT / "inputs" / (table + ".json")).read_text())))
    sagdoc = json.loads((ROOT / "inputs/022c/SAG.json").read_text())
    stages += [("022c_" + kind, {"cases": sagdoc[kind]}) for kind in ("cap", "membrane")]
    for table, doc in stages:
        docs[table] = doc
        for name, rows in doc["cases"].items():
            case = case_for(name, table)
            for grid, row in rows.items():
                label = "/".join((table, name, grid))
                own = score(row["s_m"], row["r_o_m"], row["t_film_m"], case, grid, details=True)
                compare(table, name + "/" + grid, row, own, comparisons)
                details[label] = own
                rebuilt = grid_reproduction(case, grid)
                compare(table + "_GRID", name + "/" + grid, row, rebuilt, comparisons)
                grids[label] = rebuilt
        print("REPRODUCED", table, len(doc["cases"]) * 2, "rows", flush=True)
    aux = auxiliary()
    compare("EQUILIBRIUM", "crown_example", docs["EQUILIBRIUM"]["crown_example"], aux["crown_example"], comparisons)
    compare("EQUILIBRIUM", "fixed_mass_rebalance", docs["EQUILIBRIUM"]["fixed_mass_rebalance"], aux["fixed_mass_rebalance"], comparisons)
    compare("GAMMA", "pins", docs["GAMMA"]["pins"], aux["gamma_pins"], comparisons)
    cap_mean_ratio = cap_loss(1.) * R / (3 * LIFT)
    sag_pins = {
        "lift_2_m_kg": cap_loss(2.), "lift_4_m_kg": cap_loss(4.),
        "lift_2_04_m_kg": cap_loss(2.04),
        "crown_2_04_m": 2.04 * (1 - math.sqrt(11 / 12)),
        "old_charge_2_m_kg": LIFT * 2 / (16 * R),
        "membrane_over_cap_mean": .025 / cap_mean_ratio,
    }
    compare("022c", "pins", sagdoc["pins"], sag_pins, comparisons)
    aux["022c_sag_pins"] = sag_pins
    prior = docs["EQUILIBRIUM"]["cases"]["carried_5"]["equilateral"]
    gam = .099 + .901 * math.exp(-math.sqrt(prior["rt"]) / 16)
    compare("GAMMA", "prior_equilateral_5_local_with_gamma",
            docs["GAMMA"]["prior_equilateral_5_local_with_gamma"],
            {"s_m": prior["s_m"], "rt": prior["rt"], "gamma": gam,
             "SF_local_gamma1": prior["SF_local"], "SF_local": prior["SF_local"] * gam},
            comparisons)
    result = {
        "classification": "QUESTIONABLE arithmetic audit; all additional material screens PROJECTION",
        "owner_code_executed": False, "owner_code_imported": False,
        "method": "Fresh exact-section/mass equations and stable compression root; vectorized independent recreation of stated candidate grids",
        "comparisons": comparisons, "mismatches": [c for c in comparisons if not c["passed"]],
        "at_published_geometry": details, "independent_grid_optima": grids,
        "auxiliary": aux, "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    (ROOT / "ARITHMETIC.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"comparisons": len(comparisons), "mismatches": len(result["mismatches"]),
                      "rows": len(details), "output": str(ROOT / "ARITHMETIC.json")}), flush=True)


if __name__ == "__main__":
    main()
