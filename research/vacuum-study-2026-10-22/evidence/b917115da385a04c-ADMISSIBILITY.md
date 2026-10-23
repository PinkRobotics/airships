# MAINLINE062 input admissibility

**QUESTIONABLE / PROJECTION. Decision: 047 is not admissible as a physical
fabrication tolerance for the proposed hull.** It remains a useful conditional
numerical study. No new FE run or tolerance sweep is performed.

| Input | Sourced value and product form | Disposition |
| --- | --- | --- |
| CR III small-strain normal/transverse properties | Hexcel CR III **5056**, 3/8-inch cell, 1.0 pcf: density 16.0185 kg/m³; stabilized compression modulus 15 ksi = 103.421 MPa; plate-shear moduli L 15 ksi = 103.421 MPa, W 6.8 ksi = 46.884 MPa. Table II test thickness is 0.625 inch = 15.875 mm. | **Admissible with a named limit:** catalog coupon anchors, not qualified installed properties at the 22–65 mm core thicknesses or after forming, perforation and bonding. |
| CR III strength anchors | Stabilized compression 60 psi typical / 35 psi minimum average; bare compression 55/25 psi; crush strength 35 psi typical. L shear 55/45 psi and W shear 35/25 psi, typical/minimum average. 1 psi = 0.006894757 MPa. | **Admissible with a named limit:** isolated catalog strength screens. Minimum average is not a guaranteed minimum specimen strength. Peak, crush and initial elastic modulus are separate quantities. |
| Complete CR III elastic tensor | No matched E1, E2, G12 and Poisson-coupling tensor established in the inspected sources. 047's final 1 MPa in-plane E and 0.5 MPa in-plane G are regularization. Its historical 0.01/0.005 MPa entries are not the final model. | **Not admissible.** Obtain directional small-strain tests and a reciprocal positive-definite tensor, or validated cell homogenization tied to measured foil/node geometry and coupon tests. |
| CR III through peak, crushing, unloading and mixed loading | A catalog crush-strength scalar supplies no loading curve, densification strain, unloading slope, residual strain, damage evolution or mixed normal/shear interaction. 056's PVC-foam extension supplies none of these for CR III. | **Not admissible.** Obtain matched normal and shear curves, unload/reload cycles and combined-load tests, including thickness, ribbon orientation, venting, cure and service temperature. |
| Finished Be face compression | Materion SR-200 is sheet. Its 345 MPa minimum is **tensile** yield. 036 found blank Fcy entries in the inspected sheet handbooks. Its historical 1.96 mm SR-200 values are 379.2/382.7 MPa L/LT, without the required thin-sheet/process/biaxial basis. | **Not admissible as Fcy.** Establish L/LT/off-axis and biaxial compression for purchased, formed, machined/etched, bonded stock at the finished minimum gauges, with lot scatter and temperature. Product availability does not establish a compressive allowable. |
| Be scalar elastic modulus | The currently opened **SR-200 sheet datasheet explicitly lists 290 GPa** as a physical property, with density 1.85 g/cm³. This corrects the blanket characterization of that scalar as unsourced. | **Admissible with a named limit:** representative scalar for a conditional calculation. It does not establish the thin-sheet orthotropic tensor, lot minimum or isotropic J2 law. CHECK047's +0.015 mm sensitivity at 298.7 GPa remains a numerical sensitivity. |
| Face stock dimensions/gauge | The maker lists the thin 0.020–0.058 inch sheet class at narrower/shorter sizes than 24 × 72 inches. The R10 bill's 0.809 mm face is in that class. | **Not admissible as a confirmed procurement layout.** Obtain minimum finished gauge, actual usable blank dimensions, forming yield and thickness/contour maps. R20/30 nominal gauges are thicker, but still need procurement confirmation. |
| AF 163-2U film identity and mass | 3M lists unsupported **2U 0.015 lb/ft²**, nominal 2.5 mil, and weight tolerance ±0.005 lb/ft². Thus this light film exists; a heavier film is not automatically substituted in the bill. | **Admissible with a named limit:** catalog identity/nominal mass. Verify installed adhesive mass, squeeze-out and acceptance at the actual core nodes. |
| Processed bond at 200 °F | The family guide permits longer 200 °F cures. However, the explicit p.15 200 °F strength table is **2K 0.060 lb/ft² on aluminum**, not 2U 0.015 on Be/CR III. The p.11 2U results use a different cure and aluminum substrates. | **Not admissible as the proposed processed bond law.** Obtain exact Be surface preparation, primer, film weight, pressure/temperature history, peel/flatwise/shear and mixed-mode fracture data, plus unload/cycling and environmental aging. A family cure option is not an installed-joint qualification. |
| Cure and scarf | 037b's core-force argument and 3.410223 MPa face debit are homogenized estimates. Its 30.3414:1 scarf and 10 MPa screen do not establish the in-place room-temperature Be seam's strength or residual geometry. | **Not admissible as a manufactured state.** Measure cure locking/relaxation, thermal distortion, residual strain and the actual seam; carry those states into the model. |

The core facts above are from [Hexcel Table II, p.5](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf).
The sheet facts are from [Materion DS-HPP-613, pp.1–3](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6)
and the pinned 036 evidence. Bond identity/cure distinctions are from
[3M AF 163-2, pp.1, 11, 15, 19](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf).
The borrowed mechanics and their limitations remain attributed to the pinned 037b,
047, CHECK047 and 056 cards; they are not promoted to measurements.

**What decides the small-dimple answer.** CHECK047 changes the core regularization
over 0.01–10 MPa and moves the estimated threshold by at most 0.004 mm. Face yield
governs. The decisive missing quantities are therefore the processed face's
compressive capacity and gauge, the manufactured/cured residual state, and the
actual defect spectrum and seams. Core-law incompleteness still prevents physical
qualification; it is a poor reason to spend another dense sweep merely tuning
unsourced in-plane moduli.

The admissible future calculation and the source/test prerequisites are specified
in `FE-NEXT.md`. All unresolved transfers are in `NFI.json`.
