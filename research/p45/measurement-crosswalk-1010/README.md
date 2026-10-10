# Conditional stiffness: assumption and measurement crosswalk

This is a prospective paper method. No cord, termination, joint or installed assembly has been measured here. Actual stiffness, mass, chi, confidence and physical applicability remain NULL or UNKNOWN. The [source paper](../assumed-stiffness/README.md) and its historical limitations remain unchanged.

[CROSSWALK.json](CROSSWALK.json) maps every row of the [existing input contract](../assumed-stiffness/inherited/INPUT-CONTRACT.json) to an observation, its units, the existing field it could populate, and a falsification or inapplicability condition. The embedded toy and material stipulations are copied verbatim from [ASSUMPTIONS.json](../assumed-stiffness/ASSUMPTIONS.json); they are not new results. Every observation, evidence identifier and uncertainty record is absent, and every evidence owner is UNASSIGNED. Roles describe prospective responsibilities, without appointing a person or authorizing a test.

| Existing contract | Prospective evidence | What remains unavailable without it |
|---|---|---|
| C01, C02 | As-built identities, attachment datum, orientation, force/displacement calibration and work-preserving coordinate registration | Graph-to-hardware correspondence and compatible operator comparison |
| C03 | Matched cord force/strain, active length, loadbearing area, density, construction/lot/state and material ratings | Actual cord compliance and material applicability; tangent stiffness alone does not establish strength |
| C04 | Separate cord strain and relative motion at both installed terminations, including seating and nonaxial coupling | Each end allowance and any independent-series simplification |
| C05, C06 | Full local excitation/response, support boundary and crosssite load-transfer observations with uncertainty | Complete assembled connection allowance; diagonal or isolated-end measurements cannot establish it |
| C07 | Registered pretension, tautness, contact, environment, load/history and their admitted envelopes | Transfer of a tangent operator between states |
| C08 | The preceding compatible uncertainty envelopes and measured geometry, applied to the inherited symbolic condition | Conditional local retention; proposed area and compliance remain coupled |
| C09 | Frozen reference, retained members, constraints, nullspace quotient, condensation, prestress and uniform lower-operator evidence | Global retained-stiffness comparison; local identification cannot establish it |
| C10, C12 | Coverage by construction/state/lot, explicit population/confidence/applicability target and assigned traceable evidence ownership | Population inference or qualification from a single local configuration |
| C11 | Complete measured flight-item inventory, duty/overlap ownership and supported replacement evidence | Reconciliation against the same symbolic additions pool or actual budget fit |

The toy chi is a stipulated target, never an observed installed-property field. Cord modulus and density stipulations are distinct from traceable material observations. Reference graph counts do not measure installed hardware. The anchor allowance covers the complete assembled response, both endpoint sites, support and crosssite effects once; it cannot be duplicated into separate site allowances or separate fixture budgets.

A prospective finding can reject a premise when the registered uncertainty envelope contradicts it. Missing excitation rank, unmatched state, unresolved coupling, an unregistered reference or absent population coverage leaves the comparison inapplicable. None of these conditions creates a new numeric acceptance tolerance. A failed sufficient condition does not prove that every alternative design is impossible. Evidence and scientifically justified sampling would be needed before any physical claim.

The existing fields are destinations for future registered evidence, not writes performed by this paper. Where the current source has only a contract-row actual placeholder, the prospective observation would belong to that row; this crosswalk does not invent an installed density or state field in the source schema. The [limitations](../assumed-stiffness/inherited/LIMITATIONS.json), source inputs and scientific data stay intact. [PROVENANCE.json](PROVENANCE.json) pins the public local sources and revision. No private result, solver output, physical test or new numeric result is included.
