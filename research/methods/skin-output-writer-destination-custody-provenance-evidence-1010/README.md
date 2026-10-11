# Skin writer source destinations versus actual output custody

This paper traces selected source identities in [tools/gen_skin.py](../../../tools/gen_skin.py). [CROSSWALK.json](CROSSWALK.json) records exact nonnumeric fragments, hashed contexts and prospective missing records. [PROVENANCE.json](PROVENANCE.json) pins complete authorized sources and revision, retaining parser context separately. No actual generated artifacts or physical records are acquired.

Module `ROOT`, `JSON_OUT` and `JS_OUT` are located by bare assignment names, omitting destination literals and path-resolution details. Selected separate writer sites in `main` name `open`, `fh`, `fh.write`, `json_text` and `js_text`. Both sites reuse the same `fh` local binding within `main`; separate sites do not create separate lexical variables. No path/mode/encoding literal or option, written content, check branch, formatting, serialization, output summary or algorithm is copied or evaluated. Source destination/write names are not actual acquired bytes, configuration, output/raw custody or qualified installed skin.

| Provenance boundary | Missing original records |
|---|---|
| invocation-version-and-input-configuration | Original actual invocation/version/input configuration and accountable custody. |
| input-record-page-digests-and-destination-use | Original input-record/page digests and actual destination-use records. |
| output-digests-correspondence-and-raw-custody | Original output digests/source-output correspondence and unmodified raw custody. |
| article-film-process-and-installed-skin | Matched actual article/film-material/lot/process/gores/seams/bonds/installed skin/state records. |
| metrology-referenceframe-timebase-and-calibration | Original metrology/referenceframe/timebase/calibration/uncertainty and applicability. |
| owner-criterion-and-adoption | Actual accountable owner and adopted source/version/domain/criterion record when supplied. |

All listed actual invocation/version/configuration/input/destination/digest/correspondence/output/raw-custody fields and article/film-material/lot/process/gores/seams/bonds/installed skin/state/metrology/referenceframe/timebase/calibration/uncertainty/applicability/owner/criterion/adoption remain NULL/UNKNOWN. Custodian roles are proposed and UNASSIGNED.

Related writer/emitter/literal/parser/comparator/generator-directory/manifest/assembly-record and shape/film provenance maps remain separately cited by exact unit/candidate/output identity and recorded status. No identity, numerical result, criterion, acceptance or status transfer, signature/landing or physical applicability is imported.

No format/schema/material/design, acceptance criterion, registry or production/operating/test/campaign procedure is selected. Existing source/model/code/schema/catalogue/data/test and scientific history remain unchanged. No actual generated artifact lookup/read/parse/matching/refresh/regeneration/freeze, numeric copying/evaluation, source/model/emitter/fixture/parity/native/scientific/physical execution, external retrieval or new measurement occurs. The unchanged [root README](../../../README.md) states no aircraft has been built or flown.
