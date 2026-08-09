# Open questions

> **DECIDED 2026-08-09.** All six are to be fixed. The decisions are recorded at the top of
> each entry as **DECISION**, and they change what "correct" means, so read them before
> touching the arithmetic. Three of them interact: making the hull buoyant fully loaded
> (#1) changes the force margins that make retention dead (#4), and removing the generators
> (#6) changes them again in the other direction. Do #1 first, then #6, then re-measure #4
> before deciding it is still dead.

Six things are wrong, or unjustified, or dead: five of them in the model, and one — the
Esri basemap, item 5 — in the page that displays it. They are written up here rather than
quietly fixed because each one changes a number the site publishes or a decision it has to
make before going public, and because two of them are not really bugs at all — they are
decisions about the vehicle that have been made by accident and should be made on purpose.

Each entry gives the defect, what it costs, the options, and a recommendation. The numbers
were produced by re-running the model, and by an independent Python replication that
reproduces `tests/golden/seed7-snapshot.json` exactly.

Items 1, 2 and 3 have a test in `tests/cases/` marked `knownFail`. Those tests run. They
fail. If one starts passing without this document changing, the suite fails on that too —
a defect should not be able to lose its excuse quietly. There are four `knownFail` markers
in all; the fourth is an unrelated flag bug, `plan · windUsed is false when the wind was
not applied`, which is too small to have an entry here.

Items 4, 5 and 6 have no such marker, and cannot have one. `retainedT` being zero is
*enforced* by `selftest.js`, so a test that failed on it would be asserting the opposite of
the specification; the Esri problem is not a model behaviour; and no assertion can fail
because a term is absent from a sum. Those three are held to ordinary passing tests that
record what the code does, and to this page.

`docs/PHYSICS.md` §11 quantifies the same set, but numbers them differently: its Defects 4
and 5 are the two halves of item 4 below, its Defect 6 is item 6, and item 5 has no entry
there because it is not physics.

---

## 1. Lift is bought at sea level and spent at altitude

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

## 4. Retained descent ballast is dead, and so is the cryogenic plant

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

**DECISION: re-measure after #1 and #6, then make the code and the copy agree.** Both of
those changes push the margins the other way, so retention and the cryogenic plant may
become live on their own. Whatever is true afterwards is what the prose must say.

**Recommendation.** Either the doctrine is real and the margins should be tight enough for
it to bind, or it is not and the copy should stop describing it. The honest short-term
move is the copy; the interesting one is to find out whether the margin survives fix #1,
which makes the ships heavier and may bring retention back to life on its own.

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

The size of it, for the documented 15 km balanced case: the P-10000's cycle is 0.846 h, so
its generators running flat out would produce **126.9 MWh** against a published cycle spend
of 82.5 MWh — the generators alone would cover the cycle before solar is counted.

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

**DECISION: (b), remove the generators — the vehicle is battery-electric.**

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
