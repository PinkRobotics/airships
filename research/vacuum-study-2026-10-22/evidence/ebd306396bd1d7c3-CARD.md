# MAINLINE-016 secondary NFI card — ESTIMATE

Unit ref-81587374594cae9c1e2e-nfi-1019. Status ESTIMATE. Tag QUESTIONABLE throughout. Certification none. The arithmetic is compute.py; RESULTS.json is the record. Base point is MAINLINE-009's P2 sandwich (SiC Hexoloy-SA-type faces 0.000272153646 m, Divinycell H35 core 0.0462419049 m at 38 kg/m3, R 10 m, 500 m ISA, least SF 0.23515931 global buckling, margin 244.472107509 kg). MAINLINE-012 is unfiled, so its 1/T and pressure terms are derived here from rho = p/(R_air T). A checker runs behind this card; its objections become rows, never a stop.

## 1. Holding the vacuum

The 1 percent lift loss per day allowance admits 48.894 kg of air per day inside, which is p_int 954.6 Pa, a throughput of 46.28 Pa m3/s. That allowance is equivalent to a 2.48 mm2 choked hole or a 4.25 mm2 molecular aperture: a gross defect, about a 1.8 mm diameter hole. Face permeation is nil against this budget: metal foil and monolithic sintered SiC are gas barriers (textbook), and even CFRP epoxy laminate, QUESTIONABLE at 1e-6 to 1e-5 scc/m2/s helium permeance (NASA composite cryotank literature) divided by 50 for air, passes 5.4e-5 percent of the budget. Interior outgassing at the QUESTIONABLE polymer band 1e-7 to 1e-5 Pa m3/s/m2 over 1256.6 m2 is 0.00 to 0.03 percent of the budget. The real gas problem is resident moisture: 0.5 to 3 percent of the 2208.2 kg PVC core is 11.0 to 66.2 kg of water, worth 347 to 2079 Pa if released to the void, against the 954.6 Pa one-percent ceiling. Bake-out and a vent at commissioning are required, not optional.

Holding p_int at a 1000 Pa ceiling takes 46.3 L/s there: 211 W isothermal ideal, 527 to 844 W at a QUESTIONABLE 25 to 40 percent Roots-plus-backing efficiency, and a QUESTIONABLE 150 to 400 kg pump set, which is 61 to 164 percent of the whole float margin. Pump-down at commissioning from 1 atm to the ceiling is 506 kWh of isothermal work. Optimistic: a 150 kg pump at 527 W with bake-out done on the ground. Conservative: 400 kg pump that the 009 point cannot carry.

## 2. Joints and seams

Seam length is 2A/w for square panels. At a 4 m panel, PROJECTION because no SiC face panel that size exists today, 628 m of seam costs 89.2 kg optimistic and 187.8 kg conservative, inside the 216.427 kg five percent allowance. At 2 m panels, standard width for aluminium sheet today and still a PROJECTION for SiC, 1257 m costs 178.3 to 375.5 kg, 82 to 174 percent of the allowance. At today's QUESTIONABLE Hexoloy plate size 0.5 m, 5027 m costs 713.4 to 1502.1 kg, 330 to 694 percent. At a conservative 0.25 m tile, 10053 m costs 1426.7 to 3004.3 kg, 659 to 1388 percent, leaving the hull 966 to 2543 kg heavy. The 009 point floats only on PROJECTION panels. QUESTIONABLE sources: Saint-Gobain Hexoloy SA product forms; doubler widths 60 to 120 mm owner assumption; epoxy film and splice paste densities 1250 and 1100 kg/m3.

## 3. Thermal

Energy balance with QUESTIONABLE clear-sky 970 W/m2, sky 260 to 275 K, and Whitaker convection: coated faces (alpha 0.20, epsilon 0.90) sit +2.5 to +3.8 K by day and -5.5 to -8.4 K by night; bare SiC (0.70/0.85) sits +14.6 to +21.2 K and -5.4 to -8.3 K. The no-convection bound is 313.5 K, under the QUESTIONABLE H35 service limit of 343 to 353 K (DIAB H series): solar alone does not cook this core, with the caveat that the balance averages sky and ground radiation, and a hot apron raises the ground side. The core equilibrates through-thickness in 357 s, so daily swings load the face-core difference in full transients.

That difference is the finding: CTE mismatch SiC 4.5e-6 against PVC 60e-6 per K drives sandwich shear-lag (Zenkert) with tau = dEps E tf lambda, lambda 1.526 per m, giving 283 kPa at 30 K and 567 kPa at 60 K. Against the QUESTIONABLE H35 shear strength band 0.40 to 0.55 MPa the one-off SF is 1.41 to 1.94 at 30 K and 0.71 to 0.97 at 60 K. This is a failure mode outside the five scored modes, cycled daily, unquantified for fatigue. Thermal geometric imperfection is second-order: 0.113 to 0.45 mm at 5 to 20 K vertical asymmetry, small against the imperfection a 0.20 knockdown already assumes. Property loss at temperature: SiC flat to far above this range; H35 derates above 50 to 60 C per datasheet class; the 6061 family would derate above 150 C, not reached here.

## 4. Loads beyond uniform pressure

Weather pressure: diurnal 1 hPa moves the governing SF by 0.1 percent; synoptic 3 percent gives 0.2283 to 0.2425; an extreme 10 percent storm low gives 0.2613 and margin 219.9 kg. All are noise against a mode already at 0.2352. Gust at 20 m/s: dynamic pressure 233 Pa, 0.24 percent of p_ext; drag 34.5 kN, mooring design load 48.3 kN at a QUESTIONABLE 1.4 gust factor. A bare hardpoint patch of 0.0707 m2 puts 683 kPa on the core against a 500.0 kPa QUESTIONABLE compressive allowable: SF 0.73, fails without a spreader; 0.145 m2 of spreader restores SF 1.5, about 48 kg of fittings for six hardpoints (owner assumption). Added air mass 2445 kg equals the hull mass, so mooring snatch is slow but doubled; ground handling needs cradle pads under 250 kPa. Local design and fixtures, not a mass problem.

## 5. Altitude and climate

With rho = p/(R_air T), dL/L = dp/p - dT/T at fixed volume. Climbing always loses lift here (about 9.4 percent per km), so hot-air loss is recovered by ballast, not altitude. QUESTIONABLE mid-latitude 500 m site band: a hot summer afternoon at +25.1 K from ISA loses 8.81 percent of lift, taking the margin to -186.3 kg: the hull does not float. A cold winter dawn at -11.9 K gives +448.7 kg; synoptic 2 percent pressure swings give 146.7 to 342.3 kg. Surface water: 0.1 mm retained film is 125.6 kg, 51 percent of the margin; 1 mm is 1257 kg. A hydrophobic coating, a shedding check, and a dawn-window or ballast operating rule are required with a site choice.

## Ranking and the two that most need grounding

By effect on margin or least SF: 1 seams (float-breaking at every producible SiC size today, up to 1388 percent of the allowance); 2 climate and water (margin negative on a hot afternoon, water at 51 percent per 0.1 mm); 3 thermal CTE mismatch cycling (a new mode at SF 1.41 to 1.94 on a 30 K daily swing); 4 the pump (61 to 164 percent of margin, 527 to 844 W); 5 weather, gust and point loads (SF moves 3 percent; mooring is local design plus about 48 kg).

The two most needing grounding: the seam row, because panel producibility alone decides whether the 009 point floats; and the site climate and water envelope, because it decides whether the 5 percent margin is real in summer.

## What is not claimed

No number here is a certification; every sourced value is QUESTIONABLE and every panel-size escape is PROJECTION. The five scored modes are MAINLINE-009's pinned numbers, not recomputed. Thermal bending of faces is negligible on this point because the membrane stress 877 MPa dwarfs the E alpha dT bending term. Nothing here re-runs the 009 optimization.
