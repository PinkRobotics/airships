# Derveni, Choquart, Abbasi, Yan & Reis (2024) — The most severe imperfection governs the buckling strength of pressurized multi-defect hemispherical shells

arXiv:2410.08973 (EPFL Flexible Structures Laboratory). Read in full from the arXiv PDF; not
redistributable here, see `sources.json`.

## What it establishes

Thin shells under external pressure fail far below the classical eigenvalue prediction, and the
gap is carried by an empirical knockdown factor κ. This paper asks what sets κ when a shell has
*many* defects rather than one, using finite-element simulations previously validated against
experiments on elastomeric hemispheres.

They build statistical ensembles — 100 realisations per parameter set — of hemispherical shells
with defect amplitudes drawn from a lognormal distribution, then delete defects from either end of
that distribution and re-run the buckling analysis. Deleting the *least* severe defects changes κ
by **less than 4%**. Deleting the most severe raises κ, by up to 0.85 across the range studied. A
multi-defect shell has, to within a few percent, the same knockdown factor as a single-defect shell
carrying only its worst flaw. Buckling strength is a weakest-link, extreme-value problem.

## Why it cuts against us

Both structural sources this project leans on claim scale invariance. Akhmeteli & Gavrilin say
explicitly that multiplying all linear dimensions by the same factor gives an equally viable
design. Jenett et al. hold `R/t` and lattice pitch as ratios, so their net lift scales as R³ and
their shell mass fraction is constant from R = 0.1 m to R = 100 m.

Defects do not scale that way. If the worst defect governs, then what matters is the maximum of a
distribution sampled once per manufactured feature, and the number of features grows with the
structure. Jenett's own design study counts 1,460,192 voxels and 125,600 skin panels. Our P-10000
is a 22,000,000 m³ hull. The expected worst defect in 10⁶ draws is materially larger than in 10³,
so the knockdown factor should *fall* with size — while the papers we cite hold it constant and
our model never computes it at all.

This is the mechanism behind the first item in the README's "what would change our minds": a
buckling analysis that puts the evacuated shell above the mass of the air it displaces. Derveni et
al. do not perform that analysis for our geometry. What they establish is that the way the
literature currently extrapolates to large radii is the wrong way round.

## Where it does not support the conclusion we would like

These are hemispheres, elastic, homogeneous and thin — not sandwich panels, not lattices, and not
closed bodies of revolution. Defect width is fixed at a single characteristic value, and the
defects are deliberately non-interacting; an earlier paper by the same group shows interacting
defects can raise κ as well as lower it. The paper gives no scaling law for the worst defect
against part count, so the argument above is an inference from their mechanism rather than a result
they report. It is a preprint, and carries the default arXiv distribution licence.
