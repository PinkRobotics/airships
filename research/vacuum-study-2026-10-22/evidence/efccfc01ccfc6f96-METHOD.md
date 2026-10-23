**MAINLINE-043 fold-041 method — QUESTIONABLE / PROJECTION**

The fold uses the two `best_closure_by_reserve` frequency-5 witnesses in the pinned MAINLINE-041 RESULTS.json. The 5% witness names `resize/f45-m24/f5/sample-000/RESULTS.json`; 019 names sample-001. Their associated `arrays.npz` files are pinned through the filed 041 manifest. The arrays contain segment compression N, segment maximum end-moment magnitude M, segment-to-member identifiers, member maxima, and each complete member's two correlated end N/M/T triplets. No peer code is imported or executed.

The samples use approximately 0.001 m² area. The final closure witnesses use smaller areas with unchanged gyration. We use each final A, I, ro and wall with the sample force arrays, retaining 041's scaling identity: scaling A and I together at fixed gyration leaves linear pressure-induced internal forces invariant. This is not an independent equilibrium verification. Reproducing the source's final-section stress and mass values checks the intended correspondence and avoids using the reference sample's thicker section.

Each point has 750 actual members, 252 joints, 500 cells and 24 segments per member. Per-member material volume is `A L_i`; inner-plus-outer surface is `2π(ro+ri)L_i`. Arc lengths are taken from the source geometry, not from an average-spacing formula. The complete-member probability scenario assigns a common characteristic strength regardless of unequal lengths; the coupon-calibrated scenario instead includes each actual volume explicitly. They are distinct hypothetical calibrations.

**Mechanical scoring**

For every segment s of member i, the owner convention is independently implemented as:

```text
lambda_E,s = pi² E I / (L_i² N_s)
axial_s(q) = q N_s / A
bending_s(q) = q (M_s + N_s L_i/1000) ro / [I(1 − q/lambda_E,s)]
compression_s = axial_s + bending_s
positive_longitudinal_tension_s = max(0, bending_s − axial_s)
```

E=410 GPa, density=3,100 kg/m³ and the final witness sections are retained. The L/1000 bow is an assumed imperfection relative to the stress-free manufactured arc. Bending magnitudes and bow are conservatively aligned and both magnified. The FE end moment is already in M; adding the old 043 joint proxy would double-count a separate approximation. A source-dependent maximum end magnitude does not resolve local contact or a multiaxial joint stress tensor.

We group segment stress extrema by actual member identifier. Thus correlated N and M remain paired at each segment before maximization; maxima of N and M are not first combined from different locations. Per-member maximum stress is then used uniformly over the entire member for the reliability envelope. Within a monotone positive scalar stress-power law this overestimates the hazard of the same bounded stress field. It does not bound unknown contact stresses or validate the law.

Loads are q=1, each point's own screened multiplier, and q=1.2582524765581682 from the original 022d point. The last is expressly above both new source screens. The three loads answer different questions and are never presented as equally admissible design states. No nonlinear equilibrium, instability, fracture or geometry resize is solved.

The minimum initial bow for longitudinal tension follows from
`ecrit_s = I/(A ro)(1−q/lambda_E,s) − M_s/N_s`.
All scored nominal fields remain longitudinally compressive. That does not imply an all-compressive principal-stress field; shear, hoop/contact and residual-stress inputs are missing here.

**Conditional probabilities**

The hypotheses use independent scalar Weibull member hazards:

```text
H_i = ratio_i (stress_i / scale_reference)^m
Pf_i = 1 − exp(−H_i)
Pf_frame = 1 − exp(−sum_i H_i)
```

For complete-member calibration, ratio_i=1. For compression coupon sensitivities, ratio_i=A L_i / Vref, with deliberately assumed Vref=1 cm³ or 100 cm³. The common 3.9 GPa reference scale and all tested compression moduli are assumptions. The manufacturer's typical number supplies neither this scale nor a calibrated compression m. The frozen 043 source review [source link unavailable in this public projection] retains those distinctions and the primary evidence.

We report two spatial envelopes: each member at its own maximum stress, and every member at the frame-wide maximum. The latter is higher within the same model. The old 022d values are copied verbatim from the frozen 043 results for its identical-member bow-only envelope. Its optional joint proxy remains available in the prior data. Comparing new own-screen rows to the old own-screen row changes both load multiplier and mechanical model; common-q rows are supplied to expose the load-level effect.

For target P, htarget=−ln(1−P). A common characteristic scale is
`[sum_i ratio_i stress_i^m / htarget]^(1/m)`.
We normalize stress by 1 GPa before exponentiation for numerical range, then restore units. Holding scale=3.9 GPa, a scalar root solves
`sum_i ratio_i (stress_i/scale)^m=htarget`.
All stresses in those inversions are below the hypothetical scale, making the hazard decrease with m. There is a strength–scatter tradeoff, not a unique required pair.

Equal independent allocation gives `1−(1−P)^(1/750)` per member. P/750 is instead a sufficient union-bound allocation when dependence is unspecified and valid marginals are available. The equal allocation is sufficient, but the summed unequal-stress calculation need not assign equal failure risk to every member.

Tensile scenarios retain the exact reference sizes, scales and population distinctions from 043. Full-volume, both-surfaces and miniature-CVD inner-surface populations remain separate alternatives. Fractions 1, 0.01 and 0.0001 are assigned effective stressed fractions, not measured contact patches. Uniform hypothetical positive tensile stress is applied to each fraction; the nominal zero positive longitudinal stress only sets this isolated mode's hazard to zero. It does not establish actual system probability.

All headline probabilities omit joints, membrane, instability, common-cause batch flaws, unresolved multiaxial stresses and lifetime degradation. Actual member/frame/lifetime probabilities remain null. No new material evidence or calibration is claimed.

**Verification and provenance**

`fold.py` independently implements the postprocessing. Its 843 checks cover exact section/volume identities, topology and grouping, source FE-only and amplified extrema, Euler and axial screens, end-demand maxima, conservative-envelope ordering, and inverse strength/scatter/tension calculations. These validate numerical correspondence and arithmetic, not full physical reliability.

`run_job.py` admits the calculation through the local `tools/simjob.py run --cores 1 --mem 1G` policy, with one thread per numerical library and no GPU. One job, `fold-01`, completed and released. It has command, source pins, clocks, stdout and stderr under execution/. No task or phase time cap was imposed; the launcher used its ordinary technical watchdog. No admission was bypassed or retried.

`INPUTS.json` records 26 verified input copies, including both reports, the fold order, the earlier 043 evidence, and the specific 041 samples and explanatory code. The earlier 043 artifacts are unchanged. Six member CSVs contain 4,500 rows in total: 750 members × 2 designs × 3 load cases. They are six stress states of 1,500 design-specific members, not 4,500 distinct members.

The numerical calculation can be reproduced by running `python3 run_job.py <new-label>` under the same admission policy. Reproduction would write this supplement's generated results; it never modifies the prior 043 package or any foreign seat. A resource refusal does not authorize bypass or retry.
