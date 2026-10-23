#!/usr/bin/env python3
"""Restate the carried P3 point at MAINLINE-019's P3 optimistic reserve.

Does not rewrite RESULTS.json, ORIGIN.json, CARD.md, NFI.json or INPUTS.json.
Those are the measured 5 percent run.
"""
import datetime
import json
import math
import os
import time
from zoneinfo import ZoneInfo

import floatpoint as fp

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIGIN_PATH = os.path.join(ROOT, "BUDGET_ORIGIN.json")
OUT_PATH = os.path.join(ROOT, "BUDGET.json")
CARD_PATH = os.path.join(ROOT, "BUDGET.md")
ZONE = ZoneInfo("America/Los_Angeles")

# 019 aluminium (common) optimistic lines. Joint-and-bond excess is P2's and is excluded.
# Sealed-service systems are 30 kg inside the 100 kg allowance, so systems excess is 0.
LINES = {
    "retained_water_kg": 125.66370614359174,
    "contamination_kg": 5.0,
    "temperature_pressure_loss_kg": 213.036426543752,
    "humidity_loss_kg": 18.704389882434043,
    "internal_gas_kg": 48.89442150186961,
}
P2_JOINT_EXCESS = 124.6469630808904
NINETEEN_TOTAL = 535.9459071525378
RESERVE = sum(LINES.values())
N_RO = 700


def g(x):
    return format(x, ".12g")


def masses_at_reserve(s, t_f, rho_f, mode):
    """Common-rules masses with this reserve. The 5 percent path is untouched."""
    if mode == "011b":
        return fp.masses(s, t_f, rho_f, mode)
    V = fp.node_count(s)
    members = 3.0 * V - 6.0
    m_nodes = fp.M_NODE * V
    m_film = 4.0 * math.pi * fp.R * fp.R * t_f * rho_f
    m_sys = 100.0
    vehicle = fp.L_MASS - RESERVE
    assembly = (vehicle - m_sys) / (1.0 + fp.JOINT_FRAC)
    m_joint = (vehicle - m_sys) - assembly
    m_tube = assembly - m_film - m_nodes
    return {
        "V": V,
        "members": members,
        "m_nodes": m_nodes,
        "m_film": m_film,
        "m_tube": m_tube,
        "m_joint": m_joint,
        "m_sys": m_sys,
        "vehicle": vehicle,
        "payload": RESERVE,
        "total_accounted": m_film + m_nodes + m_tube + m_joint + m_sys + RESERVE,
    }


def t_values(film):
    assembly = (fp.L_MASS - 100.0 - RESERVE) / 1.05
    t_hi = 0.75 * assembly / (4.0 * math.pi * fp.R * fp.R * film["rho"])
    t_lo = film["t_catalog_m"]
    if t_hi <= t_lo:
        return [t_lo]
    return [t_lo * (t_hi / t_lo) ** (i / 11.0) for i in range(12)]


def check_algebra():
    got = NINETEEN_TOTAL - P2_JOINT_EXCESS
    if abs(got - RESERVE) > 1e-9:
        raise SystemExit("reserve does not match 019 total minus P2 joint excess: %s %s" % (got, RESERVE))
    # At a 5 percent reserve the wrapper must match the measured mass rule.
    saved = RESERVE
    # Local check against fp.masses at the published 5 percent vehicle.
    s, t_f, rho = 2.04, 8.0e-5, 970.0
    base = fp.masses(s, t_f, rho, "common")
    vehicle_5 = 0.95 * fp.L_MASS
    if abs(base["vehicle"] - vehicle_5) > 1e-6:
        raise SystemExit("5 percent vehicle drifted")
    if abs(base["m_joint"] - 216.427144889) > 1e-3:
        raise SystemExit("5 percent joint drifted")
    opt = masses_at_reserve(s, t_f, rho, "common")
    if opt["m_tube"] <= 0.0:
        raise SystemExit("optimistic tube mass is not positive at the probe")
    if abs(opt["vehicle"] + RESERVE - fp.L_MASS) > 1e-6:
        raise SystemExit("optimistic vehicle does not close")
    if abs((opt["m_film"] + opt["m_nodes"] + opt["m_tube"]) * 0.05 - opt["m_joint"]) > 1e-6:
        raise SystemExit("optimistic joints are not 5 percent")
    print("algebra", g(RESERVE), "joint_probe", g(opt["m_joint"]), "saved", saved)


def main():
    if os.path.exists(OUT_PATH):
        raise SystemExit("BUDGET.json is the measured optimistic run. Not recomputing.")
    if not os.path.exists(os.path.join(ROOT, "RESULTS.json")):
        raise SystemExit("5 percent RESULTS.json is missing")
    check_algebra()
    mono0 = time.monotonic()
    wall0 = datetime.datetime.now(ZONE)
    origin = {"origin_local": wall0.isoformat(timespec="microseconds"), "origin_monotonic_s": mono0}
    if os.path.exists(ORIGIN_PATH):
        origin = json.loads(open(ORIGIN_PATH, encoding="utf-8").read())
        print("BUDGET_ORIGIN exists; not restamping")
    else:
        fp.atomic_write(ORIGIN_PATH, json.dumps(origin, indent=1) + "\n")
        print("BUDGET_ORIGIN", origin["origin_local"])
    fp.masses = masses_at_reserve
    film = fp.FILMS[1]
    found = fp.scan("common", film, t_values(film), [1.0], N_RO, fp.S_BAND)
    elapsed = time.monotonic() - origin["origin_monotonic_s"]
    ended = datetime.datetime.now(ZONE).isoformat(timespec="microseconds")

    def grab(grid, k, sigma):
        row = found[(grid, k, sigma)]
        keep = (
            "grid", "k", "sigma_name", "s_m", "h_m", "h_over_sagitta", "r_o_m", "t_w_m", "rt",
            "t_film_m", "film", "m_tube_kg", "m_nodes_kg", "m_joint_kg", "m_film_kg",
            "m_systems_kg", "m_payload_kg", "SF_yield", "SF_euler", "SF_local", "SF_film",
            "SF_perry", "SF_global", "SF_least", "governing",
        )
        return {name: row[name] for name in keep}

    rows = {
        "equilateral_k02_crush": grab("equilateral_triangular", 0.2, "crush_3900"),
        "two_way_k02_crush": grab("two_way", 0.2, "crush_3900"),
        "equilateral_k04_crush": grab("equilateral_triangular", 0.4, "crush_3900"),
        "two_way_k04_crush": grab("two_way", 0.4, "crush_3900"),
        "equilateral_k02_flexural": grab("equilateral_triangular", 0.2, "flexural_380"),
    }
    doc = {
        "schema": 1,
        "card": "MAINLINE-022",
        "unit": "vacuum-mainline022-p3-optimistic-floating-point-1020",
        "questionable": True,
        "reserve_kg": RESERVE,
        "reserve_fraction": RESERVE / fp.L_MASS,
        "lines_kg": LINES,
        "excluded_p2_joint_excess_kg": P2_JOINT_EXCESS,
        "nineteen_total_kg": NINETEEN_TOTAL,
        "systems_kg": 100.0,
        "systems_note": "019 sealed-service hardware is 30 kg inside the 100 kg allowance. Excess charged is 0. The unused 70 kg stays reserved.",
        "joints": "5 percent of film+nodes+tubes, PENDING-023. P2 bond-film excess is not charged.",
        "payload_inside_reserve_kg": 0.0,
        "origin": {"origin_local": origin["origin_local"]},
        "elapsed_s": elapsed,
        "ended_local": ended,
        "rows": rows,
    }
    fp.atomic_write(OUT_PATH, json.dumps(doc, indent=1) + "\n")
    eq = rows["equilateral_k02_crush"]
    tw = rows["two_way_k02_crush"]
    k4 = rows["equilateral_k04_crush"]
    flex = rows["equilateral_k02_flexural"]
    lines = [
        "# MAINLINE-022 — P3 point at the 019 optimistic reserve",
        "",
        "QUESTIONABLE. This file does not replace the measured 5 percent run.",
        "",
        "MAINLINE-019's optimistic total is 535.945907153 kg. Of that, 124.646963081 kg is P2 joint and bond-film excess. P3 does not take that row. Joints stay at 5 percent, PENDING-023. The P3 reserve is 411.298944072 kg: retained water 125.663706144 kg at 0.1 mm, contamination 5 kg, temperature and pressure 213.036426544 kg, humidity 18.7043898824 kg, internal air 48.8944215019 kg. Payload inside that reserve is 0. Sealed-service systems are 30 kg inside the 100 kg allowance, so no systems excess is charged.",
        "",
        "The 5 percent point stays the filed one. Equilateral, k 0.2, carried 011b film and crush: least SF 1.23867626922 by global, s 3 m on the band edge.",
        "",
        "At this reserve, same carried film and crush, equilateral, k 0.2. Least SF %s by %s. s %s m, r_o %s mm, wall %s mm, r/t %s, film %s mm. Yield %s, Euler %s, local %s, film %s, Perry %s, global %s. Tubes %s kg, nodes %s kg, joints %s kg, film %s kg." % (
            g(eq["SF_least"]), eq["governing"], g(eq["s_m"]), g(eq["r_o_m"] * 1e3), g(eq["t_w_m"] * 1e3),
            g(eq["rt"]), g(eq["t_film_m"] * 1e3), g(eq["SF_yield"]), g(eq["SF_euler"]), g(eq["SF_local"]),
            g(eq["SF_film"]), g(eq["SF_perry"]), g(eq["SF_global"]), g(eq["m_tube_kg"]), g(eq["m_nodes_kg"]),
            g(eq["m_joint_kg"]), g(eq["m_film_kg"]),
        ),
        "",
        "Two-way, k 0.2. Least SF %s by %s at s %s m. Global %s, local %s, film %s, Perry %s, yield %s." % (
            g(tw["SF_least"]), tw["governing"], g(tw["s_m"]), g(tw["SF_global"]), g(tw["SF_local"]),
            g(tw["SF_film"]), g(tw["SF_perry"]), g(tw["SF_yield"]),
        ),
        "",
        "Equilateral, k 0.4. Least SF %s by %s at s %s m." % (g(k4["SF_least"]), k4["governing"], g(k4["s_m"])),
        "",
        "Equilateral, k 0.2, flexural 380 MPa on the same film scan. Least SF %s by %s. The 3900 MPa crush remains PENDING-025." % (
            g(flex["SF_least"]), flex["governing"],
        ),
        "",
        "A ceramic arc still takes k 0.2. Elapsed time is a measurement.",
        "",
    ]
    fp.atomic_write(CARD_PATH, "\n".join(lines))
    print("elapsed", g(elapsed))
    print("EQ", g(eq["SF_least"]), eq["governing"], "s", g(eq["s_m"]), "ro", g(eq["r_o_m"]),
          "tw", g(eq["t_w_m"]), "tf", g(eq["t_film_m"]),
          "y", g(eq["SF_yield"]), "e", g(eq["SF_euler"]), "l", g(eq["SF_local"]),
          "f", g(eq["SF_film"]), "p", g(eq["SF_perry"]), "g", g(eq["SF_global"]))
    print("TW", g(tw["SF_least"]), tw["governing"], "s", g(tw["s_m"]))
    print("K4", g(k4["SF_least"]), k4["governing"], "s", g(k4["s_m"]))
    print("FLEX", g(flex["SF_least"]), flex["governing"], "s", g(flex["s_m"]))


if __name__ == "__main__":
    main()
