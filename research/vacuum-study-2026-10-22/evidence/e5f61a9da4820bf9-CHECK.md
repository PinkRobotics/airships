# Combined independent check: MAINLINE-032 and MAINLINE-032b

**QUESTIONABLE remains. Arithmetic reproduces; the measurement evidence needs the corrections below.** This report covers both filings and incorporates the immutable [032 check](64509e7ecbf1b4d6-CHECK.md). Its 236 comparisons remain valid. The new independent calculation passes all 297 engineering numeric/Boolean scalar checks in 032b: 228 numbers and 69 Booleans. Only the owner's elapsed-script-time number is excluded. [NUMERIC-CHECK.csv](3279a616c7ecd7d5-NUMERIC-CHECK.csv) gives every path, independently calculated value and difference. Passing arithmetic does not validate the meaning assigned to a source quantity.

The six original 032 artifact pins, five 032b artifact pins and sixteen prior-check artifact pins match. The owner's Python files were hashed, never read as code or executed. Both original owner reports, this fold order, and the earlier reviewer report are snapshotted under `inputs/`. All work is in this seat's own write root.

**032 calculation retained.** With the brief's rounded inputs,

\[
\sigma_u=\frac{0.82\sqrt{\eta E_fE_ct_f/t_c}}{1+0.64K_\delta},
\qquad K_\delta=\frac{\delta E_c}{t_cF_c}.
\]

At \(\eta=1\), inversion gives
\(\delta=(t_cF_c/E_c)(0.82/Q-1)/0.64\).
The [NASA CR-1457](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf) definition of \(F_c\) is the lowest of core flatwise compression, core tension, and core-facing bond strength. Substituting stabilized compression alone remains conditional. Hexcel's 35 psi is a **minimum average**, with a typical modulus; it is not a measured lower bound for an assembled Be panel.

| Face and required Q | Conditional Fc = 60 psi: δ, mm | Conditional Fc = 35 psi: δ, mm |
|---|---:|---:|
| S-200F, 0.371 | 0.152868766846361 | 0.0891734473270440 |
| SR-200, 0.609 | 0.0652229064039409 | 0.0380466954022988 |

The wrinkling interaction still gives \(b=0.6823278038280193\). Intracell dimpling uses its separate 0.5 equibiaxial factor, giving carried margins 9.0188536848 and 4.9753091211. Applying the wrinkle interaction once to waviness-adjusted capacity does not count waviness twice. These checks do not establish flat-panel-to-shell transfer.

Retain the earlier CARD correction: the **lead-only** δ/cell range at 60 psi is **0.00684754923–0.01604921437**. The owner's 0.0046–0.024 endpoints span all four typical-strength face/Q combinations, including crossed targets. The ten earlier findings, including rounded-Q effects, strength/thickness evidence, plasticity and measurement limitations, are retained in [NFI.json](fcb27bf7e1383d15-NFI.json).

**ER-1001: the quoted depth is real, and the coupon identities are recoverable.** The [primary NASA report](https://ntrs.nasa.gov/api/citations/19950020773/downloads/19950020773.pdf), printed pp. 19–21 and Figs. 22, 25 and 30, confirms:

| Source reading | Independent interpretation |
|---|---|
| Fig. 25, specimen 30 scan 1A: 0.000065 in | 0.001651 mm local dimple depth; 0.0108001133–0.0433940447 of the four conditional δ limits, as numbers |
| Fig. 24: 0.000057 in | 0.0014478 mm difference between neighboring cell-node elevations; a different quantity |
| Fig. 22, specimen 30 | **0.008 in = 0.2032 mm H19 face**, Crest 471 adhesive, 3/16-inch core |
| Fig. 30, specimen 32 | **0.008-inch face**, APS epoxy, 0.015-inch fillet; 3/8-inch core |
| Specimen 32 maximum slopes across scans | 0.5–1.6 mrad; the source supplies no matching depth statistic |

Thus the text pages omit some thickness information, but the report's figures supply it. The upper-slope sketches reproduce: \(sL=0.01524\) mm across one cell, \(sL/2=0.00762\) mm across half a cell, and \(sL/(2\pi)=0.00242552133272\) mm for a one-cell sine amplitude. These are projections, not observations. Dimple depth is crest-to-trough; halving it would produce a sinusoidal amplitude only under an additional shape assumption. The report describes nonsinusoidal profiles. None of these readings measures the target Be wrinkle component.

**Woody: correct the 3 μm attribution.** [Woody, Vail and Schaal (1994)](http://www.cso.caltech.edu/wiki/_media/cso/publications/1994-woody-procieee.pdf), pp. 675 and 684, supports the machined-core/epoxied 1 mm aluminum process and the 24 μm RMS fabrication figure. The stated metrology covers scales above 40 mm, with approximately 5 μm accuracy, point spacing below 40 mm and 10 mm diameter averaging. The roughly 2 μm finish below 10 mm is a sheet-finish statement, not an extracted bonded-cell amplitude.

The source's **3 μm RMS concerns adjustment of the parabolic template**. The 032b sentence attributing 3 μm to the sanded CSO surface against that template is unsupported. The text gives a 10 μm laboratory surface estimate. Table 2 distinguishes the individual budget contributions. A 10 mm averaging footprint filters a 9.525 mm periodic feature; it does not report that feature's amplitude or prove it absent.

**Von Hoerner: the number and its historical status both matter.** [NRAO report 30 (1969), p. 2](https://library.nrao.edu/public/memos/65/65R/65R_030.pdf) attributes the honeycomb figure to discussions with Rohr: 0.008 in RMS, printed as 0.20 mm. The exact inch conversion is 0.2032 mm, giving ratios 1.3292447123, 3.1154698741, 2.2787052210 and 5.3408054984 against the four lead rows. Those ratios reproduce. This is vendor whole-surface manufacturing RMS, not the report's own measured cell-scale honeycomb trace. It neither establishes a present-day process distribution nor identifies a wrinkle-band exceedance.

**Metric separation.** The 032b cell/short-wave/whole-panel split is useful, but “short wave” is not a fixed physical band. It must be tied to the selected failure model and measurement response. These quantities cannot be substituted for each other:

| Quantity | Conversion to a single sinusoidal zero-to-peak δ |
|---|---|
| One complete sine's RMS | δ = √2 × RMS |
| One sine's crest-to-trough depth | δ = depth/2 |
| Maximum slope of a sine with known full period Λ | δ = slope × Λ/(2π) |
| Whole-panel RMS, a local irregularity, or per-foot bow | No unique wrinkle-component δ without the shape, spatial band and reference surface |

For illustration only, 24 μm RMS would mean 33.9411 μm amplitude if entirely one resolved sine, still below 38.0467 μm. The paper's separate 35 μm installed nighttime upper-limit figure would give 49.4975 μm under that same assumption, above the smallest limit. Neither conversion identifies a measured component. RMS cannot bound an arbitrary local maximum, and an unresolved spatial band can be attenuated or missed.

**A conditional wavelength estimate makes the unresolved band concrete.** [NASA/CR-1999-208994, Eq. 19, printed p. 24](https://ntrs.nasa.gov/api/citations/19990017863/downloads/19990017863.pdf) gives the elastic symmetric flat-panel half-wavelength

\[
\ell=\pi\left(\frac{t_cD_f}{2E_c}\right)^{1/4},
\qquad D_f=\frac{E_ft_f^3}{12(1-\nu_f^2)}.
\]

This check evaluates it with the same brief geometry and \(E_f=290\) GPa, \(E_c=15\) ksi. The \(\nu_f=0\) idealization is consistent with the simplified 0.82 coefficient. The 0.33 column is only a sensitivity case, **not an asserted Be property**.

| Face | Half-wave, ν=0, mm | Full period, ν=0, mm | Full period, ν=0.33, mm |
|---|---:|---:|---:|
| S-200F | 19.27350839 | 38.54701677 | 39.67428985 |
| SR-200 | 18.35253559 | 36.70507118 | 37.77847820 |

These projected periods span about four 9.525 mm cells and lie below the paper's stated >40 mm metrology band. They explain why neither a single cell-depth measurement nor a broadband reflector RMS supplies the required δ. They are not measured wavelengths or a validated biaxial curved-shell eigenmode. The earlier wavelength finding is narrowed, not closed.

**An omitted measured thin-face example exists, with a material-system limitation.** [Rion's 2008 EPFL thesis](https://infoscience.epfl.ch/bitstreams/204993d8-6c72-4dca-a688-8293bdab6018/download), Table 3-3 and §§6.3–6.5, measures carbon/epoxy faces on Nomex: 0.07 mm per ply, 0.14 mm two-ply faces, 3.2 mm cells. Figure 6-11 has roughly 19–101 μm mean cell-depth readings, with scatter; these are approximate graph readings. Deliberately exaggerated single-ply specimens reach measured maximum depths of 160 and 370 μm under the two vacuum conditions, with some core-wall collapse. For the two-ply model, the 2.77 mm geometric half-wave is close to the calculated 2.79 mm critical half-wave. Crucially, the author uses an empirical \(W_\mathrm{meas}/W_0=25\), because the observed cell-local shape differs from the modeled wave.

Thus there is missed experimental evidence near **its own** wrinkle wavelength. It does not establish the proposed Be/CR-III modal amplitude, nor justify importing either the depths or the fitted factor 25.

[Camarda, NASA TM-81895 (1980)](https://ntrs.nasa.gov/api/citations/19810003663/downloads/19810003663.pdf), p. 23, Appendix A.3 and Fig. 46, supplies another omitted profile measurement: mean panel maximum waviness 0.0097 cm ≈0.097 mm (rounded separately as 0.0038 in). Forty-five points per face and curve fits produce panel maxima. The eight-ply faces average roughly 0.57 mm thickness. This is measured thin-face geometry used in a wrinkling comparison, but it is not a measured Fourier amplitude at the critical wavelength. No such matching Be/CR-III datum was found in this bounded search.

The previously read FPL 1810-A gives calibrated imperfection parameters; this check does not relabel those fits as direct profilometry. The 1999 NASA discussion of earlier measurement attempts motivated the original-source follow-up rather than supplying a new measured number by itself.

**AMS and completeness.** The retrieved three-page copy of [AMS7902G](https://img.antpedia.com/standard/files/pdfs_ora/20230614/SAE/AMS/SAE%20AMS%207902G-2018.pdf) is an SAE-authored document hosted by a third party. It confirms three classes and 0.020–0.250-inch sheet scope, but omits §3.5.5. The awkward “55 Ra” and parenthetic 63 microinches/1.6 μm are printed in the source; they are not flatness numbers. The [official SAE G listing](https://saemobilus.sae.org/standards/ams7902g-beryllium-sheet-plate-98be) and previously checked H listing establish revision context, not the unread class tolerances. No missing class value is invented.

The search followed the three assigned primary reports, NASA's wrinkling references, the Rion process-pressure experiment, and a precision-mirror abstract lead. The latter reports global optical RMS, not an obtained Be wrinkle-band datum; its full methods were not retrieved. This is a documented bounded search, not proof that no measurement exists anywhere. [SOURCE-AUDIT.json](ef235d78fdf386e5-SOURCE-AUDIT.json) and the pinned source manifest distinguish complete local PDFs, mirrored documents, reused sources, indexed-only leads and failed retrievals.

**Disposition.** File one combined report for 032 and 032b. Retain QUESTIONABLE and the existing Fc, plasticity, transfer and metrology findings. Add the source attribution correction, recovered coupon identities, omitted experiment, wavelength qualification, metric distinction and historical-evidence qualification. No successor job or out-of-band seat contact.
