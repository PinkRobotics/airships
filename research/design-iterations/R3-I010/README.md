# R3-I010 — 76 m helium envelope with explicit module restraint and trim

**100 t buoyant mission: FAIL. Physical confidence: UNKNOWN.** The nominal 76 m construction is 7.949 t heavy at 2,500 m with 100 t payload and the separate 17 t provisional equipment allowance. The 20 t equipment/payload placeholder instead needs 89.051 t of added water ballast. A positive untrimmed mass margin is not a neutral operating point or mission reserve.

The changed suspension closes the represented ideal module force equations at 0 and 5 m/s; 10/20/30 m/s remain FAIL. Static straight-path routing clears, but cable sag, folded bags, curtain stiffness and local membrane load transfer remain UNKNOWN. Both constructions have negative differential pressure over part of their full spherical bag design envelopes under the shared pressure datum. Those envelopes therefore cannot be credited as everywhere inflated by positive internal pressure. No float, structural qualification, endurance or hardware capability is established.

`R3-I010 | 76 m | P100 -7.949 t @2500m | M20 ballast 89.051 t | ideal 5 m/s nodes PASS | physical UNKNOWN`

## Scope and matched comparison

One construction replaces the separate two-cable cargo modules of R3-I006 with three-anchor sector triangles, reprices the actual water cradles and air network, and retains a connected gas inventory. This is a bounded paper calculation: analytic geometry, 3 by 3 linear balances and mass/flow arithmetic in [calculate.py](calculate.py). There is no optimizer, finite element model, CFD or native physics solve.

Research sources are the frozen R3-I002 record `2da1ca08e9013c4c65cd26984b2b66492da28c46` and R3-I006 record `300ceae0cfda20c126abc88d8d1f50728ef88c1f`. The implementation is a sibling from historical source `afb2c2d1726b9d9a805f9781085c3dd6a52913e5`; that hash is not asserted to be current public main. Neither earlier record is rewritten. I006's disclosed spatial-equilibrium UNKNOWN now has a quantified constraint: at its original 4 m module radius both upper cables pull outward. Their radial reaction is 0.313391 times supported weight, at least 7.683 kN/module for M20 and 44.947 kN/module for P100 before distributed loads. Azimuthal symmetry does not cancel that reaction.

The **matched 70.575 m column uses this new construction**, including its cradles, cable directions and ballast system. It isolates diameter from architecture. Frozen I006 instead had construction mass 37.674821 t, M20 margins +78.288007/+78.241090 t and P100 margins -18.711993/-18.758910 t at sea level/2,500 m, with its unresolved local equilibrium. Those values are historical conditional controls, not an interchangeable baseline.

M20 means 3 t fixed cargo plus 17 t provisional equipment. P100 means 100 t **movable water payload** plus the same 17 t equipment. Arbitrary solid cargo cannot be assumed to supply the represented water-shift trim. R3-I007 owns fuller mission equipment repricing; 17 t is not mission-proven. All overrun masses below are additional to that allowance.

## Common physical and gas assumptions

Both diameters use 96% helium/4% air by mole, centre-reference helium pressure ambient +1,000 Pa, and connected ballonet air at helium +250 Pa. Purity is a mole fraction, not a mass fraction. Constants are `g=9.80665`, `R_air=287.05`, `R_u=8.314462618`, `M_He=0.004002602 kg/mol`, `T0=288.15 K`, `p0=101325 Pa`, lapse `0.0065 K/m`. The local ISA equations match the repository atmosphere convention. [NIST's helium entry](https://webbook.nist.gov/cgi/cbook.cgi?Name=Helium) supplies molecular mass; [NASA atmospheric context](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/earth-atmosphere-equation-metric/) is background, not a claim that its rounded curves were substituted.

Loaded volume uses the same explicitly assumed fraction `V0 / (pi D0^3/6)` from the frozen control. This is a common deformation assumption, not a pressure/strain solution. Nominal diameter supplies envelope area and conservatively bounds pressure head; loaded radius supplies internal geometry. Each hull loses the same 100 m³ non-gas space. Sleeved helium space inside the geometrical bag envelopes is a separate 50 m³ routing reserve, not a second solids debit.

| Quantity | Matched 70.575 m | Candidate 76 m |
| --- | --- | --- |
| Loaded outer volume, m³ | 181,394.539 | 226,524.378 |
| Loaded radius, m | 35.116552 | 37.815988 |
| Free hull volume after 100 m³ debit, m³ | 181,294.539 | 226,424.378 |
| Helium/impurity inventory, mol | 5,765,795.032 | 7,201,080.395 |
| Helium mass, t | 22.155055 | 27.670136 |
| Impurity air mass, t | 6.680298 | 8.343231 |
| Installed usable connected-air capacity, m³ | 54,388.362 | 67,927.313 |

At 2,500 m, `p=74682.289817 Pa`, `T=271.9 K`. Exactly one lifting-gas inventory is fixed by `n=(p+1000)*0.95*V_free/(R_u*T)`. At any endpoint, `V_g=n R_u T_g/(p+1000)`, `V_air=V_free-V_g`, and inside air mass is `(p+1250)*V_air/(R_air*T_air)`. Four symmetric lobe positions cancel first-order horizontal hydrostatic moments under the assumed equal fill. Actual folded centres and load sharing are not established.

| 76 m endpoint | Sea level | 2,500 m |
| --- | --- | --- |
| Gross displaced ambient air, t | 277.495142 | 216.753347 |
| Helium-mixture occupied volume, m³ | 168,604.327 | 215,103.159 |
| Connected inside air volume, m³ | 57,820.051 | 11,321.219 |
| Connected inside air mass, t | 71.704073 | 11.014199 |
| Outside manifold/tail air, t | 0.024727 | 0.019399 |

The internal duct air (94.599 m³ by centreline geometry) is included in connected inside air, not added again. External manifold/tails hold 19.939 m³, charged separately at their operating density. No displacement credit is taken for outside equipment. Ascent vents 60.695202 t of air; descent must restore it. Helium and impurity masses remain fixed. Air venting is not a second lifting-gas mass saving.

## Concrete load path and construction

There are eight cargo apices at azimuths `phi=k*pi/4`, radius `r_m=0.5*r`, and height `z=-r-3 m`. Each has three independent upper anchors on the loaded sphere:

- One inward anchor at horizontal radius `0.20*r`, azimuth `phi`, height `r*sqrt(1-0.20²)`.
- Two outward anchors at horizontal radius `0.85*r`, azimuths `phi ±18 degrees`, height `r*sqrt(1-0.85²)`.

All three allowable directions point upward; one pulls radially inward and the other two pull outward with opposite azimuthal components. At 76 m, `r_m=18.907994 m`; the inner cable is 78.690 m and each outer cable 62.639 m. There are 24 main lines, 48 pin fittings, 24 lower-envelope seals/chafe sets, 24 added 5 by 5 m doublers and 24 triangular 5 by 8 m load curtains. They are counted individually, including overlapping reinforcement where present. Surface compatibility and combined stress near overlapping patches remain UNKNOWN.

Loads run from water bladder/floor through a braced cargo frame and four short lower slings to its apex; the main lines transfer those loads through curtains/doublers into the pressure envelope. Propulsion thrust acts through the same apex. The motor mount assumption is a 3 m axial offset with the thrust line still passing through the apex, and a vectorable 4 m rotor. Mount stiffness, torque cancellation and rotor/rigging clearance through its full tilt range remain UNKNOWN; no bending-moment cancellation is silently credited. Eight provisional 375 kg propulsion packages allocate 250 kg motor, 65 kg rotor and 60 kg mount each; these are mass assumptions, not selected components or ratings.

Each cargo frame is 3.2 by 3.2 by 3.8 m: twelve edges plus three floor beams, 50.4 m of 300 by 150 by 6 mm closed rectangular section. Floor plate is 16 mm. Each water bladder is a 3 m diameter, 3.6 m tall cylinder, 4.5 mm fabric including the selected 1.5 load multiplier and 30 MPa working stress with 0.6 seam efficiency. Eight frames use four X-braced sides, eight corner joints and ten floor brackets each. Lower slings are 3.020 m long, sized at 138.822 kN limit tension. Frame metal assumptions are density 2700 kg/m³, E=70 GPa and 100 MPa effective working stress; no alloy or weld qualification is inferred.

The selected module limit is 25 t **including equipment and construction**, although the geometric water volume alone could hold 25.447 t. The simple frame checks give 87.853 MPa beam bending, 67.337 MPa floor-strip bending, 8.925 mm beam deflection, and Euler/4 column load 254.786 kN against 91.937 kN demand. Local buckling, joints, bladder restraint, slosh and transient racking are UNKNOWN. The old lattice's 1 mm wall reversal is not bypassed by a nominal zero-thickness member: these retained box sections have 6 mm walls and pressure ducts 1 mm walls.

| Eight-cradle component | Mass, t |
| --- | --- |
| frames | 5.721892 |
| floor plates | 3.538944 |
| frame joints floor brackets | 1.040000 |
| side braces | 0.174260 |
| brace terminations | 0.640000 |
| lower slings | 0.128789 |
| lower sling fittings | 0.768000 |
| water bladders and 10pct laps | 2.664799 |
| water ports | 0.064000 |
| Actual total | 14.740684 |
| Overrun above the existing 3 t cradle allowance | 11.740684 |

The envelope working stress is an **assumed** 80 MPa, representing a nominal 320 MPa ultimate divided by four, with 0.70 seam efficiency. Cable working stress is an assumed 150 MPa after termination/handling deductions; density is 1440 kg/m³. Fabric density is 1400 kg/m³. These are sensitivity inputs, not supplier allowables. The [FAA-hosted LFLS](https://www.faa.gov/sites/faa.gov/files/aircraft/air_cert/design_approvals/airships/aceAirshipLFLS.pdf), printed pp. 32–33, provides context for fabric/nonmetallic suspension ultimate factors and distributed attachment/chafe concerns; it does not certify these assumed materials. The selected 1.5 limit-load multiplier is separate from the working-stress reductions.

At 5 m/s, the 76 m pressure-head bound is 376.907 Pa; `|Cp|<=1.5` and `Cd=0.8` are assumed. Peak pressure is 1,399.876 Pa. Pressure-only membrane demand is 26.598 kN/m; adding a 300 t vertical suspension bound times 1.5 and wind demand gives 45.430 kN/m versus 56.000 kN/m working capacity at 1 mm. This is a scalar strip screen, not a deformation or curtain/skin compatibility proof. The doubled anchor patch screen is 59.452/112.000 kN/m demand/capacity.

Main lines are sized against a 25 t module at 1.5 times load and horizontal/vertical force ratio 0.06, with a separate self-weight allowance. The equivalent diameter is 48.790 mm and working tension 280.447 kN. The 50 mm pins use assumed 100 MPa double-shear working stress. These screens do not establish termination fatigue or catenary compatibility.

## Ballonets, finite routing and air hardware

Four spherical design envelopes have radius 15.949184 m, centre coordinates `(±a,±a,±a)` in the four tetrahedral sign combinations with `a=11.454553 m`. Adjacent full spheres have a 0.5 m gap, and their outer extent is 35.789 m inside loaded radius 37.816 m. Their geometrical volume is usable 30% air capacity plus 50 m³ for routing; actual occupied air is 25.536% at sea level and 5% at altitude, including internal ducts. The folded shape during contraction is UNKNOWN.

Each bag has 32 gore laps, four closed meridian cradle bands, eight vertical hangers and eight upper envelope reinforcements. Hanger endpoints are at the bag's upper 45-degree latitude at 22.5-degree-offset azimuths; each upper end lies on the envelope at the same x/y. Actual hanger lengths are 3.780–37.298 m. Bag fabric is 0.25 mm; cradle bands are 250 mm wide by 3.6 mm. The support bound includes 69.729 t of apparent air load **and** supported fabric/fittings/bands, total 76.935 t before the 1.5 multiplier. Hanger self-weight is included in strength sizing. Equal vertical support reactions close the ideal bag's resultant; band/fabric contact and folded local stresses remain UNKNOWN.

The connected air and lifting gas share the hull-centre datum `z=0`, with `delta_p(0)=250 Pa`. The same uniform-density approximation gives `delta_p(z)=250-(rho_b-rho_g) g z`. Extrema include **both centre elevations and bag radii**, rather than resetting the datum at each lobe centre:

| Construction | Bag-envelope z range, m | Minimum / maximum differential, Pa | Everywhere positive over full envelopes |
| --- | --- | --- | --- |
| Matched 70.574858 m | -25.460799 / +25.460799 | -6.309 / 506.309 | FAIL |
| Candidate 76 m | -27.403737 / +27.403737 | -25.868 / 525.868 | FAIL |

The corrected positive maxima drive `t >= delta_p_max r_b / (2 × 30 MPa × 0.6)`, rounded up to a 0.05 mm gauge with a 0.25 mm floor. Both remain at 0.25 mm, so their downstream support sizes, construction masses and mass margins are unchanged. A negative differential over the upper part of a design envelope is a constraint on its assumed inflated shape, not demonstrated fabric failure or a solution for its actual folded/loaded surface. The spherical envelopes remain design bounds whose containment and contact behaviour require physical compatibility evidence; the positive-side thickness screen does not resolve that condition.

The bounded geometry calculation includes 24 main lines, 32 bag hangers and six straight duct segments. Main-node capture excludes only the last 0.5 m of each main line; the common duct manifold excludes the first 3 m, and same-duct elbow joins are intentional. All other segment pairs are compared using finite outer radii. The two upper-bag ducts use a priced waypoint at 75% of their direct path, rotated +20 degrees in azimuth; the direct versions intersected inward main cables. Mass includes terminal tails and an extra 0.5 m per dogleg.

There are 24 main-cable/bag and eight hanger/other-bag crossings. They use 120 mm flexible sealed sleeves with 1 mm fabric walls, sacrificial liners and two boots each. The inflated-sphere chord total is 647.965 m; with 4 m per crossing for tails, sleeves total 775.965 m. Their conservative air exclusion is 7.328 m³, below the 50 m³ geometric reserve. This is helium-filled excluded bag space, not missing mass. The final duct segments have no foreign-bag crossings. Minimum finite surface gap across the represented paths is 38.574 mm.

**That straight-path clearance is not a physical routing PASS.** At the 5 m/s, 22.5-degree case the small-sag estimate `q_perp L²/(8T)` reaches 0.308 m. This exceeds the minimum surface gap. Liners, boots, partial inflation and support locations need a deformation/contact calculation; no rigid compression-tube credit or unpriced guide reaction is used. Cradle/slings, sagged water hoses, rotor sweep, folds and curtain footprints are not all included in the straight-segment clearance set and remain explicit exclusions.

Four blowers feed one external common discharge manifold with isolation, then four ducts to the bag bottom ports. This connection is required before adding the three surviving blower ratings. Duct diameter is 1.030 m, charged length 125.446 m, with 1 mm aluminium walls, rings, one 10 kg support per rounded-up 4 m and four 15 kg bag ports. The wet outside air volume is charged separately. Common-manifold failure, fittings, losses and demonstrated pressure/flow curves remain UNKNOWN.

| Pressure component | 76 m mass, t |
| --- | --- |
| four blowers | 1.250000 |
| eight air valves | 0.371327 |
| two emergency helium valves | 0.092832 |
| duct 1mm aluminium and rings | 1.221505 |
| duct supports and bag ports | 0.380000 |
| common discharge manifold isolation | 0.250000 |
| sensors | 0.120000 |
| limiters | 0.080000 |
| mounts | 0.160000 |
| Total | 3.925664 |
| Overrun above existing 2 t allowance | 1.925664 |

## Complete mass budget

Construction includes full structural masses and only the increments above the cradle/pressure/ballast allocations already in equipment. Thus a cradle is not counted twice. The 17 t allocation remains 2 t pressure, 3 t propulsion, 5 t energy, 1 t avionics, 3 t cradles and 3 t ground/ballast provision. The ground provision includes fixed hose water; it is a wet equipment allowance. Its residual allocation is retained as mass even when the itemized estimate is smaller.

| Construction line | 70.575 m, t | 76 m, t |
| --- | --- | --- |
| envelope fabric | 21.906749 | 25.404175 |
| envelope seam laps | 1.714756 | 1.846571 |
| barrier weather | 1.564768 | 1.814584 |
| main anchor doublers | 0.840000 | 0.840000 |
| main load curtains | 1.344000 | 1.344000 |
| main cables | 4.091864 | 4.393131 |
| main pin fittings | 1.200000 | 1.200000 |
| lower envelope seals and chafe | 0.480000 | 0.480000 |
| bag membranes | 3.859303 | 4.475225 |
| bag 32 gore laps | 0.208456 | 0.224474 |
| bag cradle bands | 1.511302 | 2.020267 |
| bag cradle fittings doublers | 0.165600 | 0.165600 |
| bag hangers | 0.168931 | 0.226324 |
| bag hanger fittings | 0.320000 | 0.320000 |
| bag anchor doublers curtains | 0.537600 | 0.537600 |
| routing sleeves liners boots | 1.626301 | 1.697510 |
| cradle construction over 3t | 11.740684 | 11.740684 |
| pressure hardware over 2t | 1.403930 | 1.925664 |
| ballast hardware over 3t | 0.000000 | 0.000000 |
| Total construction | 54.684244 | 60.655809 |

| D, m | Case | Altitude, m | Equipment, t | Payload, t | All gas, t | Gross, t | Total before trim, t | Margin, t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 70.575 | M20 | 0 | 17.000 | 3.000 | 86.269971 | 222.210536 | 160.954215 | 61.256321 |
| 70.575 | M20 | 2500 | 17.000 | 3.000 | 37.671719 | 173.570165 | 112.355963 | 61.214202 |
| 70.575 | P100 | 0 | 17.000 | 100.000 | 86.269971 | 222.210536 | 257.954215 | -35.743679 |
| 70.575 | P100 | 2500 | 17.000 | 100.000 | 37.671719 | 173.570165 | 209.355963 | -35.785798 |
| 76.000 | M20 | 0 | 17.000 | 3.000 | 107.742168 | 277.495142 | 188.397977 | 89.097165 |
| 76.000 | M20 | 2500 | 17.000 | 3.000 | 47.046966 | 216.753347 | 127.702775 | 89.050573 |
| 76.000 | P100 | 0 | 17.000 | 100.000 | 107.742168 | 277.495142 | 285.397977 | -7.902835 |
| 76.000 | P100 | 2500 | 17.000 | 100.000 | 47.046966 | 216.753347 | 224.702775 | -7.949427 |

At 2,500 m the larger matched construction improves margin by 27.836 t, while adding 5.972 t of construction. This is a recalculated diameter comparison, not fixed-support volume scaling. P100 still fails buoyant lift.

## Loaded neutral trim and positive cable forces

A sphere's central drag plus underhung thrust creates a pitch moment. For wind unit vector `e`, total drag `H`, apex depth `h`, and module azimuth `phi`, water distribution is

```text
water_k = water_total/8 - H*h/(4*g*r_m) * cos(phi - wind_azimuth)
g * sum(m_k * position_k dot e) + H*h = 0
```

Fixed equipment stays equally distributed. The 100 t water payload is allowed to redistribute in P100; M20 uses additional ballast while its 3 t cargo stays fixed. Negative water or any module over 25 t is a FAIL, even if formal linear equations can still be solved. One fixed M20 ballast inventory, equal to the smaller endpoint margin, is carried across both altitudes. It is not independently refilled at altitude.

| Trim requirement | 70.575 m | 76 m |
| --- | --- | --- |
| M20 fixed additional water, t | 61.214202 | 89.050573 |
| M20 SL residual downward thrust, kN | 0.413 | 0.457 |
| M20 altitude downward thrust, kN | 0 | 0 |
| P100 SL upward thrust required, kN | 350.526 | 77.500 |
| P100 altitude upward thrust required, kN | 350.939 | 77.957 |

M20 at sea level therefore has total onboard mass 277.448550 t, leaving only the explicitly charged downward-thrust requirement. At altitude it is neutral in this mass model. P100 has zero added ballast and an upward-force deficit; the conditional powered balance is not evidence of buoyant float. Unballasted M20 would need 873.745 kN downforce and the chosen water-shift schedule fails because there is no movable ballast. No such state is accepted as a free positive-margin operating case.

The wet ballast system has eight sagged 100 mm-bore, 5 mm-wall hose spans on separate 30 kN messengers, attached at the apices; eight 7 m branches go to the water bladders. Span is 14.472 m with 2 m sag, total ring hose 121.669 m plus 56 m branches. The parabolic self-weight reaction supplies 1.002 kN inward at each apex, included explicitly in the main cable equations. Messenger service tension is 1.497 kN. The estimate includes 1.395 t of fixed hose water; that water is already inside the 3 t equipment allocation and is not extra transferable ballast. Itemized wet system mass is 2.877 t, including eight 20 kg pumps, 16 valves, fittings/controls/mounts and 600 kg ground tackle. Eight assumed 5 L/s pumps at 20 m head and efficiency 0.65 require 12.070 kW. This is a settled trim schedule, not demonstrated gust response; hose pressure reactions, cavitation, transfer time, mooring and dynamic stability remain UNKNOWN.

For each module, `U*T = (H_k*e_x + R_ring*cos(phi), H_k*e_y + R_ring*sin(phi), W_k)`, where the columns of `U` are its three actual cable unit vectors. `W_k = g*(m_k + excess_mass/8)` includes its share of downforce or required powered lift, and `H_k=H*W_k/sum(W_k)`. Cable tensions must all be nonnegative; this is a unique three-cable solution, not an aggregate direction bound. The ring reaction has zero whole-system resultant/moment by symmetry. Internal bag weight is supported separately and is not used to create fictitious downward cargo load.

| 76 m M20 SL, 5 m/s | Water, t | Module mass, t | Horizontal thrust, kN | Inner T, kN | Outer - T, kN | Outer + T, kN |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 8.073 | 11.791 | 5.516 | 46.964 | 35.690 | 35.690 |
| 1 | 8.969 | 12.686 | 5.935 | 55.960 | 48.862 | 22.396 |
| 2 | 11.131 | 14.849 | 6.947 | 80.703 | 55.841 | 12.035 |
| 3 | 13.294 | 17.011 | 7.958 | 109.726 | 47.806 | 12.321 |
| 4 | 14.189 | 17.907 | 8.377 | 123.002 | 27.819 | 27.819 |
| 5 | 13.294 | 17.011 | 7.958 | 109.726 | 12.321 | 47.806 |
| 6 | 11.131 | 14.849 | 6.947 | 80.703 | 12.035 | 55.841 |
| 7 | 8.969 | 12.686 | 5.935 | 55.960 | 22.396 | 48.862 |

The 76 m benign 22.5-degree wind case has minimum tension 10.282 kN at sea level and 15.774 kN at altitude. All eight modules have nonnegative water and stay below 25 t. Force residuals are below 1e-6 N; whole pitch residuals are below 1e-6 N m. These are arithmetic tolerances, not measurement accuracy. The similarly trimmed P100 equations give the same cable reactions only because the required upward force removes its excess load; propulsion capability remains UNKNOWN and its gas budget remains FAIL.

| 76 m wind, m/s | SL minimum T, kN | Altitude minimum T, kN | SL water/module limits | Altitude water/module limits | SL / altitude membrane strip | SL / altitude positive pressure |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 33.938 | 33.925 | True | True | True / True | True / True |
| 5 | 12.035 | 16.817 | True | True | True / True | True / True |
| 10 | -92.686 | -55.840 | False | True | True / True | True / True |
| 20 | -1,115.077 | -717.308 | False | False | False / True | True / True |
| 30 | -4,960.786 | -3,126.991 | False | False | False / False | False / False |

The adverse values are signed formal solutions of the same fixed 5 m/s-sized construction. A negative tension proves that the represented three tension-only directions cannot close that node. Negative water/overloaded modules are additional failures; no fictional power rating is inferred from such a state. At 20 and 30 m/s, membrane/pressure limits add failures. A stronger cable alone cannot remove a direction-cone failure.

The propulsion proxy includes induced power, not just `H*wind/efficiency`. For an assumed 4 m rotor, it uses `v_i=(sqrt(V_ax²+2*F/(rho*A))-V_ax)/2` and `P=F*(V_ax+v_i)/0.70`. [NASA's simple propeller momentum model](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/propeller-thrust/) supports the axial-flow basis, not hardware ratings. Applying axial projection to tilted thrust ignores in-plane flow and remains an unqualified proxy, especially for P100. Rotor-body interference, low-speed losses and full vectoring clearance are unresolved.

| 76 m, 5 m/s | Sea-level shaft proxy, MW | Altitude shaft proxy, MW |
| --- | --- | --- |
| M20 with fixed ballast | 1.417 | 1.104 |
| P100 including required powered lift | 2.899 | 2.910 |

The 5 t energy allocation has no demonstrated endurance or discharge rating. Pressure blowers add up to 92.308 kW and trim pumps 12.070 kW when operated. These are explicit power demands; no mission duration is claimed.

## Pressure height, descent flow and thermal carry

For descent at 1 m/s with lifting-gas cooling of an additional 10 K/hour, the calculation includes both shrinking lifting gas **and compression of existing connected air**, including the outside manifold. With `beta_g=-L/T+g*p/(R_air*T*(p+1000))` and `beta_air` replacing +1000 by +1250:

```text
Q_internal = V_g*beta_g + (V_air + V_external_air)*beta_air + V_g*10/(3600*T)
Q_ambient_inlet = Q_internal*(p+1250)/p
```

| Diameter | SL inlet, m³/s | Altitude inlet, m³/s | Each of four blowers, m³/s | One out, m³/s | Three-blower power, kW |
| --- | --- | --- | --- | --- | --- |
| 70.575 | 18.712828 | 20.234952 | 8 | 24 | 73.846 |
| 76.000 | 23.370794 | 25.271808 | 10 | 30 | 92.308 |

The assumed pressure rating is 2 kPa with 0.65 blower efficiency, leaving an unverified allowance for valves/duct loss above the 1,250 Pa reference differential. Flow ratings and mass scaling are assumptions, not catalogue validation. The original 3-by-8 m³/s available capacity would fail the 76 m altitude demand; the repriced design supplies 3-by-10 m³/s through the common manifold.

At 2,500 m, the ideal zero-air limit is +14.310526 K superheat. Rigid duct/manifold volume makes a conservative earlier limit of +14.165745 K for 76 m (counting all charged duct length as a conservative rigid-air bound). +15 K is INVALID and is never credited as negative air mass or lift. The 30% connected-air capacity also bounds cold operation; the calculation does not assume arbitrary cooling is possible.

At +10 K with the same lifting inventory, inside air falls by 7.696572 t. The fixed M20 ballast then needs 75.478 kN downforce and a 2.811 MW shaft proxy at 5 m/s. P100's thermal margin is still -0.252856 t. No heating source, energy or thermal-control authority is credited. Changing payload from M20 to P100 does not recharge gas; it changes carried mass and the explicit water/force trim requirement.

## Sensitivity and conclusion

The following are raw 2,500 m mass margins, before any ballast or powered trim. Resizing only the named component does not repair compatibility or wind failures. The pure-helium row is a separate recharged comparison; all other thermal rows explicitly conserve lifting inventory.

| Case | M20, t | P100, t |
| --- | --- | --- |
| Nominal 76 m | 89.050573 | -7.949427 |
| skin floor 2mm | 59.436627 | -37.563373 |
| fabric work halved | 66.182033 | -30.817967 |
| seam efficiency 0p5 | 82.283529 | -14.716471 |
| bag floor 0p5mm | 84.218865 | -12.781135 |
| equipment plus 30t | 59.050573 | -37.949427 |
| pure helium recharged | 96.119793 | -0.880207 |
| same inventory hot 10k | 96.747144 | -0.252856 |

Arithmetic/conservation and the stated ideal-node force equations are reproducible. Physical confidence remains UNKNOWN. P100's negative nominal mass margin is a demonstrated FAIL. The most consequential mechanical unknown is simultaneous membrane/curtain stiffness and sag/fold/contact compatibility: finite straight clearance is smaller than an estimated deformation, and point-equilibrium alone cannot establish the loaded geometry. The shared bag-pressure field also prevents an everywhere-positive pressure claim for the full spherical design envelopes. The wind-direction and higher-wind membrane failures are retained, not converted to UNKNOWN.

The next justified design change is a priced, sag-compatible version of this three-anchor attachment and its bag/duct penetrations, with explicit stiffness/slack/contact properties. Mission propulsion/energy repricing must precede a positive payload claim. Increasing diameter again without these carried constraints would not resolve the demonstrated mechanisms.

Reproduce from the repository root:

```sh
python research/design-iterations/R3-I010/calculate.py
```

The program emits the entire mass ledger, geometry, per-module signed tensions, thermal cases and sensitivities as JSON. Its PASS label covers bookkeeping and selected scalar bounds only. Reproduction, derivative/vector cross-checks, documentation checks and governed-candidate custody are recorded separately; no public operational authority identifiers are embedded here.
