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

## The one thing that keeps costing time

**The explorer does not draw the parts.** Every joint on screen is `sphereGeom` plus twelve
`socketConeGeom`. `cell/nodes.generated.js` carries data only; `explorer.js` loads no STL.

Three separate "bugs" the designer found by eye all traced to this and none were real geometry
faults: the hub resized four times, the rim drawn with no receivers, and interference inside
the sockets. Measured fix: re-run the same SDF coarser rather than decimating — node 09 gives
**3,716 triangles against 33,280 at 0.1% mass error**; all 51 ≈ 190k triangles, ~1 MB gzipped.
**Task #67, and the highest-value work left on the page.**

## Open work, in priority order

1. **#67 draw the real node meshes** — above. Retires a whole recurring class of complaint.
2. **#63 develop the net for the loaded dome shape.** The flat net now exists and is provably
   cuttable, but panels bulge at h/R = 0.25 needing 4.12% membrane strain — **cut it flat and
   the film comes up drum-tight with any barrier coating crazed on first pump-down.** This is
   the gap between a diagram and a cutting file.
3. **#65 clear the five frozen proofs.**
4. **#64 integrate the barrier and seam notes** into `research/notes/` + `sources.json`. Both
   drafts are complete at `~/tmp/skin-barrier/`. Harmonise the budget first — 2.90 cm³/(m²·day)
   is right for the 178 L article; `seams.md` deliberately used the stricter 1.6 and says so.
5. **#60 remaining**: export the net as SVG/DXF from a `tools/gen_skin.py`, with the seam
   schedule (23 cuts = 5.766 m) and fold list (13).
6. **#68 make `make check` skip unchanged work** — read the safety constraints in the task
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
