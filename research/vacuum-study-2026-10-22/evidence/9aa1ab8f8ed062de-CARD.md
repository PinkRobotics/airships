# MAINLINE-048 — coating and retained water

**QUESTIONABLE / PROJECTION. R10 floats again in the selected ISA account if a sufficiently light finish achieves the assumed optics and the 037b cure repair works. The mass recovery comes chiefly from replacing the 0.20 kg/m² coating allowance. The existing exterior-water debit remains aboard. No installed-hull safety factor is established.**

The lightest source-described recipe screened here is multilayer CCAg/ITO, calculated at 7.5752 g/m² before an assumed 10% application allowance. Its optical pair is transferred from NASA's coating class to this recipe and Be, so it is a candidate, not a qualified lightest finish. The more directly paired classical CCAg recipe is 9.326–11.179 g/m²; a catalog Ag/FEP tape including adhesive is 88 g/m² at 0.5 mil. White-paint thickness data do not establish their installed mass. Sources and unresolved transfers are detailed in [SOURCE-AUDIT.md](fa88eaee87d844a8-SOURCE-AUDIT.md).

The three drying routes below share R10 ISA, the retained joining floor, heavy pad, vented core, 100 kg systems and 10 g/m² additional structural primer. Only the bake column assumes 90% removal of added material water:

| Finish | Applied optical finish, kg at R10 | Dry-gas payload | Bake payload | Onboard-sorbent payload |
|---|---:|---:|---:|---:|
| MLCCAg | 10.471 | +123.036 | +124.262 | +94.390 |
| CCAg | 12.891 | +120.226 | +121.474 | +91.315 |
| AgFEP05 | 116.113 | +15.556 | +17.403 | -20.685 |
| AgFEP1 | 151.739 | -19.816 | -17.954 | -56.240 |

Payloads are kilograms at 028b's endpoints. The original 040 row was **-109.649 kg**. The selected multilayer case is **+124.262 kg**; its exterior water is still **125.664 kg**. Coating replacement saves 240.856 kg, the new structural primer costs 12.566 kg, added residual material water costs 0.136 kg, and the changed thermal/geometry/joining terms supply the remaining +5.758 kg. Exact closure is in [R10-RECONCILIATION.json](5b45d6904dd15be3-R10-RECONCILIATION.json).

## Finish screen

| Finish | α / ε used | Nominal added mass, g/m² | 037 day SF | Full-cycle SF | Current 200 °F edge SF |
|---|---:|---:|---:|---:|---:|
| [040 assumed white paint + primer](1cbdd9a60e056abd-INPUTS.json) | 0.200 / 0.900 | 200.000 | 1.678 | 0.917 | 1.072 |
| [AZ-93, at least 127 um](https://www.aztechnology.com/product/1/az-93) | 0.170 / 0.890 | unknown | 2.019 | 1.013 | 1.073 |
| [Z-93, 114.3 to 152.4 um](https://ntrs.nasa.gov/api/citations/19730017242/downloads/19730017242.pdf) | 0.184 / 0.880 | unknown | 1.817 | 0.961 | 1.073 |
| [SolarWhite, 150 to 220 um](https://enbio.eu/solar-white/) | 0.180 / 0.890 | unknown | 1.883 | 0.977 | 1.073 |
| [0.5 mil Ag/FEP + 3M966 tape](https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf) | 0.090 / 0.400 | 88.000 | 2.359 | 1.306 | 1.123 |
| [1 mil Ag/FEP + 3M966 tape](https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf) | 0.090 / 0.480 | 115.000 | 2.678 | 1.336 | 1.111 |
| [0.5 mil Al/FEP + 3M966 tape](https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf) | 0.140 / 0.400 | 88.000 | 1.467 | 0.977 | 1.123 |
| [2 mil Al/FEP + 3M966 tape](https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf) | 0.140 / 0.600 | 169.000 | 1.864 | 1.049 | 1.097 |
| [0.5 mil Al/polyimide second surface + silicone PSA](https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf) | 0.360 / 0.520 | 54.000 | 0.679 | 0.537 | 1.106 |
| [SiOx over Al/polyimide, high-emittance option](https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf) | 0.130 / 0.260 | unknown | 1.314 | 0.971 | 1.149 |
| [Classical direct CCAg/ITO](https://patents.justia.com/patent/11391493) | 0.090 / 0.650 | 9.326 | 3.513 | 1.395 | 1.092 |
| [Direct multilayer CCAg/ITO, 80 oxide pairs](https://patents.justia.com/patent/11391493) | 0.090 / 0.800 | 7.575 | 4.504 | 1.442 | 1.079 |
| [Chemically polished Be (historical Brush QMV)](https://ntrs.nasa.gov/api/citations/19690012311/downloads/19690012311.pdf) | 0.500 / 0.100 | 0.000 | 0.346 | 0.331 | 1.198 |
| Native/oxidized Be | unknown | unknown | unscored | unscored | unscored |

Masses above are nominal coating/tape values, before the declared application allowance and separate structural primer. Structural primer is charged outside the original four-component joining/floor bill. Classical CCAg's full recipe band is 9.326–11.179 g/m². The SolarWhite α interpretation is unresolved because its web heading says reflectance. The SiOx/polyimide construction has no sourced installed mass. Bare Be is the historical chemically polished surface, not a durable outdoor optical specification.

The first factor reproduces 037's day comparison at its original geometry and typical shear strength. The second explicitly spans the hot day to cold night. The last uses the current 037b 200 °F cure-reference model and minimum-strength core shear; these factors are not interchangeable. The declared finish screen is day ≥1.678 **and** full-cycle ≥1. Only the sourced optical assumptions, not qualification, are being screened. Full UV, humidity and Be-adhesion findings for every candidate are in [COATING-EVIDENCE.md](7abf8107c6d958d6-COATING-EVIDENCE.md). Space heritage or base-film weathering does not establish complete atmospheric-hull life.

## What the water account represents

040 → 033 → 028b/019 → 016 traces the exterior debit to an **assumed 0.1 mm retained liquid film**, selected from 016's 0.1–1 mm band. At water density 1000 kg/m³, this is 0.1 kg/m²: 125.664, 180.956 and 282.743 kg at R10, R12 and R15. It is not adhesive moisture. Baking or an internal bed cannot remove later exterior dew or rain.

Historical AF163-2U records have WVR 0.09–0.20%, distinct from TML 2.59–4.85%. WVR follows a specified vacuum test and 24-hour humidity exposure; it is not the chosen 200 °F cure's equilibrium moisture uptake. The main added-water proxy uses 0.20%. Core, structural-primer, seam-polymer and deposited-finish uptake remain assumed. FEP base-film absorption is sourced below 0.01%; the complete PSA construction is not. The severe 9.16% adhesive sensitivity comes from different AF163-2M specimens immersed at 70 °C and is not treated as 2U room-humidity data. [Moisture sources and definitions](fa88eaee87d844a8-SOURCE-AUDIT.md).

The new material inventory is charged above nominal dry/reference masses without removing nominal adhesive TML. It also retains 040's nominal volatile-pressure allowance; nominal mass/moisture baselines still need measurement.

| R, m | Route | Material water before → aboard, kg | Exterior water aboard, kg | Added bed/cartridge, kg | Ground resource scenario |
|---:|---|---:|---:|---:|---|
| 10 | dry_gas | 1.362 → 1.362 | 125.664 | 0.000 | 20,944 m³ / 23,644 kg N₂ |
| 10 | bake70 | 1.362 → 0.136 | 125.664 | 0.000 | ≥122.4 kWh ideal heat |
| 10 | desiccant | 1.362 → 1.362 | 125.664 | 28.646 | regeneration/equipment unsourced |
| 12 | dry_gas | 2.169 → 2.169 | 180.956 | 0.000 | 36,191 m³ / 40,857 kg N₂ |
| 12 | bake70 | 2.169 → 0.217 | 180.956 | 0.000 | ≥210.4 kWh ideal heat |
| 12 | desiccant | 2.169 → 2.169 | 180.956 | 43.164 | regeneration/equipment unsourced |
| 15 | dry_gas | 3.877 → 3.877 | 282.743 | 0.000 | 70,686 m³ / 79,799 kg N₂ |
| 15 | bake70 | 3.877 → 0.388 | 282.743 | 0.000 | ≥409.0 kWh ideal heat |
| 15 | desiccant | 3.877 → 3.877 | 282.743 | 72.903 | regeneration/equipment unsourced |

These are primary multilayer ISA endpoint geometries with the retained joining floor. At R10, the bake scenario removes only 1.226 kg of this added material water, leaving 0.136 kg. The onboard bed adds 28.646 kg while retaining the water aboard. External film dominates both.

The bake's 90% reduction is an **acceptance target requiring measurement**, not a demonstrated duration or process. Heat figures are ideal lower bounds with stated engineering heat-capacity assumptions, excluding tooling, pumping, losses and binding energy. Five hull-volume nitrogen exchanges are a hypothetical ground-enclosure cost; smaller panel/glovebox assembly changes it. Dry-gas assembly receives no removal credit for pre-existing material water. Bed capacity/capture at vacuum are projections. No financial quote or achieved cycle time is sourced. Details and by-material inventories are in [DRYING-COSTS.json](29dd6fef0cf42f44-DRYING-COSTS.json).

## R10, R12 and R15 account

The following uses the lightest recipe candidate, retains 0.1 kg/m² exterior water, and carries every 040 primary debit. Each cell gives **actual joining / retained joining floor** endpoint payload in kg.

| R, m | Weather | Dry gas: actual / floor | Bake: actual / floor | Sorbent: actual / floor |
|---:|---|---:|---:|---:|
| 10 | ISA | +123.036 / +123.036 | +124.262 / +124.262 | +94.390 / +94.390 |
| 10 | optimistic | -25.145 / -25.145 | -23.921 / -23.921 | -53.759 / -53.759 |
| 10 | both | -363.774 / -363.774 | -362.549 / -362.549 | -392.404 / -392.404 |
| 12 | ISA | +381.150 / +335.015 | +383.102 / +336.967 | +337.986 / +291.851 |
| 12 | optimistic | +125.055 / +71.157 | +127.003 / +73.105 | +81.946 / +28.047 |
| 12 | both | -460.076 / -509.979 | -458.126 / -508.029 | -503.213 / -553.117 |
| 15 | ISA | +1024.765 / +828.805 | +1028.255 / +832.295 | +951.862 / +755.902 |
| 15 | optimistic | +524.467 / +313.372 | +527.949 / +316.854 | +451.666 / +240.571 |
| 15 | both | -618.310 / -821.615 | -614.824 / -818.129 | -691.162 / -894.467 |

Least named optimism sets with the retained floor follow. G=global coefficient, Q=wrinkling factor, F=film weight, E/F=coupled face-material tuple. Numbers are the common normalized logarithmic usage, with 0=today and 1=declared endpoint. Selection minimizes axis count first, then common usage. `none` means no floating solution within the four stated endpoints, not impossibility under every design.

| R, m | Weather | Dry gas | Bake | Sorbent |
|---:|---|---|---|---|
| 10 | ISA | G+Q+F 0.834773 | G+Q+F 0.833076 | G+Q+F 0.873829 |
| 10 | optimistic | none | none | none |
| 10 | both | none | none | none |
| 12 | ISA | G+Q 0.887051 | G+Q 0.884705 | G+Q 0.947737 |
| 12 | optimistic | G+Q+F 0.930518 | G+Q+F 0.928595 | G+Q+F 0.972719 |
| 12 | both | none | none | none |
| 15 | ISA | G+Q 0.722673 | G+Q 0.720757 | G+Q 0.767374 |
| 15 | optimistic | G+Q 0.943987 | G+Q 0.941833 | G+Q 0.997147 |
| 15 | both | none | none | none |

For R10 ISA bake, the least point uses G+Q+F 0.833076: gamma=0.493130, Q=0.704415, film=0.08221979 kg/m²/interface, E=290 GPa. The selected geometry and every individual coefficient are in [ROWS.csv](093f5c2bc8203281-ROWS.csv) and [RESULTS.json](a9458542ae7efde6-RESULTS.json). Those files include all 432 configurations, both joining conventions, all three drying routes, all four selected finishes, weather cases, endpoints, subset trials and least sets.

R10's retained-water optimistic-weather and both-weather rows remain negative even with the light deposited finish. R12's optimistic-weather rows can become positive; both-weather remains negative throughout R10–15 in this account. These remain coupled mass/scalar-model statements, not mission qualification.

## Conditional dry operations and robustness

Deleting the exterior-water layer is a separate dry-operating assumption. It is **not** a result of the bake. Under the bake route and retained joining floor, it gives:

| Finish | R10 ISA, no exterior water | R10 optimistic, no exterior water | R10 both, no exterior water |
|---|---:|---:|---:|
| MLCCAg | +249.926 | +101.743 | -236.886 |
| CCAg | +247.138 | +98.935 | -239.683 |
| AgFEP05 | +143.067 | -5.179 | -343.775 |
| AgFEP1 | +107.710 | -40.520 | -379.124 |

At R10 ISA the multilayer bake endpoint can carry up to 0.198884 kg/m² exterior water within the same dry-optics model, equivalent to 0.198884 mm of water. That is a mass threshold, not a drainage prediction. The inherited 1 kPa vapor pressure gives a dew point of 280.13 K; the modeled dry-night surfaces are colder. Condensation/frost and wet optical properties therefore remain explicit open issues.

| Assumed optical case | 037 day / full-cycle SF | R10 ISA endpoint, kg | Meets both finish screens? |
|---|---:|---:|---|
| wet_optics_assumed (0.2/0.95) | 1.754 / 0.931 | +118.756 | no |
| aged_alpha015_assumed (0.15/0.8) | 2.149 / 1.067 | +120.755 | yes, in this model |
| aged_alpha020_assumed (0.2/0.8) | 1.534 / 0.890 | +117.957 | no |

A positive current-account payload in the table does not cure a failed legacy full-cycle finish screen. At ε=.80, the source-geometry day/full-cycle screen permits α only up to about 0.166490. That is a model aging limit, not an observed lifetime.

Other R10 ISA sensitivities are in [SENSITIVITIES.json](a49060527f34627c-SENSITIVITIES.json). The multilayer margin survives 50 g/m² structural primer and the declared scalar scarf/edge interaction, but the 0.5 mil tape margin does not. At the high-uptake/no-extra-drying sensitivity, that tape is slightly negative. The maximum classical recipe remains positive. Changing back to the original 250 °F cure and 30:1 scarf produces no geometry passing the retained minimum-strength edge screen for any of the four finishes; optical improvement does not replace the 037b cure fix.

Using an assumed hemispherical ε=.40 for classical CCAg, while keeping its deposited mass, gives R10 ISA payload +120.692 kg. This is a robustness sensitivity for the unresolved emittance statistic, not a measured CCAg property.

## Verification and remaining qualifications

Validation passed **213,078 checks** across **7,149 distinct stored points** and 432 configurations: independent mass/pressure/mode calculations, original-040 regression, denser primary geometry searches, direct 256-point thermal solves and favorable bounds for the nonmonotone face-material axis. [VALIDATION.json](0bc96ccc64903c71-VALIDATION.json) records tolerances and failures; [METHOD.md](c0248a88a5cc1d46-METHOD.md) gives equations, conventions and reproduction steps.

All eight selected four-axis points also underwent an independent E-usage scan and bounded refinement at their minimax ceilings. None improved payload by 0.002 kg; numerical search scope is recorded in [ADDITIONAL-AUDIT.json](bb84751c724a2de2-ADDITIONAL-AUDIT.json).

The service audit checks refined cavity volume, zero sorbent capture and removal of the inherited nominal-conditioning assumption. These calculations do not validate leaks, cure, sorption or process performance. All 040 qualifications remain, along with 28 new material/process findings in [NFI.json](c6e095ff87c11b12-NFI.json). The relevant gates are matched coating mass/optics and life, Be adhesion, actual material-water inventory, the 200 °F cure/primer process, gamma/Q/film qualification, joints, venting and the combined weather/thermal/water mission. **Installed-hull SF remains unknown.**

Conditional payload and onboard water accounting [source link unavailable in this public projection]

The brief is complete. Stop and file; the robotics seat supplies any next job.
