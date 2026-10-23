# MAINLINE-022d independent CHECK

Unit `vacuum-mainline022d-check-1020`. Authority `ord-admiral-rr2-check022d-codex-1693-1020`.

**Completed: the primary arithmetic and reported numerical optima reproduce.** All 64 primary witnesses and all 1,792 numeric primary-table cells pass. Across 17,452 comparisons, 50 precise differences remain in 16 square-membrane sensitivity rows; they come from one coefficient precision discrepancy and do not change the primary result. No owner code was read, copied or run.

The conditional best equilateral in-band multiplier is **1.258252476558** at chord spacing **3.170758569107 m**. Solving its active equations independently gives 1.258252476557888 at 3.170758569107043 m. The curved member length is 3.184193538867475 m, and the half-wave equals that length within numerical precision. Local wall, global surrogate and film constraints bind. All results remain **QUESTIONABLE**; unvalidated transfers remain **PROJECTION**.

## Headline witness

OD 275.082856380206 mm; wall 1.137364845158 mm; area 0.000978844783292751 m²; inertia 0.00000918247267153439 m⁴. Fractional continuum counts are 432.986282269492 members and 146.328760756497 nodes. Operating force per member is 873,771.336576808 N.

| Scored mode | Recomputed multiplier |
|---|---:|
| compression | 4.368985906310 |
| euler | 4.194174921858 |
| local | 1.258252476558 |
| perry | 3.454499160203 |
| global | 1.258252476558 |
| tension | 3.999216615332 |
| film | 1.258252476558 |

The target's mean compression is 1.123186196 GPa, amplified bending is 0.074910188 GPa, and extreme compression is **1.198096384 GPa**. Opposite-face tensile stress is zero. The tensile screen remains in the model and binds some overall optima; it is inactive at this in-band point.

**Both Zylon plies are charged.** Total gauge is 109.440222378107 μm, split equally into 54.720111189054 μm plies. Each ply weighs 107.270778772652 kg, giving **214.541557545304 kg** total. Each direction reaches the assumed 3.48 GPa at the target.

**Joint dimensions use the candidate multiplier.** Each end is designed for 1,099,424.948193309 N, with 0.0007479081280226595 m² axial section and 0.04402043674327406 m overlap. Total joint mass is **44.191468266691 kg**, compared with 27.912763991761 kg when sized at multiplier one. Axial and bond multipliers equal the target by construction; their qualification remains open.

| Mass term | kg |
|---|---:|
| tube | 4183.590022951527 |
| film | 214.541557545304 |
| joint | 44.191468266691 |
| nodes | 2.926575215130 |
| systems | 100.000000000000 |
| vehicle | 4545.249623978652 |
| reserve | 244.472107509500 |
| sag_lift_loss | 99.720418701847 |
| closure | 4889.442150190000 |

Vehicle mass excludes reserve and lost lift; their sum closes to the prescribed 4,889.44215019 kg.

## Independent recovery of the key optima

Eight active-equation solutions used coarse starting guesses, while a separate independent model recovered all 176 primary/sensitivity optima with four independent starts plus one filed-witness start each: 880 local searches. No materially better witness was found, and every case was recovered within 10⁻⁶ SF. These are numerical surrogate optima with no mathematical global certificate.

| Case | Independent multiplier | Spacing, m |
|---|---:|---:|
| cap/equilateral/5/cfrp_zylon/overall | 1.397732582060 | 6.085746577765 |
| cap/equilateral/5/cfrp_zylon/in_band | 1.258252476558 | 3.170758569107 |
| cap/equilateral/019/cfrp_zylon/overall | 1.328130588933 | 6.038536265233 |
| cap/equilateral/019/cfrp_zylon/in_band | 1.194121426005 | 3.145836800220 |
| membrane/equilateral/5/cfrp_zylon/overall | 1.384439695241 | 6.076890836212 |
| membrane/equilateral/5/cfrp_zylon/in_band | 1.251857091874 | 3.168322835340 |
| membrane/equilateral/019/cfrp_zylon/overall | 1.315080667599 | 6.029445592268 |
| membrane/equilateral/019/cfrp_zylon/in_band | 1.187857743489 | 3.143341561516 |

The best equilateral overall point remains outside the member-wave screen: SF 1.397732582060 at about 6.085747 m, half-wave/member about 0.569. Sixteen primary overall optima fail that screen. The better numerical two-way values retain the missing-shear NFI.

## Exact mismatch

`INPUTS.json`/METHOD declare square-membrane coefficient **0.07028850747757764**. The 16 square-membrane sensitivity rows imply **0.07028850698306077**, about 7.04 parts per billion lower. With the declared coefficient, the largest least-SF difference is **3.97619115410919e-09**, and the largest sag-mass difference is **3.6341572240417e-06 kg**.

For example, `SENSITIVITIES.two_way_square_cell[16]`, `membrane/two_way/5/projection/overall`, gives sag mean 0.35214890066282484 m; the declared formula gives 0.3521489031403789 m. The corresponding sag masses are 516.543503413166 and 516.5435070473233 kg. Substituting the output-implied coefficient into the independently written model reconciles that row's SF fields to roundoff.

`MISMATCHES.csv` and JSON enumerate **every one of the 50 failed comparisons**, with exact row, field, card value, check value, difference and tolerance. This is NFI-022D-CHECK-01, a precision fix. `FIELD-CHECKS.csv` retains all passing comparisons as well.

## Continuum and qualification NFIs

Frozen MAINLINE-026b frequency-4 results give discrete linear multiplier **5.254643802209333**, versus continuum **6.1933813461115825**: **15.1571087172215% below continuum**. Its nominal half-wave/spacing is above one. This evidence shows why the one-member screen cannot establish continuum accuracy. The 022d geometry and joints differ, so this gap is carried as NFI-022D-CHECK-02 rather than applied as a universal correction.

The check also records full-size compression/contact and tensile reliability, the complete membrane, joint density/bond/stiffness, local-shell conventions, two-way shear, integer geometry/manufacturing/installed mass, and search extent. The local convention diagnostic at the unchanged headline geometry is 1.229307846 for an assumed ν=0.14 and mid-surface radius; it is a model sensitivity, not a replacement optimum. All nine NFI rows have explicit owners and discriminating next evidence.

The source chain and tags are detailed in `SOURCES.md`; equations, tolerances and independence are in `METHODS.md`. The rounded 15.586 MPa tensile input reconciles to the original continuum reference, while the separate 1,047-member example gives 15.584177866 MPa. Neither is a calibrated allowable. Qualified structural SF, full-size compression allowable and assembly failure probability remain null.

## Delivery

Five scientific invocations were admitted through simjob, each with one CPU core and 2 GiB cap; all completed and released. There were no refusals in this check. Source pins and measured clocks are in `EXECUTION.json`. Watchdogs are technical controls and no work budget was imposed.

`RESULTS.json`, `CHECKS.json`, `NFI.json`, the full field/mismatch ledgers, independent search results, source arithmetic, code archive and manifest form the delivered check. Prior 026/026b artifacts remain frozen. CHECK names no successor: file this report and end the turn. Open NFIs do not stop other authorized work.
