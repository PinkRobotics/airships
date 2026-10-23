# MAINLINE-022d — model and source ledger

Every result is **QUESTIONABLE**. Unvalidated material and geometry transfers are **PROJECTION**.
The source snapshots and their supplied hashes are in INPUT-PINS.json. Existing owner scripts were read
as evidence and never imported or executed. scan.py, sensitivities.py and verify.py belong to this seat.

**Scope and inherited contracts**

The requested primary matrix is 2 sag branches × 2 grids × 2 reserves × 4 film/joint families.
Each has an unconstrained numerical optimum and an optimum satisfying the specified half-wave screen.
The source is the pinned 022c SAG.json, with 023, 024, the completed 025 work, the independent 022b/022c
check and 030's CONTINUUM.json. The order itself is snapshotted as inputs/ORDER.json.

R=10 m, p=95,460.8379139 Pa, buoyancy mass=4,889.44215019 kg, E=410 GPa,
SiC density=3,100 kg/m³, systems=100 kg and each nominal node=0.02 kg.
Reserve is 244.4721075095 kg (5%) or 411.2989440716474 kg (019's inherited fixed reserve).
The 019 reserve is not recomputed as a new equipment design.

| Family | Film density, kg/m³ | Directional stress used with total gauge | Total gauge floor | Joint rule | SiC Fc |
|---|---:|---:|---:|---|---:|
| Projected film | 970 | 1.5 GPa | 80 µm | 5% of tube+film+nodes | 3.9 GPa |
| Mylar | 1400 | 22 ksi = 151.684660450 MPa | 12.192 µm | same 5% rule | 380 MPa |
| Kapton/Ti | 1420 | 231×0.5 =115.5 MPa | 25 µm | sized Ti sleeve | 3.9 GPa |
| Zylon/CFRP | 1560 | (5800×0.6)/2 =1740 MPa | 12 µm | sized CFRP wrap | 3.9 GPa |

Zylon's scalar 1740 MPa is only a bookkeeping equivalent: total gauge t comprises two t/2 plies,
each checked against the assumed fiber stress 3480 MPa. All total ply mass is charged.
The 12 µm inherited floor is not a sourced membrane specification; it is inactive at all reported points.
None of the four continuous gauge floors is active. Arbitrary thick, seamless film supply is not established.
Mylar's 380 MPa is an inherited flexural proxy, not a qualified compression allowable.
The 3.9 GPa input is also not a full-size arc allowable. Actual qualified values remain null.

**Geometry and force**

s is chord/node spacing, L=2R asin(s/(2R)) the member arc length, and S=4πR².
Equilateral: faces=S/(√3 s²/4), members=1.5 faces, nodes=0.5 faces+2,
N=pRs/(2√3), global coefficient C=4√(3/2).
Two-way: faces=S/s², members=2 faces=2 nodes−4, nodes=faces+2,
N=pRs/2 and inherited C=4. These are continuous lattice counts, not an integer mesh.
An unbraced two-way grid lacks the in-plane shear stiffness assumed by its scalar global surrogate
(NFI-030-TWO-WAY). No computed two-way multiplier establishes a physical frame capacity.

**Sag**

Curvature radius ρ=s is retained. The cap branch uses a circular cap over the triangle inradius
b=s/(2√3): h=ρ−√(ρ²−b²), mean=h²(ρ−h/3)/b². This is a circular-cap approximation.
For an equal-tension, small-slope equilateral membrane, −∇²w=2/ρ and zero edge displacement:
w=(3s²/(2ρ)) b1 b2 b3 in barycentric coordinates. The mean of b1 b2 b3 is 1/60,
so the **exact mean within that linear membrane model** is s²/(40ρ).
At ρ=s this is 1.1660029709329 times the chosen cap mean. It does not claim an exact nonlinear
stressed membrane, measured shape or gas-barrier assembly.
Lost lift is 3×buoyancy mass×mean/R, the inherited first-order volume correction.
Film mass uses S and omits extra sagged area, seams and separate barrier coatings.

For the primary two-way comparison, both sag laws are retained literally from 022c, and the
triangular-to-square transfer is flagged. A separate 32-witness sensitivity uses square inradius s/2
for the cap and the exact linear square membrane mean 0.0702885074776 s²/ρ.
The latter follows either a double sine series or an independently checked single series.
This choice changes more than the five requested corrections and is therefore separately identified.

**Coupled mass and joint sizing**

At each candidate (s,r_o,t_film,λ), film mass is Sρ_f t_film and node mass is 0.02×nodes.
Available structural mass is buoyancy−reserve−sag loss−systems.
For 5% joints: assembly=available/1.05, M_joint=0.05 assembly,
M_tube=assembly−M_film−M_nodes. This is an allowance; there is no joint strength law for these two families.

For a sized end at its own load λN:
A_joint=λN/σ_joint, overlap=λN/(2πr_o τ), m_end=ρ_joint A_joint overlap,
and M_joint=2×members×m_end is removed before finding tube area.
Thus m_end=C_joint(λN)²/r_o, not C_joint N²/r_o.
Using 023's unrounded inputs:
Ti: density 4430, axial 827 MPa; CFRP: density 1550, compression 1470 MPa;
both use adhesive shear 28.9 MPa. C_Ti=2.949989740284e−14 and
C_CFRP=5.806797113962e−15 kg·m/N².
The adhesive result was measured on aluminum adherends; transfer to SiC is unqualified.
No adhesive layer, peel, moment stiffness, sleeve buckling or end load spreading mass is added by this law.
Both sized capacities equal λ by construction, with no additional joint reserve.
For λ<1, the computed joint is sized below operating load; that row is a failed design, not a
demonstration at full pressure. This explains why resizing sub-unity Kapton/Ti cases can raise
their numerical optimum relative to joints sized at N.

**Section and modes**

A=M_tube/(3100×members×L), r_i=√(r_o²−A/π), t=r_o−r_i,
I=π(r_o⁴−r_i⁴)/4. Invalid annuli and nonpositive tube budgets are excluded.
The separately scored linear load factors are:
compression Fc A/N; Euler N_E/N with N_E=π²EI/L²;
local [γ×0.6Et/r_o]A/N, γ=0.099+0.901 exp[−√(r_o/t)/16];
film 2σ_effective t_film/(ps); global 0.2 C E√(IA)/(sR²p).
The local correlation is inherited from NASA SP-8007 Rev.2, printed pp.23–25,
equations 9–10; application to long, curved ceramic members remains unqualified.
Primary source: https://ntrs.nasa.gov/api/citations/20205011530/downloads/20205011530%20Rev%202FINALa%201-2023.pdf

Initial bow e=L/1000. At load qN below Euler:
M=qNe/(1−qN/N_E), σ_c=qN/A+Mr_o/I,
σ_t=max(0,Mr_o/I−qN/A). Perry limits σ_c≤Fc.
The added tensile constraint is σ_t≤15.586 MPa, explicitly **PROJECTION**.
That number is the rounded, deliberately hypothetical 025 m=10 full-volume screen
at a specified reference assembly and assumed probability; it is held fixed here to reproduce
the previous check's sensitivity. It is not recalibrated for each optimized tube volume and
does not establish an actual failure probability. 0, 7.192 and 380 MPa alternatives are reported.
No finite elastic stress is reported past the Euler pole.
Taking the minimum of modes does not validate coupled shell/column/bending instability.

**Half-wave and search**

030 uses D/Y=(9/8)I/A for the equilateral smear. Its half-wave is
ℓ=π[(9/8)(I/A)R²]^(1/4)=π√(√(9/8) r_g R), r_g=√(I/A).
The primary additional condition is ℓ≥L, the actual curved member length.
Both ℓ/L and 030's original ℓ/s are recorded. A pass at one member is only the requested
minimum screen; homogenization ordinarily needs multiple cells and remains unresolved.
The same 030 expression is shown on primary two-way diagnostic rows for comparison,
without claiming it is a validated two-way wave.
The square-cell sensitivity uses D/Y=I/A, consistent with the inherited scalar C=4 closure;
it still supplies no missing two-way shear stiffness.

Primary bounds: 0.4≤s≤8 m, 0.003≤r_o≤min(0.25,s/3) m, 0.001≤λ≤5,
and continuous total film gauge between the inherited floor and the mass-only upper bound.
The objective maximizes λ subject to every strength, mass, section and optional half-wave constraint.
An initial three-variable search selects the minimum film needed at λ; the final
four-variable differential-evolution search frees film gauge, followed by multiple SLSQP refinements.
All 64 four-variable global-search runs terminate successfully. Multiple starts and the initial
witnesses agree in load factor. This is numerical evidence, not a proof of the mathematical global optimum.
No primary spacing/radius bound is active. Sixteen cap/5% cases were additionally searched over
0.15≤s≤19.9 m and 0.001≤r_o≤min(1,s/3) m; none improved beyond numerical tolerance.
Bindings are modes within 2e−6 of the optimized multiplier. Accepted feasibility uses 2e−9
absolute load-factor tolerance; the independent verification uses 3e−9. Boundary ratios are
therefore interpreted at numerical precision, not as manufactured tolerances.

verify.py independently reconstructs annulus masses, member forces, D and Y, direct
Euler-magnified moments, compression/tension roots, directional film loading and joint
area/overlap capacities. It reproduces 030's seven published half-waves, verifies both sag
integrals and the source snapshots, and checks all 112 optimized sensitivity witnesses.
The comparison is numerical/model evidence only.

Reproduce: run scan.py, sensitivities.py, verify.py, then assemble.py in this folder.
SEED-SCAN.json preserves the initial three-variable starting witnesses. The final search
does not rely on executing another seat's programs. No external seat, supplier or shared runtime
file was written by this work. The order is completed by its queue report; no next job is named.
