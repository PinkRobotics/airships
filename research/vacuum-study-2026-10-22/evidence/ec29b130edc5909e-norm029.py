#!/usr/bin/env python3
"""CHECK MAINLINE-029: every normalisation number in the card, re-derived from the card's stated formulas and inputs.
h = tc + (ti+to)/2; p_classical = 2 E h (ti+to)/(R^2 sqrt(1-nu^2)); p_crimp = 2 h^2 G/(R tc); Vc = p_cl/p_crimp;
Kc = 1 - Vc/4 (Vc <= 2) else 1/Vc; p_H = Kc p_cl; gamma_crimp = gamma_H Kc Vc."""
import json
import math
import sys

P_OP = 0.09546083791390515                                  # MPa (COMMON)
E_BE, NU = 290000.0, 0.33
G_W, G_L = 46.88434959354485, 103.4213593975254
LEAD = {"lead021": (0.8434480441930918, 20.21337638749162), "lead021b": (0.691748, 30.118231)}


def handbook(E, nu, ti, to, tc, R, G):
    h = tc + (ti + to) / 2
    pcl = 2 * E * h * (ti + to) / (R ** 2 * math.sqrt(1 - nu ** 2))
    pcr = 2 * h ** 2 * G / (R * tc)
    Vc = pcl / pcr
    Kc = 1 - Vc / 4 if Vc <= 2 else 1 / Vc
    return {"h": h, "p_classical": pcl, "p_crimp": pcr, "Vc": Vc, "Kc": Kc, "p_H": Kc * pcl}


def cmp(rows, name, card, mine, tol_rel=5e-6):
    d = mine - card
    rows.append({"row": name, "card": card, "mine": mine, "diff": d, "rel": d / card if card else None,
                 "match": abs(d) <= tol_rel * abs(card) + 1e-12})


def main():
    rows = []
    hb = {}
    for case, (tf, tc) in LEAD.items():
        for dname, G in (("W", G_W), ("L", G_L)):
            r = handbook(E_BE, NU, tf, tf, tc, 10000.0, G)
            hb[(case, dname)] = r
    card_t1 = {("lead021", "W"): (1.061063, 160.353, 205.686, 0.595318, 0.464110),
               ("lead021", "L"): (0.481015, 192.001, 453.719, 0.497189, 0.210396),
               ("lead021b", "W"): (0.886182, 203.877, 295.537, 0.468229, 0.323009),
               ("lead021b", "L"): (0.401736, 235.596, 651.919, 0.405189, 0.146431)}
    for k, (Vc, pH, pcr, gH, gC) in card_t1.items():
        r = hb[k]; tag = f"{k[0]}/{k[1]}"
        cmp(rows, f"T1 {tag} Vc", Vc, round(r["Vc"], 6), 1e-6)
        cmp(rows, f"T1 {tag} p_H kPa", pH, round(r["p_H"] * 1e3, 3), 1e-5)
        cmp(rows, f"T1 {tag} p_crimp kPa", pcr, round(r["p_crimp"] * 1e3, 3), 1e-5)
        cmp(rows, f"T1 {tag} required gamma_H", gH, round(P_OP / r["p_H"], 6), 1e-6)
        cmp(rows, f"T1 {tag} required gamma_crimp", gC, round(P_OP / r["p_crimp"], 6), 1e-6)
        # identity gamma_crimp = gamma_H Kc Vc
        cmp(rows, f"T1 {tag} identity gH*Kc*Vc", P_OP / r["p_crimp"], (P_OP / r["p_H"]) * r["Kc"] * r["Vc"], 1e-12)
    # endpoint table (card values) -> ratios
    card_t2 = {("lead021", "W"): (78.627, 0.490340, 0.382269, 0.82366),
               ("lead021", "L"): (98.094, 0.510903, 0.216200, 1.02758),
               ("lead021b", "W"): (90.722, 0.444986, 0.306975, 0.95036),
               ("lead021b", "L"): (105.051, 0.445897, 0.161142, 1.10046)}
    for k, (ep, gH, gC, rop) in card_t2.items():
        r = hb[k]; tag = f"{k[0]}/{k[1]}"
        e = ep / 1e3
        cmp(rows, f"T2 {tag} endpoint gamma_H", gH, round(e / r["p_H"], 6), 2e-5)
        cmp(rows, f"T2 {tag} endpoint gamma_crimp", gC, round(e / r["p_crimp"], 6), 2e-5)
        cmp(rows, f"T2 {tag} endpoint/operating", rop, round(e / P_OP, 5), 2e-5)
    # W denominator for both orientations
    cmp(rows, "T2 lead021 L endpoint / p_H(W)", 0.61174, round(0.098094 / hb[("lead021", "W")]["p_H"], 5), 2e-5)
    cmp(rows, "T2 lead021b L endpoint / p_H(W)", 0.51527, round(0.105051 / hb[("lead021b", "W")]["p_H"], 5), 2e-5)
    # outer radius / core
    cmp(rows, "lead021 R/tc", 494.7219, round(10000 / LEAD["lead021"][1], 4), 1e-7)
    cmp(rows, "lead021b R/tc", 332.0248, round(10000 / LEAD["lead021b"][1], 4), 1e-7)
    # Gaussian widths: card uses nu 0.30 (015's retired convention); 015b's live map uses nu 0.33
    for case, (tf, tc) in LEAD.items():
        teq = math.sqrt(3) * (tc + tf)
        w30 = math.sqrt(10000 * teq) / (12 * (1 - 0.3 ** 2)) ** 0.25
        w33 = math.sqrt(10000 * teq) / (12 * (1 - 0.33 ** 2)) ** 0.25
        card_w = 332.216 if case == "lead021" else 401.856
        cmp(rows, f"{case} Gaussian width mm (card nu 0.30)", card_w, round(w30, 3), 2e-6)
        rows.append({"row": f"{case} Gaussian width mm under 015b live nu 0.33", "card": card_w, "mine": round(w33, 3),
                     "diff": w33 - card_w, "rel": (w33 - card_w) / card_w, "match": False})
    # EUCASS (mid radius) and transfer40
    for case, ti, ep_pub, ep_el in (("flat", 0.42, 6.03, 13.956916), ("dimple", 0.40, 5.63, 13.843652)):
        T = ti + 3.1 + 0.42
        Rm = 42.8 - T / 2
        r = handbook(210000.0, 0.33, ti, 0.42, 3.1, Rm, 20.0)
        card = {"flat": (201.532, 3.915653, 1.539973), "dimple": (197.246, 3.892484, 1.446377)}[case]
        cmp(rows, f"EUCASS {case} Vc", card[0], round(r["Vc"], 3), 1e-6)
        cmp(rows, f"EUCASS {case} p_crimp MPa", card[1], round(r["p_crimp"], 6), 1e-6)
        cmp(rows, f"EUCASS {case} published imperfect / p_crimp", card[2], round(ep_pub / r["p_crimp"], 6), 1e-6)
        if case == "flat":
            cmp(rows, "EUCASS flat elastic endpoint / p_crimp", 3.5643900295147852, ep_el / r["p_crimp"], 1e-9)
    Ro = 124.0 + 3.94 / 2
    r = handbook(210000.0, 0.33, 0.42, 0.42, 3.1, 124.0, 20.0)
    cmp(rows, "transfer40 Vc", 66.359, round(r["Vc"], 3), 1e-6)
    cmp(rows, "transfer40 p_crimp MPa", 1.289324, round(r["p_crimp"], 6), 1e-6)
    for name, ep, g in (("3d24x64 static", 2.855859, 2.215006), ("3d48x128 graded", 2.253992, 1.748197),
                        ("axis192", 2.218066, 1.720333), ("axis24", 2.853333, 2.213046), ("axis384", 2.216077, 1.718791),
                        ("axis48", 2.296584, 1.781232), ("axis48 graded", 2.254362, 1.748484)):
        cmp(rows, f"transfer40 {name} endpoint gamma_crimp", g, round(ep / r["p_crimp"], 6), 2e-6)
    cmp(rows, "transfer40 defect 0.5 x total thickness mm", 1.97, 0.5 * 3.94, 1e-9)
    cmp(rows, "transfer40 width 0.1 R_outer mm", 0.1 * Ro, 0.1 * Ro, 1e-9)
    # card's relative differences in the transfer comparison
    cmp(rows, "transfer40 linear 3d vs fine axis", 0.011519049891403288, 6.446068 / 6.372661 - 1, 1e-6)
    cmp(rows, "transfer40 endpoint 3d vs fine axis", 0.017108607438142576, 2.2539915 / 2.2160775 - 1, 1e-6)
    cmp(rows, "transfer40 endpoint 3d vs matched axis", -0.00016434805057918833, 2.2539915 / 2.254362 - 1, 1e-4)
    cmp(rows, "paper finest 3D vs axisymmetric (card 0.24%)", 0.0024, round(30.28896 / 30.21717 - 1, 4), 1e-9)
    res = {"schema": 1, "rows": rows, "handbook": {f"{a}/{b}": v for (a, b), v in hb.items()},
           "mismatches": [r for r in rows if not r["match"]]}
    json.dump(res, open(sys.argv[1], "w"), indent=1)
    print(len(rows), "rows;", len(res["mismatches"]), "not matching")
    for r in res["mismatches"]:
        print("  ", r["row"], "card", r["card"], "mine", r["mine"], "rel", r["rel"])


if __name__ == "__main__":
    main()
