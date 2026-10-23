# CHECK-059 method and independence

Order: ord-admiral-rr2-check059-codex-7e53-1020. Owner report:
rpt-ref-4fb99766fa9a4406a85a.

The pinned JSON/Markdown boundary specifications supplied the equations and parameter choices. Owner and predecessor executable files were excluded before copying; EXCLUDED.json records their paths without reading or hashing them. The only reused executable material is this seat's own independently written CHECK-053 thermal/mechanical equations, frozen under intake/own053. This seat's independently calculated MAINLINE-052 data supplies the P3 bill.

Every scientific invocation used `python3 tools/simjob.py run --cores 1 --mem 1G -- ...` through admit.py. Execution receipts include actual times, commands, current local source hashes, limits, status and reservation release. Thread counts were one; scratch was unpublished-local-ref:4e9ac4eadc1acd97. No refusal occurred. No seat was contacted or woken.

## Drops, films and transfer

`liquid_check.py` derives spherical-cap volume from base radius and contact angle, applies the stated Furmidge balance, and calibrates its population multiplier against 54 g/m². It independently implements the Jeffreys rain film and Nusselt condensation film. Rain coverage ends at 135 degrees, films are applied above the equator, and the 0.8 kg/m² cap is retained as a declared assumption.

It solves the monotonic surface energy residual by bisection. The heat/mass relation uses Le=0.845, cp=1005 J/kg/K, air density 1.2 kg/m³ and vapor gas constant 461.5 J/kg/K. The sphere branch takes the maximum of the specified forced and natural terms. The second branch uses 5.7+3.8U. Magnus saturation is 610.94 exp(17.625 Tc/(243.04+Tc)) Pa. Latent heat is 2.45 MJ/kg.

The 36×72 angular midpoint convention reproduces DRY, including the distinction between normalized mean rate and the unnormalized midpoint hull integral. RETAIN uses 0.5-degree polar points. Its dew profile is reproduced by interpolating positive condensation **after** clipping on the 5-degree polar grid; all five finishes inherit the mirror's .8 emittance. P3 retains all deposited dew in the top 14-degree cap. Those implementation conventions were inferred from non-executable output fields, then explicitly recorded; no source code was inspected.

`local_drying.py` independently integrates m(beta,phi,t)=max(m0−E*t,0) under held weather, without redistribution or runoff. A dry patch contributes no further evaporation. Negative E adds water. It provides both the bulk M/E equivalent and local inventories, with 1-degree and 0.5-degree checks. The 99% removal time is more meaningful than the last polar trace, which is grid-sensitive. Neither is an operating guarantee.

## Ponds

For a side-one equilateral triangle, vertices are (0,1/sqrt(3)), (−1/2,−1/(2sqrt(3))) and (1/2,−1/(2sqrt(3))). The charged cap crown ratio is c=1−sqrt(11/12). Its circular mean/crown is 1/2+2c². Bay side is inferred independently from the 73.1007331152853 kg sag debit at R10 and ISA density 1.16726833074618 kg/m³.

The declared triangular dish is d=k*c*t*(2−t), t=3min(lambda). Uniform area gives density 2(1−t), with mean t(2−t)=1/2. Therefore continuous k=2×0.503624902308. Boundary-inclusive equal weighting of a barycentric grid with 301 divisions reproduces the filed k=1.0173672190414051; this is not continuous area quadrature.

`pond_check.py` divides the triangle into the three regions having a specified smallest barycentric coordinate. For each t, depth is linear along the remaining strip, so the integral of its positive part and its wetted fraction are analytic. Only t is numerically integrated. For tilt beta and uphill direction x, water depth normal to the bay is max(d−tan(beta)*(x−xmin),0). Gauss orders 192 and 384 check the averaged profile; 768 checks named placements. An independent two-dimensional Duffy/Gauss integral in `pond_validation.py` verifies nine cases, including directional retention at 14 and 16 degrees.

The explicit planar tiling contains one upward and one downward triangle per primitive cell, each counted once. Their orientations are retained. Tilt is atan(distance/R), with height increasing toward the chosen hull-top point. A 32×32 deterministic translation grid supplies a reproducible distribution; exact node and bay top points are additional witnesses. This is an independently specified surrogate, not the real f5 mesh and not the owner's unspecified 200 random placements. Model/sampling differences are labeled accordingly.

All 201 published angular ordinates are compared. `pond_grid_check.py` explores plausible unspecified azimuth/weight conventions as diagnostics; a best-fitting convention is not declared to be the owner's implementation. It resolves the level normalization, but does not establish the named placement statistics.

For a falling free surface under constant uniform evaporation, complete drying depends on the maximum vertical depth, not the initial volume divided by initial surface area. The supplied pond-time alternatives are deliberately conditional on constant top-point flux.

## Capacity and cost

`capacity_check.py` enumerates 16 endpoint masks at five radii and two weather cases, then re-solves each of 37 least-set rows. It uses the independent historical thermal boundary conventions and extends the tables to R20/R30 with the same 241-point thickness grids and independent face-balance solver. Cure is included in global and crimp loads; actual joining has no 5% floor; bake and mirror coating are included. That exact bill matters when comparing other cards.

Exterior water shifts the mass bill linearly: capacity = 0.1 + endpoint payload/(4πR²). The 185 comparisons retain signed deltas; absolute payload tolerance is 0.003 kg and capacity tolerance 3e−6 kg/m². Least usage tolerance is 5e−6. P3 comparisons allow 0.0005 kg for the owner's three-decimal payload rounding.

`water_check.py` independently recomputes 722 account, waiting-time and method fields. The two identified cost differences are intentional findings, not waived failures. Two coating layers cost 2*A/23*3.8/(50*3.785411784)*7685.90 under the owner's equal-price projection. Counting both dry layers similarly doubles its mass range. Heater, fabric, energy and floor-area unit conversions are retained separately from their unqualified installation assumptions.

## History and limits

Initial probes resolved air density, azimuth midpoints, clipped interpolation, cure and joining conventions. The first capacity run encountered an absent R20 historical table; independent tables were added. A pond diagnostic completed its calculation but failed while printing a NumPy integer; scalar conversion corrected it. Receipts and logs preserve these events. No computation bypassed admission.

Arithmetic agreement is not physical qualification. MISMATCHES.json distinguishes source/application errors, interpretation errors, continuum/discrete differences, and alternative-model non-reproduction. NFI.json gives a concrete next measurement or calculation for every objection and carries the owner's 12 rows unchanged.
