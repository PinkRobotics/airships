# MAINLINE-002 strength card — ESTIMATE_PENDING_UNA

Unit vacuum-mainline002-strength-owner1200-1019. This estimate is pending its own Una admission. It does not add a map point. MAINLINE-001 stays the admitted map point at 2026-10-19T19:47:15.465741-07:00. Its artifacts were read and not edited.

Case: evacuated spheres, external radius 10 m, 500 m ISA air. Pressure 95460.8379139 Pa. Density 1.16726833075 kg/m3. Lift mass 4889.44215019 kg. Internal pressure 0.

Aluminum strength uses 276 MPa, the AA typical tensile yield on the ASM MatWeb 6061-T6 sheet. That sheet says AA typical values are not for design. No compressive yield was retrieved, so the value is transferred to compression by owner assumption. Film allowable is a separate limit.

Collapse pressure for a row is the least of the stated limits. Stiffness and strength factors are separate multipliers on their own properties. A factor above one is the multiplier that brings that limit up to the external pressure with the other limits held fixed. It is not an all-mode promise.

## P1 — simple_shell — baseline

sphere R=10.0 m, t=0.0007 m, p_int=0

Masses in kilograms: shell 2375.04404611, joints 237.504404611, systems_payload 200, residual_gas 0. Total 2812.54845073. Float margin 0.424771095693.

Limits: knocked_down_buckling 82.5945600261 Pa, aluminum_yield 38640 Pa. Governing knocked_down_buckling. Collapse 82.5945600261 Pa. Crush safety factor 0.000865219307006.

knocked_down_buckling: property Young_modulus_of_6061-T6, factor 1155.77633544. Held fixed: t, R, nu, kd, sigma, masses. Scaling: p_stiff = kd*2*(t/R)^2/sqrt(3*(1-nu^2))*E.
aluminum_yield: property transferred_aluminum_tensile_yield, factor 2.47051857955. Held fixed: t, R, E, kd. Scaling: p_yield = 2*sigma*t/R.

If only stiffness is raised to the external pressure, the remaining modeled safety factor is 0.404773316937.

## P2 — sandwich — baseline

sphere R=10.0 m, tf=0.0002 m, core=0.1 m, p_int=0

Masses in kilograms: faces 1357.16802635, core 2010.6192983, joints 168.389366232, systems_payload 100, residual_gas 0. Total 3636.17669088. Float margin 0.256320745969.

Limits: knocked_down_buckling 11701.5583953 Pa, aluminum_yield 22080 Pa. Governing knocked_down_buckling. Collapse 11701.5583953 Pa. Crush safety factor 0.122579674043.

knocked_down_buckling: property Young_modulus_of_6061-T6_faces, factor 8.15795936651. Held fixed: tf, d, R, nu, kd, sigma; shear omitted. Scaling: p_stiff = kd*4*tf*d/(R^2*sqrt(1-nu^2))*E.
aluminum_yield: property transferred_aluminum_tensile_yield, factor 4.32340751422. Held fixed: tf, R, E, kd, core. Scaling: p_yield = 4*sigma*tf/R.

If only stiffness is raised to the external pressure, the remaining modeled safety factor is 0.23129903825.

## P3 — frame_membrane — baseline

sphere R=10.0 m, s=1.0 m, ro=0.02 m, tw=0.001 m, film=8e-05 m, p_int=0

Masses in kilograms: frame 1440.05384446, film 97.5150359674, nodes 29.0607898277, systems_payload 50, residual_gas 0. Total 1616.62967026. Float margin 0.669363166472.

Limits: pinned_euler 3170.21055887 Pa, aluminum_yield 6763.22066465 Pa, film_membrane 240000 Pa. Governing pinned_euler. Collapse 3170.21055887 Pa. Crush safety factor 0.0332095404582.

pinned_euler: property Young_modulus_of_6061-T6_frame, factor 30.1118288963. Held fixed: I, R, s, A, film, sigma. Scaling: p_euler = 2*pi^2*E*I/(R*s^3).
aluminum_yield: property transferred_aluminum_tensile_yield, factor 14.1147010644. Held fixed: A, R, s, E, I. Scaling: p_yield = 2*sigma*A/(R*s).
film_membrane: property film_tensile_allowable, factor 0.397753491308. Held fixed: t_film, s; not an aluminum yield. Scaling: p_film = 2*sigma_film*t_film/s.

If only stiffness is raised to the external pressure, the remaining modeled safety factor is 0.0708481175364.

## P1-A — simple_shell — float_margin_allocation

sphere R=10.0 m, t=0.0012564779436796986 m, p_int=0

Masses in kilograms: shell 4263.12922744, joints 426.312922744, systems_payload 200, residual_gas 0. Total 4889.44215019. Float margin 1.8601195675e-16.

Limits: knocked_down_buckling 266.112394467 Pa, aluminum_yield 69357.5824911 Pa. Governing knocked_down_buckling. Collapse 266.112394467 Pa. Crush safety factor 0.00278766036714.

knocked_down_buckling: property Young_modulus_of_6061-T6, factor 358.723756949. Held fixed: t, R, nu, kd, sigma, masses. Scaling: p_stiff = kd*2*(t/R)^2/sqrt(3*(1-nu^2))*E.
aluminum_yield: property transferred_aluminum_tensile_yield, factor 1.37635763078. Held fixed: t, R, E, kd. Scaling: p_yield = 2*sigma*t/R.

If only stiffness is raised to the external pressure, the remaining modeled safety factor is 0.726555349888.

## P2-A — sandwich — float_margin_allocation

sphere R=10.0 m, tf=0.0003758936444928841 m, core=0.1 m, p_int=0

Masses in kilograms: faces 2550.75417807, core 2010.6192983, joints 228.068673818, systems_payload 100, residual_gas 0. Total 4889.44215019. Float margin 0.

Limits: knocked_down_buckling 22031.3137183 Pa, aluminum_yield 41498.658352 Pa. Governing knocked_down_buckling. Collapse 22031.3137183 Pa. Crush safety factor 0.23078902511.

knocked_down_buckling: property Young_modulus_of_6061-T6_faces, factor 4.33296167148. Held fixed: tf, d, R, nu, kd, sigma; shear omitted. Scaling: p_stiff = kd*4*tf*d/(R^2*sqrt(1-nu^2))*E.
aluminum_yield: property transferred_aluminum_tensile_yield, factor 2.30033552179. Held fixed: tf, R, E, kd, core. Scaling: p_yield = 4*sigma*tf/R.

If only stiffness is raised to the external pressure, the remaining modeled safety factor is 0.434719192277.

## P3-A — frame_membrane — float_margin_allocation

sphere R=10.0 m, s=1.0 m, ro=0.02 m, tw=0.0034965263377450123 m, film=8e-05 m, p_int=0

Masses in kilograms: frame 4712.86632439, film 97.5150359674, nodes 29.0607898277, systems_payload 50, residual_gas 0. Total 4889.44215019. Float margin 3.720239135e-16.

Limits: pinned_euler 9166.73569578 Pa, aluminum_yield 22134.0021676 Pa, film_membrane 240000 Pa. Governing pinned_euler. Collapse 9166.73569578 Pa. Crush safety factor 0.0960261390545.

pinned_euler: property Young_modulus_of_6061-T6_frame, factor 10.4138311698. Held fixed: I, R, s, A, film, sigma. Scaling: p_euler = 2*pi^2*E*I/(R*s^3).
aluminum_yield: property transferred_aluminum_tensile_yield, factor 4.312859337. Held fixed: A, R, s, E, I. Scaling: p_yield = 2*sigma*A/(R*s).
film_membrane: property film_tensile_allowable, factor 0.397753491308. Held fixed: t_film, s; not an aluminum yield. Scaling: p_film = 2*sigma_film*t_film/s.

If only stiffness is raised to the external pressure, the remaining modeled safety factor is 0.231864737953.

Alternatives P1-A, P2-A and P3-A each spend the baseline float margin on one thickness. Residual margin is numerical zero by that rule. They are not an optimum.

Safety factors below one, and factors above one, are directions. Needs-further-investigation rows are in NFI.json. Core shear, knockdown curve, crippling and compression-yield measurement remain open.
