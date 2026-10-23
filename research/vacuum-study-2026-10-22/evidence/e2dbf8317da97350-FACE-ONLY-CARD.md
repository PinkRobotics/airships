# Historical face-only campaign — superseded for acceptance

This appendix preserves the E-in-plane = 0.01 MPa campaign and its sensitivities. Its amplitude boundaries omit core shear and do not establish admissibility of that core law. Use CARD.md and CORE-RESULTS.json for the final CHECK-029 fold. Run totals below include the full combined record.

# MAINLINE-047 — P2 dimple tolerance with plastic faces

**QUESTIONABLE / PROJECTION. No installed-hull qualification.**

At the held 028b point, the 255 and 300 MPa face-yield cases have **no admissible amplitude, including a perfect sphere**, under the requested pressure/first-yield screen. With the assumed 345 MPa law, the governing tested amplitude boundary is **1.209–1.227 mm at SF 1** and **0.738–0.756 mm at SF 1.05**. The passing value is the lower end of each interval; the upper end fails the first-yield screen. These are numerical brackets on the tested Gaussian branch, not physical uncertainty bounds.

The corresponding single-dimple RMS estimates about the prescribed sphere are **14.31 µm** and **8.78 µm**. This small global RMS is a consequence of one localized defect occupying little sphere area. It is not a generic RMS fabrication specification.

## Criterion and point held

The calculation requires `min(P_endpoint, P_first_yield) ≥ SF × 95.46083791 kPa`; SF 1.05 therefore requires 100.23387981 kPa. Endpoint means the last converged monotonic static pressure. No arc-length collapse load or measured failure pressure was obtained.

The main point has R_outer = 10 m, two 0.794624066985892 mm faces and a 23.23721790601544 mm core. Faces use E = 290 GPa and nu = 0.0768, with ideal finite-strain J2 plasticity at 255/300/345 MPa. Core radial modulus is 103.421 MPa; L/W transverse shear moduli are 103.421/46.884 MPa. Both face integration-point fields are checked. The 037b cure/scarf fix is carried as a 200 °F cure and 30.3414:1 scarf; seams and residual-stress stiffness are not resolved.

The 255/300/345 MPa values are assumed compression sensitivities. The 036 source audit found no matched finished-sheet compressive minimum; the 345 MPa SR-200 maker value is tensile. The scalar isotropic law and using an offset yield as a sharp onset are projections. The thicker-sheet nu basis is [NASA CR-194164, Table 2](https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf).

## Perfect-sphere limit

| Assumed yield (MPa) | First-yield native bracket, W (kPa) | Estimate (kPa) | Numerical endpoint, W (kPa) | SF 1 result |
|---:|---:|---:|---:|---|
| 255 | 80.10000–81.00000 | 80.96372 | 81.03884 | Fails even at a=0 |
| 300 | 94.95000–95.28750 | 95.26695 | 95.35486 | Fails even at a=0 |
| 345 | 109.51875–109.64531 | 109.57473 | 109.67515 | Passes this model screen |

The 300 MPa case is a small but explicit failure at the held geometry. Its entire first-yield bracket and numerical endpoint are below service pressure. No positive tolerance is assigned to either lower-strength case.

## Amplitude boundaries for the 345 MPa case

| Gaussian width (mm) | Meridian | SF 1 pass–fail (mm) | One-dimple RMS estimate (µm) | SF 1.05 pass–fail (mm) | RMS estimate (µm) |
|---:|:---:|---:|---:|---:|---:|
| 332.216 | W | 1.209–1.227  | 14.31 | 0.738–0.756  | 8.78 |
| 332.216 | L | 1.796–1.811  | 21.20 | 1.111–1.129  | 13.16 |
| 347.153 | W | 1.223–1.241  | 15.12 | 0.748–0.766  | 9.29 |
| 347.153 | L | 1.798–1.816  | 22.18 | 1.114–1.132  | 13.79 |
| 401.856 | W | 1.284–1.302  | 18.37 | 0.789–0.807  | 11.34 |
| 401.856 | L | 1.821–1.839  | 26.07 | 1.136–1.154  | 16.27 |
| 2181.425 | W | 21.127–21.217  | 1630.45 | 14.262–14.352  | 1101.25 |
| 2181.425 | L | 21.271–21.358  | 1640.96 | 14.299–14.389  | 1104.15 |

The 332 and 402 mm widths retain 029's two footprints. The current classical length is 347 mm, approximately the inverse buckling wavenumber; the full classical wavelength is 2181 mm and is checked separately as a broad Gaussian. The latter is not silently substituted for the narrow defect width. The result is limited to these tested footprints and meridian surrogates.

First yield generally precedes the numerical endpoint. The no-yield boundary uses a high-yield numerical control to evaluate the identical pre-yield constitutive branch at the exact target pressures. The control's 10,000 MPa threshold is not a proposed material strength. Actual 345 MPa runs confirm yield-free passing edges and plastic failing edges at the governing boundaries.

A geometric check helps explain the scale: the governing SF 1 dimple changes the initial pole curvature by about 22.1%. At that width the pole becomes locally concave above 5.52 mm. A small amplitude relative to the 10 m radius can therefore be a substantial local curvature error. This check explains the geometry; it is not an independent strength prediction.

The main amplitude sweeps' endpoints and first-yield brackets are in [SWEEP.csv](9dfb681cb4d897e5-SWEEP.csv). [ALL-NATIVE-RUNS.csv](9c8b5c29a3366ea9-ALL-NATIVE-RUNS.csv) additionally lists every auxiliary calculation, identifying load caps, yield not reached, and excluded controls. Pressure sweep figure [source link unavailable in this public projection] and tolerance figure [source link unavailable in this public projection] show the distinction. Extrapolations outside native PEEQ brackets are rejected and listed in RESULTS.json.

## What the inherited benchmark gap does

If the new model's endpoint is divided by **1.10**, while first-yield pressure is left unchanged, the smallest SF 1 boundary estimate is **0.521–0.539 mm** at width 401.856 mm/W (7.51 µm one-dimple RMS). At SF 1.05 the perfect sphere already fails that scenario. Transferring the larger **2.3146–2.4589×** imperfect-endpoint bias leaves no admissible amplitude even at SF 1.

CALIBRATION.json retains the unadjusted reading, the exact 029 linear factors 1.095667 and 1.097609, the rounded 1.10 scenario, and both imperfect factors. These reductions are conditional endpoint-transfer calculations, not calibrated predictions. Applying an elastic predecessor's error to a model that now includes plasticity may double-count part of the omitted-material effect.

The source benchmark is a small clamped steel/PVC hemisphere with nonlinear foam, a contact-generated defect and an arc-length solution. Its geometry and mechanisms differ substantially from this low-Vc Be/CR-III sphere. See the [EUCASS paper](https://www.eucass.eu/doi/EUCASS2023-367.pdf), the pinned 029 record, and NFI row 047-05.

## 037b cure correction

A separate local strength-debit sensitivity subtracts 3.41022257 MPa from the 345 MPa screen. It accounts conservatively for the stated residual stress magnitude through the von Mises norm inequality, but does not solve thermal deformation or geometric stiffness. It is evaluated at the nominal governing width/meridian, not presented as a new global optimization.

- At SF 1, width 332.216 mm/W: pass–fail 1.122–1.140 mm; single-dimple RMS estimate 13.30 µm.
- At SF 1.05, width 332.216 mm/W: pass–fail 0.657–0.675 mm; single-dimple RMS estimate 7.82 µm.

037b's small re-optimization has tf = 0.7946220286 mm and tc = 23.2319086293 mm. The exact-geometry control is retained beside the held-point control in RESULTS.json; the main campaign does not silently switch geometries.

## Comparison with 015b and 042

042 mapped the present P2 point to roughly 9.32–16.06 mm at a footprint near 0.36 m. The new governing SF 1 estimate is 1.219 mm, about 7.6–13.2 times smaller. This comparison adds a first-yield restriction and changes the numerical model; it is not an isolated calibration of the old knockdown formula.

The older 021/021b map amplitudes were about 11.8 and 45.8 mm. 015b corrected their paired single-Gaussian RMS values to about 0.1393 and 0.6544 mm. Pairing the amplitude from one footprint with the width from another is not repeated here.

Relevant 042 precedents remain different measurements:

- Rohr's gores departed contour about 1.27 mm after trimming and 3.81–5.08 mm after chemical milling; hand forming followed. Those deviations are comparable to or larger than the narrow-defect limits, but they are not measured Gaussian defects on this hull. [Primary report, PDF p.25](https://ntrs.nasa.gov/api/citations/19660014454/downloads/19660014454.pdf).
- The all-Be honeycomb panel report gives 0.0762 mm conformity to a cylindrical die after forming. That is encouraging at panel scale; it does not establish the shape of an assembled 20 m sphere. [Primary report, PDF p.86](https://ntrs.nasa.gov/api/citations/19730016169/downloads/19730016169.pdf).
- S-II's 0.254 mm figure is a core-to-face fit limit, not whole-shell peak/RMS accuracy. 042's 0.15 mm reflector-class peak is a three-sigma projection from RMS data. Treating either as the present hull's measured dimple spectrum would be unjustified.

For one Gaussian, RMS is approximately `a w / (sqrt(8) R)`; the filed results use the exact spherical-area integral. Multiple defects, a fitted sphere, reflector panel RMS, local waviness and core-to-face gaps need separate spatial definitions. A global RMS number alone cannot enforce this local amplitude bound.

## Numerical controls and unresolved work

319 native solver records are retained, including 2 excluded initial eigen controls. The failed controls returned SIGSEGV and supplied no factor; their pure-elastic replacements are separate records. Static one/four-core runs agree; eigen runs use one core. All heavy runs use simjob and own jobs execute serially.

Mesh controls vary angular resolution, pole grading, face layers and core layers. The constitutive controls compare the native plastic law's pre-yield response against StVK, a core in-plane regularization change, and a small hardening slope. Nu = 0.03 and 0.33 are tested at 0, 1 and 11.8 mm in both meridians with the 345 MPa law. Full tables and actual differences are in RESULTS.json; mesh brackets are not substituted for physical uncertainty.

At the target-load control (a = 1 mm, w = 347.153 mm), doubling the angular resolution from 512 to 1024 with two face layers changes the service-pressure maximum stress by 0.031 MPa; increasing to four face layers changes it by 0.139 MPa. The exact 037b re-optimized geometry changes it by 0.019 MPa. The adopted boundary mesh uses 512 angular elements, two elements through each face, six through the core, and pole grading 2.

The five-increment target ramp agrees with the 21-increment reference within 0.00020 MPa. Completed longer ramps are preserved, and each model records its own time-to-pressure mapping. Actual-yield confirmations use separate linear ramps.

Conditional endpoint-bias boundaries use 256 angular elements and one layer per face. At the governing passing point, the following controls measure sensitivity; their pressure differences are not an amplitude error bound:

| Endpoint control | Reference (kPa) | Checked (kPa) | Change |
|---|---:|---:|---:|
| endpoint_step | 105.06919 | 105.07113 | +0.0019% |
| endpoint_mesh | 105.06919 | 105.06992 | +0.0007% |

At a = 1 mm and w = 347.153 mm, the comparable 128-element angular meshes give:

| nu | Meridian | First-yield native bracket (kPa) | Numerical endpoint (kPa) |
|---:|:---:|---:|---:|
| 0.0300 | L | 100.800–104.400 | 105.275 |
| 0.0300 | W | 97.200–100.800 | 101.647 |
| 0.0768 | L | 100.800–104.400 | 105.010 |
| 0.0768 | W | 97.200–100.800 | 101.340 |
| 0.3300 | L | 97.200–100.800 | 103.971 |
| 0.3300 | W | 93.600–97.200 | 100.261 |

The inherited minimum step request of 1e-7 is raised by CalculiX to 1e-6 of the ramp, as recorded in NATIVE-WARNINGS.json. Load-control endpoints and coarse first-yield estimates are qualified accordingly. The plastic-law setup and output convention are documented in [METHOD.md](78898e4b60c74019-METHOD.md) and the [CalculiX manual](https://www.dhondt.de/ccx_2.21.pdf).

2 paths stop at the consecutive-cutback limit after observed first yield. All numerical stop diagnostics, including minimum-increment stops, remain in NUMERICAL-ENDPOINT-STOPS.json. Retaining their converged histories does not make them successful collapse solutions.

1892 custody, numerical and arithmetic checks pass; this does not validate the physical hull. Native solver elapsed time sums to 7914.0 s, with measured CPU time 24053.6 s and peak native RSS 626.5 MiB. Wall-clock start/end measurements are in RUN.json.

[NFI.json](e5f8a3dd183321bf-NFI.json) records 14 issues, including finished-sheet compression, orthotropy, core/bond behavior, continuation versus nonconvergence, thermal prestress, three-dimensional geometry, shape metrics and benchmark transfer. Installed-hull SF remains unknown.

The assigned work is complete. The brief names no successor; stop and file.
