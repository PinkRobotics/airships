# MAINLINE-048 method and limitations

All transferred material properties are QUESTIONABLE; installation, processing and mission performance are PROJECTION. No installed-hull safety factor is known.

## Reused account

The immutable 040 model, inputs, atmosphere and thermal table are pinned in `MODEL-PINS.json`. `prepare_model.py` generates local `model48.py` and `thermal48.py`; it does not change 040. The primary construction retains 037b's proposed 200 °F stress-free cure and 30.341397:1 scarf. It retains the heavy 70-knot pad, vented core, complete wind-pressure envelope, 100 kg systems allocation, maximum of gas reserve and ingress, contamination, and weather headroom. Actual joining and the retained 5% structural floor are separate conventions: charge `max(actual, floor)`, never their sum.

Here “actual” retains 040's four explicit components: film, scarf, splice and seal. The new structural primer is an additional charge outside that original floor. This declared conservative convention does not credit unused floor reserve toward primer.

028b's endpoint is mask 11: full effective global coefficient and Q=.82, 0.015 lb/ft² film at each interface, with today's E=290 GPa and compression strength 345 MPa. The film convention is carried from 028b; film optimism remains a separate named axis in least-set searches. The four axes are gamma, Q, the coupled historical E/Fcy tuple, and film weight. Every subset is enumerated. Among floating subsets, select the fewest axes, then the smallest common normalized logarithmic interpolation usage. This is a declared minimax convention, not an economic valuation of optimism. All endpoints, tie candidates, material values and geometries are retained.

For a fixed core thickness, solve for the minimum face thickness satisfying the retained scalar mechanical modes. Scan 440 logarithmically spaced core thicknesses, refine every detected local maximum, and examine feasibility boundaries. Core search domain is 0.0012–1.4 times R/10 metres; face upper bound is `min(.0195, .008 R/10)` metres. Larger independent searches check primary results. No proof of whole-hull buckling safety follows from this numerical optimization.

E raises thermal stress as well as elastic capacity. Validation uses a deliberately favorable bound with full elastic E and today's thermal E to test whether the omitted lower-cardinality subsets could float. This guards the subset-count claim; the reported common-usage value remains conditional on the defined interpolation/search model.

## Finish and temperature

`COATINGS.json` records the candidate optical values and mass provenance. Deposited masses are sums of thickness times density, without a carrier; they require direct deposition on Be. Classical CCAg totals 9.3256–11.1786 g/m². The multilayer patent recipe totals 7.5752 g/m². Its α=.09, hemispherical ε=.80 is a class-level NASA transfer, not a measured optical pair for this precise layer recipe on Be. This is the lightest recipe screened, not a proven global optimum or qualified product.

The applied deposited mass includes an assumed 10% allowance. FEP tape entries include the supplier's adhesive mass and receive an assumed 5% overlap allowance. Every new main row additionally charges 10 g/m² for the structural primer on the two interfaces. That primer is separate from the optical coating's tie layer. A source-required additional Be treatment, edge seal, repair or backing must fit the remaining mass margin.

`THERMAL-SCREEN.json` reproduces 037's source geometry, midpoint quadrature, 25 fixed iterations and its aluminum-density convention for direct day-factor comparison. Day factor uses the daytime temperature rise; the separate full-cycle factor uses the hottest day to coldest night excursion. Both use 037's typical W shear strength. Requiring day ≥1.678 and full-cycle ≥1 is a screening criterion, not the cure-reference bond calculation.

The 048 mechanics instead use converged 128-point Gauss thermal tables, mean-removed degree 2–6 curvature projection and the maximum day/night face gradient and curvature. 040 used daytime gradient/curvature; its night temperature already entered cure residuals. Each coating is solved with its own α and ε, outer-air convection, fixed inner ε=.2, 970 W/m² day sun and day/night sky temperatures 275/260 K. This retains 040's thermal environment rather than silently equating it with every 031 weather state. Log-core-thickness interpolation has a 1.002 stress guard; direct 256-point solves check it.

The current free-edge factor uses the minimum 25 psi W allowable, compliant biaxial core stiffness, and the largest excursion from the proposed 200 °F cure. The day factor, full-cycle factor and current cure-reference factor are therefore different quantities. Cold nighttime coating temperatures can increase cure residuals even while daytime solar performance improves.

The coating's own thermal resistance, coating stress, local discontinuities, wet optics and emissivity angular dependence are not resolved. `SENSITIVITIES.json` prices explicitly assumed optical aging/wetting cases. Retaining an exterior-water mass while using dry optical values does not establish a wet-hull thermal state.

## Water and dry-out

The inherited exterior debit is 0.1 kg/m², derived from an assumed 0.1 mm retained liquid film at 1000 kg/m³. It is not adhesive uptake. Every main drying row retains it. Separate zero-exterior-water rows are a conditional operating envelope, never a bake-out credit.

Extra water above the nominal material mass is:

`W = f_AF M_film + .001 M_core + .01 M_structural_primer + W_finish + .01 M_seam_polymers`.

The main `f_AF=.002` is the largest historical AF163-2U WVR, not an equilibrium isotherm. Other fractions are explicit planning allowances except FEP's <.0001 base-film datum. FEP adhesive uses an assumed .01 fraction. Deposited finish water uses an assumed .01 of its applied mass. Whether nominal densities/film weights already include some moisture is unknown; no subtraction from nominal structural mass is taken.

The routes are:

- Additional dry-gas assembly: retain all this modeled initial material water. Five ideal mixed ground-enclosure exchanges are a gas-resource example, with air concentration reduced by exp(−5); there is no assumed material drying from that equation.
- Preseal 70 °C vacuum conditioning: assume a verified 90% reduction in this added-water inventory. The temperature comes from coupon preconditioning evidence for AF163-2M; the achieved reduction and installed process are projections. No duration is inferred.
- Onboard sorbent: retain all water mass and add a dry bed/cartridge. Required water capacity is `1.1(W + I_nominal) + .1(R/10)^3 kg`; dry bed mass is capacity/.10, plus 2 kg cartridge. Ten-percent usable capacity and 95% vapor capture at hull pressure are assumptions. Ground discard of sorbent would be a different measured drying operation.

All routes inherit 040's nominal 90% volatile conditioning assumption. That inventory is `I_nominal=.1(.0485 M_film + .001 M_core + .01 M_seam_polymers)`. Its material mass remains aboard. WVR and TML are not exchanged, and no TML mass is credited as removed water. Added material water is an explicit further conservative charge. A one-day time constant releases `(1-exp(-1))` of each modeled inventory into the pressure calculation.

Desorption and adsorption change phase without a second mass charge. Incoming gas stays aboard even if its water is captured. The service audit also checks zero capture and removal of the inherited nominal-conditioning credit. Representing nominal volatiles as water-equivalent capture is unqualified, so the zero-capture result is particularly relevant.

Ground bake energy uses explicitly assumed heat capacities: Be 1825, aluminum core 900, polymers/coating 1000 J/kg/K; warm from 284.9 to 343.15 K and add 2.45 MJ/kg removed water. This is an ideal lower bound excluding ovens, supports, vacuum equipment, heat loss and binding energy. Ground-gas demand assumes five complete sphere-volume exchanges of nitrogen at the inherited pressure/temperature. Actual panel/glovebox processing changes that demand. Equipment size, process duration and financial cost are unsourced.

## Reproduction and scope

Run with `PYTHONDONTWRITEBYTECODE=1`, `OPENBLAS_NUM_THREADS=1` and scratch temporary storage:

1. `prepare_model.py`
2. `thermal_screen.py`
3. `calculate48.py MLCCAg`, `calculate48.py CCAg`, `calculate48.py AgFEP05`, `calculate48.py AgFEP1` independently.
4. `sensitivity48.py`
5. `validate48.py`
6. `qualify48.py`
7. `prepare_evidence48.py`
8. `build_card.py`
9. `package48.py`

Source downloads, selected web facts, inherited inputs, script hashes and outputs are pinned in the final manifest. No external seat was restored, woken or messaged; the final filing uses the queue only.
