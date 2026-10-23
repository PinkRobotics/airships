# CHECK-039 source readings

Primary PDFs, extracted text and selected page images are under sources/ and pinned in INPUTS.json. CR-62257 and IDH were downloaded directly from NTRS. The SP-8032 mirror returned 403; its archived primary PDF was copied read-only and matches the filed SHA-256. No reliance on owner code.

## CR-62257

[NASA CR-62257](https://ntrs.nasa.gov/api/citations/19650012174/downloads/19650012174.pdf), PDF pages 39–41 and 188–203, supports the quoted cap tests. Table 1.2 gives 5.87, 6.54 and 3.96 psi; the later table prints 5.86 for 1-G. The reported coefficients give 0.348/0.6125=0.568163 and 0.377/0.6125=0.615510. Normalizing the third design prediction gives (3.96/4.03)(0.4/0.6125)=0.641718, a design-based estimate rather than a new measured-geometry fit.

The aluminium result is 62.2 psi and co=0.52: 0.52/1.225=0.424490. Plasticity/residual-stress concerns are correctly retained.

An additional limitation appears on PDF page 201: close machining tolerances were achieved only over a central area about 20 inches in diameter, with stronger surrounding material supporting it. Thus psi=28.020476, computed from the design dimensions, does not describe a demonstrated universal threshold. The plastic psi values reproduce using nu=.35, and the aluminium value using nu=.33; these choices are not explicit in INPUTS.json. SUPPLEMENTARY.json separates the geometry calculation from test evidence.

## Isogrid Design Handbook

[NASA CR-124075](https://ntrs.nasa.gov/api/citations/19730011184/downloads/19730011184.pdf), printed 4.1.012 / PDF page 62, gives gamma=.425 for heavily stiffened domes, referring to one test. It sends lightly stiffened domes to Reference 2-8. The stated co=.260 is consistent with .612·.425=.2601.

The page contains **no psi≥28 or gamma_s≥10 criterion**. MAINLINE-039's quantitative classification is a proposed transfer rule. Its wording that the handbook applies “only at psi of about 28 or more” should be revised accordingly.

## SP-8032

[NASA SP-8032](https://everyspec.com/NASA/NASA-SP-PUBS/download.php?spec=NASA_SP-8032.046171.pdf), printed pages 5–6 and 24–25, supports gamma=.14+3.2/lambda² for the stated cap comparison. Equation 3 defines lambda from thickness, curvature and cap angle; equation 20 provides an effective thickness for orthotropic use.

Printed page 24 requires local-bay checks, discusses test verification and neglects eccentric coupling in its quoted formulation. It does not calibrate a triangular sandwich bay or a clamping threshold. Equal-area cap mapping and the plateau/branch rules are additions to the model.

The phrase “0.14 at a complete sphere” should read **approximately 0.14 in the large-lambda limit**. At any finite lambda the printed expression is greater than .14. This small wording correction does not establish transfer to a framed complete sphere.

## Ossola: arithmetic in the source table

[Accepted JSR manuscript](https://iris.polito.it/retrieve/handle/11583/2859044/e384c432-d634-d4b2-e053-9f05fe0a1d67/Design%20of%20Isogrid%20Shells%20for%20Venus%20Surface%20Probes.pdf), PDF pages 20 and 22: the plain-shell figures 317 and 917 bar imply **0.345692**, while Table 4 prints 33%. Retain that discrepancy rather than repeating 0.33 as checked arithmetic. Isogrid 410.3/934=0.439293. The three tests 414, 411 and 406 bar have mean 410.333 and sample standard deviation 4.041 bar. The author's uncertainty over buckling versus yielding is accurately retained.

## Cylinder evidence

These are cylinder-specific comparisons, not spherical-hull factors.

- [TA01](https://ntrs.nasa.gov/api/citations/20150017037/downloads/20150017037.pdf), PDF pages 14, 29, 33 and 41: 689.2/726.8=0.948266. The denominator is the perfect uniform-cylinder bifurcation prediction, whereas the nonlinear prediction includes imperfections and weld details.
- [TA02](https://ntrs.nasa.gov/api/citations/20170005857/downloads/20170005857.pdf), PDF pages 33, 38, 66 and 90: the combined-load reference is .4·726.8=290.72 kips, so LS4 gives 286.2/290.72=0.984452. LS5's 280.0 and 279.7 values are retained with their locations; the nonlinear comparisons use their matching denominators.
- [TA07](https://ntrs.nasa.gov/api/citations/20190000441/downloads/20190000441.pdf), PDF pages 13–14: 554/647−1=−14.374%. That comparison is against a nonlinear pretest prediction, not classical theory.
- [STA8.1](https://ntrs.nasa.gov/api/citations/20180001127/downloads/20180001127.pdf), PDF pages 1–4 and 7: **759,000 lb is the geometry-refined model; 754,000 lb also includes load nonuniformity.** The LIT row wrongly labels these as inconsistent. Relative to 743,000 lb, their errors are 2.153% and 1.480%; the body's 1.5% label for the intermediate 759,000 value is inaccurate. The 0.570-inch total height and 0.500-inch table height can be reconciled as 0.070-inch skin plus a 0.500-inch web; this is an interpretation requiring explicit height labels. Test/pretest is 743/697−1=6.600%, versus the paper's approximate 6%.
- [ETTA2](https://ntrs.nasa.gov/api/citations/20180006174/downloads/20180006174.pdf), PDF page 7: the reported .82/.74/.54 values are present, with combined loading and internal pressure. The passage does not supply the absolute classical load needed for an independent division.
- [SP-8007 Rev 2](https://ntrs.nasa.gov/citations/20205011530), printed pages 16–17 and 35–36: the .65 recommendation and comparison with the earlier .75 recommendation are correctly represented for the specified stiffened-cylinder application.
- [Hilburger 2012](https://ntrs.nasa.gov/api/citations/20120008172/downloads/20120008172.pdf), Table 1, reproduces the historical ranges in the LIT row. [Hilburger 2018](https://ntrs.nasa.gov/api/citations/20180006178/downloads/20180006178.pdf) describes the analysis-based method; it supplies no replacement spherical factor.

The Pineda reciprocal factors independently reproduce as 1/1.238=.807754443 and 1/1.0285=.972289742. Their measured percentages and the S-II .21–.22 values are inherited from the pinned CHECK-035 evidence, not newly re-extracted from those experiments in this check. That provenance remains explicit.

The unopened DTMB lead stays an unopened lead. No absence-of-literature conclusion is drawn from it.
