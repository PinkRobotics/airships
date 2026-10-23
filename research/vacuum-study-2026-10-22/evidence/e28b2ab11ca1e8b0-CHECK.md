# Independent CHECK MAINLINE-042

**Disposition: complete; QUESTIONABLE / PROJECTION.** The owner's conclusion that the route is plausible in parts but unqualified is supported. The shape-map and approximately 5.7 km seam arithmetic reproduce. The source record does not establish an installed P2 knockdown factor of 0.2, or any other qualified gamma or Q. Several source populations, dimensional conventions and conditional calculations need correction.

Authority: `ord-admiral-rr2-check042-codex-1693-1020`; checked report: `rpt-mainline042-opus-build-route-1020`. Owner data, cards and literature were pinned. The owner's program was never opened, copied, hashed, imported or executed. Independent arithmetic is in `check_numbers.py`; equations and reproduction instructions are in [METHOD.md](46838a336c8b888f-METHOD.md).

There are 413 field comparisons, including table axes and range flags; 20 numerical differences; 52 source/claim audit rows; and 15 nonblocking NFIs. The 20 differences are not 20 substantive errors: most are input precision, printed dimension labels or coefficient rounding. [MISMATCHES.md](d83278fe80dc8331-MISMATCHES.md) lists the exact fields and deltas; [NUMERIC-COMPARISONS.csv](61724f7d562220c5-NUMERIC-COMPARISONS.csv) retains every comparison. All 20 numerical consistency checks pass. Passing those checks establishes arithmetic consistency, not experimental validation.

**Shape required at 028b.** The pinned point has 0.794624066986 mm faces and a 23.2372179060 mm core. With the explicitly inherited map convention ν=0.33, equivalent thickness is 41.6243712967 mm, R/t=240.243868880 and characteristic width is 0.356777058864 m.

| Quantity | Independent result | Interpretation |
|---|---:|---|
| Eq. 3 dimple at gamma 0.564164 | 16.0572954817 mm | Map amplitude |
| Lee dimple at gamma 0.564164 | 9.31826724099 mm | Lower-envelope amplitude |
| Eq. 3 single-dimple RMS | 0.202546305865 mm | Assumed Gaussian, specified width |
| Lee single-dimple RMS, width factors 1–5 | 0.117540379629–0.587701898144 mm | Width dependence must remain explicit |
| Waviness at Q=0.434627854375, Fc=60 psi | 0.128773622546 mm | Typical-strength input |
| Waviness at the same Q, Fc=35 psi | 0.0751179464854 mm | Minimum-strength input |

The owner already flags small-amplitude extrapolation and the absence of band-limited waviness data. Those caveats also constrain the headline conclusions. Lee's studied R/t values are 100 and 200; this point's 240.24 is outside that set. Its lower envelope spans defect widths, so the width-one RMS is not a unique partner to the envelope. The small 0.15/0.254/1.27 mm examples fall below Eq. 3's fitted amplitude range. Whole-panel RMS multiplied by √2 is a single-sinusoid assumption, not a measured wrinkle-band amplitude. Both maps remain transfers from different models to a sandwich. See [source audit S34–S36](2e007431289b1c04-SOURCE-AUDIT.md).

**S-II does not supply a matched shape/buckling calibration.** The 0.010 in figure is core-to-face matching gap, not deviation from a sphere. Separate CR-1457 development-test triangles give graph readings about 0.20991 and 0.22226, each with roughly ±0.01 reading uncertainty. Those tests carry material and thermal qualifications, and the specimen-level SDL 468 record was unavailable. They cannot be paired with the production fit tolerance to establish a process maximum or a qualified P2 gamma. [SD 71-256](https://ntrs.nasa.gov/api/citations/19720008130/downloads/19720008130.pdf), [CR-1457](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf).

The arithmetic mapping 1–5 mm to high gamma is reproducible; the proposition that this is the achieved final precision of those builds is not. Rohr's values precede hand correction; Ares' mismatch is post-tack; ALMA's measurement sequence includes damage and readjustment; LMT's best segment figure excludes poorer populations; several large-sphere tolerances are requirements rather than measured results. Exact source distinctions, including instrument specifications and historical costs, appear in [SOURCE-AUDIT.md](2e007431289b1c04-SOURCE-AUDIT.md). No unmatched precedent receives P2 qualification credit.

**NDE changes the lower flaw-size screen.** At physical Be ν=0.0752 and face stress 300.333333333 MPa, independently solving the circular-plate boundary equations gives:

| Boundary | Owner diameter | Independent diameter |
|---|---:|---:|
| Simply supported | 29.2921329547 mm | **27.1275980724 mm** |
| Clamped | 54.7800456012 mm | 54.7799908326 mm |

The inferred owner coefficients are 4.198 and 14.682. The correct roots for this isotropic screen give 3.60050257046 and 14.6819706421; the first difference is substantive, the second is rounding. Actual disbond edge restraint, contact and fracture are still unqualified.

Genest Table 4's full cumulative logit a90/95 values are **41.8 mm manual and 29 mm automated**. The 43.3/28 mm pair excludes the best and worst inspectors. Even 28 mm exceeds the corrected 27.13 mm screen. This is not an accepted POD margin, and the test uses aluminium skins and a different core. Other UT, shearography and thermography results likewise do not establish Be scarf or face-core POD. [Genest et al., ICAF 2023](https://icaf.aero/icaf2023/proceedings/documents/55.pdf).

**Seams reproduce, but the adopted ratio changes the panel count.**

| Assumed scarf ratio | Overlap | Two-skin seam length | Continuous panels per skin | Minimum integer count |
|---|---:|---:|---:|---:|
| 30:1 | 23.838722010 mm | 5683.037087840 m | 1188.560561664 | 1189 |
| 30.34:1 | 24.108894192 mm | 5685.225424611 m | 1189.287033638 | **1190** |

These are local rectangular-coverage estimates, not an actual spherical tiling or a complete bill. Poles, manhole, closures, scrap and smaller available stock remain open. The pinned 028b total mass equals lift to roundoff; it has **approximately zero unallocated mass**, not 2 kg spare. Its existing reserve is already assigned. A room-temperature seam needs its own thickness, mass, allowables, surface preparation and inspection specification before mass can close.

**Other material corrections.** The listed forming strain gives Eε=134.709408 MPa, twice the owner's 67.354704 MPa. The latter corresponds to half the stated strain and needs its own kinematic explanation; neither scalar estimate determines actual forming stress. The 345 MPa/E ratio is the elastic strain component at a proof/yield proxy, not a measured elastic limit. The 1.22457 mm gauge-patch estimate is first order; retaining the denominator gives 1.40410 mm before compatibility effects, so “upper” is unsupported.

The inherited 43.4 kg trapped-air estimate uses a thicker core. At this point, the 500 m full-void upper estimate is 34.08511 kg; an annular, solid-fraction-adjusted estimate is 33.79884 kg. The 1.061430 sea-level/design pressure ratio reproduces but supplies no reliability or certified proof claim.

Independent mass/scarf reclosure gives usage 0.971978 without residual cure strain, 1.052282 at 250 F with 30:1, and 0.972433 for the rounded 30.34:1 fix at 200 F. This confirms the conditional calculation. It does not qualify the cure: 3M's numerical 200 F data use a different adhesive variant and weight. The family-level low-temperature statement is limited evidence. The 54 C threshold also belongs to a different 037 point. [3M AF 163 technical data](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf).

**Follow-through and limits.** [NFI.json](48cd49a70dc75de3-NFI.json) assigns specific follow-up for matched buckling data, band-limited shape, tap cohorts, disbond restraint, cure, room-temperature seams, core air, stock/layout, forming, metrology, NDE coverage, jig/facility, heritage, process controls and numerical precision. None blocks filing or the next authorized card. The proposed F1 article remains useful once stock and process are specified; this check does not authorize physical manufacture or procurement.

Qualified installed gamma, Q, safety factor and failure probability are all **null**. Three scientific jobs were admitted and released: an initial JSON serialization error was corrected, followed by two successful runs. The final run's source hashes are retained in `EXECUTION.json`; no admission refusal or live own job remains. Packaging checks are in `PACKAGE-CHECK.json`. Time is measured without a budget. The CHECK brief names no successor.
