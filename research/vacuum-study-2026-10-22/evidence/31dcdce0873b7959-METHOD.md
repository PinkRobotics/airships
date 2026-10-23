# MAINLINE-053 calculation method

The new programs import no upstream executable. Source inspection is permitted
for this settlement card and is recorded in INPUT-PINS.json; it identifies
the implemented boundary terms. New energy equations and a simultaneous
two-face/two-moment Newton method supply the independent arithmetic.
The code prohibition from the earlier CHECK-045 is not represented as applying
to this separate specification-settlement assignment.

`thermal53.py` solves both local face balances together with the mean inner
temperature and its fourth-moment temperature. Each zone contributes a two by
two face Jacobian. Eliminating those local blocks leaves a two by two system
for the cavity moments. The additional core conductance's mean-temperature
derivative is included. This differs from the owner's nested fixed-point
algorithm and is checked by energy residuals and constant-environment tests.

For reproduction, the actual historical quadrature, density, extrema and
projection choices are retained. Old owner day curvature uses raw 37-midpoint
projection; its derived 048 night field removes the mean. CHECK-048's legacy
night also projects the raw field. The latter therefore assigns substantial
curvature to a nearly constant cold field. This legacy diagnostic must not be
used as a physical night bending load. All common tables remove the mean.

Settled alternatives use split Gauss quadrature on [-1,0] and [0,1], integrating
the incident beam's hemisphere kink without the old quadrature bias. Both
poles are solved after the enclosure moments converge. Curvature extrema are
obtained from the real stationary points of the degree-six polynomial plus
the endpoints. A 241-point logarithmic core-thickness table spans
.001R/10 to 1.5R/10 metres. Higher quadrature orders and direct geometry
evaluations provide numerical checks; uncertainties in boundary physics are
kept separate.

The selected P2 uses ρBe=1850 kg/m³, E=290 GPa, ν=.0768, and the 345 MPa
tensile-to-compression proxy. The face-tuple optimism axis extends E to
293.6 GPa and that proxy to 379.2 MPa. Core properties are the pinned 040
CR-III 5056 3/8–1.0 inputs. None becomes an installed allowable.

For each face thickness tf, core thickness tc and separation h=tf+tc:

```
σp = pR/(4tf)
σ0 = E h/[R sqrt(1−ν²)]
σcr = Gc h²/(2tf tc)
Vc = σ0/σcr
Kc = 1−Vc/4 for Vc≤2, otherwise 1/Vc
γbase = .2 for Vc<2, otherwise 1
γfull = .2+.4 min(Vc,2)
γ(u) = γbase (γfull/γbase)^u
```

The remaining interpolation axes are Q=.33(.82/.33)^u, the E/strength tuple,
and film mass .1464728290914915×2^(−u) kg/m² at each interface. Mask 11 is the
028b endpoint: full gamma and Q, today's face tuple, and .015 lb/ft² film.
Calling that endpoint “two-factor” retains its historical film assumption;
the present least-set accounting counts film as a separate axis.

With thermal interpolation guard g=1.002, ΔT the largest day/night face
gradient and Kθ the corresponding largest absolute curvature temperature:

```
σgradient = E αBe g ΔT/[2(1−ν)]
σpattern = E αBe g (tf+tc) Kθ/[2(1−ν²)R]
Kbiax = .5 Efoil ρcore/ρfoil; Efoil=67 GPa
δ = g |αAl−αBe| max(|Tcure−Thot|, |Tcure−Tcold|)
τedge = δ sqrt(2 Kbiax Gc)
σcure = Kbiax (αAl−αBe) g max(Tcure−Tcold,0) tc/(2tf)
σwall = 1.2 Efoil δ
```

αBe=11.3e−6/K and αAl=23.6e−6/K remain transferred properties. Edge capacity
is 25 psi minimum W shear. Wall capacity is the 227.53 MPa 5052-H39 proxy.
The 30.34139731914874:1 scarf has average demand σd r/(1+r²), with
σd=σp+σgradient+σpattern+σcure, against the assumed 10 MPa screen.
The original compliant-core model assigns zero continuous-field mismatch
interface shear; it does not establish adhesive peel strength.

Global buckling, face compression, crimp, crush, wrinkling and dimpling retain
the 040/048 equations. Wrinkling uses β³+β=1 and
β Q sqrt(E Ec tf/tc). Dimpling uses E(tf/cell)²/(1−ν²).
Both the original exclusion and the later CHECK-040/048-fold inclusion of
balanced cure compression in global/crimp demand are calculated. Results
label that mechanical choice separately from the thermal choice.

Pressure is p0 max(1.01, weather multiplier) plus the complete 70-knot dynamic
pressure. ISA p0=95460.83791390515 Pa and lift
4889.442150186961(R/10)³ kg are inherited. The optimistic 100 m floor weather
headroom and pressure multiplier come from the pinned 031 atmosphere table.
This pressure/buoyancy substitution does not silently change the thermal
environment. No validated combined-weather thermal mission is claimed.

Stock panels are .6096 by 1.8288 m. Seam length is
A[1/(.6096−rtf)+1/(1.8288−rtf)]. Physical joining is two full film interfaces,
two-face scarf film at .07 kg/m², .0005 m core splice at 500 kg/m³, and
.002 kg/m seam seal. Actual and max(actual, 5% structural mass) accounts are
separate. Structural primer .010 kg/m² lies outside that floor.

The bill retains the .00833272 kg/m² applied multilayer coating, 0.1 kg/m²
exterior water, radius-scaled contamination, resized heavy mooring pad,
100 kg systems, gas reserve, weather headroom and added material water.
Three drying routes are carried: dry gas; projected 90% added-water removal
by ground bake; and onboard sorbent that retains water while adding bed mass.
No drying route removes the exterior-water debit.

Material water, nominal volatile release, leakage, permeability, pressure and
sorbent capacity use the written 048 equations. All phase changes conserve
vehicle mass. Charged gas is max(1% lift, initial gas plus outside ingress).
The 24-hour hot-pressure calculation uses 320 K and the independently
reconstructed dry-species molar mass. The thermal revision grants no extra
water, equipment, maintenance or process credit.

`account53.py` bisects the minimum feasible face for each core thickness,
searches a dense log-core grid, refines every sampled local maximum and
locates valid-interval boundaries. The domain is .0012–1.4 times R/10 m
in core thickness and at most min(.0195,.008R/10) m per face. Every optimism
subset is scored at its endpoint. Floating subsets of minimum cardinality
are then solved for a common logarithmic usage. Favorable E bounds use the
largest elastic E with today's thermal E to check lower-cardinality
rejections. This is a scalar-model search, not a physical buckling proof.

Heavy scientific runs use one-core, 1 GiB simjob admission. Exit 75 starts
nothing and is retried with unchanged command and resources, at least a
minute apart. Admission and completion receipts are retained in execution/.
No timing is a work budget. Source downloads and artifact custody checks are
distinct from scientific executions.
