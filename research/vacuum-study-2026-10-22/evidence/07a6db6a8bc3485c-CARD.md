# REVIEW-A2 — 058 / 061

058 needs two coverage-accounting fixes. Its pressure loads, temperature
gains and displayed whole-bill bands reproduce. The saved site counts
also reproduce exactly, but use hull mass without the hardware required
by the named relief/ballast configurations.

| Configuration | Filed full-day coverage | With declared P2 hardware |
|---|---:|---:|
| P2 R10, MLCCAg relief/ballast | 63.979% | 61.253% |
| P2 R10, AlAOC relief/ballast | 83.647% | 79.854% |
| P2 R12, AlAOC relief/ballast | 95.785% | 94.156% |
| P2 R20, AlAOC relief/ballast | 99.269% | 98.960% |

For P3 standard-pressure climb, adding only its 5 kg valve changes R10
77.747% to at most 76.482%, and R12 96.994% to at most 96.881%.
The matched bladder still needs a mass specification.

No correction was demonstrated in 061's selected arithmetic. Its six
favorable density factors, two R30 handbook factors, fixed-family P3
negative mass bound, TRL7 column correction and Be-content comparison
reproduce. R12 ISA P2 has +4.616 kg under the declared TRL7 account.

Thirteen claims reproduce, two differ, and two cannot be checked without
further evidence: the complete-hardware minimum-radius selection and the
best-product ranking. Density-only is independently mass-closing at the
supplied witness; no global-optimality claim is made.

Proposed fixes remain **unreviewed**. Physical qualification, P3's cold
screen, chronological trim operation and installed finish properties
remain open. The original 061 PROCESS-v2 pin was verified; the later
replacement is not an owner fault. No owner code was read or run.

Full claim register: `REVIEW.md` / `RESULTS.json`. Fixes: `FIXES.json`.
Limits and evidence needed: `NFI.json`. All conclusions retain
QUESTIONABLE / PROJECTION status.
