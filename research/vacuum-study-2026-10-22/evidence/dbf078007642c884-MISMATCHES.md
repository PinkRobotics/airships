**Exact mismatch disposition — CHECK MAINLINE-043**

There are **zero numerical mismatches outside the declared tolerances** in the 95,634 main comparisons and ten supplemental rise conversions. [COMPARISONS.csv](be7c216ed76b48a2-COMPARISONS.csv) retains all signed main differences; [MISMATCHES.json](37517e5f3dc66819-MISMATCHES.json) is therefore empty. [RISE-CHECK.json](00b1485e268b733c-RISE-CHECK.json) retains the supplemental comparisons. Agreement at tolerance does not mean every floating-point result is bit-identical.

One field has an ambiguous accounting label:

| Field | Owner value | Independent meaning | Correction |
|---|---:|---|---|
| `RESULTS.rise8.mass_from_owner_arc_length_and_independent_section_kg` | 5446.29062569268 kg | Charged total, including allowances | Rename to `total_mass_with_inherited_allowances_kg`; expose tube mass separately |
| Section × arc length × density | — | 5039.557738754902 kg of tubes | Derived from radii, wall, attributed length and 3100 kg/m³ |
| Excess of inherited field over tube mass | — | 406.73288693777795 kg | Joint, node, film and systems allowances |

This label does not change the main stress or probability results. The independently reconstructed charged total is 5446.290625692647 kg, agreeing at roundoff with the inherited field. The addendum verifies arithmetic from source inputs, not a new rise8 equilibrium solution.

The old-sheet/current-page property differences, statistical reference assumptions and qualification gaps are [NFI items](89a8b861a172592d-NFI.json), not arithmetic contradictions. In particular, the source already marks the proof protocol unqualified. This check adds the exact distinction between the 1.25 force factor, the 1.259378651 stress factor and the 0.375 Euler-load ratio.

The first two main diagnostic runs contained defects in this checker's section inversion and extrema correlation. Their mismatches are preserved in `execution/` for provenance and are not charged to the owner. Only the corrected `independent-final` result and the supplemental `rise-label-check` result define this review.
