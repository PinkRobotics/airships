#!/usr/bin/env python3
"""MAINLINE-055: assemble RESULTS.json, NFI.json and INPUTS.json from scale055.json and the FE runs (cap055.py), with the
cost table and the outcome table. All values QUESTIONABLE or PROJECTION as tagged."""
import datetime
import glob
import hashlib
import json
from pathlib import Path

ME = Path("unpublished-local-ref:b4008749caf12a44")
O = ME / "work/outputs/vacuum-mainline055-gamma-test-1020"
S = ME / "work/scripts/gamma055"
P_OP = 95.4608379139


def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {"path": str(p), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}


def fe(label):
    d = json.loads((O / "runs" / f"{label}.json").read_text())
    c = d["crossings_kPa"]
    return {"label": label, "limit_kPa": d["limit_kPa"], "p_H_kPa": d["p_H_kPa"], "Vc": d["Vc"],
            "gamma_H_elastic": d["gamma_H_elastic_limit"], "face_yield_outer_kPa": c.get("face yield (outer)"),
            "face_yield_inner_kPa": c.get("face yield (inner)"), "core_W_shear_typ_kPa": c.get("W shear typ"),
            "core_W_shear_min_kPa": c.get("W shear min"), "core_crush_typ_kPa": c.get("crush typ"), "args": d["args"]}


def main():
    sc = json.loads((O / "scale055.json").read_text())
    runs = {Path(f).stem: fe(Path(f).stem) for f in sorted(glob.glob(str(O / "runs" / "*.json")))}
    s1, s4 = runs["S1-be-sphere-d16"], runs["S4-al-sphere-d16"]
    s2, s5 = runs["S2-be-sphere-d9"], runs["S5-al-sphere-d9"]
    stand_in_check = {
        "dimple 16.057 mm": {"Be": s1, "5052-O": s4, "gamma_ratio": s4["gamma_H_elastic"] / s1["gamma_H_elastic"],
                             "limit_ratio": s4["limit_kPa"] / s1["limit_kPa"],
                             "core_shear_onset_ratio": s4["core_W_shear_typ_kPa"] / s1["core_W_shear_typ_kPa"],
                             "face_yield_onset_ratio": s4["face_yield_outer_kPa"] / s1["face_yield_outer_kPa"]},
        "dimple 9.318 mm": {"Be": s2, "5052-O": s5, "gamma_ratio": s5["gamma_H_elastic"] / s2["gamma_H_elastic"],
                            "limit_ratio": s5["limit_kPa"] / s2["limit_kPa"],
                            "core_shear_onset_ratio": s5["core_W_shear_typ_kPa"] / s2["core_W_shear_typ_kPa"],
                            "face_yield_onset_ratio": s5["face_yield_outer_kPa"] / s2["face_yield_outer_kPa"]}}
    cap_check = []
    for lab, ref in (("C1-be-cap1500-d16", s1), ("C2-be-cap2000-d16", s1), ("C3-be-cap2500-d16", s1), ("C4-be-cap3000-d16", s1),
                     ("C8-al-cap1500-d16", s4), ("C5-al-cap2000-d16", s4), ("C6-al-cap2500-d16", s4), ("C7-al-cap3000-d16", s4),
                     ("R30c-be-cap2500", runs["R30a-be-sphere"]), ("R30b-be-cap3000", runs["R30a-be-sphere"])):
        r = runs[lab]
        cap_check.append({"label": lab, "base_radius_mm": float(r["args"]["a"]), "limit_kPa": r["limit_kPa"],
                          "limit_vs_sphere": r["limit_kPa"] / ref["limit_kPa"],
                          "core_shear_onset_vs_sphere": r["core_W_shear_typ_kPa"] / ref["core_W_shear_typ_kPa"],
                          "outer_face_yield_vs_sphere": r["face_yield_outer_kPa"] / ref["face_yield_outer_kPa"]})
    series = []
    for lab in ("D1-be-sphere-d1", "D2-be-sphere-d2", "D4-be-sphere-d4", "D6-be-sphere-d6", "S2-be-sphere-d9", "S1-be-sphere-d16"):
        r = runs[lab]
        amp = float(r["args"]["amp"])
        series.append({"dimple_mm": amp, "dimple_over_t_eq": amp / sc["designs"]["R10 lead (028b)"]["groups"]["t_eq_mm"],
                       "elastic_limit_kPa": r["limit_kPa"], "gamma_H_elastic": r["gamma_H_elastic"],
                       "outer_face_345MPa_at_kPa": r["face_yield_outer_kPa"], "core_W_typ_shear_at_kPa": r["core_W_shear_typ_kPa"],
                       "core_W_min_shear_at_kPa": r["core_W_shear_min_kPa"], "core_crush_at_kPa": r["core_crush_typ_kPa"]})

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
