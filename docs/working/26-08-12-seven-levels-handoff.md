# The seven levels — handoff for continued development and explorer integration

Written 2026-08-12, end of the day the arc opened. For the agent taking over the
"no cell floats, the ship does" site re-org and its integration into the explorer.
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
- **Redundancy doctrine (band):** not more layers — every cell is its own sealed
  vessel; interior films are unloaded between healthy neighbours and catch the
  differential when one cell is holed; breach = one cell; the spreading-cascade
  policy is OPEN (SHIP-5) and the page says so.
- **Support doctrine (the three states, drawn in L4):** bench = sky on every side,
  net zero, self-balanced; band = one loaded face, it HANGS by short tension ties from
  the outer chord face (the through-loaded "mattress" state the crush law is written
  for); ring = pushes become hoop squeeze, the arch closed on itself.
- **Decoupling doctrine (operator Q&A, 08-12 late):** radial ties transmit PUSH, not
  SQUEEZE — a hung band has no tangential load path, so the skeleton takes effectively
  100 % of global hoop BY TOPOLOGY (band ceiling 47–67 kPa·m vs 2,634 demand ⇒ ≤~2.5 %
  even if rigidly engaged — its help is worthless, so it is deliberately not asked).
  The band's own arching is local only: tie-span slabs at ~1/3 capacity at cell-pitch
  ties. Band↔skeleton interfaces: ties (force, 99.95 % — a cell weighs ~3.5 kg vs
  7,200 kg of push), sparse whisper-light tangential stays (position), and the vacuum
  manifold (service + health monitoring). Film penetrations: ONLY at film corners
  where the membrane already terminates on joint land posts — the tie horn is a
  taller land post with the same sealed base; never mid-panel.
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
4. **The grid & skins** — `drawWallSection` (jacket→chords→band→webs→chords→void
   skin) + the interplay paragraph (film→rims→frame ~7.2 t→hangers→chords→hoop) +
   `drawCellSupport` (the bench/band/ring three-panel).
5. **"Closure" — PROVISIONAL name** (operator skipped five in his sequence; the page
   chips it "provisional name"; confirm or rename WITH HIM) — `drawShipClosure` +
   `drawLedger` (both-SF bars: +3.8 t green / −32.2 t red; never show one SF alone).
6. **Equipment & paint** — `drawShipEquip` callouts; budget = residual lift; lines
   named-not-weighed.
7. **At work** — links `../` (the wildfire dashboard, previous design, re-points later).

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
| L4 grid | 'bay' | chord grid + hangers + band, assembly-animated like #69's cell build (`jumpAssemble` idiom) |
| L5 closure | 'hull' | pump-down state + the both-SF ledger; hull becomes 52×104 ship-0 once ship.js is in |
| L6 equipment | — | new level (equipment stays visual until lines are weighed) |
| L7 at work | the dashboard | re-point `app/` renders at the new hull LAST, only on operator go |

Scene-graph rules that have bitten: any new mode scopes HARD to its level and
restores byte-exact on exit (the assembly animation does this — copy its pattern);
instance tints touch RGB never alpha; the stage cell is one shared scene.

### 4d. Deploy law for this arc
`make stamp && make check` → `tools/publish.py` → commit pink-sites → 
**`./deploy.sh stage pinkrobotics` ONLY** (guppi.ca). Production
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
  band hangs, the shell carries.
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
6. **Hanger pitch** (operator question, 2026-08-12 evening) — mid-bay band cells are
   supported only by their neighbours' shared frames until the nearest hanger line;
   scoping slab arithmetic says a 2 m one-way pitch OVERLOADS the band's own faces
   (~78 kN/m vs its 47–67 kN/m in-plane ceiling) while a hanger per cell (~0.9 m) is
   comfortable (~20 kN/m). The webs ledger line (0.5 kg/m²) has no member-level design
   behind it — SHIP-2/3 must fix the pitch BEFORE the band-cell retune below.
7. **Asymmetric band-cell retune** (operator question, same evening) — the band cell's
   duty is one-sided (loaded film out, breach-only film in, through-crush, side-shear)
   and the cell already broke symmetry once for film reasons (14×12 rim vs 10×8 main).
   Candidate lean: heavier outer rim/film, lighter inner, sides sized to the actual
   hanger pitch. FLOORS on the lean: breach reversal (a neighbour's breach turns a
   side face into a loaded face), pre-band load states (pump-down, handling, bench
   proof), and factory one-block economics. License: 865 tool at band span + U4.
   Sequence AFTER #6. Expected win: a trim, not a transformation (the through-path
   octet — most of the tube mass — survives any asymmetry).
8. **Tie material + interface** (operator question, same evening) — rope-class ties
   (Dyneema/UHMWPE vs Zylon-class braid: sustained-load creep vs UV/moisture — open
   trade, [TO VERIFY]; ties live in the atmospheric gap under the jacket) ending in
   spliced soft eyes over printed Ti horns on rim-joint clamp sleeves. CONCENTRATION
   FINDING: two ties/cell ⇒ ~35 kN into single joints whose members are article-class
   (5–7 kN) — 3–7× over; keeping the frame at proven loads wants ≥~6 pickup points per
   cell around the rim ring, or a spreader cradle. Couples #6 (pitch) and #7 (retune);
   same license (865 tool + U4). Catalog carries the part as `conn-tie`, scoping.
9. **Cell-side queue** (unchanged, `docs/HANDOFF.md`): the square-panel correction
   (#10) at the head, then #65's remaining proofs, #64, #60, #68.
10. **Helm governed Caddyfile re-sync** — small chore, helm session.

The operator's standing style notes: decisive recommendations over menus; verify
before claiming; numbers carry provenance or flags; bias toward shipping behind the
gates. He reads fast and redirects concretely — give him things to react to.
