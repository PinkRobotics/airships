# Vacuum-lift wildfire airships: a diligence report

> **Energy reading, 2026-10-02.** Energy conclusions in this earlier report are superseded by the [generated closure record](../../docs/ENERGY-CLOSURE-2026-10.md).
> Its cited tables now show supplied effort on the prescribed, unsupported profile. They do not establish delivery, endurance, savings or operating cost.
> Historical arrows retain earlier figures. Feasible delivery, cycle minutes, both energy bases and the requirements are in the generated record.

<!--tex:skip-->
**Pink Robotics · 2026-08-09 · v1 · prepared for readers doing technical and commercial diligence**

---

## 0. How to read this document

This is a diligence report on a **concept**, not on a company, a product, or a prototype. Nothing
has been built. There is no revenue, no letter of intent, no flight article, and no test rig.

The flight model assumes a hull that floats; no drawn hull does, as the [structural assessment](../../docs/FLOAT.md) explains.

What exists is a simulation and its supporting apparatus: a physics model, 309 tests and a 151-case deterministic golden baseline.
The source catalogue’s entry count is generated in the [repository README](../../README.md); written notes accompany it.
The apparatus also includes an audit of all 89 published claims and a defect list of seventeen items, two of them closed. That apparatus is the asset under
examination. **The correct question for a reader is not "do these numbers work" but "is this the
kind of work that would find out if they didn't".**

The report is organised as an argument rather than as a defence: what the idea is worth if it
works (§§1–3), then what would have to be true for it to work (§4), then the economics, the
regulatory path, and the quality of the evidence behind all of it. **§4.1 is the entry that could
end the conversation, and if you read one section, read that one.** It is placed fourth rather than
first because an obstacle is only worth arguing about if what it blocks is worth having, and
§§1–3 are what it blocks.

Every model figure is cited by key and verified automatically against the model
(`tools/check_figures.py`; the build fails on a mismatch). Every external figure names its source.
Where nothing is known, the section says so rather than estimating.

---

## 1. The thesis in one page

Conventional helicopters, water-scooping aircraft and base-refilled airtankers have distinct
refill circuits. The proposal studies a buoyant hull's requested load and repeating
water-source-to-target cycle; local water refill already exists in conventional aviation.
No comparative mission performance is established by that proposal.

Buoyant flight is the only way to get payload without paying for lift continuously, and it is the
only way to build a firefighting aircraft that never has to land. Helium is expensive and leaks;
vacuum is free and does not, if the shell can be made light enough — which is what discrete-lattice
construction may finally allow, and what §4.1 says has not been shown yet.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

**What the model says.** The reference vehicle is the **P-100**: 100 t<!--f:P100.spec.payloadT-->
of water, 110 m<!--f:P100.spec.lenM--> long — smaller than the Hindenburg — flying a
34.2-minute<!--f:P100.cycle.cycleMin--> cycle at 15 km<!--f:worked.oneWayKm--> each way and
delivering 175 t/h<!--f:P100.cycle.tph--> indefinitely, at
13.91 → 80.42 → 81.89 kWh/t<!--f:P100.cycle.kwhPerTonne-->. A daily resource comparison is not established:
helicopters, scooping aircraft and base-refilled airtankers are not modelled on a shared
invented task with common source-to-target, base, fuel, support and tactical inputs.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

Two larger classes are modelled — 1,000 t and 10,000 t — because energy per tonne *falls* with
size. **They are not a proposal and no part of this report assumes one gets built.** They are how
we found where the arithmetic stops working, which is §3.

**What the model does not say.** That the vehicle can be built. The model takes hull mass as an
assumption and computes forward from it; §4.1 is about that assumption and it does not survive
contact with the sources.

**Where the genuine invention is.** One place: the descent anchor (§3). It solves a real problem
that emerged mid-project, it is 58× cheaper than the rotor work it replaces, and it is the only
part of this concept that is not a scaling exercise on prior art.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

**Why scale is interesting, and why it is not the plan.** Energy per tonne falls as the ships get
bigger — 13.91 → 80.42 → 81.89 kWh/t<!--f:P100.cycle.kwhPerTonne--> on the reference ship against
5.43 → 69.76 → 69.42<!--f:P10000.cycle.kwhPerTonne--> at ten thousand tonnes — because buoyancy scales with volume
and drag with area. The square-cube law works against nearly every other vehicle and for this one.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

That is an argument for the concept having room to grow, not an argument for starting large.
Everything that makes a reader wince in this document is a property of the largest class: a 512 m
hull, a 1,400 MW bus, a suspended bag 1,265 times the largest ever built. The reference ship is
110 m, 30 MW, and a bag thirteen times a Bambi bucket.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

**What would make this investable.** Not a better simulation. A gram-level mass breakdown of a
lattice shell at scale, from someone who builds them. Everything else is downstream of that number
and the number is currently missing (§8). It is also cheap to obtain relative to everything it
gates: two expert reviews, not a programme.

---

## 2. What the model shows

Everything below is conditional on §4.1 — read it as "if a shell can be built, then —". What
makes it worth reading anyway is that the operational arithmetic is where the concept is
*strongest*, and it is the part a reader can check line by line today.

<!--tex:fig charts/throughput.pdf | Sustained delivery, and the cycle behind it. The vehicle never lands, so the longest phases are moving water rather than flying.-->

### 2.1 The sizing logic is sound and safety-led

Displacement is not chosen to make the numbers work. It is set by a fail-safe requirement:

> A hull must be positively buoyant at its working altitude while **fully loaded with water and
> unable to release it.**

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

### 2.2 The cycle is timed, not asserted

| Phase | P-100, min | What happens |
|---|---:|---|
| Source approach | 2.00<!--f:P100.cycle.durations.SOURCE_APPROACH--> | dead stop, lower anchor and pumps |
| Fill | 3.33<!--f:P100.cycle.durations.WATER_FILL--> | 0.5 m³/s<!--f:P100.spec.fillM3s-->, no yaw |
| Outbound | 11.76<!--f:P100.cycle.durations.OUTBOUND_TRANSIT--> | 90 km/h<!--f:P100.spec.cruiseKph--> |
| Release | 3.33<!--f:P100.cycle.durations.WATER_RELEASE--> | one pass |
| Escape | 2.00<!--f:P100.cycle.durations.BUOYANCY_ESCAPE--> | buoyancy only, no propulsion |
| Return | 11.76<!--f:P100.cycle.durations.RETURN_TRANSIT--> | |
| **Total** | **34.20<!--f:P100.cycle.cycleMin-->** | 100 t<!--f:P100.cycle.deliveredT--> delivered |

On the reference ship transit is 23.5 of 34.2 minutes and is the binding constraint, because it is
the only term that grows with distance. That has a commercial consequence, and it is the one a
buyer should press on: **the value of the concept collapses toward the value of a big pump if the
fire is not near water.** How often that is true is item 13 of `docs/OPEN-QUESTIONS.md`.

<!--tex:fig charts/render-release.png | Mid-release, rendered from the model. Ten thousand tonnes leaves along the length of the keel in one pass; the hull rises off the line as it goes, which is why the escape climb costs no propulsion.-->

### 2.3 Throughput, if the vehicle exists

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Delivery per hour | 175 t<!--f:P100.cycle.tph--> | 1,697 t<!--f:P1000.cycle.tph--> | 13,183 t<!--f:P10000.cycle.tph--> |
| Energy per tonne (earlier 1) | 13.91 | 8.45 | 5.43 |
| Energy per tonne (earlier 2) | 80.42 | 62.50 | 69.76 |
| Energy per tonne (current) | 81.89 kWh<!--f:P100.cycle.kwhPerTonne--> | 62.25 kWh<!--f:P1000.cycle.kwhPerTonne--> | 69.42 kWh<!--f:P10000.cycle.kwhPerTonne--> |
| Energy per cycle (earlier 1) | 1.391 | 8.454 | 54.325 |
| Energy per cycle (earlier 2) | 8.042 | 62.500 | 697.586 |
| Energy per cycle (current) | 8.189 MWh<!--f:P100.cycle.eCycleMWh--> | 62.251 MWh<!--f:P1000.cycle.eCycleMWh--> | 694.174 MWh<!--f:P10000.cycle.eCycleMWh--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

A resource comparison needs helicopters, scooping aircraft and base-refilled airtankers on
one shared invented mission. Their daily delivery, fuel and support schedules, and tactical
objectives have not been modelled here. The square-cube law then says a larger hull
delivers a tonne for less — 2.7× less at the top of the table — which is why the concept has room
to grow and not a reason to start there.

---

## 3. The one genuine invention, and its exposure

### 3.1 What it is

The buoyancy that guarantees float-up must be overcome to descend, and it is worst at the bottom,
over the water, where the air is densest.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Lake buoyant surplus | 135.6 t<!--f:P100.descent.holdAtSourceT--> | 1,366.9 t<!--f:P1000.descent.holdAtSourceT--> | 13,722.5 t<!--f:P10000.descent.holdAtSourceT--> |
| Rotor capability (earlier 1) | 267.2 | 1,318.1 | 12,666.2 |
| Rotor capability (earlier 2) | 141.4 | 687.6 | 7,124.3 |
| Rotor capability (current) | 140.5 t<!--f:P100.descent.rotorCapT--> | 683.3 t<!--f:P1000.descent.rotorCapT--> | 7,079.2 t<!--f:P10000.descent.rotorCapT--> |

<!--tex:fig charts/descent.pdf | The problem the anchor solves. The bar is what has to be held down at the water; the tick is how far the rotors reach unaided. | 0.95-->

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

The two larger classes **cannot reach their own water source under power.** The solution is to
borrow the lake: lower a cable with a collapsible bag, fill it, winch it clear of the surface.
12,400 t<!--f:P10000.descent.anchorT--> of hanging water is
121.6 MN<!--f:P10000.descent.anchorPullMN--> of downward force for the 15 m of lift needed to break
the surface — **0.596 → 0.596 MWh<!--f:P10000.energy.anchorHoistMWh-->** against the 34.5 MWh of rotor
work it replaces.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

The leverage is in the exponent: induced rotor power goes as thrust^1.5, so the letdown term falls
from 34.20 MWh to 1.420 → 117.284 → 117.168 MWh<!--f:P10000.energy.letdownMWh--> — 96%. Alternatives, costed and
rejected in the open: nitrogen ballast **475 MWh**, a 1,350 m hose **44 MWh** at 2 m bore and
140 bar, retention **directly reduces the product**.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

The mechanism cannot be over-sized: the most water a ship can lift is its own surplus lift, so the
physics supplies its own ceiling. The report dated 2026-08-09 said that removing the P-100’s bag, which it
does not need, costs 34% more energy per cycle. This is a dated report reading; its original
comparator and the current unsupported replay are separated in the generated note above.

### 3.2 Its exposure

| Risk | Status |
|---|---|
| **Scale** | 12,400 t against the largest bucket ever built, 9,800 L. **1,265×.** The principle is 43 years old; the engineering is not. |
| **Cable** | Rope product and diameter are unselected. The minimum-strength, quasi-static pickup and safety-factor basis is disclosed below; the bottom-up budget charges its cable mass. |
| **Pendulum** | 12,400 t swinging on one cable under an 512 m hull. Not modelled at all. |
| **Rotor wash on water** | The P-10000 has ~79 kg/m² disc loading against a Black Hawk's ~47, across 14 rotors whose combined disc area equals a single 451 m disc. A hovering Black Hawk must be over 160 ft up before surface wash falls below 30 mph (Suter 2005). The model has no wash physics, and the anchor requires a stationary hover over the surface it is disturbing. |
| **Station-keeping** | The mechanism requires a dead stop, no yaw while lines are down, and departure only when pumps clear the water. The model enforces these; nothing validates that a hull this size can hold station in the wind over a lake. |

<!-- anchor-rope:basis:start -->
Illustration: the dry-mass budget sizes an assumed UHMWPE cable by minimum break strength, not by diameter. Design load including pickup is bag-water weight under the quasi-static pickup assumption; dynamic snatch, cable self-weight and bag/rigging dry weight are omitted. Required minimum break strength is that load times the safety factor. Assumption: credible safety factor 5; assumption: floor safety factor 3; assumption: demonstrated safety factor 7. Assumption: credible minimum-strength-per-linear-density coefficient 1.5 MN per kg/m; assumption: floor coefficient 2.0 MN per kg/m; assumption: demonstrated coefficient 1.4 MN per kg/m. Those columns do not qualify a rope product. The bottom-up dry-mass budget charges the installed cable, bag and winch. The flight model still assumes dry mass equals payload; it does not integrate that equipment bill. Terminations, wear, creep, cyclic pickup and the bag load path remain unqualified. See `research/analysis/mass-budget.py` and its generated records.
<!-- anchor-rope:basis:end -->

**Positive IP note:** this is the one part of the concept that is not obvious from prior art, and
it is currently published openly. If there is defensible IP here, it is being given away. That is a
deliberate consequence of the open-source strategy and should be a conscious decision rather than a
side effect.

---

## 4. What would have to be true

Everything in §§2–3 is arithmetic on assumptions. Four of those assumptions were checked against
the literature and came back contradicted, and they are stated here in full, with their
arithmetic, because a diligence reader should not have to find them.

**Two of the four were corrected on 2026-08-09**, within hours of being found, because neither had
a defensible reading, and both corrections made the model's numbers worse. They are kept here
rather than moved to an appendix: what a project did when its own evidence went against it is
worth more to a reader than the corrections themselves. **The two that remain open are §4.1 and
§4.4. §4.1 is the one that could end this**, and §4.4 changes what the product is rather than
whether it can exist.

### 4.1 The mass budget fails against four independent sources — SEVERE

The model's foundational assumption is `dryT = payloadT`: the ship's entire dry mass — shell, skin,
joints, rotors, tanks, batteries, pumps, cable — equals the water it carries. That is a
hull-average density of **0.455 kg/m³**, and it is the same number on every class: 100 t inside
220,000 m³<!--f:P100.spec.dispM3--> and 10,000 t inside
22,000,000<!--f:P10000.spec.dispM3--> both come out there, because displacement is sized per tonne
of payload.

**So choosing the smaller reference ship does not make this go away.** Every other objection in
this report is milder on a P-100 — the bag, the bus, the grid connection, the hull length. This
one is identical, and it is the one that decides whether any of them get built.

| Source | What it gives | Against our 0.455 kg/m³ |
|---|---|---|
| **Jenett et al. 2019** (NASA NTRS) — our own cited structural precedent | bare discrete-lattice shell, **0.508 kg/m³**, at every radius (their Table 2) | **12% over our entire dry allowance**, with nothing else fitted |
| **Metlen & Palazotto 2013** | only real-materials design has structure/buoyancy **0.94** | structure alone consumes what we allocate to structure *and* payload |
| **Akhmeteli & Gavrilin 2021** | payload fraction **0.1**, shell 1.16 kg/m³ | against our implied 0.5 |
| **Chin et al. 2021 / Lvovich 2020** (NASA) | X-57 pack as built: **149 Wh/kg** at pack level from 225 Wh/kg cells; the aircraft did not fly | our 2,000 MWh<!--f:P10000.spec.battMWh--> battery masses ~13,400 t — **the battery alone is 34% over the whole dry budget** |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

Four sources, four different objections, one conclusion. The 2,000 MWh battery figure deserves
emphasis: at the density of the pack NASA actually built, the battery by itself exceeds the entire dry mass
allowance before any structure exists. Even at 500 Wh/kg — the point Lvovich says NASA sees no
clear path past — the pack consumes 40% of a budget the hull already exceeds on its own.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

**And there is a fifth objection that attacks the method rather than the numbers.** Both structural
sources hold shell mass fraction constant with radius — the scale invariance that lets a
metre-scale demonstration imply a 256 m<!--f:P10000.spec.diaM--> hull. Derveni et al. (2024) show
that in pressurised shells with distributed defects, **the single worst defect sets the buckling
knockdown factor**, and removing all the lesser defects changes it by under 4%. Defect count is not
invariant with radius: it grows with the number of manufactured features, and so does the expected
severity of the worst one. **The scale invariance both our structural sources assume cannot hold.**

*Diligence status:* unresolved, and not resolvable by more modelling. Requires a mass breakdown
from a builder of lattice structures. This is the project's single point of failure.

### 4.2 The solar skin required 76% conversion efficiency — CORRECTED 2026-08-09

The model credited the skin a flat **200 W/m² of electrical output**, continuously, in five
separate source files. NRCan's dataset gives 6.34 kWh/m²/day mean July horizontal insolation across
eight BC interior fire-belt towns: **264 W/m² incident**, day-averaged. 200 out of 264 is 76%
conversion — three and a half times the best cell ever made in a laboratory.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

It is **45 W/m²<!--f:assumptions.solarWPerM2-->** now: 264 × 0.21 flexible module × 0.81 for
curvature, cell temperature, soiling and conversion, on a projected area.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| | solar | deficit/cycle | endurance |
|---|---|---|---|
| P-100 (earlier 1) |  | 0.32 |  |
| P-100 (earlier 2) |  | 1.24 | 35.4 |
| P-100 (earlier 3) | 1.20 | 7.89 | 9.2 |
| P-100 (current) | 0.21 MW<!--f:P100.energy.solarMW--> | 8.07<!--f:P100.energy.deficitPerCycleMWh--> | 1.4 h<!--f:P100.energy.hoursOnBattery--> |
| P-1000 (earlier 1) |  | 3.09 |  |
| P-1000 (earlier 2) |  | 7.71 | 22.9 |
| P-1000 (earlier 3) | 5.60 | 61.76 | 9.2 |
| P-1000 (current) | 0.97 MW<!--f:P1000.energy.solarMW--> | 61.68<!--f:P1000.energy.deficitPerCycleMWh--> | 1.1 h<!--f:P1000.energy.hoursOnBattery--> |
| P-10000 (earlier 1) |  | 24.81 |  |
| P-10000 (earlier 2) |  | 50.23 | 61.1 |
| P-10000 (earlier 3) | 24.00 | 693.49 | 30.2 |
| P-10000 (current) | 4.48 MW<!--f:P10000.energy.solarMW--> | 690.78<!--f:P10000.energy.deficitPerCycleMWh--> | 2.2 h<!--f:P10000.energy.hoursOnBattery--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

*Diligence status:* **closed, and the finding underneath it is not.** Two things a reader should
take from this. First, the correction cut published endurance by roughly two thirds and the project
shipped it the same day — that is the behaviour the rest of this report is asking you to price.
Second, **no published throughput or energy-per-tonne figure moved at all**, because generation is
not in the ledger that computes them. A 4.4× error in the vehicle's power supply was invisible to
every test in the repository. That is defect 6 in [the paper's table](02-paper.md#85-the-other-nine-in-one-line-each), it is still open, and it is the more
important half of this entry.

### 4.3 The nitrogen recovery was thermodynamically impossible — CORRECTED 2026-08-09

`rtLN2 = 0.50` against `eLN2 = 0.45`<!--f:assumptions.eLN2--> kWh/kg recovered **225 kWh per
tonne** of liquid nitrogen. The physical exergy of LN2 at 1 bar against a 288 K ambient is
**173.4 kWh/t** (Arnaiz-del-Pozo et al. 2020; independently corroborated at 205–214 kWh/t under
more favourable assumptions). The term returned 1.3× the work the liquid contains, before any
turbine or generator efficiency.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

It is **0.20<!--f:assumptions.rtLN2-->** now — 90 kWh/t, 52% of the exergy, about what a cryogenic
expander returns with no external heat source. The P-10000's cycle rose 43.019 →
**54.325 → 697.586 → 694.174 MWh<!--f:P10000.cycle.eCycleMWh-->**, 6.6%. The shared power model limits requested recovered work per tonne before the generator cap; tests cover every selectable control pair, including both extremes.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

*Diligence status:* **closed.** Small in magnitude, absolute in kind, and worth reading for what it
says about how the model was being checked before: a unit test existed for this line and it was
asserting the violation as correct behaviour. The test now checks the physical ceiling as well as
the value, because the first is a choice and the second is not.

### 4.4 The headline metric may be measuring the wrong thing — strategic

Two findings from the wildfire-aviation literature, both aimed at the top of the funnel.

**The drop may not arrive.** The US Forest Service's 2022 assessment states that a drop released
1,000 ft above ground/vegetation "would completely dissipate". `ALT.drop` is 450 m — **1,476 ft**.
The altitude was raised for hull-clearance reasons that are sound (an 512 m hull cannot manoeuvre
out of a surprise over a fire), and **the delivery consequence was never costed**. The model has no
droplet physics at all: it moves tonnes from a tank to a coordinate.

**Tonnes is not the industry's metric.** AFUE observed 27,611 drops at 272 incidents. Overall
probability of success is 0.82, but for airtankers used to halt fire spread it falls to **0.55–0.67**,
and **without ground engagement it is 0.56 against 0.72 with it** — the modal outcome for a drop
with no ground crew being *not effective*. AFUE never counts tonnes.

An uncrewed fleet delivering enormous tonnage without ground engagement is, on the only large field
study available, **operating in the least effective mode the study measured**.

*Diligence status:* neither is a modelling error — the model is honest about being a delivery
simulator. Both bear on whether the product is valuable. A fire-agency reader will raise them in
the first five minutes, and there is currently no answer.

---

### 4.5 If the shell cannot be built, what survives?

An investor finishing §4.1 asks one question immediately, and no document in this set has asked
it: **if the vacuum shell is the thing that fails, why not helium?**

The honest answer is that most of this concept survives that substitution. The duty-cycle argument
in §1 is about buoyant flight, not about what provides the buoyancy. A vehicle that never lands
still has no turnaround. The descent anchor still works — it solves *surplus buoyancy*, which a
helium hull has too. The cycle, the pumping, the flight profile and most of the energy ledger carry
over unchanged.

What changes is the lift budget and the economics. Helium is about 14% less buoyant per cubic
metre than vacuum, so the hull grows for the same payload. It leaks, so it is a consumable with a
supply chain that has few producers of consequence — a recurring cost and a strategic exposure
that vacuum does not have. Those are commercial objections rather than physical ones, and they
look very different once the vacuum shell is what fails.

**This has not been modelled and it should be.** The model is parameterised on displacement and
lift, so a helium variant is a small change to `sim/config.js` and an afternoon of re-running, not
a new project. Until it is done, this report cannot say how much of the throughput survives, and
that is a gap a reader is entitled to hold against it.

The same applies, less favourably, to hybrid-lift designs that make up the difference
aerodynamically: they reintroduce the payload/endurance trade §1 is built on avoiding, and they do
not obviously keep the never-lands property.

---

## 5. Energy, and the only economics the model supports

### 5.1 The ledger

P-100, 15 km<!--f:worked.oneWayKm--> each way, printed from the model:

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| Term | MWh |
|---|---:|
| Return transit (drag + cryogenic plant) (earlier 1) | 0.981 |
| Return transit (drag + cryogenic plant) (earlier 2) | 4.212 |
| Return transit (drag + cryogenic plant) (current) | 4.407<!--f:P100.energy.ledgerMWh.RETURN_TRANSIT--> |
| Outbound transit (earlier 1) | 0.286 |
| Outbound transit (earlier 2) | 0.632 |
| Outbound transit (current) | 0.576<!--f:P100.energy.ledgerMWh.OUTBOUND_TRANSIT--> |
| Hotel + manoeuvring | 0.162[historical] |
| Pumping (earlier 1) | 0.109 |
| Pumping (earlier 2) | 0.857 |
| Pumping (current) | 0.864<!--f:P100.energy.ledgerMWh.WATER_FILL--> |
| Letdown (earlier 1) | 0.012 |
| Letdown (earlier 2) | 2.296 |
| Letdown (current) | 2.302<!--f:P100.energy.letdownMWh--> |
| Anchor (earlier 1) | 0.006 |
| Anchor (current) | 0.003<!--f:P100.energy.anchorHoistMWh--> |
| Nitrogen recovery (credit) | −0.165<!--f:P100.energy.ledgerMWh.recovery--> |
| **Total** (earlier 1) | 1.391 |
| **Total** (earlier 2) | 8.042 |
| **Total** (current) | 8.189<!--f:P100.cycle.eCycleMWh--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

<!--tex:fig charts/ledger.pdf | The reference ship's cycle ledger, printed from the model. Three quarters of it is the return leg; the mechanism that closes the descent costs half a per cent.-->

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

### 5.2 The fleet is a battery being spent

Every class runs a deficit every cycle. This is the project's central public conclusion and it is
stated on the site rather than hidden:

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| | deficit/cycle | endurance |
|---|---:|---:|
| P-100 (earlier 1) | 1.24 |  |
| P-100 (earlier 2) | 7.89 | 9.2 |
| P-100 (current) | 8.07 MWh<!--f:P100.energy.deficitPerCycleMWh--> | 1.4 h<!--f:P100.energy.hoursOnBattery--> |
| P-1000 (earlier 1) | 7.71 |  |
| P-1000 (earlier 2) | 61.76 | 9.2 |
| P-1000 (current) | 61.68 MWh<!--f:P1000.energy.deficitPerCycleMWh--> | 1.1 h<!--f:P1000.energy.hoursOnBattery--> |
| P-10000 (earlier 1) | 50.23 |  |
| P-10000 (earlier 2) | 693.49 | 30.2 |
| P-10000 (current) | 690.78 MWh<!--f:P10000.energy.deficitPerCycleMWh--> | 2.2 h<!--f:P10000.energy.hoursOnBattery--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

Those figures are post-correction and roughly a third of what this report would have carried a day
earlier. There is no configuration in which this fleet sustains itself; it requires an energy
import chain, and that chain is the business.

<!--tex:fig charts/deficit.pdf | Spend against generation, and endurance on a full battery. This is the project's central public conclusion and it is not a favourable one.-->

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

### 5.3 Grid implications — the number that should govern the conversation

**The model publishes no cost, and nothing below is a model output.** These are derived from model
energy figures and the published BC Hydro Transmission Service Rate Schedule 1830 (effective
1 April 2026: demand $12.178/kV·A, energy 4.914 ¢/kWh). **All currency is Canadian**, because the
tariff is. Assumptions stated inline.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

<!-- solar:supply:start -->
- **Continuous supplied effort, reference ship, unsupported prescribed profile:** 1.391 → 8.042 → 8.189 MWh<!--f:P100.cycle.eCycleMWh--> per
  34.2-minute<!--f:P100.cycle.cycleMin--> cycle = **14.37 MW average**, or **14.16 MW imported** net
  of the assumed projected solar (0.21 MW<!--f:P100.energy.solarMW-->). These quotients establish no delivery or endurance.
<!-- solar:supply:end -->
- **Energy cost per tonne delivered** at 4.914 ¢/kWh: **$0.62/t**
  (13.91 → 80.42 → 81.89 kWh/t<!--f:P100.cycle.kwhPerTonne-->). A full 100-tonne drop costs about **$62** of
  electricity.
- **A ten-ship P-100 fleet** — 1,750 t/h between them, day and night — imports about **19 MW**.
  At Schedule 1830 that is on the order of **CA$0.9M per month**. Forty ships, delivering
  7,000 t/h, would import about 77 MW.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

**And this is where the choice of reference ship changes the answer.** BC Hydro's total generating
capacity is 13.4 GW. A ten-ship P-100 fleet is **0.14% of it** — a large industrial connection,
the kind a sawmill has, not a generation-planning problem.

Run the same arithmetic at the limit and it becomes one. A single P-10000 draws
60.5 MW continuously and imports 55.1 net of solar; ten of them is **551 MW, 4.1% of provincial
capacity**, continuously, through a fire season that is also peak demand season — on the order of
**CA$26M a month**. The instantaneous figure looks worse still, since that class's battery is rated
at 1,400 MW<!--f:P10000.spec.battMW--> of discharge, but that rating is one of the
reverse-engineered constants §7 flags and nobody should plan against it.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

So: **the grid is not an obstacle to this concept. It is an obstacle to the largest version of
it**, and it arrives long before anyone is asked to believe in an 512-metre hull. A programme that
starts at the reference scale can be connected to the existing grid today; one that starts at the
top cannot, and would carry an interconnection queue measured in years. BC Hydro's 2025 capacity
call drew 106 submissions totalling 19 GW, which indicates what that queue looks like.

**Not costed anywhere, and material:** capital cost of a hull (no basis exists), the megawatt-scale
charging infrastructure at each operating base, battery replacement cycles, and the cost of the
fire-season duty factor — a fleet sized for August is idle in February.

### 5.4 The commercial side is absent, and that is a gap in this report

This section prices what the fleet *consumes*. It says nothing about what the capability is
*worth*, and a diligence reader should not have to infer that from silence. Four things are
missing:

- **What agencies pay today** per delivered tonne and per aircraft-hour for very large airtankers
  and Type 1 helicopters, and the annual aerial-suppression spend in the target jurisdictions.
  None of it is in `research/sources.json`, so this report will not quote it.
- **Who signs.** Aerial suppression is bought by provincial and federal agencies on multi-year
  standing contracts with call-when-needed extensions. The procurement route for an uncrewed
  aircraft of this size does not exist.
- **Capital cost**, even to an order of magnitude. It is derivable — hull mass against a $/kg for
  lattice structure, plus battery at published $/kWh — and it has not been done.
- **How often the mission exists.** §2.2 notes that the concept's value collapses toward the value
  of a big pump if the fire is not near water, and then drops it. That is answerable this week
  from data this project already mirrors, and it bounds the market more tightly than any of the
  above. It is now item 13 on the defect list.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

**The honest position** is that this document is a technical diligence report with a commercial
section that has not been written. It is presented that way rather than filled with estimates,
because an invented market size next to a generated throughput figure would devalue both.

---

## 6. Regulatory and legal

| Question | Finding | Status |
|---|---|---|
| **Taking the water** | BC's *Water Sustainability Act* permits diverting unrecorded water for firefighting **without authorisation**, and a fire department may divert, use and store water for firefighting preparation without authorisation. | **Clear on its face.** The legal half is the easy half. |
| **The lake's capacity** | The Act says nothing about whether a lake can stand repeated 10,000 t draws. A P-10000 removes 13,183 t/h<!--f:P10000.cycle.tph--> from one body of water. | **Open.** Hydrological, not legal, and unaddressed. |
| **Flying it** | ICAO Chicago Convention Art. 1 (sovereignty) and Art. 8 (pilotless aircraft need special authorisation over another state). FAA/EASA routes for large uncrewed aircraft exist but nothing of this scale has been certificated. | **Open, long lead.** No certification basis exists for an 512 m uncrewed vehicle. |
| **Autonomy assurance** | FAA 2024 AI safety-assurance roadmap, EASA AI roadmap 2.0, NIST AI RMF, runtime-assurance literature all catalogued as context. | **Open.** No work done. |
| **Airspace deconfliction** | An 512 m uncrewed hull working the same incident as crewed airtankers and Type 1 helicopters. Appears in `docs/PHYSICS.md` only as out of scope. | **Open. No work done**, and an operational blocker rather than a certification detail. |
| **Liability and insurability** | A 10,000 t release over ground, and a 12,400 t bag on a cable over a lake. | **Open. No work done.** |
| **Weather modification law** | ENMOD catalogued. Not obviously engaged by water delivery. | Low. |

The regulatory path is the second-longest pole after the structure, and unlike the structure it
cannot be shortened by a good result in a lab.

---

## 7. Quality of the evidence base

The §4 findings exist because of what is in this table — and it is the part of the project a
reader can verify in an afternoon.

| Artefact | What it is |
|---|---|
| `sim/` | The model. No DOM, network, storage, wall clock or location — enforced by a boundary linter across 80 modules. |
| `tests/` | 236 registered tests in 60 suites, plus 103 more that need node. **0 known-failing markers**; corrected defects run as ordinary assertions. |
| `tests/golden/` | 151 class/mode/distance/wind combinations, diffed on every run. Independently reproduced by a separate Python implementation. |
| `research/sources.json` | 73 sources: 3 load-bearing, **9 that contradict us**, 20 supporting, 41 context. 29 redistributable PDFs with provenance records; everything paywalled catalogued and refused by name. |
| `research/notes/` | 12 notes, each written from the source PDF rather than its abstract, each stating where the source does *not* support what we would like it to. |
| `research/evidence-map.md` | Audit of all 89 published claims. |
| `research/figures.json` | Every published figure, regenerated from the live model. `tools/check_figures.py` fails the build if any report disagrees. |
| `docs/OPEN-QUESTIONS.md` | Seventeen defects, each with cost, options and a recommendation. Two closed, fifteen open. |

<!--tex:fig charts/sensitivity.pdf | Every constant moved ±20%, generated rather than transcribed. Where the model's uncertainty actually lives: aerodynamics and speed, not lift.-->

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

**The signal to weigh.** The defect list went from six to seventeen once the project audited
itself properly — and it is the same model. Nothing was introduced; it was all already true and
unnoticed. Seven were found by the authors, two by auditing claims against code, four by reading
the sources, one by an outside reader asking a question none of them had, and three by an
adversarial review of the model itself. That ratio is the argument for the process and the warning about the numbers.

**The two largest errors ever found in this model were both accounting, not physics.** The
nitrogen recovery was netted against the pump bill under a `max(0, …)` and silently deleted the
entire pumping cost on two of three classes; and the lift ledger bought air at sea level and spent
it at altitude, overstating lift by 22%. Neither was caught by a test. Both were caught by
re-deriving a published number from scratch.

**Where the process is still weak:** 32 of 89 published figures rest on constants with no stated
justification, against 15 genuine documented assumptions. Two undocumented inline drag multipliers
are worth 16.9 MWh a cycle, while the defect flagged in the README since the first commit is worth
1.4. The project has been auditing the things it knew to doubt.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

**The suite had a hole in it, and it is worth understanding.** 103 of the tests need node,
which is not installed on the machine this is developed on, so `make test-node` printed "SKIPPED"
and those tests were only ever executed by CI. Two breaks reached the remote that way — including
a unit test asserting the impossible nitrogen recovery in §4.3 as correct behaviour. They run in a
browser now, against the same files, and `make check` covers them. A reader should weigh both
halves: a gap that let a wrong assertion sit unchallenged, and a project that closed it with a
tool rather than a resolution.

---

## 8. What would have to be proven, in order

1. **A lattice vacuum shell at ≤0.455 kg/m³ including everything.** Nothing in the literature is
   there. Not resolvable by modelling. Requires a gram-level mass breakdown from someone who builds
   these structures, plus an answer to the Derveni scale-invariance objection (§4.1). **This is the
   only §4 finding that both remains open and is capable of ending the concept** — §4.2 and §4.3
   are closed, and §4.4 changes what the product is rather than whether it can exist.
2. **A battery at ≥200 Wh/kg pack level, with the rest of the vehicle free.** Not available; the pack NASA
   built reached 149, and NASA sees no clear path past 500.
<!-- editorial:drop-hull:start -->
Generated from the owning record during the combined regeneration.
<!-- editorial:drop-hull:end -->
4. **A 12,400 t suspended bag, its cable, its pendulum dynamics, and hull station-keeping over
   water in wind.** The mechanism is sound in principle and unbuilt at 1,265× the precedent.
5. **An interconnection.** ~50 MW continuous per large ship, in a 13.4 GW province, during peak
   season.
6. **That tonnes delivered is the right product.** AFUE says effectiveness turns on ground
   engagement, which an uncrewed fleet does not have.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

Items 1 and 2 are structural facts about materials that no amount of engineering effort inside this
project can change. **They should be resolved before anything else is funded**, and they are cheap
to resolve relative to everything downstream: they are literature and expert review, not hardware.

---

## 9. Assessment

**On the concept.** Unproven and currently contradicted at its foundation. The mass premise fails
against the project's own cited precedent by 12% before anything is fitted, and the battery alone
exceeds the whole dry allowance at demonstrated pack densities. Neither is a detail; both are the
first line of the ledger. A reader looking for a reason to stop has one, in §4.1, sourced.

**On the invention.** The descent anchor is genuinely novel, is not obvious, solves a problem the project
discovered rather than invented, and is 58× cheaper than the alternative. It is worth attention on
its own terms — including, possibly, on vehicles other than this one. It is also published openly
and therefore unprotected.

**On the work.** The apparatus is better than the concept. A model that fails its own audit in
public, keeps two tests failing on purpose, catalogues nine sources that contradict it, and grows
its defect list from six to seventeen by checking properly is doing the thing most concept work
avoids. The clearest evidence is what happened on 2026-08-09: two of the four findings in §4 were
corrected within hours of being found, both corrections made the published numbers worse — cycle
energy up 6.6%, endurance down by roughly two thirds — and both shipped to the live site the same
day. If the question is "will this team find out whether the idea works", the record above is the
evidence, and it points one way: every check this project has run on itself has cost it something
and been published anyway. If the question is "does the idea work", the evidence today is **no, on the mass
budget**, and the project says so itself in `docs/OPEN-QUESTIONS.md` #11.

**Recommended next step, at minimal cost:** commission a lattice-structure mass breakdown at
100 m and 219 m radius from a group that builds them, and an independent pack-level mass estimate
for a 2,000 MWh flight battery. If either comes back where the literature suggests, the concept
needs a different vehicle — smaller, or hybrid-lift, or not buoyant at all — and finding that out
costs two reviews rather than a programme.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

---

## 10. Sources and reproduction

```
git clone github.com/pinkrobotics/airships && cd airships && make check
```

`make golden` diffs 151 cases; `make test` runs 236 tests with 0 known-failing markers and
`make test-node` a further 103;
`make factsheet` regenerates every published figure from the live model; `tools/check_figures.py`
fails the build if this document disagrees with it. `?seed=7&data=snapshot` reproduces any run on
the live site exactly.

Full catalogue: `research/sources.json`. Notes: `research/notes/`. Claim audit:
`research/evidence-map.md`. Defect list: `docs/OPEN-QUESTIONS.md`. Physics derivations:
`docs/PHYSICS.md`. Public summary of the evidence base: `pinkrobotics.ca/research`.

**Load-bearing sources:** Jenett et al. 2019 (NASA NTRS, redistributable — verified by hash against
the NTRS original); Akhmeteli & Gavrilin 2021 (CC BY); NOAA/NASA/USAF *U.S. Standard Atmosphere
1976*.

**Sources that contradict us:** Metlen & Palazotto 2013; Derveni et al. 2024; Arnaiz-del-Pozo et
al. 2020; NRCan 2020; USFS AFUE 2020; USFS 2022; Suter 2005; Chin et al. 2021; Lvovich 2020.

---

*Every figure marked in this document is generated by the model and verified automatically.
External figures name their source. Derived commercial figures in §5.3 state their assumptions and
are not model outputs — the model publishes no cost.*

[historical] The dated “other” ledger aggregate has no current equivalent. The corrected ledger uses the six named phases and recovery; no current-model citation is claimed for the old aggregate. Both bases and all closing requirements are in [the generated closure comparison](../../docs/ENERGY-CLOSURE-2026-10.md).
