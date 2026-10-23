# CHECK-059: retained-water audit

Complete with corrections and open qualifications. QUESTIONABLE / PROJECTION. No installed-hull qualification is asserted.

The drop/film and energy-balance arithmetic reproduces (7,094 fields). The 185 capacity comparisons reproduce within 3 g in payload and 3×10⁻⁶ kg/m² in capacity; all 37 least-set choices agree. Water-account arithmetic reproduces except the two coating-cost rows. Complete-drying claims, the coating bill and named pond placements need the changes below.

## Exact differences and consequence

| Item | Filed | Independent | Meaning |
|---|---:|---:|---|
| R10 coating dry mass, kg | 16.3363–47.1239 | 32.6726–94.2478 | Both supplier-required layers, same assumed density |
| R10 equal-price coating cost, USD | 8430.963714 | 16861.927429 | Both layers; not an installed quote |
| R30 equal-price coating cost, USD | 75878.673429 | 151757.346858 | Same correction |
| R10 pond angular-integral mean, kg | 36.629858851 | 35.596045531 | Continuum area integration of declared dish |
| R10 node-up ponds, kg | 55.149608596 | 110.766000568 | Explicit alternative tiling; filed placement not reproduced |
| R10 bay-up ponds, kg | 171.423902496 | 117.093891300 | Explicit alternative tiling; not a corrected real-hull result |
| Largest directional spill angle, deg | about 14 | 16.546263635 | Some declared bays retain water above 14 |
| R10 midday water left at the bulk time, kg | 0 (“fully dry”) | 11.707123–13.562237 | Dry parts stop evaporating |

MISMATCHES.json records exact numbers, signs, units and classifications; the comparison JSONs retain every scalar difference. POND-GRID-INDEPENDENT.json is a diagnostic of unreported quadrature, not a selected physical model.

## Drop calibration and retained loads

For cap base radius a and q=tan(theta/2), V=πa³q(3+q²)/6. Balancing rho*g*V*sin(beta) against 2*a*gamma*(cos(theta_R)-cos(theta_A)) gives a_c. Projected radius is a below 90° contact angle and a/sin(theta) above it. The plate fixes kappa=0.06264893813335032 and a_c=2.500176546338056 mm. This is a coverage/population calibration, not a measured critical radius for the hull.

| Finish, R10 | Rain after 10 min, kg/m² | Upper rain scenario | Reference dew | Saturated dew |
|---|---:|---:|---:|---:|
| paint_040 | 0.031051602 | 0.046002373 | 0.015956421 | 0.027195229 |
| MLCCAg | 0.028072068 | 0.041588249 | 0.014175944 | 0.023173297 |
| hydrophobic_FEP | 0.051481564 | 0.076268984 | 0.036734945 | 0.056001172 |
| slippery_silicone | 0.035986405 | 0.053313193 | 0.026421210 | 0.040116602 |
| superhydrophobic | 0.014219621 | 0.021066105 | 0.010875146 | 0.016538111 |

Rain 0.014219621–0.051481564 and dew 0.010875146–0.056001172 kg/m² reproduce. The ×1.481481 upper-rain scenario reaches 0.076268984 kg/m². Every retained profile and all radii are in RETAIN-INDEPENDENT.json. These values fit 0.1 kg/m² within this model, without waiting. They do not establish a measured upper bound.

## Capacity, with the named bill

| R, m | P2 ISA, kg/m² | P2 optimistic | P3 ISA | P3 optimistic |
|---|---:|---:|---:|---:|
| 10 | 0.194454341 | 0.076717845 | 0.124559764 | 0.039191489 |
| 12 | 0.306389817 | 0.165084673 | 0.227963613 | 0.125563639 |
| 15 | 0.457011978 | 0.280340664 | 0.357194234 | 0.229246714 |
| 20 | 0.688740584 | 0.453092281 | 0.544537950 | 0.374011186 |
| 30 | 1.126814566 | 0.773083400 | 0.886547811 | 0.630862558 |

Capacity is 0.1 + endpoint payload/(4πR²). P2 includes cure compression in global/crimp, bake, mirror coating and actual joining without the 5% floor. This explains why its R12 value differs from the retained-floor primary case in CHECK-053. P3 uses this seat’s independently derived MAINLINE-052 ground-service bill; the owner rounded endpoint payloads to 0.001 kg. One kg/m² exterior water floats only at R30 ISA among the sampled cases, on gamma/Q/film, usage about 0.917466 and about +1434.239 kg. Full endpoints, least choices and signed residuals are supplied.

## Pond geometry and operating claim

The charged spherical-cap crown ratio is 0.0425728922436619, and circular mean/crown is 0.503624902307981; these give s=2.324346196605 m at R10, crown 0.098954140165 m and 116.585202 kg for a level bay. The area-based equivalent bay count is 537.164867, while the actual f5 frame has 500 faces. This is already an effective surrogate.

For the stated triangular dish, d=k*c*t*(2-t), t=3 min(lambda). Uniform triangle area makes mean[t(2-t)]=1/2, hence k=1.007249804616. The reported 1.0173672190414051 is independently reproduced with 301 barycentric divisions and equal weights including the rim; it does not represent the continuum area average. Exact strip integration agrees with independent two-dimensional quadrature in nine checks. The angle-averaged profile is tabulated against every filed ordinate.

The independent explicit tiling gives a 1024-placement mean 35.711428 kg, sampled range 12.079624–113.564057 kg, and node/bay witnesses above. The owner used 200 placements without their coordinates or random seed in the packet. Its 5–171 kg placement envelope is not independently established. Both accounts scale cubically with radius, but this scaling does not validate their R10 coefficient. Use the full frame and a sagged-bay experiment to settle the load; neither surrogate licenses an R10 float.

The owner’s R10 bay-up arithmetic is 39.020593+171.423902=210.444496 kg versus 156.526706 kg total water capacity. That arithmetic is correct conditional on its pond input. Merely replacing it by the independent surrogate would leave a margin of only about 0.41 kg in that example; such a tiny unqualified difference must not be treated as flight clearance. Under the upper rain scenario both the independent node and bay witnesses exceed the capacity.

## Drying

The 76 heat/mass-transfer cases reproduce with air density 1.2 kg/m³, cp=1005 J/kg/K, vapor gas constant 461.5, Le=0.845, Magnus saturation, and 36×72 midpoint angular samples. The printed mean is normalized; the hull integral retains the midpoint sine weights. RETAIN interpolates clipped positive condensation on the coarse polar grid, uses mirror optics for all finishes, and adds all deposition over the top 14° for P3. Those conventions explain the final numerical agreement.

At R10 the mirror’s fair-midday potential is about 34.46–216.93 kg/h. M/E gives 0.16262–1.02381 h, but local integration leaves 11.7071–13.5622 kg at those respective times. A 0.5° calculation gives 99% removal after 0.31031–5.34571 h. The last trace of polar water is grid-sensitive, so no universal complete-drying time is claimed. Under held fair-morning sphere convection, about 36.545% of area condenses; a positive mean does not ensure complete drying. Weather variation and runoff are still omitted.

The pond time range reproduces as approximately 64.52–216.11 h (node) and 138.60–464.25 h (bay), using filed volumes and initial wetted areas with top-point paint flux. It is an initial-area equivalent, not full drying. As an illustrative alternative, the independent geometry with constant top-point flux would require 127–426 h for node-up and 427–1430 h for bay-up from maximum vertical depth. Actual liquid-water optics, weather and changing exposure remain unresolved.

## Disposition

Retain 0.1 kg/m² as a provisional design assumption, with the owner’s retention qualification carried forward. Correct the coating bill and drying labels. Keep P3’s pond orientation and tilt-drain claims open until the actual bay geometry and handling path are evaluated. The full-size weighing and logged drying experiments remain the right grounding measurements.

12 new NFI rows plus all 12 owner rows are in NFI.json; the pinned 052/053/050 registers are inherited. No objection stops the completed check. One report is filed to sciences, cc co, xo and admiral-robotics-review-v2; no out-of-band seat contact.

## Evidence and reproducibility

SOURCE-AUDIT.md provides primary-source checks. METHOD.md records the independent numerical choices. INPUT-PINS.json, SOURCE-PINS.json, execution receipts and MANIFEST.json carry hashes. Owner/predecessor executable paths are listed only as exclusions; none was read, copied, hashed, imported or run. Scientific work used admitted one-core, 1 GiB jobs. An early missing R20 thermal table and a diagnostic JSON-print type error were corrected; their receipts remain. Early arithmetic differences were resolved as documented density, angular-grid, clipping, cure and joining conventions.

Validation: 98 checks, 0 unexplained validation failures. Physical/model discrepancies are explicit, not suppressed.
