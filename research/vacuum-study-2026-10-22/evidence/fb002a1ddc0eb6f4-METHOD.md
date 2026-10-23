# CHECK-045 method

All installed-assembly conclusions remain QUESTIONABLE. Material transfers,
life-independent fracture probabilities and operating scenarios are PROJECTION.
This check neither changes the owner's files nor grants an allowable.

The owner report, checker order, requested briefs and fifteen additional
non-code upstream inputs were copied and SHA-256/byte checked. Nine named
owner/predecessor code artifacts were not opened, copied, hashed, imported or
executed. Their supplied metadata is retained in UNREAD-CODE.json. No other
seat was contacted. Acknowledgment and completion are ordinary queue filings.

All 36 frozen inputs still match their intake pins. The final original-file
recheck found one later COMMON amendment about retrying refused simulation
jobs; the other 35 originals remain identical. INPUT-DRIFT.json records the
amendment and its separate snapshot. It changes no scientific input, and no
unfinished simulation job remains. PIN-CHECKS.json preserves the earlier
72-of-72 check; VALIDATION.json records the final delivery check separately.

`check45.py` reconstructs the equations from the cards, 028b METHOD, 022d
METHOD and primary inputs. The owner JSON is an expected-value ledger, never
a source of executable functions. `frame45.py` builds a new mesh and beam
stiffness matrix; `leak45.py` integrates its own differential equations;
`audit45.py` checks input identity, source selection, the filed design
witnesses and independently expanded cross-form invariants.

P2 uses R=10 m, p=95460.837913905 Pa, lift=4889.442150187 kg, E=290 GPa,
rho_face=1850 kg/m³, nu=.0752 and the fixed 019 reserve 411.298944072 kg.
The 028b scarf shear screen gives sigma_face=10 MPa×901/30 and
tf=pR/(4 sigma_face). Core thickness solves the complete structural,
max(5% allowance, physical joining), 100 kg systems and reserve balance.
The nominal point is tf=.794624067 mm, tc=23.237217906 mm,
gamma=.564163567 and usage=.971977517. All modes and joining follow
the pinned 028b method. Denser-core pricing only reproduces with
Ec and Gc multiplied by density ratio k; crush uses k^(5/3). Those are
additional material projections, not product data.

For the patch, N=pR/4; D=Etf³/[12(1−nu²)]; q0=p−2N/R.
The clamped eigenvalue is the first positive root of J1, 3.831706;
the simply supported one solves xJ0(x)−(1−nu)J1(x)=0.
Critical diameter is 2x√(D/N). The owner's proposed growth depth is
(crush−q0)b²/[4(N−x²D/b²)] when the denominator is positive.
Below that eigenvalue threshold this *model* returns no growth.
This subtraction of a plate eigenvalue from a constant-force paraboloid
model is not a validated crush-foundation solution. Crushed width,
residual depth, peak penetration and face fracture are distinct quantities.

The 015b geometry transfer uses teq=√3(tc+tf), with the inherited nu=.33
for its width scale. Plateau is .964/(1+lambda)^1.23+.036.
Eq.3 inverse is −ln[(gamma−.45)/.51]/3.88 times teq; the Lee
inverse is [.25/(gamma−.068)−.28]teq. Narrow-width extrapolation and
sandwich transfer remain unvalidated. The separate Poisson conventions
are retained for reproduction and explicitly identified.

For a soft contact radius a, spread b=a+tf/2√(sigma_y/crush).
Plastic face work is π sigma_y tf d². Constant-footprint core work is
π crush b²d. Pressure balance gives d=max(0,(q a²−crush b²)/(2 sigma_y tf)).
For a hard hemisphere, contact radius expands as √(2rd−d²), capped at r;
core work is the integral of π crush b(d)² over penetration. This check
uses that integral analytically. Its differences from the filed hard-contact
quadrature are about one part per million. Eighty-percent absorption and
the doubled-depth band are declared assumptions. Core-through cases
do not establish a post-perforation shape or strain.

P3 geometry, coupled lambda-sized CFRP joints, annulus, sag loss, film mass,
six scalar modes and half-wave screen follow 022d METHOD. A new multistart
SLSQP search supplies alternative witnesses. The filed points are separately
forward-scored: their different objective values are search differences,
not automatically arithmetic errors. No global-optimality proof is claimed.
For Perry, e=L/1000 and eta=e ro A/I. If C and E denote the compression
and Euler load factors, the stable quadratic root is
2CE/[C+E(1+eta)+sqrt((C+E(1+eta))²−4CE)].
It matches the direct magnified-stress equation and the pinned 022d table.
The 15.586 MPa hypothetical tensile screen is also checked on every new witness.
At multipliers below one, lambda-sized joints are below operating demand.

The tube contact screen is an infinite isotropic plate on a Winkler foundation:
D=Et³/[12(1−nu²)], k=Et/ro², ell=(D/k)^(1/4), nu=.16, contact radius .012 m.
The centre stress multiplier is 3(1+nu)c²/t² times
integral J1(u)u²/[u⁴+(c/ell)⁴] du. Quadrature agrees with the independent
closed identity −Re[K1(z)/z], z=(c/ell)exp(iπ/4).
It gives 55.549976 Pa stress per Pa contact pressure.
Pf=1−exp[−(sigma/sigma0)^m]. Tube 299/192 MPa values are already
characteristic strengths; the 380 MPa bar mean is divided by Gamma(1+1/10).
No effective-size, dynamic-impact, installed-flaw or prestress qualification
is supplied. Exact repeated-trial counts require an independence assumption.

The beam reconstruction starts with an icosahedron, divides each face into
f² triangles and projects nodes to R=10. Euler–Bernoulli members use the
022d A/I, E=410 GPa, nu=.16 and J=2I. Radial loads with one third of each
*planar* triangle's area reproduce the owner. Spherical-area, equal-area
and face-normal alternatives are preserved as sensitivity calculations,
not errors in the selected model. Six free rigid-body modes are removed by
orthogonal Lagrange constraints. Every geometric edge class is removed:
six for f4 and nine for f5. Reported cases are paired by removed-force
class only after all independent classes have been solved. Meshes are pinned.
Truss compatibility rank confirms one additional mechanism after a member
is removed. A floating-point condition number near 1e17 is not a unique
physical property and cannot be reproduced without the exact constraint/scaling.

Atmosphere is T=288.15−.0065z, p=101325(T/288.15)^[g/(Rgas×.0065)],
Rgas=287.05287, g=9.80665. The baseline non-air mass is rho(500)V.
Mass flow uses the ideal-gas choked expression with gamma=1.4 and Cd=.6,
then the isentropic subsonic expression above pressure ratio .528281788.
Inside temperature follows outside temperature instantly. The sphere equation is
(M+m+.5rho V) zdotdot=(rho V−M−m)g−.5rho Cd_drag πR² zdot|zdot|.
The filed model omits incoming-air momentum; a separate sensitivity adds −mdot zdot.
The P2 pressure diagnostic uses 4π(R−tf−tc)³/3, although reference buoyancy
and descent use the full sphere. The tabular gas budget is rounded to 48.894 kg.
Those conventions are explicit reconstruction inputs.

DOP853 roots ground and m=.5 kg events. Main comparisons allow 0.1% plus
2e−5 in trajectory fields because very slow descent retains small oscillations.
Hole-diameter roots allow .02%. Stationary algebra normally uses relative
2e−7, hard-contact quadrature 5e−6, beam cases 3e−5 and new-search comparisons
2e−5. Every row records its own tolerance. Search differences and primary-input
corrections are separately classified. No tolerance turns a failed design into SF1.

The headline trajectory reproduces the owner's centre-height-zero convention.
GROUND-CONTACT-SENSITIVITY instead stops at z=R over level terrain. Incoming
gas is not net heaviness: the latter subtracts the local displaced mass.
The valve table follows a fixed-pressure hydrostatic gradient; a neutral
ISA descent uses the smaller density gradient, also tabulated.
Actual inventory, sagged volume, thermal fill, control and terrain need a
separate specified operating model.

All 388 library rows have source URLs and QUESTIONABLE tags; all 87 selected
value mappings match their underlying records. Primary documents were
retrieved independently. Five HTTP access pages are explicitly quarantined.
2025 annual CFR PDFs verify the cited historical clauses; failed current
retrievals do not establish current regulatory approval. EVIDENCE.json
records scope and corrections. Sixteen inherited NFIs and fifteen new
nonblocking rows remain open.
