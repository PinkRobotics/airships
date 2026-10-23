**MAINLINE-043 proof testing and cost class — QUESTIONABLE / PROJECTION**

A prospective proof programme must screen the finished curved member and its relevant stress states. No retrieved test qualifies a 3.184 m long, 275.083 mm OD, 1.137 mm wall P3 tube. The following is a qualification outline, not an executable acceptance specification. [NASA CARES/Life](https://ntrs.nasa.gov/citations/20030014949) supplies the relevant framework for proof loading, multiple flaw populations and subcritical crack growth; this card has not performed that full analysis.

The scalar idealization is useful but narrow. If strength S is unchanged by testing, a perfect proof at stress sp removes every part with S≤sp. At subsequent service stress s≤sp, instantaneous conditional failure is zero in that model. At s>sp it is `1−exp(−[(s/scale)^m−(sp/scale)^m])`. Proof rejects occur with probability `1−exp(−(sp/scale)^m)`. This mathematical truncation is not a lifetime guarantee. Handling damage, proof-induced damage, stress redistribution, untested orientations and environmental crack growth invalidate the zero-risk inference unless separately controlled.

**Stress coverage and test articles**

1. Establish the integer frame, load spectrum and resolved member/joint stress fields. Identify compression, bending, torsion, hoop stress, end bearing, adhesive peel, residual stress and possible tensile flaws separately. The current selected-point beam and joint proxy do not establish those fields.
2. Qualify finished parts from the intended manufacturing process and batches. Record curvature, bow, wall variation, machining, surface condition and end preparation. Use destructive tests and fractography to identify failure populations, then fit appropriate distributions with uncertainty. A tensile flexure fit cannot simply be relabelled a compression distribution; [ASTM C1424](https://store.astm.org/c1424-26.html) explains that limitation.
3. Develop a supported test fixture and load sequence that reaches the service-relevant stress field without introducing unrepresentative contact damage or masking dangerous flaws by confinement. Include the needed bending directions and end configurations. Demonstrate the relation between proof stresses and installed stresses, including stressed area/volume. A compression-only proof cannot screen an independently loaded tensile surface merely because its axial load is larger.
4. Qualify joints as assembled substructures, including preparation variability and environmental exposure. The source's approximately 44.19 kg CFRP joining estimate and 44.02 mm overlap have no resolved local reliability budget. Tube survival alone does not qualify approximately 866 end interfaces in a 433-member bookkeeping frame.
5. Establish 100% finished-member inspection and proof, identification, calibrated load/strain records, accept/reject rules, and post-proof inspection. Validate inspection sensitivity to the actual critical flaw populations. Restrict subsequent handling and processing to qualified operations.
6. Test representative service cycles, environment, aging and manufacturing changes; maintain batch traceability and surveillance. Prove that later damage and slow crack growth are covered by the service-life model. Define exposure duration before claiming a lifetime Pf.

The selected nominal axial force is 0.873771 MN; target is 1.099425 MN. Choosing, only as a scale illustration, proof force 1.25× target gives **1.374281 MN**. Its pressure-equivalent multiplier is q=1.572816. The source's local/global instability multiplier is only 1.258252, so an unsupported frame or member could encounter instability before that proposed screen. Neither the factor 1.25 nor a fixture configuration is endorsed as sufficient. Supported proof needs explicit validation of what it screens and what remains untested. An axial-force ratio also does not automatically give the same stress ratio when beam-column amplification changes.

**Statistical burden**

For 433 independent members, frame target Pf=10⁻³ allocates member Pf=2.31062×10⁻⁶; frame target 10⁻⁶ allocates 2.30947×10⁻⁹. Allocating P/n instead is a sufficient union-bound allocation without independence, but still requires valid member probabilities and allowance for other failure modes.

With zero failures in k independent representative tests, the one-sided 95% upper probability bound is `1−0.05^(1/k)`. Merely reaching the two member allocations by that route would require 1,296,504 and 1,297,151,426 tests. These are mathematical illustrations, not a suggested campaign. The practical case must instead combine physically justified failure laws, measured variability, validated screening and uncertainty analysis. A small high-m coupon dataset does not by itself validate billionth-level full-member tails.

Proof rejection rates and screened residual reliability are unknown because the matched distributions, proof fields and degradation law are unknown. The conditional examples in RESULTS.json are not yield or scrap forecasts.

**Cost class**

Qualification is **high/custom**: full-size curved thin-wall parts, destructive material and joint testing, a load system on the order of 1.4 MN for the illustrative screen, qualified multi-axis fixtures and supports, instrumentation, fracture containment, inspection validation, statistical analysis and environmental/life tests. This classification follows from the proposed geometry and load, not a vendor quote.

Recurring cost is also **high relative to accepting catalogue material properties alone**: 100% full-length proof and inspection, several orientations or load states if required, fixture handling, traceable records, joint process control and potential rejection of costly parts. The 433-member proxy implies hundreds of individual screens; the real mesh determines the count. Batch qualification and destructive surveillance add recurring work.

There is no justified currency estimate, cycle time, inspection detection probability, scrap percentage or supplier capability claim in the available evidence. No supplier was contacted, purchase requested, or test authorised by this outline. Those open quantities remain in NFI.json.
