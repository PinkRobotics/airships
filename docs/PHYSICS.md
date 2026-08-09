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
| h | pumping head = hose length = fill altitude | 300 / 1,100 / 1,350 m, `CLASSES[*].hoseM` × `CFG.hoseMul` |
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
| P-100 | 22,592 m² | 100 t | 4.43 kg/m² | 5.07 kg/m² on 19,707 m² |
| P-1000 | 104,349 m² | 1,000 t | 9.58 kg/m² | 10.94 kg/m² on 91,372 m² |
| P-10000 | 485,575 m² | 10,000 t | 20.59 kg/m² | 23.50 kg/m² on 425,477 m² |

σ rises with size because dry mass scales as V while area scales as V^(2/3). The lift
budget allows at most σ_max = ρ_work V / S_wet — 9.32, 20.17 and 43.35 kg/m² for the three
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
| `WATER_RELEASE` | `max(0.8, dropKm/(0.45·v)·60) × passes` | 450 → 580 m | payload → retained |
| `BUOYANCY_ESCAPE` | `2 × fixed` | 580 → 0.55·altTop | retained |
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

For the P-10000 at 15 km, balanced, still air, the cycle is 49.59 minutes: 5.0 approach,
9.9 fill, 8.1 out, 15.4 release (3 passes), 2.0 escape, 9.1 return. It delivers 8,944 of the
10,000 t it lifts — the other 1,056 t stays aboard as descent ballast — which is 10,821 t/h
to that fire, 1.21 drops per hour.

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

Water is lifted 250 m from the surface to the tanks through a deployed hose, at the class's
fill rate:

> **P_pump = ρ_w g Q h / η_pump**

P-100: 1000 × 9.81 × 0.5 × 250 / 0.75 = **1.635 MW**. P-1000: 9.81 MW. P-10000: 49.05 MW.

The energy is the potential energy of the payload divided by one lumped efficiency:
0.068 MWh ideal for a P-100 load, 0.091 MWh delivered, 9.08 MWh for a P-10000 load. That
is small — 11% of the P-10000's published cycle energy — and it is the least contentious
number in the model.

The lumped η_pump = 0.75 covers pump, motor, drive, hose friction and the kinetic energy
left in the stream. Hose friction is not separately modelled, which matters more than it
looks: 15 m³/s at a plausible 6 m/s in-hose velocity needs a 1.78 m bore, and the standing
column in a 250 m hose of that bore weighs 625 t. The model neither carries that mass nor
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

Correcting this still breaks the force-closure claim, though by less than it did: the
P-1000 now fits its bus and the P-10000 is 1.4% over rather than 14% over. The 2026-08-09
resize is why — the surplus to be pushed down is measured at altitude now and is 8% smaller
than the sea-level ledger claimed. The model's central structural boast, that the disk area
and battery peak were chosen so the hull can be driven back down to the water with nothing
held back, still survives only under the hover formula, but it is one class and one and a
half percent away from surviving properly.

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

with e_LN2 = 0.45 kWh/kg and rt_LN2 = 0.50.

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

| Term | Equation | MWh | share | pre-resize | resize only |
|---|---|---:|---:|---:|---:|
| `E.WATER_FILL` | `max(0, P_pump × t_fill/60 − E_back)` | 44.299 | 37.8% | 4.332 | 4.332 |
| `E.letdown` | `downMW × min(6, t_ret × 0.2)/60` | 35.709 | 30.5% | 43.619 | 34.196 |
| `E.RETURN_TRANSIT` | `P_drag × 0.55 × t_ret/60 + E_cryo` | 14.705 | 12.6% | 14.608 | 14.705 |
| `E.other` | `P_hotel × t_cycle/60 + P_drag × 0.4 × (approach+escape+release)/60` | 12.888 | 11.0% | 11.650 | 12.888 |
| `E.OUTBOUND_TRANSIT` | `P_drag × t_out/60` | 9.459 | 8.1% | 8.289 | 9.459 |
| **total** | | **117.061** | | 82.498 | 75.580 |

The two right-hand columns are the same budget before any of the 2026-08-09 corrections and
after only the resize. The shape changed completely, and for the better: **the largest term is
now the pump**, which lifts 10,000 t of water 1,350 m, and that is a term with a derivation. It
displaced the letdown, whose only two constants are unexplained (defect 3) and which had been
the biggest line in the budget for the life of the model.

The journey there is worth following. The resize cut the letdown 22%, because a hull sized
honestly fights a smaller surplus. Striking the descent balance at the lake put it back and
more, since the surplus down there is 24% larger. Then the long hose stopped the ship going
down to the lake at all, which cut the letdown to 30.5% — and bought that with pump work, at
3.63 kWh per tonne-kilometre of lift. Trading an unexplained constant for a hydraulic one is
the direction this model wants to move in.

Against that, generation. The only sources the code credits are the solar skin at a flat
200 W/m² and the nitrogen recovery. The generators each class advertises — 8, 40 and
150 MW — supply thrust authority and no energy at all; that is Defect 6, and it is large
enough to change the conclusion drawn from the next table.

| | solar | per cycle | cycle spend (planned) | deficit |
|---|---:|---:|---:|---:|
| P-100 | 1.20 MW | 0.72 MWh | 1.85 MWh | 1.12 MWh |
| P-1000 | 5.60 MW | 3.63 MWh | 14.53 MWh | 10.90 MWh |
| P-10000 | 24.00 MW | 19.91 MWh | 117.06 MWh | 97.15 MWh |

Every hull runs a deficit every cycle. That is stated on the page, and it is the conclusion
the project draws in public: without an energy import chain the fleet is a battery being
spent. On the planned budget a P-10000 has 29.8 hours of work in it — 2,000 MWh of storage
against a 55.67 MWh deficit per 0.830-hour cycle, so 35.9 cycles. It was 27.2 hours before
the resize; the deficit fell faster than the cycle shortened. Defect 6 is the reason that
conclusion may be an artefact rather than a finding.

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
| `propEta` | +26.4% | −13.1% | −2.8% | 0% |
| `Cd` | −6.6% | +6.6% | 0% | 0% |
| `pumpEta` | +3.0% | −2.0% | 0% | 0% |
| `hoseMul` | −6.0% | +6.1% | 0% | 0% |
| `rtLN2` | +1.3% | −1.3% | 0% | 0% |
| `eLN2` | −0.0% | +0.0% | 0% | 0% |
| `rhoAir` | −1.3% | +2.7% | 0% | 0% |
| `rhoSL` | −23.2% | +14.7% | 0% | −22.8% |

`hoseMul` looks mild in that table and is not. Within ±20% it only moves pump work, but the
hose is what keeps the ship out of the dense air near the water: below about ×0.75 the P-10000
can no longer hold itself down on rotors at the fill altitude and starts keeping water back as
ballast, at which point throughput falls away sharply. A sensitivity table sampled at two points
cannot show a cliff, and this one has one.

| Class parameter | −20% → energy | +20% → energy | −20% → t/h | +20% → t/h |
|---|---:|---:|---:|---:|
| `cruiseKph` | +0.9% | +6.9% | −13.7% | +11.9% |
| `diskM2` | +5.3% | −3.9% | 0% | 0% |
| `battMW` | +6.3% | 0% | −1.9% | 0% |
| `fillM3s` | +0.2% | −0.1% | −5.3% | +3.9% |
| `dropKm` | −2.1% | +2.1% | +6.6% | −5.8% |
| `dispM3` | −23.2% | +14.7% | 0% | −22.8% |
| `solarM2` | 0% | 0% | 0% | 0% |

Read four things off this. First, `eLN2` — the assumption with the widest published
uncertainty band and its own slider — changes the headline by nothing, because the plant
makes 21 t of nitrogen per cycle against a tank sized for a rescue. Second, `rhoSL` is still
the most sensitive constant in the model, and it now moves the headline for a defensible
reason: it is the anchor of the whole density column, so it scales lift at every altitude,
and `dispM3` moves the same figures identically because the two enter the ledger as a
product. Third, `solarM2` changes nothing at all, because generation is not part of
`planCycle`'s ledger — it only appears in the storage integration. Fourth, `diskM2` and
`battMW` have got tamer: the +20% `diskM2` response fell from −10.5% to −3.9% and the
`battMW` cliff at −20% is gone, because the 2026-08-09 resize took the P-10000 off the
`battLimited` threshold it used to sit on.

The non-monotonic entries are cliff edges, not curves. At `propEta = 0.56` the P-10000's
rotor authority drops enough that the retention clamp engages and it starts holding back
water; at `rhoSL × 1.2` the surplus grows past what the rotors can push down and throughput
falls by nearly a quarter. The model has discontinuities in its response surface and does
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
about 990 m against a 2,500 m working altitude: drag overstated 15%, induced power
understated 7%. That belongs to Defect 2, and it is pinned by a test so it cannot be lost.

### Defect 2 — two disagreeing power models

`planCycle` publishes 117.061 MWh per P-10000 cycle at 15 km. On the sampled 19 km missions
the same function says 90.18 MWh while integrating the per-system draws that `stateAt`
reports over that cycle gives 255.45 MWh — 2.83 times as much. The ratio is 1.23× for the
P-100 and 1.81× for the P-1000. All three widened with the 2026-08-09 resize (from 1.14,
1.58 and 2.29), because the plan's letdown shrank while `stateAt`'s rotor trim grew: the
plan prices buoyancy once at the ceiling, and `stateAt` now prices it where the ship is,
which for most of the cycle is lower and thicker. §9 has the numbers.

Both are live. The worked example, the "MWh per cycle" figure in the drawer and
`kwhPerTonne` all come from `planCycle`. The storage gauge, the generation-versus-
consumption dial and the power-exhaustion behaviour all come from the `stateAt` integration
in `app/loop.js`. Predicted endurance differs by a factor of three: 27.2 hours against
9.1 hours.

The gap is mostly the rotor term, and mostly §7's forward-flight error: `stateAt` prices
cruise trim with the hover formula and gets 91.9 MW where the correct expression gives
14.4 MW, while `planCycle` never charges cruise rotor trim at all. Neither is right. The
fix has to pick one representation of rotor power and make both surfaces read from it.

### Defect 3 — an unexplained window sets the largest energy term

```js
E.letdown = downMW * Math.min(6, dur.RETURN_TRANSIT * 0.2) / 60;
```

For the P-10000 at 15 km this is 1,259.5 MW × 1.629 min / 60 = 34.20 MWh, or **45.2%** of
the published cycle energy — down from 52.9% before the 2026-08-09 resize, and still the
largest single line in the budget by a factor of two.

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
// before: one ledger, struck at the ceiling
retainedT = Math.max(0, led.surplusT - ln2MakeT - rotorMaxT / 0.6);
// after: struck where the letdown ends
retainedT = Math.min(cls.payloadT, Math.max(0, ledLow.surplusT - ln2MakeT - rotorMaxT / 0.6));
```

`rotorMaxT / 0.6` exceeded the surplus for every class, so `retainedT` was identically zero,
while `narrate()` had branches for "retaining N t as descent ballast", the worked-example
note had one, and `bottleneck` could return "descent ballast — cryogenic capacity". None of
that code could execute. The mechanism was prose.

Two things were wrong, and only one of them was the hull. The resize was expected to revive
retention and did the opposite — a hull sized for fail-safe float-up is more buoyant at sea
level, where it never is, and at the altitude the surplus is now measured at it is *less*
buoyant than the sea-level ledger claimed, so the headroom widened from +122/+9/+5% to
+142/+19/+15%.

The real fault was the altitude of the check. Float-up and descent do not share a worst case:
float-up is hardest at the ceiling, in the thinnest air, and descent is hardest at the lake,
1,200 m lower, where the air is 16% denser and the hull correspondingly more buoyant. Both
were being answered with the ceiling ledger. `planCycle` now carries two — `led` at
`WORK_ALT_MSL` for sizing and float-up, `ledLow` at `TERRAIN_MSL + ALT.source` for everything
that answers to descent:

| | rotorMaxT/0.6 | surplus, ceiling | surplus, lake | headroom, ceiling | headroom, lake | retained |
|---|---:|---:|---:|---:|---:|---:|
| P-100 | 267.2 t | 110.5 t | 137.4 t | ×2.42 | ×1.94 | 0 t |
| P-1000 | 1,318.1 t | 1,105.1 t | 1,374.4 t | ×1.19 | **×0.96** | 48.8 t |
| P-10000 | 12,666.2 t | 11,050.9 t | 13,743.6 t | ×1.15 | **×0.92** | 1,056.3 t |

Below ×1.0 the rotors cannot hold the hull down alone and the shortfall stays in the tanks.
Retention is the shortfall exactly, so the balance closes rather than approximately closing,
and it is clamped at the payload — a hull cannot keep back more water than it went to fetch.
Hitting that clamp raises `descentShort` and the bottleneck says the descent does not close,
rather than quietly delivering less. It is false everywhere in the grid.

The cost is real and is charged: the P-10000 delivers 8,943.7 t of its 10,000, at 10,821 t/h
against 12,052, and 88.17 MWh against 75.58 — `downMW` returns to the full 1,550 MW bus,
`battLimited` is true again, and the return leg carries its 12% authority-limited stretch.
Roughly 10% of the published throughput had been bought by checking the hardest manoeuvre in
air the ship never lands in.

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
generators at full output would make **124.5 MWh** against a published cycle spend of
117.06 MWh. They would cover the cycle before solar was counted. Generators do not run flat
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
