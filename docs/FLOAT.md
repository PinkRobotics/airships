# Making the cell float

Written 2026-08-11. This is the standing brief for continuous work on the vacuum cell's
mass. It began as a study of retargeting the cell to one metre; the answer to that turned
out to be *size is not the lever*, so the sizing work order has moved to Appendix A and the
document now says what the lever actually is.

**Scope: article A only.** The buildable article — Kelvin cell, purchased carbon tube,
printed joints, film skin. The two other objects that appear in the reports are not this:
the "design point" is a closed-form sizing law with no geometry, and the "n = 2 hierarchy"
is that same formula with one exponent changed. Neither has a part in it. They are useful
as bounds and are cited as such below, never as designs.

Every figure here is computed by a tool in this repository that first reproduces the
published article before it evaluates anything else. If a self-check line fails, the model
moved and the numbers below are stale — re-run before trusting them:

    python3 tools/scale_study.py         # spans and SKUs, self-checks 14 published figures
    python3 tools/subdivision_study.py   # finer lattices, self-checks 6 model identities

Figures marked MEASURED came from running the real generator or the real page. Figures
marked TO VERIFY are supplier or shop-floor questions no calculation here can settle.

---

## 0. The goal state

**A cubic metre of assembled cells must weigh less than the air it displaces.**

| | kg/m³ |
|---|---|
| the target: air at 2,500 m | **0.9569** |
| (at sea level, if you prefer the easier bar) | 1.2250 |
| the article as built, optimally tubed | **~9.3 — that is 9.7×** |
| best configuration found so far (§3) | **3.89 — 4.06×** |

**Definition of done.** A bill of materials, computed by this repository's own model and
held by a gate, that comes in under 0.9569 kg/m³ *including* tube, joints, film, barrier and
seams, with at least the model's 1.5 factor on every failure mode — Euler, local wall
buckling, film bending, and joint bearing — and whose every part can be bought from a named
supplier or made on hardware we have. Under 1.2250 at sea level is a real milestone worth
declaring on the way.

**Definition of not-done.** A number that floats because a mass line was omitted, a margin
was quietly relaxed, or a part was specified that nobody sells. Each of those has happened
in this project at least once. Write down what you dropped.

---

## 1. Where the mass is

Sized optimally at every span against real thin-wall tube, holding Euler, local wall
buckling and film bending, at the model's own 1.5 factor:

| span | tube | joints | film | total | × the wall |
|---|---|---|---|---|---|
| 0.71 m | 6.55 | 2.61 | 0.16 | 9.31 | 9.7× |
| 1.0 m | 5.37 | 3.81 | 0.16 | 9.34 | 9.8× |
| 2.0 m | 4.32 | 4.57 | 0.16 | 9.05 | 9.5× |
| 3.0 m | 5.14 | 3.35 | 0.16 | 8.65 | 9.0× |

**Flat. Size is not a lever** — see §2. Two lines dominate, and neither is the film:

- **The joints are 2.6–4.6 kg/m³**, 3–5× the wall on their own. Their mass per cubic metre
  is fixed by the bore-to-span ratio, so it does not improve at any size. **A weightless
  tube still does not float.**
- **69% of the tube by length is not resisting the vacuum.** Of 216 members only **60 are
  octet** — the pressure structure. The other 156 (36 rim, 48 spokes, 72 ties) exist to
  support the film. The article is mostly a film-support frame with a pressure lattice
  inside it.

The film itself is **1% of the mass** at every size. The barrier coating is 0.45 g on the
whole cell — 100 nm of PVD aluminium over 1.681 m². Neither is a weight problem. They are a
leak problem, which is a different document (#63).

---

## 2. Settled — do not re-litigate

- **Size is not a lever.** Every mass term scales as L³, the same as the displaced volume:
  tube (length × section), joints (od³), film (areal density × area). Margins and kg/m³ are
  both invariant under geometric scaling. Verified two ways — analytically, and by sweeping
  0.4–3.0 m against real catalogue tube, which stays within ±8%.
- **What size DOES buy** is manufacturability (§3, R3), 64% fewer joints per m³ from 0.7 to
  1.3 m, and a 41% wider permeation budget. All real, none of it buoyancy.
- **Vacuum, not helium.** Gated in `research/analysis/helium.md`.
- **Full vacuum, not partial.** Shell mass goes as Δp^(2/3) while lift goes as Δp, so
  partial vacuum degrades as Δp^(-1/3). In `nullResults.partialVacuum`.
- **The bench article is a process coupon, not a floater.** `floats: false` is deliberate.
  Its job is to prove print → assemble → wrap → evacuate → **seal** → hold for months. Do
  not optimise its mass; that is not what it is for.
- **Local wall buckling is modelled**, with a NASA SP-8007 knockdown (`K_LOCAL = 0.3`) and
  an orthotropy penalty. It is the binding constraint on thin walls and it is why you cannot
  simply specify a thinner tube.

---

## 3. The routes, ranked by what they are worth

Each was priced with the tools above. The percentages are of the current 9.3 kg/m³.

| # | route | takes it to | status |
|---|---|---|---|
| **R1** | subdivide the lattice so the film needs no separate frame | **~4.1× the wall** | priced, not designed |
| **R2** | lighten the joints | up to ~2× on the total | not started |
| **R3** | source the right tube | 2–3× on tube alone, already inside R1's numbers | not started |
| **R4** | put the right material in the right member | tube floor 2.1× → ~1.0× | not started |

**All four together are roughly the 9×.** That is the honest headline: floating is
arguably reachable, but only by changing what the cell is braced with, what the joints are,
and what the tube is made of — not by any one of them.

### R1 — subdivide the lattice (the biggest single win)

`kelvin_lattice_counts` reports **`boundaryFrameNeeded: False` at every even n**. At n = 2
the octet grid reaches the cell faces on its own: the 36 rim edges, 48 spokes, 72 ties, 24
rim vertices and 8 hexagon hubs all disappear. What replaces them is more, shorter, thinner
struts — 948 members and 201 joints instead of 216 and 51.

`tools/subdivision_study.py`:

| span | n | joints | strut | tube OD × wall | tube | joints | film | kg/m³ | × wall |
|---|---|---|---|---|---|---|---|---|---|
| 1.0 | 2 | 201 | 177 mm | 9.0 × 0.15 mm | 1.81 | 2.67 | 0.08 | 4.56 | 4.77 |
| 2.0 | 2 | 201 | 354 mm | 16.5 × 0.40 mm | 2.20 | 2.06 | 0.08 | 4.33 | 4.53 |
| **4.0** | **2** | **201** | **707 mm** | **30.5 × 1.00 mm** | 2.52 | 1.62 | 0.08 | **4.22** | **4.41** |
| 3.0 | 4 | 1289 | 265 mm | 13.0 × 0.25 mm | 1.93 | 1.91 | 0.04 | 3.89 | 4.06 |
| 6.0 | 4 | 1289 | 530 mm | 26.0 × 0.50 mm | 1.93 | 1.91 | 0.04 | 3.89 | 4.06 |

**From 9.3 to ~4.2. More than half the mass, gone, in the same cell.** And the joints fall
with it — not because there are fewer (there are four times as many) but because joint mass
goes as the *cube* of the bore, and a finer lattice needs a much smaller bore.

**And this is where size finally earns something.** A fine lattice in a small cell needs a
wall nobody sells: n = 2 at 1 m wants 0.15 mm. The same lattice at 4 m wants **30.5 × 1.0
mm, which is an ordinary drone-boom tube.** The rule to hold onto: *subdivision decides the
mass; span decides whether you can buy the tube.*

**What R1 does not yet check, and it is the first task:** the film's bending load on the
members lying in the faces. At n = 1 that load governs the entire boundary. The moment falls
as the **cube** of the bracing pitch, so it should be 1/8 at n = 2 and 1/64 at n = 4 — which
is a reason to expect the numbers to survive, not a reason to skip the check.

**First tasks**
1. Add film bending at general n to `subdivision_study.py`. Reuse `film_edge_loads`' own
   line loads; the panel is now the lattice pitch. **Until this lands, every R1 figure is a
   floor.** If it fails, the answer is not to abandon R1 — it is to find which members need
   a bigger section and re-price.
2. Extend `kelvinLatticeCounts` usage into `cell/model.js` so an n = 2 article can be
   costed by the real model, not a study script, and gated like everything else.
3. Then the joint problem changes shape: 201 joints with more arms each, at ~16 mm bore.
   Count the arm valences at n = 2 before designing anything (`gen_nodes` can enumerate).

### R2 — lighten the joints

At n = 2 the joints are still **38–46% of the article**. They carry no load in the model's
own accounting (`NODE_MASS_FRAC` comment: *"nodes carry no load but weigh"*), so every gram
is overhead. Options, roughly in order of expected value:

- **Shell and vent them.** They are solid today for a stated reason — *"sparse infill is a
  virtual leak"* — but that argument is about trapped volume, and a shell **vented to the
  vacuum** has no trapped volume. This may be most of the win for very little work. Settle
  the leak question first, in writing.
- **Topology-optimise.** A hub transferring axial loads between tube ends is a classic case;
  the SDF generator already produces the field, so the optimiser has somewhere to live.
- **Stop printing them.** A mitred, bonded tube-to-tube joint has no hub at all. Bond area
  and alignment jigging become the problem instead — cost them honestly.
- **Change the material.** PAHT-CF is 1,060 kg/m³. Continuous-fibre print (CFF, 1,400) is
  denser but far stronger, so less of it; the trade needs computing, not guessing.
- **Fewer arms.** Valence drives hub volume superlinearly. This couples to R1 — check
  whether n = 2 concentrates or spreads the arm count before assuming either.

**Target to aim at:** the model's own design point allows joints at **15% of lattice mass**.
The real measured article came in at **19.5%**. At n = 2 today's law gives roughly **80%**.
Getting to 15% is worth ~1.6 kg/m³ — the single largest identified saving after R1.

### R3 — source the tube (and this is a standing, incremental job)

Every study here uses an invented catalogue: outside diameters in 0.5 mm steps against a
list of plausible walls. **That is the weakest input in the whole analysis.** The answers
turn on whether a given (OD, wall, length, modulus) is a real, orderable product.

**Deliverable: `research/data/tube-catalogue.json`**, accumulated over time, one entry per
real product:

```json
{
  "sku": "supplier part number",
  "odMm": 30.0, "idMm": 28.0, "wallMm": 1.0,
  "material": "T700-class roll-wrapped", "layup": "[0/±45/90]",
  "eGPa": 135, "sigmaMPa": 2500, "rhoKgM3": 1600,
  "lengthMm": 2000, "priceCurrency": "CAD", "price": 0.0, "moq": 1,
  "supplier": "", "url": "", "checked": "2026-08-11",
  "notes": "modulus is the supplier's claim or my estimate — say which"
}
```

Then point both study tools at it instead of the invented list, and re-run. Rules:

- **Record what you could NOT find**, not just what you found. An empty band in the
  catalogue is a finding: it tells the designer which spans are unreachable.
- **Search the whole range** — from very fine tube (3–8 mm, model-aircraft and medical
  suppliers) through the 10–30 mm drone and RC band, to 30–80 mm mast, boom and tripod
  stock. The studies want the extremes as much as the middle.
- **Pultruded, roll-wrapped and filament-wound are different products** with different
  moduli and very different minimum walls. Record which.
- **Thin-ply prepreg** (~0.02–0.03 mm cured ply) is what makes sub-0.2 mm walls possible at
  all; a 0.125 mm wall is one ply of ordinary prepreg and cannot carry hoop. If a supplier
  will wind custom thin-ply tube, that unlocks the small-span rows. Get a quote. [TO VERIFY]
- **Modulus is not optional.** A cheap tube at 70 GPa is worse than an expensive one at 135;
  the studies are buckling-driven and E is the whole game.

### R4 — the right material in the right member

Not one material for the article. The families fail differently:

- **octet struts** fail in Euler and local buckling → want **E/ρ**. M60J is 2.6× T700 on E.
- **boundary members** (while they exist, i.e. odd n) fail in **bending** → want **σ/ρ**.
  M60J is *worse* here: 2,290 MPa against T700's 2,500, at higher density. A naive swap to
  M60J makes the current article **heavier** — verified, 21.5 kg/m³ against 16.2.

The model's own design-point lattice in M60J is **0.943 kg/m³ — under the wall on its own.**
So the tube is not the thing that ultimately stops this; R4 plus R1 puts the tube line
essentially at the target and leaves the joints as the entire remaining problem. That is the
clearest statement of where this project's difficulty actually lives.

---

## 4. How to work on this continuously

**The loop's job is to lower the last column of §3's table and keep it honest.**

Each pass: pick one route, do the smallest thing that changes a number, re-run both study
tools, and record the new figure with what it assumed. Prefer a checked number that is worse
over an unchecked number that is better.

- **Run the self-checks every time.** Both tools reproduce published figures before
  computing anything new. A failed self-check means stop, not adjust the tolerance.
- **Never widen a margin definition to make something pass.** If a configuration only works
  at a lower safety factor, say so in those words and report both.
- **Never freeze a worse baseline.** `check_assembly --freeze` locks a known-bad state;
  locking a *more* broken one makes the gate useless. See `docs/HANDOFF.md`.
- **A mass line you did not model is not zero.** Bond adhesive, seam tape, the barrier
  coating, fasteners, jig-induced overlength — each is small and they are not all small
  together. Keep a running "not yet counted" list at the bottom of any result.
- **State the object.** Every figure belongs to article A at a stated span and subdivision.
  Most of the confusion in this project's history came from numbers that had drifted loose
  from their object.

### Open questions worth a research pass

1. **Is a vented, shelled joint acceptable in vacuum?** Decides R2's biggest lever.
2. **What is the real minimum wall** at each diameter band, per process? Decides R3.
3. **Does the film bending check survive n = 2**, or does it re-introduce a heavy member?
4. **What is the lightest joint that transfers 3–7 kN between two tube ends?** Ask it as a
   general question first — there may be a standard answer from mast, kite or truss
   engineering that beats anything printed.
5. **Should the film be structural?** It is 1% of the mass and currently carried *by* the
   structure. A tension-stabilised arrangement where the film helps hold the lattice has
   never been costed here.
6. **What is the assembly labour** at 948 members and 201 joints per cell? R1 wins on mass
   and loses on part count; nobody has priced the loss.

---

## Appendix A — the one-metre sizing work order

Kept because it is correct and because retargeting the span may still be wanted for
handling, array pitch or barrier reasons. It is **not** a route to floating; see §2.

## A1. What "one metre" means, and the one decision to make first

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

Nothing structural argues either way: **the margins are identical at both** (see §2 of the brief), and
0.98 gives up 5.7% of the enclosed volume. The film panels dimple *inward* under load, so
no clearance is needed for bulge — this is a tolerance-and-jig question, not a physics one.
The tables below carry both. **Ask the designer; do not pick silently.**

---

## A2. The scaling law — the whole analysis in four lines

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

## A3. The design point

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

## A4. The work order

### A4.1 First, break the span derivation — this is the real change

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

### A4.2 The tube

Two SKUs become two different SKUs: 10 × 8 → 16 × 14 (180 members), 14 × 12 → 24 × 22
(36 rim edges). Purchased length per cell goes 48.8 m → 68.9 m.

Touches: `stockBuild()` (`ro`, `ri`, and the hard-coded `0.014`/`0.012` rim), the Python
mirror, `film_edge_loads`'s hard-coded `tube(0.010, 0.008)` and `tube(0.014, 0.012)` rows,
and every explorer card that names a tube.

### A4.3 The connectors — the biggest single block of work

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

### A4.4 Re-prove and re-freeze

`check_assembly.py` re-derives all 432 member-ends from the SDF, so it needs no edit — but
**the frozen contract is invalidated the moment the parameters move**. Order:

1. `make nodes` (≈9 min at res 179, MEASURED — see §6)
2. `make assemblycheck` and read the failures **before** freezing anything
3. compare against the five standing failures (P5, P11, P13, P14, P16). New failures are
   real; do not sweep them into `KNOWN` to get a green build
4. re-freeze only when the failure set is understood
5. `--freeze` is deliberate and it is how a known-bad baseline gets locked. Locking a
   *worse* baseline is the one way to make this gate useless

### A4.5 The skin — and this is where the change actually hurts

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

### A4.6 The page

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

### A4.7 The reports

`check_figures` holds 233 cited figures across 4 reports to the model, and
`check_figures_fresh` holds `figures.json` to the live model (248 figures). Both will go off
loudly, which is the system working. Budget real time for the report prose: the gates catch
a stale *figure*, and nothing catches a stale *sentence*.

---

## A5. What the size buys — and it is not mass

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
is still needed. Going to `n = 2` is what deletes it — **that is route R1 in the brief, and
it is where the mass actually is.**

---

## A6. Order of work, if the span is retargeted

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

---

## A7. What will bite if the span is retargeted — all three MEASURED

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
