# The seven levels — handoff for continued development and explorer integration

Written 2026-08-12, end of the day the arc opened; brought current the same evening
after the operator's ruling cascade (band-outside → lean/seats → skin-and-bones →
replacement ops → the shape trade). For the agent taking over the "no cell floats,
the ship does" site re-org and its integration into the explorer. Where anything
here disagrees with an older phrase elsewhere (including analysis-v2 §4's band
position), THIS document and the ruling file win:
`~/data/airships-reviews/26-08-12-OPERATOR-RULING-band-position.md`.
Everything here is verified-at-write: the staged site is live, `make check` exits 0,
and every claim about the physics traces to a named document.

Read in this order: this file → `docs/HANDOFF.md` (the cell SSOT; its "THE SEVEN
LEVELS" section is the short version of this) → `~/data/airships-reviews/README.md`
(the ship-scale research index) → `~/data/airships-reviews/handoff/26-08-12-viz-agent-handoff.md`
(the ship.js port contract — your §4 self-check battery lives there, do not rebuild it
from memory).

## 1. The mission and the framing (operator rulings, do not relitigate)

- **No cell floats; the ship does.** Cell 0 = the first buildable block, deliberately
  not lighter than air. Ship 0 = the smallest assembly slightly lighter than air, at
  SEA LEVEL, declared SF 1.2 with SF 1.5 always shown beside it ("anything above 1").
- **`cell/levels.html` is a VISUALIZATION of the design and the blueprint/iteration
  surface. It is NOT a build timeline** — no schedule language on the page, ever. The
  explorer's levels get rebuilt to match the blueprint, not the other way round.
- **Materials of record:** roll-wrapped T700 carbon tube (never pultruded — hoop);
  **titanium CLAMPED connectors** — split clamshell sleeves, radial closure, bonded
  8–11 mm laps (the operator's words: "titanium, with clamped connectors"); Zylon-class
  formed film + PVD barrier; the printed polymer node is superseded history and stays
  in the catalog as such, last position.
- **Architecture of record:** single-band pressure skin (ONE cell-span — the step law
  is cubic; stacked/graded bands measured to buy no mass) + deep sandwich grid shell
  (two chord faces ~3 m apart, ring bays ~2 m, the hoop chords ARE the ring frames)
  + void core. Stubby 2:1 cigar, 52 m × 104 m plan of record. Vacuum, not helium;
  full vacuum, not partial.
- **Nothing crosses the void.** All global load passes around the surface as hoop —
  the keystone-arch law. Why: under external pressure every spanning member is a
  COLUMN (the sky shortens every diameter), and a 52 m column loses to Euler; the
  verified octet-fill studies all sink (1.03–1.37 kg/m³). The shell turns the load
  90° into hoop and works at strength, not slenderness. Two flagged exceptions that
  may someday exist: tension spokes against ovalization (unstudied alternative if
  SHIP-2 prices the stability reserve high) and SHIP-5 breach bulkheads (membranes,
  not trusses, only if cascade policy demands compartments).
- **Skin-and-bones terminology (operator, after the ruling):** the truss is an
  ENDOskeleton — the ship is a sealed skin of evacuated cells around a single
  two-walled skeleton, nothing in the middle. Sweep any stale "exoskeleton" phrasing.
- **Replacement-ops doctrine (operator Q&A):** a HOLED cell is near-free to carry
  (carcass plugs the wall, neighbour films back it, ~0.4 kg lift) — swaps are
  maintenance-window work, never emergencies. Paths: land-and-repressurize
  (re-evacuating ~184k m³ ≈ 19 GJ minimum ≈ 10–20 MWh real ≈ hours on ship
  generation) or aloft behind a clamped cofferdam leaning on the neighbours like a
  cell; NEVER an open hole (a cell-sized opening swallows ~10 t of air a minute).
- **Redundancy doctrine (band):** not more layers — every cell is its own sealed
  vessel; interior films are unloaded between healthy neighbours and catch the
  differential when one cell is holed; breach = one cell; the spreading-cascade
  policy is OPEN (SHIP-5) and the page says so.
- **Support doctrine (the three states, drawn in L4):** bench = sky on every side,
  net zero, self-balanced; band = one loaded face, it LEANS — the sky presses it onto
  the outer wall through short bearing seats (the through-loaded "mattress" state the
  crush law is written for); ring = pushes become hoop squeeze, the arch closed on
  itself.
- **BAND-OUTSIDE RULING (operator, 08-12 late — supersedes analysis v2 §4's "hangs
  inside the outer face" on this point):** the sealed wall wraps OUTSIDE the outer
  chord wall, pressed onto it by the atmosphere. Consequences: zero structural
  penetrations of the sealed wall (webs lace the two walls entirely behind it, in
  vacuum); lift boundary at the largest radius (both truss walls + webs count as
  lift); the LOADED outer film faces nothing but sky (every attachment lands on the
  unloaded inner film at corner land posts); ties demote to light retention straps
  (creep moot at occasional load — UHMWPE viable again); the jacket gains a hail-
  armour/standoff duty [TO VERIFY, SHIP-2/3]. Ruling file:
  `~/data/airships-reviews/26-08-12-OPERATOR-RULING-band-position.md`.
- **Decoupling doctrine (operator Q&A, 08-12 late):** radial seats transmit PUSH, not
  SQUEEZE — a leaning band has no tangential load path, so the skeleton takes effectively
  100 % of global hoop BY TOPOLOGY (band ceiling 47–67 kPa·m vs 2,634 demand ⇒ ≤~2.5 %
  even if rigidly engaged — its help is worthless, so it is deliberately not asked).
  The band's own arching is local only: seat-span slabs at ~1/3 capacity at cell-pitch
  ties. Band↔skeleton interfaces: bearing seats (force, 99.95 % — a cell weighs ~3.5 kg vs
  7,200 kg of push), light retention straps (position/handling), and the vacuum
  manifold (service + health monitoring). Film penetrations: ONLY at film corners
  where the membrane already terminates on joint land posts — the seat boss is a
  taller land post on the UNLOADED inner film; the loaded outer film is virgin.
- **Barrier stack:** exactly one LOADED barrier system (the band's outer films);
  one nearly-free inner terminal skin (10 g/m² at ≤1 kPa) closing the void; one
  UNLOADED weather jacket outside. No loaded outboard barrier — a barrier costs mass
  in proportion to the pressure it holds, and stacked pressure skins are the graded-
  band idea that measured to zero benefit. Void penetrations: plumbing/sensing ports
  only (trivial at 1 kPa); nothing structural.

## 2. Where everything lives

| thing | path |
|---|---|
| the blueprint page | `cell/levels.html` (shell + copy + bindings) |
| its logic + all figures | `cell/levels.js` (pane browser, SVG figure functions, `bindNumbers`) |
| its data | `cell/catalog.js` — CATALOG entries + `SHIP`/`BAND`/`GRID`/`ARTICLE` |
| the live cell model | `cell/model.js` + mirror `research/analysis/vacuum-cell.py` (parity-gated) |
| the explorer (untouched by this arc) | `cell/explorer.html` / `explorer.js` / `explorer-geom.js` |
| cell SSOT handoff | `docs/HANDOFF.md` (read "THE SEVEN LEVELS" + queue + traps) |
| ship-scale research | `~/data/airships-reviews/` — README is the index; `analysis/26-08-12-ship-scale-analysis-v2.md` is the numbers SSOT |
| ship.js port contract | `~/data/airships-reviews/handoff/26-08-12-viz-agent-handoff.md` (§3 reconcile, §4 gate values, §6 port order) |
| runnable ship physics prototype | `~/data/airships-reviews/prototype/ship.js` (+ selfchecks; predates v2 in places — reconcile per §3) |
| in-house production plan | `~/data/airships-reviews/26-08-12-production-machinery-note.md` |
| staged site | https://guppi.ca/airships/cell/levels.html — basic auth tyler/copper |

## 3. What is built (state at this commit)

The page is fully filled, all seven levels, first-pass:

1. **Catalog** — ONE centred pane (a second pane was tried and removed as duplicate).
   Tabs (Tubes/Connectors/Skins), prev/next arrows, and the true-relative-bore strip
   is a click-to-select size picker (labels on every bore, padded hit targets).
   Per part: schematic SVG, spec card, status chip, provenance line, red flags.
2. **The cell** — real Kelvin wireframe (`drawKelvinCell`, projected from the actual
   (0,±1,±2) permutation vertex set) + `massBar` (tube/joints/film with the float
   line = displaced-air mass, all live from `stockBuild()`).
3. **The band** — `drawBandSection` (octagon row, loaded film up, unloaded films
   down, shared walls) + the redundancy copy + facts (≈2×10⁴ cells, one layer by
   design, breach = one cell).
4. **The grid & skins** — the interplay paragraph (film→rims→frame ~7.2 t→face→
   chords→hoop) + `drawCellSupport` (bench / band-sits-face-down / ring) +
   `drawWebDetail` (one bay: ADJACENT cells face-down on the outer wall, the warm
   skin riding their landscape, webs behind) + `drawRingSection` (full ring: sealed
   wall outermost, both truss walls in the lift) + the ruled-junction and
   skin-and-bones paragraphs. Figure colour code (operator, 08-12): PINK = film
   loaded by atmosphere; BLUE DOTTED = film in vacuum, unloaded (L3 band section
   follows it: three pink top faces, everything else blue dotted). Seats are
   EMBEDDED — the cell sits on its face; never draw a seat as a prop.
   (`drawWallSection` REMOVED on operator direction — it drew the pre-ruling
   band-inside-the-sandwich arrangement.)
5. **"Closure" — PROVISIONAL name** (operator skipped five in his sequence; the page
   chips it "provisional name"; confirm or rename WITH HIM) — `drawShipClosure` +
   `drawLedger` (both-SF bars: +3.8 t green / −32.2 t red; never show one SF alone).
6. **Equipment & paint** — `drawShipEquip` callouts; budget = residual lift; lines
   named-not-weighed.
7. **At work** — links `../` (the wildfire dashboard, previous design, re-points later).

**OVERHAUL ROUND 4 (08-12 night): NAMED VIEWS replace the structure/view deck; the
patch's cross bars are PIPE.** Operator: replace "structure — light one, dim the rest /
view" with proper movement per level; render the grid's bars as the cell level's CF pipes
("they look and behave well there"); include the zoom-out ("I really like zooming out and
seeing the section you've detailed from a higher level") as a view button. Done as:
LEVEL_VIEWS registry + api.viewsFor()/applyView() — poses computed from the SAME surface
generators as the geometry, flown through the existing non-dive transition (eased from the
live camera; instant under reduced motion); `?view=` deep-link; the deck is now ONE box —
a per-level views row + a "this level's switches" row driven by data-lv (ship layer sbtns
folded in; #shipbox deleted). The grid's hoops/longerons/webs inside the patch are
strutInstances + tubeArcGeom + XM.pipe/pipeRim at schematic radii (SHIP-2 sizes chords).
The group-dim api (setGroup/?group) SURVIVES button removal — gates and deep links intact;
the cell's views apply groups as part of their poses. Traps paid: the views registry must
sit OUTSIDE the LEVELS array literal (an anchor comment lived inside it), and deleting a
deck group orphaned #toggleLoaded's wiring (null addEventListener kills the whole module —
the id-audit one-liner in the round-4 commit is the check to rerun after ANY deck edit).
**OPERATOR WISH RECORDED for the assembly arc: a ship-scale assembly animation in the
spirit of the cell's #69 — cells + cell-external CF pipe + connector flying in — "one
cell, and cell-external CF pipe and connector … assembling the entire ship."**

**OVERHAUL ROUND 3 (08-12 latest): THE GRID LEVEL IS A ZOOM, NOT A WARP** — operator
ruling: "I want the layers to be zooming into components of the existing airship, not
warping to a new thing." The old graded-band wedge (buildBay — the superseded stacked-band
idea, drawn as a bench prop) is deleted. buildGrid draws a lit patch of ship 0's OWN flank
superimposed on the whole ship kept faint: same coordinates, same generators — the ship's
surface math now lives in module-scope functions (shipDims / shipStation /
shipCellPlacements / shipSkeletonSegs) that both buildShip and buildGrid consume, so the
patch and the whole cannot drift. The forward third of the patch stands OPEN (bare chords,
warm seat ticks waiting on the wall) because an opaque wall hides the very grid the level
exists to show; one hero cell is drawn glass with its REAL half-pitch lattice inside,
tying the ladder's top to its bottom. Panel rewritten to the grid story (hoop 2,634 vs
band ≤67; bay/depth; per-cell push; seat-line-open chip). LEVELS gained a `depthR`
override (framing()) — the grid orbits a 12 m patch while keeping the 104 m ghost inside
the clip planes. NEXT in this pattern: the band level (the 3×3×2 abstract block is the
remaining warp) and per-course assembly on the grid.

**OVERHAUL ROUND 2 (08-12 later): the 190 m P-100 hull level is DELETED** — "we can get
rid of the hull level"; ship 0 tops the ladder at 7 levels. With it went buildHull, its
panel section (the wall doctrine line and wallWork binding moved into the ship section),
the hullLen/stale-177 gate checks, and a LANDMINE: a framing block that reached for
`LEVELS[LEVELS.length - 1]` to reframe "the hull" and would have silently reframed the
SHIP after the deletion. The ship gained ITS OWN CONTROL DECK (#shipbox: wall of cells /
skeleton / webs / void skin — the cell's structure/view deck hides there), the SKELETON
(hoops at bay pitch on both walls, longerons, Warren webs, all layer-toggleable, cutaway
works through it), panel dive-links into band/grid/cell, and `?layers=` deep-links for
screenshots. Rail renames: array→"The band", bay→"The grid" (their panel copy is still
the old story — the §4c rebuild owes them new sections). `#controls` had the SAME
display-beats-hidden footgun as #asmbox, found the same way — if you add a control deck,
write `#yourbox[hidden]{display:none}` FIRST. The gate now proves the wall toggle changes
drawn triangles, trusses exist as lines, and the frame restores exactly.

**THE EXPLORER GREW ITS SHIP LEVEL (08-12 late, operator direction):** `buildShip` in
explorer.js draws ship 0 as what it is — ~20k instanced Kelvin SHELLS (no internal
lattice; at that range a cell's lattice is sub-pixel) on the 52 × 104 stadium, pitch
DERIVED from surface area over BAND.cells so the drawn population equals the quoted one.
Figures come from catalog.js via a ctx merge in explorer.html (`ship.*`, `band.cells`,
two derived margins), scoping-chipped until the ship.js port. Rail slot: between bay and
the 190 m flight-reference hull (now "Level 8 … previous design, at work"). Traps paid
for: `#asmbox` needed `[hidden]{display:none}` (author display beats the hidden
attribute — the guide was showing on EVERY level); the hull depth-prepass was keyed on
levelIdx 6 and had to move to id-keyed. The full §4c level-merge (catalog tour, band
wrap, grid rebuild) is still ahead; this was its first stone.

**The number-binding system:** HTML prose carries no digits. `data-cat="a.b"` spans
resolve against `CTX = {ship, article, band, grid}` in `levels.js` (`data-f` =
decimals). Cell figures come from `model.js` live (the page can never disagree with
the explorer); ship figures are typed ONCE in `catalog.js` with provenance comments
and wear `scoping` chips. **`catalog.js` is the single swap point: when ship.js lands
under the gates, SHIP/BAND/GRID become imports and the chips come off.** Digits
inside generated SVGs are fine — they come from the data modules.

## 4. Your likely work, in order

### 4a. Iterate the blueprint with the operator
He redirects fast and concretely (this page went shell → filled → single-pane →
clickable strip → L3/L4 expansion → support figure in one day). Each figure is one
small function; each number is one data field. Keep edits cheap and screenshot every
change — the gates cannot see visibility.

**The iteration loop is `make stamp && make levelscheck` — about 10 s.** It boots the
page headless and fails on any page error, an empty figure, an unresolved data-cat, or
ANY text outside its SVG viewBox (the caption trap in §6, now a gate — it caught two
standing clips on its first run). The full chain is for pre-publish; do not pay 8
minutes per figure tweak. What no gate can see is still WHICH face is pink — the
compass in a figure remains eye-only, and the operator has caught exactly that once.

### 4b. Port ship.js under the gates (BEFORE any explorer ship-level)
Follow the viz handoff §6 exactly: reconcile the prototype to analysis-v2 (§3 lists
the known divergences — the step-law default and the 2,500 m default site are wrong
in the prototype), then land ship physics in `cell/model.js` AND `vacuum-cell.py` in
ONE commit (parity is bidirectional), `make analysis` BEFORE `make cellparity`,
reproduce the §4 value battery, keep every [TO VERIFY] flag. Then swap `catalog.js`
to imports. `check_explorer` failing a figure without a model source is the system
working.

### 4c. Rebuild the explorer levels to the blueprint
The explorer's `LEVELS` array (`cell/explorer.js:1878`) currently runs
strut → wall → track → cell → array → bay → hull, sharing ONE scene graph for the
four cell-framing levels (ordered by framing tightness — violating that makes a
dive-in read as zoom-out; see the comment above the array). The mapping:

| blueprint | explorer today | the rebuild |
|---|---|---|
| L1 catalog | strut/wall/track stages | per-part zoom stops fed by catalog.js (the tour machinery already generates stops from the article — reuse it) |
| L2 cell | 'cell' + the three stages | MERGE into one level: assemble/de-skin/zoom in a single clean UI |
| L3 band | 'array' | one-layer wrap, shared-wall story, breach vignette (one cell tinted, films take over) |
| L4 grid | 'bay' | chord grid + seat rail + band leaning on it, assembly-animated like #69's cell build (`jumpAssemble` idiom) |
| L5 closure | 'hull' | pump-down state + the both-SF ledger; hull becomes 52×104 ship-0 once ship.js is in |
| L6 equipment | — | new level (equipment stays visual until lines are weighed) |
| L7 at work | the dashboard | re-point `app/` renders at the new hull LAST, only on operator go |

Scene-graph rules that have bitten: any new mode scopes HARD to its level and
restores byte-exact on exit (the assembly animation does this — copy its pattern);
instance tints touch RGB never alpha; the stage cell is one shared scene.

### 4d. Deploy law for this arc
**Scope the gate to the change (operator ruling, on being made to wait 8 minutes for a
colour swap):**
- edits confined to `cell/levels.*`, `tools/check_levels.py` and docs →
  `make stamp && make stampcheck levelscheck` (~10 s) → publish → stage. Nothing the
  other gates verify has moved; running them is ritual, not verification.
- anything touching `cell/model.js`, `cell/catalog.js`, the generators, generated
  modules, the explorer, or the sim → the FULL `make check` before publish, as ever.
- when unsure which side an edit falls on, that uncertainty IS the answer: full chain.

**PRODUCTION RULING (operator, 08-12 late): this arc now deploys DIRECT TO PRODUCTION**
(`./deploy.sh pinkrobotics`) — the cell pages are behind the tyler/copper realm on
pinkrobotics.ca (verified: `/airships/cell/*` answers 401 unauthenticated; the monitor
root stays public by design), so guppi staging is retired for this work. Two cautions
survive the ruling: production's dirty-tree gate is REAL (a co-session's uncommitted
files block it — never ALLOW_DIRTY around someone else's work), and anything already
staged on guppi goes stale from here.

`make stamp && <the gate above>` → `tools/publish.py` → commit pink-sites →
`./deploy.sh pinkrobotics`. The old staging law, for the record: Production
(`./deploy.sh pinkrobotics`) is NOT part of this arc until the operator says the
re-org replaces the current site — he likes the current site; do not surprise him.
Verify after every stage: unauth `curl -I` = 401, auth'd = 200 with the new stamp.
The guppi auth realm (`@guppi_cell`) lives in the LIVE `/etc/caddy/Caddyfile` on
pink-edge — installed 2026-08-12 with the operator's sudo (admin API off → config
changes need `systemctl restart caddy`, NOT reload, and his password). **The helm
repo's governed copy (`ops/pink-edge/files/etc/caddy/Caddyfile`) is STALE by three
arcs — never "restore" from it**; syncing it back is an open helm chore.

## 5. The physics you must not garble (one paragraph each)

- **R-independence:** medium specific compressive strength (kJ/kg) is the only
  currency; both hoop demand and available depth scale with radius, so size fixes
  nothing. Cell-0 medium ≈ 10.9 kJ/kg vs a ~165 kJ/kg sea-level aligned-grid bar —
  which is why cells are the skin, never the spine.
- **The band:** one span kills 1 atm (cubic step law, rim-governed); ~2×10⁴ cells;
  in-plane capacity ~47–67 kPa·m vs hoop demand P·R ≈ 2,634 kPa·m at R = 26 — the
  band leans on the skeleton, the shell carries.
- **The grid:** hoop chords carry pR, longerons pR/2, webs shear; depth is
  load-bearing (ovalization resistance ∝ T²); chord σ_gov is lever #1
  (742 verified-class / 1050 mid / 1450 sourced ceiling → 52 m at SF 1.2 /
  SF-1.5-compliant / 80 m hull respectively).
- **Closure:** 52×104 → lift 225.5 t, mass 221.7 t @SF 1.2 (+3.8 t), 257.7 @SF 1.5
  (−32.2 t). Always both. Temperature window ≈ ISA+5 K.
- **Joints:** Ti clamp sleeves — the main load path never crosses the split seam
  (each half carries its half-circumference of glue; the seam is radial retention
  only); vacuum is the CURE clamp (bagging), never the service load path (no Δp at
  an interior joint, and 0.1 MPa × μ loses to 20 MPa glue by ~600×).

## 6. Traps this arc paid for (beyond docs/HANDOFF.md's list)

- `make stamp` REWRITES the files you just wrote (`?v=` hashes). Re-read before any
  Write; write plain `./x.js` imports and let the stamper stamp.
- SVG captions overflow their viewBox silently — every caption burn this arc was a
  too-long monospace string (≈6.6 px/char at font 11). Screenshot-verify EVERY figure
  change; check text extents against the viewBox arithmetic.
- Single-site `deploy.sh stage` rsyncs the site to guppi's DOCROOT ROOT with
  `--delete` (replacing whatever was staged); `stage-all` builds the composite tree
  instead. One site staged at a time is the designed behaviour.
- Headless-chromium screenshots with `#fragment` URLs glitch; capture the plain URL
  with a tall `--window-size` and crop with PIL.
- `pkill -f` needs the bracket trick (`http.serve[r]`) or you signal your own shell.
- Scratch on `~/tmp` or the session scratchpad, never `/tmp` (RAM tmpfs, has
  OOM-killed a service).

## 7. Open questions, with owners

1. **L5's real name** — operator (page chips it provisional).
2. **Chord coupon campaign** (σ1050 vs 1450) — SHIP-2; decides the hull size; the
   production machinery note argues the winding line and the campaign are one thing.
3. **Breach/cascade policy** — SHIP-5 (sacrificial gap? bulkhead membranes? valve
   doctrine). The L3 copy promises this study exists; keep it honest.
4. **Ovalization reserve** (0.4 [0–1.5] kg/m²) — SHIP-2 knockdown tests; tension
   spokes are the unstudied fallback, noted in §1.
5. **871's relaunched commercial floor** — watch `~/data/airships-reviews/` for the
   branch; review against `26-08-12-OPERATOR-RULING-871.md`; its verdict sentence is
   the project's next headline.
6. **Seat pitch** (operator question, 2026-08-12 evening; asked as hanger pitch
   pre-ruling — the arithmetic is support-direction-agnostic) — mid-bay band cells
   are supported only by their neighbours' shared frames until the nearest support
   line; scoping slab arithmetic says a 2 m one-way pitch OVERLOADS the band's own
   faces (~78 kN/m vs its 47–67 kN/m in-plane ceiling) while a support per cell
   (~0.9 m) is comfortable (~20 kN/m). The webs ledger line (0.5 kg/m²) has no member-level design
   behind it — SHIP-2/3 must fix the pitch BEFORE the band-cell retune below.
   POST-RULING FORM: this is now the SEAT RAIL requirement — the skeleton's outer
   wall must offer bearing points at CELL pitch (~0.9 m), not just bay pitch;
   per-seat ~12 kN on cm-scale Ti pads.
   OPERATOR CANDIDATE (08-12, on reading fig 6): no rail and no floor at all —
   set the hoop-chord pitch to the CELL pitch and land every cell's face directly
   on a chord. Same total hoop material by demand (P·R is fixed), spread over
   more, thinner lines; SHIP-2 must price the thinner chord's local buckling and
   what becomes of the bay/web layout before this is more than a candidate. It
   deletes the undesigned 0.5 kg/m² webs-ledger rail line if it wins.
7. **Band-cell retune — now a SHAPE TRADE (widened by the operator, 08-12 late):**
   a single-layer wall reopens the cell shape. Candidates: (a) asymmetric Kelvin
   (original scope — heavier outer rim/film, lighter inner, sides to seat pitch);
   (b) BRACED HEX PRISM honeycomb — straight through-crush columns, exactly 6 inner
   corner posts (matches the ≥6-seat finding), perfect tiling (no interstitial
   space), straight seams, hex dome films transfer; needs added diagonals (a bare
   prism is a mechanism, unlike self-bracing Kelvin) and forfeits the proven-article
   infrastructure (saw table, assembly order, the cubic crush law are Kelvin's).
   License: 865 film tool + crush-law rerun at band duty. Cell 0's process-proof
   role (clamps, seals, films, pump-down) is shape-agnostic and survives any ruling.
   Kelvin interstitial space, if Kelvin wins: vents inboard → vacuum → lift; hosts
   seams, manifold runs, strap points.
8. **Seat & strap interface** (evolved from the tie question after the band-outside
   ruling) — Ti bearing pad on the clamp sleeve (compression, mm-scale, cannot
   buckle) + light UHMWPE/Zylon retention strap (occasional load — creep moot).
   CONCENTRATION FINDING STANDS: a cell's ~70 kN over too few seats overloads
   article-class joints (5–7 kN members); wants ~6+ seat points per cell around the
   rim ring or a spreader cradle. Couples #6 (pitch) and #7 (retune); license = 865
   tool + U4. Catalog part `conn-tie` (now "Seat & retention strap"), decided.
9. **The web↔sealed-wall junction — RULED (operator, 08-12 late):** the operator
   found the hole (webs must cross the band as drawn in v2) and ruled option (c):
   band OUTSIDE the outer wall. Nothing crosses the sealed wall. The rejected
   alternatives, for the record: bag-inboard (purity for ~25–30 % of lift) and
   plating-on-frames (band sealed to ring planes). See the §1 ruling bullet and the
   ruling file in the reviews drop.
10. **Cell-side queue** (unchanged, `docs/HANDOFF.md`): the square-panel correction
   (#10) at the head, then #65's remaining proofs, #64, #60, #68.
11. **Helm governed Caddyfile re-sync** — small chore, helm session.

The operator's standing style notes: decisive recommendations over menus; verify
before claiming; numbers carry provenance or flags; bias toward shipping behind the
gates. He reads fast and redirects concretely — give him things to react to.
