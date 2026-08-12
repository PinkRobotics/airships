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
3.13 kg total: **2.39 kg tube, 0.715 kg joints, 28 g film**. The joints grew 0.465 → 0.715 kg
on 2026-08-11 when the sunken frame bought back every amputated socket and added the land
posts — whole geometry costs printed material, and the freeze bill priced it. To float, the
cell would have to be under 218 g. **The tube is still three quarters of the mass** —
printing is still not the lever, and FLOAT.md carries a dated correction saying exactly this.

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
  are octet. Subdividing to even n deletes the whole boundary apparatus, but the old
  axial-only ~4.2 kg/m3 estimate did not survive the film check: sizing the face members for
  the hexagon-square edge load at SF 1.5 gives **10.76–12.51 kg/m3** across the five checked
  article-A rows. See `docs/FLOAT.md` §3.
- **State which article a number belongs to.** The bench article is 16.21 kg/m3 and is a
  process coupon; the reports' "design point" is a closed-form sizing law with no geometry at
  1.4319. They differ by one ratio — tube R/t 5 against 75.5 — and confusing them has cost
  real time.

## What is proven, and what the gate's words mean

`tools/check_assembly.py` (~4,900 lines, 16 proofs, ~160 s) proves all 432 member-ends against
the SDF that generates them — it imports `gen_nodes`, never re-derives, and since the sunken
frame it derives the frame exactly as `main()` does (nominal dirs for the sink decision, real
positions for everything measured) and threads `land_offs`/`post_axis` into every field it
evaluates. Headline:

    check_assembly: NOT PROVEN — 5 of 16 proofs fail (5 frozen in KNOWN, 0 new), 11 pass

Exit 0 means **no regression against a known-bad baseline**. It does not mean the joints hold.
The five standing failures: **P8** (ONE swept representative — the shortest tie's shaft rides
its cup mouth at 0.4 µm on the symmetric swing path; frozen with its physics read, fix =
cup-mouth chamfer or a 2D-corridor sweep), **P11** (13 landless nodes by census; all 51 are
bed-searched now, 13,877 mm³ of island, least bed contact 1.1 mm²), **P13**, **P14** (the
bill over-bills tube — stock_build still quotes centre-to-centre while the article saws nine
true cuts), **P16** (2,064 of 3,888 margins fail — down from 2,296: whole sockets cleared
localBuckling outright and moved transverseShear's 72 to bounded-undecided).

**P5 IS DEAD.** 0 ends cut by a land, wrap 1.00000 ×432, the seat is the full 28.274 mm²
annulus at every end, and the pass is a measured clearance (worst feature-to-land distance
printed in the proof), not a zero count.

- **Assemblable: yes**, exhaustively — all 332 closing ends swept, inside-out build order
  emitted as `buildOrder` in the frozen contract. The P8 row above is a sub-micron graze on
  one representative's worst pose, 375× inside the clearance band the sweep adjudicates.
- **Printable: no verdict.** All 51 joints are bed-oriented by the measured frame search
  (sunken nodes cannot print on their lands — the only flat at a land plane is a post top);
  the island volume and bed contact are published and gated, and the threshold on them is
  the printer question this repo refuses to invent. A6's blocker stands: the extraction grid
  is coarser than the 0.15 mm clearance, so the STL cannot certify its own fit.
- **Strong: nothing is proven strong.** Node equilibrium does not close either — max residual
  7,868 N — and no proof fails on that.

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

## THE SUNKEN FRAME — LANDED, regrown, frozen, drawn (#65 P5 arc, closed 2026-08-11)

The designer resolved P5's wrap ceiling on 2026-08-11, near-verbatim: "the wrap can grow
to the size of the joints, the size is arbitrary, the edge can be wherever — it's the
overall cell and the general shape that matters," and chose architecture A: **dyneema
fabric draped over the sunken structure**, land posts pinning the drape to the nominal
planes as the mating flats. The whole sequence the previous session mapped ran to
completion the same day; what follows is what happened, for whoever touches this next.

**The article now:** boundary nodes sink along their land-normal bisector (7.6 mm at
1-land nodes, 12.28 mm at corners — derived from SKUs, never typed); lands are offset
planes each collar-radius-plus-margin above the sunken centre; a land post (r 5 mm) grows
back up and is truncated flat AT the nominal face — the film's pin. Wrap 1.00000 ×432.
Cuts are nine true lengths in `manifest.cutList` (the sink shortens every
boundary-adjacent member — even the 36 rim edges split, hex-hex vs square-hex corners
sinking along different bisectors). Joints 0.715 kg. Contract re-frozen (11,732 properties
moved, bill read); ledger holds 19 rows, "5 frozen, 0 new".

**What the sink itself exposed, each fixed the same day:**
- `bore_start()` blew up exactly like `one_way_reach` had: through-centre `tan(beta)` on
  the sink's near-90° betas pushed four bore starts per square centre to 98.7 mm and
  quietly carved those spigots SOLID (mass 736 g on the first regrow). It takes the land
  offsets now — `(r·sinβ − off)/(−c)` — and the second regrow restored the bores (715 g).
  THE PATTERN, twice proven: any formula holding a feature away from a land plane assumes
  the plane passes through the centre until shown otherwise. One more is still unfixed —
  see the probe gap under traps.
- P8 grew its one honest defect: the shortest tie's shaft rides its cup mouth at 0.4 µm
  on the symmetric swing path (shorter cuts swing steeper). Probed: extra relief does NOT
  buy margin (clearance wobbles 0–30 µm as the pose set shifts — the ride is inherent);
  the tilt direction cannot dodge a circular cup. Frozen in KNOWN with two named fixes:
  cup-mouth lead-in chamfer in node_sdf, or teach the sweep the builder's 2D engagement
  corridor instead of the symmetric identity path.
- P13's typed elevation set died (every elevation now sits a tilt off-lattice); the check
  bounds elevations by the article's own measured `tiltMaxDeg` instead.
- The page's (SKU, length, deduction) cut signature stopped being unique (two rim cuts,
  one deduction): explorer.js assigns each member's group ONCE where pipes are drawn
  (nearest true length breaks ties) and cutStops reads `m.group` — the second derivation
  it used to carry lit all 36 rim edges on both rim stops before it was removed.
- gen_node_families now derives the sunken frame, groups members by true cut, PROVES the
  groups against manifest.cutList row by row, and hands the rows' own cutMm through; the
  page binds those (`sinkShortMm` = nominal − seats − cut is displayed per stop). The
  model keeps NOMINAL lengths as conservative physics; P14 (stock_build bills
  centre-to-centre, 48.8 m vs 39.8 sawn) is STILL OPEN and is its own commit.

**Page state:** buildCell sinks every drawn point from NODEMESHES `sinkMm` (source
points, so members/seats/ghosts/parts all follow); the P5 caption is out, replaced by the
sunken-frame story; the tube tour walks nine stops; the reviewer's KNOWN brief expects
land posts, not partial sockets. Screenshots verified by eye: corner joint (full sockets,
faceted post cap), hub (post disc at the face plane, six spokes seated), whole cell
(general shape exactly preserved — the designer's rule, visible).

## The cell assembles itself on the page (#69, added 2026-08-11 late)

The cell level carries an **assemble** control (bottom-left; `?build=1` plays it from a
URL, `?build=0.45` parks it mid-build for stills). The animation is the proof played
back, not choreography: the timeline is A3's own inside-out build order carried through
`nodes.generated.js` (`ASSEMBLY`, transcribed from the same four-line sort rule and
byte-identical to the report's buildOrder — verified at generation), each joint flies in
just before the first member that needs it, tree members slide home axially, closing
members arrive tilted at their own kinematic entry angle (their cut and swing relief,
the identity P8 sweeps) and rotate down onto their pilots. The skin hides until the
frame is whole because that is the build order too.

Mechanics for whoever touches it: default state is FULLY ASSEMBLED and the seated
instance matrices are byte-cached at build time — `apply(1)` restores them exactly, and
the gate asserts displaced = 0 AND maxDisp = 0 after a played build (watch the falsy-zero
trap: `x or 1` on a measured 0.0 invented a failure on this feature's first run — AND
AGAIN the same day on the sweep's settleWorstMm; it is the house's own trap and it bites
the person who just documented it). The mode is scoped HARD to the cell level (the stage
cell is shared; leaving the level snaps everything home in stepAssemble). Pile poses are
hashed deterministically — never Math.random, or no gate could reproduce a frame. Pipes'
per-instance stretch rides in their matrix column norms: the animation rotates the
seated columns and replaces only the translation, so a pipe cannot change length
mid-flight.

**Round two, all designer catches (same day, late):**
- **The build order is tree-constrained now.** The designer spotted the seam: the
  spanning tree roots at a square-centre joint while pure |midpoint| walks from the cell
  centre, so 27 tree members used to arrive AFTER their joint was pinned — and a 20 mm
  stub cannot engage sideways. A3 emits the constrained order (Kahn over the
  tree-dependency graph, same key among the ready set): every joint arrives CARRIED by
  its own discovery member, still 0 blocked at any turn. gen_node_families transcribes
  the same construction and its dir-attach guard refuses any divergence by name.
- **Every approach is a proven line.** escape_scan returns the direction it verifies;
  A3 emits all 216 as buildOrder.escapeDirs; closing members fly their reversed escape.
  Tree pairs slide the parent axis (A4's motion).
- **The page sweeps its own animation.** Every trajectory — fly arc, settle line, pipe
  capsule, rider sphere — against everything seated at that timeline moment; fouling
  arcs replanned from a candidate set; residue REPORTED and gated (currently 217
  trajectories, 0 replanned, 0 fouling, 0 settle penetration). MUTATION-TESTED: collapse
  the arcs and it reports 2 fouls at 7.4 mm — the sweep can fire, so its zero means
  something. Joint collision body is the central-mass sphere (core+lip+2, derived);
  bare stubs are accepted crossings.
- **The player is an assembly guide**: wide top scrubber, replay / step-back /
  play-reverse / pause / play / step-forward / speed; captions name each part, its saw
  length, group, both joints by STL name, and the swing angle — all off generated data.
  `?build=1` plays, `?build=0.45` parks.
- **The ledger** (cell panel, above the metric boxes): total, film, tube and joints
  split primary/secondary, displaced air + float target + to-shed at sea level and at
  altitude, crush tf/kPa at both — every row bound, breakdown sums to the total.

**Round three (guide mode v2, designer-directed, `6953169`'s successor commit):**
- **Steps RUN the animation** — one part per press flies its full proven approach at
  watchable speed (GUIDE_PART_SECONDS 2.4 at 1×); back-step flies the newest part OUT
  and parks on the previous. Guide state = `state.assembleGuide {idx, alpha, to}`;
  `apply(t, guide)` overrides per-event alpha: strict prefix seated, suffix piled, one
  part at `alpha` — WHICH IS THE SWEEP'S OWN MODEL, so guide mode is the page's most
  literally proven view.
- **Two bars**: COMPONENTS (park on any of 217 steps → `assembleGuidePark(i)`) and THIS
  PART (scrub the current part's alpha at 1000 ticks → `assemblePartAlpha(v)`) — the
  slow-motion control. Caption on its own line below the transport.
- **The moving part is LIT** (warm tint), seated parts quiet grey, piled darker — written
  into instance tints (RGB never alpha) by `tintFor` inside apply(); `applyGroup(state.group)`
  takes the tints back the moment the article is whole (stepAssemble calls it at t=1 and
  on level-exit restore — if tints ever look stuck dim, that call went missing).
- **Speeds [⅛ ¼ ½ 1 2]** — global timeline and guide steps both scale by it.
- Global play still uses the overlapped timeline; entering guide from mid-play and back
  causes an accepted visual pop (~8 parts leap between overlap and prefix states).

**Round four (same night):** loop + bounce buttons (`assembleLoop('loop'|'bounce')`,
toggles, 0.8 s breath at each end owned by ARRIVAL in stepAssemble, cleared by every
other transport control and the scope guard); the cell level's framing target is +0.075 z
so the article sits below the guide card; the caption is TWO lines (cap1 = what the part
is, cap2 = joins/carries/motion — built per event, carried through windows and
assemblyGuide). And the SETTLE IS THE MODEL'S MOTION AT ITS OWN SCALE — the designer
caught that the swing angle belongs to a member already in its gap pivoting about its own
middle: closing members now fly (tilted) all the way TO the seated midpoint and the
settle is pure rotation in place (P8's pose sequence literally); tree pairs stage ONE
real engagement out (stubMm + 8, off the manifest) and slide that far home. Window split
FLY_END = 0.75. Sweep re-verified: 217 trajectories, 0/0/0.

## The loaded skin — solved, formed, drawn, gated (#63, closed 2026-08-12)

The film cannot be installed flat: reaching its loaded shape needs 4.12% membrane strain
and the fibre gives 0.27–0.40% at working stress — the analysis said so, the independent
physics audit reproduced it, and the page carried it as an unresolved item. Resolved now,
and the answer changed the manufacturing story.

**`tools/gen_skin.py` solves the loaded surface.** The 72 real film panels — 48 equilateral
spoked-hexagon triangles (inradius 72.36 mm) and 24 quarter-square right isosceles
triangles (inradius 51.92 mm; NOT the analysis' half-square, see the discrepancy below) —
each get the true uniform-tension membrane `div(∇w/√(1+|∇w|²)) = −2/R` at the model's own
operating law (R = 2.125·r_panel, so T = pR/2), P1 FEM with Picard on the slope weight,
pure numpy (scipy is deliberately not a dependency of this repo). Reproductions gate the
solver before its answer is used: on the incircle disc it returns the analysis' own
0.25·r cap (0.24981 measured); in the linear limit it lands on the exact Saint-Venant
closed form w = 2·d₁d₂d₃/(3rR) at second-order convergence; symmetry holds to 4e-16. The
film is pinned on the 5 mm land-post tops (the sunken frame's own boundary condition),
and the free film is proven to clear every bare tube it is not bonded to by 14.5 mm at
the worst pass (members clipped 40 mm at the ends for the joint body — the first firing
of that gate reported 2.6 mm, all of it from inside a printed joint, which is what the
clip is for).

**The solved numbers** (`research/geometry/skin/loaded-skin.json`; page copy
`cell/skin.generated.js`; `make skin` regenerates, `skincheck` re-solves and
byte-compares inside `make check`):
- sag 25.217 mm at a hex-panel centre, 18.811 mm at a square — 0.35·r, deeper than the
  0.25·r cap idealization, because a triangle is not its incircle; the cap law still
  sets the tension;
- tension 7,790 / 5,589 N/m at sea level, 5,742 / 4,120 N/m at 2,500 m;
- **displacement debit 10.35% (18.44 L): the pumped-down article displaces 159.76 L**,
  not its 178.2 L outline. The analysis' smeared 8.57% is reproduced as a check, then
  superseded. The page ledger carries the loaded rows (float target at the loaded shape:
  ×16.0 sea level, ×20.5 at 2,500 m).

**The gore study — measured, and it killed flat cutting.** Radial gores at k = 3/6/12
leave 0.68/0.32/0.20% (hex) and 0.77/0.48/0.46% (square) worst residual strain, measured
by least-squares flattening of every mesh edge. Even twelve gores per panel fails the
square's 0.27% budget — and would mean 864 film slivers and 84.8 m of seam lying on no
structure. **The net is therefore FORMED, not gored: its outline, 23 cuts and 13 folds
are unchanged from the proven flat net, and each face's panel field is pressed to the
solved surface before assembly** — two dies (one per face shape), 14 pressings, every
dimple edge ending on a member line where w = 0. `formingJustified` gates the verdict:
if a future flattening clears k ≤ 6, it goes red and the decision reopens. What remains
open is the forming PROCESS — pressing a Dyneema-class laminate to a permanent crown
without crazing the barrier stack — a coupon question that joins E6.

**The page pumps down.** `film: slack/loaded` in the view controls eases the film between
the flat net and the solved dome field: a second surface node (`CellSkinLoaded`) lerped
between two generated buffers, the unfold's own geometry-swap pattern, scoped by node id
so the flat net and the array skins are untouched. check_explorer drives the real button:
the drawn frame must gain exactly the dome field's triangles while the flat film steps
aside, the numbers read back must equal loaded-skin.json's (the page's import and the
gate's record are separate artifacts of one generator), and the slack frame must return
exactly. The gate is mutation-tested — a corrupted record fails by name.

**Found while cutting the panels; recorded for the audit round; deliberately NOT fixed
here:** `PANEL["squareSpoked"] = 1/(2+√2)` of the EDGE (73.42 mm) is the inradius of a
HALF-square — one diagonal — but the article's four in-plane ties quarter each square
(both diagonals: gen_nodes line ~153, vertex→face-centre), so the real square panel
inradius is `S(2−√2)/2` = 51.92 mm. The published square-panel tension, film mass and
smeared volume rows are computed on the wrong (larger — conservative for mass, wrong for
loads) panel. Analysis-layer correction with prose-gate consequences; it belongs with
the ~/data/airships-reviews audit integration, not in this commit.

## Open work, in priority order

1. **#65 clear the remaining frozen proofs** — P5 is dead; the bill is now P14 (stock_build
   must bill the nine cuts, not centre-to-centre — 0.44 kg of phantom tube, its own reviewed
   commit), P8 (cup-mouth chamfer or 2D-corridor sweep), P16 (bench tests named per row),
   P11 (printer threshold decision), P13 (pinned-row licensing — memo at ~/tmp/p65/MEMO.md).
2. **#64 integrate the barrier and seam notes** into `research/notes/` + `sources.json`. Both
   drafts are complete at `~/tmp/skin-barrier/`. Harmonise the budget first — 2.90 cm³/(m²·day)
   is right for the 178 L article; `seams.md` deliberately used the stricter 1.6 and says so.
3. **#60 remaining**: export the net as SVG/DXF — `tools/gen_skin.py` now exists and holds
   the solved surfaces and outlines, so this is a reader of loaded-skin.json plus the seam
   schedule (23 cuts = 5.766 m) and fold list (13). The formed net's outline is the flat
   net's, unchanged; the export should carry the per-face dimple fields as die references.
4. **#68 make `make check` skip unchanged work** — read the safety constraints in the task
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
- **FOUND, NOT YET FIXED — probe_node measures the octet-SKU field on rim arms.** Its direct
  node_sdf call (check_assembly.py ~line 970) predates the `kinds` parameter and never got
  it: every bearing/wrap/rib/lip/section probe on a rim arm samples a field with 10 mm
  sockets where the STL has 14. The frozen contract encodes those octet-flavoured numbers
  consistently, P4's radii are analytic (that is why P4 passes anyway), and the probe sample
  radii are ALSO global — so the fix is per-arm kinds AND per-arm sample radii together,
  measured, diffed and frozen as its own commit. Deliberately not slipped into the sunken-
  frame freeze: one change-class per freeze is what keeps the bill readable.
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
