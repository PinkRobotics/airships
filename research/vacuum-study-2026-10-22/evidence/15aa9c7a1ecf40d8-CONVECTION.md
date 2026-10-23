# CHECK050: night convection and heating conventions

Reply to `q-ref-4e244447c124739f6c92`.
This is an equation-only clarification of the filed MAINLINE050 calculation.
It supplies no owner implementation. Physical predictions retain their
QUESTIONABLE / PROJECTION qualification.

## Ambient properties

All temperatures in the following expressions are in kelvin. Let
`c = T - 273.15` and define saturation vapor pressure over liquid water by

```text
es_w(T) = 611.21 exp[(18.678 - c/234.5)c/(257.14 + c)] Pa
ea      = RH_water es_w(Ta)
rho_air = (P0 - 0.378 ea)/(RD Ta)

P0 = 95460.83791390515 Pa
RD = 287.053 J/(kg K)
dynamic viscosity = 1.79e-5 Pa s
air conductivity  = 0.0257 W/(m K)
Prandtl number     = 0.71
```

RH is relative to liquid water, including the cold frost case. Ambient
density is evaluated once for each night from its ambient temperature and
humidity. Conductivity, viscosity and Prandtl number are fixed: there is no
film-temperature property update or surface/ambient viscosity correction.

## Forced and natural coefficients

For radius `R` in metres and wind speed `v` in metres per second:

```text
Re       = rho_air v (2R)/(1.79e-5)
h_forced = 0.0257/(2R) [2 + (0.4 Re^(1/2) + 0.06 Re^(2/3)) 0.71^0.4]
h_natural(To) = 1.32 [max(abs(To - Ta), 0.05)]^0.25
h(To)    = hscale max(h_forced, h_natural(To))
```

The coefficients `h` are in W/(m² K); the numerical temperature difference
in the natural-convection correlation is in kelvin. Its floor is **0.05 K**.
For the transient, `To` is the old outer-skin temperature at each surface
quadrature point. The baseline has `hscale = 1`; sensitivity values 0.5 and 2
multiply the result after selecting the larger coefficient.

The following scalar values use `R = 10 m`. Full precision is also recorded
in `SCALAR-REPLAY.json`.

| Case | Ta (K) | RH_water | v (m/s) | rho_air (kg/m³) | Re | h_forced (W/m² K) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| clear_calm_reference | 284.9 | 0.7188468865165529 | 0.2 | 1.1626849926452072 | 259817.87545144293 | 0.504764407668066 |
| overcast_humid | 284.9 | 0.95 | 0.5 | 1.161211169927102 | 648721.3239816211 | 0.8673661151960881 |
| clear_saturated | 284.9 | 1 | 0.2 | 1.1608923719892559 | 259417.2898300013 | 0.5043067856535622 |
| clear_cold_frost | 268.15 | 0.9 | 0.2 | 1.2383173742793985 | 276718.9663194186 | 0.5238238227844538 |
| dry_reference_regression | 284.9 | 0.7188468865165529 | 2 | 1.1626849926452072 | 2598178.7545144293 | 1.995593683812325 |

## Meaning of the dry comparison

Disabling condensation in the night transient sets deposition flux to zero.
It retains the default ambient humidity:

```text
RH_water = es_w(280)/es_w(284.9) = 0.7188468865165529
Ta = 284.9 K; Tsky = 260 K; v = 2 m/s
time step = 2.5 s; surface quadrature = 128 Gauss-Legendre points
```

Consequently the dry night comparison still uses humid-air density
`1.1626849926452072 kg/m³`. The inherited steady dry thermal calculation
uses the fixed reference density `1.1672683307461802 kg/m³`. These are
distinct convection inputs. This clarification does not establish which
input caused the checker's small temperature or deposition residuals;
that requires comparing the checker's own equations and constants.

## Heating quadrature

The water dew point is obtained with 60 bisections on `[200 K, Ta]`.
The uniform heating target is
`Tstar = max(Tdew, 273.15 K) + 0.05 K`.
At this target, evaluate convection with the same formula above. With
`epsilon = 0.8`, `sigma = 5.670374419e-8 W/(m² K⁴)` and surface coordinate
`mu` in `[-1, 1]`, the positive heating requirement is

```text
a = epsilon sigma [Tstar^4 - (Tsky^4 + Ta^4)/2] + h(Tstar)(Tstar - Ta)
b = epsilon sigma (Ta^4 - Tsky^4)/2
q(mu) = max(a + b mu, 0)
area mean = (1/2) integral[-1,1] q(mu) dmu
```

For `b > 0`, this exact mean is zero if `a <= -b`, `a` if `a >= b`,
and `(a+b)^2/(4b)` otherwise. The filed value uses the 128-point
Gauss-Legendre quadrature with weights divided by two.

For `R = 10 m`, clear calm reference:

| Quantity | Value |
| --- | ---: |
| Tstar | 280.05 K |
| a | 16.444702511883182 W/m² |
| b | 45.78228205593695 W/m² |
| Filed 128-point quadrature mean | 21.1451220230001 W/m² |
| Exact positive-part integral | 21.144629726368056 W/m² |
| Quadrature minus exact mean | 0.0004922966320428657 W/m² |

The checker's analytic mean agrees with the exact integral. Both round to
21.1 W/m² at one decimal place. This addendum identifies the quadrature
difference and leaves the original sealed numerical record intact.
