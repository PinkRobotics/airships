# The honest ship — the overnight of 2026-08-12/13

The operator's brief, near-verbatim: *fully integrate the new idea into pink robotics;
main page gets the general idea, gritty details and render behind the password; every
explorer level gets a relevant view; a complete ship with all struts and components you
can fly through, film pressure-wrapped on; do the maths and physics — let's see if it's
actually true and if the ship actually doesn't crush; two 3× review sets at the end.*
Fable at max effort, tall not wide. This file is the record; every claim below is
committed code or a committed number.

## What the night proved (the one-paragraph version)

**Ship 0 as ruled does not float once the two-walled shell's stability is checked with
real shell mechanics.** The first draft of the checks said +6.4 t at the declared factor;
a three-refuter adversarial panel found eleven confirmed bugs (Bryant's load-side divisor
missing, the ring-plane crimp built on the wrong triangle leg and the sphere coefficient,
a brace pitch the drawn fan cannot produce, caps escaping two duties, and seven more);
fixed, the harsh-basis verdict is **0.698 — sinks by 97.3 t** at SF 1.2 on mid coupons.
The licensed fallback (v2 §1's tension spokes, licensed by exactly this finding) came in
at 20 t of cord replacing ~120 t of compression iron, and the best defensible world
(frame-practice GI knockdown 0.65 + 1,450 MPa coupons) floats at **+12.5 t**. The float
decision is now, explicitly and on every page, two named test campaigns: the GI knockdown
tests and the chord compressive coupons. Retroactively, v2's +3.8 t ledger was never real
— its 0.4–1.5 kg/m² stability reserve was an order of magnitude light.

## The commits, in order

- `8a8b0db` — tools/ship_scoping.py v1: self-checks reproduce the v2 closure; first
  verdict (+6.4 t — later refuted); the FIRST finding already in it: ring-plane webs are
  a missing member class; the float window inverts (the band's diluting mass is gone).
- `4637467` — the refuter round paid: corrected Bryant/crimp/brace/caps/junction/gates,
  one-way film, pads, straps, lift scallop, the spokes; the honest matrix.
- `b9bae9c` — the port: ship physics mirrored into vacuum-cell.py + model.js, parity
  178 → 322 values; catalog.js computes SHIP/WALL/GRID live (no literals left).
- `79d367f` — the blueprint's ledger figure goes adaptive + three bars.
- `ae3a95b` — the explorer is the ship: one-mesh pressure-formed wrap (67,959 dimples),
  rings/bars/longerons/fan/X-webs/junction as pipes, spokes as cords, fly-through view,
  the compartments level replaces the band (the last warp is dead), ladder opens at
  Ship 0, six ship rows in check_explorer.
- `ee888f6` — cell/ship.html (the checks page) + tools/check_ship.py in the chain; the
  helium note pays the 0.605 bill it had been dodging (useful fraction 53.0 → 43.7%,
  now honestly BETWEEN the two gas ships).
- pink-sites `217aa85` — the front page tells the pair (−97.3 / +12.5) with the two
  campaigns named; seven-level figure retold (bench cell / the wall / the skeleton);
  robotics.py + estate.py read the gated mirror directly; sign-aware ledger figure with
  the best-world bar. Deployed to production, stamps verified, 401/200 boundaries held.

## The physics decisions a reviewer will want to re-litigate (and where they live)

1. **Bryant with the divisor + head credit** (`L_eff = L + 2R/3`) — general_instability
   in all three mirrors. The free-tube n=2 form under-predicts nothing now; the membrane
   term dies by n=4 and the ring+crimp+foundation system carries the rest.
2. **Crimp**: X-braced ring-plane diagonals, S = 2·E·A·T·cos²θ/(bay·ℓ), cosθ the
   TANGENTIAL leg, q = S/R on the cylinder (the sphere keeps its 2 under the caps).
3. **The spokes**: Winkler ring-on-foundation term k·R/(n²−1), k = E_sp·a_sp/(2R),
   pretension credits both signs. Creep and terminations are [TO VERIFY] and the page
   says so. This is v2 §1's own named fallback, licensed by the reserve pricing high.
4. **γ_GI worlds**: 0.3 house-harsh SIZES the record (with the K_SHELL 0.2 top-up priced
   as the reserve line, on the harsh basis only); 0.65 frame-practice REPORTED beside,
   never sized at. The knockdown test is the biggest single lever on the ship.
5. **One-way film** until a drape analysis licenses the two-way credit (the drawn step
   is smaller than the membrane law's own bulge).
6. **Plan of record kept the ruled 0.5 m squares** — the pitch sweep says the ruling
   costs ~2% against the optimum, which is the right way for a ruling to survive.

## What the operator should re-decide in daylight

- The compartments level draws SHIP-5 doctrine (6 membranes) — policy still open.
- The erection-wind check fails unshored at 15 m/s ground wind (the verdict string says
  "stands SHORED"); a clamp upgrade or an ops constraint is a real choice to make.
- The torsion path is now dedicated straps (sized at margin 1.0, scoping demand model)
  — fins would change the demand entirely.
- k_fan died as a concept (it never bought circumferential bracing); the fan is 2 per
  column per bay and the ring brace pitch is honestly 2.27 m.

## What deliberately did NOT happen tonight

The dashboard and its renders (operator scoped them out); the bench-article levels of
the explorer (they are correct as the bench story); pushing either repo to a remote
(still unpushed, flagged every session); any relaxation of a margin to make a page read
better.


## ROUND TWO — the ordered review sets (added ~06:50)

The operator's two 3× review sets ran after the build (three physics reviewers, three
site reviewers, 67 findings). The physics set killed the night's second verdict too:

- **REV-1 (BLOCKER, both reviewers independently):** a diametral spoke has zero
  first-order stiffness at odd n — ends move (+w, −w), pure translation — and the
  governing mode was n=3. Foundation now credits even n only at the corrected per-end
  E·a/R. **Chordal spoke nets work the odd modes: SHIP-3's named design move.**
- **REV-2 (MAJOR, accepted as the honest bound):** Bryant's membrane term zeroed —
  it requires in-surface (x–θ) shear this wall does not have. An in-surface shear
  system buys it back [TO VERIFY — SHIP-3's second named move].
- **REV-3 (REJECTED, with the textbook):** the proposed crimp-leg swap contradicts
  Timoshenko's laced-column form, the exact X-panel slip stiffness, and both
  degenerate limits. Recorded at the line in ship_scoping.py.

**FINAL VERDICT OF THE NIGHT: harsh basis 0.558 (−178.3 t); best defensible world
0.981 (−4.3 t). Nothing floats at 52 m as drawn.** The gap in the friendliest world is
under two percent, and the model names exactly what closes it: the two test campaigns
(GI knockdown ~two hundred tonnes of verdict; chord coupons) and the two SHIP-3 design
moves (chordal spokes; in-surface shear).

The site set (42 findings) drove: the public concept page stopped teaching
cells-as-current and the floating-cell milestone (plus three 404 archive links fixed);
the blueprint dropped a hand-typed '+' that rendered '+-97.3 t', got the wall's real
populations, and retitled to "the ship is the bet"; the checks page's fabricated 0.68
wind margin became a computed, parity-held windMargin and its verdict words are now
derived, never typed; windowK died (a temperature window only exists on a basis that
floats); explorer meta/title/fallback fixed.

**Deferred to daylight, accepted but not implemented (tonnes-level refinements, none
verdict-moving):** junction diagonals through the compression solver (±5 t-class);
reserve spoke-delta convention (~3 t conservative as-is); cap-loop-before-reserve
ordering (currently dormant — cap margin 2.7, loop never fires); cradle min-flange
(passes 13× regardless); erection-wind peak flow ×2 (shoring bill only); spoke
pretension demand booking (negligible at 4.6 t of spokes). Also still open from round
two's site set: minor link/vocabulary notes recorded in the panel output file.


## MORNING — the band study (operator question, 08-13; regenerate: `python3 tools/ship_scoping.py --band`)

The operator reframed the goal: *stop declaring a safety factor; put the design in the
middle of the band between crush and sink, and let margin be an output of materials and
design.* The tool now computes it: CRUSH = the SF-1.0 ledger (every capacity meets its
demand at nominal pressure), SINK = lift, and the emergent SF of any design is the SF
whose ledger hits its mass. Record pinned first (403.1 t / 0.558 reproduces from
PLAN_CFG before it prints).

**Findings, at the record config (52 m class scales, depth 3):**
- **Sizing up does NOT buy float.** Harsh basis: band negative at every hull 32–112 m
  and DIVERGING (−22 t at 32 m → −3,160 t at 112 m, σ1450). Frame world as drawn:
  a thin window 32–80 m (σ1450, peak +50 t at 80 m; SF_float ≤ 1.17); closed by 96 m.
- **The chordal spoke net is nearly the whole prize of SHIP-3.** At 52 m harsh σ1050
  the crush boundary drops 337.7 → 255.1 t (−83 t, cord priced by the greedy at
  diametral rates); the in-surface shear system adds only ~0.3–5 t on top of it in any
  world (both fight the same low-n modes), and its own hardware is unpriced — likely
  net NEGATIVE once built. Recommendation: chordal net yes, shear system probably no.
- **The harsh world never opens** — even with both moves credited, best −5.8 t at 36 m.
  The knockdown campaign is load-bearing for the concept, not decoration.
- **In the certified world (frame 0.65 + σ1450 + chordal net):** band open at every
  hull 32–112 m; relative width peaks flat across 52–68 m (~21% of lift); mid-band at
  the ruled 52 m = design at ~201 t, float reserve +23 t, emergent SF ≈ 1.17 —
  **the declared 1.2 was a hair conservative of mid-band all along.** Absolute reserve
  (= payload) grows with hull: +77 t at 80 m, +106 t at 96 m at the same relative
  margin. SF_float peaks 1.39 at 60 m.
- **The sweep now prefers depth 4 m** (spokes even-n-only made the sandwich want
  depth): 383.0 t vs the record's 403.1 at the ruled squares — a ~20 t re-rule
  candidate for daylight, alongside the chordal net.
- σ axis (1050→1450) is worth ~7–12% of crush mass; the knockdown axis (0.3+reserve →
  0.65) is worth ~26–35%. In-house manufacturing quality pays mostly through the
  KNOCKDOWN tests it justifies, secondly through coupons hitting the datasheet ceiling.
- Fittings are not the story: clamps 2.2 t + pads 2.0 + straps 0.3 + skins 1.0 of
  403.1. The stability system (~190 t incl. reserve 81.3) and tiJoints (46.5, the eta
  axis) are. eta 0.85→0.90 (in-house joints) ≈ 17 t.

BOUND_CHORDAL / BOUND_MEMBRANE flags exist for the study only — both False in every
gated run; the gi loop is FP-identical with flags off (record pin proves it).


## MORNING, PART 2 — the two walls land on the site (operator ruling: report them everywhere)

The operator ruled the crush/float boundaries THE project-defining numbers and asked
for a figure AND an interactive calculator. Landed, all gated:

- **`ship_band()` + `ship_neutral_ceiling_m()` in BOTH mirrors** (vacuum-cell.py +
  model.js), summary block `ship0.band` = three as-drawn worlds (harsh mid, frame mid,
  frame 1450) × {crushT, liftSLT, lift2500T, bandSLT, band2500T, sfFloat, neutralCeilM}.
  **Parity 324 → 345.** The gi() in both mirrors gained default-off `gi_chordal` /
  `gi_membrane` flags (the SHIP-3 moves as bounds; FP-identical off — the record
  reproduced before anything printed).
- **cell/ship.html: "The two walls — crush and sink"** — prose, an SVG walls figure
  (crush red / sink pink / 2,500 m dashed blue, band shaded), the three-world table
  with SF_float and neutral ceilings. check_ship extended (band rows, fig marks,
  band25 binding, crush cell vs model).
- **cell/band.html — the calculator** (auth area): hull 32–112 m, neutrality altitude
  0–3,000 m, world, coupons, the two moves as loudly-labelled BOUND toggles, design
  point chosen by EMERGENT SF, payload slider. Live outputs: both walls, band,
  SF_float, structure, payload at altitude, neutral ceilings empty/loaded, plus the
  walls-by-hull chart with the design dot. Every number solved live by model.js.
  **New gate `tools/check_band.py` (`make bandcheck`, in `make check`):** boots the
  page, has window.BAND solve five tuples (record crush, frame ceiling, off-record
  80 m, declared record, bound view) and diffs them against the Python mirror at
  1e-9 relative — 23 values — plus DOM-rendered assertions.
- **Front page (public):** the walls paragraph — crushharsh/crushbest/sinkwall tokens
  (338 / 202 / 225 t) injected by robotics.py from the mirror's band block.
- **The altitude ladder is now first-class**: lift falls ~9%/1,000 m; the calculator
  and the checks page both carry it. Verified for the operator's 112 m scenario:
  mid-band structure 2,130.7 t + 100 t water + 19 t equipment = neutral at sea level
  to 0.2 t (his arithmetic exact); loaded-neutral ceiling ~sea level by construction;
  empty-at-crush ceilings 0 m (harsh) / 362 m (frame mid) / 1,075 m (frame 1450);
  at 2,500 m the certified-bound band closes at every hull.


## MORNING, PART 3 — The Ship level, and the exterior doctrine (operator round, 08-13)

Operator's orders after seeing the band live, all landed:

- **'Ship 0' is now 'The Hull' and THE SHIP sits above it** — level 8, the new default
  open. One rule drawn everywhere: **NOTHING CUTS THE WALL.** There is no interior to
  put gear in (the inside is the product), so every system is exterior: thrust pods on
  pylons LONGER THAN THEIR OWN ROTOR RADIUS (the fleet dashboard's law, imported — its
  old hull-piercing mounts are what this retires), circumferential straps + twin keel
  rails as the only wall interface, tanks/pumps/winch on a raft SUSPENDED under the
  keel from a wide bridle, the bucket on a drop line. Equipment named-not-weighed
  [SCOPING]; views: whole/flank/keel/module/drop; switches: hull/pods/module/lines.
- **Suspended vs belly-mounted, answered on the panel:** a hard-mounted gondola feeds
  thrust + slosh moments into film-on-rings as local bending the 4 mm wall has no line
  for; a wide bridle arrives near-tangential and spreads pulls along straps riding many
  rings in bearing. The hull's size makes the bridle wide and the swing angle small;
  the price is a pendulum in the control loop — ops owns it. [SCOPING], both readings.
- **Clamp render bug — operator caught it, and the model check mattered:** the drawn
  stagger walked TWO bars per ring, so every odd bar had no clamp anywhere. The model's
  erection-wind check prices each clamp at a barPitch × 4-ring tributary — which only
  exists if every bar is clamped at that spacing. The physics model was CONSISTENT
  (count = 1-in-4 and tributary both assume the true brick); only the drawing lied.
  Now a one-bar walk: every bar, every fourth ring.
- **Webs land on hoops now:** bay midpoints/junction stations are not multiples of the
  drawn ring pitch, so fan/theta/junction outer ends floated between rings. snapOuter()
  puts every outer attachment on a ring station, matching the grid level's own law.
- **The grid level is bare** — the per-panel film pillows (the old cell look) are gone;
  film is the subject on the wall level and the wrap above.
- **MISSION 0 SPEC RECORDED**: the spec ship = this architecture at 112 m — 100 t
  water + 19 t equipment, neutral at sea level in the certified world (mid-band
  structure 2,130.7 t; the operator's own arithmetic, verified to 0.2 t). It is what
  the numbers get quoted against; the 52 m plan of record is what gets BUILT first and
  models are NOT resized. Chip on the vessel panel; the band calculator explores it.


## MORNING, PART 4 — flight controls (operator: "game style I think")

Every level now carries a free camera: arrows/WASD move, Q/E and PgUp/PgDn rise
and sink, SHIFT boosts, the mouse drags the nose around, the wheel sets speed,
ESC exits, and a D-pad + toggle sits bottom-left above the cutaway (same
controls for a thumb). `?fly=1` deep-links straight into flight. Speed rides
`cam.radius`, so it flies sensibly at the 5 cm connector AND the 60 m ship.

The implementation is one honest trick: the free camera is REALIZED THROUGH THE
ORBIT RIG — az = yaw + pi, el = -pitch, target = pos + dir·L, distance = L
(maxDistance raised first; the documented clamp trap) — so projection, near/far,
styles and screenshots all see an ordinary orbit pose and no second code path
exists. flightStep() integrates inside advance(), which is the SAME path
api.tick() drives, so the gate flies it for real: check_explorer now holds
90 ticks of forward to a finite camera that actually moved and exits clean.
Dives and eased views end the flight; the flight ends tours and the fly-path.

TRAP PAID: a `function syncFly()` declared inside the boot's else-block does
not hoist to module scope, and the opts.onFlight callback threw ReferenceError
only when the first flight engaged — a `let syncFly = () => {}` indirection at
module scope is the pattern (the gate caught it before any human did).


## MORNING, PART 5 — grid truth + the stick sorted (operator round 2)

- **X-webs at EVERY bay plane** on the grid level (two lit planes had read as "some
  hoops have them, some don't" — the model has the crossed pair at every inner ring).
- **A connector at every landing**: instanced beads at web ends, X ends, and the X
  crossing itself, deduped on shared landings. New label says the honest thing: joints
  are priced SMEARED (the η line, 15% of member mass), the beads are where fittings
  live, and getting the count down is named daylight work (the η axis ≈ 17 t at ship
  scale).
- **Edge bars gone**: the patch draws interior bar columns only — the half-hanging
  edge bar with full clamps was an artefact of where the patch ends.
- **Spokes from every inner hoop** (one pair per bay drawn; the ship level carries the
  full diametral set). Operator likes the cords — keep the treatment.
- **Arrows belong to the flight now**: the html's ArrowUp/Down level-dive and
  ArrowLeft/Right tour-walk bindings fought the free camera for the stick — removed
  (levels: scroll-dive/ladder/links; tours: their own buttons). **Shift+Up/Down flies
  altitude** (operator ask); shift with anything else stays the boost; keyup clears
  both names of a shift-mapped arrow.
- **Flight feel (operator tune):** the old normal speed (0.55 radii/s) is now what
  SHIFT buys; normal is a 4x-slower walk. The mouse look is DAMPED: drags write a
  target at half sensitivity and flightStep glides the nose onto it with a ~120 ms
  first-order lag (the glide keeps frames rendering after the pointer stops).


## MORNING, PART 6 — the fine levels earn their views (operator round 3)

- **The net unfolds SKY-SIDE UP now**: netPose turns the whole net half a page about
  the root face's own in-plane axis as it opens (pi x u) — a rigid motion, so the
  offline guarantees (planarity, areas, zero overlaps) ride along and u = 0 is still
  exactly the cell. The flat used to land inside-up: the dark face of a film whose
  whole point is its bright outer surface.
- **Tube + skin walks move the HIGHLIGHT, not the vantage**: every cut/face stop parks
  at the cell's own whole-article framing; the lit group and its labels travel. The
  connector walk keeps per-joint vantages — and the STRUT LEVEL NOW HIDES THE SKIN
  outright (a solid shell around a camera parked inside it is a wall, not a reading;
  the skin button keeps its state for every other level).
- **Views belong to their level**: rebuildViews existed but was called once at boot —
  the ship's views sat on the tube level influencing nothing (operator caught it).
  Now rebuilt on every level change via a module-scope let (same TDZ pattern syncFly
  needed), and strut/wall/track carry their own poses (centre joint / whole article /
  above / level-with-it).
- **The gate followed the ruling both ways**: wall/track stops must NOT move the
  camera (highlight-only walk, dim/subject asserted), strut stops MUST. And the
  connector print-swap arithmetic now measures against the SKINLESS baseline — with
  skinTris measured by driving the real skin button by READ-BACK (counted clicks
  assumed 'solid' when the default was glass, and measured zero).


## MORNING, PART 7 — the vessel kit, compartments retired, cards retired

- **Grid joints true**: X-crossing beads at the world centroid of the four corners (the
  diagonals are SKEW on a curved wall; the parametric midpoint missed — operator catch);
  end beads pulled onto the hoop SURFACES (outer in by the ring radius, inner out by the
  inner hoop's) instead of being swallowed at centrelines.
- **THE COMPARTMENTS LEVEL IS RETIRED** (operator + agreement): it drew ONE membrane
  arrangement while SHIP-5 is an open policy, and the drawn slabs escaped the hull. The
  doctrine paragraph lives on the hull panel ("membranes so a holed wall floods a room,
  not the ship — ~10 t of air a minute through a cell-sized hole"); membranes stay
  priced as skins; the level returns when the policy is decided. Ladder is 7 levels.
- **The vessel kit grew the working end**: pump + anchor-winch BOX on the drop line
  above the bucket (lowered to the water as one unit; the anchor line runs on past the
  bucket to the anchor weight). TANKS resized to the water: three 34.8 m3 barrels =
  104 m3 — the Mission-0 100 t split with trim margin (the old draw was ~380 m3).
  SOLAR band on the hull's top sector (70 plates, placement only — energy budget lives
  in the fleet model). ROTORS GIMBALLED mid-duty: pods moved lower on the widest band
  (downthrust line near the CG; fore-aft spread for pitch/roll authority) and every
  disc pointed down-and-forward — the water cycle's posture. Cruise is the cheap duty;
  holddown is the expensive one; lifting heavy is the same bill upward, rare by doctrine.
- **FLOATING CARDS RETIRED on every level**: placeLabels() unmounts and never rebuilds;
  every reading they carried was folded into the side panels (rotor duties, working
  end, connector-at-every-landing with the eta pricing, skin-hidden-here on strut,
  open-policy compartments on the hull).
- **TRAP RE-PAID: the missing-id audit.** Removing the reseal button orphaned its
  addEventListener and the null killed the wiring module — the tour button died and
  the gate said 'the camera did not move'. The audit (ids wired vs ids present) found
  it in one line. HANDOFF already warned about exactly this.
- Stray processes: two idle serve.py killed; no headless Chromium; the mouse stutter
  suspect is localsearch-3 (GNOME indexer) chewing the night's file churn + openrgb.


## MORNING, PART 8 — collars true, walks curated, the deck is toggles

- **The X beads sit ON the crossings now** (operator round 5: "slightly above, in the
  well of the top V" — exactly diagnostic): a ring-plane panel is an isosceles
  TRAPEZOID, and trapezoid diagonals cross at the radius-weighted point
  r_outer/(r_outer + r_inner) along each diagonal (nearer the inner chord), not at the
  corner centroid the previous fix used. Landing beads became COLLARS: centred on the
  pipe centrelines with radii a little over each pipe family's own (outer hoops 0.105,
  inner 0.078, X mid-span 0.062) — visible on the big rings and the small ones, and at
  the four-legs-to-one landings.
- **The walks are curated** (operator, mid-round): tubes and connectors KEEP their
  walks — they are the good ones — with the cut chips renamed by LENGTH ('206 mm
  spoke', '134 mm tie': the identity on a saw table; nine chips no longer read
  octet/octet/octet). The SKIN's walk is retired (its stops stopped moving the camera
  under the wide-frame rule, so it was a list the panel already carries — all four
  face readings now show at once there). The '…' stepper is gone everywhere: the chip
  row IS the walk, and the gate now drives the chips, not the stepper.
- **The deck is toggle panels**: layer switches wear square checks, views and walk
  chips wear radio dots, the lit view is a bookmark of the last pose flown to.
- Operator dropped the disk-I/O + 6.32 TB download investigation from this session —
  another agent takes it. (First look before the drop: no headless browsers, two idle
  serve.py strays killed; localsearch-3 indexer + openrgb were the CPU load.)


## MORNING, PART 9 — the deck is rebuilt: fixed grid, nothing reflows

Operator round 6, the UI-quality verdict ("good, not just a trigger of functionality"):

- **NOTHING EVER RESIZES.** The reflow bug was state-in-label buttons ('skin: solid' →
  'skin: transparent', '✈ fly' → '✈ flying'): the button grew, the row reflowed, and a
  double-click hit a different control. Labels are CONSTANT now; state is indicators —
  square check = independent layer switch, radio dot = one-of-many (views, walk stops,
  two-states like pump-down/unfold/fly), SEGMENTS = modes (skin [solid|glass|off],
  parts [all|joinery|pipes], via new api setSkinMode/setPartsMode beside the cyclers).
- **ONE geometry**: every chip a uniform 26 px cell in a fixed two-column grid,
  ellipsized, same radius, same font. The views row had been UA-DEFAULT buttons since
  birth — the 'different shapes' the operator saw was three style families in one deck.
  One base rule covers .gbtn/.sbtn/.vbtn/.dot2 now; retired ids are out of every
  selector list (a stale display:none list would have eaten the unfold toggle).
- **The [hidden] trap, paid a THIRD time**: .segrow had display:grid, the data-lv sweep
  sets el.hidden, and author display beats the hidden attribute — the parts segment
  showed on every level until .segrow[hidden]{display:none} joined the two existing
  guards. The trap is now in three places in this file; it is the pattern.
- **Gate follows**: parts probe clicks segments (joinery→pipes→all, same visit order the
  cycle used), the skin read-back drives the segment, 'parts: all' label assertion
  became active-segment read-back, the pump's label assertion became a lit-dot check.


## MORNING, PART 10 — one tank, its ballast pair, and the rotor decision recorded

- **ONE water tank** (pi x 1.8^2 x 10.5 = 107 m3 — Mission-0 100 t with trim margin),
  flanked fore and aft by **two N2 ballast tanks** in cool glass (the air-admission
  ballast the descent doctrine prices). The raft frame is resized to hug the cluster
  (19.5 x 6.0 x 4.4 — was 22 x 13 x 3.2 around barrels it dwarfed). The raft's gear
  beads are gone: the pumps and the winch live in the drop-line box, which sits
  directly above the bucket as the operator specified.
- **ROTOR PLACEMENT: DECIDED [SCOPING], and the panel says why** — low on the widest
  band: the downthrust washes clear past the hull's curve instead of fountaining
  against the belly (a keel mount fights its own suckdown and the bridle), the
  fore-aft spread buys pitch/roll authority, symmetric pairs cancel their own moments,
  and the gimbal gives cruise for free. Real disc sizing belongs to the fleet-model
  power work (#88's neighbourhood).


## MORNING, PART 11 — the ALLOW_DIRTY exception burned, and the rule is absolute again

Round 7's deploy: the tanks round committed clean, but a co-agent's front-page rework
(shared/ridge.js + pinkrobotics/index.html + tools/inline_design.py) had grown INTO the
pinkrobotics rsync scope between rounds, and an ALLOW_DIRTY=1 run — justified an hour
earlier when the only foreign file sat OUTSIDE the scope — shipped their half-done
index.html to production. Caught in the same command's status echo; restored inside ~2
minutes by single-file rsync of the committed index.html straight to the edge docroot +
purge; their working files untouched throughout. The airships tree shipped that round
was fully committed, so the front page was the only casualty.

THE LESSON, PERMANENT: scope reasoning does not survive a live co-agent. Never
ALLOW_DIRTY. A deploy against a dirty tree ships the COMMITTED state from a clean
worktree (`git worktree add <tmp> HEAD`; deploy from there; remove), or waits.


## MORNING, PART 12 — the world arrives: full solar, split cables, environment, tours

- **SOLAR IS THE WHOLE TOP HALF** (operator: "as much power as we can get"): 22 x 13
  dense plate tiling with visible seams — it reads as an array, not grey paint. Straps
  ride over it; energy budget stays with the fleet model.
- **THE WORKING END SPLIT**: pump and bucket on SEPARATE cables from the winch box
  (independent operation — the pump holds station at the surface while the bucket
  cycles); the pump unit is drawn on its own line; the anchor line is the third.
- **THE ENVIRONMENT (opt-in 'env' layer)** answers "how big is it" the honest way:
  tethered over a field at the lake's edge (four tethers to anchor beads), bucket in
  the water, 1.8 m people at the anchors/hangar/shore, the hangar with trees and
  vehicles beyond, ground grid + lake glass. Stylized minimal; the fly camera makes
  the scale legible. The bow's 1.8 m scale tick stays as the always-on reference.
- **TOURS, a real system**: LEVEL_TOURS registry; PATH tours ride the fly-through's
  leg chaining (generalized off the hull level — any level flies now) and WALK tours
  drive the stop chips on a 2.6 s dwell through the existing machinery. Every level
  has a grand tour; vessel adds 'the working end' + 'over the solar field', hull adds
  'the stability circuit'. Deck: TOURS group above views; chips lit while running;
  onTourEnd (finish or any-input cancel via cancelGuidance()) clears them. Gate drives
  one path tour (camera must move through legs) + one walk tour (dwell must advance)
  + the env layer (must add >500 triangles).
- Boot-order trap (4th of its family): rebuildTours needed the module-scope let AND
  the explicit boot call beside rebuildViews' — onLevelChange fires before assignment.


## MORNING, PART 13 — camera manners, the dip, and the two-deck working end

- **The furious spin is dead**: the idle turntable winds cam.azimuth without bound and
  every transition lerped through the accumulated turns. nearAz() wraps the delta to
  the shortest path at EVERY eased builder (dive, stop, view, both leg sites). Tours
  now END POLITELY: restoreLevelPose() eases back to the level's own framing and the
  turntable holds for ~12 s (spinHold) before resuming.
- **The stale cell-era wall chip is gone** (Bambu PAHT-CF / level-2 path readout —
  #wallchip + fillChip removed; nothing gated it).
- **ENVIRONMENT v2 — the dip**: hangar, vehicles and tethers removed; the ship WORKS
  now — over a wide lake disc (a real disc; the first cut lathed a 256 m needle),
  trees ranked at the shore, PEOPLE v2 (shouldered body + separate head, 1.8 m) at
  the water's edge. Fly down and stand with them.
- **THE TWO-DECK WORKING END (doctrine)**: tanks upper deck (water amidships, N2 pair
  ON THE FLOOR of the raft); equipment lower deck — a LONGER SEE-THROUGH equipment
  bay (glass, 8.2 m) with the battery box along its ceiling, the N2 cryo unit low,
  and THREE PULLEYS on its keel: pump (100 m pipe spec, into the water), BUCKET
  CENTRED with ~0.95 m clearance to each neighbouring line, SPRAYER opposite the
  pump — separate cables, independent operation. Anchor line from the bay's stern.
  Bucket volume check: pi x 2.05^2 x ~2.9 ≈ 30 m3-class per dip — three-to-four dips
  per 100 t fill, plausible for the cycle.


## MORNING, PART 14 — the envelope goes public; the hero lands; compaction point

- **Figure 2 on pinkrobotics.ca is the LIVE DESIGN ENVELOPE**: one draggable dot in
  (hull diameter, weight/lift) space — float line flat at 1.0, the crush curve (SF-1.0
  ledger over lift, frame-practice + ceiling coupons, campaigns named on the caption)
  pinching the envelope shut near 90 m. Readouts beside the dot: all-up, lift, verdict
  (FLIES / SINKS / CRUSHES), margin ~SF (interpolated between the SF-1.0 and SF-1.5
  curves, '~' honest), headroom to neutral. Generated by fig_envelope() in
  tools/robotics.py (data from the gated mirror; the page script only interpolates);
  injected at the <!--ENVELOPE--> marker; old ledger figure renumbered Figure 3.
  Default dot = 52 m mid-band (the first default sat 0.0008 below the crush ratio and
  opened on CRUSHES — checked by DOM probe before shipping).
- **The hero agent's banner is landed and live** (its own commits: ridge.js +
  airship.js inlined by inline_design.py — Ship 0 drawn small crossing ridge country,
  proportions read off OUR gated model). My last worktree deploy had already shipped
  it; the round-9 'mid-deploy' completion was verifying + the envelope deploy.
- Round 9 (airships@6547a26) deployed same round: spin manners (nearAz everywhere,
  restoreLevelPose + spinHold), wall chip retired, environment v2 dip scene, two-deck
  working end, solar to the ends.
- COMPACTION POINT: this doc (14 parts) + memory airships-oss-repo.md are the resume
  state. Open: #85 SHIP-3 chordal net (+depth-4 re-rule, band-basis ruling), #88
  fleet-monitor exterior doctrine, older queue. BOTH REPOS UNPUSHED (pink-sites 158+
  commits ahead).

## Part 15 — envelope round 4: the lens, the ship schematic, phones (afternoon 08-13)

- **Floor to 0.8 revealed the whole truth: THE ENVELOPE IS A CLOSED LENS.** crush/lift
  at s1450+frame-gi: 1.073 @24 m (square-cube starves the small hull), min 0.901
  @52–60 m, back through 1.000 @96 m, 1.135 @120 m. Both closures now visible; the old
  "pinches shut near 90 m" docstring was half the story (it opens near 28 m too). The
  green fill now clamps at the float line (path of min(crushR,1.0)) — before this a
  wrong-green wedge lurked under the top-red band wherever crush > 1.
- Operator wording round: envelope claim on two lines; CRUSHES + explanation on two
  lines (bottom-right); float-line label centered above the lens (dOpen/dClose scanned
  in JS, label at xs((dOpen+dClose)/2)); ENVELOPE block centered on the same dMid.
- **Live hull schematic** in the readout column: capsule at TRUE relative scale
  (24 m IS a fifth of 120 m — no floor, no lie), cap-seam lines, bracketed
  length/width, surface + volume. Geometry computed in-page from ONE model constant
  (F = SHIP0.fineness = 2.0, emitted by fig_envelope) with ship_geom's own formulas —
  cyl = F·d − d, capsule area/volume; verified equal to mirror output (16,990 m² /
  184,055 m³ @52 m). Page still computes no physics.
- **Mobile**: min-width:660px removed (that forced the sideways-scroll trap);
  layout() swaps viewBox 880×430 ↔ 620×700 at container <640 px and re-transforms
  #envread (below plot) + #envhull (beside readout); .narrow class bumps text 11→14,
  big 13→17. Touch: svg root is touch-action:pan-y, ONE transparent #envcatch rect
  over the plot alone is touch-action:none and owns all pointer handlers — page
  scrolls past the figure, plot still drags/taps. drag() reads the live viewBox.
- **DOM-check technique on this box (no node): snap chromium headless.**
  `chromium --headless=new --virtual-time-budget=4000 --dump-dom <file|url>` executes
  the scripts and serializes generated children — grep for live values (length 104 m,
  surface 16,990). Screenshots via --screenshot --window-size=390,844 for narrow.
  Checked LOCALLY before commit and ON PRODUCTION after purge, both widths: 77
  children, hull values live, narrow stacks (read at translate(24,438)).
- pink-sites@f7146c1 "The envelope closes at both ends — and shows you the ship";
  deployed from clean worktree, CF purged, live-verified. Hero agent's beacon commit
  (4350cd5) rode along, already committed by them. data/live/* churn left untouched.

## Part 16 — vessel round: honest solar, the pump on its pipe, a mind aboard (late afternoon 08-13)

- **Solar diamonds diagnosed and retired**: filmDomeGeom(…, seg=4) is a lathe, and a
  4-seg lathe puts its VERTICES at revolve angles 0/90/180/270 — in the plate basis
  those are the hoop and axial axes, so every plate rendered as a diamond and its
  ±2.16 m corners lapped the 2.17 m barrel rows. Now: boxGeom(1,1,1) with
  PER-INSTANCE basis scaling (thop·4.2, tm·axLen, n·0.1) — barrel axLen 2.06 under
  its 2.167 pitch, cap rows 4.0 under 4.19 — seams show, nothing overlaps, and each
  plate stands proud by its own hoop sagitta (off = 0.18 + sag + 0.08 on caps) so a
  flat panel's corners never dip into the film at small cap radii.
- **Working end, operator's re-read**: the flared cone (old sprayer lathe) read as
  "weirdness" — GONE. Sprayer = the white upright cylinder (old pump's profile) on
  its own cable at −3.3, raised to the sprayer height (above water when env on).
  PUMP = blue-grey HORIZONTAL unit ('#5b8fc4', lathe along x, vert2 false like the
  water tank) at +3.2, z −5.4, hanging off the END of a rigid VesselPumpPipe from
  the winch keel — the pipe is reach spec and suspension in one; its old cable
  removed. Anchor line at +4.0 clears the pump body (ends x 3.8).
- **Lower deck**: cryo box was overhanging its winch sheave (boxGeom l=1.9 → span
  to −3.55 vs pulley at −3.3) → moved inboard to −2.0. NEW VesselShipMind at +2.0:
  the compute core in pink glass (TOKENS.warm, 0.3) — panel names it. N2 tanks
  raised to nzFloor = mz1+1.4 so both bellies sit on the water tank's datum
  (mz1+0.4). New vessel view 'the water gear' (tg −R·2.3, d 20) frames the trio.
- **Figures**: Figure 1 inputs panel now bills "≈68 km pipe · 46.5 t Ti" +
  "≈16,990 m² film" — the titanium is the ledger's OWN tiJoints row at the declared
  world (finished mass, never sinter feed; caption carries the basis; the ring
  count was a wall fact and panel 3 keeps it). load_ship exposes ti_finished_t.
  Figure 2's TOO HEAVY sits top-right on two lines — centred, it captioned Ship 0.
- **Chain discipline paid again**: first make check FAILED on stampcheck (explorer
  edits, no restamp) — make stamp (?v=c631abe1) then green end-to-end incl. the
  25-interaction sweep. Also: chaining pkill in a compound Bash = exit 144 again.
- airships@33ccf24 (51 files: 2 real + 48 stamps + view), pink-sites@b4286bb
  (38 published + robotics.py + index.html). Worktree deploy, CF purged, live
  verified: front page shows 46.5 t Ti / finished mass / TOO HEAVY two-liner;
  served explorer.js?v=c631abe1 carries water-gear/ShipMind/PumpPipe markers.

## Part 17 — the dashboard arc opens: env polish shipped, THE CAPSULE LANDS IN THE MONITOR (evening 08-13)

- **Env round (airships@467867c, deployed)**: lake 118→90 m core, edge FADES over three
  stepped-opacity washers (VesselEnvLakeF1-3 — shader discards per-instance alpha, so the
  fade is stepped glass materials) onto a VesselEnvShore beach annulus (94-132 m); trees
  (angle,radius on 112-127) and people (waterline knots at 97-101) all stand ON SAND —
  the old coords put them in the water. Env toggle eases the camera OUT (≥330 m, never
  in) via a view-kind transition in api.shipLayer; reduced-motion jumps. Solar cap rows
  start AT the barrel joint (f = 0.9(i+.5)/10, plate 3.6) — shoulder fully decked after
  the operator's "fill the curve/center transition".
- **DASHBOARD STAGE 1 = THE CAPSULE FAMILY (airships@a32809f, 96 files, deployed)**:
  3d/model/config.js profileR/sectionScale/HULL_DEFAULT rewritten — spherical-cap rise
  over capFrac 0.25, cylinder, mirror; pure revolve (topFlat 0). Classes re-solved at
  UNCHANGED displacement: P100 110×55, P1000 238×119, P10000 512×256 (lengths chosen so
  the solved radius ≈ L/4 → true hemispheres). sim/config.js adopts the same dims
  (spec-parity forced it — the gate works). Rotor stations LOW on radial pylons
  (LOW 0.42); network class staggers ±0.34 into two rows (seven 85 m discs no longer fit
  one line on a 512 m flank); both overlap tests (model.test.mjs + browser.html — TWO
  copies!) now use 3D centre distance. Fineness plausibility floor 2→1.9 (design point
  IS 2.0; Simpson lands 1.99).
- **THE HONEST DRAG BILL, in the open**: frontal area ×(55/47)² = 1.37 → P-100 drag
  1.06→1.46 MW, cycle 1.253→1.391 MWh (+11%), kWh/t 12.53→13.91, battery 10.4→9.2 h;
  P-10000 example cycle 45.87→54.33 MWh; anchor saving re-measures 29%→27%
  (no-anchor baseline 1.912 via js_eval probe). Golden regenerated + DIFF READ (only
  dims + drag-descended values moved); figures.json refreshed; 71 tagged citations
  rewritten by `tools/check_figures.py --fix` (IT EXISTS — the project pre-paid this);
  8 untagged 190 m/876 m prose mentions fixed by hand (Hindenburg claims survive —
  110 < 245 more than ever). Pinned observation tests re-pinned from recomputed values.
- **THE GATE CASCADE a dims change walks (order observed)**: browser suite → spec-parity
  (sim vs 3d dims) → golden (tests/golden/check.py --update, READ THE DIFF) → figfresh
  (make factsheet) → figcheck (--fix + hand-fix untagged prose) → fallbackcheck
  (tools/gen_fallback.py) → node-tests-in-browser (validateClass fineness band) →
  stampcheck at every step. CHAIN15 EXIT=0, 25 interactions green.
- **Traps**: js_eval scripts are EXPRESSIONS — async IIFE `(async()=>{...})()`, no top-
  level return; snap chromium drops `fallback-*` junk dirs in CWD (publish's manifest
  gate catches them — delete, never classify); background `(cmd) &` inside a Bash tool
  call dies with the call — use run_in_background or survive-by-file sentinel; make
  from wrong CWD = "No rule to make target".
- **REMAINING for the dashboard arc (#96/#97/#98)**: exterior working end on the
  monitor model (layout.js internal tanks → raft + bay + three lines, retire tail
  surfaces + recessed medium thrusters, solar decking on the top half — 'every layout
  item sits inside the hull' test flips by design); bind mission phaseShape to
  bucket/pump/sprayer line lengths + raft tank fills; rotor spin verify; WASH particle
  direction-vs-speed bug (Tyler: reproduce first, reimplement minimal if it persists —
  do NOT debug the old one twice); front-page spinning 3D hero (The Ship view, no
  person tick; co-agent owns hero regions — new module, check git log first). Another
  co-agent surfaced in pink-sites (tylerdwyer theme, 197cf41) — same interleave rules.

## Part 18 — the wash ruling: rotors to the horizontal plane, the avatar becomes the capsule

- **OPERATOR REVERSED the low-flank rotor call (same day)** — my advice read the wash
  direction backwards: holddown (the hard duty) THROWS AIR UP, so a low pod fires its
  hardest wash into the belly above it; the ships thrust both directions. NEW RULING:
  pods on THE HORIZONTAL PLANE (beam of the widest band), discs as far from
  wall/straps/lines as the pylons hold them; the P-10000's network in TWO BANKS at
  ±45° from the horizon, alternating stations, so neither bank sits in the other's
  column (and fourteen 85 m discs get room a single row cannot give).
- Applied in ONE round to all three surfaces: 3d/model/layout.js (drop = ±π/4 network,
  0 elsewhere), cell/explorer.js vessel pods (th = 0/π) + panel doctrine paragraph
  (supersession NAMED in the prose), and app/cockpit/shipviz.js — the 2D avatar
  rebuilt as the CAPSULE (capR profile, B = 0.5, x-station rings) with TAIL FINS
  DELETED and per-class rotor specs matching the 3D layout (P10000 banks in the
  schematic too, z0 threaded through disc/pylon/tilt/arrows).
- airships@ccec7d9, published, worktree-deployed, purged, live-verified (avatar
  markers ×7, layout ×2, explorer ×1 on the stamped ?v=4a4cf3a2 files). CHAIN16
  EXIT=0. Third co-agent commit interleaved in pink-sites (tylerdwyer 42f9c9f) —
  worktree deploys keep being the right call.
- Memory corrected at the source: airships-vehicle-architecture now carries the
  reversal (the old DECIDED-low text was the trap for any future session).

## Part 19 — round in flight: tiers/colors/badges/thrusters SHIPPED; raft/void/solar/single-source NEXT

DONE in this slice (chain pending):
- P-10000 REVISED AGAIN (operator): no banks — ALL stations on the horizontal line;
  4 per side at normal reach + 3 interleaved on EXTRA-LONG pylons (pylon += rr*1.5)
  standing wider; radius separates discs, never height. layout.js + shipviz spec
  (tiers flag, widen = r*3 unit) + explorer.html panel sentence all updated.
- LINE COLOUR CODE (explorer vessel): PINK carries WEIGHT (bridle/drop/bucket/anchor),
  BLUE carries WATER — new VesselLinesWater node (sprayer feed, '#5b8fc4'), pump pipe
  re-materialed blue; the grey upright (read as a second pump) REMOVED — VesselSprayer
  is now a modest blue nozzle head at the line end (lathe [[-0.5,.10],[-0.15,.24],
  [.2,.3],[.42,.06]] at bucketZ+0.1). Panel names the code.
- "Currently Impossible" badges: worked.js class kicker (red span, P1000+P10000) +
  shipviz footer suffix. RATIONALE for prose elsewhere: the crush envelope closes
  near 96 m dia — 119 m and 256 m hulls are OUTSIDE the lens (Figure 2 shows it).
- ALL THRUSTERS RETIRED: CLASS_SPECS mediumThrusters/localTrimFans = 0 for all three
  (arrays empty; build+actuators no-op on empty); dead 'Thruster 0' failure chip
  removed from model-lab/index.html:282.

NEXT SLICE (not started — the heavy build.js work), design settled:
1. RAFT UNDERCARRIAGE (D): post-pass at END of buildLayout (before return): move
   waterTanks/ln2Tanks/generators/batteries/compute/cryoModules(+Trains)/pumpPods/
   hoseReels/anchorWinch positions onto a two-deck raft below keel (keelZ=-R, DROP=
   R*0.34, upper deck tanks in rows, lower deck boxes); store layout.raft={W,L,decks,
   corners}; EMPTY waterManifolds/waterPipes/ln2Pipes/dropOutlets (interior routes).
   build.js: NEW RaftFrame (thin bars, reuse cylGeom like PrimaryRotorPylon_ at
   build.js~856 pattern) + BridleLines (8 pendants, material 'cable' like AnchorCable
   ~702) hull→corners + drop line. Tanks/boxes/fills follow layout.p AUTOMATICALLY
   (instanceNode maps over layout arrays). TESTS: model.test 'every layout item sits
   inside the hull' → for moved groups assert OUTSIDE hull && p[2] < -R*0.95.
2. VACUUM VOID (E): views.js:124 VacuumFillBalls pattern → new 'VacuumVoid' node
   (inset hull solid ~0.97 scale, near-black material, shown ONLY mode==='vacuum');
   balls retired from the vacuum view ("not small cells"). Balls builder at
   build.js~1171-1253.
3. SOLAR DECKING (C): replace SolarSkin single mesh (build.js~516, geom solarG) with
   instanced thin boxes over the top half like explorer plate() — barrel rows pitch
   from cylL, cap rows to the pole guard r>~R/3, HOOP arc pitch const, plates sized
   under pitch, proud + hoop sagitta. Keep id 'SolarSkin' + category 'power' so
   metadata/energy wiring holds.
4. SINGLE-SOURCE STEP (F, operator direction "one model as ground truth"): shipviz
   derives hull profile + rotor stations from resolveClass()+buildLayout() (unit
   scale 2/lenM) instead of its local capR + spec tables; longer term the explorer
   vessel and airship3d should share one vessel-geometry module — record as the
   architectural goal in HANDOFF.
5. Then: badges 'mention elsewhere' candidate = model-lab header line + maybe
   /airships page prose; wash particles (#97) reproduce-first; hero (#98).
SHIPPED: airships@f4502ec + pink-sites@38ed2ec, CHAIN19 EXIT=0 (suite pin 103->101 for
the folded blower tests), deployed from clean worktree, purged, live-verified (layout
tiers x2, explorer colour code x3, badges in served worked.js + shipviz.js). The next
slice (raft undercarriage / vacuum void / solar decking / single-source shipviz) is
fully designed above — start THERE.

## Part 20 — THE UNDERCARRIAGE SHIPPED (airships@0cd91a1 + pink-sites@98c29f6, CHAIN26 EXIT=0)

- Layout post-pass (end of buildLayout): water/LN2/generators/batteries/cryo(-intakes)/
  mind/pumps/reels → TWO-DECK RAFT below keel (deckZ = −R − 0.34R − wR; boxes lower);
  winch at stern; manifolds/pipes/dropOutlets EMPTIED; layout.raft{xHalf,yHalf,zTop,
  zBot,pendantX}. Consumers followed automatically (fills incl.) — placement-as-one-
  module proved itself.
- build.js: RaftFrame (3 axis-aligned cylGeom instance nodes) + BridleLines (8 pendants,
  hand-built kind:'lines' geom, material 'cable'); VacuumVoid = hullBandGeom full
  revolve, s 0.985, material voidBlack (palette) — views.js vacuum shows VOID only,
  balls never build (viewer ensureVacuumFill no-ops); SolarSkin = instanced boxGeom(1,1,1)
  DECKING with exact ZYX euler extraction from [meridian|hoop|normal] (m4compose is
  Rz·Ry·Rx: rx=atan2(hoop_z,nrm_z), ry=asin(−tm_z), rz=atan2(tm_y,tm_x)), proud + hoop
  sagitta; solarG/solarGeom band retired.
- Tests: containment flipped (raft groups OUTSIDE + below keel); breach-audit
  EXTERNAL_PREFIXES grew the raft cargo (interference still applies — and CAUGHT two
  real bugs: LN2 3.4:1 vs 3.1 row pitch, then cross-row gap sized to the water radius;
  both fixed); vacuum browser test = "one black void, not a field of cells"; raft bars
  + solar plates selectable:false (pick space clean); DropOutlet left the pick list;
  captions de-balled. Badges follow-up shipped earlier (f4502ec era): roster rows +
  cockpit headers + fallback generator + goldens.
- REMAINING from the operator batch: shipviz derives from resolveClass/buildLayout
  (single-source step F — direction recorded, avatar hand-matched for now); wash
  particles #97 (reproduce-first); hero #98.

## Part 21 — exterior fix shipped; THE PUBLIC ARC briefed (operator, 08-13 night)

SHIPPED: airships@<exterior-fix> + pink-sites@9596604 — the exterior allow-list
(3d/render/views.js EXTERNAL_PREFIX) now includes the raft cargo; the operator's
"only two lines down" report was exterior mode hiding the moved machinery. Test
'exterior hides the interior' flipped to assert the doctrine. CHAIN28 EXIT=0.

THE PUBLIC ARC (operator's verbatim asks, staged as #99/#100 — START HERE NEXT):
1. Move the viewer + design information OUT of the passworded area, organized into
   the main site. Three entries: "Inspect the design", "Watch the fleet", and
   "See the engineering" (engineering sits BELOW the other two).
2. HERO ANIMATION on the main page: the design model WITH the environment, but
   trees and people ALL THE WAY AROUND the ship (in view from any azimuth), slow
   spin exactly like the viewer's idle turntable, NO user control, and a link
   "Inspect the ship" -> the current explorer page. (Absorbs task #98; the person
   scale-tick at the bow is already slated for removal in the hero variant.)
3. GOOD NAMING for the pages (operator explicitly asked; propose e.g. /ship/
   /fleet/ /engineering/ under pinkrobotics.ca — decide with taste, review against
   the estate design memory).
4. MORE LINKED INFORMATION like the levels page but PUBLIC-FRIENDLY copy and
   materials — figures included and UPDATED to the current idea (capsule, raft
   undercarriage, beam rotors, colour-coded lines, currently-impossible bigs);
   clean, concise, estate styling/structure/formatting (pink-sites design system;
   tone contract in pink-sites-estate-design memory).
IMPLEMENTATION NOTES: the auth gate lives in the pink-edge Caddyfile
(@pinkrobotics_cell block) — moving pages public means NEW public paths with new
copy, not un-gating cell/* verbatim (the gated checks pages keep their audience).
The hero should be a hero-specific ENV VARIANT in buildVessel (ring of trees +
people at all azimuths — a flag, not a rewrite of the lake-shore scene) driven by
a small no-controls boot on the front page; co-agent owns the ridge hero regions,
so land it as a new module and integrate minimally after checking git log.
STILL QUEUED BEHIND THIS: wash particles #97 (reproduce-first), shipviz
single-source derivation, tail-surface retirement on the 3D model.
