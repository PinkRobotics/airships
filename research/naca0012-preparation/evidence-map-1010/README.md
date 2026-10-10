# NACA0012 validation evidence map

This prospective map records what would be required to evaluate the frozen preparation. No solver output, experimental agreement, relaxation improvement or hull qualification is supplied. All result values and evidence identifiers remain null/UNKNOWN.

[EVIDENCE-MAP.json](EVIDENCE-MAP.json) maps each frozen condition to named evidence rows, its unchanged source value and a rejection condition. Its condition coverage includes the case identity, hypothesis, reference selections, evaluation contract and tolerance extract. The original output fields remain unfilled. [PROVENANCE.json](PROVENANCE.json) pins the unchanged public sources.

The authoritative case and settings are [CASE-CONTRACT.json](../CASE-CONTRACT.json); the bands and formulas are [TOLERANCES.json](../TOLERANCES.json). [Preparation](../README.md) supplies their interpretation and [source provenance](../PROVENANCE.json) distinguishes original and derivative identities. This map neither changes those files nor authorizes execution.

| Evidence row | Decision supported | Units | Current status |
|---|---|---|---|
| geometry-domain | Geometry and domain applicability | m; dimensionless | UNKNOWN |
| frozen-mesh | Frozen mesh identity | identifiers; m^3 | UNKNOWN |
| solver-model | Solver and turbulence applicability | identifiers; m^2/s | UNKNOWN |
| normalization | Reference-state and force normalization | dimensionless; deg; m/s; m^2/s; kg/m^3; m; m^2 | UNKNOWN |
| controlled-pair | Controlled hypothesis comparison | digests; dimensionless coefficients | UNKNOWN |
| normal-exit | Normal terminal collection | exit and collection records | UNKNOWN |
| force-series | Force-series completeness | iterations; dimensionless | UNKNOWN |
| force-window | Final-window selection | iterations; dimensionless | UNKNOWN |
| force-range | Relative vector range | dimensionless | UNKNOWN |
| force-deviation | Maximum vector deviation | dimensionless | UNKNOWN |
| force-reference | Primary force agreement | dimensionless | UNKNOWN |
| trip-sensitivity | Trip sensitivity | dimensionless | UNKNOWN |
| mesh-family | Three-mesh evidence | identifiers; dimensionless | UNKNOWN |
| mesh-vector | Last-two force vector criterion | dimensionless | UNKNOWN |
| mesh-drag | Last-two drag criterion | dimensionless | UNKNOWN |
| mesh-lift | Near-zero and nonzero lift criteria | dimensionless | UNKNOWN |
| mass-flux | Mass-flux balance | dimensionless; mass/time | UNKNOWN |
| pressure-state | Pressure-reference state mismatch | dimensionless; deg | UNKNOWN |
| pressure-domain | Pressure-reference domain | x/c; dimensionless | UNKNOWN |
| pressure-rms | Pressure RMS agreement | dimensionless | UNKNOWN |
| overall | Complete validation conjunction | status record | UNKNOWN |
| hull-transfer | Airship-hull applicability | scope record | UNKNOWN |

Normal native exit and collection, complete finite series, exact final window and both force metrics are separate requirements. Reference agreement additionally needs the matching physical state, selected tripped data, bracketing interpolation and both absolute-error bands. Alternate grit sensitivity remains separate; a reference match is not evidence that the relaxation hypothesis improved a compatible baseline.

Three-mesh, geometry/domain, positive-volume, turbulence and mass-flux evidence remain required even if force convergence and force agreement are eventually shown. Near-zero absolute and nonzero relative lift branches stay distinct. No branch cutoff or farfield equivalence is invented here; its applicability must be evidenced from the frozen source basis.

Current-case pressure remains diagnostic because its Reynolds number differs from the pressure reference. Matching pressure evidence must retain upper-surface handling, original reference rows, predeclared domain exclusions and trip/model disclosure before its unchanged RMS band can be applied. Missing applicable evidence leaves complete validation UNKNOWN. An airfoil benchmark does not establish airship-hull applicability.
