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

Section 4 (PDF pp. 3–4) records **training-jettison heights over designated areas**:
60 ft or more for single-engine airtankers, 150–200 ft for large airtankers, and
**300–500 ft for very large airtankers**. These are not operational firefighting drop heights.
The same passage's dissipation statements concern long-term retardant. Airtankers otherwise
stay above 1,500 ft AGL except to drop, take off or land.

## What we take from it

`ALT.drop` in `sim/config.js` is **450 m above ground — 1,476 ft**. Section 4 warns that
high releases can disperse before reaching the ground, but describes long-term retardant
jettisons, not this proposed water system. It supports the direction of the concern about
release height, not a measured arrival fraction, a water-loss rate or a comparison with
operational firefighting heights.

Tank discharge and arrival at a target fuel layer remain separate quantities. The project's
delivery analysis computes fall time and drift under stated droplet and wind assumptions;
arrival and deposition still require release and ground-pattern tests. The source is
catalogued as **context**, rather than a direct contradiction of an unmeasured water result.

## Where it does not settle the question

The statement is qualitative and its context should be held against it. It describes long-term
retardant — a gum-thickened fluid with drop characteristics deliberately unlike water — released
from a fixed tank through a constant-flow gate. The context is a biological assessment of
jettison-area exposure; no measurement, sampling method or droplet-size distribution for
this water release is given. Our release is
10,000 t through a purpose-built aperture, four orders of magnitude larger than a tanker load, and
a mass that large may behave as a coherent falling body rather than as spray — which is the
opposite failure mode and no better.

Nothing here measures how much of a 10,000 t water release from 450 m reaches fuel.
The material and release differences prevent a quantitative transfer; the high-release
warning remains a reason to test deposition, not a result of that test.
