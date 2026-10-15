# R3-I037 — wider split steel saddle at the finite A/B cuffs

**FAIL / UNKNOWN. Physical float is NOT SHOWN.** The fixed saddle adds 217.279447 t of paid stock and conditionally displaces 116.555358 t, increasing the known hull by **100.724090 t**. The calculation records 169 positive material witnesses and 32 requested weld edges without finite backing for the specified fillet. All 31 predecessor tubes, their 62 plate locations and their existing failures remain. Neither the wider plates nor the nominal bolt lengths establish a usable connection.

The unit is one fixed load-introduction change at the actual saved A/B cuffs. It does not solve a new aircraft, pressure system, frame or mission. Qualified retirement is **zero**; additional U+C, mission hardware, equipment/payload, global loaded shape and complete all-up mass remain unknown. The fixed-volume structural-vacuum comparison is separate from the helium/internal-envelope branch.

## Reproduction and saved evidence

From the repository root, the one calculator entry is:

```sh
python3 -I -B research/design-iterations/R3-I037/saddle.py --write
```

The source is [saddle.py](saddle.py), the saved result is [saddle.json](saddle.json), the inert input is [baseline.json](baseline.json), and exact predecessor hashes and assumptions are in [sources.json](sources.json). The predecessor is [R3-I033](../R3-I033/README.md), with the earlier [R3-I029](../R3-I029/README.md) limits still carried. Inputs are saved JSON and source byte hashes; no ancestor calculator is imported or executed. The input assembly copies the saved current I033 mass record, not the older I029 mass basis nested in its baseline.

One construction, two pressure alternatives and 37 gravity orientations produce 74 keyed states. Stock is repeated across 74 physical modules once. Pressure alternatives do not double the physical bill. There is no sweep, optimizer, stiffness solver, drawing or new material qualification. The recorded run used the bounded single-process execution route; its private run and governance receipts are separate from these public reproduction paths.

## Fixed construction and actual receiving surface

Coordinates use right-handed X/R/T, with X cross R = T and common moment origin O=(40,0,0) m. Local (x,r,t) is relative to the stated receiver centre. The existing cuff axes are T.

| Datum | X m | R m | T m |
|---|---:|---:|---:|
| A | 78.04226065180615 | 10.946997454842448 | 0 |
| B | 78.04226065180615 | 9.678968752678204 | 0 |
| C, retained | 79.38734135035827 | 3 | 0 |
| D, retained | 77.56673239365855 | 12.206171277810425 | 0 |

Each inherited receiving cuff is **0.400 m long**, outer radius0.164 m and inner radius0.148 m, ending at t=±0.200 m. These are the saved active bodies131 and136. A new1.200 m wide bridge does not turn the existing cuff into a1.200 m support. Cuff-to-ring attachment, local stiffness, ovalisation, bearing, peel, slip and rotation capacity remain UNKNOWN. The old yoke and old ring-node locations are not substituted for the saved cuff centres.

The following is paid at **each** receiver; both assemblies are identical in local dimensions.

| Component | Frozen dimensions and placement |
|---|---|
| Two saddle halves | Full0.180 X ×0.800 R ×0.400 T blanks; x=[−0.180,0] and[0,0.180], r=±0.400,t=±0.200; common T-axis bore radius0.166 m |
| Two liner halves | Polymer shells between radii0.164 and0.166 m over the full0.400 m cuff length; assumed density1200 kg/m³ |
| Two bridge plates | 0.030 X ×0.800 R ×1.200 T; x=[−0.265,−0.235] and[0.235,0.265] |
| Eight M30 ties | X axes at r=±0.300 m and t=−0.150,−0.050,+0.050,+0.150 m;0.700 m under-head stock,0.034 m holes through the halves and bridges |
| Each M30 head/nut/washers | Head45 mm AF ×20 mm; nut45 mm AF ×40 mm; two60/34×5 mm washers; full nominal threaded shank stock |
| Sixteen independent tie backers | Each80 R ×80 T ×12 X mm, two per tie; separately paid |
| Sixteen tubular spacers | OD60/ID34×55 mm, one each side of each tie, x=[−0.235,−0.180] or[0.180,0.235] |
| Four web plates | 55 X ×20 R ×400 T mm; centres x=±0.2075,r=±0.390,t=0 m |
| Existing incoming plate | Retained350 R ×350 T ×25 X mm end1 plate, centre x=−0.2775 m; its +X face meets the negative bridge at x=−0.265 m |
| Eight replacement M24 sets | 0.120 m under-head shank; head36 mm AF ×20 mm; nut36 mm AF ×32 mm; two48/26×4 mm washers; matching26 mm bridge holes |
| Existing end1 backers | Eight80×80×12 mm backers retained and charged once, placed behind the new negative bridge; no free new backers |
| Two detachable steel tools | Each200 X ×80 R ×80 T mm; initial centres(−0.450,−0.300,0) and(−0.450,+0.300,0) m |

The M24 pattern is (r,t)=(±0.120,±0.120),(±0.120,0),(0,±0.120) m. Other60 feet and their hardware remain. The receiver tubes, their end0 assemblies, end1 plates/backers/perimeter welds remain. Geometry is retained even where it cannot be installed.

Steel density7850 kg/m³, E200 GPa and nominal355 MPa are explicit assumptions/comparisons. They are not bolt, weld, contact or assembled-structure allowables. No liner modulus, friction, adhesion, preload or compression capacity is invented. Full blanks and full hex head/nut stock are paid without bore or drilling-scrap credit. Finished material tests subtract bores/holes; removed material does not become a load path. Full paid stock at declared bookkeeping centres is the gravity assumption, including paid trim and detachable tools; this is not proof of their installed centres of mass or an erection sequence.

## Bolt stacks, contact and weld boundaries

`geometry.stacks` enumerates every set; all coordinates below are local x in metres. For M30, the negative head lies[−0.302,−0.282], washer[−0.282,−0.277], backer[−0.277,−0.265], bridge[−0.265,−0.235], spacer[−0.235,−0.180], and saddle half[−0.180,0]. The positive half/spacer/bridge/backer/washer continue to+0.282, with nut[0.282,0.322] and tip at+0.418. The saved beyond-nut projection is0.096 m. This passes only the nominal length identity. Thread engagement, tightening, clearance and load capacity remain UNKNOWN.

For M24, the head lies[−0.314,−0.294], incoming washer[−0.294,−0.290], retained plate[−0.290,−0.265], bridge[−0.265,−0.235], retained backer[−0.235,−0.223], back washer[−0.223,−0.219], and nut[−0.219,−0.187]. The120 mm shank ends at−0.174, with0.013 m beyond the nut. That tip enters the fixed saddle region. No bolt is shortened and no extra pocket is cut to hide the conflict.

Each spacer has two independently identified compression contacts. A sleeve does not provide tensile capacity. The two liner interfaces, split planes, bridge/web cuts, each tie, each M24 connection, each weld edge, incoming plate interfaces and cuff-to-ring cuts have separate records. A nominal interface does not determine contact pressure or sharing.

All spacer end circles and web connecting-face edges are listed once with12 mm equal-leg fillet stock. The saved result has **96 actual meeting-steel line records** and **32 unsupported requested edges** per module. A web edge at an outer R boundary, or at a saddle T end, lacks receiving steel outside the edge for the specified fillet. Those requested weld lengths remain paid as uninstalled stock; they are not called actual perimeter welds or given strength. The96 meeting-steel lines still have UNKNOWN fabrication, distortion and combined weld-group capacity. Full fillet volumes and access sweeps are not a demonstrated interference-free assembly.

## Finite geometry result

The positive test uses strict interior material witnesses in a fixed125-point grid over a pair's common enclosing box. Boxes, finite tube walls, annuli, cylindrical bores, nominal holes, retained node shells and saved curved ring material are represented explicitly. Hex tests use only the orientation-independent inscribed material core. Threads, hex corners, missing hardware poses, unknown apertures, weld volumes and trajectories are not converted to clearance PASS. A bounding-box overlap without a material witness remains UNKNOWN; the finite sample is not a complete intersection solver.

All new bodies and independently positioned retained end1 backers are checked against one another and all represented retained active bodies. The retained set includes all62 end plates, saved finite tube walls, side-node shells, covers, other saddle plates, source adapters, active legacy solids and the saved continuous AD plate. `fit.unknownRetainedGeometry` names remaining geometry gaps. The saved62-foot records in `geometry.retained62Feet` preserve predecessor locations and historical metadata: their old receiver-end1 hardware IDs and substrate descriptions are superseded by the current stacks and displacement ledger, not retained as live old M24 sets.

There are **169 positive pair witnesses**. Examples include M24 tips in the negative saddle, new wide bridges against root end plates, and the saddle against retained fork/gusset/stanchion material. One explicit witness is:

```text
A saddle half -1 / A end1 bolt0 M24x120 shank
XRT = [77.86286065180614, 10.817397454842448, -0.12480000000000001] m
opposite cap = [-77.86286065180614, 10.817397454842448, -0.12480000000000001] m
```

The reflection Q=diag(−1,1,1) preserves material intersections, as do the37 sector rotations; each positive witness has its opposite-cap image recorded. This does not prove neighboring-sector, cross-module, insertion or wrench-access clearance. The original tube failures remain independently visible in `inheritedFit`: negative root-BD-B cut, noncoplanar feet, missed bolt material, crossing tubes, independent plate conflicts and retained-material witnesses. Nothing in this unit repairs those failures.

## Rowwise replacement and mass

`stock.beforeRows` names every I033 new-stock row and every matched I029 row. `stock.retainedI024Rows` preserves the older replacement history separately. Only the following20 identified rows are eligible for this unit's conditional subtraction; no other row is removed numerically.

| Source | Displaced row(s) | Boundary |
|---|---|---|
| I029 | 58,63,71,76 | Four old A/B machined clamp-half blanks |
| I033 | new-108 through new-121 | A/B doubler plates, their perimeter stock, gusset blanks/edge stock and old four-set M30 replacement kits |
| I033 | new-389,new-398 | Old eight end1 M24 complete sets at each receiver |

Old reinforcement59/64/72/77, liners68/81 and tie backers70/83 lose their old local contact function but remain fully charged. The unsplit old pooled weld row111 also remains charged; its active/displaced fraction and location are unknown. These accounting-only rows total **10.824622 t**. No guessed mass is subtracted, and no displaced component simultaneously supplies an installed load path. The retained end1 backers new-390/new-399 are expanded into their eight explicit positions each without charging them again.

Every new part, complete bolt component, washer, independent backer, spacer, liner, tool and actual/requested weld stock has a separate row in `stock.newItems` (376 rows). The exact20-row subtraction is in `stock.conditionalDisplacedRows`; all physical names and original dimensions/masses are retained there. Already superseded historical rows are neither reactivated nor retired a second time.

| Ledger, all74 physical modules | Tonnes |
|---|---:|
| Predecessor conditional hull | 6478.234514991365 |
| Added saddle stock | 217.279447391278 |
| Conditional identified subtraction | 116.555357500243 |
| Net hull increase | 100.724089891035 |
| New conditional hull | 6578.958604882400 |
| Residual gas, once | 8.086383338156 |
| New conditional known subtotal | 6587.044988220557 |
| No new I037 retirement subtotal | 6703.600345720800 |
| Carried I033 no-retirement subtotal plus new stock | 7130.917592167977 |
| Fully unretired historical subtotal plus new stock | 7561.583690396456 |
| Qualified retirement | 0 |

The no-retirement bounds are **alternative accounting cases**, never additions to each other or to the selected subtotal. Where displaced stock is carried, its storage and gravity placement are UNKNOWN; these cases are not demonstrated assembled configurations. The original I033 fully unretired historical subtotal7344.304243005178 t remains in the saved predecessor record, distinct from the updated bound that adds this unit's new stock.

The volume remains668852.7245692962 m³. The fixed lift and resulting known margins are:

| Altitude m | Fixed lift t | Conditional known margin t | No new I037 retirement margin t | Fully unretired historical margin t |
|---|---:|---:|---:|---:|
| 0 | 819.352791739 | -5767.692196482 | -5884.247553982 | -6742.230898658 |
| 2500 | 640.002052834 | -5947.042935387 | -6063.598292887 | -6921.581637563 |

Every margin still requires subtraction of additional U+C and mission/equipment/payload obligations. Unknown additions are not zero. No displacement gain, qualified saving or physical float follows from this mass comparison.

## Wrenches and 74-state boundary

`pressureAssignments` retains both saved f0/f1 source assignments, actual application points and all couples. The pressure basis121590 Pa and polar force58.362305820542 MN per cap remain unchanged; old incoming-boundary loads remain distinct, and the whole-end611 MN value is not reapplied. The button force and signed couple−93334.26148915867 N m are included once.

For each keyed state, known placed-stock gravity is summed once with the fixed external pressure/film source wrenches about O. Moment transport is **M_Q=M_P+(P−Q)×F**. Polar force/position reflection uses Q=diag(−1,1,1); axial moments use det(Q)Q=diag(1,−1,−1), followed by the actual sector rotation. Opposite-cap moment origins are reflected too.

The known placed-stock subset is 16948.829942877 kg per module. Another 146.278676550 kg per module is charged with unknown placement. Their mass reconciliation residual is 2.0747847884194925e-12 kg. This is an accounting identity, not a structural equilibrium or capacity proof. Older hull/global gravity and the unplaced charged stock's wrench remain unknown. Consequently the complete external and complete receiver-pair wrench fields remain null, alongside a separately labelled **known-subset** required receiver-pair wrench.

For saved state `f0-s00`, the known-subset external wrench is:

```text
F_XRT = [-1646438.5575694966, -166211.2431593145, 0.0] N
M_O_XRT = [51.17048206400253, 1.0244548320770264e-08, 7405704.303081428] N m
required receiver-pair force = [1646438.5575694966, 166211.2431593145, -0.0] N
required receiver-pair moment about O = [-51.17048206400253, -1.0244548320770264e-08, -7405704.303081428] N m
```

The opposite wrench acts on the supporting structure. Neither A nor B is assigned half. Each state's252 new boundary records contain their listed components' own-stock gravity wrench about the named point and explicit null complete force/couple fields. Reusing a component's self-weight at several diagnostic cuts does **not** add that mass repeatedly to the external load ledger. The common boundary geometry and31-member/62-foot/12-node unresolved demand templates are stored once and referenced by state. A boundary's own-weight wrench is not the solved force on that contact.

The known total pair moment expressed at A or B is explicitly labelled the **entire pair expressed at that origin**, not an individual receiver moment. Source couples are not suppressed. Steel presence does not establish stiffness, moment fixity, contact, prying resistance or a ring reaction distribution. Bolt shear/tension, plate bending, weld groups, liner compression, cuff stresses and the complete member/frame response remain UNKNOWN wherever unsolved. No source-applied force is silently interpreted as a bolt reaction or tension sign.

## Carried limits and next hypothesis

All prior pressure, film, root, stanchion, footprint, barrel/midcap, assembly/access, receiver/ring, global-stiffness and loaded-shape failures or unknowns remain. In particular the saved68.639 MPa film comparison against50 MPa,22798.125 MPa button-strip comparison, AD-A pin/BD-carbon collision, stanchion socket1–3/cuff1–8 and footprint1/17 failures are not closed by a saddle change. Existing I029 foot-bolt distribution and vector-norm stress claims stay withdrawn; their corrected complete capacities are UNKNOWN. The predecessor's original control/provenance and review limits also remain; this unit does not retroactively repair them.

**Weakest assumption:** the actual finite cuff and its ring attachment can accept the saddle's complete3D force and moment without unproved slip, rotation, ovalisation or peel. Individual A/B reaction sharing and those capacities are still unknown, and the fixed construction already has finite fit failures.

**Exactly one next untested change:** a separately paid local ring doubler/diaphragm tied to the actual saved receiving frame at the same A/B datums. Its geometry is not selected or calculated here. Physical float remains **NOT SHOWN**.
