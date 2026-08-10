# USDA Forest Service (2022) — Nationwide Aerial Application of Fire Retardant, Biological Assessment Addendum: Airtanker Bases

Prepared by Laura Conway, National Technology and Development Program, 30 June 2022. A US
Government work. Read in full for the flight-height material in Section 4 and the effects analysis
in Section 5.

## What it establishes

The document exists to tell the Fish and Wildlife Service what happens to retardant jettisoned near
airtanker bases, so it has to state plainly how high a load can be released before it stops being a
load. It says:

> "When retardant is dropped at a high enough altitude it dissipates and evaporates prior to
> reaching the ground, spreading over a large area at undetectable levels. In general, a drop
> 1,000 feet above ground/vegetation level would completely dissipate. Above 500 feet above ground
> level the majority of jettison loads would dissipate."

It also records operational drop heights for training jettisons: 60 ft or more for single-engine
airtankers, 150–200 ft for large airtankers, **300–500 ft for very large airtankers**. Airtankers
otherwise stay above 1,500 ft AGL except to drop, take off or land.

## Why it cuts against us

`ALT.drop` in `sim/config.js` is **450 m above ground — 1,476 ft**. The comment beside it reasons
that the height "gives the drop the fall it needs to arrive as rain instead of a column". The
Forest Service's own operational statement is that a load released at 1,000 ft does not arrive at
all. We are dropping half again higher than the altitude at which the agency that runs the largest
airtanker fleet in the world says the water disappears.

The altitude was chosen for a different reason — clearing an 876 m hull's keel over the fire's
convective column and the terrain — so this is a genuine conflict between two constraints rather
than an oversight. But `deliveredT` is currently the whole headline metric, and it counts tonnes
leaving the tank, not tonnes arriving. On this source, at this altitude, those are not the same
number and the difference is most of it. This is the README's "what arrives" question with a
citation attached.

## Where it does not settle the question

The statement is qualitative and its context should be held against it. It describes long-term
retardant — a gum-thickened fluid with drop characteristics deliberately unlike water — released
from a fixed tank through a constant-flow gate, and it is written in a document arguing that
jettisoned retardant does not reach listed species, which is an incentive pointing towards
"dissipates". No measurement, sampling method or droplet-size distribution is given. Our release is
10,000 t through a purpose-built aperture, four orders of magnitude larger than a tanker load, and
a mass that large may behave as a coherent falling body rather than as spray — which is the
opposite failure mode and no better.

Nothing here tells us how much of a 10,000 t release from 450 m reaches fuel. It tells us the
assumption that most of it does is contradicted by the only operational authority that has written
the number down.
