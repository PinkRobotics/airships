"""Independent optimization and omitted-mode studies, using only checker code."""

from dataclasses import replace
from datetime import datetime
import json
import math

import check_model as cm


def load(stage, name, grid="equilateral"):
    if stage.startswith("022c_"):
        doc = json.loads((cm.ROOT / "inputs/022c/SAG.json").read_text())
        row = doc[stage.removeprefix("022c_")][name][grid]
    else:
        doc = json.loads((cm.ROOT / "inputs" / (stage + ".json")).read_text())
        row = doc["cases"][name][grid]
    return cm.case_for(name, stage), row


def main():
    started = datetime.now().astimezone().isoformat(timespec="seconds")
    continuous, cap_relaxation, corrections, tensile = {}, {}, {}, {}
    jobs = [
        ("GAMMA", "percent_crush_5"), ("GAMMA", "percent_crush_019"),
        ("GAMMA", "percent_mylar_5"), ("GAMMA", "percent_mylar_019"),
        ("GAMMA", "cfrp_zylon_5"), ("FOLD", "cfrp_zylon_019"),
        ("FOLD", "ti_kapton_5"), ("FOLD", "ti_kapton_019"),
    ]
    jobs += [("022c_cap", name) for name in (
        "projection_5", "projection_019", "mylar_5", "mylar_019",
        "cfrp_zylon_5", "cfrp_zylon_019", "ti_kapton_5", "ti_kapton_019",
    )]
    for stage, name in jobs:
        case, row = load(stage, name)
        refined = cm.refine(case, "equilateral")
        key = stage + "/" + name
        continuous[key] = {
            "published": row, "checker": refined,
            "SF_increase": refined["SF_least"] - row["SF_least"],
            "fractional_increase": refined["SF_least"] / row["SF_least"] - 1,
        }
        print("CONTINUOUS", key, refined["SF_least"], refined["s_m"], flush=True)

    # Open both disputed upper bounds, including s beyond the owner's 8 m band.
    for stage, name in (
        ("GAMMA", "percent_crush_5"), ("GAMMA", "cfrp_zylon_5"),
        ("022c_cap", "projection_5"), ("022c_cap", "cfrp_zylon_5"),
    ):
        case, _ = load(stage, name)
        found = cm.refine(case, "equilateral", top=19.9, cap=1., seed=591)
        key = stage + "/" + name
        cap_relaxation[key] = {
            "bounds": "0.4<=s<=19.9 m; r_o<=min(1 m,s/3)",
            "checker": found,
            "SF_change_from_cap025": found["SF_least"] - continuous[key]["checker"]["SF_least"],
            "within_original_limits": found["s_m"] < 8 and found["r_o_m"] < .25,
        }
        print("RELAXED", key, found["SF_least"], found["s_m"], found["r_o_m"], flush=True)

    # 024 uses total 0/90 thickness: each direction receives only half of it.
    for stage, name in (
        ("GAMMA", "cfrp_zylon_5"), ("FOLD", "cfrp_zylon_019"),
        ("022c_cap", "cfrp_zylon_5"), ("022c_cap", "cfrp_zylon_019"),
    ):
        for grid in ("equilateral", "two_way"):
            case, row = load(stage, name, grid)
            corrected = replace(case, film_direction_factor=.5)
            fixed = cm.score(row["s_m"], row["r_o_m"], row["t_film_m"],
                             corrected, grid, details=True)
            key = "/".join((stage, name, grid))
            entry = {"owner_film_SF": row["SF_film"], "owner_least_SF": row["SF_least"],
                     "corrected_fixed": fixed,
                     "reason": "024 t_total=2*t_direction; original scalar film formula silently gives both directions the entire thickness"}
            if grid == "equilateral":
                entry["corrected_continuous"] = cm.refine(corrected, grid, seed=492)
                print("ZYLON_FIX", key, fixed["SF_least"],
                      entry["corrected_continuous"]["SF_least"], flush=True)
            corrections[key] = entry

    for stage, name in (
        ("GAMMA", "percent_crush_5"), ("GAMMA", "percent_crush_019"),
        ("022c_cap", "projection_5"), ("022c_cap", "projection_019"),
    ):
        case, row = load(stage, name)
        base = cm.score(row["s_m"], row["r_o_m"], row["t_film_m"], case, "equilateral", details=True)
        entry = {"published_limit_stresses": base["reported_limit"],
                 "full_pressure_stresses": base["full_pressure"], "fixed_tensile_screens": []}
        for ft in (0., 7.192e6, 15.586e6, 380e6):
            fixed = cm.score(row["s_m"], row["r_o_m"], row["t_film_m"],
                             replace(case, Ft=ft), "equilateral", details=True)
            entry["fixed_tensile_screens"].append({"Ft_assumed_Pa": ft, "result": fixed})
        if stage == "022c_cap":
            entry["reoptimized_tensile_screens"] = []
            for ft in (15.586e6, 380e6):
                optimized = cm.refine(replace(case, Ft=ft), "equilateral", seed=835)
                entry["reoptimized_tensile_screens"].append({"Ft_assumed_Pa": ft, "result": optimized})
                print("TENSION_FIX", stage, name, ft, optimized["SF_least"], optimized["s_m"], flush=True)
        volume = base["m_tube"] / cm.RHO
        entry["hypothetical_uniform_volume_caps"] = []
        for m in (8, 10):
            vref = .004 * .003 * (.020 + .020 / (m + 1)) / (2 * (m + 1))
            characteristic = 380e6 / math.gamma(1 + 1 / m)
            limit = characteristic * (-math.log1p(-1e-6) * vref / volume)**(1 / m)
            entry["hypothetical_uniform_volume_caps"].append({
                "m": m, "volume_m3": volume, "reference_m3": vref,
                "tensile_cap_Pa": limit, "classification": "PROJECTION from025 hypotheses; actual stressed size and compression law unknown",
            })
        tensile[stage + "/" + name] = entry

    # The 023 sizing law spends a yield and bond allowable at N, not at lambda*N.
    joint = {}
    for stage, name in (("GAMMA", "cfrp_zylon_5"), ("FOLD", "cfrp_zylon_019"),
                        ("022c_cap", "cfrp_zylon_5"), ("022c_cap", "cfrp_zylon_019")):
        _, row = load(stage, name)
        lam = row["SF_least"]
        joint[stage + "/" + name] = {
            "published_frame_multiplier": lam,
            "frozen_joint_capacity_multiplier_under_023_sizing": 1.0,
            "published_joint_mass_kg": row["m_joint"],
            "mass_factor_if_resized_for_reported_multiplier": lam**2,
            "joint_mass_if_resized_at_same_radius_kg": row["m_joint"] * lam**2,
            "extra_mass_if_resized_at_same_radius_kg": row["m_joint"] * (lam**2 - 1),
            "scope": "Conditional sizing-law implication; structural reoptimization must charge changed joint mass. No physical joint qualification implied.",
        }
    result = {
        "classification": "QUESTIONABLE model studies; material and unvalidated structural changes PROJECTION",
        "started_at": started,
        "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "continuous_refinement": continuous, "radius_and_spacing_relaxation": cap_relaxation,
        "zylon_direction_correction": corrections, "tensile_bending": tensile,
        "joint_multiplier_consistency": joint,
        "interpretation": "Published candidate arithmetic is checked separately. A finer numerical maximum is not structural validation.",
    }
    (cm.ROOT / "STUDIES.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print("STUDIES COMPLETE", flush=True)


if __name__ == "__main__":
    main()
