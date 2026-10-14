# R3-I005 (v3, after the consolidated review) — mixed-offset net, honest pricing, finite-phase verdict

Status: v3, 2026-10-14, after the lead's consolidated I004/I005 review return (verdict paragraph wording corrected same day: "exactly" now scopes to the orientation result only; the mixed-mode trial numbers are identified as cited prior-review results — no numerical change).
Base `afb2c2d1726b9d9a805f9781085c3dd6a52913e5`. v1 (at `66249ee8`) used the
wrong engagement law; v2 (at `9761c65f`) corrected the law but closed on the
scalar eleven-mode pass — **the review disproved that closure** (finding 1:
the scalar pass is a phase AVERAGE; the actual finite topology of 78 start
anchors per family per plane is not circulant). v3 carries the five
consolidated findings, keeps the v2 winners as superseded conditional
results, and records the finite-phase verdict. Internal conditional design
hypothesis; no positive claim; `floatsToday` not shown.

**Verdict: NOT CLOSED.** The v2 statement "closes at both SFs, +46.9 t SL"
is WITHDRAWN. On the v2 winner the review demonstrated the n=4 orientation
matrix `[[31273.7411, −128.9838], [−128.9838, 31217.4206]]`, weakest
eigenvalue 31,113.5588 Pa against the scalar 31,245.5809 — margin
1.000384064 → **0.999537142 < 1.0** — which this seat reproduced exactly,
and the mixed-mode trial `cos(3θ)/√8 − sin(4θ)/√15` at **0.967922863**
(SF 1.0) / 0.985215242 (SF 1.2), cited from the review. The mixed-mode
numbers are prior-review results, not seat reproductions (see the
convention discrepancy below); every mixed-field convention this seat
could construct lands below 1.0 on that winner too: FAIL, however
combined.

v3 re-prices with the corrected crossings and ledger marginal costs (below).
The winners MOVE (heavier): SF 1.0 `d60+d180/11` at **2,207.3 t** (+42.5 t
SL, −450.0 t at 2,500 m, scalar binding n=5); SF 1.2 `d60+d20` at
**2,536.9 t** (−287.0 t SL). On these NEW points the weakest-orientation
margin over all eleven modes is 1.000003659 (SF 1.0, binding n=5) and
1.003087627 (SF 1.2, n=3) — nominally ≥ 1.0, but a 3.7 ppm pass is inside
any model uncertainty, and the mixed-mode trial under the review's exact
convention is UNKNOWN on these points (this seat reproduced the review's
orientation machinery to 1e-4 but not its mixed-field ring/foundation
combination; seat candidates land within 2–6% of the cited margins). **The
honest status of both winners is UNKNOWN, not feasible; the closure stays
withdrawn.** `alloc.json` records all of this per winner in `finitePhase`.

## The consolidated findings, carried (with the corrections)

| # | finding (demonstrated by the review) | correction in v3 |
|---|---|---|
| 1 | scalar eleven-mode pass is a phase average; finite topology fails it (matrix/eigenvalue/trial above) | `finite_phase()` on every best point: per-mode weakest-orientation margins, the binding matrix, and the trial under the documented seat convention; feasibility claims withdrawn |
| 2 | crossings counted wrong: cords (a, a+step), (b, b+step) cross iff b < a+step — shared endpoints are not crossings | per-plane count `Σ_a min(77−a, step−1)`: 3,002 / 2,652 / 2,867 / 2,925 / 2,958 / 2,967 (halfcol unchanged — reproduces the I004 record 411,274); winner clips 769,803 = 38.49 t |
| 3 | member marginal kg must carry ×(1+adder)/η = 1.235294 in the greedy and the rejection economics (ring increment 28,884.866 kg scored vs 35,681.305 kg ledger) | both scorings corrected; `growInnerRings` now 0.5754 μ/kg (was 0.7108) |
| 4 | the fixed-member line is 1,189.0361 t, not 1,164.6 (wall members + longerons + fan webs + junction, ×1.05) | ledger line corrected; the mass table below sums to the script total exactly |
| 5 | tables did not sum to the script total; clip labels carried stale per-family prices | regenerated from the record; every table here sums |

## The families (explicit endpoint topology, 155-anchor ring)

Offsets snap to half-integer columns (n odd ⇒ no anchor is exactly
antipodal; `step = 77.5 − k` for half-integer k). All cords run anchor
`m ↔ m+step`, m = 0..77, in each of the 137 kept bay planes.

| family | ideal δ | built δ | k (col) | step | crossings/plane | clips (t) | mean cord (m) | covers (f≥0.65) |
|---|---|---|---|---|---|---|---|---|
| halfcol | 1.16° | 1.161° | 0.5 | 77 | 3,002 | 20.56 | 80.70 | even n |
| d60 | 60° | 59.23° | 25.5 | 52 | 2,652 | 18.17 | 70.16 | n=3 (0.756), n=9 |
| d36 | 36° | 36.00° | 15.5 | 62 | 2,867 | 19.64 | 76.75 | n=3, n=5 (0.904) |
| d180/7 | 25.7° | 26.71° | 11.5 | 66 | 2,925 | 20.04 | 78.52 | n=7 (0.707) |
| d20 | 20° | 19.74° | 8.5 | 69 | 2,958 | 20.26 | 79.51 | n=9 (0.970) |
| d180/11 | 16.4° | 17.42° | 7.5 | 70 | 2,967 | 20.32 | 79.77 | n=4 (0.658), n=7, n=9, n=11 (0.972) |

Interior crossings per plane = pairs b ∈ (a, min(77, a+step−1)] over starts
a (finding 2; interleaved pairs cross, a shared endpoint b = a+step does
not, and no wraparound exists). halfcol reproduces the I004 record exactly
(step 77, 3,002/plane, 411,274 total).

## The myopia result (finding 4 of the I004 review, incarnate)

The FREE greedy — cheapest marginal margin per kg, member moves at their
ledger cost ×1.2353, a family's first step carrying its whole 18.2–20.6 t
clip bill — never activates any odd family and lands exactly on the
baseline (2,519.3 t at SF 1.0). Forcing families active up front and letting
the greedy shape freely changes the answer by **−312.0 t**. The enumeration
(singles and pairs over all six families; triples unexplored; no optimality
claim) at SF 1.0:

| point | total (t) | SL residual (t) | 2,500 m (t) | crit n | scalar feasible |
|---|---|---|---|---|---|
| nospoke (rings+crimp) | 3,223.8 | −974.0 | −1,466.4 | 2 | yes |
| baseline (halfcol only) | 2,519.3 | −269.5 | −762.0 | 2 | yes |
| free greedy | 2,519.3 | −269.5 | −762.0 | 2 | yes |
| **d60 + d180/11** | **2,207.3** | **+42.5** | −450.0 | 5 | yes (unknown finite) |
| d60 + d20 | 2,207.8 | +42.0 | −450.5 | 3 | yes (unknown finite) |
| halfcol + d36 | 2,214.7 | +35.1 | −457.4 | 3 | yes (unknown finite) |
| halfcol + d60 | 2,224.1 | +25.8 | −466.7 | 4 | yes (unknown finite) |

At SF 1.2 the best is d60 + d20 at 2,536.9 t (−287.0 t SL, −779.5 t at
2,500 m, crit n=3); full tables in `alloc.json`.

## The SF 1.0 layout, priced

`a_d60 = 6.6e-6`, `a_d180/11 = 1.7e-5` m²/m² (no halfcol — the odd families
carry the even modes too), inner rings 0.00145 m², theta webs 6.94e-4 m².
Scalar mode margins: n=3 1.0072, n=4 1.0856, n=5 1.0008 (binding), all
eleven ≥ 1.0008; weakest-orientation n=5 1.0000037 (the ppm caveat above).
Cap-buckle margin 1.81.

| mass line | tonnes |
|---|---|
| wall members + longerons + fan webs + junction (×1.05) | 1,189.0 |
| inner rings 105.0 + theta webs 342.0 (×1.05) | 469.3 |
| subtotal members 1,658.3, / η 0.85 (+292.6 joints) | 1,951.0 |
| cord + fittings: d60 46.0, d180/11 134.8 | 180.8 |
| crossing clips: 18.17 + 20.32 (769,803 clips) | 38.5 |
| film, clamps, pads, straps, skins | 37.0 |
| **total (script: 2,207.3204)** | **2,207.3** |

Not priced anywhere above: standoff/routing hardware for co-planar cord
depths, pretension/creep, anchor-zone compliance (per end 2.12 m of
equivalent cord costs 5% of stiffness — I004), termination hardware beyond
the ×1.3 allowance, and the membrane (excluded until its shear system is
priced). Any of these can eat the 42.5 t — and the finite-phase status is
UNKNOWN besides; the record claims only what the stated model prices.

## What v2 said, and what survives

v2 (at `9761c65f`) closed at both SFs (+46.9 t SL at SF 1.0, 2,203.0 t) on
the scalar pass; superseded by the demonstrated finite-phase failure. What
survives from v2: the corrected squared law and the World mirror with its
exact parity asserts (gi to 1e-9, mass assembly to 0.0 t against the frozen
model — re-proven here), the true-pricing convention, the greedy machinery,
and the myopia demonstration. The v2 winner's binding-mode recomputation
(156,276.3 / 155,944.5 Pa) remains a valid independent check of the scalar
machinery on that point.

## Checks and reproduction

`python3 research/design-iterations/R3-I005/alloc.py` writes `alloc.json`
(sha256 recorded in the unit evidence file), byte-identical on a second run.
Parity asserts at both SFs: gi exact vs the frozen row (full-credit
convention, membrane on), mass assembly Δ = 0.0 t, halfcol n=3 factor
0.000924 = the corrected I004 number, halfcol topology = the I004 drawn net
(3,002/plane, 411,274 — invariant under the finding-2 correction). Review
counterexamples reproduced before correcting: the six crossing counts, the
marginal-cost pair 28,884.866/35,681.305 kg (0.7108 → 0.5754 μ/kg), the
fixed-member line 1,189.0361 t, the orientation matrix / eigenvalue /
0.999537142 exactly, and the I004 variant enumeration. Documentation checks:
`make readmecheck linkcheck buildercheck`. No model, gate or programme file
edited.
