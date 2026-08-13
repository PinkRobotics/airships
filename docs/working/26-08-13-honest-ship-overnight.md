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
