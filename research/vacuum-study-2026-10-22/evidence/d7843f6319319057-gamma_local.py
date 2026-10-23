#!/usr/bin/env python3
"""MAINLINE-022b local-buckling gamma plus the filed 023 joint.

Does not rewrite EQUILIBRIUM.json, the 022 files, or the 023 and 024 trees.
"""
import datetime
import json
import math
import os
import time
from zoneinfo import ZoneInfo

import equilibrium as eq
import floatpoint as fp

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIGIN_PATH = os.path.join(ROOT, "GAMMA_ORIGIN.json")
OUT_PATH = os.path.join(ROOT, "GAMMA.json")
CARD_PATH = os.path.join(ROOT, "GAMMA.md")
ZONE = ZoneInfo("America/Los_Angeles")
MODES = ("yield", "euler", "local", "film", "perry", "global")

# 023 CARD.md, kg·m/N^2, one member end. m = C * N^2 / r.
C_CFRP = 5.807e-15
C_TI = 2.950e-14
# 024 RESULTS.json design allowables. Kapton knockdown 0.5 is their assumption.
KAPTON = {
    "name": "Kapton-HN",
    "rho": 1420.0,
    "sigma": 115.5e6,
    "t_catalog_m": 25.0e-6,
}
ZYLON = {
    "name": "Zylon-HM-0/90",
    "rho": 1560.0,
    "sigma": 3.48e9,
    "t_catalog_m": 12.0e-6,
}


def g(x):
    return format(x, ".12g")


def gamma_sp8007(rt):
    """NASA SP-8007 axial correlation, as FIX-B in the 011b check."""
    return 1.0 - 0.901 * (1.0 - math.exp(-math.sqrt(rt) / 16.0))


def finish(row, sf_local_classical):
    gam = gamma_sp8007(row["rt"])
    row["gamma"] = gam
    row["SF_local_gamma1"] = sf_local_classical
    row["SF_local"] = sf_local_classical * gam
    modes = {name: row["SF_" + name] for name in MODES}
    gov = min(modes, key=lambda name: (modes[name], name))
    row["SF_least"] = modes[gov]
    row["governing"] = gov
    modes4 = dict(modes)
    modes4["global"] = 2.0 * row["SF_global"]
    gov4 = min(modes4, key=lambda name: (modes4[name], name))
    row["k04_SF_least"] = modes4[gov4]
    row["k04_governing"] = gov4
    row["k04_SF_global"] = modes4["global"]
    return row


def section_percent(s, t_f, rho_f, grid, base_reserve, r_o, sigma, film_sigma):
    row = eq.section_row(s, t_f, rho_f, grid, base_reserve, r_o, sigma, film_sigma)
    if row is None:
        return None
    classical = row["SF_local"]
    return finish(dict(row), classical)


def section_sized(s, t_f, rho_f, grid, base_reserve, r_o, sigma, film_sigma, c_end):
    nodes, members, n_coef, coeff = eq.grid_counts(s, grid)
    m_nodes = fp.M_NODE * nodes
    m_film = 4.0 * math.pi * fp.R * fp.R * t_f * rho_f
    sag = eq.sag_loss_kg(s)
    reserve = base_reserve + sag
    vehicle = fp.L_MASS - reserve
    n_force = fp.P_EXT * n_coef
    m_end = c_end * n_force * n_force / r_o
    m_joint = 2.0 * members * m_end
    m_tube = vehicle - 100.0 - m_film - m_nodes - m_joint
    if m_tube <= 0.0 or members <= 0.0:
        return None
    length = eq.arc_length(s)
    area = m_tube / (members * length * fp.RHO)
    if area <= 0.0 or r_o * r_o <= area / math.pi:
        return None
    r_i = math.sqrt(r_o * r_o - area / math.pi)
    t_w = r_o - r_i
    inertia = 0.25 * math.pi * (r_o ** 4 - r_i ** 4)
    sf_y = (sigma * area / n_coef) / fp.P_EXT
    sf_e = (math.pi ** 2 * fp.E_MOD * inertia / (length ** 2) / n_coef) / fp.P_EXT
    sf_l = (fp.C_LOCAL * fp.E_MOD * t_w / r_o * area / n_coef) / fp.P_EXT
    sf_f = (2.0 * film_sigma * t_f / s) / fp.P_EXT
    got = fp.perry(sigma, fp.E_MOD, length, r_o, inertia, area, n_force)
    if got is None:
        return None
    sf_g = (0.2 * coeff * fp.E_MOD * math.sqrt(inertia * area) / (s * fp.R * fp.R)) / fp.P_EXT
    row = {
        "nodes": nodes, "members": members, "n_coef": n_coef,
        "m_nodes": m_nodes, "m_film": m_film, "m_joint": m_joint, "m_tube": m_tube,
        "m_end": m_end, "reserve": reserve, "sag_kg": sag, "vehicle": vehicle,
        "s_m": s, "t_film_m": t_f, "r_o_m": r_o, "t_w_m": t_w, "rt": r_o / t_w,
        "A_m2": area, "I_m4": inertia, "length_m": length, "N_N": n_force,
        "sigma_axial_Pa": n_force / area, "k": 0.2,
        "SF_yield": sf_y, "SF_euler": sf_e, "SF_local": sf_l, "SF_film": sf_f,
        "SF_perry": got[0], "SF_global": sf_g,
    }
    return finish(row, sf_l)


def scan(film, sigma, base_reserve, s_values, kind):
    best = {"equilateral": None, "two_way": None}
    ts = eq.t_grid(film, base_reserve)
    scorer = section_percent if kind == "percent" else section_sized
    c_end = {"cfrp": C_CFRP, "ti": C_TI}.get(kind)
    for s in s_values:
        if s >= 2.0 * fp.R:
            continue
        for t_f in ts:
            for grid in ("equilateral", "two_way"):
                if kind == "percent":
                    info = eq.pack(s, t_f, film["rho"], grid, base_reserve)
                    if info["m_tube"] <= 0.0:
                        continue
                    length = eq.arc_length(s)
                    area = info["m_tube"] / (info["members"] * length * fp.RHO)
                    r_min = math.sqrt(area / math.pi) * 1.0001
                else:
                    nodes, members, n_coef, _coeff = eq.grid_counts(s, grid)
                    m_nodes = fp.M_NODE * nodes
                    m_film = 4.0 * math.pi * fp.R * fp.R * t_f * film["rho"]
                    structural = fp.L_MASS - (base_reserve + eq.sag_loss_kg(s)) - 100.0 - m_film - m_nodes
                    if structural <= 0.0:
                        continue
                    # Joint mass falls as r grows, so the heaviest tube is at r_max.
                    r_max_geom = min(0.25, s / 3.0)
                    n_force = fp.P_EXT * n_coef
                    m_joint_light = 2.0 * members * c_end * n_force * n_force / r_max_geom
                    m_tube_hi = structural - m_joint_light
                    if m_tube_hi <= 0.0:
                        continue
                    length = eq.arc_length(s)
                    area = m_tube_hi / (members * length * fp.RHO)
                    r_min = math.sqrt(area / math.pi) * 1.0001
                r_max = min(0.25, s / 3.0)
                if r_max <= r_min:
                    continue
                span = r_max - r_min
                for i in range(eq.N_RO):
                    r_o = r_min + span * (i / (eq.N_RO - 1))
                    if kind == "percent":
                        row = scorer(s, t_f, film["rho"], grid, base_reserve, r_o, sigma, film["sigma"])
                    else:
                        row = scorer(
                            s, t_f, film["rho"], grid, base_reserve, r_o, sigma, film["sigma"], c_end,
                        )
                    if row is None:
                        continue
                    prev = best[grid]
                    if prev is None or row["SF_least"] > prev["SF_least"]:
                        best[grid] = row
    return best


def check():
    rt = 140.5
    gam = gamma_sp8007(rt)
    if abs(gam - 0.529) > 0.002:
        raise SystemExit("gamma at r/t 140.5 is %s" % gam)
    s = 2.04
    r_o = 0.123688362374
    nodes, members, n_coef, _coeff = eq.grid_counts(s, "equilateral")
    n_force = fp.P_EXT * n_coef
    m_cfrp = 2.0 * members * C_CFRP * n_force * n_force / r_o
    m_ti = 2.0 * members * C_TI * n_force * n_force / r_o
    if abs(m_cfrp - 31.0) > 0.25:
        raise SystemExit("CFRP joint at the 011b point is %s kg" % m_cfrp)
    if abs(m_ti - 157.7) > 0.6:
        raise SystemExit("Ti joint at the 011b point is %s kg" % m_ti)
    print("checks", "gamma140", g(gam), "cfrp", g(m_cfrp), "ti", g(m_ti), "N", g(n_force))
    return {"gamma_rt_140_5": gam, "m_cfrp_kg": m_cfrp, "m_ti_kg": m_ti, "N_N": n_force}


def values_to(top):
    return [round(0.40 + 0.05 * i, 3) for i in range(int(round((top - 0.40) / 0.05)) + 1)]


def on_edge(found, top):
    for row in found.values():
        if row is not None and row["s_m"] >= top - 0.051:
            return True
    return False


def main():
    if os.path.exists(OUT_PATH):
        raise SystemExit("GAMMA.json is the measured gamma run. Not recomputing.")
    t0 = time.monotonic()
    pins = check()
    wall0 = datetime.datetime.now(ZONE)
    if os.path.exists(ORIGIN_PATH):
        origin = json.loads(open(ORIGIN_PATH, encoding="utf-8").read())
        print("GAMMA_ORIGIN exists; not restamping", origin["origin_local"])
    else:
        origin = {"origin_local": wall0.isoformat(timespec="microseconds")}
        fp.atomic_write(ORIGIN_PATH, json.dumps(origin, indent=1) + "\n")
        print("GAMMA_ORIGIN", origin["origin_local"])

    prior = json.loads(open(os.path.join(ROOT, "EQUILIBRIUM.json"), encoding="utf-8").read())
    prior_row = prior["cases"]["carried_5"]["equilateral"]
    gam_prior = gamma_sp8007(prior_row["rt"])
    prior_local = prior_row["SF_local"] * gam_prior
    print("prior_local", g(prior_row["SF_local"]), "gamma", g(gam_prior), "knocked", g(prior_local))

    top = 8.0
    film = fp.FILMS[1]
    percent5 = None
    s_values = None
    while top <= 20.0:
        s_values = values_to(top)
        percent5 = scan(film, fp.SIG_CRUSH, eq.RESERVE_5, s_values, "percent")
        print("band", top, "s", percent5["equilateral"]["s_m"], "SF", g(percent5["equilateral"]["SF_least"]), percent5["equilateral"]["governing"])
        if not on_edge(percent5, top):
            break
        top += 4.0

    def run(label, film_row, sigma, reserve, kind):
        found = scan(film_row, sigma, reserve, s_values, kind)
        row = found["equilateral"]
        print(label, g(row["SF_least"]), row["governing"], "s", row["s_m"], "rt", g(row["rt"]), "gam", g(row["gamma"]))
        if on_edge(found, s_values[-1]):
            print("EDGE", label)
        return found

    cases = {
        "percent_crush_5": percent5,
        "percent_crush_019": run("p019", film, fp.SIG_CRUSH, eq.RESERVE_OPT, "percent"),
        "percent_mylar_5": run("pm5", fp.FILMS[0], fp.SIG_FLEX, eq.RESERVE_5, "percent"),
        "percent_mylar_019": run("pm019", fp.FILMS[0], fp.SIG_FLEX, eq.RESERVE_OPT, "percent"),
        "cfrp_crush_5": run("c5", film, fp.SIG_CRUSH, eq.RESERVE_5, "cfrp"),
        "cfrp_crush_019": run("c019", film, fp.SIG_CRUSH, eq.RESERVE_OPT, "cfrp"),
        "cfrp_mylar_5": run("cm5", fp.FILMS[0], fp.SIG_FLEX, eq.RESERVE_5, "cfrp"),
        "cfrp_mylar_019": run("cm019", fp.FILMS[0], fp.SIG_FLEX, eq.RESERVE_OPT, "cfrp"),
        "cfrp_kapton_5": run("ck5", KAPTON, fp.SIG_CRUSH, eq.RESERVE_5, "cfrp"),
        "cfrp_zylon_5": run("cz5", ZYLON, fp.SIG_CRUSH, eq.RESERVE_5, "cfrp"),
        "ti_crush_5": run("t5", film, fp.SIG_CRUSH, eq.RESERVE_5, "ti"),
    }
    elapsed = time.monotonic() - t0
    ended = datetime.datetime.now(ZONE).isoformat(timespec="microseconds")

    def pack_row(row):
        return {k: row[k] for k in row if k != "coeff"}

    doc = {
        "schema": 1,
        "card": "MAINLINE-022b-gamma",
        "questionable": True,
        "origin_local": origin["origin_local"],
        "ended_local": ended,
        "elapsed_s": elapsed,
        "s_max_m": s_values[-1],
        "gamma": "1 - 0.901*(1 - exp(-sqrt(r/t)/16)), times the local mode. QUESTIONABLE.",
        "joint": "023 CFRP wrap C=5.807e-15 kg m/N^2 per end, and Ti-6Al-4V C=2.950e-14. PROJECTION for the wrap.",
        "film_024": "Kapton HN 115.5 MPa, 1420 kg/m3, exists. Zylon HM 3.48 GPa is their lightest unsourced membrane.",
        "pending": ["PENDING-025"],
        "pins": pins,
        "prior_equilateral_5_local_with_gamma": {
            "s_m": prior_row["s_m"],
            "rt": prior_row["rt"],
            "gamma": gam_prior,
            "SF_local_gamma1": prior_row["SF_local"],
            "SF_local": prior_local,
        },
        "cases": {name: {grid: pack_row(row) for grid, row in block.items()} for name, block in cases.items()},
    }
    fp.atomic_write(OUT_PATH, json.dumps(doc, indent=1) + "\n")
    lines = ["# MAINLINE-022b gamma", "", "QUESTIONABLE. Elapsed %s s. Band to %s m." % (g(elapsed), g(s_values[-1])), ""]
    for name, block in cases.items():
        for grid in ("equilateral", "two_way"):
            row = block[grid]
            lines.append(
                "%s %s least %s by %s. s %s m, r_o %s mm, wall %s mm, r/t %s, gamma %s, film %s mm. "
                "Y %s E %s L %s F %s P %s G %s. tubes %s joints %s sag %s. k04 %s by %s."
                % (
                    name, grid, g(row["SF_least"]), row["governing"], g(row["s_m"]), g(row["r_o_m"] * 1e3),
                    g(row["t_w_m"] * 1e3), g(row["rt"]), g(row["gamma"]), g(row["t_film_m"] * 1e3),
                    g(row["SF_yield"]), g(row["SF_euler"]), g(row["SF_local"]), g(row["SF_film"]),
                    g(row["SF_perry"]), g(row["SF_global"]), g(row["m_tube"]), g(row["m_joint"]),
                    g(row["sag_kg"]), g(row["k04_SF_least"]), row["k04_governing"],
                )
            )
        lines.append("")
    fp.atomic_write(CARD_PATH, "\n".join(lines) + "\n")
    print("elapsed", g(elapsed), "end", ended)


if __name__ == "__main__":
    main()
