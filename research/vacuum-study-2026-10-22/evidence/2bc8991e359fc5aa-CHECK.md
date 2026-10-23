# MAINLINE-016 check — ref-cca93dbfd236dcaa3a8b

Unit vacuum-mainline016-check-1019. Card ref-0c9ab80606a173c6adb6. Order ord-admiral-rr2-check016-017-grok-1019.

Arithmetic is check016.py in this directory. The owner's compute.py was not run. Display rounding is half-up.

## What matches

MAINLINE-009's five mode factors, face and core thicknesses, and the 244.472 kg margin match the pin. From the stated formulas, the leak budget, permeation, outgassing, resident moisture, pump work, all eight seam rows, the four face temperatures, shear-lag stress, climate margins, and the gust loads match RESULTS.json. Climbing from 500 m to 1500 m on the stated gas constant loses 9.36 percent of density, which is the card's "about 9.4 percent per km."

## Mismatches

Vacuum mass rate. RESULTS 0.00056590766 kg/s, which is one percent of the lift per day. The stated R_air 287.05 gives 0.00056591357 kg/s. The choked area 2.47585 mm2 divides the lift mass by the 287.05 flux. The card's 2.48 mm2 is unchanged. The pinned atmosphere implies 287.053, and the register states 287.05.

No-convection bound. The stated balance gives 313.538 K. RESULTS stores 313.526 K. The card's 313.5 K stands.

Display, card versus recomputed:

- lambda 1.526 versus 1.525
- synoptic safety-factor upper end 0.2425 versus 0.2424
- storm margin 219.9 kg versus 220.0 kg on the card's own scaling
- retained water 125.6 kg versus 125.7 kg

## Objections

The storm margin multiplies the 244.472 kg margin by the pressure ratio. Section 5's law multiplies the whole lift. A 10 percent storm low is then a margin of −244.5 kg, not +220 kg. The safety factors themselves scale correctly as 1/p. The stored field name crush_SF_at_case holds that scaled global factor, not core crush.

Added air mass 2445 kg is half the displaced air. The hull is 4645 kg. The sentence that the two are equal is false.

## Sources

Every row in the inherited register and the new register has a QUESTIONABLE or PROJECTION tag and a source. Panel sizes 4 m and 2 m are marked PROJECTION. These inputs are used and are not in either register: hardpoint patch 0.0707 m2, spreader target 1.5, cradle pressure 250 kPa, pump ceiling 1000 Pa, water density 1000 kg/m3, and the Stefan-Boltzmann constant. The molar volume 22414 cm3 sits only in the formula line. Reference pressure 101325 Pa is used for permeation and is not a register row.

## NFI from this check

NFI-CHECK-016-MARGIN, NFI-CHECK-016-ADDED, NFI-CHECK-016-SOURCE. None stop the card.
