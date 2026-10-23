# MAINLINE-044 calculation method

This is a conditional fatigue and mass screen, tagged **QUESTIONABLE / PROJECTION**. It is not an installed-structure allowable. `life44.py` reads frozen JSON inputs, calculates the spectrum and component stresses, and writes the machine-readable results and figure. No predecessor code is imported or executed.

## Geometry and accounting

The primary point is the **028b full-named point selected by 037**: radius 10 m, two 0.799676344 mm SR200 faces, 22.1067901 mm CR-III 5056 3/8-1.0 core, 30:1 scarves. This differs from 028b's least-usage point. The 037b fix is evaluated at its own filed geometry: 0.794622029 mm faces, 23.2319086 mm core, scarf 30.3413973:1, AF163-2U stress-free at 200°F.

For a panel envelope `a=0.6096 m`, `b=1.8288 m`, lap `l=r*tf`, sphere area `A`:

```
unique seam length L = A * [1/(a-l) + 1/(b-l)]
node count = A / [(a-l)(b-l)]
face mass = 2 A tf rho_f
core mass = A tc rho_c
scarf film mass = 2 L sqrt(l²+tf²) * 0.070 kg/m²
core-splice mass = L tc * 0.0005 m * 500 kg/m³
seal mass = L * 0.002 kg/m
face/core film mass = 2 A * 0.015 lb/ft²
```

A 60:1 scarf changes coverage, seam length, splice and seal mass. It does not add a second full face over the tapered overlap. Procurement waste is outside installed mass. The 100 kg systems allocation and 411.299 kg fixed reserve remain charged. No mass option silently spends those lines.

## Spectrum and stress convention

`SPECTRUM.json` specifies occurrence assumptions. There is no recorded mission/weather histogram. A closed excursion is one cycle; the initial evacuation is one half-cycle. Annual pressure/temperature blocks are treated as separate excursions for Miner bookkeeping. Their actual coincidence and rainflow sequence need measured histories; the combined static check separately envelopes coincident peaks.

The reference keeps the vehicle at or above 500 m and bounds weather to ±100 Pa. This is deliberately restrictive and is not claimed to describe a normal operating year. Separate sea-level descent, +2 kPa weather and 70 kn cases expose the static limit. Flight pressure is represented by the inherited uniform-pressure screen; local aerodynamic bending and vibration are not bounded by this substitution.

Face compression magnitude from external pressure is `pR/(4tf)`. Keeping the full external pressure rather than subtracting the 10 Pa internal starting pressure is slightly conservative. Scalar stress amplitude is half the range; mean is the average of the endpoints. No beneficial compressive-mean correction is credited to Be. Thermal face stress uses the sum of 037's gradient and pattern amplitudes, with the core-induced face-stress range added. The projected opposite night gradient is identified explicitly in the spectrum.

The scarf screen is `tau = sigma_face / (r + 1/r)`. It is mean shear across an ideal scarf, not a local peel/shear solution. HexBond312 fatigue damage is **null**, not zero.

## Three thermal/core models

1. **037 rigid-core screen.** `tau = (alpha_Al-alpha_Be) (T-Tsf) sqrt(Ef tf Gc/tc)`. Changing `Tsf` moves the mean, not the daily range. It is retained to show sensitivity despite 037b's force-equilibrium objection.
2. **037b free-edge screen.** `Kb = Efoil (rho_c/rho_foil)/2`; `tau = sqrt(2 Kb Gc) (alpha_Al-alpha_Be)(Tsf-T)`. This is the filed thermal component. It does not include a complete pressure-induced core-edge stress field. Continuous-field thermal shear being small does not establish zero fatigue at free edges, nodes or hardpoints.
3. **044 coupled free-edge sensitivity.** A common biaxial membrane strain also carries pressure. Define `Kf=Ef/(1-nu)`, `H=2Kf tf+Kb tc`, `N=-pR/2`. Then:

```
epsilon = [(2Kf tf alpha_f + Kb tc alpha_c)(T-Tsf) + N] / H
sigma_f = Kf [epsilon - alpha_f(T-Tsf)]
sigma_c = Kb [epsilon - alpha_c(T-Tsf)]
tau_edge = sqrt(2 Kb Gc) [epsilon - alpha_c(T-Tsf)]
2 tf sigma_f + tc sigma_c = N
```

Pressure contraction can oppose thermal residual core extension. This is why maintaining vacuum and venting it can have quite different core-edge cycles. The formula is a new, unvalidated homogenized boundary model; the force-balance checks do not establish cell-scale accuracy. Its pressure relief is not used to erase the filed 037b static objection. Temperature gradient, local free-edge Poisson effects, pressure load transfer during pumpdown and imperfect bonds remain unresolved. L-direction values use the corresponding shear modulus/strength and L fatigue fit.

## Fatigue laws

For each supported **surrogate** curve, `D = sum(n_i/N_i)` and the repeating-year index reaches one at `365/D_year` days. This is a damage-index crossing, not a probability of failure. The table of years does not include creep, corrosion, crack-size statistics, impacts or uncalculated buckling degradation.

Core data come from the authors' 5.3 pcf 5056 shear tests, not the 1.0 pcf hull product. `CORE-DIGITIZATION.csv` preserves the manually read Fig.10 coordinates and axis transform; `SOURCE-DATA.json` preserves the resulting semilog fits:

```
W: amplitude/static = 1.5892021174 - 0.2132043236 log10(N)
L: amplitude/static = 1.2274834215 - 0.1565713959 log10(N)
```

The measured W range is approximately 0.347–0.861, L 0.206–0.694. The W coupon discussed in the paper failed at 718,394 cycles. Values outside the plotted range are explicitly marked extrapolations. A second `test_horizon_capped_N` field prevents extrapolated life from being confused with demonstrated test duration. A straight semilog extension at low stress remains an assumption, even though its result is finite.

For nonzero core shear mean, this card assumes a Goodman-style transfer:

```
equivalent normalized amplitude = tau_a / [S_static - abs(tau_mean)]
```

That rule is **not validated for this honeycomb**. A mean at/above strength returns no life. A peak above strength is marked as static overload even when the curve can produce a number. Minimum-average catalogue strength is not an A-basis fatigue allowable. ±0.03 vertical curve shifts represent reading/fit sensitivity only, not a statistical confidence interval or the much larger uncertainty in density transfer. The 45° direction is an additional unresolved qualification case.

The Be screening rule assigns `N=10^7` below a 262 MPa alternating stress based on manufacturer-reported smooth S200F tests. It gives no result above that threshold, no infinite-life assertion, and no qualified SR200 result. The AF163 screen similarly uses a 10^7-cycle test horizon for the stated 3M lap-shear runout. Neither proxy qualifies the actual thin film, substrate, mean stress, peel or environment. Assigning all smaller cycles this same horizon is a bookkeeping convention, not a derived S-N slope.

The AF proxy uses gross-area nominal shear. `BOND-CONTACT.json` separately divides this by `rho_core/rho_foil` to expose a bare-wall-foot, no-fillet contact-area sensitivity. This is not a local adhesive stress solution. It demonstrates why the full-area lap-fatigue curve cannot qualify the honeycomb bond without actual wetted contact/fillet geometry.

The mooring-plate calculation interpolates **Yahr's maximum-mean design-curve column** in alternating stress versus log cycles. Its design reductions are already included; Goodman and another factor-of-twenty are not applied again. The baseline 276 MPa peak also exceeds the source's 262 MPa cyclic-yield value, so its nominal 950-day result is an elastic screening index, not a qualified service life.

## Pad resizing

For each simply supported circular plate of radius `a`, uniformly loaded central boss radius `b=25 mm`, load `F`, and Poisson ratio 0.33:

```
t² = 3F [(1+nu) ln(a/b) + 1 - (1-nu)b²/(4a²)] / (2 pi sigma_peak)
mass = number_of_pads * pi a² t * 2700 kg/m³
```

The original six pad areas are `F_total/(6 S_W_typ)`. The larger candidate uses peak shear equal to half of `S_W_min - p/2`; the `p/2` subtraction is an intentionally conservative scalar reservation, not a validated shear/compression interaction law. Resulting area is 0.129063 m² per pad at 20 m/s.

The thickness search targets `10(D_plate + D_pad_core) <= 1` or `<=0.1`. Adding two component damage indices is an extra screening allocation, not a material damage law across components. All candidates pass that **projected** allocation. This depends on low-stress extrapolation of the core curve. If every small core cycle is instead capped at the 718,394-cycle test horizon, the declared 111,730 pad cycles/year exhaust that horizon in about 6.43 years independent of further nominal stress reduction; it does not mean the lower-stress pad physically fails at that time.

The 70 kn pad option applies the same dimensionless occurrence fractions to the larger design load, a separate severe spectrum. It is not a claim that the maximum storm load happens 730 times yearly. Lugs, fasteners, backing, bond fillets and local face/core reinforcements are unpriced.

## Vacuum-cycle reconstruction

034's leak law is resized to the actual 028b seam length and node count. `1 mbar L/s = 0.1 Pa m³/s`; pressure increment is `Q dt/V`. The finite conditioned polymer inventory releases as `B exp(-t/tau)`, with `tau=1 day`. It is not reset at each top-up. The 1-year input retains 034's assumed leak acceptance, polymer gas permeability, 90% conditioning and molecular-weight assignments; none is measured hull performance.

Volume subtracts known face/core and bond/splice solids from the radius-10-m envelope, with core void connected to the interior. This is the alternative displacement convention identified in CHECK-034; seals/ports are not completely modeled. Temperature is 284.9 K for the mass-to-pressure conversion. Thermal gas-pressure swing is a small additional envelope, not a reset of the gas inventory. A full vent also requires a new outgassing/reconditioning assessment; its pressure fatigue excursion is calculated separately here.

The first-year cyclic damage can be repeated as a conservative screening year for the life index. The finite outgassing mass is not interpreted as a new annual gas source. Commissioning damage is recorded separately.

## Reproduction and scope

Run `TMPDIR=unpublished-local-ref:1ffe4110219d37c0 python3 life44.py`. `VALIDATION.json` records 21 numerical checks, including dimensional conversions, inherited geometry/shear/plate values, a source-table ordinate, finite inventory closure and nine coupled-membrane force balances. Five additional assertions check static rejections, nonnegative increments and the resized-pad allocations. The figure was visually inspected. Input and source hashes are checked separately.

These checks verify calculation consistency. They do not convert any **QUESTIONABLE / PROJECTION** into a qualified design.
