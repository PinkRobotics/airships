# Enough water to matter

> **Energy reading, 2026-10-02.** Energy conclusions in this earlier report are superseded by the [generated closure record](../../docs/ENERGY-CLOSURE-2026-10.md).
> Its cited tables now show supplied effort on the prescribed, unsupported profile. They do not establish delivery, endurance, savings or operating cost.
> Historical arrows retain earlier figures. Feasible delivery, cycle minutes, both energy bases and the requirements are in the generated record.

<!--tex:skip-->
**A briefing · 2026-08-09 · Pink Robotics**

<!--tex:headline THE IDEA | This briefing studies the requested load and repeating water-source-to-target duty cycle of a proposed buoyant vehicle, alongside established conventional aerial resources. Nothing of this design has been built or flown.-->

## The problem is the round trip

Base-refilled airtankers return to a loading base between drops. Helicopters with buckets
can draft from nearby open water. Water-scooping aircraft already repeat source-to-target
circuits: the CL-415 and amphibious AT-802 are examples in
[NWCG's water-scooping standard](https://fs-prod-nwcg.s3.us-gov-west-1.amazonaws.com/s3fs-public/publication/pms518.pdf),
chapter 3. The [manufacturer's Canadair programme description](https://dehavilland.com/aircraft-sales/de-havilland-aircraft-of-canada-limited-launches-dhc-515-firefighter/)
also identifies the established CL-215 and CL-415 family. These sources describe conventional
resources; they do not establish a comparative hourly rate on the mission studied here.

The proposal under study combines a buoyant hull's requested water load with a repeating
water-source-to-target duty cycle. Its load, cycle and force requirements are model questions;
no aircraft of this design has been built or flown. Local refill is an established aviation
capability, and a comparison must include scooping aircraft alongside helicopters and
base-refilled airtankers.

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

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

| P-100, the reference ship | |
|---|---:|
| Water per drop | 100 t<!--f:P100.spec.payloadT--> |
| Length × diameter | 110<!--f:P100.spec.lenM--> × 55 m<!--f:P100.spec.diaM--> |
| Round trip, 15 km each way | 34.2 min<!--f:P100.cycle.cycleMin--> |
| **Water delivered per hour** | **175 t<!--f:P100.cycle.tph-->** |
| Energy per tonne delivered (earlier 1) | 13.9 |
| Energy per tonne delivered (earlier 2) | 80.4 |
| Energy per tonne delivered (current) | 78.1 kWh<!--f:P100.cycle.kwhPerTonne--> |

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

**Comparison boundary.** The table is an unsupported model profile, not a resource contest
or a measured operating rate. No conventional fleet is simulated on a shared invented mission:
source-to-target distance, scooping-water suitability, base distance, fuel, duty limits,
support and tactical objective are omitted. A capacity specification and a conditional model
rate cannot establish comparative daily delivery or suppression. A resource comparison would
need the same invented task and those inputs for helicopters, scooping aircraft and
base-refilled airtankers.

**Nothing in that table has been built** — no hull, no rotor, no cable. It is what the model says,
which is why the model is published and why the last third of this page is the four things that
would have to be true.

### And then the question of how much bigger

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

Buoyancy scales with volume and drag with area, so a bigger ship is a *cheaper* ship per tonne
delivered: 13.9 → 80.4 → 78.1 kWh/t<!--f:P100.cycle.kwhPerTonne--> on the P-100,
8.5 → 62.5 → 61.7<!--f:P1000.cycle.kwhPerTonne--> on a 1,000-tonne hull, 5.4 → 69.8 → 67.9<!--f:P10000.cycle.kwhPerTonne--> on
a 10,000-tonne one delivering 13,183 t/h<!--f:P10000.cycle.tph-->. The square-cube law, which
punishes almost every other kind of vehicle, is on this one's side.

These energy figures come from the earlier flight model, which understates the force needed to hold an empty hull down. Corrected figures will be higher, and some cycles may not be flyable as drawn.

So the interesting question is what stops you. We modelled it to find out, and **the answer is not
the structure or the power — it is getting back down.** That is the next section, and it is why
the largest class exists in this project at all: as the place the arithmetic breaks, not as
something anyone is proposing to build first.

<!--tex:fig charts/scale.pdf | True relative scale. \textbf{The reference ship is smaller than the Hindenburg} --- 110 m against 245 --- and the two larger classes are the same arithmetic extrapolated, not a plan. | 0.92-->

## What the structural model says

A conventional airship floats because it is full of helium. This concept proposes vacuum lift; nothing floats today as drawn.
The separate 52 m hull of record uses structural safety factor 1.2 against full sea-level pressure.
On the record basis, knockdown 0.30 and 1,050 MPa chords, its lift is 0.558 of its mass at sea level and 0.436 at 2,500 m.
The favourable basis assumes knockdown 0.65 and a 1,450 MPa carbon-laminate compressive ceiling, both unverified.
Its lift-to-mass ratios are 0.981 at sea level and 0.766 at 2,500 m, short by 4.3 t and 53.6 t respectively.
Closure needs tested knockdowns and chord properties, a cap load-path assessment, and a complete structure and equipment bill that fits the lift budget.

The separate 52 m structural drawing and its bill disagree in the end caps, in both directions.
Across five readings, the favourable lift-to-mass ratio ranges from 0.751 to 0.998 at sea level and from 0.586 to 0.780 at 2,500 m.
No reading reaches one; none is a checked design because the sizing checks do not resolve station lengths or connections.
The [member census](../../docs/MEMBER-CENSUS.md) records 20 disagreements between the drawing and the bill.

Francesco Lana de Terzi published the idea in 1670 and was right
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

The configured disk area prices independent actuator disks. The drawing sums both blade disks of each coaxial pair, approximately matching that budget; a pair shares a stream, so its aerodynamic area is nearer a projected footprint. These conventions differ. The generated rotor-area sensitivity in `docs/PHYSICS.md` (“Rotor area convention”) compares them at fixed controls.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

A hull big enough to float when it is full of water is very hard to push *down* when it is empty,
and hardest of all at the bottom, over the lake, where the air is thickest. The P-100 manages: it
has to hold down 136 t<!--f:P100.descent.holdAtSourceT--> of surplus lift at the water and its
rotors can produce 267 → 141<!--f:P100.descent.rotorCapT-->, comfortably.

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

**Scale it up and that margin closes, then inverts.** A 10,000-tonne hull has to hold down
13,723 t<!--f:P10000.descent.holdAtSourceT--> and its rotors can manage
12,666 → 7,124 → 7,079<!--f:P10000.descent.rotorCapT-->. It cannot reach its own water under power. Not because
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

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

The P-100 does not need it — its descent closes on rotors alone with 1.97× headroom — and it
carries one anyway, because a bucket is cheaper than thrust even when thrust would do: the bag
costs 0.006 → 0.006 MWh<!--f:P100.energy.anchorHoistMWh--> a cycle and saves 29% of the cycle's energy.
On the largest class it stops being an efficiency and becomes the thing that makes the descent
possible at all: 0.596 → 0.597 MWh<!--f:P10000.energy.anchorHoistMWh--> against 34.5 MWh of rotor work.
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

> **2026-10-02 correction: record basis, INFEASIBLE.** Arrows preserve the dated value on the left and give the current model on the right. Energy and battery hours describe supplied effort on an unsupported profile, not achieved flight.

- **A structure light enough.** The model assumes a ship's dry mass equals its water payload.
  NASA's own lattice paper — the one this rests on — gives a bare shell 12% heavier than that
  whole allowance, and at the density of the pack NASA built for its electric X-plane (which did not fly), the battery alone is 34% over.
  **This is what the concept lives or dies on.** It looks like a manufacturing question rather
  than a physics one — which is the good news — and it is unanswered.
- **A drop that arrives, and the right metric.** The US Forest Service says a release 1,000 ft
  above the canopy "would completely dissipate"; ours release from 1,476 ft. The same agency
  measures whether fire behaviour changed, not tonnes delivered, and finds success turns on ground
  crews being engaged with the drop. Tonnage is our metric and it may be the wrong one.
- **An energy chain.** Every class runs a deficit every cycle. A P-100 has
  9.2 → 1.5 hours<!--f:P100.energy.hoursOnBattery--> of work in it before the battery is flat. This
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

**Live model** pinkrobotics.ca/airships<br>**The evidence** pinkrobotics.ca/research<br>**Repository, defect list and source catalogue** github.com/pinkrobotics/airships

*Figures here are generated from the model at defaults — balanced mode,
15 km<!--f:worked.oneWayKm--> one way — and checked against it on every build.*

[historical] The dated “other” ledger aggregate has no current equivalent. The corrected ledger uses the six named phases and recovery; no current-model citation is claimed for the old aggregate. Both bases and all closing requirements are in [the generated closure comparison](../../docs/ENERGY-CLOSURE-2026-10.md).
