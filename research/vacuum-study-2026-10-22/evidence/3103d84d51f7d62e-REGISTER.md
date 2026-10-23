# MAINLINE-030b complete issue register

711 source/authored records under94 topics/rows. Original fields stay verbatim in REGISTER.json; all source fields stay verbatim in NFI.json. Historical “today” and “needed” fields below are explicitly the030 record, not silently current values.030b additions and dispositions follow each row. Nothing closes merely because it was merged.

[Morning read](e5d802234971405e-CARD.md) · [All raw findings](8b3d13a96989a2c8-NFI.json) · [Coverage](0a76db86490b59c3-REGISTER-COVERAGE.json) · [Corrections](c0d0e9df563a9928-LEDGER.md)

## T01 — Case and atmosphere

<a id="R001"></a>
### R001 — hull radius and volume convention (mould line vs mid-surface, wall intrusion)

**Original030 unknown:** Handbook radius is the middle surface; ratios use external 10 m and are unaffected since both pressures scale as 1/R^2; absolute pressure on thick rows needs an inner mould line.

**Original030 today:** buckling-peak core 1.81457668 m at 1 kg/m3 [MAINLINE-007]; external radius 10 m [MAINLINE-07B]; R = 10 m external [CHECK-MAINLINE-07B]

**Original030 needed:** Inner and outer mould lines [MAINLINE-007]; Inner mould line for absolute pressure [MAINLINE-07B]; Define inner and outer mould lines. [rpt-mainline-grok-estimates-card-1019]; Inner and outer mould lines. [MAINLINE-002]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N036 | NFI-GEOM | 030 retained | {"NFI_id": "NFI-GEOM", "gap": "External area and external volume ignore wall and core intrusion.", "direction": "Inner and outer mould lines.", "effect": "A smaller displaced volume lowers the ceiling. At 1 kg/m3 the buckling-peak core is 1.81457668291 m, which is not a thin wall on a 10 m radius."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N045 | NFI-GEOM | 030 retained | {"NFI_id": "NFI-GEOM", "gap": "The handbook radius is the middle surface. These ratios use the external 10 m in both the classical pressure and the handbook pressure, so the ratio is unchanged.", "direction": "An absolute pressure on the thick low-density rows still needs an inner mould line.", "effect": "The reported safety-factor ratios do not move with that choice."} | [rpt-ref-3dd5ab5528276031581d](07d0f8e52a240650-NFI.json) |
| N249 | NFI-GEOM | 030 retained | {"NFI_id": "NFI-GEOM", "linked_inputs_or_points": "all points", "questionable_assumption_or_gap": "External volume ignores skin intrusion and member protrusion.", "direction_of_further_investigation": "Define inner and outer mould lines.", "how_it_affects_margin_or_SF": "Volume error moves lift linearly."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |
| N259 | NFI-GEOM | 030 retained | {"NFI_id": "NFI-GEOM", "gap": "External volume still ignores wall intrusion.", "direction": "Inner and outer mould lines.", "effect": "Volume error moves lift and the allocation thicknesses."} | [rpt-mainline002-grok-strength-card-1019](b155c07e690eaa66-NFI.json) |
| N269 | NFI-GEOM | 030 retained | {"NFI_id": "NFI-GEOM", "gap": "External volume still ignores wall and core intrusion.", "direction": "Inner and outer mould lines.", "effect": "A smaller displaced volume lowers the ceiling."} | [rpt-mainline003-grok-p2-targets-1019](2090c6e1f4ca8afb-NFI.json) |
| N303 | NFI-GEOM | 030 retained | {"NFI_id": "NFI-GEOM", "gap": "Confirmed: handbook radius is the middle surface; ratios use external 10 m in both pressures and do not move with that choice, since both scale as 1/R^2.", "direction": "Absolute pressure on thick rows still needs an inner mould line.", "effect": "Owner statement stands."} | [rpt-mainline007b-check-lead4f19-1019](ef98a0f4f10c64ba-NFI.json) |

<a id="R002"></a>
### R002 — ISA case is a standard dry column, not a site or day

**Original030 unknown:** Dry constant-g geopotential formula used with geometric height substituted; no humidity case; density and pressure drive float margin and every safety factor.

**Original030 today:** N2 0.78084; O2 0.20946 (not in case) [MAINLINE-024]; 500 m ISA point matches pinned case within 0.1 Pa [MAINLINE-010]

**Original030 needed:** Include composition in the case [MAINLINE-024]; a measured column once a site is named [MAINLINE-010]; Pin an ISO 2533 or ICAO Doc 7488 table at 500 m plus a humidity case. [rpt-mainline-grok-estimates-card-1019]; Keep the 500 m case as the basis. [rpt-mainline-grok-estimates-card-1019]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N099 | NFI-AIR-FRACTIONS | 030 retained | Dry-air mole fractions 0.20946 and 0.78084 are not in the vacuum case. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N146 | NFI-010-ISA | 030 retained | {"NFI_id": "NFI-010-ISA", "gap": "ISA is a standard column, not weather. The 500 m point matches the pinned case within 0.1 Pa; other altitudes are the same formula, QUESTIONABLE.", "direction": "Fly a measured column when a site is named.", "effect": "Lever 2 numbers move with the real lapse and pressure."} | [rpt-ref-58b2bed18db2449100f2](21991360c704a696-NFI.json) |
| N242 | NFI-ISA | 030 retained | {"NFI_id": "NFI-ISA", "linked_inputs_or_points": "common atmosphere", "questionable_assumption_or_gap": "Dry constant-g geopotential formula; geometric height substituted.", "direction_of_further_investigation": "Pin ISO 2533 or ICAO Doc 7488 table at 500 m and a humidity case.", "how_it_affects_margin_or_SF": "Density moves float margin. Pressure moves every SF inversely."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |
| N252 | NFI-CHARTER | 030 retained | {"NFI_id": "NFI-CHARTER", "linked_inputs_or_points": "sensitivity only", "questionable_assumption_or_gap": "Charter density and sea-level survival belong to the historical note.", "direction_of_further_investigation": "Do not let them replace the 500 m case.", "how_it_affects_margin_or_SF": "Shown only as labelled sensitivities."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |

## T02 — Shell knockdown kd

<a id="R003"></a>
### R003 — buckling SF is linear in kd only at fixed geometry

**Original030 unknown:** The claim that local needs are independent of kd holds only at fixed geometry; re-optimising for a new kd changes thicknesses and local needs.

**Original030 today:** kd = 0.2 [MAINLINE-005]; 0.2 (0.90 optimistic carry) [MAINLINE-006]

**Original030 needed:** Qualify the statement as fixed-geometry; rebuild the design if kd changes [CHECK-MAINLINE-013]; kd from the 004 named knockdown curve; multiply each E by 0.2/kd [MAINLINE-005]; MAINLINE-004 filed values [MAINLINE-008]; Multiply buckling SF by kd/0.2 when another knockdown is adopted. [CHECK-MAINLINE-006]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N009 | NFI-CHECK013-KD-CONDITION | 030 retained | {"id": "NFI-CHECK013-KD-CONDITION", "kind": "clarification", "row": "CARD.md needs paragraph / RESULTS.json kd_scaling", "field": "independence of local needs from kd", "card_value": "Crush, crimp, wrinkling needs and face stress independent of kd; Q h_eq scales inversely with kd.", "checker_value": "Local equations have no explicit kd at fixed geometry. Reoptimising Q changes tf, tc, stress and local needs.", "example_at_rho_1": {"0.1": {"h_m": 0.378140402372981, "face_stress_Pa": 396250728.3544923, "EcGc_req_foam_design_Pa2": 2.026414217431143e+16, "Gc_req_crimp_Pa": 1260230.2477890702}, "0.2": {"h_m": 0.1890702011864905, "face_stress_Pa": 374476671.6434306, "EcGc_req_foam_design_Pa2": 1.710378811012676e+16, "Gc_req_crimp_Pa": 2515972.0959315384}, "0.4": {"h_m": 0.09453510059324526, "face_stress_Pa": 364463013.9183118, "EcGc_req_foam_design_Pa2": 1.5768064581253444e+16, "Gc_req_crimp_Pa": 5013990.593276669}}, "proposed_fix": "Qualify the scaling statement by fixed geometry. Rebuild Q if kd changes.", "nonblocking": true, "halts_owner": false, "halts_next_card": false} | [rpt-1228-mainline013-independent-check-1020](ef406b56c4cff82e-NFI.json) |
| N122 | NFI-005-KD | 030 retained | {"NFI_id": "NFI-005-KD", "gap": "All buckling requirements use kd = 0.2 and scale as 1/kd. MAINLINE-004's named knockdown curve is still running.", "direction": "Multiply each E requirement by 0.2/kd when 004 lands; no other number changes.", "effect": "A larger knockdown factor lowers every required E in this card."} | [rpt-ref-eb07faa637b7487d6dc5](c108cdbb9f3bcf68-NFI.json) |
| N137 | NFI-008-KD | 030 retained | All buckling SFs inherit kd=0.2; required E scales as 1/kd (Una's 003 correction), so every SF_b scales linearly with kd/0.2. | [rpt-ref-45da79edf548b064b228](6284193a78be0578-NFI.json) |
| N285 | NFI-KD-020 | 030 retained | {"NFI_id": "NFI-KD-020", "gap": "Confirmed: buckling uses kd 0.2 from MAINLINE-002 and scales linearly with kd. Yield does not move with kd.", "direction": "Multiply buckling SF by kd/0.2 when a later card adopts another knockdown.", "effect": "Owner statement stands."} | [rpt-mainline006-check-lead4f19-1019](8060138631058409-NFI.json) |
| N289 | NFI-KD-020 | 030 retained | {"NFI_id": "NFI-KD-020", "gap": "Buckling uses kd 0.2 from MAINLINE-002. MAINLINE-004b carries 0.90 as a QUESTIONABLE optimistic factor. Buckling SF on this card scales linearly with kd.", "direction": "Multiply buckling SF by kd/0.2 when a later card adopts another knockdown.", "effect": "Yield SF does not move with kd."} | [rpt-mainline006-grok-float-margin-1019](c433e7ad1bc469c3-NFI.json) |
| N297 | NFI-KD | 030 retained | {"NFI_id": "NFI-KD", "gap": "Confirmed: kd stays 0.2. Buckling pressure and SF scale with kd; the modulus factor scales as 1/kd; yield, membrane, crimp, wrinkling product and crush do not move with kd.", "direction": "MAINLINE-004 is one multiplication.", "effect": "Owner statement stands."} | [rpt-mainline007-check-lead4f19-1019](a27128f0dc1713bc-NFI.json) |
| N318 | NFI-KD-020 | 030 retained | {"NFI_id": "NFI-KD-020", "gap": "Buckling uses kd 0.2. The 004b optimistic carry is 0.90. Buckling SF scales linearly with kd.", "direction": "Multiply buckling SF by kd/0.2 if a later card adopts the carry.", "effect": "Yield SF does not move with kd."} | [rpt-mainline012-grok-equal-margin-1019](811b275dbd0d54b1-NFI.json) |
| N388 | NFI-015B-KD-UNCHANGED | 030b addition | The codex check's continuous SF 1 threshold is kd 0.5183040769, with global buckling and face yield active. The mode formulas already used nu 0.33. This card changes the tolerance map only. | [rpt-ref-74e882831c201b1a953c](647d16ffad5d78ae-NFI.json) |

<a id="R004"></a>
### R004 — knockdown transfer from monocoque to sandwich sphere at R 10 m

**Original030 unknown:** The curve is monolithic clamped-cap evidence; phi equal pi and the equivalent thickness are transfers onto a complete sandwich sphere, so the buckling SF is not a validated sandwich knockdown.

**Original030 today:** conservative SP-8032 cap factor, central 0.20, optimistic 0.90 [MAINLINE-08B]; transfer t_eq = sqrt(3)(d+tf) [MAINLINE-015]; dimple 0.20, flat 0.22 (numerical, small hemispheres) [MAINLINE-04B]

**Original030 needed:** a sandwich-specific knockdown for this geometry [MAINLINE-08B]; a sandwich imperfection study at this geometry [MAINLINE-015]; A sandwich knockdown test or formula at these proportions. [MAINLINE-004]; A sandwich source at these proportions. [MAINLINE-04B]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N143 | NFI-008B-KD-TRANSFER | 030 retained | The conservative SP-8032 factor is a monocoque cap curve transferred to the sandwich (phi = pi, t_eq = (6 tf d^2)^(1/3)); the central 0.20 is monocoque dome evidence; the 0.90 carry is from shells at lambda 1.58-33.18 while this sphere sits near lambda 65-68. | [rpt-ref-cc9cef5e55adca018a8f](cbad32790fc5fde1-NFI.json) |
| N177 | NFI-015-SANDWICH-TRANSFER | 030 retained | Every kd curve used here is a monocoque result transferred through t_eq = sqrt(3)(d+tf). No sandwich kd-versus-amplitude measurement was retrieved at this radius. The mapping preserves the radius of gyration by construction. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N272 | NFI-TRANSFER | 030 retained | {"NFI_id": "NFI-TRANSFER", "gap": "The curve is monolithic clamped-cap evidence. Phi equals pi and the equivalent thickness are transfers onto a complete sandwich sphere.", "direction": "A sandwich knockdown test or formula at these proportions.", "effect": "The stated buckling safety factor is not a validated sandwich knockdown."} | [rpt-mainline004-grok-knockdown-card-1019](e0152663a63bcf24-NFI.json) |
| N279 | NFI-TRANSFER | 030 retained | {"NFI_id": "NFI-TRANSFER", "gap": "SP-8032, the Wagner 2020 elastic statement, and the Krenzke upper are monocoque or dome evidence. They are transferred onto a complete sandwich sphere with phi equal to pi and t_eq = (6*tf*d^2)^(1/3).", "direction": "Keep the transfer tagged QUESTIONABLE until a sandwich source at these proportions exists.", "effect": "The buckling safety factors are not validated sandwich knockdowns."} | [rpt-mainline004b-grok-kd-range-1019](f528292663aa7701-NFI.json) |
| N280 | NFI-SANDWICH | 030 retained | {"NFI_id": "NFI-SANDWICH", "gap": "The sourced foam-core factors are Sim et al. 2024: dimple 0.20 and flat 0.22, from numerical postbuckling of small-scale hemispheres. They do not support 0.90. The paper says NASA SP-8032 at 0.18 and NASA CR-1457 at 0.20 may not provide a suitable knockdown for hemispherical foam-core shells. Their 0.18 is not this card's SP-8032 row.", "direction": "A sandwich knockdown at R = 10 m.", "effect": "Using 0.22 instead of 0.90 would raise required modulus by 0.90/0.22."} | [rpt-mainline004b-grok-kd-range-1019](f528292663aa7701-NFI.json) |
| N520 | NFI-035-TRANSFER | 030b addition | Cylinder-to-sphere transfer of a sandwich knockdown has no test behind it. The handbook monocoque ratio at the leads' R/t_eq is 0.30-0.34 (SP-8032/SP-8007), and CR-1457 makes the same split for sandwich (0.20 hemispheres against 0.32-0.36 cylinders). | [rpt-mainline035-opus-knockdown-tests-1020](4099579f3f8b5d1d-NFI.json) |

<a id="R005"></a>
### R005 — monocoque sphere knockdown kd: value and range (SP-8032 curve, 0.14 to 0.9)

**Original030 unknown:** gamma_d is 0.20 on the moderate branch; 0.90 is not a handbook value but the precision direction; 0.1407 conservative. Separation of face-modulus knockdown from core-shear flexibility is untested.

**Original030 today:** kd = 0.2 [MAINLINE-007]; kd 0.2 main; 0.1407 conservative; 0.9 optimistic [MAINLINE-009]; gamma_d 0.2 main; 0.1407 conservative; 0.9 optimistic [MAINLINE-009]; 0.14 + 3.2/lambda^2 form (text reproduction) [MAINLINE-004]

**Original030 needed:** Knockdown curve from the owning card [MAINLINE-007]; Knockdown tests on sandwich spheres at lambda near 66 [MAINLINE-009]; Tests separating face-modulus knockdown from core-shear flexibility on a complete sphere [MAINLINE-009]; Evaluate NASA SP-8032 at the complete-sphere geometry. [rpt-mainline-grok-estimates-card-1019]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N034 | NFI-KD | 030 retained | {"NFI_id": "NFI-KD", "gap": "Knockdown remains 0.2. MAINLINE-004 owns the curve.", "direction": "Multiply this card's buckling pressure and buckling safety factor by kd/0.2. Divide the modulus factor by that same ratio.", "effect": "Yield, membrane stress, crimp modulus, wrinkling product, and crush do not move with kd."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N048 | NFI-KD-PRECISION | 030 retained | {"id": "NFI-KD-PRECISION", "value": "knockdown on classical sphere buckling", "optimistic": 0.9, "optimistic_source": "Wagner 2020 Table 3, Krenzke and Kiernan, reliable upper, outside this lambda. MAINLINE-004b.", "main_point": 0.2, "main_source": "Inside the sandwich data. Sim 2024 foam-core 0.20 to 0.22. Wagner 2020 central about 0.2.", "conservative": 0.1407, "conservative_source": "CARD-009 names SP-8032's 0.1407. MAINLINE-004b P2-E sealed value is 0.140725695373. Its own optimism ratio against that sealed value is near 6.4. This ledger does not replace that ratio.", "factor_precision_gap": 4.5, "factor_meaning": "0.90/0.20 = 4.5, the precision gap CARD-009 asks this ledger to carry.", "direction": "Knockdown tests on sandwich spheres at lambda near 66, the regime of these rows."} | [rpt-ref-d5b4aaa267b71d82fe25](b9cd9c3b294887e6-NFI.json) |
| N054 | NFI-HANDBOOK-GAMMA | 030 retained | On the moderate-core branch gamma_d is 0.20 and the handbook safety factor is Kc times the classical kd=0.20 pressure. gamma_d of 0.90 is not a handbook value. It is the MAINLINE-004b precision direction, applied only to the classical pressure. | [rpt-ref-d5b4aaa267b71d82fe25](b9cd9c3b294887e6-NFI.json) |
| N244 | NFI-KD | 030 retained | {"NFI_id": "NFI-KD", "linked_inputs_or_points": "P1 I-KD", "questionable_assumption_or_gap": "0.2 is a cited severe typical knockdown, not a curve at R/t.", "direction_of_further_investigation": "Evaluate NASA SP-8032 at this complete-sphere geometry.", "how_it_affects_margin_or_SF": "SF scales directly with the knockdown. It does not change mass."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |
| N256 | NFI-KD | 030 retained | {"NFI_id": "NFI-KD", "gap": "Knockdown remains 0.2, the cited severe typical value, not a curve at this R/t.", "direction": "Evaluate NASA SP-8032 for these complete spheres.", "effect": "Stiffness pressure of P1 and P2 scales directly with the knockdown."} | [rpt-mainline002-grok-strength-card-1019](b155c07e690eaa66-NFI.json) |
| N267 | NFI-KD | 030 retained | {"NFI_id": "NFI-KD", "gap": "Knockdown remains 0.2, the inherited severe typical value.", "direction": "Evaluate a knockdown curve at these R/t and sandwich proportions.", "effect": "Buckling pressure and the required modulus scale directly with the knockdown."} | [rpt-mainline003-grok-p2-targets-1019](2090c6e1f4ca8afb-NFI.json) |
| N271 | NFI-KD | 030 retained | {"NFI_id": "NFI-KD", "gap": "The 0.14 plus 3.2 over lambda squared form is a text reproduction of NASA SP-8032, not the monograph page. The PDF was not retrieved.", "direction": "Pin the August 1969 page that prints the curve.", "effect": "A different reading of the curve would rescale buckling pressure and required modulus by the same factor."} | [rpt-mainline004-grok-knockdown-card-1019](e0152663a63bcf24-NFI.json) |
| N277 | NFI-OPT-GAP | 030 retained | {"NFI_id": "NFI-OPT-GAP", "gap": "The carried optimistic knockdown is 0.90. The conservative knockdown is the sealed per-row SP-8032 factor near 0.1407. The ratio is about 6.4. This is the optimism that must later be grounded.", "direction": "A knockdown test or formula at this sphere's lambda, on a sandwich.", "effect": "Required face modulus at 0.90 is lower than the SP-8032 modulus by that ratio.", "per_row_optimistic_over_conservative": {"P2-A": 6.396909550113781, "P2-C": 6.393643427290846, "P2-K": 6.393879448514311, "P2-E": 6.395420520834183}} | [rpt-mainline004b-grok-kd-range-1019](f528292663aa7701-NFI.json) |
| N278 | NFI-LAMBDA | 030 retained | {"NFI_id": "NFI-LAMBDA", "gap": "No reliable row in Wagner 2020 Table 3 reaches lambda near 65-68. Krenzke's 0.11-0.90 range mixes R/t 10-212 and stiffened with unstiffened machined shells, so 0.90 may be a thick or stiffened specimen. Adam and King, reliable yes, reach 0.89 only to lambda 43.11.", "direction": "Separate the Krenzke upper by R/t and by stiffened versus unstiffened.", "effect": "The carried 0.90 is an upper end of the tabulated reliable set, not a measurement at this slenderness."} | [rpt-mainline004b-grok-kd-range-1019](f528292663aa7701-NFI.json) |
| N281 | NFI-LRSM | 030 retained | {"NFI_id": "NFI-LRSM", "gap": "Central uses the prose value 0.20. Wagner 2020 also states a numerical lower-bound knockdown of 0.21 for one deep dome, H/r about 0.5, R/t about 90, lambda about 15.7. Equation (7) was not evaluated and lambda_s was not computed. The 2018 Wagner, Huehne and Niemann threshold equation was not retrieved. The comparative-study equation rho = 5.172/lambda - 1.464 + 0.1296 was not applied; it is outside this lambda and the extract is ambiguous.", "direction": "Recover the 2018 threshold equation before using it. Do not extrapolate equation (7) without lambda_s.", "effect": "Substituting 0.21 for 0.20 would rescale required modulus by 0.20/0.21."} | [rpt-mainline004b-grok-kd-range-1019](f528292663aa7701-NFI.json) |
| N282 | NFI-CLASSICAL | 030 retained | {"NFI_id": "NFI-CLASSICAL", "gap": "Classical knockdown 1.0 is the perfect-shell bound. It is reference only.", "direction": "Do not carry 1.0 as the optimistic estimate.", "effect": "None on the carried factor."} | [rpt-mainline004b-grok-kd-range-1019](f528292663aa7701-NFI.json) |
| N322 | NFI-KD-01407 | 030 retained | 0.1407 replaces the handbook gamma 0.20 on the stiff branch only. It is the brief's single figure, not a fresh SP-8032 knockdown at the optimum thickness. | [rpt-mainline014-grok-balanced-sandwich-1019](e0fba238a74bd426-NFI.json) |
| N331 | NFI-KD-01407 | 030 retained | 0.1407 replaces handbook gamma 0.20 on the stiff branch only. It is the brief's figure, not a fresh SP-8032 knockdown. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N526 | NFI-035-SP8007-P | 030b addition | CR-1457 cites SP-8007 (Sept 1965) for a 0.90 lateral-pressure factor; the 1968 SP-8007 text read here gives 0.56 with no supporting data. | [rpt-mainline035-opus-knockdown-tests-1020](4099579f3f8b5d1d-NFI.json) |

## T03 — Crimp-branch gamma

<a id="R006"></a>
### R006 — core shear (crimp) in sandwich buckling: formula and Gc basis

**Original030 unknown:** Advisory crimp replaced by sourced equations; sourced cores stay on the moderate branch, buckling SF trimmed. A core G below about 2.45 MPa would enter crimping; none do.

**Original030 today:** advisory crimp target cleared by catalog G at 16-38 kg/m3 [MAINLINE-007]; Kc trims buckling SF to 0.864-0.991 of the MAINLINE-007 value; crimp entry below G about 2.45 MPa [MAINLINE-07B]

**Original030 needed:** Published sandwich-shell formula including transverse shear [MAINLINE-007]; Sourced crimp formula [MAINLINE-007]; A published sandwich-sphere formula that includes core shear. [rpt-mainline-grok-estimates-card-1019]; A published sandwich formula that includes shear. [MAINLINE-002]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N030 | NFI-SAND | 030 retained | {"NFI_id": "NFI-SAND", "gap": "Buckling still uses the inherited sandwich extrapolation and omits core shear from the stated safety factor.", "direction": "MAINLINE-007b replaces it with a published sandwich-shell formula that includes transverse shear.", "effect": "The stated buckling pressure can fall once shear is inside the model."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N031 | NFI-SHEAR | 030 retained | {"NFI_id": "NFI-SHEAR", "gap": "The shear target uses the advisory crimping formula p=2*Gc*d/R. It is not a measured sandwich-shell limit.", "direction": "MAINLINE-007b cites a sourced formula. Catalog G at 16 to 38 kg/m3 already clears this advisory target.", "effect": "Advisory crimp does not bind the catalog cores retrieved here. A real shear interaction might."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N041 | NFI-SHEAR | 030 retained | {"NFI_id": "NFI-SHEAR", "gap": "Advisory crimp is replaced by NASA CR-1457 equations 6.2-3 through 6.2-6. Sourced cores stay on the moderate branch. Kc trims the buckling safety factor to between 0.863720643326 and 0.991105457684 of the MAINLINE-007 value.", "direction": "A core shear modulus below about 2.45 MPa would enter the crimping branch. None of the sourced moduli do.", "effect": "P2-E with Plascore at 16 kg/m3 falls from 0.233885578993 to 0.227959198328. Yield is unchanged and still larger."} | [rpt-ref-3dd5ab5528276031581d](07d0f8e52a240650-NFI.json) |
| N245 | NFI-SAND | 030 retained | {"NFI_id": "NFI-SAND", "linked_inputs_or_points": "P2", "questionable_assumption_or_gap": "Collapse formula extrapolates the monocoque D-S identity. Shear, wrinkling and core crush are omitted.", "direction_of_further_investigation": "Replace with a published sandwich-sphere formula that includes core shear.", "how_it_affects_margin_or_SF": "Shear would lower collapse pressure. The omission is optimistic for SF."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |
| N255 | NFI-SAND | 030 retained | {"NFI_id": "NFI-SAND", "gap": "Sandwich buckling still extrapolates the monocoque identity and omits core shear, wrinkling and core crush.", "direction": "Replace with a published sandwich formula that includes shear.", "effect": "Shear would lower the stiffness pressure. The omission is optimistic for that limit."} | [rpt-mainline002-grok-strength-card-1019](b155c07e690eaa66-NFI.json) |
| N263 | NFI-SAND | 030 retained | {"NFI_id": "NFI-SAND", "gap": "Buckling still uses the inherited sandwich extrapolation and omits core shear from the stated safety factor.", "direction": "Replace with a published sandwich formula that includes shear.", "effect": "The stated buckling pressure can fall once shear is inside the model."} | [rpt-mainline003-grok-p2-targets-1019](2090c6e1f4ca8afb-NFI.json) |
| N264 | NFI-SHEAR | 030 retained | {"NFI_id": "NFI-SHEAR", "gap": "The shear target uses the advisory crimping formula p=2*Gc*d/R. It is not a measured core modulus.", "direction": "Pin a core datasheet and a sourced sandwich shear formula.", "effect": "The required Gc scales with external pressure and inversely with d."} | [rpt-mainline003-grok-p2-targets-1019](2090c6e1f4ca8afb-NFI.json) |
| N275 | NFI-SAND | 030 retained | {"NFI_id": "NFI-SAND", "gap": "Classical pressure remains the inherited sandwich extrapolation.", "direction": "A published sandwich formula with shear.", "effect": "Required modulus would move if the classical pressure moved."} | [rpt-mainline004-grok-knockdown-card-1019](e0152663a63bcf24-NFI.json) |
| N288 | NFI-SHEAR | 030 retained | {"NFI_id": "NFI-SHEAR", "gap": "Confirmed: sandwich buckling omits core shear and uses the 002 formula.", "direction": "A sandwich formula with shear (007b supplies one for its rows).", "effect": "Buckling SF would move if the pressure formula moved."} | [rpt-mainline006-check-lead4f19-1019](8060138631058409-NFI.json) |
| N292 | NFI-SHEAR | 030 retained | {"NFI_id": "NFI-SHEAR", "gap": "Sandwich buckling omits core shear. The 002 formula is used.", "direction": "A sandwich formula with shear.", "effect": "Buckling SF would move if the pressure formula moved."} | [rpt-mainline006-grok-float-margin-1019](c433e7ad1bc469c3-NFI.json) |
| N469 | NFI-015-CHECK-SHEAR-RULE | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |

<a id="R007"></a>
### R007 — gamma(Vc) for a sandwich sphere: CR-1457 step (0.20 below Vc 2, 1 above) vs 018 curves; P2 lead needs 0.468-0.595 (O1)

**Original030 unknown:** A high shear modulus leaves the crimp branch and gamma becomes the knockdown 0.20; best aluminium stiff-branch rows reach SF 0.669 and 0.642, below the HRH-10 crimp balance 0.685.

**Original030 today:** gamma 0.2 at Vc=2 [CHECK-MAINLINE-09C5]; With same curve for both: Al 0.847 vs aramid 0.609 (optimistic line) [CHECK-019]; gamma_d 0.20 on moderate branch [MAINLINE-07B]; step 0.2 to 1 at Vc=2 vs 0.2+0.4*min(Vc,2) [MAINLINE-027]

**Original030 needed:** gamma = 1 for Vc>=2 per cited convention [CHECK-MAINLINE-09C5]; State the equality convention when carrying the branch wording [CHECK-MAINLINE-14B]; Re-solve budgets under the same gamma curve for both families [CHECK-019]; gamma_d 1 on crimping branch (handbook) [MAINLINE-07B]

**Current030b:** 028b nominal R10 needs gamma .564164 (2.820818× .20); 033 screened R20/R30 need .400218/.368927. CHECK-035 revises S-II hemisphere graph centers to about .21–.22, +/- .01 reading uncertainty, with Vc and plastic/thermal reduction unresolved. Additional marine and foam-core experiments invalidate categorical absence claims. No compatible elastic sphere/dome datum with recoverable moderate Vc at the lead geometry was established; neither required gamma nor unprecedented imperfection control is validated.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N004 | NFI-BRANCH-EQUALITY | 030 retained | {"id": "NFI-BRANCH-EQUALITY", "type": "source_endpoint_mismatch", "row": "Vc=2, kd=.20", "field": "gamma_d", "reported": 0.2, "independent": 1.0, "source_url": "https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf", "page": "6-7", "proposed_fix": "Use gamma=1 for Vc>=2 to follow the cited convention. Neither published point lies exactly at 2.", "stops_owner": false} | [rpt-1228-mainline009c5-independent-check-1019](4662757b4d50b2d1-NFI.json) |
| N016 | NFI-BRANCH-EQUALITY | 030 retained | {"id": "NFI-BRANCH-EQUALITY", "type": "convention_clarification", "row": "Vc=2 boundary", "field": "gamma", "reported": "No scored 014b row is exactly on the boundary; owner code was not inspected.", "independent": "CR-1457 p.6-7 includes Vc=2 in weak-core region with unity knockdown.", "proposed_fix": "State equality handling explicitly when carrying 009c-5 branch wording; all current values unaffected.", "stops_owner": false} | [rpt-1228-mainline014b-independent-check-1019](5d2a8afe8b483d72-NFI.json) |
| N025 | NFI-CHK019-GAMMA-PAIRING | 030 retained | The CR-1457 step rule gives aramid (Vc 3.1-3.5) the optimistic gamma 1 and aluminium (Vc 0.5-0.6) the conservative 0.2. Applied to both families, 018's optimistic curve (PROJECTION) gives aluminium 0.847 against aramid 0.609 on the optimistic line, 0.924 against 0.650 at 5% and 0.988 against 0.685 at 0%, where aluminium is capped by Be face compression. 018's conservative curve gives 0.557 against 0.253, 0.617 against 0.270 and 0.669 against 0.284. 'Aramid leads' on every margin line rests on the mixed pairing. The budgets were not re-solved under the curves. | [rpt-check019-opus-1020](9cc8bdcb82e9b2d1-NFI.json) |
| N044 | NFI-KD | 030 retained | {"NFI_id": "NFI-KD", "gap": "gamma_d is 0.20 on the moderate branch, the handbook hemisphere value, and the same number as kd. The handbook sets gamma_d to 1 on the crimping branch, so gamma_d times Kc jumps at Vc = 2.", "direction": "MAINLINE-004 still multiplies the moderate-branch buckling pressure by kd/0.2. Do not apply that multiplication on the crimping branch.", "effect": "No sourced row reached the jump."} | [rpt-ref-3dd5ab5528276031581d](07d0f8e52a240650-NFI.json) |
| N075 | NFI-019-BRANCH | 030 retained | The inherited Vc=2 rule changes gamma from kd to 1. MAINLINE-018 owns its physical assessment. Under large reserve the aramid optimum leaves the crimp branch, invalidating constant-slope extrapolation. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N103 | NFI-027-GAMMA | 030 retained | Design uses the inherited hemispherical 0.2/1 step at Vc=2. Full 021 uses 0.2+0.4min(Vc,2). Neither is validated for this completed sphere. Constant 0.2 removes the enhanced P2 pass. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N192 | NFI-020-INHERITED-MODEL | 030 retained | Crimp-branch gamma=1, stabilised Ec in wrinkling and common nu remain unvalidated inherited assumptions.; Resolve the inherited MAINLINE-018 crimp-step and core-modulus questions using their owning evidence; this manufacturing card does not adjudicate them. | [rpt-ref-3e02218a03708a878faa](72e91c4df6df4236-NFI.json) |
| N193 | NFI-021-GAMMA | 030 retained | Under 018's conservative gamma the point is 0.338601. 015's map: one dimple of 11.8 mm (RMS 0.364 mm) at this gamma, QUESTIONABLE. | [rpt-ref-769a7442efd5a04681e9](fae865c7f039491f-NFI.json) |
| N197 | NFI-021-CRIMP-BRANCH-GAMMA | 030 retained | The aramid route floats only on the handbook's gamma 1 at Vc >= 2, which 018 tags QUESTIONABLE for a sphere. | [rpt-ref-769a7442efd5a04681e9](fae865c7f039491f-NFI.json) |
| N202 | NFI-021-CONSERVATIVE-READING | 030 retained | If 'today' is 018's conservative gamma (0.20 at every Vc), the stiff-branch least set does not change, because its today is already 0.20; a crimp-branch point needs gamma 1, a factor 5. | [rpt-ref-769a7442efd5a04681e9](fae865c7f039491f-NFI.json) |
| N203 | NFI-021b-GAMMA | 030 retained | {"id": "NFI-021b-GAMMA", "optimism": "O1", "needed": 0.46822856667720764, "today": 0.2, "full_at_point": 0.5544727352669614, "improvement_factor": 2.341142833386038, "usage": 0.83420513484806, "state": "PROJECTION", "grounding_card": "MAINLINE-018b; MAINLINE-015's map", "tolerance_015": {"kd": 0.46822856667720764, "t_eq_mm": 53.364448806653826, "R_over_t_eq": 187.39067344687226, "in_fit_range": true, "status": "lambda_I_1 inversion", "delta_over_t_eq": 0.8586135991025216, "amplitude_mm": 45.819441454003304, "rms_worst_mm": 1.7088520330420545}} | [rpt-ref-1080d4f6a1af4cfa8c67](b056cc13a604abed-NFI.json) |
| N211 | NFI-021b-ARAMID-BLOCKED | 030 retained | The aramid family reaches 0.9407 with every optimism full; core shear crimping, which no named optimism touches, ties with global and wrinkling on the crimp branch. | [rpt-ref-1080d4f6a1af4cfa8c67](b056cc13a604abed-NFI.json) |
| N241 | NFI-028-20 | 030 retained | {"id": "NFI-028-20", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Inherited shell optimisms", "today_value": "Needed gamma=0.595318 and wrinkle coefficient=0.370681 held fixed", "required_or_budget_target": {"gamma_ratio_to_0p2": 2.9765898214975905, "wrinkle_ratio_to_0p33": 1.1232748900708642}, "needed_evidence": "Independent grounding of the inherited imperfection and wrinkle model. A computed joining improvement does not close these rows.", "factor_to_216_427kg_allowance": null, "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N299 | NFI-SHEAR | 030 retained | {"NFI_id": "NFI-SHEAR", "gap": "Confirmed: sourced cores stay on the moderate branch (all Vc < 2). Kc trims buckling SF to 0.863720643326-0.991105457684 of the 007 value. P2-E/Plascore 16 falls 0.2338855789925097 to 0.22795919832772132; yield unchanged and larger.", "direction": "A core shear modulus below about 2.45 MPa would enter the crimping branch. None sourced does.", "effect": "Owner statement stands."} | [rpt-mainline007b-check-lead4f19-1019](ef98a0f4f10c64ba-NFI.json) |
| N302 | NFI-KD | 030 retained | {"NFI_id": "NFI-KD", "gap": "Confirmed: gamma_d = 0.20 on the moderate branch, equal to kd, with a handbook jump to 1 at Vc=2 that no sourced row reaches. Do not apply the MAINLINE-004 kd/0.2 multiplication on the crimping branch.", "direction": "Owner direction stands.", "effect": "No sourced row reached the jump."} | [rpt-mainline007b-check-lead4f19-1019](ef98a0f4f10c64ba-NFI.json) |
| N327 | NFI-HEMISPHERE | 030 retained | Handbook gamma 0.20 is the CR-1457 hemisphere value. A complete sphere has no edge. MAINLINE-007b already recorded that the 0.20 rests on meager tests. | [rpt-mainline014-grok-balanced-sandwich-1019](e0fba238a74bd426-NFI.json) |
| N344 | NFI-HEMISPHERE | 030 retained | Handbook gamma 0.20 is the CR-1457 hemisphere value. A complete sphere has no edge. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N347 | NFI-STIFF-BRANCH | 030 retained | A high shear modulus leaves the crimp branch. Gamma then becomes the knockdown 0.20, and global buckling is scored with that factor. For Be S-200F the best aluminium row is CR-III 5056 at 1.6 pcf, least SF 0.668649769509 by global buckling, below the HRH-10 crimp balance 0.685338231171. The 1/4 and 3/8 cells tie. Plascore 3/16-2.0, W shear 20 ksi and transferred Ec 34 ksi, reaches 0.641722323466 by the same mode. The higher W shear does not raise the leading safety factors. 6061-T6 does move, to 0.145930331406 on CR-III 5056 3/8-1.0. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N349 | NFI-017-GC-BRANCH | 030 retained | {"NFI_id": "NFI-017-GC-BRANCH", "gap": "Raising core Gc alone lowers Vc. Past Vc = 2 the CR-1457 branch sets gamma = kd (0.20) instead of 1, so the least SF falls (caps 0.510 CNT, 0.560 Be, 0.403 graphene at a 1e4 multiplier in my scan). The governing mode's own property is not a direction alone.", "direction": "Any Gc direction must be paired with a knockdown direction, which has no sourced value above 0.20 today.", "effect": "Gc is listed as not alone on all three P2 leaders."} | [rpt-mainline017-improvement-directions-lead4f19-1019](9f3c760a855408f0-NFI.json) |
| N424 | NFI-028b-af015_scarf-gamma | 030b addition | Ground gamma at the actual jointed geometry, including imperfections. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N426 | NFI-028b-af015_scarf_primer5-gamma | 030b addition | Ground gamma at the actual jointed geometry, including imperfections. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N428 | NFI-028b-lab8_eb_eta1-gamma | 030b addition | Ground gamma at the actual jointed geometry, including imperfections. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N430 | NFI-028b-lab8_scarf-gamma | 030b addition | Ground gamma at the actual jointed geometry, including imperfections. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N489 | NFI-031-P2-GAMMA | 030b addition | The hemisphere-derived 0.2/1 branch rule and 018 interpolation to 0.2+0.4min(Vc,2) have not been validated for the complete sphere. Numerical least-set membership is conditional on these bounds. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N518 | NFI-035-SPHERE-VC | 030b addition | The only measured sandwich hemispheres (Saturn S-II, two points, gamma 0.22-0.24 at R/rho about 240) have no recoverable Vc; Gonzalez and Patton's SDL 468, which holds the specimens, was not found. The only sphere data cannot be placed on the Vc axis. | [rpt-mainline035-opus-knockdown-tests-1020](4099579f3f8b5d1d-NFI.json) |
| N519 | NFI-035-VC-GAP | 030b addition | No measured point at Vc 0.9 to 2 in any shell form. 018's linear rise from 0.2 to 1 across Vc 0 to 2 is untested there; the SBKF cylinders at Vc 0.3-0.5 already sit above it (0.72-0.87), but as cylinders. | [rpt-mainline035-opus-knockdown-tests-1020](4099579f3f8b5d1d-NFI.json) |
| N521 | NFI-035-SBKF-VC | 030b addition | SBKF Vc comes from lamination theory on stated lamina values with a generic G12 of 0.77 Msi and geometric-mean face and core conventions (range shown as bars: axial-face/axial-shear to softer-core). QUESTIONABLE. | [rpt-mainline035-opus-knockdown-tests-1020](4099579f3f8b5d1d-NFI.json) |
| N547 | NFI-036-gamma-wrinkle | 030b addition | Retain the unresolved buckling and wrinkling assumptions after adding strength. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N556 | 033-NFI-04 | 030b addition | Gamma/Q transfers and branch convention; Gamma's smooth full curve and Q=.82 are projected model transfers. The 021b baseline sets gamma=1 in the Vc>=2 crimp branch. Thus Q-plus-strength's 16.282 m crossing does not establish flotation at literal gamma=.20. The requested flat-.20 benchmark is separately negative at every radius. | [rpt-ref-5b1ba7a48fcb57c8e35e](a4edee0295bc38f3-NFI.json) |
| N600 | NFI-017b-VC2-STEP | 030b addition | Face modulus alone reaches SF 1 only at Vc 2, where CR-1457's gamma steps from 0.20 to 1; the point is a knife edge that re-optimisation cannot hold (the crimp-branch answers re-check at 0.756/0.789).; MAINLINE-029's measured crimp-branch gamma at the lead geometry. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| N657 | NFI-038-GAMMA_DENOM | 030b addition | Gamma denominators differ across models and shorthand | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N673 | NFI-C035-SII | 030b addition | S-II core properties, actual geometry, plasticity and thermal reductions are unresolved. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N674 | NFI-C035-BASELINE | 030b addition | Anisotropic/combined-load SBKF FE ratios are not proven to share the lead sphere's scalar denominator. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N675 | NFI-C035-SCALAR | 030b addition | Vc depends on scalarization, nominal versus measured thickness and stress-dependent properties. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N681 | NFI-C035-YANG | 030b addition | The new egg-shaped vessel has plastic collapse and no compatible scalar Vc established. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N686 | NFI-C035-MUC | 030b addition | Muc's 8.49% eigenvalue overprediction is supported, but an effective measured core-shear Vc is not. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N698 | NFI-036-gamma-wrinkle | 030b addition | Retain the unresolved buckling and wrinkling assumptions after adding strength. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |

## T04 — Wrinkling and core Ec

<a id="R008"></a>
### R008 — core Ec (stabilised datasheet value) transferred into the wrinkling formula

**Original030 unknown:** Plascore PAMG-XR1 5052 prints no stabilised compressive modulus and no crush column; Ec is transferred from Hexcel CR-III 5052; crush is Plascore bare, not the Hexcel crush-column test.

**Original030 today:** catalog cores miss product by about 40-180x [MAINLINE-007]; Hexcel wrinkling SF 0.0565 and 0.0415 [MAINLINE-07B]; coefficient 0.5 on cube root of E_f*Ec*Gc [MAINLINE-08B]; catalog cores 16-38 kg/m3 clear advisory crush and crimp [CHECK-MAINLINE-007]

**Original030 needed:** Sourced wrinkling formula keeping Ec and Gc separate; aluminium honeycomb Ec [MAINLINE-007]; Sourced honeycomb Ec [MAINLINE-07B]; 007b sourced sandwich-shell shear and wrinkling formulas [MAINLINE-08B]; Separate Ec and Gc from a datasheet. [MAINLINE-003]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N032 | NFI-WRINKLE | 030 retained | {"NFI_id": "NFI-WRINKLE", "gap": "The wrinkling target uses the advisory one-half cube-root formula. The equal Ec and Gc square root is not used as a result.", "direction": "MAINLINE-007b cites a sourced wrinkling formula and keeps Ec and Gc separate.", "effect": "Catalog foams and aramid honeycomb miss this product by about 40 to 180 times. Aluminium honeycomb has no retrieved Ec, so its product is open."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N042 | NFI-WRINKLE | 030 retained | {"NFI_id": "NFI-WRINKLE", "gap": "Foam wrinkling uses equation 2.2-5 with Q 0.50 and the flat-plate equibiaxial interaction 2.2-6. The stress safety factor becomes 0.709062069568 of the advisory uniaxial stress factor. Honeycomb uses equation 2.2-14.", "direction": "Plascore has no Ec, so its wrinkling stress is still open. The Hexcel stabilised modulus is QUESTIONABLE as Ec.", "effect": "Foam wrinkling stays above the trimmed general-instability factor. Hexcel equibiaxial wrinkling safety factors are 0.0565286364026 and 0.0415196459641, below general instability, so that local mode would govern if it is admitted."} | [rpt-ref-3dd5ab5528276031581d](07d0f8e52a240650-NFI.json) |
| N139 | NFI-008B-WRINKLE-FORMULA | 030 retained | The wrinkling criterion sigma_wr = 0.5*(E_f*Ec*Gc)^(1/3) is the flat-panel/dimple formula transferred to a 10 m radius sandwich sphere. Orthotropic honeycomb has no single continuum Ec; the two HexWeb sheets carry no compressive modulus on their datasheets, so their Ec*Gc products stay open (007). Foam products (ROHACELL, Divinycell) are datasheet-derived and QUESTIONABLE. | [rpt-ref-cc9cef5e55adca018a8f](cbad32790fc5fde1-NFI.json) |
| N265 | NFI-WRINKLE | 030 retained | {"NFI_id": "NFI-WRINKLE", "gap": "The wrinkling target uses the advisory one-half cube-root formula and an equal Ec and Gc split.", "direction": "Separate Ec and Gc from a datasheet.", "effect": "The reported product is the quantity fixed by the formula. The square root is only the equal-split assumption."} | [rpt-mainline003-grok-p2-targets-1019](2090c6e1f4ca8afb-NFI.json) |
| N296 | NFI-SAND/SHEAR/WRINKLE/CRUSH | 030 retained | {"NFI_id": "NFI-SAND/SHEAR/WRINKLE/CRUSH", "gap": "Confirmed: stated SF omits core shear, face wrinkling and core crush; advisory crimp (Gc = pR/(2*sep)), wrinkling product ((2*membrane)^3/E) and crush (p/2, QUESTIONABLE, not an equilibrium solution) are beside the row. Catalog cores at 16-38 kg/m3 clear advisory crush and crimp; wrinkling products miss by roughly 40-180x; aluminium honeycomb Ec is open.", "direction": "007b, checked separately.", "effect": "Owner statement stands."} | [rpt-mainline007-check-lead4f19-1019](a27128f0dc1713bc-NFI.json) |
| N325 | NFI-ALHC | 030 retained | Both Plascore aluminium honeycombs lack Ec. Wrinkling is unscored, so they are excluded from the optimum. | [rpt-mainline014-grok-balanced-sandwich-1019](e0fba238a74bd426-NFI.json) |
| N336 | NFI-PLASCORE-EC | 030 retained | Plascore PAMG-XR1 5052 prints bare compression and L/W plate shear. It prints no stabilised compressive modulus and no crush column. Ec is the Hexcel CR-III 5052 stabilised modulus at the same cell and nominal pcf. Crush is Plascore's bare compressive typical, which is the 1.29 MPa the brief names at 3/16-2.0. That bare value is not the Hexcel crush-column test. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N339 | NFI-HRH36 | 030 retained | HRH-36 para-aramid in the attributes brochure has no stabilised compressive modulus. It is not scored. HDC has strengths only. HFT 3/8-4.0 has no stabilised modulus. Preliminary and beam-shear rows were not scored. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N608 | NFI-017b-CORE-EC | 030b addition | With beryllium and handbook values kept, the core needs through-thickness stiffness per density of 41-57 MPa per kg/m3, beyond aluminium's 24.8; no carbon-honeycomb compressive modulus was sourced, and the Ultracor shear value is secondary (a 2023 paper quoting 2012).; A primary carbon-honeycomb datasheet with stabilised compressive modulus. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |

<a id="R009"></a>
### R009 — equibiaxial wrinkling interaction factor (0.682) on a curved face

**Original030 unknown:** The flat-plate interaction is applied to equibiaxial membrane stress of a sphere; a sphere-specific interaction could replace it.

**Original030 today:** equibiaxial factor 0.6823 (from R^3+R=1) [MAINLINE-07B]; equibiaxial factor 0.6823, already inside the stated SF [MAINLINE-009]; 0.6823278038280193 [CHECK-MAINLINE-07B]

**Original030 needed:** Sphere-specific wrinkling interaction [MAINLINE-07B]; Sphere-face wrinkling test [MAINLINE-009]; A sphere-specific wrinkling interaction. [CHECK-MAINLINE-07B]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N047 | NFI-BIAX | 030 retained | {"NFI_id": "NFI-BIAX", "gap": "Equation 2.2-6 is a flat-plate interaction applied here to equibiaxial membrane stress. The handbook cites it for biaxial compression of facings.", "direction": "A sphere-specific wrinkling interaction could replace it.", "effect": "The equibiaxial factor solved from R^3 + R = 1 is 0.682327803828."} | [rpt-ref-3dd5ab5528276031581d](07d0f8e52a240650-NFI.json) |
| N055 | NFI-WRINKLE-BIAX | 030 retained | {"id": "NFI-WRINKLE-BIAX", "value": "equibiaxial factor on the flat-plate interaction Rx^3+Ry=1", "optimistic": 0.23516798404427022, "factor_formula": "constant 0.682327803828, already inside the stated wrinkling safety factor", "conservative": "the same interaction", "direction": "A sphere-face wrinkling test. The interaction is a flat-plate equation."} | [rpt-ref-d5b4aaa267b71d82fe25](b9cd9c3b294887e6-NFI.json) |
| N305 | NFI-BIAX | 030 retained | {"NFI_id": "NFI-BIAX", "gap": "Confirmed: Eq 2.2-6 is a flat-plate interaction applied to equibiaxial membrane stress; the solved factor is 0.6823278038280193.", "direction": "A sphere-specific wrinkling interaction could replace it.", "effect": "Owner statement stands."} | [rpt-mainline007b-check-lead4f19-1019](ef98a0f4f10c64ba-NFI.json) |
| N451 | biaxial-on-a-shell | 030b addition | Equation 2.2-15 is recommended for biaxial compression. The foam section bases its interaction on flat plates of large aspect ratio. The honeycomb page does not show a biaxial waviness test. The hull radius is 10 m. | [rpt-mainline032-grok-wrinkle-waviness-1020](df2ac0989ca4f688-NFI.json) |
| N534 | NFI-032-CHECK-BIAXIAL-TRANSFER | 030b addition | non_blocking | [rpt-ref-a30a669ed3e245f1473b](f4fb2c3464ed42c3-NFI.json) |
| N631 | NFI-032-CHECK-BIAXIAL-TRANSFER | 030b addition | non_blocking | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N654 | NFI-038-BAXIAL | 030b addition | Uniaxial tests may censor the required wrinkle evidence | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |

<a id="R010"></a>
### R010 — honeycomb wrinkling coefficient 0.33 (design) vs 0.82 (theoretical) (O2)

**Original030 unknown:** Foam wrinkling gives 0.709 of advisory uniaxial SF; Hexcel honeycomb wrinkling (0.0565, 0.0415) falls below general instability and would govern if admitted; Plascore Ec open, Hexcel stabilised Ec questionable.

**Original030 today:** design coefficients 0.50 and 0.33; classical 0.76 and 0.82 [MAINLINE-013]; coefficient 0.33 (design lower bound) [MAINLINE-021]; coefficient 0.33 (classical 0.82) [MAINLINE-21B]; foam factor 0.6823278 (Q 0.50) [CHECK-MAINLINE-07B]

**Original030 needed:** Correct the sentence [CHECK-MAINLINE-14B]; a representative wrinkling test fixing the coefficient for the chosen face and core [MAINLINE-013]; coefficient 0.3707; a wrinkling test on a representative sandwich [MAINLINE-021]; coefficient 0.6092 [MAINLINE-21B]

**Current030b:** 028b nominal R10 needs Q=.434628 (1.317054× .33). 033 screened R20/R30 need .517583/.539762. 032's checked inverse relates these to a wavelength-specific amplitude conditional on the weaker of core/bond flatwise capacities; 032b's aluminium precedents are not Be-hull qualification.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N014 | NFI-WRINKLE-GC-TEXT | 030 retained | {"id": "NFI-WRINKLE-GC-TEXT", "type": "text_mismatch", "row": "NFI-W-SHEAR", "field": "note", "reported": "Crimping and honeycomb wrinkling use that Gc.", "independent": "The selected honeycomb wrinkling equation has no Gc; crimping and global buckling do.", "proposed_fix": "Correct the explanatory sentence; numerical values already use the stated honeycomb formula.", "stops_owner": false} | [rpt-1228-mainline014b-independent-check-1019](5d2a8afe8b483d72-NFI.json) |
| N167 | NFI-013-WRINKLE-LEVEL | 030 retained | The wrinkling-precision gap, carried as 009 and 014 carry it: design coefficients (continuum 0.50, CR-1457 eq 2.2-5; honeycomb 0.33, eq 2.2-14) against classical ones (0.76, NASA/CR-1999-208994 Table 3; 0.82, eq 2.2-12). | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N194 | NFI-021-WRINKLE | 030 retained | core-to-face ratio tc/tf 23.97 | [rpt-ref-769a7442efd5a04681e9](fae865c7f039491f-NFI.json) |
| N204 | NFI-021b-WRINKLE | 030 retained | {"id": "NFI-021b-WRINKLE", "optimism": "O2", "needed": 0.6092014443376216, "today": 0.33, "full": 0.82, "improvement_factor": 1.8460649828412774, "usage": 0.6735316047895863, "state": "between the design lower bound and the classical value; no test at this tc/tf", "grounding_card": "none pending"} | [rpt-ref-1080d4f6a1af4cfa8c67](b056cc13a604abed-NFI.json) |
| N300 | NFI-WRINKLE | 030 retained | {"NFI_id": "NFI-WRINKLE", "gap": "Confirmed: foam wrinkling (Eq 2.2-5, Q 0.50, equibiaxial factor 0.6823278038280193 from x^3+x=1) gives 0.7090620695678252 of the advisory uniaxial SF and stays above trimmed general instability. Hexcel honeycomb wrinkling (Eq 2.2-14) gives 0.05652863640260287 and 0.0415196459641, below general instability, so it would govern if admitted. Plascore Ec is open; Hexcel stabilised Ec is QUESTIONABLE.", "direction": "Owner directions stand.", "effect": "Owner statement stands."} | [rpt-mainline007b-check-lead4f19-1019](ef98a0f4f10c64ba-NFI.json) |
| N329 | NFI-WRINKLE-Q | 030 retained | Wrinkling-precision gap. Foam design coefficient 0.50, theoretical column 0.82 inside the sourced band Allen 0.78, Plantema 0.85, Hoff and Mautner 0.91. Required Ec*Gc scales as 1/coefficient^3: (0.82/0.50)^3 = 4.410943999999999. Honeycomb design coefficient 0.33 from CR-1457 eq 2.2-14. Honeycomb theoretical coefficient 0.82 from Hemp, as quoted for anti-plane cores in NASA/CR-1999-208994. QUESTIONABLE. The column is the same geometry, not a new optimum. | [rpt-mainline014-grok-balanced-sandwich-1019](e0fba238a74bd426-NFI.json) |
| N343 | NFI-WRINKLE-Q | 030 retained | Honeycomb design coefficient 0.33 is CR-1457 eq 2.2-14. Theoretical 0.82 is Hemp's symmetric anti-plane value, quoted as purely theoretical for honeycomb in NASA/CR-1999-208994. Foam design 0.50 and theoretical 0.82 are the 014 column, kept for the foam cores that remain in the set. The theoretical column is the same geometry, not a new grid. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N351 | NFI-017-WRINKLE-COEFF | 030 retained | {"NFI_id": "NFI-017-WRINKLE-COEFF", "gap": "The CNT wrinkling-coefficient requirement (0.600) lies inside the sourced theoretical band 0.78-0.91, above the design 0.33. It is a coefficient the card is scored with, not a measured property of this sphere.", "direction": "A sphere-specific wrinkling test or interaction to replace the flat-plate equibiaxial factor.", "effect": "First direction by availability, seventh by factor."} | [rpt-mainline017-improvement-directions-lead4f19-1019](9f3c760a855408f0-NFI.json) |
| N425 | NFI-028b-af015_scarf-wrinkle | 030b addition | Ground wrinkling coefficient with the actual core and bond. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N427 | NFI-028b-af015_scarf_primer5-wrinkle | 030b addition | Ground wrinkling coefficient with the actual core and bond. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N429 | NFI-028b-lab8_eb_eta1-wrinkle | 030b addition | Ground wrinkling coefficient with the actual core and bond. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N431 | NFI-028b-lab8_scarf-wrinkle | 030b addition | Ground wrinkling coefficient with the actual core and bond. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N446 | fc-is-the-lower-of-three | 030b addition | Fc is the lower of flatwise compression, flatwise tension and the face-to-core bond. The sheet prints stabilised compression, 60 psi typical and 35 psi minimum. It does not print flatwise tension or a beryllium bond. A weaker bond lowers the allowed amplitude in proportion. The crush column, 35 psi, is not that peak. | [rpt-mainline032-grok-wrinkle-waviness-1020](df2ac0989ca4f688-NFI.json) |
| N452 | design-0-33-is-not-a-measured-wave | 030b addition | Inverting equation 2.2-12 at Q 0.33 is stored so the design value can be seen as an amplitude. The handbook selected 0.33 from a test plot. | [rpt-mainline032-grok-wrinkle-waviness-1020](df2ac0989ca4f688-NFI.json) |
| N490 | NFI-031-WRINKLE-CORE | 030b addition | Wrinkle coefficients between 0.33 and 0.82 and published typical core properties are used for a curved sandwich. The catalogue includes transferred moduli and scaled cores; the winner is the sourced light 5056 core, but no assembly allowable exists. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N528 | NFI-032-CHECK-FC | 030b addition | non_blocking | [rpt-ref-a30a669ed3e245f1473b](f4fb2c3464ed42c3-NFI.json) |
| N535 | NFI-032-CHECK-DESIGN033 | 030b addition | non_blocking | [rpt-ref-a30a669ed3e245f1473b](f4fb2c3464ed42c3-NFI.json) |
| N537 | NFI-032-CHECK-ROUNDED-TARGET | 030b addition | non_blocking | [rpt-ref-a30a669ed3e245f1473b](f4fb2c3464ed42c3-NFI.json) |
| N632 | NFI-032-CHECK-DESIGN033 | 030b addition | non_blocking | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |

<a id="R011"></a>
### R011 — intracell dimpling: biaxial vs uniaxial rule and coefficient

**Original030 unknown:** Intracell dimpling uses the brief stress 2*E_f/(1-nu^2)*(tf/s_cell)^2 with nominal cell size, no equibiaxial factor; foam is not dimpled; the coefficient 2 is the brief expression.

**Original030 today:** dimpling margin 9.019 biaxial vs 18.04 uniaxial [MAINLINE-021]; coefficient 2 (brief expression) [MAINLINE-14B]

**Original030 needed:** none [MAINLINE-021]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N200 | NFI-021-DIMPLING-FORM | 030 retained | Dimpling here uses CR-1457 eq 2.1-6 (biaxial, half); 009d and 014b use the uniaxial eq 2.1-4. | [rpt-ref-769a7442efd5a04681e9](fae865c7f039491f-NFI.json) |
| N342 | NFI-DIMPLE | 030 retained | Intracell dimpling uses the brief's stress 2*E_f/(1-nu^2)*(tf/s_cell)^2, divided by the same membrane stress as wrinkling. No equibiaxial factor is applied. Cell size is the sheet nominal. Foam is not dimpled. The coefficient 2 is the brief's expression. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N659 | NFI-038-CELL_SCALE | 030b addition | Stock honeycomb cells do not scale with a miniature shell | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |

<a id="R012"></a>
### R012 — laminate bending stiffness in wrinkling

**Original030 unknown:** Composite faces use an inherited scalar quasi-isotropic modulus in the wrinkling formula; laminate bending stiffness (layup) is not supplied.

**Original030 today:** Scalar quasi-isotropic face modulus (value not stated) [CHECK-MAINLINE-14B]

**Original030 needed:** Layup / bending-stiffness sensitivity in a later fix card [CHECK-MAINLINE-14B]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N015 | NFI-LAMINATE-BENDING | 030 retained | {"id": "NFI-LAMINATE-BENDING", "type": "model_assumption", "row": "composite faces", "field": "wrinkling_modulus", "reported": "Inherited scalar quasi-isotropic face modulus", "independent": "Laminate bending stiffness is not supplied; NASA/CR-1999-208994 after Eq.17 calls for bending stiffness.", "source_url": "https://ntrs.nasa.gov/api/citations/19990017863/downloads/19990017863.pdf", "proposed_fix": "Retain QUESTIONABLE and supply a layup/bending-stiffness sensitivity in a later fix card.", "stops_owner": false} | [rpt-1228-mainline014b-independent-check-1019](5d2a8afe8b483d72-NFI.json) |

## T05 — Face properties

<a id="R013"></a>
### R013 — Be face compressive allowable by grade, form and source: 241 / 255 / 283 / 345 / 379 MPa (O3)

**Original030 unknown:** Face compression is exactly 1 on the SR-200 minimum tensile yield used as compressive; no compressive minimum is published, and gauge tolerance or post-form properties can take it below 1.

**Original030 today:** 283 MPa (frozen); current guide about 255 MPa [CHECK-MAINLINE-09C5]; S-200F E 290 GPa, 283 MPa; SR-200 lot 379.2 MPa, E 293.6 GPa; SR-200 tensile minimum 345 MPa [MAINLINE-027]; 283 MPa starting value; current guide about 255 MPa; SR-200 tensile minimum 345 MPa; main route needs about 283 MPa [CHECK-rpt-ref-e92af61311c9bf4a89cd]; 379.2 MPa sheet; tube values 450 and 544 MPa [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Original030 needed:** Pin the exact older edition supporting 283 MPa and reconcile with the newer guide [CHECK-MAINLINE-09C5]; Lot-, gauge-, direction- and post-form compression, stiffness and Poisson data [MAINLINE-027]; Matched product, lot and thickness compression value [CHECK-rpt-ref-e92af61311c9bf4a89cd]; Narrow wording to the strongest applicable sheet value; any tube-to-sheet transfer is a separate PROJECTION [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Current030b:** 036/CHECK-036 find no qualified finished thin-sheet compressive minimum. All4945 independent comparisons reproduce. Current selected scarf points demand about 300.333MPa;345MPa remains tensile proxy. Historical1.96mm379.2MPa is confirmed but not a thin-sheet allowable. Reoptimized381.612–381.639MPa R20 requirements belong to older027 splice/sheet-elastic models, not033 scarf redesign.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N002 | NFI-STRENGTH-EDITION | 030 retained | {"id": "NFI-STRENGTH-EDITION", "type": "source_version_conflict", "row": "Beryllium S-200F", "field": "compressive_yield_MPa", "reported": 283, "current_guide_value_approx": 255, "source_url": "https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74", "page": 4, "proposed_fix": "Pin the exact older MB-001 edition supporting 283 MPa and reconcile the newer guide. Current computations retain the frozen strength; 37/41 sensitivity is arithmetically correct.", "stops_owner": false} | [rpt-1228-mainline009c5-independent-check-1019](4662757b4d50b2d1-NFI.json) |
| N013 | NFI-STRENGTH-EDITION | 030 retained | {"id": "NFI-STRENGTH-EDITION", "type": "source_version_conflict", "row": "Beryllium S-200F", "field": "compressive_yield_MPa", "reported": 283, "current_guide_value_approx": 255, "source_url": "https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74", "page": 4, "proposed_fix": "Pin the exact older MB-001 edition supporting 283 MPa and reconcile the newer guide. Current computations retain the frozen strength; 37/41 sensitivity is arithmetically correct.", "stops_owner": false} | [rpt-1228-mainline014b-independent-check-1019](5d2a8afe8b483d72-NFI.json) |
| N104 | NFI-027-BE-GRADE | 030 retained | S-200F E = 290 GPa and inherited compression 283 MPa are the design screen. Full 021 transfers a historical SR-200 lot's 379.2 MPa and lower in-plane E = 293.6 GPa. Current SR-200 sheet lists E = 290 GPa and tensile minimum 345 MPa, not a guaranteed compression allowable. Nu 0.33 remains inherited. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N120 | NFI-CHECK021-STRENGTH-FORM | 030 retained | Confirms and sharpens the owner's existing Be-strength/sheet-size NFI; does not stop the estimate. | [rpt-ref-e92af61311c9bf4a89cd](0b74ca6f4252ee9e-NFI.json) |
| N121 | NFI-CHECK021-STRONGEST-SCOPE | 030 retained | {"id": "NFI-CHECK021-STRONGEST-SCOPE", "category": "source-claim scope", "status": "OPEN", "row": "Strongest sourced beryllium", "field": "scope of 379.2 MPa assertion", "card_value": "379.2 MPa as strongest sourced Be", "check_value": {"supported_sheet_value_Pa": 379200000, "other_sourced_tube_values_Pa": {"type_A": 450000000, "type_PS_1.016mm_wall": 544000000}}, "source": ["https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf", "https://ntrs.nasa.gov/api/citations/19680027581/downloads/19680027581.pdf"], "location": "CR-194164 Table 3; TN D-4833 Table VIII, PDF page 35", "tag": "QUESTIONABLE lot/product-form observations", "effect": "379.2 MPa is supported for the cited sheet directions, but is not the largest compressive value in the source collection. The larger numbers are tube results, not qualified sphere faces.", "proposed_fix": "Narrow the wording to strongest applicable sheet value among the opened sheet sources. A tube-to-sheet transfer, if pursued, is a separate PROJECTION."} | [rpt-ref-e92af61311c9bf4a89cd](0b74ca6f4252ee9e-NFI.json) |
| N187 | NFI-020-GRADE-ORIENTATION-COMPRESSION | 030 retained | S200F bulk properties are not an established rolled SR200, formed and joined, biaxial compression basis.; Measure rolled-direction/transverse compression, biaxial behavior, through-thickness/peel response and post-form/post-join properties. Resolve grade, heat treatment, gauge length and guide/datasheet discrepancies. | [rpt-ref-3e02218a03708a878faa](72e91c4df6df4236-NFI.json) |
| N195 | NFI-021-BE-STRENGTH | 030 retained | The point sits at face compression 1.0002: the 283 MPa inherited from 008 cites an older guide (MB-001, 41 ksi); the current Materion guide prints 'about 37 ksi' for S-200F. | [rpt-ref-769a7442efd5a04681e9](fae865c7f039491f-NFI.json) |
| N207 | NFI-021b-FACE-AT-ONE | 030 retained | Face compression is exactly 1 on SR-200's minimum tensile yield used as compressive; no compressive minimum is published; 020's gauge tolerance ±0.1016 mm and post-form properties can take it below 1. | [rpt-ref-1080d4f6a1af4cfa8c67](b056cc13a604abed-NFI.json) |
| N240 | NFI-028-19 | 030 retained | {"id": "NFI-028-19", "status": "OPEN", "tag": "QUESTIONABLE", "technology_state": "exists_today", "hull_adoption_state": "PROJECTION", "assumption": "Parent Be properties at thin-sheet joints", "today_value": "021 retains 283 MPa compression and E=290 GPa. This is not a supplier thin-sheet/post-join allowable.", "required_or_budget_target": {"original_required_compression_Pa": 282948186.8240931, "255MPa_guide_sensitivity_capacity_ratio": 0.9012250718486905}, "needed_evidence": "Confirm actual product form, orientation, gauge, formed and post-join strength. Joining mass savings do not establish this property.", "factor_to_216_427kg_allowance": null, "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N401 | NFI-020C-GRADE-BASIS | 030b addition | The faces are bought as SR-200 sheet (sections 1-2), but every strength screen uses S-200F block values: 283 MPa inherited as 'optimistic', 241 MPa block tensile minimum, and 0.7 x 241. SR-200's own sourced minimum tensile yield is 345 MPa (S03; guide p. 8), above the card's optimistic value. | [rpt-ref-35706d7a2ae7e951590b](17d1e17bba0e3797-NFI.json) |
| N404 | NFI-021B-CHECK-COMPRESSION | 030b addition | 345 MPa is the SR-200 datasheet minimum tensile yield, used as compressive. It is not a sourced compressive minimum at 0.691748 mm or after forming. The historical 379.2 MPa compression is a 1.96 mm sheet lot, not a thin-sheet minimum.; The three-of-five result is conditional on an additional, unvaried material transfer assumption. The card already flags this, so this is a carried source limitation, not an arithmetic error. | [rpt-ref-444ac46ffbede876f9cd](e22bbb97f4477a6d-NFI.json) |
| N432 | NFI-028b-SR200-compression | 030b addition | 345 MPa is tensile minimum, not a published compressive minimum; measure post-form compression. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N445 | NFI-028b-255-sensitivity | 030b addition | S-200-F 255 MPa is a compression sensitivity, not a rolled-sheet specification or certified minimum. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N487 | NFI-031-BE-PROPERTIES | 030b addition | SR-200 345MPa is a tensile minimum transferred to compression. The 379.2MPa endpoint is a historical lot result; continuous interpolated strength is not a procureable design allowable. 021 rev1 inherits 283MPa at E290GPa. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N498 | NFI-CHECK-028B-255-BOUND | 030b addition | With the fixed reserve and systems removed, the largest face thickness at zero core is 0.000896786528723 m and the 255 MPa compression factor is 0.958217295476. Core mass or joint excess leaves less face thickness. No gamma or wrinkling value changes that face factor. | [rpt-ref-aae116a5fcd787ed9abc](e5e8ac761055655d-CHECK-NFI.json) |
| N538 | NFI-036-finished-sheet-Fcy | 030b addition | Obtain a minimum compressive strength for the finished SR-200 face product in both in-plane directions. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N539 | NFI-036-biaxial | 030b addition | Validate transfer from directional uniaxial compression to equal in-plane compression. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N540 | NFI-036-historical-transfer | 030b addition | Resolve gauge, lot and finish transfer of the 379.2 MPa historical value. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N541 | NFI-036-current-handbook | 030b addition | Check current authorized material allowables and purchase specification. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N546 | NFI-036-other-sheet-grades | 030b addition | Qualify PS-200 or PF-60 mechanically before substitution. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N554 | 033-NFI-02 | 030b addition | Current and historical SR-200 properties; 345 MPa is a current minimum tensile-yield transfer to compression. The 379.2 MPa and 293.6 GPa endpoint is a historical roughly 1.96 mm SR-200 sheet tuple. E and strength move together; no free modulus improvement is granted. | [rpt-ref-5b1ba7a48fcb57c8e35e](a4edee0295bc38f3-NFI.json) |
| N652 | NFI-038-COMPRESSION | 030b addition | No finished thin SR200 compression minimum | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N689 | NFI-036-finished-sheet-Fcy | 030b addition | Obtain a minimum compressive strength for the finished SR-200 face product in both in-plane directions. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |
| N690 | NFI-036-biaxial | 030b addition | Validate transfer from directional uniaxial compression to equal in-plane compression. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |
| N691 | NFI-036-historical-transfer | 030b addition | Resolve gauge, lot and finish transfer of the 379.2 MPa historical value. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |
| N692 | NFI-036-current-handbook | 030b addition | Check current authorized material allowables and purchase specification. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |
| N697 | NFI-036-other-sheet-grades | 030b addition | Qualify PS-200 or PF-60 mechanically before substitution. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |
| B002 | NFI-030B-FIXED-ASSUMPTIONS | 030b addition | Two adjustable optimisms do not mean two unresolved assumptions.; The R10 nominal scarf already fixes .015 lb/ft2 film, assumes thin stock, transfers 345 MPa tensile yield to compression and uses an unqualified 10 MPa scarf screen. Neither zero strength-slider usage nor stock panel factor one qualifies those inputs. | [rpt-ref-39745602983887568501](02744dbf85113cc4-legacy--02744dbf85113cc4de64187c76ed79779e558031dadf21e6ad2f8aea21188dc1--AUTHORED-NFI.json) |

<a id="R014"></a>
### R014 — CFRP quasi-isotropic face properties (Be-free fallback)

**Original030 unknown:** QI laminate modulus and compressive strength for T700, M55J, K13D2U and boron/epoxy are estimated from UD data with assumed reduction factors, not measured.

**Original030 today:** least SF 0.5415 (exact geometry) to 0.6519 (published); relative loss 4.9 to 16.7 percent [MAINLINE-020]

**Original030 needed:** measured QI laminate modulus and compressive strength at intended fibre volume fraction [MAINLINE-008]; I014b QI laminate compression, stiffness, density and manufacturing route [MAINLINE-020]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N132 | NFI-008-QI-LAMINATE | 030 retained | QI laminate E and compressive strength for T700, M55J, K13D2U and boron/epoxy are estimates from UD/fibre data with the stated reduction factors, not measured laminate cards. | [rpt-ref-45da79edf548b064b228](6284193a78be0578-NFI.json) |
| N189 | NFI-020-BERYLLIUM-FREE-FALLBACK | 030 retained | K13D2U QI epoxy is the best inherited Be-free candidate, but its laminate and joint basis remain assumptions.; Ground the I014b QI laminate compression/stiffness/density and manufacturing route, then use the same evidenced joint mass and geometry for Be and composite. Do not substitute single-fiber moduli. | [rpt-ref-3e02218a03708a878faa](72e91c4df6df4236-NFI.json) |
| N607 | NFI-017b-FACE-MATERIAL | 030b addition | A lighter face at beryllium's E and strength (x1.73-1.87, 272-293 MPa per kg/m3) has no thin isotropic candidate: quasi-isotropic carbon is about 100 (a worker estimate with assumed matrix constants); nano-carbon films are lab only.; Sourced in-plane-isotropic properties of nano-carbon or other candidate face sheets. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |

<a id="R015"></a>
### R015 — face Poisson ratio (0.33 carried; Be sheet about 0.08)

**Original030 unknown:** Poisson ratio in buckling and foam-wrinkling formulas is carried from the 6061 case; no SiC value was given. Buckling pressure scales as 1/sqrt(1-nu^2).

**Original030 today:** nu 0.33 (carried from 6061) [MAINLINE-009]; nu 0.33 (card); nu12 0.0768, nu21 0.0752 (orthotropic lot) [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Original030 needed:** Face sheet's own Poisson ratio [MAINLINE-009]; Coherent measured in-plane elastic tuple and an orthotropic model, or a tagged isotropic approximation [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Current030b:** 028b scalar nu=.0752 and 033 scalar nu=.0768 are historical directional proxies; the inherited .33 is a comparison. Neither validates an orthotropic formed shell.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N051 | NFI-NU | 030 retained | {"id": "NFI-NU", "value": "Poisson ratio inside the buckling and foam-wrinkling formulas", "optimistic": 0.33, "conservative": 0.33, "factor": 1.0, "source": "Carried from the 6061 case. MAINLINE-008 does not give a SiC Poisson ratio.", "direction": "Use the face sheet's Poisson ratio. Buckling pressure scales as 1/sqrt(1-nu^2)."} | [rpt-ref-d5b4aaa267b71d82fe25](b9cd9c3b294887e6-NFI.json) |
| N119 | NFI-CHECK021-POISSON | 030 retained | Arithmetic follows the pinned nu=.33. Treat that as an explicit inherited assumption, not a sourced beryllium property. The demonstrated sensitivity changes the preferred two-optimism set. | [rpt-ref-e92af61311c9bf4a89cd](0b74ca6f4252ee9e-NFI.json) |
| N321 | NFI-NU | 030 retained | Every face uses nu 0.33 from the aluminium case. MAINLINE-008 published no Poisson ratio. CFRP, SiC and beryllium are not aluminium. | [rpt-mainline014-grok-balanced-sandwich-1019](e0fba238a74bd426-NFI.json) |
| N330 | NFI-NU | 030 retained | Every face uses nu 0.33. MAINLINE-008 published no Poisson ratio. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N405 | NFI-021B-CHECK-NU | 030b addition | The isotropic 0.33 value is inherited from aluminium, not established for SR-200. The cited lot has substantially lower in-plane Poisson ratios.; At nu=.0768, fixed-geometry global SF is 0.961118. Retuning the same gamma/wrinkle/panel set works at usage about 0.883289. This scalar substitution is a sensitivity, not an orthotropic laminate solution. | [rpt-ref-444ac46ffbede876f9cd](e22bbb97f4477a6d-NFI.json) |
| N433 | NFI-028b-sheet-anisotropy | 030b addition | Scalar nu=.0752 uses historical SR-200 data; a formed orthotropic shell requires its own model and properties. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N542 | NFI-036-sheet-elastic-model | 030b addition | Resolve the scalar elastic approximation and legacy nu=0.33. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N555 | 033-NFI-03 | 030b addition | Poisson ratio and isotropy; Primary nu=0.0768 is the historical SR-200 in-plane value represented as an isotropic scalar. Legacy nu=.33 changes the R10 scarf-screen endpoint from a deficit to a small surplus. The sign is convention-sensitive. | [rpt-ref-5b1ba7a48fcb57c8e35e](a4edee0295bc38f3-NFI.json) |
| N602 | NFI-017b-POISSON | 030b addition | nu 0.08 is the S-200F VHP mean (IAEA) transferred to SR-200 sheet; the inherited 0.33 reads 2.0 percent higher (0.5387 / 0.5818 against 0.5284 / 0.5711).; A measured in-plane Poisson ratio for cross-rolled SR-200 sheet. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| N693 | NFI-036-sheet-elastic-model | 030b addition | Resolve the scalar elastic approximation and legacy nu=0.33. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |

<a id="R016"></a>
### R016 — S-200F modulus is 290 GPa, not the 303 GPa of S-200FH

**Original030 unknown:** Comparisons retain 303 GPa, 283 MPa compression and nu 0.33 although the current forms sheet gives 290 GPa for S200F and 303 for S200FH; compression basis to reconcile.

**Original030 today:** E = 303 GPa as reported (source says 290 GPa) [CHECK-MAINLINE-09C5]; E = 303 GPa (card); 290 GPa (checker) [CHECK-MAINLINE-013]; E 303 GPa; compression 283 MPa; nu 0.33 (290 GPa sensitivity supplied) [MAINLINE-019]; E 303 GPa (card); 290 GPa (datasheet); sheet full-gamma SF 0.942 at same geometry [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Original030 needed:** Grade-specific 290 GPa, or an explicitly sourced 303 GPa scenario [CHECK-MAINLINE-09C5]; Use 290 GPa for the named grade and update the projection, or source and label S200FH [CHECK-MAINLINE-013]; Reconcile exact grade, compression basis and Poisson ratio; no tensile substitution [MAINLINE-019]; Keep E, strength and product form together; reissue claims under the grade correction [CHECK-rpt-ref-e92af61311c9bf4a89cd]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N001 | NFI-S200F-MODULUS | 030 retained | {"id": "NFI-S200F-MODULUS", "type": "source_mismatch", "row": "Beryllium S-200F", "field": "E_Pa", "reported": 303000000000, "source_value": 290000000000, "source_url": "https://hkvxni.files.cmp.optimizely.com/download/c3141b9ea04211ee9a7b2a5d2cb825d4", "page": 2, "proposed_fix": "Use grade-specific E=290 GPa or explicitly source a 303 GPa S200F scenario; retain QUESTIONABLE.", "stops_owner": false} | [rpt-1228-mainline009c5-independent-check-1019](4662757b4d50b2d1-NFI.json) |
| N007 | NFI-CHECK013-S200F-GRADE | 030 retained | S200F is 290 GPa; 303 GPa belongs to S200FH. Density remains 1850 kg/m3. | [rpt-1228-mainline013-independent-check-1020](ef406b56c4cff82e-NFI.json) |
| N012 | NFI-S200F-MODULUS | 030 retained | {"id": "NFI-S200F-MODULUS", "type": "source_mismatch", "row": "Beryllium S-200F", "field": "E_Pa", "reported": 303000000000, "source_value": 290000000000, "source_url": "https://hkvxni.files.cmp.optimizely.com/download/c3141b9ea04211ee9a7b2a5d2cb825d4", "page": 2, "proposed_fix": "Use grade-specific E=290 GPa or explicitly source a 303 GPa S200F scenario; retain QUESTIONABLE.", "stops_owner": false} | [rpt-1228-mainline014b-independent-check-1019](5d2a8afe8b483d72-NFI.json) |
| N074 | NFI-019-MATERIAL-GRADE | 030 retained | The current Materion forms sheet lists 290 GPa for S200F and 303 GPa for S200FH. Main comparisons deliberately retain the pinned 303 GPa, 283 MPa compression and nu=0.33; the 290 GPa sensitivity is supplied. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N118 | NFI-CHECK021-MODULUS | 030 retained | The inherited arithmetic passes, but the one-optimism sheet conclusion does not survive its own datasheet E. The E290/283 main route still uses two optimisms. | [rpt-ref-e92af61311c9bf4a89cd](0b74ca6f4252ee9e-NFI.json) |
| N198 | NFI-021-FACE-MODULUS | 030 retained | Corrected by ord-admiral-rr2-mainline021-be-modulus-290-1020: S-200F scored at its own 290 GPa (Materion DS-HPP-610); the 303 GPa the chain carried is S-200FH's. The SR-200 lot's own in-plane moduli are 298.7 and 293.6 GPa; the full-set column uses the lower. | [rpt-ref-769a7442efd5a04681e9](fae865c7f039491f-NFI.json) |
| N402 | NFI-020C-FALLBACK-E-BASIS | 030b addition | Section 4 takes 290 GPa as Be's current modulus, but section 6 prices the K13D2U trade against Be at the inherited 303 GPa. At 290 GPa, the SF given up by choosing K13D2U is smaller. | [rpt-ref-35706d7a2ae7e951590b](17d1e17bba0e3797-NFI.json) |
| N407 | NFI-021B-CHECK-GRADE-COUPLING | 030b addition | The complete subset table reproduces with E=290 GPa even when O3 is selected. Full-named-set mode and family calculations instead use 293.6 GPa. Thus the subset table does not literally couple every O3 strength choice to the stated alternate lot modulus.; Using E=293.6 GPa whenever O3 is selected changes secondary scores, e.g. all five to 0.708874 on the same grid. No subset feasibility changes and no two-member set floats. The chosen three-member set has no O3, so its answer is unchanged. | [rpt-ref-444ac46ffbede876f9cd](e22bbb97f4477a6d-NFI.json) |

<a id="R017"></a>
### R017 — SiC face properties (009b)

**Original030 unknown:** SiC face compressive strength is taken as 3900 MPa (compression mode) vs 380 MPa flexural; a compressive allowable for the sintered face and a membrane-compression-only check are open.

**Original030 today:** 3900 MPa compressive (optimistic); 380 MPa flexural (conservative); SF 0.433 if flexural used [MAINLINE-009]; E 410 GPa, density 3100 kg/m3 [MAINLINE-009]

**Original030 needed:** Compressive allowable for the sintered face; check stress stays membrane compression [MAINLINE-009]; Batch modulus and density for the actual face sheet [MAINLINE-009]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N049 | NFI-FACE-STRENGTH | 030 retained | {"id": "NFI-FACE-STRENGTH", "value": "SiC face compressive strength", "optimistic": 3900000000.0, "optimistic_source": "Saint-Gobain Hexoloy SA data https://www.ceramicsrefractories.saint-gobain.com/pt/files/4731/view (compressive 3900 MPa, flexural 380 MPa); MatWeb alpha SiC https://www.matweb.com/search/datasheet_print.aspx?matguid=dd2598e783ba4457845586b58c8ea9fb (density 3.10 g/cc, E 410 GPa)", "conservative": 380000000.0, "conservative_source": "Hexoloy SA flexural strength, the figure MAINLINE-008 says governs a bending or tension path.", "factor": 10.263157894736842, "stated_mode_uses": "compressive 3900 MPa, because the stated mode is face compression", "SF_if_flexural_were_used": 0.433343716061625, "direction": "A compressive allowable for the sintered face, and a check that the sphere stress stays membrane compression."} | [rpt-ref-d5b4aaa267b71d82fe25](b9cd9c3b294887e6-NFI.json) |
| N050 | NFI-FACE-MODULUS | 030 retained | {"id": "NFI-FACE-MODULUS", "value": "SiC Young's modulus and density", "optimistic": {"E_Pa": 410000000000.0, "rho": 3100.0}, "conservative": "no second sourced pair on MAINLINE-008", "factor": null, "tag": "QUESTIONABLE", "direction": "A batch modulus and density for the face sheet that would actually be built."} | [rpt-ref-d5b4aaa267b71d82fe25](b9cd9c3b294887e6-NFI.json) |

## T06 — Face sheet and panels

<a id="R018"></a>
### R018 — Be thin-sheet panel size and gauge: 0.914 m square-equivalent stock today, 3.13 to 4 m assumed (O4)

**Original030 unknown:** Severe-budget faces are far below supplier stock gauge; stock for the large panel begins at 0.059 in and the enhanced aluminium face at R=20 is thinner. Small panel size assumed.

**Original030 today:** 18 m equivalent widths required [MAINLINE-019]; Be faces about 0.056-0.057 mm; core 6.8-8.3 mm [MAINLINE-019]; stock begins 0.059 in (1.4986 mm); enhanced Al face 1.423 mm at R=20; panel 0.6096 x 1.8288 m [MAINLINE-027]; assumed panels 0.61x1.83 m (optimistic) to 0.30x0.61 m; source gauge tolerance 0.1016 mm [MAINLINE-020]

**Original030 needed:** Manufacturer grade, size, forming route, gauge tolerance and yield quote; spherical seam-layout takeoff [MAINLINE-019]; Local geometry, imperfections, seam load transfer and nonlinear validation [MAINLINE-019]; Supplier confirmation of dimensions at each minimum gauge, shaping yield, thickness distribution [MAINLINE-027]; supplier-confirmed grade, gauge, size, flatness; formed-panel gauge map and curvature survey [MAINLINE-020]

**Current030b:** Stock envelope factor is now one in 028b/033, eliminating adjustable panel enlargement. Availability at the required sub-1.499 mm gauges is still unestablished. 033's formal 103.892 m gamma+strength crossing exceeds the 6.35 mm sheet maximum.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N071 | NFI-019-PANELS | 030 retained | Neither 4 m nor 0.6 m curved thin S200F sandwich panels are established catalog products. The predecessor's 0.6-1.2 m rolled-sheet availability claim lacked a qualifying source. Required 18 m equivalent widths also exceed the local square-panel approximation's useful domain. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N077 | NFI-019-GEOMETRY-MODES | 030 retained | The severe case mathematically selects about 0.056-0.057 mm Be faces and 6.8-8.3 mm core. These are unqualified fabrication and continuum-model geometries; every scored least factor is far below 1. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N100 | NFI-027-PANEL-GAUGE | 030 retained | The large 020 panel is 0.6096×1.8288 m; its quoted stock maximum begins at 0.059 in (1.4986 mm). At R = 20 the enhanced aluminium face is only 1.423 mm. The conservative small panel is an assumed 0.3048×0.6096 m. Some severe-budget faces are far below the supplier's stated sheet gauge. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N186 | NFI-020-THIN-SHEET-GEOMETRY | 030 retained | Maximum currently purchasable 0.75-0.79 mm panel size and installed shape are UNKNOWN.; Ground second, with material NFI: obtain a supplier-confirmed grade/gauge/size/flatness specification, formed-panel gauge map and curvature survey. Measure edge and joint steps; establish trim yield. | [rpt-ref-3e02218a03708a878faa](72e91c4df6df4236-NFI.json) |
| N199 | NFI-021-SHEET-SIZE | 030 retained | SR-200 sheet comes to 24 by 72 inches, with gauges under 0.059 inch only at narrower widths and shorter lengths (Materion datasheet); a 10 m sphere needs over a thousand sheets, so the 5 percent joint allowance is QUESTIONABLE. | [rpt-ref-769a7442efd5a04681e9](fae865c7f039491f-NFI.json) |
| N205 | NFI-021b-PANEL | 030 retained | Thin (<0.059 in) SR-200 stock size is unpublished (020: UNKNOWN); curved forming at 10 m radius unverified. | [rpt-ref-1080d4f6a1af4cfa8c67](b056cc13a604abed-NFI.json) |
| N235 | NFI-028-14 | 030 retained | {"id": "NFI-028-14", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Today thin-sheet stock size", "today_value": "609.6 x 1828.8 mm is published for thicker sheet. Maximum size at 0.843 mm is UNKNOWN; smaller 304.8 x 609.6 is owner planning.", "required_or_budget_target": "Supplier-confirmed grade, gauge, blank dimensions and tolerances.", "needed_evidence": "A real quote/specification; do not label an extrapolated catalogue envelope as purchasable thin sheet.", "scenario": "af015_scarf", "scenario_joining_kg": 214.2399978421616, "factor_to_216_427kg_allowance": 0.9898943034693449, "mass_reduction_factor_to_fit": 1} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N236 | NFI-028-15 | 030 retained | {"id": "NFI-028-15", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Four-metre panels", "today_value": "4 x 4 m face blanks and compatible core are not demonstrated in the cited stock data", "required_or_budget_target": {"short_stock_dimension_scale_factor": 6.561679790026246, "long_stock_dimension_scale_factor": 2.1872265966754156, "modeled_AF_scarf_4m_kg": 190.76436622924268}, "needed_evidence": "Demonstrate the actual continuous face and include internal stock seams/core splices. A 4 m module assembled from small sheets keeps their seams.", "factor_to_216_427kg_allowance": null, "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N409 | NFI-021B-CHECK-PANEL-GAUGE | 030b addition | The 609.6 by 1828.8 mm stock limit applies to gauges at least .059 inch; the maximum stock size at the required .0272 inch gauge is unspecified. Forming, joining and gauge retention at a 3.128 m square-equivalent panel are unestablished.; Even the today panel endpoint is a thin-sheet transfer. A uniform minus-0.1016-mm gauge screen at fixed core reduces compression SF to 0.853129 and wrinkling SF to 0.787988; this is a sensitivity, not a prediction of the delivered gauge distribution. | [rpt-ref-444ac46ffbede876f9cd](e22bbb97f4477a6d-NFI.json) |
| N435 | NFI-028b-stock-envelope | 030b addition | Confirm available raw blank sizes at 0.74–0.80 mm thickness; full published envelope belongs to thicker sheet. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N488 | NFI-031-PANELS | 030b addition | The least-set P2 points need multi-metre square-equivalent panels at roughly 0.65–0.72mm face gauge. The nominal today 0.9144m seam-equivalent stock size is itself not established at those gauges. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N511 | ams7902-class-table-unread | 030b addition | AMS7902G section 3.5.5 was not in the three-page file. Current revision H, DOI 10.4271/AMS7902H, was not opened. No class tolerance is stated. | [rpt-mainline032b-grok-measured-flatness-1020](a754f4c4c109c350-NFI.json) |
| N545 | NFI-036-stock-size | 030b addition | Confirm available blank dimensions at the required thin gauges. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N557 | 033-NFI-05 | 030b addition | Stock dimensions and face gauges; The .6096 by 1.8288 m stock envelope is only published for gauges >=1.4986 mm; it is projected for thinner R10/R15 minima and the QS threshold. Formal gamma-plus-strength flotation at 103.892 m needs 8.235 mm faces, exceeding the 6.35 mm sheet maximum; even compression alone limits that stock to R<=99.898 m. | [rpt-ref-5b1ba7a48fcb57c8e35e](a4edee0295bc38f3-NFI.json) |
| N696 | NFI-036-stock-size | 030b addition | Confirm available blank dimensions at the required thin gauges. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |

## T07 — Cores

<a id="R019"></a>
### R019 — core crush criterion (crush strength against p/2)

**Original030 unknown:** Hexcel CR-III crush column is used; HFT and HRH-49 have no crush column so stabilised compressive strength is used; thickness does not enter; target is p/2.

**Original030 today:** catalog compressive strengths at 16-38 kg/m3 clear p/2 by about 7 to 27 times [MAINLINE-007]; core stress p/2 [MAINLINE-009]; core stress factor 1/2 of p (brief example, no pinned reference) [MAINLINE-05B]; required core strength 47730.4 Pa on every row [MAINLINE-013]

**Original030 needed:** A sourced crush model [MAINLINE-007]; Core stress from face-to-face load path including local bending [MAINLINE-009]; pinned sandwich core-crush reference and re-derived factor [MAINLINE-05B]; apply p/2 at 007's external pressure when it lands [MAINLINE-05B]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N033 | NFI-CRUSH | 030 retained | {"NFI_id": "NFI-CRUSH", "gap": "Crush is stated as about p/2 and tagged QUESTIONABLE. It is the brief's approximation, not an equilibrium solution, and it is outside the least stated safety factor.", "direction": "Keep it tagged until a sourced crush model replaces it.", "effect": "Catalog compressive strengths at 16 to 38 kg/m3 clear p/2 by about 7 to 27 times."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N053 | NFI-CRUSH-MODEL | 030 retained | {"id": "NFI-CRUSH-MODEL", "value": "core compressive stress", "optimistic": "p/2", "conservative": "p/2", "factor": 1.0, "source": "MAINLINE-005b. The brief's example, not a solved contact problem.", "direction": "A core stress from the face-to-face load path, including local bending."} | [rpt-ref-d5b4aaa267b71d82fe25](b9cd9c3b294887e6-NFI.json) |
| N128 | NFI-005B-MODEL | 030 retained | {"NFI_id": "NFI-005B-MODEL", "gap": "The p/2 core stress is the brief's example model, QUESTIONABLE, with no pinned sandwich reference. Local face bending and load spreading are ignored.", "direction": "Pin a sandwich core-crush reference and re-derive the factor.", "effect": "Required core strength scales linearly with whatever factor replaces 1/2."} | [rpt-ref-9dd3721f6f2e5595ab9a](fa0b32e084a42fda-NFI.json) |
| N130 | NFI-005B-007 | 030 retained | {"NFI_id": "NFI-005B-007", "gap": "MAINLINE-007 is not filed yet, so its rows have no crush numbers here, only the ready formula.", "direction": "Apply p/2 at 007's external pressure when that card lands.", "effect": "None until 007 exists."} | [rpt-ref-9dd3721f6f2e5595ab9a](fa0b32e084a42fda-NFI.json) |
| N168 | NFI-013-CRUSH-MODEL | 030 retained | The p/2 core-stress model is the brief's own example, QUESTIONABLE; local face bending is ignored. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N266 | NFI-CRUSH | 030 retained | {"NFI_id": "NFI-CRUSH", "gap": "Core crush has no formula in the pinned brief, so no crush target was produced.", "direction": "Name a crush pressure formula before treating crush as a stated limit.", "effect": "Crush is absent from the least stated safety factor."} | [rpt-mainline003-grok-p2-targets-1019](2090c6e1f4ca8afb-NFI.json) |
| N276 | NFI-CRUSH | 030 retained | {"NFI_id": "NFI-CRUSH", "gap": "Core crush still has no formula.", "direction": "Unchanged from 003.", "effect": "Crush stays out of the buckling safety factor."} | [rpt-mainline004-grok-knockdown-card-1019](e0152663a63bcf24-NFI.json) |
| N326 | NFI-CRUSH | 030 retained | Core crush is compressive strength over p/2. Thickness does not enter. The target is the MAINLINE-007 reading of about p/2. | [rpt-mainline014-grok-balanced-sandwich-1019](e0fba238a74bd426-NFI.json) |
| N340 | NFI-CRUSH-COLUMN | 030 retained | Hexcel CR-III crush is the crush column. HFT and HRH-49 have no crush column, so the stabilised compressive strength is used. Thickness does not enter the crush safety factor. The target is p/2. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |

<a id="R020"></a>
### R020 — core shear strength is not a scored mode

**Original030 unknown:** L and W plate-shear strengths are stored, but the crimp mode scores shear modulus and shear strength is not a separate mode.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N341 | NFI-SHEAR-STRENGTH | 030 retained | L and W plate-shear strengths are stored from the sheets. The scored crimp mode uses shear modulus. Shear strength is not a separate mode. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |

<a id="R021"></a>
### R021 — foam core allowables (crush strain, creep, design values)

**Original030 unknown:** H35 properties are typical or nominal, not allowables; rev9 prints a minimum compressive strength of 0.3 MPa vs 0.5 MPa nominal used (factor 1.67).

**Original030 today:** density 38 kg/m3; Ec 40 MPa; Gc 12 MPa; compressive 0.5 MPa nominal (0.3 MPa minimum) [MAINLINE-009]; incumbent 16 kg/m3 passes on one strain definition, fails on the other; lowest passing density between about 11 and 22 kg/m3 [MAINLINE-05B]; 11 kg/m3 lowest passing density, no creep derate [MAINLINE-05B]; EPS12 at 11.2 kg/m3: 15 kPa at 1 percent, 40 kPa at 10 percent [MAINLINE-013]

**Original030 needed:** Design allowables for Ec, Gc and compressive strength at the used thickness [MAINLINE-009]; checker names the governing strain definition [MAINLINE-05B]; sustained-load derate of foam allowables before relying on densities near 11 kg/m3 [MAINLINE-05B]; one strain definition and a measured value [MAINLINE-013]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N052 | NFI-CORE | 030 retained | {"id": "NFI-CORE", "value": "Divinycell H35", "optimistic": {"density_kg_m3": 38.0, "Ec_Pa": 40000000.0, "Gc_Pa": 12000000.0, "compressive_Pa": 500000.0}, "conservative": "Divinycell rev9 prints a minimum compressive strength of 0.3 MPa against the nominal 0.5 MPa used here. Other cores on MAINLINE-007 are typical columns, not allowables.", "factor_divinycell_compression": 1.6666666666666667, "tag": "QUESTIONABLE", "direction": "Design allowables for Ec, Gc and compressive strength at the thickness this point uses."} | [rpt-ref-d5b4aaa267b71d82fe25](b9cd9c3b294887e6-NFI.json) |
| N129 | NFI-005B-STRAIN | 030 retained | {"NFI_id": "NFI-005B-STRAIN", "gap": "Foam strengths are quoted at 1% and 10% strain by different sources. The incumbent 16 kg/m3 passes on one definition and fails on the other.", "direction": "The checker names the governing strain definition for a vacuum shell core.", "effect": "Lowest passing density moves between about 11 and about 22 kg/m3 on that choice."} | [rpt-ref-9dd3721f6f2e5595ab9a](fa0b32e084a42fda-NFI.json) |
| N131 | NFI-005B-CREEP | 030 retained | {"NFI_id": "NFI-005B-CREEP", "gap": "EPS at 10% strain is a short-term value; sustained vacuum loading creeps. No creep derate is applied.", "direction": "Derate foam allowables for sustained load before any density near 11 kg/m3 is relied on.", "effect": "The practical lowest density is higher than 11 kg/m3."} | [rpt-ref-9dd3721f6f2e5595ab9a](fa0b32e084a42fda-NFI.json) |
| N169 | NFI-013-EPS-DEFINITIONS | 030 retained | EPS strengths are specification minima at 1, 5 or 10 percent strain, and the sheets disagree. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |

<a id="R022"></a>
### R022 — honeycomb datasheet values and conversions (W vs L shear, typical vs minimum, density)

**Original030 unknown:** Datasheets print conflicting values: Plascore 5052 gives 100 psi and 0.55 MPa in one cell; Divinycell H35 0.45 MPa (rev7) vs 0.50 MPa (rev9). Crush margins still clear.

**Original030 today:** 100 psi vs 0.55 MPa; H35 0.45 vs 0.50 MPa [MAINLINE-007]; Hexcel test thickness 0.625 inch vs 20 mm core [MAINLINE-021]; 16 kg/m3 [rpt-mainline-grok-estimates-card-1019]; 14.3 ksi used (brochure 13.3 ksi) [MAINLINE-14B]

**Original030 needed:** Keep both readings; resolve revision [MAINLINE-007]; Pin a honeycomb or foam sheet at the thickness used. [rpt-mainline-grok-estimates-card-1019]; Stabilised Ec and L/W shear moduli in the band. [MAINLINE-14B]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N039 | NFI-DATASHEET | 030 retained | {"NFI_id": "NFI-DATASHEET", "gap": "Plascore PAMG-XR1 5052 prints 100 psi and 0.55 MPa in one bare-compression minimum cell. Those are not the same number. Divinycell H35 prints 0.45 MPa on a rev7 sheet and 0.50 MPa nominal on rev9. The psi column and the rev9 nominal were used.", "direction": "Keep both readings. Do not pick a silent third value.", "effect": "The crush margins move by that disagreement and still clear p/2."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N201 | NFI-021-CORE-TABLE | 030 retained | Core properties are 014b's: W shear as Gc, stabilised Ec, Hexcel's crush column for crush; Hexcel test thickness 0.625 inch against a 20 mm core. | [rpt-ref-769a7442efd5a04681e9](fae865c7f039491f-NFI.json) |
| N246 | NFI-CORE | 030 retained | {"NFI_id": "NFI-CORE", "linked_inputs_or_points": "I-RHO-CORE", "questionable_assumption_or_gap": "16 kg/m^3 has no pinned datasheet.", "direction_of_further_investigation": "Pin a honeycomb or foam sheet at the thickness used.", "how_it_affects_margin_or_SF": "Core density scales core mass and can erase the float margin. It does not enter the reported collapse formula."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |
| N334 | NFI-W-SHEAR | 030 retained | Gc is the W plate-shear modulus, the lower of L and W on every sheet row scored here. Crimping and honeycomb wrinkling use that Gc. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N335 | NFI-W-13-3 | 030 retained | The attributes brochure text shows 13.3 ksi for CR-III 5052 3/16-2.0 W modulus. The CR-III data sheet prints 14.3 ksi. This card uses 14.3. The brochure's 1/4-3.4 L modulus glyph 50..0 is 50.0 on the data sheet. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N337 | NFI-DENSITY | 030 retained | Hexcel pcf converts at 0.45359237/0.3048^3. Plascore uses the kg/m3 printed on its sheet, so 2.0 pcf is 32 there and 32.037 on the Hexcel conversion. Rows above 4.0 pcf, and Plascore rows printed above 64 kg/m3, are outside the band and were not scored. HFT at 4.0 pcf converts to 64.074 kg/m3 and is kept. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N338 | NFI-CARBON | 030 retained | No carbon-fiber honeycomb sheet located here lists stabilised Ec and both shear moduli in this density band. Hexcel's product list has no carbon honeycomb table. Ultracor UCF-51-3/8-2.0 on MatWeb lists density 0.032 g/cc, compressive yield 1.41 MPa and L shear modulus 0.331 GPa, and omits Ec and W shear, so it is not scored. HFT is fiberglass phenolic. HRH-49 is Kevlar 49 fabric. Neither is carbon. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N444 | NFI-028b-core-data | 030b addition | Confirm core lot, minimum properties, forming and strength after bonding on the selected low-density core. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N529 | NFI-032-CHECK-MINIMUM-AVERAGE | 030b addition | non_blocking | [rpt-ref-a30a669ed3e245f1473b](f4fb2c3464ed42c3-NFI.json) |
| N612 | NFI-017b-CORE-CHOICE | 030b addition | Directions are computed on the lead's CR-III 5056 3/8-1.0; 5056 1/4-1.6 is 2.7 percent better today (0.5425 / 0.5939).; None for the ranking; factors on 1/4-1.6 would be slightly smaller. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| N625 | NFI-032-CHECK-FC | 030b addition | non_blocking | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N626 | NFI-032-CHECK-MINIMUM-AVERAGE | 030b addition | non_blocking | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |

<a id="R023"></a>
### R023 — thick curved honeycomb core validation

**Original030 unknown:** Core data are catalogue typical rows tested at 15.875 mm depth, while optimised cores reach about 120-144 mm; Ec transferred from another maker and bare compression substituted for crush.

**Original030 today:** test depth 15.875 mm vs 120-144 mm needed at R=50 [MAINLINE-027]

**Original030 needed:** Validation of thick curved honeycomb: skin restraint, orthotropy, depth effects, crush definition [MAINLINE-027]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N105 | NFI-027-CORE-TRANSFER | 030 retained | 5056 3/8-1.0 uses the published typical Ec/Gc/crush row; stabilized modulus is used in the wrinkle formula. Manufacturer tests were at 15.875 mm depth; optimized cores reach roughly 120–144 mm at R = 50. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N447 | sheet-thickness | 030b addition | Table II says the test thickness is 0.625 inch. The lead cores are 20.21 mm and 30.12 mm. Ec is typical only. No minimum modulus is printed. | [rpt-mainline032-grok-wrinkle-waviness-1020](df2ac0989ca4f688-NFI.json) |
| N530 | NFI-032-CHECK-THICKNESS | 030b addition | non_blocking | [rpt-ref-a30a669ed3e245f1473b](f4fb2c3464ed42c3-NFI.json) |
| N627 | NFI-032-CHECK-THICKNESS | 030b addition | non_blocking | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |

<a id="R024"></a>
### R024 — ultralight cores below about 16 kg/m3: no sourced material; scaled moduli are PROJECTION

**Original030 unknown:** No measured shear modulus at or below 10 kg/m3; G=E/2 is an assumption; figure reads, bulk-scale transfer and continuum validity unproved; 190 kg/m3 row passes locally only.

**Original030 today:** Basotect crush above 9000 Pa, no upper bound; EPS12 minimum 15000 Pa at 1% strain, density minimum 11.2 kg/m3 [CHECK-MAINLINE-013]; named-set high SF 0.737 at 1 kg/m3; buckling SF reaches 1 at 3.73 kg/m3 [MAINLINE-007]; density at or above 0.9 kg/m3 [MAINLINE-007]; lightest sourced catalog core 16 kg/m3 (ROHACELL 31, HexWeb 24); microlattice at 0.9 kg/m3 has no modulus or strength [MAINLINE-08B]

**Original030 needed:** Measured crush, Ec and G of the actual material; keep comparison operators and property basis [CHECK-MAINLINE-013]; Measured properties at the claimed density before any new material claim; keep PROJECTION tag on ideal-lattice uses [CHECK-MAINLINE-013]; A sourced structural core at low density [MAINLINE-007]; Sourced Gc, Ec and crush strength at those densities [MAINLINE-007]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N008 | NFI-CHECK013-LOWER-BOUNDS | 030 retained | The scalar screening ratios reproduce, but a lower bound below a demand does not establish that the actual material fails. Neither of these records supplies Ec or G. The data still establish no all-three pass. | [rpt-1228-mainline013-independent-check-1020](ef406b56c4cff82e-NFI.json) |
| N011 | NFI-CHECK013-INHERITED-LIMITS | 030 retained | No measured G at or below 10 kg/m3; isotropic G=E/2 is an assumption, not a universal anisotropic bound. Figure reads, bulk-scale transfer, continuum/elastic validity and independent crush modelling remain unproved. The 190 kg/m3 row is a conditional local pass, while its global SF is 0.02035. | [rpt-1228-mainline013-independent-check-1020](ef406b56c4cff82e-NFI.json) |
| N029 | NFI-DENSITY | 030 retained | {"NFI_id": "NFI-DENSITY", "gap": "This card is the density trade NFI-DENSITY asked for. The least stated safety factor still rises as density falls through 1 kg/m3. There is no interior peak on 0.25 to 64 kg/m3.", "direction": "Do not treat 1 kg/m3 as a proved best density. No sourced structural core was retrieved there.", "effect": "The named-set high is 0.737028554512 at 1 kg/m3, still below 1. Buckling safety factor reaches 1 at 3.73369568197 kg/m3 and yield governs that point."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N038 | NFI-CORE-FLOOR | 030 retained | {"NFI_id": "NFI-CORE-FLOOR", "gap": "No catalog structural core with sourced Gc, Ec, and compressive strength was retrieved at 8, 6, 4, 3, 2, or 1 kg/m3.", "direction": "Do not extrapolate a honeycomb or foam modulus below the catalog floor.", "effect": "The low-density safety factors are geometry of the stated model, not a claim that a core exists."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N040 | NFI-MICROLATTICE | 030 retained | {"NFI_id": "NFI-MICROLATTICE", "gap": "Schaedler et al. 2011 place a nickel microlattice at or above 0.9 kg/m3. The open abstract has no usable modulus or strength.", "direction": "A later card can read the paper. This card does not invent the coefficient.", "effect": "No crush, crimp, or wrinkling margin is reported for it. A usable-core projection is not claimed."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N046 | NFI-CORE-FLOOR | 030 retained | {"NFI_id": "NFI-CORE-FLOOR", "gap": "Densities 8 through 1 still have no sourced Gc and Ec. The Schaedler microlattice still has no modulus.", "direction": "Do not extrapolate a catalog modulus down to those densities.", "effect": "Those MAINLINE-007 safety factors are not revised."} | [rpt-ref-3dd5ab5528276031581d](07d0f8e52a240650-NFI.json) |
| N138 | NFI-008B-CORE-NONE-LIGHT | 030 retained | The re-rank rows at 4 and 1 kg/m3 presume a structural core that does not exist today. MAINLINE-007 retrieved no catalog core with sourced shear modulus, compressive modulus and strength below 16 kg/m3 (Plascore lightest 16, ROHACELL IG-F starts 31, HexWeb lightest retrieved 24; Schaedler nickel microlattice 0.9 kg/m3 has no retrieved modulus or strength). | [rpt-ref-cc9cef5e55adca018a8f](cbad32790fc5fde1-NFI.json) |
| N155 | NFI-013-WRINKLE-PRODUCT | 030 retained | No measured core at or below 10 kg/m3 meets the wrinkling need with 6061 faces on the P2 float ceiling. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N156 | NFI-013-SHEAR-UNMEASURED | 030 retained | No source measured a transverse shear modulus for any core at or below 10 kg/m3. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N157 | NFI-013-CRIMP | 030 retained | On the least-factor split no measured core at or below 10 kg/m3 reaches the crimp shear modulus. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N158 | NFI-013-STRENGTH-BASIS | 030 retained | Most ultralight strengths are not crush strengths: stress at 80 percent strain (Qiu 2012), undefined 'max stress' (Si 2014), ultimate stress of undefined strain (Xu 2019), 40 percent compression (Basotect), indentation or tension (Kashani 2019). These can fail the crush check but never pass it. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N159 | NFI-013-MID-DENSITY | 030 retained | This card sourced no core between 53 and 190 kg/m3, so the lightest core passing all three is bounded, not found. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N162 | NFI-013-CONTINUUM-AND-DIMPLING | 030 retained | The continuum wrinkling form assumes a core finer than the wrinkle wavelength; lattice cell sizes were not sourced. Intracell dimpling, a fourth local mode outside the card's three, is reported beside them. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N163 | NFI-013-HONEYCOMB-FORM | 030 retained | CR-1457 eq 2.2-14 at these core-to-face ratios (tc/tf about 220 to 560) is far outside its test data; it makes the honeycomb need an Ec no honeycomb has. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N166 | NFI-013-IDEAL-LATTICE | 030 retained | The ideal stretch-dominated lattice (Ashby 2006 eq 5.1, Gc = Ec/2) is a bound, not a material; strength is not projected because no strut-buckling constant was sourced. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N170 | NFI-013-SCALE-AND-ENVIRONMENT | 030 retained | Every lattice and aerogel in this table was tested as a laboratory specimen (micrometres to centimetres); the float-ceiling core is about 1257 m2 by 0.19 m. The commercial foams (EPS, melamine, polyimide) are made at larger scale but fail the checks by orders of magnitude. Vacuum outgassing, creep under a sustained p/2 (polymer foams), and temperature were not assessed. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N262 | NFI-DENSITY | 030 retained | {"NFI_id": "NFI-DENSITY", "gap": "All three points keep the inherited core density of 16 kg/m3. The advisory lower-density leads were not given a point.", "direction": "A later card can spend one of three points on a named lower density.", "effect": "A lighter core leaves more of the ceiling for faces or for a thicker core."} | [rpt-mainline003-grok-p2-targets-1019](2090c6e1f4ca8afb-NFI.json) |
| N273 | NFI-DENSITY | 030 retained | {"NFI_id": "NFI-DENSITY", "gap": "Lower core density stays deferred. This unit adds no density point.", "direction": "Leave it to a later card.", "effect": "None inside these four rows."} | [rpt-mainline004-grok-knockdown-card-1019](e0152663a63bcf24-NFI.json) |
| N295 | NFI-DENSITY | 030 retained | {"NFI_id": "NFI-DENSITY", "gap": "Confirmed: least SF rises as density falls through the named set, peaking at 1 kg/m3 (0.7370285545124737), and my 0.25-64 kg/m3 scan has no interior peak (0.7672968655351241 at 0.25). No sourced structural core was retrieved at 1-8 kg/m3.", "direction": "Do not treat 1 kg/m3 as a proved best density.", "effect": "Owner statement stands."} | [rpt-mainline007-check-lead4f19-1019](a27128f0dc1713bc-NFI.json) |
| N304 | NFI-CORE-FLOOR | 030 retained | {"NFI_id": "NFI-CORE-FLOOR", "gap": "Confirmed: densities 8-1 have no sourced Gc/Ec and are not revised; the microlattice has no modulus and no SF.", "direction": "Do not extrapolate catalog moduli downward.", "effect": "Owner statement stands."} | [rpt-mainline007b-check-lead4f19-1019](ef98a0f4f10c64ba-NFI.json) |
| N323 | NFI-SCALE | 030 retained | Densities 16, 8 and 4 have no fully sourced core in MAINLINE-007. Ec and Gc scale as rho^2 and crush strength as rho^1.5 from the 32 kg/m3 sourced row. PROJECTION. | [rpt-mainline014-grok-balanced-sandwich-1019](e0fba238a74bd426-NFI.json) |
| N324 | NFI-013 | 030 retained | MAINLINE-013 has not filed. Its cores are not used. | [rpt-mainline014-grok-balanced-sandwich-1019](e0fba238a74bd426-NFI.json) |
| N332 | NFI-SCALE | 030 retained | The 014 projections at 16, 8 and 4 kg/m3 stay in the set. Moduli scale as rho^2 and crush as rho^1.5. The scaled aramid keeps the parent 4.8 mm cell. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |
| N333 | NFI-013 | 030 retained | MAINLINE-013 has not filed. Its cores are not used. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |

## T08 — P2 joints, seams and film

<a id="R025"></a>
### R025 — 30:1 adhesive scarf seam

**Original030 unknown:** Thin Be/Be scarf performance is untested; the 10 MPa shear screen is selected, not qualified.

**Original030 today:** 25.303 mm run; 9.421 MPa average shear; 0.01060 kg/m seam [MAINLINE-028]

**Original030 needed:** thin Be/Be scarf compression, biaxial transfer, peel and cyclic data at actual film weight [MAINLINE-028]

**Current030b:** CHECK-028b confirms the nominal/primer screen and no-singleton result. The 10 MPa mean-shear screen, corresponding to 300.333 MPa face stress at 30:1, remains a projection; peel and installed capacity are unknown.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N228 | NFI-028-07 | 030 retained | {"id": "NFI-028-07", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Thirty-to-one adhesive scarf", "today_value": "25.303-mm run; 70-g/m2 seam film; 9.421 MPa average shear; screen 10 MPa is selected, not qualified", "required_or_budget_target": {"total_seam_kg_m": 0.010597793381544554, "max_seam_kg_m_after_AF015": 0.011365897456349418}, "needed_evidence": "Thin Be/Be scarf compression, biaxial transfer, peel/end effects, cyclic and local buckling data at actual film weight.", "scenario": "af015_scarf", "scenario_joining_kg": 214.2399978421616, "factor_to_216_427kg_allowance": 0.9898943034693449, "mass_reduction_factor_to_fit": 1} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N422 | NFI-028-SHEAR-SCREEN | 030b addition | The 30:1 scarf average shear is 9.421138296 MPa. The 10 MPa screen is owner-selected. Its factor at the frozen geometry is 1.061442862. No qualified allowable for this beryllium scarf was in the pinned sources. | [rpt-ref-68dff0680696fe9b4cb4](43ed944cb7138cf7-NFI.json) |
| N434 | NFI-028b-scarf10 | 030b addition | Measure mean-shear allowable and peel/compression failure of the exact scarf; 10 MPa is assumed. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N497 | NFI-CHECK-028B-SEAM-SCREEN | 030b addition | The 0.97197751743 and 0.996075 usages are set by the assumed 10 MPa scarf-shear screen, which caps face stress at 300.333333 MPa. That screen is not a measured beryllium scarf allowable. The laboratory 0.651468543105 usage is the same with the screen off, because the ideal weld is scored as parent face compression. | [rpt-ref-aae116a5fcd787ed9abc](e5e8ac761055655d-CHECK-NFI.json) |
| N548 | NFI-036-scarf | 030b addition | Qualify the assumed scarf compression/shear/peel capacity. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N613 | NFI-017b-SCARF | 030b addition | The scarf is steepened beyond 30:1 to meet 028's 10 MPa average-shear screen, which is owner-selected, not an allowable; bond and seam strengths are unmeasured (028's rows).; 028's evidence needs: a weighed, load-tested curved Be/Al panel. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| N656 | NFI-038-SEAM_MODES | 030b addition | Mean shear does not qualify peel, cyclic debond or local instability | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N699 | NFI-036-scarf | 030b addition | Qualify the assumed scarf compression/shear/peel capacity. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |

<a id="R026"></a>
### R026 — adhesive-free diffusion interface

**Original030 unknown:** Zero added filler is an ideal limit; the replacement core density and strength are unknown.

**Original030 today:** 0 added filler (ideal limit) [MAINLINE-028]

**Original030 needed:** complete installed bill and measured structure: core density, stiffness, strength, process pressure [MAINLINE-028]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N227 | NFI-028-06 | 030 retained | {"id": "NFI-028-06", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Diffusion/integral adhesive-free interface", "today_value": "0 added filler is an ideal limit; replacement core mass and strengths unknown", "required_or_budget_target": "Provide a complete installed bill and measured structure, not just zero adhesive.", "needed_evidence": "New core density/stiffness/strength, processing pressure and post-process interface performance.", "factor_to_216_427kg_allowance": null, "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |

<a id="R027"></a>
### R027 — bond film areal weight and coverage (0.015 to 0.060 lb/ft2)

**Original030 unknown:** Matching Be/core strength and stiffness at the lowest-weight reticulated film weight are unmeasured; hull adoption is a projection.

**Original030 today:** 0.03 lb/ft2 (full optimism 0.015 lb/ft2) [MAINLINE-21B]; AF163-2U 73.236 g/m2 exists; budget maximum 74.107 g/m2 [MAINLINE-028]; manufacturer tolerance +/-0.005 lb/ft2; upper-weight joining 275.6 kg vs 216.4 kg allowance [MAINLINE-028]; HexBond312 70 g/m2 lap shear 37 MPa on Al; 100 g/m2 5.4 MPa on a different sandwich [MAINLINE-028]

**Original030 needed:** 0.03 lb/ft2 at the floating point [MAINLINE-21B]; weigh installed cured film; Be/core strength, stiffness and defects at that weight [MAINLINE-028]; lot areal-mass distribution and cured retained mass [MAINLINE-028]; test of the actual assembly [MAINLINE-028]

**Current030b:** The .015lb/ft2 film in 028b/033 is a fixed2× mass reduction from.030, not a proven assembly. CHECK-028 reports a weight tolerance;033 did not independently establish it. CHECK-036 identifies an unused olderR20 .015 label but governing.146472829kg/m2=.030lb/ft2 field; the old027 calculations use.030 correctly. Keep the two models distinct.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N206 | NFI-021b-FILM | 030 retained | Be/honeycomb bond suitability of any AF 163 weight is unqualified (019, 020). | [rpt-ref-1080d4f6a1af4cfa8c67](b056cc13a604abed-NFI.json) |
| N222 | NFI-028-01 | 030 retained | {"id": "NFI-028-01", "status": "OPEN", "tag": "QUESTIONABLE", "technology_state": "exists_today", "hull_adoption_state": "PROJECTION", "assumption": "Lowest-weight reticulated film performance", "today_value": "AF163-2U 73.236 g/m2 exists; no matching flatwise/core-shear result", "required_or_budget_target": {"maximum_g_m2_with_modeled_stock_scarf": 74.10665270534186}, "needed_evidence": "Weigh installed cured film and obtain Be/selected-core strength, stiffness and defect performance at this weight. Reticulation is not an open-area mass discount.", "scenario": "af015_scarf", "scenario_joining_kg": 214.2399978421616, "factor_to_216_427kg_allowance": 0.9898943034693449, "mass_reduction_factor_to_fit": 1} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N223 | NFI-028-02 | 030 retained | {"id": "NFI-028-02", "status": "OPEN", "tag": "QUESTIONABLE", "technology_state": "exists_today", "hull_adoption_state": "PROJECTION", "assumption": "Film weight tolerance", "today_value": "Manufacturer +/-0.005 lb/ft2", "required_or_budget_target": {"nominal_kg": 214.2399978421616, "upper_weight_kg": 275.5943930187407}, "needed_evidence": "Lot areal-mass distribution and cured retained mass; prove low tail still bonds and high tail floats.", "scenario": "af020_tolerance_scarf", "scenario_joining_kg": 275.5943930187407, "factor_to_216_427kg_allowance": 1.2733818262933878, "mass_reduction_factor_to_fit": 1.2733818262933878} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N224 | NFI-028-03 | 030 retained | {"id": "NFI-028-03", "status": "OPEN", "tag": "QUESTIONABLE", "technology_state": "exists_today", "hull_adoption_state": "PROJECTION", "assumption": "Low-weight fillet-forming catalogue film", "today_value": "HexBond312: 70 g/m2 lap shear 37 MPa on Al; its flatwise column is blank. 100 g/m2 has 5.4 MPa on a different sandwich.", "required_or_budget_target": {"70gsm_complete_kg": 206.10600091345282, "100gsm_complete_kg": 281.5042245996078}, "needed_evidence": "Do not move the 100-g/m2 result into the 70-g/m2 column; test the actual assembly.", "scenario": "hex100_scarf", "scenario_joining_kg": 281.5042245996078, "factor_to_216_427kg_allowance": 1.3006881587956576, "mass_reduction_factor_to_fit": 1.3006881587956576} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N437 | NFI-028b-AF015-bond | 030b addition | Published weight exists; matched Be/low-density-aluminium-core bond strength and stiffness are unknown. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N655 | NFI-038-BOND_MASS | 030b addition | Thin film, primer and repairs have no demonstrated installed mass | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N704 | CHECK036-D1 | 030b addition | Inherited R20 film label differs by a factor of two from the governing mass field. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |

<a id="R028"></a>
### R028 — brazed scarf seam

**Original030 unknown:** Al-Si braze shear is a typical value, not an allowable; thin-sheet joint distribution, fatigue and distortion unknown.

**Original030 today:** Al-Si typical shear 103.4 MPa vs 84.884 MPa needed; 50 um filler gap [MAINLINE-028]

**Original030 needed:** thin-sheet joint distribution, compressive/peel fatigue, distortion, closure sequence [MAINLINE-028]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N230 | NFI-028-09 | 030 retained | {"id": "NFI-028-09", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Brazed scarf seam", "today_value": "Materion Al-Si typical average shear 103.4 MPa; assumed 3:1 scarf needs 84.884 MPa; 50-um filler gap", "required_or_budget_target": {"mean_shear_ratio_available_to_required": 1.218126436982413, "face_filler_kg_m": 0.0007201485650694222}, "needed_evidence": "Thin-sheet joint distribution, compressive/peel fatigue, distortion and final closure sequence; source typical is not an allowable.", "scenario": "lab8_braze_scarf", "scenario_joining_kg": 41.54621864151882, "factor_to_216_427kg_allowance": 0.1919639916829661, "mass_reduction_factor_to_fit": 1} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |

<a id="R029"></a>
### R029 — butt-strap seam route

**Original030 unknown:** Butt-strap bending, peel and strip buckling are unmeasured; this route is 2.88x over the joining allowance.

**Original030 today:** 47.730 mm strap width per face; 0.162691 kg/m; 623.1 kg [MAINLINE-028]

**Original030 needed:** measured local bending and peel, strip buckling, or a symmetric alternative [MAINLINE-028]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N229 | NFI-028-08 | 030 retained | {"id": "NFI-028-08", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Butt-strap seam", "today_value": "47.730-mm width per face under a 10-MPa mean-shear screen; 0.162691 kg/m including closure", "required_or_budget_target": "Carry 238.652 kN/m per face including eccentricity.", "needed_evidence": "Measured local bending/peel, strip buckling and a mass-accounted symmetric alternative.", "scenario": "hex70_strap", "scenario_joining_kg": 623.092652861521, "factor_to_216_427kg_allowance": 2.8789949300486715, "mass_reduction_factor_to_fit": 2.8789949300486715} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |

<a id="R030"></a>
### R030 — core splice allowance

**Original030 unknown:** Installed core splice mass and its ability to transmit core shear are unknown.

**Original030 today:** selected 0.5 mm gap and 500 kg/m3 cured filling; 0.00505 kg/m [MAINLINE-028]

**Original030 needed:** weighed edge splice transmitting core shear with real gaps and nodes [MAINLINE-028]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N232 | NFI-028-11 | 030 retained | {"id": "NFI-028-11", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Core splicing allowance", "today_value": "Selected 0.5-mm gap and 500 kg/m3 cured filling density; installed value unknown", "required_or_budget_target": {"modeled_kg_m": 0.005053344096872905}, "needed_evidence": "Weighed edge splice transmitting core shear with actual gaps, nodes and intersections.", "scenario": "af015_scarf", "scenario_joining_kg": 214.2399978421616, "factor_to_216_427kg_allowance": 0.9898943034693449, "mass_reduction_factor_to_fit": 1, "modeled_component_kg": 14.389204513742502, "component_fraction_of_allowance": 0.06648521155280727} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N441 | NFI-028b-splice-and-seal | 030b addition | Weigh and qualify the core splice, seals and intersection details. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |

<a id="R031"></a>
### R031 — core-to-face brazing route

**Original030 unknown:** No structural data for brazing a Be face to the selected 16 kg/m3 Al core exist; coated CRIII properties may not carry over.

**Original030 today:** generic Be brazing exists; filler 5.67-22.68 g/m2 geometric [MAINLINE-028]

**Original030 needed:** wetting, residual stress and bare-core condition after joining qualified [MAINLINE-028]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N226 | NFI-028-05 | 030 retained | {"id": "NFI-028-05", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Core-to-face brazing", "today_value": "Generic Be brazing exists; no selected Be/16-kg/m3-Al-core structural data found", "required_or_budget_target": {"geometric_filler_g_m2": [5.6692913386, 22.6771653543], "fillet_leg_mm": [0.1, 0.2]}, "needed_evidence": "Qualify wetting, residual stress and bare/metal-node core after joining. Do not retain coated H-39 CRIII properties without evidence.", "factor_to_216_427kg_allowance": null, "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill.", "modeled_component_kg": 14.248483216281267, "component_fraction_of_allowance": 0.06583500985313998} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |

<a id="R032"></a>
### R032 — electron-beam seam retention

**Original030 unknown:** Thin-sheet Be EB seam compression retention is unknown; 100 percent retention is a projection and 80 percent a sensitivity.

**Original030 today:** Be EB process exists; SF 0.853 at assumed 80 percent retention [MAINLINE-028]

**Original030 needed:** retention 0.9998 at original gauge; weld/HAZ compression, ductility, penetration, leak integrity [MAINLINE-028]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N231 | NFI-028-10 | 030 retained | {"id": "NFI-028-10", "status": "OPEN", "tag": "QUESTIONABLE", "technology_state": "exists_today", "hull_adoption_state": "PROJECTION", "assumption": "Electron-beam seam retention", "today_value": "Be EB process exists; matching thin-sheet compression evidence unknown. 100% retention is a projection; 80% is a sensitivity.", "required_or_budget_target": {"required_retention_at_original_gauge": 0.9998169145727672, "SF_with_assumed_80pct_reoptimized": 0.8529780485063345}, "needed_evidence": "Establish weld/HAZ compression, ductility, full penetration, distortion and leak integrity; account reinforcement/repair mass.", "scenario": "lab8_eb_eta1", "scenario_joining_kg": 39.492661922586976, "factor_to_216_427kg_allowance": 0.18247554826252008, "mass_reduction_factor_to_fit": 1} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N440 | NFI-028b-lab-weld | 030b addition | Ground parent compression retention, HAZ, brittle seam failure, distortion and final-hull access. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N549 | NFI-036-lab-bond-weld | 030b addition | Qualify the 8 g/m2 bond and weld strength retention. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N700 | NFI-036-lab-bond-weld | 030b addition | Qualify the 8 g/m2 bond and weld strength retention. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |

<a id="R033"></a>
### R033 — P2 seam and bond mass and capacity on the hull (016, 019, 020, 021b, 027, 028)

**Original030 unknown:** Net-section efficiencies are assumed screens applied only to compression; the enhanced aluminium optimum is joint-limited and no joint buckling, shear or peel allowables exist.

**Original030 today:** today's 0.5 m Hexoloy plate gives 330-694% of the 216.427 kg allowance [MAINLINE-016]; film use .015/.030 lb/ft2 (.015 mass-lower choice) [MAINLINE-019]; efficiencies 0.9 / 0.6 (assumed) [MAINLINE-027]; joining 968.2 kg optimistic (eta 0.9) to 3722.0 kg conservative (eta 0.6); payload -507 to -3261 kg [MAINLINE-020]

**Original030 needed:** Real maximum plate size and a seam parts list for a named panel size, or a face family with 2-4 m sheets [MAINLINE-016]; Test a complete seam and bond architecture for installed mass, leak rate and stiffness [MAINLINE-019]; Weigh and load-test a curved two-skin splice; seam parameters versus thickness [MAINLINE-027]; Measured seam biaxial compression, eccentricity and failure envelope [MAINLINE-027]

**Current030b:** 028b nominal/primer joining at the reoptimized R10 points is 215.742/227.880 kg, not the old frozen 214.240/226.806 kg. 033 main account charges actual joining; its comparison retains the unused 5% floor. Joint strengths remain unknown.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N057 | NFI-016-SEAM | 030 retained | {"NFI_id": "NFI-016-SEAM", "rank": 1, "gap": "Joint and seam mass at the 009 SiC point: 89.2 to 3004.3 kg across panel sizes 4 m to 0.25 m, against the 216.427 kg five percent allowance. Only 4 m panels, which do not exist in SiC today (PROJECTION), fit; today's 0.5 m Hexoloy plate size is 330 to 694 percent of the allowance; conservative 0.25 m tiling leaves the hull 966 to 2543 kg heavy.", "direction": "Pin the real maximum Hexoloy SA plate size from the manufacturer, and produce a seam parts list (doubler, adhesive, core splice) for a named panel size; or re-run the point on a face family whose sheet widths are 2 to 4 m today (aluminium, CFRP layup).", "effect": "Decides alone whether the 009 point floats; up to 1388 percent of the joint allowance."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |
| N072 | NFI-019-JOINTS | 030 retained | Two face strips, their bond lines, core splice and full-area face/core adhesive are now counted. Strip sizing and .015/.030 lb/ft2 film use are not qualified for Be, peel, thermal cycling or vacuum; .015 is only a mass lower choice. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N101 | NFI-027-SEAM-SCALING | 030 retained | Frozen 020 kg/m 2 hides Be-doubler and core-gap masses that grow with optimized thickness. The corrected model holds widths/gaps fixed but resizes their depths. Neither seam is mechanically designed. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N102 | NFI-027-JOINT-STRENGTH | 030 retained | 020's 0.9/0.6 net-section efficiencies are assumed screens, applied only to compression. The enhanced aluminium optimum is global/joint limited. No joint buckling, shear or peel allowables exist. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N185 | NFI-020-JOINT-MASS-CAPACITY | 030 retained | Installed bond/seam mass and capacity are not contained by an evidenced 5% allowance.; Ground first: weigh and load a representative curved two-skin/core seam with the intended film coverage, seal, manufacturing defects and post-thermal-cycle condition. Establish seam buckling, shear/peel and leak behavior. | [rpt-ref-3e02218a03708a878faa](72e91c4df6df4236-NFI.json) |
| N209 | NFI-021b-JOINT-PARAMETERS | 030 retained | 019's optimistic joint parameters (60 mm strips, 0.2 mm adhesive, 1.5 mm core splice) are owner assumptions, not validated joints; 020's own splice model weighs 0.218 kg per hull-seam metre in its optimistic case. | [rpt-ref-1080d4f6a1af4cfa8c67](b056cc13a604abed-NFI.json) |
| N238 | NFI-028-17 | 030 retained | {"id": "NFI-028-17", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Installed bond strength and stiffness", "today_value": "Core Ec=103.421 MPa, G_W=46.884 MPa inherited; actual bonded effective values unknown", "required_or_budget_target": {"core_W_typical_strength_Pa": 241316.50526088, "core_W_min_average_strength_Pa": 172368.9323292, "illustrative_normal_at_0p1mm_Pa": 511648.1156583237}, "needed_evidence": "Representative flatwise, shear, interface stiffness/toughness and wrinkle/disbond tests. Relative displacement is not established by the pressure alone.", "factor_to_216_427kg_allowance": null, "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N410 | NFI-021B-CHECK-RESERVE-JOINTS | 030b addition | The correct mass closure still assumes sealed service, zero payload, the chosen weather/water condition, 60 mm strips, 0.2 mm seam adhesive, 1.5 mm core splice and no demonstrated Be/core bond at the nominated film weight. These are explicit inputs, not measured capabilities.; 3M lists .030 and .015 lb/ft² films, with .015 unsupported; nominal areal mass does not qualify the joint. 775.729 kg reserve is spent on the declared condition rather than spare payload. Other service, seal, coating or handling loads need a new budget. | [rpt-ref-444ac46ffbede876f9cd](e22bbb97f4477a6d-NFI.json) |
| N421 | NFI-028-LEGACY-09 | 030b addition | METHOD.md states the 020 optimistic splice mass and does not state a 0.9 face-retention screen. Fixed legacy mass matches on every panel. The stored re-optimised factor, joining mass and core fraction match only after projected joint retention is set to 0.9 times face stress capacity over demand. That screen is in the owner's calculation and is absent from METHOD.md and CARD.md. | [rpt-ref-68dff0680696fe9b4cb4](43ed944cb7138cf7-NFI.json) |
| N423 | NFI-028-HULL-SF | 030b addition | The least modeled factor excludes unmeasured core-bond, seam, thermal and defect modes. Flatwise strength is not reported for AF 163-2U at 0.015 lb/ft². No source in the card qualifies the lightest joining mass. | [rpt-ref-68dff0680696fe9b4cb4](43ed944cb7138cf7-NFI.json) |
| N442 | NFI-028b-unmodelled-bond-seam | 030b addition | Relevant flatwise, imperfection shear, peel/HAZ, local buckling, thermal/cycle and leak allowables are absent. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N491 | NFI-031-JOINTS | 030b addition | P2 seams and bond films are a mass recipe, not checked structural joints. P3 percent joints are an allowance, not strength or rotational stiffness. Folded source joints sized at p0 cannot automatically take a larger float pressure. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N550 | NFI-036-R20-joint | 030b addition | Qualify the inherited R20 0.9 joint efficiency and full-gauge splice model. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N553 | 033-NFI-01 | 030b addition | Installed joints remain unqualified; The six-mode shell result excludes scarf, peel and face/core bond capacities. The additional 10 MPa average-shear screen caps face stress at 300.333 MPa, but is not a qualified allowable. All installed-hull SF values remain null. | [rpt-ref-5b1ba7a48fcb57c8e35e](a4edee0295bc38f3-NFI.json) |
| N559 | 033-NFI-07 | 030b addition | Nominal adhesive and seam inventory; Nominal film is .015 lb/ft2 per face/core interface; scarf film .07 kg/m2, splice gap .5 mm at 500 kg/m3, sealing .002 kg/m for both faces. Nominal primer is zero. No AF163 mass tolerance was independently verified; the inherited +/- .005 statement is unused. | [rpt-ref-5b1ba7a48fcb57c8e35e](a4edee0295bc38f3-NFI.json) |
| N701 | NFI-036-R20-joint | 030b addition | Qualify the inherited R20 0.9 joint efficiency and full-gauge splice model. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |

<a id="R034"></a>
### R034 — primer and surface prep mass

**Original030 unknown:** Be-compatible primer and surface preparation mass is not counted; zero is only a bookkeeping limit.

**Original030 today:** zero primer; 5 g/m2 per line as sensitivity (12.57 kg) [MAINLINE-028]

**Original030 needed:** qualified Be-compatible preparation weighed including core-side coverage [MAINLINE-028]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N234 | NFI-028-13 | 030 retained | {"id": "NFI-028-13", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Primer and surface preparation mass", "today_value": "Zero is a bookkeeping lower limit, not proof of a primer-free process; 5 g/m2 per line is sensitivity", "required_or_budget_target": {"remaining_g_m2_per_line_at_nominal_stock": 0.8702381595960997, "5gsm_added_kg": 12.566370614359172}, "needed_evidence": "Qualify Be-compatible preparation/primer and weigh it including core-side coverage.", "scenario": "af015_scarf_primer5", "scenario_joining_kg": 226.80636845652077, "factor_to_216_427kg_allowance": 1.047957124659267, "mass_reduction_factor_to_fit": 1.047957124659267} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N438 | NFI-028b-primer | 030b addition | Actual primer coverage, surface preparation and mass must be measured; 5 g/m² is a selected sensitivity. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |

<a id="R035"></a>
### R035 — seam step effect on kd

**Original030 unknown:** A seam step is counted only as delta/t_eq; a real seam also breaks face continuity, and no joint failure model exists.

**Original030 today:** kd 0.950, 0.931, 0.869 at steps of 1, 3, 10 mm on P2-E [MAINLINE-015]

**Original030 needed:** a joint model with the sandwich failure cards [MAINLINE-015]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N182 | NFI-015-SEAM-DISCONTINUITY | 030 retained | A seam step is counted only as delta/t_eq. A real seam also breaks face continuity. On P2-E the geometric reading is kd 0.950, 0.931 and 0.869 at steps of 1, 3 and 10 mm. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |

<a id="R036"></a>
### R036 — selective cell-edge adhesive deposition

**Original030 unknown:** Selective cell-edge deposition is lab-only on CFRP/Nomex and not shown on Be/Al.

**Original030 today:** 8-80 g/m2 deposited in CFRP/Nomex experiments [MAINLINE-028]

**Original030 needed:** coverage, fillets, cured mass and mechanical performance after transfer to Be/Al [MAINLINE-028]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N225 | NFI-028-04 | 030 retained | {"id": "NFI-028-04", "status": "OPEN", "tag": "QUESTIONABLE", "technology_state": "in_the_lab", "hull_adoption_state": "PROJECTION", "assumption": "Selective cell-edge deposition", "today_value": "8-80 g/m2 deposited in CFRP/Nomex experiments; not a Be/Al strength limit", "required_or_budget_target": {"assumed_g_m2": 8, "less_aggressive_g_m2": 20}, "needed_evidence": "Measure coverage, fillets, cured mass and mechanical performance after transfer to Be/Al.", "scenario": "lab8_scarf", "scenario_joining_kg": 50.28300529539905, "factor_to_216_427kg_allowance": 0.23233224890109164, "mass_reduction_factor_to_fit": 1, "modeled_component_kg": 20.106192982974676, "component_fraction_of_allowance": 0.0929005139038753} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N439 | NFI-028b-lab-bond | 030b addition | 8 g/m² deposition exists in laboratory work on other materials; transfer to Be/Al core is unqualified. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |

<a id="R037"></a>
### R037 — spherical layout and scarf edges

**Original030 unknown:** No polar-cap or intersection design; the mean-field rectangular layout ignores tessellation, tolerances and rejects.

**Original030 today:** mean-field layout with scarf overlap deducted; spare 2.19 kg [MAINLINE-028]

**Original030 needed:** finished spherical tessellation with fit tolerances, waviness and installation rejects [MAINLINE-028]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N237 | NFI-028-16 | 030 retained | {"id": "NFI-028-16", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Spherical layout and scarf feather edges", "today_value": "Mean-field rectangular layout with scarf overlap deducted; no polar-cap/intersection design", "required_or_budget_target": {"remaining_all_extra_installed_kg_AF_stock": 2.1871470472484873}, "needed_evidence": "Finished spherical tessellation, machining/fit tolerances, edge waviness, intersections, curvature and installation rejects.", "scenario": "af015_scarf", "scenario_joining_kg": 214.2399978421616, "factor_to_216_427kg_allowance": 0.9898943034693449, "mass_reduction_factor_to_fit": 1} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |

## T09 — Margin items

<a id="R038"></a>
### R038 — 019's optimistic reserve embeds 4 m panels and 0.015 lb/ft2 film

**Original030 unknown:** The 019 reserve of 535.95 kg embeds 4 m panels and 0.015 lb/ft2 film; at today panel and film the reserve is larger.

**Original030 today:** reserve 1229.4 kg at today panel and film [MAINLINE-21B]

**Current030b:** Do not mix the old 021b enlarged-panel reserve with 028b's stock-scarf account. 028b fixed non-joint reserve is 411.298944 kg; total excess is recomputed. 033 explicitly reports both actual-bill and retained-floor budgets.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N208 | NFI-021b-RESERVE-HIDES-OPTIMISMS | 030 retained | 019's 535.95 kg reserve embeds 4 m panels and 0.015 lb/ft2 films; at today's panel and film this point's reserve is 1229.4 kg. | [rpt-ref-1080d4f6a1af4cfa8c67](b056cc13a604abed-NFI.json) |
| N443 | NFI-028b-019-reserve | 030b addition | Validate the optimistic service/environment assumptions behind the fixed mass-equivalent reserve. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N558 | 033-NFI-06 | 030b addition | Joining allowance policy; 028 uses actual joining; 027 retains unused 5% structural-mass allowance. Main results use 028, with the floor reported separately. The Q-plus-strength crossing shifts from 16.282 to 40.470 m; R50 six-mode endpoint payload shifts from 89.422 to 74.375 tonnes. | [rpt-ref-5b1ba7a48fcb57c8e35e](a4edee0295bc38f3-NFI.json) |
| N601 | NFI-017b-JOINT-ALLOWANCE | 030b addition | Explicit 028 joining replaces the 5% joint allowance, as 028 did. Under the 5% floor of 019, 021b and 027, sheet size and bond film stop being levers at all. The reserve is 019's optimistic (sealed-service) set, scaled with radius by 027's laws.; A ruling on whether the 5% allowance is a floor once joining is explicit. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |

<a id="R039"></a>
### R039 — design-day climate envelope for lift (site, temperature, pressure, humidity)

**Original030 unknown:** Lift depends on site temperature and pressure; no site is named so the 5% margin has no climate envelope. Hot afternoon and retained water each consume the margin.

**Original030 today:** +25.1 K gives margin -186.3 kg; 0.1 mm retained water 125.6 kg [MAINLINE-016]; optimistic +10 K, +/-1%, 1000 Pa vapour; conservative +25.1 K, +/-2%, 6000 Pa [MAINLINE-027]; optimistic day: 0.1 mm water, +10 K, 1 percent, 1 kPa; conservative needs 4229 kg [MAINLINE-21B]

**Original030 needed:** Named site and season windows; ballast or trim sizing; coating and shedding check [MAINLINE-016]; Station data and operating constraints; recompute mass and max differential-pressure cases [MAINLINE-019]; Site, gas composition, temperatures, weather exposure, water shedding/icing, duration [MAINLINE-027]; site and gas-load measurement (019 follow-ups) [MAINLINE-21B]

**Current030b:** 031 and CHECK-031 confirm altitude is conditional on a weather profile and terrain/clearance requirement. Spending all nominal lift gives below-sea-level hot/low/humid roots. This does not license deleting climate mass from an existing hull.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N058 | NFI-016-CLIMATE | 030 retained | {"NFI_id": "NFI-016-CLIMATE", "rank": 2, "gap": "Lift at the site: dL/L = dp/p - dT/T. A QUESTIONABLE hot summer afternoon at +25.1 K takes the margin to -186.3 kg; 0.1 mm of retained water is 125.6 kg, 51 percent of the margin; 1 mm is 1257 kg. No site is named anywhere in the mainline, so the 5 percent margin has no climate envelope.", "direction": "Name the operating site and season windows; size a ballast or trim system for the hot-day deficit; require a hydrophobic coating and a shedding check before flight; weigh the hull after rain.", "effect": "Margin negative at the hot extreme without these; climbing does not recover it (lift falls about 9.4 percent per km)."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |
| N068 | NFI-019-SITE | 030 retained | No operating site, measured temperature/pressure/humidity envelope or cold-case minimum is specified. The selected weather cases are assumptions, not site return-period limits. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N108 | NFI-027-ENVIRONMENT | 030 retained | The optimistic +10 K/±1%/1000 Pa vapour and conservative +25.1 K/±2%/6000 Pa cases are owner scenarios, not a site distribution. Water is a full-area equivalent retained film, contamination an area load. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N210 | NFI-021b-CLIMATE-SERVICE | 030 retained | The fixed reserve items are 019's optimistic sealed-service day (0.1 mm water, +10 K, 1 percent, 1 kPa); 019's conservative day needs 4229 kg. | [rpt-ref-1080d4f6a1af4cfa8c67](b056cc13a604abed-NFI.json) |
| N408 | NFI-021B-CHECK-PRESSURE | 030b addition | The printed point scores the COMMON reference pressure. The inherited service package includes a 1% pressure swing; its high-pressure structural corner is separate from the low-pressure buoyancy corner.; At +1% external pressure on the same geometry and needed values, global and wrinkle SF are 0.990099, compression 0.990103. This does not contradict the reference-case arithmetic but prevents treating that exact point as covering the complete service package. | [rpt-ref-444ac46ffbede876f9cd](e22bbb97f4477a6d-NFI.json) |
| N470 | NFI-015-CHECK-HYDROSTATIC | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N560 | 033-NFI-08 | 030b addition | Weather and systems reserve laws; The 019 optimistic temperature, pressure, humidity and internal-air losses scale with volume; .1 mm water and contamination scale with area; 100 kg systems remains reserved. Primary structural pressure is +1%; pressure at the reference value alone flips the R10 screen result to positive in the floor sensitivity. | [rpt-ref-5b1ba7a48fcb57c8e35e](a4edee0295bc38f3-NFI.json) |

<a id="R040"></a>
### R040 — float margin and payload: 0%, 5%, 10.96% and 86.49% budgets

**Original030 unknown:** Reserve is the explicit charge above baseline floors, not statistical contingency or free payload; climate plus internal air alone exceeds a 5% margin and larger radius alone cannot fix it.

**Original030 today:** payload reserve 5% of lift; total mass 95% of lift [CHECK-MAINLINE-09C5]; 5% main and conservative; 0% optimistic [MAINLINE-009]; payload 0 kg; +100 kg case supplied [MAINLINE-019]; climate plus internal air alone: 5.7396% optimistic, 13.1183% conservative [MAINLINE-027]

**Original030 needed:** Reword to state payload 5% and total mass 95% [CHECK-MAINLINE-09C5]; Newer equal-margin geometry input [MAINLINE-009]; Set payload and float reserve separately [MAINLINE-019]; Specified residual reserve added to the budget [MAINLINE-019]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N003 | NFI-PAYLOAD-SENTENCE | 030 retained | {"id": "NFI-PAYLOAD-SENTENCE", "type": "text_mismatch", "row": "CARD.md opening", "field": "mass_fraction", "reported": "The mass is 5 percent of lift", "reported_fraction": 0.05, "independent_total_mass_fraction": 0.95, "independent_payload_fraction": 0.05, "proposed_fix": "Say payload reserve is 5% of lift and total mass is 95%.", "stops_owner": false} | [rpt-1228-mainline009c5-independent-check-1019](4662757b4d50b2d1-NFI.json) |
| N056 | NFI-MASS | 030 retained | {"id": "NFI-MASS", "value": "payload margin", "optimistic": 0.0, "main_point": 0.05, "conservative": 0.05, "factor": "zero margin raises the structural budget by (lift-100)/(0.95*lift-100), about 5 percent, which does not close a wrinkling gap of several times", "source": "CARD-009 default, kept because MAINLINE-006's P2-E knee is that same 0 to 5 percent step.", "direction": "MAINLINE-012's equal-margin geometry, when that card is the newer input."} | [rpt-ref-d5b4aaa267b71d82fe25](b9cd9c3b294887e6-NFI.json) |
| N069 | NFI-019-PAYLOAD | 030 retained | Zero payload is an unladen demonstrator choice. The former 009c5 payload/margin number cannot simultaneously be mission payload and contingency. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N080 | NFI-019-RESERVE | 030 retained | The summed margin is consumed at the declared design condition; it is not an additional residual flight contingency or positive safety factor. The cases do not form a statistical confidence interval. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N115 | NFI-027-RESERVE-MEANING | 030 retained | Reserve is the explicit charge above retained baseline system/joint floors, not statistical contingency or free payload. Climate plus internal air alone is 5.7396% optimistic and 13.1183% conservative. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N196 | NFI-021-MARGIN | 030 retained | The 5 percent margin stands until 019 files; every number here moves with it. | [rpt-ref-769a7442efd5a04681e9](fae865c7f039491f-NFI.json) |
| N212 | NFI-021b-MARGIN | 030 retained | No payload: 019's unladen case. 019's +100 kg payload sensitivity raises the reserve to 637.85 kg. | [rpt-ref-1080d4f6a1af4cfa8c67](b056cc13a604abed-NFI.json) |
| N486 | NFI-031-RESERVE-MEANING | 030b addition | Climate is absent mass; water, contamination and gas are carried mass. 021 rev1 has a 5% placeholder, no separate climate rows or explicit seam budget. Recasting that placeholder is a new budget assumption. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N598 | NFI-022D-MASS | 030b addition | The inherited mass contract omits independent barrier/seam/coating and some joint process masses; sag volume is first-order. Two reserve choices are carried assumptions, not an audited vehicle budget. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |
| N624 | NFI-026B-10 | 030b addition | Source-dependent mass conventions; Compare each case with its stated source allowances. Do not treat the three masses as an optimization under one common budget. | [rpt-ref-8befdd4c89803adc44a8](d90bde67ada2ca77-NFI.json) |
| N650 | NFI-026B-10 | 030b addition | Source-dependent mass conventions; Compare each case with its stated source allowances. Do not treat the three masses as an optimization under one common budget. | [rpt-ref-4a20323946ecafd56a6b](d90bde67ada2ca77-NFI.json) |

<a id="R041"></a>
### R041 — retained water and contamination

**Original030 unknown:** Water films are equivalent retained thickness, not rainfall; absorbed core moisture, corrosion, thermal gradients and derating are unquantified; 320 K gas temperature is an acceptance condition.

**Original030 today:** gas temperature at most 320 K (acceptance condition) [MAINLINE-019]

**Original030 needed:** Measured water shedding, conditioning, absorbed moisture and thermal response [MAINLINE-019]; Exterior humidity case and hull water rate [MAINLINE-024]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N078 | NFI-019-ENVIRONMENT | 030 retained | Water films are equivalent retained thickness over the whole area, not rainfall depths. Moisture absorbed in core, corrosion, thermal gradients and property derating are not separately quantified here. Gas temperature <=320 K is an acceptance condition, not a thermal prediction. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N094 | NFI-HULL-HUMIDITY | 030 retained | The case has no exterior humidity. Water loads stay at the sheet condition and are not a hull rate. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |

<a id="R042"></a>
### R042 — systems and allowance masses are owner allowances (100 kg P2, 50 kg P3, pump, battery)

**Original030 unknown:** Battery estimate assumes packaged energy density, usable fraction and conversion; catalog pump data are not installed duty measurements and the smaller pump misses the hot-gas flow.

**Original030 today:** joint fraction 5%; systems 100 kg; residual gas zero [MAINLINE-007]; 150 Wh/kg packaged, 80% usable, 90% conversion [MAINLINE-019]; optimistic case retains 70 kg unused system allowance [MAINLINE-019]; 100 kg system floor (70 kg above passive package); 0.1 kg/m2 sensitivity [MAINLINE-027]

**Original030 needed:** A parts list [MAINLINE-007]; Measured pump curve, power, cooling, conductance and duty cycle; qualified power package [MAINLINE-019]; Explicit allocation of each needed item [MAINLINE-019]; Itemised additional vehicle masses [MAINLINE-027]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N035 | NFI-MASS | 030 retained | {"NFI_id": "NFI-MASS", "gap": "Joint fraction 5 percent, systems 100 kg, and zero residual gas are unchanged inherited numbers.", "direction": "Replace them with a parts list.", "effect": "They set the structural mass on the ceiling."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N073 | NFI-019-SYSTEMS | 030 retained | The battery estimate assumes 150 Wh/kg packaged, 80% usable and 90% conversion. Catalog pump speed/power are not installed duty measurements; the smaller SV220B cannot meet the stated hot-gas flow at the fixed pressure cap. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N079 | NFI-019-OTHER-MASS | 030 retained | This closes the card's explicit budget, not every aircraft subsystem. Separate coating, hardpoint/spreader, mooring attachment, handling, navigation or propulsion masses are not individually sized. The optimistic case retains 70 kg of unused system allowance; the active case has no such spare allowance. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N109 | NFI-027-OTHER-MASS | 030 retained | Extra coatings, lightning protection, mooring, hardpoints, navigation and propulsion are not independently sized. P2 retains a 100 kg system floor, including 70 kg above the passive package, but this is not a complete vehicle mass model. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N145 | NFI-010-SYSTEMS | 030 retained | {"NFI_id": "NFI-010-SYSTEMS", "gap": "Systems at 100 kg per sphere in a cluster is the mass rule read literally. A shared-systems cluster would pay it once.", "direction": "Name the systems architecture before crediting any cluster margin.", "effect": "Cluster margins improve by up to (n-1) x 100 kg of lift; SFs unchanged."} | [rpt-ref-58b2bed18db2449100f2](21991360c704a696-NFI.json) |
| N250 | NFI-MASS | 030 retained | {"NFI_id": "NFI-MASS", "linked_inputs_or_points": "joints nodes systems", "questionable_assumption_or_gap": "Allowances are round owner numbers.", "direction_of_further_investigation": "Replace with a parts list.", "how_it_affects_margin_or_SF": "Each kilogram reduces margin by 1/lift."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |
| N260 | NFI-MASS | 030 retained | {"NFI_id": "NFI-MASS", "gap": "Joint fractions, node mass and payload allowances are unchanged owner numbers.", "direction": "Replace with a parts list.", "effect": "They set how much margin the allocation can spend."} | [rpt-mainline002-grok-strength-card-1019](b155c07e690eaa66-NFI.json) |
| N268 | NFI-MASS | 030 retained | {"NFI_id": "NFI-MASS", "gap": "Joint fraction, payload allowance and zero gas are unchanged inherited numbers.", "direction": "Replace them with a parts list.", "effect": "They set the structural mass on the ceiling."} | [rpt-mainline003-grok-p2-targets-1019](2090c6e1f4ca8afb-NFI.json) |
| N413 | NFI-CHK024-PUMP-MASS | 030b addition | The scan has 50 kg for all systems. The inherited pump alone is 150-400 kg, not debited from tube mass. Reallocating all 50 kg leaves 100-350 kg unbooked; keeping the original systems adds the full pump. No getter capacity is sourced. | [rpt-ref-7d6892c4e55be16ad523](1b8584393478c427-NFI.json) |
| N586 | NFI-034-MASS-ALLOCATION | 030b addition | Both current lead models carry 100 kg systems. Identified sealed hardware is 30-50 kg. Zylon barrier and previously omitted joint adhesive may be funded from remaining allocation only by explicit reallocation; other installed hardware is unresolved. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |

## T10 — Vacuum holding

<a id="R043"></a>
### R043 — getter capacity nitrogen air

**Original030 unknown:** SAES offers room-temperature nitrogen sorption, so the blanket denial and unsourced N2 capacity band cannot support the mass result; all-air getter lifetime incl. noble gases is unsized.

**Original030 today:** pump band 150-400 kg (catalog class) [MAINLINE-024]

**Original030 needed:** Measured species loads, sorption speeds and capacities with activation conditions [MAINLINE-019]; Getter capacity against gas load [MAINLINE-024]

**Current030b:** 034 distinguishes dry-gas getter capacity from water sorbents. Nitrogen can be gettered in some systems; no matched complete-hull sizing result is admitted.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N076 | NFI-019-GETTERS | 030 retained | SAES explicitly offers room-temperature nitrogen sorption. The unfinished script's blanket denial and unsourced N2 capacity band cannot support its mass result. All-air getter lifetime including noble gases remains unsized. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N096 | NFI-GETTER | 030 retained | No getter capacity is stated. The pump band is the 150 to 400 kg catalog class, not scaled to the gas load. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N583 | NFI-034-GETTER | 030b addition | BASF capacity is a humid-equilibrium number; the 10 wt% usable vacuum capacity is assumed. The SAES UHV capacity illustration is not a mixed-gas rough-vacuum recommendation. COMBO removes N2 at room temperature, but the opened page supplies no sizing capacity. Getter-retained external gas still adds vehicle mass. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |

<a id="R044"></a>
### R044 — vacuum-holding route mass and power (sealed service vs onboard pump)

**Original030 unknown:** Holding internal pressure at a 1000 Pa ceiling needs a pump whose mass and power are uncertain and can exceed the float margin; the ceiling itself is an owner assumption.

**Original030 today:** 46.3 L/s; 527-844 W; 150-400 kg pump set; commissioning pump-down 506 kWh [MAINLINE-016]; pumps needed 1,3,7,23,103 at R 10,15,20,30,50 m [MAINLINE-027]; 30 kg fixed [MAINLINE-027]; perfect vacuum (zero residual) assumed [rpt-mainline-grok-estimates-card-1019]

**Original030 needed:** Real Roots or screw pump spec at this duty; operational ceiling set from leak budget [MAINLINE-016]; Measured leak/outgas and installed speed at pressure; measured gas-load decomposition [MAINLINE-027]; 24 h hold demonstration at temperature envelope; supporting hardware mass [MAINLINE-027]; State a hold pressure and the pump mass. [rpt-mainline-grok-estimates-card-1019]

**Current030b:** 034 selects ground evacuation plus sealed 24-hour service at an estimated 30–50 kg, retaining 100 kg systems. Longer gas-only lives do not establish electrical endurance; the assumed 10 kg power package lasts at most nine days at 5 W.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N060 | NFI-016-PUMP | 030 retained | {"NFI_id": "NFI-016-PUMP", "rank": 4, "gap": "Holding p_int at a 1000 Pa ceiling takes 46.3 L/s there, 527 to 844 W real, and a QUESTIONABLE 150 to 400 kg pump set: 61 to 164 percent of the whole 244.472 kg float margin. The ceiling itself is an owner assumption; commissioning pump-down is 506 kWh.", "direction": "Shop a real Roots or screw pump specification at this duty (mass, power, intake pressure curve); set the operational p_int ceiling from the leak budget; consider distributed smaller pumps or a ground-only pump.", "effect": "Trades directly against the margin; can exceed it entirely at the conservative end."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |
| N106 | NFI-027-PUMP-SCALE | 030 retained | One SV300B catalog pumping speed is insufficient for 019's volume-proportional 1%/day gas load above R = 10. Modular counting gives 1,3,7,23,103 pumps at 10,15,20,30,50 m, with full rated power continuously budgeted. Installed conductance/manifolds are not sized. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N107 | NFI-027-PASSIVE-SERVICE | 030 retained | The 30 kg sealed-service package is held fixed. Its normalized gas-load limit grows with volume; this does not prove its seals, plumbing, monitoring or ground evacuation hardware scale at fixed mass. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N251 | NFI-GAS | 030 retained | {"NFI_id": "NFI-GAS", "linked_inputs_or_points": "I-PINT and gas masses", "questionable_assumption_or_gap": "Perfect vacuum.", "direction_of_further_investigation": "State a hold pressure and the pump mass.", "how_it_affects_margin_or_SF": "Residual gas adds mass and reduces differential pressure."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |
| N496 | NFI-031-SYSTEMS-GAS | 030b addition | The calculation retains optimistic 019 nonclimate loads and the full 100kg system floor even on conservative weather. This isolates weather; it does not qualify the conservative pump/battery/rain/contamination hardware package. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N584 | NFI-034-PUMP-AND-CONDUCTANCE | 030b addition | KNF inlet speed is read from the low-pressure curve, not its STP delivery rating. Installed speed is assumed 75% of nominal. E2M28 motor 750 W is mechanical; 1000 W electrical is an assumption. One E2M28 is 2.3% short of the Kapton hot constant-source envelope at the assumed installation factor. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N585 | NFI-034-POWER-ENDURANCE | 030b addition | 30 kg sealed hardware includes an assumed 10 kg power package. Even if all ten kilograms were battery, the stated pack factors support five-watt monitoring for only nine days. Gas-only lifetimes are not autonomous mission endurance. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N668 | NFI-038-SYSTEM_MASS | 030b addition | Sealed life and pumping hardware are not determined by a helium leak rate | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |

<a id="R045"></a>
### R045 — whole-hull gas load: leaks, permeation, outgassing (needs measurement)

**Original030 unknown:** Face permeation is negligible at the present budget; CFRP figure comes from a helium band divided by 50 for air and no measured air permeance exists.

**Original030 today:** 0.5-3% moisture = 11.0-66.2 kg water = 347-2079 Pa vs 954.6 Pa ceiling [MAINLINE-016]; budget equals 2.48 mm2 choked hole or 4.25 mm2 molecular aperture; 46.28 Pa m3/s [MAINLINE-016]; CFRP 5.4e-5 percent of the 1%/day budget [MAINLINE-016]; 30-50 kg passive package (estimate) [MAINLINE-019]

**Original030 needed:** Water content of the core lot; bake-out and dry-gas backfill procedure [MAINLINE-016]; Operational leak spec with margin; per-panel seam leak testing; sensitive pressure sensor [MAINLINE-016]; Measured air permeance of the chosen face and seam coupon [MAINLINE-016]; Measure gas load through a representative panel/valve assembly then the hull; Qref at most 40.71949 Pa m3/s for 24 h from 10 Pa [MAINLINE-019]

**Current030b:** 034 requires measured assembly leakage, conditioning and vent paths. Unvented cells/bores retain substantial air. Outgassing changes phase of already carried mass; ingress adds mass; getters retain it.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N061 | NFI-016-BAKEOUT | 030 retained | {"NFI_id": "NFI-016-BAKEOUT", "rank": 5, "gap": "Resident moisture 0.5 to 3 percent of the 2208.2 kg PVC core is 11.0 to 66.2 kg of water, worth 347 to 2079 Pa inside if released, against the 954.6 Pa one-percent-per-day ceiling. Steady outgassing itself is only 0.00 to 0.03 percent of the leak budget.", "direction": "Measure water content of the core lot; specify a bake-out and vent procedure at commissioning with a dry-gas backfill during assembly.", "effect": "Without bake-out the moisture alone can exceed the one-percent ceiling after release."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |
| N062 | NFI-016-LEAKSPEC | 030 retained | {"NFI_id": "NFI-016-LEAKSPEC", "rank": 6, "gap": "The 1 percent-per-day budget equals a 2.48 mm2 choked hole or 4.25 mm2 molecular aperture: vacuum integrity at this budget is a discrete-defect and detection problem, not a material one. No leak specification, no detection threshold, no in-service pressure telemetry is defined.", "direction": "Set an operational leak spec well inside 46.28 Pa m3/s with margin; specify seam leak testing per panel at assembly and a pressure sensor resolution able to see a fraction of the budget.", "effect": "Detection latency decides whether the trim pump is a convenience or a life-limit."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |
| N067 | NFI-016-PERM | 030 retained | {"NFI_id": "NFI-016-PERM", "rank": 11, "gap": "Face permeation is nil against the 1-percent budget: metals and monolithic SiC are gas barriers; CFRP epoxy laminate passes 5.4e-5 percent of budget on a QUESTIONABLE NASA composite-cryotank helium band divided by 50 for air. No measured air permeance exists for the actual faces.", "direction": "Measure air permeance of the chosen face and seam coupon directly; matters only if the leak budget is tightened far below 1 percent per day.", "effect": "None at the current budget; decisive if the budget tightens by four or more orders."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |
| N070 | NFI-019-LEAK | 030 retained | Whole-hull leakage, trapped core gas, moisture desorption and outgassing have not been measured. The 30-50 kg passive package is a bill-of-mass estimate, not demonstrated vacuum retention. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N233 | NFI-028-12 | 030 retained | {"id": "NFI-028-12", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Sealant and pressure integrity", "today_value": "Selected 0.002 kg/m TOTAL for both face seams; leak-tested geometry unknown", "required_or_budget_target": "Maintain the inherited evacuated condition and service leak allocation.", "needed_evidence": "Measure permeability, pinholes and seam leak rate over temperature/pressure cycles; add any required barrier mass.", "scenario": "af015_scarf", "scenario_joining_kg": 214.2399978421616, "factor_to_216_427kg_allowance": 0.9898943034693449, "mass_reduction_factor_to_fit": 1, "modeled_component_kg": 5.694923693261571, "component_fraction_of_allowance": 0.026313352219156993} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N572 | NFI-034-LEAK-RATES | 030b addition | No full-hull or seam/node leak rate is measured. The 1e-5/1e-3/0.1 mbar L/s per metre and per node values are scenarios, with a separate port allowance. They span four decades but are not bounds. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N573 | NFI-034-SOURCE-TO-SERVICE | 030b addition | 500 m fixes nominal pressure, not humidity or membrane temperature. Water rates are source-condition values mapped to a chosen 1 kPa driving partial pressure. Temperature dependence and humidity-gradient dependence are not measured. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N574 | NFI-034-TML-NOT-RATE | 030b addition | NASA E595 uses 125 C for 24 h. TML is neither kg/day at 284.9 K nor a certified finite flight inventory. Historical cures/lots and several material/gauge proxies differ. CVCM is a subset, not added to TML. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N575 | NFI-034-CONDITIONING | 030b addition | Reference calculations assume 90% of the chosen release inventory was removed and the residue releases exponentially with one-day time constant. Neither fraction nor kinetics is demonstrated. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N576 | NFI-034-CORE-AND-TUBE-VENTING | 030b addition | Unvented P2 honeycomb would retain about 43.388 kg of ambient air. P3 tube bores would retain about 88.153/76.110 kg. Base cases require these spaces to share the evacuation path. Trapped gas is onboard mass even before it leaks into the main cavity. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N577 | NFI-034-P2-PERMEATION-PATH | 030b addition | Intact Be bulk ambient-gas permeation is set to zero in the screen, not measured. AF full-area bonds are behind Be and do not see the full exterior-to-interior gradient. The outer 30:1 scarf is screened at an assumed 10 Barrer; its adhesive is the 028 70 g/m2 route, not silently replaced with AF163. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N578 | NFI-034-P3-RESIN-AND-SURFACES | 030b addition | SiC tubes remain SiC in both 022c rows; CFRP is only the end wrap. The wrap outgassing proxy uses a different graphite/epoxy. A 0.1 g/m2 SiC surface inventory and 1 wt% unspecified attachment/seal inventories are assumptions. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N587 | NFI-034-PHASE-VERSUS-LIFT | 030b addition | Desorbed material was already aboard: gas-phase inventory consumes a pressure allowance without adding the same mass again to the vehicle. Net external ingress adds mass. Passive getters retain it; pumps can expel it. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N666 | NFI-038-TRAPPED_GAS | 030b addition | Every core cell/tube bore must be evacuated or charged | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N667 | NFI-038-VACUUM_SPECIES | 030b addition | Pressure, free gas and added mass are different constraints | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |

## T11 — Thermal

<a id="R046"></a>
### R046 — ground-side thermal environment

**Original030 unknown:** Thermal balance averages sky and ground radiation; a hot apron, heat island or hangar is not bounded and the core-limit conclusion could invert.

**Original030 today:** no-convection bound 313.5 K vs H35 limit 343-353 K [MAINLINE-016]

**Original030 needed:** Re-run for named ground conditions; measure emissivity of the face finish [MAINLINE-016]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N065 | NFI-016-THERMENV | 030 retained | {"NFI_id": "NFI-016-THERMENV", "rank": 9, "gap": "The thermal balance averages sky (260 to 275 K) and ground radiation and gives a no-convection bound of 313.5 K, under the QUESTIONABLE H35 service limit 343 to 353 K; but a hot apron, heat island, or hangar radiates from the ground side and is not bounded here.", "direction": "Re-run the balance for named ground conditions (asphalt apron, hangar wall); measure emissivity of the actual face finish.", "effect": "The core-limit conclusion could invert on a hot-ground site."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |

<a id="R047"></a>
### R047 — thermal mismatch, cycling and fatigue of bonded faces and joints

**Original030 unknown:** Property loss at temperature is datasheet-class only; no derate curves pinned and daily-cycle fatigue of core and adhesive is unquantified.

**Original030 today:** SiC 4.5e-6 vs PVC 60e-6 per K; shear 283 kPa per 30 K; SF 1.41-1.94 at 30 K, 0.71-0.97 at 60 K [MAINLINE-016]; scored modes use room-temperature properties; H35 derates above 50-60 C [MAINLINE-016]

**Original030 needed:** Bond-line and core shear coupon under daily thermal cycling; pinned H35 shear strength and modulus [MAINLINE-016]; Derate curves for core and adhesive against the measured daily band [MAINLINE-016]; effective CTE, temperature histories, restraint and fatigue under compressive mean load; test 10,958 daily cycles for 30 years [MAINLINE-020]; CTE residual stress, polymer heat exposure, corrosion, fatigue, final weld/braze access [MAINLINE-028]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N059 | NFI-016-CTE | 030 retained | {"NFI_id": "NFI-016-CTE", "rank": 3, "gap": "CTE mismatch SiC 4.5e-6 vs PVC 60e-6 per K drives sandwich shear-lag at 283 kPa per 30 K face-core difference (567 kPa at 60 K), against a QUESTIONABLE H35 shear strength of 0.40 to 0.55 MPa: one-off SF 1.41 to 1.94 at 30 K, 0.71 to 0.97 at 60 K, cycled daily. Not one of the five scored modes; no fatigue law.", "direction": "Bond-line and core shear coupon under thermal cycling over the full daily band; pin DIAB H35 shear strength and modulus; add the mismatch mode to the scored set.", "effect": "A new structural failure mode at the 009 point, unquantified for the life of the hull."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |
| N066 | NFI-016-PROPTEMP | 030 retained | {"NFI_id": "NFI-016-PROPTEMP", "rank": 10, "gap": "Property loss at temperature is datasheet-class only: H35 derates above 50 to 60 C, SiC is flat far above this range, and the aluminium family derates above about 150 C, not reached. No derate curves are pinned and the daily cycle fatigue of core and adhesive is not quantified.", "direction": "Pin derate curves for the core and adhesive against the measured daily band; couple to NFI-016-CTE.", "effect": "The scored five modes use room-temperature properties for a cycling structure."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |
| N188 | NFI-020-THERMAL-FATIGUE | 030 retained | Daily thermal-cycle life of the pressure-loaded Be/HRH10 joint is UNKNOWN.; Measure effective directional core/face/adhesive expansion, service temperature histories, restraint and fatigue under representative compressive mean load. Test the assumed 10,958 daily cycles if a 30-year target is adopted. | [rpt-ref-3e02218a03708a878faa](72e91c4df6df4236-NFI.json) |
| N239 | NFI-028-18 | 030 retained | {"id": "NFI-028-18", "status": "OPEN", "tag": "PROJECTION", "technology_state": "PROJECTION", "hull_adoption_state": "PROJECTION", "assumption": "Thermal, cyclic and assembly compatibility", "today_value": "No post-form/post-join envelope established for the selected route", "required_or_budget_target": "Maintain the adopted properties and leak/shape limits through assembly and service.", "needed_evidence": "CTE residual stress, polymer heat exposure, corrosion, fatigue and final weld/braze access; do not equate a furnace coupon with a closed 20 m hull.", "factor_to_216_427kg_allowance": null, "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."} | [rpt-ref-2519e14e5d71b9eb18f3](4a6f636dbfa17be3-NFI.json) |
| N551 | NFI-036-environment | 030b addition | Cover mission temperature and cycling in the strength basis. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N702 | NFI-036-environment | 030b addition | Cover mission temperature and cycling in the strength basis. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |

## T12 — Handling, cost and supply

<a id="R048"></a>
### R048 — Be cost, supply and controlled processing

**Original030 unknown:** Finished-sheet capacity, current S200F/SR200 prices and fabrication yields are unknown; the multipliers are owner stress cases.

**Original030 today:** assumed S200F 4800-9600 USD/kg, SR200 9600-24000 USD/kg, yield 0.85-0.5 [MAINLINE-020]; owner allowance 10 to 30 percent of conversion cost [MAINLINE-020]

**Original030 needed:** grade/gauge/size-specific quotes, lead time, rolling capacity, scrap recovery, panel yield [MAINLINE-020]; contractor quote pricing the conversion and capital separately [MAINLINE-020]

**Current030b:** CHECK-020 adds omitted Be doublers to the historical supply/cost comparison: its stated stock totals become $44.70m/$267.10m under those dated assumptions. No fresh price or purchase recommendation is made here.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N190 | NFI-020-SUPPLY-QUOTE-YIELD | 030 retained | Finished-sheet capacity, current S200F/SR200 prices and fabrication yields are UNKNOWN.; Obtain grade/gauge/size-specific lot quotations, lead time, rolling capacity, scrap recovery and installed-panel yield. No vendor contact or purchase was made in this task. | [rpt-ref-3e02218a03708a878faa](72e91c4df6df4236-NFI.json) |
| N191 | NFI-020-CONTROLLED-PROCESS-COST | 030 retained | Controlled fabrication costs are an explicit open procurement item.; Specify jurisdiction and process steps; get a contractor quote including enclosure/extraction or wet processing, exposure assessment, waste/hygiene and surveillance obligations. Price F and C separately. | [rpt-ref-3e02218a03708a878faa](72e91c4df6df4236-NFI.json) |
| N403 | NFI-020C-DOUBLER-BERYLLIUM | 030b addition | Section 3's splice doublers are full-gauge Be, but section 1 buys and prices only the faces. | [rpt-ref-35706d7a2ae7e951590b](17d1e17bba0e3797-NFI.json) |

<a id="R049"></a>
### R049 — brittle face buildability SiC Be

**Original030 unknown:** SiC and beryllium rank only on compressive membrane modes; flexure, fracture toughness, toxicity, joining and ductility are outside the formulas.

**Original030 today:** SiC flexural strength about 380 MPa [MAINLINE-008]

**Original030 needed:** fracture and joining assessment before either is carried as a face [MAINLINE-008]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N134 | NFI-008-BRITTLE-FACES | 030 retained | SiC and beryllium rank on compressive membrane modes only. SiC flexural strength (~380 MPa) and fracture toughness, and beryllium toxicity, joining and low ductility, are outside both formulas. | [rpt-ref-45da79edf548b064b228](6284193a78be0578-NFI.json) |

<a id="R050"></a>
### R050 — ground handling and dent survey

**Original030 unknown:** Growth of diameter from 20 to 100 m raises ground area and wind force 25-fold and overturning moment 125-fold; point attachments, transport, launch and landing fall outside uniform-pressure modes.

**Original030 today:** core-safe pad pressure target 250 kPa or less; hull 4645 kg [MAINLINE-016]; diameter 20 to 100 m; wind force x25; overturning moment x125 [MAINLINE-027]

**Original030 needed:** Cradle geometry, pad pressure and post-move imperfection survey [MAINLINE-016]; Design and weigh handling and anchoring equipment; verify concentrated and asymmetric loads [MAINLINE-027]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N064 | NFI-016-HANDLE | 030 retained | {"NFI_id": "NFI-016-HANDLE", "rank": 8, "gap": "Ground handling of a 4645 kg, 20 m vacuum sphere has no concept, cradle, or transport plan; core-safe pad pressure target is 250 kPa or less, and any handling dent is an imperfection feeding the already-severe 0.20 knockdown.", "direction": "Specify cradle geometry and pad pressure; define a dimensional inspection and imperfection survey after every move, tied to the knockdown basis.", "effect": "A dent below the survey threshold enters the buckling knockdown unmeasured."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |
| N110 | NFI-027-HANDLING | 030 retained | Diameters grow 20→100 m, projected ground area and wind force at fixed speed grow 25-fold, characteristic overturning moment 125-fold. Point attachments, transport, launch and landing are outside uniform-pressure modes. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |

## T13 — P3 member force

<a id="R051"></a>
### R051 — P3 member force: pRs/(2*sqrt3) on the equilateral frame (FIX-A), two-way 2V-4 members

**Original030 unknown:** P3 assumes tributary width equals spacing, pinned members, a real-valued equal triangulation, and ignores tube crippling; Euler pressure scales with I, E and 1/s^3.

**Original030 today:** N = pRs/2; member-end load 974 kN at s 2.04 m (statics: 562 kN) [CHECK-011b]; equilateral N = 562166 N at s 2.04 m (two-way 973701 N) [MAINLINE-023]

**Original030 needed:** N = pRs/(2*sqrt3) on the equilateral frame, or a true two-way frame, then re-optimise [CHECK-011b]; none; 022b rescales [MAINLINE-023]; Integer geodesic, end fixity, imperfection knockdown and local crippling. [rpt-mainline-grok-estimates-card-1019]; Integer mesh, end fixity and crippling. [MAINLINE-002]

**Current030b:** Equilateral membrane force remains pRs/(2sqrt(3)). 026 additionally corrects tributary line load to ps/(2sqrt(3)); CHECK-027 flags the inherited two-way member-force continuation. Grid and local loading must remain explicit.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N018 | NFI-CHK011B-FORCE | 030 retained | The card's member force N = pRs/2 is the two-way arch resultant, but the frame it counts has M = 3V-6 members of length s. Statics fix their mean compression at 4*pi*R^3*p/(M*s) = pRs/(2*sqrt3) exactly (virial identity). The card's own Et=(2/sqrt3)EA/s with nu=1/3 gives the same strain. Geodesic trusses of 162 and 362 nodes solved by statics (rank complete, residual 6e-15) give mean C/(pRl/(2*sqrt3)) = 1.017 and 1.007, with a maximum of 600 kN at mean l 2.0 m. Each member carries 0.289*s^2 of film, not s^2/2. The force is inherited from MAINLINE-002's P3 rule (COMMON.md). Yield, Euler, local and Perry are sqrt3-conservative at a given tube. Re-optimised, SiC on the equilateral grid at k 0.2 is 1.408 and 6061 is 0.339. The member-end load at s 2.04 m is 562 kN, not 974 kN (022, 023). | [rpt-check011b-opus-1020](610aec93220adcc1-NFI.json) |
| N213 | NFI-023-EQUILIBRIUM-FORCE | 030 retained | The first filing sized the equilateral grid at the two-way force. Yield, Euler, local and Perry were low by sqrt(3). Global was not. The sleeve total at equilibrium, with the radius held, does not depend on s. | [rpt-ref-a4768f77870336c8cdbb](30c19a9c27a07c4b-NFI.json) |
| N247 | NFI-FRAME | 030 retained | {"NFI_id": "NFI-FRAME", "linked_inputs_or_points": "P3", "questionable_assumption_or_gap": "Tributary width equals spacing, members are pinned, mesh is a real-valued equal triangulation, tube crippling ignored.", "direction_of_further_investigation": "Integer geodesic, end fixity, imperfection knockdown and local crippling.", "how_it_affects_margin_or_SF": "Euler pressure scales with I and E and inversely with s^3. Mass scales with edge count and area."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |
| N257 | NFI-FRAME | 030 retained | {"NFI_id": "NFI-FRAME", "gap": "Pinned Euler, tributary width equal to spacing, and no local crippling.", "direction": "Integer mesh, end fixity and crippling.", "effect": "Euler pressure scales with I. Section yield scales with area. Crippling could govern first."} | [rpt-mainline002-grok-strength-card-1019](b155c07e690eaa66-NFI.json) |
| N374 | NFI-025-EQUILIBRIUM | 030b addition | Uniform equilateral force correction is established for the stated continuum; full discrete topology and coupled film/load collection remain unresolved.; Amendment ord-admiral-rr2-mainline025-demand-082gpa-1020 and its pinned note confirm N=pRs/(2sqrt3). Both demands are scored in fixed and reoptimized principal tables. Extra arc rise must not reduce this equilibrium force; bending about the actual thrust line must be evaluated. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N389 | NFI-CHECK-027-MEMBER-FORCE | 030b addition | The P3 continuation holds the 011b axial force p*R*s/2. On an equilateral grid the member force is p*R*s/(2*sqrt(3)). Yield, Euler, local and Perry are scored on the larger force. Global and film do not use it. The bay and radius bounds themselves are held. | [rpt-ref-7b45cb6b4d7f92067f8b](dbd1b2dcf58882f2-CHECK-NFI.json) |
| N391 | NFI-023-CHECK-OLD-FORCE | 030b addition | {"id": "NFI-023-CHECK-OLD-FORCE", "status": "resolved_by_load_fix", "non_blocking": true, "field": "first filing member force", "reported": "973700.54672178N, pRs/2, applied to triangulated member count.", "check": {"equilateral_N": 562166.2727599056, "old_N": 973700.5467217801, "fixed_geometry_factors": {"yield": 1.732050807568877, "euler": 1.7320508075688772, "local": 1.732050807568877, "film": 1.0, "perry": 1.7320508075688772, "global": 1.0}}, "evidence": ["independent global-cut/node/tributary derivations", "RESULTS.json"], "next": "Carry the corrected force. The initial numbers are reproduced solely as superseded-load calculations."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N499 | NFI-026-01 | 030b addition | 011b local-member tributary share differs from equal triangular cell transfer; Reconcile inherited local/Euler/Perry checks. This factor does not replace the separately inherited continuum global expression. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |

<a id="R052"></a>
### R052 — P3 member shape: arcs vs straight chords, arc length

**Original030 unknown:** Members are scored as spherical arcs with N=p*R*s/2; straight chords would give sag 0.1125 m and bending stress 2.1-3.2 GPa, reported outside the least-SF minimiser.

**Original030 today:** chord sag 0.1125 m; bending 2.1065-3.1598 GPa [MAINLINE-11B]

**Current030b:** 026b eightfold rise retains 538.899kN mean compression, rather than reducing it eightfold; elastic bending becomes4.248GPa. Fixed spherical nodal loads also fail the isolated-arch reduction. This controlled026 variant is not022's s1.1m rise8 section.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N309 | NFI-011B-ARC | 030 retained | Scored members are spherical arcs. N=p*R*s/2 is the 011 arch resultant. Straight chords are the alternative: at the rounded point the sag is 0.1125 m and the bending stress is 2.1065 to 3.1598 GPa. Those stresses are reported and are outside the least-SF minimiser. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N313 | NFI-011B-LENGTH | 030 retained | Mass, Euler and Perry use the spacing s, as 011 did. The spherical arc is longer than the chord. That extra length was not substituted. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N378 | NFI-025-CURVATURE | 030b addition | Straight tubes cannot silently be scored as stress-free R10 m arcs.; The cold-bending number is a kinematic linear-elastic warning for a finished straight member, not a claim that a stress-free manufactured curve carries that residual stress. Catalogue straightness of other products is not arc-error certification. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N399 | NFI-023-CHECK-ARC-LENGTH | 030b addition | {"id": "NFI-023-CHECK-ARC-LENGTH", "status": "open", "non_blocking": true, "field": "tube mass and Euler/Perry span", "reported": "011b and 023 use chord spacing s as spherical-arc length.", "check": {"exact_arc_length_m": 2.043554024505062, "chord_m": 2.04, "length_ratio": 1.0017421688750303, "extra_tube_mass_at_unchanged_filed_area_kg": 7.856208800768033}, "evidence": ["circular geometry derivation", "RESULTS.json"], "next": "Carry the approximation explicitly or charge exact arc length and update Euler/Perry. Film sag and actual integer-node geometry remain outside this score."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N617 | NFI-026B-03 | 030b addition | Rise eightfold does not reduce lattice thrust eightfold; Reject isolated supported-arch thrust reduction as a lattice-equilibrium rule. Elastic stresses exceed plausible capability. | [rpt-ref-8befdd4c89803adc44a8](d90bde67ada2ca77-NFI.json) |
| N643 | NFI-026B-03 | 030b addition | Rise eightfold does not reduce lattice thrust eightfold; Reject isolated supported-arch thrust reduction as a lattice-equilibrium rule. Elastic stresses exceed plausible capability. | [rpt-ref-4a20323946ecafd56a6b](d90bde67ada2ca77-NFI.json) |

## T14 — P3 local buckling

<a id="R053"></a>
### R053 — P3 tube local buckling knockdown: SP-8007 gamma (FIX-B)

**Original030 unknown:** Local buckling keeps gamma = 1 at r/t 140.5, while the cited NASA report's curve gives 0.529; local capacity at the SiC point falls to 0.648.

**Original030 today:** gamma 1 at r/t 140.5 [CHECK-011b]; gamma = 1 (classical 0.6 E tw/ro) [MAINLINE-011]

**Original030 needed:** gamma 0.529 from the SP-8007 expression, then re-optimise [CHECK-011b]; re-optimise ro under a knocked-down local curve; conclusion survives to gamma about 0.29 [MAINLINE-011]

**Current030b:** 022d carries local gamma .552141 at its screened lead and flags the long-member shell/column transfer. 026's frame elastic instability exceeds the inherited local-wall screen, reached near lambda 2.03.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N019 | NFI-CHK011B-LOCAL-GAMMA | 030 retained | Local buckling keeps gamma = 1 at r/t 140.5. NASA SP-8007, the source 011 cites for the 0.6, gives gamma = 1-0.901*(1-exp(-sqrt(r/t)/16)) = 0.529. Local at the card's SiC point is then 0.648. Re-optimised with gamma, SiC on the equilateral grid at k 0.2 is 1.075 (r/t 94), two-way is 0.967, and with FIX-A as well 1.205 and 1.083. At 100 kg systems and a 5% margin these are 1.130 and 1.015. | [rpt-check011b-opus-1020](610aec93220adcc1-NFI.json) |
| N150 | NFI-011-LOCAL-KD | 030 retained | {"NFI_id": "NFI-011-LOCAL-KD", "gap": "sigma_local = 0.6*E*t_w/r_o is SP-8007 classical with gamma=1 (no imperfection knockdown). At the aluminum best, local sits 3.9x above the least SF, so the answer is robust; at the T700 best the margin is 1.18x, and a gamma of 0.65 would pull that point's local to ~0.59.", "direction": "Re-optimise r_o under a knocked-down local curve: at s=1 the local margin is 2.6x, so the material conclusion (T700 least ~0.76, yield-bound) survives down to gamma ~0.29 after re-optimisation.", "effect": "The best-point geometry moves; the least SF per material does not."} | [rpt-ref-f21d4bd21d2026511818](0f1373271ca0676e-NFI.json) |
| N373 | NFI-025-LOCAL | 030b addition | NASA axial cylinder knockdown is not a qualified curved-ceramic/CMC member curve.; Global k0.2 is independent of local gamma. Long-strut range cautions apply; scalar CMC modulus omits orthotropic shell stiffness. The 4 mm reoptimized section is thick (mean r/t about 6.21), so thin-shell local theory is not established there. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N493 | NFI-031-P3-LOCAL | 030b addition | FIX-A triangular load sharing is used. FIX-B SP-8007 axial-cylinder knockdown is transferred to curved ceramic members; Perry and k=0.2 global continuum equations remain inherited idealisations. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N505 | NFI-026-07 | 030b addition | Frame elastic instability is beyond the inherited local-wall screen; Do not use the larger frame-only eigenvalue or nonlinear limit as the structural allowable. Ceramic cracking, local wall buckling and ovalization are absent. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |

## T15 — P3 global lattice

<a id="R054"></a>
### R054 — lattice knockdown k (0.2 floor; Wright 1965's 0.4 and its meaning)

**Original030 unknown:** Wright 1965 modified k 0.4 is applied to this card derived classical pressure, which may not match his Table 2 expression; thickness equation illegible; other sources gave no number.

**Original030 today:** k = 0.4 used [CHECK-011b]; k = 0.2 design; 0.5 band top [MAINLINE-11B]; scored 0.2; Wright 0.4 (factor 2.0) [MAINLINE-022]

**Original030 needed:** Wright 1965 Table 2 expression [CHECK-011b]; Legible Wright thickness equation and expression. [MAINLINE-11B]

**Current030b:** 026 prescribed imperfections give nonlinear elastic knockdowns .702–.790 against discrete perfect linear; these do not calibrate a general design k=.2 or .4.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N022 | NFI-CHK011B-WRIGHT-K | 030 retained | Wright's 'modified k of 0.4' may be the coefficient in p = k*E*(t/R)^2, where classical is 2/sqrt(3(1-nu^2)) = 1.2247 at nu 1/3. That would be about 0.327 of classical, not 0.4, and the k 0.4 global pressures would fall by about 18%. The citation is confirmed in Buchert 1965's bibliography. The Table 2 expression is needed. | [rpt-check011b-opus-1020](610aec93220adcc1-NFI.json) |
| N307 | NFI-011B-WRIGHT | 030 retained | Wright 1965, ASCE Journal of the Structural Division 91(ST1):173-201, is the cited paper. The extract shows a modified k of 0.4 used for his Table 2. The thickness equation in the extract is not legible. k=0.4 here multiplies the classical pressure derived in this card, which may not be the expression in that table. Buchert, Gioncu 1995 and Makowski contributed no number. A secondary E' and t' pair that cancels back to the two-way pressure was not scored. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N308 | NFI-011B-KNOCKDOWN | 030 retained | Perfect is k=1. Design level is k=0.2, the floor of the brief's 0.2 to 0.5 lattice-dome band. k=0.5 is the top of that band. This is not the SP-8032 curve and it does not rescale 004's P2-E knockdown. P2-E stays the pinned pair 0.233885578993 and 0.164568553708. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N360 | NFI-022-KNOCKDOWN | 030 retained | {"id": "NFI-022-KNOCKDOWN", "scored_design": 0.2, "wright": 0.4, "factor": 2.0, "recommendation": "Use k 0.2 for ceramic arcs. A brittle member does not shed load after first crack. Wright 1965 used a modified k of 0.4 for a reticulated-shell table. That factor is an optimism here.", "state": "Both values are in the catalog. k 0.2 is the brief's band floor."} | [rpt-mainline022-grok-p3-optimistic-floating-point-1020](307ab133da904ca4-NFI.json) |
| N503 | NFI-026-05 | 030b addition | Specified nonlinear imperfections do not establish a design knockdown; Measured k values apply only to this elastic model and these patterns; combined defects, joint compliance and a worst-case imperfection spectrum remain untested. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |

<a id="R055"></a>
### R055 — P3 continuum validity: smeared global mode vs member length (band s <= 3 m; buckle half-wave)

**Original030 unknown:** Optima stay within s<=3 m where 011 judged the equal-triangle continuum defensible; the unconstrained run to s=6.4 m was not repeated.

**Original030 today:** optimum cut at s <= 3.0 m (V >= 161 nodes) [MAINLINE-011]; s <= 3 m [MAINLINE-11B]

**Original030 needed:** re-run on real geodesic layouts if a design point is picked [MAINLINE-011]

**Current030b:** 022d screened SF 1.258252 at s3.170759m passes only the requested one-member half-wave screen. 026b frequency 4 gives discrete/continuum .848428913 (15.157% lower); frequency 2 .317565955. Ordered .848 applied only to the current global mode gives SF 1.066998; exact ratio gives1.067538. Both are QUESTIONABLE geometry transfers, not a solved 022d frame. CHECK-026 independently reproduces the earlier frequency 6 linear model; it did not rerun nonlinear paths.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N149 | NFI-011-BAND | 030 retained | {"NFI_id": "NFI-011-BAND", "gap": "The unconstrained optimum rides the node-mass saving to s=6.4 m (V=37 nodes), where the equal-triangle continuum behind V(s) is no longer a defensible reading; the reported optimum is cut at s<=3.0 m (V>=161), suppressing 0.0002 of SF.", "direction": "Re-run on real geodesic layouts (unequal members, real tributary areas) if a design point is ever picked.", "effect": "At most +0.1 percent on aluminum; no ranking change."} | [rpt-ref-f21d4bd21d2026511818](0f1373271ca0676e-NFI.json) |
| N315 | NFI-011B-BAND | 030 retained | The reported optima stay inside s<=3 m, where 011 judged the equal-triangle continuum defensible. The unconstrained ride to s=6.4 m was not repeated. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N363 | NFI-030-CONTINUUM | 030b addition | The smeared lattice buckle half-wave pi*sqrt(1.06*rg*R) is 0.57 of the member at 022b's s 6.15 m (40 nodes) and 0.64 at s 5.5 m, against 1.48 at 011b's s 2.04 m and 4.56 at the Mylar s 0.55 m frame. Where the half-wave is shorter than a member, the global formula does not describe the frame; 022b's 1.375 and 1.487 need a discrete geometrically nonlinear check before they count. | [rpt-mainline030-opus-register-1020](858f8f97e8cb24d5-NFI.json) |
| N365 | NFI-030-P3-INBAND | 030b addition | Inside s <= 3 m, SiC arcs with FIX-A and FIX-B at 100 kg and 5% are 1.130, film-limited at s 2.224 m (r_o 121.7 mm, wall 0.915 mm), on the carried 1.5 GPa film. 022c could report an in-band row beside the open band. | [rpt-mainline030-opus-register-1020](858f8f97e8cb24d5-NFI.json) |
| N419 | NFI-CHK024-LATTICE-MODEL | 030b addition | Retains 011b continuum coefficient, k=0.2, 3900 MPa SiC crush, local gamma=1, s as arc length, five-percent joints and steel-column Perry formula on ceramic arcs. They are not newly validated by this film check. | [rpt-ref-7d6892c4e55be16ad523](1b8584393478c427-NFI.json) |
| N463 | NFI-C022-DISCRETE-JOINTS | 030b addition | Uniform lattice equilibrium is correct, but smeared global stiffness and approximately40 continuum vertices at long spacing do not establish a real spherical frame. | [rpt-ref-f6de390e1555b4ca8e78](c6fe867af95c0749-NFI.json) |
| N480 | NFI-030-COEFF-106 | 030b addition | REGISTER.md writes the smeared half-wave as pi*sqrt(1.06*rg*R). The stored waves match pi*sqrt((3/4)*rg_section*R), which is pi*sqrt(1.06066*rg_thin*R). Using the printed 1.06 with the stored thin-ring rg shortens the 022b wave by 1.094 mm, from 3.514184 m to 3.513090 m. | [rpt-ref-490f8e9228d526b69dc8](c637ae242ae817f5-NFI.json) |
| N502 | NFI-026-04 | 030b addition | Discrete perfect eigenvalue differs from smeared continuum; Geometry, nonuniform spacing, torsion, pressure transfer and omitted initial-moment couplings differ. Agreement in scale is not validation of a global knockdown. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |
| N509 | NFI-026-11 | 030b addition | Symmetric eigenmode multiplicities and nonlinear collapse scope; No full multiplicity census, post-collapse dynamics or damaged-state residual capacity is claimed. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |
| N562 | NFI-037-022D-UNFILED | 030b addition | 022d had not filed. The P3 rows are 022c. Projection at 6.15 m and CFRP/Zylon at 5.5 m fail the half-wave test, ratios 0.571 and 0.636. Their global factors are not in-band leads. | [rpt-ref-8c5de04c9c33dbcf7447](f9ff7da1d21d1380-NFI.json) |
| N570 | NFI-CHECK-031-HALF-WAVE | 030b addition | 030's half-wave is pi*sqrt((3/4)*rg*R), rg=sqrt((ro^2+ri^2)/2), divided by bay side. Below 1, or a bay longer than 3 m, is outside the smeared band. The 019-reserve 022b point is s 6.15 m at ratio 0.567895. Every reoptimised SiC row is outside that band. The optimistic 100 m row is ratio 0.568724. The least factor on those rows is global. | [rpt-ref-be337d7d2ce1259d0aff](68d5541c02f9b231-CHECK-NFI.json) |
| N592 | NFI-022D-CONTINUUM | 030b addition | Sixteen overall optima fail half-wave>=arc length. Their screened alternatives are filed, but a wavelength of exactly one member does not establish homogenization, an integer mesh or discrete stability. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |
| N615 | NFI-026B-01 | 030b addition | Coarse-bay continuum departure; Use discrete frame results for these cases; no continuum applicability threshold is validated. | [rpt-ref-8befdd4c89803adc44a8](d90bde67ada2ca77-NFI.json) |
| N641 | NFI-026B-01 | 030b addition | Coarse-bay continuum departure; Use discrete frame results for these cases; no continuum applicability threshold is validated. | [rpt-ref-4a20323946ecafd56a6b](d90bde67ada2ca77-NFI.json) |
| N665 | NFI-038-TOPOLOGY | 030b addition | Fractional optimized node counts are not buildable frames | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N671 | NFI-CHECK-026-01 | 030b addition | 3-segment reproduction agrees; finest-column gaps are the published segment count; No fix card. The card's own mesh table already separates 3 segments from 24. | [rpt-check026-grok-p3-lattice-1020](b7e57b840d56288c-NFI.json) |
| B006 | NFI-030B-DISCRETE-TRANSFER | 030b addition | The ordered 026b-to-022d fold is a sensitivity, not an exact-frame solution.; Apply the ordered .848 only to the global mode of the held 022d screened lead, with all other modes and masses held. The frequency-4 section/topology differs, so the resulting 1.067 multiplier is QUESTIONABLE. The exact source ratio is also shown; no reoptimization, material qualification or verified nonlinear first loss follows. | [rpt-ref-39745602983887568501](02744dbf85113cc4-legacy--02744dbf85113cc4de64187c76ed79779e558031dadf21e6ad2f8aea21188dc1--AUTHORED-NFI.json) |

<a id="R056"></a>
### R056 — P3 global lattice mode added and its coefficient (sqrt(3/2), Buchert 1968)

**Original030 unknown:** Scored global pressure uses the equilateral continuum grid (nu 1/3); the brief two-way coefficient 4 is robotics arithmetic and a geodesic coefficient was not invented.

**Original030 today:** coefficient 4*sqrt(3/2) on E*sqrt(I*A)/(s*R^2) [MAINLINE-11B]; 009 estimate: about 0.70 perfect, 0.14-0.35 knocked down (6061 optimum) [MAINLINE-017]

**Original030 needed:** equivalent-stiffened-shell general-instability check (ribbed-sphere analogy) [MAINLINE-011]; A geodesic grid coefficient. [MAINLINE-11B]; Score global lattice buckling and member bending (011b) before admitting SiC. [MAINLINE-017]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N148 | NFI-011-GLOBAL | 030 retained | {"NFI_id": "NFI-011-GLOBAL", "gap": "No global frame mode: the model checks member Euler, member yield, tube local buckling and film only. Snap-through or general-instability of the whole stiffened sphere between nodes is unmodelled, and MAINLINE-004's spherical knockdown therefore neither applies to nor rescales any P3 number.", "direction": "Add an equivalent-stiffened-shell general-instability check (ribbed-sphere analogy) before any P3 number is read as a whole-vehicle figure.", "effect": "Could only lower the P3 rows; the aluminum plateau's flatness and the material ranking survive any such factor applied uniformly."} | [rpt-ref-f21d4bd21d2026511818](0f1373271ca0676e-NFI.json) |
| N306 | NFI-011B-GRID | 030 retained | 011 counts nodes with the equilateral continuum. The scored global pressure uses that grid: Et=(2/sqrt(3))*E*A/s, nu=1/3, D=(3*sqrt(3)/4)*E*I/s, and the classical sphere 4*sqrt(D*Et)/R^2. The product is 4*sqrt(3/2)*E*sqrt(I*A)/(s*R^2). The brief's two-way pressure, coefficient 4, is the robotics arithmetic and is re-optimised beside it. A geodesic coefficient was not invented. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N348 | NFI-017-P3-MODES | 030 retained | {"NFI_id": "NFI-017-P3-MODES", "gap": "The best P3 point (SiC, least SF 2.848476) is scored on 011's four modes only. Global lattice buckling and member bending are absent; 011b had not filed when this card started, and 009 carries P3 as PENDING-011b with an equivalent-continuum lattice estimate of about 0.70 perfect at the 6061 optimum, 0.14-0.35 knocked down, not recomputed here.", "direction": "011b. Do not admit the SiC point as passing until those two modes are scored.", "effect": "SiC's factor-1 ranking is conditional on the scored modes."} | [rpt-mainline017-improvement-directions-lead4f19-1019](9f3c760a855408f0-NFI.json) |

<a id="R057"></a>
### R057 — two-way grid global coefficient 4 assumes isotropy; an unbraced two-way grid has no in-plane shear stiffness (022b's two-way rows rest on it)

**Original030 unknown:** Whether a two-way grid without diagonals has any smeared global buckling capacity near 4*E*sqrt(I*A)/(s*R^2); the lattice sum gives C1212 = 0. 022b's two-way rows (Ti + Kapton 0.986, SiC 1.98) are governed by it.

**Original030 today:** C = 4 (isotropic) [CHECK-011b]

**Original030 needed:** a discrete buckling solve of the two-way frame, or diagonals [CHECK-011b]

**Current030b:** 022d retains two-way surrogate diagnostics up to SF 1.867825 screened, but no qualified shear stiffness supports C=4. Square-cell sensitivity 1.728883 does not repair that missing mechanism.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N023 | NFI-CHK011B-TEXT | 030 retained | M1: the report body says 'k 0.4 and 0.5 are in the card', but the CARD.md table carries k 1, 0.4 and 0.2 (k 0.5 is in RESULTS.json only). M2: INPUTS.json materials carry no source and 011's INPUTS.json, which holds them, is not pinned. M3: Buchert 1968 prints the card's Et and D, so it can be cited. M4: the 'two_way' rows are the triangulated frame scored with C = 4, not a two-way frame, which would have zero in-plane shear stiffness (C1212 = 0). | [rpt-check011b-opus-1020](610aec93220adcc1-NFI.json) |
| N364 | NFI-030-TWO-WAY | 030b addition | 022b re-counted the two-way grid at 2V-4 members but kept the isotropic C = 4. An unbraced two-way grid has no in-plane shear stiffness, so its two-way rows (Ti + Kapton 0.986, SiC 1.98) are not floating points until a discrete solve or diagonals settle it. | [rpt-mainline030-opus-register-1020](858f8f97e8cb24d5-NFI.json) |
| N593 | NFI-022D-TWO-WAY | 030b addition | The unbraced two-way lattice has no demonstrated in-plane shear stiffness supporting inherited C=4. Primary half-wave and triangular-sag transfers are diagnostic only. Square-cell sensitivity does not repair shear. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |

## T16 — P3 Perry

<a id="R058"></a>
### R058 — P3 member imperfection: geometric Perry eta, brittle tube

**Original030 unknown:** The P3 pass relies on SiC compression 3900 MPa and a metal-style Perry interaction; a 380 MPa screen gives only about 0.24-0.25. Compressive strength is not a bending allowable.

**Original030 today:** 3900 MPa compression; 380 MPa screen gives SF about 0.24-0.25 over 10-50 m [MAINLINE-027]; a0 = s/1000 [MAINLINE-11B]

**Original030 needed:** Brittle tension/compression interaction, statistical size effect and joint eccentricity [MAINLINE-027]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N112 | NFI-027-FRAME-BRITTLE | 030 retained | 011b's SiC compression 3900 MPa and metal-style Perry interaction produce the P3 pass. A380 MPa strength screen gives only about 0.24–0.25 over 10–50 m. Compressive strength is not a ceramic bending/tensile allowable. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N310 | NFI-011B-PERRY | 030 retained | Geometric Perry-Robertson with a0=s/1000 and eta=a0*r_o/rg^2. This is not a code eta table. SF is sigma_cr divided by the arch stress at p_ext. When N exceeds Ne the pole of 1/(1-N/Ne) is passed and that factor is not the score. The formula is a steel-column interaction. On CFRP, CNT and SiC it is a projection. It is scored beside Euler and yield and can bind below both. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |

## T17 — P3 tube material

<a id="R059"></a>
### R059 — SiC tube density 3100 vs 3150

**Original030 unknown:** Tube density kept at 3100 kg/m3 though sheet density is 3150; brazed-socket mass about 1.6 percent light.

**Original030 today:** 3100 kg/m3 used; sheet 3150 kg/m3 [MAINLINE-023]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N221 | NFI-023-DENSITY-3100 | 030 retained | Substituting 3150 would raise the brazed-socket mass about 1.6 percent and would move the recovered safety factor. It was not substituted. | [rpt-ref-a4768f77870336c8cdbb](30c19a9c27a07c4b-NFI.json) |

<a id="R060"></a>
### R060 — SiC tube design allowable: 3.9 GPa crush vs 380 MPa flexural vs Weibull; demand 0.82 GPa with FIX-A (025)

**Original030 unknown:** SiC and T700 P3 values are 011 equal-mass swap properties from 008; SiC 3900 MPa is compressive, flexural about 380 MPa governs bending; 011 uses compressive sigma for member yield.

**Original030 today:** service compression 1.428 GPa; imperfection adds +/-58.8 MPa; no tension [CHECK-011b]; 3900 MPa crush allowable; flexural about 380 MPa [MAINLINE-011]; flexural 380 MPa; compressive 3900 MPa scored; axial stress 824.7 MPa at 562.2 kN [MAINLINE-023]; 3900 MPa crush primary; 380 MPa flexural [MAINLINE-11B]

**Original030 needed:** Compressive design allowable (Weibull treatment) [CHECK-011b]; a buildable-tube demonstration; row to be read as material-boundary only [MAINLINE-011]; allowable owned by MAINLINE-025 [MAINLINE-023]; Score member bending before admitting the SiC direction (011b). [MAINLINE-017]

**Current030b:** 025/CHECK-025 leave full-size SiC/CMC compression allowable null. 022d screened lead assumes Fc3900 MPa; its calculated maximum compression is .947377 GPa at design pressure and 1.198096 GPa at its claimed multiplier. Neither 380 MPa flexure nor 3.9 GPa typical crush qualifies the arc.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N021 | NFI-CHK011B-SIC-FIBRE | 030 retained | At the SiC point the L/1000 imperfection adds +/-58.8 MPa (eta 0.0332, amplifier 1.240) to 1.428 GPa of compression. The fibres are at -1.487 and -1.370 GPa, so there is no tension, and with FIX-A they are -0.855 and -0.794 GPa. The 380 MPa flexural scan (0.262) is therefore not the arcs' allowable. The open number is the compressive design allowable of a 0.88 mm brittle wall at about 1.4 GPa of service stress (022's Weibull item). | [rpt-check011b-opus-1020](610aec93220adcc1-NFI.json) |
| N151 | NFI-011-SIC | 030 retained | {"NFI_id": "NFI-011-SIC", "gap": "SiC's 3900 MPa is a crushing value; 008's own NFI carries that flexural ~380 MPa governs any bending or tension path, with brittle fracture, joining and handling unresolved. A 0.04 m radius sintered SiC tube of 1.3 mm wall is undemonstrated.", "direction": "Treat the SiC row as a material-boundary statement (sigma/rho headroom), not a buildable tube.", "effect": "The P3 sigma/rho-bound conclusion stands; the SiC design point does not."} | [rpt-ref-f21d4bd21d2026511818](0f1373271ca0676e-NFI.json) |
| N220 | NFI-023-FLEXURE-380 | 030 retained | Against 3900 MPa the contact factor is 4.73. Against 380 MPa it is 0.461, and the member itself fails. This card does not replace the 011b allowable. | [rpt-ref-a4768f77870336c8cdbb](30c19a9c27a07c4b-NFI.json) |
| N312 | NFI-011B-SIC | 030 retained | The primary SiC row uses 011's 3900 MPa crush. A second scan uses 380 MPa, the flexural figure 011 carried from 008. Flexural strength, brittle fracture, joining and a sintered tube of this size remain open. Perry and yield at 3900 MPa are not a bending allowable. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N352 | NFI-017-SIC-SIGMA | 030 retained | {"NFI_id": "NFI-017-SIC-SIGMA", "gap": "SiC and T700 P3 values are 011's equal-mass swap properties from 008. SiC sigma 3900 MPa is compressive strength; flexural strength about 380 MPa governs bending paths (008's note), and 011 uses compressive sigma for member yield.", "direction": "Score member bending before the SiC direction is admitted (011b).", "effect": "P3 SiC strength is QUESTIONABLE as a tube direction."} | [rpt-mainline017-improvement-directions-lead4f19-1019](9f3c760a855408f0-NFI.json) |
| N355 | NFI-022-SIC-ALLOWABLE | 030 retained | {"id": "NFI-022-SIC-ALLOWABLE", "value_scored_today_Pa": 380000000.0, "sourced_today": "Saint-Gobain Hexoloy SA 4-point flexural strength 380 MPa on a 3 x 4 x 45 mm bar. Compressive strength on the same sheets is 3900 MPa.", "weibull_Pa": 190451148.77836347, "weibull_note": "Two-parameter Weibull at P_f = 0.001, m = 10, sigma_0 taken as 380 MPa, same volume as the bar. m = 10 is the seal-tube and structural-tile page. Sheet B-1003-2 lists 8 for standard SA and 12 for enhanced SA. This is not a volume-scaled tube allowable, and it is not a compression test.", "crush_Pa": 3900000000.0, "factor_crush_over_flexural": 10.263157894736842, "factor_flexural_over_weibull": 1.9952623149688795, "state": "PENDING-025. 380 and 3900 exist on the datasheet. The 190 MPa figure is a calculation. This card carries 3900 MPa as 011b did. Using it as a tube allowable is an optimism. MAINLINE-025 owns the row.", "scored_baseline_SF": 0.2438010340863489, "weibull_case_SF": 0.12408348691924517, "source": "https://www.ceramicsrefractories.saint-gobain.com/hexoloy-enhanced-sa-sic-technical-data-sheet and the Hexoloy seal-tube page"} | [rpt-mainline022-grok-p3-optimistic-floating-point-1020](307ab133da904ca4-NFI.json) |
| N356 | NFI-022-BENDING-CONTACT | 030 retained | PENDING-025. At the sourced-today point the axial stress is the contact stress if the tube section bears the member force. Perry is the scored bending-imperfection mode. MAINLINE-025 owns the allowable. | [rpt-mainline022-grok-p3-optimistic-floating-point-1020](307ab133da904ca4-NFI.json) |
| N362 | NFI-022-DATASHEET-SPREAD | 030 retained | This card keeps 011b's E of 410 GPa and density 3100 kg/m3 so the regression is the same material. Hexoloy pages also print E 430 GPa, density 3.10 to 3.15 g/cm3, and Poisson's ratio 0.14. The local-buckling coefficient stays 0.6. | [rpt-mainline022-grok-p3-optimistic-floating-point-1020](307ab133da904ca4-NFI.json) |
| N368 | NFI-025-COMPRESSION | 030b addition | No probability-qualified compression allowable for full-size Hexoloy SA or CVD arcs.; ASTM C1424 separates compression from tensile weakest-link statistics; 380 MPa flexure is not a measured compression allowable. Zero continuum tensile hazard cannot establish compressive survival. Earlier unqualified required-stress keys denote the inherited force rule; explicitly named dual-demand fields distinguish the amendment. The requested tube-size interface is supplied in allowable.py with compression qualification null. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N369 | NFI-025-WEIBULL | 030b addition | Hexoloy SA fitted population, characteristic strength and test reference size are incomplete; current m8 and 2012 m10 differ.; The 40/20 mm bend spans and mean interpretation of typical380 MPa are explicit assumptions. Independent tensile SA data show m5; do not cherry-pick m10 as validated. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N370 | NFI-025-CVD-REFERENCE | 030b addition | Commercial CVD m11/beta424 MPa lack effective coupon size; miniature CVD hoop tests are distinct populations.; Do not borrow a reference area from the miniature TRISO tube paper for a commercial CVD strength distribution. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N371 | NFI-025-RISK-LIFE | 030b addition | Analyst-selected short-term system failure target has no demonstrated structural or lifetime qualification.; Target concerns first critical member loss in one load exposure. A uniform tensile illustration is not actual contact reliability, total failure probability or lifetime survival. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N379 | NFI-025-CMC-PROPERTIES | 030b addition | CMC compression, tensile damage onset, density and stiffness are not a coherent tube allowable set.; 128 MPa is tensile PLS, not measured compression onset. 580 MPa comes from another Hi-Nicalon CVI product; its E/density are not given. Do not use apparent Archimedes density as bulk mass density. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N398 | NFI-023-CHECK-CONTACT-METRIC | 030b addition | {"id": "NFI-023-CHECK-CONTACT-METRIC", "status": "open", "non_blocking": true, "field": "sigma_contact and flexural SF", "reported": "N/A called contact stress;380MPa flexure ratio used to say the tube fails.", "check": {"filed_mean_axial_Pa": 824658297.2240398, "flexural_ratio": 0.46079691586097404, "interpretation": "N/A is mean axial wall compression. Local bearing/peel/splitting is not resolved;380MPa flexure is not a compressive failure criterion."}, "evidence": ["Hexoloy primary sheet", "CHECK.md"], "next": "Retain both as explicit material sensitivities; use a suitable ceramic stress/failure model and geometry for contact acceptance."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N454 | NFI-CHECK-025-SHEET-MODULUS | 030b addition | Hexoloy SA Form B-1045, opened this check, heads the table Typical Physical Properties. It prints compressive strength 3900 MPa, four-point flexure 380 MPa, Weibull modulus 10, elastic modulus 430 GPa, Poisson 0.14, density 3.10 g/cm3, and flexure bars 3 x 4 x 45 mm. The card scores the inherited 410 GPa and says so. Density matches. The same-bay factors at 430 GPa are recorded and are not a new optimum and not a qualified allowable. | [rpt-ref-a8b77f7de2ffc56af7b4](50b53f5a5398101c-CHECK-NFI.json) |
| N455 | NFI-CHECK-025-NULL-ALLOWABLE | 030b addition | The filed decision leaves qualified Hexoloy SA, CVD SiC and CMC tube compression allowables null. The cited SA figures are typical flexural 380 MPa and typical compression 3900 MPa. Null is not zero strength, and 3.9 GPa is not a qualified tube allowable. | [rpt-ref-a8b77f7de2ffc56af7b4](50b53f5a5398101c-CHECK-NFI.json) |
| N462 | NFI-C022-ALLOWABLE | 030b addition | Neither3900 MPa compression nor380 MPa flexure supplies a full-sized curved-tube compression allowable. | [rpt-ref-f6de390e1555b4ca8e78](c6fe867af95c0749-NFI.json) |
| N506 | NFI-026-08 | 030b addition | Material input editions and thin curved member fabrication; Bulk typical data do not establish thin-wall curved SiC member strength, defects, residual stress or joint capability. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |
| N595 | NFI-022D-ALLOWABLE | 030b addition | Neither 3900 MPa bulk crush nor 380 MPa flexure is a qualified full-size curved SiC compression allowable. No qualified assembly failure probability is known. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |
| N605 | NFI-017b-SIC-ALLOWABLE | 030b addition | Every P3 route to SF 1 needs a qualified SiC design compressive strength of 0.83-1.20 GPa (projection row 0.91 GPa). No design compressive allowable exists; flexure is 380 MPa and 3900 MPa is an unqualified typical value.; Full-size curved tube compression tests with a Weibull (or other probabilistic) basis. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| N663 | NFI-038-CERAMIC_SIZE | 030b addition | Small compression specimens do not establish full curved SiC reliability | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N672 | NFI-CHECK-026-02 | 030b addition | Vendor typical modulus was not substituted and was not re-fetched; Owner NFI-026-08 stands. Bulk typical data are not an allowable for these members. | [rpt-check026-grok-p3-lattice-1020](b7e57b840d56288c-NFI.json) |

<a id="R061"></a>
### R061 — SiC tube manufacture at hull scale (025)

**Original030 unknown:** P3 needs metre-scale curved thin-walled SiC tubes and a film at 1.5 GPa allowable; the opened supplier example is about 12 in long; not demonstrated products.

**Original030 today:** supplier seal tube typically 12 in long [MAINLINE-027]; design OD 281.9 mm, L 0.62 m, wall 0.216 mm; exists: OD 25-381 mm, single piece to 1.4 m, SiSiC wall about 2-4 mm [MAINLINE-022]

**Original030 needed:** Tube and film manufacturing, joints, leaks, defects, proof loads and tolerances [MAINLINE-027]

**Current030b:** 022d screened lead requires 275.083 mm OD, 1.137365 mm wall, 3.184194 m curved members. Complete product/tolerance/process capability remains unsourced.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N111 | NFI-027-FRAME-PRODUCT | 030 retained | P3 asks for metre-scale curved, thin-walled SiC tubes and a pressure membrane at 1.5 GPa allowable. The opened supplier seal-tube example is typically 12 in long. These components and their formed geometry are not demonstrated products. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N357 | NFI-022-TUBE | 030 retained | {"id": "NFI-022-TUBE", "design_OD_mm": 281.8989450499424, "design_length_m": 0.62, "design_wall_mm": 0.2163958093517604, "exists": "Hexoloy SA process tubes: OD 25 to 381 mm, single piece to 1.4 m, bonded assemblies to 4.9 m. Seal tubes are about 0.30 m long. Silit SiSiC radiant tubes reach OD 300 mm, length 3.5 m, thinnest published wall about 4 mm, Amasic-3D about 2 mm.", "factor_length_over_hexoloy_single": 0.4428571428571429, "factor_wall_vs_2mm": 0.1081979046758802, "state": "PENDING-025. A 250 mm class diameter exists. A 2 m single Hexoloy piece does not. A wall near 0.9 mm is below the 2 mm SiSiC floor and is a PROJECTION for alpha-SiC. MAINLINE-025 owns the manufacture row. These factors are context at the sourced-today geometry, not a closed finding.", "source": "https://www.ceramicsrefractories.saint-gobain.com/products/shapes/tubes/hexoloy-sic-process-tubes and the ceramic radiant tube page"} | [rpt-mainline022-grok-p3-optimistic-floating-point-1020](307ab133da904ca4-NFI.json) |
| N375 | NFI-025-SA-FABRICATION | 030b addition | Commercial SA large straight tubes do not establish the target thin, curved, long member.; Large diameter, long bonded assemblies and thin small tubes cannot be combined into a demonstrated one-piece envelope. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N376 | NFI-025-SISIC-WALL | 030b addition | Published infiltrated SiSiC walls are thicker; its properties differ from sintered SA.; 2/4 mm constraints are geometric borrowed screens only. Fixed-OD masses use inherited SA density; reoptimized small-OD cases preserve float mass and must score tensile bending separately. The unconstrained4mm row reaches3.192GPa tension at its limiting load and is an explicitly incomplete upper bound; scoring tensile proxies lowers its optimum. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N377 | NFI-025-CVD-FABRICATION | 030b addition | Historical CVD examples demonstrate relevant dimensions individually, not a current qualified complete arc.; Patent evidence is not a current purchase specification or proof of1047 repeatable members. OD202 mm is inferred from a200 mm mandrel plus two1 mm deposits. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N380 | NFI-025-CMC-SCALE | 030b addition | Long small cladding and wide short rings do not prove the required large thin structural CMC arc.; Fiber bridging may improve damage tolerance but does not validate a monolithic isotropic shell model or guarantee a gas-tight matrix after tensile cracking. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N465 | NFI-C022-MANUFACTURE | 030b addition | The long-span optimum increases the full-size manufacturing burden beyond025's original two-metre target. | [rpt-ref-f6de390e1555b4ca8e78](c6fe867af95c0749-NFI.json) |
| N597 | NFI-022D-MANUFACTURE | 030b addition | No complete diameter, wall, arc length, curvature and tolerance combination is production-qualified by this scan. Continuous film and fractional node counts are optimization surrogates. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |
| N606 | NFI-017b-TUBE-MATERIAL | 030b addition | Tube specific stiffness x1.41 (186 MPa per kg/m3) is beyond SiC (best CVD 145). A carbon-fibre tube would need a sourced compressive strength near 0.8-1.2 GPa with that stiffness.; Sourced UHM carbon tube compressive strength and modulus. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| N620 | NFI-026B-06 | 030b addition | Actual thin curved SiC sections, film and joints ungrounded; Fabrication, ceramic defects, residual stress, joint compliance, seals and film strength need separate evidence. No certification. | [rpt-ref-8befdd4c89803adc44a8](d90bde67ada2ca77-NFI.json) |
| N646 | NFI-026B-06 | 030b addition | Actual thin curved SiC sections, film and joints ungrounded; Fabrication, ceramic defects, residual stress, joint compliance, seals and film strength need separate evidence. No certification. | [rpt-ref-4a20323946ecafd56a6b](d90bde67ada2ca77-NFI.json) |

## T18 — P3 nodes and joints

<a id="R062"></a>
### R062 — P3 node and joint mass (5% assumed; 023 bill 31 to 859 kg)

**Original030 unknown:** Joints carried at 5 percent (216.4 kg); a SiC pad bearing the member force gives bounds 1938-11620 kg; a 1 MN ceramic load introduction is not a catalog fitting.

**Original030 today:** 20 g/node; joints 5% of tube mass [MAINLINE-027]; node hardware 0.02 kg each [MAINLINE-011]; 5 percent of tube mass [MAINLINE-11B]; 216.4 kg allowance; bounds 1937.7-11619.8 kg; member force 295857 N [MAINLINE-022]

**Original030 needed:** Nodes and film attachment sized from load paths [MAINLINE-027]; real geodesic load paths and joint masses [MAINLINE-011]; A measured fitting or parts list. [MAINLINE-11B]; Joint mass owned by MAINLINE-023. [MAINLINE-022]

**Current030b:** 026 discrete inherited mass overruns lift by 61.40 kg. 022d's separate continuum witness closes its own inherited mass contract; that does not repair the 026 mesh or include omitted process masses.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N113 | NFI-027-FRAME-NODES | 030 retained | P3 retains 20 g/node and 5% tube-mass joints without measured capacity or complete film-attachment masses. A load-linked node-mass sensitivity changes little numerically, but does not validate the 20 g anchor. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N153 | NFI-011-NODES | 030 retained | {"NFI_id": "NFI-011-NODES", "gap": "Node count is the equilateral-continuum formula (equal members, equal tributary area R*s per member, load N=p*R*s/2 — the 002 pinned load path), node hardware 0.02 kg each, and no separate joint or gusset mass exists for P3 in the pinned mass rules.", "direction": "Real geodesic load paths and joint masses before any design pick.", "effect": "Node and joint mass growth eats tube mass one-for-one at the ceiling; SF_yield falls in proportion."} | [rpt-ref-f21d4bd21d2026511818](0f1373271ca0676e-NFI.json) |
| N311 | NFI-011B-JOINT | 030 retained | 011 had no separate joint mass. This card sets joint mass to 5 percent of tube mass and reduces the tube budget so film, nodes, joints, systems and tube still equal the lift mass. The 5 percent is the P2 sandwich fraction applied to tubes, not a measured fitting. RESULTS carries a 6061 scan with the joint term removed. Node mass remains 0.02 kg times V(s). | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N358 | NFI-022-JOINTS | 030 retained | {"id": "NFI-022-JOINTS", "allowance_kg": 216.4271448895479, "lower_bound_kg": 1937.6527363866064, "upper_bound_kg": 11619.759954966023, "member_force_N": 295857.48359825916, "factor_lower_over_allowance": 8.9529099382403, "state": "PENDING-023. This card carries joints at 5 percent of film, nodes and tubes, 216.427144889 kg. The bounds are context only: a SiC pad at 380 MPa over one tube diameter of engagement. MAINLINE-023 owns the joint mass. A 1 MN ceramic load introduction is not a catalog fitting.", "tag": "PENDING-023"} | [rpt-mainline022-grok-p3-optimistic-floating-point-1020](307ab133da904ca4-NFI.json) |
| N381 | NFI-025-JOINT-MASS | 030b addition | Fixed node mass and 5% joint mass have no demonstrated force-transfer design.; Any mass growth reduces available tube material and increases mean compressive demand; no permission to borrow the entire lift mass twice. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N500 | NFI-026-02 | 030b addition | Discrete geometry exceeds inherited mass allowance; The original just-floating point is not preserved by the actual geodesic realization; film shape and all real joints remain ungrounded. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |

<a id="R063"></a>
### R063 — P3 node moment rigidity required by the smeared global mode

**Original030 unknown:** Smeared bending stiffness assumes members continuous through nodes; pinned or soft nodes lower the global mode. Member torsion omitted (would add 11.8-13.7%).

**Original030 needed:** Joints that carry member-end moments as well as axial force; check torsion-rigid case [CHECK-011b]

**Current030b:** 026 freely rolling curved ball-pin members have zero-strain mechanisms; actual anti-roll/film or joint rotational stiffness is required. The nominal rigid-joint solution is not a measured connection.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N020 | NFI-CHK011B-JOINTS | 030 retained | The smeared D (Buchert's t_B) presumes members continuous in bending through the nodes, which means moment-rigid joints. With pinned or soft nodes the bending stiffness and the global mode fall, so 023's joints must carry member-end moments as well as axial force. Member torsion is omitted; with torsion-rigid joints it would raise the global SF by 13.7% for SiC (nu 0.14) and 11.8% for 6061 (lattice sum D1111 1.454 or 1.407 against 1.125). | [rpt-check011b-opus-1020](610aec93220adcc1-NFI.json) |
| N393 | NFI-023-CHECK-NODE-LOAD-PATH | 030b addition | {"id": "NFI-023-CHECK-NODE-LOAD-PATH", "status": "open", "non_blocking": true, "field": "m_joint_kg and smeared bending stiffness", "reported": "31.039kg of wrap,157.685kg Ti orthe re-closed socket mass plus.02kg/node described as fittings.", "check": {"sixfold_pressure_force_N": 344045.7589290622, "remaining_load_path": "No sized central receiver/hub, collector, load turning, film attachment or measured rotational stiffness. Braze model only extends a ceramic wall."}, "evidence": ["CHECK.md", "joint formulas", "011b D=(3sqrt3/4)EI/s"], "next": "Define a complete node geometry and its mass/stiffness. Preserve present values as partial end-material estimates; do not assume they establish the global D used in the score."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N508 | NFI-026-10 | 030b addition | Beam and joint idealizations; Shear flexibility, cross-section distortion, brittle failure, finite joint stiffness and construction stress require independent grounding. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |
| N664 | NFI-038-JOINT_STIFFNESS | 030b addition | Required P3 rotation/roll stiffness is unknown | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |

<a id="R064"></a>
### R064 — P3 tube-end joint routes at about 0.5 MN (023: CFRP wrap, Ti, Invar, braze, pin, bond to SiC)

**Original030 unknown:** The rough 0.5 kg fitting was the pin at the two-way force; at the equilateral force the pin is 0.202 kg and the wall still cannot bear it.

**Original030 today:** 31.0 kg (0.015 kg per end) at 562.2 kN; 1470 MPa compression allowable [MAINLINE-023]; 28.9 MPa lap shear at 25 C (anodized aluminium); bond 25.0 mm at 562.2 kN [MAINLINE-023]; 157.7 kg (0.075 kg per end) at 562.2 kN, 0.70x the 225.5 kg allowance [MAINLINE-023]; 858.6 kg (0.410 kg per end), 3.81x the allowance [MAINLINE-023]

**Original030 needed:** compression coupon of the wrap bonded to SiC at the sized bond length [MAINLINE-023]; lap shear on the real SiC surface at service temperature [MAINLINE-023]; a higher allowable or a shorter bonded detail [MAINLINE-023]; shear measurement on the tube diameter and a socket section [MAINLINE-023]

**Current030b:** CHECK-022b/022c establishes that old joints sized at lambda1 did not support quoted multipliers. 022d charges lambda-squared joint mass and sizes nominal axial/bond capacities at its target. Adhesive mass, peel, bearing, moment transfer and actual SiC bonds remain open.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N214 | NFI-023-CFRP-WRAP | 030 retained | The lightest joint is this wrap: 0.015 kg per end and 31.0 kg at 562.2 kN. The fiber and the coupon exist today. A wound transition on an SiC tube does not. | [rpt-ref-a4768f77870336c8cdbb](30c19a9c27a07c4b-NFI.json) |
| N215 | NFI-023-ADHESIVE-TRANSFER | 030 retained | The paste exists today. The adherend in the coupon is aluminum, not SiC. The bond at 562.2 kN on the 011b radius is 25.0 mm. It uses 28.9 MPa with no temperature knockdown and no peel length. | [rpt-ref-a4768f77870336c8cdbb](30c19a9c27a07c4b-NFI.json) |
| N216 | NFI-023-TI-SLEEVE | 030 retained | The sheet exists today. At 562.2 kN the sleeve is 0.075 kg per end and 157.7 kg, 0.70 times the 225.5 kg allowance. Frozen least SF is 1.232 by the film. Re-optimised least SF is 1.431 at k 0.2 and 1.995 at k 0.4. | [rpt-ref-a4768f77870336c8cdbb](30c19a9c27a07c4b-NFI.json) |
| N217 | NFI-023-INVAR | 030 retained | The alloy exists today and is the expansion match. At 562.2 kN the sleeve is 0.410 kg per end and 858.6 kg, 3.81 times the allowance. Frozen least SF is 1.054, global. Re-optimised least SF is 1.245 at k 0.2 and 1.616 at k 0.4. | [rpt-ref-a4768f77870336c8cdbb](30c19a9c27a07c4b-NFI.json) |
| N218 | NFI-023-BRAZE | 030 retained | The shear pair is a lab result. At 562.2 kN the socket is the tube wall continued for 28.9 mm, 0.062 kg per end and 130.6 kg, 0.58 times the allowance. Frozen least SF is 1.232. A solid node is not sized. A co-sintered frame is a PROJECTION. The 342 MPa bend result failed in the ceramic and is not a shear allowable. | [rpt-ref-a4768f77870336c8cdbb](30c19a9c27a07c4b-NFI.json) |
| N219 | NFI-023-PIN-BEARING | 030 retained | The rough 0.5 kg titanium fitting was this pin at the two-way force. At 562.2 kN it is 0.202 kg and the wall still cannot bear it. The titanium sleeve is 0.075 kg. | [rpt-ref-a4768f77870336c8cdbb](30c19a9c27a07c4b-NFI.json) |
| N372 | NFI-025-CONTACT | 030b addition | Unknown node/seat geometry and stress-weighted tensile regions.; Ct is positive principal tensile stress divided by mean axial compression, not bearing pressure. Full-volume caps only illustrate a hypothetical field; actual smaller hot spots require correct surface/volume/edge integration. Original unqualified force/Ct keys refer to the inherited case; the new branch-specific arrays score both demands. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N392 | NFI-023-CHECK-JOINT-MARGIN | 030b addition | {"id": "NFI-023-CHECK-JOINT-MARGIN", "status": "open", "non_blocking": true, "field": "reported least SF 1.466/2.061 for wrap shell search", "reported": "The six scored modes exclude joint strength. End sections and bonds are sized at N/strength and N/shear.", "check": {"nominal_joint_strength_SF": 1.0, "frozen_joint_inclusive_nominal_SF": 1.0, "wrap_shell_k02": 1.4658145265725706, "wrap_shell_k04": 2.0607540827668074, "sleeve_scaling_for_target_q": "end mass scales q^2 at fixed section; braze overlap scales q"}, "evidence": ["CHECK.md joint sizing derivation", "RESULTS.json nominal_joint_SF"], "next": "Label existing factors shell-only. Include joint modes and resize at the desired load factor before quoting assembled-frame margin."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N394 | NFI-023-CHECK-BOND-MASS-AND-TRANSFER | 030b addition | {"id": "NFI-023-CHECK-BOND-MASS-AND-TRANSFER", "status": "open", "non_blocking": true, "field": "metal sleeve/CFRP mass and bond allowable", "reported": "EA9394 nominal shear28.9MPa and no adhesive mass in the budget.", "check": {"bond_area_m2_per_end": 0.019452120164702612, "additional_adhesive_mass_per_100um_gap_kg": 5.534469519646309, "gap_status": "100micron is a sensitivity assumption, not a selected design", "source_status": "Aluminum lap-shear typical datum; SiC, peel, environment and design basis unresolved"}, "evidence": ["Henkel TDS pp1,3–5", "independent volume calculation"], "next": "Specify bondline thickness and charge its mass, then establish SiC joint strength and load-transfer distribution for the required conditions."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N395 | NFI-023-CHECK-BRAZE-PAIR | 030b addition | {"id": "NFI-023-CHECK-BRAZE-PAIR", "status": "open", "non_blocking": true, "field": "Cusil-ABA socket", "reported": "25MPa coupon shear used on a continued SiC tube wall.", "check": "Primary publisher abstract identifies SiC/Mo and SiC/Kovar, not an all-SiC tubular node. Receiver metal, braze filler, residual stress and central connection are not sized.", "evidence": ["sources/braze2020-reading.json", "INPUTS.json"], "next": "Name the actual material pair and include receiver/filler geometry and mass; retain in-the-lab evidence and PROJECTION assembly tag."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N397 | NFI-023-CHECK-PIN-SPAN | 030b addition | {"id": "NFI-023-CHECK-PIN-SPAN", "status": "open", "non_blocking": true, "field": "pin_clevis_reference.length_m and mass_kg", "reported": "A3d pin is assumed for a two-wall bearing calculation.", "check": {"length_3d_m": 0.08056850952246337, "tube_OD_m": 0.24737672474737216, "mass_for_2r_span_minimum_kg": 0.6207841105826379, "bearing_Pa": 11889414314.899754}, "evidence": ["RESULTS.json supplements", "pin volume and diameter geometry"], "next": "If used as a through-tube reference, include the full span plus lugs and pin bending. It is already rejected on bearing; keep it out of candidate mass ranking."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N460 | NFI-C022-JOINT-MULTIPLIER | 030b addition | 023's sleeve/wrap dimensions consume the assumed axial and bond allowables at design force N; the frozen joint has no modeled pressure margin above1. | [rpt-ref-f6de390e1555b4ca8e78](c6fe867af95c0749-NFI.json) |
| N579 | NFI-034-JOINT-ADHESIVE-MASS | 030b addition | The 023 end-material estimate omits adhesive mass. At nominal inherited bond area, assumed 0.2 mm gap and 1400 kg/m3 density, this card adds 12.565 kg for Ti sleeves and 4.078 kg for CFRP wraps. Shear-transfer and gap assumptions remain unqualified. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N590 | NFI-022D-JOINT | 030b addition | 023 axial/bond dimensions now use each candidate's lambda and their lambda-squared mass. SiC adhesion, peel, moment transfer, local bearing, sleeve stability and adhesive mass remain unknown. Percent joints have no scored capacity. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |

## T19 — P3 film

<a id="R065"></a>
### R065 — fibre cross-ply membranes as film (Zylon, Dyneema): not a sourced film; resin, life, gas-tightness

**Original030 unknown:** A uniaxial filament needs a 0/90 build for both pillow directions, doubling thickness; resin not included so a real laminate is heavier.

**Original030 today:** 19 years at 60% of break (filament) [MAINLINE-024]; total thickness = 2 x one-direction thickness [MAINLINE-024]; 20% fraction; lives 15 and 250 years at 16 C (rope) [MAINLINE-024]

**Original030 needed:** Laminate creep test [MAINLINE-024]; Resin-inclusive laminate mass [MAINLINE-024]; Film creep data [MAINLINE-024]; Printed density [MAINLINE-024]

**Current030b:** DEMONSTRATED source-contract correction: total Zylon 0/90 gauge must be shared between directions. Old published cap points fall to film SF .746876/.708523 at fixed geometry. 022d charges both plies and reoptimizes; an actual complete membrane remains unqualified.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N085 | NFI-ZYLON-EXTRAPOLATION | 030 retained | The 19 year life is Toyobo's extrapolation of an HM filament at 60 percent of break, not a laminate test. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N086 | NFI-CROSSPLY | 030 retained | A uniaxial filament needs a 0/90 build to carry both pillow directions. Total thickness is twice the one-direction thickness. No resin is included, so a real laminate is heavier. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N087 | NFI-DYNEEMA-ROPE | 030 retained | The 20 percent fraction and the 15 and 250 year lives are indicative rope numbers at 16 C, not a film. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N088 | NFI-DYNEEMA-DENSITY | 030 retained | Density is the printed GPa divided by the printed N/tex. The sheet does not print density. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N098 | NFI-FABRIC-POROUS | 030 retained | A filament crossply is not taken as gas-tight. The barrier is a separate layer. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N412 | NFI-CHK024-COMPLETE-SYSTEM | 030b addition | The lightest Zylon row is 109.701010474 kg of ideal two-direction fibre only. Resin, barrier substrate/coating, attachments and installation losses are unbooked. No complete gas-tight film system mass is supplied. Fibre alone exceeds the 97.515 kg pin. | [rpt-ref-7d6892c4e55be16ad523](1b8584393478c427-NFI.json) |
| N416 | NFI-CHK024-CREEP-TRANSFER | 030b addition | Toyobo 19 years at 60% break is extrapolated HM filament performance. DSM 15/250 years at 20% break is an indicative 16 C rope comparison. Neither qualifies a resin-free 0/90 pressure membrane, joints or weather exposure. Toyobo calls for light protection outdoors. | [rpt-ref-7d6892c4e55be16ad523](1b8584393478c427-NFI.json) |
| N457 | NFI-C022-ZYLON-DIRECTION | 030b addition | 022b and 022c assign the full total 0/90 thickness to both tensile directions. | [rpt-ref-f6de390e1555b4ca8e78](c6fe867af95c0749-NFI.json) |
| N568 | NFI-037-FILM-CTE | 030b addition | The projection film has no stated modulus or expansion. The two assumptions are 10 GPa with 4.5e-6 and with 17e-6. Neither moves the out-of-band global factor below 1. | [rpt-ref-8c5de04c9c33dbcf7447](f9ff7da1d21d1380-NFI.json) |
| N589 | NFI-022D-FILM | 030b addition | The doubled directional mass is corrected in this model; a complete 0/90 Zylon membrane with a barrier, seams, biaxial/creep allowables and this gauge is still unsourced. The 1.5 GPa film is also PROJECTION. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |
| N662 | NFI-038-FILM_EXISTS | 030b addition | No complete qualified high-strength gas-tight laminate supplied | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |

<a id="R066"></a>
### R066 — film barrier: permeation data and coatings

**Original030 unknown:** Alumina barrier numbers are coupon measurements; coating a 1257 m2 hull was not opened. PROJECTION at hull scale.

**Original030 today:** 1 atm oxygen assumed [MAINLINE-024]; coupon-scale measurements [MAINLINE-024]

**Original030 needed:** Stated test pressure [MAINLINE-024]; N2 permeation for those films [MAINLINE-024]; Hull-scale coating demonstration [MAINLINE-024]

**Current030b:** 034 adds a projected 57.546 kg barrier/attachment/seam bill to its older Zylon geometry. It is not a proven minimum and must be recomputed for the 022d assembly.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N092 | NFI-MYLAR-PRESSURE | 030 retained | The oxygen column does not print the test pressure. The scale uses 1 atm of oxygen. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N093 | NFI-N2-MISSING | 030 retained | N2 is opened for Kapton only. PEN, Mylar and the ALD paper do not give N2. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N095 | NFI-ALD-SCALE | 030 retained | The alumina numbers are coupon measurements. A 1257 m2 hull coating was not opened. Tagged PROJECTION at hull scale. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N417 | NFI-CHK024-GAS-COVERAGE | 030b addition | N2 is available only for Kapton. Water retains source conditions, with no hull RH. Seams, defects, outgassing, thickness scaling and stressed/coated permeability are unqualified. Kapton source-condition sum is below the inherited allowance; it is not a complete service leak test. | [rpt-ref-7d6892c4e55be16ad523](1b8584393478c427-NFI.json) |
| N418 | NFI-CHK024-ALD-AND-UNSOURCED | 030b addition | ALD bound is a supported lab coupon, not a bare film, fibre coating or hull-scale result; substrate and fabrication mass remain necessary. CNT/graphene production allowables remain uncomputed. | [rpt-ref-7d6892c4e55be16ad523](1b8584393478c427-NFI.json) |
| N580 | NFI-034-BARRIER-ASSEMBLY | 030b addition | The Zylon row needs a separate barrier. A 12 um PET substrate, assumed 50 nm Al, 25 g/m2 attachment/lamination and 5 kg seam installation total 57.546 kg. This is a worked bill, not a qualified lightest laminate or weather/UV protection system. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N581 | NFI-034-GAS-COVERAGE | 030b addition | Kapton has sourced CO2/O2/H2/N2/He data but not Ar; Ar is set to N2. Mylar has sourced O2 only: other gas ratios are assumed, including N2, and checked in a sensitivity. Outgassing is water-equivalent with a 5 mass% H2 sensitivity, not measured composition. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |

<a id="R067"></a>
### R067 — film pillow radius assumption

**Original030 unknown:** Pillow radius set to the bay side 2.04 m because that is the earlier film formula, not a measured cap.

**Original030 today:** pillow radius 2.04 m [MAINLINE-024]

**Original030 needed:** Measured pillow cap [MAINLINE-024]

**Current030b:** 022c charges cap sag; 022d derives equilateral constant-tension mean s²/(40rho), 1.166003× the selected cap mean. Loaded nonlinear shape, edge motion and additional area remain open.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N083 | NFI-CURVATURE | 030 retained | Pillow radius is set to the bay side, 2.04 m, because that is the 011b film formula. It is not a measured cap. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N411 | NFI-CHK024-SAG-NOT-CHARGED | 030b addition | The original filed card gives cap rise 0.374346974907 m but keeps full-sphere lift. All three closures spend the original 4889.44215019 kg. No sag-volume integral or lift deduction appears. | [rpt-ref-7d6892c4e55be16ad523](1b8584393478c427-NFI.json) |
| N414 | NFI-CHK024-PILLOW-AREA-BOUNDARY | 030b addition | Curvature equals bay side to preserve the 011b film equation. Circumscribed circular-cap rise does not establish compatibility with all three actual edge arcs. Film masses and gas rates use 4*pi*R^2 without pillow-area correction. Triangular tributary and scored arc line loads differ; the stated 011b load path is retained. | [rpt-ref-7d6892c4e55be16ad523](1b8584393478c427-NFI.json) |
| N456 | NFI-CHECK-025-SAG-UNCHARGED | 030b addition | Zero-spare optima do not deduct the sag lift loss already filed on MAINLINE-024: 64.1580396987 kg at s 2.04 m and 94.3500583804 kg at s 3 m. 025 assigns that charge elsewhere. This is not a numerical mismatch. | [rpt-ref-a8b77f7de2ffc56af7b4](50b53f5a5398101c-CHECK-NFI.json) |
| N464 | NFI-C022-SAG-GEOMETRY | 030b addition | 022c correctly charges the selected circular-cap approximation; an exact triangular membrane is not integrated, and the same triangular cap law is used for two-way cells. | [rpt-ref-f6de390e1555b4ca8e78](c6fe867af95c0749-NFI.json) |
| N494 | NFI-031-P3-SAG | 030b addition | 022b's s/(16R) displacement loss is applied as reduced volume at every altitude. Film shape may change with pressure, and the spherical arc/member model is approximate for 6m bays on R10m. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N507 | NFI-026-09 | 030b addition | Pressure fan omits film stiffness and solved membrane shape; Quantify membrane and connection restraint. Especially consequential for pinned member roll and actual enclosed volume. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |
| N582 | NFI-034-GEOMETRY | 030b addition | Uses 021b face/core geometry and re-sizes 028 scarfs to its panel width. Uses 022c cap sag for volume and the original sphere area for films; a 10% area sensitivity is supplied. A sphere cutting pattern and exact pillow area are absent. P3 internal solid volume is neglected in the pressure model. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N594 | NFI-022D-SAG | 030b addition | The exact equilateral mean is now derived for the linear constant-tension membrane. Cap is a circular surrogate; nonlinear shape, extra membrane area and loaded edge movement remain open. Primary two-way rows intentionally preserve 022c's geometry; square-cell alternatives are separate. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |
| N619 | NFI-026B-05 | 030b addition | Film shape, sag and material stiffness unresolved; Remaining payload301.391/301.814 kg is conditional; do not interpret uncharged sag as physically zero or substitute fan volume for actual lift. | [rpt-ref-8befdd4c89803adc44a8](d90bde67ada2ca77-NFI.json) |
| N645 | NFI-026B-05 | 030b addition | Film shape, sag and material stiffness unresolved; Remaining payload301.391/301.814 kg is conditional; do not interpret uncharged sag as physically zero or substitute fan volume for actual lift. | [rpt-ref-4a20323946ecafd56a6b](d90bde67ada2ca77-NFI.json) |

<a id="R068"></a>
### R068 — P3 film allowable and design stress (1.5 GPa carried, no datasheet; Kapton, Teonex, Mylar today)

**Original030 unknown:** Film allowable is an owner assumption with no datasheet; wrinkling, puncture, sag area and shear transfer are unmodelled, and it binds for SiC and CNT rows.

**Original030 today:** film allowable 1.5 GPa (no datasheet) [CHECK-011b]; 1.5 GPa, 80 um, 970 kg/m3 (pin) [MAINLINE-024]; design stress = 0.5 x ultimate [MAINLINE-024]; 210 MPa ultimate (thickest opened gauge, 250 um row) [MAINLINE-024]

**Original030 needed:** A datasheet or test for the film allowable [CHECK-011b]; A sourced film allowable [MAINLINE-024]; Creep-rupture fraction for each film [MAINLINE-024]; Data at design thickness [MAINLINE-024]

**Current030b:** 022d screened equilateral Zylon/CFRP gives 1.258252 cap and 1.251857 membrane on the 5% reserve, 1.194121/1.187858 on 019. Mylar and Kapton remain below one. The new film capacity is a corrected projection, not a material demonstration.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N024 | NFI-CHK011B-FILM | 030 retained | The film co-binds in most restated rows (SF 2.514/s). Its 1.5 GPa allowable has no datasheet (I-SIG), so it sits on the critical path of every SiC row at SF 1 or above. | [rpt-check011b-opus-1020](610aec93220adcc1-NFI.json) |
| N082 | NFI-FILM-ALLOWABLE-011B | 030 retained | 1.5 GPa and 80 um at 970 kg/m3 are the 011b pin. They are not a candidate allowable. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N084 | NFI-KNOCK-HALF | 030 retained | Where no creep-rupture fraction was opened, the design stress is half the opened ultimate. Kapton, Teonex and Vectran use it. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N089 | NFI-PEN-THICKNESS | 030 retained | The design thickness is above the 250 um row. The 210 MPa ultimate is the thickest opened gauge, not a measurement at the design thickness. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N090 | NFI-PEN-NOT-DESIGN-DATA | 030 retained | The IEC Teonex sheet says its typical values are not design data. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N091 | NFI-MYLAR-STRENGTH | 030 retained | The barrier brochure has no PET strength, modulus, density or creep. The 12 um mass is not computed. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N126 | NFI-005-FILM | 030 retained | {"NFI_id": "NFI-005-FILM", "gap": "Film allowable 1.5 GPa is inherited from MAINLINE-001 with no pinned datasheet (inherited NFI-FILM). The film passes at SF 2.51 on that value.", "direction": "Pin one film datasheet; required allowable 5.966e8 Pa is the bar it must clear.", "effect": "A real film below 5.966e8 Pa allowable would govern P3 and P3-A."} | [rpt-ref-eb07faa637b7487d6dc5](c108cdbb9f3bcf68-NFI.json) |
| N152 | NFI-011-FILM | 030 retained | {"NFI_id": "NFI-011-FILM", "gap": "The film allowable 1.5e9 Pa is an owner assumption with no datasheet, and wrinkling, puncture, sag area and shear transfer to members are unmodelled. For aluminum the film never binds (>=0.838 at the best point), but for SiC and the CNT projection it is the second limit and binds from s=1.0.", "direction": "Pin a real film (material, thickness, seaming) before crediting any SiC-family margin.", "effect": "SiC-family rows are film-capped in reality until the film is real."} | [rpt-ref-f21d4bd21d2026511818](0f1373271ca0676e-NFI.json) |
| N248 | NFI-FILM | 030 retained | {"NFI_id": "NFI-FILM", "linked_inputs_or_points": "P3 film", "questionable_assumption_or_gap": "Allowable, density and thickness are not one published film. Pocket radius set equal to spacing.", "direction_of_further_investigation": "Pin one film datasheet and a local pocket test.", "how_it_affects_margin_or_SF": "Film pressure scales with allowable and thickness. Film mass scales with density and thickness."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |
| N258 | NFI-FILM | 030 retained | {"NFI_id": "NFI-FILM", "gap": "Film allowable stays the owner value from MAINLINE-001 and is not aluminum yield.", "direction": "Pin one film datasheet.", "effect": "Film pressure is reported separately and can govern if it is the least."} | [rpt-mainline002-grok-strength-card-1019](b155c07e690eaa66-NFI.json) |
| N314 | NFI-011B-LOCAL-FILM | 030 retained | Local buckling remains 0.6*E*t_w/r_o with gamma=1. The film allowable remains 1.5 GPa with no datasheet. Both are open, carried from 011. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N359 | NFI-022-FILM | 030 retained | {"id": "NFI-022-FILM", "today": "Mylar 850H, tensile MD 22 kpsi, density 1.40 g/cc, O2 transmission 6.0 cc/100 in 2/day at 48 gauge and 1 atm.", "scored_thickness_m": 4.793113556654862e-05, "scored_sigma_Pa": 151684660.449916, "permeation_kg_per_day": 0.03619834160684392, "permeation_pct_of_1pct_budget": 0.07403368420145287, "method": "MAINLINE-016: 1 percent of lift per day is 48.894 kg, and permeance is converted as scc to mol to kg at p_ext. Mylar transmission is scaled as 1/thickness from the 48-gauge line.", "projection": "The 011 film, 1.5 GPa at 970 kg/m3, has no datasheet. It is the film optimism.", "source": "https://polymerfilms.com/wp-content/uploads/2023/09/Mylar850H-Datasheets.pdf", "state": "PENDING-024. This card carries the 011b film: 1.5 GPa, 970 kg/m3. Mylar exists and is the sourced-today comparison. The 1.5 GPa film is a PROJECTION. MAINLINE-024 owns the film, its thickness and the vacuum permeation. Seams are not in the Mylar figure."} | [rpt-mainline022-grok-p3-optimistic-floating-point-1020](307ab133da904ca4-NFI.json) |
| N383 | NFI-025-FILM-MARGIN | 030b addition | Optimistic reoptimized SiC point is also limited by inherited film strength and has zero spare float mass.; A surrogate SF above1 at exactly the float mass is not demonstrated practical levitation margin. MAINLINE-024/022b owns the film-sag/lift correction. This card preserves the inherited budget for reproducible comparison; zero spare mass cannot absorb the cited loss without changing tube mass and demands. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N415 | NFI-CHK024-ALLOWABLES-AND-GAUGE | 030b addition | Half-ultimate Kapton/PEN/Vectran values are assumptions, not creep-rupture allowables. Kapton design gauge 843 um exceeds opened 12.7-125 um rows; PEN 927 um exceeds the 250 um strength row and transfers 25 um modulus/permeability. Kapton 115.5 MPa exceeds its 69 MPa stress at 3% yield and 90 MPa at 5% strain. Long-term shape is unqualified. | [rpt-ref-7d6892c4e55be16ad523](1b8584393478c427-NFI.json) |
| N492 | NFI-031-P3-MATERIAL-FILM | 030b addition | The passing P3 keeps a 3900MPa SiC tube compression value, 410GPa modulus, 1.5GPa/970kg/m3 film and metre-scale thin curved tubes. These are not a demonstrated assembly or a safe tensile/bending allowable. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N569 | NFI-037-P3-BASELINE | 030b addition | In-band Mylar stays at 0.4105 by Perry and titanium/Kapton at 0.7412 by global after the flight gust. A proportional tube-wall increase is 5863 kg and 1634 kg. The lift does not have that margin. Sun and wind are not the gap. | [rpt-ref-8c5de04c9c33dbcf7447](f9ff7da1d21d1380-NFI.json) |
| N571 | NFI-CHECK-031-PASS-CONDITIONS | 030b addition | The P3 pass uses 3900 MPa, a typical property, and a 1.5 GPa film. The lapse with constant vapour fraction is a projection. The C=0 roots at -23.190 m and -1015.877 m are below sea-level ground. | [rpt-ref-be337d7d2ce1259d0aff](68d5541c02f9b231-CHECK-NFI.json) |
| N610 | NFI-017b-FILM-RULE | 030b addition | 024's half-of-tensile design rule is carried to every film in the trend (Upilex-S comparison); barrier, creep and seaming are not scored. The 1975 Kapton H row prints no density; Kapton HN's 1420 is used.; Film design allowables with barrier and creep for Upilex-S class films. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |

## T20 — Tolerance maps

<a id="R069"></a>
### R069 — 015 tolerance map conventions (lambda, nu) and inversion range; Lee 2016 envelope (015b)

**Original030 unknown:** Amplitudes at kd 0.5, 0.7 and 0.9 are lambda_I = 1 values; worst-width amplitudes are smaller, so the inverted table is optimistic in width.

**Original030 today:** kd 0.3 ceiling below 197.052 mm (P2-E), 73.17 mm (014b Be), 39.05 mm (014 Be) [MAINLINE-015]; least SF 0.6686 at kd 0.20; kd 0.2991 lifts only the global mode [MAINLINE-015]; P2-E factor 1.82 (0.46 mm RMS allowance looser than 0.25 mm) [MAINLINE-015]; ratio 293.1 on P2-E [MAINLINE-015]

**Original030 needed:** digitised worst-width envelope at delta/t below 1 [MAINLINE-015]; re-optimised split with kd 0.519 (face yield) for SF 1 [MAINLINE-015]; none [MAINLINE-015]; the min-over-width envelope [MAINLINE-015]

**Current030b:** 015b/CHECK-015b repair the lambda/nu width mismatch: old/live RMS 2.6112627. Actual-gamma 021/021b RMS .139344/.654416 mm. The SF 1 threshold .518304077 is unchanged. Rounding and wide-wave area qualifications remain.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N172 | NFI-015-KD03-AMPLITUDE | 030 retained | Eq 3 floors at 0.45, so kd 0.3 has no lambda_I = 1 amplitude. The worst-width curve is pinned only at its plateau 0.2338 and by the one-thickness statement, kd about 0.20-0.25 at delta equal to t. kd 0.3 sits on the unretrieved rising branch between those pins. No pair is interpolated. The aluminium-honeycomb beryllium point has R/t_eq 136.7, inside the fit range 100-1550, so the missing amplitude is the floor, not the range. P2-E at R/t_eq 50.75 remains outside that range. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N173 | NFI-015-BE-WRINKLING | 030 retained | The 014b beryllium point on CR-III 5056 at 1.6 pcf has least SF 0.668649769508548 by global buckling at kd 0.20. Face wrinkling on that same split is 0.6688 and does not contain kd. Raising kd to 0.2991 brings only the global mode to SF 1. The least factor stays 0.6688. Re-optimising the mass split on the same core and the same structural mass reaches least SF 0.8536 at kd 0.3 and crosses 1 at kd 0.519 by face yield. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N174 | NFI-015-GAP-DIRECTION | 030 retained | The gap factor is required tolerance divided by the achieved figure. Above 1, manufacture is already inside the allowance. The partial's sentence that kd 0.9 needs 1.8 times better than the GBT assembled surface reads the P2-E factor 1.82 the other way. On P2-E the 0.46 mm RMS allowance is looser than 0.25 mm. On the aluminium beryllium point the 0.10 mm RMS allowance is tighter than 0.25 mm and looser than 0.05 mm. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N175 | NFI-015-PRESSURE-RATIO | 030 retained | The partial's prose says the gyration thickness and the bending thickness give classical pressures 3.42 times apart. On P2-E, Zoelly's pressure at t_eq divided by the COMMON sandwich pressure is 293.1. The 3.42 figure is not that ratio. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N176 | NFI-015-WORST-WIDTH-RISING-BRANCH | 030 retained | The kd-versus-amplitude relation is closed-form only at width lambda_I = 1. The worst-width curve is pinned at its plateau 0.2338 and by the one-thickness statement. Amplitudes at kd 0.5, 0.7 and 0.9 are lambda_I = 1 values. Worst-width amplitudes at those levels are smaller. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N178 | NFI-015-FIT-RANGE-FLOOR | 030 retained | Eq 3 was fit over R/t 100-1550 and nu near 0.5. P2-E sits at R/t_eq 50.75 with nu 0.33. The aluminium beryllium point sits at 136.7 and is inside the R/t window. The Poisson mismatch remains on both. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N179 | NFI-015-HT-EQ32-UNRESOLVED | 030 retained | Hutchinson and Thompson 2018 Eq 3.2, the lower envelope over dimple width, was not resolved from the primary. It is not used. The rising branch is Baizhikova 2026 Eq 3, which meets Jimenez at the shared plateau (0.4470 against 0.45). | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N183 | NFI-015-PNAS-EXTRAPOLATION | 030 retained | The PNAS 2024 random-field design values are evaluated at R/t_eq 50.75 by scaling N with sqrt(R/t). Their fits span R/t 100-400. The reproduced anchors are 0.278 and 0.320 at R/t 100. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N384 | NFI-015B-WIDTH-NU | 030b addition | The filed 015 prominent RMS paired a lambda_I = 1 amplitude with a lambda_I = 2.625 width, and the widths used nu 0.30 while COMMON and the 015 inputs declare 0.33. The live map carries nu 0.33 only and matches width to amplitude at lambda_I = 1. The filed column is 2.611 times the live single-dimple RMS. | [rpt-ref-74e882831c201b1a953c](647d16ffad5d78ae-NFI.json) |
| N385 | NFI-015B-EQ3-REGIME | 030b addition | Baizhikova 2026 Eq. 3 is a lambda_I = 1 fit over R/t 100 to 1550 at nu 0.5, and the paper excludes delta/t below about 0.07. The kd 0.9 inverse is delta/t 0.0323. P2-E is at R/t 50.75. The 015 beryllium point is at 136.67, the 021 point at 274.19, and the 021b point at 187.39. | [rpt-ref-74e882831c201b1a953c](647d16ffad5d78ae-NFI.json) |
| N386 | NFI-015B-LEE-RANGE | 030b addition | Lee 2016 Eq. 23 is the lower envelope over k from 1 to 5, computed at R/t 100 and 200. Section 7 gives no FEM result below delta/t 0.15 and no ODE result below 0.2. The envelope does not fix one width. None of these shells is at R/t 100 or 200. At kd 0.9 and 0.7 the inverse is below 0.15. At kd 0.595 it is between 0.15 and 0.2. At kd 0.5, 0.468, 0.3 and 0.2 it is at or above 0.2. | [rpt-ref-74e882831c201b1a953c](647d16ffad5d78ae-NFI.json) |
| N406 | NFI-021B-CHECK-TOLERANCE | 030b addition | The two filed RMS values use nu=.30 for angular width, while mechanics inherit nu=.33. More substantially, amplitude is inverted from a lambda_I=1 fit and then the RMS width is set to 2.625; that is not a single defect with a demonstrated knockdown/amplitude/RMS tuple.; 45.819441 mm amplitude reproduces. With width nu=.33, the same lambda_I=1 Gaussian gives 0.654416 mm whole-sphere RMS; merely changing width gives 1.717842 mm, not a validated tolerance at the same knockdown. The filed 1.708852 mm is reproduced with width nu=.30. | [rpt-ref-444ac46ffbede876f9cd](e22bbb97f4477a6d-NFI.json) |
| N466 | NFI-015-CHECK-SMALL-DEFECT | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N467 | NFI-015-CHECK-LOW-KD-ENVELOPE | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N477 | NFI-015B-CHECK-ROUNDING-PROSE | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N478 | NFI-015B-CHECK-RMS-AREA | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N479 | NFI-015B-CHECK-LEE-CRITICAL-WIDTH | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |

<a id="R070"></a>
### R070 — tolerance maps from monocoque shells transferred to sandwich (core shear, waviness, boundaries)

**Original030 unknown:** Core shear cut to classical pressure is derived, but its cut to imperfection sensitivity has no coefficient; kd levels carry no shear correction.

**Original030 today:** core shear cuts classical pressure 10.3, 7.0, 0.8 percent on P2-E at 9, 14, 138 MPa [MAINLINE-015]; a locally 10 percent thin face costs 10.0 percent of P2-E classical pressure [MAINLINE-015]; hydrostatic column 240 Pa, 0.25 percent of case pressure [MAINLINE-015]

**Original030 needed:** a shear-flexible imperfection study [MAINLINE-015]; autoclave and core-machining tolerances when the build is chosen [MAINLINE-015]; a separate card for any equator the design keeps [MAINLINE-015]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N180 | NFI-015-CORE-SHEAR-SENSITIVITY | 030 retained | Core shear's cut to the classical pressure is derived: 10.3, 7.0 and 0.8 percent on P2-E at 9, 14 and 138 MPa, and 11.4 percent on the aluminium core at 72.4 MPa. The cut to imperfection sensitivity has no retrieved coefficient. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N181 | NFI-015-THICKNESS-WAVINESS-VALUES | 030 retained | The thickness sensitivity is derived. A locally 10 percent thin face costs 10.0 percent of P2-E classical pressure. No sourced cure tolerance for the faces or the core was retrieved. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N184 | NFI-015-BOUNDARY-AND-TRANSIENT | 030 retained | Full-sphere curves are used. A clamped equator can cap kappa near 0.8 for a small dimple. The static hydrostatic column is 240 Pa, 0.25 percent of the case pressure. Pump-down transients are not modelled. | [rpt-ref-06668dbf12580ed0ffc3](32fd0bf058dd6218-NFI.json) |
| N387 | NFI-015B-SANDWICH | 030b addition | Both curves are monocoque results transferred through t_eq = sqrt(3)(core+tf). No sandwich measurement at this radius was retrieved. Core shear's effect on imperfection sensitivity has no coefficient. A single-dimple RMS is not an assembled-surface RMS. | [rpt-ref-74e882831c201b1a953c](647d16ffad5d78ae-NFI.json) |
| N468 | NFI-015-CHECK-EFFECTIVE-MODULUS | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N476 | NFI-015-CHECK-MODEL-VALIDATION | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N603 | NFI-017b-GAMMA-TRANSLATION | 030b addition | The brief's translation of gamma into core shear stiffness per density cannot reach SF 1 (Kc caps at 1). As shape precision, MAINLINE-015's monocoque-equivalent map (t_eq = sqrt(3) h) gives a 2.47 mm dimple at R 10 and 13.1 mm at R 20; that map is a cylinder/monocoque fit applied to a sandwich sphere.; An imperfection-controlled sandwich-sphere or dome buckling test series. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| N660 | NFI-038-IMPERFECTION | 030b addition | Maximum dent alone does not preserve buckling similarity | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N676 | NFI-C035-TRANSFER | 030b addition | The 0.30–0.34 handbook ratio and SBKF-scaled sphere envelope are projections. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N687 | NFI-C035-IMPERFECTION | 030b addition | The record does not establish that required imperfection control exceeds every recorded sandwich dome. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |

## T21 — Geometry levers

<a id="R071"></a>
### R071 — geometry levers at equal margin (radius, altitude, partial vacuum)

**Original030 unknown:** 11000 m is evaluated on the tropospheric lapse at the tropopause boundary; the isothermal stratosphere is not used; no effect inside this grid.

**Original030 today:** 0.1 m core [MAINLINE-012]; troposphere lapse at 11000 m [MAINLINE-012]

**Original030 needed:** re-run levers with thickness re-solved at the float ceiling per radius [MAINLINE-010]; re-run lever 1 on their best rows when filed [MAINLINE-010]; A core thickness that scales with radius. [MAINLINE-012]; Hold T at 216.65 K above 11000 m if climbing further. [MAINLINE-012]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N144 | NFI-010-FIXEDTHICK | 030 retained | {"NFI_id": "NFI-010-FIXEDTHICK", "gap": "Levers 1 and 4 hold face and core thickness fixed while radius changes. A real design re-optimizes thickness per radius; the mass-ceiling rows of 002/003 show how much that moves things at 10 m only.", "direction": "Re-run the levers with thickness re-solved at the float ceiling per radius.", "effect": "Margins improve at small radius; SF rankings are not expected to flip."} | [rpt-ref-58b2bed18db2449100f2](21991360c704a696-NFI.json) |
| N147 | NFI-010-007008 | 030 retained | {"NFI_id": "NFI-010-007008", "gap": "MAINLINE-007 and 008 had not filed when this card closed, so lever 1 was not re-run on their best rows, as the brief's Then clause directs.", "direction": "Re-run lever 1 on their best rows when they file; the script here takes any tf/core row.", "effect": "None on this card's numbers."} | [rpt-ref-58b2bed18db2449100f2](21991360c704a696-NFI.json) |
| N319 | NFI-CORE-FIXED | 030 retained | {"NFI_id": "NFI-CORE-FIXED", "gap": "P2-A keeps the 0.1 m core while radius and altitude change. That fixed core can exhaust the mass budget.", "direction": "A core thickness that scales with radius.", "effect": "An infeasible row has no safety factor."} | [rpt-mainline012-grok-equal-margin-1019](811b275dbd0d54b1-NFI.json) |
| N320 | NFI-TROPOPAUSE | 030 retained | {"NFI_id": "NFI-TROPOPAUSE", "gap": "11000 m is evaluated on the tropospheric lapse at the tropopause boundary. The isothermal stratosphere is not used.", "direction": "Hold T at 216.65 K above 11000 m if a later card climbs further.", "effect": "None inside this grid. 11000 m is the top row."} | [rpt-mainline012-grok-equal-margin-1019](811b275dbd0d54b1-NFI.json) |

<a id="R072"></a>
### R072 — P3 member cap bounded continuation

**Original030 unknown:** P3 re-optimisation holds bay 0.4-3 m and member radius at most 0.25 m, which governs large hulls; similarity rows hold 80 um film so film SF falls as 1/R.

**Original030 today:** bay 0.4-3 m; member radius at most 0.25 m; film 80 um [MAINLINE-027]

**Original030 needed:** Relaxed member caps or thicker film costed as separate designs [MAINLINE-027]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N114 | NFI-027-FRAME-BOUNDARY | 030 retained | P3 reoptimization holds bay 0.4–3 m and radius≤0.25 m. The radius cap governs large hulls. Similarity rows separately scale members but hold 80 µm film, making film SF fall as 1/R. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |

<a id="R073"></a>
### R073 — thin-shell validity at low density

**Original030 unknown:** On the buckling split the core exceeds a tenth of the radius below about 1.8 kg/m3, so margins there are not physical.

**Original030 today:** B-split core 1.81 m at 1 kg/m3, 18.1 m at 0.1 kg/m3 [MAINLINE-013]

**Original030 needed:** thick-shell sandwich model with inner-surface area [MAINLINE-013]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N165 | NFI-013-GEOMETRY-B | 030 retained | On the buckling split the core exceeds a tenth of the radius below about 1.8 kg/m3 and the radius itself below about 0.18 kg/m3, so B-split margins there are not physical (external-area and thin-shell rules). | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |

## T22 — Metal strength transfer

<a id="R074"></a>
### R074 — face stress past yield elastic wrinkling

**Original030 unknown:** The 6061 face exceeds its questionable 276 MPa yield on every row, so elastic wrinkling forms flatter it.

**Original030 today:** face stress 3.57e8 to 7.09e8 Pa against 276 MPa [MAINLINE-013]

**Original030 needed:** a face change (008b) or plasticity factors from CR-1457 section 9 [MAINLINE-013]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N164 | NFI-013-FACE-YIELD | 030 retained | The 6061 face is past its QUESTIONABLE 276 MPa on every row, so the elastic wrinkling forms (eta 1) flatter it. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N448 | eta | 030b addition | The page says elastic cases use eta = 1, and inelastic cases use section 9. The map uses eta = 1. The 021 faces sit at compression safety factor about 1, so a plasticity factor may apply. It is not in this Q map. | [rpt-mainline032-grok-wrinkle-waviness-1020](df2ac0989ca4f688-NFI.json) |
| N531 | NFI-032-CHECK-ETA | 030b addition | non_blocking | [rpt-ref-a30a669ed3e245f1473b](f4fb2c3464ed42c3-NFI.json) |
| N628 | NFI-032-CHECK-ETA | 030b addition | non_blocking | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |

<a id="R075"></a>
### R075 — tensile yield used as the compressive allowable (aluminium and others)

**Original030 unknown:** 276 MPa typical tensile yield is transferred to compression by owner assumption; source says typical values are not for design; no compressive yield was retrieved.

**Original030 today:** 276 MPa tensile yield used in compression [MAINLINE-007]; 276 MPa typical tensile yield used as compression [MAINLINE-005]; tensile yields transferred to compression for four metals [MAINLINE-008]; 276 MPa; all-face SF 0.7773844341284152 [CHECK-MAINLINE-007]

**Original030 needed:** A compression yield or a design allowable [MAINLINE-007]; a compressive design allowable [MAINLINE-005]; measured compressive yield per temper and product form [MAINLINE-008]; MMPDS allowables at about 285 K. [rpt-mainline-grok-estimates-card-1019]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N028 | NFI-AL-YIELD-CARRY | 030 retained | {"NFI_id": "NFI-AL-YIELD-CARRY", "gap": "276 MPa remains the inherited AA typical tensile yield, transferred to compression. Strength safety factors are QUESTIONABLE.", "direction": "A compression yield or a design allowable can replace the transfer.", "effect": "Yield cannot reach safety factor 1 on this ceiling. The all-face factor on 276 MPa is 1.28636483585. At the named least-factor peak the factor is 1.35679953494. Where buckling safety factor first reaches 1 the strength factor is 2.57095082176."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N123 | NFI-005-SIGMA | 030 retained | {"NFI_id": "NFI-005-SIGMA", "gap": "276 MPa is a QUESTIONABLE typical tensile yield transferred to compression (inherited NFI-AL-YIELD-CARRY). Required strengths here are membrane stresses and do not depend on it; only the x276 MPa multiples and SF labels do.", "direction": "Obtain a compressive design allowable and rescale the multiples only.", "effect": "No required Pa value in this card moves."} | [rpt-ref-eb07faa637b7487d6dc5](c108cdbb9f3bcf68-NFI.json) |
| N133 | NFI-008-SIGMA-TRANSFER | 030 retained | 6061-T6, 7075-T6, 2195-T8 and AlBeMet 162 compressive strengths are tensile yields transferred to compression; AZ31 uses a compressive yield, Ti-6Al-4V and Be S-200F use compressive values, SiC a compressive ultimate, Vitreloy 1 a compressive ultimate. | [rpt-ref-45da79edf548b064b228](6284193a78be0578-NFI.json) |
| N243 | NFI-AL | 030 retained | {"NFI_id": "NFI-AL", "linked_inputs_or_points": "I-E I-RHO-AL I-NU", "questionable_assumption_or_gap": "Room-temperature typical properties, Poisson estimated.", "direction_of_further_investigation": "MMPDS allowables at about 285 K.", "how_it_affects_margin_or_SF": "E scales collapse linearly in all three models. Density scales metallic mass."} | [rpt-mainline-grok-estimates-card-1019](2d0dc7b9973fdc16-NFI.json) |
| N253 | NFI-AL-YIELD-CARRY | 030 retained | {"NFI_id": "NFI-AL-YIELD-CARRY", "gap": "276 MPa is the retrieved AA typical tensile yield. It is transferred to compression by owner assumption. The sheet says AA typical values are not for design. No compressive yield was in the retrieved snippet.", "direction": "Obtain a compression yield or design allowable and drop the transfer.", "effect": "Aluminum-strength pressure and its factor scale linearly with this value."} | [rpt-mainline002-grok-strength-card-1019](b155c07e690eaa66-NFI.json) |
| N261 | NFI-AL-YIELD-CARRY | 030 retained | {"NFI_id": "NFI-AL-YIELD-CARRY", "gap": "276 MPa remains the inherited AA typical tensile yield, transferred to compression. Strength safety factors are QUESTIONABLE. The carry is parallel and is not a gate.", "direction": "A compression yield or design allowable can replace the transfer.", "effect": "Strength pressure and the required compressive strength scale linearly with this value."} | [rpt-mainline003-grok-p2-targets-1019](2090c6e1f4ca8afb-NFI.json) |
| N274 | NFI-AL-YIELD-CARRY | 030 retained | {"NFI_id": "NFI-AL-YIELD-CARRY", "gap": "003 strength safety factors stay QUESTIONABLE and unchanged. Buckling knockdown does not cure yield, shear, wrinkling or crush.", "direction": "Keep the carry parallel.", "effect": "Strength safety factor is not rescaled."} | [rpt-mainline004-grok-knockdown-card-1019](e0152663a63bcf24-NFI.json) |
| N283 | NFI-STRENGTH | 030 retained | {"NFI_id": "NFI-STRENGTH", "gap": "Strength safety factors stay at the sealed 003 QUESTIONABLE values. Knockdown does not rescale yield.", "direction": "Leave strength on its own card.", "effect": "Strength safety factor is unchanged at every knockdown."} | [rpt-mainline004b-grok-kd-range-1019](f528292663aa7701-NFI.json) |
| N287 | NFI-YIELD | 030 retained | {"NFI_id": "NFI-YIELD", "gap": "Confirmed: yield is 276 MPa tensile yield transferred to compression, QUESTIONABLE.", "direction": "A compression allowable.", "effect": "Yield SF scales linearly with that allowable."} | [rpt-mainline006-check-lead4f19-1019](8060138631058409-NFI.json) |
| N291 | NFI-YIELD | 030 retained | {"NFI_id": "NFI-YIELD", "gap": "Yield uses 276 MPa tensile yield transferred to compression. QUESTIONABLE.", "direction": "A compression allowable.", "effect": "Yield SF scales linearly with that allowable."} | [rpt-mainline006-grok-float-margin-1019](c433e7ad1bc469c3-NFI.json) |
| N294 | NFI-AL-YIELD-CARRY | 030 retained | {"NFI_id": "NFI-AL-YIELD-CARRY", "gap": "Confirmed: 276 MPa is a typical tensile yield transferred to compression, QUESTIONABLE. Yield cannot reach SF 1 on this ceiling: all-face SF 0.7773844341284152, strength factor 1.28636483585 with no core, 1.35679953494 at the named peak, 2.57095082176 where buckling first reaches 1.", "direction": "A compression yield or design allowable.", "effect": "Owner statement stands."} | [rpt-mainline007-check-lead4f19-1019](a27128f0dc1713bc-NFI.json) |

## T23 — PROJECTION materials

<a id="R076"></a>
### R076 — CNT and graphene materials (PROJECTION)

**Original030 unknown:** Cheapest P2 direction on all three leaders is lower face density alone, needing faces near 0.9-1.1 g/cc with CNT, Be and graphene E and sigma; all PROJECTION.

**Original030 today:** lightest questionable face T700 at 1550 kg/m3 [MAINLINE-017]

**Original030 needed:** Production allowable and thickness [MAINLINE-024]; a demonstrated QI CNT-yarn or graphene laminate card [MAINLINE-008]; Structural face at about 0.9-1.1 g/cc (959.5, 1129.7, 906.5 kg/m3) with those E and sigma. [MAINLINE-017]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N097 | NFI-CNT-GRAPHENE | 030 retained | No production allowable was opened. Thickness is not stated. | [rpt-ref-4f09fd6b4c4dd848ebb0](9c93ce0d2b5d8d46-NFI.json) |
| N136 | NFI-008-PROJECTIONS | 030 retained | CNT-yarn and graphene QI rows are PROJECTION scenarios, not available materials; their assumed values are stated per row. | [rpt-ref-45da79edf548b064b228](6284193a78be0578-NFI.json) |
| N350 | NFI-017-FACE-DENSITY | 030 retained | {"NFI_id": "NFI-017-FACE-DENSITY", "gap": "The cheapest P2 direction on all three leaders is face density alone (factors 1.459, 1.637, 1.655), requiring faces at 959.5, 1129.7 and 906.5 kg/m3 carrying CNT, Be and graphene E and sigma. The lightest QUESTIONABLE face today is T700 at 1550 kg/m3.", "direction": "A structural face at about 0.9-1.1 g/cc with those stiffness and strength values.", "effect": "All three are PROJECTION. Beryllium itself cannot get lighter; that direction is a different face carrying Be-like properties."} | [rpt-mainline017-improvement-directions-lead4f19-1019](9f3c760a855408f0-NFI.json) |

## T24 — Method and provenance

<a id="R077"></a>
### R077 — 013 source quality (figure-read, second-hand, unopened sources)

**Original030 unknown:** A list of paywalled sources was not opened, so none of their values is used; the stiffer ultralight ceramic octet point may be among them.

**Original030 today:** 1.1 GPa and 10.2 MPa (secondary Jacobsen) [MAINLINE-013]; read-off uncertainty about 25 to 50 percent [MAINLINE-013]

**Original030 needed:** primary papers opened and values matched [MAINLINE-013]; tabulated values from journal SI or theses [MAINLINE-013]; obtain those texts and add values through build_cores.py [MAINLINE-013]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N160 | ref-ce7077da95749d9c1df0 | 030 retained | Two values arrive second-hand: the vitreous carbon octet micro-lattice (Jacobsen 2011, via Zhang 2019) and the glassy carbon exponents (Bauer 2016, via Zhang 2019); Schaedler 2011's 10 kg/m3 nickel point also via Zhang 2019. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N161 | NFI-013-FIGURE-READS | 030 retained | Maloney 2013, Zheng 2016, Meza 2014, Meza 2015 and Zhu 2015 values are read by eye from log plots (about 25 to 50 percent); the Meza densities are inferred from relative density. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N171 | NFI-013-NOT-OPENED | 030 retained | Sources that were paywalled or blocked, so none of their values is used: Schaedler 2011 full text and SI, Torrents 2012, Valdevit 2013, Salari-Sharif 2014, Zheng 2014 (Science 344, 1373), Jang 2013, Deshpande-Ashby-Fleck 2001, Gross and Fricke 1995, Woignier 1989 full text, Ma 2000 full text, Sun 2013, Hu 2013, Zou 2010, Gui 2010, Worsley 2009 and 2012, Mecklenburg 2012, Eckel 2016, Bauer 2016, Jacobsen 2011. | [rpt-ref-44f9940325e236cb80b3](fe5e5ec3daad9605-NFI.json) |
| N472 | NFI-015-CHECK-SOURCE-IDENTIFIERS | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N522 | NFI-035-EYE-READ | 030b addition | CR-1457 Fig. 4.2-3 and Fig. 6.2-3 values are read by eye from page images, by the B and C researchers and independently by this seat; about +/-0.02 in gamma and +/-10% in R/rho. | [rpt-mainline035-opus-knockdown-tests-1020](4099579f3f8b5d1d-NFI.json) |
| N523 | ref-5e993e8eb72d4845aa62 | 030b addition | Not retrieved: FPL 1830 (March and Kuenzi 1957; DTIC 403, FPL 502 from here), Baker AIAA J 1968, the Hexcel summary of 25 Jul 1963, FPL PE-227, Kazimi 1960. Per-specimen geometry and Vc of the pre-1969 cylinders stay unknown. | [rpt-mainline035-opus-knockdown-tests-1020](4099579f3f8b5d1d-NFI.json) |
| N524 | NFI-035-DESICOS | 030b addition | Measured buckling of the Ariane 5 SYLDA/ISS sandwich shells (Bisagni 2016) is in a restricted paper; Alfano and Bisagni 2017 give only geometry, FE and SP-8007 0.57/0.64. | [rpt-mainline035-opus-knockdown-tests-1020](4099579f3f8b5d1d-NFI.json) |
| N525 | NFI-035-DOME-LEADS | 030b addition | Brix 1968 (GFP sandwich domes under external pressure) and Anderson 1966 (Georgia Tech, spherical sandwich shell) are unread leads; either may hold the only sandwich-dome test series. | [rpt-mainline035-opus-knockdown-tests-1020](4099579f3f8b5d1d-NFI.json) |
| N611 | NFI-017b-TREND-GAPS | 030b addition | Eras not found: beryllium datasheets of about 2006 and 2016; Hexoloy datasheets of about 1996 and 2016; any carbon-honeycomb history; Wright 1965 and JGJ 7-2010 (the lattice 0.4 and 0.2) were not read; Krenzke 1963 not opened. Identical Hexcel tables may mean no re-testing rather than no progress.; The missing datasheets (Wayback rate limits blocked some). | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| N678 | ref-196608af78549ed7f1ff | 030b addition | Primary Baker, FPL, Hexcel and Kazimi specimen reports remain unread. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N679 | NFI-C035-BRIX | 030b addition | Brix 1968 sandwich-dome paper remains an unread experimental lead. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N680 | NFI-C035-SIM | 030b addition | 035's Vc≈200, R/rho≈26 and crimp ratios 1.44–1.54 have no independently reconstructed chain here; Sim's uniform-pressure results are FE. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N682 | NFI-C035-TANG-MARINE | 030b addition | Tang's 2025 elliptical steel/resin pressure-hull experiment is an abstract-level lead. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N683 | NFI-C035-TANG-JSSM | 030b addition | Tang's three sandwich ellipsoids use a stronger/stiffer core; applicability to a soft-core model is unresolved. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N684 | NFI-C035-BARATHAN | 030b addition | The owner's C05 semi-ellipsoid hydrostatic experiment was omitted from its categorical conclusion. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N685 | NFI-C035-DENARDO | 030b addition | A documented foam-core cylinder experiment contradicts the card's no-test claim; full thesis access failed. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| N688 | NFI-C035-RESTRICTED | 030b addition | Restricted DESICOS and other abstract-only leads prevent an exhaustive claim about modern cylinder data. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |

<a id="R078"></a>
### R078 — 1/least SF is not property multiple

**Original030 unknown:** 1/least SF is the safety-factor gap and equals the property multiple only when the mode scales proportionally; wrinkling scales as a cube or square root.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N328 | NFI-FACTOR | 030 retained | 1/least SF is the safety-factor gap. It is the property multiple only when that mode scales in proportion to the named property. Wrinkling scales as a cube root or a square root. | [rpt-mainline014-grok-balanced-sandwich-1019](e0fba238a74bd426-NFI.json) |
| N345 | NFI-FACTOR | 030 retained | 1/least SF is the safety-factor gap. It is the property multiple only when that mode scales in proportion. Wrinkling scales as a square root or a cube root. Dimpling scales as tf cubed. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |

<a id="R079"></a>
### R079 — documentation and provenance defects (no numeric effect)

**Original030 unknown:** Owner caveats stand: volume ignores intrusion; joints 5% and systems 100 kg inherited; no sourced Gc/Ec core at 8-1 kg/m3; datasheet disagreements kept; microlattice 0.9 kg/m3 is density only.

**Original030 today:** Notes say 12 um cell, N 20, rel. density 0.000104; table gives 8 um, N 10, 0.00182 [CHECK-MAINLINE-013]; payload 0 kg both lines; 100 kg sensitivity [CHECK-019]; 53 verified/measured pins in INPUTS [MAINLINE-027]; RESULTS.json 59234 bytes filed vs 67862 observed; float021.py 31581 vs 36429 [CHECK-rpt-ref-e92af61311c9bf4a89cd]

**Original030 needed:** Correct the notes field only [CHECK-MAINLINE-013]; Correct text, pin 011 inputs, relabel two_way rows [CHECK-011b]; Correct the id; state payload handling [CHECK-019]; Normalised throughput, exact p/T climate calculation, variable-pressure integral; measured ground pump-down energy [MAINLINE-019]

**Current030b:** Every original 030 source row and both citations of N023 are preserved. CHECK-030 confirms 362 unique rows versus 363 original pointers. Source-file provenance mismatches from earlier rewritten artifacts remain in the baseline index.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N010 | NFI-CHECK013-MEZA-SPECIMEN-NOTE | 030 retained | Architecture field is correct; notes copy the lightest specimen into the heaviest record. | [rpt-1228-mainline013-independent-check-1020](ef406b56c4cff82e-NFI.json) |
| N023 | NFI-CHK011B-TEXT | 030 retained | M1: the report body says 'k 0.4 and 0.5 are in the card', but the CARD.md table carries k 1, 0.4 and 0.2 (k 0.5 is in RESULTS.json only). M2: INPUTS.json materials carry no source and 011's INPUTS.json, which holds them, is not pinned. M3: Buchert 1968 prints the card's Et and D, so it can be cited. M4: the 'two_way' rows are the triangulated frame scored with C = 4, not a two-way frame, which would have zero in-plane shear stiffness (C1212 = 0). | [rpt-check011b-opus-1020](610aec93220adcc1-NFI.json) |
| N026 | NFI-CHK019-TEXT | 030 retained | M1: the order cites rpt-ref-ea73d14ec4d4d8963f76; the filing is rpt-ref-d7f99cd71e977826da48. M2: the brief asks every line item for an optimistic and a conservative value; payload is 0 kg on both lines, and the 100 kg payload is only a sensitivity on the optimistic case. | [rpt-check019-opus-1020](9cc8bdcb82e9b2d1-NFI.json) |
| N081 | NFI-019-PREDECESSOR-ARITHMETIC | 030 retained | The inherited partial script was not runnable and omitted the 86400 divisor in gas throughput plus the g-to-kg conversion for getter mass. MAINLINE-016 used a linear temperature loss and a constant-final-ratio commissioning expression. | [rpt-ref-d7f99cd71e977826da48](fec518f4f7e18a36-NFI.json) |
| N116 | NFI-027-PROVENANCE | 030 retained | The dispatch names a nonmatching 019 report ID; actual verified ID uses lead-sci. Original 021 hashes are superseded by revision 1, which was used. Scientific uncertainty remains despite arithmetic checks. | [rpt-ref-2898e43e4928e833af6d](fecbe3eb74d15e6e-NFI.json) |
| N117 | NFI-CHECK021-PINS | 030 retained | [withheld: private quotation] | [rpt-ref-e92af61311c9bf4a89cd](0b74ca6f4252ee9e-NFI.json) |
| N140 | NFI-008B-BASIS | 030 retained | The quasi-isotropic moduli 54, 135, 210, 86 and 180 GPa are rounded products of their stated bases (53.6, 136.5, 211.15, 85.68, 179.2); the unidirectional compressive strengths behind 520, 350 and 220 MPa are unnamed. | [rpt-ref-cc9cef5e55adca018a8f](cbad32790fc5fde1-NFI.json) |
| N284 | CHECK-NFI-1 | 030 retained | {"NFI_id": "CHECK-NFI-1", "gap": "Owner report body calls every baseline a sealed 002 baseline. P2-E/baseline (face 0.000248148148148 m, core 0.08375 m) is an equal-mass split constructed at the 002 P2 counted mass, not a sealed 002 geometry.", "direction": "Relabel that one row as the equal-split row at the 002 P2 mass. No number changes.", "effect": "Provenance only. All P2-E baseline numbers reproduce."} | [rpt-mainline006-check-lead4f19-1019](8060138631058409-NFI.json) |
| N293 | CHECK-NFI-1 | 030 retained | {"NFI_id": "CHECK-NFI-1", "gap": "No numeric mismatch was found. At the equal-factor split (densities 8, 6, 4, 3, 1) SF_b and SF_y are equal; a checker's strict inequality can label that tie either way by the last bit.", "direction": "Keep the card's both_equal label. No fix card.", "effect": "None. Least SF is unchanged."} | [rpt-mainline007-check-lead4f19-1019](a27128f0dc1713bc-NFI.json) |
| N298 | NFI-GEOM/MASS/RULE/CORE-FLOOR/DATASHEET/MICROLATTICE | 030 retained | {"NFI_id": "NFI-GEOM/MASS/RULE/CORE-FLOOR/DATASHEET/MICROLATTICE", "gap": "Confirmed as stated by the owner: external area/volume ignore intrusion (the 1 kg/m3 buckling-peak core is 1.8145766829090553 m); joints 5% and systems 100 kg are inherited; the splits optimise only buckling and QUESTIONABLE yield; no catalog core with sourced Gc, Ec and strength exists at 8-1 kg/m3; the Plascore psi/MPa and Divinycell rev7/rev9 disagreements are kept visible; the 0.9 kg/m3 microlattice is density only.", "direction": "Owner directions stand.", "effect": "None inside the compared numbers."} | [rpt-mainline007-check-lead4f19-1019](a27128f0dc1713bc-NFI.json) |
| N317 | NFI-011B-SKIP | 030 retained | The brief's last line names checks 006, 007 and 007b. The rotating order says those checks are already filed and are skipped here. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N353 | NFI-017-UNFILED | 030 retained | {"NFI_id": "NFI-017-UNFILED", "gap": "MAINLINE-014b, 011b and 013 had not filed at the start of this card. This card used 014, 009, 009b and 011 and named that. The 009b Kc restatement does not change the 014 leaders, which already carry Kc and sit on the crimping branch.", "direction": "Revisit if 014b or 011b lands a better point.", "effect": "The three best P2 points could change under 014b."} | [rpt-mainline017-improvement-directions-lead4f19-1019](9f3c760a855408f0-NFI.json) |
| N367 | NFI-030-HELD-020 | 030b addition | This seat finished a 020 check before it read the narrowing that moved 020 to ref-4189c1615990eb515921. The report was pulled from the outbox before ingest and is held unfiled at .ship/held/rpt-check020-opus-1020.json; its only new result (019's reserve at 020's stock and film, 1154.23 kg) is carried in R038 and agrees with 021b. | [rpt-mainline030-opus-register-1020](858f8f97e8cb24d5-NFI.json) |
| N390 | NFI-023-CHECK-FIRST-PINS | 030b addition | {"id": "NFI-023-CHECK-FIRST-PINS", "status": "open", "non_blocking": true, "field": "first report artifacts", "reported": "Five paths pinned under the initial973.7kN report.", "check": "All five now contain load-fix bytes. Current load-fix pins match; original full files unavailable at cited paths.43 preserved report quantities reconstruct.", "evidence": ["inputs/pin-audit.json", "REPORT-CHECK.csv"], "next": "Preserve distinct immutable version paths on future fixes; restore original versions only if already archived, without substituting reconstructed data."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N396 | NFI-023-CHECK-BRAZE-UNITS | 030b addition | {"id": "NFI-023-CHECK-BRAZE-UNITS", "status": "open", "non_blocking": true, "field": "mass_coefficients.sic_braze.C_end_per_area_1_per_N", "reported": "Coefficient labelled1/N in JSON and CARD.", "check": {"value": 1.9735212943395024e-05, "correct_units": "kg/(N*m), equivalently s^2/m^2", "equation": "m_end=C*A*N/r"}, "evidence": ["dimensional derivation CHECK.md"], "next": "Correct units and field label. Numeric coefficient itself is reproduced."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N420 | NFI-CHK024-INPUT-RECORD | 030b addition | Owner INPUTS primarily pins sources and upstream scripts; explicit gas constants and complete material/frame values are missing. This check supplies them and a fresh standalone calculation. | [rpt-ref-7d6892c4e55be16ad523](1b8584393478c427-NFI.json) |
| N453 | kommers | 030b addition | The card names Norris, Ericksen and Kommers. FPL Report 1810 is Norris, Ericksen and March. Kommers was not found on it. | [rpt-mainline032-grok-wrinkle-waviness-1020](df2ac0989ca4f688-NFI.json) |
| N474 | NFI-015-CHECK-PROJECTION-TAGS | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N475 | NFI-015-CHECK-PNAS-CONSISTENCY | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N481 | NFI-030-DOUBLE-CITE | 030b addition | Unique source ids are 362 and source pointers are 363. N023, row NFI-CHK011B-TEXT, is cited on R057 and on R079. The source note contains the two-way shear objection and the documentation defects together. | [rpt-ref-490f8e9228d526b69dc8](c637ae242ae817f5-NFI.json) |
| N504 | NFI-026-06 | 030b addition | Whole-tangent linearization failed mesh convergence; Rejected as primary linear buckling. Standard initial-stress calculation converges; full nonlinear calculations receive their own mesh comparison. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |
| N510 | NFI-026-12 | 030b addition | Execution diagnostics and receipt exception; All diagnostics retained; recovered child receipt distinguishes observed closure from unavailable exact outer end clock. No admission refusal was bypassed. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |
| N527 | NFI-035-PALETTE | 030b addition | The chart uses the dataviz skill's documented passing slots 1-3; its validator could not run here (no JavaScript runtime). Marker shapes carry identity as well. | [rpt-mainline035-opus-knockdown-tests-1020](4099579f3f8b5d1d-NFI.json) |
| N536 | NFI-032-CHECK-LEAD-RANGE | 030b addition | non_blocking | [rpt-ref-a30a669ed3e245f1473b](f4fb2c3464ed42c3-NFI.json) |
| N651 | NFI-038-SOURCE_STATE | 030b addition | P3 optimum changed during the card | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N677 | NFI-C035-CTA83 | 030b addition | The source's printed 0.864 conflicts with 432000/499246=0.8653048798. | [rpt-ref-d3afcdc3514000cb6fc2](064ba103ce9ab63c-NFI.json) |
| B005 | NFI-030B-EVIDENCE-LABEL | 030b addition | A demonstrated source-contract correction is not a demonstrated hull capability.; The Zylon directional factor is a demonstrated arithmetic/source mismatch in CHECK-022b/022c. New correction, measured coupon precedent, source absence and projected assembly capability remain distinct in this register. | [rpt-ref-39745602983887568501](02744dbf85113cc4-legacy--02744dbf85113cc4de64187c76ed79779e558031dadf21e6ad2f8aea21188dc1--AUTHORED-NFI.json) |

<a id="R080"></a>
### R080 — equal-mass separation convention

**Original030 unknown:** Whether face separation should follow face thickness when face density changes at equal mass; effect is second order against 0.1-0.16 m cores.

**Original030 today:** separation held at the row value [MAINLINE-005]; at most 0.348 percent of SF_b on P2-E [MAINLINE-08B]

**Original030 needed:** recompute E/rho with separation following tf for faces far from 2700 kg/m3 [MAINLINE-005]; folds into any future exact recompute [MAINLINE-08B]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N124 | NFI-005-SEP | 030 retained | {"NFI_id": "NFI-005-SEP", "gap": "P2 equal-mass figure holds face separation at the row value while face thickness follows 1/rho. A changed face density moves tf and so moves separation by the same amount, a second-order change against 0.1-0.16 m cores.", "direction": "Recompute E/rho with separation following tf if a candidate face material is far from 2700 kg/m3.", "effect": "Small optimistic or pessimistic shift in the P2 buckling figure for extreme densities."} | [rpt-ref-eb07faa637b7487d6dc5](c108cdbb9f3bcf68-NFI.json) |
| N141 | NFI-008B-SEP | 030 retained | At equal face mass the face-thickness change moves the separation slightly; the first-order scaling drops that term. The 008 checker measured the effect at most 0.348 percent of SF_b on P2-E (worst tf/d 0.00722). | [rpt-ref-cc9cef5e55adca018a8f](cbad32790fc5fde1-NFI.json) |
| N471 | NFI-015-CHECK-ONE-FACE | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |

<a id="R081"></a>
### R081 — omitted failure modes scope

**Original030 unknown:** Core shear, wrinkling, crush, laminate anisotropy, bond and thermal stress are omitted; SF_b is a first-order thin-face scaling.

**Original030 needed:** 005b for crush; later cards for shear, wrinkling, crippling [MAINLINE-005]; MAINLINE-004 knockdown for kd rescaling and a sandwich failure check per candidate [MAINLINE-008]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N127 | NFI-005-OMITTED | 030 retained | {"NFI_id": "NFI-005-OMITTED", "gap": "Core shear, face wrinkling, core crush, local crippling and end fixity remain outside these two limits, as in 002/003. Core crush is worked next as MAINLINE-005b.", "direction": "005b for crush; later cards for shear, wrinkling and crippling.", "effect": "Any omitted mode can only lower a row's true SF below the figures here."} | [rpt-ref-eb07faa637b7487d6dc5](c108cdbb9f3bcf68-NFI.json) |
| N135 | NFI-008-OMITTED-MODES | 030 retained | Core shear, face wrinkling, core crush, laminate anisotropy (nu, shear), face-core bond and thermal stress are omitted, as in 002/003; equal face mass holds the pinned core and separation fixed. | [rpt-ref-45da79edf548b064b228](6284193a78be0578-NFI.json) |
| N400 | NFI-023-CHECK-SOURCE-AND-TAGS | 030b addition | {"id": "NFI-023-CHECK-SOURCE-AND-TAGS", "status": "open", "non_blocking": true, "field": "material allowable transfer and result labels", "reported": "Nominal coupon strengths and inherited density are used as joint design values; overallRESULTS tagQUESTIONABLE.", "check": "1470MPa cited Toray coupon is verified, as are Henkel/TIMET/Invar values. The fabricated transition, its layup, complete node and film remain PROJECTION. Producer data vary by resin/version and typical/minimum basis.", "evidence": ["INPUTS.json source_audit", "primary PDFs"], "next": "Keep source version, test basis, material density and joint state explicit in each downstream row; do not promote the sizing to a qualified joint."} | [rpt-ref-f4daf73c940b6f527d37](6e377349147b3b13-NFI.json) |
| N552 | NFI-036-installed-hull | 030b addition | Establish installed capacity including unmodeled local failures. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N588 | NFI-034-STRUCTURAL-CARRY | 030b addition | This is a vacuum-maintenance estimate at fixed inherited points. The 022c Kapton equilateral row has filed least SF below one; Zylon structural assumptions and P2 optimism remain unqualified. | [rpt-ref-244f32e2449e729d312f](e2c32a737d582c44-NFI.json) |
| N618 | NFI-026B-04 | 030b addition | New nonlinear first instability not verified; Freshly authorized smallest-algebraic or inertia checks must find and refine earliest tangent loss. Do not use raw critical_lambda_estimate as a first-instability allowable. | [rpt-ref-8befdd4c89803adc44a8](d90bde67ada2ca77-NFI.json) |
| N644 | NFI-026B-04 | 030b addition | New nonlinear first instability not verified; Freshly authorized smallest-algebraic or inertia checks must find and refine earliest tangent loss. Do not use raw critical_lambda_estimate as a first-instability allowable. | [rpt-ref-4a20323946ecafd56a6b](d90bde67ada2ca77-NFI.json) |
| N670 | NFI-038-RELIABILITY | 030b addition | Screening count is not a design allowable or mission qualification | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N703 | NFI-036-installed-hull | 030b addition | Establish installed capacity including unmodeled local failures. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |

<a id="R082"></a>
### R082 — optimiser resolution and scope (grid vs continuous, splits, knees)

**Original030 unknown:** General instability now includes transverse shear; the 007 thickness splits were not re-searched, which matters only for a named core whose Kc moves the equal-factor point.

**Original030 today:** least SF 0.65041 (continuous balance 0.65041) [CHECK-MAINLINE-09C5]; least SF 0.17502 (boundary limit 0.17503) [CHECK-MAINLINE-09C5]; grid j/8000 [CHECK-MAINLINE-14B]; grid 0.66865; continuous 0.66871 [CHECK-019]

**Original030 needed:** Label as finite search result; refinement optional [CHECK-MAINLINE-09C5]; Label as grid resolution [CHECK-MAINLINE-09C5]; Label as grid optima; keep reported precision as computational precision [CHECK-MAINLINE-14B]; The unstated core-fraction grid [CHECK-019]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N005 | NFI-OPTIMUM-RESOLUTION | 030 retained | {"id": "NFI-OPTIMUM-RESOLUTION", "type": "estimate_resolution", "row": "optimum", "field": "least_SF", "reported": 0.6504118436805308, "independent_continuous_balance": 0.6504130224098148, "independent_fraction": 0.19176846298505057, "proposed_fix": "Label the filed point as a finite search result; optional refinement only.", "stops_owner": false} | [rpt-1228-mainline009c5-independent-check-1019](4662757b4d50b2d1-NFI.json) |
| N006 | NFI-OTHER-BRANCH-RESOLUTION | 030 retained | {"id": "NFI-OTHER-BRANCH-RESOLUTION", "type": "estimate_resolution", "row": "other_branch", "field": "least_SF", "reported": 0.175022781624177, "independent_boundary_limit": 0.17502890484090416, "proposed_fix": "Label grid resolution; the small refinement changes no decision.", "stops_owner": false} | [rpt-1228-mainline009c5-independent-check-1019](4662757b4d50b2d1-NFI.json) |
| N017 | NFI-GRID-RESOLUTION | 030 retained | {"id": "NFI-GRID-RESOLUTION", "type": "estimate_resolution", "row": "all optima", "field": "optimality", "reported": "best", "independent": "Reproduced on j/8000 finite grid, not a continuous optimality proof.", "proposed_fix": "Label grid optima and retain the reported precision as computational precision.", "stops_owner": false} | [rpt-1228-mainline014b-independent-check-1019](5d2a8afe8b483d72-NFI.json) |
| N027 | NFI-CHK019-014B-GRID | 030 retained | 014b's grid value 0.668649769508548 needs 014b's unstated core-fraction grid. Seven regular grids land 5e-5 to 8e-4 away. The card's continuous 0.668710748 is reproduced. | [rpt-check019-opus-1020](9cc8bdcb82e9b2d1-NFI.json) |
| N037 | NFI-RULE | 030 retained | {"NFI_id": "NFI-RULE", "gap": "The splits are an optimum of knocked-down buckling and QUESTIONABLE yield on the ceiling. They are not an optimum once shear, wrinkling, or crush enter the stated factor.", "direction": "Recompute after MAINLINE-007b.", "effect": "Another limit would move both thicknesses."} | [rpt-ref-05310d05f1fb52d6522e](d0ddbdac23ccf0df-NFI.json) |
| N043 | NFI-SAND | 030 retained | {"NFI_id": "NFI-SAND", "gap": "General instability now includes transverse shear and matches the kd 0.2 pressure when shear stiffness is infinite. The 007 splits were not searched again.", "direction": "A new split search would matter only for a named core whose Kc moves the equal-factor point.", "effect": "On the reported rows, buckling still governs after the trim except where honeycomb wrinkling is admitted."} | [rpt-ref-3dd5ab5528276031581d](07d0f8e52a240650-NFI.json) |
| N254 | NFI-FLOAT-ALLOCATION-CARRY | 030 retained | {"NFI_id": "NFI-FLOAT-ALLOCATION-CARRY", "gap": "Each alternative spends the baseline margin on one thickness. Residual margin is numerical zero by that rule. It is not an optimum and not a search over families.", "direction": "A later card can compare other single changes, including core thickness and tube radius.", "effect": "The allocation changes both stiffness and strength pressures through the named thickness."} | [rpt-mainline002-grok-strength-card-1019](b155c07e690eaa66-NFI.json) |
| N270 | NFI-RULE | 030 retained | {"NFI_id": "NFI-RULE", "gap": "Equal mass, core-only and proportional scale are stated rules. They are not an optimum and not the advisory search.", "direction": "Do not read the equal-mass point as a proved best split.", "effect": "Another rule would move both safety factors."} | [rpt-mainline003-grok-p2-targets-1019](2090c6e1f4ca8afb-NFI.json) |
| N286 | NFI-KNEE | 030 retained | {"NFI_id": "NFI-KNEE", "gap": "Confirmed: knee is the largest finite-difference drop per 100 kg on the tabulated margins, sorted by payload, not a fitted optimum.", "direction": "A denser margin grid if a smoother knee is needed.", "effect": "Owner statement stands."} | [rpt-mainline006-check-lead4f19-1019](8060138631058409-NFI.json) |
| N290 | NFI-KNEE | 030 retained | {"NFI_id": "NFI-KNEE", "gap": "The knee is the tabulated interval with the largest drop in least SF per 100 kg of payload. It is a finite difference on these margins, not a fitted optimum.", "direction": "A denser margin grid if a later card needs a smoother knee.", "effect": "The named knee can move if margins are added between 0 and 5 percent."} | [rpt-mainline006-grok-float-margin-1019](c433e7ad1bc469c3-NFI.json) |
| N301 | NFI-SAND | 030 retained | {"NFI_id": "NFI-SAND", "gap": "Confirmed: general instability includes transverse shear and restores the kd 0.2 classical pressure at infinite shear (Kc=1). The 007 splits were not re-searched.", "direction": "A new split search only for a named core whose Kc moves the equal-factor point.", "effect": "Owner statement stands."} | [rpt-mainline007b-check-lead4f19-1019](ef98a0f4f10c64ba-NFI.json) |
| N354 | NFI-017-COMBO | 030 retained | {"NFI_id": "NFI-017-COMBO", "gap": "The cheapest combination is a product-minimising differential-evolution search on a 900-point depth grid, seeded, not a proof of global optimality. In all three P2 points it returns face density alone, at products 1.474, 1.657 and 1.685 on the grid against continuous single factors 1.459, 1.637 and 1.655.", "direction": "An analytic product bound if a later card needs to beat these products.", "effect": "Split statements read as 'cheapest found'."} | [rpt-mainline017-improvement-directions-lead4f19-1019](9f3c760a855408f0-NFI.json) |
| N461 | NFI-C022-SEARCH-RESOLUTION | 030b addition | The reported optima are maxima of a grid with 12 film gauges, not established continuous maxima. | [rpt-ref-f6de390e1555b4ca8e78](c6fe867af95c0749-NFI.json) |
| N561 | 033-NFI-09 | 030b addition | Catalogue and numerical scope; The 47-row honeycomb catalogue includes projected density-scaled rows. Winners are identified, and source tags remain intact. Radius crossings and noncrossing peaks are numerical searches, not interval proofs. Missing open-mode allowables and load cases are not silently assigned SF>=1. | [rpt-ref-5b1ba7a48fcb57c8e35e](a4edee0295bc38f3-NFI.json) |
| N599 | NFI-022D-SEARCH | 030b addition | The 12-film-gauge discretization is removed. Continuous DE, constrained refinements, independent residual checks and 16 expanded-domain cases agree, but no mathematical global certificate is claimed. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |
| N609 | NFI-017b-P3-SEARCH | 030b addition | P3 uses 022c's equilateral rows only; the two-way grid is not scored. The finer film grid and polish lift 022c's rows by 1.1 and 1.7 percent (0.7017 to 0.7097; 1.4170 to 1.4412).; 022's owner's view on the two-way grid's stability with the film. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| N623 | NFI-026B-09 | 030b addition | Finite grid, eigenvalue multiplicity and model scope; Coarse-grid discrepancy is established for these cases; do not infer a universal cutoff or uniquely attribute the difference to one mechanism. | [rpt-ref-8befdd4c89803adc44a8](d90bde67ada2ca77-NFI.json) |
| N634 | NFI-032-CHECK-ROUNDED-TARGET | 030b addition | non_blocking | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N649 | NFI-026B-09 | 030b addition | Finite grid, eigenvalue multiplicity and model scope; Coarse-grid discrepancy is established for these cases; do not infer a universal cutoff or uniquely attribute the difference to one mechanism. | [rpt-ref-4a20323946ecafd56a6b](d90bde67ada2ca77-NFI.json) |

<a id="R083"></a>
### R083 — optimism factor comparison 021 vs frame

**Original030 unknown:** MAINLINE-021 P2 reaches SF 1 with gamma 2.90x0.20 and wrinkling 1.10x0.33; this frame least equilateral SF 1.354 needs a largest named factor of 8 (arc rise); both questionable.

**Original030 today:** P2 largest factor 2.90; frame largest 8; frame least SF 1.35387562843 [MAINLINE-022]

**Current030b:** 017b P2 direction study uses nu=.08, variable scarf ratio and piecewise gamma, so its gamma-only and modulus-at-Vc 2 results do not overturn033's flat-gamma singleton result. Its P3 leads/trend closure predate022d and are superseded for current design; all findings retained.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N361 | NFI-022-021 | 030 retained | MAINLINE-021 has filed (rpt-ref-fe49179fb6a8ad8c986e). Its P2 sandwich reaches SF 1 on gamma 2.90 times 0.20 and a wrinkling coefficient 1.10 times 0.33, at a face allowable of 283 MPa. Least mode 1.000. Full named set 1.111. This frame's least equilateral set is arc_rise_above_sphere, least SF 1.35387562843. The P2 sandwich needs less optimism. Its largest named factor is 2.90, and this frame's largest is 8 (arc rise over the spherical sagitta, factor 8). Both are QUESTIONABLE. | [rpt-mainline022-grok-p3-optimistic-floating-point-1020](307ab133da904ca4-NFI.json) |
| N614 | NFI-017b-COMBINATION-METRIC | 030b addition | The product of factors depends on how a property is parametrised (Q against Ec = Q^2; K_delta against physical waviness). Each lever's definition is stated so a reader can re-weight.; None; a reading note. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| B001 | NFI-030B-BASIS | 030b addition | P2 comparisons use distinct pressure, Poisson and joint-account conventions.; 028b uses p0, nu=.0752 and max(J,.05S); 033 uses 1.01p0, nu=.0768 and actual J as its main case. 036's 027 R20 point retains a separate eta=.9 splice law. Keep these bases attached; a changed threshold is not an arithmetic contradiction. | [rpt-ref-39745602983887568501](02744dbf85113cc4-legacy--02744dbf85113cc4de64187c76ed79779e558031dadf21e6ad2f8aea21188dc1--AUTHORED-NFI.json) |
| B007 | NFI-030B-017B-SUPERSESSION | 030b addition | 017b's P3 improvement factors and trend projection use superseded 022c physics.; Retain its directional study as historical evidence, but use 022d for current P3 values and the ordered 026b global sensitivity. Its 1.441 Zylon optimum and projected 14–25 year closure are not current lead predictions. P2's variable scarf, nu=.08 and piecewise gamma also differ from 028b/033. | [rpt-ref-39745602983887568501](02744dbf85113cc4-legacy--02744dbf85113cc4de64187c76ed79779e558031dadf21e6ad2f8aea21188dc1--AUTHORED-NFI.json) |

<a id="R084"></a>
### R084 — regressions recover filed points

**Original030 unknown:** With dimpling off, Be S-200F on HRH-10-4.8-32 at kd 0.20 recovers the filed 014 least SF, thicknesses and modes.

**Original030 today:** kd 0.20 [MAINLINE-14B]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N316 | NFI-011B-REGRESSION | 030 retained | With joints off and only yield, Euler, local and film, the 6061 banded optimum recovers the filed 011 point. The 011 tree was not rewritten. | [rpt-mainline011b-grok-p3-global-arcs-1019](da2eeba2a608cb9e-NFI.json) |
| N346 | NFI-014-REGRESSION | 030 retained | With dimpling turned off, Be S-200F on HRH-10-4.8-32 at kd 0.20 recovers the filed 014 least SF, thicknesses and modes. The 014 tree was not rewritten. | [rpt-mainline014b-grok-metal-honeycomb-1019](e56941cee236de62-NFI.json) |

<a id="R085"></a>
### R085 — thin-wall section approximation P3

**Original030 unknown:** Answered here: exact annuli used, and tw/ro at optima is thin; only the fixed ro = 0.02 comparison rows are thick.

**Original030 today:** tw/ro = 0.175 on P3-A [MAINLINE-005]; tw/ro 0.019-0.076 at optima; 0.175 to 0.38 at comparison rows [MAINLINE-011]

**Original030 needed:** exact annulus A and I for a named candidate section [MAINLINE-005]; none unless a family nears P3 feasibility [MAINLINE-08B]; none for optima [MAINLINE-011]

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N125 | NFI-005-THINWALL | 030 retained | {"NFI_id": "NFI-005-THINWALL", "gap": "P3 figures use thin-wall A and I at fixed outer radius. P3-A has tw/ro = 0.175, where thin-wall understates I for a given mass.", "direction": "Use exact annulus A and I for a named candidate section.", "effect": "P3-A's E/rho requirement is mildly pessimistic; exact section helps it."} | [rpt-ref-eb07faa637b7487d6dc5](c108cdbb9f3bcf68-NFI.json) |
| N142 | NFI-008B-THINWALL | 030 retained | The P3 columns use the thin-wall tube figures; the approximation is weakest on P3-A where tw/ro = 0.175. | [rpt-ref-cc9cef5e55adca018a8f](cbad32790fc5fde1-NFI.json) |
| N154 | NFI-011-TW-EXACT | 030 retained | {"NFI_id": "NFI-011-TW-EXACT", "gap": "NFI-005-THINWALL answered: all sections here are exact annuli, and at every reported optimum t_w/r_o lies in 0.019-0.076 (thin). Only the 005-frame comparison rows at fixed r_o=0.02 sit thick (t_w/r_o 0.175 aluminum, up to 0.38 for swaps), where the thin-cylinder local formula itself is weakest.", "direction": "None for this card's optima; the 005-frame rows are comparison only.", "effect": "None on the reported optima."} | [rpt-ref-f21d4bd21d2026511818](0f1373271ca0676e-NFI.json) |

## T25 — Other

<a id="R086"></a>
### R086 — mooring hardpoint load design

**Original030 unknown:** Mooring hardpoint patch stress exceeds the questionable core allowable and snatch loads need dynamic analysis.

**Original030 today:** design load 48.3 kN; bare patch 683 kPa vs 500 kPa allowable, SF 0.73 [MAINLINE-016]

**Original030 needed:** Spreaders of at least 0.145 m2 per hardpoint; mooring dynamics with added mass [MAINLINE-016]

**Current030b:** 037's R10 full-point 70-knot uniform excess falls to .998442; flight-gust screen is 1.003303. Its nominal single hardpoint pads weigh 8.65 or 33.14 kg at different wind cases and must be charged. Neither these values nor the thermal values are validated on the larger 033 hulls.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N063 | NFI-016-MOOR | 030 retained | {"NFI_id": "NFI-016-MOOR", "rank": 7, "gap": "Mooring design load 48.3 kN at 20 m/s with a 1.4 gust factor; a bare 0.0707 m2 hardpoint patch sees 683 kPa against a 500.0 kPa QUESTIONABLE core allowable, SF 0.73. Added air mass 2445 kg equals hull mass, so snatch loads need a dynamic mooring analysis.", "direction": "Design spreaders of at least 0.145 m2 per hardpoint for core SF 1.5; run the mooring dynamics with the added mass; qualify six hardpoints, about 48 kg.", "effect": "Local design plus about 20 percent of the margin in fittings; not a hull-mode problem."} | [ref-0c9ab80606a173c6adb6](e000d61baed6b1db-NFI.json) |
| N565 | NFI-037-MOORING-WIND | 030b addition | FAA-P-8110-2 Table 4 lists 70 knots. Mapped as a uniform windward excess, the floated P2 lead falls from 1.006358 to 0.998442. The flight gust, 35 ft/s at 35 knots, leaves 1.003303. The change discussion names 78 knots. | [rpt-ref-8c5de04c9c33dbcf7447](f9ff7da1d21d1380-NFI.json) |
| N567 | NFI-037-PATCH-BUCKLING | 030b addition | No sourced sphere-buckling factor under a windward patch was applied. Potential-flow area-mean Cp is -0.5, so a uniform excess overstates the mean pressure. | [rpt-ref-8c5de04c9c33dbcf7447](f9ff7da1d21d1380-NFI.json) |

## T06 — Face sheet and panels

### R087 — Finished minimum gauge, forming and strength retention

**Current030b:** 036 distinguishes already etched finished stock from extra finishing. Require a minimum finished gauge and post-process compression basis; do not deduct etch twice.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N436 | NFI-028b-gauge | 030b addition | Map actual minimum thickness after forming and scarf preparation; nominal gauges sit at tight mode boundaries. | [rpt-ref-d907de1e97319ecc3f9a](737765424727a77d-NFI.json) |
| N543 | NFI-036-minimum-gauge | 030b addition | Specify minimum finished gauge rather than an unqualified nominal gauge. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N544 | NFI-036-forming-finish | 030b addition | Determine strength after the actual forming and finishing history. | [rpt-ref-5f14d083ceae03234596](15aa21e2896e5dbe-NFI.json) |
| N653 | NFI-038-GAUGE | 030b addition | Nominal thickness is not finished minimum | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N694 | NFI-036-minimum-gauge | 030b addition | Specify minimum finished gauge rather than an unqualified nominal gauge. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |
| N695 | NFI-036-forming-finish | 030b addition | Determine strength after the actual forming and finishing history. | [rpt-ref-f182f16ed5be422b7811](4b0e541f707f3658-NFI.json) |

## T04 — Wrinkling and core Ec

### R088 — Waviness at the critical wavelength; metric and process transfer

**Current030b:** Combined CHECK-032/032b passes 533 comparisons, corrects Woody3micrometres to template-adjustment RMS, recovers .008in face identity, and adds Rion carbon/Nomex measured depth near its own critical wavelength. Conditional full periods 37–40mm approach/breach Woody's >40mm measurement band. None establishes actual Be/CR-III modal amplitude; retain all original Fc and metrology qualifications.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N449 | wavelength-versus-cell | 030b addition | Section 2.2.2 does not print the critical half-wavelength. FPL 1810-A says cell size changes that wavelength. Delta over the 9.525 mm cell is an amplitude ratio, not a separation of modes. | [rpt-mainline032-grok-wrinkle-waviness-1020](df2ac0989ca4f688-NFI.json) |
| N450 | shop-flatness-is-not-delta | 030b addition | AMS7902H defines three flatness classes. The class numbers were not read. Bonded-panel numbers found here are long-wave bows or an architectural wave. Hexcel's design note that a large cell telegraphs into a thin face gives no depth. None of those is the Fourier component in equation 2.2-13. | [rpt-mainline032-grok-wrinkle-waviness-1020](df2ac0989ca4f688-NFI.json) |
| N473 | NFI-015-CHECK-MANUFACTURING-PROVENANCE | 030b addition | non_blocking | [rpt-ref-a5374575ee8867fc8d2e](5a38cd8c393ec4c9-NFI.json) |
| N512 | no-beryllium-face-at-wrinkle-wavelength | 030b addition | No page read here gives a zero-to-peak amplitude of an as-bonded beryllium face on CR-III 3/8-1.0 at the CR-1457 wrinkle wavelength. That wavelength was not computed on 032 and is not computed here. | [rpt-mainline032b-grok-measured-flatness-1020](a754f4c4c109c350-NFI.json) |
| N513 | optical-bench-and-space-mirror-unread | 030b addition | A space-mirror or optical-bench sandwich with a measured cell-print depth was not opened. The space sandwich that was opened is the aluminum solar-concentrator coupon, not an optical bench. Publisher gates blocked a 2025 panel-unit abstract on this pass. | [rpt-mainline032b-grok-measured-flatness-1020](a754f4c4c109c350-NFI.json) |
| N514 | hexcel-telegraph-depth-still-unprinted | 030b addition | A text extract of the local HexWeb attributes brochure contains no telegraphing depth. This pass does not add a depth Hexcel did not print. | [rpt-mainline032b-grok-measured-flatness-1020](a754f4c4c109c350-NFI.json) |
| N515 | three-eighths-slope-is-not-a-depth | 030b addition | ER-1001 prints 0.5 to 1.6 milliradian on 3/8-inch cells and does not print the matching depth. The sine and the slope-times-cell sketches are labelled projections. | [rpt-mainline032b-grok-measured-flatness-1020](a754f4c4c109c350-NFI.json) |
| N516 | transfer-to-the-lead-faces | 030b addition | Leighton faces are 1 mm aluminum on a machined core. The ER-1001 faces are aluminum foil, 0.003 to 0.016 inch in the series, thinner than the lead sheets, and the core on the depth trace is 3/16 inch. Neither is S-200F or SR-200 on CR-III 3/8-1.0. Flatwise tension and the beryllium bond remain unprinted, so the 60 psi amplitudes stay an upper bound only if that F_c is real. | [rpt-mainline032b-grok-measured-flatness-1020](a754f4c4c109c350-NFI.json) |
| N517 | panel-rms-is-not-delta | 030b addition | Treating the 0.20 mm honeycomb rms, or a per-foot shop bow, as the wrinkle component exceeds the needed amplitudes only by using the wrong spatial piece. | [rpt-mainline032b-grok-measured-flatness-1020](a754f4c4c109c350-NFI.json) |
| N532 | NFI-032-CHECK-WAVELENGTH | 030b addition | non_blocking | [rpt-ref-a30a669ed3e245f1473b](f4fb2c3464ed42c3-NFI.json) |
| N533 | NFI-032-CHECK-SHOP-METRIC | 030b addition | non_blocking | [rpt-ref-a30a669ed3e245f1473b](f4fb2c3464ed42c3-NFI.json) |
| N604 | NFI-017b-FLATNESS-TRANSLATION | 030b addition | Q is translated to waviness with CR-1457 eq 2.2-12/13 using Fc = 60 psi (typical stabilised compression, taken as the lowest flatwise strength). The lever holds K_delta; physical waviness depends on Ec and Fc (0.347 mm today's equivalent at R 10; 0.099 mm in the Be-kept material combination).; Measured flatwise tension and bond strength for the Be/CR-III bond, and measured face waviness. | [rpt-ref-6ba73ec8a89453b26832](e10b0bbc09d310a0-NFI.json) |
| N629 | NFI-032-CHECK-WAVELENGTH | 030b addition | non_blocking | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N630 | NFI-032-CHECK-SHOP-METRIC | 030b addition | non_blocking | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N633 | NFI-032-CHECK-LEAD-RANGE | 030b addition | non_blocking | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N635 | NFI-032B-CHECK-CSO-TEMPLATE | 030b addition | CARD attributes 3 um to the completed CSO surface against its template.; Relabel the 3 um result and its ratios. Numeric conversion passes; surface attribution does not. | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N636 | NFI-032B-CHECK-COUPON-IDENTITY | 030b addition | The source text pages do not name the face thicknesses.; The report's figures fill the identity gap. They do not establish Be or CR-III equivalence. | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N637 | NFI-032B-CHECK-METRIC | 030b addition | Numerical depth/RMS/slope-to-delta comparisons can be mistaken for modal comparisons.; Keep number-only labels and metrology bandwidth. Single-sine examples are projections, not fitted measurements. | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N638 | NFI-032B-CHECK-MISSED-RION | 030b addition | 032b did not retrieve the Rion thin-face waviness experiment.; Evidence exists for a different system; no measured Be/CR-III modal amplitude follows. Preserve the empirical shape conversion. | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N639 | NFI-032B-CHECK-WAVELENGTH | 030b addition | The target wrinkle wavelength was not computed in 032/032b.; A conditional band is now specified. Curvature, biaxiality, material tangent properties, other modes and actual measured spectrum remain unresolved. | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |
| N640 | NFI-032B-CHECK-HISTORICAL-EVIDENCE | 030b addition | The 'exceeded today' field includes a 1969 honeycomb vendor RMS.; Label it historical whole-surface capability evidence; do not infer a current production distribution or wrinkle-band exceedance. | [rpt-ref-7427b639691bfaf71f29](fcb27bf7e1383d15-NFI.json) |

## T11 — Thermal

### R089 — Sun, bond reference temperature and additional pressure/load interaction

**Current030b:** 037 coated reference thermal shear screen is 1.678; a cold-night stress-free bond reference gives .917, and bare Be gives .388. Coating, bond temperature, wind and local load requirements remain choices; no combined whole-vehicle closure is claimed.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N495 | NFI-031-ENVIRONMENT-LOADS | 030b addition | Mode scores use uniform centre pressure, no internal-pressure relief and fixed material properties. Local bottom pressure is about a further 0.1% higher, while gradients, thermal mismatch, wind, attached loads and descent transients are unscored. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N563 | NFI-037-BARE-BE | 030b addition | Bare beryllium, absorptance 0.40 and emittance 0.05, reaches 356.9 K. The day rise from the air temperature produces 621 kPa of face-core shear and factor 0.388 on the 241 kPa sheet. The optical pair is an engineering band, not a measured SR-200 coupon. | [rpt-ref-8c5de04c9c33dbcf7447](f9ff7da1d21d1380-NFI.json) |
| N564 | NFI-037-ASSEMBLY-TEMPERATURE | 030b addition | Coated shear-lag is 1.678 on the day rise from the air temperature and 0.917 on the 30.493 K day-night swing. Which one applies is the temperature at which the bond is stress-free. | [rpt-ref-8c5de04c9c33dbcf7447](f9ff7da1d21d1380-NFI.json) |
| N566 | NFI-037-PATTERN-BOUND | 030b addition | A through-thickness-uniform solar pattern has no membrane stress on a complete sphere. Bending is 0.818 MPa coated. The constrained upper bounds are 20.51 MPa coated and 60.75 MPa bare. The table uses the bending value. | [rpt-ref-8c5de04c9c33dbcf7447](f9ff7da1d21d1380-NFI.json) |
| B003 | NFI-030B-LOAD-AND-MASS-TRANSFER | 030b addition | Weather, extra loads and vacuum bills have not been jointly optimized on every current lead.; 031 reoptimizes older seam/film geometry; 037 evaluates 028b's full endpoint and pre-022d P3; 034 estimates service at older geometries. Carry their requirements and evidence, but do not add their margins or copy their bills as validated values for 033/022d. Coating, pads, barriers and fittings require a complete reclosure. | [rpt-ref-39745602983887568501](02744dbf85113cc4-legacy--02744dbf85113cc4de64187c76ed79779e558031dadf21e6ad2f8aea21188dc1--AUTHORED-NFI.json) |

## T01 — Case and atmosphere

### R090 — Terrain, weather, altitude floor/ceiling and passive equilibrium requirement

**Current030b:** 031's illustrative 100m centre floor needs 55.341 kg optimistic climate headroom or 441.770 kg for both weather sets on its own geometry; ISA equilibria are 617.075/1464.507 m. The Admiral must choose terrain-relative clearance, ceiling and weather envelope.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N482 | NFI-031-REQUIREMENT | 030b addition | No site elevation, terrain, minimum hull clearance, altitude ceiling or required 500m condition has been authorised. Centre 10m is ground tangency at sea level; 100m is only an illustrative 90m clearance. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N483 | NFI-031-PROFILE | 030b addition | 019 specifies conditions at one altitude, not a vertical profile. A 6.5K/km lapse and constant e/p were imposed. At the 100m floor, isothermal optimistic climate mass is 11.73kg versus 55.34kg with the chosen lapse; both-weather values are 403.66 versus 441.77kg. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N484 | NFI-031-SATURATION | 030b addition | The conservative high-pressure humid day becomes supersaturated in the all-weather 500m-floor diagnostic. The 0/10/100m-floor main cases are unsaturated in the stated model. Continuing an unsaturated lapse through cloud is not a physical forecast. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |
| N485 | NFI-031-CONTROL | 030b addition | A fixed evacuated hull has one passive equilibrium per weather profile and carried load. Positive C raises its ISA float altitude; C=0 cannot float at 500m ISA and satisfy the illustrative sea-level-ground clearance on both 019 hot-day extremes. Static equilibrium does not provide station keeping. | [rpt-ref-9a0319231d2fe686eb92](d18857e0b502c9fe-NFI.json) |

## T14 — P3 local buckling

### R091 — Tensile bending and coupled shell/column/curvature limits

**Current030b:** CHECK-022b/022c identifies omitted tensile bending and local/column interaction. 022d includes a projected Ft15.586 MPa ceiling; the screened lead has zero tension at its target, while coupled instability remains open.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N382 | NFI-025-MODEL | 030b addition | Arc, shell, column and global instability are represented by separate surrogate minima.; Perry equation here is an elastic extreme-fiber stress criterion for an assumed bow; it is not a ceramic code allowable. No post-Euler finite stress is claimed. SourceE410 GPa is retained for reproduction, not treated as a qualified same-lot manufacturer property. | [rpt-ref-58c781cbea9c220eb5b4](30fd9d8f3fc5e5ed-NFI.json) |
| N458 | NFI-C022-TENSILE-BENDING | 030b addition | Long-span projected rows develop substantial tensile stress at their claimed least multipliers; Perry limits compression only. | [rpt-ref-f6de390e1555b4ca8e78](c6fe867af95c0749-NFI.json) |
| N459 | NFI-C022-LOCAL-INTERACTION | 030b addition | The separate minimum of shell, column and compression-only Perry factors does not establish their interaction. | [rpt-ref-f6de390e1555b4ca8e78](c6fe867af95c0749-NFI.json) |
| N591 | NFI-022D-TENSION | 030b addition | Amplified tensile bending is screened at assumed Ft=15.586 MPa. This fixed reference-volume ceiling is PROJECTION, not a full-stress-field weakest-link model or measured allowable. Eight overall equilateral witnesses bind it; no screened optimum has tensile stress at its target. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |
| N596 | NFI-022D-INTERACTION | 030b addition | Separate local, Euler and Perry/tension minima leave shell-column-curvature interaction unresolved. The optional magnified-local diagnostic is not a validated law and is excluded from the primary least SF. | [rpt-ref-6c81b0b188ad134a3ea2](23377b822a4303a6-NFI.json) |
| N621 | NFI-026B-07 | 030b addition | Beam-only instability omits earlier failure modes; Elastic frame factors are not physical structural allowables. | [rpt-ref-8befdd4c89803adc44a8](d90bde67ada2ca77-NFI.json) |
| N647 | NFI-026B-07 | 030b addition | Beam-only instability omits earlier failure modes; Elastic frame factors are not physical structural allowables. | [rpt-ref-4a20323946ecafd56a6b](d90bde67ada2ca77-NFI.json) |

## T18 — P3 nodes and joints

### R092 — Discrete curved-member rolling mechanisms and restraint

**Current030b:** 026b reports1080/480/120 member-roll mechanisms at frequencies6/4/2. Its new nonlinear tangent zeros 5.082444/2.218113 are not verified first-instability loads; the top-level fields remain null. Eightfold rise does not divide thrust by eight and introduces4.248GPa elastic bending.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N501 | NFI-026-03 | 030b addition | Freely rolling pinned curved members are mechanisms; Specify joint anti-roll stiffness and attached-film restraint before assigning a positive pinned buckling factor. | [rpt-ref-7ce5b278fa083d87105b](78c3ad662469116d-NFI.json) |
| N616 | NFI-026B-02 | 030b addition | Freely pinned curved members roll; Specify joint and film anti-roll restraint before assigning positive pinned reserve. | [rpt-ref-8befdd4c89803adc44a8](d90bde67ada2ca77-NFI.json) |
| N642 | NFI-026B-02 | 030b addition | Freely pinned curved members roll; Specify joint and film anti-roll restraint before assigning positive pinned reserve. | [rpt-ref-4a20323946ecafd56a6b](d90bde67ada2ca77-NFI.json) |

## T26 — Grounding plan

### R093 — Ordered evidence route and grounding of the current leads

**Current030b:** 038 supplies nine physical test families. Its first purchase sequence is finished-sheet compression, weighed sealed scarf panel, then same-batch wrinkle coupons; retain original 030 FE-first list as historical planning. Planning costs and providers are unverified projections; no contact or purchase was performed.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N658 | NFI-038-MIN_SHELL | 030b addition | Smallest manufactured similarity shell not established | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N661 | NFI-038-VACUUM_LOAD | 030b addition | Ambient evacuation gives little Be overload and censored survivals | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |
| N669 | NFI-038-COST_AVAILABILITY | 030b addition | All prices and custom fabrication feasibility are projections | [rpt-ref-536c47263ffe5f46fd19](e3f1573de8237f38-NFI.json) |

## T24 — Method and provenance

### R094 — Snapshot completeness and pending follow-on filings

**Current030b:** This is a measured-time snapshot. Any named running card/check lacking a filed report at final intake is PENDING for 030c, not silently complete.

| UID | Source row | Version | Finding / disposition (full raw fields in NFI.json) | Source |
|---|---|---|---|---|
| N366 | NFI-030-SNAPSHOT | 030b addition | Snapshot at 01:15 PDT. Pending cards 022c, 025, 026, 028b, 015b, 029 and checks of 021b, 022b, 023, 024, 027, 028; 030b refiles on them. | [rpt-mainline030-opus-register-1020](858f8f97e8cb24d5-NFI.json) |
| N622 | NFI-026B-08 | 030b addition | One optional static refinement refused by simjob; No retry/fallback/subsequent scientific launch. Paired m12 force/rise comparison complete; m24 rise-8 refinement complete. New numerical work requires fresh authority. | [rpt-ref-8befdd4c89803adc44a8](d90bde67ada2ca77-NFI.json) |
| N648 | NFI-026B-08 | 030b addition | One optional static refinement refused by simjob; No retry/fallback/subsequent scientific launch. Paired m12 force/rise comparison complete; m24 rise-8 refinement complete. New numerical work requires fresh authority. | [rpt-ref-4a20323946ecafd56a6b](d90bde67ada2ca77-NFI.json) |
| B004 | NFI-030B-SNAPSHOT | 030b addition | Unfiled cards and checks remain pending for 030c.; Coverage is through the recorded final queue intake. No result or check is inferred from a running seat, a brief, an elapsed time or an unfiled artifact. | [rpt-ref-39745602983887568501](02744dbf85113cc4-legacy--02744dbf85113cc4de64187c76ed79779e558031dadf21e6ad2f8aea21188dc1--AUTHORED-NFI.json) |
