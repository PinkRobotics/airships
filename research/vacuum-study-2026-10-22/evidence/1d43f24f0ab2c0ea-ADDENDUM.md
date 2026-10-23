# CHECK050 addendum: convection and scoped gas reproduction

The independent scalar replay reproduces all five originally filed gas rows with **zero recorded differences** in pressure, gas mass, connected volume and release inventory. It evaluates all 160 supplied geometries using a new checker implementation of the owner's equation-only clarification. The original CHECK050 package remains sealed; this addendum resolves its pending numerical-convention question.

The received authority is `rpt-1228-check050-convection-gas-conventions-1020`, answering the checker's two queued questions. Its five artifact pins were verified before reading. Only non-executable owner inputs were accessed.

## Gas result and corrected scope

The sample consists of 16 masks at pressure-knot indices 0 and 64 for each radius, with frozen thermal conditions at 284.9 K and usage 1. The two design pressures are 97172.30184301017 and 106500 Pa. There is no payload filter. Each reported result selects the greatest calculated gas pressure and carries that candidate's mass, volume and inventory.

| Radius (m) | Selected mask / knot | Pressure at 24 h (Pa) | Gas mass (kg) | Reserved gas mass (kg) |
| --- | --- | ---: | ---: | ---: |
| 10 | 2 / 64 | 102.491169310 | 3.192389619 | 48.894421502 |
| 12 | 2 / 64 | 89.976365129 | 4.879627277 | 84.489560355 |
| 15 | 2 / 64 | 77.483931511 | 8.289089519 | 165.018672569 |
| 20 | 2 / 64 | 65.034183600 | 16.715781588 | 391.155372015 |
| 30 | 2 / 64 | 52.695997361 | 46.607026218 | 1320.149380550 |

All 160 sampled candidates meet their declared gas-mass reserve and the 800 Pa pressure ceiling. The maximum-mass and maximum-pressure candidates happen to coincide at each radius.

**This establishes reproduction of the sampled frozen-thermal supplement. It does not establish a maximum over all coupled-weather geometries.** The owner explicitly corrected that scope in `inputs/SCOPE-ADDENDUM.json`. The earlier checker sweep over 8,432 finite coupled geometries per radius remains a separately defined calculation. Its R10 3.216712 kg and 103.376932 Pa values used different volume, inventory, molecular-mass and diffusion-path conventions; the difference from this replay is not a same-input arithmetic error.

The clarified calculation subtracts face and core metal volumes and specified polymer/splice displacement from the sphere volume, assuming connected core pores. It fully releases the conditioned inventory as water; initial, leak and permeating gas use a lumped 0.029 kg/mol air mass. The inventory contains both stated core contributions, and the primer/coating terms enter the absorbed-water contribution. Initial gas and leak conversion use 258 K; final pressure uses 326 K. Scarf diffusion uses one outer seam cross-section and the overlap length. These are model assumptions, not measured installed-hull properties.

## Convection and heating

The five R10 convection scalar cases reproduce using humid-air density at 95460.83791390515 Pa, viscosity 1.79e-5 Pa s, conductivity 0.0257 W/(m K), Prandtl number 0.71 and a 0.05 K natural-convection floor. The dry transient disables deposition while retaining default ambient humidity. These conventions agree with the corrected night calculation already filed in CHECK050; this addendum performs no new night transient.

For the clear-reference heater, the independent exact positive-part integral is **21.144629726368056 W/m²**. The independently evaluated 128-point Gauss-Legendre result is **21.1451220230001 W/m²**. Their difference is **0.0004922966320428657 W/m²**. Both reproduce the clarification and retain the previous one-decimal headline of 21.1 W/m².

## Qualification disposition

- **CHK50-06:** the quadrature difference is now explicitly acknowledged and quantified by both implementations. The heater's installation mass and physical performance remain unqualified.
- **CHK50-07:** the missing sampling and equation conventions are supplied and independently reproduced. This closes that computational subquestion. Geometry scope, measured leaks, pore communication, conditioning, desorption, permeability and sealed life remain qualifications.
- All eight original checker qualification records and the inherited register remain carried. CHK50-01 through -05 and -08 are unchanged. Installed-hull safety factor, sealed life and operational availability remain null.

The full 89-quantity headline check and weather classifications are those already filed in `rpt-ref-3eaf9fd65c0d3223ee65`; they were not recomputed here. The original package manifest remains pinned at `6f9b10df5fbebdb6d93c2bf879050a5a7c33640c59bdbc6f8160b1f834cb7fbb`.

`RESULTS.json` records exact comparisons; `GAS-CANDIDATES.json` and `.csv` retain every sampled candidate. `INPUT-PINS.json`, `METHOD.md`, `NFI-DISPOSITION.json` and `MANIFEST.json` provide provenance and current scope. No successor is named.
