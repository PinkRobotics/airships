#!/usr/bin/env python3
"""MAINLINE-011 check. Own arithmetic. Does not call the owner's script.

Mass ceiling and the four stated limits are the COMMON member formulas:
  Euler 2*pi^2*E*I/(R*s^3), yield 2*sigma*A/(R*s),
  local 2*(0.6*E*t_w/r_o)*A/(R*s), film 2*sigma_f*t_f/s.
Sections are exact annuli. Node count is the equilateral continuum.
The scan maximises the least of those four. It does not add a global
lattice mode or chord bending; those are reported as model facts.
"""

import json
import math
from pathlib import Path

import numpy as np

P = 95460.8379139
R = 10.0
LIFT = 4889.44215019
FILM_KG = 97.515
SYS = 50.0
NODE_KG = 0.02
SIG_F = 1.5e9
T_F = 8.0e-5
RHO_F = 970.0
E_AL = 68.9e9
SIG_AL = 276e6
RHO_AL = 2700.0
NU = 0.33

OWN = Path("evidence/d529b7e4efa6fadc-RESULTS.json")

MATERIALS = {
    "6061-T6": (2700.0, 68.9e9, 276e6),
    "CFRP-QI-T700-epoxy": (1550.0, 54.0e9, 520e6),
    "CFRP-QI-M55J-epoxy": (1640.0, 135.0e9, 350e6),
    "CFRP-QI-K13D2U-epoxy": (1750.0, 210.0e9, 220e6),
    "SiC-alpha-Hexoloy-SA": (3100.0, 410.0e9, 3900e6),
    "CNT-yarn-QI-PROJECTION": (1400.0, 180.0e9, 1200e6),
}


def nodes(s):
    return 8.0 * math.pi * R * R / (math.sqrt(3.0) * s * s) + 2.0


def tube_mass(s):
    return LIFT - FILM_KG - NODE_KG * nodes(s) - SYS


def evaluate(s, ro, rho, E, sigma):
    v = nodes(s)
    m = 3.0 * v - 6.0
    mass = tube_mass(s)
    area = mass / (m * s * rho)
    if ro * ro <= area / math.pi:
        return None
    ri2 = ro * ro - area / math.pi
    tw = ro - math.sqrt(ri2)
    inertia = math.pi / 4.0 * (ro ** 4 - ri2 ** 2)
    p_euler = 2.0 * math.pi ** 2 * E * inertia / (R * s ** 3)
    p_yield = 2.0 * sigma * area / (R * s)
    p_local = 2.0 * (0.6 * E * tw / ro) * area / (R * s)
    p_film = 2.0 * SIG_F * T_F / s
    sfs = {
        "euler": p_euler / P,
        "yield": p_yield / P,
        "local": p_local / P,
        "film": p_film / P,
    }
    binding = min(sfs, key=sfs.get)
    return {
        "s": s,
        "ro": ro,
        "tw": tw,
        "tw_over_ro": tw / ro,
        "A": area,
        "I": inertia,
        "nodes": v,
        "members": m,
        "m_tube": mass,
        "sfs": sfs,
        "least": sfs[binding],
        "binding": binding,
    }


def best_at_s(s, rho, E, sigma, n=4000):
    v = nodes(s)
    m = 3.0 * v - 6.0
    mass = tube_mass(s)
    if mass <= 0 or m <= 0:
        return None
    area = mass / (m * s * rho)
    ro_min = math.sqrt(area / math.pi) * 1.0000001
    ro_max = min(0.25, s / 3.0)
    if ro_max <= ro_min:
        return None
    ros = np.linspace(ro_min, ro_max, n)
    best = None
    # Vectorised section. I = A/2*ro^2 - A^2/(4*pi)
    ri2 = ros * ros - area / math.pi
    tw = ros - np.sqrt(ri2)
    inertia = 0.5 * area * ros * ros - area * area / (4.0 * math.pi)
    p_euler = 2.0 * math.pi ** 2 * E * inertia / (R * s ** 3)
    p_yield = 2.0 * sigma * area / (R * s)
    p_local = 2.0 * (0.6 * E * tw / ros) * area / (R * s)
    p_film = 2.0 * SIG_F * T_F / s
    least = np.minimum(np.minimum(p_euler, p_yield), np.minimum(p_local, p_film)) / P
    k = int(np.argmax(least))
    return evaluate(s, float(ros[k]), rho, E, sigma)


def optimise(name, s_hi=3.0):
    rho, E, sigma = MATERIALS[name]
    best = None
    band = []
    s = 0.4
    while s <= s_hi + 1e-9:
        row = best_at_s(s, rho, E, sigma)
        if row is not None:
            band.append(row)
            if best is None or row["least"] > best["least"]:
                best = row
        s = round(s + 0.02, 10)
    return best, band


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-30)


def main():
    own = json.loads(OWN.read_text())
    print("film mass", 4 * math.pi * R * R * T_F * RHO_F)
    print("nodes s=1 mass", NODE_KG * nodes(1.0))
    classical = 1.0 / math.sqrt(3.0 * (1.0 - NU * NU))
    print("classical local coefficient", classical)

    # Stated aluminium points.
    al = own["materials_swap"]["6061-T6"]["best"]
    mine = evaluate(al["s"], al["r_o"], RHO_AL, E_AL, SIG_AL)
    print("\nAL stated point")
    for key in ("euler", "yield", "local", "film"):
        print(f"  {key} card {al['SF_'+key]:.8f} mine {mine['sfs'][key]:.8f} rel {rel(al['SF_'+key], mine['sfs'][key]):.3e}")
    print("  tw", al["t_w"], mine["tw"], "ro", al["r_o"], mine["ro"])
    sag = al["s"] ** 2 / (8.0 * R)
    print(f"  chord sag {sag:.6f} m vs ro {al['r_o']:.6f} m")

    # Global continuum formula quoted by the 011b brief, evaluated here only as a missing mode.
    g = 4.0 * E_AL * math.sqrt(mine["I"] * mine["A"]) / (al["s"] * R * R)
    print(f"  global perfect p {g:.3f} SF {g/P:.4f}  kd0.5 {(0.5*g)/P:.4f}  kd0.2 {(0.2*g)/P:.4f}")

    print("\nscan aluminium s<=3")
    best, band = optimise("6061-T6", 3.0)
    print(f"  best s {best['s']} least {best['least']:.6f} bind {best['binding']} ro {best['ro']*1000:.2f} mm tw {best['tw']*1000:.3f}")
    print(f"  s=1 least {next(r['least'] for r in band if abs(r['s']-1)<1e-9):.6f}")
    print(f"  band least min {min(r['least'] for r in band):.6f} max {max(r['least'] for r in band):.6f}")
    top = sorted(band, key=lambda r: -r["least"])[:4]
    for r in top:
        print(f"   s {r['s']:.2f} least {r['least']:.6f} {r['binding']} film {r['sfs']['film']:.3f} local {r['sfs']['local']:.3f}")

    print("\nswaps")
    for name in MATERIALS:
        b, rows = optimise(name, 6.4)
        inband = [r for r in rows if r["s"] <= 3.0 + 1e-9]
        card = own["materials_swap"][name]["best"]
        bb = max(inband, key=lambda r: r["least"])
        stated = evaluate(card["s"], card["r_o"], *MATERIALS[name])
        print(
            f"  {name}: card s {card['s']} SF {card['SF_least']:.4f} {card['binding']} | "
            f"stated-point mine {stated['least']:.4f} {stated['binding']} rel {rel(card['SF_least'], stated['least']):.2e} | "
            f"my best s {bb['s']} SF {bb['least']:.4f} {bb['binding']}"
        )
        gg = 4.0 * MATERIALS[name][1] * math.sqrt(stated["I"] * stated["A"]) / (card["s"] * R * R)
        print(f"    global perfect SF at card point {gg/P:.3f}")

    # Fixed ro=0.02 at s=1, the 005 P3-A comparison.
    area_target_note = None
    v = nodes(1.0)
    m = 3 * v - 6
    mass = tube_mass(1.0)
    area = mass / (m * 1.0 * RHO_AL)
    ro = 0.02
    row = evaluate(1.0, ro, RHO_AL, E_AL, SIG_AL)
    print("\nP3-A s=1 ro=0.02")
    print("  tw", row["tw"], "SFe", row["sfs"]["euler"], "SFy", row["sfs"]["yield"])
    # 005 required E and sigma are the values that put each SF at 1, at this geometry.
    print("  E for euler SF1", E_AL / row["sfs"]["euler"])
    print("  sigma for yield SF1", SIG_AL / row["sfs"]["yield"])

    p2 = 0.233885578993
    p2c = 0.164568553708
    print("\nP2-E ratios", best["least"] / p2, best["least"] / p2c)
    print("band floor s=0.40", next(r["least"] for r in band if abs(r["s"] - 0.4) < 1e-9))
    k13 = evaluate(1.0, 0.02, *MATERIALS["CFRP-QI-K13D2U-epoxy"])
    print("K13 fixed ro binding", k13["binding"], "euler", k13["sfs"]["euler"], "yield", k13["sfs"]["yield"])
    sic = best_at_s(0.90, *MATERIALS["SiC-alpha-Hexoloy-SA"])
    print("SiC s=0.90 least", sic["least"], sic["binding"], "film", sic["sfs"]["film"], "yield", sic["sfs"]["yield"])


if __name__ == "__main__":
    main()
