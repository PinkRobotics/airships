# MAINLINE-048 independent check — partial after admission refusal

QUESTIONABLE / PROJECTION. The completed calculation checks the account at all 7,149 distinct stored main design points, conditional on the pinned thermal tables. It does **not** independently establish the thermal tables, the least-set optimum, or an installed-hull safety factor. The required full check remains open.

The account rerun was refused by simjob at 2026-10-20T12:13:10Z: memory PSI some avg10 6.13 exceeded the 5.00 admission threshold. Exit 75; nothing started. The standing order says a refusal is a stop and grants no retry. There were no subsequent scientific launches. Three earlier admitted jobs completed and released their reservations. Collection, source reading, and this report continued. No owner code was read, copied, hashed, imported, or run.

## What is established

The layer arithmetic below reproduces the selected mass recipes. In the executed account check, all compared mass-bill terms, signed payloads, structural modes, joining quantities, material-water charges, sorbent masses, and pressure values agree with the stored main points within `rtol=2e-8, atol=2e-8`. This is evaluation at supplied geometries and supplied optical/thermal inputs, not independent geometry optimization.

The executed account made 686,304 comparisons. Its 16,679 recorded differences occupy three vacuum bookkeeping fields, discussed below. `ACCOUNT-COMPARISONS.csv.gz` retains every comparison; `ACCOUNT-MISMATCHES.json` retains every differing row, field, owner value, independent value, delta, and tolerance. The initial run's source is preserved under `execution/account-01/source/`.

The independent thermal model made 325 comparisons across 13 optical candidates at the source geometry; 297 differ. Those are unresolved model/convention differences, not 297 established owner mistakes. Every difference is retained in `THERMAL-COMPARISONS.csv` and `THERMAL-RESULTS.json`. A separately executed diagnostic is in `THERMAL-DIAGNOSTIC.json`.

## Finish masses and optical provenance

For thickness in micrometres and density in g/cm³, their product is g/m². The selected multilayer recipe gives:

| Layer | Thickness, µm | Density, g/cm³ | Mass, g/m² |
|---|---:|---:|---:|
| NiCr | 0.05 | 8.4 assumed | 0.4200 |
| Ag | 0.12 | 10.5 | 1.2600 |
| Al₂O₃, 80 layers | 1.20 | 3.97 | 4.7640 |
| SiO₂, 80 layers | 0.40 | 2.648 | 1.0592 |
| ITO | 0.01 | 7.2 | 0.0720 |
| Total | 1.78 | — | **7.5752** |

The assumed 10% application allowance gives **8.33272 g/m²**. Classical CCAg uses 0.08 µm alumina beneath silver, 1.6–1.9 µm alumina above it, 0.5–0.75 µm silica, the same silver, and 0.01 µm ITO: **9.3256–11.1786 g/m²**. Its modeled lower applied mass is **10.25816 g/m²**. The classical ITO source says less than 100 Å; assigning 100 Å is an upper-cap convention, so the reported lower recipe is not an exact physical minimum.

These thickness recipes are supported by the [NASA patent text](https://patents.justia.com/patent/11391493). Its claim also associates the multilayer coating with about 3.2 µm overall thickness, whereas the explicit selected recipe totals 1.78 µm. This internal source ambiguity needs reconciliation before treating recipe mass and measured optical performance as a matched specimen.

The MLCCAg α=.09, hemispherical ε=.80 pair is a class-level transfer from [NASA's 2018 coating presentation](https://ntrs.nasa.gov/api/citations/20180002012/downloads/20180002012.pdf), not a measured pair for this exact stack on Be. The owner labels that transfer PROJECTION, appropriately.

There is one precise citation correction: `COATINGS.json`, `CCAg.optical_source`, points to [NASA 2015, printed slide 19](https://ntrs.nasa.gov/api/citations/20150018109/downloads/20150018109.pdf), which gives **α=.08 and normal ε=.72 on 3 mil Kapton**. It does not directly support the modeled **α=.09 and ε=.65**. The patent describes the latter classical coating range, but the emittance statistic and Be transfer still need qualification. Fix the citation and retain the assumption label; do not silently equate normal and hemispherical emittance.

The [Sheldahl Red Book](https://sheldahl.com/wp-content/uploads/2023/07/RedBook.pdf), printed pages 65 and 67, supports bare silver/FEP masses 28/54 g/m² and adhesive-backed masses 88/115 g/m² for 0.5/1 mil. The modeled 5% overlap gives 92.4/120.75 g/m². The bare products already include metallization. Peel data on stainless steel do not qualify Be adhesion.

Bulk-density arithmetic does not establish deposited-film density, full-area coverage, added surface treatment, repair mass, wet optics, or installed adhesion. Those remain nonblocking NFIs.

## Thermal differences

The independent model solves coupled outer convection/radiation, core conduction, and gray inner-cavity radiation to convergence. Its written choices are explicit in `METHOD.md`. The owner describes 25 fixed iterations for legacy screening and a converged common model. The checker did not reproduce the missing implementation conventions from those descriptions.

At the old R10 source geometry, common-model reference040 values are:

| Field | Owner | Independent model |
|---|---:|---:|
| Day face gradient, K | 0.4227611395799613 | 0.47485709887945404 |
| Day curvature-temperature amplitude, K | 55.77743433326896 | 56.09230426656874 |
| Night curvature-temperature amplitude, K | 0.8066049556018386 | 0.41063492717972566 |
| Maximum outer temperature, K | 302.02481753419386 | 303.3783010927029 |
| Minimum outer temperature, K | 270.90519361594414 | 269.7355642937402 |
| Day/night swing, K | 31.119623918249715 | 33.64273679896269 |

The common independent balance residual for this row is about 2.02e-12 W/m². That verifies its own equations, not equivalence to the owner's model. The diagnostic also cannot reconcile the published subsolar and antisolar temperatures with one cavity radiation moment under the checker's assumed boundary conditions. Resolve the boundary/iteration conventions before attributing an arithmetic defect.

The source-geometry finish screens are:

| Finish | Day SF, owner / independent | Cycle SF, owner / independent | Cure-edge SF, owner / independent |
|---|---:|---:|---:|
| MLCCAg | 4.504429 / 4.454426 | 1.441504 / 1.359730 | 1.079085 / 1.066421 |
| CCAg | 3.512632 / 3.402132 | 1.395190 / 1.312789 | 1.092040 / 1.080207 |
| AgFEP05 | 2.359309 / 2.176276 | 1.305830 / 1.211106 | 1.122637 / 1.114101 |
| AgFEP1 | 2.678114 / 2.515827 | 1.336072 / 1.247632 | 1.111199 / 1.101237 |

All four still exceed the numerical day≥1.678 and cycle≥1 screens in this independent variant. Their factors differ, and no independently optimized account using these temperatures was completed. The legacy raw midpoint curvature has a constant-field projection artifact; the common model removes the mean. No physical conclusion is taken from the legacy curvature artifact.

## R10 reconciliation

At the owner's selected MLCCAg ISA, retained-floor, bake70 geometry, the independent account reproduces **+124.26191019077487 kg**, including exterior water **125.66370614359174 kg**, coating **10.471204774568298 kg**, structural primer **12.566370614359172 kg**, and added residual material water **0.13623828076349537 kg**.

The pinned reconciliation from the old **−109.64920782047648 kg** is:

| Payload change | kg |
|---|---:|
| Coating replacement | +240.85620751261519 |
| Additional structural primer | −12.566370614359172 |
| Faces | +6.932285271581804 |
| Core | −1.154044752943662 |
| Charged joining | −0.02072112487888944 |
| Added residual material water | −0.13623828076349537 |
| Other terms | 0 |
| Total gain | +233.91111801125177 |

The new endpoint bill is independently evaluated. The old 040 optimum and the independent end-to-end optimization of the reconciliation were not rerun before refusal. Thus the claimed gain is supported by the pinned bill decomposition and checked new bill, with thermal/optimization independence still open. It is not a drying credit for exterior water.

## Water trace and material accounting

The pinned 016 `INPUTS.json` explicitly calls the retained surface film **0.0001–0.001 m, owner assumption**. Its card discusses the 0.1 mm and 1 mm cases. MAINLINE-048 selects the lower endpoint: water density 1000 kg/m³ gives 0.1 kg/m². The sphere areas produce the stored 125.664/180.956/282.743 kg at R10/12/15, reproduced by the executed main-point account. This is a planning assumption, not measured drainage performance.

The R10 MLCCAg bake point's initial material inventory is:

| Component | Initial added water, kg |
|---|---:|
| AF163-2U | 0.3681263710594745 |
| Coated core | 0.4501181665149596 |
| Structural primer | 0.12566370614359174 |
| Finish | 0.10471204774568296 |
| Seam polymers | 0.31376251617124484 |
| Total | 1.3623828076349536 |

Its modeled 90% removal leaves 0.13623828076349537 kg and removes 1.2261445268714581 kg on the ground. The dry-gas point retains all its material water. The onboard-sorbent point retains that water and adds the independently reproduced **28.646250572344307 kg** bed/cartridge.

The historical NASA AF163-2U rows give WVR .09–.20% and TML 2.59–4.85% with different cures. NASA defines WVR as regain after the vacuum test and 24 hours at 25°C/50% RH; it is not an equilibrium installed-water isotherm. The model's .002 adhesive fraction is consequently a proxy. [NASA outgassing guide](https://etd.gsfc.nasa.gov/capabilities/outgassing-database/user-guide).

The 70°C preconditioning evidence concerns AF163-2M coupons cured at 121°C, not the installed 2U/200°F process. The fitted 8.72–9.16% uptake comes from hot immersion and is correctly a severe sensitivity. It does not establish the model's 90% dry-out target. [Yasuoka et al.](https://www.jstage.jst.go.jp/article/transjsme/88/916/88_22-00284/_article/-char/en).

Core, primer, seam-polymer and deposited-finish uptake, nominal volatile conditioning, desorption time, and sorbent capture at hull vacuum remain assumptions. Ground-energy, nitrogen-demand, dew-point, refined-volume service and additional sensitivity tables were inspected but their planned independent arithmetic was not completed.

## Vacuum discrepancy disposition

These are the only executed account fields outside tolerance:

| Field | Rows | Representative owner / checker | Disposition |
|---|---:|---|---|
| `vacuum.initial_gas_kg` | 7,149 | 0.5122158623775337 / 0.5121935085670086 kg at R10 | Checker used inherited density; dry-species molar convention proposed, rerun refused |
| `vacuum.gas_aboard_counted_kg` | 7,149 | 0.8126294370465615 / 0.8126070832360365 kg at first least point | Same initial-gas difference |
| `vacuum.desorbed_24h_kg` | 2,381 | Maximum stored difference +9.098811028138057 kg | Owner field appears to be net vapor after capture; checker returned gross release |

The largest initial-gas difference is −7.544411052196054e-05 kg at R15. The charged gas floor and pressure calculations already agree in the executed run. The dry-species/net-release amendments exist in the working source, but `account-02` never ran; they are **unverified proposed corrections to the checker**, not a passing rerun or established owner numerical errors. Rename the desorption field or document gross release and captured mass separately.

## Least sets and remaining work

The executed check reproduces the mechanics and mass at the owner's stored least-set witnesses and endpoint trials, including coefficient interpolation. It does not prove that a better geometry, smaller subset, or lower common usage is absent.

The owner's retained-water/retained-floor MLCCAg bake claims remain **pending independent search**:

| Radius and weather | Claimed least set | Claimed common usage |
|---|---|---:|
| R10 ISA | G+Q+film | 0.833076 |
| R12 ISA | G+Q | 0.884705 |
| R12 optimistic | G+Q+film | 0.928595 |
| R15 ISA | G+Q | 0.720757 |
| R15 optimistic | G+Q | 0.941833 |

The remaining negative-weather and no-floating-solution claims are also unverified as global search statements. `independent_search.py` was prepared but never executed or validated. The E-axis favorable bounds and supplemental sensitivities have not received an independent numerical check.

`NFI.json` lists specific next checks and evidence requests. They impose no hold on the owner's card. This filing does not close the full CHECK order. Resuming refused numerical work requires fresh queue authority; no retry is scheduled. No successor is named by CHECK. State: SLEEPING; no live own job.

Custody note: the live upstream `COMMON.md` changed after intake. The retained copy still matches the dispatch's exact pin and remains this check's basis. `SOURCE-DRIFT.json` records expected and current hashes; the package check reports this observation separately from required intake-copy and manifest verification. No source was silently refreshed.
