# CHECK050: 24-hour gas supplement conventions and scope correction

Reply to `q-ref-c57caca0c9aba79b98d3`.
This is an equation-only description of the filed MAINLINE050
`SUPPLEMENTAL-RESULTS.json` field `gas_24h_bounds`.
It supplies no owner implementation. The result remains
QUESTIONABLE / PROJECTION.

## Geometry selection and corrected scope

For each radius `R = 10, 12, 15, 20, 30 m`, the supplement samples **32**
geometries: all 16 masks, usage 1, at the first and last pressure knots of
the frozen-thermal family in `MASS-CURVES.json`. That family uses ambient
temperature 284.9 K. The pressure array contains 65 knots; the selected
indices are 0 and 64, corresponding to 97172.30184301017 and 106500 Pa.
The sample has no nonnegative-payload filter.

For each candidate, the equations below combine conservative gas
temperature and external-pressure assumptions. The stored row is the
candidate with the largest calculated **gas pressure**. Mass, connected
volume and inventory are taken from that same row. The selection is not
defined as an independent maximum-mass optimization; in this particular
32-row sample, the maximum-mass candidate is also the maximum-pressure
candidate at every radius.

The 24-hour supplement therefore establishes conditional results for
these sampled frozen-thermal geometries. **It does not establish a bound
over every coupled-weather geometry.** Any earlier description extending
this supplement to all coupled-weather geometries is narrowed by this
addendum. The checker's reported 8,432 finite coupled geometries per radius
are a different sample. Their reported R10 mass of 3.216712 kg cannot be
compared as an identical-input replay of the filed 3.192390 kg row. This
addendum does not independently audit that wider sample.

## Geometry and physical component masses

Let `tf` be one face thickness and `tc` the core thickness, in metres.
For each sampled geometry:

```text
A  = 4 pi R^2
V0 = 4 pi R^3/3
s  = 30.34139731914874
ell = s tf
L  = A [1/(0.6096 - ell) + 1/(1.8288 - ell)]
rho_core = 16.018463373960138 kg/m^3
f0 = 0.030 * 0.45359237 / 0.3048^2 kg/m^2

Mface   = 2 A tf * 1850
Mcore   = A tc rho_core
Mfilm   = 2 A f0 * (0.5 if mask bit 8 is set, otherwise 1)
Mscarf  = 2 L sqrt(ell^2 + tf^2) * 0.070
Msplice = L tc * 0.0005 * 500
Mseal   = 0.002 L
Mprimer = 0.010 A
Mcoat   = 0.00833272 A
```

`L` is the unique joint length in metres and all `M` values are kilograms.
The numerical density factors are kg/m³ and areal-density factors kg/m²,
except the seal factor 0.002 kg/m. The gas calculation uses these physical
component masses. It does not replace them with a charged joining
allowance such as the larger of actual joining mass and 5% of face-plus-core
mass.

## Connected volume

```text
Vc = V0
     - Mface/1850
     - Mcore/2700
     - (Mfilm + Mscarf + Mseal)/1250
     - Msplice/500
```

`Vc` is in m³. The core subtraction is the core's metal volume, so this
expression assumes that core pores communicate with the cavity. It does
not subtract the whole bulk core envelope. Primer, coating, pads and
systems have no additional displacement terms in this expression.
This is an assumed connected volume, not a measured volume.

## Conditioned finite release inventory

The retained absorbed-water inventory `W` and complete internal release
inventory `I`, in kg, are

```text
W = 0.1 [0.002 Mfilm + 0.001 Mcore + 0.01 Mprimer + 0.01 Mcoat
         + 0.01 (Mscarf + Msplice + Mseal)]

I = 0.1 [0.0485 Mfilm + 0.001 Mcore
         + 0.01 (Mscarf + Msplice + Mseal)] + W
```

The factor 0.1 is a projected 90% conditioning removal. The two written
inventory contributions are additive; in particular their core terms
are not deduplicated. The full finite `I` is released for this bound and
is assigned water molecular mass `0.01801528 kg/mol`. There is no
one-day exponential-release fraction and no additional core-pore
storage inventory. Exterior water film is a separate mass bill and is
not added to this internal inventory.

## Initial gas, leakage and scarf diffusion

Use `Rg = 8.31446261815324 J/(mol K)` and `t = 86400 s`.
The initial pressure is 10 Pa. Both its mole conversion and the leak
throughput conversion use 258 K:

```text
n0    = 10 Vc/(Rg * 258)
Qleak = (0.001 L + 0.01) mbar litre/s
nleak = (0.001 L + 0.01) * 0.1 * 86400/(Rg * 258)
```

The factor 0.1 converts one mbar litre to Pa m³.
Scarf permeation uses one outer seam cross-section:

```text
Adiff = L * 0.070/1250
ddiff = s tf
nperm = 10 * 3.34645e-16 * (Adiff/ddiff) * 106500 * 86400
```

`Adiff` is in m² and `ddiff` is in m. The permeability assumption is
10 Barrer, with conversion
`3.34645e-16 mol m/(m² s Pa)` per Barrer. The full 106500 Pa is applied
as the diffusion driving pressure, without subtracting internal pressure.
There is no extra factor of two in `Adiff`: scarf mass includes two faces,
but this gas path is the outer seam. There is no full-area bondfilm
permeation through intact metal.

Initial gas, leak gas and permeating gas all use the lumped air molecular
mass `0.029 kg/mol` for the mass bill. The supplement does not use a
species-resolved incoming humidity mixture. The finite internal release
inventory alone is assigned water molecular mass in the pressure
calculation.

## Final pressure and mass

```text
p24 = (n0 + nleak + nperm + I/0.01801528) Rg * 326/Vc
m24 = 0.029 (n0 + nleak + nperm) + I
```

Thus the pressure calculation combines initial/leak mole conversion at
258 K with final gas temperature 326 K. It is a conservative combination
within the stated inventory and geometry assumptions, rather than a
time-resolved weather history.

The comparisons are `p24 < 800 Pa`, where `800 = 0.01 * 80000 Pa`, and
`m24 <= 0.01 * 4889.442150186961 * (R/10)^3 kg`.

## Scalar reproduction of the filed rows

Direct scalar evaluation of these equations over the 160 existing input
geometries reproduces all five filed pressure, mass, connected-volume
and inventory values exactly at the recorded floating-point precision.
It performs no new geometry optimization or weather transient and
does not execute owner implementation modules. These are owner
clarification checks, not a substitute for the checker's independent
implementation.

All five selected candidates have mask 2, pressure-knot index 64 and
design pressure 106500 Pa:

| R (m) | tf (m) | tc (m) | Vc (m³) | I (kg) | p24 (Pa) | m24 (kg) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 0.000906562090079837 | 0.06897709869910812 | 4185.591127578047 | 2.2917216606431747 | 102.49116931015585 | 3.1923896191733703 |
| 12 | 0.0010884197613220958 | 0.08274576072147953 | 7232.784429737846 | 3.416369200710219 | 89.97636512864531 | 4.879627277159516 |
| 15 | 0.0013614730709300854 | 0.10338572728725696 | 14126.691320284228 | 5.612230609934515 | 77.48393151095745 | 8.289089519198495 |
| 20 | 0.0018171086197073284 | 0.1377590597710054 | 33485.855714158104 | 10.797739569493672 | 65.03418359961825 | 16.715781587945543 |
| 30 | 0.00273011302533012 | 0.20642163554002388 | 113015.89217875218 | 28.062819821425457 | 52.695997360861895 | 46.60702621821409 |

The R10 decomposition is:

```text
L       = 2856.4531921187704 m
W       = 0.3014858053027727 kg
n0      = 19.51205047130818 mol
nleak   = 11.545286267247546 mol
nperm   = 0.00017907283032443219 mol
Adiff   = 0.15996137875865116 m²
ddiff   = 0.027506360569590244 m
```

`SCALAR-REPLAY.json` records the remaining component masses, every selected
row's decomposition, zero differences from the filed values and the
non-code input hashes. This clarification leaves the original sealed
artifacts intact and explicitly limits the supplement's geometry scope.
