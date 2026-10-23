# REVIEW-A1 independent method

All inherited physics is QUESTIONABLE; transfers and cost/growth scenarios are
PROJECTION. Seventeen load-bearing claims were listed before review. The authors'
prose, pinned inputs and result data were inspected. Their executable code was
neither read nor run. REVIEW-A1 owns only 056 and 062.

## Nonlinear equilibrium spot check

`check_field_a1.py` reads a pinned Q8 mesh and the refined pressure case's PEAK
state. It obtains the eight serendipity shape functions by interpolation of
`[1,s,t,st,s²,t²,s²t,st²]` on the eight natural nodes. This supplies fresh
shape derivatives and quadrature without importing an element implementation.

At each integration point it evaluates the meridional deformation gradient,
hoop stretch r/R, J and H=log(U). It subtracts the saved corotational plastic
strain and applies the declared elastic tensor to obtain Cauchy stress in that
frame. It uses `P=J F U⁻¹ sigma_hat U⁻¹`, with the hoop analogue, for virtual
work in reference volume. The nodal radial force includes the hoop term N/R.

Independent current-surface integration gives the unit inward pressure load.
After excluding the declared constrained degrees of freedom, pressure is
`dot(f_internal,f_unit)/dot(f_unit,f_unit)`. Saved pressure is consulted only
after this result is obtained. Yield-surface ratio, minimum J, reference volume
and the number of core points beyond the last hardening knot are separately
computed.

The state lacks explicit Voigt/quadrature metadata. The review checks the two
standard axisymmetric component arrangements, tensor versus engineering shear,
and both Gauss loop orders. The standard rr/zz/hoop/engineering-rz layout and
xi-outer point order is uniquely consistent with equilibrium. This resolves
the format for this reconstruction without fitting geometry, material
constants or pressure.

The review independently extracts sampled maximum pressure and neighboring
samples from four pinned raw paths. This verifies the reported range and
percentage comparisons. It does not recreate the constitutive/contact history,
test alternative imported hardening, or prove a physical/nonaxisymmetric limit.

## Independent linear anchors

`check_linear_a1.py` constructs a fresh perfect hemisphere mesh for each radius
reading: outer radius 42.8 and 44.77 mm; faces 0.42 mm each, core 3.1 mm.
Resolution is 384 meridional elements, eight core layers and two layers per face.
Steel E=210000 MPa, nu=.33; foam E=40 MPa, nu=0. These are the source's
conditional elastic anchors.

The script integrates the small-strain axisymmetric B matrix and elasticity
matrix, applies unit dead pressure, solves its preload and builds geometric
stiffness from that stress. Boundary conditions constrain radial motion at the
axis and both components at the equator. The lowest positive eigenvalue of
`(K + p Kg)v=0` is found through `(-Kg)v=mu K v`, with p=1/mu.
Rayleigh quotient and eigen residual are checked separately.

The first execution completed the first numerical solve but its comparison
adapter incorrectly treated the owner's four-value eigenvalue array as a scalar.
The adapter was corrected to select the smallest value; the failed receipt and
successful two-case rerun remain in the package. This was a reviewer-harness
issue, not a finding against 056.

## Independent 062 arithmetic

`check_accounts_a1.py` selects the pinned 057 mask-15, actual-joining bills at
R10/20/30. It recovers face/core gauges from mass, area and density.
It eliminates C between the reference and target amplitude equations and also
solves the equivalent linear stress-slope equation. The reference amplitudes
are intentionally rounded to four decimals as declared by 062. Pure homothetic
scaling holds dimensionless stress ratios constant and multiplies amplitude by R.

Stock takeoff charges the full rectangular blank count before scarf trimming,
then divides by the declared 90%/70% additional process yield. Panel, seam,
core, joining, labor, hardware, jig, metrology and other charges are rebuilt
from quantities and stated rates. Hall/handling larger-radius values are
supplied planning allowances because their scaling exponents are not declared
in the assumptions file; the implied exponents are reported, not invented as
sourced prices.

For mass, preserve every original bill line, add 0.020 kg/m² shape hardware and
its 30% growth, and independently apply the inherited class rates. Two accounts
are shown: exact reconstruction of the owner's inherited formula, and the
correct embedded-coating-margin denominator. The latter correction is explicitly
unreviewed. There is no second review of fixes.

## Primary-source spot checks

The pressure-paper provenance, SR-200 sheet properties and AF 163-2 film/cure
identity are read directly from pinned primary PDFs; browser access was also
attempted. Hexcel Table II supplies directional anchors, not an installed full
law. ALMA and the S-II fit record are selected precedent checks; the remaining
records' local-defect fields are inspected without rebuilding the full
precedent table. Exact pages, URLs and hashes travel in INPUTS.json.

## Execution

Use the own `admit_a1.py` wrapper from the checkout, with TMPDIR=unpublished-local-ref:1ffe4110219d37c0 and
OMP/OPENBLAS/MKL/VECLIB/NUMEXPR thread counts set to one. It submits the named
script to simjob for one core and 1 GiB, retains logs and source hashes, and
retries only unchanged admission refusal exit 75. Run `check_field_a1.py`,
`check_linear_a1.py`, then `check_accounts_a1.py`; `build_review_a1.py` assembles
the review. `validate_a1.py` checks the resulting dispositions, pins and
arithmetic consistency. Times are measured; no task budget or clock stop is used.
