# MAINLINE-052 source and boundary audit

This is a synthesis of pinned filings and a new algebraic calculation, not a new literature search or fresh finite-element solution. The original source pages and qualification limits remain with the cited upstream packages. No claim is made that this unit newly verified every manufacturer's current document or a regulatory requirement.

| Input | Use here | Boundary retained |
|---|---|---|
| 041 + CHECK041 | f5-019 geometry, checked static forces, eigen scaling, local/joint equations; f5-5 sensitivity | No nonlinear qualification; film stiffness receives no frame credit |
| CHECK037 | SiC/arc tube masses and material mapping | Ti/CFRP identify fittings; all tubes use 3100 kg/m³ and 410 GPa |
| 046 + CHECK046 | OD4 white package, hot/fully restrained film screen, retention targets and cold humidity criterion | No qualified outdoor one- or ten-year installed life |
| 034, this seat's prior work | Species, coupon transmission, seam/node leakage, finite desorption inventories, service hardware and battery equations | Gas source-rate envelope; installed leakage/conditioning/pump performance unmeasured |
| 043, 043fold and CHECK043 | Both 3.9 GPa scale readings, m=10 hazard formulas and 750-member validation tables | Compression m and reference-size scale are hypotheses, not calibrated distributions |
| 040, this seat's frozen independent check | Complete weather, 70-knot envelope, gas/water/system accounting and P2 comparison | P2 thermal lookup was a conditional input in that audit; no new P2 qualification |
| 048 | Exterior water .1 kg/m² and improved P2 coating/bake comparison | No R=20/30 048 result; optical, life and drying transfer remains open |
| 045 | Existing damage objections | No new damage tolerance, tear arrest or hail shield is claimed |

UPSTREAM-PINS.json records 237 verified non-executable artifact pins and 36 excluded code/archive entries. Exclusions were selected from metadata before file access. BRIEF-PINS.json records four briefing artifacts. EXTRA-PINS.json records eight further 041/CHECK041 numerical files plus four own prior-check artifacts (one is this seat's own code). Pins are not necessarily distinct physical files; the package integrity check separately hashes every actual packaged file.

The source-grade distinction is important. 043's `SA_catalog_compression` entry is a typical 3900 MPa compression number with no fitted m, characteristic scale, reference volume or sample count. The 380 MPa/m=10 flexure entry is a different loading population and is **not** used as the axial compression baseline. The numerical 1 GPa baseline in this card is a declared qualification target, not an asserted material property.

The PBO 5.8 GPa yarn number and warehouse retention are inherited source observations. Construction efficiencies .6→1 and ten-year extrapolation are explicit projections. The white package's 25 g/m² layer is an allowance, not a product thickness or proof that the assembly achieves the specified optics or life.

The vacuum source conditions also differ: the 034 metallized-Mylar oxygen coupon is at 25 C/45% RH, while the stated water upper rate is at 38 C/90% RH. This card uses those as the declared source-rate envelope and does not claim a validated mapping to every weather case. OD4 is not credited with a lower WVTR merely because it is optically denser.

The input/output integrity checks, inherited NFI registers, code, execution records, source hashes and failed superseded sweep are supplied. These establish traceability and arithmetic, not physical qualification.
