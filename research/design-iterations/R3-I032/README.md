# R3-I032 — taller upper D1 barrels + shortened lower D2 barrels with paid upper-storage/transfer

Unit r3-i032. Base: landed75 `3e4ba19d705c992700caba9c03316ca2c4b7af4f`
(tree `d5bed71921eb565274fd2ec9a102bb79d518c3e1`), branch `i032-successor-1014`.
Owner: worker-pinkrobotics-6212eb3a406be37a. Started 2026-10-14T16:53:00-07:00.

**STATUS: CONTROL STOP at the pre-calculation guard — zero numerical results.**
The frozen design and its complete paid hardware bill are below; the new
calculator `tanks.py` never reached its first numerical section. Payload start 1
died in 33 ms on a launcher working-directory defect (python could not open the
source; no calculation began). Payload start 2 reached the section-0 control
guard, which PASSED cgroup placement (`robotics-p1.slice/r3i032-run2.service`),
IPC-namespace unsharing, RLIMIT_CPU 60 s, RLIMIT_AS 1 GiB and the single-thread
environment — and STOPPED because the required single-CPU affinity narrowing
(`AllowedCPUs=28`) did not reach the process mask (read `0-31`). Per the issued
contract a guard failure is stop-and-report with no retry, probe or relaunch;
the unused scientific allowance (of three starts, one consumed by the launcher
defect and one by the separately-recorded guard stop) is the lead's to dispose.
**No `tanks.json` exists. Every quantitative screen of this candidate is
UNKNOWN.** Numbers quoted below are worker hand derivations from the frozen
inputs, labelled as such and verified by nothing.

## Frozen design (inputs, not results)

Two upper D1 barrels: OD 3.05 m, straight 4.20 m, two oblate heads 0.30 m each.
Two lower D2 barrels: OD 3.05 m, straight 3.00 m, same heads. 3 mm 5083-class
plate; 60 mm freeboard; two flow-through baffles per tank (8 × 150 mm ports
each); apex drains. Stations exactly I017 (upper z = −19.0 m, lower
z = −21.5 m, x = ±14 m, y = ±11 m on the diagonals); two bands + one adapter
per tank into the inherited pickup datums; statics convention: each of the two
pickup datums carries W/2 per tank — no additional halving.

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

Inventory schedule (issued freeze): D1 removes 25 t per upper (no transfer
before/during D1) → 5 t upper / 20 t lower each. During D2, per pair at
cumulative delivery x ∈ [0,25] t: upper = 5 − 0.2x, lower = 20 − 0.8x (20 % of
outgoing discharge transferred continuously); at completion both empty. Return
routing unchanged: 25 t per upper at D1 + 0.45 t per lower at D2. 6.5 h moored
reset earliest; 18.9 MJ partial energy accounting carried; new transfer/reset
duty additional.

Paid hardware, frozen and priced before any execution (masses declared ±50 %
assumptions unless a recorded line): bands 2 × 15.3 kg per tank; adapter 45 kg
per tank (construction UNKNOWN; the I017 0.10 t pickup-fittings line stays
PENDING — bonded-socket split unresolved, neither retired nor charged);
transfer per pair: pump 45 kg, 25 m of 80/74 mm steel pipe (~5.7 kg/m), 2 ×
15 kg valves, 12 kg wiring; vent/drain 8 kg per tank; fitout 95 kg per tank
(I017 datum); retained I017 lines (valves/doors/orifices/piping/cross-pump/
ducts/wiring/grating 2.37 t + empty-bay structure 0.71 t + fasteners 0.10 t).

## Hand derivations (UNVERIFIED — calculator never ran)

Usable volume ≈ 31.5 m³ upper / 22.8 m³ lower vs required 30.0 / 20.0 (both
nominally PASS with 5 % / 14 % headroom). New tank set ≈ 2.07 t + transfer
hardware ≈ 0.46 t; set delta vs I017's 6.0 t drawn set ≈ +0.23 t; DRY ≈ 66.41 t;
n1 ≈ 111,600 m³ (floor clearance anchor ≈ +1,600 m³ vs I017's +1,338); ceiling
margin ≈ +9.6 t anchor / +7.6 t drawn. Hydrostatics (clean SI): upper bottom
pressure ≈ 41 kPa, hoop ≈ 21 MPa ≈ 23 % of the 90 MPa weld datum; pickup
≈ 147 kN per datum at 30 t fill. Fit (static containment witness vs the
circular R 27.5 m section only): worst lower corner ≈ 26.45 m radial → ≈ 1.05 m
clearance vs the declared 0.50 m minimum. Transfer: need ≈ 9.3 kg/s vs the
20 kg/s rating, head ≈ 0.017 MPa vs 0.20 MPa (both nominally PASS on the
recorded ~9 min linear drain). **All of these are hand figures; none is a
calculator result.**

## What is known vs unknown

- **Demonstrated FAIL (inherited, unchanged):** economics 35.1× vs SEAT;
  off-nominal fuel shortfalls 0.245112 t (33-min) and 0.350732 t (half-pump).
  No physical float is shown anywhere in the programme.
- **UNKNOWN (this unit):** every calculator screen — usable capacity, mass
  delta, lift margins, floor/ceiling, trim/authority margins for the new set,
  hoop/support numbers, fit beyond the static containment witness, transfer
  timing — plus the inherited UNKNOWNs (occupancy/bag envelope, curtain
  attachment, valve spec, one-empty recovery at min-air, transients,
  transition-energy closure, bonded-socket split).
- **Predecessor carried:** I017 comparison values and the landed I027 archive
  remain attributed history; the I027 calculator's unit and support-load
  errata are not used here (consistent-SI rewrite, no extra halving).

## Weakest assumption

That the bounded lane can actually deliver its declared CPU affinity: the
guard measured the launcher's `AllowedCPUs=28` NOT reaching the process mask,
so even the control environment of this unit is unproven until that gap is
closed — the science never got the chance to be wrong.

## Next hypothesis (unissued, unproved)

Same frozen design, executed once under a launcher whose affinity narrowing is
verified to reach the child (e.g. slice-level cpuset or an explicitly measured
mask assert at the same guard), with everything else unchanged; alternatively
the lead disposes the allowance differently. The design itself is untouched by
this stop — no dimension, material or schedule change is proposed.

## Reproduction

Not reproducible as a calculation: `python3 -B tanks.py` from this directory
would run unguarded in an uncontrolled shell (guards would stop on affinity
outside the bounded unit — exit 3 by design). The two bounded payload starts,
their guard report and all receipts are preserved in the unit's private
evidence custody.
