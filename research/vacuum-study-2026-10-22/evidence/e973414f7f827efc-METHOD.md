# MAINLINE-040 common-account method

QUESTIONABLE material inputs; PROJECTION geometry, assembly, loads, mission and all numerical results. No installed-hull safety factor is assigned.

## Basis and scope

The fixed construction is 021b/028b's selected Hexcel CR-III 5056 3/8–1.0 honeycomb and two SR-200 Be faces. Filed 037b is incorporated: AF163-2U's 200°F cure and scarf ratio 30.34139731914874, with its compliant-core/free-edge model. This is a geometry optimization of that grade, not another search across the 47-core catalogue in 033. Radius is the nominal displaced-sphere radius; both face and core areas use its outer area. This conservatively overstates the inner face area. Exact mouldline, seams and manufacturing tolerances remain open. The completed earlier rigid-037 calculation is preserved in comparison-037/ and is superseded as the primary account.

Use p0 = 95,460.83791390515 Pa, T0 = 284.9 K, lift = 4,889.442150186961(R/10)^3 kg and scalar ν = .0768. Thus 033 supplies the pressure-floor and ν convention. The four p/ν combinations in BASIS-RECONCILIATION.json quantify the change from 028b's p0/.0752. With the new debits disabled and 033's climate terms restored, the independent implementation reproduces its four full-endpoint payloads within 0.001 kg.

Be density is 1,850 kg/m³; E ranges from 290 to 293.6 GPa with the coupled compression proxy 345 to 379.2 MPa. These are not certified compression allowables for the finished shell. Honeycomb properties are taken from the pinned 033 input. The primary account uses solid Al density 2,700 kg/m³ consistently for thermal conduction, pore volume and 037b's biaxial stiffness. This replaces 037's 2,640 kg/m³ conductivity input and agrees with 034/037b. It changes pore volume by less than 0.014%; the gross core density and mass stay unchanged.

The four optimism axes are γ, Q, the coupled E/compression tuple, and film weight. γ follows 033: baseline .2 below Vc=2, 1 at/above; favorable .2+.4 min(Vc,2). Q ranges .33–.82. Film ranges .030–.015 lb/ft² **per interface**, or .1464728291–.07323641455 kg/m². Intermediate film weights are mathematical design targets, not claims of available qualified products. The named 028b “two-factor endpoint” already assumes .015 film and the baseline face tuple; it is mask 11 in this explicit four-axis account.

For each subset, a common logarithmic usage ceiling u bounds its selected axes. First minimize the number of selected axes; then minimize u. Slack γ and Q are reduced at the final geometry in QUALIFICATION-AUDIT.json. An E increase also increases thermal stress, so an endpoint-only monotonicity claim would be invalid. The audit gives every otherwise excluded E-containing subset the largest elastic E and smallest thermal E simultaneously. Those deliberately favorable bounds still do not produce a lower-cardinality solution or rescue any failed primary account.

## Loads and constraints

With tf the thickness of each face, tc core thickness, h=tf+tc:

σp = pR/(4tf); σ0 = Eh/[R√(1−ν²)]; σcr = Gc h²/(2tf tc);
Vc=σ0/σcr; Kc=1−Vc/4 for Vc≤2, otherwise 1/Vc.

The six shell screens are γKcσ0/σp; Fcy/σd; σcr/σt; 2Fcrush/p;
βQ√(E Ec tf/tc)/σd; and E(tf/cell)²/[(1−ν²)σd], where β³+β=1.
Here σt=σp+absolute thermal gradient stress+absolute thermal pattern bending stress, and σd=σt+the balanced cure compression from 037b.
The global screen receives full wind pressure but no unsupported reduction for thermal curvature. Following the filed 037b model, balanced cure compression is excluded from global buckling and crimping. That mechanics assumption remains unqualified; it is not inferred from a higher global allowable.

The primary scarf screen is 10 MPa/[σd r/(1+r²)], r=30.34139731914874. The continuous-core field carries no mismatch interface shear in 037b's proposed model; a separate free-edge screen compares the calculated edge shear with the 25 psi minimum-average W strength. A cell-wall screen uses the doubled-ribbon single-wall stress and a 227.53 MPa 5052-H39 yield proxy transferred to 5056. Passing either does not establish the film's bond or peel strength. A separate sensitivity adds the free-edge shear to the scarf demand when their interaction is unresolved.

031's 100 m centre-altitude floor is used for its optimistic and both-weather envelopes. At R10 their headrooms are 55.340908918 and 441.770105446 kg; they scale with R³. Their required external-pressure multipliers are 1.036552962 and 1.022888808. ISA has zero weather debit and multiplier 1. The pressure design basis is p0×max(1.01, weather multiplier), **not** their product. It receives the wind pressure below. These climate terms replace 033's 500 m hot/humid loss terms; they are never charged twice. A 100 m centre floor is 100−R metres of bottom clearance above the datum, not a terrain-clearance mission.

Wind uses ISA density conservatively for ground/mooring loads. The 70 kn dynamic pressure is .5ρV². The gust case combines a 35 kn baseline with an aligned 35 ft/s increment: .5ρ(V+U)². The 290.634 Pa reported in 037 is the increment alone; 040 also includes the baseline steady dynamic pressure. Both full cases are saved. The larger 70 kn pressure governs the geometry optimization. The gust is not added again on top of 70 kn. Cp=1 applied uniformly is a conservative shell-pressure surrogate, not a resolved aerodynamic pressure field.

## Thermal factor and coating

037's thermal boundary conditions remain explicit: ambient 284.9 K, 970 W/m² solar input, 2 m/s convection, sky 275 K by day/260 K by night, outer α=.20/ε=.90 and inner ε=.20. The common-account core conduction coefficient is 130ρcore/2700 W/(m K). Face/core radiative and convective balances are solved to convergence.

The numerical implementation reproduces 037's 37-midpoint temperatures. Its uncorrected midpoint Legendre projection assigns curvature to a constant temperature field. 040 removes that constant component and uses 128-point Gauss-Legendre quadrature, degree 2–6 pattern terms and analytic derivatives. At the old R10 geometry the resolved day/night swing is about 31.118 K versus 30.493 K in 037, and the curvature-temperature amplitude is about 55.79 K versus 216.84 K. Thus this is a documented numerical correction, not a free reduction of the thermal load.

For each radius, a 241-point core-thickness table supplies gradient, swing and pattern curvature. All three are multiplied by 1.002; direct 256-point solves at the primary endpoints verify that this guard covers interpolation/quadrature differences. Thermal stress is EαBeΔT/[2(1−ν)]; pattern bending is E h κ/[2(1−ν²)]; shear lag is |αAl−αBe|ΔT√(E tf Gc/tc).

037b filed at 03:23:51−07:00 before closeout and therefore replaces the primary rigid-substrate screen. At every candidate geometry use the resolved cold/hot temperatures and Tstress-free=366.483333333 K (200°F). The worst mismatch strain is 1.002|αAl−αBe|max(|Tcure−Tcold|,|Tcure−Thot|). With Kbiax=.5 Efoil ρcore/ρfoil, Efoil=67 GPa and ρfoil=2700, the free-edge shear is mismatch×√(2Kbiax Gc). Balanced face compression is Kbiax(αAl−αBe)max(Tcure−Tcold,0)tc/(2tf), also with the 1.002 numerical guard. Doubled single-wall stress is 1.2 Efoil×mismatch. Minimum W shear is 25 psi, rather than the 35 psi typical value used in 037.

The source's +0.12 kg scarf cost is specific to its old R10 geometry. Here overlap, seam length, scarf adhesive and joining floor are recomputed throughout. No constant +0.12 kg is substituted at larger radii. No CTE-matched core or soft interlayer is adopted.

Actual stress-free temperature, core-field restraint, free-edge transfer and cure-to-service residual stress remain model assumptions. Source 037b's free-edge derivation and its global/crimp exclusion are author-derived, not qualified material data. The original 250°F cure fails the minimum free-edge screen in this model; a low-temperature mid-swing cure remains an explicitly unqualified sensitivity. The 031 weather choices alter buoyancy and pressure; the retained 037 thermal environment is not a validated combined weather/solar mission envelope.

Coating plus primer costs **an assumed 0.20 kg/m² on the outside**, with 0.10 and 0.40 sensitivities. AZ Technology lists AZ-93 nominal dry thickness 5±1.5 mil and optical data, but no installed dry areal mass. That source does not qualify these optics on Be or the assumed mass. The older NASA Z-93 compilation also does not supply a density to close this account. We retain 037's optics, rather than taking additional optical credit. Sources: [AZ-93 manufacturer](https://www.aztechnology.com/product/1/az-93), [NASA coating compilation](https://ntrs.nasa.gov/api/citations/19730017242/downloads/19730017242.pdf).

## Joining, pads and service

For nominal rectangular stock a=.6096 m, b=1.8288 m and scarf ratio r=30.34139731914874,
Ls=A[1/(a−r tf)+1/(b−r tf)]. Joining is:
2A μfilm + Ls[2tf√(1+r²)×.07 + .0005tc×500 + .002].
The actual account charges this sum. The retained-floor account charges max(actual, .05 structural mass), not their sum. No free deletion of scarf overlap or reticulated film is taken.

The light pad carries the 20 m/s drag multiplied by 1.4; the heavy pad carries the unfactored 70 kn drag, as in 037. Each is resized at each R. Pad area F/Fcrush and 6061 plate thickness √[3(1+.33)F ln(a/.025)/(2π×276 MPa)] determine mass at 2,700 kg/m³. At R10 they reproduce approximately 8.65075 and 33.1375 kg, the latter differing by 0.0001 kg from source velocity rounding. Keeping those kilogram values constant at larger radii would not preserve their load capacity. The light pad has only 0.431832 of the 70 kn load capacity. Pad/core punching, peel and distribution into the spherical sandwich remain unqualified.

All accounts retain 100 kg systems. 034's 15 kg vacuum hardware, 5 kg controls, 10 kg power and 0–20 kg installation occupy 30–50 kg **inside** that allowance. Their marginal cost above 100 kg is zero. Separate +30/+50 kg sensitivities show the alternative if the entire 100 kg is already committed. Monitoring 5 W for 24 h needs 1.111 kg battery at the stated deratings, inside the 10 kg power package. Hardware scalability remains an assumption.

The 24 h sealed-service calculation is rebuilt at each actual seam length, film mass and core thickness. It uses 10 Pa initial gas, .001 mbar L/(s m) seam leakage plus .01 mbar L/s ports, 10 Barrer assumed scarf permeability, and conditioned finite outgassing inventories from 034. A no-backpressure integration provides an upper ingress/pressure bound. Only the scarf polymer path is exposed; no full-area film flux is invented through intact metal. External water partial pressure is 1 kPa in ISA/optimistic and 6 kPa in both-weather.

Gas mass charged is max(.01 lift, initial gas + external ingress + trapped-cell gas). Outgassing changes the phase of material already aboard and is charged to pressure, not again to vehicle mass. Pore volume is A tc(1−ρcore/ρAl). Unvented cells retain that volume's ambient air. P2 has no tube bores; its bore term is zero, not an omitted P3 debit.

SERVICE-AUDIT.json corrects pressure for the inner cavity and connected pore volume, verifies the conservative retained gas charge, and gives late-vent, high-leak and unconditioned sensitivities. Unvented results are mass sensitivities: their isolated cell pressure changes the mechanical load path, so they are never labeled a passing assembly. The late-vent pressure is a counterfactual, not the pressure inside still-isolated cells.

Retained water is .10 kg/m² and contamination 5(R/10)² kg. The signed payload is reference lift minus all bill lines, including weather headroom. A negative value is a required mass reduction; it is not payload aboard.

## Search, debit costs and checks

At each core thickness, a vector bisection finds the least face gauge satisfying the seven shell/scarf screens. Thermal shear and service pressure filter feasibility. A logarithmic thickness scan identifies every local maximum and feasibility boundary; bounded refinements and boundary bisections finish the one-dimensional search. Denser 3,000-point scans check every primary endpoint and least-use result. The selected feasible designs lie well inside the geometry search range.

All 16 subsets are evaluated for each of the 120 radius/weather/joining/pad/venting configurations. Full details and negative balances are retained. No material property is fitted to a floating result.

Debit costs are paired reoptimizations, not additive derivatives: remove one charge or load screen, then solve the least γ with Q=.82 or least Q with γ at its favorable envelope, holding .015 film and baseline Be properties. Those are two different constrained optima and must not be combined into one design. Where the whole bill cannot float even at the endpoints, no finite in-range γ/Q price exists. The payload recovered by an omission is still reported. Floor-release, two film weights, service nesting and the extra-service alternatives are explicit.

VALIDATION.json records scalar independent equation/ledger checks, source hashes, atmospheric reconstruction, 033 regression, 037b free-edge/residual reproduction, thermal resolution and denser searches. QUALIFICATION-AUDIT.json supplies the favorable modulus bounds and the reduced necessary γ/Q values. Numerical validation does not validate the material, bond, aerodynamic or mission assumptions.
