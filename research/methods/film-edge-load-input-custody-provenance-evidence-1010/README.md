# Film edge-load input and installed panel custody provenance

The source `filmEdgeLoads(span, sf = LATTICE_SF)` has its own `span` and `sf` inputs and local `f = kelvinFaces(span)` identity. The selected `stockBuild` caller has local `spanM` and obtains local `loads` through `filmEdgeLoads(spanM)`. Its returned `governing` field refers to `loads.rows`; no row index or value is copied. These are lexical/default/caller identities, not actual configured inputs, acquired outputs or installed load-path correspondence.

The source comment frames bending, governing and a Python mirror. Those words are attributed source history, not newly proved correctness/equivalence, a physical result or installed-load qualification. No numeric value, load equation, tributary width, dihedral, panel tension or force is reconstructed or evaluated. No consumption of `PAD_R_M` or measured pad protection is inferred from names or comments.

[EVIDENCE-MAP.json](EVIDENCE-MAP.json) pins exact nonnumeric applicability fragments and source-context span hashes. [PROVENANCE.json](PROVENANCE.json) pins unchanged sources. The [model source](../../../ship/model.js) supplies conditional lexical context; the [member census](../../../docs/MEMBER-CENSUS.md) retains unresolved physical station lengths, sections and connections. The [README](../../../README.md) states no aircraft has been built or flown.

| Evidence row | Requirement | Current status |
|---|---|---|
| source-load-inputs | Retain own load input and default-label identity | UNKNOWN |
| local-face-namespace | Retain local face input namespace | UNKNOWN |
| stock-caller-loads | Retain selected stock caller and loads identity | UNKNOWN |
| historical-governing-mirror | Retain historical governing and mirror attribution | UNKNOWN |
| invocation-version-input-output | Keep actual invocation version and input-output unresolved | UNKNOWN |
| panel-attachment-frame-member | Keep installed panel attachment frame and member unresolved | UNKNOWN |
| material-lot-process-state | Keep matched material lot process and state unresolved | UNKNOWN |
| pressure-support-timebase | Keep pressure support and observation timebase unresolved | UNKNOWN |
| custody-calibration-uncertainty-applicability | Keep raw custody calibration uncertainty and applicability unresolved | UNKNOWN |
| owner-criterion-adoption | Keep assigned owner criterion and adoption unresolved | UNKNOWN |

Actual computational invocation/source version/span-sf-input configuration/output correspondence/raw custody remain null/UNKNOWN. Separately matched panel-film/attachment/frame/member/article/material/lot/process/state/pressure-support/observation timebase, calibration, uncertainty, applicability, criterion and adoption also remain null/UNKNOWN. Assigned owner and custodian remain null/UNASSIGNED. Source labels, repository checks and publication signatures do not supply installed-load qualification or pad-protection evidence.

Rim bending, pressure-reference, declared SF, strength, seam and fitting maps remain separate records. Their property/world/load/strength/geometry/bill tables and analyses are not repeated. Corresponding preceding owned candidates absent from this observed main base are not imported or treated as landed.

This paper records qualitative source input/default/local/caller and attributed-history identity only. It copies or evaluates no numerical span, pitch, SF, pressure, material, load, stress, margin or capacity and reconstructs no load equation, tributary width, dihedral, panel tension, force or proof. It chooses no load/input/design/support/allowable/criterion and executes no branch, model, parity check, fixture, native or physical run. It supplies no operating/test/campaign procedure. Source/model/code/schema/catalogue/data/test/history and primary/remote/settings remain unchanged; no new science, external or out-of-band action.
