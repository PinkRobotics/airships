# The vacuum cell

A vacuum airship lifts by holding nothing. The hard part has never been the lift — it is
surviving the atmosphere trying to crush the nothing, and for three hundred and fifty years
that is where the idea dies.

Computed by `research/analysis/vacuum-cell.py`; the same physics runs live on `/cell/` and the
two are held identical by `tools/check_cell_parity.py`.

> ## Where this landed, and where it goes
> The single-level formula with outer-envelope film gives **1.306 kg/m³**.
> Its lattice uses safety factor 1.5, full sea-level pressure, and local-wall knockdown 0.30.
> Air is 1.225 kg/m³ at sea level and 0.957 kg/m³ at 2,500 m.
> The classical buckling coefficient is 0.605.
> The level-two formula gives **0.538 kg/m³**; no higher-level strut is drawn or tested.
> The crush coupon in `docs/VERIFICATION-PLAN.md` (E5) tests the hierarchy assumption.
> A drawn structure also needs joints, film, connections and load checks, as the [ledger](../../docs/FLOAT-LEDGER.md) explains.
>
> The hull's bill and drawing disagree in the end caps in both directions.
> Across the [cap readings](cap-readings.md), the favourable ratio spans 0.751 to 0.998 at sea level and 0.586 to 0.780 at 2,500 m.
> This basis assumes knockdown 0.65 and a 1,450 MPa carbon-laminate ceiling, both unverified, with structural safety factor 1.2 against full sea-level pressure.
> No reading reaches one. The [member census](../../docs/MEMBER-CENSUS.md) records 20 disagreements.

## The one number

> **Air density is 0.9569 kg/m³ at 2,500 m.** At or above this lift wall a shell
> has no net lift at any size. With sundries on everything, including the shell, a hull
> can be grown until its equipment budget closes only below ρ/(1 + f):
> **0.870 kg/m³ in the floor case (f = 0.10)**.

The cases differ with their own sundries fractions: floor: f = 0.10, wall 0.870 kg/m³; credible: f = 0.15, wall 0.832 kg/m³; demonstrated: f = 0.20, wall 0.797 kg/m³. These are conditional mass balances, not structural validation.

## What the sealed-cell architecture buys, and what it does not

Every vacuum-balloon study analyses **one sphere** and reaches the same negative result:
Akhmeteli & Gavrilin show that a perfect *diamond* single-layer sphere collapses at about
0.2 atm, and the criterion is scale-free. Note the qualifier — **single-layer**. Their own
paper reaches a *positive* result for a sandwich, and Jenett's lattice is positive too, so
nothing was ever proved impossible about a multi-layer or cellular shell.

Fill the volume with sealed cells and there is no thin shell at all: interior walls have vacuum
on both sides and carry no pressure differential, the atmosphere is held only at the boundary,
and the array is a cellular solid in hydrostatic compression. What governs becomes the
**crushing strength of that solid**, which is a well-posed engineering problem.

Two honest caveats on how much that buys:

- **The tube step does nearly all the work, not the cell step.** Monolithic and solid-strut
  lattice land within 8% of each other; it is going hollow that moves the number, and hollow
  struts help a lattice-stiffened monocoque just as much. What cells specifically buy is the
  removal of the hull's *shape* penalty (the buckling radius becomes the cell's) and **failure
  containment** — which is the claim `mass-budget.md` already made, and it is the better one.
- A reviewer derives that a *filled* array also beats an optimally-proportioned lattice
  **shell** by about 25%, because strength is superlinear in relative density so concentrating
  material into a shell wastes it. That is a strong argument and it is **not reproduced here** —
  an attempt at it produced nonsense and was removed rather than published.

## The design result: struts must be hollow, and proportioned

At floating densities lattice members are slender enough that **Euler buckling governs, not
yield** — by more than an order of magnitude for every material tested. Solid rods therefore
give strength ∝ φ², and nothing floats. Hollow struts, sized so the strut's Euler buckling and
the tube wall's local buckling fail together, restore φ^1.5.

**Jenett et al. use hollow tubes too** — at a *fixed* R/t = 10, which puts local buckling far
out of reach and recovers the φ² law. The optimum here is **R/t ≈ 54**, and that proportion is
what the mass turns on. That is the contribution, and it is a narrower and fairer claim than
the one this page made first: Jenett explicitly discusses the strength-exponent shift, cites a
threshold for it, and bounds his claim to relative densities above 10⁻³.

## The five corrections, in the order they bite

| | effect on the reference shell |
|---|---|
| **1. Fibre properties used as laminate properties.** M60J's 588 GPa / 3.82 GPa / 1930 is the *fibre*. A laminate at 60% fibre volume is ~354 / 2.29 / 1658. Jenett makes the same conflation and this project inherited it. | ×1.20 |
| **2. The tube wall is orthotropic.** Local buckling depends on √(E_axial·E_hoop), not the axial modulus — so the governing modulus is E_x^¾·E_θ^¼, and the best [0/90] split (¾ axial) costs a factor **0.570**. | ×1.43 |
| **3. Nodes.** They join twelve tubes, weigh 10–30%, and carry no load — so their solid raises φ without raising capacity, and it counts twice. | ×1.15 |
| **4. A safety factor.** Every strut sat *exactly* at its Euler load, all of them simultaneously, with no knockdown — while the monolithic branch got 0.2 and the sealing film got 8. | ×1.31 |
| **5. The interior sealing film, which the model computed and never counted.** | +0.347 |

**Correction 5 is the one worth understanding.** If every cell is individually sealed — the
entire premise — the film is not a skin over the hull, it is the array's **internal** surface,
about 3/*l* m² per m³. And because a film's areal mass grows with the span it bulges across
exactly as fast as area-per-volume falls, the product is **the same at every cell size**:

| cell size | 0.5 m | 1 m | 2 m | 4 m |
|---|---|---|---|---|
| film sized to hold an atmosphere | 0.347 | 0.347 | 0.347 | 0.347 kg/m³ |
| minimum-gauge foil laminate instead | 0.300 | 0.150 | 0.075 | 0.038 kg/m³ |

**You cannot choose a cell size that makes this term go away** — if you need it at all. And a
third review showed the model was incoherent about whether it does.

**Interior partitions have vacuum on both sides, so there is no partial-pressure gradient and
no permeation driving force across them.** A permeation barrier is only needed where vacuum
meets atmosphere. The dated 190 × 47 m spheroid reference from the first study has
22,592 m² of envelope against 660,000 m² of interior wall at 1 m cells, a factor of **29**. So the film has exactly two possible jobs, and the model was paying
for one while its own notes said it did the other:

| architecture | film cost | total | margin | what you get |
|---|---|---|---|---|
| partitions sized to hold an atmosphere | 0.347 | 1.630 | 0.59× | a breach stays in one cell |
| barrier on the outer envelope only | 0.024 | **1.306** | **0.73×** | one breach floods the hull |

The envelope-only figure was 0.002 in an earlier version — an unsourced 17 g/m² film assigned
to a surface that must hold a full atmosphere over 2 m spans. A review priced it with the
model's own membrane function: **0.232 kg/m² — twelve times what was charged — and as
published, nothing in that option was holding the atmosphere at the boundary at all.** Two
design levers reduce it honestly: finer boundary cells (film mass is span-proportional), and
the graded band below, which divides the envelope's differential by its step count.

**That trade — containment against 0.35 kg/m³ — is the sharpest unresolved question in the
design.** It is worth a third of the shortfall, and the earlier version of this page paid for
it without claiming the function.

**A separate problem with the film calculation, verified independently.** The assumed bulge
(h/a = 0.25) demands **4.12% membrane strain**, and Zylon at the model's own working stress
delivers **0.27–0.40%** — ten to fifteen times less. The reachable bulge is h/a ≈ 0.07, at
which the film is about **3.7× heavier** and sinks the design outright. The escape is to
**pre-form the membrane to its loaded dome shape** rather than install it flat, and that has to
become a stated design requirement. 4% strain would also craze any inorganic barrier coating on
first pump-down.

## Where every material lands

Lattice + nodes + film, at 2 m cells, against air at 0.957 kg/m³ at 2,500 m:

| material | index E^⅔/ρ | lattice | +nodes | +film | **total** | margin |
|---|---|---|---|---|---|---|
| M60J UD laminate | 20,746 | 1.115 | 0.167 | 0.347 | **1.630** | 0.59× |
| T700 UD laminate | 11,306 | 2.046 | 0.307 | 0.347 | **2.700** | 0.35× |
| Continuous CF, printed | 7,525 | 3.074 | 0.461 | 0.347 | **3.883** | 0.25× |
| Ti-6Al-4V, sintered | 5,307 | 4.358 | 0.654 | 0.347 | **5.360** | 0.18× |
| Bambu PAHT-CF (X-Y) | 1,596 | 14.496 | 2.174 | 0.347 | **17.018** | 0.06× |
| Bambu PAHT-CF (Z) | 1,090 | 21.216 | 3.182 | 0.347 | **24.746** | 0.04× |

**The index is E_eff^⅔/ρ, not specific strength.** Everything here is buckling-governed, so
strength is not a lever at all — an earlier version of this page said the opposite in three
places. Titanium's problem is not that it is weak; it is that stiffness per unit density is
what counts and it has a quarter of carbon's.

## Two "null results" that were wrong, both in the same way

Both assumed shell mass scales with pressure. That is the **yield** case, and nothing here is
yield-governed — it scales as p^⅔.

**Partial vacuum is not neutral; full vacuum is strictly optimal.** Lift goes as Δp and shell
mass as Δp^⅔, so shell-per-lift degrades as Δp^−⅓: 1.13 at full vacuum, 1.25 at three
quarters, 1.43 at half. *This correction favours the concept*, which is why it is worth
getting right.

**Altitude is not neutral either; it is mildly unfavourable.** The requirement goes as
T·p^−⅓, so it gets *harder* with height. Sized locally, margin falls 1.13 → 1.08 → 1.03 from
sea level to 5,000 m. And a ship that lands has to survive sea level anyway, which is the
convention used throughout.

## Aerogel, asked and answered

Filling the struts is the obvious idea — a core stabilises the wall against wrinkling. But
aerogel's modulus falls as roughly the *cube* of density, so a core stiff enough to matter is
several times the mass of the wall it stabilises and one light enough to carry is far too soft.
The bare tube already carries over a gigapascal before it wrinkles. **No density beats it.**
Aerogel's role here, if any, is thermal or a manufacturing aid.

## The manufacturing consequence still stands

The optimum tube wall is a fixed fraction of the strut length, so the thinnest wall you can
produce sets a floor on the lattice:

| thinnest wall | struts at least |
|---|---|
| 0.03 mm (thin-ply prepreg) | 0.08 m |
| 0.125 mm (standard ply) | 0.33 m |
| 0.2 mm | 0.53 m |
| 0.4 mm | 1.06 m |

A reviewer notes the argument needs restating: the flight article is wound or pultruded, not
printed, so the floor is a *ply*, not a nozzle — and you need at least four plies to have any
hoop modulus at all (correction 2). The metre-ish conclusion survives for a different reason
than the one first given.

## What is still not modelled

Deviatoric load of any kind — gusts, manoeuvre, hull bending, the anchor's 1.2 MN reaction,
ground handling, thermal. Creep at permanent load, which attacks the matrix-dominated hoop
modulus that correction 2 just made decisive. Permeation over a service life for a hull with
no valve and no pump. Load introduction at the array boundary. Packing fraction. Any
lattice-scale imperfection knockdown, as distinct from the strut-scale safety factor now
applied.

## Hierarchy is the path, and it is short

Each level of self-similar structure improves the strength-density exponent: (n+2)/(n+1),
tending to linear. Lakes, *Materials with structural hierarchy*, Nature 361 (1993).

| levels | exponent | density kg/m³ | lift/mass at sea level | lift/mass at 2,500 m | status |
|---|---|---|---|---|---|
| 0 | 2.000 | 7.986 | 0.153 | 0.120 | formula only |
| 1 | 1.500 | 1.306 | 0.938 | 0.733 | formula only |
| 2 | 1.333 | 0.538 | 2.276 | 1.778 | formula only |
| 3 | 1.250 | 0.403 | 3.037 | 2.372 | formula only; yield-capped |
| 4 | 1.200 | 0.403 | 3.037 | 2.372 | formula only; yield-capped |

**The ladder ends where the material's strength begins** — a correction a review caught.
Buckling permits ever-lower solid fractions, but the solid still carries 3p/φ, so φ can never
fall below the yield floor. Levels 3 and 4 both hit it: their rows are the *strength* of the
laminate, not the exponent, and the reserve they promise is 2.37×, not the 3.9–5.7× an
earlier version published. Level 2 itself runs the solid at **89% of laminate strength** —
a margin worth knowing about before anyone leans on it.

**It converges fast, and the second level is the one that matters.** Beyond it the returns
end at the yield floor while the manufacturing cost does not — every level adds joints,
tolerance stack and inspection, and the *coefficient* degrades even as the exponent improves.
So the design target is two levels, and the third buys strength reserve only.

That also settles the argument with the literature rather than continuing it. Jenett assumes
linear scaling; linear is the n→∞ limit; hierarchy is the mechanism that gets there. He was
describing the destination, and this page is describing the road.

## The path, as a list

Each gap below has a lever, and none of them is a physics objection:

| gap | size | lever |
|---|---|---|
| single-level lattice is short of the wall | see both altitudes in the hierarchy table above | **a second level of hierarchy**, conditional on drawn members and load tests |
| interior films, if sized to hold an atmosphere | −0.35 kg/m³ | evacuate and seal at *every* scale, so no single partition ever faces a full atmosphere |
| membrane strain at the assumed bulge | 3.7× on film mass | **pre-form the membrane to its loaded dome** rather than installing it flat |
| node mass, asserted at 15% | ±0.14 kg/m³ | the largest unsourced number left; a real joint design settles it |
| printed parts cannot hold vacuum | 4–7 orders | the barrier is a separate film, not the printed structure |
| deviatoric load, creep, ground handling | unquantified | not yet modelled; each is ordinary aerospace work |

**Sealing at every scale is the elegant part**, and it is the user's own instruction rather
than an analyst's fix: if sub-cells are evacuated and sealed inside cells inside sections, then
no partition ever faces more than the differential of its own level, a breach is bounded by the
smallest enclosure that contains it, and the containment-versus-mass trade that dominates the
single-scale design largely dissolves.

---

## Pressure grading: costly in bulk, free at the boundary

Staging the pressure across N levels of cells so no *partition* sees more than 1/N of an
atmosphere works for the films. It does not work for the lattice, and this section has now
been wrong about that twice, in opposite directions:

> **Version one** charged nested-shell structure *and* the full staged-gas mass — double
> counting. **Version two** claimed "the gas columns transmit the compression, so the
> lattice sees only its local step" — and a reviewer's force balance killed it in a line:
> gas transmits compression only **up to its own pressure**, so across any cut the solid
> must carry P<sub>atm</sub> minus the local gas pressure. The load *accumulates* inward,
> and the vacuum core carries the full atmosphere exactly as if the grading were not there.
> This table is the statics-correct third version, and the correction chain is left visible
> because that is what this repository is for.

Model: equal-volume zones, the lattice in each zone sized for its **cumulative** load
(j/N atm), level-2 struts (mass ∝ p^¾), films holding one step over a 2 m span, the
envelope film priced for the differential it actually sees:

| N levels | structure | gas held | films | net lift |
|---|---|---|---|---|
| 1 — hard vacuum | 0.515 | 0.000 | 0.024 | **+0.418** |
| 2 | 0.410 | 0.239 | 0.186 | +0.122 |
| 10 | 0.319 | 0.431 | 0.037 | +0.170 |

**In bulk, grading surrenders over half the net lift** — the gas costs lift everywhere while
the deep lattice still carries nearly the full atmosphere — and it hands the array's
rigidity and trim to trapped gas and its temperature, which is exactly the property the
sealed-vacuum architecture exists to avoid.

**At the boundary, the honest envelope price changes the verdict for the better.** Stage the
outermost 5% of the volume in ten steps and the envelope film's differential — and so its
mass — falls tenfold, a saving of about the same size as the band's gas: the whole
arrangement nets **-1.9% of net lift, a small saving**, while the outer surface sees
**0.1 atm** instead of one. Membrane strain, barrier-crazing risk and the consequence of an
outer-face breach all fall tenfold with it. The band is half a metre deep on this hull, so
its steps are sub-cell-scale layers — which is the seal-at-every-scale doctrine anyway, and
film mass is span-proportional so thin layers cost no more. What the band still costs is
operational: trapped gas ties its trim to temperature, and the outermost cells must survive
the ground-level case like everything else.

## The pumped plenum: the same doctrine, made active

The graded band stages pressure with sealed gas; the **pumped plenum** does it with a pump:
a soft outer shell across the whole ship holding as much vacuum as it can — lossy, actively
pumped, never sealed — so that **no interior cell operates against a full atmosphere**. It
is already what the section-and-bay picture shows, and it deserves stating as doctrine.

Statics is not fooled: the shell's mounts deliver the withheld atmosphere into the array as
structure load, so the plenum buys **no lattice mass**. What it buys scales directly with
the plenum pressure, and every line of it is margin rather than mass:

| plenum | cell operating margin | permeation drive | a breach floods to |
|---|---|---|---|
| 1.00 atm (no plenum) | ×1.50 | ×1.00 | 1.00 atm |
| 0.50 atm | ×3.00 | ×0.50 | 0.50 atm |
| 0.25 atm | ×6.00 | ×0.25 | 0.25 atm |
| 0.10 atm | ×15.00 | ×0.10 | 0.10 atm |

Pump failure is a slow drift back to the 1 atm case the cells were designed for — margin
erodes toward the design point, nothing breaks. The price is a pump fighting the shell's
leak rate for the life of the ship; that power line needs a leak-rate assumption nobody has
made yet and is left open rather than invented. **The prototype requirement is unchanged on
purpose: one cell, zero net weight, against a full atmosphere, outside any ship** — the
plenum is what the ship then adds around it, as redundancy and as reach.

## The cell shape: the interlocking near-sphere is also the film-optimal one

The analysis charges film area with the cube coefficient (3.0 per m³·cell size). The
interlocking, "as spherical as tessellation allows" block the design intends is the
**truncated octahedron** — the Kelvin cell, BCC's Voronoi cell, eight hexagons and six
squares — and it carries **11.4% less shared-wall area** than cubes at equal cell volume
(coefficient 2.657). Kelvin posed equal-volume space partition as a minimum-surface problem
in 1887; his cell held the record until Weaire–Phelan's pair of shapes shaved a further 0.3%
in 1994. Minimum film mass and printable interlocking blocks are the same ask, and the
analysis's cube figure is conservative against both.

How the membrane meshes with the structure — corrected once, and the correction recorded:
an earlier version claimed every face was node-supported, from a lattice generator that
admitted **two interleaved octets** (all integer grid points instead of the even-sum FCC
sites — twice the design density; the count ratio converging to 2.0 instead of 1.0 caught
it). The true octet puts a node in the centre of **each square face**; the hexagon centres
belong to the *dual* lattice and carry no node. So a standalone article frames its
hexagons with a printed **rim along its 36 edges** — each edge exactly one strut-length,
so the rim prints as the same struts — while in the array the struts simply continue
through the hexagon planes and the film bonds to their crossings.

**Cells do not seat face-to-face, and an earlier version of this paragraph said they did.**
It claimed all boundary structure sits inset beneath the true faces so the mating planes
stay flat; the generated geometry says otherwise, and the geometry is right. **108 of the
216 members lie exactly in a face plane** shared by both their end nodes — every rim edge,
every hexagon spoke, every in-plane square tie — because both endpoints are lattice or
dual-lattice sites *on* that plane, and no generator can inset a member off a plane its own
end nodes lie in. Each stands half a tube proud on both sides, so two finished articles stop
14 mm apart on the rim pipes and never touch the 86 flat lands the 38 boundary joints carry.
Nothing in the architecture asks them to. The parity argument two sections down is what
settles it: the rim, hubs, spokes and ties are the **odd-n** boundary apparatus, and at even
n the hexagon plane is full of lattice sites, the film bonds straight onto the octet and the
whole frame disappears. An array is one continuous lattice partitioned by film, not a stack
of finished cells butted together. The lands are therefore the **print datum** — the flat
that puts a joint on the bed — and the plane the **film bonds to**; they are not a bearing
surface between cells, and what the inter-cell joint actually is remains E1's open question.
`tools/check_assembly.py` measures the 108 every run and caps it in the contract, which is
what would catch anyone quietly re-adopting the claim this paragraph just retired.

## From the printer nozzle to the demonstrator

The chain runs: nozzle → extrusion width → wall → strut length → cell. For PAHT-CF in the
interlayer direction (the one that governs a pressure vessel):

| nozzle | perimeters | wall | strut | cell | enclosed |
|---|---|---|---|---|---|
| 0.4 mm | 2 | 0.80 mm | 0.130 m | 0.184 m | 6 L |
| **0.6 mm** | **2** | **1.20 mm** | **0.195 m** | **0.276 m** | **21 L** |
| 0.6 mm | 3 | 1.80 mm | 0.292 m | 0.413 m | 71 L |
| 1.0 mm | 2 | 2.00 mm | 0.325 m | 0.459 m | 97 L |

These are the chain at the CORRECTED physics — the classical 0.605 cylinder coefficient
landed on 2026-08-12 (audit O1), and the co-critical wall fraction grew with it, so every
nozzle's natural cell shrank. **The built article predates the correction and is pinned at
the pre-correction design point — 251 mm struts, 354 mm pitch, 44 L — as a measurement**
(the size it was sawn and printed at is a fact about the object, not about the optimiser).
The row above is what the same nozzle would produce if the chain were walked today.

**0.6 mm hardened, two perimeters, is the design point.** Chopped fibre abrades brass and
bridges a 0.4 mm orifice, so 0.6 hardened steel is the reliable choice for a shop running many
machines — and a 1.2 mm wall is the smallest that is repeatable across them.

The happy accident: **251 mm struts fit a 256 mm bed exactly.** The chain's 354 mm figure is
the *sub-cell pitch* those struts make, enclosing 44 litres per pitch cube. (The first draft
said 45 — hand arithmetic, caught the day the number was generated. Rule 1 exists for a
reason.)

**The article itself is not a cube — it is the design's own shape.** A **709 mm Kelvin
article, 178 litres**, its octet interior at the 354 mm pitch, its hexagons framed by a
rim along the 36 edges: **60 octet struts, a 36-member rim frame, 48 vertex ties and 43
nodes**, every long member the same 251 mm co-critical part. (The rim frame is a count of
printed members, not of octet struts — a distinction that later cost the analysis a wrong
demand on 72 member-ends; see *Which member reacts which load* below.) (An earlier version printed one
cubic octet cell — "why is it a cube" was the designer's response — and a still earlier
count carried the doubled phantom lattice recorded above: 204 struts and 7.85 kg were
that error's numbers.)

**Three more corrections, all caught by the designer's eye, all correct.** First the
rim: the 24 rim vertices are dual-lattice sites — coordinate sum odd, every one — so the
rim frame as drawn touched the octet *nowhere*. "Only touches the face on the points of a
cube," he said, looking at the render; the counts agreed. Two ties per vertex now bind rim
to lattice. Then the faces: "the main faces are actually still unsupported — the smaller
faces are supported by secondary structures already." Exactly so, and checkable: **24 of
those 48 ties lie IN the square face planes**, cutting each square into four triangles,
while the eight hexagons had nothing in plane at all. Each hexagon now carries **six radial
spokes**, and they are the same cut as every primary because the hexagon's circumradius
*is* the strut length. Third, the joinery itself: purchased pipe for the secondaries, and a
flat pad where the film meets each hub.

## What the film does to the frame, which nothing had computed

Every strength number in this project was axial. The film, though, does not push on the
lattice — it *pulls on the boundary frame*, sideways. Writing that down for the first time:
each panel's membrane leaves the face plane at a fixed angle, and at a dihedral edge the
two panels' tensions **add along the bisector** rather than cancelling as they do inside a
flat face. With the hexagons bare that is **41,744 N/m** on a
251 mm rim member: 5,649 MPa of bending in a 10x8 pultruded
tube against T700's 2,500. **The rim tore off at 0.44
atmospheres** — the article could not have held half the load it exists to hold, and no
gate would have noticed, because the model computed no bending stress anywhere.

Spoking the hexagons cuts the panel, and bending falls as the **cube** of the bracing
pitch: the same edge drops to 13,915 N/m, and moving the 36 cell
edges to a 14x12 section takes the article to **2.84 atm**, a
margin of x1.89 on the 1.5-atmosphere design load.
Propping a spoke at midspan would reach 10.08 atm; that is the
next increment, priced and not yet built.

**And bracing buys something bigger than strength.** Each panel bulges *inward* by a
quarter of its half-span, and that dimple is open to the sky — the article displaces less
air than its outline claims. Unbraced, the bulges swallow
**21.8% of the enclosed volume**; spoked,
8.6%. On the bench that is cosmetic. On a floater, where mass and
displaced air are equal by construction, it is a fifth of the lift, and nothing in this
project was counting it. It is the strongest argument for bracing there is — stronger than
film mass, which is 28 g on a 2.8 kg article.

The **flat pad** on each hub is right for the reason the designer gave — a point support in
a 16-micron film is a puncture — but it is honest to say what it is not. A pad collects only
what the film's tension hands it around its perimeter: at 70 mm across,
806 N, against a hub share of 5,507 N. It is local
protection; the spokes do the carrying, and the tripod legs take
3,179 N each.

### Which member reacts which load — and the 96 that is not a member count

Until 2026-08-11 this analysis published **one** axial demand, 3·p·SF·V/(96·L), and the joint
manifest priced all 432 member-ends at it. The comment beside the divisor read "96 = 60 octet
+ 36 rim" — which is a true member count, since before the spokes existed the article held
exactly 96 long members. **It is simply not what the divisor means, and the two 96s have
nothing to do with each other.** Read as a member count it handed the crush to the rim, whose
24 vertices are dual-lattice sites: *not one rim member is an octet strut*, so it could never
have had a share of the crush at all. And it made the 48 hexagon spokes look like an omission
to be repaired by writing 144, when in fact they had simply never been given a demand of
their own and had inherited the octet's. `check_assembly` called that fabricating a
numerator, and it was — for four families, not one.

**So the 96 is right, and it is worth saying why before someone "corrects" it to 144.** The
divisor is the φ in σ = 3p/φ, so it counts the octet lattice's own strut-*lengths* per
Kelvin-cell **volume**: the lattice is FCC at half-pitch, so it runs three struts per cubic
half-pitch, and a cell of span four half-pitches encloses 32 of those — 3 × 32 = **96**,
exactly. (Clip the infinite lattice against the cell and the measure is 102 strut-lengths, of
which the 6 lying *in* the six square faces belong equally to the cell above: 96 again.)
Putting 144 there would dilute the octet's stress with members that are not in the octet, and
this article's numbers would stop agreeing with the array's — the one thing the demonstrator
exists to prove.

What the article carries is **two load sets that do not mix.** The crush is the array's
hydrostatic field, and only the octet takes it: at even n the whole boundary apparatus does
not exist and the same octet carries the same load. The film is the standalone article's
alone, and each panel's pull splits into a normal resultant — which the ⟨100⟩ props and the
four struts at each square centre react *exactly*, node by node — and a self-equilibrated
in-plane pull q = T·cos α, whose path is genuinely indeterminate between a face's radial
member and hoop around the rim. Both are therefore sized for all of it.

These are statically admissible **envelopes**, not a solved frame — each family carries the
whole of a path that could load it, which is the only honest treatment of an indeterminate
split, and bending stays where it belongs, in the rows above. They were checked once against
a linear pin-jointed solve of all 216 members under the same two load sets: the tripod prop
comes out exact, the spoke and the ties sit just above the solve, the rim comfortably above,
and the octet's array crush far above anything a standalone article puts through it.

| family | axial demand, SF 1.5 | what it reacts |
| --- | --- | --- |
| 60 octet | **3,372 N** | the array's crush, 3pV/(96L) |
| 36 rim | **4,471 N** | the film's in-plane pull, as hoop for two hexagon rings |
| 48 hexagon spoke | **2,235 N** | the hexagon's radial tributary of that same pull |
| 24 tripod prop | **4,769 N** | the hub's H/3 through three legs at 54.74° — exactly p·a²/2 |
| 24 vertex inward tie | 4,769 N | 2H/9 + Q/6 at a rim vertex: the same p·a²/2, reached independently |
| 24 in-plane square tie | **5,031 N** | that vertex's square share, p·a²/3, plus the square panel's radial pull |

These are quoted at the span the printer chain produces, 708.540 mm. `check_assembly.py`
prices the same six families **0.13% higher** because the article is not cut at that span: its
half-pitch is rounded to 177.25 mm, so it spans 709.000 mm exactly, and a crush demand goes as
span². The prover asks for the demands at the span the part was actually cut for, which is the
conservative direction and the only one that describes the article on the bench. Two spans,
one derivation, and the difference is 4 N on the octet.

**Three demands moved and two of them moved against us.** The rim's rises by a third, because
it was being handed a crush share it cannot carry and does not have. The governing short
member is no longer the hexagon tripod but the **in-plane square tie**, which takes the
sizing load for all 72 ties from 4,769 N to 5,031 N and their Euler margin from ×2.58 to
**×2.45**. The spoke, which had nothing, now has 2,235 N and ×2.75; the rim holds
**×4.12** at 14×12. Nothing in that correction made the article lighter or heavier —
mass was untouched by it, because not one cut length or section changed.

**And one result that is not a margin.** In the *standalone* article the octet only sees
**1,124 N** — the square face's centre share, entering through four struts at 45° — because
the boundary frame carries the rest around the outside. The 3,372 N is the *array's* number.
A strain gauge on a single sealed cell will read about a third of it, and that is a
prediction to check rather than a discrepancy to explain away.

**Tube, not rod; round, not hex; roll-wrapped, not pultruded.** Three sourcing questions
with arithmetic behind them. *Hollow* is the project's founding result and it holds at
article scale: at equal mass a 10x8 tube carries **4.6x** the Euler load of the solid rod
you could make from the same grams, and a rod sized to the actual load weighs 1.3-1.6x the
tube. Rods only win where buckling stops governing — below about six diameters of length —
and every member here is thirty to sixty diameters long. (The one place rods do belong is
the floater's level-2 boom chords at ~1.7 mm, where no tube can be made.) *Round* beats a
hexagonal section by **9.4%** on Euler at identical mass, and by far more on the flight
article, where the wall is thin enough that local buckling co-governs and a flat face has
no curvature to stabilise it; hex would buy anti-rotation and a flat bonding land, and we
need neither. *Roll-wrapped* is the correction: a **pultrusion is all-axial fibre**, and
this model has assumed a cross-plied wall since ORTHO_PENALTY was written — 0.75^0.75 *
0.25^0.25 is precisely the value for three-quarters axial, one-quarter hoop. An all-axial
wall scores 0.370 against that 0.570, so buying pultruded tube would have contradicted our
own physics by a factor of 0.65 on local buckling, and would split at the sockets, where
the spigot and its crush ribs press outward on hoop fibre that a pultrusion does not have.
The vendors are right to warn against pultruded drone arms, and for the same reason.

**Two SKUs, and the designer was right for the wrong reason.** He proposed the secondaries
be a *smaller* carbon pipe. Carbon yes; smaller no — sized against the load they actually
react, the ties come out ABOVE the octet's own crush demand, the most heavily loaded
members in the article, and a 6x4 tube buckles at half their load. So every member is the
same 10x8 roll-wrapped tube, except the 36 rim edges at 14x12:
**216 cuts, 1.95 kg** — billed at the saw table at last: 39.8 m across nine measured
lengths, where the old bill priced the 48.8 m of centre-to-centre spans as if they were
cuts (P14's standing finding, closed 2026-08-12; the spans still do the Euler physics) —
with x2.45 Euler on the ties. 1.69 kg of printed plastic became 1.95 kg
of carbon that is stronger. The hybrid article now weighs **2.69 kg**.

The 51 printed joints are **weighed, not budgeted**: gen_nodes.py integrates each one
from its own field and the article reads the manifest — **0.71 kg** since the sunken
boundary frame (2026-08-11). The arc of that number is the design's own history: the old
15% rule asserted 0.42, the first generated geometry measured 0.73, the pilot redesign
brought it to 0.47 — 153 g saved on 332 shortened spigots, 112 spent on real seats and
cups — and then the sunken frame spent 0.25 kg buying back what the mating planes had
been amputating: every socket whole, a land post per boundary joint pinning the film to
the true face, and the full seat annulus at all 432 ends. Whole geometry is printed
material; the freeze bill priced it and the ledger caps it.

**Then 21 g of that came back, and it is worth naming what bought it.** Giving the 36 rim
members the 14×12 socket the stock build specifies — instead of the 10×8 every other member
gets — pushed the 24 rim vertices' slot base from 16.383 to 18.984 mm and lengthened their
arms to suit. All of it lands on those 24 joints: **+20.87 g there, −0.13 g across the other
27**, for +20.74 g on the article. Against the only budget that matters — 0.9569 kg/m³, the
air a cell has to displace at 2,500 m — 21 g over this cell's 0.1779 m³ is **+0.117 kg/m³,
12% of the entire wall, spent on 72 connections that did not previously exist**. The pilot
redesign is still 24% of the wall to the good and the joints stand 20 g below the ones they
replaced, so the direction of travel holds; but a wall budget that a single socket diameter
can move by an eighth is the measure of how little slack there is at this cell size.

None of that makes this article fly, and it was never meant to.
The bench article is **15.13 kg/m³**: its mass is 12.4 times displaced air at sea level and 15.8 times at 2,500 m.
Its structural sizing uses safety factor 1.5 against full sea-level pressure; the stock-tube path does not apply the closed-form local-wall check.
The all-printed variant is 7.48 kg, about 34 times its sea-level displaced air; it tests the printer chain.

**The finite article is a formula, not a floating design.** At unit subdivision, the level-two M60J-class result is **1.203 kg/m³**.
Air is 1.225 kg/m³ at sea level and 0.957 kg/m³ at 2,500 m.
The corresponding T700 density is 2.236 kg/m³; printed continuous fibre is 2.269 kg/m³.
The sizing uses safety factor 1.5 against full sea-level pressure and local-wall knockdown 0.30.
Odd subdivision counts need boundary members because the hexagon planes contain no lattice sites; even counts have sites in those planes.
Boundary joints, the membrane and the higher-level struts still need a drawn and tested design.

**The joints are now grown, not modelled.** `tools/gen_nodes.py` builds every joint in
the article from one rule — a signed distance field that smooth-min-blends a capsule
stub along each incident member into a solid core, then subtracts the bore the purchased
rod glues into — and extracts the surface with surface nets into watertight STL, one per
node: 51 files, all closed, straight to a slicer (`make nodes`; `make check` verifies
the manifest against the same lattice counting this note uses). Change a diameter and
every node regrows; that is the "computed smoothing" the designer asked for, v1. The
generator also *measures* what the 15% node budget only assumed, by integrating each
node's own SDF: at v1's deliberately chunky parameters (26 mm engagement, 9 mm cores)
the 51 nodes weigh 0.73 kg printed — well over the budget's 0.42 kg for the hybrid,
recorded here rather than smoothed over; engagement, wall and core are now dials with a
gate on them instead of a hope. **Capture is INTERNAL by default — the designer's call:
pipes slide OVER a hollow printed spigot sized to the tube's bore (the mandrel side, the
precise surface), butt against a full-width annular seat, and an outer cup closes around
the cut end so the pultrusion cannot splinter — the arrow-insert pattern, which arrows and
kite ferrules have proven on exactly this class of tube.** The manifest still carries the
joint arithmetic at the octet's 3,372 N for *every* end — which the per-family table above
now says is the wrong load on 156 of the 216 members, four of them worse than 3,372 and one
of them better; rewiring the manifest to read the family's own demand is
`check_assembly`'s P12, and it is open. It carries it twice, because the article has two
joints: a tree end bonds 581 mm² over both surfaces and a closing end 113, so the glue line
runs 5.8 MPa at one and 29.8 at the other against a deliberately lowball 10 MPa epoxy
allowable. Axial load rides the seat and the glue rather than the spigot's own section —
and the printed-section margins quoted honestly (×0.98 XY / ×0.5 Z on the spigot section
alone) are exactly what E5's single-joint crush coupon exists to interrogate, one coupon
per engagement now; the CF-ferrule variant (an 8×6 stub tube as the spigot, load
running carbon-to-carbon) is the recorded escape if the coupon votes no.

**Most of the members cannot be slid on at all, and that is a property of the graph.** 51
nodes and 216 members give a cycle rank of 216 − 51 + 1 = **166 closing members**: only 50
members ever have a free end, and the other 166 have to drop between two nodes already
fixed in space, into a gap that equals their own cut length. Twenty millimetres of spigot at
each end has nowhere to go. Nothing springs it in — the pin-jointed frame wants 116–227 kN
for 20 mm, and 200 N of hand force buys 0.02 mm — and nothing tilts it in either, because a
socket engaged 20 mm with 0.30 mm of diametral clearance permits 0.86° where 24.5° is
wanted. So engagement is **per member-end**: the 100 tree ends keep the full 20 mm, and the
332 closing ends get a **2 mm pilot in a 2 mm cup**, against a swing-in bound of
s ≤ 0.75(2D)^⅔P^⅓ = 2.80–3.23 mm on this article's own cut lengths. The cup is what keeps
that from being a bare 2 mm spigot: it captures the pipe on its outside as well, in the
node, where the alternative was 166 external sleeves. It costs pull-out — a closing end
holds 763 N at the 10 MPa line against a tree end's 5,115 — and `check_assembly.py` freezes
that number rather than hiding it.

**And the pilot alone is still not enough, because the pipe has ends.** Tilting a member by
φ pulls each end back from its seat by P(1 − cos φ)/2, but swings its end-face corner
R_o sin φ the other way — and below about 4R_o/P, which is 5.3° on the long cut, the corner
is inside the seat at *every* axial position. A square-cut tube whose length equals the seat
gap cannot be rotated down through the last few degrees at all, at any pilot depth. So the
closing members are cut **0.15–0.25 mm short at each end**, derived per cut length by
`gen_nodes.swing_relief` and published on every cut-list row; the sweep in `check_assembly`
puts the pipe at the pose the kinematic identity gives at each tilt and confirms all of them
clear, tightest approach 0.007 mm. What that costs is stated rather than absorbed: a closing
end no longer butts dry on its seat, it butts through a 0.15–0.25 mm bondline, so **E5 must
crush a glue-filled butt as well as a dry one**.

**And the joint has an assembly constraint no picture can show, which the designer
reasoned out before any render could.** The pipe seats in an annular slot; two arms at
angle theta have their SLOTS intersect until the slot starts far enough out. Cut
both anyway — the field subtracts last, so both win — and the part prints with each slot
bored through its neighbour: the pipe fouls on the remains and never reaches its shoulder,
and you find out with glue on your hands. The tightest pair in this article is 45 degrees
(a tie against an octet arm). The rule now takes the worst of four feature pairs rather
than one, and the seat collar is the pair that governs, so the slot begins as far out as
**19.8433 mm** where it began at 10.0 — and it is per node, not per article: a rim vertex
holding a 14 mm tube's collar clear of a 10 mm one needs that much, while the rest of the
article spreads from 12.26 at the cell centre to 17.26, each node's own arms deciding
(the sunken frame tilts every boundary-adjacent arm a fraction of a degree, so even the
interior spread is measured, not assumed). That is what took the pipe–pipe interference at
a shared node from −1.32 mm of overlap to **2.2572 mm** of air. The slot start is computed
per node from the node's own arms and gated end by end.

**What is proven about these joints, and what is not.** `tools/check_assembly.py` measures
all **432 member-ends** out of the generator's own field on every run — not one calculation
reprinted 432 times — and `research/geometry/nodes/contract.json` caps what it finds: for
every end and every one of the **51 nodes**, the arm axis, the slot base, the engagement, the
clearances, the insertion slack, the demand and capacity of every load path, and the pass
state of every check, generated by `--freeze` and never typed. A later run recomputes all of
it and fails naming any member-end whose properties moved, which is what makes optimising
these joints for weight safe to start: shrink a node and quietly take engagement with it, and
the build goes red with the arms named. **12 of the 16 proofs pass**, and they are the ones
assembly turns on — every one of the **332 closing ends** carries a pilot inside its own
swing-in bound and none is at the full stub, and the swing is now swept end by end rather
than sampled; the seat is a real land of **28.274 mm²** — the
whole pipe annulus, at every one of the 432 ends now that no mating plane cuts a socket —
rather than the blend fillet the pipe used to come down on; the crush ribs survive the slot that used to delete them; no
slot starts closer than the declared **0.500 mm** to the feature it would foul; every pipe's
own annulus is empty for its whole travel; and every member-end is priced at a load derived
from the path that puts it there rather than at one number wearing 432 hats.

**0 rim member-ends have a socket drawn for the wrong tube**. The stock build
specifies **14×12** for the rim, `arm_pipe()` draws that socket now, and
**10×8** goes everywhere else. It was 72 until 2026-08-11 — every rim socket four
millimetres too small for the tube the analysis buys, 2.15 mm of radial slop, and the cup
sitting inside the pipe's own bore. Those connections did not exist, and the designer found
it by eye in a render before any gate did.

The five proofs still failing are frozen at the value measured, which is how this repository
publishes a defect it has not fixed yet. **0 sockets are open-sided
grooves** since the frame sank (2026-08-11): a boundary node now settles beneath its mating
faces until every socket clears them whole — the worst of them keeps **1.000** of its
circumference where the old on-plane article kept 0.304 — and a printed land post carries
the mating flat back up to the true face, the pin the draped skin holds its shape by. What
the sink could not buy back is the pilot: **332
member-ends do not reach the 10 MPa glue line** in pull-out, which is the pilot's own bill and
is survivable only because every member in an evacuated cell is in compression and rides its
seat — something nothing in this repository yet computes. The sink also has a price of its
own, frozen at its measured size: every boundary-adjacent cut got shorter, the shortest tie's
swing now rides its cup mouth at less than a micron of interference on the symmetric
insertion path, and that one representative is capped until the cup gets a lead-in chamfer
or the sweep learns the builder's full freedom. And **0 margins have a demand and
no capacity at all**, where 888 did: bearing, dry pull-out and transverse shear are derived
or bounded now, and most of them fail. **316 margins are UNPROVEN** — bounded but
not decided — and each of those names the bench test that would settle it, one afternoon
each. No bearing allowable, no friction coefficient and no creep knockdown for this print
exists in any source we hold, so every parameter they would depend on stays frozen. The cap
does not make any of that go away. It makes the next change to these joints declare itself.

## The stock build: purchased pipe, printed joints

"Could this be assembled mainly from CF stock and 3d printed connectors??" — the
designer's question (2026-08-10), and the answer reframed the build, because the design
had already converged on it without saying so: **144 of the 216 members are the same
251 mm cut**, the nodes are already printed sockets a pipe end seats into,
and **roll-wrapped CF tube is the T700 laminate row as a catalogue item** — stock delivers
true laminate properties, which no chopped-fibre print does.

The hybrid article uses **180 cuts of 10×8 mm roll-wrapped pipe and 36 rim edges at 14×12**.
The octet demand is 3,372 N per strut, with safety factor already included.
Its Euler margins are ×1.8 pinned and ×4.3 with socket fixity; the stress margin is ×21.
Every other family has its own demand and margin in the table above.
All 51 joint masses are computed from geometry; none has been physically weighed.
The ties are carbon, so the printed mass is the nodes alone.
Film skin is 28 g at its halved span.
The computed total is **2.69 kg**, against 218 g of displaced air at sea level and 170 g at 2,500 m.
It does not float at either altitude.
Structural sizing uses safety factor 1.5 against full sea-level pressure; see the [ledger](../../docs/FLOAT-LEDGER.md) for the nominal-volume basis and missing adhesive, seams, barrier and hardware.
A prospective level-two alternative would replace the primary pipes with three-rod wound booms; that alternative still needs drawn struts, joints and load tests.
The 10×8 choice is deliberate: margins that hold pinned make socket fixity a bonus rather than an assumption.
E5's coupon crushes one pipe-plus-sockets to test that fixity claim.
