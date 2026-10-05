# The physics

This document states the model in the order a physicist would want it: what lifts the
vehicle, what the shell would have to be, what one delivery cycle costs, and where the
arithmetic fails. Every equation is the one in the code. Every constant is given with its
value, its provenance, and how much the headline figures move when it moves.

No such aircraft exists. Nothing here is validated against a built vehicle.
The energy sections and notation are regenerated from the model.
Earlier energy text and figures remain as dated history in the closure record.
The shell and buoyancy sections have their own analysis and validation limits.

The flight model assumes a hull that floats; no drawn hull does, as the [float case](FLOAT.md) and [ledger](FLOAT-LEDGER.md) explain.

The [simulator reference](../sim/README.md) names the modules that own the calculation.

---

<!-- energy:notation:start -->
## Energy notation

| Input | Value or source |
|---|---|
| Air density | Local ISA density at each force and power evaluation |
| Sea-level density kg/m³ | 1.225 |
| Frontal drag coefficient | 0.05 |
| Propulsion efficiency | 0.7 |
| Lumped pump efficiency | 0.75 |
| Pump head m | P100: 300; P1000: 300; P10000: 300 |
| Displacement | CLASSES[*].dispM3 |
| Dry-mass target | Equal to payload by assumption |
| Water density kg/m³ | 1000 |
| Gravity m/s² | 9.81 |
<!-- energy:notation:end -->

## 1. Lift and the mass ledger

The hull is a vacuum vessel. It lifts the mass of the air it displaces, with nothing
inside to subtract:

> **L = ρ(h) V**

`physics.js → ledger(cls, h)` evaluates this at the altitude it is given, in metres above
mean sea level, and calls the result `liftT`. There is no default altitude: a caller that
has not decided where the ship is gets a thrown error rather than a sea-level answer, which
is the shape the old Defect 1 took. Density comes from `sim/atmosphere.js`, the ISA
troposphere, anchored at ρ_SL so the page's sea-level dial scales the whole column.

The dry mass is set equal to the payload — one tonne of vehicle per tonne of water — and the
model is explicit that this is the ledger's bet, not a mass estimate. The three classes are
assumed to be geometrically similar capsules with fineness ratio 2; their configured
dimensions are listed below.

<!-- atmosphere:physics:start -->
**FAIL-SAFE FLOAT-UP SETS THE DISPLACEMENT.** The requirement, decided 2026-08-09, is that a
hull be positively buoyant at its working altitude *while fully loaded with water and unable
to drop it*. Nitrogen ballast is excluded from that mass because it vents to atmosphere in
seconds; water is the load a ship can be stuck with. In the reference atmosphere, the working altitude
h_t + `ALT.cruise` = 2,500 m MSL is the thinnest air in the nominal cycle, so sizing there
covers that reference cycle. At the working-altitude reference pressure of 74682.51 Pa,
loaded neutrality occurs at P-100: 0.909091 kg/m³, reference temperature +14.29 K; P-1000: 0.909091 kg/m³, reference temperature +14.29 K; P-10000: 0.909091 kg/m³, reference temperature +14.29 K. Float-up requires air denser than these boundaries;
at the same pressure, warmer air beyond them removes the margin. ISA+15 K gives P-100 -0.25%; P-1000 -0.25%; P-10000 -0.25%.
These are fixed-pressure model scenarios, not an established weather envelope; the
[generated boundary record](../research/analysis/loaded-atmosphere.json) holds the calculation.
At ρ_work = 0.95686 kg/m³ a loaded tonne needs 2,194.7 m³ of
displacement with a 5% margin; the classes carry 2,200 m³ per tonne of payload:
<!-- atmosphere:physics:end -->

| | displacement | L at ρ_work | dry | payload | float-up margin | surplus, empty |
|---|---:|---:|---:|---:|---:|---:|
| P-100 | 220,000 m³ | 210.5 t | 100 t | 100 t | +5.25% | 110.5 t |
| P-1000 | 2,200,000 m³ | 2,105.1 t | 1,000 t | 1,000 t | +5.25% | 1,105.1 t |
| P-10000 | 22,000,000 m³ | 21,050.9 t | 10,000 t | 10,000 t | +5.25% | 11,050.9 t |

The margin is identical for all three classes because m_dry = m_pay for all three, so no
class needs an exception to the fail-safe requirement and none is granted one.

The first study increased displacement from 180,000 / 1.8×10⁶ / 1.8×10⁷ m³ after accounting for altitude.
Its spheroids grew from 177 × 44 to 190 × 47 m, 380 × 95 to 404 × 102 m, and 820 × 205 to 876 × 219 m.
Those are historical dimensions, replaced by capsules on 2026-08-13.

Correction, 2026-10-02: the simulation now uses the configured capsule dimensions below.
These are fleet assumptions, not structurally checked ships.

<!-- fleet-dimensions:start -->
| Class | Capsule length × diameter (m) |
| --- | ---: |
| P-100 | 110 × 55 |
| P-1000 | 238 × 119 |
| P-10000 | 512 × 256 |
<!-- fleet-dimensions:end -->

**Lift is not a constant, and the ledger no longer pretends it is.** The same envelope in
the same cycle:

| point in the cycle | altitude MSL | ρ | P-100 lift | net, loaded | surplus, empty |
|---|---:|---:|---:|---:|---:|
| ground | 1,000 m | 1.1116 | 244.6 t | +44.6 t | 144.6 t |
| source hold, 300 m AGL | 1,300 m | 1.0793 | 237.4 t | +37.4 t | 137.4 t |
| drop run, 450 m AGL | 1,450 m | 1.0633 | 233.9 t | +33.9 t | 133.9 t |
| cruise ceiling, 1,500 m AGL | 2,500 m | 0.9569 | 210.5 t | +10.5 t | 110.5 t |

14% of the lift is spent on the climb. The net force stays positive throughout, which is
what the fail-safe requirement bought.

**The break-even density is identical for all three classes**, because the ratio
(m_dry + m_pay)/V is identical:

> ρ* = 2 m_pay / V = **0.90909 kg/m³** loaded, **0.45455 kg/m³** empty

0.90909 kg/m³ is ISA density at 3,000 m — 500 m above the cruise ceiling. It used to be
1.1111 kg/m³, which is 1,005 m, below the drop run. That is the whole of the fix, in one
number.

---

## 2. Why the vacuum shell is the hard part

A gas envelope trades lift for the mass of the lifting gas. A vacuum envelope keeps all of
the lift and must instead survive one atmosphere of external pressure without collapsing.
That is a stability problem, not a strength problem, and it does not scale kindly.

Be honest about the size of that trade: the gas tax is small — hydrogen costs 7% of the
displaced-air mass and helium 14% — while the structure that survives the atmosphere costs
this project's *target* design 47% of it. **Vacuum does not win on lift**; the break-even
structure against hydrogen is 0.067 kg/m³, six times below even the deepest hierarchy
level. The decision to build vacuum anyway is the mission's — no feedstock, no gas
logistics tail, crush-safe fixed displacement, the array as airframe — and it is worked,
with the market numbers, in `research/analysis/helium.md`. That is the challenge this
document exists to map.

**THE HULL IS NOT ONE ENVELOPE. It is many permanently sealed vacuum cells**, and this
document did not say so until 2026-08-10, which is long enough for it to have caused a
mistake — an analysis proposed ballasting by admitting air, which a sealed-cell hull cannot
do, and the retraction is at `research/analysis/air-ballast.md`. The model has no geometry
below `dispM3`, so nothing in the code implies it either.

**Nothing lives inside a cell.** Machinery sits in ambient-pressure bays *within the hull*,
surrounded by cells, bolted to a structure the cells are themselves part of. The cells pull
up on that structure; they are the lift elements and the airframe at the same time. The
intended cell is a space-filling near-spherical solid whose walls are printed to interlock and
to carry services between neighbours — lighter-than-air building blocks that are stronger
assembled than alone, so the array is the substructure and much of the superstructure too.

Four consequences, and they are not small:

- **There is no valve, and cracking a cell open is irreversible in the field.** Nothing aboard
  can expel an atmosphere once it is admitted. Ballast therefore has to be *made* — which is
  what the cryogenic plant is for, and why it cannot be deleted.
- **The buckling radius is the cell's, not the hull's.** Every vacuum design in the literature
  is a sphere because a sphere is optimal against external pressure, and the first study used
  fineness-4 spheroids. The current configured hulls are capsules. On a monocoque that penalty is severe enough to be fatal
  (see `research/analysis/mass-budget.md`). With small cells the outer body becomes a fairing
  and the penalty largely goes away. **This is the reason the shape of the ship and the shape
  of its pressure vessels are allowed to differ.**
- **It costs packing.** Space that is not cell — machinery bays, structure, and any gap between
  cells — sits at ambient and lifts nothing, so effective lift scales by the packing fraction.
  A space-filling cell drives the geometric part of that to 1; the bays are a real deduction.
  The number has never been chosen.
- **MOST WALL AREA CARRIES NO PRESSURE AT ALL.** An interior wall has vacuum on both sides. At
  2 m cells the first study’s dated 190 × 47 m spheroid reference has
  ~330,000 m² of interior wall against 22,592 m² of array boundary —
  **93.6% of the wall area sits at zero differential** in normal operation, and the atmosphere
  is carried only at the boundary. That is a fundamentally different problem from N independent
  pressure vessels, which is what the entire literature models and what
  `research/analysis/mass-budget.md` costed. **The whole internal structure is therefore sized
  by the BREACH case** — one flooded cell puts an atmosphere into its own walls in tension
  (0.162 kg/m³, scale-free, clears the wall with 5.9× margin) and against its neighbours' walls
  in compression (3.59 kg/m³ monolithic, which fails by 3.7× and is exactly why a lattice or
  sandwich is needed rather than a skin). Breach stops being a safety test and becomes the
  sizing load case for the ship.

  Correction, 2026-10-02: 0.162 kg/m³ and 3.59 kg/m³ are hand figures with no generator.
  Their load and material basis remains an [open question](OPEN-QUESTIONS.md#breach-hand-figures); they do not establish ship sizing.

Everything below treats the shell as a single sphere, because that is what the sources do and
because it is the conservative reading for stability. The cellular case is better, and nobody
has worked it.

Take a spherical shell of radius R, wall thickness t, material density ρ_m, Young's modulus
E and Poisson's ratio ν. Net lift is positive when

> 4πR²tρ_m < (4/3)πR³ρ_air  ⟹  σ = tρ_m < ρ_air R / 3

where σ is areal density. Classical elastic buckling of a complete sphere under external
pressure gives

> p_cr = 2E t² / (R² √(3(1−ν²)))

Requiring p_cr ≥ p_atm and combining the two eliminates both R and t:

> **E / ρ_m² ≥ 9 p_atm √(3(1−ν²)) / (2 ρ_air²) ≈ 5.0 × 10⁵ Pa·m⁶/kg²**

with p_atm = 101,325 Pa, ν = 0.3, ρ_air = 1.225. No safety factor, no imperfection
knockdown, no joints, no penetrations. Against that:

| Material | E (GPa) | ρ_m (kg/m³) | E/ρ_m² | fraction of requirement |
|---|---:|---:|---:|---:|
| aluminium 6061 | 70 | 2,700 | 9,602 | 0.02× |
| silicon carbide | 410 | 3,210 | 39,790 | 0.08× |
| carbon/epoxy, unidirectional | 150 | 1,600 | 58,594 | 0.12× |
| boron carbide | 460 | 2,520 | 72,436 | 0.14× |
| beryllium | 287 | 1,850 | 83,857 | 0.17× |
| diamond | 1,050 | 3,510 | 85,227 | 0.17× |

The best material anyone has is short by a factor of about six, and diamond is one of
them. This is the standard result for monocoque vacuum balloons and it is why the concept
is not simply an engineering exercise. Any workable design has to escape the *monocoque*
part of the derivation — a sandwich, isogrid or internally braced structure whose
stability does not scale as t²/R² — and the model makes no attempt to describe such a
structure or to demonstrate that one exists.

What the model does instead is assert an areal density and get on with the arithmetic:

| | wetted area | dry allowance | implied σ | was, before the 2026-08-09 resize |
|---|---:|---:|---:|---:|
| P-100 | 19,007 m² | 100 t | 5.26 kg/m² | 5.07 kg/m² on 19,707 m² |
| P-1000 | 88,976 m² | 1,000 t | 11.24 kg/m² | 10.94 kg/m² on 91,372 m² |
| P-10000 | 411,775 m² | 10,000 t | 24.29 kg/m² | 23.50 kg/m² on 425,477 m² |

**2026-10-02 correction:** the table now prices each nominal capsule on its own surface.
The former spheroid areas and allowances are retained in
[the regeneration audit](audit/26-10-02-analysis-regeneration.md).

σ rises with size because dry mass scales as V while area scales as V^(2/3). The lift
budget allows at most σ_max = ρ_work V / S_wet — 11.08, 23.66 and 51.12 kg/m² for the three
classes — and the assumed values are 47.5% of that in every case, identically, because
m_dry = m_pay = L/2.1051 by construction. So the shell, the machinery, the batteries and the
rotors together are given a little under half of what buoyancy would permit. That is a
statement about the lift budget only. It says nothing about whether such a shell can be
built.

**Fail-safe float-up made this harder, and that is the price of it.** Growing the hull 22%
added 14% to the wetted area without adding anything to the dry allowance, so every square
metre of shell now has to come in 13% lighter than it did. The requirement is a safety
property and the areal density is the hardest unsolved problem in the project; buying the
first with the second is a deliberate trade and it is stated rather than netted off.

---

<!-- energy:physics:start -->
## 3. Storage inside the dry-mass target

## What this model leaves out

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

Generated by `node research/analysis/energy-omissions.mjs`. These loads are not silently absorbed into a closing claim.

| Class | Beam-wind side force, t | Cable mass, t (floor / credible / demonstrated) | Battery mass, t (same cases) | Dry target, t | Bag, t | Cable, m | Pendulum period, s | Day-average solar, MW |
|---|---:|---|---|---:|---:|---:|---:|---:|
| P100 | 29.709 | 0.644 / 1.431 / 2.146 | 40.000 / 66.667 / 134.228 | 100 | 125 | 350 | 37.530 | 0.207 |
| P1000 | 139.077 | 11.036 / 24.525 / 36.788 | 240.000 / 400.000 / 805.369 | 1000 | 1250 | 600 | 49.138 | 0.967 |
| P10000 | 643.635 | 155.096 / 344.658 / 516.987 | 4000.000 / 6666.667 / 13422.819 | 10000 | 12400 | 850 | 58.486 | 4.476 |

| Class | Design displacement, m³ | Geometric capsule, m³ | Difference from design, % |
|---|---:|---:|---:|
| P100 | 220000.000 | 217784.366 | -1.007 |
| P1000 | 2200000.000 | 2205867.973 | 0.267 |
| P10000 | 22000000.000 | 21961324.389 | -0.176 |

Buoyancy uses the declared design displacement. The capsule comparison is a geometry difference, not a change to lift or the class constants.

The beam wind is 10 m/s, with an unverified side-drag coefficient of 1 and local source density. No horizontal actuator or station-keeping power is priced.

Cable and battery estimates bind to `research/analysis/mass-budget.json`. Cable mass is not added to the energy model's dry target.

Storage cases use 500, 300, 149 Wh/kg, respectively. Their source qualifications remain in the mass-budget record.

The bag is a moving pendulum; its ideal small-angle period is shown, but swing, damping and winch transients are unpriced. The steady hoist bill does not bound pickup shock.

Solar is credited at its day average at every instant, including night. Dry mass is a target equal to payload, not an assembled mass ledger; see [the float analysis](../float/).

## 4. The prescribed delivery cycle

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

| Class | km | Basis | As drawn | Minutes | Supplied MWh | kWh/planned tonne | Battery-hours quotient | Profile note |
|---|---|---|---|---|---|---|---|---|
| P100 | 15 | record | does not close | 34.196 | 8.192 | 81.923 | 1.418 |  |
| P100 | 15 | favourable | does not close | 34.196 | 6.402 | 64.017 | 1.824 |  |
| P100 | 60 | record | closes | 104.784 | 20.521 | 205.214 | 1.742 | quasi-static closure; dynamic profile unresolved; quasi-static closure; exceeds nominal storage in one ideal cycle |
| P100 | 60 | favourable | closes | 104.784 | 14.764 | 147.639 | 2.444 | quasi-static closure; dynamic profile unresolved |
| P1000 | 15 | record | does not close | 35.362 | 62.314 | 62.314 | 1.149 |  |
| P1000 | 15 | favourable | does not close | 35.362 | 61.355 | 61.355 | 1.167 |  |
| P1000 | 60 | record | does not close | 93.116 | 141.533 | 141.533 | 1.334 |  |
| P1000 | 60 | favourable | does not close | 93.116 | 142.484 | 142.484 | 1.325 |  |
| P10000 | 15 | record | does not close | 45.512 | 694.378 | 69.438 | 2.198 |  |
| P10000 | 15 | favourable | does not close | 45.512 | 766.285 | 76.629 | 1.990 |  |
| P10000 | 60 | record | does not close | 94.381 | 1113.855 | 111.385 | 2.846 |  |
| P10000 | 60 | favourable | does not close | 94.381 | 1386.308 | 138.631 | 2.283 |  |

| Class | km | Basis | Profile | Delivered t | Kept t | Minutes | MWh | kWh/delivered tonne | Profile note |
|---|---|---|---|---|---|---|---|---|---|
| P100 | 15 | record | as drawn: does not close | 100.000 | 0.000 | 34.196 | 8.192 | 81.923 |  |
| P100 | 15 | record | cheapest feasible profile found in the stated space | 65.000 | 35.000 | 34.914 | 5.201 | 80.021 | quasi-static closure; hull-only sampled screen does not validate dynamics |
| P100 | 15 | favourable | as drawn: does not close | 100.000 | 0.000 | 34.196 | 6.402 | 64.017 |  |
| P100 | 15 | favourable | cheapest feasible profile found in the stated space | 65.000 | 35.000 | 34.914 | 3.793 | 58.359 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | record | as drawn: closes | 100.000 | 0.000 | 104.784 | 20.521 | 205.214 | quasi-static closure; dynamic profile unresolved; quasi-static closure; exceeds nominal storage in one ideal cycle |
| P100 | 60 | record | cheapest feasible profile found in the stated space | 98.382 | 1.618 | 64.420 | 14.100 | 143.315 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | favourable | as drawn: closes | 100.000 | 0.000 | 104.784 | 14.764 | 147.639 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | favourable | cheapest feasible profile found in the stated space | 100.000 | 0.000 | 75.440 | 11.263 | 112.630 | quasi-static closure; dynamic profile unresolved |
| P1000 | 15 | record | as drawn: does not close | 1000.000 | 0.000 | 35.362 | 62.314 | 62.314 |  |
| P1000 | 15 | record | cheapest feasible profile found in the stated space | 215.591 | 784.409 | 25.616 | 26.489 | 122.866 | quasi-static closure; dynamic profile unresolved |
| P1000 | 15 | favourable | as drawn: does not close | 1000.000 | 0.000 | 35.362 | 61.355 | 61.355 |  |
| P1000 | 15 | favourable | cheapest feasible profile found in the stated space | 215.591 | 784.409 | 25.616 | 21.539 | 99.905 | quasi-static closure; dynamic profile unresolved |
| P1000 | 60 | record | as drawn: does not close | 1000.000 | 0.000 | 93.116 | 141.533 | 141.533 |  |
| P1000 | 60 | record | cheapest feasible profile found in the stated space | 270.506 | 729.494 | 74.049 | 68.866 | 254.583 | quasi-static closure; dynamic profile unresolved |
| P1000 | 60 | favourable | as drawn: does not close | 1000.000 | 0.000 | 93.116 | 142.484 | 142.484 |  |
| P1000 | 60 | favourable | cheapest feasible profile found in the stated space | 270.506 | 729.494 | 74.049 | 56.659 | 209.457 | quasi-static closure; dynamic profile unresolved |
| P10000 | 15 | record | as drawn: does not close | 10000.000 | 0.000 | 45.512 | 694.378 | 69.438 |  |
| P10000 | 15 | record | cheapest feasible profile found in the stated space | 2626.200 | 7373.800 | 23.667 | 200.116 | 76.200 | quasi-static closure; dynamic profile unresolved |
| P10000 | 15 | favourable | as drawn: does not close | 10000.000 | 0.000 | 45.512 | 766.285 | 76.629 |  |
| P10000 | 15 | favourable | cheapest feasible profile found in the stated space | 2626.200 | 7373.800 | 23.667 | 183.419 | 69.842 | quasi-static closure; dynamic profile unresolved |
| P10000 | 60 | record | as drawn: does not close | 10000.000 | 0.000 | 94.381 | 1113.855 | 111.385 |  |
| P10000 | 60 | record | cheapest feasible profile found in the stated space | 3009.297 | 6990.703 | 66.573 | 439.851 | 146.164 | quasi-static closure; dynamic profile unresolved |
| P10000 | 60 | favourable | as drawn: does not close | 10000.000 | 0.000 | 94.381 | 1386.308 | 138.631 |  |
| P10000 | 60 | favourable | cheapest feasible profile found in the stated space | 3009.297 | 6990.703 | 66.573 | 397.762 | 132.178 | quasi-static closure; dynamic profile unresolved |

Cycle durations and supplied energy are model outputs. A cycle that does not close supplies no justified delivery rate.

## 5. Pumping energy

Pump power is water density times gravity, flow and head, divided by pump efficiency.
The electrical fill energy is delivered water times gravity and head, divided by the same efficiency.

| Class | Head m | Pump MW | Ideal MWh | Electrical MWh |
|---|---|---|---|---|
| P100 | 300 | 1.962 | 0.082 | 0.109 |
| P1000 | 300 | 11.772 | 0.818 | 1.090 |
| P10000 | 300 | 58.860 | 8.175 | 10.900 |

The lumped pump efficiency is 0.75; it covers the pump, motor, drive and hose losses. Hose mass and detailed friction are not separately modelled.

## 6. Drag and cruise power

Zero-lift drag power is dynamic pressure times frontal area and drag coefficient, times airspeed, divided by propulsion efficiency.
Induced drag for aerodynamic hold-down is additional.

| Class | Local density kg/m³ | Balanced cruise drag MW | Volumetric drag coefficient |
|---|---|---|---|
| P100 | 0.956859 | 1.269 | 0.03260 |
| P1000 | 0.956859 | 10.843 | 0.03288 |
| P10000 | 0.956859 | 82.829 | 0.03278 |

The frontal drag coefficient is 0.05. This hull-only assumption does not price rotor installations, fins, the hose pod or their interference.

## 7. Vertical force and rotor pricing

## Force and energy rules

The ledger subtracts all onboard weight from local buoyant lift.
Its owners are the cable-carried water, downward rotors, permitted aerodynamic downforce and signed vertical drag.
Unheld force stays visible.

Surplus is local displaced-air mass minus dry mass, water and nitrogen.
The signed residual is surplus minus bag support, rotor thrust, aerodynamic downforce and vertical drag.

Glauert momentum pricing solves T = 2 ρ A v_i √(V² + (v_c + v_i)²), then P = T (v_c + v_i) / η.
The vertical drag owner is ρ C_D S v_z |v_z| / (2 g), with upward velocity positive.
The favourable downforce cap is C_L,max q S, and its induced drag is T_aero² / (q π b² e).

The force tolerance is 0.000001 times the larger of unity and absolute surplus.
Constraint sampling uses 1024 intervals per phase, plus seams and internal profile joins.
Energy uses 96 midpoint intervals per phase; constraint peaks are checked separately.

The unverified broadside coefficient is 1; the favourable lift coefficient is 1.
The reported lift-coefficient sweep is 0.5, 1, 1.5; rotor-efficiency endpoints are 0.55, 0.7.
Bag water is credited when carried; its 15 m lift at efficiency 0.85 remains priced.

A cycle closes only when the residual and gross bus draw meet the stated tolerances at every checked instant.
Bus saturation alone is a note.
The rotors have no upward authority.

Record basis credits no aerodynamic hold-down.
Favourable basis chooses the least-power split between capped rotors and capped aerodynamic downforce.
Induced drag is charged to propulsion, and all force and power terms use local ISA density.

Rotor efficiency represents figure of merit times drive efficiency.
Hold-down descent is priced as climb, on the conservative side; climb against hold-down thrust is priced as level flight, with no bound claimed.

The installed thrust cap is an unverified hover surrogate at the battery-plus-generator rating.
A feasible result is quasi-static.
Feasible means quasi-static force and bus closure at every checked instant. Battery hours are reported; they do not determine feasibility. These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.
The [served-candidate inertia diagnostic](../research/analysis/energy-served-inertia.json) checks signed vertical hull demand against rotor authority in both directions at published and captured routes.
The feasible-profile records also contain that comparison for every phase.

## Signed demand, added mass and suspended-load limits

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

With upward acceleration positive and forces in tonnes-force:

`I = (m_onboard + C * m_displaced_air) * a_z / g`

`T_required = T_quasi + unheld - I`

The sampled rotor demand is accepted only inside `0 <= T_required <= T_available`.
A negative required thrust is an upward-authority shortage; a demand above available thrust is a downward-authority shortage.
The screen fixes aerodynamic, bag and drag owners and other electrical loads at the quasi-static values.
Buoyancy is already in the ledger. Shedding hold-down supplies an upward increment; it is not additional buoyancy.
The samples, central second difference and cutoff remain unchanged; a gap-free sample is not continuous-time control evidence.

| Phase | Vertical acceleration and first allocation | Still unresolved |
|---|---|---|
| SOURCE_APPROACH | Downward into descent: add downward thrust; upward braking: shed it | When rotors are zero and the bag carries the surplus, braking needs a different pickup, tension or trajectory schedule |
| WATER_FILL | Constant hull altitude; no hull acceleration demand | Water and nitrogen flow and load transfer |
| OUTBOUND_TRANSIT | Both signs in climb and letdown; shed for upward acceleration, add for downward acceleration | Force allocation follows acceleration, not velocity; aerodynamic response is unvalidated |
| WATER_RELEASE | Upward while starting the rise: shed; downward while stopping it: add | A rising hull can need additional downward force |
| BUOYANCY_ESCAPE | Upward then downward: shed then add | No hanging-water owner is credited |
| RETURN_TRANSIT | Either sign according to endpoint geometry; apply the signed equation | Short-route joins, actuator response and load control |

### Geometry-specific added mass remains open

The coefficients 0.70 and 1.00 are a sensitivity pair for transverse motion of a horizontal capsule of length/diameter 2.
The lower value rounds Munk's 0.702 transverse coefficient for a prolate spheroid of that fineness: [NACA Report 184 (1924)](https://ntrs.nasa.gov/citations/19930091249), Table I, printed p.20 / PDF p.21.
It is a potential-flow surrogate, not a measured capsule coefficient; neither endpoint establishes a physical limit.
The configured capsule has about 25% more volume than the spheroid on the same axes.
Added mass uses local displaced-air mass, not surplus lift. Attitude coupling requires a mass tensor and separate validation.

### Hull and load need separate equations

The current screen covers the hull alone. A minimum load model treats a rigid load on a taut, inextensible cable with prescribed winch length.
In SI units, with upward positive, a vertical schematic at fixed instantaneous mass is:

`(m_h + A_h) * z_h'' = B_h - m_h*g - T - F_rotor - F_aero - D_h + F_flow,h`

`(m_b + A_b) * z_b'' = T + B_b - m_b*g - D_b + F_flow,b`

Here B denotes buoyancy, T tensile cable force, A added mass and F_flow the separately required inventory/flow momentum terms.
The hull feels downward cable tension; bag weight already credited in the quasi-static ledger must not be charged twice.
For the straight taut-cable limit, `z_b = z_h - ell(t)` and `a_b = a_h - ell''`.
For a rigid airborne bag with no other force, `T = m_b * (g + a_h - ell'')`.
Bag buoyancy, water added mass and flow momentum must be supplied through immersion and pickup; dry-air load does not describe an immersed bag.

For peak loads use a one-sided elastic cable with stiffness k, damping c and unloaded winch length ell_0:
`T = 0` when slack; in extension, `T = max(0, k*(d-ell_0) + c*(d'-ell_0'))`.
Lateral motion needs pendulum coordinates: `r_b = r_h + ell*q(theta,phi)`, with q a downward-directed unit vector, and the separate body equations.
Unknown inputs are bag geometry, shell mass and immersion; cable stiffness, damping, distributed mass and slack; initial swing, flow history and winch speed ramps.
No snatch factor or assumed value closes these equations.
This treatment follows [Cicolani and Kanning, NASA TP-3280 (1992)](https://ntrs.nasa.gov/citations/19930003627), section 3, eqs.9b and 10 (PDF pp.14 and 16), and Figure 3 (printed p.15 / PDF p.23). No suspension parameters from another aircraft are transferred.

### Dated withdrawn measurement

Dated measurement at landing 16, 2026-10-05: absolute inertial force minus the additional downward rotor reserve at the same samples and coefficients. Withdrawn because it misses upward authority that cannot be obtained by shedding the existing downward thrust. Recomputed here solely to preserve that measurement.

| Population | Withdrawn absolute / signed | Reason |
|---|---|---|
| candidates | 284 / 354 | Signed demand must fit the authority in its own direction; profiles and verdicts are unchanged |
| capturedMissions | 16 / 21 | Signed demand must fit the authority in its own direction; profiles and verdicts are unchanged |


## 8. Nitrogen storage and recovery

Nitrogen is storage, not an energy source. Recovery is bounded by the stored nitrogen and the generator rating.

Liquefaction costs 0.45 MWh per tonne in this model; round-trip recovery is 0.2. Solar is 45 W/m² as a day average.

| Class | Tank t | Tank fill MWh | Ground-surplus t | Ground-surplus MWh | Solar days: ground / tank | Tank days at rated plant |
|---|---|---|---|---|---|---|
| P100 | 155 | 69.750 | 144.561 | 65.053 | 58.189 / 62.390 | 0.484 |
| P1000 | 1550 | 697.500 | 1445.613 | 650.526 | 162.233 / 173.948 | 0.969 |
| P10000 | 15500 | 6975.000 | 14456.134 | 6505.260 | 183.696 / 196.960 | 2.906 |

Solar-only days subtract hotel load and assume the day-average sun throughout. Tank capacity and ground-surplus ballast are different masses; their energy bills must not be interchanged.

## 9. Cycle energy and endurance

## Necessary stored energy, ideal accounting

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

Ideal, lossless chronological accounting with nominal class storage fully usable and the plan initial nitrogen inventory charged. No losses, health, state-of-charge window, reserve, external recharge or thermal limit. This is not an endurance rule, a mission-completion verdict or a battery model. Solar and nitrogen recovery are the existing bus inputs, not a promised recharge system.

Integrate the existing drawAt electrical.batteryPowerMW at 2000 midpoint samples per phase, in PHASES order. Record cumulative draw at every phase end; interpolate the first nominal-storage crossing inside its sample.

| Captured mission or printed profile | Class / km / basis | Draw MWh | Nominal storage MWh | First empty min | Shortage MWh | Pages |
|---|---|---|---|---|---|---|
| exercise mission 11 (zero-based) | P100 / 13.981185 / record | 41.6 | 20 | 127.9 | 21.6 | index.html |
| exercise mission 12 (zero-based) | P100 / 9.689204 / record | 58.9 | 20 | 169.5 | 38.9 | index.html |
| fullDeliveryBest | P100 / 15.000000 / record | 42.0 | 20 | 129.3 | 22.0 | index.html; concept/index.html |
| fullDeliveryBest | P100 / 15.000000 / favourable | 37.8 | 20 | 123.9 | 17.8 | index.html; concept/index.html |
| asDrawn | P100 / 60.000000 / record | 20.1 | 20 | 104.7 | 0.1 | index.html; concept/index.html |
| ready selector | P1000 / 400.000000 / record | 330.5 | 120 | 233.1 | 210.5 | concept/energy-analysis.html |

Of 32 captured cycles, 2 exceed nominal storage; every other captured cycle stays inside it for one ideal cycle. The full JSON records cumulative draw in phase order and each printed profile, including every shortage found. Initial nitrogen is charged storage, not free energy. The 400 km P1000 ready-selector result is printed on concept/energy-analysis.html; it is outside the worked-example slider range.

Records: `research/analysis/energy-necessary.json`; generator: `research/analysis/energy-necessary.mjs`. No operational horizon or completion gate is added.

| Class | km | Basis | As drawn | Minutes | Supplied MWh | kWh/planned tonne | Battery-hours quotient | Profile note |
|---|---|---|---|---|---|---|---|---|
| P100 | 15 | record | does not close | 34.196 | 8.192 | 81.923 | 1.418 |  |
| P100 | 15 | favourable | does not close | 34.196 | 6.402 | 64.017 | 1.824 |  |
| P100 | 60 | record | closes | 104.784 | 20.521 | 205.214 | 1.742 | quasi-static closure; dynamic profile unresolved; quasi-static closure; exceeds nominal storage in one ideal cycle |
| P100 | 60 | favourable | closes | 104.784 | 14.764 | 147.639 | 2.444 | quasi-static closure; dynamic profile unresolved |
| P1000 | 15 | record | does not close | 35.362 | 62.314 | 62.314 | 1.149 |  |
| P1000 | 15 | favourable | does not close | 35.362 | 61.355 | 61.355 | 1.167 |  |
| P1000 | 60 | record | does not close | 93.116 | 141.533 | 141.533 | 1.334 |  |
| P1000 | 60 | favourable | does not close | 93.116 | 142.484 | 142.484 | 1.325 |  |
| P10000 | 15 | record | does not close | 45.512 | 694.378 | 69.438 | 2.198 |  |
| P10000 | 15 | favourable | does not close | 45.512 | 766.285 | 76.629 | 1.990 |  |
| P10000 | 60 | record | does not close | 94.381 | 1113.855 | 111.385 | 2.846 |  |
| P10000 | 60 | favourable | does not close | 94.381 | 1386.308 | 138.631 | 2.283 |  |

Battery hours divide usable storage by the modelled energy deficit. They are reported, but do not gate the force-and-bus feasibility verdict. On an infeasible row this is an accounting quotient, not demonstrated endurance.
Every phase draws from the same ledger. The phase and channel integrals are stored in `energy-documents.json`.

## 10. Sensitivity

These sweeps change one input at a time around the prescribed P-10000 balanced profile at the worked distance.
All displayed energy changes are supplied-effort changes when the row is infeasible.

| Basis | Input | Energy change at −20% | Energy change at +20% | Verdict at −20% / +20% |
|---|---|---|---|---|
| record | propEta | 4.6% | -4.1% | does not close / does not close |
| record | Cd | -0.6% | 0.6% | does not close / does not close |
| record | rhoAir | 0.0% | 0.0% | does not close / does not close |
| record | pumpEta | 0.2% | -0.1% | does not close / does not close |
| record | hoseMul | -0.1% | 0.2% | does not close / does not close |
| record | rhoSL | -33.6% | 28.0% | does not close / does not close |
| record | rtLN2 | 0.0% | -0.0% | does not close / does not close |
| record | eLN2 | -0.0% | 0.0% | does not close / does not close |
| record | solarWPerM2 | -0.0% | 0.0% | does not close / does not close |
| record | cruiseKph | 8.2% | -4.0% | does not close / does not close |
| record | anchorBagT | 3.5% | -1.4% | does not close / does not close |
| record | dropKm | 0.6% | -0.9% | does not close / does not close |
| record | fillM3s | 15.7% | -10.7% | does not close / does not close |
| record | dispM3 | -36.4% | 29.9% | does not close / does not close |
| record | diskM2 | 4.0% | -3.4% | does not close / does not close |
| record | battMW | -15.2% | 14.0% | does not close / does not close |
| record | anchorM | 1.5% | -0.6% | does not close / does not close |
| record | solarM2 | -0.0% | 0.0% | does not close / does not close |
| favourable | propEta | 4.9% | -7.1% | does not close / does not close |
| favourable | Cd | -0.2% | 0.2% | does not close / does not close |
| favourable | rhoAir | 0.0% | 0.0% | does not close / does not close |
| favourable | pumpEta | 0.2% | -0.1% | does not close / does not close |
| favourable | hoseMul | -0.1% | 0.1% | does not close / does not close |
| favourable | rhoSL | -41.5% | 25.4% | does not close / does not close |
| favourable | rtLN2 | 0.0% | -0.0% | does not close / does not close |
| favourable | eLN2 | -0.0% | 0.0% | does not close / does not close |
| favourable | solarWPerM2 | -0.0% | 0.0% | does not close / does not close |
| favourable | cruiseKph | 6.5% | -4.1% | does not close / does not close |
| favourable | anchorBagT | 3.2% | -1.3% | does not close / does not close |
| favourable | dropKm | 0.6% | -0.7% | does not close / does not close |
| favourable | fillM3s | 14.1% | -9.5% | does not close / does not close |
| favourable | dispM3 | -46.0% | 26.8% | does not close / does not close |
| favourable | diskM2 | 2.5% | -2.9% | does not close / does not close |
| favourable | battMW | -15.9% | 11.1% | does not close / does not close |
| favourable | anchorM | 0.8% | -0.5% | does not close / does not close |
| favourable | solarM2 | -0.0% | 0.0% | does not close / does not close |

The old fixed-density input has no effect because the force and power laws now use local ISA density. Drop distance can change the force-price integral even when metering fixes release time.

## 11. Corrections and remaining limits

Earlier energy figures are retained beside current values in [the closure document](ENERGY-CLOSURE-2026-10.md).
The former unowned aerodynamic share, phase power discounts, split densities and silent bus overdraw have been removed.
Local-density force balance leaves the named endurance example infeasible; the generated unheld table records every failing phase.

## What the profile search means

The prescribed profile is retained as "as drawn".
The result is the cheapest feasible profile found in the stated space, not a global optimum.

Cruise speed multipliers: 0.5, 0.75, 1, 1.25, 1.5.
Modes: rapid, balanced, endurance.

| Independent parameter | Searched values |
|---|---|
| climbRateMps | 0.5, 2 |
| letdownRateMps | 0.5, 2 |
| climbAirspeedMps | 0, 5 |
| letdownAirspeedMps | 0, 5 |

Climb and letdown each have independent peak-rate and peak-airspeed caps.
The slowest peak letdown cap is 0.5 m/s on each class.
This finite bound includes slow descents; smaller caps remain unsearched, not physically excluded.

Short joins take longer when needed for smoothness.
The prescribed return widens its climb and letdown joins using an upper bound on the composed easing derivatives, so each of the 2,001 sampled vertical speeds differs by at most 0.1 m/s. If those joins would overlap, its return time grows instead. This applies to all searched prescribed controls, not one retained-water row.
The drop altitude, terrain clearance and cable reach stay fixed.
The approach remains stationary.
Segment time and ground distance are integrated; energy uses the same instantaneous ledger.
A profile exceeding the route distance is refused.

Retained water is searched at five-percent payload steps and at each bisected first closing threshold.
Printed requirements round upward at the verdict resolution and replay through the model.
The older whole-phase dilation is named `movingPhaseRateMultiplier`; the new search does not use it.
<!-- energy:physics:end -->

## 12. What the model deliberately does not attempt

Listed so nobody has to discover them by reading code.

- **Weather.** One 850 hPa wind vector per route, applied as an along-track component to
  transit times only, clamped to between 0.35× and 1.8× airspeed. No vertical motion, no
  shear, no gusts, no icing, no convective column, no diurnal cycle. Altitude profiles are
  unaffected by wind entirely.
- **Turbulence and gust loading.** An 876 m hull in the convective column over a fire is a
  structural and control problem the model does not represent. The 450 m drop altitude was
  chosen with that in mind and is a guess.
- **Fire behaviour.** Nothing in the model says whether a fire grows, spreads or is
  contained. Water delivered is not fire extinguished, and no suppression effectiveness is
  claimed, modelled or implied. Fire size and perimeter are read from the provincial feed
  and never change in response to anything the fleet does.
- **Water uptake and drop physics.** Drops are metered mass leaving the tanks along a line.
  Droplet size, drift, evaporation, canopy interception, ground pattern and the effect of
  rotor-induced airflow on all of it are absent. A rotor holding the hull down has an upward wake.
- **Hydrology and ecology.** Lakes are selected on mapped surface area. Depth, intake
  screening, seasonal drawdown, fish, mussels and the legal right to take the water are not
  established. Repeated withdrawal at these rates is not claimed to be sustainable.
- **Air traffic and airspace.** No deconfliction with crewed aircraft, no TFRs, no
  separation between the fleet's own hulls, which are routinely modelled sharing a lake.
- **Regulation and certification.** No airworthiness basis exists for any of this.
- **Cost.** No capital cost, no operating cost, no comparison with existing air tanker
  fleets, ground crews or the alternative of doing nothing. Any economic claim about this
  concept would be invented.
- **Manufacturing.** No process is proposed for a 425,000 m² vacuum shell.
- **Failure.** No structural failure modes, no rotor-out cases, no what-happens-when-the-
  vacuum-is-breached. The 3D library has a failure explorer; the model behind these numbers
  has none.
- **People.** No crew, no maintenance, no basing, no logistics beyond the water.

The autonomy — "the Mind" — is a narration layer over a deterministic state machine. It
makes no decisions the code does not make in `assign.js`, `water.js` and `targets.js`, and
nothing in the model learns, adapts or replans in response to anything except a new data
fetch.
