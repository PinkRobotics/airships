# MAINLINE-040 / 037b explicit bond rows

QUESTIONABLE / PROJECTION. This addendum closes the late fold order. The filed 040 account already uses the 200 °F cure and 30.341397:1 scarf fix. This addendum supplies its explicitly requested as-designed counterpart: 250 °F cure, 30:1 scarf, the compliant-core 037b model, and the same complete bill.

The as-designed bond field survives cure in 037b's compliant-core model. The minimum-strength free-edge screen fails (about 0.83); the typical-strength screen is about 1.16. Those statements concern different locations and strength statistics. No as-designed row passes the complete 040 screen, regardless of the four optimism axes. A longer scarf alone cannot cure this edge failure. The fixed row retains approximately 1.07 minimum edge factor.

For comparison, as-designed shell thicknesses are reoptimized with only the free-edge feasibility filter relaxed. This gives a conditional mass price, not an accepted float. Every reported safety factor and assembly flag keeps the failure. The fixed row is reproduced from immutable 040 output. All 120 account combinations have both rows in PAIRED-ROWS.csv, plus a common fixed-geometry comparison in RESULTS.json.

|R (m)|Weather|Account|As-designed conditional payload (kg)|Fix payload (kg)|As-designed edge SF|Fix edge SF|
|---:|---|---|---:|---:|---:|---:|
|10|ISA|actual|-154.130|-109.649|0.830514|1.071882|
|10|ISA|floor|-154.130|-109.649|0.830514|1.071882|
|10|optimistic|actual|-303.622|-257.973|0.830515|1.071884|
|10|optimistic|floor|-306.259|-258.040|0.830515|1.071884|
|10|both|actual|-641.577|-596.529|0.830514|1.071883|
|10|both|floor|-641.868|-596.529|0.830514|1.071883|
|12|ISA|actual|-33.643|43.246|0.830478|1.071821|
|12|ISA|floor|-84.740|-3.499|0.830478|1.071821|
|12|optimistic|actual|-292.039|-213.132|0.830479|1.071824|
|12|optimistic|floor|-351.002|-267.651|0.830479|1.071824|
|12|both|actual|-875.987|-798.118|0.830479|1.071822|
|12|both|floor|-930.902|-848.636|0.830479|1.071822|
|15|ISA|actual|338.649|488.899|0.830437|1.071752|
|15|ISA|floor|132.779|291.539|0.830437|1.071752|
|15|optimistic|actual|-166.247|-12.053|0.830438|1.071754|
|15|optimistic|floor|-387.458|-224.575|0.830438|1.071754|
|15|both|actual|-1306.659|-1154.494|0.830437|1.071753|
|15|both|floor|-1519.974|-1359.213|0.830437|1.071753|
|20|ISA|actual|1658.235|2014.691|0.830379|1.071654|
|20|ISA|floor|919.894|1296.561|0.830379|1.071654|
|20|optimistic|actual|460.604|826.414|0.830381|1.071657|
|20|optimistic|floor|-314.001|72.449|0.830381|1.071657|
|20|both|actual|-2242.160|-1881.166|0.830380|1.071655|
|20|both|floor|-2998.101|-2616.688|0.830380|1.071655|
|30|ISA|actual|8152.829|9357.973|0.830277|1.071481|
|30|ISA|floor|4826.570|6100.222|0.830277|1.071481|
|30|optimistic|actual|4105.313|5342.079|0.830279|1.071485|
|30|optimistic|floor|657.470|1964.195|0.830279|1.071485|
|30|both|actual|-5013.691|-3793.198|0.830278|1.071483|
|30|both|floor|-8398.962|-7109.257|0.830278|1.071483|

On 037b's original 028b geometry, its reported 250 °F result adds 4.403 MPa balanced face compression, takes usage from 0.971978 to 1.052282 and gamma to 0.618429. Its 200 °F / 30.341397:1 repair adds 0.120151 kg there. These source values are not transplanted as a constant surcharge at all radii: our paired rows recompute geometry, joining mass and residual stress.

The older comparison-037 directory in the filed report is the rigid, cold-reference thermal model. It is not the as-designed 037b row. The original 040 report and its artifacts are unchanged.

Validation: all 120 fixed rows reproduce their filed payload within 1e-8 kg; all 120 conditional rows preserve the failed edge and satisfy every other mode used by the optimizer; all mass sums close within 1e-8 kg. The edge failure bound covers every interpolation knot for all five radii and is independent of the four optimism axes.

Installed-hull SF remains unknown. Free-edge homogenization, creep and fatigue, bond/core preparation, thermal cycles, hardpoints and the original 040 qualifications remain open. This is an analytical comparison, not proof of an installed joint.
