# Status against today’s model

**Disposition: LAND — the embedded solver reproduces against the current inputs.**
Its full executable appendix was extracted and run against this checkout, with one BLAS
thread; exit 0. The pinned / pinned-fixed / fixed checks give **1.000000 / 0.699156 /
0.500000**. The minimum catalogue plateau remains **1,210–2,150 N·m/rad**, the tube-density
saving remains **1.223680 kg/m³**, and all **149 main + 202 rim** lighter candidates remain
rejected; the additional **18** beyond-cap sections fail the local-wall screen.
The same-geometry PAHT / Al / Ti totals remain **15.081526 / 21.175735 / 27.837728 kg/m³**
on the report's own nominal 0.709 m volume and physical-cut convention.

Two surrounding comparisons have moved. The purchasing model now bills **1.948 kg** of tube
and **2.691 kg** total, replacing 2.390 / 3.133 kg; it no longer bills centre spans.
The solver's separate **1.944230 kg** physical-cut object is still a different convention,
not another saving to subtract. The current loaded-skin record also has a different
loaded volume from this report's old 0.162927 m³ example: use the generated ledger's
loaded-shape row for current buoyancy. The stored assembly certificate is now 12/16;
it was read, not rerun. None of these changes supplies physical joint stiffness or a
qualified combined-load criterion. The “dead end” verdict below is bounded to its finite
invented catalogue, not a theorem about every joint or hull.

**Reproduction:** extract the `python` fenced appendix to a scratch file, then run
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 "$TMPDIR/end_fixity_second.py" .`.
The script reads the model and geometry and prints JSON; it does not edit them.

## Dated audit record

The text below records what was claimed on its audit date. “Today” in that text means that date. Only the reproductions above are current; historical numbers and review-era paths are preserved as evidence, not revalidated claims. See [the float ledger](../FLOAT-LEDGER.md).

---

# What is end fixity worth?

**Finding, 2026-08-12.** Abstract hub-centre end restraint is worth at most **1.224 kg/m3 of
tube** on the standalone 0.709 m article in this directional catalogue. Its tube-only optimum is
the broad catalogue plateau **1,210--2,150 N m/rad** (integer-resolved and checked against every
lighter catalogue section), not the infinitely rigid joint.
The reason is film bending. Tube mass falls from 4.722 kg/m3 pinned to 3.498 kg/m3 on that
plateau, then rises to 3.664 kg/m3 as support moment approaches the clamped value.

That does **not** make stiff joints a route to floating. On exact current geometry the PAHT-CF,
aluminium, and titanium substitutions are respectively **15.08, 21.18, and 27.84 kg/m3**
including current tube and film. The denser metals pass the tube-only stiffness knee but cannot
claim its savings without regenerating and qualifying a smaller socket.
More importantly, none is licensed. The repository has no bondline stiffness, no global frame
eigenmode, and no validated tube ovalization criterion. The frozen P13 screen says all 216
moment-loaded ends fail, but its 72 rim rows are contaminated by the known global-10x8 probe
defect; the other 144 spoke/tie failures remain direct evidence, while the rim census is
unproved rather than a number to quote as physical capacity. The physical `K` and physical
optimum are therefore **NOT COMPUTABLE**. Crediting the published `K=0.65` socket bonus is
**UNSAFE**.

This is a read-only audit of the model. No model, generator, JSON artifact, baseline, tolerance,
or margin definition changed.

## Objects and mass ledgers

The primary object is standalone article A: nominal 0.709 m square-face span, `n=1`, nominal
Kelvin volume

`V = 0.709^3/2 = 0.1782004145 m3`,

51 generated joints, and 216 generated members. Every density in the article-A tables divides
by that same nominal volume. Axial demands remain the model's periodic-array demands; physical
tube mass uses the standalone article's 216 cuts. This intentional conservative mismatch is
stated rather than hidden.

The generated loaded-shape volume is a different denominator, `0.162927 m3`. Using it would
multiply every article-A density in this report by
`0.1782004145/0.162927 = 1.093744`, a **9.374% density debit** (for example the current PAHT
same-geometry total becomes 16.50 rather than 15.08 kg/m3). The nominal-volume comparisons are
therefore optimistic for the loaded physical object; the denominator is held fixed here only
to isolate the restraint trade.

Two current-article mass objects coexist and must not be mixed:

- **Published purchasing object:** 2.390 kg tube + corrected 0.715 kg joint set + 0.028 kg film
  = 3.133 kg, about 17.6 kg/m3 on the model's unrounded volume. This is the corrected article
  figure requested by the work order. Every older table using 0.465 kg of joints is stale by
  `0.715/0.465 = 1.537634`, or **1.54**.
- **Generated physical-cut object used in this sweep:** deduplicating all 216 members, using
  `cutMm` for 50 tree members and `closingCutMm` for 166 closing members, gives 39.737812 m and
  `m = sum(rho A_i L_i) = 1.944230 kg` of the current 10x8/14x12 tube, or 10.9104 kg/m3.
  Adding 0.715 kg joints and 0.028 kg film gives 15.08 kg/m3. P14 explains the difference:
  `stockBuild` bills 48.8 m of centre lengths as cuts. The sweep does not freeze that known
  overbill as a worse baseline.

R1 is a different object: the reviewed `n=2`/`n=4` finite articles have 948/6,840 physical cuts
and no generated even-`n` joint geometry. Commit `0f0899a...` prices their pinned, film-sized
totals at 10.76--12.51 kg/m3. This audit does not attach article A's 51-joint mass or stiffness
to those 201/1,289-joint objects.

## Reproduction gates

The gates ran before the calculation:

1. `python3 tools/scale_study.py` exited 0 after fourteen `ok` rows and printed verbatim:
   `=> reproduces the published article`.
2. `python3 tools/subdivision_study.py` exited 0 after six `ok` rows and printed verbatim:
   `=> consistent with the model`.
3. `make check` exited 2. Contrary to the work order's stale expected `stampcheck` stop, boundary
   and both stamp checks passed; `figfresh` then failed with
   `FileNotFoundError: [Errno 2] No such file or directory: 'chromium'`.
4. Separate `make assemblycheck` exited 0 and printed verbatim:
   `check_assembly: NOT PROVEN — 5 of 16 proofs fail (5 frozen in KNOWN, 0 new), 11 pass, 7 advisories.`
   It also repeated: `216 of the 216 moment-loaded ends cannot license the clamped row` and
   `2064 of 3888 margins fail`. Those are the raw frozen-screen counts: the prior physics audit
   establishes that its global-SKU probe corrupts all 72 rim rows, so only the 144 non-rim
   moment-row failures can be used directly and the rim result remains unproved. Exit 0 means
   the frozen bill did not move, not that the joint passes. Its path/timing-only JSON rewrite
   was restored immediately.

No self-check failed, and no tolerance was adjusted.

## Finding 1 — the model uses pinned K; its socket bonus is unlicensed

`tools/scale_study.py:61-62` declares `euler(..., k=1.0)`. Calls at lines 79, 82, 85, and 88
omit `k`, so octet, rim, spoke, and governing short-tie primary margins all use the unstated
default `K=1.0`. `tools/subdivision_study.py` likewise writes `pi^2 E I/L^2` directly. That
unstated provenance is the S-class finding.

`cell/model.js:584-585` separately computes an octet-only display value
`pcrSocketed = pcrPinned/0.65^2`; lines 627-633 keep the primary family margins pinned. No code
derives 0.65 from the joint. If a downstream decision credits it, capacity is multiplied by
`1/0.65^2 = 2.3669` without a licensed restraint path.

| model member family | centre length; physical cut used for mass | factored axial demand | Euler formula/source and status | other K |
|---|---:|---:|---|---:|
| octet 10x8 | 245.354--250.669; 210.883--221.500 mm | 3.376 kN | `pi^2 EI/(K L)^2`; `scale_study.euler` omitted default, primary `K=1` | 0.65 display only |
| spoke 10x8 | 243.023; 205.742 mm | 2.238 kN | same; primary `K=1` | none |
| rim 14x12 | 242.465--243.564; 202.078--203.177 mm | 4.477 kN | same; primary `K=1` | none |
| tripod tie 10x8 | 172.974; 138.525--139.025 mm | 4.775 kN | same; primary `K=1` | none |
| inward tie 10x8 | 166.525; 129.270--129.770 mm | 4.775 kN | same; primary `K=1` | none |
| in-plane square tie 10x8 | 171.479; 133.876--134.376 mm | 5.038 kN | same; primary `K=1` | none |

The first length in each row is the generated hub-centre Euler object; the second is the real
tree/closing cut ledger used only for mass. Even `K=1` is conditional on no sway; the absent
global eigenmode means it is not a system-stability proof.

## Finding 2 — today's licensed K is NOT COMPUTABLE

The current generated socket has two parallel moment paths: the tube bore over an inner spigot
and the tube outside inside a cup. Inputs from `manifest.json`/`gen_nodes.py:997-1016` are:

- 20 mm inner engagement at 100 tree ends and 2 mm at 332 closing ends;
- outer cup overlap `min(2.5 mm, engagement)`, hence 2.5 mm tree and 2 mm closing;
- 0.15 mm radial clearance, 2.0 mm spigot wall, and 1.6 mm input lip wall; the latter produces
  a 1.45 mm nominal physical cup wall and 1.44 mm measured minimum;
- 10x8 main tube and 14x12 rim tube, full wrap at all 432 ends.

### Transparent lumped sensitivity

For an annular branch,

`I = pi(Do^4-Di^4)/64`, `k_adherend = E_h I/L_s`.

For a concentric bond surface of radius `R`, overlap `L_s`, adhesive shear modulus `G_a`, and
bondline thickness `t_a`, uniform rigid-adherend slip gives

`k_bond = (G_a/t_a) integral(z^2 dA) = (G_a/t_a) pi R^3 L_s`.

Within each inner/outer branch bond and adherend are series; the branches are parallel:

`k_theta = [1/k_bond,i + 1/k_spigot]^-1 + [1/k_bond,o + 1/k_cup]^-1`.

Perfect bond reduces this sensitivity to `E_h(I_s/L_s + I_c/L_c)`. For the current 10x8
socket, `r_s=3.85 mm`, `r_si=1.85 mm`, `r_ci=5.15 mm`, `r_co=6.60 mm`, so
`I_s=163.357 mm4` and `I_c=937.789 mm4`. At 6 GPa this gives 2,299.7 N m/rad for a tree end and
3,303.4 N m/rad for a closing end. The 14x12 values are 5,608.7 for a hypothetical tree end and
8,972.5 N m/rad for the actual closing rim ends (all rims are closing members).

This is a **sensitivity, not a bound**: applying the full moment through the adherend while
omitting distributed tube/bond compatibility, root deformation, hub rotation, peel, and
three-dimensional node coupling mixes conservative and nonconservative errors. A defensible
physical stiffness needs a measured moment-rotation curve or a validated distributed/FE model.

### Distributed and segmented licensing solve — terminated as NOT COMPUTABLE

The reviewed design's licensing model is the generalized eigenproblem over the full hub-centre
distance, not a short-cut Euler member:

`[K_b(E_t I_t(x), E_h I_h(x), G_a/t_a, K_hub) - P K_g] q = 0`.

On each overlap, compatibility requires separate tube and printed-adherend curvature fields and
the bond's distributed slip/peel law; outside it, the element properties switch among tube,
printed arm/root, and central hub. This avoids counting both a socket spring and a fictitious
carbon tube through the printed end. The two article-A end records would set every segment, and
the reported eigenvalue would use the 166--251 mm **hub-centre-to-hub-centre** length.

That matrix cannot be populated from the repository. The generated STL/manifest gives volume,
clearance, engagement, and a few minimum sections, but no load-axis `I_SDF(x)`, printed material
tensor mapped to each arm, bond `G_a/t_a` or peel law, root compliance, central-hub rotational
impedance, or global no-sway boundary. Assuming any of them rigid is the restraint being tested.
The distributed/segmented solve therefore stops before assembly; its physical `k_theta` and `K`
are **NOT COMPUTABLE**, not zero and not the nominal-annulus value below. The executable's
uniform full-length beam is only the common abstract
`k_eq at hub centres -> formal K -> tube` demand curve. Its `k_eq` is not the tube-end socket
spring above: equating the two would both extend carbon `EI` through the printed offsets and add
the socket compliance. The lumped annuli therefore price plausible stiffness order-of-magnitude
only; they cannot be converted to a physical or conditional member `K` without the terminated
segmented solve.

The executable prices that omission for **all actual paired end classes**, rather than one
representative span. Its geometric bond-area reconciliation uses
`A_b=2 pi r_s L_s + 2 pi r_c L_c` on the same radii as the spring model:

| actual paired end class | ends | recorded area/end; total | nominal spring-model area/end; total |
|---|---:|---:|---:|
| main tree | 100 | 581.195; 58,119.5 mm2 | 564.701; 56,470.1 mm2 |
| main closing | 260 | 113.097; 29,405.3 mm2 | 113.097; 29,405.3 mm2 |
| rim closing | 72 | 113.097; 8,143.0 mm2 | 163.363; 11,762.1 mm2 |
| **all article-A ends** | **432** | **95,667.8 mm2** | **97,637.6 mm2** |

The rim mismatch is the prior audit's global-10x8 assembly-probe defect; the nominal column is
only the corrected concentric 14x12 geometry, not a measured contacted area. Solving the shown
series/parallel equation for `q=G_a/t_a` at 6 GPa gives:

| end class | formal full-span target | abstract k_eq over actual centre lengths | q giving the same scalar in the uncoupled lumped socket model |
|---|---:|---:|---:|
| main tree | K=0.70 / 0.65 | 559--841 / 852--1,282 N m/rad | 6.16e11--1.14e12 / 1.16e12--2.54e12 Pa/m |
| main closing | K=0.70 / 0.65 | 559--841 / 852--1,282 | 5.67e11--9.62e11 / 9.79e11--1.81e12 Pa/m |
| rim closing | K=0.70 / 0.65 | 1,722--1,729 / 2,624--2,636 | 6.06e11--6.09e11 / 1.06e12--1.07e12 Pa/m |

This is a **two-model scalar comparison, not a socket-to-K conversion**: the first model asks what
hub-centre spring a uniform carbon span would require, and the second asks what nominal bond
parameter produces the same number before the missing offsets and hub compliance are assembled.
At a merely illustrative 0.20 mm bondline, multiply `q` by `2e-13` to obtain `G_a` in GPa.
For the common abstract tube-optimum knee, the required `q` at 1,210 / 2,150 N m/rad is respectively
`2.24e12 / 2.94e13` main-tree, `1.65e12 / 5.46e12` main-closing, and
`3.96e11 / 8.06e11 Pa/m` rim-closing. Neither `G_a`, `t_a`, peel, nor shear-lag qualification
exists. The fast rise near the main-tree perfect-bond limit of 2,299.7 N m/rad shows why the
physical upper edge of the catalogue plateau cannot be claimed from nominal modulus alone.

### Spring-to-K equation

For the reduced, non-sway beam with end rotations reacting against **grounded hubs**,

`y=A sin(lambda xi)+B cos(lambda xi)+C xi+D`,
`lambda^2=P L^2/(EI)`, and `r_i=k_i L/(EI)`.

The boundary conditions are

`y(0)=y(1)=0`, `y''(0)-r_0 y'(0)=0`, `y''(1)+r_1 y'(1)=0`.

Removing the trivial zero factors gives the characteristic equation

`lambda^3 sin(lambda) - lambda^2(r0+r1)cos(lambda)`
`- lambda r0 r1 sin(lambda) + lambda(r0+r1)sin(lambda)`
`- 2 r0 r1[cos(lambda)-1] = 0`,

and `K=pi/lambda_1`, with the physical first root bracketed on `[pi,2pi]`. Checks recover
`K=1.000000` pinned-pinned, `0.699156` pinned-fixed, and `0.500000` fixed-fixed.

The current geometry's perfect-bond lumped annulus numbers are:

| hub modulus/material sensitivity | lumped annulus k_theta over actual ends (N m/rad) | effective member K |
|---|---:|---:|
| repository PAHT Z, 2.18 GPa | 836--3,260 | NOT COMPUTABLE |
| repository PAHT XY, 3.86 GPa | 1,480--5,772 | NOT COMPUTABLE |
| PAHT-CF 6 GPa `[TO VERIFY]` | 2,300--8,972 | NOT COMPUTABLE |
| PAHT-CF 8 GPa `[TO VERIFY]` | 3,066--11,963 | NOT COMPUTABLE |
| AlSi10Mg 70 GPa `[TO VERIFY]` | 26,830--104,679 | NOT COMPUTABLE |
| Ti6Al4V 110--115 GPa `[TO VERIFY]` | 42,161--171,973 | NOT COMPUTABLE |

There is deliberately no material-to-K read-across: the socket acts at the physical tube end,
while the directional curve's abstract spring acts at the hub centre. The local socket is also
relative tube-to-hub; a real hub co-rotates with its other arms. The global rotational impedance
and eigenmode are absent. The frozen P13
screen also reports 216 failures, but only its 144 non-rim spoke/tie rows survive the known
global-SKU probe defect; the 72 rim rows need a per-SKU SDF rerun. Thus the screen supplies
independent non-rim failure evidence, not the previously quoted corrupt 0.0406 physical margin.
The only honest physical entry is **K = NOT COMPUTABLE**, and 0.65 is
**UNLICENSED/UNSAFE IF CREDITED**.

## Finding 3 — directional tube trade, with film bending carried

The article-A catalogue uses the reviewed R1 wall set and 0.5 mm OD steps, capped at 30 mm OD;
walls are 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.75, 1.00, 1.50, 2.00 mm. It is invented,
not supplier-qualified. One main SKU must hold all 180 non-rim members and one rim SKU all 36
rims. The exhaustive proof below also checks every lighter full-R1-range section outside that cap.

For every actual member and candidate section the calculation requires:

`P_fact < Pcr(k_theta)`,

`P_fact < 0.605 K_LOCAL ORTHO_PENALTY E (t/R) A`, and

`P_fact/A + 1.5 max|M_service(P_fact,k_theta)|/Z < sigma_T700`.

`M_service` comes from the closed-form compressed Euler-Bernoulli beam with the same end springs,
not an interpolation. A 24/48-element solve independently checks it. The axial term is the already
factored demand; the UDL is one-atmosphere service film load and receives 1.5 exactly once in the
stress check. The
unloaded equal-spring identity is

`|M_end|=(wL^2/12)r/(r+2)`, `M_mid=wL^2/8-|M_end|`.

Thus pinned maximum is `wL^2/8`, not the work order's erroneous `/24` shorthand; fixed support
maximum is `wL^2/12`, while fixed midspan is `/24`. Numerical checks at `w=1000 N/m`, `L=.25 m`
give 7.812500 N m pinned and 5.208333 N m fixed.

### Rotational-stiffness curve

The joint column below is the **current 0.715 kg PAHT set divided by V = 4.012 kg/m3**, shown only
as the requested common reference. It is not the mass of the resized socket, so the reference
total is a break-even envelope, not a build. Exact current film is 0.028304 kg/article or
0.158833 kg/m3.

| abstract k_eq at hub centres (N m/rad, both ends) | formal K range | main / rim OD x wall (mm) | tube kg/m3 | reference joint kg/m3 | reference total incl. film kg/m3 |
|---:|---:|---|---:|---:|---:|
| 0 | 1.000--1.000 | 16.0x0.25 / 22.0x0.25 | 4.722 | 4.012 | 8.893 |
| 30 | 0.972--0.989 | 16.0x0.25 / 21.5x0.25 | 4.696 | 4.012 | 8.867 |
| 100 | 0.903--0.962 | 15.0x0.25 / 21.0x0.25 | 4.442 | 4.012 | 8.613 |
| 300 | 0.734--0.888 | 13.0x0.25 / 20.0x0.25 | 3.933 | 4.012 | 8.104 |
| 1,000 | 0.580--0.690 | 12.0x0.25 / 17.0x0.25 | 3.550 | 4.012 | 7.721 |
| 1,200 | 0.568--0.657 | 12.0x0.25 / 16.5x0.25 | 3.524 | 4.012 | 7.695 |
| **1,210** | **0.568--0.646** | **12.0x0.25 / 16.0x0.25** | **3.498** | **4.012** | **7.669** |
| **1,500** | **0.555--0.624** | **12.0x0.25 / 16.0x0.25** | **3.498** | **4.012** | **7.669** |
| **2,150** | **0.539--0.591** | **12.0x0.25 / 16.0x0.25** | **3.498** | **4.012** | **7.669** |
| 2,151 | 0.539--0.599 | 12.0x0.25 / 16.5x0.25 | 3.524 | 4.012 | 7.695 |
| 3,000 | 0.528--0.574 | 12.0x0.25 / 16.5x0.25 | 3.524 | 4.012 | 7.695 |
| 10,000 | 0.510--0.523 | 12.5x0.25 / 16.5x0.25 | 3.638 | 4.012 | 7.809 |
| 30,000 | 0.503--0.509 | 12.5x0.25 / 17.0x0.25 | 3.664 | 4.012 | 7.835 |
| fixed floor | 0.500--0.500 | 12.5x0.25 / 17.0x0.25 | 3.664 | 4.012 | 7.835 |

At the representative 1,500 N m/rad point the worst article-A moments are 65.65 N m rim,
38.49 N m spoke, and 19.60 N m in-plane tie. At the fixed floor they rise to 74.28, 39.84,
and 20.39 N m. At 1,500 the combined-stress minimum margin is 1.034 (spoke), and the corrected
axial local-wall minimum is 1.066 (in-plane tie). Local buckling therefore nearly re-governs;
it was not held fixed or dropped. Nevertheless **every row remains NOT QUALIFIED for bending-local
buckling/ovalization**, because the repository has no validated combined shell criterion.

The same solve sends these **factored article-A joint resultants** into each socket at 1,500;
they are demands only, because no qualified joint capacity is available. Axial demand already
contains the model's 1.5 factor; service film reactions and end moments are multiplied by 1.5
once here:

| family; selected tube | axial N | transverse end reaction N | end moment N m | max member moment N m |
|---|---:|---:|---:|---:|
| rim; 16x0.25 | 4,476.6 | 2,543.5 | 98.48 | 98.55 |
| spoke; 12x0.25 | 2,238.3 | 1,336.4 | 57.73 | 57.77 |
| in-plane tie; 12x0.25 | 5,037.7 | 956.8 | 29.40 | 29.42 |
| octet / tripod / inward tie; 12x0.25 | 3,376.5 / 4,775.1 / 4,775.1 | 0 | 0 | 0 |

These resultants expose the missing load-path gate: a stiffness-only material substitution must
also carry up to 98.48 N m and 2.54 kN per loaded rim end. This report assigns no zero-mass or
infinite-strength fitting, adhesive, root, or hub to those demands.

### The honest knee and sharpness

The global minimum of this finite abstract-spring catalogue is a plateau bounded by
integer-stiffness transition searches. An independent closed-form beam-column enumeration tested
all **149 main and 202 rim sections lighter** than the selected 12x0.25 and 16x0.25 sections over
`0 <= k_eq <= 1e10 N m/rad`, refining every local minimum on a 0.1-decade grid. None qualifies:
the closest lighter main is 11.5x0.25 with minimum utilization 1.02609 at 532.38 N m/rad, and the
closest lighter rim is 15.5x0.25 with 1.04067 at 1,285.68 N m/rad. This closes the sparse-sweep
hole: the transition bisections locate the proven minimum pair's edges rather than assuming no
lighter pair exists between sample points. The full R1 OD range adds eighteen lighter rim-area
sections at 30.5--39.0x0.10 outside the declared article-A cap; all fail the stiffness-independent
local-wall gate, with maximum margin only 0.19548. Thus the cap does not hide a lighter solution.

The selected pair's exact beam-column transition results are:

- at 1,209 N m/rad the 16.5 mm rim is still required; at 1,210 the 16.0 mm rim passes;
- the same lightest pair remains selected through 2,150 N m/rad; at 2,151 the 16.0 mm rim
  fails combined action and the 16.5 mm rim returns;
- 1,000 to the plateau saves 0.00916 kg/article, or 0.0514 kg/m3;
- fixed adds 0.02955 kg/article, or 0.1658 kg/m3, relative to the plateau.

With the requested fixed 0.715 kg reference joint, total slope is exactly zero inside the
catalogue plateau. At its integer boundaries it changes discontinuously by -0.02570 kg/m3 from
1,209 to 1,210 and +0.02570 kg/m3 from 2,150 to 2,151: a one-unit `k_theta` increment changes
the selected rim SKU. That is catalogue sharpness, not a physical derivative; a continuously
optimized tube and regenerated-joint mass curve is among the uncomputed redesign quantities.

The maximum tube value of the abstract restraint relative to the pinned catalogue point is
`0.841442-0.623382 = 0.218061 kg/article = 1.22368 kg/m3`. A stiffer joint may add at most
0.218 kg/article before consuming all of that saving. Past 2,150 N m/rad, added stiffness
buys no tube in this catalogue; it increases support-moment demand and soon increases tube mass.

## Finding 4 — material and joint-mass trade

Material values below are operator-supplied and `[TO VERIFY]`: PAHT-CF 1,060 kg/m3 and 6--8 GPa;
AlSi10Mg SLM 2,670 and 70 GPa; Ti6Al4V SLM 4,430 and 110--115 GPa. This exact
**same-geometry substitution** holds today's 10x8/14x12 tube and current 0.715 kg SDF volume.
It is the only material comparison reproducible without inventing a redesigned hub. The tube
therefore remains 10.910 kg/m3; joint mass is `0.715(rho/1060)/V`; exact film is 0.159 kg/m3.

| material sensitivity | lumped current-end k_theta (N m/rad) | tube kg/m3 | joint kg/m3 (kg/article) | tube + joint | incl. film | x wall |
|---|---:|---:|---:|---:|---:|---:|
| PAHT-CF 6 GPa | 2,300--8,972 | 10.910 | 4.012 (0.715) | 14.923 | **15.082** | 15.76 |
| PAHT-CF 8 GPa | 3,066--11,963 | 10.910 | 4.012 (0.715) | 14.923 | **15.082** | 15.76 |
| AlSi10Mg 70 GPa | 26,830--104,679 | 10.910 | 10.107 (1.801) | 21.017 | **21.176** | 22.13 |
| Ti6Al4V 110 GPa | 42,161--164,496 | 10.910 | 16.769 (2.988) | 27.679 | **27.838** | 29.09 |
| Ti6Al4V 115 GPa | 44,078--171,973 | 10.910 | 16.769 (2.988) | 27.679 | **27.838** | 29.09 |

PAHT is lowest only among these exact substitutions. Aluminium and titanium are nearly tied in
specific stiffness, but both are already far beyond the directional tube knee and add 1.086 or
2.273 kg/article of hub mass. A smaller metal socket could change that mass, but its geometry,
process walls, SDF volume, bond, strength, and assembly are unmodelled. Enumerating and
generating every viable tube/socket pair is required to name a physical material optimum;
that optimum is **NOT COMPUTABLE**. Adhesive, seams, barrier, fasteners, vents, supports, and
capture remain positive unmodelled mass, not zero.

Sensitivity to the `[TO VERIFY]` inputs is transparent: same-geometry `k_theta` is linear in
`E_h` and joint mass is linear in `rho`. Thus PAHT's 6--8 GPa range moves every nominal stiffness
by +/-14.3% about 7 GPa without changing its table mass; titanium's 110--115 GPa range moves it
4.45% while leaving density fixed. The supplied specific moduli are 5.66--7.55, 26.22, and
24.83--25.96 MJ/kg for PAHT, aluminium, and titanium. This supports aluminium over titanium for
a stiffness-driven redesign, but it cannot overturn the current-geometry mass result or license
a smaller joint. Bondline, process anisotropy, porosity, and minimum metal wall are not zero;
their uncertainty is outside this provisional material-only sensitivity.

## R1 implication

The reviewed R1 totals at `0f0899a...` remain 10.76--12.51 kg/m3 with pinned face members and
OD-cubed joint estimates. The appendix now carries that work's exact four-case HH/HS/coplanar
film envelope, 948/6,840 finite-cut ledgers, factored axial force, 0.605-corrected local check,
and simultaneous beam-column bending through a **tube-only** spring sweep:

| R1 article A object | pinned tube kg/m3 (SKU mm) | best sampled spring: k_theta, tube kg/m3 (SKU) | fixed tube kg/m3 (SKU) |
|---|---:|---:|---:|
| 1 m, n=2, 948 cuts | 4.511 (18.0x0.15) | 1,000; **3.374** (13.5x0.15) | 3.626 (14.5x0.15) |
| 2 m, n=2, 948 cuts | 4.511 (36.0x0.30) | 10,000; **3.374** (27.0x0.30) | 3.563 (28.5x0.30) |
| 4 m, n=2, 948 cuts | 5.034 (64.5x0.75) | 30,000; **3.731** (48.0x0.75) | 3.968 (51.0x0.75) |
| 3 m, n=4, 6,840 cuts | 4.263 (25.5x0.25) | 3,000; **3.166** (19.0x0.25) | 3.419 (20.5x0.25) |
| 6 m, n=4, 6,840 cuts | 4.263 (51.0x0.50) | 30,000; **3.208** (38.5x0.50) | 3.377 (40.5x0.50) |

These are sampled directional tube minima, not replacements for the checked R1 totals: the
invented catalogue selects very large, thin tubes because joint mass is deliberately absent.
Every row remains unqualified for bending-local ovalization. No even-n joint geometry,
moment-rotation curve, or joint mass exists, so R1 joint-plus-tube and physical optima are
**NOT COMPUTABLE**. The result nevertheless confirms the same finite optimum: fixed ends are
0.19--0.25 kg/m3 heavier in tube than each sampled minimum.

## Reproducibility

The computation read commit `1833121532102c009b0062e3364431aa35eb022d` plus reviewed objects
`49f901b1894e71d44557d5648904359708fecf65` and
`0f0899a23ffb3c2674d84a1928b3c2ac55bc8025`. Input SHA-256 values were:

- `assembly.json`: `47671e27f8b875c2eeef1901fa6fb84f17f67e3e75280e539533ba553cfac86e`
- `manifest.json`: `96a4dd7e171f88dbb43b4a2e7d667e06d34d80e0cb861d4fb8da2c6884ad49dc`
- `vacuum-cell.py`: `dfc47a2d5bf7618457f7afbf81d599cb023f86d178ca944e043e1b994d6a2186`
- embedded solver: `a4597d52e21731f9d4bc00bb1036711e1ab3856b303e1735f73e075ab676652f`

The executable appendix below imports the live model constants, derives unrounded film line
loads (13,923.82884 rim, 7,332.08061 spoke, 7,439.21604 N/m square tie), enumerates all 216
assembly members, solves the characteristic equation with a dependency-free 100-step bracketed
bisection (including logarithmic endpoint probes), and uses the closed-form compressed-beam
solution for article-A section selection. Its 24/48-element solution is an independent convergence
check and supplies the displayed joint-resultant ledger and R1 sweep.
It also reproduces the reviewed R1 HH/HS/coplanar construction directly from model functions,
uses the model's 948/6,840 finite strut counts, and emits all five R1 spring sweeps.
Its mandatory checks recover `K={1,0.699156,0.5}` for pin-pin/pin-fix/fix-fix,
`K=0.999999999` for equal `1e-6 N m/rad` springs, and `K=0.634089` for unequal 500/2,500
N m/rad springs with normalized characteristic residual `1.76e-16`. It recovers
`M={wL^2/8,wL^2/12}` for unloaded pinned/fixed UDL and matches the exact pinned beam-column
magnifier at `P/Pcr=0.3` to 0.00268% with 96 elements. At the representative 1,500 N m/rad
point, 24-to-48 elements changes the maximum moment by 0.0481% rim, 0.0589% spoke, and 0.0658%
square tie. The 1,210 and 2,151 catalogue transitions are found by executable integer bisection,
and the independent closed-form enumeration emits all 351 within-cap lighter-section checks plus
the eighteen beyond-cap local-wall rejections and each closest rejection; none is embedded as an
unsupported assertion. Raw JSON rows retain their named exact/FE method and tables above are
rounded only for presentation.

Run it from a clean checkout as `python3 end_fixity.py /path/to/checkout > result.json`.

<details>
<summary>Complete executable <code>end_fixity.py</code></summary>

```python
#!/usr/bin/env python3
"""Read-only directional end-fixity trade for the 2026-08-12 audit."""
import hashlib
import importlib.util
import json
import math
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
ASSEMBLY = ROOT / 'research/geometry/nodes/assembly.json'
MANIFEST = ROOT / 'research/geometry/nodes/manifest.json'
VC_PATH = ROOT / 'research/analysis/vacuum-cell.py'
spec = importlib.util.spec_from_file_location('vc', VC_PATH)
vc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vc)

E_TUBE = vc.MATERIALS['T700_LAM']['E']
SIG_TUBE = vc.MATERIALS['T700_LAM']['sigma']
RHO_TUBE = vc.MATERIALS['T700_LAM']['rho']
SF = vc.LATTICE_SF
VOL = 0.709 ** 3 / 2
WALL = 0.956859
ODS = [x / 2 for x in range(8, 61)]
WALLS = [0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.75, 1.00, 1.50, 2.00]
KTHETAS = [0, 30, 100, 300, 1000, 1200, 1209, 1210, 1500, 2150, 2151,
           3000, 10000, 30000, 1e9]
R1_ODS = [x / 2 for x in range(8, 261)]
R1_KTHETAS = [0, 1000, 3000, 10000, 30000, 100000, 300000, 1e6, 1e9]

# Reproduce the unrounded service line loads behind film_edge_loads(); that public
# reporting function rounds to whole N/m before returning its table.
_faces = vc.kelvin_faces(0.709)
_edge = _faces['edgeM']
_tri_t, _sin_a = vc.panel_tension(vc.PANEL['hexSpoked'] * _edge)
_sq_t, _ = vc.panel_tension(vc.PANEL['squareSpoked'] * _edge)
_cos_a = math.sqrt(1.0 - _sin_a ** 2)
_half = math.acos(-1.0 / 3.0) / 2.0
FILM_W = {
    'rim': 2.0 * _tri_t * (math.cos(_half) * _cos_a + math.sin(_half) * _sin_a),
    'spoke': 2.0 * _tri_t * _sin_a,
    'vertexTieInPlane': 2.0 * _sq_t * _sin_a,
}


def section(od_mm, wall_mm):
    ro = od_mm / 2000
    ri = (od_mm - 2 * wall_mm) / 2000
    if ri <= 0:
        return None
    return {'od': od_mm, 'wall': wall_mm,
            'A': math.pi * (ro * ro - ri * ri),
            'I': math.pi / 4 * (ro ** 4 - ri ** 4),
            'Z': math.pi / 4 * (ro ** 4 - ri ** 4) / ro,
            'ro': ro}


CAT = [section(od, wall) for od in ODS for wall in WALLS if od > 2 * wall]


def char(lam, r0, r1):
    """Normalized rotational-spring characteristic; zero factors excluded by bracket."""
    return (lam ** 3 * math.sin(lam) - lam ** 2 * (r0 + r1) * math.cos(lam)
            - lam * r0 * r1 * math.sin(lam) + lam * (r0 + r1) * math.sin(lam)
            - 2 * r0 * r1 * (math.cos(lam) - 1))


def bisect_root(fn, a, b, iterations=100):
    """Dependency-free bracketed root solve."""
    fa, fb = fn(a), fn(b)
    if fa == 0:
        return a
    if fb == 0:
        return b
    if fa * fb > 0:
        raise ValueError((a, b, fa, fb))
    for _ in range(iterations):
        c = (a+b)/2
        fc = fn(c)
        if fa*fc <= 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return (a+b)/2


@lru_cache(maxsize=None)
def lambda1(k0, k1, L, EI):
    if k0 == 0 and k1 == 0:
        return math.pi
    r0, r1 = k0 * L / EI, k1 * L / EI
    # Log-spaced endpoint probes catch the root as it leaves pi under a very soft spring;
    # the regular grid covers the rest of the interval.
    eps = [10.0**p for p in range(-13, -1)]
    xs = sorted(set([math.pi+x for x in eps]
                    + list(np.linspace(math.pi+.01, 2*math.pi-1e-10, 1201))))
    vals = [char(x, r0, r1) for x in xs]
    roots = []
    for a, b, fa, fb in zip(xs[:-1], xs[1:], vals[:-1], vals[1:]):
        if fa * fb < 0:
            roots.append(bisect_root(lambda x: char(x, r0, r1), a, b))
    if roots:
        return min(roots)
    # Only the numerical fixed limit may land on the upper endpoint.
    if min(r0, r1) > 1e8:
        return 2 * math.pi
    raise ValueError(f'no characteristic root: r0={r0}, r1={r1}')


@lru_cache(maxsize=None)
def beam_response(L, EI, P, w, k0, k1, elements=24):
    """Second-order EB beam under service UDL; P is already factored."""
    n = elements
    le = L / n
    nd = 2 * (n + 1)
    K = np.zeros((nd, nd))
    F = np.zeros(nd)
    ke = EI / le ** 3 * np.array([
        [12, 6*le, -12, 6*le], [6*le, 4*le**2, -6*le, 2*le**2],
        [-12, -6*le, 12, -6*le], [6*le, 2*le**2, -6*le, 4*le**2]])
    kg = P / (30 * le) * np.array([
        [36, 3*le, -36, 3*le], [3*le, 4*le**2, -3*le, -le**2],
        [-36, -3*le, 36, -3*le], [3*le, -le**2, -3*le, 4*le**2]])
    fe = w * le / 12 * np.array([6, le, 6, -le])
    for i in range(n):
        ix = [2*i, 2*i+1, 2*i+2, 2*i+3]
        K[np.ix_(ix, ix)] += ke - kg
        F[ix] += fe
    K[1, 1] += k0
    K[-1, -1] += k1
    fixed = {0, 2*n}
    free = [i for i in range(nd) if i not in fixed]
    d = np.zeros(nd)
    d[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    moments = []
    for i in range(n):
        ix = [2*i, 2*i+1, 2*i+2, 2*i+3]
        q = ke @ d[ix] - fe
        moments.extend([q[1], -q[3]])
    return max(abs(x) for x in moments), abs(k0*d[1]), abs(k1*d[-1])


def load_members():
    a = json.loads(ASSEMBLY.read_text())
    m = json.loads(MANIFEST.read_text())
    cuts = {(r['family'], round(r['cutMm'], 3)): r for r in m['cutList']}
    pairs = {}
    for e in a['ends']:
        pairs.setdefault(e['memberIndex'], []).append(e)
    rows = []
    for index, ends in sorted(pairs.items()):
        if len(ends) != 2:
            raise AssertionError((index, len(ends)))
        e = ends[0]
        cr = min(m['cutList'], key=lambda r: (r['family'] != e['family'],
                                              abs(r['cutMm'] - e['cutLengthMm'])))
        cut = cr['closingCutMm'] if e['isClosingMember'] else cr['cutMm']
        key = e['family'] if e['family'] != 'tie' else e['tieKind']
        w = FILM_W.get(key, 0.0)
        rows.append({'index': index, 'family': key, 'sku_family': 'rim' if key == 'rim' else 'main',
                     'L': e['memberLengthMm']/1000, 'cut': cut/1000,
                     'P': e['axialN'], 'w': w, 'closing': e['isClosingMember']})
    assert len(rows) == 216
    return rows


MEMBERS = load_members()


def equal_lambda(k, L, EI):
    """Fast equal-spring first root; endpoint signs bracket it for every k > 0."""
    if k == 0:
        return math.pi
    r = k*L/EI
    return bisect_root(lambda x: char(x, r, r), math.pi, 2*math.pi)


def exact_max_moment(L, EI, P, w, k):
    """Closed-form compressed EB beam under UDL and equal end springs."""
    if w == 0:
        return 0.0
    b = math.sqrt(P/EI)
    s, c = math.sin(b*L), math.cos(b*L)
    matrix = np.array([
        [0, 1, 0, 1],
        [s, c, L, 1],
        [-k*b, -EI*b*b, -k, 0],
        [-EI*b*b*s+k*b*c, -EI*b*b*c-k*b*s, k, 0]])
    rhs = np.array([0, -w*L*L/(2*P), -EI*w/P, -EI*w/P-k*w*L/P])
    A, B, _, _ = np.linalg.solve(matrix, rhs)
    points = [0.0, L]
    if abs(B) > 1e-30:
        first = math.atan(A/B)/b
        for n in range(-2, 5):
            x = first+n*math.pi/b
            if 0 < x < L:
                points.append(x)
    return max(abs(EI*(-A*b*b*math.sin(b*x)-B*b*b*math.cos(b*x)+w/P))
               for x in points)


def exact_family_utilization(s, sku_family, k):
    """Worst exact utilization over deduplicated structural cases in one SKU family."""
    cases = {}
    for m in MEMBERS:
        if m['sku_family'] == sku_family:
            cases[(m['family'], m['L'], m['P'], m['w'])] = m
    values = []
    for m in cases.values():
        EI = E_TUBE*s['I']
        lam = equal_lambda(k, m['L'], EI)
        pcr = lam*lam*EI/m['L']**2
        local = (0.605*vc.K_LOCAL*vc.ORTHO_PENALTY*E_TUBE
                 * (s['wall']/1000)/s['ro']*s['A'])
        M = exact_max_moment(m['L'], EI, m['P'], m['w'], k)
        stress = m['P']/s['A']+SF*M/s['Z']
        values.append(max(m['P']/pcr, m['P']/local, stress/SIG_TUBE))
    return max(values)


def minimum_utilization(s, sku_family):
    """Refine every local basin on log10(k+1) in [0,10]."""
    xs = [i/10 for i in range(101)]
    objective = lambda x: exact_family_utilization(s, sku_family, 10**x-1)
    ys = [objective(x) for x in xs]
    candidates = list(zip(ys, xs))
    phi = (math.sqrt(5)-1)/2
    for i in range(1, len(xs)-1):
        if ys[i] <= ys[i-1] and ys[i] <= ys[i+1]:
            a, b = xs[i-1], xs[i+1]
            c, d = b-phi*(b-a), a+phi*(b-a)
            fc, fd = objective(c), objective(d)
            for _ in range(45):
                if fc < fd:
                    b, d, fd = d, c, fc
                    c = b-phi*(b-a)
                    fc = objective(c)
                else:
                    a, c, fc = c, d, fd
                    d = a+phi*(b-a)
                    fd = objective(d)
            x = (a+b)/2
            candidates.append((objective(x), x))
    value, x = min(candidates)
    return value, 10**x-1


def lighter_section_proof(sku_family, selected):
    lighter = [s for s in CAT if s['A'] < selected['A']-1e-18]
    checked = []
    for s in lighter:
        utilization, k = minimum_utilization(s, sku_family)
        checked.append((utilization, k, s))
    utilization, k, closest = min(checked, key=lambda row: row[0])
    assert utilization > 1.0
    return {'family': sku_family, 'sectionsChecked': len(lighter),
            'closestRejected': f"{closest['od']:.1f}x{closest['wall']:.2f}",
            'minimumUtilization': utilization, 'atKthetaNmPerRad': k}


def excluded_large_od_proof():
    """Reject lighter rim sections beyond the declared 30 mm article-A OD cap."""
    selected = section(16, .25)
    excluded = [section(od, .10) for od in R1_ODS if od > max(ODS)
                and section(od, .10)['A'] < selected['A']]
    demand = max(m['P'] for m in MEMBERS if m['sku_family'] == 'rim')
    margins = []
    for s in excluded:
        local_sig = (0.605*vc.K_LOCAL*vc.ORTHO_PENALTY*E_TUBE
                     * (s['wall']/1000)/s['ro'])
        margins.append(local_sig*s['A']/demand)
    assert len(excluded) == 18 and max(margins) < 1.0
    return {'sectionsChecked': len(excluded),
            'odRangeMm': [excluded[0]['od'], excluded[-1]['od']],
            'wallMm': .10, 'maximumLocalWallMargin': max(margins)}


def qualifies(s, member, kt):
    EI = E_TUBE * s['I']
    lam = lambda1(kt, kt, member['L'], EI)
    pcr = lam * lam * EI / member['L'] ** 2
    if pcr < member['P']:
        return False, 'Euler', None
    local_sig = 0.605 * vc.K_LOCAL * vc.ORTHO_PENALTY * E_TUBE * (
        s['wall']/1000) / s['ro']
    if local_sig * s['A'] < member['P']:
        return False, 'local', None
    M = exact_max_moment(member['L'], EI, member['P'], member['w'], kt)
    stress = member['P']/s['A'] + SF*M/s['Z']
    if stress > SIG_TUBE:
        return False, 'stress', None
    return True, 'pass', {'K': math.pi/lam, 'Pcr': pcr, 'M': M,
                          'localMargin': local_sig*s['A']/member['P'],
                          'stressMargin': SIG_TUBE/stress}


@lru_cache(maxsize=None)
def best_for(kt, sku_family):
    group = [m for m in MEMBERS if m['sku_family'] == sku_family]
    viable = []
    for s in CAT:
        checks = [qualifies(s, m, kt) for m in group]
        if all(c[0] for c in checks):
            mass = sum(m['cut']*s['A']*RHO_TUBE for m in group)
            viable.append((mass, s, checks))
    return min(viable, key=lambda x: x[0]) if viable else None


def best_for_material(Ehub, sku_family):
    group = [m for m in MEMBERS if m['sku_family'] == sku_family]
    viable = []
    for s in CAT:
        idm = s['od'] - 2*s['wall']
        checks = [qualifies(s, m, hub_k(Ehub, s['od'], idm, m['closing'])) for m in group]
        if all(c[0] for c in checks):
            mass = sum(m['cut']*s['A']*RHO_TUBE for m in group)
            viable.append((mass, s, checks))
    return min(viable, key=lambda x: x[0]) if viable else None


def hub_k(E, od, idm, closing):
    """Perfect-bond lumped branch sensitivity, N m/rad."""
    rs = idm/2 - 0.15
    ris = max(0, rs - 2.0)
    rc = od/2 + 0.15
    roc = od/2 + 1.60
    Is = math.pi/4*(rs**4-ris**4)*1e-12
    Ic = math.pi/4*(roc**4-rc**4)*1e-12
    Ls = 0.002 if closing else 0.020
    Lc = 0.002 if closing else 0.0025
    return E*(Is/Ls+Ic/Lc)


def bond_k(q, E, od, idm, closing):
    """Rigid-slip bond plus annular-adherend series branches; q=G_a/t_a in Pa/m."""
    rs = idm/2 - 0.15
    ris = max(0, rs - 2.0)
    rc = od/2 + 0.15
    roc = od/2 + 1.60
    Is = math.pi/4*(rs**4-ris**4)*1e-12
    Ic = math.pi/4*(roc**4-rc**4)*1e-12
    Ls = 0.002 if closing else 0.020
    Lc = 0.002 if closing else 0.0025
    kb_i = q*math.pi*(rs/1000)**3*Ls
    kb_o = q*math.pi*(rc/1000)**3*Lc
    ka_i = E*Is/Ls
    ka_o = E*Ic/Lc
    return 1/(1/kb_i+1/ka_i) + 1/(1/kb_o+1/ka_o)


def q_for_k(target, E, od, idm, closing):
    """Required G_a/t_a for the lumped sensitivity, or None above its adherend limit."""
    if target >= hub_k(E, od, idm, closing):
        return None
    z = bisect_root(lambda logq: bond_k(10**logq, E, od, idm, closing)-target,
                    3, 18)
    return 10**z


def k_for_effective_K(target_K, L, EI):
    """Equal-end spring stiffness that gives target effective K for one prismatic span."""
    z = bisect_root(lambda logk: math.pi/lambda1(10**logk, 10**logk, L, EI)-target_K,
                    -6, 8)
    return 10**z


def characteristic_residual(lam, r0, r1):
    terms = [lam**3*math.sin(lam), -lam**2*(r0+r1)*math.cos(lam),
             -lam*r0*r1*math.sin(lam), lam*(r0+r1)*math.sin(lam),
             -2*r0*r1*(math.cos(lam)-1)]
    return abs(sum(terms))/sum(abs(x) for x in terms)


def transition(left_k, right_k, target_pair, entering):
    """Discover an integer catalogue boundary inside a bracket from the reported sweep."""
    lo, hi = left_k, right_k
    while lo + 1 < hi:
        mid = (lo+hi)//2
        pair = (best_for(mid, 'main')[1]['od'], best_for(mid, 'main')[1]['wall'],
                best_for(mid, 'rim')[1]['od'], best_for(mid, 'rim')[1]['wall'])
        if (pair == target_pair) == entering:
            hi = mid
        else:
            lo = mid
    return {'lastOutside' if entering else 'lastTarget': lo,
            'firstTarget' if entering else 'firstOutside': hi}


def r1_line_loads(span, n):
    """Reviewed even-n HH/HS/coplanar envelope, unrounded and at one atmosphere."""
    pitch = span / (2 * math.sqrt(2) * n)
    th, sa = vc.panel_tension(vc.PANEL['hexSpoked'] * pitch)
    ts, sas = vc.panel_tension(pitch / 2)
    assert math.isclose(sa, sas, abs_tol=1e-12)
    def dihedral(t1, t2, theta):
        beta = theta/2-math.asin(sa)
        return math.hypot((t1+t2)*math.cos(beta), (t1-t2)*math.sin(beta))
    return {
        'HH': dihedral(th, th, math.acos(-1/3)),
        'HS': dihedral(th, ts, math.pi-math.acos(1/math.sqrt(3))),
        'coplanarHex': 2*th*sa,
        'coplanarSquare': 2*ts*sa,
    }


def r1_best(span, n, kt):
    """Lightest one-SKU R1 tube under simultaneous factored axial + service-film bending."""
    L = span/(2*math.sqrt(2)*n)
    vol = span**3/2
    P = 3*vc.P_ATM*SF*vol/(96*n**3*L)
    w = max(r1_line_loads(span, n).values())
    count = vc.kelvin_lattice_counts(n)['struts']
    cat = sorted((section(od, wall) for od in R1_ODS for wall in WALLS
                  if od > 2*wall), key=lambda s: s['A'])
    for s in cat:
        EI = E_TUBE*s['I']
        lam = lambda1(kt, kt, L, EI)
        pcr = lam**2*EI/L**2
        local_sig = 0.605*vc.K_LOCAL*vc.ORTHO_PENALTY*E_TUBE*(s['wall']/1000)/s['ro']
        if min(pcr, local_sig*s['A']) < P:
            continue
        M = beam_response(L, EI, P, w, kt, kt)[0]
        stress = P/s['A'] + SF*M/s['Z']
        if stress <= SIG_TUBE:
            kg = count*L*s['A']*RHO_TUBE
            return {'span': span, 'n': n, 'kthetaNmPerRad': kt,
                    'od': s['od'], 'wall': s['wall'], 'tubeKg': kg,
                    'tubeKgM3': kg/vol, 'K': math.pi/lam,
                    'momentNm': M, 'stressMargin': SIG_TUBE/stress,
                    'localMargin': local_sig*s['A']/P}
    return None


def run():
    # Current-cut mass gate.
    current_mass = 0.0
    for m in MEMBERS:
        od, idm = (14, 12) if m['sku_family'] == 'rim' else (10, 8)
        A = math.pi/4*((od/1000)**2-(idm/1000)**2)
        current_mass += m['cut']*A*RHO_TUBE
    curves = []
    for kt in KTHETAS:
        main, rim = best_for(kt, 'main'), best_for(kt, 'rim')
        if not main or not rim:
            continue
        tm = main[0]+rim[0]
        all_checks = main[2]+rim[2]
        curves.append({'kthetaNmPerRad': kt, 'Kmin': min(c[2]['K'] for c in all_checks),
                       'Kmax': max(c[2]['K'] for c in all_checks),
                       'main': f"{main[1]['od']:.1f}x{main[1]['wall']:.2f}",
                       'rim': f"{rim[1]['od']:.1f}x{rim[1]['wall']:.2f}",
                       'tubeKg': tm, 'tubeKgM3': tm/VOL,
                       'governor': min((c[2]['stressMargin'], 'stress') for c in all_checks)[1],
                       'localMin': min(c[2]['localMargin'] for c in all_checks)})
    mats = []
    film_kg = vc.film_kg(.709)
    for name, rho, E in [('PAHT-6',1060,6e9),('PAHT-8',1060,8e9),
                         ('AlSi10Mg',2670,70e9),('Ti6Al4V-110',4430,110e9),
                         ('Ti6Al4V-115',4430,115e9)]:
        ks = [hub_k(E, 14 if m['sku_family']=='rim' else 10,
                       12 if m['sku_family']=='rim' else 8, m['closing']) for m in MEMBERS]
        joint = 0.715*rho/1060
        mats.append({'material':name,'kMin':min(ks),'kMax':max(ks),
                     'jointKg':joint,'jointKgM3':joint/VOL,
                     'tubeKg':current_mass,'tubeKgM3':current_mass/VOL,
                     'filmKgM3':film_kg/VOL,
                     'totalKgM3':(joint+current_mass+film_kg)/VOL})
    r1 = [r1_best(span, n, kt)
          for span, n in ((1,2),(2,2),(4,2),(3,4),(6,4))
          for kt in R1_KTHETAS]
    conv_cases = []
    for family in ('rim', 'spoke', 'vertexTieInPlane'):
        member = max((m for m in MEMBERS if m['family'] == family), key=lambda m: m['L'])
        sec = section(12, .25) if family != 'rim' else section(16, .25)
        m24 = beam_response(member['L'], E_TUBE*sec['I'], member['P'], member['w'],
                            1500, 1500, 24)[0]
        m48 = beam_response(member['L'], E_TUBE*sec['I'], member['P'], member['w'],
                            1500, 1500, 48)[0]
        conv_cases.append({'family': family, 'M24': m24, 'M48': m48,
                           'relativeChange': abs(m48/m24-1)})

    # Parameterized bond/adherend sensitivity on the three actual socket classes.
    raw_assembly = json.loads(ASSEMBLY.read_text())
    socket_classes = {}
    for e in raw_assembly['ends']:
        name = ('rim-closing' if e['family'] == 'rim'
                else 'main-closing' if e['isClosingMember'] else 'main-tree')
        c = socket_classes.setdefault(name, {'ends': [], 'od': e['pipeOdMm'],
                                              'id': e['pipeIdMm'],
                                              'closing': e['isClosingMember']})
        c['ends'].append(e)
    bond_sensitivity = []
    for name, c in sorted(socket_classes.items()):
        od, idm, closing = c['od'], c['id'], c['closing']
        Ls = 2.0 if closing else 20.0
        Lc = 2.0 if closing else 2.5
        rs, rc = idm/2-0.15, od/2+0.15
        nominal_area = 2*math.pi*rs*Ls + 2*math.pi*rc*Lc
        member_ids = {e['memberIndex'] for e in c['ends']}
        actual_members = [m for m in MEMBERS if m['index'] in member_ids]
        sec = section(14, 1) if name.startswith('rim') else section(10, 1)
        target_rows = {}
        for target_K in (.70, .65):
            targets = [k_for_effective_K(target_K, m['L'], E_TUBE*sec['I'])
                       for m in actual_members]
            qs = [q_for_k(k, 6e9, od, idm, closing) for k in targets]
            target_rows[str(target_K)] = {
                'kthetaRange': [min(targets), max(targets)],
                'qRangePaPerM': None if any(q is None for q in qs) else [min(qs), max(qs)]}
        knee_rows = {str(k): q_for_k(k, 6e9, od, idm, closing)
                     for k in (1210, 2150)}
        bond_sensitivity.append({
            'class': name, 'endCount': len(c['ends']),
            'recordedAreaPerEndMm2': [min(e['bondAreaMm2'] for e in c['ends']),
                                      max(e['bondAreaMm2'] for e in c['ends'])],
            'recordedAreaTotalMm2': sum(e['bondAreaMm2'] for e in c['ends']),
            'nominalAreaPerEndMm2': nominal_area,
            'nominalAreaTotalMm2': nominal_area*len(c['ends']),
            'perfectBondLimitNmPerRad': hub_k(6e9, od, idm, closing),
            'effectiveKTargets': target_rows, 'commonKneeQPaPerM': knee_rows})

    # Factored joint resultants at a representative point on the article-A curve.
    joint_loads = []
    for family in sorted({m['family'] for m in MEMBERS}):
        group = [m for m in MEMBERS if m['family'] == family]
        sku = group[0]['sku_family']
        s = best_for(1500, sku)[1]
        resultants = []
        for m in group:
            M, m0, m1 = beam_response(m['L'], E_TUBE*s['I'], m['P'], m['w'], 1500, 1500)
            resultants.append((m['P'], SF*m['w']*m['L']/2, SF*max(m0, m1), SF*M))
        joint_loads.append({'family': family,
                            'section': f"{s['od']:.1f}x{s['wall']:.2f}",
                            'factoredAxialN': max(x[0] for x in resultants),
                            'factoredEndShearN': max(x[1] for x in resultants),
                            'factoredEndMomentNm': max(x[2] for x in resultants),
                            'factoredMemberMomentNm': max(x[3] for x in resultants)})

    ref_sec = section(10, 1)
    ref_L, ref_EI = .25, E_TUBE*ref_sec['I']
    unequal_lam = lambda1(500, 2500, ref_L, ref_EI)
    unequal_r0, unequal_r1 = 500*ref_L/ref_EI, 2500*ref_L/ref_EI
    pcr_ref = math.pi**2*ref_EI/ref_L**2
    p_ref, w_ref = .3*pcr_ref, 1000.0
    beta = math.pi*math.sqrt(p_ref/pcr_ref)
    analytic_M = w_ref*ref_L**2/8 * (8/beta**2)*(1/math.cos(beta/2)-1)
    fe_M = beam_response(ref_L, ref_EI, p_ref, w_ref, 0, 0, 96)[0]
    exact_M = exact_max_moment(ref_L, ref_EI, p_ref, w_ref, 0)
    lighter_proof = [lighter_section_proof('main', section(12, .25)),
                     lighter_section_proof('rim', section(16, .25))]
    pair_mid = (best_for(1500, 'main')[1]['od'], best_for(1500, 'main')[1]['wall'],
                best_for(1500, 'rim')[1]['od'], best_for(1500, 'rim')[1]['wall'])
    out = {'volumeM3':VOL, 'wallKgM3':WALL, 'filmLineLoadsNPerM': FILM_W,
           'hashes': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in (ASSEMBLY, MANIFEST, VC_PATH)},
           'members': len(MEMBERS), 'cutM': sum(m['cut'] for m in MEMBERS),
           'currentTubeKg': current_mass, 'curve': curves, 'materials': mats,
           'r1TubeOnly': r1,
           'convergence24to48': conv_cases,
           'bondSensitivity': bond_sensitivity,
           'jointLoadsAt1500': joint_loads,
           'lighterSectionProof': lighter_proof,
           'excludedLargeOdProof': excluded_large_od_proof(),
           'catalogueTransitions': {
               'intoMinimumPlateau': transition(1200, 1500, pair_mid, True),
               'outOfMinimumPlateau': transition(1500, 3000, pair_mid, False)},
           'selfChecks': {
               'K_pinned': math.pi/lambda1(0,0,.25,E_TUBE*section(10,1)['I']),
               'K_tiny_equal_springs': math.pi/lambda1(1e-6,1e-6,ref_L,ref_EI),
               'K_pinned_fixed': math.pi/lambda1(0,1e12,.25,E_TUBE*section(10,1)['I']),
               'K_fixed': math.pi/lambda1(1e12,1e12,.25,E_TUBE*section(10,1)['I']),
               'K_unequal_500_2500': math.pi/unequal_lam,
               'unequalCharacteristicRelativeResidual': characteristic_residual(
                   unequal_lam, unequal_r0, unequal_r1),
               'beamPinnedM': beam_response(.25,E_TUBE*section(10,1)['I'],0,1000,0,0)[0],
               'beamFixedM': beam_response(.25,E_TUBE*section(10,1)['I'],0,1000,1e12,1e12)[0],
               'beamColumnPinnedAnalyticM': analytic_M,
               'beamColumnPinnedClosedFormM': exact_M,
               'beamColumnPinnedClosedFormRelativeError': abs(exact_M/analytic_M-1),
               'beamColumnPinnedFEM96M': fe_M,
               'beamColumnPinnedRelativeError': abs(fe_M/analytic_M-1)}}
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    run()
```

</details>

## Verdict

**Stiffening the joint is a dead end as a route to floating.** It is a real but small tube lever:
1.224 kg/m3 at most on this directional article-A catalogue, minimized on the
1,210--2,150 N m/rad plateau and reversing as film load migrates to the supports. Even the
incompatible frozen-joint envelope bottoms at 7.669 kg/m3, 8.01 times the 0.9569 kg/m3 wall;
the exact current-geometry PAHT point is 15.082 kg/m3. Metal makes the total worse.

The narrower research verdict is: measure the current joint's moment-rotation curve if useful,
but do not redesign around fixity before closing bond, fitting strength, global stability, and
tube ovalization. Until then, use pinned primary margins and treat every `K<1` mass row in this
audit as a directional, unlicensed sensitivity.
