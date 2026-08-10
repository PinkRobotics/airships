# Continuous aerial water delivery by vacuum-lift airship: a checkable first-order model, and the four places it fails

**Pink Robotics · 2026-08-09 · v1**

> **Status.** Every quantitative statement below is either an output of the simulation in this
> repository, cited by key and verified automatically against `research/figures.json`, or a figure
> from a catalogued source, cited plainly. Nothing has been built. The model is first-order
> throughout and thirteen of its assumptions are known to be wrong or unjustified; §8 lists them
> and four of them are severe. This paper is written to be attacked, and the fastest attacks are
> the ones it makes on itself.

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
assembled from discrete parts, which reach very low densities at usable stiffness. Jenett et al.
(NASA, 2019) is this project's structural precedent, and the honest summary of it appears in §8.1:
**their own numbers do not close our mass budget.** Akhmeteli & Gavrilin (2021) reach a positive
result for a vacuum balloon by a different route, and their published payload fraction is 0.1
against our implied 0.5.

So the correct statement is: vacuum lift is not obviously impossible any more, and this model
assumes a structure that the two best available sources say is not yet available. Everything
downstream inherits that assumption.

## 3. The vehicle

Three classes, geometrically similar, sized by a single safety requirement (§4).

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
| **total** | **45.51**<!--f:P10000.cycle.cycleMin--> | 10,000 t<!--f:P10000.cycle.deliveredT--> delivered |

That is 13,183 t/h<!--f:P10000.cycle.tph--> and 1.32<!--f:P10000.cycle.dropsPerHour--> drops per
hour. Water handling — fill plus release — is 22.2 of the 45.5 minutes, and the model reports the
bottleneck as transit distance at this range because both scale but
only transit scales with distance.

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

### 6.2 Three ways out, costed

1. **Retain water as ballast.** Directly reduces delivery, which is the metric.
2. **Make ballast from air.** Liquefy nitrogen on the return leg. The plant is real and it is
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
  bag costs 1.526 MWh a cycle against 1.005<!--f:P100.cycle.eCycleMWh-->: a 34% saving on a class
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

| Term | MWh | share |
|---|---:|---:|
| `RETURN_TRANSIT` (drag × 0.55 + cryogenic plant) | 14.705<!--f:P10000.energy.ledgerMWh.RETURN_TRANSIT--> | 34.2% |
| `WATER_FILL` (pumping 10,000 t up 300 m<!--f:P10000.spec.hoseM-->) | 10.900<!--f:P10000.energy.ledgerMWh.WATER_FILL--> | 25.3% |
| `other` (hotel + manoeuvring drag) | 10.689<!--f:P10000.energy.ledgerMWh.other--> | 24.8% |
| `OUTBOUND_TRANSIT` (drag, loaded) | 9.459<!--f:P10000.energy.ledgerMWh.OUTBOUND_TRANSIT--> | 22.0% |
| `letdown` (rotor work, with the anchor deployed) | 1.420<!--f:P10000.energy.ledgerMWh.letdown--> | 3.3% |
| `anchor` (lifting the bag 15 m) | 0.596<!--f:P10000.energy.ledgerMWh.anchor--> | 1.4% |
| `recovery` (nitrogen store, credited back) | −4.751<!--f:P10000.energy.ledgerMWh.recovery--> | −11.0% |
| **total** | **43.019**<!--f:P10000.cycle.eCycleMWh--> | |

4.30 kWh/t<!--f:P10000.cycle.kwhPerTonne--> delivered, against
6.39<!--f:P1000.cycle.kwhPerTonne--> for the P-1000 and 10.05<!--f:P100.cycle.kwhPerTonne--> for the
P-100. Larger is cheaper per tonne, as the square-cube law demands.

The bottom two rows were one row until 2026-08-09, and merging them was hiding an error: the
recovery was netted against the pump bill under a `max(0, …)`, so on the smaller classes the
recovery exceeded the pumping and the excess was *deleted*, taking the whole pump bill with it.
Splitting them moved the P-100 from 1.308 to 1.005 MWh. **The lesson generalises: the two most
consequential errors found in this model were both accounting, not physics.**

### 7.2 What the cryogenic plant is actually for

The nitrogen plant makes 21.12 t<!--f:P10000.energy.ln2MakeT--> per cycle against a
15,500 t<!--f:P10000.spec.ln2CapT--> tank. As cycle ballast it is three orders of magnitude short,
and saying so is more useful than defending it.

Its real job is unpowered recovery. The tank is sized so that an empty hull can be made heavy
enough to **land with no rotor authority at all**, at ground level rather than at the ceiling —
14,456.1 t<!--f:P10000.lift.ln2ToSinkEmptyAtGroundT--> of ballast to sink an empty P-10000 at
1,000 m<!--f:atmosphere.terrainMslM--> MSL. Filling it costs about 6,505 MWh: 2.7 days at rated
plant power, 12.9 days on solar. That is a rescue that takes days, and it should stop being
confused with a cycle that takes an hour.

### 7.3 Generation, and the deficit

| | solar | per cycle | spend | deficit | endurance |
|---|---:|---:|---:|---:|---:|
| P-100 | 1.20 MW<!--f:P100.energy.solarMW--> | 0.68 MWh<!--f:P100.energy.solarPerCycleMWh--> | 1.005<!--f:P100.cycle.eCycleMWh--> | 0.32<!--f:P100.energy.deficitPerCycleMWh--> | 35.4 h<!--f:P100.energy.hoursOnBattery--> |
| P-1000 | 5.60 MW<!--f:P1000.energy.solarMW--> | 3.30 MWh<!--f:P1000.energy.solarPerCycleMWh--> | 6.389<!--f:P1000.cycle.eCycleMWh--> | 3.09<!--f:P1000.energy.deficitPerCycleMWh--> | 22.9 h<!--f:P1000.energy.hoursOnBattery--> |
| P-10000 | 24.00 MW<!--f:P10000.energy.solarMW--> | 18.20 MWh<!--f:P10000.energy.solarPerCycleMWh--> | 43.019<!--f:P10000.cycle.eCycleMWh--> | 24.81<!--f:P10000.energy.deficitPerCycleMWh--> | 61.1 h<!--f:P10000.energy.hoursOnBattery--> |

**Every hull runs a deficit every cycle, and this is the project's central public conclusion:
without an energy import chain the fleet is a battery being spent.** It is not a perpetual machine
and does not claim to be.

Two defects attack this table from opposite directions. The generators each class advertises —
8<!--f:P100.spec.genMW-->, 40<!--f:P1000.spec.genMW--> and 150 MW<!--f:P10000.spec.genMW--> —
supply thrust authority and no energy at all, which understates generation. And the solar figure
is credited at 200 W/m², which overstates it by about 3.8× (§8.2). Correcting both moves the
conclusion in the same direction it already points.

## 8. What is wrong with this model

Thirteen entries are documented in `docs/OPEN-QUESTIONS.md`. Six were found by inspection, two by
auditing all 89 published claims against the code, and four by reading the sources. The four from
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

### 8.2 The solar skin needs 76% conversion efficiency

`state.js` credits 200 W/m² of *electrical output*, continuously. NRCan's dataset gives
6.34 kWh/m²/day mean July horizontal insolation across eight BC interior fire-belt towns —
264 W/m² incident, day-averaged. 200 out of 264 is **76% conversion**. At 20% modules the honest
figure is **53 W/m²**, and a fixed horizontal-equivalent ignores that most of an airship's skin
faces the wrong way at any moment.

Consequence: the P-10000's solar falls 24.0 → 6.4 MW, generation 18.20 → 4.83 MWh per cycle,
deficit 24.81 → 38.19 MWh, endurance 61.1 h<!--f:P10000.energy.hoursOnBattery--> → about 40.

### 8.3 `rtLN2` returns more work than the nitrogen contains

`rtLN2 = 0.50`<!--f:assumptions.rtLN2--> against `eLN2 = 0.45`<!--f:assumptions.eLN2--> kWh/kg
recovers **225 kWh per tonne** of liquid nitrogen. The physical exergy of LN2 at 1 bar against a
288 K ambient is **173.4 kWh/t** (Arnaiz-del-Pozo et al. 2020; corroborated at 205–214 kWh/t under
more favourable assumptions). The recovery term returns 1.3× the work available in the liquid,
before any turbine or generator efficiency. The ceiling is `rtLN2 ≤ 0.385`; a real plant would be
nearer 0.25.

### 8.4 The drop may not arrive, and tonnes may be the wrong metric

The US Forest Service's 2022 assessment states that a drop released 1,000 ft above
ground/vegetation "would completely dissipate". `ALT.drop` is 450 m — **1,476 ft** — raised for
hull-clearance reasons that are sound, with the delivery consequence never costed. The model has
no droplet physics: it moves tonnes from a tank to a coordinate.

And AFUE — 27,611 observed drops — reports probability of success **0.56 without ground engagement
against 0.72 with it**, the modal outcome without ground crews being *not effective*. AFUE never
counts tonnes. This project's headline metric is tonnes per hour.

### 8.5 The other nine, in one line each

| # | Defect | Cost |
|---|---|---|
| 1 | Lift bought at sea level, spent at altitude | **fixed** 2026-08-09; hulls grew 22.2% |
| 2 | Two power models disagree | `planCycle` vs integrated `stateAt`: **2.83×** on the P-10000 |
| 3 | An unexplained `0.2` sets the letdown window | 1.42 MWh today; was 34.20 before the anchor |
| 4 | Retained ballast is dead code; the plant is inert in-cycle | ballast **fixed**; plant restated (§7.2) |
| 5 | Esri basemap tiles used outside their terms | not physics; blocking for publication |
| 6 | Generators supply peak power but no energy | 150 MW uncounted on the P-10000 |
| 7 | 32 of 89 published figures rest on unjustified constants | two inline drag multipliers are worth **16.9 MWh** |
| 8 | `diskM2`/`battMW` answer a superseded constraint | `battMW` ±20% now moves every figure by **0.0%** |
| 12 | Rotor wash over a water surface is unmodelled | Suter (2005); a 121.6 MN anchor hangs in it |

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
- `make test` runs 196 tests. Two are marked `knownFail` and **fail on purpose** — a defect is not
  allowed to lose its excuse quietly.
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
5. **An energy import chain.** The fleet is a battery being spent; nothing here changes that.

If (1) fails, the rest is a well-tested model of a vehicle that cannot exist. That is why it is
first on the list and why §8.1 is written the way it is.

## 11. Availability

Model, tests, sources and defect list: `github.com/pinkrobotics/airships`. Live simulation:
`pinkrobotics.ca/airships`. Source catalogue: `research/sources.json` — 73 entries, 29
redistributable PDFs with provenance, 12 written notes, 9 sources that contradict us. Claim audit:
`research/evidence-map.md`.

---

*Every figure marked in this document is generated by `tools/figures_dump.js` from the model at
defaults and verified by `tools/check_figures.py`. Figures from cited sources are written plainly
and accounted for in `research/sources.json`.*
