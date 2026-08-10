# Continuous aerial water delivery by vacuum-lift airship: a first-order model

<!--tex:skip-->
**Pink Robotics · 2026-08-09 · v1**

<!--tex:headline THE RESULT | A buoyant hull that never lands turns aerial firefighting from a sortie problem into a flow-rate problem. Modelled at three scales, the largest class delivers \textbf{13,183 tonnes of water an hour}, continuously, for 4.6 kWh a tonne --- and gets cheaper per tonne the larger it is, because buoyancy scales with volume and drag with area. This paper is the arithmetic behind that sentence, and the list of what would have to be true for it to survive contact with hardware.-->

> **Status.** Every headline quantity below is an output of the simulation in this repository,
> cited by key and verified automatically against `research/figures.json`; figures from catalogued
> sources are cited plainly. Superseded values, historical comparisons and one-off derivations are
> written unmarked and sit outside that gate — they are identified as such where they appear.
> Nothing has been built. The model is first-order throughout, and §8 lists the seventeen defects
> and unjustified assumptions the project has found in itself — fifteen open, two corrected on
> 2026-08-09 and kept in place with what they cost.

---

## 1. The problem, and why an airship is a plausible shape for it

Aerial firefighting is a duty cycle problem before it is an aviation problem. A very large
airtanker carries something like 70 t, releases it in seconds, and then spends 30–90 minutes
flying to a base, loading, and flying back. Its instantaneous delivery rate is enormous and its
*sustained* rate is set almost entirely by the turnaround. Helicopters with buckets shorten the
turnaround by dipping from a nearby lake, and pay for it in payload — a Chinook carries about 10 t.

The gap in the middle is a vehicle that dips like a helicopter and carries like a tanker. Nothing
occupies it, and the reason is that lift-per-unit-mass for rotorcraft is bought continuously with
power, so payload and endurance trade against each other directly.

Buoyant flight does not have that trade. A hull that displaces its own weight in air holds
altitude at zero power, and the marginal cost of carrying more is the cost of building a bigger
hull, once. That is the argument for an airship, and it is not a new one: it has been made for
cargo, for surveillance, and for high-altitude platforms for a century, and it has generally lost
to the fact that the vehicle is enormous, slow, and vulnerable to weather.

Firefighting is a plausible exception on three counts. The mission is short-range and repetitive,
so slowness costs little. The vehicle can be uncrewed, so the risk calculus that has historically
killed large airships changes. And — the point of this paper — the water source and the fire are
usually within tens of kilometres of each other, so the duty cycle is dominated by loading and
unloading rather than by transit, which is precisely where a buoyant vehicle wins.

## 2. Why vacuum rather than helium

A vacuum displaces the same air as helium and weighs nothing instead of 0.169 kg/m³, so it is
about 14% more buoyant at sea level. It also cannot leak away, cannot be embargoed, and cannot be
priced by a supply chain with two producers of consequence.

The reason nobody flies one is structural. A gas envelope is in tension and can be a fabric; a
vacuum envelope is in compression and must resist 101 kPa of atmosphere trying to crush it, which
means it must be stiff, which historically means it must be heavy. Lana de Terzi proposed it in
1670 and the arithmetic has failed ever since.

The modern case rests on discrete lattice construction — ultralight periodic cellular structures
assembled from many identical mass-produced parts, which hold their stiffness as they lose density
where foams and honeycombs do not. Applied to the vacuum balloon that moves the binding constraint
**from buckling to strength**, and the distinction is the whole reopening of the question.
Buckling is a geometry failure: sudden, total, and not fixable by a better material. Strength is a
number you can look up, test on a bench, and buy more of. The question stops being *is this
impossible* and becomes *how light can we build it*, which is an engineering question, and those
get answered. Jenett et al.
(NASA, 2019) is this project's structural precedent, and the honest summary of it appears in §8.1:
**their own numbers do not close our mass budget.** Akhmeteli & Gavrilin (2021) reach a positive
result for a vacuum balloon by a different route, and their published payload fraction is 0.1
against our implied 0.5.

So the correct statement is: vacuum lift is not obviously impossible any more, and this model
assumes a structure that the two best available sources say is not yet available. Everything
downstream inherits that assumption.

## 3. The vehicle

Three classes, geometrically similar, sized by a single safety requirement (§4).

<!--tex:fig charts/scale.pdf | The three hulls at true relative scale, against the largest aircraft and the largest airship ever flown. Drawn from the same lengths and diameters as the table below. | 0.92-->

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Payload | 100 t<!--f:P100.spec.payloadT--> | 1,000 t<!--f:P1000.spec.payloadT--> | 10,000 t<!--f:P10000.spec.payloadT--> |
| Displacement | 220,000 m³<!--f:P100.spec.dispM3--> | 2,200,000 m³<!--f:P1000.spec.dispM3--> | 22,000,000 m³<!--f:P10000.spec.dispM3--> |
| Length × diameter | 190<!--f:P100.spec.lenM--> × 47 m<!--f:P100.spec.diaM--> | 404<!--f:P1000.spec.lenM--> × 102 m<!--f:P1000.spec.diaM--> | 876<!--f:P10000.spec.lenM--> × 219 m<!--f:P10000.spec.diaM--> |
| Cruise | 90 km/h<!--f:P100.spec.cruiseKph--> | 110 km/h<!--f:P1000.spec.cruiseKph--> | 130 km/h<!--f:P10000.spec.cruiseKph--> |
| Rotors / disc area | 4<!--f:P100.spec.rotors--> / 2,500 m²<!--f:P100.spec.diskM2--> | 6<!--f:P1000.spec.rotors--> / 12,000 m²<!--f:P1000.spec.diskM2--> | 14<!--f:P10000.spec.rotors--> / 160,000 m²<!--f:P10000.spec.diskM2--> |
| Battery | 20 MWh<!--f:P100.spec.battMWh--> | 120 MWh<!--f:P1000.spec.battMWh--> | 2,000 MWh<!--f:P10000.spec.battMWh--> |
| Fill rate | 0.5 m³/s<!--f:P100.spec.fillM3s--> | 3 m³/s<!--f:P1000.spec.fillM3s--> | 15 m³/s<!--f:P10000.spec.fillM3s--> |
| Descent bag | 125 t<!--f:P100.spec.anchorBagT--> | 1,250 t<!--f:P1000.spec.anchorBagT--> | 12,400 t<!--f:P10000.spec.anchorBagT--> |

Dry mass is set equal to payload in every class. That is an assumption, not a result, and §8.1 is
about it.

## 4. What sizes the hull: fail-safe float-up

The displacement is not chosen to make the numbers work. It is chosen so that a ship that cannot
release its water still rises.

> A hull must be positively buoyant at its working altitude while **fully loaded with water and
> unable to drop it.**

An uncrewed vehicle whose outlets jam must not sink into the fire it is fighting. Making that a
sizing constraint rather than a design goal means the failure mode of a stuck valve is an
inconvenient ascent rather than a crash.

The arithmetic is identical per tonne of payload across the classes because dry mass equals
payload. Loaded mass is 2 t per tonne of payload; air at the 2,500 m<!--f:atmosphere.workAltMslM-->
MSL working ceiling is 0.9569 kg/m³<!--f:atmosphere.rhoAtWorkAlt-->; a 5% margin therefore wants
2,194.7 m³ of displaced air per tonne. Published: 2,200 m³/t, giving
+5.25%<!--f:P10000.lift.floatUpMarginPct--> — 21,050.9 t<!--f:P10000.lift.atWorkAltT--> of lift
against 20,000 t<!--f:P10000.lift.loadedMassT--> of loaded ship.

**This is where a correction made on 2026-08-09 belongs.** The ledger previously bought its lift at
sea-level density and spent it at altitude, which overstated lift by 22%. Correcting it grew every
hull by 22.2% and, in doing so, created the descent problem in §6 — the buoyancy that guarantees
the ship comes up is exactly the buoyancy that stops it going back down.

The two extremes are not the same case, and the model evaluates both:

- **Float-up is hardest at the ceiling**, 2,500 m MSL, in the thinnest air.
- **Descent is hardest at the water**, 1,300 m MSL, in air 16% denser.

Nothing else in this model changes conclusions as often as remembering which of those two applies.

## 5. The cycle

Six phases, timed rather than asserted. For the P-10000 at 15 km<!--f:worked.oneWayKm--> one way:

| Phase | Minutes | What happens |
|---|---:|---|
| `SOURCE_APPROACH` | 5.00<!--f:P10000.cycle.durations.SOURCE_APPROACH--> | arrive over the lake, come to a **dead stop**, lower the anchor and pumps |
| `WATER_FILL` | 11.11<!--f:P10000.cycle.durations.WATER_FILL--> | pump at 15 m³/s<!--f:P10000.spec.fillM3s-->, no yaw (the lines would tangle) |
| `OUTBOUND_TRANSIT` | 8.14<!--f:P10000.cycle.durations.OUTBOUND_TRANSIT--> | climb and run to the fire at 130 km/h<!--f:P10000.spec.cruiseKph--> |
| `WATER_RELEASE` | 11.11<!--f:P10000.cycle.durations.WATER_RELEASE--> | one long pass, 450 m AGL |
| `BUOYANCY_ESCAPE` | 2.00<!--f:P10000.cycle.durations.BUOYANCY_ESCAPE--> | rise off the line on buoyancy alone, no propulsion |
| `RETURN_TRANSIT` | 8.14<!--f:P10000.cycle.durations.RETURN_TRANSIT--> | run back, make nitrogen, let down onto the lake |
| **total** | **45.51<!--f:P10000.cycle.cycleMin-->** | 10,000 t<!--f:P10000.cycle.deliveredT--> delivered |

<!--tex:fig charts/throughput.pdf | Sustained delivery, and the cycle behind it. Water handling is the longest part of every cycle, which is the signature of a vehicle that never lands.-->

That is 13,183 t/h<!--f:P10000.cycle.tph--> and 1.32<!--f:P10000.cycle.dropsPerHour--> drops per
hour. Water handling — fill plus release — is 22.2 of the 45.5 minutes, the largest single
slice of the cycle. The model nonetheless names transit as the bottleneck, because water handling
is fixed by the pumps while transit grows with every kilometre: transit is the term that decides
how the cycle changes, not the one that dominates it at this range.

**The drop is one pass**, not three. Three circuits meant two turns of an 876 m hull over a fire,
which is a manoeuvre the model had no business assuming. A single long release removes them.

## 6. The descent problem, and the lake as its solution

### 6.1 The problem

Buoyancy that guarantees the ship rises when loaded must be overcome when it is empty. Worst at
the bottom of the letdown, over the water:

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Surplus to hold down at the source | 135.6 t<!--f:P100.descent.holdAtSourceT--> | 1,366.9 t<!--f:P1000.descent.holdAtSourceT--> | 13,722.5 t<!--f:P10000.descent.holdAtSourceT--> |
| Rotor capability | 267.2 t<!--f:P100.descent.rotorCapT--> | 1,318.1 t<!--f:P1000.descent.rotorCapT--> | 12,666.2 t<!--f:P10000.descent.rotorCapT--> |
| Closes on rotors alone? | yes, ×1.97 | **no** | **no** |

The two larger classes cannot reach their own water source under power. This was discovered by
moving the force balance from the ceiling — where it had always been struck, and where it closed —
to the place where the descent actually ends.

<!--tex:fig charts/render-anchor.png | The vehicle at the source, rendered from the same model: six pump pods on hoses to the surface, and the anchor cable running down to a bag in the water with its contact rings. The bag is to scale. The wash blows upward because the rotors are pushing the hull down against its own buoyancy.-->

<!--tex:fig charts/descent.pdf | What has to be held down at the water, and what holds it. The bar is the job; the tick is how far the rotors reach unaided. | 0.95-->

### 6.2 Three ways out, costed

1. **Retain water as ballast.** Directly reduces delivery, which is the metric.
2. **Make ballast from air.** Liquefy nitrogen on the return leg. The plant is in the model and it is
   sized for something else (§7.2): at cycle rate it makes 21.12 t<!--f:P10000.energy.ln2MakeT-->
   against a need of thousands. Making the whole 12,400 t as LN2 costs about **475 MWh**, eleven
   times the entire cycle.
3. **Never enter the dense air.** Hover at 1,350 m and fill through a long hose. Costed at
   **44 MWh** a cycle in pump work, with a 2 m bore at 140 bar at the pod.

### 6.3 What was actually chosen: borrow the lake

Lower a cable with a collapsible bag, fill it, winch it clear of the surface. Water hanging on a
line is downward force at the cost of the lift needed to break the surface — 15 m of it.

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Bag | 125 t<!--f:P100.descent.anchorT--> | 1,250 t<!--f:P1000.descent.anchorT--> | 12,400 t<!--f:P10000.descent.anchorT--> |
| Cable | 350 m<!--f:P100.spec.anchorCableM--> | 600 m<!--f:P1000.spec.anchorCableM--> | 850 m<!--f:P10000.spec.anchorCableM--> |
| Pull | 1.2 MN<!--f:P100.descent.anchorPullMN--> | 12.3 MN<!--f:P1000.descent.anchorPullMN--> | 121.6 MN<!--f:P10000.descent.anchorPullMN--> |
| Energy cost | 0.006 MWh<!--f:P100.energy.ledgerMWh.anchor--> | 0.060 MWh<!--f:P1000.energy.ledgerMWh.anchor--> | 0.596 MWh<!--f:P10000.energy.ledgerMWh.anchor--> |

**The leverage is in the exponent.** Induced rotor power goes as thrust^1.5, so moving load off
the rotors pays superlinearly: carrying 90% of the hold on the bag drops the required rotor power
from 1,748 MW to 52.3 MW<!--f:P10000.energy.downMW-->, a 97% reduction, and the letdown term from
34.20 MWh to 1.420 MWh<!--f:P10000.energy.ledgerMWh.letdown-->.

That is why the bag is sized to do the *whole* descent rather than to cover the 1,056 t shortfall
that revealed the problem. The shortfall was the symptom; the exponent was the finding.

Three consequences worth stating plainly:

- **Every class carries one, including the P-100 whose descent closes without it.** Removing its
  bag costs 1.526 MWh a cycle against 1.253<!--f:P100.cycle.eCycleMWh-->: a 34% saving on a class
  that does not need the mechanism. A bucket is cheaper than thrust everywhere.
- **The mechanism cannot be over-sized.** The most water a ship can lift out of a lake is its own
  surplus lift; a bag equal to the surplus leaves the hull neutral. The physics supplies the
  ceiling.
- **A cable is a much better thing to hang than a hose.** 121.6 MN is about 440 mm of UHMWPE
  massing 125 t — 1.25% of payload in rope, and **not charged as dry mass anywhere in this model.**

### 6.4 What the anchor forces on the flight profile

The mechanism only works if the ship is not moving. A 12,400 t bag on an 850 m cable at 130 km/h
is not an anchor, it is an accident. The model therefore requires: a dead stop before the cable
goes out; no yaw while the lines are down; and departure permitted as soon as the pumps clear the
water. This costs the 5-minute<!--f:P10000.cycle.durations.SOURCE_APPROACH--> approach phase and
buys the mechanism.

## 7. The energy ledger

### 7.1 The budget

P-10000, 15 km<!--f:worked.oneWayKm--> one way, balanced, still air. Printed from the model, not
transcribed:

| Term | MWh |
|---|---:|
| `RETURN_TRANSIT` (drag × 0.55 + cryogenic plant) | 14.705<!--f:P10000.energy.ledgerMWh.RETURN_TRANSIT--> |
| `WATER_FILL` (pumping 10,000 t up 300 m<!--f:P10000.spec.hoseM-->) | 10.900<!--f:P10000.energy.ledgerMWh.WATER_FILL--> |
| `other` (hotel + manoeuvring drag) | 10.689<!--f:P10000.energy.ledgerMWh.other--> |
| `OUTBOUND_TRANSIT` (drag, loaded) | 9.459<!--f:P10000.energy.ledgerMWh.OUTBOUND_TRANSIT--> |
| `letdown` (rotor work, with the anchor deployed) | 1.420<!--f:P10000.energy.ledgerMWh.letdown--> |
| `anchor` (lifting the bag 15 m) | 0.596<!--f:P10000.energy.ledgerMWh.anchor--> |
| `recovery` (nitrogen store, credited back) | −1.900<!--f:P10000.energy.ledgerMWh.recovery--> |
| **total** | **45.869<!--f:P10000.cycle.eCycleMWh-->** |

Shares are on the figure rather than in the table. They were in both, and the table's column was
still dividing by the pre-correction 43.0 MWh cycle — so the same seven numbers carried two sets
of percentages on one page. A share is derived and has no figure key, which means the citation
gate cannot see it; the chart computes it from the ledger, so the chart is where it belongs.

<!--tex:fig charts/ledger.pdf | The cycle ledger, printed from the model rather than transcribed. The anchor is the smallest positive line, and it is the reason the letdown is the second smallest.-->

4.59 kWh/t<!--f:P10000.cycle.kwhPerTonne--> delivered, against
7.40<!--f:P1000.cycle.kwhPerTonne--> for the P-1000 and 12.53<!--f:P100.cycle.kwhPerTonne--> for the
P-100. Larger is cheaper per tonne, as the square-cube law demands.

The bottom two rows were one row until 2026-08-09, and merging them was hiding an error: the
recovery was netted against the pump bill under a `max(0, …)`, so on the smaller classes the
recovery exceeded the pumping and the excess was *deleted*, taking the whole pump bill with it.
Splitting them moved the P-100 from 1.308 to 1.005 MWh. **The lesson generalises: the two most
consequential errors found in this model were both accounting, not physics.**

### 7.2 What the cryogenic plant is actually for

The cryogenic plant is not cycle ballast. It is a rescue system, and the two get confused because
they share a tank. As cycle ballast it makes 21.12 t<!--f:P10000.energy.ln2MakeT--> against a
15,500 t<!--f:P10000.spec.ln2CapT--> tank — three orders of magnitude short, and saying so is more
useful than defending it.

Its real job is unpowered recovery. The tank is sized so that an empty hull can be made heavy
enough to **land with no rotor authority at all**, at ground level rather than at the ceiling —
14,456.1 t<!--f:P10000.lift.ln2ToSinkEmptyAtGroundT--> of ballast to sink an empty P-10000 at
1,000 m<!--f:atmosphere.terrainMslM--> MSL. Filling it costs about 6,505 MWh: 2.7 days at rated
plant power, 12.9 days on solar. That is a rescue that takes days, and it should stop being
confused with a cycle that takes an hour.

### 7.3 Generation, and the deficit

| | solar | per cycle | spend | deficit | endurance |
|---|---:|---:|---:|---:|---:|
| P-100 | 0.27 MW<!--f:P100.energy.solarMW--> | 0.15 MWh<!--f:P100.energy.solarPerCycleMWh--> | 1.253<!--f:P100.cycle.eCycleMWh--> | 1.10<!--f:P100.energy.deficitPerCycleMWh--> | 10.4 h<!--f:P100.energy.hoursOnBattery--> |
| P-1000 | 1.26 MW<!--f:P1000.energy.solarMW--> | 0.74 MWh<!--f:P1000.energy.solarPerCycleMWh--> | 7.399<!--f:P1000.cycle.eCycleMWh--> | 6.66<!--f:P1000.energy.deficitPerCycleMWh--> | 10.6 h<!--f:P1000.energy.hoursOnBattery--> |
| P-10000 | 5.40 MW<!--f:P10000.energy.solarMW--> | 4.10 MWh<!--f:P10000.energy.solarPerCycleMWh--> | 45.869<!--f:P10000.cycle.eCycleMWh--> | 41.77<!--f:P10000.energy.deficitPerCycleMWh--> | 36.3 h<!--f:P10000.energy.hoursOnBattery--> |

<!--tex:fig charts/deficit.pdf | What each hull spends against what its skin makes, and how long a full battery lasts.-->

**Every hull runs a deficit every cycle, and this is the project's central public conclusion:
without an energy import chain the fleet is a battery being spent.** It is not a perpetual machine
and does not claim to be.

One open defect still attacks this table. The generation each class advertises —
8<!--f:P100.spec.genMW-->, 40<!--f:P1000.spec.genMW--> and 150 MW<!--f:P10000.spec.genMW--> — is
counted for thrust authority and never as energy. Crediting it would not shrink the deficit: that
generation runs on the nitrogen store, which is storage rather than a source, and its round trip
loses. Modelling it honestly moves the conclusion further in the direction it already points, not
back. The solar half of the table was corrected on 2026-08-09 and the figures above are
post-correction; §8.2 has what moved.

## 8. What is wrong with this model

Seventeen entries are documented in `docs/OPEN-QUESTIONS.md`. Seven were found by inspection,
two by auditing all 89 published claims against the code, four by reading the sources, one by an
outside reader asking a question none of them had, and three by an adversarial review of the
model on 2026-08-10 — including one that says the two power models in §8.5 disagree by 5.05×
rather than the 2.83× recorded there. The four from
the sources are the serious ones and they are given here in full.

### 8.1 The dry-mass budget fails twice, independently — the largest open question

`dryT = payloadT` implies a hull-average density of **0.455 kg/m³**: 10,000 t of
everything-that-is-not-water inside 22,000,000 m³<!--f:P10000.spec.dispM3-->.

- **Jenett et al. 2019** (NASA NTRS) — the structural precedent this project cites — gives a bare
  discrete-lattice shell at **0.508 kg/m³** in its own Table 2, at every radius. That is 12% over
  our *entire* dry allowance, before skin, joints, rotors, tanks, batteries, or the 125 t of
  anchor cable §6.3 admits is uncharged.
- **Metlen & Palazotto 2013**'s only real-materials vacuum-lift design has a
  structure-to-buoyancy ratio of **0.94** — structure alone consuming what we allocate to
  structure and payload together.
- **Akhmeteli & Gavrilin 2021** publish a payload fraction of **0.1** against our implied 0.5, on a
  shell of 1.16 kg/m³.
- Independently, every class carries **0.2 MWh of battery per tonne of dry mass**, requiring
  200 Wh/kg at *pack* level with nothing left for anything else. NASA flew 149 Wh/kg on X-57;
  Lvovich (2020) sees no clear path past 500 Wh/kg at pack level, where the battery still consumes
  40% of the budget.

Four sources, four different objections, one conclusion: **the mass premise is not supported by
the literature this project itself cites.** Everything in §§5–7 is conditional on it.

### 8.2 The solar skin needed 76% conversion efficiency — FIXED 2026-08-09

`state.js` credited 200 W/m² of *electrical output*, continuously, in **five separate files**.
NRCan's dataset gives 6.34 kWh/m²/day mean July horizontal insolation across eight BC interior
fire-belt towns — 264 W/m² incident, day-averaged. 200 out of 264 is **76% conversion**, three and
a half times the best cell ever made in a laboratory.

It is `CFG.solarWPerM2 = 45`<!--f:assumptions.solarWPerM2--> now: 264 × 0.21 flexible module ×
0.81 for curvature, cell temperature, soiling and conversion, applied to a *projected* area —
`solarM2` is 80–87% of each hull's plan ellipse, so the curvature is paid for once, in the area.

| | solar | per cycle | deficit | endurance |
|---|---|---|---|---|
| P-100 | 1.20 → **0.27 MW<!--f:P100.energy.solarMW-->** | 0.68 → **0.15 MWh<!--f:P100.energy.solarPerCycleMWh-->** | 0.32 → **1.10<!--f:P100.energy.deficitPerCycleMWh-->** | 35.4 → **10.4 h<!--f:P100.energy.hoursOnBattery-->** |
| P-1000 | 5.60 → **1.26 MW<!--f:P1000.energy.solarMW-->** | 3.30 → **0.74 MWh<!--f:P1000.energy.solarPerCycleMWh-->** | 3.09 → **6.66<!--f:P1000.energy.deficitPerCycleMWh-->** | 22.9 → **10.6 h<!--f:P1000.energy.hoursOnBattery-->** |
| P-10000 | 24.00 → **5.40 MW<!--f:P10000.energy.solarMW-->** | 18.20 → **4.10 MWh<!--f:P10000.energy.solarPerCycleMWh-->** | 24.81 → **41.77<!--f:P10000.energy.deficitPerCycleMWh-->** | 61.1 → **36.3 h<!--f:P10000.energy.hoursOnBattery-->** |

**Three things this exposed are worth more than the correction.** The constant was duplicated five
times and wrong in every copy — there is one now, plus one on the far side of the `3d/` boundary
and a parity test that reads both. **No published figure moved**, because generation is not in
`planCycle`'s ledger: cycle energy, throughput and kWh/t came out bit-identical across a 4.4×
change to the vehicle's power supply, which is defect 6 in §8.5 stated as sharply as it can be.
And the honest number strengthens the project's conclusion rather than weakening it.

*Still open:* 45 W/m² is a 24-hour average — right for energy over a cycle, wrong for power at an
instant. There is no sun at 03:00 and the storage gauge draws it anyway.

### 8.3 `rtLN2` returned more work than the nitrogen contains — FIXED 2026-08-09

`rtLN2 = 0.50` against `eLN2 = 0.45`<!--f:assumptions.eLN2--> kWh/kg recovered **225 kWh per
tonne** of liquid nitrogen. The physical exergy of LN2 at 1 bar against a 288 K ambient is
**173.4 kWh/t** (Arnaiz-del-Pozo et al. 2020; corroborated at 205–214 kWh/t under more favourable
assumptions). The term returned 1.3× the work available in the liquid, before any turbine or
generator efficiency. Not an optimistic efficiency — a violation, and it was on the page.

It is **0.20<!--f:assumptions.rtLN2-->** now: 90 kWh/t, 52% of the exergy, about what a cryogenic
expander returns with no external heat source. `E.recovery` fell from −4.751 to
−1.900 MWh<!--f:P10000.energy.ledgerMWh.recovery--> and the P-10000's cycle rose to
45.869<!--f:P10000.cycle.eCycleMWh-->. Two tests enforce `rtLN2 × eLN2 × 1000 ≤ 173.4`, one on each
copy of the constant, because a second law is not a tuning bound.

### 8.4 The drop may not arrive, and tonnes may be the wrong metric

The US Forest Service's 2022 assessment states that a drop released 1,000 ft above
ground/vegetation "would completely dissipate". `ALT.drop` is 450 m — **1,476 ft** — raised for
hull-clearance reasons that are sound, with the delivery consequence never costed. The model has
no droplet physics: it moves tonnes from a tank to a coordinate.

And AFUE — 27,611 observed drops — reports probability of success **0.56 without ground engagement
against 0.72 with it**, the modal outcome without ground crews being *not effective*. AFUE never
counts tonnes. This project's headline metric is tonnes per hour.

<!--tex:fig charts/sensitivity.pdf | Every constant moved ±20%, measured rather than asserted. The top of the table is aerodynamics and speed; the two constants corrected on 2026-08-09 now move the headline by 0.8% and 0.0%.-->

### 8.5 The other nine, in one line each

| # | Defect | Cost |
|---|---|---|
| 1 | Lift bought at sea level, spent at altitude | **fixed** 2026-08-09; hulls grew 22.2% |
| 2 | Two power models disagree | `planCycle` vs integrated `stateAt`: **2.83×** on the P-10000 |
| 3 | An unexplained `0.2` sets the letdown window | 1.42 MWh today; was 34.20 before the anchor |
| 4 | Retained ballast is dead code; the plant is inert in-cycle | ballast **fixed**; plant restated (§7.2) |
| 5 | Esri basemap tiles used outside their terms | not physics; blocking for publication |
| 6 | Generators supply peak power but no energy | 150 MW uncounted on the P-10000; §8.2 shows what that concealed |
| 7 | 32 of 89 published figures rest on unjustified constants | two inline drag multipliers are worth **16.9 MWh** |
| 8 | `diskM2`/`battMW` answer a superseded constraint | `battMW` ±20% now moves every figure by **0.0%** |
| 0 | The sizing requirement that ties #1, #4 and #6 together | the tank is sized to land a dead hull, not to ballast a cycle |
| — | Rotor wash over a water surface is unmodelled — not a numbered entry | Suter (2005); a 121.6 MN anchor hangs in it |

Defect 7 deserves a sentence of its own. The audit found that the constants nobody had questioned
move the headline more than the defects everyone had: the two undocumented drag multipliers on the
return and manoeuvring phases are worth 16.9 MWh a cycle, while defect 3 — flagged in the README
since the first commit — is worth 1.4.

## 9. How to check any of this

```
git clone … && cd airships && make check
```

- `make golden` re-runs 151 class/mode/distance/wind combinations and diffs every output against
  `tests/golden/seed7-snapshot.json`.
- `make test` runs 206 tests in 39 suites. Two are marked `knownFail` and **fail on purpose** — a
  defect is not allowed to lose its excuse quietly.
- `make test-node` runs a further 103. Until 2026-08-09 it printed "SKIPPED — no node here" on the
  machine this is developed on, so those 103 were only ever executed by CI and two breaks were
  found by a red badge after a push. They run in a browser now, against the same files, and
  `make check` covers them.
- `make factsheet` regenerates `research/figures.json` from the live model in a real browser;
  `tools/check_figures.py` then fails the build if any number in this paper disagrees with it.
  Every figure marked above passed that check at the commit that carries this file.
- `?seed=7&data=snapshot` makes any run on the live site exactly reproducible.

An independent Python replication reproduces the golden snapshot exactly.

## 10. What would have to be true

In descending order of how likely it is to kill the concept:

1. **A discrete-lattice vacuum shell at ≤0.455 kg/m³ including everything.** Nothing in the
   literature is there. This is the concept's single point of failure and no amount of care in the
   rest of the model substitutes for it.
2. **Batteries at 200 Wh/kg pack-level with the rest of the vehicle free.** Not available.
3. **A 12,400 t bucket on a 440 mm cable, and a hull that can hold station over water while it
   hangs there.** The mechanism is a scaled Bambi bucket at 1,265 times the largest
   ever built (9,800 L) — the principle is 43 years old and the engineering is not. Pendulum dynamics under an 876 m hull are not modelled.
4. **A drop from 450 m that arrives as water rather than as mist.** Currently contradicted by the
   USFS's own guidance.
5. **An energy import chain.** The fleet is a battery being spent, and the 2026-08-09 solar
   correction made that sharper rather than softer: the smallest class now has
   10.4 hours<!--f:P100.energy.hoursOnBattery--> of work in it and the largest
   36.3<!--f:P10000.energy.hoursOnBattery-->. Nothing here changes that; §7.3 is where it is
   costed.

If (1) fails, the rest is a well-tested model of a vehicle that cannot exist. That is why it is
first on the list and why §8.1 is written the way it is.

**What the two corrections of 2026-08-09 say about the other eleven.** Both were found by reading
a source rather than by running the model, both had been on the page for the life of the project,
and neither was catchable by any test that existed — one because generation is absent from the
ledger, the other because a test was asserting the violation as correct behaviour. The eleven
still open should be read in that light: the list is what has been checked, not what is wrong.

## 11. Availability

Model, tests, sources and defect list: `github.com/pinkrobotics/airships`. Live simulation:
`pinkrobotics.ca/airships`. The literature and the nine sources against us, written for a reader
who has not cloned anything: `pinkrobotics.ca/research`. Source catalogue: `research/sources.json` — 73 entries, 29
redistributable PDFs with provenance, 12 written notes, 9 sources that contradict us. Claim audit:
`research/evidence-map.md`.

---

*Every figure marked in this document is generated by `tools/figures_dump.js` from the model at
defaults and verified by `tools/check_figures.py`. Figures from cited sources are written plainly
and accounted for in `research/sources.json`.*
