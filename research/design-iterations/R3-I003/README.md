# R3-I003 — an independent challenge to the vacuum-only architecture

Status: design iteration, 2026-10-13, under the float redirect (ord-boyce-co-robotics-float-confidently-1013
via ord-spock-r3-glm-a-start-1013). Internal, conditional design hypothesis pending applicable claim review;
no positive public claim is made here. No aircraft has been built or flown. Every number below is either
copied from a recorded source, computed by [`budget.py`](budget.py) (deterministic, stdlib only), or labelled
assumed / UNKNOWN. Not a drawn structure: no seam detail, load path or joint is designed.

## The question

The recorded architecture evacuates the hull and pays a crush structure. The recorded shortfall is the
structure: the [float ledger](../../../docs/FLOAT-LEDGER.md) has every 52 m vacuum row negative at sea level
(best honest: 229.2 t against 224.8 t of lift, −4.3 t), and the [mass budget](../../analysis/mass-budget.md)
puts the P-100 shell alone at 111.8–255.2 t against a whole-vehicle budget of ~210 t at working altitude.
This unit asks the complementary question, which no recorded row answers: **what does the same mission look
like with lifting gas at ambient pressure — a conventional gas-supported hull — and does any partial-vacuum
hybrid between the two pay?**

## Recorded baseline (copied, afb2c2d1)

| Row | Value | Source |
|---|---|---|
| P-100 class: displacement, length × diameter | 220,000 m³, 110 × 55 m | `sim/config.js`, `mass-budget.json` |
| P-100 hull surface | 19,007 m² | `mass-budget.json` |
| P-100 payload allowance | 100 t | `mass-budget.json` |
| Lift at working altitude 2,500 m (vacuum basis, = air displaced) | 210.5 t | `mass-budget.json` |
| Vacuum shell, floor / credible / demonstrated | 111.8 / 165.0 / 255.2 t | `mass-budget.json` P100 cases |
| Equipment ex-shell, floor / credible / demonstrated | 103.5 / 293.2 / 787.5 t | same lines, shell and barrier removed |
| Modelled lattice density, level 1 / level 2 | 1.306 / 1.124 kg/m³ | [vacuum-cell analysis](../../analysis/vacuum-cell.md) |
| Best modelled level-2 margin at 2,500 m | 0.851 lift/mass — sinks | same |

Air anchors, the programme's own: 1.2250 kg/m³ sea level, 0.9569 kg/m³ at 2,500 m. Molar-mass lift factors
computed, not remembered: He/air 0.13819, H₂/air 0.06960.

## Option A — gas-supported P-100 (helium, non-rigid)

Same volume, same payload target, same recorded equipment evidence classes. The hull is a pressure-stabilised
capsule instead of a crush structure.

**Design definition.**

- **Geometry:** capsule 110 × 55 m (as the P-100 class), 19,007 m² hull surface.
- **Envelope material:** helium-quality laminate, assumed 0.45 kg/m² nominal (range 0.35–0.65; UNKNOWN, no
  coupon — modern large-airship hull laminates span this range). The barrier is the envelope itself; no
  separate film line. Stress check: membrane tension is p·r/2 = 6.9–13.8 kN/m across the 500–1,000 Pa band,
  at least an order below a hull laminate's working strength, so areal density (tear, handling, seams), not
  stress, sizes the fabric. The vacuum concept's barrier pricing (a film holding a full atmosphere over 2 m
  spans) does not apply at kPa gauge.
- **Gas:** helium at 97 % purity assumed (initial fill, declining in service; sensitivity below). Hydrogen
  would add 17.9 t of lift at this scale but is rejected as the default for wildfire operations; that is an
  internal default, revisable.
- **Pressure schedule:** superpressure 500 Pa nominal, 250–1,000 Pa band; two ballonets at 25 % volume each
  (50 % total — generous against the 21.9 % expansion to 2,500 m, kept for trim authority). Ballonet fabric
  assumed 0.30 kg/m², sphere-equivalent area basis.
- **Seams and fittings (allowances, undrawn):** lapped adhesive seams at assumed 85 % joint efficiency
  (UNKNOWN — coupon needed); suspension septum and catenary curtain 3 t; nose reinforcement and mooring
  fitting 1 t; fins with actuators 3 t; gondola and systems 4 t.

**Component mass budget.**

| Line | Tonnes | Basis |
|---|---:|---|
| Envelope laminate | 8.55 | 19,007 m² × 0.45 kg/m², assumed |
| Ballonets 2 × 25 % | 4.20 | sphere-equivalent 13,988 m² × 0.30 kg/m², assumed |
| Suspension / septum | 3.00 | allowance, undrawn |
| Nose + mooring | 1.00 | allowance, undrawn |
| Fins + actuators | 3.00 | allowance, undrawn |
| Gondola + systems | 4.00 | allowance, undrawn |
| **Gas hull total** | **23.75** | fabric range makes it 21.85–27.55 t |
| Recorded equipment (floor / credible / demonstrated) | 103.5 / 293.2 / 787.5 | `mass-budget.json`, unchanged |
| *vs* recorded vacuum shell + barrier | 112.6 / 173.2 / 320.8 t | replaced by the gas hull |

**Lift budget and margins** (helium, 97 % purity: net 1.0240 kg/m³ sea level, 0.7999 kg/m³ at 2,500 m;
lift 225.3 t and 176.0 t; payload target 100 t).

| Vehicle | Mass | Margin, sea level | Margin, 2,500 m |
|---|---:|---:|---:|
| Float-only systems (envelope + minimal power/avionics) | 30.2 t | **+195.0 t** | +145.7 t |
| Mission, floor equipment | 127.2 t | **+98.0 t** | **+48.7 t** |
| Mission, credible equipment | 316.9 t | −91.7 t | −141.0 t |
| Mission, demonstrated equipment | 811.2 t | −586.0 t | −635.3 t |

At the floor evidence class the gas P-100 carries the full 100 t payload at sea level with 98 t of reserve,
and 48.7 t of payload margin at 2,500 m. At the credible equipment class it does not close — see the weakest
assumption. The float question itself is not close: the float-only vehicle's margin is 6–9× the entire gas
hull mass.

## Option B — partial-vacuum hybrid: closed

Reducing internal pressure by a fraction *f* below ambient (helium remaining inside) adds lift
ΔL = *f* × (displaced helium mass) = at most **36.1 t** at *f* = 1, P-100, sea level, 97 % purity. The shell
differential is *f* × 101.3 kPa, and buckling-governed shell mass scales as Δp^⅔ (the
[vacuum-cell analysis](../../analysis/vacuum-cell.md) own correction), so mass(*f*) = M_vac·*f*^⅔ and the
ratio of structure to gain is ratio(1)·*f*^−⅓ — monotonically at least its full-vacuum value. That value is:

| Shell | Mass / gain at *f* = 1 |
|---|---:|
| Recorded floor (Jenett basis, 0.508 kg/m³) | 3.09× |
| Recorded credible | 4.57× |
| Recorded demonstrated | 7.06× |
| Modelled level-1 lattice | 7.95× |
| Modelled level-2 hierarchy | 6.85× |

**No vacuum fraction pays for any recorded or modelled shell.** A crossover would need a full-vacuum shell
at ≤ 36.1 t = 0.164 kg/m³ — 3.1× below the best recorded bound and 6.8× below the best modelled lattice.
This closes the partial-vacuum hybrid family at P-100 scale for lattice shells in the recorded material
class, and it is independent of scale for buckling-similar architectures (the ratio is a material-and-form
number). The recorded graded-band and pumped-plenum tables reach the same verdict from the vacuum side.

## Demonstrator and mission are different vehicles

- **Minimum demonstrator:** 24 × 48 m capsule, 18,096 m³, envelope 1.63 t + ballonets 0.33 t + kit 1.5 t
  against 18.53 t of lift — floats with +15.1 t at sea level. It proves the gas-side bench questions this
  programme has not yet asked: seam and barrier coupons at kPa gauge, ballonet and valve schedule,
  superpressure control, permeation rate. The vacuum programme's E5 coupon tests lattice joints; the gas
  path needs none of those and its own instead.
- **Mission airship:** the P-100 rows above. The recorded equipment set (cryo plant, LN₂, battery bus,
  rotors) belongs to the vacuum concept's buoyancy-control philosophy; a gas ship trims with ballonets and
  vents or adds helium, so the cryo + LN₂ lines (19.8–413.2 t across the three evidence classes) are a
  descope lever, not a requirement. That descope is the next unit's arithmetic, not a credit taken here.

## Sensitivity and the expert ledger

Base: mission at floor equipment, sea level, margin +98.0 t.

| Change | Δ margin | Resulting margin |
|---|---:|---:|
| Helium purity 97 → 95 % | −4.6 t | +93.4 t |
| Fabric 0.45 → 0.65 kg/m² | −3.8 t | +94.2 t |
| Superpressure 500 → 1,000 Pa | −0.2 t | +97.9 t |
| Sea level → 2,500 m | −49.3 t | +48.7 t |
| Equipment floor → credible | −189.7 t | −91.7 t |
| Hydrogen instead of helium | +17.9 t | +116.0 t |

| Assumption (expert ledger) | Why it matters | If wrong |
|---|---|---|
| Envelope areal density 0.45 kg/m² (UNKNOWN, no coupon) | the one new mass line this design adds | ±0.2 kg/m² → ∓3.8 t; cannot reverse float |
| Helium purity 97 % (assumed ops value) | air ingress cuts lift directly | −2 % → −4.6 t |
| Seam efficiency 85 % (UNKNOWN, undrawn) | seam-adjacent fabric mass and inspection | within the fabric range above |
| Suspension/fitting allowances 3+1+3+4 t (undrawn) | detail design grows, never shrinks | ±50 % → ±5.5 t |
| Equipment evidence class (recorded) | floor closes, credible does not | the mission decider, −189.7 t between them |
| Icing and water-ops allowance (UNKNOWN, not budgeted) | firefighting environment | could add tonnes; unpriced |
| Altitude requirement 2,500 m (programme anchor) | each 100 m ≈ −2 t at P-100 | linear in the miss |

## Weakest assumption, and the next change

**The equipment evidence class, not the hull.** The hull question this unit was assigned is answered with
room to spare: gas support replaces a 112–321 t crush structure with a 22–28 t envelope at a cost of 13.8 %
of gross lift, and no partial-vacuum hybrid between them pays. The mission closure now turns entirely on the
recorded equipment spread — floor closes with 98 t of sea-level reserve, credible misses by 92 t — whose
widest swings (cryo 12→120→390 t, sundries 20→61→185 t) are priced "NO SOURCE" in the recorded evidence.

**Next concrete design change:** re-price the P-100 equipment set for a gas ship — drop the cryogenic plant
and LN₂ tankage (buoyancy control passes to ballonets and helium management), and price a diesel-electric
propulsion and water-delivery set at quote-backed values or UNKNOWN per the programme's rules. Arithmetic
bound on the effect: the credible-class vehicle loses 132.4 t with those two lines dropped, which takes its
sea-level margin from −91.7 t to +40.8 t and its 2,500 m margin to −8.5 t — sea level closes, the working
altitude does not yet, so the remainder must come from the sundries and battery spreads. Second change:
freeze the envelope laminate specification and obtain a coupon measurement (areal density, seam strength,
helium permeation) to move the one genuinely new assumed line off UNKNOWN.

## Scoreboard

> Paper, gas-envelope P-100 with floor-kit: floats, +98 t SL / +49 t @2500 m; credible kit −92 t SL; confidence low-medium; decisive assumption: equipment case class, not the hull.

(178 characters.) This moves the scoreboard from `not shown` to a conditional paper YES for the gas
architecture; it is not a measured or drawn vehicle and makes no public claim.
