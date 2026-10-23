# MAINLINE-053 thermal specification

All inherited material properties are QUESTIONABLE. Installed geometry, optical
transfers, environmental cases and performance predictions are PROJECTION.
This document specifies computations; it does not qualify a flight envelope.

| Item | Explicit convention | Qualification or missing input |
| --- | --- | --- |
| Geometry | Sphere of outer radius 10, 12, 15, 20 or 30 m; nominal equal face/core areas | Exact inner mouldline and coating/bond thicknesses are omitted |
| Coordinate | μ = cos θ; sun and zenith coincide | No latitude, season, tilt or time history is supplied |
| Air | 284.9 K, 1.1672683307461802 kg/m³; speed 2 m/s | These values remain fixed when buoyancy weather changes |
| Air properties | μair = 1.79e−5 Pa·s, kair = .0257 W/(m K), Pr = .71 | Constant properties; viscosity-ratio correction equals one |
| Forced convection | D = 2R; Re = ρvD/μair; Nu = 2 + (.4 Re^.5 + .06 Re^(2/3)) Pr^.4 | Whitaker's sphere correlation is extrapolated far beyond its source Reynolds range |
| Alternative mixed convection | h = max(hforced, 1.32 max(abs(To−Ta), .05)^.25) | The inherited natural-convection floor has no documented sphere size, wind direction or validated range |
| Day | Direct beam 970 W/m², solar input α 970 max(μ,0); sky 275 K | No diffuse solar, ground-reflected solar, cloud distribution or Earth curvature |
| Night | Zero sun; sky 260 K | Separate equilibrium, not a transient overnight calculation |
| Ground | 284.9 K both cases | No sun-heated ground or changing terrain temperature |
| External view factors | Fsky = (1+μ)/2; Fground = (1−μ)/2 | Infinite flat ground, opaque diffuse surroundings, unobstructed local hemispheres |
| Outer longwave | εo σ[To⁴ − Fsky Tsky⁴ − Fground Tg⁴] | Hemispherical thermal emittance, not a normal-emittance measurement |
| Selected finish | Multilayer CCAg/ITO, α=.09, εo=.80; applied mass .00833272 kg/m² | Optical pair transferred from a coating class; exact recipe on Be unqualified |
| Reference finish | α=.20, εo=.90 | Retained to explain 037/040 and the two checks |
| Inner cavity | Uniform inner emissivity .20; diffuse gray enclosure, no internal obstruction | Unspecified equipment/view obstruction and actual inner-face finish |
| Cavity flux | qi = .20 σ[Ti⁴ − average(Ti⁴)] | Sphere view-factor identity gives uniform irradiation; no net cavity heat source |
| Core conduction | kcore = 130 ρcore/ρfoil; ρcore =16.018463373960138 kg/m³ | Solid-metal parallel conduction approximation; no measured bonded-panel conductance |
| Foil density | 2640 kg/m³ for historical 037 comparison; 2700 for current tables | Distinct conventions are never silently mixed |
| Extra core-gap term | U = kcore/tc + 4 εgap σ average(Ti)³; εgap either 0 or .20 | This is separate from enclosure radiation; effective gap emissivity is not established |
| Face, film and contact resistance | Zero in the inherited and primary comparison tables | Adhesive, coating and face resistance need measured material/process inputs |
| Surface conduction | No lateral face/core conduction | Degree-dependent smoothing and seam effects are unresolved |
| Energy balance | External convection + external radiation + core heat flux − absorbed sunlight = 0; inner core flux balances cavity exchange | Residuals and net cavity exchange are checked explicitly |
| Extremes | Settled alternatives include μ=±1; old tables use extrema at quadrature nodes | Missing the poles produces a small numerical, separately measured difference |
| Curvature | Mean face temperature; remove constant and degree 1; retain Legendre degrees 2–6; analytic θ-second derivative | Six-degree truncation is a structural screen, not a complete shell temperature field |
| Thermal stresses | Gradient and pattern terms below; 1.002 interpolation guard | The guard covers numerical approximation only |
| Cure | Proposed stress-free temperature 366.4833333333333 K (200°F); use coldest/hottest service temperature | Actual stress-free cure state and bond process remain unqualified |

The owner uses the mixed-convection floor and εgap=.20. Both independent checks
use forced convection alone and εgap=0. These choices change the physical
equations; reducing a solver residual cannot make one set reproduce the other.
The later 048 fold supplies the previously missing terms in non-code form.

For a uniform-emissivity diffuse sphere, the differential view factor from any
surface point to a receiving patch is dA/(4πR²). Therefore irradiation is
constant, and averaging the radiosity equation gives G=σ average(Ti⁴).
The cavity formula above follows without prescribing an interior air
temperature. This derivation assumes an empty, unobstructed sphere.

The gap term and cavity term represent different paths. Their simultaneous
presence is not automatically double counting. However, taking the same .20
for both does not establish the gap's effective emissivity. Even two infinite
gray plates of emissivity .20 have effective exchange factor 1/9, before
honeycomb-wall and adhesive effects are considered.

Primary evidence does not select a validated full-hull convection law or an
installed core-gap conductance. Consequently the settled product is an
explicit four-row model matrix: forced/mixed convection crossed with zero/.20
gap augmentation. The conduction-only rows are the transparent reference
calculations; the additional rows preserve the owner's assumptions. These
alternatives are not certified upper/lower bounds on the real hull.

Whitaker's original Table 1 gives a sphere Reynolds interval 3.5–76,000.
The present 20–60 m diameters at 2 m/s exceed that interval; the source does not
validate either a spatially uniform local coefficient or the inherited
natural-convection floor. [Whitaker, 1972, Table 1 and Eq. 33](https://www.researchgate.net/profile/Stephen-Whitaker-3/publication/229709417_Forced_convection_heat_transfer_correlations_for_flow_in_pipes_past_flat_plates_single_cylinders_single_spheres_and_for_flow_in_packed_beds_and_tube_bundles/links/59d73bda0f7e9b42a6b0694a/Forced-convection-heat-transfer-correlations-for-flow-in-pipes-past-flat-plates-single-cylinders-single-spheres-and-for-flow-in-packed-beds-and-tube-bundles.pdf).

NASA's honeycomb investigation separates metal-core conduction, radiative
transport and the bonded interface. Its specimens do not provide the missing
conductance for this CR-III/AF163/Be assembly.
[NASA honeycomb thermal-property investigation, section 3](https://ntrs.nasa.gov/api/citations/19680009019/downloads/19680009019.pdf).
NASA's coating presentation reports a multilayer CCAg class with hemispherical
emittance above .80 and solar absorptance below .09. It does not qualify the
selected recipe on Be in wet terrestrial service.
[NASA Goddard, 2018, slide 39](https://ntrs.nasa.gov/api/citations/20180002012/downloads/20180002012.pdf).
