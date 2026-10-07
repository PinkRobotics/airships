# Continuous aerial water delivery by vacuum-lift airship: a first-order model

> **Energy reading, 2026-10-02.** Energy conclusions in this earlier report are superseded by the [generated closure record](../../docs/ENERGY-CLOSURE-2026-10.md).
> Its cited tables now show supplied effort on the prescribed, unsupported profile. They do not establish delivery, endurance, savings or operating cost.
> Historical arrows retain earlier figures. Feasible delivery, cycle minutes, both energy bases and the requirements are in the generated record.

<!--tex:skip-->
**Pink Robotics · 2026-08-09 · v1**

<!--tex:headline THE RESULT | A buoyant hull that never lands turns aerial firefighting from a sortie problem into a flow-rate problem. The reference vehicle here is the \textbf{P-100}: 110 m long, smaller than the Hindenburg, delivering \textbf{175 tonnes an hour indefinitely} --- about 2,100 tonnes in a twelve-hour day against roughly 560 for a very large airtanker, and it does not stop at dusk. Two larger classes are modelled to find where the arithmetic breaks; it breaks on the descent, not on the structure or the power. This paper is that arithmetic and the list of what would have to be true.-->

> **Status.** Every headline quantity below is an output of the simulation in this repository,
> cited by key and verified automatically against `research/figures.json`; figures from catalogued
> sources are cited plainly. Superseded values, historical comparisons and one-off derivations are
> written unmarked and sit outside that gate — they are identified as such where they appear.
> Nothing has been built. The model is first-order throughout, and §8 lists the seventeen defects
> and unjustified assumptions the project has found in itself — fifteen open, two corrected on
> 2026-08-09 and kept in place with what they cost.

The flight model assumes a hull that floats; no drawn hull does, as the [structural assessment](../../docs/FLOAT.md) explains.

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

At sea level, with air at 1.225 kg/m³ and helium at 0.169 kg/m³, a vacuum is about 16% more buoyant than helium. Helium lifts about 14% less than vacuum at that reference state. It also cannot leak away, cannot be embargoed, and cannot be
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

Three classes, geometrically similar, sized by a single safety requirement (§4). **The P-100 is
the reference vehicle and everything below is worked through on it unless it says otherwise.** It
is the smallest of the three and the only one smaller than something that has already flown: 110 m
against the Hindenburg’s 245. The P-1000 and P-10000 are the same arithmetic extrapolated, and §6
is about what that extrapolation runs into.

<!--tex:fig charts/scale.pdf | The three hulls at true relative scale, against the largest aircraft and the largest airship ever flown. Drawn from the same lengths and diameters as the table below. | 0.92-->

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Payload | 100 t<!--f:P100.spec.payloadT--> | 1,000 t<!--f:P1000.spec.payloadT--> | 10,000 t<!--f:P10000.spec.payloadT--> |
| Displacement | 220,000 m³<!--f:P100.spec.dispM3--> | 2,200,000 m³<!--f:P1000.spec.dispM3--> | 22,000,000 m³<!--f:P10000.spec.dispM3--> |
| Length × diameter | 110<!--f:P100.spec.lenM--> × 55 m<!--f:P100.spec.diaM--> | 238<!--f:P1000.spec.lenM--> × 119 m<!--f:P1000.spec.diaM--> | 512<!--f:P10000.spec.lenM--> × 256 m<!--f:P10000.spec.diaM--> |
| Cruise | 90 km/h<!--f:P100.spec.cruiseKph--> | 110 km/h<!--f:P1000.spec.cruiseKph--> | 130 km/h<!--f:P10000.spec.cruiseKph--> |
| Rotors / disc area | 4<!--f:P100.spec.rotors--> / 2,500 m²<!--f:P100.spec.diskM2--> | 6<!--f:P1000.spec.rotors--> / 12,000 m²<!--f:P1000.spec.diskM2--> | 14<!--f:P10000.spec.rotors--> / 160,000 m²<!--f:P10000.spec.diskM2--> |
| Battery | 20 MWh<!--f:P100.spec.battMWh--> | 120 MWh<!--f:P1000.spec.battMWh--> | 2,000 MWh<!--f:P10000.spec.battMWh--> |
| Fill rate | 0.5 m³/s<!--f:P100.spec.fillM3s--> | 3 m³/s<!--f:P1000.spec.fillM3s--> | 15 m³/s<!--f:P10000.spec.fillM3s--> |
| Descent bag | 125 t<!--f:P100.spec.anchorBagT--> | 1,250 t<!--f:P1000.spec.anchorBagT--> | 12,400 t<!--f:P10000.spec.anchorBagT--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

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

The fleet model assumes dry mass equals payload: loaded mass is 2 t per tonne of water.
In its P-10000 scenario, lift is 26,950 t at sea level and 21,050.9 t at 2,500 m, against an assumed 20,000 t loaded mass.
The corresponding lift-to-mass ratios are 1.348 and 1.053.
No structural safety factor, pressure sizing or knockdown establishes this allowance.
A complete hull and equipment bill must fit the assumed mass and pass load tests before this becomes a vehicle.

The separate 52 m structural drawing and its bill disagree in the end caps, in both directions.
These readings retain structural safety factor 1.2 against full sea-level pressure. The favourable basis assumes knockdown 0.65 and a 1,450 MPa carbon-laminate compressive ceiling, both unverified.
Across five readings, the favourable lift-to-mass ratio ranges from 0.751 to 0.998 at sea level and from 0.586 to 0.780 at 2,500 m.
No reading reaches one; none is a checked design because the sizing checks do not resolve station lengths or connections.
The [member census](../../docs/MEMBER-CENSUS.md) records 20 disagreements between the drawing and the bill.

**This is where a correction made on 2026-08-09 belongs.** The ledger previously bought its lift at
sea-level density and spent it at altitude, which overstated lift by 22%. Correcting it grew every
hull by 22.2% and, in doing so, created the descent problem in §6 — the buoyancy that guarantees
the ship comes up is exactly the buoyancy that stops it going back down.

The two extremes are not the same case, and the model evaluates both:

- **Float-up is hardest at the ceiling**, 2,500 m MSL, in the thinnest air.
- **Descent is hardest at the water**, 1,300 m MSL, in air 16% denser.

Nothing else in this model changes conclusions as often as remembering which of those two applies.

## 5. The cycle

Six phases, timed rather than asserted. For the reference P-100 at
15 km<!--f:worked.oneWayKm--> one way:

| Phase | Minutes | What happens |
|---|---:|---|
| `SOURCE_APPROACH` | 2.00<!--f:P100.cycle.durations.SOURCE_APPROACH--> | arrive over the lake, come to a **dead stop**, lower the anchor and pumps |
| `WATER_FILL` | 3.33<!--f:P100.cycle.durations.WATER_FILL--> | pump at 0.5 m³/s<!--f:P100.spec.fillM3s-->, no yaw (the lines would tangle) |
| `OUTBOUND_TRANSIT` | 11.76<!--f:P100.cycle.durations.OUTBOUND_TRANSIT--> | climb and run to the fire at 90 km/h<!--f:P100.spec.cruiseKph--> |
| `WATER_RELEASE` | 3.33<!--f:P100.cycle.durations.WATER_RELEASE--> | one long pass, 450 m AGL |
| `BUOYANCY_ESCAPE` | 2.00<!--f:P100.cycle.durations.BUOYANCY_ESCAPE--> | rise off the line on buoyancy alone, no propulsion |
| `RETURN_TRANSIT` | 11.76<!--f:P100.cycle.durations.RETURN_TRANSIT--> | run back, make nitrogen, let down onto the lake |
| **total** | **34.20<!--f:P100.cycle.cycleMin-->** | 100 t<!--f:P100.cycle.deliveredT--> delivered |

<!--tex:fig charts/throughput.pdf | Sustained delivery, and the cycle behind it. Water handling is the longest part of every cycle, which is the signature of a vehicle that never lands.-->

That is 175 t/h<!--f:P100.cycle.tph--> sustained, and 1.75<!--f:P100.cycle.dropsPerHour--> drops
an hour. Transit is 23.5 of the 34.2 minutes on this class and the model names it as the
bottleneck: water handling is fixed by the pumps while transit grows with every kilometre.

**Compare it to the right quantity.** 175 t/h is not a rival to an airtanker's seventy-tonne drop;
it is a rival to that airtanker's *day*. Twelve hours of a P-100 is about 2,100 tonnes against
roughly 560 for eight sorties, and the airtanker then stops while the airship does not.

**The drop is one pass**, not three. Three circuits meant two turns of a large hull over a fire,
which is a manoeuvre the model had no business assuming. A single long release removes them.

Scaled up, the same cycle gives 1,697 t/h<!--f:P1000.cycle.tph--> and
13,183<!--f:P10000.cycle.tph-->, on cycles of 35.4<!--f:P1000.cycle.cycleMin--> and
45.5 minutes<!--f:P10000.cycle.cycleMin--> — the cycle barely lengthens because only the transit
term scales with distance and none of these scale with payload.

## 6. What limits the size: the descent, and the lake as its solution

### 6.1 The problem

Buoyancy that guarantees the ship rises when loaded must be overcome when it is empty, and it is
worst at the bottom of the letdown where the air is 16% denser than the air the hull was sized in.
**This is the term that decides how large one of these can usefully be**, which is why the two
larger classes are in this paper at all: not as a proposal, but as the arithmetic finding its own
ceiling.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Source buoyant surplus | 135.6 t<!--f:P100.descent.holdAtSourceT--> | 1,366.9 t<!--f:P1000.descent.holdAtSourceT--> | 13,722.5 t<!--f:P10000.descent.holdAtSourceT--> |
| Rotor capability (earlier 1) | 267.2 | 1,318.1 | 12,666.2 |
| Rotor capability (earlier 2) | 141.4 | 687.6 | 7,124.3 |
| Rotor capability (current) | 140.5 t<!--f:P100.descent.rotorCapT--> | 683.3 t<!--f:P1000.descent.rotorCapT--> | 7,079.2 t<!--f:P10000.descent.rotorCapT--> |
| Rotors close (old model)? | yes, ×1.97 | **no** | **no** |

**The reference ship is comfortable and the extrapolations are not.** The P-100 closes with 1.97×
headroom. The P-1000 is 4% short and the P-10000 is 8% short: neither can reach its own water
under power. This was discovered by moving the force balance from the ceiling — where it had
always been struck, and where it closed — to the place where the descent actually ends.

Nothing here is a structural or a power limit. It is geometry and air density, and it is the first
thing that bites as the hull grows.

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

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

### 6.3 What was actually chosen: borrow the lake

Lower a cable with a collapsible bag, fill it, winch it clear of the surface. Water hanging on a
line is downward force at the cost of the lift needed to break the surface — 15 m of it.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Bag | 125 t<!--f:P100.descent.anchorT--> | 1,250 t<!--f:P1000.descent.anchorT--> | 12,400 t<!--f:P10000.descent.anchorT--> |
| Cable | 350 m<!--f:P100.spec.anchorCableM--> | 600 m<!--f:P1000.spec.anchorCableM--> | 850 m<!--f:P10000.spec.anchorCableM--> |
| Pull | 1.2 MN<!--f:P100.descent.anchorPullMN--> | 12.3 MN<!--f:P1000.descent.anchorPullMN--> | 121.6 MN<!--f:P10000.descent.anchorPullMN--> |
| Energy cost (earlier 1) | 0.006 | 0.060 | 0.596 |
| Energy cost (current) | 0.003 MWh<!--f:P100.energy.anchorHoistMWh--> | 0.059 MWh<!--f:P1000.energy.anchorHoistMWh--> | 0.596 MWh<!--f:P10000.energy.anchorHoistMWh--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

**The leverage is in the exponent.** Induced rotor power goes as thrust^1.5. The earlier
model's assumed 90% load transfer gave a stated 97% reduction; that is not an achieved
current-cycle result. Its comparison was 1,748 MW to 52.3 → 1404.8 MW<!--f:P10000.energy.downMW-->,
and 34.20 MWh of letdown effort against 1.420 → 117.284 → 117.168 MWh<!--f:P10000.energy.letdownMWh-->.
The arrows' current terms are supplied effort on the prescribed profile. Actual held inventory,
not nominal bag capacity, determines the present load split.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

That is why the bag is sized to do the *whole* descent rather than to cover the 1,056 t shortfall
that revealed the problem. The shortfall was the symptom; the exponent was the finding.

Three consequences worth stating plainly:

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

- **Every class carries one.** The earlier P-100 sizing model claimed its descent closed
  without the bag and attributed a 1.526 MWh penalty to removing it, against 1.391 → 8.042 → 8.189<!--f:P100.cycle.eCycleMWh-->. That earlier 34% saving is not a current achieved
  result; the current force ledger and actual held inventory decide closure.
- **The mechanism cannot be over-sized.** The most water a ship can lift out of a lake is its own
  surplus lift; a bag equal to the surplus leaves the hull neutral. The physics supplies the
  ceiling.
- **A cable is a much better thing to hang than a hose.** 121.6 MN is about 440 mm of UHMWPE
  massing 125 t — 1.25% of payload in rope, and **not charged as dry mass anywhere in this model.**

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

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

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| Term | MWh |
|---|---:|
| `RETURN_TRANSIT` (drag × 0.55 + cryogenic plant) (earlier 1) | 16.611 |
| `RETURN_TRANSIT` (drag × 0.55 + cryogenic plant) (earlier 2) | 112.360 |
| `RETURN_TRANSIT` (drag × 0.55 + cryogenic plant) (current) | 114.037<!--f:P10000.energy.ledgerMWh.RETURN_TRANSIT--> |
| `WATER_FILL` (pumping 10,000 t up 300 m<!--f:P10000.spec.hoseM-->) (earlier 1) | 10.900 |
| `WATER_FILL` (pumping 10,000 t up 300 m<!--f:P10000.spec.hoseM-->) (earlier 2) | 213.327 |
| `WATER_FILL` (pumping 10,000 t up 300 m<!--f:P10000.spec.hoseM-->) (current) | 213.959<!--f:P10000.energy.ledgerMWh.WATER_FILL--> |
| `other` (hotel + manoeuvring drag) | 13.772[historical] |
| `OUTBOUND_TRANSIT` (drag, loaded) (earlier 1) | 12.926 |
| `OUTBOUND_TRANSIT` (drag, loaded) (earlier 2) | 34.838 |
| `OUTBOUND_TRANSIT` (drag, loaded) (current) | 34.345<!--f:P10000.energy.ledgerMWh.OUTBOUND_TRANSIT--> |
| `letdown` (rotor work, with the anchor deployed) (earlier 1) | 1.420 |
| `letdown` (rotor work, with the anchor deployed) (earlier 2) | 117.284 |
| `letdown` (rotor work, with the anchor deployed) (current) | 117.168<!--f:P10000.energy.letdownMWh--> |
| `anchor` (lifting the bag 15 m) (earlier 1) | 0.596 |
| `anchor` (lifting the bag 15 m) (current) | 0.596<!--f:P10000.energy.anchorHoistMWh--> |
| `recovery` (nitrogen store, credited back) | −1.900<!--f:P10000.energy.ledgerMWh.recovery--> |
| **total** (earlier 1) | 54.325 |
| **total** (earlier 2) | 697.586 |
| **total** (current) | 694.174<!--f:P10000.cycle.eCycleMWh--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

Shares are on the figure rather than in the table. They were in both, and the table's column was
still dividing by the pre-correction 43.0 MWh cycle — so the same seven numbers carried two sets
of percentages on one page. A share is derived and has no figure key, which means the citation
gate cannot see it; the chart computes it from the ledger, so the chart is where it belongs.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

<!--tex:fig charts/ledger.pdf | The reference ship's cycle ledger, printed from the model rather than transcribed. Three quarters of it is the return leg; the anchor is the smallest positive line and it is the reason the letdown is the second smallest.-->

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

<!--tex:fig charts/ledger-limit.pdf | The same ledger at the limit case. The proportions invert: pumping and water handling dominate where flying did, which is the square-cube law seen from the other side.-->

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

13.91 → 80.42 → 81.89 kWh/t<!--f:P100.cycle.kwhPerTonne--> delivered, against
8.45 → 62.50 → 62.25<!--f:P1000.cycle.kwhPerTonne--> for the P-1000 and 5.43 → 69.76 → 69.42<!--f:P10000.cycle.kwhPerTonne--> for
the largest. Larger is cheaper per tonne, as the square-cube law demands — which is the reason to
model the larger classes at all, and §6 is the reason not to assume you can build them.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

Note what dominates on the reference ship and does not at the limit: **the return leg is 75% of a
P-100's cycle** and 32% of a P-10000's. The small ship spends its energy flying; the large one
spends it moving water. That is the same square-cube law seen from the other side.

The bottom two rows were one row until 2026-08-09, and merging them was hiding an error: the
recovery was netted against the pump bill under a `max(0, …)`, so on the smaller classes the
recovery exceeded the pumping and the excess was *deleted*, taking the whole pump bill with it.
Splitting them moved the P-100 from 1.308 to 1.005 MWh. **The lesson generalises: the two most
consequential errors found in this model were both accounting, not physics.**

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

### 7.2 What the cryogenic plant is actually for

The cryogenic plant is not cycle ballast. It is a rescue system, and the two get confused because
they share a tank. As cycle ballast it makes 21.12 t<!--f:P10000.energy.ln2MakeT--> against a
15,500 t<!--f:P10000.spec.ln2CapT--> tank — three orders of magnitude short, and saying so is more
useful than defending it.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

Its real job is unpowered recovery. The tank is sized so that an empty hull can be made heavy
enough to **land with no rotor authority at all**, at ground level rather than at the ceiling —
14,456.1 t<!--f:P10000.lift.ln2ToSinkEmptyAtGroundT--> of ballast to sink an empty P-10000 at
1,000 m<!--f:atmosphere.terrainMslM--> MSL. Filling it costs about 6,505 MWh: 2.7 days at rated
plant power, 12.9 days on solar. That is a rescue that takes days, and it should stop being
confused with a cycle that takes an hour.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

### 7.3 Generation, and the deficit

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| | solar | per cycle | spend | deficit | endurance |
|---|---:|---:|---:|---:|---:|
| P-100 (earlier 1) |  |  | 1.391 | 1.24 |  |
| P-100 (earlier 2) |  |  | 8.042 | 7.89 | 9.2 |
| P-100 (current) | 0.21 MW<!--f:P100.energy.solarMW--> | 0.12 MWh<!--f:P100.energy.solarPerCycleMWh--> | 8.189<!--f:P100.cycle.eCycleMWh--> | 8.07<!--f:P100.energy.deficitPerCycleMWh--> | 1.4 h<!--f:P100.energy.hoursOnBattery--> |
| P-1000 (earlier 1) |  |  | 8.454 | 7.71 |  |
| P-1000 (earlier 2) |  |  | 62.500 | 61.76 | 9.2 |
| P-1000 (current) | 0.97 MW<!--f:P1000.energy.solarMW--> | 0.57 MWh<!--f:P1000.energy.solarPerCycleMWh--> | 62.251<!--f:P1000.cycle.eCycleMWh--> | 61.68<!--f:P1000.energy.deficitPerCycleMWh--> | 1.1 h<!--f:P1000.energy.hoursOnBattery--> |
| P-10000 (earlier 1) |  |  | 54.325 | 50.23 |  |
| P-10000 (earlier 2) |  |  | 697.586 | 693.49 | 30.2 |
| P-10000 (current) | 4.48 MW<!--f:P10000.energy.solarMW--> | 3.39 MWh<!--f:P10000.energy.solarPerCycleMWh--> | 694.174<!--f:P10000.cycle.eCycleMWh--> | 690.78<!--f:P10000.energy.deficitPerCycleMWh--> | 2.2 h<!--f:P10000.energy.hoursOnBattery--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

<!--tex:fig charts/deficit.pdf | What each hull spends against what its skin makes, and how long a full battery lasts.-->

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

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

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

## 8. What is wrong with this model

Seventeen entries are documented in `docs/OPEN-QUESTIONS.md`. Seven were found by inspection,
two by auditing all 89 published claims against the code, four by reading the sources, one by an
outside reader asking a question none of them had, and three by an adversarial review of the
model on 2026-08-10 — including one that says the two power models in §8.5 disagree by 5.05×
rather than the 2.83× recorded there. The four from
the sources are the serious ones and they are given here in full.

### 8.1 The dry-mass budget fails twice, independently — the largest open question

`dryT = payloadT` implies a hull-average density of **0.455 kg/m³** — and it is the same figure on
every class, because displacement is sized per tonne of payload. 100 t inside
220,000 m³<!--f:P100.spec.dispM3--> and 10,000 t inside
22,000,000<!--f:P10000.spec.dispM3--> both come out there. **Choosing the smaller reference ship
does not soften this one**, which is what makes it the concept's single point of failure rather
than a scaling limit.

- **Jenett et al. 2019** (NASA NTRS) — the structural precedent this project cites — gives a bare
  discrete-lattice shell at **0.508 kg/m³** in its own Table 2, at every radius. That is 12% over
  our *entire* dry allowance, before skin, joints, rotors, tanks, batteries, or the 125 t of
  anchor cable §6.3 admits is uncharged.
- **Metlen & Palazotto 2013**'s only real-materials vacuum-lift design has a
  structure-to-buoyancy ratio of **0.94** — structure alone consuming what we allocate to
  structure and payload together.
- **Akhmeteli & Gavrilin 2021** publish a payload fraction of **0.1** against our implied 0.5, on a
  shell of 1.16 kg/m³.

The per-class configured battery comparison below uses the built X-57 pack's 149 Wh/kg reference density (Chin et al., printed p. 2). The electric aircraft it was built for did not fly ([NASA's X-57 lessons learned](https://ntrs.nasa.gov/api/citations/20240006845/downloads/SE_lessonsleared_final.pdf), printed p. 4):

<!-- battery:ratios:start -->
At the 149 Wh/kg reference pack density, the battery alone exceeds the dry allowance on P-100 and P-10000.
The per-class ratio of reference-pack mass to dry allowance is shown below.
The complete nominal floor budget exceeds the dry allowance on P-100, P-1000, P-10000, as its own totals show below.

| Class | MWh/t dry | Reference pack / dry | Floor pack / dry | Complete floor t | Floor / dry |
|---|---|---|---|---|---|
| P-100 | 0.20 | 134.2% | 40.0% | 216.1 | 2.16× |
| P-1000 | 0.12 | 80.5% | 24.0% | 1,803.6 | 1.80× |
| P-10000 | 0.20 | 134.2% | 40.0% | 19,524.2 | 1.95× |

The complete floor uses the budget’s own evidence choices, including its 500 Wh/kg battery assumption; it is separate from the 149 Wh/kg reference-pack comparison.

This comparison comes from [battery-ratios.json](../analysis/battery-ratios.json), configuration and the generated mass budget. It does not establish a buildable pack or a complete aircraft.
<!-- battery:ratios:end -->

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

Four sources, four different objections, one conclusion: **the mass premise is not supported by
the literature this project itself cites.** Everything in §§5–7 is conditional on it.

### 8.2 The solar skin needed 76% conversion efficiency — FIXED 2026-08-09

`state.js` credited 200 W/m² of *electrical output*, continuously, in **five separate files**.
NRCan's dataset gives 6.34 kWh/m²/day mean July horizontal insolation across eight BC interior
fire-belt towns — 264 W/m² incident, day-averaged. 200 out of 264 is **76% conversion**, three and
a half times the best cell ever made in a laboratory.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

It is `CFG.solarWPerM2 = 45`<!--f:assumptions.solarWPerM2--> now: 264 × 0.21 flexible module ×
0.81 for curvature, cell temperature, soiling and conversion, applied to a *projected* area.

<!-- solar:area:start -->
`solarM2` is 85% of each current capsule's projected footprint, a named design assumption
rather than a validated panel layout. See the [generated areas](../analysis/solar-area.json).
<!-- solar:area:end -->

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| | solar | per cycle | deficit | endurance |
|---|---|---|---|---|
| P-100 (earlier 1) |  |  | 0.32 |  |
| P-100 (earlier 2) |  |  | 1.24 | 35.4 |
| P-100 (earlier 3) | 1.20 | 0.68 | 7.89 | 9.2 |
| P-100 (current) | 0.21 MW<!--f:P100.energy.solarMW--> | 0.12 MWh<!--f:P100.energy.solarPerCycleMWh--> | 8.07<!--f:P100.energy.deficitPerCycleMWh--> | 1.4 h<!--f:P100.energy.hoursOnBattery--> |
| P-1000 (earlier 1) |  |  | 3.09 |  |
| P-1000 (earlier 2) |  |  | 7.71 | 22.9 |
| P-1000 (earlier 3) | 5.60 | 3.30 | 61.76 | 9.2 |
| P-1000 (current) | 0.97 MW<!--f:P1000.energy.solarMW--> | 0.57 MWh<!--f:P1000.energy.solarPerCycleMWh--> | 61.68<!--f:P1000.energy.deficitPerCycleMWh--> | 1.1 h<!--f:P1000.energy.hoursOnBattery--> |
| P-10000 (earlier 1) |  |  | 24.81 |  |
| P-10000 (earlier 2) |  |  | 50.23 | 61.1 |
| P-10000 (earlier 3) | 24.00 | 18.20 | 693.49 | 30.2 |
| P-10000 (current) | 4.48 MW<!--f:P10000.energy.solarMW--> | 3.39 MWh<!--f:P10000.energy.solarPerCycleMWh--> | 690.78<!--f:P10000.energy.deficitPerCycleMWh--> | 2.2 h<!--f:P10000.energy.hoursOnBattery--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

**Three things this exposed are worth more than the correction.** The constant was duplicated five
times and wrong in every copy — there is one now, plus one on the far side of the `3d/` boundary
and a parity test that reads both. **No published figure moved**, because generation is not in
`planCycle`'s ledger: cycle energy, throughput and kWh/t came out bit-identical across a 4.4×
change to the vehicle's power supply, which is defect 6 in §8.5 stated as sharply as it can be.
And the honest number strengthens the project's conclusion rather than weakening it.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

*Still open:* 45 W/m² is a 24-hour average — right for energy over a cycle, wrong for power at an
instant. There is no sun at 03:00 and the storage gauge draws it anyway.

### 8.3 `rtLN2` returned more work than the nitrogen contains — FIXED 2026-08-09

`rtLN2 = 0.50` against `eLN2 = 0.45`<!--f:assumptions.eLN2--> kWh/kg recovered **225 kWh per
tonne** of liquid nitrogen. The physical exergy of LN2 at 1 bar against a 288 K ambient is
**173.4 kWh/t** (Arnaiz-del-Pozo et al. 2020; corroborated at 205–214 kWh/t under more favourable
assumptions). The term returned 1.3× the work available in the liquid, before any turbine or
generator efficiency. Not an optimistic efficiency — a violation, and it was on the page.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

It is **0.20<!--f:assumptions.rtLN2-->** now: 90 kWh/t, 52% of the exergy, about what a cryogenic
expander returns with no external heat source. `E.recovery` fell from −4.751 to
−1.900 MWh<!--f:P10000.energy.ledgerMWh.recovery--> and the P-10000's cycle rose to
54.325 → 697.586 → 694.174<!--f:P10000.cycle.eCycleMWh-->. The shared power model limits requested recovered work per tonne before the generator cap; tests cover every selectable control pair, including both extremes.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

### 8.4 The drop may not arrive, and tonnes may be the wrong metric

The US Forest Service's 2022 assessment states that a drop released 1,000 ft above
ground/vegetation "would completely dissipate". `ALT.drop` is 450 m — **1,476 ft** — raised for
hull-clearance reasons that are sound, with the delivery consequence never costed. The model has
no droplet physics: it moves tonnes from a tank to a coordinate.

And AFUE — 27,611 observed drops — reports probability of success **0.56 without ground engagement
against 0.72 with it**, the modal outcome without ground crews being *not effective*. AFUE never
counts tonnes. This project's headline metric is tonnes per hour.

<!--tex:fig charts/sensitivity.pdf | Every constant moved ±20%, measured rather than asserted. The top of the table is aerodynamics and speed; the two constants corrected on 2026-08-09 now move the headline by 0.8% and 0.0%.-->

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

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

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

Defect 7 deserves a sentence of its own. The audit found that the constants nobody had questioned
move the headline more than the defects everyone had: the two undocumented drag multipliers on the
return and manoeuvring phases are worth 16.9 MWh a cycle, while defect 3 — flagged in the README
since the first commit — is worth 1.4.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

## 9. How to check any of this

```
git clone … && cd airships && make check
```

- `make golden` re-runs 151 class/mode/distance/wind combinations and diffs every output against
  `tests/golden/seed7-snapshot.json`.
- `make test` registers 236 tests in 60 suites, with 0 known-failing markers. Corrected defects run as ordinary assertions.
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

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

1. **A discrete-lattice vacuum shell at ≤0.455 kg/m³ including everything.** Nothing in the
   literature is there. This is the concept's single point of failure and no amount of care in the
   rest of the model substitutes for it.
2. **Batteries at 200 Wh/kg pack-level with the rest of the vehicle free.** Not available.
3. **A 12,400 t bucket on a 440 mm cable, and a hull that can hold station over water while it
   hangs there.** The mechanism is a scaled Bambi bucket at 1,265 times the largest
   ever built (9,800 L) — the principle is 43 years old and the engineering is not. Pendulum dynamics under an 512 m hull are not modelled.
4. **A drop from 450 m that arrives as water rather than as mist.** Currently contradicted by the
   USFS's own guidance.
5. **An energy import chain.** The fleet is a battery being spent, and the 2026-08-09 solar
   correction made that sharper rather than softer: the smallest class now has
   9.2 → 1.4 hours<!--f:P100.energy.hoursOnBattery--> of work in it and the largest
   30.2 → 2.2<!--f:P10000.energy.hoursOnBattery-->. Nothing here changes that; §7.3 is where it is
   costed.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

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
who has not cloned anything: `pinkrobotics.ca/research`. Source catalogue: `research/sources.json`; its current entry count is generated in the [repository README](../../README.md).
The collection includes PDFs with provenance, written notes and sources that contradict the project. Claim audit:
`research/evidence-map.md`.

---

*Every figure marked in this document is generated by `tools/figures_dump.js` from the model at
defaults and verified by `tools/check_figures.py`. Figures from cited sources are written plainly
and accounted for in `research/sources.json`.*

[historical] The dated “other” ledger aggregate has no current equivalent. The corrected ledger uses the six named phases and recovery; no current-model citation is claimed for the old aggregate. Both bases and all closing requirements are in [the generated closure comparison](../../docs/ENERGY-CLOSURE-2026-10.md).
