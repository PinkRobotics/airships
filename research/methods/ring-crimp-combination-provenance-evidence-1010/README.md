# Ring/crimp reciprocal combination provenance

This paper traces the existing conditional source combination in [ship/model.js](../../../ship/model.js). It records source identity and missing evidence for applicability; it supplies no measured coupled ring/crimp response or accepted failure model. [CROSSWALK.json](CROSSWALK.json) holds exact nonnumeric locators, lexical/caller context and prospective record requirements. [PROVENANCE.json](PROVENANCE.json) pins the full sources and revision.

Within `shipSkeleton`, `crimpOf` has its own `aTheta` parameter and captures the declared material and geometric context from its parent. Its nonpositive-input guard and shear-to-pressure return are source assumptions. The sibling nested `gi` has a separate `aTheta` parameter and passes it to `crimpOf`, storing the result in local `qCrimp`. `solve` passes its local `aTh` as that argument; the ordinary caller supplies the enclosing configuration. These are lexical and caller identities, not measured material, member or connection response.

In the `gi` mode-loop block, `qRing` first names the ring expression. The next assignment overwrites that same binding: when both the initial ring term and `qCrimp` are positive, the source uses reciprocal combination; otherwise the combined contribution is source zero. The later sum `qRing + qFound + qMem` uses the already combined `qRing`. The foundation and optional membrane terms remain separate. The returned `qCrimpPa` names the uncombined crimp term. No numeric constants, pressure, stiffness, capacity, mass or margin quantities are copied or evaluated. The source branch result is not a physical absence statement.

`capMargin` is a separate source domain. Its own `aTheta` parameter goes through shared `crimpOf` into `sCap` and `qCapCrimp`; the latter combines with separately defined `qCapBend` under its own positivity guard. Source knockdown and pressure/safety-factor normalization remain in the original expression. This traces the domain distinction without repeating cap geometry, topology, reserve iteration, world selection or margin analysis.

The [member census](../../../docs/MEMBER-CENSUS.md) states that the checks use smeared areas at full radius and do not resolve station lengths, sections or connections. That limitation remains. Unknown mass is never zero. The unchanged [root README](../../../README.md) says no aircraft has been built or flown.

| Provenance boundary | Missing original records |
|---|---|
| original-combination-derivation-and-reference | Original derivation, reference article, source domain and assumptions tied to the reciprocal combination. |
| actual-member-section-connection-configuration | Matched actual member, section, connection and configuration records with source revision correspondence. |
| load-boundary-and-interaction-domain | Applicable load/boundary conditions and interaction-mode/domain correspondence. |
| matched-validation-and-raw-custody | Original validation/raw records, acquisition context and responsible custody. |
| calibration-uncertainty-and-applicability | Applicable original calibration, uncertainty and domain/applicability records. |
| responsible-owner-and-adoption | Actual responsible owner and adoption source/version/domain/criterion when supplied. |

Actual original derivation, reference article, source domain, member/section/connection/configuration, load/boundary conditions, interaction mode, validation/raw/custody/calibration/uncertainty/applicability, responsible owner, adoption and criterion remain NULL/UNKNOWN. Custodian roles are proposals and UNASSIGNED. A source formula, comment, parameter name, positive branch or passing repository check cannot supply those records or establish physical qualification.

The crosswalk names separate smeared/discrete, laminate and reserve provenance maps by unit/candidate/output identity without assuming their landing or reproducing their analysis. Optional hardware credit, GI knockdown campaign, cap topology and P2 diagnostic-mode outcomes also remain separate. No numerical outcome is imported from them.

No combination/failure model, geometry, member, section, connection, material, loadcase, criterion, check, procedure or design is chosen. Existing source/model/code/catalogue/schema/data/test and scientific history remain unchanged. This is static prospective paper preparation: no model/equation/generator/fixture execution, new derivation/calculation/comparison/experiment, native or physical action, new measurement or scientific result.
