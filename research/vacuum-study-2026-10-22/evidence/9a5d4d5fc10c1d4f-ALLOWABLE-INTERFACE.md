# MAINLINE-022b handoff: size-dependent tensile screening and both demands

This implements `ord-admiral-rr2-mainline025-demand-082gpa-1020`. The pinned equilibrium note agrees with the independent family-density derivation in CARD.md. Every supplied material value is **QUESTIONABLE**; all proposed size transfer is **PROJECTION**.

**There is no established compression allowable function.** `qualified_compression_allowable_Pa` and its margin are deliberately null. The available compression figure has no calibrated component-size law, failure distribution or confidence bound. A null value is not zero strength, and it is not permission to substitute a tensile Weibull calculation.

`allowable.py` is standalone Python 3, with only standard-library imports. It has no writes on import. Executing it writes the reproducible example `ALLOWABLE-DEMANDS.json`. The supplied scalar compression cases are explicit caller assumptions; they are not a measured allowable.

**Geometry and the effective stressed size.**

For outer radius \(r_o\), wall \(t\), member length \(L\), and count \(n\):

```text
A = pi [ro^2 - (ro-t)^2]
V_total = n A L
A_surfaces = n 2 pi (2 ro-t) L             # excludes end annuli
Q_eff(m) = integral [(max(sigma(x),0)/sigma_peak)^m dQ]
```

`tube_geometry(ro, t, L, n)` returns those measures and exact annular \(I\). `effective_measure(normalized_positive_stress, measure_weights, m)` integrates a resolved one-direction tensile field. Use the effective size appropriate to **each m**, process and flaw population. The numerical weights must have consistent m³ or m² units. The function does not implement a general multiaxial fracture criterion, contact mechanics, surface/edge competition or time-dependent degradation.

For a coupon characteristic stress \(s_c\), calibrated effective reference measure \(Q_\mathrm{ref}\), and specified one-exposure failure target \(P\):

```text
sigma_target = sc [-ln(1-P) Q_ref / Q_eff]^(1/m)
```

Call `weibull_threshold(sc, m, Q_ref, Q_eff, P)`. The result is a **conditional peak tensile stress**, not an axial compression allowable. At zero positive tensile exposure the function returns `None`; zero tensile hazard does not prove compressive survival.

`sa_illustrative_calibration(m, "volume" or "surface")` provides the two documented **hypotheses**, m=8 and m=10. It assumes typical 380 MPa is a mean and assumes 40/20 mm loading spans on the manufacturer's 3×4×45 mm bend bars. Neither assumption is established for that dataset. It derives \(s_c=\bar{s}/\Gamma(1+1/m)\) and the stress-weighted beam reference measure; all values and source limitations are in `research/reliability.json`.

For a uniform volume field, geometry dependence is explicitly:

```text
sigma_target(ro,t,L,n)
  = sc [-ln(1-P) V_ref / (n pi(2ro*t-t^2)L)]^(1/m)
```

Doubling member count or uniformly stressed volume multiplies this stress by \(2^{-1/m}\). The full-surface expression follows by substituting its effective reference area and total surface area. Independent, separately calibrated populations require **adding hazards**, not choosing the strongest allowable or reusing one bend fit as two independent fits. Commercial CVD m=11, β=424 MPa cannot be scaled without its missing effective reference measure.

**Example for 022b.**

```python
from allowable import tube_geometry, sa_illustrative_calibration, weibull_threshold

g = tube_geometry(0.12368836237368608, 0.0008802990936851718, 2.04, 1047)
c = sa_illustrative_calibration(10, "volume")  # PROJECTION, not calibrated product
Ft_uniform_example = weibull_threshold(
    c["characteristic_stress_Pa"], c["m"], c["reference_measure"],
    g["total_volume_m3"], 1e-6,
)
Fc_qualified = None
```

A resolved nonuniform stress calculation replaces `g["total_volume_m3"]` with its correctly weighted effective volume. A small contact hot spot is not the whole tube volume; its local peak, principal directions and surface/volume/edge populations must actually be resolved. A tube-count change during optimization must update the array's total hazard.

**Both force rules are explicit.** `member_demand` takes a required `force_factor`, with \(N=\text{factor}\,pRs/2\). Use \(1/\sqrt3\) for the uniform equilateral equilibrium correction and 1 for the legacy two-way comparison. At the original physical tube:

| Quantity at full pressure | Equilateral \(pRs/(2\sqrt3)\) | Legacy \(pRs/2\) |
|---|---:|---:|
| Mean compression | 0.824658 GPa | 1.428350 GPa |
| End force | 0.562166 MN | 0.973701 MN |
| Qualified compression allowable | unknown | unknown |

The module computes amplified bending and both signed face stresses separately, using the stated \(a_0=L/1000\) bow. It refuses finite prebuckling stresses when \(N\ge N_E\). Arbitrary extra arc rise must not reduce the equilibrium force: it can add bending relative to the actual thrust line, as the pinned note explains. Node spacing and physical member length are separate inputs to allow an explicit arc-length correction.

`assumed_compression_capacity(Fc, demand)` gives the elastic extreme-compression pressure multiplier for a **caller-assumed** positive \(F_c\). It excludes tensile failure, contact, local/global instability, film and mass feasibility. `research/model-results.json` supplies the full reoptimized surrogate tables for both demands, including those additional scored modes; none is a qualified structural safety factor.

For contact screening only, `ALLOWABLE-DEMANDS.json` gives \(C_t=\sigma_\mathrm{t,example}/(N/A)\) under each demand. \(C_t\) is a positive principal tensile stress ratio, not a compressive bearing-pressure coefficient. No actual node \(C_t\) is known.

**Remaining coupling.** Film sag and its lost lift are not charged by the inherited fixed mass budget. The pinned equilibrium note assigns that correction to MAINLINE-024/022b; these results are explicitly conditional on the original lift ceiling. Geometry, joint mass, environment, proof testing and full-size compression/contact statistics still require their own evidence. Open issues are enumerated in `NFI.json`.
