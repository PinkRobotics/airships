#!/usr/bin/env python3
"""MAINLINE-022c. Charge 024's inradius-cap lift inside the 022b scan.

Does not rewrite EQUILIBRIUM.json, GAMMA.json, or FOLD.json.
"""
import datetime
import json
import math
import os
import time
from zoneinfo import ZoneInfo

import equilibrium as eq
import floatpoint as fp
import gamma_local as gl

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIGIN_PATH = os.path.join(ROOT, "SAG_ORIGIN.json")
OUT_PATH = os.path.join(ROOT, "SAG.json")
CARD_PATH = os.path.join(ROOT, "SAG.md")
ZONE = ZoneInfo("America/Los_Angeles")
SQRT3 = math.sqrt(3.0)


def g(x):
    return format(x, ".12g")


def crown(s, base):
    return s - math.sqrt(s * s - base * base)


def mean_of_cap(s, h):
    """Spherical-cap mean height. s is the pillow radius, 024's rho."""
    return h * (3.0 * s - h) / (3.0 * (2.0 * s - h))


def cap_geometry(s):
    base = s / (2.0 * SQRT3)
    h = crown(s, base)
    mean = mean_of_cap(s, h)
    lift = fp.L_MASS * 3.0 * mean / fp.R
    return {"crown_m": h, "mean_m": mean, "lift_kg": lift}


def lift_cap(s):
    return cap_geometry(s)["lift_kg"]


def lift_membrane(s):
    """Uniform-tension mean sag s^2/(40 rho) with rho = s."""
    mean = s * s / (40.0 * s)
    return fp.L_MASS * 3.0 * mean / fp.R


def check():
    cap2 = cap_geometry(2.0)
    cap4 = cap_geometry(4.0)
    cap204 = cap_geometry(2.04)
    if abs(cap2["lift_kg"] - 62.9000389203) > 1e-6:
        raise SystemExit("lift at 2 m: %s" % cap2["lift_kg"])
    if abs(cap4["lift_kg"] - 125.800077841) > 1e-6:
        raise SystemExit("lift at 4 m: %s" % cap4["lift_kg"])
    if abs(cap204["lift_kg"] - 64.1580396987) > 1e-6:
        raise SystemExit("lift at 2.04 m: %s" % cap204["lift_kg"])
    if abs(cap204["crown_m"] - 0.0868487001771) > 1e-9:
        raise SystemExit("crown at 2.04 m: %s" % cap204["crown_m"])
    old2 = fp.L_MASS * 2.0 / (16.0 * fp.R)
    ratio = (2.0 / 40.0) / cap2["mean_m"]
    print(
        "checks", "lift2", g(cap2["lift_kg"]), "old2", g(old2),
        "mean2", g(cap2["mean_m"]), "ratio", g(ratio),
    )
    return {
        "lift_2_m_kg": cap2["lift_kg"],
        "lift_4_m_kg": cap4["lift_kg"],
        "lift_2_04_m_kg": cap204["lift_kg"],
        "crown_2_04_m": cap204["crown_m"],
        "old_charge_2_m_kg": old2,
        "membrane_over_cap_mean": ratio,
    }


def jobs():
    film = fp.FILMS[1]
    mylar = fp.FILMS[0]
    return (
        ("projection_5", film, fp.SIG_CRUSH, eq.RESERVE_5, "percent"),
        ("projection_019", film, fp.SIG_CRUSH, eq.RESERVE_OPT, "percent"),
        ("mylar_5", mylar, fp.SIG_FLEX, eq.RESERVE_5, "percent"),
        ("mylar_019", mylar, fp.SIG_FLEX, eq.RESERVE_OPT, "percent"),
        ("ti_kapton_5", gl.KAPTON, fp.SIG_CRUSH, eq.RESERVE_5, "ti"),
        ("ti_kapton_019", gl.KAPTON, fp.SIG_CRUSH, eq.RESERVE_OPT, "ti"),
        ("cfrp_zylon_5", gl.ZYLON, fp.SIG_CRUSH, eq.RESERVE_5, "cfrp"),
        ("cfrp_zylon_019", gl.ZYLON, fp.SIG_CRUSH, eq.RESERVE_OPT, "cfrp"),
    )


def run_block(s_values):
    found = {}
    edge = False
    for label, film, sigma, reserve, kind in jobs():
        block = gl.scan(film, sigma, reserve, s_values, kind)
        found[label] = block
        row = block["equilateral"]
        cap = row["r_o_m"] >= 0.249
        print(
            label, g(row["SF_least"]), row["governing"], "s", row["s_m"],
            "ro", g(row["r_o_m"]), "sag", g(row["sag_kg"]), "cap", cap,
        )
        if gl.on_edge(block, s_values[-1]):
            edge = True
            print("EDGE", label)
    return found, edge


def pack_cases(cases):
    out = {}
    for name, block in cases.items():
        out[name] = {}
        for grid, row in block.items():
            kept = {k: row[k] for k in row if k != "coeff"}
            kept["on_ro_cap_0_25"] = row["r_o_m"] >= 0.249
            out[name][grid] = kept
    return out


def main():
    if os.path.exists(OUT_PATH):
        raise SystemExit("SAG.json is the measured 022c run. Not recomputing.")
    pins = check()
    t0 = time.monotonic()
    wall0 = datetime.datetime.now(ZONE)
    if os.path.exists(ORIGIN_PATH):
        origin = json.loads(open(ORIGIN_PATH, encoding="utf-8").read())
        print("SAG_ORIGIN exists; not restamping", origin["origin_local"])
    else:
        origin = {"origin_local": wall0.isoformat(timespec="microseconds")}
        fp.atomic_write(ORIGIN_PATH, json.dumps(origin, indent=1) + "\n")
        print("SAG_ORIGIN", origin["origin_local"])

    top = 8.0
    cap_cases = None
    s_values = None
    eq.sag_loss_kg = lift_cap
    while top <= 20.0:
        s_values = gl.values_to(top)
        print("CAP", top)
        cap_cases, edge = run_block(s_values)
        if not edge:
            break
        top += 4.0

    eq.sag_loss_kg = lift_membrane
    print("MEMBRANE", s_values[-1])
    membrane_cases, edge_m = run_block(s_values)
    if edge_m:
        print("MEMBRANE on the band edge")

    elapsed = time.monotonic() - t0
    ended = datetime.datetime.now(ZONE).isoformat(timespec="microseconds")
    doc = {
        "schema": 1,
        "card": "MAINLINE-022c",
        "questionable": True,
        "origin_local": origin["origin_local"],
        "ended_local": ended,
        "elapsed_s": elapsed,
        "s_max_m": s_values[-1],
        "sag": "024 inradius cap, rho = s, lift = L*3*mean/R. Membrane sensitivity mean = s/40.",
        "pins": pins,
        "cap": pack_cases(cap_cases),
        "membrane": pack_cases(membrane_cases),
    }
    fp.atomic_write(OUT_PATH, json.dumps(doc, indent=1) + "\n")
    lines = [
        "# MAINLINE-022c sag in the scan",
        "",
        "QUESTIONABLE. Elapsed %s s. Band to %s m." % (g(elapsed), g(s_values[-1])),
        "024 lift at 2 m is %s kg. The 022b charge L*s/(16R) at 2 m is %s kg."
        % (g(pins["lift_2_m_kg"]), g(pins["old_charge_2_m_kg"])),
        "Membrane mean over the cap mean is %s. The order says 1.19."
        % g(pins["membrane_over_cap_mean"]),
        "",
    ]
    for title, cases in (("cap", cap_cases), ("membrane", membrane_cases)):
        lines.append("## " + title)
        lines.append("")
        for name, block in cases.items():
            row = block["equilateral"]
            lines.append(
                "%s equilateral least %s by %s. s %s m, r_o %s mm, on 0.25 cap %s, "
                "wall %s mm, r/t %s, gamma %s, film %s mm, sag %s kg. "
                "Y %s E %s L %s F %s P %s G %s."
                % (
                    name, g(row["SF_least"]), row["governing"], g(row["s_m"]),
                    g(row["r_o_m"] * 1e3), row["r_o_m"] >= 0.249,
                    g(row["t_w_m"] * 1e3), g(row["rt"]), g(row["gamma"]),
                    g(row["t_film_m"] * 1e3), g(row["sag_kg"]),
                    g(row["SF_yield"]), g(row["SF_euler"]), g(row["SF_local"]),
                    g(row["SF_film"]), g(row["SF_perry"]), g(row["SF_global"]),
                )
            )
        lines.append("")
    fp.atomic_write(CARD_PATH, "\n".join(lines) + "\n")
    print("elapsed", g(elapsed), "end", ended)


if __name__ == "__main__":
    main()
