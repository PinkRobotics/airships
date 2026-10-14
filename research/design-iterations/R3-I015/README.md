# R3-I015 — the coupled finite-endpoint cos/sin block

Status: v1.1, 2026-10-14 (coordinate-mapping interpretation corrected,
member-energy validation added, doubled-lug assembly corrected, rounding
note narrowed, summary figures fixed). Base: the corrected R3-I005/R3-I009
record in the same checkout. Internal conditional design hypothesis; no
positive claim; `floatsToday` not shown.

**Verdict: the inherited comparison FAILS hard, and the one-step response
fixes the matrix at a positive bill — conditionally.** The record carried
the mixed-mode question as UNKNOWN (the per-mode orientation margin passed
by 3.7 ppm). Building the FULL 22-coordinate coupled block — n = 2..12,
cos and sin, cross-mode terms from the actual member endpoints — the
inherited arrangement-B geometry scores **λ_min = 0.781900996**: 22% below
unity, 22% below its own per-mode pass. Preserved, not tuned away. The
selected one-step response (complete each family from 78 to all 155 start
anchors per plane) zeroes every cross-mode entry by exact DFT
orthogonality, so the coupled minimum EQUALS the licensed scalar eleven-
mode minimum: **1.000811196 rigid / 1.0001500 at the declared lug**, at a
fully re-priced bill of **+9.6 t on the spokes line (SL +32.9 t, still
positive)**. PASS, with the exact scope below — a matrix improvement with
a positive full bill is still not a float claim.

## The construction (every entry hand-derivable)

u(θ) = Σ_{n=2..12} [c_n cos nθ + s_n sin nθ] — radial metres, first-order
linearised in u/r. Cord j (subtended angle φ, start anchor a): endpoints
t_a, t_b = t_a+φ, midpoint t_mid = t_a+φ/2, and the exact sum-to-product
kinematics dL_j = sin(φ/2)·(u(t_a)+u(t_b)) with
u(t_a)+u(t_b) = Σ_n 2cos(nφ/2)·[c_n cos n·t_mid + s_n sin n·t_mid].

**Coordinates.** The 1/√((n²−1)(m²−1)) factors make the matrix
coordinates **y = √D·c**, D = diag(n²−1), with c the declared radial
amplitudes: the mapped radial field of any matrix vector is
c = y/√(n²−1), and λ_min(M) is the worst margin over fields of unit
modal norm ‖y‖=1, i.e. Σ_n (n²−1)(c_n²+s_n²) = 1.

The foundation entry is the SELECTED symmetric bilinear extension of the
licensed law sc_j(n) = E·a_j·sin²(φ/2)·cos²(nφ/2)/(n²−1):

K_f[(n,α),(m,β)] = Σ_j E·a_j·sin²(φ/2)·cos(nφ/2)cos(mφ/2)/√((n²−1)(m²−1))
                    · (2/n_cords)·Σ_a trig_α(n·t_mid)·trig_β(m·t_mid)

whose pure-mode reduction IS the committed `orientation_phase` block
(asserted to 1e-9, both winners, modes 3/4/5 — and the historical mode-4
matrix `[[31273.7411, −128.9838], [−128.9838, 31217.4206]]` reproduces
to 5e-4 Pa). Pure-mode blocks alone do not determine the cross entries
(a block-diagonal form shares them); the selection is validated directly:
enumerating members one by one through the mapped radial field, the
member-extension energy equals **E_direct = (A/L̄)·(y′K_f y)** exactly
(asserted per family to 1e-12, both geometries) under the stated
assumptions — first-order cord extension, equal per-cord section, the
licensed equal-length convention (one L̄ per family; with actual
per-plane lengths the direct energy is 22–28% higher, the disclosed
convention gap). Ring+crimp: axisymmetric per-mode series on the
diagonal, as committed (the direct check covers the foundation, the part
that carries cross entries). Demand: the licensed margin formula uses one
pressure number, so M = K·KD/(P·SF). Units SI throughout; eigenvalues by
a deterministic pure-Python Jacobi solve (residual asserted < 1e-9).

## The coupling mechanism, and why 78 starts couple odd modes

```
   one family plane, 155 anchor stations (d60, step 52; unrolled)

   COMPARISON — 78 starts (a = 0..77), the half-window:
        end*  start o          o = start anchor   * = that cord's far end
         *  o    o    o    o    o    o    o    o    o         (no wrap:
        154  0   10   20   30   40   50   60   70   77          77+52=129)
            |___________________________________________|
             window phase sums are COHERENT for odd modes:
             sum sin(k t) piles toward the window edge, so modes 2-3,
             2-5, 2-7, 4-5 leak into each other — the dominant
             cross entries (2,3)=0.557, (4,5)=0.124, (2,5)=0.124,
             (3,4)=0.117, (2,7)=0.084, (6,7)=0.076 (margin units)

   COMPLETED — 155 starts (every station starts one cord):
        o    o    o    o    o    o    o    o    o    o   ...  o
        154  0   10   20   30   40   50   60   70   77        51(wrap)
             full-circle sums vanish identically for n = 2..12:
             every cross-mode entry = 0 (measured max 1.7e-16), and
             the coupled minimum EQUALS the licensed scalar minimum

     axial layout unchanged: d60 in even-index planes, d180/11 in odd
     index planes of the 137 kept — disjoint planes, zero between-family
     contact, zero standoff hardware, before and after.
```

The comparison's worst field is dominated by the odd pair c₃/s₃ (≈ ±1.0)
with a strong c₂ (0.42) riding the (2,3) entry — precisely the window
coherence above, not a margin-level effect: the licensed scalar law
presumed full-circle orthogonality, and the half-window breaks it.

## The one-step response (selected by mechanism, no sweep, no tuning)

Completing each family to all 155 start anchors per occupied plane:
same stations, same planes, same licensed total section — per-cord
section × 78/155, cord count × 155/78. Cross entries vanish by identity,
λ_min = scalar minimum exactly: **1.000811196 rigid** (n=5 binding, cos/sin
degenerate), **1.0001500 at the declared lug**. On input precision: this
unit's exact routed lengths give 1.000150027465328; the record's own
4-decimal mean cord lengths give 1.000150027596421 — a display-rounding
identity at 4 decimals (both print 1.0002, asserted) and a harmless
1.3e-10 difference at the 9th decimal, not full-precision equality. The
arrangement-B compliant state, for contrast, FAILS coupled at 0.7809.
No ring buyback is needed; no optimisation or sweep was run — the change
was chosen because the coupling mechanism names it.

## Full re-pricing of the completed arrangement

| family | planes | starts/plane | cords | ends | cord Ø | clearance | crossings/plane | total crossings |
|---|---|---|---|---|---|---|---|---|
| d60 (m↔m+52) | 69 (even) | 155 | 10,695 | 21,390 | 7.87 mm | 133.4 mm | 7,905 | 545,445 |
| d180/11 (m↔m+70) | 68 (odd) | 155 | 10,540 | 21,080 | 12.72 mm | 41.3 mm | 10,695 | 727,260 |

(Both families: 155 starts per plane; every anchor carries two ends;
crossings exclude shared endpoints, corrected counting; sag 0.063 m
(d60) / 0.0815 m (d180/11) — worst 0.0815 m, unchanged from arrangement
B, section-independent.)

| line | basis | tonnes |
|---|---|---|
| cord | volume conserved exactly (section ×78/155, count ×155/78; asserted to 1e-12) | 139.51 |
| terminations | 42,470 swaged lugs × 0.35 kg | 14.86 |
| crossing clips | 1,272,705 × 0.05 kg | 63.64 |
| assembly allowance | 5% on the above | 10.90 |
| **total spokes line** | replaces the R3-I005 line (219.30 t) exactly as arrangement B did | **228.91 (+9.6)** |

Invariants that survive the change: cord volume identical; sag exactly
section-independent (ρgL²/8Eε₀) — worst 0.0815 m (d180/11; d60 0.063 m),
unchanged; per-plane
radial preload total unchanged (per-cord T₀ halves, count doubles:
1,835.2 / 5,453.5 kN, the counted-both-ends figures); midpoint spacing
unchanged (same stations), so clearance improves by the diameter
reduction alone (d60 133.4 mm, d180/11 41.3 mm — both measured in
`coupled.json`); doubling fully priced by the enumerated terminations at
the unchanged per-family η (cord length depends only on plane radius).
The fixed-member bill, ring members and gas are the winner's record,
counted exactly once. The ×1.235294 marginal-member factor binds ledger
economics of marginal stiffness members; this delta is an enumerated BOM
replacement (like I009's) and no ring growth is priced.

| budget | total (t) | SL (t) | 2,500 m (t) |
|---|---|---|---|
| corrected winner before | 2,207.3 | +42.5 | −450.0 |
| after arrangement B (I009 v2.1) | 2,162.6 | +87.3 | −405.2 |
| **after completion (this unit)** | **2,216.9** | **+32.9** | **−459.6** |
| stacked worst case (lug mass ×2 incl. assembly) | — | +17.3 | — |

SF1.2 adverse case (d60+d20, inherited): the same completion restores its
coupled margins too (0.7692 → 1.0045) but the mass failure is inherited:
2,536.9 → 2,546.1 t, sea level **−296.3 t — still fails, retained
honestly.**

## Reconciliation of the two-mode figures (0.967922863 / 0.985215242)

The construction's 1/√((n²−1)(m²−1)) factors make its matrix coordinates
y = √D·c. The historical trial field cos(3θ)/√8 − sin(4θ)/√15 has radial
coefficients c = (1/√8, −1/√15), which maps to **y = (1, −1)** in the
mode-(3,4) subspace. Evaluated consistently, the frozen v2 winner scores
**0.967922863** (SF1.0) and **0.985215242** (SF1.2) — both historical
figures reproduce exactly (asserted to 5e-10).

**An earlier reading here is withdrawn as false.** It evaluated the trial
by supplying the radial coefficients directly as matrix coordinates
(scoring 0.970129223 / 0.984860951) and concluded that no single
convention produces both cited numbers. That was an inconsistent mapping,
not an irreconcilable convention: under the one consistent mapping
y = √D·c both figures reproduce. The repair is interpretive — every
eigenvalue, eigenvector and verdict is unchanged (asserted against the
committed record at full precision) — and the question is superseded
anyway: the full 22-block minima are 0.8116 (v2 winner) and 0.7819 (the
inherited comparison), far below any two-mode value.

## Scope of the PASS, assumptions, sensitivities

The PASS is conditional on: the frozen model; the licensed foundation law
and its bilinear extension (pure-mode reduction committed and reproduced;
the cross entries are the SELECTED extension — the bilinear form of
direct member-extension energy, verified member-by-member to 1e-12 — but
pure-mode blocks alone do not determine them, so the selection rests on
the stated member-energy assumptions: first-order cord extension, equal
per-cord section, the licensed equal-length convention with its 22–28%
disclosed gap to actual per-plane lengths. This remains the weakest
assumption); the **taut window** — the carried 0.014105 m single-mode
figure is superseded by the R3-I019 unit in the same checkout, whose
rigorous class bound for arbitrary mixed fields is 4.149 mm (d60) /
5.292 mm (d180/11); the declared lug compliance (η = L/(L+0.30) per
family); the corrected crossing counts. Sensitivities: lug mass ×2
including its 5% assembly leaves SL +17.3 t; the 5%-per-end anchor-zone
scenario remains as priced in I009. Axial (2-bay modulation vs the
licensed average), bay-local modes and the membrane: unchanged from the
record.

**Next concrete change:** declare the field class the vehicle must resist
(worst gust/ascent envelope) and re-state the taut window for that
restricted class, then the membrane/load-path question — both carried by
the R3-I019 unit's next change; the drawn termination and per-end anchor
hardware it prices supersede the ideal-lug detail here.

## Checks and reproduction

`python3 research/design-iterations/R3-I015/coupled.py` writes
`coupled.json` (sha256 in the unit evidence file), byte-identical on a
second run (cmp-proven). Parity asserts: per-mode 2×2 blocks equal the
committed `orientation_phase` to 1e-9 (both winners, modes 3/4/5); the
historical mode-4 matrix to 5e-4 Pa; symmetry to 1e-12; the subspace bound
λ_min ≤ per-mode weakest; eigensolve residual < 1e-9; completion
orthogonality < 1e-12 with λ_min = the scalar minimum to 1e-9 (both SFs);
the consistent-mapping trial evaluation reproduces both historical
two-mode figures to 5e-10; the direct member-extension energy equals
(A/L̄)·(y′K_f y) per family to 1e-12 (both geometries); the display-
rounding identity round(λ_lug, 4) = 1.0002 holds for both the exact-
length and the rounded-input compliant minima, which differ by 1.3e-10
(both asserted); every eigenvalue equals the committed record's value at
full float precision (regression assert — the correction is interpretive);
the 78-start geometry branch equals `routing.family_geometry`
field-for-field (cords/ends/crossings/lengths); cord volume conservation
vs arrangement B to 1e-12. Documentation checks:
`make readmecheck linkcheck buildercheck`. No model, gate or programme
file edited.
