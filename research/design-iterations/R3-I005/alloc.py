#!/usr/bin/env python3
"""R3-I005 (v3, after the consolidated 2026-10-14 review) — a mixed-offset
net that covers the odd modes, priced honestly, with the finite-endpoint
phase/coupling verdict the scalar pass cannot give.

v1 fed the WRONG engagement factors (the I004 review's finding 1) into the
foundation and treated them linearly; superseded. v2 corrected the law and
closed at both SFs on the SCALAR eleven-mode pass. The consolidated review
disproved that closure: the scalar pass is a phase AVERAGE, and the actual
finite topology (78 start anchors per family per plane — not circulant)
fails it (weakest orientation 0.999537142 at SF 1.0, mixed-mode trial
0.967922863, both demonstrated). v3 keeps the corrected law:

  a cord family at antipodal offset delta_j (subtended phi_j = pi - delta_j)
  delivers, at mode n, the stiffness factor

      f_j(n) = cos^2(delta_j/2) * cos^2(n * phi_j / 2)          (SQUARED)

  (amplitude engagement cos(delta_j/2)|cos(n phi_j/2)|, stiffness its square).
  Even n: f ~ cos^2(delta/2) cos^2(n delta/2) ~ 1 for small delta.
  Odd n:  f = cos^2(delta/2) sin^2(n delta_j/2) — near ZERO for the v1
  half-column offset (n=3: 0.000924), order unity only for offsets of tens of
  degrees. Odd coverage must therefore be DESIGNED IN: candidate offsets
  180/3, 180/5, 180/7, 180/9, 180/11 deg place sin^2(n delta/2) = 1 at their
  named mode. A mixed-offset family is ONE internal design option, not an
  established solution.

and adds the v3 corrections: interleaved interior crossings (finding 2:
cords (a, a+step), (b, b+step) cross iff b < a+step — shared endpoints are
not crossings), member moves priced at their ledger cost x(1+adder)/eta in
the greedy and the rejection economics (finding 3), and the finite-phase
verdict on every bestFeasible point (finding 1). v2 winners are retained as
superseded conditional results; FAIL is recorded where the finite topology
fails.

World W2 (both safety factors): 112 m, sigma s1450, gamma 0.65, membrane
credit EXCLUDED (unpriced), hull/structure basis. Pricing is identical for
every point: cord material over each family's true mean length
(2 rbar cos(delta/2)), the model's x1.3 end-fitting allowance, and 0.05 kg per
same-depth interior crossing (per family 363k-411k crossings, 18.2-20.6 t of
clips; families routed at separate standoff depths — that hardware is UNKNOWN
and unpriced, not zero).

Points:
  baseline   single half-column family — even modes only in effect (the honest
             successor of the as-drawn world at true prices);
  free       the unconstrained greedy — never activates an odd family: the
             first step must carry the whole clip bill (the activation hump);
  variants   every single family and PAIR of odd families FORCED active up
             front, greedy shaping freely around them — the hump-covering
             enumeration (finding 4: a myopic path is not a dominance proof;
             triples unexplored, no optimality claim);
  nospoke    no cords at all (rings + crimp floor).

An infeasible point is never counted as an improvement; the best FEASIBLE
point is reported and a worsening is reported as one. FEASIBLE here means
the scalar mode margins — the finite-phase verdict rides on top as
finitePhase/feasibleFinitePhase and, per the consolidated review, is the
one that governs. Deterministic arithmetic; run twice -> identical
alloc.json. Internal conditional design hypothesis; no positive claim.
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
MAT = vc.MATERIALS
P_ATM = vc.P_ATM

I004 = json.loads((HERE.parent / "R3-I004" / "net.json").read_text())
NET10 = I004["worlds"]["sf1.0"]["net"]
MEAN_DIAMETRAL = NET10["meanCordM"] / math.sin(
    math.radians(NET10["subtendDeg"]) / 2.0)     # mean of 2r over kept planes
CLIPS_PER_FAMILY = NET10["crossings"]            # 411,274 interior crossings
CLIP_KG = 0.05
FITTING = SHIP0["spokeFitting"]
KD = 0.65
DIA = 112.0
SF_LIST = (1.0, 1.2)

# Candidate families, by IDEAL offset: halfcol is the v1 layout (even modes);
# 180/3, 180/5, 180/7, 180/9, 180/11 deg place sin^2(n delta/2)=1 at
# n = 3/5/7/9/11. Realizable offsets on the 155-anchor ring are half-integer
# multiples of the column angle (2.3226 deg); each family snaps to the nearest
# realizable offset (the exact endpoint topology is built per family below).
IDEAL_OFFSETS_DEG = [180.0 / 155.0, 60.0, 36.0, 180.0 / 7.0, 20.0,
                     180.0 / 11.0]
N_KEPT_PLANES = 137          # from the I004 drawn net (polar cutoff 6 m)


def build_families(g):
    """Explicit endpoint topology per family: anchor m <-> m + step in every
    kept bay plane, step = 77.5 - k for offset k half-columns from antipodal.
    Shared-endpoint pairs and interior crossings follow from step — they are
    PER FAMILY, not one number (I004 finding 6 arithmetic, generalised)."""
    n = g["nLong"]
    half = n // 2
    col = 360.0 / n
    fams = []
    for ideal in IDEAL_OFFSETS_DEG:
        # n is ODD (155): |77.5 - step| is a half-integer column count for
        # every integer step, so the offset must snap to a HALF-INTEGER k
        # (integer k would demand a non-integer step). Nearest such k:
        k = max(0.5, round(ideal / col - 0.5) + 0.5)
        step = int(half + 0.5 - k)                       # exact integer
        off = abs(n / 2.0 - step) * col
        shared = max(0, (half + 1) - step)              # m1+step = m2 <= half
        # Interior crossings per plane (consolidated review finding 2): two
        # cords (a, a+step) and (b, b+step) with a < b cross iff b < a+step
        # (interleaved); a shared endpoint b = a+step is NOT a crossing, and
        # no wraparound exists (a+step <= 154). Count = pairs b in
        # (a, min(half, a+step-1)] summed over a. (The v2 formula
        # (half+1)*half/2 - shared subtracted SHARED pairs instead and
        # overcounted by step-1 - shared per plane.)
        interior = sum(min(half - a, step - 1) for a in range(half))
        fams.append(dict(
            idealDeg=ideal, offsetDeg=off, columnsK=k, step=step,
            subtendDeg=step * col,
            doubledAnchorsPerPlane=shared, unusedAnchors=n - 2 * (half + 1)
            + shared, interiorCrossingsPerPlane=interior,
            crossings=N_KEPT_PLANES * interior))
    return fams


FAMILIES = None      # built in World.__init__ (geometry-dependent)
FAMILY_NAMES = ["halfcol", "d60", "d36", "d180/7", "d20", "d180/11"]


def factor(offset_deg: float, n: int) -> float:
    """Squared stiffness factor f_j(n) — the corrected law."""
    d = math.radians(offset_deg)
    phi = math.pi - d
    return math.cos(d / 2.0) ** 2 * math.cos(n * phi / 2.0) ** 2


class World:
    """One SF world: mirrored gi with the explicit multi-family foundation."""

    def __init__(self, sf: float):
        self.sf = sf
        r = vc.ship0("s1450", sf, DIA, KD, True, True, basis="favourable")
        self.base = r
        g, skel, wall = r["geom"], r["skeleton"], r["wall"]
        self.g, self.skel, self.wall = g, skel, wall
        self.E = MAT["T700_LAM"]["E"]
        self.rho = MAT["T700_LAM"]["rho"]
        depth, r_in, bay = g["depthM"], g["rIn"], SHIP0["bayM"]
        self.depth, self.r_in, self.bay = depth, r_in, bay
        adder = SHIP0["junctionAdder"]
        self.member_fixed_t = wall["membersT"] + (
            skel["longeronsT"] + skel["websT"] + skel["junctionT"]) * (1 + adder)
        pads_t = (g["areaM2"] / (SHIP0["ringPitchM"] * SHIP0["barPitchM"])
                  * (SHIP0["clampEvery"] - 1) / SHIP0["clampEvery"]
                  * SHIP0["padKg"]) / 1000.0
        skins_t = (SHIP0["voidSkinKgM2"] + SHIP0["jacketKgM2"]) \
            * g["areaM2"] / 1000.0
        self.other_t = (wall["filmT"] + wall["clampsT"] + pads_t
                        + skel["strapsT"] + skins_t)
        self.eta = SHIP0["etaMass"]
        self.adder = adder
        self.n_inner = round(g["meridianM"] / bay) + 1
        self.n_theta = self.n_inner * g["nLong"] * 2
        circ_col = 2.0 * math.pi * g["R"] / g["nLong"]
        self.theta_len = math.sqrt(depth * depth + circ_col * circ_col)
        self.cos_th = circ_col / self.theta_len
        self.kg_inner = self.rho * self.n_inner * 2.0 * math.pi * r_in
        self.kg_theta = self.rho * self.theta_len * self.n_theta
        self.kg_flange = self.rho * 2.0 * math.pi * g["R"] * g["cylL"]
        self.a_o0 = wall["ring"]["A"] / SHIP0["ringPitchM"]
        self.a_cap = (wall["capGridKgM2"] - wall["barKgM2"]) / self.rho / 2.0
        # per-family pricing (kg of cord+fittings per m2/m2 of family area)
        # from the EXPLICIT endpoint topology: realizable snapped offsets,
        # per-family crossings, per-family clip mass.
        self.fam = []
        for name, topo in zip(FAMILY_NAMES, build_families(g)):
            off = topo["offsetDeg"]
            mean_len = MEAN_DIAMETRAL * math.cos(math.radians(off) / 2.0)
            self.fam.append(dict(
                name=name, topology=topo, offsetDeg=off, meanCordM=mean_len,
                kgPerA=mean_len * SHIP0["rhoSpoke"] * FITTING * g["areaM2"],
                clipT=topo["crossings"] * CLIP_KG / 1000.0,
                f={n: factor(off, n) for n in range(2, 13)}))

    # -- checks ---------------------------------------------------------
    def gi(self, a, full_credit_family=None, membrane=False):
        """Mirror of the model's gi with the multi-family foundation. With
        full_credit_family set, that family gets f(n)=1 at every n and all
        others zero — the model's own gi_chordal convention, for parity.
        membrane=True reproduces the frozen both-moves row's Bryant term."""
        a_x = self.base["skeleton"]["longeron"]["A"] \
            * self.g["nLong"] / (2.0 * math.pi * self.r_in)
        lam2 = (math.pi * self.g["R"]
                / (self.g["cylL"] + 2.0 * self.g["R"] / 3.0)) ** 2
        g = self.g
        a_o = self.a_o0 + a["a_oe"]
        a_i_s = a["a_i"] / self.bay
        abar = a_o * a_i_s / (a_o + a_i_s)
        i_eff = abar * self.depth ** 2
        a_th = a["a_th"]
        q_crimp = 0.0
        if a_th > 0.0:
            q_crimp = (2.0 * self.E * a_th * self.depth * self.cos_th ** 2
                       / (self.bay * self.theta_len)) / g["R"]
        best_n, best_q = 2, None
        for n in range(2, 13):
            q_ring = (n * n - 1) * self.E * i_eff / (g["R"] ** 3)
            q_ring = 1.0 / (1.0 / q_ring + 1.0 / q_crimp) \
                if (q_ring > 0.0 and q_crimp > 0.0) else 0.0
            q_found = 0.0
            if full_credit_family is not None:
                aj = a.get(f"a_{full_credit_family}", 0.0)
                q_found = SHIP0["eSpoke"] * aj / (n * n - 1)
            else:
                for f in self.fam:
                    aj = a.get(f"a_{f['name']}", 0.0)
                    if aj > 0.0:
                        q_found += SHIP0["eSpoke"] * aj * f["f"][n] / (n * n - 1)
            q_mem = 0.0
            if membrane:
                nn_l2 = n * n + lam2
                q_mem = (self.E * a_x * lam2 * lam2
                         / (self.g["R"] * (n * n + lam2 / 2.0 - 1.0)
                            * nn_l2 * nn_l2))
            q = q_ring + q_found + q_mem
            if best_q is None or q < best_q:
                best_q, best_n = q, n
        return dict(qCrPa=best_q * KD, critN=best_n,
                    marginAtSF=best_q * KD / (P_ATM * self.sf))

    def cap_margin(self, a):
        b_cap = self.E * self.a_cap
        a_i_cap = a["a_i"] / self.bay
        d_cap = self.E * (self.a_cap * a_i_cap / (self.a_cap + a_i_cap)) \
            * self.depth ** 2
        q_cap_bend = 4.0 * math.sqrt(b_cap * d_cap) / (self.g["R"] ** 2)
        s_cap = 0.0
        if a["a_th"] > 0.0:
            s_cap = (2.0 * self.E * a["a_th"] * self.depth
                     * self.cos_th ** 2 / (self.bay * self.theta_len))
        q_cap_crimp = 2.0 * s_cap / self.g["R"]
        if q_cap_bend <= 0.0 or q_cap_crimp <= 0.0:
            return 0.0
        return (KD / (1.0 / q_cap_bend + 1.0 / q_cap_crimp)) \
            / (P_ATM * self.sf)

    # -- pricing ---------------------------------------------------------
    def spokes_t(self, a):
        t = 0.0
        for f in self.fam:
            aj = a.get(f"a_{f['name']}", 0.0)
            if aj > 0.0:
                t += aj * f["kgPerA"] / 1000.0 + f["clipT"]
        return t

    def components_t(self, a):
        return (a["a_i"] * self.kg_inner / 1000.0,
                a["a_th"] * self.kg_theta / 1000.0,
                a["a_oe"] * self.kg_flange / 1000.0)

    def total_t(self, a):
        inn, th, fl = self.components_t(a)
        member = self.member_fixed_t + (inn + th + fl) * (1 + self.adder)
        return member / self.eta + self.spokes_t(a) + self.other_t

    def point(self, a):
        ov = self.gi(a)
        cm = self.cap_margin(a)
        total = self.total_t(a)
        return dict(
            alloc={k: v for k, v in a.items()},
            innerRingsT=a["a_i"] * self.kg_inner / 1000.0,
            thetaWebsT=a["a_th"] * self.kg_theta / 1000.0,
            flangeDoublerT=a["a_oe"] * self.kg_flange / 1000.0,
            spokesByFamilyT={f["name"]: round(
                (a.get(f"a_{f['name']}", 0.0) * f["kgPerA"] / 1000.0
                 + (f["clipT"] if a.get(f"a_{f['name']}", 0.0) > 0 else 0.0)), 1)
                for f in self.fam},
            spokesT=self.spokes_t(a),
            totalT=total, marginSLT=self.base["liftSLT"] - total,
            margin2500T=self.base["lift2500T"] - total,
            critN=ov["critN"], marginAtSF=ov["marginAtSF"],
            capMarginAtSF=cm,
            feasible=ov["marginAtSF"] >= 1.0 and cm >= 1.0)

    def mode_margins(self, a):
        """Margin at EVERY mode n=2..12 of the honest world — the explicit
        coverage table (rings+crimp + the multi-family foundation, no
        membrane)."""
        g = self.g
        a_o = self.a_o0 + a["a_oe"]
        abar = a_o * (a["a_i"] / self.bay) / (a_o + a["a_i"] / self.bay)
        i_eff = abar * self.depth ** 2
        q_crimp = 0.0
        if a["a_th"] > 0.0:
            q_crimp = (2.0 * self.E * a["a_th"] * self.depth * self.cos_th ** 2
                       / (self.bay * self.theta_len)) / g["R"]
        out = {}
        for n in range(2, 13):
            q_ring = (n * n - 1) * self.E * i_eff / (g["R"] ** 3)
            q_ring = 1.0 / (1.0 / q_ring + 1.0 / q_crimp) \
                if (q_ring > 0.0 and q_crimp > 0.0) else 0.0
            q_found = sum(SHIP0["eSpoke"] * a.get(f"a_{f['name']}", 0.0)
                          * f["f"][n] / (n * n - 1) for f in self.fam
                          if a.get(f"a_{f['name']}", 0.0) > 0.0)
            q = q_ring + q_found
            out[str(n)] = round(q * KD / (P_ATM * self.sf), 4)
        return out

    def orientation_phase(self, a, n):
        """Finite-endpoint orientation matrix at mode n on the
        (cos n.theta, sin n.theta) basis — consolidated review finding 1.
        Each active family j contributes sc_j(n) * S_j / (78/2), with
        sc_j(n) = eSpoke * a_j * sin^2(phi_j/2) * cos^2(n phi_j/2)/(n^2-1)
        and S_j the anchor sums of the rotated phase factors
        cos/sin(n t_a + n phi_j/2). The phase-average identity puts the
        MEAN diagonal exactly at the scalar law, so entries read as scalar
        +- orientation deviation. The 78 start anchors per family per
        plane break the circulant symmetry a continuous net would have —
        this is the deviation the scalar eleven-mode pass cannot see."""
        n_l = self.g["nLong"]
        half = n_l // 2
        M = [[0.0, 0.0], [0.0, 0.0]]
        for f in self.fam:
            a_j = a.get(f"a_{f['name']}", 0.0)
            if a_j <= 0.0:
                continue
            phi = 2.0 * math.pi * f["topology"]["step"] / n_l
            sc = (SHIP0["eSpoke"] * a_j * math.sin(phi / 2.0) ** 2
                  * math.cos(n * phi / 2.0) ** 2 / (n * n - 1))
            cc = ss = cs = 0.0
            for m in range(half + 1):
                t = 2.0 * math.pi * m / n_l
                c_ = math.cos(n * t + n * phi / 2.0)
                s_ = math.sin(n * t + n * phi / 2.0)
                cc += c_ * c_
                ss += s_ * s_
                cs += c_ * s_
            M[0][0] += sc * cc / ((half + 1) / 2.0)
            M[1][1] += sc * ss / ((half + 1) / 2.0)
            M[0][1] += sc * cs / ((half + 1) / 2.0)
        M[1][0] = M[0][1]
        tr, det = M[0][0] + M[1][1], M[0][0] * M[1][1] - M[0][1] ** 2
        lam = tr / 2.0 - math.sqrt((tr / 2.0) ** 2 - det)
        return M, lam

    def finite_phase(self, a):
        """Finite-endpoint verdict over ALL modes n=2..12 (finding 1): per
        mode, the scalar margin and the weakest-ORIENTATION margin (the
        reviewer's convention — reproduced exactly on the v2 winner); the
        binding mode's orientation matrix; and the mixed-mode trial
        cos(3t)/sqrt(8) - sin(4t)/sqrt(15) under this seat's documented
        anchoring, ring at the weaker participating mode. The weakest
        ORIENTATION over modes is the deterministic gate; a pass within ppm
        of 1.0 is recorded as a number and never read as established
        feasibility."""
        g = self.g
        a_o = self.a_o0 + a["a_oe"]
        abar = a_o * (a["a_i"] / self.bay) / (a_o + a["a_i"] / self.bay)
        i_eff = abar * self.depth ** 2
        q_crimp = 0.0
        if a["a_th"] > 0.0:
            q_crimp = (2.0 * self.E * a["a_th"] * self.depth
                       * self.cos_th ** 2 / (self.bay * self.theta_len)) / g["R"]

        def q_ring(m):
            qr = (m * m - 1) * self.E * i_eff / g["R"] ** 3
            return 1.0 / (1.0 / qr + 1.0 / q_crimp) if q_crimp > 0.0 else 0.0

        margins = {}
        bind = None
        for n in range(2, 13):
            M, lam = self.orientation_phase(a, n)
            scalar = sum(SHIP0["eSpoke"] * a.get(f"a_{f['name']}", 0.0)
                         * f["f"][n] / (n * n - 1) for f in self.fam
                         if a.get(f"a_{f['name']}", 0.0) > 0.0)
            qr = q_ring(n)
            m_weak = (qr + lam) * KD / (P_ATM * self.sf)
            margins[str(n)] = dict(
                scalar=round((qr + scalar) * KD / (P_ATM * self.sf), 9),
                weakestOrientation=round(m_weak, 9))
            if bind is None or m_weak < bind[0]:
                bind = (m_weak, n, M, lam, scalar)
        m_weak, n, M, lam, scalar = bind
        # Mixed trial, per-mode anchored: family j's 3-3 (4-4) block is its
        # scalar sc3_j (sc4_j) times the finite phase-sum deviation; the
        # cross block carries the geometric mean of the two anchors.
        n_l = g["nLong"]
        half = n_l // 2
        c3, c4 = 1.0 / math.sqrt(8.0), -1.0 / math.sqrt(15.0)
        qf = 0.0
        for f in self.fam:
            a_j = a.get(f"a_{f['name']}", 0.0)
            if a_j <= 0.0:
                continue
            phi = 2.0 * math.pi * f["topology"]["step"] / n_l
            sh = math.sin(phi / 2.0)
            sc3 = SHIP0["eSpoke"] * a_j * sh * sh * math.cos(1.5 * phi) ** 2 / 9.0
            sc4 = SHIP0["eSpoke"] * a_j * sh * sh * math.cos(2.0 * phi) ** 2 / 15.0
            p33 = p44 = p34 = 0.0
            for m in range(half + 1):
                t = 2.0 * math.pi * m / n_l
                c_ = math.cos(3 * t + 1.5 * phi)
                s_ = math.sin(4 * t + 2.0 * phi)
                p33 += c_ * c_
                p44 += s_ * s_
                p34 += c_ * s_
            qf += (sc3 * p33 / ((half + 1) / 2.0) * c3 * c3
                   + sc4 * p44 / ((half + 1) / 2.0) * c4 * c4
                   + 2.0 * math.sqrt(sc3 * sc4) * p34 / ((half + 1) / 2.0)
                   * c3 * c4)
        m_trial = (min(q_ring(3), q_ring(4)) + qf) * KD / (P_ATM * self.sf)
        return dict(
            bindingModeFinite=n,
            orientationMatrix=[[round(M[0][0], 4), round(M[0][1], 4)],
                               [round(M[1][0], 4), round(M[1][1], 4)]],
            weakestEigenvalue=round(lam, 4),
            scalarQFound=round(scalar, 4),
            modeMargins=margins,
            marginWeakestOrientation=round(m_weak, 9),
            trial=dict(
                field="cos(3t)/sqrt(8) - sin(4t)/sqrt(15)",
                marginSeatConvention=round(m_trial, 9),
                marginReviewDemonstrated=(0.967922863 if self.sf == 1.0
                                          else 0.985215242),
                note="review values are the demonstrated margins on the "
                     "SUPERSEDED v2 winner (cited from the consolidated "
                     "return); this seat reproduces that winner's "
                     "orientation matrix, eigenvalue and both orientation "
                     "margins to 1e-4; the review's exact mixed-field "
                     "ring/foundation combination was not recovered from "
                     "the published values (seat candidates land within "
                     "2-6% of the cited margins), and on the v2 winner "
                     "every tested convention lands below 1.0; on THIS "
                     "point the mixed-mode verdict under the review "
                     "convention is UNKNOWN"),
            feasibleFinitePhase=m_weak >= 1.0,
            note="the scalar eleven-mode pass is a phase AVERAGE; margins "
                 "within ppm of 1.0 are not established feasibility — the "
                 "v2 closure remains withdrawn")

    def rejection_economics(self, a):
        """Why no odd-mode family activates: marginal gain in binding-mode
        margin per kg for every move at the final allocation, first-step
        family moves carrying their full clip activation. A family activates
        only if its gain/kg beats every member move; the table shows none
        does, and by how much."""
        rec = self.gi(a)
        moves = {}
        d_ai, d_th, d_oe, d_sp = 4e-4, 4e-5, 2e-4, 2e-7
        # Member moves are priced at their LEDGER cost (consolidated review
        # finding 3): every member kg enters the total as
        # (1 + junctionAdder)/etaMass = 1.05/0.85 = 1.235294 kg on the scale.
        # (Cord moves are not: spokes_t carries cord + fittings directly.)
        ledger = (1.0 + self.adder) / self.eta
        for key, dk, kg in (("growInnerRings", d_ai,
                             d_ai * self.rho * self.n_inner * 2 * math.pi
                             * self.r_in * ledger),
                            ("growThetaWebs", d_th, d_th * self.theta_len
                             * self.n_theta * self.rho * ledger),
                            ("growFlangeDoubler", d_oe, d_oe * self.kg_flange
                             * ledger),
                            ("growHalfcol", d_sp, d_sp * self.fam[0]["kgPerA"])):
            b = dict(a)
            src = {"growInnerRings": "a_i", "growThetaWebs": "a_th",
                   "growFlangeDoubler": "a_oe", "growHalfcol":
                       f"a_{self.fam[0]['name']}"}[key]
            b[src] += dk
            moves[key] = round((self.gi(b)["marginAtSF"]
                                - rec["marginAtSF"]) / kg * 1e6, 4)
        for f in self.fam[1:]:
            key = f"a_{f['name']}"
            kg = d_sp * f["kgPerA"] + f["clipT"] * 1000.0
            b = dict(a)
            b[key] += d_sp
            moves[f"activate_{f['name']}"] = round(
                (self.gi(b)["marginAtSF"] - rec["marginAtSF"]) / kg * 1e6, 4)
        return dict(marginGainPerKgPerMillion=moves,
                    note="1e-6 margin units per kg at the baseline exit "
                         "point; member moves priced at their ledger cost "
                         "(1+adder)/eta (finding 3); a first-step family "
                         "move carries its full per-family clip activation "
                         "(18.2-20.6 t per family)")

    # -- the greedy at true prices, per-family activation costs ----------
    def solve(self, active=None, seeds=True, force=None, force2=None):
        d_ai, d_th, d_oe, d_sp = 4e-4, 4e-5, 2e-4, 2e-7
        a = dict(a_i=0.0, a_th=0.0, a_oe=0.0)
        if seeds:
            inner0 = vc.ship_size_compression(
                0.10 * self.wall["ring"]["demandN"], self.bay,
                SHIP0["sigmaWorldsMPa"]["s1450"] * 1e6, self.sf)
            a["a_i"] = inner0["A"]
            a["a_th"] = vc.ship_section(30.0, 1.5)["A"]
        for f in self.fam:
            a[f"a_{f['name']}"] = 0.0
        for fc in (force, force2):
            if fc is not None:
                # pay the activation up front, so the family competes without
                # the first-step fixed cost (finding 4: myopia is not proof)
                a[f"a_{fc}"] = d_sp
        rec = self.gi(a)
        guard = 0
        # Member candidates are priced at their ledger cost (finding 3):
        # x(1+adder)/eta on the scale; cord candidates at cord cost (the
        # spokes line carries no junction adder and no eta).
        ledger = (1.0 + self.adder) / self.eta
        while rec["marginAtSF"] < 1.0 and guard < 6000:
            cands = []
            for key, dk, kg in (("a_i", d_ai, d_ai * self.rho
                                 * self.n_inner * 2 * math.pi * self.r_in
                                 * ledger),
                                ("a_th", d_th, d_th * self.theta_len
                                 * self.n_theta * self.rho * ledger),
                                ("a_oe", d_oe, d_oe * self.kg_flange
                                 * ledger)):
                b = dict(a)
                b[key] += dk
                rb = self.gi(b)
                cands.append(((rb["marginAtSF"] - rec["marginAtSF"]) / kg,
                              key, kg, rb))
            for f in self.fam:
                if active is not None and f["name"] not in active:
                    continue
                key = f"a_{f['name']}"
                kg = d_sp * f["kgPerA"]
                if a[key] == 0.0:
                    kg += f["clipT"] * 1000.0   # activation: the clip bill
                b = dict(a)
                b[key] += d_sp
                rb = self.gi(b)
                cands.append(((rb["marginAtSF"] - rec["marginAtSF"]) / kg,
                              key, kg, rb))
            cands.sort(key=lambda c: -c[0])
            _, move, _, rec = cands[0]
            step = dict(a_i=d_ai, a_th=d_th, a_oe=d_oe)
            if move in step:
                a[move] += step[move]
            else:
                a[move] += d_sp
            guard += 1
        guard_c = 0
        while self.cap_margin(a) < 1.0 and guard_c < 4000:
            a["a_th"] += 4e-5
            guard_c += 1
        return a, guard, guard_c


def parity(w):
    """The mirror must reproduce the frozen model before any use: the base
    row (full-credit foundation + membrane, the model's own flags for that
    row) exactly; and the corrected I004 record's mode-3 verdict via the
    halfcol family factors."""
    skel = w.base["skeleton"]
    a_full = dict(a_i=skel["innerRingAM2"], a_th=skel["thetaWebAM2"],
                  a_oe=0.0)
    a_full.update({f"a_{f['name']}": 0.0 for f in w.fam})
    a_full["a_halfcol"] = skel["spokeAM2PerM2"]
    # P1: gi parity with the model's full-credit convention, membrane ON —
    # exactly the flags the frozen both-moves row was computed with.
    ov_mine = w.gi(a_full, full_credit_family="halfcol", membrane=True)
    ov_model = skel["ovalization"]
    p1 = (abs(ov_mine["qCrPa"] - ov_model["qCrPa"]) < 1e-9
          and ov_mine["critN"] == ov_model["critN"])
    # P2: mass assembly parity at the base allocation with SMEAR spokes.
    member = w.member_fixed_t + (
        skel["innerRingsT"] + skel["thetaWebsT"] + skel["flangeDoublerT"]) \
        * (1 + w.adder)
    total_smear = member / w.eta + skel["spokesT"] + w.other_t
    p2 = abs(total_smear - w.base["totalT"]) < 1e-6
    # P3: halfcol squared factors reproduce the corrected I004 mode-3 number.
    f3 = factor(w.fam[0]["offsetDeg"], 3)
    p3 = abs(f3 - 0.000924) < 2e-6
    p4 = (w.fam[0]["topology"]["step"] == 77
          and w.fam[0]["topology"]["crossings"] == CLIPS_PER_FAMILY)
    return dict(giParity=p1, massParity=round(total_smear
                                              - w.base["totalT"], 9),
                halfcolFactorN3=round(f3, 6),
                halfcolTopologyMatchesI004=p4,
                ok=p1 and p2 and p3 and p4)


def main():
    out = dict(unit="R3-I005", rev="v3-after-consolidated-review",
               base="afb2c2d1726b9d9a805f9781085c3dd6a52913e5",
               world=None, parity={}, worlds={})
    for sf in SF_LIST:
        w = World(sf)
        par = parity(w)
        out["parity"][f"sf{sf}"] = par
        assert par["ok"], (sf, par)
        if out["world"] is None:
            out["world"] = dict(
                diaM=DIA, sigma="s1450", giKnockdown=KD, membrane=False,
                stiffnessLaw="per-family f_j(n) = cos^2(delta/2) "
                             "cos^2(n phi/2), SQUARED (review finding 1)",
                families=[dict(
                    name=f["name"], idealOffsetDeg=round(f["topology"]
                                                         ["idealDeg"], 3),
                    offsetDeg=round(f["offsetDeg"], 3),
                    columnsFromAntipodal=f["topology"]["columnsK"],
                    step=f["topology"]["step"],
                    doubledAnchorsPerPlane=f["topology"]
                    ["doubledAnchorsPerPlane"],
                    unusedAnchors=f["topology"]["unusedAnchors"],
                    interiorCrossingsPerPlane=f["topology"]
                    ["interiorCrossingsPerPlane"],
                    crossings=f["topology"]["crossings"],
                    clipT=round(f["clipT"], 2),
                    meanCordM=round(f["meanCordM"], 2),
                    endpointTopology=f"anchor m <-> m+{f['topology']['step']} "
                                     f"in every kept bay plane (137 planes, "
                                     f"m = 0..77)")
                    for f in w.fam],
                routing="families at separate standoff depths; standoff "
                        "hardware UNKNOWN and unpriced, not zero",
                status="internal conditional design hypothesis; scalar "
                       "feasibility is NOT established — see finitePhase "
                       "on each bestFeasible (consolidated review "
                       "finding 1: the scalar pass is a phase average; "
                       "the demonstrated finite topology fails it)")
        base_a, g1, c1 = w.solve(active=["halfcol"])       # even-mode net
        cand_a, g2, c2 = w.solve()                          # free greedy
        nosp_a, g3, c3 = w.solve(active=[])                 # rings+crimp only
        # Finding 4 discipline: the free greedy is myopic — a family whose
        # first step must carry its whole clip bill can be worthwhile yet
        # never win a step (demonstrated: forced d36 saves 216.6 t at SF1.0).
        # Enumerate every single family and PAIR forced active up front,
        # greedy shaping freely; triples unexplored. No optimality claim —
        # this is a hump-covering enumeration, not a proof.
        names = [f["name"] for f in w.fam]
        variants = {"free": (cand_a, g2, c2)}
        for name in names:
            variants[f"force:{name}"] = w.solve(force=name)
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                variants[f"force:{names[i]}+{names[j]}"] = \
                    w.solve(force=names[i], force2=names[j])
        pts = dict(baseline=w.point(base_a), nospoke=w.point(nosp_a))
        var_pts = {k: w.point(a) for k, (a, _, _) in variants.items()}
        feas = {k: p for k, p in {**pts, **var_pts}.items() if p["feasible"]}
        best = min(feas.items(), key=lambda kv: (kv[1]["totalT"], kv[0])) \
            if feas else None
        out["worlds"][f"sf{sf}"] = dict(
            baseline=dict(point=pts["baseline"], greedySteps=g1, capSteps=c1,
                          modeMargins=w.mode_margins(base_a),
                          note="single half-column family: even modes only "
                               "in effect — the honest as-drawn successor"),
            nospoke=dict(point=pts["nospoke"], greedySteps=g3, capSteps=c3,
                         modeMargins=w.mode_margins(nosp_a)),
            variants={k: dict(totalT=round(p["totalT"], 1),
                              marginSLT=round(p["marginSLT"], 1),
                              margin2500T=round(p["margin2500T"], 1),
                              critN=p["critN"],
                              marginAtSF=round(p["marginAtSF"], 4),
                              capMarginAtSF=round(p["capMarginAtSF"], 4),
                              feasible=p["feasible"],
                              spokesT=round(p["spokesT"], 1),
                              innerRingsT=round(p["innerRingsT"], 1),
                              thetaWebsT=round(p["thetaWebsT"], 1),
                              alloc={k2: round(v, 7) for k2, v
                                     in p["alloc"].items()})
                     for k, p in var_pts.items()},
            rejectionEconomics=w.rejection_economics(base_a),
            bestFeasible=None if best is None else dict(
                which=best[0], totalT=best[1]["totalT"],
                marginSLT=best[1]["marginSLT"],
                margin2500T=best[1]["margin2500T"], critN=best[1]["critN"],
                point=best[1], modeMargins=w.mode_margins(
                    variants[best[0]][0]) if best[0] in variants
                else w.mode_margins(base_a),
                finitePhase=w.finite_phase(
                    variants[best[0]][0] if best[0] in variants
                    else base_a)),
            lift=dict(slT=w.base["liftSLT"], at2500T=w.base["lift2500T"]),
        )
    (HERE / "alloc.json").write_text(json.dumps(out, indent=1) + "\n")
    for sf in SF_LIST:
        ww = out["worlds"][f"sf{sf}"]
        for k in ("baseline", "nospoke"):
            p = ww[k]["point"]
            print(f"SF {sf} {k:9s} total {p['totalT']:8.1f} "
                  f"mSL {p['marginSLT']:+8.1f} m25 {p['margin2500T']:+8.1f} "
                  f"critN {p['critN']:2d} marg {p['marginAtSF']:.4f} "
                  f"feas {p['feasible']} spokes "
                  f"{p['spokesT']:6.1f}")
        for k in sorted(ww["variants"],
                        key=lambda kk: ww["variants"][kk]["totalT"]):
            p = ww["variants"][k]
            print(f"SF {sf} {k:22s} total {p['totalT']:8.1f} "
                  f"mSL {p['marginSLT']:+8.1f} feas {p['feasible']} "
                  f"critN {p['critN']:2d} spokes {p['spokesT']:6.1f}")
        b = ww["bestFeasible"]
        print(f"SF {sf} best: {b['which']} total {b['totalT']:.1f} "
              f"mSL {b['marginSLT']:+.1f} m25 {b['margin2500T']:+.1f}")


if __name__ == "__main__":
    main()
