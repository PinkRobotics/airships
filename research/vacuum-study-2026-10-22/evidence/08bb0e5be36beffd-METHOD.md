# MAINLINE-033 method and source record

All inherited material values are QUESTIONABLE; all shell/process transfers and calculated outputs are PROJECTION. An “SF” here is capacity divided by applied pressure in the stated screening equation. Installed-hull SF is unknown.

## Case, reserve and accounting

R is sphere radius, A=4πR², and reference lift L=4889.442150186961(R/10)³ kg. p0=95460.83791390515 Pa, T0=284.9 K. Structural load uses p=1.01p0, simultaneously with the optimistic reserve budget. S is faces plus honeycomb, before joining.

The 019 optimistic fixed reserve is:

```
B = L[1 − 0.99T0/(T0+10)]
  + L[0.378×1000/p0 × T0/(T0+10)]
  + 0.01L
  + A×1000×0.0001
  + A×5/(400π).
```

The first three terms scale with volume; water and contamination scale with area. Ground evacuation/monitoring hardware totals 30 kg in the inherited assumption; the full 100 kg systems allowance stays reserved, so there is no additional excess systems charge.

Main mass closure is **Y=L−100−B−S−J**, where Y is signed payload and J is the nominal 028 inventory below. The 027 accounting comparison is **Y=L−100−B−S−max(J,0.05S)**. Thus unused joint reserve is retained only in that comparison. Reserve at R10 is recalculated from input numbers rather than a rounded percentage.

For each core mass fraction f, tf=S(1−f)/(2Aρface), tc=Sf/(Aρcore), and h=tf+tc. tf is each face thickness. ρface=1850 kg/m³. Stock panel dimensions never increase with radius.

## Joining scaled by its own geometry

Stock blanks a=.6096 m and b=1.8288 m, scarf ratio r=30; each coverage dimension loses r tf. The common hull seam length, counted once, is

```
Ls = A[1/(a−r tf) + 1/(b−r tf)].
J = 2A μ
  + Ls[2 tf sqrt(1+r²) × .07
       + tc × .0005 × 500
       + .002]
  + 2A μprimer.
```

μ=.07323641454574575 kg/m² is .015 lb/ft² per face/core interface. The two scarf films use .07 kg/m²; core splice is a .5 mm gap at projected 500 kg/m³; .002 kg/m is sealing for both faces combined. Primer is zero nominal and .005 kg/m² per interface in the named sensitivity. Invalid a−r tf or b−r tf is infeasible. This counts overlap-related coverage loss and seam adhesive; it does not add a full extra sheet strip where two scarf wedges already form one nominal face thickness.

The 028 frozen R10 geometry reconstructs 214.239997842 kg of nominal joining. At each new optimum both thicknesses and the seam takeoff are recalculated; J is not treated as one fixed kg/m² across changing geometries. The old 020 splice mass and eta=.9 are unused.

## Face properties and optimism

Baseline face E=290 GPa, strength=345 MPa; full third improvement E=293.6 GPa, strength=379.2 MPa. Density remains 1850 kg/m³. Strength is an uncertain compression transfer. E and strength always move together under that named third improvement. Primary nu=.0768 uses the historical SR-200 in-plane value as an isotropic proxy; nu=.33 is a separately identified legacy sensitivity.

Let sigma=pR/(4tf), sigma0=E h/[R sqrt(1−nu²)], and sigma_cr=Gc h²/(2tf tc). Set Vc=sigma0/sigma_cr. The baseline gamma is .20 for Vc<2 and 1 for Vc≥2, as in 021b. Full gamma=.20+.40 min(Vc,2). The separate literal handbook benchmark keeps gamma=.20 on both branches. Baseline Q=.33; full Q=.82.

Selected improvements interpolate logarithmically: value=today×(full/today)^u, 0≤u≤1. Unselected improvements stay at baseline. To minimize maximum usage, all selected improvements can first be capped at common u and geometry reoptimized; monotonicity makes this sufficient for feasibility. After finding the smallest u, any unused gamma/Q is reduced at fixed geometry. The paired E/strength choice stays coupled. Set selection first minimizes number of named improvements, then maximum normalized logarithmic usage.

## Six shell modes and separate scarf screen

Use Kc=1−Vc/4 for Vc≤2, otherwise 1/Vc. beta is the positive root of beta³+beta=1, approximately .6823278038280194.

| Mode | Screening SF |
| --- | --- |
| Global buckling | gamma Kc sigma0 / sigma |
| Face compression | strength / sigma |
| Core shear crimping | sigma_cr / sigma |
| Core crush | 2 sigma_crush / p |
| Face wrinkling | beta Q sqrt(E Ec tf/tc) / sigma |
| Intracell dimpling | E(tf/cell)² / [(1−nu²)sigma] |
| Optional scarf average shear | 10 MPa / [sigma r/(1+r²)] |

The 30:1 scarf screen caps sigma at 10 MPa×(901/30)=300.333333 MPa. Its 10 MPa value is an owner-selected projection, not an AF163-2U/SR-200 allowable. The six-mode optimization reports this seventh number but does not constrain it; the paired track constrains it. No mode is silently made safe because its material allowable is unknown.

## Search and independent checks

All eight subsets and all 47 supplied honeycomb rows are evaluated at R=10,15,20,30,50 m. For fixed f and core, required S/L follows explicit compression, crimp, wrinkle, scarf and cubic dimpling bounds; monotone global capacity is resolved with an upper-sided 42-step bisection, preserving the upward branch switch. Payload decreases with S at fixed f, so the least feasible S gives its greatest payload.

Reported full endpoints search 3,999 interior fractions per core and refine all local peaks on all cores. Minimum usage starts with a coarser search and then refines the chosen active equations: global SF=1, observed active wrinkle or scarf SF=1, and Y=0. The independent verifier rechecks capacities directly from reported tf/tc using 50-digit Decimal critical pressures and direct mass takeoffs; it imports no model code. All 10,289 scalar comparisons passed. The retained and actual-joining cases, all full subsets, thresholds, refined minima and sensitivities are included in its 381 geometries.

A separate dense 15,999-fraction grid on all 47 cores checks 39 endpoint/crossing cases and 22 least-usage/noncrossing-peak cases. All 61 passed. Refined results never underperform the dense grid beyond tolerance, and local improvement is below .001 of lift. This is a numerical cross-check rather than an interval certificate. One refinement initially assumed scarf remained active at R50; its zero-payload assertion caught that assumption, and the final method selects the observed active constraint. Final outputs include that mode switch.

Radius searches use 64 logarithmically spaced points plus interior-peak refinement, then zero-crossing refinement across every core. The lower endpoint is .5 m, already impossible from the 100 kg systems allowance alone. An upper endpoint follows required face thickness and scarf overlap: R<4 sigma_cap a/(r p), where sigma_cap is the available face strength, additionally bounded by 300.333 MPa when the scarf screen is applied. Best sampled noncrossing peaks are separately checked with all 47 cores at a denser grid. Accepted finite geometries all have positive coverage dimensions. SciPy warnings in the search log arise from rejected infinite-cost overlap geometries.

A radius-independent ideal SF envelope omits systems, water, contamination, actual joining and dimpling, retaining volume climate/gas losses and any selected 5% floor. At its maximum available structural fraction, geometry depends only on f/core and those modes are independent of R. A numerical maximum below one rules out a crossing under that model; a maximum above one triggers the finite-radius search. Both the bounding omissions and numerical scope are explicit in RESULTS.json.

Published face-gauge limits are recorded, not imposed on every formal search. In particular, the gamma+strength crossing uses a face above 6.35 mm; the compression-only radius ceiling for that sheet maximum is already below its formal crossing, so it is not a stock-gauge result. Published maximum blank dimensions at thin gauges remain unknown.

## Sources and limits of transfer

[Materion SR-200 product data](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6) supports the baseline density, E, tensile-yield figure and stock description. It does not qualify compression of a formed thin sphere. The stock dimensions apply to the stated gauge interval; use the 0.25 inch maximum where the printed metric conversion is inconsistent.

[NASA CR-194164, Tables 2 and 3, PDF page 22](https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf) reproduces historical SR-200 rolled-sheet results supporting the E/strength endpoint and nu12=.0768, nu21=.0752. These are historical sheet data, not current process allowables or an isotropic validation. The original Fenn study cited there was not reopened.

[NASA CR-1457](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf) supplies the inherited sandwich-shell modeling context. The present gamma curve, scalar-property substitutions and application to a joined sphere are projected transfers.

[3M AF163 technical data](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf?fn=AF163-2.pdf) supports the nominal film weight. Reticulation is resin redistribution, not proportional mass deletion. This card does not assign a qualified bond or scarf allowable to the installed combination; no unverified weight tolerance is used.

[CIPM-2007 moist-air formulation](https://www.nist.gov/system/files/documents/calibrations/CIPM-2007.pdf) supports the ideal-mixture direction and molar-mass humidity correction behind the reserve convention. The full high-accuracy metrology formulation is not extrapolated here; the 019 loss laws remain assumptions.

The pinned 014b/027 catalogue supplies all 47 core rows and their source tags. The selected aluminium row cites [Hexcel CR-III data](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf): rho=16.018463 kg/m³, cell=9.525 mm, Ec=103.421359 MPa, weak-direction Gc=46.884350 MPa, crush=0.241316505 MPa. Those supplier typical values remain QUESTIONABLE design inputs. The alternate Q+strength route uses HRH-10-4.8-32. The catalogue includes projected scaled cores but they do not win the selected minima.

INPUTS.json records absolute primary-document pins and all upstream snapshots. Primary evidence was inspected in this seat's preceding CHECK-021/021b and reused with hashes verified here. No upstream owner's executable was read, imported or run for this card.

## Reproduction

From this artifact directory, with Python, NumPy, SciPy and Matplotlib versions recorded in INPUTS.json:

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 TMPDIR=unpublished-local-ref:1ffe4110219d37c0 python3 calculate.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 TMPDIR=unpublished-local-ref:1ffe4110219d37c0 python3 refine.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 TMPDIR=unpublished-local-ref:1ffe4110219d37c0 python3 validate.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 TMPDIR=unpublished-local-ref:1ffe4110219d37c0 python3 verify_search.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 TMPDIR=unpublished-local-ref:1ffe4110219d37c0 python3 verify_minima.py
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 TMPDIR=unpublished-local-ref:1ffe4110219d37c0 python3 package_card.py
```

Use a new output copy for reproduction; the filed artifacts are immutable. The original run computed the two retained-floor tracks first, then added the explicit-bill tracks with extend_budget.py; calculate.py now reproduces all four in one run. Reporting precision exceeds material certainty so that checks can reproduce the numbers.
