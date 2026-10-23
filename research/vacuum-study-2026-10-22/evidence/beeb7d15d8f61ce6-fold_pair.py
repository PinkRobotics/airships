#!/usr/bin/env python3
"""MAINLINE-022b pairings named by the fold order. Does not rewrite GAMMA.json."""
import datetime
import json
import os
import time
from zoneinfo import ZoneInfo

import equilibrium as eq
import floatpoint as fp
import gamma_local as gl

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIGIN_PATH = os.path.join(ROOT, "FOLD_ORIGIN.json")
OUT_PATH = os.path.join(ROOT, "FOLD.json")
CARD_PATH = os.path.join(ROOT, "FOLD.md")
ZONE = ZoneInfo("America/Los_Angeles")


def g(x):
    return format(x, ".12g")


def main():
    if os.path.exists(OUT_PATH):
        raise SystemExit("FOLD.json is the measured pair run. Not recomputing.")
    t0 = time.monotonic()
    wall0 = datetime.datetime.now(ZONE)
    if os.path.exists(ORIGIN_PATH):
        origin = json.loads(open(ORIGIN_PATH, encoding="utf-8").read())
        print("FOLD_ORIGIN exists; not restamping", origin["origin_local"])
    else:
        origin = {"origin_local": wall0.isoformat(timespec="microseconds")}
        fp.atomic_write(ORIGIN_PATH, json.dumps(origin, indent=1) + "\n")
        print("FOLD_ORIGIN", origin["origin_local"])

    top = 8.0
    s_values = gl.values_to(top)
    jobs = (
        ("ti_kapton_5", gl.KAPTON, fp.SIG_CRUSH, eq.RESERVE_5, "ti"),
        ("ti_kapton_019", gl.KAPTON, fp.SIG_CRUSH, eq.RESERVE_OPT, "ti"),
        ("cfrp_zylon_019", gl.ZYLON, fp.SIG_CRUSH, eq.RESERVE_OPT, "cfrp"),
        ("cfrp_kapton_019", gl.KAPTON, fp.SIG_CRUSH, eq.RESERVE_OPT, "cfrp"),
    )
    cases = {}
    while top <= 20.0:
        s_values = gl.values_to(top)
        cases = {}
        edge = False
        for label, film, sigma, reserve, kind in jobs:
            found = gl.scan(film, sigma, reserve, s_values, kind)
            cases[label] = found
            row = found["equilateral"]
            print(label, top, g(row["SF_least"]), row["governing"], "s", row["s_m"], "rt", g(row["rt"]))
            if gl.on_edge(found, top):
                edge = True
                print("EDGE", label)
        if not edge:
            break
        top += 4.0

    elapsed = time.monotonic() - t0
    ended = datetime.datetime.now(ZONE).isoformat(timespec="microseconds")

    def pack_row(row):
        return {k: row[k] for k in row if k != "coeff"}

    doc = {
        "schema": 1,
        "card": "MAINLINE-022b-fold",
        "questionable": True,
        "origin_local": origin["origin_local"],
        "ended_local": ended,
        "elapsed_s": elapsed,
        "s_max_m": s_values[-1],
        "pairs": "today is Ti-6Al-4V sleeve plus Kapton HN. Projection is CFRP wrap plus Zylon HM. 024's 0.374 m cap lift stays pending with 024.",
        "cases": {name: {grid: pack_row(row) for grid, row in block.items()} for name, block in cases.items()},
    }
    fp.atomic_write(OUT_PATH, json.dumps(doc, indent=1) + "\n")
    lines = ["# MAINLINE-022b fold pairs", "", "QUESTIONABLE. Elapsed %s s." % g(elapsed), ""]
    for name, block in cases.items():
        for grid in ("equilateral", "two_way"):
            row = block[grid]
            lines.append(
                "%s %s least %s by %s. s %s m, r_o %s mm, wall %s mm, r/t %s, gamma %s, film %s mm. "
                "Y %s E %s L %s F %s P %s G %s. tubes %s joints %s filmkg %s sag %s. k04 %s by %s."
                % (
                    name, grid, g(row["SF_least"]), row["governing"], g(row["s_m"]), g(row["r_o_m"] * 1e3),
                    g(row["t_w_m"] * 1e3), g(row["rt"]), g(row["gamma"]), g(row["t_film_m"] * 1e3),
                    g(row["SF_yield"]), g(row["SF_euler"]), g(row["SF_local"]), g(row["SF_film"]),
                    g(row["SF_perry"]), g(row["SF_global"]), g(row["m_tube"]), g(row["m_joint"]),
                    g(row["m_film"]), g(row["sag_kg"]), g(row["k04_SF_least"]), row["k04_governing"],
                )
            )
        lines.append("")
    fp.atomic_write(CARD_PATH, "\n".join(lines) + "\n")
    print("elapsed", g(elapsed), "end", ended)


if __name__ == "__main__":
    main()
