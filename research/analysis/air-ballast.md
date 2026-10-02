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
| P-100 | 1.83 t | 0.824 MWh | 0.658 MWh | **47.3%** |
| P-1000 | 7.49 t | 3.371 MWh | 2.696 MWh | 31.9% |
| P-10000 | 21.12 t | 9.504 MWh | 7.604 MWh | 14.0% |

Correction, 2026-10-02: the regenerated shares replace 52.5%, 36.4% and 16.6%.
The cycle energy used as the denominator comes from the earlier flight model.
The historical argument below has not been recomputed here.

Over half of a P-100's published cycle energy is liquefaction, and it is invisible: `plan.js`
adds `eCryo` to `E.RETURN_TRANSIT`, so a ledger reporting 0.938 MWh against "return transit" is
reporting 0.114 MWh of flying and 0.824 MWh of refrigeration.

It is also unnecessary. `plan.js:64` makes `ln2MakeT` whatever the plant can produce in the
time available — capacity times duration, not demand — so the ship refrigerates because it
*can*. The descent does not need it, because the anchor is already sized to take 90% of the
hold:

| | surplus at the source | anchor | left for the rotors | rotor capacity | margin |
|---|---|---|---|---|---|
| P-100 | 137.4 t | 125 t | 12.4 t | 267.2 t | **21.5×** |
| P-1000 | 1,374.4 t | 1,250 t | 124.4 t | 1,318.1 t | 10.6× |
| P-10000 | 13,743.6 t | 12,400 t | 1,343.6 t | 12,666.2 t | 9.4× |

**Recommendation: keep the plant and the tank, and stop running them in the normal cycle.**
Liquefy on the ground, or when idle, or when the forecast says the ship may need to come down
unpowered — not on every return leg. The plant's job is the emergency; the anchor's job is the
cycle; and at present the ship pays for both every 34 minutes.

## Read this next to `descent.md`, because the two corrections nearly cancel

They use different denominators and must not be quoted separately:

| | P-100 cycle |
|---|---|
| as published | 1.253 MWh |
| stop making nitrogen in the cycle | −0.658 |
| price the letdown honestly (`descent.md`) | +0.622 |
| **both** | **1.217 MWh — about 3% below published, not 52% below** |

The nitrogen saving is real and the letdown correction is real, and together they very nearly
swap one error for another. Neither number means anything on its own.
