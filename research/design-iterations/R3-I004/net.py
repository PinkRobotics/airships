#!/usr/bin/env python3
"""R3-I004 (corrected after review) — the drawn net, its true modal stiffness.

v2, 2026-10-14. The v1 of this unit claimed the half-column-offset chordal net
engages every mode n=2..12 at >=0.9926 and "delivers the credited stiffness".
The lead's review (2026-10-14, seven findings, all reproduced below and in
net.json) demonstrated the endpoint law was wrong:

  for w = w_n cos(n th), a cord from anchor m to anchor m+step subtends
  phi = 2 pi step / nLong and stretches

      dL = 2 w sin(phi/2) cos(n phi/2) cos(n th + n phi/2),

  so the amplitude factor (engagement) is sin(phi/2)|cos(n phi/2)| — with PHI,
  the subtended angle, not the offset from antipodal. At odd n this is
  sin(phi/2) sin(n delta/2) with delta = pi - phi the antipodal offset: for the
  drawn 0.5-column offset (1.161 deg) mode 3 gets 0.030396, not 0.999487. The
  modal STIFFNESS scales with the SQUARE of the amplitude factor (energy:
  K = sum k_i (dL_i/w)^2), so odd-mode foundation from this layout is
  0.0009-0.0124 of what the model's gi_chordal credits. v1's formula used
  |cos(n delta/2)|, which is the EVEN-mode factor misapplied to all n.

Consequence, computed below: at the frozen allocation the mode-3 capacity is
84.1 kPa (engagement squared, membrane term as the reviewed row carried it)
against 101.325 kPa demand — FAIL before the gamma 0.65 knockdown (which would
require 155.9 kPa). The drawn net does NOT establish the +180.7 t bound; the
both-moves favourable rows' odd-n foundation credit is not delivered by this
layout. Verdict: FAIL for this layout under these assumptions (a vacuum design
with a different layout is not thereby excluded — see R3-I005).

Also corrected (findings 2,3,5,6,7): anchor-sensitivity lengths are PER END;
chord midpoints sit 20.3 mm apart at the barrel and 2.9 mm at the smallest
kept plane, so the v1 clearance claim is withdrawn (routing hardware UNKNOWN,
not zero); the extra-offset variant doubles anchors 76/77 and leaves 154
unused; crossings are 3,002 interior + 1 shared-endpoint pair per plane
(411,274 clips, 6.85 kg less than v1 billed); the sf1.08 row is a
recomputation, not an exact ledger reproduction (frozen row: 2130.7/119.1/-
373.3 t).

Deterministic arithmetic over the frozen model at base afb2c2d1; edits
nothing; proves nothing about a built aircraft; run twice -> identical bytes.
Internal conditional design hypothesis; no positive claim.
"""
from __future__ import annotations

import importlib.util
import json
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def load_model():
    spec = importlib.util.spec_from_file_location(
        "vc", ROOT / "research" / "analysis" / "vacuum-cell.py")
    vc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vc)
    return vc


vc = load_model()
SHIP0 = vc.SHIP0

POLAR_CUTOFF_M = 6.0
FITTING = SHIP0["spokeFitting"]   # 1.30 — the model's own end-fitting allowance
CLIP_KG = 0.05                    # per INTERIOR cord crossing (saddle clip)


def planes_of(g):
    """The model's own bay-plane enumeration (mirrors ship_spoke_net)."""
    bay = SHIP0["bayM"]
    n_bays = max(2, round(g["meridianM"] / bay))
    s_cap = math.pi * g["R"] / 2.0

    def r_at(s):
        if s <= s_cap:
            return g["rIn"] * math.sin(s / g["R"])
        if s <= s_cap + g["cylL"]:
            return g["rIn"]
        return g["rIn"] * math.cos((s - s_cap - g["cylL"]) / g["R"])

    return [r_at(g["meridianM"] * i / n_bays) for i in range(n_bays + 1)]


def drawn_net(g, extra_off=0):
    """The explicit net of v1, retained: anchor m <-> m + floor(n/2) - extra_off
    per kept bay plane. Counts, lengths and miss geometry are UNCHANGED from v1
    (the review confirmed them); only the modal law derived from this topology
    changes. Engagement is now the exact endpoint law, squared for stiffness."""
    n = g["nLong"]
    half = n // 2
    step = half - extra_off
    off = abs(n / 2.0 - step) * 2.0 * math.pi / n   # antipodal offset, rad
    kept = [r for r in planes_of(g) if r >= POLAR_CUTOFF_M]
    phi = 2.0 * math.pi * step / n                  # subtended angle, rad
    cords = len(kept) * (half + 1)                  # m = 0..half inclusive
    length = sum(2.0 * r * math.sin(phi / 2.0) for r in kept) * (half + 1)
    # THE CORRECTED LAW: amplitude engagement, and its square for stiffness.
    engage = {m: math.sin(phi / 2.0) * abs(math.cos(m * phi / 2.0))
              for m in range(2, 13)}
    engage_v1 = {m: math.sin(phi / 2.0) * abs(math.cos(m * off / 2.0))
                 for m in range(2, 13)}
    stiffness = {m: engage[m] ** 2 for m in engage}
    # crossings: interior pairs only; the doubled anchor shares one endpoint
    pairs = half + 1
    interior = pairs * (pairs - 1) // 2 - 1 if extra_off == 0 else None
    return dict(
        nLong=n, step=step, offsetDeg=math.degrees(off),
        subtendDeg=math.degrees(phi), planes=len(kept),
        planesTotal=len(planes_of(g)), cords=cords,
        anchorEnds=cords * 2, doubledAnchors=len(kept),
        lengthM=length, meanCordM=length / cords,
        engageByMode=engage, engageV1ByMode=engage_v1,
        stiffnessFactorByMode=stiffness,
        interiorCrossingsPerPlane=interior,
        crossings=len(kept) * interior if interior else 0,
        sharedEndpointPairsPerPlane=1 if extra_off == 0 else 0,
        missRadiusMaxM=max(r * math.sin(off / 2.0) for r in kept),
        # finding 3: adjacent chord-midpoint spacing on the miss circle
        midpointSpacingMmBarrel=max(kept) * math.sin(off / 2.0)
        * (2.0 * math.pi / n) * 1000.0,
        midpointSpacingMmSmallestPlane=min(kept) * math.sin(off / 2.0)
        * (2.0 * math.pi / n) * 1000.0,
    )


def variant_topology(g):
    """Finding 5: enumerate the extra_off=1 variant's actual endpoints."""
    n = g["nLong"]
    half = n // 2
    step = half - 1
    ends = {}
    # 78 cords, m = 0..77: m and m+76 as endpoints. (The v2 code enumerated
    # m = 0..78 — 79 cords — which doubled 78 and used anchor 154; caught in
    # the 2026-10-14 consolidated return, residual B.)
    for m in range(half + 1):
        ends[m] = ends.get(m, 0) + 1
        ends[m + step] = ends.get(m + step, 0) + 1
    doubled = sorted(k for k, v in ends.items() if v > 1)
    unused = [k for k in range(n) if k not in ends]
    return dict(step=step, doubledAnchors=doubled, unusedAnchors=unused,
                offsetDeg=math.degrees(abs(n / 2.0 - step) * 2.0 * math.pi / n))


def capacity_at_mode(r, g, net, n_mode, membrane=True):
    """Mode capacity of the FROZEN allocation under the corrected law, in Pa,
    before knockdown (the reviewed both-moves row carried the membrane term).
    q_found is the model's full-credit foundation times the squared engagement."""
    skel = r["skeleton"]
    E = vc.MATERIALS["T700_LAM"]["E"]
    depth, r_in, bay = g["depthM"], g["rIn"], SHIP0["bayM"]
    a_i = skel["innerRingAM2"]
    a_th = skel["thetaWebAM2"]
    a_oe = 0.0
    a_sp = skel["spokeAM2PerM2"]
    a_o0 = r["wall"]["ring"]["A"] / SHIP0["ringPitchM"]
    circ_col = 2.0 * math.pi * g["R"] / g["nLong"]
    theta_len = math.sqrt(depth * depth + circ_col * circ_col)
    cos_th = circ_col / theta_len
    q_crimp = (2.0 * E * a_th * depth * cos_th ** 2 / (bay * theta_len)) / g["R"]
    a_o = a_o0 + a_oe
    abar = a_o * (a_i / bay) / (a_o + a_i / bay)
    i_eff = abar * depth * depth
    q_ring = (n_mode ** 2 - 1) * E * i_eff / g["R"] ** 3
    q_ring = 1.0 / (1.0 / q_ring + 1.0 / q_crimp)
    q_found_full = SHIP0["eSpoke"] * a_sp / (n_mode ** 2 - 1)
    q_mem = 0.0
    if membrane:
        l_eff = g["cylL"] + 2.0 * g["R"] / 3.0
        lam2 = (math.pi * g["R"] / l_eff) ** 2
        a_x = skel["longeron"]["A"] * g["nLong"] / (2.0 * math.pi * r_in)
        nn_l2 = n_mode ** 2 + lam2
        q_mem = (E * a_x * lam2 ** 2
                 / (g["R"] * (n_mode ** 2 + lam2 / 2.0 - 1.0) * nn_l2 * nn_l2))
    f2 = net["stiffnessFactorByMode"][n_mode]
    q = q_ring + q_found_full * f2 + q_mem
    return dict(modeN=n_mode, qRingCrimpPa=q_ring, qFoundFullPa=q_found_full,
                stiffnessFactor=f2, qFoundCorrectedPa=q_found_full * f2,
                qMembranePa=q_mem, qTotalPa=q,
                demandPa=vc.P_ATM * r["sf"],
                demandWithKnockdownPa=vc.P_ATM * r["sf"] / r["giKnockdown"],
                passes=q * r["giKnockdown"] >= vc.P_ATM * r["sf"])


def price_net(g, r, net):
    """Mass arithmetic of the drawn article (v1's arithmetic, crossings
    corrected). These are the MASS OF THE DRAWN NET, not evidence of a feasible
    bound — the capacity verdict above governs that question."""
    a_sp = r["skeleton"]["spokeAM2PerM2"]
    a_cord_total = a_sp * g["areaM2"]
    cord_t = a_cord_total * net["meanCordM"] * SHIP0["rhoSpoke"] / 1000.0
    fitted_t = cord_t * FITTING
    total = r["totalT"] - r["skeleton"]["spokesT"] + fitted_t \
        + net["crossings"] * CLIP_KG / 1000.0
    return dict(
        aSpokeM2PerM2=a_sp, cordAreaM2=a_cord_total,
        billedSpokesT=r["skeleton"]["spokesT"], drawnCordT=cord_t,
        drawnFittedT=fitted_t,
        crossingClipsT=net["crossings"] * CLIP_KG / 1000.0,
        clipsCount=net["crossings"],
        massDeltaT=fitted_t + net["crossings"] * CLIP_KG / 1000.0
        - r["skeleton"]["spokesT"],
        massOfDrawnArticleT=total,
        note="mass arithmetic only; NOT a feasible-bound mass: the mode-3 "
             "capacity verdict fails under the corrected engagement law",
    )


def series_anchor_sensitivity(net):
    """End/anchor compliance in series: L/(L+2La). PER END and combined."""
    l_c = net["meanCordM"]
    out = dict(meanCordM=round(l_c, 4))
    for pct in (5, 25, 50):
        la = l_c * (1.0 / (1.0 - pct / 100.0) - 1.0) / 2.0
        out[f"pct{pct}"] = dict(perEndM=round(la, 4),
                                bothEndsM=round(2 * la, 4))
    out["note"] = ("an anchor+termination zone behaving as La of extra cord "
                   "AT EACH end costs the named stiffness fraction; v1 "
                   "mislabelled the per-end values as combined")
    return out


def row(sf):
    r = vc.ship0("s1450", sf, 112.0, 0.65, True, True, basis="favourable")
    return r["geom"], r


def main():
    out = dict(
        unit="R3-I004", rev="v2-corrected-after-review",
        review="lead review 2026-10-14 (seven findings, all reproduced; "
               "see reviewDisposition)",
        base="afb2c2d1726b9d9a805f9781085c3dd6a52913e5",
        verdict="FAIL — the drawn half-column-offset net does not deliver the "
                "odd-mode foundation the both-moves rows credit; mode-3 "
                "capacity 84.1 kPa vs 101.325 kPa demand (before knockdown) "
                "at the frozen allocation. The +180.7 t feasible-bound claim "
                "is withdrawn. Not generalised to all vacuum designs.",
        assumptions=dict(
            pairing="anchor m <-> m + floor(nLong/2), 0.5-column antipodal "
                    "offset, one doubled anchor per plane (topology "
                    "unchanged from v1)",
            engagementLaw="amplitude sin(phi/2)|cos(n phi/2)| with phi the "
                          "SUBTENDED angle; stiffness scales as its square",
            polarCutoffM=POLAR_CUTOFF_M, fittingKept=FITTING,
            crossingClipKg=CLIP_KG,
            routingHardware="UNKNOWN and unpriced: 20.3 mm barrel / 2.9 mm "
                            "smallest-plane chord-midpoint spacing vs "
                            "11.9 mm cord — v1's no-contact claim withdrawn",
            status="internal conditional design hypothesis, not measured"),
        worlds={}, mode3Capacity=None, anchorSensitivity=None,
        variantTopology=None, reviewDisposition=[],
    )
    nets = {}
    for sf in (1.0, 1.08, 1.2):
        g, r = row(sf)
        net = drawn_net(g)
        nets[sf] = (g, r, net)
        out["worlds"][f"sf{sf}"] = dict(
            net={k: (round(v, 4) if isinstance(v, float) else v)
                 for k, v in net.items()
                 if k not in ("engageByMode", "engageV1ByMode",
                              "stiffnessFactorByMode")},
            engageByMode={str(k): round(v, 6) for k, v in
                          net["engageByMode"].items()},
            stiffnessFactorByMode={str(k): round(v, 6) for k, v in
                                   net["stiffnessFactorByMode"].items()},
            price=price_net(g, r, net),
            ledgerBefore=dict(
                totalT=round(r["totalT"], 1),
                marginSLT=round(r["residualSLT"], 1),
                margin2500T=round(r["residual2500T"], 1),
                provenance="exact ledger reproduction" if sf != 1.08 else
                           "recomputation at sf=1.08; frozen ledger mid-band "
                           "row reads 2130.7/119.1/-373.3 t (finding 7)"),
        )
    g10, r10, net10 = nets[1.0]
    out["mode3Capacity"] = capacity_at_mode(r10, g10, net10, 3)
    out["anchorSensitivity"] = series_anchor_sensitivity(net10)
    out["variantTopology"] = dict(
        variant_topology(g10),
        note="finding 5: v1 claimed the offset 'removes doubled-anchor "
             "bookkeeping' — false; and these are 112 m numbers, not the "
             "52 m/72-anchor case (whose one-column offset is 5 deg)")
    out["reviewDisposition"] = [
        dict(id=1, severity="HIGH",
             claim="engagement law wrong at odd n; stiffness squared",
             reproduction="exact law sin(phi/2)|cos(n phi/2)| gives n=3 "
                          "0.030396 (v1: 0.999487); squared 0.000924",
             correction="law replaced throughout; mode-3 capacity verdict "
                        "FAIL recorded; bound withdrawn"),
        dict(id=2, severity="MEDIUM",
             claim="anchor lengths are per end, labelled combined",
             reproduction="per end 2.1237/13.4499/40.3496 m; combined "
                          "4.2473/26.8997/80.6992 m",
             correction="both reported, labels fixed"),
        dict(id=3, severity="MEDIUM",
             claim="midpoint spacing 20.349/2.896 mm, not 40 mm",
             reproduction="20.35 mm barrel (r=49.54 m), 2.90 mm smallest "
                          "kept plane (r=7.05 m) vs 11.869 mm cord",
             correction="clearance claim withdrawn; routing hardware "
                        "UNKNOWN, not zero"),
        dict(id=4, severity="MEDIUM",
             claim="no retained incumbent; re-solve has no improvement "
                   "guarantee",
             reproduction="greedy starts at minimum members, zero spokes; "
                          "R3-I005's own sf1.2 rerun landed 20.2 t worse",
             correction="upper-bound/guaranteed-improvement language "
                        "withdrawn everywhere"),
        dict(id=5, severity="LOW",
             claim="offset variant doubles anchors 76/77, leaves 154 unused",
             reproduction="enumerated: doubled [76, 77], unused [154]",
             correction="variantTopology records the real endpoints; "
                        "52 m/72-anchor remark corrected"),
        dict(id=6, severity="LOW",
             claim="3002 interior crossings + 1 shared pair, not 3003",
             reproduction="per plane 3002 interior; 411,274 clips; v1 excess "
                          "137 clips = 6.85 kg",
             correction="crossings and clip mass corrected"),
        dict(id=7, severity="LOW",
             claim="sf1.08 row not an exact ledger reproduction",
             reproduction="recomputed 2130.9/119.0/-373.5 vs frozen "
                          "2130.7/119.1/-373.3 t",
             correction="provenance stated per row; sf1.0/1.2 exact"),
    ]
    (HERE / "net.json").write_text(json.dumps(out, indent=1) + "\n")
    cap = out["mode3Capacity"]
    print(f"R3-I004 v2 net.json written: verdict FAIL — mode-3 q "
          f"{cap['qTotalPa']:.1f} Pa vs demand {cap['demandPa']:.1f} Pa "
          f"(knockdown-required {cap['demandWithKnockdownPa']:.1f}); "
          f"stiffness factor n=3 {cap['stiffnessFactor']:.6f}")


if __name__ == "__main__":
    main()
