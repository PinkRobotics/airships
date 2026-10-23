# CHECK MAINLINE-021 — arithmetic reproduced; source gaps remain

Order ord-admiral-rr2-check021-codex-1020. Started 2026-10-20T00:35:27-07:00; completed 2026-10-20T01:00:13-07:00. QUESTIONABLE, with gamma interpolation PROJECTION. No certification.

The original 0.843448-mm Be / CR-III 5056 3/8-1.0 point reproduces. At gamma .579149448960 and wrinkle coefficient .362641644309, the six SFs are 1, 1.000183118954, 2.154663914751, 5.055822063463, 1 and 9.423147125824. Faces, core, joints, systems and the five-percent unused-lift allowance close the 4889.442150187-kg budget. Minimum face-strength demand is 282.948186824 MPa; 283 MPa is the retained available input.

All eight subset outcomes reproduce on an independent 4000-step search. Boundary refinement retains gamma plus wrinkling as the least pair under E303/283 MPa/nu .33, reducing usage from .909899005721 to .908635413226. Full-set family mode scores at the filed geometries reproduce; their continuous optima improve slightly.

The material conclusions are conditional. Current S-200F and SR-200 datasheets give typical E=290 GPa. The main E290 sensitivity still floats with two optimisms; the gamma-only SR-200 claim does not survive E290. The guide's S-200F compression is about 255 MPa, not the inherited 283. The cited sheet tests have in-plane nu about .076, whereas the model carries .33. An explicitly limited isotropic sensitivity changes the preferred pair to wrinkling plus strength on aramid. Those observations are NFI rows, not stops.

Five NFI rows cover changed filing pins, modulus, Poisson ratio, strength/product form, and the scope of “strongest sourced Be.” RESULTS.json and float021.py no longer matched the original report's byte pins when checked; the original CARD and inputs did match and are snapshotted. No owner program was executed or imported. CHECK.md contains exact comparisons, formulas and 20 passing checks; SOURCE-AUDIT.md gives the primary source readings.

The report goes once to sciences, cc co, xo and admiral-robotics-review-v2. The next queue order is ord-admiral-rr2-check021b-after-021-codex-1020; begin that independent check after this filing.
