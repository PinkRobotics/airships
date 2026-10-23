# MAINLINE-026b — P3 bay size, discrete frame versus continuum

**QUESTIONABLE.** The rigid-joint linear pressure factor is **5.254644 at
frequency 4** and **2.183661 at frequency 2**, against same-section smeared
values **6.193381 and 6.876245**. These are respectively **15.16% and 68.24%
below** the source continuum predictions. The frequency-6 result inherited
from MAINLINE-026 was 5.51% above its continuum prediction.

The requested linear comparison, pinned counts, mass charge, and open
member-force/rise supplement are complete. The optional new nonlinear runs
produced converged equilibria and tangent zero crossings, but **their first
instability loads are unverified**: selecting only modes nearest zero can
skip an already-negative family. Frequency 4 exhibits this ambiguity.
The raw nonlinear outputs are diagnostic evidence, not accepted limits.

Authority is `ord-admiral-rr2-mainline026b-bays-1020`, with the open
`ord-admiral-rr2-mainline026-continuum-bays-1020` and
`ord-admiral-rr2-mainline026-member-forces-rise-1020` supplements.
Source receipts and verified artifact copies are in [INPUTS.json](32c8b5f76a7daa33-INPUTS.json).
The original MAINLINE-026 package remains frozen.

Same-section continuum comparison [source link unavailable in this public projection]

All factors multiply **p = 95,460.8379139 Pa** on a radius-10 m hull.
E = 410 GPa, density = 3,100 kg/m³ and ν = 0.14 are retained. No empirical
knockdown is applied to either the perfect discrete eigenvalue or the
continuum comparison. Real film, joint and material capability is not
established by this elastic calculation.

| Frequency | Original joints / members | Nominal source bay (m) | Actual mean arc (m) | Tube outer radius / wall (mm) | Continuum λ | Discrete linear λ | Difference |
|---|---:|---:|---:|---:|---:|---:|---:|
| 6, inherited 011b/026 | 362 / 1,080 | 2.04 | 2.001344 | 123.688 / 0.880299 | 6.127640 | 6.465222 | +5.51% |
| 4, 022 section | 162 / 480 | 3.00 | 2.994745 | 136.709 / 1.071849 | 6.193381 | 5.254644 | −15.16% |
| 2, 022b section | 42 / 120 | 6.15 | 5.909464 | 167.646 / 1.625275 | 6.876245 | 2.183661 | −68.24% |

Full precision is in [CASES.json](a9347de2cea46271-CASES.json) and [RESULTS.json](18ef4273eaf5516c-RESULTS.json).
The sections use the exact source-card values behind the rounded order.
The prescribed icosahedral frequencies do not realize exactly uniform
3.00 or 6.15 m members: frequency 4 spans 2.539–3.264 m and frequency 2
spans 5.536–6.283 m.

The register's half-wave/bay ratios are recovered: **1.481, 1.058, 0.571**.
Using the actual mean arc in the continuum denominator instead gives
6.245997, 6.204250 and 7.156132. This does not remove the discrepancy.
The departure is already material at the 3 m case and decisive at the
6 m case. Agreement at the first point does not establish an applicability
threshold: a half-wave spanning only 1.48 members is not a well-separated
continuum scale. Sections and frequency both change across these ordered
points; this is not an isolated frequency-only experiment.

| Case | Segments per curved member | First linear factors |
|---|---|---|
| Frequency 4 | 6 → 12 → 24 | 5.259243 → 5.255473 → **5.254644** |
| Frequency 2 | 12 → 24 → 48 | 2.185423 → 2.184011 → **2.183661** |

The last changes are about −0.0158% and −0.0160%. The finest models have
67,212 and 34,092 physical DOFs. Original joints are fully rigid; six global
motions are removed by orthogonality conditions. The twelve returned modes
and residuals are retained; this does not guarantee a complete census of
degenerate eigenspaces. The first modes are distributed joint/member
deformations. Member-relative motion is appreciable at frequency 4 and
larger than joint motion at frequency 2; the broad automated
`global_lattice` label in raw output should not be read as a continuum mode.

The primary linear method is the validated MAINLINE-026 Hermite
initial-compression stiffness with the conservative pressure Hessian.
It omits initial-moment geometric couplings, shear deformation, tube-wall
failure and real joint compliance. It is a conditional frame eigenvalue.
[METHODS.md](0464535b02194307-METHODS.md) records the equations and implementation.

For freely ball-pinned curved members, the internal mechanism counts are
**1,080, 480 and 120**, respectively, excluding six global rigid motions.
The joint-position rigidity matrices have full rank 3V−6; each curved
member adds an independent roll about its endpoint chord. Finite rolls
leave elastic energy at numerical zero. No positive pinned buckling
factor is assigned. Film and joint anti-roll restraint remain unspecified.

The mass charge uses exact circular member lengths and the source card's
film, systems and joint rules. Frequency 6 has 5% of tube mass for joints
and 50 kg systems; frequencies 4 and 2 have 5% of tubes + film + nodes for
joints and 100 kg systems. Film masses are 97.515, 184.442 and 348.856 kg.
Thus the three total masses are not an optimization at one common
allowance. Gross inherited lift is 4,889.442150 kg.

| Frequency | Tubes (kg) | Joints (kg) | Nodes (kg) | Total before payload (kg) | Carried sag debit (kg) | Remaining payload (kg) |
|---|---:|---:|---:|---:|---:|---:|
| 6 | 4,567.703 | 228.385 | 7.240 | 4,950.843 | 0 | **−61.401** |
| 4 | 4,086.652 | 213.717 | 3.240 | 4,588.051 | 0 | **301.391** |
| 2 | 3,745.247 | 204.747 | 0.840 | 4,399.690 | 187.938 | **301.814** |

Relative to the 022/022b 244.472 kg payload target, the last two headrooms
are 56.919 and 57.342 kg. Frequency 4's source did not charge sag;
zero in the table means **not charged**, not zero physical sag. Frequency
2's sag debit is inherited from 022b, not solved here. The pressure fan
is a load-transfer surface, not a validated film shape or lift volume.
Projection film and joint allowances remain consequential.

The open force supplement uses a paired frequency-6, 12-segment comparison.
At unit pressure, mean member compression is **550.519 kN**, maximum
member-mean compression **588.079 kN**. At all twelve five-valent nodes
the incident member means are **460.622 kN** and endpoint values
**460.638 kN**, to numerical symmetry. Every node and incident member is
listed in RESULTS.

At nominal s = 2.04 m, pRs/(2√3) is **562.166 kN**, while pRs/2 is
**973.701 kN**. At the realized mean arc, the triangular prediction is
551.514 kN, within about 0.18% of the discrete mean. Frequency-4 and
frequency-2 static member means are 822.953 and 1,617.338 kN; their
complete five-valent-node tables are also retained.

The rise variant changes each circular arc's crown rise to eight times
its original sagitta, retaining the spherical joints and frequency-6
section. At 24 segments, mean axial compression is **538.899 kN** and
mean endpoint chord thrust **569.788 kN**. Peak end moment is
**177.825 kN·m**, and the elastic bending-stress extrapolation is
**4.248 GPa**, versus 0.059 GPa in the original m12 frame. The paired
m12 rise case gives 538.923 kN and 4.224 GPa; refinement changes peak
bending by 0.57%.

Holding the original spherical nodal load vector while changing the arc
shape gives mean compression **513.844 kN**, chord thrust **551.204 kN**
and peak bending **4.069 GPa**. Thus neither load convention produces an
eightfold thrust reduction. Rise adds bending and member length; the
rise-8 vehicle mass becomes 5,446.291 kg under the inherited frequency-6
allowances. These excessive elastic stresses are not physical allowables.
This is a controlled variant of 026, not a reproduction of 022's different
s = 1.1 m rise-8 section.

Rise and force comparison [source link unavailable in this public projection]

The optional perfect nonlinear runs converge at both beam resolutions.
Raw reported tangent zeros are 5.155463 → 5.082444 at frequency 4 and
2.230417 → 2.218113 at frequency 2. Their changes are 1.42% and 0.55%.
**Neither new pair is accepted as a verified first-instability limit.**
The nearest-zero solver can select a different triplet after a previous
family becomes negative. In the finer frequency-4 path a near-zero triplet
at λ = 5.059945 is followed by a different positive nearest-zero result
at 5.080744. An independent smallest-algebraic or inertia check is required.
The frequency-2 path has no comparable visible ambiguity, but lacks that
independent check. Both pressure paths are still rising at their reported
zeros; they are not demonstrated pressure maxima or ultimate loads.
The frozen frequency-6 nonlinear result had its own independent check.

Nonlinear diagnostic paths [source link unavailable in this public projection]

[CHECKS.json](c234c56353d88203-CHECKS.json) records passing section recovery, topology,
zero-state energy Hessian, exact pressure representation and finite
pin-roll checks at all three frequencies. Prior finite-state derivative,
Euler and pure-bending checks are inherited from the pinned 026 package.
They do not cure the new nonlinear eigenvalue-selection ambiguity.

[EXECUTION.json](b95d1ffec9a0a7ac-EXECUTION.json) contains **16 admitted, successful,
released jobs** and **one refusal**. The optional additional
frequency-6 m24 rise-1 static run was refused: 31 GiB charged plus 6 GiB
requested exceeded the host's 36 GiB admission budget. Nothing started
for that request. The two other members of its concurrent submission
batch had already been admitted when the refusal was observed; both
finished. There was no retry, fallback or subsequent scientific launch.
The paired m12 force/rise comparison is complete. Collection, chart
rendering and packaging perform no additional simulation.

The refusal was filed as
`rpt-ref-4a20323946ecafd56a6b`.
Any nonlinear first-loss verification needs fresh execution authority.
All times are measurements, not budgets. [NFI.json](d90bde67ada2ca77-NFI.json) preserves
the scientific holds and the execution limitation. **No certification.**
