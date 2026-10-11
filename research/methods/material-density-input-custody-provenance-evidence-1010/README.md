# Representative material-density input custody provenance

This paper traces declared source-density inputs in [ship/model.js](../../../ship/model.js), without turning them into actual article/lot measurements or installed mass evidence. [CROSSWALK.json](CROSSWALK.json) records exact nonnumeric fragments and caller identities alongside prospective missing records. [PROVENANCE.json](PROVENANCE.json) pins the complete public sources and revision.

The module `MATERIALS` contains separate `M60J_LAM`, `T700_LAM` and `CFF` object properties named `rho`. The existing M60J description says the density is a prior mixture estimate; the T700 description retains prior representative inputs. The CFF description retains a prior representative density and explicitly says it is not the datasheet plaque density. The nearby typical coupon/plaque strength descriptions do not supply actual article density or license property transfer. No density, mixture fraction, strength, modulus or mass value is copied.

The existing Toray and Markforged reference URL strings are pinned as source identities in the crosswalk, separately for the tensile and compression source properties. They identify source strength references, not independently verified density records. No external page was retrieved and no current vendor-source validity is inferred.

`shipSection` references `MATERIALS.T700_LAM.rho` directly. `shipWall` and `shipSkeleton` each capture that same module property into a distinct local `rho` binding. Separately, module `SHIP0.rhoSpoke` is a declared spoke-density input, referenced by baseline `spokeT` and nested `solve`'s `kgSp` within `shipSkeleton`. This traces lexical/caller identity only; it does not infer that the spoke input equals any MATERIALS row, measure a cord, compute source accounting or repeat reserve-growth or P45 cord-stiffness analysis.

The [member census](../../../docs/MEMBER-CENSUS.md) says its tonnes price unchanged model sections including existing allowances, without resizing or checking those sections. Unknown mass is never zero. Source accounting does not establish actual process/state/configuration density or installed inventory.

| Provenance boundary | Missing original records |
|---|---|
| original-source-and-mixture-derivation | Original density source/domain and applicable mixture derivation identity, assumptions and custody. |
| actual-material-lot-article | Actual material, lot and article identity tied to source revision and responsible custody. |
| process-state-and-configuration | Matched process, state and configuration records with actual density applicability. |
| raw-density-measurement-and-custody | Original unmodified actual density measurement/raw record and acquisition/custody context. |
| calibration-uncertainty-and-applicability | Applicable original calibration, uncertainty and matched source/article/domain records. |
| responsible-owner-criterion-and-adoption | Actual custodian, responsible owner and adoption source/version/domain/criterion when supplied. |

Actual material/lot/article/process/state/configuration, density record/raw measurement, original mixture derivation/source domain, calibration/uncertainty/applicability, custodian/owner/criterion/adoption remain NULL/UNKNOWN. Custodian roles are proposals and UNASSIGNED. A source name, estimate, typical plaque description, URL or passing software check does not supply those records or physical qualification.

Conditional laminate stiffness/strength and whole-hull fitting maps are named separately by unit/candidate/output identity without assuming landing or importing their results. Q11 dry-mass reconciliation, P45 cord stiffness, joint allowances and retired-skin bill provenance remain distinct; no repeated maps, installed mass, geometry or inventory inference is supplied.

No material, density, loadcase, criterion, design, campaign, check or test procedure is selected. Existing source/model/code/catalogue/schema/data/test and scientific history remain unchanged. No numerical copying/calculation, mixture derivation/comparison/sensitivity, source/model/equation/generator/fixture execution, external retrieval, native/physical action, new measurement or scientific result is supplied. The unchanged [root README](../../../README.md) says no aircraft has been built or flown.
