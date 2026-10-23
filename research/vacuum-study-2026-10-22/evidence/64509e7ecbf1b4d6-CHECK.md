# MAINLINE-032 independent check — ESTIMATE / QUESTIONABLE

Unit `vacuum-mainline032-check-1020`; order `ord-admiral-rr2-check032-codex-575b-1020`. No certification. The focused equations and conditional tolerance tables pass; the amplitudes are not established manufacturing allowables.

All **236** numerical, Boolean, source-constant, display and self-check comparisons pass at the stated precision. This covers all 155 engineering/Boolean scalar leaves in owner RESULTS; the sole excluded numeric field is its elapsed timer. INPUTS has 38 checked scalar fields and two pin-length metadata fields separately verified. One CARD range label is incorrect. Ten nonblocking findings record that correction and the outstanding material, measurement and transfer limits.

## What was checked

The initial ten owner/authority artifact pins match. The owner script was hashed only; it was never read as code or run. Own `check.py` uses primary equations, the pinned brief's rounded face/core geometry, and independently read source constants. `NUMERIC-CHECK.csv` contains reported value, checked value and exact floating-point difference for every comparison. Raw tolerances are relative 3e-12 or absolute 1e-12. The inherited dimpling values use their stated one/two-decimal precision; exact underlying values are reported below. All other input/source and snapshot pins also verify.

Comparison categories: 139 numerical values, 14 Booleans, four rounded upstream quantities, 36 source constants or conversions, seven owner PASS labels, 20 CARD amplitude tokens and 16 additional CARD/report tokens. No equation or table mismatch survives the appropriate precision comparison. Source facts and access limitations are recorded separately in `SOURCE-AUDIT.json`; an unavailable source passage is not treated as verified.

## Equation and strength definition

The printed [NASA CR-1457](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf) pages 2-29 and 2-33 were inspected visually. Its equations give

`sigma_u = 0.82 sqrt(eta Ef Ec tf/tc) / (1 + 0.64 Kdelta)`,
`Kdelta = delta Ec/(tc Fc)`.

For the elastic case, define `Q=sigma_u/sqrt(Ef Ec tf/tc)`. Then

`Q = 0.82/(1+0.64 Kdelta)` and
`delta = (tc Fc/Ec) (0.82/Q - 1)/0.64`.

This is a monotone amplitude ceiling when the model, properties, wavelength interpretation and target Q apply. It gives zero amplitude at Q=0.82; positive amplitude for 0<Q<0.82. No face thickness enters this inverse at fixed Q, although tf enters the normalization δ/tf and the required stress.

**Fc is the lowest flatwise core-compressive, core-tensile and core-to-facing bond strength.** Stabilized compression is the relevant compression candidate for a bonded core; it is not automatically the controlling Fc. Bare compression and post-crush resistance are different quantities. The owner states the lower-of-three qualification in its NFI, and that statement is correct.

[Hexcel Table II](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf) confirms, for CR-III 5056 3/8-1.0, stabilized compression 60 psi typical / 35 psi minimum average and normal compression modulus 15 ksi typical. The separately listed typical crush value is also 35 psi. Its numerical equality to the compression column does not make the properties interchangeable. The table's “min” means a minimum average for a product type. Tests used 0.625 inch thickness. No matching Be-bond or flatwise tensile strength is supplied.

Own unit conversions give 15 ksi = 103421359.3975254 Pa, 60 psi = 413685.4375901016 Pa, 35 psi = 241316.50526089262 Pa, 1 pcf = 16.0184633739601 kg/m³, and 3/8 inch = 9.525 mm. The owner correctly keeps its separate 9.5 mm brief-normalization column.

## Recomputed curves and inverses

For the two specified geometries, a single curve describes Q versus δ/tc. Their absolute amplitudes differ by 30.12/20.21 = 1.49035131123206. Switching the conditional Fc from 60 to 35 psi multiplies every amplitude by 7/12 = 0.583333333333333.

| δ/tc | Q at conditional Fc=60 psi | Q at conditional Fc=35 psi |
|---:|---:|---:|
| 0.0000 | 0.820000000000 | 0.820000000000 |
| 0.0005 | 0.759259259259 | 0.721105527638 |
| 0.0010 | 0.706896551724 | 0.643497757848 |
| 0.0020 | 0.621212121212 | 0.529520295203 |
| 0.0030 | 0.554054054054 | 0.449843260188 |
| 0.0040 | 0.500000000000 | 0.391008174387 |
| 0.0050 | 0.455555555556 | 0.345783132530 |
| 0.0070 | 0.386792452830 | 0.280821917808 |
| 0.0100 | 0.315384615385 | 0.219083969466 |

The four Q/face combinations at each strength are:

| Face | Q | Fc psi | δ mm | δ/tf | δ/9.525 mm | Kδ |
|---|---:|---:|---:|---:|---:|---:|
| S-200F | 0.371 | 60 | 0.152868766846 | 0.181252984167 | 0.016049214367 | 1.891004043127 |
| S-200F | 0.609 | 60 | 0.043763444171 | 0.051889310138 | 0.004594587315 | 0.541358784893 |
| SR-200 | 0.371 | 60 | 0.227828167116 | 0.329374247674 | 0.023918967676 | 1.891004043127 |
| SR-200 | 0.609 | 60 | 0.065222906404 | 0.094293633662 | 0.006847549229 | 0.541358784893 |
| S-200F | 0.371 | 35 | 0.089173447327 | 0.105730907431 | 0.009362041714 | 1.891004043127 |
| S-200F | 0.609 | 35 | 0.025528675766 | 0.030268764247 | 0.002680175933 | 0.541358784893 |
| SR-200 | 0.371 | 35 | 0.132899764151 | 0.192134977810 | 0.013952731144 | 1.891004043127 |
| SR-200 | 0.609 | 35 | 0.038046695402 | 0.055004619636 | 0.003994403717 | 0.541358784893 |

The two lead cases at 60 psi are **0.152868766846361 mm** for S-200F at Q=0.371 and **0.0652229064039409 mm** for SR-200 at Q=0.609. At the 35 psi scenario they become **0.0891734473270440 mm** and **0.0380466954022988 mm**. These reproduce the filed values. The table includes the cross-Q cases explicitly, so they cannot be mistaken for each face's lead requirement.

The Q=0.33 inversions also reproduce:

| Face | Fc psi | Projected δ at Q=0.33, mm |
|---|---:|---:|
| S-200F | 60 | 0.187554924242 |
| SR-200 | 60 | 0.279522727273 |
| S-200F | 35 | 0.109407039141 |
| SR-200 | 35 | 0.163054924242 |

These are correctly tagged PROJECTION by the owner. Algebraically, 0.33/0.82 = 0.402439024390244. The empirical design coefficient does not identify a measured wave amplitude.

`Q-WAVINESS.png` and `Q-WAVINESS.pdf` plot the independently derived curves against δ/tf and δ/cell; `CURVE-DATA.csv` supplies the plotted points. The strength cases are conditional scenarios, not a measured confidence interval.

## Biaxial transfer and the dimpling distinction

The [source wrinkling interaction](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf#page=75) is `Rx³+Ry=1`, with each ratio referred to that direction's uniaxial capacity. For equal capacities and equal applied compression, solve `b³+b=1`. The independent 60-digit solution is

`b = 0.682327803828019327369483739711048256891188581897998577803732`.

The card uses 0.6823, giving `card-root = -2.7803828019257182e-5` and cubic residual `-6.663623299996146e-5`, as filed. Its relative rounding change is about -0.00407485%. Multiplying the already waviness-adjusted uniaxial stress by this factor does not duplicate the waviness reduction. This algebra does not establish equal directional strengths or validate a curved Be sandwich under pressure.

Intracell dimpling uses a [different source interaction](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf#page=49), `Rx+Ry=1`. Its equal-compression multiplier is 0.5. Applying it to the uniaxial expression `2 Ef/(1-nu²) (tf/s)²`, and using the full pinned upstream geometry with membrane stress `pR/(4tf)`, gives:

| Upstream point | Applied stress MPa | Formal elastic equibiaxial dimpling SF | Filed rounded SF |
|---|---:|---:|---:|
| 021 S-200F | 282.948186824093 | 9.018853684781929 | 9.0 |
| 021b SR-200 | 344.998605253324 | 4.975309121115971 | 4.98 |

The raw printed-minus-derived differences are -0.018853684781929 and +0.004690878884029, both consistent with rounding. These are conditional elastic-model factors, not validated physical failure margins. NASA notes that dimples can develop into wrinkling; [FPL 1810-A](https://ir.library.oregonstate.edu/downloads/2f75rc704) also relates wrinkles to cell geometry. A small amplitude/cell ratio alone does not show independence. Neither cell size nor the pictured shop bow is a measured critical wavelength.

## Exact prose correction and input precision

The CARD's sentence saying the **lead amplitudes** span 0.0046–0.024 of the cell is mislabeled. The actual lead-only ratios are

`0.006847549228760197 to 0.01604921436707204`.

The endpoints for all four typical-strength rows are

`0.004594587314516719 to 0.02391896767621028`.

The latter round to the printed sentence. Correct its label to all four cases, or use the lead-only endpoints. None of the four underlying rows needs recalculation.

The brief itself requests rounded Q and geometry. Using full pinned upstream values instead gives:

| Point | Full required Q | Full core mm | Conditional 60 psi amplitude mm | Brief minus full amplitude mm |
|---|---:|---:|---:|---:|
| 021 | 0.37068071372338524 | 20.21337638749162 | 0.15313481918912647 | -0.000266052342765333 |
| 021b | 0.6092014443376216 | 30.118230884842855 | 0.06513526466329604 | +0.000087641740644823 |

These differences are -0.1737373278% and +0.1345534421% relative to the full-input amplitudes. They are input-precision effects, not failures of the requested brief-based calculation. In particular, a quoted Q of 0.609 must not be read as the exact 021b SF=1 threshold.

For nonelastic eta, the coefficient relative to the elastic square-root scale is `0.82 sqrt(eta)/(1+0.64 Kdelta)`. Thus a target Q would give

`delta = (tc Fc/Ec) [0.82 sqrt(eta)/Q - 1]/0.64`,

only when the bracket is nonnegative. Even a perfect facing cannot reach the two targets if eta is below 0.204701070791196 or 0.551577929803688 respectively. At an illustrative eta=0.8, the 60 psi amplitudes become 0.123394816285189 and 0.0384630596694614 mm. These are PROJECTION sensitivities, not claims about Be's actual eta. A stress-dependent eta must be treated self-consistently.

## Manufacturing and source audit

The retrieved manufacturer specifications support the quoted magnitudes:

| Primary source | Verified quantity | Comparison limit |
|---|---|---|
| Flatiron | ±0.008 in/radial ft = ±0.2032 mm/radial ft; selected face 0.040 in = 1.016 mm | Commercial aluminum panel, thicker selected faces; a spatial bow tolerance. |
| Honylite | ±0.7 mm/radial m | Balanced aluminum panels; no critical-mode amplitude supplied. |
| QC Facades | WAVE ±1 mm; ±1/16 in (printed 1.5 mm)/60 in | Architectural surface categories; no critical-wavelength qualification. |
| Indy | 0.010 in = 0.254 mm overall; 0.003 in = 0.0762 mm steps | Welded core under hold-down ≤7 psi, not this bonded Be/Al sandwich. |
| SAE AMS7902H | Hot-rolled Be scope verified; no flatness-class values read | Public primary page does not expose §3.5.5; three-class statement remains unverified here. |
| Hexcel design guide | Telegraphing described; no amplitude depth | No numerical as-bonded Be surface capability. |

[Flatiron](https://www.flatironpanelproducts.com/wp-content/uploads/2020/02/Flatiron-Stock-AHP04038-Data-Sheet-2-11-2020.pdf), [Honylite](https://www.honylite.com/materials/strength-flatness-inserts), [QC Facades](https://qcfacades.com/wp-content/uploads/2019/05/190101_Honeycomb-Flatness-Guarantee.pdf) and [Indy](https://indyhoneycomb.com/wp-content/uploads/2023/04/IHSS-N1_C.pdf) specify different geometry and measurement conditions. The owner's warning that these are not delta is appropriate. The [official SAE record](https://saemobilus.sae.org/standards/ams7902h-beryllium-sheet-plate-98be) confirms scope but not the missing quantitative flatness comparison. The [Hexcel design guide](https://www.hexcel.com/wp-content/uploads/2026/01/Honeycomb_Sandwich_Design_Technology.pdf) describes telegraphing without a depth.

The [FPL 1810 primary indexed introduction](https://www.fpl.fs.usda.gov/documnts/fplr/fplr1810.pdf) discusses amplification of Fourier components near the critical wavelength, including nearby components. Its full PDF was not retrieved in this check; the direct request failed. Its bibliography, independently confirmed in CR-1457, lists Norris, Ericksen, March, Smith and Boller. The owner's correction of the brief's Kommers attribution to March as third author is supported. The retrieved FPL 1810-A lists Norris, Boller and Voss.

## Nonblocking findings

| Finding | Disposition | Exact point |
|---|---|---|
| NFI-032-CHECK-FC | qualification | The correct Fc is min(compression, core tension, facing-core bond). Neither scenario establishes the bonded sandwich value. Typical crush 35 psi happens to equal minimum-average stabilized compression numerically, but represents a different property. |
| NFI-032-CHECK-MINIMUM-AVERAGE | qualification | Table II labels min as minimum average for a product type, not a guaranteed pointwise or full-hull minimum. Ec is typical. Pairing these values is a scenario, not a statistical lower tolerance bound. |
| NFI-032-CHECK-THICKNESS | open | 0.625 inch is 15.875 mm; the requested cores are 20.21 and 30.12 mm. No matching thickness/bonded-state validation was supplied. |
| NFI-032-CHECK-ETA | open | Relative to sqrt(Ef*Ec*tf/tc), the effective coefficient is 0.82*sqrt(eta)/(1+0.64*Kdelta). For a fixed target Q, amplitude changes with eta. Plasticity in the nearly strength-limited faces is not calibrated. |
| NFI-032-CHECK-WAVELENGTH | open | Those ratios do not identify wavelength or mode separation. CR-1457 explicitly allows dimples to precipitate wrinkling. Dimpling uses a different biaxial factor (0.5) from wrinkling's cubic root. |
| NFI-032-CHECK-SHOP-METRIC | open | Quoted product numbers reproduce, but geometry, material, ± convention, hold-down, wavelength and load state differ. The primary SAE public record does not verify the three-class claim or give flatness numbers. |
| NFI-032-CHECK-BIAXIAL-TRANSFER | open | The algebra is correct for equal directional uniaxial capacities and does not count waviness twice. The handbook's flat-plate rule alone does not validate the loaded curved Be sandwich or establish equal directional capacity. |
| NFI-032-CHECK-DESIGN033 | projection | The arithmetic is correct but this is not a measured defect distribution or proof of why the empirical knockdown has that value. The owner already tags these rows PROJECTION. |
| NFI-032-CHECK-LEAD-RANGE | correction | The lead-only ratios are 0.006847549228760197 and 0.01604921436707204. The printed endpoints are the two cross-Q rows among all four 60 psi cases. The underlying four rows are correct. |
| NFI-032-CHECK-ROUNDED-TARGET | qualification | Using the full pinned 021/021b geometry and required Q gives conditional 60 psi amplitudes 0.15313481918912647 and 0.06513526466329604 mm. The brief-based rows differ by -0.1737373278% and +0.1345534421%, respectively. This is intentional input precision, not an error in the requested calculation. |

Seven of the owner's eight open NFI topics remain valid qualifications; the author correction is independently verified. Three additional entries distinguish the minimum-average label, the lead-only range and rounded target precision. No finding is a stop gate.

## Record and disposition

`SOURCE-AUDIT.json` records exact source locations, access limits and page images. `INPUTS.json` pins the evidence, copied upstream data and authority. All original files were left unchanged.

The owner's elapsed timer is metadata, not an engineering value that can be independently recreated without executing foreign code. The printed timestamps differ by 0.000275 s; its recorded elapsed timer differs from that by about 0.00000132201 s. Distinct clocks/read points can account for this; no duration discrepancy is asserted.

Work began 2026-10-20T01:44:49-07:00; the independent calculation completed 2026-10-20T01:54:37-07:00. Final assembly/end time is in WORK.json. Times are measurements, not limits. The check is complete and will be filed once; no successor job is named.
