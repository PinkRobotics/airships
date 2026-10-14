#!/usr/bin/env python3
"""R3-I019 v3 — targeted completion of the v2 correction: ONE signed
installed spring model, a buildable bolted attachment with ONE
cord accounting boundary and the Pa/MPa units label for
the drawn termination/pretension construction and the mixed-field taut
window of the completed 155-start arrangement of R3-I015.

v2 corrected the eleven demonstrated defects of the
v1 record; its targeted verification left the spring-model and
accounting repairs partially open and the units label open.  This
successor repairs exactly those in the v2 record:

SPRING  ONE spring denominator everywhere.  v2 defined the declared law
     d_eps = dL/(L_free + 2*L_a) with L_free = chord - 2*(NOSE+Lg)
     (between socket mouths) but computed the drawn stiffness factor
     as eta = mc/(mc + 2*L_a) — the WHOLE mean anchor-centre chord as
     free cord — and fed that into the coupled energy.  Every eta now
     uses the same chain: eta = mc/(L_free_mean + 2*L_a) where the
     reference length mc is the mean anchor-centre chord (the coupled
     matrix's pin-jointed ideal).  The drawn chain is STIFFER than
     that ideal (the bonded grip shortens the active cord by more than
     the stud/body series adds back), so eta > 1 and the drawn coupled
     margin sits just above the licensed rigid value — reported, with
     the licensed rigid scalar retained as the quotable margin (no
     beyond-rigid qualification is claimed).

PACKET  SIGNED mixed-packet first loss on the declared law.  The v2
     packet numbers kept the v1 chord amplitude and ABSOLUTE-value
     severity counts.  The corrected-law result is computed exactly
     over the finite occupied member set (155 station phases x both
     families' innermost planes; the plane dimension is closed by the
     exact monotonicity of L(r_min)/L_eff(r)): the first cord to lose
     tension under the slack adversary -x*, its amplitude, the most-
     stretched remaining cord per family and SIGNED severity counts.
     First tension loss comes from signed tension, never |strain|.
     Grid-sampled amplitude estimates (w_of, 2^16 points) are labelled
     as sampled and kept separate from the continuous two-sided class
     bounds; the v1 chord-scale numbers are retained as labelled
     historical counterexamples.

ACCOUNTING  ONE cord accounting boundary.  The anchor-centre datum is
     the grip back face: anchor-centre chord = free span + 2 embedded
     (nose+grip) runs, so the potted embedded cord lies INSIDE the
     chord and the record's cord mass (priced over full anchor-centre
     chords) already contains it.  v2's separate 0.34 t potted-tow
     line was a double count — removed; every cord segment is counted
     once.  The stud/seat lies BEYOND the anchor centre: drawn in the
     station stack, priced in the socket hardware and carried in the
     spring model as the series compliance L_ser.

BOLTS  A buildable bolted stack.  30 mm shanks cannot span block 24/30
     + doubler pad 3 + ring wall 6 + backing nut 8 (41/47 mm before
     protrusion).  Per-family M10 shanks 45/50 mm are dimensioned and
     priced for the full stack; single-shear capacity is unchanged;
     laminate bearing/bending/pull-through remain UNKNOWN.

UNITS  materialLedger.cord.EMpa held 70e9 (a Pa value behind an MPa
     label); the key is EPa=70e9 with the narrative in Pa/GPa only.

Historical v3 input: the corrected R3-I015 record (not the original
R3-I015 record).  Imported record files are the corrected R3-I015
outputs in ../R3-I015/.

Scope (bounded analytic/small-matrix work only; no solver, no sweep,
no optimizer; 22 coordinates throughout):

1. MATERIAL IDENTITY.  The inherited cord inputs eSpoke 70 GPa /
   rhoSpoke 970 kg/m^3 are documented at their source
   (tools/ship_scoping.py:138-139) as a DYNEEMA-CLASS (UHMWPE) cord
   modulus with creep unverified.  They are NOT a carbon-tow record:
   this unit no longer names T700 for the cord, borrows no fibre
   ultimate, claims no carbon-specific swage incompatibility and no
   positive potting compatibility.  Cord strength is UNKNOWN; the
   drawn potted-socket is a SELECTED hypothetical construction whose
   12 MPa design bond shear is an ASSUMED design value, not a
   qualified UHMWPE-termination number.  The laminate (rings, rails,
   doubler pads) remains T700S-sourced where the record sourced it.

2. TERMINATION SIZING ON THE TRANSFERRING INTERFACE.  The grip
   is sized on the cord/resin interface pi*d_cord*Lg (v1 used the
   larger bore perimeter pi*d_bore*Lg).  At the v1 grips the cord
   interface shear was 13.7715/13.7825 MPa against the assumed 12 MPa
   (counterexamples, asserted); required unrounded grips
   59.677/96.478 mm; drawn grips 60/97 mm.  The resin/socket-wall
   interface pi*d_bore*Lg is checked as the other transferring
   surface (10.4 MPa, within the same assumed value).

3. SIGNED SLACK, FREE LENGTH AND BOTH-END COMPLIANCE.  Every
   projected extension is SIGNED: the reported adversarial packet
   x* = g_j*/||g_j*|| STRETCHES its target cord (+eps0, 2*T0 at
   scale); its negative is the slack adversary.  Declared spring
   model per end: the cord runs free between socket mouths
   (L_free = anchor-centre chord - 2*(NOSE + Lg)), and each end
   contributes an equivalent cord length L_a = NOSE + Lg/2 (the
   stretch up to the mid-grip transfer centroid) + the stud/body
   series compliance as cord length.  Incremental strain is
   dL/(L_free + 2*L_a); slack when the increment reaches -eps0.
   The mid-grip transfer centroid is a DECLARED ASSUMPTION; the
   no-transfer variant (whole embedded cord stretches) is carried as
   the upper sensitivity.

4. n=5 FIRST SLACK FROM THE 155-STATION PHASES.  The v1 value
   50.4 mm evaluated the a=0 endpoint only.  For u = +-w cos(5*theta)
   the true first-slack threshold is the minimum over occupied
   cords: under the OLD chord law the counterexamples
   25.668698 mm (d180/11, +cos5) / 26.797732 mm (d60, +cos5) /
   25.537001 mm (d180/11, -cos5) are asserted.  5*theta quantises
   the 155 stations into 31 phases; the controlling station follows
   analytically (no field search); the controlling plane is the
   innermost (the strain denominator is monotone in r and the
   station phase set is plane-independent).  The +-sin5 degenerate
   partner is enumerated alongside.  Corrected-law thresholds use
   the declared spring model denominator.

5. COORDINATES.  The norm used in this unit is on RADIAL Fourier
   coefficients c (cos+sin pairs).  The R3-I015 eigen machinery uses
   y = sqrt(D) c with D_nn = n^2-1 (y_c5 = 1 maps to c5 = 1/sqrt(24)
   = 0.204124145232); cross-basis comparisons carry the sqrt(D)
   mapping.  Pressure-work normalisation: the licensed constant
   KD/(P_ATM*SF) = 6.41500123365e-06 at SF=1.

6. NO UNIQUENESS.  Pure-mode restrictions do not determine the
   cross-mode entries (diag(a,b) and the off-diagonal sqrt(ab)/2
   matrix are both positive definite with identical pure-mode
   blocks); the cross extension is an EXPLICIT ASSUMPTION carried
   from I015, and numerical parity is not a physical measurement.

7-8. SENSITIVITIES.  The x1.5 station-hardware scenario
   applies the 5% assembly allowance to the INCREMENT (v1 omitted
   0.69225 t; counterexample 4.57575 asserted on the v1
   bill).  Bond-shear sensitivity is tabulated from the sizing
   relation Lg ~ 1/tau (150%/60% for 12->8/20 MPa before rounding)
   with the stud/nut/nose masses FIXED (socket mass does not scale
   with grip length); tau itself is an unverified assumed property.

9. RING ATTACHMENT.  ONE dimensioned securing construction per
   station: the anchor block is bolted to the doubler pad and the
   pad to the ring wall by 3 x M10 Ti-6Al-4V through-bolts with
   internal backing nuts (single-shear sizing on the worst-window
   pair load with the record's 1.3 fitting factor; installation
   access through the adjacent bay at the 0.5 m ring pitch before
   pump-down).  The pad/ring bond film is credited ZERO capacity;
   laminate bearing, block local bending and pull-through are
   UNKNOWN.  Anchor-centre, grip, embedded lengths and the actual
   free cord length are defined once; cord and potted material are
   each counted once (chord + embedded extra, no overlap).

10. REPRESENTATIONS and 11. SF1.2 BASELINE.  Drawings,
    JSON and prose carry the same numbers.  The SF1.2 comparison is
    rebuilt against the CORRECTED completed R3-I015 case
    (budgets.sf12Completed, pinned: before 2536.9 -> after 2546.1 t,
    margin -296.3), not the I005 winner line; the inherited +9.2 t
    completion change is not presented as new termination mass.

LOAD-PATH LIMIT (retained, material-honest).  The static per-plane
pressure reference P*2*pi*R*bay shared by cord radial components
would put the outermost-plane cords at ~234 kN (d60) / ~206 kN (d11)
if the web resisted the band directly; the cord's qualified strength
is UNKNOWN, so no utilisation is computed.  The vehicle-level load
path is recorded UNKNOWN (the model excludes the membrane); the
R3-I023 unit in the same checkout reads the 234/206 kN figure as the
bypass force, superseded as a load path (cross-reference, itself
unreviewed).

Units: SI throughout (lengths m unless labelled mm, forces N, stresses
Pa, masses kg/t).  Deterministic: pure Python, no randomness; output
JSON is byte-identical across runs.
"""
from __future__ import annotations

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _p in ("..", "../R3-I005", "../R3-I009", "../R3-I015"):
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, _p)))

import alloc as I005                # noqa: E402  (R3-I005 record)
import routing as RT                # noqa: E402  (R3-I009 record)
import coupled as C                 # noqa: E402  (R3-I015 record, corrected)

SHIP0 = I005.SHIP0
E_SPOKE, RHO_SPOKE = RT.E_SPOKE, RT.RHO_SPOKE
EPS0 = RT.EPS_PRETENSION
P_ATM, KD = I005.P_ATM, I005.KD
FITTING = SHIP0["spokeFitting"]          # 1.3 — the record's own factor
N_LONG, MODES = C.N_LONG, C.MODES
NMOD = C.NMOD

# ---- the drawn construction's declared numbers (assumptions explicit) ----
TI_RHO = 4430.0        # Ti-6Al-4V kg/m^3 (public datasheet)
TI_E = 114.0e9         # Ti-6Al-4V Pa (public datasheet)
TI_SIGMA_Y = 880.0e6   # Ti-6Al-4V Pa (public datasheet)
EPOXY_RHO = 1150.0     # filled epoxy kg/m^3
TAU_BOND = 12.0e6      # ASSUMED design bond shear Pa (unverified property)
BORE_K = 1.15          # socket bore / cord diameter
BODY_OD_K = 2.6        # socket body OD / bore
NOSE_M = 0.008         # nose+seat length each side of the pot
STUD_D_K = 1.8         # stud major diameter / cord diameter
STUD_L_K = 10.0        # stud length / cord diameter (thread+shank)
NUT_T_K = 1.6          # jam nut thickness / cord diameter
NUT_OD_K = 2.2         # jam nut across-flats / cord diameter
NUT_FULL = 0.7         # hex volume fullness vs enveloping cylinder
# station hardware (bounded assumptions; sensitivity in JSON)
BLOCK = {"d60": (0.050, 0.036, 0.024), "d180/11": (0.064, 0.046, 0.030)}
DOUBLER = (0.200, 0.140, 0.003)         # m, carbon laminate (rho 1600)
LAM_RHO = 1600.0
# attachment: one dimensioned securing construction per station.
# the through-bolt must span the FULL radial stack — block +
# doubler pad + ring wall + backing nut + point protrusion.  30 mm
# shanks (v2) cannot: block 24/30 + pad 3 + wall 6 + nut 8 alone is
# 41/47 mm.  Dimensioned per family:
#   d60:     24 + 3 + 6 + 8 + 4 protrusion/washers = 45 mm shank
#   d180/11: 30 + 3 + 6 + 8 + 3 protrusion/washers = 50 mm shank
ATT_BOLTS = 3          # M10 Ti through-bolts, single shear, backing nuts
ATT_D = 0.010                    # bolt shank diameter m
ATT_L_M = {"d60": 0.045, "d180/11": 0.050}   # priced shank length m
RING_WALL_M = 0.006              # ring wall thickness in the bolt axis
ATT_NUT_AF, ATT_NUT_T = 0.017, 0.008
ATT_PITCH = 0.016                # hole pitch in the block base flange
ATT_SHEAR_K = 0.6                # tau_allow = 0.6 sigma_y (distortion-energy)
# the ONE accounting datum.  Anchor centre = grip back face (where
# cord tension passes into the socket body metal).  The embedded run
# nose+grip is INSIDE the anchor-centre chord: chord = L_free +
# 2*(NOSE+Lg).  The stud/seat lies BEYOND the anchor centre (priced in
# the socket hardware, carried in the spring model as L_ser).
ANCHOR_DATUM = ("anchor centre = grip back face; socket mouth at"
                " NOSE+Lg inboard of it; the potted embedded cord"
                " (nose+grip) lies INSIDE the anchor-centre chord and"
                " is contained in the record's cord mass (priced over"
                " full anchor-centre chords); stud/seat BEYOND the"
                " anchor centre is socket hardware + series compliance")
# v1 grips retained ONLY as counterexample inputs (52/84 mm)
LEGACY_GRIP_MM = {"d60": 52.0, "d180/11": 84.0}


def g_vec(step, L, t_mid):
    """22-vector strain functional of one cord (eps_j = g_j . x)."""
    phi = 2.0 * math.pi * step / N_LONG
    sh = math.sin(phi / 2.0)
    g = []
    for n in MODES:
        a = 2.0 * sh * math.cos(n * phi / 2.0) / L
        g.append(a * math.cos(n * t_mid))
        g.append(a * math.sin(n * t_mid))
    return g


def g_norm(step, L):
    """||g_j||_2 — exact, and independent of t_mid (clock-free)."""
    phi = 2.0 * math.pi * step / N_LONG
    sh = math.sin(phi / 2.0)
    s = sum(math.cos(n * phi / 2.0) ** 2 for n in MODES)
    return 2.0 * sh * math.sqrt(s) / L


def w_of(x, ngrid=1 << 16):
    """max_theta |u(theta)| for radial-coefficient vector x (exact grid)."""
    best = 0.0
    for k in range(ngrid):
        th = 2.0 * math.pi * k / ngrid
        u = 0.0
        for i, n in enumerate(MODES):
            u += x[2 * i] * math.cos(n * th) + x[2 * i + 1] * math.sin(n * th)
        best = max(best, abs(u))
    return best


def main():
    w = I005.World(1.0)
    rec = json.load(open(os.path.join(HERE, "..", "R3-I005", "alloc.json")))
    win = rec["worlds"]["sf1.0"]["bestFeasible"]
    win_a = win["point"]["alloc"]
    area = w.g["areaM2"]
    kept = [r for r in C.planes_of(w.g) if r >= 6.0]
    pe, po = kept[0::2], kept[1::2]
    cjson = json.load(open(os.path.join(HERE, "..", "R3-I015", "coupled.json")))

    fams = [("d60", 52, 59.226, pe, "a_d60"),
            ("d180/11", 70, 17.419, po, "a_d180/11")]

    # ------------------------------------------------------------------
    # 0. dependency pin: the corrected completed I015 budgets
    # ------------------------------------------------------------------
    b15 = cjson["budgets"]["sf10Completed"]
    b12c = cjson["budgets"]["sf12Completed"]
    assert abs(b12c["beforeT"] - 2536.9) < 0.05
    assert abs(b12c["afterT"] - 2546.1) < 0.05
    assert abs(b12c["afterMarginSLT"] + 296.3) < 0.05

    # ------------------------------------------------------------------
    # 1. the drawn termination, sized and priced on the cord interface
    # ------------------------------------------------------------------
    term = {}
    hw_mass = 0.0            # kg: sockets + blocks + doublers
    attach_mass = 0.0        # kg: bolts+nuts
    removed_lug_kg = 0.0
    tow_v2_t = 0.0           # t: the v2 double-counted potted-tow line (pin)
    for name, step, off, planes, key in fams:
        g = C.family_geometry_full(name, step, off, planes, 155)
        sec = win_a[key] * area / g["cords"]
        dia = 2.0 * math.sqrt(sec / math.pi)
        T0 = E_SPOKE * sec * EPS0
        T_fit = 2.0 * T0 * FITTING          # worst taut-window swing x fitting
        bore = BORE_K * dia
        # counterexample (v1 grips on the WRONG perimeter):
        lg_old = LEGACY_GRIP_MM[name] / 1000.0
        tau_old = T_fit / (math.pi * dia * lg_old)
        lg_req = T_fit / (math.pi * dia * TAU_BOND)
        # drawn grip: cord/resin interface, mm ceiling
        Lg = math.ceil(lg_req * 1000.0) / 1000.0
        # other transferring interface: resin annulus on the socket wall
        tau_wall = T_fit / (math.pi * bore * Lg)
        od = BODY_OD_K * bore
        body_l = Lg + 2.0 * NOSE_M
        body_v = math.pi / 4.0 * (od ** 2 - bore ** 2) * body_l
        pot_v = (math.pi / 4.0 * (bore ** 2 - dia ** 2) * Lg
                 + math.pi / 4.0 * bore ** 2 * NOSE_M)
        stud_d, stud_l = STUD_D_K * dia, STUD_L_K * dia
        stud_v = math.pi / 4.0 * stud_d ** 2 * stud_l
        nut_v = NUT_FULL * math.pi / 4.0 * (NUT_OD_K * dia) ** 2 * NUT_T_K * dia
        per_end = dict(
            bodyKg=body_v * TI_RHO, resinKg=pot_v * EPOXY_RHO,
            studKg=stud_v * TI_RHO, nutKg=nut_v * TI_RHO)
        per_end["totalKg"] = sum(per_end.values())
        # --- free length and both-end compliance (declared model) ---
        ea = E_SPOKE * sec
        series = stud_l / (TI_E * math.pi / 4.0 * stud_d ** 2) \
            + body_l / (TI_E * math.pi / 4.0 * (od ** 2 - bore ** 2))
        la_ser = ea * series                      # stud+body as cord length
        l_a = NOSE_M + Lg / 2.0 + la_ser          # per end, mid-grip centroid
        l_a_notransfer = NOSE_M + Lg + la_ser     # sensitivity: no transfer
        rmin = min(planes)
        chord_min = 2.0 * rmin * g["sinHalf"]
        l_free = chord_min - 2.0 * (NOSE_M + Lg)  # between socket mouths
        l_eff = l_free + 2.0 * l_a                # chord - Lg + 2 la_ser
        l_eff_nt = l_free + 2.0 * l_a_notransfer
        mc = g["meanCordM"]
        # v1 chord-basis eta with the v1 grip (counterexample)
        series_old = stud_l / (TI_E * math.pi / 4.0 * stud_d ** 2) \
            + (lg_old + 2.0 * NOSE_M) \
            / (TI_E * math.pi / 4.0 * (od ** 2 - bore ** 2))
        la_old = lg_old / 2.0 + ea * series_old
        eta_v1 = chord_min / (chord_min + 2.0 * la_old)
        # ONE denominator everywhere.  The eta reference length is
        # the MEAN anchor-centre chord (the coupled matrix's pin-jointed
        # ideal); the drawn chain denominator is the SAME declared law
        # as the slack model — L_free(mean) + 2*L_a, NOT mc + 2*L_a.
        mc_free = mc - 2.0 * (NOSE_M + Lg)      # mean inter-mouths span
        mc_eff = mc_free + 2.0 * l_a            # = mc - Lg + 2 l_ser
        assert abs(mc_eff - (mc - Lg + 2.0 * la_ser)) < 1e-12
        assert mc_eff < mc, (name, mc_eff, mc)  # chain stiffer than ideal
        # --- attachment sizing (worst-window pair load, single shear) ---
        pair_load = FITTING * 2.0 * (2.0 * T0) * g["sinHalf"]
        bolt_a = math.pi / 4.0 * ATT_D ** 2
        cap = ATT_BOLTS * bolt_a * ATT_SHEAR_K * TI_SIGMA_Y
        bl = BLOCK[name]
        block_kg = bl[0] * bl[1] * bl[2] * TI_RHO
        doubler_kg = DOUBLER[0] * DOUBLER[1] * DOUBLER[2] * LAM_RHO
        # shank priced at the full dimensioned stack length
        att_l = ATT_L_M[name]
        stack_min = bl[2] + DOUBLER[2] + RING_WALL_M + ATT_NUT_T
        assert att_l >= stack_min + 0.003, (name, att_l, stack_min)
        bolt_set_kg = ATT_BOLTS * (
            bolt_a * att_l * TI_RHO
            + NUT_FULL * math.pi / 4.0 * ATT_NUT_AF ** 2 * ATT_NUT_T * TI_RHO)
        # cord mass over full anchor-centre chords (the record's
        # bom cordT) already contains the embedded (nose+grip) runs —
        # they lie INSIDE the chord.  v2 charged them AGAIN as a
        # potted-tow line (double count, removed); the value is kept
        # only as the counterexample pin at the bill.
        tow_kg_v2 = (Lg + NOSE_M) * sec * RHO_SPOKE   # DOUBLE COUNT (v2)
        plane_kn = 2.0 * 155 * (T0 / 1000.0) * g["sinHalf"]
        pitch = 2.0 * math.pi * min(planes) / N_LONG
        eta_old = mc / (mc + 2.0 * RT.LUG_LA_M)   # declared lug (reference)
        # the consistent drawn eta — same declared law as slack
        eta_new = mc / mc_eff                     # > 1: chain stiffer than ideal
        tow_v2_t += tow_kg_v2 * g["ends"] / 1000.0   # v2 double count (pin)
        pload = P_ATM * 2.0 * math.pi * max(planes) * w.bay
        teq = pload / (2.0 * 155 * g["sinHalf"])
        term[name] = dict(
            diaMm=round(dia * 1000.0, 2), sectionM2=sec,
            T0kN=round(T0 / 1000.0, 3), TfitkN=round(T_fit / 1000.0, 2),
            cordInterfaceShearV1MPa=round(tau_old / 1e6, 6),
            requiredGripUnroundedMm=round(lg_req * 1000.0, 6),
            gripLgMm=round(Lg * 1000.0, 1), gripOverDia=round(Lg / dia, 2),
            wallInterfaceShearMPa=round(tau_wall / 1e6, 3),
            boreMm=round(bore * 1000.0, 1),
            bodyOdMm=round(od * 1000.0, 1), bodyLenMm=round(body_l * 1000.0, 1),
            studMm=f"M{stud_d*1000.0:.0f}x{stud_l*1000.0:.0f}",
            perEndKg={k: round(v, 4) for k, v in per_end.items()},
            ends=g["ends"],
            socketsT=round(per_end["totalKg"] * g["ends"] / 1000.0, 2),
            blockKg=round(block_kg, 3), doublerKg=round(doubler_kg, 3),
            stations=g["cords"],                       # 155 per plane
            blocksT=round(block_kg * g["cords"] / 1000.0, 2),
            doublersT=round(doubler_kg * g["cords"] / 1000.0, 2),
            embeddedAccounting="embedded (nose+grip) cord lies INSIDE the "
                               "anchor-centre chord and is contained in the "
                               "record cordT — NO separate tow line (the v2 "
                               + "{:.2f} t potted-tow line was a double "
                               "count)".format(
                                   tow_kg_v2 * g["ends"] / 1000.0),
            removedLugT=round(g["ends"] * RT.LUG_KG / 1000.0, 2),
            freeLength=dict(
                anchorCentreChordMinM=round(chord_min, 6),
                lFreeM=round(l_free, 6), lAPerEndM=round(l_a, 6),
                lSerM=round(la_ser, 6),
                lEffM=round(l_eff, 6), lEffNoTransferM=round(l_eff_nt, 6),
                etaV1ChordBasis=round(eta_v1, 9),
                etaDrawnMeanCord=round(eta_new, 9),
                etaDeclared=round(eta_old, 6),
                referenceLength="eta reference = the MEAN anchor-centre "
                                "chord mc (the coupled matrix's pin-jointed "
                                "ideal); meanCordM={:.6f}".format(mc),
                meanCordM=round(mc, 6),
                lFreeMeanM=round(mc_free, 6), lEffMeanM=round(mc_eff, 6),
                denominatorLaw="ONE law everywhere: chain denominator = "
                               "L_free + 2 L_a with L_free = chord - "
                               "2 (NOSE+Lg) (eta uses the mean cord, slack "
                               "the innermost plane of each family); v2's "
                               "eta = mc/(mc+2 L_a) treated the whole mean "
                               "chord as free cord — SUPERSEDED",
                etaStifferThanIdeal="eta > 1: the bonded grip shortens the "
                                    "active cord by more than the stud/body "
                                    "series adds back (Lg - 2 l_ser = "
                                    "{:.5f} m per cord)".format(
                                        Lg - 2.0 * la_ser),
                etaGainPct=round((eta_new - eta_old) / eta_old * 100.0, 3),
                strainIncrement="d_eps = dL/(L_free + 2 L_a); slack at "
                                "-eps0 on the SAME denominator; the mid-grip "
                                "transfer centroid is a DECLARED assumption, "
                                "the no-transfer variant is the upper bound"),
            attachment=dict(
                construction="3 x M10 Ti-6Al-4V through-bolts, internal "
                             "backing nuts, block flange -> doubler pad -> "
                             "ring wall; 16 mm hole pitch; installed through "
                             "the adjacent bay before pump-down",
                shankMm=round(att_l * 1000.0, 0),
                stackDimensioned="block {:.0f} + doubler pad {:.0f} + ring "
                                 "wall {:.0f} + backing nut {:.0f} = {:.0f} mm "
                                 "minimum; shank {:.0f} mm leaves {:.0f} mm "
                                 "point protrusion/washers (v2's 30 mm shank "
                                 "could NOT span this stack)".format(
                                     bl[2] * 1000.0, DOUBLER[2] * 1000.0,
                                     RING_WALL_M * 1000.0,
                                     ATT_NUT_T * 1000.0, stack_min * 1000.0,
                                     att_l * 1000.0,
                                     (att_l - stack_min) * 1000.0),
                pairLoadkN=round(pair_load / 1000.0, 2),
                singleShearCapacitykN=round(cap / 1000.0, 2),
                utilisation=round(pair_load / cap, 3),
                boltsPerStation=ATT_BOLTS, boltSetKg=round(bolt_set_kg, 4),
                boltsT=round(bolt_set_kg * g["cords"] / 1000.0, 2),
                bondFilm="pad/ring bond film credited ZERO capacity",
                unknowns="laminate bearing, block local bending, "
                         "pull-through, contact/creep: UNKNOWN"),
            planePreloadKN=round(plane_kn, 1),
            stationPitchInnermostM=round(pitch, 3),
            stationPitchVsHardware="pitch {p:.3f} m at r_min vs block "
                                   "{b:.3f} m + 2 sockets {s:.3f} m".format(
                                       p=pitch, b=bl[0],
                                       s=2.0 * od) + (" — FITS"
                                                      if pitch > bl[0]
                                                      + 2.2 * od
                                                      else " — CHECK"),
            staticEqTensionkN=round(teq / 1000.0, 1),
            staticEqStress="UNKNOWN (cord strength UNKNOWN; no fibre "
                           "ultimate is borrowed for the UHMWPE-class cord)",
        )
        assert term[name]["stationPitchVsHardware"].endswith("FITS"), name
        hw_mass += (per_end["totalKg"] * g["ends"] + block_kg * g["cords"]
                    + doubler_kg * g["cords"])   # embedded cord in cordT
        attach_mass += bolt_set_kg * g["cords"]
        removed_lug_kg += g["ends"] * RT.LUG_KG
        # counterexample pins
        assert abs(tau_old / 1e6
                   - {"d60": 13.771544132,
                      "d180/11": 13.782540511}[name]) < 2e-6, (name, tau_old)
        assert abs(lg_req * 1000.0
                   - {"d60": 59.676691237,
                      "d180/11": 96.477783577}[name]) < 2e-6, (name, lg_req)
        # (scalar-probe values; their float path mixed the v1
        # JSON's rounded laEffM with the unrounded one — 6th-digit noise)
        assert abs(eta_v1
                   - {"d60": 0.992487726,
                      "d180/11": 0.991539174}[name]) < 5e-6, (name, eta_v1)
        # preload parity with the committed record
        rec_kn = cjson["geometry"]["families"][name]["pretensionPerPlaneKN"]
        assert abs(plane_kn - rec_kn) < 0.05, (name, plane_kn, rec_kn)

    # ------------------------------------------------------------------
    # 2. signed mixed-field taut window: chord basis + declared model
    # ------------------------------------------------------------------
    slack = {}
    PACK = {}                # per-family packet stash for the signed scan
    for name, step, off, planes, key in fams:
        g = C.family_geometry_full(name, step, off, planes, 155)
        sh = g["sinHalf"]
        phi = 2.0 * math.pi * step / N_LONG
        rmin = min(planes)
        Lmin = 2.0 * rmin * sh
        L_eff = term[name]["freeLength"]["lEffM"]
        L_eff_nt = term[name]["freeLength"]["lEffNoTransferM"]
        # exact-norm identity (clock independence) checked two ways
        gn = g_norm(step, Lmin)
        g0 = g_vec(step, Lmin, phi / 2.0)
        gn2 = math.sqrt(sum(v * v for v in g0))
        assert abs(gn - gn2) < 1e-12, (name, gn, gn2)
        for t_off in (0.0, 0.7, 2.1):
            gx = g_vec(step, Lmin, phi / 2.0 + t_off)
            assert abs(math.sqrt(sum(v * v for v in gx)) - gn) < 1e-12
        # worst single mode at Lmin (chord basis — carried record value)
        sm = max(((2.0 * sh * abs(math.cos(n * phi / 2.0)) / Lmin, n)
                  for n in MODES))
        # the adversarial packet STRETCHES its target (signed!)
        xs = [v / gn for v in g0]
        wxs = w_of(xs)     # GRID-SAMPLED amplitude (2^16 pts), labelled
        s_star = EPS0 / gn
        w_stretch_chord = s_star * wxs    # HISTORICAL chord-law scale (v1)
        # declared-law strain amplification for this family.
        # g_vec carries 1/L inside, so the declared law is exactly the
        # same functional built on L_eff: every strain scales by
        # f = Lmin/L_eff.  At the OLD chord scale the target reaches
        # T/T0 = 1 + f (already past 2*T0); its negative is already
        # slack (1 - f < 0); the scale hitting +-eps0 exactly is the
        # old scale / f.  These reproduce the review's algebraic
        # witnesses (computed there from saved rounded lengths).
        f_ratio = Lmin / L_eff
        wit = {"d60": (1.001463766, 0.998538374),
               "d180/11": (1.001760355, 0.998242738)}[name]
        assert abs(f_ratio - wit[0]) < 3e-7, (name, f_ratio)
        assert abs(1.0 / f_ratio - wit[1]) < 3e-7, (name, 1.0 / f_ratio)
        w_stretch_eff = w_stretch_chord / f_ratio   # declared-law scale
        resid_chord = (1.0 - term[name]["freeLength"]["etaV1ChordBasis"])
        # rigorous class bound, both bases (Cauchy-Schwarz + w lower bound)
        wb_chord = EPS0 / (math.sqrt(2.0) * gn)
        gn_eff = gn * Lmin / L_eff
        wb_eff = EPS0 / (math.sqrt(2.0) * gn_eff)
        assert wxs >= 1.0 / math.sqrt(2.0) - 1e-12
        assert wxs <= math.sqrt(11.0) + 1e-12
        # exact monotonicity that closes the plane dimension: for a cord
        # at radius r, g_eff_j(r,t).x = [L(r_min)/L_eff(r)] [g_j(r_min,t).x]
        # with L_eff increasing in r — asserted over the occupied planes
        # strictly above the innermost (its case is the definition; a
        # radius twin within 1e-9 of r_min is the same plane; 2e-6
        # absorbs the 6-dp rounding of the stored grip/l_ser)
        for r in sorted(planes):
            if r <= rmin + 1e-9:
                continue
            le_r = 2.0 * r * sh - term[name]["gripLgMm"] / 1000.0 \
                + 2.0 * term[name]["freeLength"]["lSerM"]
            assert le_r >= L_eff + 1e-6, (name, r, le_r, L_eff)
        # stash for the cross-family signed first-loss scan (below)
        PACK[name] = dict(xs=xs, wxs=wxs, L_eff=L_eff, step=step, phi=phi,
                          gn=gn, f=f_ratio, key=key, planes=planes,
                          T0kN=term[name]["T0kN"])
        # ---- signed n=5 first slack over occupied cords, both laws ----
        def n5(denomL):
            c5phi = math.cos(5.0 * phi / 2.0)
            out = {}
            for lbl, fn, sgn in (("+cos5", math.cos, 1.0),
                                 ("-cos5", math.cos, -1.0),
                                 ("+sin5", math.sin, 1.0),
                                 ("-sin5", math.sin, -1.0)):
                # cord a: k_a*W = 2 sh c5phi sgn fn(5 t_mid) * W ; slack
                # where k_a < 0 at W = eps0*L/|k_a| -> minimise over a
                best = None
                for a in range(N_LONG):
                    t_mid = 2.0 * math.pi * a / N_LONG + phi / 2.0
                    k = 2.0 * sh * c5phi * sgn * fn(5.0 * t_mid)
                    if k < 0.0:
                        wmm = EPS0 * denomL / (-k) * 1000.0
                        if best is None or wmm < best[0] - 1e-9:
                            best = (wmm, a)
                # tension extremes at first slack: slack cord -> 0; the
                # most-stretched cord of the same family at the same W
                wslack_m = best[0] / 1000.0
                tmax = 0.0
                for a in range(N_LONG):
                    t_mid = 2.0 * math.pi * a / N_LONG + phi / 2.0
                    k = 2.0 * sh * c5phi * sgn * fn(5.0 * t_mid)
                    tmax = max(tmax, k)
                t_up = E_SPOKE * win_a[key] * area / g["cords"] \
                    * (tmax * wslack_m / denomL)
                out[lbl] = dict(
                    slackMm=round(best[0], 6),
                    controllingStartMod31=best[1] % 31,
                    controllingPlane="innermost (denominator monotone in r; "
                                     "station phase set plane-independent)",
                    mostStretchedCordTkN=round(
                        (E_SPOKE * win_a[key] * area / g["cords"]
                         * EPS0 + t_up) / 1000.0, 2))
            return out
        n5_chord = n5(Lmin)
        n5_eff = n5(L_eff)
        n5_nt = n5(L_eff_nt)
        slack[name] = dict(
            rMinM=round(rmin, 4), LminM=round(Lmin, 4),
            phiDeg=round(math.degrees(phi), 3),
            gNormPerM=round(gn, 6),
            gNormMaxPlaneCords="all 155 cords of the innermost plane tie "
                               "(||g_j|| is t_mid-independent)",
            singleModeWorstN=sm[1],
            singleModeCoeffPerM=round(sm[0], 6),
            singleModeSlackChordBasisMm=round(EPS0 / sm[0] * 1000.0, 3),
            adversarialPacket="x* = g_j*/||g_j*|| centred on the cord "
                              "midpoint: SIGNED stretch identity on its "
                              "target (+eps0, T = 2*T0); the slack "
                              "adversary is -x* — first-loss results in "
                              "signedPacket below",
            adversarialWperNorm=round(wxs, 4),
            adversarialWperNormBasis="GRID-SAMPLED amplitude (2^16 theta "
                                     "points) of the unit-norm packet — "
                                     "a sampled estimate labelled as such; "
                                     "the exact two-sided bound for any "
                                     "unit-norm x is 1/sqrt(2) <= "
                                     "w(x) <= sqrt(11)",
            adversarialStretchDeclaredMm=round(w_stretch_eff * 1000.0, 3),
            adversarialStretchHistoricalChordMm=round(
                w_stretch_chord * 1000.0, 3),
            declaredLawAmplification=round(f_ratio, 9),
            declaredLawNote="every strain scales by Lmin/L_eff (g_vec "
                            "carries 1/L inside): at the historical chord "
                            "scale the target reaches T/T0 = "
                            "{:.6f} (past 2*T0) and its negative is "
                            "already slack ({:.6f}); the +-eps0 scale is "
                            "the chord scale / {:.6f}".format(
                                1.0 + f_ratio, 1.0 - f_ratio, f_ratio),
            residualAtV1ThresholdPct=round(resid_chord * 100.0, 4),
            classBoundChordBasisMm=round(wb_chord * 1000.0, 3),
            classBoundDeclaredModelMm=round(wb_eff * 1000.0, 3),
            classBoundNoTransferMm=round(
                EPS0 / (math.sqrt(2.0) * gn * Lmin / L_eff_nt) * 1000.0, 3),
            classBoundBasis="Cauchy-Schwarz |g.x| <= ||g|| ||x|| with "
                            "||x||_2 <= sqrt(2) w(x) — exact two-sided "
                            "CONTINUOUS norm relation on RADIAL coefficients "
                            "c, holds for EVERY field (no sampling)",
            endpointBound="|eps| <= w/r for the ideal chord model "
                          "(stronger than the modal bound)",
            n5FirstSlackChordBasis=n5_chord,
            n5FirstSlackDeclaredModel=n5_eff,
            n5FirstSlackNoTransfer=n5_nt,
            n5Method="5*theta quantises the 155 stations into 31 phases "
                     "(155/5); the controlling station is read off the "
                     "station topology — no field search; the v1 50.4 mm "
                     "evaluated the a=0 endpoint only (SUPERSEDED)",
        )
    # parity with the carried record value (I009 v2.1 / I015 bounds)
    assert abs(slack["d60"]["singleModeCoeffPerM"] - 0.141792) < 5e-7
    assert abs(slack["d60"]["singleModeSlackChordBasisMm"] - 14.105) < 0.002
    # counterexample pins (old chord law, v1 grips)
    n5c = slack["d180/11"]["n5FirstSlackChordBasis"]
    assert abs(n5c["+cos5"]["slackMm"] - 25.668698) < 2e-6
    assert n5c["+cos5"]["controllingStartMod31"] in (11, 12)
    assert abs(slack["d60"]["n5FirstSlackChordBasis"]["+cos5"]["slackMm"]
               - 26.797732) < 2e-6
    assert abs(n5c["-cos5"]["slackMm"] - 25.537001) < 2e-6
    assert n5c["-cos5"]["controllingStartMod31"] == 27

    # ------------------------------------------------------------------
    # 2b. SIGNED mixed-packet first loss on the declared law.  For
    # each family's adversarial packet the strain functional of EVERY
    # occupied cord is evaluated SIGNED (no abs) on that family's own
    # declared-law denominator: g_eff_j = g_vec(step, L_eff, t_a+phi/2).
    # The member set is finite and fully enumerated: 155 station phases
    # x both families' innermost planes; the plane dimension is closed
    # by the exact monotonicity asserted above (g_eff_j(r,t).x =
    # [L(r_min)/L_eff(r)] [g_j(r_min,t).x], L_eff increasing in r), so
    # the innermost plane maximises every projection.  First tension
    # loss is read from SIGNED tension T = T0(1 - w proj/eps0) under
    # the slack adversary -x*, never from |strain|.
    # ------------------------------------------------------------------
    first_loss = {}
    for pk, P in PACK.items():
        proj = {}
        for fam, Q in PACK.items():
            vals = []
            for a in range(N_LONG):
                gj = g_vec(Q["step"], Q["L_eff"],
                           2.0 * math.pi * a / N_LONG + Q["phi"] / 2.0)
                vals.append(sum(gj[i] * P["xs"][i] for i in range(NMOD)))
            proj[fam] = vals
        # the first cord to lose tension: max SIGNED projection overall
        loser_fam = max(proj, key=lambda f: max(proj[f]))
        vals = proj[loser_fam]
        mx = max(vals)
        a_lo = vals.index(mx)
        w_first = EPS0 / mx                       # exact, unit-norm packet
        # remaining tensions at first loss, per family (most stretched)
        rem = {}
        for fam, Q in PACK.items():
            vv = proj[fam]
            mn_f, mx_f = min(vv), max(vv)
            t0 = Q["T0kN"]
            rem[fam] = dict(
                mostStretchedCordTkN=round(t0 * (1.0 - mn_f / mx), 3),
                nearestSlackCordTkN=round(t0 * (1.0 - mx_f / mx), 3),
                signedTowardsSlack999=sum(
                    1 for v in vv if v >= 0.999 * mx),
                signedTowardsSlack90=sum(1 for v in vv if v >= 0.9 * mx),
                signedStretch90=sum(1 for v in vv if v <= -0.9 * mx),
            )
        first_loss[pk] = dict(
            packet="-x* (the slack adversary of family {})".format(pk),
            firstLoser="family {} innermost plane, station {} of 155 "
                       "(t = 2 pi a/155 + phi/2)".format(loser_fam, a_lo),
            firstLoserFamily=loser_fam, firstLoserStation=a_lo,
            firstLoserIsPacketTarget=(loser_fam == pk and a_lo == 0),
            firstLossVectorNormMm=round(w_first * 1000.0, 3),
            firstLossAmplitudeSampledMm=round(w_first * P["wxs"] * 1000.0,
                                              3),
            firstLossAmplitudeBasis="vector-norm scale is EXACT; the "
                                    "physical amplitude is the GRID-"
                                    "SAMPLED w_of of the scaled packet; "
                                    "its exact continuous bound is "
                                    "[w/sqrt(2), sqrt(11) w]",
            targetTensionAtHistoricalChordScaleTkN=round(
                P["T0kN"] * (1.0 + P["f"]), 3),
            targetTT0AtHistoricalChordScale=round(1.0 + P["f"], 9),
            remainingCords=rem,
            method="finite occupied-member enumeration, SIGNED: 155 "
                   "station phases x both families' innermost planes; "
                   "plane dimension closed by the asserted monotonicity; "
                   "no abs() anywhere; first loss from signed tension; "
                   "the packet attains the Cauchy-Schwarz equality "
                   "proj = ||g_eff|| ||x|| on its family, so "
                   "firstLossVectorNormMm = eps0/gn_eff exactly and the "
                   "sampled first-loss amplitude equals the declared-law "
                   "stretch scale (same +-eps0 threshold)",
        )
        slack[pk]["signedPacket"] = first_loss[pk]

    # ------------------------------------------------------------------
    # 3. the full known bill (old parts removed once, new charged once)
    # ------------------------------------------------------------------
    bom15 = cjson["bom"]
    sockets_t = sum(term[f]["socketsT"] for f, *_ in fams)
    blocks_t = sum(term[f]["blocksT"] for f, *_ in fams)
    doublers_t = sum(term[f]["doublersT"] for f, *_ in fams)
    attach_t = sum(term[f]["attachment"]["boltsT"] for f, *_ in fams)
    removed_lug_t = removed_lug_kg / 1000.0
    cord_t, clips_t = bom15["cordT"], bom15["clipsT"]
    # double-count pin: the v2 potted-tow line double-counted (the embedded
    # runs lie INSIDE the anchor-centre chords the cord line prices)
    assert abs(tow_v2_t - 0.34) < 0.011, tow_v2_t
    hardware_t = (cord_t + clips_t + sockets_t + blocks_t + doublers_t
                  + attach_t)
    spokes_new = hardware_t * (1.0 + RT.ASSEMBLY)
    delta = spokes_new - b15["spokesLineT"]
    total_new = b15["totalT"] + delta
    # the x1.5 station-hardware scenario takes the 5% assembly on
    # the INCREMENT (v1 omitted 0.69225 t of the v1 bill)
    x15_increment = 0.5 * (sockets_t + blocks_t + doublers_t + attach_t) \
        * (1.0 + RT.ASSEMBLY)
    bill = dict(
        cordT=cord_t, clipsT=clips_t,
        socketsT=round(sockets_t, 2), anchorBlocksT=round(blocks_t, 2),
        doublerPadsT=round(doublers_t, 2),
        attachmentBoltsT=round(attach_t, 2),
        assemblyT=round(hardware_t * RT.ASSEMBLY, 2),
        removedIdealLugT=round(removed_lug_t, 2),
        removedLugAssemblyT=round(removed_lug_t * RT.ASSEMBLY, 2),
        spokesLineOldT=b15["spokesLineT"], spokesLineNewT=round(spokes_new, 2),
        deltaT=round(delta, 1),
        totalT=round(total_new, 1),
        marginSLT=round(b15["marginSLT"] - delta, 1),
        margin2500T=round(b15["margin2500T"] - delta, 1),
        stackedStationHardwareX1_5_SLT=round(
            b15["marginSLT"] - delta - x15_increment, 1),
        x15IncrementT=round(x15_increment, 2),
        accounting="ONE boundary: anchor centre = grip back face, "
                   "so anchor-centre chord = free span + 2 embedded "
                   "(nose+grip) runs; cordT prices FULL anchor-centre "
                   "chords and therefore already contains the potted "
                   "embedded cord — the v2 {:.2f} t potted-tow line was a "
                   "double count and is REMOVED; potting resin is inside "
                   "socketsT; studs/seats beyond the anchor centre are "
                   "inside socketsT and the series spring L_ser; old "
                   "0.35 kg ideal-lug line removed ONCE (inside the "
                   "spokesLineOldT comparison); sockets, blocks, pads and "
                   "attachment bolts charged ONCE; ring members, fixed "
                   "members and gas unchanged".format(tow_v2_t),
        knownSubtotal="attachment bolts are sized on metallic single "
                      "shear (traceable); laminate bearing, block local "
                      "bending and pull-through are UNKNOWN — the bill is "
                      "a known subtotal with those unresolved, not a "
                      "qualified all-up margin",
    )

    # counterexample on the v1 bill composition
    v1_sbd = 18.67 + 6.18 + 2.85          # v1 sockets+blocks+doublers t
    assert abs(0.5 * v1_sbd * RT.ASSEMBLY - 0.69225) < 0.002

    # ------------------------------------------------------------------
    # 4. SF1.2 adverse case against the FIXED completed I015 baseline
    # ------------------------------------------------------------------
    w12 = I005.World(1.2)
    win12 = rec["worlds"]["sf1.2"]["bestFeasible"]
    a12 = win12["point"]["alloc"]
    sp12 = w12.spokes_t(a12)
    f12 = [("d60", 52, 59.226, pe, "a_d60", "d60"),
           ("d20", 69, 19.742, po, "a_d20", "d180/11")]
    hw12 = lug12 = 0.0
    for name, step, off, planes, key, bkey in f12:
        g = C.family_geometry_full(name, step, off, planes, 155)
        sec = a12[key] * area / g["cords"]
        dia = 2.0 * math.sqrt(sec / math.pi)
        T_fit = 2.0 * E_SPOKE * sec * EPS0 * FITTING
        bore = BORE_K * dia
        Lg = math.ceil(T_fit / (math.pi * dia * TAU_BOND) * 1000.0) / 1000.0
        od = BODY_OD_K * bore
        body_l = Lg + 2.0 * NOSE_M
        bl = BLOCK[bkey]
        # per-family dimensioned shank; no tow line (the
        # embedded run is inside the anchor-centre chord hw12 prices)
        bolt_set_kg = ATT_BOLTS * (
            math.pi / 4.0 * ATT_D ** 2 * ATT_L_M[bkey] * TI_RHO
            + NUT_FULL * math.pi / 4.0 * ATT_NUT_AF ** 2 * ATT_NUT_T * TI_RHO)
        per_end = (math.pi / 4.0 * (od ** 2 - bore ** 2) * body_l * TI_RHO
                   + (math.pi / 4.0 * (bore ** 2 - dia ** 2) * Lg
                      + math.pi / 4.0 * bore ** 2 * NOSE_M) * EPOXY_RHO
                   + math.pi / 4.0 * (STUD_D_K * dia) ** 2 * STUD_L_K * dia
                   * TI_RHO
                   + NUT_FULL * math.pi / 4.0 * (NUT_OD_K * dia) ** 2
                   * NUT_T_K * dia * TI_RHO)
        hw12 += g["totalLenM"] * sec * RHO_SPOKE / 1000.0
        hw12 += g["crossings"] * RT.CLIP_KG / 1000.0
        hw12 += per_end * g["ends"] / 1000.0
        hw12 += bl[0] * bl[1] * bl[2] * TI_RHO * g["cords"] / 1000.0
        hw12 += DOUBLER[0] * DOUBLER[1] * DOUBLER[2] * LAM_RHO \
            * g["cords"] / 1000.0
        hw12 += bolt_set_kg * g["cords"] / 1000.0
        lug12 += g["ends"] * RT.LUG_KG / 1000.0
    # the FIXED baseline: I015's completed d60+d20 line, rebuilt here and
    # pinned to the committed budgets (delta12 == the committed 9.2)
    cord12 = clips12 = 0.0
    for name, step, off, planes, key, _bkey in f12:
        g = C.family_geometry_full(name, step, off, planes, 155)
        sec = a12[key] * area / g["cords"]
        cord12 += g["totalLenM"] * sec * RT.RHO_SPOKE / 1000.0
        clips12 += g["crossings"] * RT.CLIP_KG / 1000.0
    b12_fin = (cord12 + lug12 + clips12) * (1.0 + RT.ASSEMBLY)
    delta12_base = b12_fin - sp12
    assert abs((win12["totalT"] + delta12_base) - 2546.1) < 0.05
    assert abs((win12["marginSLT"] - delta12_base) + 296.3) < 0.05
    spokes12 = hw12 * (1.0 + RT.ASSEMBLY)
    delta12 = spokes12 - b12_fin
    sf12 = dict(
        point=win12["which"],
        baseline="CORRECTED completed R3-I015 case, pinned: before "
                 "2536.9 -> after 2546.1 t, margin -296.3 "
                 "(budgets.sf12Completed in the corrected R3-I015 record)",
        baselineSpokesT=round(b12_fin, 2),
        baselineDeltaT=round(delta12_base, 2),
        afterSpokesT=round(spokes12, 2),
        deltaVsCompletedT=round(delta12, 1),
        afterT=round(b12c["afterT"] + delta12, 1),
        afterMarginSLT=round(b12c["afterMarginSLT"] - delta12, 1),
        inheritedCompletionT=round(delta12_base, 1),
        verdict="STILL FAILS at sea level (mass failure inherited and "
                "unchanged in kind); the delta is measured against the "
                "COMPLETED baseline — the +9.2 t completion change is "
                "inherited, not new termination mass",
    )

    # ------------------------------------------------------------------
    # 5. energy / pressure-work normalisation
    # ------------------------------------------------------------------
    Mf, Kf, qrf, scf = C.build_M(w, win_a, n_cords=155)
    lam_fin, _, _ = C.eig_min(Mf)
    scalar = min((qrf[n] + sum(E_SPOKE * win_a.get("a_" + f["name"], 0.0)
                               * f["f"][n] / (n * n - 1.0)
                               for f in w.fam
                               if win_a.get("a_" + f["name"], 0.0) > 0.0))
                 * scf for n in MODES)
    assert abs(lam_fin - scalar) < 1e-9
    # the drawn termination is STIFFER than the declared lug AND than
    # the pin-jointed ideal (eta > 1 on the consistent law): rebuild
    # the compliant-state coupled margin with the drawn eta per family
    a_drawn = dict(win_a)
    for name, step, off, planes, key in fams:
        eta_new = term[name]["freeLength"]["etaDrawnMeanCord"]
        assert eta_new > 1.0, (name, eta_new)
        a_drawn[key] = win_a[key] * eta_new
    M_dr, _, _, _ = C.build_M(w, a_drawn, n_cords=155)
    lam_dr, _, res_dr = C.eig_min(M_dr)
    assert res_dr < 1e-9
    assert lam_dr > lam_fin  # beyond-rigid: reported, NOT claimed
    energy = dict(
        marginMatrix="M = K KD/(P_ATM SF); lambda_min(M) worst margin over "
                     "all fields of unit MODAL norm ||y|| = 1, "
                     "sum_n (n^2-1)(c_n^2+s_n^2) = 1",
        yNormMapping="this unit's slack/norm work is on RADIAL "
                     "coefficients c (cos+sin pairs); the I015 eigen "
                     "machinery uses y = sqrt(D) c, D_nn = n^2-1: y_c5 = 1 "
                     "maps to c5 = 1/sqrt(24) = 0.204124145232 — "
                     "cross-basis comparisons carry the sqrt(D) mapping",
        pressureWork="folded into the licensed constant KD/(P_ATM SF) = "
                     + "{:.11e}".format(KD / (P_ATM * 1.0)) + " (SF=1); "
                     "PARITY to the licensed scalar law, not an "
                     "independently qualified pressure-loaded structural "
                     "model",
        pureModeCheck="the pure-mode check is numerical parity with the "
                      "committed orientation_phase, NOT a physical "
                      "measurement; pure-mode blocks do NOT uniquely "
                      "determine the cross entries (diag(a,b) and the "
                      "sqrt(ab)/2 off-diagonal matrix are both positive "
                      "definite with identical pure-mode restrictions) — "
                      "the cross-mode extension is an EXPLICIT ASSUMPTION "
                      "carried from I015, pending independent member "
                      "kinematics/energy normalisation",
        coupledMinEqualsScalar=round(lam_fin, 9),
        drawnEtaCoupledMin=round(lam_dr, 9),
        drawnEtaNote="rebuilt with the drawn per-family eta on the ONE "
                     "consistent law (eta = mc/(L_free_mean + "
                     "2 L_a) > 1 — v2's eta = mc/(mc + 2 L_a) treated "
                     "the whole mean chord as free cord and its "
                     "1.000438088 is SUPERSEDED): the drawn chain is "
                     "stiffer than the pin-jointed ideal, so the "
                     "compliant-state coupled margin {:.9f} sits just "
                     "ABOVE the licensed rigid {:.7f} — beyond-rigid is "
                     "an extrapolation of the same linear model and is "
                     "NOT claimed as a qualification; the quotable "
                     "margin remains the licensed rigid scalar".format(
                         lam_dr, cjson["response"]["lambdaMinRigid"]),
        licensedQuotableMargin=round(lam_fin, 9),
    )

    # load-path limit (whole-vehicle, retained as UNKNOWN)
    load_path = dict(
        staticEqTensionOuterPlaneKN={f: term[f]["staticEqTensionkN"]
                                     for f, *_ in fams},
        staticEqUtilisation="UNKNOWN — the UHMWPE-class cord has no "
                            "qualified strength in this record and no "
                            "fibre ultimate is borrowed",
        i023CrossReference="R3-I023 (same checkout, delivered, unreviewed) "
                           "reads these teq magnitudes as the force the "
                           "web would need bypassing the ring box and "
                           "supersedes them as a load path; the honest "
                           "static cord demand there is the pretension "
                           "itself (6.8/17.8 kN)",
        verdict="the record's model excludes the membrane that carries "
                "global pressure equilibrium (bounds.membrane) and "
                "licenses only the stability margin; the termination is "
                "sized to the model's own tension quantities and the "
                "vehicle-level pressure load path remains UNKNOWN",
    )

    # ------------------------------------------------------------------
    # 6. sensitivities and material ledger
    # ------------------------------------------------------------------
    tau_table = {}
    for name, step, off, planes, key in fams:
        g = C.family_geometry_full(name, step, off, planes, 155)
        sec = win_a[key] * area / g["cords"]
        dia = 2.0 * math.sqrt(sec / math.pi)
        T_fit = 2.0 * E_SPOKE * sec * EPS0 * FITTING
        bore = BORE_K * dia
        od = BODY_OD_K * bore
        stud_d, stud_l = STUD_D_K * dia, STUD_L_K * dia
        fixed_kg = (math.pi / 4.0 * (STUD_D_K * dia) ** 2 * STUD_L_K * dia
                    * TI_RHO
                    + NUT_FULL * math.pi / 4.0 * (NUT_OD_K * dia) ** 2
                    * NUT_T_K * dia * TI_RHO)
        rows = []
        base_end = None
        for tau_mpa in (8.0, 12.0, 20.0):
            lg = math.ceil(T_fit / (math.pi * dia * tau_mpa * 1e6)
                           * 1000.0) / 1000.0
            body_l = lg + 2.0 * NOSE_M
            end = (math.pi / 4.0 * (od ** 2 - bore ** 2) * body_l * TI_RHO
                   + (math.pi / 4.0 * (bore ** 2 - dia ** 2) * lg
                      + math.pi / 4.0 * bore ** 2 * NOSE_M) * EPOXY_RHO
                   + fixed_kg)
            if abs(tau_mpa - 12.0) < 1e-9:
                base_end = end
            rows.append((tau_mpa, lg * 1000.0, end))
        tau_table[name] = dict(
            rows=[dict(tauMPa=r[0], gripMm=round(r[1], 1),
                       perEndKg=round(r[2], 4),
                       massOverBase=round(r[2] / base_end, 6))
                  for r in rows],
            note="Lg ~ 1/tau exactly (150%/60% for 12->8/20 MPa before "
                 "the mm ceiling); stud, nut and nose masses are FIXED "
                 "so socket mass does not scale with grip length; tau "
                 "is an UNVERIFIED assumed bond property — this is "
                 "geometric sensitivity only",
        )

    material = dict(
        cord=dict(
            identity="UHMWPE-class (Dyneema-type) per its source "
                     "documentation tools/ship_scoping.py:138-139",
            EPa=70e9, rhoKgM3=970.0,
            units="key is EPa = 70e9 Pa = 70 GPa (v2's EMpa key "
                  "held the Pa value behind an MPa label — relabelled, "
                  "numerics unchanged)",
            provenance="ASSUMED inherited model inputs, creep UNVERIFIED",
            strength="UNKNOWN — no fibre ultimate is borrowed"),
        terminationMetal=dict(
            identity="Ti-6Al-4V", EPa=TI_E, rhoKgM3=TI_RHO,
            sigmaYPa=TI_SIGMA_Y,
            provenance="public datasheet values"),
        potResin=dict(rhoKgM3=EPOXY_RHO, designShearPa=TAU_BOND,
                      provenance="ASSUMED design value, unverified"),
        laminate=dict(identity="T700S/epoxy Vf 0.6 (rings, rails, pads)",
                      provenance="record-priced where sourced"),
    )

    limits = dict(
        otherModes="n outside 2..12 (incl. n=1 and bay-local): outside the "
                   "field family; unchanged from the record",
        postSlack="beyond first slack the tension-only foundation is "
                  "unmodelled; no redistribution solver is run",
        largeDisplacement="first-order linearised in u/r; the stud thread "
                          "adjustment covers installation tolerance, not "
                          "geometric nonlinearity",
        membrane="global pressure equilibrium excluded (see loadPath)",
        transferCentroid="the mid-grip transfer centroid is a DECLARED "
                         "assumption; the no-transfer variant bounds the "
                         "taut window from above (both reported)",
        bondCreepSensitivity="tau 8-20 MPa -> grips 150%/60% before "
                             "rounding (table in sensitivities); mass "
                             "moves less (fixed stud/nut/nose terms)",
        stationHardwareSensitivity="block+doubler+attachment geometry is "
                                   "a bounded assumption; the x1.5 "
                                   "scenario is priced WITH its assembly "
                                   "share in the bill",
        attachmentUnknowns="laminate bearing, block local bending, "
                           "pull-through, bond-film capacity, creep and "
                           "contact behaviour: UNKNOWN",
        sampledAmplitudes="w_of amplitudes are GRID-SAMPLED (2^16 theta "
                           "points) and labelled as sampled wherever "
                           "reported; the continuous statements are the "
                           "two-sided class bounds and the exact finite "
                           "member enumeration",
        accountingBoundary="anchor centre = grip back face: the "
                           "embedded (nose+grip) cord is INSIDE the "
                           "anchor-centre chord and inside cordT; no "
                           "separate tow line exists anywhere (bill, x1.5, "
                           "SF1.2 all use the same boundary)",
        boltStack="the dimensioned stack is block + doubler pad + ring "
                  "wall + backing nut (+ protrusion); shank lengths "
                  "45/50 mm are priced for it; laminate bearing/"
                  "bending/pull-through remain UNKNOWN",
    )
    bounds = dict(
        cpu="single pure-Python process; measured wall/RSS receipts live "
            "in the unit evidence file (not embedded — the JSON is "
            "deterministic)",
        declared="analytic + <=22-coordinate small-matrix work only; no "
                 "solver, sweep, optimizer or review family; measured "
                 "run < 1 s wall, < 25 MB RSS",
    )
    out = dict(
        unit="R3-I019", rev="v3.1",
        date="2026-10-14",
        dependency="corrected R3-I015 record (record imports); "
                   "v3.1 follows this unit's v3 correction — v3 repairs "
                   "the v2 spring model (one signed installed spring "
                   "model + signed mixed-packet first loss), the bolt "
                   "stack (buildable, dimensioned) and ONE cord "
                   "accounting boundary, and the Pa units label",
        construction="epoxy-potted titanium socket with a threaded "
                     "adjustment stud and jam nut, per-station titanium "
                     "anchor block on a carbon-laminate doubler pad, "
                     "bolted to the ring wall by 3 x M10 Ti through-"
                     "bolts with internal backing nuts",
        compatibility="the cord is UHMWPE-CLASS (Dyneema-type) with "
                      "ASSUMED inherited inputs; swage compatibility is "
                      "creep/slip-sensitive and NOT QUALIFIED (neither "
                      "retained nor sized); potting compatibility is an "
                      "ASSUMED construction on an ASSUMED 12 MPa design "
                      "bond shear — not a qualified termination",
        materialLedger=material,
        slack=slack, termination=term, bill=bill, sf12=sf12,
        sensitivities=dict(bondShear=tau_table),
        preload=dict(
            perCordT0kN={f: term[f]["T0kN"] for f, *_ in fams},
            perPlaneTotalsKN={f: term[f]["planePreloadKN"] for f, *_ in fams},
            statement="T0 = E a eps0 set as stud force at installation on "
                      "the declared spring model (increment dT = EA dL/"
                      "(L_free+2 L_a)); per-plane totals asserted equal "
                      "to the committed record; the physical pressure "
                      "demand reference (P 2 pi R bay, no KD) is "
                      "unchanged and KD=0.65 remains a CAPACITY "
                      "knockdown — preload and demand stay separate "
                      "books",
        ),
        loadPath=load_path, energy=energy, limits=limits, bounds=bounds,
        verdict=dict(
            scope="frozen model; licensed law + its EXPLICIT cross-mode "
                  "assumption; taut window stated on ONE declared spring "
                  "model with the no-transfer bound alongside; the "
                  "chord-basis v1 numbers retained as labelled "
                  "counterexample pins",
            firstSlack="signed n=5 first slack over occupied cords "
                       "(declared model): d180/11 "
                       "{:.3f} mm, d60 {:.3f} mm — the v1 50.4 mm "
                       "(a=0 endpoint) is superseded".format(
                           min(v["slackMm"] for v in
                               slack["d180/11"]
                               ["n5FirstSlackDeclaredModel"].values()),
                           min(v["slackMm"] for v in
                               slack["d60"]
                               ["n5FirstSlackDeclaredModel"].values())),
            mixedPacket="signed mixed-packet first loss, both packets: "
                        "the d60 adversary's first loser is {}/station "
                        "{} at {:.3f} mm vector norm ({:.3f} mm sampled "
                        "amplitude); the d180/11 adversary's first "
                        "loser is {}/station {} at {:.3f} mm vector "
                        "norm ({:.3f} mm sampled amplitude). Both are "
                        "the coefficient-norm Cauchy-Schwarz equality "
                        "case, which fixes the vector-norm scales, NOT "
                        "physical-amplitude sharpness: the sampled "
                        "amplitudes exceed the sufficient class bounds "
                        "and are themselves lower bounds on the "
                        "continuous maxima. Remaining tensions per "
                        "family in slack.*.signedPacket".format(
                            first_loss["d60"]["firstLoserFamily"],
                            first_loss["d60"]["firstLoserStation"],
                            first_loss["d60"]["firstLossVectorNormMm"],
                            first_loss["d60"]["firstLossAmplitudeSampledMm"],
                            first_loss["d180/11"]["firstLoserFamily"],
                            first_loss["d180/11"]["firstLoserStation"],
                            first_loss["d180/11"]["firstLossVectorNormMm"],
                            first_loss["d180/11"]["firstLossAmplitudeSampledMm"]),
            weakestAssumption="the 12 MPa design bond shear and the "
                              "mid-grip transfer centroid are ASSUMED "
                              "(grip length, socket mass and the taut "
                              "window scale with them); station hardware "
                              "geometry is a bounded assumption",
            nextChange="qualify the cord material record and the bond "
                       "value; declare the field class the vehicle must "
                       "resist and re-state the taut window for that "
                       "restricted class",
            massVerdict="SL margin stays positive with the real "
                        "termination (+{:.1f} t vs the completed I015 "
                        "line); 2500 m and SF1.2 remain failures as "
                        "before".format(delta),
        ),
    )
    op = os.path.join(HERE, "termination.json")
    with open(op, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote", op)
    print(json.dumps(dict(
        grips={f: term[f]["gripLgMm"] for f, *_ in fams},
        eta={f: term[f]["freeLength"]["etaDrawnMeanCord"]
             for f, *_ in fams},
        f_ratio={f: slack[f]["declaredLawAmplification"]
                 for f, *_ in fams},
        first_loss={f: dict(loser=first_loss[f]["firstLoserFamily"]
                            + "/" + str(first_loss[f]["firstLoserStation"]),
                            mm=first_loss[f]["firstLossVectorNormMm"])
                    for f, *_ in fams},
        n5_declared={f: min(v["slackMm"] for v in
                            slack[f]["n5FirstSlackDeclaredModel"].values())
                     for f, *_ in fams},
        drawn_coupled=energy["drawnEtaCoupledMin"],
        boltsT={f: term[f]["attachment"]["boltsT"] for f, *_ in fams},
        bill_deltaT=bill["deltaT"], marginSLT=bill["marginSLT"],
        x15_SLT=bill["stackedStationHardwareX1_5_SLT"],
        sf12=sf12["afterMarginSLT"]), indent=1)[:1600])


if __name__ == "__main__":
    main()
