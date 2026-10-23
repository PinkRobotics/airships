# MAINLINE-041 — the 022d point on its own discrete frame

**QUESTIONABLE / PROJECTION. Best SF at closure mass; no certified capacity.**

The selected section's own frequency-4 frame gives **SF 1.133451** under 022d's 0.2-times-linear convention, not a transferred 1.07. But the unchanged integer frame exceeds closure mass by **174.444 kg**. After resizing, frequency 5 is the best found in the tested family: **1.143285 at the 5% reserve** and **1.083205 at the 019 reserve**. Film stiffness is not credited in those resize results.

The conservative peak-compression local-shell sensitivity lowers those two resized witnesses to **1.033223 / 0.978132**. That sensitivity is an unqualified interaction surrogate, but its sub-unity 019 result is material to interpretation. No result here establishes a buildable margin.

## Selected section, realized geometry and mass

R=10 m; p=95460.8379139 Pa. OD 275.082856 mm; wall 1.137365 mm; two Zylon directions total 109.440222 μm. Frequency 4 has 162 joints, 480 members and 320 cells. Arcs range 2.538658–3.263662 m; mean 2.994745 m. All counts and lengths are realized geometry.

| Term | Selected 022d continuum (kg) | Actual f=4, unchanged section (kg) |
|---|---:|---:|
| SiC tubes | 4183.590023 | 4361.908697 |
| Both film directions | 214.541558 | 214.541558 |
| All joint ends | 44.191468 | 48.989785 |
| Nodes | 2.926575 | 3.240000 |
| Systems | 100.000000 | 100.000000 |
| 5% reserve | 244.472108 | 244.472108 |
| Sag lift debit | 99.720419 | 90.733892 |
| Closure sum | 4889.442150 | 5063.886039 |

Actual tube mass increases by 178.318674 kg. With the 019 reserve and the same unchanged section, the mass deficit would be 341.270725 kg. The sag term extends the selected cap surrogate to unequal cells; it is not a membrane solution.

## Actual-frame limits and moments

| Limit multiplier | Unchanged f=4 | Closed f=5, 5% | Closed f=5, 019 |
|---|---:|---:|---:|
| SiC mean compression | 4.455478 | 4.249978 | 4.095224 |
| Member Euler | 4.087035 | 4.955476 | 4.662903 |
| Local wall, inherited axial convention | 1.283162 | 1.143285 | 1.083205 |
| Perry compression with FE bending + L/1000 | 3.128943 | 3.356917 | 3.207415 |
| Tension with FE bending + L/1000 | 3.681994 | 4.533560 | 4.263297 |
| Film strength surrogate | 1.227877 | 1.143285 | 1.083205 |
| Perfect global linear (no 0.2) | 5.667253 | 5.717454 | 5.417034 |
| Global linear ×0.2 | 1.133451 | 1.143491 | 1.083407 |
| Joint sleeve axial + bending | 1.218315 | 1.143285 | 1.083205 |
| Joint bond axial + bending + torsion | 1.218314 | 1.143285 | 1.083205 |

At operating pressure, unchanged f=4 reaches end compression 0.856809 MN, bending 3.356559 kN·m and torsion 1.118657 kN·m. These are separate maxima, not assumed to occur at the same end. The full correlated per-end arrays are retained. Original sleeve area and overlap are held fixed here; the resized designs size each end for its actual correlated N/M/T.

Required extreme SiC compression at the unchanged screened limit is **1.124802 GPa**. The peak-compression local-shell sensitivity for that same point is 1.131897. Required stress is a target, not a qualified allowable.

## Linear and verified perfect nonlinear first loss

| Elements per arc | Perfect linear λ | 0.2 × linear | Perfect nonlinear first sampled loss |
|---:|---:|---:|---:|
| 6 | 5.672191923 | 1.134438385 | 5.524841712 |
| 12 | 5.668143555 | 1.133628711 | 5.449877138 |
| 24 | 5.667253080 | 1.133450616 | 5.430902212 |

The final tangent-sign bracket is **[5.430880209, 5.430924214]**. The m=12→24 nonlinear change is -0.3482%. Every recorded equilibrium uses smallest-algebraic tangent eigenvalues; separate shifted eigensolves and finite-difference tangents pass. This resolves the earlier nearest-zero selection concern for these new calculations. A further fresh random-start, unshifted eight-eigenvalue smallest-algebraic solve confirms the final positive snapshot has no hidden lower negative mode. It does not validate the frozen 026b nonlinear paths.

This is the ideal elastic frame's first sampled tangent loss. Joint/material limits and imperfection sensitivity remain separate. The resize ranking keeps the explicit 022d linear convention. If the same uncalibrated 0.2 were instead applied to this selected-frame nonlinear multiplier, the arithmetic sensitivity would be **1.086180**; that is not a measured knockdown or a reoptimized nonlinear design. Nonlinear continuation was performed for the selected f=4 section, not every resized candidate.

## Pins and film stiffness

The bare pinned f=4 frame has **480 internal roll mechanisms**, excluding whole-frame motions. Zero-strain finite rolls lower pressure potential or experience pressure torque, so the prescribed bare configuration has no positive stable pressure margin.

A source-based 270 GPa Zylon axial tangent, with perfect attachment and no assigned shear or prestress, gives the following conditional comparisons at m=6:

| Frame with projected film tangent | Perfect linear λ | Illustrative 0.2 × λ | Least declared screen |
|---|---:|---:|---:|
| ideal rigid | 7.155002 | 1.431000 | 1.218006 |
| ideal pinned | 2.047133 | 0.409427 | 0.409427 |

These are material-tangent sensitivities, not a coupled, pressure-equilibrated, wrinkling-aware membrane prediction. Filament data alone do not establish a complete 0/90 laminate or its attachments. The primary resize takes no stiffness credit.

## Best found closure witnesses

The objective is maximum SF at the available mass. Frequencies 1–10 were searched; 4/5/6 were reoptimized with m=6 and m=12, and 4/5 checked at m=24. Multiple local starts and adaptive exact FE checks support the ranking, not a global-optimum proof. Fine-mesh witnesses retain the m=12 optimum gyration and re-solve area for exact closure.

| Quantity | f=5, 5% reserve | f=5, 019 reserve |
|---|---:|---:|
| Declared screened SF | 1.143284619 | 1.083205354 |
| Peak-compression local sensitivity | 1.033222935 | 0.978132017 |
| OD (mm) | 249.558751 | 246.599720 |
| Wall (mm) | 0.978509 | 0.954326 |
| Both film directions (μm) | 82.041755 | 77.730485 |
| Tube mass (kg) | 4263.217784 | 4108.765016 |
| Film mass (kg) | 160.830867 | 152.379253 |
| All joint ends (kg) | 42.780659 | 38.858204 |
| Nodes (kg) | 5.040000 | 5.040000 |
| Systems (kg) | 100.000000 | 100.000000 |
| Reserve (kg) | 244.472108 | 411.298944 |
| Sag lift debit (kg) | 73.100733 | 73.100733 |
| Closure sum (kg) | 4889.442150 | 4889.442150 |
| Required extreme SiC compression (GPa) | 1.164235 | 1.145748 |
| Tube change vs selected 022d (kg) | +79.627761 | -74.825007 |
| Tube change vs matching-reserve 022d (kg) | +79.627761 | +74.979461 |
| Joint end peak bending (kN·m) | 3.079005 | 3.051787 |

Frequency 4, resized with the same rules, gives 1.129787 / 1.068508. Its 019 value happens to be near 1.07, but this is a different reserve and a resized design, not validation of the transferred correction.

The matching-reserve continuum comparisons are 1.258252 / 1.194121. Neither best found discrete witness recovers those SFs. The required strength, bond shear, laminate strength and density remain projections; joint rotational stiffness and local-shell interaction are open NFIs.

## Evidence, open work and stop

`RESULTS.json` carries all numeric witnesses and explicit null qualified capacities. `RESIZE.csv` and `MODES.csv` are machine-readable tables. `CHECKS.json`, `SCIENCE-CHECKS.json`, `NONLINEAR-AUDIT-*.json` and `GLOBAL-SA-AUDIT.json` retain the checks. `METHODS.md` states formulas, search bounds and failure interpretations; `SOURCES.md` and `INPUTS.json` trace inputs. `NFI.json` records unresolved issues. `EXECUTION.json`, `CODE.tar.gz`, `MANIFEST.json` and `PACKAGECHECK.json` pin the execution and review package. `SUMMARY` and `SELECTED-MODE` are supplied in PNG/PDF.

Times measure work; no task time budget was imposed. No other seat was messaged, restored or woken. Prior outputs remain frozen. **The brief names no successor: file this card, then stop.**
