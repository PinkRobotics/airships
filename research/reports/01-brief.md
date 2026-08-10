# A wildfire airship that has not been built, and the arithmetic that says whether it could be

**A two-page brief · 2026-08-09 · Pink Robotics**

---

## What this is

A conceptual design for a fleet of very large, uncrewed airships that fight wildfire by carrying
water from a lake to a fire, continuously, day and night, without landing between drops. There is
a working simulation of it at [pinkrobotics.ca/airships](https://pinkrobotics.ca/airships/) and the
whole thing — model, tests, sources, and a list of everything wrong with it — is open source.

**Nothing has been built.** No hull, no rotor, no bucket, no cable. This is a set of numbers about
a vehicle that does not exist, published so that people who know more than we do can find the
places where the numbers are wrong. Several already have.

## The idea in one paragraph

A conventional airship floats because it is full of helium. This one floats because it is full of
*nothing*: a rigid shell holding a vacuum, which is 14% more buoyant than helium and does not have
to be bought, shipped, or replaced when it leaks. That is a 350-year-old idea — Francesco Lana de
Terzi, 1670 — and it has never worked, because a shell stiff enough to resist an atmosphere
pressing in on it has always been heavier than the air it displaces. What has changed is the
manufacturing: NASA has demonstrated ultralight discrete lattice structures that get close enough
to the line to make the arithmetic worth re-running. **Close enough to re-run is not the same as
over the line, and this project's own numbers say it is not over the line yet.** See "What is
wrong with it", below.

## What the model says a fleet would do

Three classes. The largest is 876 m<!--f:P10000.spec.lenM--> long and 219 m<!--f:P10000.spec.diaM-->
across — longer than the Hindenburg by a factor of three — and carries
10,000 t<!--f:P10000.spec.payloadT--> of water.

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Water per drop | 100 t<!--f:P100.spec.payloadT--> | 1,000 t<!--f:P1000.spec.payloadT--> | 10,000 t<!--f:P10000.spec.payloadT--> |
| Length | 190 m<!--f:P100.spec.lenM--> | 404 m<!--f:P1000.spec.lenM--> | 876 m<!--f:P10000.spec.lenM--> |
| Round trip, 15 km each way | 34.2 min<!--f:P100.cycle.cycleMin--> | 35.4 min<!--f:P1000.cycle.cycleMin--> | 45.5 min<!--f:P10000.cycle.cycleMin--> |
| Water delivered per hour | 175 t<!--f:P100.cycle.tph--> | 1,697 t<!--f:P1000.cycle.tph--> | 13,183 t<!--f:P10000.cycle.tph--> |
| Energy per tonne delivered | 12.5 kWh<!--f:P100.cycle.kwhPerTonne--> | 7.4 kWh<!--f:P1000.cycle.kwhPerTonne--> | 4.6 kWh<!--f:P10000.cycle.kwhPerTonne--> |

For scale: a Boeing 747 supertanker drops about 70 t and then flies to an airbase to reload. The
model's largest ship delivers 13,183 t<!--f:P10000.cycle.tph--> in an hour and never lands.

Those are outputs of a simulation, not measurements, and at least two known defects in the model
affect the energy row. They are listed in the repository, not buried in it.

## The one genuinely new idea in it

Everything above is a scaling exercise. One part is not.

A hull big enough to float when it is full of water is extremely hard to push *down* when it is
empty — and hardest right at the bottom, over the lake, where the air is thickest. Our largest
ship has to hold down 13,723 t<!--f:P10000.descent.holdAtSourceT--> of surplus lift there, and its
rotors can manage 12,666 t<!--f:P10000.descent.rotorCapT-->. It cannot get back down to the water
under its own power. That is a real physical problem and it appeared, unwelcome, in the middle of
this project.

The answer turned out to be to borrow the lake. The ship lowers a cable with a collapsible bag on
the end — a helicopter Bambi bucket, in service since 1983, at 1,265 times the largest size
anyone has built (9,800 litres) — fills the bag, and winches it just clear of the surface.
12,400 t<!--f:P10000.descent.anchorT--> of water hanging on a line is
12,400 t<!--f:P10000.descent.anchorT--> of downward force. It costs the 15 m of lift needed to
break the surface: **0.596 MWh<!--f:P10000.energy.ledgerMWh.anchor-->**, against the
34.5 MWh of rotor work it replaces. Fifty-eight to one. Then the bag is dumped back where it came
from, and nothing is carried away or manufactured.

The two alternatives were costed and rejected in the open: making the same ballast as liquid
nitrogen is 475 MWh, and filling from high up through a 1,350 m hose is 44 MWh and needs a
two-metre bore at 140 bar.

## What is wrong with it

This is the part most concept announcements leave out, and it is the reason this one exists.

`docs/OPEN-QUESTIONS.md` in the repository lists **thirteen** defects and unjustified
assumptions, eleven of them still open. Six were found by the people who wrote the model. The
other seven were found by auditing every published claim against the code, and then by going and
reading the sources — and four of those came back saying the project is wrong.

**Two of the four are fixed, and fixing them made our numbers worse:**

- **The solar skin was credited with 200 W/m² of electricity.** Against the actual solar resource
  in the BC interior, getting that out of the sun would need 76% conversion efficiency — three
  and a half times the best cell
  ever made in a laboratory. It is **45 W/m²** now. Every endurance figure on the site fell by
  about two thirds: the smallest ship went from 35 hours of work in it to
  **10.4**<!--f:P100.energy.hoursOnBattery-->.
- **The nitrogen store recovered more work than the nitrogen contains** — 225 kWh from a tonne of
  liquid holding 173. Not an optimistic efficiency, an impossible one. It is
  **0.20**<!--f:assumptions.rtLN2--> now, and a test fails the build if anyone raises it past the
  physical ceiling again.

**Two are open, and the first of them is the one that could end the project:**

- **The structure may not be achievable.** The model assumes the ship's entire dry mass equals its
  water payload. NASA's own lattice paper, which this project cites as its precedent, gives a
  *bare shell* 12% heavier than that whole allowance — before skin, joints, rotors, tanks or
  batteries. Separately, at the battery density NASA has actually flown, the battery alone is 34%
  over the same budget. This is the largest unresolved question here and no amount of simulation
  settles it.
- **The water may not reach the ground.** The US Forest Service states that a drop released
  1,000 ft up "would completely dissipate". Our ships release from 1,476 ft. And the Forest
  Service's own effectiveness study measures whether fire behaviour changed — not tonnes, which is
  what this project has optimised.

Notice which direction the two fixes went. Both made the vehicle look worse and both made the
project's stated conclusion — that this fleet is a battery being spent, not a perpetual machine —
harder to argue with. That is the whole reason to do it this way.

## Why publish something with thirteen holes in it

Because a concept nobody can check is not a concept, it is a picture. Every number on the site is
produced by code in the repository; every claim in these reports cites a figure the model
generates, and a script fails the build if the prose and the model disagree. The list of defects
grew from six to thirteen the day we started checking properly, and *it is the same model* —
nothing was introduced, it was all already true and unnoticed.

One finding from that day is worth more than any of the numbers. Correcting the solar skin changed
the vehicle's power supply by a factor of 4.4 — and **not one published figure moved**, because
generation is not in the ledger that computes them. A model can be badly wrong about something
central and have no test anywhere able to notice. That is now defect 6 on the list, and it is the
reason this project believes in publishing the arithmetic rather than the conclusion.

If the idea is wrong, this is the fastest way to find out. If it is not wrong, this is the only
kind of evidence worth anything.

**Repository:** github.com/pinkrobotics/airships · **Live model:** pinkrobotics.ca/airships
**The evidence, in public:** pinkrobotics.ca/research
**The defect list:** `docs/OPEN-QUESTIONS.md` · **The sources:** `research/sources.json` (73 of
them, 12 with written notes, 9 that contradict us)

---

*Figures marked in this document are generated from the model at defaults —
balanced mode, 15 km<!--f:worked.oneWayKm--> one way — and verified against it
automatically. Where a number here disagrees with the model, the build fails.*
