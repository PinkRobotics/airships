# Open questions

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

Six things are wrong, or unjustified, or dead: five of them in the model, and one — the
Esri basemap, item 5 — in the page that displays it. They are written up here rather than
quietly fixed because each one changes a number the site publishes or a decision it has to
make before going public, and because two of them are not really bugs at all — they are
decisions about the vehicle that have been made by accident and should be made on purpose.

Each entry gives the defect, what it costs, the options, and a recommendation. The numbers
were produced by re-running the model, and by an independent Python replication that
reproduces `tests/golden/seed7-snapshot.json` exactly.

Items 2 and 3 have a test in `tests/cases/` marked `knownFail`. Those tests run. They fail.
If one starts passing without this document changing, the suite fails on that too — a
defect should not be able to lose its excuse quietly. There are three `knownFail` markers
left; the third is an unrelated flag bug, `plan · windUsed is false when the wind was not
applied`, which is too small to have an entry here. Item 1 had the fourth. It started
passing on 2026-08-09, which is what a fix looks like from the suite's side, and the marker
was converted into two ordinary tests that assert the corrected behaviour rather than
deleted: `physics · FAIL-SAFE FLOAT-UP` and `physics · UNPOWERED RECOVERY`.

Items 4, 5 and 6 have no such marker, and cannot have one. `retainedT` being zero is
*enforced* by `selftest.js`, so a test that failed on it would be asserting the opposite of
the specification; the Esri problem is not a model behaviour; and no assertion can fail
because a term is absent from a sum. Those three are held to ordinary passing tests that
record what the code does, and to this page.

`docs/PHYSICS.md` §11 quantifies the same set, but numbers them differently: its Defects 4
and 5 are the two halves of item 4 below, its Defect 6 is item 6, and item 5 has no entry
there because it is not physics.

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
every rotor calculation — ISA at about 990 m, against a working altitude of 2,500 m. Drag is
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

**It costs throughput, and that is the point.** The P-10000's 15 km balanced cycle delivers
8,943.7 t instead of 10,000, at 10,821 t/h instead of 12,052, for 88.17 MWh instead of 75.58.
Roughly 10% of the headline figure was being claimed by checking the hardest manoeuvre in air
the ship never lands in. The published numbers now carry the price of getting back down.

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

## 5. Esri basemap tiles

`app/map/basemap.js` fetches satellite tiles directly from `server.arcgisonline.com` with
no API key, from the visitor's browser. This sends every viewer's IP address and precise
viewport to a third party with no consent step, and it is very likely outside Esri's terms
of use for that endpoint.

It also sits oddly beside a stated principle of this project: the wildfire feeds are mirrored
first-party precisely so that traffic to this page does not become traffic to someone
else's service.

This is the one item on this page that is not a defect in the model. It is here because it
has to be decided before the repository is public, not because the arithmetic depends on it.

**Options:** drop the imagery layer; obtain an Esri key and use it within terms; or switch
to an openly-licensed basemap. See `DATA-SOURCES.md` §6.

**DECISION: resolve before the repository is public.** Publishing the technique is worse
than using it.

**Recommendation.** Decide before the repository is public, because publishing the
technique is worse than using it.

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
`rtLN2` = 0.50 a full tank is worth 34.9 / 349 / 3,489 MWh of expansion energy — 1.7 times a
P-100's battery, 2.9 times a P-1000's, 1.7 times a P-10000's. So the store is the same order
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

*Found in review round 1 (codex), 2026-08-09.*

---

## What is not on this list

The model does not attempt weather beyond a single wind vector, turbulence, fire behaviour,
water's actual effect on a fire, air traffic, airspace, regulation, manufacturing or cost.
Those are not defects; they are the boundary of the thing. `docs/PHYSICS.md` says where
that boundary is drawn and why.
