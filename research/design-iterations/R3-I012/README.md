# R3-I012 — a dimensioned four-bay payload/trim arrangement for the gas P-100

Status: design iteration, 2026-10-14, on the corrected [R3-I007](../R3-I007/README.md) equipment set
and trim laws. Internal, conditional design
hypothesis pending applicable claim review; no positive public claim is made here. No aircraft has been
built or flown. Every number below is either copied from a recorded source, computed by
[`layout.py`](layout.py) (deterministic, stdlib only; this revision's figures are from one bounded
recorded execution), or labelled assumed / UNKNOWN. Not a drawn structure: the hardware set is
preliminary with declared assumptions (±50 %); no bracket, seam, valve or load path is drawn — and
disjoint occupancy / usable bay capacity are UNKNOWN here (see below).

## The question

R3-I007 closed the mass budget and the 100 t trim cycle at the *aggregate* level — one water-delivery
set line, 4.94 t, kept from the recorded floor kit. This unit asks the next question: **can the two
50 t deliveries be given ONE dimensioned arrangement inside the corrected I007 hull — four discrete
water bays, supports, valve and pump routing, per-state mass/force/moment balance — such that every
state of the outing closes under the corrected I007 laws (SL-return floor, 50 % bag cap, rate-matched
exchange, zero-slack fuel envelope), with the asymmetric intermediate release states shown rather than
concealed by the symmetric ideal?** The economics verdict is expected to survive unchanged and is
re-derived, not assumed.

## The dimensioned arrangement

Four bays in two frames on the hull centreline, in the P-100 capsule (110.0 × 27.5 m; drawn volume
217,547 m³, 1.3 % below the recorded 220,000 m³ displacement anchor, which all lift uses — programme
convention, stated once):

| Bay | Centre (x, y, z) m | Frame | Delivery |
|---|---|---|---|
| B1-FL | (−10, +11, −19) | fore | **D1** (fast drop) |
| B4-AR | (+10, −11, −19) | aft | **D1** (fast drop) |
| B2-FR | (−10, −11, −19) | fore | **D2** (hose exchange) |
| B3-AL | (+10, +11, −19) | aft | **D2** (hose exchange) |

- **Shell:** 3.0 × 3.0 × 2.8 m outside, baffled, ~48 kg/m³ (assumed). **Usable capacity per bay is
  UNKNOWN** — 25.2 m³ of outside envelope does not price internal walls, baffles or freeboard, so it
  does not by itself prove 25 m³ of storable water; the ledger carries water as *mass* (25 t/bay), not
  as a drawn tank. Two bays per 50 t delivery: **D1 = B1-FL + B4-AR** (a diagonal pair), **D2 =
  B2-FR + B3-AL** (the other diagonal).
- **Why diagonals:** each pair's centroid sits exactly on the hull centreline — D1 and D2 centroids
  both (0, 0, −19) — so *every* conserved state of the outing has zero nominal pitch and roll moment by
  construction. The real moments are the mismatch/worst cases below, not hidden averages.
- **Clearance (computed, necessary but NOT sufficient):** hull half-width at the bay depth z = −19 is
  19.9 m against a bay outboard edge at 12.5 m — **7.4 m of lateral skin clearance**; the hull floor
  under a bay row is −25.2 m against a bay bottom at −20.4 m — **4.8 m vertical**. This does **not**
  demonstrate disjoint occupancy: the ledger allocates *all* of V between mixture and ballonet with
  **nothing reserved** — the four shell outside envelopes alone occupy 100.8 m³, with equipment and
  routes undrawn beyond them — so occupancy is UNKNOWN and the scalar results below are an **ideal
  unobstructed-volume bound**. The drawn construction (reserved volumes, usable capacity, routing) is
  the next unit's work.
- **Supports:** two shared frames (one per x = ±10 m station) with cradles under each bay and
  suspension pick-ups fairing into the main suspension curtains; the frames are the stiff backbone the
  matched manifolds hang from.
- **Valve/pump routing:** a paired release manifold per D1 frame station — both doors interlocked,
  matched orifices, declared drain-rate mismatch bound ±5 % — for the fast drop; a single dip hose at
  the D2 station delivering at the scoop pump rate (rate-matched exchange); an internal cross-pump
  (~1.2 m³/min assumed ±50 %, Fire Boss-class; hover/dip procedure UNKNOWN) that routes scooped water
  into the emptied D1 bays first, the tail into the emptying D2 bays, and pumps the ballast out again
  at the base.

```
side elevation (x: nose -55 left, tail +55 right; hull axis z=0; 1 char ~ 2.8 m)

        fore ballonet (55k m3 max)         aft ballonet (55k m3 max)
     .--------------------------.      .--------------------------.
   .'                            '....'                           '.
  (  mixture 97/3 He/air, inventory n0 = 165,403 m3 STP (drawn)      )
   '.                            '----'                           .'|
     '--------------------------'      '--------------------------' |
             |cradle|                       |cradle|                |
     [B1-FL] [B2-FR]             [B3-AL] [B4-AR]      winch/hose    |
       x=-10    z=-19               x=+10   z=-19        z=-22.5     |
  ________________________________._______________________________|
  |<--- midbody 54.9 m ---------->|<-- nose 27.5 + tail 27.5 m --->|
        gondola + equipment (x~0, z=-22.5): 6 engines, paired fuel
        tanks x=+/-3, trim controls; suspension curtains carry the
        bay frames at x=+/-10 m down to the keel

section at x=+/-10 m (bow view; y+ = port/left; 1 char ~ 1.7 m)

            z=0  __________________
            _,--'                  '--._
        _,-'      mixture / bag          '-,_
     _,-'   (bag 3.7% departing -> 33.4% post-D1 of V at 2,500 m,  '-,_
   ,'          55k m3 cap/side; 48.0% max at SL - under the 50% cap)   ',
  |          _,  z=-19:  [B?-L]      [B?-R]          |   y=+/-11 m
  |        ,'  \____/          \____/        ',
  |       | 25 t  |    22 m     |  25 t |        |   hull R=27.5 m
  |       | water |<----------->| water |        |
   ',      \____/                \____/      ,'
     '-,_        cradles to keel          _,-'
         '--..____ gondola ____..--'   z=-22.5 (engines/fuel/trim)
                   | suspension curtains to hull skin
```

Occupancy at each state is the ledger below (which bays hold payload or scooped ballast); the section
view shows the full 100 t departure load, both bay rows occupied. The section is a *schematic of
mass placement*, not a disjoint-occupancy demonstration (see the clearance note above).

## Preliminary hardware (declared assumptions, ±50 %, undrawn)

| Line | Mass t | Basis |
|---|---|---|
| Bay shells 4 × (25.2 m³, baffled, ~48 kg/m³) | 4.80 | assumed areal density |
| Shared frames + cradles + suspension pick-ups | 1.60 | allowance, undrawn |
| Paired release manifold, doors, valves | 1.40 | allowance, undrawn |
| Water cross-pump + internal piping | 0.35 | allowance, undrawn |
| Ballonet air-transfer ducts + fans | 0.75 | allowance, undrawn |
| Trim controls, wiring, instrumentation | 0.30 | allowance, undrawn |
| **Total dimensioned set** | **9.20** | replaces the recorded tanks+pump 2.34 t |
| Equipment ex-hull | 45.63 | corrected I007 38.77 + 9.20 − 2.34 |
| **Dry vehicle** | **69.38** | gas hull 23.75 + equipment (incl. the 5.40 t fuel+tank line: 4.90 t consumable + 0.50 t permanent tank) |
| **Loaded (dry + 100 t)** | **169.38** | |

Margin at max inventory (lift 175.98 t): **+6.60 t** with the dimensioned hardware; the **massless
ideal bound** — keeping the recorded 2.34 t aggregate tanks instead — is **+13.46 t** (I007's margin).
The dimensioned set costs **6.86 t of margin**; it buys the floor-freedom below. Departure inventory
n₀ = 165,403 m³ (SL) → lift 169.38 t, balanced at departure sizing (bag 3.7 % at 2,500 m, 24.8 % at
SL).

## The outing against the corrected-I007 laws

- **D1 (zone A, no lake):** paired-manifold fast drop of B1-FL + B4-AR (~9 min) concurrent with the
  relief vent, which stops **at neutral**: n₁ = 114,463 m³ (vent 50,940 m³ = 10.24 t mixture =
  **8.36 t He, the only vent and only helium purchase of the outing**); bag after 33.4 % at 2,500 m,
  48.0 % at SL. The vented mixture splits **by species** as 49,411 m³ STP He + 1,529 m³ STP air
  (97/3 by STP volume) — the reset below restores both constituents. Declared transient bound:
  residual ≤ ~5 t for ≤ 2 min while release and vent rate-match.
- **The SL-return floor never binds — the one place the hardware mass helps.** The floor
  (n ≥ 110,000 m³; lift 112.64 t) would cap total venting at 55,403 m³, and the whole outing vents
  50,940 m³ — but more precisely: this craft's D1 *neutral* sits **4,463 m³ above the floor**, so the
  full neutral vent is legal. Corrected I007's D1 neutral (107,764 m³) lay 2,236 m³ *below* its floor,
  so I007's vent was floor-capped and it flew the transit ~2.3 t light. The 6.86 t of dimensioned
  hardware is exactly what lifts the neutral above the floor. A neutral vent reconciles the weight
  *change* (50 t payload + burn), from which **dry mass cancels** — hardware mass does not change the
  vent (see economics).
- **D2 (zone B, a lake):** rate-matched exchange — the hose delivers the B2-FR + B3-AL pair at the
  scoop rate while the lake refills **50.9 t** of ballast (50.0 t into the emptied D1 bays + 0.9 t tail
  into the emptying D2 bays, both diagonals on-axis). **No second vent, no helium or bag-capacity
  reset between drops**: the exchange closes with water alone and the residual stays in band end to
  end (~+0.3 → +0.1 → 0.0 t). A fast D2 (instant release, no concurrent scoop) would swing ~50 t light
  against 10–15 t of thrust authority — several times over, which is why D2 is an exchange.
  An earlier internal sketch vented D2 down to the floor as well (9.10 t He, a −4.3 t heavy dip
  mid-exchange): nothing forces it, the sketch was rejected, and it is recorded in the unit evidence.
- **Return and reset:** return on the scooped ballast; the descent grows the bag 33.4 % → 48.0 % —
  **under the installed 50 % total cap at every state, 2.0 % spare at the maximum** (the separate
  55,000 m³ *per-bag* capacity is what bounds transfer authority — asymmetric section below). At
  base, moored: pump out the 50.9 t (cross-pump at the scoop rate, ~45 min) → 52.5 t light;
  **restore the vented mixture by species** — re-add 49,411 m³ STP of helium (8.36 t, the only
  helium purchase) *and* re-admit 1,529 m³ STP of air **into the lifting-mixture compartment**
  (declared routing convention; the admission path's hardware is UNKNOWN — and air into a ballonet
  alone would *not* restore the mixture's air fraction. Free from atmosphere; its admission work is
  **not** in the partial energy budget below) — re-adding 50,940 m³ of pure helium would change the
  composition. The reset inventory is **computed from these operations** (species arithmetic: the
  arrival mixture split by the declared 97/3, plus the two named replenishments — 49,411 m³ STP He
  and 1,529 m³ STP air) → computed n_S7 = 165,403 m³, asserted equal to S0's n₀ at the declared
  97/3 composition with the two species asserted individually → **104.7 t light on the mast against the
  recorded 1.2 MN cable (122 t) — within, 17.7 t to spare** (mast load is payload + burnt fuel +
  hardware, independent of inventory); refuel 4.70 t (to 4.90 t consumable, derived as arrival +
  refuel); load 100 t; release neutral. The reset state is **computed and checked** as the S7
  ledger row — the assertions consume the computed inventories, never an assigned target — and it
  reproduces S0 exactly (asserted in `layout.py`). Ops complete **no earlier than t = 6.50 h**
  (~45 min pump-out after S6 arrival; replenishment/load durations UNKNOWN, moored — outside the
  6.00 h flight envelope).

## Per-state ledger (from `layout.py`; every term once; force identity asserted each state)

Fuel column = consumable fuel only (the 0.50 t tank is permanent hardware inside dry). Residual =
lift − (dry ex fuel + fuel + payload + scoop); + light / − heavy. Ballonet air is tracked per state
(SL→2,500 m climb sheds ~59 t as the mixture expands; descent re-admits it). Times in hours;
uncertainties bounded in the sensitivity section.

| State | t h | fuel t | pay t | scoop t | air t | n m³ | bag % | lift t | weight t | resid t |
|---|---|---|---|---|---|---|---|---|---|---|
| S0 mast release, SL | 0.00 | 4.90 | 100 | 0.0 | 66.9 | 165,403 | 24.8 | 169.4 | 169.4 | +0.00 |
| S1 top of climb | 0.50 | 4.49 | 100 | 0.0 | 7.9 | 165,403 | 3.7 | 169.4 | 169.0 | +0.41 |
| S2 zone A arrival | 2.50 | 2.86 | 100 | 0.0 | 7.9 | 165,403 | 3.7 | 169.4 | 167.3 | +2.04 |
| S3 D1 done (50 t) | 2.65 | 2.74 | 50 | 0.0 | 70.3 | 114,463 | 33.4 | 117.2 | 117.2 | +0.00 |
| S4 zone B arrival | 3.00 | 2.45 | 50 | 0.0 | 70.3 | 114,463 | 33.4 | 117.2 | 116.9 | +0.29 |
| S4.5 exchange midpoint | 3.38 | 2.14 | 25 | 25.4 | 70.3 | 114,463 | 33.4 | 117.2 | 117.1 | +0.14 |
| S5 exchange done (100 t) | 3.75 | 1.84 | 0 | 50.9 | 70.3 | 114,463 | 33.4 | 117.2 | 117.2 | +0.00 |
| S6 base arrival, SL | 5.75 | 0.20 | 0 | 50.9 | 129.3 | 114,463 | 48.0 | 117.2 | 115.6 | +1.63 |
| S7 reset checked (=S0) | 6.50* | 4.90 | 100 | 0.0 | 66.9 | 165,403 | 24.8 | 169.4 | 169.4 | +0.00 |

\* S7's t = 6.50 h is the **earliest** ops-complete clock (~45 min pump-out after S6 arrival;
replenishment/load durations UNKNOWN, moored — outside the 6.00 h flight envelope). Its masses are
the *computed end state of the reset operations* (ballast pumped out, He + air restored to the
mixture by species, fuel refilled, 100 t reloaded — each derived from the S6 arrival row plus its
named operation, not assigned) — `layout.py` asserts the computed inventory, both species, the
composition and the weight reproduce S0; it is not a copy of S6.

Residuals are **all light-side, max +2.04 t**, within ±2.6 t against 10–15 t of thrust authority. Net
vertical force is the residual column; the script asserts the force identity
(displaced − mixture − air − dry − payload − scoop = lift − weight) at every state to guard against
double-counted terms. Nominal Mx/My are zero every state by construction (pair centroids on the
centreline, fuel equal-draw from ±3 m tanks, ballonet air at the 50/50 fore/aft datum); the real
moments are next.

## Asymmetric intermediate release states (defined, not concealed)

The symmetric ideal — matched manifolds, simultaneous release — is a *bound*, not a description. Each
state below is **defined** (own time, water, inventory, altitude) and carries its **own gross mass** —
dry ex fuel + fuel + water + mixture + ballonet air — in the CoM and heel denominators; the fixed
169.38 t departure load is not any flying state's gross (a first-review finding, corrected here).

| State | water t | n m³ | fuel t | mix t | air t | **gross t** | pitch t·m | roll t·m | CoM shift (p, r) m |
|---|---|---|---|---|---|---|---|---|---|
| S2 cruise (min air) | 100.00 | 165,403 | 2.86 | 33.2 | 7.9 | 208.5 | — | — | — |
| D1-end ±5 % mismatch | 51.25 | 114,463 | 2.74 | 23.0 | 70.3 | 211.7 | 12.5 | 13.8 | (0.059, 0.065) |
| One bay empty, mid-D1 (t = 2.575 h) | 75.00 | 138,935 | 2.80 | 27.9 | 40.3 | 210.5 | 250.0 | 275.0 | (1.188, 1.306) |

- **Design bound:** ±5 % manifold mismatch of 25 t = 1.25 t retained at the released bay → pitch
  12.5 t·m (x-arm 10 m), roll 13.8 t·m (y-arm 11 m). **Absolute worst** (manifold failure, one bay
  empty, pairmate full): 25 t off-diagonal → pitch 250 t·m, roll 275 t·m. Gas contributes the
  denominator, not the numerator (mixture centroid and the 50/50 air datum sit on the centreline).
- **Pitch authority is helium-free but ONE-DIRECTIONAL and state-specific, bounded by BOTH the donor
  bag's air and the receiving bag's headroom** under the declared separate 55,000 m³ per-bag capacity
  (both bags at the same P,T from the 50/50 datum); the displaced lifting mixture still nets the
  transfer ×(1 − 0.164045). Donor-bound datums: minimum-air (S1/S2, 7.88 t air) **196.98 t·m one-way,
  164.66 t·m net** — the first candidate's 393.96 t·m whole-inventory figure is **withdrawn** — and
  one-empty mid-D1 (air 40.3 t) **1007.5 / 842.3 t·m**. **Receiver-bound:** at the D1-end mismatch
  datum the bag is 33.4 % of V, so moving the whole donor half would put 33 % of V into one bag
  against its 25 % of V cap — headroom caps the transfer at 18,273 m³ (vs 36,727 m³ of donor air) →
  **874.2 / 730.8 t·m**. The earlier donor-only 1757.0 / 1468.8 t·m D1-end figure was **not an
  installed-capacity bound and is withdrawn** (installed one-direction authority at that datum is the
  receiver-bounded figure; nothing here proves the small mismatch untrimmable).
- **Coverage, per state:** the ±5 % mismatch (12.5 t·m pitch) sits within net authority at its own
  datum (731 t·m there, receiver-bounded). The one-bay-empty pitch demand **250 t·m EXCEEDS the
  164.66 t·m minimum-air one-direction bound** — at that datum ballonet transfer alone does not
  cover it, while at the neutral one-empty mid-D1 datum it does (842 t·m). Release and vent timing
  set the actual state: this is **not** a universal transient-failure claim, and recovery for the
  fault case at the minimum-air datum (concurrent vent, thrust, ballast) is **UNKNOWN**. Transient
  response is not established anywhere — static capacity is not transient control.
- **Roll:** no bag authority (ballonets on the centreline); pendulum righting W×h with the **state's**
  gross — ≈ 5,294 t·m/rad (211.7 t) at the mismatch bound → heel **0.15°**; ≈ 5,262 t·m/rad
  (210.5 t) one-bay-empty → heel **2.99°** (rigid-hull assumption; envelope heel limit UNKNOWN —
  R3-I006 does not establish the P-100 interface).
- **Between deliveries:** the empty D1 pair is a balanced diagonal (zero moment); the scoop refills
  the *same* diagonal first, so both stay on-axis through the exchange. The intermediate states above
  (S3–S5) are the asymmetric worst cases, not averages.

## One concrete trim action per transition

| Transition | Action |
|---|---|
| S0→S1 climb | auto-valves shed ~59 t of ballonet air as the mixture expands (fans trim the rate; descent is the reverse); not neutral at top: +0.41 t light from climb burn |
| S1→S2 cruise | none (lightness grows with burn, inside authority) |
| S2→S3 D1 | paired-manifold drop concurrent with the 50,940 m³ relief vent to neutral (rate-matched; bound ≤ ~5 t ≤ 2 min); mismatch moments within one-direction ballonet authority at that datum (asymmetric section); transition energy bounded below, closure UNKNOWN |
| S3→S4 transit | none (fuel burns from paired centreline tanks, equal draw — no moment) |
| S4→S5 D2 | rate-matched exchange (hose out at the scoop rate, lake water in: 50.0 t to the D1 bays + 0.9 t tail); no vent — the exchange closes with water alone |
| S5→S6 return | valve air in freely as the mixture contracts; light residual on thrust; bag 33.4 % → 48.0 %, under the cap throughout |
| S6→S7 reset | pump out 50.9 t (~45 min), restore the vented mixture by species into the mixture compartment (49,411 m³ STP He purchased + 1,529 m³ STP air; admission hardware/routing UNKNOWN), refuel 4.70 t, load 100 t; the S7 row is **computed** from these operations and reproduces S0 (asserted); ops complete no earlier than t = 6.50 h (pump-out ~45 min after S6; moored, outside the 6.00 h flight envelope) |

Impossible transitions stay FAIL/UNKNOWN, never averaged away: fast D2 (~50 t light swing — beyond
authority), venting below the SL floor (strands the ship), bag beyond 50 % (cap-blocked).

## Transition energy (partial preliminary budget — closure UNKNOWN)

The first candidate's "~2 kW" line carried no head, efficiency, work or source; it is withdrawn and
replaced by this bounded budget (heads/efficiencies declared ±50 %, no qualified pump/fan map,
supply allocation undrawn — **energy closure UNKNOWN**; this is missing accounting, *not* a
demonstrated fuel shortage):

| Transition | Work | Electrical | Mean power |
|---|---|---|---|
| D2 exchange pump: 50.9 t at 10 m declared head | 4.99 MJ hydraulic | 9.99 MJ at 50 % | 3.7 kW over 45 min |
| Reset pump-out: 50.9 t at 5 m head | — | 4.99 MJ at 50 % | 1.8 kW |
| D1 trim fans: 1 t air at 1.5 kPa declared | — | 3.92 MJ at 40 % | within the ~9-min window |

Total for the **listed** transitions: **18.9 MJ electrical (5.2 kWh) ≈ 0.0015 t fuel equivalent** at
a 30 % generator — a **partial budget**: only the D2 exchange pump, the reset water pump-out and the
D1 trim fan are listed. **Reset-air admission, helium handling and every other supply/transition
work are UNKNOWN and not included** (the D1 trim-fan term does not account for reset-air work).
The inherited fixed burn (0.817041 t/h) **excludes** this demand and is kept distinct; both
off-nominal fuel-FAIL cases below stand unchanged — no new fuel shortage is inferred from the
missing accounting.

## Schedule/fuel envelope (carried corrected-I007 law, zero slack)

The 4.902246 t of consumable fuel (0.50 t tank permanent, never burns) buys **exactly** the 6.00 h
nominal outing including the 0.25 h / 0.204260 t reserve — **zero slack**; a timing slip is covered
only while ≤ +15 min. Both carried off-nominal cases are **fuel FAIL / outside the accepted nominal
envelope**: (a) the +33 min published band (climb +10, exchange +23 min) reaches 6.30 h —
**0.245112 t short** (cover 5.351618 t = +0.449373 t fuel + ~0.05 t tank, priced not taken);
(b) the −50 % pump (0.6 m³/min, reciprocal rate with burn coupling — this craft's smaller 50.9 t
scoop alone takes 84.831242 min, the overtime burn must itself be scooped, converging at
**85.756228 min** of exchange and **6.429270 h** base arrival) — **0.350732 t short** (cover
5.457237 t = +0.554992 t fuel + ~0.06 t tank, priced not taken). The extra exchange burn is scooped
ballast, not helium.

## Economics — the retained FAIL (re-derived from this ledger)

8.36 t He = 49,411 m³ STP vented per 100 t airborne-delivered (494 m³ per delivered tonne; of the
50,940 m³ vented mixture, 1,529 m³ STP was air — re-admitted free at reset, so the priced purchase is
the helium alone) — one
neutral vent, **+0.36 t vs corrected I007's 8.00 t floor-capped vent**. The difference is the
residual-band choice (full neutral here vs I007's floor-blocked ~2.3 t light transit), **not hardware
mass — dry mass cancels from a neutral vent**; what the 6.86 t of hardware costs is margin (+13.46 →
+6.60 t), and in exchange it lifts the neutral above the floor, which is what makes the single full
neutral vent legal.

| Helium price | Per delivered tonne | Per 100 t cycle |
|---|---|---|
| $12/m³ (USGS base 2025) | $5,929 | $0.59 M |
| $28/m³ (retail low) | $13,835 | $1.38 M |
| $92/m³ (retail high) | $45,458 | $4.55 M |

Public comparator: scooping SEAT ≈ $169/t → **35.1×** that cost at the USGS base; sign-reversal needs
helium at **$0.34/m³** — no public price is near it. Jet fuel per outing (4.70 t) is under $15k —
under 1 % of the helium bill. Same custody basis as I007 (USGS 2026 MCS; Fire Boss operator-published
comparator); no vendor contacted.

## Sensitivity (margin at max inventory, +6.60 t)

Hardware masses +50 % (undrawn) −4.60 → +2.00; I007 fabric lines hi range −3.80 → +2.80; **I007
sundries +50 % −9.82 → −3.22 (breaks it)**; I007 trim set 3→9 t −6.00 → +0.60; endurance 6→12 h
−4.90 → +1.70; TSFC +20 % −0.98 → +5.62; balance sizing instead of max inventory −6.60 → 0.00.
Sign-reversal on the hardware set alone at 15.8 t (+72 % over estimate); any one large carried I007
line plus hardware +50 % breaks the closure — **thinner than I007's, honestly**.

## Verdict

- **GEOMETRY: closes as an ideal unobstructed-volume bound only.** Four bays at (±10, ±11, −19) m in
  two frames; 7.4 m lateral and 4.8 m vertical skin clearance — necessary, not sufficient; diagonal
  deliveries put both pair centroids on the centreline — every conserved state zero-moment.
  **Disjoint occupancy and usable bay capacity are UNKNOWN** (no reserved volume: the shells alone
  occupy 100.8 m³; internal walls unpriced); the drawn construction is the next unit's work.
- **TRIM/CAPACITY: closes under the corrected-I007 laws for the nominal cycle.** One neutral vent
  50,940 m³ (8.36 t He); D2 closes with 50.9 t of scooped lake water; no second vent, no resets; the
  SL floor never binds (cleared 4,463 m³); max bag 48.0 % — under the 50 % cap; residuals light-side,
  max +2.04 t; the ±5 % mismatch sits within state-specific one-direction ballonet authority
  (bounded by donor inventory **and** receiving-bag headroom — receiver-bounded at the D1-end datum,
  730.8 t·m there); the
  **one-bay-empty pitch demand 250 t·m exceeds the 164.66 t·m minimum-air one-direction bound**, so
  recovery for that fault case at that datum is UNKNOWN (state-dependent; larger air inventories cover
  it); transient response is not established anywhere — static capacity is not transient control;
  fast-D2 and below-floor transitions stay FAIL/UNKNOWN; transition-energy closure UNKNOWN (bounded
  budget above, distinct from the fixed burn).
- **FUEL/SCHEDULE (carried law): zero slack.** 6.00 h / +15 min envelope only; +33 min and −50 %-pump
  cases fuel FAIL (0.245112 / 0.350732 t short), covering priced not taken.
- **ECONOMICS: retained FAIL.** $5,929/t at the USGS base = 35.1× the comparator; the arrangement's
  helium bill is set by the reconciled weight change (payload + burn), not by its own hardware mass.

**Confidence:** high on the arithmetic (bounded scalar identities, asserted per state, deterministic
and diffed); low on the hardware masses (±50 %, undrawn) and on every withdrawn item (occupancy,
usable capacity, transient response, energy closure — UNKNOWN, not shown); none claimed on economics
(retained FAIL — a paper margin, never renamed as a physical float). **Weakest assumption:** the
9.2 t hardware set (undrawn, ±50 %) — it thins the mass margin to +6.60 t with sign-reversal at
15.8 t. **Next geometry change (one, a proposal to derive, not a result):** draw the x = ±14 m frame
stations with staggered z fairing the cradle loads into the main suspension curtains — the ~0.4 t
frame saving quoted by the first candidate was an assumption, to be replaced by a quantity-derived
mass — then re-price the shells from a drawn tank (usable capacity) and re-run the mismatch bound with
a real valve spec.

Carried unresolved: D2 exchange ops (pump rate, hover/dip) UNKNOWN and load-bearing (its −50 % case is
fuel FAIL); transition-energy closure UNKNOWN (bounded budget, distinct from the fixed burn); disjoint
occupancy and usable bay capacity UNKNOWN (withdrawn to an ideal-volume bound); one-bay-empty trim
recovery at the minimum-air datum UNKNOWN; TSFC secondary; 5.2 t of I007 allowances undrawn;
R3-I006 and R3-I010 do not establish P-100 interfaces (envelope heel/pressure limits UNKNOWN).

## Scoreboard

> Dimensioned 4-bay P-100 water kit: one neutral vent 8.36 t He, floor never binds; occupancy, usable capacity, one-empty trim recovery UNKNOWN; economics FAIL: 35.1x SEAT.

(170 characters.) Conditional paper result on an assumed-basis hull and allowance-priced hardware: not
a measured or drawn vehicle, and no public claim is made. The rejected two-vent sketch is preserved in
the unit evidence as a historical attempt.
