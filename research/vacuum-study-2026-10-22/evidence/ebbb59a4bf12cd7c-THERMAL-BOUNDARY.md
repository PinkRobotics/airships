# Existing 040/048 temperature-table boundary, in non-code form

PROJECTION. This specifies what the already filed owner solver computes. It does not establish the real hull boundary or close CHECK-040's independent reproduction finding.

Let μ=cosθ on a sphere, with μ=1 sunward/upward in the imposed axisymmetric model. The sphere diameter is 2R. Air temperature is 284.9 K, density 1.1672683307461802 kg/m³, speed 2 m/s, viscosity 1.79×10⁻⁵ Pa·s, conductivity 0.0257 W/(m·K), and Pr=0.71. The temperature table uses these values even when a different 031 buoyancy/weather reserve is selected.

`Re = ρ × 2 × (2R) / μ_air`

`h_forced = [2 + (0.4 sqrt(Re) + 0.06 Re^(2/3)) Pr^0.4] × 0.0257/(2R)`

At each location, with outer-face temperature To:

`h_natural = 1.32 max(|To − Ta|, 0.05)^0.25`

`h = max(h_forced, h_natural)`

In particular, this is **not a constant forced-convection-only coefficient**. CHECK-040's stated alternative uses the forced term. This difference is visible in the boundary assumptions; its full numerical consequences have not been independently closed here.

Day forcing is 970 W/m² sun with sky 275 K. Night forcing is zero sun with sky 260 K. Ground stays at air temperature. The radiative environment fourth-power temperature is:

`Tenv⁴(μ) = (1+μ)/2 × Tsky⁴ + (1−μ)/2 × Ta⁴`

`q_solar(μ) = α_outer × S × max(μ, 0)`

Outer α/ε come from the selected 048 coating row. Inner ε is 0.20. Let Ti be the inner-face temperature, with sphere-average quantities `mean(Ti)` and `mean(Ti⁴)` from normalized Gauss weights. The code uses:

`q_inner = 0.20 σ [Ti⁴ − mean(Ti⁴)]`

`U = (130 × ρ_core/ρ_Al)/tc + 0.20 × 4σ × mean(Ti)³`

`To = Ti + q_inner/U`

`ε_outer σ [To⁴ − Tenv⁴] + h(To−Ta) + q_inner − q_solar = 0`

Here σ=5.670374419×10⁻⁸ W/(m²·K⁴), ρ_core=16.018463373960138 kg/m³ and ρ_Al=2700 kg/m³ for current tables. The historical 037 comparison uses 2640 kg/m³. The explicit extra term in U is part of the inherited approximation; it should not silently disappear when independently reproducing the table. Its physical adequacy remains a model question.

The solver iterates the inner enclosure mean and the local nonlinear balances. Current tables use 128-point Gauss-Legendre quadrature, local update tolerance 10⁻¹⁰ K and enclosure update tolerance 2×10⁻⁹ K. Local energy residuals and iterations are saved. Direct 256-point checks are numerical convergence checks of these same equations.

The structural temperature pattern is `(To+Ti)/2`. Its spherical mean is removed before projecting Legendre degrees 2 through 6:

`c_j = (2j+1)/2 × integral[-1,1] (Tpattern−mean(Tpattern)) P_j(μ) dμ`

The reported curvature-temperature amplitude is the maximum absolute second derivative with respect to θ of this degree-2-to-6 expansion, sampled at 1441 evenly spaced θ values from 0 to π. The 048 table uses the larger day/night curvature and face gradient; 040 used the daytime versions. Both include the night minimum in the cure reference.

The hottest daytime To and coldest nighttime To define extrema; their difference defines full swing. The tabulated core-thickness grid has 241 log-spaced values per radius. Structural stress terms use log-thickness interpolation with a 1.002 guard; the guard is not a statement of physical-boundary accuracy.

The independent check's old-geometry differences remain in THERMAL-CLOSURE.json [source link unavailable in this public projection]. Independent reproduction from this complete statement, and selection/validation of the actual combined weather/thermal/wetting boundary, remain open.
