# Independent method and execution boundary

The permitted inputs are the pinned order, brief, owner data/docs and primary-source copies listed in `INPUTS.json`. Owner scripts are explicitly excluded. No owner module was imported. This check uses its own algebra, numerical solver and comparison writer.

## Executed thermal calculation

`thermal_check.py` uses a 2 m/s outer flow, diameter 2R, inherited density 1.1672683307461802 kg/m³, viscosity 1.79e-5 Pa·s, conductivity .0257 W/(m·K), and Prandtl .71. Its Whitaker expression is:

`Nu = 2 + (.4 sqrt(Re) + .06 Re^(2/3)) Pr^.4; h = Nu k/(2R)`.

At R10 the resulting h is 2.0003531525224467 W/(m² K). The viscosity-ratio factor is taken as one; this is an explicit checker convention.

At μ=cosθ, it assumes sky/ground view fractions `(1+μ)/2` and `(1−μ)/2`, ground temperature 284.9 K, sky 275 K by day and 260 K by night, and solar flux `α*970*max(μ,0)`. Outer and inner balances are:

`0 = solar + h(Ta−To) + εo σ(Fsky Tsky^4 + Fground Ta^4 − To^4) + U(Ti−To)`

`0 = U(To−Ti) + .2 σ(<Ti^4>−Ti^4)`.

The core conductance is `U=130 ρcore/(ρAl tc)`, with ρAl=2640 for the legacy convention and 2700 for common. A coupled Newton method solves both temperatures and the cavity fourth moment, with residuals recorded. Legacy uses 37 uniform μ midpoints; common uses 128 Gauss-Legendre points.

Degrees 0 and 1 are removed from the Legendre temperature reconstruction. Common also subtracts the weighted mean before projection. Curvature extrema are found from the derivative roots of `(1−μ²)T''−μT'`. The uncorrected legacy projection assigns spurious curvature to a constant field; it is retained only as a diagnostic.

Day and cycle shear-lag factors use the independently derived mismatch coefficient, published source geometry and typical W shear strength. Cure-edge factors use minimum W strength, compliant core stiffness, the 200°F cure reference and the 1.002 guard.

This model does not reproduce the owner's published temperatures. In particular, its fully converged legacy calculation is not identical to the owner's declared 25 fixed iterations. The common-model discrepancy also remains. These results are explicitly a different, fully specified boundary reconstruction; they do not establish that the owner implemented the stated model incorrectly.

## Executed account calculation

`execution/account-01/source/account_model.py` is the version that produced all retained account results. It independently evaluates the written 040/048 pressure, stability, compression, crimping, wrinkling, dimpling, scarf, core-edge and cell-wall equations. It implements the nominal sphere area for both skins, full 70-knot pressure case, separate gust case, maximum floor/weather pressure multiplier, and the inherited weather mass debits.

Joining is two face/core film interfaces plus geometric scarf, splice and edge-seal masses. The retained joining allowance is the larger of actual joining and 5% of faces plus core; structural primer is added separately. Exterior water, contamination, gas floor, heavy mooring pad, systems, optional service mass, added material water and dry sorbent are explicit bill terms.

The one-day gas calculation uses finite nominal and added-water inventories, exponential release, seam leakage, a scarf permeability path, optional vapor capture and the 320 K upper pressure. Internal phase changes do not add vehicle mass again.

For this account, owner thermal tables are **declared inputs**. Independent thermal results were not substituted or used to resize geometries. The comparison recursively visits distinct stored main points and writes every common numeric output field, using `rtol=2e-8, atol=2e-8`.

`account-01` includes the three vacuum bookkeeping differences reported in CHECK. The latest working `account_model.py` proposes using dry-species molecular mass for initial gas and reporting net release after capture. The revised `verify_account.py` also intends to cover supplemental point files. Those changes are unverified because `account-02` was refused before Python started.

## Unexecuted search

`independent_search.py` contains a proposed vector-bisection face solver, dense log-core scan and local refinement, followed by independent common-usage roots. It was never run, tested or used for a result. Its presence is preparation, not evidence. It must not be cited as independent validation of the least sets, E-axis bounds, optimizer completeness or absence of a feasible design.

## Execution and packaging

Each numerical invocation used the one-core simjob route, numerical threads fixed to one, no GPU visibility and isolated environment/scratch. START/END receipts record source hashes, commands and measured times. Three jobs were admitted and released; the fourth was refused for PSI. No post-refusal numerical fallback occurred.

Only text extraction, source reading, artifact copying, SHA-256/schema checks and report assembly followed refusal. Package checks verify custody and report consistency; they do not verify unexecuted scientific code. Original 043 and earlier artifacts are untouched. Times are measured, not a task budget.
