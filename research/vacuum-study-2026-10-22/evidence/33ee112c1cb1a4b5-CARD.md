# Estimates card — ESTIMATE_PENDING_UNA

Unit vacuum-mainline-estimates-owner3000-1019. Owner ref-2543c559b19ffce7dfdd. This is an estimate, not an admission and not a map point. Una has not checked it. H1 certification limits were not used.

## Case

Evacuated hull in air at 500 m. Temperature 284.9 K. External pressure 95460.8379139 Pa. Density 1.16726833075 kg/m3. All three points use external radius 10 m, displaced volume 4188.79020479 m3, lift-equivalent mass 4889.44215019 kg, and internal pressure 0. Float margin is (lift minus all stated mass) over lift. Crush safety factor is collapse pressure over this external pressure.

Sea-level 101325 Pa is not the primary case. Charter density 1.167 kg/m3 is a sensitivity only.

## Points

### P1 — simple_shell

Complete sphere, external radius 10 m, thickness 0.0007 m, p_int=0.

Equations: Zoelly p_cl=2*E*(t/R)^2/sqrt(3*(1-nu^2)); p_collapse=kd*p_cl. Identity 4/R^2*sqrt(D*S) checked.

Masses in kilograms: shell 2375.04404611, joints 237.504404611, systems_payload 200, residual_gas 0. Total 2812.54845073.

Float margin 0.424771095693. Collapse pressure 82.5945600261 Pa. Crush safety factor 0.000865219307006.

Safety factor is below one. Property to improve: Young_modulus_of_6061-T6. Factor 1155.77633544 on baseline E 68900000000. Held fixed: R, t, nu, knockdown, all masses, p_ext. Scaling: p_collapse = kd*2*(t/R)^2/sqrt(3*(1-nu^2))*E, linear in E. The factor equals collapse-pressure ratio over the reported safety factor because that model is linear in the named property. This is a direction, not a stop.

margin=(lift-all_mass)/lift. Margin is positive at the stated allowances. It falls if those allowances or densities rise.

### P2 — sandwich

Complete sphere, external radius 10 m, two faces 0.0002 m, core 0.10 m, p_int=0.

Equations: Owner extrapolation: D=E*tf*d^2/(2*(1-nu^2)), S=E*2*tf, p_cl=4/R^2*sqrt(D*S), p_collapse=kd*p_cl. d=core+tf. Core shear, wrinkling and core crush omitted.

Masses in kilograms: faces 1357.16802635, core 2010.6192983, joints 168.389366232, systems_payload 100, residual_gas 0. Total 3636.17669088.

Float margin 0.256320745969. Collapse pressure 11701.5583953 Pa. Crush safety factor 0.122579674043.

Safety factor is below one. Property to improve: Young_modulus_of_6061-T6_faces. Factor 8.15795936651 on baseline E 68900000000. Held fixed: R, tf, d, nu, knockdown, core, all masses, p_ext; shear omitted. Scaling: p_collapse = kd*4*tf*d/(R^2*sqrt(1-nu^2))*E, linear in E. The factor equals collapse-pressure ratio over the reported safety factor because that model is linear in the named property. This is a direction, not a stop.

margin=(lift-all_mass)/lift. Margin is positive at the stated allowances. It falls if those allowances or densities rise.

### P3 — frame_membrane

Complete sphere, external radius 10 m, spacing 1 m, tube 0.020 m outer by 0.001 m wall, film 80e-6 m, p_int=0.

Equations: Equilibrium N=p*R/2. Owner tributary: F=N*s. Pinned Euler p_euler=2*pi^2*E*I/(R*s^3). Film p_film=2*sigma*t_film/s. Collapse is the lesser. No extra knockdown.

Masses in kilograms: frame 1440.05384446, film 97.5150359674, nodes 29.0607898277, systems_payload 50, residual_gas 0. Total 1616.62967026.

Float margin 0.669363166472. Collapse pressure 3170.21055887 Pa. Crush safety factor 0.0332095404582.

Safety factor is below one. Property to improve: Young_modulus_of_6061-T6_frame. Factor 30.1118288963 on baseline E 68900000000. Held fixed: R, s, tube radii, film, knockdown not applied, nu unused. Scaling: p_euler = (2*pi^2*I/(R*s^3))*E, linear in E. The factor equals collapse-pressure ratio over the reported safety factor because that model is linear in the named property. This is a direction, not a stop.

margin=(lift-all_mass)/lift. Margin is positive at the stated allowances. It falls if those allowances or densities rise.

## Sensitivities

- S-RHO-P1. replace computed ISA density with charter 1.167 kg/m3. QUESTIONABLE historical charter density; pressure case unchanged. float_margin 0.42463883211.
- S-RHO-P2. replace computed ISA density with charter 1.167 kg/m3. QUESTIONABLE historical charter density; pressure case unchanged. float_margin 0.256149750245.
- S-RHO-P3. replace computed ISA density with charter 1.167 kg/m3. QUESTIONABLE historical charter density; pressure case unchanged. float_margin 0.669287142454.
- S-SL-P1. replace p_ext with 101325 Pa. NON_PRIMARY sea-level comparison. Not the ordered 500 m case. crush_SF 0.000815144929939.
- S-SL-P2. replace p_ext with 101325 Pa. NON_PRIMARY sea-level comparison. Not the ordered 500 m case. crush_SF 0.115485402372.
- S-SL-P3. replace p_ext with 101325 Pa. NON_PRIMARY sea-level comparison. Not the ordered 500 m case. crush_SF 0.0312875456094.
- S-P2-CORE-0.16m. P2 core thickness 0.10 m to 0.16 m; other P2 inputs fixed. QUESTIONABLE single alternate. Shear still omitted. float_margin -0.00274565036435. crush_SF 0.195980676463. collapse_pressure_Pa 18708.4795901. all_mass_kg 4902.86684881.

The 0.16 m core alternate still has crush safety factor below one, and its float margin is slightly negative. Thickening this sandwich toward a safety factor of one, with the knockdown held at 0.2, spends the float margin first.

## What is not claimed

No point is a certified floating non-crushing hull. The monocoque and sandwich pressures use knockdown 0.2. The sandwich formula omits core shear, so its safety factor is optimistic relative to shear and still below one. The frame model uses pinned Euler and an equal-triangle count. Every input is QUESTIONABLE. Needs-further-investigation rows are in NFI.json. Full input rows are in INPUTS.json.
