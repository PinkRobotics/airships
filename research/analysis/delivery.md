# Does the water arrive?

`docs/OPEN-QUESTIONS.md` #12, in two halves: the US Forest Service says a load released
1,000 ft above the vegetation "would completely dissipate", and `ALT.drop` is 450 m — 1,476 ft;
and AFUE, the largest field study of aerial suppression ever run, never counts tonnes at all.

Computed by `research/analysis/delivery.py`. This is the first time this project has looked at
what happens between the tank and the fuel.

## First, the mission this vehicle is actually for

**The primary use is not attacking a burning fire.** It is putting water on ground *before* it
burns — soaking fuel ahead of a front, wetting a containment corridor in advance, raising fuel
and atmospheric moisture over a landscape during a heat event. Direct attack on an active fire
is the **hardest and most extreme case**, kept because a concept that survives it survives
anything, not because it is the concept.

That distinction decides most of this page, because every hard number below comes from the fire
itself — the convection column, the fire-generated turbulence, the urgency that forces a
release from an unsafe height. **Pre-treatment has none of them.** There is no column over
unburned fuel. There is no reason not to fly low and slow. There is no reason not to wait for
the calm hour. The physics that makes direct attack marginal is the physics of the fire, and in
the primary mission the fire is not there yet.

So read what follows as the extreme case, and note that the extreme case is survivable too —
just not from 450 m.

## Water cannot fall faster than about 9 m/s

Drops larger than roughly 5.5 mm are aerodynamically unstable and break up, so released water
arrives as 1–5 mm drops at 4–9 m/s (Gunn & Kinzer). That is a property of water. Three things
follow.

**The pattern smears, and the smear is worse than the drift.** A uniform wind merely
*translates* a pattern — that is aimable bias, not destruction. What destroys it is the spread
across the drop spectrum, because small drops hang and large ones do not. From 450 m a 0.5 mm
drop is airborne for 214 s and a 5 mm drop for 49 s, so one release in a 10 m/s wind is
stretched over **1,645 m along-wind — longer than the whole 1.2 km drop run.**

**And the mean drift is large on its own:**

| release height | fall time, 2 mm | drift at 3 m/s | 5 m/s | 10 m/s | 15 m/s |
|---|---|---|---|---|---|
| SEAT jettison, 18 m | 2.8 s | 8 m | 14 m | 28 m | 42 m |
| large airtanker jettison, 53 m | 8.2 s | 24 m | 41 m | 82 m | 122 m |
| very large airtanker jettison, 122 m | 18.8 s | 56 m | 94 m | 188 m | 282 m |
| USFS "completely dissipates", 305 m | 46.9 s | 141 m | 235 m | 469 m | 704 m |
| **`ALT.drop`, 450 m** | **69.2 s** | **208 m** | **346 m** | **692 m** | **1,038 m** |
| **sprayers on a 300 m lead → 150 m** | **23.1 s** | 69 m | 116 m | **231 m** | 347 m |
| **sprayers on a 400 m lead → 50 m** | **7.7 s** | 23 m | 39 m | **77 m** | 116 m |

*(The three airtanker rows are USFS **training-jettison** heights, which is the only published
table; real operational drops are lower again — DC-10 practice is 150–300 ft AGL. And the
"1,000 ft would completely dissipate" statement this page opens with is about gum-thickened
long-term retardant jettisoned over a designated area, in a document arguing to the Fish and
Wildlife Service that it does not reach listed species. It is evidence for the direction of
this arithmetic, not the same finding as it.)*

**A drop cannot descend through rising air faster than it falls.** Once a load has broken up
into free drops:

| | updraft | drops that still descend |
|---|---|---|
| quiet flank | 5 m/s | 2, 3 and 5 mm |
| active flank | 10 m/s | **none** |
| crown fire column | 25 m/s | **none** |

This is true of every airtanker ever flown, which is why aerial suppression lays line in
*unburned* fuel beside and ahead of a fire rather than dropping onto flame. It is a statement
about free drops after breakup, not about the coherent, air-entraining mass a load is for its
first tens of metres — that descends much faster, which is how airtankers work at all.

## The ship makes its own updraft, and this is the one nobody had noticed

**A buoyant hull holds station by thrusting downward, so its rotors accelerate air *upward*.**
That is the opposite sign to a helicopter, and it happens directly over the release.

For a P-100 holding an emptying hull down during the run:

| | held down | induced velocity **upward** at the disc | wake | air moved |
|---|---|---|---|---|
| start of release | 34.4 t | 7.8 m/s | 15.7 m/s | 21,525 kg/s |
| end of release | 137.4 t | **15.7 m/s** | 31.3 m/s | **43,051 kg/s** |

Against a water release of **500 kg/s**. The ship moves **86 times more air upward than it
releases water downward**, at a velocity that exceeds the terminal velocity of every drop it is
making. By this document's own criterion, a release into the ship's own disc flow does not
descend.

## Which is the argument for putting the sprayers on leads

The vehicle already lowers a 300 m hose to pick water up. **Lowering sprayer leads to put it
down is the same mechanism in reverse**, and it solves the drift, the column and the ship's own
wake at once — because below the disc the rotor flow is a sink, and a sink falls off as 1/z²:

| distance below the hull | induced flow, P-100 |
|---|---|
| 50 m | 2.49 m/s |
| 100 m | 0.62 m/s |
| 200 m | 0.16 m/s |
| 300 m | 0.07 m/s |
| 400 m | 0.04 m/s |

*(Point-sink far field, valid for distances well beyond the disc radius — 28 m on a P-100. It
is not valid close under the very large discs of the bigger classes, and their near field has
not been computed.)*

**A few hundred metres of lead puts the release outside the ship's own flow field entirely**,
and puts it at airtanker release height while the hull stays at a safe one. The release height
stops being a compromise between hull clearance and delivery, and becomes a **control input** —
long lead in calm air for a precise line, short lead when turbulence says stay high, and the
choice made per pass. Multiple leads, like the multiple pumps and multiple bags the fleet
already implies, spread the release across a wider swath and shorten the run.

This is the single highest-value change on this page, and it needs no new physics: it is the
intake hose, pointed the other way.

## Only the reference ship's drop makes suppression sense

Coverage level — US gallons per 100 ft² — is how every aerial drop is prescribed. Grass takes
CL 1–2; heavy timber and slash take CL 6–8. What one pass lays, at the model's own `dropKm`:

| swath | P-100 (100 t over 1.2 km) | P-1000 (1,000 t over 2.5 km) | P-10000 (10,000 t over 5 km) |
|---|---|---|---|
| 20 m | CL 10.2 | CL 49.1 | CL 245.4 |
| 30 m | **CL 6.8** | CL 32.7 | CL 163.6 |
| 50 m | **CL 4.1** | CL 19.6 | CL 98.2 |
| 80 m | CL 2.6 | CL 12.3 | CL 61.4 |

**The P-100 lands inside a real prescription at every plausible swath.** The others are absurd
— CL 163 is 6.7 cm of standing water over a 30 m by 5 km strip. Their drop runs are one to two
orders of magnitude too short for their payloads. A third independent argument for the
reference-class decision, this time from fire doctrine.

## The metric that means something

AFUE counts objectives achieved, not litres, and for large aircraft the objective is nearly
always line. BC campaign fires, 615 with mapped perimeters: median **40.6 km**, p90 146.3 km.

What one P-100 lays in 24 hours at a 30 m swath, at the real 4.71 km median leg:

| prescription | line per 24 h | perimeters it could line daily |
|---|---|---|
| CL 2 (grass) | 326.2 km | 97.9% |
| CL 4 (normal timber) | **163.1 km** | **91.4%** |
| CL 6 | 108.7 km | 84.9% |
| CL 8 (heavy timber, slash) | 81.6 km | 76.6% |

**One P-100 could put a normal timber prescription around the entire perimeter of nine out of
ten BC campaign fires in a day** — or a heavy-timber one around three in four. That is a
logistics claim, not an effectiveness claim, and it is the one this project can defend.

**Two caveats it must be quoted with.** First, **energy**: 7,975 t/day is about 100 MWh at the
published cycle and 150 MWh at `descent.md`'s corrected one, against 6.5 MWh/day from the solar
skin. The rest has to arrive by tender, and the tender fleet is named in the README and
deliberately never modelled. Every 24-hour figure on this page is a statement about the
*aircraft*, not about a system that has been shown to supply it. Second, **persistence**: CL 4
is 1.63 mm of water, which evaporates in tens of minutes to a few hours in fire weather. Water
is not retardant. A wet line is a delaying action and a fuel-moisture change, not a barrier
that is still there tomorrow — which is exactly why the pre-treatment mission wants *repeated*
passes over a corridor, and why an aircraft that never stops is the right shape for it.

## Night is not a consolation prize, it is the design point

Everything here improves after dark, for physical reasons: columns collapse, winds drop,
humidity rises so less is lost in the fall and fuel moisture recovers, and nothing else is
flying. The delivery physics and the endurance advantage point the same way.

## What this does not resolve

**AFUE's 0.56.** Probability of success was 0.72 with ground engagement and 0.56 without, and
without crews the modal outcome was *not effective*. An uncrewed fleet is the 0.56 case by
construction unless it is working *for* ground resources — which points at a product that is
not "drops water on fires" but **"puts water where crews and corridors need it, before they
need it"**. That is the pre-treatment mission again, and it is a logistics problem, which is
what this vehicle is good at.

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
