#!/usr/bin/env python3
"""R3-I009 v2 — a routed cord assembly and its anchor compliance, carrying
the consolidated 2026-10-14 review findings.

Prices ONE concrete physical arrangement for the R3-I005 SF1.0 winner
(d60 + d180/11) on the 155-anchor ring and 137 kept bay planes, and its
anchor/standoff load path. Two candidate arrangements are enumerated and
priced; the surviving one is carried to a full before/after budget.

v1 (commit 914bab52) priced the v2 R3-I005 winner under the scalar
eleven-mode pass; the consolidated review disproved that pass (finding 1:
it is a phase AVERAGE; the demonstrated finite topology fails it), and
corrected the crossing counts (finding 2) and the ledger marginal costs
(finding 3). v2 re-prices on the CORRECTED R3-I005 record (v3 winner,
heavier: 2,207.3 t) and records the finite-phase verdict of the ACTUAL
arrangement honestly: the scalar pass does not establish feasibility, the
weakest-orientation margin passes by ppm, and the mixed-mode trial verdict
under the review's convention is UNKNOWN on this point. The v1 closure
claim (+80.0 t SL, "margins >= 1.0") is WITHDRAWN; v1 is preserved as the
historical record of the superseded attempt.

Option A (two-depth co-planar): both families in every kept plane, each at
its own axial depth maintained by a standoff post at every anchor point.
Priced honestly: the post is a cantilever IN SERIES with the cord
foundation, and the winner's binding-mode margin tolerates almost no
series loss — so the post stiffness requirement, not the post mass guess,
decides it.

Option B (alternating planes): the two families occupy DISJOINT bay planes
(d60 even-index, d180/11 odd-index of the kept list). No co-planar
families, no standoff hardware, zero between-family interaction; the
family's total licensed section concentrates in the planes it occupies
(per-cord section x137/n_occ). For GLOBAL circumferential modes every
occupied plane contributes the same anchor phase sums, so the
finite-endpoint orientation matrix of the arrangement equals the
underlying winner's (the 2-bay axial modulation bound is recorded
separately).

v2.1 (this revision) carries the first-review corrections, each
reproduced from the review before correcting (asserts pin the parity):
the first-slack threshold now comes from the SHORTEST occupied-plane
cord at its own worst mode (w = 0.0141 m, not the mean-cord 0.080 m);
the declared-lug COMPLIANT state is evaluated on the binding orientation
margin and FAILS it (0.999345419 at n=5 vs the rigid baseline
1.000003659, which passes by 3.7 ppm); the per-plane radial preload
counts BOTH cord ends (156 endpoints) and is compared against the
physical pressure demand without the KD capacity knockdown (2.57% /
7.65%). No redesign: the compliant-state failure is recorded, priced as
a bounded recovery scenario, and left to the coupled finite-endpoint
unit that owns the change.

Everything below is bounded arithmetic on the frozen model + the
CORRECTED R3-I005 record. No broad search, no solver, no FEA.
Deterministic: writes routing.json byte-identically on a second run (no
timestamps inside).
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "R3-I004"))
sys.path.insert(0, os.path.join(HERE, "..", "R3-I005"))

from net import planes_of            # noqa: E402  (R3-I004 record)
import alloc as I005                 # noqa: E402  (R3-I005 record)

SHIP0 = I005.SHIP0
P_ATM, KD = I005.P_ATM, I005.KD
CLIP_KG = 0.05                       # per interior crossing (I004/I005 basis)
RHO_SPOKE = SHIP0["rhoSpoke"]        # 970 kg/m3 (model cord lam basis)
E_SPOKE = SHIP0["eSpoke"]            # 70 GPa
N_LONG = 155
HALF = N_LONG // 2                   # 77 -> cords m = 0..77 per plane

# Declared component assumptions (public-spec absent; sensitivity carried)
LUG_KG = 0.35                        # swaged termination per cord END
LUG_LA_M = 0.15                      # compliant length per end, cord-equiv
ASSEMBLY = 0.05                      # assembly allowance on cord hardware
EPS_PRETENSION = 0.002               # declared pretension strain (0.2%)
G = 9.81
POST_LEN_M = 0.30                    # option-A standoff post length
E_STEEL = 200e9
ANCHOR_5PCT_LA = 2.1237              # I004 anchor sensitivity, per end

# The no-buyback budget is computed at the winner's BINDING mode (the v3
# R3-I005 winner binds at n=5, margin 1.0008): the margin tolerates a total
# foundation stiffness loss of exactly (margin-1) scaled by q/q_found.


def kept_planes(w):
    kept = [r for r in planes_of(w.g) if r >= 6.0]
    assert len(kept) == 137, len(kept)
    return kept


def family_geometry(name, step, off_deg, planes, kept=None):
    """Endpoint topology + geometry for one family over given planes."""
    phi = 2.0 * math.pi * step / N_LONG
    sub = math.degrees(phi)
    used = HALF + 1 + step            # anchors [0, 77+step]
    doubled = HALF + 1 - step         # anchors in [step, 77] carry 2 ends
    unused = N_LONG - used
    # Interior crossings per plane (consolidated review finding 2): cords
    # (a, a+step) and (b, b+step), a < b, cross iff b < a+step — a shared
    # endpoint is not a crossing; no wraparound (a+step <= 154).
    crossings_pp = sum(min(HALF - a, step - 1) for a in range(HALF))
    lens = [2.0 * r * math.sin(phi / 2.0) for r in planes]
    total_len = sum(lens) * (HALF + 1)
    off_rad = math.radians(off_deg)
    spacing = lambda r: (r * math.sin(off_rad / 2.0)
                         * (2.0 * math.pi / N_LONG) * 1000.0)
    return dict(
        name=name, step=step, offsetDeg=off_deg, subtendDeg=sub,
        planes=len(planes), cords=len(planes) * (HALF + 1),
        ends=2 * len(planes) * (HALF + 1),
        anchorMin=0, anchorMax=HALF + step, anchorsUsed=used,
        doubledAnchorsPP=doubled, unusedAnchors=unused,
        crossingsPP=crossings_pp, crossings=crossings_pp * len(planes),
        totalLenM=total_len, meanCordM=total_len / (len(planes) * (HALF + 1)),
        minCordM=min(lens), maxCordM=max(lens),
        sinHalf=math.sin(phi / 2.0), cosHalf=math.cos(phi / 2.0),
        missMinM=min(planes) * math.sin(off_rad / 2.0),
        missMaxM=max(planes) * math.sin(off_rad / 2.0),
        # within-family chord-midpoint spacing on the miss circle — at the
        # family's own smallest OCCUPIED plane, and (kept given) at the
        # smallest retained plane of the whole hull, occupancy aside
        spacingMinMm=spacing(min(planes)),
        spacingMaxMm=spacing(max(planes)),
        spacingAtSmallestKeptMm=spacing(min(kept)) if kept else None,
        spacingAtBarrelMm=spacing(max(kept)) if kept else None,
    )


def cord_section(a_family, area_m2, n_occ):
    """Per-cord section: family's licensed total section over its cords."""
    return a_family * area_m2 / (n_occ * (HALF + 1))


def diameter(section):
    return 2.0 * math.sqrt(section / math.pi)


def main():
    w = I005.World(1.0)                       # the frozen SF1.0 world
    alloc_rec = json.load(open(os.path.join(HERE, "..", "R3-I005",
                                            "alloc.json")))
    win = alloc_rec["worlds"]["sf1.0"]["bestFeasible"]
    win_a = win["point"]["alloc"]
    area_m2 = w.g["areaM2"]
    kept = kept_planes(w)
    r_min, r_max = min(kept), max(kept)

    # ---- winner reproduction parity (imports carry the corrections) -----
    p = w.point(win_a)
    assert abs(p["totalT"] - win["totalT"]) < 1e-6
    assert abs(p["marginSLT"] - win["marginSLT"]) < 1e-6
    mm0 = w.mode_margins(win_a)
    n_bind = min(mm0, key=lambda k: mm0[k])
    assert int(n_bind) == win["critN"], (n_bind, win["critN"])
    assert abs(mm0[n_bind] - min(win["modeMargins"].values())) < 5e-5, mm0
    finite_phase = win["finitePhase"]

    # ---- arrangement B geometry ----------------------------------------
    planes_even, planes_odd = kept[0::2], kept[1::2]   # 69 / 68
    d60 = family_geometry("d60", 52, 59.226, planes_even, kept)
    d11 = family_geometry("d180/11", 70, 17.419, planes_odd, kept)
    f_all60 = family_geometry("d60", 52, 59.226, kept)     # all-137 spacing
    f_all11 = family_geometry("d180/11", 70, 17.419, kept)
    # parity with the R3-I005 family record (all-137-plane topology)
    rec = {f["name"]: f for f in alloc_rec["world"]["families"]}
    assert f_all60["doubledAnchorsPP"] == rec["d60"]["doubledAnchorsPerPlane"]
    assert f_all60["crossingsPP"] == rec["d60"]["interiorCrossingsPerPlane"]
    assert f_all60["crossings"] == rec["d60"]["crossings"]
    assert f_all11["crossings"] == rec["d180/11"]["crossings"]
    for f, a_key in ((d60, "a_d60"), (d11, "a_d180/11")):
        f["sectionM2"] = cord_section(win_a[a_key], area_m2, f["planes"])
        f["diaMm"] = diameter(f["sectionM2"]) * 1000.0
        f["bareT"] = f["totalLenM"] * f["sectionM2"] * RHO_SPOKE / 1000.0
        f["clipT"] = f["crossings"] * CLIP_KG / 1000.0
        f["lugT"] = f["ends"] * LUG_KG / 1000.0
        # clearance proof: midpoint spacing vs cord diameter, both at the
        # family's smallest occupied plane and at the smallest retained
        # plane of the hull (occupancy aside — the binding case)
        f["clearanceMm"] = f["spacingMinMm"] - f["diaMm"]
        f["clearanceAtSmallestKeptMm"] = (f["spacingAtSmallestKeptMm"]
                                          - f["diaMm"])
        assert f["clearanceMm"] > 0.0
        assert f["clearanceAtSmallestKeptMm"] > 0.0
        # sag at declared pretension vs the 2-bay plane gap
        t0 = E_SPOKE * f["sectionM2"] * EPS_PRETENSION
        f["pretensionKN"] = t0 / 1000.0
        wl = f["sectionM2"] * RHO_SPOKE * G
        f["sagM"] = wl * f["maxCordM"] ** 2 / (8.0 * t0)
        f["planeGapClearanceM"] = SHIP0["bayM"] - 2.0 * f["sagM"]
        assert f["planeGapClearanceM"] > 0.5

    # cord-mass conservation vs the I005 smear (occupied-mean vs all-mean)
    i005_spokes = w.spokes_t(win_a)          # cord x1.3 + clips at 137 planes
    f_all11 = family_geometry("d180/11", 70, 17.419, kept)
    i005_cord_t = sum(
        win_a[k] * area_m2 * fm["meanCordM"] * RHO_SPOKE / 1000.0
        for k, fm in (("a_d60", f_all60), ("a_d180/11", f_all11)))
    b_cord_t = d60["bareT"] + d11["bareT"]

    # ---- BOM (option B) --------------------------------------------------
    lugs_t = d60["lugT"] + d11["lugT"]
    clips_t = d60["clipT"] + d11["clipT"]
    b_hardware_t = b_cord_t + lugs_t + clips_t
    b_spokes_t = b_hardware_t * (1.0 + ASSEMBLY)
    delta_spokes_t = b_spokes_t - i005_spokes

    # ---- forces per anchor ---------------------------------------------
    forces = {}
    for f in (d60, d11):
        phi_half = math.pi * f["step"] / N_LONG
        # first-slack basis (first review, finding 2): the SHORTEST cord of
        # the family — its smallest OCCUPIED plane — at the worst mode for
        # THAT cord (antinode at its midpoint: strain/w =
        # 2 sin(phi/2)|cos(n phi/2)| / L_min). The family-mean figure is
        # kept labeled for the stiffness-tension number only; it
        # understates the slack strain ~5.7x here.
        sw = max(((2.0 * f["sinHalf"] * abs(math.cos(n * phi_half))
                   / f["minCordM"], n) for n in range(2, 13)))
        # unit-tension components at an anchor (radial inward, tangential)
        forces[f["name"]] = dict(
            radialShare=f["sinHalf"], tangentialShare=f["cosHalf"],
            axialShare=0.0,
            # mean-cord strain per unit modal amplitude (antinode, |cos|=1);
            # superseded for SLACK by strainPerWShortestCord below
            strainPerWMeanBasis=f["sinHalf"] * 2.0 / f["meanCordM"],
            # first-slack basis: shortest cord, worst mode, |cos| included
            strainPerWShortestCord=sw[0], slackWorstModeN=sw[1],
            minCordM=f["minCordM"],
            # per-cord tension per unit modal amplitude (stiffness tension)
            kNperW=E_SPOKE * f["sectionM2"] * f["sinHalf"] * 2.0
            / f["meanCordM"] / 1000.0,
            # radial pretension load per occupied plane: BOTH ends of all
            # 78 cords pull their anchor inward — 156 endpoints (first
            # review, finding 4; v2 counted one end)
            planePretensionRadialKN=2.0 * (HALF + 1) * f["pretensionKN"]
            * f["sinHalf"],
        )
    # plane pressure demand: the PHYSICAL load P 2 pi R bay (first review,
    # finding 4: KD is a capacity knockdown on the stiffness side, not a
    # load reduction — v2 applied it to the demand)
    pressure_load_kn = P_ATM * 2.0 * math.pi * w.g["R"] * SHIP0["bayM"] \
        / 1000.0
    pressure_load_kd_kn = P_ATM * KD * 2.0 * math.pi * w.g["R"] \
        * SHIP0["bayM"] / 1000.0
    for f in (d60, d11):
        forces[f["name"]]["pretensionVsPressurePct"] = round(
            forces[f["name"]]["planePretensionRadialKN"]
            / pressure_load_kn * 100.0, 2)
    # sign-reversal (slack) thresholds on the shortest-cord worst-mode
    # basis: eps0 needed to stay taut at modal amplitude w
    worst_strain = max(forces[f["name"]]["strainPerWShortestCord"]
                       for f in (d60, d11))
    fam_worst = max((d60, d11), key=lambda ff: forces[ff["name"]][
        "strainPerWShortestCord"])
    n_slack_worst = forces[fam_worst["name"]]["slackWorstModeN"]
    w_slack = EPS_PRETENSION / worst_strain
    slack = {str(wm): round(worst_strain * wm * 100.0, 3)
             for wm in (0.02, 0.05, 0.10)}
    slack["wSlackAtDeclaredPretensionM"] = round(w_slack, 6)
    slack["basis"] = ("shortest occupied-plane cord at its own worst mode "
                      "(single-mode antinode bound); amplitudes above "
                      "wSlackAtDeclaredPretensionM leave that cord slack "
                      "— mixed-mode phase combinations and post-slack "
                      "redistribution are outside this bound (carried to "
                      "the coupled finite-endpoint unit)")
    # parity with the first-review counterexamples, reproduced before
    # correcting: first slack 0.0141052 m; both-ends preload 1835.2 /
    # 5453.5 kN against the 71,304 kN physical demand (2.57% / 7.65%)
    assert abs(w_slack - 0.0141052) < 1e-6, w_slack
    assert abs(forces["d60"]["planePretensionRadialKN"] - 1835.2) < 0.1
    assert abs(forces["d180/11"]["planePretensionRadialKN"] - 5453.5) < 0.1
    assert abs(pressure_load_kn - 71304.1) < 0.1

    # ---- option A: two-depth co-planar, priced and rejected -------------
    # Every anchor point hosting a family needs a depth post:
    post_count = (HALF + 1 + 52) * 137 + (HALF + 1 + 70) * 137
    # binding-mode no-buyback loss budget on the FOUNDATION:
    nb = int(n_bind)
    nn = nb * nb - 1.0
    g = w.g
    a_o = w.a_o0
    abar = a_o * (win_a["a_i"] / w.bay) / (a_o + win_a["a_i"] / w.bay)
    i_eff = abar * w.depth ** 2
    q_crimp = (2.0 * w.E * win_a["a_th"] * w.depth * w.cos_th ** 2
               / (w.bay * w.theta_len)) / g["R"]
    q_ring_b = 1.0 / (1.0 / (nn * w.E * i_eff / g["R"] ** 3)
                      + 1.0 / q_crimp)
    q_found_b = sum(E_SPOKE * win_a[f"a_{f['name']}"] * f["f"][nb] / nn
                    for f in w.fam if win_a.get(f"a_{f['name']}", 0.0) > 0.0)
    q_total_b = q_ring_b + q_found_b
    demand_b = P_ATM * w.sf / KD
    assert abs(q_total_b / demand_b - mm0[n_bind]) < 2e-4   # matches record
    loss_budget = (q_total_b / demand_b - 1.0) * q_total_b / q_found_b
    # post series compliance: 2.La/L <= loss_budget  ->  La_max
    la_post_max = loss_budget * f_all60["meanCordM"] / 2.0
    ea60 = E_SPOKE * cord_section(win_a["a_d60"], area_m2, 137)
    k_post_min = ea60 / max(la_post_max, 1e-9)
    i_post = k_post_min * POST_LEN_M ** 3 / (3.0 * E_STEEL)
    d_post = (64.0 * i_post / math.pi) ** 0.25
    m_post = math.pi * (d_post / 2.0) ** 2 * POST_LEN_M * 7850.0
    # at the 5%-loss point instead (buyback path):
    k_post_5pct = ea60 / (ANCHOR_5PCT_LA / 2.0)
    i_post5 = k_post_5pct * POST_LEN_M ** 3 / (3.0 * E_STEEL)
    d_post5 = (64.0 * i_post5 / math.pi) ** 0.25
    m_post5 = math.pi * (d_post5 / 2.0) ** 2 * POST_LEN_M * 7850.0
    option_a = dict(
        arrangement="both families in every kept plane, axial depths "
                    "plane +/- 0.30 m held by a standoff post per anchor "
                    "point per family",
        bindingMode=nb,
        postCount=post_count,
        betweenFamilyCrossings=137 * (HALF + 1) ** 2,   # projection pass-bys
        betweenFamilyConnectors=0,                      # separated depth
        withinFamilyCrossings=d60["crossingsPP"] * 137
        + d11["crossingsPP"] * 137,
        seriesLossBudgetPct=round(loss_budget * 100.0, 3),
        postStiffnessNeededMNperM=round(k_post_min / 1e6, 2),
        postDiaMm=round(d_post * 1000.0, 1),
        postMassT=round(post_count * m_post / 1000.0, 1),
        postMassTat5pct=round(post_count * m_post5 / 1000.0, 1),
        postBudgetNote="post sized to HALF the I004 5%-point compliance "
                       "(1.06 m/end) — the anchor zone would need the rest",
        verdict=f"REJECTED — holding the no-buyback line at the binding "
                f"mode n={nb} requires a {k_post_min / 1e6:.0f} MN/m post "
                f"({d_post * 1000.0:.0f} mm solid steel, ~"
                f"{post_count * m_post / 1000.0:.0f} t); even spending the "
                "whole I004 5% compliance point on posts alone costs ~"
                f"{post_count * m_post5 / 1000.0:.0f} t against a "
                f"+{win['marginSLT']:.1f} t allowance, and mode {nb} then "
                "still needs ring buyback.",
    )

    # ---- series compliance (option B) and ring buyback ------------------
    def margins_with_la(la_per_end):
        a2 = dict(win_a)
        for f, key in ((d60, "a_d60"), (d11, "a_d180/11")):
            eta = f["meanCordM"] / (f["meanCordM"] + 2.0 * la_per_end)
            a2[key] = win_a[key] * eta
        return w.mode_margins(a2), a2

    def buyback(la_per_end):
        """Grow a_i until min mode margin restored to >= 1.0; return delta."""
        mm, a2 = margins_with_la(la_per_end)
        lo, base_ai = 0.0, win_a["a_i"]
        if min(mm.values()) >= 1.0:
            return 0.0, mm
        hi = base_ai
        for _ in range(200):
            hi *= 1.05
            a3 = dict(a2)
            a3["a_i"] = hi
            if min(w.mode_margins(a3).values()) >= 1.0:
                break
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            a3 = dict(a2)
            a3["a_i"] = base_ai + mid
            if min(w.mode_margins(a3).values()) >= 1.0:
                hi = mid
            else:
                lo = mid
        d_ai = hi
        d_t = d_ai * w.kg_inner / 1000.0 * (1.0 + w.adder) / w.eta
        a3 = dict(a2)
        a3["a_i"] = base_ai + d_ai
        return d_t, w.mode_margins(a3)

    compliance = {}
    for label, la in (("declared lug only", LUG_LA_M),
                      ("lug + anchor-zone 5% point", LUG_LA_M
                       + ANCHOR_5PCT_LA)):
        d_t, mm = buyback(la)
        eta60 = d60["meanCordM"] / (d60["meanCordM"] + 2.0 * la)
        compliance[label] = dict(
            laPerEndM=la, foundationLossPct=round((1.0 - eta60) * 100.0, 2),
            marginsAfter=mm, buybackInnerRingsT=round(d_t, 2))

    # ---- declared-lug orientation state (first review, finding 3) -------
    # The COMPLIANT as-declared state (eta per family on the foundation,
    # the same convention as margins_with_la) evaluated on the orientation
    # margin — computed here, not asserted from the review; parity asserts
    # pin both the rigid baseline against the record and the post-lug
    # value against the review's published counterexample.
    def orientation_margins(a_dict):
        """Per-mode weakest-orientation margins: ring series + 2x2 min."""
        a_o = w.a_o0 + a_dict["a_oe"]
        abar = a_o * (a_dict["a_i"] / w.bay) / (a_o + a_dict["a_i"] / w.bay)
        i_eff = abar * w.depth ** 2
        q_c = (2.0 * w.E * a_dict["a_th"] * w.depth * w.cos_th ** 2
               / (w.bay * w.theta_len)) / w.g["R"]
        out_m = {}
        for n in range(2, 13):
            qr = 1.0 / (1.0 / ((n * n - 1.0) * w.E * i_eff / w.g["R"] ** 3)
                        + 1.0 / q_c)
            _, lam = w.orientation_phase(a_dict, n)
            out_m[n] = (qr + lam) * KD / P_ATM
        return out_m

    om_rigid = orientation_margins(win_a)
    n_rigid = min(om_rigid, key=lambda k: om_rigid[k])
    # rigid parity with the R3-I005 record's own finitePhase block
    assert n_rigid == finite_phase["bindingModeFinite"], (n_rigid,)
    assert abs(om_rigid[n_rigid]
               - finite_phase["marginWeakestOrientation"]) < 1e-8
    mm_lug, a_lug = margins_with_la(LUG_LA_M)
    om_lug = orientation_margins(a_lug)
    n_lug = min(om_lug, key=lambda k: om_lug[k])
    # parity with the review's demonstrated counterexample
    assert abs(om_lug[5] - 0.999345419) < 1e-8, om_lug[5]
    # bounded scenario (no redesign): inner-ring growth that restores the
    # post-lug orientation margin to >= 1.0
    lo_r, hi_r = win_a["a_i"], win_a["a_i"]
    for _ in range(200):
        hi_r *= 1.05
        a_r = dict(a_lug)
        a_r["a_i"] = hi_r
        if min(orientation_margins(a_r).values()) >= 1.0:
            break
    for _ in range(80):
        mid_r = 0.5 * (lo_r + hi_r)
        a_r = dict(a_lug)
        a_r["a_i"] = mid_r
        if min(orientation_margins(a_r).values()) >= 1.0:
            hi_r = mid_r
        else:
            lo_r = mid_r
    orient_recover_t = ((hi_r - win_a["a_i"]) * w.kg_inner / 1000.0
                        * (1.0 + w.adder) / w.eta)
    post_lug = dict(
        basis="compliant as-declared state: eta = meanCordM/"
              "(meanCordM + 2*0.15) per family on a_d60/a_d180/11 "
              "(this unit's own compliance convention)",
        rigidBaselineMargin=om_rigid[n_rigid], rigidBaselineModeN=n_rigid,
        postLugOrientationMargin=om_lug[n_lug], postLugModeN=n_lug,
        scalarMinAfterLug=min(mm_lug.values()),
        orientationRecoveryInnerRingsT=round(orient_recover_t, 2),
        verdict="FAIL vs 1.0 in the compliant as-declared state (the "
                "rigid baseline passes by 3.7 ppm); scalar phase-average "
                "margins stay >= 1.0 after the 0.00 t buyback — recorded, "
                "priced as a bounded recovery scenario, not fixed here")
    compliance["declared lug only"]["orientationState"] = post_lug

    # ---- budgets before/after -------------------------------------------
    sf10_before = dict(totalT=round(win["totalT"], 1),
                       marginSLT=round(win["marginSLT"], 1),
                       margin2500T=round(win["margin2500T"], 1),
                       spokesLineT=round(i005_spokes, 1))
    b_total = win["totalT"] + delta_spokes_t
    buy_lug = compliance["declared lug only"]["buybackInnerRingsT"]
    buy_5pct = compliance["lug + anchor-zone 5% point"]["buybackInnerRingsT"]
    sf10_after = dict(
        totalT=round(b_total + buy_lug, 1),
        marginSLT=round(win["marginSLT"] - delta_spokes_t - buy_lug, 1),
        margin2500T=round(win["margin2500T"] - delta_spokes_t - buy_lug, 1),
        spokesLineT=round(b_spokes_t, 1),
        deltaSpokesT=round(delta_spokes_t, 1),
        cordT=round(b_cord_t, 1), terminationsT=round(lugs_t, 1),
        clipsT=round(clips_t, 1), assemblyT=round(
            b_hardware_t * ASSEMBLY, 1),
        complianceBuybackT_lugOnly=round(buy_lug, 2),
        complianceBuybackT_anchor5pctScenario=round(buy_5pct, 2),
        marginSLT_anchor5pctScenario=round(
            win["marginSLT"] - delta_spokes_t - buy_5pct, 1),
        # what the surviving allowance can bear, stacked worst case:
        # terminations at 2x declared mass AND the anchor-zone 5% point
        stackedWorstCaseT=round(
            win["marginSLT"] - delta_spokes_t - buy_5pct - lugs_t, 1),
    )

    # SF1.2 honest failure, same mechanism
    w12 = I005.World(1.2)
    win12 = alloc_rec["worlds"]["sf1.2"]["bestFeasible"]
    a12 = win12["point"]["alloc"]
    sp12 = w12.spokes_t(a12)
    fams12 = dict(d60=family_geometry("d60", 52, 59.226, planes_even),
                  d20=family_geometry("d20", 69, 19.742, planes_odd))
    cord12 = lug12 = clip12 = 0.0
    for f, key in ((fams12["d60"], "a_d60"), (fams12["d20"], "a_d20")):
        f["sectionM2"] = cord_section(a12[key], area_m2, f["planes"])
        cord12 += f["totalLenM"] * f["sectionM2"] * RHO_SPOKE / 1000.0
        lug12 += f["ends"] * LUG_KG / 1000.0
        clip12 += f["crossings"] * CLIP_KG / 1000.0
    b12 = (cord12 + lug12 + clip12) * (1.0 + ASSEMBLY)
    sf12 = dict(point=win12["which"],
                beforeT=round(win12["totalT"], 1),
                beforeMarginSLT=round(win12["marginSLT"], 1),
                spokesLineT=round(sp12, 1),
                afterT=round(win12["totalT"] - sp12 + b12, 1),
                afterMarginSLT=round(
                    win12["marginSLT"] + sp12 - b12, 1),
                verdict="STILL FAILS at sea level; retained honestly. The "
                        "mechanism improves it by the same spoke-line "
                        "delta but does not close it.")

    # ---- arrangement B bounds and unknowns ------------------------------
    l_eff = g["cylL"] + 2.0 * g["R"] / 3.0     # the model's axial length
    bounds = dict(
        circumferential="n = 2..12 vs 155 anchors: >= 12 anchor stations "
                        "per lobe at n=12; scalar factor licensed",
        axial=f"foundation modulation period 2 bays = {2.0 * SHIP0['bayM']:.0f} m"
              f" vs the model's axial mode length l_eff = {l_eff:.0f} m"
              " (the gi membrane term's own scale); the axial AVERAGE the "
              "model licenses is preserved exactly by section conservation",
        bayLocal="bay-local modes are outside the model's n=2..12 global "
                 "family both before and after this unit — unchanged "
                 "UNKNOWN, not a regression",
        sagVsGap="worst cord sag at declared pretension "
                 f"{max(d60['sagM'], d11['sagM']):.3f} m against a "
                 f"{SHIP0['bayM']:.0f} m plane gap; no intermediate guides "
                 "required by clearance; cord dynamics UNKNOWN (no guide "
                 "mass carried, threshold: guide needed if sway exceeds "
                 "half the residual gap)",
    )
    unknowns = dict(
        anchorZoneCompliance=f"per-end La UNKNOWN; the I004 5% point "
                             f"({ANCHOR_5PCT_LA} m/end) is priced as a "
                             "scenario, not assumed",
        creep="relieves pretension. The declared eps0 = 0.2% keeps the "
              "SHORTEST cord taut to a single-mode modal amplitude of "
              f"{round(w_slack, 4)} m (worst mode n={n_slack_worst} at "
              "its smallest occupied plane — the family-mean figure "
              "5.7x overstates the window); creep strain eps_c lowers "
              "that to (0.002 - eps_c)/"
              f"{round(worst_strain, 6)} m and reverses the cord's sign "
              "beyond it. Single-mode antinode bound: mixed-mode phase "
              "combinations and post-slack redistribution are outside it "
              "(carried to the coupled finite-endpoint unit). UNKNOWN, "
              "threshold recorded",
        cordDynamics="flutter/vibration of 70-80 m spans unmodelled; "
                     "clearance threshold in bounds.sagVsGap",
        membrane="still excluded, unchanged from the R3-I005 record",
        lugRating=f"{LUG_KG} kg swaged lug assumed rated >= 2x working "
                  "tension; sensitivity x2 mass = +"
                  f"{lugs_t:.1f} t (inside the allowance)",
    )

    out = dict(
        unit="R3-I009", rev="v2.1-first-review-corrections",
        world=dict(diaM=112.0, sigma="s1450", giKnockdown=0.65,
                   membrane=False,
                   status="internal conditional design hypothesis; scalar "
                          "feasibility NOT established (see "
                          "winner.finitePhase)"),
        winner=dict(source="../R3-I005/alloc.json bestFeasible (v3 "
                           "after-consolidated-review record)",
                    alloc={k: win_a[k] for k in win_a},
                    totalT=win["totalT"], marginSLT=win["marginSLT"],
                    modeMargins=mm0,
                    finitePhase=dict(
                        bindingModeFinite=finite_phase["bindingModeFinite"],
                        marginWeakestOrientation=finite_phase[
                            "marginWeakestOrientation"],
                        feasibleFinitePhase=finite_phase[
                            "feasibleFinitePhase"],
                        trial=finite_phase["trial"],
                        note=finite_phase["note"],
                        carriedFrom="the R3-I005 record; for GLOBAL "
                                    "circumferential modes every occupied "
                                    "plane contributes identical anchor "
                                    "phase sums, so the arrangement's "
                                    "orientation matrix equals the "
                                    "winner's — the alternating-plane "
                                    "geometry does not change it",
                        postLug=post_lug)),
        planes=dict(kept=137, total=145, minR=round(r_min, 3),
                    maxR=round(r_max, 3), bayM=SHIP0["bayM"]),
        arrangementB=dict(
            description="families in DISJOINT bay planes: d60 at even "
                        "indices (69 planes, both polar caps), d180/11 at "
                        "odd indices (68 planes); cords terminate directly "
                        "at the plane's ring anchor fittings, zero standoff, "
                        "zero axial offset, zero between-family contact",
            families={f["name"]: {k: (round(v, 4) if isinstance(v, float)
                                      else v)
                                  for k, v in f.items()
                                  if k not in ("name",)} for f in (d60, d11)},
            betweenFamilyCrossings=0, betweenFamilyConnectors=0,
            withinFamilyCrossings=d60["crossings"] + d11["crossings"],
        ),
        optionA=option_a,
        forces=forces,
        slackThresholdsPctByW=slack,
        bomB=dict(basis="explicit enumeration; replaces the model's x1.3 "
                        "fitting allowance and the 137-plane clip line — "
                        "no double count",
                  cordT=round(b_cord_t, 2),
                  i005CordSmearT=round(i005_cord_t, 2),
                  terminationsT=round(lugs_t, 2),
                  clipsT=round(clips_t, 2),
                  assemblyT=round(b_hardware_t * ASSEMBLY, 2),
                  totalT=round(b_spokes_t, 2),
                  i005SpokesLineT=round(i005_spokes, 2),
                  deltaT=round(delta_spokes_t, 2)),
        compliance=compliance,
        budgets=dict(sf10Before=sf10_before, sf10After=sf10_after,
                     sf12=sf12),
        bounds=bounds, unknowns=unknowns,
        verdict=dict(
            v1ClaimWithdrawn="v1 (commit 914bab52) claimed 'all 11 margins "
                             ">= 1.0, SF1.0 SL +80.0 t' on the scalar pass "
                             "of the then-current winner; the consolidated "
                             "review disproved that pass and v2 re-prices "
                             "on the corrected record — the closure claim "
                             "is withdrawn, v1 preserved as history",
            hypothesis="SF1.0 d60+d180/11 routed in alternating bay planes "
                       "(option B): explicit enumerated BOM replaces the "
                       "x1.3/137-plane allowances at "
                       f"{round(delta_spokes_t, 1)} t, and the declared "
                       "lug-only series compliance is bought back with "
                       f"{round(buy_lug, 2)} t of inner rings",
            margin="SCALAR margins restored to >= 1.0 by the buyback "
                   "(binding mode at the budget edge); the scalar pass "
                   "does NOT establish feasibility: the RIGID "
                   "weakest-orientation margin of the corrected winner is "
                   f"{finite_phase['marginWeakestOrientation']:.9f} "
                   "(binding n="
                   f"{finite_phase['bindingModeFinite']}), a pass by "
                   "3.7 ppm — and in the COMPLIANT as-declared state "
                   "(declared lug eta per family) the binding orientation "
                   f"margin FAILS at {om_lug[n_lug]:.9f} (n={n_lug}) vs "
                   "1.0, with a bounded ring-growth recovery of "
                   f"{round(orient_recover_t, 2)} t priced but not "
                   "applied; the mixed-mode trial verdict under the "
                   "review's convention is UNKNOWN on this point — "
                   "overall status UNKNOWN with a demonstrated "
                   "compliant-state orientation failure, closure not "
                   "claimed",
            confidence="LOW — conditional on an UNRESOLVED finite-phase "
                       "question, on the corrected-but-superseding R3-I005 "
                       "record, and on the declared lug/pretension "
                       "assumptions",
            weakestAssumption="the finite-endpoint phase/coupling verdict "
                              "(consolidated finding 1) — the engineering "
                              "below prices a layout whose feasibility is "
                              "NOT established; then anchor-zone series "
                              "compliance (UNKNOWN; the 5% point costs "
                              f"{round(buy_5pct, 1)} t of buyback)",
            nextChange="resolve the mixed-mode finite-phase verdict on the "
                       "corrected winner (review convention or a "
                       "demonstrated bound), then measure or bound the "
                       "anchor-zone compliance per end (La) with a "
                       "declared termination detail",
            failModes="finite-phase feasibility UNRESOLVED (this unit's "
                      "binding caveat); SF1.2 does not close (retained); "
                      f"mode {nb} fails without ring buyback once per-end "
                      "La exceeds "
                      f"{round(loss_budget * d60['meanCordM'] / 2.0, 3)} m",
        ),
    )
    with open(os.path.join(HERE, "routing.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print("R3-I009 routing.json written:",
          f"delta_spokes={delta_spokes_t:+.1f} t, "
          f"buyback_lug={buy_lug:.2f} t, buyback_5pct={buy_5pct:.2f} t, "
          f"SL={sf10_after['marginSLT']:+.1f} t, "
          f"postlug_n{n_lug}={om_lug[n_lug]:.9f}, "
          f"w_slack={w_slack:.6f} m")


if __name__ == "__main__":
    main()
