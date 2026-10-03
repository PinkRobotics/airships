# The physics

This document states the model in the order a physicist would want it: what lifts the
vehicle, what the shell would have to be, what one delivery cycle costs, and where the
arithmetic fails. Every equation is the one in the code. Every constant is given with its
value, its provenance, and how much the headline figures move when it moves.

No such aircraft exists. Nothing here is validated against a built vehicle, because there
is no built vehicle. This is arithmetic on stated assumptions, published so that the
assumptions can be attacked. Six defects were found by audit; one — the cryogenic plant's inertness in the cycle — is
open, and five are written up as fixed rather than deleted: buoyancy at sea level and retained
ballast on 2026-08-09, and the two power models, the letdown window and the generators on
2026-10-01, when one energy model replaced two. They have their own section and they are not
hidden anywhere else in the document.

The flight model assumes a hull that floats; no drawn hull does, as the [float case](FLOAT.md) and [ledger](FLOAT-LEDGER.md) explain.

Symbol-to-function references are in [`../sim/README.md`](../sim/README.md), which indexes
every published number to the line that computes it.

---

## Notation

| Symbol | Meaning | Value or source |
|---|---|---|
| ρ_SL | sea-level air density | 1.225 kg/m³, ISA; `DEFAULTS.rhoSL`, the anchor of the density column |
| ρ(h) | air density at altitude h above MEAN SEA LEVEL | `sim/atmosphere.js`, ISA troposphere |
| ρ_work | air density at the altitude the hulls are sized at | 0.95686 kg/m³, ρ(2,500 m) |
| ρ_air | working air density used for drag and rotors | 1.10 kg/m³, `DEFAULTS.rhoAir`. See Defect 2 |
| h_t | terrain reference elevation | 1,000 m MSL, `TERRAIN_MSL` |
| ρ_w | water density | 1000 kg/m³ |
| g | gravity | 9.81 m/s² |
| V | hull displacement | `CLASSES[*].dispM3` |
| m_dry | dry mass allowance | `= payloadT`, by assumption |
| m_pay | water payload | `CLASSES[*].payloadT` |
| A_f | hull frontal area | π(d/2)² |
| A_d | total rotor disk area | `CLASSES[*].diskM2` |
| C_d | drag coefficient on frontal area | 0.05, `DEFAULTS.Cd` |
| η_p | propulsive efficiency | 0.70, `DEFAULTS.propEta` |
| η_pump | pump-system efficiency | 0.75, `DEFAULTS.pumpEta` |
| h | pumping head = hose length = fill altitude | 300 m on every class, `CLASSES[*].hoseM` × `CFG.hoseMul` |
| Q | fill rate | `CLASSES[*].fillM3s` |

SI throughout, surfaced as tonnes, kilometres, minutes, megawatts and megawatt-hours. One
tonne of water is one cubic metre.

---

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

**FAIL-SAFE FLOAT-UP SETS THE DISPLACEMENT.** The requirement, decided 2026-08-09, is that a
hull be positively buoyant at its working altitude *while fully loaded with water and unable
to drop it*. Nitrogen ballast is excluded from that mass because it vents to atmosphere in
seconds; water is the load a ship can be stuck with. The working altitude is
h_t + `ALT.cruise` = 2,500 m MSL, which is the thinnest air in the cycle, so sizing there
sizes for everywhere. At ρ_work = 0.95686 kg/m³ a loaded tonne needs 2,194.7 m³ of
displacement with a 5% margin; the classes carry 2,200 m³ per tonne of payload:

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

## 3. What has to fit inside the dry allowance

The dry allowance is not a structure budget. It also has to contain the batteries, the
generators, the cryogenic plant, the rotors, the water tanks and everything else. The
batteries alone are the problem:

| | storage | mass at 250 Wh/kg | at 350 | at 500 | share of dry allowance at 250 Wh/kg |
|---|---:|---:|---:|---:|---:|
| P-100 | 20 MWh | 80 t | 57 t | 40 t | **80%** |
| P-1000 | 120 MWh | 480 t | 343 t | 240 t | **48%** |
| P-10000 | 2,000 MWh | 8,000 t | 5,714 t | 4,000 t | **80%** |

250 Wh/kg is roughly a good current pack. 500 Wh/kg is beyond anything shipping. At either
figure the battery is a large fraction of a dry allowance that also has to include a
vacuum shell nobody knows how to make.

The 3D library's mass breakdown (`3d/model/metadata.js`, `MASS_SHARE`) allots 14% of dry
mass to "power": 1,400 t on the P-10000, for 2,000 MWh of storage plus 150 MW of
generation. That is 1,430 Wh/kg for the storage alone before the generators are counted.
The two halves of the project do not agree with each other here, and neither agrees with
any cell chemistry.

The rotors are the other awkward item. 160,000 m² of disk in the 14 units `sim/config.js`
counts is 120.6 m per unit — the diameter of a large offshore wind turbine — carried by an
876 m hull, and each must absorb 111 MW of the 1,550 MW bus. A 5 MW wind turbine of that
diameter operates at about 0.4 kW/m² of disk. These run at 9.7 kW/m².

The two halves of the project do not agree on the disc count either. `3d/model/config.js`
resolves the same published area as 14 *stations* of two 85 m rotors — 28 discs,
158,886 m², 0.7% below the published 160,000 — so `rotors: 14` in `sim/config.js` has to be
read as a station count, and the 120.6 m figure as the diameter a single disc per station
would need. Nothing in the model depends on which reading is taken, because only the total
area enters `diskMW`; the illustration and the arithmetic are nonetheless describing
different hardware.

---

## 4. The delivery cycle, phase by phase

Six phases, `config.js → PHASES`, timed in `plan.js → planCycle`. Work that can overlap
does: the hose pays out during the flown approach and winds up during the climb-out, so
neither gets stopped time of its own.

| Phase | Duration | Altitude | Water |
|---|---|---|---|
| `SOURCE_APPROACH` | `max(1.5·fixed, hoseDeployMin·0.5·hose, anchorM / 5 m/s)` | holdAgl → sourceAlt: 430 / 960 / 1,210 → 300 m AGL | retained only |
| `WATER_FILL` | `deliveredT / Q / 60` | 300 m, station-keeping | 0 → payload |
| `OUTBOUND_TRANSIT` | `max(legKm/gs_out · 60/0.85, hoseRetractMin·0.4·hose + 0.8)` | 300 → altTop → 450 m | payload |
| `WATER_RELEASE` | `max(dropKm/(0.45·v)·60, delivered/fill/60)` — one pass | 450 → 580 m | payload → retained |
| `BUOYANCY_ESCAPE` | `2 × fixed` | 580 → max(760, 0.75·altTop) | retained |
| `RETURN_TRANSIT` | `max(1.2, legKm/gs_ret · 60/0.85)` — no stretch since 2026-10-01 | altEsc → altTop → holdAgl (430 / 960 / 1,210 m) | retained |

Transit legs are trapezoids, not steps: 15% of the distance accelerating and 15% braking,
so a leg takes 1/0.85 as long as distance/cruise. The drop is a run at 45% of cruise, laid
along a `dropKm` line, repeated an odd number of times so the ship finishes at the far end
where the escape climb begins.

`ALT.cruise = 1500` m is a ceiling, not a cruise altitude. `power.js → cycleGeometry` derives
the achieved ceiling from what the shorter leg can reach at 30% of `VZ_MAX`:

> altTop = min(1500, 300 + 108 × min(t_out, t_ret) minutes)

so 1,500 m is only reached when the shorter transit leg exceeds 11.1 minutes. A P-10000
working a fire 15 km from its lake tops out at 1,180 m above ground.

For the P-10000 at 15 km, balanced, still air, the cycle is 45.51 minutes: 5.0 approach,
11.1 fill, 8.1 out, 11.1 release, 2.0 escape, 8.1 return. It delivers the whole 10,000 t —
the descent anchor means nothing is kept back as ballast — which is 13,183 t/h to that fire,
1.32 drops per hour.

The release is ONE pass, flown at about 27 km/h. It used to be three passes over the same
line at drop speed, 15.4 minutes for 11.1 minutes of water: the extra 4.3 minutes were
turnarounds, an 876 m hull reversing over the fire it was dropping on, and the water lands on
the same line either way. The line itself cannot simply grow — `dropSeg()` shrinks it until
both ends are inside the fire — so the run is long in TIME rather than in distance.

Two corrections on 2026-08-09 moved this, in opposite directions. The resize took it from
50.76 minutes and 11,820 t/h to 49.79 and 12,052: honest density cut the surplus the rotors
must push down from 12,050 t to 11,051 t, `downMW` fell from 1,434.5 to 1,259.5 MW, under the
ceiling that raises `battLimited`, so the 12% authority-limited stretch stopped applying.

Then the descent balance moved to the altitude where the descent ends. At the lake the hull
is 24% more buoyant than at its ceiling, `downMW` goes back to the full 1,550 MW bus,
`battLimited` is true again with its 12% stretch, and 1,056 t of water never leaves the
tanks. The fill is shorter because only the delivered water needs replacing, the return leg
longer because the letdown is authority-limited. Delivered per hour is 10% below the figure
this page carried an hour earlier, and that 10% is the cost of being able to get back down.

Since 2026-10-01 there is no stretch to apply. The return leg is kinematic whether or not the
bus clips — under disk theory a slower letdown costs more rotor energy, not less (Defect 3) —
and `battLimited` means the bus clamp bound the rotors during the letdown, which it does on the
P-1000 for 0.16 minutes. The altitude the transit levels off at before the slow approach,
`holdAgl`, is the bag's engagement altitude plus 60 m, struck on the honest bus of Defect 6:
430 / 960 / 1,210 m AGL, which on the P-10000 at 15 km is above its 1,180 m ceiling.

---

## 5. Pumping energy

Water is lifted 300 m from the surface to the tanks through a deployed hose, at the class's
fill rate:

> **P_pump = ρ_w g Q h / η_pump**

P-100: 1000 × 9.81 × 0.5 × 300 / 0.75 = **1.962 MW**. P-1000: 11.772 MW. P-10000: 58.86 MW.

The energy is the potential energy of the payload divided by one lumped efficiency:
0.068 MWh ideal for a P-100 load, 0.091 MWh delivered, 9.08 MWh for a P-10000 load. That
is small — 11% of the P-10000's published cycle energy — and it is the least contentious
number in the model.

The lumped η_pump = 0.75 covers pump, motor, drive, hose friction and the kinetic energy
left in the stream. Hose friction is not separately modelled, which matters more than it
looks: 15 m³/s at a plausible 6 m/s in-hose velocity needs a 1.78 m bore, and the standing
column in a 300 m hose of that bore weighs 750 t. The model neither carries that mass nor
charges for the friction of moving water through it.

---

## 6. Drag and cruise power

> **P_drag = ½ ρ_air C_d A_f v³ / η_p**

referenced to frontal area, cubed in airspeed. At default settings: P-100 1.06 MW,
P-1000 9.16 MW, P-10000 69.68 MW. Those are 14% above the 0.93 / 7.94 / 61.06 MW the
narrower pre-resize hulls cost: frontal area goes as the square of the diameter, and the
diameters grew 6.9% to buy fail-safe float-up.

C_d = 0.05 on frontal area is equivalent to a volumetric coefficient of

> C_dv = C_d A_f / V^(2/3) = **0.024**

for all three classes. That is inside the normal band for a bare streamlined body of
revolution at high Reynolds number and is not an unreasonable figure. A check on it: at
cruise the P-10000 sits at Re ≈ 2 × 10⁹, giving a flat-plate C_f of about 0.00145, and
skin friction over 485,575 m² of wetted area comes to 505 kN against the model's total
drag of 1,351 kN. Friction is 37% of the assumed total, leaving 63% for form drag and
everything else, which is generous for a fineness-4 hull.

**2026-10-02 correction:** this hand calculation used the former spheroid’s surface.
The nominal capsule now has 411,775 m² of surface, as recorded in the regeneration audit.
The force estimate has not been rerun; its precise air-density and speed basis was not recorded here.

Generous for a *bare* hull. The model charges nothing at all for 14 rotor installations
of 120 m diameter, for fins, for the hose pod, or for the interference between them. On a
real vehicle those appendages would plausibly rival the hull. C_d = 0.05 should be read as
a hull-only figure that the sensitivity table shows is not where the model's problems are.

---

## 7. Rotor and aerodynamic hold-down — correction 2026-10-01

`sim/power.js` is the authority for both the record and favourable bases. Rotor power
uses ideal Glauert momentum theory: T = 2 rho A vi sqrt(V² + (vc + vi)²),
P = T (vc + vi) / eta. Airspeed is the instantaneous profile speed, corrected for
along-track wind on transit legs. The axial term is max(0, -vz). Opposite-flow operation
is priced as level flight; there is **no validated error bound** for that approximation.
A downward-thrust rotor's slipstream points upward. Disk induced velocity is not a
measurement of wind at the lake surface.

The bus includes battery rating, the solar assumption and actual nitrogen return.
Every other running channel is reserved before rotor power is allocated. Thrust is
also capped independently at the hover thrust corresponding to the existing class's
battery-plus-generator rating. **This is an unverified installed-thrust surrogate:
the class record supplies no blade thrust rating.** No class constant changed.

The record basis has zero aerodynamic hold-down. The favourable basis minimises total
rotor plus induced-drag power. Its limit is C_L,max q S, q = rho V² / 2, with
S = d(L-d) + pi d²/4, b = d, e = 1. Induced drag is L_down²/(q pi b² e), and
propulsion is (zero-lift drag + induced drag) V / eta. Downforce is zero at zero airspeed.
C_L,max = 1 is unverified; [the generated table](ENERGY-CLOSURE-2026-10.md) reports
0.5, 1 and 1.5. No attainable hull coefficient was found in the local research.
Broadside vertical C_D = 1 is a separate unverified assumption. Drag and rotor density
remain the stated flat CFG.rhoAir; buoyancy uses local ISA density.

---

## 8. Cryogenic ballast

The intended mechanism: on the return leg, an onboard air-separation plant liquefies
nitrogen and stores it, so the empty hull has ballast to descend on instead of fighting its
own buoyancy with rotors. On the fill, the nitrogen boils off and hands some energy back
while incoming water replaces its mass.

> ballast target: **m_N2,need = min(0.8 × surplus, ln2CapT)**
> produced: **m_N2 = min(m_N2,need, P_cryo · t_return / e_LN2)**
> cost: **E_cryo = m_N2 · e_LN2**, recovered: **E_back = E_cryo · rt_LN2**

with e_LN2 = 0.45 kWh/kg and rt_LN2 = 0.20 (0.50 until 2026-08-09; see §9 and OPEN-QUESTIONS #10).

The arithmetic does not work. A P-10000 returning for 8.1 minutes on a 70 MW plant makes
9.50 MWh of liquefaction work, which at 0.45 kWh/kg is **21.1 t of nitrogen** — against a
15,500 t tank and an 11,051 t buoyancy surplus. `ln2NeedT` is the smaller of 80% of that
surplus and the tank, so the function asks for 8,841 t and gets 0.24% of it. It costs 5.4%
of the cycle's energy to do that (12.6% of the smaller cycle published before 2026-10-01).
The recovered 1.90 MWh is real and comes back as `gen.regen` while the nitrogen is vented —
30% in the approach, 70% in the fill — at no more than the generators' rating (§9, Defect 6);
until 2026-08-09 it was netted against the pump bill under a `max(0, …)` that discarded the
excess on the two smaller classes.

To make the mechanism work at the stated energy intensity, the P-10000 would have to
liquefy roughly 8,841 t of nitrogen per cycle, costing 3,978 MWh — about twice its entire
battery, per drop. Nitrogen ballast at cycle rate is not an efficiency question; it is off
by three orders of magnitude. The honest statement is that the cryogenic plant, as modelled,
does nothing in the delivery cycle.

**What it is not decoration for.** Since 2026-08-09 the tank is sized by a requirement
instead of a round number: `ln2CapT` = 155 / 1,550 / 15,500 t is what it takes to make an
empty hull heavy enough to LAND with no rotor authority at all, at the ground rather than at
the ceiling — see `docs/OPEN-QUESTIONS.md` #0. Filling it costs 65 / 651 / 6,505 MWh, which
is 2.6 / 5.7 / 12.9 days on solar alone after the hotel load, or 0.45 / 0.90 / 2.7 days at
rated plant power. Those are the unpowered-recovery figures the fail-safe claim rests on,
and they are what the plant is for. It is sized for a rescue that takes days, not for a
cycle that takes an hour, and the two should stop being confused for each other.

---

## 9. Vertical closure and the two energy bases — 2026-10-01

At every instant `drawAt` returns local buoyant lift minus dry mass, water and nitrogen,
and named force owners in tonnes-force: bag, rotors, aerodynamic downforce and signed
vertical drag. Their sum plus `unheldT` equals the surplus. No hold/share schedule assigns
an unpriced force. The bag carries only geometrically reachable water whose 15 m hoist
at 85% efficiency has completed; the fill inherits that inventory across its seam.

An unsupported instant makes the plan `feasible: false`, with worst unheld force,
phase, progress and binding limits. This is quasi-static force closure along the prescribed
profile, **not validation of its accelerations**. No residual is silently used to fly a
different trajectory. A negative residual can require upward authority the model does not grant.

Both bases use this one record. `stateAt` reads it, and the 3D adapter maps its actual power
channels. Missing standalone telemetry is unknown. Energy is integrated separately from
constraint events: seams and profile breakpoints are included in a fixed 1,024-step constraint
mesh, local power maxima are refined, and clipping crossings are bisected. Changing the
96-step energy quadrature does not change the reported peak or clipping duration.

**At 15 km, all three classes are INFEASIBLE on both bases.** The values in the
[generated comparison and requirements tables](ENERGY-CLOSURE-2026-10.md) are supplied effort
along an unsupported profile, not an achievable cycle price. At 60 km the P100 closes in this
model on both bases; the larger drawn classes still do not. Those are model conclusions on
unverified assumptions, not flight evidence. Battery hours are energy quotients only.

`research/analysis/energy-closure.json` binds every comparison, coefficient sensitivity and
requirement. `research/analysis/energy-model-change.json` preserves the first builder's
attribution and extends it with the closure step. Ballast reduces delivered water, while the
power/thrust requirement keeps ballast at zero. Air admission is not an available lever:
`research/analysis/air-ballast.md` retracts it for permanently sealed cells.

---

## 10. Sensitivity

The current C_L,max sweep, at 0.5 / 1 / 1.5 for each class, distance and basis, is generated
in [ENERGY-CLOSURE-2026-10.md](ENERGY-CLOSURE-2026-10.md). `tools/figures_dump.js` also recomputes
the original ±20% parameter sweep on the record basis. A smaller clipped energy number does
not show a more efficient feasible flight: power may simply have been refused. Interpret
energy changes beside feasibility, unheld force and binding limits.

---

## 11. Known defects — historical record with correction

**2026-10-01 correction:** the entries below retain the earlier arithmetic-fix record. Their energy numbers and claims of physical closure are superseded by §§7 and 9 and the generated closure table. “Fixed” in an older heading does not certify flight feasibility.

Each is quantified below and each has an entry in
[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) giving the options and a recommendation. The
numbering is not one-to-one: Defects 4 and 5 here are the two halves of open question 4,
Defect 6 here is open question 6, and open question 5 — the Esri basemap — is a licensing
and privacy problem rather than a physics one, so it has no entry here.

One `knownFail` marker is left in `tests/cases/`, and it is the unrelated flag bug
(`plan · windUsed`). Defects 2 and 3 carried the other two until 2026-10-01, when the one
energy model made them pass; their markers were replaced by ordinary tests of the corrected
behaviour — the budget equal to the integral of the flight on every golden combination, and
the letdown equal to the rotor energy over the flown descent with no window. Defects 4, 5 and 6
were asserted by ordinary passing tests from the start, because each of them is a statement
about what the code *does* rather than a broken assertion: `selftest.js` requires `retainedT`
to be zero, and no test can fail because a term is missing from a sum; Defect 6's tests now
assert the generators as storage. Defect 1 had the fourth marker; it started passing on
2026-08-09 and was converted the same way.

Five of the six are fixed (1, 2, 3, 4 and 6); 5 — the cryogenic plant's inertness in the
cycle — is open. They are stated here with numbers because the alternative — publishing the
figures and letting a reader find these — would be worse than useless.

### Defect 1 — buoyancy was computed at sea level — FIXED 2026-08-09

**What it was.** `ledger()` evaluated L = ρV at ρ_SL = 1.225 kg/m³ and used the result at
every altitude. The ships work between 300 m and about 1,180 m above ground, over interior
British Columbia terrain that is itself 500–1,500 m above sea level. Loaded break-even was
1.1111 kg/m³, which is 1,005 m in ISA, so the sign of the net force reversed *within a
single cycle*: a full P-10000 was +406 t over the lake, −860 t on the drop run and −2,209 t
at the ceiling it climbs to. `netFrac`, `vert`, every rotor draw and every force readout had
the wrong sign for part of the cycle, and the outbound leg needed rotor thrust upward that
the model never charged for.

**What was done.** `sim/atmosphere.js` computes ISA density against altitude, with its
constants sourced to ISO 2533:1975 and cross-checked against the published table. `ledger()`
takes an altitude in metres MSL, with no default, so a caller that has not decided where the
ship is gets an exception. `planCycle` evaluates it at `WORK_ALT_MSL` = 2,500 m; `stateAt`
evaluates it at every instant from the ship's own altitude. The hulls were then resized to
satisfy fail-safe float-up — buoyant fully loaded, at the working altitude, with a 5.25%
margin — which cost +22.2% of displacement (§1) and 14% more cruise drag (§6).

The same table, recomputed on the shipped numbers:

| Point in the cycle | altitude MSL | ρ | P-10000 net, loaded | water at which it goes heavy |
|---|---:|---:|---:|---:|
| source hold, 300 m AGL | 1,300 m | 1.0793 | +3,744 t | 137% of payload |
| drop run, 450 m AGL | 1,450 m | 1.0633 | +3,393 t | 134% |
| achieved ceiling, 1,180 m AGL | 2,180 m | 0.9884 | +1,745 t | 117% |
| nominal ceiling, 1,500 m AGL | 2,500 m | 0.9569 | +1,051 t | 111% |

The hull is buoyant at every point in the cycle carrying more water than it can hold. Over a
whole seed-7 cycle the minimum net force on the three classes is +10.5 t, +105.1 t and
+1,231.1 t, so the rotors only ever push down, as computed rather than as asserted.

**What is left.** `rhoAir` is still a flat 1.10 kg/m³ for drag and rotors, which is ISA at
about **1,107 m** against a 2,500 m working altitude: drag overstated 15%, induced power
understated 7%. (Three documents said "about 990 m"; ISA at 990 m is 1.1127 kg/m³. Run
`altitudeForDensity(1.10)`.) That belongs to Defect 2, and it is pinned by a test so it cannot be lost.

### Defect 2 — two disagreeing power models — FIXED 2026-10-01

**What it was.** `planCycle` published a per-phase budget and `stateAt` reported a per-system
draw that `app/loop.js` integrated to drive the storage gauge; they were separate
implementations of one quantity. Re-measured at the base of the fix on the fixture missions
(legs of about 19 km): 2.64 MWh integrated against 1.70 planned for the P-100 (1.55×), 24.54
against 10.10 for the P-1000 (2.43×), 236.77 against 62.34 for the P-10000 (3.80×). The gap
was mostly the rotor term, and mostly §7's forward-flight error: `stateAt` priced cruise trim
with the hover formula (80.3 MW where Glauert gives 12.1) while `planCycle` never charged
cruise rotor trim at all. Neither was right.

**What was done** (OPEN-QUESTIONS #2, decision (c): fix the physics, then unify). `sim/power.js`
is the one model. `drawAt(cls, mode, plan, phase, prog)` prices an instant — hotel, prop,
fans, winch, pumps, cryo, rotors; the bus; the nitrogen return; the anchor — with the rotors on
Glauert momentum theory (§7). `integrateCycle` sums it, 96 midpoint steps per phase, and that
is what `planCycle` returns as `E` (six phases plus `recovery`), `Echan` (by channel) and
`eCycleMWh`. `stateAt` calls `drawAt` and adds only position, bearing and the sub-phase label;
a test asserts `stateAt(...).draw` deep-equal to `drawAt(...).draw` sample by sample, another
asserts the integral of `stateAt` within 0.5% of `plan.eCycleMWh` on all 135 golden
combinations (measured worst 0.0757% at 4,000 samples), and `selftest.js` check 20 does the
same on the live page.

**What it moved.** Both numbers moved towards each other, as the decision asked, and the
published one moved most: 1.391 → 2.023, 8.454 → 18.149 and 54.325 → 176.000 MWh per cycle at
15 km. Attributed step by step in `research/analysis/energy-model-change.json`: pricing the
hold-down wherever the ship is (Defects 3 and 15) is +56 / +155 / +307% of the old cycle;
Glauert takes −10 / −25 / −53% back; the anchor credit (#14) −1 / −9 / −21%; the honest bus
clamp (Defect 6) 0 / −1.1 / 0; and the descent closure re-struck on that bus, which changes the
hold altitude and engagement time, not the cable reach, 0 / −5.3 / −8.7%. Endurance on the battery: 9.2 / 9.2 /
30.2 hours → 6.1 / 4.1 / 8.8.

**What is left.** The choreography the integral prices is the one `stateAt` always flew — the
hold and share schedules (12% of the surplus to the rotors at cruise, 60% at the stop, aero
trim the rest, including with the ship stopped), the phase speed profiles, the 72% letdown
point — and none of it is derived. The share schedule is the largest lever left on the rotor
channel (`research/analysis/descent.md`, "what remains"). `CFG.rhoAir` is still flat.

### Defect 3 — an unexplained window sets the largest energy term — FIXED 2026-10-01

**What it was.**

```js
E.letdown = downMW * Math.min(6, dur.RETURN_TRANSIT * 0.2) / 60;
```

For the P-10000 at 15 km this was 52.3 MW × 1.628 min / 60 = 1.420 MWh, 2.6% of the published
cycle; neither the `6` nor the `0.2` was justified anywhere, the `min` was inactive below about
55 km one-way, and `downMW` was the bag-assisted residual applied to a descent the bag could
not reach most of (#15). The `battLimited` branch stretched the return leg by 1.12 and so
*raised* the letdown energy its comment said it reduced.

**What was done.** The window, the `0.92` threshold and the `1.12` stretch are gone from
`sim/plan.js`; `/usr/bin/grep -rn 'Math.min(6' sim/` prints nothing and a test fails if the
implied window ever equals 6 minutes or 0.2 × the return leg again. `letdownMWh` is the rotor
energy integrated over the flown descent — the last 28% of the return leg and the whole
approach — with the rate of descent in the disk model (§7). The return leg stays kinematic
(`max(1.2, km / kph × 60 / 0.85)` minutes) whether or not the bus clips, because under disk
theory a slower letdown costs more, not less; `battLimited` now means that the bus clamp held
the rotors below what the hold asked for during the letdown (`letdownClipMin > 0`), and the
class reports `descent authority` as its bottleneck when it does.

**What it moved.** The letdown is 0.390 / 4.279 / 35.398 MWh at 15 km — 19.3 / 23.6 / 20.1% of
the cycle — against 0.012 / 0.161 / 1.420 before. The P-1000 is the class that clips: 0.16
minutes of its letdown, 0.015 MWh short, during the approach before the bag goes in, because the
rotors-alone crossing (1,450 m AGL) is above its 600 m cable's reach.
`research/analysis/descent.md` has the profile.

### Defect 4 — retained descent ballast was zero, everywhere, always — FIXED 2026-08-09

```js
// before: one ledger, struck at the ceiling, and nothing but rotors and kept water
retainedT = Math.max(0, led.surplusT - ln2MakeT - rotorMaxT / 0.6);
// after: struck where the letdown ends, and the lake holds the ship down
const holdT    = Math.max(0, ledLow.surplusT - ln2MakeT);
const anchorT  = Math.min(cls.anchorBagT, Math.max(0, holdT - 0.9 * rotorMaxT / 0.6));
const retained = Math.min(cls.payloadT, Math.max(0, holdT - anchorT - rotorMaxT / 0.6));
```

`rotorMaxT / 0.6` exceeded the surplus for every class, so `retainedT` was identically zero,
while `narrate()` had branches for "retaining N t as descent ballast", the worked-example note
had one, and `bottleneck` could return "descent ballast — cryogenic capacity". None of that
code could execute. The mechanism was prose.

**The altitude was the fault.** Float-up and descent do not share a worst case: float-up is
hardest at the ceiling in the thinnest air, descent is hardest at the lake 1,200 m lower where
the air is 16% denser and the hull correspondingly more buoyant. Both were answered with the
ceiling ledger. `planCycle` now carries two — `led` at `WORK_ALT_MSL` for sizing and float-up,
`ledLow` at `TERRAIN_MSL + sourceAltM(cls)` for everything that answers to descent:

| | rotorMaxT/0.6 | surplus, ceiling | surplus, lake | headroom, ceiling | headroom, lake |
|---|---:|---:|---:|---:|---:|
| P-100 | 267.2 t | 110.5 t | 137.4 t | ×2.42 | ×1.94 |
| P-1000 | 1,318.1 t | 1,105.1 t | 1,374.4 t | ×1.19 | **×0.96** |
| P-10000 | 12,666.2 t | 11,050.9 t | 13,743.6 t | ×1.15 | **×0.92** |

Below ×1.0 the rotors cannot hold the hull down alone. That left 49 t and 1,056 t to find.
Re-struck on the honest bus of 2026-10-01 (Defect 6), `rotorMaxT/0.6` is 227.8 / 1,107.5 /
11,474.6 t, the lake headroom ×1.66 / ×0.81 / ×0.83, and the bag covers 259 t and 2,248 t —
which is exactly what a hull without the bag keeps aboard (`research/analysis/descent.md`).

**The answer is a bucket.** Three things can make up a descent shortfall and they are not
equal: rotors cost power, retained water costs DELIVERY, and a bag of lake water on a cable
costs the 15 m of lift needed to break the surface. So the order is rotors, then anchor, then —
never, on the shipped numbers — retention. The bag is dumped back into the lake as soon as the
tanks hold more than the shortfall, so nothing is carried away and nothing is manufactured.

It is a Bambi bucket, the collapsible helicopter bucket in service since 1983, at a scale
nobody has built: the largest ever made is 9,800 L and the P-10000's is **1,265 times** that.
The principle
is unchanged and the engineering is not, which is the honest way to describe it.

The bag is sized generously on purpose. The bare shortfall is 1,056 t, and a bag that size
leaves the rotors at 100% of authority for the whole letdown, which is not a margin and costs
power besides. The bag is sized to do the whole descent instead: at 12,400 t it takes 12,400 of
the 13,722 t hold, the rotors are left doing 10% as trim, `battLimited` stays false and the 12%
letdown stretch never applies. Cable: 12,400 t is 122 MN, which is about 440 mm of UHMWPE massing
125 t, against roughly ten times that in steel wire. Synthetic rope is what makes this cheap, as
it did for deep-tow oceanography.

**Costs, against the alternatives.** Anchor 0.60 MWh a cycle. A 1,350 m hose so the ship fills
from altitude and never meets the dense air: 44 MWh, 2 m bore, 140 bar. The same ballast as
liquid nitrogen: 475 MWh, or 5.8× the cryogenic plant to make it inside one cycle. The 2026-08-09 version reported
13,183 t/h for a 45.87 MWh cycle. This is a historical number, superseded first by 176.000 MWh
and now by the explicitly infeasible record/favourable figures in §9.

**In the picture.** The 3D view draws the whole sequence — cable out, bag dipped, bag lifted
clear, bag dumped — against a translucent lake with rings at one-hull-length intervals. The rings
are there because a featureless plane has no perspective and the hull reads as floating IN the
water rather than 300 m above it. The bag is drawn at its true size, which is smaller than a
reader expects: 12,400 t of water is a sphere 28.7 m across beside an 876 m ship, and that
contrast is worth seeing rather than correcting.

**Not modelled, and material:** 12,400 t swinging on one cable under an 876 m hull is a pendulum
nobody has analysed; the bag has to survive being filled and dumped every cycle; the winch is
assumed to run at 5 m/s both ways; and the cable is paid out during the approach, which is the
only place it can extend the cycle.

### Defect 5 — the cryogenic plant is numerically inert in the cycle

Covered in §8. 21.1 t of nitrogen against an 11,051 t surplus and a 15,500 t tank; 5.4% of
the cycle's energy (12.6% of the smaller cycle before 2026-10-01) for 0.24% of the stated
function. `cryoLimited` is now true for **every**
combination in the 135-case grid, where before the resize one — a P-100 in endurance mode on
a 400 km leg — did fill its tanks. The target rose with the honest surplus and the tank cap
stopped binding first, so the flag has gone from almost uninformative to entirely
uninformative. Copy on the concept page and in the mission narration describes the plant as
making the ballast the ship descends on, and within a cycle it does not.

What the plant is not inert for is unpowered recovery, which is what its tank is now sized
by: 65 / 651 / 6,505 MWh to make a hull heavy enough to land itself with no rotors, taking
days rather than a cycle. §8 has the figures. The two jobs should be described separately,
because one of them works.

The bookkeeping wrinkle this paragraph used to record — `ln2MakeT` computed from the
pre-stretch return leg while `E.letdown` was charged over the post-stretch one — is gone with
the stretch (Defect 3). The plant now runs for exactly the fraction of the return leg that
makes its integral equal `eCryo` (`power.js → cryoOnFrac`), so the cryo channel in the ledger
is the plant's energy to the kilowatt-hour.

### Defect 6 — the generators supply thrust but no energy — FIXED 2026-10-01

**What it was.** Each class advertises onboard generation — 8, 40 and 150 MW — and `plan.js`
counted it in full when it sized rotor authority (`rotorMaxT` from `battMW + genMW`, and the
`battLimited` bus ceiling with it) while nothing credited that generation as energy. The
vehicle was given the thrust its generators would allow and flown as though they were
switched off; the open possibility this entry carried was that the published deficit was an
artefact of the omission.

**What was done** (OPEN-QUESTIONS #6, decision: keep the generators and credit them as the
nitrogen expansion path, which is storage, not a source). `drawAt` books the generators'
output as `gen.regen`: the store's energy (`ln2MakeT × eLN2 × rtLN2` — 0.165 / 0.674 /
1.900 MWh at 15 km) returned at a rate bounded by `genMW`, 30% during the approach as the bag
goes in and 70% during the fill, so `eBack` can never exceed either the store or `genMW` ×
the venting time (both asserted on all 135 golden combinations). The bus the rotors are
clamped to is `battMW + min(genMW, regen)` at every instant; the descent closure in `plan.js`
is struck on the same bus (`descentBusMW`), with the same 0.95 ceiling `stateAt` uses, so the
state clamp and the plan closure cannot disagree.

**What it moved.** `rotorMaxT` 160.3 / 790.9 / 7,599.7 → 136.7 / 664.5 / 6,884.8 t and the
descent bus 38 / 190 / 1,550 → 31.5 / 154.0 / 1,406.8 MW; the altitude below which the rotors
stop managing alone rises, and with it the scan/hold altitude (500 → 900 m and 750 →
1,150 m in that version). These are not physical cable tops: the cables are 600 / 850 m,
and usable reach after half the hull diameter is 540.5 / 722 m. The energy credit is unchanged —
it was already the `recovery` line — and the deficit got larger, not smaller, because the rest
of the model was fixed in the same change: 1.24 / 7.71 / 50.23 → 1.87 / 17.41 / 171.9 MWh per
cycle. In plain words: the generators cannot make the fleet's energy close. They return a
fifth of what the plant spent liquefying nitrogen, and only when there is nitrogen to expand.

**What is left.** A hull that runs out of battery has only the store to descend on, and the
model does not yet refuse to fly a cycle it cannot power; `app/loop.js` still drains a gauge.
The fuel-mass question the first reading of #6 raised does not arise — there is no fuel — but
the store's mass is in the mass budget only as a tank.

---

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
