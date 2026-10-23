**MAINLINE-043 — SiC frame reliability — QUESTIONABLE / PROJECTION**

P3's frame failure probability is **unknown**. The available evidence does not qualify today's SiC for this frame, and it does not prove the frame impossible. No retrieved candidate supplies a matched compression Weibull modulus, characteristic strength and reference size for the finished curved members. A catalogue compression strength divided by stress cannot establish a probability of survival. `qualified_frame_failure_probability`, qualified compression parameters and lifetime probability remain null in [RESULTS.json](598bc8854cf39bd5-RESULTS.json).

The selected CHECK-022d point reaches **1.19810 GPa peak longitudinal compression** at its target load, including its assumed L/1,000 initial bow. A joint-moment transfer sensitivity raises this to **1.26913 GPa**. Both fields remain longitudinally compressive. This does not resolve contact, circumferential stress, shear-induced principal tension or manufacturing residual stress.

For 433 independent identical members, if compression followed a scalar Weibull law with **m=10**, the uniform-peak envelope requires complete-member characteristic strengths **4.38651 GPa for frame Pf=10⁻³** and **8.75267 GPa for Pf=10⁻⁶**. Relative to an *assumed complete-member scale* of 3.9 GPa, these are 1.12475× and 2.24427×. Hexoloy-SA's 3.9 GPa is a typical catalogue compression value, not that measured scale. The actual improvement factor is therefore unknown.

**Evidence and the closest available grade**

| Candidate / population | Compression evidence | Tensile or flexural statistics | Reference-size limitation |
|---|---|---|---|
| Hexoloy-SA | Typical 3,900 MPa; compression m and scale absent | Manufacturer flexure 380 MPa, m=10 in 2012 sheet and m=8 on current page; treating 380 as a mean implies scales 399.432/403.507 MPa | 3×4×45 mm bend bars; spans and compression specimen size absent |
| Commercial CVD SiC, PremaTech | Matched compression statistics absent | Reported four-point m=11, scale 424 MPa; average 415 MPa | Test dimensions and effective size absent |
| Reaction-bonded SiC | Schunk CarSIK-G/Z typical compression 1,000 MPa; compression fit absent | Separate 2017 bend population: m=8.6, mean 280.7 MPa, derived scale 297.041 MPa | 3×4×40 mm bars, 30 mm three-point span; effective tensile volume 1.953125 mm³ under our stated stress integral |
| SiC/SiC | Separate 2.5D composite study: three compression coupons, average 460 MPa, no m/scale | Mini-composites: reported tensile m/scale 20.59/374.79 MPa and 5.01/400.74 MPa for two furnace batches | Compression coupons about 14.1×10.2×3.2 mm; tensile gauge 50 mm but area missing; populations and failure laws cannot be combined |

Primary evidence: [SA manufacturer sheet](https://www.ceramicsrefractories.saint-gobain.com/sites/hps-mac3-cma-pcr/files/assetbank_media/hexoloy-sa-sic-en-1013-tds-215398.pdf), [current SA page](https://www.ceramicsrefractories.saint-gobain.com/materials/silicon-carbide-sic/hexoloy-silicon-carbide-material/hexoloy-sa-sic-material), [CVD manufacturer sheet](https://www.prematechac.com/wp-content/uploads/2019/05/18437-CVD-Silicon-Carbide-Data-Sheet.pdf), [Schunk](https://www.schunk-group.com/technical-ceramics/en/materials/silicon-carbide), [RBSC study](https://www.powdermat.org/journal/view.php?number=1448), [mini-composite study](https://fhclxb.buaa.edu.cn/cn/article/doi/10.13801/j.cnki.fhclxb.20230217.004?viewType=HTML), [composite compression study](https://doi.org/10.1016/j.jmrt.2024.12.069).

Hexoloy-SA is the closest **catalogue compression candidate among the retrieved comparisons**, subject to making the required geometry. There is no defensible ranking by qualified frame reliability. Commercial CVD's reported tensile scale is promising evidence to pursue, but its missing reference dimensions prevent the required transfer. The higher mini-composite tensile m belongs to a different architecture and mode; it is not a compression solution for a monolithic tube.

[SOURCES.md](1250e75f1ca70223-SOURCES.md) and the 17 rows in [SOURCE-DATA.json](ceed140103a0b568-SOURCE-DATA.json) also cover NIST's direct-tension SA data, Morton CVD flexure, two miniature CVD coating-tube populations, and RBSC C-rings. Those records preserve sample sizes, dimensions, reported versus inferred scales and missing entries. A ring loaded by a compressive force can fail in hoop tension; such results are not compression Weibull fits. [ASTM C1424](https://store.astm.org/c1424-26.html) explicitly limits transferring tensile weakest-link assumptions to compression.

**Geometry and stresses**

The selected member is 3.18419 m long, 275.083 mm OD and 1.13736 mm wall. Its material volume is 3,116.831 cm³; inner plus outer cylindrical surface is 5.48079 m². The rounded 433-member assembly contains 1.34959 m³ and 2,373.18 m² of those surfaces. These sizes, rather than coupon dimensions, must enter a calibrated statistical transfer.

The source continuum count is 432.9863. Rounding to 433 supports risk arithmetic only: 433 edges cannot form a closed triangular spherical mesh, whose edge count satisfies E=3V−6. A 435-edge count is compatible with that identity but is not a constructed or solved replacement frame. RESULTS includes 433/435/480/1,080 allocation cases.

| Selected-point case | Axial compression, MPa | Bow bending, MPa | Added joint-proxy bending, MPa | Peak compression, MPa | Positive opposite-face longitudinal tension, MPa |
|---|---:|---:|---:|---:|---:|
| Operating, source bow | 892.656 | 54.722 | 0 | 947.377 | 0 |
| Operating, bow + joint proxy | 892.656 | 54.722 | 56.454 | 1,003.832 | 0 |
| Target q=1.258252, source bow | 1,123.186 | 74.910 | 0 | 1,198.096 | 0 |
| Target, bow + joint proxy | 1,123.186 | 74.910 | 71.034 | 1,269.130 | 0 |

The nominal and target axial loads are 0.87377 and 1.09942 MN. Target bow moment is 5.001 kN m. The joint proxy scales CHECK-026b's f4 end moment by the selected-to-f4 force and length ratios, giving 4.742 kN m at target. Adding aligned peak moments is a sensitivity assumption, not a selected-frame equilibrium solution or a bound on actual joint moments.

Independent recovery from frozen CHECK-026b displacements gives:

| Mesh | Members | Maximum longitudinal compression, MPa | Maximum bending contribution, MPa | Positive longitudinal tension, MPa | Estimated positive principal-tension cap from beam shear, MPa |
|---|---:|---:|---:|---:|---:|
| f4-m24 | 480 | 984.237 | 53.678 | 0 | 0.198 |
| f6-m24 | 1,080 | 906.098 | 59.265 | 0 | 0.422 |
| f2-m48 | 120 | 1,063.040 | 117.705 | 0 | 0.384 |

These meshes retain their own geometry. Each of the 1,680 members has forces, stresses and conditional probability columns in the three `MEMBERS-*.csv` files. The shear calculation is an ideal thin-beam estimate; it excludes joint contact and shell stresses. Column maxima need not occur on the same member or section.

The owner's rise-8 solution reports 177.825 kN m peak moment, 5.05649 GPa compression and 3.43968 GPa positive tension. Its force solution remains **independently unverified**: the earlier CHECK-026b rise job was refused admission and yielded no independent solution. Applying that same moment to the selected section gives 2.66358 GPa bending and 1.77093 GPa positive longitudinal tension at nominal axial load, but this is only a section conversion. It is not a solved selected rise-8 frame and is not merged into the nominal case.

With only the assumed initial bow, opposite-face tension begins at 47.743 mm bow at target, versus the assumed 3.184 mm. An imposed 50 mm bow gives 53.096 MPa peak tension; 60 mm gives 288.352 MPa. The manufactured spherical centerline is not an initial imperfection. Changing bow here does not requalify instability or fabrication tolerances.

**Member and series-frame probability — conditional projections**

For a specified stress field and calibrated flaw population, the calculation uses
`H_i=(Qeff/Qref)(stress/scale_ref)^m`, `Pf_i=1−exp(−H_i)`, and independent series `Pf_frame=1−exp(−sum H_i)`. Q is either effective volume or area. Surface and volume fits from the same bend data are alternative hypotheses, not two independently measured contributions. Size transfer requires compatible processing, flaw populations and stress fields; see [ASTM C1683](https://store.astm.org/c1683-10r24.html).

The following compression example assumes m=10 and scale=3.9 GPa, changing only the deliberately assigned reference size. Uniform peak compression fills each member; none of these rows estimates the actual frame probability.

| Reference assigned to the 3.9 GPa scale | Operating member Pf | Operating frame Pf | Target member Pf | Target frame Pf |
|---|---:|---:|---:|---:|
| Complete member | 7.15457×10⁻⁷ | 0.000309745 | 7.48635×10⁻⁶ | 0.00323635 |
| 100 cm³ coupon | 0.0000222993 | 0.00960926 | 0.000233310 | 0.0960988 |
| 1 cm³ coupon | 0.00222747 | 0.619235 | 0.0230636 | 0.999959 |

Neither coupon size is established for the manufacturer's compression number. Integrating the assumed axial-plus-sinusoidal-bow field reduces the 1 cm³-reference frame probabilities to 0.426009 operating and 0.996165 target, still entirely conditional. The large reference-size sensitivity is the reason the missing calibration cannot be hidden inside a single quoted Pf.

Using unequal f4/f6/f2 member stresses, the same m=10 complete-member-scale hypothesis gives operating series Pf 0.000348012 / 0.000301802 / 0.000210715; target linear stress scaling gives 0.00345618 / 0.00299788 / 0.00209394. The CSVs preserve every member's contribution. Linear target scaling does not solve nonlinear loss of stability.

For a tensile-volume example, take SA's 380 MPa typical flexure as an assumed mean, m=10, and assumed 40/20 mm bend spans. The derived coupon scale is 399.432 MPa and effective reference volume 11.9008 mm³. A uniform positive tensile stress throughout all members then gives:

| Uniform positive tension | Member Pf | 433-member frame Pf |
|---|---:|---:|
| 10 MPa | 2.53342×10⁻¹¹ | 1.09697×10⁻⁸ |
| 25 MPa | 2.41606×10⁻⁷ | 0.000104610 |
| 50 MPa | 0.000247374 | 0.101588 |
| 100 MPa | 0.223798 | Approximately 1 |

Localization changes the result: at 100 MPa and assumed effective-volume fractions 1%, 0.01%, frame Pf becomes 0.666119, 0.0109098. These fractions are sensitivity inputs, not measured contact areas. Under the same m=10 model, the positive-tension caps for Pf=10⁻³ / 10⁻⁶ are **31.333 / 15.703 MPa** for the full volume, or **36.382 / 18.233 MPa** under the alternative both-surfaces calibration. SA m=8 gives volume caps 17.216 / 7.260 MPa. The RBSC three-point population gives 12.478 / 5.589 MPa under its separate volume transfer.

The miniature CVD A/B populations give inner-surface caps 1.735 / 0.436 MPa and 17.842 / 8.753 MPa respectively. These are demonstrations of their own statistical transfers, not a ranking of commercial CVD against SA. Reference population and surface finish remain decisive. For the nominal beam's zero positive longitudinal stress, that isolated tensile-normal-stress model has zero hazard; the actual frame Pf remains null.

**Required strength and scatter**

The following requirements use 433 members, peak target compression 1.198096 GPa, and a hypothetical complete-member scalar compression distribution. A characteristic strength is a distribution's 63.2-percentile, not a minimum allowable.

| Assumed compression m | Required member characteristic strength for frame Pf=10⁻³, GPa | For frame Pf=10⁻⁶, GPa |
|---:|---:|---:|
| 5 | 16.060 | 63.942 |
| 8 | 6.068 | 14.390 |
| 10 | 4.387 | 8.753 |
| 11 | 3.898 | 7.305 |
| 15 | 2.846 | 4.511 |
| 20 | 2.292 | 3.238 |
| 30 | 1.847 | 2.325 |

Holding complete-member scale at an assumed 3.9 GPa instead requires m≥10.996 / 16.849. Thus there is a strength–scatter tradeoff, not a unique required pair. Adding the joint proxy at m=10 requires 4.64658 / 9.27161 GPa, or 1.19143× / 2.37733× the assumed 3.9 GPa baseline. If 3.9 GPa instead belonged to a 1 cm³ reference, required reference scales would be 9.80596 / 19.56644 GPa. The changes in interpretation must not be mixed.

For a separate uniform **100 MPa positive-tension** requirement, m=10 needs complete-member tensile scales 0.366123 / 0.730548 GPa. Transferring back through the assumed SA bend geometry requires coupon scales 1.27480 / 2.54368 GPa, approximately 3.19× / 6.37× the assumed 399.432 MPa reference. These demands scale linearly with the specified positive tensile stress; 100 MPa is a sensitivity, not the nominal beam result.

The property that must be demonstrated is the **lower-tail strength of finished members under their actual combined stress field and environment**. In the nominal scalar compression approximation, the member strength quantile at probability 2.30947×10⁻⁹ must exceed 1.19810 GPa to allocate frame Pf=10⁻⁶; the joint proxy raises that demand to 1.26913 GPa. This is a direct requirement on rare weak members. It could be addressed by improving characteristic strength, reducing scatter, or validated proof screening. Available data cannot say which improvement factor is physically achievable. Better catalogue mean compression alone does not close the tension, joining or instability questions.

**Proof, cost and disposition**

The prospective route is 100% finished-member proof with qualified compression/bending/end-contact coverage, separate representative bonded-joint qualification, inspection and traceability. For the 433-member bookkeeping case this means hundreds of full-length parts and about 866 end interfaces. A merely illustrative proof load of 1.25× target is **1.37428 MN** and corresponds to q=1.57282, above the source's 1.25825 local/global stability multiplier. Proof fixtures therefore need their own qualification; this is not a ready proof protocol. [PROOF.md](1c80acf8111b2d2e-PROOF.md) gives screening assumptions, failure coverage and a high/custom qualification and recurring-inspection cost class. There is no price quote.

The member probability allocation is 2.31062×10⁻⁶ / 2.30947×10⁻⁹ for frame targets 10⁻³ / 10⁻⁶. A simple zero-failure demonstration at 95% confidence would require about 1.30 million / 1.30 billion independent representative member tests; that illustrates why a small coupon batch does not validate this tail. The projections allocate the entire risk budget to tubes, omitting joints, membrane, instability, shared-batch defects and lifetime growth. A whole-frame or lifetime claim requires those contributions and uncertainties.

This card completes the source review, stress recovery, conditional probability calculations, inverse requirements and proof/cost assessment. It verifies 26 input pins and 210 numerical checks. Four one-core, 1 GiB postprocessing jobs were admitted and released; no new nonlinear FE solve was made. [METHOD.md](0ca71c04971b35b7-METHOD.md) defines the models, [VALIDATION.json](b2e8f58063e20b23-VALIDATION.json) records their checks, and [NFI.json](02a2f53e8d94208a-NFI.json) retains the unresolved qualification questions without blocking this report. The brief names no successor: file to sciences, cc co, xo and the robotics admiral, then SLEEPING.
