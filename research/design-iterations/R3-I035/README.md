# R3-I035 — Segregated upper-tank exchange chambers (finite construction)

Status: ARCHIVAL, CORRECTED AND UNREVIEWED. The saved source and output do not establish
this frozen construction's usable capacity, complete hardware mass, mass distribution,
moment/CG, or inherited authority boundaries; those quantities and every construction
margin depending on them are UNKNOWN. Saved values are historical outputs; no numerical
or physical repair occurred in this correction. The sole canonical review returned eleven
MEDIUM findings (F1–F11), all still OPEN; this correction is the last text change and it
ships UNREVIEWED under the Captain's cap (no targeted follow-up, no second review). One
supported guarded payload is an execution fact, not an adequacy claim. Nothing here is
evidence of physical adequacy, fit, or safety.

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

Selected/intended hardware (listed in [baseline.json](baseline.json); the saved mass rows in
[exchange.json](exchange.json) are defective historical pricing, not a complete paid bill):
divider plates/seating rings/T-stiffeners, sump cups, DN300 service drains with twin
isolation valves + blank + bleed, reserve draw nozzles with valves and check, separate
fresh fill and scoop fill paths (never shared), two independent DN50 vents per upper (one
per compartment, sealed sleeve through the service side, traps and drains), DN80 reset
drains per compartment, per-compartment level/pressure instrumentation and interlocked
controllers, fresh and scoop pump sets per pair, exact-node route pipe (S->P->V->F scoop;
reserve->lower inlet fresh), P-frames, clamps/brackets, and the retained inherited charges
(I017 lines, adapters, fitout allowances, cross-pump). Explicitly UNCHARGED as saved:
retained bands, divider welds, central collars, reserve-vent sleeves and closure plates
(F6). The separate 350 kg cross-pump row duplicates the duty already carried by the
inherited 2.37 t group (F7); both raw rows are preserved unpriced. The saved route lengths
omit the final ascent to the lower inlet and one pair's support count is priced once while
routes are doubled, so the saved route/clamp accounting — including the "31 clamps" exact
count — is withdrawn (F8).

## What was run

`exchange.py` (stdlib only) was executed once under a private guarded launcher
(one-CPU cgroup quota, 1 GiB memory + address-space caps, swap off, 16-task cap,
private IPC namespace, fixed single CPU, no threads, /dev/null stdin, bytecode off,
input hashes re-verified by the guard before exec). Exit 0, all pre-execution controls
observed PASS. That is an execution fact only. Sources and bindings:
[sources.json](sources.json).

## Saved results (withdrawn and retained)

- **Usable-capacity PASS is WITHDRAWN (F1).** The saved 6.455/26.030/24.241 m³
  comparisons and the 0.58 m³ / 2.2% service margins do not establish capacity: an
  apex-based head volume is applied to tangent-based liquid heights, divider faces use
  inconsistent offsets, and segregated interiors and submerged stock displacement are
  absent (exchange.py:36–39, 71–116). No replacement integral, capacity or margin is
  offered; usable capacity is UNKNOWN.
- **Retained as command-law results only:** the fixed nominal command schedule and the
  eight fixed skew cases, which remain TIMING FAILs at T=2700 s (fresh shortfalls
  1250.0–1290.4 kg, scoop shortfalls 1272.5–1290.4 kg), reported not repaired. The sole
  reviewer found no demonstrated defect in the command/clamping law; this is not
  mission-execution or physical-capacity proof. The design freeze fixes T; D2 stays
  2700 s; unfinished business at T is a FAIL, never a permitted extension.
- **The "8.991 t dry total" complete-bill claim is WITHDRAWN (F2, F3, F4, F5, F7).**
  The saved subtotal is defective: the `unit pipes/nozzles x2` row is −11.81 kg from
  signed vent differences used as lengths; the listed 227.78 kg lower-baffle and
  126.76 kg DN300 drain rows are missing from DRY; a full closed oblate-spheroid area
  is charged twice for two half-heads; the steel sump is priced with aluminium density;
  and the 350 kg cross-pump row duplicates inherited duty. Raw signed rows are preserved
  unchanged in [exchange.json](exchange.json); the complete corrected dry bill, pickup
  deadweight, whole-vehicle subtotal and all construction margins are UNKNOWN.
- **Computed fluid states, liquid/relocation CG, nominal roll/pitch and the D1 boundary
  moment are WITHDRAWN as construction results (F9, F10).** They are incomplete
  fixed-point historical approximations: half/full service inventories share one fixed
  centroid, hardware and pipe water are absent from the state gravity, no complete
  aggregate wrench is formed, opposite-signed station arms were added same-sign, and the
  D1 expression uses the opposite-side separation as an origin arm. UNKNOWN pickup
  sharing does not qualify them.
- **Inherited authority boundaries are mislabelled in public text (F11).** The 922.3 t·m
  datum is the one-bay-empty **mid-D1** authority, not D2_end; the so-called
  ceiling/floor caps are total/per-bag caps. baseline.json:151–152 and the saved output
  remain unchanged historical mislabels; no replacement cap or inherited acceptance is
  claimed.
- Inherited FAILs remain: economics 35.1x vs SEAT, fuel shortfalls 0.245/0.351 t. The
  moored reset/partial-energy scope is preserved; the withdrawn I032 hand numbers remain
  withdrawn; no accepted tanks data is fabricated.

## Honesty ledger

Every unproved property stays UNKNOWN in [exchange.json](exchange.json): fit in hull,
divider both-direction pressure/structural adequacy, vent P/V qualification, switch-event
actuation/drainage/contamination/duration, valve capacity, transients/anti-slosh adequacy
of the repartitioned baffles, occupancy/bag shape, one-empty minimum-air recovery, full
energy closure. No favourable screen or physical float is claimed; the geometric capacity
check itself is withdrawn (F1), so no capacity margin of any size stands.

## Weakest assumption

Whether the actual partitioned tanks and fully segregated plumbing leave usable capacity
at all while transmitting concurrent liquid loads through a complete paid support system.
The saved capacity margin is unestablished (F1); no thin-margin number from this unit is
treated as real.

## Next unissued hypothesis

A fully paid **external small reserve tank** replacing the 5 t internal freshwater reserve,
returning the lost upper-barrel volume to scoop service. Unissued, untested DESIGN
hypothesis only; a separate frozen unit would be required.

Ancestral context: [../R3-I032/README.md](../R3-I032/README.md), [../R3-I027/README.md](../R3-I027/README.md).
