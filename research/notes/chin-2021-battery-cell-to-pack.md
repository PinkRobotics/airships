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

`sim/config.js` gives every class 0.2 MWh of battery per tonne of dry mass — 20 MWh on a 100 t
P-100, 120 MWh on a 1,000 t P-1000, 2,000 MWh on a 10,000 t P-10000. Turned round, that is a
demand for **200 Wh/kg at pack level before anything else is allowed to weigh anything at all**.

Against the 149 Wh/kg pack NASA actually flew, the P-10000's 2,000 MWh masses about **13,400
tonnes** — 134% of the entire dry-mass allowance, which also has to contain the hull, the rotors,
the pumps, the 15,500 t nitrogen tank's structure and an 850 m cable. The same ratio holds on all
three classes, because the specification is linear.

Read alongside `notes/jenett-2019-lattice-vacuum-airship.md`, which finds the bare lattice shell
already 12% over the same allowance, the two independent overruns are additive and each is on its
own larger than the budget.

## Where it does not close the argument

The paper is about aviation packs designed for crash loads, altitude and certification, at
kilowatt-hour scale. A 2,000 MWh pack is six orders of magnitude larger, and at that size some
overheads amortise: containment walls scale with area rather than volume, and a hull with 22
million m³ of internal space has thermal options a wing box does not. Grid-scale stationary packs
already beat aviation packs on mass fraction for exactly this reason.

It also assumes cylindrical cells in modules of the X-57 type. Nothing here rules out a structural
battery that is also part of the hull, which is the only architecture that would make the mass
budget close — and which nobody has built at any scale.
