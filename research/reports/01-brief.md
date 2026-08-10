# Enough water to matter

<!--tex:skip-->
**A briefing · 2026-08-09 · Pink Robotics**

<!--tex:headline THE IDEA | Fire loses to water. It always has. The only question has ever been how much you can put on it, how fast, and for how long --- and the answer today is \emph{not enough, not fast enough, and not for long}. This is a design for a machine that changes all three at once.-->

## Why aerial firefighting is a duty-cycle problem

A very large airtanker carries perhaps seventy tonnes. It arrives, releases in seconds, and then
spends the next half hour to hour-and-a-half flying to a base, loading, and flying back. Its
instantaneous delivery is spectacular; its *sustained* delivery — the number that decides whether
a fire line holds — is set almost entirely by the turnaround.

Helicopters with buckets shorten the turnaround by dipping from a lake nearby, and pay for it in
payload: a heavy-lift helicopter carries about ten tonnes.

Nothing occupies the middle, because for a rotorcraft every kilogram of lift is bought
continuously with power, so payload and endurance trade directly against each other.

**Buoyant flight does not have that trade.** A hull that displaces its own weight in air holds
altitude at zero power. Carrying more costs the price of a bigger hull, once. Put a buoyant
vehicle over a lake and the turnaround stops existing: it never lands, so there is nothing to
turn around.

## What the model says a fleet would do

<!--tex:fig charts/throughput.pdf | Sustained delivery, and the cycle that produces it. Nothing here lands: on every class the longest phases are moving water, not flying.-->

| | P-100 | P-1000 | P-10000 |
|---|---:|---:|---:|
| Water per drop | 100 t<!--f:P100.spec.payloadT--> | 1,000 t<!--f:P1000.spec.payloadT--> | 10,000 t<!--f:P10000.spec.payloadT--> |
| Length | 190 m<!--f:P100.spec.lenM--> | 404 m<!--f:P1000.spec.lenM--> | 876 m<!--f:P10000.spec.lenM--> |
| Round trip, 15 km each way | 34.2 min<!--f:P100.cycle.cycleMin--> | 35.4 min<!--f:P1000.cycle.cycleMin--> | 45.5 min<!--f:P10000.cycle.cycleMin--> |
| **Water delivered per hour** | **175 t**<!--f:P100.cycle.tph--> | **1,697 t**<!--f:P1000.cycle.tph--> | **13,183 t**<!--f:P10000.cycle.tph--> |
| Energy per tonne delivered | 12.5 kWh<!--f:P100.cycle.kwhPerTonne--> | 7.4 kWh<!--f:P1000.cycle.kwhPerTonne--> | 4.6 kWh<!--f:P10000.cycle.kwhPerTonne--> |

Thirteen thousand tonnes an hour is thirteen million litres an hour, from one aircraft, without
landing, through the night — and at industrial electricity prices the energy in a full
10,000-tonne<!--f:P10000.spec.payloadT--> drop costs on the order of two thousand dollars.
**It also gets cheaper as it gets bigger**: buoyancy scales with volume and drag with area, so the
largest class delivers a tonne for 4.6 kWh<!--f:P10000.cycle.kwhPerTonne--> against the smallest
class's 12.5<!--f:P100.cycle.kwhPerTonne-->. The square-cube law, which punishes almost every
other kind of vehicle, is on this one's side.

<!--tex:fig charts/scale.pdf | The three classes at true relative scale, against the two largest aircraft most readers can picture. The volume is the lift. | 0.92-->

## Why it is possible now, and was not before

A conventional airship floats because it is full of helium. This one floats because it is full of
*nothing* — a rigid shell holding a vacuum, about 14% more buoyant than helium, and impossible to
embargo, to price, or to leak.

The idea is 356 years old. Francesco Lana de Terzi published it in 1670 and was right about
everything except the metal: thin the shell enough to float and the atmosphere crushes it. That
was never fixable by waiting for better materials. Akhmeteli and Gavrilin put a number on it in
2021 — floating and surviving together demand a stiffness-to-density ratio **no solid substance
possesses**, diamond included.

What changed is not a better material but a better *arrangement* of ordinary ones. Discrete
lattice structures — ultralight frameworks assembled from many identical mass-produced parts —
hold their stiffness as they lose density, where foams and honeycombs do not. Jenett, Gregg and
Cheung, at NASA Ames and MIT, applied that to the vacuum balloon and found the binding constraint
moves from **buckling to strength**. Buckling is a geometry failure: sudden, total, unfixable by a
better material. Strength is a number you can look up, test on a bench, and buy more of. The
question stopped being *is this impossible* and became *how light can we build it* — and that is
an engineering question, which is the kind that gets answered.

## Borrowing the lake

One part of this is not a scaling exercise, and it is our favourite thing in the project. A hull
big enough to float when it is full of water is very hard to push *down* when it is empty
— hardest of all at the bottom, over the lake, where the air is thickest. Our largest class has
to hold down 13,723 t<!--f:P10000.descent.holdAtSourceT--> of surplus lift there and its rotors
can manage 12,666<!--f:P10000.descent.rotorCapT-->. It cannot reach its own water under power.
The problem arrived uninvited, out of a correction to something else.

The answer is to borrow the lake. The ship lowers a cable with a collapsible bag, fills it at the
surface, and winches it just clear: **12,400 tonnes<!--f:P10000.descent.anchorT--> hanging on a
line is 12,400 tonnes<!--f:P10000.descent.anchorT--> of downward force**, bought for the fifteen
metres of lift it takes to break the surface — then tipped back where it came from.


It costs 0.596 MWh<!--f:P10000.energy.ledgerMWh.anchor--> and removes 34.5 MWh of rotor work.
**Fifty-eight to one.** Rotor power goes as thrust to the 1.5, so load moved onto the lake comes
off faster than linearly — which is why the bag does the *whole* descent rather than covering the
shortfall that revealed it, and why every class carries one including the class that does not
need it. The alternatives were costed in the open and rejected: the same ballast as liquid
nitrogen is 475 MWh, and filling from high up a 1,350 m hose is 44 MWh at two-metre bore and
140 bar. When a mechanism is three orders of magnitude cheaper than everything else, that is
usually the design telling you something.

## What would have to be true

This is arithmetic on a vehicle nobody has built, resting on assumptions we have gone looking for
evidence *against*. Four are load-bearing:

- **A structure light enough.** The model assumes a ship's dry mass equals its water payload.
  NASA's own lattice paper — the one this rests on — gives a bare shell 12% heavier than that
  whole allowance, and at the battery density NASA has flown, the battery alone is 34% over.
  **This is what the concept lives or dies on**, and it is a manufacturing question rather than a
  physics one, which is both the good news and the reason to keep going.
- **A drop that arrives.** The US Forest Service says a release 1,000 ft above the canopy "would
  completely dissipate". Ours release from 1,476 ft, raised for hull clearance and never costed
  against delivery.
- **Ground crews.** The Forest Service measures whether fire behaviour changed, not tonnes, and
  finds success turns on crews being engaged with the drop. Tonnage is our metric; it may be the
  wrong one.
- **An energy chain.** Every class runs a deficit every cycle — a P-100 has
  10.4 hours<!--f:P100.energy.hoursOnBattery--> of work in it, a P-10000
  36.3<!--f:P10000.energy.hoursOnBattery-->. This fleet is a battery being spent.

Thirteen such issues are tracked at `docs/OPEN-QUESTIONS.md`, eleven still open. Two closed on
2026-08-09 by making our own numbers *worse*: the solar skin had needed an impossible 76%
conversion efficiency, and the nitrogen store had been returning more work than the nitrogen
contained.

## Why we publish the arithmetic

Because a concept nobody can check is not a concept, it is a picture. Every number here is
produced by code you can run; every claim cites a figure the model generates, and the build fails
if the prose and the model disagree. Two tests fail on purpose, so a known defect cannot quietly
lose its excuse. We catalogue the sources that contradict us beside the ones that support us —
nine against, at last count.

One finding from that discipline is worth more than any single number. When we corrected the solar
skin, the vehicle's power supply changed by a factor of 4.4 and **not one published figure moved**,
because generation was not in the ledger those figures come from. A model can be badly wrong about
something central with nothing able to notice. We would rather be corrected early and loudly than
be right in private.

<!--tex:headline WHERE THIS GOES | A vehicle that moves ten thousand tonnes of water to wherever it is needed, for four and a half kilowatt-hours a tonne, is not only a firefighting machine --- it is water logistics at a scale that does not currently exist. Fire is where it starts because that is where the need is loudest and the round trip is shortest.-->

**Repository** github.com/pinkrobotics/airships<br>**Live model** pinkrobotics.ca/airships<br>**The evidence, in public** pinkrobotics.ca/research<br>**The defect list** `docs/OPEN-QUESTIONS.md`<br>**The sources** `research/sources.json` — 73 of them, 12 with written notes, 9 that contradict us

---

*Figures marked in this document are generated from the model at defaults — balanced mode,
15 km<!--f:worked.oneWayKm--> one way — and verified against it automatically. Where a number here
disagrees with the model, the build fails.*
