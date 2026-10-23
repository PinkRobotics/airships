# MAINLINE-027 calculation and scope

All material inputs are QUESTIONABLE. Fabrication, joint efficiency, gamma curve,
full-021 material transfer and P3 components are PROJECTION.

The requested radius series is evaluated at one atmosphere: reference R = 0=10 m,
L0=4889.442150186961 kg, p 0=95460.83791390515 Pa, T0=284.9 K.
A=4πR², V=4πR³/3, L=L0(R/10)³. No additional altitude change is inferred.

## Budget laws and exact mass closure

The two climatic scenarios retain 019's temperature rises 10/25.1 K, pressure
fractions±.01/±.02 and vapour pressures 1000/6000 Pa. Moist lift is

    Lhot = L [(1-dp) - .378 e/p0] T0/(T0+dT).

Dry loss uses e=0; humidity is the difference between dry and moist values.
Internal air mass is .01L, retained conservatively with no load relief.
This is an ideal-mixture planning calculation, not a meteorological bound.
Water is Aρδ, with δ=.0001/.001 m. Contamination is A times 5/25 kg divided
by 4π(10 m)². Extra coating is zero in the main scope and .1 kg/m² in a sensitivity.
No statistical contingency is hidden in the word reserve.

020's panel dimensions are held: (.6096,1.8288)m optimistic,
(.3048,.6096)m conservative. Let λ=1/a+1/b, μ be film mass per interface
(.1464728290914915/.292945658182983 kg/m²), w=.06/.12 m, g=.001/.002 m,
and sealant cross-section Ab=1e-5/3e-5 m², paste density 1100 kg/m³.
Both skins are included. At structural mass S and core mass fraction f:

    tf = (1-f)S/(2Aρf), tc = fS/(Aρc)
    m_join = A λ [2ρf tf w + 2μw + 1100 g tc + 1100 Ab] + 2Aμ
           = u(f)S + v
    u(f) = λ[w(1-f) + 1100 g f/ρc]
    v = A[λ(2μw+1100Ab) + 2μ].

The requested frozen-areal screen replaces this with 020's original total
joining/A0. Those constants describe the old 009c5 gauge only. In the coupled
model, strap/core-gap parts approachR³ if thicknesses scale with R, whereas the
remaining film/adhesive/sealant parts remainR². Neither recipe is a designed joint.

Let B be weather+gas+water+contamination+coating+systems excess, excluding
joining and payload Y. Systems excess=max(0, actual systems-100).
With retained baseline floors the complete equation is

    L = 100 + 1.05S + B + max(0, m_join-.05S) + Y.

For each f, let H=L-100-B-Y. Candidate S0=H/1.05 is accepted if
m_join(S0)<=.05S0. Otherwise S=(H-v)/(1+u). This closes the resized seam
budget analytically at every optimizer evaluation. Negative S is infeasible.
Reported reserve is B+max(0, m_join-.05S), not the remaining free payload.
This makes the physical carried mass equal the hot moist lift after removing
the separate climate opportunity-loss rows. Unused allowances remain reserved.
There is no common margin constraint across families.

The passive systems estimate 15+10+5=30 kg is fixed. The literal active screen
uses 223 kg pump+20 kg controls+24 h(5500+5)W/(150Wh/kg×.8×.9)
=1466.333333 kg. With one-percent-volume/day gas load and gas temperature 320 K,
required inlet speed is(V/24 h)(320/T0), equal 196.0355776 m³/h at R = 10.
The capacity-aware variant takes N=ceil(required speed/240 m³/h),
hardware 223Nkg, power 5500N+5 W and the same battery formula, with 20 kg controls.
This is an explicit modular projection, not installed-system qualification.
If leak/outgas follows area rather than the inherited volume allowance,
capacity would instead tend toR²; no such measured decomposition is available.
All 24 h pumping cases hold the 1% internal-gas mass reserve.

Passive total gas throughput, normalized toT0, must not exceed
V[(.01p 0)T0/320-10 Pa]/86400s to finish below the pressure ceiling after a 10 Pa
start atT0. This is conditional capacity, not achieved leak tightness.

## P2 structural calculation and search

With h=tf+tc:

    sigma0 = E h/[R sqrt(1-nu²)]
    sigma_crimp = h² Gc/(2tf tc)
    Vc = sigma0/sigma_crimp
    Kc = 1-Vc/4 for Vc<2; 1/Vc otherwise.

Design gamma=.2 below Vc 2 and 1 at/above 2 (021 convention). Full 021
gamma=.2+.4min(Vc,2). Flat-gamma sensitivity is.2 throughout.
The inherited discontinuity is not newly justified. Both sides of every
observed Vc=2 crossing are explicit optimizer candidates.

At maximum external pressure p=p 0(1+dp), capacities divided by p are:

    global: 4 gamma Kc sigma0 tf/(Rp)
    face: 4 sigma_allow tf/(Rp)
    core crush: 2 core_crush/p
    crimp: 2 h² Gc/(R tc p)
    wrinkle: 4 BX Cw sqrt(E Ec tf³/tc)/(Rp)
    dimpling: 4 E tf³/[(1-nu²)cell² R p]
    joint net section: eta × face SF.

BX is the positive root of BX³+BX=1. Dimpling uses 021's equibiaxial half of
the older uniaxial allowable. η=.9/.6 is 020's assumed seam screen; it does
not scale global, wrinkle or every other mode. All modes are retained in JSON.
The solver scans 4001 fractions, refines all observed local peaks and both
sides of branch switches, and checks the result against 100001 fractions.
There is no gauge, core-depth or procurement feasibility constraint hidden in
the optimizer; unrealistic small gauges are explicitly projected.

Payload is an outer feasibility bisection, reoptimizing at every trial. It is
only returned when the zero-payload envelope has least SF≥1. The lower feasible
side is retained. This is a model maximum, not an operational payload approval.

## P3 continuation

The held bounds are physical bay.4≤s≤3 m and outer radius≤min(.25 m, s/3).
Nnodes=8πR²/(√3s²)+2; Nmembers=3Nnodes-6; member length=s as in 011b.
Spherical arcs are assumed; extra arc/chord length correction is not applied.
Node mass=.02Nnodes, film=A×970 kg/m³×80 µm, systems floor 50 kg,
joints=.05×tube mass. Tube mass is the remaining mass divided by 1.05, and
section area is tube mass/(Nmembers s×3100 kg/m³).

For an annular section with outer/inner radii ro/ri,
I=π(ro⁴-ri⁴)/4, rg²=I/Abar, axial stress=pRs/(2Abar).
Scores are compressionσc/σax, Eulerπ²E rg²/(s²σax),
local.6E(tw/ro)/σax, film 2σfilm tfilm/(sp),
PerryσP/σax, and global
.2×4√(3/2)E√(I Abar)/(sR²p).
Perry uses imperfectiona 0=s/1000, η=a 0 ro/rg²,
φ=[σc+(1+η)σEuler]/2, σP=φ-sqrt(φ²-σcσEuler).
The evaluator uses the algebraically equivalent rationalized root.
E = 410 GPa, compression 3900 MPa, film 1.5 GPa remain inherited.
The 380 MPa strength case and node mass∝R·s sensitivity are separate.
The material is brittle; Perry's applicability and all joints remain open.

A131×401 coarse grid seeds local refinement of distinct peaks, checked against
801×1001. Payload is reoptimized with the same bounds. Bounds intentionally
are not silently expanded at largerR. Therefore this is a bounded continuation
of 011b, not a proof of the best conceivable SiC frame.

The independent similarity diagnostic scales source 011b s, ro, tw by R/10,
keeping film thickness fixed and separately reporting member and node count.
Its film score falls as 1/R, all other modelled structural scores are constant.
If film also scaled in thickness, its mass would becomeR³ and this specific
film penalty would vanish. A different design would have to pay that mass.

## Provenance and validation

prepare_inputs.py verifies 53 pins and extracts values without importing old
code. 021 revision 1 is used; the superseded original has changed artifacts.
The actual 019 filing ID uses lead-sci, despite the brief's lead-sciences spelling.

validate_and_plot.py imports neither numerical solver. It re-derives critical
pressures and carried-mass balances in 45-digit Decimal arithmetic, reproduces
020 joining and 021 points, and verifies source pins. frame.py separately
reproduces the 011b SiC pressure scores. These are in-house arithmetic checks,
not an independent seat review, experiment or structural certification.

Reproduction sequence, working within this output directory:

    python3 prepare_inputs.py
    python3 compute.py
    python3 frame.py
    python3 catalogue.py
    python3 validate_and_plot.py
    python3 build_card.py

Set TMPDIR=unpublished-local-ref:1ffe4110219d37c0 and OPENBLAS_NUM_THREADS=1 for numerical runs.
The scripts write only their own directory; freeze filed outputs.
