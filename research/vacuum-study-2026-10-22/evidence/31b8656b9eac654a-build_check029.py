#!/usr/bin/env python3
"""CHECK MAINLINE-029: set the card's numbers against my own runs (own axisymmetric model, check029/axi029.py) and write
RESULTS.json, NFI.json and INPUTS.json in outputs/vacuum-mainline029-check-1020/. Prints the comparison table.

Tolerances for "reproduced" (a row outside its tolerance is a mismatch and is listed in RESULTS.json "mismatches"):
linear eigenpressures 0.02%; lead nonlinear endpoints 0.05%; EUCASS and transfer nonlinear endpoints 0.2%; face stress
maxima 2% (a Gauss-point maximum near the flat top of the path moves with the sampled state)."""
import datetime
import hashlib
import json
import math
from pathlib import Path

ME = Path("unpublished-local-ref:b4008749caf12a44")
O = ME / "work/outputs/vacuum-mainline029-check-1020"
R = O / "runs"
S = ME / "work/scripts/check029"
OWN = Path("unpublished-local-ref:1a1d51aea95bb074"
           "vacuum-mainline029-crimp-gamma-fe-1020")
BRIEFS = Path("unpublished-local-ref:792ada9d1fcd5e54")
P_OP_KPA = 95.46083791390515
TOL = {"linear": 2e-4, "lead-nl": 5e-4, "nl": 2e-3, "stress": 2e-2}


def J(name):
    p = R / name
    return json.loads(p.read_text()) if p.exists() else None


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


rows = []


def cmp(group, row, card, mine, unit, tol, owner_mesh="", my_mesh="", note=""):
    if mine is None:
        rows.append({"group": group, "row": row, "card": card, "mine": None, "unit": unit, "pending": True})
        return
    rel = (mine - card) / card
    rows.append({"group": group, "row": row, "card": card, "mine": mine, "unit": unit, "rel": rel, "tol": TOL[tol],
                 "reproduced": abs(rel) <= TOL[tol], "owner_mesh": owner_mesh, "my_mesh": my_mesh, "note": note})


def main():
    ext = {}
    # ---------- EUCASS linear (owner meshes from MODEL.json: full96/192 2 face x 8 core, full384 3 x 12, dimple full192 2 x 8)
    lin = {(r["case"], r["ntheta"], r["nface"], r["ncore"]): r for r in json.loads((O / "EUCASS-LINEAR.json").read_text())}
    for (case, n, f, c), card, om in ((("flat", 96, 2, 6), 30.23653, "96 x 2f x 8c CAX8"), (("flat", 192, 2, 6), 30.21954, "192 x 2f x 8c"),
                                      (("flat", 384, 3, 10), 30.21717, "384 x 3f x 12c"), (("dimple", 192, 2, 6), 30.19659, "192 x 2f x 8c")):
        r = lin[(case, n, f, c)]
        cmp("EUCASS linear", f"{case} first eigenpressure (dead pressure)", card, r["dead_MPa"][0], "MPa", "linear", om, f"{n} x {f}f x {c}c")
    ext["eucass_linear_follower"] = {f"{k[0]} {k[1]}x{k[2]}fx{k[3]}c": {"dead_MPa": v["dead_MPa"][0], "follower_MPa": v["follower_MPa"][0],
                                     "follower_over_dead": v["follower_MPa"][0] / v["dead_MPa"][0]} for k, v in lin.items()}
    sens = {}
    for s_, f_ in (("E_steel 190 GPa", "sens-flat-Esteel-190000.json"), ("E_steel 200 GPa", "sens-flat-Esteel-200000.json"),
                   ("E_foam 30 MPa", "sens-flat-Efoam-30.json"), ("E_foam 35 MPa", "sens-flat-Efoam-35.json"),
                   ("foam nu 0.3", "sens-flat-nufoam-0.3.json")):
        sens[s_] = J(f_)["dead_MPa"][0]
    for s_, f_ in (("flat, 42.80 mm read as the mid-surface radius (R_outer 44.77)", "radius-eucass-flat-mid.json"),
                   ("dimple, 42.80 mm read as the mid-surface radius (R_outer 44.76)", "radius-eucass-dimple-mid.json"),
                   ("flat, 42.80 mm read at the foam/outer-face interface (R_outer 43.22)", "radius-eucass-flat-face.json"),
                   ("dimple, 42.80 mm read at the foam/outer-face interface (R_outer 43.22)", "radius-eucass-dimple-face.json")):
        sens[s_] = J(f_)["dead_MPa"][0]
    ext["eucass_linear_sensitivity_192x2fx6c_MPa"] = {"paper": {"flat": 27.53, "dimple": 27.56}, "runs": sens,
                                                      "E_steel_closing_flat_GPa_linear_interp": 190 - (sens["E_steel 190 GPa"] - 27.53) /
                                                      ((sens["E_steel 200 GPa"] - sens["E_steel 190 GPa"]) / 10)}
    # ---------- EUCASS nonlinear
    for case, card, lc in (("flat", 28.84878, "lc-eucass-flat-96-2-4-a0.json"), ("dimple", 28.83042, "lc-eucass-dimple-96-2-4-a0.json")):
        cmp("EUCASS perfect nonlinear", f"{case} elastic endpoint (owner-style load control)", card, J(lc)["endpoint_MPa"], "MPa", "nl",
            "96 x 2f x 4c, p_ref 40 MPa", "96 x 2f x 4c, same increments")
    a0 = J("eucass-flat-96-2-4-a0.json")
    ext["eucass_perfect_flat_arc_peak_MPa"] = a0["p_peak_MPa"]
    ext["eucass_perfect_flat_stability_scan"] = J("stab-eucass-flat-96-2-4-a0.json")["rows"]
    for case, card, arc, lc, dc in (("flat", 13.956916, "eucass-flat-96-2-4.json", "lc-eucass-flat-96-2-4.json", "stretch-eucass-flat-96-2-4.json"),
                                    ("dimple", 13.843652, "eucass-dimple-96-2-4.json", "lc-eucass-dimple-96-2-4.json",
                                     "stretch-eucass-dimple-96-2-4.json")):
        cmp("EUCASS imperfect nonlinear", f"{case} mu 0.75: first critical point (arc-length)", card, J(arc)["p_peak_MPa"], "MPa", "nl",
            "96 x 2f x 4c load control", "96 x 2f x 4c arc-length")
        cmp("EUCASS imperfect nonlinear", f"{case} mu 0.75: owner-style load-control endpoint", card, J(lc)["endpoint_MPa"], "MPa", "nl",
            "96 x 2f x 4c load control", "96 x 2f x 4c load control")
        cmp("EUCASS imperfect nonlinear", f"{case} mu 0.75: pole displacement-control maximum", card, J(dc)["peak_MPa"], "MPa", "nl",
            "96 x 2f x 4c load control", "96 x 2f x 4c displacement control")
    series = {}
    for f_ in ("eucass-flat-96-1-4.json", "eucass-flat-96-2-4.json", "eucass-flat-96.json", "eucass-flat-96-2-8.json", "eucass-flat-96-2-10.json",
               "eucass-flat-96-2-12.json", "eucass-flat-96-3-8.json", "eucass-flat-arc192-a2.955.json", "eucass-flat-384.json",
               "eucass-dimple-96-1-4.json", "eucass-dimple-96-2-4.json", "eucass-dimple-96-2-6.json", "eucass-dimple-96-2-8.json",
               "eucass-dimple-96-2-10.json", "eucass-dimple-192.json"):
        d = J(f_); a = d["args"]
        series[f"{d['case']} {a['nth']} x {a.get('nface', '2')}f x {a.get('ncore', '6')}c"] = {
            "first_critical_MPa": d["p_peak_MPa"], "outer_face_vm_MPa": d["outer_face_max_vonmises_MPa"], "dof": d["dof"]}
    ext["eucass_imperfect_mesh_series"] = series
    E_foam = 40.0
    ext["stvk_foam_uniaxial_limit"] = {"max_compressive_cauchy_MPa": E_foam / (3 * math.sqrt(3)), "at_stretch": 1 / math.sqrt(3),
                                       "formula": "sigma = E lambda (lambda^2 - 1)/2 for nu 0; extremum at lambda = 1/sqrt(3)"}
    coll = {}
    for f_ in ("stretch-eucass-flat-96-2-4.json", "stretch-eucass-flat-96-2-12.json", "stretch-eucass-dimple-96-2-4.json"):
        d = J(f_); P = d["path"]
        k = max(range(len(P)), key=lambda i: P[i]["p_MPa"])
        # the state at the arc-length-like first maximum: first point where the path stops rising by more than 0.01%
        coll[f_[8:-5]] = {"path_max_MPa": d["peak_MPa"], "at_max": P[k],
                          "at_13.0_MPa": next((r for r in P if r["p_MPa"] >= 13.0), None),
                          "min_core_stretch_on_path": min(r["core_min_stretch"] for r in P),
                          "p_at_min_core_stretch_MPa": min(P, key=lambda r: r["core_min_stretch"])["p_MPa"]}
    ext["eucass_core_collapse"] = coll
    st = {}
    for f_ in ("stress-eucass-flat-a2.955.json", "stress-eucass-flat-a0.json"):
        d = J(f_)
        st[f_[7:-5]] = {k: d[k] for k in ("at_5.63", "at_6.03", "at_12.45")}
    pf = J("stress-eucass-flat-a0.json")["path"]; pi_ = J("stress-eucass-flat-a2.955.json")["path"]

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    def tau_crit(Ein, G, En):
        lo, hi = 1e-6, 100.0
        for _ in range(80):
            mid = (lo * hi) ** 0.5
            lo, hi = (lo, mid) if det_min(Ein, G, En, mid) < 0 else (mid, hi)
        return hi
    ext["core_ellipticity_threshold_tau_MPa"] = {
        f"{lab} E_in {ein}": tau_crit(ein, G, 103.42135939752539) for lab, G in (("W", 46.88434959354485), ("L", 103.4213593975254))
        for ein in (0.01, 1.0)}
    for k, v in cs.items():
        d = J(f"core-{k}.json")
        P = d["path"]
        v["p_kPa_at_tau"] = {}
        for lab, thr in ext["core_ellipticity_threshold_tau_MPa"].items():
            prev = {"p_kPa": 0.0, "core_max_abs_tau_MPa": 0.0}
            hit = None
            for r_ in P:
                if r_["core_max_abs_tau_MPa"] >= thr > prev["core_max_abs_tau_MPa"]:
                    f_ = (thr - prev["core_max_abs_tau_MPa"]) / (r_["core_max_abs_tau_MPa"] - prev["core_max_abs_tau_MPa"])
                    hit = prev["p_kPa"] + f_ * (r_["p_kPa"] - prev["p_kPa"])
                    break
                prev = r_
            v["p_kPa_at_tau"][f"ellipticity threshold, {lab} ({thr:.3f} MPa)"] = hit
    ext["core_ellipticity_formula"] = ("acoustic tensor of C = diag(E_in, E_n, G) in (t, n) with initial shear tau: "
                                       "det = E_in G + 2 tau x (E_in + G) + x^2 (E_in E_n + 4 tau^2) + 2 tau x^3 (G + E_n) + G E_n x^4, "
                                       "x = k_n/k_t; ellipticity is lost when det < 0 for some x")
    # ---------- face stress diagnostic (card: outer-face max von Mises at the load-control endpoint)
    for k, card in (("nl-lead021-W-a11.8", 660.806), ("nl-lead021-L-a11.8", 835.808), ("nl-lead021b-W-a46", 1144.503),
                    ("nl-lead021b-L-a46", 1303.532)):
        d = J(k + ".json")
        cmp("face stress", f"{k}: outer-face max von Mises at the load-control endpoint", card, d["load_control"]["outer_face_vm_MPa"], "MPa",
            "stress", "graded 512 x 1f x 4c", "same", f"at my displacement-control maximum: {d['disp_control']['outer_face_vm_at_max_MPa']:.1f}")
    yields = {}
    for c, d_ in (("lead021", "W"), ("lead021", "L"), ("lead021b", "W"), ("lead021b", "L")):
        y = J(f"yield-{c}-{d_}.json"); P = y["path"]

        def first(thr):
            for a, b in zip([{"p_kPa": 0.0, "outer_face_vm_MPa": 0.0, "where": None}] + P, P):
                if a["outer_face_vm_MPa"] < thr <= b["outer_face_vm_MPa"]:
                    f = (thr - a["outer_face_vm_MPa"]) / (b["outer_face_vm_MPa"] - a["outer_face_vm_MPa"])
                    return a["p_kPa"] + f * (b["p_kPa"] - a["p_kPa"]), b["where"]
            return None, None
        yields[f"{c}/{d_}"] = {}
        for thr, lab in ((241.0, "S200F spec-minimum yield 241 MPa (Materion, the card's cited datasheet)"),
                         (345.0, "345 MPa, the line's SR-200 proxy (021b is sized to it)"), (379.2, "379.2 MPa, one historical lot")):
            p_, w_ = first(thr)
            yields[f"{c}/{d_}"][lab] = {"p_kPa": p_, "over_operating": p_ / P_OP_KPA if p_ else None,
                                        "element_and_r_mm": w_}
        yields[f"{c}/{d_}"]["limit_kPa"] = y["limit_kPa"]
    ext["first_face_yield_on_the_path"] = yields
    # ---------- transfer40 (owner axis meshes from MODEL.json)
    tr = J("transfer40.json")
    for n, card, f_ in ((24, 7.472405, "transfer40-eigen24.json"), (48, 6.626231, "transfer40-eigen48.json"),
                        (96, 6.417224, "transfer40-eigen96.json"), (192, 6.378169, "transfer40-eigen192.json")):
        cmp("transfer40", f"axis eigen{n}", card, J(f_)["eigen_dead_MPa"][0], "MPa", "linear", f"{n} x 1f x 2c", f"{n} x 1f x 2c")
    cmp("transfer40", "axis eigen384", 6.372661, tr["eigen384_dead_MPa"][0], "MPa", "linear", "384 x 2f x 4c", "384 x 2f x 4c")
    for n, card, d in ((24, 2.853333, J("transfer40-static24.json")), (48, 2.296584, J("transfer40-static48.json")),
                       (192, 2.218066, J("transfer40-static192.json"))):
        cmp("transfer40", f"axis static{n} endpoint vs my limit point", card, d["disp_control_lambda_max_MPa"], "MPa", "nl", "", "")
        cmp("transfer40", f"axis static{n} endpoint vs my load control", card, d["load_control_endpoint_MPa"], "MPa", "nl", "", "")
    cmp("transfer40", "axis static384 endpoint vs my limit point", 2.216077, tr["static384"]["disp_control_lambda_max_MPa"], "MPa", "nl")
    cmp("transfer40", "axis static384 endpoint vs my load control", 2.216077, tr["static384"]["load_control_endpoint_MPa"], "MPa", "nl")
    cmp("transfer40", "axis static48 graded endpoint vs my limit point", 2.254362, tr["static48graded"]["disp_control_lambda_max_MPa"],
        "MPa", "nl")
    cmp("transfer40", "axis static48 graded endpoint vs my load control", 2.254362, tr["static48graded"]["load_control_endpoint_MPa"],
        "MPa", "nl")
    # ---------- arithmetic in the text and records (own arithmetic from the card's printed values)
    arith = []

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
