# Independent check of MAINLINE-015b — ESTIMATE / QUESTIONABLE

Order `ord-admiral-rr2-check015b-codex-575b-1020`. Unit `vacuum-mainline015b-check-1020`. Nothing here is a certification.

The focused correction passes its arithmetic check. The live lambda-1 amplitude/width pair and nu 0.33 repair the principal error found in 015. All 1,331 scalar/display/flag comparisons match at the stated precision. There is one false blanket prose claim about rounding and two qualifications concerning RMS area measure and Lee's envelope width. These do not invalidate the reproduced arithmetic. All fourteen prior findings are dispositioned individually below; this revision does not close all fourteen.

## Independence, identity and coverage

Own `check.py` derives the equations and performs the comparisons. The owner's `map015b.py` and earlier owner scripts were not read as code or run. Pinned 015, 021 and 021b RESULTS provide geometry and gamma inputs only; this check does not redo the 021/021b optimisations. P2-E's filed input rounding is preserved. The former 015 check and its primary PDFs are immutable inputs.

All original owner/authority pins, seven owner-declared upstream pins, and the prior primary-source manifest match their hashes and lengths; `SOURCE-PINS.json` records each verification. Snapshot and prior-check pins are in `INPUTS.json`.

Every one of the 1,201 numeric, Boolean, null or decimal-string leaves of owner RESULTS is covered, with no missing or extra scalar path. Categories: 647 numeric, 223 Boolean, 24 null, 216 display fields and 91 leaves in the owner's 47 self-check records. A further 40 directly parsed CARD table entries and 90 CARD/report quantities match. `NUMERIC-CHECK.csv` gives reported value, independently computed value, exact floating-point difference and disposition for each comparison; `PROSE-CHECK.json` identifies checked excerpts. Booleans and displays are compared exactly. Raw tolerances are relative 5e-12 or absolute 2e-12; the published ten-decimal threshold is allowed 5e-11.

The published threshold 0.5183040769 differs from the independently recovered 0.5183040769297532 by -2.97532e-11, consistent with rounding. Apart from this intentional printed precision and floating-point operation-order differences, there are no numerical mismatches under the specified approximate map. Coefficients and range limits are separately checked against primary sources. Identifiers, dates and equation numbers are metadata.

## Derivation

Write face thickness f, core depth d, face-center separation h=d+f, radius R=10 m, and alpha=delta/teq. Matching the face-dominated extensional and bending stiffnesses gives

`teq_thin = sqrt(3) h`, `teq_finite = sqrt(3h²+f²)`, and `Eeq/Ef = 2f/teq`.

The latter modulus relation is still missing from the owner's description. It is required if the equivalent monocoque is used to calculate absolute pressure. This card only maps dimensionless defects and does not claim a new pressure score. For P2-E, Eeq/Ef=0.00341122758754; keeping Ef with the equivalent thickness would not preserve extensional stiffness.

At a chosen width parameter lambda,

`beta0 = lambda sqrt(teq/R) / [12(1-nu²)]^(1/4)`, `width = R beta0`, `classical wavelength = 2pi R beta0(lambda=1)`.

The map's RMS is `delta beta0/sqrt(8)`, a small-angle area approximation for a single Gaussian dimple on a whole sphere. It is not an arbitrary manufactured-field maximum or a hemispherical RMS. The classical wavelength is distinct from `sqrt(R teq)`.

For [Baizhikova et al., Eq. 3](https://www.epfl.ch/labs/flexlab/wp-content/uploads/2025/12/Baizhikova-et-al.-2026-A-probabilistic-buckling-model-for-hemispherical-shells-with-non-interacting-localized-defects.pdf), lambda=1 gives

`alpha = -ln[(kd-0.45)/0.51]/3.88`.

There is no finite real inverse at or below kd=0.45. The reported 0.2 and 0.3 rows correctly return null. The old-to-live RMS ratio at fixed amplitude is

`2.625 [(1-0.33²)/(1-0.30²)]^(1/4) = 2.611262732308197`.

For [Lee et al., Eq. 23](https://www.epfl.ch/labs/flexlab/wp-content/uploads/2017/12/64_2016_Lee_JAM_GeometricRolePreciselyEngineeredImperfectionsCriticalBucklingLoadSphericalElasticShells.pdf),

`alpha = 0.25/(kd-0.068) - 0.28`.

This uses the original coefficient 0.068. Alpha at kd 0.9/0.7/0.5/0.3/0.2 is 0.0204807692308 / 0.115569620253 / 0.298703703704 / 0.797586206897 / 1.61393939394. Its forward equation round-trips every level checked.

| Shell | tf mm | core mm | teq mm | exact finite-face teq mm | R/teq | lambda-1 width m | classical wavelength m |
|---|---:|---:|---:|---:|---:|---:|---:|
| Al-P2-E | 0.336094970 | 113.432052508 | 197.052211716 | 197.052498339 | 50.747971377 | 0.776271666 | 4.877458724 |
| Be-015 | 0.693223127 | 41.549713762 | 73.166912953 | 73.170196866 | 136.673799623 | 0.473021023 | 2.972078745 |
| Be-021 | 0.843448044 | 20.213376387 | 36.471489762 | 36.481241345 | 274.186770689 | 0.333964135 | 2.098358544 |
| Be-021b | 0.691747999 | 30.118230885 | 53.364448807 | 53.368932083 | 187.390673447 | 0.403969979 | 2.538218236 |

## Recomputed tolerance rows

These are the owner's conditional small-angle RMS quantities, not validated manufacturing tolerances. Lee k1 and k5 columns bound geometry at the envelope-derived amplitude; they are not a statement that every width has the requested kd.

| Shell | kd | Eq. 3 amplitude mm | Eq. 3 RMS mm | Lee amplitude mm | Lee RMS k1 mm | Lee RMS k5 mm |
|---|---:|---:|---:|---:|---:|---:|
| Al-P2-E | 0.9 | 6.356617048 | 0.174459567 | 4.035780875 | 0.110763410 | 0.553817052 |
| Al-P2-E | 0.7 | 36.208334144 | 0.993750329 | 22.773249278 | 0.625019750 | 3.125098751 |
| Al-P2-E | 0.595 | 63.873203913 | 1.753022305 | 38.303659522 | 1.051257263 | 5.256286315 |
| Al-P2-E | 0.5 | 117.946298130 | 3.237077190 | 58.860225462 | 1.615439368 | 8.077196838 |
| Al-P2-E | 0.468 | 169.832545019 | 4.661113290 | 67.983013042 | 1.865817447 | 9.329087235 |
| Al-P2-E | 0.3 | not invertible | — | 157.166126103 | 4.313479015 | 21.567395077 |
| Al-P2-E | 0.2 | not invertible | — | 318.030327151 | 8.728452984 | 43.642264921 |
| Be-015 | 0.9 | 2.360257934 | 0.039472526 | 1.498514660 | 0.025060887 | 0.125304437 |
| Be-015 | 0.7 | 13.444416632 | 0.224841986 | 8.455872345 | 0.141414476 | 0.707072379 |
| Be-015 | 0.595 | 23.716583082 | 0.396631835 | 14.222426116 | 0.237853275 | 1.189266377 |
| Be-015 | 0.5 | 43.794314478 | 0.732408174 | 21.855227888 | 0.365502868 | 1.827514341 |
| Be-015 | 0.468 | 63.060053626 | 1.054604902 | 25.242584969 | 0.422152414 | 2.110762069 |
| Be-015 | 0.3 | not invertible | — | 58.356920572 | 0.975950558 | 4.879752788 |
| Be-015 | 0.2 | not invertible | — | 118.086963148 | 1.974864959 | 9.874324793 |
| Be-021 | 0.9 | 1.176517084 | 0.013891626 | 0.746964165 | 0.008819716 | 0.044098580 |
| Be-021 | 0.7 | 6.701634438 | 0.079128980 | 4.214996222 | 0.049768211 | 0.248841053 |
| Be-021 | 0.595 | 11.821998253 | 0.139587242 | 7.089448598 | 0.083708063 | 0.418540316 |
| Be-021 | 0.5 | 21.830139166 | 0.257757517 | 10.894169071 | 0.128631978 | 0.643159888 |
| Be-021 | 0.468 | 31.433526541 | 0.371148700 | 12.582663968 | 0.148568738 | 0.742843690 |
| Be-021 | 0.3 | not invertible | — | 29.089157179 | 0.343467757 | 1.717338786 |
| Be-021 | 0.2 | not invertible | — | 58.862774082 | 0.695017214 | 3.475086072 |
| Be-021b | 0.9 | 1.721459313 | 0.024586735 | 1.092944961 | 0.015609982 | 0.078049908 |
| Be-021b | 0.7 | 9.805714826 | 0.140050079 | 6.167309084 | 0.088084565 | 0.440422823 |
| Be-021b | 0.595 | 17.297742008 | 0.247054924 | 10.373157753 | 0.148154580 | 0.740772898 |
| Be-021b | 0.5 | 31.941479538 | 0.456204040 | 15.940158505 | 0.227665243 | 1.138326216 |
| Be-021b | 0.468 | 45.992988739 | 0.656894658 | 18.410734838 | 0.262951239 | 1.314756194 |
| Be-021b | 0.3 | not invertible | — | 42.562748307 | 0.607902264 | 3.039511321 |
| Be-021b | 0.2 | not invertible | — | 86.126986165 | 1.230108299 | 6.150541493 |

All nine levels for every shell, including both unrounded gammas, are retained in `RESULTS.json`; above are the seven requested rounded/low-kd levels.

For the actual 021 geometry at gamma 0.5953179642995181, Eq. 3 amplitude is 11.8014082501152 mm, matched RMS 0.139344127347082 mm, and retired RMS 0.363864126707443 mm. Lee amplitude is 7.07901609093948 mm and the approximate geometric RMS interval is 0.0835848823091335–0.417924411545668 mm.

For actual 021b at gamma 0.46822856667720764, Eq. 3 amplitude is 45.8194414540033 mm, matched RMS 0.654415969675917 mm, and retired RMS 1.70885203304205 mm. Lee amplitude is 18.3916873867886 mm and the approximate geometric interval is 0.262679193662454–1.31339596831227 mm.

## Source limits and interpretation

Baizhikova's source computations use nu 0.5 and R/t from 100 to 1550. Its discussion explicitly excludes the near-perfect asymptote around alpha below 0.07 from what Eq. 3 captures. The kd 0.9 inverse is 0.0322585419984552, so every such row needs the limitation. P2-E has R/teq=50.7479713774, outside the source range. The three Be geometries lie inside that radius interval; this does not validate material or sandwich transfer.

Lee section 7 supplies no FEM values below alpha 0.15 and no ODE values below 0.2. The computed radii are R/t=100 and 200. Kd 0.9 and 0.7 inverses are below both amplitude limits. Kd 0.595 and the actual 021 gamma lie between the two limits. Kd 0.5, 0.468, actual 021b gamma, 0.3 and 0.2 satisfy both amplitude cutoffs. The numerical range flags all reproduce. Be-015 and Be-021b lie between the computed radii; P2-E and Be-021 lie outside the interval. None is exactly a computed radius.

Lee Fig. 6(c) provides a minimizing width as a function of amplitude. The scalar Eq. 23 does not encode that width, but the paper does provide information beyond the scalar envelope. The owner's k1–k5 RMS span is a defensible broad geometric bound, conditional on the source sweep and mapping. It is not an iso-knockdown curve; equality at both endpoints is not established. This is NFI-015B-CHECK-LEE-CRITICAL-WIDTH.

## Exact corrections and additional qualifications

The CARD says rounding gamma changes the fourth digit of amplitude. For 021, using 0.595 instead of its actual gamma gives 11.8219982525557 rather than 11.8014082501152 mm: +0.0205900024405 mm, or +0.174470724206% relative to the actual-gamma value. For 021b, using 0.468 gives 45.9929887386092 rather than 45.8194414540033 mm: +0.173547284606 mm, or +0.378763422466%; the third significant digit changes. On P2-E the latter delta is +0.640836306447 mm. The two numerical columns are correct; the blanket prose is not. NFI-015B-CHECK-ROUNDING-PROSE records this correction.

For a Gaussian displacement referenced to the original spherical surface, retaining the spherical area element gives

`RMS/delta = sqrt[ (1/2) integral_0^pi exp(-2(theta/beta0)²) sin(theta) dtheta ]`.

Replacing sin(theta) by theta and extending the negligible Gaussian tail gives the owner's beta0/sqrt(8). Direct quadrature and the equivalent infinite-tail Dawson-function expression agree to better than 1e-13 in RMS/amplitude for these widths. The widest P2-E k5 calculation overstates this spherical-area RMS by 0.628886203836%; its exact k5/k1 ratio is 4.96999986296 rather than 5. At lambda 1, the largest overstatement is only 0.025110128610%. This is a model-precision qualification, not an error in implementing the stated formula.

| Shell | k1 RMS approximation overstatement % | k5 overstatement % | Exact k5/k1 ratio | Eeq/Ef |
|---|---:|---:|---:|---:|
| Al-P2-E | 0.025110129 | 0.628886204 | 4.969999863 | 0.003411227588 |
| Be-015 | 0.009323131 | 0.233234636 | 4.988830476 | 0.018949087761 |
| Be-021 | 0.004647233 | 0.116219693 | 4.994427853 | 0.046252459096 |
| Be-021b | 0.006799795 | 0.170078056 | 4.991849948 | 0.025925424671 |

NFI-015B-CHECK-RMS-AREA asks that the approximation be named. No fit coefficient is changed and no physical validation is inferred from this integration.

## Continuous threshold and manufacturing comparison

The original 015 threshold is independently reconstructed from its mass law `1.05 Mstructure + 100 = 4889.442150186961 kg`, pressure 95460.83791390515 Pa and original Be/CR-III properties. Yield sets f=pR/(4 sigma_y). At the yield-feasible core-fraction boundary x=0.140403238862653, global buckling with the existing NASA Kc gives kd=0.5183040769297532. Global capacity is increasing across the yield-feasible split interval, as confirmed by the analytic derivative; all other original modes exceed one at the crossing. The 0.518 grid optimum is 0.999887434269507 and the 0.519 grid optimum is 1.00017826831089. Thus 0.519 remains the first passing level on the original 0.001 grid. This recheck does not conflate the original 015 optimum with either 021 floating-point geometry.

Against 0.25 mm, the matched Eq. 3 RMS ratios are 0.697838266371 for P2-E kd 0.9, 0.157890102811 for frozen Be kd 0.9, 0.557376509388 for actual 021 and 2.61766387870 for actual 021b. The directions in the corrected CARD are right. The last is looser; the first three are tighter. The GBT figure refers to an active assembled surface under benign nighttime conditions, not proof of a loaded pressure-shell defect spectrum. The corrected CARD appropriately disclaims a manufacturing proof, but does not restore all old benchmark provenance.

## Response to every earlier finding

Three resolved in this map; five partly addressed; five not revisited because they are outside the focused map; one validation finding acknowledged and still open. The unchanged original sections are not silently approved. `COVERAGE.json` retains the original text and requested action for each finding.

| Prior finding | Disposition | What 015b addresses | What remains |
|---|---|---|---|
| 1. RMS-WIDTH | resolved in new map | The live Eq. 3 amplitude and width both use lambda 1; the mixed width 2.625 is explicitly retired. The small-amplitude restriction is flagged. | No remaining width/amplitude mismatch in the live map. This does not validate the monocoque transfer. |
| 2. NU | resolved in new map | All live width and RMS rows use the declared nu 0.33. Nu 0.30 appears only in explicitly retired comparisons. | No remaining internal nu mismatch. Source-to-sandwich material transfer remains part of MODEL-VALIDATION. |
| 3. SMALL-DEFECT | partly addressed | Every kd 0.9 Eq. 3 row is flagged below alpha 0.07; P2-E is flagged outside R/t 100–1550; source nu 0.5 is disclosed. | No valid near-perfect replacement is supplied. The inherited 1/3/10 mm seam calculations are not revisited. |
| 4. LOW-KD-ENVELOPE | partly addressed | Primary Lee Eq. 23 now supplies kd 0.2/0.3 amplitudes, with FEM/ODE cutoffs and k 1–5 RMS bounds. Eq. 3 below its floor returns null. | The old one-thickness bound and universal worst-width/plateau language are not explicitly repaired in the old 015 artifacts. Lee critical-width interpretation needs the new qualification below. |
| 5. EFFECTIVE-MODULUS | partly addressed | The thin-face thickness is declared, and exact finite-face A/D-equivalent thickness is stored and reproduces. | The simultaneous effective modulus Eeq/Ef = 2tf/teq is still absent. Thickness alone does not match extensional and bending stiffness; no new pressure rescore is claimed. |
| 6. SHEAR-RULE | not revisited outside focused map | 015b acknowledges unquantified core-shear effects on imperfection sensitivity. | It does not source or remove the old standalone square-root shear rule or reconcile it with NASA Kc. No new shear multiplier is applied. |
| 7. HYDROSTATIC | not revisited outside focused map | 015b contains no hydrostatic-gradient recomputation. | The old sea-level-density gradient is not corrected to the pinned 500 m density. The previous finding remains attached to the old card. |
| 8. ONE-FACE | not revisited outside focused map | 015b contains no thickness-loss sensitivity calculation. | The prior both-faces versus one-face labeling and local-patch distinction remain unrepaired in the earlier sensitivity section. |
| 9. SOURCE-IDENTIFIERS | partly addressed | Lee Eq. 23 is now cited and pinned directly, avoiding the later paper's printed coefficient ambiguity. | The two incorrect DOI identifiers in the old 015 material are not expressly corrected. They are not repeated in this focused card. |
| 10. MANUFACTURING-PROVENANCE | partly addressed | The comparison is narrowed to a 0.25 mm assembled-surface figure, and the card avoids a manufacturing-proof claim. | The active-surface/benign-night conditions of the GBT benchmark remain unstated here. Old replica/MeerKAT/DVA-C/panel-target provenance errors are not repaired. |
| 11. MANUFACTURING-METRIC | resolved in new map | The revised ratios and looser/tighter directions reproduce; the card explicitly separates single-dimple RMS from assembled-surface RMS and disclaims manufacturing proof. | The interpretive error is resolved for this map. Local maximum, spectrum and loaded-shape qualification are still future validation, not achievements. |
| 12. PROJECTION-TAGS | not revisited outside focused map | 015b maps only Al and Be, with QUESTIONABLE retained. | The old CNT and graphene rows requiring PROJECTION tags are omitted rather than corrected. No new CNT or graphene result is claimed. |
| 13. PNAS-CONSISTENCY | not revisited outside focused map | 015b does not use the PNAS stochastic estimate. | The earlier mean/quantile/support inconsistency is neither repeated nor reconciled. The earlier reliability claim remains unresolved. |
| 14. MODEL-VALIDATION | acknowledged open | The card and NFI explicitly retain QUESTIONABLE and identify the missing sandwich imperfection/core-shear study. | No matching sandwich experiment or validated nonlinear imperfection model is supplied. The admission answers the request for qualification; the scientific validation remains open. |

## Filing

`NFI.json` carries the eleven earlier findings that remain open in some respect and the three new qualifications, all nonblocking. `COVERAGE.json` separately records the three resolved findings. No additional job is named. The one report closes the assigned check work; it does not certify a vacuum shell or close the remaining scientific questions.

Start measured 2026-10-20T01:24:12-07:00; arithmetic completed 2026-10-20T01:33:54-07:00. Final assembly/end time is recorded in WORK.json. These are measurements, not work limits.
