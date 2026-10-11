# Smeared-area versus discrete-member applicability provenance

The census says its checks use **smeared areas at full radius** and do not resolve station lengths, sections or connections. This paper traces existing equivalent input/section identities and preserves that limitation. It does not turn a continuum-equivalent assumption into an actual discrete-member or assembled-system response.

The local **bay** uses the declared **SHIP0.bayM** convention. The source passes **aI / bay** to **gi** as **aISmeared**. It forms **aO0** from the source outer-ring area and pitch, combines it with **aOExtra** as **aO**, combines inner/outer smeared areas as **abar**, and uses declared depth in **iEff**. CROSSWALK.json records exact symbolic fragments without numerical values, evaluation or independent derivation. These area-per-spacing and equivalent-section conventions are source assumptions, not measured spacing, reference-cell response or effective stiffness.

[CROSSWALK.json](CROSSWALK.json) preserves source identities separately from actual records and requirements. [PROVENANCE.json](PROVENANCE.json) pins the source revision/bytes and declares the one-based, end-exclusive locator convention. Sources: [member census](../../../docs/MEMBER-CENSUS.md), [model source](../../../ship/model.js), and [root README](../../../README.md). No source or generated census is modified or executed.

| Provenance boundary | Missing evidence |
|---|---|
| source-domain-and-units-convention | Original source/configuration/revision/domain and area-per-spacing/equivalent-section unit conventions, including inclusion/exclusion. |
| matched-reference-cell-and-member-spacing | Original reference-cell/configuration/member-spacing records with matched source domain and applicability. |
| boundary-and-connection-response | Applicable boundary/connection configuration and response records, source custody and domain correspondence. |
| original-homogenization-derivation-and-validation | Original derivation identity/revision/assumptions and matched validation records if supplied. |
| raw-custody-calibration-and-uncertainty | Unmodified original raw records, acquisition context, responsible custody and applicable calibration/uncertainty. |
| applicability-and-responsible-adoption | Matched reference/domain/applicability records, actual responsible owner and adoption source/version/criterion only when supplied. |

Actual installed configuration, matched reference-cell/member-spacing/boundary/connection response, original applicable derivation/validation/raw/calibration/uncertainty/custody/applicability/adoption records, assigned owner and adopted criterion remain NULL/UNKNOWN. Custodian roles are proposals, UNASSIGNED.

Formula identity is not a matched original derivation or validation record, measured effective stiffness, boundary/connection response or licensed transfer to a discrete assembly. No source area/spacing/radius/inertia/stiffness/capacity/mass values are copied or calculated; no homogenization calibration or sensitivity experiment is supplied.

Station/shoulder load transfer, laminate material properties, cap/polar topology, reserve iteration/inclusion, optional hardware credit, fitting manifest, P16/P45 and Q11 normalization remain separate. No maps from those papers are repeated. This paper concerns only continuum-equivalent versus discrete-assembly applicability record custody.

Existing source/model/code/catalogue/schema/data/test and recorded scientific history remain unchanged. No counting, completed physical manifest, calculation, generation, native/physical/solver action, external lookup, source/primary/remote/settings change or new measurement/scientific outcome is supplied. No aircraft has been built or flown according to the unchanged root README. Passing repository checks cannot establish physical presence, absence, applicability, feasibility, qualification, benefit or safety.
