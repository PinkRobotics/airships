# Conditional laminate sensitivity and measured member-property provenance

[Conditional laminate-stiffness sensitivity](../../../docs/OPEN-QUESTIONS.md#conditional-laminate-stiffness-sensitivity) asks what measured axial, hoop and shear properties, layup, coupling terms and compression allowables should describe discrete tubes, before moduli are used in a physical member check. The published comparison contrasts the code's co-critical effective-modulus factor with a stated fibre-only fixed-tube idealisation, also using consistent axial and global moduli in that idealisation. Its numerical operands, factors, ratios, masses and safety factors remain solely in the unchanged sources.

The source explicitly says this is conditional arithmetic, not measured laminate data or a corrected prediction. The [original sensitivity record](../../../docs/audit/26-10-02-stiffness-sensitivity.json) records a computational rerun and says no person checked the arithmetic. Its status says it is not a replacement for the model. This paper preserves that original execution boundary and source identity; it neither reruns the equations nor supplies a new validation, corrected property or measured member outcome.

[CROSSWALK.json](CROSSWALK.json) maps each source property question and the conditional record's coCriticalFactor, fixedTubeFactor, capacityRatio and record/favourable branch identities. JSON pointers identify existing results without copying values. Source execution/status pointers retain provenance while actual measured property and comparison records remain unknown.

| Property or record boundary | Missing applicable provenance |
|---|---|
| Axial property | Original definition/orientation/units and matched material-state/specimen/member evidence. |
| Hoop property | Original hoop definition and applicable source/member configuration. |
| Shear property | Original shear convention and records, without scalar-factor substitution. |
| Layup | Original member/specimen layup and configuration applicability, without choosing one. |
| Coupling terms | Declared identities/conventions and raw evidence, without inventing a matrix or absent terms. |
| Compression allowable | Original definition and adopted source/domain, without choosing an allowable or policy. |
| Matched records and adoption | Applicable raw custody, calibration, uncertainty and responsible criterion provenance. |

The [member census](../../../docs/MEMBER-CENSUS.md#recorded-disagreements) says current checks use smeared areas at full radius, unresolved station lengths/sections/connections and schematic inner-ring, fan, theta and junction display sections. That depiction cannot supply actual discrete-tube material, layup, coupling or member/specimen applicability. A conditional effective factor cannot silently replace distinct measured property records or select a physical allowable.

Prospective evidence would need unmodified specimen/member/configuration/revision/material-state and property-source records, original units/orientation/reference and comparison applicability, raw custody, calibration, uncertainty and responsible adoption/version/domain provenance. Actual property/specimen/member/configuration/material-state/layup/coupling/allowable/raw/calibration/uncertainty/applicability/matched-comparison/assigned-owner/criterion records remain NULL/UNKNOWN. Role names are proposed custodians, UNASSIGNED. [PROVENANCE.json](PROVENANCE.json) pins all authoritative inputs and declares fragment/pointer conventions.

P16 collapse, P45 assumed cord stiffness, Q11 mass, reserve inclusion and station/shoulder transfer remain separate. This paper concerns conditional-source versus actual measured discrete-member material-property provenance only. Source/model/data/code/catalogue/schema/tests remain unchanged. No numerical copy/calculation, equation rerun, property estimate, selected layup/material/allowable/criterion/design/test procedure, code/model/fixture/generator/solver execution, physical action, external lookup, measurement or scientific outcome is supplied. The root README says no aircraft has been built or flown; conditional arithmetic and repository checks do not supply measured material data, a corrected prediction, physical qualification, feasibility, benefit or safety.
