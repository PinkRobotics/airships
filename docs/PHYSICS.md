# The physics

This document states the model in the order a physicist would want it: what lifts the
vehicle, what the shell would have to be, what one delivery cycle costs, and where the
arithmetic fails. Every equation is the one in the code. Every constant is given with its
value, its provenance, and how much the headline figures move when it moves.

No such aircraft exists. Nothing here is validated against a built vehicle, because there
is no built vehicle. This is arithmetic on stated assumptions, published so that the
assumptions can be attacked. Six defects were found by audit; five are open, one — buoyancy
at sea level — was fixed on 2026-08-09 and is written up as fixed rather than deleted. They
have their own section and they are not hidden anywhere else in the document.

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
geometrically similar (fineness ratio 4, displacement matching a prolate spheroid to better
than 0.2%), so their ledgers are the same ledger scaled.

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

That displacement is +22.2% on the 180,000 / 1.8×10⁶ / 1.8×10⁷ m³ the hulls carried while
the ledger bought its lift at sea level, and the published sizes grew with it: 177 × 44 →
**190 × 47 m**, 380 × 95 → **404 × 102 m**, 820 × 205 → **876 × 219 m**.

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
  is a sphere because a sphere is optimal against external pressure, and these hulls are
  fineness-4 bodies of revolution. On a monocoque that penalty is severe enough to be fatal
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
| `SOURCE_APPROACH` | `max(1.5·fixed, hoseDeployMin·0.5·hose)` | 430 → 300 m AGL | retained only |
| `WATER_FILL` | `deliveredT / Q / 60` | 300 m, station-keeping | 0 → payload |
| `OUTBOUND_TRANSIT` | `max(legKm/gs_out · 60/0.85, hoseRetractMin·0.4·hose + 0.8)` | 300 → altTop → 450 m | payload |
| `WATER_RELEASE` | `max(dropKm/(0.45·v)·60, delivered/fill/60)` — one pass | 450 → 580 m | payload → retained |
| `BUOYANCY_ESCAPE` | `2 × fixed` | 580 → max(760, 0.75·altTop) | retained |
| `RETURN_TRANSIT` | `max(1.2, legKm/gs_ret · 60/0.85)`, ×1.12 if authority-limited | 0.55·altTop → altTop → 430 m | retained |

Transit legs are trapezoids, not steps: 15% of the distance accelerating and 15% braking,
so a leg takes 1/0.85 as long as distance/cruise. The drop is a run at 45% of cruise, laid
along a `dropKm` line, repeated an odd number of times so the ship finishes at the far end
where the escape climb begins.

`ALT.cruise = 1500` m is a ceiling, not a cruise altitude. `stateAt` derives the achieved
ceiling from what the shorter leg can reach at 30% of `VZ_MAX`:

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

## 7. Actuator-disk theory, and where it stops being valid

The rotors are treated with ideal momentum theory. For thrust T through disk area A_d in
still air:

> **P_ind = T^{3/2} / √(2 ρ_air A_d)**, delivered as `P_ind / η_p`

`physics.js → diskMW` is exactly this. `plan.js` inverts it to find the most thrust the bus
can produce, `rotorMaxT = (P η_p √(2ρA))^{2/3} / g`, and `state.js` calls it every frame to
price whatever downforce the current phase demands.

The resulting disk loadings are not absurd. On the P-10000's descent the model asks for
6.49 × 10⁷ N over 160,000 m², which is 406 N/m² — a helicopter figure — with an induced
velocity of 13.6 m/s. That is a 14 m/s downwash over the lake or over the fire, which the
model does not otherwise account for.

Two places where the formula is the wrong one:

**In forward flight it overstates induced power badly.** Hover momentum theory assumes the
disk draws still air. At airspeed v the induced velocity solves the Glauert relation
v_i = T/(2ρA√(v² + v_i²)), and induced power falls towards T²/(2ρAv). On the P-10000's
return leg at 36.1 m/s, holding the empty hull down, the model charges 80.4 MW where the
Glauert expression gives 12.1 MW — a factor of **6.7**. The P-100 and P-1000 are
overstated by 5.4× and 4.5× on the same comparison. This is the single largest reason the
integrated power model (§9) exceeds the planned one.

**In axial descent it understates.** When the vehicle is descending at rate v_c with the
rotors pushing down, the correct ideal power is T(v_c + v_i) with
v_i = −v_c/2 + √((v_c/2)² + v_h²). At v_c = 6 m/s, `VZ_MAX`, with the thrust the descent
actually asks for — the rotors' 0.6 share of the full empty surplus at the working altitude,
66.3 / 663 / 6,631 t:

| | model, hover form | axial-descent form | bus |
|---|---:|---:|---:|
| P-100 | 10.1 MW | 13.3 MW (+31%) | 38 MW |
| P-1000 | 145.9 MW | 176.4 MW (+21%) | 190 MW |
| P-10000 | 1,263 MW | 1,572 MW (+24%) | 1,550 MW |

**That boast has since been withdrawn, and this section is kept as the record of it.** The
disk area and battery peak were chosen so the hull could be driven back down to the water on
rotors alone with nothing held back, and the check that justified them was made at the
CEILING. Moving it to the source — where the letdown ends and the air is 16% denser, and where
it belongs — breaks it outright: 12,666 t of rotor capability against a 13,723 t hold. The
descent is closed by the anchor now, not by the discs, and `diskM2` and `battMW` are numbers
left over from a constraint that no longer binds. Measured today, `diskM2` ±20% moves cycle
energy by ∓0.4% and `battMW` ±20% moves every published figure by 0.0%. See
docs/OPEN-QUESTIONS.md #8.

Momentum theory also says nothing about blade loading, tip Mach number, solidity, or the
structural problem of hanging a 120 m rotor off a pressure vessel. Those are outside the
model entirely.

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
surplus and the tank, so the function asks for 8,841 t and gets 0.24% of it. It costs 12.6%
of the cycle's published energy to do that. The recovered 4.75 MWh is real but arrives
during the fill, where on the smaller two classes it exceeds the entire pumping bill and the
excess is silently discarded by a `max(0, …)`.

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

## 9. The energy budget, and why it does not close

`planCycle` builds a per-phase energy ledger. For the P-10000 at 15 km, balanced, still
air:

| Term | Equation | MWh | share |
|---|---|---:|---:|
| `E.RETURN_TRANSIT` | `P_drag × 0.55 × t_ret/60 + E_cryo` | 14.705 | 32.1% |
| `E.WATER_FILL` | `P_pump × t_fill/60` | 10.900 | 23.8% |
| `E.other` | `P_hotel × t_cycle/60 + P_drag × 0.4 × (approach+escape+release)/60` | 10.689 | 23.3% |
| `E.OUTBOUND_TRANSIT` | `P_drag × t_out/60` | 9.459 | 20.6% |
| `E.letdown` | `downMW × min(6, t_ret × 0.2)/60` | 1.420 | 3.1% |
| `E.anchor` | `m_bag g × 15 m / 0.85` | 0.596 | 1.3% |
| `E.recovery` | `−E_cryo × rt_LN2`, credited where it arrives | −1.900 | −4.1% |
| **total** | | **45.869** | |

Before the 2026-08-09 corrections this budget totalled 82.5 MWh; it fell **48%**. The table is
now printed straight out of `planCycle`'s returned `E` — it used to be transcribed by hand, which
is how it came to be 5% wrong in its total and to disagree with §11 of this document by 24×.

The bottom two rows were one row until 2026-08-09, and the merge was hiding an error. The pump
bill and the nitrogen credit were being netted inside `E.WATER_FILL` under a `max(0, …)`, so on
both smaller classes the recovery exceeded the pumping and the excess was *deleted* — 0.303 MWh
on a P-100, 0.594 on a P-1000 — taking the entire pump bill off the ledger with it. They are two
different physical events and they are two lines now. This alone moved the P-100's cycle from
1.308 to 1.005 MWh and its intensity from 13.08 to 10.05 kWh/t.

**`E.recovery` then shrank again, later the same day, and for a better reason.** `rtLN2` was 0.50
— a store returning 225 kWh from a tonne of liquid nitrogen holding 173.4 kWh of exergy. It is
0.20 now, 90 kWh/t, 52% of what is actually there. The credit fell from 4.751 to 1.900 MWh and the
cycle rose to 45.869. A test enforces the ceiling: `rtLN2 × eLN2 × 1000 ≤ 173.4`, and it is in
`spec-parity.cases.js` because both copies of the constant have to obey it. `E.anchor` is the whole story: it spends 0.596 MWh lifting
12,400 t of lake water the 15 m it takes to break the surface, and that purchase removes
34.5 MWh of rotor work. Fifty-eight to one.

The leverage is in the exponent. Rotor power goes as thrust^1.5 (§4), so load taken off the
rotors comes off faster than linearly: moving 90% of the hold onto the bag drops `downMW` from
1,748 MW to 52. This is why the bag is sized to do the whole descent rather than to cover the
1,056 t the rotors could not manage — the shortfall was the problem that revealed the mechanism,
not the limit of what it is worth.

For contrast, the two alternatives that were costed and rejected. Making the same ballast as
liquid nitrogen is 0.45 MWh per tonne — **475 MWh**, five times the whole cycle, or 5.8× the
cryogenic plant to do it inside one cycle. Filling from 1,350 m up a long hose so the ship never
meets the dense air is **44 MWh**, and needs a 2 m bore at 140 bar. Borrowing mass from the lake
and giving it back is 0.60 MWh. When a mechanism is nearly three orders of magnitude cheaper than the
alternatives, that is usually the design telling you something.

Against that, generation. The only sources the code credits are the solar skin at a flat
45 W/m² and the nitrogen recovery. **That was 200 W/m² until 2026-08-09, in five separate files,
and it required 76% conversion of the 264 W/m² day-averaged incident that NRCan's dataset actually
gives for the BC interior in July.** At 45 — 264 × 0.21 module × 0.81 for curvature, cell
temperature, soiling and conversion — the generation column falls by a factor of 4.4 and the
deficit roughly doubles on the largest class. The generators each class advertises — 8, 40 and
150 MW — supply thrust authority and no energy at all; that is Defect 6, and it is large
enough to change the conclusion drawn from the next table.

| | solar | per cycle | cycle spend (planned) | deficit |
|---|---:|---:|---:|---:|
| P-100 | 0.27 MW | 0.15 MWh | 1.25 MWh | 1.10 MWh |
| P-1000 | 1.26 MW | 0.74 MWh | 7.40 MWh | 6.66 MWh |
| P-10000 | 5.40 MW | 4.10 MWh | 45.87 MWh | 41.77 MWh |

Every hull runs a deficit every cycle. That is stated on the page, and it is the conclusion
the project draws in public: without an energy import chain the fleet is a battery being
spent. On the planned budget a P-10000 has **36.3 hours** of work in it — 2,000 MWh of storage
against a 41.77 MWh deficit per 0.765-hour cycle, so **47.9 cycles**. The smaller two are far worse
off, at **10.4 and 10.6 hours**, because their batteries scale with dry mass while their solar
scales with projected area, and honest solar hurts the small hulls hardest.

Those numbers halved on 2026-08-09 when the solar figure was corrected, and **the project's public
conclusion got stronger, not weaker**: a fleet with ten hours in it is unambiguously a battery
being spent. Defect 6 is the remaining reason this may still be an artefact — 150 MW of generators
that supply thrust authority and no energy at all are still uncounted, and correcting that would
push in the other direction.

**The budget does not close against the model's own second opinion.** `state.js → stateAt`
reports an instantaneous draw for every system at every moment, and `app/loop.js`
integrates it to drive the storage gauge. Measured over one whole cycle of each of the three
sampled missions in `tests/golden/seed7-snapshot.json`, whose legs are about 19 km rather
than the 15 km of the table above, so the totals are not comparable with it:

| | integrated `stateAt` draw | `planCycle` total | ratio | ratio before the resize |
|---|---:|---:|---:|---:|
| P-100 | 2.59 MWh | 2.12 MWh | 1.23× | 1.14× |
| P-1000 | 26.18 MWh | 14.44 MWh | 1.81× | 1.58× |
| P-10000 | 255.45 MWh | 90.18 MWh | 2.83× | 2.29× |

**The resize made the disagreement worse on every class, and the mechanism is diagnostic.**
`planCycle` shrank, because the letdown term it is dominated by fights a smaller surplus.
`stateAt` grew, because it now evaluates lift where the ship actually is: at the bottom of
the cycle the air is thick and the surplus the rotors trim against is 24% larger than the
single ceiling figure the plan uses. Two implementations of one quantity moving in opposite
directions when the physics improves is what Defect 2 looks like from outside.

The rotor term is still three quarters of the integrated total, and it is three quarters of
it because hover momentum theory is being applied to a hull in 36 m/s cruise (§7).

Both numbers are visible on the page simultaneously: at 15 km the worked example reads
88.2 MWh per cycle while the storage gauge beside it drains at a rate the same cycle would
put near 250 MWh. Predicted endurance differs by a factor of three either way. See
Defect 2.

---

## 10. Sensitivity

Each constant moved ±20% from default, P-10000 at 15 km, balanced, still air. Where the
response is asymmetric it is because a threshold (`battLimited`, or the retention clamp)
flips.

| Constant | −20% → energy per cycle | +20% → energy per cycle | −20% → t/h | +20% → t/h |
|---|---:|---:|---:|---:|
| `propEta` | +13.4% | −8.9% | 0% | 0% |
| `Cd` | −10.1% | +10.1% | 0% | 0% |
| `rhoAir` | −9.7% | +9.8% | 0% | 0% |
| `pumpEta` | +5.9% | −4.0% | 0% | 0% |
| `hoseMul` | −4.2% | +4.3% | 0% | 0% |
| `rhoSL` | −3.5% | +27.3% | 0% | 0% |
| `rtLN2` | +0.8% | −0.8% | 0% | 0% |
| `eLN2` | 0.0% | 0.0% | 0% | 0% |
| `solarWPerM2` | 0.0% | 0.0% | 0% | 0% |

| Class parameter | −20% → energy | +20% → energy | −20% → t/h | +20% → t/h |
|---|---:|---:|---:|---:|
| `cruiseKph` | −15.1% | +23.9% | −8.2% | +6.3% |
| `anchorBagT` | +11.7% | −3.0% | 0% | 0% |
| `dropKm` | −10.7% | +10.7% | +7.7% | −6.7% |
| `fillM3s` | +3.4% | −2.3% | −10.9% | +8.9% |
| `dispM3` | −3.5% | +27.3% | 0% | 0% |
| `diskM2` | +0.4% | −0.3% | 0% | 0% |
| `battMW` | 0% | 0% | 0% | 0% |
| `anchorM` | 0% | 0% | 0% | 0% |
| `solarM2` | 0% | 0% | 0% | 0% |

Read five things off this. First, **the two constants corrected on 2026-08-09 now move nothing**:
`rtLN2` is down to ±0.8% because the credit it scales is four times smaller, and `solarWPerM2`
moves the headline by exactly 0.0% because generation is not in `planCycle`'s ledger at all. The
second of those is Defect 6 wearing a different hat: the model spent a day being wrong by 4.4×
about its own generation and **no published figure noticed**, which is the sharpest available
statement of why a term missing from a sum cannot be caught by a test. `eLN2` is inert for the
older reason — the plant makes 21 t of nitrogen per cycle against a tank sized for a rescue. Second, **the top of both tables is
now aerodynamics and speed, not lift**: `cruiseKph`, `propEta`, `Cd` and `rhoAir` are four of the
top five, and three of them are the crude drag model that is Defect 2. The model's uncertainty
has migrated into the part of it that is weakest. Third, `solarM2` changes nothing at all, because
generation is not part of `planCycle`'s ledger — it only appears in the storage integration.
Fourth, `diskM2` and `battMW` have gone quiet — ±20% of the battery peak moves **nothing at all**,
and the disc area moves 0.4% — because the anchor took the descent off the rotors. Both numbers
were sized by a descent balance that no longer binds; that is `docs/OPEN-QUESTIONS.md` #8. Fifth,
`anchorBagT` is now the second most powerful lever in the model and it is not on the page, has no
slider, and appears in no sensitivity discussion before this line: shrinking the bag 20% costs
12.5% more energy per cycle.

`hoseMul` is a different number than it was: while the larger classes carried 1,350 m hoses to
keep out of the dense air, shortening the hose pushed them into retaining water and throughput
fell off a cliff the table could not show. With the anchor doing that job the hose only moves pump
work, and it moves it symmetrically.

The non-monotonic entries are cliff edges, not curves. `rhoSL` is the sharpest: −20% costs 3.7%
and +20% costs **29.2%**, because a denser column means more surplus to push down and the anchor
starts running out of authority. `dispM3` moves identically, since the two enter the ledger as a
product. The model has discontinuities in its response surface and does
not mark them.

---

## 11. Known defects

Each is quantified below and each has an entry in
[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) giving the options and a recommendation. The
numbering is not one-to-one: Defects 4 and 5 here are the two halves of open question 4,
Defect 6 here is open question 6, and open question 5 — the Esri basemap — is a licensing
and privacy problem rather than a physics one, so it has no entry here.

Three of the six have a `knownFail` test in `tests/cases/` (Defects 2 and 3, plus one
unrelated flag bug). Defects 4, 5 and 6 are asserted by ordinary passing tests instead,
because each of them is a statement about what the code *does* rather than a broken
assertion: `selftest.js` requires `retainedT` to be zero, and no test can fail because a
term is missing from a sum. Defect 1 had the fourth marker; it started passing on
2026-08-09 and was converted into two ordinary tests of the corrected behaviour.

Open, tracked, and being fixed in separate commits. They are stated here with numbers
because the alternative — publishing the figures and letting a reader find these — would be
worse than useless.

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

### Defect 2 — two disagreeing power models

`planCycle` publishes 45.869 MWh per P-10000 cycle at 15 km. On the sampled 19 km missions
the same function says 90.18 MWh while integrating the per-system draws that `stateAt`
reports over that cycle gives 255.45 MWh — 2.83 times as much. The ratio is 1.23× for the
P-100 and 1.81× for the P-1000. All three widened with the 2026-08-09 resize (from 1.14,
1.58 and 2.29), because the plan's letdown shrank while `stateAt`'s rotor trim grew: the
plan prices buoyancy once at the ceiling, and `stateAt` now prices it where the ship is,
which for most of the cycle is lower and thicker. §9 has the numbers.

Both are live. The worked example, the "MWh per cycle" figure in the drawer and
`kwhPerTonne` all come from `planCycle`. The storage gauge, the generation-versus-
consumption dial and the power-exhaustion behaviour all come from the `stateAt` integration
in `app/loop.js`. Predicted endurance differs by a factor of three: 36.3 hours against
roughly 13.

The gap is mostly the rotor term, and mostly §7's forward-flight error: `stateAt` prices
cruise trim with the hover formula and gets 91.9 MW where the correct expression gives
14.4 MW, while `planCycle` never charges cruise rotor trim at all. Neither is right. The
fix has to pick one representation of rotor power and make both surfaces read from it.

### Defect 3 — an unexplained window sets the largest energy term

```js
E.letdown = downMW * Math.min(6, dur.RETURN_TRANSIT * 0.2) / 60;
```

For the P-10000 at 15 km this is 52.3 MW × 1.628 min / 60 = 1.420 MWh, or **3.1%** of the
published cycle energy. It was 34.20 MWh and 45.2% of the cycle before the descent anchor —
the anchor took 96% of the rotor work out of the letdown, which is what turned this from the
largest line in the budget into one of the smallest.

**The defect survives the shrinkage, and this is why it is still here.** The window is still
undefined, and a term that nobody can justify is a term that will be wrong again the moment the
number in front of it grows. It is 1.4 MWh today because the anchor is doing the work; take the
anchor away and the same unexplained `0.2` is back in front of 1,748 MW.

Nothing states what the window is. It is not the duration of the letdown as drawn — the
descent in `stateAt` occupies the last 30% of the return leg, which is 2.44 minutes here,
not 1.63. The `min(6, …)` cap is inactive at every distance below roughly 55 km one-way
(38 km for a P-100, 47 km for a P-1000), so for typical missions the term is really the
bare 0.2 fraction with a cap that never fires.

The interaction with `battLimited` still runs backwards — when the descent is judged
authority-limited the model stretches the return leg by 12% and calls it "a longer,
shallower letdown", without reducing `downMW`, so the letdown energy *rises* by 12% — but
`battLimited` is now false for every class at every distance in the grid, where the P-10000
used to trip it everywhere. The bug is unreachable rather than fixed, which is worse: it
will come back the moment anything tightens the descent budget again.

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
liquid nitrogen: 475 MWh, or 5.8× the cryogenic plant to make it inside one cycle. Delivery is
unchanged, and after the single-pass drop run it is 13,183 t/h for a 45.87 MWh cycle.

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

Covered in §8. 21.1 t of nitrogen against an 11,051 t surplus and a 15,500 t tank; 12.6% of
the cycle's energy for 0.24% of the stated function. `cryoLimited` is now true for **every**
combination in the 135-case grid, where before the resize one — a P-100 in endurance mode on
a 400 km leg — did fill its tanks. The target rose with the honest surplus and the tank cap
stopped binding first, so the flag has gone from almost uninformative to entirely
uninformative. Copy on the concept page and in the mission narration describes the plant as
making the ballast the ship descends on, and within a cycle it does not.

What the plant is not inert for is unpowered recovery, which is what its tank is now sized
by: 65 / 651 / 6,505 MWh to make a hull heavy enough to land itself with no rotors, taking
days rather than a cycle. §8 has the figures. The two jobs should be described separately,
because one of them works.

A related bookkeeping wrinkle: `ln2MakeT` is computed from the *pre-stretch*
`dur.RETURN_TRANSIT`, before the `battLimited` 1.12 multiplier, while `E.letdown` is charged
over the *post-stretch* leg. The plant is credited with 8.145 minutes and the letdown
billed for 9.122.

### Defect 6 — the generators supply thrust but no energy

Each class advertises onboard generation — 8, 40 and 150 MW — and `plan.js` counts it in
full when it sizes rotor authority: `rotorMaxT` is computed from `(battMW + genMW)`, and so
is the `battLimited` bus ceiling. Nothing then credits that generation as energy.
`stateAt` reports only `gen.solar` and `gen.regen`, and `app/loop.js` subtracts every
remaining load from the battery. The vehicle is given the thrust its generators would allow
and flown as though they were switched off.

The size of the missing term, for the 15 km balanced P-10000: the cycle is 0.827 h, so the
generators at full output would make **113.8 MWh** against a published cycle spend of
45.87 MWh. They would cover the cycle before solar was counted. Generators do not run flat
out, so the defensible figure is demand-following output capped at `genMW`; measured that
way over the three sampled missions in `tests/golden/seed7-snapshot.json` — longer legs
than 15 km, so not comparable with the figure above — it is 0.74, 8.2 and 140.9 MWh per
cycle. On those missions the P-100 stops draining its battery and starts charging, the
P-1000's endurance goes from 4.7 hours to 15.4, and the P-10000's from 10.3 to 20.1.

Either calculation is enough to show that the omitted term is the same order as the whole
budget. That matters more than the arithmetic, because the per-cycle deficit in §9 is a
conclusion the project states in public — that every hull runs at a loss and therefore
needs a tanker chain to import energy. That conclusion may be an artefact of not modelling
the generators the vehicle is said to carry. The fix is not free either way: fuel has mass,
and mass is the problem the whole project is about, which is exactly why it should be
modelled rather than assumed in either direction.

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
  14 rotors' downwash on all of it are absent.
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
