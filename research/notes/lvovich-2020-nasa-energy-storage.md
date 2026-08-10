# Lvovich (2020) — Energy Storage for NASA Missions

NASA Glenn Research Center, invited presentation to the ARPA-E IONICS programme review.
NTRS 20205009101. Read in full; it is a slide deck, and its findings are stated as bullet points
rather than derived, which limits how hard it can be leaned on.

## What it establishes

NASA's own view, stated at pack level rather than cell level, of where lithium-ion energy storage
is and where it can go:

- State of the art specific energy **~250 Wh/kg** (cell).
- "Pack specific energy of **300 Wh/kg** is achievable within reasonable timeframe."
- "Pack specific energy of **400 Wh/kg** will probably require maturation of all solid state."
- "**No clear path** for achieving pack specific energy greater than **500 Wh/kg**."

The mission ladder underneath those numbers is the useful part: 300 Wh/kg buys hybrid-electric
capability, 400 Wh/kg buys eVTOL urban air mobility, 500 Wh/kg buys hybrid-electric regional
aircraft, and a single-aisle 150-passenger aircraft needs above 700 Wh/kg — which is beyond the
point where NASA says it can see a route.

## Why it cuts against us

Our classes specify 0.2 MWh of battery per tonne of dry mass, which is a requirement for 200 Wh/kg
at pack level *if the battery is permitted to be the whole aircraft*. Divide by what is left for
everything else and the requirement moves:

- at NASA's near-term achievable 300 Wh/kg, the pack is **67%** of the dry mass allowance;
- at 400 Wh/kg, requiring mature solid state, it is 50%;
- at 500 Wh/kg, the point NASA says it has no clear path beyond, it is **40%**.

Forty per cent is the best case, and it has to share the budget with a hull that
`notes/jenett-2019-lattice-vacuum-airship.md` already shows exceeds 100% on its own. There is no
point on this ladder where the mass budget closes.

## Where it does not support a conclusion

It is a 2020 conference deck by one author, with no derivations, no error bars and no statement of
what "reasonable timeframe" means. Six years have passed and sodium-ion and LFP cell-level claims
have moved; the paper's cell figure of 250 Wh/kg is already conservative against vendor claims,
though vendor pack claims remain unverified by anyone independent.

Crucially, it addresses **aviation and space** packs. The README's intended answer to the energy
problem is not an onboard pack at all — it is tender ships swapping charged cells for discharged
ones. If the aircraft never has to lift the energy it uses, the ceiling this document describes
constrains the tender fleet's size rather than the airship's mass budget. That argument is
available, and it is not the one `sim/config.js` currently makes.
