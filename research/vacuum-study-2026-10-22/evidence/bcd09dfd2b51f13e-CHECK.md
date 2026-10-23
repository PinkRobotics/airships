# CHECK MAINLINE-026

Unit `vacuum-mainline026-check-1020`. Checker `ref-2543c559b19ffce7dfdd`.
Owner card `rpt-ref-7ce5b278fa083d87105b`.
**QUESTIONABLE. PROJECTION for rigid joints and the fan. No certification.**

The owner's scripts were not executed. Counts, arc lengths, annulus properties
and the allowance stack were recomputed from the pinned inputs. The linear
eigen is an independent 3-segment model: great-circle chords, centroid-fan
pressure, orthogonality constraints, and the card's cubic Hermite geometric
stiffness. A pin-ended column of that stiffness gives P L^2/EI = 12 and
moves to pi squared as the element count rises. Nonlinear paths were not rerun.

## Agreement

| Field | Card | This check |
|---|---:|---:|
| Joints, members, cells | 362, 1080, 720 | same |
| Arc mean, m | 2.0013435607236976 | 2.0013435607237002 |
| Total mass, kg | 4950.843078369846 | 4950.843078369851 |
| Overrun, kg | 61.40092817984714 | 61.4009281798526 |
| w at 2.04 m, N/m | 56216.62727599055 | 56216.627275990555 |
| Wall screen, Pa | 1750799936.9601378 | 1750799936.960138 |
| 3-segment follower lambda | 6.472319662311285 | 6.472325166760517 |

The overrun rounded to 0.01 kg is the card's 61.40 kg. The 24-segment lambda
6.465222 is 5.509 percent above the 011b continuum 6.127640, which is
SF_global 1.2255279468805444 divided by k = 0.2.

## Same formulation, finer card column

These are listed because the numbers differ. Each is the 3-segment mesh
against the card's finest published column, not a different formula.

| Field | Card finest | This 3-segment check | Relative |
|---|---:|---:|---:|
| Follower lambda | 6.465222443853006 | 6.472325166760517 | 0.001099 |
| Fixed-direction lambda | 6.571963275671537 | 6.579531734296541 | 0.001152 |
| Mean compression, N | 550543.522936495 | 550033.6938633921 | 0.000926 |
| Fan volume, m3 | 4167.275913727444 | 4162.619948271157 | 0.001117 |
| Unit axial stress, Pa | 863586316.6401045 | 862059918.1056993 | 0.001768 |
| Wall-screen lambda | 2.027359516037556 | 2.030949241680748 | 0.001771 |
| Member Euler minimum | 7.571721534683924 | 7.582215002592791 | 0.001386 |

The follower mode residual is 8.45e-5 and the radial fraction is 0.979.
Joint-energy on the original 362 nodes is 0.143 under this check's split;
the card's 0.344 uses its own participation definition and was not recomputed.
No fix card. Cited nonlinear ratios recompute from the published limits.
