#!/usr/bin/env python3
"""MAINLINE-060: the carbon-framed P3 through 052's whole bill (this seat's own arithmetic on pinned inputs).

Tubes. 051's fresh-FE q>=1 witnesses (019 reserve, the family 052 resizes) give each carbon construction's
stiffness-sized tube mass and its peak laminate compression at operating pressure. The laminate's mean compressive
screen is its 0 deg ply's sourced unidirectional strength Xc divided by 051's 0 deg ply stress per unit laminate stress
(first-ply failure, PROJECTION).
- If the peak exceeds the screen, the wall thickens in proportion. Peak stress scales as 1/wall at fixed radius, which is
  conservative because thicker walls also cut Euler amplification.
- Reliability sizing uses 051's own frame target. Pf = 1 - exp(-H) with H = 0.0010005 (k(m) sigma_peak / scale)^m, where
  k(m) is 051's required whole-member scale over the peak at Pf 1e-3.
- The Weibull modulus follows from the sourced coefficient of variation by m = 1.2 / CV, and the scale = mean /
  Gamma(1 + 1/m). Coupon-to-member size scaling (V_coupon / V_member)^(1/m) is shown as a separate reading.

Bill. 052's MASS-ACCOUNT rows at R 10-30, ground service, with SiC tubes replaced:
- carbon tubes = 052's SiC tubes x (051 carbon witness / 051 041-reference witness) x the wall factor;
- sleeves at 052's actual value, or 5% of the carbon tubes under today's J;
- lift = 052's CARD endpoint payload + its endpoint bill.
054's dry cavity is added for one day (MET barrier) and seven days (SiOx barrier + 3A capture). Its R 10-15 rows are
used; R 20-30 extrapolate the barrier as R^2 and the capture as a + b R^2 fitted to R 10-15 (PROJECTION).

Writes CARBON.json."""
import csv
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import src60 as S  # noqa: E402

Q = "unpublished-local-ref:ab52dba26d6cc3a7"
RADII = (10, 12, 15, 20, 30)
L_MEMBER = 2.399569        # 051 CARD: mean arc length of its 750 members, m
COUPON_M3 = 3.2e-7         # 12.7 x 12.7 x 2 mm compression gauge (PROJECTION)


def art(rid, name):
    return next(a["path"] for a in json.load(open(f"{Q}/{rid}.json"))["artifacts"] if a["path"].endswith("/" + name))


R051, R052, R054 = ("rpt-ref-17635c55001d23054259", "rpt-ref-d7b2450119f373b2d1db",
                    "rpt-ref-71723c1ae93445240630")


def k_of_m(gaps, material, m, pf=1e-3):
    """051's required whole-member scale / peak at Pf, interpolated in log k against log m (operating, witness section)."""
    rows = [r for r in gaps if r["material"] == material and r["reserve"] == "019" and r["load_case"] == "operating"
            and r["section_policy"] == "verified_q1_1" and r.get("peak_Pa")]
    if not rows:
        rows = [r for r in gaps if r["material"] == material and r["reserve"] == "019" and r["load_case"] == "operating" and r.get("peak_Pa")]
    r = rows[0]
    pts = sorted((t["m"], t["whole_member_scale_needed_Pa"] / r["peak_Pa"]) for t in r["targets"] if t["Pf"] == pf)
    for (m0, k0), (m1, k1) in zip(pts, pts[1:]):
        if m0 <= m <= m1:
            u = (math.log(m) - math.log(m0)) / (math.log(m1) - math.log(m0))
            return math.exp(math.log(k0) + u * (math.log(k1) - math.log(k0)))
    m0, k0 = pts[-1]
    return k0 if m >= m0 else pts[0][1]


def main():
    src = {}
    xc = {"K13D2U": S.val("xc_k13d2u", "compression", "ud_compression", "0 deg UD composite compressive strength", 340.0, "K13D2U"),
          "K13C2U": S.val("xc_k13c2u", "compression", "ud_compression", "0 deg UD composite compressive strength", 380.0, "K13C2U"),
          "YS-90A": S.val("xc_ys90a", "compression", "ud_compression", "0 deg UD composite compressive strength", 360.0, "YS-90A"),
          "YS-95A": S.val("xc_ys95a", "compression", "ud_compression", "0 deg UD composite compressive strength", 340.0, "YS-95A"),
          "K1352U": S.val("xc_k1352u", "compression", "ud_compression", "0 deg UD composite compressive strength", 450.0, "K1352U"),
          "M55J": S.val("xc_m55j", "compression", "ud_compression", "0 deg UD composite compressive strength", 890.0, "M55J / #2500"),
          "M46J": S.val("xc_m46j", "compression", "ud_compression", "0 deg UD composite compressive strength", 1080.0, "M46J"),
          "M60J": S.val("xc_m60j", "compression", "ud_compression", "0 deg UD composite compressive strength", 790.0, "M60J / #2500"),
          "T800S": S.val("xc_t800s", "compression", "ud_compression", "0 deg UD composite compressive strength", 1490.0, "T800S")}
    ecomp = {"K13D2U": S.val("ec_k13d2u", "compression", "ud_compression_modulus", "0 deg UD composite compressive modulus", 560.0, "K13D2U")}
    cv = {"K63712_measured": S.val("cv_k637", "compression", "compression_scatter", "Coefficient of variation of compressive failure stress", 5.1),
          "NCAMP_IM": S.val("cv_ncamp", "compression", "compression_scatter", "CV of 0 deg compressive strength", 5.198)}
    S.note("cmh17_cv", "compression", "compression_scatter", "CMH-17 statement")
    S.val("k637_meas", "compression", "ud_compression", "0 deg UD composite compressive failure stress, measured", 374.0, "K63712")
    src["xc_MPa"], src["ecomp_GPa"], src["cv_percent"] = xc, ecomp, cv
    joints = {"boeing44_fittings_lb": S.val("b44_ins", "joints", "fitting_mass", "titanium insert mass per strut (44K strut)", 1.2)
              + S.val("b44_ball", "joints", "fitting_mass", "titanium ball end fitting mass per strut (44K strut)", 1.5),
              "boeing44_total_lb": S.val("b44_tot", "joints", "fitting_mass", "total strut assembly mass incl. body", 16.01),
              "cordis_fitting_share": S.val("cordis", "joints", "fitting_mass", "fitting share of total strut mass", 70.0) / 100,
              "bonded_fitting_failure_fraction": S.val("bond70", "joints", "joint_strength", "bonded-fitting strut failure load in compression", 70.0) / 100}
    joints["boeing44_fitting_share"] = joints["boeing44_fittings_lb"] / joints["boeing44_total_lb"]
    src["joints"] = joints

    mats = {m["id"]: m for m in json.load(open(art(R051, "MATERIAL-MODELS.json")))}
    wit = {(r["material"], r["reserve"]): r["comparison_geometry"] for r in json.load(open(art(R051, "WITNESSES.json")))["rows"]}
    gaps = json.load(open(art(R051, "GAPS.json")))["rows"]
    psi = {k: -next(p["stress_per_unit_global_compression"][0] for p in v["ply_ratios"] if p["angle"] == 0)
           for k, v in mats.items() if v.get("kind") == "composite" and v.get("ply_ratios")}
    ref = wit[("041-reference", "019")]
    fibre_of = {"K13D2U": "K13D2U", "M55J": "M55J", "T700S": None}
    # T700S: 051's own Toray value (MATERIAL-MODELS ply_Xc 1.45 GPa), pinned through 051
    cons = []
    for mid in ("K13D2U-50-20-20-10", "K13D2U-70-10-10-10", "K13D2U-UD", "M55J-50-20-20-10", "M55J-70-10-10-10", "M55J-UD",
                "T700S-50-20-20-10", "T700S-70-10-10-10", "T700S-UD"):
        fib = mid.split("-")[0]
        X = xc.get(fib) if fib in xc else mats[mid]["ply_Xc_GPa"] * 1000
        g = wit[(mid, "019")]
        screen = X / 1000 / psi[mid]                         # GPa, laminate first-ply compression (mean)
        peak = g["q1_peak_compression_Pa"] / 1e9
        out = {"id": mid, "fibre": fib, "Xc_MPa": X, "Xc_source": "060 compression.json" if fib in xc else "051 MATERIAL-MODELS (Toray)",
               "psi_0deg": psi[mid], "laminate_screen_GPa": screen, "witness_tubes_kg": g["frame_tubes_kg"],
               "witness_frame_kg": g["frame_plus_joints_nodes_kg"], "witness_wall_mm": g["wall_m"] * 1e3,
               "witness_peak_GPa": peak, "mean_SF_at_witness": screen / peak, "Eax_GPa": mats[mid]["Eax_Pa"] / 1e9,
               "rho": mats[mid]["density_kgm3"], "ratio_to_SiC_witness": g["frame_tubes_kg"] / ref["frame_tubes_kg"]}
        out["f_mean"] = max(1.0, peak / screen)
        for lab, cvp in (("cv5.2", 5.2), ("cv6", 6.0)):
            m = 1.2 / (cvp / 100)
            k = k_of_m(gaps, mid, m)
            scale = screen / math.gamma(1 + 1 / m)
            size1 = (COUPON_M3 / (g["area_m2"] * L_MEMBER)) ** (1 / m)    # coupon -> one member at the witness wall
            x = peak * k / (scale * size1)
            f_size = max(1.0, x ** (m / (m - 1)))           # the member's volume grows with its wall: f = x^(m/(m-1))
            out[f"m_{lab}"] = m
            out[f"k_{lab}"] = k
            out[f"f_rel_{lab}"] = max(1.0, peak * k / scale)
            out[f"f_rel_size_{lab}"] = f_size
            out[f"size_factor_{lab}"] = size1 * f_size ** (-1 / m)
            H = 0.0010005 * (k * peak / out["f_mean"] / scale) ** m
            out[f"Pf_at_mean_section_{lab}"] = 1 - math.exp(-H) if H < 700 else 1.0
        out["Xc_needed_for_witness_mean_MPa"] = peak * psi[mid] * 1000
        out["Xc_needed_for_witness_Pf1e3_cv6_MPa"] = peak * psi[mid] * out["k_cv6"] * math.gamma(1 + 1 / out["m_cv6"]) * 1000
        cons.append(out)

    # 052's rows and lift
    m052 = list(csv.DictReader(open(art(R052, "MASS-ACCOUNT.csv"))))
    card052 = art(R052, "CARD.md")
    ep052 = {}
    for line in open(card052):
        mm = re.match(r"\| (\d+) \| (ISA|optimistic|both) \| (-?[\d,]+\.\d+) \|", line)
        if mm:
            ep052[(int(mm.group(1)), mm.group(2))] = float(mm.group(3).replace(",", ""))
    lines = ["SiC_tubes", "joint_sleeves_and_allowance", "joint_bond_and_installation", "nodes", "PBO_two_plies", "barrier_and_protection",
             "systems", "vacuum_service", "gas", "exterior_water", "contamination", "mooring_load_introduction", "sag_lift_debit", "weather_headroom"]

    def row(R, w, sel):
        return next(r for r in m052 if int(r["R_m"]) == R and r["weather"] == w and r["service"] == "ground" and r["selection"] == sel)
    lift = {}
    for R in RADII:
        for w in ("ISA", "optimistic"):
            e = row(R, w, "all_endpoints")
            lift[(R, w)] = ep052[(R, w)] + sum(float(e[k]) for k in lines)
    # 054 dry cavity increments over 052's endpoint (one day MET barrier; seven days SiOx + 3A)
    m054 = list(csv.DictReader(open(art(R054, "MASS-ACCOUNT.csv"))))

    def r054(R, w, cand, days, route):
        return next((r for r in m054 if int(r["R_m"]) == R and r["weather"] == w and r["account"] == "endpoint" and r["candidate"] == cand
                     and r["days"] == days and r["route"] == route), None)
    cav = {}
    fit = []
    for R in (10, 12, 15):
        x = r054(R, "ISA", "SIOX", "7", "barrier_plus_3A")
        cap = sum(float(x[k]) for k in ("bed_dry_kg", "housing_kg", "distribution_monitoring_kg", "battery_kg"))
        fit.append((R * R, cap))
    (x0, y0), (x1, y1) = fit[0], fit[-1]
    b = (y1 - y0) / (x1 - x0)
    a = y0 - b * x0
    bar = {}
    for R in (10, 12, 15):
        e = row(R, "ISA", "all_endpoints")
        bar[R] = {"MET": float(r054(R, "ISA", "MET", "1", "barrier_only")["barrier_and_protection"]) - float(e["barrier_and_protection"]),
                  "SIOX": float(r054(R, "ISA", "SIOX", "7", "barrier_plus_3A")["barrier_and_protection"]) - float(e["barrier_and_protection"])}
    for R in RADII:
        for w in ("ISA", "optimistic"):
            if R in (10, 12, 15):
                d1 = ep052[(R, w)] - float(r054(R, w, "MET", "1", "barrier_only")["payload_kg"])
                d7 = ep052[(R, w)] - float(r054(R, w, "SIOX", "7", "barrier_plus_3A")["payload_kg"])
                basis = "054 rows"
            else:
                d1 = bar[10]["MET"] * (R / 10) ** 2
                d7 = bar[10]["SIOX"] * (R / 10) ** 2 + a + b * R * R
                basis = "extrapolated from 054's R10-15 (barrier as R^2, capture a + b R^2)"
            cav[(R, w)] = {"one_day_kg": d1, "seven_day_kg": d7, "basis": basis}

    acct = []
    for c in cons:
        for R in RADII:
            for w in ("ISA", "optimistic"):
                for sel in ("all_endpoints", "baseline"):
                    base = row(R, w, sel)
                    ends = row(R, w, "all_endpoints")
                    sic_ref = float(ends["SiC_tubes"])               # stiffness-sized SiC tubes (052 endpoints)
                    others = sum(float(base[k]) for k in lines if k not in ("SiC_tubes", "joint_sleeves_and_allowance"))
                    sleeves_actual = float(ends["joint_sleeves_and_allowance"])
                    for sizing in ("witness", "mean", "Pf1e-3_cv6", "Pf1e-3_cv6_size"):
                        f = {"witness": 1.0, "mean": c["f_mean"], "Pf1e-3_cv6": c["f_rel_cv6"], "Pf1e-3_cv6_size": c["f_rel_size_cv6"]}[sizing]
                        tubes = sic_ref * c["ratio_to_SiC_witness"] * f
                        sleeves = sleeves_actual if sel == "all_endpoints" else max(sleeves_actual, 0.05 * tubes)
                        total = others + tubes + sleeves
                        pay = lift[(R, w)] - total
                        acct.append({"construction": c["id"], "R_m": R, "weather": w, "axes": sel, "sizing": sizing, "wall_factor": f,
                                     "tubes_kg": tubes, "sleeves_kg": sleeves, "total_kg": total, "lift_kg": lift[(R, w)],
                                     "payload_kg": pay, "payload_one_day_kg": pay - cav[(R, w)]["one_day_kg"],
                                     "payload_seven_day_kg": pay - cav[(R, w)]["seven_day_kg"]})
    # SiC reference on the same arithmetic (052 endpoints reproduce)
    sic = []
    for R in RADII:
        for w in ("ISA", "optimistic"):
            e = row(R, w, "all_endpoints")
            tot = sum(float(e[k]) for k in lines)
            sic.append({"R_m": R, "weather": w, "payload_kg": lift[(R, w)] - tot, "card_payload_kg": ep052[(R, w)],
                        "payload_one_day_kg": lift[(R, w)] - tot - cav[(R, w)]["one_day_kg"],
                        "payload_seven_day_kg": lift[(R, w)] - tot - cav[(R, w)]["seven_day_kg"], "SiC_tubes_kg": float(e["SiC_tubes"])})
    # the compression the best stiffness case needs to float (K13D2U 50/20/20/10, 052 endpoints)
    k13 = next(c for c in cons if c["id"] == "K13D2U-50-20-20-10")
    need = []
    for R in RADII:
        for w in ("ISA", "optimistic"):
            e = row(R, w, "all_endpoints")
            sic_ref = float(e["SiC_tubes"])
            t1 = sic_ref * k13["ratio_to_SiC_witness"]
            pay1 = lift[(R, w)] - (sum(float(e[k]) for k in lines) - sic_ref + t1)
            for days, d in (("ground", 0.0), ("one_day", cav[(R, w)]["one_day_kg"]), ("seven_day", cav[(R, w)]["seven_day_kg"])):
                fmax = (pay1 - d + t1) / t1                      # largest wall factor that still floats
                need.append({"R_m": R, "weather": w, "service": days, "payload_at_witness_kg": pay1 - d, "max_wall_factor": fmax,
                             "Xc_needed_mean_MPa": None if fmax <= 0 else k13["Xc_needed_for_witness_mean_MPa"] / fmax,
                             "Xc_needed_Pf1e3_cv6_MPa": None if fmax <= 0 else k13["Xc_needed_for_witness_Pf1e3_cv6_MPa"] / fmax})
    out = {"basis": __doc__, "sources": src, "constructions": cons, "account": acct, "sic_reference": sic, "cavity": {f"{R}|{w}": v for (R, w), v in cav.items()},
           "cavity_fit": {"a": a, "b": b, "barrier_increment_R10": bar[10]}, "lift": {f"{R}|{w}": v for (R, w), v in lift.items()},
           "k13_compression_to_float": need, "sources_used": S.USED,
           "pins": {n: art(r, n) for r, n in ((R051, "MATERIAL-MODELS.json"), (R051, "WITNESSES.json"), (R051, "GAPS.json"),
                                               (R051, "HAIL-DESIGN.csv"), (R051, "CARD.md"), (R052, "MASS-ACCOUNT.csv"), (R052, "CARD.md"),
                                               (R054, "MASS-ACCOUNT.csv"), (R054, "CARD.md"))}}
    with open(os.path.join(HERE, "CARBON.json.tmp"), "w") as fh:
        json.dump(out, fh, indent=1)
    os.replace(os.path.join(HERE, "CARBON.json.tmp"), os.path.join(HERE, "CARBON.json"))
    for c in cons:
        print(f"{c['id']:20s} Xc {c['Xc_MPa']:6.0f} psi {c['psi_0deg']:.3f} screen {c['laminate_screen_GPa']:.3f} GPa | witness {c['witness_tubes_kg']:7.0f} kg peak {c['witness_peak_GPa']:.3f} "
              f"meanSF {c['mean_SF_at_witness']:.3f} | f_mean {c['f_mean']:.2f} f_rel(cv6) {c['f_rel_cv6']:.2f} f_rel+size {c['f_rel_size_cv6']:.2f} | Pf at mean section {c['Pf_at_mean_section_cv6']:.3g}")
    for x in sic:
        print("SiC", x["R_m"], x["weather"], round(x["payload_kg"], 2), "card", x["card_payload_kg"], "| 1d", round(x["payload_one_day_kg"], 2), "7d", round(x["payload_seven_day_kg"], 2))
    for x in acct:
        if x["axes"] == "all_endpoints" and x["weather"] == "ISA" and x["construction"] in ("K13D2U-50-20-20-10", "M55J-50-20-20-10", "M55J-70-10-10-10", "T700S-70-10-10-10"):
            print(f"  {x['construction']:20s} R{x['R_m']} {x['sizing']:16s} f {x['wall_factor']:.2f} tubes {x['tubes_kg']:9.0f} payload {x['payload_kg']:+10.0f} 1d {x['payload_one_day_kg']:+10.0f} 7d {x['payload_seven_day_kg']:+10.0f}")
    for x in need:
        if x["weather"] == "ISA":
            print("K13 needs", x)


if __name__ == "__main__":
    main()
