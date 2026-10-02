# Enough water to matter

<!--tex:skip-->
**A briefing · 2026-08-09 · Pink Robotics**

<!--tex:headline THE IDEA | Water is how fires are stopped. The only questions have ever been how much of it you can put on one, how fast, and for how long --- and the answers today are \emph{not enough, not fast enough, and not for long}. This is a design for a machine that changes all three at once.-->

## The problem is the round trip

A very large airtanker carries about seventy tonnes. It arrives, releases in seconds, and then
spends the next half hour to hour-and-a-half flying to a base, loading, and flying back. Its
instantaneous delivery is spectacular; its *sustained* delivery — the number that decides whether
a fire line holds — is set almost entirely by the turnaround.

Helicopters with buckets shorten the turnaround by dipping from a lake nearby, and pay for it in
payload: a heavy-lift helicopter carries about ten tonnes.

Nothing occupies the gap between them — a machine that dips like a helicopter and carries like a
tanker — because for a rotorcraft every kilogram of lift is bought continuously with power, so
payload and endurance trade directly against each other.

**Buoyant flight does not have that trade.** A hull that displaces its own weight in air holds
altitude at zero power. Carrying more costs the price of a bigger hull, once. Put a buoyant
vehicle over a lake and the turnaround stops existing: it never lands, so there is nothing to turn
around. Nobody is aboard — these are uncrewed ships, sized for the British Columbia interior,
where the fires and the lakes are usually within tens of kilometres of each other.

## What the model says a fleet would do

<!--tex:fig charts/throughput.pdf | Sustained delivery, and the cycle that produces it. Nothing here lands: on every class the longest phases are moving water, not flying.-->

**The reference ship is the smallest one.** The P-100 carries
100 tonnes<!--f:P100.spec.payloadT--> of water, is 110 m<!--f:P100.spec.lenM--> long and
55 m<!--f:P100.spec.diaM--> across — **smaller than the Hindenburg**, which flew in 1936 at 245 m.
Everything below is that ship unless it says otherwise.

| P-100, the reference ship | |
|---|---:|
| Water per drop | 100 t<!--f:P100.spec.payloadT--> |
| Length × diameter | 110<!--f:P100.spec.lenM--> × 55 m<!--f:P100.spec.diaM--> |
| Round trip, 15 km each way | 34.2 min<!--f:P100.cycle.cycleMin--> |
| **Water delivered per hour** | **175 t<!--f:P100.cycle.tph-->** |
| Energy per tonne delivered | 13.9 kWh<!--f:P100.cycle.kwhPerTonne--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

175 tonnes an hour sounds modest beside a very large airtanker's seventy-tonne drop. It is not the
same quantity. **The airtanker's number is one drop; this one is every hour, indefinitely, through
the night.** Over a twelve-hour operational day one P-100 puts down about 2,100 tonnes against
roughly 560 for an airtanker flying eight sorties — and the airtanker then stops, while this does
not. In energy terms a full drop costs about seventy dollars of electricity.

**Nothing in that table has been built** — no hull, no rotor, no cable. It is what the model says,
which is why the model is published and why the last third of this page is the four things that
would have to be true.

### And then the question of how much bigger

Buoyancy scales with volume and drag with area, so a bigger ship is a *cheaper* ship per tonne
delivered: 13.9 kWh/t<!--f:P100.cycle.kwhPerTonne--> on the P-100,
8.5<!--f:P1000.cycle.kwhPerTonne--> on a 1,000-tonne hull, 5.4<!--f:P10000.cycle.kwhPerTonne--> on
a 10,000-tonne one delivering 13,183 t/h<!--f:P10000.cycle.tph-->. The square-cube law, which
punishes almost every other kind of vehicle, is on this one's side.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

So the interesting question is what stops you. We modelled it to find out, and **the answer is not
the structure or the power — it is getting back down.** That is the next section, and it is why
the largest class exists in this project at all: as the place the arithmetic breaks, not as
something anyone is proposing to build first.

<!--tex:fig charts/scale.pdf | True relative scale. \textbf{The reference ship is smaller than the Hindenburg} --- 110 m against 245 --- and the two larger classes are the same arithmetic extrapolated, not a plan. | 0.92-->

## Why it is possible now, and was not before

A conventional airship floats because it is full of helium. This one floats because it is full of
*nothing* — a rigid shell holding a vacuum, about 14% more buoyant than helium, and impossible to
embargo, to corner, or to leak. Francesco Lana de Terzi published the idea in 1670 and was right
about everything except the metal: thin the shell enough to float and the atmosphere crushes it.
Akhmeteli and Gavrilin put a number on that in 2021 — floating and surviving together demand a
stiffness-to-density ratio **no solid substance possesses**, diamond included.

What changed is not a better material but a better *arrangement* of ordinary ones. Discrete
lattice structures hold their stiffness as they lose density, where foams and honeycombs do not,
and applying that to the vacuum balloon moves the binding constraint **from buckling to strength**
(Jenett, Gregg and Cheung, NASA Ames and MIT). Buckling is a geometry failure: sudden, total,
unfixable by a better material. Strength is a number you can look up, test on a bench, and buy
more of. The question stopped being *is this impossible* and became *how light can we build it* —
which is an engineering question, and those get answered.


## What stops you getting bigger: borrowing the lake

A hull big enough to float when it is full of water is very hard to push *down* when it is empty,
and hardest of all at the bottom, over the lake, where the air is thickest. The P-100 manages: it
has to hold down 136 t<!--f:P100.descent.holdAtSourceT--> of surplus lift at the water and its
rotors can produce 267<!--f:P100.descent.rotorCapT-->, comfortably.

**Scale it up and that margin closes, then inverts.** A 10,000-tonne hull has to hold down
13,723 t<!--f:P10000.descent.holdAtSourceT--> and its rotors can manage
12,666<!--f:P10000.descent.rotorCapT-->. It cannot reach its own water under power. Not because
the structure fails or the power runs out — because the air near a lake is 16% denser than the air
it was sized in, and buoyancy that guarantees the ship rises when loaded has to be overcome when
it is empty. **That is the physics that stops the idea getting arbitrarily large**, and it arrived
uninvited, out of a correction to something else.
The answer is to borrow the lake. The ship lowers a cable with a collapsible bag, fills it at the
surface, and winches it just clear: **water hanging on a line is downward force**, and the whole
price of it is the fifteen metres of lift needed to break the surface. When the ship has what it
came for, the bag is tipped back into the lake it came from.

On the P-100 the bag is 125 tonnes<!--f:P100.descent.anchorT--> — **thirteen times** the largest
helicopter bucket ever built, which is an engineering programme. On the 10,000-tonne hull it is
12,400<!--f:P10000.descent.anchorT-->, which is **1,265 times** the same bucket, and that number is
a fair measure of how far past the reference ship the limit case sits.


<!--tex:fig charts/render-anchor.png | The mechanism at the limit case, rendered from the same model that computes the numbers: pump pods on hoses to the surface, and the anchor cable running down to a bag in the water. The bag is to scale --- 12,400 tonnes is 28.7 m across beside an 512 m hull. The rotors are pushing the ship \emph{down} here, which is why the wash blows upward.-->

The P-100 does not need it — its descent closes on rotors alone with 1.97× headroom — and it
carries one anyway, because a bucket is cheaper than thrust even when thrust would do: the bag
costs 0.006 MWh<!--f:P100.energy.ledgerMWh.anchor--> a cycle and saves 29% of the cycle's energy.
On the largest class it stops being an efficiency and becomes the thing that makes the descent
possible at all: 0.596 MWh<!--f:P10000.energy.ledgerMWh.anchor--> against 34.5 MWh of rotor work.
**Fifty-eight to one.** Rotors get disproportionately expensive as you load them, so every tonne
handed to the lake is worth more than a tonne taken off the rotors. That is why the bag does the
*whole* descent rather than just covering the shortfall that revealed it, and why every class
carries one — including the class whose rotors could manage without. The alternatives were costed and rejected in the open: the same ballast as liquid nitrogen is
475 MWh, and filling from high up a 1,350 m hose is 44 MWh. When one mechanism is three orders of
magnitude cheaper than another, that is usually the design telling you something.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

## What would have to be true

This is arithmetic on a vehicle nobody has built, resting on assumptions we have gone looking for
evidence *against*. Four are load-bearing:

- **A structure light enough.** The model assumes a ship's dry mass equals its water payload.
  NASA's own lattice paper — the one this rests on — gives a bare shell 12% heavier than that
  whole allowance, and at the battery density NASA has flown, the battery alone is 34% over.
  **This is what the concept lives or dies on.** It looks like a manufacturing question rather
  than a physics one — which is the good news — and it is unanswered.
- **A drop that arrives, and the right metric.** The US Forest Service says a release 1,000 ft
  above the canopy "would completely dissipate"; ours release from 1,476 ft. The same agency
  measures whether fire behaviour changed, not tonnes delivered, and finds success turns on ground
  crews being engaged with the drop. Tonnage is our metric and it may be the wrong one.
- **An energy chain.** Every class runs a deficit every cycle. A P-100 has
  9.2 hours<!--f:P100.energy.hoursOnBattery--> of work in it before the battery is flat. This
  fleet is a battery being spent, and the chain that recharges it is part of the design.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

Seventeen such issues are tracked at `docs/OPEN-QUESTIONS.md`, fifteen still open. Two closed on
2026-08-09, and both closed by making our own numbers *worse*.

## Why we publish the arithmetic

Because a concept nobody can check is not a concept, it is a picture. Every number here is
produced by code you can run; every claim cites a figure the model generates, and the build fails
if the prose and the model disagree. We catalogue the nine sources that contradict us beside the
ones that support us.

One finding from that discipline is worth more than any single number. When we corrected the solar
skin, the vehicle's power supply changed by a factor of 4.4 and **not one published figure moved**,
because generation was not in the ledger those figures come from. A model can be badly wrong about
something central with nothing able to notice. We would rather be corrected early and loudly than
be right in private.

<!--tex:headline WHERE THIS GOES | If a shell this light can be built, what falls out of it is not only a firefighting machine. Moving ten thousand tonnes of water for four and a half kilowatt-hours a tonne is a capability nothing currently has, at any price. Fire is where it would start: the need is loudest there, and the round trip is shortest.-->

**Live model** pinkrobotics.ca/airships<br>**The evidence** pinkrobotics.ca/research<br>**Repository, defect list and 73 catalogued sources** github.com/pinkrobotics/airships

*Figures here are generated from the model at defaults — balanced mode,
15 km<!--f:worked.oneWayKm--> one way — and checked against it on every build.*
