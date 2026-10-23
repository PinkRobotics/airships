"""Claim comparisons, independent grid cross-check, and source sensitivities."""
import json
import math
from datetime import datetime

import numpy as np

import check021 as c


def core(name):
    return next(row for row in c.CORES if row["name"] == name)


def subset_grid(E, strength_today, n=4000):
    xs = np.arange(1, n, dtype=float) / n
    best = {s: None for s in c.SUBSETS}
    for material in c.CORES:
        d = c.raw(material, xs, E)
        sf = {
            "gamma": d["global_raw"] * d["gamma_today"],
            "wrinkle": d["wrinkle_per_coefficient"] * d["coefficient_today"],
            "strength": strength_today / d["stress"],
        }
        fixed = (d["crimp"] >= 1) & (d["crush"] >= 1) & (d["dimpling"] >= 1)
        u = {}
        with np.errstate(divide="ignore", invalid="ignore"):
            u["gamma"] = np.where(
                d["gamma_full"] > d["gamma_today"],
                np.maximum(0, np.log(1 / sf["gamma"]) / np.log(d["gamma_full"] / d["gamma_today"])),
                np.where(sf["gamma"] >= 1, 0, np.inf),
            )
            u["wrinkle"] = np.maximum(0, np.log(1 / sf["wrinkle"]) / math.log(.82 / d["coefficient_today"]))
            u["strength"] = np.maximum(0, np.log(1 / sf["strength"]) / math.log(379.2e6 / strength_today))
        for subset in c.SUBSETS:
            mask = fixed.copy()
            for name in c.NAMES:
                if name not in subset:
                    mask &= sf[name] >= 1
            target = np.maximum.reduce([u[name] for name in subset]) if subset else np.zeros_like(xs)
            target = np.where(mask, target, np.inf)
            i = int(np.argmin(target))
            if math.isfinite(target[i]) and (best[subset] is None or target[i] < best[subset]["usage"]):
                best[subset] = {"core": material["name"], "fraction": float(xs[i]), "usage": float(target[i])}
    return [{"subset": list(subset), "best": best[subset]} for subset in c.SUBSETS]


def positive_modes(point):
    return min(x for x in point["needed_set"].values() if x is not None)


main_core = core("Hexcel CR-III 5056 3/8-1.0")
al = core("Hexcel CR-III 5056 1/4-1.6")
ar = core("Hexcel HRH-10-4.8-32")
validation = []
expected_009d = {
    "global_buckling": .6170447855269701,
    "face_compression": .771940448044521,
    "core_shear_crimping": 6.329757041733213,
    "core_crush": 7.222602947804261,
    "face_wrinkling": .6170619661451509,
    "intracell_dimpling_uniaxial": 19.494913735632846,
}
mine = c.modes(al, .30075)
mine["intracell_dimpling_uniaxial"] = 2 * mine["intracell_dimpling"]
for name, target in expected_009d.items():
    relative = abs(mine[name] - target) / target
    assert relative < 1e-11
    validation.append({"row": "009d", "field": name, "reported": target,
                       "independent": mine[name], "relative_error": relative, "status": "PASS"})
sealed = json.loads((c.HERE / "snapshots/p009c5_point.json").read_text())["optimum"]
mine = c.modes(ar, sealed["core_mass_fraction"])
for name, target in sealed["modes_at_0.20_design_wrinkle"].items():
    relative = abs(mine[name] - target) / target
    assert relative < 1e-11
    validation.append({"row": "009c-5 held geometry", "field": name, "reported": target,
                       "independent": mine[name], "relative_error": relative, "status": "PASS"})
kd = .2 / c.modes(al, .30075)["global_buckling"]
assert abs(kd - .3241255816288854) < 1e-12
validation.append({"row": "009d kd needed", "independent": kd, "status": "PASS"})
assert abs(c.BETA**3 + c.BETA - 1) < 1e-14
validation.append({"row": "equibiaxial wrinkle interaction", "residual": c.BETA**3 + c.BETA - 1,
                   "independent": c.BETA, "status": "PASS"})

scenarios = json.loads((c.HERE / "CALCULATIONS.json").read_text())["scenarios"]
for result in scenarios:
    p = result["floating_point"]
    if p is not None:
        least = positive_modes(p)
        assert least >= 1 - 1e-8, (result["label"], least)
        validation.append({"row": result["label"], "test": "all six needed-set modes >= 1",
                           "least": least, "status": "PASS"})

claims = {
    "filed_main_f0.094_E303": c.point(main_core, .094, 303e9),
    "filed_main_f0.094_E290": c.point(main_core, .094, 290e9),
    "filed_S255_aramid_f0.30475": c.point(ar, .30475, 303e9, 255e6),
    "filed_SR200_gamma_only_f0.18275": c.point(al, .18275, 303e9, 345e6),
    "same_SR200_geometry_E290": c.point(al, .18275, 290e9, 345e6),
    "filed_full_aluminium_f0.115": c.point(main_core, .115, 303e9),
    "filed_full_aramid_f0.308": c.point(ar, .308, 303e9),
    "filed_full_other_f0.21875": c.point(core("Hexcel HFT fiberglass 3/16-2.0"), .21875, 303e9),
}
grids = {}
for E, strength in ((303e9, 283e6), (303e9, 255e6), (303e9, 345e6), (290e9, 283e6), (290e9, 345e6)):
    label = f"E{E/1e9:g}-sigma{strength/1e6:g}"
    grids[label] = subset_grid(E, strength)

# Source-consistent SR-200 changes E together with its strength. At any level
# of the strength optimism, use the weaker in-plane measured modulus.
coupled = []
for subset in c.SUBSETS:
    E = 293.6e9 if "strength" in subset else 290e9
    choices = [row for material in c.CORES
               if (row := c.solve_subset(material, subset, E, 255e6)) is not None]
    best = min(choices, key=lambda v: v["max_usage"]) if choices else None
    coupled.append({"subset": list(subset), "E_Pa": E, "best": best})

# The CR-194164 sheet is orthotropic. This is explicitly an isotropic
# sensitivity only, not a claim to solve its orthotropic shell problem.
c.NU = .0768
c.SQRTNU = math.sqrt(1 - c.NU**2)
poisson_sensitivity = {
    "tag": "QUESTIONABLE isotropic surrogate; an orthotropic calculation remains open",
    "source": "NASA CR-194164 Table 2, nu12=.0768, nu21=.0752",
    "filed_geometry_E290_nu0.0768": c.point(main_core, .094, 290e9),
    "same_geometry_carry_gamma_wrinkle": c.modes(
        main_core, .094, 290e9, 283e6, .5791494489601828, .36264164430889406
    ),
    "main_reoptimised": c.solve_scenario("E290 sigma283 nu.0768 sensitivity", 290e9, 283e6),
}
result = {
    "validation": validation, "filed_geometry_checks": claims, "grid4000_subsets": grids,
    "grade_coupled_subsets_S200F255_to_SR200": coupled,
    "poisson_sensitivity": poisson_sensitivity,
    "checked_at": datetime.now().astimezone().isoformat(timespec="seconds"),
}
(c.HERE / "SUPPLEMENTAL.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
print(json.dumps({"validation_passes": len(validation), "poisson_sensitivity_least_set":
                  poisson_sensitivity["main_reoptimised"]["least_set"]}, indent=2))
