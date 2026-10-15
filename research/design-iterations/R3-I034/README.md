# R3-I034 — fixed raised guide crown

**FAIL/UNKNOWN; physical float NOT SHOWN.** Raising the guide departure to
z=18 m reduces the conditional rope force relative to the historical near-level
departure, but the complete paid construction is heavier, still intersects full
bags and other routes, and has unresolved receiver and connection mechanics.
This is one fixed construction, not an optimisation or a qualified load path.

**Inherited I030 correction UNREVIEWED; both original MEDIUM findings remain
OPEN.** The old square-RHS vector-magnitude stress is not a biaxial corner bound,
and the old scalar bolt proxy omits the bending-group distribution needed for a
conservative bolt bound. Neither is used as a new capacity result here. All new
section, bolt, weld, prying, fatigue and complete receiver capacities are UNKNOWN.

**I034 F1 correction implemented; targeted follow-up disposition pending.** The
initial MEDIUM finding remains OPEN until that disposition. It identified the
receiver-name prefix lookup omitting retained-path CG gravity from local records,
while the global paid inventory already included that stock. The explicit ID
mapping below repairs those records without a design or inventory change.

## Sources and fixed construction

The exact starting object is `99379c8b480a5ac1689177c455fd3f0b0bf89618`, tree
`6424e901617975b2cbf7a7c77c8bc7a729ac63b4`. The accepted
[I030 README](../R3-I030/README.md), [saved result](../R3-I030/hoop.json) and
[saved inputs](../R3-I030/baseline.json) supply inert data. The new
[baseline](baseline.json) records their full byte/hash bindings and selected
fields; [sources](sources.json) freezes every selected dimension and assumption.
[crown.py](crown.py) imports only the standard library and reads those two JSON
files. It never executes or imports an ancestor. [crown.json](crown.json) is the
complete saved stdout from the one directed correction calculation, including
every part, stock CG, interface, seam, geometry witness and all 32 route/state
rows. The correction parent is `9c4a811333b74b8480ddb46ec3b9e52ec58acbae`;
its original calculation and evidence remain a separate historical record.

The vehicle frame and handedness are unchanged: metres, +z up, clockwise from
+x viewed from +z. The crown radius is exactly 29 m and height exactly +18 m.
All saved station x/y values, including tiny coordinate round-off, are retained
in JSON. Coordinates below are rounded for display only.

```text
             eight curved RHS500 x 500 x 12 mm sectors, radius 29 m
 z = 18 m    Q_j ================================ Q_(j+1)
             [800 mm node]                     [800 mm node]
              | Q_j - (0,0,0.4) : main leg to R_j - (0.4,0,0)
              | Q_j + (0,0,0.4) : brace to R_(j+1) + (0.4,0,0)
              | 16 unsegmented RHS300 x 300 x 10 mm supports total
              v
          actual saved R_j + new 800 mm node/saddle stock
              -> retained rack/root -> retained pad AND curtain endpoint

 L (saved cradle) -> circular lower guide at G0 z=18
                  -> circular upper guide at saved G1 z=22.5
                  -> rope socket E -> nominal 1 m actuator -> fixed H
```

There are eight sectors, sixteen supports, sixteen node boxes, eight actual
receivers, sixteen new arms and eight routes. Each circular guide has 450 mm
bend radius, 600 mm guard radius, 60 mm axle and 120 mm bearing span. G0/G1 are
polygon-intersection datums, **not sheave centres**. The two tangent circles and
their centres are constructed afresh in 3D. The actuator interface is recomputed
as H minus one metre along the new final straight direction. The upper anchor H,
lower cradle L, host order and all four full bag centres/radii remain fixed.

| j | Receiver | Q_j (m) | R_j (m) |
| --- | --- | --- | --- |
| 0 | rack-1-root1 | (29.000000, 0.000000, 18.000000) | (2.400000, -29.000000, 0.000000) |
| 1 | rack-1-root3 | (20.506097, -20.506097, 18.000000) | (2.400000, -29.000000, 23.000000) |
| 2 | rack-1-root0 | (0.000000, -29.000000, 18.000000) | (-2.400000, -29.000000, 0.000000) |
| 3 | rack-1-root2 | (-20.506097, -20.506097, 18.000000) | (-2.400000, -29.000000, 23.000000) |
| 4 | rack1-root0 | (-29.000000, -0.000000, 18.000000) | (-2.400000, 29.000000, 0.000000) |
| 5 | rack1-root2 | (-20.506097, 20.506097, 18.000000) | (-2.400000, 29.000000, 23.000000) |
| 6 | rack1-root1 | (-0.000000, 29.000000, 18.000000) | (2.400000, 29.000000, 0.000000) |
| 7 | rack1-root3 | (20.506097, 20.506097, 18.000000) | (2.400000, 29.000000, 23.000000) |

| Host | G0 (m) | G1 (m) | L (m) | H (m) | Unloaded free stock (m) |
| --- | --- | --- | --- | --- | --- |
| 9 | (26.792506, -11.097820, 18.000000) | (-1.800000, -29.000000, 22.500000) | (15.770371, -1.035246, -0.176777) | (15.770371, -1.035246, 34.355095) | 90.000000 |
| 10 | (11.097820, -26.792506, 18.000000) | (-0.600000, -29.000000, 22.500000) | (7.138735, -1.035246, -0.176777) | (7.138735, -1.035246, 37.121633) | 76.000000 |
| 11 | (-11.097820, -26.792506, 18.000000) | (0.600000, -29.000000, 22.500000) | (1.035246, -7.138735, -0.176777) | (1.035246, -7.138735, 37.121633) | 67.500000 |
| 12 | (-26.792506, -11.097820, 18.000000) | (1.800000, -29.000000, 22.500000) | (1.035246, -15.770371, -0.176777) | (1.035246, -15.770371, 34.355095) | 83.000000 |
| 16 | (-26.792506, 11.097820, 18.000000) | (-1.800000, 29.000000, 22.500000) | (-1.035246, 15.770371, -0.176777) | (-1.035246, 15.770371, 34.355095) | 78.500000 |
| 21 | (-11.097820, 26.792506, 18.000000) | (-0.600000, 29.000000, 22.500000) | (-15.770371, 1.035246, -0.176777) | (-15.770371, 1.035246, 34.355095) | 76.000000 |
| 22 | (11.097820, 26.792506, 18.000000) | (0.600000, 29.000000, 22.500000) | (-7.138735, 1.035246, -0.176777) | (-7.138735, 1.035246, 37.121633) | 79.500000 |
| 23 | (26.792506, 11.097820, 18.000000) | (1.800000, 29.000000, 22.500000) | (-1.035246, 7.138735, -0.176777) | (-1.035246, 7.138735, 37.121633) | 89.000000 |

## Finite stock, joints and assembly

Each of the sixteen 800 mm boxes pays six 800×800×20 mm aluminium outer blanks
and two full internal diaphragm blanks. Whole blank masses are charged; corner
and diaphragm intersections receive no automatic notching or hole credits.
Their nominal outer faces, plate vertices and finite seam paths are exported.
No box is assumed perfectly rigid.

Each end of every main leg/brace pays a 400×400×25 mm endplate, two
400×400×20 mm backers, four 300×250×20 mm gussets and eight M24×180 mm shanks.
The eight bolt positions are the specified ±140 mm corner/edge pattern with
26 mm holes. Every bolt pays its 80×80×12 mm backer, two 48/26×4 mm washers,
36 AF×20 mm head, 36 AF×32 mm nut and 20 mm insertion/runout reservation.
All tube/endplate, box, diaphragm, saddle and gusset junctions have enumerated
12 mm nominal fillet paths. Full triangular bead stock is charged. Weld strength,
HAZ, access and fit remain UNKNOWN.

The endplate normal follows its actual member axis. Local v is projected vehicle
z (vehicle x only for a parallel case), and w=e×v. An oblique endplate is not
silently made coincident with a box face: each interface records both normals,
the tube-wall/bolt-hole conflicts and full finite blanks. The known 137 mm M24
stack is shorter than the selected 180 mm shank, but omits the unresolved mating
wall and oblique grip; it is not a bolt-fit or couple-capacity pass.

Each receiver pays two 800×600×20 mm aluminium saddle/doubler blanks with nominal
±x normals at the saved receiver datum, plus eight M24×500 mm through-shanks at
the specified ±200/±150 mm pattern. The distinct mating-face offsets and actual
old receiver-wall stack are UNKNOWN. The exported 112 mm known stack cannot
certify a 500 mm bolt across an unspecified grip. The nominal coincident blanks
are not a manufactured receiver adapter. Additional wall, rack, curtain and hull
spreading remains U/C.

All sixteen guide bodies/axles/bearings/guards/saddles retain their complete saved
composite mass and material volume, paid once and relocated to their new centres.
Their internal stock is not separated to claim an arm credit. The sixteen old
standalone arm rows are individually replaced by new RHS150×150×6 mm arms from
the actual guide centre to its own G0/G1. Both ends pay a 300×300×20 mm plate,
two 300×300×12 mm backers, four 250×200×12 mm gussets and four M20×140 mm bolts
on the 180 mm square. Each bolt pays its 60×60×10 mm backer, two 40/22×3 mm
washers, 30 AF×16 mm head and 30 AF×24 mm nut. The 104 mm known stack excludes
the unresolved fork or supporting-face grip. All arm/endplate/gusset seams are
paid. The real saved fork fit remains UNKNOWN; its force and moment are retained.

The retained eight four-cover/sixteen-shank splices are explicitly identified by
old part ID and paid once. Their 800×350×20 mm steel covers, sixteen M24×560 mm
shanks and 0.5 kg head/nut/washer allowance per shank remain. The new geometric
record retains holes, shanks, edge ligaments and full cover blank enclosures.
Only 20 mm remains beyond the known 540 mm plate/tube grip; the unspecified
head/nut/washer dimensions and new node intersections prevent a fit claim.

Every per-bolt backer, washer, head and nut is charged as steel; all named tube,
endplate, large backer, gusset, node and saddle blanks are aluminium. Hex heads
and nuts use whole nominal hex stock without bore credits. This material
accounting convention is explicit and grants no rating.

Four kilograms of isolation is paid per Q and R box; one kilogram of bonding
per R box; twenty kilograms of assembly/access stock per sector; and ten
kilograms of temporary brace stock per receiver. Existing named Q isolation,
bonding and sector assembly rows are physically retained/relocated once. The
new R isolation and temporary stock are added. No erection capability follows
from those allowances.

A 600 mm diameter × 800 mm guide access cylinder and a finite axle-removal path
are represented for each guide. Capsule tests conservatively enclose those
cylinders. Local mating overlaps remain in the record, together with all other
structure, guide, bolt, plate and assembly conflicts. No whole member or local
contact gets a blanket clearance exclusion.

## Paid comparison and complete conditional ledgers

| Quantity | kg |
| --- | --- |
| Accepted I030 known construction | 109538.038202 |
| Only named I030 conditional replacements removed | 7703.972146 |
| New stock added | 22890.287464 |
| I034 known construction + U+C | 124724.353520 |
| Increase from I030 | 15186.315319 |
| No-retirement construction + U+C | 132428.325666 |
| Penetration liners/cuffs retained | 1346.129043 |
| Qualified retirement count | 0 |

| New stock group | kg |
| --- | --- |
| node_box_full_blanks | 4423.680000 |
| nominal_fillet_welds | 94.556160 |
| node_isolation | 32.000000 |
| temporary_assembly_stock | 80.000000 |
| main_legs | 6408.683561 |
| connection_plates | 501.120000 |
| connection_backers | 739.584000 |
| connection_gussets | 725.760000 |
| bolts_backers_washers_heads_nuts | 759.484371 |
| braces | 8220.894139 |
| receiver_saddles | 414.720000 |
| replacement_rope_and_two_tails | 371.298383 |
| new_guide_arms | 118.506851 |

| Conditional removed group | kg |
| --- | --- |
| receiver_members | 6433.754361 |
| receiver_plates_gussets_pins_bolts | 768.928706 |
| eight_replacement_ropes | 390.273968 |
| guide_arms | 111.015111 |

The complete part-ID map is `mass.reconciliation`; new IDs, original and
relocated CGs, volumes and masses are retained alongside it. Only the old eight
receiver members, their explicitly identified complete end-joint rows, sixteen
standalone arms and eight rope rows are conditionally replaced. The sectors,
splices, all guide composite stock, rack frames, roots, pads, curtains,
crossbeams, lower cradle contacts, sockets and actuators remain paid. The prior
I026→I030 credit of 2,777.814438522 kg is **not subtracted again**. The
no-retirement column restores this unit's conditional removal credit; it does
not claim any previously unqualified retirement has become qualified.

The same inventory remains: helium 27,670.136440858 kg, impurity air
8,343.231319462 kg and fixed water 74,669.472503010 kg. The 17,000 kg equipment
convention, pressure hardware 8,666.759795158 kg with its original 2,000 kg
allowance counted once, 5,000 kg energy and 3,000 kg propulsion allowances are
unchanged. M20 means 3,000 kg payload plus that 17,000 kg equipment convention;
P100 means 100,000 kg payload plus the same equipment. No gas reset, water
release, bag shrink, pressure relaxation, payload relaxation or powered lift
is used. Each row below uses its own saved gross displacement and other-air mass.
Every margin still needs **U+C subtracted once**.

| Altitude m / superheat K | Case | Gross displacement kg | Other air kg | All-up before water kg | All-up with fixed water kg | Margin before water kg | Margin with water kg |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 / 0 | M20 | 277495.141642 | 71922.931460 | 252660.652741 | 327330.125244 | 24834.488901 | -49834.983602 |
| 0 / 0 | P100 | 277495.141642 | 71922.931460 | 349660.652741 | 424330.125244 | -72165.511099 | -146834.983602 |
| 0 / 10 | M20 | 277495.141642 | 64660.823942 | 245398.545223 | 320068.017726 | 32096.596419 | -42572.876084 |
| 0 / 10 | P100 | 277495.141642 | 64660.823942 | 342398.545223 | 417068.017726 | -64903.403581 | -139572.876084 |
| 2500 / 0 | M20 | 216753.347389 | 11121.997885 | 191859.719166 | 266529.191669 | 24893.628224 | -49775.844279 |
| 2500 / 0 | P100 | 216753.347389 | 11121.997885 | 288859.719166 | 363529.191669 | -72106.371776 | -146775.844279 |
| 2500 / 10 | M20 | 216753.347389 | 3403.098319 | 184140.819600 | 258810.292103 | 32612.527789 | -42056.944714 |
| 2500 / 10 | P100 | 216753.347389 | 3403.098319 | 281140.819600 | 355810.292103 | -64387.472211 | -139056.944714 |

| Altitude m / superheat K | Case | No-retirement raw margin kg | No-retirement fixed-water margin kg |
| --- | --- | --- | --- |
| 0 / 0 | M20 | 17130.516755 | -57538.955748 |
| 0 / 0 | P100 | -79869.483245 | -154538.955748 |
| 0 / 10 | M20 | 24392.624273 | -50276.848230 |
| 0 / 10 | P100 | -72607.375727 | -147276.848230 |
| 2500 / 0 | M20 | 17189.656078 | -57479.816425 |
| 2500 / 0 | P100 | -79810.343922 | -154479.816425 |
| 2500 / 10 | M20 | 24908.555643 | -49760.916860 |
| 2500 / 10 | P100 | -72091.444357 | -146760.916860 |

The enumerated paid subassembly contains 49834.983602 kg at nominal CG (0.044995, 0.018418, 15.826556) m. Every enumerated part has its own gravity wrench. The remaining 74889.369919 kg of unchanged whole-vehicle construction has no invented CG. Rope rounding-stock placement and actual loaded CG also remain UNKNOWN. This is not a complete vehicle trim calculation.

The represented material amount is 19.479767 m³ against the retained 50 m³ reserve within the original 100 m³ debit. This is a material accounting comparison. It does not establish routing fit, hydrostatic redistribution, sealed displacement or preserved physical lift; no new displacement or bag-capacity credit is claimed.

## Conditional route mechanics and unresolved receiving boundary

Only the saved host/state `unchanged_bag_duty_n` is reused as a duty. Tensions,
guide forces, support wrenches, extensions and commands are new. The nominal
traction is the vertical bag duty plus local lower deadweight divided by the
new upward departure cosine. The inherited factor 1.5 applies to that service
traction for the conditional rope/actuator screen; it does not certify dynamic,
connection or fatigue duty.

Each straight span's distributed gravity is balanced by half-weight endpoint
reactions; each circular bend and folded tail retains its own exact nominal CG
moment. The rounded surplus stock is paid, with a disclosed nominal half at each
termination. Its actual laid-out/loaded shape is UNKNOWN. This is a frictionless,
nominal equal-traction model with a statically balanced gravity allocation,
not a solved catenary with varying tension or loaded contact.

The unloaded free length is rounded up once to 0.5 m, excludes the nominal
actuator, and has two additional paid 1 m folded tails. It is not retuned by
state. For each of the three straight spans, transverse weight q gives positive
sag `q L²/(8 T)` and positive geometric excess `q² L³/(24 T²)`. The local
small-slope limit is 0.1. Rope elastic extension is `T Lfree/(E A)` and actuator
stretch is `T/k`. Compatibility is explicitly

```text
Lfree + elastic extension + command + actuator stretch
    = unloaded geometric rope length + nominal 1 m actuator + positive sag excess
```

The selected actuator stays at the saved stiffness 2,238,410.615108458 N/m,
conditional force rating 53,878.314009065 N and 0.8–1.2 m command interval.
The rope remains 18 mm, assumed E=50 GPa and working stress 150 MPa, density
1,440 kg/m³ plus 0.2 kg/m coating, within the 35 mm enclosure. Both bearing
locations and their conditional radial reactions are exported. Their axial
sharing, spin/friction support, contact, fork and fatigue ratings remain UNKNOWN.

All 32 route rows appear below. PASS here is only a local conditional screen;
it cannot override failed contact, unqualified connections or unsolved shape.

| Altitude / K | Host | T N | Rope extension m | Actuator stretch m | Command m | Rope | Actuator | Stroke |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0/0 | 9 | 27045.963923 | 0.191311 | 0.012083 | 0.669380 | FAIL | PASS (conditional) | FAIL |
| 0/0 | 10 | 36579.757480 | 0.218499 | 0.016342 | 0.334740 | FAIL | FAIL | FAIL |
| 0/0 | 11 | 33827.512966 | 0.179461 | 0.015112 | 0.348704 | FAIL | PASS (conditional) | FAIL |
| 0/0 | 12 | 38647.192111 | 0.252111 | 0.017265 | 0.610841 | FAIL | FAIL | FAIL |
| 0/0 | 16 | 36686.960218 | 0.226348 | 0.016390 | 0.662948 | FAIL | FAIL | FAIL |
| 0/0 | 21 | 36690.531541 | 0.219161 | 0.016391 | 0.659562 | FAIL | FAIL | FAIL |
| 0/0 | 22 | 41954.348529 | 0.262144 | 0.018743 | 0.395724 | FAIL | FAIL | FAIL |
| 0/0 | 23 | 38541.929089 | 0.269599 | 0.017218 | 0.666263 | FAIL | FAIL | FAIL |
| 0/10 | 9 | 24809.940334 | 0.175494 | 0.011084 | 0.686219 | PASS (conditional) | PASS (conditional) | FAIL |
| 0/10 | 10 | 33559.012494 | 0.200455 | 0.014992 | 0.354141 | FAIL | PASS (conditional) | FAIL |
| 0/10 | 11 | 31033.131939 | 0.164636 | 0.013864 | 0.364783 | FAIL | PASS (conditional) | FAIL |
| 0/10 | 12 | 35456.045558 | 0.231294 | 0.015840 | 0.633093 | FAIL | PASS (conditional) | FAIL |
| 0/10 | 16 | 33657.015376 | 0.207654 | 0.015036 | 0.683004 | FAIL | PASS (conditional) | FAIL |
| 0/10 | 21 | 33660.586699 | 0.201062 | 0.015038 | 0.679024 | FAIL | PASS (conditional) | FAIL |
| 0/10 | 22 | 38491.787399 | 0.240508 | 0.017196 | 0.418915 | FAIL | FAIL | FAIL |
| 0/10 | 23 | 35359.516349 | 0.247338 | 0.015797 | 0.689955 | FAIL | PASS (conditional) | FAIL |
| 2500/0 | 9 | 7101.424258 | 0.050232 | 0.003173 | 0.821005 | PASS (conditional) | PASS (conditional) | PASS (conditional) |
| 2500/0 | 10 | 9635.780466 | 0.057557 | 0.004305 | 0.508311 | PASS (conditional) | PASS (conditional) | FAIL |
| 2500/0 | 11 | 8902.622409 | 0.047230 | 0.003977 | 0.492478 | PASS (conditional) | PASS (conditional) | FAIL |
| 2500/0 | 12 | 10183.293377 | 0.066430 | 0.004549 | 0.809928 | PASS (conditional) | PASS (conditional) | PASS (conditional) |
| 2500/0 | 16 | 9660.923745 | 0.059605 | 0.004316 | 0.842371 | PASS (conditional) | PASS (conditional) | PASS (conditional) |
| 2500/0 | 21 | 9664.495067 | 0.057728 | 0.004318 | 0.833732 | PASS (conditional) | PASS (conditional) | PASS (conditional) |
| 2500/0 | 22 | 11069.527754 | 0.069166 | 0.004945 | 0.603085 | PASS (conditional) | PASS (conditional) | FAIL |
| 2500/0 | 23 | 10155.932877 | 0.071040 | 0.004537 | 0.878207 | PASS (conditional) | PASS (conditional) | PASS (conditional) |
| 2500/10 | 9 | 4575.306299 | 0.032364 | 0.002044 | 0.842478 | PASS (conditional) | PASS (conditional) | PASS (conditional) |
| 2500/10 | 10 | 6223.133930 | 0.037172 | 0.002780 | 0.531108 | PASS (conditional) | PASS (conditional) | FAIL |
| 2500/10 | 11 | 5745.707549 | 0.030482 | 0.002567 | 0.511251 | PASS (conditional) | PASS (conditional) | FAIL |
| 2500/10 | 12 | 6578.137933 | 0.042912 | 0.002939 | 0.836091 | PASS (conditional) | PASS (conditional) | PASS (conditional) |
| 2500/10 | 16 | 6237.883793 | 0.038486 | 0.002787 | 0.865931 | PASS (conditional) | PASS (conditional) | PASS (conditional) |
| 2500/10 | 21 | 6241.455116 | 0.037282 | 0.002788 | 0.856704 | PASS (conditional) | PASS (conditional) | PASS (conditional) |
| 2500/10 | 22 | 7157.745295 | 0.044724 | 0.003198 | 0.630149 | PASS (conditional) | PASS (conditional) | FAIL |
| 2500/10 | 23 | 6560.644341 | 0.045891 | 0.002931 | 0.906019 | PASS (conditional) | PASS (conditional) | PASS (conditional) |

| State altitude / K | Rope failures / 8 | Actuator failures / 8 | Stroke failures / 8 | Local sag-domain failures / 8 |
| --- | --- | --- | --- | --- |
| 0/0 | 8 | 6 | 8 | 0 |
| 0/10 | 7 | 1 | 8 | 0 |
| 2500/0 | 0 | 0 | 3 | 0 |
| 2500/10 | 0 | 0 | 3 | 0 |

For every state, `sectors` exports each complete applied wrench and the
required sum of its two end wrenches. `supports` exports all sixteen member/end
gravity requirements; each unresolved endpoint force and couple is null with an
explicit UNKNOWN equation. `Q_nodes` preserves node deadweight and incident
members. `receivers` follows all eight actual R datums through the retained rack
root, pad and curtain endpoint, including local gravity, both arriving supports
and unresolved upper-guide/rack sharing. `upper_guide_rack_wrenches` retains that
separate load input. No equal two-leg split, fixed receiver, free hinge couple or
inherited local stiffness is asserted.

The corrected receiver lookup uses these explicit saved identities. The three
suffixes in each row select the root strut, plate-pin assembly and curtain:

| Saved receiver | Paid retained part IDs |
| --- | --- |
| `rack-1-root0` | `rack-1-root-strut0`, `rack-1-plate-pin0`, `rack-1-curtain0` |
| `rack-1-root1` | `rack-1-root-strut1`, `rack-1-plate-pin1`, `rack-1-curtain1` |
| `rack-1-root2` | `rack-1-root-strut2`, `rack-1-plate-pin2`, `rack-1-curtain2` |
| `rack-1-root3` | `rack-1-root-strut3`, `rack-1-plate-pin3`, `rack-1-curtain3` |
| `rack1-root0` | `rack+1-root-strut0`, `rack+1-plate-pin0`, `rack+1-curtain0` |
| `rack1-root1` | `rack+1-root-strut1`, `rack+1-plate-pin1`, `rack+1-curtain1` |
| `rack1-root2` | `rack+1-root-strut2`, `rack+1-plate-pin2`, `rack+1-curtain2` |
| `rack1-root3` | `rack+1-root-strut3`, `rack+1-plate-pin3`, `rack+1-curtain3` |

All 32 receiver/state records now reference those existing paid parts through
`retained_path_part_ids`. Each `retained_members` record carries its saved mass
and CG, gravity wrench about R, and opposite required sum of external wrenches.
`local_known_gravity_wrench` includes both those three parts and the paid receiver
stock. Its `required_external_wrench_sum` requires **all** external forces and
couples on that assembly, transported about R, to balance the known gravity.
It does not assign all retained weight to R, determine a pad/curtain reaction,
solve internal sharing, or add that gravity a second time to the global total.
Receiver, pad and curtain reactions remain null/UNKNOWN. Baseline, declaration,
geometry, paid inventory, global gravity/first moments and mission ledgers are
unchanged. The original lookup failure and original result are retained in the
parent candidate; this text does not relabel that earlier calculation as corrected.

The total force/moment identity sums the ideal rope interface tractions to zero
and adds each enumerated paid part's gravity once. This verifies that nominal
internal action/reaction bookkeeping is closed. It does not solve compatible
frame/receiver reactions, whole-vehicle equilibrium, hydrostatics or trim. The
individual receiver forces/couples and all new section/connection capacities
remain UNKNOWN.

## Geometry, physical limits and next change

Every sector retains 32 enclosing chords; every guide arc uses 16, with explicit
analytic enclosure error. Straight-segment distance witnesses are exact for the
represented segments. All four complete bags, the hull, fixed pressure/hanger/
service hardware, all eight sectors/sixteen supports/sixteen arms, boxes, plates,
bolts, receivers and assembly/access envelopes are included. All 28 rope pairs
are checked. A sweep of enclosing AABBs removes only geometrically disjoint
pairs; local mating overlaps are counted and qualified, never silently exempted.

Negative conservative-envelope clearance is unqualified fit; it is not by itself
a proof that a full solid shape penetrates. A negative represented-axis upper
bound is separately identified as a stronger unloaded axis witness. Loaded
extension, receiver motion, contact and actual surplus-rope shape remain
UNKNOWN even where the conditional fixed-end sag envelope has clearance.

The selected `rope12-straight0` has a represented-axis gap upper bound of -12.457717 m to complete bag 3, with enclosure gap -12.492717 m. The saved result contains 92 new object/bag axis-intrusion witnesses; these are discretised witnesses, not a count of independent physical failures.

The minimum nominal rope-pair enclosure gap is -0.070000 m for hosts 10 and 11 (`rope10-straight1`, `rope11-straight1`). Finite node/plate/bolt/gusset and access overlaps and unresolved face/grip packing are retained in the detailed geometry record. There is no qualified receiver adapter or complete routing fit.

Trapped-bag/header/lower-trip pressure FAIL remains. Full loaded shape, membrane
and curtain load spreading, global equilibrium, trim, energy and mission closure
remain UNKNOWN. Physical float is NOT SHOWN. All inherited scientific/provider/
control qualifications remain attached to their original records; the new run
does not rehabilitate a historical failure or the unreviewed I030 withdrawal.

The weakest assumption is whether this paid sixteen-support crown can deliver
its couples into the existing racks without unsupported fixity or dominant extra
U+C. The single next **untested and unissued** change is one wider paid receiver
saddle connecting each crown support into both existing same-rack upper and
lower receiver levels, with its full additional stock and compatible load
sharing. It was not built or run here.

One initial calculator invocation produced the parent result. Exactly one
additional directed correction invocation produced this saved result (two total);
its execution began from the parent candidate with the new source/input hashes.
No geometry tuning, ancestor execution, separate scientific validator, compile
or bytecompile preflight, drawing or preview was used for this correction.
The source and input hashes in `crown.json` identify that calculation; they do not
claim it executed at a later governed commit. No signature or landing is inferred
from the calculation or this document.

