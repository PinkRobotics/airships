# R3-I004 — corrected after review: the drawn net does NOT deliver the credited odd-mode stiffness

Status: CORRECTED RECORD (v2), 2026-10-14. Base `afb2c2d1726b9d9a805f9781085c3dd6a52913e5`;
original attempt preserved verbatim at commit `2d7b0573` (now known NOT cleared —
see the lead's 2026-10-14 review, seven findings, all reproduced below). This file
replaces the original README's claims. Internal conditional design hypothesis;
no positive claim; `floatsToday` not shown.

**Verdict: FAIL for this layout under these assumptions.** The +180.7 t
feasible crush-floor bound advertised in v1 is WITHDRAWN: the drawn
half-column-offset net delivers 0.09–1.2% of the odd-mode foundation stiffness
the model's `gi_chordal` credit assumes, and the frozen allocation's mode-3
capacity is 84.1 kPa against 101.325 kPa demand *before* the γ 0.65 knockdown
(which requires 155.9 kPa). This fails the specific layout — a differently
routed net is not thereby excluded (R3-I005 pursues exactly that).

## Finding 1 (HIGH) — the engagement law was wrong at odd n

For a breathing mode `w·cos(nθ)`, a cord subtending `φ` (here 178.839°, a
0.5-column offset `δ` = 1.161° from antipodal) stretches

`dL = 2w·sin(φ/2)·cos(nφ/2)·cos(nθ + nφ/2)`,

so the amplitude engagement is **`sin(φ/2)·|cos(nφ/2)|`** — with φ, the
subtended angle. At odd n this becomes `sin(φ/2)·sin(nδ/2)`: near-cancellation,
exactly the physics the model's own comment describes for a true diameter. v1
used `|cos(nδ/2)|` — the even-mode factor — at every n. And the modal
stiffness scales with the **square** of the amplitude factor (energy:
`K = Σ kᵢ (dLᵢ/w)²`); v1 applied it linearly, to mass.

| n | v1 claim | exact engagement | exact² (stiffness) |
|---|---|---|---|
| 2 | 0.9997 | 0.9997 | 0.9995 |
| **3** | **0.9995** | **0.030396** | **0.000924** |
| 4 | 0.9991 | 0.9991 | 0.9983 |
| **5** | **0.9987** | **0.050647** | **0.002565** |
| 6 | 0.9981 | 0.998101 | 0.996205 |
| **7** | **0.9974** | **0.070876** | **0.005023** |
| 8 | 0.9967 | 0.996664 | 0.993339 |
| 12 | 0.9926 | 0.992564 | 0.985183 |

Even modes were right; odd modes — the ones `gi_chordal` exists to cover — are
effectively zero. Capacity at mode 3 of the frozen SF 1.0 allocation, corrected
law, membrane term as the reviewed row carried it: rings+crimp 70,795 Pa,
corrected foundation 131,250 × 0.000924 = 121 Pa, membrane 13,165 Pa →
**84,081 Pa < 101,325 Pa**. FAIL.

```
   bay plane, mode n=3 (exaggerated): the two anchors of a near-diametral
   cord move (+w, -w); the cord TRANSLATES instead of stretching.

        anchor i  o------> <------o anchor i+77      displacement
               .'      almost cancels at odd n       '.
              o   cord stretch ~ sin(n*delta/2) ~ 3%      o
```

## Findings 2–7 — reproduced and corrected

| # | Finding | Reproduction | Correction |
|---|---|---|---|
| 2 MEDIUM | anchor lengths are PER END, labelled combined | per end 2.1237 / 13.4499 / 40.3496 m; combined 4.2473 / 26.8997 / 80.6992 m | both reported in `net.json`; labels fixed |
| 3 MEDIUM | midpoint spacing 20.3 / 2.9 mm, not 40 mm | barrel (r 49.54 m) 20.35 mm; smallest kept plane (r 7.05 m) 2.90 mm — vs 11.869 mm cord | clearance claim withdrawn; axis routing hardware UNKNOWN and unpriced, not zero |
| 4 MEDIUM | no retained incumbent; "re-solve can only improve" unsupported | the greedy starts at minimum members/zero spokes; R3-I005's own SF 1.2 rerun landed 20.2 t worse | guarantee and upper-bound language withdrawn everywhere |
| 5 LOW | offset variant doubles anchors 76/77, leaves 154 unused | enumerated: doubled [76, 77], unused [154] (the v2 code enumerated 79 cords — doubled [76, 77, 78], unused []; corrected in the 2026-10-14 consolidated return, residual B) | `variantTopology` records real endpoints; the 52 m / 72-column one-column offset is 5°, not these 112 m numbers |
| 6 LOW | 3,002 interior crossings + 1 shared-endpoint pair per plane | 411,274 clips over 137 planes; v1 billed 411,411 (137 clips = 6.85 kg excess) | counts and clip mass corrected |
| 7 LOW | sf 1.08 row is a recomputation, not exact | recomputed 2130.9 / 119.0 / −373.5 t vs frozen ledger 2130.7 / 119.1 / −373.3 t | provenance stated per row; SF 1.0 / 1.2 reproduce exactly |

## What survives from v1, and what does not

Survives (review-confirmed arithmetic): the net's counts and lengths (10,686
cords, mean 80.699 m, 862.4 km, miss radius 0.50 m); the 1.441 length ratio
against the smear's R = 56 m billing; the mass arithmetic of the drawn article
(cord over the drawn mean, ×1.3 fittings, clips — now 411,274); the even-mode
engagement values; the anchor-sensitivity numbers (relabeled); determinism.

Withdrawn: the odd-mode engagement claim; the "chordal at every mode"
conclusion; the feasible +180.7 t / +57.4 t bounds and the SF 1.2 "survives"
row; the no-contact clearance argument; the upper-bound / re-solve-guarantee
language; the variant's "removes doubled-anchor bookkeeping" note; exact-reproduction
claim for the mid-band row.

## Weakest assumption (unchanged in kind, now decisive in fact)

The odd-mode foundation does not exist in this layout at all — a net that
covers odd modes must be *designed* for it (offsets of tens of degrees, a
finite-diameter hub, or mixed families), and its routing hardware is UNKNOWN.
Anchor-zone stiffness (per end: 2.12 m of equivalent cord costs 5%) and
pretension/creep remain unmeasured behind that.

## Next concrete design change

R3-I005: a mixed-offset chord family (or finite-diameter routing) with the
corrected squared factors, priced with crossings/standoffs honestly — restoring
odd-mode coverage by geometry rather than by a misapplied cosine. If no layout
closes, the honest answer is FAIL plus the next ranked change.

## Checks and reproduction

`python3 research/design-iterations/R3-I004/net.py` — writes the corrected
`net.json` (sha256 recorded in the unit evidence file), byte-identical on a
second run; every disposition number above is recomputed there. Documentation
checks: `make readmecheck linkcheck buildercheck` (Builder gate environment
closed 2026-10-14 with the Astra-a Node 22.23.3 runtime: 12/12 self-tests,
exit 0 — not rerun for this correction). No model, gate or programme file
edited.
