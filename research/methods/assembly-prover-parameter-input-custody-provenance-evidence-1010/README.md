# Assembly-prover input source versus actual run custody

This paper traces selected source input lineage in [tools/check_assembly.py](../../../tools/check_assembly.py) and its separately pinned [generator header namespace](../../../tools/gen_nodes.py). [CROSSWALK.json](CROSSWALK.json) records exact nonnumeric fragments, hashed lexical context and prospective missing records. [PROVENANCE.json](PROVENANCE.json) pins complete sources and revision. No prover run, manifest file or physical article is acquired.

The selected `main` read uses `MANIFEST`, `read_text` and `json.loads` to bind `manifest`, then `load_params(manifest)` binds `prm` and `params_source`. These are selected source input/caller names, not an exhaustive use inventory, actual invocation or verified file/configuration correspondence. Identical spelling elsewhere is not assumed to be the same lexical binding.

`load_params` has its own `manifest` parameter. When that manifest is truthy and its `paramsMm` is a dict, the source seeds `GEN_NODES_DEFAULTS`, updates with `manifest["paramsMm"]`, then updates with `EXTRA_PARAMS`. The exact order is defaults, manifest, extras: extras take precedence for overlapping keys. The returned `manifest.paramsMm` string labels this branch; it does not certify that every returned key originated in the manifest or in a printed part. Otherwise the source seeds defaults and updates extras, returning `gen_nodes defaults`. That label also does not imply an extras-free dictionary. No numerical values, complete parameter inventory, default design or geometry/proof formula is reproduced or evaluated.

The docstring wording that the prover measures “WHAT WAS PRINTED” and the rim-fallback comment remain attributed computational source wording and history. They do not identify fabricated parts, supply metrology, remeasure a bug, prove current correctness or establish successful physical assembly. The generator's `paramsMm` namespace is separately pinned source context, not an acquired manifest or matched print record.

| Provenance boundary | Missing original records |
|---|---|
| run-source-version-and-argument-custody | Original actual invocation/source-version and responsible argument/input custody. |
| manifest-digest-and-input-configuration | Original manifest digest/input configuration and correspondence tied to that run. |
| source-label-and-raw-custody | Original actual source-label/run record and preserved raw custody. |
| printed-part-serial-material-process-installation | Matched actual printed part/serial/material/lot/process/drawing/installation records. |
| metrology-calibration-uncertainty-and-applicability | Original metrology/calibration/uncertainty and source-to-article applicability. |
| owner-criterion-and-adoption | Actual responsible owner and adopted source/version/domain/criterion record when supplied. |

Actual invocation/version/manifest digest/input configuration/source-label record/correspondence/raw custody and separately matched printed part/serial/material/lot/process/drawing/installation/metrology/calibration/uncertainty/applicability/owner/criterion/adoption remain NULL/UNKNOWN. Proposed custodians are UNASSIGNED. Source labels, merge order and software gates cannot replace those original computational or physical records.

Generator-header, node-file, member-kind/socket, assembly-frame and whole-fitting maps remain separately cited by exact unit/candidate/output identity and recorded status. Q13 remains water-drafting/operational availability; assembly-source context is separately unnumbered. No imported result, repeated dimension/geometry/bill/count/acceptance tables or full build-path contract is supplied, and no signature/landing or physical applicability is inferred.

No input selection, default design, acceptance/operating/test/campaign guidance is developed. Existing source/model/code/schema/catalogue/data/test and scientific history remain unchanged. No manifest/file lookup, numerical defaults/parameters/results copying, formula reconstruction/evaluation, check/model/generator/fixture/parity/scientific/physical execution, freeze/proof/contract generation, external retrieval, native action or new measurement occurs. The unchanged [root README](../../../README.md) states no aircraft has been built or flown.
