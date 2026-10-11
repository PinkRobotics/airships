# Material compression-source flags and fallback provenance

This paper traces source input custody in [ship/model.js](../../../ship/model.js). [CROSSWALK.json](CROSSWALK.json) records namespace/header distinctions and the two explicitly assigned consumers. [PROVENANCE.json](PROVENANCE.json) pins the full source revision and bytes. No qualified article allowable, model correctness, fallback justification or physical acceptance is supplied.

The source header identifies `sigma` as tensile strength and `sigmaCompression` as the compression-side input for compressed struts and bending. It explicitly says missing compression data retains the tensile value as an unsourced assumption. Printed interlayer Z and in-plane XY properties remain separate; a vendor UD coupon is not a part allowable.

All MATERIALS object rows are traced by their field names and source-reported flags: M60J_LAM, T700_LAM and CFF have `compressionSourced` true; PAHT_XY, PAHT_Z, TI64 and AEROGEL have it false with explicit unsourced tensile-value retention text. These are source Boolean identities, not independent verification. Typical UD/plaque descriptions and existing tensile/compression citation URLs remain distinct from actual specimen, lot, process, print-axis and part applicability. URLs are retained only as identities; no external retrieval or current-standard/datasheet validation occurred. Numeric property values remain solely in source.

`solidStrut` and `tubeStrut` each have their own `m` parameter and local `phiY`, explicitly consuming `m.sigmaCompression`. This paper maps these two consumers as assigned; it does not claim other model consumers are absent or give a comprehensive consumer inventory. Their use of a source field cannot establish its correctness, qualification, safety or licensed transfer. No expression is evaluated and no tensile/compression comparison or numerical outcome is reproduced.

| Provenance boundary | Missing original records |
|---|---|
| source-flag-citation-and-fallback-custody | Original compression source/citation/domain and fallback assumption records tied to source version. |
| actual-coupon-specimen-and-material-lot | Actual original compression coupon, specimen and material-lot/raw records with responsible custody. |
| print-axis-process-state-and-part | Matched print axis, process, state, part and configuration records. |
| qualification-and-transfer-domain | Original qualified article allowable/domain/transfer and applicability evidence when supplied. |
| calibration-uncertainty-and-raw-custody | Original applicable calibration, uncertainty, raw record and acquisition/custody context. |
| responsible-owner-criterion-and-adoption | Actual responsible owner and adoption source/version/domain/criterion when supplied. |

Actual compression coupon/raw/specimen/material-lot/print-axis/process/state/part/configuration/domain, calibration/uncertainty/qualification/transfer/applicability/custody, owner/criterion/adoption remain NULL/UNKNOWN. Custodian roles are proposals and UNASSIGNED. A true flag is not a qualified part allowable; false/unsourced fallback remains an assumption. This paper supplies no justification for that fallback and chooses no material, axis, allowable, fallback, loadcase, criterion or design.

Hull strength-world coupon, conditional laminate moduli, representative density, GI knockdown, homogenization and cord stiffness maps remain separate. Available laminate/density/homogenization maps are named by unit/candidate/output identity with their recorded status; no landing, numerical outcome or property transfer is inferred. The density candidate's recorded scoped stop is retained.

Existing source/model/code/catalogue/schema/data/test and scientific history remain unchanged. No numeric strength/modulus/factor/density/capacity/mass/margin copying/calculation/comparison/derivation, safety analysis, campaign/test/procedure development, source/model/equation/generator/fixture execution, external retrieval, native/physical action or new measurement/scientific result is supplied. Passing repository gates cannot supply missing article qualification or adoption. The unchanged [root README](../../../README.md) says no aircraft has been built or flown.
