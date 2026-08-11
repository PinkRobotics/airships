# Taking the cell to one metre

Written 2026-08-11 for the agent implementing it. **Nothing here is implemented** — this is
the analysis and the work order. Every number was computed by `tools/scale_study.py`, which
first reproduces all fourteen published figures of the 0.709 m article from
`research/analysis/vacuum-cell.py` before it evaluates anything at another span. Run it. If
the self-check does not print `reproduces the published article`, the model moved and every
number below is stale.

The three measured figures (node mass, node generation time, extraction failure) came from
running `tools/gen_nodes.py` at the new parameters; they are marked MEASURED. Everything
marked TO VERIFY is a supplier or shop-floor question this analysis cannot answer.

---

## 1. What "one metre" means, and the one decision to make first

The designer's requirement: *"the metric I want to be 1 m is square face to square face …
so that an array of N×N would consume a space of N×N metres."*

That is the model's `span` parameter exactly. Setting `span = 1.0`:

| | 0.7085 m | 1.000 m |
|---|---|---|
| square face to square face | 709 mm | **1000 mm** |
| hexagon face to hexagon face (`S·√3/2`) | 614 mm | 866 mm |
| corner to corner | 793 mm | 1118 mm |
| edge / long member | 250.5 mm | **353.6 mm** |
| short member (`a/√2`) | 177.1 mm | **250.0 mm** |
| enclosed | 178 L | **500 L** |
| surface area | 1.681 m² | 3.348 m² |
| load on one hexagon | 1.68 tf | 3.36 tf |
| load on the whole surface | 17.4 tf | 34.6 tf |
| cells per m³ of ship (BCC, 2 per S³) | 5.61 | 2.00 |

**The decision: exactly 1.000, or a little under?** The array pitch IS the span — cells seat
face to face, so N cells occupy N × span. At `span = 1.000` a 10×10×10 block is exactly
10 m and there is no room for assembly tolerance between cells. At `span = 0.980` the same
block is 9.8 m and every cell has 20 mm of slack to its neighbour.

Nothing structural argues either way: **the margins are identical at both** (see §2), and
0.98 gives up 5.7% of the enclosed volume. The film panels dimple *inward* under load, so
no clearance is needed for bulge — this is a tolerance-and-jig question, not a physics one.
The tables below carry both. **Ask the designer; do not pick silently.**

---

## 2. The scaling law — the whole analysis in four lines

| quantity | how it scales |
|---|---|
| crush demand per octet strut | `L²` |
| film line load on a boundary member | `L¹` (membrane tension `T = pR/2`, and `R ∝ a`) |
| bending moment `wL²/8` | `L³` |
| Euler margin at a FIXED tube | **`1/L⁴`** |
| bending stress at a FIXED tube | **`L³`** |

Both failure modes are held **exactly constant** by scaling the tube diameter with the span:
`I ∝ d⁴` against a capacity `∝ d⁴/L²`, and `Z ∝ d³` against a stress `∝ L³/d³`.

Verified rather than asserted — `scale_study.py` at the pure geometric scale, main
14.11 × 11.29 and rim 19.76 × 16.94, reports octet 1.82 / spoke 2.75 / tie 2.45 / rim 4.12
and rim bending at 2.84 atm, which are today's numbers to the last digit.

**And so is the mass budget.** Tube mass grows as `L³` alongside the volume, so **16.21
kg/m³ at 0.709 m is 16.21 kg/m³ at 1 m**. A bigger cell of this architecture is not lighter
per litre. It still does not float and this change will not make it float — the wall it
must beat is 0.9569 kg/m³ and the article is 16.9× over it at every size.

### What happens if the tube does NOT grow

Because someone will ask. At `span = 1.0` on today's 10×8 / 14×12:

    octet Euler 0.46   spoke 0.69   tie 0.62   rim 1.04
    rim bending 2475 MPa, fails at 1.01 atm

The interior members buckle at less than half their load and the rim reaches ultimate at
the atmosphere it is meant to hold. **Not a degraded article — a broken one.**

---

## 3. The design point

The sweep minimises TOTAL mass (tube + joints + film) over 25 catalogue SKUs subject to
holding **every** margin the 0.709 article holds: four Euler margins, the rim's bending
capacity in atmospheres, and the spoke and square-tie bending margins.

| span | target | main | rim | tube | joints | film | total | kg/m³ |
|---|---|---|---|---|---|---|---|---|
| 1.000 | parity with today | **16 × 14** | **24 × 22** | 5.71 kg | 1.90 kg | 79 g | **7.69 kg** | 15.38 |
| 1.000 | +30% on every margin | 18 × 16 | 26 × 24 | 6.40 kg | 2.71 kg | 79 g | 9.19 kg | 18.38 |
| 0.980 | parity with today | 16 × 14 | 22 × 20 | 5.47 kg | 1.90 kg | 75 g | 7.45 kg | 15.83 |
| 0.980 | +30% on every margin | 18 × 16 | 25 × 23 | 6.21 kg | 2.71 kg | 75 g | 9.00 kg | 19.12 |

Achieved margins at the recommended 1.000 m parity point — every one above today's:

    octet 2.11 (was 1.82)   spoke 3.19 (2.75)   tie 2.83 (2.45)   rim 5.73 (4.12)
    rim bending fails at 3.25 atm (2.84)

**Stock tube beats geometric scaling.** 15.38 kg/m³ against the scale-invariant 16.21,
because a 16 mm tube with a 1 mm wall buys more `I` per gram than a 14.1 mm tube with a
1.4 mm wall. The lesson generalises: *thin wall, big diameter*, right up to the local
buckling limit — which is **NOT CHECKED ANYWHERE IN THIS MODEL** and wants checking before
anyone buys 24 × 22. At `R/t = 12` the classical shell-buckling stress is far above the
axial demand here, but "far above" is not a number in the repository.

The joints column is `0.465 kg × (od/10)³`, and that cube law is MEASURED, not assumed
(§6). At 1 m the joints are 25% of the article by mass instead of 16%.

---

## 4. The work order

### 4.1 First, break the span derivation — this is the real change

`span` is not a parameter today. It is *derived*, in both model files:

```js
const chain = printerChain(m).find(r => r.designPoint);   // 0.6 mm nozzle x 2 perimeters
const p = chain.cellM;                                     // 0.3543 m
const spanM = 2 * p;                                       // 0.7085 m
```

The article's size is a consequence of **a printed-lattice sizing law the article no longer
uses**. Every member is bought tube now; the nozzle that set this span prints only the
joints, whose size is set by the pipe OD and not by this chain at all. The 709 mm is a
fossil.

- Make `span` a named constant in `cell/model.js` and `research/analysis/vacuum-cell.py`,
  and have `stockBuild()` / `stock_build()` take it.
- **`demonstrator()` must keep using the printer chain** — that function is about the
  all-printed article and the chain is genuinely its sizing law. Do not "fix" both.
- The parity gate holds 178 values identical across the two files. Change them together, in
  one commit, and run `make parity` before anything else.

### 4.2 The tube

Two SKUs become two different SKUs: 10 × 8 → 16 × 14 (180 members), 14 × 12 → 24 × 22
(36 rim edges). Purchased length per cell goes 48.8 m → 68.9 m.

Touches: `stockBuild()` (`ro`, `ri`, and the hard-coded `0.014`/`0.012` rim), the Python
mirror, `film_edge_loads`'s hard-coded `tube(0.010, 0.008)` and `tube(0.014, 0.012)` rows,
and every explorer card that names a tube.

### 4.3 The connectors — the biggest single block of work

`tools/gen_nodes.py`. Parameters split into three groups, and **the split is the whole
point**:

**Scale with the pipe** (×1.6 for a 10 → 16 mm main):

    --pipe-od 10 -> 16        --pipe-id 8 -> 14
    --rim-pipe-od 14 -> 24    --rim-pipe-id 12 -> 22
    --core-r 8 -> 12.8        --stub 20 -> 32       --shoulder 2 -> 3.2
    --lip 2.5 -> 4.0          --lip-wall 1.6 -> 2.56
    --spigot-wall 2 -> 3.2    --blend 4 -> 6.4      --pad-t 3 -> 4.8

**Do NOT scale — these are printer tolerances, not geometry:**

    --clearance 0.15    --rib-h 0.25    --bore-margin 0.4    --slot-margin 0.5    --pilot 2.0

Absolute tolerances on a 1.6× part are *relatively tighter*, which is the easy direction.
`--pilot` is a bond gap, not a fit; leave it and let the glue area grow with the diameter.

**Recompute from the model:**

    --demand-n 3372 -> 6717        (octet axial at span 1.0; 6451 at 0.98)
    --res 112 -> ~160              (holds the 0.883 mm voxel at the bigger window; §6)

**Change the argparse DEFAULTS, do not pass flags.** Two of these parameters live in two
files. `check_assembly.load_params()` reads `manifest.paramsMm` — what was actually cut —
but then *overrides* it with its own `EXTRA_PARAMS`, which carries a second hard-coded
`demand_n=3372.0`, because `demand_n` and `slot_margin` are not written to the manifest.
Change the flag on the command line only and the prover will measure brand-new 16 mm joints
against the old 3372 N demand **and pass**. `grep -rn 3372 tools/` finds both copies; there
is no gate that compares them.

### 4.4 Re-prove and re-freeze

`check_assembly.py` re-derives all 432 member-ends from the SDF, so it needs no edit — but
**the frozen contract is invalidated the moment the parameters move**. Order:

1. `make nodes` (≈9 min at res 179, MEASURED — see §6)
2. `make assemblycheck` and read the failures **before** freezing anything
3. compare against the five standing failures (P5, P11, P13, P14, P16). New failures are
   real; do not sweep them into `KNOWN` to get a green build
4. re-freeze only when the failure set is understood
5. `--freeze` is deliberate and it is how a known-bad baseline gets locked. Locking a
   *worse* baseline is the one way to make this gate useless

### 4.5 The skin — and this is where the change actually hurts

The flat net today is **1.6808 m² of film inside a 1.986 × 2.237 m bounding box** (38%
utilisation; printed by `make explorercheck`). At 1 m every dimension grows 1.4114×:

    2.803 x 3.157 m, 3.35 m2 of film

**A single-piece net is very likely no longer cuttable from roll goods.** Composite film
laminates are commonly 1.37 m (54") wide, occasionally to ~2.7 m; 3.16 m is outside
anything ordinary. TO VERIFY with the supplier — this is a purchase question, and it is the
first phone call of this project, because the answer decides whether the net stays one
piece.

If it does not fit, the net must be split, and that fights the standing rule that seams are
the leak path. Do not solve it by splitting arbitrarily: the net is already cut as a
Steinhaus–Johnson–Trotter path for zero three-way junctions (#62), and any split must keep
that property. Two half-nets joined along an existing fold is the cheapest option — the
seam added is exactly the fold path you cut, so split along the shortest one — but it has to
be chosen together with the fold tree, not bolted on after it.

Also moving: the film's required areal density scales with the span, 16.6 → **23.6 g/m²**
on the hexagons. Still an ordinary product, but it is a different order.

### 4.6 The page

`cell/explorer.js` takes `span` through `buildCell` already and most of it follows. What
does not:

- `LEVELS`: `scaleM: 0.709` and every `radius`, `dist` on the four stage levels
- the level's own label, `71 cm`, and the ladder rung text
- `RIM_COLLAR_R`, `socketConeGeom` radii, and anything sized from a pipe OD
- the skin is drawn at `span * 1.012`; that 1.2% is a drawing offset to clear the collars.
  The collars grow with the PIPE and the offset is a fraction of the SPAN, so the fraction
  falls: 8.5 mm today, about 13.6 mm at a 1.6× pipe, which is ~1.4% of a metre. Re-check it
  by eye — an intersecting skin is one of the things the designer has caught twice
- every `data-n` figure re-reads from the model automatically; every number typed into prose
  does not. `grep -n '[0-9]\{3\} mm\|709\|251 mm\|177 mm\|178 L' cell/explorer.html`
- the three tours name cut lengths in their stop copy

### 4.7 The reports

`check_figures` holds 233 cited figures across 4 reports to the model, and
`check_figures_fresh` holds `figures.json` to the live model (248 figures). Both will go off
loudly, which is the system working. Budget real time for the report prose: the gates catch
a stale *figure*, and nothing catches a stale *sentence*.

---

## 5. What the size buys — and it is not mass

Per cubic metre of ship:

| | 0.709 m | 1.000 m |
|---|---|---|
| cells | 5.61 | 2.00 |
| printed joints | **287** | **102** |
| tube cuts | 1214 | 432 |
| printed mass | 2.61 kg | 3.81 kg |
| grams per joint | 9.1 g | 37.3 g |

**Part count falls by 64%; printed mass rises by 46%.** Fewer, bigger parts: 2.8× fewer
assembly operations and 2.8× fewer bond joints per cubic metre of ship, paid for in printer
hours. If assembly labour is the constraint, this is a large win. If print time is the
constraint, it is a loss. Both are true and the designer has to say which one binds.

**The barrier gets easier, and this may be the best reason to do it.** Area per unit volume
falls as `1/L`, so the same decade vacuum life allows more permeation per square metre:

| span | m²/m³ | decade budget |
|---|---|---|
| 0.7085 | 9.4506 | 2.90 cm³/(m²·day) |
| 0.980 | 6.8328 | 4.01 cm³/(m²·day) |
| 1.000 | 6.6962 | **4.09 cm³/(m²·day)** |

A 41% wider budget on the hardest open problem in the project (#63).

**And the parity prize is still ahead, not here.** The rim, the 48 spokes and the 72 ties
exist because a hexagon face at this subdivision contains no lattice point of its own. That
is a property of `n = 1`, not of the span — at 1 m with `n = 1` the whole boundary apparatus
is still needed. Going to `n = 2` is what deletes it, and that is a different change.

---

## 6. What will bite — all three MEASURED

**The node SDF does not survive the parameter change as it stands.** One node generated at
the 1 m parameters:

    node_00_lattice.stl:  8 arms, 109576 tris, OPEN (758 saddle), island 19.3 mm3, 49.8 g

`OPEN` means the surface ran into the edge of the extraction window and the mesh is not
closed — the same class of failure the 14 mm rim SKU caused, when a window fixed at 42 mm
clipped the bigger part. The window is derived as
`max(base_of.values()) + stub + blend + 6.0`, and with `stub = 32` and `blend = 6.4` that
derivation is still short. **Fix the window derivation first**, before generating all 51,
or you will debug 51 open meshes instead of one.

**Node mass: 11.7 g → 49.8 g, a factor of 4.26** against the `(16/10)³ = 4.10` the cube law
predicts. The law holds; use 4.26 for the estimate. 51 joints ≈ **1.98 kg**.

**Generation time: 2.2 s → 10.4 s per node** (measured at res 179, a slightly finer voxel
than needed), so `make nodes` goes ≈2 min → 6–9 min, and
`check_assembly` (122 s today, and it samples the same field) will grow with it. The full
`make check` chain is about 4 minutes today; assume 12–15. Use `make explorercheck` (11 s)
while iterating on the page and run the full chain once before each commit.

**Seat bearing and bond shear both rise 19%**, MEASURED from the same run: 119.3 → 142.5 MPa
bearing, 29.82 → 35.63 MPa closing-end glue shear. Not a scaling effect — a 16 × 14 tube has
a thinner wall *relative to its diameter* than 10 × 8, so the seat annulus grows 1.67× while
the demand grows 1.99×. If those numbers are unacceptable, **16 × 13 puts the bearing at
98.3 MPa, below today's**, for about 2 kg more tube. That is the cleanest lever available
and it is a designer's call, not an implementer's.

---

## 7. Order of work

1. `tools/scale_study.py`, self-check green — everything downstream depends on it
2. **ask: 1.000 or 0.980, and does the film supplier have a wide enough roll**
3. break the `printerChain` derivation; `make parity`
4. new SKUs in both model files; `make parity`, `make figcheck`
5. fix the extraction window; generate one node; then all 51
6. `make assemblycheck` without freezing; understand the failure set; then freeze
7. the page, then the reports, then the net
8. full `make check`, screenshot every level, deploy

Steps 1–4 are half a day and reversible. Step 5 is where the unknown is. Steps 6–8 are
grind, and the gates will tell you when you are done.

**Screenshot after every visual change.** The gates hold every number on the page to the
model and cannot see whether anything is *visible* — see the explorer section of
`docs/HANDOFF.md`, which is written from six consecutive faults that all passed a green
check.
