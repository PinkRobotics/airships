# NACA0012 preparation

This record specifies a controlled iteration hypothesis and its evidence requirements. It supplies no solver outputs, experimental agreement, physical qualification or airship-hull conclusion. Quantities requiring results remain NULL/UNKNOWN in [CASE-CONTRACT.json](CASE-CONTRACT.json).

The declared case is alpha0°, Re6 million, the fixed n449 mesh and eight-rank decomposition, with OpenFOAM14 incompressibleFluid and fully turbulent Spalart–Allmaras closure. The frozen hypothesis changes only U equation matrix relaxation from0.7 to0.5; p remains0.3 and nuTilda0.7. Geometry, mesh, schemes, closure, reference selection, time controls and all other settings stay fixed. Damping iteration updates is a hypothesis, not a predicted result or an identified cause.

[CASE-INPUTS.json](CASE-INPUTS.json) lists the121 frozen field/mesh/dictionary input names, sizes and digests. It records identity, without embedding mesh or field contents. The baseline and candidate fvSolution digests in the contract distinguish the sole proposed numerical setting change. This preparation does not modify either case.

## Comparison criteria

[TOLERANCES.json](TOLERANCES.json) is a scientific extract of the previously frozen project bands. They are comparison criteria, not measurement uncertainty, and are not fitted to an output. Require a normal collected solver exit and a complete finite4001-row, six-column force series at iterations0..4000. The final window is3801..4000 inclusive,200 rows. Both the relative vector range and maximum vector deviation divided by mean-vector norm must be strictly below0.005. Missing, invalid or nonfinite values and zero normalization cannot establish convergence.

At the matching force-reference state, use the selected80-grit Ladson Mach0.15 tripped data and the declared bracketing interpolation. Absolute CL error must be at most0.05 and CD error at most0.002; report120/180-grit spread as sensitivity using the same bands. Agreement with a reference is separate from evidence that changing relaxation improved the result: the latter needs a compatible matched baseline.

The Gregory pressure reference is at Re2.88 million. A Re6 million pressure trace is diagnostic only; it cannot establish experimental pressure agreement with that reference. A matching pressure comparison needs its own state and disclosed trip/model applicability. Preserve the stated upper-surface domain handling and RMS band in the tolerance extract.

## Evidence beyond a single force trace

Full applicability additionally requires the registered reference geometry and domain, positive cell volume, mass-flux balance, turbulence inputs and closure, three-mesh comparisons, normal collected exit and each applicable pressure check. The farfield requirement is approximately500 chords or a demonstrated equivalent. Retain geometry findings rather than infer qualification from a force match. The last-two-mesh vector/CD and near-zero versus nonzero CL criteria remain separate in the frozen bands. Missing evidence leaves its gate UNKNOWN.

The contract leaves force metrics, experimental errors, a matched baseline, three-mesh evidence, geometry, mass flux, cell volume, matching pressure error and overall validation unfilled. A two-dimensional airfoil benchmark does not qualify an airship hull. No new experimental result, mesh or tolerance is supplied here.

[PROVENANCE.json](PROVENANCE.json) uses repository-relative extracts and distinct original/derivative digests. Scientific selections and input identities are retained; operational metadata and unrelated historical dispositions are outside this paper.
