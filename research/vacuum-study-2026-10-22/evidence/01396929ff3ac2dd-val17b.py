#!/usr/bin/env python3
"""Reproduction checks for model17b before anything new: 028, 021b and 022c."""
import json
import math
import sys

import numpy as np

import model17b as m

WS = "unpublished-local-ref:7a5bf1cec24b249e"
R028 = f"{WS}/ref-70f7af6d0a8d64c42272/.ship/work/outputs/vacuum-mainline028-p2-joining-1020/RESULTS.json"
R21B = f"{WS}/ref-4189c1615990eb515921/.ship/work/outputs/vacuum-mainline021b-floating-point-on-019-budget-1020/RESULTS.json"
SAG = f"{WS}/ref-2543c559b19ffce7dfdd/.ship/work/outputs/vacuum-mainline022-p3-optimistic-floating-point-1020/SAG.json"


def checks(verbose=True):
    out = []

    def rec(name, mine, theirs, tol):
        ok = abs(mine - theirs) <= tol * max(1.0, abs(theirs))
        out.append({"check": name, "mine": mine, "theirs": theirs, "tol": tol, "ok": ok})
        if verbose:
            print(("PASS " if ok else "FAIL ") + name, mine, theirs)

    # V1: 028 nominal AF 0.015 + 30:1 adhesive scarf, stock envelope, 5% line, 021's needed gamma and Q
    r028 = json.load(open(R028))
    case = next(c for c in r028["cases"] if c["panel"] == "stock_envelope" and c["route"] == "af015_scarf")
    want = case["reoptimized_5pct_margin"]
    q = dict(m.P2_TODAY)
    q.update({"sigma": 283e6, "nu": 0.33, "gamma": r028["case"]["gamma_needed"], "Q": r028["case"]["wrinkle_needed"],
              "film": 0.07323641454574575})
    row = m.p2_optimise(10.0, q, line="5pct", fixed30=True, extra_scarf_mode=True, n=2001)
    rec("028 af015/scarf stock: reoptimised least SF", row["least"], want["evaluation"]["least_known_mode_SF"], 2e-6)
    rec("028 af015/scarf stock: core-mass fraction", row["F"], want["core_mass_fraction"], 2e-3)
    # same fraction, every mode and the joining mass
    g = m.p2_geometry(10.0, np.array([want["core_mass_fraction"]]), q, "5pct", fixed30=True)
    ev, aux = m.p2_modes(10.0, g["tf"], g["tc"], q)
    rec("028 at its fraction: tf", float(g["tf"][0]), want["tf_m"], 1e-9)
    rec("028 at its fraction: joining kg", float(g["J"][0]), want["joining"]["total_kg"], 1e-9)
    rec("028 at its fraction: global", float(ev["global_buckling"][0]), want["evaluation"]["sfs"]["global_buckling"], 1e-9)
    rec("028 at its fraction: wrinkle", float(ev["face_wrinkling"][0]), want["evaluation"]["sfs"]["face_wrinkling"], 1e-9)
    rec("028 at its fraction: dimpling", float(ev["intracell_dimpling"][0]),
        want["evaluation"]["sfs"]["intracell_dimpling"], 1e-9)

    # V2: 021b floating point, every mode at the needed values
    fp = json.load(open(R21B))["floating_point"]
    q = dict(m.P2_TODAY)
    q.update({"nu": 0.33, "sigma": 345e6, "gamma": fp["needed_values"]["gamma"], "Q": fp["needed_values"]["wrinkle"]})
    ev, aux = m.p2_modes(10.0, np.array([fp["tf_m"]]), np.array([fp["core_m"]]), q)
    for k in m.P2_MODES:
        rec("021b floating point: " + k, float(ev[k][0]), fp["at_needed_values"]["sfs"][k], 1e-9)
    q["gamma"] = 0.2
    q["Q"] = 0.33
    ev, aux = m.p2_modes(10.0, np.array([fp["tf_m"]]), np.array([fp["core_m"]]), q)
    rec("021b today at its point: least", float(m.p2_least(ev)[0]), fp["today"]["least_SF"], 1e-9)

    # V3: 022c cap rows on 019's reserve, with 022c's own grid
    sag = json.load(open(SAG))
    s_values = [round(0.40 + 0.05 * i, 3) for i in range(int(round((8.0 - 0.40) / 0.05)) + 1)]
    for label, film, joint in (("ti_kapton_019", "kapton", "ti"), ("cfrp_zylon_019", "zylon", "cfrp")):
        want = sag["cap"][label]["equilateral"]
        q = m.p3_apply(m.P3_TODAY, m.FILMS[film], joint, {})
        best = m.p3_grid_search(q, 411.2989440716474, s_values, n_t=12, n_ro=480)
        rec(f"022c {label}: least SF", best["least"], want["SF_least"], 1e-9)
        rec(f"022c {label}: s", best["s"], want["s_m"], 1e-12)
        rec(f"022c {label}: r_o", best["ro"], want["r_o_m"], 1e-9)
        row = m.p3_row(q, 411.2989440716474, want["s_m"], want["t_film_m"], want["r_o_m"])
        for mode in m.P3_MODES:
            rec(f"022c {label} at its point: {mode}", row["modes"][mode], want["SF_" + mode], 1e-9)
        rec(f"022c {label} at its point: sag kg", row["sag"], want["sag_kg"], 1e-9)
    return out


if __name__ == "__main__":
    res = checks()
    bad = [r for r in res if not r["ok"]]
    print(len(res), "checks,", len(bad), "failed")
    sys.exit(1 if bad else 0)
