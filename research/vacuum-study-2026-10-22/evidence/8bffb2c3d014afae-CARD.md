# Morning card — claim record version 9

Unit vacuum-record-delta-e-1022. QUESTIONABLE / PROJECTION. No qualified hull safety factor. No finite-element run and no simjob: this step appends the record and does not recompute.

Base is admitted version 8, sha256 dede05e82b02973f6d4b2d79170dd9930563bc0500ce63717897c62da70040c7. Version 9 sha256 3ece1a1eab4a6fc21f2132b526a714ff64c237a330b16103ab16c2d1b04f2a07, 21892803 bytes, 2416 findings, 123 register rows, 2299 NFI rows. Written 2026-10-22T10:12:21-07:00. The live file on ref-08887151c61d86c0cd02 was not the base and was not written. Its sha256 remains c2fdd2327f93a78cc989bcb6cdaa15e32a836122f49da335985496cb6bac308d.

One line for each change since version 8.

- **graphite-variant-thermal.** 069's filed graphite-film variant described 070's gamma-held-0.20 cases. None float. R 30 optimistic still needs density factor 1.659, to 1357 kg/m3. 071 carries the thermal result this variant was missing. Above Vc 2, CR-1457 governs by shear crimping and sets the knockdown to 1, so 070's gamma = 1 branch matches the handbook, with the named limit that the rule is not this film on CR-III and not a closed 20 to 30 m sphere. DOI 10.2514/3.5568 and DOI 10.2514/3.1932 do not govern that step. On the aluminum core every gamma-step case is thermally infeasible. At 070's geometry the thermal margin is 0.536. Face density cannot release it. A core expansion at or below 12.2e-6 per K would release it at this stiffness. At that boundary, R 20 optimistic still needs a face-density factor of 3.467 at concept and 3.137 at TRL 7, to 649 and 717 kg/m3, and the core thickness is the search floor. On CR-III the graphite variant is infeasible. Its condition is a core with matched expansion. 072 tests real cores of that kind. The filed 069 page is unchanged. This delta reconciles it. Provenance: this append is DELTA-069-GRAPHITE-071, written 2026-10-20T19:07:56-07:00 on ord-admiral-rr2-mainline069-graphite-variant-amendment-1020, never filed or admitted until DELTA-E-1022. The dispatch card names that writing at 19:07:58.

- **071-limits.** Beside the graphite re-append, Sciences holds three limits. The expansion is an HOPG catalogue proxy, not the graphite film. The 12.2e-6 per K release is at fixed stiffness. The thermal law is the copied model law, distinct from the E1 cure-data note.

- **kc-sourced.** kc = 1 - Vc/4 is CR-1457 (4.2-4), used on domes in (6.2-1). It is SOURCED and leaves the optimism ledger. The 19 t that 069 reported from removing it, and the factor 1.459147 without it, are struck. PD066-NO-KC remains a historical sensitivity only.

- **fix-2.2-15.** Demonstrated fix, UNREVIEWED. Equation 2.2-15 puts 069's filed full-demand wrinkling margin at 0.793700544. The face stress must fall by 1.259921. Sciences holds this as a fixed-geometry correction, not by itself the reoptimized density target. Other modes on that geometry were unchanged.

- **mainline-073.** UNREVIEWED. Under 2.2-15, with BETA 1 and kc kept, face-density factors in order R20 ISA, R20 optimistic, R30 ISA, R30 optimistic are concept 1.968795546378443, 2.0628486187667696, 1.9320040871374877, 2.0234598518275413 beside 1.779, 1.863, 1.743, 1.825, and TRL 7 1.7158053450450115, 1.7946424557687226, 1.6891161125502747, 1.7661563938364964 beside 1.544, 1.614, 1.519, 1.587. Densities 939.661, 896.818, 957.555, 914.276 and 1078.211, 1030.846, 1095.247, 1047.472 kg/m3. The rise is 1.107 to 1.113, not 1.260, because the face thickened. R30 optimistic concept closes at 914.276 kg/m3, tf 3.668148 mm, tc 167.033 mm, payload +0.009001 kg, wrinkling and buckling co-bound. The 993 and 1146 kg/m3 targets become 896.818 and 1030.846. TRL 7 at 1850 kg/m3 needs gamma factor 3.2035729948565477, realized gamma 0.6407145989713096, beside filed 2.7669873295303313 and 0.5533974659060663. Gram-scale residuals are not physical reserves. simjob-20261022t095337-eb517fa6490c exited 0.

- **questionable-terms.** Cure, the gradient and bending stresses, and the pressure adder stay QUESTIONABLE. They are absent from CR-1457 and from DOI 10.2514/3.5568 and DOI 10.2514/3.1932. DELTA-D factors without them, uniaxial, are 1.7694119150252845, 1.8092731638452857 and 1.7397410734805205 at R30 optimistic concept. Sciences: those factors are not biaxial sensitivities and were not recomputed under 2.2-15.

- **mainline-068.** 068, literature arithmetic. The index is density over modulus to the power 0.514. Graphite film still needs concept multiplier 1.219 and TRL 7 multiplier 1.056. The review reproduced the film improvement as 1.5286 against filed 1.529. No beryllium sheet at 993 or 1146 kg/m3 was opened. T3 and T7 stayed on SR-200 bonded to CR-III. No purchase.

- **mainline-069.** 069 design point, bill arithmetic reproduced, physical float not independently closed. R30 optimistic concept: face 3.216 mm at 1013.825 kg/m3, core 178.708 mm, payload +5.031 kg, buckling and wrinkling at 1.000, thermal 1.071, gamma 0.20, Q 0.33, Vc filed 1.322817. The same hull is +1499 kg in ISA and +11607 / +13101 kg at TRL 7. The graphite paragraph on this page does not stand on CR-III. simjob-20261020t185846-4e60751d4d81 exited 0.

- **mainline-070.** 070: a graphite-film P2 floats in no case. At gamma 0.20 the face still needs factor 1.693 at concept and 1.478 at TRL 7, set by R20 optimistic, to 1329 and 1522 kg/m3, at 969 GPa. The review reproduced Vc on all 56 rows, the mass bills, and those factors. Vc is above 2, so the gamma 0.20 step is outside the named CR-1457 support.

- **mainline-071.** 071: on an aluminum core every gamma-step case is thermally infeasible. Thermal margin 0.535943 at 070's geometry. A core expansion at or below 12.2e-6 per K would release it at this stiffness. At that boundary R20 optimistic still needs factor 3.467 at concept and 3.137 at TRL 7, to 649 and 717 kg/m3, on the search floor. The review reproduced those figures. The limits are PE-071-LIMITS.

- **review-graphite.** Graphite review half is a pass. No demonstrated mismatch and no fix. Twenty-eight load-bearing numbers were re-derived and the owner code was not run. Unity knockdown at Vc at or above 2 is admissible with the named limit that it is not this film on CR-III and not a closed 20 to 30 m sphere. Five NFI rows are carried.

- **mainline-072b.** 072b, UNREVIEWED. No tested core gives a positive payload. That is the headline. HRH-49 has feasible geometry in all eight cases, so a blanket claim that no core is feasible is not admitted. Kevlar payloads are -27250 to -97399 kg, and the face-density factor to float is 2.67 to 3.04 at concept and 2.16 to 2.41 at TRL 7. Carbon UCF-355 has no feasible geometry in the eight cases. The model keeps equation 2.2-14. The RESULTS completion stamp is future-dated and is excluded.

- **programme-state.** Programme state, UNREVIEWED as a restatement. After 2.2-15 the floating design is a hypothetical face, concept R30 optimistic 914.276 kg/m3, factor 2.0234598518275413, with wrinkling and buckling co-bound and the QUESTIONABLE cure, gradient, bending and pressure adder still in the margin. The 993 and 1146 kg/m3 targets are now 896.818 and 1030.846. kc stands. The graphite route needs a matched core; 072b found no tested core with a positive payload, while HRH-49 is geometrically feasible and still heavy. T3 has to be equibiaxial, or a pressurized sphere or dome of this sandwich, before 2.2-15 is a measured allowable. T7 still has to measure this shell before any gamma above 0.20. Neither test is authorized work.

- **nfi-e-vc.** Independent Vc on the handbook (4.2-3) is 1.3208622451020047 against filed 1.322817147615744. The model power was not fitted to close that gap.

- **nfi-e-buckling.** Handbook global buckling with cure removed is 1.0272329728699576 against the filed margin 1.000. Cure stays in the model and is unsourced.

- **nfi-e-membrane.** Equation 2.2-14 on membrane stress at the filed pressure is 1.0491194341443413. The filed margin 1.000 includes gradient, bending and cure.

- **nfi-e-thermal.** The thermal interface margin near 1.071 cannot be checked. kb and the cure-temperature increment are not a closed law in the admitted record.

- **nfi-e-joints.** Scarf, splice, mooring and weather headroom were not re-derived. Their mass exceeds the +5.031 kg residual, so the physical float is not independently closed.

- **nfi-e-sig0.** The copied model uses sig0 = E*h/(R*sqrt(1-nu^2)). Handbook (4.2-3) uses the one-quarter power. The discrepancy is disclosed and uncorrected. Buckling in 073 still uses the model power.

- **nfi-e-073-limits.** 073 limits that remain open: the wrinkle wavelength was not compared with R; 2.2-14 and 2.2-15 are not a measured SR-200 on CR-III allowable; gamma for both weathers uses separate geometries, optimistic tf/tc 2.561/60.538 mm and ISA 2.508/59.855 mm, so the +3963.234 kg ISA payload is not a same-hull result; gram-scale residuals are not physical reserves; DELTA-D's term-removal factors were uniaxial.

- **nfi-g-sigma.** Graphite review NFI-1. The applied face stress 303.7436 MPa is constant across rows and is not carried by a pinned input.

- **nfi-g-blend.** Graphite review NFI-2. Global buckling sits within 0.4 percent, their side higher. CR-1457 gives no blending rule between the Kc branches.

- **nfi-g-growth.** Graphite review NFI-3. Growth plus joining is 4160 to 28235 kg per row and 070's outputs do not decompose it.

- **nfi-g-gamma.** Graphite review NFI-4. gamma_d = 0.20 for hemispheres rests on CR-1457 figure 6.2-3, which the review could not re-read.

- **nfi-g-scarf.** Graphite review NFI-5. The wrinkling level rides the unpinned applied stress, and the 10 MPa scarf screen is an owner assumption.

- **nfi-e-072b.** 072b limits. The carbon outcome rests on unmeasured wall modulus and in-plane expansion. The Kevlar values are typical, not lot minima. The model keeps 2.2-14, so no corrected-law closure follows. The future-dated RESULTS completion stamp is excluded.
