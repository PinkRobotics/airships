# Reserve solver iteration and stopping provenance

The [published greedy-increment question](../../../docs/OPEN-QUESTIONS.md#greedy-reserve-increments) asks which station-aware stiffness and connection checks should replace the source reserve solver’s area steps before their mass enters a float comparison. This paper preserves that question without selecting replacement checks, copying step/guard/margin/mass values, executing the model or reconstructing logs.

The existing [`solve` source](../../../ship/model.js) defines candidate marginal-margin-improvement ordering per incremental mass, selected moves, working-state updates and a loop jointly conditioned on its margin predicate and iteration guard. Source guard exhaustion and margin-predicate satisfaction are distinct possible termination boundaries. The returned tuple contains working quantities and the current record; it does not itself report which predicate ended an actual run. Later `capMargin`/`guardC` growth is a separate phase and can change shared working state. None of this source provenance is observed convergence, an optimum proof, station-aware validation or an adopted physical check.

[PROVENANCE.json](PROVENANCE.json) pins the unchanged assigned source, and [EVIDENCE-MAP.json](EVIDENCE-MAP.json) identifies source spans by custody metadata without copying their numeric operands or executing expressions. It maps missing existing run/input-configuration/revision, per-iteration candidate/order/move/state records, guard/margin exits, stopping reason, convergence, later cap-growth records, raw custody, applicability and owner/adoption evidence. The [README](../../../README.md) states that no aircraft has been built or flown; repository checks and publication signatures are not physical observations.

| Evidence row | Requirement | Units | Current status |
|---|---|---|---|
| run-input-identity | Keep actual run and input configuration unresolved | run, configuration, revision and record identifiers | UNKNOWN |
| candidate-ordering | Keep actual candidate ordering record unresolved | candidate, iteration and record identifiers | UNKNOWN |
| selected-move | Keep actual selected moves unresolved | move, state, iteration and record identifiers | UNKNOWN |
| guard-exit | Keep actual guard termination unresolved | guard, exit, iteration and record identifiers | UNKNOWN |
| margin-exit | Keep actual margin termination unresolved | margin, exit and record identifiers | UNKNOWN |
| returned-state-reason | Keep returned source state distinct from stopping reason | return, state, reason and record identifiers | UNKNOWN |
| later-cap-growth | Keep later cap growth as a separate phase | phase, guard, state and record identifiers | UNKNOWN |
| convergence-applicability | Keep observed convergence and applicability unresolved | convergence, scope and applicability record identifiers | UNKNOWN |
| raw-record-custody | Keep actual iteration and terminal custody unresolved | raw record, custody and source identifiers | UNKNOWN |
| owner-adoption | Keep assigned owner and criterion adoption unresolved | owner, custody, criterion and decision identifiers | UNKNOWN |

Actual observations, values, run/iteration/terminal records, stopping reason, convergence, applicability, criterion and adoption remain null/UNKNOWN. Assigned custodian and owner remain null/UNASSIGNED. A source guard, margin condition or returned tuple cannot silently fill a missing actual terminal record.

This is prospective iteration-record provenance only. It runs no algorithm or model, performs no convergence or sensitivity experiment, synthesizes no iteration log, and selects no stopping criterion, solver, design, member, material, geometry, replacement check or procedure. It changes or generates no source, model, code, catalogue, schema, data or test. Reserve-basis accounting and differences, station/shoulder stiffness-transfer and laminate-property work remain separate; the published replacement-check question is unanswered.
