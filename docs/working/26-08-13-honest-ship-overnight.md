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
