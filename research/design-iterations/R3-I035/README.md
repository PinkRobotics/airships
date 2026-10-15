# R3-I035 — Segregated upper-tank exchange chambers (finite construction)

Status: CONSTRUCTED AND CALCULATED, single guarded run, honest FAIL/UNKNOWN retained.
Nothing here is evidence of physical adequacy, fit, or safety.

## Frozen design (unchanged during this unit)

Each of the two upper countermass tanks (4.20 m straight barrel, 3.05 m OD / 3 mm wall,
oblate heads, centres z=-19.0 m) receives a fixed internal divider 0.75 m above the bottom
barrel tangent (midplane z=-20.350 m), splitting it into:

- a bottom **fresh reserve** chamber (5 t delivered-freshwater working mass), and
- a **switchable service** chamber (25 t D1 fresh, later 25.45 t scoop countermass).

The two lower tanks (3.00 m straight, centres z=-21.5 m) remain freshwater-only (20 t each).
All 50.9 t of scoop countermass is received upstairs, 25.45 t per upper service chamber; the
explicit 0.9 t relocation (0.45 t formerly in each lower) moves mass upstairs and changes
fluid heights and trim — it is not a mission-mass change and no unchanged-CG claim is made.
The original mission is unchanged: 100 t initial fresh, two 50 t deliveries, 45-minute (2700 s)
concurrent D2 window with scoop receipt, D1 timing inherited.

```
   upper tank (per pair member)                    lower tank (per pair member)
   z=-16.603  inner apex                            z=-19.703  inner apex
      |  60 mm freeboard                             |  60 mm freeboard
      |                                            20 t fresh (S0) -> 0 (D2 end)
      |  SERVICE chamber                            |
      |  25 t D1 fresh  ->  switch  ->  25.45 t scoop|
      |  2 repartitioned baffles (-19.350/-18.350)  |
      |  scoop downpipe + splash plate              |
   z=-20.350  ===== divider (6 mm + ring + 8 T) =====
      |  60 mm gas below divider                    |
      |  RESERVE chamber                            |
      |  5 t fresh, sump cup + DN300 drain passing  |
   z=-21.100  bottom tangent                      z=-23.000  bottom tangent
```

Paid hardware (full bill in [baseline.json](baseline.json), computed masses in
[exchange.json](exchange.json)): divider plates/seating rings/T-stiffeners/welds, sump cups,
DN300 service drains with twin isolation valves + blank + bleed, reserve draw nozzles with
valves and check, separate fresh fill and scoop fill paths (never shared), two independent
DN50 vents per upper (one per compartment, sealed sleeve through the service side, traps and
drains), DN80 reset drains per compartment, per-compartment level/pressure instrumentation
and interlocked controllers, fresh and scoop pump sets per pair, exact-node route pipe
(S->P->V->F scoop; reserve->lower inlet fresh, paying beyond the 25 m allowance where the
actual route is longer), P-frames, clamps/brackets at exact count, and all retained
inherited charges (I017 lines, adapters, fitout allowances, cross-pump).

## What was run

`exchange.py` (stdlib only) was executed once under a private guarded launcher
(one-CPU cgroup quota, 1 GiB memory + address-space caps, swap off, 16-task cap,
private IPC namespace, fixed single CPU, no threads, /dev/null stdin, bytecode off,
input hashes re-verified by the guard before exec). Exit 0, all pre-execution controls
observed PASS. Sources and bindings: [sources.json](sources.json).

## Results (calculation, not qualification)

- **Geometric capacity vs frozen demands: ALL PASS.** Reserve 6.455 m³ usable vs 5 t
  demand (+1.455); service 26.030 m³ vs 25.45 t (+0.580); lower 24.241 m³ vs 20 t
  (+4.241). Margins are small where noted: the service chamber clears the scoop demand
  by 0.58 m³ (2.2%) after paying every displaced volume.
- **Nominal event programme completes** inside the 2700 s window: both pairs deliver
  50 t fresh and receive 50.9 t scoop concurrently, 1:4 reserve:lower internal split.
- **All eight fixed skew cases are TIMING FAILs at T, reported not repaired.** With a
  leading pair at ±5% rate error (and the lagging pair opposite, +2 s start offset), the
  rate-degraded side of each pair cannot finish inside the window: fresh shortfalls of
  1250.0-1290.4 kg or scoop shortfalls of 1272.5-1290.4 kg remain at T=2700 s. The
  design freeze fixes T; unfinished business at T is a FAIL, never a permitted extension.
- **Complete paid hardware bill: 8.991 t dry total** (conditional: adapter attachment,
  old-frame brackets and the S-to-scoop link remain unpriced C duties, so the complete
  bill stays UNKNOWN). Part-level masses and CG z are itemised in [exchange.json](exchange.json).
- Fluid state table (S0 -> D1 end -> D2 end) and the explicit 0.9 t relocation's CG shift
  are computed; **trim/load-sharing adequacy remains UNKNOWN** (W/2 pickup convention is a
  declared ideal, not a proved load path).
- Inherited FAILs remain: economics 35.1x vs SEAT, fuel shortfalls 0.245/0.351 t.

## Honesty ledger

Every unproved property stays UNKNOWN in [exchange.json](exchange.json): fit in hull,
divider both-direction pressure/structural adequacy, vent P/V qualification, switch-event
actuation/drainage/contamination/duration, valve capacity, transients/anti-slosh adequacy
of the repartitioned baffles, occupancy/bag shape, one-empty minimum-air recovery, full
energy closure. No favourable screen, capacity margin beyond the geometric check, or
physical float is claimed. The withdrawn I032 hand numbers remain withdrawn; no accepted
tanks data is fabricated.

## Weakest assumption

That a fixed divider plus fully independent plumbing still leaves enough usable capacity
while carrying concurrent service pressure and full pickup loads — the 0.58 m³ service
margin is the thinnest number in this unit.

## Next unissued hypothesis

A fully paid **external small reserve tank** replacing the 5 t internal freshwater reserve,
returning the lost upper-barrel volume to scoop service. Not studied here; a separate frozen
unit would be required.

Ancestral context: [../R3-I032/README.md](../R3-I032/README.md), [../R3-I027/README.md](../R3-I027/README.md).
