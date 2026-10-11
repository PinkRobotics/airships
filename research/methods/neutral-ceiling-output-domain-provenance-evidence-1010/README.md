# Neutral ceiling output and physical domain provenance

The [model source](../../../ship/model.js) defines `shipNeutralCeilingM(massT, liftSLT)` and refers to `rhoAir`. Its historical comment frames a highest ISA altitude, the ledger's own law and deterministic/parity-held context. Those words are attributed source framing, not a newly demonstrated maximum, search correctness, fresh parity result or physical operating clearance. This paper pins the function context without reconstructing its algorithm, reproducing numeric operands or evaluating an output.

`shipBand` obtains conditional source `r1` from `ship0`: `crush` retains `r1.totalT`, and `liftSL` retains `r1.liftSLT`. Its returned `neutralCeilM` calls `shipNeutralCeilingM(crush, liftSL)`. Keep that conditional crush-ledger caller context distinct from an actually manufactured configuration, observed mass/lift, meteorology, flight condition or adopted altitude envelope. The separately returned `ship0` fields `totalT`, `liftSLT` and altitude-related field identifiers retain source bookkeeping only. Digits inside source field names are identifier characters, not copied altitude values or physical flight conditions.

[EVIDENCE-MAP.json](EVIDENCE-MAP.json) pins exact nonnumeric fragments and hashed identifier/caller context. [PROVENANCE.json](PROVENANCE.json) pins unchanged sources. The [member census](../../../docs/MEMBER-CENSUS.md) retains the unresolved physical station/section/connection boundary, and the [README](../../../README.md) states no aircraft has been built or flown. Conditional reference density is not an atmospheric observation, and source output attribution is not an accepted operating domain.

| Evidence row | Requirement | Current status |
|---|---|---|
| source-output-framing | Retain historical output framing as attribution | UNKNOWN |
| helper-input-density-identity | Retain helper input and reference-density identity | UNKNOWN |
| band-caller-domain | Retain conditional band caller context | UNKNOWN |
| separate-ship-ledger-fields | Retain whole-ship ledger fields separately | UNKNOWN |
| article-mass-lift-custody | Keep actual article configuration and mass/lift custody unresolved | UNKNOWN |
| atmosphere-timebase-domain | Keep matched atmosphere timebase and reference domain unresolved | UNKNOWN |
| raw-validation-custody | Keep raw validation and custody unresolved | UNKNOWN |
| calibration-uncertainty | Keep calibration and uncertainty unresolved | UNKNOWN |
| physical-applicability | Keep physical output applicability unresolved | UNKNOWN |
| owner-criterion-permission | Keep owner criterion and operating permission unresolved | UNKNOWN |

Actual article/configuration, mass-lift record, atmospheric observation, timebase, reference domain, raw validation, calibration, uncertainty, custody, applicability, adopted criterion and operating permission remain null/UNKNOWN. Assigned owner and custodian remain null/UNASSIGNED. Source output, repository checks and publication signatures cannot fill those missing records or authorize physical flight.

Atmosphere-reference, declared/emergent-SF adoption, mission-timebase, reference-pressure-domain and unpressurised-state maps remain separate preceding records. Their tables, numerical reference reconciliation and acceptance fields are not repeated. Corresponding owned candidates absent from this observed main base are not imported or treated as landed.

This paper supplies no route, weather, altitude, flight or operating guidance and selects no threshold, clearance, safety basis, design or procedure. It copies or evaluates no numerical altitude/pressure/density/mass/lift/iteration/cap/output value, performs no derivation or reconstructed search, executes no search/parity test and asserts no source correctness. It develops no campaign or physical work. Source/model/code/schema/catalogue/data/test and primary/remote/settings are unchanged.
