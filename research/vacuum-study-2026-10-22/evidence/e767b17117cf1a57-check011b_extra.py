#!/usr/bin/env python3
"""MAINLINE-011b check, objections in numbers (checker's own arithmetic; builds on check011b.py).

1. Local buckling with NASA SP-8007's own axial correlation factor, gamma = 1 - 0.901*(1 - exp(-sqrt(r/t)/16)),
   the source 011 cites for the 0.6 coefficient (the card keeps gamma = 1).
2. Fibre stresses from the L/1000 Perry imperfection at the SiC point: is any fibre in tension?
3. Member torsion in the smeared plate D (rigid joints), as a magnitude.
4. Combined restatements of the SiC equilateral and two-way rows.
Every value is QUESTIONABLE; nothing here is a certification.
"""
import json
import math
from pathlib import Path

import numpy as np

import check011b as c

OUT = c.OUT


def gamma_sp8007(r_over_t):
    return 1 - 0.901 * (1 - np.exp(-np.sqrt(r_over_t) / 16.0))


def modes2(mat, s, ro, A, k, grid, force=1.0, sp8007=False, sys_kg=None):
    md, (ri, tw, I, N, sax) = c.all_modes(mat, s, ro, A, k, grid, force)
    if sp8007:
        md = dict(md)
        md["local"] = md["local"] * gamma_sp8007(ro / tw)
    return md, (ri, tw, I, N, sax)


def refine2(mat, grid, k, force=1.0, sp8007=False, sys_kg=c.SYS, margin_kg=0.0, jf=c.JF):
    rho = c.MATS[mat][0]
    best = None
    for s in np.round(np.arange(0.400, 3.0000001, 0.002), 6):
        s = float(s)
        mt = c.m_tube(s, jf, sys_kg, margin_kg)
        A = mt / (rho * c.members(s) * s)
        lo, hi = math.sqrt(A / math.pi) * 1.0001, min(0.25, s / 3)
        if hi <= lo:
            continue
        ro = np.linspace(lo, hi, 20000)
        sf = c.least(modes2(mat, s, ro, A, k, grid, force, sp8007)[0])
        i = int(np.argmax(sf))
        if best is None or sf[i] > best[0]:
            best = (float(sf[i]), s, float(ro[i]), A, mt)
    sfv, s, ro, A, mt = best
    md, (ri, tw, I, N, sax) = modes2(mat, s, np.array([ro]), A, k, grid, force, sp8007)
    vals = {m: float(md[m][0]) for m in c.MODES}
    order = sorted(vals, key=vals.get)
    return {"material": mat, "grid": grid, "k": k, "force_factor": force, "local_sp8007": sp8007,
            "systems_kg": sys_kg, "margin_kg": margin_kg, "SF_least": sfv, "governs": order[0], "second": order[1],
            "s_m": s, "r_o_m": ro, "t_w_m": float(tw[0]), "r_over_t": ro / float(tw[0]),
            "gamma_local": float(gamma_sp8007(ro / float(tw[0]))), "N_member_N": float(N),
            "sigma_axial_Pa": float(np.ravel(sax)[0]), "m_tube_kg": mt, "m_joint_kg": jf * mt,
            "nodes": c.nodes(s), "SF": vals}


def fibre(mat, s, ro, tw, force):
    rho, E, sig = c.MATS[mat]
    ri = ro - tw
    A = math.pi * (ro ** 2 - ri ** 2)
    I = math.pi / 4 * (ro ** 4 - ri ** 4)
    N = c.P * c.R * s / 2 * force
    sax = N / A
    rg2 = I / A
    sE = math.pi ** 2 * E * rg2 / s ** 2
    eta = (s / 1000) * ro / rg2
    amp = 1 / (1 - sax / sE)
    sb = sax * eta * amp
    return {"force_factor": force, "N_N": N, "sigma_axial_Pa": sax, "sigma_E_Pa": sE, "eta": eta,
            "amplifier": amp, "sigma_bending_Pa": sb, "fibre_max_compression_Pa": sax + sb,
            "fibre_min_compression_Pa": sax - sb, "any_tension": sax - sb < 0}


def torsion_plate(nu_m):
    """Smeared plate operator of the equilateral grid with member bending EI and torsion GJ (tube: J = 2I,
    G = E/(2(1+nu))), per unit E*I/h. Returns the del^4 coefficient and an isotropy check."""
    fam = [math.radians(a) for a in (0.0, 60.0, 120.0)]
    gj = 1.0 / (1 + nu_m)                      # GJ/EI for a thin tube
    D = np.zeros((2, 2, 2, 2))
    for th in fam:
        e = np.array([math.cos(th), math.sin(th)])
        t = np.array([-math.sin(th), math.cos(th)])
        D += np.einsum("i,j,k,l->ijkl", e, e, e, e)
        sym = 0.5 * (np.outer(e, t) + np.outer(t, e))
        D += gj * np.einsum("ij,kl->ijkl", sym, sym)
    c4 = D[0, 0, 0, 0]
    mixed = 2 * D[0, 0, 1, 1] + 4 * D[0, 1, 0, 1]
    return {"nu_member": nu_m, "GJ_over_EI": gj, "D1111_bending_only": 9 / 8, "D1111_with_torsion": c4,
            "isotropic": bool(abs(D[1, 1, 1, 1] - c4) < 1e-12 and abs(mixed - 2 * c4) < 1e-12),
            "global_SF_factor_sqrt": math.sqrt(c4 / (9 / 8))}


def main():
    res = {"schema": 1, "card": "MAINLINE-011b CHECK extras", "questionable": True, "certification": False}
    base = json.loads((OUT / "RESULTS.json").read_text())
    card_sic = next(r for r in base["primary_joints_on_grid"]
                    if r["material"].startswith("SiC") and r["grid"] == "equilateral_triangular" and r["k"] == 0.2)
    s, ro, tw = card_sic["s_m"], card_sic["r_o_m"], card_sic["t_w_m"]
    res["card_SiC_point"] = {"s_m": s, "r_o_m": ro, "t_w_m": tw, "r_over_t": ro / tw,
                             "p_global_Pa": card_sic["SF"]["global"] * c.P,
                             "gamma_sp8007": float(gamma_sp8007(ro / tw)),
                             "SF_local_card": card_sic["SF"]["local"],
                             "SF_local_with_sp8007_gamma": card_sic["SF"]["local"] * float(gamma_sp8007(ro / tw)),
                             "fibre_card_force": fibre("SiC-alpha-Hexoloy-SA", s, ro, tw, 1.0),
                             "fibre_equilibrium_force": fibre("SiC-alpha-Hexoloy-SA", s, ro, tw, 1 / math.sqrt(3))}
    res["torsion"] = {"SiC_nu_0.14": torsion_plate(0.14), "6061_nu_0.33": torsion_plate(0.33)}
    fx = 1 / math.sqrt(3)
    combos = []
    for mat in ("SiC-alpha-Hexoloy-SA", "6061-T6"):
        for grid in ("equilateral_triangular", "two_way"):
            for k in (0.2, 0.4):
                for force, sp in ((1.0, False), (fx, False), (1.0, True), (fx, True)):
                    combos.append(refine2(mat, grid, k, force, sp))
                    if mat.startswith("SiC"):
                        combos.append(refine2(mat, grid, k, force, sp, sys_kg=100.0, margin_kg=0.05 * c.L))
    res["restatements"] = combos
    (OUT / "RESULTS-EXTRA.json").write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps({k: res[k] for k in ("card_SiC_point", "torsion")}, indent=1, default=float))
    for r in combos:
        print(f"{r['material'][:5]} {r['grid'][:5]} k{r['k']} f{r['force_factor']:.3f} sp8007={int(r['local_sp8007'])} "
              f"sys{r['systems_kg']:.0f} mar{r['margin_kg']:.0f} | {r['SF_least']:.4f} {r['governs']}/{r['second']} | "
              f"s {r['s_m']:.3f} ro {r['r_o_m']*1e3:.1f} tw {r['t_w_m']*1e3:.3f} r/t {r['r_over_t']:.0f} "
              f"gam {r['gamma_local']:.3f} N {r['N_member_N']/1e3:.0f}kN")


if __name__ == "__main__":
    main()
