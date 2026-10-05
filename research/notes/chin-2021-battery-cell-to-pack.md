# Chin, Look, McNichols, Hall, Gray & Schnulo (2021) — Battery Cell-to-Pack Scaling Trends for Electric Aircraft

NASA Glenn Research Center, NTRS 20210017488. Read in full.

## What it establishes

The gap between a cell datasheet and a pack that can fly, and why the gap gets *worse* as cells
improve.

The empirical anchor is flight hardware: "The X-57 battery is a common reference, using 225 Wh/kg
lithium-ion cells to create a 149 Wh/kg pack" — a cell-to-pack factor of **0.66**. The paper's
contribution is to show that this factor is not a constant to be carried forward. Preventing
thermal runaway from propagating cell to cell is the dominant packaging cost, and the heat a single
cell releases scales with its energy: a 200 Wh/kg cell corresponds to a 16 kJ core heat load and a
400 Wh/kg cell to 32 kJ, against a design rule of about 20 kJ released per amp-hour. So the mass
of spacing, conduction paths and containment grows with the very quantity that was supposed to be
saving mass. Phase-change-material cores were evaluated and came out heavier than aluminium at
every energy density tested.

## Why it cuts against us

The configured battery-to-dry-allowance ratio differs by class. The generated comparison
uses each class's capacity and dry allowance, the reference pack density, and the complete
nominal floor budget:

<!-- battery:ratios:start -->
At the 149 Wh/kg reference pack density, the battery alone exceeds the dry allowance on P-100 and P-10000.
The per-class ratio of reference-pack mass to dry allowance is shown below.
The complete nominal floor budget exceeds the dry allowance on P-100, P-1000, P-10000, as its own totals show below.

| Class | Battery MWh | Dry allowance t | MWh/t dry | Battery-only minimum Wh/kg | Reference pack t | Pack / dry ratio | Complete floor t | Floor / dry |
|---|---|---|---|---|---|---|---|---|
| P-100 | 20 | 100 | 0.20 | 200 | 134.2 | 134.2% | 216.1 | 2.16× |
| P-1000 | 120 | 1,000 | 0.12 | 120 | 805.4 | 80.5% | 1,803.6 | 1.80× |
| P-10000 | 2,000 | 10,000 | 0.20 | 200 | 13,422.8 | 134.2% | 19,524.2 | 1.95× |

The complete floor uses the budget’s own evidence choices, including its 500 Wh/kg battery assumption; it is separate from the 149 Wh/kg reference-pack comparison.

This comparison comes from [battery-ratios.json](../analysis/battery-ratios.json), configuration and the generated mass budget. It does not establish a buildable pack or a complete aircraft.
<!-- battery:ratios:end -->

Against the 149 Wh/kg pack NASA actually flew, the class-specific reference masses
are in the generated table.

Read alongside `notes/jenett-2019-lattice-vacuum-airship.md`, which finds the bare lattice shell
already 12% over the same allowance, these are independent component comparisons. The
generated totals above assess the complete nominal floor under its own evidence assumptions.

## Where it does not close the argument

The paper is about aviation packs designed for crash loads, altitude and certification, at
kilowatt-hour scale. A 2,000 MWh pack is six orders of magnitude larger, and at that size some
overheads amortise: containment walls scale with area rather than volume, and a hull with 22
million m³ of internal space has thermal options a wing box does not. Grid-scale stationary packs
already beat aviation packs on mass fraction for exactly this reason.

It also assumes cylindrical cells in modules of the X-57 type. Nothing here rules out a structural
battery that is also part of the hull, which is the only architecture that would make the mass
budget close — and which nobody has built at any scale.
