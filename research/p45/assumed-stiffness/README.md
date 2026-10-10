# P4.5 assumed stiffness continuation

This is a conditional paper record, not a measured stiffness, mass, hardware qualification or a new public scientific conclusion. Actual cord/end/shared-anchor stiffness, matrices, chi, masses, confidence and applicability remain **UNKNOWN** (JSON `null` for actual numeric inputs).

[ASSUMPTIONS.json](ASSUMPTIONS.json) explicitly stipulates chi-star = 0.94 as a toy assumption and one possible compliance allocation. The stipulated source assumptions E = 70 GPa and density = 970 kg/m³ remain unqualified. Active lengths, baseline areas, load state and installed hardware are unknown; no dimensional compliance value is invented. The model's 19,440 cords, 38,880 ends and 4,320 degree-nine sites are graph counts, not a measured installation.

## Registered interface and conditional comparison

The [12-row input contract](inherited/INPUT-CONTRACT.json) and [sufficient conditions](inherited/SUFFICIENT-CONDITIONS.md) retain the scientific interface and bounds. They are public derivatives with separate original and derivative digests. Register common datum, work-conjugate signs/units, all nine ports and their moment arms, state/contact/pretension, both cord ends and the complete frame/support boundary. Preserve all anchor cross terms and offsite coupling. A diagonal or isolated end test cannot qualify a nine-port shared anchor; a local matrix cannot by itself qualify global load transfer.

Write D0 = diag(L/(E A0)). At the stipulated proposed area A = A0/chi-star, D = chi-star D0. As a **paper assumption**, allocate at most 0.02 D0 to each end contribution and 0.02 D0 to the entire assembled anchor/support contribution. That last allowance covers both endpoint sites and every within-site/offsite term once; it is not an allowance at each anchor. These are operator upper bounds in the same compatible basis, not measured matrices or independent scalar certifications.

If the summed passive symmetric connection operator obeys those assumed bounds, C-conn <= 0.06 D0 = (1/chi-star - 1)D. The inherited inversion argument then gives (D + C-conn)^(-1) >= chi-star D^(-1). This is conditional axial-network sufficiency. The assumed bounds have not been demonstrated on hardware.

Global qualification additionally needs the same compatibility map, constraints, nullspace quotient, internal-coordinate condensation, prestress and retained members as the reference, plus a uniform uncertainty-aware constrained lower-operator comparison over every admitted state and configuration. Actual slack/contact, support mechanisms, crosssite transfer, material ratings and population coverage remain unknown. No global chi or qualification follows from this illustrative allocation.

## Sensitivity without another scientific run

For a symbolic 0 < chi-star <= 1, shares alpha-end1, alpha-end2 and alpha-anchor must be nonnegative and sum to at most 1-chi-star in D0 units. Increasing any share consumes allowance available to the others; unbounded cross terms invalidate the assumed bound. Increasing proposed cord area also changes cord compliance and retention, so chi cannot be treated as an independently certified joint constant. For fixed independent-series c-total, the inherited baseline-retention condition is A >= A0/(1 - E A0 c-total/L), with positive denominator; this specialization does not replace the coupled global condition. No new grid, optimization or numerical experiment is reported.

## One mass pool and qualification limits

The [mass inventory](inherited/MASS-INVENTORY.json) retains all 34 canonical rows, their scientific values and JSON numeric types, and actual-mass nulls; provenance and decision labels are adapted for public reading. Its end/site/support/fixture/reinforcement duty map assigns every flight item once to the same symbolic C-U/chi additions pool. Laboratory equipment is excluded only after an explicit duty decision; carried hardware consumes that pool. Unknown replacement savings are not credits. Actual inventory and budget fit remain UNKNOWN.


[LIMITATIONS.json](inherited/LIMITATIONS.json) records the missing physical inputs and applicability limits. Historical source assumptions remain conditional; this paper provides no retrospective qualification.

## Evidence needed for physical use

The inherited [decision brief](inherited/DECISION-BRIEF.md) gives nine minimum-measurement lines covering matched cords, both ends, the shared anchor, frame/global coupling, state, material limits and actual masses. Nine independent load directions with all nine responses identify a local linear operator at one state; they do not establish population confidence or all-site applicability. Instrument classes are requirements only. Evidence owners, exact statistically justified specimen counts, and confidence target remain unassigned/UNKNOWN.

[PROVENANCE.json](PROVENANCE.json) lists repository-relative derivative paths and separate original/derivative digests. The extracts remove operational narratives and adapt provenance labels for readers; they are not byte-identical copies. Scientific assumptions, the twelve-row interface, ledger values and numeric types, one-pool accounting and UNKNOWN limits are retained. Original source records remain the historical basis; this paper does not change their evidence or qualify hardware.
