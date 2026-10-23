CHECK-041 covers every numeric cell in the CARD's five tables. `CARD-TABLE-CHECK.json` and CSV retain the printed value, independent value, exact difference, display tolerance, and basis. A specified geometry or mesh count is explicitly identified as an input, rather than an independently optimized choice.

| CARD content | Independent evidence | Qualification |
|---|---|---|
| Selected f4 SF, mass increase, closure deficits | `SCALAR-CHECK.json`, `SUPPLEMENT-CHECK.json`, seven independent linear solves | Same declared equations; no certified capacity |
| R, p, OD, wall, film gauge | Exact pinned input and unit conversion | Inputs, not design optimization results |
| 162 joints, 480 members, 320 cells; arc lengths | Independently generated integer mesh and spherical geometry | Geometry reproduced |
| Both columns of selected mass table | Independent discrete mass plus reconstructed continuum baseline | Cap sag and joint mass remain assumed models |
| All 30 limit-table cells | Independent FE forces and modes, member formulas, correlated joint-end sizing | Conditional scalar screens |
| Operating end N/M/T, 1.124802 GPa selected required compression, 1.131897 local sensitivity | Independent arrays and scoring | Separate end maxima are not falsely combined into one joint |
| Linear m=6/12/24 table | Fresh independent matrices and eigensolves | Eight modes retained |
| Nonlinear m=6/12/24 table and 5.430880209–5.430924214 bracket | Re-equilibrated supplied endpoints and separate zero-start continuations | Different finite-rotation formulations; exact differences retained |
| −0.3482% reported nonlinear mesh change and 1.086180 sensitivity | Arithmetic replay of reported midpoints plus separate arithmetic from independent brackets in `NONLINEAR-CHECK.json` | Replay and independent-model result distinguished; 0.2 is not calibrated |
| 480 bare-pin internal rolls and zero positive margin for the prescribed state | Independent rigidity rank and finite pressure-descending isometries in `PIN-CHECK.json` | No assertion about all rearranged configurations |
| Film rigid/pinned λ, ×0.2, and least screens | Independent film assembly and endpoint releases | Numerical mismatch remains; orientation convention not uniquely supplied as data |
| Every f5 closure-table cell, including SiC peaks and both tube-mass comparisons | Independent FE, cap/mass arithmetic, exact joint sizing, continuum baseline reconstruction | Fixed witnesses evaluated; optimizer not rerun |
| f4 resized 1.129787 / 1.068508 | Two additional independent m24 frame solves | Confirms these witnesses are lower than f5 under the stated screens |
| Continuum comparisons 1.258252 / 1.194121 | Independent homogenization/scalar arithmetic at the filed 022d dimensions | Earlier optimization not rerun |
| Frequencies 1–10; refined 4/5/6 at m6/m12; 4/5 at m24 | Filed search metadata inspected | Historical execution scope, not independently repeated searches |
| Cited transferred 1.07, reserve name 019, card identifiers, prior 026b audit history | Contextual references in the filed card | Not new physical calculations |

The scientific results remain conditional even where arithmetic agrees. Exact nonlinear differences must be assessed with bracket widths and formulation differences, not hidden by rounding. The film mismatch and the m6 bracket difference are carried as NFI work. A failed low-pressure convergence attempt and earlier checker interpretations are retained, not reclassified as owner failures.
