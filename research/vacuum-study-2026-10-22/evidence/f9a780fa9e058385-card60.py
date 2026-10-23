#!/usr/bin/env python3
"""MAINLINE-060: CARD.md, RESULTS.json, NFI.json and INPUTS.json from CARBON.json and EXTRA.json."""
import csv
import datetime
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from carbon60 import art, R051, R052, R054  # noqa: E402

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def acc(cid, R, sizing, w="ISA", axes="all_endpoints"):
    return next(x for x in C["account"] if x["construction"] == cid and x["R_m"] == R and x["weather"] == w and x["axes"] == axes
                and x["sizing"] == sizing)


def sic(R, w="ISA"):
    return next(x for x in C["sic_reference"] if x["R_m"] == R and x["weather"] == w)


def kg(v):
    return f"{v:+,.0f}"


def main():
    k13 = CONS["K13D2U-50-20-20-10"]
    gap = X["gap_to_2p16"]
    # the best frame at each sizing, by R 10 ISA endpoint payload
    best = {s: max(CONS, key=lambda c: acc(c, 10, s)["payload_kg"]) for s in ("witness", "mean", "Pf1e-3_cv6", "Pf1e-3_cv6_size")}
    fr = best["Pf1e-3_cv6"]                                   # the best-supported frame: lightest meeting Pf 1e-3 on sourced data
    floats = [x for x in C["account"] if x["sizing"] != "witness" and x["payload_kg"] > 0]
    assert not floats, floats[:2]
    need = {(x["R_m"], x["weather"], x["service"]): x for x in X["to_float"]}
    jt = {(x["construction"], x["R_m"], x["weather"], x["sizing"], x["share"]): x for x in X["joints"]["rows"]}
    first_b44 = next(R for R in RADII if jt[("K13D2U-50-20-20-10", R, "ISA", "witness", "Boeing_44K")]["payload_kg"] > 0)
    rel = {(x["construction"], x["cv"], x["sizing"]): x for x in X["reliability"]}
    hail = {(x["construction"], x["sizing"]): x for x in X["hail"]["rows"]}
    H = X["hail"]
    e910 = H["design"]["energy_J"]["rho_910"]
    e_lo, e_hi = H["design"]["energy_J"]["rho_810"], H["design"]["energy_J"]["rho_920"]
    fte159 = H["flat_panel_FTE_508mm"]["1.59"]
    hk = hail[("K13D2U-50-20-20-10", "witness")]
    hm = hail[("M55J-50-20-20-10", "witness")]
    hfr = hail[(fr, "Pf1e-3_cv6")]
    m55 = CONS["M55J-50-20-20-10"]
    cav7 = {R: C["cavity"][f"{R}|ISA"]["seven_day_kg"] for R in RADII}
    cav1 = {R: C["cavity"][f"{R}|ISA"]["one_day_kg"] for R in RADII}
    mx = {R: 1 + sic(R)["payload_kg"] / sic(R)["SiC_tubes_kg"] for R in RADII}     # the heaviest tube bill that floats, over SiC's
    J = X["joints"]
    k70_first = next(R for R in RADII if acc("K13D2U-70-10-10-10", R, "witness")["payload_kg"] > 0)
    k13_worst = min(acc("K13D2U-50-20-20-10", 10, "witness", w, ax)["payload_seven_day_kg"]
                    for w in ("ISA", "optimistic") for ax in ("all_endpoints", "baseline"))
    w5 = next(r["comparison_geometry"]["frame_tubes_kg"] for r in json.load(open(art(R051, "WITNESSES.json")))["rows"]
              if r["material"] == "K13D2U-50-20-20-10" and r["reserve"] == "5")
    lk = [C["lift"][f"{R}|{w}"] / R ** 3 for R in RADII for w in ("ISA", "optimistic")]
    lift_k = lk[0]
    assert max(lk) - min(lk) < 1e-6 * lift_k
    m054 = list(csv.DictReader(open(art(R054, "MASS-ACCOUNT.csv"))))
    m052 = list(csv.DictReader(open(art(R052, "MASS-ACCOUNT.csv"))))
    lift_d = max(abs(float(r["lift_kg"]) - C["lift"][f"{r['R_m']}|{r['weather']}"]) for r in m054 if r["weather"] in ("ISA", "optimistic"))
    cav_d = 0.0
    for R in (10, 12, 15):
        e = next(r for r in m052 if int(r["R_m"]) == R and r["weather"] == "ISA" and r["service"] == "ground" and r["selection"] == "all_endpoints")
        for cand, days, route, key in (("SIOX", "7", "barrier_plus_3A", "seven_day_kg"), ("MET", "1", "barrier_only", "one_day_kg")):
            s = next(r for r in m054 if int(r["R_m"]) == R and r["weather"] == "ISA" and r["account"] == "endpoint" and r["candidate"] == cand
                     and r["days"] == days and r["route"] == route)
            hw = sum(float(s[k]) for k in ("bed_dry_kg", "housing_kg", "distribution_monitoring_kg", "battery_kg"))
            inc = float(s["barrier_and_protection"]) - float(e["barrier_and_protection"]) + hw
            cav_d = max(cav_d, abs(inc - C["cavity"][f"{R}|ISA"][key]))
            assert all(abs(float(e[k]) - float(s[k])) < 1e-9 for k in LINES if k != "barrier_and_protection")
    cap12 = C["cavity"]["12|ISA"]["seven_day_kg"] - C["cavity_fit"]["barrier_increment_R10"]["SIOX"] * 1.44
    fit12 = abs(C["cavity_fit"]["a"] + C["cavity_fit"]["b"] * 144 - cap12) / cap12
    assert lift_d < 0.01 and cav_d < 0.01 and fit12 < 0.01
    used = C["sources_used"]
    m = {k: v for k, v in used.items()}
    L = []
    a = L.append
    a("# MAINLINE-060: the carbon-framed P3. ESTIMATE")
    a("")
    a(f"Unit vacuum-mainline060-p3-carbon-frame-1020. Order {ORDER}, which replaced {FIRST} to drop its deadline. Status ESTIMATE. "
      "Values are QUESTIONABLE, and PROJECTION where named. Nothing here is a certification. Started 06:58:23 PDT when the order "
      "was read; the end time is in RESULTS.json. Times are measurements, not limits.")
    a("")
    a("## The answer")
    a("")
    a(f"- **Does a carbon-framed P3 float? No, at no radius from 10 to 30 m, on sourced compression.** That holds even at mean "
      f"strength, with all of 052's endpoint optimisms and ground vacuum service. The best case at mean strength is "
      f"{NICE[best['mean']]}: {kg(acc(best['mean'], 10, 'mean')['payload_kg'])} kg at R 10 ISA and "
      f"{kg(acc(best['mean'], 30, 'mean')['payload_kg'])} kg at R 30. A frame sized to mean strength fails with Pf near 1, so it "
      f"is not a design. The best-supported frame is the lightest that meets 051's Pf 1e-3 with carbon's own scatter: "
      f"{NICE[fr]}, walls x{CONS[fr]['f_rel_cv6']:.2f}. It gives {kg(acc(fr, 10, 'Pf1e-3_cv6')['payload_kg'])} kg at R 10 ISA "
      f"and {kg(acc(fr, 30, 'Pf1e-3_cv6')['payload_kg'])} kg at R 30.")
    a(f"- **On which optimisms it would float.** Only the light pitch layups can float, and only if their compression is ignored: "
      f"{NICE['K13D2U-50-20-20-10']} from R 10, and {NICE['K13D2U-70-10-10-10']} from R {k70_first}. At its stiffness wall "
      f"{NICE['K13D2U-50-20-20-10']} gives {kg(acc('K13D2U-50-20-20-10', 10, 'witness')['payload_kg'])} kg at R 10 ISA "
      f"and {kg(acc('K13D2U-50-20-20-10', 30, 'witness')['payload_kg'])} kg at R 30. At R 10 it still floats with 052's optimistic "
      f"weather, its baseline film and joint axes and seven days of dry cavity together ({kg(k13_worst)} kg). "
      f"So the one optimism that matters is compression. Its tubes must carry at least "
      f"{need[(10, 'ISA', 'ground')]['laminate_mean_needed_GPa']:.2f} GPa of laminate compression at mean, "
      f"{need[(10, 'ISA', 'ground')]['laminate_mean_needed_GPa'] / k13['laminate_screen_GPa']:.1f} times the sourced "
      f"{k13['laminate_screen_GPa']:.2f} GPa. That needs a UD 0 deg strength of {need[(10, 'ISA', 'ground')]['Xc_needed_mean_MPa'] / 1000:.2f} GPa "
      f"at mean. For Pf 1e-3 it needs {need[(10, 'ISA', 'ground')]['Xc_needed_Pf1e3_cv6_MPa'] / 1000:.2f} GPa, or "
      f"{need[(10, 'ISA', 'ground')]['Xc_needed_Pf1e3_cv6_size_MPa'] / 1000:.2f} GPa with coupon-to-tube size scaling. "
      f"The sourced value is {k13['Xc_MPa']:.0f} MPa. The second optimism is 052's lean SiC joint bill: with titanium end "
      f"fittings at the sourced Boeing strut share, it floats only from R {first_b44}.")
    a(f"- **Is it a better lead than SiC? No.** SiC floats on paper ({kg(sic(10)['payload_kg'])} kg at R 10 ISA), with one unknown: "
      f"its whole-tube strength. The light carbon layup misses by a factor of three in compression on sourced data. The PAN layups "
      f"that are strong enough are stiffness-heavy: {NICE['M55J-50-20-20-10']}'s tubes weigh {m55['ratio_to_SiC_witness']:.3f} "
      f"times SiC's, and P3 floats only below {mx[10]:.3f} (R 10) to {mx[30]:.3f} (R 30). Carbon's real advantage is damage "
      f"(below) and tight scatter (m about 20 against SiC's assumed 10). Neither closes the strength gap.")
    a(f"- **The single test that would ground it.** Compress about 30 full-length wrapped {NICE['K13D2U-50-20-20-10']} tubes "
      f"(2.4 m, 247 mm outer diameter, 1.45-1.70 mm wall) with their end fittings, to failure. At R 10 the frame floats only if the "
      f"tubes carry a laminate mean of at least {need[(10, 'ISA', 'ground')]['laminate_mean_needed_GPa']:.2f} GPa. For Pf 1e-3 it "
      f"also needs a whole-tube Weibull scale of at least {need[(10, 'ISA', 'ground')]['member_scale_needed_cv6_GPa']:.2f} GPa at m 20. "
      f"Sourced data predict {k13['laminate_screen_GPa']:.2f} GPa, so the test is more likely to close the option than to open it. "
      "A flat-laminate compression coupon of the same layup is the cheap first gate.")
    a("")
    a("## 1. What the tubes carry")
    a("")
    a("**Sourced 0 deg compressive strength of unidirectional laminates (data sheets, 60% fibre volume, epoxy; all QUESTIONABLE):**")
    a("")
    a("| Fibre (class) | UD compression, MPa | UD modulus, GPa | Source |")
    a("|---|---|---|---|")
    rows = json.load(open(f"{SRC}/compression.json"))["rows"]
    mod = {r["product"].split("/")[0].strip(): r["value"] for r in rows if r["property_id"] == "ud_compression_modulus"}
    seen = set()
    for r in sorted((r for r in rows if r["property_id"] == "ud_compression" and r["units"] == "MPa"), key=lambda r: r["value"]):
        name = r["product"].split("/")[0].strip()
        org = r["source"]["org_or_authors"]
        who = "Montagnier and Hochard (measured)" if "Montagnier" in org else org.split("(")[0].strip()
        if (name.upper(), who) in seen:
            continue
        seen.add((name.upper(), who))
        a(f"| {name} | {r['value']:g} | {mod.get(name, '') if 'measured' not in who else ''} | {who} |")
    a("")
    a(f"- **Pitch fibres:** the ultra-high-modulus pitch fibres carry 340-380 MPa. The best pitch value, "
      f"{gap['best_sourced_pitch_Xc_MPa']:.0f} MPa, belongs to a 160 GPa fibre. The one independent measurement (K63712, "
      f"Montagnier and Hochard) found {gap['K63712_measured_MPa']:.0f} MPa against the maker's {gap['K63712_maker_MPa']:.0f}, "
      f"{(1 - gap['K63712_measured_MPa'] / gap['K63712_maker_MPa']) * 100:.0f}% lower.")
    a(f"- **High-modulus PAN fibres:** 785-1,080 MPa. A 2025 Nippon Steel report gives a compression-to-tension ratio of "
      f"{gap['compression_over_tension']['PAN_230GPa']:g} for a 230 GPa PAN fibre and "
      f"{gap['compression_over_tension']['pitch_XN15_155GPa']:g} for a 155 GPa pitch fibre.")
    a(f"- **Scatter:** the coefficient of variation of compressive strength is {m['cv_k637']['value']}% (K63712, n=6) and "
      f"{m['cv_ncamp']['value']}% (an NCAMP IM fibre). CMH-17 expects at least 6%. These give m = 1.2/CV of about 20-23.5 "
      "(PROJECTION).")
    a("- **Not found:** tube or strut compression tests, quasi-isotropic or multidirectional laminate compression, and a "
      "Weibull modulus, for any pitch or M-series fibre.")
    a("")
    a(f"**What 50/20/20/10 gives.** The 0 deg ply fails first. Per unit of laminate stress, 051's laminate model puts "
      f"{k13['psi_0deg']:.4f} on that ply. The laminate's mean first-ply compression is therefore {k13['Xc_MPa']:.0f}/"
      f"{k13['psi_0deg']:.4f} = {k13['laminate_screen_GPa']:.3f} GPa (PROJECTION). Its Weibull scale is "
      f"{gap['laminate_scale_m10_GPa']:.3f} GPa at m 10 and {gap['laminate_scale_m20_GPa']:.3f} GPa at m 20. "
      f"**That is {gap['times_mean']:.1f} times below 051's 2.16 GPa** ({gap['times_scale_m10']:.1f} times in scale at m 10). "
      f"Reaching 2.16 GPa at m 10 would need a 0 deg ply strength of {gap['Xc_UD_needed_m10_MPa'] / 1000:.2f} GPa, above every "
      f"sourced carbon laminate (T800S {m['xc_t800s']['value']:.0f} MPa). At 051's own stiffness-sized wall the tubes carry "
      f"{k13['witness_peak_GPa']:.3f} GPa at q 1: a mean safety factor of {k13['mean_SF_at_witness']:.3f}.")
    a("")
    a("**Every construction at 051's 019-reserve witness (tube mass scales with wall; peak stress with 1/wall):**")
    a("")
    a("| Construction | UD strength, MPa | 0 deg ply ratio | Laminate mean, GPa | Witness tubes, kg | Peak at q 1, GPa | Mean SF | "
      "Wall for mean | Wall for Pf 1e-3 (CV 5.2 / 6%) | With size scaling (CV 6%) | Pf at witness (CV 6%) |")
    a("|---|---|---|---|---|---|---|---|---|---|---|")
    for cid, c in CONS.items():
        a(f"| {NICE[cid]} | {c['Xc_MPa']:.0f} | {c['psi_0deg']:.3f} | {c['laminate_screen_GPa']:.3f} | {c['witness_tubes_kg']:,.0f} | "
          f"{c['witness_peak_GPa']:.3f} | {c['mean_SF_at_witness']:.3f} | x{c['f_mean']:.2f} | x{c['f_rel_cv5.2']:.2f} / x{c['f_rel_cv6']:.2f} | "
          f"x{c['f_rel_size_cv6']:.2f} | {rel[(cid, 'cv6', 'witness')]['Pf_coupon_scale_as_member']:.3g} |")
    a("")
    a("The T700S strength is 051's Toray value, not re-sourced here. T700S frames are stiffness-limited, so it does not decide anything.")
    a("")
    a("## 2. The whole bill")
    a("")
    a("**Method.** 052's account is used line by line, ground service, R 10-30.")
    a("- **Tubes:** the SiC tubes are replaced by 052's stiffness-sized SiC tubes x (051's carbon witness / 051's 041 reference "
      "witness) x the wall factor.")
    a("- **Kept unchanged:** the film (PBO plies, barrier and protection), the joint lines (sleeves, bond, nodes), systems, vacuum "
      "service, gas, water, contamination, mooring, sag and weather headroom.")
    a("- **Lift:** 052's card endpoint payload plus its endpoint bill (checked below against R^3 and 054's lift).")
    a("- **Dry cavity:** 054's increment over ground service. One day is the MET barrier; seven days are the SiOx barrier plus a "
      "3A sieve. These are 054's R 10-15 rows; R 20 and 30 are extrapolated (barrier as R^2, capture as a + bR^2; PROJECTION). "
      "054's ALD and ML3 carriers are not used, as 054 did not verify them.")
    a("")
    a("**Line by line at R 10, ISA, 052's endpoints, kg:**")
    a("")
    b = list(csv.DictReader(open(art(R052, "MASS-ACCOUNT.csv"))))
    e10 = next(r for r in b if int(r["R_m"]) == 10 and r["weather"] == "ISA" and r["service"] == "ground" and r["selection"] == "all_endpoints")
    cols = [("SiC (052)", None), ("K13D2U 50/20/20/10, stiffness wall", ("K13D2U-50-20-20-10", "witness")),
            ("K13D2U 50/20/20/10, mean strength", ("K13D2U-50-20-20-10", "mean")),
            (f"{NICE[best['mean']]}, mean strength", (best["mean"], "mean")), (f"{NICE[fr]}, Pf 1e-3", (fr, "Pf1e-3_cv6"))]
    a("| Line | " + " | ".join(c for c, _ in cols) + " |")
    a("|---|" + "---|" * len(cols))
    for ln in LINES:
        cells = []
        for _, sel in cols:
            if sel is None:
                v = float(e10[ln])
            else:
                x = acc(sel[0], 10, sel[1])
                v = x["tubes_kg"] if ln == "SiC_tubes" else x["sleeves_kg"] if ln == "joint_sleeves_and_allowance" else float(e10[ln])
            cells.append(f"{v:,.1f}")
        a(f"| {'tubes' if ln == 'SiC_tubes' else ln.replace('_', ' ')} | " + " | ".join(cells) + " |")
    tot = [sum(float(e10[k]) for k in LINES)] + [acc(s[0], 10, s[1])["total_kg"] for _, s in cols[1:]]
    pay = [sic(10)["payload_kg"]] + [acc(s[0], 10, s[1])["payload_kg"] for _, s in cols[1:]]
    a("| **total** | " + " | ".join(f"{v:,.1f}" for v in tot) + " |")
    a(f"| lift | " + " | ".join(f"{C['lift']['10|ISA']:,.1f}" for _ in cols) + " |")
    a("| **payload, ground** | " + " | ".join(f"{v:+,.1f}" for v in pay) + " |")
    a("| dry cavity, 1 day | " + " | ".join(f"{cav1[10]:,.2f}" for _ in cols) + " |")
    a("| dry cavity, 7 days | " + " | ".join(f"{cav7[10]:,.1f}" for _ in cols) + " |")
    a("")
    a("**Payload by radius, ISA, 052's endpoints, kg (ground / 1 day / 7 days of dry cavity):**")
    a("")
    a("| Frame | " + " | ".join(f"R {R}" for R in RADII) + " |")
    a("|---|" + "---|" * len(RADII))
    a("| SiC (052) | " + " | ".join(f"{kg(sic(R)['payload_kg'])} / {kg(sic(R)['payload_one_day_kg'])} / {kg(sic(R)['payload_seven_day_kg'])}" for R in RADII) + " |")
    for cid, s in (("K13D2U-50-20-20-10", "witness"), ("K13D2U-50-20-20-10", "mean"), ("K13D2U-50-20-20-10", "Pf1e-3_cv6"),
                   ("M55J-50-20-20-10", "witness"), (fr, "Pf1e-3_cv6"), (best["Pf1e-3_cv6_size"], "Pf1e-3_cv6_size"),
                   ("T700S-70-10-10-10", "witness")):
        a(f"| {NICE[cid]}, {SIZ[s]} | " + " | ".join(
            f"{kg(acc(cid, R, s)['payload_kg'])} / {kg(acc(cid, R, s)['payload_one_day_kg'])} / {kg(acc(cid, R, s)['payload_seven_day_kg'])}"
            for R in RADII) + " |")
    a("")
    a(f"052's optimistic-weather case and its baseline axes (PBO ply 3.48 GPa, retention 0.8616, sleeves at 5% of the tubes) "
      f"lower every row. For example, {NICE[fr]} at Pf 1e-3 gives {kg(acc(fr, 10, 'Pf1e-3_cv6', 'optimistic')['payload_kg'])} kg "
      f"(optimistic weather) and {kg(acc(fr, 10, 'Pf1e-3_cv6', 'ISA', 'baseline')['payload_kg'])} kg (baseline axes) at R 10. "
      "All rows are in CARBON.json.")
    a("")
    a(f"**The cubic penalty.** Carbon tubes scale as R^3, like lift. P3 floats only while the tube bill stays below "
      f"{mx[10]:.4f} times SiC's at R 10, {mx[15]:.4f} at R 15 and {mx[30]:.4f} at R 30 (ISA endpoints). So a construction heavier "
      f"than that never floats at any size. At its stiffness wall, {NICE['M55J-50-20-20-10']} is {m55['ratio_to_SiC_witness']:.4f} "
      f"and {NICE['M55J-70-10-10-10']} is {CONS['M55J-70-10-10-10']['ratio_to_SiC_witness']:.4f}. The light pitch layup is "
      f"{k13['ratio_to_SiC_witness']:.4f}, so it floats only below a wall factor of "
      f"{need[(10, 'ISA', 'ground')]['max_wall_factor']:.3f} (R 10) to {need[(30, 'ISA', 'ground')]['max_wall_factor']:.3f} (R 30).")
    a("")
    a(f"**Joints (QUESTIONABLE).** 052's SiC joint bill is kept: {float(e10['joint_sleeves_and_allowance']):.1f} kg of sleeves at R 10. "
      "Carbon tubes need bonded end fittings, so the sourced strut fitting shares are used as a sensitivity:")
    a(f"- **Boeing 44K strut:** titanium insert and ball are {J['shares']['Boeing_44K'] * 100:.1f}% of the strut, or "
      f"{J['fittings_per_tube']['Boeing_44K']:.3f} times the tube. Even the strength-ignored {NICE['K13D2U-50-20-20-10']} frame then gives "
      f"{kg(jt[('K13D2U-50-20-20-10', 10, 'ISA', 'witness', 'Boeing_44K')]['payload_kg'])} kg at R 10, and floats only from R {first_b44} "
      f"({kg(jt[('K13D2U-50-20-20-10', 30, 'ISA', 'witness', 'Boeing_44K')]['payload_kg'])} kg at R 30).")
    a(f"- **Typical space strut:** fittings are {J['shares']['space_strut_typical'] * 100:.0f}% of the strut, or "
      f"{J['fittings_per_tube']['space_strut_typical']:.2f} times the tube. No frame floats.")
    a(f"- **Load:** each tube carries up to {J['peak_tube_load_kN']:.0f} kN ({J['peak_tube_load_klb']:.0f} klb) at q 1. That is "
      f"{J['peak_tube_load_klb'] / abs(J['ng2_klb']):.2f} times the largest sourced composite strut failure ({abs(J['ng2_klb']):.1f} klb, "
      f"Northrop Grumman NG-2). Bonded-fitting struts failed at about {J['bonded_fitting_knockdown'] * 100:.0f}% of their compressive "
      "design ultimate.")
    a("")
    a("## 3. Reliability and damage")
    a("")
    a("**Pf with carbon's own scatter.** This uses 051's frame sum, H = 0.0010005 (k(m) peak / scale)^m, and 051's k(m) for each "
      "construction (Pf 1e-3, operating). The scale is the sourced mean / Gamma(1 + 1/m), with m from the coefficient of variation.")
    a("- **Size scaling:** the size-scaled reading moves the coupon scale (a 0.32 cm3 compression gauge; PROJECTION) to one tube's "
      "volume as (V coupon / V tube)^(1/m).")
    a(f"- **At the stiffness walls:** Pf is near 1 for both multidirectional K13D2U layups, K13D2U UD "
      f"({rel[('K13D2U-UD', 'cv6', 'witness')]['Pf_coupon_scale_as_member']:.3f}) and {NICE['M55J-50-20-20-10']}. "
      f"{NICE['M55J-70-10-10-10']} is {rel[('M55J-70-10-10-10', 'cv6', 'witness')]['Pf_coupon_scale_as_member']:.2f}.")
    a(f"- **To meet 1e-3:** at CV 6% the walls must be x{CONS[fr]['f_rel_cv6']:.2f} ({NICE[fr]}) to x{k13['f_rel_cv6']:.2f} "
      f"({NICE['K13D2U-50-20-20-10']}). With size scaling they must be x{CONS[fr]['f_rel_size_cv6']:.2f} to x{k13['f_rel_size_cv6']:.2f}.")
    a(f"- **Already below 1e-3:** M55J UD and every T700S frame, at their stiffness walls, at "
      f"{rel[('M55J-UD', 'cv6', 'witness')]['Pf_size_scaled']:.1e} and below with size scaling. They are the heavy ones.")
    a("- **Scatter:** carbon's scatter is tight (m about 20 against SiC's assumed 10), so its size penalty is mild (x0.56-0.64). "
      "Its mean strength is the problem.")
    a("")
    a(f"**Design hail on a carbon tube.** 051's design strike is 50.8 mm ice at 32.0 m/s: {e_lo:.1f}-{e_hi:.1f} J over the "
      "sourced natural-hail density range of 810-920 kg/m3.")
    a(f"- **Ice on flat carbon panels.** Ice first delaminates a 1.59 mm quasi-isotropic T800 panel at {fte159:.0f} J with 50.8 mm "
      f"ice; the source prints \"{X['sources_used']['fte_1.59']['printed']}\" (FAA JAMS, Kim et al. 2010, an interim table). That is "
      f"{fte159 / e910:.1f} times the design energy. The threshold is linear in thickness: {H['fte_line']['a_J']:.0f} + "
      f"{H['fte_line']['b_J_per_mm']:.0f} J/mm, so {hk['ice_FTE_flat_panel_J']:.0f} J at the pitch layup's 1.45 mm wall (x"
      f"{hk['energy_margin_rho910']:.1f}). AS4/8552 at 4 mm needs {H['pernas_4mm_50mm']:.0f} J with 50 mm ice. On these data a "
      "design strike most likely leaves the laminate intact, unlike SiC's 1-5% fracture per strike (045, 051).")
    a(f"- **Hard impactors.** 20 J punctured 76-102 mm CFRP tubes, and barely visible damage needs 10.8-20 J on 4 mm laminates. "
      f"These are not ice, but they show what a thin carbon wall gives up. If a strike does delaminate, the one paired "
      f"compression-after-impact row keeps {H['hard_impactor']['cai_retention'] * 100:.0f}% (202/385 MPa at 50 J, 5 mm).")
    a(f"- **Quasi-static stress (051's method, extended as a power of the wall; PROJECTION).** The strike adds "
      f"{hk['hail_surface_stress_MPa']:.0f} MPa of surface stress at the pitch layup's stiffness wall, and "
      f"{hm['hail_surface_stress_MPa']:.0f} MPa at M55J 50/20/20/10's. At M55J 50/20/20/10's wall the mean strength left after "
      f"the operating load is only {hm['screen_left_after_operating_MPa']:.0f} MPa, so a strike exceeds it "
      f"{hm['hail_over_left']:.1f} times over. At {NICE[fr]}'s Pf 1e-3 wall it takes {hfr['hail_over_left'] * 100:.0f}% of the "
      f"{hfr['screen_left_after_operating_MPa']:.0f} MPa left.")
    a("- **Not sourced:** ice on pitch-fibre laminates, ice on tubes, walls below 1.5 mm, and members under compressive preload.")
    a("")
    a("## 4. What the light frame must carry to float")
    a("")
    a(f"{NICE['K13D2U-50-20-20-10']}, ISA, 052's endpoints. The largest wall factor that still floats, and the compression it "
      "then needs:")
    a("")
    a("| R, m | Service | Payload at stiffness wall, kg | Max wall factor | Laminate mean, GPa | UD 0 deg at mean, GPa | "
      "UD for Pf 1e-3, CV 5.2 / 6%, GPa | Same, size-scaled, GPa | Whole-tube scale at m 20, GPa |")
    a("|---|---|---|---|---|---|---|---|---|")
    for R in RADII:
        for sv in ("ground", "one_day", "seven_day"):
            x = need[(R, "ISA", sv)]
            a(f"| {R} | {sv.replace('_', ' ')} | {kg(x['payload_at_witness_kg'])} | {x['max_wall_factor']:.3f} | "
              f"{x['laminate_mean_needed_GPa']:.3f} | {x['Xc_needed_mean_MPa'] / 1000:.3f} | "
              f"{x['Xc_needed_Pf1e3_cv5.2_MPa'] / 1000:.2f} / {x['Xc_needed_Pf1e3_cv6_MPa'] / 1000:.2f} | "
              f"{x['Xc_needed_Pf1e3_cv5.2_size_MPa'] / 1000:.2f} / {x['Xc_needed_Pf1e3_cv6_size_MPa'] / 1000:.2f} | "
              f"{x['member_scale_needed_cv6_GPa']:.3f} |")
    a("")
    a(f"Sourced K13D2U is {k13['Xc_MPa']:.0f} MPa. So the requirement is about three times the data at mean, and five to nine "
      "times for the reliability target.")
    a("")
    a("## Method and limits")
    a("")
    a(f"- **Witnesses:** 051's 019-reserve witnesses, because 052 resizes that family. The 5%-reserve "
      f"K13D2U 50/20/20/10 witness has {(w5 / k13['witness_tubes_kg'] - 1) * 100:.1f}% more tube mass ({w5:,.1f} against "
      f"{k13['witness_tubes_kg']:,.1f} kg).")
    a("- **Wall scaling (PROJECTION):** walls thicken uniformly at fixed radius. Peak stress goes as 1/wall and mass as wall. "
      "Thicker walls also cut Euler amplification, so this is conservative. 051's FE was not re-run.")
    a("- **First-ply failure:** the 0 deg ply's failure is taken as the laminate's (PROJECTION). No laminate data test it.")
    a("- **Not explored:** film and joint redesign, hybrid layups (PAN 0 deg plies over pitch), and other tube radii.")
    a("")
    a("## Checks")
    a("")
    a(f"- **Lift:** taken as 052's card payload plus its bill, it scales exactly as R^3 ({lift_k:.5f} R^3 kg in both "
      f"weathers). It matches 054's own lift column at R 10-15 within {lift_d * 1000:.1f} g.")
    a(f"- **Cavity:** 054's one- and seven-day increments equal its barrier change plus its capture hardware within "
      f"{cav_d * 1000:.1f} g at R 10-15, and no other line moves. The capture fit reproduces R 12 within {fit12 * 100:.1f}%.")
    a("- Every sourced value is asserted against its row (sources_used in CARBON.json and EXTRA.json).")
    a(f"- The Pf-sized walls give Pf = 1.000e-3 when recomputed, with and without size scaling.")
    a("- No sized carbon row floats; the script asserts it.")
    a("")
    a("## Reproduce")
    a("")
    a("In the outputs folder, run `python3 carbon60.py`, then `python3 extra60.py`, then `python3 card60.py`. Each runs in under "
      "two seconds on one core.")
    a("")
    a("## Then")
    a("")
    a("Stop and file. The robotics seat sends the next job. NFI.json carries the open rows.")
    text = "\n".join(L) + "\n"
    with open(os.path.join(HERE, "CARD.md.tmp"), "w") as fh:
        fh.write(text)
    os.replace(os.path.join(HERE, "CARD.md.tmp"), os.path.join(HERE, "CARD.md"))

    for cid in CONS:
        for lab in ("cv5.2", "cv6"):
            assert abs(rel[(cid, lab, "Pf1e-3")]["Pf_coupon_scale_as_member"] - 1e-3) < 1e-6 or CONS[cid][f"f_rel_{lab}"] == 1.0
            assert abs(rel[(cid, lab, "Pf1e-3_size")]["Pf_size_scaled"] - 1e-3) < 1e-6 or CONS[cid][f"f_rel_size_{lab}"] == 1.0
    for R in RADII:
        for w in ("ISA", "optimistic"):
            assert abs(sic(R, w)["payload_kg"] - sic(R, w)["card_payload_kg"]) < 1e-3

    now = datetime.datetime.now().astimezone().isoformat()
    results = {"schema": 1, "card": "MAINLINE-060", "unit": "vacuum-mainline060-p3-carbon-frame-1020", "order": ORDER, "replaces": FIRST,
               "status": "ESTIMATE", "tag": "QUESTIONABLE / PROJECTION", "certification": "none",
               "job_started_at": JOB_STARTED, "job_ended_at": now, "times_are": "measurements only",
               "answer": {"floats_on_sourced_compression": False, "best_at_mean": best["mean"], "best_supported_Pf1e3": fr,
                          "best_supported_Pf1e3_size": best["Pf1e-3_cv6_size"],
                          "payload_kg_ISA_endpoints_ground": {s: {R: acc(best[s], R, s)["payload_kg"] for R in RADII} for s in best},
                          "K13D2U_50_laminate_mean_GPa": k13["laminate_screen_GPa"], "times_below_2p16": gap["times_mean"],
                          "K13D2U_50_needed_to_float": X["to_float"], "better_lead_than_SiC": False,
                          "joints_first_float_R_with_Boeing_share": first_b44,
                          "hail": {"design_energy_J": H["design"]["energy_J"], "flat_panel_FTE_1p59mm_J": fte159,
                                   "margin_at_1p45mm": hk["energy_margin_rho910"]},
                          "test": "axial compression to failure of ~30 full-length wrapped K13D2U 50/20/20/10 tubes with end fittings"},
               "constructions": C["constructions"], "sic_reference": C["sic_reference"], "cavity": C["cavity"],
               "reliability": X["reliability"], "hail": X["hail"], "joints": {k: v for k, v in J.items() if k != "rows"}}
    with open(os.path.join(HERE, "RESULTS.json.tmp"), "w") as fh:
        json.dump(results, fh, indent=1, default=str)
    os.replace(os.path.join(HERE, "RESULTS.json.tmp"), os.path.join(HERE, "RESULTS.json"))
    items = [
        ("NFI-060-TUBE-COMPRESSION", "QUESTIONABLE", "No compression data exist for wrapped K13D2U-class tubes or for any pitch or M-series "
         "multidirectional laminate. The laminate value is the data-sheet UD strength over 051's 0 deg ply ratio.",
         "Axial compression of a population of full-length wrapped tubes with fittings; a flat-laminate coupon first."),
        ("NFI-060-SCATTER", "PROJECTION", "The Weibull modulus is m = 1.2/CV from coupon CVs of 5.1% (n=6, pitch K63712) and 5.2% (an NCAMP IM fibre), "
         "plus CMH-17's 6% floor. No pitch tube scatter exists.", "The same tube population, fitted for m."),
        ("NFI-060-SIZE", "PROJECTION", "Size scaling moves a 0.32 cm3 compression gauge to one tube's volume. 052 used 1 cm3 for SiC, which "
         "differs by about 6% at m 20. Whether fibre-composite compression follows volume scaling is not established.",
         "Tube and coupon strengths of the same laminate."),
        ("NFI-060-WALL-SCALING", "PROJECTION", "Walls thicken uniformly at fixed radius, with peak stress as 1/wall. 051's FE is not re-run at "
         "the thickened walls, and the hail stress power fit (wall exponent -1.13 to -1.30) is carried from 051's 0.98-3.6 mm walls to as much as 17 mm.",
         "Re-run 051's frame FE and hail model at the sized walls."),
        ("NFI-060-FIRST-PLY", "PROJECTION", "The 0 deg ply's first failure is taken as the laminate's compressive failure, using 051's "
         "lamination ratios for virtual laminates.", "Laminate compression of the actual layup."),
        ("NFI-060-JOINTS", "QUESTIONABLE", "052's SiC sleeve, bond and node bill is kept. Sourced strut fitting shares (17-70% of the strut) "
         "would add 0.2-2.3 times the tube mass. The peak member load, 775 kN, exceeds the largest sourced composite strut test "
         "(121.7 klb, 541 kN). Bonded fittings failed at about 70% of design ultimate.", "A bonded end-fitting test at 775 kN on a 247 mm, 1.45 mm-wall tube."),
        ("NFI-060-FILM", "QUESTIONABLE", "052's PBO film and barrier lines are carried unchanged. Attaching the film to carbon tubes, and the "
         "thermal mismatch between near-zero-CTE pitch tubes and the film, are not addressed.", "A film-to-tube attachment design."),
        ("NFI-060-MOISTURE", "QUESTIONABLE", "Epoxy-matrix tubes inside the evacuated cavity hold absorbed water. 054's capture, sized for a "
         "SiC frame, does not carry it, and no uptake was sourced here.", "Moisture uptake and outgassing of the laminate in vacuum."),
        ("NFI-060-CAVITY-EXTRAPOLATION", "PROJECTION", "054's cavity rows cover R 10-15. R 20 and 30 extrapolate the barrier as R^2 and the "
         "capture as a + bR^2 (R 12 reproduced within 0.5%).", "054's model run at R 20 and 30."),
        ("NFI-060-HAIL", "QUESTIONABLE", "Ice thresholds are for flat quasi-isotropic PAN panels, 1.59-6 mm thick (the T800 table is an interim "
         "2010 snapshot). There are none for tubes, pitch fibres, walls under 1.5 mm or preloaded members. Tube data are hard-impactor "
         "only. The 52% CAI retention is a single row.", "Ice-gun strikes on preloaded full-size tubes of the chosen layup."),
        ("NFI-060-T700S", "QUESTIONABLE", "T700S strength is 051's Toray value (1.45 GPa), not re-sourced. T700S frames are "
         "stiffness-limited, so the answer does not depend on it.", "The data sheet."),
        ("NFI-060-UNEXPLORED", "PROJECTION", "Hybrid layups (PAN 0 deg plies over pitch), other ply angles, tube radii and frame "
         "geometries are not explored. The frame is 051's and 052's fixed family.", "A layup and geometry search on the same account."),
    ]
    nfi = {"schema": 1, "card": "MAINLINE-060", "unit": "vacuum-mainline060-p3-carbon-frame-1020", "tag": "QUESTIONABLE", "status": "OPEN",
           "items": [{"id": i, "tag": t, "claim": c, "needed_to_ground": n} for i, t, c, n in items]}
    with open(os.path.join(HERE, "NFI.json.tmp"), "w") as fh:
        json.dump(nfi, fh, indent=1)
    os.replace(os.path.join(HERE, "NFI.json.tmp"), os.path.join(HERE, "NFI.json"))

    def pin(p, role):
        data = open(p, "rb").read()
        return {"path": p, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "role": role}
    B = "unpublished-local-ref:792ada9d1fcd5e54"
    Q = "unpublished-local-ref:ab52dba26d6cc3a7"
    pins = [pin(f"{B}/CARD-060-P3-CARBON-FRAME.md", "brief"), pin(f"{B}/COMMON.md", "brief"), pin(f"{Q}/{ORDER}.json", "order"),
            pin(f"{Q}/{FIRST}.json", "order (replaced)")]
    for rid, names in ((R051, ("MATERIAL-MODELS.json", "WITNESSES.json", "GAPS.json", "HAIL-DESIGN.csv", "CARD.md")),
                       (R052, ("MASS-ACCOUNT.csv", "CARD.md")), (R054, ("MASS-ACCOUNT.csv", "CARD.md"))):
        pins.append(pin(f"{Q}/{rid}.json", "source report"))
        for n in names:
            pins.append(pin(art(rid, n), f"{rid} {n}"))
    for n in ("compression", "joints", "impact"):
        for e in ("json", "md"):
            pins.append(pin(f"{SRC}/{n}.{e}", "sourcing file"))
    for n in ("carbon60.py", "extra60.py", "src60.py", "card60.py", "CARBON.json", "EXTRA.json"):
        pins.append(pin(os.path.join(HERE, n), "this card's own code or intermediate"))
    inputs = {"schema": 1, "card": "MAINLINE-060", "unit": "vacuum-mainline060-p3-carbon-frame-1020", "pins": pins,
              "sources_used": {**C["sources_used"], **X["sources_used"]}}
    with open(os.path.join(HERE, "INPUTS.json.tmp"), "w") as fh:
        json.dump(inputs, fh, indent=1)
    os.replace(os.path.join(HERE, "INPUTS.json.tmp"), os.path.join(HERE, "INPUTS.json"))
    print(len(text), "bytes card;", len(items), "NFI;", len(pins), "pins; best", best, "first float with Boeing share R", first_b44)


if __name__ == "__main__":
    main()
