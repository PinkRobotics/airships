# Handoff — the vacuum cell

Written 2026-08-11 at the end of a long session, for someone picking this up cold. Everything
below is verified rather than remembered: `make check` exits 0, the tree is clean, the site is
live. Where a number appears it came from running the code, not from recollection.

## What the article is

A Kelvin cell (truncated octahedron), **709 mm span, 178 L**. 216 purchased carbon tubes on two
SKUs — 10×8 mm for 180 members, 14×12 mm for the 36 rim edges — and **51 printed joints**.

The designer's framing, and it should drive priorities: *"these 3d printed components are the
entire airship really… the only thing that is really actually designed in this entire airship
is these connectors, then its stock pipe, stock skin and paints, and stock parts."* Everything
except the joints is bought.

### Sizing, because the naming is easy to get wrong
- The model's `span` parameter **is the square-face-to-square-face distance**. At S = 0.709 that
  is 709 mm.
- **Hex face to hex face is NOT the same** — it is `S·√3/2` = 614 mm, 13% closer. A truncated
  octahedron is not equidistant in the two directions and cannot be made so.
- Corner to corner is 793 mm. Edge (and therefore the long member's cut) is `S/(2√2)` = 251 mm.
- Cells tile on **BCC**, and the cubic sub-lattice spacing is exactly S — so an N×N×N block at
  S = 1 m is N metres on a side and holds **2N³ cells** (a second cell sits at every body
  centre).

### Mass, and what actually decides float
2.88 kg total: **2.39 kg tube, 0.465 kg joints, 28 g film**. To float it would have to be under
218 g, so it is 16.9× over. **The tube is five sixths of the mass** — printing is not the lever.

## The 1 m cell (asked and costed 2026-08-11)

The designer wants square faces at 1 m so an N×N array occupies N×N metres. That means S = 1.0.

| | 709 mm | 1.0 m |
|---|---|---|
| edge / cut length | 251 mm | 354 mm |
| enclosed | 178 L | 500 L |
| load per hexagon | 1.69 tf | 3.36 tf |
| whole surface | 17.4 tf | 34.6 tf |
| braced rim holds | 2.83 atm | **1.01 atm** |
| Euler margin, same tube | 1.82 | **0.46** |

**There is no spare margin to spend.** Demand grows as L² while buckling capacity falls as
1/L², so **margin goes as 1/L⁴** — a 1.41× span costs a factor of 4. At 1 m with today's tube
the members buckle and the rim has no margin at all.

Scaling the tube geometrically to about **14×11 mm** restores the Euler margin exactly, but
then tube mass grows as L³ alongside volume, so **kg/m³ is unchanged**. A bigger cell of the
same architecture is not lighter per litre once the tube has to grow with it. What size really
buys is **parity**: at the right subdivision a hexagon face gains lattice points of its own and
the whole rim-and-spoke apparatus stops being needed.

Retargeting is a parameter change rather than a redesign — `span` flows through the model — but
every gated figure moves and `check_assembly` re-proves all 432 member-ends. Bounded, and worth
its own session.

## The mass question has its own brief now — `docs/FLOAT.md`

Everything about whether this article can float, and what would make it, lives there: the goal
state (0.9569 kg/m3, everything counted, gated), where the mass actually is, and four priced
routes to closing the gap. Two self-checking tools back it, `tools/scale_study.py` and
`tools/subdivision_study.py`. The three findings that change how you should read the rest of
this document:

- **Size is not a lever.** kg/m3 and every margin are invariant under geometric scaling. The
  1 m retarget is still costed (Appendix A of FLOAT.md) but it is not a route to floating.
- **69% of the tube by length holds the film, not the vacuum** — only 60 of the 216 members
  are octet. Subdividing to even n deletes the whole boundary apparatus: ~9.3 -> ~4.2 kg/m3.
- **State which article a number belongs to.** The bench article is 16.21 kg/m3 and is a
  process coupon; the reports' "design point" is a closed-form sizing law with no geometry at
  1.4319. They differ by one ratio — tube R/t 5 against 75.5 — and confusing them has cost
  real time.

## What is proven, and what the gate's words mean

`tools/check_assembly.py` (~3,300 lines, 16 proofs, ~120 s) proves all 432 member-ends against
the SDF that generates them — it imports `gen_nodes`, never re-derives. Headline:

    check_assembly: NOT PROVEN — 5 of 16 proofs fail (5 frozen in KNOWN, 0 new), 11 pass

Exit 0 means **no regression against a known-bad baseline**. It does not mean the joints hold.
The five standing failures: **P5** (216 ends cut by a mating land, worst wrap 0.304), **P11**
(13 landless nodes; 37 of 51 carry unprintable islands), **P13**, **P14** (the bill over-bills
tube), **P16** (2,296 of 3,888 margins fail).

- **Assemblable: yes**, exhaustively — all 332 closing ends swept, inside-out build order
  emitted as `buildOrder` in the frozen contract.
- **Printable: no.** P11, plus A6's blocker: the extraction grid is 5× the 0.15 mm clearance
  the capture depends on, so the STL cannot certify its own fit.
- **Strong: nothing is proven strong.** Node equilibrium does not close either — max residual
  8,080 N, only 9 of 51 nodes balance — and no proof fails on that.

## The explorer draws the parts now (#67, closed 2026-08-11)

Every joint on screen is the generator's own mesh — `cell/nodemeshes.generated.js`, written
by `tools/gen_display_meshes.py`, regrown by `make nodes`, held fresh by a source-hash check
in `make nodescheck`. The ball-and-cone stand-ins are gone, and with them the whole class of
"bug" the designer kept finding that was never in the geometry.

What the measurement changed about the plan, because the next person will be tempted to
"just extract coarser": the handoff's old "node 09 at 3,716 tris, 0.1% error" was ONE LUCKY
NODE. The full field coarsened to res 40 loses a **median 23% of volume, and 30% on every rim
vertex** — the 1.05 mm slot annuli and 1.6 mm collar walls alias below a 2.5 mm cell, in no
monotone way. So the article draws a **display field** (`node_sdf(display=True)`: the
additive half, no slots/bores/ribs — those sit under the drawn pipes) at res 48, and the
five family REPRESENTATIVES ship at print resolution with everything in, swapped in when the
connector tour frames them. The module is 3.6 MB raw / 2.1 MB gzipped; if that ever hurts,
the bounded fix is a lazily-fetched binary sidecar for the reps.

Pipes are now drawn seat to seat — each end stops at its joint's own slot base, so the drawn
article IS the cut schedule (instances stretch axially onto the drawn span; boundary insets
bend the lattice a few percent and a short pipe read as "not connected"). The gate asserts
joints, reps and pipes by count AND asserts the rep swap as triangle arithmetic on the
rendered frame, stop by stop.

## THE SUNKEN FRAME — decided, rule landed, article NOT yet regrown (#65, in flight)

The designer resolved P5's wrap ceiling on 2026-08-11, near-verbatim: "the wrap can grow
to the size of the joints, the size is arbitrary, the edge can be wherever — it's the
overall cell and the general shape that matters," and chose architecture A: **dyneema
fabric draped over the sunken structure**, land posts pinning the drape to the nominal
planes as the mating flats.

`gen_nodes.boundary_frame()` implements it: boundary nodes sink along their land-normal
bisector until every in-plane arm's collar clears its former plane (sinks: 7.6 mm at
1-land nodes, 12.3 mm at corners — derived from SKUs, never typed); lands become offset
planes; a land post (r 5 mm) grows back to the nominal planes, truncated flat by the same
lands-last rule. Full sockets, wrap 1.0. Validated on node 22 (`--only 22`: closed,
0 arms in air). The sink also exposed and fixed a real formula hole: `one_way_reach`
exploded on NEAR-opposed arm pairs (178-179° after sinking, past the collinear guard) —
a hub slot base went 16.4 → 96.6 mm; pairs ≥ 175° are now opposed by definition.

**The rule is INERT until `make nodes` runs** — the committed STLs/manifest/contract are
still the on-plane article, so every gate stays green. DO NOT regrow yet: the sequence
that keeps the proofs honest is
  1. teach `check_assembly` offset lands (79 land-touching lines; it reconstructs
     node_sdf args itself and would otherwise measure a field the STLs are not),
  2. `make nodes` (regrow all 51 + families + display module),
  3. run the prover, READ the diff, `--freeze` with the designer's sign-off (he has
     authorized the redesign; still print the bill),
  4. model: keep NOMINAL lengths as conservative physics (members shorten under the
     sink → real margins better than quoted); manifest cutList carries true cuts (this
     is also P14's fix — stock_build must bill cuts, not centre-to-centre),
  5. page: display module rows carry per-node `sinkMm` — apply as drawn-point offsets,
  6. `make jointreview` re-verifies all 51 against the vision baseline (51/51 pass on
     the old article, verdicts committed).

Working notes for step 1, the prover surgery (mapped, not yet started):
- `face_planes(` is called at three sites in check_assembly.py (~411 per-end setup,
  ~1965 shared-land logic, ~3098 pairwise checks); "land" appears on 79 lines. The
  prover must call `gen_nodes.boundary_frame()` per node exactly as main() does —
  NOMINAL dirs for the sink decision, then real positions/dirs for everything measured
  — and pass `land_offs`/`post_axis` into every node_sdf it evaluates, or it measures a
  field the STLs are not. P5's wrap measurement, P10 land-integrity and bore-vs-land
  logic all read lands directly and need the offset carried through.
- After the regrow, expect the ledger to move EVERYWHERE (positions, angles, cuts,
  masses, wraps, print metrics). Exit 1 with a long diff is the correct first result;
  read it, then `make contractfreeze` prints the bill before capping.
- The page edits for step 5: buildCell's `pts` / rim corner points / `hexCorePts` gain
  the per-node sink offsets (mm→m via /1000) from NODEMESHES rows matched on
  (role, u); the P5 caption in explorer.html ("the land truncates its socket") comes
  OUT once wrap is 1.0, and the vision reviewer's KNOWN brief in
  tools/review_joints.py drops its P5 lines the same day.
- Page/api state: cell/explorer.js gained `cellFrame` (vision harness) after the last
  deploy — the live site is one commit-family behind; redeploy rides the regrow.
- The goal the designer stated for this arc: "get this model looking complete."

## Open work, in priority order

1. **#63 develop the net for the loaded dome shape.** The flat net now exists and is provably
   cuttable, but panels bulge at h/R = 0.25 needing 4.12% membrane strain — **cut it flat and
   the film comes up drum-tight with any barrier coating crazed on first pump-down.** This is
   the gap between a diagram and a cutting file.
2. **#65 clear the five frozen proofs.**
3. **#64 integrate the barrier and seam notes** into `research/notes/` + `sources.json`. Both
   drafts are complete at `~/tmp/skin-barrier/`. Harmonise the budget first — 2.90 cm³/(m²·day)
   is right for the 178 L article; `seams.md` deliberately used the stricter 1.6 and says so.
4. **#60 remaining**: export the net as SVG/DXF from a `tools/gen_skin.py`, with the seam
   schedule (23 cuts = 5.766 m) and fold list (13).
5. **#68 make `make check` skip unchanged work** — read the safety constraints in the task
   first. This repo has twice shipped a gate that lied by comparing a stale file.

## Decided, do not re-litigate

- **Vacuum, not helium.** Settled and gated in `research/analysis/helium.md`.
- **Seams: wet-applied curing adhesive in a FIN seam**, not tape and not heat-sealed. Heat seal
  is impossible — 160 °C is 32 K above the UHMWPE fibre's melt onset. An inside lap outgasses
  46× the entire budget; the same adhesive edge-on is 0.04%. Cut as a Steinhaus–Johnson–Trotter
  path for zero three-way junctions. (#62)
- **Barrier: PVD-metallised faces + vacuum impregnation at the seams**, not one dip. Electroless
  is dead — the bath temperature Dyneema survives is the one that cannot coalesce a film. (#63)
- **Tape is not a vacuum seal.** Best-practice butyl vacuum bagging spends the whole decade
  budget in **4.2 days** while butyl's material floor is 290× inside it. The gap is workmanship.

## Traps that have each cost real time

- **`main` is committed but NOT pushed.** Local commits do not survive a disk loss, which was
  the reason for committing. Ask first; the remote is private.
- **Never write to `/tmp`** — 45 GB RAM tmpfs, has OOM-killed a service. Use `~/tmp/`.
- **`pkill -f` can match your own shell** and killed a session today. Collect PIDs from `pgrep`
  and kill them individually. Clean up `serve.py` after every screenshot — 13 orphans
  accumulated in one session.
- **A background-task notification fires when the WRAPPER exits, not the work.** A `make check`
  launched with `& sleep 2` reports "completed" immediately and its log looks truncated because
  it is still being written. Poll for a sentinel line.
- **`make stamp` before any check** after touching `cell/` — the site hash moves and
  `stampcheck` fails first, wasting the run.
- **Use the fast path.** Explorer-only edits: `make stamp && make explorercheck` is **11 s**
  against ~4 min; `check_assembly` alone is 122 s of the chain. Full chain once before commit.
- **Editorial sweeps break things.** Two defects came from find-and-replace over prose without
  reading around each hit: a concatenated label got its first half replaced and the tail welded
  on, and a gated `data-n` was deleted with its paragraph. Before deleting copy, check
  `grep -c 'data-n="X"' tools/check_explorer.py`.
- **Prose is not gated against the plan.** "crushed, sealed and pumped down" survived review and
  was wrong three ways — the real order is bake out, bond the barrier in the chamber, seal last,
  and the atmosphere does the crushing afterwards. Nothing holds page copy to
  `VERIFICATION-PLAN.md`.
- **State that is shared between levels leaks.** The unfold blanked the connector and tube tours
  because they share the stage cell. Scope any new mode to the level that owns it.

## Working on the explorer specifically — read this before touching cell/explorer.js

These each cost a round trip with the designer on 2026-08-11, and every one was invisible to a
green `make check`.

- **`api.tick()` is NOT the render loop.** The page runs
  `requestAnimationFrame` -> `frame()` -> `advance()` -> `renderBody()`. The headless gate calls
  `api.tick()`. Put per-frame work in `advance()` or it runs under test and never in a browser —
  which is exactly how an animation shipped "verified" and did nothing when clicked.
- **Instanced nodes cannot be dimmed by `dimOf`**, which returns 1 for them; their shading is the
  per-instance TINT buffer. And write tint to **RGB, never alpha** — cell families are opaque
  surfaces, the shader discards `vTint.a`, so an alpha fade renders nothing while a probe reading
  the array reports a perfectly dimmed scene.
- **`cam.radius` is the bounding radius and only sets the clamps. `cam.distance` is where the
  camera actually sits.** And raise `cam.maxDistance` BEFORE writing distance or the clamp
  silently caps it and the move looks like no change at all.
- **Ease camera moves from the LIVE camera, not the level's defaults** — otherwise a user who has
  zoomed somewhere gets a snap to the default on the first frame.
- **Scope any new mode to the level that owns it.** The stage cell is shared by the connector,
  tube and skin levels; a leaked flag blanked two whole tours.
- **A flat sheet edge-on is invisible.** Anything planar needs its facing decided deliberately.
- **Labels are pushed clear of the article** by a keep-out disc at 46% of the smaller viewport
  dimension (30% was still inside the silhouette). Direction is preserved, only distance changes.

**THE META-LESSON, and it is the most useful line in this file.** The gates hold every number on
the page to the model and cannot see whether anything is *visible*. Six consecutive faults in one
feature — rotation, frame loop, camera axis, camera field, clamp, tint — all passed a green check
and were each found by the designer looking at the screen. **Screenshot after every visual
change**; `tools/screenshot.py` with `A3D_GPU=1`, and add a `?param` if the state needs a click
to reach. A frame-content assertion now guards the unfold, but assertions on *properties of the
data* will keep missing faults in *what is drawn*.

## Deploy path

```
make stamp && make check                 # or make explorercheck for explorer-only work
python3 tools/publish.py                 # -> pink-sites/pinkrobotics/airships
cd ../pink-sites && git add -A pinkrobotics/airships && git commit
./deploy.sh pinkrobotics                 # refuses a dirty tree, exit 65
# purge Cloudflare: token ~/.config/cloudflare/token-dns, zone ec339e336294deb8339928dcb4919dcd
```

Live behind Caddy basic auth **tyler/copper** at `pinkrobotics.ca/airships/cell/explorer.html`.
