#!/usr/bin/env python3
"""MAINLINE-045, the deterministic half: the two lead points, 015's map at P2, the lost-core face patch, the P3
frame with one member gone, the film over the merged bay, holes and descent, and the landing valve.
Writes DET.json. This seat's own arithmetic; no sourced threat or impact value enters here."""
import datetime
import json
import math
import os
import sys
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "unpublished-local-ref:d49761785f6805ea"
                   "vacuum-mainline037b-bond-temperature-1020")
import bond37b as b  # noqa: E402  (037b's replica of 028b's least set)
import dt45 as d  # noqa: E402
import p3_022d as q  # noqa: E402

E_BE, NU_BE, SIG_FACE_YIELD = 290e9, 0.0752, 345e6
R = 10.0


def bisect(f, lo, hi, n=80):
    flo = f(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    t0 = time.monotonic()
    out = {"started": datetime.datetime.now().astimezone().isoformat()}
    # ---------------------------------------------------------------- P2: 028b's nominal AF/scarf least set
    u = b.usage_028b(b.base_q())
    checks = []

    def rec(name, mine, theirs, tol):
        checks.append({"check": name, "mine": mine, "theirs": theirs, "ok": abs(mine - theirs) <= tol * max(1.0, abs(theirs))})
    rec("028b usage", u["max_usage"], 0.971978, 2e-6)
    rec("028b gamma needed", u["gamma_need"], 0.564164, 2e-6)
    rec("028b wrinkle needed", u["Q_need"], 0.434628, 2e-6)
    rec("028b face mm", u["tf"] * 1e3, 0.794624, 2e-6)
    rec("028b core mm", u["tc"] * 1e3, 23.2372, 2e-6)
    tf, tc = u["tf"], u["tc"]
    sig_m = b.m.P0 * R / (4.0 * tf)
    teq = d.teq_sandwich(tf, tc)
    w1 = d.width_lambda1(R, teq)
    g_need = u["gamma_need"]
    lam_free = d.lam_plateau(g_need)
    p2 = {"tf_m": tf, "tc_m": tc, "sigma_m_Pa": sig_m, "gamma_need": g_need, "gamma_full": u["gamma_full"],
          "Q_need": u["Q_need"], "usage": u["max_usage"], "Vc": u["Vc"], "others": u["others"], "S_kg": u["S"],
          "J_kg": u["J"], "teq_m": teq, "R_over_teq": R / teq, "length_scale_m": math.sqrt(R * teq),
          "width_lambda1_m": w1, "classical_wavelength_m": 2 * math.pi * math.sqrt(R * teq) / (12 * (1 - 0.33 ** 2)) ** 0.25,
          "lambda_free": lam_free, "width_free_m": lam_free * w1,
          "depth_allow_eq3_lambda1_m": d.x_eq3(g_need) * teq, "depth_allow_lee_envelope_m": d.x_lee(g_need) * teq,
          "lee_x_at_need": d.x_lee(g_need), "eq3_x_at_need": d.x_eq3(g_need)}
    # allowed depth against the dent's 1/e radius
    p2["depth_vs_width"] = []
    for r0 in (0.005, 0.01, 0.025, 0.05, 0.1, 0.15, 0.2, 0.225, 0.25, 0.3, 0.357, 0.5, 0.75, 1.0, 1.5):
        lam = r0 / w1
        da = d.depth_allowed(g_need, lam, teq) if lam <= 5.0 else None
        p2["depth_vs_width"].append({"r0_m": r0, "lambda": lam, "plateau": d.plateau(lam),
                                     "depth_allowed_m": (None if da is None or math.isinf(da) else da),
                                     "unlimited": bool(da is not None and math.isinf(da))})
    # a face patch that has lost its core (crushed or disbonded), at the working stress
    p2["patch"] = {}
    for edge in ("clamped", "ss"):
        Dc = d.patch_diameter(tf, sig_m, E_BE, NU_BE, edge)
        p2["patch"][edge] = {"D_crit_m": Dc}
    # the face at a hole edge: elastic hoop stress 2 sigma_m, and the plastic ring at 345 MPa (Tresca, plane stress)
    p2["hole_edge"] = {"elastic_edge_stress_Pa": 2 * sig_m, "factor_on_345": SIG_FACE_YIELD / (2 * sig_m),
                       "plastic_ring_over_hole_radius": SIG_FACE_YIELD / (2 * (SIG_FACE_YIELD - sig_m))}
    out["p2"] = p2
    # ---------------------------------------------------------------- P3: 022d's best equilateral screened point
    pt = q.lam_point(3.1707585691074884, 0.27508285638020646 / 2, 0.00010944022237810727)
    rec("022d least SF", pt["lam"], 1.258252477, 1e-9)
    rec("022d tube kg", pt["m_tube"], 4183.590023, 1e-9)
    rec("022d film kg", pt["m_film"], 214.541558, 1e-8)
    rec("022d joint kg", pt["m_joint"], 44.191468, 1e-8)
    rec("022d sag kg", pt["sag"], 99.720419, 1e-8)
    p3 = {k: pt[k] for k in ("s", "L", "ro", "t", "A", "I", "N", "members", "nodes", "m_tube", "m_film", "m_joint",
                             "m_nodes", "sag", "lam", "half_over_L", "gamma_local")}
    p3["modes"] = pt["modes"]
    p3["film_stress_Pa"] = q.P * pt["s"] / (2 * 0.00010944022237810727)
    p3["film_line_load_N_per_m"] = q.P * pt["s"] / 2
    p3["ply_fibre_stress_Pa"] = 2 * p3["film_stress_Pa"]
    p3["bay_area_m2"] = math.sqrt(3) / 4 * pt["s"] ** 2
    p3["stress_axial_Pa"] = pt["N"] / pt["A"]
    p3["projected_tube_cover_fraction"] = (3.0 * math.sqrt(3) / pt["s"]) / 1.0 * pt["ro"] * 2 / 3.0 * 1.0
    # tube length per area 2 sqrt(3)/s for a triangular lattice; covered fraction = that times OD
    p3["tube_length_per_m2"] = 2 * math.sqrt(3) / pt["s"]
    p3["projected_tube_cover_fraction"] = p3["tube_length_per_m2"] * 2 * pt["ro"]
    out["p3"] = p3
    # ---------------------------------------------------------------- the frame with one member gone
    frame = {}
    nu_sic = 0.16
    for f in (4, 5):
        X, E_, T_ = d.geodesic(f, R)
        base, c0, _ = d.frame_solve(X, E_, T_, q.P, pt["A"], pt["I"], q.E_SIC, nu_sic)
        N0 = np.array([r["N"] for r in base])
        M0 = np.array([r["M"] for r in base])
        sig0 = np.abs(np.minimum(N0, 0)) / pt["A"] + M0 * pt["ro"] / pt["I"]
        val = np.zeros(len(X), int)
        for i, j in E_:
            val[i] += 1
            val[j] += 1
        cands = [k for k, (i, j) in enumerate(E_) if val[i] == 6 and val[j] == 6]
        k_med = min(cands, key=lambda k: abs(N0[k] - np.median(N0)))
        rows = []
        for tag, k in (("median member", k_med), ("most compressed member", int(np.argmin(N0)))):
            res, c1, _ = d.frame_solve(X, E_, T_, q.P, pt["A"], pt["I"], q.E_SIC, nu_sic, removed=(k,))
            keep = [kk for kk in range(len(E_)) if kk != k]
            N1 = np.array([r["N"] for r in res])
            M1 = np.array([r["M"] for r in res])
            sig1 = np.abs(np.minimum(N1, 0)) / pt["A"] + M1 * pt["ro"] / pt["I"]
            ten1 = np.maximum(M1 * pt["ro"] / pt["I"] - np.maximum(-N1, 0) / pt["A"], 0)
            i0, j0 = E_[k]
            nb = [n for n, kk in enumerate(keep) if (set(E_[kk]) & {i0, j0})]
            rows.append({"case": tag, "removed_N_kN": float(N0[k] / 1e3), "neighbours": len(nb),
                         "neighbour_N_ratio_max": float(np.max(N1[nb] / N0[keep][nb])),
                         "N_ratio_max_anywhere": float(np.max(N1 / N0[keep])),
                         "M_max_Nm": float(M1.max()), "M_max_intact_Nm": float(M0.max()),
                         "sigma_max_Pa": float(sig1.max()), "sigma_max_intact_Pa": float(sig0.max()),
                         "sigma_ratio": float(sig1.max() / sig0.max()), "tension_max_Pa": float(ten1.max())})
        _, cp0, _ = d.frame_solve(X, E_, T_, q.P, pt["A"], pt["I"], q.E_SIC, nu_sic, pinned=True)
        _, cp1, _ = d.frame_solve(X, E_, T_, q.P, pt["A"], pt["I"], q.E_SIC, nu_sic, removed=(k_med,), pinned=True)
        L = np.array([np.linalg.norm(X[j] - X[i]) for i, j in E_])
        frame[f"f{f}"] = {"nodes": len(X), "members": len(E_), "edge_min_m": float(L.min()), "edge_max_m": float(L.max()),
                          "edge_mean_m": float(L.mean()), "N_intact_min_kN": float(N0.min() / 1e3),
                          "N_intact_max_kN": float(N0.max() / 1e3), "N_theory_kN": float(-q.P * R * L.mean() / (2 * math.sqrt(3)) / 1e3),
                          "rigid_joint_cases": rows, "pinned_intact_cond": float(cp0), "pinned_one_gone_cond": float(cp1)}
    out["frame"] = frame
    # ---------------------------------------------------------------- the film over the two bays a lost member leaves
    s = pt["s"]
    b_tri = s / (2 * math.sqrt(3))                       # inradius of the bay
    b_rhomb = s * math.sin(math.pi / 3) / 2              # inradius of the 60-degree rhombus the two bays make
    out["film_merged_bay"] = {"inradius_triangle_m": b_tri, "inradius_rhombus_m": b_rhomb,
                              "tension_ratio_same_rise_to_span": b_rhomb / b_tri,
                              "film_SF_after": pt["modes"]["film"] / (b_rhomb / b_tri)}
    # ---------------------------------------------------------------- holes and descent
    T5, p5, rho5 = d.isa(500.0)
    holes = []
    for dia in (0.001, 0.003, 0.01, 0.03, 0.1):
        A = math.pi * (dia / 2) ** 2
        md = d.mdot_hole(A, 0.6, p5, T5, 0.0)
        tend = min(4.0e6, 2.7e5 * (0.01 / dia) ** 2 * 3)
        row = {"hole_m": dia, "mdot_kg_s": md, "t_48p9_h": 48.894 / md / 3600, "t_411_h": 411.2989 / md / 3600,
               "t_244_h": 244.4721 / md / 3600}
        for lead, wall in (("p2", 0.024), ("p3", 0.0)):
            for cdd in (0.47, 0.2):
                o = d.descent(A, 0.6, wall=wall, m_hull=None, cd_drag=cdd, t_end=tend)
                row[f"{lead}_cd{cdd}"] = o
        holes.append(row)
    out["holes"] = holes
    big = []
    for label, area, tend in (("P3 one torn bay", math.sqrt(3) / 4 * s * s, 600.0),
                              ("P2 hole 0.3 m", math.pi * 0.15 ** 2, 3000.0), ("P2 hole 1 m", math.pi * 0.5 ** 2, 1000.0)):
        for cdd in (0.47, 0.2):
            big.append({"case": label, "area_m2": area, "cd_drag": cdd,
                        **d.descent(area, 0.6, wall=0.0, m_hull=None, cd_drag=cdd, t_end=tend)})
    out["big_holes"] = big
    # hole diameter at which touchdown reaches 0.914 m/s (TAR 473's landing floor) and 4.2 m/s (14 CFR 31.27(c))
    thr = {}
    for vlim in (0.914, 4.2):
        for cdd in (0.47, 0.2):
            def f(dia, vlim=vlim, cdd=cdd):
                A = math.pi * (dia / 2) ** 2
                o = d.descent(A, 0.6, wall=0.024, m_hull=None, cd_drag=cdd, t_end=2.0e5)
                return abs(o["v_end_m_s"]) - vlim
            thr[f"v{vlim}_cd{cdd}"] = bisect(f, 0.02, 1.0, n=40)
    out["touchdown_thresholds_hole_m"] = thr
    # the landing valve: inflow that holds the 500 m pressure difference during a descent at speed v
    valve = []
    T0, p0, rho0 = d.isa(0.0)
    V = 4.0 / 3.0 * math.pi * R ** 3
    for v in (0.914, 2.0, 7.5):
        md = V / (d.R_AIR * T0) * rho0 * d.G0 * v
        A1 = md / d.mdot_hole(1.0, 0.6, p0, T0, 0.0)
        valve.append({"descent_m_s": v, "mdot_kg_s": md, "area_m2": A1, "diameter_m": 2 * math.sqrt(A1 / math.pi)})
    out["landing_valve"] = valve
    # neutral-buoyancy pressure difference: dp = M R T / V, independent of altitude at fixed temperature
    out["neutral_dp_note"] = {"dp_500_Pa": p5, "dp_ground_isa_Pa": p5 * 288.15 / T5, "ratio": 288.15 / T5}
    out["checks"] = checks
    assert all(c["ok"] for c in checks), [c for c in checks if not c["ok"]]
    out["ended"] = datetime.datetime.now().astimezone().isoformat()
    out["elapsed_s"] = time.monotonic() - t0
    with open(os.path.join(HERE, "DET.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "DET.json.tmp"), os.path.join(HERE, "DET.json"))
    print("elapsed", round(out["elapsed_s"], 1), "checks", len(checks))


if __name__ == "__main__":
    main()
