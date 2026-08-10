# Arnaiz-del-Pozo, López-Paniagua, López-Grande & González-Fernández (2020) — Optimum Expanded Fraction for an Industrial, Collins-Based Nitrogen Liquefaction Cycle

*Entropy* 22(9), 959. CC BY 4.0. Read in full.

## What it establishes

An optimisation of a realistic industrial nitrogen liquefier — Collins topology, four pressure
levels (1, 4, 18 and 36 bar, the last just above nitrogen's 33.9 bar critical pressure), with
mechanically coupled compander sets — simulated in Unisim with Peng-Robinson. Two numbers come out
of it that matter to us.

**Optimum specific compression work: 430.7 kWh per tonne of liquid nitrogen**, at an expanded flow
fraction of 88%. That is 0.431 kWh/kg for a well-designed, large, stationary plant.

**The reversible minimum for the same change of state: 173.4 kWh per tonne**, giving a rational
exergy efficiency of 40.3%. Roughly 40% of the 59.7% exergy destruction happens in the aftercoolers
after compression — heat thrown away to ambient.

## What this project takes

`CFG.eLN2 = 0.45` kWh/kg, in `sim/config.js`, described there as a demonstration assumption with no
source. This is the source it should have had, and it holds: 0.45 against a best-practice 0.431 is
a 4% margin on the pessimistic side, which is the right direction for an assumption to be wrong in.

## Where it cuts against us

`CFG.rtLN2 = 0.50` — "electrical round-trip efficiency of the nitrogen store" — cannot be true, and
this paper is why.

The most work recoverable from liquid nitrogen is its exergy relative to the surroundings. This
paper puts that at 173.4 kWh per tonne for its feed and product states; the wider literature
clusters around 0.17–0.21 kWh/kg depending on the reference state chosen. Our model spends
`eLN2` = 450 kWh per tonne to make the liquid and then credits back `rtLN2 × eLN2` = **225 kWh per
tonne**. That is 30% more than the source's exergy figure and about 7% more than the most generous
figure in the literature. `eBack` in `sim/plan.js` recovers more work from the nitrogen than the
nitrogen contains, whichever end of the range you take.

The number that would be defensible is the exergy divided by the liquefaction energy — 173.4/450,
or about 0.39, and lower once a real expander's isentropic efficiency and heat leak are counted.
Halving `rtLN2` roughly halves `eBackMWh`, which currently runs from 0.41 MWh on a P-100 to 4.75 MWh
on a P-10000, so this is not a rounding error in the published cycle energy.

## Where it does not support us either way

The feed is gaseous nitrogen already at 4 bar. Separating nitrogen from air is a *different* process
and its work is not in the 430.7 figure, so `eLN2`'s own description — "kWh per kg to liquefy
nitrogen from air" — is doing more than this source can pay for. The plant is also stationary, and
about a quarter of its exergy destruction is in aftercoolers rejecting heat to ground-level
surroundings. An airborne plant at 2,500 m has thinner, and often warmer, air to reject into, and
has to carry the heat exchangers that do it. Both effects push the real number up, not down.
