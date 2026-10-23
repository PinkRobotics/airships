# CHECK MAINLINE-026b

**The independently solved linear factors, discrete masses, payloads and baseline forces pass. Independent rise-8 verification remains open after a host admission refusal.** The new nonlinear first-loss fields should remain null. All physical inputs and results are QUESTIONABLE; ideal joints, fabrication and film/load-transfer assumptions are PROJECTION.

No owner code was read, extracted, imported or executed. The independent calculation starts from the pinned written equations and source section/allowance rows. It rebuilds the icosahedral subdivision, curved-member geometry, integrated beam stiffness, conservative pressure derivatives and constrained eigenproblem. [METHOD.md](7799f53a0b9fc3c1-METHOD.md) describes the calculation; [VALIDATION.json](bb7870a8515df6b3-VALIDATION.json) records the checks.

There are **3,618 passing independent field comparisons**, including member-force populations after matching the endpoint convention. A further **18 passing arithmetic checks depend on owner-supplied rise or nonlinear outputs** and do not independently validate those states. [NUMERIC-COMPARISON.json](fb9ff8da9a5cf65c-NUMERIC-COMPARISON.json) keeps those categories separate. [COVERAGE.json](f44df81535b9d36c-COVERAGE.json) assigns every load-bearing card row a status.

| Frequency | Owner discrete factor | Independent factor | Continuum at nominal bay | Difference from continuum |
|---|---:|---:|---:|---:|
| 6 | 6.465222443853 | 6.465222443850 | 6.127639734403 | +5.50918% |
| 4 | 5.254643802209 | 5.254643802209 | 6.193381346112 | −15.15711% |
| 2 | 2.183661359086 | 2.183661359101 | 6.876245150203 | −68.24340% |

The independent f4 refinements are 5.259242805183 → 5.255473022805 → 5.254643802209 at 6/12/24 segments. The f2 refinements are 2.185422854234 → 2.184010557041 → 2.183661359101 at 12/24/48 segments. Final changes reproduce −0.0157782% and −0.0159888%. The largest relative difference in the three final factors is below 6.73×10⁻¹². The eigen residuals are retained separately; close agreement between implementations does not establish physical model completeness.

The continuum values using actual mean arc length also reproduce: 6.245997, 6.204250 and 7.156132. Nominal half-wave/bay ratios are 1.480615, 1.058295 and 0.571412. The departure from the continuum comparison therefore persists. Frequency and section both change across these cases; these three points do not establish a universal continuum cutoff.

| Frequency | Tubes, kg | Joints, kg | Nodes, kg | Total vehicle, kg | Carried sag, kg | Remaining payload, kg |
|---|---:|---:|---:|---:|---:|---:|
| 6 | 4567.702932 | 228.385147 | 7.240 | 4950.843078 | 0 | −61.400928 |
| 4 | 4086.652452 | 213.716708 | 3.240 | 4588.050858 | 0 | 301.391292 |
| 2 | 3745.246593 | 204.747148 | 0.840 | 4399.690098 | 187.937933 | 301.814120 |

These totals use true circular member lengths and preserve each source's film, system and joint rule. The last two payload headrooms over 244.472108 kg are 56.919185 and 57.342012 kg. The f4 zero sag entry means uncharged sag. The f2 debit is inherited, not solved. Neither these allowances nor the pressure fan establish actual displaced volume or fabricated vehicle mass.

The endpoint rigidity ranks are independently 1080, 480 and 120 for f6/f4/f2, leaving six endpoint rigid motions. Each curved member has an independent roll about its endpoint chord, giving the stated 1080/480/120 internal ball-pin mechanisms. A finite 0.05-rad roll preserves endpoint positions, segment lengths and relative director/chord geometry. No positive ball-pin reserve is inferred.

The baseline mean member compressions reproduce **550.519239, 822.952926 and 1617.337670 kN** for f6/f4/f2. The f6 maximum member mean is 588.079206 kN. All twelve five-valent-node incident means reproduce 460.621779 kN, with adjacent endpoint axial values 460.638281 kN. At nominal s=2.04 m, pRs/(2√3)=562.166273 kN and pRs/2=973.700547 kN. At the actual mean arc, the triangular estimate is 551.513652 kN.

One definition needs clarification. The owner's `member_endpoint_chord_thrust` samples the **first endpoint in the stored member orientation**. Independent end-force recovery from the completed baseline solutions reproduces that choice. Averaging both ends produces these different means:

| Frequency | Owner first-end mean, kN | Independent both-end mean, kN |
|---|---:|---:|
| 6 | 548.641657 | 548.650355 |
| 4 | 816.156815 | 816.219567 |
| 2 | 1562.995245 | 1564.326572 |

These are sampling differences, not an axial-force error. [ENDPOINT-AUDIT.json](34feeef3c9efbdc4-ENDPOINT-AUDIT.json) contains both ends and confirms the first-end reproduction using this check's displacement solutions. [MISMATCHES.json](330d783a63051a92-MISMATCHES.json) lists six exact mean/maximum differences and the unresolved fields. Name the convention explicitly or publish both ends.

The resource gate refused the independent f6/m12/rise8 run at **memory PSI some avg10=7.89**, against the admission threshold **<5.00**. Nothing started for that request. No solver was retried or launched by another route, and the m24 rise8 request was not submitted. Eight earlier jobs succeeded and released their reservations, including the baseline f6/m24 solve. Subsequent work used completed data for scalar audits and report preparation. [EXECUTION.json](1060268b6301e8af-EXECUTION.json) and the refusal receipt [source link unavailable in this public projection] preserve this limitation.

Consequently, the owner's **538.899 kN rise8 compression, 569.788 kN chord thrust, 177.825 kN·m moment, 4.248 GPa bending and frozen-load force results are not independently solved here**. The moment-to-stress calculation, mass formula using the supplied raised length, and reported refinement ratios reproduce as conditional arithmetic. This does not verify the raised geometry, pressure fan or equilibrium. The claim of no eightfold thrust reduction is not contradicted, but this check cannot mark its exact rise forces reproduced. [RISE-AUDIT.json](b0083b506d4666c4-RISE-AUDIT.json).

For nonlinear results, the four reported crossing values reproduce only as midpoints of the owner's supplied brackets. The f4 path contains the documented near-zero triplet at λ=5.059945 followed by a positive nearest-zero triplet at 5.080744. Shift-invert selection near zero is distinct from smallest-algebraic selection, so neither f4's 5.082444 nor f2's 2.218113 establishes first loss. [SciPy eigsh definitions](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.linalg.eigsh.html). The top-level nulls are correct. Raw files still describe “first loss” and reference an m6 check without qualifying the new frequencies; downstream readers need the explicit top-level override. No independent nonlinear solve was performed. [NONLINEAR-AUDIT.json](d8fc4082fb896e1c-NONLINEAR-AUDIT.json).

Eight nonblocking checker issues are retained in [NFI.json](598492b5e2ba7f1f-NFI.json), including the rise execution gap, nonlinear verification, endpoint definition, film/sag, joints and physical model scope. This report completes the check with those coverage limitations visible. The brief names no successor; return to SLEEPING after filing.
