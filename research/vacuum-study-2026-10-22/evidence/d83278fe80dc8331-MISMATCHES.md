# CHECK-042 exact discrepancies

The numerical table separates actual model inconsistencies from input rounding. Twenty numerical differences are not twenty substantive errors. All remaining compared fields are in NUMERIC-COMPARISONS.csv. Source/interpretation corrections follow below.

| Field | Owner | Independent | Independent − owner | Classification |
|---|---:|---:|---:|---|
| `Q_need_028b.waviness_mm_60psi` | 0.128773530738889 | 0.128773622546367 | 9.18074778422096e-08 | INPUT PRECISION / LABEL |
| `Q_need_028b.waviness_mm_35psi` | 0.0751178929310186 | 0.0751179464853807 | 5.35543620699963e-08 | INPUT PRECISION / LABEL |
| `route.forming_stress_strip_MPa` | 67.354704 | 134.709408 | 67.354704 | UNEXPLAINED STRAIN/STRESS PAIR |
| `route.forming_strain_small_blank_0.305x0.610` | 0.000145161 | 0.0001453515625 | 1.90562499999985e-07 | INPUT PRECISION / LABEL |
| `disbond_critical_diameter_mm.clamped` | 54.7800456012138 | 54.7799908325667 | -5.47686470611097e-05 | COEFFICIENT ROUNDING |
| `disbond_critical_diameter_mm.simply_supported` | 29.29213295474 | 27.1275980724118 | -2.16453488232818 | POISSON-DEPENDENT BOUNDARY COEFFICIENT |
| `reproduce.015b_Be_kd0.9.mine[0]` | 2.36027392038513 | 2.3602579343906 | -1.59859945325636e-05 | INPUT PRECISION / LABEL |
| `reproduce.015b_Be_kd0.9.mine[1]` | 0.0394729267236484 | 0.0394725257026587 | -4.01020989686252e-07 | INPUT PRECISION / LABEL |
| `reproduce.015b_Be_kd0.9.mine[2]` | 1.49852480893667 | 1.49851465951749 | -1.01494191817597e-05 | INPUT PRECISION / LABEL |
| `reproduce.015b_Be_kd0.9.mine[3]` | 0.0250611420419689 | 0.0250608874359688 | -2.54606000064245e-07 | INPUT PRECISION / LABEL |
| `reproduce.015b_021.mine[0]` | 36.4708377629321 | 36.4714897617356 | 0.000651998803505194 | INPUT PRECISION / LABEL |
| `reproduce.015b_021.mine[1]` | 11.8011972769932 | 11.8014082501152 | 0.000210973121992808 | INPUT PRECISION / LABEL |
| `reproduce.015b_021.mine[2]` | 0.139340390792906 | 0.139344127347082 | 3.73655417662544e-06 | INPUT PRECISION / LABEL |
| `reproduce.015b_021.mine[3]` | 7.0788895397607 | 7.07901609093948 | 0.000126551178782464 | INPUT PRECISION / LABEL |
| `reproduce.015b_021b.mine[0]` | 53.3640489043936 | 53.3644488066538 | 0.000399902260234342 | INPUT PRECISION / LABEL |
| `reproduce.015b_021b.mine[1]` | 45.8190980924844 | 45.8194414540033 | 0.000343361518950758 | INPUT PRECISION / LABEL |
| `reproduce.015b_021b.mine[2]` | 0.654408613600638 | 0.654415969675918 | 7.35607527968529e-06 | INPUT PRECISION / LABEL |
| `reproduce.015b_021b.mine[3]` | 18.3915495632466 | 18.3916873867886 | 0.000137823542075921 | INPUT PRECISION / LABEL |
| `reproduce.032_S200F.mine` | 0.152891458894879 | 0.152868766846361 | -2.26920485175142e-05 | INPUT PRECISION / LABEL |
| `reproduce.032_SR200.mine` | 0.0652185755336617 | 0.0652229064039409 | 4.33087027915113e-06 | INPUT PRECISION / LABEL |

Rounding explanation: 042 uses Q=.434628 rather than .43462785437520957. The 015b reproduction mixes rounded core dimensions with face dimensions; full-precision pins produce the differences above. The 032 values filed in that card use 20.21/30.12 mm; 042 uses slightly different cores. No engineering credit is lost on those tiny differences.

The .305×.610 label represents 12×24 in (.3048×.6096 m) in the owner arithmetic. The clamped coefficient is 14.682 versus the root 14.6819706421. Both are harmless rounding when declared. The simply supported 4.198 coefficient is a different Poisson convention; the appropriate value for this scalar Be model is 3.60050257046.

**S02.** `S-II gamma .21–.22 despite .254 mm precision` → Own skew-corrected graph reading gives .20991/.22226, approximately ±.01, at R/rho≈241. CR-1457 refers to S-II development tests, with plasticity corrections and thermal-gradient qualifications. No matched shape/buckling dataset is available here.
Evidence: `sources/cr1457-fig623.png; RESULTS.json sensitivities.SII_digitization`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S04.** `Rohr 57 in: .050 in after forming, .150–.200 after milling` → The values are supported, but are residual contour errors before extensive hand forming to the welding jig. The report also describes a final creep-sizing tensile failure. They are not achieved final bulkhead precision. Conversions are 1.27 and 3.81–5.08 mm.
Evidence: `sources/009-ntrs66014454.txt PDF pp.3–4,25`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S06.** `Ares I weld mismatch ≤.041 in` → The .041 in value is the magnitude of the maximum post-tack effective mismatch on CBMDA #1, approximately 20% of its weld land thickness. It is not a demonstrated final shape tolerance; the subsequent full weld had PAUT indications.
Evidence: `sources/008-ntrs20120014602.txt Table 2`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S10.** `ALMA 38 µm laser →55 µm holography→14 µm` → Values occur, but an intervening hard-stop accident led to a repeat laser measurement of 50 µm before 55 µm holography. Two full and one partial adjustments reached about 14 µm; later evaluation gives 16–17 µm. The sequence is not a pure instrument comparison.
Evidence: `sources/030-alma_proto.txt §5.1.1`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S12.** `LMT 98 µm, segments <20 µm` → The 98 µm overall optical RMS is supported. ≤20 µm applies to recent outer-ring segments; some inner segments remain 30–40 µm and 11 ring-4 segments require improvement. The claim cannot cover every segment.
Evidence: `sources/033-lmt_hughes.txt PDF pp.7–8,13–14`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S17.** `Moss R18.3 m held <2 cm; JUNO ±50 mm; JT-60SA ±8 mm` → Moss <2 cm is a required deviation, not a demonstrated final-shell bound in the cited sentence. JUNO ±50 mm is a diameter requirement; panels require <6 mm deviation. JT-60SA ±8 mm is a specified spherical-radius tolerance. They are not interchangeable measured RMS values.
Evidence: `sources/076-isprs-faig-1980.txt p.1; sources/074-arxiv-juno-cd-2311.17314.txt p.27; sources/077-jt60sa-cryostat.txt`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S21.** `345 MPa gives a 1.19e-3 elastic limit` → 345/E=1.189655e-3 is the elastic strain component at a tensile proof/yield proxy, not a measured proportional limit or compression forming allowable. The listed 4.645152e-4 strain gives Eε=134.709408 MPa; 67.354704 MPa needs half that strain or another stated model.
Evidence: `RESULTS.json route and sensitivities; intake/upstream/028b-METHOD.md`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S22.** `AF163-2U's own verified 200 F/6 h cure` → The sheet says limited family-level results suggest useful performance at 200 F/6 h. Its numerical 200 F metal-to-metal table is AF163-2K .06 lb/ft² at 50 psi, not U .015 on this core/Be. A supplier process qualification remains open.
Evidence: `sources/072-3m-af163-2.txt sections V and VI`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S24.** `A stress-free temperature above 54 C is the threshold` → The 54 C threshold in 037b concerns the separate 037 floated point. 028b's 30:1 scarf already binds at nominal load; positive added compression has no spare scarf margin.
Evidence: `intake/upstream/035/CARD.md sections 1,2 and residual state`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S26.** `028b closes with 2 kg to spare` → The selected 028b charged-total mass equals lift within numerical roundoff. Unallocated margin is approximately zero; its fixed reserve is already assigned. The 2 kg statement is not supported by the pinned point.
Evidence: `RESULTS.json sensitivities.mass_residual_at_028b_kg; intake/upstream/004/RESULTS.json`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S27.** `43.4 kg trapped air in this 23.2 mm core` → 034 used a 30.1182 mm core. At 028b, even a completely void thin-shell core contains at most 34.0851 kg at the specified 500 m atmosphere; a finite annulus with the stated solid fraction gives 33.7988 kg. Ground sea-level full-void upper estimate is 35.7709 kg.
Evidence: `RESULTS.json sensitivities.trapped_core_air; intake/upstream/012/CARD.md`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S31.** `1.22 mm upper gauge-patch deflection` → The value reproduces a first-order unconstrained local membrane estimate. Keeping the exact 1/(1−gauge_fraction) dependence gives 1.40410 mm before compatibility effects. Therefore 1.22 is not established as an upper bound.
Evidence: `RESULTS.json sensitivities.low_gauge_independent_membrane_patch_mm`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S35.** `Eq.3 values near .90–.95 from small fabrication errors` → The inverses/forward values reproduce, but .15/.254/1.27 mm examples are below d/t=.07, excluded from the fit's small-amplitude behavior. A monolithic-shell fit transferred through equivalent thickness does not validate sandwich buckling.
Evidence: `sources/baizhikova2026.txt Eq.3; RESULTS.json precedent_dimples`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S37.** `Tap a90/95 43 manual, 28 automated` → Table 4 full cumulative logit values are 41.8 and 29 mm. 43.3/28 remove best and worst inspectors. The worst manual fit did not converge; worst automated is 70 mm. Test panels have .5 mm Al skins, 19 mm panel thickness, 4.76 mm cells and 91 kg/m³ core.
Evidence: `sources/087-icaf2023-genest-tap.txt Table 4 and test-panel description`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S38.** `Disbond buckling diameter 29.292–54.780 mm` → The inferred coefficients are 4.198 and 14.682. Solving the circular-plate boundary equations at Be nu=.0752 gives k=3.600503 and 14.681971, hence 27.127598 and 54.779991 mm. The lower value is below even the 28 mm selected-cohort tap statistic; actual flaw boundary/contact effects remain unknown.
Evidence: `RESULTS.json disbond_critical_diameter_mm; independent boundary derivation in METHOD.md`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S45.** `Profiler .4 µm repeatability means yes for .075 mm waviness` → The current LJ-X8060 page confirms .4 µm Z repeatability but separately specifies linearity and temperature effects. Repeatability is not accuracy or an installed-surface acceptance capability.
Evidence: `sources/keyence-current.html; public page checked 2026-10-20`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S47.** `Fibre sensing .65 mm pitch, ±5 µε` → The Luna sheet distinguishes measurement uncertainty from system accuracy: the .65 mm-pitch column has ±5 µε uncertainty but ±25 µε system accuracy. Pitch availability also depends on the 610x/600x mode. It is not full-field shape data.
Evidence: `sources/163-luna-odisi6000.txt specification table and notes 6–7`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S48.** `OSHA .2 µg/m³ therefore every scarf must be supplier-cut` → The .2 value is an 8-hour TWA; the 15-minute STEL is 2.0 µg/m³. Controls and regulated-area criteria depend on exposure. Supplier-only cutting is the proposed process choice, not a categorical location requirement in this rule.
Evidence: `official public rule checked 2026-10-20, paragraphs (b),(c),(e),(f)`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).

**S52.** `Published gamma/Q map supports .2 / about .6` → The arithmetic is a projection. The historical .2 handbook design factor, isolated defect maps and reflector RMS do not establish any measured installed P2 gamma or Q. Qualified values remain null.
Evidence: `RESULTS.json; S02,S34–S36; CHECK.md`. See [source audit](2e007431289b1c04-SOURCE-AUDIT.md).
