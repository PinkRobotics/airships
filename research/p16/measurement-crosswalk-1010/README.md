# P1.6 evidence-to-measurement crosswalk

Date: 2026-10-10. Status: prospective method paper; every observation and evidence-record reference is null. This records what would replace missing inputs, without selecting hardware or doing a physical test, solver run, capacity calculation or new scientific result.

The [machine-readable crosswalk](CROSSWALK.json) preserves the identifiers of every row and input in the public [assumed input contract](../../program/p1-6-assumed-port-inputs.json). Each entry names its source JSON pointer, original status, units, request IDs, required observation method, prospective evidence identifier, missing nested-value targets and conditions that invalidate transfer. A reserved evidence identifier is a name for a future record, not an observation or a claim that evidence exists. Different sites and concepts require separate records; shared request IDs do not transfer measurements between articles.

The source [scalar result](../../program/p1-6-scalar-result.json) remains the stipulated toy scenario. No scalar was recomputed. Source geometry, topology and recipe constants remain hypotheses. Unavailable private source entries stay null; no private witness outcome is recovered or republished. Actual mesh/clearance evidence and physical capacity evidence are separate. A geometric screen cannot qualify a bond, clamp, support or barrier. Missing implementation error cannot be substituted by zero, and a conservative cover failing cannot prove actual collision.

Measurement records must identify the article, site, concept, lot, coordinate frame, assembly/process state, calibration, uncertainty, controls and immutable evidence location. Required local contact, ingress, egress, load and coverage criteria stay UNKNOWN until an authorized source supplies them. Equality handling and nonnegative margin requirements already stated in the input contract are retained; this paper chooses no margin or threshold. The catalogue of source requests in CROSSWALK.json retains every requested observation and unit.

| Source row | Evidence category | Source requests | Physical disposition |
|---|---|---|---|
| `n00.l0:bondedboss:R1` | Registered aperture and entire stack | ACC01, GEO01, GEO02, MET01, SUP01 | UNKNOWN/HOLD |
| `n00.l0:bondedboss:R2` | Attachment and intentional contact process | ACC01, BND01, COV01, CRT01, ENV01, MAT01R, MAT02R | UNKNOWN/HOLD |
| `n00.l0:bondedboss:R3` | Operate, disconnect, gauge and vent | ACC01, ENV01, GAS01, HW01R, MET01 | UNKNOWN/HOLD |
| `n00.l0:bondedboss:R4` | Insertion, removal, preparation and backing by state | ACC01, BND01, ENV01, SUP01 | UNKNOWN/HOLD |
| `n00.l0:bondedboss:R5` | Film, material, seams, drape and barrier ownership | CRT01, ENV01, GAS01, GEO02, MAT01R, MAT02R | UNKNOWN/HOLD |
| `n00.l0:bondedboss:R6` | Independent support anchors and common load route | COV01, CRT01, ENV01, HW01R, SUP01 | UNKNOWN/HOLD |
| `n00.l0:bondedboss:R7` | Geometry binding, uncertainty and conditional mesh recipe | CRT01, ENV01, GEO01, MET01 | UNKNOWN/HOLD |
| `n00.l0:bondedboss:R8` | Acquisition and qualification evidence gate | BND01, COV01, CRT01, CST01, MET01 | UNKNOWN/HOLD |
| `n00.l0:reinforcedclampedflange:R1` | Registered aperture and entire stack | ACC01, GEO01, GEO02, MET01, SUP01 | UNKNOWN/HOLD |
| `n00.l0:reinforcedclampedflange:R2` | Attachment and intentional contact process | ACC01, CLP01, CRT01, ENV01, MAT01R, MAT02R | UNKNOWN/HOLD |
| `n00.l0:reinforcedclampedflange:R3` | Operate, disconnect, gauge and vent | ACC01, ENV01, GAS01, HW01R, MET01 | UNKNOWN/HOLD |
| `n00.l0:reinforcedclampedflange:R4` | Insertion, removal, preparation and backing by state | ACC01, CLP01, ENV01, SUP01 | UNKNOWN/HOLD |
| `n00.l0:reinforcedclampedflange:R5` | Film, material, seams, drape and barrier ownership | CRT01, ENV01, GAS01, GEO02, MAT01R, MAT02R | UNKNOWN/HOLD |
| `n00.l0:reinforcedclampedflange:R6` | Independent support anchors and common load route | COV01, CRT01, ENV01, HW01R, SUP01 | UNKNOWN/HOLD |
| `n00.l0:reinforcedclampedflange:R7` | Geometry binding, uncertainty and conditional mesh recipe | CRT01, ENV01, GEO01, MET01 | UNKNOWN/HOLD |
| `n00.l0:reinforcedclampedflange:R8` | Acquisition and qualification evidence gate | CLP01, COV01, CRT01, CST01, MET01 | UNKNOWN/HOLD |
| `n10.l0:bondedboss:R1` | Registered aperture and entire stack | ACC01, GEO01, GEO02, MET01, SUP01 | UNKNOWN/HOLD |
| `n10.l0:bondedboss:R2` | Attachment and intentional contact process | ACC01, BND01, COV01, CRT01, ENV01, MAT01R, MAT02R | UNKNOWN/HOLD |
| `n10.l0:bondedboss:R3` | Operate, disconnect, gauge and vent | ACC01, ENV01, GAS01, HW01R, MET01 | UNKNOWN/HOLD |
| `n10.l0:bondedboss:R4` | Insertion, removal, preparation and backing by state | ACC01, BND01, ENV01, SUP01 | UNKNOWN/HOLD |
| `n10.l0:bondedboss:R5` | Film, material, seams, drape and barrier ownership | CRT01, ENV01, GAS01, GEO02, MAT01R, MAT02R | UNKNOWN/HOLD |
| `n10.l0:bondedboss:R6` | Independent support anchors and common load route | COV01, CRT01, ENV01, HW01R, SUP01 | UNKNOWN/HOLD |
| `n10.l0:bondedboss:R7` | Geometry binding, uncertainty and conditional mesh recipe | CRT01, ENV01, GEO01, MET01 | UNKNOWN/HOLD |
| `n10.l0:bondedboss:R8` | Acquisition and qualification evidence gate | BND01, COV01, CRT01, CST01, MET01 | UNKNOWN/HOLD |
| `n10.l0:reinforcedclampedflange:R1` | Registered aperture and entire stack | ACC01, GEO01, GEO02, MET01, SUP01 | UNKNOWN/HOLD |
| `n10.l0:reinforcedclampedflange:R2` | Attachment and intentional contact process | ACC01, CLP01, CRT01, ENV01, MAT01R, MAT02R | UNKNOWN/HOLD |
| `n10.l0:reinforcedclampedflange:R3` | Operate, disconnect, gauge and vent | ACC01, ENV01, GAS01, HW01R, MET01 | UNKNOWN/HOLD |
| `n10.l0:reinforcedclampedflange:R4` | Insertion, removal, preparation and backing by state | ACC01, CLP01, ENV01, SUP01 | UNKNOWN/HOLD |
| `n10.l0:reinforcedclampedflange:R5` | Film, material, seams, drape and barrier ownership | CRT01, ENV01, GAS01, GEO02, MAT01R, MAT02R | UNKNOWN/HOLD |
| `n10.l0:reinforcedclampedflange:R6` | Independent support anchors and common load route | COV01, CRT01, ENV01, HW01R, SUP01 | UNKNOWN/HOLD |
| `n10.l0:reinforcedclampedflange:R7` | Geometry binding, uncertainty and conditional mesh recipe | CRT01, ENV01, GEO01, MET01 | UNKNOWN/HOLD |
| `n10.l0:reinforcedclampedflange:R8` | Acquisition and qualification evidence gate | CLP01, COV01, CRT01, CST01, MET01 | UNKNOWN/HOLD |

For each actual-input field, a matching record would fill the missing observation, rather than overwrite a historical hypothesis. For assumed model entries, independent geometry/process evidence would establish or refute applicability. For unavailable-source entries, independently admissible public evidence is required; a private archival identifier cannot serve as a public result. Nested missing recipe error and mesh-binding fields have their own recorded targets even though their enclosing object is an assumption.

The top-level selection, aperture, mesh binding and numerical-error fields remain null. Physical clearance and physical capacity both remain UNKNOWN/HOLD. The [delivery plan](../../program/PLAN.md#unit-record-and-review) requires exact-object custody and preserved chronology. The [verification plan](../../../docs/VERIFICATION-PLAN.md#the-experiments-specified) describes prospective experiments; its physical work and unresolved criteria are dependencies, not authorization from this paper. Scope-specific failures, NOT RUN and missing coverage must remain visible when future observations are dispositioned.
