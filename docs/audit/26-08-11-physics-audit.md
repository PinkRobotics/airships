# Status against today’s model

**Disposition: LAND IN PART — retain the dated audit and its still-live O5 challenge.**
The current `scale_study.py` and `subdivision_study.py` both exit 0, but neither emits
FLOAT §1's 9.31 / 9.34 / 9.05 / 8.65 kg/m³ totals. FLOAT now labels that table historical
and unreproduced. This directly contradicts its former claim to a current tool-derived optimum.

Several other findings are already addressed: the classical 0.605 coefficient now appears in
`arch_tube_strut()` and the M60J lattice computes 1.114930 kg/m³; `stock_build()` now bills
1.948 kg of tube, 0.715 kg of joints and 0.028 kg of skin, total 2.691 kg. The old 0.367 kg
saving is not an additional saving today. The assembly file now records 12/16 proofs passing;
that stored record was read, not regenerated. The old per-end censuses and provisional
missing-mass scenarios below were not rerun and must not be quoted as current measurements.

**Reproduction:** `python3 tools/scale_study.py`; `python3 tools/subdivision_study.py`;
`python3 tools/float_ledger.py` (bench, closed-form, scale and subdivision sections).

## Dated audit record

The text below records what was claimed on its audit date. “Today” in that text means that date. Only the reproductions above are current; historical numbers and review-era paths are preserved as evidence, not revalidated claims. See [the float ledger](../FLOAT-LEDGER.md).

---

# Independent physics audit of vacuum-cell article A

**Audit date:** 2026-08-12

**Object:** article A, Kelvin-cell span 709.000 mm (assembly geometry), subdivision `n=1`

**Float wall:** 0.9569 kg/m³ at 2,500 m

**Scope:** independent arithmetic audit; no model, generator, baseline, tolerance, or margin was
changed.

## Bottom line

Article A is not structurally proved. The external film load is assigned to member families,
but the combined member field is not a closing equilibrium solution: the checked certificate
has an 8.080 kN maximum node residual and balances only 9/51 nodes. Independently, P16 emits
2,296 `FAIL` verdicts among 3,888 scalar interface rows, although those overlapping rows mix
bounds, stand-ins, and one known measurement artifact rather than demonstrating 2,296 physical
failures. Correcting the checker's per-SKU annular areas analytically, the worst rim end reaches
only 11.10% of the assumed side-bond capacity. All 72 rim ends are closing ends with a 0.30 mm
adhesive-filled butt gap, so their direct bearing capacity is not computable from the printed-seat
screen. Those screens do not prove that a complete interface fails; they prove that adequacy is
not established.
Joint bending remains unquantified because neither ideal pinned nor clamped support behaviour is
licensed.

There is one loud favourable correction: **the real cut schedule makes article A's tube 0.367
kg lighter than `stockBuild` says, a reduction of 2.06 kg/m³ at nominal volume.** That saving is
real for this object. It does not rescue the float result: inward film bulge removes 8.57% of the
standalone article's displacement, while a provisional base budgeting scenario adds 0.095 kg of
previously omitted material and allowances. Combining those assumptions gives
2.611 kg / 0.16293 m³ = **16.03 kg/m³**, close to the model's 16.21 kg/m³ for the wrong reasons
and still 16.75 times the altitude wall. This is a scenario, not a replacement BOM: the current
interface is not demonstrated adequate, and any reinforcement found necessary after licensed
criteria and tests is presently uncomputable.

The §3 route table does not survive as a table of article configurations. R1 remains a useful
directional hypothesis and is actually lighter under a consistent bulk allocation (3.65× at its
best row, not 4.06×), R2 and R3 remain unquantified tasks, and R4's closed-form level-1 tube floor
is 18% too light because one implementation omits the classical 0.605 factor. None has a complete
geometry, closing load path, proved joints, orderable tube set, and complete mass budget.

## Reproduction gates and conventions

- `python3 tools/scale_study.py` exited 0. All 14 rows printed `ok`; the last line was
  `=> reproduces the published article`.
- `python3 tools/subdivision_study.py` exited 0. All six rows printed `ok`; the last line was
  `=> consistent with the model`.
- `make check` exited 2 at `stampcheck`: 42 site files are not stamped at hash `d451d384`.
  It did not reach `assemblycheck`. I did not run `make stamp` because this audit may change no
  other file.
- `make assemblycheck`, run separately because the aggregate gate could not reach it, exited 0
  after 134.7 s with: `NOT PROVEN — 5 of 16 proofs fail (5 frozen in KNOWN, 0 new), 11 pass`.
- The checked-in assembly result is 11/16 proofs passing. Standing failures are P5, P11, P13,
  P14, and P16. Exit 0 from that frozen-baseline checker would mean no regression, not strength.
- The requested `./scripts/test.sh` invocation exited 127: that path does not exist in this
  repository. It therefore cannot be a gate here. The repository-defined gates are the two
  studies and `make check` above.
- Pressure-derived axial demands below already contain SF = 1.5. Service bending stress is
  multiplied by 1.5 exactly once before interaction. Capacities are not divided by a second SF.
- Repository-tool numbers are named as such. Every other number below is an **independent audit
  derivation**, with substitutions shown; it is not a newly settled model figure.

---

# 1. Findings that make the article UNSAFE

## U1 — CRITICAL: tube-to-joint adequacy is not proved; the node is not mass-only overhead

**What the model says.** `NODE_MASS_FRAC = 0.15` describes nodes as carrying no load but weighing.
`stockBuild` replaces that mass estimate with the measured 0.465 kg, but it still publishes no
joint margin. The separate assembly certificate does evaluate nine scalar paths over 432 ends;
P16's raw checked-in census reports 2,296 `FAIL` verdicts among 3,888 rows. These are
heterogeneous, overlapping screens:
bearing uses a tensile-strength stand-in, bond uses an unsourced 10 MPa line, and all 432
press-fit rows are explicitly attributed to “the measurement, not the part.” They establish that
adequacy is not proved, not that 2,296 distinct interfaces have physically failed.

| path | checked-in census |
|---|---:|
| axial bearing | FAIL 432/432 |
| bond shear | FAIL 356, PASS 76 |
| dry pull-out | FAIL 332, UNPROVEN 100 |
| spigot direct | FAIL 432/432 |
| spigot bending | FAIL 216, NO DEMAND 216 |
| transverse shear | FAIL 72, UNPROVEN 144, NO DEMAND 216 |
| press fit | FAIL 432/432 |
| local spigot buckling | FAIL 24, PASS 408 |
| printability | PASS 432/432 |

**What I computed.** At the largest article demand, 5,037.7 N, even the weakest printed
direction's tensile strength, 47 MPa, used optimistically as a bearing allowable, requires

`A_req = F/σ = 5,037.7 N / (47 N/mm²) = 107.2 mm²`.

At the requested 7 kN bound it requires 148.9 mm². The checker records 8.615–28.274 mm², but its
field probe samples the global 10×8 annulus even for 14×12 rim records. Using each end's own SKU
and wrap, the analytic annulus range is 12.419–28.274 mm². P16 applies that direct-seat screen to
all ends, but the geometry does not: only 100 tree ends butt on a dry seat, and their raw P16
margins are 0.2582–0.7704, all below one. The other 332 are closing ends shortened at both ends;
all 72 rim ends are in this class. The worst rim's hypothetical contacted seat is
`A=π(14²-12²)×0.30409/4 = 12.419 mm²`; at its interpolated 69.5 MPa stand-in this gives
863.1 N against 4,476.6 N, margin 0.1928. But each closing rim cut is 0.60 mm short, or 0.30 mm
per end, and the generator specifies that space as an adhesive-filled butt. The 0.1928 figure is
therefore a sensitivity for a contact condition that the rim does not have, not its capacity.
Adhesive compression and creep are **NOT COMPUTABLE — no criterion or test**. Even for the 100
tree ends, tensile strength is not a measured bearing allowable.

For the repository's unsourced adhesive line `τ = 10 MPa`, the 5,037.7 N member needs total
wetted area `F/τ = 503.8 mm²`; 7 kN needs 700 mm². Recomputing each generated end with its own
tube SKU gives areas of 49.7–581.2 mm². Expressed
as engagement on one 10 mm circumference,
`L_req = F/(τπD) = 5,037.7/(10π10) = 16.0 mm` (22.3 mm at 7 kN). If the 8 mm spigot and
10 mm cup surfaces both develop load uniformly, `L_req = 5,037.7/[10π(8+10)] = 8.91 mm`
(12.38 mm at 7 kN). Closing ends have only a 2 mm pilot and partial wraps reach 0.304.

The worst rim end is also evidence of a checker defect: its stored 34.392 mm² area was computed
with the global 10×8 dimensions even though that record carries a 14×12 rim tube. Under the
checker's two-surface convention, the corrected area is
`π(12+14)×2×0.30409 = 49.677 mm²`; `10×49.677 = 496.8 N`, margin
`496.8/4,476.6 = 0.1110`. Recomputing all ends with their own SKU leaves the 356 bond-screen
failures unchanged. The same global-SKU probe defect affects the recorded 10.912 mm² spigot
section. With the rim spigot's `r_o=12/2-0.15=5.85 mm`, `r_i=5.85-2=3.85 mm`, and wrap 0.30409,
the analytic section is `π(5.85²-3.85²)×0.30409 = 18.533 mm²`; even the 69.5 MPa tensile
stand-in gives only 1,288.1 N, margin 0.2877. Repeating that annular screen for all ends still
leaves 432/432 direct failures.

The defect also contaminates rim pull-out, transverse-shear, bending, and local-section values,
so a complete corrected P16 census requires a per-arm field-probe rerun. A nominal-annulus
sensitivity with the checker's deliberately optimistic 92 MPa uniform-shear ceiling gives
`18.533×92/1,745.4 = 0.977` at wrap 0.30409 and
`21.207×92/1,745.4 = 1.118` at wrap 0.34796. Neither is a corrected verdict: P16 measures the
smooth-blended SDF root at `base+0.25 engagement`, and the nominal annulus is not proved to bound
that section. All 72 corrected rim transverse-shear rows are therefore `UNPROVEN` until the
per-SKU field probe is rerun. It would be false precision to rewrite the raw census analytically.

**Delta.** For a contacted seat, required/available area is 3.79 at the best 28.274 mm² analytic
section and 8.63 at the worst 12.419 mm² section for 5,037.7 N; the 7 kN audit band raises those
ratios to 5.27 and 11.99. That comparison applies physically only to the 100 tree ends; the 332
closing ends require an adhesive-butt compression/creep check that does not exist. The favourable
SKU correction raises the hypothetical worst rim bearing sensitivity by 44% and its direct
section margin by 70%, but neither reaches unity. No combined bearing eccentricity, adhesive
peel, or `N-V-M` interaction is checked.

**Effect on float target.** Unsafe, not merely heavy: no density may be credited as a viable
article until the interface is demonstrated by a licensed combined criterion and tests. Failure
of alternative dry, bond, bearing, and section screens is not proof that every possible complete
interface fails; it is proof that this repository has not established one that holds. The
current-geometry adhesive fill is counted in the mass ledger below; any joint reinforcement found
necessary is **NOT COMPUTABLE — missing geometry and allowables**, so every route remains a mass
floor.

## U2 — CRITICAL: film-to-frame load assignment is an envelope, not a closing load path

**What the model says.** It separates infinite-array hydrostatic crush from standalone-cell film
load. It intentionally gives the full indeterminate in-plane pull to both radial and hoop paths.
P12 then says every member end has a demand, while also reporting a maximum node residual of
8,079.5 N and only 9/51 nodes balanced.

**What I computed.** For the 709.000 mm assembly object,

`a = S/(2√2) = 0.709/(2√2) = 0.250669 m`,
`V = S³/2 = 0.178200 m³`,
`A_hex = 3√3 a²/2 = 0.163250 m²`,
`A_sq = a² = 0.0628351 m²`.

At 101,325 Pa, one hexagon carries 16,541.4 N and one square 6,366.77 N. The scalar surface
load is
`p(8A_hex+6A_sq) = 101,325×1.683014 = 170,531 N`; its vector sum over the closed polyhedron is
zero, so node forces—not a scalar total—must close.

The factored face partitions do close locally before the member envelope is applied:

- Hexagon: hub `1.5H/3 = 8,270.68 N`; six vertices each `1.5H/9 = 2,756.89 N`;
  `8,270.68 + 6×2,756.89 = 24,812.0 N = 1.5H`.
- Square: centre `1.5Q/3 = 3,183.38 N`; four vertices each
  `1.5Q/6 = 1,591.69 N`; their sum is 9,550.15 N = `1.5Q`.
- At a hex hub, three props at 54.7356° need
  `F = 8,270.68/[3 cos(54.7356°)] = 4,775.08 N`, matching the tool.
- At a square centre, four 45° octet entries need
  `F = 3,183.38/[4 cos45°] = 1,125.45 N`, not the 3,376.49 N infinite-array crush envelope.

The octet envelope itself is correct for the infinite lattice:
`F = 3p SF V/(96a) = 3×101,325×1.5×0.178200/(96×0.250669) = 3,376.49 N`.
The 96 is three FCC strut-lengths per half-pitch cube times 32 such cubes; it is not the 216
article-member count and must not become 144.

The film membrane calculation also reproduces the family demands. With hex triangular-panel
inradius `r=a/(2√3)=0.0723620 m`, `h=0.25r`,
`R=(r²+h²)/(2h)=0.153769 m`, `T=pR/2=7,790.34 N/m`, and
`q=T√[1-(r/R)²]=6,873.83 N/m`. Hence the factored spoke demand is
`1.5(√3/2)qa = 2,238.32 N`; the two-hex-ring rim is 4,476.63 N. The 5,037.67 N figure belongs
to the in-plane square tie, **not the spoke**. Tripod and inward ties are 4,775.08 N.

**Delta.** All six family magnitudes reproduce, but they cannot be superposed as a single
equilibrium state: array crush requires neighbouring continuation that the standalone article
does not have, and the radial/hoop envelope counts an indeterminate pull twice for sizing. That
explains conservatism; it does not turn the 8.080 kN residual into a reaction.

**Effect on float target.** The individual demands are useful upper envelopes, but they cannot
prove load-path closure or support an article/route verdict. A global stiffness/equilibrium solve
with actual boundary and neighbouring-cell conditions is required; its mass delta is not
computable yet.

## U3 — HIGH: end restraint and system stability are not proved

**What the model says.** `stockBuild` reports both pinned `K=1.0` and socketed `K=0.65` for the
10×8 octet (margins 1.82 and 4.32), while its primary family margins use pinned values. The
printed socket is described as fixity bonus. P13 independently says 216/216 moment-loaded ends
cannot license the clamped bending row.

**What I computed.** With `E=135 GPa`,
`I_10 = π(10⁴-8⁴)/64 = 289.812 mm⁴` and
`I_14 = π(14⁴-12⁴)/64 = 867.865 mm⁴`. Using centre-to-centre lengths (the joints remain part of
the column), Euler gives:

| family | `L` (mm) | factored demand (N) | `Pcr`, K=1 (N) | margin K=1 | margin K=.65 | margin K=2 sensitivity |
|---|---:|---:|---:|---:|---:|---:|
| octet 10×8 | 250.669 | 3,376.49 | 6,145.36 | 1.820 | 4.308 | 0.455 |
| spoke 10×8 | 250.669 | 2,238.32 | 6,145.36 | 2.746 | 6.498 | 0.686 |
| rim 14×12 | 250.669 | 4,476.63 | 18,402.8 | 4.111 | 9.730 | 1.028 |
| tripod/inward tie 10×8 | 177.250 | 4,775.08 | 12,290.7 | 2.574 | 6.092 | 0.643 |
| in-plane tie 10×8 | 177.250 | 5,037.67 | 12,290.7 | 2.440 | 5.775 | 0.610 |

These are `Pcr=π²EI/(KL)²`; therefore changing 1.0 to 0.65 multiplies capacity by
`1/0.65² = 2.367`, while the arbitrary `K=2` sensitivity quarters it. `K=2` is not a derived
mode of this frame; it is shown only to expose the factor-of-four consequence if the effective
length were twice the member length. The physical
tube cuts (141.883–222.029 mm) are shorter than node spacing, but using them as Euler length
would silently assume the printed ends supply both lateral and rotational continuity—the very
property at issue.

**Delta.** No moment–rotation stiffness, system eigenvalue, or no-sway restraint is measured.
`K=.65` is therefore unlicensed, and even `K=1` is conditional. The repository cannot turn the
`K=2` sensitivity column into a physical failure verdict without a global stability model.

**Effect on float target.** Unsafe until system restraint is demonstrated. Crediting socket
fixity could under-size Euler-controlled route tubes by a factor up to 2.367 in capacity; the
corresponding mass change needs a new qualified-section sweep and is not computable here.

## U4 — HIGH: axial compression, film bending, and beam-column amplification are simultaneous

**What the model says.** It reports Euler and film-bending margins in separate columns. At
article A it gives pinned bending margins 1.89 rim, 1.68 spoke, and 3.31 square tie, with Euler
margins 4.11, 2.75, and 2.44 respectively.

**What I computed.** Section moduli are
`Z_10 = I/(D/2) = 57.9624 mm³` and `Z_14 = 123.981 mm³`. For a pin-ended beam-column under
uniform line load, use the elastic magnifier
`B_UDL=8/(βL)²[sec(βL/2)-1]`, where `βL=π√(P/Pcr)`, then combine
`σ = P_fact/A + 1.5 B M_service/Z`. This applies SF exactly once to both pressure actions:

| family | service bend (MPa) | axial factored (MPa) | `B` | combined (MPa) | 2.5 GPa material margin |
|---|---:|---:|---:|---:|---:|
| rim 14×12 | 882.1 | 109.6 | 1.331 | 1,870 | 1.34 |
| spoke 10×8 | 993.5 | 79.2 | 1.590 | 2,448 | **1.02** |
| square tie 10×8 | 504.0 | 178.2 | 1.715 | 1,475 | 1.70 |

For the spoke, `P/Pcr=2,238.3/6,145.4=0.3642`, `βL=1.8960`,
`B_UDL=8/1.8960²[sec(1.8960/2)-1]=1.5897`, and
`79.2 + 1.5×1.5897×993.5 = 2,448 MPa`.
This is a screening interaction, not a substitute for a nonlinear frame solve; its purpose is
to show that independent green columns do not establish combined adequacy.

The assembly joint check also conflates a member maximum with a joint-end demand. Its clamped-row
`wL²/12=72.9 N·m` is a beam maximum, while P13 says the socket cannot license clamped behaviour.
For the ideal simply supported case, the joint end moment is zero, end shear is
`wL/2 = 13,924×0.250669/2 = 1,745.4 N`, and the tube midspan maximum is
`wL²/8 = 109.4 N·m`. A real semi-rigid socket lies between ideal boundary cases; its end moment
cannot be inferred without moment–rotation stiffness.

**Delta.** The tube's governing spoke margin falls from 1.68 bending-only to 1.02 combined; the
rim falls from 1.89 to 1.34. The joint check's 72.9 N·m cannot be called either a licensed end
moment or the simply supported tube maximum; actual joint moment is unquantified.

**Effect on float target.** Article A has essentially no quantified spoke reserve beyond the
nominal SF, before imperfections and real laminate allowables. Route optimizers that preserve
separate margins do not preserve combined margin and are unsafe as selection gates.

## U5 — HIGH: film sag and the loaded shape are assumed, not compatible with the flat net

**What the model says.** It fixes `h/r=0.25`, giving 4.12% membrane strain, line loads, film
gauge, and 8.6% volume loss. HANDOFF says the preformed loaded-dome cutting geometry is still
open; a flat film would craze an inorganic barrier on first pump-down.

**What I computed.** For a spherical cap, meridional arc length from centre to boundary is
`s=R asin(r/R)` while the flat radius is `r`; with `R/r=2.125`, the geometric strain is
`s/r-1 = 2.125 asin(1/2.125)-1 = 0.04116`, or 4.116%, reproducing the repository's 4.12%.
The model's own working strain is only 0.27–0.40%. Thus a flat net
cannot reach the assumed shape elastically.

At the assumed shape, the model's volume rule gives
`ΔV = 8A_hex(0.25r_hex)/2 + 6A_sq(0.25r_sq)/2 = 0.0152731 m³`, where
`r_sq=a/(2+√2)`. That is 8.5708% of the 0.178200 m³ nominal volume, leaving 0.162927 m³.

**Delta.** Until a preformed net fixes sag/slack, `T`, `w`, film gauge, barrier strain, and
displacement all move together. The 8.57% displacement debit alone multiplies kg/m³ by
`1/(1-0.085708)=1.0937`.

**Effect on float target.** Unsafe for sealing and optimistic for lift. The base mass ledger
uses the stated shape only as a transparent scenario; it cannot be a qualified flight BOM.

---

# 2. Findings that make the numbers OPTIMISTIC (plus the loud favourable corrections)

## O1 — HIGH: `0.605` is omitted from the closed-form local-buckling routes

**What the model says.** `K_LOCAL=0.3` is described as a fraction of the classical
`0.605Et/R` stress, and `ORTHO_PENALTY=0.5699`. But `tubeStrut`, `ladder`, and the assembly
spigot expression use `0.3 E_eff t/R`; `subdivision_study.py` correctly uses
`0.605×0.3×E_eff t/R`. `scale_study.py` does not check local wall buckling at all.

**What I computed.** For a buckling-governed level-1 closed-form tube, its formula makes
relative density proportional to `K_LOCAL^(-1/3)`. Treating 0.3 as the knockdown on the
classical coefficient therefore changes density by
`[0.3/(0.605×0.3)]^(1/3) = 1.18236`.
The published M60J lattice line becomes `0.943×1.18236 = 1.115 kg/m³`; with 15% nodes and
0.02379 kg/m³ outer film, `1.115×1.15+0.02379 = 1.306 kg/m³`, not 1.108.

At level 2 (`α=4/3`) the factor is
`[sqrt(0.3/(0.605×0.3))]^(1/α) = 1.20737`; the 0.3706 kg/m³ lattice becomes 0.4475 and the
same node/film convention totals 0.5384 kg/m³ instead of 0.4499. It remains below the wall only
as an abstract bound with asserted nodes, not an article.

The same omitted coefficient changes P16's own local-spigot screen. Applying `0.605` to the
checked-in margins leaves all 360 non-rim ends above one but changes the raw rim result from 24
to 72 failures: 48 ends at wrap 0.34796 move from `1.3282` to
`1.3282×0.605 = 0.8036`, while the 24 already-failing ends at wrap 0.30409 move from `0.9107`
to `0.5510`. These are formula corrections to P16's stored field sections, not a substitute for
the per-SKU field-probe rerun U1 requires.

For stock 10×8 and 14×12 tubes, `R/t` is only 4.5 and 6.5 at the wall midsurface, so a
thin-shell equation is not validated. For orientation only, the corrected stresses are
`0.605×0.3×0.5699×135 GPa×1/4.5 = 3.103 GPa` and 2.148 GPa; using outer radii gives 2.793
and 1.995 GPa. The range itself shows why thin-shell radius convention is not harmless here.
NASA's current SP-8007 is a design guideline for buckling-critical thin-walled cylinders, and
NASA separately warns that general composite shells are outside the original scope and require
care ([NASA SP-8007 Rev. 2](https://ntrs.nasa.gov/citations/20205011530),
[NESC composite-cylinder bulletin](https://ntrs.nasa.gov/citations/20240000391)). No actual SKU
layup, laminate `A/B/D` data, imperfection survey, or coupon result is in the repository.

**Delta.** Level-1 closed-form structure is 18.2% heavier and level 2 is 20.7% heavier under the
model's stated interpretation; P16's raw local-buckling failure count rises by 48, from 24 to 72.
The study and assembly paths disagree with the subdivision path; this is not a defensible choice
of `K=0.3`.

**Effect on float target.** R4's claim that the M60J tube floor moves from 2.1× to about 1.0×
does not survive: the corrected bare lattice is 1.165× the wall before joints and film. R1 rows
already include 0.605, but remain floors for other reasons.

## O2 — HIGH: combined bending/local-shell buckling at the recommended 1 m rim is unquantified

**What the model says.** FLOAT Appendix A selects a 16×14 main and 24×22 rim at 1 m, claiming
all current margins are preserved and explicitly noting that local wall buckling is not checked.

**What I computed.** At 1 m, the 24×22 rim has `A=72.2566 mm²`, service bending stress
769.23 MPa, factored axial demand 8,905.52 N or 123.25 MPa, and Euler margin 5.73. The same
uniform-load magnifier gives `βL=π√(1/5.73)=1.3125`, `B_UDL=1.2175`, and combined
stress `123.25 + 1.5×1.2175×769.23 = 1,528 MPa`.
Corrected uniform-axial local stress is 1,164 MPa using outer radius or 1,214 MPa at the
midsurface. The corresponding *axial-only* margin is
`σcr/σaxial = (1,164 to 1,214)/123.25 = 9.44–9.85`. Comparing that cylinder stress directly with
the 1,528 MPa maximum-fibre screen would give a ratio 0.762–0.795, but that is not a licensed shell-interaction
criterion and must not be reported as a local-buckling margin. It instead exposes the missing
combined bending/local-shell check at a stress scale large enough to matter.

**Delta.** The advertised parity section passes the implemented axial-only local screen by
9.44–9.85, but neither the model nor this audit can turn separate axial and bending columns into a
combined shell margin. The omitted interaction is therefore unquantified, not a demonstrated
20–24% failure.

**Effect on float target.** The 15.38 kg/m³ Appendix A point and any `~9.3 kg/m³` optimization
using the same unchecked interaction remain provisional. The sign and mass delta are not
computable without a licensed combined-load shell criterion and real products.

## O3 — HIGH: the incomplete mass ledger makes every density an optimistic floor

**What the model says.** Article A is 2.390 kg tube + 0.465 kg SDF-integrated nodes + 0.028 kg
flat-area film = 2.883 kg. Bond adhesive, seam construction, a real multilayer barrier, permanent
fasteners, retained jig overlength, dome area, and process waste are absent. FLOAT's definition of
done nevertheless requires a gated, complete BOM including tube, joints, film, barrier, and seams.

**What I computed.** The detailed ledger below closes the existing node and film lines, then
quantifies 21.6/95.3/202.9 g of low/base/high allowances. It still cannot bound joint changes,
adhesive peel and environmental knockdowns, the evacuation port, repair material, manufacturing
fallout, or inter-cell hardware because no designs exist.

**Delta.** The provisional base scenario is 0.272 kg lighter than the 2.883 kg stock figure before
loaded-volume correction and 0.18 kg/m³ lower after it, but neither sign nor magnitude is complete:
the excluded unknowns are unbounded. This is an acceptance blocker, not a bookkeeping footnote.

**Effect on float target.** No §1 or §3 number is a complete-BOM density. The quantified scenario
cannot support a float verdict while material required by an adequate interface, sealing, service,
and assembly architecture remains undesigned.

## O4 — MEDIUM: loaded displacement and assembly packing are absent from §3 densities

**What the model says.** `stockBuild.kgPerM3` and the §3 studies divide by nominal Kelvin volume.
`filmEdgeLoads` separately reports 8.6% spoked and 21.8% unbraced bulge loss. R1 assumes even-n
cells share a continuous lattice, but no assembled outer-envelope pitch, packing gap, or
inter-cell joint BOM exists.

**What I computed.** For standalone article A, the explicit derivation in U5 gives
0.162927 m³ loaded displacement rather than 0.178200 m³. Every standalone density is therefore
9.37% higher. That debit must **not** be copied to an internal array partition with vacuum on
both sides; for an array, displaced volume is the exterior union and needs an outer-hull control
volume.

**Delta.** +9.37% for this standalone loaded-shape scenario; unknown for R1–R4 assembled hulls.

**Effect on float target.** All route last-column numbers are unsupported as buoyancy figures
until their exterior control volumes and inter-cell masses exist.

## O5 — MEDIUM: §1's 9.3 table is not reproduced by either named tool and uses an invented catalogue

**What the model says.** FLOAT says every figure is computed by the two self-checking tools and
calls §1's sections “real thin-wall tube.” The same document's R3 section says the catalogue is
invented. `scale_study.py` contains 25 hand-enumerated OD/ID pairs; `subdivision_study.py`
generates ODs in 0.5 mm steps and walls from a plausible list, explicitly awaiting
`tube-catalogue.json`.

**What I computed.** Running both tools reproduces their self-checks and printed sweep tables,
but neither prints FLOAT §1's 0.71/1/2/3 m rows (9.31, 9.34, 9.05, 8.65 kg/m³). No
`research/data/tube-catalogue.json` exists. `scale_study.py` also evaluates the spoke with
`propped=True`, although the report says that midspan prop is priced and not built.

**Delta.** The quoted table cannot be traced to its claimed current tool output, its products
are not orderable evidence, and at least one support condition is absent from generated geometry.

**Effect on float target.** The “current ~9.3” baseline and reductions measured from it are not
gated article numbers. Use 16.21 kg/m³ only for `stockBuild`'s nominal-volume coupon, and label
the optimized rows as unverified floors.

## O6 — FAVOURABLE, LOUD: R1's mixed allocation is pessimistic for a bulk array

**What the model says.** `subdivision_study.py` prices tube with the infinite-array convention
`96n³` but joints with all 201/1,289 nodes of a standalone even-`n` Kelvin boundary. Those are
different control volumes. The graph contains 948/6,840 physical struts at `n=2/4`, whereas the
shared allocation uses 768/6,144 strut-lengths.

**What I computed.** A bulk octet lattice has 12 strut ends per node, so the node allocation
consistent with `96n³` shared struts is `2(96n³)/12 = 16n³`: 128 nodes at `n=2` and 1,024 at
`n=4`. Keeping the study's own equal-mass-per-node law gives, for its highlighted 4 m `n=2` row,

`ρ = 2.51645 + 1.62491(128/201) + 0.07942 = 3.63063 kg/m³ = 3.79×` the wall,

not 4.22077 kg/m³ or 4.41×. At the advertised best `n=4` row,

`ρ = 1.93354 + 1.91263(1024/1289) + 0.03971 = 3.49268 kg/m³ = 3.65×`,

not 3.88589 kg/m³ or 4.06×. Conversely, a standalone allocation must charge all physical struts
and all boundary nodes; that yields 4.81056 kg/m³ (5.03×) at the same `n=2` row and 4.10492 kg/m³
(4.29×) at `n=4`. Neither object is what the mixed tool row reports.

**Delta.** On the bulk object R1 is **0.59014 kg/m³ lighter at `n=2` and 0.39321 kg/m³ lighter
at `n=4`** than reported. This is the largest verified movement in §3's favourable direction.
The result still inherits the tool's asserted equal node mass and omits inter-cell joint geometry.

**Effect on float target.** Say this louder: the corrected bulk floor is 3.65× rather than 4.06×
at the best row. It still does not float, and it is not a verified article, but the prior table is
pessimistic for the control volume R1 actually intends.

## O7 — FAVOURABLE, LOUD: actual tube cuts remove 0.367 kg from article A

**What the model says.** `stockBuild` bills 108+36 long members at 250.669 mm and 72 short
members at 177.250 mm: 48.8 m and 2.390 kg of tube.

**What I computed.** Using assembly P14's six generated seat-to-seat cut rows and
`m=ρ(π/4)(D²-d²)Ln`, with `ρ=1,600 kg/m³`:

| row | cut × count | mass (kg) |
|---|---:|---:|
| octet 10×8 | 222.029 mm × 12 | 0.12053 |
| octet 10×8 | 217.903 mm × 48 | 0.47317 |
| rim 14×12 | 212.702 mm × 36 | 0.50037 |
| spoke 10×8 | 215.302 mm × 48 | 0.46752 |
| tie 10×8 | 144.484 mm × 24 | 0.15687 |
| tie 10×8 | 141.883 mm × 48 | 0.30809 |
| **seat-to-seat total** | **41.393 m** | **2.02655** |

The manifest also says every closing member is cut shorter at both ends for swing clearance.
There are 42 closing octets and 48 closing spokes at 0.15 mm relief per end, 36 closing rims at
0.30 mm, and 40 closing ties at 0.25 mm. The additional reduction is
`2(42×0.15+48×0.15+36×0.30+40×0.25)=68.6 mm`; applying each SKU's line mass gives 0.00354 kg.
Actual scheduled tube is therefore 41.3249 m and 2.02302 kg.

**Delta.** `2.02302-2.390 = -0.36698 kg`, or `-0.36698/0.178200 = -2.0594 kg/m³` at nominal
volume. This is the audit's largest verified movement in the favourable direction.

**Effect on float target.** Article A is lighter, loudly. The correction is object-specific and
cannot be applied to R1–R4, whose cuts and joints differ. It also does not license using the
short physical cuts as Euler spans; the printed load-transfer regions replace the removed tube.

## Detailed not-yet-counted mass ledger supporting O3

**What the model says.** Article A is 2.390 kg tube + 0.465 kg SDF-integrated nodes + 0.028 kg
flat-area film = 2.883 kg. Bond adhesive, seam construction, a real multilayer barrier, permanent
fasteners, retained jig overlength, dome area, and process waste are not in that total.

**What I computed.** The 51 generated node records sum to 438,468 mm³. At the generator's
`ρ_print=1,060 kg/m³`, node mass is
`438,468×10⁻⁹×1,060 = 0.464776 kg` (the individually rounded `massG` fields sum to 0.46481 kg).
This is geometric integration, not a weighed assembly.

The base film line also closes independently. From U2,
`A_hex=0.163250 m²`, `A_sq=0.0628351 m²`, with panel radii
`r_hex=0.0723620 m`, `r_sq=0.0734194 m` and `R=2.125r`. At effective film stress
`(5.8 GPa/4)×0.5=725 MPa`, areal masses are
`μ_hex=1,560×101,325×0.153769/(2×725e6)=0.0167627 kg/m²` and
`μ_sq=1,560×101,325×0.156016/(2×725e6)=0.0170076 kg/m²`. Thus
`m_film=8×0.163250×0.0167627+6×0.0628351×0.0170076=0.0283041 kg`.

The following is a transparent estimate, not a qualified BOM. Low/base/high are deliberately
shown so an omitted line cannot masquerade as zero.

| not-yet-counted line | derivation | low / base / high (g) |
|---|---|---:|
| tube-to-node adhesive, current geometry | per-SKU two-surface area `Σπ[ID·engagement + OD·min(2.5,engagement)]·wrap = 77,685 mm²`; bondline 0.1/0.2/0.3 mm, density 1.1/1.2/1.3 mg/mm³, waste 1.0/1.25/1.5 | 8.5 / 23.3 / 45.4 |
| closing-end adhesive butt fill | 332 ends; supported gap volume `Σ[π(OD²-ID²)/4]·wrap·swingRelief = 1,334.55 mm³`; density and waste as above | 1.47 / 2.00 / 2.60 |
| wet fin-seam adhesive | 5.766 m × width 5/10/15 mm × thickness 0.1/0.2/0.3 mm × density above × waste 1.0/1.25/1.5 | 3.2 / 17.3 / 50.6 |
| deposited barrier stack | 1.683 m² × 0.27 g/m² for 100 nm Al; base/high use the repository note's 2/5 g/m² deposited stack | 0.45 / 3.37 / 8.42 |
| permanent fastener allowance | no fastener is designed; scenario is 0/1/2 M2×12 mm Ti pins per 216 members, `m=216π(1 mm)²(12 mm)(4.43 mg/mm³)` | 0 / 36.1 / 72.1 |
| retained jig overlength | 0.5/1/2 mm on 180 10×8 and 36 14×12 cuts at 45.24/65.35 g/m | 5.25 / 10.50 / 20.99 |
| dome surface above flat area | spherical-cap area ratio `1+(h/r)²=1.0625`; 6.25% of 28.304 g at stated sag | 1.77 / 1.77 / 1.77* |
| film fin/trim allowance | 5.766 m × 10 mm × `(28.304 g/1.683 m²)` | 0.97 / 0.97 / 0.97* |
| **provisional budgeting subtotal** | sum | **21.6 / 95.3 / 202.9 g*** |

`*` The high film/trim value is not truly bounded because sag, net, and production yield are
unfixed. The current-geometry adhesive line is the material that fits the generated cups, not the
164,259 mm² required if every end independently developed its demand at the unsourced 10 MPa
screen; fitting that area requires a redesign whose additional node/tube mass is unknown. The
fastener and jig lines are explicit allowances, not generated parts. Any joint reinforcement
found necessary after licensed criteria and tests,
adhesive peel capacity, a valve/evacuation port, leak-test repair, and inter-cell hardware are
**NOT COMPUTABLE — missing designs** and sit outside the subtotal.

The brief also names seam tape. The settled architecture rejects tape as the vacuum seal, so it
must not be double-counted with wet fin adhesive. As a mutually exclusive rejected comparison,
25 mm × 50 µm tape at 950 kg/m³ over 5.766 m would weigh
`5.766×0.025×0.00005×950 = 0.00685 kg`.

For sensitivity only, combining the actual 2.02302 kg cut tube, 0.464776 kg nodes, 0.028304 kg
base film, and each provisional allowance column gives:

| scenario | mass (kg) | nominal kg/m³ | loaded-shape kg/m³ | × 0.9569 wall |
|---|---:|---:|---:|---:|
| low | 2.538 | 14.24 | 15.58 | 16.28 |
| base | 2.611 | 14.65 | **16.03** | **16.75** |
| high quantified only | 2.719 | 15.26 | 16.69 | 17.44 |

**Delta.** Against the 2.883 kg stock figure, the base budgeting scenario is 0.272 kg lighter
before the loaded-volume correction; after it, density is 0.18 kg/m³ lower. The rows mix existing
material with contingent process allowances, so they are not a coherent qualified BOM; unbounded
items prohibit a complete total.

**Effect on float target.** The cut correction helps, but “a mass line not modelled is not zero”
holds. No complete-BOM or float verdict is permitted from this subtotal.

---

# 3. Findings that are MERELY UNSTATED

## S1 — LOW: units close, but object identity and duplicated demand constants do not

**What the model says.** Published analysis uses the unrounded 708.5395 mm model span; generated
assembly uses 709.000 mm. The same nominal 3,372 N demand is also stored as a generator parameter,
while assembly recomputes 3,376.49 N from its actual span.

**What I computed.** Crush scales as span squared, so
`(0.709/0.7085395)²-1 = 0.001300`, a 0.130% increase; `3,372.10×1.001300 = 3,376.49 N`.
All audited pressure, Euler, film, section, and mass equations are dimensionally consistent when
SI inputs are used. The scale tool reproduces 14 rounded figures and the subdivision tool six
identities. The discrepancy is provenance, not dimensional algebra.

**Delta.** 4.38 N on the octet demand, correctly conservative in assembly. There is no gate that
proves the typed generator `demand_n=3372` follows either live derivation.

**Effect on float target.** Negligible mass effect, but every result must retain its object/span.
The larger document inconsistency is material: FLOAT's 9.3 table is not emitted by its named tools
and cannot be called currently reproduced.

## S2 — LOW: `K_LOCAL=0.3` is not a material qualification

**What the model says.** The constant is “mildly conservative” for an isotropic wall and the
orthotropy penalty analytically optimizes a 75% axial / 25% hoop `[0/90]` split. The stock SKU is
described instead as `[0/±45/90]` T700-class without supplier evidence.

**What I computed.** `ORTHO_PENALTY=0.75^0.75×0.25^0.25=0.56988` is arithmetically correct for
the stated optimization. It does not establish the laminate stiffnesses, coupling, compressive
allowables, wall waviness, or socket damage of a purchased roll-wrapped tube. At stock `R/t`
the thin-shell relation is outside its natural asymptotic regime; at the closed-form `R/t=75.5`
the geometry is thin but the laminate and imperfection data remain absent.

**Delta.** Not computable as a single replacement knockdown. The verified code error is O1;
material qualification is a separate missing input.

**Effect on float target.** Every “buyable tube” and R3/R4 density remains provisional until tied
to a named SKU and tested/process-specific properties.

---

## Not-yet-counted list

The provisional quantified subtotal is **21.6 / 95.3 / 202.9 g low/base/high** for article A:
current-geometry tube-to-node side adhesive, closing-end adhesive butt fill, wet fin-seam adhesive,
deposited barrier, a provisional fastener allowance, jig overlength, dome surface, and film
fin/trim. Seam tape is a 6.85 g rejected
alternative, not additive. These scenario columns satisfy the requirement to make omitted lines
visible; they are not a qualified BOM. Unbounded and therefore excluded are any joint
reinforcement found necessary after licensed bearing/pull-out/bending/shear criteria and tests,
adhesive peel and environmental knockdowns, the evacuation
port/valve, leak-test repair material, manufacturing fallout, and all inter-cell/outer-envelope
hardware. A quantified subtotal plus unbounded unknowns is the honest result; there is no complete
mass total yet.

## Verdict on FLOAT.md §3's route table

**The table does not survive as a set of float-capable article configurations.** R1 survives only
as a directional hypothesis: its tool correctly includes the 0.605 local-buckling coefficient,
but prices 96n³ shared struts alongside standalone node counts. A consistent bulk allocation makes
its best row **3.65×, lighter than the stated 4.06×**, while a consistent standalone allocation is
4.29×; neither includes generalized film bending, generated high-valence joints, load-path
closure, real tube SKUs, loaded exterior displacement, or complete assembly mass. R2 is an
aspiration until a
load-carrying joint is designed—the present joint emits failing scalar screens before interaction,
while several capacities remain stand-ins or bounds.
R3 is necessary but has no catalogue. R4's direction survives, but its level-1 M60J floor rises
from 0.943 to 1.115 kg/m³ when the model's own stated classical factor is applied; level 2 remains
an abstract 0.538 kg/m³ bound, not an article. Consequently §3's last column may be retained only
if relabelled **unverified lower bounds/directional hypotheses**. No route, alone or combined,
currently meets the definition of done at 0.9569 kg/m³.
