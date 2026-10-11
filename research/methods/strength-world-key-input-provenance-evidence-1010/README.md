# Strength-world key input and material correspondence provenance

`ship0` accepts source `sigmaKey` with a null default. Its normalized `key` retains `SHIP0.sigmaMid` for null input, otherwise the supplied key, and the source lookup refers to `SHIP0.sigmaWorldsMPa[key]`. The returned `sigmaKey` retains that local key. These are lexical parameter/default/lookup/returned identities only; no lookup, branch, test or model was executed.

Source labels `s742`, `s1050` and `s1450` occur in the declared namespace and selected `ship0Summary` caller contexts. Digits inside those strings are code labels only; their property values and conversions are omitted and are not interpreted as MPa strengths. Keys and defaults do not identify an actual material, tube, article, coupon, strength distribution, accepted allowable or verified configuration.

[EVIDENCE-MAP.json](EVIDENCE-MAP.json) pins exact nonnumeric applicability fragments and source-context span hashes. [PROVENANCE.json](PROVENANCE.json) pins unchanged sources. The [model source](../../../ship/model.js) supplies conditional lexical context; the [member census](../../../docs/MEMBER-CENSUS.md) retains unresolved physical station lengths, sections and connections. The [README](../../../README.md) states no aircraft has been built or flown.

| Evidence row | Requirement | Current status |
|---|---|---|
| source-key-namespace | Retain source key labels without property interpretation | UNKNOWN |
| null-default-supplied-key | Retain null-default and supplied-key identity | UNKNOWN |
| lookup-return-correspondence | Retain source lookup and returned-key identity | UNKNOWN |
| summary-caller-identity | Retain selected summary caller key context | UNKNOWN |
| invocation-sourceversion | Keep actual invocation and source version unresolved | UNKNOWN |
| actual-key-configuration | Keep actual key and configuration correspondence unresolved | UNKNOWN |
| material-article-coupon | Keep matched material article and coupon unresolved | UNKNOWN |
| domain-raw-custody | Keep property domain and raw custody unresolved | UNKNOWN |
| calibration-uncertainty-applicability | Keep calibration uncertainty and applicability unresolved | UNKNOWN |
| owner-criterion-adoption | Keep assigned owner criterion and adoption unresolved | UNKNOWN |

Actual computational invocation/source version/key correspondence, material/tube/article/coupon/lot/process/configuration/property-domain/raw custody, calibration, uncertainty, applicability, criterion and adoption remain null/UNKNOWN. Assigned owner and custodian remain null/UNASSIGNED. Public source pins and repository/publication checks do not supply matched coupon evidence or physical acceptance authority.

Strength-world/coupon property provenance, compression-source fallback, material-density, named basis, GI knockdown and declared/emergent SF remain separate records. Their worlds, property and credit analyses and tables are not repeated. Corresponding preceding owned candidates absent from this observed main base are not imported or treated as landed.

This paper records qualitative source key/interface/caller identity only. It reconstructs no decision or formula, explores no invalid-key behaviour and executes no branch, test, model or parity check. It copies, interprets or evaluates no strength, factor, threshold, load, capacity, mass or numerical output. It selects no key, world, material, allowable, design or criterion and supplies no operating/test/campaign guidance. Source/model/code/schema/catalogue/data/test and primary/remote/settings remain unchanged; no native, physical, new science, external or out-of-band action.
