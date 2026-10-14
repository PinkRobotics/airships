# R3-I019 — one drawn termination and the mixed-field taut window

Status: v3.1, 2026-10-14 — a text-only correction of v3's amplitude
claims; every numeric result is unchanged. Source: the corrected
[R3-I015 record](../R3-I015/README.md); this v3.1 text correction
follows the unit's v3 spring-model and accounting correction.
Internal conditional design hypothesis; no positive claim;
`floatsToday` not shown. v1 mis-sized the bonded grip, mis-identified
the cord material, evaluated the wrong first-slack endpoint and
under-charged two sensitivities; v2 corrected eight of the eleven
demonstrated defects; v3 closes the accounting-boundary and units
defects and finishes what v2's verification left open — ONE signed
installed spring model (every eta on the same denominator as the
slack law), the SIGNED mixed-packet first-loss result (no
absolute-value severity counts), a buildable dimensioned bolt stack,
ONE cord accounting boundary (the double-counted potted-tow line
removed) and the Pa/MPa units label — but v3's prose also claimed the
physical-amplitude class bound tight, which the coefficient-norm
equality alone does not establish; v3.1 withdraws that claim and keeps
the conservative sufficient bounds, amplitude sharpness left unproved.

**Verdict: the ideal 0.35 kg lug is replaced by a drawn, priced
termination at +16.5 t (sea level stays positive at +16.4 t), and the
taut-window statement is now signed, compliance-consistent and taken
over the occupied cords: the n=5 margin-critical field first slackens
a d180/11 cord at 25.49 mm (declared spring model), not the 50.4 mm
the v1 record quoted from a single convenient endpoint — and the
rigorous class bound for ARBITRARY mixtures stands at 4.143 mm (d60) /
5.283 mm (d11).** The mixed-packet slack adversary −x\* now has its
exact first-loss result: each family's own target cord is the first
loser, at 5.860 mm vector norm (d60) / 7.471 mm (d180/11) — the
coefficient-norm Cauchy–Schwarz equality case, which fixes those
vector-norm scales exactly. It does NOT make the class bound tight:
amplitude sharpness would additionally require ‖x‖ = √2·w(x), which
these packet fields do not attain (the recorded unit-norm sampled
amplitudes are 2.4047/2.3532 against the 1/√2 ≈ 0.7071 equality
value), so the class bound remains a conservative sufficient bound,
sharpness unproved. The cord
is UHMWPE-class (Dyneema-type) with ASSUMED inherited inputs and
UNKNOWN strength — v1 called it a T700-class carbon tow and quoted
98.2% of a borrowed ultimate; that pairing is withdrawn. The grip is
sized on the transferring cord/resin interface (60/97 mm drawn; the
v1 52/84 mm sat at 13.77/13.78 MPa against the assumed 12 MPa), the
block is BOLTED to the ring through the doubler pad (3 × M10 Ti ×
45/50 mm shanks spanning the full dimensioned stack, +1.41 t,
priced), and the SF1.2 comparison is measured against the corrected
completed baseline: 2,562.4 t, sea level −312.6 t — still fails,
inherited.

## Material identity, stated first

The cord's 70 GPa / 970 kg/m³ inputs are documented at their source
(`tools/ship_scoping.py:138-139`) as a **Dyneema-class (UHMWPE) cord
modulus, creep unverified** (recorded as EPa = 70e9 Pa — the v2 key
`EMpa` held the Pa value behind an MPa label; relabelled, numerics
unchanged). This unit therefore claims: **no carbon identity, no
borrowed fibre ultimate, no utilisation figure — the cord's qualified
strength is UNKNOWN.** Swage compatibility with a UHMWPE cord is
creep/slip-sensitive and NOT QUALIFIED (the v1 carbon-crushing
argument is withdrawn; neither swage nor pot is thereby qualified or
disqualified). The drawn potted socket is a SELECTED hypothetical
construction on an ASSUMED 12 MPa design bond shear — an assumption,
not a qualified UHMWPE termination. The laminate (rings, rails,
doubler pads) keeps its record-priced T700S basis where the record
sourced it.

## The drawn cord end (dimensioned, sized on the transferring interface)

```
                 socket, longitudinal section (d60 size; d180/11 in [])
                 cord axis ----> insertion from the right

      stud M14x79 [M23x127] Ti      body Ti-6Al-4V
   +------------------------+  +------------------------------+
   |OOOOOOOOOOOOOOOOOOOOOOOO|  | ############################  |-- nose 8 mm
   +--------+---------------+  | #....epoxy pot, Lg = 60 [97]#  |  (strain
            |  jam nut        | #.mm over bore 9.0 [14.6] mm #  |   relief)
   +--------+  hex AF 17 [28],| |#.tow Ø7.87 [12.72] enters -->#  |
   |OOOOOOOO|  t = 12.6 [20]+| |#..............bore...........#  |
   +--------+----------------+ +------------------------------+
            |<-- body OD 23.5 [38.0] mm, length 76 [113] mm -->|

   per-end mass: body 0.125 [0.485] + resin 0.002 [0.006]
                 + stud 0.055 [0.232] + nut 0.009 [0.039]
                 = 0.191 kg [0.762 kg]      (removed lug: 0.35 kg flat)
```

Grip length is DERIVED on the interface that actually transfers load —
the cord/resin cylinder `π·d_cord·Lg`, not the larger bore perimeter
the v1 sizing used: T_fit = 2·T₀·1.3 (worst taut-window tension with
the record's own `spokeFitting` factor) gives required grips
59.68/96.48 mm unrounded → **60/97 mm drawn = 7.62 cord diameters**
(identical ratio because T_fit ∝ d²). At the v1 52/84 mm the cord
interface ran 13.77/13.78 MPa against the assumed 12 MPa — a
counterexample to the v1 fitting-load sizing, not a demonstrated
failure at the lower operating load. The other transferring surface is
checked: the resin annulus on the socket wall `π·d_bore·Lg` sees
10.38 MPa, inside the same assumed value.

## Free length, both-end compliance, and SIGNED slack

ONE datum set and ONE spring law, defined once (d60 [d180/11], shortest
cord): the anchor centre is the **grip back face** (where cord tension
passes into the socket body metal); the socket mouth sits nose + grip
inboard of it; the cord runs free between socket mouths
**L_free = 12.124 [17.181] m** (= anchor-centre chord 12.260 [17.391]
minus 2 × (nose 8 + grip 60 [97]) mm — the potted embedded cord lies
INSIDE the anchor-centre chord); each end contributes an equivalent
cord length **L_a = 59 [90] mm** = nose + half the grip (the stretch up
to the MID-GRIP TRANSFER CENTROID — a declared assumption) + 21 [33] mm
of stud/body series compliance. Incremental strain is
**Δε = ΔL/(L_free + 2·L_a)**; slack when it reaches −ε₀. The stud and
seat lie BEYOND the anchor centre: priced in the socket hardware,
carried in the spring model as that series compliance — nothing of the
cord lies beyond the anchor centre.

Every quantity that divides by a length uses THIS denominator — slack
thresholds, the per-family drawn eta (reference length = the mean
anchor-centre chord, the coupled matrix's pin-jointed ideal) and the
coupled energy: **eta = mc/(L_free,mean + 2·L_a) = 1.000257 [1.000381]**
— the v2 eta mc/(mc + 2·L_a) treated the whole mean chord as free cord
and is SUPERSEDED. Eta exceeds 1 because the bonded half-grip
shortens the active cord by more than the stud/body series adds back
(per cord: grip − 2·l_ser = 17.9 [30.6] mm) — the drawn chain is
STIFFER than the pin-jointed ideal, and the no-transfer variant (whole
embedded cord stretches) still bounds the taut window above at
12.302 [17.458] m.

Every projected extension is SIGNED. The v1 "adversarial slack" packet
x\* = g_j\*/‖g_j‖\* actually **stretches** its target cord: +ε₀, i.e.
T = 2·T₀ at its amplitude — a stretch identity, not slack; the slack
adversary is −x\*. On the declared law every strain scales by
**L_min/L_eff = 1.001464 [1.001760]** (the functional carries 1/L
inside), so at the historical chord-scale amplitudes 14.111 [17.611] mm
the target sits at T/T₀ = 2.001464 [2.001760] — already past 2·T₀ —
and the same amplitude of −x\* would take it to **−0.001464 [−0.001760]
× T₀: already slack** (linear prediction; the exact first-loss scale is
the chord scale divided by the same factor: 14.090 [17.580] mm).
Even on the v1 chord basis, sign reversal alone left 0.751%/0.846% of
pretension standing (the v1 η factors 0.99249/0.99154, kept as labelled
counterexamples).

**The signed mixed-packet first-loss result** (the finite occupied
member set, enumerated exactly: 155 station phases × both families'
innermost planes; the plane dimension closed by the exact monotonicity
of L_eff(r); no |·| anywhere; first loss read from signed tension
T = T₀(1 − w·proj/ε₀)): for each family's −x\* the **first loser is the
packet's own target cord** (the cross-family scan stays clear — the
other family's nearest cord keeps 10.9 kN under the d60 packet), at
vector-norm scale **5.860 mm (d60) / 7.471 mm (d180/11)** — exactly
ε₀/‖g_eff‖, the coefficient-norm Cauchy–Schwarz equality (attained in
the coefficient norm ONLY). Amplitude sharpness would additionally
require ‖x‖ = √2·w(x), which these fields do not attain: the sampled
first-loss amplitudes 14.090/17.580 mm sit well above the sufficient
class bounds 4.143/5.283 mm — and a sampled maximum is itself only a
lower bound on the continuous maximum — so the class bound below is
CONSERVATIVE, sharpness unproved. At that scale the most-stretched
surviving cord of the stricken family holds 9.31 kN = 1.37·T₀ (d60
packet) / 23.8 kN = 1.34·T₀ (d180/11 packet); signed severity: under
either packet exactly 1 cord of the stricken family sits within 0.1%
of the loser and 3 within 10% (the old v1/v2 counts were
absolute-value based and are withdrawn); amplitudes quoted via w_of
are GRID-SAMPLED (2¹⁶ points) and labelled as sampled — the exact
continuous statements are the class bounds and this enumeration.

## n=5 first slack over the OCCUPIED cords (the corrected threshold)

The v1 record's 50.4 mm evaluated the a=0 endpoint only. The true
first-slack threshold minimises over occupied cords/families/planes,
and the controlling cord follows analytically from the station
topology — 5θ quantises the 155 stations into **31 phases**
(155/5 = 31), and the strain denominator is monotone in r, so the
innermost plane controls (no field search):

| field (u = w·f(5θ)) | d60 chord → declared | d180/11 chord → declared | controlling start (mod 31) |
|---|---|---|---|
| +cos 5θ | 26.798 → 26.759 mm | 25.669 → 25.624 mm | d180/11: 11 |
| −cos 5θ | 26.660 → **26.621 mm** | 25.537 → **25.492 mm** | d180/11: 27 |
| ±sin 5θ | 26.695 → 26.655 mm | 25.570 → 25.525 mm | d180/11: 19/4 |

The binding case is **−cos 5θ on the innermost d180/11 plane:
25.492 mm** (declared model; 25.537 mm chord basis; 25.635 mm
no-transfer) — the ±sin 5θ degenerate partner sits 33 µm above it.
At that amplitude the slack cord's tension is zero and the
most-stretched cord of the same family holds 35.5 kN (0.996 × 2·T₀;
13.58–13.65/35.5–35.69 across the four fields) — the stretch target
is a different cord than the first loser, and both are named.

## The class bound for ARBITRARY mixtures (unchanged in kind, shifted by the denominator)

u(θ) = Σ_{n=2..12}[c_n cos nθ + s_n sin nθ]; every cord's strain is
EXACTLY linear in the 22 RADIAL coefficients, ε_j = g_j·x. Two
normalisations stay distinct: the Euclidean norm on c and the PHYSICAL
amplitude w(x) = max_θ|u(θ)|, with the exact two-sided relation
‖x‖₂/√2 ≤ w(x) ≤ √11·‖x‖₂. (The I015 eigen machinery normalises
y = √D·c with D_nn = n²−1 — y_c5 = 1 maps to c5 = 1/√24 =
0.204124145; cross-basis comparisons carry that mapping.)

| family | worst single mode | adversarial packet (declared law) | RIGOROUS class bound |
|---|---|---|---|
| d60 (r=7.051, L=12.260) | n=3, 14.105 mm | first loss 5.860 mm norm (stretch 14.090; hist. chord 14.111) | **4.143 mm** (chord 4.149) |
| d180/11 (r=8.797, L=17.391) | n=11, 17.685 mm | first loss 7.471 mm norm (stretch 17.580; hist. chord 17.611) | **5.283 mm** (chord 5.292) |

No field of physical amplitude w can push any cord past |ε| ≤
√2·‖g_j‖·w (Cauchy–Schwarz + the exact norm relation), and the ideal
chord model also gives |ε| ≤ w/r. The n=5 margins above (~25.5 mm) are
explicit-field values — nearly 5× the class bound — because a pure
mode spreads its displacement; the class bound, not any explicit field,
is the design taut window for an unrestricted mixture — and the
adversarial packet family attains the coefficient-norm equality (its
vector-norm first-loss scale is that equality case), but amplitude
sharpness does not follow: the sampled first-loss amplitudes sit
~3.4×/~3.3× above the bound, so it remains conservative and its
sharpness is unproved.

## Ring attachment (per station — the connection v1 did not draw)

```
   securing detail, radial section at one anchor station
   (cord pull is INWARD, toward hull centre; ring wall at bottom)

        Ti anchor block 50x36x24 [64x46x30] mm
        2 x cord sockets, studs M14 [M23], jam nuts
   +--------------------------------------------+
   |  doubler pad 200 x 140 x 3 mm laminate     |  <-- bond film: ZERO
   +--------------------------------------------+      capacity credit
   |  ring wall (laminate tube, 6 mm)           |
   +--------------------------------------------+
      ^  ^  ^  3 x M10 Ti-6Al-4V through-bolts, 16 mm pitch,
        internal backing nuts, SINGLE shear (conservative):
        capacity 124.4 kN vs pair load 30.8 [91.5] kN -> util 0.25 [0.74]

   the through-bolt SPANS the full stack (dimensioned, fits):
        block 24 [30] + pad 3 + ring wall 6 + nut 8
        = 41 [47] mm minimum
        + 4 [3] mm point protrusion/washers
        = shank 45 [50] mm, priced        (v2 priced 30 mm: TOO SHORT)

   pair load = 1.3 (fitting) x 2 cords x 2.T0 (worst window) x sin(phi/2)
   installation: through the adjacent bay at the 0.5 m ring pitch,
   before pump-down; stud gives +-16 [+-25] mm length adjustment
   UNKNOWN: laminate bearing, block local bending, pull-through,
   contact/creep — priced hardware, unpriced capacities
```

Station pitch at the innermost planes: 286 mm (d60, r 7.051) and
357 mm (d180/11, r 8.797) vs hardware widths 97/140 mm — FITS
(asserted). Cord accounting runs on the ONE datum of the free-length
section: the anchor centre is the grip back face, the embedded
(nose + grip) cord lies INSIDE the anchor-centre chord, and the cord
line prices FULL anchor-centre chords — so it already contains every
metre of potted cord. There is NO separate potted-tow line (the v2
0.34 t line double-counted cord already inside the chord and is
removed); the potting resin is inside the socket line; studs and seats
beyond the anchor centre are inside the socket line too. The same
boundary is applied to the nominal bill, the ×1.5 sensitivity and the
SF1.2 case.

## Full known bill (old removed once, new charged once)

| line | basis | tonnes |
|---|---|---|
| cord (incl. potted embedded runs) | unchanged from the completion | 139.51 |
| crossing clips | unchanged (1,272,705) | 63.64 |
| sockets (body+resin+stud+nut) | 21,390 × 0.191 + 21,080 × 0.762 kg | 20.14 |
| anchor blocks | 10,695 × 0.192 + 10,540 × 0.391 kg | 6.17 |
| doubler pads | 21,235 × 0.134 kg | 2.86 |
| attachment bolts+nuts (M10 × 45/50) | 10,695 × 0.064 + 10,540 × 0.069 kg | 1.41 |
| assembly 5% | on the above | 11.69 |
| **spokes line** | was 228.91 t | **245.42 (+16.5)** |

The completion's ideal-lug line is simply ABSENT from this basis: the
old spokes line carried 14.86 t of lugs plus a 0.74 t assembly share;
removing those and charging the drawn hardware (30.58 t) nets the
+16.5 t. There is no potted-tow row: the v2 0.34 t line priced cord
that the chord-priced cord line already contains (a v2 double count,
removed — the value is asserted in the code as the counterexample
pin).

| budget | total (t) | SL (t) | 2,500 m (t) |
|---|---|---|---|
| corrected completion (ideal lugs) | 2,216.9 | +32.9 | −459.6 |
| **with the drawn termination** | **2,233.4** | **+16.4** | **−476.1** |
| station-hardware ×1.5 sensitivity | — | +0.3 | — |

The ×1.5 scenario now takes its 5% assembly share ON THE INCREMENT
(+16.05 t), which the v1 arithmetic omitted (+0.69 t on the v1 bill —
the v1 residual read +5.3 t where its own numbers give +4.6 t). The
bill is a KNOWN SUBTOTAL: bolts are sized on traceable metallic single
shear, but laminate bearing, block bending and pull-through are
UNKNOWN — not a qualified all-up margin.

SF1.2 adverse case (d60+d20), against the FIXED corrected completion
baseline (2,536.9 → 2,546.1 t, its +9.2 t completion change inherited
and NOT counted here): spokes 227.66 → 243.98 t, +16.3 t of
termination, total **2,562.4 t, sea level −312.6 t — still fails**;
the mass failure is inherited and the replacement does not change its
kind.

## Sensitivities (from the corrected model)

Bond shear τ (ASSUMED, unverified): Lg ∝ 1/τ exactly — 12 → 8/20 MPa
is 150%/60% before the mm ceiling. d60 grips 90/60/36 mm, d180/11
grips 145/97/58 mm; per-end socket mass moves only 1.26/0.79× (d60)
and 1.27/0.78× (d180/11) because stud, nut and nose masses are FIXED —
socket mass does not scale with grip length. This is GEOMETRIC
sensitivity; the bond property itself is unverified. The mid-grip
transfer centroid is the other declared assumption: the no-transfer
variant shifts the first-slack thresholds and class bounds by ≤0.6%
vs the declared model (d60 26.621 → 26.752 mm, 4.143 → 4.164 mm;
d180/11 25.492 → 25.635 mm, 5.283 → 5.312 mm — all in the JSON). The
attachment bolts are now dimensioned (M10, 45/50 mm shanks);
their single-shear cap 124.4 kN and utilisation 0.25/0.74 are
unchanged, so the block shear path they enter is carried unchanged.

## Energy and pressure-work normalisation

The licensed margin is λ_n = q_n·KD/(P_ATM·SF) — the pressure work is
folded into the licensed constant KD/(P_ATM·SF) = 6.41500123365e-06
(SF=1), and M = K·KD/(P_ATM·SF) extends it to all fields. This is
numerical parity to the licensed scalar law, not a qualified
pressure-loaded structural model. The pure-mode check is numerical
parity, NOT a physical measurement, and **pure-mode blocks do not
uniquely determine the cross entries** — diag(a,b) and the matrix with
off-diagonal √(ab)/2 are both positive definite with identical
pure-mode restrictions — so the cross-mode extension is an EXPLICIT
ASSUMPTION carried from I015. Asserted here: the completed coupled
minimum equals the licensed scalar minimum (1.000811196). The drawn
per-family eta on the ONE consistent law (η = 1.000257048/1.000380871,
reference length the mean anchor-centre chord — the bonded grip
shortens the active cord by more than the stud/body series adds back)
makes the drawn chain stiffer than the pin-jointed ideal, so the
compliant-state coupled margin lands at **1.000874096 — just ABOVE
the licensed rigid 1.000811196**. That is an extrapolation of the
same linear model beyond its rigid anchor, NOT a claimed
qualification: the quotable margin remains the licensed rigid scalar
(1.000811196), and v2's 1.000438088 (built on the superseded
whole-chord denominator) is withdrawn.

## Load-path limit (whole-vehicle, retained)

The static pressure-equilibrium per-cord reference at the outermost
plane is 234 kN (d60) / 206 kN (d11) — the force the web would need IF
it resisted the band load directly, bypassing the rings; the honest
static cord demand under the ring-box load path is the pretension
itself (the R3-I023 unit in this checkout reads and supersedes it; it
is itself unreviewed). The cord's qualified strength is UNKNOWN, so NO
utilisation is computed. The model excludes the membrane that carries
global pressure equilibrium and licenses only the stability margin;
the vehicle-level pressure load path remains UNKNOWN.

## Limits

n outside 2..12 and bay-local modes: outside the family, unchanged.
Post-slack redistribution: unmodelled, no solver. Large displacement:
first-order in u/r. Membrane/global pressure path: excluded. Material
creep, contact and bond behaviour: UNKNOWN throughout. Pretension is
a stud-set force at installation on the declared spring model
(per-cord T₀ = 6.81/17.8 kN at unchanged per-plane totals
1835.2/5453.5 kN, asserted against the committed record); the
physical pressure demand reference (P·2πR·bay, no KD) is unchanged and
KD = 0.65 remains a capacity knockdown — preload and demand stay
separate books.

**Next concrete change:** qualify the cord material record and the
bond value; declare the field class the vehicle must resist (worst
gust/ascent envelope) and re-state the taut window for that restricted
class.

## Checks and reproduction

`python3 research/design-iterations/R3-I019/termination.py` writes
`termination.json`, byte-identical across runs (cmp-proven). Asserts:
v1 counterexamples reproduced — cord-interface shear 13.771544/
13.782541 MPa at the 52/84 mm grips, required grips 59.676691/
96.477784 mm, chord-basis η 0.99249/0.99154 (sign-reversal residual),
n=5 chord-law thresholds 26.797732 (d60) / 25.668698 / 25.537001 mm
(d180/11) with controlling starts 20 / 11 / 27 (mod 31), and the v1
assembly omission 0.69225 t on the v1 bill composition; the corrected
completed I015 baseline pinned (2536.9 → 2546.1 t, −296.3 t, spokes
227.66 t, base delta 9.25 t); ‖g_j‖ t_mid-independence; single-mode
n=3 coefficient 0.141792 → 14.105 mm (chord basis); per-plane preload
totals equal the committed record (0.05 kN); station-pitch-vs-hardware
FITS at both innermost planes; coupled minimum = licensed scalar
minimum (1e-9); eigen-residual < 1e-9. v3 asserts — the reviewer's
algebraic witnesses reproduced from the saved lengths to < 3e-7
(f = 1.001463729/1.001760331 vs 1.001463766/1.001760355, chord-scale
targets 2.001463766/2.001760355, ±ε₀ scales 0.998538374/0.998242738);
the eta identity mc_eff = mc − Lg + 2·l_ser (1e-12) with mc_eff < mc
and η > 1 (1.000257048/1.000380871); L_eff monotone in r asserted over
the occupied planes (innermost controls); the signed first-loss
enumeration — first loser = the packet's own target at the
Cauchy–Schwarz equality, norm 5.860/7.471 mm, remaining most-stretched
cord 9.31 kN (1.37·T₀)/23.777 kN (1.34·T₀); the removed v2 potted-tow
line re-derived (0.342 t, pinned < 0.011 t) and absent from the
bill/×1.5/SF1.2; the bolt stack fits (45/50 mm ≥ 41/47 + 3 mm) and
prices 1.41 t (0.0639/0.0691 kg per set); the ledger cord modulus
carries the unambiguous EPa = 70000000000; the drawn coupled margin
1.000874096 > licensed rigid 1.000811196 (asserted, NOT claimed as
qualification — quotable stays the licensed rigid). Bounded work:
analytic + ≤22-coordinate small-matrix only; single pure-Python
process, measured < 1 s wall, < 25 MB RSS (receipts in the unit
evidence); no solver, sweep, optimizer or model invocation.
Documentation checks: `make readmecheck linkcheck buildercheck`.
