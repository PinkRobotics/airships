# Status against today’s model

**Disposition: LAND IN PART — retain the conditional regime finding, not a qualified material winner.**
Replaying the report's axial sleeve formulas at its 0.709 m object reproduces sleeve plus
adhesive masses: Ti **0.215142 kg**, Al **0.213315 kg**, 316L **0.368662 kg**. The updated
15%-of-tube allowance is **0.2922 kg**, so Ti and Al leave only **0.077058 kg** and
**0.078885 kg** for every omitted central, shear, vent and assembly part. At the report's
supplier-route 1 mm wall, Al is **0.264624 kg**, leaving **0.027576 kg**, replacing the old
**0.0939 kg** headroom. Ti and 316L exceed this updated allowance before those omitted parts.
These replay the old assumptions; no structure is newly designed or qualified.

The current contacted-root and nominal-seat screens reproduce **0.352924** and **0.278624**
against the report's assumed allowable. The weakest tied representative is now `n06.a07`;
this is a scalar screen, not the physical governing failure load. The 51-STL triangle sum
still gives **1,395,120 triangles / 502,337.66 mm²**. It does not measure outgassing.
The assembly file records 12/16 proofs passing, read without rerunning the prover.
Supplier pages, process limits and outgassing references remain dated citations, not refreshed
procurement or test evidence. The missing global load case and moment–rotation data still
prevent a complete material winner in this report.

**Reproduction:** the displayed formulas in §§2–5, using current `member_demands(0.709)`,
`stock_build()`, `assembly.json` end fields and the manifest's binary STLs. The complete
read-only replay command is retained in the order's hand-up.

## Dated audit record

The text below records what was claimed on its audit date. “Today” in that text means that date. Only the reproductions above are current; historical numbers and review-era paths are preserved as evidence, not revalidated claims. See [the float ledger](../FLOAT-LEDGER.md).

---

# The metal joint: regime and material audit

**Date:** 2026-08-12

**Scope:** findings only; no model, generator, manifest, study, margin or frozen baseline changed

**Object for every unqualified figure:** article A, square-face span 0.709 m, subdivision
`n=1`, volume `0.709³/2 = 0.178200 m³`, 51 nodes, 216 members and 432 member-ends.

## Answer first

**Today's PAHT-CF connector demonstrably fails the strength screen (A), but its actual A-versus-C
governing regime is NOT COMPUTABLE.** That is a failure-screen verdict, not a qualification. On
the physically contacted tree ends, compression bypasses the side bond and reaches the printed
seat/root. The weakest live contacted end is a tripod/inward tie at 4.775 kN and 47.058 MPa
direction-aware tensile allowable: it needs 101.47 mm² at a 35.814 mm² root, and its 28.274 mm²
seat sees 168.88 MPa. The corresponding optimistic screen margins are 0.353 and 0.279. Strength
therefore fails a known compression path, but that does not establish which failure occurs first.

That does **not** prove the operator's expected C regime false for either the current joint or a
redesign. It proves only that the current joint already fails a known A screen. The 332 closing
ends do not contact a dry seat: their
0.15–0.35 mm end gaps are adhesive-filled. Their compression/creep and load sharing between
the butt and side lap have no allowable or stiffness model. Applying the whole compressive
member force to `F/(τπD)` would invent a tensile load path. It is retained below as an explicit
full-reversal/coupon-sizing sensitivity, not mislabelled as the article's vacuum capacity.
Since that unknown C path could fail below the known A screen, the present article cannot
honestly be named A-governed or C-governed from available evidence.

**For a deliberately pin-ended, axial-`N`-only resized socket, bond length controls the three
metal sleeve sensitivities, but the real redesigned regime remains NOT COMPUTABLE.** At the supplied low allowables
`[TO VERIFY]`, an axial 5.038 kN square-tie sleeve needs only 0.175 mm Ti, 0.654 mm AlSi10Mg or
0.344 mm 316L wall, while a conservative one-surface epoxy lap at 20 MPa needs 8.018 mm length.
The provisional process walls are thicker than those axial-strength walls. Thus bond length is
the remaining dimension in the `N`-only sensitivity for the three metals, but a one-piece
8.018 mm closing socket cannot be
assembled through the proved 2 mm pilot. A split/post-assembly sleeve or a different assembly
scheme is mandatory. Simultaneous transverse shear already invalidates a universal C verdict for
the displayed walls, and its unmodelled mass prevents a complete winner.

**B does not select a material for the model's primary tube sizing.** The live family Euler
margins use pinned `K=1`; `K=0.65` is printed only as an unlicensed socket bonus. There is no
required hub stiffness to “license” a fixity that the primary sizing does not use. A monolithic
hub will nevertheless attract an unknown moment. Without a global stability solution and a
measured/calculated `M–θ` curve, its actual bending wall is not computable. The ideal zero- and
fixed-end rows below are sensitivities, not a bound on the compressed frame.

**Printed metal is favored over unisolated printed nylon on current months-hold evidence, but no
complete metal node is yet proved to meet R2.** The relevant qualification difference is vacuum
compatibility, not raw density. The 51 current nylon STLs give a nominal post-bake outgassing
screen 2.6–35× over the proposed decade-average pressure-rise budget, and saturated PAHT-CF can
carry water equal to 47% of that whole budget. Unisolated nylon is not presently qualified and
its admissibility is NOT COMPUTABLE until a production bake plus integrated rate-of-rise test
closes the evidence gap. Vented SLM metal removes the nylon-water
reservoir and the virtual-leak argument, although trapped powder and rough internal surfaces
remain real risks.

No complete candidate is proved below the R2 line. The corrected current node set is
**0.715 kg total = 14.02 g/joint = 4.012 kg/m³ = 29.9% of the model's 2.390 kg tube line**.
The target is 0.3585 kg. Under the cited supplier's 1.0 mm general wall minimum, the axial-`N`-only
metal **socket-plus-adhesive sensitivities** are 0.2646 kg for AlSi10Mg, 0.4228 kg for Ti and
0.7437 kg for 316L. Only Al stays under the target, leaving 0.0939 kg, or 1.84 g per node, for the
entire omitted transverse/root, 7–12-arm central load path, vents and assembly solution. Because the family
envelopes do not form an equilibrated per-node load case, that central mass is **NOT
COMPUTABLE**. “Best achievable” is consequently not a number; the best useful result is this
necessary headroom test.

---

## 1. Provenance and corrections

| input | status and use |
|---|---|
| `docs/FLOAT.md`, live manifest/contract and study outputs | repository evidence for article A |
| reviewed physics audit, Git object `49f901b…` | U1/U2/U3/U4 and missing-mass findings; old geometry values are historical |
| reviewed previous joint audit, Git object `1a61377…` | survey and corrected R2 basis; this report builds on it rather than repeating it |
| operator material/process values in the work order | `[TO VERIFY]`; low strength and high density are used where a range is supplied |
| supplier capabilities | `[TO VERIFY]` until the actual 51 STEP files receive DfM approval and a quote |
| hand calculations below | **AUDIT DERIVATION — NOT IN THE TOOLS**; every substitution is shown |

The requested supply-market primer was absent from this checkout, the supplied review path and
reachable Git history. No claim is attributed to it. Current supplier pages are cited directly.

The corrected mass object matters. `0.715/0.465 = 1.537634`, so any old 0.465-based joint column
scales by 1.54. The article subtotal is 3.13 kg and `3.13/0.178200 = 17.56 kg/m³`, about the
published 17.6. The old “19.5% measured” statement was `0.465/2.390`; after the correction it is
`0.715/2.390 = 29.916%`. Here 0.715 kg is the **51-joint set**, not one joint.

The geometry also moved. The current sunken-frame contract reports `wrapFrac=1.0` for all 432
ends: 100 tree ends at 20 mm engagement and 332 closing ends at 2 mm, including all 72 rim ends.
The older 0.304/0.348 wraps belong to the partial-socket geometry and are not mixed into this
article. P16 still repeats global 10×8 interface areas on rim records, so this audit recomputes
the 14×12 rows with their own SKU.

## 2. Interface requirement by member family

### 2.1 Factored axial envelopes

The repository's `member_demands(0.709)` values already contain `SF=1.5`; no second factor is
applied. They are conservative family envelopes, not a simultaneous equilibrated node load set.

| family | factored axial magnitude | end population |
|---|---:|---:|
| octet | 3,376.49 N | 36 tree + 84 closing |
| spoke | 2,238.32 N | 96 closing |
| rim, 14×12 | 4,476.63 N | 72 closing |
| tripod prop + inward vertex tie | 4,775.08 N | 40 tree + 56 closing |
| in-plane square tie | **5,037.67 N** | 24 tree + 24 closing |
| separate survey ceiling | 7,000 N | sensitivity, not an article family |

The 5,037.67 N demand belongs to the in-plane square tie, not the spoke.

### 2.2 Axial fitting section: A screen

**AUDIT DERIVATION.** `A_req=F/σ_allow`. Low supplied yield/tensile values are used:
Ti 900 MPa, Al 230 MPa, 316L 450 MPa, PA12-CF 60 MPa and CFF 800 MPa along fibre, all
`[TO VERIFY]`. The PAHT-CF column applies the repository-catalogued Bambu Z tensile value 47 MPa
to every family as a conservative orientation-independent redesign bound, rather than claiming
that every live arm is printed in Z. The live-current comparison in §3.1 instead uses the
direction-aware allowable for each actual end. CFF values are aligned-fibre sensitivities only.

| family | Ti, mm² | Al, mm² | 316L, mm² | PA12-CF, mm² | PAHT-CF Z, mm² | CFF aligned, mm² |
|---|---:|---:|---:|---:|---:|---:|
| octet: `3376.49/σ` | 3.75 | 14.68 | 7.50 | 56.27 | 71.84 | 4.22 |
| spoke: `2238.32/σ` | 2.49 | 9.73 | 4.97 | 37.31 | 47.62 | 2.80 |
| rim: `4476.63/σ` | 4.97 | 19.46 | 9.95 | 74.61 | 95.25 | 5.60 |
| tripod/inward: `4775.08/σ` | 5.31 | 20.76 | 10.61 | 79.58 | 101.60 | 5.97 |
| square tie: `5037.67/σ` | 5.60 | 21.90 | 11.19 | 83.96 | **107.18** | 6.30 |
| 7 kN sensitivity: `7000/σ` | 7.78 | 30.43 | 15.56 | 116.67 | 148.94 | 8.75 |

The live main spigot/root section is 35.814 mm². At 47 MPa its optimistic direct capacity is
`35.814×47 = 1,683 N`, only `1,683/5,037.67 = 0.334` for the square-tie screen. P16's
direction-aware field result is correspondingly below one; a tensile number is still not a
qualified bearing/compression allowable.

### 2.3 Seat bearing and closing butt

**AUDIT DERIVATION.** Full-wrap dry-seat area is
`A_seat=π(OD²-ID²)/4`. Thus main `A_seat=π(10²-8²)/4=28.274 mm²` and rim
`A_seat=π(14²-12²)/4=40.841 mm²`. Required average bearing pressure is `p=F/A_seat`.

| family | substitution | average pressure |
|---|---|---:|
| octet | `3376.49/28.274` | 119.42 MPa |
| spoke | `2238.32/28.274` | 79.16 MPa |
| rim, own 14×12 SKU | `4476.63/40.841` | 109.61 MPa |
| tripod/inward tie | `4775.08/28.274` | 168.88 MPa |
| in-plane square tie | `5037.67/28.274` | **178.17 MPa** |
| 7 kN on main tube | `7000/28.274` | 247.57 MPa |

These pressures physically apply to the 100 contacted tree ends. No tube-end bearing allowable
or printed-material bearing allowable is qualified; 47 MPa is only an optimistic tensile
stand-in. The 332 closing ends have no dry seat. Their corresponding annulus is an adhesive butt
across a 0.15/0.20/0.25/0.35 mm per-end relief. Compression modulus, sustained compression/creep,
peel and butt-versus-side-lap stiffness sharing are absent. Closing compression capacity is
therefore **NOT COMPUTABLE**, not the dry-seat number above.

### 2.4 Dry pull-out

The article's uniform vacuum envelope is compressive. A pull-out requirement needs a defined
tensile handling, asymmetric evacuation or reversal load; none exists. Even if `F_tension=F`
is imposed as an audit sensitivity, friction gives

`N_normal,req = F_tension/μ`,

not a length. Engagement length affects pull-out only through interference/contact pressure and
its distribution, which are unmeasured. At the deliberately impossible optimistic bound `μ=1`,
the required normal force is simply 2.238–5.038 kN by family (7 kN at the survey ceiling).

P16's live geometry expresses the same upper bound as required `μ=F/capacity(μ=1)`:

| family/end class | live required `μ` range | disposition |
|---|---:|---|
| octet tree / closing | 0.257–0.345 / **2.570–3.451** | tree unproved; closing fails upper bound |
| spoke closing | **1.704–2.264** | fails upper bound |
| rim closing | **2.242–2.968** | fails upper bound |
| tripod/inward tree / closing | 0.363–0.711 / **3.635–7.106** | tree unproved; closing fails upper bound |
| square tie tree / closing | 0.384 / **3.835** | tree unproved; closing fails upper bound |

Dry pull-out engagement is therefore **NOT COMPUTABLE** and dry capture cannot retain any closing
end at the full family load. A bond or positive post-assembly capture is required if that tensile
case is adopted.

### 2.5 Bond shear: C sensitivity

The vacuum load is compression, so this is explicitly a full-reversal/coupon-sizing sensitivity.
It does not replace the missing closing-butt compression/creep model. At the low supplied epoxy
lap value `τ=20 MPa [TO VERIFY]`:

`A_bond,req=F_tension/τ`,

`L_outer=F_tension/(τπOD)`, and

`L_two=F_tension/[τπ(OD+ID)]`.

`L_two` assumes inner and outer bondlines reach the same allowable together despite different
adherend stiffness; it is not credited as a design without a shear-lag/load-sharing model.

| family | `A_req=F/20` | conservative external-sleeve `L_outer` | two-surface sensitivity `L_two` |
|---|---:|---:|---:|
| octet | 168.82 mm² | `3376.49/(20π10)=5.374 mm` | `3376.49/[20π(10+8)]=2.985 mm` |
| spoke | 111.92 mm² | `2238.32/(20π10)=3.562 mm` | 1.979 mm |
| rim, own 14×12 SKU | 223.83 mm² | `4476.63/(20π14)=5.089 mm` | `4476.63/[20π(14+12)]=2.740 mm` |
| tripod/inward tie | 238.75 mm² | `4775.08/(20π10)=7.600 mm` | 4.222 mm |
| square tie | 251.88 mm² | `5037.67/(20π10)=8.018 mm` | 4.454 mm |
| 7 kN, main | 350.00 mm² | `7000/(20π10)=11.141 mm` | 6.189 mm |

Sensitivity is exactly inverse in allowable: `L(τ)=L(20)(20/τ)`, so 40 MPa halves every length.
Average shear is only a coupon-sizing relation: real qualification must include bondline thickness,
surface preparation, overlap-end shear peaks, peel, sustained load, moisture and tube-wall
splitting.

All 332 closing ends are limited by assembly to a 2 mm pilot. Even the smallest conservative
one-surface output above is 3.562 mm. A one-piece lengthened socket is therefore not buildable in
the proved sequence. It needs a counted split sleeve/clamshell, injected feature, positive pin or
new assembly order.

The requested hoop wall cannot be derived from axial lap shear alone. Uniform longitudinal bond
shear loads the sleeve in axial membrane; hoop tension requires radial contact pressure or peel,
neither of which the model supplies. The parameterized thin-ring requirement is

`t_hoop(p)=pD/(2σ_hoop)`.

For a 10 mm socket this is `p×{0.00556, 0.02174, 0.01111, 0.08333, 0.10638, 0.00625}` mm per
MPa of radial pressure for Ti, Al, 316L, PA12-CF, PAHT-CF-Z and aligned CFF respectively; the
14 mm rim coefficients are 1.4× larger. Example: at an assumed 10 MPa uniform radial pressure,
Al needs `10(10)/(2·230)=0.217 mm`. These are `[TO VERIFY]` sensitivities, not additions to the
wall schedule: discrete overlap-end peel causes ring bending/stress concentration that this
membrane equation does not capture. Until `p(x)` or a tested peel criterion exists, the
hoop/peel wall and every mass subtotal remain incomplete lower bounds.

### 2.6 Unlicensed end bending

`film_edge_loads(0.709)` supplies service line load `w`. The following applies SF=1.5 exactly
once:

`V_end,SF=1.5wL/2`,

`M_mid,pinned,SF=1.5wL²/8`, and

`|M_end,fixed,SF|=1.5wL²/12`.

| family | full substitution | factored end shear | pinned member maximum | fixed-end sensitivity |
|---|---|---:|---:|---:|
| octet | no film-edge row | 0 from this load set | 0 | 0 |
| spoke | `w=7332 N/m`, `L=0.250669 m` | `1.5(7332)(.250669)/2=1,379 N` | 86.4 N·m | **57.6 N·m** |
| rim | `w=13924 N/m`, `L=0.250669 m` | `1.5(13924)(.250669)/2=2,618 N` | 164.1 N·m | **109.4 N·m** |
| tripod/inward tie | no film-edge row | 0 from this load set | 0 | 0 |
| square tie | `w=7439 N/m`, `L=0.177250 m` | `1.5(7439)(.177250)/2=989 N` | 43.8 N·m | **29.2 N·m** |

The pinned maximum is at midspan, not at the joint. For the requested isolated-member
boundary-condition band, each loaded joint has `0 ≤ |M_end| ≤ 1.5wL²/12`: spoke 0–57.6 N·m,
rim 0–109.4 N·m and square tie 0–29.2 N·m; octet and tripod/inward tie receive no moment from
this film-edge load set. This pinned-to-fixed band is an interface sizing requirement, but it is
not a rigorous bound for a compressed, translating global frame. U4's
beam-column screen already moved the spoke tube from a 1.68 bending-only margin to 1.02 combined.
Actual joint `M`, combined `N-V-M`, sway and effective length remain **NOT COMPUTABLE** without a
global solve and `M–θ` evidence.

## 3. Regime determination

### 3.1 Current PAHT-CF geometry

The known screens line up as follows. The weakest live contacted end is tripod/inward
`n01.a09`; the square tie is shown separately because it carries the largest family force:

| candidate regime | arithmetic | result |
|---|---|---|
| A, weakest live root | `A_req=4775.08/47.058=101.47 mm²`; live root 35.814 mm² | actual direction-aware screen ratio `35.814/101.47=0.353`; below one |
| A, weakest live contacted seat | `p=4775.08/28.274=168.88 MPa`; stand-in 47.058 MPa | actual direction-aware screen ratio `47.058/168.88=0.279`; below one |
| A, largest-load square-tie check | `σ=5037.67/35.814=140.66 MPa`; its live allowable is 91.984 MPa | actual direction-aware root ratio `91.984/140.66=0.654`; below one, but not the weakest live end |
| C, closing adhesive | square-tie side-lap full-reversal average `τ=5037.67/113.097=44.54 MPa`; butt compression/creep missing | two-surface side-lap exceeds 20 MPa sensitivity, but actual compressive sharing and failure load are not computable |
| B, fixity | primary Euler calculation uses `K=1`; no `kθ`, `M–θ` or global mode | no stiffness requirement selects material; monolithic bending remains unlicensed |

**Verdict: the current joint demonstrably fails A, but the current A-versus-C governor is NOT
COMPUTABLE.** C may fail first at the closing ends, but the article has no calculation that turns
its compressive force into the side-lap shear used in that comparison or qualifies the adhesive
butt. B is not a licensed credit or a sized requirement. A known A failure excludes an adequate
joint; it does not rank an unknown C failure load.

### 3.2 Resized axial/pin-ended socket

For a thin external sleeve with inner radius `r=OD/2`, axial section is

`A=π[(r+t)²-r²]`, hence

`t_strength=sqrt(r²+F/(πσ))-r`.

At the 10 mm square tie this gives:

- Ti: `sqrt(5²+5037.67/(π·900))-5 = 0.175 mm`;
- Al: `sqrt(5²+5037.67/(π·230))-5 = 0.654 mm`;
- 316L: `sqrt(5²+5037.67/(π·450))-5 = 0.344 mm`;
- PA12-CF: `sqrt(5²+5037.67/(π·60))-5 = 2.192 mm`;
- PAHT-CF Z: `sqrt(5²+5037.67/(π·47))-5 = 2.689 mm`; and
- CFF aligned: `sqrt(5²+5037.67/(π·800))-5 = 0.197 mm`.

For all three metals, the provisional process wall is thicker than `t_strength`, while the
conservative 8.018 mm external bond length remains required by the stated axial 20 MPa
sensitivity. This does **not** prove C for the real interface because `V` and transverse/root
criteria remain. For example, the rim's Al 0.8 mm annulus has
`A=π(7.8²-7²)=37.196 mm²`; the conservative thin-annulus screen
`τ_peak≈2V/A=2(2618)/37.196=140.77 MPa` and
`σ_vm=sqrt[(4476.63/37.196)²+3(140.77)²]=271.9 MPa`, above the supplied 230 MPa yield.
Thus the redesigned A/B/C regime is **NOT COMPUTABLE** until combined `N-V(-M)`, transverse/root
and peel criteria are supplied. PA12-CF and PAHT-CF are coupled **A+C** in the `N`-only screen because material
strength sets 1.1–2.7 mm family walls while bond length sets overlap. CFF would also cross to C
only where continuous fibre actually follows each arm; the central multi-arm path is unresolved.

For the fixed-end sensitivity, axial and bending stress are simultaneous. This audit solves the
thick annulus, not `max(t_N,t_M)`:

`σ_max(t)=F/{π[(r+t)²-r²]} + 1000M(r+t)/{(π/4)[(r+t)⁴-r⁴]} ≤ σ_allow`,

with `M` in N·m and every length in mm.

The family wall schedules below use the larger of that solution and the process wall. They still
omit transverse/root interaction and do not license the fixed case.

The familiar material indices explain the conditional ranking but do not choose the regime. At
the conservative values used here, `σ/ρ` is 0.203 Ti, 0.086 Al, 0.056 316L, 0.055 PA12-CF and
0.044 PAHT-CF-Z MPa/(kg/m³); aligned CFF is 0.571 but has no multi-arm path. `E/ρ` is 0.0248 Ti,
0.0262 Al and 0.0238 316L GPa/(kg/m³), versus 0.0027 PA12-CF and 0.0021 PAHT-CF-Z. The
operator's higher PAHT indices use in-plane estimates; they cannot be assigned to arms crossing
layers. Hence Ti and Al are effectively tied in specific stiffness, Ti leads ordinary candidates
in specific strength, and neither observation proves whether A, B or C is active.

## 4. Sized mass comparison

### 4.1 Material inputs and wall outputs

| candidate | density | modulus | strength used | process wall used for low-mass screen | mechanical regime |
|---|---:|---:|---:|---:|---|
| Ti6Al4V, stress-relieved SLM | 4,430 kg/m³ | 110 GPa | 900 MPa yield | 0.5 mm `[TO VERIFY]`; cited PCBWay route says 1.0 mm | C; process/assembly realized |
| AlSi10Mg SLM | 2,670 kg/m³ | 70 GPa | 230 MPa yield | 0.8 mm `[TO VERIFY]`; PCBWay 1.0 mm | C; process/assembly realized |
| 316L SLM | 8,000 kg/m³ | 190 GPa | 450 MPa yield | 0.5 mm `[TO VERIFY]`; PCBWay 1.0 mm | C; process/assembly realized |
| PA12-CF MJF/SLS | 1,100 kg/m³ | 3 GPa | 60 MPa tensile | 0.8 mm `[TO VERIFY]`; strength is thicker | A+C; strength/assembly realized |
| PAHT-CF FDM | 1,060 kg/m³ | 2.18 GPa Z / 3.86 GPa XY TDS | **47 MPa Z** | live measured 1.44 mm; strength is thicker | A+C; strength/assembly realized |
| continuous-fibre print | 1,400 kg/m³ | not supplied across path | 800 MPa along fibre only | 1.0 mm scenario `[TO VERIFY]` | aligned sensitivity only; central path not manufacturable as shown |

All values in this table are operator-supplied `[TO VERIFY]` except the direction-aware PAHT-CF
TDS values already catalogued in the repository. Using the operator's isotropic 6–8 GPa PAHT
estimate in every arm would ignore the exact Z-direction defect the work order requires.

Each sequence is `octet / spoke / rim / tripod-inward / square tie`, in millimetres:

| candidate | axial-only wall schedule | ideal fixed-end sensitivity schedule |
|---|---|---|
| Ti | 0.500 / 0.500 / 0.500 / 0.500 / 0.500 | 0.500 / 0.818 / 0.846 / 0.500 / 0.558 |
| Al | 0.800 / 0.800 / 0.800 / 0.800 / 0.800 | 0.800 / 2.577 / 2.804 / 0.800 / 1.881 |
| 316L | 0.500 / 0.500 / 0.500 / 0.500 / 0.500 | 0.500 / 1.506 / 1.592 / 0.500 / 1.056 |
| PA12-CF | 1.551 / 1.072 / 1.529 / 2.095 / 2.192 | 1.551 / 6.287 / 7.277 / 2.095 / 5.056 |
| PAHT-CF Z | 1.919 / 1.440 / 1.906 / 2.572 / 2.689 | 1.919 / 7.227 / 8.444 / 2.572 / 5.910 |
| CFF aligned sensitivity | 1.000 / 1.000 / 1.000 / 1.000 / 1.000 | 1.000 / 1.000 / 1.000 / 1.000 / 1.000 |

**Complete wall-solve ledger (AUDIT DERIVATION — NOT IN THE TOOLS).** In family order
`O/S/R/P/Q`, substitute

`N={3376.49,2238.32,4476.63,4775.08,5037.67} N`,

`r={5,5,7,5,5} mm`, and

`M={0,57.6,109.4,0,29.2} N·m`

into

`t_N=max[t_process,sqrt(r²+N/(πσ))-r]`

and

`t_NM=max[t_process, positive root of N/{π[(r+t)²-r²]} + 1000M(r+t)/{(π/4)[(r+t)⁴-r⁴]}=σ]`.

The full material substitutions and their evaluated `t_N ; t_NM` vectors (mm) are:

- Ti `(σ,t_process)=(900,0.500)`: `0.500/0.500/0.500/0.500/0.500 ; 0.500/0.818/0.846/0.500/0.558`;
- Al `(230,0.800)`: `0.800/0.800/0.800/0.800/0.800 ; 0.800/2.577/2.804/0.800/1.881`;
- 316L `(450,0.500)`: `0.500/0.500/0.500/0.500/0.500 ; 0.500/1.506/1.592/0.500/1.056`;
- PA12-CF `(60,0.800)`: `1.551/1.072/1.529/2.095/2.192 ; 1.551/6.287/7.277/2.095/5.056`;
- PAHT-CF Z bound `(47,1.440)`: `1.919/1.440/1.906/2.572/2.689 ; 1.919/7.227/8.444/2.572/5.910`; and
- aligned CFF `(800,1.000)`: `1.000/1.000/1.000/1.000/1.000 ; 1.000/1.000/1.000/1.000/1.000`.

Thus every displayed wall is reproducible from a shown `N,r,M,σ,t_process` substitution; the
rounding is applied only after solving.

The large polymer fixed sensitivities are a useful falsification of “bulk material barely
matters”: if the monolithic hub attracts anything near the ideal fixed moment, polymer is plainly
strength-driven and metal wins by section. Only an actual pin or `M–θ` solve can choose a point
between these sensitivities.

### 4.2 Socket-only mass lower bounds

The mass object is 432 conservative external sleeves, one per actual end, at each family's
`L_outer` and wall above. It is deliberately simple and reproducible:

`m_socket=Σ n_i ρ π[(D_i/2+t_i)²-(D_i/2)²]L_i·10⁻⁹` kg.

Example, axial Ti octets:

`m=120(4430)π[(5+0.5)²-5²](5.37385)10⁻⁹ = 0.0471 kg`.

Every other row uses the same displayed family counts, lengths, wall schedule and density. Bond
area for all 432 full-reversal sleeves is

`Σn_iF_i/20 = 82,129.51 mm²`.

At a 0.20 mm bondline, 1.20 mg/mm³ cured density and 1.25 application factor `[TO VERIFY]`,

`m_adh=82129.51(0.20)(1.20)(1.25)/10⁶ = 0.02464 kg`.

| candidate | explicit socket length output | axial socket kg/article | socket kg/joint | socket kg/m³ | fixed socket kg/article | socket + adhesive kg/article | combined kg/joint | combined kg/m³ | remaining to R2 line |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Ti | family 3.562–8.018 mm | 0.1905 | 0.00374 | 1.069 | 0.2382 | **0.2151** | **0.00422** | **1.207** | **0.1434 kg** |
| Al | same, `L∝20/τ` | 0.1887 | 0.00370 | 1.059 | 0.4095 | **0.2133** | **0.00418** | **1.197** | **0.1452 kg** |
| 316L | same | 0.3440 | 0.00675 | 1.931 | 0.6718 | 0.3687 | 0.00723 | 2.069 | **−0.0102 kg** |
| PA12-CF | same | 0.1834 | 0.00360 | 1.029 | 0.5221 | 0.2081 | 0.00408 | 1.168 | 0.1504 kg |
| PAHT-CF | same | 0.2272 | 0.00445 | 1.275 | 0.6212 | 0.2518 | 0.00494 | 1.413 | 0.1067 kg |
| CFF aligned sensitivity | same | 0.1258 | 0.00247 | 0.706 | 0.1258 | 0.1505 | 0.00295 | 0.844 | 0.2080 kg |

**Complete sleeve-mass ledger (AUDIT DERIVATION — NOT IN THE TOOLS).** In the same `O/S/R/P/Q`
order, use `n={120,96,72,96,48}`, `D={10,10,14,10,10} mm`, and
`L={5.37385,3.56240,5.08913,7.59978,8.01770} mm` in the displayed summation. The five family
terms and total (kg/article) are:

| candidate | axial family terms and total | fixed-band-upper-end family terms and total |
|---|---|---|
| Ti | `0.04712+0.02499+0.03697+0.05331+0.02812=0.19050` | `0.04712+0.04211+0.06408+0.05331+0.03155=0.23816` |
| Al | `0.04673+0.02478+0.03639+0.05287+0.02789=0.18868` | `0.04673+0.09298+0.14480+0.05287+0.07214=0.40953` |
| 316L | `0.08509+0.04512+0.06677+0.09627+0.05078=0.34402` | `0.08509+0.14897+0.22857+0.09627+0.11293=0.67183` |
| PA12-CF | `0.03992+0.01403+0.03007+0.06387+0.03554=0.18344` | `0.03992+0.12102+0.19607+0.06387+0.10125=0.52213` |
| PAHT-CF | `0.04911+0.01876+0.03699+0.07857+0.04372=0.22716` | `0.04911+0.14178+0.23124+0.07857+0.12052=0.62122` |
| CFF | `0.03120+0.01655+0.02417+0.03530+0.01862=0.12583` | same `=0.12583` |

Division by 51 and by `0.178200 m³` produces the per-joint and kg/m³ columns; adding
`m_adh=0.02464 kg` produces the socket-plus-adhesive column. The last column is
`0.3585-(m_socket+m_adh)`.

These are **axial-`N`-only lower-bound sensitivities, not mechanically sized complete joints**.
They exclude simultaneous transverse shear (which already fails the displayed 0.8 mm Al rim
screen), the central 7–12-arm redistribution body, overlap
subtraction, the split/post-assembly mechanism required at 332 ends, vents/bosses, peel/root
reinforcement and post-processing mass. The unequilibrated family envelopes cannot size the
central body. Adding an arbitrary “core allowance” would violate the rule that an unmodelled mass
line is not zero.

Sensitivity is explicit. With the displayed wall schedule unchanged,
`m_socket(τ,ρ)=m_socket(20,ρ_table)(20/τ)(ρ/ρ_table)` and the displayed adhesive mass also scales
as `20/τ`. Strength-wall rows must instead recompute
`t=sqrt[r²+F/(πσ)]-r`; they do not scale linearly with `σ`. At the high supplied 40 MPa adhesive
line, all bond lengths and these sleeve/adhesive subtotals halve. No strength or vacuum conclusion
is upgraded by that unqualified sensitivity.

For scale, retaining today's solid SDF volume and merely swapping density gives
`m=0.715(ρ/1060)`: 2.99 kg Ti, 1.80 kg Al, 5.40 kg 316L, 0.742 kg PA12-CF and 0.944 kg CFF.
That is not a design either; it shows why metal wins only if it is genuinely hollow and vented.

### 4.3 R2 verdict

R2 permits `0.15(2.390)=0.3585 kg`, or `2.012 kg/m³`, across all 51 complete nodes. Today's
corrected set is 0.715 kg, 29.9% of tube mass; reaching R2 needs
`1-0.3585/0.715=49.86%` reduction.

- **No candidate is proved to reach 15%.** Complete mass is not computable from the available
  load envelopes.
- Al and Ti have the lowest provisional axial-`N`-only socket-plus-adhesive sensitivities, essentially tied
  at 0.213–0.215 kg. Aluminium is lower at the selected process walls because both are
  process-limited and its density is lower; this is not a specific-strength result.
- The axial Ti line leaves 143.4 g and Al 145.2 g for all central/assembly/vent mass, about
  2.81–2.85 g per node. Passing that necessary test would still require the missing load case and
  proof.
- At the ideal fixed-end sensitivity, Ti socket plus adhesive is 0.2628 kg and retains 95.7 g of
  headroom; Al is already 0.4342 kg and misses R2 before a core. Thus a stiffness/moment result can
  reverse the metal ranking: Ti wins strength-driven bending, Al wins process-limited axial mass.
- CFF has the lowest numerical arm-shell lower bound, but no supplied process can place continuous
  fibre through a 3-D 7–12-arm node. It is not an orderable complete candidate.

At the cited PCBWay 1.0 mm general minimum, the same axial-only calculation gives Ti/Al/316L
socket-plus-adhesive totals `0.4228/0.2646/0.7437 kg`, respectively; per joint
`8.29/5.19/14.58 g`, and `2.373/1.485/4.173 kg/m³`. Only Al retains R2 headroom, 93.9 g, before
the omitted shear/root/core/assembly lines. These are supplier-route sensitivities, still not
qualified designs.

Accordingly the **best achievable complete number is NOT COMPUTABLE**. The best actionable
supplier-route number is the approximately 93.9 g central-system budget left by the 1.0 mm Al
axial-only sensitivity; even that wall fails the report's completeness requirement until combined
loading is sized.

## 5. Vacuum admissibility

### 5.1 Nylon screen

Direct integration of all 1,395,120 triangles in the 51 live STLs gives 502,337.66 mm² =
0.502338 m² nominal surface. It includes areas later covered by tubes/adhesive and excludes
internal pore/road area, so it is a geometric screen rather than a rigorous exposure bound.
This is the explicit triangle sum
`A=Σ 0.5‖(b-a)×(c-a)‖` over `research/geometry/nodes/*.stl`. It reproduces without a mesh
library by reading each binary STL's 80-byte header, little-endian triangle count, then each
50-byte `<12fH` record; summing vertices `q[3:6],q[6:9],q[9:12]` prints
`1395120 502337.66`. This specifies the path, record interpretation and complete area operation,
not an unexplained hand total.

Povilus et al. measured cleaned/baked **SLS PA12**, not FDM PAHT-CF, at
`q=3×10⁻⁸–4×10⁻⁷ mbar·L/(cm²·s)`; cross-process use is `[TO VERIFY]`.

`Q=5023.38 cm²(3×10⁻⁸–4×10⁻⁷)=1.51×10⁻⁴–2.01×10⁻³ mbar·L/s`.

The barrier note proposes, but the project has not adopted, a 10%-atmosphere rise in ten years.
For article A:

`pV_allow=0.10(1013.25 mbar)(178.200 L)=18,056 mbar·L`,

`Q_budget=18056/[10(365.25)(86400)]=5.72×10⁻⁵ mbar·L/s`.

The instantaneous post-bake nylon screen is therefore `1.51e-4/5.72e-5=2.6×` to
`2.01e-3/5.72e-5=35×` the decade-average budget. Desorption decays, so a constant-decade
integration would be false; the production `Q(t)` is absent.

The independent finite water inventory uses the Bambu PAHT-CF TDS's 0.88% saturation at
25 °C/55% RH:

`m_water=0.0088(0.715 kg)=0.006292 kg=6.292 g`,

`n=6.292/18.015=0.3493 mol`,

`pV=nRT=(0.3493)(8.314)(293.15)=851.5 Pa·m³=8515 mbar·L`,

`8515/18056=47.2%` of the entire proposed decade allowance. This reservoir is not added to a
constant outgassing flow; release depends on bake–pump–seal history.

**Verdict:** unisolated PAHT-CF and PA12-CF are not presently qualified for a months-hold cell;
their admissibility is NOT COMPUTABLE from this cross-process instantaneous screen. They can
qualify only if the actual printed/bonded system is vacuum-baked and its
integrated rate-of-rise stays inside the pressure budget remaining after face and seam
permeation. An internal barrier is a different candidate and its mass, seams and process must be
counted. Metal is favored because it removes the known hygroscopic reservoir, but this screen
does not prove nylon intrinsically inadmissible after a qualified bake/pump/seal process.

### 5.2 Vented SLM

A hollow SLM node with deliberate de-powdering passages is open to vessel vacuum and traps no
sealed gas volume. That largely answers FLOAT open question 1 for metal; FDM “sparse infill is a
virtual leak” is the wrong analogy. The residual risks are blocked passages, retained unfused
powder, support remnants, large rough internal area and contaminants. Require borescope/CT or
equivalent inspection and a cleaned-part rate-of-rise test `[TO VERIFY]`. Use part density in the
mass model: approximately 2.67 g/cm³ for AlSi10Mg, not a supplier page's 1.45 g/cm³ loose-powder
density.

## 6. What it takes to order

| candidate | process and wall disposition | orderability / required post-process |
|---|---|---|
| Ti6Al4V | SLM/DMLS; axial 0.5 mm and fixed-band-upper 0.5–0.85 mm sensitivities, but PCBWay states 1.0 mm general minimum `[TO VERIFY]` | stress relief, support removal, de-powder, ream/machine bond datums, clean/passivate as specified, CT/borescope vents, witness coupons |
| AlSi10Mg | SLM; axial 0.8 mm and fixed-band-upper 0.8–2.80 mm sensitivities; PCBWay minimum 1.0 mm `[TO VERIFY]` | heat-treatment state must match 230 MPa input, support removal, de-powder, machine bores; combined shear must be resized |
| 316L | SLM; axial 0.5 mm and fixed-band-upper 0.5–1.59 mm sensitivities; PCBWay minimum 1.0 mm `[TO VERIFY]` | same inspection; density makes even axial socket-plus-adhesive miss R2 |
| PA12-CF | MJF/SLS; axial 1.07–2.19 mm and fixed-band-upper 1.55–7.28 mm sensitivities `[TO VERIFY]` | de-powder, seal/finish if exposed, bake and rate-of-rise; vacuum qualification absent |
| PAHT-CF | FDM; axial 1.44–2.69 mm and fixed-band-upper 1.92–8.44 mm sensitivities | dry/anneal in qualified orientation, machine bond datums, barrier or bake/rate-of-rise; weak Z direction and water require qualification |
| CFF | segmented CFF arms; axial/fixed sensitivity 1.0 mm, but process wall and transverse properties `[TO VERIFY]` | fibre path must be shown arm by arm; a continuous 3-D high-valence core is not established, so complete order is not ready |

PCBWay's current SLM page lists AlSi10Mg, 316L and TC4/Ti, 300 mm build size, 1 mm minimum wall
and ±0.3 mm accuracy `[TO VERIFY]`. Protolabs publishes material/resolution-dependent DMLS walls
below that but also warns about wall aspect ratio and inaccessible powder `[TO VERIFY]`.
HP's MJF guidance gives 0.3 mm XY/0.5 mm Z only for short walls; the structurally calculated PA12
walls are thicker. Sources: [PCBWay SLM](https://www.pcbway.com/rapid-prototyping/3D-Printing/3D-Printing-SLM.html),
[Protolabs DMLS guidance](https://www.protolabs.com/resources/design-for-3d-printing-toolkit/),
[HP MJF guidance](https://www.hp.com/us-en/printers/3d-printers/learning-center/how-to-design-3d-print-model.html),
[Bambu PAHT-CF TDS](https://wiki.bambulab.com/filament-acc/asacf-pahtcf/65f1b18a6d6142d794a1a6a00f1496ef.pdf),
and [Povilus et al.](https://arxiv.org/abs/1308.4962).

The supplier package must contain:

1. one true-solid STEP per node, quantity and revision; STL alone is insufficient for controlled
   bores;
2. a dimensioned drawing with tube OD/ID, bondline, bore, concentricity, runout, datums and
   inspection method; the current 0.15 mm radial clearance is smaller than PCBWay's published
   ±0.3 mm SLM accuracy, so as-printed fit is not orderable without machining `[TO VERIFY]`;
3. material grade, build orientation, heat treatment and property direction;
4. all de-powdering/vent holes shown open to vessel vacuum, minimum passage diameter and forbidden
   support zones;
5. machined bond surfaces, target roughness and cleaning/passivation instructions compatible with
   the selected adhesive;
6. CT/borescope or equivalent retained-powder inspection, dimensional report, density/porosity
   certificate and representative witness coupons `[TO VERIFY]`; and
7. a separate split-sleeve/positive-capture design for 332 closing ends, or a newly proved
   assembly sequence. The present one-piece geometry cannot accept the sized bond length.

CNC is plausible only for separable/open socket modules. A one-piece hollow valence-7–12 node is
not made machinable by choosing metal. Monetary price is **NOT QUOTABLE** until this STEP/drawing
package exists; “priced” in this report is mass-priced in kg/joint and kg/m³.

## 7. Not yet counted

- central load-redistribution body for every 7–12-arm node;
- split sleeves, pins, clamps or injected structure required at 332 closing ends;
- adhesive spew fillets, bondline-control media and closing-end butt fill beyond the displayed
  24.64 g side-lap sensitivity;
- peel/root reinforcement, tube-end splitting prevention and galvanic isolation for metal/CFRP;
- vent rims/bosses, supports, machining stock and any mass retained after post-processing;
- coating or internal barrier on a polymer candidate;
- inspection witness features, repair material and production yield;
- actual combined `N-V-M`, global stability and any mass change needed to produce a physical pin;
- equilibrium-driven central topology, because the family envelopes cannot be superposed at a
  node; and
- adhesive compression, creep, moisture and temperature knockdowns.

None of these is zero. Their absence is why the complete winner and best achievable R2 percentage
remain not computable.

## 8. Reproduction gates

Run before and after writing this audit:

- `python3 tools/scale_study.py`: exit 0; all 14 published-figure self-checks `ok` and
  `=> reproduces the published article`.
- `python3 tools/subdivision_study.py`: exit 0; all six model-identity self-checks `ok` and
  `=> consistent with the model`.
- `make check`: exit 2 at `figfresh` in this environment because `chromium` is absent. Lint and
  both stamp lines passed first; the aggregate gate did not reach assembly. The work order's
  expected `stampcheck` failure was not reproduced and is not rewritten as if it were.
- `make assemblycheck`, run separately: exit 0;
  `NOT PROVEN — 5 of 16 proofs fail (5 frozen in KNOWN, 0 new), 11 pass`, with 2,064 of 3,888
  scalar margins failing. Exit 0 means the frozen bill did not move, not that a joint holds.

The repository has no `./scripts/test.sh`; per the work order it was not substituted with bare
pytest. `make assemblycheck` rewrites path/runtime fields in `assembly.json`; those incidental
changes are restored byte-for-byte. Final `git status` must show this audit as the only changed
path.

## Final disposition

The present connector has not earned a material winner by changing density. It demonstrably fails
the A screen, while its actual A-versus-C governor remains uncomputable. A metal,
axial/pin-ended redesign makes bond length control an `N`-only sleeve sensitivity, but the 2 mm
closing assembly limit and the missing central equilibrium problem then become the real design.
Aluminium wins the provisional axial mass screen; titanium wins once enough moment is
attracted to make specific strength matter. The actual monolithic joint cannot choose between
those rows until `M–θ` and node equilibrium exist.

Order **neither** as a complete 51-node set yet. First produce one equilibrated node load case,
choose physical pin versus monolithic restraint, design the closing-end capture, and quote/test
one Ti and one Al representative with the same 20 MPa bond coupon system. That is the shortest
path from this audit to a defensible order.
