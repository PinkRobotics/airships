# Status against today’s model

**Disposition: LAND IN PART — retain the joint requirement and correct the published mass comparison.**
The report's contradiction of FLOAT's 19.5% is reproduced. Current `stock_build()` gives
0.715 / 1.948 = **36.704%**, replacing the report's 29.916% on the old 2.390 kg tube bill.
The 15% allowance is now **0.2922 kg**, requiring a **59.13%** reduction from the present
computed node set, instead of the report's 0.3585 kg / 49.86%. These are integrated geometry
and arithmetic, not weighed joints.

`member_demands(0.709)` still reproduces the five reported force magnitudes, including
5,037.667 N for the in-plane tie. The R1 section choices below predate film-bending sizing:
today's subdivision tool gives 10.76–12.51 kg/m³ in its publication rows. Its higher-order
candidate prices and the old 2.0 m / n=2 comparison are historical scenarios, not current
designs. No complete-node capacity or procurement claim was independently qualified here.
The survey's external supplier availability was not refreshed.

**Reproduction:** `python3 tools/float_ledger.py`; `python3 tools/subdivision_study.py`;
read-only calls to `stock_build()` and `member_demands(0.709)` in
`research/analysis/vacuum-cell.py`. The body states every historical sensitivity formula.

## Dated audit record

The text below records what was claimed on its audit date. “Today” in that text means that date. Only the reproductions above are current; historical numbers and review-era paths are preserved as evidence, not revalidated claims. See [the float ledger](../FLOAT-LEDGER.md).

---

# What is the lightest joint that transfers 3–7 kN between carbon-tube ends?

**Date:** 2026-08-12

**Object 1:** article A as generated, square-face span 0.709 m, subdivision `n=1`,
51 nodes and 216 members (432 member-ends), 10×8 mm main tube and 14×12 mm rim tube.

**Object 2:** the standalone R1 load-band comparison, span 2.0 m, subdivision `n=2`, 201 nodes and
948 octet members, using the study's selected 16.5×0.40 mm tube. This is not the built
article. It is the `n=2` object whose 6.717 kN member demand and approximately 16 mm bore
make it comparable to the question asked. Holding article A's 0.709 m span while changing
to `n=2` gives 0.844 kN and selects 5.0×0.25 mm: a read-only call to
`subdivision_study.strut_force(0.709,2)` gives 844.12 N and
`best_article(0.709,2)` selects that tube. It is outside the requested 3–7 kN band.
“Standalone” here specifies the complete 948-member/201-node **mass allocation**, not a
complete standalone structural load case: the 6.717 kN is the array-crush demand, while
general-`n` face-member film bending and other boundary demands remain uncomputed. Every
`n=2` candidate price is therefore a structural floor/sensitivity, not a sized design.

**Scope:** findings only. No model, generator, manifest, contract, tolerance, margin, or
frozen baseline was changed.

## Answer first

There is no proved lightest joint yet. The standard engineering answer is not a solid
many-arm printed hub: it is usually a **bonded, tapered socket/end-fitting that spreads
load into the composite tube wall**, followed by a pin or compact node if rotation is
intended, or by a moulded/laminated central node if moment transfer is intended. Internal
ferrules, external sleeves, scarf/double-lap joints, moulded composite end fittings and
bonded metallic inserts are variations of that same load-spreading mechanism.

No buyable fitting found in the 10–16 mm band carries a published complete-node mass *and*
a 3–7 kN rating. Tent, kite and mast ferrules are light but unrated at this demand; drone
clamps are light but are clamp halves, not multi-arm structural nodes; building space-frame
nodes are rated but start far above this bore and mass scale. Aerospace bonded end fittings
are the only mechanism supported by relevant qualification practice, and they are made to
order.

The node-corrected mass result is also harsher than FLOAT's pre-correction R2 prose:

- FLOAT's node-corrected but P14-stale model-billed article A, 0.709 m, `n=1` subtotal is
  **3.13 kg = about 17.6 kg/m³ = 18.4× the 0.9569 kg/m³ wall**; its joint line is the
  0.715 kg used here. The unresolved 2.390 kg tube line still bills nominal rather than live
  cuts, so these are the required corrected R2 comparison figures, not a reconciled production BOM.
- article A, 0.709 m, `n=1`: measured printed nodes are **0.715 kg = 4.012 kg/m³**, or
  **29.9% of the 2.390 kg tube mass**. The published 19.5% was
  `0.465/2.390`; it predates the 0.465→0.715 kg correction. The 15% target is 0.3585 kg,
  so this object needs at least a **49.9% node-mass reduction**.
- standalone R1 comparison, 2.0 m, `n=2`: correcting the study's stale 0.465 kg node basis
  gives **12.659 kg of nodes = 3.165 kg/m³**. Charging all 948 physical struts gives
  **10.850 kg of tube**, so nodes are **116.7%** of tube mass. The 15% target is
  1.627 kg = 0.407 kg/m³, so this object needs at least an **87.1% node-mass reduction**.

The only priced screen below the `n=2` 15% line is the bonded composite no-hub **material
sensitivity scenario**, 0.299 kg/m³ versus the 0.407 kg/m³ target. It omits the mass that redistributes
loads among the arms and is therefore not a complete design or an achievable checked
number. The lightest observed geometry remains today's solid 0.715 kg node set, and even
it is structurally `NOT PROVEN`. Accordingly: **no candidate is proved to transfer the
required loads, and no candidate is proved to meet the 15% target.**

---

# 1. The requirement, before the design

## 1.1 Axial demand by member family

These are repository-tool results for **article A, span 0.709 m, `n=1`**.
`research/analysis/vacuum-cell.py:member_demands(0.709)` includes the model's safety factor
of 1.5 once. They are sizing envelopes, not one closing equilibrium solution: the live
assembly certificate reports a 7,868 N maximum node residual because array crush and the
standalone-film envelopes are deliberately combined conservatively.

| member family | factored axial magnitude | source/load path |
|---|---:|---|
| octet | 3,376.49 N | infinite-array hydrostatic crush, `3p SF V/(96a)` |
| spoke | 2,238.32 N | hexagon film's in-plane radial tributary |
| rim | 4,476.63 N | two-hexagon hoop envelope; no octet crush share |
| tripod prop / inward vertex tie | 4,775.08 N | factored normal film reaction, `p SF a²/2` |
| in-plane square tie | 5,037.67 N | square normal share plus in-plane radial tributary |

The required per-family interface disposition is explicit below. `NOT PROVED` means the
repository emits a screen but has no licensed capacity; `NOT COMPUTABLE` means the required
criterion or load is absent. End-class counts come from the 432 live contract rows for
**article A, span 0.709 m, `n=1`**.

| member family | end classes | bearing | pull-out | bond shear | actual end bending |
|---|---|---|---|---|---|
| octet, 3,376.49 N | 36 tree, 84 closing | tree **NOT PROVED**; closing **NOT COMPUTABLE** (adhesive butt) | **NOT PROVED**; no qualified tension path | **NOT COMPUTABLE**; no qualified adhesive/system allowable | **NOT COMPUTABLE**; no licensed `M-θ` demand |
| spoke, 2,238.32 N | 96 closing | **NOT COMPUTABLE** (adhesive butt) | **NOT PROVED**; no qualified tension path | **NOT COMPUTABLE**; no qualified adhesive/system allowable | **NOT COMPUTABLE**; no licensed `M-θ` demand |
| rim, 4,476.63 N | 72 closing | **NOT COMPUTABLE** (adhesive butt; rim field probe also wrong-SKU) | **NOT PROVED**; wrong-SKU rim values | **NOT COMPUTABLE**; no qualified allowable and wrong-SKU rim area | **NOT COMPUTABLE**; no licensed `M-θ` demand |
| tripod prop / inward vertex tie, 4,775.08 N | prop: 16 tree, 32 closing; inward: 24 tree, 24 closing | tree **NOT PROVED**; closing **NOT COMPUTABLE** (adhesive butt) | **NOT PROVED**; no qualified tension path | **NOT COMPUTABLE**; no qualified adhesive/system allowable | **NOT COMPUTABLE**; no licensed `M-θ` demand |
| in-plane square tie, 5,037.67 N | 24 tree, 24 closing | tree **NOT PROVED**; closing **NOT COMPUTABLE** (adhesive butt) | **NOT PROVED**; no qualified tension path | **NOT COMPUTABLE**; no qualified adhesive/system allowable | **NOT COMPUTABLE**; no licensed `M-θ` demand |

The connection requirement is not merely “hold 5 kN axially.” At each tube end it must
provide a traceable path through tube wall, adhesive/contact, fitting and node for:

1. axial compression without crushing or splitting the tube end;
2. axial tension without pull-out;
3. bond shear and peel over a controlled bondline;
4. transverse end shear from the film-loaded members;
5. the actual end moment and rotation; and
6. combined `N-V-M`, duration, creep, moisture and manufacturing eccentricity.

## 1.2 The bending and shear that reach the end

`film_edge_loads(0.709)` emits service line loads and ideal beam rows. The following
**DERIVATION — NOT IN THE TOOLS** applies the same 1.5 factor as the axial demands:

`V_end,SF = 1.5 wL/2`, `M_mid,pinned,SF = 1.5 wL²/8`, and
`|M_end,fixed,SF| = 1.5 wL²/12`.

| article-A family | tool `w` | factored end shear | ideal pinned, factored member maximum | ideal fixed, factored end moment | actual joint end moment |
|---|---:|---:|---:|---:|---|
| octet | no film edge | 0 from this load set | 0 | 0 | **NOT COMPUTABLE** from the global frame |
| rim, 14×12 | 13,924 N/m over 0.2507 m | 2,618 N | 164.1 N·m | 109.4 N·m | **NOT COMPUTABLE** |
| spoke, 10×8 | 7,332 N/m over 0.2507 m | 1,379 N | 86.4 N·m | 57.6 N·m | **NOT COMPUTABLE** |
| tripod / inward tie | no film edge | 0 from this load set | 0 | 0 | **NOT COMPUTABLE** from the global frame |
| in-plane square tie, 10×8 | 7,439 N/m over 0.1772 m | 989 N | 43.8 N·m | 29.2 N·m | **NOT COMPUTABLE** |

The ideal pinned member maximum is at midspan and is **not** a joint moment. The ideal
fixed value is a support moment but is also not licensed: audit U3 found no measured
moment–rotation stiffness or system eigenmode, and U4 found that axial compression,
film bending and beam-column amplification act simultaneously. The live P13 result says
all 216 moment-loaded ends lack licensed clamped fixity. The pinned row is only an ideal
simply-supported reference; it does not prove a physical pin, omits beam-column amplification,
and is not a conservative combined-`N-V-M` screen. A real semi-rigid end can only be priced
after a moment–rotation curve or a qualified global model supplies the joint's `M-θ` demand.

## 1.3 Interface requirements and what is not computable

| interface mode, article A 0.709 m `n=1` | required numerator | present evidence | status |
|---|---|---|---|
| contacted-seat bearing | the family's factored axial compression, 2.238–5.038 kN | audit U1's analytic annulus screen was 12.419–28.274 mm²; tensile strength was substituted for an unmeasured bearing allowable | **NOT PROVED** for the 100 contacted tree ends; capacity is not licensed |
| closing-end bearing | the family's factored axial compression | 332 closing ends have an adhesive-filled axial butt gap; all 72 rim ends are closing ends. Audit U1's pre-correction rim screen used 0.30 mm per end; the live sunken-frame manifest now emits 0.35 mm per end | **NOT COMPUTABLE**: there is no adhesive compression/creep criterion and no dry seat contact |
| pull-out | the same factored axial magnitude when tension reaches the interface | live P16: 332 `FAIL`, 100 `UNPROVEN`; dry friction is bounded at `μ≤1`, not measured as a pass | **NOT PROVED**; a bonded or positive-capture path is required |
| bond shear | 2.238–5.038 kN divided by a qualified design shear allowable, with peel/eccentricity interaction | generated global-SKU areas are 113.1 mm² closing and 581.2 mm² tree; the 10 MPa line is unsourced | **NOT COMPUTABLE as a margin** until adhesive, preparation, bondline and allowable are qualified |
| direct/transverse fitting section | factored axial plus the 0.989–2.618 kN factored transverse shears above | live P16 uses bounded tensile substitutions; the rim field is sampled with the wrong 10×8 SKU | **NOT PROVED**; all rim bearing/pull-out/shear section values are contaminated |
| end moment and combined interaction | unknown `M-θ`, plus the factored axial and shear loads above | ideal pinned/fixed endpoints only; no combined fitting criterion | **NOT COMPUTABLE** |

The per-family bond-area sensitivity is useful only to size a test. With the repository's
unlicensed `τ=10 MPa` line,

`A_req = F/τ = {337.65, 223.83, 447.66, 477.51, 503.77} mm²`

for octet, spoke, rim, tripod/inward tie and in-plane tie respectively. At the 7 kN survey
ceiling it is 700 mm². This is **DERIVATION — NOT IN THE TOOLS**, not a capacity claim.
Audit U1 showed why: its pre-correction per-SKU rim calculation changed the recorded
area materially yet left the screen below one, and the global-SKU field-probe defect also
contaminates rim pull-out, bending and transverse shear. The correction must be a per-arm
field rerun, not a report-side replacement verdict.

## 1.4 Node populations used for pricing

The generated article-A manifest gives the `n=1` valences directly: 24 nodes at valence 7,
6 at 8, 8 at 9, 12 at 11 and one at 12; total 432 arms, mean 8.4706.

For the 2.0 m, `n=2` comparison, the exact FCC enumeration used by
`kelvin_lattice_counts(2)` gives 201 nodes and 948 struts. Counting each node's `<110>`
neighbours gives 24 nodes at valence 6, 36 at 7, 6 at 8, 56 at 9 and 79 at 12; total
1,896 arms, mean 9.4328. This is a **DERIVATION — NOT IN THE TOOLS' printed output** over
the same predicate: integer triples with `max|u|≤4`, `Σ|u|≤6`, even coordinate sum, and
all in-bounds `<110>` neighbours. No `n=2` STL was generated.

This distribution is a warning against treating every node as the article-A average: the
`n=2` object has 79 valence-12 nodes where article A has one. The price below follows the
study's node-count-plus-OD³ law so it can correct the published comparison, but it is not a
generated `n=2` mass measurement and does not capture valence-superlinear hub growth.

---

# 2. The general engineering question

The survey asks how adjacent fields transfer the load, not what resembles the present
print. “Mass” below means an order at this bore, and “qualified mass” means a complete
10–16 mm node with evidence at 3–7 kN. No source supplied that complete combination.

| adjacent field / mechanism | load transfer and bending behaviour | mass order at 10–16 mm | buyable? | vacuum compatibility and disposition |
|---|---|---:|---|---|
| **Tensegrity strut end caps** | carbon strut carries axial compression; cables or springs attach to an end cap, so the cap resolves several tensile vectors. Usually pin/compliant, not a moment joint. NASA's ReCTeR used 8 mm carbon struts and modular caps, but at robot/drop-test loads, not 3–7 kN. | no transferable 3–7 kN complete-node mass; ReCTeR's three passive struts totalled 50 g including tubes/caps | made for the structure | vent cavities and qualify polymers; useful topology precedent, rejected as load/mass evidence ([NASA ReCTeR](https://ntrs.nasa.gov/api/citations/20140010029/downloads/20140010029.pdf?attachment=true)) |
| **Geodesic hubs** | common systems flatten/bolt strut ends or capture them between hub collars; axial force becomes bolt bearing and local bending. Locking collars add rotational restraint, but the hub is eccentric and bending-bearing dominated. | small plastic dome hubs advertise about 0.9 kN per connector, below this requirement; structural dome hubs are much larger and their mass is not published per 10–16 mm node | buyable at recreational scale | open geometry vents readily; polymer/outgassing still needs screening. Rejected: no 3–7 kN evidence at this bore ([Zip Tie Domes load description](https://www.ziptiedomes.johnhurt.com/faq/About-Our-Geodesic-Dome-Connectors.htm)) |
| **Sailing/kite spar ferrules** | an internal carbon or metal ferrule bridges tube bores; bending transfers through bearing/contact along the insertion length, axial tension only if bonded or positively retained. A straight ferrule joins two collinear ends, not a high-valence node. | commercial 10–12 mm ferrules are gram-to-tens-of-grams parts; no published 3–7 kN rating or complete-node mass | buyable for straight joins | an open ferrule is ventable; a blind bonded insert needs a vent. Retained only as a low-mass analogue, not a survivor ([Prism internal carbon ferrules](https://prismkites.com/products/internal-carbon-ferrules), [Rainbow Flight 10.2 mm ferrule listing](https://kites-rainbowflight.co.nz/products/accessories/)) |
| **Tent-pole coupling** | swaged/internal or repair sleeve transfers bending by distributed contact; shock cord locates it, not structural pull-out. Designed for handling and wind-flexure, not permanent multi-kN axial load. | a buyable 11×130 mm 7001-T6 repair sleeve is 12 g; another 11 mm ferrule is listed at 0.5 oz (`0.5×28.3495=14.2 g`) | buyable | open sleeve is naturally vented; no adhesive if demountable. Rejected: mass is real, qualification is not ([Tatonka 11 mm sleeve](https://www.tatonka.com/de/produkt/reparaturhuelse-11/), [Tent Pole Technologies](https://www.tentpoletech.com/product/ferrule-for-11mm-diameter-aluminum/)) |
| **Antenna/sectional mast coupling** | long spigots or external sleeves transfer bending and shear through bearing; pins/clamps provide axial retention. The long overlap is structurally sensible but adds a fitting to each end. | no qualified complete node found; a commercial carbon-tube clamp accepting a 12 mm reducing sleeve is 30 g before the mast/node structure | buyable as proprietary mast sections; custom at this load | through-pin and sleeve volumes can be vented; bonded blind spigots cannot. Retained as a long-overlap geometry precedent only ([Carbon Composite tube connectors](https://www.carbon-composite.com/en/Products/Connector/)) |
| **Model-aircraft / drone-boom clamps** | split aluminium clamps turn bolt preload and friction into shear transfer; twin plates can carry bending, but a single C-clamp is not a node and friction-only pull-out is exactly the current unproved path. | buyable 16 mm aluminium clamps are 9.4–9.9 g **per clamp**, before the opposing structure/bolts/node | buyable | metal is fine; crevices and blind screw holes need vents, lubricants/locking compounds need screening. Rejected as a complete joint ([JMRRC 16 mm clamp](https://www.alibaba.co.uk/product-detail/16mm-C-type-Clamp-for-16mm_1600963827818.html), [GoGo RC 16 mm clamp](https://gogo-rc.com/store/index.php?product_id=4320&route=product%2Fproduct)) |
| **Space-frame ball/cone node (MERO)** | compression passes through cone/sleeve bearing; tension through a high-strength bolt into a spherical node. The standard KK connection is pin-jointed; separate cylinder systems use multiple bolts for moment resistance. This is the cleanest explicit split of compression and tension paths. | structural system starts at 30 mm tubes and 49.5 mm balls; even the smallest standard node is outside this bore/mass class | buyable as a system, not as a 10–16 mm fitting | steel/aluminium are compatible if holes/threads are vented. Rejected on scale and mass, retained as load-path precedent ([MERO KK system](https://www.mero.com.sg/fa%C3%A7ade-system/spaceframe-system/)) |
| **Bonded internal insert / modular end fitting** | a tapered or channelled insert puts adhesive predominantly in shear over controlled engagement; a tab, pin or thread then connects to the node. It can be deliberately pin-ended. DragonPlate adds bondline-control beads; Simons Observatory used injected epoxy, flow channels and a dedicated vent hole. | no qualified mass at this bore. Aerospace evidence warns that fittings commonly dominate strut mass; Simons pull tests reached the kN range but its fitting/fastener, not adhesive, governed | commercial concepts exist; a 3–7 kN part is made/qualified to order | **survivor** if resin passes outgassing, blind volume is vented, galvanic isolation and moisture/creep are addressed ([DragonPlate inserts](https://dragonplate.com/patented-modular-connector-technology), [Simons Observatory strut](https://arxiv.org/abs/2201.06094), [EU TFP strut finding](https://cordis.europa.eu/project/id/696376/reporting)) |
| **Bonded lap/scarf tube joint** | overlap spreads axial load as adhesive shear; taper, spew fillet and double-lap/scarf geometry reduce peel and end stress concentration. It can carry bending if the overlap is circumferential and long enough; a mitred many-arm node additionally needs central fibre continuity. | adhesive is sub-gram per arm in the screen below, but the central wrap/gusset mass is unknown; there is no qualified complete-node mass | made | open laminate is ventable; resin system and bondline require vacuum screening. **Survivor mechanism**, not yet a design ([Hexcel bonding guide](https://www.hexcel.com/wp-content/uploads/2026/01/Adhesive_Bonding_Technology.pdf), [CFRP/titanium scarf double-shear precedent](https://www.sciencedirect.com/science/article/abs/pii/0263822386900760)) |
| **Moulded composite end fitting / node** | co-cured or compression-moulded material wraps the tube end and redistributes load into a central fitting, reducing discrete metal/bolt mass. Can be pin or moment-capable according to the central geometry. | no public qualified mass at 10–16 mm/3–7 kN | made | continuous cured composite avoids a metal crevice but still needs vents and resin qualification. **Survivor mechanism**; Hexcel reports thin-wall tube bonding required a test programme, not a catalogue assumption ([Hexcel X-Brace case](https://www.hexcel.com/wp-content/uploads/2026/01/HexcelCSAudiv7web1.pdf), [qualified moulded CFRP end-fitting abstract](https://www.nasampe.org/store/viewproduct.aspx?ID=4288545)) |

The survey answer is therefore a mechanism hierarchy:

1. bonded tapered composite socket / scarf / moulded end fitting;
2. the same fitting terminating in a true pin if the global model licenses a pin;
3. a lightweight central laminated node if the joint must carry moment;
4. printed shell/topology variants only after the missing boundary loads are supplied.

Nothing found licenses friction-only capture, a short 2 mm pilot, or a bare adhesive butt
as the 3–7 kN answer.

---

# 3. Price the families after the survey

## 3.1 Corrected bases and target

All candidate values below are **DERIVATIONS — NOT IN THE TOOLS**, except the source
quantities named in each equation. The read-only restriction prevents adding candidate
mass models to the studies.

For article A, 0.709 m, `n=1`:

- tool/manifest bases: `V=0.709³/2=0.178200 m³`, 51 nodes, 432 arms,
  `m_tube=2.390 kg`, `m_node,solid=0.715 kg`;
- mean solid node `=0.715/51=0.0140196 kg`;
- solid-node density `=0.715/0.178200=4.01234 kg/m³`;
- 15% target `=0.15(2.390)=0.3585 kg=2.01178 kg/m³=0.007029 kg/node`.

The 2.390 kg tube line is the model line against which `NODE_MASS_FRAC` is defined. P14 says
that line over-bills the generated cut schedule; fixing that bill is outside this pass, so the
target is identified as the model target rather than silently recomputed from a different BOM.

For the 2.0 m, `n=2` R1 comparison:

- tool bases: `V=2³/2=4.000 m³`, 201 nodes, 948 physical members, 1,896 arms,
  selected OD 16.5 mm, `F=6,716.962 N`, and bulk-allocated
  `m_tube,768=8.789657 kg` for the study's `96n³=768` strut allocation;
- the stated standalone object must charge all 948 physical struts, so its tube mass is the
  **DERIVATION — NOT IN THE TOOLS' printed output**
  `m_tube,948=8.789657(948/768)=10.849733 kg`;
- the study prints 8.23248 kg of nodes from the stale constant `465/51 g`;
- corrected solid nodes
  `=201(0.715/51)(16.5/10)³=12.658544 kg`;
- corrected mean `=12.658544/201=0.0629778 kg/node`; corrected density
  `=12.658544/4=3.164636 kg/m³`;
- standalone 15% target `=0.15(10.849733)=1.627460 kg=0.406865 kg/m³`
  `=0.008097 kg/node`.

Pairing the 201 standalone nodes with the study's 768-strut bulk allocation would mix control
volumes. The independent audit identified exactly this R1 defect; this report retains the
requested standalone mass object and charges all 948 struts consistently. The section and
candidate masses still inherit the study's missing general-`n` film-bending check, so they are
floors that can move upward when the standalone boundary load case exists.

This is the required 0.715/0.465 = **1.537634 correction**. A green
`subdivision_study.py` self-check does not correct its `NODE_G_AT_10MM = 465/51` constant.

## 3.2 Candidate assumptions and full derivations

**Printed solid, today.** The `n=1` mass is the generated SDF integration. The `n=2`
mass applies the study's measured cubic-OD law to the corrected article base, as shown
above. Neither is a strength proof.

**Printed shell, deliberately vented.** There is no shell generator or shell mass output.
The pricing screen assumes a shell plus ribs/arm load paths retains **40%** of today's solid
SDF mass:

`m_shell = 0.40 m_solid`.

Thus `n=1` is 5.608 g/node and 1.60493 kg/m³; `n=2` is 25.191 g/node and
1.26585 kg/m³. The 40% is an explicit scenario, not an observed shell fraction. Vent holes,
local bosses and any reinforcement are not added.

**Topology-optimised print.** No load-complete optimization exists. The screen assumes an
aggressive **25%** retained mass after bearing, pull-out, bond, shear and moment boundary
conditions have been added:

`m_topology = 0.25 m_solid`.

Thus `n=1` is 3.505 g/node and 1.00308 kg/m³; `n=2` is 15.744 g/node and
0.79116 kg/m³. This is a sensitivity, not topology-optimizer output.

**Mitred/bonded composite, no printed hub — material sensitivity scenario.** This is the survey
survivor reduced to the material needed at each arm, before central load redistribution.
The screen intentionally uses the largest family load for all arms at `n=1` and the study's
octet demand for all arms at `n=2`. Assumptions: adhesive design shear sensitivity
`τ=10 MPa`; bondline 0.20 mm; cured adhesive density 1.20 mg/mm³; application/waste factor
1.25; composite design stress sensitivity 500 MPa; composite density 1.60 mg/mm³; and a
20 mm stressed composite path per arm.

Per arm:

`A_bond=F/τ`, `L_one-sided=A_bond/(πD)`,

`m_adh=A_bond(0.20)(1.20)(1.25)/1000 g`,

`A_comp=F/500`, and `m_comp=A_comp(20)(1.60)/1000 g`.

For article A, `n=1`, using `F=5,037.667 N`, `D=10 mm`:

`A_bond=503.767 mm²`, `L_one-sided=16.035 mm`, `m_adh=0.15113 g/arm`,

`A_comp=10.0753 mm²`, `m_comp=0.32241 g/arm`.

At `432/51=8.47059 arms/node`, the sensitivity result is
`(0.15113+0.32241)(8.47059)=4.01117 g/node`,
0.204570 kg per article and **1.14797 kg/m³**.

For the 2.0 m, `n=2` object, using `F=6,716.962 N`, `D=16.5 mm`:

`A_bond=671.696 mm²`, `L_one-sided=12.958 mm`, `m_adh=0.20151 g/arm`,

`A_comp=13.4339 mm²`, `m_comp=0.42989 g/arm`.

At `1,896/201=9.43284 arms/node`, the sensitivity result is
`(0.20151+0.42989)(9.43284)=5.95584 g/node`,
1.197124 kg per cell and **0.299281 kg/m³**.

The central material that turns multiple arm forces into equilibrium is absent because no
geometry or closing load solution exists. Calling this a complete 5.956 g node would be
false. The assumed 10 MPa bond line, 500 MPa composite line and 20 mm stressed path do not
establish a mathematical lower bound. This sensitivity only illustrates how little allowance
would remain under those assumptions: the standalone `n=2` 15% target permits 1.627460 kg
total. After the 1.197124 kg arm-material screen, only **0.430336 kg total** remains,
equivalent to **2.141 g/node on average**. The required allocation across valences 6–12 is
not computed; 2.141 g is not a demonstrated cap for each individual node.

## 3.3 Ranked comparison

Rank is by **2.0 m, `n=2` node kg/m³ saved**, because that is R2 after R1. The `n=1`
columns remain article A, 0.709 m. Percentages are node mass divided by tube mass, matching
the model's `NODE_MASS_FRAC=0.15` definition.

| rank | family and status | article A 0.709 m `n=1`, kg/node | `n=1` node kg/m³ (saved) | `n=1` node/tube | R1 2.0 m `n=2`, kg/node | `n=2` node kg/m³ (saved) | `n=2` node/tube | governing assumption |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | bonded/mitred composite, **incomplete material sensitivity** | 0.004011 | 1.14797 (2.86437) | 8.6% | 0.005956 | 0.29928 (2.86536) | 11.0% | assumed 10 MPa bond, 500 MPa laminate and 20 mm path; **central redistribution mass absent** |
| 2 | topology-optimised print, **scenario** | 0.003505 | 1.00308 (3.00925) | 7.5% | 0.015744 | 0.79116 (2.37348) | 29.2% | retains 25% of corrected solid mass after all missing loads are applied |
| 3 | shelled-and-vented print, **scenario** | 0.005608 | 1.60493 (2.40740) | 12.0% | 0.025191 | 1.26585 (1.89878) | 46.7% | retains 40% of corrected solid mass; vent/boss/reinforcement mass absent |
| 4 | printed solid, **`n=1` measured; `n=2` scaled; strength not proved** | 0.014020 | 4.01234 (0) | 29.9% | 0.062978 | 3.16464 (0) | 116.7% | corrected 0.715 kg base and cubic-OD scaling; no valence correction |
| — | bonded internal insert / modular fitting, **survivor; unranked** | **NOT COMPUTABLE** | **NOT COMPUTABLE** | **NOT COMPUTABLE** | **NOT COMPUTABLE** | **NOT COMPUTABLE** | **NOT COMPUTABLE** | no qualified complete-node mass at either bore/load; opposing fitting, pin and centre absent |
| — | moulded composite end fitting / node, **survivor; unranked** | **NOT COMPUTABLE** | **NOT COMPUTABLE** | **NOT COMPUTABLE** | **NOT COMPUTABLE** | **NOT COMPUTABLE** | **NOT COMPUTABLE** | no geometry, load-complete laminate or production mass at either object |
| — | 15% target, not a candidate | 0.007029 | 2.01178 | 15.0% | 0.008097 | 0.40687 | 15.0% | `0.15 × tube mass`; standalone 948-member tube allocation at `n=2` |

The table does **not** establish that a 25%-mass topology or 40%-mass shell survives the
loads. It prices precisely what those hypotheses would be worth. At `n=1`, either scenario
would beat the 15% mass line if it survived. At `n=2`, neither does. The bonded sensitivity
is `100(0.406865-0.299281)/0.406865=26.4%` below the standalone `n=2` target by mass,
but its unmodelled central material must fit inside 0.430336 kg total, or 2.141 g/node only
as a 201-node average. No node-by-node allocation exists, so that is not credible enough to
freeze as a baseline or call a winner.

The **best mass-checked number** is therefore the worse one: article A's generated solid
set, 0.715 kg or 4.012 kg/m³ at 0.709 m, `n=1`; its structural verdict is still `NOT
PROVEN`. At 2.0 m, `n=2`, no geometry exists, so even the corrected 3.165 kg/m³ solid row is
a study-law projection. The 0.299 kg/m³ bonded line is the best quantified hypothesis, not
an achievable checked result.

---

# 4. Is a vented shell acceptable in vacuum?

## Verdict: yes as a vacuum architecture, conditional as a structural joint

“Sparse infill is a virtual leak” is correct for closed or poorly connected pores: gas
trapped behind a low-conductance path continues to enter the evacuated volume. It is not a
reason to make the joint solid. A deliberately open shell whose internal cavities are
connected to the cell vacuum has no permanently trapped gas volume; after the pump-down
transient, both sides of the shell approach the same pressure.

This is established vacuum practice, not an analogy invented for this report:

- NASA's vacuum-joint guidance vents blind tapped holes and slots threaded fasteners so
  each trapped volume has an escape path
  ([NASA vacuum apparatus practice](https://ntrs.nasa.gov/api/citations/19690022568/downloads/19690022568.pdf?attachment=true)).
- Current ECSS-E-ST-20-01C identifies chamber pressure, equipment venting design and time for
  moisture to outgas as the combination controlling pressure in critical internal regions
  ([ECSS-E-ST-20-01C](https://ecss.nl/wp-content/uploads/2020/07/ECSS-E-ST-20-01C%2815June2020%29.pdf)).
  The superseded ECSS-E-20-01A Annex B remains useful historical experimental evidence: it
  sizes distributed vent conductance against cavity volume/outgassing and shows wall outgassing
  can dominate ultimate pressure even after conductance is provided
  ([historical ECSS-E-20-01A, Annex B](https://ecss.nl/wp-content/uploads/standards/ecss-e/ECSS-E-20-01A5May2003.pdf)).
- NASA and ECSS screen non-metallic materials for total mass loss and condensable products;
  NASA's usual historical screen is TML ≤1.0% and CVCM ≤0.10%, but application-specific
  requirements may be stricter
  ([NASA outgassing database description](https://outgassing.nasa.gov/Description),
  [ECSS-Q-ST-70-02C](https://ecss.nl/standard/ecss-q-st-70-02c-thermal-vacuum-outgassing-test-for-the-screening-of-space-materials/)).

Venting solves **trapped volume**. It does not solve PAHT-CF/adhesive outgassing, water
desorption, blocked passages, transient differential pressure, shell buckling, permeation
through the outer skin, or the missing 3–7 kN interface proof.

## Test that would settle it

1. Print representative solid, sealed-shell and redundantly vented-shell coupons with the
   intended PAHT-CF, orientation, post-process, adhesive and coating. The vented specimen
   must include the smallest/longest production vent path and production bond squeeze-out.
2. CT-scan or section witnesses to confirm that every internal cell reaches at least two
   visible vents and that adhesive/support material has not made a blind pocket.
3. Pump from one atmosphere at the article's maximum planned pump-down rate while measuring
   chamber pressure and a witness internal-cavity pressure. Calculate conductance and require
   the peak differential pressure to remain below a separately proved shell transient limit.
4. Hold at pressure and record pump-down tail with a residual-gas analyser or rate-of-rise
   method. Compare solid, sealed and vented coupons. The vented shell passes the virtual-leak
   question only if its tail is explained by material outgassing rather than a delayed cavity.
5. Run ASTM E595/ECSS-Q-ST-70-02 screening on the actual printed and bonded material system,
   then bake/condition as the process will be used. A resin name alone is not a qualification.
6. Helium-leak-test the **skin-to-node sealed boundary**, keeping intentional node vents on
   the vacuum side of that boundary. An intentional vent is not itself a leak through the
   airship envelope.
7. Test axial compression, pull-out, transverse shear and imposed rotation to the factored
   family envelope before and after vacuum dwell, moisture conditioning and duration/creep.
   Record failure mode and mass for every coupon.

A successful pump-down coupon licenses hollow geometry for structural development. Only the
combined structural/environmental programme licenses a flight joint.

---

# 5. What would have to be true for the screen-leading candidate to become the winner

For a bonded/mitred or moulded composite node to be the actual winner rather than the
incomplete material sensitivity in §3:

1. A closing global stiffness/equilibrium model must give each arm's signed `N`, `V`, `M`
   and rotation for the standalone article and array. It must replace, not average away,
   the current 7,868 N residual.
2. The intended end behaviour must be licensed by an `M-θ` curve or a true pin detail.
   Neither `K=1` nor `K=0.65` may be credited by description alone.
3. Per-SKU geometry must be measured on the actual arm field. The global 10×8 probe defect
   must be fixed and the rim/closing-end census rerun before any analytic sensitivity is
   promoted to a verdict.
4. A controlled overlap/scarf must develop the factored axial load without tube splitting,
   adhesive peel, bearing failure, pull-out or bond creep. Coupons must use the purchased
   tube surface, production preparation, bondline spacers and cure.
5. The central laminate must close every arm force and moment with **≤0.430336 kg total**
   additional mass across the 201 nodes on the 2.0 m, `n=2` comparison if the 15% target is
   to survive. That is 2.141 g/node only on average; the allocation across valences 6–12 is
   **NOT COMPUTABLE** without geometry. The same allowance must cover vents and local
   manufacturing features.
6. Compression must have a positive path. A tension-adequate lap is not automatically a
   bearing-adequate tube end, and neither the audit's historical 0.30 mm nor the live
   rim's 0.35 mm closing-end butt fill can silently become a hard seat.
7. Assembly must remain possible for the 948-member, 201-node cell. No `n=2` insertion order
   has been generated: the new architecture needs its own generated and checked order and
   cannot add unpriced sleeves after closure. Article A is only precedent, and its P8 insertion
   path remains frozen `NOT PROVEN` because one swept representative grazes its cup mouth.
8. The adhesive/composite system must pass outgassing, moisture, temperature and sustained
   load tests; carbon/metal variants must include galvanic isolation.
9. Production mass, not coupon CAD mass, must include squeeze-out/fillets, gap fill, trim,
   inspection features, rejected parts and repair allowance.
10. Shell/vent, topology and bonded-node mass models must be added to
    `subdivision_study.py` under its existing self-check, and the corrected 0.715 kg basis
    must replace the stale 0.465 kg constant. This report does not make that model change.

If the central mass cannot close inside 0.430336 kg total across the 201 nodes, the 15%
`n=2` target is not reached by this screen. The next honest output is the measured heavier
value, not a relaxed target.

## Not yet counted

These lines are unknown, not zero, in every candidate unless its row explicitly includes them:

- production tube-to-fitting adhesive, spew fillets and bondline-control media;
- the adhesive-filled closing-end butt gaps;
- central CFRP wrap, gusset, insert, pin, bolt or other arm-to-arm redistribution material;
- local tube-end hoop reinforcement against splitting/bearing;
- vent passages, bosses and material around them;
- seal/barrier transition at the node and any galvanic isolation;
- jig-induced overlength, trim and alignment features;
- moisture/desorption allowance, creep knockdown and environmental conditioning effects;
- inspection witnesses, manufacturing fallout, repair material and replacement yield;
- any reinforcement demanded by the missing combined `N-V-M` criterion.

The recovered physics audit quantified several of these on the old 0.465 kg geometry, but
the sunken-frame correction changed the sockets and wrap. Those historical adhesive figures
are not copied onto the 0.715 kg article as though the geometry had not moved.

---

# 6. Reproduction gates

Run on this branch after the report was completed:

- `python3 tools/scale_study.py`: **exit 0; all 14 self-check rows `ok`** and
  `=> reproduces the published article`.
- `python3 tools/subdivision_study.py`: **exit 0; all six self-check rows `ok`** and
  `=> consistent with the model`. Its calculated candidate rows remain on the stale
  `465/51 g` node constant; §3 corrects them explicitly rather than editing the tool.
- `make check`: **exit 2 at `figfresh` in this execution environment**. `lint` and
  `stampcheck` passed first; `figfresh` then failed because no `chromium` executable is
  installed, so later gates were not reached. No compatible executable exists elsewhere
  in the audit environment. The audit branch on the source workstation had
  earlier recorded exit 2 at `stampcheck`; the current tree's stamps now match.
- `make assemblycheck`: **exit 0; `NOT PROVEN — 5 of 16 proofs fail (5 frozen in KNOWN,
  0 new), 11 pass`**. It reports 2,064 of 3,888 scalar margins failing. Exit 0 means the
  frozen bill did not move, not that a joint holds.

`make assemblycheck` rewrites runtime/path fields in `assembly.json`; that incidental output
was restored byte-for-byte, leaving this audit as the only changed file. The repository has
no `./scripts/test.sh` and the task explicitly defines the two studies plus `make check` and
`make assemblycheck` as its gates.

## Source correction note

The reviewed independent audit was recovered read-only from git object
`49f901b1894e71d44557d5648904359708fecf65` and read in full. Its U1/U3/U4 derivations govern
the missing interface, restraint and interaction checks. It predates the sunken-frame
correction: its 0.465 kg node mass, 8.080 kN residual and older P16 census are historical.
This report uses the live 0.715 kg manifest, live 7.868 kN residual and live assembly census
where those values changed, and says explicitly whenever an older audit screen is quoted.
