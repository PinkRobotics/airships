# The physics

This document states the model in the order a physicist would want it: what lifts the
vehicle, what the shell would have to be, what one delivery cycle costs, and where the
arithmetic fails. Every equation is the one in the code. Every constant is given with its
value, its provenance, and how much the headline figures move when it moves.

No such aircraft exists. Nothing here is validated against a built vehicle, because there
is no built vehicle. This is arithmetic on stated assumptions, published so that the
assumptions can be attacked. Six defects are known and open; they have their own section
and they are not hidden anywhere else in the document.

Symbol-to-function references are in [`../sim/README.md`](../sim/README.md), which indexes
every published number to the line that computes it.

---

## Notation

| Symbol | Meaning | Value or source |
|---|---|---|
| ρ_SL | sea-level air density | 1.225 kg/m³, ISA |
| ρ_air | working air density used for drag and rotors | 1.10 kg/m³, `DEFAULTS.rhoAir` |
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
| h | pumping head | 250 m, `DEFAULTS.hoseHead` |
| Q | fill rate | `CLASSES[*].fillM3s` |

SI throughout, surfaced as tonnes, kilometres, minutes, megawatts and megawatt-hours. One
tonne of water is one cubic metre.

---

## 1. Lift and the mass ledger

The hull is a vacuum vessel. It lifts the mass of the air it displaces, with nothing
inside to subtract:

> **L = ρ V**

`physics.js → ledger()` evaluates this at ρ = ρ_SL and calls the result `liftT`. The dry
mass is set equal to the payload — one tonne of vehicle per tonne of water — and the model
is explicit that this is the ledger's bet, not a mass estimate. The three classes are
geometrically similar (fineness ratio 4, displacement matching a prolate spheroid to
better than 0.4%), so their ledgers are the same ledger scaled:

| | displacement | L at ρ_SL | dry | payload | surplus, empty | reserve, full |
|---|---:|---:|---:|---:|---:|---:|
| P-100 | 180,000 m³ | 220.5 t | 100 t | 100 t | 120.5 t | 20.5 t |
| P-1000 | 1,800,000 m³ | 2,205 t | 1,000 t | 1,000 t | 1,205 t | 205 t |
| P-10000 | 18,000,000 m³ | 22,050 t | 10,000 t | 10,000 t | 12,050 t | 2,050 t |

The loaded reserve is 10.25% of gross weight in all three cases — equivalently 9.3% of the
displacement lift. That margin is the whole basis of the site's claim that the rotors only
ever push the hull *down*.

**The break-even density is identical for all three classes**, because the ratio
(m_dry + m_pay)/V is identical:

> ρ* = 2 m_pay / V = **1.1111 kg/m³** loaded, **0.5556 kg/m³** empty

1.1111 kg/m³ is ISA density at 1,005 m. The model's own `rhoAir = 1.10` — the density it
uses for every drag and rotor calculation — is *below* the loaded break-even. See Defect 1.

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

| | wetted area | dry allowance | implied σ |
|---|---:|---:|---:|
| P-100 | 19,707 m² | 100 t | 5.07 kg/m² |
| P-1000 | 91,372 m² | 1,000 t | 10.94 kg/m² |
| P-10000 | 425,477 m² | 10,000 t | 23.50 kg/m² |

σ rises with size because dry mass scales as V while area scales as V^(2/3). The lift
budget allows at most σ_max = ρ_SL V / S_wet — 11.19, 24.13 and 51.82 kg/m² for the three
classes — and the assumed values are 45.3% of that in every case, identically, because
m_dry = m_pay = L/2.205 by construction. So the shell, the machinery, the batteries and the
rotors together are given a little under half of what buoyancy would permit. That is a
statement about the lift budget only. It says nothing about whether such a shell can be
built.

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
820 m hull, and each must absorb 111 MW of the 1,550 MW bus. A 5 MW wind turbine of that
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

For the P-10000 at 15 km, balanced, still air, the cycle is 50.76 minutes: 5.0 approach,
11.1 fill, 8.1 out, 15.4 release (3 passes), 2.0 escape, 9.1 return. It delivers 10,000 t,
which is 11,820 t/h to that fire, 1.18 drops per hour.

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

referenced to frontal area, cubed in airspeed. At default settings: P-100 0.93 MW,
P-1000 7.94 MW, P-10000 61.06 MW.

C_d = 0.05 on frontal area is equivalent to a volumetric coefficient of

> C_dv = C_d A_f / V^(2/3) = **0.024**

for all three classes. That is inside the normal band for a bare streamlined body of
revolution at high Reynolds number and is not an unreasonable figure. A check on it: at
cruise the P-10000 sits at Re ≈ 2 × 10⁹, giving a flat-plate C_f of about 0.00145, and
skin friction over 425,477 m² of wetted area comes to 441 kN against the model's total
drag of 1,184 kN. Friction is 37% of the assumed total, leaving 63% for form drag and
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
7.08 × 10⁷ N over 160,000 m², which is 443 N/m² — a helicopter figure — with an induced
velocity of 14.2 m/s. That is a 14 m/s downwash over the lake or over the fire, which the
model does not otherwise account for.

Two places where the formula is the wrong one:

**In forward flight it overstates induced power badly.** Hover momentum theory assumes the
disk draws still air. At airspeed v the induced velocity solves the Glauert relation
v_i = T/(2ρA√(v² + v_i²)), and induced power falls towards T²/(2ρAv). On the P-10000's
return leg at 36.1 m/s, holding the empty hull down, the model charges 91.9 MW where the
Glauert expression gives 14.4 MW — a factor of **6.4**. The P-100 and P-1000 are
overstated by 5.5× and 4.7× on the same comparison. This is the single largest reason the
integrated power model (§9) exceeds the planned one.

**In axial descent it understates.** When the vehicle is descending at rate v_c with the
rotors pushing down, the correct ideal power is T(v_c + v_i) with
v_i = −v_c/2 + √((v_c/2)² + v_h²). At v_c = 6 m/s, `VZ_MAX`, with the thrust the descent
actually asks for — the rotors' 0.6 share of the full empty surplus, 72.3 / 723 / 7,230 t:

| | model, hover form | axial-descent form | bus |
|---|---:|---:|---:|
| P-100 | 11.5 MW | 14.9 MW (+30%) | 38 MW |
| P-1000 | 166.1 MW | 199.2 MW (+20%) | 190 MW |
| P-10000 | 1,438 MW | 1,774 MW (+23%) | 1,550 MW |

Correcting this breaks the force-closure claim: at `VZ_MAX` both the P-1000 and the
P-10000 need more power than their buses have. The model's central structural boast — that
the disk area and battery peak were chosen so the hull can be driven back down to the water
with nothing held back — survives only under the hover formula.

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
5,000 t tank and a 12,050 t buoyancy surplus. `ln2NeedT` is the smaller of 80% of that
surplus and the tank, so the function asks for 5,000 t and gets 0.42% of it; measured
against the 9,640 t the ballast target would be without the tank cap it is 0.22%. It costs
11.5% of the cycle's published energy to do that. The
recovered 4.75 MWh is real but arrives during the fill, where on the smaller two classes it
exceeds the entire pumping bill and the excess is silently discarded by a `max(0, …)`.

To make the mechanism work at the stated energy intensity, the P-10000 would have to
liquefy roughly 9,640 t of nitrogen per cycle, costing 4,338 MWh — more than twice its
entire battery, per drop. Nitrogen ballast at this scale is not an efficiency question; it
is off by three orders of magnitude. The honest statement is that the cryogenic plant, as
modelled, is decoration.

---

## 9. The energy budget, and why it does not close

`planCycle` builds a per-phase energy ledger. For the P-10000 at 15 km, balanced, still
air:

| Term | Equation | MWh | share |
|---|---|---:|---:|
| `E.letdown` | `downMW × min(6, t_ret × 0.2)/60` | 43.619 | 52.9% |
| `E.RETURN_TRANSIT` | `P_drag × 0.55 × t_ret/60 + E_cryo` | 14.608 | 17.7% |
| `E.other` | `P_hotel × t_cycle/60 + P_drag × 0.4 × (approach+escape+release)/60` | 11.650 | 14.1% |
| `E.OUTBOUND_TRANSIT` | `P_drag × t_out/60` | 8.289 | 10.0% |
| `E.WATER_FILL` | `max(0, P_pump × t_fill/60 − E_back)` | 4.332 | 5.3% |
| **total** | | **82.498** | |

Against that, generation. The only sources the code credits are the solar skin at a flat
200 W/m² and the nitrogen recovery. The generators each class advertises — 8, 40 and
150 MW — supply thrust authority and no energy at all; that is Defect 6, and it is large
enough to change the conclusion drawn from the next table.

| | solar | per cycle | cycle spend (planned) | deficit |
|---|---:|---:|---:|---:|
| P-100 | 1.20 MW | 0.72 MWh | 1.70 MWh | 0.98 MWh |
| P-1000 | 5.60 MW | 3.63 MWh | 11.89 MWh | 8.26 MWh |
| P-10000 | 24.00 MW | 20.31 MWh | 82.50 MWh | 62.19 MWh |

Every hull runs a deficit every cycle. That is stated on the page, and it is the conclusion
the project draws in public: without an energy import chain the fleet is a battery being
spent. On the planned budget a P-10000 has 27.2 hours of work in it — 2,000 MWh of storage
against a 62.19 MWh deficit per 0.846-hour cycle, so 32.2 cycles. Defect 6 is the reason
that conclusion may be an artefact rather than a finding.

**The budget does not close against the model's own second opinion.** `state.js → stateAt`
reports an instantaneous draw for every system at every moment, and `app/loop.js`
integrates it to drive the storage gauge. Over the identical cycle:

| | integrated `stateAt` draw | `planCycle` total | ratio |
|---|---:|---:|---:|
| P-100 | 2.03 MWh | 1.70 MWh | 1.19× |
| P-1000 | 20.77 MWh | 11.89 MWh | 1.75× |
| P-10000 | 211.18 MWh | 82.50 MWh | 2.56× |

Broken down for the P-10000: rotors 160.94 MWh, propulsion 21.18, pumps 9.08, cryogenic
plant 9.05, fans 8.07, hotel 2.54, winch 0.32. The rotor term is three quarters of it, and
it is three quarters of it because hover momentum theory is being applied to a hull in
36 m/s cruise (§7). Endurance on this basis is 9.1 hours, not 27.2.

Both numbers are visible on the page simultaneously: the worked example reads 82.5 MWh per
cycle while the storage gauge beside it drains at 211 MWh per cycle. See Defect 2.

---

## 10. Sensitivity

Each constant moved ±20% from default, P-10000 at 15 km, balanced, still air. Where the
response is asymmetric it is because a threshold (`battLimited`, or the retention clamp)
flips.

| Constant | −20% → energy per cycle | +20% → energy per cycle | −20% → t/h | +20% → t/h |
|---|---:|---:|---:|---:|
| `propEta` | +9.8% | −18.7% | −8.9% | +2.0% |
| `Cd` | −5.5% | +5.5% | 0% | 0% |
| `pumpEta` | +2.8% | −1.8% | 0% | 0% |
| `hoseHead` | −2.2% | +2.2% | 0% | 0% |
| `rtLN2` | +1.2% | −1.2% | 0% | 0% |
| `eLN2` | −0.0% | +0.0% | 0% | 0% |
| `rhoAir` | −1.5% | −5.2% | −2.1% | +2.0% |
| `rhoSL` | −29.8% | −0.2% | +2.0% | −32.1% |

| Class parameter | −20% → energy | +20% → energy | −20% → t/h | +20% → t/h |
|---|---:|---:|---:|---:|
| `cruiseKph` | +4.8% | +2.9% | −13.9% | +12.0% |
| `diskM2` | +3.9% | −10.5% | −2.1% | +2.0% |
| `battMW` | −7.2% | −6.4% | −7.5% | +2.0% |
| `fillM3s` | +0.2% | −0.1% | −5.2% | +3.8% |
| `dropKm` | −1.7% | +1.7% | +6.5% | −5.7% |
| `solarM2` | 0% | 0% | 0% | 0% |

Read three things off this. First, `eLN2` — the assumption with the widest published
uncertainty band and its own slider — changes the headline by nothing, because the plant
makes 21 t of nitrogen. Second, `rhoSL` is the most sensitive constant in the model, which
is the wrong constant to be most sensitive to (Defect 1). Third, `solarM2` changes nothing
at all, because generation is not part of `planCycle`'s ledger — it only appears in the
storage integration.

The non-monotonic entries are cliff edges, not curves. At `propEta = 0.56` the P-10000's
rotor authority drops enough that the retention clamp engages and it starts holding back
1,113 t of water; at `rhoSL × 1.2` the surplus grows past what the rotors can push down and
throughput falls by a third. The model has discontinuities in its response surface and
does not mark them.

---

## 11. Known defects

Each is quantified below and each has an entry in
[OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) giving the options and a recommendation. The
numbering is not one-to-one: Defects 4 and 5 here are the two halves of open question 4,
Defect 6 here is open question 6, and open question 5 — the Esri basemap — is a licensing
and privacy problem rather than a physics one, so it has no entry here.

Four of the six have a `knownFail` test in `tests/cases/` (Defects 1, 2 and 3, plus one
unrelated flag bug). Defects 4, 5 and 6 are asserted by ordinary passing tests instead,
because each of them is a statement about what the code *does* rather than a broken
assertion: `selftest.js` requires `retainedT` to be zero, and no test can fail because a
term is missing from a sum.

Open, tracked, and being fixed in separate commits. They are stated here with numbers
because the alternative — publishing the figures and letting a reader find these — would be
worse than useless.

### Defect 1 — buoyancy is computed at sea level

`ledger()` evaluates L = ρV at ρ_SL = 1.225 kg/m³ and uses the result at every altitude.
The ships work between 300 m and about 1,180 m above ground, over interior British
Columbia terrain that is itself 500–1,500 m above sea level. Loaded break-even is
1.1111 kg/m³, which is 1,005 m in ISA.

Taking 1,000 m of terrain under the fire and 500 m under the lake:

| Point in the cycle | altitude MSL | ρ | P-10000 net, loaded | water at which it goes heavy |
|---|---:|---:|---:|---:|
| source hold, 300 m AGL | 800 m | 1.1336 | +406 t | 104% of payload |
| drop run, 450 m AGL | 1,450 m | 1.0633 | −860 t | 91% |
| achieved ceiling, 1,180 m AGL | 2,180 m | 0.9884 | −2,209 t | 78% |
| nominal ceiling, 1,500 m AGL | 2,500 m | 0.9569 | −2,777 t | 72% |

The sign of the net force reverses *within a single cycle*. Full over the lake the hull is
just buoyant; full at the drop line it is 860 t heavy; full at the ceiling it is 2,209 t
heavy. The fractions are identical for all three classes.

Consequences: the page's claim that the rotors only ever push down is false on the loaded
leg; `netFrac`, `vert`, every rotor draw and every force readout have the wrong sign for
part of the cycle; and the outbound leg needs rotor thrust *upward* that the model never
charges for. The model does not use `rhoAir` for the ledger even though it uses it for
everything else, and even `rhoAir` would put the loaded hull marginally heavy.

### Defect 2 — two disagreeing power models

`planCycle` publishes 82.498 MWh per P-10000 cycle. Integrating the per-system draws that
`stateAt` reports, over the same cycle, gives 211.18 MWh — 2.56 times as much. The ratio is
1.19× for the P-100 and 1.75× for the P-1000.

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

For the P-10000 at 15 km this is 1,434.5 MW × 1.824 min / 60 = 43.62 MWh, or **52.9%** of
the published cycle energy. It is 44.4% for the P-1000 and 25.9% for the P-100.

Nothing states what the window is. It is not the duration of the letdown as drawn — the
descent in `stateAt` occupies the last 30% of the return leg, which is 2.74 minutes here,
not 1.82. The `min(6, …)` cap is inactive at every distance below roughly 55 km one-way
(38 km for a P-100, 47 km for a P-1000), so for typical missions the term is really the
bare 0.2 fraction with a cap that never fires.

Worse, the interaction with `battLimited` runs backwards. When the descent is judged
authority-limited the model stretches the return leg by 12% and calls it "a longer,
shallower letdown" — but `downMW` is not reduced, so the letdown energy *rises* by 12%,
from 38.95 to 43.62 MWh. A shallower descent that costs more is not a shallower descent.

### Defect 4 — retained descent ballast is zero, everywhere, always

```js
retainedT = Math.max(0, led.surplusT - ln2MakeT - rotorMaxT / 0.6);
```

`rotorMaxT / 0.6` exceeds the surplus for every class, so `retainedT` is identically zero:

| | rotorMaxT/0.6 | surplus | headroom |
|---|---:|---:|---:|
| P-100 | 267.2 t | 120.5 t | +122% |
| P-1000 | 1,318.1 t | 1,205.0 t | +9% |
| P-10000 | 12,666.2 t | 12,050.0 t | +5% |

This is deliberate — the P-10000's disk area and battery peak were sized to make it true,
and `selftest.js` throws if any class retains more than a tonne. The defect is that the
rest of the project describes retention as a live mechanism: `narrate()` has branches for
"retaining N t as descent ballast", the worked-example note has one, and `bottleneck` can
return "descent ballast — cryogenic capacity". None of that code can execute. It should
either be removed or the mechanism should be made real.

The margin is also thinner than it looks. A 7.5% reduction in bus power or in η_p, or a
14.3% reduction in disk area, puts the P-10000 into retention. The behaviour is not robust,
it is tuned.

### Defect 5 — the cryogenic plant is numerically inert

Covered in §8. 21.1 t of nitrogen against a 12,050 t surplus and a 5,000 t tank; 11.5% of
the cycle's energy for 0.42% of the stated function. `cryoLimited` is true for every class
at every distance the fleet can actually fly — a P-100 would need a 5.4-hour return leg to
fill its 50 t tank, against a 25 km search radius — so the flag carries no information for
any reachable mission. Copy on the concept page and in the
mission narration describes the plant as making the ballast the ship descends on, and it
does not.

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

The size of the missing term, for the 15 km balanced P-10000: the cycle is 0.846 h, so the
generators at full output would make **126.9 MWh** against a published cycle spend of
82.50 MWh. They would cover the cycle before solar was counted. Generators do not run flat
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
- **Turbulence and gust loading.** An 820 m hull in the convective column over a fire is a
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
