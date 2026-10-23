**MAINLINE-038 — calculation and interpretation rules. QUESTIONABLE / PROJECTION.**

This is a proposed physical test program. There are no new measurements, supplier quotes, FE solves, qualified allowables or installed-hull safety factors. `prepare_inputs.py` verifies filed bytes and selects reference data; `calculate.py` performs scalar arithmetic. `validate.py` independently checks reference equations, similarity, force and mass accounting. OUTCOMES.csv and SHELL-SCALING.csv contain the unrounded calculations.

**Frozen reference choices.** R=10 m, p=95,460.8379139 Pa, lift=4,889.44215019 kg. Current P2 is the seam-enforced AF015/scarf point in 028b's PROPERTY-CHECKS.json, using E=290 GPa, scalar ν=0.0752, not its earlier ν=0.33 RESULTS file. Faces are 0.794624067 mm, core 23.237217906 mm, Vc=0.953213853; required γ=0.564163567, wrinkle coefficient Q=0.434627854. Its modeled seven-mode minimum is unity, with global buckling, wrinkling and scarf mean shear at unity simultaneously. Installed-hull SF is unknown.

The 021b comparison uses ν=0.33, faces 0.691747999 mm and core 30.118230885 mm, γ=0.468228567, Q=0.609201444. Its different joining bill and imperfection inversion remain historical reference conditions. Do not transplant its 2.34×/1.85× factors into current 028b.

The frozen P3 sensitivity reference is 022c, equilateral, cap-sag, 019 reserve: s=6.15 m, outer radius 165.569277 mm, wall 1.576494 mm, member arc length 6.251292 m, film 0.282331413 mm. The later 022d filing supersedes its optimum; P3-LATEST.md and RESULTS.json/P3_022d carry the current test targets. Both Zylon plies are charged, with effective total-gauge stress 1.74 GPa corresponding to 3.48 GPa per directional ply. All margins remain conditional. 026's physical frame has 362 joints and 1080 arcs near s=2.04 m; it does not supply a pressure factor for either newer topology.

**P2 equations and test normalization.**

```
h = tf + tc
sigma_demand = p R / (4 tf)                    # per skin
sigma0 = E h / [R sqrt(1 - nu²)]
sigma_crimp = h² Gc / (2 tf tc)
Vc = sigma0 / sigma_crimp
Kc = 1 - Vc/4  (Vc <= 2);  Kc = 1/Vc otherwise
p_ref = 4 Kc sigma0 tf/R
gamma_eff = measured collapse differential pressure / p_ref
SF_global = gamma_eff/gamma_required           # same geometry/properties
```

Report both `p_collapse/p_ref` and `p_collapse/p_perfect_FE` with the denominators in Pa. Neither is automatically `p_collapse/p_crimp`; the 029 brief's shorthand must not silently change the gamma convention. At the historical/current references, p_ref is 203.876578/169.207733 kPa. Collapse caused by seam opening, wrinkling or plasticity is a system failure; it cannot be labeled a measurement of the isolated global gamma.

The carried wrinkle equation is

```
sigma_wr,biax = b Q sqrt(E Ec tf/tc)
b³ + b - 1 = 0, b = 0.6823278038...
```

The scalar b is itself an inherited biaxial model. A uniaxial C364 result gives `Q_uni = sigma_wr,uni / sqrt(E Ec tf/tc)` only when the failure is identified as wrinkling; it does not measure b. A custom equal-biaxial panel is the follow-on. The current equal-biaxial demand is 300.333 MPa; if b applies, required uniaxial wrinkle onset is about 440.16 MPa. Face yielding may occur first. A censored result must be recorded as censored, not fitted as a wrinkle coefficient. Core Ec and Gc are measured independently with the actual cure and density; retain both honeycomb orientations.

At unchanged geometry, replacing one capacity multiplies that mode's SF by capacity ratio. All other modes stay fixed. Tables cap the corresponding seven-screen P2 minimum at one because other baseline modes already bind. Improved γ alone does not create payload margin. If thickness, density, core, modulus, joints, sag or pressure changes, re-run the design solver; do not multiply these ratios as though independent.

**Mass and reserve accounting.** Physical joining is 215.742080 kg; the embedded 5% allowance is 208.120056 kg, so 7.622024 kg is already charged as excess. Count `max(0.05*S, measured_joining)`, never add both the whole measured joining mass and the allowance. Unused allowance is not automatically a payload credit.

Fit component data from weighed before/after parts to

```
M_join = A*b_two_interfaces + L_seam*c_both_skins + N_crossings*m_crossing
         + M_ports + M_process_repairs
```

Use one-skin hull area A=1256.637061 m², and explicitly define whether a film mass is per interface. The current physical coincident seam length is 2841.518544 m. An extra 1 g/m² on each of two interfaces costs 2.513274 kg; an extra 1 g/m of completed seam costs 2.841519 kg. A 5 g/m² primer on each interface costs 12.566371 kg. Doubling the 0.015 lb/ft² core-bond film adds 184.063186 kg before scarf-film changes. These are losses of current mass closure, not a precomputed SF penalty.

**Shell similarity and the meaning of “smallest.”** For the same materials, scaling R, tf, tc, cell size, all bond layers and defect lengths by λ preserves Vc, R/tc, tf/tc, cell/tf, stress and predicted collapse pressure. Forces scale λ²; mass and collapse energy scale λ³. A maximum dent alone is insufficient: match δ/[sqrt(3)h], dent angular width, mode shape, spatial spectrum, seams, load introduction and core directions.

The 021b inversion gives δ/[sqrt(3)h]=0.858613599 and δ=45.819441 mm at R10. Its 46 mm value is a localized dimple amplitude, not RMS manufacturing error. The current 028b geometry is also tabulated with that *imposed comparison ratio*; this is not evidence that it has the same γ-versus-defect map.

There is no mathematical minimum radius. Our explicitly assumed fabrication floors, 25 μm faces and 1 mm core, give

```
R_min = 10 m * max(25 μm/tf_R10, 1 mm/tc_R10)
```

Hence 0.361403 m for 021b and 0.430344 m for 028b. These are conditional engineering lower bounds, not supplier capabilities. Choose R=0.5 m (1 m diameter) as the first custom surrogate. It requires either scaled cellular material or a continuous foam surrogate whose measured shear modulus is adjusted to the target. A continuous foam removes honeycomb cell failure from the experiment and can calibrate only the corresponding homogenized model.

For an elastic aluminum surrogate with nominal E*=69 GPa and ν*=0.33, retain the geometry ratios and set

```
a = (E*/E) sqrt(1-nu²)/sqrt(1-nu*²)
Gc* = a Gc
p* = a p
```

This exactly matches Vc, R/tc and the chosen imperfection ratio. It does not also match orthotropy, Poisson ratio, face strength, local wrinkling, density, bond microstructure or full-hull mass. Measure those quantities and reproduce them in a separate as-built FE model. The E* value is a planning nominal, not a tested coupon modulus. The actual core batch must meet its G target; otherwise adjust the design and recompute the dimensionless groups before fabrication.

At R=0.5 m the old/current variants require tf=34.5874/39.7312 μm, tc=1.505912/1.161861 mm and Gc*=11.15524/11.78377 MPa. Their scaled design differentials are 22.71310/23.99284 kPa. The old/current face stresses at γ=1 are approximately 175/134 MPa: foil temper must survive that range if the objective is the complete elastic curve. A weak annealed foil that yields earlier cannot measure global elastic buckling. Verify compression, bonding and forming first.

Full cellular similarity would need 0.47625 mm cells at R=0.5 m. Keeping the 9.525 mm cells gives same-Be dimpling screens only 0.01244/0.01690 at the geometrically scaled faces. That experiment would test a different failure problem. The 0.508 mm minimum catalog SR-200 gauge reported in 036 gives face-only similarity lower bounds R≈7.344/6.393 m, before any other manufacturing restriction. Custom thinner foil is a different, unqualified product/process. No commercially established small actual-Be replica is identified.

**What open-air evacuation can establish.** At ambient 101.325 kPa, even perfect internal vacuum limits Δp to 101.325 kPa, only 1.06143 times the R10 design differential. At the design ambient pressure, it reaches design load only; residual internal pressure reduces that further. The old/current Be reference gamma ceilings are 0.496992/0.598820. Thus the old full γ≈0.554 cannot be measured to collapse in open air, whereas the current full γ≈0.581 may fit narrowly at sea-level pressure. Survival is a lower bound, not an observed collapse point or a statistical proof margin.

For the Al surrogate, γ=1 references are only 48.50857/42.52816 kPa; atmospheric evacuation can span that elastic range if material and other failure modes permit. This validates a scaled mechanical experiment, not buoyancy or the actual Be hull. A laboratory external-pressure vessel is required for substantial overload of actual-material similarity specimens. Pressure must be measured as a differential. A water bath's hydrostatic gradient across a 1 m article is about 9.8 kPa, material compared with the 24 kPa surrogate load; model it or use a uniform-pressure facility.

**P3 parameter transfer.** The equilateral force is `N=pRs/(2sqrt(3))`, giving N=1.694766 MN and mean compression 1.038318 GPa at the current point. The inherited Perry estimate uses the exact annular A,I, `sigma_E = pi² E I/(A L²)`, `eta=(L/1000)ro/(I/A)` and the lower root of `sigma²-[Fc+(1+eta)sigma_E]sigma+Fc*sigma_E=0`. It reproduces 022c's 1.299373 at Fc=3.9 GPa. This scalar estimate does not capture full component ceramic statistics, contacts or the new discrete loading.

Film stress from the frozen 022c cap approximation is `p*s/(2t)=1.039707... GPa`; its 1.5 GPa assumption gives SF=1.442714. For 022d Zylon, t is total two-ply thickness in this expression and the directional-ply stress is twice the total-gauge effective stress. Actual film tests must use measured principal curvatures and tension, not assume every triangular panel is a spherical cap. Added barrier, resin and seams are weighed; altered sag changes displaced volume.

Joint stiffness is reported as `beta_theta=Ktheta*L/(E I)` for each bending axis and member roll. Here EI/L=1.453409 MN m/rad. No justified minimum beta is available: a discrete-frame sensitivity must define it. At geometric scale λ with unchanged elastic material, N scales λ² and Ktheta scales λ³; simply using miniature commercial rigid fittings generally breaks that similarity.

For R10→R20 with all geometric lengths doubled and pressure unchanged, stresses and dimensionless modes stay constant; areas, volumes and forces grow by 4,8,4. At fixed commercial panel dimensions seam length grows roughly 4; when panels also scale, seam length grows roughly 2. Adhesive thickness held at its process gauge breaks cubic mass scaling. Fixed-span P3 with unchanged s also breaks homothety and increases member count. State which design is being transferred. The filed 027 R20 point is a *different re-optimized design*, with p=96.415 kPa and a 0.9 joint-efficiency rule; 036 gives its separate 376–382 MPa material requirement.

**Vacuum test reduction.** Use a calibrated chamber volume and absolute pressure, temperature and volume-deformation records:

```
Q_ref(t) = T_ref * d[p(t) V(t)/T(t)]/dt
mass_i(t) = M_i p_i(t) V(t)/(R_universal T(t))
```

Subtract the blank fixture's signal; retain the article's outgassing, absorbed water and real leaks in its service gas load. Separately identify face-area, seam-length, crossing and port contributions using blanks and paired samples. For constant dry-air Q at T=284.9 K, `dm/dt=Q/(Rd*T)`. The filed 019 limit is 46.280720 Pa m³/s, corresponding to 1% lift gas in 24 h; a tiny 0.00105% density-constant difference with the mass/Rd reconstruction is disclosed in RESULTS.json.

The area-only and seam-only upper bounds are respectively 0.0368290 Pa m³/s/m² and 0.0162873 Pa m³/s/m. They cannot both receive the entire gas allowance. A 0.36 m² panel's area-only quota is 0.01325845 Pa m³/s; in a 10 L chamber it causes 1.325845 Pa/s. Actual fixture pressure range and area must keep the pressure difference representative, or measure throughput with a calibrated pumping arrangement. For helium, report test gas and conditions; do not equate helium throughput to service-air mass without a flow/permeation model.

For a sealed system, use `time=(gas_allowance-initial_gas)/measured_service_mass_rate` only if the rate is effectively constant over that interval. Projected pump mass is not derivable from a helium number: measure the candidate pump's installed speed, power, gas mix and conductance, then price power and hardware against the 100 kg system floor. Long-term creep, ageing and wet service need additional durations; a 24–72 h screen is not a mission-life qualification.

034 adds a separate hot-pressure and phase-accounting requirement. Its source gas inventories are not automatically those of 028b/022d. Species pressure is `sum(m_i R_universal T/(M_i V))`; water and air therefore cannot share a single mass-to-pressure conversion. Outgassing contributes to free-gas pressure but does not add total vehicle mass already charged as solid/absorbed material. The illustrative constant-ingress table in this card is external dry air only. Inspect all core/bore evacuation paths; preserve the mass and pressure contribution of initially trapped air. Maintain separate net-added-mass, free-gas and hot-pressure ledgers.

**Evidence thresholds.** A measured lower uncertainty bound must clear demand for the tested failure mode. Target instrument/geometry uncertainty below 2% of that mode's margin; where the nominal margin is zero, report a confidence interval and do not claim a robust pass. Three to six screening specimens expose large errors; they do not make a population allowable. For perspective only, even zero failures in identical independent trials requires 2,995 trials to bound per-trial failure probability below 0.001 with 95% confidence. Real hull size, flaw population and duration require their own statistical model.
