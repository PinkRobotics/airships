# R3-I003 — an independent challenge to the vacuum-only architecture

Status: design iteration, 2026-10-13, **corrected 2026-10-14** per the recorded correction disposition
(lead intake found the 100 t mission payload printed but absent from every vehicle case, and a hybrid model
that removed only the helium constituent of the 97/3 mixture; both are fixed here and the failure history is
carried in the unit evidence file). Under the float redirect (ord-boyce-co-robotics-float-confidently-1013
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

The equipment lines include water tanks and plumbing, **not** the 100 t of water itself — payload is carried
as a separate line below and enters every mission case. Air anchors, the programme's own: 1.2250 kg/m³ sea
level, 0.9569 kg/m³ at 2,500 m. Molar-mass lift factors computed, not remembered: He/air 0.13819, H₂/air
0.06960.

## Option A — gas-supported P-100 (helium, non-rigid)

Same volume, same payload target, same recorded equipment evidence classes. The hull is a pressure-stabilised
capsule instead of a crush structure.

**Design definition.**

- **Geometry:** capsule 110 × 55 m (as the P-100 class), 19,007 m² hull surface.
- **Envelope material:** helium-quality laminate, assumed 0.45 kg/m² nominal (range 0.35–0.65; UNKNOWN, no
  coupon — modern large-airship hull laminates span this range). The barrier is the envelope itself; no
  separate film line. Membrane loading, derived from equilibrium and labelled by direction: in the closed
  cylindrical section the hoop resultant is N = p·r = 13.75 kN/m at 500 Pa gauge (27.50 kN/m at 1,000 Pa)
  and the axial resultant is N = p·r/2 = 6.88 / 13.75 kN/m at the 27.5 m class radius; dished end caps are
  approximately spherical, ~p·r_cap/2 in both directions. Laminate working line-strength and seam reduction
  are UNKNOWN (no coupon exists), so **no strength margin is asserted** — fabric sizing rests on the assumed
  areal density alone, and the previously printed "an order below working strength" claim is withdrawn. The
  vacuum concept's barrier pricing (a film holding a full atmosphere over 2 m spans) still does not apply at
  kPa gauge.
- **Gas:** a 97 % He / 3 % air mixture by volume (assumed initial fill, declining in service; sensitivity
  below). The mixture-to-air density ratio is 0.164045 — the contaminant air is carried in every lift figure
  below, not just the helium. Hydrogen would add +17.9 t at sea level / +14.0 t at 2,500 m but is rejected as
  the default for wildfire operations; that is an internal default, revisable.
- **Pressure and ballonet schedule (nominal paper schedule, next section):** design point at 2,500 m with
  the mixture filling the hull and ballonets empty; at sea level the same inventory leaves 21.9 % ballonet
  occupancy. Installed ballonet capacity is 50 % (two at 25 % volume each, 0.30 kg/m² assumed fabric,
  sphere-equivalent area basis) — capacity and occupancy are different numbers and both are stated. Main
  tables are zero-gauge; the nominal 500 Pa superpressure is a labelled sensitivity (−0.22 t at the design
  point).
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

## Gas inventory, ballonet schedule, and the two sea-level bounds

Full-hull helium figures at both altitudes are separate static bounds unless a connected schedule is stated;
this is the nominal paper schedule (isothermal atmosphere assumed — P at 2,500 m = 79,149 Pa = 0.7811 × sea
level; a lapse-rate refinement is UNKNOWN):

- **Design point, 2,500 m:** the 97/3 mixture fills the hull (220,000 m³), ballonets empty. Mixture mass
  34.53 t, net lift **175.98 t**.
- **Same inventory at sea level, no venting:** the mixture occupies 171,851 m³ (78.1 % of the hull) and the
  ballonets hold 48,149 m³ = **58.98 t of air** (occupancy 21.9 % of hull volume against 50 % installed
  capacity). Ballonet air is budgeted exactly once, here: it is ambient air in ambient air and contributes
  zero net lift, so net lift at sea level is **175.98 t**, equal to the design point — the constant-inventory
  property that makes a ballonet airship a fixed-lift vehicle between fillings.
- **Sea-level full-hull bound (first departure, or helium topped up at base):** net lift **225.29 t** with
  the ballonets empty — no sea-level trim authority. Climbing to 2,500 m must vent 61,639 m³ = 9.68 t of
  mixture, irreversible per cycle; base helium logistics UNKNOWN. After any climb-descent cycle the
  recoverable sea-level state is the no-vent state unless helium is re-added.

## Lift budget and margins — payload included

| Case | Dry vehicle | Payload | Margin, 2,500 m | Margin, SL full-hull | Margin, SL no-vent |
|---|---:|---:|---:|---:|---:|
| Float-only systems | 30.2 t | — | **+145.7 t** | +195.0 t | +145.7 t |
| Mission, floor equipment | 127.2 t | 100.0 t | **−51.3 t** | −1.96 t | −51.3 t |
| Mission, credible equipment | 317.0 t | 100.0 t | −241.0 t | −191.7 t | −241.0 t |
| Mission, demonstrated equipment | 811.2 t | 100.0 t | −735.3 t | −686.0 t | −735.3 t |

With the 100 t mission payload included, **the mission does not close at any recorded equipment class.**
Floor equipment misses by 51.27 t at the 2,500 m design point and at the recoverable sea-level state; only
the first-departure full-hull bound comes within 1.96 t of sea-level closure, and that bound spends the
ballonets' trim authority and 9.68 t of helium per climb. The previous tip's +98.0 / +48.7 t were available
lift *before* payload, not reserves after it — corrected here. The float-only row is a payload-free float
bound, not a mission success.

## Option B — partial-vacuum hybrid: closed (full-mixture model)

Model, stated once and used consistently: the hull gas is the uniform 97/3 mixture; reducing internal
pressure by a fraction *f* removes **both constituents in proportion** (a hard vacuum does not selectively
keep the contaminant air), and the remaining (1−*f*) gas keeps 97/3 proportions. The lift gain is
ΔL = *f* × **44.21 t** at *f* = 1, P-100, sea level — the full mixture mass, not the 36.1 t of displaced
helium the previous tip counted; that figure is superseded. The shell differential is *f* × 101.3 kPa, and
buckling-governed shell mass scales as Δp^⅔ (the [vacuum-cell analysis](../../analysis/vacuum-cell.md) own
correction), so mass(*f*) = M_vac·*f*^⅔ and the ratio of structure to gain is ratio(1)·*f*^−⅓ —
monotonically at least its full-vacuum value. That value is:

| Shell | Mass / gain at *f* = 1 |
|---|---:|
| Recorded floor (Jenett basis, 0.508 kg/m³) | 2.53× |
| Recorded credible | 3.73× |
| Recorded demonstrated | 5.77× |
| Modelled level-1 lattice | 6.50× |
| Modelled level-2 hierarchy | 5.59× |

**No vacuum fraction pays for any recorded or modelled shell, under this one stated model.** A crossover
would need a full-vacuum shell at ≤ 44.21 t = 0.200955 kg/m³ — 2.53× below the best recorded bound and
5.59× below the best modelled lattice. This closes the partial-vacuum hybrid family at P-100 scale for
lattice shells in the recorded material class, and it is independent of scale for buckling-similar
architectures (the ratio is a material-and-form number). The recorded graded-band and pumped-plenum tables
reach the same verdict from the vacuum side.

## Demonstrator and mission are different vehicles

- **Minimum demonstrator:** 24 × 48 m capsule, 18,096 m³, envelope 1.63 t + ballonets 0.33 t + kit 1.5 t
  against 18.53 t of lift — a payload-free static bound at sea level, +15.08 t; no altitude schedule is
  claimed at this scale. It proves the gas-side bench questions this programme has not yet asked: seam and
  barrier coupons at kPa gauge, ballonet and valve schedule, superpressure control, permeation rate. The
  vacuum programme's E5 coupon tests lattice joints; the gas path needs none of those and its own instead.
- **Mission airship:** the P-100 rows above. The recorded equipment set (cryo plant, LN₂, battery bus,
  rotors) belongs to the vacuum concept's buoyancy-control philosophy; a gas ship trims with ballonets and
  vents or adds helium. The descope lever (cryo + LN₂, 132.4 t at the credible class) is the next unit's
  arithmetic, not a credit here — and it no longer implies closure: dropping those two lines alone leaves
  the credible-class mission at −59.3 t sea level (full-hull bound) / −108.6 t at 2,500 m, with the required
  replacement trim and control equipment still unpriced (UNKNOWN).

## Sensitivity and the expert ledger

Base: mission at floor equipment, design point 2,500 m, payload included, margin −51.27 t.

| Change | Δ margin | Resulting margin |
|---|---:|---:|
| Helium purity 97 → 95 % | −3.63 t | −54.89 t |
| Fabric 0.45 → 0.65 kg/m² | −3.80 t | −55.07 t |
| Superpressure 0 → 500 Pa | −0.22 t | −51.48 t |
| Equipment floor → credible | −189.70 t | −240.97 t |
| Hydrogen instead of helium | +14.01 t | −37.26 t |
| Sea-level full-hull bound instead of design point | +49.31 t | −1.96 t |

| Assumption (expert ledger) | Why it matters | If wrong |
|---|---|---|
| Envelope areal density 0.45 kg/m² (UNKNOWN, no coupon) | the one new mass line this design adds | ±0.2 kg/m² → ∓3.8 t; cannot alone reverse the miss |
| Helium purity 97 % (assumed ops value) | air ingress cuts lift directly | −2 % → −3.6 t |
| Seam efficiency 85 % (UNKNOWN, undrawn) | seam-adjacent fabric mass and inspection | within the fabric range above |
| Suspension/fitting allowances 3+1+3+4 t (undrawn) | detail design grows, never shrinks | ±50 % → ±5.5 t |
| Equipment evidence class (recorded) | floor misses by 51.3 t at the design point, credible by 241 t | the mission decider, −189.7 t between classes |
| Gas schedule policy (nominal paper) | the SL full-hull bound buys +49.3 t but vents 9.68 t per climb and carries no SL trim authority | ops profile UNKNOWN; bound is a policy, not a free margin |
| Isothermal atmosphere (schedule assumption) | sets the 78.1 % / 21.9 % SL split and the 9.68 t vent | lapse rate shifts it slightly; refinement UNKNOWN |
| Icing and water-ops allowance (UNKNOWN, not budgeted) | firefighting environment | could add tonnes; unpriced |

## Weakest assumption, and the next change

**The equipment evidence class and the gas schedule policy, not the hull.** The hull question this unit was
assigned is answered with room to spare: gas support replaces a 112.6–320.8 t shell + barrier with a
21.9–27.6 t envelope at a 16.40 % gross-lift concession (the mixture mass fraction of displaced air,
altitude-independent), and no partial-vacuum hybrid between them pays (≥ 2.53× at every vacuum fraction).
But with the 100 t payload included, the mission misses at every recorded equipment class — by 51.3 t at
the floor class design point — so the gas architecture is a live hull option, not a closed mission.

**Next concrete design change:** re-price the P-100 equipment set for a gas ship — drop the cryogenic plant
and LN₂ tankage (buoyancy control passes to ballonets and helium management) **and price the required
replacement trim/control equipment in**; a diesel-electric propulsion and water-delivery set at quote-backed
values or UNKNOWN per the programme's rules. The cryo + LN₂ drop alone (−132.4 t, credible class) leaves
−59.3 t at the full-hull sea-level bound and −108.6 t at 2,500 m, so the remainder must come from the
sundries and battery spreads. Second change: freeze the envelope laminate specification and obtain a coupon
measurement (areal density, seam strength, helium permeation) to move the one genuinely new assumed line —
and the withdrawn strength question — off UNKNOWN. Third: fix the mission ops profile (altitude cycling,
water drops, helium replenishment) so the sea-level bound is a measured state rather than a policy choice.

## Scoreboard

> Paper P-100 gas hull: no mission float — floor kit −2 t SL bound / −51 t @2500 m with 100 t payload; payload-free +146 t; hybrid closed; decisive: equipment class + gas schedule.

(178 characters.) The previous tip's scoreboard claimed a floor-class float by omitting the payload; it is
withdrawn. This is a conditional paper result on an assumed-basis hull: not a measured or drawn vehicle, and
no public claim is made.
