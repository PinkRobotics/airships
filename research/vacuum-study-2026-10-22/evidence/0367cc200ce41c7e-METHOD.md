# MAINLINE062 closed-form calculation

**QUESTIONABLE / PROJECTION throughout.** `calculate062.py` uses only pinned data
and explicit arithmetic. It performs no finite-element solve, optimization or
parameter sweep. The new rows are the three requested sizes, plus two inherited
weather mass accounts per size.

## Scaling law

Let `tf` be one finished face thickness, `tc` the core thickness and
`d = tc + tf` the separation of the face centrelines. All length arithmetic uses
metres. For two load-sharing faces of a thin sphere,

```text
sigma_m = SF p R/(4 tf)
```

An initial local offset `a` gives an eccentricity-induced bending stress whose
first-order scaling is `sigma_m a/d`. Represent the dimensionless shape,
load-amplification and orientation response by `C`:

```text
sigma_peak ≈ sigma_m [1 + C a/d] + sigma_res
a_allow ≈ (d/C) [(Fy - sigma_res)/sigma_m - 1]
```

This is a **calibrated scaling hypothesis**, not a new constitutive law or a
closed-form proof of shell stability. A nonpositive bracket means no positive
amplitude under this screen; it does not mean a negative physical tolerance.
The reported cases all have positive brackets.

For geometric similitude (`tf`, `tc`, dimple width and `R` multiplied by the same
factor, with fixed pressure/material state), `sigma_m` and `C` are unchanged:
**tolerance scales linearly with radius**, not with radius squared. Merely making
the core thicker at fixed radius does not establish that benefit because the
shear compliance and load amplification can change.

Calibration uses CHECK047's printed independent estimates, **1.2179 mm at SF 1**
and **0.7469 mm at SF 1.05**, at the 047 reference geometry:
R = 10 m, tf = 0.794624066986 mm, tc = 23.237217906015 mm,
p = 95460.83791390515 Pa, Fy = 345 MPa. This gives
`C1 = 2.934644079` and `C1.05 = 3.025216514`. The two coefficients retain the
observed pressure dependence; they are not silently combined.

The requested 057 geometries are recovered from its **mask 15, actual-joining,
ISA** mass bills:

```text
A  = 4 pi R²
tf = Mfaces/(2 A * 1850 kg/m³)
tc = Mcore/(A * 16.018463373960138 kg/m³)
```

R10 uses the 048 record in 057; R20/30 use 057's 040-with-048-finish transfers.
Those are different geometries from 047's held R10 point. All four optimism axes
remain inherited; this is not a newly qualified minimum-optimism design.
The density conversions and thin-shell area convention match that bill.

For a separate conservative cure debit, retain 047's 037b-derived
`sigma_res,0 = 3.4102225696822703 MPa` and scale its core-force/face-area ratio:

```text
sigma_res(R) = sigma_res,0 (tc/tf)/(tc0/tf0)
w(R) = 0.332216 m * sqrt[R d/(10 m * d0)]
```

`w` is the Gaussian **e-fold radial span**, with displacement
`a exp[-(r/w)²]`. It is neither the full wavelength nor the dimple diameter.
The width relation keeps the classical sandwich length proportional to
`sqrt(R d)`. The precise nondimensional shear compliance and load ratio are not
identical in the new bills, so holding `C` fixed remains an unvalidated transfer.

| R (m) | tf / tc (mm) | w (m) | No cure, SF 1 / 1.05 (mm) | Cure debit (MPa) | With debit, SF 1 / 1.05 (mm) |
| ---: | --- | ---: | --- | ---: | --- |
| 10 | 0.809443 / 22.227508 | 0.32527 | 1.33564 / 0.87134 | 3.20232 | 1.25038 / 0.79257 |
| 20 | 1.625205 / 43.737746 | 0.64549 | 2.70067 / 1.78102 | 3.13840 | 2.53549 / 1.62841 |
| 30 | 2.442563 / 65.428684 | 0.96701 | 4.09370 / 2.71369 | 3.12380 | 3.84722 / 2.48598 |

Digits show reproducible arithmetic, not physical precision. No uncertainty band
is implied. The same result is checked algebraically with the ratio form:

```text
a_R/a_0 = (d_R/d_0)
          * [(Fy-sigma_res,R)/sigma_m,R - 1]
          / [Fy/sigma_m,0 - 1]
```

Pure homothetic scaling of the original geometry would instead give SF 1.05
values 0.7469, 1.4938, 2.2407 mm. The table's slightly larger values arise from
the changed 057 gauges and face-stress headroom, not a claimed new material.
The 345 MPa tensile-to-compression proxy remains the dominant assumption.

## Mass and cost account

Preserve all entries of 057's six selected bills, including gas, systems, water,
primer, finish, pads and contamination. Its optimistic-weather headroom is a
**lift debit**, not additional physical material. The selected actual-joining
account is named explicitly; the separate 5%-floor cases are not substituted.

Add projected retained shape hardware/filler `0.020 A kg`, plus `30%` concept
growth on this addition. Existing itemized 057 growth is retained once. Temporary
jigs and adjusters are ground equipment, counted in cost and reported mass but
not in flying mass. No extra flight frame is assumed.

The cost arithmetic uses the delivered stock, panel count, two-face seam length
and component amounts. With scarf overlap `ell = 30.34139731914874 tf`,

```text
panels_per_skin = ceil[A/((0.6096-ell)(1.8288-ell))]
unique_joint_length = A[1/(0.6096-ell) + 1/(1.8288-ell)]
two_face_scarf_length = 2 * unique_joint_length
rectangular_blank_stock = 2 * panels_per_skin * 0.6096 * 1.8288 * tf * 1850
purchased_Be = rectangular_blank_stock / additional_process_yield
```

These are ideal tiling estimates. Actual closure patterns, polar pieces and smaller
stock can add seams; the stock-yield and cost-contingency assumptions are shown
separately and do not prove that the nominal layout is procurable.
The rectangular stock takeoff charges material removed by scarf preparation.
Net face/rectangular-stock yields are 0.9464, 0.8942 and 0.8428; the separate
90%/70% process/procurement yield multiplies these, rather than replacing them.

Every cost line is `quantity × stated planning rate`; the two scenarios use
different procurement yields and cost contingency. All rates and scope limits are
in `ASSUMPTIONS.json`, and every line is in `COST-BILL.csv`. Historical telescope
costs retain their original price year and procurement scope; they do not set
the Be sphere's price.
