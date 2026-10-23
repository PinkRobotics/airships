#!/usr/bin/env python3
"""CHECK-047 part B: this checker's own CalculiX model (fe047.py, runall.py) against MAINLINE-047's filed numbers.

Crossings are linear interpolations between this model's two runs (or two pressure steps) that straddle the limit,
the same estimator the card states. Writes B-FE.json."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FE = os.path.join(HERE, "fe")
O = "unpublished-local-ref:0286370e2b9e2809"
P1 = 95.46083791390515
P105 = 1.05 * P1
ROWS = []


def res(name):
    return json.load(open(os.path.join(FE, name, "result.json")))


def frame(name, p):
    return next(f for f in res(name)["frames"] if abs(f.get("pressure_kPa", -1) - p) < 1e-6)


def cross(x0, y0, x1, y1, y):
    return x0 + (y - y0) / (y1 - y0) * (x1 - x0)


def row(name, card, mine, tol=0, note=""):
    if isinstance(tol, str):
        note, tol = tol, 0
    if card is None or mine is None:
        ok = None
    elif isinstance(card, bool) or isinstance(mine, bool):
        ok = card == mine
    else:
        ok = abs(card - mine) <= tol
    ROWS.append({"check": name, "card": card, "mine": mine, "difference": None if ok is None or isinstance(card, bool) else mine - card, "tolerance": tol,
                 "agrees": ok, "note": note})
    print(("ok  " if ok else "DIFF" if ok is False else "info"), name, "| card", card, "| mine", mine, ("| " + note) if note else "")


def main():
    R = json.load(open(f"{O}/RESULTS.json"))
    cf = R["core_fold"]
    out = {}
    # ---- perfect sphere: first yield on the pre-yield branch (own steps at the card's bracket pressures)
    pf = res("perfect-W-hi")["frames"]
    byp = {round(f["pressure_kPa"], 6): f["face_mises_max"] for f in pf}
    for ys, (lo, hi), est in ((255, (80.1, 81.0), 80.97427573789561), (300, (94.95, 95.2875), 95.27981155403744),
                              (345, (109.51875, 109.645308), 109.59013059273423)):
        s_lo, s_hi = byp[round(lo, 6)], byp[round(hi, 6)]
        row(f"perfect sphere {ys} MPa: own stress below yield at the card's lower bracket, above at its upper", True, s_lo < ys < s_hi,
            f"{s_lo:.3f} / {s_hi:.3f} MPa")
        row(f"perfect sphere {ys} MPa first yield, kPa (interpolated)", est, cross(lo, s_lo, hi, s_hi, ys), 0.02)
    for ys, card in ((345, 109.68211799999999), (300, 95.36283), (255, 81.044172)):
        try:
            row(f"perfect sphere {ys} MPa numerical endpoint, kPa", card, res(f"e-perfect-{ys}").get("endpoint_kPa"), 0.1,
                "last converged follower-pressure increment of own run")
        except FileNotFoundError:
            row(f"perfect sphere {ys} MPa numerical endpoint, kPa", card, None, 0.1, "run missing")
    # ---- governing W 332.216 brackets
    g = cf["governing_boundaries"]
    for sf, p, (a0, a1), card_est, yld in (("1.0", P1, (1.208988, 1.226988), g["1.0"]["amplitude_estimate_mm"], 345.0),
                                           ("1.05", P105, (0.737936, 0.755936), g["1.05"]["amplitude_estimate_mm"], 345.0)):
        f0, f1 = frame(f"g-W332-a{a0}-hi", p), frame(f"g-W332-a{a1}-hi", p)
        b = g[sf]
        row(f"SF {sf} passing amplitude {a0}: max face stress, MPa", b["passing_face_MPa"], f0["face_mises_max"], 0.7,
            f"own max at s = {f0['face_max_s_mm']:.0f} mm, {f0['face_max_layer']} face")
        row(f"SF {sf} failing amplitude {a1}: max face stress, MPa", b["failing_face_MPa"], f1["face_mises_max"], 0.7,
            f"own max at s = {f1['face_max_s_mm']:.0f} mm, {f1['face_max_layer']} face")
        row(f"SF {sf} own pass at {a0} and fail at {a1}", True, f0["face_mises_max"] <= yld < f1["face_mises_max"])
        est = cross(a0, f0["face_mises_max"], a1, f1["face_mises_max"], yld)
        row(f"SF {sf} tolerance estimate, mm", card_est, est, 0.018, "within one bracket width (0.018 mm) counts as reproduced")
        row(f"SF {sf} passing core shear, MPa (current material frame)", b["passing_core_shear_MPa"], abs(f0["core_tau_meridian"]), 0.003)
        row(f"SF {sf} passing core index (minimum average)", b["passing_core_index"], f0["core_index_min_avg"], 0.02)
        row(f"SF {sf} passing core compression, MPa", b["passing_core_compression_MPa"], f0["core_max_compression"], 0.003)
        row(f"SF {sf} own minimum sufficient acoustic bound at the passing state, MPa (card's minimum 0.314142 over all passing states)",
            None, f0["core_min_sufficient_bound"], 0, "positive = locally strongly elliptic by the card's own sufficient bound")
        out[f"SF{sf}"] = {"estimate_mm": est, "passing": f0, "failing": f1}
        for amp, side in ((a0, "passing"), (a1, "failing")):
            try:
                fp = frame(f"p-W332-a{amp}-345", p)
                yielded = fp.get("peeq_max", 0) > 1e-10
                row(f"SF {sf} 345 MPa own run at {amp}: yields = {side == 'failing'}", True, yielded == (side == "failing"),
                    f"PEEQ max {fp.get('peeq_max')}")
            except (FileNotFoundError, StopIteration):
                row(f"SF {sf} 345 MPa own run at {amp}", True, None, 0, "run missing or not converged to the target")
    # ---- other footprints, SF 1
    cb = {(round(x["width_mm"], 3), x["meridian"]): x for x in json.load(open(f"{O}/CORE-BOUNDARIES.json"))}
    for key, (a0, a1), tag in (((332.216, "L"), (1.79559, 1.810809), "L332"), ((401.856, "W"), (1.284271, 1.302271), "W402")):
        b = next(x for x in cb[key]["boundaries"] if x["SF"] == 1.0 and x["strength_basis"] == "minimum_average")
        f0, f1 = frame(f"g-{tag}-a{a0}-hi", P1), frame(f"g-{tag}-a{a1}-hi", P1)
        row(f"{key} SF 1 own pass/fail at the card's pair", True, f0["face_mises_max"] <= 345 < f1["face_mises_max"],
            f"{f0['face_mises_max']:.3f} / {f1['face_mises_max']:.3f} MPa (card {b['passing_face_MPa']:.3f} / {b['failing_face_MPa']:.3f})")
        row(f"{key} SF 1 tolerance estimate, mm", b["amplitude_estimate_mm"], cross(a0, f0["face_mises_max"], a1, f1["face_mises_max"], 345), 0.018)
        row(f"{key} SF 1 passing core shear, MPa", b["passing_core_shear_MPa"], abs(f0["core_tau_meridian"]), 0.003)
    # ---- cure debit (341.59 MPa screen)
    td = {(b["SF"], b["strength_basis"]): b for b in cf["thermal_debit"]["boundaries"]}
    for sf, p, (a0, a1) in ((1.0, P1, (1.117424, 1.135424)), (1.05, P105, (0.65274, 0.67074))):
        b = td[(sf, "minimum_average")]
        f0, f1 = frame(f"g-W332-a{a0}-hi", p), frame(f"g-W332-a{a1}-hi", p)
        y = b["face_yield_MPa"]
        row(f"cure debit SF {sf}: own pass/fail at the card's pair", True, f0["face_mises_max"] <= y < f1["face_mises_max"],
            f"{f0['face_mises_max']:.3f} / {f1['face_mises_max']:.3f} vs {y:.4f} MPa")
        card_est = b["passing_amplitude_mm"] + (y - b["passing_face_MPa"]) / (b["failing_face_MPa"] - b["passing_face_MPa"]) * (
            b["failing_amplitude_mm"] - b["passing_amplitude_mm"])
        row(f"cure debit SF {sf} estimate, mm", card_est, cross(a0, f0["face_mises_max"], a1, f1["face_mises_max"], y), 0.018)
    # ---- endpoint division by 1.10 on the limiting footprint
    cal = json.load(open(f"{O}/CORE-CALIBRATION.json"))["global_bracket"]
    need = 1.1 * P1
    for side, a in (("passing", 0.520967), ("failing", 0.538967)):
        e = res(f"e-W402-a{a}-345").get("endpoint_kPa")
        row(f"1.10 division {side} amplitude {a}: numerical endpoint, kPa", cal[side]["endpoint_kPa"], e, 0.1)
        if e is not None:
            row(f"1.10 division {side}: own endpoint/1.1 {'>=' if side == 'passing' else '<'} service", True,
                (e >= need) if side == "passing" else (e < need), f"needs {need:.4f} kPa")
    # ---- mesh control
    for a in (1.208988, 1.226988):
        f0, f1 = frame(f"g-W332-a{a}-hi", P1), frame(f"m-W332-a{a}-hi", P1)
        row(f"mesh control at {a}: refined minus base max face stress, MPa", None, f1["face_mises_max"] - f0["face_mises_max"], 0,
            "own 2 mm / 3+8+3 layers against own 4 mm / 2+6+2")
        row(f"mesh control at {a}: refined minus base core shear, MPa", None, abs(f1["core_tau_meridian"]) - abs(f0["core_tau_meridian"]), 0)
    # ---- larger dimple 332.2 W 11.8 mm
    sw = next(x for x in cf["sweep"] if abs(x["width_mm"] - 332.2164186283597) < 1e-6 and x["amplitude_mm"] == 11.8)
    fr = sorted(res("s-W332-a11.8-hi")["frames"], key=lambda f: f["pressure_kPa"])
    ci = [(f["pressure_kPa"], f["core_index_min_avg"]) for f in fr]
    fy = [(f["pressure_kPa"], f["face_mises_max"]) for f in fr]
    c_cross = next((cross(p0, i0, p1, i1, 1.0) for (p0, i0), (p1, i1) in zip(ci, ci[1:]) if i0 < 1.0 <= i1), None)
    f_cross = next((cross(p0, s0, p1, s1, 345.0) for (p0, s0), (p1, s1) in zip(fy, fy[1:]) if s0 < 345.0 <= s1), None)
    row("11.8 mm / 332.2 W: first minimum-average core shear, kPa", sw["first_core_shear"]["minimum_average"]["estimate_kPa"], c_cross, 0.5)
    row("11.8 mm / 332.2 W: first face yield (pre-yield branch), kPa", sw["first_face_yield_estimate_kPa"], f_cross, 0.5)
    try:
        row("11.8 mm / 332.2 W: 345 MPa numerical endpoint, kPa", sw["endpoint_kPa"], res("s-W332-a11.8-345").get("endpoint_kPa"), 0.5)
    except FileNotFoundError:
        pass
    # ---- regularisation sensitivity (own runs, if present)
    for nm, lab in (("c-W332-a1.208988-hi-ein0.01", "inherited 0.01/0.005 MPa"), ("c-W332-a1.208988-hi-ein10", "stiffer 10/5 MPa")):
        if os.path.exists(os.path.join(FE, nm, "result.json")):
            f0, f1 = frame("g-W332-a1.208988-hi", P1), frame(nm, P1)
            row(f"core in-plane law {lab} minus regularized 1/0.5: max face stress at 1.208988 mm, MPa", None,
                f1["face_mises_max"] - f0["face_mises_max"], 0, f"core shear {abs(f1['core_tau_meridian']):.5f} vs {abs(f0['core_tau_meridian']):.5f} MPa")
    # ---- face modulus sensitivity: NASA CR-194164 Table 2 longitudinal 298.7 GPa against the card's 290 GPa
    if os.path.exists(os.path.join(FE, "f-W332-a1.226988-hi-E298.7", "result.json")):
        s = {}
        for a in (1.208988, 1.226988):
            f0, f1 = frame(f"g-W332-a{a}-hi", P1), frame(f"f-W332-a{a}-hi-E298.7", P1)
            s[a] = f1["face_mises_max"]
            row(f"face E 298.7 GPa minus 290 GPa: max face stress at {a} mm, MPa", None, f1["face_mises_max"] - f0["face_mises_max"], 0)
        est = cross(1.208988, s[1.208988], 1.226988, s[1.226988], 345.0)
        row("face E 298.7 GPa: SF 1 tolerance estimate, mm (linear, extrapolated past the pair)", None, est, 0,
            f"{est - out['SF1.0']['estimate_mm']:+.4f} mm against own 290 GPa estimate")
        out["E298.7_SF1_estimate_mm"] = est
    with open(os.path.join(HERE, "B-FE.json.tmp"), "w") as fh:
        json.dump({"tag": "QUESTIONABLE/PROJECTION", "rows": ROWS, "governing": out}, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "B-FE.json.tmp"), os.path.join(HERE, "B-FE.json"))
    n = [r for r in ROWS if r["agrees"] is not None]
    print(sum(r["agrees"] for r in n), "of", len(n), "compared rows agree")


if __name__ == "__main__":
    main()
