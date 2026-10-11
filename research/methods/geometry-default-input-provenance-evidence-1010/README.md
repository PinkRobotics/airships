# Geometry default input and article metrology provenance

The [model source](../../../ship/model.js) defines `shipGeom(diaM = null)`. Its local `dia` retains the declared `SHIP0.diaM` source identity when the argument is null, otherwise the supplied `diaM` identity. This is a source input contract, not a measured design/manufacturing dimension, validated drawing, chosen default or adopted argument. The source default value and all numerical geometry are omitted.

The returned `diaM` retains `dia`; `lenM`, `R`, `depthM`, `rIn`, `nLong` and `braceM` remain distinct source field identifiers. Their formulae, scale, counts and rounding are not reconstructed or evaluated. `ship0` passes its source `diaM` to `shipGeom`, retains local `g`, and returns it under `geom`. These lexical identities do not identify an actual configured article, input record, drawing or metrology correspondence.

[EVIDENCE-MAP.json](EVIDENCE-MAP.json) pins source-context span hashes and exact nonnumeric applicability fragments. [PROVENANCE.json](PROVENANCE.json) pins unchanged sources. The [member census](../../../docs/MEMBER-CENSUS.md) retains unresolved physical station lengths, sections and connections. The [README](../../../README.md) states no aircraft has been built or flown.

| Evidence row | Requirement | Current status |
|---|---|---|
| source-default-field | Retain declared source default field identity | UNKNOWN |
| null-versus-argument-contract | Retain null default and argument identities | UNKNOWN |
| returned-field-identities | Retain returned geometry field identifiers | UNKNOWN |
| caller-container-correspondence | Retain caller and returned container identity | UNKNOWN |
| article-configuration | Keep matched article and configuration unresolved | UNKNOWN |
| measurement-referenceframe | Keep metrology reference frame unresolved | UNKNOWN |
| calibration-uncertainty | Keep calibration and uncertainty unresolved | UNKNOWN |
| raw-source-custody | Keep raw source custody and revision correspondence unresolved | UNKNOWN |
| input-applicability | Keep actual input correspondence and applicability unresolved | UNKNOWN |
| owner-criterion-adoption | Keep owner criterion and adoption unresolved | UNKNOWN |

Actual article/configuration/drawing, measurement reference frame/instrument, calibration, raw source custody, actual source-version and input correspondence, uncertainty, applicability, criterion and adoption remain null/UNKNOWN. Assigned owner and custodian remain null/UNASSIGNED. A public source pin, repository checks and publication signature do not supply matched physical metrology or acceptance authority.

Membrane shape-volume, station section, cap-grid direction, fitting inventory, scale question, geometric member census and named-basis selector remain separate records. Their geometry derivations, bills, tables and numerical reconciliation are not repeated. Corresponding preceding owned candidates absent from this observed main base are not imported or treated as landed.

This paper copies or evaluates no numerical diameter, length, radius, depth, count, pitch, area, volume, mass, load, capacity or threshold. It reconstructs no source algorithm, formula, rounding, count or scale; chooses no argument, default, dimension or design; and executes no fixture, test, parity check, model branch or physical measurement. It supplies no manufacturing/operating guidance, procedure or campaign. Source/model/code/schema/catalogue/data/test and primary/remote/settings are unchanged.
