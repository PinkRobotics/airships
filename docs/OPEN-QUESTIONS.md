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
> | #13 | **Mapped shore proximity is measured separately from drafting stations.** The water study records geometric distances, with no claim of operational availability; depth, access and permission remain unknown. | `water-availability.md` |
> | #0, #4 | **The cryogenic plant CANNOT be deleted** — a sealed-cell hull has no way to ballast with air, and an earlier claim that it could is retracted. But the ship makes nitrogen on every cycle it does not need, at **32.5%** of the P-100's cycle energy as the one model prices it since 2026-10-01 (52.5% of the smaller cycle published before). | `air-ballast.md` |
> | #3, #14, #15 | **FIXED 2026-10-01 — one energy model.** The letdown is 0.390 / 4.279 / 35.398 MWh, a fifth of each cycle, against the 0.012 / 0.161 / 1.420 the window constant produced; cycle energy rose 45 / 115 / 224%. The bag's credit to the rotors is 0.7–5.2% of the cycle — not the 96% once claimed, nor the 27–49% this note then argued — and what it buys is water (2,248 t a cycle on the P-10000). | `descent.md`, `../docs/ENERGY-MODEL-2026-10.md` |
> | #8 | **Re-opened, and now measurable.** `diskM2` was retired as inert on a measurement taken against a letdown too small to see it. With the rotors priced over the whole flight, ±20% on the disc moves the P-10000 cycle by +9.6% / −5.8% and `battMW` ±20% moves it −0.1% / +2.3% through the letdown clamp. | `descent.md` |
> | #12 | **`ALT.drop` = 450 m does not deliver water** — and the ship's own rotors push air *upward* at 86× the mass flow of the water. The answer is sprayer leads. The accepted-plan analysis reports a conditional geometric line-length comparison; it establishes no deposition or fire outcome. | `delivery.md` |
>
> Regenerate all of it with `make analysis`.
>
> **2026-10-02 correction to #11:** the conditional capsule budget now gives 457,324 m³ and 140 m length. This is equipment-budget closure under an assumed shell density, not a checked design.

<!-- anchor-budget:question:start -->
> Current anchor-reach correction to #11: the conditional equipment budget gives 510,406 m³ and 146 m length, replacing the earlier 457,324 m³ after corrected reach changed energy-based battery sizing. This is not a checked design.
<!-- anchor-budget:question:end -->
> See [the regeneration audit](audit/26-10-02-analysis-regeneration.md).

<!-- closure-correction:start -->

> **2026-10-05 correction to #11:** shell sundries were omitted from the resized
> bill. The 0.508 kg/m³ floor now closes conditionally at 510,406 m³,
> a 146 m hull. Its closure wall is 0.870 kg/m³; 0.957 kg/m³ is the lift wall.
> This complete equipment bill does not validate a drawn hull.

<!-- closure-correction:end -->

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

An earlier edition of `docs/PHYSICS.md` quantified items 0–6 in its §11 under different numbers (its Defects 4 and 5
were the two halves of item 4 below, its Defect 6 was item 6, item 5 had no entry as it is not physics); the current
PHYSICS carries no such list. Items 7–12 were documented here only.

---

<!-- logistics:line-summary:start -->
At the accepted median-leg rate, the conditional CL 4 line-length quotient is 93.0 km per day, longer than 80.0% of the stored simplified final perimeters; this is a geometric comparison, with no fire-outcome inference.
<!-- logistics:line-summary:end -->

## 0. The sizing requirement that ties #1, #4 and #6 together

**DECIDED 2026-08-09.** Added before the individual defects because it constrains three of
them at once, and because it is the requirement that makes ballast a structural part of the
vehicle rather than a doctrine the code ignores.

**Total-failure recovery, unpowered.** Assume the rotors have failed entirely and the
battery is flat. The ship must then:

<!-- atmosphere:recovery:start -->
1. float up within the flight model's reference-atmosphere assumption (#1): a loaded model rises
   only when air density exceeds its computed boundary at 2,500 m MSL
   (P-100: 0.909091 kg/m³, reference temperature +14.29 K; P-1000: 0.909091 kg/m³, reference temperature +14.29 K; P-10000: 0.909091 kg/m³, reference temperature +14.29 K). These temperature offsets hold reference pressure at 74682.51 Pa;
   they do not establish a weather envelope. See the [generated boundaries](../research/analysis/loaded-atmosphere.json);
2. recharge on solar alone;
3. liquefy enough nitrogen to make itself heavy enough to descend **with no rotor
   authority at all**; and
4. land empty on ballast alone.
<!-- atmosphere:recovery:end -->

Taking days to do it is acceptable. Being unable to do it is not. Recharging on solar alone is a requirement: the energy suffices on paper as a lossless quotient, while making and retaining the required ballast has not been shown. The capacity self-test checks that the tanks can hold it, not that the plant and storage can accumulate it. The generated recovery question below gives the energy-based loss requirement and ground-tank sensitivities.

That fourth step is the demanding one, because it sizes the cryogenic plant and the nitrogen
tankage: the LN₂ aboard must be able to exceed the *empty* hull's surplus buoyancy at
altitude. With the hull already grown for fail-safe float-up when full, that is roughly a
payload's worth of nitrogen.

**CURRENT RECOVERY STATUS: PARTLY SPECIFIED.** Capacity and lossless energy accounting are specified; production and retention remain open. The following sizing tables are the superseded 2026-08-09 record from the earlier peak-solar model, with no storage loss. The recorded “DONE” below refers to that historical sizing work, not demonstrated production and retention.

**DONE 2026-08-09.** Built, with one correction to the sizing table below. What was
planned, at ρ = 0.96 kg/m³ (about 2,500 m MSL: 1,500 m over a 1,000 m plateau), a 5%
float-up margin when fully loaded, and the model's own `eLN2` = 0.45 kWh/kg:

| class | hull grows | LN₂ to sink an empty hull | capacity in that record | tankage | energy | lossless solar energy quotient | at rated cryo power |
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

The corrected 2026-08-09 sizing record from that earlier peak-solar model used ISA density and
ground-level ballast. This superseded table also gives lossless energy quotients, not measured tank or aircraft results:

| class | displacement | hull grows | LN₂ to land an empty hull | tank | tankage | energy | lossless solar energy quotient | at rated cryo power |
|---|---|---|---|---|---|---|---|---|
| P-100 | 180,000 → 220,000 m³ | +22.2% | 144.6 t | 155 t | 192 m³ | 65 MWh | 2.6 days | 0.45 days |
| P-1000 | 1.8 → 2.2 ×10⁶ m³ | +22.2% | 1,445.6 t | 1,550 t | 1,921 m³ | 651 MWh | 5.7 days | 0.90 days |
| P-10000 | 1.8 → 2.2 ×10⁷ m³ | +22.2% | 14,456.1 t | 15,500 t | 19,207 m³ | 6,505 MWh | 12.9 days | 2.7 days |

Lengths and diameters follow: 177 × 44 → **190 × 47 m**, 380 × 95 → **404 × 102 m**,
820 × 205 → **876 × 219 m**, all at fineness 4. The float-up margin is 5.25% and is
identical for all three classes, because dry mass is set equal to payload for all three. No
class needed the rotor-lift exception #1 allows, and none was granted one.

Four things fall out of it.

**Liquid volume and tank mass are different allowances.** The liquid occupies little of the hull volume, while insulated tanks are a material mass allowance in the budget. Storage loss, cold readiness and the production schedule constrain recovery as well as the lossless energy bill.

**Plant rating and tank capacity do not establish recovery.** The earlier sizing record increased capacity while retaining the plant rating. Rated-power and solar-only quotients still omit cold maintenance, startup and storage loss; neither supplies a production and retention trajectory.

**Solar recovery days are lossless energy quotients.** The generated recovery question below uses the current day-average solar budget after hotel load. Those quotients are neither a worst-case time nor a demonstration that a real plant can operate at that average input and retain the ballast. The ground-tank sensitivities show why a storage-loss requirement is needed; they do not prove recovery impossible with every tank.

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
"descent authority" as its bottleneck. These are earlier model readings, not figures in the current PHYSICS sections.

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
| P100 | 159.325 | 32.282 |
| P1000 | 785.857 | 156.061 |
| P10000 | 7551.654 | 1411.659 |
<!-- energy:question-2:end -->

<!-- energy:question-3:start -->
## 3. What vertical profile remains feasible with acceleration included?

The search stops at a peak letdown cap of 0.5 m/s. What lower bound would mission conditions justify?

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished. Can shape-specific added-mass and control measurements close the signed authority gaps? Full-delivery profiles below are quasi-static analysis.

No full-payload profile meets the control reserve target in this stated search.

| Class | km | Basis | Full-payload mode | Delivered t | Minutes | MWh | kWh/t | Profile note |
|---|---|---|---|---|---|---|---|---|
<!-- energy:question-3:end -->

<!-- energy:question-4:start -->
## 4. How much delivery can be retained while holding the hull?

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished. Can a measured vehicle carry the retained-water requirements below throughout the cycle? What reserve is needed beyond the first closing threshold?

| Class | km | Basis | Profile | Delivered t | Kept t | Minutes | MWh | kWh/delivered tonne | Profile note |
|---|---|---|---|---|---|---|---|---|---|
| P100 | 15 | record | as drawn: does not close | 100.000 | 0.000 | 34.196 | 7.812 | 78.122 |  |
| P100 | 15 | record | cheapest reserve-eligible profile found in the stated space | 70.948 | 29.052 | 40.108 | 6.622 | 93.338 | quasi-static closure; dynamic profile unresolved |
| P100 | 15 | favourable | as drawn: does not close | 100.000 | 0.000 | 34.196 | 6.024 | 60.241 |  |
| P100 | 15 | favourable | cheapest reserve-eligible profile found in the stated space | 70.000 | 30.000 | 40.076 | 4.843 | 69.192 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | record | as drawn: closes | 100.000 | 0.000 | 104.784 | 20.150 | 201.503 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | record | cheapest reserve-eligible profile found in the stated space | 89.304 | 10.696 | 63.815 | 12.706 | 142.281 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | favourable | as drawn: closes | 100.000 | 0.000 | 104.784 | 14.393 | 143.928 | quasi-static closure; dynamic profile unresolved |
| P100 | 60 | favourable | cheapest reserve-eligible profile found in the stated space | 90.930 | 9.070 | 74.835 | 10.035 | 110.357 | quasi-static closure; dynamic profile unresolved |
| P1000 | 15 | record | as drawn: does not close | 1000.000 | 0.000 | 35.362 | 61.680 | 61.680 |  |
| P1000 | 15 | record | cheapest reserve-eligible profile found in the stated space | 191.775 | 808.225 | 25.483 | 24.472 | 127.610 | quasi-static closure; dynamic profile unresolved |
| P1000 | 15 | favourable | as drawn: does not close | 1000.000 | 0.000 | 35.362 | 60.689 | 60.689 |  |
| P1000 | 15 | favourable | cheapest reserve-eligible profile found in the stated space | 191.775 | 808.225 | 25.483 | 19.815 | 103.325 | quasi-static closure; dynamic profile unresolved |
| P1000 | 60 | record | as drawn: does not close | 1000.000 | 0.000 | 93.116 | 140.806 | 140.806 | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | cheapest reserve-eligible profile found in the stated space | 244.826 | 755.174 | 73.907 | 65.351 | 266.928 | quasi-static closure; dynamic profile unresolved |
| P1000 | 60 | favourable | as drawn: does not close | 1000.000 | 0.000 | 93.116 | 141.626 | 141.626 | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | cheapest reserve-eligible profile found in the stated space | 244.826 | 755.174 | 73.907 | 54.099 | 220.969 | quasi-static closure; dynamic profile unresolved |
| P10000 | 15 | record | as drawn: does not close | 10000.000 | 0.000 | 45.512 | 679.093 | 67.909 |  |
| P10000 | 15 | record | cheapest reserve-eligible profile found in the stated space | 2945.496 | 7054.504 | 24.022 | 202.102 | 68.614 | quasi-static closure; dynamic profile unresolved |
| P10000 | 15 | favourable | as drawn: does not close | 10000.000 | 0.000 | 45.512 | 750.823 | 75.082 |  |
| P10000 | 15 | favourable | cheapest reserve-eligible profile found in the stated space | 2945.496 | 7054.504 | 24.022 | 184.209 | 62.539 | quasi-static closure; dynamic profile unresolved |
| P10000 | 60 | record | as drawn: does not close | 10000.000 | 0.000 | 94.381 | 1098.254 | 109.825 |  |
| P10000 | 60 | record | cheapest reserve-eligible profile found in the stated space | 2993.634 | 7006.366 | 58.071 | 402.745 | 134.534 | quasi-static closure; dynamic profile unresolved |
| P10000 | 60 | favourable | as drawn: does not close | 10000.000 | 0.000 | 94.381 | 1370.397 | 137.040 |  |
| P10000 | 60 | favourable | cheapest reserve-eligible profile found in the stated space | 3009.668 | 6990.332 | 70.313 | 368.571 | 122.462 | quasi-static closure; dynamic profile unresolved |
<!-- energy:question-4:end -->

## 5. Esri basemap tiles — FIXED 2026-10-01

Removed the Esri tile loader and satellite toggle. The bundled first-party terrain hillshade
is now the default backdrop, with outlined labels and markers and stronger water/perimeter
contrast. No Esri tiles are fetched or redistributed: `DATA-SOURCES.md` records the backdrop's
sources and terms under `data/terrain-bc.jpg`, and the network gate below refuses external
hosts.

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
| P100 | rapid | 31.238 | 2.122 | 133.407 |
| P100 | balanced | 32.282 | 2.122 | 136.578 |
| P100 | endurance | 33.912 | 2.122 | 141.457 |
| P1000 | rapid | 153.498 | 12.572 | 643.926 |
| P1000 | balanced | 156.061 | 12.572 | 651.709 |
| P1000 | endurance | 160.063 | 12.572 | 663.772 |
| P10000 | rapid | 1408.045 | 61.860 | 6874.232 |
| P10000 | balanced | 1411.659 | 61.860 | 6886.530 |
| P10000 | endurance | 1417.304 | 61.860 | 6905.714 |
<!-- energy:question-6:end -->

## 7. Thirty-two unjustified constants, and only fifteen of them are dialled

**Current anchor correction:** the audit measurements below use an earlier sizing model.
They do not establish achieved inventory or current cycle closure. The present bag sizes
are an intention to carry about 90% of the source hold; the nominal-keel reach and actual
held-water channel determine the split. Current prescribed profiles and supplied effort
are generated in `research/analysis/descent.json`; this is not structural float or handling
validation.

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

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished. What evidence supports the installed disk area, downward-only thrust and battery rating together? Can any required storage mass fit inside the dry-mass target?

## What the model would require

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

Generated by `node research/analysis/energy-tables.mjs`. Each printed closing value is rounded up to three decimals and replayed at the verdict resolution.

| Class | km | Basis | As drawn | Minutes: drawn / kept / power pair | Water kept, t | Delivered, t | kWh/t | Required battery, MW | Rotor thrust, t | Battery mass, t (500 / 300 / 149 Wh/kg) | Storage notes |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|
| P100 | 15 | record | does not close | 34.196 / none / none | none | none | none | none | none | none |  |
| P100 | 15 | favourable | does not close | 34.196 / none / none | none | none | none | none | none | none |  |
| P100 | 60 | record | closes | 104.784 / 104.784 / 104.784 | 0.000 | 100.000 | 201.503 | 29.850 | 131.166 | 39.800 / 66.333 / 133.557 (exceeds dry target) | retained-water: ; power pair:  |
| P100 | 60 | favourable | closes | 104.784 / 104.784 / 104.784 | 0.000 | 100.000 | 143.928 | 28.658 | 131.166 | 38.211 / 63.684 / 128.224 (exceeds dry target) | retained-water: ; power pair:  |
| P1000 | 15 | record | does not close | 35.362 / 28.389 / 35.362 | 800.681 | 199.319 | 123.582 | 521.681 | 1367.262 | 834.690 / 1391.149 (exceeds dry target) / 2800.972 (exceeds dry target) | retained-water: ; power pair:  |
| P1000 | 15 | favourable | does not close | 35.362 / 28.389 / 35.362 | 800.681 | 199.319 | 96.228 | 521.681 | 1367.262 | 834.690 / 1391.149 (exceeds dry target) / 2800.972 (exceeds dry target) | retained-water: ; power pair:  |
| P1000 | 60 | record | does not close | 93.116 / 86.423 / 93.116 | 750.235 | 249.765 | 267.061 | 499.667 | 1349.041 | 799.467 / 1332.445 (exceeds dry target) / 2682.776 (exceeds dry target) | unsupported profile; exceeds nominal storage in an ideal cycle; retained-water: ; power pair: quasi-static closure; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | does not close | 93.116 / 86.423 / 93.116 | 750.235 | 249.765 | 208.265 | 499.667 | 1349.041 | 799.467 / 1332.445 (exceeds dry target) / 2682.776 (exceeds dry target) | unsupported profile; exceeds nominal storage in an ideal cycle; retained-water: ; power pair: quasi-static closure; exceeds nominal storage in an ideal cycle |
| P10000 | 15 | record | does not close | 45.512 / 32.455 / 45.512 | 6366.275 | 3633.725 | 79.727 | 3892.845 | 13092.990 | 11122.414 (exceeds dry target) / 18537.357 (exceeds dry target) / 37323.538 (exceeds dry target) | retained-water: ; power pair:  |
| P10000 | 15 | favourable | does not close | 45.512 / 32.455 / 45.512 | 6366.275 | 3633.725 | 71.249 | 3892.845 | 13092.990 | 11122.414 (exceeds dry target) / 18537.357 (exceeds dry target) / 37323.538 (exceeds dry target) | retained-water: ; power pair:  |
| P10000 | 60 | record | does not close | 94.381 / 81.453 / 94.381 | 6250.292 | 3749.708 | 148.256 | 3848.409 | 13092.989 | 10995.454 (exceeds dry target) / 18325.757 (exceeds dry target) / 36897.498 (exceeds dry target) | retained-water: ; power pair:  |
| P10000 | 60 | favourable | does not close | 94.381 / 81.453 / 94.381 | 6250.292 | 3749.708 | 129.694 | 3848.409 | 13092.989 | 10995.454 (exceeds dry target) / 18325.757 (exceeds dry target) / 36897.498 (exceeds dry target) | retained-water: ; power pair:  |

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
| P1000 | 15 | record | 61.681 |
| P1000 | 15 | favourable | 61.681 |
| P1000 | 60 | record | 60.430 |
| P1000 | 60 | favourable | 60.430 |
| P10000 | 15 | record | 388.207 |
| P10000 | 15 | favourable | 388.207 |
| P10000 | 60 | record | 386.953 |
| P10000 | 60 | favourable | 386.953 |

## Broadside-drag range

Each entry gives the signed worst unheld force in tonnes and the feasibility verdict. Negative force needs upward authority, which is unavailable.

| Class | km | Basis | Coefficient 0 | Coefficient 1 | Coefficient 2 |
|---|---:|---|---|---|---|
| P100 | 15 | record | 13.274; does not close;  | 34.759; does not close;  | 56.679; does not close;  |
| P100 | 15 | favourable | 0.798; does not close;  | -5.714; does not close;  | -32.818; does not close;  |
| P100 | 60 | record | 0.000; closes;  | -0.000; closes;  | -0.000; closes;  |
| P100 | 60 | favourable | 0.000; closes;  | -0.000; closes;  | -0.000; closes;  |
| P1000 | 15 | record | 718.423; does not close;  | 800.681; does not close;  | 882.939; does not close;  |
| P1000 | 15 | favourable | 718.423; does not close;  | 800.681; does not close;  | 882.939; does not close;  |
| P1000 | 60 | record | 667.977; does not close; unsupported profile; exceeds nominal storage in an ideal cycle | 750.235; does not close; unsupported profile; exceeds nominal storage in an ideal cycle | 832.493; does not close; unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | 667.977; does not close; unsupported profile; exceeds nominal storage in an ideal cycle | 750.235; does not close; unsupported profile; exceeds nominal storage in an ideal cycle | 832.493; does not close; unsupported profile; exceeds nominal storage in an ideal cycle |
| P10000 | 15 | record | 6167.429; does not close;  | 6366.280; does not close;  | 6565.131; does not close;  |
| P10000 | 15 | favourable | 6167.429; does not close;  | 6366.280; does not close;  | 6565.131; does not close;  |
| P10000 | 60 | record | 6096.904; does not close;  | 6250.297; does not close;  | 6449.148; does not close;  |
| P10000 | 60 | favourable | 6096.904; does not close;  | 6250.297; does not close;  | 6449.148; does not close;  |

## Rotor-efficiency range

Rotor figure of merit times drive efficiency. Hold-down descent is priced as climb, on the conservative side; climb against hold-down thrust is priced as level flight, with no bound claimed.

| Class | km | Basis | Efficiency | Static thrust cap over local densities, t | Worst unheld force, t | Verdict | Storage note |
|---|---:|---|---:|---|---:|---|---|
| P100 | 15 | record | 0.55 | 130.327 to 135.663 | 47.665 | does not close |  |
| P100 | 15 | record | 0.7 | 153.059 to 159.325 | 34.759 | does not close |  |
| P100 | 15 | favourable | 0.55 | 130.327 to 135.663 | 47.665 | does not close |  |
| P100 | 15 | favourable | 0.7 | 153.059 to 159.325 | -5.714 | does not close |  |
| P100 | 60 | record | 0.55 | 130.327 to 135.663 | 17.748 | does not close | unsupported profile; exceeds nominal storage in an ideal cycle |
| P100 | 60 | record | 0.7 | 153.059 to 159.325 | -0.000 | closes |  |
| P100 | 60 | favourable | 0.55 | 130.327 to 135.663 | 15.997 | does not close |  |
| P100 | 60 | favourable | 0.7 | 153.059 to 159.325 | -0.000 | closes |  |
| P1000 | 15 | record | 0.55 | 646.328 to 669.145 | 892.273 | does not close |  |
| P1000 | 15 | record | 0.7 | 759.061 to 785.857 | 800.681 | does not close |  |
| P1000 | 15 | favourable | 0.55 | 646.328 to 669.145 | 892.273 | does not close |  |
| P1000 | 15 | favourable | 0.7 | 759.061 to 785.857 | 800.681 | does not close |  |
| P1000 | 60 | record | 0.55 | 642.828 to 669.145 | 846.818 | does not close | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | 0.7 | 754.950 to 785.857 | 750.235 | does not close | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | 0.55 | 642.828 to 669.145 | 846.818 | does not close | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | 0.7 | 754.950 to 785.857 | 750.235 | does not close | unsupported profile; exceeds nominal storage in an ideal cycle |
| P10000 | 15 | record | 0.55 | 6238.062 to 6430.112 | 7322.061 | does not close |  |
| P10000 | 15 | record | 0.7 | 7326.107 to 7551.654 | 6366.280 | does not close |  |
| P10000 | 15 | favourable | 0.55 | 6238.062 to 6430.112 | 7322.061 | does not close |  |
| P10000 | 15 | favourable | 0.7 | 7326.107 to 7551.654 | 6366.280 | does not close |  |
| P10000 | 60 | record | 0.55 | 6177.222 to 6430.112 | 7215.718 | does not close |  |
| P10000 | 60 | record | 0.7 | 7254.655 to 7551.654 | 6250.297 | does not close |  |
| P10000 | 60 | favourable | 0.55 | 6177.222 to 6430.112 | 7215.718 | does not close |  |
| P10000 | 60 | favourable | 0.7 | 7254.655 to 7551.654 | 6250.297 | does not close |  |
<!-- energy:question-8:end -->

<!-- energy:question-9:start -->
## 9. How long can recovery take through a real day and night?

The model uses 45 W/m² as a day average. What storage and charging losses apply when instantaneous sunlight is zero?

| Class | Day-average solar MW | Ground-surplus solar days | Full-tank solar days |
|---|---|---|---|
| P100 | 0.207 | 58.189 | 62.390 |
| P1000 | 0.967 | 162.233 | 173.948 |
| P10000 | 4.476 | 183.696 | 196.960 |
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
  rotors, tanks, batteries or the installed anchor cable that the bottom-up budget charges
  under its stated minimum-strength, quasi-static pickup and safety-factor policy.
- **Metlen & Palazotto 2013**'s only real-materials vacuum-lift design has a
  structure-to-buoyancy ratio of **0.94** — structure alone consuming what we allocate to
  structure *and* payload.
- Separately: the configured battery ratio differs by class. The built X-57 pack was 149 Wh/kg (Chin et al., printed p. 2);
  the electric aircraft did not fly ([NASA's lessons learned](https://ntrs.nasa.gov/api/citations/20240006845/downloads/SE_lessonsleared_final.pdf), printed p. 4).

<!-- battery:ratios:start -->
At the 149 Wh/kg reference pack density, the battery alone exceeds the dry allowance on P-100 and P-10000.
The per-class ratio of reference-pack mass to dry allowance is shown below.
The complete nominal floor budget exceeds the dry allowance on P-100, P-1000, P-10000, as its own totals show below.

| Class | Battery MWh | Dry allowance t | MWh/t dry | Battery-only minimum Wh/kg | Reference pack t | Pack / dry ratio | Complete floor t | Floor / dry |
|---|---|---|---|---|---|---|---|---|
| P-100 | 20 | 100 | 0.20 | 200 | 134.2 | 134.2% | 216.1 | 2.16× |
| P-1000 | 120 | 1,000 | 0.12 | 120 | 805.4 | 80.5% | 1,803.6 | 1.80× |
| P-10000 | 2,000 | 10,000 | 0.20 | 200 | 13,422.8 | 134.2% | 19,524.2 | 1.95× |

The complete floor uses the budget’s own evidence choices, including its 500 Wh/kg battery assumption; it is separate from the 149 Wh/kg reference-pack comparison.

This comparison comes from [battery-ratios.json](../research/analysis/battery-ratios.json), configuration and the generated mass budget. It does not establish a buildable pack or a complete aircraft.
<!-- battery:ratios:end -->

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

## 13. Water geometry is measured; operational availability remains open

The whole concept is a duty cycle between a fire and a lake. `sim/plan.js` takes the one-way
distance as an input and `sim/water.js` applies a size-weighted choice among reachable generated drafting stations, but **no figure anywhere
in this project says what fraction of real fires have an adequate source within range.**

Adequate means more than nearby. A P-10000 draws 10,000 t a cycle at
13,183 t/h and hovers over the surface while it does it, so the body has to be large enough and
deep enough to stand repeated full-payload draws, and open enough to hold station over. A pond at
4 km is not a source.

This matters more than most entries on this list because it bounds the market rather than the
vehicle. If the answer is "most fires in the interior", the concept has a customer. If it is "a
quarter of them", the fleet is a niche tool and the P-100 is the interesting class rather than the
P-10000.

**Partial answer: geographic measures.** The water-availability study joins the dated
points and mapped water already in `data/`, and reports mapped shore proximity separately
from generated drafting stations. Planned legs are reported for the invented exercise alone.
Operational availability remains open: station depth, access, permission and sustainable draw
are not established by that spatial join.


---

<!-- energy:question-14:start -->
## 14. Can the bag be picked up and released at this scale?

What cable, winch and control measurements would quantify pickup loads and pendulum motion? How much station-keeping power is missing under a beam wind?

## What this model leaves out

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

Generated by `node research/analysis/energy-omissions.mjs`. These loads are not silently absorbed into a closing claim.

| Class | Beam-wind side force, t | Cable mass, t (floor / credible / demonstrated) | Battery mass, t (same cases) | Dry target, t | Bag, t | Cable, m | Pendulum period, s | Day-average solar, MW |
|---|---:|---|---|---:|---:|---:|---:|---:|
| P100 | 29.709 | 0.644 / 1.431 / 2.146 | 40.000 / 66.667 / 134.228 | 100 | 125 | 350 | 37.530 | 0.207 |
| P1000 | 139.077 | 11.036 / 24.525 / 36.788 | 240.000 / 400.000 / 805.369 | 1000 | 1250 | 600 | 49.138 | 0.967 |
| P10000 | 643.635 | 155.096 / 344.658 / 516.987 | 4000.000 / 6666.667 / 13422.819 | 10000 | 12400 | 850 | 58.486 | 4.476 |

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

Generated by `node research/analysis/energy-unheld.mjs`. Largest absolute signed unheld force in each failing phase, using the verdict mesh, refined extrema and both sides of seams from cycleLimits, with additional local refinement for the printed phase peak. Positive is unsupported surplus lift; negative requires unavailable upward authority.

| Class | km | Basis | Profile | Phase | Signed unheld, t | Progress | Cycle minute | Airspeed, m/s | Vertical speed, m/s | Limits | Storage note |
|---|---:|---|---|---|---:|---:|---:|---:|---:|---|---|
| P100 | 15 | record | as drawn | SOURCE_APPROACH | 2.334 | 0.604878 | 1.210 | 0.000 | -2.283 | bus power, anchor cable reach |  |
| P100 | 15 | record | as drawn | OUTBOUND_TRANSIT | -5.714 | 0.222832 | 7.955 | 25.000 | 9.745 | upward authority unavailable |  |
| P100 | 15 | record | as drawn | RETURN_TRANSIT | 34.759 | 0.810716 | 31.969 | 25.000 | -8.821 | bus power |  |
| P100 | 15 | favourable | as drawn | SOURCE_APPROACH | 2.334 | 0.604878 | 1.210 | 0.000 | -2.283 | bus power, aerodynamic coefficient, anchor cable reach |  |
| P100 | 15 | favourable | as drawn | OUTBOUND_TRANSIT | -5.714 | 0.222832 | 7.955 | 25.000 | 9.745 | upward authority unavailable |  |
| P100 | 60 | record | as drawn | no unheld phase | 0 | | | | | |  |
| P100 | 60 | favourable | as drawn | no unheld phase | 0 | | | | | |  |
| P1000 | 15 | record | as drawn | SOURCE_APPROACH | 800.681 | 0.629117 | 1.887 | 0.000 | -7.829 | bus power, rotor thrust, anchor cable reach |  |
| P1000 | 15 | record | as drawn | WATER_FILL | 418.983 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach |  |
| P1000 | 15 | record | as drawn | WATER_RELEASE | 643.713 | 1.000000 | 23.737 | 0.000 | 0.052 | bus power, rotor thrust |  |
| P1000 | 15 | record | as drawn | BUOYANCY_ESCAPE | 643.717 | 0.000000 | 23.737 | 0.000 | 0.011 | bus power, rotor thrust |  |
| P1000 | 15 | record | as drawn | RETURN_TRANSIT | 588.712 | 1.000000 | 35.362 | 9.167 | -0.000 | bus power, rotor thrust |  |
| P1000 | 15 | favourable | as drawn | SOURCE_APPROACH | 800.681 | 0.629117 | 1.887 | 0.000 | -7.829 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P1000 | 15 | favourable | as drawn | WATER_FILL | 418.983 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P1000 | 15 | favourable | as drawn | WATER_RELEASE | 643.713 | 1.000000 | 23.737 | 0.000 | 0.052 | bus power, rotor thrust, aerodynamic coefficient |  |
| P1000 | 15 | favourable | as drawn | BUOYANCY_ESCAPE | 643.717 | 0.000000 | 23.737 | 0.000 | 0.011 | bus power, rotor thrust, aerodynamic coefficient |  |
| P1000 | 15 | favourable | as drawn | RETURN_TRANSIT | 504.128 | 1.000000 | 35.362 | 9.167 | -0.000 | bus power, rotor thrust, aerodynamic coefficient |  |
| P1000 | 60 | record | as drawn | SOURCE_APPROACH | 750.235 | 0.629117 | 1.887 | 0.000 | -7.829 | bus power, rotor thrust, anchor cable reach | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | as drawn | WATER_FILL | 362.490 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | as drawn | WATER_RELEASE | 643.713 | 1.000000 | 52.614 | 0.000 | 0.052 | bus power, rotor thrust | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | as drawn | BUOYANCY_ESCAPE | 643.717 | 0.000000 | 52.614 | 0.000 | 0.014 | bus power, rotor thrust | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | record | as drawn | RETURN_TRANSIT | 566.252 | 1.000000 | 93.116 | 9.167 | -0.000 | bus power, rotor thrust | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | as drawn | SOURCE_APPROACH | 750.235 | 0.629117 | 1.887 | 0.000 | -7.829 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | as drawn | WATER_FILL | 362.490 | 0.300000 | 4.667 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | as drawn | WATER_RELEASE | 643.713 | 1.000000 | 52.614 | 0.000 | 0.052 | bus power, rotor thrust, aerodynamic coefficient | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | as drawn | BUOYANCY_ESCAPE | 643.717 | 0.000000 | 52.614 | 0.000 | 0.014 | bus power, rotor thrust, aerodynamic coefficient | unsupported profile; exceeds nominal storage in an ideal cycle |
| P1000 | 60 | favourable | as drawn | RETURN_TRANSIT | 481.668 | 1.000000 | 93.116 | 9.167 | -0.000 | bus power, rotor thrust, aerodynamic coefficient | unsupported profile; exceeds nominal storage in an ideal cycle |
| P10000 | 15 | record | as drawn | SOURCE_APPROACH | 6366.280 | 0.531063 | 2.655 | 0.000 | -5.749 | bus power, rotor thrust, anchor cable reach |  |
| P10000 | 15 | record | as drawn | WATER_FILL | 3846.724 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach |  |
| P10000 | 15 | record | as drawn | WATER_RELEASE | 6096.900 | 1.000000 | 35.367 | 0.000 | 0.026 | bus power, rotor thrust |  |
| P10000 | 15 | record | as drawn | BUOYANCY_ESCAPE | 6096.904 | 0.000000 | 35.367 | 0.000 | 0.008 | bus power, rotor thrust |  |
| P10000 | 15 | record | as drawn | RETURN_TRANSIT | 4994.044 | 0.000000 | 37.367 | 30.694 | 0.000 | rotor thrust |  |
| P10000 | 15 | favourable | as drawn | SOURCE_APPROACH | 6366.280 | 0.531063 | 2.655 | 0.000 | -5.749 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P10000 | 15 | favourable | as drawn | WATER_FILL | 3846.724 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P10000 | 15 | favourable | as drawn | WATER_RELEASE | 6096.900 | 1.000000 | 35.367 | 0.000 | 0.026 | bus power, rotor thrust, aerodynamic coefficient |  |
| P10000 | 15 | favourable | as drawn | BUOYANCY_ESCAPE | 6096.904 | 0.000000 | 35.367 | 0.000 | 0.008 | bus power, rotor thrust, aerodynamic coefficient |  |
| P10000 | 15 | favourable | as drawn | RETURN_TRANSIT | 3959.850 | 1.000000 | 45.512 | 10.833 | 0.000 | bus power, rotor thrust, aerodynamic coefficient |  |
| P10000 | 60 | record | as drawn | SOURCE_APPROACH | 6250.297 | 0.531063 | 2.655 | 0.000 | -5.749 | bus power, rotor thrust, anchor cable reach |  |
| P10000 | 60 | record | as drawn | WATER_FILL | 3742.576 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, anchor cable reach |  |
| P10000 | 60 | record | as drawn | WATER_RELEASE | 6096.900 | 1.000000 | 59.801 | 0.000 | 0.026 | bus power, rotor thrust |  |
| P10000 | 60 | record | as drawn | BUOYANCY_ESCAPE | 6096.903 | 0.000000 | 59.801 | 0.000 | 0.014 | bus power, rotor thrust |  |
| P10000 | 60 | record | as drawn | RETURN_TRANSIT | 4518.750 | 0.000000 | 61.801 | 30.694 | 0.000 | rotor thrust |  |
| P10000 | 60 | favourable | as drawn | SOURCE_APPROACH | 6250.297 | 0.531063 | 2.655 | 0.000 | -5.749 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P10000 | 60 | favourable | as drawn | WATER_FILL | 3742.576 | 0.300000 | 8.333 | 0.000 | 0.000 | bus power, rotor thrust, aerodynamic coefficient, anchor cable reach |  |
| P10000 | 60 | favourable | as drawn | WATER_RELEASE | 6096.900 | 1.000000 | 59.801 | 0.000 | 0.026 | bus power, rotor thrust, aerodynamic coefficient |  |
| P10000 | 60 | favourable | as drawn | BUOYANCY_ESCAPE | 6096.903 | 0.000000 | 59.801 | 0.000 | 0.014 | bus power, rotor thrust, aerodynamic coefficient |  |
| P10000 | 60 | favourable | as drawn | RETURN_TRANSIT | 3896.501 | 1.000000 | 94.381 | 10.833 | -0.000 | bus power, rotor thrust, aerodynamic coefficient |  |

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

## Closed: served figures use quasi-static feasible plans

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

Closed on 2026-10-03. The monitor plans each mission at its exact leg distance, full wind input and shown mode; record basis is the default, with the same controls on the favourable basis beside it. Missing wind is labelled and uses still air. A mission without an accepted plan stands down and contributes no rate. The worked examples and ruled page sentences are generated and checked. Requested water, water kept aboard, energy supplied and water delivered remain distinct.

The interim labels are retired. Earlier report text remains dated history under its superseded-report warning; unsupported prescribed profiles remain diagnostic analysis. The model's structural, transient-control and hardware assumptions remain open. No aircraft has flown.

<!-- energy:open-limits:start -->
## Endurance frame: what mission can the stores support?

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

Closure needs an authorised mission horizon and terminal state, a usable state-of-charge window, an operational reserve, a recharge schedule and a thermal policy. Each must be supplied before endurance can become a gate.

| Component | What closes it | What it moves |
|---|---|---|
| Mission horizon | Name cycles, base transit, holding, standby, abort/return and terminal state; the director sets the requirement | Availability, sustained rate and completion acceptance |
| Usable storage and initial state | Pack tests and BMS limits for initial SoC, usable window, health, losses and power versus SoC/temperature; account for initial nitrogen and integrate both inventories | Permitted energy, storage mass and rejected cycles |
| Reserve | A named contingency trajectory with force, power, energy and a terminal state; distinguish contingency reserve from the protected pack floor | Dispatch availability and return/termination acceptance |
| Recharge | Installed source schedule, charger rating/efficiency, charge acceptance, hotel/cooling power, nitrogen production and turnaround; conserve both stores over repeated cycles | Recovery time, repeated-cycle availability and sustained rate |
| Thermal policy | Measured electrical/thermal pack parameters, initial and ambient temperature, cooling and derating, charge/discharge limits and abort thresholds | Sustained power, energy, cooling mass and accepted duty cycle |

The accounting structure is supported by [Welstead, NASA/TM-20230011630 (2023)](https://ntrs.nasa.gov/citations/20230011630), printed pp.5-7 / PDF pp.9-11, Table 1.
Mission and reserve definition are illustrated by [Johnson and Silva (2022)](https://ntrs.nasa.gov/citations/20210026170), printed pp.66-67 / PDF pp.8-9, sections 4 and 4.1.
Duty-cycle voltage, temperature and health validation are supported by [Bills et al.](https://arxiv.org/abs/2008.01527), PDF pp.4-5 and 7-8.
Their pack and mission examples are not values adopted for this vehicle; no endurance horizon, reserve or thermal threshold is invented here.

## Necessary stored energy, ideal accounting

These plans close only in the quasi-static force-and-bus model. Vertical dynamics, suspended-load control and sufficient stored energy for mission completion remain unestablished.

Ideal, lossless chronological accounting with nominal class storage fully usable and the plan initial nitrogen inventory charged. No losses, health, state-of-charge window, reserve, external recharge or thermal limit. This is not an endurance rule, a mission-completion verdict or a battery model. Solar and nitrogen recovery are the existing bus inputs, not a promised recharge system.

Integrate the existing drawAt electrical.batteryPowerMW at 2000 midpoint samples per phase, in PHASES order. Record cumulative draw at every phase end; interpolate the first nominal-storage crossing inside its sample.

| Captured mission or printed profile | Class / km / basis | Draw MWh | Nominal storage MWh | First empty min | Shortage MWh | Pages |
|---|---|---|---|---|---|---|
| energy-profiles row 6 asDrawn | P1000 / 60.000000 / record | 139.3 MWh | 120 MWh | 85.4 min | 19.3 MWh | research/analysis/energy-profiles.md; research/analysis/energy-requirements.md; docs/ENERGY-MODEL-2026-10.md; docs/ENERGY-CLOSURE-2026-10.md; docs/PHYSICS.md; sim/README.md |
| energy-profiles row 7 asDrawn | P1000 / 60.000000 / favourable | 140.1 MWh | 120 MWh | 85.1 min | 20.1 MWh | research/analysis/energy-profiles.md; research/analysis/energy-requirements.md; docs/ENERGY-MODEL-2026-10.md; docs/ENERGY-CLOSURE-2026-10.md; docs/PHYSICS.md; sim/README.md |
| power-and-thrust requirement (nominal class energy capacity) | P1000 / 60.000000 / record | 246.0 MWh | 120 MWh | 64.8 min | 126.0 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / record | 139.2 MWh | 120 MWh | 85.4 min | 19.2 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / record | 139.3 MWh | 120 MWh | 85.4 min | 19.3 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / record | 139.5 MWh | 120 MWh | 85.3 min | 19.5 MWh | research/analysis/energy-requirements.md |
| power-and-thrust requirement (nominal class energy capacity) | P1000 / 60.000000 / favourable | 175.3 MWh | 120 MWh | 74.8 min | 55.3 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / favourable | 140.0 MWh | 120 MWh | 85.1 min | 20.0 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / favourable | 140.1 MWh | 120 MWh | 85.1 min | 20.1 MWh | research/analysis/energy-requirements.md |
| prescribed drag sweep | P1000 / 60.000000 / favourable | 140.3 MWh | 120 MWh | 85.0 min | 20.3 MWh | research/analysis/energy-requirements.md |
| prescribed rotor-efficiency sweep | P100 / 60.000000 / record | 23.6 MWh | 20 MWh | 97.5 min | 3.6 MWh | research/analysis/energy-requirements.md |
| prescribed rotor-efficiency sweep | P1000 / 60.000000 / record | 140.1 MWh | 120 MWh | 84.9 min | 20.1 MWh | research/analysis/energy-requirements.md |
| prescribed rotor-efficiency sweep | P1000 / 60.000000 / record | 139.3 MWh | 120 MWh | 85.4 min | 19.3 MWh | research/analysis/energy-requirements.md |
| prescribed rotor-efficiency sweep | P1000 / 60.000000 / favourable | 143.3 MWh | 120 MWh | 83.8 min | 23.3 MWh | research/analysis/energy-requirements.md |
| prescribed rotor-efficiency sweep | P1000 / 60.000000 / favourable | 140.1 MWh | 120 MWh | 85.1 min | 20.1 MWh | research/analysis/energy-requirements.md |
| ready selector | P1000 / 400.000000 / record | 322.3 MWh | 120 MWh | 233.6 min | 202.3 MWh | concept/energy-analysis.html |

Of 20 captured cycles, 0 exceed nominal storage; every other captured cycle stays inside it for one ideal cycle. The full JSON records cumulative draw in phase order for 926 deduplicated current profiles, including unsupported paths as diagnostics and every shortage found. Earlier historical cells, the payload-exchange study and static component-only scans are outside this planCycle storage diagnostic. Current prescribed, selected, full-delivery, coefficient, single-input, requirement, descent and served-candidate profile tables are covered, including unsupported paths as supplied-effort diagnostics. Initial nitrogen is charged storage, not free energy. The 400 km P1000 ready-selector result is printed on concept/energy-analysis.html; it is outside the worked-example slider range.

Records: `research/analysis/energy-necessary.json`; generator: `research/analysis/energy-necessary.mjs`. No operational horizon or completion gate is added.

## Shape-specific added mass: what coefficient belongs to the capsule?

Closure needs a capsule-specific potential-flow solution at the configured geometry, followed by unsteady, viscous, appendage and attitude evidence and experimental validation.
The current spheroid surrogate and sensitivity pair are not measured capsule data. Local density and displaced volume must remain explicit.
A measured coefficient or tensor would move signed force demand, permissible acceleration, replan time and integrated energy, then any authorised dynamic acceptance.
Source: [Munk, NACA Report 184](https://ntrs.nasa.gov/citations/19930091249), Table I, printed p.20 / PDF p.21.

## Bag and cable: what load history reaches the hull?

Closure needs rigid-body hull and load equations, a taut cable with prescribed winch length, an elastic one-sided tension law for peak loads and pendulum coordinates for lateral motion.
Needed inputs are bag geometry and immersion, water-flow and entrained mass, cable stiffness, damping and slack, initial swing and winch speed ramps. They are unknown.
It would move cable and winch sizing, power, hull control demand, pickup/transfer limits and accepted profiles.
Source: [Cicolani and Kanning, NASA TP-3280](https://ntrs.nasa.gov/citations/19930003627), section 3, eqs.9b and 10; Figure 3, printed p.15 / PDF p.23.

## Dynamic replan: what trajectory and load schedule can close together?

Closure needs a search of altitude acceleration, climb/letdown timing and airspeed, release-rise timing, rotor thrust schedule and bag pickup/tension/winch schedule together, while preserving endpoints, cable reach and requested water.
Check signed force in both directions, bus draw, actuator rates, coupled load limits and both sides of joins over the same chronological history. A C1 altitude join alone does not establish realizable acceleration or thrust response.
Check initial stores, usable energy, reserve, recharge and thermal policy when an endurance frame is authorised. Publish both successful and failed searches.
This would move mission profiles, cycle minutes, rates, peaks and energy, and ultimately an authorised completion predicate. A release-only time change cannot establish full-cycle cost without bag and actuator inputs; no replanning count or universal time/energy factor is asserted here.
<!-- energy:open-limits:end -->

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

**Current rope correction:** the paragraph above is archived history. This correction withdraws its earlier diameter and omission claims.

<!-- anchor-rope:basis:start -->
Illustration: the dry-mass budget sizes an assumed UHMWPE cable by minimum break strength, not by diameter. Design load including pickup is bag-water weight under the quasi-static pickup assumption; dynamic snatch, cable self-weight and bag/rigging dry weight are omitted. Required minimum break strength is that load times the safety factor. Assumption: credible safety factor 5; assumption: floor safety factor 3; assumption: demonstrated safety factor 7. Assumption: credible minimum-strength-per-linear-density coefficient 1.5 MN per kg/m; assumption: floor coefficient 2.0 MN per kg/m; assumption: demonstrated coefficient 1.4 MN per kg/m. Those columns do not qualify a rope product. The bottom-up dry-mass budget charges the installed cable, bag and winch. The flight model still assumes dry mass equals payload; it does not integrate that equipment bill. Terminations, wear, creep, cyclic pickup and the bag load path remain unqualified. See `research/analysis/mass-budget.py` and its generated records.
<!-- anchor-rope:basis:end -->

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

<!-- solar:budget-reference:start -->
Earlier enlarged-hull figures on this page retain the preceding power-input publication. The existing P-100 0.508 kg/m³ sizing routine now returns 510,406 m³, against the earlier 457,324 m³, on the current model after the projected solar-area correction. Other integrated model corrections can also contribute. This is a diagnostic comparison, not validation of the closure condition. See the [generated before/after budget comparison](../research/analysis/mass-budget.md#solar-input-sensitivity-of-the-existing-budget-diagnostic).
<!-- solar:budget-reference:end -->
