# Open questions

Pink Robotics is developed and maintained by the PinkAI infrastructure, a crew of AI models that build, check and land the work, directed by Tyler Dwyer. See the [work log](https://pinkrobotics.ca/log/). The work log names the model behind each change it records, from 1 October 2026; earlier work predates that record.

> **Energy correction, 2026-10-02.** Current force, energy and delivery questions below use generated records.
> The [closure document](ENERGY-CLOSURE-2026-10.md) retains earlier figures beside both current bases.
> Arithmetic corrections do not certify flight. The profile search states its finite limits and prints cycle minutes.
> Superseded energy entries remain in `research/analysis/energy-document-history.json`.


> **2026-10-01: #16 is PARTLY FIXED, and #18 to #20 are new.** The 3D viewer now reads the model's
> constants through a checked boundary, and the rotor count is decided: the model counts stations.
> Three atmosphere implementations disagree in the sixth digit (#18), six failure buttons in the
> model lab change only the drawing (#19), and the engineering page's sentence about scale is not
> what the model says across ship sizes (#20).

> **2026-10-01: #5 is FIXED.** The Esri layer and toggle are removed; the monitor uses
> the bundled first-party hillshade. The dated status notes below are historical.

> **2026-08-10: SIX OF THESE NOW HAVE ANSWERS, and they are in `research/analysis/`.**
>
> This page says what is wrong. `docs/VERIFICATION-PLAN.md` says what would settle it, and
> sorts every question into settled-by-analysis, needs-an-experiment, needs-an-expert or
> needs-data. Read that first if you want to know what to *do*.
>
> | entry | what the analysis found | where |
> |---|---|---|
> | #11 | **The go/no-go is one number nobody had written down: a vacuum shell must mass less than 0.957 kg/m³ of enclosed volume.** Jenett's published 0.508 clears it with 47% margin and the hull is free to grow — 353,975 m³, a 223 m ship. What decides it is the shell density of one *sealed cell* and the *packing fraction*. | `mass-budget.md` |
> | #13 | **Water is not a constraint.** 3,286 BC fires over 20 seasons; all have an adequate source in range; median 4.71 km. The binding unknown is lake *depth*, which the Freshwater Atlas does not carry. | `water-availability.md` |
> | #0, #4 | **The cryogenic plant CANNOT be deleted** — a sealed-cell hull has no way to ballast with air, and an earlier claim that it could is retracted. But the ship makes nitrogen on every cycle it does not need, at **32.5%** of the P-100's cycle energy as the one model prices it since 2026-10-01 (52.5% of the smaller cycle published before). | `air-ballast.md` |
> | #3, #14, #15 | **FIXED 2026-10-01 — one energy model.** The letdown is 0.390 / 4.279 / 35.398 MWh, a fifth of each cycle, against the 0.012 / 0.161 / 1.420 the window constant produced; cycle energy rose 45 / 115 / 224%. The bag's credit to the rotors is 0.7–5.2% of the cycle — not the 96% once claimed, nor the 27–49% this note then argued — and what it buys is water (2,248 t a cycle on the P-10000). | `descent.md`, `../docs/ENERGY-MODEL-2026-10.md` |
> | #8 | **Re-opened, and now measurable.** `diskM2` was retired as inert on a measurement taken against a letdown too small to see it. With the rotors priced over the whole flight, ±20% on the disc moves the P-10000 cycle by +9.6% / −5.8% and `battMW` ±20% moves it −0.1% / +2.3% through the letdown clamp. | `descent.md` |
> | #12 | **`ALT.drop` = 450 m does not deliver water** — and the ship's own rotors push air *upward* at 86× the mass flow of the water. The answer is sprayer leads. Measured in line rather than tonnes, one P-100 could wet the perimeter of 91.4% of BC campaign fires daily. | `delivery.md` |
>
> Regenerate all of it with `make analysis`.
>
> **2026-10-02 correction to #11:** the conditional capsule budget now gives 457,324 m³ and 140 m length. This is equipment-budget closure under an assumed shell density, not a checked design.
> See [the regeneration audit](audit/26-10-02-analysis-regeneration.md).

> **DECIDED 2026-08-09.** All six are to be fixed. The decisions are recorded at the top of
> each entry as **DECISION**, and they change what "correct" means, so read them before
> touching the arithmetic. Three of them interact: making the hull buoyant fully loaded
> (#1) changes the force margins that make retention dead (#4), and removing the generators
> (#6) changes them again in the other direction. Do #1 first, then #6, then re-measure #4
> before deciding it is still dead.
>
> **#0 and #1 are DONE, 2026-08-09.** The hulls are resized, `ledger()` takes an altitude,
> and every published figure that moved is listed in each entry. Two things did not happen
> that this page predicted, and both are recorded below rather than quietly dropped: #4 got
> *further* from binding rather than closer, and the cryogenic plant is no less inert in the
> delivery cycle than it was. #2, #3 and #6 were closed on 2026-10-01 by one change (see each entry); #5 is still open.

Seventeen things are wrong, or unjustified, or dead. They are written up here rather than quietly
fixed because each one changes a number the site publishes or a decision it has to make before
going public, and because several are not really bugs at all — they are decisions about the
vehicle that have been made by accident and should be made on purpose.

**Two are already fixed.** #9 (the solar skin) and #10 (the nitrogen store) were corrected the same
day they were found, because neither had a defensible reading: one required 76% conversion of
sunlight and the other returned more work than the liquid it drew on contained. Both fixes made the
model's numbers worse and its conclusions stronger.

**The list grew from six to seventeen over 2026-08-09 and 08-10, and where the new ones came from matters.**
Items 0–6 were found by the PinkAI infrastructure that wrote the model, looking at it. Items 7 and 8 came from an
adversarial audit of all 89 published claims (`research/evidence-map.md`), which found that the
constants nobody had thought to question moved the headline more than the defects everyone had.
Items 9–12 came from reading the sources — the catalogue in `research/sources.json` was built by
going and checking, and four of the things it checked came back negative. Two of those, #10 and
#11, are the most serious entries on this page: one is thermodynamically impossible and the other
questions whether the vehicle's mass premise is reachable at all.

That is the argument for the exercise. A model that is only reviewed by its authors grows a list
of six. The same model, checked against its own claims and then against the literature, has
thirteen — and it is the same model. Nothing here was introduced by the audit; it was all already
true and unnoticed.

Each entry gives the defect, what it costs, the options, and a recommendation. The numbers
were produced by re-running the model, and by an independent Python replication that
reproduces `tests/golden/seed7-snapshot.json` exactly.

Items 2 and 3 had a test in `tests/cases/` marked `knownFail`. Those tests ran, and failed,
until 2026-10-01, when the one energy model made them pass; the markers were converted into
ordinary tests of the corrected behaviour rather than deleted — `energy · the budget is the
integral of the flight` on every golden combination, and the `defects 3 and 15` suite that
fails if a letdown window ever comes back. <!-- test-status:markers:start -->
The current suites contain 0 known-failing markers. The corrected wind flag is an ordinary assertion; item 17 records its closure.
<!-- test-status:markers:end -->
Item 1 had another. It started passing on 2026-08-09, which is what a fix looks
like from the suite's side, and was converted the same way: `physics · FAIL-SAFE FLOAT-UP` and
`physics · UNPOWERED RECOVERY`.

Items 4, 5 and 6 have no such marker, and cannot have one. `retainedT` being zero is
*enforced* by `selftest.js`, so a test that failed on it would be asserting the opposite of
the specification; the Esri problem is not a model behaviour; and no assertion can fail
because a term is absent from a sum. Those three are held to ordinary passing tests that
record what the code does, and to this page.

`docs/PHYSICS.md` §11 quantifies items 0–6, but numbers them differently: its Defects 4 and 5 are
the two halves of item 4 below, its Defect 6 is item 6, and item 5 has no entry there because it
is not physics. Items 7–12 are documented here only; §11 predates them.

---

## 0. The sizing requirement that ties #1, #4 and #6 together

**DECIDED 2026-08-09.** Added before the individual defects because it constrains three of
them at once, and because it is the requirement that makes ballast a structural part of the
vehicle rather than a doctrine the code ignores.

**Total-failure recovery, unpowered.** Assume the rotors have failed entirely and the
battery is flat. The ship must then:

1. float up — it is buoyant by design (#1), so a dead ship rises rather than falls;
2. recharge on solar alone;
3. liquefy enough nitrogen to make itself heavy enough to descend **with no rotor
   authority at all**; and
4. land empty on ballast alone.

Taking days to do it is acceptable. Being unable to do it is not.

That fourth step is the demanding one, because it sizes the cryogenic plant and the nitrogen
tankage: the LN₂ aboard must be able to exceed the *empty* hull's surplus buoyancy at
altitude. With the hull already grown for fail-safe float-up when full, that is roughly a
payload's worth of nitrogen.

**DONE 2026-08-09.** Built, with one correction to the sizing table below. What was
planned, at ρ = 0.96 kg/m³ (about 2,500 m MSL: 1,500 m over a 1,000 m plateau), a 5%
float-up margin when fully loaded, and the model's own `eLN2` = 0.45 kWh/kg:

| class | hull grows | LN₂ to sink an empty hull | capacity today | tankage | energy | on solar alone | at rated cryo power |
|---|---|---|---|---|---|---|---|
| P-100 | +21.5% | 110 t | 50 t | 136 m³ | 49 MWh | 1.7 days | 0.3 days |
| P-1000 | +21.5% | 1,100 t | 500 t | 1,363 m³ | 495 MWh | 3.7 days | 0.7 days |
| P-10000 | +21.5% | 11,000 t | 5,000 t | 13,631 m³ | 4,950 MWh | 8.6 days | 2.1 days |

**The correction: that ballast column sizes the wrong end of the descent.** 110 t is the
empty hull's surplus buoyancy *at 2,500 m*, which is enough to make a dead ship start
sinking and not enough to land it. The air thickens as it falls. A P-100 carrying 110 t of
nitrogen reaches neutral buoyancy again at about 2,065 m MSL and hangs there for ever. The
binding altitude is the BOTTOM of the descent, where the hull is most buoyant: at
`TERRAIN_MSL` = 1,000 m the air is 1.1116 kg/m³, 16% denser than at the ceiling, and the
empty surplus is 144.6 t per 100 t of payload — 31% more ballast than the table asks for.
Step 4 of the requirement says "land", so the tanks are sized to land.

What was actually built, at ISA density computed honestly rather than rounded, and with the
ballast sized at ground level:

| class | displacement | hull grows | LN₂ to land an empty hull | tank | tankage | energy | on solar alone | at rated cryo power |
|---|---|---|---|---|---|---|---|---|
| P-100 | 180,000 → 220,000 m³ | +22.2% | 144.6 t | 155 t | 192 m³ | 65 MWh | 2.6 days | 0.45 days |
| P-1000 | 1.8 → 2.2 ×10⁶ m³ | +22.2% | 1,445.6 t | 1,550 t | 1,921 m³ | 651 MWh | 5.7 days | 0.90 days |
| P-10000 | 1.8 → 2.2 ×10⁷ m³ | +22.2% | 14,456.1 t | 15,500 t | 19,207 m³ | 6,505 MWh | 12.9 days | 2.7 days |

Lengths and diameters follow: 177 × 44 → **190 × 47 m**, 380 × 95 → **404 × 102 m**,
820 × 205 → **876 × 219 m**, all at fineness 4. The float-up margin is 5.25% and is
identical for all three classes, because dry mass is set equal to payload for all three. No
class needed the rotor-lift exception #1 allows, and none was granted one.

Four things fall out of it.

**The tankage is still free and the energy still is not.** 19,207 m³ of nitrogen is 0.087%
of the P-10000's hull volume — volumetrically irrelevant. The constraint is entirely the
time to liquefy it.

**The plant did not need scaling; the tanks did.** `cryoMW` is unchanged at 6 / 30 / 100 MW.
A P-10000 fills a fail-safe ballast load in 2.7 days at rated power, and "taking days to do
it is acceptable" was the standard. The tanks were the undersized part, by a factor of about
three.

**"A couple of days" is right only at rated plant power.** The plants are sized well above
what the solar skin can feed — 100 MW against 24 MW gross on the P-10000, 21 MW after the
hotel load — so an unpowered ship recovering on solar alone takes about thirteen days, not
three. Both are published. Thirteen is the true unaided worst case and it is the one the
fail-safe claim rests on. It is also optimistic in a way worth stating: the model's solar is
a flat 200 W/m² day and night, so a real recovery is several times longer again.

**This is what battery tenders are for.** Delivering charged cells collapses the recovery
from days to hours and is the same mechanism that sets the normal cycle rate — the tender
fleet is not only a throughput story, it is the rescue story.

Consequences for the entries below, as measured rather than as predicted: #4 did **not**
stop being a question — the surplus that has to be pushed down is now measured in thin air
and got *smaller*, so retention is further from binding than before (see #4). #6's nitrogen
bound is now a real number, because the tank is a requirement rather than a round figure.
#1's hull growth and this tankage were one calculation and are done together.

---

## 1. Lift is bought at sea level and spent at altitude — FIXED 2026-08-09

**DONE 2026-08-09.** `sim/atmosphere.js` is new: the ISA troposphere, constants sourced to
ISO 2533:1975, cross-checked against the published density table at 0 / 1,000 / 2,000 /
2,500 / 3,000 m, and it throws rather than extrapolate outside the layer. `ledger()` takes
an altitude in metres MSL and has **no default**, so the failure mode that caused this
defect — a caller that had not thought about where it was — is now a thrown error instead of
a wrong number. `planCycle` evaluates it once at `WORK_ALT_MSL` = 2,500 m, the thinnest air
of the cycle. `stateAt` evaluates it at `TERRAIN_MSL + alt` at every instant, so lift moves
through the cycle by 14% as the ship climbs, which is the point.

The hulls are resized to satisfy fail-safe float-up: see the table in #0. Every class is
5.25% buoyant fully loaded at 2,500 m, and the loaded break-even moved from 1,005 m MSL —
below the drop run — to 3,000 m MSL, 500 m above the ceiling. Sampling a whole cycle at
seed 7, the minimum net force on the three classes is +10.5 t, +105.1 t and +1,231.1 t: the
sign never reverses, so the page's claim that the rotors only ever push down is now true as
computed rather than true as asserted.

**The terrain the fail-safe claim assumes**, stated because "1,500 m above ground" is a
profile and not a clearance: the interior fire belt burns between valley floors at
300–500 m (Okanagan, Thompson) and treeline at about 2,100 m in the southern interior, with
local summits inside the fuel belt reaching roughly 2,320 m at Big White. A 2,500 m MSL
ceiling clears the fuel everywhere in that envelope and the highest ground in it by about
180 m. Relief (d), flying lower, was available and **not taken**: it buys a smaller hull by
putting the largest aircraft ever proposed under the ridgelines it is working.

**What moved, in two steps.** The resize alone *improved* the P-10000, because honest density
shrank the surplus its rotors fight: `battLimited` went false, the 12% letdown stretch stopped
applying, and the 15 km balanced cycle fell from 50.76 to 49.79 minutes, 11,820 to 12,052 t/h,
82.50 to 75.58 MWh. Cruise drag rose 14% on every class, the running cost of the bigger hull.

That improvement was half an answer, and the second half took it back. Lift answers to the air
the ship is IN, which is the whole point of this defect — and a cycle crosses 1,200 m of it, so
float-up and descent have *different* worst cases. Evaluating the descent at the ceiling with
the rest of the plan was the same mistake one layer up. Struck at the source instead (#4), the
P-10000 delivers 8,944 of 10,000 t at 10,821 t/h for 88.17 MWh and 9.86 kWh/t, back to
"descent authority" as its bottleneck. Both steps are in `docs/PHYSICS.md` §9 and §10.

**What did not move, and should have.** `CFG.rhoAir` is still a flat 1.10 kg/m³ for drag and
every rotor calculation — ISA at about 1,107 m, against a working altitude of 2,500 m. Drag is
therefore overstated by 15% and induced power understated by 7%. That is deliberately left
to #2, whose whole subject is the power model, because fixing it here would have confounded
a ledger change with a power change; it is pinned by a test so it cannot be forgotten. The
page copy in `app/worked.js` called the printed ledger a "sea-level ledger" while printing
the 2,500 m figures under it; it now names the altitude it actually used.

---

*The original write-up follows, in the present tense it was written in and unedited. It is
kept because the decision below is only readable against the options it chose between, and
because a fix that erases the argument for it is a fix nobody can audit.*

`ledger()` in `sim/physics.js` computes displacement lift at `rhoSL` = 1.225 kg/m³. The
ships cruise at `ALT.cruise` = 1500 m above ground, over an interior plateau that is itself
around 1000 m, and every aerodynamic term in the same file already uses `rhoAir` = 1.10.

Structure allowance equals payload for all three classes, so a loaded ship weighs exactly
twice its payload, and break-even air density is **1.1111 kg/m³ for every class** — ISA
density at about 1,005 m. The model's own `rhoAir` is below that. At their working
altitude the classes are **2 t, 20 t and 200 t heavy**, not buoyant.

This matters more than a 1% error, because the sign is load-bearing elsewhere. The page
states, and the 3D model animates, that the hull is buoyant at every point in the cycle and
that the rotors therefore only ever push down. Computed honestly, a full P-10000 is +406 t
over the lake, −860 t on the drop run, and −2,209 t at the ceiling it climbs to: the net
force reverses **inside a single cycle**.

**Options**

| | Effect |
|---|---|
| a. Make `ledger` altitude-aware and accept the consequences | Honest, and cheap to implement — one ISA function and one argument. The ships become heavy at altitude, the "rotors only push down" story inverts, and the energy budget worsens because rotors must now hold weight up during cruise. |
| b. Grow the hull | Displacement +12.4% restores buoyancy at 2,180 m MSL — the ceiling a 15 km P-10000 mission actually reaches over a 1,000 m plateau. (+5.0% would do it at 1,500 m MSL, +16.1% at the nominal 1,500 m AGL.) Every published size grows; the P-10000 goes from 820 m to about 853 m; the vacuum-shell areal density target gets harder, which is already the hardest number in the project. |
| c. Cut the structure allowance | The dry allowance is a bet, not a measurement. Reducing it makes the vehicle buoyant on paper by making the hardest unsolved problem harder. |
| d. Fly lower | Does not work, and the arithmetic says so plainly: loaded break-even is 1,005 m MSL, so over a 1,000 m plateau the hull is buoyant only below about 5 m above ground. At 900 m AGL it is 1,700 t heavy. There is no cruise altitude that rescues this option. |

**DECISION: (a) plus (b), to a stricter requirement than any option above, with (d)
available as relief.**

The requirement is FAIL-SAFE FLOAT-UP: the hull must be positively buoyant at its working
altitude *while fully loaded with water and unable to drop it*. A ship that cannot shed its
payload must still rise, not sink. That is a safety property, not a performance one, and it
sets the displacement.

So: compute density honestly at the altitude actually flown, then size each hull so that
displacement lift exceeds dry mass plus a full payload plus ballast at that altitude, with a
stated margin. Publish the resulting sizes.

Two reliefs are permitted where the fail-safe sizing is unreachable:

  * the P-10000 may rely on continual rotor lift, if the hull that would satisfy fail-safe
    float-up is not credible. If so, say plainly on the page that the largest class is the
    one that does not float when full, and what happens to it if the bus fails;
  * cruise may be lowered. It must still clear terrain: the Okanagan floor is already near
    350 m and the fires that matter are in mountains above that, so the constraint is
    terrain clearance over the fire belt, not a round number of metres above ground. State
    the assumed terrain envelope and check the chosen cruise against it.

**Recommendation, superseded by the decision above: (a) plus (b).** (d) is not available at all. Compute density honestly at
the altitude flown, then size
the hull so it is buoyant there, and publish the larger displacement. Anything else leaves
the site claiming a sign the arithmetic does not support. (a) alone is defensible and
honest but turns the vehicle into something that needs continuous rotor lift, which is a
different machine from the one described.

---

<!-- energy:question-2:start -->
## 2. Which measurements would validate the force owners?

Can an aerospace engineer establish attainable hull downforce and drag across the stated airspeeds? Which rotor thrust rating can replace the unverified hover surrogate?

| Class | Full-bus static hold-down t | Actual balanced stationary supply MW |
|---|---|---|
| P100 | 159.325 | 32.345 |
| P1000 | 785.857 | 156.354 |
| P10000 | 7551.654 | 1412.584 |
<!-- energy:question-2:end -->

<!-- energy:question-3:start -->
## 3. What vertical profile remains feasible with acceleration included?

The search stops at a peak letdown cap of 0.5 m/s. What lower bound would mission conditions justify?

Can added-mass and control measurements close the gap where omitted inertia exceeds simultaneous rotor reserve? Full-delivery profiles below are quasi-static analysis.

| Class | km | Basis | Full-payload mode | Delivered t | Minutes | MWh | kWh/t | Inertia qualification |
|---|---|---|---|---|---|---|---|---|
| P100 | 15 | record | rapid | 100.000 | 176.468 | 42.788 | 427.878 | closes only quasi-statically |
| P100 | 15 | favourable | rapid | 100.000 | 163.432 | 38.497 | 384.967 | closes only quasi-statically |
| P100 | 60 | record | rapid | 100.000 | 75.440 | 14.848 | 148.479 | closes only quasi-statically |
| P100 | 60 | favourable | rapid | 100.000 | 75.440 | 11.263 | 112.630 | closes only quasi-statically |
<!-- energy:question-3:end -->

<!-- energy:question-4:start -->
## 4. How much delivery can be retained while holding the hull?

Can a measured vehicle carry the retained-water requirements below throughout the cycle? What reserve is needed beyond the first closing threshold?

| Class | km | Basis | Profile | Delivered t | Kept t | Minutes | MWh | kWh/delivered tonne |
|---|---|---|---|---|---|---|---|---|
| P100 | 15 | record | as drawn: does not close | 100.000 | 0.000 | 34.196 | 8.192 | 81.923 |
| P100 | 15 | record | cheapest feasible profile found in the stated space | 65.000 | 35.000 | 34.914 | 5.201 | 80.021 |
| P100 | 15 | favourable | as drawn: does not close | 100.000 | 0.000 | 34.196 | 6.402 | 64.017 |
| P100 | 15 | favourable | cheapest feasible profile found in the stated space | 65.000 | 35.000 | 34.914 | 3.793 | 58.359 |
| P100 | 60 | record | as drawn: closes | 100.000 | 0.000 | 104.784 | 20.521 | 205.214 |
| P100 | 60 | record | cheapest feasible profile found in the stated space | 98.382 | 1.618 | 64.420 | 14.100 | 143.315 |
| P100 | 60 | favourable | as drawn: closes | 100.000 | 0.000 | 104.784 | 14.764 | 147.639 |
| P100 | 60 | favourable | cheapest feasible profile found in the stated space | 100.000 | 0.000 | 75.440 | 11.263 | 112.630 |
| P1000 | 15 | record | as drawn: does not close | 1000.000 | 0.000 | 35.362 | 62.314 | 62.314 |
| P1000 | 15 | record | cheapest feasible profile found in the stated space | 215.591 | 784.409 | 25.616 | 26.489 | 122.866 |
| P1000 | 15 | favourable | as drawn: does not close | 1000.000 | 0.000 | 35.362 | 61.355 | 61.355 |
| P1000 | 15 | favourable | cheapest feasible profile found in the stated space | 215.591 | 784.409 | 25.616 | 21.539 | 99.905 |
| P1000 | 60 | record | as drawn: does not close | 1000.000 | 0.000 | 93.116 | 141.533 | 141.533 |
| P1000 | 60 | record | cheapest feasible profile found in the stated space | 270.506 | 729.494 | 74.049 | 68.866 | 254.583 |
| P1000 | 60 | favourable | as drawn: does not close | 1000.000 | 0.000 | 93.116 | 142.484 | 142.484 |
| P1000 | 60 | favourable | cheapest feasible profile found in the stated space | 270.506 | 729.494 | 74.049 | 56.659 | 209.457 |
| P10000 | 15 | record | as drawn: does not close | 10000.000 | 0.000 | 45.512 | 694.378 | 69.438 |
| P10000 | 15 | record | cheapest feasible profile found in the stated space | 2626.200 | 7373.800 | 23.667 | 200.116 | 76.200 |
| P10000 | 15 | favourable | as drawn: does not close | 10000.000 | 0.000 | 45.512 | 766.285 | 76.629 |
| P10000 | 15 | favourable | cheapest feasible profile found in the stated space | 2626.200 | 7373.800 | 23.667 | 183.419 | 69.842 |
| P10000 | 60 | record | as drawn: does not close | 10000.000 | 0.000 | 94.381 | 1113.855 | 111.385 |
| P10000 | 60 | record | cheapest feasible profile found in the stated space | 3009.297 | 6990.703 | 66.573 | 439.851 | 146.164 |
| P10000 | 60 | favourable | as drawn: does not close | 10000.000 | 0.000 | 94.381 | 1386.308 | 138.631 |
| P10000 | 60 | favourable | cheapest feasible profile found in the stated space | 3009.297 | 6990.703 | 66.573 | 397.762 | 132.178 |
<!-- energy:question-4:end -->

## 5. Esri basemap tiles — FIXED 2026-10-01

Removed the Esri tile loader and satellite toggle. The bundled first-party terrain hillshade
is now the default backdrop, with outlined labels and markers and stronger water/perimeter
contrast. No Esri tiles are fetched or redistributed. See `DATA-SOURCES.md` §6.

The browser network gate (`tests/firstparty/check.py`, part of `make check`) records requests
for every served page in fixture-live, snapshot and absent-mirror modes and refuses external
hosts. The static gate checks loading positions separately. The server mirrors wind hourly;
missing agency mirrors fall back only to the dated files in this repository.

---

<!-- energy:question-6:start -->
## 6. What power can nitrogen recovery actually supply?

Can the nitrogen expander supply the modelled phase output after its mass, heat exchangers and losses are counted? Which transient bus limits would reduce this supply?

| Class | Mode | Stationary supply MW | Other load MW | Available hold-down t |
|---|---|---|---|---|
| P100 | rapid | 31.301 | 2.122 | 133.601 |
| P100 | balanced | 32.345 | 2.122 | 136.769 |
| P100 | endurance | 33.976 | 2.122 | 141.645 |
| P1000 | rapid | 153.791 | 12.572 | 644.818 |
| P1000 | balanced | 156.354 | 12.572 | 652.596 |
| P1000 | endurance | 160.356 | 12.572 | 664.651 |
| P10000 | rapid | 1408.970 | 61.860 | 6877.378 |
| P10000 | balanced | 1412.584 | 61.860 | 6889.674 |
| P10000 | endurance | 1418.228 | 61.860 | 6908.854 |
<!-- energy:question-6:end -->

## 7. Thirty-two unjustified constants, and only fifteen of them are dialled

An audit of every published figure (`research/evidence-map.md`, 89 claims) put 32 of them on
constants with no stated justification anywhere — against 15 genuine stated assumptions. **The
expected result was the opposite.** `sim/config.js` does what it advertises: every number in it is
visible, dialled and captioned. The problem is everything that is NOT in it — coefficients written
inline in `plan.js` and `state.js`, never surfaced, never argued for, and in several cases moving
the published output by more than the defect this project has spent a week naming.

The three that matter most, measured:

| constant | where | what it does | moving it |
|---|---|---|---|
| `0.55` and `0.4` drag multipliers | `plan.js` E.RETURN_TRANSIT, E.other | charge the return leg and the manoeuvring phases a fraction of cruise drag | charging full drag everywhere: **45.87 → 62.74 MWh, +37%** |
| anchor bag at 90% of the hold | `config.js` anchorBagT | how much of the descent the lake does | the minimum bag that still delivers the full payload is 1,099 t against the shipped 12,400 t; between them the cycle runs **91.47 → 45.87 MWh** with throughput unchanged |
| `fillM3s` 0.5 / 3 / 15 m³/s | `config.js` | sets the fill AND, since the single-pass drop, the release — 22.2 of 45.5 cycle minutes | halved: cycle **45.5 → 67.7 min**, delivery −33%, bottleneck flips to water handling |

For comparison, defect 3 — the unexplained letdown window this project has flagged in its README
since the first commit — is worth 1.42 MWh. The two drag multipliers are worth 16.87.

**DECISION: none yet.** This is the entry that says the audit found something the project's own
self-assessment did not. Each of these needs the same treatment the six original defects got:
a stated reason, or a derivation, or an admission that it is a guess — and `research/evidence-map.md`
is the list to work through.

---

<!-- energy:question-8:start -->
## 8. What rotor area, thrust and storage mass can be built?

What evidence supports the installed disk area, downward-only thrust and battery rating together? Can any required storage mass fit inside the dry-mass target?

## What the model would require

Generated by `node research/analysis/energy-tables.mjs`. Each printed closing value is rounded up to three decimals and replayed at the verdict resolution.

| Class | km | Basis | As drawn | Minutes: drawn / kept / power pair | Water kept, t | Delivered, t | kWh/t | Required battery, MW | Rotor thrust, t | Battery mass, t (500 / 300 / 149 Wh/kg) |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|
| P100 | 15 | record | does not close | 34.196 / none / none | none | none | none | none | none | none |
| P100 | 15 | favourable | does not close | 34.196 / none / none | none | none | none | none | none | none |
| P100 | 60 | record | closes | 104.784 / 104.784 / 104.784 | 0.000 | 100.000 | 205.214 | 29.787 | 132.345 | 39.716 / 66.193 / 133.275 (exceeds dry target) |
| P100 | 60 | favourable | closes | 104.784 / 104.784 / 104.784 | 0.000 | 100.000 | 147.639 | 28.595 | 132.345 | 38.127 / 63.544 / 127.942 (exceeds dry target) |
| P1000 | 15 | record | does not close | 35.362 / 28.290 / 35.362 | 818.465 | 181.535 | 133.729 | 529.178 | 1390.813 | 846.685 / 1411.141 (exceeds dry target) / 2841.224 (exceeds dry target) |
| P1000 | 15 | favourable | does not close | 35.362 / 28.290 / 35.362 | 818.465 | 181.535 | 105.087 | 529.178 | 1390.813 | 846.685 / 1411.141 (exceeds dry target) / 2841.224 (exceeds dry target) |
| P1000 | 60 | record | does not close | 93.116 / 86.322 / 93.116 | 768.406 | 231.594 | 281.017 | 507.427 | 1373.163 | 811.883 / 1353.139 (exceeds dry target) / 2724.440 (exceeds dry target) |
| P1000 | 60 | favourable | does not close | 93.116 / 86.322 / 93.116 | 768.406 | 231.594 | 221.296 | 507.427 | 1373.163 | 811.883 / 1353.139 (exceeds dry target) / 2724.440 (exceeds dry target) |
| P10000 | 15 | record | does not close | 45.512 / 31.669 / 45.512 | 7073.814 | 2926.186 | 88.166 | 4213.645 | 13092.990 | 12038.986 (exceeds dry target) / 20064.976 (exceeds dry target) / 40399.281 (exceeds dry target) |
| P10000 | 15 | favourable | does not close | 45.512 / 31.669 / 45.512 | 7073.814 | 2926.186 | 79.113 | 4213.645 | 13092.990 | 12038.986 (exceeds dry target) / 20064.976 (exceeds dry target) / 40399.281 (exceeds dry target) |
| P10000 | 60 | record | does not close | 94.381 / 80.664 / 94.381 | 6960.518 | 3039.482 | 160.619 | 4169.829 | 13092.989 | 11913.797 (exceeds dry target) / 19856.329 (exceeds dry target) / 39979.185 (exceeds dry target) |
| P10000 | 60 | favourable | does not close | 94.381 / 80.664 / 94.381 | 6960.518 | 3039.482 | 141.825 | 4169.829 | 13092.989 | 11913.797 (exceeds dry target) / 19856.329 (exceeds dry target) / 39979.185 (exceeds dry target) |

Cycle minutes are printed separately for the prescribed profile, retained-water requirement and power-and-thrust requirement.

The battery masses retain each class's energy-to-peak-power ratio. Power alone does not fix storage mass. These are requirements, never equipment options.

Specific energies and their source qualifications bind to `research/analysis/mass-budget.json`. Values that exceed the entire dry-mass target are marked.

The bag counts when the cable carries water; the hoist remains priced. Delaying force credit until hoisting finishes changes the retained-water requirement as follows.

| Class | km | Basis | Extra water kept under stricter rule, t |
|---|---:|---|---:|
| P100 | 15 | record | none |
| P100 | 15 | favourable | none |
| P100 | 60 | record | 0.000 |
| P100 | 60 | favourable | 0.000 |
| P1000 | 15 | record | 53.381 |
| P1000 | 15 | favourable | 53.381 |
| P1000 | 60 | record | 52.110 |
| P1000 | 60 | favourable | 52.110 |
| P10000 | 15 | record | 398.182 |
| P10000 | 15 | favourable | 398.182 |
| P10000 | 60 | record | 396.642 |
| P10000 | 60 | favourable | 396.642 |

## Broadside-drag range

Each entry gives the signed worst unheld force in tonnes and the feasibility verdict. Negative force needs upward authority, which is unavailable.

| Class | km | Basis | Coefficient 0 | Coefficient 1 | Coefficient 2 |
|---|---:|---|---|---|---|
| P100 | 15 | record | 13.069; does not close | 34.556; does not close | 56.476; does not close |
| P100 | 15 | favourable | 1.146; does not close | -5.714; does not close | -32.818; does not close |
| P100 | 60 | record | 0.000; closes | 0.000; closes | -0.000; closes |
| P100 | 60 | favourable | 0.000; closes | 0.000; closes | -0.000; closes |
| P1000 | 15 | record | 740.143; does not close | 818.465; does not close | 898.012; does not close |
| P1000 | 15 | favourable | 740.143; does not close | 818.465; does not close | 898.012; does not close |
| P1000 | 60 | record | 690.084; does not close | 768.406; does not close | 847.903; does not close |
| P1000 | 60 | favourable | 690.084; does not close | 768.406; does not close | 847.903; does not close |
| P10000 | 15 | record | 6814.274; does not close | 7073.819; does not close | 7333.364; does not close |
| P10000 | 15 | favourable | 6814.274; does not close | 7073.819; does not close | 7333.364; does not close |
| P10000 | 60 | record | 6700.978; does not close | 6960.523; does not close | 7220.068; does not close |
| P10000 | 60 | favourable | 6700.978; does not close | 6960.523; does not close | 7220.068; does not close |

## Rotor-efficiency range

Rotor figure of merit times drive efficiency. Hold-down descent is priced as climb, on the conservative side; climb against hold-down thrust is priced as level flight, with no bound claimed.

| Class | km | Basis | Efficiency | Static thrust cap over local densities, t | Worst unheld force, t | Verdict |
|---|---:|---|---:|---|---:|---|
| P100 | 15 | record | 0.55 | 130.327 to 135.663 | 47.519 | does not close |
| P100 | 15 | record | 0.7 | 153.059 to 159.325 | 34.556 | does not close |
| P100 | 15 | favourable | 0.55 | 130.327 to 135.663 | 47.519 | does not close |
| P100 | 15 | favourable | 0.7 | 153.059 to 159.325 | -5.714 | does not close |
| P100 | 60 | record | 0.55 | 130.327 to 135.663 | 17.577 | does not close |
| P100 | 60 | record | 0.7 | 153.059 to 159.325 | 0.000 | closes |
| P100 | 60 | favourable | 0.55 | 130.327 to 135.663 | 15.835 | does not close |
| P100 | 60 | favourable | 0.7 | 153.059 to 159.325 | 0.000 | closes |
| P1000 | 15 | record | 0.55 | 646.328 to 669.145 | 910.770 | does not close |
| P1000 | 15 | record | 0.7 | 759.061 to 785.857 | 818.465 | does not close |
| P1000 | 15 | favourable | 0.55 | 646.328 to 669.145 | 910.770 | does not close |
| P1000 | 15 | favourable | 0.7 | 759.061 to 785.857 | 818.465 | does not close |
| P1000 | 60 | record | 0.55 | 642.828 to 669.145 | 865.724 | does not close |
| P1000 | 60 | record | 0.7 | 754.950 to 785.857 | 768.406 | does not close |
| P1000 | 60 | favourable | 0.55 | 642.828 to 669.145 | 865.724 | does not close |
| P1000 | 60 | favourable | 0.7 | 754.950 to 785.857 | 768.406 | does not close |
| P10000 | 15 | record | 0.55 | 6238.062 to 6430.112 | 8028.158 | does not close |
| P10000 | 15 | record | 0.7 | 7326.107 to 7551.654 | 7073.819 | does not close |
| P10000 | 15 | favourable | 0.55 | 6238.062 to 6430.112 | 8028.158 | does not close |
| P10000 | 15 | favourable | 0.7 | 7326.107 to 7551.654 | 7073.819 | does not close |
| P10000 | 60 | record | 0.55 | 6177.222 to 6430.112 | 7924.536 | does not close |
| P10000 | 60 | record | 0.7 | 7254.655 to 7551.654 | 6960.523 | does not close |
| P10000 | 60 | favourable | 0.55 | 6177.222 to 6430.112 | 7924.536 | does not close |
| P10000 | 60 | favourable | 0.7 | 7254.655 to 7551.654 | 6960.523 | does not close |
<!-- energy:question-8:end -->

<!-- energy:question-9:start -->
## 9. How long can recovery take through a real day and night?

The model uses 45 W/m² as a day average. What storage and charging losses apply when instantaneous sunlight is zero?

| Class | Day-average solar MW | Ground-surplus solar days | Full-tank solar days |
|---|---|---|---|
| P100 | 0.270 | 24.641 | 26.420 |
| P1000 | 1.260 | 58.924 | 63.179 |
| P10000 | 5.400 | 112.939 | 121.094 |
<!-- energy:question-9:end -->

<!-- energy:question-10:start -->
## 10. What nitrogen recovery fraction is demonstrable?

Liquefaction costs 0.45 MWh/t and recovery returns 0.2 of that investment. Can a complete airborne system reproduce that fraction without an external heat source?

Which plant and tank masses belong in the dry ledger, and what duty cycle can they sustain?
<!-- energy:question-10:end -->

## 11. The dry-mass budget fails twice, against two independent sources

`dryT = payloadT` is the assumption the whole ledger stands on: 10,000 t of everything-that-is-not-
water inside 22 million m³, or **0.455 kg/m³** of hull-average density. Two sources contradict it
independently, and neither was cited when the assumption was made:

- **Jenett et al. 2019** (NASA NTRS, in `research/papers/`) — the discrete cellular lattice this
  project cites as its structural precedent — gives a bare shell of **0.508 kg/m³** in its own
  Table 2, at every radius. That is 12% over our *entire* dry allowance before skin, joints,
  rotors, tanks, batteries or the 125 t of anchor cable this model also does not charge.
- **Metlen & Palazotto 2013**'s only real-materials vacuum-lift design has a
  structure-to-buoyancy ratio of **0.94** — structure alone consuming what we allocate to
  structure *and* payload.
- Separately: every class carries **0.2 MWh of battery per tonne of dry mass**, which demands
  200 Wh/kg at pack level with nothing left over for anything else. NASA flew 149 Wh/kg on X-57.

**DECISION: none yet**, and this is the largest open question in the project — larger than any of
#1–#8, because those are errors inside a model and this is a question about whether the model's
premise is reachable. It is stated here rather than resolved because resolving it honestly means
either a mass breakdown this project has not done, or saying plainly that the vehicle is
conditional on a structural technology that has been demonstrated at the scale of a metre.

---

## 12. The drop may not reach the ground, and tonnes may be the wrong metric

Two findings from the wildfire-aviation literature, both aimed at the top of the funnel:

- The **US Forest Service's 2022 assessment** states that a drop released 1,000 ft above
  ground/vegetation level "would completely dissipate". `ALT.drop` is **450 m — 1,476 ft**, three
  to five times a very large airtanker's release height. The model has no droplet physics at all;
  it moves tonnes from a tank to a coordinate. The altitude was raised for hull-clearance reasons
  that are sound, and the delivery consequence was never costed.
- **AFUE** (Aerial Firefighting Use and Effectiveness, 27,611 observed drops) reports probability
  of success **0.56 without ground engagement against 0.72 with it**, the modal outcome without
  ground crews being *not effective*. AFUE never counts tonnes. This project's headline metric is
  tonnes per hour.

**DECISION: none yet.** Neither is a modelling error — the model is honest about being a delivery
simulator — but both bear on whether delivered tonnage is the right thing to have optimised, and a
reader from the fire community will raise them in the first five minutes. They belong on the list.

---

## 13. Nobody has asked how often the mission exists

The whole concept is a duty cycle between a fire and a lake. `sim/plan.js` takes the one-way
distance as an input and `sim/water.js` picks the nearest adequate source, but **no figure anywhere
in this project says what fraction of real fires have an adequate source within range.**

Adequate means more than nearby. A P-10000 draws 10,000 t a cycle at
13,183 t/h and hovers over the surface while it does it, so the body has to be large enough and
deep enough to stand repeated full-payload draws, and open enough to hold station over. A pond at
4 km is not a source.

This matters more than most entries on this list because it bounds the market rather than the
vehicle. If the answer is "most fires in the interior", the concept has a customer. If it is "a
quarter of them", the fleet is a niche tool and the P-100 is the interesting class rather than the
P-10000.

**DECISION: none yet, and this one is cheap.** The data is already mirrored in `data/`: BC fire
perimeters and a water extract. Joining them is an afternoon. It has not been done because the
project has been auditing its physics, which is a reasonable order of work and not an excuse for
leaving the question unasked.


---

<!-- energy:question-14:start -->
## 14. Can the bag be picked up and released at this scale?

What cable, winch and control measurements would bound pickup shock and pendulum motion? How much station-keeping power is missing under a beam wind?

## What this model leaves out

Generated by `node research/analysis/energy-omissions.mjs`. These loads are not silently absorbed into a closing claim.

| Class | Beam-wind side force, t | Cable mass, t (floor / credible / demonstrated) | Battery mass, t (same cases) | Dry target, t | Bag, t | Cable, m | Pendulum period, s | Day-average solar, MW |
|---|---:|---|---|---:|---:|---:|---:|---:|
| P100 | 29.709 | 0.644 / 1.431 / 2.146 | 40.000 / 66.667 / 134.228 | 100 | 125 | 350 | 37.530 | 0.270 |
| P1000 | 139.077 | 11.036 / 24.525 / 36.788 | 240.000 / 400.000 / 805.369 | 1000 | 1250 | 600 | 49.138 | 1.260 |
| P10000 | 643.635 | 155.096 / 344.658 / 516.987 | 4000.000 / 6666.667 / 13422.819 | 10000 | 12400 | 850 | 58.486 | 5.400 |

| Class | Design displacement, m³ | Geometric capsule, m³ | Difference from design, % |
|---|---:|---:|---:|
| P100 | 220000.000 | 217784.366 | -1.007 |
| P1000 | 2200000.000 | 2205867.973 | 0.267 |
| P10000 | 22000000.000 | 21961324.389 | -0.176 |

Buoyancy uses the declared design displacement. The capsule comparison is a geometry difference, not a change to lift or the class constants.

The beam wind is 10 m/s, with an unverified side-drag coefficient of 1 and local source density. No horizontal actuator or station-keeping power is priced.

Cable and battery estimates bind to `research/analysis/mass-budget.json`. Cable mass is not added to the energy model's dry target.

Storage cases use 500, 300, 149 Wh/kg, respectively. Their source qualifications remain in the mass-budget record.

The bag is a moving pendulum; its ideal small-angle period is shown, but swing, damping and winch transients are unpriced. The steady hoist bill does not bound pickup shock.

Solar is credited at its day average at every instant, including night. Dry mass is a target equal to payload, not an assembled mass ledger; see [the float analysis](../float/).
<!-- energy:question-14:end -->

<!-- energy:question-15:start -->
## 15. Which empty-hull strategy survives its failure case?

The payload-exchange study is analysis, not design. What measurable advantage justifies giving up fail-safe float-up for a half-load hull with two-way rotors?

How would an approach at airspeed transfer load to the bag? How would variable displacement work with sealed cells? Can cryogenic ballast be produced within the available time and dry mass?

The current unheld phases and their signed force provide the requirement that each analysis must address.

## Where the prescribed hull is unheld

Generated by `node research/analysis/energy-unheld.mjs`. Largest absolute signed unheld force in each failing phase, using the verdict mesh, refined extrema and both sides of seams from cycleLimits. Positive is unsupported surplus lift; negative requires unavailable upward authority.

| Class | km | Basis | Profile | Phase | Signed unheld, t | Progress | Cycle minute | Airspeed, m/s | Vertical speed, m/s | Limits |
|---|---:|---|---|---|---:|---:|---:|---:|---:|---|
| P100 | 15 | record | as drawn | SOURCE_APPROACH | 2.690 | 0.686344 | 1.373 | 0.000 | -2.296 | bus power, anchor cable reach |
| P100 | 15 | record | as drawn | OUTBOUND_TRANSIT | -5.714 | 0.222832 | 7.955 | 25.000 | 9.745 | upward authority unavailable |
| P100 | 15 | record | as drawn | RETURN_TRANSIT | 34.556 | 0.810707 | 31.969 | 25.000 | -8.821 | bus power |
| P100 | 15 | favourable | as drawn | SOURCE_APPROACH | 2.690 | 0.686344 | 1.373 | 0.000 | -2.296 | bus power, aerodynamic coefficient, anchor cable reach |
| P100 | 15 | favourable | as drawn | OUTBOUND_TRANSIT | -5.714 | 0.222832 | 7.955 | 25.000 | 9.745 | upward authority unavailable |
| P100 | 60 | record | as drawn | no unheld phase | 0 | | | | | |
| P100 | 60 | favourable | as drawn | no unheld phase | 0 | | | | | |
| P1000 | 15 | record | as drawn | SOURCE_APPROACH | 818.465 | 0.713996 | 2.142 | 0.000 | -7.594 | bus power, rotor thrust, anchor cable reach |
| P1000 | 15 | record | as drawn | WATER_FILL | 418.096 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach |
| P1000 | 15 | record | as drawn | WATER_RELEASE | 642.848 | 1.000000 | 23.737 | 0.000 | 0.052 | bus power, rotor thrust |
| P1000 | 15 | record | as drawn | BUOYANCY_ESCAPE | 642.851 | 0.000000 | 23.737 | 0.000 | 0.011 | bus power, rotor thrust |
| P1000 | 15 | record | as drawn | RETURN_TRANSIT | 587.811 | 1.000000 | 35.362 | 9.167 | -0.000 | bus power, rotor thrust |
| P1000 | 15 | favourable | as drawn | SOURCE_APPROACH | 818.465 | 0.713996 | 2.142 | 0.000 | -7.594 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |
| P1000 | 15 | favourable | as drawn | WATER_FILL | 418.096 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |
| P1000 | 15 | favourable | as drawn | WATER_RELEASE | 642.848 | 1.000000 | 23.737 | 0.000 | 0.052 | bus power, rotor thrust, aerodynamic coefficient |
| P1000 | 15 | favourable | as drawn | BUOYANCY_ESCAPE | 642.851 | 0.000000 | 23.737 | 0.000 | 0.011 | bus power, rotor thrust, aerodynamic coefficient |
| P1000 | 15 | favourable | as drawn | RETURN_TRANSIT | 503.207 | 1.000000 | 35.362 | 9.167 | -0.000 | bus power, rotor thrust, aerodynamic coefficient |
| P1000 | 60 | record | as drawn | SOURCE_APPROACH | 768.406 | 0.713996 | 2.142 | 0.000 | -7.594 | bus power, rotor thrust, anchor cable reach |
| P1000 | 60 | record | as drawn | WATER_FILL | 361.633 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach |
| P1000 | 60 | record | as drawn | WATER_RELEASE | 642.848 | 1.000000 | 52.614 | 0.000 | 0.052 | bus power, rotor thrust |
| P1000 | 60 | record | as drawn | BUOYANCY_ESCAPE | 642.851 | 0.000000 | 52.614 | 0.000 | 0.014 | bus power, rotor thrust |
| P1000 | 60 | record | as drawn | RETURN_TRANSIT | 565.351 | 1.000000 | 93.116 | 9.167 | -0.000 | bus power, rotor thrust |
| P1000 | 60 | favourable | as drawn | SOURCE_APPROACH | 768.406 | 0.713996 | 2.142 | 0.000 | -7.594 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |
| P1000 | 60 | favourable | as drawn | WATER_FILL | 361.633 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |
| P1000 | 60 | favourable | as drawn | WATER_RELEASE | 642.848 | 1.000000 | 52.614 | 0.000 | 0.052 | bus power, rotor thrust, aerodynamic coefficient |
| P1000 | 60 | favourable | as drawn | BUOYANCY_ESCAPE | 642.851 | 0.000000 | 52.614 | 0.000 | 0.014 | bus power, rotor thrust, aerodynamic coefficient |
| P1000 | 60 | favourable | as drawn | RETURN_TRANSIT | 480.748 | 1.000000 | 93.116 | 9.167 | -0.000 | bus power, rotor thrust, aerodynamic coefficient |
| P10000 | 15 | record | as drawn | SOURCE_APPROACH | 7073.819 | 0.666936 | 3.335 | 0.000 | -6.485 | bus power, rotor thrust, anchor cable reach |
| P10000 | 15 | record | as drawn | WATER_FILL | 3843.580 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach |
| P10000 | 15 | record | as drawn | WATER_RELEASE | 6093.823 | 1.000000 | 35.367 | 0.000 | 0.026 | bus power, rotor thrust |
| P10000 | 15 | record | as drawn | BUOYANCY_ESCAPE | 6093.827 | 0.000000 | 35.367 | 0.000 | 0.008 | bus power, rotor thrust |
| P10000 | 15 | record | as drawn | RETURN_TRANSIT | 4994.044 | 0.000000 | 37.367 | 30.694 | 0.000 | rotor thrust |
| P10000 | 15 | favourable | as drawn | SOURCE_APPROACH | 7073.819 | 0.666936 | 3.335 | 0.000 | -6.485 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |
| P10000 | 15 | favourable | as drawn | WATER_FILL | 3843.580 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |
| P10000 | 15 | favourable | as drawn | WATER_RELEASE | 6093.823 | 1.000000 | 35.367 | 0.000 | 0.026 | bus power, rotor thrust, aerodynamic coefficient |
| P10000 | 15 | favourable | as drawn | BUOYANCY_ESCAPE | 6093.827 | 0.000000 | 35.367 | 0.000 | 0.008 | bus power, rotor thrust, aerodynamic coefficient |
| P10000 | 15 | favourable | as drawn | RETURN_TRANSIT | 3956.719 | 1.000000 | 45.512 | 10.833 | 0.000 | bus power, rotor thrust, aerodynamic coefficient |
| P10000 | 60 | record | as drawn | SOURCE_APPROACH | 6960.523 | 0.666936 | 3.335 | 0.000 | -6.485 | bus power, rotor thrust, anchor cable reach |
| P10000 | 60 | record | as drawn | WATER_FILL | 3739.448 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach |
| P10000 | 60 | record | as drawn | WATER_RELEASE | 6093.823 | 1.000000 | 59.801 | 0.000 | 0.026 | bus power, rotor thrust |
| P10000 | 60 | record | as drawn | BUOYANCY_ESCAPE | 6093.827 | 0.000000 | 59.801 | 0.000 | 0.014 | bus power, rotor thrust |
| P10000 | 60 | record | as drawn | RETURN_TRANSIT | 4518.750 | 0.000000 | 61.801 | 30.694 | 0.000 | rotor thrust |
| P10000 | 60 | favourable | as drawn | SOURCE_APPROACH | 6960.523 | 0.666936 | 3.335 | 0.000 | -6.485 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |
| P10000 | 60 | favourable | as drawn | WATER_FILL | 3739.448 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |
| P10000 | 60 | favourable | as drawn | WATER_RELEASE | 6093.823 | 1.000000 | 59.801 | 0.000 | 0.026 | bus power, rotor thrust, aerodynamic coefficient |
| P10000 | 60 | favourable | as drawn | BUOYANCY_ESCAPE | 6093.827 | 0.000000 | 59.801 | 0.000 | 0.014 | bus power, rotor thrust, aerodynamic coefficient |
| P10000 | 60 | favourable | as drawn | RETURN_TRANSIT | 3893.371 | 1.000000 | 94.381 | 10.833 | -0.000 | bus power, rotor thrust, aerodynamic coefficient |

The cheapest feasible profiles found in the stated space, including their minutes and delivery, are in [the profile table](../research/analysis/energy-profiles.md).
<!-- energy:question-15:end -->

## 16. Nine constants cross the sim/3d boundary unchecked, and two are already wrong — PARTLY FIXED 2026-10-01

**PARTLY FIXED — 2026-10-01.** The model remains authoritative. The import rule in
`tools/check_boundaries.py` keeps `3d/` standalone, so its model constants live in
`3d/model/config.js` as declared, checked copies; the animation and physics import that file.
`spec-parity.cases.js` now enumerates numeric keys on **both** sides, including numeric tables,
and requires a partner or a one-sentence exemption for each. It also compares evaluated drag,
pump power, cruise, hose timing, release altitude and working-density lift. Missing required
class fields throw, and the node suite rejects numeric defaults on spec reads throughout `3d/`.

**What changed.** Drop altitude was 250 m against the model's 450 m; it now starts at 450 m
and finishes at 580 m, where escape begins. Missing cruise speeds made every standalone class
fly at 90 km/h; they are now 90 / 110 / 130. Missing hose timings made every class deploy/retract
in 4 / 3 minutes; they are now 4 / 3, 6 / 5 and 10 / 8. Fill rates and every mode-table entry
are checked, and standalone airspeed now applies the selected mode multiplier as its timeline
already did. The rotor helpers also read the shared air density instead of literal 1.10.
Source altitude, pump head, hose geometry, camera framing and pump-pod metadata
now read each class's 300 m hose, removing the remaining 250 m defaults. Liquid densities have
one declaration inside `3d/`. Working density is derived from checked ISA inputs rather than
rounded to 0.95686, and the resolved class lift ledger uses that density too.

The identical `Cd` used to multiply frontal area in the model and volume to the two-thirds
power in the viewer. Both now use the published nominal frontal area. **The original audit's
2.08× claim is not reproduced on this tree:** executing both formulas gives **1.533910× /
1.520891× / 1.525382×** for P-100 / P-1000 / P-10000, at equal speed and density. Those ratios
are now 1. `make mutationcheck` runs `tests/parity/mutations.mjs` using the stamp in
`sim/version.json`. It mutates declarations, missing partners, tables, formulas, defaults and
required field validation, requires each mutation to fail with its expected diagnostic, then
restores the files and checks the parity and required-spec suites again. It prints the caught
mutation count and exits nonzero if any mutation escapes.

**Decided 2026-10-01 — the model counts stations.** The model declares 4 / 6 / 14 rotors; the
viewer draws that many stations with two rotors each, or 8 / 12 / 28. The drawing's aggregate disc
areas remain 2,513 / 12,215 / 158,886 m² against the model's 2,500 / 12,000 / 160,000 m², within
the existing 10% illustration allowance, and the model's power reads the disc area, never the
count. The two do not disagree on physics: the model's count means vectoring stations, each drawn
as a pair. No mesh is halved and no rotor resized; the exemption and the station and pair counts
stay tested. **Still open:** public copy that prints the count still says rotors. It is to say
rotor stations, two rotors each, and that wording lands with the README.

The standalone eleven-phase cycle and its illustrative power shares still differ from the
host's six-phase mission; sharing constants does not make those two simulations identical.
Host-supplied mission state continues to take precedence. Raising the release does not deploy
or lengthen a hose or anchor: both are stowed at 250 and 450 m in the driver checks. The drawn
spray remains a short hull-relative curtain (30.4 / 65.4 / 140.9 m), without a ground plane
or a simulation of water reaching the ground; it has not been stretched to disguise the height.

---

## 17. `windUsed` requires a route bearing

**Closed 2026-10-03.** The returned flag now uses the same speed-and-bearing condition as the wind calculation in `sim/plan.js`.
A wind without a bearing leaves both ground speeds unchanged and reports `windUsed: false`.
The ordinary case in `tests/cases/sim-plan.cases.js` checks null and missing bearings, plus the valid zero-degree bearing.

The earlier reproduction used P-1000, balanced mode, 40 km and `{ spd: 40, dir: 270, bearing: null }`.
Both ground speeds were 110 km/h, but the flag claimed wind use.
The test failed on that implementation and passes after the flag correction.

---

## 18. Three atmosphere implementations that do not agree to the last digit

**Reproduced 2026-10-01. Open.** Run `make labelledcheck` and read the density rows at 1,000 m in
`research/validation/report.md`. `sim/atmosphere.js` returns 1.111642738880746 kg/m³;
`research/analysis/vacuum-cell.py` and `research/analysis/helium.py` both return
1.111652281952491 kg/m³; Table I of the 1976 standard prints 1.1116. With the tolerance written
before the first run (0.00005 kg/m³) the browser model agrees, and the two Python copies MISS by
about 0.0000023 kg/m³ beyond it.

The cause is the gas constant for dry air: `sim/atmosphere.js` uses 287.0528 J/(kg·K) and the two
Python files use 287.05. All three also treat their argument as geopotential height, although the
JavaScript interface describes it as height above mean sea level: at a geometric 2,500 m the
standard's temperature is 271.906 K against the functions' 271.900 K.

It stays a MISS. The constant feeds the cell parity mirror and the generated analysis figures, so
it is not changed quietly. Decide the altitude contract and the constant together, publish what
moves, old and new, then move the row.

---

## 19. Six of the model lab's failure buttons change only the drawing

**Reproduced 2026-10-01. Open.** The model lab offers a failure button for each of up to six rotor
stations, then for an HVDC bus, a generator, a pump pod, a vacuum cell, a sensor cluster and a tail
surface. Failing a rotor makes the allocator re-solve the wrench, and the page says so. The other
six reach no physics module: the drawing code reads them (`3d/anim/driver.js`) and nothing else
does. With any of them failed, the allocation is identical to the allocation with nothing failed.

The page does not claim otherwise, and it does not say so either. Wire each to the model, or label
the six as drawing-only where the buttons are.

---

## 20. "Scale is the lever" is not what the model says across ship sizes

**Reproduced 2026-10-01. Open: what does scale buy, and where does it stop?**
The bench article carries 15.1 kg of structure per cubic metre enclosed.
The 52 m hull carries 2.190 on the record basis and 1.245 on the favourable basis; neither is a floating design.
The [float ledger](FLOAT-LEDGER.md) separates those objects and their load cases.

The hull comparisons use safety factor 1.2 against full sea-level pressure.
The record basis assumes knockdown 0.30 and 1,050 MPa chords.
The favourable basis assumes knockdown 0.65 and a 1,450 MPa carbon-laminate compressive ceiling, both unverified.
Knockdown tests, chord coupons, drawn load paths and a complete joint bill would have to support any closing case.

Across sampled ship sizes the record-basis lift-to-mass ratio falls as diameter grows.
Each table cell gives sea level / 2,500 m for the same hull and mass, sized by `ship0()`:

| Lift-to-mass ratio: sea level / 2,500 m | 40 m | 44 m | 48 m | 52 m | 56 m | 60 m | 68 m | 80 m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| record | 0.585 / 0.457 | 0.582 / 0.454 | 0.577 / 0.451 | 0.558 / 0.436 | 0.543 / 0.424 | 0.532 / 0.416 | 0.508 / 0.397 | 0.455 / 0.356 |
| favourable | 0.956 / 0.747 | 0.987 / 0.771 | 0.953 / 0.744 | 0.981 / 0.766 | 0.969 / 0.757 | 0.969 / 0.757 | 0.957 / 0.748 | 0.916 / 0.715 |

No sampled hull floats as drawn on either basis at either altitude.
For the 52 m hull, the bill and drawing disagree in the end caps in both directions.
Across five readings, favourable lift-to-mass ratios span 0.751 to 0.998 at sea level and 0.586 to 0.780 at 2,500 m.
No reading reaches 1; none is a checked design.

The [member census](MEMBER-CENSUS.md) records 20 drawing/bill disagreements behind these float comparisons.

The page keeps its sentence until the float ledger generates this table from the model. The
rewrite then says what scale buys, which is the step from a bench cell to a ship, and where it
stops.

---

<!-- structure-questions:start -->
## Questions for an outside structures engineer

**Recorded 2026-10-02. Open.** These questions do not select a cap, a laminate or a new vehicle.
The [member census](MEMBER-CENSUS.md) and [cap readings](../research/analysis/cap-readings.md) preserve the measured disagreement.

### Cap members, directions and connections

What physical members, sections and connections make up the 52 m hull’s caps?
The drawing contains 16,905.361 m of cap hoops without a hoop bill line.
The grid is charged by 8,494.867 m² of area: 45.107 t record and 33.220 t favourable.
Do its membrane directions coincide with the drawn hoops or bars, and which sections and connections carry each load?
The drawn cap bars total 24,888.412 m; the grid also includes a bending-bar allowance.

### Station-aware cap and shoulder checks

What check would resolve station radius, member length, connection stiffness and the load transfer across each shoulder?
Inner rings total 9,826.902 m in the bill and 7,508.594 m in the drawing.
Shoulder diagonals total 610.940 m billed and 1,307.772 m drawn.
Their unchanged-section price increases by 8.885819 t record and 6.434558 t favourable, before the separate joint allowance.
Removing the grid stiffness returns cap margin 0 on both bases.
Which analysis and physical measurements would establish the applicability of a replacement check?

### Conditional laminate-stiffness sensitivity

What measured axial, hoop and shear properties, layup, coupling terms and compression allowables should describe the discrete tubes?
The code’s co-critical effective-modulus factor is 0.569876764239; the stated fibre-only 75/25 fixed-tube idealisation gives 0.433012701892.
Their local-capacity ratio is 1.316074013.
The executed sensitivity also uses consistent axial and global moduli under that same idealisation.
**This is conditional arithmetic, not measured laminate data or a corrected prediction.**

| Basis | Original mass t | Conditional mass t | Original sea-level / 2,500 m ratios | Conditional sea-level / 2,500 m ratios |
| --- | ---: | ---: | --- | --- |
| record | 403.101266 | 504.389381 | 0.558 / 0.436 | 0.446 / 0.348 |
| favourable | 229.161609 | 266.800490 | 0.981 / 0.766 | 0.843 / 0.658 |

Which laminate measurements would settle this difference before those moduli are used in a physical member check?
Execution record: [conditional sensitivity](audit/26-10-02-stiffness-sensitivity.json).

### Odd-column spoke anchors and polar stations

How should diametral spokes attach when the scaled model has 165 columns at 119 m diameter?
The Python bill counts 11,972 cords and the drawing contains 12,118.
The formula length is 1,030,187.784 m against 1,036,431.346 m drawn.
Which polar stations are physical members when 68 inner stations are billed but 64 rings are drawn?
What sections, anchors and terminations belong at those stations?

### Fittings, torsion straps and retired skin

What whole-hull fitting manifest replaces the area-derived 16,989.733 clamps and 50,969.199 pads?
Which physical joints support the 46.450 t record allowance and 32.945 t favourable allowance?
Where are the helical torsion straps charged at 0.256 t, distinct from the outfit’s circumferential straps?
What does the 1.019 t skin line represent after the inner void skin was retired from the drawing?
Which seals, coatings, bonds, seams and equipment attachments belong in a complete bill?

<a id="breach-hand-figures"></a>
### Breach hand figures without a generator

What calculation, load case and material basis support the physics note’s 0.162 kg/m³ tension and 3.59 kg/m³ compression figures?
They are hand figures without a generator. What would make that breach comparison reproducible and applicable to the proposed cellular architecture?
<!-- structure-questions:end -->

### Sag debit and enclosed volume

Why does removing sag alone give the lightest favourable cap reading a lift-to-mass ratio of 1.001 at sea level and 0.782 at 2,500 m?
How should the drawn mesh’s smaller enclosed volume change the billed lift basis?
What measured membrane shape would settle this sign change on the same safety factor and material basis?

### Reserve omitted on the favourable basis

Should the favourable figure include the stability reserve it currently leaves out?
What justifies `ship/model.js` gating that purchase on the record knockdown, when the same purchased increments cost 68.6 t at drawn lengths?
Which imperfection allowance should govern that comparison?

### Retired void skin still charged

Should the 0.170 t retired void skin remain in the mass bill?
Removing it alone leaves the lightest favourable reading 0.186 t short at sea level and 49.398 t short at 2,500 m.

### Greedy reserve increments

What station-aware stiffness and connection checks should replace the reserve solver’s greedy area steps of 0.0004, 0.00004, 0.0002 and 0.0000002 m² before their mass enters a float comparison?

### Outfit named but not weighed

What measured mass belongs to the outfit’s 622 solar pieces, 6 pods and 12 module pieces, and to the remaining equipment named in the census but absent from the bare-hull float comparison?

---

## Closed: current served energy figures use feasible plans

Closed on 2026-10-03. The monitor plans each mission at its exact leg distance, full wind input and shown mode; record basis is the default, with the same controls on the favourable basis beside it. Missing wind is labelled and uses still air. A mission without an accepted plan stands down and contributes no rate. The worked examples and ruled page sentences are generated and checked. Requested water, water kept aboard, energy supplied and water delivered remain distinct.

The interim labels are retired. Earlier report text remains dated history under its superseded-report warning; unsupported prescribed profiles remain diagnostic analysis. The model's structural, transient-control and hardware assumptions remain open. No aircraft has flown.

## What is not on this list

The model does not attempt weather beyond a single wind vector, turbulence, fire behaviour,
water's actual effect on a fire, air traffic, airspace, regulation, manufacturing or cost.
Those are not defects; they are the boundary of the thing. `docs/PHYSICS.md` says where
that boundary is drawn and why.

## Archived README wording before the generated front door

The passages below are retained verbatim as the historical README account. Their old dimensions and energy figures are not current; use the generated README table and current model records for present values. The live questions and decisions are in the sections above.

**The P-100 is the reference vehicle** — the smallest of the three, 190 m long, which is smaller
than the Hindenburg. The other two are the same arithmetic extrapolated, kept because energy per
tonne falls with size and because we wanted to know what stops you. It is the descent: a large
enough hull cannot push itself back down into the dense air over a lake. Nobody is proposing to
build a P-10000.

```js
AIRSHIPS.sim.ledger(AIRSHIPS.sim.CLASSES.P100, AIRSHIPS.sim.WORK_ALT_MSL)
// {rho: 0.9569, altMslM: 2500, liftT: 210.5, dryT: 100, reserveT: 10.5, surplusT: 110.5}
// the altitude is required: call it without one and it throws rather than assume sea level
```

## Known defects

All six are DECIDED. One is done: **#1, lift bought at sea level, was fixed on 2026-08-09**
and its numbers are published below. The other five are awaiting implementation, each with a
test that fails on purpose. The decision, its reasoning and its interactions are written up in
[docs/OPEN-QUESTIONS.md](OPEN-QUESTIONS.md) — what it costs, the options, and a
recommendation. They are open because fixing them means choosing what the vehicle is,
not just correcting a line.

These were found by audit. They are listed here rather than fixed quietly because a model that
hides its faults is worth less than one that publishes them, and the one that is fixed stays on
the list with its old and new numbers for the same reason.

**1. Sea-level lift, 1,500 m cruise — FIXED 2026-08-09.** `ledger()` in `sim/physics.js` computed
displacement lift at `CFG.rhoSL` = 1.225 kg/m³ and used it at every altitude, while the ships cruise
1,500 m above a plateau that is itself around 1,000 m up. Loaded break-even was 1.111 kg/m³, ISA at
1,005 m, so a full P-10000 was 860 t heavy on its drop run and 2,209 t heavy at its ceiling — the
sign of the net force reversed inside one cycle, against a page that says the rotors only ever push
down. `sim/atmosphere.js` now computes ISA density against altitude; `ledger()` takes an altitude in
metres MSL and throws without one; and the hulls were resized to a stricter requirement than the
defect asked for — FAIL-SAFE FLOAT-UP, buoyant at the working altitude while fully loaded with water
it cannot drop. Displacement grew 22.2% to 220,000 / 2.2M / 22M m³, the P-10000 from 820 to 876 m,
and the margin is +5.25% on all three classes. Cruise drag rose 14%.

The same correction has a second half. Lift depends on where the ship IS, and a cycle crosses
1,200 m of atmosphere, so float-up and descent do not share a worst case: float-up is hardest at the
ceiling, descent is hardest down at the lake where the air is 16% denser and the hull is 24% more
buoyant. `planCycle` was checking the descent balance at the ceiling — the easy end. Checked at the
source instead, the two larger classes could not hold themselves down on rotors and had to keep
water back as ballast, costing about 10% of the delivered figure.

Which raised the obvious question: what actually holds a buoyant ship down? Not ballast it has to
carry, make, or keep back. **It borrows the lake.** The larger classes lower a cable with a bag on
it, fill the bag, and winch it just clear of the surface — 12,400 t of water hanging on a line is
12,400 t of downward force, and it costs the 15 m of lift needed to break the surface, or
0.60 MWh.
When the tanks hold more than the shortfall, the bag is dumped back where it came from. It is a
Bambi bucket, the collapsible helicopter bucket in service since 1983, at a scale nobody has built:
the largest ever made is 9,800 litres, so ours is 1,265 times that.

Retention returns to zero and the whole load is delivered. Then the bag turned out to be worth far
more than the shortfall it was built for. Rotor power goes as thrust^1.5, so moving load onto the
lake pays superlinearly: sized to take 90% of the hold rather than the 8% the descent strictly
needed, it cuts `downMW` from 1,748 to 52 MW and the P-10000's cycle from 79.2 to **45.2 MWh** —
4.3 kWh per delivered tonne, against 7.6 before any of this. Every class carries one for that
reason, including the P-100, whose descent closes on rotors alone and which still saves 29%.

Two changes to how the cycle is flown followed from looking at the animation. The drop is **one
run, flown slowly** rather than three passes over the same line — every turn was an 876 m hull
reversing over the fire it was dropping on, the water lands on the same line either way, and the
turns were 4.3 minutes of pure overhead. And the approach now comes to a **dead stop before it
descends**: a bag of several thousand tonnes cannot be dipped from a ship still making 30 km/h.
Nothing yaws while there is line in the water, so the turn onto the outbound track waits until the
pod is clear.

An earlier attempt gave the big hulls 1,350 m hoses so they could fill from altitude and never meet
the dense air; that worked, and cost 29 MWh a cycle in pump work against a 2 m bore and 140 bar at
the pod. A cable is a much better thing to hang than a pipe: 12,400 t is 122 MN, which is about
440 mm of UHMWPE massing 125 t — and that rope is **not** charged as dry mass anywhere yet.

**2. Two power models that disagree by 2.8×.** `planCycle` builds an energy budget from five terms
and reports 90.2 MWh for the sampled P-10000 mission. Integrating `stateAt`'s per-system draw over
the same cycle gives 255.5 MWh. Both are shipped; the page shows the first as the headline energy
figure and the second on the instruments. At least one is wrong and they cannot both be right, and
fixing #1 widened the gap rather than closing it.

**3. An unexplained window still has no derivation, but no longer decides anything.** The letdown
term is `E.letdown = downMW * Math.min(6, dur.RETURN_TRANSIT * 0.2) / 60` in `sim/plan.js`, and
neither the 6-minute cap nor the 0.2 fraction has a stated justification. It used to be 45% of the
P-10000's published cycle — an unexplained constant setting the headline number. The descent anchor
did not explain it; it made it small, because rotor power goes as thrust^1.5 and the bag took the
thrust away. It is now 1.4 MWh of 45.2, or 3.1%, and the test that tracked this defect has come off
its known-failure marker. The constants are still unjustified and still worth deleting.

Also, and in the same spirit:

- **Retained descent ballast — FIXED 2026-08-09, and the fix is a bucket.** `retainedT` used to
  be 0 for every class, mode, distance and wind in the grid, while the copy, the `bottleneck`
  string and the narration all described retained ballast as a live constraint. It was not one.
  The cause was an altitude: the balance was struck at the ceiling, where the air is thinnest,
  when the letdown ends 1,200 m lower in air 16% denser. Struck where the descent happens, the
  P-1000 was 49 t short and the P-10000 1,056 t. The descent anchor pays that with lake water on
  a cable instead of with delivered payload, so retention is back to zero — but the mechanism is
  no longer dead code, and a test removes the anchor and watches the water go back in the tanks.
- **The cryogenic plant is numerically inert in the cycle.** For the same reason, `ln2MakeT` never
  changes how much water is delivered; it only moves energy between two terms, at the round-trip
  loss. The copy describes it as load-bearing. Its TANK is load-bearing as of 2026-08-09: at
  155 / 1,550 / 15,500 t it holds enough nitrogen to bring a dead, empty hull down and land it
  with no rotor authority, which takes 2.6 / 5.7 / 12.9 days on solar alone.
- **The generators supply thrust but never energy.** Each class advertises 8/40/150 MW, and
  `rotorMaxT` in `sim/plan.js` spends it when sizing how hard the rotors can push down. Nothing
  credits it as energy: `stateAt` reports only solar and nitrogen recovery, and the loop drains
  the rest from the battery. That generation is the nitrogen plant — expansion of what was
  liquefied earlier — so it is storage rather than a source, and modelling it honestly should
  make the deficit *larger*, not close it. Today it is doing neither.

All six are decided and none is implemented yet. The decisions matter as much as the defects,
because two of them are choices about what the vehicle is rather than corrections to arithmetic —
the hull is to be sized for fail-safe float-up when fully loaded, and the nitrogen plant, the
ballast doctrine and the generators all stay and must be made to bind. The reasoning, the options
that were rejected and the order the fixes have to happen in are in
[docs/OPEN-QUESTIONS.md](OPEN-QUESTIONS.md).


## What would change our minds

The concept rests on a small number of load-bearing claims. Each has a result that would sink it,
and we would rather be shown one than not.

- **Shell mass.** The ledger assumes structure mass equals payload mass — that a P-10000 hull
  enclosing 18 million m³ of vacuum weighs 10,000 t. A buckling analysis showing that no plausible
  material and geometry gets the evacuated shell below the mass of the air it displaces would end
  the concept, not amend it. This is the single most likely place for it to be wrong.
- **Lift at altitude.** If defect 1 is fixed honestly and the classes cannot be made net buoyant at
  a working altitude that clears BC terrain, then the aircraft is a helicopter with an expensive
  balloon attached, and the energy argument goes with it.
- **Energy per tonne.** If the honest per-cycle energy — once defects 2 and 3 are resolved — puts
  kWh per delivered tonne above what conventional air tankers and ground crews achieve, there is no
  case. The current 4.6–12.5 kWh/t is the number to attack; the comparison should be against real
  suppression logistics, not against nothing.
- **Sustainment.** Every class already runs a per-cycle deficit on these assumptions: solar at
  45 W/m² plus nitrogen recovery does not cover propulsion, pumping and the cryogenic plant, and
  `selftest()` asserts that this stays visibly true. The intended answer is battery tender ships
  swapping charged cells for discharged ones at mechanical speed — named, but deliberately not
  modelled here. If no plausible energy import chain closes the gap at the cycle rates claimed,
  the throughput figures are fiction. A related limit, which we would rather state than hide: a
  hull that runs its storage down may be unable to descend until solar, nitrogen expansion or a
  swap restores it.
- **What arrives.** Tonnes delivered is not fire extinguished. Evidence that 10,000 t released from
  450 m over a convective column arrives as drift rather than as water on fuel would make the
  headline metric the wrong metric.
- **Downwash.** Nothing in this model accounts for what an 876 m hull trimming on rotors 450 m above
  a fire does to the fire's own air. A credible estimate that the downwash spreads more fire than
  the water suppresses would invert the whole idea.
- **Water.** Surface area is used as a proxy for a lake being drawable. Evidence that repeated
  full-payload draws from the mapped bodies are hydrologically, ecologically or legally impossible
  breaks the logistics chain regardless of whether the aircraft flies.

If you have one of these, [CONTRIBUTING.md](../CONTRIBUTING.md) explains the one thing we ask: bring
the number you computed and how you computed it.

## Claims awaiting review

<a id="float-deferred-energy-model"></a>
### Energy, delivery and descent

Which flight-model energy, delivery and descent results replace the deferred claims? The float record does not review those performance results. Closure needs regenerated outputs, reconciled prose and replacement dispositions.

`python3 tools/float_claims.py --stats` prints the current count; [the generated list](FLOAT-DEFERRED.md) identifies every block and its reason.

<a id="float-deferred-mixed-block"></a>
### Mixed statements

How should each mixed block distinguish current structural results, historical claims, outside designs and operational assumptions? The float record leaves inseparable statements unreviewed. Closure needs independently supported statements and new dispositions without discarding history.

`python3 tools/float_claims.py --stats` prints the current count; [the generated list](FLOAT-DEFERRED.md) identifies every block and its reason.

<a id="float-deferred-hand-arithmetic"></a>
### Arithmetic without generated records

Which generated calculations support the deferred hand arithmetic and probe figures? The float record has no reproducible source for these comparisons. Closure needs named generated fields, their stated bases and freshness checks before binding the figures.

`python3 tools/float_claims.py --stats` prints the current count; [the generated list](FLOAT-DEFERRED.md) identifies every block and its reason.

<a id="float-deferred-source-needed"></a>
### Outside quantities without sources

Which sources and reference states support the deferred figures for outside aircraft, materials and measurements? The float record leaves these quantities unreviewed. Closure needs traceable quantitative sources and dispositions tied to those sources.

`python3 tools/float_claims.py --stats` prints the current count; [the generated list](FLOAT-DEFERRED.md) identifies every block and its reason.
