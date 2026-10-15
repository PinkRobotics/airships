# R3-I031 — mechanically captured tapered-pot socket cartridge

Status: **ARCHIVED — construction result withdrawn.** The frozen code and saved
results do not consistently represent the drawn cartridge. Every calculated
quantity retained below is a historical output of the mismatched model, not an
achieved construction result. Complete cartridge/vehicle mass, lift/margins,
fit, bearing capacity and the dependent compliance/force propagation for the
frozen construction are **UNKNOWN**. The saved arithmetic and its negative
values are retained as history and are not converted here into a physical
claim in either direction. The canonical static review of this unit left nine
findings open — body geometry, fastener-stack fit, three bearing
interpretations, cord-length accounting, predecessor compliance,
removed-aluminium reconciliation, whole-vehicle rollup, cap-screen inference
scope and compliance denominators; this correction withdraws and attributes
the affected claims throughout this file and `sources.json`, and closes none
of them. `cartridge.py`, `cartridge.json` and `baseline.json` are unchanged —
byte and mode identical to the archived candidate; no code, number or
dimension was repaired.

Inputs pinned: `R3-I028/baseline.json` sha256
`dce7fd4d3c8650e71788a7c3e55decb0f95e8899dd43b463b12f47697aa7034e`,
`R3-I028/socket_body.json` sha256
`c20cec9156e27339c3da0469c15d9c16739add69a34d594f9c73613b6440db40`
(copied as data; never imported, executed or regenerated).

## What replaced what (drawn concept — not established by the saved results)

Only I028's adhesive-to-aluminium and unspecified aluminium female-thread axial
transfer is replaced on paper: cord → **tapered resin pot** → **frictionless 5°
cone bearing** (narrow at the cord exit, widening rear; **zero adhesive-shear
credit to aluminium**) → conical body with continuous shoulder → rear flange →
four titanium cap bolts with clearance holes and separate Ti nuts (**no
aluminium female thread anywhere**) → bolted cap → paid Ti bearing washer on an
isolation layer → interior titanium load nut (1.5d nominal engagement) →
titanium through-stud → retained exterior anchor interface. Radial spreading
`N·cos5°` is drawn as reacted hoop in the body wall; at the frozen fitting
demand the cone normal is **N = T/sin5° = 203 kN (d60) / 531 kN (d180/11)** —
a model value, not a measured one. The sections below withdraw the saved
capacity, fit and compliance claims made for this concept.

Retained unchanged: cord families (E 70 GPa, 970 kg/m³, strength UNKNOWN),
plane/station counts, clips, anchor blocks, doubler pads, 45/50 mm attachment
bolts, exterior jam nut and anchor interface, the pressure structure, and the
one free-cord/transfer datum. Material records remain the accepted ASSUMED
records: Al 69 GPa / 2,700 / 150 MPa working; Ti-6Al-4V 114 GPa / 4,430 /
880 MPa; resin 12 MPa shear plus this unit's frozen additions — E 3 GPa and
80 MPa compression-bearing (ASSUMED, unqualified). No qualified retirement of
anything is claimed here; inherited failures and UNKNOWNs stay visible.

## Dimensioned construction (ASCII; drawn values, d60 with d180/11 bracketed; mm)

```
        cord axis ────────────────────────────────────────────────────────────────────────►
        nose face     grip OD 23.5 [38.0] drawn over grip 60 [97]   OD 3d = 42 [69]
   ┌──────┬──────────────────────────────────────────────┬───────────────┬─────────────┬─────────┐
   │ cord │      tapered resin pot in 5° internal cone    │   chamber     │ rear flange │  cap    │
   │ 7.87 │      [12.72]                                  │  clear 2.5d   │  OD 4d,     │  OD 4d, │
   │      │      cone Ø 9.0 [14.6] at exit → 35.0 [57.5]  │  Ø35 [57.5]   │  0.5d thk   │ 0.5d    │
   └──────┴──────────────────────────────────────────────┴───────────────┴─────────────┴─────────┘
   |◄──────────────── cone 148.6 [245.2] ────────────────►|◄ 2d =28 [46]►|◄ 7 [11.5] ►|◄7 [11.5]►|
                                          OD flares 23.5→42 [38→69] behind the grip in the DRAWING
   total body 183.6 [302.7] as implemented  (old body 76 [113] — comparison value only)
   wall at chamber entrance 0.25d = 3.5 [5.75];  wall over cone = frontWall 7.25 [11.7]
```

**Drawn ≠ implemented — body geometry withdrawn for the drawn cartridge.**
The drawing retains grip OD 23.5 [38.0] over the 60 [97] mm grip and flares
behind it. The frozen calculator implements a different outer body: its OD
rule `min(max(gripOD, localConeDiameter + 2·frontWall), 3d)` exceeds the grip
OD already at the cord-exit station, so the implemented body flares outward
immediately from the exit and never holds a constant grip OD. The saved body
mass, minimum wall (saved field `geometry.min_wall_over_grip_mm`), wall /
hoop / axial capacity and body compliance describe that implemented flaring
body; they are **withdrawn as results for the drawn constant-grip
construction**. The dimensions are not modified and the grip OD is not
extended here.

```
   rear elevation (cap/flange, d60)             chamber section (d60)
        Ø56 [92]                                     wall 3.5 [5.75]
        bolt circle Ø49 [80.5]                          ┌───────────┐
        4 × Ø6.6 [10.6] clearance holes           ══════╡   clear     ╞══════
        + separate Ti nuts (no Al thread)                │  Ø35 [57.5]│
          ○   ○                                         └───────────┘
        ○   ┼   ◇  stud clearance Ø14.6 [23.6]      cone enters at left,
          ○   ○                                      chamber 2d long
   bolt-head seats drawn spot-faced/counterbored inside the 4d envelope;
   the saved head-seat screen credits a full annulus beyond the flange
   material and is withdrawn below
```

```
   interior load path at the cap (d60)          exterior (retained)
   chamber side:                                cap rear face:
   Ti stud end ─► interior load nut             stud tip 3 [14] mm + jam nut
   1.5d = 21 [34.5] nominal engagement,         + anchor block, 3 × M10 Ti
   bears through Ti washer Ø1.5d = 21 [34.5]    attachment bolts 45 [50] mm
   on paid isolation layer on cap inner face    shanks (exterior anchor
        ▼ T                                    interface unchanged)
   ═════════════ cap 0.5d ═════════════
        ▼ T                     new stud overall 31 [60] mm as priced (old
   4 × M6 [M10] Ti cap bolts            79 [127]); the priced stacks do not
   in tension, T/4 each                 close — fit withdrawn below
```

## Per-end piece count and incremental bill (kg/end — historical pricing, not an established assembly)

Per cord end, as priced: **one** conical body (shoulder/chamber/flange
integral), **one** pot, **one** cap, **four** cap bolts, **four** cap nuts,
**eight** cap washers, **one** interior load nut, **one** bearing washer;
isolation/seal stock priced at every Ti/Al contact (bolt holes, stud hole,
bearing face) in addition to the retained 0.025 kg/end provision.

| line (kg/end) | d60 | d180/11 |
|---|---:|---:|
| REMOVED: I028 aluminium body (frozen before-state) | 0.0760 | 0.2954 |
| REMOVED: machining on it (3 %) | 0.0023 | 0.0089 |
| REMOVED: old resin pot | 0.0017 | 0.0061 |
| REMOVED: old stud blank (79/127 mm) | 0.0549 | 0.2321 |
| NEW: conical body (Ø rules above, − 4 bolt holes) | 0.2947 | 1.2934 |
| NEW: cap (− 4 bolt holes − stud hole) | 0.0408 | 0.1819 |
| NEW: pot resin (frustum − embedded cord) | 0.0642 | 0.2859 |
| NEW: cap bolt stack (4 bolts + 4 nuts + 8 washers, Ti) | 0.0226 | 0.1041 |
| NEW: interior load nut + bearing washer (Ti) | 0.0311 | 0.1378 |
| NEW: stud blank (shorter, 31/60 mm, Ti) | 0.0215 | 0.1097 |
| NEW: isolation/seal stock (added interfaces, ASSUMED) | 0.0150 | 0.0350 |
| NEW: machining 3 % on new Al metal | 0.0101 | 0.0443 |
| **increment per end (saved arithmetic)** | **+0.3651** | **+1.6494** |
| × ends | 21,390 | 21,080 |
| **family increment (saved arithmetic)** | **+7.81 t** | **+34.77 t** |

**Fastener stacks do not close — fit withdrawn.** The priced stud rule
(1.5d nominal engagement + 0.5d cap + tip extension) omits the 0.1d
bearing-washer thickness — and the paid isolation — that sit between the
interior load nut and the cap before engagement; and the priced cap-bolt
shank subtracts the head height from a stack whose stated length allowance
is already consumed by its two washers, with no recess modeled. The specified
unrecessed washer/flange/cap/nut stacks do not fit the stated lengths, so the
finite fit and engagement claims are **withdrawn**, and with them the stud
saving and the bolt bill as an established assembly. Recess, isolation and
engagement details are unresolved. The priced figures above are retained as
history; the **complete new-hardware bill is UNKNOWN**.

**Removed-aluminium reconciliation (unreconciled history).** The frozen
before-state removes 0.076004 / 0.295445 kg/end of aluminium body; the
accepted I028 record carries 0.07594839509961494 / 0.29494000995555875
kg/end, and the removed-machining line (3 % on it) inherits the same
difference. The increment arithmetic is therefore not an exact
before/after reconciliation against the accepted predecessor; it and the
frozen baseline/output are retained as unreconciled history. This discrepancy
is separate from the inherited residual.

Required-but-unsized (UNKNOWN, not zero-mass): station-pitch envelope
compatibility for the 183.6/302.7 mm bodies; adjustment take-up travel; pot
moulding/insertion process stock; contact-seating shims.

## Whole-vehicle saved arithmetic (historical, unreconciled — not construction margins)

Same lift, gas, payload, pressure and mission constraints as I028. Every row
is saved model arithmetic retained as history:

| line | I028 accepted | saved arithmetic | Δ |
|---|---:|---:|---:|
| hardware increment | — | **+42.58 t** | |
| 5 % assembly share on the increment | — | +2.13 t | |
| **total increment (saved)** | | | **+44.71 t** |
| sockets line | 16.41 t | 58.99 t | +42.58 |
| whole known subtotal (conditional) | 2,229.5 t | **2,274.2 t** | +44.71 |
| **sea-level margin** | +20.3 t | **−24.4 t** | saved FAIL (hist.) |
| 2,500 m margin | −472.2 t | **−516.9 t** | saved FAIL (hist.) |
| x1.5 station-hardware increment | 14.10 t | 36.45 t | |
| stacked x1.5 sea-level | +6.22 t | **−60.9 t** | saved FAIL (hist.) |
| SF1.2 (separate d60+d20 construction) | historical FAIL | substitution UNCOMPUTED/UNKNOWN | |

**Rollup qualification.** In the saved output the whole `vehicle.spokesLineT`
line stays 241.51 t before and after, although the positive socket increment
and its 5 % assembly share appear in the other lines: the added assembly
share is applied once, in its own model line, while this subtotal is omitted
(not updated). A reconciled whole-spokes/whole-vehicle bill and the complete
construction margin are **withdrawn**; no replacement is hand-calculated here,
and the negative values above are historical arithmetic only.

U+C remains subtractive/UNKNOWN; physical float is not shown. The known
subtotal was already conditional and stays conditional.

## Screens (saved model output; fitting demand T_fit = 17.7 / 46.27 kN — inherited source observations)

| element | d60 demand | d180/11 | limit (ASSUMED) | util | saved verdict |
|---|---:|---:|---|---:|---|
| cone bearing, resin | 19.7 MPa | 19.0 MPa | 80 MPa | 0.25 | PASS (cond., model output) |
| cone bearing, aluminium | 19.7 MPa | 19.0 MPa | 150 MPa | 0.13 | PASS (cond., model output) |
| hoop (max, at chamber entrance 5p) | 98.5 MPa | 95.2 MPa | 150 MPa | 0.66 | WITHDRAWN (implemented geometry) |
| body axial (closed-form integral) | 41.8 MPa | 40.5 MPa | 150 MPa | 0.28 | WITHDRAWN (implemented geometry) |
| **cap bending (radial-strip screen)** | **459.9 MPa** | **445.5 MPa** | 150 MPa | **3.07 / 2.97** | **screen FAIL retained** |
| **cap bending at T0 service** | **176.9 MPa** | **171.3 MPa** | 150 MPa | **1.18 / 1.14** | **screen FAIL retained** |
| cap-bolt tension (4 × M6/M10 Ti) | 220.1 MPa | 199.4 MPa | 880 MPa | 0.25 | PASS (cond., model output) |
| cap-bolt bearing on Al | 105.4 MPa | 100.6 MPa | 150 MPa | 0.70 | WITHDRAWN (interpretation) |
| bolt-head seat bearing | 99.8 MPa | 94.0 MPa | 150 MPa | 0.67 | WITHDRAWN (interpretation) |
| stud tension (M14/M23) | 153.9 MPa | 138.5 MPa | 880 MPa | 0.18 | PASS (cond., model output) |
| interior load-nut stripping (1.5d) | 22.5 MPa | 21.8 MPa | 528 MPa | 0.04 | PASS (cond., model output) |
| washer bearing on cap inner face | 98.9 MPa | 93.0 MPa | 150 MPa | 0.66 | WITHDRAWN (interpretation) |
| cord-to-resin embed shear | 4.8 MPa | 4.7 MPa | 12 MPa | 0.40 | PASS (cond., model output) |

**Three bearing interpretations withdrawn.** The saved
`screens.boltBearingAl` applies the axial bolt force to a transverse
shank-bearing area (diameter × thickness); the saved `screens.headSeatBearing`
credits a complete head-seat annulus that extends beyond the flange material
available at the bolt circle; and the saved `screens.washerBearingCap`
credits contact area inside the bearing washer's actual bore. All three
conditional-PASS interpretations are **withdrawn**. Neither these witnesses
nor their withdrawal proves a replacement-capacity FAIL — the replacement
capacities are UNKNOWN. The remaining conditional screens are model outputs
and cannot restore overall construction adequacy.

The hoop and body-axial rows are withdrawn with the body geometry above: they
screen the implemented flaring body, not the drawn constant-grip construction.
The longer embed lowers the saved cord–resin screen value (13.77 MPa
inherited → 4.8/4.7 MPa) as a model output. Assembly/access as drawn: the
interior load nut passes the chamber clear bore (hex 22.4/36.8 mm vs clear
35/57.5 mm); cap bolts insert from the front with rear nuts; envelope
compatibility stays UNKNOWN.

## Series compliance (saved model output — historical, unreconciled)

The soft stage of the saved model is the **pot wedge**: axial stiffness
k_z = k_r·tan²5°, so the pot's confined radial compliance appears divided by
tan²5°.

| family | L_ser (saved) | chain denominator (saved, exact) | eta (saved) | both-end take-up (saved) |
|---|---|---|---|---:|
| d60 | 0.02104 → **0.17302 m** † | 12.2424 → **12.546349215197774** † | 1.000257 → **0.995915** † | **0.61 mm** † |
| d180/11 | 0.03322 → **0.27633 m** † | 17.3607 → **17.846918559373222** † | 1.000381 → **0.994355** † | **0.97 mm** † |

† Historical model output, unreconciled under the geometry, cord-accounting
and predecessor withdrawals below — not a response of the rebuilt cartridge.

**Cord-length accounting withdrawn.** Total cord length is the free length
plus both embedded runs. The saved chain credits the longer cone as the
embedded length while the inherited free-cord/transfer terms and the
unchanged cord mass persist, so the rebuilt cartridge has no consistent cord
datum. The complete physical denominator, eta, the n=5 declared-model force
propagation and the take-up are **withdrawn** as responses of the rebuilt
cartridge; the numerical tables above are retained only as historical model
output. Full n=2..12 class bounds, centroid/no-transfer sensitivity, global
stability and SF1.2 substitution remain UNCOMPUTED/UNKNOWN; no numerical
reconciliation is attempted here.

**Predecessor compliance withdrawn.** The saved before-state lengths
(0.02104 / 0.03322 m) are the **pre-I028 titanium** spring lengths, not the
accepted I028 state (0.025039521352712354 / 0.039170696441288136 m). The
advertised I028 before→after transition, effective-length change and
restoration take-up are **withdrawn**; that historical intermediate is not
the accepted predecessor comparison. The equations are not replaced and no
new transition is calculated.

Saved-model detail retained as history: tension at unchanged imposed
extension falls 6.809 → 6.644 kN and 17.797 → 17.312 kN; the take-up
demand's availability is UNKNOWN (no free installation-after-evacuation is
claimed); n=5 declared-model first-slack scales by the saved denominator
ratio (e.g. d60 −cos5 26.6213 → 27.2822 mm; all four packets in
`cartridge.json`); chord-basis tables stay unchanged historical comparators.
The coupled eigen margin is not recomputed (dependent UNKNOWN). The R3-I023
equilibrium closure stays withdrawn; this unit reopens nothing.

## Status of the saved result

**The saved result is a FAIL of the frozen model, retained as history. No
construction adequacy — failure or adequacy — is established.** The saved
arithmetic has the implemented model heavier by 44.7 t with the sea-level
margin line moving +20.3 → −24.4 t. Of the screens: the declared upper-bound
radial-strip cap screen **failed and the FAIL is retained**, including the
saved T0 service values — but a bound exceeding the limit does not prove that
the actual stress exceeds the limit, and no refinement-independent physical
failure is claimed; it is a failed screen, not a physical proof. The hoop and
body-axial screens are withdrawn with the implemented geometry. The
mass/margin lines are unreconciled history (removed-aluminium discrepancy,
un-updated spokes line). Complete construction mass, lift/margins, fit and
bearing capacity are UNKNOWN.

**Weakest assumption (engineering):** the confined resin at the cord/cone
interface — the 80 MPa bearing and 3 GPa modulus records are unqualified
ASSUMED values, the wedge compliance model concentrates the transfer in that
soft stage, and confined creep is UNKNOWN. The mechanical-capture concept
stands or falls on this interface, independent of the saved arithmetic above.

**Next hypothesis (UNISSUED):** a **paid direct mechanical cord grip** (e.g.
a split-wedge or swaged sleeve on the cord itself) replacing the long soft
resin pot remains the candidate direction. It is UNISSUED: any such unit
requires a new finite root freeze that reconciles both cord ends (free length
plus both embedded runs), the actual fastener stacks (recesses, washer
thicknesses, head heights) and the accepted predecessor state before the
first calculation. No construction or parameter selection is made here.

**Scoreboard (≤180 chars):** R3-I031 ARCHIVED: model ≠ drawn cartridge;
mass/margins/fit/bearing/compliance UNKNOWN; saved FAIL kept as history; cap
upper-bound screen FAIL retained, no physical-failure proof.

## Reproduction

```
python3 research/design-iterations/R3-I031/cartridge.py
```

Standard library only; reads the frozen `baseline.json` (sha-pinned by
`sources.json`) and writes `cartridge.json`. Two scientific payloads were
executed for this unit: the first produced the saved result; the second
re-ran the committed source after an identifier rename, and its saved output
is byte-identical to the first (sha256 `a83b5ad6…` in both saved records).
The repeat is preserved as a **scope deviation** — not a demonstrated-defect
necessity — and is not retroactively authorized here; the third allowed start
remains unused and unreleased, and this correction authorizes no science.
The design, dimensions, materials and formulas were frozen before the first
run; nothing was tuned after the FAIL. Run-boundary, control and provenance
receipts are retained in private evidence.
