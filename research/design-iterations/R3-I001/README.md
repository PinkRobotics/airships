# R3-I001: the 112 m both-moves budget

Internal conditional design hypothesis, 2026-10-13. No aircraft has been built or flown.
This record does not qualify a structure or authorise a new public scientific claim.

**Result: FAIL for positive hull margin at SF1.2 on the frozen model; complete-vehicle
mass, margin and physical confidence remain UNKNOWN.** The represented hull alone is
2330.730 t. Its mass-equivalent lift is 2249.837 t at sea level and
1757.363 t at 2500 m. It is already too heavy on both bases before omitted
systems are added. This closes that fixed-budget hypothesis, not the architecture or programme.

`not shown · margin UNKNOWN · confidence UNKNOWN · weakest assumption: required structural mass`

## Question and source

Can the strongest favourable large-hull bound carried into the programme close a matched
mass and lift budget at the declared structural factor 1.2? Start with its existing 112 m
both-moves case rather than silently lowering the factor or borrowing another vehicle's bill.

Sources are frozen at `afb2c2d1726b9d9a805f9781085c3dd6a52913e5`:
[float ledger](../../analysis/float-ledger.json), [model](../../analysis/vacuum-cell.py),
and [ledger generator](../../../tools/float_ledger.py). The selected ledger case IDs are
`hull-112m/both-moves/gamma-0.65/chord-1450/sf-1.2` and the same ID ending in `sf-1.0`.
The original ledger calls them bounds and sets `floatsToday=false` for both.
The [ledger guide](../../../docs/FLOAT-LEDGER.md) and [claim gate](../../../docs/CLAIM-GATE.md)
remain applicable.

The numbers below come from calling the frozen `ship0()` model, not from subtracting
rounded carry values. Both calls reproduce the original ledger's rounded mass, lift and
margin entries. Component sums close to the unrounded model total. Three decimal places
show reproducible arithmetic, not physical measurement accuracy; displayed component sums
can differ slightly through rounding. All masses and lift equivalents are tonnes (1000 kg).

## Candidate definition

This is a conceptual capsule bound, not a completed drawing:

| Item | Frozen input or interpretation |
|---|---|
| Geometry | Diameter 112 m; overall length 224 m; 112 m cylindrical section and hemispherical heads of radius 56 m; fineness 2 |
| Gross volume and boundary area | 1839046.452 m³ and 78816.276 m² |
| Double-wall skeleton | Scaled depth 6.461538 m; inner radius 49.538462 m; 155 longeron positions; circumferential brace spacing 2.270054 m |
| Fixed pitches | Outer ring and bar pitch 0.5 m; axial bay 2 m. The model scales depth and longeron count from the 52 m record, keeping these pitches absolute |
| Structural concept | Film on carbon-laminate hoop rings; end-cap grid; longerons and inner rings linked by fan and circumferential webs; tension spokes and separate gust-sized torsion straps |
| Carbon-laminate proxy | T700 UD, nominal fibre volume 0.6; E = 135 GPa, density 1600 kg/m³; chord compression ceiling 1450 MPa. These are model inputs, not qualified chord/process allowables |
| Tension-cord proxy | E = 70 GPa, density 970 kg/m³, fitting multiplier 1.3; no selected, qualified chordal net or termination design |
| Boundary-film proxy | Strength 5.8 GPa, density 1560 kg/m³, film SF4, efficiency 0.5 and bulge fraction 0.25; the model bills the one-way film factor of two |
| Pressure | Full vacuum idealisation, nominal internal/external pressure ratio 0; structure sized against 101325 Pa sea-level external pressure. Changing altitude here changes lift only, not structural sizing |
| Structural cases | SF1.2 is the declared comparison. SF1.0 is a crush-floor reference with no member safety reserve, never a safe operating candidate |
| Stability assumptions | General-instability knockdown 0.65; local-wall knockdown 0.30; classical coefficient 0.605; orthotropic factor 0.5699 |
| Both moves | Chordal net response credited at diametral-cord mass rates; in-surface shear stiffness credited without pricing its own hardware |
| Accounting policy | Explicit `basis='favourable'`; joint efficiency 0.85, 5% addition on the indicated skeleton members, and no extra record-policy stability reserve |

The 0.15 cellular node fraction elsewhere in the model is not a separate bill added to this
ship budget. Here joints are represented by the `etaMass=0.85` allowance. A real joint and
termination inventory must reconcile against these existing allowances to avoid double counting.
The 52 m wall-4 m scoping sweep and P100 equipment/cost case are different configurations;
neither contributes a number to this budget.

## Represented hull mass

| Component | SF1.2, t | SF1.0 crush floor, t |
|---|---:|---:|
| Outer hoop rings | 468.674 | 399.343 |
| End-cap grid, including its bending bars | 312.729 | 261.796 |
| Barrel bars | 16.639 | 15.055 |
| Boundary film allowance | 9.129 | 9.129 |
| Modelled clamps | 11.738 | 11.604 |
| Modelled pads | 9.458 | 9.458 |
| Longerons, including 5% junction addition | 223.400 | 208.670 |
| Inner rings, including 5% junction addition | 82.734 | 79.876 |
| Fan webs, including 5% junction addition | 275.680 | 257.199 |
| Circumferential webs, including 5% junction addition | 421.146 | 338.396 |
| Outer flange doubler | 0.000 | 0.000 |
| Cap-to-longeron shear members, including 5% addition | 56.368 | 46.973 |
| Equivalent tension spokes, including fitting multiplier | 107.974 | 83.485 |
| Gust-sized torsion straps | 2.561 | 2.134 |
| Joint mass allowance from member efficiency 0.85 | 327.771 | 283.643 |
| Void skin and jacket allowance | 4.729 | 4.729 |
| Additional reserve mass under favourable policy | 0.000 | 0.000 |
| **Represented hull total** | **2330.730** | **2011.490** |

These are computed bills, not measured parts. A zero flange-doubler or additional-reserve
entry means zero in this particular model solution and policy. It does not establish that
an as-built structure needs no such provision. Film, clamps, pads and joint allowances are
already in the bill; none proves that real seams, interfaces or fittings have been designed.

## Missing or unresolved all-up entries

| Entry | Treatment in the present budget | What resolves it |
|---|---|---|
| In-surface shear hardware | Own mass UNKNOWN and not in the total, despite the stiffness credit | A geometry, stiffness and mass bill for the actual shear load path, or removal of that credit |
| Chordal net and terminations | The spoke allowance above is included; the correction to real geometry, preload, fittings and anchors is UNKNOWN | Price and check an explicit net against every credited mode; reconcile its total against the existing allowance |
| Real joints, bonds, seams and interfaces | Coarse allowances partly included; replacement corrections UNKNOWN | Component drawings and a mass reconciliation, followed by applicable material/joint evidence |
| Vacuum retention and isolation | Ideal vacuum assumed; retained gas and any carried leak-control, valve or evacuation hardware UNKNOWN | Specify the pressure schedule, allowable leak rate and carried-versus-ground hardware |
| Propulsion, energy, controls and mission equipment | UNKNOWN; no P100 battery, rotor, cryogenic or other equipment budget imported | Define the vehicle mission and price the carried systems on this exact configuration |
| Payload and ballast | UNKNOWN for a mission; zero is used only when screening the most favourable unladen hull bound | An explicit payload/trim requirement and matched mass budget |
| Loaded shape and useful evacuated volume | Geometric volume with the model scallop debit only; further loss UNKNOWN | Loaded geometry and measured or validated volume/pressure behaviour |

If the represented hull bill is held fixed and omitted carried additions are `U >= 0` t,
then `M_all = M_hull + U`, and the SF1.2 margins are at most −80.893 t at sea level and
−573.367 t at 2500 m. More generally real replacements also introduce an UNKNOWN signed
correction `C` to existing allowances, so `M_all = M_hull + U + C`; no numeric all-up result
is claimed. Neither UNKNOWN is silently set to zero to assert float confidence.

## Lift and margin on the matching basis

The model uses its ISA density and applies the same hull volume at each altitude.
Its film-scallop approximation subtracts `area × 0.03125 m` = 2463.009 m³,
leaving 1836583.443 m³ in this lift calculation. This is not a measured
usable vacuum volume. The budget is displaced-air mass equivalent with ideal vacuum;
retained gas and further volume losses still need their own debit.

| Altitude | Density, kg/m³ | Gross displaced-air equivalent, t | Scallop debit, t | Model lift, t |
|---|---:|---:|---:|---:|
| 0 m | 1.225012266 | 2252.854 | 3.017 | 2249.837 |
| 2500 m | 0.956865434 | 1759.720 | 2.357 | 1757.363 |

| Case | Sea-level margin, t | 2500 m margin, t | Interpretation |
|---|---:|---:|---|
| SF1.2 | -80.893 | -573.367 | Hull-only FAIL at both altitudes before additions |
| SF1.0 crush floor | +238.347 | -254.127 | Conditional sea-level allowance only; zero member safety reserve, no all-up or safe-vehicle conclusion |

Reducing the factor from 1.2 to 1.0 removes 319.240 t from this model
bill. It does not validate the missing structure. The crush-floor sea-level allowance is
exhausted by 238.347 t of nonnegative additions even before any replacement
correction. At 2500 m the same crush-floor hull already fails by 254.127 t.

## Sensitivity and expert-confirmation ledger

The weakest quantitatively tested assumption is the attainable structural mass under the
unverified GI knockdown, with 0.65 the dominant sampled capacity assumption. An important
unbounded uncertainty is whether the credited chordal net and unpriced shear load path can
be realised at their represented masses. These uncertainties are not a statistical confidence
interval and cannot be added as independent probabilities.

Four one-at-a-time model changes keep diameter 112 m and SF1.2. All keep the favourable
reserve-accounting policy fixed, so the knockdown row isolates capacity rather than also
switching to the record policy. They are sensitivities of this bounded greedy model, not
new validated designs or a continuous optimum:

| Changed assumption | Represented mass, t | Change in margin at either altitude, t | Sea-level margin, t |
|---|---:|---:|---:|
| GI knockdown 0.65 → 0.30; favourable reserve policy held fixed | 3160.131 | -829.401 | -910.294 |
| Chord compression input 1450 → 1050 MPa | 2572.045 | -241.315 | -322.208 |
| Remove the unpriced in-surface membrane stiffness credit | 2331.843 | -1.113 | -82.006 |
| Remove chordal credit; retain the diametral-only spoke response | 2730.589 | -399.859 | -480.752 |

All six model evaluations return their listed sizing checks true. Those checks cover the
coded member/GI/cap conditions only; they do not qualify missing hardware, all global failure
modes, manufacturing imperfections or an aircraft. In particular, the small 1.113 t penalty
for dropping membrane credit in this 112 m solution is a model sensitivity, not a measured
price for the omitted shear system.

| Expert confirmation | Why it matters | Change if wrong, on this frozen basis |
|---|---|---|
| GI knockdown applicable to this assembly | Sets credited global stability capacity and structural mass | 0.65 → 0.30 costs 829.401 t of margin with favourable reserve policy held fixed; more adverse values not bounded here |
| Actual chord compression allowable | Datasheet UD ceiling is not the built chord/laminate/process | 1450 → 1050 MPa costs 241.315 t; manufacturing/local interaction outside these scalar inputs remains UNKNOWN |
| Chordal geometry, preload and termination behaviour | The model credits response in modes that diametral cords do not engage | Removing chordal credit costs 399.859 t; actual added/replacement hardware mass remains UNKNOWN |
| In-surface shear load path | The credited stiffness has no dedicated hardware bill | Every added tonne costs one tonne of margin; switching off its credit costs 1.113 t in this particular model solution |
| Matched as-built joints, films, equipment and fittings | Allowances and omitted subsystems are not a vehicle inventory | Each extra tonne beyond the represented bill reduces either margin by 1 t; total correction UNKNOWN |
| Loaded evacuated volume and retention | The lift equation assumes ideal vacuum and the modelled shape | A 1% loss of effective volume at fixed hull mass costs 22.498 t at sea level or 17.574 t at 2500 m; each retained-gas tonne also costs 1 t |

Each entry concerns R3-I001 and the successor that reuses it. Confirmation requires an
applicable drawing, analysis or measurement; a source citation, passing checksum or expert
opinion alone is not a weighed assembly. No expert contact, physical work or purchase was made.

## Next concrete design change

**Next trial: reduce diameter from 112 m to 80 m, retaining fineness 2 and SF1.2.** This
produces a 160 m long candidate, scaled wall depth 4.615385 m and 111 longeron positions
under the existing rule. Keep material inputs, absolute pitches and the two bound credits
explicitly frozen so the geometric change can be assessed on a comparable basis.

This ranks first because the original ledger's ten sampled SF1.2/favourable/both-moves
sizes give their largest absolute sea-level hull allowance at 80 m: **51.9 t**, versus
42.0 t at 96 m, 46.9 t at 68 m and −80.9 t at 112 m. These are the source's rounded values,
not newly precise subtractions. The 80 m row still has **−127.5 t at 2500 m** and retains
both unqualified credits. This selects a design hypothesis; it is not a global optimum,
a new calculation of that candidate, or evidence of a complete floating vehicle.

The next assigned iteration should lay out and price that 80 m configuration, retain an
explicit additions/corrections budget, and test whether its possible sea-level allowance
survives. The next structural priority is a costed chordal net and terminations; removing
unsupported stiffness credit is preferable to claiming it without a load path. If the
budget still fails, preserve the result and rank the next geometry/structural change.
Do not seek an apparent improvement by adopting SF1.0 as an operating design.

## Reproduction and custody

The evaluation used six deterministic, single-process calls to the existing Python model
under a 60 s wall / 30 s CPU / 1 GiB address-space ceiling. They completed in under one
second. No native solver, CFD, FEA, simulation attempt under the exhausted old caps,
source-code change or historical patch replay occurred. The selected future 80 m trial
was not executed as a new design in this unit.

From the repository root, the two principal rows can be reproduced with:

```sh
python3 -B - <<'PYCODE'
import importlib.util
import math
s = importlib.util.spec_from_file_location('cell', 'research/analysis/vacuum-cell.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
for sf in (1.2, 1.0):
    r = m.ship0('s1450', sf=sf, dia_m=112.0, gi_knockdown=0.65,
                gi_chordal=True, gi_membrane=True, basis='favourable')
    assert math.isclose(sum(r['ledgerT'].values()), r['totalT'], abs_tol=1e-8)
    print(sf, r['ledgerT'], r['totalT'], r['liftSLT'], r['lift2500T'],
          r['residualSLT'], r['residual2500T'])
PYCODE
```

| Frozen source path | SHA256 |
|---|---|
| `research/analysis/float-ledger.json` | `d4c8085510bd80fb6feb0951b6bb33030cd16b5f9452f5fb7c015a97d2916126` |
| `research/analysis/vacuum-cell.py` | `21d5a26c3616bb09fab0585e9e8613f84be8ed786d5d509287fd1839efd564a5` |
| `tools/float_ledger.py` | `632fa75dd99557c96ef7c6154baaefd860dd3a2c4502369001574803ead0a9bf` |

One external custody evidence file retains the unrounded calls and their arguments,
component-sum and original-ledger comparisons, exact candidate/base/tree, governance,
checks, review status and limits. Documentation checks establish repository consistency;
arithmetic reproduction establishes agreement with this model. Structural qualification,
complete-vehicle float confidence, review acceptance and landing are separate claims.
