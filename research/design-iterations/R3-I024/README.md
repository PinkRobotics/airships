# R3-I024 — One spaced polar-node construction

**The selected assembly fails.** Separating the real pin axes clears the represented pin pairs, but other material intersections and insertion obstructions remain. The selected AD blank cannot contain its transverse eyes and the cartridge has zero-area eye/shoulder contact. The button support has a 40 mm gap at each attachment. Post rows 1–2 have proven hoop-cuff/foot material gaps; rows 1–8 place the source datum beyond the finite cuff. Three post rows have overlapping end sockets and two cuffs extend outside their carbon. The collector and receiver nominal screens also fail. No retirement, physical float, global pressure capacity, loaded-shape qualification or complete U+C mass is established.

The single hypothesis is that tangentially separating the pins, axially staggering the polar pair, replacing the short AD tube by a finite steel cartridge and adding a fully priced moment collector can remove the former coplanar interference without hiding the connection moments. The geometry below was selected once. Its failed dimensions were retained; no parameter sweep, successive enlargement, changed hull, improved material allowable or favorable pressure case was selected.

[Geometry and assembly drawing](geometry.svg) · [saved result](result.json) · [calculation](calc.py) · [drawing generator](draw.py) · [frozen comparison](baseline.json) · [source context](sources.json).

## Fixed comparison and pressure boundary

The fixed scientific comparison is corrected [R3-I020](../R3-I020/README.md), publicly represented by commit `84864c083961fad534419cd7145a99b696f84834`, tree `5fd7c075dc95a3292002d7d26c537bb7949b78ec` after mechanical repackaging with the I020 unit files unchanged at landing. Its complete saved result and seven file hashes are frozen in `baseline.json`; the calculation checks those files before using the saved inputs. No predecessor executable is imported or run. The corrected I020 button moment and separate series-foot accounting remain the comparison, including their FAIL/UNKNOWN qualifications. I016's targeted film-clip correction does not qualify the rest of that construction.

The unloaded envelope remains a D80 × 160 m capsule: R40 spherical ends joined by an 80 m cylindrical section. The polar construction repeats in 37 sectors at each cap, 74 modules total. The pressure is 121590 Pa. The 18 film bays and 666 columns per cap, their finite bar pins, circumferential hoops, terminal row and 3 m finite button remain unchanged. There are two actual incident bars at every row through row 17, including the incoming old bar at row 0, and one new incident bar at terminal row 18. The terminal button pressure is separate from that bar load.

The new polar tributary contributes 58.362305821 MN axial per cap, once. The old incoming boundary is separately (-2.555921, -0.850242) MN in axial/local-radial components. Local radial components are sector quantities, not a single global vector sum around a complete ring. The 611 MN whole-end load is never applied again. The only two assignments are `f=0` (the circumferential route takes the radial part) and `f=1` (that radial part joins the meridional route). Neither assignment proves the hoop or receiver can carry it.

## Actual displaced geometry

Use a right-handed local frame `(X,R,T)` with `X × R = T`, axial X, radial R and tangential T. Old scalar XR moments embed as T couples. Every new member axis is computed between its displaced pin centres. For another sector rotate R/T by `2π/37`; for the opposite cap reflect X in positions and forces and transform couples as axial vectors: `(Mx,Mr,Mt) → (Mx,−Mr,−Mt)`. This reflection preserves the force/couple identity; it does not qualify an installed opposite cap.

The chosen D tangential planes are −500/0/+500 mm for AD/BD/DC. At C, DC is displaced −350 mm axially and +250 mm tangentially; BC is +350 mm axially and −250 mm tangentially. At the other ends AD_A and BD_B are −250 mm tangential, BC_B +250 mm. There are no drawing-only offsets. All eight pins are 100 mm diameter, 220 mm occupied length. Each local pin direction is the normalized component of T perpendicular to the actual member axis.

| Member | First pin (X,R,T), m | Last pin (X,R,T), m | Pin spacing m | Carbon cut m | Unit axis (X,R,T) |
| --- | --- | --- | --- | --- | --- |
| AD | (+77.739370, +11.242298, -0.250000) | (+77.619623, +11.910870, -0.500000) | 0.723759681 | steel cartridge | (-0.165451, +0.923749, -0.345419) |
| BD | (+77.589230, +9.978953, -0.250000) | (+77.569763, +11.906187, +0.000000) | 1.943477951 | 1.443477951 | (-0.010017, +0.991641, +0.128635) |
| DC | (+77.624933, +11.911871, +0.500000) | (+78.979141, +3.294300, +0.250000) | 8.726906773 | 8.226906773 | (+0.155176, -0.987471, -0.028647) |
| BC | (+77.670127, +9.389250, +0.250000) | (+79.659475, +3.289718, -0.250000) | 6.435199444 | 5.935199444 | (+0.309135, -0.947839, -0.077698) |

BD, DC and BC use 350 × 20 mm carbon tubes. Each actual carbon interval begins 250 mm behind its pin and ends 250 mm before the other pin. Each end has a 309/285 × 300 mm steel insert, 290 mm bond, 400 × 20 mm end plate and a 350 × 220 × 80 mm eye plate with a 102 mm hole. These six ends per module have sufficient axial insert separation in their own selected tubes. Their fit with other branches still fails.

Every pin sits between two 300 × 220 × 30 mm fork cheeks. Cheek centres are 58 mm either side of the eye plane, leaving 3 mm clearance at each face of the 80 mm eye. The cheeks extend from −200 to +100 mm along the member direction relative to the pin. Each pin has two 140/102 × 8 mm washers centred at ±77 mm and two 130/90 × 12 mm retaining collars centred at ±99 mm. The nominal 220 mm stock contains those envelopes; the actual retaining groove/lock and certification remain unqualified. The fork base is 400 × 300 × 30 mm, 200 mm behind the pin, with two 400 × 250 × 20 mm gussets. A 200 × 200 × 20 mm steel box stem runs to its actual ring face or yoke anchor. Each root has its own 400 × 300 × 30 mm mating plate, four M24 × 120 sets, four 80 × 80 × 12 mm nut backers and charged welds.

| Root | Anchor (X,R,T), m | Stem centre distance m | M24 selected grip mm | Pin axis |
| --- | --- | --- | --- | --- |
| AD-A | (+77.863261, +10.946997, -0.250000) | 0.158867 | 72.0 | (-0.060898, +0.340008, +0.938449) |
| AD-D | (+77.781732, +12.206171, -0.500000) | 0.234727 | 67.0 | (-0.060898, +0.340008, +0.938449) |
| BD-B | (+77.863261, +9.678969, -0.250000) | 0.291538 | 72.0 | (+0.001299, -0.128629, +0.991692) |
| BD-D | (+77.781732, +12.206171, +0.000000) | 0.238286 | 67.0 | (+0.001299, -0.128629, +0.991692) |
| DC-D | (+77.781732, +12.206171, +0.500000) | 0.211391 | 67.0 | (+0.004447, -0.028300, +0.999590) |
| DC-C | (+79.272341, +3.000000, +0.250000) | 0.279526 | 62.0 | (+0.004447, -0.028300, +0.999590) |
| BC-B | (+77.863261, +9.678969, +0.250000) | 0.274366 | 72.0 | (+0.024092, -0.073868, +0.996977) |
| BC-C | (+79.502341, +3.000000, -0.250000) | 0.241279 | 62.0 | (+0.024092, -0.073868, +0.996977) |

### Short AD cartridge

AD is an attempted one-piece steel cartridge with a priced, insufficient 220 mm diameter billet 943.759681 mm long. The 723.759681 mm pin spacing contains two 80 mm thick, 220 mm OD eyes with 102 mm bores; a 180 mm diameter neck has 403.759681 mm free length. Each 180 mm shoulder is 50 mm long, starting 110 mm from its pin. The full selected blank is charged, with no trim credit. This paid allowance cannot fabricate the represented eyes; it is not a complete machined cartridge or permission to add unpriced material. There is no overlapping carbon/insert scheme.

**Independent stock-containment FAIL:** in an eye's local `(e,n,p)` frame, the point `(0,0.108,0.030)` m is inside the selected 220 mm OD / 102 mm bore / 80 mm thick eye. Its eye-plane radius is 108 mm, outside the bore and inside the OD, and its thickness coordinate is 30 mm, inside ±40 mm. For the longitudinal billet, however, `n²+p² = 0.012564 m² > 0.110² = 0.012100 m²`. The saved record supplies this actual point at both eyes. Each lies outside the charged blank. The selected billet and eyes remain unchanged; no larger blank or added bridge is supplied. This failure is separate from the zero-area shoulder contact below.

**FAIL:** the 110 mm radius eye ends at the exact tangent where the shoulder starts. The represented eye chord and load-transfer area there are zero. No fillet, extra overlap or enlarged eye is silently supplied. The nominal neck-only compliance is 7.93337642652e-11 m/N using 200 GPa, but bearing/shoulder compliance and continuous installed stiffness are UNKNOWN. The neck axial stress below is conditional on a connection that this geometry does not provide.

### Collector and actual receiving interfaces

The existing D 400 × 400 × 25 mm and C 200 × 200 × 20 mm curved rings remain active once. The adjacent ring splices are represented at the half-sector angle with four 304 mm long covers of the respective ring width and wall thickness. No new infinitely rigid point replaces those walls or splices.

The collector's centres `S_D` and `S_C` are 600 mm axially inward and 200 mm radially inward of D and C. A 500 × 500 × 20 mm steel spine follows the actual S_D–S_C line. Two halves leave a 20 mm central gap. Four 750 × 500 × 20 mm face covers overlap each half by 365 mm. Each face has four M24 × 120 bolts per series side at longitudinal 100/250 mm and transverse ±150 mm: 16 bolts on each side, 32 total. The sides are in series; 32 is never the resisting area at one side.

Two 300 × 300 × 16 mm node arms start at the actual inward ring attachment faces: D at X−215 mm and C at X−115 mm from their ring centres. The C wrench and separate button enter S_C, traverse the spine to S_D, combine with D's wrench and go through one 500 × 500 × 20 mm arm to A. B retains its own main-member reactions. No equal A/B moment sharing or installed fixed restraint is inferred.

Each of four transfer legs has two independently recorded plate connections, four M24 × 120 per face, a selected 60 mm grip, 80 × 80 × 12 mm backers and perimeter weld stock. Full 500 × 500 × 20 mm end-plate stock is charged at eight faces, including trim for smaller arms. Four 300 × 200 × 12 mm access covers, each with four M12 and a 2 mm gasket, are charged per module; access openings, local cut weakening and a usable nut-installation sequence remain unqualified. The finite centre-line box layout and stock budget do not resolve miter joints or all plate/box intersections.

A and B each get a 1000 mm tangential × 300 mm radial × 30 mm axial yoke with two 1000 × 150 × 20 mm webs. The yoke plane lies 179 mm axially inward of the inherited frame datum. Existing 400 mm wide receiving cuff bodies and liners are active reuse; their old extra fittings remain contingency. Each new profiled pad is charged as full 1000 × 300 × 100 mm stock, with an active central 400 mm region profiled around the 328 mm cuff OD. Eight new M24 × 120 bolts and 80 × 80 × 12 mm backers per yoke use R=±60 mm and T=±150/±50 mm. The selected grip is 70 mm. Contact, pad fit under load, nut access, prying and old carbon/frame stiffness remain UNKNOWN, including any local packing needed to realize the declared grip.

| Datum | (X,R,T), m |
| --- | --- |
| S_D | (+76.966732, +12.006171, +0.000000) |
| S_C | (+78.787341, +2.800000, +0.000000) |
| Collector A end | (+77.863261, +10.946997, +0.000000) |
| Inherited A frame | (+78.042261, +10.946997, +0.000000) |
| Inherited B frame | (+78.042261, +9.678969, +0.000000) |

The actual collector spine length is 9.384466238 m. All force/couple transfers use these datums, including the actual ring-face, splice and receiver lever arms.

## Film root, all 17 posts and button

The pressure surface, finite bar hardware, incoming bar and separate new root bar stay in place. Their offsets are not removed to make a connection fit.

### Root normal-datum bridge

The old incoming interface is (+78.042261, +12.339180, +0.000000) m and the new interface is (+77.985197, +12.342139, +0.000000) m. The inward normal is (-0.951057, -0.309017, +0.000000). The actual displacement has a 53.356134621 mm normal step and -20.447715100 mm tangent step. Two 160 × 120 × 8 mm plates and two 100 mm wide × 12 mm thick webs span that displacement. Each web is 42.586263591 mm long between the plate faces, oriented along the actual inclined axis, with its centre at T=±35 mm. The old 16 mm flat plate's 37.356 mm unbridged step remains a fixed comparison.

There are four M8 × 50 bolts, four 30 × 30 × 4 mm backers and 400 mm of 4 mm weld at each end, with a selected 24 mm grip. Both series ends are priced and checked separately. The new bridge transmits the old incoming bar only, whose magnitude is 4.044489 kN and whose required delivered T couple is −84.205095 Nm. The new root bar remains distinct; the complete row retains both actual incident vectors. Installed clip, plate/web and receiving-hoop capacity remain UNKNOWN. Geometry closure of the bridge alone is not a clip qualification.

There are 18 adapters in every sector, at `(k−8.5)·2π/666`, k=0…17. All 1332 adapters across both caps are charged. Their solids are rotated to their actual column meridians; force and couple vectors must rotate together.

### Canted post stock and both feet

For each interior hoop, intersect its inward normal in X–R with the **changed** DC projection, then use the actual T coordinate of that DC point. The post runs between the actual hoop and beam datums along that canted 3D axis. The **infinite-cylinder intersections**, not established finite-cuff material contacts, lie at depths `66 mm / sqrt(1−(a·T)²)` at the hoop and `193 mm / sqrt(1−(a·e_DC)²)` at the beam. Each end then occupies 62 mm: 12 mm mating cuff pad, 12 mm base, 30 mm web height and 8 mm head. This fixes the unchanged selected carbon cut in the table; the finite source-domain and material-gap tests below show why those datums do not by themselves provide a joined foot. The preselected minimum is 80 mm and is never silently shortened.

The carbon post is 100 × 8 mm. Each end has an 83/69 × 100 mm steel socket with 90 mm bond, two 160 × 30 × 8 mm webs and a 120 × 120 × 8 mm head. There are four M12 × 70 bolts and four 30 × 30 × 6 mm backers per plate foot; the 30 mm grip comprises 12 mm base + 12 mm pad + 6 mm backer. Two 160 mm, 8 mm base welds belong to each foot. Separate head/insert welds are also charged. The 386/354 × 200 mm beam cuff has its own eight M12 and 600 mm of 8 mm fabrication weld; the 132/110 × 80 mm hoop cuff has its own four M8 and 160 mm of 4 mm weld. None of these distinct connections is pooled with the opposite end's resisting area.

| Row | DC station m | Carbon cut mm | Two-socket gap mm | Cuff interval within carbon? | Cut ≥80 mm? |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.228818 | 106.200729 | -93.799271 | FAIL | yes |
| 2 | 0.757358 | 156.480158 | -43.519842 | yes | yes |
| 3 | 1.284041 | 199.093340 | -0.906660 | yes | yes |
| 4 | 1.809062 | 237.077576 | 37.077576 | yes | yes |
| 5 | 2.332612 | 270.908908 | 70.908908 | yes | yes |
| 6 | 2.854882 | 300.370244 | 100.370244 | yes | yes |
| 7 | 3.376061 | 325.092056 | 125.092056 | yes | yes |
| 8 | 3.896335 | 344.714728 | 144.714728 | yes | yes |
| 9 | 4.415889 | 358.931008 | 158.931008 | yes | yes |
| 10 | 4.934909 | 367.489753 | 167.489753 | yes | yes |
| 11 | 5.453578 | 370.188283 | 170.188283 | yes | yes |
| 12 | 5.972079 | 366.862681 | 166.862681 | yes | yes |
| 13 | 6.490595 | 357.379012 | 157.379012 | yes | yes |
| 14 | 7.009310 | 341.626254 | 141.626254 | yes | yes |
| 15 | 7.528406 | 319.510954 | 119.510954 | yes | yes |
| 16 | 8.048067 | 290.953477 | 90.953477 | yes | yes |
| 17 | 8.568479 | 255.885714 | 55.885714 | FAIL | yes |

All 17 selected cuts exceed 80 mm. Rows 1–3 nevertheless fail the two 100 mm socket fit; rows 1 and 17 place some cuff footprint outside the actual DC carbon interval. These are 222 failed socket kits and 148 cuff-footprint locations across 74 modules. Socket, bond, post and cuff strength calculations remain conditional on the represented attachment geometry. No inherited short-post failure is silently relabelled as a complete repaired assembly.

### Finite hoop-cuff material, separate from sockets and beam footprint

The 132/110 × 80 mm hoop cuff occupies T=−40…+40 mm relative to its hoop centre. `sourceCuffSurfaceXRT` retains its historical field name but denotes the intersection with the **extended** 132 mm OD cylinder. It is not automatically a point on finite selected material. The complete 160 × 160 × 24 mm mating pad/base is checked using its actual centre and oriented axes: its T half-span is `Σ |axis_i·T| dimension_i/2`. A disjoint T interval proves no contact with any point of the finite cuff.

| Post row | Source T mm | Source in finite ±40 mm? | Complete pad/base T interval mm | Proven axial gap mm | Connection geometry |
| --- | --- | --- | --- | --- | --- |
| 1 | 121.444482 | FAIL: outside | [83.244504, 180.731625] | 43.244504 | FAIL |
| 2 | 92.564981 | FAIL: outside | [46.120853, 158.550472] | 6.120853 | FAIL |
| 3 | 75.168147 | FAIL: outside | [22.384641, 145.986374] | 0.000000 | FAIL |
| 4 | 63.575078 | FAIL: outside | [5.957978, 137.842233] | 0.000000 | FAIL |
| 5 | 55.326503 | FAIL: outside | [-5.981779, 132.052842] | 0.000000 | FAIL |
| 6 | 49.185270 | FAIL: outside | [-14.961259, 127.673000] | 0.000000 | FAIL |
| 7 | 44.462058 | FAIL: outside | [-21.886804, 124.220043] | 0.000000 | FAIL |
| 8 | 40.743423 | FAIL: outside | [-27.330230, 121.424137] | 0.000000 | FAIL |
| 9 | 37.767519 | inside | [-31.667795, 119.122831] | 0.000000 | UNKNOWN |
| 10 | 35.361833 | inside | [-35.154478, 117.212627] | 0.000000 | UNKNOWN |
| 11 | 33.409742 | inside | [-37.966308, 115.625135] | 0.000000 | UNKNOWN |
| 12 | 31.831652 | inside | [-40.225476, 114.314677] | 0.000000 | UNKNOWN |
| 13 | 30.574094 | inside | [-42.015483, 113.251674] | 0.000000 | UNKNOWN |
| 14 | 29.603559 | inside | [-43.390023, 112.419275] | 0.000000 | UNKNOWN |
| 15 | 28.903510 | inside | [-44.377448, 111.812090] | 0.000000 | UNKNOWN |
| 16 | 28.474041 | inside | [-44.981459, 111.436699] | 0.000000 | UNKNOWN |
| 17 | 28.334418 | inside | [-45.177529, 111.314175] | 0.000000 | UNKNOWN |

Rows 1–2 have strictly disjoint cuff/pad-base material intervals. Row 1's complete foot begins at 83.244504 mm, leaving 43.244504 mm beyond the cuff end; row 2's proven gap is 6.120853 mm. These are explicit attachment failures. Rows 1–8 also fail the claimed finite source-point domain. Rows 3–17 have overlapping axial bounds, which alone prove neither material contact nor a load-bearing joint; rows 9–17 therefore remain UNKNOWN at this interface. No cuff was lengthened, no foot moved and no unpriced bridge inserted. These checks do not replace the separate socket-overlap rows 1–3 or beam-carbon-footprint rows 1 and 17. All downstream force/couple records are conditional demands on the failed or unqualified route.

### Button support with its full source couple

The unchanged finite button force acts through the source datum (+79.881358, +2.999550, +0.000000) m. The new receiver is S_C, (+78.787341, +2.800000, +0.000000) m. A 300 × 300 × 16 mm steel box follows this actual 1.112067074 m axis. Its selected cut is 0.972067074 m, leaving 70 mm at each end. Each foot has a 400 × 400 × 20 mm plate, a full 400 × 400 × 20 mm profile-pad stock, eight M24 × 140 bolts on a 320 mm square perimeter, eight 80 × 80 × 20 mm backers and 1200 mm of 10 mm weld. The source grip is 20 plate +20 pad +12 shell +20 backer +8 mm paid packing =80 mm; the receiver's selected grip is also 80 mm. The finite button itself remains counted once in the prior hull.

**FAIL:** the plate centred on each datum plus its forward pad reaches 30 mm, but the box begins at 70 mm. There is a 40 mm unbridged gap at each end. No free joining stub is assumed; the stated weld and section demands cannot qualify this disconnected selection.

The force has zero net moment about the cap centre only when its full source couple is included. At the selected source that T couple is −93.334261 kNm. At the new S_C receiver it is -79.878006663 kNm after the actual lever transfer. Corrected I020's different receiver couple, −95.672290 kNm, and its 1980.940401 MPa support FAIL remain fixed comparison witnesses. Its previously rejected 87.610873 MPa force-only surrogate is not restored. The new box has conditional endpoint normal envelopes 62.192822/53.957977 MPa; the selected gaps prevent an installed pass, and the old button strip and dome failures are unchanged.

## Full vector demand accounting

All vectors refer to `O=(40,0,0)` m, the right-cap centre. For a force F with source moment M_O, its couple at any actual point P is `M_P=M_O−(P−O)×F`. Transferring to Q preserves `M_Q=M_P+(P−Q)×F`. Every post, adapter, button, collector leg and receiver uses that identity with all three components. Both required connection reactions are recorded; the receiver force/couple has the opposite sign of the applied wrench at the second series foot.

The saved film row vector and moment are retained. In each radial assignment, the circumferential reaction is subtracted at the actual row datum; it is not a load reduction without an assigned route. The 17 post loads reach the actual canted DC points together with their transported couples. If e is the actual DC unit axis, L its pin length, F_total the sum of those loads and M_D their complete moment about the D pin, the force component delivered at C is `(M_D×e)/L`. D gets the remaining force, and the unresolved axial torsion is `e(e·M_D)` at D. Thus `(P_C−P_D)×F_C + torsion_D = M_D`. The D clevis must transmit that perpendicular-to-pin bearing couple; its component along the free pin axis is checked to be zero. Its magnitude is still a connection demand, not a joint rating.

The two scalar X–R balance equations at C determine the new DC axial reference and BC tension using the actual 3D direction vectors' X–R components. The analogous equations at D determine AD and BD. The resulting T residuals and all node couples are explicitly assigned to the collector. This is one statically consistent **conditional load routing**, not a stiffness-derived 3D frame solution. It is not valid to treat the former 2D member forces as proof after moving the pins.

The C node record excludes the full button pressure force because that force enters physically at S_C. The C-node hoop reaction remains at C. The button wrench then joins the C collector input once. C → D → A carries the complete required wrench through the ring faces, box walls, central splice, receiver arm and A yoke. B's separately computed wrench reaches its own yoke/frame datum. Required opposite frame forces/couples are recorded; they are **not qualified installed reactions**. Full source/delivery algebraic closure does not resolve the inherited receiver or global stability failures.

| Quantity | f=0 | f=1 |
| --- | --- | --- |
| AD signed tension, MN | +2.463996568 | +2.072281127 |
| BD signed tension, MN | -6.321278769 | -6.523361296 |
| BC signed tension, MN | -4.212032015 | -4.428228368 |
| DC_reference signed tension, MN | +4.130280941 | +4.349675816 |
| DC maximum additive normal, MPa | 1127.587925 | 1186.677013 |
| DC maximum torsion shear, MPa | 171.117016 | 175.936096 |
| AD neck-only normal, MPa | 96.828947 | 81.435502 |
| Maximum pin force-only double shear, MPa | 402.425105 | 415.290078 |
| Maximum conditional fork bearing, MPa | 2258.506527 | 2389.380643 |
| Collector maximum normal envelope, MPa | 1717.765506 | 1804.906548 |
| Splice cover normal envelope, MPa | 514.986049 | 545.747977 |
| Splice moment-induced wall-force pair, MN | 6.339135 | 6.717794 |
| Splice torsional wall flow, kN/m | 122.951354 | 115.618553 |
| Splice force-only bolt mean, each side MPa | 44.050409 | 42.674310 |
| Force identity residual, N | 2.60312573e-10 | 2.39996334e-10 |
| Moment identity residual, Nm | 2.43750444e-08 | 4.53475043e-09 |

For a section the nominal normal envelope is `|N|/A + |M_b|/Z`; circular torsion uses `|T|r/J` and a square closed box uses `|T|/(2 A_m t)`. DC is sampled before and after every applied post wrench, plus both actual pins. The box normal envelope uses the bending-vector magnitude with one face section modulus; it is a scalar comparison, not a complete rectangular-corner biaxial interaction or a weld/local-buckling assessment. The collector and splice already exceed the nominal 355 MPa comparison. Fork bearing and pin demands are also unqualified and severe.

The changed BC's conditional pin-ended Euler load is 9.114513 MN against 4.212032/4.428228 MN compression; its nominal screen passes on this routing. The new DC normal envelope is below the 1450 MPa carbon proxy, but significant torsion and all connection/global interactions remain UNKNOWN. These changes coexist with the fixed I020 BC/DC failures, not a claim that the whole inherited structure has been repaired. AD's neck stress is below 355 MPa only in the disconnected neck idealization. Laminate, local buckling, pin/bearing restraint and installed stiffness remain unqualified for all members.

| Case / receiver | Force to frame (X,R,T), MN | Couple to frame (X,R,T), MNm | Yoke strip envelope MPa |
| --- | --- | --- | --- |
| f=0 / A | (-0.407671, +2.276114, +0.485875) | (+2.287833, +0.587943, -3.690303) | 89614.937935 |
| f=0 / B | (-1.238768, -2.276114, -0.485875) | (-2.903937, -0.587943, +0.957881) | 66617.841189 |
| f=1 / A | (-0.342861, +1.914267, +0.495072) | (+2.390164, +0.610683, -3.751520) | 93242.822226 |
| f=1 / B | (-1.303578, -2.271588, -0.495072) | (-3.017929, -0.610683, +0.952438) | 69133.519778 |

The yoke strip envelope is `6|M_yoke|/(0.300·0.030²)`, a deliberately simple demand comparison. Its enormous values already reject the nominal plate screen; they are not a finite-element stress field. Box arm/plate interactions, cuff contact, circumferential-ring deformation and the original frame's stiffness and moment-transfer capacity remain UNKNOWN. The inherited I020 unresolved module moments −181789.586575/−179927.499632 Nm remain in the comparison record. The new algebraic account shows where the demanded moments would go; it supplies no installed restraint that could erase those failures.

### Transfer-section sign convention

The button, posts and collector legs use an axis from source to receiver. For a cut enclosing the source-side applied wrench, equilibrium gives `F_internal = −F_source` and `M_internal = −M_source-at-cut`. Section axial force is `N = F_internal·axis`, tensile positive; `N<0` activates the compression comparison `−N ≤ π²EI/L²`. The external source forces, delivered receiver forces/couples, origins and separately recorded connection wrenches retain their physical signs. Main-member and DC beam-cut forces are derived separately and do not use this transfer conversion.

The button force is now **−92241.493297 N compression**, compared with a conditional pin-Euler value of 391226060.193234 N. Both endpoints still pass that nominal comparison after actually entering the compression branch. All 17 posts are also compression in both assignments. Absolute normal, bending and torsion envelopes are unchanged, as are the independent BC/DC screens and every physical source/delivery wrench. Internal signed torque changes with the same cut convention; no external couple is dropped. The following saved first-end axial force and full-length Euler values apply at both endpoints. Values of order 10⁻⁹ N in several collector legs are algebraic residuals near zero, not meaningful structural tension/compression predictions. All endpoint Euler flags remain nominal PASS; combined connection and global capacities remain UNKNOWN.

| Case f | Transfer | Internal axial N | Signed branch | Pin Euler N | Both endpoint nominal Euler |
| --- | --- | --- | --- | --- | --- |
| 0 | button | -92241.4933 | compression | 391226060 | PASS |
| 0 | post 1 | -56638.6653 | compression | 291181253 | PASS |
| 0 | post 2 | -66441.1705 | compression | 134121948 | PASS |
| 0 | post 3 | -72667.6699 | compression | 82852371.3 | PASS |
| 0 | post 4 | -76123.7424 | compression | 58430210.3 | PASS |
| 0 | post 5 | -77499.2513 | compression | 44747815.2 | PASS |
| 0 | post 6 | -77325.3817 | compression | 36400268.7 | PASS |
| 0 | post 7 | -75992.2057 | compression | 31074610.3 | PASS |
| 0 | post 8 | -73781.1463 | compression | 27637498.2 | PASS |
| 0 | post 9 | -70894.9437 | compression | 25491562 | PASS |
| 0 | post 10 | -67480.8042 | compression | 24318004.7 | PASS |
| 0 | post 11 | -63647.0544 | compression | 23964759.1 | PASS |
| 0 | post 12 | -59474.7762 | compression | 24401208.4 | PASS |
| 0 | post 13 | -55025.8568 | compression | 25713448 | PASS |
| 0 | post 14 | -50348.5749 | compression | 28139470.9 | PASS |
| 0 | post 15 | -45481.5221 | compression | 32169691.9 | PASS |
| 0 | post 16 | -40456.4271 | compression | 38794602.1 | PASS |
| 0 | post 17 | -35300.2994 | compression | 50156396.4 | PASS |
| 0 | C ring to spine | 87670.6183 | tension | 1.75793115e+09 | PASS |
| 0 | C spine to D | 1.69386387e-11 | tension | 33107498.4 | PASS |
| 0 | D ring to spine | 6.43995351e-10 | tension | 2.57046938e+09 | PASS |
| 0 | D spine to A yoke | 1.00987793e-09 | tension | 1.51417723e+09 | PASS |
| 1 | button | -92241.4933 | compression | 391226060 | PASS |
| 1 | post 1 | -62088.2817 | compression | 291181253 | PASS |
| 1 | post 2 | -72250.6151 | compression | 134121948 | PASS |
| 1 | post 3 | -78418.7036 | compression | 82852371.3 | PASS |
| 1 | post 4 | -81552.623 | compression | 58430210.3 | PASS |
| 1 | post 5 | -82455.3267 | compression | 44747815.2 | PASS |
| 1 | post 6 | -81735.2854 | compression | 36400268.7 | PASS |
| 1 | post 7 | -79833.4123 | compression | 31074610.3 | PASS |
| 1 | post 8 | -77063.7264 | compression | 27637498.2 | PASS |
| 1 | post 9 | -73649.3191 | compression | 25491562 | PASS |
| 1 | post 10 | -69749.5845 | compression | 24318004.7 | PASS |
| 1 | post 11 | -65479.5697 | compression | 23964759.1 | PASS |
| 1 | post 12 | -60923.3735 | compression | 24401208.4 | PASS |
| 1 | post 13 | -56143.3557 | compression | 25713448 | PASS |
| 1 | post 14 | -51186.4894 | compression | 28139470.9 | PASS |
| 1 | post 15 | -46088.7979 | compression | 32169691.9 | PASS |
| 1 | post 16 | -40878.5288 | compression | 38794602.1 | PASS |
| 1 | post 17 | -35578.5404 | compression | 50156396.4 | PASS |
| 1 | C ring to spine | 87670.6183 | tension | 1.75793115e+09 | PASS |
| 1 | C spine to D | 1.37221362e-09 | tension | 33107498.4 | PASS |
| 1 | D ring to spine | -8.92201892e-11 | compression | 2.57046938e+09 | PASS |
| 1 | D spine to A yoke | -1.38175181e-09 | compression | 1.51417723e+09 | PASS |

### Separate series-foot controls and fastener locations

Each plate-foot check divides its own load by its own bolt count and thread-root proxy area. Each weld mean uses only that foot's weld length and `0.707·leg` throat. The opposite series end is never parallel area. Four-M12 post feet, eight-M24 button feet, four-M8 adapter feet, the eight distinct root patterns, the four collector legs and each receiving yoke remain separate. The beam-cuff eight-M12 and hoop-cuff four-M8 sets do not contribute to the separate post-plate foot capacity.

For the explicit symmetric bolt pattern, the conditional equal-stiffness bilateral distribution uses axial force plus both plate-normal bending components and in-plane shear plus torsion. Negative axial terms are recorded; no tension-only/contact/prying model is invented. The saved bolt forces can be summed independently to recover all three force and three moment components at that foot. Maximum conditional tension and shear stresses use thread-root proxies 6.5/9.8/20 mm for M8/M12/M24. Head, shank, nut, washer and backer centres and finite dimensions are recorded relative to the selected grip. M8/M12/M24 backers are 4/6/12 mm, with 20 mm backers specifically at the button. The declared washer stacks and head/nut positions are not assumed away.

All known couples remain in each connection record. Additional weld moment stress, combined connection capacity, contact/preload, prying, slip, plate bending and material certification are UNKNOWN. A bolt-length allowance or a force-only mean cannot turn the selected disconnected or interfering assembly into a pass. Declared stack dimensions are necessary construction data, not proof that every curved surface and selected grip mates without packing.

| Post plate-foot maximum over rows and both ends | f=0 | f=1 |
| --- | --- | --- |
| Force-only bolt mean, MPa | 411.622821 | 430.957563 |
| Force-only weld mean, MPa | 68.618637 | 71.841791 |
| Conditional bolt tension, MPa | 2633.824676 | 3258.453826 |
| Conditional bolt shear, MPa | 423.649037 | 442.817835 |
| Known connection couple, kNm | 40.478670 | 42.127181 |

The force-only post means retain the corrected I020 values because the source force and independent foot area are unchanged. The new spatial offsets change the moments and conditional bolt distribution. Each new button plate foot has its own eight M24 bolts and 1200 mm, 10 mm weld footprint: force-only means are 37.016161 MPa for bolts and 10.965554 MPa for weld. The prior corrected button's separate 308.339535/51.401034 MPa bolt/weld means remain comparison values for its different hardware. The full button source and receiver couples, root adapter couple, post moments and collector/receiver moments are carried regardless of those nominal means.

## Finite fit, access and attempted assembly

The saved solids include actual pins, fork cheeks, washers/collars, eyes, inserts, carbon walls, root stems/plates, collector boxes/covers, rings/splices, yokes/profile pads, post cuffs/base blocks/sockets, all 18 actual adapter columns and the button box/plates/pads. Circular bores, tube interiors, square-box voids and the cuff pad's removed cylinder are excluded from material tests. Some web, head, bolt, weld, packing, access-cover and attachment details are dimensioned and priced separately rather than all entering the collision mesh. Consequently this is a finite witness set, not a complete manufacturing tolerance or erection certification.

A separating-axis test on 15 oriented-bound axes proves separation of represented bounds. When bounds overlap, deterministic interior points are tested against the actual material shapes of both parts. A point strictly inside both is a material-intersection FAIL. Lack of such a sample is UNKNOWN, not proof of clearance. Connected groups and intended ring-cover pairs are excluded; their joints must be assessed separately, which is why the AD zero-contact defect is explicitly retained. One representative sector and its neighbor are checked, with whole rings represented once. Periodic repetition and the opposite-cap transform are explicit; remote-sector collisions and all manufacturing/access paths are not certified.

The intended-cover exclusion is limited to the actual ring identity (`C` or `D`) and its declared splice-cover role. The next-sector cover belongs to that same continuous ring; other ring/body, cover/body and access comparisons remain. All 16 excluded pairs are enumerated below. The eight periodic copies newly excluded remove exactly one former material witness (`C curved box ring` / `C ring splice radial-1 [next sector]`) and seven former UNKNOWN bound overlaps. Compared pairs change 178594→178586, material witnesses 187→186 and UNKNOWN overlaps 422→415; 177985 proved separations, the other witnesses, all 92 pin comparisons and every insertion record remain unchanged. Excluding an intended connection is not a joint capacity pass.

| Continuous ring | Intended cover |
| --- | --- |
| D curved box ring | D ring splice axial-1 |
| D curved box ring | D ring splice axial1 |
| D curved box ring | D ring splice radial-1 |
| D curved box ring | D ring splice radial1 |
| D curved box ring | D ring splice axial-1 [next sector] |
| D curved box ring | D ring splice axial1 [next sector] |
| D curved box ring | D ring splice radial-1 [next sector] |
| D curved box ring | D ring splice radial1 [next sector] |
| C curved box ring | C ring splice axial-1 |
| C curved box ring | C ring splice axial1 |
| C curved box ring | C ring splice radial-1 |
| C curved box ring | C ring splice radial1 |
| C curved box ring | C ring splice axial-1 [next sector] |
| C curved box ring | C ring splice axial1 [next sector] |
| C curved box ring | C ring splice radial-1 [next sector] |
| C curved box ring | C ring splice radial1 [next sector] |

| Represented check | Result |
| --- | --- |
| Selected body count | 347 |
| Compared solid pairs | 178586 |
| Proved disjoint finite bounds | 177985 |
| Material intersection witnesses | 186 |
| Overlapping bounds still UNKNOWN | 415 |
| Finite pin-pair checks | 92 |
| Minimum pin envelope gap, mm | 187.121838145 |
| Post cuts below 80 mm | [] |
| Two-socket overlap rows | [1, 2, 3] |
| Cuff beyond carbon rows | [1, 17] |

All 92 represented finite pin pairs clear their conservative cylinder envelopes; this removes the selected pin-pair clashes only. An actual point (+77.720772, +11.291868, -0.175395) m remains inside both the AD A pin and the BD carbon wall. Further saved witnesses include AD/collector, fork/yoke, ring and button/collector conflicts. The full list and unresolved bound pairs are in `clearance` in `result.json`; no body was shrunk to improve that list.

| Pin insertion | 300 mm extra travel result | Proved obstructing material |
| --- | --- | --- |
| AD pin A | FAIL | BD carbon |
| AD pin D | FAIL | D curved box ring |
| BD pin B | FAIL | collector D half |
| BD pin D | UNKNOWN | none sampled; unresolved bounds remain |
| DC pin D | UNKNOWN | none sampled; unresolved bounds remain |
| DC pin C | UNKNOWN | none sampled; unresolved bounds remain |
| BC pin B | UNKNOWN | none sampled; unresolved bounds remain |
| BC pin C | UNKNOWN | none sampled; unresolved bounds remain |

The explicit assembly attempt is: preassemble split cuffs, profile pads, yokes and reachable backers; assemble the two collector halves and four-face splice while keeping access covers open; offer the fork roots and keyed DC end; insert each 220 mm pin along its actual local axis through 300 mm extra travel before fitting the final collars; attach posts, adapters and button feet; inspect nuts and close access covers. This sequence is blocked by the saved AD_A, AD_D and BD_B insertion witnesses. The other five insertion paths remain UNKNOWN. It is an evaluated unsuccessful sequence, not an erection instruction or permission to ignore the final occupied solids.

Four new erection kits per module are charged, 296 total, with 12 mm lugs, 24 mm holes, 20 × 80 mm pins, paired washers, 120 × 100 × 16 mm bases, four M12 and weld stock. **Each** carries the unchanged inherited 10528.099486 N nominal required demand; adding locations does not divide it. The carried lug net/bearing/pin/root/four-M12 mean screens are 15.666815/43.867081/33.511981/274.169257/34.893775 MPa. Collector attachment capacity and other wind cases remain UNKNOWN; the original non-replaced erection-flange FAIL remains.

## Complete selected-stock reconciliation

Every new row below is charged across both caps. Steel uses 7850 kg/m³, carbon 1600 kg/m³, adhesive 1200 kg/m³ and lining 1100 kg/m³. These are provisional inherited mass inputs. Cut waste and machining stock are retained where specified. The AD blank is charged against its attempted replacement duty but fails containment; its mass does not buy a fabricatable cartridge. No old AD insert is simultaneously installed. Changed main members, forks, stems, collector, yokes, pads, both ends of all feet, bolts, nuts, washers, backers, adhesive, welds, access closures and erection fittings are explicit rows. The inherited whole hull remains in the starting mass; this table is the new addition, not a second charge for active reused film or button.

No replacement qualifies for retirement. The old duties displaced by this attempted construction therefore become **inactive contingency**, not co-installed active solids. Their mass remains in the carried hull budget. Active reuse, inactive contingency and selected retirement partition every old I020 row below. The earlier polar contingency remains embedded in that hull and is not added again. This distinction avoids a mass credit while also avoiding a false claim that mutually exclusive old/new hardware can occupy the same space.

| Quantity | tonnes |
| --- | --- |
| Corrected I020 hull carried | 5313.920567045 |
| Qualified retirement | 0.000000000 |
| All new selected stock | 652.553319758 |
| New known hull | 5966.473886802 |
| Residual gas, once | 8.086383338 |
| Known subtotal | 5974.560270141 |
| Reused finite button already inside prior hull | 5.334396577 |

| Altitude m | Existing lift t | Prior known margin t | New known margin t | Change t |
| --- | --- | --- | --- | --- |
| 0 | 819.352791739 | -4502.654158644 | -5155.207478402 | -652.553319758 |
| 2500 | 640.002052834 | -4682.004897549 | -5334.558217307 | -652.553319758 |

The accounting identity is 5313.920567045 − 0 + 652.553319758 = 5966.473886802 t hull; adding gas once gives 5974.560270141 t. Displacement remains 668852.724569296 m³ with zero selected volume change. The margins above fail the stated reference-lift budget. Complete U+C, installed hull, physical float and loaded displacement remain UNKNOWN; no unknown support, equipment or stability duty is assigned zero mass.

### Changed hardware: selected material, charged stock and prior allocation

The previous I024 ledger incorrectly reused the old 83.411872091 kg main-end and 105.677526200 kg fork-root allocations despite changed selected parts. Those old per-kit amounts remain historical comparison only. The changed eye and cheek masses now come from the actual solid dimensions and 102 mm bores; the two retaining collars come from the selected 130/90 × 12 mm annuli.

For plate eyes/cheeks, the corrected ledger charges the **full rectangular selected blank**, including the actual removed bore as retained trim: `charged stock = selected net material + charged bore trim`. This deliberately makes the stock allowance larger than the corrected net part mass. The collars use the selected annular tube stock, with no extra solid-billet assumption or unselected machining allowance. Other kit component allocations and provisional densities remain individually identified and unchanged. No historical accepted row is rewritten and no corrected component is added twice.

| Changed component per kit | Parts / kit | Total parts | Old allocation kg | Selected net kg | Charged bore trim kg | Corrected charged stock kg |
| --- | --- | --- | --- | --- | --- | --- |
| centredEye | 1 | 444 | 36.515699534 | 43.224434595 | 5.131565405 | 48.356000000 |
| twoForkCheeks | 2 | 1184 | 27.386774650 | 27.237325946 | 3.848674054 | 31.086000000 |
| retainers | 2 | 1184 | 0.600000000 | 1.302127323 | 0.000000000 | 1.302127323 |

The eye uses `7850 × (0.350×0.220×0.080 − π×0.051²×0.080)` kg net. The pair of cheeks uses `2×7850 × (0.300×0.220×0.030 − π×0.051²×0.030)` kg net. The pair of collars uses `2×7850×π×(0.130²−0.090²)×0.012/4` kg. The eye net is 43.224434595 kg; the two collar net is 1.302127323 kg. These formulas describe the unchanged selected solids, not enlarged parts.

| Kit/component | Prior kg / kit | Corrected charged kg / kit | Treatment |
| --- | --- | --- | --- |
| mainEnd/insert | 26.368078292 | 26.368078292 | unchanged explicit allocation |
| mainEnd/bond | 0.169184189 | 0.169184189 | unchanged explicit allocation |
| mainEnd/endPlate | 19.729201865 | 19.729201865 | unchanged explicit allocation |
| mainEnd/centredEye | 36.515699534 | 48.356000000 | derived selected stock above |
| mainEnd/eyeWeld | 0.248688000 | 0.248688000 | unchanged explicit allocation |
| mainEnd/insertWeld | 0.381020211 | 0.381020211 | unchanged explicit allocation |
| mainRoot/twoForkCheeks | 27.386774650 | 31.086000000 | derived selected stock above |
| mainRoot/pin | 13.563826282 | 13.563826282 | unchanged explicit allocation |
| mainRoot/washers | 0.907148702 | 0.907148702 | unchanged explicit allocation |
| mainRoot/retainers | 0.600000000 | 1.302127323 | derived selected stock above |
| mainRoot/twoGussets | 31.400000000 | 31.400000000 | unchanged explicit allocation |
| mainRoot/basePlate | 28.260000000 | 28.260000000 | unchanged explicit allocation |
| mainRoot/fourM24 | 2.881536566 | 2.881536566 | unchanged explicit allocation |
| mainRoot/welds | 0.678240000 | 0.678240000 | unchanged explicit allocation |

| Kit | Count | Prior each kg | Corrected each kg | Prior total t | Corrected total t | Correction t |
| --- | --- | --- | --- | --- | --- | --- |
| mainEnd | 444 | 83.411872091 | 95.252172557 | 37.034871208 | 42.291964615 | 5.257093407 |
| mainRoot | 592 | 105.677526200 | 110.078878872 | 62.561095510 | 65.166696292 | 2.605600782 |

| I024 total | Historical uncorrected t | Corrected t |
| --- | --- | --- |
| New stock | 644.690625568 | 652.553319758 |
| Hull | 5958.611192613 | 5966.473886802 |
| Hull plus gas once | 5966.697575951 | 5974.560270141 |
| Margin at 0 m | -5147.344784213 | -5155.207478402 |
| Margin at 2500 m | -5326.695523118 | -5334.558217307 |

The total correction is 7.862694189 t. The old 644.690625568 t addition is not the corrected answer. This pressure-only calculation has no mass-derived gravity demand to update. Selected displacement, residual gas, the once-counted finite button, all predecessor rows and zero retirement remain unchanged. Neither corrected stock totals nor nominal screens qualify fabrication, physical float or complete U+C.

### All new stock rows

| Item | Count | Each kg | Added t | Dimensions and allocated duty |
| --- | --- | --- | --- | --- |
| AD one-piece machined cartridge billet | 74 | 281.621832033 | 20.840015570 | 220mm full round billet, pin spacing+220mm stock; intended180mm neck,80mm eyes,102mm bores; Priced blank only: FAIL to contain the selected transverse eyes; also zero-area eye/shoulder contact. All blank stock retained, no free added material or fabricated-cartridge claim. |
| main carbon BD | 74 | 47.887696314 | 3.543689527 | 350x20, actual displaced pin length minus500mm; Changed member cut; both caps |
| main carbon DC | 74 | 272.929429125 | 20.196777755 | 350x20, actual displaced pin length minus500mm; Changed member cut; both caps |
| main carbon BC | 74 | 196.901537923 | 14.570713806 | 350x20, actual displaced pin length minus500mm; Changed member cut; both caps |
| BD DC BC end assemblies | 444 | 95.252172557 | 42.291964615 | 309/285x300 inserts,290mm bond,400x20 plates;350x220x80 eyes with102mm bore; Six ends per module; selected eye full plate blank includes charged bore trim, other explicit kit allocations unchanged; no AD end overlap |
| eight spaced fork root kits | 592 | 110.078878872 | 65.166696292 | two300x220x30 cheeks with102mm bores,100x220 pin,two140/102x8 washers,two130/90x12 retainers,400x300x30 base,two400x250x20 gussets,fourM24 and welds; Eight separate roots per module; actual cheeks full plate blanks with charged bore trim and actual annular collars; other explicit allocations unchanged, no shared free pin |
| root stem AD-A | 74 | 17.958364956 | 1.328919007 | 200x200x20; full centre-to-centre stock incl end trim; Actual pin-base to ring/yoke anchor |
| root stem AD-D | 74 | 26.533572354 | 1.963484354 | 200x200x20; full centre-to-centre stock incl end trim; Actual pin-base to ring/yoke anchor |
| root stem BD-B | 74 | 32.955479482 | 2.438705482 | 200x200x20; full centre-to-centre stock incl end trim; Actual pin-base to ring/yoke anchor |
| root stem BD-D | 74 | 26.935895095 | 1.993256237 | 200x200x20; full centre-to-centre stock incl end trim; Actual pin-base to ring/yoke anchor |
| root stem DC-D | 74 | 23.895607030 | 1.768274920 | 200x200x20; full centre-to-centre stock incl end trim; Actual pin-base to ring/yoke anchor |
| root stem DC-C | 74 | 31.597659120 | 2.338226775 | 200x200x20; full centre-to-centre stock incl end trim; Actual pin-base to ring/yoke anchor |
| root stem BC-B | 74 | 31.014296568 | 2.295057946 | 200x200x20; full centre-to-centre stock incl end trim; Actual pin-base to ring/yoke anchor |
| root stem BC-C | 74 | 27.274134020 | 2.018285917 | 200x200x20; full centre-to-centre stock incl end trim; Actual pin-base to ring/yoke anchor |
| root mating plates and nut backers | 592 | 30.471465893 | 18.039107809 | 400x300x30 mating plate;four80x80x12 backers; M24 grip includes mating wall/pad; fork base already separately counted |
| root stem fabrication weld | 592 | 0.904320000 | 0.535357440 | two800mm 12mm perimeter seams; Each end of each stem |
| collector spine stock | 74 | 2828.853502742 | 209.335159203 | 500x500x20; two halves with20mm gap; Full pretrim length charged, gap waste not credited |
| collector A receiver arm | 74 | 418.297515233 | 30.954016127 | 500x500x20, actual centre distance; Whole collector wrench to A as an explicit unqualified routing |
| collector node arm D | 74 | 61.902276911 | 4.580768491 | 300x300x16, actual ring-face to spine datum; Finite wrench transfer at each node |
| collector node arm C | 74 | 74.853465370 | 5.539156437 | 300x300x16, actual ring-face to spine datum; Finite wrench transfer at each node |
| collector four-face splice covers | 296 | 58.875000000 | 17.427000000 | 750x500x20;365mm each-side overlap,20mm gap; Full stock incl bolt holes; four covers per module |
| collector splice M24 sets | 2368 | 0.720384141 | 1.705869647 | M24x120;16 bolts per series side,32 total; Two longitudinal stations100/250mm,transverse +/-150mm on each face |
| collector arm end plates | 592 | 39.250000000 | 23.236000000 | 500x500x20 full stock, including smaller-arm trim; Two ends of four represented connections |
| collector attachment M24 sets | 2368 | 0.720384141 | 1.705869647 | fourM24x120 per independent face;60mm selected grip; No opposite-end pooling |
| collector attachment nut backers | 2368 | 0.552866473 | 1.309187809 | 80x80x12; Install before closure; no free inaccessible nut |
| collector four-seam fabrication weld | 74 | 18.417039585 | 1.362860929 | four10mm longitudinal equivalent seams; Full new box length |
| collector attachment perimeter weld | 74 | 6.280000000 | 0.464720000 | eight2000mm 10mm perimeter weld allowances; Section end plates, stock incl trim; unqualified group moments |
| receiver yokes | 148 | 117.750000000 | 17.427000000 | 1000x300x30 plate,two1000x150x20 webs; Separate A/B finite overhang, old cuff body active once |
| receiver profiled pad full stock | 148 | 235.500000000 | 34.854000000 | 1000x300x100 steel billet; active central400mm bearing region machined to328OD cuff; All trim charged; grip/bearing/stiffness unqualified |
| receiver new M24 and backers | 148 | 10.186004917 | 1.507528728 | eightM24x120 plus80x80x12 backers per yoke; Old bolts/flanges kept as contingency; new explicit pattern +/-60R, fourT stations +/-150/50 |
| receiver welds | 148 | 1.570000000 | 0.232360000 | 4m of10mm weld per yoke; Web/plate fabrication; no qualified old carbon grip |
| profiled root datum adapters | 1332 | 3.213845206 | 4.280841814 | two160x120x8 plates,two100x12 webs at actual inclined length; Exact old/new normal and tangent datum displacement;no flat-plate gap credit |
| root adapter M8 and backers | 1332 | 0.489038595 | 0.651399409 | fourM8x50 per end,30x30x4 backers;24mm grip; Two series feet,8 bolts total |
| root adapter welds | 1332 | 0.050240000 | 0.066919680 | 400mm of4mm weld each end; Two sides of each100mm web at each plate |
| canted stanchion row 1 | 74 | 0.392893792 | 0.029074141 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 2 | 74 | 0.578904527 | 0.042838935 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 3 | 74 | 0.736553676 | 0.054504972 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 4 | 74 | 0.877077859 | 0.064903762 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 5 | 74 | 1.002238207 | 0.074165627 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 6 | 74 | 1.111231586 | 0.082231137 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 7 | 74 | 1.202690906 | 0.088999127 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 8 | 74 | 1.275285756 | 0.094371146 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 9 | 74 | 1.327879447 | 0.098263079 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 10 | 74 | 1.359542860 | 0.100606172 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 11 | 74 | 1.369526179 | 0.101344937 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 12 | 74 | 1.357222982 | 0.100434501 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 13 | 74 | 1.322137776 | 0.097838195 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 14 | 74 | 1.263859824 | 0.093525627 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 15 | 74 | 1.182043399 | 0.087471211 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 16 | 74 | 1.076393885 | 0.079653147 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| canted stanchion row 17 | 74 | 0.946659308 | 0.070052789 | 100x8 carbon, actual available cut or selected80mm minimum; No shortening to hide foot/socket space or insert overlap |
| new stanchion beam cuffs | 1258 | 35.539474502 | 44.708658923 | 386/354x200 cuff,354/350 liner,eightM12 and600mm8mm fabrication weld; Separate from the four-M12 plate feet |
| new stanchion hoop cuffs | 1258 | 3.206498685 | 4.033775346 | 132/110x80 cuff,110/108 liner,fourM8 and160mm4mm weld; At existing108OD splice datum; no pooled foot area |
| stanchion mating plates and socket shoes | 1258 | 12.660480000 | 15.926883840 | four160x160x12 plates,four160x30x8 webs,two120x120x8 heads; 62mm each-end occupied depth:12pad+12base+30web+8head |
| stanchion inserts and bonds | 1258 | 2.652314731 | 3.336611931 | two83/69x100 steel sockets;90mm bonds; Insert overlap explicitly checked against actual carbon cut |
| stanchion plate-foot M12 sets and backers | 1258 | 1.169032345 | 1.470642690 | fourM12x70 per foot,30mm grip,30x30x6 backers; Eight total per two-foot kit; each grip12base+12pad+6backer |
| stanchion shoe welds | 1258 | 0.223662475 | 0.281367394 | two160mm8mm base welds per end;two120mm4mm head welds and83mm circumference4mm insert weld per end; All interfaces separately charged; moment distribution remains unqualified |
| button support box | 74 | 138.696085444 | 10.263510323 | 300x300x16 steel, actual source-to-spine span minus140mm end stack; Full button source couple retained |
| button feet profile pads and backers | 74 | 116.556800000 | 8.625203200 | two400x400x20 feet,two full400x400x20 profile pads,16 backers80x80x20; Full pad/trim stock, existing finite button reused once |
| button source packing | 74 | 10.048000000 | 0.743552000 | 400x400x8 full steel packing stock; Source grip:20plate+20pad+12shell+20backer+8packing=80mm; no end-gap closure credit |
| button foot M24 sets | 74 | 12.662548290 | 0.937028573 | eightM24x140 per end,80mm selected grip; Separate series ends |
| button support seams and foot weld | 74 | 2.468145306 | 0.182642753 | 1200mm10mm perimeter weld each foot plus four longitudinal seams; Known moments do not create a welded-assembly rating |
| collector nut access closure kits | 296 | 6.223962936 | 1.842293029 | 300x200x12 cover,fourM12,2mm gasket;full removed wall stock retained; Four finite hatches per collector; access/section weakening unqualified |
| new collector erection kits | 296 | 2.944864442 | 0.871679875 | 12mm lug,24mm hole,20x80pin,120x100x16base,fourM12,welds; Four per collector,full inherited demand each; no dilution among more locations |

### Every prior I020 row

The 114 prior rows total 552.332455015 t: active reuse 330.803521542 t plus inactive contingency 221.528933473 t, with zero selected retirement. These are already included in the prior hull, not additional entries in the new stock total. Only the receiving cuff bands and liners remain active in their partly replaced kit; its old extra fittings stay in contingency.

| Prior item | Prior t | Active reuse t | Inactive contingency t | Retirement t |
| --- | --- | --- | --- | --- |
| main carbon AD | 0.439957833 | 0.000000000 | 0.439957833 | 0.000000000 |
| main carbon BD | 3.504050431 | 0.000000000 | 3.504050431 | 0.000000000 |
| main carbon DC | 20.338084294 | 0.000000000 | 20.338084294 | 0.000000000 |
| main carbon BC | 14.278062318 | 0.000000000 | 14.278062318 | 0.000000000 |
| main member end assemblies | 49.379828278 | 0.000000000 | 49.379828278 | 0.000000000 |
| centred double-fork node roots | 62.561095510 | 0.000000000 | 62.561095510 | 0.000000000 |
| receiving bridge cuffs | 11.485407808 | 7.408418344 | 4.076989464 | 0.000000000 |
| outer receiver stem | 2.091240000 | 0.000000000 | 2.091240000 | 0.000000000 |
| inner receiver stem | 3.764232000 | 0.000000000 | 3.764232000 | 0.000000000 |
| box ring D | 45.066243212 | 45.066243212 | 0.000000000 | 0.000000000 |
| four face splice covers D | 6.940377301 | 6.940377301 | 0.000000000 | 0.000000000 |
| ring splice bolts D | 0.852934823 | 0.852934823 | 0.000000000 | 0.000000000 |
| ring box fabrication weld D | 0.240353297 | 0.240353297 | 0.000000000 | 0.000000000 |
| root bolt access/nut backing plates D | 0.490945428 | 0.490945428 | 0.000000000 | 0.000000000 |
| box ring C | 4.228047763 | 4.228047763 | 0.000000000 | 0.000000000 |
| four face splice covers C | 2.726804241 | 2.726804241 | 0.000000000 | 0.000000000 |
| ring splice bolts C | 0.852934823 | 0.852934823 | 0.000000000 | 0.000000000 |
| ring box fabrication weld C | 0.058722886 | 0.058722886 | 0.000000000 | 0.000000000 |
| root bolt access/nut backing plates C | 0.327296952 | 0.327296952 | 0.000000000 | 0.000000000 |
| fine hoop row 1 | 0.545875508 | 0.545875508 | 0.000000000 | 0.000000000 |
| fine hoop row 2 | 0.522414079 | 0.522414079 | 0.000000000 | 0.000000000 |
| fine hoop row 3 | 0.498860289 | 0.498860289 | 0.000000000 | 0.000000000 |
| fine hoop row 4 | 0.475218293 | 0.475218293 | 0.000000000 | 0.000000000 |
| fine hoop row 5 | 0.451492261 | 0.451492261 | 0.000000000 | 0.000000000 |
| fine hoop row 6 | 0.427686381 | 0.427686381 | 0.000000000 | 0.000000000 |
| fine hoop row 7 | 0.403804852 | 0.403804852 | 0.000000000 | 0.000000000 |
| fine hoop row 8 | 0.379851887 | 0.379851887 | 0.000000000 | 0.000000000 |
| fine hoop row 9 | 0.355831713 | 0.355831713 | 0.000000000 | 0.000000000 |
| fine hoop row 10 | 0.331748566 | 0.331748566 | 0.000000000 | 0.000000000 |
| fine hoop row 11 | 0.307606697 | 0.307606697 | 0.000000000 | 0.000000000 |
| fine hoop row 12 | 0.283410365 | 0.283410365 | 0.000000000 | 0.000000000 |
| fine hoop row 13 | 0.259163837 | 0.259163837 | 0.000000000 | 0.000000000 |
| fine hoop row 14 | 0.234871393 | 0.234871393 | 0.000000000 | 0.000000000 |
| fine hoop row 15 | 0.210537318 | 0.210537318 | 0.000000000 | 0.000000000 |
| fine hoop row 16 | 0.186165905 | 0.186165905 | 0.000000000 | 0.000000000 |
| fine hoop row 17 | 0.161761453 | 0.161761453 | 0.000000000 | 0.000000000 |
| fine hoop splices | 3.114573725 | 3.114573725 | 0.000000000 | 0.000000000 |
| film bar span 0 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 1 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 2 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 3 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 4 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 5 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 6 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 7 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 8 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 9 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 10 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 11 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 12 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 13 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 14 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 15 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 16 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar span 17 | 0.115436857 | 0.115436857 | 0.000000000 | 0.000000000 |
| film bar steel end fittings | 41.109124970 | 41.109124970 | 0.000000000 | 0.000000000 |
| fixed bar-end bonds | 0.157274060 | 0.157274060 | 0.000000000 | 0.000000000 |
| poleward guide liners | 0.144167888 | 0.144167888 | 0.000000000 | 0.000000000 |
| shared film clips including terminal stock | 53.262647414 | 53.262647414 | 0.000000000 | 0.000000000 |
| root old-to-new datum adapters | 3.396546401 | 0.000000000 | 3.396546401 | 0.000000000 |
| film clip normal post row 0 | 0.183094663 | 0.183094663 | 0.000000000 | 0.000000000 |
| film clip normal post row 1 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 2 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 3 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 4 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 5 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 6 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 7 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 8 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 9 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 10 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 11 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 12 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 13 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 14 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 15 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 16 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 17 | 0.149410357 | 0.149410357 | 0.000000000 | 0.000000000 |
| film clip normal post row 18 | 0.312054873 | 0.312054873 | 0.000000000 | 0.000000000 |
| film post end hardware | 24.355805738 | 24.355805738 | 0.000000000 | 0.000000000 |
| fine hoop clip-foot cuffs | 72.607956225 | 72.607956225 | 0.000000000 | 0.000000000 |
| profiled fine-clip foot packing | 2.779725245 | 2.779725245 | 0.000000000 | 0.000000000 |
| normal hoop-to-DC stanchion row 1 | 0.021901274 | 0.000000000 | 0.021901274 | 0.000000000 |
| normal hoop-to-DC stanchion row 2 | 0.021901274 | 0.000000000 | 0.021901274 | 0.000000000 |
| normal hoop-to-DC stanchion row 3 | 0.021901274 | 0.000000000 | 0.021901274 | 0.000000000 |
| normal hoop-to-DC stanchion row 4 | 0.030257197 | 0.000000000 | 0.030257197 | 0.000000000 |
| normal hoop-to-DC stanchion row 5 | 0.038759371 | 0.000000000 | 0.038759371 | 0.000000000 |
| normal hoop-to-DC stanchion row 6 | 0.045344524 | 0.000000000 | 0.045344524 | 0.000000000 |
| normal hoop-to-DC stanchion row 7 | 0.050018480 | 0.000000000 | 0.050018480 | 0.000000000 |
| normal hoop-to-DC stanchion row 8 | 0.052785368 | 0.000000000 | 0.052785368 | 0.000000000 |
| normal hoop-to-DC stanchion row 9 | 0.053647631 | 0.000000000 | 0.053647631 | 0.000000000 |
| normal hoop-to-DC stanchion row 10 | 0.052606031 | 0.000000000 | 0.052606031 | 0.000000000 |
| normal hoop-to-DC stanchion row 11 | 0.049659647 | 0.000000000 | 0.049659647 | 0.000000000 |
| normal hoop-to-DC stanchion row 12 | 0.044805878 | 0.000000000 | 0.044805878 | 0.000000000 |
| normal hoop-to-DC stanchion row 13 | 0.038040437 | 0.000000000 | 0.038040437 | 0.000000000 |
| normal hoop-to-DC stanchion row 14 | 0.029357337 | 0.000000000 | 0.029357337 | 0.000000000 |
| normal hoop-to-DC stanchion row 15 | 0.021901274 | 0.000000000 | 0.021901274 | 0.000000000 |
| normal hoop-to-DC stanchion row 16 | 0.021901274 | 0.000000000 | 0.021901274 | 0.000000000 |
| normal hoop-to-DC stanchion row 17 | 0.021901274 | 0.000000000 | 0.021901274 | 0.000000000 |
| stanchion beam feet | 44.708658923 | 0.000000000 | 44.708658923 | 0.000000000 |
| stanchion hoop feet | 4.033775346 | 0.000000000 | 4.033775346 | 0.000000000 |
| stanchion end hardware | 7.376577211 | 0.000000000 | 7.376577211 | 0.000000000 |
| profiled pressure-film pads,full stock | 16.160059210 | 16.160059210 | 0.000000000 | 0.000000000 |
| new annular polymer film | 1.298414201 | 1.298414201 | 0.000000000 | 0.000000000 |
| root and button edge straps | 2.181988455 | 2.181988455 | 0.000000000 | 0.000000000 |
| edge strap backing plates | 1.454658970 | 1.454658970 | 0.000000000 | 0.000000000 |
| edge seal gaskets | 0.042466159 | 0.042466159 | 0.000000000 | 0.000000000 |
| edge bolts | 0.293015315 | 0.293015315 | 0.000000000 | 0.000000000 |
| edge and button weld allowances | 0.096977265 | 0.096977265 | 0.000000000 | 0.000000000 |
| button normal/offset support stock | 0.529229614 | 0.000000000 | 0.529229614 | 0.000000000 |
| button support feet and bolts | 0.433916307 | 0.000000000 | 0.433916307 | 0.000000000 |
| fine-hoop erection kits | 29.003023363 | 29.003023363 | 0.000000000 | 0.000000000 |
| box-ring erection kits | 1.743359750 | 1.743359750 | 0.000000000 | 0.000000000 |
| profiled erection cuff packing | 0.655914701 | 0.655914701 | 0.000000000 | 0.000000000 |

### Earlier embedded polar contingencies

| Earlier item | Prior t | Active reused t | Inactive contingency t | Retirement t |
| --- | --- | --- | --- | --- |
| polarClosure.twoDomePlatesT | 92.699123517 | 5.334396577 | 87.364726939 | 0.000000000 |
| polarClosure.twoHubBoxesT | 7.642303634 | 0.000000000 | 7.642303634 | 0.000000000 |
| polarClosure.goreAndButtonCoverStrapsT | 2.142018287 | 0.000000000 | 2.142018287 | 0.000000000 |
| polarClosure.allCoverWeldsT | 0.210650572 | 0.000000000 | 0.210650572 | 0.000000000 |
| polarClosure.twoRootFlangesT | 2.926396158 | 0.000000000 | 2.926396158 | 0.000000000 |
| polarClosure.rootFlangeWeldT | 0.078037231 | 0.000000000 | 0.078037231 | 0.000000000 |
| polarClosure.rootBoltsT | 0.138645228 | 0.000000000 | 0.138645228 | 0.000000000 |
| polarClosure.domeHubPostsT | 0.131396484 | 0.000000000 | 0.131396484 | 0.000000000 |
| polarClosure.domePostFeetT | 0.121207146 | 0.000000000 | 0.121207146 | 0.000000000 |
| polarClosure.domePostWeldsT | 0.010992890 | 0.000000000 | 0.010992890 | 0.000000000 |
| polarClosure.rootGasketsT | 0.068344709 | 0.000000000 | 0.068344709 | 0.000000000 |
| terminal meridian carbon | 13.247967816 | 0.000000000 | 13.247967816 | 0.000000000 |
| terminal meridian end fittings | 9.579800555 | 0.000000000 | 9.579800555 | 0.000000000 |
| old hub roots | 9.097983850 | 0.000000000 | 9.097983850 | 0.000000000 |
| old terminal film clips and splices | 0.200199805 | 0.000000000 | 0.200199805 | 0.000000000 |
| last-frame meridian saddles,remaining cap/barrel and attachments | UNKNOWN | UNKNOWN | UNKNOWN | 0.000000000 |

## Limits, unchanged failures and next construction

The selected arrangement clears the represented pin-pair envelopes and makes the root normal-datum bridge explicit. It still fails installed assembly, pin insertion, AD billet containment and continuity, finite hoop-cuff attachment, button-foot continuity, three socket fits, two beam-cuff footprints, collector/cover nominal stress and yoke nominal stress. All those failures remain even where an individual conditional normal/Euler/bolt-length comparison passes.

The unchanged film's 68.639 MPa versus 50 MPa provisional tensile comparison, the finite button strip's 22798.125 MPa nominal failure, dome/film crease and drape uncertainty, old barrel and mid-cap construction failures, receiving-frame and circumferential-ring limitations, local pin/fork/bond/weld unknowns and non-replaced erection failure are not resolved here. The corrected I020 support FAIL and original coplanar pin, short AD, post, cuff and flat-adapter witnesses stay in the frozen comparison rather than being erased. The finite button itself is neither resized nor requalified.

The weakest assumption is that a finite collector and its A yoke/cuff could transmit the complete vector moment into an already unqualified receiving frame. This unit exposes both the demand and failures; static bookkeeping supplies neither stiffness nor capacity. Global pressure resistance, stable loaded shape, cap-to-cap coupling, prestress, certified joints, fatigue/creep, combined wind/pressure cases, physical float and complete U+C remain UNKNOWN.

The one untested next construction is a receiver-integrated split polar cassette with an explicit insertion order and ring-wall isolation. Its actual frame attachment and continuous short-link geometry would need definition before any retirement could be selected. No such alternative is calculated, compared or credited here.

## Material context and reproduction

The source context is carried from corrected I020; no new material qualification or external measurement was obtained. [Toray T700S data](https://www.toraycma.com/wp-content/uploads/T700S-Data-Sheet.pdf) provides context for the inherited carbon proxies, not a manufactured tube laminate specification. The calculation retains 135 GPa and 1450 MPa as provisional carbon comparisons. [SSAB steel context](https://www.ssab.com/en/support/product-material-data/steel/20-questions) is the inherited basis for 200 GPa and 7850 kg/m³; [SSAB Domex 355MC](https://www.ssab.com/en-gb/brands-and-products/ssab-domex/product-offer/355mc) supplies context for a 355 MPa sheet comparison, not a pin, weld, cartridge or assembled-box rating. Adhesive, liner, film, contact and composite shear/interaction remain unqualified inputs as enumerated in `sources.json`.

The calculation uses standard-library scalar/vector arithmetic, a two-equation scalar elimination for each projected node balance and bounded finite-solid witnesses. It performs no matrix/eigenvalue solve, parameter sweep or ancestor calculation. Maximum matrix order is zero; there are exactly two fixed radial assignments and one selected geometry. Bounds declared before calculation are 30 CPU seconds, 60 wall seconds and 1 GiB address space per numerical or drawing check. This correction used one calculation generation, one drawing generation and one saved-image rendering, each attributed to the precommit source hashes. No corrected numerical replay or independent numerical control was run; static formulas and saved-output differences were inspected. The reproduction commands below are for a later reader, not evidence that this correction reran them at its final commit.

From the repository root, reproduce the saved result and drawing under those bounds:

```sh
python3 - <<'PY'
import resource
import subprocess

def limits():
    resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
    resource.setrlimit(resource.RLIMIT_AS, (1073741824, 1073741824))

for script in ["calc.py", "draw.py"]:
    subprocess.run(
        ["python3", "-B", "research/design-iterations/R3-I024/" + script, "--check"],
        check=True, timeout=60, preexec_fn=limits,
    )
PY
python3 tools/check_links.py
python3 tools/check_builder_line.py
```

`calc.py --write` regenerates `research/design-iterations/R3-I024/result.json`; `draw.py --write` regenerates `research/design-iterations/R3-I024/geometry.svg` from that saved result. The drawing does not run the engineering model. A successful reproduction means the declared numbers and geometry reproduce; it does not change the engineering FAIL/UNKNOWN disposition.

The scientific comparison remains the commit and tree above. The README hash below includes a later provenance-only text cleanup; all six non-README comparison files and the saved scientific result are unchanged.

The installed comparison file hashes are:

| Comparison file | SHA-256 |
| --- | --- |
| README.md | ba91d87d22f49362da14b16c186167a21ebf6eaba6d926a1f6ac915e42fff8f6 |
| baseline.json | 2975239c8321f9adfa8134b6476f6b3ce41fac3fa58ed9730daa3312ed1115e7 |
| calc.py | bae28bcd08d4344a157b16153682a8afb91c658bbccb178b684438ccd61ac419 |
| draw.py | 109d6e0b7aa2a71453f7e6c48d94904c2f70e603c5a23a22b4074ba4c918ffa3 |
| geometry.svg | dce892fd98dc32afe69b1522692c1f5e19cd33d4d66ab761521404c547a4e129 |
| result.json | c2eb01180ae2d991815ede5408d452a1e0fb05b930a53154a23120404bb0288a |
| sources.json | ed566668e6b2c3273f3f5268981fd5dfa8cbbca2c11f8fd4c820b91231ab3563 |
