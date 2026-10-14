# R3-I017 — the drawn four-bay arrangement: tanks, cradles, load path, occupancy

Status: design iteration, 2026-10-14 (consolidated first-review successor; targeted correction), on
the twice-corrected R3-I012 state (in-tree governed successor `0ba417da`; the earlier `7bbc5c23`
line's own review findings are under targeted correction here), which itself sits on the corrected
R3-I007 equipment set. Internal, conditional design hypothesis pending applicable claim review; no
positive public claim is made here. No aircraft has been built or flown. Every number below is either
copied from a recorded source, computed by [`layout.py`](layout.py) (deterministic, stdlib only; this
revision's figures are from one bounded recorded execution), or labelled assumed / UNKNOWN. This is
the unit R3-I012 deferred: I012 carried the bays as *mass* with an allowance-priced hardware set
(9.20 t) and withdrew occupancy to an ideal unobstructed-volume bound; here the tanks, saddles,
pickups and stations are **drawn and priced from quantities**, the disjoint-occupancy question is
held OPEN — the earlier "conditional" bag-plane envelope is **withdrawn** (occupancy UNKNOWN) — and
the twice-corrected I012 laws (one-direction state-specific pitch authority bounded by donor AND
receiver, state-gross CoM/heel, species-consistent reset, partial transition energy) are carried,
not re-derived.

## The question

R3-I012 closed the payload/trim cycle with four bays as mass points at x = ±10 m and a 9.20 t
allowance. The brief for this unit: **can ONE drawn hardware arrangement at the proposed x = ±14 m
frame stations — real tank dimensions, plate thicknesses, saddle beams, pickup fittings, valves and
doors, staggered vertically to fair into the declared suspension-curtain planes — carry the same 100 t
cycle with the load path priced from quantities (not allowances), the frame-station saving DERIVED
(not assumed), disjoint occupancy demonstrated or made honestly conditional, and member
reactions/moments shown for full / ±5 % mismatch / one-bay-empty under one stated loading
convention?** The I012 x = ±10 arrangement is preserved as the sole comparison, re-priced with the
same drawn method.

## The drawn tank (per bay)

Outside 3.05 × 3.05 × 2.85 m; 3 mm 5083 plate — **SELECTED STOCK** (min-gauge + corrosion +
handling, declared); its flat-panel bending/support/attachment adequacy is **UNKNOWN**: the earlier
p·L/(2σ) "0.58 mm pressure thickness" is a membrane/hoop relation, not a flat-panel check, and is
**withdrawn**; no corrected thickness is claimed (bottom hydrostatic head 28.0 kPa freshwater at
1.000 t/m³ declared; weld-affected allowable 90 MPa remains a declared sizing datum for the members
below); two full baffles, 3 mm; 60 mm freeboard. **Usable volume 25.74 m³ ≥ 25.0 m³ required**
(25 t fresh water at 1.000 t/m³ declared; salt at 1.025 would need **24.4 m³** — still within),
ullage margin 3.0 %. Mass from quantities: plates 53.4 m² × 3 mm = 0.432 t + baffles 0.141 +
rims 0.082 + fitout 0.095 (declared ±50 %) = **0.751 t/bay — 28 kg/m³ against I012's assumed 48**.
Slosh impact, gust and release-door transient loads are NOT modelled (quasi-static 1 g × FS 1.5
only).

## The arrangement (drawn stations, diagonal stagger)

Four bays in two frames at the **proposed x = ±14 m stations** — chosen because they coincide with
*declared* curtain planes (0, ±7, ±14, ±21; R3-I003 records no curtain spacing, only a 3 t undrawn
suspension allowance), so the saddles tie directly into structure that is declared to exist:

| Bay | Centre (x, y, z) m | Row | Delivery |
|---|---|---|---|
| B1-FL | (−14, +11, −19.0) | upper | **D1** (fast drop) |
| B4-AR | (+14, −11, −19.0) | upper | **D1** (fast drop) |
| B2-FR | (−14, −11, −21.5) | lower | **D2** (hose exchange) |
| B3-AL | (+14, +11, −21.5) | lower | **D2** (hose exchange) |

- **Diagonal stagger, each pair at one height:** the upper row (B1-FL fore-port + B4-AR
  aft-starboard) sits at z = −19.0, the lower (B2-FR + B3-AL) at z = −21.5, both at y = ±11. Each
  delivery pair is at a single height — release within a pair is height-balanced — and both pair
  centroids stay on the hull centreline in x and y, so **zero nominal Mx/My is preserved**: the
  stagger moves only z, which enters neither the roll (y) nor the pitch (x) arm. The stagger is
  CHOSEN (pickup heights layered on the curtain fan, two working heights), not forced: both rows at
  z = −19.0 would also fit (worst corner then 3.54 m radial).
- **Corner ledger (computed, each bay's own worst and best corner over all four):** the global worst
  radial skin clearance is **1.38 m** at the lower-row outboard-bottom corners (B2-FR/B3-AL,
  y = 12.53, z = −22.93; their best corner 5.30 m) against the declared 0.50 m minimum; the upper
  row (B1-FL/B4-AR) runs worst **3.54 m** (y = 12.53, z = −20.43) to best **7.53 m** — the earlier
  ledger's sign filter had shown intermediate corners for the positive-y bays and omitted their
  worst corner; every corner of every bay now prints. Hull half-width 19.9 m at z = −19.0 and
  17.1 m at z = −21.5 against the 12.53 m bay outboard edge — outboard maintenance gaps
  **7.4 / 4.6 m** (≥ 0.9 m scaffold declared). Inboard, both rows leave |y| < 9.47 m open to the
  keel corridor (lower-row bottom −22.9 m down to the hull floor −27.5 m at y = 0) for hose, ducts
  and the winch at z = −22.5; the gondola/engines/fuel block (x ∈ [−3, 3], z = −22.5) clears the
  nearest bay face by **9.5 m** in x.
- Skin clearance is necessary, not sufficient — the disjoint-occupancy answer is **UNKNOWN** (see
  the withdrawn bag-plane envelope below).

## Member statics (one loading convention)

Convention: quasi-static 1 g, bay weights at cradle points, members simply supported at their pickup
points, allowable 276/1.5 = **184 MPa**. Full bay 25.75 t = **253 kN**.

- **Saddle beam** (per bay): 3.7 m long, 3.0 m support span, UDL → M = **95 kN·m**, S req
  **515 cm³** → **box 200 × 320 × 8 mm** (S 555 cm³, 21.8 kg/m) → **96 kg/saddle** including wear
  pads/lugs. Pickups: **2 × 126 kN** per bay (two-ended, tying into the x = ±14 curtain plane).
- **The x = ±10 comparison** (I012's fixed station) — labelled **SIMPLIFIED SCALAR BEAM, not a drawn
  load path**: no curtain plane at 10, so a transverse X-spreader modelled from the ±7 and ±14
  planes with both saddles at midspan (x = 10 sits 3 m from the 7 plane and 4 m from 14 — NOT
  midway; the separated real pickups need transverse collection that is unpriced) —
  P = **505 kN**, M = **884 kN·m**, S req **4805 cm³** → **box 450 × 800 × 16 mm** (105 kg/m) →
  **839 kg/station of MEMBER STOCK under that simplification**, two stations.
- **The earlier "DERIVED station delta = 1.68 t of spreader the ±14 stations do not need" claim is
  WITHDRAWN** as an established physical saving: 2 × 0.84 t is the simplified beam's member stock,
  conditional on the declared curtain planes AND on an undrawn connecting load path (I012's README
  had ASSUMED ~0.4 t; neither number is an established saving — a derived difference needs member
  statics under the same declared method at both arrangements). If the real planes sat at ±10
  instead, the ±14 stations would need ~2 × 0.84 t of such members (a 3.4 t swing); R3-I003 carries
  the curtain as an undrawn 3 t allowance.
- **Load cases (reactions per pickup):** full bays 126 kN; **bounded release mismatch 1.34 t
  retained at the lagging bay** (±5 % rate at zero skew gives the 1.25 t endpoint; the declared
  linear drain with the allowed 2 s pair start skew gives the 1.34 t bound) → **+6.6 kN at EACH of
  that bay's two pickups** (symmetric UDL → equal ΔW/2 reactions, total +13.1 kN, support-to-support
  difference 0 — the earlier ~8 kN width-lever "end unbalance" figure is withdrawn); one bay empty →
  its saddle falls to shell weight (~7 kN total), the full pairmate unchanged at 126 kN. Endpoint
  interface loads are these same reactions into the curtain fittings — **envelope/curtain attachment
  qualification UNKNOWN, bonds/certificates UNRESOLVED** (fitting hardware priced, attachment not).

## Priced hardware set (from quantities; declared lines ±50 %)

| Line | Mass t | Basis |
|---|---|---|
| Drawn bay shells 4 × (plates+baffles+rims+fitout) | 3.00 | quantities above |
| Cradle saddles 4 × (box 200×320×8, pads, lugs) | 0.38 | drawn section |
| Pickup fittings 8 × (clevis + bonded socket) | 0.10 | declared |
| Bay tie rods (pair spacing/orientation) | 0.05 | declared |
| Isolation valves + actuators 4 × DN300 | 0.14 | declared ±50 % |
| D1 bottom door sets 2 × (hinges, locks, actuators) | 0.16 | declared ±50 % |
| Matched orifice plates + positioners 4 × | 0.06 | declared |
| Internal piping DN300 Al ~30 m + supports | 0.41 | declared |
| Water cross-pump (carried) | 0.35 | I012 line |
| Ballonet air ducts + fans (carried) | 0.75 | I012 line |
| Trim controls, wiring, instrumentation (carried) | 0.30 | I012 line |
| Fasteners, bonds, lugs at interfaces (declared) | 0.10 | declared |
| Keel corridor grating + handrails (declared) | 0.20 | declared |
| **Total drawn set** | **6.00** | vs I012's allowance set 9.20 t |
| Equipment ex-hull | 42.43 | corrected I007 38.77 + 6.00 − 2.34 |
| **Dry vehicle** | **66.18** | gas hull 23.75 + equipment (fuel line unchanged) |
| **Loaded (dry + 100 t)** | **166.18** | |

**Margin at max inventory +9.80 t** (I012 +6.60; massless ideal bound +13.46 t). The drawn set is
**3.20 t lighter than I012's allowance set** — thin-plate drawn tanks and saddle beams replace the
lumped 48 kg/m³ shells and the 1.60 t frame allowance — and that lightness cuts both ways below
(floor and cap margins).

## The ledger on the drawn set (states as corrected I012)

Fuel = consumable only. Residual = lift − (dry ex fuel + fuel + payload + scoop); + light /
− heavy. The force identity is asserted at every state in `layout.py`.

| State | t h | fuel t | pay t | air t | n m³ | bag % | lift t | weight t | resid t |
|---|---|---|---|---|---|---|---|---|---|
| S0 mast release, SL | 0.00 | 4.90 | 100 | 70.7 | 162,278 | 26.2 | 166.2 | 166.2 | +0.00 |
| S1 top of climb | 0.50 | 4.49 | 100 | 11.7 | 162,278 | 5.6 | 166.2 | 165.8 | +0.41 |
| S2 zone A arrival | 2.50 | 2.86 | 100 | 11.7 | 162,278 | 5.6 | 166.2 | 164.1 | +2.04 |
| S3 D1 done (50 t) | 2.65 | 2.74 | 50 | 74.1 | 111,338 | 35.2 | 114.0 | 114.0 | +0.00 |
| S4 zone B arrival | 3.00 | 2.45 | 50 | 74.1 | 111,338 | 35.2 | 114.0 | 113.7 | +0.29 |
| S4.5 exchange mid | 3.38 | 2.14 | 25 | 74.1 | 111,338 | 35.2 | 114.0 | 113.9 | +0.14 |
| S5 exchange done | 3.75 | 1.84 | 0 | 74.1 | 111,338 | 35.2 | 114.0 | 114.0 | +0.00 |
| S6 base arrival, SL | 5.75 | 0.20 | 0 | 133.1 | 111,338 | 49.4 | 114.0 | 112.4 | +1.63 |
| S7 reset checked (=S0) | 6.50* | 4.90 | 100 | 70.7 | 162,278 | 26.2 | 166.2 | 166.2 | +0.00 |

\* The reset is the **COMPUTED** end state, derived by species arithmetic on the S6 arrival mixture
plus the named reset operations — 49,411 m³ STP He purchased + 1,529 m³ STP air replenished to the
MIXTURE compartment (mixture-compartment convention), ballast pumped out (~45 min), 4.70 t refuel,
100 t reloaded — giving n_S7 = 162,278 m³ at 97/3 with **both species asserted individually against
S0**, and weight asserted equal; the clock is the **earliest** ops-complete, t = 6.50 h moored
(replenishment/load durations UNKNOWN, outside the 6.00 h flight envelope). Residuals light-side,
max **+2.04 t** (I012 +2.04).

- **One neutral vent, unchanged:** vent = n0 − n1 = **50,940 m³ = 8.36 t He**; the identity vent =
  (50 t D1 delivery + burn to D1)/1.02405 = 50,940 m³ shows **dry mass cancels** — the drawn set
  changes the vent only through the floor crossover below, not in size; the 50.9 t scoop is likewise
  dry-independent. The species-consistent vent accounting (49,411 m³ STP He + 1,529 m³ STP air) and
  the **partial** transition-energy budget (18.9 MJ electrical covers the LISTED subset only —
  exchange pump + reset pump-out + D1 trim fan; reset-air and other work UNKNOWN; closure UNKNOWN)
  carry from twice-corrected I012 unchanged.
- **The lighter set moves the margins it bought.** n0 = 162,278 m³, D1 neutral n1 = 111,338 m³ — only
  **1,338 m³ above the SL floor** (I012 cleared 4,463): the lighter drawn set lowers n1 toward the
  floor. The floor re-binds below **DRY = 64.81 t**, i.e. a drawn set under **4.63 t** (ours is
  6.00 t) — about 1.4 t of hardware margin before the vent becomes floor-capped again. Max bag
  **49.4 %** of V at base arrival = **99 % of the 110,000 m³ installed cap** (cap margin 0.6 %,
  I012 2.0 %) — the lighter set lifts n1's slack into the bag, trading floor clearance and cap
  margin for the +3.20 t of mass margin.

## Disjoint occupancy (bag-plane envelope WITHDRAWN; occupancy UNKNOWN)

The I012 question — do the bays and the ballonet occupy disjoint volume? — is **not answered**
here. The earlier "conservative envelope, explicitly conditional" demonstration is **WITHDRAWN**
on two counts:

- **The envelope's own arithmetic was nonconservative:** each declared 40 m ballonet centred at
  x = ±25 covers |x| 5..45, but the midbody ends at LC/2 = 27.45 m — **17.6 m of each bag sits in
  the hemispherical-cap sections**, where the span bound had used the full midbody circle R
  throughout. The z = −3.1 m plane, the 14.1 m vertical separation and the 26.3 m sufficient span
  are **NOT established**; membrane shape and drape over structure are UNKNOWN regardless
  (R3-I006/R3-I010 do not establish the P-100 interface).
- **The scalar ledger reserves NOTHING:** mixture + bag volume = V identically, with no term for the
  four tank outside envelopes (**106.0 m³, 4 × 26.5 m³**) or any equipment — placing tanks below a
  bag plane does not reserve them from mixture volume. Every scalar result in this file is an
  **IDEAL-UNOBSTRUCTED-VOLUME bound** (the twice-corrected I012 convention).
- Declared interface data retained (a placement statement, not an occupancy proof): stations between
  the columns (|x| < 5) and outboard of ±45 see no bag on the declared span — the gondola, fuel
  tanks (x = ±3) and winch sit in that bag-free zone.
- **Physical disjoint occupancy is UNKNOWN** — to be re-run only against a drawn bag at the real
  ballonet gore count.

## Moments, authority, finite trim (twice-corrected-I012 laws, the ±14 arms)

**Bounded release mismatch 1.34 t** at x = ±14, y = ±11 — ±5 % rate WITH the allowed 2 s pair start
skew under the declared linear ~9 min drain (endpoints: 1.25 t rate-only at zero skew, 1.34 t at the
allowed skew): roll **14.7 t·m** (I012's rate-only 13.8), pitch **18.7 t·m** (I012 12.5 rate-only —
the 14 m station grows the pitch arm 40 %); one bay empty: roll **275 t·m** (= I012), pitch
**350 t·m** (I012 250, +40 %). Authority is the twice-corrected **one-direction net law, bounded by
BOTH the donor bag's air and the receiving bag's headroom** under the separate 55,000 m³ per-bag
capacity (the receiver bound governs at datums whose bag exceeds 25 % of V — the D1-end datum
here); donor bag at the 50/50 datum, displaced mixture nets ×(1 − 0.164045), state-specific:

| Datum | n m³ | air t | gross t | pitch demand t·m | auth net t·m | covers |
|---|---|---|---|---|---|---|
| min air (n0 @2500) | 162,278 | 11.7 | 208.5 | 0.0 | 244.7 | (bound) |
| D1-end mismatch | 111,338 | 74.1 | 211.8 | 18.7 | 650.8 | yes |
| one bay empty mid-D1 | 135,811 | 44.1 | 210.5 | 350.0 | 922.3 | yes |

I012 twice-corrected values at the same datums: 164.66 min-air / 730.8 mismatch / 842.3 one-empty;
the earlier donor-only **1548.8 t·m at the mismatch datum was not an installed capacity** and is
superseded by the receiver-bounded 650.8 row. **Coverage, per state:** the mismatch pitch is
covered at its own datum; the one-bay-empty pitch 350 t·m is covered at the neutral one-empty
datum but **EXCEEDS the 244.7 t·m minimum-air one-direction bound** — same structure as corrected
I012, ratio 1.43 here vs 1.52 there (the 14 m arm grows the demand; the lighter kit grows the
min-air inventory; net marginally less exposed). Recovery at the min-air datum (concurrent vent,
thrust, ballast) UNKNOWN; transient response NOT established. Heel on the state pendulums (state
gross × 25 m): **0.16°** at the mismatch bound, **2.99°** one-bay-empty (rigid hull; envelope heel
limit UNKNOWN, I006).

- **Release law (declared, no free simultaneity):** orifice drain is sqrt-head, front-loaded; the
  BOUND is linear over ~9 min with rate mismatch ±5 %, door opening ≤ 5 s, pair start skew ≤ 2 s —
  no free perfect simultaneous release. **Valve spec UNQUALIFIED** (matched orifices are a declared
  tolerance, not a purchased spec).
- **Finite trim:** countering the 18.7 t·m mismatch pitch needs **0.448 t** of air shifted over the
  50 m ballonet lever **net of the 0.164045 mixture fraction** (18.7/50/(1 − 0.164045) — the
  earlier /50 figure understated the transfer; it is additionally bounded by the receiving bag's
  headroom, inherited) → **27 s at the declared 1.0 t/min** (drain ~9 min; fan energy falls under
  the corrected-I012 **partial** budget — 3.92 MJ per t at 1.5 kPa/40 % covers the LISTED subset
  only, reset-air and other work UNKNOWN; closure UNKNOWN). **Static capacity shown, transient
  control NOT proven** (fan capability, gust coupling, slosh unmodelled).

## Carried envelope and economics (unchanged, restated)

Zero-slack fuel: 4.902246 t buys exactly 6.00 h with the 0.204260 t reserve; +33 min → **0.245112 t
short**; −50 % pump (scoop 50.9 t alone 84.831242 min, coupled 85.756228 min, base 6.429270 h) →
**0.350732 t short**; both **fuel FAIL**, covering priced not taken. Economics: 8.36 t He =
49,411 m³ STP per 100 t → **$5,929/t at the USGS base = 35.1× the $169/t SEAT comparator**
(sign-reversal $0.34/m³) — **retained FAIL**, unchanged by the drawn set (dry mass cancels from the
neutral vent).

## Sensitivity (margin at max inventory, +9.80 t)

| Line | Δ t | margin t |
|---|---|---|
| fitout/valves/doors +50 % (declared lines) | −0.34 | +9.46 |
| curtain planes actually at ±10 (delta reverses) | −1.68 | +8.13 |
| curtain misaligned ±3.5 m (spreader 10.5 m ×2) | −2.33 | +7.47 |
| plate 3 → 5 mm (handling/corrosion doubling) | −1.15 | +8.65 |
| occupancy/bag fit (withdrawn) | — | UNKNOWN (not a mass line) |
| I007 sundries +50 % (carried) | −9.82 | **−0.02 (breaks it)** |
| endurance 6 → 12 h (carried) | −4.90 | +4.90 |
| lift on 217,547 m³ not the anchor (DRAWN-VOLUME) | −1.96 | +7.84 |

**DRAWN-VOLUME, named explicitly:** every lift above uses the recorded **220,000 m³ anchor**; the
drawn capsule is **217,547 m³ (−1.1 %)**. Mixture lift is hull-independent (lift = n × 1.02404 t per
km³), so **n0, the 50,940 m³ vent and the 50.9 t scoop do NOT change** on the capsule; what changes
is the ceiling — max inventory 169,935 m³ → max lift 174.02 t (**−1.96 t vs anchor**) — and the SL
floor drops to 107,547 m³, which n1 clears by 3,791 m³ (MORE than the anchor's 1,338 — the cap, not
the hull volume, binds). Displacement is not silently added: the geometric-volume sensitivity alone
consumes 1.96 t of margin.

## Verdict

- **GEOMETRY/OCCUPANCY: fit UNKNOWN (ideal-volume convention).** Drawn tanks 3.05 × 3.05 × 2.85 m
  (usable 25.7 m³ ≥ 25.0) at x = ±14, y = ±11, upper row z = −19.0 / lower z = −21.5 (diagonal,
  each pair at one height); worst radial skin clearance 1.38 m; corridors and gondola clearances
  stated; the bag-plane fit demonstration is **WITHDRAWN** (the earlier z = −3.1 m plane /
  14.1 m separation / 26.3 m sufficient-span bound used the full midbody circle into the caps —
  ~17.6 m of each declared 40 m bag sits in the smaller hemispherical-cap sections); every volume
  here is an ideal-unobstructed-volume bound; physical disjoint occupancy, membrane shape/drape and
  the I006/I010 interfaces UNKNOWN.
- **LOAD PATH: priced under the SIMPLIFIED SCALAR BEAM model.** 6.00 t vs I012's 9.20 t allowance
  (−3.20 t); member stock 1.68 t total is the simplified-beam quantity — the earlier claim that the
  ±14 stations **derive 1.68 t of station saving** vs the fixed ±10 arrangement is **withdrawn** (a
  derived difference needs member statics under the same declared method at both arrangements, not
  the scalar simplification); member M/S shown for full/mismatch/one-empty under the simplification;
  **envelope/curtain attachment qualification and bonds UNRESOLVED**.
- **TRIM: nominal zero-moment preserved; coverage per state** under the twice-corrected
  one-direction law bounded by donor inventory AND receiver headroom — mismatch 18.7 t·m covered at
  its datum (651 t·m), one-bay-empty 350 t·m covered at the neutral one-empty datum (922) but
  **exceeding the min-air bound (245)** — recovery there UNKNOWN, transient control NOT proven;
  finite response 27 s (0.45 t netted transfer) vs 9 min drain at the DECLARED fan rate;
  quasi-static only.
- **MASS/MARGIN: DRY 66.18 t, margin +9.80 t** (I012 +6.60); the lighter set **trades** floor
  clearance (1,338 m³, was 4,463) and cap margin (0.6 %, was 2.0 %); the crossover to a floor-bound
  vent sits at DRY = 64.81 t — a drawn set under 4.63 t (ours is 6.00 t).
- **ECONOMICS/FUEL (carried, retained):** vent 8.36 t He (dry-independent), **35.1× SEAT FAIL**;
  zero-slack envelope, both off-nominal cases fuel FAIL (0.245112 / 0.350732 t short).

**Weakest assumption:** the declared curtain-plane stations (R3-I003 carries the suspension as an
undrawn 3 t allowance) — the saddle load path hangs on them and the member stock here is
scalar-beam only. **Next geometry change (one):** draw the curtain fan itself — station spacing,
run angles and fitting loads from the envelope seam pattern — which converts the member statics and
the attachment UNKNOWN into a drawn interface, then re-run the bag occupancy at the real ballonet
gore count.

Carried unresolved: envelope/curtain attachment qualification and bonds UNKNOWN; valve spec
UNQUALIFIED; bag shape/membrane drape UNKNOWN (**occupancy UNKNOWN** — the conditional envelope
withdrawn); flat-panel tank adequacy UNKNOWN (3 mm selected stock); one-bay-empty trim recovery at
the minimum-air datum UNKNOWN; transient control unproven; transition-energy closure UNKNOWN
(partial listed-subset budget, twice-corrected I012); R3-I006/R3-I010 do not establish P-100
interfaces.

## Scoreboard

> Drawn 4-bay P-100 kit at +/-14 m stations: 6.00 t from quantities, margin +9.80 t, occupancy UNKNOWN (envelope withdrawn), attachment UNKNOWN; economics FAIL 35.1x SEAT.

(169 characters.) Conditional paper result on an assumed-basis hull with declared (±50 %) fittings
and an undrawn curtain fan: not a measured or drawn-structure vehicle, and no public claim is made.
