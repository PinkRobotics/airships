"""R3-I023 — the signed static pressure load path of the vacuum hull.

Question: what carries the atmospheric pressure resultant, and what does the
cord web actually see? The earlier termination unit divided the outermost
band load by the cord web's radial share and reported ~234 kN/cord at 98% of
a tow ultimate — a SCALAR DIVISION. This unit builds the path itself, signed,
from the record's own members: film strip -> barrel rings + inner rail with
theta webs -> end caps and longerons, and the cord web as in-plane stability
hardware whose static duty is its own pretension equilibrium.

Rev v1.3 (consolidated correction of the sole first review, eight
findings, all addressed in this file and the README):

  * the inner rail is the RETAINED replacement section alone (the record's
    allocated a_i, 1 453.5 mm2) — the v1.2.x smeared box double-credited the
    pre-replacement skeleton section on top of it (2 507 mm2 total). Every
    stiffness, load-share, utilisation and slack number below moves with
    that fix; the v1.2.2 values survive only as labelled historical pins.
  * the claimed CLOSED common-strain box equilibrium is WITHDRAWN: the
    connected theta webs also strain under the asserted common contraction,
    and the balance of web pulls against inner-ring cuts leaves a large
    unresolved inward resultant per station (diagnostic below). The strain,
    service-force and slack outputs are therefore CONDITIONAL on the
    declared common-strain kinematic model — model diagnostics, not
    physical predictions; the retained construction's compatibility/
    force balance is UNSOLVED here (see modelStatus in the record).
  * the exterior tributary accounting is corrected: the envelope is a
    112 m cylinder plus two hemispherical caps — the caps are EXACTLY HALF
    the film area, not a 12% polar remainder, and the earlier band sum used
    inner cord-plane radii, not exterior film radii.
  * the pump-down reset claim is WITHDRAWN: restoring tension through the
    existing studs needs combined take-up of order chord x strain
    (0.58 m at the longest representative cord under the declared model's
    own barrel strain) against 0.254 m of combined stud LENGTH before any
    thread engagement — the existing-stud reset is UNAVAILABLE, and any
    install-after-evacuation or added-travel construction is UNQUALIFIED
    with UNKNOWN parts and mass.
  * the fitting value 2*T0*1.3 is a design DEMAND (it sized the bond
    grip), never a derived stud/thread/nut capacity: every stud-cover and
    capacity-shortfall verdict is removed; stud capacity is UNKNOWN.
  * the installation/pressure-loss identities carry their compliance
    feedback: the unrestrained installation force and the taut pressure
    decrement divide by (1+beta*kappa); the restrained (undeformed-rail)
    set load is named as the different book it is.
  * the film strip is a circular ONE-WAY membrane under uniform normal
    pressure: its tension is CONSTANT p*R_tr = 53.8 kN/m along the arc (the
    26.9 kN/m half-value is the two-curvature pricing reference, not this
    strip's trough tension); each support also receives the axial
    component T*cos(alpha) = 15p/32 = 47.5 kN/m, which cancels between
    adjacent strips and is exported UNCANCELLED at the cap edges.
  * the historical 234.0/205.8 kN magnitudes are retained ONLY as a signed,
    mechanically inadmissible hypothetical: with inward pressure and inward
    cord pulls, direct web resistance would require NEGATIVE cord tension —
    compression these cords cannot supply. It is not an alternative tensile
    load path.

Inputs (unchanged bytes, hash-guarded at load): the R3-I019 v3.1
termination record and the corrected R3-I015 coupled record. The kinematic
law is unchanged: a box contraction eps shortens the ANCHOR-CENTRE chord by
eps*L_chord, the cord strains on L_eff = L_chord - Lg + 2*l_ser, so
kappa = L_chord/L_eff (~1.0015) and the held strain after a contraction eps
is (eps_set - kappa*eps)/(1+beta*kappa) — beta the cord->rail->cord strain
loop gain; eps_set is the installed set strain (compatible hold set
eps0*(1+beta*kappa), nominal flat set eps_set = eps0, eps0 the fixed
nominal 0.002), so the eps0 form names the nominal flat-set case.
The no-transfer variant is reported as the bound.

Convention (signed throughout): outward normal n; delta_p = p_in - p_out =
0 - 101325 = -101325 Pa — the vacuum lineage's INWARD traction. The record's
P_ATM magnitudes are |delta_p|. Nothing here turns the positive magnitude
into internal overpressure, a helium envelope or an outward reaction.

Bounds: one pure-Python process, analytic free bodies + 1x1 solves, no
matrix over 22 coordinates, no solver/sweep/optimizer/FEA, no model fit.
Run:  python3 research/design-iterations/R3-I023/loadpath.py   (writes
loadpath.json next to this file). The v1.3 evidence records ONE bounded
execution; no determinism re-run is claimed for it.
"""

import hashlib
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "R3-I004"))
sys.path.insert(0, os.path.join(HERE, "..", "R3-I005"))
sys.path.insert(0, os.path.join(HERE, "..", "R3-I009"))

from net import planes_of            # noqa: E402  (R3-I004 record)
import alloc as I005                 # noqa: E402  (R3-I005 record)
import routing as RT                 # noqa: E402  (R3-I009 record)

SHIP0 = I005.SHIP0
P_ATM = I005.P_ATM                   # 101325 Pa, |delta_p|
KD = I005.KD                         # 0.65 capacity knockdown (buckling only)
E_SPOKE = RT.E_SPOKE                 # 70 GPa  (ASSUMED, inherited pair)
RHO_SPOKE = RT.RHO_SPOKE             # 970 kg/m3 (ASSUMED, inherited pair)
EPS0 = RT.EPS_PRETENSION            # 0.002 declared pretension strain
FITTING = SHIP0["spokeFitting"]      # 1.3 fitting factor
N_LONG = RT.N_LONG                   # 155 anchor stations
BAY = SHIP0["bayM"]                  # 2.0 m bay pitch
S_R = SHIP0["ringPitchM"]            # 0.5 m barrel ring pitch
E_LAM = I005.MAT["T700_LAM"]["E"]    # 135 GPa (representative)
SIG_C = I005.MAT["T700_LAM"]["sigmaCompression"]      # 1.45 GPa SOURCED
SIG_T = I005.MAT["T700_LAM"]["sigma"]                 # 2.86 GPa SOURCED
RHO_LAM = I005.MAT["T700_LAM"]["rho"]                 # 1600

TERM_PATH = os.path.join(HERE, "..", "R3-I019", "termination.json")
COUP_PATH = os.path.join(HERE, "..", "R3-I015", "coupled.json")


def _sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# dependency guards: this unit consumes the CORRECTED records, byte-exact.
# R3-I019 v3.1 (commit 3c0305db, directly on the v3 82ce49c2): material
# ledger UHMWPE-class (EPa key), grips 60/97, dimensioned bolted attachment
# (M10 45/50 mm shanks), ONE cord accounting boundary (no separate tow line),
# bill spokes 245.42 t. R3-I015 corrected (736180fd).
TERM_SHA = "0fb204a2362f17f342b1582fb2e41981f7207402b509db81ba3bbf5c38a2cc6a"
COUP_SHA = "6090c36e6b4479c5c81bfd47d8ebb9cadd95244ed8bc6fad3e5b5b39b71e620c"
REV = "v1.3-consolidated-correction"
assert _sha256(TERM_PATH) == TERM_SHA, "R3-I019 termination.json is not the v3.1 bytes"
assert _sha256(COUP_PATH) == COUP_SHA, "R3-I015 coupled.json drifted"
TERM = json.load(open(TERM_PATH, encoding="utf-8"))
COUP = json.load(open(COUP_PATH, encoding="utf-8"))
assert TERM["rev"] == "v3.1" and TERM["dependency"].startswith("corrected R3-I015 record (record imports);")
for _n, _lg in (("d60", 60.0), ("d180/11", 97.0)):
    assert TERM["termination"][_n]["gripLgMm"] == _lg
assert abs(TERM["bill"]["spokesLineNewT"] - 245.42) < 0.005
# the binding n=5 margin and the drawn-state margin, BOUND from the records
# (v1.0 carried these as prose literals; no spectrum is rerun here)
N5_RIGID = COUP["response"]["equalsScalarMin"]            # 1.000811
assert COUP["response"]["limitingMode"].startswith("n=5")
N5_DRAWN = TERM["energy"]["drawnEtaCoupledMin"]           # 1.000874 — BEYOND the
# licensed rigid (the v3 consistent spring law has eta > 1): reported, NOT
# claimable — the quotable tolerance is the rigid licensed value below
TOL_RIGID_PCT = 100.0 * (N5_RIGID - 1.0)                  # 0.081%
TOL_DRAWN_PCT = 100.0 * (N5_DRAWN - 1.0)                  # 0.087% (beyond-rigid)

# ---------------------------------------------------------------------
# 1. the SF1.0 construction, from the record's own constructors
# ---------------------------------------------------------------------
W = I005.World(1.0)
G, WALL, SKEL = W.g, W.wall, W.base["skeleton"]
R_ENV, R_IN, DEPTH = G["R"], G["rIn"], G["depthM"]
WIN = json.load(open(os.path.join(HERE, "..", "R3-I005", "alloc.json"),
                     encoding="utf-8"))["worlds"]["sf1.0"]["bestFeasible"]["point"]
A_I_ADD = WIN["alloc"]["a_i"]                      # 1.45345e-3 m2 per ring

RING = WALL["ring"]
A_RING, N_RING_DEMAND = RING["A"], RING["demandN"]
RING_CAP = RING["sigmaCapPa"] * A_RING             # Euler-governed capacity
LONG = SKEL["longeron"]
A_LONG, N_LONG_DEMAND = LONG["A"], LONG["demandN"]
LONG_CAP = LONG["sigmaCapPa"] * A_LONG
# v1.3 (sole first review): the inner rail is the retained
# REPLACEMENT section ALONE. I005 excludes the old inner rings from fixed
# members and prices a_i as the ENTIRE replacement section, so adding the
# skeleton's pre-replacement innerRingAM2 on top double-credits a section
# that was REPLACED, not retained alongside. The v1.2.x box ran with the
# inflated sum — a labelled FAILED calculation (pinned below), never a
# variant; nothing else in the inherited bill changes to preserve old
# answers.
A_IN = A_I_ADD                                     # replacement rail alone
A_IN_V122 = SKEL["innerRingAM2"] + A_I_ADD         # frozen failed pin only
assert round(A_IN_V122, 6) == 0.002507             # pins the v1.2.2 JSON value
A_BOX = 4.0 * A_RING + A_IN                        # one bay of the box

# ring demand reproduced from the free-body formula (barrel convention)
assert abs(N_RING_DEMAND - P_ATM * S_R * R_ENV) < 1e-6, N_RING_DEMAND
assert abs(N_LONG_DEMAND - P_ATM * math.pi * R_ENV ** 2 / N_LONG) < 1e-6

# ---------------------------------------------------------------------
# 2. the film strip (declared one-way drape, circular trough)
#    v1.3 (sole first review): a circular ONE-WAY membrane under uniform normal
#    pressure has no tangential traction, so equilibrium fixes a CONSTANT
#    strip tension T = p*R_tr along the whole arc — there is no trough/
#    support split. The half-value p*R_tr/2 is the two-curvature PRICING
#    reference the record doubles for mass: retained as pricing, never
#    read as this strip's tension. Each support also receives the axial
#    component T*cos(a) (= 15p/32 exactly for this geometry).
# ---------------------------------------------------------------------
SPAN = max(S_R, SHIP0["barPitchM"])          # 0.5 m
A_HALF, BULGE = SPAN / 2.0, 0.25             # trough: quarter-span sag
H_TR = BULGE * A_HALF                        # 0.0625 m
R_TR = (A_HALF ** 2 + H_TR ** 2) / (2.0 * H_TR)      # 0.53125 m
SIN_A = A_HALF / R_TR                        # support tangent slope 8/17
COS_A = math.sqrt(1.0 - SIN_A ** 2)          # 15/17
T_FILM = P_ATM * R_TR                        # 53.8 kN/m, CONSTANT on the arc
T_TWO_CURV = P_ATM * R_TR / 2.0              # 26.9 kN/m, pricing reference
T_EDGE = P_ATM * SPAN / (2.0 * SIN_A)        # arc-carry form of the same T
RAD_EDGE = T_FILM * SIN_A                    # 25.33 kN/m inward per edge
T_AXIAL = T_FILM * COS_A                     # 47.5 kN/m at each support
assert abs(2.0 * RAD_EDGE - P_ATM * SPAN) < 1e-9      # strip radial balance
assert abs(T_EDGE - T_FILM) < 1e-6           # arc-carry form == p*R_tr
assert abs(T_AXIAL - P_ATM * (15.0 / 32.0)) < 1e-6    # R_tr*cos(a) = 15/32 m

# ---------------------------------------------------------------------
# 3. the cord web (per family, from the record geometry)
# ---------------------------------------------------------------------
FAMS = [("d60", 52), ("d180/11", 70)]
PL = [r for r in planes_of(G) if r >= 6.0]
assert len(PL) == 137
EVEN, ODD = PL[0::2], PL[1::2]
CORDS = {}
for name, step in FAMS:
    t = TERM["termination"][name]
    fg = RT.family_geometry(name, step, 59.226 if name == "d60" else 17.419,
                            EVEN if name == "d60" else ODD)
    phi = 2.0 * math.pi * step / N_LONG
    sin_half = math.sin(phi / 2.0)
    planes = EVEN if name == "d60" else ODD
    a_pc = WIN["alloc"]["a_" + name] * G["areaM2"] / (len(planes) * N_LONG)
    t0 = E_SPOKE * a_pc * EPS0                         # imposed strain
    n0 = 155.0 * sin_half * t0 / math.pi               # per-plane rail hoop
    teq = (P_ATM * 2.0 * math.pi * max(planes) * BAY) / (2.0 * 155.0 * sin_half)
    # parity with the committed I019 record
    assert abs(t["sectionM2"] - a_pc) < 1e-15, (name, a_pc)
    assert abs(t["T0kN"] - t0 / 1000.0) < 5e-4, (name, t0)
    assert abs(t["planePreloadKN"] - 2.0 * 155.0 * t0 * sin_half / 1000.0) < 0.05
    assert abs(t["staticEqTensionkN"] - teq / 1000.0) < 0.1, (name, teq)
    assert abs(fg["sinHalf"] - sin_half) < 1e-15
    CORDS[name] = dict(name=name, step=step, planes=planes, sinHalf=sin_half,
                       a_pc=a_pc, T0=t0, N0=n0, teq=teq, term=t, geom=fg)

# ---------------------------------------------------------------------
# 4. the smeared ring box (n=0): common hoop strain, area-share loads
#    DECLARED approximation: the theta webs force both rails to one hoop
#    strain (the record's own crimp model); pressure enters at the barrel
#    surface, cord pulls at the inner rail, every load then distributes
#    by area share. No local bending inside the box is derived here.
#
#    v1.3 WITHDRAWAL (sole first review): this common-strain kinematics is
#    a DECLARED MODEL, not a solved equilibrium. Under the asserted
#    axisymmetric contraction the connected straight theta webs also
#    strain, and the balance of their inward pulls against the inner-ring
#    cuts leaves a large unresolved inward resultant per station
#    (diagnostic in section 4c). The retained construction's compatibility/
#    force balance is UNSOLVED in this bounded unit; no reaction is
#    invented and no stiffness/geometry/pretension is tuned to force a
#    pass. Every strain-, service-force- and slack-derived number below
#    is CONDITIONAL on this declared model.
#
#    Both-end compliance (v1.1): the box contraction acts on the
#    ANCHOR-CENTRE chord, the cord strains on its effective length. The
#    termination record's declared spring model gives, per family,
#    L_eff = L_chord - Lg + 2*l_ser (shortest cord: 12.242397 / 17.360698 m
#    against chords 12.260317 / 17.391259 m), so the strain coupling is
#    kappa = L_chord/L_eff > 1 and the no-transfer variant
#    L_eff_NT = L_chord + 2*l_ser bounds it below (kappa_NT < 1). The
#    shortest cord's kappa is used for the family (largest kappa,
#    conservative for slack); per-cord values for the representative
#    cords are computed in section 6b.
# ---------------------------------------------------------------------
NOSE_M = 0.008                                        # socket strain relief
KAPPA = {}
for name, _ in FAMS:
    t = TERM["termination"][name]
    fl = t["freeLength"]
    chord = fl["anchorCentreChordMinM"]
    lg = t["gripLgMm"] / 1000.0
    l_a = fl["lAPerEndM"]                      # nose + Lg/2 + l_ser
    l_ser = l_a - NOSE_M - lg / 2.0
    l_eff = fl["lEffM"]
    l_eff_nt = fl["lEffNoTransferM"]
    # re-derive the record's own lengths from the family constants, then
    # pin them (the guard chain reaches back to the hash above; the
    # record stores 6-decimal values, so the identity closes to ~1e-6)
    assert abs((chord - 2.0 * (NOSE_M + lg)) - fl["lFreeM"]) < 2e-6
    assert abs((chord - lg + 2.0 * l_ser) - l_eff) < 2e-6
    assert abs((chord + 2.0 * l_ser) - l_eff_nt) < 2e-6
    KAPPA[name] = dict(chord=chord, lg=lg, lSer=l_ser, lEff=l_eff,
                       lEffNT=l_eff_nt,
                       kappa=chord / l_eff, kappaNT=chord / l_eff_nt)


def eps_box(r_env, extra_n=0.0):
    """Common hoop strain of one bay of the box at envelope radius r_env
    with total added rail compression extra_n (N)."""
    return (P_ATM * BAY * r_env + extra_n) / (E_LAM * A_BOX)


def beta_of(name):
    """Strain loop gain: a unit cord strain d eps raises cord tension
    E*a_pc*d eps, the plane's cords compress the rail by that times
    155*sinHalf/pi, and the rail strain is that over E_lam*A_box —
    strain-to-strain, LENGTH-FREE. The anchor-motion feedback into cord
    strain then picks up kappa (see cord_state)."""
    c = CORDS[name]
    return E_SPOKE * c["a_pc"] * (155.0 * c["sinHalf"] / math.pi) \
        / (E_LAM * A_BOX)


def kappa_of(name):
    return KAPPA[name]["kappa"]


def cord_state(name, eps_set, eps_other):
    """Held cord tension for a stud SET of eps_set cord strain against a
    box whose hoop strain then changes by eps_other after the set. The box
    contraction shortens the anchor-centre chord by eps_other*L_chord but
    the cord strains on L_eff, so the coupling is kappa*eps_other; the
    cord's own rail reaction re-enters scaled the same way. Held strain
    (eps_set - kappa*eps_other)/(1 + beta*kappa) — a 1x1 LINEAR system,
    slack-clamped at zero. (v1.0 implicitly took kappa = 1: the bare
    chord. The no-transfer bound kappa_NT is reported alongside.)"""
    c = CORDS[name]
    t = E_SPOKE * c["a_pc"] * (eps_set - kappa_of(name) * eps_other) \
        / (1.0 + beta_of(name) * kappa_of(name))
    return t if t > 0.0 else 0.0


# install state: the compatible assembled length, in THREE named books
# (v1.3, sole first review): (i) the compatible installed SET strain
# eps_set = eps0*(1+beta*kappa); (ii) the unrestrained installation
# EQUILIBRIUM tension — the rail is free to respond, so the compliance
# loop divides: EA*eps_set/(1+beta*kappa) = T0 for the hold set; (iii) the
# RESTRAINED installation load EA*eps_set — the force only if the rail
# were held undeformed during the set, a different state, never to be
# mixed with (ii). A flat eps0 set holds only T0/(1+beta*kappa).
INSTALL = {}
for name, _ in FAMS:
    c = CORDS[name]
    beta, kap = beta_of(name), kappa_of(name)
    t_flat = cord_state(name, EPS0, 0.0)
    t_hold = cord_state(name, EPS0 * (1.0 + beta * kap), 0.0)
    assert abs(t_hold - c["T0"]) < 1e-6
    eps_set_hold = EPS0 * (1.0 + beta * kap)
    restrained = E_SPOKE * c["a_pc"] * eps_set_hold
    assert abs(restrained / (1.0 + beta * kap) - t_hold) < 1e-6
    INSTALL[name] = dict(
        t0NominalkN=round(c["T0"] / 1000.0, 3),
        tHeldFlatSetkN=round(t_flat / 1000.0, 3),
        loopGainBeta=round(beta, 4),
        strainCouplingKappa=round(kap, 6),
        loopGainBetaKappa=round(beta * kap, 4),
        setStrainToHold=round(eps_set_hold, 6),
        equilibriumTensionAtSetkN=round(t_hold / 1000.0, 3),
        restrainedInstallLoadkN=round(restrained / 1000.0, 2),
        installationBooks="unrestrained installation (rail free) carries the "
                          "denominator: EA*eps_set/(1+beta*kappa) = "
                          "%.3f kN, the equilibrium tension; EA*eps_set = "
                          "%.2f kN is the RESTRAINED (undeformed-rail) "
                          "installation load — a different named state"
                          % (t_hold / 1000.0, restrained / 1000.0),
        flatSetLossPct=round(100.0 * beta * kap / (1.0 + beta * kap), 2),
        studCapacity="UNKNOWN — the record's Tfit (2*T0*1.3) is the design "
                     "DEMAND that sized the bond grip, not a derived "
                     "stud/thread/nut capacity; no cover verdict is claimed",
    )

# vacuum states at the outermost occupied plane of each family
R_ENV_PL = lambda r: min(R_ENV, r + DEPTH)     # envelope bound at a plane
STATES = {}
for name, _ in FAMS:
    c = CORDS[name]
    beta, kap = beta_of(name), kappa_of(name)
    r_pl = max(c["planes"])
    r_env = R_ENV_PL(r_pl)
    eps_p = eps_box(r_env)
    set_hold = EPS0 * (1.0 + beta * kap)        # the record-consistent set
    # S1: studs set at assembly (holding T0), THEN pump-down
    t_s1 = cord_state(name, set_hold, eps_p)
    # S2: pump down, THEN set the studs against the contracted box (the
    # record-consistent service state: foundation present at full vacuum)
    t_s2 = cord_state(name, set_hold, 0.0)
    assert abs(t_s2 - c["T0"]) < 1e-6
    n0_eff = c["N0"] / c["T0"] * t_s2
    n_tot_s2 = P_ATM * BAY * r_env + n0_eff
    # S1': keep S1's sequence but set deep enough to still HOLD T0 at vacuum
    eps_set_star = kap * eps_p + EPS0 * (1.0 + beta * kap)
    t_star = cord_state(name, eps_set_star, eps_p)
    assert abs(t_star - c["T0"]) < 1e-6
    stud_set_load = E_SPOKE * c["a_pc"] * eps_set_star        # RESTRAINED book
    stud_set_unrestrained = stud_set_load / (1.0 + beta * kap)  # equilibrium
    STATES[name] = dict(
        planeR=round(r_pl, 4), envR=round(r_env, 4), epsBox=round(eps_p, 6),
        S1=dict(tServicekN=round(t_s1 / 1000.0, 3), slack=t_s1 <= 0.0),
        S2=dict(tServicekN=round(t_s2 / 1000.0, 3),
                n0EffkN=round(n0_eff / 1000.0, 1),
                nTotalkN=round(n_tot_s2 / 1000.0, 1),
                ringUtil=round(n_tot_s2 * A_RING / A_BOX / RING_CAP, 4),
                innerUtil=round(n_tot_s2 / (SIG_C * A_BOX), 4)),
        S1prime=dict(epsSetStar=round(eps_set_star, 6),
                     restrainedSetLoadkN=round(stud_set_load / 1000.0, 2),
                     unrestrainedSetLoadkN=round(
                         stud_set_unrestrained / 1000.0, 2),
                     setDemandRatioVsFitting=round(
                         stud_set_load / (c["term"]["TfitkN"] * 1000.0), 2),
                     studCapacity="UNKNOWN — Tfit is the design demand "
                                  "(2*T0*1.3) that sized the bond grip, not "
                                  "a stud capacity; the ratio above is a "
                                  "DEMAND comparison, not a shortfall "
                                  "verdict",
                     heldAtVacuumkN=round(t_star / 1000.0, 3),
                     n0AtVacuumkN=round(n0_eff / 1000.0, 1)),
    )

# the taut-branch identity and the slack threshold (family-independent)
R_STAR = EPS0 * E_LAM * A_BOX / (P_ATM * BAY)   # ~18.8 m envelope (v1.3 box)
EPS_BARREL = P_ATM * BAY * R_ENV / (E_LAM * A_BOX)
SLACK = {}
for name, _ in FAMS:
    c = CORDS[name]
    beta, kap = beta_of(name), kappa_of(name)
    set_hold = EPS0 * (1.0 + beta * kap)
    # slack where kappa*eps_box >= set strain (declared model); the
    # no-transfer bound uses kappa_NT on both couplings
    kap_nt = KAPPA[name]["kappaNT"]
    set_hold_nt = EPS0 * (1.0 + beta * kap_nt)
    slack_r = [r for r in c["planes"]
               if kappa_of(name) * eps_box(R_ENV_PL(r)) >= set_hold]
    slack_nt = [r for r in c["planes"]
                if kap_nt * eps_box(R_ENV_PL(r)) >= set_hold_nt]
    taut_r = [r for r in c["planes"] if r not in slack_r]
    worst_taut = min((cord_state(name, set_hold, eps_box(R_ENV_PL(r)))
                      for r in taut_r), default=0.0)
    SLACK[name] = dict(planesTotal=len(c["planes"]),
                       planesSlackS1=len(slack_r),
                       planesSlackS1NoTransferBound=len(slack_nt),
                       fraction=round(len(slack_r) / len(c["planes"]), 4),
                       tautHeldWorstkN=round(worst_taut / 1000.0, 3))
# identity check: at the outermost d60 plane the kappa-coupled pressure
# strain alone exceeds eps0 by the factor below -> S1 slack. While TAUT the
# exact branch identity carries its compliance feedback (v1.3, sole first
# review): T/T0 = 1 - kappa*eps_box / (eps0*(1+beta*kappa)); when the
# numerator crosses zero the branch clamps at slack (T = 0). The v1.2.x
# form without the (1+beta*kappa) denominator is withdrawn.
_c = CORDS["d60"]
_e = eps_box(R_ENV_PL(max(_c["planes"])))
assert kappa_of("d60") * _e / EPS0 > 1.0 \
    and abs(kappa_of("d60") * _e / EPS0 - 2.9808) < 1e-3

# ---------------------------------------------------------------------
# 4c. equilibrium-deficit diagnostic — WHY the claimed common-strain
#     closure is WITHDRAWN. Pure arithmetic on saved constants,
#     reproducing the sole first review's published check (its literals)
#     and recomputing it at the corrected inner-rail area. Not a new
#     model, not a claimed reaction.
# ---------------------------------------------------------------------
A_TH = WIN["alloc"]["a_th"]                  # theta-web section (both webs)
assert abs(A_TH - 0.0006943030859409637) < 1e-18
DEFC = {}
for label, area, strain, depth, r_env_l in (
        # the review's own literals (its rounded geometry, inflated v1.2.2
        # area, 6-dp strain) — reproduces its published numbers exactly:
        ("reviewWitnessInputs", 0.002507, 0.00554, 6.4615, 56.0),
        # this correction (retained section, record geometry, unrounded
        # strain):
        ("v13CorrectedInputs", A_IN, EPS_BARREL, DEPTH, R_ENV)):
    l_web = math.hypot(depth, 2.0 * math.pi * r_env_l / N_LONG)
    web_in = 2.0 * E_LAM * A_TH * strain * depth / l_web
    ring_out = 2.0 * E_LAM * area * strain * math.sin(math.pi / N_LONG)
    DEFC[label] = dict(
        innerRailAreaM2=area, strain=round(strain, 6),
        depthM=depth, webLengthM=round(l_web, 4),
        webInwardN=round(web_in, 1), ringOutwardN=round(ring_out, 1),
        unresolvedInwardN=round(web_in - ring_out, 1),
        requiredWebStrain=round(ring_out * l_web
                                / (2.0 * E_LAM * A_TH * depth), 9),
        imposedWebStrain=round(strain, 9))
assert abs(DEFC["reviewWitnessInputs"]["webInwardN"] - 979829.344) < 0.1
assert abs(DEFC["reviewWitnessInputs"]["ringOutwardN"] - 76000.474) < 0.1
assert abs(DEFC["reviewWitnessInputs"]["unresolvedInwardN"] - 903828.870) < 0.1
assert abs(DEFC["reviewWitnessInputs"]["requiredWebStrain"]
           - 0.000429710) < 1e-8
DEFICIT = dict(
    geometry=dict(thetaWebAreaM2=A_TH, recordDepthM=DEPTH,
                  recordWebPitchM=round(2.0 * math.pi * R_ENV / N_LONG, 6)),
    statement="under the declared common-strain model the connected "
              "straight theta webs contract with the box, and their "
              "inward pulls overwhelm the inner-ring cuts' outward push "
              "per station — the single-DOF common-strain state does not "
              "balance the priced webs, so the claimed CLOSED equilibrium "
              "is withdrawn and the model's strain/service/slack outputs "
              "are CONDITIONAL diagnostics",
    reviewWitness="the sole first review demonstrated this deficit with "
                  "saved values (979829.344 N inward vs 76000.474 N "
                  "outward, 903828.870 N unresolved; required web strain "
                  "0.000429710 vs imposed 0.005540000); the "
                  "reviewWitnessInputs row reproduces that arithmetic "
                  "exactly, the v13CorrectedInputs row recomputes it on "
                  "the retained section — still unresolved by an order of "
                  "magnitude, and NO reaction is invented here",
    rows=DEFC)

# ---------------------------------------------------------------------
# 5. member utilization table (SF1.0 construction; SF column = demand x SF)
# ---------------------------------------------------------------------
def util_rows(sf):
    rows = []
    n_p = P_ATM * BAY * R_ENV * sf
    worst = max(STATES[n]["S2"]["n0EffkN"] for n, _ in FAMS) * 1000.0
    rows.append(dict(member="barrel ring (smeared share, slack cords)",
                     demandN=round(n_p * A_RING / A_BOX, 0),
                     capacityN=round(RING_CAP, 0),
                     util=round(n_p * A_RING / A_BOX / RING_CAP, 4),
                     note="the S1 pressure-only case; record sizes each ring "
                          "alone at util 0.981 (no inner-rail credit)"))
    rows.append(dict(member="barrel ring (smeared share, worst d11 plane)",
                     demandN=round((n_p + worst) * A_RING / A_BOX, 0),
                     capacityN=round(RING_CAP, 0),
                     util=round((n_p + worst) * A_RING / A_BOX / RING_CAP, 4),
                     note="pressure + held pretension N0 (S2/S1'); "
                          "Euler-governed, braced 2.27 m"))
    rows.append(dict(member="inner rail (yield check)",
                     demandN=round((n_p + worst) * A_IN / A_BOX, 0),
                     capacityN=round(SIG_C * A_IN, 0),
                     util=round((n_p + worst) / (SIG_C * A_BOX), 4),
                     note="Euler stability of the ADDED area rides on the "
                          "box webs at bay spacing (not re-derived)"))
    rows.append(dict(member="longeron (end-cap thrust)",
                     demandN=round(N_LONG_DEMAND * sf, 0),
                     capacityN=round(LONG_CAP, 0),
                     util=round(N_LONG_DEMAND * sf / LONG_CAP, 4),
                     note="unchanged by the cord state; boundary reaction"))
    rows.append(dict(member="cord (static, S2)",
                     demandN=round(_c["T0"], 0), capacityN=None, util=None,
                     note="stress = E*eps0 = 140 MPa, but cord strength is "
                          "UNKNOWN in the ledger — no utilisation claimed"))
    return rows

UTIL_SF10, UTIL_SF12 = util_rows(1.0), util_rows(1.2)

# ---------------------------------------------------------------------
# 6. exterior tributary reconciliation + boundary reactions
#    v1.3 (sole first review): the loaded film surface is the EXTERIOR
#    envelope (R = 56 m) — a 112 m cylinder (cylL = 2R by the fineness-2
#    geometry) closed by two hemispherical caps. The v1.2.x band sum
#    2*pi*sum(PL)*BAY used INNER cord-plane radii (49.5385 m at the
#    barrel, cap planes below that): not the pressure surface, withdrawn
#    as a reconciliation and retained only as the labelled failed pin.
#    Exterior tiling: 224 barrel bands of 2*pi*R*s_r each tile the
#    cylinder once; the caps are EXACTLY HALF the envelope (4*pi*R^2 =
#    2*pi*R*cylL), not a ~12% polar remainder.
# ---------------------------------------------------------------------
CAP_PAIR_AREA = 4.0 * math.pi * R_ENV ** 2    # the two caps (= one sphere)
CYL_AREA = G["areaM2"] - CAP_PAIR_AREA        # = 2*pi*R*cylL, cylL = 2R
N_BANDS = round(CYL_AREA / (2.0 * math.pi * R_ENV * S_R))   # 224 bands
BAND_AREA_EXT = N_BANDS * 2.0 * math.pi * R_ENV * S_R
BAND_AREA_V122 = 2.0 * math.pi * sum(PL) * BAY    # withdrawn v1.2.x sum
assert abs(G["areaM2"] - (CYL_AREA + CAP_PAIR_AREA)) < 1e-6
assert abs(CYL_AREA - CAP_PAIR_AREA) < 1e-6   # cylL = 2R: cylinder = caps
assert N_BANDS == 224 and abs(BAND_AREA_EXT - CYL_AREA) < 1e-6
# ---------------------------------------------------------------------
# 6b. representative cords: anchor-centre chord AND the corrected spring
#     lengths (declared model, family constants from the guarded record)
# ---------------------------------------------------------------------
def cord_lengths(name, r):
    """Anchor-centre chord and the declared spring model's lengths for a
    cord of this family at plane radius r (same per-family constants the
    termination record used for its shortest cord)."""
    chord = 2.0 * r * CORDS[name]["sinHalf"]
    k = KAPPA[name]
    l_free = chord - 2.0 * (NOSE_M + k["lg"])
    l_eff = chord - k["lg"] + 2.0 * k["lSer"]
    l_eff_nt = chord + 2.0 * k["lSer"]
    return chord, l_free, l_eff, l_eff_nt


REP = {}
for label, name, r in (("d60Shortest", "d60", min(EVEN)),
                       ("d11Longest", "d180/11", max(ODD))):
    chord, l_free, l_eff, l_eff_nt = cord_lengths(name, r)
    if label == "d60Shortest":
        # the guarded record's own shortest-cord entry, pinned
        fl = TERM["termination"][name]["freeLength"]
        assert abs(chord - fl["anchorCentreChordMinM"]) < 1e-6
        assert abs(l_free - fl["lFreeM"]) < 1e-6
        assert abs(l_eff - fl["lEffM"]) < 1e-6
        assert abs(l_eff_nt - fl["lEffNoTransferM"]) < 1e-6
    REP[label] = dict(r=r, chord=chord, lFree=l_free, lEff=l_eff,
                      lEffNT=l_eff_nt, kappa=chord / l_eff)

# ---------------------------------------------------------------------
# 7. the anchor station (local, both incident cord axes)
# ---------------------------------------------------------------------
# corrected termination constants (R3-I019 v3), read as values so the
# sibling unit's script is never re-run by this import; the block
# dimensions are unchanged by the correction, the GRIP and the RING
# CONNECTION are not (60/97 mm grips; the pad is now BOLTED through)
BLOCK = {"d60": (0.050, 0.036, 0.024), "d180/11": (0.064, 0.046, 0.030)}
for name, _ in FAMS:
    t = TERM["termination"][name]
    blk = BLOCK[name]
    assert abs(blk[0] * blk[1] * blk[2] * 4430.0 - t["blockKg"]) < 0.002
    assert t["gripLgMm"] in (60.0, 97.0)
STATION = {}
for name, _ in FAMS:
    c, t = CORDS[name], CORDS[name]["term"]
    blk = BLOCK[name]
    e = blk[0] / 2.0 + t["bodyOdMm"] / 2000.0      # block half-width + socket
    t_s2 = STATES[name]["S2"]["tServicekN"] * 1000.0
    att = t["attachment"]
    STATION[name] = dict(
        radialResultantkN=round(2.0 * t_s2 * c["sinHalf"] / 1000.0, 2),
        eccentricityMm=round(e * 1000.0, 1),
        momentkNm=round(2.0 * t_s2 * c["sinHalf"] * e / 1000.0, 3),
        hardware=dict(blockMm=[round(x * 1000.0) for x in blk],
                      socketBodyOdmM=t["bodyOdMm"], stud=t["studMm"],
                      gripLgMm=t["gripLgMm"],
                      doublerPadMm=[200.0, 140.0, 3.0],
                      ringConnection=att["construction"],
                      boltsPerStation=att["boltsPerStation"],
                      boltShankMm=att["shankMm"],
                      boltStack=att["stackDimensioned"],
                      boltShearCapkN=att["singleShearCapacitykN"],
                      boltUtilisation=att["utilisation"]),
        capacityVerdict="UNKNOWN — the station moment is carried by the "
                        "bolted block/pad/ring connection whose laminate "
                        "bearing, block bending and pull-through capacities "
                        "are not derived; the metallic bolt set itself is "
                        "sized (shear util "
                        + str(att["utilisation"]) + " vs the worst window); "
                        "the stud pair's thread/nut capacity is likewise "
                        "UNKNOWN (the record's fitting value is a demand, "
                        "not a capacity)",
    )

# ---------------------------------------------------------------------
# 8. ledger, factors, verdict
# ---------------------------------------------------------------------
BILL = TERM["bill"]
# SF1.2 read DYNAMICALLY from the record's own sf12 block and asserted at
# load (the intake flagged the hard-coded 2562.4/-312.6 prose: a changed
# record could previously leave stale narrative behind)
SF12 = TERM["sf12"]
assert abs(SF12["afterSpokesT"] - 243.98) < 0.005
assert abs(SF12["afterT"] - 2562.4) < 0.05
assert abs(SF12["afterMarginSLT"] - (-312.6)) < 0.05
MATERIAL = dict(
    cord=dict(E=E_SPOKE, rho=RHO_SPOKE, strength=None,
              identity="UHMWPE-class (Dyneema-type) per its source "
                       "documentation — creep UNVERIFIED",
              provenance="ASSUMED inherited pair (E 70 GPa + rho 970); NOT a "
                         "fibre spec — never combined with any UTS; strain "
                         "limit: the declared eps0 0.2% sets 140 MPa",
              termination=dict(stud="Ti-6Al-4V, E 114 GPa, rho 4430 "
                                     "(public datasheet); the fitting value "
                                     "2*T0*1.3 is the DEMAND that sized the "
                                     "bond grip, NOT a stud capacity",
                               bond="design shear 12 MPa, filled epoxy — "
                                    "ASSUMED, unverified",
                               attachment="3x M10 Ti through-bolts, single "
                                          "shear; laminate capacities "
                                          "UNKNOWN")),
    film=dict(sigmaBasis="5.8 GPa at sf 4 x eff 0.5 -> 725 MPa working",
              rho=1560.0,
              provenance="record pricing basis; doubled for the one-way arc"),
    laminate=dict(E=E_LAM, rho=RHO_LAM, sigmaC=SIG_C, sigmaT=SIG_T,
                  provenance="sigma_c/sigma_t SOURCED (Toray T700S datasheet "
                             "SACMA SRM 1R-94 / ASTM D3039, Vf 0.6); E and "
                             "rho representative inputs, not coupon values"),
)
FACTORS = [
    dict(factor="physical pressure / preload", value="delta_p = -101325 Pa; "
         "eps0 = 0.2% imposed strain", appliesTo="state definition, unfactored"),
    dict(factor="demand SF", value="1.0 / 1.2",
         appliesTo="pressure demand only (SF1.2 world is a separate "
                   "construction in the record)"),
    dict(factor="material allowable", value="sigma_c 1450 MPa SOURCED; barrel "
         "ring Euler 913 MPa governs; film 725 MPa working",
         appliesTo="member statics here"),
    dict(factor="fitting factor", value="1.3 (spokeFitting); a DEMAND of "
         "2 x T0 x 1.3 sized the bond grip — not a derived stud/thread/nut "
         "capacity", appliesTo="cord hardware"),
    dict(factor="capacity knockdown KD", value="0.65 — NOT applied to these "
         "statics (it prices the licensed buckling margins)",
         appliesTo="stability licensing only"),
    dict(factor="assembly allowance", value="5%", appliesTo="mass only"),
]
I019_HYP = dict(
    staticEqTensionOuterPlaneKN={n: CORDS[n]["term"]["staticEqTensionkN"]
                                 for n, _ in FAMS},
    reading="retained as a SIGNED, mechanically inadmissible hypothetical "
            "(v1.3, sole first review): with inward pressure and inward "
            "tensile cord pulls, removing the ring support leaves "
            "-P_band - 2*155*T*sin(phi/2) = 0, so a web that resisted the "
            "band directly would require NEGATIVE T — compression these "
            "cords cannot supply. The magnitudes 234.0/205.8 kN are that "
            "bypassed-rings free body's COMPRESSION requirement, recorded "
            "as inadmissible: NOT an alternative tensile load path and NOT "
            "this construction's demand (the film closes on the ring box; "
            "the cord web's static duty is its own pretension, 6.8/17.8 "
            "kN, which compatibility only relaxes). The termination record "
            "consumed here is its corrected v3.1 "
            "(hash-guarded above; its first review's findings stand "
            "corrected as follows — eight closed in the v2 correction; "
            "the one cord accounting boundary with the dimensioned "
            "bolt stack, and the Pa units label, closed in the v3 "
            "correction; the spring model's mechanics were repaired "
            "in v3, and v3's overstated physical-amplitude claims "
            "were corrected by the immediate v3.1 successor — that "
            "correction is submitted for lead targeted verification; "
            "no acceptance is asserted here); this supersedes only its "
            "load-path interpretation, not its record",
    utilisation="UNKNOWN — the corrected ledger carries no cord strength "
                "and no fibre ultimate is borrowed (staticEqStress is a "
                "string UNKNOWN in the guarded record)",
    historicalUtilisationNote="the withdrawn v1 figure divided an ASSUMED "
                              "cord stress by a T700 tow UTS — an invalid "
                              "pairing, moot under the corrected path",
)
VERDICT = (
    "CONDITIONAL on the declared common-strain model, whose claimed "
    "closure is WITHDRAWN: the priced theta webs do not balance under "
    "that kinematics (see equilibriumDeficit — the sole first review "
    "demonstrated the deficit and this unit reproduces it). Within the "
    "model, the pressure resultant is TRACED film -> barrel rings + "
    "inner rail (the retained replacement section ALONE, 1 453.5 mm2 — "
    "the v1.2.x 2 507 mm2 double-credit is a labelled failed "
    "calculation) -> caps/longerons, and the cords' static duty is "
    "their own pretension. The binding model result is kinematic: while "
    "taut, dT/T0 = kappa*eps_box / (eps0*(1+beta*kappa)), then "
    "slack-clamped; at the barrel eps_box %.2fe-3 exceeds the declared "
    "eps0 2.0e-3 by %.2fx, so cords tensioned before pump-down go slack "
    "over the barrel (%d/%d d60 and %d/%d d11 planes, ~%.0f%%) — against "
    "a foundation-loss tolerance of %.3f%% rigid licensed (the QUOTABLE "
    "bound, from the record), while the drawn-termination compliant "
    "state computes %.3f%% — BEYOND the rigid anchor on the v3 "
    "consistent spring law (eta > 1), reported and NOT claimed — which "
    "un-licenses the stability PASS within the model. The record's "
    "margins are valid only for an assembly that sets (or maintains) "
    "the stud length at the pumped-down state — and resetting through "
    "the EXISTING studs is UNAVAILABLE: the longest representative cord "
    "needs ~%.2f m combined take-up at the model's own barrel strain "
    "against 0.254 m of combined stud LENGTH before thread engagement "
    "(resetTravel). Any install-after-evacuation or added-travel "
    "construction is UNQUALIFIED with UNKNOWN parts and mass. The "
    "deeper-eps0 alternative is quantified as a DEMAND comparison only "
    "(restrained set load %.2fx/%.2fx the priced fitting demand — a "
    "demand, not a capacity; stud capacity UNKNOWN) and left UNPRICED. "
    "The retained construction's compatibility/force balance, full-hull "
    "closure, the bolted station connection's laminate capacities and "
    "the cord strength remain UNKNOWN."
) % (EPS_BARREL * 1e3, kappa_of("d60") * EPS_BARREL / EPS0,
     SLACK["d60"]["planesSlackS1"], SLACK["d60"]["planesTotal"],
     SLACK["d180/11"]["planesSlackS1"], SLACK["d180/11"]["planesTotal"],
     100.0 * SLACK["d60"]["fraction"], TOL_RIGID_PCT, TOL_DRAWN_PCT,
     REP["d11Longest"]["chord"] * EPS_BARREL,
     STATES["d60"]["S1prime"]["setDemandRatioVsFitting"],
     STATES["d180/11"]["S1prime"]["setDemandRatioVsFitting"])
NEXT_CHANGE = (
    "Solve the retained construction's compatibility/force balance — a "
    "model in which the theta webs' stiffness participates in the "
    "station equilibrium instead of being bypassed by an asserted "
    "common strain — then re-derive the pressure strain, service forces "
    "and slack counts under that solved model; separately, write the "
    "assembly/installation construction (evacuation sequence, cord-"
    "length control, or qualified added travel with priced parts and "
    "mass) into the record before any stability margin is re-licensed."
)

OUT = dict(
    unit="R3-I023", rev=REV, date="2026-10-14",
    dependency=dict(
        inputs="R3-I019 v3.1 termination.json + corrected R3-I015 "
               "coupled.json, both HASH-GUARDED at load (sha256 in "
               "loadpath.py; the v1.0 run read the uncorrected termination "
               "record; v1.1 pinned the v2 bytes, superseded by this "
               "re-pin)",
        i019=(TERM_SHA[:16] + "… (rev " + TERM["rev"] + "; grips 60/97 mm; bill spokes "
              "245.42 t; UHMWPE-class ledger with the EPa key; dimensioned "
              "bolted attachment, one cord accounting boundary)"),
        i015=(COUP_SHA[:16] + "… (K labelled Pa; numerics unchanged)"),
        springModel="both-end compliance carried as kappa = L_chord/L_eff "
                    "(declared model; no-transfer variant reported as the "
                    "bound), from the corrected free-length record — the "
                    "v3 successor ratified this same law (eta > 1)",
        n5MarginBound=dict(rigidLicensed=round(N5_RIGID, 9),
                           drawnCompliant=round(N5_DRAWN, 9),
                           toleranceRigidPct=round(TOL_RIGID_PCT, 4),
                           toleranceDrawnPct=round(TOL_DRAWN_PCT, 4),
                           quotable="rigidLicensed — the drawnCompliant value "
                                    "sits BEYOND the rigid anchor (v3 "
                                    "consistent eta > 1) and is reported, "
                                    "not claimed",
                           source="read from the guarded records, replacing "
                                  "the v1.0 prose literals"),
    ),
    conventions=dict(
        normal="outward", deltaP=-P_ATM,
        statement="delta_p = p_in - p_out = -101325 Pa: the vacuum lineage's "
                  "INWARD traction; record P_ATM magnitudes are |delta_p|. "
                  "No internal overpressure, helium envelope or outward "
                  "reaction is introduced anywhere in this unit.",
        pricedSystem="the priced film/bar/ring wall and the caps/longerons "
                     "CARRY the pressure (traced under the DECLARED model — "
                     "see modelStatus); the membrane term stays excluded "
                     "from the licensed stability calc exactly as the record "
                     "excludes it (no continuous pressure shell is invented)",
    ),
    modelStatus=dict(
        declaredModel="common hoop strain across the smeared ring box "
                      "(theta webs asserted to enforce one strain) with "
                      "both-end termination compliance kappa",
        equilibrium="WITHDRAWN closure claim: the declared kinematics does "
                    "not balance the priced theta webs — see "
                    "equilibriumDeficit, which reproduces the sole first "
                    "review's demonstrated deficit and recomputes it at the "
                    "corrected inner-rail area (still unresolved). No "
                    "reaction is invented; no stiffness, geometry, "
                    "pretension or load-share coefficient is tuned to "
                    "force a pass",
        conditionals=["pressure strain eps_box and every epsBox-derived "
                      "field (box.epsBarrel, states.*, slack counts, "
                      "threshold radii)",
                      "S1/S2/S1' service forces and rail reactions",
                      "the reset-travel take-up arithmetic (which "
                      "additionally assumes the model strain state)"],
        withdrawn=["the v1.2.x zero-mass existing-stud reset claim "
                   "(resetTravel)",
                   "all studCovers / stud-shortfall capacity verdicts — "
                   "the fitting value is a DEMAND, stud capacity UNKNOWN",
                   "the counted-once inner-plane band reconciliation "
                   "(boundaryReactions.tributary)",
                   "the film trough/support tension split — the strip "
                   "tension is CONSTANT p*R_tr",
                   "the denominator-free taut identity dT/T0 = "
                   "kappa*eps_box/eps0"],
        unknowns=["the retained construction's compatibility/force balance "
                  "with the webs participating (nextChange)",
                  "stud/thread/nut capacity for the actual sections and "
                  "materials",
                  "the installation construction for pump-down tensioning",
                  "cap-edge/junction local bending and traction "
                  "distribution"],
    ),
    filmStrip=dict(spanM=SPAN, sagM=round(H_TR, 4), troughRM=round(R_TR, 4),
                   tConstantkNm=round(T_FILM / 1000.0, 2),
                   tTwoCurvaturePricingRefkNm=round(T_TWO_CURV / 1000.0, 2),
                   tEdgeFormkNm=round(T_EDGE / 1000.0, 2),
                   radialPerEdgekNm=round(RAD_EDGE / 1000.0, 2),
                   axialAtSupportkNm=round(T_AXIAL / 1000.0, 2),
                   balance="one-way circular membrane under uniform normal "
                           "pressure: CONSTANT tension T = p*R_tr along the "
                           "arc (2*T*sin(a) = p*s_r exactly). The half-value "
                           "is the two-curvature PRICING reference the "
                           "record doubles for mass — not this strip's "
                           "trough tension; the doubled thickness pricing "
                           "stands",
                   axialCancellation="T*cos(a) = 15p/32 = 47.5 kN/m at each "
                                     "support: equal and opposite between "
                                     "adjacent strips on every interior "
                                     "barrel ring, UNCANCELLED at the cap "
                                     "edges — exported unsolved in "
                                     "boundaryReactions.unsolved",
                   pricedKgM2=WALL["filmKgM2"]),
    barrelRing=dict(sectionM2=A_RING, odMm=RING["odMm"],
                    demandN=N_RING_DEMAND, capacityN=RING_CAP,
                    governs=RING["governs"], bracedM=RING["bracedL"],
                    lineLoadkNm=round(P_ATM * S_R / 1000.0, 2),
                    utilAlone=round(N_RING_DEMAND / RING_CAP, 4)),
    box=dict(aRingM2=A_RING, aInnerM2=round(A_IN, 6), aBoxM2=round(A_BOX, 6),
             aInnerV122M2=round(A_IN_V122, 6),
             epsBarrel=round(EPS_BARREL, 6),
             aInnerStatement="the retained replacement inner-rail section "
                             "ALONE (I005's a_i prices the ENTIRE "
                             "replacement rail); the v1.2.x box added the "
                             "pre-replacement skeleton section on top — a "
                             "labelled FAILED calculation, pinned in "
                             "aInnerV122M2",
             share="CONDITIONAL: loads distribute by area share under the "
                   "DECLARED common-strain kinematics (theta webs asserted "
                   "to enforce one hoop strain); that kinematics does not "
                   "balance the priced webs — see equilibriumDeficit"),
    equilibriumDeficit=DEFICIT,
    cordWeb={n: dict(
        sinHalf=round(CORDS[n]["sinHalf"], 6),
        perCordSectionM2=CORDS[n]["a_pc"], t0kN=round(CORDS[n]["T0"] / 1000.0, 3),
        n0PerPlanekN=round(CORDS[n]["N0"] / 1000.0, 1),
        identity="the box contraction shortens the anchor-centre chord "
                 "(2 r sin(phi/2), both ends on the same contracted plane) "
                 "by eps*L_chord, the cord strains on L_eff, so the held "
                 "strain after a box contraction eps is (eps_set - "
                 "kappa*eps)/(1+beta*kappa) with kappa = L_chord/L_eff; "
                 "eps_set is the installed set strain: the compatible "
                 "hold set is eps0*(1+beta*kappa), the nominal flat set "
                 "is eps_set = eps0 (eps0 the fixed nominal 0.002)",
        springModel={k: (round(v, 6) if isinstance(v, float) else v)
                     for k, v in KAPPA[n].items()},
        install=INSTALL[n], states=STATES[n], slackS1=SLACK[n],
    ) for n, _ in FAMS},
    slackThreshold=dict(
        envRadiusFlatEps0M=round(R_STAR, 3),
        envRadiusHoldSetM={n: round(R_STAR * (1.0 + beta_of(n)
                                              * kappa_of(n)) / kappa_of(n), 3)
                           for n, _ in FAMS},
        statement="slack in S1 wherever kappa*eps_box >= eps0(1+beta*kappa) "
                  "(declared spring model); no-transfer bound counts in "
                  "cordWeb.*.slackS1.planesSlackS1NoTransferBound; envelope "
                  "bound: min(R, r_plane + depth); all counts CONDITIONAL "
                  "on the declared model (modelStatus)"),
    utilizationSF10=UTIL_SF10, utilizationSF12onSameConstruction=UTIL_SF12,
    boundaryReactions=dict(
        longeron=dict(eachN=round(N_LONG_DEMAND, 0), count=N_LONG,
                      totalMN=round(N_LONG * N_LONG_DEMAND / 1e6, 1),
                      identity="N x p pi R^2 / 155 = p pi R^2 exactly"),
        capMembranekNm=round(P_ATM * R_ENV / 2.0 / 1000.0, 1),
        junctionThrustNPerM=round(P_ATM * R_ENV / 2.0, 0),
        signedCapResultant=dict(
            perCapMN=round(-P_ATM * math.pi * R_ENV ** 2 / 1e6, 1),
            statement="the SIGNED resultant, kept separate from any scalar "
                      "area: each cap carries -p*pi*R^2 = -%.1f MN "
                      "(inward, toward midship); the barrel structure "
                      "returns the SAME total thrust as axial COMPRESSION "
                      "p*pi*R^2, transferred serially and counted once: "
                      "the pR/2 membrane per rim metre feeds the "
                      "cap/rim/junction path, which delivers the identical "
                      "p*pi*R^2 total to the 155 longerons (the "
                      "p*pi*R^2/155 each is that same thrust shared, not "
                      "an addition to it); the net closed-hull resultant "
                      "is zero"
                      % (P_ATM * math.pi * R_ENV ** 2 / 1e6)),
        axialClosure="closes at the sizing identity; the distribution among "
                     "longerons/rings near the nose taper is UNKNOWN",
        filmAxialAtSupportkNm=round(T_AXIAL / 1000.0, 2),
        tributary=dict(
            envelopeAreaM2=round(G["areaM2"], 1),
            cylinderAreaM2=round(CYL_AREA, 1),
            twoCapsAreaM2=round(CAP_PAIR_AREA, 1),
            barrelBands=N_BANDS,
            bandAreaM2=round(BAND_AREA_EXT, 1),
            halves="the caps are EXACTLY HALF the envelope (4*pi*R^2 = "
                   "2*pi*R*cylL with cylL = 2R = 112 m), not a ~12%% polar "
                   "remainder; the %d exterior barrel bands of 2*pi*R*s_r "
                   "tile the cylinder once; the longitudinal cuts at the "
                   "155 anchor stations divide each band among its cords — "
                   "a kinematic split, not a solved distribution"
                   % N_BANDS,
            withdrawnV122="the v1.2.x sum 2*pi*sum(inner cord-plane radii)"
                          "*BAY = %.0f m2 used INNER cord-plane radii "
                          "(49.5385 m at the barrel, cap planes below) — "
                          "not the pressure surface; retained only as the "
                          "labelled failed pin" % BAND_AREA_V122,
        ),
        unsolved=[
            "cap-edge/cylinder junction: the film's uncancelled axial "
            "traction (47.5 kN/m) plus the moment/shear redistribution "
            "between the cap membrane (pR/2) and the first barrel ring — "
            "UNSOLVED here",
            "longeron/ring axial-compression distribution near the nose "
            "taper",
            "local bending and ring-beam effects inside one bay of the box",
        ],
    ),
    station=STATION,
    representativeCords={lbl: dict(
        rM=round(REP[lbl]["r"], 4),
        anchorCentreChordM=round(REP[lbl]["chord"], 4),
        freeBetweenSocketMouthsM=round(REP[lbl]["lFree"], 4),
        effectiveSpringM=round(REP[lbl]["lEff"], 4),
        effectiveSpringNoTransferM=round(REP[lbl]["lEffNT"], 4),
        strainCouplingKappa=round(REP[lbl]["kappa"], 6),
        tServicekN=STATES[("d60" if lbl == "d60Shortest" else "d180/11")]
        ["S2"]["tServicekN"],
        perEndRadialkN=round(CORDS["d60" if lbl == "d60Shortest" else "d180/11"]
                             ["T0"] * CORDS["d60" if lbl == "d60Shortest"
                                            else "d180/11"]["sinHalf"] / 1000.0, 2),
    ) for lbl in ("d60Shortest", "d11Longest")},
    resetTravel=dict(
        bindingCase="d180/11 longest representative cord",
        chordM=round(REP["d11Longest"]["chord"], 4),
        modelStrainTakeupM=round(REP["d11Longest"]["chord"] * EPS_BARREL, 4),
        studCombinedLengthM=0.254,
        studs="2 x M23x127 (the record's d180/11 stud pair): combined "
              "LENGTH 0.254 m BEFORE any thread engagement allowance",
        shortestCase="d60 shortest representative cord: take-up "
                     "%.4f m is a barrel-strain diagnostic; it is below "
                     "the 2 x M14x79 = 0.158 m combined LENGTH only as a "
                     "gross stock comparison — usable thread travel after "
                     "engagement/construction limits is UNKNOWN. The "
                     "figure 0.254 m / strain = 42.7 m chord (~21.6 m "
                     "plane radius) is a hypothetical UNIFORM-BARREL-"
                     "STRAIN comparison, not an actual all-plane "
                     "threshold: the implemented local strain is "
                     "eps_box(min(56, r+depth)), smaller at cap-plane "
                     "radii, so no universal cap-plane travel bound is "
                     "claimed" % (REP["d60Shortest"]["chord"]
                                          * EPS_BARREL),
        verdict="WITHDRAWN (v1.3, sole first review) as a claimed "
                "existing-stud zero-mass reset: at the declared model's "
                "own barrel strain the longest cord's combined take-up "
                "exceeds the combined stud LENGTH by >2x before thread "
                "engagement, so the existing studs cannot provide the "
                "travel. An install-after-evacuation sequence or an "
                "added-travel mechanism is UNQUALIFIED with UNKNOWN parts "
                "and mass — a force comparison or a re-tuned set length "
                "does not establish it; the strain state itself is "
                "CONDITIONAL on the withdrawn-equilibrium model "
                "(modelStatus)",
    ),
    i019Hypothesis=I019_HYP,
    materialLedger=MATERIAL,
    factors=FACTORS,
    bill=dict(
        before=BILL, after=BILL,
        statement=("analysis-only unit: no construction change, so after == "
                   "before line-for-line — and the bill is the CORRECTED "
                   "termination record's (drawn sockets 60/97 mm grips, "
                   "DIMENSIONED bolted attachment priced — M10 45/50 mm "
                   "shanks — one cord accounting boundary with no separate "
                   "tow line, x1.5 with its assembly share): "
                   "total 2233.4 t, SL +16.4 t, 2500 m -476.1 t; SF1.2 mass "
                   "failure carried at %.1f t / %.1f t against the "
                   "corrected completed baseline (READ from the record's "
                   "own sf12 block and asserted at load — no hard-coded "
                   "prose remains). The v1.0 run copied the "
                   "pre-correction bill (2230.7 t, SL +19.1, -473.4, "
                   "stackedFittings 5.3) — superseded; v1.1 pinned the v2 "
                   "record (spokes 245.37 t) — superseded by this v3 re-pin "
                   "(spokes 245.42 t, bolts 1.41 t, no tow line). NOTHING "
                   "required-but-unsized is zeroed:"
                   % (SF12["afterT"], SF12["afterMarginSLT"])),
        unknowns=[
            "deeper-eps0 hardware if S1' is chosen (restrained set demand "
            "%.2fx/%.2fx the priced fitting demand in cordWeb.*.states."
            "S1prime — a DEMAND comparison; stud CAPACITY unknown; "
            "UNPRICED, no fitted coefficient)"
            % (STATES["d60"]["S1prime"]["setDemandRatioVsFitting"],
               STATES["d180/11"]["S1prime"]["setDemandRatioVsFitting"]),
            "installation/reset construction at pump-down: existing-stud "
            "travel insufficient (resetTravel); alternatives UNKNOWN "
            "parts and mass",
            "the retained construction's theta-web equilibrium "
            "(modelStatus, equilibriumDeficit)",
            "the bolted station connection's laminate bearing/bending/"
            "pull-through capacities vs the stated moment",
            "full-hull axial closure beyond the sizing identity",
            "cord material strength (ledger row, not a utilisation)",
        ],
        gasBuoyancy="lift lines unchanged and counted once",
    ),
    verdict=VERDICT, nextChange=NEXT_CHANGE,
)

with open(os.path.join(HERE, "loadpath.json"), "w", encoding="utf-8") as fh:
    json.dump(OUT, fh, indent=1)
    fh.write("\n")
print("R3-I023 loadpath.json written ({})".format(REV))
print("  eps_barrel %.6f  threshold R* %.3f m  slack d60 %d/%d  d11 %d/%d"
      % (EPS_BARREL, R_STAR, SLACK["d60"]["planesSlackS1"],
         SLACK["d60"]["planesTotal"], SLACK["d180/11"]["planesSlackS1"],
         SLACK["d180/11"]["planesTotal"]))
print("  n5 tolerance: %.4f%% drawn / %.4f%% rigid (bound from records)"
      % (TOL_DRAWN_PCT, TOL_RIGID_PCT))
print("  equilibrium deficit (declared model, v1.3 inputs): web %.0f kN in"
      " vs ring %.0f kN out per station — %.0f kN unresolved (closure"
      " WITHDRAWN)"
      % (DEFC["v13CorrectedInputs"]["webInwardN"] / 1e3,
         DEFC["v13CorrectedInputs"]["ringOutwardN"] / 1e3,
         DEFC["v13CorrectedInputs"]["unresolvedInwardN"] / 1e3))
for n, _ in FAMS:
    s = STATES[n]
    i = INSTALL[n]
    print("  %-8s kappa %.6f  beta %.4f -> beta*kappa %.4f  flat set %.3f kN"
          " (%.2f%% loss)"
          % (n, i["strainCouplingKappa"], i["loopGainBeta"],
             i["loopGainBetaKappa"], i["tHeldFlatSetkN"],
             i["flatSetLossPct"]))
    print("  %-8s S1 %.3f kN (slack=%s)  S2 %.3f kN  ring util %.4f"
          " inner util %.4f  S1' restrained set %.2f kN (%.2fx fitting"
          " demand, capacity UNKNOWN)"
          % (n, s["S1"]["tServicekN"], s["S1"]["slack"], s["S2"]["tServicekN"],
             s["S2"]["ringUtil"], s["S2"]["innerUtil"],
             s["S1prime"]["restrainedSetLoadkN"],
             s["S1prime"]["setDemandRatioVsFitting"]))
