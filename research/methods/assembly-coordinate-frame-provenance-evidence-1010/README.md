# Assembly coordinate-source context versus installed metrology custody

This paper traces selected source namespaces in [tools/gen_nodes.py](../../../tools/gen_nodes.py). [CROSSWALK.json](CROSSWALK.json) records exact nonnumeric fragments, hashed lexical context and prospective missing records. [PROVENANCE.json](PROVENANCE.json) pins complete sources and revision. Assembly is an unnumbered source boundary; Q13 remains water-drafting/operational availability.

Inside `main`, selected `pos_of`, `R`, `v` and `t` declarations/calls locate the position/extraction context. The selected per-node `write_stl` call is separate from the optional `args.assembly` branch. That branch uses `world`, a `pos_of[u]` consumer and `asm_v`/`asm_t` buffers; a separately guarded `article.stl` writer references the stacked buffers. Bare declaration/call fragments locate names only and are deliberately incomplete: they do not define a transform or offset formula. These are selected source identities, not an exhaustive caller/use inventory or verified run-to-output correspondence. Identical spelling in another scope is not assumed to be the same binding.

The source comment calls `R` orthonormal; that remains attributed source framing, with no inverse relation, transform formula or matrix reproduced and no newly proved correctness or physical datum alignment. Its `off` versus `base` comment describes a historical rebinding correction and manifest context. The historical correction and outcome wording remain attributed; no bug remeasurement, reconstructed numerical fix, current correctness or physical fit is asserted.

| Provenance boundary | Missing original records |
|---|---|
| computational-invocation-and-source-version | Original invocation/source-version/parameters and accountable custody records. |
| per-node-and-assembly-output-correspondence | Original per-node/assembled output and frame-transform custody tied to that run. |
| manufactured-article-serial-and-configuration | Matched actual manufactured article/node/member serial/configuration records. |
| installed-referenceframe-datum-and-instrument | Actual installed-coordinate referenceframe/datum/instrument/raw measurement custody. |
| calibration-uncertainty-and-applicability | Applicable original calibration/uncertainty and source-to-article domain correspondence. |
| responsible-owner-criterion-and-adoption | Actual responsible owner and adopted source/version/domain/criterion record when supplied. |

Actual invocation/source version/parameters/per-node-and-assembly outputs/frame-transform custody and separately manufactured article/node-member serial/configuration/installed-coordinate referenceframe/datum/instrument/raw custody/calibration/uncertainty/applicability/owner/criterion/adoption remain NULL/UNKNOWN. Custodian roles are proposals and UNASSIGNED. Source coordinates and software gates cannot replace original records of physical installed geometry or joint fit.

Whole-fitting inventory, member-kind/socket dimensions and computed mass/printability/closure maps are separately cited by exact unit/candidate/output identity and recorded status, with no geometry/bill/mass/fit/acceptance tables or algorithms repeated. The separately cited Q13 concerns water drafting and operational availability, never assembly acceptance. The [Q16 sim/3d interface question](../../../docs/OPEN-QUESTIONS.md) is a separately pinned source boundary; no sim-geometry results or full build-path contract are repeated. No signature, landing or applicability is inferred from these citations.

No referenceframe, geometry, assembly design or manufacturing/operating/test/campaign procedure/criterion is selected. Existing source/model/code/schema/catalogue/data/test and scientific history remain unchanged. No coordinate/vector/rotation/matrix/dimension/count/mass values are copied, evaluated or derived; no transform formula reconstruction, CAD/generator/SDF/mesh/parity/test/model/physical execution or regenerated output occurs. No numerical result, new measurement, external retrieval, native action or physical campaign is supplied. The unchanged [root README](../../../README.md) states no aircraft has been built or flown.
