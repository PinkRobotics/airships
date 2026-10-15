# R3-I031 — mechanically captured tapered-pot socket cartridge

Status: **FAIL returned same-day** — the frozen two-family cartridge construction
(tapered resin pot in a 5° internal cone, paid rear chamber, bolted cap, titanium
through-stud with interior load nut) evaluated against the accepted R3-I028
aluminium-socket lineage at frozen base `3e4ba19d705c992700caba9c03316ca2c4b7af4f`
(tree `d5bed71921eb565274fd2ec9a102bb79d518c3e1`). It is **heavier by 44.7 t
whole-vehicle, flipping the sea-level margin negative, and its cap fails bending
even at service tension**. A heavier or inadequate construction is a valid
same-day FAIL; the frozen construction is not enlarged after seeing this.

Inputs pinned: `R3-I028/baseline.json` sha256
`dce7fd4d3c8650e71788a7c3e55decb0f95e8899dd43b463b12f47697aa7034e`,
`R3-I028/socket_body.json` sha256
`c20cec9156e27339c3da0469c15d9c16739add69a34d594f9c73613b6440db40`
(copied as data; never imported, executed or regenerated).

## What replaced what

Only I028's adhesive-to-aluminium and unspecified aluminium female-thread axial
transfer is replaced: cord → **tapered resin pot** → **frictionless 5° cone
bearing** (narrow at the cord exit, widening rear; **zero adhesive-shear credit
to aluminium**) → conical body with continuous shoulder → rear flange → four
titanium cap bolts with clearance holes and separate Ti nuts (**no aluminium
female thread anywhere**) → bolted cap → paid Ti bearing washer on an isolation
layer → interior titanium load nut (1.5d engagement) → titanium through-stud →
retained exterior anchor interface. Radial spreading `N·cos5°` is reacted as
hoop in the body wall; at the frozen fitting demand the cone normal is
**N = T/sin5° = 203 kN (d60) / 531 kN (d180/11)**.

Retained unchanged: cord families (E 70 GPa, 970 kg/m³, strength UNKNOWN),
plane/station counts, clips, anchor blocks, doubler pads, 45/50 mm attachment
bolts, exterior jam nut and anchor interface, the pressure structure, and the
one free-cord/transfer datum. Material records are the accepted ASSUMED records:
Al 69 GPa / 2,700 / 150 MPa working; Ti-6Al-4V 114 GPa / 4,430 / 880 MPa;
resin 12 MPa shear plus this unit's frozen additions — E 3 GPa and 80 MPa
compression-bearing (ASSUMED, unqualified).

## Dimensioned construction (ASCII; d60 values, d180/11 bracketed; mm)

```
        cord axis ────────────────────────────────────────────────────────────────────────►
        nose face     grip OD 23.5 [38.0] retained over grip 60 [97]   OD 3d = 42 [69]
   ┌──────┬──────────────────────────────────────────────┬───────────────┬─────────────┬─────────┐
   │ cord │      tapered resin pot in 5° internal cone    │   chamber     │ rear flange │  cap    │
   │ 7.87 │      [12.72]                                  │  clear 2.5d   │  OD 4d,     │  OD 4d, │
   │      │      cone Ø 9.0 [14.6] at exit → 35.0 [57.5]  │  Ø35 [57.5]   │  0.5d thk   │ 0.5d    │
   └──────┴──────────────────────────────────────────────┴───────────────┴─────────────┴─────────┘
   |◄──────────────── cone 148.6 [245.2] ────────────────►|◄ 2d =28 [46]►|◄ 7 [11.5] ►|◄7 [11.5]►|
                                          OD flares 23.5→42 [38→69] behind the grip (shoulder)
   total body 183.6 [302.7]  (old body 76 [113] — comparison value only)
   wall at chamber entrance 0.25d = 3.5 [5.75];  wall over cone = frontWall 7.25 [11.7]
```

```
   rear elevation (cap/flange, d60)             chamber section (d60)
        Ø56 [92]                                     wall 3.5 [5.75]
        bolt circle Ø49 [80.5]                          ┌───────────┐
        4 × Ø6.6 [10.6] clearance holes           ══════╡   clear     ╞══════
        + separate Ti nuts (no Al thread)                │  Ø35 [57.5]│
          ○   ○                                         └───────────┘
        ○   ┼   ◇  stud clearance Ø14.6 [23.6]      cone enters at left,
          ○   ○                                      chamber 2d long
   bolt-head seats are spot-faced/counterbored inside the frozen 4d envelope
   (the 3.5d circle + standard heads overlap both corner edges by construction;
   relief is priced in the machining stock, not a new dimension)
```

```
   interior load path at the cap (d60)          exterior (retained)
   chamber side:                                cap rear face:
   Ti stud end ─► interior load nut             stud tip 3 [14] mm + jam nut
   1.5d = 21 [34.5] engagement,                 + anchor block, 3 × M10 Ti
   bears through Ti washer Ø1.5d = 21 [34.5]    attachment bolts 45 [50] mm
   on paid isolation layer on cap inner face    shanks (exterior anchor
        ▼ T                                    interface unchanged)
   ═════════════ cap 0.5d ═════════════
        ▼ T                     new stud overall 31 [60] mm (old 79 [127]);
   4 × M6 [M10] Ti cap bolts            old length/adjustment travel do NOT
   in tension, T/4 each                 survive by name
```

## Per-end piece count and complete incremental bill (kg/end)

Per cord end: **one** conical body (shoulder/chamber/flange integral), **one**
pot, **one** cap, **four** cap bolts, **four** cap nuts, **eight** cap washers,
**one** interior load nut, **one** bearing washer — each counted and priced;
isolation/seal stock priced at every Ti/Al contact (bolt holes, stud hole,
bearing face) in addition to the retained 0.025 kg/end provision.

| line (kg/end) | d60 | d180/11 |
|---|---:|---:|
| REMOVED: I028 aluminium body | 0.0760 | 0.2954 |
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
| **increment per end** | **+0.3651** | **+1.6494** |
| × ends | 21,390 | 21,080 |
| **family increment** | **+7.81 t** | **+34.77 t** |

Required-but-unsized (UNKNOWN, not zero-mass): station-pitch envelope
compatibility for the 183.6/302.7 mm bodies; adjustment take-up travel; pot
moulding/insertion process stock; contact-seating shims.

## Whole-vehicle result (same lift, gas, payload, pressure, mission as I028)

| line | I028 accepted | this unit | Δ |
|---|---:|---:|---:|
| hardware increment | — | **+42.58 t** | |
| 5 % assembly share on the increment | — | +2.13 t | |
| **total increment** | | | **+44.71 t** |
| sockets line | 16.41 t | 58.99 t | +42.58 |
| whole known subtotal (conditional) | 2,229.5 t | **2,274.2 t** | +44.71 |
| **sea-level margin** | +20.3 t | **−24.4 t** | **FAIL (new)** |
| 2,500 m margin | −472.2 t | **−516.9 t** | FAIL persists |
| x1.5 station-hardware increment | 14.10 t | 36.45 t | |
| stacked x1.5 sea-level | +6.22 t | **−60.9 t** | FAIL |
| SF1.2 (separate d60+d20 construction) | historical FAIL | substitution UNCOMPUTED/UNKNOWN | |

U+C remains subtractive/UNKNOWN; physical float is not shown. The known subtotal
was already conditional and stays conditional.

## Screens (fitting demand T_fit = 17.7 / 46.27 kN — inherited source observations)

| element | d60 demand | d180/11 | limit (ASSUMED) | util | verdict |
|---|---:|---:|---|---:|---|
| cone bearing, resin | 19.7 MPa | 19.0 MPa | 80 MPa | 0.25 | PASS (cond.) |
| cone bearing, aluminium | 19.7 MPa | 19.0 MPa | 150 MPa | 0.13 | PASS (cond.) |
| hoop (max, at chamber entrance 5p) | 98.5 MPa | 95.2 MPa | 150 MPa | 0.66 | PASS (cond.) |
| body axial (closed-form integral) | 41.8 MPa | 40.5 MPa | 150 MPa | 0.28 | PASS (cond.) |
| **cap bending (radial-strip screen)** | **459.9 MPa** | **445.5 MPa** | 150 MPa | **3.07 / 2.97** | **FAIL** |
| **cap bending at T0 service** | **176.9 MPa** | **171.3 MPa** | 150 MPa | **1.18 / 1.14** | **FAIL** |
| cap-bolt tension (4 × M6/M10 Ti) | 220.1 MPa | 199.4 MPa | 880 MPa | 0.25 | PASS |
| cap-bolt bearing on Al | 105.4 MPa | 100.6 MPa | 150 MPa | 0.70 | PASS (cond.) |
| bolt-head seat bearing | 99.8 MPa | 94.0 MPa | 150 MPa | 0.67 | PASS (cond.) |
| stud tension (M14/M23) | 153.9 MPa | 138.5 MPa | 880 MPa | 0.18 | PASS |
| interior load-nut stripping (1.5d) | 22.5 MPa | 21.8 MPa | 528 MPa | 0.04 | PASS |
| washer bearing on cap inner face | 98.9 MPa | 93.0 MPa | 150 MPa | 0.66 | PASS (cond.) |
| cord-to-resin embed shear | 4.8 MPa | 4.7 MPa | 12 MPa | 0.40 | PASS (cond.) |

The longer embed actually **improves** the cord–resin screen (13.77 MPa inherited
→ 4.8/4.7 MPa). Assembly/access: interior load nut wrenches through the chamber
clear bore (hex 22.4/36.8 mm vs clear 35/57.5 mm); cap bolts insert from the
front with rear nuts; envelope compatibility stays UNKNOWN.

## Series compliance (both ends, one free-cord datum)

The soft stage is the **pot wedge**: axial stiffness k_z = k_r·tan²5°, so the
pot's confined radial compliance appears divided by tan²5°.

| family | L_ser | chain denominator | eta (mean cord) | both-end take-up to hold T0 |
|---|---|---|---|---:|
| d60 | 0.02104 → **0.17302 m** | 12.2424 → 12.5529 (+2.48 %) | 1.000257 → **0.995915** | **0.61 mm** |
| d180/11 | 0.03322 → **0.27633 m** | 17.3607 → 17.8475 (+2.80 %) | 1.000381 → **0.994355** | **0.97 mm** |

Tension at unchanged imposed extension falls 6.809 → 6.644 kN and 17.797 →
17.312 kN; take-up demand is ~40× the I028 demand and its availability is
UNKNOWN (no free installation-after-evacuation is claimed). n=5 declared-model
first-slack scales by the exact denominator ratio (e.g. d60 −cos5
26.6213 → 27.2822 mm; all four packets in `cartridge.json`); chord-basis tables
stay unchanged historical comparators. Full n=2..12 class bounds,
centroid/no-transfer sensitivity and global stability remain UNCOMPUTED/
UNKNOWN; the coupled eigen margin is not recomputed (dependent UNKNOWN). The
R3-I023 equilibrium closure stays withdrawn; this unit reopens nothing.

## Verdict

**FAIL.** The construction is decisively heavier (+44.7 t; sea-level margin
+20.3 → −24.4 t) and its cap fails the frozen bending screen at 3.0×/2.97× the
ASSUMED aluminium limit at fitting demand and 1.18×/1.14× even at service
tension — an impossible fit under the frozen dimensions, not a marginal call.
The cone bearing, hoop, body axial and all fastener screens pass conditionally
on the ASSUMED records. No mass advantage of the mechanical capture survives at
these two families' fitting demands.

**Weakest assumption:** resin/cord transfer and pot compression/creep under
confinement — the wedge compliance (tan²5°) dominates the series spring and the
80 MPa / 3 GPa resin record is unqualified; confined creep is UNKNOWN.

**Next change (ranked):** a **paid direct mechanical cord grip** (e.g. a
split-wedge or swaged sleeve on the cord itself) to replace the long soft resin
pot — it attacks simultaneously the 44.7 t mass, the 5° wedge compliance and the
resin-dominated unknowns; the cap/shoulder FAIL then governs and is second in
line (a thicker cap or larger bolt circle would enlarge the frozen construction
and is not taken here).

**Scoreboard (≤180 chars):** R3-I031 tapered-pot cartridge: +44.7 t, subtotal
2229.5→2274.2, SL +20.3→−24.4 FAIL; 2500 m −516.9 FAIL; cap bend 3.1×FAIL at
fit, 1.2× at T0; cone/hoop/fasteners PASS cond.

## Reproduction

```
python3 research/design-iterations/R3-I031/cartridge.py
```

Standard library only; reads the frozen `baseline.json` (sha-pinned by
`sources.json`) and writes `cartridge.json`. **Two scientific payloads** were
executed for this unit, both under the controlling launcher (private-IPC bwrap
child, robotics-p3.slice, CPU30, CPUQuota 100 %, 1 GiB memory/AS caps, no swap,
≤16 tasks, CPU 60 s, wall 120 s), each with a pre-science enforcement guard
verifying namespace, cgroup, quota, memory, swap, affinity and rlimits BEFORE
any calculation, and full source/input/output hashes, wall/CPU/RSS and stream
receipts. The first completed (exit 0) and produced the saved FAIL result. The
second was a pure identifier rename in the source (two local antiderivative
variable names carried tokens forbidden in public files — a demonstrated
hygiene defect, not a construction change; no dimension, material, formula or
number moved), re-run to bind the committed bytes; its output is **byte-for-byte
identical** to the first (sha256 `a83b5ad6…` both runs). The design, dimensions,
materials and screen formulas were frozen before the first run; the FAIL is the
physical result and nothing was tuned after it. One of the three allowed
scientific payloads remains unspent.

## Expert-confirmation ledger (short)

1. Mass arithmetic is count × exact frustum/cylindrical volumes at the frozen
   densities; the two family increments (+7.81/+34.77 t) follow from the
   per-end bill above with no rounding buried in the sum.
2. The cone transfer is frictionless with zero adhesive-shear credit; N =
   T/sin5° and the hoop model (local thin-wall p·r/t, worst at the chamber
   entrance where it is exactly 5p by the frozen ratio geometry) is a declared
   screen, not a certification.
3. The cap bending screen is a declared upper-bound radial-strip model; its
   FAIL at 3.0×/2.97× fitting and 1.18×/1.14× service demand is robust to the
   model refinement the frozen scope excludes.
4. Series compliance changes only the socket spring; retained terms carry by
   the frozen residual decomposition (stud-dominated everything-else prorated
   by length), the pot wedge is the new dominant term, and contact seating
   stays UNKNOWN/excluded.
5. Every margin moves only by the reconciled +44.71 t increment at unchanged
   lift; inherited FAIL/UNKNOWN qualifications from R3-I019/R3-I023/R3-I028
   remain visible and unclosed; SF1.2 substitution stays UNKNOWN.
