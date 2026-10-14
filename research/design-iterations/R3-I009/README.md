# R3-I009 v2.1 — routed cord assembly, carrying the consolidated review findings and the first-review corrections

Status: v2.1, 2026-10-14. Base: the CORRECTED R3-I005 record (v3
after-consolidated-review) in the same checkout; v1 (commit `914bab52`) is
preserved below as the historical record of the superseded attempt. v2.1
carries the three mechanical-accounting corrections of this unit's first
review (first-slack from the shortest cord, declared-lug orientation state,
both-ends preload vs the physical pressure demand) — each reproduced from
the review before correcting, asserts pinning the parity. Internal
conditional design hypothesis; no positive claim; `floatsToday` not shown.

**Verdict: the engineering stands, the FEASIBILITY does not — and the
compliant state now has a demonstrated failure.** v1 claimed
"all 11 margins ≥ 1.0, SF1.0 SL +80.0 t". The consolidated I004/I005 review
disproved the scalar eleven-mode pass that claim rested on (finding 1: the
scalar pass is a phase AVERAGE — the demonstrated finite topology of the
then-winner fails it at 0.999537142 weakest-orientation / 0.967922863
mixed-mode trial), and corrected the crossing counts (finding 2) and the
ledger marginal costs (finding 3), which MOVE the R3-I005 winner (heavier:
2,207.3 t, scalar binding n=5). v2 re-priced this unit on the corrected
record: the alternating-plane arrangement still removes the standoff
problem and still prices at **−44.8 t** against the allowances it replaces
(SL arithmetic +87.3 t). The corrected winner's RIGID weakest-orientation
margin is 1.000003659 at n=5 — a pass by 3.7 ppm, inside any model
uncertainty — and the first review then demonstrated, and this revision
reproduces exactly, that the **compliant as-declared state** (declared lug
η per family) FAILS that margin: **0.999345419 at n=5** (a bounded 0.45 t
ring-growth recovery is priced below, not applied). The mixed-mode trial
verdict under the review's convention remains unresolved on this point.
The v1 closure claim is WITHDRAWN; what follows prices a layout whose
feasibility is NOT established.

## The corrections carried (from the consolidated return, reproduced before correcting)

| finding | carry into this unit |
|---|---|
| 1 finite-endpoint phase/coupling | the winner's `finitePhase` rides in `routing.json`; for global circumferential modes every occupied plane contributes identical anchor phase sums, so the alternating-plane arrangement's orientation matrix EQUALS the winner's — the routing does not change the finite-phase question, and the question is open |
| 2 crossings | per-plane counts 2,652 (d60) / 2,967 (d180/11): interleaved pairs `b < a+step`, shared endpoints excluded; clips 384,744 × 0.05 kg = 19.24 t (v1 overcounted at 2,977/2,995 → 409,073 → 20.45 t) |
| 3 ledger marginal cost ×1.2353 | moves the R3-I005 winner this unit prices: a_d180/11 8.4e-6 → 1.7e-5 m²/m², a_i 0.00185 → 0.00145, total 2,203.0 → 2,207.3 t, scalar binding n=4 → n=5 |
| mass ledger | fixed-member line 1,189.0361 t now correct in R3-I005 |

## The two arrangements, one decision (unchanged in kind, re-priced)

Option A — both families in every plane, held at axial depths ±0.30 m by a
standoff post at every anchor point per family (38,086 posts). The post is
a cantilever IN SERIES with the cord foundation. The corrected winner's
binding-mode margin (n=5, 1.0008) tolerates **0.47%** total foundation
loss: holding the no-buyback line needs 20.8 MN/m per post (66 mm solid
steel, 307 t); sized instead to half the earlier 5%-per-end
anchor-compliance point, posts alone cost ~121 t against a +42.5 t
allowance, and mode 5 then still needs ring buyback. **REJECTED.**

Option B — the families occupy disjoint bay planes: d60 at even indices of
the 137 kept planes (69 planes, both polar caps), d180/11 at odd indices
(68). Cords terminate directly at their plane's ring anchor fittings: zero
standoff, zero axial offset, zero between-family contact anywhere. The
family's licensed total section concentrates in the planes it occupies
(Ø11.1 mm / Ø17.9 mm — the corrected winner doubles the d180/11 section),
and the axial-AVERAGE foundation the model licenses is preserved exactly.
**SELECTED (engineering); feasibility UNKNOWN (above).**

## Endpoint and depth schedule (arrangement B)

| family | planes | cords | ends | anchors used | doubled | unused | crossings/plane | total crossings |
|---|---|---|---|---|---|---|---|---|
| d60 (m↔m+52) | 69 (even) | 5,382 | 10,764 | 0–129 (130) | 26/plane | 25 | 2,652 | 182,988 |
| d180/11 (m↔m+70) | 68 (odd) | 5,304 | 10,608 | 0–147 (148) | 8/plane | 7 | 2,967 | 201,756 |

Axial depth: none — every cord lies in its own bay plane. Within-family
crossings (384,744 total) are the only connector sites; between-family
geometric intersections: **zero** (never co-planar).

## Finite-diameter clearance

| family | cord Ø | spacing @ smallest kept plane (r=7.05 m) | @ barrel (r=49.54 m) | clearance (binding) |
|---|---|---|---|---|
| d60 | 11.1 mm | 141.2 mm | 992.3 mm | 130.1 mm |
| d180/11 | 17.9 mm | 43.2 mm | 304.1 mm | 25.3 mm |

Both clear the finite diameter at the smallest retained plane and the
barrel (occupied miss radii: d60 3.48 m at its polar plane to 24.48 m,
d180/11 1.33–7.50 m; the r=7.05 m row is the occupancy-aside worst case).
Worst cord sag at the declared 0.2% pretension is 0.082 m against a 2 m
plane gap; no intermediate guides required by clearance.

## Loads, pretension, sign-reversal thresholds

Per unit tension at an anchor: radial share sin(φ/2) = 0.869 (d60) / 0.988
(d180/11), tangential 0.494 / 0.151, axial zero. Declared pretension
ε₀ = 0.2% → T₀ = 13.5 / 35.4 kN per cord (the d180/11 section doubled with
the corrected winner). Radial preload per OCCUPIED plane counts BOTH ends
of all 78 cords (156 endpoints; v2 counted one end): **1,835.2 kN (d60) /
5,453.5 kN (d180/11) = 2.57% / 7.65%** of the plane's PHYSICAL pressure
demand 71,304 kN (P·2πR·bay; KD is a capacity knockdown on the stiffness
side, not a load reduction — v2 had applied it to the demand and reported
1.98%/5.88%). Small, no longer quite "negligible" for the heavy family.

Slack threshold, corrected to the ACTUAL first cord to go slack: the
SHORTEST d60 cord (polar plane r = 7.051 m, cord (0, 52), L = 12.260 m) at
its worst mode n=3 — strain per unit modal amplitude **0.141792/m**, so
ε₀ = 0.2% keeps cords taut only to **w = 0.0141 m** (v2's 0.080 m used the
family MEAN cord length and understated the strain 5.7×); required ε₀:
0.284% @ w=0.02 m, 0.709% @ 0.05 m, 1.418% @ 0.10 m. Creep strain ε_c
lowers the taut limit to (0.002−ε_c)/0.1418 m. This is a SINGLE-MODE
antinode bound on one cord: mixed-mode phase combinations and post-slack
tension-only redistribution sit outside it, and the linear margins below
presume w < 0.0141 m — carried to the coupled finite-endpoint unit as an
explicit scope condition.

## Bill of materials (explicit, replaces the allowances — no double count)

| line | count basis | tonnes |
|---|---|---|
| cord, d60 | 5,382 × drawn lengths (mean 69.73 m, Ø11.1 mm, 970 kg/m³) | 35.19 |
| cord, d180/11 | 5,304 × drawn lengths (mean 80.27 m, Ø17.9 mm) | 104.32 |
| terminations | 21,372 swaged lugs × 0.35 kg (declared) | 7.48 |
| crossing clips | 384,744 × 0.05 kg | 19.24 |
| assembly allowance | 5% on the above | 8.31 |
| **total** | | **174.54** |

Replaces the corrected R3-I005 spokes line (219.30 t = cord×1.3 +
137-plane clips): **−44.76 t**. The ×1.3 fitting allowance is superseded
by the explicit lugs; sensitivity ×2 lug mass = +7.5 t, inside the
allowance. (v1's 121.52 t priced the superseded winner's smaller cord
bill and the overcounted clips.)

## Series compliance and the ring buyback

η = L/(L+2Lₐ) per family on the foundation term only. Declared
Lₐ = 0.15 m/end → 0.43% foundation loss → the corrected winner's SCALAR
binding margin (n=5, 1.0008) survives it: **buyback 0.00 t**, min scalar
margin after 1.0002. But the same compliant state evaluated on the
ORIENTATION margin (first review, finding 3) FAILS: rigid baseline
1.000003659 (n=5, pass by 3.7 ppm) → **0.999345419 with the declared lug**
— the routed design's as-declared state has a demonstrated single-mode
orientation failure that no scalar buyback was sized against. Bounded
recovery scenario: +0.45 t of inner rings restores it to 1.0 — recorded,
not applied (the coupled finite-endpoint unit owns the change). At the
5%-per-end anchor-zone point (Lₐ = 2.27 m/end, 6.1% loss) the scalar
buyback is **10.61 t** and mode 3 binds (restored exactly 1.000).
No-buyback threshold: mode 5 fails once Lₐ > 0.163 m/end — the declared
lug sits just inside it on the SCALAR margin (v1's 0.067 m threshold
priced the n=4 winner); on the orientation margin the declared state is
already past it.

## Budgets, same lift/shell/SF basis (hull-only; membrane still excluded)

| point | total (t) | SL residual (t) | 2,500 m (t) |
|---|---|---|---|
| corrected R3-I005 winner (before) | 2,207.3 | +42.5 | −450.0 |
| **after routing + BOM (lug buyback 0)** | **2,162.6** | **+87.3** | −405.2 |
| anchor-zone 5% scenario (+10.61 t buyback) | 2,173.2 | +76.7 | −415.8 |
| stacked worst case (×2 lugs AND 5% anchor) | — | +69.2 | — |

These are ARITHMETIC on a layout whose feasibility is UNKNOWN (the
finite-phase caveat above), not a closure. SF1.2 (d60+d20, same
mechanism): 2,536.9 → 2,492.3 t, sea-level −242.4 t — **still fails;
retained honestly**. No equipment/payload/gas zeros anywhere.

## Bounds and unknowns

Scalar family factors stay licensed: circumferentially n≤12 vs 155
anchors; axially the 2-bay (4 m) modulation sits against the model's own
axial mode length l_eff = 149 m, and section conservation preserves the
licensed average exactly. Bay-local modes remain outside the model both
before and after — unchanged UNKNOWN, not a regression. THE NEW HEADLINE
UNKNOWN is the finite-phase verdict itself (above). Others with
thresholds: anchor-zone compliance (scenarios priced), creep (taut-limit
formula), cord dynamics (guide threshold: half the ~1.84 m residual plane
gap), lug rating (×2 mass sensitivity shown).

## v1, preserved as history (superseded)

v1 (commit `914bab52`, base R3-I005 v2 at `9761c65f`) priced the
then-winner under the scalar pass: option A rejected at 52 MN/m/487 t
(mode-4 budget 0.19%), option B BOM 121.52 t (−33.4 t), lug buyback 0.25 t,
"all 11 margins ≥ 1.0", SL +80.0 t, SF1.2 −243.7 t. The consolidated
review withdrew the scalar pass and corrected the crossings and marginal
costs; every one of those numbers is superseded by the v2 tables above.
What survives from v1: the arrangement decision (alternating planes beat
two-depth standoffs — re-priced, still true), the clearance/sag/pretension
method, and the buyback machinery.

## Checks and reproduction

`python3 research/design-iterations/R3-I009/routing.py` writes
`routing.json` (sha256 in the unit evidence file), byte-identical on a
second run. Parity asserts: the corrected R3-I005 winner reproduced
exactly (total/margin to 1e-6, binding mode n=5 vs the record);
all-137-plane family topology equals the CORRECTED R3-I005 record
(26/8 doubled anchors, 2,652/2,967 crossings per plane, 363,324/406,479
totals); binding-mode margin matches the record to 2e-4; every clearance
assert positive. The consolidated counterexamples were reproduced before
correcting (crossing counts, marginal costs, orientation matrix,
0.999537142), and the FIRST-REVIEW counterexamples are now pinned by
asserts in the script: first slack w = 0.0141052 m from the shortest d60
cord at n=3 (finding 2); post-lug n=5 orientation margin 0.999345419 with
the rigid baseline 1.000003659 matching the record to 1e-8 (finding 3);
both-ends radial preload 1,835.2 / 5,453.5 kN against the 71,304 kN
physical demand → 2.57% / 7.65% (finding 4). Documentation checks:
`make readmecheck linkcheck buildercheck`. No model, gate or programme
file edited.
