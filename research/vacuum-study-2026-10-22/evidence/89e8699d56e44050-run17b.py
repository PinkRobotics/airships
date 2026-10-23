#!/usr/bin/env python3
"""MAINLINE-017b driver: pins, reproduction checks, today's baselines, each property alone, translations,
cheapest combinations and the SiC strength sensitivity. Writes COMPUTE.json (trends are added by trend17b.py)."""
import datetime
import hashlib
import json
import math
import os
import time

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import numpy as np  # noqa: E402

import combo17b as cb  # noqa: E402
import model17b as m  # noqa: E402
import scan17b as sc  # noqa: E402
import val17b  # noqa: E402

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def pin(path):
    b = open(path, "rb").read()
    return {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def tolerance(R, h, kd):
    """MAINLINE-015's map (as re-implemented in 021): single-dimple amplitude and worst-width RMS for a knockdown."""
    t_eq = math.sqrt(3.0) * h
    root = (12.0 * (1.0 - 0.3 ** 2)) ** 0.25 * math.sqrt(R / t_eq)
    ratio = (kd - 0.45) / 0.51
    out = {"gamma": kd, "t_eq_mm": t_eq * 1e3, "R_over_t_eq": R / t_eq, "in_fit_range": 100.0 <= R / t_eq <= 1550.0}
    if ratio <= 0.0 or ratio >= 1.0:
        out.update({"amplitude_mm": None, "rms_worst_mm": None, "status": "outside Eq 3 (floor 0.45)"})
        return out
    dbar = -math.log(ratio) / 3.88
    out.update({"amplitude_mm": dbar * t_eq * 1e3, "rms_worst_mm": dbar * t_eq * (2.625 / root) / math.sqrt(8.0) * 1e3,
                "status": "inverted"})
    return out


def flatness(q, tc, kdelta):
    """CR-1457 eq 2.2-13: waviness amplitude delta = K_delta tc Fc / Ec, in mm."""
    return kdelta * tc * q["Fc_flatwise"] / q["Ec"] * 1e3


def strip(row):
    return {k: v for k, v in row.items() if not isinstance(v, np.ndarray)}


def main():
    t0 = time.monotonic()
    started = datetime.datetime.now().astimezone().isoformat()
    out = {"started": started, "pins": {}}
    for k, p in PIN_FILES.items():
        rec = pin(p)
        if k in KNOWN:
            rec["matches_upstream_pin"] = rec["sha256"] == KNOWN[k]
        out["pins"][k] = rec
    out["checks"] = val17b.checks(verbose=False)
    assert all(c["ok"] for c in out["checks"]), "reproduction checks failed"

    # ---------------------------------------------------------------- P2
    P2_LEVERS_M = ["face_strength", "face_modulus", "face_density", "core_shear_modulus", "core_density",
                   "core_tt_modulus", "face_flatness", "core_crush", "cell_size", "sheet_size", "film_mass", "seam_mass"]
    sets = {"all": P2_LEVERS_M + ["gamma"], "material_only": P2_LEVERS_M}
    sets["be_kept"] = [x for x in sets["all"] if x not in ("face_modulus", "face_density")]
    sets["be_kept_material_only"] = [x for x in P2_LEVERS_M if x not in ("face_modulus", "face_density")]
    p2 = {}
    for R in (10.0, 20.0):
        key = f"R{int(R)}"
        base = sc.p2_best(R, {}, "handbook")
        q0 = m.p2_apply(m.P2_TODAY, {})
        rec = {"R_m": R, "lift_kg": m.lift(R), "reserve_019_kg": m.reserve_019(R), "today": base,
               "today_nu_0p33": m.p2_optimise(R, dict(q0, nu=0.33), "019")["least"],
               "today_flatness_mm": flatness(q0, base["tc"], m.KDELTA_TODAY),
               "alone": {}, "alone_conservative_gamma": {}, "combos": {}}
        for rule, slot in (("handbook", "alone"), ("conservative", "alone_conservative_gamma")):
            res = sc.p2_scan(R, rule)
            for prop, r in res.items():
                r2 = {k: v for k, v in r.items() if k not in ("at_factor", "at_f_max")}
                if r.get("at_factor"):
                    r2["at"] = r["at_factor"]
                if r.get("at_f_max"):
                    r2["at_f_max"] = r["at_f_max"]
                rec[slot][prop] = r2
        # translations at the gamma-alone point
        g = rec["alone"]["gamma"]
        if g.get("factor"):
            pt = g["at"]
            rec["gamma_translation"] = {
                "needed_gamma": min(1.0, 0.2 * g["factor"]),
                "map_015_at_gamma_alone_point": tolerance(R, pt["tc"] + pt["tf"], min(1.0, 0.2 * g["factor"])),
                "core_shear_modulus_alone": rec["alone"]["core_shear_modulus"],
            }
        # combinations, both branches
        for name, levers in sets.items():
            for branch in ("stiff", "crimp"):
                x0 = np.concatenate([np.zeros(len(levers)), [math.log(base["F"])]])
                best = cb.p2_combo(R, levers, {"gamma": 5.0}, branch, starts=[x0], seed=7)
                if best:
                    v = cb.p2_verify(R, best["factors"], best["F"])
                    best["verify"] = {k: v[k] for k in ("least", "governing", "Vc", "tf", "tc", "F") if k in v}
                    # the point itself, at the found factors, with every mode
                    q = m.p2_apply(m.P2_TODAY, best["factors"])
                    gg = m.p2_geometry(R, np.array([best["F"]]), q, "019")
                    if branch == "stiff":
                        q["gamma_rule"] = "conservative"
                    ev, aux = m.p2_modes(R, gg["tf"], gg["tc"], q, gamma_override=(1.0 if branch == "crimp" else None))
                    best["point"] = {"tf": float(gg["tf"][0]), "tc": float(gg["tc"][0]), "J": float(gg["J"][0]),
                                     "Vc": float(aux["Vc"][0]), "gamma": float(aux["gamma"][0]),
                                     "modes": {k: float(ev[k][0]) for k in m.P2_MODES},
                                     "Q_eff": q["Q"], "Ec": q["Ec"],
                                     "flatness_mm": flatness(q, float(gg["tc"][0]),
                                                             m.KDELTA_TODAY / best["factors"].get("face_flatness", 1.0))}
                rec["combos"][f"{name}|{branch}"] = best
        p2[key] = rec
    out["p2"] = p2

    # ---------------------------------------------------------------- P3
    M3 = ["sic_strength", "sic_modulus", "sic_density", "film_specific_strength", "joint_mass", "node_mass",
          "straightness"]
    sets3 = {"all": M3 + ["lattice_knockdown", "local_knockdown"], "material_only": M3}
    sets3["sic_kept"] = [x for x in sets3["all"] if x not in ("sic_modulus", "sic_density")]
    sets3["sic_kept_material_only"] = [x for x in M3 if x not in ("sic_modulus", "sic_density")]
    p3 = {}
    for row in ("today", "projection"):
        base = sc.p3_best(row, {})
        rec = {"row": row, "film": sc.P3_ROWS[row][0], "joint": sc.P3_ROWS[row][1], "today": base, "alone": {},
               "combos": {}, "strength_sensitivity": {}}
        res = sc.p3_scan(row)
        for prop, r in res.items():
            r2 = {k: v for k, v in r.items() if k not in ("at_factor", "at_f_max")}
            if r.get("at_factor"):
                r2["at"] = r["at_factor"]
            if r.get("at_f_max"):
                r2["at_f_max"] = r["at_f_max"]
            rec["alone"][prop] = r2
        for sig in (3900e6, 1000e6, 580e6, 380e6):
            b = sc.p3_best(row, {"sic_strength": sig / 3900e6})
            rec["strength_sensitivity"][f"{sig/1e6:.0f}MPa"] = b
        lo, hi = 1e-3, 1.0
        target = base["least"] * 0.999
        for _ in range(40):
            mid = math.sqrt(lo * hi)
            if sc.p3_best(row, {"sic_strength": mid})["least"] >= target:
                hi = mid
            else:
                lo = mid
        rec["strength_the_design_uses_MPa"] = hi * 3900.0
        if base["least"] < 1.0:
            for name, levers in sets3.items():
                x0 = np.concatenate([np.zeros(len(levers)), [base["s"], math.log(base["tfilm"]), base["ro"]]])
                best = cb.p3_combo(row, levers, {"lattice_knockdown": 5.0}, starts=[x0], seed=13)
                if best:
                    v = cb.p3_verify(row, best["factors"])
                    best["verify"] = {k: v[k] for k in ("least", "governing", "s", "ro", "tfilm")}
                rec["combos"][name] = best
        p3[row] = rec
    out["p3"] = p3
    out["ended"] = datetime.datetime.now().astimezone().isoformat()
    out["elapsed_s"] = time.monotonic() - t0
    tmp = os.path.join(HERE, "COMPUTE.json.tmp")
    with open(tmp, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    os.replace(tmp, os.path.join(HERE, "COMPUTE.json"))
    print("elapsed", round(out["elapsed_s"], 1), "s")


if __name__ == "__main__":
    main()
