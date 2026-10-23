# MAINLINE-030d — Corrections

QUESTIONABLE / PROJECTION. All inherited entries are preserved;030d entries and annotations carry current corrections.

## 1. S-200F E is 290 GPa, not 303 (S-200FH's)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 2. Equilateral member force is pRs/(2*sqrt3), not pRs/2 (FIX-A)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 3. 015's tolerance map mixed conventions (lambda 1 amplitude with lambda 2.625 width; nu 0.33 declared, 0.30 used)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 4. 019's step rule pairs aramid's optimistic gamma 1 with aluminium's conservative 0.2

```json
{
  "correction": "019's step rule pairs aramid's optimistic gamma 1 with aluminium's conservative 0.2",
  "by": [
    "rpt-check019-opus-1020"
  ],
  "effect_on_lead": "P2 family choice: with one 018 curve for both, aluminium leads (0.847 against 0.609 on the optimistic line; 0.557 against 0.253 conservative). 021 rev1's lead is already on aluminium honeycomb.",
  "lead_relevant": true,
  "ids_in_store": {
    "rpt-check019-opus-1020": true
  }
}
```

## 5. S-200F compression is about 255 MPa (Materion guide), not 283

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 6. SP-8007's gamma applies to tube local buckling: 0.529 at r/t 140, not 1 (FIX-B)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 7. A rise above the sagitta does not cut N; it adds a crown moment

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 8. A two-way grid has 2V-4 members, not the triangulated 3V-6; its C = 4 assumes isotropy

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 9. The film rule implies a sag of about s/24 that costs lift (about 31.45 kg per metre of s)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 10. 019's optimistic reserve embeds 4 m panels and 0.015 lb/ft2 film

```json
{
  "correction": "019's optimistic reserve embeds 4 m panels and 0.015 lb/ft2 film",
  "by": [
    "rpt-ref-1080d4f6a1af4cfa8c67"
  ],
  "effect_on_lead": "P2: at today's 0.914 m stock and 0.030 film the reserve is 1229 kg at 021b's point (1154 kg on 019's aluminium family, which this checker reproduced); 021b names panel size as its third optimism.",
  "lead_relevant": true,
  "ids_in_store": {
    "rpt-ref-1080d4f6a1af4cfa8c67": true
  }
}
```

## 11. The 020 brief's 2,100 kg of faces is 3,498.47 kg

```json
{
  "correction": "The 020 brief's 2,100 kg of faces is 3,498.47 kg",
  "by": [
    "rpt-ref-3e02218a03708a878faa"
  ],
  "effect_on_lead": "P2: supply and cost rows use the real face mass (0.81% of world mine output; $39.5m to $167.9m sheet stock).",
  "lead_relevant": true,
  "ids_in_store": {
    "rpt-ref-3e02218a03708a878faa": true
  }
}
```

## 12. Intracell dimpling takes CR-1457's biaxial rule, which halves the uniaxial SF

```json
{
  "correction": "Intracell dimpling takes CR-1457's biaxial rule, which halves the uniaxial SF",
  "by": [
    "rpt-ref-444cea756201354c34c3",
    "rpt-ref-0d85ae067b41baf8d095"
  ],
  "effect_on_lead": "P2: none; dimpling stays far above 1 (9.0 at 021 rev1, 4.98 at 021b).",
  "lead_relevant": true,
  "ids_in_store": {
    "rpt-ref-444cea756201354c34c3": true,
    "rpt-ref-0d85ae067b41baf8d095": true
  }
}
```

## 13. Ceramic arcs take lattice k 0.2; Wright's 0.4 is an optimism of factor 2

```json
{
  "correction": "Ceramic arcs take lattice k 0.2; Wright's 0.4 is an optimism of factor 2",
  "by": [
    "rpt-mainline022-grok-p3-optimistic-floating-point-1020"
  ],
  "effect_on_lead": "P3: every P3 row scores k 0.2; k 0.4 rows are sensitivities only.",
  "lead_relevant": true,
  "ids_in_store": {
    "rpt-mainline022-grok-p3-optimistic-floating-point-1020": true
  }
}
```

## 14. Tensile yield used as the compressive allowable is a source objection, carried as a qualification

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 15. Opening sentence on mass split of the 5% float point

```json
{
  "correction": "Opening sentence on mass split of the 5% float point",
  "old": null,
  "new": "total mass 95% of lift, payload reserve 5%",
  "by": [
    "rpt-1228-mainline009c5-independent-check-1019"
  ],
  "cards": [
    "MAINLINE-009c-5"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 16. Beryllium S200F modulus (303 GPa belongs to S200FH); E-only fixed-geometry SF 0.636308391376, rebalanced 0.643084807693

```json
{
  "correction": "Beryllium S200F modulus (303 GPa belongs to S200FH); E-only fixed-geometry SF 0.636308391376, rebalanced 0.643084807693",
  "old": "303 GPa",
  "new": "290 GPa",
  "by": [
    "rpt-1228-mainline009c5-independent-check-1019"
  ],
  "cards": [
    "MAINLINE-009c-5"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 17. Endpoint wording at Vc=2 in the weak-core branch

```json
{
  "correction": "Endpoint wording at Vc=2 in the weak-core branch",
  "old": null,
  "new": null,
  "by": [
    "rpt-1228-mainline009c5-independent-check-1019"
  ],
  "cards": [
    "MAINLINE-009c-5"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 18. S200F modulus

```json
{
  "correction": "S200F modulus",
  "old": "303 GPa",
  "new": "290 GPa",
  "by": [
    "rpt-1228-mainline013-independent-check-1020"
  ],
  "cards": [
    "MAINLINE-013",
    "MAINLINE-007",
    "MAINLINE-007b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 19. Ideal Q design crossing density

```json
{
  "correction": "Ideal Q design crossing density",
  "old": "4.81751557814 kg/m3",
  "new": "5.29333338323 kg/m3",
  "by": [
    "rpt-1228-mainline013-independent-check-1020"
  ],
  "cards": [
    "MAINLINE-013",
    "MAINLINE-007",
    "MAINLINE-007b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 20. Ideal B crossing density

```json
{
  "correction": "Ideal B crossing density",
  "old": "8.82396627456 kg/m3",
  "new": "9.21851132666 kg/m3",
  "by": [
    "rpt-1228-mainline013-independent-check-1020"
  ],
  "cards": [
    "MAINLINE-013",
    "MAINLINE-007",
    "MAINLINE-007b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 21. Required ideal fraction at 5 kg/m3

```json
{
  "correction": "Required ideal fraction at 5 kg/m3",
  "old": "0.982088063907",
  "new": "1.02611270125",
  "by": [
    "rpt-1228-mainline013-independent-check-1020"
  ],
  "cards": [
    "MAINLINE-013",
    "MAINLINE-007",
    "MAINLINE-007b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 22. Basotect and EPS12 strength treated as exact values

```json
{
  "correction": "Basotect and EPS12 strength treated as exact values",
  "old": "exactly 9 kPa (Basotect)",
  "new": "greater than 9 kPa bound",
  "by": [
    "rpt-1228-mainline013-independent-check-1020"
  ],
  "cards": [
    "MAINLINE-013",
    "MAINLINE-007",
    "MAINLINE-007b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 23. Densest Meza 2015 notes field

```json
{
  "correction": "Densest Meza 2015 notes field",
  "old": "lightest specimen: 12 um, N=20, 0.000104",
  "new": "octets, 8 um, N=10, 0.00182",
  "by": [
    "rpt-1228-mainline013-independent-check-1020"
  ],
  "cards": [
    "MAINLINE-013",
    "MAINLINE-007",
    "MAINLINE-007b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 24. S200F modulus

```json
{
  "correction": "S200F modulus",
  "old": "303 GPa",
  "new": "290 GPa",
  "by": [
    "rpt-1228-mainline014b-independent-check-1019"
  ],
  "cards": [
    "MAINLINE-014b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 25. Beryllium fixed-geometry least SF with E-only substitution

```json
{
  "correction": "Beryllium fixed-geometry least SF with E-only substitution",
  "old": "0.685338231171",
  "new": "0.670589282589",
  "by": [
    "rpt-1228-mainline014b-independent-check-1019"
  ],
  "cards": [
    "MAINLINE-014b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 26. Beryllium reoptimized grid SF (continuous balance 0.677676080411)

```json
{
  "correction": "Beryllium reoptimized grid SF (continuous balance 0.677676080411)",
  "old": null,
  "new": "0.677588686611",
  "by": [
    "rpt-1228-mainline014b-independent-check-1019"
  ],
  "cards": [
    "MAINLINE-014b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 27. Overall face ordering

```json
{
  "correction": "Overall face ordering",
  "old": "CNT, beryllium, graphene",
  "new": "CNT, graphene, beryllium",
  "by": [
    "rpt-1228-mainline014b-independent-check-1019"
  ],
  "cards": [
    "MAINLINE-014b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 28. Sentence that honeycomb wrinkling uses Gc

```json
{
  "correction": "Sentence that honeycomb wrinkling uses Gc",
  "old": null,
  "new": null,
  "by": [
    "rpt-1228-mainline014b-independent-check-1019"
  ],
  "cards": [
    "MAINLINE-014b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 29. Recommends Una's correction be carried as a qualification, not an objection; strength factors P2-A x2.30, P3-A x4.31, P1-A x1.38 kept as QUESTIONABLE directions

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 30. Each point should state collapse as the lesser of buckling and yield; yield strength must also rise at the same geometry

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 31. P1 modulus factor when float margin is spent on thickness (1.26 mm)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 32. Omitted core limits as property targets: crimping needs Gc about 1 MPa at 0.49 m; wrinkling needs Ec*Gc near 4e16 Pa^2

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## 33. Report body says k 0.4 and 0.5 are in the card; the CARD.md table carries k 1, 0.4 and 0.2 only

```json
{
  "correction": "Report body says k 0.4 and 0.5 are in the card; the CARD.md table carries k 1, 0.4 and 0.2 only",
  "old": "k 0.4 and 0.5 in card",
  "new": "k 1, 0.4, 0.2 in card; k 0.5 only in RESULTS.json",
  "by": [
    "rpt-check011b-opus-1020"
  ],
  "cards": [
    "MAINLINE-011b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 34. INPUTS.json material rows carry no source (COMMON.md asks for one); sources are in 011's INPUTS.json

```json
{
  "correction": "INPUTS.json material rows carry no source (COMMON.md asks for one); sources are in 011's INPUTS.json",
  "old": null,
  "new": "pin 011 INPUTS.json or copy sources",
  "by": [
    "rpt-check011b-opus-1020"
  ],
  "cards": [
    "MAINLINE-011b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 35. Card says no coefficient was taken from Buchert; Buchert 1968 prints the card's Et and D, so it can cite it

```json
{
  "correction": "Card says no coefficient was taken from Buchert; Buchert 1968 prints the card's Et and D, so it can cite it",
  "old": "no Buchert coefficient",
  "new": "cite Buchert 1968",
  "by": [
    "rpt-check011b-opus-1020"
  ],
  "cards": [
    "MAINLINE-011b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 36. The 'two_way' rows are the triangulated frame scored with C=4, not a true two-way frame

```json
{
  "correction": "The 'two_way' rows are the triangulated frame scored with C=4, not a true two-way frame",
  "old": null,
  "new": null,
  "by": [
    "rpt-check011b-opus-1020"
  ],
  "cards": [
    "MAINLINE-011b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 37. FIX-A (equilibrium member force) SiC equilateral k 0.2 least SF

```json
{
  "correction": "FIX-A (equilibrium member force) SiC equilateral k 0.2 least SF",
  "old": "1.22552794688",
  "new": "1.408",
  "by": [
    "rpt-check011b-opus-1020"
  ],
  "cards": [
    "MAINLINE-011b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 38. FIX-B (SP-8007 gamma on local mode) SiC equilateral k 0.2 least SF; both fixes give 1.205

```json
{
  "correction": "FIX-B (SP-8007 gamma on local mode) SiC equilateral k 0.2 least SF; both fixes give 1.205",
  "old": "1.22552794688",
  "new": "1.075",
  "by": [
    "rpt-check011b-opus-1020"
  ],
  "cards": [
    "MAINLINE-011b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 39. Ranking of aluminium versus aramid when one gamma curve is applied to both (optimistic line, optimistic curve)

```json
{
  "correction": "Ranking of aluminium versus aramid when one gamma curve is applied to both (optimistic line, optimistic curve)",
  "old": "aramid 0.609 ahead of aluminium (mixed pairing)",
  "new": "aluminium 0.847 vs aramid 0.609",
  "by": [
    "rpt-check019-opus-1020"
  ],
  "cards": [
    "MAINLINE-019"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 40. Same ranking under the conservative curve (optimistic line)

```json
{
  "correction": "Same ranking under the conservative curve (optimistic line)",
  "old": "aramid ahead",
  "new": "aluminium 0.557 vs aramid 0.253",
  "by": [
    "rpt-check019-opus-1020"
  ],
  "cards": [
    "MAINLINE-019"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 41. Order cites the owner report id with the wrong prefix

```json
{
  "correction": "Order cites the owner report id with the wrong prefix",
  "old": "rpt-ref-ea73d14ec4d4d8963f76",
  "new": "rpt-ref-d7f99cd71e977826da48",
  "by": [
    "rpt-check019-opus-1020"
  ],
  "cards": [
    "MAINLINE-019"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 42. Aluminium dimpling safety factors (1/4 and 3/8 inch cells) under equal-biaxial interaction

```json
{
  "correction": "Aluminium dimpling safety factors (1/4 and 3/8 inch cells) under equal-biaxial interaction",
  "old": "19.4949 and 8.6644",
  "new": "9.7475 and 4.3322",
  "by": [
    "rpt-ref-444cea756201354c34c3"
  ],
  "cards": [
    "MAINLINE-009d"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 43. Aluminium intracell dimpling SF (1/4 and 3/8 inch) under equal-biaxial interaction

```json
{
  "correction": "Aluminium intracell dimpling SF (1/4 and 3/8 inch) under equal-biaxial interaction",
  "old": "33.4499 and 14.8666",
  "new": "16.7250 and 7.4333",
  "by": [
    "rpt-ref-0d85ae067b41baf8d095"
  ],
  "cards": [
    "MAINLINE-009e"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 44. Sim dimple sigma_0

```json
{
  "correction": "Sim dimple sigma_0",
  "old": "19119540732.73865 Pa",
  "new": "19113852932.30557 Pa",
  "by": [
    "rpt-ref-62323cf6831eb964377f"
  ],
  "cards": [
    "MAINLINE-018"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 45. Sim dimple Vc

```json
{
  "correction": "Sim dimple Vc",
  "old": "197.24625832023136",
  "new": "197.18758027094242",
  "by": [
    "rpt-ref-62323cf6831eb964377f"
  ],
  "cards": [
    "MAINLINE-018"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 46. Sim dimple Gc for Vc=2

```json
{
  "correction": "Sim dimple Gc for Vc=2",
  "old": "1972462583.2023137 Pa",
  "new": "1971875802.7094243 Pa",
  "by": [
    "rpt-ref-62323cf6831eb964377f"
  ],
  "cards": [
    "MAINLINE-018"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 47. Dimple sigma_0

```json
{
  "correction": "Dimple sigma_0",
  "old": "19119540732.739 Pa",
  "new": "19113852932.306 Pa",
  "by": [
    "rpt-ref-d458cd5a32d90025482b"
  ],
  "cards": [
    "MAINLINE-018b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 48. Dimple Vc

```json
{
  "correction": "Dimple Vc",
  "old": "197.24625832023",
  "new": "197.18758027094",
  "by": [
    "rpt-ref-d458cd5a32d90025482b"
  ],
  "cards": [
    "MAINLINE-018b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 49. Dimple classical pressure

```json
{
  "correction": "Dimple classical pressure",
  "old": "767777835.49685 Pa",
  "new": "767549432.14939 Pa",
  "by": [
    "rpt-ref-d458cd5a32d90025482b"
  ],
  "cards": [
    "MAINLINE-018b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 50. Threshold kd for SF 1 (continuous, not first 0.001 grid point)

```json
{
  "correction": "Threshold kd for SF 1 (continuous, not first 0.001 grid point)",
  "old": "0.519",
  "new": "0.518304076929753",
  "by": [
    "rpt-ref-88e650e7f8b713866e0b"
  ],
  "cards": [
    "MAINLINE-015"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 51. Hydrostatic pressure difference across 20 m (uses sea-level density)

```json
{
  "correction": "Hydrostatic pressure difference across 20 m (uses sea-level density)",
  "old": "240.262925 Pa",
  "new": "228.939839514 Pa",
  "by": [
    "rpt-ref-88e650e7f8b713866e0b"
  ],
  "cards": [
    "MAINLINE-015"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 52. Frozen Be core-shear reduction

```json
{
  "correction": "Frozen Be core-shear reduction",
  "old": "11.39981%",
  "new": "15.11569%",
  "by": [
    "rpt-ref-88e650e7f8b713866e0b"
  ],
  "cards": [
    "MAINLINE-015"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 53. P2-E pressure loss from one 10% thin face

```json
{
  "correction": "P2-E pressure loss from one 10% thin face",
  "old": "10.0%",
  "new": "5.14568%",
  "by": [
    "rpt-ref-88e650e7f8b713866e0b"
  ],
  "cards": [
    "MAINLINE-015"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 54. P2-E kd 0.9 RMS against the 0.25 mm criterion

```json
{
  "correction": "P2-E kd 0.9 RMS against the 0.25 mm criterion",
  "old": "1.82224",
  "new": "0.697838",
  "by": [
    "rpt-ref-88e650e7f8b713866e0b"
  ],
  "cards": [
    "MAINLINE-015"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 55. Be kd 0.9 RMS against the 0.25 mm criterion

```json
{
  "correction": "Be kd 0.9 RMS against the 0.25 mm criterion",
  "old": "0.412293",
  "new": "0.157890",
  "by": [
    "rpt-ref-88e650e7f8b713866e0b"
  ],
  "cards": [
    "MAINLINE-015"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 56. Matched-width ask replacing the 0.10 mm panel ask

```json
{
  "correction": "Matched-width ask replacing the 0.10 mm panel ask",
  "old": "0.10 mm",
  "new": "0.03947 mm",
  "by": [
    "rpt-ref-88e650e7f8b713866e0b"
  ],
  "cards": [
    "MAINLINE-015"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 57. Hutchinson-Thompson DOI

```json
{
  "correction": "Hutchinson-Thompson DOI",
  "old": "10.1016/j.ijsolstr.2018.08.020",
  "new": "10.1016/j.ijsolstr.2018.01.030",
  "by": [
    "rpt-ref-88e650e7f8b713866e0b"
  ],
  "cards": [
    "MAINLINE-015"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 58. Gerasimidis/Virot/Hutchinson/Rubinstein DOI

```json
{
  "correction": "Gerasimidis/Virot/Hutchinson/Rubinstein DOI",
  "old": "10.1115/1.4039193",
  "new": "10.1115/1.4040455",
  "by": [
    "rpt-ref-88e650e7f8b713866e0b"
  ],
  "cards": [
    "MAINLINE-015"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 59. Lower-kd envelope supplied from Lee 2016 Eq. 23: delta/t = 0.25/(kd-0.068) - 0.28

```json
{
  "correction": "Lower-kd envelope supplied from Lee 2016 Eq. 23: delta/t = 0.25/(kd-0.068) - 0.28",
  "old": null,
  "new": "Lee 2016 Eq. 23",
  "by": [
    "rpt-ref-88e650e7f8b713866e0b"
  ],
  "cards": [
    "MAINLINE-015"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 60. S-200F/SR-200 modulus

```json
{
  "correction": "S-200F/SR-200 modulus",
  "old": "303 GPa",
  "new": "290 GPa",
  "by": [
    "rpt-ref-e92af61311c9bf4a89cd"
  ],
  "cards": [
    "MAINLINE-021"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 61. Required gamma / C in the headline tuple at E290

```json
{
  "correction": "Required gamma / C in the headline tuple at E290",
  "old": "0.579149449 / 0.362641644",
  "new": "0.595317964 / 0.370680714",
  "by": [
    "rpt-ref-e92af61311c9bf4a89cd"
  ],
  "cards": [
    "MAINLINE-021"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 62. Fewest optimisms for the sheet claim at E290

```json
{
  "correction": "Fewest optimisms for the sheet claim at E290",
  "old": "gamma alone",
  "new": "two optimisms needed",
  "by": [
    "rpt-ref-e92af61311c9bf4a89cd"
  ],
  "cards": [
    "MAINLINE-021"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 63. Be Poisson ratio (orthotropic sheet)

```json
{
  "correction": "Be Poisson ratio (orthotropic sheet)",
  "old": "0.33",
  "new": "0.0768 / 0.0752",
  "by": [
    "rpt-ref-e92af61311c9bf4a89cd"
  ],
  "cards": [
    "MAINLINE-021"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 64. S-200F compression starting strength per the guide

```json
{
  "correction": "S-200F compression starting strength per the guide",
  "old": "283 MPa",
  "new": "about 255 MPa",
  "by": [
    "rpt-ref-e92af61311c9bf4a89cd"
  ],
  "cards": [
    "MAINLINE-021"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 65. Scaling of required buckling moduli with kd

```json
{
  "correction": "Scaling of required buckling moduli with kd",
  "old": "every modulus scales as E(0.2)*0.2/kd",
  "new": "P1 and P2 only; P3, P3-A unchanged (2.0747e12, 7.175e11 Pa)",
  "by": [
    "rpt-ref-78794352b6bc0d9b9309"
  ],
  "cards": [
    "MAINLINE-005"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 66. Lowest density on the 1% strain definition

```json
{
  "correction": "Lowest density on the 1% strain definition",
  "old": "18-22 kg/m3",
  "new": "27.49 (linear) or 19.90 (squared) kg/m3",
  "by": [
    "rpt-ref-40cc094053ddae09d5ac"
  ],
  "cards": [
    "MAINLINE-005b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 67. Quasi-isotropic modulus basis sentences (T700, M55J, K13D2U, boron, CNT-yarn)

```json
{
  "correction": "Quasi-isotropic modulus basis sentences (T700, M55J, K13D2U, boron, CNT-yarn)",
  "old": "54, 135, 210, 86, 180 GPa",
  "new": "53.6, 136.5, 211.15, 85.68, 179.2 GPa",
  "by": [
    "rpt-ref-f08b92e3e640a19fb4ea"
  ],
  "cards": [
    "MAINLINE-008"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 68. Beryllium buckling at kd 0.1407 in the close and report

```json
{
  "correction": "Beryllium buckling at kd 0.1407 in the close and report",
  "old": "no candidate passes buckling",
  "new": "beryllium 1.0562 passes buckling",
  "by": [
    "rpt-ref-c49d322288a0b11e4381"
  ],
  "cards": [
    "MAINLINE-008b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 69. SiC P3 yield SF

```json
{
  "correction": "SiC P3 yield SF",
  "old": "0.8720",
  "new": "0.8719",
  "by": [
    "rpt-ref-c49d322288a0b11e4381"
  ],
  "cards": [
    "MAINLINE-008b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 70. Graphene QI P3 yield SF

```json
{
  "correction": "Graphene QI P3 yield SF",
  "old": "0.4159",
  "new": "0.4158",
  "by": [
    "rpt-ref-c49d322288a0b11e4381"
  ],
  "cards": [
    "MAINLINE-008b"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 71. Lever 3 prose that the SF gain cancels to the last digit after rescaling (only the fixed-structure product SF*(1-f) equals baseline)

```json
{
  "correction": "Lever 3 prose that the SF gain cancels to the last digit after rescaling (only the fixed-structure product SF*(1-f) equals baseline)",
  "old": "returns to baseline SF",
  "new": "P2-E buckling 0.112110, yield 0.380577",
  "by": [
    "rpt-ref-7d4d494ebf14f37f5ea0"
  ],
  "cards": [
    "MAINLINE-010"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 72. K13D2U binding mode at r_o 0.02 m, s 1

```json
{
  "correction": "K13D2U binding mode at r_o 0.02 m, s 1",
  "old": "Euler",
  "new": "yield 0.2852 (Euler 0.4050)",
  "by": [
    "rpt-ref-3484d24f707ffbfe30ee"
  ],
  "cards": [
    "MAINLINE-011"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 73. First spacing at which SiC film is the least limit

```json
{
  "correction": "First spacing at which SiC film is the least limit",
  "old": "s 1.0, SF 2.514",
  "new": "s 0.90, SF 2.793",
  "by": [
    "rpt-ref-3484d24f707ffbfe30ee"
  ],
  "cards": [
    "MAINLINE-011"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 74. Vacuum mass rate at stated R_air 287.05

```json
{
  "correction": "Vacuum mass rate at stated R_air 287.05",
  "old": "0.00056590766 kg/s",
  "new": "0.00056591357 kg/s",
  "by": [
    "rpt-ref-e5b19d75c664308465ef"
  ],
  "cards": [
    "MAINLINE-016"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 75. No-convection temperature bound stored in RESULTS (card's 313.5 K stands)

```json
{
  "correction": "No-convection temperature bound stored in RESULTS (card's 313.5 K stands)",
  "old": "313.526 K",
  "new": "313.538 K",
  "by": [
    "rpt-ref-e5b19d75c664308465ef"
  ],
  "cards": [
    "MAINLINE-016"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 76. Storm margin for a 10 percent low (whole-lift scaling)

```json
{
  "correction": "Storm margin for a 10 percent low (whole-lift scaling)",
  "old": "+220 kg",
  "new": "-244.5 kg",
  "by": [
    "rpt-ref-e5b19d75c664308465ef"
  ],
  "cards": [
    "MAINLINE-016"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 77. Display roundings: lambda, synoptic upper factor, retained water

```json
{
  "correction": "Display roundings: lambda, synoptic upper factor, retained water",
  "old": "1.526, 0.2425, 125.6 kg",
  "new": "1.525, 0.2424, 125.7 kg",
  "by": [
    "rpt-ref-e5b19d75c664308465ef"
  ],
  "cards": [
    "MAINLINE-016"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 78. CNT wrinkling factor

```json
{
  "correction": "CNT wrinkling factor",
  "old": "0.750642",
  "new": "0.750492",
  "by": [
    "rpt-ref-6936f2b720197d97b0f2"
  ],
  "cards": [
    "MAINLINE-017"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 79. Beryllium wrinkling factor

```json
{
  "correction": "Beryllium wrinkling factor",
  "old": "0.685455",
  "new": "0.685398",
  "by": [
    "rpt-ref-6936f2b720197d97b0f2"
  ],
  "cards": [
    "MAINLINE-017"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 80. Beryllium yield factor

```json
{
  "correction": "Beryllium yield factor",
  "old": "0.940266",
  "new": "0.940245",
  "by": [
    "rpt-ref-6936f2b720197d97b0f2"
  ],
  "cards": [
    "MAINLINE-017"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 81. Graphene crimping factor

```json
{
  "correction": "Graphene crimping factor",
  "old": "0.677970",
  "new": "0.677924",
  "by": [
    "rpt-ref-6936f2b720197d97b0f2"
  ],
  "cards": [
    "MAINLINE-017"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 82. Beryllium density at factor 1.637323

```json
{
  "correction": "Beryllium density at factor 1.637323",
  "old": "1129.7 kg/m3",
  "new": "1129.9 kg/m3",
  "by": [
    "rpt-ref-6936f2b720197d97b0f2"
  ],
  "cards": [
    "MAINLINE-017"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 83. Least factors at the recorded combination (CNT, beryllium, graphene)

```json
{
  "correction": "Least factors at the recorded combination (CNT, beryllium, graphene)",
  "old": "1.0010, 1.0004, 1.0009",
  "new": "0.9954, 0.9891, 0.9977",
  "by": [
    "rpt-ref-6936f2b720197d97b0f2"
  ],
  "cards": [
    "MAINLINE-017"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 84. Provenance label of the P2-E baseline

```json
{
  "correction": "Provenance label of the P2-E baseline",
  "old": "each family's sealed 002 baseline",
  "new": "equal-split row at the 002 P2 mass (3636.17669088 kg)",
  "by": [
    "rpt-mainline006-check-lead4f19-1019"
  ],
  "cards": [
    "MAINLINE-006"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 85. Reading of the modulus improvement factors (qualification, not a gate)

```json
{
  "correction": "Reading of the modulus improvement factors (qualification, not a gate)",
  "old": "requirement for SF 1",
  "new": "conditional buckling/Euler factors within the stated models",
  "by": [
    "rpt-xo-h1-mainline-estimates-review-600-sci-1019"
  ],
  "cards": [
    "MAINLINE-001"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 86. Verdict on MAINLINE-002 amended to apply the CO's source condition: aluminium yield limits and stiffness-only remaining SF checked as arithmetic of a tensile premise only

```json
{
  "correction": "Verdict on MAINLINE-002 amended to apply the CO's source condition: aluminium yield limits and stiffness-only remaining SF checked as arithmetic of a tensile premise only",
  "old": "ADMITTED for scope",
  "new": "ADMITTED with SOURCE OBJECTION on every sigma-dependent output",
  "by": [
    "rpt-xo-h1-mainline002-review-600-source-objection-correction-sci-1019"
  ],
  "cards": [
    "MAINLINE-002"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 87. NFI-AL-YIELD-CARRY effect sentence on required compressive strength

```json
{
  "correction": "NFI-AL-YIELD-CARRY effect sentence on required compressive strength",
  "old": "scales linearly with sigma",
  "new": "independent of sigma; only strength pressure and SF scale",
  "by": [
    "rpt-xo-mainline003-review-600-sci-1019"
  ],
  "cards": [
    "MAINLINE-003"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 88. NFI-KD effect sentence on required modulus

```json
{
  "correction": "NFI-KD effect sentence on required modulus",
  "old": "scales directly with knockdown",
  "new": "scales inversely with knockdown",
  "by": [
    "rpt-xo-mainline003-review-600-sci-1019"
  ],
  "cards": [
    "MAINLINE-003"
  ],
  "effect_on_lead": null,
  "lead_relevant": false
}
```

## 89. CHECK-036 reproduces thresholds and corrects a legacy film label

```json
{
  "correction": "CHECK-036 reproduces thresholds and corrects a legacy film label",
  "by": [
    "rpt-ref-5f14d083ceae03234596",
    "rpt-ref-f182f16ed5be422b7811"
  ],
  "effect_on_lead": "4945 comparisons and150 threshold/sensitivity points pass. R20 sheet-scalar threshold381.612–381.639MPa. OldR20 .015lb/ft2 label conflicts with governing.146472829kg/m2=.030; calculations use.030. Historical379.2MPa at1.96mm confirmed, still not matched finished thin-sheet qualification.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 90. CHECK-035 revises graph readings and narrows absence claims

```json
{
  "correction": "CHECK-035 revises graph readings and narrows absence claims",
  "by": [
    "rpt-mainline035-opus-knockdown-tests-1020",
    "rpt-ref-d3afcdc3514000cb6fc2"
  ],
  "effect_on_lead": "S-II centers .209242/.221511 (about +/- .01), not .22/.24. Add eleventh cylinder point; use analytic CR1457 curve. CTA8.3 printed .864 versus load ratio .865305 unresolved. Other marine/foam-core tests exist; no compatible elastic sphere at recoverable moderateVc is established, and unprecedented control is not proven.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 91. 026b global transfer moves the current P3 screen

```json
{
  "correction": "026b global transfer moves the current P3 screen",
  "by": [
    "rpt-ref-8befdd4c89803adc44a8",
    "rpt-ref-6c81b0b188ad134a3ea2"
  ],
  "effect_on_lead": "Ordered .848 times1.258252476558=1.066998100121; exact frequency4 ratio gives1.067537780749. Global alone moves; mass and other modes held. QUESTIONABLE cross-geometry sensitivity.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 92. 026b new nonlinear first-loss fields remain null

```json
{
  "correction": "026b new nonlinear first-loss fields remain null",
  "by": [
    "rpt-ref-8befdd4c89803adc44a8"
  ],
  "effect_on_lead": "Raw nearest-zero crossings5.082444/2.218113 can skip an unstable family. No verified first-instability claim, no retry or new numerical work performed here.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 93. 026b rise and mass conventions remain explicit

```json
{
  "correction": "026b rise and mass conventions remain explicit",
  "by": [
    "rpt-ref-8befdd4c89803adc44a8"
  ],
  "effect_on_lead": "Rise8 retains538.899kN mean compression and4.248GPa elastic bending. Frequency4 sag uncharged; frequency2 carries187.938kg. No uniform mass-budget comparison.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 94. 017b P3 numerical leads superseded by022d

```json
{
  "correction": "017b P3 numerical leads superseded by022d",
  "by": [
    "rpt-ref-6ba73ec8a89453b26832",
    "rpt-ref-6c81b0b188ad134a3ea2"
  ],
  "effect_on_lead": "Retain trends/directions and all15NFIs, not old1.441 Zylon optimum or its14–25year closure as current predictions. P2 comparisons use variable scarf and piecewise gamma.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 95. Combined032/032b check repairs metrology attribution

```json
{
  "correction": "Combined032/032b check repairs metrology attribution",
  "by": [
    "rpt-ref-7427b639691bfaf71f29"
  ],
  "effect_on_lead": "533 comparisons pass; Woody3micrometres is template adjustment, .008in coupon faces identified, Rion near-wavelength measured evidence added for carbon/Nomex. Be modal gap remains.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 96. 038 turns ground-first list into physical test sequence

```json
{
  "correction": "038 turns ground-first list into physical test sequence",
  "by": [
    "rpt-ref-536c47263ffe5f46fd19"
  ],
  "effect_on_lead": "First compression/specification, weighed sealed scarf, same-batch wrinkle screens; nine test families. Prices projected, no quotes; newest P3 target must use selected022d reserve, not frozen022c.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 97. 028b replaces panel enlargement with stock scarf and fixed thin film

```json
{
  "correction": "028b replaces panel enlargement with stock scarf and fixed thin film",
  "by": [
    "rpt-ref-d907de1e97319ecc3f9a",
    "rpt-ref-aae116a5fcd787ed9abc"
  ],
  "effect_on_lead": "Two remaining adjustable factors; fixed O5 is still consumed. Nominal gamma/Q=2.820818×/1.317054× at p0.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 98. P2 R10 results must keep pressure and accounting bases

```json
{
  "correction": "P2 R10 results must keep pressure and accounting bases",
  "by": [
    "rpt-ref-d907de1e97319ecc3f9a",
    "rpt-ref-5b1ba7a48fcb57c8e35e"
  ],
  "effect_on_lead": "028b passes at p0; 033 includes +1% pressure and fails at R10 with the scarf screen. Threshold actual bill10.350852m; floor10.358194m.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 99. Thin-sheet compression remains unqualified

```json
{
  "correction": "Thin-sheet compression remains unqualified",
  "by": [
    "rpt-ref-5f14d083ceae03234596"
  ],
  "effect_on_lead": "Current maker345MPa is tensile. Current scarf demand about300MPa; 036 older027 R20 needs about382MPa under its own different joint/elastic assumptions.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 100. Zylon 0/90 source contract halves old film factors

```json
{
  "correction": "Zylon 0/90 source contract halves old film factors",
  "by": [
    "rpt-ref-f6de390e1555b4ca8e78",
    "rpt-ref-6c81b0b188ad134a3ea2"
  ],
  "effect_on_lead": "Old022c cap5%/019 fixed-geometry factors .746876/.708523. 022d charges both plies and reoptimizes; selected screened1.258252.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 101. Joint capacities and mass must use claimed multiplier

```json
{
  "correction": "Joint capacities and mass must use claimed multiplier",
  "by": [
    "rpt-ref-f4daf73c940b6f527d37",
    "rpt-ref-f6de390e1555b4ca8e78",
    "rpt-ref-6c81b0b188ad134a3ea2"
  ],
  "effect_on_lead": "Old joint sized at lambda1 had no pressure reserve. New sleeve/wrap mass scales lambda²; its own capacity equals target, still unqualified.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 102. P3 tensile bending and local/column interaction

```json
{
  "correction": "P3 tensile bending and local/column interaction",
  "by": [
    "rpt-ref-f6de390e1555b4ca8e78",
    "rpt-ref-6c81b0b188ad134a3ea2"
  ],
  "effect_on_lead": "022d includes Ft15.586MPa projection; current screened lead has no tensile stress at target. Coupled instability stays open.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 103. P3 screened lead replaces out-of-band maxima

```json
{
  "correction": "P3 screened lead replaces out-of-band maxima",
  "by": [
    "rpt-ref-6c81b0b188ad134a3ea2",
    "rpt-ref-490f8e9228d526b69dc8"
  ],
  "effect_on_lead": "Half-wave/member=1 at3.170759m spacing; not validated continuum. Two-way C4 remains unqualified.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 104. Discrete frame result is not an installed safety factor

```json
{
  "correction": "Discrete frame result is not an installed safety factor",
  "by": [
    "rpt-ref-7ce5b278fa083d87105b"
  ],
  "effect_on_lead": "6.465222 elastic eigenvalue versus6.127640; mechanisms for free pins;61.40kg overrun; local/material screens precede elastic limits.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 105. Altitude benefit requires weather/terrain choice

```json
{
  "correction": "Altitude benefit requires weather/terrain choice",
  "by": [
    "rpt-ref-9a0319231d2fe686eb92",
    "rpt-ref-be337d7d2ce1259d0aff"
  ],
  "effect_on_lead": "Optimistic100m floor55.341kg headroom, nominalSF1.036553. P3 altitude passes remain out of half-wave band; do not adopt them as the current P3 lead.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 106. Thermal, wind and mooring screens add required mass and choices

```json
{
  "correction": "Thermal, wind and mooring screens add required mass and choices",
  "by": [
    "rpt-ref-8c5de04c9c33dbcf7447"
  ],
  "effect_on_lead": "Coated/bond-reference shear can be1.678 or.917; bare.388.70-knot screen.998442, nominal pads8.65/33.14kg. No uncharged pad fixes.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 107. Vacuum service differs from gas-only life

```json
{
  "correction": "Vacuum service differs from gas-only life",
  "by": [
    "rpt-ref-244f32e2449e729d312f"
  ],
  "effect_on_lead": "Ground-evacuated sealed24h at30–50kg estimated; preserve100kg. Outgassing is phase transfer, ingress adds mass. Zylon complete bill91.624–111.624kg at older geometry.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 108. Frame material names refer to fittings

```json
{
  "correction": "Frame material names refer to fittings",
  "by": [
    "rpt-ref-244f32e2449e729d312f"
  ],
  "effect_on_lead": "Both Kapton/Ti and Zylon/CFRP P3 frames are SiC tubes. Titanium and CFRP designate end fittings, not tube material.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 109. 035 arithmetic is separate from physical comparability

```json
{
  "correction": "035 arithmetic is separate from physical comparability",
  "by": [
    "rpt-mainline035-opus-knockdown-tests-1020",
    "rpt-ref-d3afcdc3514000cb6fc2"
  ],
  "effect_on_lead": "112 comparable derived fields reproduce. Corrected S-II readings, unknownVc/plasticity, anisotropic SBKF denominator and extra experimental leads prevent universal absence or transferable sphere-penalty claims.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 110. 032 lead-only amplitude/cell prose corrected

```json
{
  "correction": "032 lead-only amplitude/cell prose corrected",
  "by": [
    "rpt-ref-a30a669ed3e245f1473b"
  ],
  "effect_on_lead": "Lead-only range .00684754923–.01604921437; .0046–.024 spans four cases. Fc is weakest of core compression/tension/bond;35psi is minimum average.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 111. 032b compares distinct measurement quantities

```json
{
  "correction": "032b compares distinct measurement quantities",
  "by": [
    "rpt-mainline032b-grok-measured-flatness-1020"
  ],
  "effect_on_lead": ".001651mm aluminium cell depth is precedent; .024mm reflector RMS and .2032mm whole-panel RMS are not the critical wrinkle component.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 112. 015b tolerance correction retains extra source qualifications

```json
{
  "correction": "015b tolerance correction retains extra source qualifications",
  "by": [
    "rpt-ref-a5374575ee8867fc8d2e"
  ],
  "effect_on_lead": "Old/live RMS2.6112627; actual-gamma RMS .139344/.654416mm. Rounded021b gamma changes amplitude.379%, not only fourth digit; k-span is conditional.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 113. 028 legacy reoptimization contained unstated eta=.9

```json
{
  "correction": "028 legacy reoptimization contained unstated eta=.9",
  "by": [
    "rpt-ref-68dff0680696fe9b4cb4"
  ],
  "effect_on_lead": "Without hidden screen, legacy stock/four-metre SF .792549/.914222 rather than .750851/.844536. Nominal scarf result stands.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 114. 020 grade, modulus and doubler supply corrections

```json
{
  "correction": "020 grade, modulus and doubler supply corrections",
  "by": [
    "rpt-ref-35706d7a2ae7e951590b"
  ],
  "effect_on_lead": "Use product-specific SR200 strength/290GPa basis; doubling material changes historical supply/cost. Do not treat a source transfer as compression admission.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 115. 024 original sag and pump accounts incomplete

```json
{
  "correction": "024 original sag and pump accounts incomplete",
  "by": [
    "rpt-ref-7d6892c4e55be16ad523",
    "rpt-ref-244f32e2449e729d312f"
  ],
  "effect_on_lead": "Original cap rise alone charged no sag volume.022c/d charge sag;034 separates systems choices and extra membrane mass.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 116. 027 P3 member-force convention flagged

```json
{
  "correction": "027 P3 member-force convention flagged",
  "by": [
    "rpt-ref-7b45cb6b4d7f92067f8b"
  ],
  "effect_on_lead": "Inherited pRs/2 is not triangular pRs/(2sqrt3); global/film unchanged, member scores conditional.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 117. 025 property edition and missing sag carried

```json
{
  "correction": "025 property edition and missing sag carried",
  "by": [
    "rpt-ref-a8b77f7de2ffc56af7b4"
  ],
  "effect_on_lead": "CurrentSA table430GPa versus carried410GPa has negligible reported governing effect; no qualified compression; original025 excludes sag.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 118. 030 half-wave coefficient and duplicate source pointer confirmed

```json
{
  "correction": "030 half-wave coefficient and duplicate source pointer confirmed",
  "by": [
    "rpt-ref-490f8e9228d526b69dc8"
  ],
  "effect_on_lead": "Printed1.06 rounds1.06066 under thin-radius convention; no conclusion changes.362 unique rows,363 pointers because N023 has two subjects.",
  "lead_relevant": true,
  "register_version": "030b",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 119. Selected P2 lead includes cure

```json
{
  "correction": "Selected P2 lead includes cure",
  "by": [
    "rpt-ref-d6eac96dde8db1968e86"
  ],
  "old": "028b no-residual gamma .564164/Q .434628",
  "new": "200 F + 30.341397:1 scarf, gamma .564287956/Q .439513308, usage .972190149; +.120150655 kg source allowance",
  "effect_on_lead": "200 F + 30.341397:1 scarf, gamma .564287956/Q .439513308, usage .972190149; +.120150655 kg source allowance",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 120. Keep as-designed 250 F case

```json
{
  "correction": "Keep as-designed 250 F case",
  "by": [
    "rpt-ref-d6eac96dde8db1968e86"
  ],
  "old": "Nominal 028b called current without cure",
  "new": "30:1 case gamma .618429128, usage 1.052281584; minimum-strength edge SF .833325314; not within named stretch",
  "effect_on_lead": "30:1 case gamma .618429128, usage 1.052281584; minimum-strength edge SF .833325314; not within named stretch",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 121. Gamma evidence state

```json
{
  "correction": "Gamma evidence state",
  "by": [
    "rpt-1228-mainline029-crimp-gamma-fe-1020"
  ],
  "old": "029 pending; 015 amplitudes used as tolerance map",
  "new": "Benchmark not reproduced; 78.627395/90.722275 kPa endpoints below 95.460838 kPa. Not collapse limits or current-hull SF",
  "effect_on_lead": "Benchmark not reproduced; 78.627395/90.722275 kPa endpoints below 95.460838 kPa. Not collapse limits or current-hull SF",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 122. Gamma denominator

```json
{
  "correction": "Gamma denominator",
  "by": [
    "rpt-1228-mainline029-crimp-gamma-fe-1020"
  ],
  "old": "Handbook and crimp ratios conflated",
  "new": "Both lead points Vc<2; required handbook .595318/.468229 versus W crimp .464110/.323009",
  "effect_on_lead": "Both lead points Vc<2; required handbook .595318/.468229 versus W crimp .464110/.323009",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 123. Optimism label collision

```json
{
  "correction": "Optimism label collision",
  "by": [
    "rpt-mainline039-opus-stiffened-sandwich-1020"
  ],
  "old": "039 calls frame-bay cap transfer O5",
  "new": "Rename to P2-O6 (source alias 039/O5); preserve P2-O5 as .015/.030 bond-film mass reduction",
  "effect_on_lead": "Rename to P2-O6 (source alias 039/O5); preserve P2-O5 as .015/.030 bond-film mass reduction",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 124. Stiffened constructive improvement

```json
{
  "correction": "Stiffened constructive improvement",
  "by": [
    "rpt-ref-20ab4b33b504a00ad3b6"
  ],
  "old": "Grid .689107645 / +1329.818726 kg claimed best",
  "new": "Attained .699691806 at fixed mass; +1127.071353 kg at SF 1.000001080. Finite-search scope, not global proof",
  "effect_on_lead": "Attained .699691806 at fixed mass; +1127.071353 kg at SF 1.000001080. Finite-search scope, not global proof",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 125. Stiffened source gates and point distinctions

```json
{
  "correction": "Stiffened source gates and point distinctions",
  "by": [
    "rpt-ref-20ab4b33b504a00ad3b6"
  ],
  "old": "psi>=28 handbook gate; mass-added Q/scarf/tubes said to require change",
  "new": "psi>=28 and gamma_s>=10 are unvalidated gates; at owner's mass-added point Q/scarf/local already pass. Cap factor .601013192, not .603",
  "effect_on_lead": "psi>=28 and gamma_s>=10 are unvalidated gates; at owner's mass-added point Q/scarf/local already pass. Cap factor .601013192, not .603",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 126. Stiffened source ratios

```json
{
  "correction": "Stiffened source ratios",
  "by": [
    "rpt-ref-20ab4b33b504a00ad3b6"
  ],
  "old": "Ti ratio .33 and STA8.1 predictions conflated",
  "new": "317/917=.345692475 while printed 33% remains a source inconsistency; 759000 and 754000 lb are sequential model levels",
  "effect_on_lead": "317/917=.345692475 while printed 33% remains a source inconsistency; 759000 and 754000 lb are sequential model levels",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 127. P3 checked continuum point

```json
{
  "correction": "P3 checked continuum point",
  "by": [
    "rpt-ref-4b8e7b08241bb7a45536"
  ],
  "old": "Primary 022d not yet checked in 030b",
  "new": "All primary witnesses reproduce; 50 sensitivity-field differences from coefficient precision, maximum SF change 3.98e-9",
  "effect_on_lead": "All primary witnesses reproduce; 50 sensitivity-field differences from coefficient precision, maximum SF change 3.98e-9",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 128. P3 rise/nonlinear verification

```json
{
  "correction": "P3 rise/nonlinear verification",
  "by": [
    "rpt-ref-b92330879d6ba35bd62c"
  ],
  "old": "Rise8 and raw first-loss labels potentially read as checked",
  "new": "Rise8 independent solve refused; first-loss null/verified_first_loss=false overrides raw labels. Linear/mass/baseline forces reproduce",
  "effect_on_lead": "Rise8 independent solve refused; first-loss null/verified_first_loss=false overrides raw labels. Linear/mass/baseline forces reproduce",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 129. 033 crossing precision

```json
{
  "correction": "033 crossing precision",
  "by": [
    "rpt-ref-d2ffe81a7858ecabf149"
  ],
  "old": "103.892275563 and 40.470112218 m",
  "new": "Active roots 103.892078332461 and 40.470082164560 m; retain 241 exact path findings and basis distinctions",
  "effect_on_lead": "Active roots 103.892078332461 and 40.470082164560 m; retain 241 exact path findings and basis distinctions",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 130. Vacuum mission distinction

```json
{
  "correction": "Vacuum mission distinction",
  "by": [
    "rpt-ref-025def9d3634f5e320d7"
  ],
  "old": "30–50 kg generalized to continuous installation",
  "new": "Daily ground-serviced sealed estimate; Edwards continuous 24 h 292.333 kg, 2.307% speed shortfall for stated Kapton envelope",
  "effect_on_lead": "Daily ground-serviced sealed estimate; Edwards continuous 24 h 292.333 kg, 2.307% speed shortfall for stated Kapton envelope",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 131. Vacuum area and reconstruction

```json
{
  "correction": "Vacuum area and reconstruction",
  "by": [
    "rpt-ref-025def9d3634f5e320d7"
  ],
  "old": "10% transmission sensitivity treated as complete area increase",
  "new": "Charge gauge/mass/release consistently; +10% Zylon vacuum/barrier/bond subtotal 96.878937–116.878937 kg plus structural fiber",
  "effect_on_lead": "Charge gauge/mass/release consistently; +10% Zylon vacuum/barrier/bond subtotal 96.878937–116.878937 kg plus structural fiber",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 132. Thermal inputs remain missing

```json
{
  "correction": "Thermal inputs remain missing",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": "Filed temperatures and projection coefficients treated as independently recovered",
  "new": "84 fields unrecovered: 60 P3 temperatures, 10 P2 temperatures/swings, 14 coefficients. 037b does not supply missing inputs",
  "effect_on_lead": "84 fields unrecovered: 60 P3 temperatures, 10 P2 temperatures/swings, 14 coefficients. 037b does not supply missing inputs",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 133. Thermal polynomial and total flight

```json
{
  "correction": "Thermal polynomial and total flight",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": "Residual maxima 5.788444/17.145083 K; increment-only flight",
  "new": "Filed-polynomial maxima 8.292853/14.851720 K. Include steady pressure: 479.847608 Pa, conditional minimum 1.001324769",
  "effect_on_lead": "Filed-polynomial maxima 8.292853/14.851720 K. Include steady pressure: 479.847608 Pa, conditional minimum 1.001324769",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 134. 038 test plan and procurement

```json
{
  "correction": "038 test plan and procurement",
  "by": [
    "rpt-ref-2beb70a569266cf0297d"
  ],
  "old": "Historical end-mass precision and full-envelope thin sheet assumed",
  "new": "Two coefficient-rounding differences retained; current targets and first-three ordering survive. Thin stock and prices unqualified; cited F1249-20 superseded by -25",
  "effect_on_lead": "Two coefficient-rounding differences retained; current targets and first-three ordering survive. Thin stock and prices unqualified; cited F1249-20 superseded by -25",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 135. 042 build-map applicability

```json
{
  "correction": "042 build-map applicability",
  "by": [
    "rpt-mainline042-opus-build-route-1020",
    "rpt-1228-mainline029-crimp-gamma-fe-1020"
  ],
  "old": "Plausible process precision interpreted as gamma support",
  "new": "Conditional map only; retain adverse 029 evidence. No matched Be process, full-scale gamma or inspection qualification",
  "effect_on_lead": "Conditional map only; retain adverse 029 evidence. No matched Be process, full-scale gamma or inspection qualification",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 136. 041 direct P3 replaces transferred shortcut

```json
{
  "correction": "041 direct P3 replaces transferred shortcut",
  "by": [
    "rpt-ref-c7dfc45babe1b96007db"
  ],
  "old": "1.067 cross-geometry sensitivity used as current estimate",
  "new": "Selected-section f4 directly gives1.133451 but +174.444kg closure deficit. Resized f5 gives1.143285/1.083205, local sensitivities1.033223/.978132 at5%/019 reserve.",
  "effect_on_lead": "Selected-section f4 directly gives1.133451 but +174.444kg closure deficit. Resized f5 gives1.143285/1.083205, local sensitivities1.033223/.978132 at5%/019 reserve.",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 137. 041 nonlinear evidence scope

```json
{
  "correction": "041 nonlinear evidence scope",
  "by": [
    "rpt-ref-c7dfc45babe1b96007db"
  ],
  "old": "Earlier nearest-zero first-loss ambiguity",
  "new": "New selected f4 smallest-algebraic sampled first loss5.430902 is source-audited; old026b paths remain unverified. Resized witnesses keep k=.2 times linear; no calibrated nonlinear knockdown.",
  "effect_on_lead": "New selected f4 smallest-algebraic sampled first loss5.430902 is source-audited; old026b paths remain unverified. Resized witnesses keep k=.2 times linear; no calibrated nonlinear knockdown.",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 138. 040 common bill supersedes R10 float interpretation

```json
{
  "correction": "040 common bill supersedes R10 float interpretation",
  "by": [
    "rpt-ref-b10363665c6202d8ef75"
  ],
  "old": "028b+037b conditional structural point treated as installed R10float",
  "new": "No R10float within named ranges; full gamma/Q endpoint ISA deficit109.649kg. R30ISA/optimistic minimum sets gamma+Q, usage.601233/.789568; both-weather no float.",
  "effect_on_lead": "No R10float within named ranges; full gamma/Q endpoint ISA deficit109.649kg. R30ISA/optimistic minimum sets gamma+Q, usage.601233/.789568; both-weather no float.",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 139. 040 film and favorable tuple definitions

```json
{
  "correction": "040 film and favorable tuple definitions",
  "by": [
    "rpt-ref-b10363665c6202d8ef75"
  ],
  "old": "Same film multiplier or compression-only improvement assumed across all points",
  "new": "R30minimum uses.030film (O5factor1), endpoint payload uses.015(factor2). Face tuple couples E/Fcy; Fcy alone is nonbinding and does not recover marginal tuple-dependent floats.",
  "effect_on_lead": "R30minimum uses.030film (O5factor1), endpoint payload uses.015(factor2). Face tuple couples E/Fcy; Fcy alone is nonbinding and does not recover marginal tuple-dependent floats.",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 140. CHECK037b HexBond support mass

```json
{
  "correction": "CHECK037b HexBond support mass",
  "by": [
    "rpt-ref-4bf25e71ae0c2ca315e2"
  ],
  "old": "Rejected HexBond679 increment444.255345188kg",
  "new": "Add30g/m2support at both interfaces:519.653568874kg, +75.398223686kg; rejection stands.16 L-precision path differences retained.",
  "effect_on_lead": "Add30g/m2support at both interfaces:519.653568874kg, +75.398223686kg; rejection stands.16 L-precision path differences retained.",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 141. CHECK037b product/cure scope

```json
{
  "correction": "CHECK037b product/cure scope",
  "by": [
    "rpt-ref-4bf25e71ae0c2ca315e2"
  ],
  "old": "200F family/2K evidence treated as qualification of light2UBe/core",
  "new": "Principal numbers reproduce; light2U substrate/core/cure,50psi tooling and residual-state transfer remain open.",
  "effect_on_lead": "Principal numbers reproduce; light2U substrate/core/cure,50psi tooling and residual-state transfer remain open.",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 142. 043 reliability evidence

```json
{
  "correction": "043 reliability evidence",
  "by": [
    "rpt-ref-8cb22d2e233e57207cf6"
  ],
  "old": "Typical3.9GPa divided by stress treated as survival probability",
  "new": "No matched compression Weibull distribution/reference size; qualified framePf/lifetime null.Conditional433-member m10 requirements4.38651/8.75267GPa are hypotheses, not demonstrated factors.",
  "effect_on_lead": "No matched compression Weibull distribution/reference size; qualified framePf/lifetime null.Conditional433-member m10 requirements4.38651/8.75267GPa are hypotheses, not demonstrated factors.",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 143. 044 life and combined loads

```json
{
  "correction": "044 life and combined loads",
  "by": [
    "rpt-ref-29830021a6e140ff7411"
  ],
  "old": "Small037bfix taken to establish ten-year service",
  "new": "Original pad core static.7143; plate-only949.846day index not hull life. Fix combined-load scarf.9891.Conditional pad+60:1scarf addition36.661kg does not float or qualify Be/scarf life.",
  "effect_on_lead": "Original pad core static.7143; plate-only949.846day index not hull life. Fix combined-load scarf.9891.Conditional pad+60:1scarf addition36.661kg does not float or qualify Be/scarf life.",
  "lead_relevant": true,
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 144. CHECK-037 /p3/0/tube_mass_kg (projection_5)

```json
{
  "correction": "CHECK-037 /p3/0/tube_mass_kg (projection_5)",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": 3733.1853334618195,
  "new": 3794.671994894594,
  "delta_kg": 61.486661432774326,
  "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
  "source": {
    "report": "rpt-ref-bba592d71d65b13cc2e5",
    "file": "evidence/17d9e138610b8036-AUDIT.json",
    "original_file": "evidence/17d9e138610b8036-AUDIT.json",
    "sha256": "17d9e138610b803643ab71d3df14a9cfeecd4ef1ab10c17f060ff61baed2f8b3",
    "selector": "row=/p3/0,field=tube_mass_kg"
  },
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 145. CHECK-037 /p3/1/tube_mass_kg (projection_5)

```json
{
  "correction": "CHECK-037 /p3/1/tube_mass_kg (projection_5)",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": 3733.1853334618195,
  "new": 3794.671994894594,
  "delta_kg": 61.486661432774326,
  "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
  "source": {
    "report": "rpt-ref-bba592d71d65b13cc2e5",
    "file": "evidence/17d9e138610b8036-AUDIT.json",
    "original_file": "evidence/17d9e138610b8036-AUDIT.json",
    "sha256": "17d9e138610b803643ab71d3df14a9cfeecd4ef1ab10c17f060ff61baed2f8b3",
    "selector": "row=/p3/1,field=tube_mass_kg"
  },
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 146. CHECK-037 /p3/2/tube_mass_kg (projection_019)

```json
{
  "correction": "CHECK-037 /p3/2/tube_mass_kg (projection_019)",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": 3581.5126092693927,
  "new": 3640.5011762956547,
  "delta_kg": 58.98856702626199,
  "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
  "source": {
    "report": "rpt-ref-bba592d71d65b13cc2e5",
    "file": "evidence/17d9e138610b8036-AUDIT.json",
    "original_file": "evidence/17d9e138610b8036-AUDIT.json",
    "sha256": "17d9e138610b803643ab71d3df14a9cfeecd4ef1ab10c17f060ff61baed2f8b3",
    "selector": "row=/p3/2,field=tube_mass_kg"
  },
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 147. CHECK-037 /p3/3/tube_mass_kg (projection_019)

```json
{
  "correction": "CHECK-037 /p3/3/tube_mass_kg (projection_019)",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": 3581.5126092693927,
  "new": 3640.5011762956547,
  "delta_kg": 58.98856702626199,
  "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
  "source": {
    "report": "rpt-ref-bba592d71d65b13cc2e5",
    "file": "evidence/17d9e138610b8036-AUDIT.json",
    "original_file": "evidence/17d9e138610b8036-AUDIT.json",
    "sha256": "17d9e138610b803643ab71d3df14a9cfeecd4ef1ab10c17f060ff61baed2f8b3",
    "selector": "row=/p3/3,field=tube_mass_kg"
  },
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 148. CHECK-037 /p3/4/tube_mass_kg (mylar_5)

```json
{
  "correction": "CHECK-037 /p3/4/tube_mass_kg (mylar_5)",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": 4082.490566662958,
  "new": 4083.0053057749465,
  "delta_kg": 0.5147391119885469,
  "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
  "source": {
    "report": "rpt-ref-bba592d71d65b13cc2e5",
    "file": "evidence/17d9e138610b8036-AUDIT.json",
    "original_file": "evidence/17d9e138610b8036-AUDIT.json",
    "sha256": "17d9e138610b803643ab71d3df14a9cfeecd4ef1ab10c17f060ff61baed2f8b3",
    "selector": "row=/p3/4,field=tube_mass_kg"
  },
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 149. CHECK-037 /p3/5/tube_mass_kg (mylar_019)

```json
{
  "correction": "CHECK-037 /p3/5/tube_mass_kg (mylar_019)",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": 3925.4252327975605,
  "new": 3925.920168386683,
  "delta_kg": 0.49493558912263325,
  "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
  "source": {
    "report": "rpt-ref-bba592d71d65b13cc2e5",
    "file": "evidence/17d9e138610b8036-AUDIT.json",
    "original_file": "evidence/17d9e138610b8036-AUDIT.json",
    "sha256": "17d9e138610b803643ab71d3df14a9cfeecd4ef1ab10c17f060ff61baed2f8b3",
    "selector": "row=/p3/5,field=tube_mass_kg"
  },
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 150. CHECK-037 /p3/6/tube_mass_kg (ti_kapton_5)

```json
{
  "correction": "CHECK-037 /p3/6/tube_mass_kg (ti_kapton_5)",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": 4681.445574594023,
  "new": 3280.644870479246,
  "delta_kg": -1400.800704114777,
  "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
  "source": {
    "report": "rpt-ref-bba592d71d65b13cc2e5",
    "file": "evidence/17d9e138610b8036-AUDIT.json",
    "original_file": "evidence/17d9e138610b8036-AUDIT.json",
    "sha256": "17d9e138610b803643ab71d3df14a9cfeecd4ef1ab10c17f060ff61baed2f8b3",
    "selector": "row=/p3/6,field=tube_mass_kg"
  },
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 151. CHECK-037 /p3/7/tube_mass_kg (ti_kapton_019)

```json
{
  "correction": "CHECK-037 /p3/7/tube_mass_kg (ti_kapton_019)",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": 4478.93999775417,
  "new": 3138.733815147143,
  "delta_kg": -1340.2061826070267,
  "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
  "source": {
    "report": "rpt-ref-bba592d71d65b13cc2e5",
    "file": "evidence/17d9e138610b8036-AUDIT.json",
    "original_file": "evidence/17d9e138610b8036-AUDIT.json",
    "sha256": "17d9e138610b803643ab71d3df14a9cfeecd4ef1ab10c17f060ff61baed2f8b3",
    "selector": "row=/p3/7,field=tube_mass_kg"
  },
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 152. CHECK-037 /p3/8/tube_mass_kg (cfrp_zylon_5)

```json
{
  "correction": "CHECK-037 /p3/8/tube_mass_kg (cfrp_zylon_5)",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": 2102.6112155993883,
  "new": 4126.9865492776535,
  "delta_kg": 2024.3753336782652,
  "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
  "source": {
    "report": "rpt-ref-bba592d71d65b13cc2e5",
    "file": "evidence/17d9e138610b8036-AUDIT.json",
    "original_file": "evidence/17d9e138610b8036-AUDIT.json",
    "sha256": "17d9e138610b803643ab71d3df14a9cfeecd4ef1ab10c17f060ff61baed2f8b3",
    "selector": "row=/p3/8,field=tube_mass_kg"
  },
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 153. CHECK-037 /p3/9/tube_mass_kg (cfrp_zylon_019)

```json
{
  "correction": "CHECK-037 /p3/9/tube_mass_kg (cfrp_zylon_019)",
  "by": [
    "rpt-ref-bba592d71d65b13cc2e5"
  ],
  "old": 2014.309964427877,
  "new": 3957.5886775659837,
  "delta_kg": 1943.2787131381067,
  "effect_on_lead": "Historical 022c material/arc correction; current 022d not replaced",
  "source": {
    "report": "rpt-ref-bba592d71d65b13cc2e5",
    "file": "evidence/17d9e138610b8036-AUDIT.json",
    "original_file": "evidence/17d9e138610b8036-AUDIT.json",
    "sha256": "17d9e138610b803643ab71d3df14a9cfeecd4ef1ab10c17f060ff61baed2f8b3",
    "selector": "row=/p3/9,field=tube_mass_kg"
  },
  "register_version": "030c",
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## 154. 040/037b fold confirmed

```json
{
  "correction": "040/037b fold confirmed",
  "by": "rpt-ref-378f34abc5a6eea5b053",
  "effect_on_lead": "All as-designed 250°F rows fail the minimum-strength free-edge screen. Geometry-specific 200°F/scarf repair is distinct from the original +0.120151 kg allowance; positive conditional payload is not an assembly qualification.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 155. 043 uses the direct 041 f5 frames

```json
{
  "correction": "043 uses the direct 041 f5 frames",
  "by": "rpt-ref-14993e3c2e5e64177c8f",
  "effect_on_lead": "At their own screens, m=10 and assumed 3.9 GPa complete-member scale give Pf .002524/.002143; interpreting 3.9 GPa at 1 cm³ instead gives .991133/.979046. These are different uncalibrated populations.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 156. Build-route values corrected by CHECK-042

```json
{
  "correction": "Build-route values corrected by CHECK-042",
  "by": "rpt-ref-049190971618f3ca1e72",
  "effect_on_lead": "S-II .254 mm is a core-face matching gap, not spherical error. Simply supported critical disbond is 27.127598 mm. Two-skin seams total 5683.037–5685.225 m with at least 1190 panels per skin at 30.34:1. The 200°F data do not qualify the specified bond.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 157. Damage requirement added for both leads

```json
{
  "correction": "Damage requirement added for both leads",
  "by": "rpt-ref-57c98dcce7960aca042a",
  "effect_on_lead": "028b/022d damage models find no priced damage-tolerant float on their original budgets. Local crushed-core growth and member-loss/film-tear screens consume the intact margins. Transfer to 048/041 geometry requires reclosure; no operating protocol is qualified.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 158. P3 film life and protection charged

```json
{
  "correction": "P3 film life and protection charged",
  "by": "rpt-ref-b6da4592385c83f4db2a",
  "effect_on_lead": "No installed film life is demonstrated. At 041, OD4/white protection is 95.751 kg; hot-film corrections plus equipment leave 31.465–51.465 / 39.916–59.916 kg closure deficits. Ten-year SF depends on the unselected ageing law.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 159. Common-account sensitivities and thermal limit retained

```json
{
  "correction": "Common-account sensitivities and thermal limit retained",
  "by": "rpt-ref-593068c3ed82fd458128",
  "effect_on_lead": "Arithmetic matches conditional on the owner temperature table; independent thermal reproduction remains open. One millimetre of water removes every original primary float. Cure in global/crimp demand gives R15 optimistic actual −1.821 kg; edge/scarf coincidence removes four of thirteen primary floats.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 160. Light coating recovers conditional R10 ISA float

```json
{
  "correction": "Light coating recovers conditional R10 ISA float",
  "by": "rpt-ref-2092a3e39c7141afde61",
  "effect_on_lead": "Multilayer CCAg/ITO at 7.5752 g/m² plus 10%, separate 10 g/m² structural primer, .1 kg/m² exterior water and a distinct material-water inventory give +124.262 kg at the original R10 ISA bake endpoint. Optics and process transfer remain unqualified.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 161. Film label and pad credit corrected

```json
{
  "correction": "Film label and pad credit corrected",
  "by": "rpt-1228-mainline044-independent-check-1020",
  "effect_on_lead": "The .060 fatigue-test film is AF163-2K. The +36.661200 kg strict-pad/60:1-scarf scenario requires 3.414034 kg old-plate credit; without documented credit the addition is +40.075234 kg. Installed life stays null.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 162. Proof and mass labels corrected

```json
{
  "correction": "Proof and mass labels corrected",
  "by": "rpt-ref-a53ddf165139979127c4",
  "effect_on_lead": "At 1.25× target force the member Euler ratio is .375, not buckling. Exceeding the combined screen does not establish Euler failure; fixtures and stress coverage remain open. Required Pf10⁻⁶ member scales are 8.53751/8.39866 GPa. Rise8 is 5446.291 kg total, 5039.558 kg tubes.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 163. Direct-frame computation corroborated with exact limits

```json
{
  "correction": "Direct-frame computation corroborated with exact limits",
  "by": "rpt-ref-52963d63a80d69bb90bd",
  "effect_on_lead": "Fixed f5 screens 1.143285/1.083205 and local sensitivities 1.033223/.978132 reproduce. Independent nonlinear continuation corroborates the m24 bracket. Nine printed cells differ, including film-direction and midpoint values; prior postprocessor exposure is disclosed.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 164. Film-life audit adds quantitative limits

```json
{
  "correction": "Film-life audit adds quantitative limits",
  "by": "rpt-ref-982a0ff761f72abce96c",
  "effect_on_lead": "Required retention and ten-year scenarios reproduce. Coupon-only 458.672527 kg/year becomes 459.261468 with weighted leakage. Warehouse reading uncertainty crosses SF1 at both f5 points; hot 041-5 annual loss ceiling is .457%, below the .5% requirement.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 165. CHECK-040 folded into 048

```json
{
  "correction": "CHECK-040 folded into 048",
  "by": "rpt-ref-9a9a131b4ca724b68cc2",
  "effect_on_lead": "648 new rows include cure compression and both water scenarios. All 432 1 mm R10–15 cases fail to float; best all-four is −998.333 kg. Cure-included R10 ISA bake is +118.695 kg, least G+Q+film usage .842794; two marginal floats are lost. Exact 2U .015 bond qualification stays open.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 166. 050 operational exception retained as history

```json
{
  "correction": "050 operational exception retained as history",
  "by": "rpt-1228-mainline050-simjob-refusal-retry-request-1020",
  "effect_on_lead": "A canonical exception report records refusal before execution and a request for retry authority. The subsequently filed050 card reports authorized unchanged retries and completion. The exception itself supplies no numerical result.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 167. Partial CHECK-048: supplied bill matches; full check remains open

```json
{
  "correction": "Partial CHECK-048: supplied bill matches; full check remains open",
  "by": "rpt-ref-29ebe6d900e7cbd982ea",
  "effect_on_lead": "At7149 stored points, compared bills/modes/payloads match conditional on owner thermal tables. The+124.261910kg R10 bill reproduces. Three vacuum bookkeeping fields differ; proposed corrections are unverified. Thermal297/325 comparisons differ and independent searches are unfinished. The classical optical citation gives alpha.08/normal epsilon.72 on Kapton, not the model's.09/.65.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 168. Partial 051: load-specific member targets complete, candidate frames pending

```json
{
  "correction": "Partial 051: load-specific member targets complete, candidate frames pending",
  "by": "rpt-ref-8d5027d15bbe034522e3",
  "effect_on_lead": "All288 reliability target rows are filed. Under assumed member-scale3.9GPa/m10, q1 Pf=.000643916/.000947308 meets1e-3, while own-screen Pf does not. Own-screen Pf1e-3 scales are4.278678/4.209090GPa; candidate masses/SFs and041damage remain null. Old f5 stress amplification2.427/2.480 differs from f4's3.27.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 169. CHECK-045 corrects damage arithmetic and limits categorical claims

```json
{
  "correction": "CHECK-045 corrects damage arithmetic and limits categorical claims",
  "by": "rpt-ref-e0fc07c506c86dae19c1",
  "effect_on_lead": "Main danger screens reproduce;1358 comparisons include71 differences and88 exact findings. The55mm growth threshold is19.176311mm within the core; Pach calibration does not agree. PerrySF is3.454499, not4.095818. Better wall/tear witnesses remain below1. All-edge stress ratios1.959485–3.270739 and trajectory/inspection corrections do not establish universal cascade or a safe vent protocol.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 170. 052 closes a conditional P3 whole bill with additional strength assumptions

```json
{
  "correction": "052 closes a conditional P3 whole bill with additional strength assumptions",
  "by": "rpt-ref-d7b2450119f373b2d1db",
  "effect_on_lead": "Resized f5-019 first closes at tested R10 ISA/R12 optimistic with ground service; full endpoints +30.863/+46.259kg. R10 least S+F+J usage.839340 requires5.343GPa effective ply strength and planned15.552h ground service. No combined-weather or24h onboard-dry case closes throughR30. Its original048 comparison is supplemented with the cure-included account and the same extra50kg service debit.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 171. 050 separates weather design families from one fixed hull

```json
{
  "correction": "050 separates weather design families from one fixed hull",
  "by": "rpt-1228-mainline050-flyable-weather-1020",
  "effect_on_lead": "The2,027,245-point map extends the original048 finish account throughR30. No sampled radius closes the declared MIL10% hot profile, even at all four endpoints. At100m the full-range fixed R10/R30 upper ISA offsets are−6.5/+3.3K, versus family+5.8/+15.8K; cold limit about−10.5K. R10 saturated-clear dew gives−82.280kg. The cure-included alternate and operational probabilities remain unqualified.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```

## 172. R30 beryllium supply scale

```json
{
  "correction": "R30 beryllium supply scale",
  "by": "rpt-ref-3e02218a03708a878faa",
  "effect_on_lead": "102.230791t faces at original040 named endpoint; 23.609882% of revised2024 output433t; distinct from103.146t least-usage point.",
  "lead_relevant": true,
  "register_version": "030d",
  "tag": "QUESTIONABLE / PROJECTION",
  "ids_in_store": []
}
```
