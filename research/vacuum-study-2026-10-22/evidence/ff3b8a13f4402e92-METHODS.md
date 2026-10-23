# Independent CHECK of MAINLINE-022d

Authority: `ord-admiral-rr2-check022d-codex-1693-1020`. This completed check uses the owner's filed documents and numerical witness data. No owner program was read, copied, imported or run. Prior MAINLINE-026/026b scientific outputs remain frozen; the new order does not resume the refused 026b run.

The input manifest identifies each copied file, its original path, byte length and SHA-256. The four governing brief pins match the order. Only data and prose were taken from the owner. Source PDFs retrieved for this check have separate URL, retrieval-time and hash receipts in `web-sources/SOURCES.json`.

## Arithmetic

`independent_model.py` was written from the declared equations. The independent inputs to each witness are its case and four physical variables: chord spacing, outer tube radius, target pressure multiplier and total film gauge. All section properties, masses, demands, capacities, stresses and half-wave quantities are then reconstructed.

The two force rules follow the membrane resultant pR/2. For three equilateral member directions, the summed direction-cosine factor gives resultant √3N/s and hence N=pRs/(2√3). For two orthogonal directions it gives N/s and N=pRs/2. The curved member length is 2R asin(s/2R).

Both Zylon plies enter the total film gauge and mass. Only half that gauge is available in each idealized tensile direction. With 5.8 GPa times the assumed 0.6 knockdown, the effective capacity per unit total gauge is 1.74 GPa.

At every candidate multiplier q, each joint end has axial area qN/σ and overlap qN/(2πrτ). The checker multiplies those dimensions by material density and twice the member count. This directly derives joint mass, independently of the reduced coefficient C=ρ/(2πστ). The resulting axial and bond multipliers equal q by construction. The percent-joint cases retain their stated mass rule and have unknown joint capacity.

Tube area comes from the residual tube budget. To avoid reproducing the same cancellation patterns, the checker uses I=A(rₒ²+rᵢ²)/4 and t=(A/π)/(rₒ+rᵢ). It rationalizes the cap sagitta. It derives the tensile and extreme-compression roots with stable quadratic formulas, then checks those roots independently by bracketing the signed stress equations below the Euler pole.

The cap mean is also integrated over its circular footprint. The triangular membrane mean is integrated in barycentric coordinates. An independent square double-sine series checks the declared square-membrane coefficient. These calculations verify the chosen surrogates; they do not establish a physically matched pressure-loaded membrane.

## Coverage and tolerances

The final arithmetic run checks 64 primary witnesses, 112 sensitivity witnesses, four duplicated headline witnesses, eight local-bending diagnostics, all 1,792 numeric cells in the primary CSV table, eight independently solved active-equation cases and geometric identities. It records 17,452 comparisons.

The default numerical tolerance is an absolute term plus 2×10⁻⁹ times the larger magnitude. The absolute term is 3×10⁻⁹ for SF, constraint and SF-difference fields; 0.05 Pa for stresses; 10⁻⁸ kg for nested mass fields; 10⁻²⁵ for the very small joint coefficient; and 10⁻¹² for other scalars. Active-equation locations use 10⁻⁷ absolute tolerance. Every comparison, its exact inputs, difference, tolerance and result is retained in `FIELD-CHECKS.json` and CSV. `MISMATCHES.csv` is the complete failed-comparison subset.

The final result has zero primary-witness or primary-table failures. Its 50 failed comparisons all concern the documented versus output-implied square-membrane coefficient in 16 sensitivity rows. The full difference ledger is retained, even though the largest resulting least-SF change is below 4×10⁻⁹.

The first checker run used provisional names for eight public joint fields and an overly generic absolute tolerance for near-zero SF differences. Those checker issues were corrected before the final comparison. That development version and its output remain archived in `development/arithmetic-01/`; its provisional mismatches are not reported as owner errors.

Owner optimizer timings, iteration histories and internal verification counts are historical execution metadata, not independently derived physical outputs. This check supplies its own execution receipts and comparison counts.

## Independent searches

`independent_optima.py` uses the independently written physical model in 880 SLSQP searches across all 176 cases: one filed-witness start and four independently specified starts per case. Film gauge remains a free variable. Standard and expanded search bounds follow the documented case. The search feasibility threshold is 2×10⁻⁸ and the material objective-difference threshold is 10⁻⁶.

Every case has an independent-start result within 10⁻⁶ SF of the filed optimum. No materially better witness was found. Eight Zylon/equilateral optima were additionally solved from their active equations using coarse initial guesses. These results corroborate numerical optima of the stated surrogate; a mathematical global certificate remains absent.

Two individual local-search attempts returned a non-success solver status while remaining within the recorded feasibility tolerance. Their full records are retained, and each affected case also has successful independent-start solutions.

## Source calculations and limits

`source_arithmetic.py` integrates the assumed bend-bar stress field to recover the tensile reference volumes. The original 1,046.0203946-member continuum reference gives 7.191893634 and 15.585636721 MPa for the m=8 and m=10 assumptions, explaining the carried 7.192 and 15.586 MPa rounded inputs. The separate 1,047-member example gives 7.191052170 and 15.584177866 MPa. These references must not be silently interchanged. Both depend on uncalibrated size-transfer hypotheses.

The local-shell source calculation explicitly exposes the inherited coefficient and radius convention. Using ν=0.14 and the mid-surface radius at the fixed headline geometry would give local SF 1.229307846, versus the declared-model value 1.258252477. This is a hypothetical convention sensitivity, not a replacement optimum or a validated ceramic model.

The frequency-4 026b comparison is arithmetic on frozen, previously filed linear-frame results: 5.254643802209333/6.1933813461115825−1 = −15.1571087172215%. It is an applicability NFI for continuum transfer. It does not authorize a nonlinear rerun or establish a universal multiplier correction for the different 022d geometry.

## Execution

Every scientific invocation used `simjob.py run` with one CPU core, a 2 GiB memory cap, CPU-only environment and single-thread numerical libraries. Technical watchdogs were 600 or 1,800 seconds; there was no work or phase time budget. Each invocation has exact source pins, command, start/end clocks, stdout, stderr and release receipt under `execution/`.

Five invocations were admitted and completed. There were no refused admissions for this check. The second source calculation resolved the continuum-versus-rounded reference count; both versions are archived. Packaging, hashing and source retrieval were administrative operations.

Reproduce with the own `run_job.py` wrapper: `audit_witnesses.py`, `independent_optima.py`, then `source_arithmetic.py`, each with a new execution label and fresh admission. A refusal requires stopping and filing it; it does not authorize a retry.

The qualification fields remain null. Open technical issues are assigned NFI rows and do not stop other authorized cards. CHECK names no successor.
