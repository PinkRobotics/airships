# Unpressurised source-state and physical record provenance

The [model source](../../../ship/model.js) declares `shipUnpressurised(g, wall, skel, totalT)`, obtains `ring` from `wall` and forms source jig/cradle/wind/clamp records. `skel` is named in its signature but is not read within that function body. Source arguments and conditional reference checks are not actual article, support installation, pressure-state or observed erection/parked/service-state evidence. No numeric jig count, threshold, wind, force, stress, capacity, mass, margin or SF is copied or evaluated here.

Its returned `stands` aliases `cradleOk`; `allOk` conjoins `cradleOk` and `windOk`. `erectionClampN` retains the `clampN` source record. `jigPoints` is a separate source record and is not an operand of `allOk`. These exact field identities do not establish a physically accepted jig, cradle, clamp or complete state. The operator-requirement/refuter-fix comment is attributed source context, not an original adopted requirement or a source-check correctness assertion.

`ship0` passes its `g`, `wall`, `skel` and `totalT` source identities into `shipUnpressurised` and returns the result under `unpressurised`. Its separate `checksPass` and `floatsAndStands` source context is retained: `floatsAndStands` refers to `totalT`, `liftSL` and `checksPass`, without referencing `unp.stands` or `unp.allOk`. The summary obtains a default source `mid` record and presents `stands` and `allOk` under distinct labels. This paper traces those expressions and labels without deciding their correctness, evaluating results or accepting a physical service state.

[EVIDENCE-MAP.json](EVIDENCE-MAP.json) pins exact nonnumeric fragments and lexical/caller locators without numeric operands or source-loop execution. [PROVENANCE.json](PROVENANCE.json) pins unchanged sources. The [member census](../../../docs/MEMBER-CENSUS.md) retains the unresolved physical station/section/connection boundary; the [README](../../../README.md) states no aircraft has been built or flown.

| Evidence row | Requirement | Current status |
|---|---|---|
| source-state-inputs | Retain conditional source-state arguments | UNKNOWN |
| source-jig-record | Retain source jig record separately | UNKNOWN |
| source-cradle-wind-flags | Retain cradle and wind source flags separately | UNKNOWN |
| stands-allok-caller-context | Retain flag and whole-ship return distinctions | UNKNOWN |
| article-state-pressure | Keep actual article state and pressure correspondence unresolved | UNKNOWN |
| support-installation | Keep matched support installation unresolved | UNKNOWN |
| load-boundary-environment | Keep matched load boundary and environment unresolved | UNKNOWN |
| observations-raw-custody | Keep observations and raw custody unresolved | UNKNOWN |
| calibration-uncertainty-applicability | Keep calibrated applicability correspondence unresolved | UNKNOWN |
| owner-criterion-adoption | Keep responsible owner and criterion adoption unresolved | UNKNOWN |

Actual article/state, support-jig/cradle/clamp configuration, load-boundary/environment/pressure-state, installation, observations, raw record, custody, calibration, uncertainty, applicability, criterion, adoption and physical acceptance remain null/UNKNOWN. Assigned owner and custodian remain null/UNASSIGNED. Source flags, repository checks and publication signatures cannot fill missing matched physical records.

Generic ground-handling, gust-load, nominal pressure-reference, ring/crimp, fitting-bill and declared/emergent-SF maps remain separate records. Their numerical checks, loads, property values, acceptance tables and procedures are not repeated. Corresponding preceding owned candidates absent from this observed main base are not imported or treated as landed.

This record selects no support, jig, cradle, clamp, loadcase, environment, procedure, operating limit or design. It performs no numerical copying/calculation, source-loop simulation, derivation, safety analysis, erection, campaign or test development, and asserts no source-check correctness. Source/model/code/schema/catalogue/data/test and primary/remote/settings are unchanged.
