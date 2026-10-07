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

The liquefaction dial in `sim/config.js` is an assumed all-in figure with no all-in source in
the repository. This paper starts with already-pure nitrogen supplied at pressure: its
compressor-work optimum does not include separating air. It therefore supplies neither an
all-in bill nor a conservative margin for the model. Intake, separation, compression,
liquefaction, transfer and heat rejection still need a complete, specified boundary.

## What constrains recovery

The source's exergy is a bound for its stated feed, product and reference states, not
an electrical round-trip guarantee. The model's recovery fraction remains an assumption;
the [generated plant sensitivity](../analysis/energy-plant.json) holds recovered work per
tonne fixed when it changes the ground-comparator liquefaction energy. Earlier round-trip
figures in this note are withdrawn rather than presented as the current model.

## Where it does not support us either way

The feed is gaseous nitrogen already at 4 bar. Separating nitrogen from air is a *different* process
and its work is not in the 430.7 figure, so `eLN2`'s own description — "kWh per kg to liquefy
nitrogen from air" — is doing more than this source can pay for. The plant is stationary and includes aftercoolers rejecting heat to its specified
surroundings. That boundary does not establish the cooling utility, exchanger mass or full
energy bill of an airborne plant. Those remain evaluator questions.
