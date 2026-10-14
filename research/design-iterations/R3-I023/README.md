# R3-I023 — the signed static pressure load path

Status: v1.3 (consolidated correction of the sole first review — eight
findings, all addressed in this file and `loadpath.py`),
2026-10-14. Base: the CORRECTED R3-I015 record and the I019 **v3.1**
termination record in the same checkout — both input files are
**hash-guarded at load** in `loadpath.py`, so this unit cannot silently
run against stale inputs again (its v1.0 run did exactly that: it
consumed the pre-correction termination record; v1.1 pinned the v2
bytes). Internal conditional design hypothesis; no positive claim;
`floatsToday` not shown.

**Verdict (CONDITIONAL on the declared common-strain model): the pressure
resultant is TRACED film arc → barrel rings + inner rail as one box →
caps and longerons, and the cord web carries no pressure increment; its
static duty is its own pretension equilibrium. The claimed CLOSURE of that
tracing is WITHDRAWN: under the declared common-strain kinematics the
connected theta webs also contract, and their inward pulls overwhelm the
inner-ring cuts — ~1.0 MN per station unresolved at the corrected areas
(`equilibriumDeficit`; the sole first review demonstrated the deficit and
this unit reproduces its arithmetic). Every strain, service-force and
slack number below is a model diagnostic, not a physical prediction; the
retained construction's compatibility/force balance is UNSOLVED here.
Within the model: at the barrel the box strain (5.95‰ on the corrected
box — the inner rail is the retained replacement section ALONE,
1 453.5 mm²; the v1.2.x 2 507 mm² double-credit is a labelled failed
calculation) is 2.98× the declared pretension strain (2.0‰), so cords
tensioned before pump-down go slack over ~91–94% of the planes (65/69
d60, 62/68 d11) — against a foundation-loss tolerance BOUND from the
records at **0.081% rigid licensed** on the binding n=5 margin (the
QUOTABLE value; the drawn-termination compliant state computes 0.087%
on the v3 consistent spring law — an extrapolation beyond the rigid
anchor, reported and not claimed). The record's stability PASS therefore
rides on an assembly step it does not state — and the v1.2.x claim that
the existing studs provide it at zero mass cost is WITHDRAWN: restoring
tension through the existing studs needs ~0.58 m of combined take-up at
the longest representative cord against 0.254 m of combined stud LENGTH
before thread engagement. Any install-after-evacuation or added-travel
construction is UNQUALIFIED with UNKNOWN parts and mass. The earlier
~234 kN reading survives only as a signed, mechanically inadmissible
hypothetical (it would require cord compression). Full-hull closure, the
bolted station connection's laminate capacities, stud/thread/nut
capacity and the cord strength remain UNKNOWN.**

## Sign convention (the whole unit is signed)

Outward normal `n`; `δp = p_in − p_out = 0 − 101325 = −101325 Pa`: the
vacuum lineage's **inward** traction. The record's `P_ATM` magnitudes are
`|δp|`. Nothing in this unit turns the positive magnitude into internal
overpressure, a helium envelope or an outward reaction. The priced
film/bar/ring wall and the caps/longerons **carry** the pressure (traced
under the DECLARED model — see the withdrawal in free body 2); the
membrane term stays excluded from the licensed stability calculation
exactly as the record excludes it — no continuous pressure shell is
invented here.

## Free body 1 — the film strip (declared one-way drape)

The film spans 0.5 m between barrel rings with the declared quarter-span
trough (sag 62.5 mm, trough radius 0.53125 m, `sin α = 8/17 = 0.4706`,
`cos α = 15/17 = 0.8824` at the supports). A circular one-way membrane
under uniform normal pressure has no tangential traction, so its
equilibrium fixes a **constant** strip tension `T = p·R_tr = 53.83 kN/m`
along the whole arc — there is no trough/support split. The record's
one-way price `p·R_tr/2 = 26.91 kN/m`, **doubled** for mass "until a
drape analysis licenses the doubly-curved credit", is the two-curvature
PRICING reference: the doubling stands as pricing, and the doubled
thickness is exactly what carries the real constant tension (53.83 kN/m
through a strip priced for twice 26.91). The support reactions:

```
        ring                                      ring
         |                                        |
         |   \  support tangent (alpha to chord)   /   arc r = 0.53125 m
         |    \                                __/    T = p R_tr = 53.83 kN/m
         |     \        trough, sag 62.5 mm   /       CONSTANT along the arc
         |      \____________________________/
         |<----------- chord 0.5 m ----------->|
         ^            ^ inward traction           ^
         |  radial component per edge            |
         |  = T sin a = 25.33 kN/m INWARD        |  axial component
         |________ p * s_r = 50.66 kN/m _________|  = T cos a = 15p/32
                    (radial balance closes          = 47.5 kN/m along the
                     exactly: 2 x 25.33 = 50.66)     ring axis, per support
```

A tension-only film cannot supply compression. Each interior barrel ring
receives `p·s_r = 50.66 kN/m` inward from its two adjacent strips (the
full tributary band, no double count) **plus** the axial components of
every strip pair meeting there — `T·cos α = 47.5 kN/m` each, equal and
opposite between adjacent strips, so they cancel on interior rings. At
the cap edges that cancellation is absent: the uncancelled axial
traction is exported in the boundary ledger as an explicit UNSOLVED
junction quantity (below). No membrane stability credit is taken
anywhere in this unit.

## Free body 2 — the barrel ring (envelope, R = 56 m)

```
   ...o o o o... ring circle R = 56, 577 rings at s_r = 0.5 m
      |     |
      v     v   w = p s_r = 50.66 kN/m inward, uniform (n = 0)
   +-----------------------------------+
   |  ring closes its own cut:         |   N = w R = 2.837 MN
   |  hoop COMPRESSION                 |   section: tube OD174 x 6
   +-----------------------------------+   A = 3167 mm2, braced 2.27 m
                                           Euler-governed capacity
                                           2.892 MN -> util 0.981 alone
```

This reproduces the record's own sizing demand (`P·s_r·R`) from the free
body. New here: the box behind it. The theta webs brace the inner rail to
the four barrel rings of each bay (4×3 167 mm²). **v1.3 correction:** the
inner rail is the retained replacement section ALONE — 1 453.5 mm², the
allocation record's `a_i`, which prices the ENTIRE replacement rail (the
v1.2.x unit added the pre-replacement skeleton section on top for a
2 507 mm² double-credit: a labelled failed calculation, pinned in the
record as `aInnerV122M2`; no second ring is invented and nothing else in
the inherited bill is changed to preserve old answers). The declared
crimp kinematics requires both rails to share one hoop strain, so the
smeared box (A_box = 14 120 mm² per bay) carries the band load
`p·bay·R = 11.35 MN` at model strain `ε = 5.95‰`, which **reduces** the
barrel ring to util 0.88 (slack cords) / 0.95 (pretensioned, worst d11
plane). The record sized each ring alone — conservative, not unsafe. The
inner rail's added area rides on the box webs for local stability (not
re-derived; stated).

**Withdrawal of the claimed box closure (v1.3):** the one-hoop-strain
state is an ASSERTED kinematics, not a solved equilibrium. Under it the
connected straight theta webs contract too, and their inward pulls
(`2·E·a_th·ε·depth/L_web` ≈ 1.05 MN per station at the corrected inputs)
overwhelm the inner-ring cuts' outward push (≈ 47 kN): ≈ 1.01 MN per
station unresolved — the sole first review demonstrated exactly this with
saved values (979 829 N vs 76 005 N, 903 829 N unresolved, even at the
inflated area) and this unit carries the arithmetic as a labelled
diagnostic (`equilibriumDeficit`) rather than a closure. No reaction is
invented and no stiffness, geometry, pretension or load-share coefficient
is tuned to force a pass: the retained construction's
compatibility/force balance — with the webs' stiffness participating in
the station equilibrium — is the unit's declared next change, and every
ε_box-, service-force- and slack-derived number in this README is
CONDITIONAL on the declared model.

## Free body 3 — both ends of a representative cord

Cords are chords of their own plane's circle: `L = 2r·sin(φ/2)`, both ends
at the same plane (φ = 120.77° d60, 162.58° d11). The two representative
cords, drawn with both ends and the rail reactions (equal and opposite
transfers at each cut), with the corrected spring lengths (free run
between socket mouths and the effective spring of the drawn termination —
grip 60 mm d60 / 97 mm d11, stud/body series compliance per end):

```
 d60, shortest (nose plane r = 7.051 m):
        chord 12.260 m | free 12.124 m | effective spring 12.242 m  T = 6.809 kN
        station a o--------------------------o station b
        phi = 120.77 deg   each end pulls the rail INWARD
        per-end radial component = T sin(phi/2) = 5.92 kN
        tangential components of the chord pair cancel by symmetry
        rail takes the pair: 2 x 5.92 = 11.84 kN at this station

 d11, longest (r = 49.539 m):
        chord 97.934 m | free 97.724 m | effective spring 97.904 m  T = 17.797 kN
        station a o----------------------------------------------o station b
        phi = 162.58 deg   per-end radial = 17.59 kN
        station pair resultant 35.18 kN inward at r = 49.5 m
```

At installation each station carries **two** cord ends (the departing and
the arriving cord of the same family), symmetric about the station radial —
the tangential parts cancel, the radial parts add.

## Free body 4 — the anchor station (both incident cord axes, hardware)

The corrected termination's securing construction: the socket is epoxide-
potted over **60 mm (d60) / 97 mm (d11)** of cord — sized on the
transferring cord/resin interface — and the block is **bolted** through
the doubler pad into the ring wall (3 × M10 Ti-6Al-4V through-bolts,
45 [50] mm dimensioned shanks spanning block+pad+ring-wall+nut =
41 [47] mm minimum; internal backing nuts; the bond film carries zero
credit):

```
                 cord 2 axis (arriving)          cord 1 axis (departing)
                      \                               /
                       \  T = 17.8 kN               /  T = 17.8 kN
                        \                         /
      doubler pad  ______\_______________________/______  200 x 140 x 3 mm
      (0.134 kg)  |      socket body OD 38 mm            |
      on the rail |  pot grip 97 mm | stud M23x127 | jam |
                  |         anchor block 64 x 46 x 30 mm |
                  |______________________________________|
                     ^ ^ ^  3 x M10 Ti through-bolts, 16 mm pitch
                            (internal backing nuts; single shear)
                         inner rail (tube, 1 453.5 mm2 retained
                            replacement section)
                  resultant 2 T sin(phi/2) = 35.2 kN INWARD at e = 51 mm
                  outside the rail centroid -> station moment 1.79 kN m
                  (d60: 11.8 kN at e = 36.8 mm -> 0.44 kN m)
                  bolt set shear utilisation 0.25 [0.74] vs the worst
                  taut-window pair load — metallic part sized
```

Force and moment balance in physical coordinates at the station: the two
cord-end tensions, the socket bearing, the stud axial load, the block
bearing on the pad, the bolt group shear and the pad/ring contact close
the free body with equal-and-opposite transfers at each interface. The
**moment** enters the rail locally through the eccentricity `e` (block
half-width + socket radius — the corrected block and socket OD are
unchanged from the values used before, so the moments stand at 0.44 /
1.79 kN·m); the bolted connection's laminate bearing, block bending and
pull-through capacities are not derived, and the stud pair's
thread/nut capacity is likewise not derived (the record's fitting value
is a demand, not a capacity) — station bending capacity is
**UNKNOWN**, stated as such.

## The kinematic finding (exact), and the three states

With the box at hoop strain ε, the **anchor-centre chord** `2r·sin(φ/2)`
shortens by exactly `ε·L_chord` (both ends sit on the same contracted
plane) — an identity of this geometry. The cord, however, strains on its
**effective spring length** `L_eff = L_chord − L_grip + 2·l_ser` (the
drawn termination's declared model: free run between socket mouths plus
the mid-grip/stud compliance of both ends), so the strain coupling is
`κ = L_chord/L_eff` (1.00146 d60 / 1.00176 d11 on the shortest cords; the
no-transfer variant bounds it at 0.9966/0.9967). The held cord strain
after a contraction ε is `(ε_set − κε)/(1+βκ)`, where ε_set is the
installed set strain — the compatible hold set is `ε₀(1+βκ)`, the
nominal flat set is `ε_set = ε₀` (ε₀ the fixed nominal 2‰; the flat-set
form describes the saved flat-set forces 6.324/14.492 kN, the
compatible hold set the 6.809/17.797 kN equilibrium) — and
`β = E_cord·a_pc·(155 sin(φ/2)/π)/(E_lam·A_box)` is the cord→rail→cord
strain loop gain (v1.3 recomputes it on the corrected box). Two
consequences, and one bookkeeping distinction the v1.2.x unit missed:

1. **βκ is not small**: 0.0767 (d60) / 0.2281 (d11). A flat `ε₀ = 2‰` set
   holds only **6.324 / 14.492 kN** (92.9% / 81.4% of nominal). Holding
   the committed totals requires the compatible installed SET strain
   `ε₀(1+βκ) = 2.153‰ / 2.456‰`. Three different books now carry three
   different numbers: the **equilibrium tension** at that set (rail free
   to respond) is exactly `EA·ε_set/(1+βκ)` = 6.809 / 17.797 kN; the
   **restrained installation load** `EA·ε_set` = 7.33 / 21.86 kN is the
   force only if the rail is held undeformed during the set — a different,
   explicitly named state; and the priced fitting value (17.7 / 46.3 kN)
   is a design DEMAND that sized the bond grip, NOT a stud/thread/nut
   capacity — stud capacity is UNKNOWN and no cover verdict is claimed.
2. **The vacuum state dominates βκ**: at the barrel `ε_box = 5.95‰`
   (pressure band 11.35 MN over E·A_box, model strain). Since
   `κ·ε_box/ε₀ = 2.981`, the S1 sequence (set at assembly, then pump
   down) drives the cords slack wherever `κ·ε_box ≥ ε₀(1+βκ)`, i.e.
   envelope radius above 20.2 m (d60) / 23.1 m (d11), against 18.8 m at
   flat ε₀ — 65/69 d60 planes and 62/68 d11 planes (94% / 91%; the
   no-transfer bound gives the same counts), the surviving nose/tail
   planes holding as little as 1.089 / 0.737 kN. The binding stability
   margin (n=5) tolerates a total foundation stiffness loss of
   **0.081% rigid licensed** — READ from the corrected records, not
   asserted — which is the QUOTABLE bound; the drawn-termination
   compliant state computes 0.087% on the v3 consistent spring law
   (η > 1), an extrapolation beyond the rigid anchor that is reported
   and NOT claimed, so the finding rests on the rigid value either way.
   Losing ~91–94% of the family planes un-licenses the PASS (within the
   declared model). **The assembly sequence is load-bearing — and the
   reset is NOT available through the existing hardware (below).**
3. **The taut-branch identity carries its compliance feedback**: while
   taut, `ΔT/T₀ = κ·ε_box / (ε₀·(1+βκ))` — the v1.2.x form without the
   `(1+βκ)` denominator is withdrawn — and the branch clamps at slack
   (`T = 0`) once the numerator crosses zero. Distinguish throughout:
   the compatible installed LENGTH (set by ε_set alone), the EQUILIBRIUM
   tension at that set, and the RESTRAINED installation load.

| state | sequence | cord tension at vacuum | rails | notes |
|---|---|---|---|---|
| S1 | set at assembly → pump | **0 (slack)** over 94%/91% of planes | box carries pressure alone (model); barrel util 0.88 | un-licenses the stability margin (model) |
| **S2** | pump → set studs to hold ε₀ | 6.809 / 17.797 kN (= committed) | pressure + N₀ 292/868 kN per plane; barrel util 0.90/0.95, inner rail 0.57/0.60 | **requires an installation construction the record does not carry** (resetTravel below) |
| S1′ | set deep at assembly | holds 6.809 / 17.797 kN | same as S2 | restrained set load 27.6 / 74.9 kN = **1.56× / 1.62× the priced fitting demand** (a demand comparison — stud CAPACITY unknown); hardware mass UNPRICED |

The S1′ set strains (8.115‰ d60) put the cord at ~568 MPa in the
RESTRAINED (undeformed-rail) installation book — that stress is
E·ε_set unrelieved by rail compliance; the unrestrained equilibrium
force book is lower — the cord is
UHMWPE-class (Dyneema-type) per its source documentation, and its
strength and creep behaviour at that stress are **UNKNOWN** (the assumed
E 70 GPa + ρ 970 pair is a model pair, not a fibre spec, and is never
combined with any UTS here).

**Reset travel (the withdrawn zero-mass claim).** For any assembly that
tensions before pump-down and re-sets after it, restoring a cord's
tension takes combined take-up of order `chord × ε_box` at the model's
own barrel strain: **0.583 m** at the longest representative cord
(d11, chord 97.934 m) — against the two M23×127 studs' **0.254 m of
combined stud LENGTH**, before any thread engagement allowance. The
existing studs cannot provide the travel (>2× short on the binding
case; the d60 shortest representative's 0.073 m take-up — a
barrel-strain diagnostic — is below its 0.158 m combined stock LENGTH
only as a gross comparison, and usable thread travel after
engagement/construction limits is UNKNOWN; the uniform-barrel-strain
figure "chord above 0.254 m / ε_box ≈ 42.7 m, plane radius above
~21.6 m" is a hypothetical comparison at the barrel strain, not an
actual all-plane threshold — the implemented local strain
ε_box(min(56, r+depth)) is smaller at cap-plane radii, so no universal
cap-plane travel bound is claimed). Installing
different compatible cord lengths after evacuation, or an added-travel
mechanism, is UNQUALIFIED with UNKNOWN parts and mass: a force
comparison or a re-tuned set length does not establish it, and the
strain state it would target is itself conditional on the withdrawn
equilibrium.

## Member utilization (SF1.0 construction)

| member | demand | capacity | util |
|---|---|---|---|
| barrel ring (smeared share, slack cords) | 2.545 MN | 2.892 MN (Euler) | 0.88 |
| barrel ring (smeared share, worst d11 plane) | 2.740 MN | 2.892 MN (Euler) | 0.95 |
| inner rail (yield check, same plane) | 1.257 MN | 2.108 MN (σ_c, sourced) | 0.60 |
| longeron (end-cap thrust, ×155) | 6.440 MN each | 6.449 MN (Euler) | 0.999 |
| film | constant strip tension 53.8 kN/m | priced doubled thickness | by construction |

At SF1.2 on the *same* construction the barrel reads 1.06 (worst plane
1.12) and the longeron 1.20 — the record's convention handles adverse SF
by a separately sized world, not by this construction; the readings are
tabled, not adjudicated. All smeared-box rows are CONDITIONAL on the
declared common-strain model (withdrawn closure, free body 2). No
knockdown is applied to these statics: KD = 0.65 prices the licensed
buckling margins, and applying it here as well would double-count.

## Boundary reactions and closure

Longerons: `p·πR²/155 = 6.440 MN` each, ×155 = 998.3 MN = `p·πR²`
exactly — the axial closure holds at the sizing identity. Caps: membrane
`p·R/2 = 2 837 kN/m` into the priced grid; the junction diagonals carry
the same thrust inward to the longerons. **Signed resultant, kept
separate from any scalar area:** each cap carries `−p·πR² = −998.3 MN`
(inward, toward midship); the barrel structure returns the SAME total
thrust as axial compression `p·πR²`, transferred serially and counted
once: the `pR/2` membrane per rim metre feeds the cap/rim/junction
path, which delivers the identical `p·πR²` total to the 155 longerons
(the `p·πR²/155` each is that same thrust shared, not an addition to
it) — and the net closed-hull resultant is zero.

**Exterior tributary reconciliation (v1.3 correction):** the loaded film
surface is the EXTERIOR envelope (R = 56 m) — a 112 m cylinder (cylL =
2R) closed by two hemispherical caps, total 78 816 m². The caps are
**exactly half** the envelope (4πR² = 2πR·cylL = 39 408 m² each), not a
~12% polar remainder; the 224 exterior barrel bands of `2πR·s_r` tile
the cylinder once (39 408 m²); the longitudinal cuts at the 155 anchor
stations divide each band among its cords — a kinematic split, not a
solved distribution. The v1.2.x "counted once, 88%" statement summed
`2π·(inner cord-plane radii)·bay = 69 469 m²` — inner radii (49.5385 m
at the barrel, cap planes below), not the pressure surface: withdrawn,
retained as the labelled failed pin. **Unsolved boundary reactions,
exported explicitly:** the film's uncancelled axial traction at the cap
edges (47.5 kN/m, free body 1) together with the moment/shear
redistribution between the cap membrane (pR/2) and the first barrel
ring; the longeron/ring compression distribution through the nose
taper; local bending inside one bay of the box. **Full-hull closure
beyond the sizing identity is UNKNOWN** and returned as such.

## The earlier 234 kN reading — a signed, inadmissible hypothetical

`(P·2π·r_max·bay)/(2·155·sin(φ/2))` = 234.0 kN (d60) / 205.8 kN (d11) —
reproduced exactly (asserted against the corrected record) and retained
ONLY as a **signed, mechanically inadmissible hypothetical**. With inward
pressure and inward tensile cord pulls, removing the ring support leaves
`−P_band − 2·155·T·sin(φ/2) = 0`, so a web that resisted the band
directly would require **negative T — compression**, which these cords
cannot supply. The magnitudes are that bypassed-rings free body's
compression requirement: NOT an alternative tensile load path, and NOT
this construction's demand (the film closes on the ring box; the honest
static cord demand is the pretension itself — 6.8 / 17.8 kN, ~34×
smaller — with compatibility only ever *relaxing* it). The withdrawn
98.2%-of-ultimate figure also divided by a T700 tow UTS, an invalid
pairing with the assumed cord material; the corrected ledger carries no
cord strength at all, so no utilisation is computed. The termination
record consumed here is its corrected v3.1 (hash-guarded at load; its
first review's findings stand corrected as follows — eight closed in
the v2 correction; the one cord accounting boundary with the
dimensioned bolt stack, and the Pa units label, closed in the v3
correction; the spring model's mechanics were repaired in v3, and
v3's overstated physical-amplitude claims were corrected by the
immediate v3.1 successor — that correction is submitted for lead
targeted verification, and no acceptance is asserted here) — this
supersedes only its load-path interpretation, not its record.

## Material ledger (each property once, with provenance)

| item | E | ρ | strength | provenance |
|---|---|---|---|---|
| cord | 70 GPa **assumed** (inherited) | 970 **assumed** (inherited) | **UNKNOWN** — UHMWPE-class (Dyneema-type) per its source; creep UNVERIFIED; never paired with any UTS | inherited model pair; strain limit is the declared ε₀ |
| cord termination | Ti-6Al-4V 114 GPa | 4 430 | stud capacity **UNKNOWN** (2·T₀·1.3 is the design DEMAND that sized the bond grip — not a derived stud/thread/nut capacity); bond 12 MPa design shear **ASSUMED**; 3×M10 bolted attachment, shear util 0.25/0.74, laminate capacities UNKNOWN | public datasheet values (metal); priced in the corrected termination record |
| film | — | 1 560 | 5.8 GPa basis at sf 4 × eff 0.5 → 725 MPa working | record pricing basis |
| laminate (rings, rails, longerons, caps) | 135 GPa representative | 1 600 | σ_c 1.45 GPa **sourced** (SACMA SRM 1R-94); σ_t 2.86 GPa **sourced** (ASTM D3039) | Toray T700S datasheet, Vf 0.6; E and ρ are representative inputs, not coupon values |

Factors, once each: pressure/preload unfactored state (δp = −101325 Pa;
ε₀ imposed); demand SF 1.0/1.2 on pressure only; material allowable as
tabled (barrel Euler 913 MPa governs); fitting factor 1.3 on cord
hardware; capacity KD 0.65 on the stability licensing only; assembly
allowance 5% on mass only. No factor is applied twice.

## Bill (one construction, before = after)

This is an analysis-only unit: no member changes, so the bill is
line-for-line the **corrected** termination record's — the drawn sockets
(60/97 mm grips), dimensioned bolted attachments (M10 45/50 mm shanks,
1.41 t) and the ×1.5-with-assembly-share sensitivity are all priced in
it: total **2 233.4 t**, SL **+16.4 t**, 2 500 m **−476.1 t**, spokes
line **245.42 t**, SF1.2 mass failure carried at 2 562.4 t / −312.6 t
(read from the record's own `sf12` block and asserted at load — no
hard-coded SF1.2 prose remains)
against the corrected completed baseline. The potted cord swallowed
inside the anchor-centre chord is priced once inside the cord line
(the v2 record's separate 0.34 t tow line double-counted it and is
gone); gas and buoyancy counted once. (The v1.0 run of this unit
copied the pre-correction bill — 2 230.7 t, +19.1, −473.4, stacked
×1.5 +5.3 — superseded; v1.1 pinned the v2 bill, spokes 245.37 t —
superseded by this re-pin.) Nothing required-but-unsized is zeroed:

- the installation/reset construction at pump-down: the existing studs'
  travel is insufficient (reset-travel arithmetic above), and
  install-after-evacuation or added-travel alternatives carry UNKNOWN
  parts and mass;
- the retained construction's theta-web equilibrium — the declared
  common-strain model's closure is withdrawn (free body 2);
- deeper-ε₀ hardware if S1′ is chosen (restrained set demand 1.56×/1.62×
  the priced fitting demand — a demand comparison, stud capacity unknown;
  **UNPRICED**, no fitted coefficient offered);
- the bolted station connection's laminate bearing/bending/pull-through
  capacities vs the 0.44 / 1.79 kN·m moments;
- full-hull axial closure beyond the sizing identity;
- cord material strength.

**Next concrete change:** solve the retained construction's
compatibility/force balance — a model in which the theta webs' stiffness
participates in the station equilibrium instead of being bypassed by an
asserted common strain — and re-derive the pressure strain, service
forces and slack counts under that solved model; separately, write the
assembly/installation construction (evacuation sequence, cord-length
control, or qualified added travel with priced parts and mass) into the
record before any stability margin is re-licensed.

## Checks and reproduction

`python3 research/design-iterations/R3-I023/loadpath.py` writes
`loadpath.json`. The v1.3 output was produced by ONE bounded execution
(recorded with full receipts in the unit's evidence file: argv, source
hash, wall/CPU/RSS, enforced limits, raw stdout/stderr, output hash; one
earlier invocation failed on a correction-side assert literal and is
preserved there too) — no determinism re-run is claimed for v1.3.
Dependency guards: the R3-I019 v3.1 and corrected R3-I015 input files are
sha256-pinned at load, with value pins (rev, grips 60/97, bill 245.42 t,
dependency string) — a stale or mutated input aborts the run. The SF1.2
case is READ from the record's own `sf12` block and asserted
(afterSpokes, afterT, afterMarginSL) — no hard-coded SF1.2 narrative
remains. Parity asserts: per-cord sections, T₀, per-plane preload totals
and the 234.0 / 205.8 kN figures reproduce the corrected termination
record; the shortest cord's spring lengths re-derive from the family
constants and pin the record's own `freeLength` entry; the n=5 margins
are READ from the records (rigid licensed and drawn compliant)
replacing v1.0's prose literals; the ring (2.837 MN) and longeron
(6.440 MN) demands reproduce the sizing formulas; the film balances hold
exactly (`2·T·sinα = p·s_r`, the arc-carry form `T = p·s_r/(2 sinα) =
p·R_tr`, and the axial component `T·cosα = 15p/32`); the corrected
inner-rail area pins against the allocation record and the withdrawn
v1.2.x sum pins at 0.002507 m²; the envelope halves assert exactly
(cylinder = caps = 4πR², 224 bands tiling the cylinder); the
equilibrium-deficit diagnostic reproduces the sole first review's
witness row (979 829 / 76 000 / 903 829 N) on its own literals; the box
split sums to the total; the held-tension solves are the closed forms of
the 1×1 linear systems (S2 holds exactly the committed T₀, and the
restrained/equilibrium installation books satisfy
`EA·ε_set/(1+βκ)` identically); slack is monotone in plane radius; the
κ-coupled barrel identity `κ·ε_box/ε₀ = 2.981` holds at the outermost
d60 plane; block dimensions re-derive the record's block masses.
Bounds: one pure-Python process, analytic free bodies + 1×1 solves, no
matrix over 22 coordinates, no solver/sweep/optimizer/FEA, no model fit;
measured wall/RSS in the unit's evidence file. Documentation checks:
`make readmecheck linkcheck buildercheck`. No model, gate or programme
file edited; no sibling unit's files touched by this reconciliation.
