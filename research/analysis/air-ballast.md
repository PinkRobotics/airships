> The retained mass-budget capture reported a 52.5% nitrogen-cycle saving under its older energy denominator; this is historical, not a current feasible-flight saving.
>
> **2026-10-01:** the retraction stands. The energy shares and rotor capacities below are regenerated; the retained historical argument does not establish feasible flight. Current record/favourable requirements are bound to `energy-closure.json` and `docs/ENERGY-CLOSURE-2026-10.md`.

# Ballast — a retraction, and the finding that survived it

> ## RETRACTED, 2026-08-10, the same day it was written.
>
> This document argued that a vacuum airship should ballast by **admitting air into the
> envelope**, deleting the cryogenic plant. **It cannot.** The hull is many *permanently
> sealed* vacuum cells. There is no valve. A cell can be cracked open, but nothing aboard can
> expel the atmosphere again, so the act is irreversible and takes that cell's lift with it
> for good. The mechanism does not exist for this vehicle.
>
> The page is kept rather than deleted, because a fix that erases the argument for it is a fix
> nobody can audit — and because the retraction is more instructive than the claim was.

## What was wrong, and why it was worth writing down anyway

The physics of the claim is fine: air admitted to an evacuated volume *does* add mass at
exactly ambient density, which *is* the ideal ballast, and it *would* be altitude-correct for
free. What was wrong was the **architecture assumption** — that the hull is one evacuable
envelope with a valve on it, rather than a cellular structure sealed at manufacture.

That assumption was not checked because **the cellular architecture is written down nowhere**:
not in `sim/config.js`, not in `docs/PHYSICS.md`, not in the README. A reader — or an analyst —
reasonably infers a single envelope from a model whose only geometric input is `dispM3`. That is
now the most important undocumented fact in the project, and it is load-bearing in the other
direction too: see `mass-budget.md`, where sealed cells are what rescues the shell from the
fineness-ratio buckling penalty.

Two independent reviews also found the mechanism would not have worked even given a valve:

- **A fail-open valve on a dead ship is a crash, not a landing.** A fully flooded hull weighs
  its structure with no buoyancy at all — about 13 m/s terminal broadside, 34 m/s nose-down.
  A 6 m/s descent needs net weight held to 3–20 t out of 245 t of displacement, which is a
  metered, closed-loop, *powered* valve on a ship the fail-safe case defines as unpowered.
- **The pumps were sized wrongly by kind.** Vacuum pumping is limited by swept volume, not by
  work: nearly all the energy is in the first decade of pressure and nearly all the volume in
  the last. Re-evacuating meant sweeping about 10⁶ m³, which is tens of tonnes of blower train,
  not the 1.8 t the power-based sizing gave.

## What the cryogenic plant is actually for

**Emergency ballast, and it is the only source a sealed-cell hull has.** A dead ship floats up,
recharges on solar, liquefies nitrogen until it is heavy enough, and lands. It is slow — 69.8
MWh and about 10.8 days on solar alone for a P-100 — and slow was always the accepted standard
for total-failure recovery. There is no alternative mechanism, which makes the plant's mass
non-negotiable and its **complete absence of any published mass estimate** the worst-supported
number in the vehicle (`mass-budget.md` carries it at 12 to 120 t across three columns).

## The finding that survives, and it is the large one

**The ship liquefies nitrogen on every normal cycle, and it does not need to.**

| | LN₂ made per cycle | energy | net of recovery | share of the published cycle |
|---|---|---|---|---|
| P-100 | 1.83 t | 0.824 MWh | 0.658 MWh | **8.0%** |
| P-1000 | 7.49 t | 3.371 MWh | 2.696 MWh | 4.3% |
| P-10000 | 21.12 t | 9.504 MWh | 7.604 MWh | 1.1% |

Correction, 2026-10-02: the regenerated shares are 8.0%, 4.3% and 1.1%, replacing 47.3%, 31.9% and 14.0%.
The force ledger raises the supplied cycle energy used as the denominator.
These prescribed cycles are infeasible, so the subtraction does not establish a flight saving.

The table attributes 8.0% of a P-100's prescribed cycle energy to net liquefaction.
The earlier sentence said over half while its table showed 47.3%.
The net nitrogen term remains 0.658 MWh; the supplied cycle energy rises from 1.391 to 8.192 MWh.
The [energy correction](../../docs/audit/26-10-02-energy-carry.md) records the dependent changes.

It is also unnecessary. `plan.js:64` makes `ln2MakeT` whatever the plant can produce in the
time available — capacity times duration, not demand — so the ship refrigerates because it
*can*. The descent does not need it, because the anchor is already sized to take 90% of the
hold:

| | surplus at the source | anchor | left for the rotors | rotor capacity | margin |
|---|---|---|---|---|---|
| P-100 | 137.4 t | 125 t | 12.4 t | 140.5 t | **11.3×** |
| P-1000 | 1,374.4 t | 1250 t | 124.4 t | 683.3 t | 5.5× |
| P-10000 | 13,743.6 t | 12400 t | 1,343.6 t | 7,079.2 t | 5.3× |

**Recommendation: keep the plant and the tank, and stop running them in the normal cycle.**
Liquefy on the ground, or when idle, or when the forecast says the ship may need to come down
unpowered — not on every return leg. The plant's job is the emergency; the anchor's job is the
cycle; and at present the ship pays for both every 34 minutes.

## Read this next to `descent.md` — the cancellation is gone

The earlier version of this note put the nitrogen saving beside the descent correction and found
they nearly cancelled: 1.253 MWh published, −0.658 for the plant, +0.622 for the letdown priced
honestly, 1.217 MWh for both. The letdown is now priced in the published budget itself
(`sim/power.js`, 2026-10-01; `docs/ENERGY-MODEL-2026-10.md`), so there is nothing left to cancel
against:

| | P-100 cycle |
|---|---|
| supplied effort on the prescribed profile | 8.192 MWh |
| stop making nitrogen in the cycle | −0.658 |
| **arithmetic after subtracting net refrigeration** | **7.534 MWh — 8.0% below supplied effort** |

The nitrogen subtraction is 8.0%, 4.3% and 1.1% of the three prescribed cycle energies.
These shares do not establish feasible delivery; the subtraction does not replan the cycle. (The subtraction is `mass-budget.py`'s: it
removes the plant's net energy and does not re-fly the descent with 1.83 t less nitrogen aboard,
which would cost the rotors slightly more.)
