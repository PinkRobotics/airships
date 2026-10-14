# R3-I007 — a priced equipment set and the 100 t trim cycle for the gas P-100

Status: design iteration, 2026-10-14, on the corrected R3-I003 gas hull (landed); **corrected in the
design review** (one HIGH, one MEDIUM — the trim cycle and economics below are the repaired, conserved
version; the first-round two-vent cycle is preserved as a historical attempt in the unit evidence);
**fuel/reserve/schedule remainder repaired under the 2026-10-14 targeted check** — consumable fuel
(4.902246 t) is now separated from the permanent 0.50 t tank, and the two published off-nominal
schedule cases are marked **fuel FAIL / outside the accepted nominal envelope** (below).
Internal, conditional design hypothesis pending applicable claim review; no positive public claim is
made here. No aircraft has
been built or flown. Every number below is either copied from a recorded source, computed by
[`budget.py`](budget.py) (deterministic, stdlib only), or labelled assumed / UNKNOWN. Not a drawn
structure: no bracket, duct, seam or load path is designed; masses marked "allowance" are placeholders
with their sign-reversal size stated.

## The question

R3-I003 closed the hull question with a mission FAIL at every recorded equipment class: the floor kit
(gas hull + vacuum-programme equipment, dry 127.25 t) misses the 100 t-payload mission by −51.27 t at
2,500 m. The recorded equipment lines are vacuum-programme hardware — cryo plant, LN₂ tankage, a 20 MWh
battery, a 30 MW electric bus — whose deletion alone leaves the mission negative (−59/−109 t, recorded in
the I003 evidence). This unit asks the next question: **with the gas hull kept and the equipment
re-selected and priced from public component data, does the mass budget close — and can the 100 t
load/drop cycle be balanced without crediting the ballonets with ballast they cannot hold?**

## The law this unit is built on: forced ballast

At zero gauge and fixed hull volume the ballonet-bag volume is not a control — it is forced:

> v_bag(z) = V − v_mix(z) = V − n·ρ₀/ρ(z),  m_air(z) = ρ(z)·V − n·ρ₀

so net lift = n·ρ₀·(1−f) = 1.02405 t per 1,000 m³ of inventory — altitude-independent, set by inventory
alone. Consequences, each computed in `budget.py`:

- **The bag cannot grow into "free room".** Every m³ of bag growth displaces a m³ of mixture: net ballast
  gained = ΔV·(ρ_air−ρ_mix), gas cost = 0.1962 t mixture = **0.1603 t He per tonne of ballast,
  altitude-independent** (the ratio ρ_mix/(ρ_air−ρ_mix) is the constant mixture fraction). A ballonet is a
  trim device, not an arbitrary ballast tank.
- **Altitude exchanges air, not lift.** The SL→2,500 m climb sheds 59.0 t of ballonet air as the mixture
  expands; net lift never moves. There is no altitude at which the drop "gets easier".
- **Superpressure is weak here**: +2 kPa admits only 0.92 t of mixture at scale (220,000 m³ hull).
- **Carried water does not reduce the post-drop need** — ballast aboard is still weight, and it competed
  with the payload for lift on the way out.
- The remaining honest controls: venting (the 0.1603 t/t law), dynamic thrust (~10–15 t with the
  installed 5.4 MW), and the mooring mast (recorded 1.2 MN anchor cable — unlimited at zero airspeed).

## Selected equipment set (public data, recorded lines kept where gas-agnostic)

| Line | Mass t | Basis |
|---|---|---|
| Gas hull (envelope, ballonets, suspension, nose, fins, gondola) | 23.75 | R3-I003 corrected, carried |
| Solar skin | 2.16 | recorded floor line, kept |
| Water delivery set (tanks, pump, hose, cable, anchor bag, winch) | 4.94 | recorded floor line, kept |
| Engines: 6 × PT6A-67B turboprop | 1.41 | EASA TCDS: 234.5 kg dry each |
| Propellers: 6 × | 0.72 | ~120 kg composite each, **assumed** |
| Gearboxes, nacelles, mounts | 1.50 | **allowance, undrawn** |
| Fuel + tankage (6 h) | 5.40 | computed: 2,460 kW cruise at 0.332 kg/kWh (TSFC estimate); **4.90 t of it is expendable fuel** — 0.817 t/h, tracked per state below — **and 0.50 t is the permanent tank** (never burns; rides in dry mass) |
| Ballonet trim set (fans, valves, controls) | 3.00 | **allowance, UNKNOWN detail** |
| Sundries and margin | 19.64 | recorded floor line, kept |
| **Equipment ex-hull** | **38.77** | (recorded floor kit: 103.5 t) |
| **Dry vehicle** | **62.52** | |
| **Loaded (dry + 100 t payload)** | **162.52** | |

Sizing: inventory n = 158,703 m³ (SL) → net lift 162.52 t, **balanced at departure sizing** (full fuel +
100 t payload; bag 7.6 % at 2,500 m, 27.9 % at SL); max inventory 171,851 m³ → lift 175.98 t, margin
+13.46 t. The loaded ship does not stay neutral: fuel burns at 0.817 t/h and the outing ledger below
tracks it state by state (a design-review repair).
Public data used, with custody split: **PT6A-67B primary** — EASA Type-Certificate Data Sheet
No. EASA.IM.E.008 Issue 06 (2022-02-18, type certificate holder Pratt & Whitney Canada Corp.):
895 kW maximum continuous (take-off, 5 min, also 895 kW) and 234.5 kg dry spec weight; **TSFC
0.332 kg/kWh is an estimate from secondary public figures (0.546 lb/shp·h, Wikipedia PT6 table)** —
the TCDS carries no fuel-consumption data and no primary public source is known, so it is treated as
qualified-UNKNOWN with an explicit sensitivity below. Helium: USGS Mineral Commodity Summaries 2026,
base $12/m³ (2025), $14/m³ (2024), public retail band $28–92/m³ (government primary). Comparator:
Fire Boss LLC operator-published comparison, scooping SEAT water delivery ≈ $0.64/gal ≈ $169/t.
No vendor was contacted; no quote was solicited.

Departure identity (every term once, from `budget.py`): loaded at 2,500 m — displaced 210.5 − mixture
31.9 − ballonet air 16.1 = net 162.5 t vs dry+payload 162.5 t; loaded at SL — 269.5 − 31.9 − 75.1 =
162.5 t. The loaded ship is **not** neutral through the outing: already at top of climb it is 0.41 t
light and 2.04 t light at the zone-A arrival (fuel burn; the first-round "neutral throughout the
climb" claim is withdrawn — the review's MEDIUM finding). The D1 vent sizing absorbs the cruise lightness.

## The 100 t trim cycle (corrected after the design review)

- **Capacity wall.** Empty-balanced inventory is 61,051 m³, needing a 64.5 % bag at 2,500 m against the
  50 % installed: full-drop venting is cap-blocked at working altitude. Max single drop on installed
  bags: **74.5 t at 2,500 m**. A full 100 t single-pass drop needs a ~64 % ballonet (+1.01 t fabric,
  sphere-equivalent) — envelope and pressure limits belong to the parallel envelope/pressure-control
  unit (R3-I006); stated here as an interface requirement, not designed.
- **The SL-return floor (the binding constraint).** The bag volume v_bag(z) = V − n·ρ₀/ρ(z) *grows* as
  the ship descends, so the 50 % cap binds at the **sea-level base**, not at 2,500 m: bag(SL) = V − n,
  hence **n ≥ 110,000 m³ for the whole outing** (lift at the floor 112.64 t). Superpressure cannot
  relax this — gauge compresses the mixture, shrinking v_mix and growing the bag. Venting below the
  floor strands the ship at altitude: there is no helium source aloft. This law is what the first-round
  cycle ignored.
- **The two first-round counterexamples, reproduced and marked FAIL.** (a) Closing both 50 t drops by
  neutral vents lands at n = 61,051 m³ with the bag at **64.471 %** at 2,500 m — beyond the installed
  50 %. (b) Those two vents plus the stated 50 t of scooped ballast leave the ship **50.0 t heavy**,
  with no vent left (below the floor) and no helium aloft. The published return state (one vent's
  inventory, n_mid ≈ 109,877 m³) could not carry the two-vent helium bill attached to it: the story
  and the bill described different outings.
- **Corrected cycle — one conserved outing.** D1 at zone A (no lake): a fast 50 t drop (~9 min) with a
  concurrent relief vent that **stops at the floor** — 48,703 m³ = 9.79 t mixture = **8.00 t He, the
  only vent of the outing**; the ship flies the transit leg ~2.3 t light (the floor blocks the last of
  the reconciliation), well inside the 10–15 t thrust authority. D2 at zone B (a lake) is a
  **rate-matched exchange**: the hose delivers mission water at the scoop pump rate (~1.2 m³/min,
  assumed ±50 %, Fire Boss-class) while the tanks refill from the lake, closing the floor-blocked
  ~53 t of lightness with **53.2 t of scooped ballast**; a fast D2 would swing ~53 t light — several
  times the installed authority — which is why D2 is an exchange. Hover/dip scoop procedure: UNKNOWN
  ops. Return 2.0 h on the scooped ballast; the descent grows the bag 36 % → 50 %, exactly at the cap
  at base arrival. At base, moored on the recorded 1.2 MN cable: pump out the ballast (mast takes
  ~53 t of its 100 t case), re-add 48,703 m³ of helium (the only helium purchase), refuel 4.70 t,
  load 100 t of mission water, release neutral.
- **Ledger (from `budget.py`; fuel tracked per state — the fuel column is CONSUMABLE fuel only, the
  0.50 t tank is permanent hardware inside dry; residual = lift − weight, + light / − heavy):**

| State | t h | fuel t | pay t | scoop t | n m³ | bag % | lift t | weight t | resid t |
|---|---|---|---|---|---|---|---|---|---|
| S0 mast release, SL | 0.00 | 4.90 | 100 | 0.0 | 158,703 | 27.9 | 162.5 | 162.5 | +0.00 |
| S1 top of climb | 0.50 | 4.49 | 100 | 0.0 | 158,703 | 7.6 | 162.5 | 162.1 | +0.41 |
| S2 zone A arrival | 2.50 | 2.86 | 100 | 0.0 | 158,703 | 7.6 | 162.5 | 160.5 | +2.04 |
| S3 drop 1 done | 2.65 | 2.74 | 50 | 0.0 | 110,000 | 36.0 | 112.6 | 110.4 | +2.29 |
| S4 zone B arrival | 3.00 | 2.45 | 50 | 0.0 | 110,000 | 36.0 | 112.6 | 110.1 | +2.58 |
| S4.5 exchange midpoint | 3.38 | 2.14 | 25 | 26.6 | 110,000 | 36.0 | 112.6 | 111.4 | +1.29 |
| S5 exchange done (100 t) | 3.75 | 1.84 | 0 | 53.2 | 110,000 | 36.0 | 112.6 | 112.6 | +0.00 |
| S6 base arrival, SL | 5.75 | 0.20 | 0 | 53.2 | 110,000 | 50.0 | 112.6 | 111.0 | +1.63 |
| S7 reset, moored | 5.75 | 0.20 | 0 | 53.2 | 110,000 | 50.0 | 112.6 | 111.0 | +1.63 |

  Max bag fraction of the outing: **50.0 % at base arrival — exactly AT the installed cap, never
  beyond**; residuals stay within ±2.6 t against 10–15 t of thrust authority. Transients: the D1
  release and its vent are concurrent (instantaneous residual ≤ ~5 t for ≤ 2 min, declared bound); the
  D2 exchange is rate-matched end to end (2.6 t light → 1.3 → 0). Every tonne of post-vent fuel burn
  closes with water ballast at 1.00 t per t — no helium cost, because the vent is floor-capped
  (neutralising six hours of burn *by venting* would have cost 0.786 t He: the quantity restated
  from the review's MEDIUM finding).
- **Schedule/fuel envelope (targeted-check repair; the former "±0.45 t, 1:1" line here was wrong —
  it assumed fuel existed to absorb the slip).** The 4.902246 t of consumable fuel buys **exactly**
  the 6.00 h nominal outing including the 0.25 h / 0.204260 t reserve — **zero slack**: a timing slip
  is covered only while ≤ +15 min. Two published off-nominal cases exceed it and are **fuel FAIL /
  outside the accepted nominal envelope**: (a) the +33 min band (climb +10, exchange +23 min) needs
  5.147358 t — **0.245112 t short**; (b) the −50 % pump (0.6 m³/min, reciprocal-rate with burn
  coupling: the 53.19 t scoop alone takes 88.649409 min, the burn during the overtime must itself be
  scooped, converging at **89.663063 min** of exchange and **6.494384 h** base arrival) — **0.403932 t
  short**; the committed code had printed +0.096068 t "remaining" there because the 0.50 t tank rode
  in the fuel column. Covering each case with the reserve held is priced but NOT taken: +0.449373 t /
  +0.608193 t of fuel plus ~0.05 / ~0.06 t of tank (margin +13.46 → +12.97 / +12.80 t) — the nominal
  outing and its economics stand on the declared 6 h / +15 min envelope only.
- **No question of "just venting everything":** the reconciliation need is exactly lift − dry = 100.0 t
  at unburned fuel, every tonne costs 0.1603 t of vented helium at any altitude — and the floor then
  strands anything beyond one vent's worth.

## Delivery economics — the retained FAIL (from the same ledger)

8.00 t He = 47,242 m³ STP vented per 100 t airborne-delivered (472 m³ per delivered tonne) — **one
floor-capped vent**, not the first round's 16.0 t two-vent bill:

| Helium price | Per delivered tonne | Per 100 t cycle |
|---|---|---|
| $12/m³ (USGS base 2025) | $5,669 | $0.57 M |
| $28/m³ (retail low) | $13,228 | $1.32 M |
| $92/m³ (retail high) | $43,463 | $4.35 M |

Public comparator: scooping SEAT ≈ $169/t → helium-trimmed airdrop is **33.5×** that cost at the USGS
base price; sign-reversal needs helium at **$0.36/m³** — 34× below the base price; no public price is
near it. Jet fuel per outing (4.70 t) costs under $15k at any plausible price — under 1 % of the helium
bill; fuel is not the economic constraint. On-board helium capture is rejected by scalar arithmetic:
62,355 m³ of vented mixture at 2,500 m is ~230 m³ of 200-bar pressure-tube volume — hundreds of tonnes
of vessels, and capture would also strand the floor-blocked states. Helium-free alternatives, stated
not selected: **(a) surface transfer** — release at a moored/anchor station, mast takes the load
(recorded cable+winch+hose kept); the mission changes from airdrop to crane/hose, ops UNKNOWN;
**(b) heavy-leg aerodynamic lift** — non-rigid hull CL limit UNKNOWN (R3-I006 interface);
**(c) ~64–72 % ballonet capacity** (mass and volume, R3-I006) — removes the two-pass constraint but
not the helium law.

## Matched before/after budget (t)

| Recorded floor line | | Selected line | | Δ |
|---|---|---|---|---|
| Vacuum shell + barrier | 112.58 | Gas hull (R3-I003) | 23.75 | −88.83 |
| Cryo plant + LN₂ (emergency ballast) | 19.75 | Ballonet trim set | 3.00 | −16.75 |
| Battery 20 MWh | 40.00 | Fuel + tankage 6 h | 5.40 | −34.60 |
| Motors+drives+rotors (30 MW) | 17.01 | Engines+props+mounts | 3.63 | −13.38 |
| Solar skin / water set / sundries | 26.74 | kept | 26.74 | 0.00 |
| **Total structure+equipment** | **216.08** | | **62.52** | **−153.56** |

I003 floor case (gas hull + floor kit, 227.25 t loaded) missed 2,500 m lift by 51.27 t; the selected set
at 162.52 t is balanced with +13.46 t of inventory margin in hand. **The mass budget closes.** The
recorded 30 MW hover-thrust concept is deliberately not carried — mass closes only without it, and a
hovering water-dropper is not the mission the comparator prices.

## Sensitivity (margin at max inventory, +13.46 t)

Fabric lines at the hi range −3.80; sundries +50 % −9.82; trim set 3→9 t (undrawn) −6.00; endurance
6→12 h −4.90; Cd 0.030→0.040 −1.50 (fuel); **TSFC estimate +20 % −0.98** (no primary source; fuel
scales linearly with it); balance sizing instead of max inventory −13.46 (to zero). Burn-side notes
(review repair): all six hours burnt = 4.902246 t; neutralising that *by venting* would cost
0.786070 t He, but the corrected cycle is floor-capped — post-vent burn closes with water ballast at
1.00 t per t, no helium. Schedule slips are NOT absorbed (targeted-check repair): the nominal
envelope admits ≤ +15 min; the +33 min and −50 %-pump cases are **fuel FAIL / outside the envelope**
(0.245112 t / 0.403932 t short; covering priced at +0.45 / +0.61 t with tank growth, not taken —
see the cycle section).
Any two large lines consume the whole margin — the closure is real but thin, and the three allowance
lines (props, mounts, trim set, 5.2 t combined) plus the TSFC estimate are the honest soft spot.

## Verdict

- **MASS: closes.** 38.8 t of equipment ex-hull against a 103.5 t recorded floor; loaded 162.5 t vs
  175.98 t max-inventory lift at 2,500 m.
- **TRIM: closes as one conserved outing** (review-repaired): the SL bag floor caps venting at a
  single 48,703 m³ vent (8.00 t He); D1 fast drop closed by it; D2 a rate-matched lake exchange; return
  on 53.2 t of scooped ballast; base refill 48,703 m³ He; max bag 50.0 % at base arrival; residuals
  ±2.6 t vs 10–15 t authority. A 100 t single drop still needs the ~64 % capacity (R3-I006 interface).
- **ECONOMICS: retained FAIL.** 8.00 t He per 100 t delivered = $5.7 k/t at the USGS base vs $169/t
  public comparator (33.5×; repaired down from the first round's inconsistent two-vent bill);
  reversal needs $0.36/m³ helium. Surface transfer is the helium-free fallback.
- **SCHEDULE (targeted-check repair): zero fuel slack.** The 4.902246 t of consumable fuel (0.50 t
  tank permanent) buys exactly the 6.00 h nominal outing with the 0.25 h reserve; both published
  off-nominal cases — the +33 min band and the −50 % pump (89.663063 min exchange, 6.494384 h base
  arrival) — are **fuel FAIL / outside the accepted nominal envelope**, 0.245112 t / 0.403932 t
  short; covering fuel is priced (+0.45 / +0.61 t with tank growth) but not taken.

**Weakest assumptions:** the D2 rate-matched exchange (pump ~1.2 m³/min, hover/dip at a lake) is an
UNKNOWN ops procedure that the second delivery now depends on — and its −50 % case now also breaks
the fuel envelope (marked FAIL, not absorbed); the TSFC is a secondary-sourced estimate
with no primary public source (fuel scales linearly with it); the propeller/mount masses and the 3.0 t
trim set are allowances, not drawings (5.2 t combined; any two sensitivity lines consume the closure).
**Next design change:** price
the ballonet trim set and the enlarged-capacity (~64 %) option against the envelope/pressure-control
lane — noting that its current R3-I006 envelope does not establish the P-100 bag interface — then
re-run the cycle economics across the retail helium band; a bigger bag removes the two-pass constraint
but not the 0.1603 t/t helium law, so the economics verdict is expected to survive.

## Scoreboard

> Paper gas P-100 kit: mass closes (162.5 t vs 176.0 t lift); one floor-capped vent + rate-matched lake exchange per outing; economics FAIL: 33.5x SEAT cost.

(155 characters.) Conditional paper result on an assumed-basis hull and allowance-priced equipment: not
a measured or drawn vehicle, and no public claim is made. First-round cycle preserved in the unit
evidence as a historical attempt (first review: HIGH inventory inconsistency, MEDIUM fuel-as-trim — both
repaired here).
