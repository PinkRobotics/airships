# Computed printability output custody versus physical demonstration

This paper traces source context in [tools/gen_nodes.py](../../../tools/gen_nodes.py). [CROSSWALK.json](CROSSWALK.json) records nonnumeric helper/caller/output fragments with span hashes and prospective missing records; [PROVENANCE.json](PROVENANCE.json) pins the complete sources and revision. Computational measured wording is not physical observation or manufacturing qualification.

The source describes `overhang_fraction` as a whole-mesh area fraction that is diluted and cannot see islands. `bed_support` describes field-derived computational measures and explicitly concedes that a sideways cantilever may count as reached even though it droops. These limitations remain. No threshold, angle, grid resolution, output value, formula or support algorithm is reproduced or evaluated.

`print_frame` carries its own input context and optional `search_out`. Its source comments distinguish search-grid ranking from extraction-grid reported measures. Within that function the call is `bed_support(F3, hh)`; within `main` the later extraction field is passed as `bed_support(F3, h)`. These are distinct local contexts. This paper maps their identities without reconstructing a search/ranking procedure, selecting an orientation/support system or claiming source-check correctness.

The per-node `frameSearch` field retains ranked search context. The adjacent per-node bed/support/island fields report extraction context, with bed-normal and overhang output identities kept separate. The aggregate `manifest["printability"]` draws from the node rows and its source rule explicitly attributes reported measures to the extraction grid. A repeated field name across namespaces does not equate context, raw custody, calibration, physical response or applicability. No output manifest was looked up, matched or regenerated and no current equality is assumed.

| Provenance boundary | Missing original records |
|---|---|
| computational-invocation-and-version | Original exact computational invocation/version/parameters/orientation and source correspondence. |
| manifest-custody-and-context | Original unmodified manifest/raw custody with search-ranking versus extraction-report context. |
| physical-part-printer-material-process | Actual part/printer/material/process/state/orientation/support records with responsible custody. |
| physical-observations-and-rejections | Original physical observations/rejections and applicable acquisition context. |
| calibration-uncertainty-and-applicability | Original applicable calibration/uncertainty/custody/domain correspondence. |
| responsible-owner-and-criterion | Actual responsible owner and adoption source/version/domain/criterion when supplied. |

Actual computational invocation/version/parameters/orientation/manifest custody/source correspondence and physical part/printer/material/process/orientation/support/observations/rejections/calibration/uncertainty/custody/applicability/owner/criterion/adoption remain NULL/UNKNOWN. Custodian roles are proposals and UNASSIGNED. A computational source report or passing software gate cannot supply these records or physical print qualification.

Q13 assembly and computed-node-mass maps are cited separately by exact unit/candidate/output identity and recorded status in the crosswalk. [Print yield and tolerance](../../../docs/VERIFICATION-PLAN.md) is separately pinned there as an existing prospective plan boundary, without adopting its tolerance, campaign, procedure or claiming completed tests. No mass/volume/cut/strength/output results or full build-path contract are repeated; no landing or physical applicability is inferred.

No orientation, support, printer, material, process, procedure, criterion, design or physical campaign is selected. Existing source/model/code/catalogue/schema/data/test and scientific history remain unchanged. No numerical copying/calculation/comparison/derivation, generator/search/support/mesh/extraction/model/fixture execution, formula reconstruction, regenerated geometry/manifest, external retrieval, native/physical action or new measurement/scientific result is supplied. The unchanged [root README](../../../README.md) says no aircraft has been built or flown.
