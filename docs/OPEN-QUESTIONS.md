# Open questions

Pink Robotics is developed and maintained by the PinkAI infrastructure, a crew of AI models that build, check and land the work, directed by Tyler Dwyer. See the [work log](https://pinkrobotics.ca/log/). The work log names the model behind each change it records, from 1 October 2026; earlier work predates that record.

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
> | #0, #4 | **The cryogenic plant CANNOT be deleted** — a sealed-cell hull has no way to ballast with air, and an earlier claim that it could is retracted. But the ship makes nitrogen on every cycle it does not need, at **52.5%** of the P-100's cycle energy. | `air-ballast.md` |
> | #3, #14, #15 | **The letdown is understated by 30–54×.** Corrected, cycle energy rises 50–92%. The anchor saves 4.7–49.2%, not the 96% claimed, because the cable is in the water for only 4–46% of the fall. | `descent.md` |
> | #8 | **Re-opened with a purpose.** `diskM2` was retired as inert on a measurement taken against a letdown 53× too small. Doubling the disc saves 9.9% of the cycle. | `descent.md` |
> | #12 | **`ALT.drop` = 450 m does not deliver water** — and the ship's own rotors push air *upward* at 86× the mass flow of the water. The answer is sprayer leads. Measured in line rather than tonnes, one P-100 could wet the perimeter of 91.4% of BC campaign fires daily. | `delivery.md` |
>
> Regenerate all of it with `make analysis`.
>
> **2026-10-02 correction to #11:** the conditional capsule budget now gives 355,499 m³ and 129 m length. This is equipment-budget closure under an assumed shell density, not a checked design.
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
> delivery cycle than it was. #2, #3, #5 and #6 are still open.

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

Items 2 and 3 have a test in `tests/cases/` marked `knownFail`. Those tests run. They fail.
If one starts passing without this document changing, the suite fails on that too — a
defect should not be able to lose its excuse quietly. There are three `knownFail` markers
left; the third is the flag bug in #17, `plan · windUsed is false when the wind was not
applied`. Item 1 had the fourth. It started
passing on 2026-08-09, which is what a fix looks like from the suite's side, and the marker
was converted into two ordinary tests that assert the corrected behaviour rather than
deleted: `physics · FAIL-SAFE FLOAT-UP` and `physics · UNPOWERED RECOVERY`.

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

## 2. Two power models that disagree by 2.5×

`planCycle` builds an energy budget for a cycle. `stateAt` independently reports a
per-system power draw at each instant, and the page integrates that draw to drain the
batteries. They are separate implementations of the same quantity and they do not agree:

| class | planned (MWh/cycle) | integrated (MWh/cycle) | ratio |
|---|---|---|---|
| P-100 | 1.7 | 2.0 | 1.19× |
| P-1000 | 11.9 | 20.8 | 1.75× |
| P-10000 | 82.5 | 211.2 | 2.56× |

Of the integrated 211 MWh for a P-10000, **161 MWh is rotors**. Endurance therefore reads
9.1 hours on the page and 27.2 hours in the plan.

The root cause is identified: the rotor power terms apply **hover momentum theory at
36 m/s cruise**. Induced power falls with forward speed; using the hover expression at
cruise overstates it by about **6.4×** against the standard Glauert correction. The planned
budget avoids the error mostly by not modelling the same holds.

**Options**

| | Effect |
|---|---|
| a. One model: delete the budget, integrate the draw | Structurally right — one number, computed once. Publishes 211 MWh, and the energy deficit gets much worse. |
| b. One model: delete the draw, publish the budget | Keeps the headline figures; loses the per-system instrument readings that make the page worth looking at. |
| c. Fix the physics first, then unify | Add the forward-flight correction so induced power is right at cruise, then make `stateAt` report the same model `planCycle` sums. Both numbers move, and they move towards each other. |

**DECISION: (c).** Fix the hover-at-cruise error first, then make the instruments and the
budget the same code.

**Recommendation: (c).** The disagreement is a symptom; the hover-at-cruise error is the
disease, and it is a real physics error that a reader will find. Fix it, then make the
instruments and the budget the same code — the project's own rule everywhere else.

---

## 3. Half the energy comes from an unexplained constant

The letdown term in `planCycle` is

```js
E.letdown = downMW * Math.min(6, dur.RETURN_TRANSIT * 0.2) / 60;
```

It is **52.9% of the P-10000's published cycle energy** at 15 km, and 61.3% at 45 km.
Neither `6` nor `0.2` is justified anywhere. The `min` is inactive below roughly 55 km
one-way, so in practice the term is a bare 20% of the return leg, and past 55 km the
letdown energy simply stops growing with distance, which is not a physical behaviour.

Worse, the `battLimited` branch stretches `RETURN_TRANSIT` by 1.12 to model "a longer,
shallower letdown" — and because the term is proportional to duration, it **raises**
letdown energy from 38.95 to 43.62 MWh. The code does the opposite of what its comment says.

**DECISION: fix it.** Replace the constant with a descent model derived from the disk
theory already in the file. No free constants, and the `battLimited` branch must reduce
letdown energy rather than raise it, as its comment claims.

**Recommendation.** Replace it with a descent model: the energy needed to push a buoyant
hull down through a known height at a chosen rate is computable from the same disk theory
already in the file, and it has no free constants. Until then the largest single line in
the energy budget is a guess.

---

## 4. Retained descent ballast is dead, and so is the cryogenic plant — BALLAST FIXED 2026-08-09

`retainedT` is **0 for all 135 combinations** in the golden file — every class, every mode,
every distance, every wind. The force balance always closes without holding water back, by
a margin of +122% (P-100), +9% (P-1000) and +5% (P-10000). A 7.5% cut in bus power × prop
efficiency, or a 14.3% cut in disk area, would start the P-10000 retaining.

The cryogenic ballast plant is similarly inert: it is cryo-rate-limited to 1.8 t, 7.5 t and
21.1 t on a 15 km balanced return leg, against tanks of 50, 500 and 5,000 t. The P-10000
makes 0.42% of the ballast the same function asks for, and `cryoLimited` is true for every
class at every distance the fleet can fly, so the flag carries no information.

Both are described in the prose as working parts of the vehicle. `passes` is likewise 3 in
all 135 combinations, which makes it a constant wearing a formula.

**DECISION (revised 2026-08-09): KEEP both, and make them bind.**

Retained descent ballast and the cryogenic plant stay in the design. If holding water back
or carrying LN₂ costs longer cycles or more power, that is the honest price and the
published throughput should carry it. What is not acceptable is a doctrine described in the
prose that never changes an outcome in the code.

Both changes above push on this: a hull sized for fail-safe float-up (#1) is more buoyant
and needs more holding down, and bounding N₂ output by the ballast actually aboard (#6)
couples the cryogenic plant to something that matters. Re-measure after both, and if
retention still never binds, tighten until it does rather than deleting it.

**RE-MEASURED after #1, 2026-08-09. It went the wrong way.** The prediction above is wrong,
and the reason is worth keeping. A hull sized for fail-safe float-up is more buoyant *at sea
level*, where it never is. At the altitude the surplus is now measured at it is LESS buoyant
than the sea-level ledger claimed: 110.5 / 1,105 / 11,051 t against 120.5 / 1,205 / 12,050 t.
`rotorMaxT` did not move, so the headroom widened rather than closing:

| | rotorMaxT/0.6 | surplus, was | surplus, now | headroom, was | headroom, now |
|---|---:|---:|---:|---:|---:|
| P-100 | 267.2 t | 120.5 t | 110.5 t | +122% | +142% |
| P-1000 | 1,318.1 t | 1,205.0 t | 1,105.1 t | +9% | +19% |
| P-10000 | 12,666.2 t | 12,050.0 t | 11,050.9 t | +5% | +15% |

`retainedT` is still 0 in all 135 golden combinations, `passes` is still 3 in all of them,
and the P-10000's `battLimited` flag — which used to be true everywhere — is now false
everywhere, so a second flag has joined `cryoLimited` in carrying no information.

**RESOLVED 2026-08-09 by striking the balance at the source.** The descent check was being
made at the wrong altitude. `planCycle` used one ledger, at the working altitude, because
that is what float-up needs — but the letdown does not happen at the ceiling. It ends over
the lake at 1,300 m MSL, in air 16% denser, with the hull correspondingly more buoyant. Two
questions, two worst cases, one ledger between them.

`planCycle` now evaluates a second ledger, `ledLow`, at `TERRAIN_MSL + ALT.source`, and
everything that answers to descent reads it: how much nitrogen to make, how much water to
keep back, how hard the rotors work coming down. Float-up and the class table keep the
ceiling figure. The headroom that was comfortable at the ceiling is a shortfall at the lake:

| | rotorMaxT/0.6 | surplus at 2,500 m | surplus at 1,300 m | headroom, ceiling | headroom, lake |
|---|---:|---:|---:|---:|---:|
| P-100 | 267.2 t | 110.5 t | 137.4 t | ×2.42 | ×1.94 |
| P-1000 | 1,318.1 t | 1,105.1 t | 1,374.4 t | ×1.19 | **×0.96** |
| P-10000 | 12,666.2 t | 11,050.9 t | 13,743.6 t | ×1.15 | **×0.92** |

Below 1.0 the rotors cannot do it alone and the water stays in the tanks. **Retained ballast
is live**: 0 t on the P-100, 48.8 t on the P-1000, 1,056.3 t on the P-10000 — 10.6% of its
load — and both larger classes are descent-authority limited again. The doctrine in the prose
is now a mechanism in the code, and `retainedT`, `battLimited` and the bottleneck string all
carry information.

**It cost throughput until the anchor was added, and the anchor turned out to be worth more
than the problem it solved.** Striking
the balance honestly took the P-10000 from 12,052 t/h to 10,821, because 1,056 t of every load
stayed in the tanks to make the descent possible. Then the obvious question: what actually holds
a buoyant ship down? Not ballast it carries, makes, or keeps back — it borrows the lake. A bag on
a cable, filled at the surface and winched clear, is 12,400 t of downward force for the 15 m of
lift needed to break the surface, and it is dumped back where it came from once the tanks hold
more than the shortfall. A Bambi bucket at 1,265 times the largest ever built (9,800 L).

Delivery returns to 12,052 t/h with the whole load dropped. The three ways of closing the same
1,056 t gap, priced: anchor **0.11 MWh** at that size (0.60 once the bag is sized to do the whole
descent), a 1,350 m hose so the ship fills from altitude
**44 MWh** (2 m bore, 140 bar), liquid nitrogen **475 MWh** (or 5.8× the plant to do it in one
cycle). Retaining water costs no energy at all and 10% of the delivery, which is the one
currency this fleet cannot spend.

**And then the bag was sized for the job rather than for the gap.** Rotor power goes as
thrust^1.5, so load moved onto the lake comes off the bus faster than linearly. A bag carrying
90% of the hold instead of the 8% the shortfall required drops `downMW` from 1,748 MW to 52 and
the P-10000's cycle from 91.47 to **45.87 MWh** — 4.59 kWh per delivered tonne against 9.15
before any of this began. Every class carries one, including the P-100 whose descent closes on
rotors alone: it saves 29% for the same delivered water, and a fleet that has built the
technology should use it. Bags are 125 / 1,250 / 12,400 t; cables 350 / 600 / 850 m.

That has a consequence for #3. The letdown window was 45% of the cycle and is now 3.1%, so its
two unexplained constants no longer decide a published figure — its known-failure marker came
off. The defect is not fixed, it is defused, and the test says so.

A `descentShort` flag reports the wall: retention is clamped at the payload, because a hull
cannot keep back more water than it went to fetch, and reaching that clamp means nitrogen,
rotors and the whole load together do not close the descent. It is false everywhere in the
grid today. If it ever goes true the bottleneck string says so outright rather than quietly
delivering less.

The cryogenic plant is unchanged in the cycle: still 1.8 / 7.5 / 21.1 t on a 15 km balanced
return leg. What did change is that `cryoLimited` is now true for **every** combination in
the grid, including the single P-100 endurance 400 km case that used to fill its tanks — the
target rose with the honest surplus and the tank cap stopped binding first. So the flag is
now uninformative everywhere rather than almost everywhere. See #5 in `docs/PHYSICS.md`.

**Superseded first reading — re-measure, then make code and copy agree:** Both of
those changes push the margins the other way, so retention and the cryogenic plant may
become live on their own. Whatever is true afterwards is what the prose must say.

**Superseded recommendation** (kept because the outcome was neither branch): *Either the
doctrine is real and the margins should be tight enough for it to bind, or it is not and the
copy should stop describing it.* It bound, in the end, without tightening anything — the
margin was never the problem. The question was being asked at the wrong altitude, and the
answer changed as soon as it was asked where the manoeuvre happens. The ballast half of this
entry is closed; the cryogenic half is still open, and is now the only reason the plant is
not purely decorative in the mass budget.

---

## 5. Esri basemap tiles — FIXED 2026-10-01

Removed the Esri tile loader and satellite toggle. The bundled first-party terrain hillshade
is now the default backdrop, with outlined labels and markers and stronger water/perimeter
contrast. No Esri tiles are fetched or redistributed. See `DATA-SOURCES.md` §6.

The browser network gate (`tests/firstparty/check.py`, part of `make check`) records requests
for every served page in fixture-live, snapshot and absent-mirror modes and refuses external
hosts. The static gate checks loading positions separately. The server mirrors wind hourly;
missing agency mirrors fall back only to the dated files in this repository.

---

## 6. The generators supply peak power but no energy

Each class advertises onboard generation — 8, 40 and 150 MW — and `plan.js` counts it when
sizing rotor authority (`rotorMaxT` uses `battMW + genMW`). But nothing ever credits that
generation as *energy*. `stateAt` reports only solar and nitrogen recovery under
`gen`, and `app/loop.js` subtracts every remaining load straight from the battery.

So the vehicle is described as having generators, is given the thrust they would allow, and
is then flown as though they were not running.

The size of it, for the documented 15 km balanced case: the P-10000's cycle is 0.827 h, so
its generators running flat out would produce **124.0 MWh** against a published cycle spend
of 88.2 MWh — the generators alone would very nearly cover the cycle before solar is counted.

Generators do not run flat out, so the honest figure is demand-following output capped at
`genMW`. Measured that way against the sampled missions in `tests/golden/seed7-snapshot.json`
— which fly different legs from the 15 km case, so the numbers are not comparable with the
paragraph above — generation would contribute 0.74, 8.2 and 140.9 MWh per cycle
for the three classes. On those same missions the P-100 stops draining its battery and
begins charging, P-1000 endurance goes from 4.7 hours to 15.4, and P-10000 from 10.3 to 20.1.

Both calculations are of the same thing at different distances. Either one is enough to
show that the missing term is the same order as the entire budget.

This is the most consequential item on this page, because the deficit is a *conclusion* the
project draws in public: that every hull runs at a loss and therefore needs an energy-import
chain of tanker ships. That conclusion may be an artefact of not modelling the generators
the vehicle is said to carry.

**Options**

| | Effect |
|---|---|
| a. Dispatch the generators, with a fuel ledger | The honest version: generation is credited, fuel is consumed, fuel mass enters the mass ledger and eats into payload. The deficit probably becomes an endurance limit instead. |
| b. Remove the generators | If the intent is a solar-and-storage vehicle, then `genMW` must also come out of rotor authority, and the class cards and prose must stop mentioning generators. The published thrust figures fall. |

**DECISION (revised 2026-08-09, superseding the first reading below): KEEP the generators
and credit them as energy — they are the nitrogen plant, not a fuel burner.**

The onboard generation IS the N₂ expansion path: liquefy nitrogen when there is power to
spare, expand it back through a generator when there is not. That is why it stays. But it
also means this is **storage, not a source** — the round trip loses (`CFG.rtLN2` < 1), so
crediting it honestly makes the per-cycle deficit *larger*, not smaller. The model must
therefore bound expansion output by the LN₂ actually aboard, rather than treating `genMW`
as free continuous power the way `rotorMaxT` currently does.

*Updated 2026-08-09:* that bound is now a real number. `ln2CapT` is 155 / 1,550 / 15,500 t,
sized by unpowered recovery rather than picked, and at `eLN2` = 0.45 kWh/kg and
`rtLN2` = 0.20 a full tank is worth 13.95 / 139.5 / 1,395 MWh of expansion energy — 0.70 times a
P-100's battery, 1.16 times a P-1000's, 0.70 times a P-10000's. (At the old `rtLN2` = 0.50 those
read 34.9 / 349 / 3,489 MWh, which was the arithmetic of a store returning more work than the
liquid holds — see #10.) So the store is the same order
as the battery and the generators have something definite to run on. The plant still cannot
fill the tank inside a cycle, which is #5.

Alongside it:

  * **batteries grow on every class, most on the P-10000.** Their mass is bought at design
    time with more vacuum cells, so the displacement sizing in #1 and the storage sizing
    here are one calculation, not two.
  * **more rotor authority comes from the battery**, particularly for getting down.
  * **a hull that runs out of power may be unable to descend** until solar, N₂ expansion or
    a cell swap restores it. That is a real operating limit and it should be modelled and
    stated, not designed away.
  * **the energy equation is best-effort by design.** Fleet throughput depends on battery
    tender ships ferrying charged cells for discharged ones, swapped at mechanical speed.
    Named as the mechanism, deliberately unmodelled beyond that.

**Superseded first reading — (b), remove the generators:**

The resupply story is battery-cell swap: tender airships exchange depleted cells for charged
ones from a ground centre. That makes the vehicle battery-electric, and an onboard generator
is then an anomaly that exists only to inflate rotor authority.

So `genMW` comes out of the thrust budget and out of the class cards and prose. Solar stays.
The energy deficit stays and gets larger, which is now honest rather than accidental: the
deficit is the argument for resupply, and it should be stated as such.

Note two consequences. Removing `genMW` from `rotorMaxT` cuts descent authority, which is
what currently lets every class dump its whole payload with nothing retained — so #4 must be
re-measured afterwards, and retention may come back to life. And this pairs with #1: a hull
sized for fail-safe float-up is more buoyant, which needs *more* down-force, not less.

Cell swap is to be mentioned as a future direction only. No mass, rate or fleet-count model
for the tenders: the point of naming it is to close the story, not to open a second one.

**Recommendation, superseded by the decision above: (a).** Note that it is not free — fuel has mass, and mass is the entire
problem — which is exactly why it should be modelled rather than assumed either way.
Whichever is chosen, the two halves must agree: a generator that provides thrust must also
provide the energy for it, or provide neither.

*Identified during review, 2026-08-09.*

---

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

## 8. The disc area and the battery peak answer a question that is no longer asked

`diskM2` (160,000 m²) and `battMW` (1,400 MW) on the P-10000 were reverse-engineered so the force
balance would close with nothing held back: the rotors alone pushing an emptied hull back down
under its own buoyancy. That check was made at the CEILING. On 2026-08-09 it moved to the source,
where the letdown actually ends and the air is 16% denser, and there it does not close —
`rotorMaxT/0.6` is 12,666 t against a 13,723 t hold.

The descent is closed by the anchor now. These two numbers satisfy a superseded constraint.

What makes it a defect rather than a tidy-up is that they were still being published as evidence
for a property the model does not have: `sim/config.js` asserted closure in a comment, and
`docs/PHYSICS.md` §7 called it "the model's central structural boast" while computing its
supporting table against the superseded ceiling ledger. Both are corrected as of this entry.

And they are no longer load-bearing on anything. Measured: `diskM2` ±20% moves cycle energy by
∓0.4%; `battMW` ±20% moves **every published figure by 0.0%**. Two of the most striking numbers on
the class cards are inert.

**DECISION: none yet.** Re-deriving them needs a decision about what the primary rotors are
actually for now that the anchor does the descent — trim and cruise, or descent authority in
reserve for a bag that fails to fill. That is a design question, not a re-tune, and it is entangled
with the dedicated-propulsor question.

---

## 9. The solar skin needed 76% conversion efficiency — FIXED 2026-08-09

`sim/state.js` credited the skin a flat **200 W/m² of electrical output**, continuously, and every
sustainment number in this project rested on it: the generation side of PHYSICS §9's deficit table,
the endurance figures, the storage gauge, and the public conclusion that the fleet is a battery
being spent rather than a perpetual machine.

NRCan's dataset gives **6.34 kWh/m²/day** mean July horizontal insolation averaged across eight BC
interior fire-belt towns. That is 264 W/m² *incident*, day-averaged. Getting 200 W/m² of
electricity out of it required **76% conversion** — three and a half times the best cell ever made
in a laboratory.

**DECISION: taken. `CFG.solarWPerM2 = 45`.**

    264 W/m² incident × 0.21 flexible module × 0.81 (curvature, cell temperature, soiling,
    conversion) = 45 W/m² electrical, 24-hour averaged, on a PROJECTED area.

`solarM2` is 80–87% of each hull's plan ellipse, so it is a projected area and horizontal
insolation applies to it directly — the curvature is paid for once, in the area, and the 0.81
covers what is left. What moved:

| | solar | per cycle | deficit | endurance |
|---|---|---|---|---|
| P-100 | 1.20 → **0.27 MW** | 0.68 → **0.15 MWh** | 0.32 → **1.10** | 35.4 → **10.4 h** |
| P-1000 | 5.60 → **1.26 MW** | 3.30 → **0.74 MWh** | 3.09 → **6.66** | 22.9 → **10.6 h** |
| P-10000 | 24.00 → **5.40 MW** | 18.20 → **4.10 MWh** | 24.81 → **41.77** | 61.1 → **36.3 h** |

**Three things this exposed that are worth more than the correction.**

First, the constant was written out in **five separate files** — `sim/state.js`, `sim/selftest.js`,
`app/cockpit/panels.js`, `tools/figures_dump.js` and `3d/model/metadata.js` — and wrong in every
one. A duplicated constant is wrong everywhere or nowhere. There is now one `CFG.solarWPerM2`, one
`ASSUMPTIONS.solarWPerM2` on the far side of the `3d/` boundary, and a parity test that reads both.

Second, **no published figure moved.** Generation is not in `planCycle`'s ledger, so cycle energy,
throughput and kWh/t are all bit-identical across a 4.4× correction to the vehicle's power supply.
That is Defect 6 stated as sharply as it can be: a term missing from a sum cannot be caught by a
test, and this one went a day being wrong by a factor of four without a single assertion noticing.

Third, **it makes the project's conclusion stronger.** A P-100 with ten hours in it is
unambiguously a battery being spent. The honest number was the more useful one.

*Still open:* the figure is a 24-hour average, which is right for energy over a cycle and wrong for
power at an instant — there is no sun at 03:00 and the storage gauge draws 45 W/m² of it anyway.
Fixing that needs a diurnal term the model does not have.

---

## 10. `rtLN2` recovered more work than the nitrogen contained — FIXED 2026-08-09

`rtLN2 = 0.50` said half the 0.45 kWh/kg spent liquefying nitrogen came back as electricity —
**225 kWh per tonne**. The physical exergy of liquid nitrogen at 1 bar against a 288 K ambient is
**173.4 kWh/t** (Arnaiz-del-Pozo et al. 2020, corroborated independently at 205–214 kWh/t under
more favourable assumptions).

So the recovery term returned 1.3× the work thermodynamically available in the liquid, before any
turbine, heat exchanger or generator efficiency. Not an optimistic efficiency — a violation, and
it was on the page.

It was also the line this project's own accounting bug had been hiding: until earlier the same day
the recovery was netted against the pump bill inside a `max(0, …)`, so on the two smaller classes
it silently deleted the entire pumping cost. Splitting the lines exposed the credit, and exposing
it is what made it checkable.

**DECISION: taken. `rtLN2 = 0.20`** — 90 kWh/t, 52% of the exergy. That is about what a cryogenic
expander returns with no external heat source, and consistent with liquid-air storage plant that
reaches 50–60% round trip only by recycling waste heat this vehicle does not have. The hard ceiling
is 173.4/450 = **0.385**, and `spec-parity.cases.js` now fails the build if `rtLN2 × eLN2 × 1000`
ever exceeds 173.4 in either copy of the constant. A second law is not a tuning bound.

Cost: `E.recovery` fell from −4.751 to −1.900 MWh and the P-10000's cycle rose 43.019 → **45.869**.
The nitrogen store is now worth 4.1% of a cycle rather than 11.0%, and `rtLN2` ±20% moves the
headline by ±0.8% instead of ±2.2%.

---

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

## 14. The rotor power model cannot see the anchor

`sim/plan.js` credits the bag: the residual the rotors must hold is `holdT − anchorT`, and
`downMW` comes out at **52.3 MW**. `sim/state.js` does not. `draw.rotors` is built from
`led.liftT − massT` with no anchor term at all, and `plan.anchorT` enters the function only
*after* the rotors are computed — because `anchorHang` needs the ground speed, which is settled
later. The ordering is the evidence it was never considered.

Measured on the seed-7 P-10000 mission, `SOURCE_APPROACH`:

| prog | altitude AGL | anchor | `draw.rotors` | with the bag credited |
|---|---|---|---|---|
| 0.00 | 820 m | 0 t | **1,472.5 MW** (clamped at the bus) | — |
| 0.90 | 329 m | 12,400 t | 155.3 MW | ~4.7 MW |

At prog 0.90 the same returned object reports 121.6 MN of lake water pulling the hull down *and*
155 MW of rotor thrust also pushing it down, computed against the full 13,722 t surplus. **The
instrument over-reads by about 33× at the moment the mechanism is doing its job**, and the
`Math.min(bus × 0.95, …)` clamp then hides the overflow behind a bus pinned at its limit.

This is not #2's hover-formula error — the ship is at 0–39 km/h here, where momentum theory is
the right model. It makes #2 worse than #2 says: that entry reports the P-10000 diverging 2.56×,
and measured today it is **5.05×** (192.1 MWh integrated against 38.0 planned).

**DECISION: none yet.** The fix is to compute the anchor before the rotors, which means
restructuring how ground speed is settled in `stateAt`. It should be done with #2 rather than
before it.

---

## 15. The letdown is priced at the anchor-assisted residual for the whole descent

`E.letdown = downMW × window`, and `downMW` is the *bagged* residual — 52.3 MW. But the plan's own
`anchorFromAglM` says the bag is not available above 750 m AGL, and the cable cannot reach the
water above about 950 m. Priced with the model's own `ledger` and `diskMW`:

| altitude AGL | hold | rotors alone | with the bag |
|---|---|---|---|
| 1,500 m | 11,030 t | 1,260 MW | 0 MW |
| 1,000 m | 12,122 t | 1,451 MW | 0 MW |
| 750 m | 12,684 t | **1,553 MW** — over the 1,550 MW bus | 5.2 MW |

`E.letdown` for the whole cycle is 1.42 MWh, which is 1,451 MW for 3.5 seconds. `stateAt` agrees
with the table rather than the ledger: its peak rotor draw in the return leg is 1,472.5 MW.

Distinct from #3, which is about the undefined `6` and `0.2` constants: **even with a perfect
window, `downMW` is the wrong power for most of the descent.** #14 and #15 are two halves of one
fact — neither model prices the descent, and they disagree by 20–30× in the phase the anchor was
invented for.

**DECISION: none yet.**

---

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

## 17. `windUsed` claims wind without a route bearing

**Reproduced 2026-10-01. Open: the fix is one line, and it lands with the energy model change,
which rewrites the same function.** For P-1000, balanced mode, 40 km and
`{ spd: 40, dir: 270, bearing: null }`, `planCycle` returns the same ground speeds as still air
(110 km/h each) and `tailOut: 0`, but `windUsed: true`. The guard that applies the wind in
`sim/plan.js` requires a speed and a bearing; the returned flag checks only the speed. The
executable case is `plan · windUsed is false when the wind was not applied` in
`tests/cases/sim-plan.cases.js`, marked `knownFail`.

It is harmless on the live page today, because the mission code always sets a bearing before
planning. It is still a flag that can lie, and the cockpit reads it to decide whether to say that
wind was applied.

The correction is `!!(wind && wind.spd != null && wind.bearing != null)`, matching the guard, after
which the known failure becomes an ordinary test.

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

**Reproduced 2026-10-01. Open: the sentence is rewritten when the float ledger lands.** The
engineering page says that structure per litre falls as the vessel grows, and that scale is the
lever. From a bench cell to a ship that is true: the bench article carries 15.1 kg of structure per
cubic metre enclosed, and Ship 0 carries 2.19 on the record basis and 1.25 in the best defensible
world, against 1.225 kg of sea-level air.

Across ship sizes the model says the opposite. `SHIP.floatWindow` and `SHIP.floatWindowFrame` in
`ship/catalog.js`, both computed by `ship0Summary()` in `ship/model.js`, give lift over mass at
sea level by hull diameter:

| basis | 40 m | 44 m | 48 m | 52 m | 56 m | 60 m | 68 m | 80 m |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| record | 0.585 | 0.582 | 0.577 | 0.558 | 0.543 | 0.532 | 0.508 | 0.455 |
| best defensible world | 0.956 | 0.987 | 0.953 | 0.981 | 0.969 | 0.969 | 0.957 | 0.916 |

On the record basis the ratio falls at every step as the hull grows. In the best defensible world
it wanders between 0.953 and 0.987 up to 60 m and falls above it. Nothing in the range floats.

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

---

## Interim energy figures: earlier model, under review

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

The figures will be published old and new, with the reason for each change, when the corrected model lands. The interim labels change no calculation.

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
