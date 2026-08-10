# Vacuum-lift wildfire airships: a diligence report

**Pink Robotics · 2026-08-09 · v1 · prepared for readers doing technical and commercial diligence**

---

## 0. How to read this document

This is a diligence report on a **concept**, not on a company, a product, or a prototype. Nothing
has been built. There is no revenue, no letter of intent, no flight article, and no test rig.

What exists is a simulation and its supporting apparatus: a physics model, 196 tests, a 151-case
deterministic golden baseline, a 73-source catalogue with 12 written notes, an audit of all 89
published claims, and a defect list of thirteen items. That apparatus is the asset under
examination. **The correct question for a reader is not "do these numbers work" but "is this the
kind of work that would find out if they didn't".**

The report is organised so that the disqualifying findings come first. §2 could end the
conversation and is placed where it can. If you read one section, read §2.

Every model figure is cited by key and verified automatically against the model
(`tools/check_figures.py`; the build fails on a mismatch). Every external figure names its source.
Where nothing is known, the section says so rather than estimating.

---

## 1. The thesis in one page

**Claim.** Aerial firefighting is limited by turnaround, not by drop size. A vehicle that dips from
a lake like a helicopter but carries like a tanker would change the sustained delivery rate by
orders of magnitude. Buoyant flight is the only way to get payload without paying for lift
continuously. Helium is expensive and leaks; vacuum is free and does not — if the shell can be
made light enough, which modern discrete-lattice construction may finally allow.

**What the model says.** Three classes, from 100 t<!--f:P100.spec.payloadT--> to
10,000 t<!--f:P10000.spec.payloadT--> of water. The largest is 876 m<!--f:P10000.spec.lenM--> long,
flies a 45.5-minute<!--f:P10000.cycle.cycleMin--> cycle at 15 km<!--f:worked.oneWayKm--> each way,
and delivers 13,183 t/h<!--f:P10000.cycle.tph--> at 4.59 kWh/t<!--f:P10000.cycle.kwhPerTonne-->.

**What the model does not say.** That the vehicle can be built. The model takes hull mass as an
assumption and computes forward from it; §2.1 is about that assumption and it does not survive
contact with the sources.

**Where the genuine invention is.** One place: the descent anchor (§4). It solves a real problem
that emerged mid-project, it is 58× cheaper than the rotor work it replaces, and it is the only
part of this concept that is not a scaling exercise on prior art.

**What would make this investable.** Not a better simulation. A gram-level mass breakdown of a
lattice shell at scale, from someone who builds them. Everything else is downstream of that number
and the number is currently missing (§8).

---

## 2. Disqualifying findings

Four findings from the source catalogue contradict the model. Two are severe enough to be
disqualifying on their own. They are stated here first, in full, with their arithmetic.

### 2.1 The mass budget fails against four independent sources — SEVERE

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

### 2.2 The solar skin requires 76% conversion efficiency — SEVERE for sustainment

The model credits the skin a flat **200 W/m² of electrical output**, continuously. NRCan's dataset
gives 6.34 kWh/m²/day mean July horizontal insolation across eight BC interior fire-belt towns:
**264 W/m² incident**, day-averaged. 200 out of 264 is 76% conversion. At 20% modules — generous
for flexible cells on a curved hull, most of which faces the wrong way at any moment — the honest
figure is **53 W/m²**.

Consequence for the P-10000: solar 5.4<!--f:P10000.energy.solarMW--> → 6.4 MW; per-cycle
generation 4.10<!--f:P10000.energy.solarPerCycleMWh--> → 4.83 MWh; deficit
41.77<!--f:P10000.energy.deficitPerCycleMWh--> → 38.19 MWh; endurance
36.3 h<!--f:P10000.energy.hoursOnBattery--> → about 40.

*Diligence status:* arithmetically trivial to fix, and **it moves the project's stated conclusion in
the direction that conclusion already points** — the fleet is more dependent on imported energy, not
less. No commercial claim rests on the 200 W/m² figure.

### 2.3 The nitrogen recovery is thermodynamically impossible — narrow but absolute

`rtLN2 = 0.20`<!--f:assumptions.rtLN2--> against `eLN2 = 0.45`<!--f:assumptions.eLN2--> kWh/kg
recovers **225 kWh per tonne** of liquid nitrogen. The physical exergy of LN2 at 1 bar against a
288 K ambient is **173.4 kWh/t** (Arnaiz-del-Pozo et al. 2020; independently corroborated at
205–214 kWh/t under more favourable assumptions). The term returns 1.3× the work the liquid
contains, before any turbine or generator efficiency.

The absolute ceiling is `rtLN2 ≤ 0.385`; a plant that exists would be nearer 0.25. Cost of the
correction: about 1.0 MWh a cycle, 2.4%.

*Diligence status:* small in magnitude, absolute in kind. A reviewer who finds this before you do
will discount everything else in the model, and they would be right to.

### 2.4 The headline metric may be measuring the wrong thing — strategic

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

## 3. What survives §2

Everything below is conditional on §2.1. Read it as "if a shell can be built, then —".

### 3.1 The sizing logic is sound and safety-led

Displacement is not chosen to make the numbers work. It is set by a fail-safe requirement:

> A hull must be positively buoyant at its working altitude while **fully loaded with water and
> unable to release it.**

A ship whose outlets jam rises. For an uncrewed vehicle over a fire, that turns a stuck valve from
a crash into an inconvenience. It costs displacement — 2,200 m³ per tonne of payload, giving
+5.25%<!--f:P10000.lift.floatUpMarginPct--> margin, 21,050.9 t<!--f:P10000.lift.atWorkAltT--> of
lift against 20,000 t<!--f:P10000.lift.loadedMassT--> loaded — and the project pays it rather than
trading it away. That is the correct instinct for a vehicle of this size operating autonomously
over people.

### 3.2 The cycle is timed, not asserted

| Phase | P-10000, min | |
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

### 3.3 Throughput, if the vehicle exists

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Delivered per hour | 175 t<!--f:P100.cycle.tph--> | 1,697 t<!--f:P1000.cycle.tph--> | 13,183 t<!--f:P10000.cycle.tph--> |
| Energy per tonne | 12.53 kWh<!--f:P100.cycle.kwhPerTonne--> | 7.40 kWh<!--f:P1000.cycle.kwhPerTonne--> | 4.59 kWh<!--f:P10000.cycle.kwhPerTonne--> |
| Energy per cycle | 1.253 MWh<!--f:P100.cycle.eCycleMWh--> | 7.399 MWh<!--f:P1000.cycle.eCycleMWh--> | 45.869 MWh<!--f:P10000.cycle.eCycleMWh--> |

A 747 supertanker drops about 70 t and then flies to a base. Scale is the entire argument, and the
square-cube law means only the largest class is interesting: it is 2.3× cheaper per tonne than the
smallest.

---

## 4. The one genuine invention, and its exposure

### 4.1 What it is

The buoyancy that guarantees float-up must be overcome to descend, and it is worst at the bottom,
over the water, where the air is densest.

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Surplus to hold down at the lake | 135.6 t<!--f:P100.descent.holdAtSourceT--> | 1,366.9 t<!--f:P1000.descent.holdAtSourceT--> | 13,722.5 t<!--f:P10000.descent.holdAtSourceT--> |
| Rotor capability | 267.2 t<!--f:P100.descent.rotorCapT--> | 1,318.1 t<!--f:P1000.descent.rotorCapT--> | 12,666.2 t<!--f:P10000.descent.rotorCapT--> |

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

### 4.2 Its exposure

| Risk | Status |
|---|---|
| **Scale** | 12,400 t against the largest bucket ever built, 9,800 L. **1,265×.** The principle is 43 years old; the engineering is not. |
| **Cable** | 121.6 MN needs ~440 mm of UHMWPE massing 125 t — **not charged as dry mass anywhere in the model**, on a budget already over (§2.1). |
| **Pendulum** | 12,400 t swinging on one cable under an 876 m hull. Not modelled at all. |
| **Rotor wash on water** | The P-10000 has ~79 kg/m² disc loading against a Black Hawk's ~47, across 14 rotors whose combined disc area equals a single 451 m disc. A hovering Black Hawk must be over 160 ft up before surface wash falls below 30 mph (Suter 2005). The model has no wash physics, and the anchor requires a stationary hover over the surface it is disturbing. |
| **Station-keeping** | The mechanism requires a dead stop, no yaw while lines are down, and departure only when pumps clear the water. The model enforces these; nothing validates that a hull this size can hold station in the wind over a lake. |

**Positive IP note:** this is the one part of the concept that is not obvious from prior art, and
it is currently published openly. If there is defensible IP here, it is being given away. That is a
deliberate consequence of the open-source strategy and should be a conscious decision rather than a
side effect.

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

### 5.2 The fleet is a battery being spent

Every class runs a deficit every cycle. This is the project's central public conclusion and it is
stated on the site rather than hidden:

| | deficit/cycle | endurance |
|---|---:|---:|
| P-100 | 1.10 MWh<!--f:P100.energy.deficitPerCycleMWh--> | 10.4 h<!--f:P100.energy.hoursOnBattery--> |
| P-1000 | 6.66 MWh<!--f:P1000.energy.deficitPerCycleMWh--> | 10.6 h<!--f:P1000.energy.hoursOnBattery--> |
| P-10000 | 41.77 MWh<!--f:P10000.energy.deficitPerCycleMWh--> | 36.3 h<!--f:P10000.energy.hoursOnBattery--> |

Correcting §2.2 takes the P-10000 to about 40 hours. There is no configuration in which this fleet
sustains itself; it requires an energy import chain, and that chain is the business.

### 5.3 Grid implications — the number that should govern the conversation

**The model publishes no cost, and nothing below is a model output.** These are derived from model
energy figures and the published BC Hydro Transmission Service Rate Schedule 1830 (effective
1 April 2026: demand $12.178/kV·A, energy 4.914 ¢/kWh). Assumptions stated inline.

- **Continuous draw per P-10000 in sustained operation:** 45.869 MWh<!--f:P10000.cycle.eCycleMWh-->
  per 45.51-minute<!--f:P10000.cycle.cycleMin--> cycle = **56.7 MW average**. Net of solar at the
  model's optimistic 200 W/m² that is ~32.7 MW imported; at the honest 53 W/m² (§2.2), **~50.3 MW**.
- **Energy cost per tonne delivered** at 4.914 ¢/kWh: **$0.21/t** for the P-10000
  (4.59 kWh/t<!--f:P10000.cycle.kwhPerTonne-->), $0.49/t for the P-100. Per 10,000 t drop: **~$2,100**.
- **A ten-ship P-10000 fleet** in continuous operation imports roughly **500 MW**. At Schedule 1830
  that is on the order of **US$20–25M per month** in energy and demand charges combined, assuming
  unity power factor and continuous operation — figures given to one significant digit because the
  duty cycle assumption dominates them.

**The governing comparison:** BC Hydro's total generating capacity is **13.4 GW** (Site C fully
operational). A single P-10000's 1,400 MW<!--f:P10000.spec.battMW--> battery discharge peak is
**over 10% of the province's entire generating capacity.** A ten-ship fleet's sustained import is
~4% of provincial capacity, continuously, during fire season — which is also peak demand season.

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

This is where the project is genuinely strong, and it is the reason the §2 findings exist at all.

| Artefact | What it is |
|---|---|
| `sim/` | The model. No DOM, network, storage, wall clock or location — enforced by a boundary linter across 80 modules. |
| `tests/` | 196 tests, 38 suites. **Two fail on purpose**, marked `knownFail`, so a documented defect cannot quietly lose its excuse. |
| `tests/golden/` | 151 class/mode/distance/wind combinations, diffed on every run. Independently reproduced by a separate Python implementation. |
| `research/sources.json` | 73 sources: 3 load-bearing, **9 that contradict us**, 20 supporting, 41 context. 29 redistributable PDFs with provenance records; everything paywalled catalogued and refused by name. |
| `research/notes/` | 12 notes, each written from the source PDF rather than its abstract, each stating where the source does *not* support what we would like it to. |
| `research/evidence-map.md` | Audit of all 89 published claims. |
| `research/figures.json` | Every published figure, regenerated from the live model. `tools/check_figures.py` fails the build if any report disagrees. |
| `docs/OPEN-QUESTIONS.md` | Thirteen defects, each with cost, options and a recommendation. |

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

---

## 8. What would have to be proven, in order

1. **A lattice vacuum shell at ≤0.455 kg/m³ including everything.** Nothing in the literature is
   there. Not resolvable by modelling. Requires a gram-level mass breakdown from someone who builds
   these structures, plus an answer to the Derveni scale-invariance objection (§2.1).
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
first line of the ledger. A reader looking for a reason to stop has one, in §2.1, sourced.

**On the invention.** The descent anchor is real, is not obvious, solves a problem the project
discovered rather than invented, and is 58× cheaper than the alternative. It is worth attention on
its own terms — including, possibly, on vehicles other than this one. It is also published openly
and therefore unprotected.

**On the work.** The apparatus is better than the concept. A model that fails its own audit in
public, keeps two tests failing on purpose, catalogues nine sources that contradict it, and grows
its defect list from six to thirteen by checking properly is doing the thing most concept work
avoids. If the question is "will this team find out whether the idea works", the evidence is
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

`make golden` diffs 151 cases; `make test` runs 196 tests including two deliberate failures;
`make factsheet` regenerates every published figure from the live model; `tools/check_figures.py`
fails the build if this document disagrees with it. `?seed=7&data=snapshot` reproduces any run on
the live site exactly.

Full catalogue: `research/sources.json`. Notes: `research/notes/`. Claim audit:
`research/evidence-map.md`. Defect list: `docs/OPEN-QUESTIONS.md`. Physics derivations:
`docs/PHYSICS.md`.

**Load-bearing sources:** Jenett et al. 2019 (NASA NTRS, redistributable — verified by hash against
the NTRS original); Akhmeteli & Gavrilin 2021 (CC BY); NOAA/NASA/USAF *U.S. Standard Atmosphere
1976*.

**Sources that contradict us:** Metlen & Palazotto 2013; Derveni et al. 2024; Arnaiz-del-Pozo et
al. 2020; NRCan 2020; USFS AFUE 2020; USFS 2022; Suter 2005; Chin et al. 2021; Lvovich 2020.

---

*Every figure marked in this document is generated by the model and verified automatically.
External figures name their source. Derived commercial figures in §5.3 state their assumptions and
are not model outputs — the model publishes no cost.*
