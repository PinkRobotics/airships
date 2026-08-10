# NOAA / NASA / USAF (1976) — U.S. Standard Atmosphere, 1976

NOAA-S/T 76-1562, also NASA-TM-X-74335. A US Government work. Consulted for the troposphere
definition in Part 1; the upper-atmosphere chemistry that makes up most of the 243 pages is not
relevant here.

## What it establishes

The idealised mean vertical profile of a static atmosphere: sea-level pressure 101,325 Pa,
temperature 288.15 K, density 1.225 kg/m³, gravity 9.80665 m/s², and a linear temperature lapse of
6.5 K/km through the troposphere to 11 km, from which pressure follows the hydrostatic relation and
density follows the perfect-gas law. Air is treated as a homogeneous mixture of fixed mean
molecular weight below 86 km, which is what makes a single specific gas constant of 287.053
J/kg·K legitimate.

## What this project takes

All of it, and recently. Until 2026-08-09 `ledger()` computed displacement at 1.225 kg/m³ and used
that number at every altitude; the fix was to build `sim/atmosphere.js` around this profile, so
every lift figure the site now publishes is the ISA column evaluated at a stated altitude.
`figures.json` records the three values the fleet is sized against: 1.225 at sea level, 1.1116 at
the 1,000 m plateau, **0.9569 at the 2,500 m working altitude**. The 22.2% growth in hull
displacement and the 5.25% float-up margin are consequences of this document and nothing else.

`CFG.rhoSL` is the sea-level anchor the profile is scaled from, which is the honest place to put
the dial: moving it moves the air at every altitude rather than lying about where the ship flies.

## Where it does not support us

It is a standard, not a measurement, and the introduction says as much: an idealised, steady-state
representation of a mid-latitude mean. British Columbia in fire season is neither mid-latitude
mean nor steady.

The exposure that matters is temperature. Density at a given altitude is `p/RT`, and the pressure
at 2,500 m is fixed by the column below, so 15 K of summer warmth over the ISA value takes density
from 0.957 to about 0.907 — **5.2% less lift**, or 1,100 t on a P-10000. Our float-up margin is
5.25%. A hot afternoon over a burning plateau is enough to consume the entire safety margin the
hulls were resized to obtain, and the model has no temperature input at all.

The standard is also silent on exactly the air our aircraft works in. It describes a static
atmosphere; a fire generates a convective column with its own density deficit, vertical velocity
and entrainment, and a 22 million m³ hull trimming above one is inside that flow rather than in the
standard column. Nothing in this document, and nothing anywhere in `sim/`, accounts for it.
