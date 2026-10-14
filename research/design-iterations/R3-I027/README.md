# R3-I027 — four upright curved tanks (barrels) at the inherited P-100 stations

Order `ord-spock-glm-a-i027-restart-1014` (unit r3-i027). Base: frozen landing72
`e3a6f7b854ef0683fbcdacd6db330a7c3b94044b` (tree `91c7eadb15f641e918fd94faf87c70599a418363`),
branch `i027`. Owner: worker-pinkrobotics-6212eb3a406be37a. Started 2026-10-14T15:16:07-07:00.

**STATUS: CONTROL STOP at the execution cap.** All three authorized numerical
executions are consumed (one initial + two logged corrections) and the calculator
did not complete, so **no `tank.json` exists and no number below is calculator
output**. Every quantitative result in this README is hand-derived from the frozen
inputs in `baseline.json` by the formulas committed in `tank.py`, and is labeled
as such; the committed `tank.py` is the executable confirmation/refutation for a
later explicitly authorized rerun (see "Execution record"). The frozen candidate,
drawing and bill are complete; the stop is a one-line validator-tolerance defect,
not a design failure.

## Frozen candidate (drawn before calculation — see geometry.svg)

Four identical upright circular barrels replacing I017's four 3.05×3.05×2.85 m
rectangular flat-panel tanks, **centres and diagonal pairs exactly I017**:
x = ±14 m, y = ±11 m; upper row z = −19.0 m (B1-FL/B4-AR, D1 pair), lower row
z = −21.5 m (B2-FR/B3-AL, D2 pair). Outside diameter 3.05 m; straight barrel
3.60 m; two shallow ellipsoidal heads 0.30 m each (total height 4.20 m); 3 mm
5083 selected stock (same gauge and alloy as the predecessor's panels); two
internal full-circle baffles 3 mm at 1/3 and 2/3 barrel height; 60 mm freeboard
below the top-head springline (top head = ullage). Supports, paid as required new
stock: two circumferential bands 100×6 mm per tank at ±1.20 m from mid-height,
one adapter assembly per tank (band saddles + clevis + links + its fasteners)
into the two inherited pickup datums, plus band-zone doublers. No dimension was
searched and no plate thinned; if a screen fails, the failure is retained below.

## Assumptions (frozen before the first execution)

- Same I017 dry/equipment budget basis (I012: 38.77 t equipment ex-hull + 23.75 t
  gas hull − 2.34 t correction; DRY 66.18 t includes fuel). Net tank-set change
  propagates through DRY only.
- Declared allowances, each counted once: weld/seam 8 % of shell; manway 0.030 t;
  three port fittings 0.024 t; sump fitting 0.010 t with 0.030 m³ drain remainder
  debited from capacity; adapter 0.045 t; band-zone doublers 2×0.010 t;
  installation/access 0.080 t set-level (ASSUMED, flagged).
- Shallow-head surface ≈ π·a²·√(1+(c/a)²); capacity uses inner radii and inner
  head depth (0.297 m); envelope uses outer.
- Hydrostatics: internal freshwater column to the bottom-head apex (3.837 m at
  full); hoop membrane at the bottom of the straight wall p·r/t with the
  inherited 90 MPa weld-affected datum; head resultant = apex pressure ×
  projected inner area (upper bound). Salt ×1.025.
- Hull section law: linear half-width 19.9 m @ −19.0 → 17.1 m @ −21.5 (recorded),
  and below −21.5 m a **corner-calibrated taper** that exactly reproduces I017's
  recorded worst corner (1.38 m clearance at y = 12.53, z = −22.93 → 13.91 m
  half-width, 2.231 m/m). This reproduces the recorded datum; below −22.93 m it
  is extrapolation — the exact capsule law there is UNKNOWN. A linear-to-floor
  (−27.5 m) law is rejected as primary because it gives 0.51 m at that same
  recorded corner (would contradict I017's 1.38 m) but is reported as the stiff basis.
- Trim authority law (verified in-run, see below): one-direction net authority =
  min(donor bag, per-bag headroom) × air density × (1−0.164045) × 50 m lever,
  bags split 50/50, per-bag cap 55,000 m³. Recorded I017 air inventories carried
  at the three datums; the second-order air shift from the −0.65 t dry change is
  not re-derived (declared UNKNOWN sensitivity, <1 % of authority).
- Mismatch bound ±5 % rate at zero skew + 2 s pair-start skew over the ~9 min
  drain; release law, 25 m whole-craft restoring arm (assumed, not a derived
  CoM) and heel scaling inherited unchanged.

## Execution record (cap 3/3, all receipts in worker evidence)

| run | outcome |
|-----|---------|
| 1 | exit 2 at validation V2 D1-end: reproduced 1548.6 vs recorded 650.8. **Defect A** — `baseline.json` carried the recorded air density 0.9572 (kg/m³) under a t/m³ key (1000× unit transcription error). It passed V2 min-air spuriously (density cancels on the donor bound). Corrected to 0.0009572 t/m³; physical check 74.1 t / 0.0009572 = 77,419 m³ = I017's recorded 35.2 % bag. |
| 2 | exit 1 pre-science: JSON trailing comma introduced by the correction edit itself. **Defect B** — removed; no computation started. |
| 3 | exit 2 at validation V1 n1: 111,343.3 computed vs 111,338 recorded, tolerance ±5. **Defect C (unfixed, cap reached)** — the tolerance is stricter than the recorded value's own rounding: the same law reproduces recorded n0 (162,277.6 vs 162,278) exactly, and all three V2 authority reproductions PASSED in this run before the abort. The one-line fix (widen V1 n1 tolerance to ±10 m³ or compare against the recorded rounding basis) is identified but not applied or executed; it needs a later explicit targeted order. |

A sign error in the below-−21.5 m taper was caught by hand-check and fixed
BEFORE run 1 (pre-execution source edit; no execution consumed). Limits every
run: one process/thread, ulimit −t 60 CPU s, 1 GiB (−v 1048576), timeout 120 wall s,
stdin /dev/null, PYTHONDONTWRITEBYTECODE=1, TMPDIR=/mnt/scratch, /usr/bin/time -v
receipt. Actual: 0.01–0.04 s CPU, ≤33 MB RSS, all well inside limits.

**Verified in-run (run 3, before the abort):** authority law reproduces 244.5 /
651.7 / 921.8 vs recorded 244.7 / 650.8 / 922.3 (≤0.14 %); n0 law exact.
Everything below is hand-derived.

## Results — hand-derived from baseline.json by the committed formulas

**Capacity (PASS, expected).** Usable 27.13 m³/bay = barrel water 25.7615 +
bottom head 1.4409 − baffles 0.0437 − sump 0.030 ≥ 25.45 m³ required fresh
(largest per-bay inventory incl. the 50.9 t return scoop split — not the
convenient 25 t label) and ≥ 24.83 m³ salt. Ullage 6.2 % fresh. Envelope
29.21 m³/tank, 116.8 m³ set, remains unreserved from lifting gas (occupancy
UNKNOWN, carried).

**Incremental mass bill (t), before → new.**

| line | I017 | I027 |
|---|---|---|
| bay shells (4×0.751) | 3.00 | barrel 1.100 + heads 0.475 + weld 0.126 + baffles 0.465 + manway/ports/sump 0.256 = **2.422** |
| cradle saddles 4× | 0.38 | bands 0.123 + adapter 0.180 + doublers 0.080 = **0.383** (paid supports) |
| pickup fittings 8× | 0.10 | retired (adapters carry the interface; datum capacity UNKNOWN at 127.8 kN) |
| bay tie rods | 0.05 | retired (round section, no rods) |
| installation/access (ASSUMED) | — | 0.080 |
| reused unchanged (valves 0.14, doors 0.16, orifices 0.06, piping 0.41, pump 0.35, ducts+fans 0.75, controls 0.30, grating 0.20) | 2.37 | 2.37 |
| interface fasteners (fit to adapters UNKNOWN) | 0.10 | 0.10 |
| **set total** | **6.00** | **5.354** |

Δ = **−0.646 t** known stock. **DRY 65.53 t** (was 66.18), loaded 165.53 t.
Required-but-unsized, exposed not assumed away: curtain-fitting reinforcement
beyond adapter stock (cannot be sized — attachment qualification UNKNOWN).

**Lift/margin (matching basis: same 1.02404 t per 1000 m³ law).** n0 = 161,645 m³
(was 162,278; net displaced mixture at S0 **−633 m³**); D1-end n1 = 110,713 m³ —
**713 m³ above the 110,000 m³ anchor floor** (3,166 m³ above the 107,547 m³
drawn-volume floor), so the vent identity (n0−n1 = 50,932 ≈ recorded 50,940,
dry-independent while floor-clear) still applies. Margin at max inventory
**+10.45 t anchor / +8.49 t drawn** (was +9.80). **The trade:** the lighter set
lifts n1's slack into the bag — base-arrival bag 109,287 m³ = 49.7 % of V =
**99.4 % of the 110,000 m³ installed cap**; floor/cap headroom halves, 1,338 → 713 m³
(the same 110,000 line seen from both sides). Floor re-binds below DRY 64.81 t —
a further −0.72 t of hardware, not a present failure. At 5 mm plate the set is
HEAVIER than I017 (DRY 66.98, margin +9.00): the candidate's case rests on 3 mm
membrane adequacy. Adapter ×2 costs 0.18 t (margin +10.27).

**Loads/states.** Bottom pressure 37.7 kPa fresh / 38.6 salt; **hoop 18.1 MPa
salt = 20 % of the 90 MPa weld-affected datum** — genuine membrane action vs the
predecessor's withdrawn flat-panel check, but membrane alone proves no head
bending, weld/seam, buckling or load introduction. Head resultant 273.6/280.5 kN
(capacity UNKNOWN). Full-bay pickup reaction **127.8 kN per datum** (recorded
datum line 126 kN; +1.4 %); band line load 13.3 kN/m each band (local shell
bending UNKNOWN). Skew-inclusive mismatch bound 1.367 t → roll 15.0 / pitch
19.1 t·m = 2.9 % of the 650.8 t·m D1-end authority. One-bay-empty (hardware
stays, 25.45 t released): roll 280.0 / pitch 356.3 t·m = 39 % of the 922.3 t·m
one-empty authority, but 1.46× the 244.7 t·m min-air bound — recovery there
remains UNKNOWN (carried from I012/I017). Heel 0.16° / 3.04° on the assumed 25 m
arm. S7 reset: n_S7 = n0 both species, earliest 6.50 h; moored reset and
partial-energy qualification retained — no turnaround or energy-closure claim.

**Fit (MARGINAL-FAIL, expected — the honest debit).** Upper row: 5.36 m min
clearance. Lower row: the barrel bottom-head region sits below the last recorded
section datum; on the corner-calibrated taper the minimum is **0.43 m at
z ≈ −23.45 m vs the declared 0.50 m minimum** (short by 0.07 m; the head springline
at −23.30 m clears by 0.56 m). On the rejected stiff linear-to-floor basis it
would interfere by 0.79 m. The verdict is extrapolation-dependent: **exact hull
section law below −21.5 m UNKNOWN** — this is the specific tank variable the next
iteration must resolve, and no dimension was changed here to chase a pass.

## Screens (hand-derived; calculator confirmation pending the authorized rerun)

capacity **PASS** · mass **PASS** (−0.646 t) · hoop **PASS** (20 % of datum) ·
floor **PASS** (713 m³ anchor, 3,166 drawn) · ceiling **PASS** (+10.45/+8.49) ·
trim mismatch **PASS** (2.9 %) · trim one-empty **PASS** vs 922.3, UNKNOWN
recovery at min-air · fit **MARGINAL-FAIL** (0.43 < 0.50, extrapolated law).

Carried unchanged: economics **FAIL 35.1×** SEAT ($5,929/t); fuel **FAIL**
0.245112 t (33-min) / 0.350732 t (half-pump) — no directly changed ledger input.
Carried UNKNOWN: curtain support/load introduction (weakest, below), hull law
below −21.5 m, head seam/weld, band shell bending/buckling, pickup fitting
capacity, occupancy/bag shape, one-empty min-air recovery, slosh/transient,
valve spec, transition energy, installation allowance and I007 sundries scale.

## Weakest assumption — support/load introduction into the curtain system

As the order predicted: the two bands + one adapter per tank are *priced* stock,
but how 127.8 kN per datum enters the declared curtain planes (x = 0, ±7, ±14 m)
through the inherited fittings is unsized and unqualified — local shell bending,
weld capacity and curtain-fitting reinforcement are all UNKNOWN. Sensitivity:
adapter ×2 costs only 0.18 t, so qualification will not be saved by mass; it is a
structural-closure question, not a budget one.

## Assumption-confirmation ledger

| assumption | status |
|---|---|
| authority law form | CONFIRMED in-run vs all three recorded I017 datums (≤0.14 %) |
| lift law (n0) | CONFIRMED in-run exact vs recorded 162,278 |
| recorded n1 reproduction | NOT CONFIRMED — off 5.3 m³ (0.005 %); recorded-value rounding, defect C |
| section law below −21.5 m | NOT CONFIRMED — single corner datum calibrates it; extrapolation |
| hoop ≤ 90 MPa datum | expected PASS, hand-derived; membrane-only limit declared |
| all bill/ledger/fit numbers | hand-derived from frozen inputs; pending authorized calculator rerun |

## Next change

1. (execution, needs lead's targeted order) apply the one-line V1 tolerance fix
   and rerun `tank.py` once — everything else is already verified in-run.
2. (design) resolve the actual capsule section law below −21.5 m; if it confirms
   interference, shorten the lower-row straight barrel (3.60 → ~3.00 m restores
   >1 m clearance) and re-split the 50.9 t scoop allocation across the D1 bays so
   each D2 bay still carries ≥ its required inventory — then the paid
   curtain-fan attachment construction.

## Scoreboard (≤180 chars)

`P100 I027 4x barrel OD3.05 H4.20 3mm5083: DRY 65.53 (-0.65) margin +10.45 anchor; lower-head fit 0.43<0.50 MARGINAL-FAIL(interp); load-intro UNKNOWN; float not shown`

Reproduction (from this directory): `python3 tank.py` — exits 2 at V1 n1 with the
cap record; frozen inputs `baseline.json`, provenance `sources.json`, drawing
`geometry.svg`. Hand-derived numbers above are reproducible from those files by
the formulas in `tank.py`.
