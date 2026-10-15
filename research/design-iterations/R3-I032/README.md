# R3-I032 — taller upper D1 barrels + shortened lower D2 barrels with paid upper-storage/transfer

Unit r3-i032. Base: landed75 `3e4ba19d705c992700caba9c03316ca2c4b7af4f`
(tree `d5bed71921eb565274fd2ec9a102bb79d518c3e1`), branch `i032-successor-1014`.
Owner: worker-pinkrobotics-6212eb3a406be37a. Started 2026-10-14 — actual start
UNKNOWN (bounded 16:50:51–16:52:16 PDT by order and start-ack ingestion; first
owned construction receipt 16:54:05 PDT). The nominal 16:53:00 start figure is
withdrawn.

**STATUS: CONTROL STOP at the pre-calculation guard — zero numerical results.**
The frozen design and its partial priced hardware assumptions are below;
complete mass and all derived candidate outcomes remain UNKNOWN. The new
calculator `tanks.py` never reached its first numerical section; both
unsuccessful payload starts are preserved (details under *Execution
limitation*), and the unused third start is not released. **No `tanks.json`
exists. Every quantitative screen of this candidate is UNKNOWN.** Numbers
quoted below are preserved as withdrawn historical hand estimates, not
candidate results.

> The unexecuted calculator contains demonstrated mass-boundary, D2 exchange,
> support-load and freeboard-datum defects. Its formulas and the original hand
> estimates are archival, not verified results. Complete mass/delta/lift
> margins, total pickup forces and moments, structural adequacy, D2 total
> inventory/headroom/trim, exchange flow/timing and usable capacity are not
> established. No favourable screen or physical float is claimed. The source
> and baseline remain unchanged; this text withdraws claims rather than
> repairing their implementation.

## Frozen design (inputs, not results)

Two upper D1 barrels: OD 3.05 m, straight 4.20 m, two oblate heads 0.30 m each.
Two lower D2 barrels: OD 3.05 m, straight 3.00 m, same heads. 3 mm 5083-class
plate; 60 mm freeboard — the specified input allowance, not an achieved
freeboard; two flow-through baffles per tank (8 × 150 mm ports each); apex
drains. Stations exactly I017 (upper z = −19.0 m, lower z = −21.5 m, x = ±14 m,
y = ±11 m on the diagonals); two bands + one adapter per tank into the
inherited pickup datums; statics convention (declared input): each of the two
pickup datums carries W/2 per tank — no additional halving; the archived
implementation supplies water-only contributions; full tank/hardware
deadloads and their moments have not been included.

The unexecuted `freeboard_actual_m` mixes a bottom-head-offset liquid level
with a barrel-length-only top reference. That field is withdrawn;
consistent-datum freeboard and usable capacity remain UNKNOWN (tanks.py
104–114).

```
   upper D1 barrel (x2)                 lower D2 barrel (x2)
   OD 3.05, wall 3 mm                   OD 3.05, wall 3 mm
   |<------ 4.20 ------>|               |<-- 3.00 -->|
        ____                ____
       /    \  oblate      /    \            heads 0.30 m outer depth each,
      |      | head 0.30  |      |           same 3 mm plate, both ends
      |      |            |      |
      |      | 4.20       |      | 3.00     centre z: upper −19.0
      |      | straight   |      |           lower −21.5
      |      |            |      |
       \____/              \____/            hull: circular midbody R 27.5 m
                                              floor −27.5 m (I017 record)
   initial water: 30 t each upper, 20 t each lower (100 t mission unchanged)
   transfer: pump per same-frame pair, 20 kg/s @ 0.20 MPa (frozen assumption)
```

Inventory schedule (issued freeze, inputs only): D1 removes 25 t per upper (no
transfer before/during D1) → 5 t upper / 20 t lower each. During D2, per pair
at cumulative delivery x ∈ [0,25] t: upper = 5 − 0.2x, lower = 20 − 0.8x —
issued as outgoing delivery-water commands only, not total onboard water and
not receiving headroom (frozen input values retained without endorsement).
Return routing unchanged: 25 t per upper at D1 + 0.45 t per lower at D2. 6.5 h
moored reset earliest; 18.9 MJ partial energy accounting carried; new
transfer/reset duty additional.

> Those equations exhaust only represented outgoing delivery water. Concurrent
> scoop countermass is omitted, so total inventory, receiver headroom, trim and
> exchange compatibility remain UNKNOWN. The inherited D2 comparison is the
> rate-matched 45-minute concurrent exchange, not a nine-minute drain or
> sequential-pair substitute. The later return-fill row does not account for
> this concurrent pickup.

Hardware priced before any execution — a partial priced subtotal, not a
complete bill (masses declared ±50 % assumptions unless a recorded line):
bands 2 × 15.3 kg per tank; adapter 45 kg per tank (construction UNKNOWN; the
I017 0.10 t pickup-fittings line stays PENDING — the retained/replaced
pickup-fitting boundary is unresolved and the omission cannot be treated as
retirement or a complete bill; the source subtracts the complete I017 set
while omitting unresolved pickup fittings from its replacement sum,
tanks.py 149–161; the baseline's PENDING adapter note remains an explicitly
qualified historical input, not corrected data); transfer per pair: pump
45 kg, 25 m of 80/74 mm steel pipe (~5.7 kg/m), 2 × 15 kg valves, 12 kg
wiring; vent/drain 8 kg per tank; fitout 95 kg per tank (I017 datum);
retained I017 lines (valves/doors/orifices/piping/cross-pump/ducts/wiring/
grating 2.37 t + empty-bay structure 0.71 t + fasteners 0.10 t). Complete
tank-set/DRY mass, delta and dependent lift/floor/ceiling margins remain
UNKNOWN.

## Withdrawn historical hand estimates — not candidate results

Preserved only as historical worker notes made before execution; every
conclusion below is withdrawn — all PASS and headroom claims, total pickup
and stress adequacy, mass/lift/margin figures and transfer-timing adequacy:

- Usable volume ≈ 31.5 m³ upper / 22.8 m³ lower vs required 30.0 / 20.0
  (withdrawn 5 % / 14 % headroom PASS claims — consistent-datum freeboard and
  usable capacity remain UNKNOWN, see `freeboard_actual_m` above).
- New tank set ≈ 2.07 t + transfer hardware ≈ 0.46 t; set delta vs I017's
  6.0 t drawn set ≈ +0.23 t; DRY ≈ 66.41 t; n1 ≈ 111,600 m³ (floor clearance
  anchor ≈ +1,600 m³ vs I017's +1,338); ceiling margin ≈ +9.6 t anchor /
  +7.6 t drawn — all withdrawn; complete mass/delta and margins UNKNOWN.
- Hydrostatics: upper bottom pressure ≈ 41 kPa, hoop ≈ 21 MPa (withdrawn
  adequacy comparison against the 90 MPa weld datum); pickup ≈ 147 kN per
  datum at 30 t fill — a withdrawn unverified water-only hand contribution,
  not a total pickup reaction; full tank/hardware deadloads and moments not
  included; total forces/moments, support stress and adequacy UNKNOWN.
- Fit: worst lower corner ≈ 26.45 m radial → ≈ 1.05 m clearance vs the
  declared 0.50 m minimum — withdrawn and unverified, not an established fit
  witness; all fit remains UNKNOWN.
- Transfer: need ≈ 9.3 kg/s vs the 20 kg/s rating, head ≈ 0.017 MPa vs
  0.20 MPa, ~9 min linear drain (both nominally PASS) — withdrawn;
  delivery-only equations; concurrent-exchange flow/timing adequacy UNKNOWN.
  The frozen pump/pipe selections and mission are not modified to make them
  pass.

## What is known vs unknown

- **Demonstrated FAIL (inherited, unchanged):** economics 35.1× vs SEAT;
  off-nominal fuel shortfalls 0.245112 t (33-min) and 0.350732 t (half-pump).
  No physical float is shown anywhere in the programme.
- **UNKNOWN (this unit, complete):** complete tank-set/DRY mass, delta and all
  lift/floor/ceiling margins; usable capacity and consistent-datum freeboard;
  all fit (no fit exception — the 1.05 m containment note above is withdrawn);
  total pickup forces/moments and support stresses/adequacy; D2 total
  inventory, receiver headroom, trim and concurrent-exchange flow/timing —
  plus the inherited UNKNOWNs (occupancy/bag envelope, curtain attachment,
  valve spec, one-empty recovery at min-air, transients, transition-energy
  closure, bonded-socket split).
- **Predecessor carried:** I017 comparison values and the landed I027 archive
  remain attributed history; the I027 calculator's unit and support-load
  errata are recorded there. The intended conventions here (consistent SI,
  W/2 per pickup datum per tank, no extra halving) are declared inputs; the
  archived implementation supplies water-only contributions.

## Execution limitation

Payload start 1 (33 ms, exit 2) produced no calculation; the missing-script
explanation is worker-reported, not established by saved Python stderr.
Payload start 2 (43 ms, exit 3 GUARD-STOP) loaded baseline, then ran the
section-0 guard: its own asserts passed for the values it read — cgroup unit
path `robotics-p1.slice/r3i032-run2.service`, self-vs-init IPC inode
difference, RLIMIT_CPU 60 s, RLIMIT_AS 1 GiB and the single-thread
environment variables — and it stopped on the affinity assert, reading
`0-31` where the launcher had submitted `AllowedCPUs=28`: the requested
single-CPU narrowing did not reach the process mask. These are the guard's
observed values and assertions, not an independent measurement of every
requested control. Per the issued contract a guard failure is stop-and-report
with no retry, probe or relaunch; the unused scientific allowance (of three
starts, one consumed by start 1 and one by the guard stop) is the lead's to
dispose.

## Weakest assumption

The selected upper/lower storage can accept concurrent D2 scoop countermass
while delivering the required mission water, with physically usable receiver
headroom and a fully paid tank/support/transfer load path. Compatibility and
mass/trim sensitivity are UNKNOWN; neither delivery-only bookkeeping nor a
launcher repair establishes them.

## Next hypothesis (unissued, untested design — not authorised work here)

Test a paid dedicated countermass-receiving compartment in the emptied upper
D1 tanks, with an explicit divider, independent vent/drain/fill ports and a
segregated transfer manifold. Freeze the finite compartment allocation and
all added structure/hardware before a future unit; retain the 100 t
initial/two 50 t delivery mission and the 45-minute concurrent D2 exchange.
Charge all lost usable volume and added mass. This is a next design
hypothesis, not a fit, capacity or margin claim and not authorised work
here. No guard repair or launch is requested by this hypothesis; the current
dimensions, schedule and calculator are not revised.

## Reproduction

Not reproducible as a calculation: `python3 -B tanks.py` from this directory
would run unguarded in an uncontrolled shell (guards would stop on affinity
outside the bounded unit — exit 3 by design). The two bounded payload starts,
their guard report and all receipts are preserved in the unit's private
evidence custody.
