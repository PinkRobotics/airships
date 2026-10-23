**MAINLINE-025 — ceramic strength and reliability evidence**

Research date: 2026-10-20. Scope: Hexoloy SA and monolithic CVD SiC; no procurement or vendor contact. Every material-property value below is **QUESTIONABLE** for the proposed tubes. Every unvalidated transfer, assumed stress field, and calculated risk threshold is **PROJECTION**. “Questionable” describes applicability to this design, not an assertion that the source measurements are wrong. The accompanying `reliability.json` preserves source-specific parameters, missing information, formulas, and calculated scenarios.

**No validated compression allowable or assembly failure probability follows from the available tensile/flexural data.** The supplied nominal midspan stress, 1,428.35 MPa compression with ±58.8306 MPa bending, remains compressive throughout the section: approximately 1,369.52–1,487.18 MPa compression. The tensile weakest-link calculations below therefore do not describe that nominal midspan state. They illustrate sensitivity to a hypothetical tensile field, including one that might arise at contacts or during another loading condition.

Saint-Gobain's [current SA material page](https://www.ceramicsrefractories.saint-gobain.com/materials/silicon-carbide-sic/hexoloy-silicon-carbide-material/hexoloy-sa-sic-material) reports typical four-point and three-point strengths of 380 and 550 MPa, and Weibull modulus 8. Its linked [2012 SA datasheet, page 4](https://www.ceramicsrefractories.saint-gobain.com/files/4731/download) instead reports modulus 10 alongside those strengths and 3,900 MPa compression. Its flexure footnote specifies **3 × 4 × 45 mm bars**. It does not give support/loading spans, sample counts, fitted characteristic strength, confidence bounds, or compression specimen geometry. The 380 MPa entry is **typical**, not explicitly a measured mean or characteristic strength. Keep the modulus-8 and modulus-10 versions separate; neither establishes a tube population.

An independent official dataset demonstrates the danger of mixing test modes. [NIST SRD 30, Z00297, material 9](https://srdata.nist.gov/CeramicDataPortal/Scd/Z00297), reporting Graves and Hecht's UDR-TR-94-136 (1995), lists room-temperature Hexoloy SA tensile strength **234 ± 50 MPa, tensile m = 5**, versus flexural strength **395 ± 19 MPa, flexural m = 9**, at 0.004 cm/s crosshead speed. The method describes 165 mm overall-length buttonhead tension specimens and 3 × 4 × 50 mm four-point bars. The tension gauge dimensions and interpretation of the ± values are not supplied by the retrieved record; no reference tension volume or characteristic strength is inferred from them.

CVD SiC is also not one calibrated material population:

| Source | Published quantity | Limits for this use |
|---|---|---|
| [PremaTech CVD sheet](https://www.prematechac.com/wp-content/uploads/2019/05/18437-CVD-Silicon-Carbide-Data-Sheet.pdf) | Four-point average/typical strength 415 MPa at room temperature; m = 11; scale factor β = 424 MPa; beam finish 0.5 µm RMS | No bar dimensions, spans, reference size, sample count, or tensile/compression tests. Do not attach an arbitrary reference volume to β. The average and fit need not describe an identical dataset. |
| [CoorsTek SiC material table](https://www2.coorstek.com/en/materials/silicon-carbide/) | PureSiC high-resistivity CVD MOR 468 MPa; low-resistivity MOR 517 MPa at 20 °C | Typical product table; retrieved official search extraction, with direct-page fetch timing out. No Weibull calibration or test size provided in that table. |
| [Hong et al., JMR 24 (2009), 1422–1434, Tables II/IV](https://www.researchgate.net/publication/250012990_Evaluation_methods_for_the_hoop_strength_of_small-sized_tubular_ceramic_components) | CVD miniature-tube internal-pressurization means 263 MPa (m = 5, n = 21) and 239 MPa (m = 9.7, n = 17) | Author-uploaded primary paper, DOI [10.1557/jmr.2009.0158](https://doi.org/10.1557/jmr.2009.0158). TRISO-process specimens, not the proposed large tubes or either commercial product above. |

For the two Hong populations, ID/OD/length are respectively 1.022/1.222/5.83 mm and 0.894/1.084/5.27 mm; the pressurizing insert is 3 mm long. Reported effective inner areas are 9.64 and 8.42 mm². The paper's 448/312 MPa surface-normalized scale entries are **not coupon characteristic stresses**. The illustrative calculations instead derive coupon scales from the reported means and m. Diametral “crush” loading in this paper measures hoop tensile fracture; it is not a measurement of homogeneous uniaxial compression strength. Inner and outer surface flaw populations can differ.

The methodological boundary is explicit in primary institutional guidance:

- [ASTM C1424-26, §§4.2–4.4](https://store.astm.org/standards/c1424) separates monotonic compression characterization from tensile weakest-link statistics, notes evidence that the latter need not describe compression, and warns that standardized coupons may not represent full-size products. Compression data still require statistically adequate testing.
- [NASA CARES/Life, TM-2003-106316](https://ntrs.nasa.gov/citations/20030014949) treats surface/volume flaw populations, multiaxial tensile fracture, and time-dependent crack growth using stress histories and measured parameters. [NASA TP-2005-212505, printed pp. 95 and 97](https://ntrs.nasa.gov/api/citations/20050237907/downloads/20050237907.pdf) directs significant compression to separate limiting methods and excludes purely compressive failure from its weakest-link model. A computed zero tensile hazard is therefore not survival evidence against compression.
- [NIST SP 960-16, third edition, compression-fracture discussion and Fig. 4.37](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.960-16e3.pdf) describes local tensile wing cracks under macroscopic compression, their growth/interactions, and eventual compression failure. The continuum tensile flaw model does not automatically capture this damage and splitting mechanism.
- [ASTM C1683-10(2024), §§5.3–5.8](https://store.astm.org/c1683-10r24.html) permits size scaling only under assumptions including consistent material/flaw populations, suitable flaw size, known stress distributions, and appropriate surface/volume treatment; estimated Weibull parameters carry sampling uncertainty. [C1239-13(2024)e1, §§1.3–1.4 and 5.2–5.4](https://store.astm.org/c1239-13r24e01.html) explains estimation, confidence bounds, competing flaws, and its stable-flaw/no-slow-growth assumptions. That is a historical revision: the catalog identifies C1239-26a as active, but its detailed page was not retrieved.
- [ASTM C1322-25, §§5.8–5.9](https://store.astm.org/c1322-25.html) explains why processing, machining, handling, and environmental damage must be identified by fractography, and why a surface-located fracture origin need not be a surface-distributed population.
- [ORNL/TM-2024/3438](https://info.ornl.gov/sites/publications/Files/Pub216010.pdf), an ASME working-group analysis of the **2023** III-5-HHB rules, discusses separate loading-mode allowables, environmental effects, and buckling (§5.16). Its subject is C/C and SiC/SiC **composites** for nuclear core components. It is useful qualification guidance, not an applicable monolithic-SiC pressure-vessel code or a basis for importing its numerical factors here. No applicable ASME monolithic-tube allowable was established in this search.

The following calculations are reproducible **PROJECTIONS for one specified short-term load exposure**, not lifetime reliability or design allowables.

For one identified tensile flaw population and one positive principal stress field, let `Q_eff` denote its stress-weighted volume or area, and let `s_c` be the **coupon** characteristic stress for effective reference size `Q_ref`:

```text
H = (Q_eff / Q_ref) (s_max / s_c)^m
P_failure = 1 - exp(-H)
s_c = mean / Gamma(1 + 1/m)                 [only if a Weibull mean is established/assumed]
s_target = s_c [ -ln(1-P_target) Q_ref / Q_eff ]^(1/m)
```

For independent series members, hazards add. With 1,047 members, equal allocation requires per-member failure probability 9.5511×10⁻¹⁰ for assembly 10⁻⁶, or 9.55587×10⁻⁷ for assembly 10⁻³. The rounded 1,046-member values are 9.56023×10⁻¹⁰ and 9.56501×10⁻⁷. Independence and identical flaw populations are assumptions. A conservative union-bound allocation `P_i ≤ P_assembly/N` does not require independence, but still requires justified marginal probabilities. Common batch defects, correlated loads, joints, and other failure modes require additional treatment and risk allocation.

Given `r_o = 0.123688362374 m`, wall `0.000880299093685 m`, and length `2.04 m`, one tube contains 0.00139066 m³ of ceramic. The supplied continuum count 1,046.0203946 gives 1.45465858 m³, inner area 1,646.56 m², and both cylindrical surfaces 3,304.92 m², excluding end annuli. A real integer assembly of 1,047 identical tubes contains 1.45602088 m³; the distinction is recorded in JSON.

For SA only, assume 380 MPa is a Weibull mean and assume four-point **40/20 mm outer/inner spans** on the manufacturer's 3 × 4 × 45 mm bars. The spans are an unverified assignment: [NASA/TM-2006-214089, Table 1 note 4](https://ntrs.nasa.gov/api/citations/20060008932/downloads/20060008932.pdf) documents that geometry in a C1161 experiment on different materials, not in the SA dataset. With width `b = 4 mm`, depth `h = 3 mm`, and simple beam theory:

```text
L_eff = L_inner + (L_outer-L_inner)/(m+1)
V_ref = b h L_eff / [2(m+1)]
A_ref = [b + h/(m+1)] L_eff
```

The area expression includes the bottom face and the tensile portions of both side faces, assuming one identical surface flaw population. The unstressed bar overhangs do not count. Using all 540 mm³ as uniformly tensile reference material would overstate strength. The volume and surface alternatives below are separate hypotheses; their hazards must not be added as though the same flexure dataset independently calibrated two populations. In a real material with separately characterized independent volume and surface populations, **add their hazards**, `H_total = H_volume + H_surface` (and other identified populations). Choosing whichever separate calculation gives higher strength is invalid; missing calibration is not evidence that a population's hazard is zero.

| Illustrative calibration and full-assembly tensile field | Effective coupon size | Derived coupon characteristic stress | Tensile threshold at assembly P=10⁻⁶ | At P=10⁻³ |
|---|---:|---:|---:|---:|
| SA m=8, uniform tensile volume | 14.8 mm³ | 404 MPa | **7.19 MPa** | **17.1 MPa** |
| SA m=10, uniform tensile volume | 11.9 mm³ | 399 MPa | **15.6 MPa** | **31.1 MPa** |
| SA m=8, uniformly tensile inner+outer surfaces | 96.3 mm² | 404 MPa | 8.20 MPa | 19.5 MPa |
| SA m=10, same surface assumption | 93.2 mm² | 399 MPa | 17.6 MPa | 35.2 MPa |
| Hong CVD A, uniformly tensile inner surfaces | 9.64 mm² | 286 MPa | 0.408 MPa | 1.62 MPa |
| Hong CVD B, uniformly tensile inner surfaces | 8.42 mm² | 252 MPa | 8.46 MPa | 17.2 MPa |

The commercial CVD β=424 MPa is deliberately **not** put through this table: its effective reference size is missing. The miniature CVD cases demonstrate process/tail sensitivity, not bounds on the commercial products. Their coupon scales are arithmetic implications of the reported sample mean and fitted m, not recovered original maximum-likelihood fits. The SA volume cases span assembly/reference-size ratios of about 9.82×10⁷ to 1.22×10⁸. That extrapolation, followed into a 10⁻⁶ assembly tail, has not been validated by these sources. No confidence-bound reliability claim follows from the point estimates.

Define a contact tensile coefficient explicitly as `C_t = peak positive principal tensile stress / nominal compressive membrane stress`; this differs from a peak compressive contact-pressure multiplier. Using 1,428.35 MPa as the denominator, the SA volume illustrations give `C_t = 0.00504` (m=8) or `0.0109` (m=10) at 10⁻⁶; at 10⁻³ they give `0.0119` or `0.0218`. These are conditional full-volume stress caps, **not contact allowables**. For an actual smaller tensile region with the same calibrated population, the threshold changes as `(Q_full/Q_contact,eff)^(1/m)`. Obtain that effective size from a resolved contact/bending stress field. Surface and volume hazards, tensile principal directions, edge populations, residual stress, and finite contact widths must be handled consistently; a one-direction uniform field is not automatically a bound on an arbitrary multiaxial state.

The next qualifying evidence would be production-representative tube/coupon tests with raw fracture data and origins, established surface/volume/edge populations and reference geometry, confidence-bounded fits, and separate compression/contact/buckling tests. Long-term survival additionally needs the specified temperature, environment, hold time, cyclic history, aging, slow-crack-growth and proof-test evidence. The present sources supply none of that for a 247 mm OD, 0.880 mm wall, 2.04 m tube population. Keep proposed compression limits of 100/200/380/1,000/3,900 MPa as explicit assumed scenario inputs; do not fabricate compression Weibull parameters or label 380 MPa flexural strength a compression allowable.
