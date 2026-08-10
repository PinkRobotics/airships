# Suter (2005) — Rotor Wash

One page, Wildland Fire Chemical Systems, USDA Forest Service Missoula Technology and Development
Center, revision date 26 January 2005. A US Government work. Read in full — it is a page.

## What it establishes

"Helicopters flying at low levels can create a vertical down wash of air (rotor wash) that becomes
a surface wind which may spread fire along the ground." The page carries a chart of drop height
against drop speed for a UH-60 Black Hawk, contoured by the surface wind the rotor wash produces,
and states the operational consequence directly: **hovering, a Black Hawk would have to be well
over 160 feet up to keep rotor wash below 30 mph.**

That is the whole document. It matters because it is the Forest Service telling its own pilots that
the aircraft delivering the water is also making wind at the fire, and giving a number for how much
height it takes to stop.

## Why it cuts against us

The README lists downwash as a thing that could invert the concept and says, correctly, that
nothing in the model accounts for it. This source lets us put a first bound on the size of the
omission.

A UH-60 at 9,979 kg over a 16.36 m rotor is about 47 kg/m² of disc loading, and at that loading it
needs 50 m of height to get its surface wind under 30 mph. Our P-10000 gives itself `diskM2` =
160,000 m² and a maximum down-thrust `rotorCapT` of 12,666 t: **79 kg/m²**, two thirds again
higher. Momentum theory at that thrust gives an induced velocity of about 19 m/s at the disc and
roughly twice that in the developed slipstream — of the order of 40 m/s, or 84 mph, at the rotor
authority the model allows itself. The ship trims 450 m above the fire, but it is doing so with a
disc some 450 m across, and a jet that wide does not decay over its own diameter the way a 16 m
rotor's does.

The rotor is not at full thrust during the drop; the descent anchor exists precisely to take that
load onto a cable instead. So the figure above is a ceiling, not an operating point. It is still
the case that the model has an unmodelled term whose scale is plausibly tens of metres per second
of wind, delivered onto the fuel it is trying to wet.

## Where it does not support the conclusion

This is a one-page field aid about a 16 m rotor, published in 2005, with no method, no measurement
description and no citation behind its chart. Nothing in it licenses extrapolation to a 450 m disc,
and the scaling above is ours, not Suter's — momentum theory gives induced velocity at the disc
and says nothing about how a wake of that diameter interacts with a convective column that is
itself rising at tens of metres per second. It establishes that rotor wash fans fire and that
height is the mitigation. It does not establish what our aircraft would do, and no source we have
found does.
