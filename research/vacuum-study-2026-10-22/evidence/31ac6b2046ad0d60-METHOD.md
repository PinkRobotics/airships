# MAINLINE-047 method and limits

This is a QUESTIONABLE/PROJECTION calculation of the specified P2 point, not a qualified pressure hull. The reported acceptance screen is the smaller of first face yield and the last converged static pressure. Numerical nonconvergence is retained as an endpoint, not renamed as a measured collapse load.

The main geometry has outer radius 10,000 mm, two 0.794624066985892 mm Be faces and a 23.23721790601544 mm CR-III core. The 037b fix uses the same faces with a 30.34139731914874:1 scarf and the 200 °F AF 163-2U cure. The scarf, film, cells, patches, support system and core seams are not resolved by the continuum model.

The brief explicitly authorizes 029 code reuse. `inputs/rpt-1228-mainline029-crimp-gamma-fe-1020/axisymmetric.py` preserves that source. `axisymmetric.py` adds the current point, plastic faces, both-face integration-point output, and explicit yield/hardening parameters. The full sphere uses shared-node quadratic CAX8 elements with full integration. Only axis radial displacement and one south-pole axial translation are restrained. Every layer receives the same stress-free inward radial offset:

`d(theta) = a exp[-(R theta / w)^2]`.

The core remains elastic and orthotropic. Its radial modulus is 103.4213594 MPa; transverse shear moduli are 103.4213594 and 46.8843496 MPa. W and L cases interchange the meridian and hoop shear moduli. Unmeasured in-plane moduli are regularized at E = 0.01 MPa and G = 0.005 MPa, with zero core Poisson ratios. The two orientations are axisymmetric surrogates, not rigorous bounds on a panelized three-dimensional core.

Faces use E = 290 GPa and nu = 0.0768; nu = 0.03 and 0.33 are sensitivities. NASA CR-194164 Table 2 reports 0.0768 for a thicker cross-rolled sheet. It does not establish isotropy or the finished gauge's elastic-plastic law. The 255, 300 and 345 MPa cases are assumed compressive-yield sensitivities. The 036 evidence record distinguishes the 345 MPa SR-200 tensile minimum from the missing finished-sheet compressive minimum.

CalculiX `*PLASTIC` with `NLGEOM` uses finite-strain isotropic J2 plasticity and a hyperelastic elastic response. It therefore changes the pre-yield finite-strain law from 029's StVK model. Constant stress versus plastic strain defines the ideal perfectly plastic cases. Both faces output Cauchy stress and equivalent plastic strain at integration points. These choices follow the [CalculiX 2.21 manual](https://www.dhondt.de/ccx_2.21.pdf), printed pp. 253, 258–259, 488 and 563–564. High-yield and elastic controls distinguish the constitutive change from yielding; a native displacement-controlled coupon checks the plastic plateau.

First yield is bracketed between the last output with every face integration point at PEEQ ≤ 1e-10 and the first with any point above it. An estimate from the last two elastic stress points is separately labeled; it is not substituted for a rigorous bracket. Exact target-load checks and finer meshes resolve acceptance boundaries. Each numerical endpoint is the last converged monotonic follower-pressure increment. Neither arc-length postbuckling nor unloading was performed. No plastic redistribution credit is allowed in the requested first-yield acceptance screen.

The fine target-load controls initially used 21 equal pressure increments, landing on service and 1.05 service. A five-increment piecewise ramp was then checked on the same a = 1 mm, w = 347.153 mm, 512-angular/2-face/6-core mesh: target stresses changed by at most 0.00020 MPa. New elastic boundary runs use this shorter ramp, with service at pseudo-time 0.8 and 1.05 service at 1.0. Each MODEL.json records its actual pressure schedule; collection maps pseudo-time to that schedule. Completed 21-increment runs remain intact and are reused. Actual 345 MPa boundary confirmations use their separate linear ramps. TARGET-RAMP-CHECK.json retains the comparison.

Automatic cutbacks can skip the intermediate service-pressure knot. EXACT-TARGET-AUDIT.json checks all final boundary edges. An affected group is recalculated using separate service-pressure cap runs wherever necessary, so no final pass/fail edge relies on stress interpolation between pressure increments. The initial group records and all native histories remain preserved.

The inherited deck requests a minimum time increment of 1e-7. CalculiX warns that it raises this to 1e-6 of the unit ramp. The native effective minimum is therefore 0.00018 kPa on the 180 kPa ramp. This is a numerical stepping setting, not a claim of collapse-pressure accuracy. First-yield brackets are determined by the actual converged output increments.

Numerical endpoints retain either the native minimum-increment diagnostic or a maximum-cutbacks diagnostic. Two broad-footprint sweeps stopped at the cutback limit after observed first yield; their last converged pressures and native histories are retained without calling them successful collapse solves. NUMERICAL-ENDPOINT-STOPS.json and ALL-NATIVE-RUNS.csv identify each stop. These algorithmic limits are part of the endpoint uncertainty.

The Gaussian widths are 332.2164186 mm (029's old 021), 401.8559050 mm (old 021b), and 347.1529189 mm (current 015-style classical length). The last is

`w = sqrt(R t_eq) / [12 (1 - nu^2)]^(1/4)`, with `t_eq = sqrt(3) (tc + tf)`.

This length is approximately the inverse classical buckling wavenumber, not a full wavelength. Retaining the individual-face bending term gives 347.1845439 mm and a full wavelength of 2181.424825 mm. The broad-dimple sensitivity uses that full wavelength as its Gaussian width.

For comparison with the corrected 015b record, one dimple's RMS about the prescribed sphere is computed by integrating its squared radial offset over the sphere. Its small-patch approximation is `a w / (sqrt(8) R)`. A global RMS tolerance alone does not control the maximum defect at a dangerous wavelength. Multiple dimples, a best-fit sphere, panel RMS and peak core-to-face fit are different metrics.

037b adds 3.41022257 MPa of cold face compression at this geometry. A separate strength-debit screen uses 345 − 3.41022257 = 341.58977743 MPa. The von Mises norm triangle inequality makes this a conservative local stress screen for the assumed residual stress magnitude. It is not a thermal prestress simulation: initial-stress stiffness, local edge transfer, adhesive relaxation and residual deformation remain unmodeled.

The calibration section preserves the unadjusted model and conditional endpoint reductions. Applying an inherited benchmark ratio to the endpoint does not validate the plastic law or establish that the same ratio applies to first yield. The 029 benchmark used a small clamped steel/PVC hemisphere with different core behavior, plasticity, contact-generated defects and an arc-length solution. Its bias cannot be promoted to a measured Be-sphere correction.

All native solver runs pass through `run_job.py` and simjob. Static multithreading is used only after a matched one/four-core check; eigen runs use one core. A run list executes serially. Native decks, load histories, diagnostics, timing and compressed integration-point data are retained. `NATIVE-DAT.json` records each uncompressed data hash. Failed load-control solves remain visible.

The later standing order `ord-admiral-rr2-mainline047-simjob-retry-standing-1020` explicitly makes simjob exit 75 a wait condition. Refused launches are preserved, and unchanged commands/resources are retried at least 60 seconds apart through simjob. RETRY-STANDING-ORDER.json and RETRY-POLICY.json pin that authority. No native result is inferred from a refused launch.
