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
| Energy per tonne delivered | 10.1 kWh<!--f:P100.cycle.kwhPerTonne--> | 6.4 kWh<!--f:P1000.cycle.kwhPerTonne--> | 4.3 kWh<!--f:P10000.cycle.kwhPerTonne--> |

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

`docs/OPEN-QUESTIONS.md` in the repository lists **thirteen** open defects and unjustified
assumptions. Six were found by the people who wrote the model. The other seven were found by
auditing every published claim against the code, and then by reading the sources — and four of
those came back saying the project is wrong:

- **The structure may not be achievable.** The model assumes the ship's entire dry mass equals
  its water payload. NASA's own lattice paper, which this project cites as its precedent, gives a
  *bare shell* 12% heavier than that whole allowance — before skin, joints, rotors, tanks or
  batteries. This is the largest unresolved question in the project.
- **The solar skin is credited with 200 W/m² of electricity**, which against the actual solar
  resource in the BC interior would require 76% conversion efficiency. The honest figure is about
  53 W/m².
- **The nitrogen energy store recovers more work than the nitrogen contains** — 225 kWh per tonne
  from a liquid that holds 173 kWh per tonne. That is not an optimistic efficiency; it is
  impossible, and it is on the page.
- **The water may not reach the ground.** The US Forest Service states that a drop released
  1,000 ft up "would completely dissipate". Our ships release from 1,476 ft. And the Forest
  Service's own effectiveness study measures whether fire behaviour changed — not tonnes, which is
  what this project has optimised.

The first three make the concept harder. The fourth suggests the headline metric may be measuring
the wrong thing entirely.

## Why publish something with thirteen holes in it

Because a concept nobody can check is not a concept, it is a picture. Every number on the site is
produced by code in the repository; every claim in these reports cites a figure the model
generates, and a script fails the build if the prose and the model disagree. The list of defects
grew from six to thirteen the day we started checking properly, and *it is the same model* —
nothing was introduced, it was all already true and unnoticed.

If the idea is wrong, this is the fastest way to find out. If it is not wrong, this is the only
kind of evidence worth anything.

**Repository:** github.com/pinkrobotics/airships · **Live model:** pinkrobotics.ca/airships
**The defect list:** `docs/OPEN-QUESTIONS.md` · **The sources:** `research/sources.json` (73 of
them, 12 with written notes, 9 that contradict us)

---

*Figures marked in this document are generated from the model at defaults —
balanced mode, 15 km<!--f:worked.oneWayKm--> one way — and verified against it
automatically. Where a number here disagrees with the model, the build fails.*
