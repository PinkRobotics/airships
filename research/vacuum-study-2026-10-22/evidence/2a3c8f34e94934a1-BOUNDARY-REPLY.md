# CHECK-048: exact filed thermal conventions

QUESTIONABLE / PROJECTION. Response to `q-ref-645bd2bebe189705b552`. This is an equation and convention clarification of the existing 040/048 calculations. No numerical model was rerun and no code is supplied.

The stated checker setup differs from the filed owner boundary in at least one explicit respect: the owner uses **the maximum of forced and local natural convection**, rather than a constant forced coefficient. Also retain the **additional radiative conductance in U**. These differences are candidates for the discrepancy; this clarification does not assert that they quantitatively explain every differing cell. A small residual establishes convergence to the equations being solved, not equivalence between two boundary models.

The earlier filed [THERMAL-BOUNDARY.md](ebbb59a4bf12cd7c-THERMAL-BOUNDARY.md) gives the same physical equations. The iteration, averaging and legacy details below complete the requested specification.

## Environment and convection

Let μ = cos θ, with μ = 1 sunward/upward in the imposed axisymmetric case. All temperatures are kelvin. The fixed table environment is:

| Quantity | Value |
| --- | ---: |
| Air and ground temperature, Ta | 284.9 K |
| Air density | 1.1672683307461802 kg/m³ |
| Air speed, v | 2 m/s |
| Air dynamic viscosity, η | 1.79 × 10⁻⁵ Pa·s |
| Air conductivity, ka | 0.0257 W/(m·K) |
| Prandtl number | 0.71 |
| Stefan–Boltzmann constant, σ | 5.670374419 × 10⁻⁸ W/(m²·K⁴) |
| Day solar flux / sky temperature | 970 W/m² / 275 K |
| Night solar flux / sky temperature | 0 / 260 K |

Ground remains at Ta in both cases. The local sky and ground fractions are **(1+μ)/2** and **(1−μ)/2**:

$$
T_{\mathrm{env}}^4(\mu)
=\frac{1+\mu}{2}T_{\mathrm{sky}}^4
+\frac{1-\mu}{2}T_a^4,\qquad
q_{\mathrm{solar}}=\alpha_o S\max(\mu,0).
$$

The forced-convection characteristic length is **D = 2R**:

$$
\mathrm{Re}=\frac{\rho vD}{\eta},\qquad
h_f=\left[2+\left(0.4\sqrt{\mathrm{Re}}
+0.06\mathrm{Re}^{2/3}\right)\mathrm{Pr}^{0.4}\right]\frac{k_a}{D}.
$$

There is no additional viscosity-ratio multiplier. At each surface location:

$$
h_n=1.32\max(|T_o-T_a|,0.05)^{1/4},
\qquad h=\max(h_f,h_n).
$$

The natural-convection branch depends on the current **outer** temperature. These fixed air properties and temperatures do not change when a separate 031 weather/lift-reserve row is selected.

## Inner mean, conductance and balances

Use the normalized spherical area average

$$
\langle f\rangle=\frac12\int_{-1}^{1}f(\mu)\,d\mu
\simeq\frac12\sum_i w_i f_i.
$$

The current quadrature weights sum to 2. In particular, **⟨Ti⁴⟩ and ⟨Ti⟩⁴ are different quantities**. The inner emissivity εi is 0.20:

$$
q_i=\epsilon_i\sigma\left(T_i^4-\langle T_i^4\rangle\right).
$$

There is no external heat sink added to this inner balance. The mean exchange is zero at a converged enclosure state. The through-core relation is:

$$
U=\frac{130(\rho_c/\rho_{\mathrm{Al}})}{t_c}
+0.20(4\sigma)\langle T_i\rangle^3,
\qquad T_o=T_i+\frac{q_i}{U}.
$$

Here ρc = 16.018463373960138 kg/m³. The **common 040/048** tables use ρAl = 2700 kg/m³; the historical 037 comparison uses **2640 kg/m³**. The second term in U uses the cube of the arithmetic area mean Ti, not ⟨Ti³⟩. Its coefficient is the inherited gap value 0.20, with no replacement by a two-surface effective-emissivity expression. This term and the enclosure exchange qi are both present in the filed approximation; neither should be silently omitted when reproducing it.

The outer balance, with positive qi flowing from the outer skin toward the inner enclosure, is:

$$
\epsilon_o\sigma(T_o^4-T_{\mathrm{env}}^4)
+h(T_o-T_a)+q_i-\alpha_o S\max(\mu,0)=0.
$$

For `reference040`, αo = 0.20 and εo = 0.90. Other 048 rows use their own filed coating pair; the selected multilayer row uses 0.09/0.80. Inner εi stays 0.20.

## Current and legacy iteration conventions

The current 040/048 calculation begins with Ti = Ta at every node. At each enclosure iteration it evaluates ⟨Ti⁴⟩ and ⟨Ti⟩ from the previous complete temperature vector, forms U, and holds these quantities fixed while solving all local balances. All new Ti values replace the previous vector together, without relaxation.

The local solve uses Newton updates, at most 12 per enclosure iteration, stopping when the maximum absolute temperature update is below 10⁻¹⁰ K. The derivative includes the local natural-convection dependence. If Δ = To−Ta, the derivative of hΔ with respect to To is h + h/4 when the natural branch strictly governs and |Δ| > 0.05 K; otherwise it is h. The enclosure iteration stops when the maximum change in Ti is below 2 × 10⁻⁹ K, with a limit of 500 iterations. After stopping, the means, U and To are recomputed from the final Ti vector, and the residual is evaluated again.

Current tables use **128-point Gauss–Legendre quadrature**. Day maximum and night minimum are extrema among those nodes, not extrapolated values at μ = ±1.

The **original 037 legacy** calculation uses 37 equal-area midpoint nodes, μj = −1 + 2(j+1/2)/37 for j = 0…36. It starts at Ta, performs **25 enclosure updates**, holds the previous arithmetic means fixed during each local solve, and replaces all nodes together without relaxation. Each local root is solved by bisection on the initial 180–900 K bracket, with 80 bisection steps. It does not use a convergence-based enclosure stopping test. The owner’s later “legacy” diagnostic reproduces the midpoint/25-update/2640-density conventions using its current local root solver; that diagnostic is distinguished from the original implementation.

## Mean removal and reported structural temperatures

Mean removal belongs to the structural projection, **not to the absolute temperatures in the radiation balances**. Let Tpattern = (To+Ti)/2. The current projection first subtracts its own spherical mean:

$$
c_j=\frac{2j+1}{2}
\int_{-1}^{1}\left(T_{\mathrm{pattern}}-\langle T_{\mathrm{pattern}}\rangle\right)
P_j(\mu)\,d\mu,\qquad j=2,\ldots,6.
$$

Only degrees 2–6 contribute to curvature. The current amplitude is the maximum absolute second θ derivative of their sum, sampled at 1441 evenly spaced θ values from 0 to π. For each polynomial, the derivative is

$$
\frac{d^2P_j(\cos\theta)}{d\theta^2}
=(1-\mu^2)P_j''(\mu)-\mu P_j'(\mu).
$$

The original 037 midpoint projection applied the degree coefficients to the **unsubtracted absolute** Tpattern, then omitted degrees 0 and 1 from the curvature reconstruction. Midpoint quadrature can consequently leak a constant-temperature contribution into degrees 2–6. It used 721 angular samples with interior finite differences for curvature. The later owner legacy diagnostic keeps the unsubtracted midpoint projection but uses the current analytic derivative and 1441-angle sampling; it is not an exact replay of that final historical differentiation step.

040 uses the **daytime** maximum |To−Ti| and daytime curvature. 048 uses the larger **day/night** gradient and curvature. Both report hottest daytime To, coldest nighttime To, and their full swing. The reference040 comparison point happens to have a larger daytime gradient and curvature.

The 241-point log-thickness table and the later 1.002 structural interpolation guard are separate from the direct boundary solution. Do not apply that guard to the direct temperature extrema in the following reference.

## Already-filed reference values

At R = 10 m, tc = 0.02210679007353296 m and reference040 optics, the common 2700-density, 128-point direct result is:

| Quantity | Filed value |
| --- | ---: |
| Day maximum outer temperature | 302.02481753419386 K |
| Night minimum outer temperature | 270.90519361594414 K |
| Day maximum face gradient | 0.4227611395799613 K |
| Night maximum face gradient | 0.17808366814682586 K |
| Day curvature-temperature amplitude | 55.77743433326896 K |
| Night curvature-temperature amplitude | 0.8066049556018386 K |
| Day / night enclosure iterations | 13 / 13 |
| Day / night maximum energy residual | 7.2500938586 × 10⁻¹⁰ / 5.5719340253 × 10⁻¹⁰ W/m² |

[REFERENCE-VALUES.json](9083450a5982f932-REFERENCE-VALUES.json) copies the already-filed diagnostics with exact source selectors. These values were not regenerated for this reply. Natural convection, the inherited conductance approximation, physical boundary selection and independent thermal reproduction remain subject to the existing NFIs.
