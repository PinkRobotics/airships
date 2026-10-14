# R3-I027 — four upright curved tanks (barrels) at the inherited P-100 stations

Order `ord-spock-glm-a-i027-restart-1014` (unit r3-i027). Base: frozen landing72
`e3a6f7b854ef0683fbcdacd6db330a7c3b94044b` (tree `91c7eadb15f641e918fd94faf87c70599a418363`),
branch `i027`. Owner: worker-pinkrobotics-6212eb3a406be37a. Started 2026-10-14T15:16:07-07:00.

**STATUS: incomplete / UNKNOWN attempted construction.** Three authorized
numerical attempts are exhausted (two partial numerical runs exiting at coded
validation assertions, one input-load failure before any numerical section).
**No `tank.json` was ever produced, and no complete mass/lift/trim result
exists for this candidate.** This README was corrected once, documentation
only, after the unit's sole canonical static review; the withdrawn claims are
listed with their reasons below and remain visible rather than erased. The
committed calculator and drawing are preserved as the **original defective/
incomplete attempted construction** — not a supported calculation and not a
build drawing. No fourth numerical run, source repair, redraw or preview was
authorized or performed.

## Attempted candidate (as frozen before the first execution)

Four identical upright circular barrels to replace I017's four 3.05×3.05×2.85 m
rectangular flat-panel tanks, centres and diagonal pairs exactly I017:
x = ±14 m, y = ±11 m; upper row z = −19.0 m (B1-FL/B4-AR, D1 pair), lower row
z = −21.5 m (B2-FR/B3-AL, D2 pair). Outside diameter 3.05 m; straight barrel
3.60 m; two shallow ellipsoidal heads 0.30 m each (total height 4.20 m); 3 mm
5083 selected stock; two internal full-circle baffles 3 mm at 1/3 and 2/3
barrel height; 60 mm freeboard. Supports priced as required new stock: two
circumferential bands 100×6 mm per tank and one adapter assembly per tank
(0.045 t allowance) into the two inherited pickup datums. No dimension was
searched and no plate thinned during the iteration.

## Execution record (3/3 attempts consumed; no run completed)

| run | outcome |
|-----|---------|
| 1 | exit 2 at the coded V2 D1-end assertion: my `baseline.json` carried the recorded air density 0.9572 (kg/m³) under a t/m³ key — a 1000× transcription error. Corrected in the input; re-run consumed attempt 2. |
| 2 | exit 1 before any numerical section: JSON trailing comma introduced by my own correction edit. Run 2's input was the intermediate (never-committed) baseline hash `44e740f2…`, bytes absent — see `sources.json`. |
| 3 | exit 2 at the coded V1 n1 assertion (`tank.py` line 136), **after** the numerical sections 1–4 and the coded V1 n0 assertion had executed. The ledger, fit scan, V3, sensitivities, screens and the result writer were **never reached**. |

What actually happened inside run 3, stated precisely: the coded V2 assertions
(all three authority reproductions) and the coded V1 n0 assertion **passed
inside the process** — but the raw saved stdout never printed the asserted
values, so the earlier README claim that they were "verified in-run" with exact
figures overstated the saved evidence. Nothing beyond the stopping point was
computed by the calculator. Every number in this README is worker hand
derivation or a copied predecessor value, and is labeled as such; `tank.json`
never existed. Historical enforcement is likewise incompletely demonstrated:
the saved pre-run note declares ulimit/timeout/stdin/environment and `/usr/bin/time`
totals, but no complete launcher or measured affinity/cgroup/swap/IPC/rlimit
record was preserved — the totals do not prove isolation. The runs predate the
prospective bwrap launch control, which cures nothing retroactively.

## Withdrawn claims (sole canonical review; correction is documentation-only)

**W1 — tank-body fit "0.43 m MARGINAL-FAIL" and the corner-calibrated taper
law: WITHDRAWN as unsupported.** The fit scan turned I017's *radial* clearance
record into an invented horizontal half-width taper. The inherited frozen
section is a **circular midbody of radius 27.5 m** across this tank's x extent.
A conservative static check of the lower tank's worst point
(12.525² + 23.60² = 713.8 < 27.5²) contradicts the claimed tank-body failure —
the barrel body does not approach the hull skin on that section. This
withdrawal does **not** establish construction fit: adapter, neighbouring
hardware, gas-bag and whole-system occupancy remain UNKNOWN, and no fit PASS
is claimed.

**W2 — calculator pressure/force outputs: INVALIDATED, not repaired.** The
archived executable multiplies tonne-based densities by g and height (which
already yields kPa) and by tonnes·g (which already yields kN), then applies
Pa/N conversions as if the inputs were kg-based — understating pressure, hoop
stress, head resultants and pickup loads by **1000× in their stated units**,
with the same mismatch in the allowable comparison. The affected calculator
outputs and screens are erroneous and unvalidated; no repair was executed (the
execution cap is exhausted). The hand figures previously quoted in this README
(37.7 kPa bottom pressure, 18.1 MPa hoop, 273.6 kN head resultant, 127.8 kN
pickups) are correct-unit **hand derivations**, but nothing about them was
verified by this source, and their adequacy claims (e.g. "20 % of the 90 MPa
weld-affected datum") are withdrawn. Strength/seam/buckling/introduction
capacity remains UNKNOWN.

**W3 — band line load 13.3 kN/m: WITHDRAWN.** The archived expression carries
an extra halving: with bay weight W it sets each pickup reaction to W/2 and
then each band load to half of that, so the two declared band loads sum to only
W/2 — they do not balance the bay. 13.3 kN/m is not an established design
load. Support equilibrium, local shell bending and band/adapter connections are
UNKNOWN; no new band calculation is assigned or performed.

**W4 — geometry.svg is the original flawed schematic; kept for the record.**
Its exact bytes are preserved unchanged, and it must not be read as a dimensioned
construction drawing: one of the two support bands is drawn **below the tank**
(the tank occupies y = 10…430 in drawing coordinates with bands correctly at
100/340 for ±1.20 m; one was placed at 520), and the "adapter assembly" is
linework over a 0.045 t allowance with no finite stock and no dimensioned
connection to the two inherited pickup datums. Any claim of complete
dimensioned construction, adapter extrema/fit, or a complete paid support bill
is withdrawn. No redraw belongs to this exhausted iteration.

**W5 — complete retirement of the 0.10 t pickup-fittings line and the complete
−0.646 t set saving: WITHDRAWN.** The retired I017 0.10 t line includes clevises
**and bonded sockets**, and bonded sockets remain load-path hardware; the
retained/replaced split was never reconciled, and the new adapter allowance
does not name a replacement for them. The line stays pending a breakdown —
neither complete retirement nor a full 0.10 t add-back is asserted. In
consequence the candidate **dry-mass delta and the matching lift-margin update
are UNKNOWN**, not an accepted −0.646 t credit; the earlier DRY 65.53 /
margin +10.45 / +8.49 figures are withdrawn as established outputs.
Predecessor (I017/I012) quantities remain clearly attributed historical data.

**W6 — unchanged trim authorities, the "<1 % air-shift" sensitivity claim and
the derived coverage ratios: WITHDRAWN.** Changed gas/air inventory affects
both donor supply and receiver headroom (the stated −633 m³ initial inventory
implies roughly +0.775 t air at the ~11.7 t donor datum — about 6.6 %, not
<1 %). Separately, the capacity-bound 25.45 t per-bay figure is not the
unchanged 25 t-per-bay delivery state: the saved scoop routing (50.0 t D1
return + 0.9 t D2 tail) is predecessor routing, not a new allocation.
Mission-state, inventory and trim margins for **both** displacement
conventions are UNCOMPUTED/UNKNOWN and were not recalculated in this
correction. (This withdrawal does not establish a trim failure.)

**W7 — usable-capacity PASS for 27.13 m³: WITHDRAWN.** The two depicted
full-circle horizontal baffles have no communicating openings and no
compartment vent/drain routes, yet the capacity figure counted every
compartment as bottom-drain usable volume, debiting only plates and sump.
27.13 m³ is gross geometric containment, not established usable drainable
capacity. Capacity, delivery/scoop compatibility and complete construction
are unresolved pending a new explicitly paid design. No openings, routes or
fresh geometry were added to the frozen failed source.

**W8 — the proposed "3.60 → 3.00 m lower-row barrel + scoop redistribution"
next change: WITHDRAWN as a fix.** By the original expression it removes
0.60·π·1.522² m³, leaving less than 23 m³ — insufficient for either the 25 t
freshwater or saltwater D2 lower-bay delivery; redistribution of the return
scoop cannot cure initial D2 capacity. See "Next hypothesis" for what a valid
successor would have to include. It remains unissued and unproved.

## What stands after the correction

- **Demonstrated FAIL (inherited, unchanged):** economics 35.1× vs SEAT
  ($5,929/t); off-nominal fuel shortfalls 0.245112 t (33-min) and 0.350732 t
  (half-pump). No physical float is shown anywhere in the programme.
- **Carried predecessor qualifications:** moored reset and partial-energy
  qualification (no turnaround or energy-closure claim); material/strength,
  occupancy/bag-shape, one-empty min-air recovery, slosh/transient, valve spec
  and transition-energy UNKNOWNs; I017/I012 values remain attributed history.
- **This candidate:** an incomplete attempted construction — frozen geometry,
  three failed/aborted attempts, an erroneous archived calculator (W2/W3), a
  flawed schematic (W4), and **UNKNOWN** capacity, mass delta, lift margin,
  trim margins, support load path and construction fit. The earlier screens
  table (capacity/mass/hoop/floor/ceiling/trim/fit) is withdrawn in full: none
  of those screens was ever computed to completion, and several of the
  hand-derived ones depended on the withdrawn items above.
- Provenance qualifications recorded in the private append-only addendum:
  initial-vs-final baseline bindings, historical control limits, and governance
  metrics — see `sources.json` for the public input bindings.

## Weakest assumption

Support/load introduction into the declared curtain system — now twofold: the
band load path was never in equilibrium in the archived calculation (W3), and
the adapter is an allowance with no finite construction (W4). How any bay load
reaches the declared curtain planes through the inherited pickup datums
(including the unresolved bonded-socket split, W5) is unresolved.

## Next hypothesis (unissued, unproved — not asserted to work)

Shorter lower-row tanks **only** together with: explicit initial-water
redistribution, paid upper storage, a finite transfer circuit, and full
mission timing/capacity accounting — or a different capacity-preserving
construction. Any successor must define baffle openings/vent-drain routes and
their paid effects before claiming usable capacity (W7), reconcile the
pickup-fitting retained/replaced split before claiming any mass saving (W5),
recompute both displacement conventions' inventory/trim margins (W6), and use
a consistent unit basis before any strength screen (W2).

## Assumption-confirmation ledger (corrected)

| item | status |
|---|---|
| authority-law form (V2) and lift-law n0 (V1) | coded assertions passed inside run 3 before its exit; raw stdout never printed the values — worker claims, not saved output |
| everything downstream of `tank.py` line 136 (ledger, fit, sensitivities, screens, writer) | NEVER computed; no calculator output exists |
| all README quantities | hand-derived or copied predecessor data; none verified by the archived source |
| archived pressure/force/band expressions | demonstrated erroneous (W2, W3); preserved unrepaired |
| fit taper law | withdrawn (W1); inherited section is circular, radius 27.5 m |
| capacity 27.13 m³ usable | withdrawn (W7); gross containment only |
| dry-mass delta / margins | withdrawn (W5); UNKNOWN |

## Scoreboard (≤180 chars)

`P100 I027 attempted barrels 3/3 aborted, no tank.json; capacity/mass-delta/margins/trim/fit UNKNOWN; calc unit+band errata kept; econ FAIL 35.1x carried; float not shown`

Reproduction (from this directory): `python3 tank.py` exits 2 at the archived
V1 n1 assertion after sections 1–4. Frozen inputs: `baseline.json` (final
4,846 B / `5ac2d4fe…` — executed by **run 3 only**); run 2's input was the
malformed never-committed intermediate `44e740f2…` (hash-only: a trailing
comma my unit-fix edit introduced; bytes absent), and run 1's was the initial
`a06b321a…`. Provenance: `sources.json`; flawed original schematic:
`geometry.svg`. The calculator's known unit and load-path errors (W2, W3) are
preserved deliberately — repairing them needs a new authorized execution.
