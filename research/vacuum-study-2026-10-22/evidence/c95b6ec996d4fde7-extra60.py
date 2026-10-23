#!/usr/bin/env python3
"""MAINLINE-060 part two: this seat's own arithmetic on CARBON.json, 051's pinned tables and the 060 sources.

- Joints. The sourced fitting shares of a whole aerospace strut are used as a sensitivity on the carbon tubes. They are
  the Boeing 44K strut's titanium insert and ball, and the space-strut "typical" share. The fittings then weigh share /
  (1 - share) times the tube.
- Reliability. The frame's Pf with carbon's own scatter at each sizing, with and without coupon-to-member size scaling.
  It uses 051's H = 0.0010005 (k(m) sigma_peak / scale)^m, as in carbon60.
- To float. The compression the light pitch frame must carry, and how far 50/20/20/10 sits from 051's 2.16 GPa.
- Hail. 051's design strike is 50.8 mm ice at 32.004 m/s. Its energy is taken over the sourced natural-hail density
  range. It is compared with the sourced ice thresholds on flat carbon/epoxy panels (first delamination, by thickness).
  051's quasi-static surface stresses at three walls are fitted as a power of the wall, carried to the strength-sized
  walls (PROJECTION) and set against the laminate's sourced mean screen less the operating stress.

Writes EXTRA.json."""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import src60 as S  # noqa: E402
from carbon60 import art, R051, L_MEMBER, COUPON_M3  # noqa: E402



def power_fit(pts):
    """Least-squares y = A x^b through (x, y) in log-log."""
    lx = [math.log(x) for x, _ in pts]
    ly = [math.log(y) for _, y in pts]
    n = len(pts)
    mx, my = sum(lx) / n, sum(ly) / n
    b = sum((a - mx) * (c - my) for a, c in zip(lx, ly)) / sum((a - mx) ** 2 for a in lx)
    return math.exp(my - b * mx), b


def line_fit(pts):
    n = len(pts)
    mx, my = sum(x for x, _ in pts) / n, sum(y for _, y in pts) / n
    b = sum((x - mx) * (y - my) for x, y in pts) / sum((x - mx) ** 2 for x, _ in pts)
    return my - b * mx, b


def main():
    C = json.load(open(os.path.join(HERE, "CARBON.json")))
    cons = {c["id"]: c for c in C["constructions"]}
    acct = C["account"]
    gaps = json.load(open(art(R051, "GAPS.json")))["rows"]
    wit = {(r["material"], r["reserve"]): r["comparison_geometry"] for r in json.load(open(art(R051, "WITNESSES.json")))["rows"]}

    # ---- joints: sourced fitting shares as a sensitivity on the tube bill
    b44 = (S.val("b44_ins", "joints", "fitting_mass", "titanium insert mass per strut (44K strut)", 1.2)
           + S.val("b44_ball", "joints", "fitting_mass", "titanium ball end fitting mass per strut (44K strut)", 1.5))
    b44_tot = S.val("b44_tot", "joints", "fitting_mass", "total strut assembly mass incl. body", 16.01)
    cordis = S.val("cordis", "joints", "fitting_mass", "fitting share of total strut mass", 70.0) / 100
    knock = S.val("bond70", "joints", "joint_strength", "bonded-fitting strut failure load in compression", 70.0) / 100
    ng2 = S.val("ng2", "joints", "strut_capacity", "compressive failure load of corrugated-fitting strut (NG-2)", -121.7)
    shares = {"Boeing_44K": b44 / b44_tot, "space_strut_typical": cordis}
    per_tube = {k: s / (1 - s) for k, s in shares.items()}
    joints = []
    for x in acct:
        if x["axes"] != "all_endpoints":
            continue
        for k, r in per_tube.items():
            fit = r * x["tubes_kg"]
            joints.append({"construction": x["construction"], "R_m": x["R_m"], "weather": x["weather"], "sizing": x["sizing"], "share": k,
                           "fittings_kg": fit, "replaces_sleeves_kg": x["sleeves_kg"],
                           "payload_kg": x["payload_kg"] - (fit - x["sleeves_kg"]),
                           "payload_seven_day_kg": x["payload_seven_day_kg"] - (fit - x["sleeves_kg"])})
    k13 = cons["K13D2U-50-20-20-10"]
    g = wit[("K13D2U-50-20-20-10", "019")]
    area = g["area_m2"]
    tube_load_kN = g["q1_peak_compression_Pa"] * area / 1e3

    # ---- reliability with carbon's own scatter at each sizing
    rel = []
    for cid, c in cons.items():
        gw = wit[(cid, "019")]
        for lab in ("cv5.2", "cv6"):
            m, k = c[f"m_{lab}"], c[f"k_{lab}"]
            scale = c["laminate_screen_GPa"] / math.gamma(1 + 1 / m)
            for sizing, f in (("witness", 1.0), ("mean", c["f_mean"]), ("Pf1e-3", c[f"f_rel_{lab}"]), ("Pf1e-3_size", c[f"f_rel_size_{lab}"])):
                vol = gw["area_m2"] * f * L_MEMBER
                size = (COUPON_M3 / vol) ** (1 / m)
                out = {"construction": cid, "cv": lab, "m": m, "k": k, "sizing": sizing, "wall_factor": f, "size_factor": size}
                for tag, sc in (("coupon_scale_as_member", scale), ("size_scaled", scale * size)):
                    H = 0.0010005 * (k * c["witness_peak_GPa"] / f / sc) ** m
                    out[f"Pf_{tag}"] = -math.expm1(-H) if H < 700 else 1.0
                rel.append(out)

    # ---- what the light pitch frame must carry to float, and the distance to 051's 2.16 GPa
    need = []
    for x in C["k13_compression_to_float"]:
        fmax = x["max_wall_factor"]
        row = dict(x)
        if fmax > 0:
            for lab in ("cv5.2", "cv6"):
                m, k = k13[f"m_{lab}"], k13[f"k_{lab}"]
                vol = area * fmax * L_MEMBER
                size = (COUPON_M3 / vol) ** (1 / m)
                lam_scale = k13["witness_peak_GPa"] / fmax * k          # whole-member laminate scale needed (GPa)
                row[f"laminate_mean_needed_GPa"] = k13["witness_peak_GPa"] / fmax
                row[f"member_scale_needed_{lab}_GPa"] = lam_scale
                row[f"Xc_needed_Pf1e3_{lab}_MPa"] = lam_scale * math.gamma(1 + 1 / m) * k13["psi_0deg"] * 1000
                row[f"Xc_needed_Pf1e3_{lab}_size_MPa"] = row[f"Xc_needed_Pf1e3_{lab}_MPa"] / size
        need.append(row)
    sc051 = 2.161413                                                  # 051 CARD: whole-member scale at m10, 5% reserve
    gap216 = {"scale_051_GPa": sc051, "laminate_mean_GPa": k13["laminate_screen_GPa"],
              "laminate_scale_m10_GPa": k13["laminate_screen_GPa"] / math.gamma(1.1),
              "laminate_scale_m20_GPa": k13["laminate_screen_GPa"] / math.gamma(1.05),
              "Xc_UD_MPa": k13["Xc_MPa"], "psi": k13["psi_0deg"]}
    gap216["times_mean"] = sc051 / gap216["laminate_mean_GPa"]
    gap216["times_scale_m10"] = sc051 / gap216["laminate_scale_m10_GPa"]
    gap216["Xc_UD_needed_m10_MPa"] = sc051 * math.gamma(1.1) * k13["psi_0deg"] * 1000
    best_pitch = max(S.val("xc_k13312", "compression", "ud_compression", "0 deg UD composite compressive strength", 540.0, "K13312"),
                     S.val("xc_k1352u", "compression", "ud_compression", "0 deg UD composite compressive strength", 450.0, "K1352U"))
    gap216["best_sourced_pitch_Xc_MPa"] = best_pitch
    gap216["compression_over_tension"] = {
        "PAN_230GPa": S.val("ct_pan", "compression", "compression_tension_ratio", "Compressive strength / tensile strength ratio", 0.5, "PAN-CF 230"),
        "pitch_XN15_155GPa": S.val("ct_xn15", "compression", "compression_tension_ratio", "Compressive strength / tensile strength ratio", 0.79, "XN-15")}
    gap216["K63712_measured_MPa"] = S.val("k637_meas", "compression", "ud_compression", "compressive failure stress, measured", 374.0, "K63712")
    gap216["K63712_maker_MPa"] = S.val("k637_maker", "compression", "ud_compression", "manufacturer value quoted", 440.0, "K63712")

    # ---- hail
    v = S.val("v51", "impact", "hail_properties", "Terminal velocity of 2 inch (5.1 cm) ice sphere", 32.0)
    S.note("rho_range", "impact", "hail_properties", "Natural hail ice density range")
    d, v051 = 0.0508, 32.004                                         # 051 CARD's design strike
    vol = math.pi / 6 * d ** 3
    energy = {f"rho_{r}": 0.5 * r * vol * v051 ** 2 for r in (810, 910, 920)}
    fte = {t: S.val(f"fte_{t}", "impact", "hail_threshold", "50.8 mm ice sphere", e, f"{t} mm" if t != 1.59 else "1.59 mm")
           for t, e in ((1.59, 254), (3.11, 453), (4.66, 666))}
    fte38 = S.val("fte38_159", "impact", "hail_threshold", "38.1 mm ice sphere", 196, "1.59 mm")
    ps = S.val("ps_50_4", "impact", "hail_threshold", "onset of full delamination, ice sphere 50 mm, plate 4 mm", 667)
    S.note("fte_linear", "impact", "hail_threshold", "FTE depends linearly")
    a_t, b_t = line_fit(sorted(fte.items()))
    hard = {"tube_puncture_J": S.val("tube20", "impact", "tube_impact", "punctured", 20),
            "bvid_IM7_32ply_J": S.val("bvid108", "impact", "impact_threshold", "barely visible impact damage", 10.8),
            "bvid_4mm_J": S.val("bvid20", "impact", "impact_threshold", "BVID impact energy for 16-ply", 20),
            "cai_damaged_MPa": S.val("cai202", "impact", "cai_retention", "CAI strength, damaged vs undamaged", 202),
            "radial_retention_T800_pct": S.val("xiao881", "impact", "tube_impact", "carbon T800 tube", 88.1)}
    cai_undamaged = 385.0                                            # the same Barile row prints "-385 +- 20 MPa" (asserted below)
    assert "385" in S.USED["cai202"]["printed"]
    hard["cai_retention"] = hard["cai_damaged_MPa"] / cai_undamaged
    import csv
    hd = list(csv.DictReader(open(art(R051, "HAIL-DESIGN.csv"))))
    hail = []
    for cid in ("K13D2U-50-20-20-10", "K13D2U-70-10-10-10", "M55J-50-20-20-10", "M55J-70-10-10-10", "T700S-70-10-10-10"):
        c = cons[cid]
        pts = [(float(r["wall_mm"]), float(r["stress_Shi_MPa"])) for r in hd if r["material"] == cid]
        A, b = power_fit(pts)
        w0 = c["witness_wall_mm"]
        for sizing, f in (("witness", 1.0), ("mean", c["f_mean"]), ("Pf1e-3_cv6", c["f_rel_cv6"]), ("Pf1e-3_cv6_size", c["f_rel_size_cv6"])):
            w = w0 * f
            s_h = A * w ** b
            s_op = c["witness_peak_GPa"] * 1000 / f
            left = c["laminate_screen_GPa"] * 1000 - s_op
            ft = a_t + b_t * w
            left = 0.0 if abs(left) < 1e-9 * c["laminate_screen_GPa"] * 1000 else left
            hail.append({"construction": cid, "sizing": sizing, "wall_mm": w, "hail_surface_stress_MPa": s_h,
                         "fit_A": A, "fit_b": b, "fit_points": pts, "operating_peak_MPa": s_op,
                         "laminate_mean_screen_MPa": c["laminate_screen_GPa"] * 1000, "screen_left_after_operating_MPa": left,
                         "hail_over_left": None if left <= 0 else s_h / left,
                         "ice_FTE_flat_panel_J": ft, "energy_margin_rho910": ft / energy["rho_910"]})
    vel_fte159 = math.sqrt(2 * fte[1.59] / (910 * vol))

    out = {"basis": __doc__, "joints": {"shares": shares, "fittings_per_tube": per_tube, "bonded_fitting_knockdown": knock,
                                        "peak_tube_load_kN": tube_load_kN, "ng2_klb": ng2,
                                        "peak_tube_load_klb": tube_load_kN * 1e3 / 4448.22, "rows": joints},
           "reliability": rel, "to_float": need, "gap_to_2p16": gap216,
           "hail": {"design": {"d_m": d, "v_ms": v051, "v_sourced_ms": v, "energy_J": energy},
                    "flat_panel_FTE_508mm": {str(k): x for k, x in fte.items()}, "fte_381_159": fte38, "pernas_4mm_50mm": ps,
                    "fte_line": {"a_J": a_t, "b_J_per_mm": b_t}, "velocity_for_FTE_159_ms": vel_fte159,
                    "hard_impactor": hard, "rows": hail},
           "sources_used": S.USED}
    with open(os.path.join(HERE, "EXTRA.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1)
    os.replace(os.path.join(HERE, "EXTRA.json.tmp"), os.path.join(HERE, "EXTRA.json"))

    print("fitting shares", {k: round(s, 4) for k, s in shares.items()}, "per tube", {k: round(s, 4) for k, s in per_tube.items()},
          "peak tube load kN", round(tube_load_kN, 1), "klb", round(tube_load_kN * 1e3 / 4448.22, 1))
    for x in joints:
        if x["weather"] == "ISA" and x["construction"] in ("K13D2U-50-20-20-10", "M55J-70-10-10-10") and x["sizing"] in ("witness", "Pf1e-3_cv6"):
            print("  joints", x["construction"], x["R_m"], x["sizing"], x["share"], round(x["fittings_kg"]), round(x["payload_kg"]))
    for x in rel:
        if x["cv"] == "cv6":
            print(f"  Pf {x['construction']:20s} {x['sizing']:12s} f {x['wall_factor']:.2f} size {x['size_factor']:.3f} "
                  f"Pf {x['Pf_coupon_scale_as_member']:.3g} sized {x['Pf_size_scaled']:.3g}")
    for x in need:
        if x["weather"] == "ISA" and x["service"] in ("ground", "seven_day"):
            print("  float", x["R_m"], x["service"], {k: round(v, 3) for k, v in x.items() if isinstance(v, float)})
    print("gap 2.16", {k: round(v, 4) if isinstance(v, float) else v for k, v in gap216.items()})
    print("hail energy", {k: round(v, 2) for k, v in energy.items()}, "FTE line", round(a_t, 1), round(b_t, 1), "v for FTE 1.59", round(vel_fte159, 1))
    for x in hail:
        print(f"  hail {x['construction']:20s} {x['sizing']:16s} wall {x['wall_mm']:.3f} stress {x['hail_surface_stress_MPa']:7.1f} "
              f"op {x['operating_peak_MPa']:6.1f} left {x['screen_left_after_operating_MPa']:7.1f} ratio {x['hail_over_left']} FTE {x['ice_FTE_flat_panel_J']:.0f} margin {x['energy_margin_rho910']:.1f} b {x['fit_b']:.3f}")
    print("hard", hard)


if __name__ == "__main__":
    main()
