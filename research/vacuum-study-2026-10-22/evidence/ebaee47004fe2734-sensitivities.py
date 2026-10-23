#!/usr/bin/env python3
"""Explicit alternatives to the requested inherited-022c comparison."""
from dataclasses import replace
import json
import math
import time

from scipy.optimize import brentq

import scan

ROOT = scan.ROOT


def run():
    start = time.monotonic()
    main = json.loads((ROOT / "SCAN.json").read_text())["rows"]
    out = {
        "status": "QUESTIONABLE", "complete": False,
        "two_way_square_cell": [], "tensile_projection": [],
        "spacing_instead_of_arc_screen": [], "expanded_search": [],
        "unvalidated_local_bending_diagnostic": [],
    }
    for i, original in enumerate(main):
        case = scan.Case(**original["case"])
        if case.grid != "two_way":
            continue
        # This is a separate geometry sensitivity, not a quiet change to 022c.
        # Square incircle cap or exact linear square membrane; D/Y=rg² under
        # the same unvalidated scalar two-way stiffness closure used by C=4.
        alt = replace(case, square_geometry=True, wave_ratio_DY=1.)
        row = scan.optimize(alt, seed=2450+i, starts=[original["x"]])
        out["two_way_square_cell"].append({
            "primary_key": original["key"], "primary_SF": original["target_multiplier"],
            "change_SF": row["target_multiplier"] - original["target_multiplier"], "result": row})
        print("SQUARE", original["key"], f"{row['target_multiplier']:.10f}", flush=True)

    for i, original in enumerate(main):
        case = scan.Case(**original["case"])
        if case.grid != "equilateral" or case.family not in ("projection", "cfrp_zylon"):
            continue
        for ft in (0., 7.192e6, 380e6):
            alt = replace(case, Ft=ft)
            row = scan.optimize(alt, seed=9460+i+int(ft/1e6), starts=[original["x"]])
            out["tensile_projection"].append({
                "primary_key": original["key"], "primary_SF": original["target_multiplier"],
                "Ft_projection_Pa": ft, "change_SF": row["target_multiplier"] - original["target_multiplier"],
                "result": row})
        print("TENSION", original["key"], flush=True)

    for i, original in enumerate(main):
        case = scan.Case(**original["case"])
        if case.band != "in_band" or not original["in_band_binding"]:
            continue
        alt = replace(case, spacing_screen=True)
        row = scan.optimize(alt, seed=8640+i, starts=[original["x"]])
        out["spacing_instead_of_arc_screen"].append({
            "primary_key": original["key"], "primary_SF": original["target_multiplier"],
            "change_SF": row["target_multiplier"] - original["target_multiplier"], "result": row})
    print("SPACING SCREEN", len(out["spacing_instead_of_arc_screen"]), flush=True)

    for i, original in enumerate(main):
        case = scan.Case(**original["case"])
        if case.branch != "cap" or case.reserve != "5":
            continue
        row = scan.optimize(case, seed=7640+i, starts=[original["x"]],
                            bounds=((.15, 19.9), (.01, 10.), (.001, 5.)))
        out["expanded_search"].append({
            "primary_key": original["key"], "primary_SF": original["target_multiplier"],
            "change_SF": row["target_multiplier"] - original["target_multiplier"], "result": row})
    print("EXPANDED DOMAIN", len(out["expanded_search"]), flush=True)

    for row in main:
        c = row["case"]
        if c["branch"] != "cap" or c["reserve"] != "5" or c["family"] not in ("projection", "cfrp_zylon"):
            continue
        limit_stress = row["gamma"] * .6 * scan.E * row["wall_m"] / row["r_o_m"]
        mean, euler, eta = row["axial_stress_at_pressure_1_Pa"], row["euler_stress_Pa"], row["eta"]
        def demand(lam):
            stress = lam * mean
            return (stress * (1 + eta / (1 - stress / euler)) - limit_stress) / 1e9
        lam = brentq(demand, 0., euler / mean * (1 - 1e-10))
        out["unvalidated_local_bending_diagnostic"].append({
            "primary_key": row["key"], "primary_SF": row["target_multiplier"],
            "diagnostic_multiplier": lam,
            "status": "PROJECTION; applying local axial threshold to amplified compression is NOT a validated interaction law"})

    out["elapsed_seconds"] = time.monotonic() - start
    out["complete"] = True
    (ROOT / "SENSITIVITIES.json").write_text(json.dumps(out, indent=2, allow_nan=False) + "\n")
    print("COMPLETE", {k:len(v) for k,v in out.items() if isinstance(v,list)}, flush=True)


if __name__ == "__main__":
    run()
