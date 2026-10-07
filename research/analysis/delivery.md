# Does the water arrive?

The flight model assumes a hull that floats; no drawn hull does. See [the float case](../../docs/FLOAT.md).

`docs/OPEN-QUESTIONS.md` asks whether a high release reaches the fuel and whether tonnes
measure useful work. The Forest Service's training-jettison dissipation statement is a
comparison, not a deposition model. AFUE measures objectives rather than tank tonnage.

<!-- logistics:release-air:start -->
The model release is 450 m above terrain at 1000 m MSL, hence 1450 m MSL; its reference-atmosphere density is 1.063334 kg/m³. These are model inputs, not sampled fire weather.
<!-- logistics:release-air:end -->

Computed by `research/analysis/delivery.py`. This is the first time this project has looked at
what happens between the tank and the fuel.

## First, the mission this vehicle is actually for

**Remote pre-wetting** means wetting ground well before any fire is near: a containment
corridor prepared in advance or a proposed moisture treatment during a heat event. There is
no nearby fire driving a plume in that mission, so timing can be chosen for suitable ambient
weather. Low, slow release still needs a demonstrated aircraft and release envelope; neither
flight nor useful wetting has been established.

**Work ahead of an active front is a separate mission.** Unburned fuel does not put a release
outside fire-generated airflow or a bent-over plume. [Lareau and Clements](https://doi.org/10.1175/JAMC-D-16-0384.1)
observe convergence and a disturbance extending beyond the plume base in their velocity-field
section and plume-velocity figure. That observed reach is not an operating standoff.

To establish a release outside the fire's disturbed air would require local, time-resolved wind
profiles and vertical velocity observations across the hull, release line and fall path, plus
plume location and motion observations, compared with nearby undisturbed air. Scanning Doppler
lidar or radar, in-situ wind measurements and plume imagery are candidate observations; smoke
imagery alone cannot exclude disturbed clear air. Their spatial coverage, uncertainty and
changes during the pass must support exclusion from the plume and its inflow under an
independently demonstrated operating envelope. This model supplies neither those observations
nor a universal distance. Direct attack remains an extreme delivery screen, with no established
survival or changed fire outcome.

Read what follows as the extreme case, with a limit on free-drop delivery at any release
height: a drop cannot descend where air at and below the release rises faster than it falls.
The free-drop reference and local corrected speeds are generated below.
Lowering the sprayers does not remove that limit; the proposed operating
envelope is release **outside active convection columns**. Direct-attack survival has not
been established.

## Free-drop speed depends on the air

<!-- logistics:drop-reference:start -->
For 2 mm drops, terminal speed is 6.5 m/s in the sea-level reference table; at the model release it is 6.903 m/s.

The retained Gunn–Kinzer table describes free drops in sea-level reference air, rather than a density-independent property of water. Drops near and above 5.5 mm can break up. The density adjustment in [Ghiggi et al.](https://doi.org/10.5194/amt-19-4943-2026), Appendix B1, Eq. B1, printed p. 4967, is applied to that table through the model's dry standard-atmosphere column.

| Diameter mm | Sea-level reference m/s | At release m/s | At ground m/s | Fall time s |
|---|---|---|---|---|
| 0.5 | 2.1 | 2.218 | 2.181 | 204.609 |
| 1 | 4.0 | 4.233 | 4.158 | 107.260 |
| 2 | 6.5 | 6.903 | 6.774 | 65.810 |
| 3 | 8.1 | 8.633 | 8.462 | 52.653 |
| 5 | 9.1 | 9.767 | 9.553 | 46.589 |

This empirical correction holds diameter fixed and integrates inverse terminal speed down to the ground. It does not solve break-up, evaporation, entrainment, initial acceleration, humidity or a separate viscosity correction. No deposition or flight envelope follows.
<!-- logistics:drop-reference:end -->

<!-- logistics:drop-drift:start -->
**The pattern smears, and the smear is worse than the drift.** A stipulated uniform 10 m/s wind translates the pattern, while the spread of fall times stretches it. At the model release height, 0.5 mm drops fall for 204.609 s and 5 mm drops for 46.589 s. The resulting along-wind spread is 1580.207 m, against the 1.2 km planned release run. This is a fixed-diameter, no-updraft sensitivity, not a ground pattern.

**The mean drift is also conditional:**

| Release example / height AGL m | Fall time, 2 mm s | Drift at 3 m/s, m | Drift at 5 m/s, m | Drift at 10 m/s, m | Drift at 15 m/s, m |
|---|---|---|---|---|---|
| single-engine airtanker / 18 | 2.656 | 8 | 13 | 27 | 40 |
| large airtanker / 53 | 7.816 | 23 | 39 | 78 | 117 |
| very large airtanker / 122 | 17.965 | 54 | 90 | 180 | 269 |
| USFS 'completely dissipates' / 305 | 44.740 | 134 | 224 | 447 | 671 |
| P-series ALT.drop / 450 | 65.810 | 197 | 329 | 658 | 987 |
| sprayer lead, hull 450 m - 300 m lead / 150 | 22.075 | 66 | 110 | 221 | 331 |
| sprayer lead, hull 450 m - 400 m lead / 50 | 7.374 | 22 | 37 | 74 | 111 |

Each wind is a stipulated uniform horizontal input; the reference jettison heights are comparisons, and every row uses the same model terrain and atmospheric column.
<!-- logistics:drop-drift:end -->

*(The three airtanker rows are USFS **training-jettison** heights, which is the only published
table; real operational drops are lower again — DC-10 practice is 150–300 ft AGL. And the
"1,000 ft would completely dissipate" statement this page opens with is about gum-thickened
long-term retardant jettisoned over a designated area, in a document arguing to the Fish and
Wildlife Service that it does not reach listed species. It is evidence for the direction of
this arithmetic, not the same finding as it.)*

<!-- logistics:drop-updraft:start -->
**Free drops descend only where their downward speed relative to the air exceeds the local upward air motion.** The following updrafts are stipulated screens, not observed weather or operating limits. Diameter is held fixed.

| Stipulated case | Updraft m/s | Diameters descending throughout the reference column, mm |
|---|---|---|
| quiet flank | 5 | 2, 3, 5 |
| active flank | 10 | none in reference air |
| crown fire column | 25 | none in reference air |

A stipulated 15 K warming at unchanged pressure raises the 5 mm release speed from 9.767 to 10.027 m/s, near the 10 m/s screen. This is a threshold case: reference-speed precision and empirical/model uncertainty do not establish a robust crossing, and release-level speed does not establish descent through the full column. No quantitative confidence interval is supplied by this calculation.
<!-- logistics:drop-updraft:end -->

This is true of every airtanker ever flown, which is why aerial suppression lays line in
*unburned* fuel beside and ahead of a fire rather than dropping onto flame. It is a statement
about free drops after breakup, not about the coherent, air-entraining mass a load is for its
first tens of metres — that descends much faster, which is how airtankers work at all.

## The ship makes its own updraft, and this is the one nobody had noticed

**A buoyant hull holds station by thrusting downward, so its rotors accelerate air *upward*.**
That is the opposite sign to a helicopter, and it happens directly over the release.

<!-- editorial:release-illustration:start -->
The producer replays the accepted 15 km balanced reference plan (record basis), releasing 70.948 t and retaining 29.052 t. The release endpoints use local air density, water aboard and rotor force ownership:

| State | AGL altitude | Local density | Water aboard | Rotor hold | Ideal induced velocity upward | Ideal far-wake velocity | Ideal air flow |
|---|---|---|---|---|---|---|---|
| start of release | 450 m | 1.063334 kg/m³ | 100.0 t | 33.933 tf | 7.9 m/s | 15.8 m/s | 21,035 kg/s |
| end of release | 580 m | 1.049682 kg/m³ | 29.1 t | 101.877 tf | 13.8 m/s | 27.6 m/s | 36,212 kg/s |

The endpoint ideal-disc air-flow estimate is **36,212 kg/s**, **72.4 times** the nominal **500 kg/s** water-rate benchmark from configured intake capacity. The accepted plan's mean tank release rate is 498.9 kg/s. Neither quantity measures outlet flow, a wake, drift or where water lands. At the end of release, the ideal induced upward velocity of 13.8 m/s exceeds the largest tabulated density-corrected release-level fall speed, 9.767 m/s. This compares the named endpoint with fixed-diameter drop speeds in the model air; it does not represent every drop or a ground pattern. The upward-flow sign motivates further investigation; ideal-disc arithmetic alone does not establish deposition or suppression.
<!-- editorial:release-illustration:end -->

## Which is the argument for putting the sprayers on leads

The vehicle already lowers a 300 m hose to pick water up. **Lowering sprayer leads to put it
down is the same mechanism in reverse**: the shorter fall reduces drift, and the release is
farther from the ship's own wake. Below the disc the rotor flow is approximated as a sink,
which falls off as 1/z². This does not remove ambient rising air in a fire column:

<!-- editorial:release-inflow:start -->
Point-sink heuristic using the accepted release endpoint's ideal-disc volume flow; this is not a measured wake:

| Distance below hull | Reference heuristic inflow |
|---|---|
| 50 m below | 2.20 m/s |
| 100 m below | 0.55 m/s |
| 200 m below | 0.14 m/s |
| 300 m below | 0.06 m/s |
| 400 m below | 0.03 m/s |
<!-- editorial:release-inflow:end -->

*(Point-sink far field, valid for distances well beyond the disc radius — 28 m on a P-100. It
is not valid close under the very large discs of the bigger classes, and their near field has
not been computed.)*

**A few hundred metres of lead greatly reduces the calculated rotor sink flow at release**
and shortens the fall while keeping the hull higher. It does not establish a safe hull height
or descent through an active column. The release height
stops being a compromise between hull clearance and delivery, and becomes a **control input** —
long lead in calm air for a precise line, short lead when turbulence says stay high, and the
choice made per pass. Multiple leads, like the multiple pumps and multiple bags the fleet
already implies, spread the release across a wider swath and shorten the run.

This is the single highest-value change on this page, and it needs no new physics: it is the
intake hose, pointed the other way.

## What the accepted plans release

Coverage level expresses liquid volume per ground area in US gallons per 100 ft². The fuel
coverage levels in the [USFS AT-802 drop guide](https://www.fs.usda.gov/t-d/pubs/pdfpubs/pdf17512802P/1751-2802P_AT-802DropGuide_Sec508_03-01-19_150dpi.pdf)
(Table 1, PDF p. 3) are **retardant prescriptions**, not prescriptions for plain water.
The table below is an **even-spread water depth in coverage-level units**: released tonnes
over the accepted plan's run and an assumed swath, with all released water assigned to that
rectangle. It is not a measured ground pattern or a dose reaching a named fuel layer.

<!-- logistics:one-pass:start -->
| Swath | P-100 CL | P-1000 CL | P-10000 CL |
|---|---|---|---|
| 20 m | 7.3 | 9.4 | 72.3 |
| 30 m | 4.8 | 6.3 | 48.2 |
| 50 m | 2.9 | 3.8 | 28.9 |
| 80 m | 1.8 | 2.4 | 18.1 |

| Class | Released t | Run km | Retained t |
|---|---|---|---|
| P-100 | 70.948 | 1.2 | 29.052 |
| P-1000 | 191.775 | 2.5 | 808.225 |
| P-10000 | 2945.496 | 5.0 | 7054.504 |

These are tank-release quotients for the accepted 15 km plans, at assumed swaths. No ground deposition or suppression is established.
<!-- logistics:one-pass:end -->

This arithmetic supports a comparison of released payload and run length, not a water
prescription or suppression performance. A water prescription would need a ground-pattern
test, including deposition in the intended fuel layer, and a wetting test in named fuels
under stated weather conditions.

## The metric that means something

AFUE counts objectives achieved, not litres, and for large aircraft the objective is nearly
always line. BC campaign fires, 615 with mapped perimeters: median **40.6 km**, p90 146.3 km.

A conditional line-length comparison for a P-100 at the median leg:

<!-- logistics:daily:start -->
| Coverage level | Geometric line km per 24 h | Stored simplified perimeters no longer than that line |
|---|---|---|
| CL 2 | 186.0 km | 93.8% |
| CL 4 | 93.0 km | 80.0% |
| CL 6 | 62.0 km | 67.6% |
| CL 8 | 46.5 km | 56.7% |

At the 4.71 km median shore-proxy distance the accepted rapid plan releases 65.000 t and retains 35.000 t per cycle. Its rate is 189.5 t/h, with 3.933 MWh supplied per 20.584 minute cycle. Repeating it for 24 hours gives 4,547 t released and requires 275.1 MWh of supplied effort. Stand-downs across the fire-leg dataset: 277.

The table compares line length at an assumed 30 m swath with stored simplified final perimeter lengths. Those outlines are lower bounds on a convoluted edge. It establishes neither deposition nor coverage of an actual fire, continuous operation or supply, suppression, or a changed fire outcome.
<!-- logistics:daily:end -->

**Two caveats accompany this arithmetic.** First, **energy**: the supplied effort above must
arrive from storage, the generator or a tender; solar credit is reported separately in the
[energy model](../../docs/ENERGY-MODEL-2026-10.md). The tender fleet is not modelled. Second, **persistence**: CL 4
is 1.63 mm of even-spread water equivalent. The earlier drying range, tens of minutes to a few
hours in fire weather, was an **unsourced estimate for exposed free water on fuel surfaces**,
not a measurement of absorbed fuel moisture or useful treatment lifetime. Water is not
retardant. [Wheatley et al.](https://doi.org/10.1071/WF22218)
did not directly sample litter moisture; their modelled drying of wetted litter is distinct
from the measured change in ambient humidity. How long this pre-treatment stays useful in
named fuels is **unknown**. A corridor stays treated only if each part is revisited within
that useful time, so the length an aircraft can keep treated is at most its treatment line
rate times that time. Flying without stopping is necessary to sustain that continuous line
rate, but is not sufficient: useful wetting, revisit timing and supply must also be established.

## Night as a conditional design point

Typical cooler, moister nights can favour the proposed pre-treatment mission; some nights
do not. [Luo et al.](https://doi.org/10.1038/s41586-024-07028-5) document
overnight burning promoted by drought, so darkness does not ensure quiet fire behaviour.
The [USFS Helicopter Night Operations Study](https://www.fs.usda.gov/sites/default/files/media/2014/17/cr-2013-report-nanfo-ecm7351935.pdf#page=131)
describes night firefighting in Los Angeles County
and San Diego; night airspace cannot be assumed empty.

Night remains a design point under suitable weather and visibility, a release outside
active columns, cleared and deconflicted airspace, and coordination with incident command
and ground crews. Those conditions must be checked for each operation. The model has no
daily weather cycle, vertical air motion or air traffic ([physics limits](../../docs/PHYSICS.md#12-what-the-model-deliberately-does-not-attempt)),
so it has not computed a night advantage.

## What this does not resolve

**AFUE's observed contrast.** In its non-random sample of airtanker retardant drops,
[AFUE](../papers/usfs-2020-afue.pdf) reports probability of success of 0.72 with ground
engagement and 0.56 without. The [denominator](../papers/usfs-2020-afue.pdf) is drops
with **known, interacting outcomes**, and the numerator is effective drops; the
[sampling design](../papers/usfs-2020-afue.pdf) is observational. Ground engagement
concerns crews on the ground, not whether the
aircraft carries a pilot. These values are neither a causal crew effect nor a success
probability for this unbuilt fleet. The recommendation remains to work **for ground crews**,
putting water where crews and corridors need it before they need it. AFUE's metric is
objectives achieved, not tonnes; this project's water arithmetic establishes logistics,
not effectiveness.

**Swath width is assumed.** Nothing models a drop pattern; 20–80 m brackets airtanker practice.
A slow release from leads should be narrower and far more controllable, which would be an
advantage, and nobody has computed it.

## What to verify, and by whom

| question | discipline | what would settle it |
|---|---|---|
| **What pattern does a sprayer lead make?** | fire aviation / drop testing | a cup-grid test under a slow release at 50–150 m, the standard USFS method |
| Can a 300–400 m sprayer lead be flown stably behind a hull? | flight dynamics | towed-body analysis; the intake hose is the precedent |
| What release height should each class use? | operations | a clearance analysis **per class** — 450 m is one number applied to three very different aircraft |
| How long does a water line hold, in what fuels? | fire behaviour | wetting and drying trials; the persistence question above |
| Does pre-treatment work? | fire behaviour / operations research | the mission's own effectiveness question, and the one nobody has asked |

The last of those is now the most important row in the table, because it is the primary mission
and this project has spent all its effort on the extreme case instead.
