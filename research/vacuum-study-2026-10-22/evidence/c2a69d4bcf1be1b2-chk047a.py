#!/usr/bin/env python3
"""CHECK-047 part A: this checker's own arithmetic against MAINLINE-047's filed numbers (no owner code read or run).

Each row records the card's value, this checker's value and whether they agree. Inputs are the owner's filed data
files (as data), the source reports they inherit from, and the pinned source documents. Writes A-ARITH.json."""
import csv
import json
import math
import os

import numpy as np
from scipy import integrate, optimize

HERE = os.path.dirname(os.path.abspath(__file__))
O = "unpublished-local-ref:0286370e2b9e2809"
WS = "unpublished-local-ref:7a5bf1cec24b249e"
PSI = 0.006894757293168361
ROWS = []


def row(name, card, mine, tol=0, note=""):
    if isinstance(tol, str):
        note, tol = tol, 0
    if isinstance(card, (int, float)) and isinstance(mine, (int, float)):
        ok = abs(card - mine) <= tol * max(1.0, abs(card)) if tol < 1 else abs(card - mine) <= tol
    else:
        ok = card == mine
    ROWS.append({"check": name, "card": card, "mine": mine, "tolerance": tol, "agrees": bool(ok), "note": note})
    print(("ok  " if ok else "DIFF"), name, "| card", card, "| mine", mine, ("| " + note) if note else "")
    return ok


def rms_exact(a, w, R=10000.0):
    """RMS about the prescribed sphere of d = a exp(-(R th / w)^2), integrated over the full sphere."""
    f = lambda th: (a * math.exp(-(R * th / w) ** 2)) ** 2 * math.sin(th)
    v, _ = integrate.quad(f, 0, math.pi, points=[w / R, 3 * w / R], limit=400, epsabs=1e-22, epsrel=1e-13)
    return math.sqrt(0.5 * v)


def stvk_D(En, Gw_m, Gl_h, Ein, Gin):
    """Voigt stiffness on (E11, E22, E33, 2E12, 2E13, 2E23) in axes 1 = meridian, 2 = normal, 3 = hoop, zero Poisson."""
    return np.diag([Ein, En, Ein, Gw_m, Gin, Gl_h])


def S_of(E, D):
    v = np.array([E[0, 0], E[1, 1], E[2, 2], 2 * E[0, 1], 2 * E[0, 2], 2 * E[1, 2]])
    s = D @ v
    return np.array([[s[0], s[3], s[4]], [s[3], s[1], s[5]], [s[4], s[5], s[2]]])


def d2W(E, D, a, N, Fs):
    """Exact StVK rank-one second variation |a|^2 N.S.N + sym(F^T a x N):C:sym(F^T a x N)."""
    S = S_of(E, D)
    b = Fs.T @ a
    X = 0.5 * (np.outer(b, N) + np.outer(N, b))
    return float(a @ a) * float(N @ S @ N) + float(np.tensordot(X, S_of(X, D), 2))


def acoustic_min(E, D, starts=60, seed=1):
    C = np.eye(3) + 2 * E
    Fs = np.linalg.cholesky(C).T                       # upper factor, Fs^T Fs = C
    rng = np.random.default_rng(seed)

    def unit(p):
        t1, f1, t2, f2 = p
        return (np.array([math.sin(t1) * math.cos(f1), math.sin(t1) * math.sin(f1), math.cos(t1)]),
                np.array([math.sin(t2) * math.cos(f2), math.sin(t2) * math.sin(f2), math.cos(t2)]))
    best = None
    for _ in range(starts):
        p0 = rng.uniform([0, 0, 0, 0], [math.pi, 2 * math.pi, math.pi, 2 * math.pi])
        r = optimize.minimize(lambda p: d2W(E, D, *unit(p), Fs), p0, method="Nelder-Mead",
                              options={"xatol": 1e-10, "fatol": 1e-14, "maxiter": 4000})
        if best is None or r.fun < best.fun:
            best = r
    return best.fun


def main():
    R = json.load(open(f"{O}/RESULTS.json"))
    cf = R["core_fold"]
    # ---- target pressure: ISA at 500 m, and SF 1.05
    p = 101325 * (1 - 0.0065 * 500 / 288.15) ** (9.80665 * 0.0289644 / (8.31432 * 0.0065)) / 1000
    row("service pressure = ISA 500 m (US 1976 constants, R* = 8.31432)", R["required_pressure_kPa"], p, 1e-7,
        f"agrees to {abs(p - R['required_pressure_kPa']) / p:.1e} relative; the constant set differs beyond the 8th digit")
    row("SF 1.05 target", R["SF105_pressure_kPa"], 1.05 * R["required_pressure_kPa"], 1e-12)
    # ---- geometry inherited through 037b (this seat's own record)
    b37 = json.load(open(f"{WS}/ref-4189c1615990eb515921/.ship/work/outputs/vacuum-mainline037b-bond-temperature-1020/RESULTS.json"))
    fx = b37["compute"]["fixes"][0]["without_residual"]
    row("face thickness (028b via 037b)", 0.794624066985892, fx["tf_mm"], 1e-12)
    row("core thickness (028b via 037b)", 23.23721790601544, fx["tc_mm"], 1e-12, "differs in the 15th digit only")
    sf = b37["compute"]["scarf_fix"][1]
    row("037b scarf ratio", 30.34139731914874, sf["r_need"], 1e-12)
    row("037b residual face compression, MPa", 3.41022257, sf["sigma_res_lead_MPa"], 1e-9)
    row("cure-debit yield screen, MPa", 341.58977743, 345 - 3.41022257, 1e-12)
    tf, tc, Ro = 0.794624066985892, 23.23721790601544, 10000.0
    # ---- classical lengths
    nu = 0.0768
    teq = math.sqrt(3) * (tc + tf)
    w15 = math.sqrt(Ro * teq) / (12 * (1 - nu ** 2)) ** 0.25
    row("classical length w = sqrt(R t_eq)/[12(1-nu^2)]^1/4", 347.1529189, w15, 1e-9)
    h = tc + tf
    D_over_A = (tf * h ** 2 / 2 + 2 * tf ** 3 / 12) / (2 * tf)        # bending / membrane stiffness, faces only
    teq2 = math.sqrt(12 * D_over_A)
    w15b = math.sqrt(Ro * teq2) / (12 * (1 - nu ** 2)) ** 0.25
    row("classical length with face bending", 347.1845439, w15b, 1e-9)
    row("full classical wavelength 2 pi w", 2181.424825, 2 * math.pi * w15b, 1e-9)
    # ---- widths and moduli inherited from 029
    r29 = json.load(open(f"{WS}/ref-ed3515d83349998d6b1b/.ship/work/outputs/vacuum-mainline029-crimp-gamma-fe-1020/RESULTS.json"))
    ws29 = sorted(set(round(x["width_mm"], 10) for x in r29["elastic_sensitivities"]))
    row("width 332.2164186 in 029", True, any(abs(x - 332.2164186283597) < 1e-9 for x in ws29))
    row("width 401.8559050 in 029", True, any(abs(x - 401.8559050423529) < 1e-9 for x in ws29))
    norms = [n["G_meridian_MPa"] for n in r29["normalizations"]]
    row("G_L = 15 ksi (CR III Table II)", 103.4213594, 15000 * PSI, 1e-9)
    row("G_W = 6.8 ksi (CR III Table II)", 46.8843496, 6800 * PSI, 1e-9)
    row("029 carries both shear moduli", True, any(abs(g - 15000 * PSI) < 1e-6 for g in norms) and any(abs(g - 6800 * PSI) < 1e-6 for g in norms))
    # ---- core strengths (CR III Table II, 5056 3/8 1.0 pcf row read from the pinned PDF text)
    txt = open("unpublished-local-ref:413d063c9d334c35").read().splitlines()
    t2 = next(i for i, l in enumerate(txt) if "Table II" in l and "5056" in l)
    r38 = next(l for l in txt[t2:] if l.split()[:2] == ["3/8", "1.0"]).split()
    vals = [float(x) for x in r38[2:]]
    # columns: bare typ, bare min, stab typ, stab min, comp modulus ksi, crush typ, L typ, L min, L mod ksi, W typ, W min, W mod ksi
    row("CR III 1.0 pcf row (L typ, L min, W typ, W min, crush)", [55, 45, 35, 25, 35], [vals[6], vals[7], vals[9], vals[10], vals[5]], 0)
    row("CR III moduli ksi (compressive, L, W)", [15.0, 15.0, 6.8], [vals[4], vals[8], vals[11]], 0)
    for lab, psi, card in (("S_W min avg", 25, 0.172369), ("S_L min avg", 45, 0.310264), ("S_W typical", 35, 0.241317), ("S_L typical", 55, 0.379212)):
        row(f"{lab} MPa", card, round(psi * PSI, 6), 0, "rounded to the card's 6 decimals")
    # ---- perfect sphere, membrane statics (both faces carry the hemisphere load)
    Ri = Ro - 2 * tf - tc
    sig = 0.09546083791390515 * Ro ** 2 / (2 * tf * (Ro + Ri))         # MPa at service, equal face stress
    pc = cf["perfect_cases"]
    for y in (255, 300, 345):
        py = R["required_pressure_kPa"] * y / sig
        br = pc[f"{y}-W"]["first_yield_bracket_kPa"]
        row(f"perfect sphere first yield {y} MPa inside the card bracket", True, br[0] <= py <= br[1],
            f"membrane estimate {py:.4f} kPa; bracket {br}; endpoint {pc[f'{y}-W']['endpoint_kPa']}")
    row("perfect sphere face stress at service, MPa (membrane, equal faces)", 300.7068, sig, 1e-5, "own value; the card prints no number")
    # ---- governing boundaries: linear estimate, RMS, ratios
    g = cf["governing_boundaries"]
    for sf_, card_amp, card_rms in (("1.0", 1.2191760361482857, 14.32), ("1.05", 0.7477706794756136, 8.78)):
        b = g[sf_]
        est = b["passing_amplitude_mm"] + (345 - b["passing_face_MPa"]) / (b["failing_face_MPa"] - b["passing_face_MPa"]) * (
            b["failing_amplitude_mm"] - b["passing_amplitude_mm"])
        row(f"SF {sf_} amplitude estimate by linear interpolation of face stress", card_amp, est, 1e-9)
        r_est = rms_exact(est, b["width_mm"])
        row(f"SF {sf_} single-Gaussian RMS, micrometres (exact sphere integral)", card_rms, round(r_est * 1000, 2), 0)
        row(f"SF {sf_} RMS bracket agrees to 1e-9", True, all(abs(x - y) < 1e-9 for x, y in zip(
            b["rms_bracket_mm"], [rms_exact(b["passing_amplitude_mm"], b["width_mm"]), rms_exact(b["failing_amplitude_mm"], b["width_mm"])])))
        sp = est * b["width_mm"] / (math.sqrt(8) * Ro)
        row(f"SF {sf_} small-patch RMS a w/(sqrt 8 R) against the exact integral, nm", round(r_est * 1e6, 3), round(sp * 1e6, 3), 1e-4,
            f"the small-patch form is {(sp / r_est - 1):.1e} high; the card uses the exact integral, as it states")
        ratio = b["passing_core_shear_MPa"] / (25 * PSI)
        tau_h = math.sqrt(max(0.0, b["passing_core_index"] ** 2 - ratio ** 2)) * 45 * PSI
        row(f"SF {sf_} core index >= meridian shear / S_W (quadratic interaction adds the hoop term)", True,
            b["passing_core_index"] >= ratio - 1e-12, f"index {b['passing_core_index']:.7f}, ratio {ratio:.7f}, implied hoop shear {tau_h:.5f} MPa")
    r42 = json.load(open(f"{WS}/ref-55cff924be25afe6f9dd/.ship/work/outputs/vacuum-mainline042-build-route-1020/RESULTS.json"))
    lo, hi = r42["gamma_need_028b"]["lee_amp_mm"], r42["gamma_need_028b"]["eq3_amp_mm"]
    row("042's mapped amplitudes, mm", [9.32, 16.06], [round(lo, 2), round(hi, 2)], 0)
    a1 = g["1.0"]["amplitude_estimate_mm"]
    row("ratio to 042, low", 7.6, round(lo / round(a1, 3), 1), 0, f"{lo / a1:.3f} with the unrounded estimate")
    row("ratio to 042, high", 13.2, round(hi / round(a1, 3), 1), 0, f"{hi / a1:.3f}")
    r15 = json.load(open(f"{WS}/ref-cca93dbfd236dcaa3a8b/.ship/work/outputs/vacuum-mainline015b-kd-precision-fix-1020/RESULTS.json"))
    txt15 = json.dumps(r15)
    row("015b's own RMS 0.1393 and 0.6544 mm are in 015b", True, '"filed_gamma_eq3_rms_mm": "0.1393"' in txt15 and '"filed_gamma_eq3_rms_mm": "0.6544"' in txt15,
        "the card quotes 015b's values at 015b's widths (333.96 and 403.97 mm), not recomputed at 047's widths")
    row("015b 11.801 mm at 333.964 mm, small-patch RMS", 0.1393, round(11.801408250115193 * 333.96413471140424 / (math.sqrt(8) * Ro), 4), 0)
    row("015b 45.819 mm at 403.970 mm, small-patch RMS", 0.6544, round(45.819441454003304 * 403.96997884764135 / (math.sqrt(8) * Ro), 4), 0)
    # ---- the eight tested boundaries: card table against the filed CORE-BOUNDARIES rows
    cb = json.load(open(f"{O}/CORE-BOUNDARIES.json"))
    card_tab = {(332.216, "W"): (1.209, 1.227, 0.738, 0.756, 0.119693, 0.6944), (332.216, "L"): (1.796, 1.811, 1.111, 1.129, 0.131763, 0.4247),
                (347.153, "W"): (1.223, 1.241, 0.748, 0.766, 0.115260, 0.6687), (347.153, "L"): (1.798, 1.816, 1.114, 1.132, 0.126322, 0.4071),
                (401.856, "W"): (1.284, 1.302, 0.789, 0.807, 0.101647, 0.5897), (401.856, "L"): (1.821, 1.839, 1.136, 1.154, 0.109734, 0.3537),
                (2181.425, "W"): (21.127, 21.217, 14.262, 14.352, 0.012361, 0.0717), (2181.425, "L"): (21.271, 21.358, 14.299, 14.389, 0.013029, 0.0420)}
    for grp in cb:
        key = (round(grp["width_mm"], 3), grp["meridian"])
        bs = {(b["SF"], b["strength_basis"]): b for b in grp["boundaries"]}
        b1, b5 = bs[(1.0, "minimum_average")], bs[(1.05, "minimum_average")]
        S_m = (25 if grp["meridian"] == "W" else 45) * PSI
        mine = (round(b1["passing_amplitude_mm"], 3), round(b1["failing_amplitude_mm"], 3), round(b5["passing_amplitude_mm"], 3),
                round(b5["failing_amplitude_mm"], 3), round(b1["passing_core_shear_MPa"], 6), round(b1["passing_core_shear_MPa"] / S_m, 4))
        row(f"boundary table {key}", list(card_tab[key]), list(mine), 0)
        for bb in grp["boundaries"]:
            pass_ok = bb["passing_face_MPa"] <= bb["face_yield_MPa"] and bb["failing_face_MPa"] > bb["face_yield_MPa"] if bb["governing"] == "face_yield" else None
            if pass_ok is not None and not pass_ok:
                row(f"face stress straddles yield {key} SF {bb['SF']} {bb['strength_basis']}", True, False)
    # ---- endpoint division by 1.10
    cal = json.load(open(f"{O}/CORE-CALIBRATION.json"))
    gb = cal["global_bracket"]
    target = R["required_pressure_kPa"]
    for side in ("passing", "failing"):
        s = gb[side]
        cap = min(s["endpoint_kPa"] / 1.1, s["face_yield_bracket"][0])
        row(f"1.10 division, {side} capacity kPa", s["capacity_kPa"], cap, 1e-9)
    row("1.10 division: passing side passes, failing side fails", True, gb["passing"]["capacity_kPa"] >= target > gb["failing"]["capacity_kPa"])
    row("1.10 bracket, mm", [0.521, 0.539], [round(gb["passing"]["amplitude_mm"], 3), round(gb["failing"]["amplitude_mm"], 3)], 0)
    for c in cal["common_passing_checks"]:
        cap = min(c["endpoint_kPa"] / 1.1, c["face_yield_bracket"][0])
        if not cap >= target:
            row(f"common passing amplitude passes {c['label']} {c['meridian']}", True, False, f"capacity {cap}")
    row("all eight footprints pass at 0.520967 mm", True, all(min(c["endpoint_kPa"] / 1.1, c["face_yield_bracket"][0]) >= target
                                                             for c in cal["common_passing_checks"]))
    pe = pc["345-W"]["endpoint_kPa"]
    row("perfect sphere 345: endpoint / 1.10 below the SF 1.05 target", True, pe / 1.1 < R["SF105_pressure_kPa"], f"{pe / 1.1:.4f} < {R['SF105_pressure_kPa']:.4f}")
    row("1.10 global estimate RMS, mm", gb["rms_estimate_mm"], rms_exact(gb["estimate_mm"], gb["width_mm"]), 1e-9)
    c29 = json.load(open(f"{WS}/ref-55cff924be25afe6f9dd/.ship/work/outputs/vacuum-mainline029-check-1020/RESULTS.json"))
    fs = [x["card"] for x in c29["text_and_record_arithmetic"] if isinstance(x.get("card"), float) and 2.2 < x["card"] < 2.5]
    row("transfer factors 2.3146-2.4589 (CHECK-029 record)", [2.3146, 2.4589], [round(min(fs), 4), round(max(fs), 4)], 0)
    row("perfect-sphere endpoint / 2.3146 below service: no admissible amplitude", True, pe / 2.3146 < target, f"{pe / 2.3146:.2f} kPa")
    # ---- cure debit boundaries
    td = cf["thermal_debit"]
    bt = {(b["SF"], b["strength_basis"]): dict(b, width_mm=td["width_mm"]) for b in td["boundaries"]}
    for sf_, card_br, card_rms in ((1.0, [1.117, 1.135], 13.30), (1.05, [0.653, 0.671], 7.83)):
        b = bt[(sf_, "minimum_average")]
        row(f"cure-debit SF {sf_} bracket", card_br, [round(b["passing_amplitude_mm"], 3), round(b["failing_amplitude_mm"], 3)], 0)
        est = b["passing_amplitude_mm"] + (b["face_yield_MPa"] - b["passing_face_MPa"]) / (b["failing_face_MPa"] - b["passing_face_MPa"]) * (
            b["failing_amplitude_mm"] - b["passing_amplitude_mm"])
        row(f"cure-debit SF {sf_} RMS, micrometres", card_rms, round(rms_exact(est, b["width_mm"]) * 1000, 2), 0, f"estimate {est:.6f} mm")
    # ---- larger dimples table against the filed sweep
    sw = {(round(x["width_mm"], 1), x["meridian"], x["amplitude_mm"]): x for x in cf["sweep"]}
    card_big = {(332.2, "W", 11.8): (61.910, 22.651, 68.629), (332.2, "W", 46.0): (44.707, 12.043, 56.953),
                (401.9, "W", 11.8): (57.215, 26.202, 64.857), (401.9, "W", 46.0): (41.429, 11.631, 51.485),
                (2181.4, "W", 11.8): (101.910, None, 102.152), (2181.4, "W", 46.0): (77.457, None, 78.330)}
    for k, (fy, cs, ep) in card_big.items():
        x = sw[k]
        csm = x["first_core_shear"]["minimum_average"]
        mine = (round(x["first_face_yield_estimate_kPa"], 3), None if csm.get("estimate_kPa") is None else round(csm["estimate_kPa"], 3),
                round(x["endpoint_kPa"], 3))
        row(f"larger dimple {k}", [fy, cs, ep], list(mine), 0)
    # ---- the inherited-law acoustic probe, recomputed from its filed state
    pr = cf["inherited_core_acoustic_probe"]
    E = np.array(pr["green_strain"])
    Dinh = stvk_D(15000 * PSI, 6800 * PSI, 15000 * PSI, 0.01, 0.005)
    Fs = np.linalg.cholesky(np.eye(3) + 2 * E).T
    a = np.array(pr["polarization_in_cholesky_frame"]); a = a / np.linalg.norm(a)
    Nn = np.array(pr["reference_wave_direction"]); Nn = Nn / np.linalg.norm(Nn)
    row("inherited probe second variation, MPa (its own a, N, E)", pr["minimum_sampled_acoustic_eigenvalue_MPa"], d2W(E, Dinh, a, Nn, Fs), 1e-6,
        "W orientation: meridian shear modulus 6.8 ksi")
    row("inherited probe exact minimum over a and N is negative", True, acoustic_min(E, Dinh) < 0, f"{acoustic_min(E, Dinh):.6f} MPa")
    # ---- simple-shear ellipticity limits of the two laws (radial-meridian shear, W orientation)
    out = {}
    for lab, Ein, Gin in (("inherited", 0.01, 0.005), ("regularized", 1.0, 0.5)):
        D = stvk_D(15000 * PSI, 6800 * PSI, 15000 * PSI, Ein, Gin)
        def lam(tau, sense):
            gam = tau / (6800 * PSI)
            F = np.eye(3)
            if sense == "m_on_n":
                F[0, 1] = gam                    # meridian displacement varies through the thickness
            else:
                F[1, 0] = gam
            E_ = 0.5 * (F.T @ F - np.eye(3))
            return acoustic_min(E_, D, starts=24, seed=3)
        res = {}
        for sense in ("m_on_n", "n_on_m"):
            hi_ = 0.5 if lab == "inherited" else 3.0
            if lam(hi_, sense) > 0:
                res[sense] = f"> {hi_}"
                continue
            res[sense] = optimize.brentq(lambda t: lam(t, sense), 1e-4, hi_, xtol=1e-5)
        out[lab] = res
        print(lab, res)
    row("inherited law: simple-shear loss of ellipticity, MPa (CHECK-029 found about 0.088)", 0.088,
        min(v for v in out["inherited"].values() if isinstance(v, float)), 0.15, "own exact minimisation; both shear senses")
    row("regularized law: no loss of ellipticity below 0.5 MPa simple shear", True,
        all((not isinstance(v, float)) or v > 0.5 for v in out["regularized"].values()), json.dumps(out["regularized"]))
    with open(os.path.join(HERE, "A-ARITH.json.tmp"), "w") as fh:
        json.dump({"tag": "QUESTIONABLE/PROJECTION", "rows": ROWS, "simple_shear_ellipticity_MPa": out}, fh, indent=1, default=str)
    os.replace(os.path.join(HERE, "A-ARITH.json.tmp"), os.path.join(HERE, "A-ARITH.json"))
    print(sum(r["agrees"] for r in ROWS), "of", len(ROWS), "agree")


if __name__ == "__main__":
    main()
