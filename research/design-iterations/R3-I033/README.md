# R3-I033 — two triangulated side frames

**FAIL. The frozen construction increases the known hull mass by 367.629438 t.** Its finite representation has a negative root-arm cut, missing bolt material, intersecting tube walls and overlapping independent plates. Full member/foot/node demands, the individual A/B receiver reactions and complete cuff/frame capacity remain **UNKNOWN**. No installed structure, qualified retirement, loaded shape, global pressure resistance, all-up mission budget or physical float is established.

The hypothesis was that two triangulated steel side frames, transverse bracing and paid standoffs could replace the long split-cassette cheeks while preserving all pressure and gravity duties at the actual A/B receiving cuffs. This is a bending-capable closed frame, not an axial-only truss. The saved result rejects a mass reduction and records physical failures without tuning the issued geometry.

[Calculator](triangulation.py) · [saved result](triangulation.json) · [frozen saved inputs](baseline.json) · [source pins and inherited material proxies](sources.json) · [I029 predecessor and withdrawals](../R3-I029/README.md).

**Full mass and fixed-volume margins**

All table masses are tonnes. The vacuum-structural branch, unloaded D80 ×160 m / R40 pressure-surface datum and fixed668,852.724569 m³ displacement are unchanged. Gas is counted once. Unknown U+C, additional receiver reinforcement, equipment, payload and mission obligations are still deductions; no unknown item is set to zero.

| Quantity | Selected construction, t |
|---|---:|
| I029 known hull | 6,110.605077 |
| I029 cassette stock already included | 574.797288 |
| Explicit conditional I029 removal | 427.317246 |
| I029 stock retained | 147.480042 |
| Older I024 local stock retained | 221.887222 |
| New frame, connections and temporary bracing | 794.946684 |
| Known hull | 6,478.234515 |
| Residual gas, once | 8.086383 |
| Known hull + gas | 6,486.320898 |
| Change from I029 known hull | 367.629438 |
| Qualified retirement | 0.000000 |
| No new retirement: hull, separate bound | 6,905.551761 |
| No new retirement: hull + gas, separate bound | 6,913.638145 |
| Fully unretired I024/I029 local stock: hull + gas, separate bound | 7,344.304243 |

| Altitude | Fixed lift, t | I029 known margin, t | I033 known margin, t | Change, t | No new retirement margin, t |
|---:|---:|---:|---:|---:|---:|
| 0 m | 819.352792 | -5,299.338669 | -5,666.968107 | -367.629438 | -6,094.285353 |
| 2500 m | 640.002053 | -5,478.689408 | -5,846.318845 | -367.629438 | -6,273.636092 |

The matched bill is `I029 hull − explicit conditional removal + full new stock`. The older 5,313.920567 t hull and its active/inactive contingencies remain charged. The new 405 stock rows and retained rows form 471 local gravity sources, totalling 15,733.972270 kg per module. Their stock/bookkeeping centres are explicit; a declared centre is not a measured installed centre of gravity. Earlier hull gravity and global stability remain UNKNOWN.

The selected and no-new-retirement bills are alternatives, never added together. The latter restores every item conditionally removed in this unit. A further separately labelled historical bound also restores the430.666098 t conditionally removed in I029 from I024; it is not another additive charge to the selected bill. None grants qualified retirement.

**Frozen datums and dimensioned construction**

Coordinates are metres in right-handed X/R/T, `X × R = T`, with wrench origin O=(40,0,0). A/B are copied from `receivingFrameXRT`, not the shifted yoke or ring-node labels. Each proposed side node is `(S_X−0.60,S_R,±0.75)`; each S0 is `(S_X−0.60,S_R,0)`. These are paid proposed nodes, not assertions of clear space.

| Existing datum | X/R/T, m |
|---|---|
| A | (78.042261, 10.946997, 0.000000) |
| B | (78.042261, 9.678969, 0.000000) |
| C | (79.387341, 3.000000, 0.000000) |
| D | (77.566732, 12.206171, 0.000000) |

```text
X/R projection of EACH side plane T = -0.75 or +0.75 m
(schematic connectivity only; exact coordinates/lengths in tables and JSON)

           D± o
             / \
            /   \
       A± o-------o B±
            \   /
             \ /
           C± o

Edges on each side: D-A, D-B, C-A, C-B, A-B.
Four continuous T crossheads: S- ===== S0 ===== S+  (S=A,B,C,D).
Four transverse diagonals: D-→A+, D+→B-, C-→A+, C+→B-.
Crossings are occupied material unless a paid joint exists; none is added.

Typical A/B X/T projection (R fixed):
 T=+0.75    [500 mm side-node box]
                  |
             continuous200×200×12 crosshead
 T=0              S0 =====300×300×16===== actual cuff
                  |       centre-to-centre X=0.600 m
 T=-0.75    [500 mm side-node box]
            X=S_X-0.600                    X=S_X

Node: 500 mm external cube;20 mm wall;6 full500×500×20 blanks.
Generic independent foot:350×350×25 plate;8M24×180;
bolt VW offsets(mm): (±120,±120),(±120,0),(0,±120).
Fork source foot only:4M24×180 at(±60,±60) mm.
```

There are exactly31 tubes:18 RHS200×200×12 main members (ten side edges, four continuous crossheads, four diagonals), eight RHS200×200×12 root arms, D/C RHS200×200×12 source arms, one RHS300×300×16 button arm and two RHS300×300×16 receiving standoffs. Full centre-to-centre stock is paid even where finite cuts fail. Available cuts terminate at declared plates/node bodies. No unsupported extension, negative-length rescue, free crossing joint or trim credit is introduced.

| Member | Centre-to-centre m | Available cut m | Cut-length screen |
|---|---:|---:|---|
| `D---A-` | 1.345974 | 0.761507 | PASS LENGTH ONLY |
| `D---B-` | 2.571552 | 2.012778 | PASS LENGTH ONLY |
| `C---A-` | 8.060025 | 7.502914 | PASS LENGTH ONLY |
| `C---B-` | 6.813066 | 6.253027 | PASS LENGTH ONLY |
| `A---B-` | 1.268029 | 0.718029 | PASS LENGTH ONLY |
| `D+--A+` | 1.345974 | 0.761507 | PASS LENGTH ONLY |
| `D+--B+` | 2.571552 | 2.012778 | PASS LENGTH ONLY |
| `C+--A+` | 8.060025 | 7.502914 | PASS LENGTH ONLY |
| `C+--B+` | 6.813066 | 6.253027 | PASS LENGTH ONLY |
| `A+--B+` | 1.268029 | 0.718029 | PASS LENGTH ONLY |
| `crosshead-A` | 1.500000 | 0.950000 | PASS LENGTH ONLY |
| `crosshead-B` | 1.500000 | 0.950000 | PASS LENGTH ONLY |
| `crosshead-C` | 1.500000 | 0.950000 | PASS LENGTH ONLY |
| `crosshead-D` | 1.500000 | 0.950000 | PASS LENGTH ONLY |
| `diagonal-D---A+` | 2.015353 | 1.293568 | PASS LENGTH ONLY |
| `diagonal-D+--B-` | 2.977059 | 2.338056 | PASS LENGTH ONLY |
| `diagonal-C---A+` | 8.198415 | 7.632597 | PASS LENGTH ONLY |
| `diagonal-C+--B-` | 6.976236 | 6.403982 | PASS LENGTH ONLY |
| `root-AD-A` | 0.667165 | 0.093445 | PASS LENGTH ONLY |
| `root-AD-D` | 0.655061 | 0.132774 | PASS LENGTH ONLY |
| `root-BD-B` | 0.507407 | -0.009151 | FAIL |
| `root-BD-D` | 0.946646 | 0.328348 | PASS LENGTH ONLY |
| `root-DC-D` | 0.679982 | 0.124067 | PASS LENGTH ONLY |
| `root-DC-C` | 0.561060 | 0.013018 | PASS LENGTH ONLY |
| `root-BC-B` | 0.521825 | 0.013096 | PASS LENGTH ONLY |
| `root-BC-C` | 1.056889 | 0.477171 | PASS LENGTH ONLY |
| `boundary-D` | 0.600000 | 0.182000 | PASS LENGTH ONLY |
| `boundary-C` | 0.600000 | 0.282000 | PASS LENGTH ONLY |
| `button` | 1.094017 | 0.899017 | PASS LENGTH ONLY |
| `receiver-A` | 0.600000 | 0.160000 | PASS LENGTH ONLY |
| `receiver-B` | 0.600000 | 0.160000 | PASS LENGTH ONLY |

All eight root arms start at the exact retained forkBase datums. The mapping is AD-A→A−, AD-D→D−, BD-B→B−, BD-D→D+, DC-D→D+, DC-C→C+, BC-B→B+, BC-C→C−. Their original pins, finite forks, carbon/end assemblies and insertion sweeps stay represented in the frozen input with explicit active/inactive disposition. The continuous I029 AD plate remains charged. Already replaced I024 collector, yokes, root stems and old button support are neither reactivated as solids nor retired again.

Each side node pays six full500×500×20 wall blanks with mitred corners, a negative-X300×300×12 removable cover and four M12×80 sets. Each midpoint saddle pays two400×400×25 plates normal to the source/standoff X axis, two400×200×20 webs, four200×200×20 gussets and eight M24×180 sets with independent backers. Crossheads remain continuous through the saddle; no hinge or torsion-free joint is assumed. The issued blank sizes do not determine saddle web/gusset positions, bolt layout or cover aperture: those details are explicitly UNKNOWN, with all stock retained.

Every generic tube end has its own350×350×25 full plate and eight M24×180 complete sets. The eight fork-source ends instead retain the four-hole±60 mm pattern and pay four NEW M24×180 sets; the old pooled fork kits, including their old fasteners, stay charged. Each new M24 set includes a24 mm shank,36 mm AF×20 mm head,36 mm AF×32 mm nut, two48/26×4 mm washers and one80×80×12 backer;20 mm thread root is only a nominal demand proxy. The frame basis is `e=toward the other endpoint`, `v=unit(T×e)`, `w=e×v`; only a T-parallel e uses X as seed. Independent series feet never pool bolt area.

D/C retain their complete finite boundary contact plates, liners, ties and backers, with a new350×350×20 adaptor at each source. The button retains its separate force AND couple, contact/packing duties, and a new350×350×20 adaptor. Mating-hole registration, curved contact, through-grip, nut/tool access and blind anchors are not inferred from a point or blank. Each foot records its own material rays, plate/body geometry and unresolved F/M and bolt demands.

A/B retain the old split half blanks, liners, reinforcement and actual receiving cuffs. Exactly four M30×520 sets per receiver are replaced by four M30×700 sets, preserving the same explicit head/nut/two-washer stock and the old backers. Each receiver adds two600×400×25 doublers on±X and four250×250×20 full gusset blanks. The lower stack is554 mm and washer/nut/thread projection46 mm, leaving100 mm length allowance for the700 mm ties. This is a length-only comparison; installed grip, access, curved contact, gusset placement, ring/cuff capacity and any additional reinforcement C remain UNKNOWN.

All tube ends pay a separate12 mm equal-leg fillet around the full tube perimeter. The bill enumerates twelve500 mm node seams per cube, each saddle plate/web/gusset blank perimeter and each receiver doubler/gusset perimeter. Unspecified weld placements are charged finite stock allowances, not assumed installed strength. Prying, preload, contact, distortion and certified weld/bolt capacity remain UNKNOWN. The existing15 kg tool and12 kg erection allocations per module remain once, with an additional10 kg temporary bracing allowance; erection and unloading capacity are not established.

**Finite failures and assembly limits**

| Screen in this saved run | Result | Meaning |
|---|---:|---|
| Negative available tube cuts | 1 | `root-BD-B`: −0.009151 m; the issued body/feet do not leave positive tube length |
| Noncoplanar foot-to-substrate interfaces | 41 | A plate normal along the member does not create a full mate on an oblique cube/fork face; no wedge is added |
| Bolt centre rays missing paid substrate | 16 | Finite fork-source misses; no invented blind anchor or edge clamp |
| Tube-wall pair intersections | 28 | Positive overlap of finite solid RHS wall prisms, with no shared-node exclusion |
| Independent end-plate intersections | 44 | No relocation, trim or shared plate-area credit |
| Cover/end-plate intersections found | 0 | Only this narrow pair screen; aperture, screws, tools and full access remain UNKNOWN |
| Retained-material interior witnesses | 29 | Finite points inside new tube/plate material and saved active source material |
| AD-A pin / BD carbon | Inherited FAIL | Unchanged obstruction; no newly issued fit or access qualification |
| All other swept, neighboring-sector, tool and full-body clearance | UNKNOWN | Absence of a sampled witness is not clearance |

Both issued pairs of transverse diagonals physically cross. The saved solid-wall SAT overlap witnesses are0.006497158440 m for D−→A+ versus D+→B−, and0.088634490337 m for C−→A+ versus C+→B−. These are separating-axis overlap values, not unique physical penetration depths. No free joint is placed at either crossing. A saved root AD-D wall witness at(77.37765971086831,12.043481070366015,−0.7294847209856961) m lies inside the unchanged curved D-ring wall.

The declared assembly sequence is unload and independently support the old interface; fit the retained open A/B clamps; offer the paid side-node boxes and source feet; install the side members, crossheads, transverse braces and saddles; retain the finite forks/AD plate/carbon ends; insert each original pin along its recorded axis/travel; connect the D/C/button adaptors and receiver standoffs; inspect independent nuts, tools and contact before closure. This sequence fails at the recorded cuts, occupied crossings, fork material and retained AD-A obstruction. Unpriced extra erection support and unproved accesses remain UNKNOWN. No installability conclusion follows from the schematic.

**Pressure, gravity and full force/moment duties**

Pressure remains121,590 Pa with37 sectors per cap,18 film bays and666 film columns. New polar axial load is58.362305820542 MN per cap ONCE; the old incoming boundary(−2.555920809530 MN axial,−0.850241688208 MN radial) remains separate. The unrelated whole-end611 MN is not reapplied. The finite button source remains at(79.88135824915571,2.9995499999999953,0) m with force(−92915.57450675245,−4648.052577960895,0) N and couple(0,0,−93334.26148915867) Nm.

The only load assignments are saved f=0 and f=1. Full pin-source and D/C wall-source wrenches are transported to both actual source-arm feet using `M_Q=M_P+(P−Q)×F`. D/C boundary remainders and the separate button are neither omitted nor counted twice. This is bookkeeping, not a compatible frame solution.

| Assignment | Total source force X/R/T, N | Source moment about O, Nm | Force residual, N | Moment residual, Nm |
|---|---|---|---:|---:|
| f0 | (-1,646,438.557569, 0.000000, 0.000000) | (-0.000000, 0.000000, 13,720,343.196465) | 0.000000e+00 | 4.083524e-08 |
| f1 | (-1,646,438.557569, -357,320.807075, 0.000000) | (-0.000000, 0.000000, -21,788.731405) | 2.910383e-10 | 2.012723e-09 |

There are exactly74 keyed states, `f0-s00…f0-s36` and `f1-s00…f1-s36`. Each uses `g_local=(0,−g cosθ,+g sinθ)`, g=9.80665 m/s². All471 declared selected-local-stock gravity sources act once at their saved centres. Each state records aggregate F and M about O, the required opposite receiver-pair wrench, the separate source-arm pressure-plus-tube-stock subset, and references the complete31-member/62-foot/12-node unresolved demand sets. The subset is never substituted for the full member load: connection weight and other retained/new local weight remain in the aggregate and full unresolved duties.

At f0-s00 the full known local applied force is(−1646438.5575694966,−154297.5591571655,0) N and moment about O is(51.17048206400253,1.0244548320770264e−8,7858634.947991187) Nm. The required receiver-pair reaction is their opposite. The individual A/B reactions remain UNKNOWN. Six equilibrium equations cannot determine the twelve A/B reaction force/couple components, let alone the closed-frame stiffness and contact distribution:

```text
RA + RB = -F_external
(A-O)×RA + MA + (B-O)×RB + MB = -M_external
```

No equal split, zero end couple, ideal pin truss or free torsional restraint is introduced. Every full member, node, foot and receiver F/M record is present directly or by the state’s named demand-set reference; UNKNOWN values are null, not zero. Bolt reaction means the force of substrate on the isolated end plate, with its negative on the substrate. No source-applied force is called bolt tension. A future square-section corner calculation would require `|N|/A+|Mv|/Zv+|Mw|/Zw`, not the old transverse vector norm divided by one face modulus. Full member stress/buckling, bolt tension/shear/bearing/prying, weld interaction and installed capacity remain UNKNOWN here.

The opposite cap reflects X through the vehicle midplane before the R/T sector rotation. Position and force use Q=diag(−1,1,1); couples use det(Q)Q=diag(1,−1,−1), and the moment origin is reflected too. Each saved state includes its opposite-cap wrench mapping. The physical bill is37 sectors×2 caps; the two radial assignments do not double that count or add another pressure load. This symmetry bookkeeping does not prove loaded shape or global equilibrium.

**Retirement, qualifications and one next hypothesis**

Every I029 stock row has an old/removed/retained match in `stock.matchedI029Rows`; the earlier I024 match is retained in the input and referenced explicitly. Conditional removal covers only the long cheeks, cross spacers, eight old root arms and their added foot stock, old cheek-to-receiver bridges, D/C bridges, button arm and the replaced M30 ties. The full old fork kit, continuous AD plate, carbon/end assemblies, A/B/D/C contact stock, root adapters/stanchions and older hull/contingencies remain. Pooled button feet/pads/backers/sets, old access stock and the unsplit old weld row stay charged. No pooled row is quietly retired or treated as proven reusable geometry.

The weakest assumption is that the two actual A/B cuffs and their surrounding frame can accept the complete three-dimensional reaction pair without dominant additional reinforcement, peel, rotation or contact conflict. That assumption is UNKNOWN. Structural and stiffness sensitivity are UNKNOWN; only the bookkeeping statement that each additional tonne reduces each fixed-lift margin by one tonne is established. No parameter sweep, revised fit or favorable load distribution was tried.

**Exactly one future untested hypothesis:** a separately paid wider frame saddle replacing cuff load introduction at the same named frame region, with its own future construction freeze. It is not another geometry or execution in this unit.

Inherited failures remain: film68.639 MPa versus50 MPa proxy; finite button strip22,798.125 MPa; AD-A pin/BD-carbon interference; post socket rows1–3, finite cuff rows1–8 and carbon cuff footprint rows1/17; barrel/mid-cap and non-replaced erection failures. Complete pressure resistance, loaded shape, earlier-hull gravity/stability, all-up U+C/equipment/payload/mission and physical float remain UNKNOWN.

I029’s original technical review completed but was ineligible under its effort policy (requested max, actual xhigh); its three MEDIUM findings remain open. F1 was the AD-D second-foot bolts missing the old cheek; F2 the source-foot force/reaction sign and zero-tension misclassification; F3 the nonbounding square-section normalEnvelopePa comparison. The later I029 README-only withdrawal is explicitly UNREVIEWED and did not repair mechanics or close findings. This unit imports source loads and paid stock, not those withdrawn capacity claims. Earlier review caps, failed launches, control gaps, governance timeouts/fallbacks and packaging limitations remain historical.

**Execution and custody scope**

This new calculation ran once from the dirty integration worktree on the exact landing76 base, before any governed commit. The Python3.14.4 payload passed the actual pre-execution guard: its IPC namespace differed from the host, it ran in the task’s p2 cgroup on CPU29 with cpu.max100000/100000,1 GiB memory/address-space caps, swap0, TasksMax16,60-second CPU and120-second wall limits, scientific NPROC1, core0,256 MiB file-size cap,64 descriptors and one-thread environment values. Source, input, manifest, launcher and guard byte hashes were checked before calculator exec. This demonstrates this invocation’s controls; it does not repair historical gaps.

The observed launcher elapsed time was0.707608 s. GNU time inside the task measured0.65 user+0.01 system CPU seconds,0.67 s elapsed and26,760 KiB maximum RSS for the namespace wrapper/guarded task and waited descendants. Those are observations, not configured limits or the client wait4 measurements. Terminal collection recorded the task inactive/dead, MainPID0 and absent cgroup. No independent post-exec thread trace was sampled; the record does not claim one. No drawing, renderer, optimizer, stiffness solver, external scientific lookup, ancestor execution or extra numerical probe was used.

The public package is limited to these five files and the exact baseline/result declarations in[the derived-path manifest](../../../.helm/derived-paths). The baseline producer is inert saved-field input assembly; the result producer is triangulation.py. The existing manifest prefix, including I029 declarations, is preserved. Source pins name the actual landed I029 postimages on base `bef6780cc2a7e6a245cc975a4139d14edf283712`, tree `409e905138c90892585d669cc6334c6a8b025845`. The Captain landing receipt attributes unchanged signed postimages, gate/HONOURED and publication to landing76; this calculation does not independently re-establish those acts. Governance, Builder checks and any later technical review are separate evidence, not scientific certification.

Steel density7850 kg/m³, modulus200 GPa and nominal355 MPa are inherited screening proxies documented in[sources.json](sources.json), not certified RHS, bolt, weld, machined plate, cuff, adhesive or composite properties. No new external source was fetched. The saved compact JSON stores immutable geometry/material/connections once and references them from the74 states; unresolved duties are retained without duplicating giant geometry records.
