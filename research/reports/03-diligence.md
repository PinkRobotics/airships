# Vacuum-lift wildfire airships: a diligence report

<!--tex:skip-->
**Pink Robotics · 2026-08-09 · v1 · prepared for readers doing technical and commercial diligence**

---

## 0. How to read this document

This is a diligence report on a **concept**, not on a company, a product, or a prototype. Nothing
has been built. There is no revenue, no letter of intent, no flight article, and no test rig.

What exists is a simulation and its supporting apparatus: a physics model, 309 tests, a 151-case
deterministic golden baseline, a 73-source catalogue with 12 written notes, an audit of all 89
published claims, and a defect list of thirteen items, two of them closed. That apparatus is the asset under
examination. **The correct question for a reader is not "do these numbers work" but "is this the
kind of work that would find out if they didn't".**

The report is organised as an argument rather than as a defence: what the idea is worth if it
works (§§1–3), then what would have to be true for it to work (§4), then the economics, the
regulatory path, and the quality of the evidence behind all of it. **§4.1 is the entry that could
end the conversation**, and if you read one section, read that one — but read it after §3, because
the size of the prize is what decides whether the obstacle is worth attacking.

Every model figure is cited by key and verified automatically against the model
(`tools/check_figures.py`; the build fails on a mismatch). Every external figure names its source.
Where nothing is known, the section says so rather than estimating.

---

## 1. The thesis in one page

**Claim.** Aerial firefighting is limited by turnaround, not by drop size. A very large airtanker
delivers seventy tonnes in seconds and then spends most of an hour not delivering anything. A
vehicle that dips from a lake like a helicopter but carries like a tanker would change the
*sustained* rate — the one that decides whether a line holds — by orders of magnitude.

Buoyant flight is the only way to get payload without paying for lift continuously, and it is the
only way to build a firefighting aircraft that never has to land. Helium is expensive and leaks;
vacuum is free and does not, if the shell can be made light enough — which is what discrete-lattice
construction may finally allow, and what §4.1 says has not been shown yet.

**What the model says.** Three classes, from 100 t<!--f:P100.spec.payloadT--> to
10,000 t<!--f:P10000.spec.payloadT--> of water. The largest is 876 m<!--f:P10000.spec.lenM--> long,
flies a 45.5-minute<!--f:P10000.cycle.cycleMin--> cycle at 15 km<!--f:worked.oneWayKm--> each way,
and delivers 13,183 t/h<!--f:P10000.cycle.tph--> at 4.59 kWh/t<!--f:P10000.cycle.kwhPerTonne-->.

**What the model does not say.** That the vehicle can be built. The model takes hull mass as an
assumption and computes forward from it; §4.1 is about that assumption and it does not survive
contact with the sources.

**Where the genuine invention is.** One place: the descent anchor (§3). It solves a real problem
that emerged mid-project, it is 58× cheaper than the rotor work it replaces, and it is the only
part of this concept that is not a scaling exercise on prior art.

**Why the scale is the point.** Energy per tonne *falls* as the ships get bigger —
12.53 kWh/t<!--f:P100.cycle.kwhPerTonne--> on the smallest against
4.59<!--f:P10000.cycle.kwhPerTonne--> on the largest — because buoyancy scales with volume and drag
with area. The square-cube law works against nearly every other vehicle and for this one. It is
the reason to be interested in the largest class rather than to start with the smallest.

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

A ship whose outlets jam rises. For an uncrewed vehicle over a fire, that turns a stuck valve from
a crash into an inconvenience. It costs displacement — 2,200 m³ per tonne of payload, giving
+5.25%<!--f:P10000.lift.floatUpMarginPct--> margin, 21,050.9 t<!--f:P10000.lift.atWorkAltT--> of
lift against 20,000 t<!--f:P10000.lift.loadedMassT--> loaded — and the project pays it rather than
trading it away. That is the correct instinct for a vehicle of this size operating autonomously
over people.

### 2.2 The cycle is timed, not asserted

| Phase | P-10000, min | What happens |
|---|---:|---|
| Source approach | 5.00<!--f:P10000.cycle.durations.SOURCE_APPROACH--> | dead stop, lower anchor and pumps |
| Fill | 11.11<!--f:P10000.cycle.durations.WATER_FILL--> | 15 m³/s<!--f:P10000.spec.fillM3s-->, no yaw |
| Outbound | 8.14<!--f:P10000.cycle.durations.OUTBOUND_TRANSIT--> | 130 km/h<!--f:P10000.spec.cruiseKph--> |
| Release | 11.11<!--f:P10000.cycle.durations.WATER_RELEASE--> | one pass |
| Escape | 2.00<!--f:P10000.cycle.durations.BUOYANCY_ESCAPE--> | buoyancy only, no propulsion |
| Return | 8.14<!--f:P10000.cycle.durations.RETURN_TRANSIT--> | |
| **Total** | **45.51**<!--f:P10000.cycle.cycleMin--> | 10,000 t<!--f:P10000.cycle.deliveredT--> delivered |

Water handling is 22.2 of 45.5 minutes. **The vehicle is a pump with a hull attached**, and at
operational ranges the binding constraint is transit distance only because transit is the term that
scales with distance. That has a commercial consequence: the value of the concept collapses toward
the value of a big pump if the fire is not near water.

<!--tex:fig charts/render-release.png | Mid-release, rendered from the model. Ten thousand tonnes leaves along the length of the keel in one pass; the hull rises off the line as it goes, which is why the escape climb costs no propulsion.-->

### 2.3 Throughput, if the vehicle exists

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Delivered per hour | 175 t<!--f:P100.cycle.tph--> | 1,697 t<!--f:P1000.cycle.tph--> | 13,183 t<!--f:P10000.cycle.tph--> |
| Energy per tonne | 12.53 kWh<!--f:P100.cycle.kwhPerTonne--> | 7.40 kWh<!--f:P1000.cycle.kwhPerTonne--> | 4.59 kWh<!--f:P10000.cycle.kwhPerTonne--> |
| Energy per cycle | 1.253 MWh<!--f:P100.cycle.eCycleMWh--> | 7.399 MWh<!--f:P1000.cycle.eCycleMWh--> | 45.869 MWh<!--f:P10000.cycle.eCycleMWh--> |

A 747 supertanker drops about 70 t and then flies to a base. Scale is the entire argument, and the
square-cube law means only the largest class is interesting: it is 2.3× cheaper per tonne than the
smallest.

---

## 3. The one genuine invention, and its exposure

### 3.1 What it is

The buoyancy that guarantees float-up must be overcome to descend, and it is worst at the bottom,
over the water, where the air is densest.

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Surplus to hold down at the lake | 135.6 t<!--f:P100.descent.holdAtSourceT--> | 1,366.9 t<!--f:P1000.descent.holdAtSourceT--> | 13,722.5 t<!--f:P10000.descent.holdAtSourceT--> |
| Rotor capability | 267.2 t<!--f:P100.descent.rotorCapT--> | 1,318.1 t<!--f:P1000.descent.rotorCapT--> | 12,666.2 t<!--f:P10000.descent.rotorCapT--> |

<!--tex:fig charts/descent.pdf | The problem the anchor solves. The bar is what has to be held down at the water; the tick is how far the rotors reach unaided. | 0.95-->

The two larger classes **cannot reach their own water source under power.** The solution is to
borrow the lake: lower a cable with a collapsible bag, fill it, winch it clear of the surface.
12,400 t<!--f:P10000.descent.anchorT--> of hanging water is
121.6 MN<!--f:P10000.descent.anchorPullMN--> of downward force for the 15 m of lift needed to break
the surface — **0.596 MWh<!--f:P10000.energy.ledgerMWh.anchor-->** against the 34.5 MWh of rotor
work it replaces.

The leverage is in the exponent: induced rotor power goes as thrust^1.5, so the letdown term falls
from 34.20 MWh to 1.420 MWh<!--f:P10000.energy.ledgerMWh.letdown--> — 96%. Alternatives, costed and
rejected in the open: nitrogen ballast **475 MWh**, a 1,350 m hose **44 MWh** at 2 m bore and
140 bar, retention **directly reduces the product**.

The mechanism cannot be over-sized: the most water a ship can lift is its own surplus lift, so the
physics supplies its own ceiling. And it pays on every class — removing the P-100's bag, which it
does not need, costs 34% more energy per cycle.

### 3.2 Its exposure

| Risk | Status |
|---|---|
| **Scale** | 12,400 t against the largest bucket ever built, 9,800 L. **1,265×.** The principle is 43 years old; the engineering is not. |
| **Cable** | 121.6 MN needs ~440 mm of UHMWPE massing 125 t — **not charged as dry mass anywhere in the model**, on a budget already over (§4.1). |
| **Pendulum** | 12,400 t swinging on one cable under an 876 m hull. Not modelled at all. |
| **Rotor wash on water** | The P-10000 has ~79 kg/m² disc loading against a Black Hawk's ~47, across 14 rotors whose combined disc area equals a single 451 m disc. A hovering Black Hawk must be over 160 ft up before surface wash falls below 30 mph (Suter 2005). The model has no wash physics, and the anchor requires a stationary hover over the surface it is disturbing. |
| **Station-keeping** | The mechanism requires a dead stop, no yaw while lines are down, and departure only when pumps clear the water. The model enforces these; nothing validates that a hull this size can hold station in the wind over a lake. |

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
joints, rotors, tanks, batteries, pumps, cable — equals the water it carries. For the P-10000 that
is 10,000 t inside 22,000,000 m³<!--f:P10000.spec.dispM3-->, a hull-average density of
**0.455 kg/m³**.

| Source | What it gives | Against our 0.455 kg/m³ |
|---|---|---|
| **Jenett et al. 2019** (NASA NTRS) — our own cited structural precedent | bare discrete-lattice shell, **0.508 kg/m³**, at every radius (their Table 2) | **12% over our entire dry allowance**, with nothing else fitted |
| **Metlen & Palazotto 2013** | only real-materials design has structure/buoyancy **0.94** | structure alone consumes what we allocate to structure *and* payload |
| **Akhmeteli & Gavrilin 2021** | payload fraction **0.1**, shell 1.16 kg/m³ | against our implied 0.5 |
| **Chin et al. 2021 / Lvovich 2020** (NASA) | X-57 flew **149 Wh/kg** at pack level from 225 Wh/kg cells | our 2,000 MWh<!--f:P10000.spec.battMWh--> battery masses ~13,400 t — **the battery alone is 34% over the whole dry budget** |

Four sources, four different objections, one conclusion. The 2,000 MWh battery figure deserves
emphasis: at the density NASA has actually flown, the battery by itself exceeds the entire dry mass
allowance before any structure exists. Even at 500 Wh/kg — the point Lvovich says NASA sees no
clear path past — the pack consumes 40% of a budget the hull already exceeds on its own.

**And there is a fifth objection that attacks the method rather than the numbers.** Both structural
sources hold shell mass fraction constant with radius — the scale invariance that lets a
metre-scale demonstration imply a 219 m<!--f:P10000.spec.diaM--> hull. Derveni et al. (2024) show
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

It is **45 W/m²**<!--f:assumptions.solarWPerM2--> now: 264 × 0.21 flexible module × 0.81 for
curvature, cell temperature, soiling and conversion, on a projected area.

| | solar | deficit/cycle | endurance |
|---|---|---|---|
| P-100 | 1.20 → **0.27 MW**<!--f:P100.energy.solarMW--> | 0.32 → **1.10**<!--f:P100.energy.deficitPerCycleMWh--> | 35.4 → **10.4 h**<!--f:P100.energy.hoursOnBattery--> |
| P-1000 | 5.60 → **1.26 MW**<!--f:P1000.energy.solarMW--> | 3.09 → **6.66**<!--f:P1000.energy.deficitPerCycleMWh--> | 22.9 → **10.6 h**<!--f:P1000.energy.hoursOnBattery--> |
| P-10000 | 24.00 → **5.40 MW**<!--f:P10000.energy.solarMW--> | 24.81 → **41.77**<!--f:P10000.energy.deficitPerCycleMWh--> | 61.1 → **36.3 h**<!--f:P10000.energy.hoursOnBattery--> |

*Diligence status:* **closed, and the finding underneath it is not.** Two things a reader should
take from this. First, the correction cut published endurance by roughly two thirds and the project
shipped it the same day — that is the behaviour the rest of this report is asking you to price.
Second, **no published throughput or energy-per-tonne figure moved at all**, because generation is
not in the ledger that computes them. A 4.4× error in the vehicle's power supply was invisible to
every test in the repository. That is §8's defect 6, it is still open, and it is the more
important half of this entry.

### 4.3 The nitrogen recovery was thermodynamically impossible — CORRECTED 2026-08-09

`rtLN2 = 0.50` against `eLN2 = 0.45`<!--f:assumptions.eLN2--> kWh/kg recovered **225 kWh per
tonne** of liquid nitrogen. The physical exergy of LN2 at 1 bar against a 288 K ambient is
**173.4 kWh/t** (Arnaiz-del-Pozo et al. 2020; independently corroborated at 205–214 kWh/t under
more favourable assumptions). The term returned 1.3× the work the liquid contains, before any
turbine or generator efficiency.

It is **0.20**<!--f:assumptions.rtLN2--> now — 90 kWh/t, 52% of the exergy, about what a cryogenic
expander returns with no external heat source. The P-10000's cycle rose 43.019 →
**45.869 MWh**<!--f:P10000.cycle.eCycleMWh-->, 6.6%. Two tests, one on each copy of the constant,
now fail the build if `rtLN2 × eLN2 × 1000` exceeds 173.4.

*Diligence status:* **closed.** Small in magnitude, absolute in kind, and worth reading for what it
says about how the model was being checked before: a unit test existed for this line and it was
asserting the violation as correct behaviour. The test now checks the physical ceiling as well as
the value, because the first is a choice and the second is not.

### 4.4 The headline metric may be measuring the wrong thing — strategic

Two findings from the wildfire-aviation literature, both aimed at the top of the funnel.

**The drop may not arrive.** The US Forest Service's 2022 assessment states that a drop released
1,000 ft above ground/vegetation "would completely dissipate". `ALT.drop` is 450 m — **1,476 ft**.
The altitude was raised for hull-clearance reasons that are sound (an 876 m hull cannot manoeuvre
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

## 5. Energy, and the only economics the model supports

### 5.1 The ledger

P-10000, 15 km<!--f:worked.oneWayKm--> each way, printed from the model:

| Term | MWh |
|---|---:|
| Return transit (drag + cryogenic plant) | 14.705<!--f:P10000.energy.ledgerMWh.RETURN_TRANSIT--> |
| Pumping | 10.900<!--f:P10000.energy.ledgerMWh.WATER_FILL--> |
| Hotel + manoeuvring | 10.689<!--f:P10000.energy.ledgerMWh.other--> |
| Outbound transit | 9.459<!--f:P10000.energy.ledgerMWh.OUTBOUND_TRANSIT--> |
| Letdown | 1.420<!--f:P10000.energy.ledgerMWh.letdown--> |
| Anchor | 0.596<!--f:P10000.energy.ledgerMWh.anchor--> |
| Nitrogen recovery (credit) | −1.900<!--f:P10000.energy.ledgerMWh.recovery--> |
| **Total** | **45.869**<!--f:P10000.cycle.eCycleMWh--> |

<!--tex:fig charts/ledger.pdf | The cycle ledger, printed from the model. Seventy-six per cent of it is transit and pumping; the mechanism that closes the descent costs 1.3%.-->

### 5.2 The fleet is a battery being spent

Every class runs a deficit every cycle. This is the project's central public conclusion and it is
stated on the site rather than hidden:

| | deficit/cycle | endurance |
|---|---:|---:|
| P-100 | 1.10 MWh<!--f:P100.energy.deficitPerCycleMWh--> | 10.4 h<!--f:P100.energy.hoursOnBattery--> |
| P-1000 | 6.66 MWh<!--f:P1000.energy.deficitPerCycleMWh--> | 10.6 h<!--f:P1000.energy.hoursOnBattery--> |
| P-10000 | 41.77 MWh<!--f:P10000.energy.deficitPerCycleMWh--> | 36.3 h<!--f:P10000.energy.hoursOnBattery--> |

Those figures are post-correction and roughly a third of what this report would have carried a day
earlier. There is no configuration in which this fleet sustains itself; it requires an energy
import chain, and that chain is the business.

<!--tex:fig charts/deficit.pdf | Spend against generation, and endurance on a full battery. This is the project's central public conclusion and it is not a favourable one.-->

### 5.3 Grid implications — the number that should govern the conversation

**The model publishes no cost, and nothing below is a model output.** These are derived from model
energy figures and the published BC Hydro Transmission Service Rate Schedule 1830 (effective
1 April 2026: demand $12.178/kV·A, energy 4.914 ¢/kWh). Assumptions stated inline.

- **Continuous draw per P-10000 in sustained operation:** 45.869 MWh<!--f:P10000.cycle.eCycleMWh-->
  per 45.51-minute<!--f:P10000.cycle.cycleMin--> cycle = **60.5 MW average**. Net of the corrected
  solar (5.40 MW<!--f:P10000.energy.solarMW-->), **55.1 MW imported**. That is 9% worse than this
  report said before the 2026-08-09 corrections, and the earlier figure was the optimistic one.
- **Energy cost per tonne delivered** at 4.914 ¢/kWh: **$0.23/t** for the P-10000
  (4.59 kWh/t<!--f:P10000.cycle.kwhPerTonne-->), **$0.62/t** for the P-100
  (12.53 kWh/t<!--f:P100.cycle.kwhPerTonne-->). Per 10,000 t drop: **~$2,250**.
- **A ten-ship P-10000 fleet** in continuous operation imports roughly **550 MW**. At Schedule 1830
  that is on the order of **US$26M per month** — about $20M energy and $7M demand — assuming unity
  power factor and continuous operation. Given to one significant digit because the duty-cycle
  assumption dominates it.

**The governing comparison:** BC Hydro's total generating capacity is **13.4 GW** (Site C fully
operational). A single P-10000's 1,400 MW<!--f:P10000.spec.battMW--> battery discharge peak is
**over 10% of the province's entire generating capacity.** A ten-ship fleet's sustained import is
**4.1% of provincial capacity**, continuously, during fire season — which is also peak demand
season.

That is not a tariff problem, it is an interconnection and generation-planning problem, and it has
a lead time measured in years. BC Hydro's 2025 capacity call drew 106 submissions totalling 19 GW,
which indicates the queue this would join.

**Not costed anywhere, and material:** capital cost of a hull (no basis exists), the megawatt-scale
charging infrastructure at each operating base, battery replacement cycles, and the cost of the
fire-season duty factor — a fleet sized for August is idle in February.

---

## 6. Regulatory and legal

| Question | Finding | Status |
|---|---|---|
| **Taking the water** | BC's *Water Sustainability Act* permits diverting unrecorded water for firefighting **without authorisation**, and a fire department may divert, use and store water for firefighting preparation without authorisation. | **Clear on its face.** The legal half is the easy half. |
| **The lake's capacity** | The Act says nothing about whether a lake can stand repeated 10,000 t draws. A P-10000 removes 13,183 t/h<!--f:P10000.cycle.tph--> from one body of water. | **Open.** Hydrological, not legal, and unaddressed. |
| **Flying it** | ICAO Chicago Convention Art. 1 (sovereignty) and Art. 8 (pilotless aircraft need special authorisation over another state). FAA/EASA routes for large uncrewed aircraft exist but nothing of this scale has been certificated. | **Open, long lead.** No certification basis exists for an 876 m uncrewed vehicle. |
| **Autonomy assurance** | FAA 2024 AI safety-assurance roadmap, EASA AI roadmap 2.0, NIST AI RMF, runtime-assurance literature all catalogued as context. | **Open.** No work done. |
| **Weather modification law** | ENMOD catalogued. Not obviously engaged by water delivery. | Low. |

The regulatory path is the second-longest pole after the structure, and unlike the structure it
cannot be shortened by a good result in a lab.

---

## 7. Quality of the evidence base

This is where the project is genuinely strong, and it is the reason the §4 findings exist at all.

| Artefact | What it is |
|---|---|
| `sim/` | The model. No DOM, network, storage, wall clock or location — enforced by a boundary linter across 80 modules. |
| `tests/` | 206 tests in 39 suites, plus 103 more that need node. **Two fail on purpose**, marked `knownFail`, so a documented defect cannot quietly lose its excuse. |
| `tests/golden/` | 151 class/mode/distance/wind combinations, diffed on every run. Independently reproduced by a separate Python implementation. |
| `research/sources.json` | 73 sources: 3 load-bearing, **9 that contradict us**, 20 supporting, 41 context. 29 redistributable PDFs with provenance records; everything paywalled catalogued and refused by name. |
| `research/notes/` | 12 notes, each written from the source PDF rather than its abstract, each stating where the source does *not* support what we would like it to. |
| `research/evidence-map.md` | Audit of all 89 published claims. |
| `research/figures.json` | Every published figure, regenerated from the live model. `tools/check_figures.py` fails the build if any report disagrees. |
| `docs/OPEN-QUESTIONS.md` | Thirteen defects, each with cost, options and a recommendation. Two closed, eleven open. |

<!--tex:fig charts/sensitivity.pdf | Every constant moved ±20%, generated rather than transcribed. Where the model's uncertainty actually lives: aerodynamics and speed, not lift.-->

**The signal to weigh.** The defect list went from six to thirteen the day the project audited
itself properly — and it is the same model. Nothing was introduced; it was all already true and
unnoticed. Six were found by the authors, two by auditing claims against code, four by reading the
sources. That ratio is the argument for the process and the warning about the numbers.

**The two largest errors ever found in this model were both accounting, not physics.** The
nitrogen recovery was netted against the pump bill under a `max(0, …)` and silently deleted the
entire pumping cost on two of three classes; and the lift ledger bought air at sea level and spent
it at altitude, overstating lift by 22%. Neither was caught by a test. Both were caught by
re-deriving a published number from scratch.

**Where the process is still weak:** 32 of 89 published figures rest on constants with no stated
justification, against 15 genuine documented assumptions. Two undocumented inline drag multipliers
are worth 16.9 MWh a cycle, while the defect flagged in the README since the first commit is worth
1.4. The project has been auditing the things it knew to doubt.

**And the test suite had a hole in it that is worth understanding.** 103 of the tests need node,
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
   only §2 finding that both remains open and is capable of ending the concept** — §4.2 and §4.3
   are closed, and §4.4 changes what the product is rather than whether it can exist.
2. **A battery at ≥200 Wh/kg pack level, with the rest of the vehicle free.** Not available; NASA
   has flown 149 and sees no clear path past 500.
3. **A drop from a height an 876 m hull can safely use that still arrives as water.** Currently
   contradicted by USFS guidance. Needs droplet physics and, eventually, a drop test.
4. **A 12,400 t suspended bag, its cable, its pendulum dynamics, and hull station-keeping over
   water in wind.** The mechanism is sound in principle and unbuilt at 1,265× the precedent.
5. **An interconnection.** ~50 MW continuous per large ship, in a 13.4 GW province, during peak
   season.
6. **That tonnes delivered is the right product.** AFUE says effectiveness turns on ground
   engagement, which an uncrewed fleet does not have.

Items 1 and 2 are structural facts about materials that no amount of engineering effort inside this
project can change. **They should be resolved before anything else is funded**, and they are cheap
to resolve relative to everything downstream: they are literature and expert review, not hardware.

---

## 9. Assessment

**On the concept.** Unproven and currently contradicted at its foundation. The mass premise fails
against the project's own cited precedent by 12% before anything is fitted, and the battery alone
exceeds the whole dry allowance at demonstrated pack densities. Neither is a detail; both are the
first line of the ledger. A reader looking for a reason to stop has one, in §4.1, sourced.

**On the invention.** The descent anchor is real, is not obvious, solves a problem the project
discovered rather than invented, and is 58× cheaper than the alternative. It is worth attention on
its own terms — including, possibly, on vehicles other than this one. It is also published openly
and therefore unprotected.

**On the work.** The apparatus is better than the concept. A model that fails its own audit in
public, keeps two tests failing on purpose, catalogues nine sources that contradict it, and grows
its defect list from six to thirteen by checking properly is doing the thing most concept work
avoids. The clearest evidence is what happened on 2026-08-09: two of the four findings in §4 were
corrected within hours of being found, both corrections made the published numbers worse — cycle
energy up 6.6%, endurance down by roughly two thirds — and both shipped to the live site the same
day. If the question is "will this team find out whether the idea works", the evidence is
strongly yes. If the question is "does the idea work", the evidence today is **no, on the mass
budget**, and the project says so itself in `docs/OPEN-QUESTIONS.md` #11.

**Recommended next step, at minimal cost:** commission a lattice-structure mass breakdown at
100 m and 219 m radius from a group that builds them, and an independent pack-level mass estimate
for a 2,000 MWh flight battery. If either comes back where the literature suggests, the concept
needs a different vehicle — smaller, or hybrid-lift, or not buoyant at all — and finding that out
costs two reviews rather than a programme.

---

## 10. Sources and reproduction

```
git clone github.com/pinkrobotics/airships && cd airships && make check
```

`make golden` diffs 151 cases; `make test` runs 206 tests including two deliberate failures and
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
