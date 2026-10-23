# MAINLINE-030c — complete issue register

QUESTIONABLE / PROJECTION. Current 030c annotations govern; original source fields and dispositions remain verbatim history. Counts include attributed duplicates and resolved records.

## R001 — hull radius and volume convention (mould line vs mid-surface, wall intrusion)

**Original question:** Handbook radius is the middle surface; ratios use external 10 m and are unaffected since both pressures scale as 1/R^2; absolute pressure on thick rows needs an inner mould line.

### N036 — NFI-GEOM

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-GEOM",
  "gap": "External area and external volume ignore wall and core intrusion.",
  "direction": "Inner and outer mould lines.",
  "effect": "A smaller displaced volume lowers the ceiling. At 1 kg/m3 the buckling-peak core is 1.81457668291 m, which is not a thin wall on a 10 m radius."
}
```

### N045 — NFI-GEOM

Source `rpt-ref-3dd5ab5528276031581d`; original file `unpublished-local-ref:474808f25f6dc0cd; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-GEOM",
  "gap": "The handbook radius is the middle surface. These ratios use the external 10 m in both the classical pressure and the handbook pressure, so the ratio is unchanged.",
  "direction": "An absolute pressure on the thick low-density rows still needs an inner mould line.",
  "effect": "The reported safety-factor ratios do not move with that choice."
}
```

### N249 — NFI-GEOM

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-GEOM",
  "linked_inputs_or_points": "all points",
  "questionable_assumption_or_gap": "External volume ignores skin intrusion and member protrusion.",
  "direction_of_further_investigation": "Define inner and outer mould lines.",
  "how_it_affects_margin_or_SF": "Volume error moves lift linearly."
}
```

### N259 — NFI-GEOM

Source `rpt-mainline002-grok-strength-card-1019`; original file `unpublished-local-ref:f02996967e2f160d; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-GEOM",
  "gap": "External volume still ignores wall intrusion.",
  "direction": "Inner and outer mould lines.",
  "effect": "Volume error moves lift and the allocation thicknesses."
}
```

### N269 — NFI-GEOM

Source `rpt-mainline003-grok-p2-targets-1019`; original file `unpublished-local-ref:c644022670e558c3; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-GEOM",
  "gap": "External volume still ignores wall and core intrusion.",
  "direction": "Inner and outer mould lines.",
  "effect": "A smaller displaced volume lowers the ceiling."
}
```

### N303 — NFI-GEOM

Source `rpt-mainline007b-check-lead4f19-1019`; original file `unpublished-local-ref:c88bee0b56cece84; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-GEOM",
  "gap": "Confirmed: handbook radius is the middle surface; ratios use external 10 m in both pressures and do not move with that choice, since both scale as 1/R^2.",
  "direction": "Absolute pressure on thick rows still needs an inner mould line.",
  "effect": "Owner statement stands."
}
```

### C071 — NFI-034-GEOMETRY

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/10`.

```json
{
  "id": "NFI-034-GEOMETRY",
  "tag": "QUESTIONABLE",
  "finding": "Uses 021b face/core geometry and re-sizes 028 scarfs to its panel width. Uses 022c cap sag for volume and the original sphere area for films; a 10% area sensitivity is supplied. A sphere cutting pattern and exact pillow area are absent. P3 internal solid volume is neglected in the pressure model.",
  "proposed_next": "Carry an actual surface-area, solid-volume, seam-length and node inventory with the manufactured layout.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C118 — NFI-029-RADIUS

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/8`.

```json
{
  "id": "NFI-029-RADIUS",
  "status": "resolved-by-explicit-convention",
  "title": "Brief aspect-ratio range",
  "issue": "The sealed021 point hasR_outer/tc494.7219, not at most480.021b332.0248. Use mean radius for paper to reproduce018b and outer radius for lead to compare021; record both.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

## R002 — ISA case is a standard dry column, not a site or day

**Original question:** Dry constant-g geopotential formula used with geometric height substituted; no humidity case; density and pressure drive float margin and every safety factor.

### N099 — NFI-AIR-FRACTIONS

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-AIR-FRACTIONS",
  "state": "assumption",
  "note": "Dry-air mole fractions 0.20946 and 0.78084 are not in the vacuum case."
}
```

### N146 — NFI-010-ISA

Source `rpt-ref-58b2bed18db2449100f2`; original file `unpublished-local-ref:9b713febb61ac916; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-010-ISA",
  "gap": "ISA is a standard column, not weather. The 500 m point matches the pinned case within 0.1 Pa; other altitudes are the same formula, QUESTIONABLE.",
  "direction": "Fly a measured column when a site is named.",
  "effect": "Lever 2 numbers move with the real lapse and pressure."
}
```

### N242 — NFI-ISA

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-ISA",
  "linked_inputs_or_points": "common atmosphere",
  "questionable_assumption_or_gap": "Dry constant-g geopotential formula; geometric height substituted.",
  "direction_of_further_investigation": "Pin ISO 2533 or ICAO Doc 7488 table at 500 m and a humidity case.",
  "how_it_affects_margin_or_SF": "Density moves float margin. Pressure moves every SF inversely."
}
```

### N252 — NFI-CHARTER

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-CHARTER",
  "linked_inputs_or_points": "sensitivity only",
  "questionable_assumption_or_gap": "Charter density and sea-level survival belong to the historical note.",
  "direction_of_further_investigation": "Do not let them replace the 500 m case.",
  "how_it_affects_margin_or_SF": "Shown only as labelled sensitivities."
}
```

## R003 — buckling SF is linear in kd only at fixed geometry

**Original question:** The claim that local needs are independent of kd holds only at fixed geometry; re-optimising for a new kd changes thicknesses and local needs.

### N009 — NFI-CHECK013-KD-CONDITION

Source `rpt-1228-mainline013-independent-check-1020`; original file `unpublished-local-ref:b1c8a108ddfdc4b1; pointer `retained original identity`.

```json
{
  "id": "NFI-CHECK013-KD-CONDITION",
  "kind": "clarification",
  "row": "CARD.md needs paragraph / RESULTS.json kd_scaling",
  "field": "independence of local needs from kd",
  "card_value": "Crush, crimp, wrinkling needs and face stress independent of kd; Q h_eq scales inversely with kd.",
  "checker_value": "Local equations have no explicit kd at fixed geometry. Reoptimising Q changes tf, tc, stress and local needs.",
  "example_at_rho_1": {
    "0.1": {
      "h_m": 0.378140402372981,
      "face_stress_Pa": 396250728.3544923,
      "EcGc_req_foam_design_Pa2": 2.026414217431143e+16,
      "Gc_req_crimp_Pa": 1260230.2477890702
    },
    "0.2": {
      "h_m": 0.1890702011864905,
      "face_stress_Pa": 374476671.6434306,
      "EcGc_req_foam_design_Pa2": 1.710378811012676e+16,
      "Gc_req_crimp_Pa": 2515972.0959315384
    },
    "0.4": {
      "h_m": 0.09453510059324526,
      "face_stress_Pa": 364463013.9183118,
      "EcGc_req_foam_design_Pa2": 1.5768064581253444e+16,
      "Gc_req_crimp_Pa": 5013990.593276669
    }
  },
  "proposed_fix": "Qualify the scaling statement by fixed geometry. Rebuild Q if kd changes.",
  "nonblocking": true,
  "halts_owner": false,
  "halts_next_card": false
}
```

### N122 — NFI-005-KD

Source `rpt-ref-eb07faa637b7487d6dc5`; original file `unpublished-local-ref:2ef2c84bad6b0b03; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-005-KD",
  "gap": "All buckling requirements use kd = 0.2 and scale as 1/kd. MAINLINE-004's named knockdown curve is still running.",
  "direction": "Multiply each E requirement by 0.2/kd when 004 lands; no other number changes.",
  "effect": "A larger knockdown factor lowers every required E in this card."
}
```

### N137 — NFI-008-KD

Source `rpt-ref-45da79edf548b064b228`; original file `unpublished-local-ref:20c691c11e9fda46; pointer `retained original identity`.

```json
{
  "id": "NFI-008-KD",
  "issue": "All buckling SFs inherit kd=0.2; required E scales as 1/kd (Una's 003 correction), so every SF_b scales linearly with kd/0.2.",
  "effect": "MAINLINE-004's knockdown rescales every buckling column by one multiplication, as COMMON.md states.",
  "needed": "MAINLINE-004 filed values (next job 008c)."
}
```

### N285 — NFI-KD-020

Source `rpt-mainline006-check-lead4f19-1019`; original file `unpublished-local-ref:5ea5fd1bf192b52a; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD-020",
  "gap": "Confirmed: buckling uses kd 0.2 from MAINLINE-002 and scales linearly with kd. Yield does not move with kd.",
  "direction": "Multiply buckling SF by kd/0.2 when a later card adopts another knockdown.",
  "effect": "Owner statement stands."
}
```

### N289 — NFI-KD-020

Source `rpt-mainline006-grok-float-margin-1019`; original file `unpublished-local-ref:50c93f23f6adae0f; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD-020",
  "gap": "Buckling uses kd 0.2 from MAINLINE-002. MAINLINE-004b carries 0.90 as a QUESTIONABLE optimistic factor. Buckling SF on this card scales linearly with kd.",
  "direction": "Multiply buckling SF by kd/0.2 when a later card adopts another knockdown.",
  "effect": "Yield SF does not move with kd."
}
```

### N297 — NFI-KD

Source `rpt-mainline007-check-lead4f19-1019`; original file `unpublished-local-ref:a0b67c87ff180a29; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD",
  "gap": "Confirmed: kd stays 0.2. Buckling pressure and SF scale with kd; the modulus factor scales as 1/kd; yield, membrane, crimp, wrinkling product and crush do not move with kd.",
  "direction": "MAINLINE-004 is one multiplication.",
  "effect": "Owner statement stands."
}
```

### N318 — NFI-KD-020

Source `rpt-mainline012-grok-equal-margin-1019`; original file `unpublished-local-ref:e1f08cf5f095ddec; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD-020",
  "gap": "Buckling uses kd 0.2. The 004b optimistic carry is 0.90. Buckling SF scales linearly with kd.",
  "direction": "Multiply buckling SF by kd/0.2 if a later card adopts the carry.",
  "effect": "Yield SF does not move with kd."
}
```

### N388 — NFI-015B-KD-UNCHANGED

Source `rpt-ref-74e882831c201b1a953c`; original file `unpublished-local-ref:71470bf7da8d8fcd; pointer `/rows/4`.

```json
{
  "id": "NFI-015B-KD-UNCHANGED",
  "issue": "The codex check's continuous SF 1 threshold is kd 0.5183040769, with global buckling and face yield active. The mode formulas already used nu 0.33. This card changes the tolerance map only.",
  "consequence": "The knockdown result is not replaced. kd 0.519 remains the first passing point on the 0.001 grid.",
  "next": "None."
}
```

## R004 — knockdown transfer from monocoque to sandwich sphere at R 10 m

**Original question:** The curve is monolithic clamped-cap evidence; phi equal pi and the equivalent thickness are transfers onto a complete sandwich sphere, so the buckling SF is not a validated sandwich knockdown.

### N143 — NFI-008B-KD-TRANSFER

Source `rpt-ref-cc9cef5e55adca018a8f`; original file `unpublished-local-ref:2bbb739a4c037482; pointer `retained original identity`.

```json
{
  "id": "NFI-008B-KD-TRANSFER",
  "inherited": "004b's transfer caveats",
  "issue": "The conservative SP-8032 factor is a monocoque cap curve transferred to the sandwich (phi = pi, t_eq = (6 tf d^2)^(1/3)); the central 0.20 is monocoque dome evidence; the 0.90 carry is from shells at lambda 1.58-33.18 while this sphere sits near lambda 65-68.",
  "consequence": "All three levels are QUESTIONABLE; the optimistic 0.90 is outside the regime by 004b's own reading.",
  "next": "007b-adjacent: a sandwich-specific knockdown for this geometry."
}
```

### N177 — NFI-015-SANDWICH-TRANSFER

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-SANDWICH-TRANSFER",
  "issue": "Every kd curve used here is a monocoque result transferred through t_eq = sqrt(3)(d+tf). No sandwich kd-versus-amplitude measurement was retrieved at this radius. The mapping preserves the radius of gyration by construction.",
  "consequence": "The tolerance table carries this transfer as its central QUESTIONABLE. It is the sibling of 004b's NFI-KD-TRANSFER.",
  "next": "A sandwich imperfection study at this geometry."
}
```

### N272 — NFI-TRANSFER

Source `rpt-mainline004-grok-knockdown-card-1019`; original file `unpublished-local-ref:bd4eb9f1634108a4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-TRANSFER",
  "gap": "The curve is monolithic clamped-cap evidence. Phi equals pi and the equivalent thickness are transfers onto a complete sandwich sphere.",
  "direction": "A sandwich knockdown test or formula at these proportions.",
  "effect": "The stated buckling safety factor is not a validated sandwich knockdown."
}
```

### N279 — NFI-TRANSFER

Source `rpt-mainline004b-grok-kd-range-1019`; original file `unpublished-local-ref:1b2ceafd06f5792e; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-TRANSFER",
  "gap": "SP-8032, the Wagner 2020 elastic statement, and the Krenzke upper are monocoque or dome evidence. They are transferred onto a complete sandwich sphere with phi equal to pi and t_eq = (6*tf*d^2)^(1/3).",
  "direction": "Keep the transfer tagged QUESTIONABLE until a sandwich source at these proportions exists.",
  "effect": "The buckling safety factors are not validated sandwich knockdowns."
}
```

### N280 — NFI-SANDWICH

Source `rpt-mainline004b-grok-kd-range-1019`; original file `unpublished-local-ref:1b2ceafd06f5792e; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SANDWICH",
  "gap": "The sourced foam-core factors are Sim et al. 2024: dimple 0.20 and flat 0.22, from numerical postbuckling of small-scale hemispheres. They do not support 0.90. The paper says NASA SP-8032 at 0.18 and NASA CR-1457 at 0.20 may not provide a suitable knockdown for hemispherical foam-core shells. Their 0.18 is not this card's SP-8032 row.",
  "direction": "A sandwich knockdown at R = 10 m.",
  "effect": "Using 0.22 instead of 0.90 would raise required modulus by 0.90/0.22."
}
```

### N520 — NFI-035-TRANSFER

Source `rpt-mainline035-opus-knockdown-tests-1020`; original file `unpublished-local-ref:4d5781abcddc2e1c; pointer `/rows/2`.

```json
{
  "id": "NFI-035-TRANSFER",
  "state": "open",
  "note": "Cylinder-to-sphere transfer of a sandwich knockdown has no test behind it. The handbook monocoque ratio at the leads' R/t_eq is 0.30-0.34 (SP-8032/SP-8007), and CR-1457 makes the same split for sandwich (0.20 hemispheres against 0.32-0.36 cylinders).",
  "settle": "029's FE run on both a cylinder and a sphere of the lead's section"
}
```

## R005 — monocoque sphere knockdown kd: value and range (SP-8032 curve, 0.14 to 0.9)

**Original question:** gamma_d is 0.20 on the moderate branch; 0.90 is not a handbook value but the precision direction; 0.1407 conservative. Separation of face-modulus knockdown from core-shear flexibility is untested.

### N034 — NFI-KD

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD",
  "gap": "Knockdown remains 0.2. MAINLINE-004 owns the curve.",
  "direction": "Multiply this card's buckling pressure and buckling safety factor by kd/0.2. Divide the modulus factor by that same ratio.",
  "effect": "Yield, membrane stress, crimp modulus, wrinkling product, and crush do not move with kd."
}
```

### N048 — NFI-KD-PRECISION

Source `rpt-ref-d5b4aaa267b71d82fe25`; original file `unpublished-local-ref:1d727f2cb127351c; pointer `retained original identity`.

```json
{
  "id": "NFI-KD-PRECISION",
  "value": "knockdown on classical sphere buckling",
  "optimistic": 0.9,
  "optimistic_source": "Wagner 2020 Table 3, Krenzke and Kiernan, reliable upper, outside this lambda. MAINLINE-004b.",
  "main_point": 0.2,
  "main_source": "Inside the sandwich data. Sim 2024 foam-core 0.20 to 0.22. Wagner 2020 central about 0.2.",
  "conservative": 0.1407,
  "conservative_source": "CARD-009 names SP-8032's 0.1407. MAINLINE-004b P2-E sealed value is 0.140725695373. Its own optimism ratio against that sealed value is near 6.4. This ledger does not replace that ratio.",
  "factor_precision_gap": 4.5,
  "factor_meaning": "0.90/0.20 = 4.5, the precision gap CARD-009 asks this ledger to carry.",
  "direction": "Knockdown tests on sandwich spheres at lambda near 66, the regime of these rows."
}
```

### N054 — NFI-HANDBOOK-GAMMA

Source `rpt-ref-d5b4aaa267b71d82fe25`; original file `unpublished-local-ref:1d727f2cb127351c; pointer `retained original identity`.

```json
{
  "id": "NFI-HANDBOOK-GAMMA",
  "value": "NASA CR-1457 gamma_d",
  "optimistic": 0.9,
  "main": 0.2,
  "conservative": 0.1407,
  "factor": 4.5,
  "note": "On the moderate-core branch gamma_d is 0.20 and the handbook safety factor is Kc times the classical kd=0.20 pressure. gamma_d of 0.90 is not a handbook value. It is the MAINLINE-004b precision direction, applied only to the classical pressure.",
  "direction": "Tests that separate face-modulus knockdown from core-shear flexibility on a complete sphere."
}
```

### N244 — NFI-KD

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD",
  "linked_inputs_or_points": "P1 I-KD",
  "questionable_assumption_or_gap": "0.2 is a cited severe typical knockdown, not a curve at R/t.",
  "direction_of_further_investigation": "Evaluate NASA SP-8032 at this complete-sphere geometry.",
  "how_it_affects_margin_or_SF": "SF scales directly with the knockdown. It does not change mass."
}
```

### N256 — NFI-KD

Source `rpt-mainline002-grok-strength-card-1019`; original file `unpublished-local-ref:f02996967e2f160d; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD",
  "gap": "Knockdown remains 0.2, the cited severe typical value, not a curve at this R/t.",
  "direction": "Evaluate NASA SP-8032 for these complete spheres.",
  "effect": "Stiffness pressure of P1 and P2 scales directly with the knockdown."
}
```

### N267 — NFI-KD

Source `rpt-mainline003-grok-p2-targets-1019`; original file `unpublished-local-ref:c644022670e558c3; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD",
  "gap": "Knockdown remains 0.2, the inherited severe typical value.",
  "direction": "Evaluate a knockdown curve at these R/t and sandwich proportions.",
  "effect": "Buckling pressure and the required modulus scale directly with the knockdown."
}
```

### N271 — NFI-KD

Source `rpt-mainline004-grok-knockdown-card-1019`; original file `unpublished-local-ref:bd4eb9f1634108a4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD",
  "gap": "The 0.14 plus 3.2 over lambda squared form is a text reproduction of NASA SP-8032, not the monograph page. The PDF was not retrieved.",
  "direction": "Pin the August 1969 page that prints the curve.",
  "effect": "A different reading of the curve would rescale buckling pressure and required modulus by the same factor."
}
```

### N277 — NFI-OPT-GAP

Source `rpt-mainline004b-grok-kd-range-1019`; original file `unpublished-local-ref:1b2ceafd06f5792e; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-OPT-GAP",
  "gap": "The carried optimistic knockdown is 0.90. The conservative knockdown is the sealed per-row SP-8032 factor near 0.1407. The ratio is about 6.4. This is the optimism that must later be grounded.",
  "direction": "A knockdown test or formula at this sphere's lambda, on a sandwich.",
  "effect": "Required face modulus at 0.90 is lower than the SP-8032 modulus by that ratio.",
  "per_row_optimistic_over_conservative": {
    "P2-A": 6.396909550113781,
    "P2-C": 6.393643427290846,
    "P2-K": 6.393879448514311,
    "P2-E": 6.395420520834183
  }
}
```

### N278 — NFI-LAMBDA

Source `rpt-mainline004b-grok-kd-range-1019`; original file `unpublished-local-ref:1b2ceafd06f5792e; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-LAMBDA",
  "gap": "No reliable row in Wagner 2020 Table 3 reaches lambda near 65-68. Krenzke's 0.11-0.90 range mixes R/t 10-212 and stiffened with unstiffened machined shells, so 0.90 may be a thick or stiffened specimen. Adam and King, reliable yes, reach 0.89 only to lambda 43.11.",
  "direction": "Separate the Krenzke upper by R/t and by stiffened versus unstiffened.",
  "effect": "The carried 0.90 is an upper end of the tabulated reliable set, not a measurement at this slenderness."
}
```

### N281 — NFI-LRSM

Source `rpt-mainline004b-grok-kd-range-1019`; original file `unpublished-local-ref:1b2ceafd06f5792e; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-LRSM",
  "gap": "Central uses the prose value 0.20. Wagner 2020 also states a numerical lower-bound knockdown of 0.21 for one deep dome, H/r about 0.5, R/t about 90, lambda about 15.7. Equation (7) was not evaluated and lambda_s was not computed. The 2018 Wagner, Huehne and Niemann threshold equation was not retrieved. The comparative-study equation rho = 5.172/lambda - 1.464 + 0.1296 was not applied; it is outside this lambda and the extract is ambiguous.",
  "direction": "Recover the 2018 threshold equation before using it. Do not extrapolate equation (7) without lambda_s.",
  "effect": "Substituting 0.21 for 0.20 would rescale required modulus by 0.20/0.21."
}
```

### N282 — NFI-CLASSICAL

Source `rpt-mainline004b-grok-kd-range-1019`; original file `unpublished-local-ref:1b2ceafd06f5792e; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-CLASSICAL",
  "gap": "Classical knockdown 1.0 is the perfect-shell bound. It is reference only.",
  "direction": "Do not carry 1.0 as the optimistic estimate.",
  "effect": "None on the carried factor."
}
```

### N322 — NFI-KD-01407

Source `rpt-mainline014-grok-balanced-sandwich-1019`; original file `unpublished-local-ref:8c5f980fe25f9829; pointer `retained original identity`.

```json
{
  "id": "NFI-KD-01407",
  "note": "0.1407 replaces the handbook gamma 0.20 on the stiff branch only. It is the brief's single figure, not a fresh SP-8032 knockdown at the optimum thickness."
}
```

### N331 — NFI-KD-01407

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-KD-01407",
  "note": "0.1407 replaces handbook gamma 0.20 on the stiff branch only. It is the brief's figure, not a fresh SP-8032 knockdown."
}
```

### N526 — NFI-035-SP8007-P

Source `rpt-mainline035-opus-knockdown-tests-1020`; original file `unpublished-local-ref:4d5781abcddc2e1c; pointer `/rows/8`.

```json
{
  "id": "NFI-035-SP8007-P",
  "state": "open",
  "note": "CR-1457 cites SP-8007 (Sept 1965) for a 0.90 lateral-pressure factor; the 1968 SP-8007 text read here gives 0.56 with no supporting data.",
  "settle": "the 1965 edition"
}
```

## R006 — core shear (crimp) in sandwich buckling: formula and Gc basis

**Original question:** Advisory crimp replaced by sourced equations; sourced cores stay on the moderate branch, buckling SF trimmed. A core G below about 2.45 MPa would enter crimping; none do.

### N030 — NFI-SAND

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SAND",
  "gap": "Buckling still uses the inherited sandwich extrapolation and omits core shear from the stated safety factor.",
  "direction": "MAINLINE-007b replaces it with a published sandwich-shell formula that includes transverse shear.",
  "effect": "The stated buckling pressure can fall once shear is inside the model."
}
```

### N031 — NFI-SHEAR

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SHEAR",
  "gap": "The shear target uses the advisory crimping formula p=2*Gc*d/R. It is not a measured sandwich-shell limit.",
  "direction": "MAINLINE-007b cites a sourced formula. Catalog G at 16 to 38 kg/m3 already clears this advisory target.",
  "effect": "Advisory crimp does not bind the catalog cores retrieved here. A real shear interaction might."
}
```

### N041 — NFI-SHEAR

Source `rpt-ref-3dd5ab5528276031581d`; original file `unpublished-local-ref:474808f25f6dc0cd; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SHEAR",
  "gap": "Advisory crimp is replaced by NASA CR-1457 equations 6.2-3 through 6.2-6. Sourced cores stay on the moderate branch. Kc trims the buckling safety factor to between 0.863720643326 and 0.991105457684 of the MAINLINE-007 value.",
  "direction": "A core shear modulus below about 2.45 MPa would enter the crimping branch. None of the sourced moduli do.",
  "effect": "P2-E with Plascore at 16 kg/m3 falls from 0.233885578993 to 0.227959198328. Yield is unchanged and still larger."
}
```

### N245 — NFI-SAND

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SAND",
  "linked_inputs_or_points": "P2",
  "questionable_assumption_or_gap": "Collapse formula extrapolates the monocoque D-S identity. Shear, wrinkling and core crush are omitted.",
  "direction_of_further_investigation": "Replace with a published sandwich-sphere formula that includes core shear.",
  "how_it_affects_margin_or_SF": "Shear would lower collapse pressure. The omission is optimistic for SF."
}
```

### N255 — NFI-SAND

Source `rpt-mainline002-grok-strength-card-1019`; original file `unpublished-local-ref:f02996967e2f160d; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SAND",
  "gap": "Sandwich buckling still extrapolates the monocoque identity and omits core shear, wrinkling and core crush.",
  "direction": "Replace with a published sandwich formula that includes shear.",
  "effect": "Shear would lower the stiffness pressure. The omission is optimistic for that limit."
}
```

### N263 — NFI-SAND

Source `rpt-mainline003-grok-p2-targets-1019`; original file `unpublished-local-ref:c644022670e558c3; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SAND",
  "gap": "Buckling still uses the inherited sandwich extrapolation and omits core shear from the stated safety factor.",
  "direction": "Replace with a published sandwich formula that includes shear.",
  "effect": "The stated buckling pressure can fall once shear is inside the model."
}
```

### N264 — NFI-SHEAR

Source `rpt-mainline003-grok-p2-targets-1019`; original file `unpublished-local-ref:c644022670e558c3; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SHEAR",
  "gap": "The shear target uses the advisory crimping formula p=2*Gc*d/R. It is not a measured core modulus.",
  "direction": "Pin a core datasheet and a sourced sandwich shear formula.",
  "effect": "The required Gc scales with external pressure and inversely with d."
}
```

### N275 — NFI-SAND

Source `rpt-mainline004-grok-knockdown-card-1019`; original file `unpublished-local-ref:bd4eb9f1634108a4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SAND",
  "gap": "Classical pressure remains the inherited sandwich extrapolation.",
  "direction": "A published sandwich formula with shear.",
  "effect": "Required modulus would move if the classical pressure moved."
}
```

### N288 — NFI-SHEAR

Source `rpt-mainline006-check-lead4f19-1019`; original file `unpublished-local-ref:5ea5fd1bf192b52a; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SHEAR",
  "gap": "Confirmed: sandwich buckling omits core shear and uses the 002 formula.",
  "direction": "A sandwich formula with shear (007b supplies one for its rows).",
  "effect": "Buckling SF would move if the pressure formula moved."
}
```

### N292 — NFI-SHEAR

Source `rpt-mainline006-grok-float-margin-1019`; original file `unpublished-local-ref:50c93f23f6adae0f; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SHEAR",
  "gap": "Sandwich buckling omits core shear. The 002 formula is used.",
  "direction": "A sandwich formula with shear.",
  "effect": "Buckling SF would move if the pressure formula moved."
}
```

### N469 — NFI-015-CHECK-SHEAR-RULE

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/3`.

```json
{
  "id": "NFI-015-CHECK-SHEAR-RULE",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "not_revisited_outside_focused_map",
  "reported": "015b acknowledges unquantified core-shear effects on imperfection sensitivity.",
  "checked": "It does not source or remove the old standalone square-root shear rule or reconcile it with NASA Kc. No new shear multiplier is applied.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Use a consistent sourced shear model, or justify the alternate model. Do not multiply an additional reduction into factors that already include Kc."
}
```

## R007 — gamma(Vc) for a sandwich sphere: CR-1457 step (0.20 below Vc 2, 1 above) vs 018 curves; P2 lead needs 0.468-0.595 (O1)

**Current 030c:** 029 is filed: paper benchmark not reproduced; weak-meridian endpoints at 015's 11.8/46 mm defects are 78.627/90.722 kPa against 95.461 kPa. These do not support the target. Any workable shape target must be tighter within that model, but physical tolerance remains uncalibrated. Current 028b+037b needs gamma .564288; 029 did not solve that joined geometry.

**030b source history:** 028b nominal R10 needs gamma .564164 (2.820818× .20); 033 screened R20/R30 need .400218/.368927. CHECK-035 revises S-II hemisphere graph centers to about .21–.22, +/- .01 reading uncertainty, with Vc and plastic/thermal reduction unresolved. Additional marine and foam-core experiments invalidate categorical absence claims. No compatible elastic sphere/dome datum with recoverable moderate Vc at the lead geometry was established; neither required gamma nor unprecedented imperfection control is validated.

**Original question:** A high shear modulus leaves the crimp branch and gamma becomes the knockdown 0.20; best aluminium stiff-branch rows reach SF 0.669 and 0.642, below the HRH-10 crimp balance 0.685.

### N004 — NFI-BRANCH-EQUALITY

Source `rpt-1228-mainline009c5-independent-check-1019`; original file `unpublished-local-ref:52f757339520e0fd; pointer `retained original identity`.

```json
{
  "id": "NFI-BRANCH-EQUALITY",
  "type": "source_endpoint_mismatch",
  "row": "Vc=2, kd=.20",
  "field": "gamma_d",
  "reported": 0.2,
  "independent": 1.0,
  "source_url": "https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf",
  "page": "6-7",
  "proposed_fix": "Use gamma=1 for Vc>=2 to follow the cited convention. Neither published point lies exactly at 2.",
  "stops_owner": false
}
```

### N016 — NFI-BRANCH-EQUALITY

Source `rpt-1228-mainline014b-independent-check-1019`; original file `unpublished-local-ref:8f2d079b76102928; pointer `retained original identity`.

```json
{
  "id": "NFI-BRANCH-EQUALITY",
  "type": "convention_clarification",
  "row": "Vc=2 boundary",
  "field": "gamma",
  "reported": "No scored 014b row is exactly on the boundary; owner code was not inspected.",
  "independent": "CR-1457 p.6-7 includes Vc=2 in weak-core region with unity knockdown.",
  "proposed_fix": "State equality handling explicitly when carrying 009c-5 branch wording; all current values unaffected.",
  "stops_owner": false
}
```

### N025 — NFI-CHK019-GAMMA-PAIRING

Source `rpt-check019-opus-1020`; original file `unpublished-local-ref:391c78ac32ab1335; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK019-GAMMA-PAIRING",
  "state": "demonstrated with 018's own curves",
  "direction": "ranking depends on the rule",
  "note": "The CR-1457 step rule gives aramid (Vc 3.1-3.5) the optimistic gamma 1 and aluminium (Vc 0.5-0.6) the conservative 0.2. Applied to both families, 018's optimistic curve (PROJECTION) gives aluminium 0.847 against aramid 0.609 on the optimistic line, 0.924 against 0.650 at 5% and 0.988 against 0.685 at 0%, where aluminium is capped by Be face compression. 018's conservative curve gives 0.557 against 0.253, 0.617 against 0.270 and 0.669 against 0.284. 'Aramid leads' on every margin line rests on the mixed pairing. The budgets were not re-solved under the curves."
}
```

### N044 — NFI-KD

Source `rpt-ref-3dd5ab5528276031581d`; original file `unpublished-local-ref:474808f25f6dc0cd; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD",
  "gap": "gamma_d is 0.20 on the moderate branch, the handbook hemisphere value, and the same number as kd. The handbook sets gamma_d to 1 on the crimping branch, so gamma_d times Kc jumps at Vc = 2.",
  "direction": "MAINLINE-004 still multiplies the moderate-branch buckling pressure by kd/0.2. Do not apply that multiplication on the crimping branch.",
  "effect": "No sourced row reached the jump."
}
```

### N075 — NFI-019-BRANCH

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-BRANCH",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "The inherited Vc=2 rule changes gamma from kd to 1. MAINLINE-018 owns its physical assessment. Under large reserve the aramid optimum leaves the crimp branch, invalidating constant-slope extrapolation.",
  "next_evidence": "Resolve the knockdown/branch model and recompute the same margin lines; this card preserves the ordered scoring rule."
}
```

### N103 — NFI-027-GAMMA

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-GAMMA",
  "tag": "PROJECTION",
  "issue": "Design uses the inherited hemispherical 0.2/1 step at Vc=2. Full 021 uses 0.2+0.4min(Vc,2). Neither is validated for this completed sphere. Constant 0.2 removes the enhanced P2 pass.",
  "next_evidence": "Carry the 018b and 015 evidence into an installed-geometry shell test/model, retaining imperfection maps."
}
```

### N192 — NFI-020-INHERITED-MODEL

Source `rpt-ref-3e02218a03708a878faa`; original file `unpublished-local-ref:3fe2376964ec428a; pointer `retained original identity`.

```json
{
  "id": "NFI-020-INHERITED-MODEL",
  "rank": 0,
  "tag": "QUESTIONABLE",
  "claim": "Crimp-branch gamma=1, stabilised Ec in wrinkling and common nu remain unvalidated inherited assumptions.",
  "optimistic": {
    "retained_crimp_gamma": 1.0,
    "nu_inherited": 0.33,
    "baseline_SF": 0.6504118436805659
  },
  "conservative": {
    "nu_VHP_sensitivity": 0.08,
    "current_E_only_SF": 0.6363083913759237,
    "validated_shell_model_SF": null
  },
  "sources": [
    {
      "id": "S07",
      "url": "https://www-pub.iaea.org/MTCD/Publications/PDF/Pub23vol5_web.pdf"
    }
  ],
  "needed_to_ground": "Resolve the inherited MAINLINE-018 crimp-step and core-modulus questions using their owning evidence; this manufacturing card does not adjudicate them.",
  "effect_on_lead": "No source or manufacturing result here establishes SF 1. Branch transitions can sharply affect direct substitutions; do not blindly scale every mode with kd.",
  "closed_by_this_card": false
}
```

### N193 — NFI-021-GAMMA

Source `rpt-ref-769a7442efd5a04681e9`; original file `unpublished-local-ref:63c049a0d93b9857; pointer `retained original identity`.

```json
{
  "id": "NFI-021-GAMMA",
  "optimism": "O1",
  "binds": true,
  "needed": 0.5953179642995181,
  "today": 0.2,
  "improvement_factor": 2.9765898214975905,
  "usage_of_018_stretch": 0.9580717283996654,
  "state": "PROJECTION: no sphere or dome test at Vc near 1 supports a knockdown above 0.20 (018)",
  "grounding_card": "MAINLINE-018b (crimp gamma measured from Sim's absolute loads); MAINLINE-015 (kd precision)",
  "tolerance_015": {
    "kd": 0.5953179642995181,
    "t_eq_mm": 36.47148976173557,
    "R_over_t_eq": 274.1867706893509,
    "in_fit_range": true,
    "wavelength_m": 0.6039163001752442,
    "status": "lambda_I_1 inversion",
    "delta_over_t_eq": 0.3235790017685749,
    "amplitude_mm": 11.801408250115193,
    "rms_worst_mm": 0.3638641267074433,
    "rms_narrow_mm": 0.13861490541235935
  },
  "note": "Under 018's conservative gamma the point is 0.338601. 015's map: one dimple of 11.8 mm (RMS 0.364 mm) at this gamma, QUESTIONABLE."
}
```

### N197 — NFI-021-CRIMP-BRANCH-GAMMA

Source `rpt-ref-769a7442efd5a04681e9`; original file `unpublished-local-ref:63c049a0d93b9857; pointer `retained original identity`.

```json
{
  "id": "NFI-021-CRIMP-BRANCH-GAMMA",
  "issue": "The aramid route floats only on the handbook's gamma 1 at Vc >= 2, which 018 tags QUESTIONABLE for a sphere.",
  "numbers": "Aramid family under the full set 1.00053; under 018's conservative gamma 0.358097.",
  "grounding_card": "MAINLINE-018b"
}
```

### N202 — NFI-021-CONSERVATIVE-READING

Source `rpt-ref-769a7442efd5a04681e9`; original file `unpublished-local-ref:63c049a0d93b9857; pointer `retained original identity`.

```json
{
  "id": "NFI-021-CONSERVATIVE-READING",
  "issue": "If 'today' is 018's conservative gamma (0.20 at every Vc), the stiff-branch least set does not change, because its today is already 0.20; a crimp-branch point needs gamma 1, a factor 5.",
  "numbers": {
    "S-200F at its own E 290 GPa and the inherited 283 MPa": {
      "branch": "stiff_or_moderate_core",
      "Vc": 1.0610630680728836,
      "gamma_needed": 0.5953179642995181,
      "factor_over_0.20": 2.9765898214975905,
      "usage_against_018_curve": 0.9580717283996654
    },
    "today = S-200-F, Materion design guide compressive yield 'about 37 ksi'": {
      "branch": "shear_crimping",
      "Vc": 2.7856228623470924,
      "gamma_needed": 0.9994717109284957,
      "factor_over_0.20": 4.997358554642479,
      "usage_against_018_curve": 0.9996716688098004
    },
    "today = SR-200 sheet, Materion datasheet minimum tensile yield (compressive about equal per the 1967 lot)": {
      "branch": "stiff_or_moderate_core",
      "Vc": 0.9986907155584266,
      "gamma_needed": 0.37038887488235733,
      "factor_over_0.20": 1.8519443744117865,
      "usage_against_018_curve": 0.5613684779431448
    },
    "E = 303 GPa as filed at 00:30 (S-200FH's value), S-200F 283 MPa today": {
      "branch": "stiff_or_moderate_core",
      "Vc": 1.108627964227875,
      "gamma_needed": 0.5791494489601828,
      "factor_over_0.20": 2.895747244800914,
      "usage_against_018_curve": 0.9098990057213333
    }
  }
}
```

### N203 — NFI-021b-GAMMA

Source `rpt-ref-1080d4f6a1af4cfa8c67`; original file `unpublished-local-ref:4edbd73193c8c843; pointer `retained original identity`.

```json
{
  "id": "NFI-021b-GAMMA",
  "optimism": "O1",
  "needed": 0.46822856667720764,
  "today": 0.2,
  "full_at_point": 0.5544727352669614,
  "improvement_factor": 2.341142833386038,
  "usage": 0.83420513484806,
  "state": "PROJECTION",
  "grounding_card": "MAINLINE-018b; MAINLINE-015's map",
  "tolerance_015": {
    "kd": 0.46822856667720764,
    "t_eq_mm": 53.364448806653826,
    "R_over_t_eq": 187.39067344687226,
    "in_fit_range": true,
    "status": "lambda_I_1 inversion",
    "delta_over_t_eq": 0.8586135991025216,
    "amplitude_mm": 45.819441454003304,
    "rms_worst_mm": 1.7088520330420545
  }
}
```

### N211 — NFI-021b-ARAMID-BLOCKED

Source `rpt-ref-1080d4f6a1af4cfa8c67`; original file `unpublished-local-ref:4edbd73193c8c843; pointer `retained original identity`.

```json
{
  "id": "NFI-021b-ARAMID-BLOCKED",
  "issue": "The aramid family reaches 0.9407 with every optimism full; core shear crimping, which no named optimism touches, ties with global and wrinkling on the crimp branch."
}
```

### N241 — NFI-028-20

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-20",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Inherited shell optimisms",
  "today_value": "Needed gamma=0.595318 and wrinkle coefficient=0.370681 held fixed",
  "required_or_budget_target": {
    "gamma_ratio_to_0p2": 2.9765898214975905,
    "wrinkle_ratio_to_0p33": 1.1232748900708642
  },
  "needed_evidence": "Independent grounding of the inherited imperfection and wrinkle model. A computed joining improvement does not close these rows.",
  "factor_to_216_427kg_allowance": null,
  "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."
}
```

### N299 — NFI-SHEAR

Source `rpt-mainline007b-check-lead4f19-1019`; original file `unpublished-local-ref:c88bee0b56cece84; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SHEAR",
  "gap": "Confirmed: sourced cores stay on the moderate branch (all Vc < 2). Kc trims buckling SF to 0.863720643326-0.991105457684 of the 007 value. P2-E/Plascore 16 falls 0.2338855789925097 to 0.22795919832772132; yield unchanged and larger.",
  "direction": "A core shear modulus below about 2.45 MPa would enter the crimping branch. None sourced does.",
  "effect": "Owner statement stands."
}
```

### N302 — NFI-KD

Source `rpt-mainline007b-check-lead4f19-1019`; original file `unpublished-local-ref:c88bee0b56cece84; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KD",
  "gap": "Confirmed: gamma_d = 0.20 on the moderate branch, equal to kd, with a handbook jump to 1 at Vc=2 that no sourced row reaches. Do not apply the MAINLINE-004 kd/0.2 multiplication on the crimping branch.",
  "direction": "Owner direction stands.",
  "effect": "No sourced row reached the jump."
}
```

### N327 — NFI-HEMISPHERE

Source `rpt-mainline014-grok-balanced-sandwich-1019`; original file `unpublished-local-ref:8c5f980fe25f9829; pointer `retained original identity`.

```json
{
  "id": "NFI-HEMISPHERE",
  "note": "Handbook gamma 0.20 is the CR-1457 hemisphere value. A complete sphere has no edge. MAINLINE-007b already recorded that the 0.20 rests on meager tests."
}
```

### N344 — NFI-HEMISPHERE

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-HEMISPHERE",
  "note": "Handbook gamma 0.20 is the CR-1457 hemisphere value. A complete sphere has no edge."
}
```

### N347 — NFI-STIFF-BRANCH

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-STIFF-BRANCH",
  "note": "A high shear modulus leaves the crimp branch. Gamma then becomes the knockdown 0.20, and global buckling is scored with that factor. For Be S-200F the best aluminium row is CR-III 5056 at 1.6 pcf, least SF 0.668649769509 by global buckling, below the HRH-10 crimp balance 0.685338231171. The 1/4 and 3/8 cells tie. Plascore 3/16-2.0, W shear 20 ksi and transferred Ec 34 ksi, reaches 0.641722323466 by the same mode. The higher W shear does not raise the leading safety factors. 6061-T6 does move, to 0.145930331406 on CR-III 5056 3/8-1.0."
}
```

### N349 — NFI-017-GC-BRANCH

Source `rpt-mainline017-improvement-directions-lead4f19-1019`; original file `unpublished-local-ref:b586b896a14aa878; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-017-GC-BRANCH",
  "gap": "Raising core Gc alone lowers Vc. Past Vc = 2 the CR-1457 branch sets gamma = kd (0.20) instead of 1, so the least SF falls (caps 0.510 CNT, 0.560 Be, 0.403 graphene at a 1e4 multiplier in my scan). The governing mode's own property is not a direction alone.",
  "direction": "Any Gc direction must be paired with a knockdown direction, which has no sourced value above 0.20 today.",
  "effect": "Gc is listed as not alone on all three P2 leaders."
}
```

### N424 — NFI-028b-af015_scarf-gamma

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/0`.

```json
{
  "id": "NFI-028b-af015_scarf-gamma",
  "status": "OPEN",
  "issue": "Ground gamma at the actual jointed geometry, including imperfections.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": 0.5641635666030083,
  "today": 0.2,
  "improvement_factor": 2.8208178330150413,
  "null_factor_reason": null,
  "source": "MAINLINE-018 curve",
  "usage": 0.9719775174295638,
  "full": 0.5812855410551349
}
```

### N426 — NFI-028b-af015_scarf_primer5-gamma

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/2`.

```json
{
  "id": "NFI-028b-af015_scarf_primer5-gamma",
  "status": "OPEN",
  "issue": "Ground gamma at the actual jointed geometry, including imperfections.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": 0.5785244156939786,
  "today": 0.2,
  "improvement_factor": 2.892622078469893,
  "null_factor_reason": null,
  "source": "MAINLINE-018 curve",
  "usage": 0.9960764380867377,
  "full": 0.580949962703325
}
```

### N428 — NFI-028b-lab8_eb_eta1-gamma

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/4`.

```json
{
  "id": "NFI-028b-lab8_eb_eta1-gamma",
  "status": "OPEN",
  "issue": "Ground gamma at the actual jointed geometry, including imperfections.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": 0.39149957705208616,
  "today": 0.2,
  "improvement_factor": 1.9574978852604308,
  "null_factor_reason": null,
  "source": "MAINLINE-018 curve",
  "usage": 0.6514685431051914,
  "full": 0.5607762431930751
}
```

### N430 — NFI-028b-lab8_scarf-gamma

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/6`.

```json
{
  "id": "NFI-028b-lab8_scarf-gamma",
  "status": "OPEN",
  "issue": "Ground gamma at the actual jointed geometry, including imperfections.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": 0.5559108486791616,
  "today": 0.2,
  "improvement_factor": 2.779554243395808,
  "null_factor_reason": null,
  "source": "MAINLINE-018 curve",
  "usage": 0.9578679244374443,
  "full": 0.5814783035567451
}
```

### N489 — NFI-031-P2-GAMMA

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/7`.

```json
{
  "id": "NFI-031-P2-GAMMA",
  "tag": "PROJECTION",
  "issue": "The hemisphere-derived 0.2/1 branch rule and 018 interpolation to 0.2+0.4min(Vc,2) have not been validated for the complete sphere. Numerical least-set membership is conditional on these bounds.",
  "next_evidence": "Correlate full-shell imperfection-sensitive nonlinear analysis and representative structural testing."
}
```

### N518 — NFI-035-SPHERE-VC

Source `rpt-mainline035-opus-knockdown-tests-1020`; original file `unpublished-local-ref:4d5781abcddc2e1c; pointer `/rows/0`.

```json
{
  "id": "NFI-035-SPHERE-VC",
  "state": "open",
  "note": "The only measured sandwich hemispheres (Saturn S-II, two points, gamma 0.22-0.24 at R/rho about 240) have no recoverable Vc; Gonzalez and Patton's SDL 468, which holds the specimens, was not found. The only sphere data cannot be placed on the Vc axis.",
  "settle": "SDL 468, or an S-II common-bulkhead construction record (faces, core, depth, radius)"
}
```

### N519 — NFI-035-VC-GAP

Source `rpt-mainline035-opus-knockdown-tests-1020`; original file `unpublished-local-ref:4d5781abcddc2e1c; pointer `/rows/1`.

```json
{
  "id": "NFI-035-VC-GAP",
  "state": "open",
  "note": "No measured point at Vc 0.9 to 2 in any shell form. 018's linear rise from 0.2 to 1 across Vc 0 to 2 is untested there; the SBKF cylinders at Vc 0.3-0.5 already sit above it (0.72-0.87), but as cylinders.",
  "settle": "MAINLINE-029's FE at the lead geometry; a sandwich test at Vc about 1"
}
```

### N521 — NFI-035-SBKF-VC

Source `rpt-mainline035-opus-knockdown-tests-1020`; original file `unpublished-local-ref:4d5781abcddc2e1c; pointer `/rows/3`.

```json
{
  "id": "NFI-035-SBKF-VC",
  "state": "computed by this seat",
  "note": "SBKF Vc comes from lamination theory on stated lamina values with a generic G12 of 0.77 Msi and geometric-mean face and core conventions (range shown as bars: axial-face/axial-shear to softer-core). QUESTIONABLE.",
  "settle": "the SBKF laminate stiffness tables, if published"
}
```

### N547 — NFI-036-gamma-wrinkle

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/9`.

```json
{
  "id": "NFI-036-gamma-wrinkle",
  "status": "OPEN",
  "issue": "Retain the unresolved buckling and wrinkling assumptions after adding strength.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "gamma_model": ".2+.4 min(Vc,2) for full endpoint",
    "wrinkle_max": 0.82
  },
  "today": {
    "today_gamma": 0.2,
    "today_wrinkle": 0.33
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "028b; 027; RESULTS today_infinite_strength_screens",
  "closure": "Representative joined-shell imperfection tests and actual face/core wrinkling/bond characterization. High Fcy alone does not close these modes."
}
```

### N556 — 033-NFI-04

Source `rpt-ref-5b1ba7a48fcb57c8e35e`; original file `unpublished-local-ref:6bdf8f2e409f7e2b; pointer `/issues/3`.

```json
{
  "id": "033-NFI-04",
  "tag": "PROJECTION",
  "title": "Gamma/Q transfers and branch convention",
  "finding": "Gamma's smooth full curve and Q=.82 are projected model transfers. The 021b baseline sets gamma=1 in the Vc>=2 crimp branch. Thus Q-plus-strength's 16.282 m crossing does not establish flotation at literal gamma=.20. The requested flat-.20 benchmark is separately negative at every radius.",
  "next_evidence": "Establish shell knockdown and wrinkling behavior for the chosen geometry, seams and measured imperfection distribution.",
  "status": "open"
}
```

### N600 — NFI-017b-VC2-STEP

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/0`.

```json
{
  "id": "NFI-017b-VC2-STEP",
  "tag": "QUESTIONABLE",
  "claim": "Face modulus alone reaches SF 1 only at Vc 2, where CR-1457's gamma steps from 0.20 to 1; the point is a knife edge that re-optimisation cannot hold (the crimp-branch answers re-check at 0.756/0.789).",
  "needed_to_ground": "MAINLINE-029's measured crimp-branch gamma at the lead geometry."
}
```

### N657 — NFI-038-GAMMA_DENOM

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/6`.

```json
{
  "id": "NFI-038-GAMMA_DENOM",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Gamma denominators differ across models and shorthand",
  "evidence": "029 brief versus 021b/028b finite-core convention.",
  "resolution_needed": "Report collapse/reference pressures explicitly; preserve both FE and inherited normalizations.",
  "tests": [
    "T7"
  ]
}
```

### N673 — NFI-C035-SII

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/0`.

```json
{
  "id": "NFI-C035-SII",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "S-II core properties, actual geometry, plasticity and thermal reductions are unresolved.",
  "next_evidence": "Recover Gonzalez/Patton SDL 468 and specimen-level pressures, faces, core shear, imperfections and reduction method; then compute compatible Vc and KDF.",
  "evidence": [
    "E07",
    "DIGITIZATION.json"
  ],
  "blocks_card": false
}
```

### N674 — NFI-C035-BASELINE

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/1`.

```json
{
  "id": "NFI-C035-BASELINE",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "Anisotropic/combined-load SBKF FE ratios are not proven to share the lead sphere's scalar denominator.",
  "next_evidence": "Derive matching anisotropic shell baselines and shear corrections, retaining actual load and boundary conditions; compare with the scalar proxy.",
  "evidence": [
    "E01",
    "E04",
    "E05",
    "METHOD.md"
  ],
  "blocks_card": false
}
```

### N675 — NFI-C035-SCALAR

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/2`.

```json
{
  "id": "NFI-C035-SCALAR",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "Vc depends on scalarization, nominal versus measured thickness and stress-dependent properties.",
  "next_evidence": "Publish nominal, as-built and directional conventions separately; recover measured G12 and effective core shear where possible.",
  "evidence": [
    "E01",
    "E02",
    "SOURCE-CORRECTIONS.json"
  ],
  "blocks_card": false
}
```

### N681 — NFI-C035-YANG

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/8`.

```json
{
  "id": "NFI-C035-YANG",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "The new egg-shaped vessel has plastic collapse and no compatible scalar Vc established.",
  "next_evidence": "Recover effective core shear and local-curvature/denominator definitions; retain its 12.44 MPa physical result without assigning an elastic sphere KDF.",
  "evidence": [
    "E17",
    "AUXILIARY.json"
  ],
  "blocks_card": false
}
```

### N686 — NFI-C035-MUC

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/13`.

```json
{
  "id": "NFI-C035-MUC",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "Muc's 8.49% eigenvalue overprediction is supported, but an effective measured core-shear Vc is not.",
  "next_evidence": "Separate constituent-wall assumptions from homogenized honeycomb shear and recover a specimen-compatible Vc.",
  "evidence": [
    "E14"
  ],
  "blocks_card": false
}
```

### N698 — NFI-036-gamma-wrinkle

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/9`.

```json
{
  "id": "NFI-036-gamma-wrinkle",
  "status": "OPEN",
  "issue": "Retain the unresolved buckling and wrinkling assumptions after adding strength.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "gamma_model": ".2+.4 min(Vc,2) for full endpoint",
    "wrinkle_max": 0.82
  },
  "today": {
    "today_gamma": 0.2,
    "today_wrinkle": 0.33
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "028b; 027; RESULTS today_infinite_strength_screens",
  "closure": "Representative joined-shell imperfection tests and actual face/core wrinkling/bond characterization. High Fcy alone does not close these modes.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### C013 — CHECK033-NFI-04

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/3`.

```json
{
  "id": "CHECK033-NFI-04",
  "inherited_id": "033-NFI-04",
  "tag": "PROJECTION",
  "title": "Gamma/Q transfers and branch convention",
  "finding": "Gamma's smooth full curve and Q=.82 are projected model transfers. The 021b baseline sets gamma=1 in the Vc>=2 crimp branch. Thus Q-plus-strength's 16.282 m crossing does not establish flotation at literal gamma=.20. The requested flat-.20 benchmark is separately negative at every radius.",
  "next_evidence": "Establish shell knockdown and wrinkling behavior for the chosen geometry, seams and measured imperfection distribution.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Retained physical/model limitation. Arithmetic reproduction does not establish an installed-hull allowable."
}
```

### C110 — NFI-029-BENCHMARK

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/0`.

```json
{
  "id": "NFI-029-BENCHMARK",
  "status": "open",
  "title": "Paper benchmark not reproduced",
  "issue": "The CAX8 paper linear result is 30.21717 MPa versus published 27.53 MPa. Full 3D refinement gives 34.34704, 30.80495 and 30.28896 MPa, approaching CAX8 within0.24%; nonaxisymmetric modes at this resolution do not remove the roughly10% discrepancy. Elastic Gaussian-dimple endpoints exceed the published nonlinear pressures by over2x. No calibrated transfer of knockdown is established. The paper uses continuum-shell faces and tie constraints; ours uses conforming solid elements. No isolated cause for the linear discrepancy is claimed. Figure4 and the brief specify42.8mm radius; the conclusion says41.8mm. We use42.8mm and retain the text ambiguity.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C117 — NFI-029-GAMMA

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/7`.

```json
{
  "id": "NFI-029-GAMMA",
  "status": "resolved-by-reporting-both",
  "title": "Gamma denominator mismatch",
  "issue": "Both lead points have Vc<2. Their.595318/.468229 targets multiplyKc*p_classical; p_collapse/p_crimp is a different ratio. For W meridian targets are.464110/.323009 under the requested crimp normalization. No branch transfer from paper Vc~200 is established.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C121 — NFI-029-NUMERICAL-EVIDENCE

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/11`.

```json
{
  "id": "NFI-029-NUMERICAL-EVIDENCE",
  "status": "open",
  "title": "Published pressure results are simulations",
  "issue": "EUCASS367 pressure-collapse values are numerical ABAQUS results. Its physical validation is an axial-compression experiment, not a hydrostatic collapse test. Present solver measurements are not hardware measurements.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C137 — N042-01

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/0`.

```json
{
  "id": "N042-01",
  "issue": "The single-dimple map is not the record",
  "detail": "By 015b's map, the dimples a dome-class build holds (1-5 mm) imply gamma 0.69-0.90, and a reflector-class build (0.15 mm) about 0.95. The only measured large sandwich domes, S-II's, were built with a 0.254 mm core-to-face fit and inflation-faired skins, and reached about 0.21-0.22 (035, CHECK-035). The map transfers to a sandwich at Vc 0.95 only through t_eq (015b NFI-015B-SANDWICH).",
  "to_close": "A built sandwich shell with measured shape and measured knockdown: 038 T7, or a subscale shell built by this route.",
  "tag": "PROJECTION"
}
```

### C168 — 040-06-gamma

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/5`.

```json
{
  "id": "040-06-gamma",
  "tag": "PROJECTION",
  "open_issue": "The effective global coefficient and Vc branch convention lack whole-hull imperfection validation.",
  "grounding": "Use measured imperfections, orthotropic shell analysis and correlated physical buckling tests."
}
```

### C242 — NFI-044-BUCKLING-DEGRADATION

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/18`.

```json
{
  "id": "NFI-044-BUCKLING-DEGRADATION",
  "finding": "S-N damage does not quantify evolving waviness, debond-induced buckling, impact damage, or nonlinear aerodynamic/local bending stresses. Static projected gamma is not a life property.",
  "evidence_needed": "Cycled curved-panel and shell stability tests, validated imperfection growth and a combined-load nonlinear structural model."
}
```

### S001 — NFI-030C-GAMMA-GEOMETRY

Source `rpt-1228-mainline030c-design-register-1020`; original file `unpublished-local-ref:3c01fd6db28be861; pointer `/rows/0`.

```json
{
  "id": "NFI-030C-GAMMA-GEOMETRY",
  "title": "029 is adverse numerical evidence at 021/021b, not a solved 028b/037b hull.",
  "finding": "Weak-meridian endpoints at 11.8/46 mm are below operating pressure. The working shape target must be tighter than those 015 amplitudes within that model. Benchmark and collapse validation are absent; no quantitative physical tolerance or current joined-hull SF is established.",
  "status": "OPEN",
  "blocks_progress": false,
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## R008 — core Ec (stabilised datasheet value) transferred into the wrinkling formula

**Original question:** Plascore PAMG-XR1 5052 prints no stabilised compressive modulus and no crush column; Ec is transferred from Hexcel CR-III 5052; crush is Plascore bare, not the Hexcel crush-column test.

### N032 — NFI-WRINKLE

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-WRINKLE",
  "gap": "The wrinkling target uses the advisory one-half cube-root formula. The equal Ec and Gc square root is not used as a result.",
  "direction": "MAINLINE-007b cites a sourced wrinkling formula and keeps Ec and Gc separate.",
  "effect": "Catalog foams and aramid honeycomb miss this product by about 40 to 180 times. Aluminium honeycomb has no retrieved Ec, so its product is open."
}
```

### N042 — NFI-WRINKLE

Source `rpt-ref-3dd5ab5528276031581d`; original file `unpublished-local-ref:474808f25f6dc0cd; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-WRINKLE",
  "gap": "Foam wrinkling uses equation 2.2-5 with Q 0.50 and the flat-plate equibiaxial interaction 2.2-6. The stress safety factor becomes 0.709062069568 of the advisory uniaxial stress factor. Honeycomb uses equation 2.2-14.",
  "direction": "Plascore has no Ec, so its wrinkling stress is still open. The Hexcel stabilised modulus is QUESTIONABLE as Ec.",
  "effect": "Foam wrinkling stays above the trimmed general-instability factor. Hexcel equibiaxial wrinkling safety factors are 0.0565286364026 and 0.0415196459641, below general instability, so that local mode would govern if it is admitted."
}
```

### N139 — NFI-008B-WRINKLE-FORMULA

Source `rpt-ref-cc9cef5e55adca018a8f`; original file `unpublished-local-ref:2bbb739a4c037482; pointer `retained original identity`.

```json
{
  "id": "NFI-008B-WRINKLE-FORMULA",
  "issue": "The wrinkling criterion sigma_wr = 0.5*(E_f*Ec*Gc)^(1/3) is the flat-panel/dimple formula transferred to a 10 m radius sandwich sphere. Orthotropic honeycomb has no single continuum Ec; the two HexWeb sheets carry no compressive modulus on their datasheets, so their Ec*Gc products stay open (007). Foam products (ROHACELL, Divinycell) are datasheet-derived and QUESTIONABLE.",
  "consequence": "The wrinkling column measures a product gap, not a verified failure mode. MAINLINE-007b is sourced to replace this reading.",
  "next": "007b's sourced sandwich-shell shear and wrinkling formulas supersede this column when filed."
}
```

### N265 — NFI-WRINKLE

Source `rpt-mainline003-grok-p2-targets-1019`; original file `unpublished-local-ref:c644022670e558c3; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-WRINKLE",
  "gap": "The wrinkling target uses the advisory one-half cube-root formula and an equal Ec and Gc split.",
  "direction": "Separate Ec and Gc from a datasheet.",
  "effect": "The reported product is the quantity fixed by the formula. The square root is only the equal-split assumption."
}
```

### N296 — NFI-SAND/SHEAR/WRINKLE/CRUSH

Source `rpt-mainline007-check-lead4f19-1019`; original file `unpublished-local-ref:a0b67c87ff180a29; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SAND/SHEAR/WRINKLE/CRUSH",
  "gap": "Confirmed: stated SF omits core shear, face wrinkling and core crush; advisory crimp (Gc = pR/(2*sep)), wrinkling product ((2*membrane)^3/E) and crush (p/2, QUESTIONABLE, not an equilibrium solution) are beside the row. Catalog cores at 16-38 kg/m3 clear advisory crush and crimp; wrinkling products miss by roughly 40-180x; aluminium honeycomb Ec is open.",
  "direction": "007b, checked separately.",
  "effect": "Owner statement stands."
}
```

### N325 — NFI-ALHC

Source `rpt-mainline014-grok-balanced-sandwich-1019`; original file `unpublished-local-ref:8c5f980fe25f9829; pointer `retained original identity`.

```json
{
  "id": "NFI-ALHC",
  "note": "Both Plascore aluminium honeycombs lack Ec. Wrinkling is unscored, so they are excluded from the optimum."
}
```

### N336 — NFI-PLASCORE-EC

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-PLASCORE-EC",
  "note": "Plascore PAMG-XR1 5052 prints bare compression and L/W plate shear. It prints no stabilised compressive modulus and no crush column. Ec is the Hexcel CR-III 5052 stabilised modulus at the same cell and nominal pcf. Crush is Plascore's bare compressive typical, which is the 1.29 MPa the brief names at 3/16-2.0. That bare value is not the Hexcel crush-column test."
}
```

### N339 — NFI-HRH36

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-HRH36",
  "note": "HRH-36 para-aramid in the attributes brochure has no stabilised compressive modulus. It is not scored. HDC has strengths only. HFT 3/8-4.0 has no stabilised modulus. Preliminary and beam-shear rows were not scored."
}
```

### N608 — NFI-017b-CORE-EC

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/8`.

```json
{
  "id": "NFI-017b-CORE-EC",
  "tag": "QUESTIONABLE",
  "claim": "With beryllium and handbook values kept, the core needs through-thickness stiffness per density of 41-57 MPa per kg/m3, beyond aluminium's 24.8; no carbon-honeycomb compressive modulus was sourced, and the Ultracor shear value is secondary (a 2023 paper quoting 2012).",
  "needed_to_ground": "A primary carbon-honeycomb datasheet with stabilised compressive modulus."
}
```

## R009 — equibiaxial wrinkling interaction factor (0.682) on a curved face

**Original question:** The flat-plate interaction is applied to equibiaxial membrane stress of a sphere; a sphere-specific interaction could replace it.

### N047 — NFI-BIAX

Source `rpt-ref-3dd5ab5528276031581d`; original file `unpublished-local-ref:474808f25f6dc0cd; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-BIAX",
  "gap": "Equation 2.2-6 is a flat-plate interaction applied here to equibiaxial membrane stress. The handbook cites it for biaxial compression of facings.",
  "direction": "A sphere-specific wrinkling interaction could replace it.",
  "effect": "The equibiaxial factor solved from R^3 + R = 1 is 0.682327803828."
}
```

### N055 — NFI-WRINKLE-BIAX

Source `rpt-ref-d5b4aaa267b71d82fe25`; original file `unpublished-local-ref:1d727f2cb127351c; pointer `retained original identity`.

```json
{
  "id": "NFI-WRINKLE-BIAX",
  "value": "equibiaxial factor on the flat-plate interaction Rx^3+Ry=1",
  "optimistic": 0.23516798404427022,
  "factor_formula": "constant 0.682327803828, already inside the stated wrinkling safety factor",
  "conservative": "the same interaction",
  "direction": "A sphere-face wrinkling test. The interaction is a flat-plate equation."
}
```

### N305 — NFI-BIAX

Source `rpt-mainline007b-check-lead4f19-1019`; original file `unpublished-local-ref:c88bee0b56cece84; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-BIAX",
  "gap": "Confirmed: Eq 2.2-6 is a flat-plate interaction applied to equibiaxial membrane stress; the solved factor is 0.6823278038280193.",
  "direction": "A sphere-specific wrinkling interaction could replace it.",
  "effect": "Owner statement stands."
}
```

### N451 — biaxial-on-a-shell

Source `rpt-mainline032-grok-wrinkle-waviness-1020`; original file `unpublished-local-ref:e20bd8d3e1ca97e2; pointer `/open/5`.

```json
{
  "id": "biaxial-on-a-shell",
  "tag": "QUESTIONABLE",
  "note": "Equation 2.2-15 is recommended for biaxial compression. The foam section bases its interaction on flat plates of large aspect ratio. The honeycomb page does not show a biaxial waviness test. The hull radius is 10 m."
}
```

### N534 — NFI-032-CHECK-BIAXIAL-TRANSFER

Source `rpt-ref-a30a669ed3e245f1473b`; original file `unpublished-local-ref:46e93c1ee5674acc; pointer `/findings/6`.

```json
{
  "id": "NFI-032-CHECK-BIAXIAL-TRANSFER",
  "status": "open",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "b=0.6823 is applied to the uniaxial stress containing waviness.",
  "checked": "The algebra is correct for equal directional uniaxial capacities and does not count waviness twice. The handbook's flat-plate rule alone does not validate the loaded curved Be sandwich or establish equal directional capacity.",
  "followup": "Retain the algebraic result and QUESTIONABLE transfer; validate the actual biaxial construction and relevant directional capacities.",
  "source_audit_ids": [
    "NASA-BIAXIAL"
  ],
  "owner_nfi_ids": [
    "biaxial-on-a-shell"
  ]
}
```

### N631 — NFI-032-CHECK-BIAXIAL-TRANSFER

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/prior_032_findings_retained/6`.

```json
{
  "id": "NFI-032-CHECK-BIAXIAL-TRANSFER",
  "status": "open",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "b=0.6823 is applied to the uniaxial stress containing waviness.",
  "checked": "The algebra is correct for equal directional uniaxial capacities and does not count waviness twice. The handbook's flat-plate rule alone does not validate the loaded curved Be sandwich or establish equal directional capacity.",
  "followup": "Retain the algebraic result and QUESTIONABLE transfer; validate the actual biaxial construction and relevant directional capacities.",
  "source_audit_ids": [
    "NASA-BIAXIAL"
  ],
  "owner_nfi_ids": [
    "biaxial-on-a-shell"
  ]
}
```

### N654 — NFI-038-BAXIAL

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/3`.

```json
{
  "id": "NFI-038-BAXIAL",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Uniaxial tests may censor the required wrinkle evidence",
  "evidence": "Current equal-biaxial threshold needs approximately 440 MPa uniaxial wrinkle onset if inherited b applies.",
  "resolution_needed": "Separate face yield from wrinkles; test equal-biaxial panel and actual orthotropy.",
  "tests": [
    "T1",
    "T3"
  ]
}
```

## R010 — honeycomb wrinkling coefficient 0.33 (design) vs 0.82 (theoretical) (O2)

**Current 030c:** Selected 028b+037b 200 F/30.3414:1 point requires Q=.439513 (1.331859× .33); no matched Be/core/bond wrinkle-band evidence. Prior .434628 belongs to the no-residual 028b point.

**030b source history:** 028b nominal R10 needs Q=.434628 (1.317054× .33). 033 screened R20/R30 need .517583/.539762. 032's checked inverse relates these to a wavelength-specific amplitude conditional on the weaker of core/bond flatwise capacities; 032b's aluminium precedents are not Be-hull qualification.

**Original question:** Foam wrinkling gives 0.709 of advisory uniaxial SF; Hexcel honeycomb wrinkling (0.0565, 0.0415) falls below general instability and would govern if admitted; Plascore Ec open, Hexcel stabilised Ec questionable.

### N014 — NFI-WRINKLE-GC-TEXT

Source `rpt-1228-mainline014b-independent-check-1019`; original file `unpublished-local-ref:8f2d079b76102928; pointer `retained original identity`.

```json
{
  "id": "NFI-WRINKLE-GC-TEXT",
  "type": "text_mismatch",
  "row": "NFI-W-SHEAR",
  "field": "note",
  "reported": "Crimping and honeycomb wrinkling use that Gc.",
  "independent": "The selected honeycomb wrinkling equation has no Gc; crimping and global buckling do.",
  "proposed_fix": "Correct the explanatory sentence; numerical values already use the stated honeycomb formula.",
  "stops_owner": false
}
```

### N167 — NFI-013-WRINKLE-LEVEL

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-WRINKLE-LEVEL",
  "issue": "The wrinkling-precision gap, carried as 009 and 014 carry it: design coefficients (continuum 0.50, CR-1457 eq 2.2-5; honeycomb 0.33, eq 2.2-14) against classical ones (0.76, NASA/CR-1999-208994 Table 3; 0.82, eq 2.2-12).",
  "numbers": "The product need falls to 0.285 at 0.76 (a factor 3.51); the honeycomb Ec need falls to 0.162 at 0.82 (6.17). No verdict in this card moves.",
  "closes_when": "a representative wrinkling test fixes the coefficient for the chosen face and core."
}
```

### N194 — NFI-021-WRINKLE

Source `rpt-ref-769a7442efd5a04681e9`; original file `unpublished-local-ref:63c049a0d93b9857; pointer `retained original identity`.

```json
{
  "id": "NFI-021-WRINKLE",
  "optimism": "O2",
  "needed": 0.37068071372338524,
  "today": 0.33,
  "improvement_factor": 1.1232748900708642,
  "usage_of_named_stretch": 0.1277158154673571,
  "state": "between today's design lower bound (0.33) and the classical value (0.82); no test at this core-to-face ratio",
  "grounding_card": "none pending; a wrinkling test on a representative sandwich",
  "note": "core-to-face ratio tc/tf 23.97"
}
```

### N204 — NFI-021b-WRINKLE

Source `rpt-ref-1080d4f6a1af4cfa8c67`; original file `unpublished-local-ref:4edbd73193c8c843; pointer `retained original identity`.

```json
{
  "id": "NFI-021b-WRINKLE",
  "optimism": "O2",
  "needed": 0.6092014443376216,
  "today": 0.33,
  "full": 0.82,
  "improvement_factor": 1.8460649828412774,
  "usage": 0.6735316047895863,
  "state": "between the design lower bound and the classical value; no test at this tc/tf",
  "grounding_card": "none pending"
}
```

### N300 — NFI-WRINKLE

Source `rpt-mainline007b-check-lead4f19-1019`; original file `unpublished-local-ref:c88bee0b56cece84; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-WRINKLE",
  "gap": "Confirmed: foam wrinkling (Eq 2.2-5, Q 0.50, equibiaxial factor 0.6823278038280193 from x^3+x=1) gives 0.7090620695678252 of the advisory uniaxial SF and stays above trimmed general instability. Hexcel honeycomb wrinkling (Eq 2.2-14) gives 0.05652863640260287 and 0.0415196459641, below general instability, so it would govern if admitted. Plascore Ec is open; Hexcel stabilised Ec is QUESTIONABLE.",
  "direction": "Owner directions stand.",
  "effect": "Owner statement stands."
}
```

### N329 — NFI-WRINKLE-Q

Source `rpt-mainline014-grok-balanced-sandwich-1019`; original file `unpublished-local-ref:8c5f980fe25f9829; pointer `retained original identity`.

```json
{
  "id": "NFI-WRINKLE-Q",
  "note": "Wrinkling-precision gap. Foam design coefficient 0.50, theoretical column 0.82 inside the sourced band Allen 0.78, Plantema 0.85, Hoff and Mautner 0.91. Required Ec*Gc scales as 1/coefficient^3: (0.82/0.50)^3 = 4.410943999999999. Honeycomb design coefficient 0.33 from CR-1457 eq 2.2-14. Honeycomb theoretical coefficient 0.82 from Hemp, as quoted for anti-plane cores in NASA/CR-1999-208994. QUESTIONABLE. The column is the same geometry, not a new optimum."
}
```

### N343 — NFI-WRINKLE-Q

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-WRINKLE-Q",
  "note": "Honeycomb design coefficient 0.33 is CR-1457 eq 2.2-14. Theoretical 0.82 is Hemp's symmetric anti-plane value, quoted as purely theoretical for honeycomb in NASA/CR-1999-208994. Foam design 0.50 and theoretical 0.82 are the 014 column, kept for the foam cores that remain in the set. The theoretical column is the same geometry, not a new grid."
}
```

### N351 — NFI-017-WRINKLE-COEFF

Source `rpt-mainline017-improvement-directions-lead4f19-1019`; original file `unpublished-local-ref:b586b896a14aa878; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-017-WRINKLE-COEFF",
  "gap": "The CNT wrinkling-coefficient requirement (0.600) lies inside the sourced theoretical band 0.78-0.91, above the design 0.33. It is a coefficient the card is scored with, not a measured property of this sphere.",
  "direction": "A sphere-specific wrinkling test or interaction to replace the flat-plate equibiaxial factor.",
  "effect": "First direction by availability, seventh by factor."
}
```

### N425 — NFI-028b-af015_scarf-wrinkle

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/1`.

```json
{
  "id": "NFI-028b-af015_scarf-wrinkle",
  "status": "OPEN",
  "issue": "Ground wrinkling coefficient with the actual core and bond.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": 0.43462785437520957,
  "today": 0.33,
  "improvement_factor": 1.3170541041673016,
  "null_factor_reason": null,
  "source": "Inherited CR-1457 bounds",
  "usage": 0.30256423597576293,
  "full": 0.82
}
```

### N427 — NFI-028b-af015_scarf_primer5-wrinkle

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/3`.

```json
{
  "id": "NFI-028b-af015_scarf_primer5-wrinkle",
  "status": "OPEN",
  "issue": "Ground wrinkling coefficient with the actual core and bond.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": 0.42895155156547243,
  "today": 0.33,
  "improvement_factor": 1.2998531865620375,
  "null_factor_reason": null,
  "source": "Inherited CR-1457 bounds",
  "usage": 0.288121245604928,
  "full": 0.82
}
```

### N429 — NFI-028b-lab8_eb_eta1-wrinkle

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/5`.

```json
{
  "id": "NFI-028b-lab8_eb_eta1-wrinkle",
  "status": "OPEN",
  "issue": "Ground wrinkling coefficient with the actual core and bond.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": 0.5970894471618662,
  "today": 0.33,
  "improvement_factor": 1.809361961096564,
  "null_factor_reason": null,
  "source": "Inherited CR-1457 bounds",
  "usage": 0.6514685371580532,
  "full": 0.82
}
```

### N431 — NFI-028b-lab8_scarf-wrinkle

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/7`.

```json
{
  "id": "NFI-028b-lab8_scarf-wrinkle",
  "status": "OPEN",
  "issue": "Ground wrinkling coefficient with the actual core and bond.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": 0.4379873839250472,
  "today": 0.33,
  "improvement_factor": 1.3272344967425673,
  "null_factor_reason": null,
  "source": "Inherited CR-1457 bounds",
  "usage": 0.31102374985315945,
  "full": 0.82
}
```

### N446 — fc-is-the-lower-of-three

Source `rpt-mainline032-grok-wrinkle-waviness-1020`; original file `unpublished-local-ref:e20bd8d3e1ca97e2; pointer `/open/0`.

```json
{
  "id": "fc-is-the-lower-of-three",
  "tag": "QUESTIONABLE",
  "note": "Fc is the lower of flatwise compression, flatwise tension and the face-to-core bond. The sheet prints stabilised compression, 60 psi typical and 35 psi minimum. It does not print flatwise tension or a beryllium bond. A weaker bond lowers the allowed amplitude in proportion. The crush column, 35 psi, is not that peak."
}
```

### N452 — design-0-33-is-not-a-measured-wave

Source `rpt-mainline032-grok-wrinkle-waviness-1020`; original file `unpublished-local-ref:e20bd8d3e1ca97e2; pointer `/open/6`.

```json
{
  "id": "design-0-33-is-not-a-measured-wave",
  "tag": "PROJECTION",
  "note": "Inverting equation 2.2-12 at Q 0.33 is stored so the design value can be seen as an amplitude. The handbook selected 0.33 from a test plot."
}
```

### N490 — NFI-031-WRINKLE-CORE

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/8`.

```json
{
  "id": "NFI-031-WRINKLE-CORE",
  "tag": "QUESTIONABLE",
  "issue": "Wrinkle coefficients between 0.33 and 0.82 and published typical core properties are used for a curved sandwich. The catalogue includes transferred moduli and scaled cores; the winner is the sourced light 5056 core, but no assembly allowable exists.",
  "next_evidence": "Test curvature, cell depth, orthotropy, face/core bond and biaxial wrinkling/crimp/crush/dimpling at service temperature."
}
```

### N528 — NFI-032-CHECK-FC

Source `rpt-ref-a30a669ed3e245f1473b`; original file `unpublished-local-ref:46e93c1ee5674acc; pointer `/findings/0`.

```json
{
  "id": "NFI-032-CHECK-FC",
  "status": "qualification",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "60 psi typical and 35 psi stabilized compression are used as Fc scenarios.",
  "checked": "The correct Fc is min(compression, core tension, facing-core bond). Neither scenario establishes the bonded sandwich value. Typical crush 35 psi happens to equal minimum-average stabilized compression numerically, but represents a different property.",
  "followup": "Preserve the conditional labels; supply matching core tensile and Be-bond flatwise data before converting the scenario into an allowable.",
  "source_audit_ids": [
    "NASA-FC",
    "HEXCEL-5056"
  ],
  "owner_nfi_ids": [
    "fc-is-the-lower-of-three"
  ]
}
```

### N535 — NFI-032-CHECK-DESIGN033

Source `rpt-ref-a30a669ed3e245f1473b`; original file `unpublished-local-ref:46e93c1ee5674acc; pointer `/findings/7`.

```json
{
  "id": "NFI-032-CHECK-DESIGN033",
  "status": "projection",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "PROJECTION",
  "reported": "The 0.33 design coefficient is inverted as an illustrative wave amplitude.",
  "checked": "The arithmetic is correct but this is not a measured defect distribution or proof of why the empirical knockdown has that value. The owner already tags these rows PROJECTION.",
  "followup": "Keep the existing projection label and source-test limitations.",
  "source_audit_ids": [
    "NASA-DESIGN033"
  ],
  "owner_nfi_ids": [
    "design-0-33-is-not-a-measured-wave"
  ]
}
```

### N537 — NFI-032-CHECK-ROUNDED-TARGET

Source `rpt-ref-a30a669ed3e245f1473b`; original file `unpublished-local-ref:46e93c1ee5674acc; pointer `/findings/9`.

```json
{
  "id": "NFI-032-CHECK-ROUNDED-TARGET",
  "status": "qualification",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "The specified brief rounds both geometry and required Q; many decimal digits are displayed.",
  "checked": "Using the full pinned 021/021b geometry and required Q gives conditional 60 psi amplitudes 0.15313481918912647 and 0.06513526466329604 mm. The brief-based rows differ by -0.1737373278% and +0.1345534421%, respectively. This is intentional input precision, not an error in the requested calculation.",
  "followup": "Use the full-input supplemental rows when interpreting the precise upstream SF=1 threshold; do not interpret decimal output as metrological accuracy.",
  "source_audit_ids": [],
  "owner_nfi_ids": [],
  "exact_values": {
    "Be S-200F": {
      "tf_m": 0.0008434480441930918,
      "tc_m": 0.02021337638749162,
      "Q_needed": 0.37068071372338524,
      "Q_needed_from_membrane_stress": 0.37068071372338524,
      "pressure_Pa": 95460.83791390515,
      "radius_m": 10.0,
      "stress_Pa": 282948186.8240931,
      "intracell_uniaxial_critical_Pa": 5103736594.681676,
      "intracell_equibiaxial_factor": 0.5,
      "intracell_critical_Pa": 2551868297.340838,
      "intracell_SF": 9.018853684781929,
      "actual_input_amplitude_60psi": {
        "Q": 0.37068071372338524,
        "is_that_leads_Q": true,
        "delta_m": 0.00015313481918912647,
        "delta_mm": 0.15313481918912647,
        "delta_over_tf": 0.1815580938783576,
        "delta_over_cell_3_8_in": 0.016077146371561837,
        "delta_over_card_9_5_mm": 0.016119454651486998,
        "delta_over_tc": 0.007575914891877682,
        "K_delta": 1.8939787229694207
      },
      "brief_amplitude_60psi": {
        "Q": 0.371,
        "is_that_leads_Q": true,
        "delta_m": 0.00015286876684636114,
        "delta_mm": 0.15286876684636114,
        "delta_over_tf": 0.18125298416689725,
        "delta_over_cell_3_8_in": 0.01604921436707204,
        "delta_over_card_9_5_mm": 0.016091449141722225,
        "delta_over_tc": 0.007564016172506737,
        "K_delta": 1.8910040431266844
      },
      "brief_minus_actual_amplitude_mm": -0.00026605234276533274,
      "brief_over_actual_minus_one_percent": -0.17373732778352968
    },
    "SR-200": {
      "tf_m": 0.0006917479988347394,
      "tc_m": 0.030118230884842855,
      "Q_needed": 0.6092014443376216,
      "Q_needed_from_membrane_stress": 0.6092014443376215,
      "pressure_Pa": 95460.83791390515,
      "radius_m": 10.0,
      "stress_Pa": 344998605.25332373,
      "intracell_uniaxial_critical_Pa": 3432949414.9782996,
      "intracell_equibiaxial_factor": 0.5,
      "intracell_critical_Pa": 1716474707.4891498,
      "intracell_SF": 4.975309121115971,
      "actual_input_amplitude_60psi": {
        "Q": 0.6092014443376216,
        "is_that_leads_Q": true,
        "delta_m": 6.513526466329605e-05,
        "delta_mm": 0.06513526466329604,
        "delta_over_tf": 0.0941603947868551,
        "delta_over_cell_3_8_in": 0.006838347996146567,
        "delta_over_card_9_5_mm": 0.006856343648768005,
        "delta_over_tc": 0.002162652411834577,
        "K_delta": 0.5406631029586443
      },
      "brief_amplitude_60psi": {
        "Q": 0.609,
        "is_that_leads_Q": true,
        "delta_m": 6.522290640394087e-05,
        "delta_mm": 0.06522290640394086,
        "delta_over_tf": 0.09429363366190671,
        "delta_over_cell_3_8_in": 0.006847549228760197,
        "delta_over_card_9_5_mm": 0.006865569095151671,
        "delta_over_tc": 0.00216543513957307,
        "K_delta": 0.5413587848932675
      },
      "brief_minus_actual_amplitude_mm": 8.764174064482266e-05,
      "brief_over_actual_minus_one_percent": 0.13455344212980336
    }
  }
}
```

### N632 — NFI-032-CHECK-DESIGN033

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/prior_032_findings_retained/7`.

```json
{
  "id": "NFI-032-CHECK-DESIGN033",
  "status": "projection",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "PROJECTION",
  "reported": "The 0.33 design coefficient is inverted as an illustrative wave amplitude.",
  "checked": "The arithmetic is correct but this is not a measured defect distribution or proof of why the empirical knockdown has that value. The owner already tags these rows PROJECTION.",
  "followup": "Keep the existing projection label and source-test limitations.",
  "source_audit_ids": [
    "NASA-DESIGN033"
  ],
  "owner_nfi_ids": [
    "design-0-33-is-not-a-measured-wave"
  ]
}
```

### C169 — 040-07-wrinkling_Q

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/6`.

```json
{
  "id": "040-07-wrinkling_Q",
  "tag": "PROJECTION",
  "open_issue": "Q=.33–.82 is a selectable model factor rather than a qualified lower-bound allowable.",
  "grounding": "Correlate matched sandwich wrinkle specimens across relevant wavelengths and defects."
}
```

## R011 — intracell dimpling: biaxial vs uniaxial rule and coefficient

**Original question:** Intracell dimpling uses the brief stress 2*E_f/(1-nu^2)*(tf/s_cell)^2 with nominal cell size, no equibiaxial factor; foam is not dimpled; the coefficient 2 is the brief expression.

### N200 — NFI-021-DIMPLING-FORM

Source `rpt-ref-769a7442efd5a04681e9`; original file `unpublished-local-ref:63c049a0d93b9857; pointer `retained original identity`.

```json
{
  "id": "NFI-021-DIMPLING-FORM",
  "issue": "Dimpling here uses CR-1457 eq 2.1-6 (biaxial, half); 009d and 014b use the uniaxial eq 2.1-4.",
  "numbers": "Floating point 9.019 biaxial, 18.04 uniaxial; both far above 1."
}
```

### N342 — NFI-DIMPLE

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-DIMPLE",
  "note": "Intracell dimpling uses the brief's stress 2*E_f/(1-nu^2)*(tf/s_cell)^2, divided by the same membrane stress as wrinkling. No equibiaxial factor is applied. Cell size is the sheet nominal. Foam is not dimpled. The coefficient 2 is the brief's expression."
}
```

### N659 — NFI-038-CELL_SCALE

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/8`.

```json
{
  "id": "NFI-038-CELL_SCALE",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Stock honeycomb cells do not scale with a miniature shell",
  "evidence": "At R=.5m exact cellular similarity requires .47625mm cells.",
  "resolution_needed": "Use custom cells or identify continuous-core model scope; separately validate real honeycomb local modes.",
  "tests": [
    "T3",
    "T7"
  ]
}
```

## R012 — laminate bending stiffness in wrinkling

**Original question:** Composite faces use an inherited scalar quasi-isotropic modulus in the wrinkling formula; laminate bending stiffness (layup) is not supplied.

### N015 — NFI-LAMINATE-BENDING

Source `rpt-1228-mainline014b-independent-check-1019`; original file `unpublished-local-ref:8f2d079b76102928; pointer `retained original identity`.

```json
{
  "id": "NFI-LAMINATE-BENDING",
  "type": "model_assumption",
  "row": "composite faces",
  "field": "wrinkling_modulus",
  "reported": "Inherited scalar quasi-isotropic face modulus",
  "independent": "Laminate bending stiffness is not supplied; NASA/CR-1999-208994 after Eq.17 calls for bending stiffness.",
  "source_url": "https://ntrs.nasa.gov/api/citations/19990017863/downloads/19990017863.pdf",
  "proposed_fix": "Retain QUESTIONABLE and supply a layup/bending-stiffness sensitivity in a later fix card.",
  "stops_owner": false
}
```

## R013 — Be face compressive allowable by grade, form and source: 241 / 255 / 283 / 345 / 379 MPa (O3)

**030b source history:** 036/CHECK-036 find no qualified finished thin-sheet compressive minimum. All4945 independent comparisons reproduce. Current selected scarf points demand about300.333MPa;345MPa remains tensile proxy. Historical1.96mm379.2MPa is confirmed but not a thin-sheet allowable. Reoptimized381.612–381.639MPa R20 requirements belong to older027 splice/sheet-elastic models, not033 scarf redesign.

**Original question:** Face compression is exactly 1 on the SR-200 minimum tensile yield used as compressive; no compressive minimum is published, and gauge tolerance or post-form properties can take it below 1.

### N002 — NFI-STRENGTH-EDITION

Source `rpt-1228-mainline009c5-independent-check-1019`; original file `unpublished-local-ref:52f757339520e0fd; pointer `retained original identity`.

```json
{
  "id": "NFI-STRENGTH-EDITION",
  "type": "source_version_conflict",
  "row": "Beryllium S-200F",
  "field": "compressive_yield_MPa",
  "reported": 283,
  "current_guide_value_approx": 255,
  "source_url": "https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74",
  "page": 4,
  "proposed_fix": "Pin the exact older MB-001 edition supporting 283 MPa and reconcile the newer guide. Current computations retain the frozen strength; 37/41 sensitivity is arithmetically correct.",
  "stops_owner": false
}
```

### N013 — NFI-STRENGTH-EDITION

Source `rpt-1228-mainline014b-independent-check-1019`; original file `unpublished-local-ref:8f2d079b76102928; pointer `retained original identity`.

```json
{
  "id": "NFI-STRENGTH-EDITION",
  "type": "source_version_conflict",
  "row": "Beryllium S-200F",
  "field": "compressive_yield_MPa",
  "reported": 283,
  "current_guide_value_approx": 255,
  "source_url": "https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74",
  "page": 4,
  "proposed_fix": "Pin the exact older MB-001 edition supporting 283 MPa and reconcile the newer guide. Current computations retain the frozen strength; 37/41 sensitivity is arithmetically correct.",
  "stops_owner": false
}
```

### N104 — NFI-027-BE-GRADE

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-BE-GRADE",
  "tag": "QUESTIONABLE",
  "issue": "S-200F E = 290 GPa and inherited compression 283 MPa are the design screen. Full 021 transfers a historical SR-200 lot's 379.2 MPa and lower in-plane E = 293.6 GPa. Current SR-200 sheet lists E = 290 GPa and tensile minimum 345 MPa, not a guaranteed compression allowable. Nu 0.33 remains inherited.",
  "next_evidence": "Obtain lot-, gauge-, direction- and post-form compression/stiffness/Poisson data. Keep these mechanical optimism choices separate from weather optimism."
}
```

### N120 — NFI-CHECK021-STRENGTH-FORM

Source `rpt-ref-e92af61311c9bf4a89cd`; original file `unpublished-local-ref:e3324087b91fd866; pointer `retained original identity`.

```json
{
  "id": "NFI-CHECK021-STRENGTH-FORM",
  "category": "source applicability",
  "status": "OPEN",
  "row": "No strength optimism / sheet at guaranteed minimum",
  "field": "compressive yield and product form",
  "card_value": {
    "S200F_Pa": 283000000,
    "SR200_minimum_transferred_to_compression_Pa": 345000000
  },
  "check_value": {
    "current_guide_S200F_about_Pa": 255000000,
    "main_minimum_required_Pa": 282948186.8240931,
    "factor_needed_over_255MPa": 1.1096007326435025,
    "SR200_datasheet_minimum_tensile_Pa": 345000000,
    "SR200_guaranteed_compressive_minimum": null,
    "historical_sheet_compression_to_tension_ratios": [
      0.9890453834115807,
      0.9911939911939911
    ]
  },
  "source": [
    "https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74",
    "https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6",
    "https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf"
  ],
  "tag": "QUESTIONABLE",
  "effect": "No strength optimism is true only relative to the inherited 283-MPa starting value. The current guide's S-200F value does not support that point without an uplift. The 345-MPa sheet number is tensile; equality in compression is an additional transfer assumption.",
  "product_form": "The S-200F datasheet offers SR-200 sheet and PS-200 foil as additional options below 6.3 mm; it does not establish an exclusive mandatory substitution. SR-200 below 0.059 inch is available only at smaller sheet dimensions. The datasheet's parenthetic 0.059 inch = 0.5 mm is internally inconsistent (0.059 inch = 1.4986 mm).",
  "disposition": "Confirms and sharpens the owner's existing Be-strength/sheet-size NFI; does not stop the estimate.",
  "proposed_fix": "Use a matched product/lot/thickness compression value; keep the tensile-to-compressive transfer explicit. MAINLINE-020 is the named grounding card."
}
```

### N121 — NFI-CHECK021-STRONGEST-SCOPE

Source `rpt-ref-e92af61311c9bf4a89cd`; original file `unpublished-local-ref:e3324087b91fd866; pointer `retained original identity`.

```json
{
  "id": "NFI-CHECK021-STRONGEST-SCOPE",
  "category": "source-claim scope",
  "status": "OPEN",
  "row": "Strongest sourced beryllium",
  "field": "scope of 379.2 MPa assertion",
  "card_value": "379.2 MPa as strongest sourced Be",
  "check_value": {
    "supported_sheet_value_Pa": 379200000,
    "other_sourced_tube_values_Pa": {
      "type_A": 450000000,
      "type_PS_1.016mm_wall": 544000000
    }
  },
  "source": [
    "https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf",
    "https://ntrs.nasa.gov/api/citations/19680027581/downloads/19680027581.pdf"
  ],
  "location": "CR-194164 Table 3; TN D-4833 Table VIII, PDF page 35",
  "tag": "QUESTIONABLE lot/product-form observations",
  "effect": "379.2 MPa is supported for the cited sheet directions, but is not the largest compressive value in the source collection. The larger numbers are tube results, not qualified sphere faces.",
  "proposed_fix": "Narrow the wording to strongest applicable sheet value among the opened sheet sources. A tube-to-sheet transfer, if pursued, is a separate PROJECTION."
}
```

### N187 — NFI-020-GRADE-ORIENTATION-COMPRESSION

Source `rpt-ref-3e02218a03708a878faa`; original file `unpublished-local-ref:3fe2376964ec428a; pointer `retained original identity`.

```json
{
  "id": "NFI-020-GRADE-ORIENTATION-COMPRESSION",
  "rank": 3,
  "tag": "QUESTIONABLE",
  "claim": "S200F bulk properties are not an established rolled SR200, formed and joined, biaxial compression basis.",
  "optimistic": {
    "inherited_E_GPa": 303,
    "inherited_compression_MPa": 283,
    "orientation_retention": 1.0,
    "SR200_tensile_elongation_percent_in_1inch": 10
  },
  "conservative": {
    "current_E_GPa": 290,
    "assumed_compression_proxy_MPa": 241,
    "bulk_tensile_elongation_percent": 2,
    "assumed_E_retention": 0.8,
    "assumed_strength_retention": 0.7,
    "least_SF_with_retention": 0.5318828249382828
  },
  "sources": [
    {
      "id": "S02",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/c2eca2d0f75e11ee9aa0f6c265376dea"
    },
    {
      "id": "S03",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6"
    },
    {
      "id": "S04",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74"
    },
    {
      "id": "S07",
      "url": "https://www-pub.iaea.org/MTCD/Publications/PDF/Pub23vol5_web.pdf"
    }
  ],
  "needed_to_ground": "Measure rolled-direction/transverse compression, biaxial behavior, through-thickness/peel response and post-form/post-join properties. Resolve grade, heat treatment, gauge length and guide/datasheet discrepancies.",
  "effect_on_lead": "Current E alone gives SF 0.63631. Neither 241 MPa tensile floor nor 283 MPa inherited value is a guaranteed current SR200 compression minimum.",
  "closed_by_this_card": false
}
```

### N195 — NFI-021-BE-STRENGTH

Source `rpt-ref-769a7442efd5a04681e9`; original file `unpublished-local-ref:63c049a0d93b9857; pointer `retained original identity`.

```json
{
  "id": "NFI-021-BE-STRENGTH",
  "optimism": "O3",
  "needed_Pa": 283000000.0,
  "today_Pa": 283000000.0,
  "improvement_factor": 1.0,
  "state": "exists today as SR-200 sheet if compressive yield equals the 345 MPa datasheet minimum tensile yield (the 1967 lot shows ratio 0.99); NOT met by S-200F block at the Materion guide's 255 MPa (factor 1.11 short)",
  "grounding_card": "MAINLINE-020 (beryllium reality)",
  "note": "The point sits at face compression 1.0002: the 283 MPa inherited from 008 cites an older guide (MB-001, 41 ksi); the current Materion guide prints 'about 37 ksi' for S-200F."
}
```

### N207 — NFI-021b-FACE-AT-ONE

Source `rpt-ref-1080d4f6a1af4cfa8c67`; original file `unpublished-local-ref:4edbd73193c8c843; pointer `retained original identity`.

```json
{
  "id": "NFI-021b-FACE-AT-ONE",
  "optimism": "O3",
  "needed_Pa": 345000000.0,
  "today_Pa": 345000000.0,
  "usage": 0.0,
  "issue": "Face compression is exactly 1 on SR-200's minimum tensile yield used as compressive; no compressive minimum is published; 020's gauge tolerance ±0.1016 mm and post-form properties can take it below 1.",
  "grounding_card": "MAINLINE-020 follow-up: post-form compression and gauge map"
}
```

### N240 — NFI-028-19

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-19",
  "status": "OPEN",
  "tag": "QUESTIONABLE",
  "technology_state": "exists_today",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Parent Be properties at thin-sheet joints",
  "today_value": "021 retains 283 MPa compression and E=290 GPa. This is not a supplier thin-sheet/post-join allowable.",
  "required_or_budget_target": {
    "original_required_compression_Pa": 282948186.8240931,
    "255MPa_guide_sensitivity_capacity_ratio": 0.9012250718486905
  },
  "needed_evidence": "Confirm actual product form, orientation, gauge, formed and post-join strength. Joining mass savings do not establish this property.",
  "factor_to_216_427kg_allowance": null,
  "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."
}
```

### N401 — NFI-020C-GRADE-BASIS

Source `rpt-ref-35706d7a2ae7e951590b`; original file `unpublished-local-ref:1df5aace4f5947b0; pointer `/items/0`.

```json
{
  "id": "NFI-020C-GRADE-BASIS",
  "rank": 1,
  "kind": "proposed fix",
  "tag": "QUESTIONABLE",
  "against": "CARD.md sections 3 and 4; RESULTS mechanical_sensitivities and joining eta",
  "claim": "The faces are bought as SR-200 sheet (sections 1-2), but every strength screen uses S-200F block values: 283 MPa inherited as 'optimistic', 241 MPa block tensile minimum, and 0.7 x 241. SR-200's own sourced minimum tensile yield is 345 MPa (S03; guide p. 8), above the card's optimistic value.",
  "support": "S02 lists S-200-F in rod and bar and points to SR-200 sheet and PS-200 foil below 6.3 mm. Guide p. 8: wrought products are stronger than hot-pressed block in the working direction, and SR-200's in-plane properties are balanced by cross rolling. Guide p. 11: machined beryllium needs a 0.004 in etch on each side, together 27% of a 0.752 mm face, which points to rolled sheet for faces this thin.",
  "numbers": {
    "face_SF_at_lead": {
      "card_283": 0.8922515676202372,
      "card_241": 0.7598326070546896,
      "SR200_345": 1.0877271760741407
    },
    "least_SF_eta_0.9_0.6": {
      "card": [
        0.6504118436805659,
        0.5353509405721423
      ],
      "SR200_345_same_E": [
        0.6504118436805659,
        0.6504118436805659
      ]
    },
    "least_SF_retention_0.8E_0.7sigma": {
      "card": 0.5318828249382828,
      "SR200_345": 0.5691315271080425
    },
    "eta_at_which_net_section_governs": {
      "283": 0.728955674928437,
      "345": 0.5979549449412976
    }
  },
  "proposed_fix": "Add an SR-200 row (E 290 GPa, 345 MPa minimum tensile yield used as the compression proxy, the card's own transfer convention, QUESTIONABLE, S03) to the eta and retention screens, and keep 241 MPa only as an explicitly block-grade lower screen.",
  "effect_on_lead": "None on the least SF at eta 1. The conservative joint screen (eta 0.6) no longer lowers it (0.65041 instead of 0.53535), and the retention screen becomes wrinkling-governed at 0.56913 instead of 0.53188. Rolled-sheet compression data are still needed (owner's NFI-020-GRADE-ORIENTATION-COMPRESSION)."
}
```

### N404 — NFI-021B-CHECK-COMPRESSION

Source `rpt-ref-444ac46ffbede876f9cd`; original file `unpublished-local-ref:e116eab86edf378e; pointer `/rows/0`.

```json
{
  "id": "NFI-021B-CHECK-COMPRESSION",
  "status": "open",
  "tag": "QUESTIONABLE",
  "field": "case.face.sigma_today_Pa; O3 usage zero",
  "card": 345000000,
  "check_demand_Pa": 344998605.25332373,
  "issue": "345 MPa is the SR-200 datasheet minimum tensile yield, used as compressive. It is not a sourced compressive minimum at 0.691748 mm or after forming. The historical 379.2 MPa compression is a 1.96 mm sheet lot, not a thin-sheet minimum.",
  "implication": "The three-of-five result is conditional on an additional, unvaried material transfer assumption. The card already flags this, so this is a carried source limitation, not an arithmetic error.",
  "source": "Materion DS-HPP-613; NASA CR-194164 PDF p.22 Tables 2–3",
  "needed_evidence": "Thin-sheet post-form compression and biaxial properties, with gauge and orientation."
}
```

### N432 — NFI-028b-SR200-compression

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/8`.

```json
{
  "id": "NFI-028b-SR200-compression",
  "status": "OPEN",
  "issue": "345 MPa is tensile minimum, not a published compressive minimum; measure post-form compression.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "face_stress_scarf_Pa": 300333333.3333344,
    "face_stress_lab_weld_Pa": 321580390.796927,
    "assumed_compressive_Pa": 345000000.0
  },
  "today": {
    "minimum_tensile_Pa": 345000000.0,
    "minimum_compressive_Pa": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6",
  "O3_usage": 0
}
```

### N445 — NFI-028b-255-sensitivity

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/21`.

```json
{
  "id": "NFI-028b-255-sensitivity",
  "status": "OPEN",
  "issue": "S-200-F 255 MPa is a compression sensitivity, not a rolled-sheet specification or certified minimum.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "compression_Pa": 255000000.0,
    "no_core_face_SF_upper_bound": 0.9582172954756751
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74"
}
```

### N487 — NFI-031-BE-PROPERTIES

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/5`.

```json
{
  "id": "NFI-031-BE-PROPERTIES",
  "tag": "QUESTIONABLE",
  "issue": "SR-200 345MPa is a tensile minimum transferred to compression. The 379.2MPa endpoint is a historical lot result; continuous interpolated strength is not a procureable design allowable. 021 rev1 inherits 283MPa at E290GPa.",
  "next_evidence": "Obtain gauge-, direction-, lot-, temperature- and post-form compression and modulus allowables."
}
```

### N498 — NFI-CHECK-028B-255-BOUND

Source `rpt-ref-aae116a5fcd787ed9abc`; original file `unpublished-local-ref:b1574c3b91d41b2e; pointer `/rows/1`.

```json
{
  "id": "NFI-CHECK-028B-255-BOUND",
  "status": "stands",
  "note": "With the fixed reserve and systems removed, the largest face thickness at zero core is 0.000896786528723 m and the 255 MPa compression factor is 0.958217295476. Core mass or joint excess leaves less face thickness. No gamma or wrinkling value changes that face factor."
}
```

### N538 — NFI-036-finished-sheet-Fcy

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/0`.

```json
{
  "id": "NFI-036-finished-sheet-Fcy",
  "status": "OPEN",
  "issue": "Obtain a minimum compressive strength for the finished SR-200 face product in both in-plane directions.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "R10_scarf_MPa": 300.3333333333333,
    "R10_lab_weld_MPa": 321.580390796927,
    "R20_as_filed_including_eta09_MPa": 376.3819067936061
  },
  "today": {
    "tensile_minimum_MPa": 345,
    "matched_compressive_minimum_MPa": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "sr200; mil5j; mmpds01; mmpds08",
  "closure": "Supplier specification plus traceable post-form/post-finish compression data at 0.7-0.85 mm and around 1.4 mm, rolling directions, offset definition and lower-basis statistics."
}
```

### N539 — NFI-036-biaxial

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/1`.

```json
{
  "id": "NFI-036-biaxial",
  "status": "OPEN",
  "issue": "Validate transfer from directional uniaxial compression to equal in-plane compression.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "stress_state": "(-s,-s,0)",
    "matched_yield_locus": true
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "nasa4397; sr200_lot",
  "closure": "Matched biaxial compression yield/failure data or validated anisotropic constitutive and fracture model; distinguish membrane, bending and local 3-D stresses."
}
```

### N540 — NFI-036-historical-transfer

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/2`.

```json
{
  "id": "NFI-036-historical-transfer",
  "status": "OPEN",
  "issue": "Resolve gauge, lot and finish transfer of the 379.2 MPa historical value.",
  "state": "in_the_lab",
  "tag": "QUESTIONABLE",
  "needed": {
    "modern_target_gauges_mm": [
      0.7,
      0.85,
      1.4
    ]
  },
  "today": {
    "historical_gauge_mm": 1.96,
    "Fcy_L_MPa": 379.2
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "sr200_lot Table 3",
  "closure": "Obtain original AFML-TR-67-212 and qualification data for the purchased thin sheet; historical reported values remain non-minimum evidence."
}
```

### N541 — NFI-036-current-handbook

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/3`.

```json
{
  "id": "NFI-036-current-handbook",
  "status": "OPEN",
  "issue": "Check current authorized material allowables and purchase specification.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "approved_revision": true
  },
  "today": {
    "reviewed": "MIL-HDBK-5J/MMPDS-01 (2003), MMPDS-08 (2013)",
    "sheet_Fcy": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "mil5j; mmpds01; mmpds08",
  "closure": "Controlled current MMPDS/AMS7902 review and supplier-specific compression requirement; no assumption that a blank archived cell proves absence in all later/private data."
}
```

### N546 — NFI-036-other-sheet-grades

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/8`.

```json
{
  "id": "NFI-036-other-sheet-grades",
  "status": "OPEN",
  "issue": "Qualify PS-200 or PF-60 mechanically before substitution.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "Fcy_MPa": "route-specific requirement"
  },
  "today": {
    "catalog_nominal_mm": 0.8,
    "Fty_MPa": null,
    "Fcy_MPa": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "ps200; pf60",
  "closure": "Actual in-plane compression and biaxial qualification for the candidate grade, finish, gauge and size."
}
```

### N554 — 033-NFI-02

Source `rpt-ref-5b1ba7a48fcb57c8e35e`; original file `unpublished-local-ref:6bdf8f2e409f7e2b; pointer `/issues/1`.

```json
{
  "id": "033-NFI-02",
  "tag": "QUESTIONABLE",
  "title": "Current and historical SR-200 properties",
  "finding": "345 MPa is a current minimum tensile-yield transfer to compression. The 379.2 MPa and 293.6 GPa endpoint is a historical roughly 1.96 mm SR-200 sheet tuple. E and strength move together; no free modulus improvement is granted.",
  "next_evidence": "Obtain present supplier compression, modulus, density and process allowables for the selected gauges and formed state.",
  "status": "open"
}
```

### N652 — NFI-038-COMPRESSION

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/1`.

```json
{
  "id": "NFI-038-COMPRESSION",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "No finished thin SR200 compression minimum",
  "evidence": "036; catalog 345 MPa is tensile.",
  "resolution_needed": "Obtain lot/gauge/process specification and directional plus biaxial evidence.",
  "tests": [
    "T1"
  ]
}
```

### N689 — NFI-036-finished-sheet-Fcy

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/0`.

```json
{
  "id": "NFI-036-finished-sheet-Fcy",
  "status": "OPEN",
  "issue": "Obtain a minimum compressive strength for the finished SR-200 face product in both in-plane directions.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "R10_scarf_MPa": 300.3333333333333,
    "R10_lab_weld_MPa": 321.580390796927,
    "R20_as_filed_including_eta09_MPa": 376.3819067936061
  },
  "today": {
    "tensile_minimum_MPa": 345,
    "matched_compressive_minimum_MPa": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "sr200; mil5j; mmpds01; mmpds08",
  "closure": "Supplier specification plus traceable post-form/post-finish compression data at 0.7-0.85 mm and around 1.4 mm, rolling directions, offset definition and lower-basis statistics.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### N690 — NFI-036-biaxial

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/1`.

```json
{
  "id": "NFI-036-biaxial",
  "status": "OPEN",
  "issue": "Validate transfer from directional uniaxial compression to equal in-plane compression.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "stress_state": "(-s,-s,0)",
    "matched_yield_locus": true
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "nasa4397; sr200_lot",
  "closure": "Matched biaxial compression yield/failure data or validated anisotropic constitutive and fracture model; distinguish membrane, bending and local 3-D stresses.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### N691 — NFI-036-historical-transfer

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/2`.

```json
{
  "id": "NFI-036-historical-transfer",
  "status": "OPEN",
  "issue": "Resolve gauge, lot and finish transfer of the 379.2 MPa historical value.",
  "state": "in_the_lab",
  "tag": "QUESTIONABLE",
  "needed": {
    "modern_target_gauges_mm": [
      0.7,
      0.85,
      1.4
    ]
  },
  "today": {
    "historical_gauge_mm": 1.96,
    "Fcy_L_MPa": 379.2
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "sr200_lot Table 3",
  "closure": "Obtain original AFML-TR-67-212 and qualification data for the purchased thin sheet; historical reported values remain non-minimum evidence.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### N692 — NFI-036-current-handbook

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/3`.

```json
{
  "id": "NFI-036-current-handbook",
  "status": "OPEN",
  "issue": "Check current authorized material allowables and purchase specification.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "approved_revision": true
  },
  "today": {
    "reviewed": "MIL-HDBK-5J/MMPDS-01 (2003), MMPDS-08 (2013)",
    "sheet_Fcy": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "mil5j; mmpds01; mmpds08",
  "closure": "Controlled current MMPDS/AMS7902 review and supplier-specific compression requirement; no assumption that a blank archived cell proves absence in all later/private data.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### N697 — NFI-036-other-sheet-grades

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/8`.

```json
{
  "id": "NFI-036-other-sheet-grades",
  "status": "OPEN",
  "issue": "Qualify PS-200 or PF-60 mechanically before substitution.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "Fcy_MPa": "route-specific requirement"
  },
  "today": {
    "catalog_nominal_mm": 0.8,
    "Fty_MPa": null,
    "Fcy_MPa": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "ps200; pf60",
  "closure": "Actual in-plane compression and biaxial qualification for the candidate grade, finish, gauge and size.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### B002 — NFI-030B-FIXED-ASSUMPTIONS

Source `rpt-ref-39745602983887568501`; original file `unpublished-local-ref:534f72d6d7dd0ad8; pointer `retained original identity`.

```json
{
  "id": "NFI-030B-FIXED-ASSUMPTIONS",
  "title": "Two adjustable optimisms do not mean two unresolved assumptions.",
  "finding": "The R10 nominal scarf already fixes .015 lb/ft2 film, assumes thin stock, transfers 345 MPa tensile yield to compression and uses an unqualified 10 MPa scarf screen. Neither zero strength-slider usage nor stock panel factor one qualifies those inputs.",
  "status": "OPEN",
  "blocks_progress": false
}
```

### C011 — CHECK033-NFI-02

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/1`.

```json
{
  "id": "CHECK033-NFI-02",
  "inherited_id": "033-NFI-02",
  "tag": "QUESTIONABLE",
  "title": "Current and historical SR-200 properties",
  "finding": "345 MPa is a current minimum tensile-yield transfer to compression. The 379.2 MPa and 293.6 GPa endpoint is a historical roughly 1.96 mm SR-200 sheet tuple. E and strength move together; no free modulus improvement is granted.",
  "next_evidence": "Obtain present supplier compression, modulus, density and process allowables for the selected gauges and formed state.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Retained physical/model limitation. Arithmetic reproduction does not establish an installed-hull allowable."
}
```

### C115 — NFI-029-FACE-PLASTICITY

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/5`.

```json
{
  "id": "NFI-029-FACE-PLASTICITY",
  "status": "open",
  "title": "Faces remain elastic",
  "issue": "Neither beryllium nor stainless faces yield in the model. Beryllium inheritednu=.33 is used for comparison, not a verified grade-specific value. Known strength-basis uncertainty of021 is not resolved by these stability runs. NASA CR194164 Table2 reports SR200 in-plane nu12=.0768 andnu21=.0752 for1.96mm sheet. Treating.0768 isotropically at the lead gauge is itself a transfer. Its strong-direction endpoint98.34692kPa leaves only3.02% over operating pressure. A declared.03 sensitivity for021 gives91.468265kPa, below operating pressure. At the baseline endpoints, outer-face maximum equivalent stresses are660.806/835.808MPa for021 W/L and1144.503/1303.532MPa for021b W/L. These are von Mises diagnostics, not a verified beryllium criterion. Face survival to these loads is not established.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C166 — 040-04-face_compression

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/3`.

```json
{
  "id": "040-04-face_compression",
  "tag": "QUESTIONABLE",
  "open_issue": "Compression strength is nonbinding under the scarf cap. Marginal face-tuple floats receive elasticity credit from 033's coupled historical E/Fcy tuple.",
  "grounding": "Measure lot, orientation and formed-condition elastic modulus and compression, and state whether the design credits the coupled historical tuple."
}
```

### C226 — NFI-044-SR200-FATIGUE

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/2`.

```json
{
  "id": "NFI-044-SR200-FATIGUE",
  "finding": "The manufacturer S200F block rotating-beam data do not supply an SR200 0.8 mm processed-sheet S-N curve under biaxial compression, local bending or notch effects.",
  "evidence_needed": "Orientation-specific fatigue and fracture data on actual thin stock after forming, machining, surface preparation, bonding and repair; defects and statistical basis."
}
```

## R014 — CFRP quasi-isotropic face properties (Be-free fallback)

**Original question:** QI laminate modulus and compressive strength for T700, M55J, K13D2U and boron/epoxy are estimated from UD data with assumed reduction factors, not measured.

### N132 — NFI-008-QI-LAMINATE

Source `rpt-ref-45da79edf548b064b228`; original file `unpublished-local-ref:20c691c11e9fda46; pointer `retained original identity`.

```json
{
  "id": "NFI-008-QI-LAMINATE",
  "issue": "QI laminate E and compressive strength for T700, M55J, K13D2U and boron/epoxy are estimates from UD/fibre data with the stated reduction factors, not measured laminate cards.",
  "effect": "Those four rows move with the assumed QI factors; fibre properties were not used, per the brief.",
  "needed": "Measured QI laminate modulus and compressive strength for each system at the intended fibre volume fraction."
}
```

### N189 — NFI-020-BERYLLIUM-FREE-FALLBACK

Source `rpt-ref-3e02218a03708a878faa`; original file `unpublished-local-ref:3fe2376964ec428a; pointer `retained original identity`.

```json
{
  "id": "NFI-020-BERYLLIUM-FREE-FALLBACK",
  "rank": 5,
  "tag": "QUESTIONABLE",
  "claim": "K13D2U QI epoxy is the best inherited Be-free candidate, but its laminate and joint basis remain assumptions.",
  "optimistic": {
    "equal_5pct_budget_resized_SF": 0.6186549721852572,
    "published_zero_payload_SF": 0.6519321738941608,
    "published_relative_SF_loss_percent": 4.874389864420692
  },
  "conservative": {
    "exact_009c5_geometry_SF": 0.5414748616333155,
    "relative_SF_loss_percent": 16.74892348681649,
    "payload_kg_with_inherited_joints": 443.0337212063869
  },
  "sources": [
    {
      "id": "S09",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/d896d6d2a04211ee94aa3aa4a5458726"
    }
  ],
  "needed_to_ground": "Ground the I014b QI laminate compression/stiffness/density and manufacturing route, then use the same evidenced joint mass and geometry for Be and composite. Do not substitute single-fiber moduli.",
  "effect_on_lead": "Preserves a relatively small equal-budget trade but cannot promise a direct drop-in result. M55J is weaker in the published comparison; AlBeMet retains 62 wt% Be.",
  "closed_by_this_card": false
}
```

### N607 — NFI-017b-FACE-MATERIAL

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/7`.

```json
{
  "id": "NFI-017b-FACE-MATERIAL",
  "tag": "PROJECTION",
  "claim": "A lighter face at beryllium's E and strength (x1.73-1.87, 272-293 MPa per kg/m3) has no thin isotropic candidate: quasi-isotropic carbon is about 100 (a worker estimate with assumed matrix constants); nano-carbon films are lab only.",
  "needed_to_ground": "Sourced in-plane-isotropic properties of nano-carbon or other candidate face sheets."
}
```

## R015 — face Poisson ratio (0.33 carried; Be sheet about 0.08)

**030b source history:** 028b scalar nu=.0752 and 033 scalar nu=.0768 are historical directional proxies; the inherited .33 is a comparison. Neither validates an orthotropic formed shell.

**Original question:** Poisson ratio in buckling and foam-wrinkling formulas is carried from the 6061 case; no SiC value was given. Buckling pressure scales as 1/sqrt(1-nu^2).

### N051 — NFI-NU

Source `rpt-ref-d5b4aaa267b71d82fe25`; original file `unpublished-local-ref:1d727f2cb127351c; pointer `retained original identity`.

```json
{
  "id": "NFI-NU",
  "value": "Poisson ratio inside the buckling and foam-wrinkling formulas",
  "optimistic": 0.33,
  "conservative": 0.33,
  "factor": 1.0,
  "source": "Carried from the 6061 case. MAINLINE-008 does not give a SiC Poisson ratio.",
  "direction": "Use the face sheet's Poisson ratio. Buckling pressure scales as 1/sqrt(1-nu^2)."
}
```

### N119 — NFI-CHECK021-POISSON

Source `rpt-ref-e92af61311c9bf4a89cd`; original file `unpublished-local-ref:e3324087b91fd866; pointer `retained original identity`.

```json
{
  "id": "NFI-CHECK021-POISSON",
  "category": "inherited material-model gap",
  "status": "OPEN",
  "row": "All beryllium calculations",
  "field": "nu",
  "card_value": 0.33,
  "check_value": {
    "nu12": 0.0768,
    "nu21": 0.0752
  },
  "tag": "QUESTIONABLE transfer from an orthotropic 1.96-mm sheet lot; not a replacement isotropic specification",
  "source": "https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf",
  "location": "PDF page 22, Table 2",
  "effect": {
    "isotropic_sensitivity_E_GPa": 290,
    "nu_surrogate": 0.0768,
    "fixed_geometry_gamma_needed": 0.6169290607109224,
    "fixed_geometry_gamma_full": 0.6018361371765335,
    "fixed_geometry_full_gamma_global_SF": 0.9755353986453542,
    "preferred_subset_in_surrogate": {
      "subset": [
        "wrinkle",
        "strength"
      ],
      "best": {
        "core": "Hexcel HRH-10-4.8-32",
        "tag": "QUESTIONABLE",
        "fraction": 0.30457951448127507,
        "max_usage": 0.9985514670768213,
        "feasible_within_named": true,
        "needed": {
          "gamma": 0.9999999999999998,
          "wrinkle": 0.818919565710445,
          "strength": 368627416.93813074
        },
        "usage": {
          "gamma": 0.0,
          "wrinkle": 0.9985514670768213,
          "strength": 0.903363923032564
        },
        "feasible_intervals": [
          [
            0.30457951448127507,
            0.47808902548736587
          ]
        ]
      }
    }
  },
  "disposition": "Arithmetic follows the pinned nu=.33. Treat that as an explicit inherited assumption, not a sourced beryllium property. The demonstrated sensitivity changes the preferred two-optimism set.",
  "proposed_fix": "A card using a coherent measured in-plane elastic tuple and an appropriate orthotropic model, or an explicitly tagged isotropic approximation."
}
```

### N321 — NFI-NU

Source `rpt-mainline014-grok-balanced-sandwich-1019`; original file `unpublished-local-ref:8c5f980fe25f9829; pointer `retained original identity`.

```json
{
  "id": "NFI-NU",
  "note": "Every face uses nu 0.33 from the aluminium case. MAINLINE-008 published no Poisson ratio. CFRP, SiC and beryllium are not aluminium."
}
```

### N330 — NFI-NU

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-NU",
  "note": "Every face uses nu 0.33. MAINLINE-008 published no Poisson ratio."
}
```

### N405 — NFI-021B-CHECK-NU

Source `rpt-ref-444ac46ffbede876f9cd`; original file `unpublished-local-ref:e116eab86edf378e; pointer `/rows/1`.

```json
{
  "id": "NFI-021B-CHECK-NU",
  "status": "open",
  "tag": "QUESTIONABLE",
  "field": "inherited isotropic nu=0.33",
  "card": 0.33,
  "historical_sheet_nu12": 0.0768,
  "historical_sheet_nu21": 0.0752,
  "same_geometry_global_at_needed": 0.9611180727562139,
  "same_geometry_needed_gamma_usage": 0.9037790873103138,
  "same_set_reoptimized_usage": 0.8832886644378072,
  "issue": "The isotropic 0.33 value is inherited from aluminium, not established for SR-200. The cited lot has substantially lower in-plane Poisson ratios.",
  "implication": "At nu=.0768, fixed-geometry global SF is 0.961118. Retuning the same gamma/wrinkle/panel set works at usage about 0.883289. This scalar substitution is a sensitivity, not an orthotropic laminate solution.",
  "source": "NASA CR-194164 Tables 2–3; pinned 014b nu",
  "needed_evidence": "A consistent orthotropic shell model and sourced thin-sheet elastic tensor."
}
```

### N433 — NFI-028b-sheet-anisotropy

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/9`.

```json
{
  "id": "NFI-028b-sheet-anisotropy",
  "status": "OPEN",
  "issue": "Scalar nu=.0752 uses historical SR-200 data; a formed orthotropic shell requires its own model and properties.",
  "state": "in_the_lab",
  "tag": "QUESTIONABLE",
  "needed": {
    "nu": 0.0752,
    "E_Pa": 290000000000.0
  },
  "today": {
    "nu12": 0.0768,
    "nu21": 0.0752
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf"
}
```

### N542 — NFI-036-sheet-elastic-model

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/4`.

```json
{
  "id": "NFI-036-sheet-elastic-model",
  "status": "OPEN",
  "issue": "Resolve the scalar elastic approximation and legacy nu=0.33.",
  "state": "in_the_lab",
  "tag": "QUESTIONABLE",
  "needed": {
    "R20_scalar_sheet_threshold_MPa": 381.61217284422
  },
  "today": {
    "handbook_E_GPa": 293.02718495965536,
    "nu": 0.1,
    "historical_nu12_nu21": [
      0.0768,
      0.0752
    ]
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "mmpds08; sr200_lot",
  "closure": "Use measured post-form orthotropic stiffness, including shear moduli and reciprocity, in validated shell buckling analysis."
}
```

### N555 — 033-NFI-03

Source `rpt-ref-5b1ba7a48fcb57c8e35e`; original file `unpublished-local-ref:6bdf8f2e409f7e2b; pointer `/issues/2`.

```json
{
  "id": "033-NFI-03",
  "tag": "PROJECTION",
  "title": "Poisson ratio and isotropy",
  "finding": "Primary nu=0.0768 is the historical SR-200 in-plane value represented as an isotropic scalar. Legacy nu=.33 changes the R10 scarf-screen endpoint from a deficit to a small surplus. The sign is convention-sensitive.",
  "next_evidence": "Use a complete current orthotropic material matrix and shell analysis; establish the relevant orientation and post-form properties.",
  "status": "open"
}
```

### N602 — NFI-017b-POISSON

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/2`.

```json
{
  "id": "NFI-017b-POISSON",
  "tag": "QUESTIONABLE",
  "claim": "nu 0.08 is the S-200F VHP mean (IAEA) transferred to SR-200 sheet; the inherited 0.33 reads 2.0 percent higher (0.5387 / 0.5818 against 0.5284 / 0.5711).",
  "needed_to_ground": "A measured in-plane Poisson ratio for cross-rolled SR-200 sheet."
}
```

### N693 — NFI-036-sheet-elastic-model

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/4`.

```json
{
  "id": "NFI-036-sheet-elastic-model",
  "status": "OPEN",
  "issue": "Resolve the scalar elastic approximation and legacy nu=0.33.",
  "state": "in_the_lab",
  "tag": "QUESTIONABLE",
  "needed": {
    "R20_scalar_sheet_threshold_MPa": 381.61217284422
  },
  "today": {
    "handbook_E_GPa": 293.02718495965536,
    "nu": 0.1,
    "historical_nu12_nu21": [
      0.0768,
      0.0752
    ]
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "mmpds08; sr200_lot",
  "closure": "Use measured post-form orthotropic stiffness, including shear moduli and reciprocity, in validated shell buckling analysis.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### C012 — CHECK033-NFI-03

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/2`.

```json
{
  "id": "CHECK033-NFI-03",
  "inherited_id": "033-NFI-03",
  "tag": "PROJECTION",
  "title": "Poisson ratio and isotropy",
  "finding": "Primary nu=0.0768 is the historical SR-200 in-plane value represented as an isotropic scalar. Legacy nu=.33 changes the R10 scarf-screen endpoint from a deficit to a small surplus. The sign is convention-sensitive.",
  "next_evidence": "Use a complete current orthotropic material matrix and shell analysis; establish the relevant orientation and post-form properties.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Retained physical/model limitation. Arithmetic reproduction does not establish an installed-hull allowable."
}
```

## R016 — S-200F modulus is 290 GPa, not the 303 GPa of S-200FH

**Original question:** Comparisons retain 303 GPa, 283 MPa compression and nu 0.33 although the current forms sheet gives 290 GPa for S200F and 303 for S200FH; compression basis to reconcile.

### N001 — NFI-S200F-MODULUS

Source `rpt-1228-mainline009c5-independent-check-1019`; original file `unpublished-local-ref:52f757339520e0fd; pointer `retained original identity`.

```json
{
  "id": "NFI-S200F-MODULUS",
  "type": "source_mismatch",
  "row": "Beryllium S-200F",
  "field": "E_Pa",
  "reported": 303000000000,
  "source_value": 290000000000,
  "source_url": "https://hkvxni.files.cmp.optimizely.com/download/c3141b9ea04211ee9a7b2a5d2cb825d4",
  "page": 2,
  "proposed_fix": "Use grade-specific E=290 GPa or explicitly source a 303 GPa S200F scenario; retain QUESTIONABLE.",
  "stops_owner": false
}
```

### N007 — NFI-CHECK013-S200F-GRADE

Source `rpt-1228-mainline013-independent-check-1020`; original file `unpublished-local-ref:b1c8a108ddfdc4b1; pointer `retained original identity`.

```json
{
  "id": "NFI-CHECK013-S200F-GRADE",
  "kind": "source correction",
  "row": "ideal_lattice_PROJECTION.strut_references[2]",
  "field": "S_Pa_per_kg_m3",
  "card_value": 163783783.7837838,
  "checker_value": 156756756.75675675,
  "source": "sources/s200.pdf p2, Materion material-property comparison",
  "issue": "S200F is 290 GPa; 303 GPa belongs to S200FH. Density remains 1850 kg/m3.",
  "effects": {
    "Q_first_density_card": 4.817515578142902,
    "Q_first_density_corrected": 5.29333338323427,
    "B_first_density_card": 8.823966274563121,
    "B_first_density_corrected": 9.21851132665868,
    "Q_classical_card": 1.96042850745283,
    "Q_classical_corrected": 2.0674778788188943,
    "ideal_fraction_at_5_card": 0.9820880639067651,
    "ideal_fraction_at_5_corrected": 1.0261127012543099
  },
  "proposed_fix": "Use 290 GPa for the named grade and update its projection, or explicitly source and label S200FH. No 76-core arithmetic changes.",
  "nonblocking": true,
  "halts_owner": false,
  "halts_next_card": false
}
```

### N012 — NFI-S200F-MODULUS

Source `rpt-1228-mainline014b-independent-check-1019`; original file `unpublished-local-ref:8f2d079b76102928; pointer `retained original identity`.

```json
{
  "id": "NFI-S200F-MODULUS",
  "type": "source_mismatch",
  "row": "Beryllium S-200F",
  "field": "E_Pa",
  "reported": 303000000000,
  "source_value": 290000000000,
  "source_url": "https://hkvxni.files.cmp.optimizely.com/download/c3141b9ea04211ee9a7b2a5d2cb825d4",
  "page": 2,
  "proposed_fix": "Use grade-specific E=290 GPa or explicitly source a 303 GPa S200F scenario; retain QUESTIONABLE.",
  "stops_owner": false
}
```

### N074 — NFI-019-MATERIAL-GRADE

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-MATERIAL-GRADE",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "The current Materion forms sheet lists 290 GPa for S200F and 303 GPa for S200FH. Main comparisons deliberately retain the pinned 303 GPa, 283 MPa compression and nu=0.33; the 290 GPa sensitivity is supplied.",
  "next_evidence": "Reconcile the exact grade, compression basis, Poisson ratio and sheet/curved-face properties before revising the material point; do not substitute a tensile value for compression."
}
```

### N118 — NFI-CHECK021-MODULUS

Source `rpt-ref-e92af61311c9bf4a89cd`; original file `unpublished-local-ref:e3324087b91fd866; pointer `retained original identity`.

```json
{
  "id": "NFI-CHECK021-MODULUS",
  "category": "material source consistency",
  "status": "OPEN",
  "row": "S-200F headline and SR-200 gamma-only sensitivity",
  "field": "E_Pa",
  "card_value": 303000000000,
  "check_value": 290000000000,
  "tag": "QUESTIONABLE sourced typical, not a guaranteed minimum",
  "source": [
    "https://hkvxni.files.cmp.optimizely.com/download/c2eca2d0f75e11ee9aa0f6c265376dea",
    "https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6"
  ],
  "effect": {
    "main_same_geometry_gamma_needed": 0.5953179642995182,
    "main_same_geometry_wrinkle_coefficient_needed": 0.37068071372338524,
    "main_same_geometry_gamma_usage": 0.9580717283996654,
    "sheet_same_geometry_full_gamma_SF": 0.9423586953989969,
    "sheet_same_geometry_design_wrinkle_SF": 0.9785077502510343,
    "sheet_E290_reoptimised_gamma_only_usage": 1.091888191022227
  },
  "disposition": "The inherited arithmetic passes, but the one-optimism sheet conclusion does not survive its own datasheet E. The E290/283 main route still uses two optimisms.",
  "proposed_fix": "Keep E, strength and product form together. Reissue the 303-GPa card claims under the ordered grade correction.",
  "already_known": "The owner was ordered to correct E at 00:21:45; the observed changed results use E290 and a separate SR-200 modulus. This check does not certify that later packet."
}
```

### N198 — NFI-021-FACE-MODULUS

Source `rpt-ref-769a7442efd5a04681e9`; original file `unpublished-local-ref:63c049a0d93b9857; pointer `retained original identity`.

```json
{
  "id": "NFI-021-FACE-MODULUS",
  "issue": "Corrected by ord-admiral-rr2-mainline021-be-modulus-290-1020: S-200F scored at its own 290 GPa (Materion DS-HPP-610); the 303 GPa the chain carried is S-200FH's. The SR-200 lot's own in-plane moduli are 298.7 and 293.6 GPa; the full-set column uses the lower.",
  "numbers": "Least set unchanged; gamma's usage 0.9099 at 303 GPa becomes 0.9581; gamma needed 0.5791 becomes 0.5953."
}
```

### N402 — NFI-020C-FALLBACK-E-BASIS

Source `rpt-ref-35706d7a2ae7e951590b`; original file `unpublished-local-ref:1df5aace4f5947b0; pointer `/items/1`.

```json
{
  "id": "NFI-020C-FALLBACK-E-BASIS",
  "rank": 2,
  "kind": "proposed fix",
  "tag": "QUESTIONABLE",
  "against": "CARD.md section 6",
  "claim": "Section 4 takes 290 GPa as Be's current modulus, but section 6 prices the K13D2U trade against Be at the inherited 303 GPa. At 290 GPa, the SF given up by choosing K13D2U is smaller.",
  "numbers": {
    "published_designs": {
      "Be_303": 0.6853382311714526,
      "Be_290": 0.6705892825890435,
      "K13D2U": 0.651932173894196,
      "loss_pct_303": 4.874389864425844,
      "loss_pct_290": 2.7821960742968055
    },
    "009c5_geometry": {
      "Be_303": 0.6504118436805659,
      "Be_290": 0.6363083913759237,
      "K13D2U": 0.5414748616333155,
      "loss_pct_303": 16.74892348681649,
      "loss_pct_290": 14.903705660323697
    },
    "5pct_budget_resized": {
      "Be_lead_303": 0.6504118436805659,
      "Be_lead_290": 0.6363083913759237,
      "K13D2U": 0.6186549721852571,
      "loss_pct_303": 4.882578908096491,
      "loss_pct_290": 2.774349581103841
    }
  },
  "proposed_fix": "State section 6's SF given up at both Be moduli; K13D2U's 210 GPa stays the 014b QI value.",
  "effect_on_lead": "The Be-free fallback costs less SF than the card shows; the ranking does not change."
}
```

### N407 — NFI-021B-CHECK-GRADE-COUPLING

Source `rpt-ref-444ac46ffbede876f9cd`; original file `unpublished-local-ref:e116eab86edf378e; pointer `/rows/3`.

```json
{
  "id": "NFI-021B-CHECK-GRADE-COUPLING",
  "status": "open",
  "tag": "QUESTIONABLE",
  "field": "subsets versus optimisms.O3_face_strength.E_full_Pa",
  "card_full_E_Pa": 293600000000,
  "reproduced_search_E_Pa": 290000000000,
  "card_all_five_usage": 0.7193182727147767,
  "coupled_full_lot_E_grid_usage": 0.7088740221506279,
  "issue": "The complete subset table reproduces with E=290 GPa even when O3 is selected. Full-named-set mode and family calculations instead use 293.6 GPa. Thus the subset table does not literally couple every O3 strength choice to the stated alternate lot modulus.",
  "implication": "Using E=293.6 GPa whenever O3 is selected changes secondary scores, e.g. all five to 0.708874 on the same grid. No subset feasibility changes and no two-member set floats. The chosen three-member set has no O3, so its answer is unchanged.",
  "needed_evidence": "Declare whether keeping 290 GPa is intentional conservatism; if grade and strength co-vary, specify interpolation and recompute the usage objective."
}
```

## R017 — SiC face properties (009b)

**Original question:** SiC face compressive strength is taken as 3900 MPa (compression mode) vs 380 MPa flexural; a compressive allowable for the sintered face and a membrane-compression-only check are open.

### N049 — NFI-FACE-STRENGTH

Source `rpt-ref-d5b4aaa267b71d82fe25`; original file `unpublished-local-ref:1d727f2cb127351c; pointer `retained original identity`.

```json
{
  "id": "NFI-FACE-STRENGTH",
  "value": "SiC face compressive strength",
  "optimistic": 3900000000.0,
  "optimistic_source": "Saint-Gobain Hexoloy SA data https://www.ceramicsrefractories.saint-gobain.com/pt/files/4731/view (compressive 3900 MPa, flexural 380 MPa); MatWeb alpha SiC https://www.matweb.com/search/datasheet_print.aspx?matguid=dd2598e783ba4457845586b58c8ea9fb (density 3.10 g/cc, E 410 GPa)",
  "conservative": 380000000.0,
  "conservative_source": "Hexoloy SA flexural strength, the figure MAINLINE-008 says governs a bending or tension path.",
  "factor": 10.263157894736842,
  "stated_mode_uses": "compressive 3900 MPa, because the stated mode is face compression",
  "SF_if_flexural_were_used": 0.433343716061625,
  "direction": "A compressive allowable for the sintered face, and a check that the sphere stress stays membrane compression."
}
```

### N050 — NFI-FACE-MODULUS

Source `rpt-ref-d5b4aaa267b71d82fe25`; original file `unpublished-local-ref:1d727f2cb127351c; pointer `retained original identity`.

```json
{
  "id": "NFI-FACE-MODULUS",
  "value": "SiC Young's modulus and density",
  "optimistic": {
    "E_Pa": 410000000000.0,
    "rho": 3100.0
  },
  "conservative": "no second sourced pair on MAINLINE-008",
  "factor": null,
  "tag": "QUESTIONABLE",
  "direction": "A batch modulus and density for the face sheet that would actually be built."
}
```

## R018 — Be thin-sheet panel size and gauge: 0.914 m square-equivalent stock today, 3.13 to 4 m assumed (O4)

**Current 030c:** CHECK-038 and 042 retain the thin-stock restriction: .6096×1.8288 m at about .8 mm is not established by the maker's stock envelope. No panel enlargement is chosen, but factor one is not demonstrated supply.

**030b source history:** Stock envelope factor is now one in 028b/033, eliminating adjustable panel enlargement. Availability at the required sub-1.499 mm gauges is still unestablished. 033's formal 103.892 m gamma+strength crossing exceeds the 6.35 mm sheet maximum.

**Original question:** Severe-budget faces are far below supplier stock gauge; stock for the large panel begins at 0.059 in and the enhanced aluminium face at R=20 is thinner. Small panel size assumed.

### N071 — NFI-019-PANELS

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-PANELS",
  "tag": "PROJECTION",
  "status": "open",
  "issue": "Neither 4 m nor 0.6 m curved thin S200F sandwich panels are established catalog products. The predecessor's 0.6-1.2 m rolled-sheet availability claim lacked a qualifying source. Required 18 m equivalent widths also exceed the local square-panel approximation's useful domain.",
  "next_evidence": "Obtain a manufacturer-specific material grade, size, forming route, thickness tolerance and yield quote; replace 2A/w with a spherical seam-layout takeoff."
}
```

### N077 — NFI-019-GEOMETRY-MODES

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-GEOMETRY-MODES",
  "tag": "PROJECTION",
  "status": "open",
  "issue": "The severe case mathematically selects about 0.056-0.057 mm Be faces and 6.8-8.3 mm core. These are unqualified fabrication and continuum-model geometries; every scored least factor is far below 1.",
  "next_evidence": "Treat the result as an estimate of the gap, not a build point; local face/core geometry, buckling imperfections, seam load transfer and nonlinear validation remain open."
}
```

### N100 — NFI-027-PANEL-GAUGE

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-PANEL-GAUGE",
  "tag": "PROJECTION",
  "issue": "The large 020 panel is 0.6096×1.8288 m; its quoted stock maximum begins at 0.059 in (1.4986 mm). At R = 20 the enhanced aluminium face is only 1.423 mm. The conservative small panel is an assumed 0.3048×0.6096 m. Some severe-budget faces are far below the supplier's stated sheet gauge.",
  "next_evidence": "Supplier-confirm panel dimensions at each minimum gauge, shaping yield, thickness distribution and installed geometry; re-run with procurement bounds."
}
```

### N186 — NFI-020-THIN-SHEET-GEOMETRY

Source `rpt-ref-3e02218a03708a878faa`; original file `unpublished-local-ref:3fe2376964ec428a; pointer `retained original identity`.

```json
{
  "id": "NFI-020-THIN-SHEET-GEOMETRY",
  "rank": 2,
  "tag": "PROJECTION",
  "claim": "Maximum currently purchasable 0.75-0.79 mm panel size and installed shape are UNKNOWN.",
  "optimistic": {
    "assumed_panel_m": [
      0.6096,
      1.8288
    ],
    "panels_per_skin_lower_bound": 1128,
    "flatness_type3_mm_per_foot": 0.762,
    "nominal_gauge_m": 0.000752430055433027
  },
  "conservative": {
    "assumed_panel_m": [
      0.3048,
      0.6096
    ],
    "panels_per_skin_lower_bound": 6764,
    "flatness_type1_fraction_span": 0.02,
    "source_gauge_tolerance_m": 0.0001016
  },
  "sources": [
    {
      "id": "S03",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6"
    },
    {
      "id": "S04",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74"
    }
  ],
  "needed_to_ground": "Ground second, with material NFI: obtain a supplier-confirmed grade/gauge/size/flatness specification, formed-panel gauge map and curvature survey. Measure edge and joint steps; establish trim yield.",
  "effect_on_lead": "Thinner-size maximum is unspecified. Uniform upper tolerance adds 472.40 kg faces; low-gauge wrinkle SF is 0.52323. Flatness measured restrained cannot qualify assembled buckling.",
  "closed_by_this_card": false
}
```

### N199 — NFI-021-SHEET-SIZE

Source `rpt-ref-769a7442efd5a04681e9`; original file `unpublished-local-ref:63c049a0d93b9857; pointer `retained original identity`.

```json
{
  "id": "NFI-021-SHEET-SIZE",
  "issue": "SR-200 sheet comes to 24 by 72 inches, with gauges under 0.059 inch only at narrower widths and shorter lengths (Materion datasheet); a 10 m sphere needs over a thousand sheets, so the 5 percent joint allowance is QUESTIONABLE.",
  "grounding_card": "MAINLINE-020"
}
```

### N205 — NFI-021b-PANEL

Source `rpt-ref-1080d4f6a1af4cfa8c67`; original file `unpublished-local-ref:4edbd73193c8c843; pointer `retained original identity`.

```json
{
  "id": "NFI-021b-PANEL",
  "optimism": "O4",
  "needed_m": 3.1278027873808982,
  "today_m": 0.9144000000000001,
  "full_m": 4.0,
  "improvement_factor": 3.4206067228575,
  "usage": 0.8333333333333334,
  "state": "PROJECTION",
  "note": "Thin (<0.059 in) SR-200 stock size is unpublished (020: UNKNOWN); curved forming at 10 m radius unverified.",
  "grounding_card": "a supplier-confirmed thin-sheet specification (020's first ground)"
}
```

### N235 — NFI-028-14

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-14",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Today thin-sheet stock size",
  "today_value": "609.6 x 1828.8 mm is published for thicker sheet. Maximum size at 0.843 mm is UNKNOWN; smaller 304.8 x 609.6 is owner planning.",
  "required_or_budget_target": "Supplier-confirmed grade, gauge, blank dimensions and tolerances.",
  "needed_evidence": "A real quote/specification; do not label an extrapolated catalogue envelope as purchasable thin sheet.",
  "scenario": "af015_scarf",
  "scenario_joining_kg": 214.2399978421616,
  "factor_to_216_427kg_allowance": 0.9898943034693449,
  "mass_reduction_factor_to_fit": 1
}
```

### N236 — NFI-028-15

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-15",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Four-metre panels",
  "today_value": "4 x 4 m face blanks and compatible core are not demonstrated in the cited stock data",
  "required_or_budget_target": {
    "short_stock_dimension_scale_factor": 6.561679790026246,
    "long_stock_dimension_scale_factor": 2.1872265966754156,
    "modeled_AF_scarf_4m_kg": 190.76436622924268
  },
  "needed_evidence": "Demonstrate the actual continuous face and include internal stock seams/core splices. A 4 m module assembled from small sheets keeps their seams.",
  "factor_to_216_427kg_allowance": null,
  "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."
}
```

### N409 — NFI-021B-CHECK-PANEL-GAUGE

Source `rpt-ref-444ac46ffbede876f9cd`; original file `unpublished-local-ref:e116eab86edf378e; pointer `/rows/5`.

```json
{
  "id": "NFI-021B-CHECK-PANEL-GAUGE",
  "status": "open",
  "tag": "PROJECTION",
  "field": "O4 today's panel width and headline 0.691748 mm faces",
  "card_today_square_equivalent_m": 0.9144,
  "required_panel_m": 3.1278027873808987,
  "gauge_minus_01016mm_modes": {
    "global_buckling": 0.885172336569417,
    "face_compression": 0.8531291534717521,
    "core_shear_crimping": 3.0755087830073746,
    "core_crush": 5.0558220634629825,
    "face_wrinkling": 0.7879878860686423,
    "intracell_dimpling": 3.089293361240542
  },
  "issue": "The 609.6 by 1828.8 mm stock limit applies to gauges at least .059 inch; the maximum stock size at the required .0272 inch gauge is unspecified. Forming, joining and gauge retention at a 3.128 m square-equivalent panel are unestablished.",
  "implication": "Even the today panel endpoint is a thin-sheet transfer. A uniform minus-0.1016-mm gauge screen at fixed core reduces compression SF to 0.853129 and wrinkling SF to 0.787988; this is a sensitivity, not a prediction of the delivered gauge distribution.",
  "source": "Materion DS-HPP-613; MAINLINE-020 gauge/shape assessment",
  "needed_evidence": "Supplier-confirmed gauge and dimensions, curved panel takeoff, measured gauge and shape map."
}
```

### N435 — NFI-028b-stock-envelope

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/11`.

```json
{
  "id": "NFI-028b-stock-envelope",
  "status": "OPEN",
  "issue": "Confirm available raw blank sizes at 0.74–0.80 mm thickness; full published envelope belongs to thicker sheet.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "a_m": 0.6096,
    "b_m": 1.8288
  },
  "today": {
    "thin_gauge_envelope": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6",
  "panel_search_usage": 0,
  "panel_enlargement_factor": 1
}
```

### N488 — NFI-031-PANELS

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/6`.

```json
{
  "id": "NFI-031-PANELS",
  "tag": "PROJECTION",
  "issue": "The least-set P2 points need multi-metre square-equivalent panels at roughly 0.65–0.72mm face gauge. The nominal today 0.9144m seam-equivalent stock size is itself not established at those gauges.",
  "next_evidence": "Supplier-confirm formed sheet sizes, gauges, thickness distribution, yield and joining geometry."
}
```

### N511 — ams7902-class-table-unread

Source `rpt-mainline032b-grok-measured-flatness-1020`; original file `unpublished-local-ref:9a0f9d6404b3f821; pointer `/open/0`.

```json
{
  "id": "ams7902-class-table-unread",
  "tag": "QUESTIONABLE",
  "note": "AMS7902G section 3.5.5 was not in the three-page file. Current revision H, DOI 10.4271/AMS7902H, was not opened. No class tolerance is stated."
}
```

### N545 — NFI-036-stock-size

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/7`.

```json
{
  "id": "NFI-036-stock-size",
  "status": "OPEN",
  "issue": "Confirm available blank dimensions at the required thin gauges.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "width_m": 0.6096,
    "length_m": 1.8288
  },
  "today": {
    "catalog_full_envelope_minimum_mm": 1.4986
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "sr200 p3",
  "closure": "Supplier-confirmed usable dimensions at final gauge; rerun seams/mass if smaller."
}
```

### N557 — 033-NFI-05

Source `rpt-ref-5b1ba7a48fcb57c8e35e`; original file `unpublished-local-ref:6bdf8f2e409f7e2b; pointer `/issues/4`.

```json
{
  "id": "033-NFI-05",
  "tag": "PROJECTION",
  "title": "Stock dimensions and face gauges",
  "finding": "The .6096 by 1.8288 m stock envelope is only published for gauges >=1.4986 mm; it is projected for thinner R10/R15 minima and the QS threshold. Formal gamma-plus-strength flotation at 103.892 m needs 8.235 mm faces, exceeding the 6.35 mm sheet maximum; even compression alone limits that stock to R<=99.898 m.",
  "next_evidence": "Obtain gauge-specific stock dimensions, tolerances, forming and scarf-machining feasibility. The formal oversized result is not an available-stock design.",
  "status": "open"
}
```

### N696 — NFI-036-stock-size

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/7`.

```json
{
  "id": "NFI-036-stock-size",
  "status": "OPEN",
  "issue": "Confirm available blank dimensions at the required thin gauges.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "width_m": 0.6096,
    "length_m": 1.8288
  },
  "today": {
    "catalog_full_envelope_minimum_mm": 1.4986
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "sr200 p3",
  "closure": "Supplier-confirmed usable dimensions at final gauge; rerun seams/mass if smaller.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### C014 — CHECK033-NFI-05

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/4`.

```json
{
  "id": "CHECK033-NFI-05",
  "inherited_id": "033-NFI-05",
  "tag": "PROJECTION",
  "title": "Stock dimensions and face gauges",
  "finding": "The .6096 by 1.8288 m stock envelope is only published for gauges >=1.4986 mm; it is projected for thinner R10/R15 minima and the QS threshold. Formal gamma-plus-strength flotation at 103.892 m needs 8.235 mm faces, exceeding the 6.35 mm sheet maximum; even compression alone limits that stock to R<=99.898 m.",
  "next_evidence": "Obtain gauge-specific stock dimensions, tolerances, forming and scarf-machining feasibility. The formal oversized result is not an available-stock design.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Retained physical/model limitation. Arithmetic reproduction does not establish an installed-hull allowable."
}
```

### C104 — NFI-CHECK038-STOCK_SIZE

Source `rpt-ref-2beb70a569266cf0297d`; original file `unpublished-local-ref:0746af9cb88f6eb1; pointer `/items/2`.

```json
{
  "id": "NFI-CHECK038-STOCK_SIZE",
  "status": "OPEN",
  "blocking": false,
  "issue": "The shared-stock example assumes a 24×72 inch blank at about 0.8 mm.",
  "evidence": "Materion assigns reduced dimensions to 0.020–0.058 inch sheet. The mass arithmetic is right, but that full-envelope product is not established.",
  "resolution_needed": "Obtain a finished-gauge/blank/process specification and a cutting layout; revise the stock/process allowance if only smaller or thicker blanks are available.",
  "tests": [
    "T1",
    "T2",
    "T3"
  ],
  "classification": "specific procurement gap"
}
```

### C139 — N042-03

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/2`.

```json
{
  "id": "N042-03",
  "issue": "Thin-sheet size is unknown",
  "detail": "SR-200 at 0.795 mm is in the 0.020-0.058 in class sold 'at narrower widths and shorter lengths' than 24 x 72 in (DS-HPP-613). The 028b blank of 0.6096 x 1.8288 m is a projection; smaller sheets multiply blanks and seams (020: up to 6,764 per skin).",
  "to_close": "Supplier specification (038 T1).",
  "tag": "QUESTIONABLE"
}
```

### C172 — 040-10-stock_and_mouldline

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/9`.

```json
{
  "id": "040-10-stock_and_mouldline",
  "tag": "PROJECTION",
  "open_issue": "Low-radius face gauges are outside the cited standard sheet gauge envelope; spherical coverage and rejection rates are unresolved.",
  "grounding": "Confirm formed stock supply and make a dimensioned panel/seam/mouldline manufacturing account."
}
```

## R019 — core crush criterion (crush strength against p/2)

**Original question:** Hexcel CR-III crush column is used; HFT and HRH-49 have no crush column so stabilised compressive strength is used; thickness does not enter; target is p/2.

### N033 — NFI-CRUSH

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-CRUSH",
  "gap": "Crush is stated as about p/2 and tagged QUESTIONABLE. It is the brief's approximation, not an equilibrium solution, and it is outside the least stated safety factor.",
  "direction": "Keep it tagged until a sourced crush model replaces it.",
  "effect": "Catalog compressive strengths at 16 to 38 kg/m3 clear p/2 by about 7 to 27 times."
}
```

### N053 — NFI-CRUSH-MODEL

Source `rpt-ref-d5b4aaa267b71d82fe25`; original file `unpublished-local-ref:1d727f2cb127351c; pointer `retained original identity`.

```json
{
  "id": "NFI-CRUSH-MODEL",
  "value": "core compressive stress",
  "optimistic": "p/2",
  "conservative": "p/2",
  "factor": 1.0,
  "source": "MAINLINE-005b. The brief's example, not a solved contact problem.",
  "direction": "A core stress from the face-to-face load path, including local bending."
}
```

### N128 — NFI-005B-MODEL

Source `rpt-ref-9dd3721f6f2e5595ab9a`; original file `unpublished-local-ref:f2f94747b8afb926; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-005B-MODEL",
  "gap": "The p/2 core stress is the brief's example model, QUESTIONABLE, with no pinned sandwich reference. Local face bending and load spreading are ignored.",
  "direction": "Pin a sandwich core-crush reference and re-derive the factor.",
  "effect": "Required core strength scales linearly with whatever factor replaces 1/2."
}
```

### N130 — NFI-005B-007

Source `rpt-ref-9dd3721f6f2e5595ab9a`; original file `unpublished-local-ref:f2f94747b8afb926; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-005B-007",
  "gap": "MAINLINE-007 is not filed yet, so its rows have no crush numbers here, only the ready formula.",
  "direction": "Apply p/2 at 007's external pressure when that card lands.",
  "effect": "None until 007 exists."
}
```

### N168 — NFI-013-CRUSH-MODEL

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-CRUSH-MODEL",
  "inherited": "MAINLINE-005b",
  "issue": "The p/2 core-stress model is the brief's own example, QUESTIONABLE; local face bending is ignored.",
  "numbers": "Required 47730.4 Pa on every row.",
  "closes_when": "a sandwich-sphere through-thickness solution replaces it."
}
```

### N266 — NFI-CRUSH

Source `rpt-mainline003-grok-p2-targets-1019`; original file `unpublished-local-ref:c644022670e558c3; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-CRUSH",
  "gap": "Core crush has no formula in the pinned brief, so no crush target was produced.",
  "direction": "Name a crush pressure formula before treating crush as a stated limit.",
  "effect": "Crush is absent from the least stated safety factor."
}
```

### N276 — NFI-CRUSH

Source `rpt-mainline004-grok-knockdown-card-1019`; original file `unpublished-local-ref:bd4eb9f1634108a4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-CRUSH",
  "gap": "Core crush still has no formula.",
  "direction": "Unchanged from 003.",
  "effect": "Crush stays out of the buckling safety factor."
}
```

### N326 — NFI-CRUSH

Source `rpt-mainline014-grok-balanced-sandwich-1019`; original file `unpublished-local-ref:8c5f980fe25f9829; pointer `retained original identity`.

```json
{
  "id": "NFI-CRUSH",
  "note": "Core crush is compressive strength over p/2. Thickness does not enter. The target is the MAINLINE-007 reading of about p/2."
}
```

### N340 — NFI-CRUSH-COLUMN

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-CRUSH-COLUMN",
  "note": "Hexcel CR-III crush is the crush column. HFT and HRH-49 have no crush column, so the stabilised compressive strength is used. Thickness does not enter the crush safety factor. The target is p/2."
}
```

## R020 — core shear strength is not a scored mode

**Original question:** L and W plate-shear strengths are stored, but the crimp mode scores shear modulus and shear strength is not a separate mode.

### N341 — NFI-SHEAR-STRENGTH

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-SHEAR-STRENGTH",
  "note": "L and W plate-shear strengths are stored from the sheets. The scored crimp mode uses shear modulus. Shear strength is not a separate mode."
}
```

## R021 — foam core allowables (crush strain, creep, design values)

**Original question:** H35 properties are typical or nominal, not allowables; rev9 prints a minimum compressive strength of 0.3 MPa vs 0.5 MPa nominal used (factor 1.67).

### N052 — NFI-CORE

Source `rpt-ref-d5b4aaa267b71d82fe25`; original file `unpublished-local-ref:1d727f2cb127351c; pointer `retained original identity`.

```json
{
  "id": "NFI-CORE",
  "value": "Divinycell H35",
  "optimistic": {
    "density_kg_m3": 38.0,
    "Ec_Pa": 40000000.0,
    "Gc_Pa": 12000000.0,
    "compressive_Pa": 500000.0
  },
  "conservative": "Divinycell rev9 prints a minimum compressive strength of 0.3 MPa against the nominal 0.5 MPa used here. Other cores on MAINLINE-007 are typical columns, not allowables.",
  "factor_divinycell_compression": 1.6666666666666667,
  "tag": "QUESTIONABLE",
  "direction": "Design allowables for Ec, Gc and compressive strength at the thickness this point uses."
}
```

### N129 — NFI-005B-STRAIN

Source `rpt-ref-9dd3721f6f2e5595ab9a`; original file `unpublished-local-ref:f2f94747b8afb926; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-005B-STRAIN",
  "gap": "Foam strengths are quoted at 1% and 10% strain by different sources. The incumbent 16 kg/m3 passes on one definition and fails on the other.",
  "direction": "The checker names the governing strain definition for a vacuum shell core.",
  "effect": "Lowest passing density moves between about 11 and about 22 kg/m3 on that choice."
}
```

### N131 — NFI-005B-CREEP

Source `rpt-ref-9dd3721f6f2e5595ab9a`; original file `unpublished-local-ref:f2f94747b8afb926; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-005B-CREEP",
  "gap": "EPS at 10% strain is a short-term value; sustained vacuum loading creeps. No creep derate is applied.",
  "direction": "Derate foam allowables for sustained load before any density near 11 kg/m3 is relied on.",
  "effect": "The practical lowest density is higher than 11 kg/m3."
}
```

### N169 — NFI-013-EPS-DEFINITIONS

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-EPS-DEFINITIONS",
  "issue": "EPS strengths are specification minima at 1, 5 or 10 percent strain, and the sheets disagree.",
  "numbers": "EPS12 (11.2 kg/m3): 15 kPa at 1 percent and 40 kPa at 10 percent (ASTM D6817 minima, margins 0.314 and 0.838); 34 kPa at 10 percent (older C578 minimum, 0.712); 005b's National Polystyrene 50 kPa at 11 kg/m3 gave 1.05.",
  "closes_when": "the design adopts one strain definition and a measured (not minimum) value."
}
```

### C111 — NFI-029-FOAM

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/1`.

```json
{
  "id": "NFI-029-FOAM",
  "status": "open",
  "title": "Crushable foam missing",
  "issue": "Paper uses crushable-foam plasticity, density80kg/m3 and plotted compression hardening. Present PVC80 is elastic E40MPa,nu0. The full yield-surface/hardening and contact-created initial fields were not recovered; no parameters were tuned to the target pressure.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C122 — NFI-029-STEEL-CURVE

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/12`.

```json
{
  "id": "NFI-029-STEEL-CURVE",
  "status": "open",
  "title": "Steel graph scale ambiguity",
  "issue": "EUCASS Figure5 is labelled~7500–10000MPa at strain0–.4. This was not silently divided by10 or used as a calibrated steel law.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

## R022 — honeycomb datasheet values and conversions (W vs L shear, typical vs minimum, density)

**Original question:** Datasheets print conflicting values: Plascore 5052 gives 100 psi and 0.55 MPa in one cell; Divinycell H35 0.45 MPa (rev7) vs 0.50 MPa (rev9). Crush margins still clear.

### N039 — NFI-DATASHEET

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-DATASHEET",
  "gap": "Plascore PAMG-XR1 5052 prints 100 psi and 0.55 MPa in one bare-compression minimum cell. Those are not the same number. Divinycell H35 prints 0.45 MPa on a rev7 sheet and 0.50 MPa nominal on rev9. The psi column and the rev9 nominal were used.",
  "direction": "Keep both readings. Do not pick a silent third value.",
  "effect": "The crush margins move by that disagreement and still clear p/2."
}
```

### N201 — NFI-021-CORE-TABLE

Source `rpt-ref-769a7442efd5a04681e9`; original file `unpublished-local-ref:63c049a0d93b9857; pointer `retained original identity`.

```json
{
  "id": "NFI-021-CORE-TABLE",
  "issue": "Core properties are 014b's: W shear as Gc, stabilised Ec, Hexcel's crush column for crush; Hexcel test thickness 0.625 inch against a 20 mm core.",
  "grounding_card": "none pending"
}
```

### N246 — NFI-CORE

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-CORE",
  "linked_inputs_or_points": "I-RHO-CORE",
  "questionable_assumption_or_gap": "16 kg/m^3 has no pinned datasheet.",
  "direction_of_further_investigation": "Pin a honeycomb or foam sheet at the thickness used.",
  "how_it_affects_margin_or_SF": "Core density scales core mass and can erase the float margin. It does not enter the reported collapse formula."
}
```

### N334 — NFI-W-SHEAR

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-W-SHEAR",
  "note": "Gc is the W plate-shear modulus, the lower of L and W on every sheet row scored here. Crimping and honeycomb wrinkling use that Gc."
}
```

### N335 — NFI-W-13-3

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-W-13-3",
  "note": "The attributes brochure text shows 13.3 ksi for CR-III 5052 3/16-2.0 W modulus. The CR-III data sheet prints 14.3 ksi. This card uses 14.3. The brochure's 1/4-3.4 L modulus glyph 50..0 is 50.0 on the data sheet."
}
```

### N337 — NFI-DENSITY

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-DENSITY",
  "note": "Hexcel pcf converts at 0.45359237/0.3048^3. Plascore uses the kg/m3 printed on its sheet, so 2.0 pcf is 32 there and 32.037 on the Hexcel conversion. Rows above 4.0 pcf, and Plascore rows printed above 64 kg/m3, are outside the band and were not scored. HFT at 4.0 pcf converts to 64.074 kg/m3 and is kept."
}
```

### N338 — NFI-CARBON

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-CARBON",
  "note": "No carbon-fiber honeycomb sheet located here lists stabilised Ec and both shear moduli in this density band. Hexcel's product list has no carbon honeycomb table. Ultracor UCF-51-3/8-2.0 on MatWeb lists density 0.032 g/cc, compressive yield 1.41 MPa and L shear modulus 0.331 GPa, and omits Ec and W shear, so it is not scored. HFT is fiberglass phenolic. HRH-49 is Kevlar 49 fabric. Neither is carbon."
}
```

### N444 — NFI-028b-core-data

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/20`.

```json
{
  "id": "NFI-028b-core-data",
  "status": "OPEN",
  "issue": "Confirm core lot, minimum properties, forming and strength after bonding on the selected low-density core.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "name": "Hexcel CR-III 5056 3/8-1.0",
    "family": "aluminium_honeycomb",
    "form": "honeycomb",
    "cell": "3/8",
    "pcf": 1.0,
    "rho": 16.018463373960138,
    "s_cell_m": 0.009524999999999999,
    "Ec_Pa": 103421359.3975254,
    "Gc_Pa": 46884349.59354485,
    "Gl_Pa": 103421359.3975254,
    "crush_Pa": 241316.50526089262,
    "shear_strength_L_Pa": 379211.65112425986,
    "shear_strength_W_Pa": 241316.50526089262,
    "tag": "QUESTIONABLE",
    "source": "Hexcel HexWeb CR-III data sheet, 5056 typical, https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf",
    "ec_source": "sheet",
    "crush_basis": "CR-III crush column",
    "Gc_direction": "W"
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "Hexcel HexWeb CR-III data sheet, 5056 typical, https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf"
}
```

### N529 — NFI-032-CHECK-MINIMUM-AVERAGE

Source `rpt-ref-a30a669ed3e245f1473b`; original file `unpublished-local-ref:46e93c1ee5674acc; pointer `/findings/1`.

```json
{
  "id": "NFI-032-CHECK-MINIMUM-AVERAGE",
  "status": "qualification",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "Owner calls 35 psi the stabilized minimum.",
  "checked": "Table II labels min as minimum average for a product type, not a guaranteed pointwise or full-hull minimum. Ec is typical. Pairing these values is a scenario, not a statistical lower tolerance bound.",
  "followup": "Use the precise source label and a qualified statistical/material basis for any design allowable.",
  "source_audit_ids": [
    "HEXCEL-5056"
  ],
  "owner_nfi_ids": []
}
```

### N612 — NFI-017b-CORE-CHOICE

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/12`.

```json
{
  "id": "NFI-017b-CORE-CHOICE",
  "tag": "QUESTIONABLE",
  "claim": "Directions are computed on the lead's CR-III 5056 3/8-1.0; 5056 1/4-1.6 is 2.7 percent better today (0.5425 / 0.5939).",
  "needed_to_ground": "None for the ranking; factors on 1/4-1.6 would be slightly smaller."
}
```

### N625 — NFI-032-CHECK-FC

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/prior_032_findings_retained/0`.

```json
{
  "id": "NFI-032-CHECK-FC",
  "status": "qualification",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "60 psi typical and 35 psi stabilized compression are used as Fc scenarios.",
  "checked": "The correct Fc is min(compression, core tension, facing-core bond). Neither scenario establishes the bonded sandwich value. Typical crush 35 psi happens to equal minimum-average stabilized compression numerically, but represents a different property.",
  "followup": "Preserve the conditional labels; supply matching core tensile and Be-bond flatwise data before converting the scenario into an allowable.",
  "source_audit_ids": [
    "NASA-FC",
    "HEXCEL-5056"
  ],
  "owner_nfi_ids": [
    "fc-is-the-lower-of-three"
  ]
}
```

### N626 — NFI-032-CHECK-MINIMUM-AVERAGE

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/prior_032_findings_retained/1`.

```json
{
  "id": "NFI-032-CHECK-MINIMUM-AVERAGE",
  "status": "qualification",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "Owner calls 35 psi the stabilized minimum.",
  "checked": "Table II labels min as minimum average for a product type, not a guaranteed pointwise or full-hull minimum. Ec is typical. Pairing these values is a scenario, not a statistical lower tolerance bound.",
  "followup": "Use the precise source label and a qualified statistical/material basis for any design allowable.",
  "source_audit_ids": [
    "HEXCEL-5056"
  ],
  "owner_nfi_ids": []
}
```

### C051 — NFI-CHECK037-SHEAR-ALLOWABLE

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/13`.

```json
{
  "id": "NFI-CHECK037-SHEAR-ALLOWABLE",
  "tag": "QUESTIONABLE",
  "status": "open",
  "finding": "The 241.317 kPa W value is typical core shear, not a bonded-interface or cyclic allowable; the minimum-average column is 172.369 kPa.",
  "proposed_fix": "Choose the intended material statistic, stress-free bond temperature, finite transfer geometry and interface properties. The nominal thermal-change limits are 27.975 K typical and 19.982 K minimum-average in this screen."
}
```

### C100 — NFI-037b-FOIL

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/11`.

```json
{
  "id": "NFI-037b-FOIL",
  "tag": "QUESTIONABLE",
  "claim": "5056-H39 foil properties were not sourced: the wall stiffness uses 5056-H14 bulk (67 GPa, 2700 kg/m3) and the wall allowable the measured 5052-H39 foil yield (227.5 MPa).",
  "needed_to_ground": "5056-H39 foil modulus and yield."
}
```

### C173 — 040-11-core_properties

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/10`.

```json
{
  "id": "040-11-core_properties",
  "tag": "QUESTIONABLE",
  "open_issue": "Typical CR-III properties, weak shear direction and scalar elasticity are transferred to a formed shell.",
  "grounding": "Measure density, orthotropic stiffness, compression, shear and crushed/formed condition for the selected lot."
}
```

### C197 — NFI-037b-FOIL

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/11`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-FOIL",
  "tag": "QUESTIONABLE",
  "claim": "5056-H39 foil properties were not sourced: the wall stiffness uses 5056-H14 bulk (67 GPa, 2700 kg/m3) and the wall allowable the measured 5052-H39 foil yield (227.5 MPa).",
  "needed_to_ground": "5056-H39 foil modulus and yield."
}
```

### C218 — NFI-CHECK037b-FOIL-ALLOWABLE-TRANSFER

Source `rpt-ref-4bf25e71ae0c2ca315e2`; original file `unpublished-local-ref:0360eb0aa78daa3e; pointer `/items/3`.

```json
{
  "id": "NFI-CHECK037b-FOIL-ALLOWABLE-TRANSFER",
  "tag": "QUESTIONABLE",
  "status": "OPEN",
  "finding": "67 GPa/2700 kg/m3 came from a 5056-H14 bulk register, while 227.53 MPa comes from 5052-H39 foil. Neither is a primary allowable for the actual cured 5056-H39 core. The 10 MPa Be scarf limit also remains projected.",
  "disposition": "Use the present numbers only as model inputs; measure or source the actual foil and bonded-scarf properties.",
  "carries_owner_rows": [
    "NFI-037b-FOIL",
    "NFI-037b-SCARF",
    "NFI-037b-028B-SCARF-LEVER"
  ],
  "blocking": false
}
```

## R023 — thick curved honeycomb core validation

**Original question:** Core data are catalogue typical rows tested at 15.875 mm depth, while optimised cores reach about 120-144 mm; Ec transferred from another maker and bare compression substituted for crush.

### N105 — NFI-027-CORE-TRANSFER

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-CORE-TRANSFER",
  "tag": "QUESTIONABLE",
  "issue": "5056 3/8-1.0 uses the published typical Ec/Gc/crush row; stabilized modulus is used in the wrinkle formula. Manufacturer tests were at 15.875 mm depth; optimized cores reach roughly 120–144 mm at R = 50.",
  "next_evidence": "Validate thick curved honeycomb, skin restraint, orthotropy, cell-depth effects, local modes, thermal response and crush definition. Catalogue sensitivity includes Plascore rows with Ec transferred from Hexcel and bare compression substituted for crush."
}
```

### N447 — sheet-thickness

Source `rpt-mainline032-grok-wrinkle-waviness-1020`; original file `unpublished-local-ref:e20bd8d3e1ca97e2; pointer `/open/1`.

```json
{
  "id": "sheet-thickness",
  "tag": "QUESTIONABLE",
  "note": "Table II says the test thickness is 0.625 inch. The lead cores are 20.21 mm and 30.12 mm. Ec is typical only. No minimum modulus is printed."
}
```

### N530 — NFI-032-CHECK-THICKNESS

Source `rpt-ref-a30a669ed3e245f1473b`; original file `unpublished-local-ref:46e93c1ee5674acc; pointer `/findings/2`.

```json
{
  "id": "NFI-032-CHECK-THICKNESS",
  "status": "open",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "The table's compression data are from a 0.625 inch specimen.",
  "checked": "0.625 inch is 15.875 mm; the requested cores are 20.21 and 30.12 mm. No matching thickness/bonded-state validation was supplied.",
  "followup": "Retain QUESTIONABLE until relevant properties are measured or supported for the actual construction.",
  "source_audit_ids": [
    "HEXCEL-5056"
  ],
  "owner_nfi_ids": [
    "sheet-thickness"
  ]
}
```

### N627 — NFI-032-CHECK-THICKNESS

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/prior_032_findings_retained/2`.

```json
{
  "id": "NFI-032-CHECK-THICKNESS",
  "status": "open",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "The table's compression data are from a 0.625 inch specimen.",
  "checked": "0.625 inch is 15.875 mm; the requested cores are 20.21 and 30.12 mm. No matching thickness/bonded-state validation was supplied.",
  "followup": "Retain QUESTIONABLE until relevant properties are measured or supported for the actual construction.",
  "source_audit_ids": [
    "HEXCEL-5056"
  ],
  "owner_nfi_ids": [
    "sheet-thickness"
  ]
}
```

### C114 — NFI-029-HOMOGENIZATION

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/4`.

```json
{
  "id": "NFI-029-HOMOGENIZATION",
  "status": "open",
  "title": "Honeycomb continuum completion",
  "issue": "Only normalE and transverseGL/GW are sourced. InplaneE=.01MPa,G=.005MPa and zero core Poisson couplings are explicit regularizations. Actual cells, cell-scale dimpling, defects, adhesive, seams and debonding are absent. Increasing inplaneE/G100-fold to1/.5MPa changes accepted W linear eigenpressures by about0.0001% for021 and0.003% for021b; this limited sensitivity does not source the properties.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

## R024 — ultralight cores below about 16 kg/m3: no sourced material; scaled moduli are PROJECTION

**Original question:** No measured shear modulus at or below 10 kg/m3; G=E/2 is an assumption; figure reads, bulk-scale transfer and continuum validity unproved; 190 kg/m3 row passes locally only.

### N008 — NFI-CHECK013-LOWER-BOUNDS

Source `rpt-1228-mainline013-independent-check-1020`; original file `unpublished-local-ref:b1c8a108ddfdc4b1; pointer `retained original identity`.

```json
{
  "id": "NFI-CHECK013-LOWER-BOUNDS",
  "kind": "source semantics",
  "rows": [
    {
      "row": "basotect-gplus-datasheet",
      "field": "sigma_c_Pa / rows.B,Q.verdict",
      "card_value": 9000,
      "checker_value": ">9000 Pa, no upper bound supplied",
      "card_margin": 0.18855899857315267,
      "checker_margin": ">0.18855899857315267 at nominal input density; not an established physical failure",
      "card_verdict": "FAIL",
      "physical_evidence_verdict": "INCOMPLETE",
      "source": "sources/basotect.pdf p2"
    },
    {
      "row": "eps12-astm-d6817-spec",
      "field": "density_kg_m3 / sigma_c_Pa / status / rows.B,Q.verdict",
      "card_value": {
        "density": 11.2,
        "strength": 15000,
        "status": "MEASURED",
        "verdict": "FAIL"
      },
      "checker_value": {
        "density": "minimum 11.2 kg/m3",
        "strength": "minimum 15000 Pa at 1% strain",
        "status": "SPECIFICATION_MINIMUM",
        "physical_evidence_verdict": "INCOMPLETE"
      },
      "card_margin": 0.3142649976219211,
      "source": "sources/eps-spec.pdf pp4,30"
    }
  ],
  "issue": "The scalar screening ratios reproduce, but a lower bound below a demand does not establish that the actual material fails. Neither of these records supplies Ec or G. The data still establish no all-three pass.",
  "proposed_fix": "Preserve comparison operators/property basis and distinguish rejection of an insufficient guaranteed specification from measured failure; retain unknown physical outcomes.",
  "nonblocking": true,
  "halts_owner": false,
  "halts_next_card": false
}
```

### N011 — NFI-CHECK013-INHERITED-LIMITS

Source `rpt-1228-mainline013-independent-check-1020`; original file `unpublished-local-ref:b1c8a108ddfdc4b1; pointer `retained original identity`.

```json
{
  "id": "NFI-CHECK013-INHERITED-LIMITS",
  "kind": "carry",
  "row": "all core rows and ideal-lattice projection",
  "source": "inputs/NFI.json (17 owner rows)",
  "issue": "No measured G at or below 10 kg/m3; isotropic G=E/2 is an assumption, not a universal anisotropic bound. Figure reads, bulk-scale transfer, continuum/elastic validity and independent crush modelling remain unproved. The 190 kg/m3 row is a conditional local pass, while its global SF is 0.02035.",
  "proposed_fix": "Retain all original qualifications and the PROJECTION tag on every ideal-lattice application. A new material claim requires measured properties at its own density.",
  "nonblocking": true,
  "halts_owner": false,
  "halts_next_card": false
}
```

### N029 — NFI-DENSITY

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-DENSITY",
  "gap": "This card is the density trade NFI-DENSITY asked for. The least stated safety factor still rises as density falls through 1 kg/m3. There is no interior peak on 0.25 to 64 kg/m3.",
  "direction": "Do not treat 1 kg/m3 as a proved best density. No sourced structural core was retrieved there.",
  "effect": "The named-set high is 0.737028554512 at 1 kg/m3, still below 1. Buckling safety factor reaches 1 at 3.73369568197 kg/m3 and yield governs that point."
}
```

### N038 — NFI-CORE-FLOOR

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-CORE-FLOOR",
  "gap": "No catalog structural core with sourced Gc, Ec, and compressive strength was retrieved at 8, 6, 4, 3, 2, or 1 kg/m3.",
  "direction": "Do not extrapolate a honeycomb or foam modulus below the catalog floor.",
  "effect": "The low-density safety factors are geometry of the stated model, not a claim that a core exists."
}
```

### N040 — NFI-MICROLATTICE

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-MICROLATTICE",
  "gap": "Schaedler et al. 2011 place a nickel microlattice at or above 0.9 kg/m3. The open abstract has no usable modulus or strength.",
  "direction": "A later card can read the paper. This card does not invent the coefficient.",
  "effect": "No crush, crimp, or wrinkling margin is reported for it. A usable-core projection is not claimed."
}
```

### N046 — NFI-CORE-FLOOR

Source `rpt-ref-3dd5ab5528276031581d`; original file `unpublished-local-ref:474808f25f6dc0cd; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-CORE-FLOOR",
  "gap": "Densities 8 through 1 still have no sourced Gc and Ec. The Schaedler microlattice still has no modulus.",
  "direction": "Do not extrapolate a catalog modulus down to those densities.",
  "effect": "Those MAINLINE-007 safety factors are not revised."
}
```

### N138 — NFI-008B-CORE-NONE-LIGHT

Source `rpt-ref-cc9cef5e55adca018a8f`; original file `unpublished-local-ref:2bbb739a4c037482; pointer `retained original identity`.

```json
{
  "id": "NFI-008B-CORE-NONE-LIGHT",
  "issue": "The re-rank rows at 4 and 1 kg/m3 presume a structural core that does not exist today. MAINLINE-007 retrieved no catalog core with sourced shear modulus, compressive modulus and strength below 16 kg/m3 (Plascore lightest 16, ROHACELL IG-F starts 31, HexWeb lightest retrieved 24; Schaedler nickel microlattice 0.9 kg/m3 has no retrieved modulus or strength).",
  "consequence": "Every light-core row in this card is PROJECTION on the core side regardless of face material. The wrinkling comparison on those rows uses Ec*Gc products belonging to 24-38 kg/m3 cores, which cannot ride on a 1-4 kg/m3 row at any thickness near the mass ceiling (a 32 kg/m3 core at the 1 kg/m3 row's 0.1884 m thickness would alone mass about 7576 kg against a 4889 kg ceiling).",
  "next": "Source or project an ultra-light core with a stated Ec*Gc product and strength; until then the light-core readings measure the core gap, not a build."
}
```

### N155 — NFI-013-WRINKLE-PRODUCT

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-WRINKLE-PRODUCT",
  "binds": true,
  "issue": "No measured core at or below 10 kg/m3 meets the wrinkling need with 6061 faces on the P2 float ceiling.",
  "numbers": "Best measured: meza2014-hollow-alumina-octet-lightest-E at 5.5 kg/m3, Ec*Gc margin 0.000171 on the least-factor split (gap 5.84e+03, 18 on stress; 1.66e+03 at the classical 0.76), gap 1.7e+04 on the buckling split. Band 1-4 kg/m3: kashani2019-npg-3-tension, gap 7.57e+04 (2.16e+04 classical).",
  "closes_when": "a measured core's Ec*Gc at its own density meets the need on its row; or a face change lowers the need, which scales as sigma_face^3/E_face (008b's face table); or a wrinkling test on a representative sandwich replaces the CR-1457 design coefficient."
}
```

### N156 — NFI-013-SHEAR-UNMEASURED

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-SHEAR-UNMEASURED",
  "issue": "No source measured a transverse shear modulus for any core at or below 10 kg/m3.",
  "numbers": "Gc is DERIVED as Ec/2 (isotropic, nu = 0, the optimistic bound) for every non-honeycomb core; at nu = 1/3 every product falls by 0.75 and every crimp margin by 0.75. Si et al. 2014 measured shear stress at 9.6 kg/m3 but printed no modulus.",
  "closes_when": "a plate-shear or sandwich-beam shear modulus is measured on a candidate core."
}
```

### N157 — NFI-013-CRIMP

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-CRIMP",
  "issue": "On the least-factor split no measured core at or below 10 kg/m3 reaches the crimp shear modulus.",
  "numbers": "Need 2.52e+06 Pa at 1 to 9.6 kg/m3; best meza2014-hollow-alumina-octet-lightest-E margin 0.735 (gap 1.36) on the derived Gc. On the buckling split three alumina lattice points pass (0.3, 5.3, 5.5 kg/m3), the 0.3 point on a 6 m core.",
  "closes_when": "a measured Gc above the need on the row the design uses."
}
```

### N158 — NFI-013-STRENGTH-BASIS

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-STRENGTH-BASIS",
  "issue": "Most ultralight strengths are not crush strengths: stress at 80 percent strain (Qiu 2012), undefined 'max stress' (Si 2014), ultimate stress of undefined strain (Xu 2019), 40 percent compression (Basotect), indentation or tension (Kashani 2019). These can fail the crush check but never pass it.",
  "numbers": "The only structural pass at or below 10 kg/m3 is meza2015-hier-hollow-alumina-heaviest-halfcell at 5.3 kg/m3, margin 1.34, read by eye from a plot (about 25 percent) with its density inferred from relative density times 2900 kg/m3.",
  "closes_when": "a small-strain collapse or yield strength is measured at the candidate density."
}
```

### N159 — NFI-013-MID-DENSITY

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-MID-DENSITY",
  "issue": "This card sourced no core between 53 and 190 kg/m3, so the lightest core passing all three is bounded, not found.",
  "numbers": "The only pass is jacobsen2011-vitreous-carbon-octet-0p19 at 190 kg/m3 (secondary source); at that density the float-ceiling core is 9.2 mm thick and the shell's buckling SF is 0.0204 at kd 0.2.",
  "closes_when": "mid-density cores are sourced (for example high-density PMI foams, end-grain balsa, carbon micro-lattices from 50 to 190 kg/m3) and run through compute.py."
}
```

### N162 — NFI-013-CONTINUUM-AND-DIMPLING

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-CONTINUUM-AND-DIMPLING",
  "issue": "The continuum wrinkling form assumes a core finer than the wrinkle wavelength; lattice cell sizes were not sourced. Intracell dimpling, a fourth local mode outside the card's three, is reported beside them.",
  "numbers": "CR-1457 eq 2.1-4 with the straight-line biaxial rule allows cells up to 3.52 mm above 9.6 kg/m3 and up to 9.84 mm on the least-factor split at 0.1 kg/m3; every honeycomb cell in the table fails it except the 1/8-inch (1.11).",
  "closes_when": "cell sizes are sourced and a wrinkling model valid at that cell scale is applied."
}
```

### N163 — NFI-013-HONEYCOMB-FORM

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-HONEYCOMB-FORM",
  "issue": "CR-1457 eq 2.2-14 at these core-to-face ratios (tc/tf about 220 to 560) is far outside its test data; it makes the honeycomb need an Ec no honeycomb has.",
  "numbers": "Ec needed 1.03e+10 to 7.74e+10 Pa; best honeycomb margin 0.00462 (gap 216).",
  "closes_when": "a symmetric-wrinkling model or test for very thick honeycomb cores, or a honeycomb with a stabilising foam fill."
}
```

### N166 — NFI-013-IDEAL-LATTICE

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-IDEAL-LATTICE",
  "tag": "PROJECTION",
  "issue": "The ideal stretch-dominated lattice (Ashby 2006 eq 5.1, Gc = Ec/2) is a bound, not a material; strength is not projected because no strut-buckling constant was sourced.",
  "numbers": "Passes wrinkling and crimp on the least-factor split from 1.34 (K13D2U-grade), 2.46 (CNT yarn), 4.82 (beryllium), 25.3 (alumina), 55.9 kg/m3 (6061). At 5 kg/m3 a lattice needs 0.378, 0.628 and 0.982 of ideal; measured alumina lattices reach 0.0279 to 0.0422.",
  "closes_when": "a lattice of a fibre-grade strut material is built and measured at 1 to 8 kg/m3."
}
```

### N170 — NFI-013-SCALE-AND-ENVIRONMENT

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-SCALE-AND-ENVIRONMENT",
  "issue": "Every lattice and aerogel in this table was tested as a laboratory specimen (micrometres to centimetres); the float-ceiling core is about 1257 m2 by 0.19 m. The commercial foams (EPS, melamine, polyimide) are made at larger scale but fail the checks by orders of magnitude. Vacuum outgassing, creep under a sustained p/2 (polymer foams), and temperature were not assessed.",
  "numbers": "No lattice or aerogel source here reports a manufacturing route at metre scale.",
  "closes_when": "a manufacturing route at metre scale is sourced for a candidate core."
}
```

### N262 — NFI-DENSITY

Source `rpt-mainline003-grok-p2-targets-1019`; original file `unpublished-local-ref:c644022670e558c3; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-DENSITY",
  "gap": "All three points keep the inherited core density of 16 kg/m3. The advisory lower-density leads were not given a point.",
  "direction": "A later card can spend one of three points on a named lower density.",
  "effect": "A lighter core leaves more of the ceiling for faces or for a thicker core."
}
```

### N273 — NFI-DENSITY

Source `rpt-mainline004-grok-knockdown-card-1019`; original file `unpublished-local-ref:bd4eb9f1634108a4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-DENSITY",
  "gap": "Lower core density stays deferred. This unit adds no density point.",
  "direction": "Leave it to a later card.",
  "effect": "None inside these four rows."
}
```

### N295 — NFI-DENSITY

Source `rpt-mainline007-check-lead4f19-1019`; original file `unpublished-local-ref:a0b67c87ff180a29; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-DENSITY",
  "gap": "Confirmed: least SF rises as density falls through the named set, peaking at 1 kg/m3 (0.7370285545124737), and my 0.25-64 kg/m3 scan has no interior peak (0.7672968655351241 at 0.25). No sourced structural core was retrieved at 1-8 kg/m3.",
  "direction": "Do not treat 1 kg/m3 as a proved best density.",
  "effect": "Owner statement stands."
}
```

### N304 — NFI-CORE-FLOOR

Source `rpt-mainline007b-check-lead4f19-1019`; original file `unpublished-local-ref:c88bee0b56cece84; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-CORE-FLOOR",
  "gap": "Confirmed: densities 8-1 have no sourced Gc/Ec and are not revised; the microlattice has no modulus and no SF.",
  "direction": "Do not extrapolate catalog moduli downward.",
  "effect": "Owner statement stands."
}
```

### N323 — NFI-SCALE

Source `rpt-mainline014-grok-balanced-sandwich-1019`; original file `unpublished-local-ref:8c5f980fe25f9829; pointer `retained original identity`.

```json
{
  "id": "NFI-SCALE",
  "note": "Densities 16, 8 and 4 have no fully sourced core in MAINLINE-007. Ec and Gc scale as rho^2 and crush strength as rho^1.5 from the 32 kg/m3 sourced row. PROJECTION."
}
```

### N324 — NFI-013

Source `rpt-mainline014-grok-balanced-sandwich-1019`; original file `unpublished-local-ref:8c5f980fe25f9829; pointer `retained original identity`.

```json
{
  "id": "NFI-013",
  "note": "MAINLINE-013 has not filed. Its cores are not used."
}
```

### N332 — NFI-SCALE

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-SCALE",
  "note": "The 014 projections at 16, 8 and 4 kg/m3 stay in the set. Moduli scale as rho^2 and crush as rho^1.5. The scaled aramid keeps the parent 4.8 mm cell."
}
```

### N333 — NFI-013

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-013",
  "note": "MAINLINE-013 has not filed. Its cores are not used."
}
```

### C098 — NFI-037b-NONMETAL-CTE

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/9`.

```json
{
  "id": "NFI-037b-NONMETAL-CTE",
  "tag": "PROJECTION",
  "claim": "Hexcel prints only thickness-direction expansion for glass and aramid cores; their in-plane values are proxies here. The carbon core UCF-145 (12.8 kg/m3, second-hand shear data, W strength 97 kPa) has no sourced in-plane expansion or compressive modulus and is not priced.",
  "needed_to_ground": "In-plane expansion and compressive data for candidate non-metallic cores."
}
```

### C195 — NFI-037b-NONMETAL-CTE

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/9`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-NONMETAL-CTE",
  "tag": "PROJECTION",
  "claim": "Hexcel prints only thickness-direction expansion for glass and aramid cores; their in-plane values are proxies here. The carbon core UCF-145 (12.8 kg/m3, second-hand shear data, W strength 97 kPa) has no sourced in-plane expansion or compressive modulus and is not priced.",
  "needed_to_ground": "In-plane expansion and compressive data for candidate non-metallic cores."
}
```

## R025 — 30:1 adhesive scarf seam

**Current 030c:** Selected scarf ratio is 30.341397:1 with 037b's 200 F panel cure, conditional 10 MPa screen and +.120151 kg joining allowance. As-designed 250 F/30:1 requires gamma .618429, beyond its named stretch, and free-edge minimum-strength factor .833325. 042 proposes a distinct room-temperature seam process that remains unqualified. CHECK-037b reproduces the selected numbers but does not qualify2U/Be/honeycomb low-cure transfer. 044's combined-load scarf screen falls to.9891 on its R10fix scenario.

**030b source history:** CHECK-028b confirms the nominal/primer screen and no-singleton result. The 10 MPa mean-shear screen, corresponding to 300.333 MPa face stress at 30:1, remains a projection; peel and installed capacity are unknown.

**Original question:** Thin Be/Be scarf performance is untested; the 10 MPa shear screen is selected, not qualified.

### N228 — NFI-028-07

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-07",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Thirty-to-one adhesive scarf",
  "today_value": "25.303-mm run; 70-g/m2 seam film; 9.421 MPa average shear; screen 10 MPa is selected, not qualified",
  "required_or_budget_target": {
    "total_seam_kg_m": 0.010597793381544554,
    "max_seam_kg_m_after_AF015": 0.011365897456349418
  },
  "needed_evidence": "Thin Be/Be scarf compression, biaxial transfer, peel/end effects, cyclic and local buckling data at actual film weight.",
  "scenario": "af015_scarf",
  "scenario_joining_kg": 214.2399978421616,
  "factor_to_216_427kg_allowance": 0.9898943034693449,
  "mass_reduction_factor_to_fit": 1
}
```

### N422 — NFI-028-SHEAR-SCREEN

Source `rpt-ref-68dff0680696fe9b4cb4`; original file `unpublished-local-ref:5ac789d6de7269e0; pointer `/rows/1`.

```json
{
  "id": "NFI-028-SHEAR-SCREEN",
  "issue": "The 30:1 scarf average shear is 9.421138296 MPa. The 10 MPa screen is owner-selected. Its factor at the frozen geometry is 1.061442862. No qualified allowable for this beryllium scarf was in the pinned sources.",
  "consequence": "The shear arithmetic matches. The screen is not a certification. The card already says so.",
  "next": "A measured scarf allowable for this face, film and thickness."
}
```

### N434 — NFI-028b-scarf10

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/10`.

```json
{
  "id": "NFI-028b-scarf10",
  "status": "OPEN",
  "issue": "Measure mean-shear allowable and peel/compression failure of the exact scarf; 10 MPa is assumed.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "average_shear_Pa": 10000000.0,
    "ratio": 30,
    "total_skin_seams_m": 5683.037087839708
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "MAINLINE-028 owner screen"
}
```

### N497 — NFI-CHECK-028B-SEAM-SCREEN

Source `rpt-ref-aae116a5fcd787ed9abc`; original file `unpublished-local-ref:b1574c3b91d41b2e; pointer `/rows/0`.

```json
{
  "id": "NFI-CHECK-028B-SEAM-SCREEN",
  "status": "scope",
  "note": "The 0.97197751743 and 0.996075 usages are set by the assumed 10 MPa scarf-shear screen, which caps face stress at 300.333333 MPa. That screen is not a measured beryllium scarf allowable. The laboratory 0.651468543105 usage is the same with the screen off, because the ideal weld is scored as parent face compression."
}
```

### N548 — NFI-036-scarf

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/10`.

```json
{
  "id": "NFI-036-scarf",
  "status": "OPEN",
  "issue": "Qualify the assumed scarf compression/shear/peel capacity.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "ratio": 30,
    "mean_shear_screen_MPa": 10
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "028b",
  "closure": "Exact Be/adhesive/core process testing under equal compression, including peel and local buckling."
}
```

### N613 — NFI-017b-SCARF

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/13`.

```json
{
  "id": "NFI-017b-SCARF",
  "tag": "PROJECTION",
  "claim": "The scarf is steepened beyond 30:1 to meet 028's 10 MPa average-shear screen, which is owner-selected, not an allowable; bond and seam strengths are unmeasured (028's rows).",
  "needed_to_ground": "028's evidence needs: a weighed, load-tested curved Be/Al panel."
}
```

### N656 — NFI-038-SEAM_MODES

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/5`.

```json
{
  "id": "NFI-038-SEAM_MODES",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Mean shear does not qualify peel, cyclic debond or local instability",
  "evidence": "028b lists unquantified seam/core modes.",
  "resolution_needed": "Instrument production scarf and welded alternatives; retain failure locations and leak changes.",
  "tests": [
    "T2"
  ]
}
```

### N699 — NFI-036-scarf

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/10`.

```json
{
  "id": "NFI-036-scarf",
  "status": "OPEN",
  "issue": "Qualify the assumed scarf compression/shear/peel capacity.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "ratio": 30,
    "mean_shear_screen_MPa": 10
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "028b",
  "closure": "Exact Be/adhesive/core process testing under equal compression, including peel and local buckling.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### C010 — CHECK033-NFI-01

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/0`.

```json
{
  "id": "CHECK033-NFI-01",
  "inherited_id": "033-NFI-01",
  "tag": "PROJECTION",
  "title": "Installed joints remain unqualified",
  "finding": "The six-mode shell result excludes scarf, peel and face/core bond capacities. The additional 10 MPa average-shear screen caps face stress at 300.333 MPa, but is not a qualified allowable. All installed-hull SF values remain null.",
  "next_evidence": "Measure compression/scarf/bond/peel capacity of the actual SR-200, AF163-2U, primer and honeycomb process, including seam imperfections and environmental conditioning.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Retained physical/model limitation. Arithmetic reproduction does not establish an installed-hull allowable."
}
```

### C034 — N039-13

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/12`.

```json
{
  "id": "N039-13",
  "issue": "The seam screen decides feasibility",
  "detail": "028's 10 MPa mean shear on a 30:1 scarf (300.333 MPa face stress) keeps every stiffened version from SF 1. A 40:1 scarf would cap at 400 MPa for about +3 kg of film. It is not evaluated as a route, because 028b's routes are fixed.",
  "to_close": "A seam card if stiffening is pursued.",
  "tag": "QUESTIONABLE"
}
```

### C092 — NFI-037b-SCARF

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/3`.

```json
{
  "id": "NFI-037b-SCARF",
  "tag": "PROJECTION",
  "claim": "028b's fixed 30:1 scarf binds at its projected 10 MPa screen, so the cure compression costs usage (0.972 to 1.052); 028's sizing rule restores it at 30.44:1 for 0.16 kg. The 10 MPa screen is not a measured Be scarf allowable, and a filled core splice at the scarf may change the local face stress.",
  "needed_to_ground": "A measured Be scarf allowable and the splice-at-scarf detail."
}
```

### C093 — NFI-037b-028B-SCARF-LEVER

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/4`.

```json
{
  "id": "NFI-037b-028B-SCARF-LEVER",
  "tag": "QUESTIONABLE",
  "claim": "028b's faces are pinned by its fixed 30:1 scarf. Without any cure compression a 30.44:1 scarf would let them thin, to usage 0.894. 028b gives no reason for fixing 30:1, such as machining, overlap, peel or panel-edge limits. This card notes the lever and does not take it.",
  "needed_to_ground": "028b's owner states why the scarf is fixed at 30:1, or re-runs the least set with the scarf ratio free."
}
```

### C171 — 040-09-scarf

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/8`.

```json
{
  "id": "040-09-scarf",
  "tag": "PROJECTION",
  "open_issue": "The 10 MPa mean-shear screen and worst-direction thermal addition do not resolve scarf peel, voids or intersections.",
  "grounding": "Weigh and load/leak-test full process scarf intersections under thermal cycling."
}
```

### C189 — NFI-037b-SCARF

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/3`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-SCARF",
  "tag": "PROJECTION",
  "claim": "028b's fixed 30:1 scarf binds at its projected 10 MPa screen, so the cure compression costs usage (0.972 to 1.052); 028's sizing rule restores it at 30.44:1 for 0.16 kg. The 10 MPa screen is not a measured Be scarf allowable, and a filled core splice at the scarf may change the local face stress.",
  "needed_to_ground": "A measured Be scarf allowable and the splice-at-scarf detail."
}
```

### C190 — NFI-037b-028B-SCARF-LEVER

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/4`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-028B-SCARF-LEVER",
  "tag": "QUESTIONABLE",
  "claim": "028b's faces are pinned by its fixed 30:1 scarf. Without any cure compression a 30.44:1 scarf would let them thin, to usage 0.894. 028b gives no reason for fixing 30:1, such as machining, overlap, peel or panel-edge limits. This card notes the lever and does not take it.",
  "needed_to_ground": "028b's owner states why the scarf is fixed at 30:1, or re-runs the least set with the scarf ratio free."
}
```

### C233 — NFI-044-HEXBOND-SCARF

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/9`.

```json
{
  "id": "NFI-044-HEXBOND-SCARF",
  "finding": "The face scarf uses HexBond312, a separate adhesive. Its 10 MPa screen is static and unsourced for this Be joint. No applicable S-N or crack-growth data were obtained.",
  "evidence_needed": "30:1 and proposed 60:1 Be scarf fatigue and sustained-load tests including peel, roots, manufacturing flaws, leak integrity and repairs."
}
```

### C235 — NFI-044-COMBINED-SCARF

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/11`.

```json
{
  "id": "NFI-044-COMBINED-SCARF",
  "finding": "Adding the inherited local thermal envelope to 037b's cured point takes the scarf below its static screen. The extrema are conservative and not time-correlated.",
  "evidence_needed": "A complete combined-load, layer-resolved scarf/face/core solution and strain measurements at critical locations."
}
```

### S005 — NFI-030C-SEAM-PROCESS

Source `rpt-1228-mainline030c-design-register-1020`; original file `unpublished-local-ref:3c01fd6db28be861; pointer `/rows/4`.

```json
{
  "id": "NFI-030C-SEAM-PROCESS",
  "title": "042 changes the in-place seam process without qualifying its mass and strength.",
  "finding": "Its 200 F panel bond and proposed room-temperature Be scarf are distinct cures. Do not transfer AF film weight or the 10 MPa scarf screen to the proposed seam paste as measured capability. F1 expands the existing T2 evidence route; it does not certify gamma.",
  "status": "OPEN",
  "blocks_progress": false,
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## R026 — adhesive-free diffusion interface

**Original question:** Zero added filler is an ideal limit; the replacement core density and strength are unknown.

### N227 — NFI-028-06

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-06",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Diffusion/integral adhesive-free interface",
  "today_value": "0 added filler is an ideal limit; replacement core mass and strengths unknown",
  "required_or_budget_target": "Provide a complete installed bill and measured structure, not just zero adhesive.",
  "needed_evidence": "New core density/stiffness/strength, processing pressure and post-process interface performance.",
  "factor_to_216_427kg_allowance": null,
  "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."
}
```

## R027 — bond film areal weight and coverage (0.015 to 0.060 lb/ft2)

**030b source history:** The .015lb/ft2 film in028b/033 is a fixed2× mass reduction from.030, not a proven assembly. CHECK-028 reports a weight tolerance;033 did not independently establish it. CHECK-036 identifies an unused olderR20 .015 label but governing.146472829kg/m2=.030lb/ft2 field; the old027 calculations use.030 correctly. Keep the two models distinct.

**Original question:** Matching Be/core strength and stiffness at the lowest-weight reticulated film weight are unmeasured; hull adoption is a projection.

### N206 — NFI-021b-FILM

Source `rpt-ref-1080d4f6a1af4cfa8c67`; original file `unpublished-local-ref:4edbd73193c8c843; pointer `retained original identity`.

```json
{
  "id": "NFI-021b-FILM",
  "optimism": "O5",
  "needed_lb_ft2": 0.03,
  "today_lb_ft2": 0.03,
  "full_lb_ft2": 0.015,
  "usage": 0.0,
  "state": "not needed at the floating point",
  "note": "Be/honeycomb bond suitability of any AF 163 weight is unqualified (019, 020)."
}
```

### N222 — NFI-028-01

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-01",
  "status": "OPEN",
  "tag": "QUESTIONABLE",
  "technology_state": "exists_today",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Lowest-weight reticulated film performance",
  "today_value": "AF163-2U 73.236 g/m2 exists; no matching flatwise/core-shear result",
  "required_or_budget_target": {
    "maximum_g_m2_with_modeled_stock_scarf": 74.10665270534186
  },
  "needed_evidence": "Weigh installed cured film and obtain Be/selected-core strength, stiffness and defect performance at this weight. Reticulation is not an open-area mass discount.",
  "scenario": "af015_scarf",
  "scenario_joining_kg": 214.2399978421616,
  "factor_to_216_427kg_allowance": 0.9898943034693449,
  "mass_reduction_factor_to_fit": 1
}
```

### N223 — NFI-028-02

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-02",
  "status": "OPEN",
  "tag": "QUESTIONABLE",
  "technology_state": "exists_today",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Film weight tolerance",
  "today_value": "Manufacturer +/-0.005 lb/ft2",
  "required_or_budget_target": {
    "nominal_kg": 214.2399978421616,
    "upper_weight_kg": 275.5943930187407
  },
  "needed_evidence": "Lot areal-mass distribution and cured retained mass; prove low tail still bonds and high tail floats.",
  "scenario": "af020_tolerance_scarf",
  "scenario_joining_kg": 275.5943930187407,
  "factor_to_216_427kg_allowance": 1.2733818262933878,
  "mass_reduction_factor_to_fit": 1.2733818262933878
}
```

### N224 — NFI-028-03

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-03",
  "status": "OPEN",
  "tag": "QUESTIONABLE",
  "technology_state": "exists_today",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Low-weight fillet-forming catalogue film",
  "today_value": "HexBond312: 70 g/m2 lap shear 37 MPa on Al; its flatwise column is blank. 100 g/m2 has 5.4 MPa on a different sandwich.",
  "required_or_budget_target": {
    "70gsm_complete_kg": 206.10600091345282,
    "100gsm_complete_kg": 281.5042245996078
  },
  "needed_evidence": "Do not move the 100-g/m2 result into the 70-g/m2 column; test the actual assembly.",
  "scenario": "hex100_scarf",
  "scenario_joining_kg": 281.5042245996078,
  "factor_to_216_427kg_allowance": 1.3006881587956576,
  "mass_reduction_factor_to_fit": 1.3006881587956576
}
```

### N437 — NFI-028b-AF015-bond

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/13`.

```json
{
  "id": "NFI-028b-AF015-bond",
  "status": "OPEN",
  "issue": "Published weight exists; matched Be/low-density-aluminium-core bond strength and stiffness are unknown.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "film_lb_ft2": 0.015,
    "weight_per_line_kg_m2": 0.07323641454574575
  },
  "today": {
    "old_film_lb_ft2": 0.03
  },
  "improvement_factor": 2,
  "null_factor_reason": null,
  "source": "https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf",
  "fixed_O5_usage": 1
}
```

### N655 — NFI-038-BOND_MASS

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/4`.

```json
{
  "id": "NFI-038-BOND_MASS",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Thin film, primer and repairs have no demonstrated installed mass",
  "evidence": "028b nominal route has no unused joining allowance.",
  "resolution_needed": "Weigh staged actual-process components; apply area/length/crossing model once.",
  "tests": [
    "T2"
  ]
}
```

### N704 — CHECK036-D1

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/15`.

```json
{
  "id": "CHECK036-D1",
  "status": "OPEN",
  "tag": "QUESTIONABLE",
  "issue": "Inherited R20 film label differs by a factor of two from the governing mass field.",
  "source": "MISMATCHES.json",
  "closure": "Label the 0.015 lb/ft2 field as legacy or reconcile it with the explicitly governing 0.1464728290914915 kg/m2 per interface.",
  "impact": "Documentation ambiguity; all current calculations use the governing mass field."
}
```

### C016 — CHECK033-NFI-07

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/6`.

```json
{
  "id": "CHECK033-NFI-07",
  "inherited_id": "033-NFI-07",
  "tag": "PROJECTION",
  "title": "Nominal adhesive and seam inventory",
  "finding": "Nominal film is .015 lb/ft2 per face/core interface; scarf film .07 kg/m2, splice gap .5 mm at 500 kg/m3, sealing .002 kg/m for both faces. Nominal primer is zero. No AF163 mass tolerance was independently verified; the inherited +/- .005 statement is unused.",
  "next_evidence": "Obtain an installed bill including primer, intersections, closeouts, rejected material, repairs and leak barriers; qualify sustained load, thermal cycling and leakage.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Retained physical/model limitation. Arithmetic reproduction does not establish an installed-hull allowable."
}
```

### C167 — 040-05-bond_strength

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/4`.

```json
{
  "id": "040-05-bond_strength",
  "tag": "QUESTIONABLE",
  "open_issue": "Film weights do not establish adhesive shear, peel, flatwise tension, fatigue or leakage on Be/5056.",
  "grounding": "Test the exact film, primer, surface treatment, cure and honeycomb geometry."
}
```

### C184 — 040-22-film_interpolation

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/21`.

```json
{
  "id": "040-22-film_interpolation",
  "tag": "PROJECTION",
  "open_issue": "Intermediate film weights rank optimism but are not necessarily available or qualified resin systems.",
  "grounding": "Choose an available process and demonstrate both installed weight and bond/leak performance."
}
```

### C215 — NFI-CHECK037b-HEX679-SUPPORT

Source `rpt-ref-4bf25e71ae0c2ca315e2`; original file `unpublished-local-ref:0360eb0aa78daa3e; pointer `/items/0`.

```json
{
  "id": "NFI-CHECK037b-HEX679-SUPPORT",
  "tag": "CORRECTION",
  "status": "OPEN",
  "finding": "HexBond 679 was priced using 250 g/m2 resin while its separate 30 g/m2 support was omitted at both interfaces.",
  "exact": {
    "owner_increment_kg": 444.25534518822144,
    "corrected_increment_kg": 519.6535688743766,
    "omitted_kg": 75.39822368615503,
    "corrected_classical_maximum_minimum_SF": 0.9162604110157426
  },
  "disposition": "Correction already re-solved in this check; replace the owner's mass line when reconciling the card. It remains rejected.",
  "evidence": "EVIDENCE.md; DERIVED.json/hexbond_support_correction; primary HexBond 679 p.1",
  "blocking": false
}
```

### C232 — NFI-044-AF163-015U

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/8`.

```json
{
  "id": "NFI-044-AF163-015U",
  "finding": "3M lap runouts and thicker supported-film failure curves do not qualify the actual 0.015 lb/ft2 U-film Be/core joint or the 200F cycle. Gross-area shear masks the sparse core-foot contact: a no-fillet area sensitivity gives 27.0 MPa at the 200F cold edge; effective fillet/contact area is not known.",
  "evidence_needed": "Actual-film, actual-substrate shear/peel/mixed-mode fatigue, process repeatability and environmental retention, with weighed fillets/primer."
}
```

## R028 — brazed scarf seam

**Original question:** Al-Si braze shear is a typical value, not an allowable; thin-sheet joint distribution, fatigue and distortion unknown.

### N230 — NFI-028-09

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-09",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Brazed scarf seam",
  "today_value": "Materion Al-Si typical average shear 103.4 MPa; assumed 3:1 scarf needs 84.884 MPa; 50-um filler gap",
  "required_or_budget_target": {
    "mean_shear_ratio_available_to_required": 1.218126436982413,
    "face_filler_kg_m": 0.0007201485650694222
  },
  "needed_evidence": "Thin-sheet joint distribution, compressive/peel fatigue, distortion and final closure sequence; source typical is not an allowable.",
  "scenario": "lab8_braze_scarf",
  "scenario_joining_kg": 41.54621864151882,
  "factor_to_216_427kg_allowance": 0.1919639916829661,
  "mass_reduction_factor_to_fit": 1
}
```

## R029 — butt-strap seam route

**Original question:** Butt-strap bending, peel and strip buckling are unmeasured; this route is 2.88x over the joining allowance.

### N229 — NFI-028-08

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-08",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Butt-strap seam",
  "today_value": "47.730-mm width per face under a 10-MPa mean-shear screen; 0.162691 kg/m including closure",
  "required_or_budget_target": "Carry 238.652 kN/m per face including eccentricity.",
  "needed_evidence": "Measured local bending/peel, strip buckling and a mass-accounted symmetric alternative.",
  "scenario": "hex70_strap",
  "scenario_joining_kg": 623.092652861521,
  "factor_to_216_427kg_allowance": 2.8789949300486715,
  "mass_reduction_factor_to_fit": 2.8789949300486715
}
```

## R030 — core splice allowance

**Original question:** Installed core splice mass and its ability to transmit core shear are unknown.

### N232 — NFI-028-11

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-11",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Core splicing allowance",
  "today_value": "Selected 0.5-mm gap and 500 kg/m3 cured filling density; installed value unknown",
  "required_or_budget_target": {
    "modeled_kg_m": 0.005053344096872905
  },
  "needed_evidence": "Weighed edge splice transmitting core shear with actual gaps, nodes and intersections.",
  "scenario": "af015_scarf",
  "scenario_joining_kg": 214.2399978421616,
  "factor_to_216_427kg_allowance": 0.9898943034693449,
  "mass_reduction_factor_to_fit": 1,
  "modeled_component_kg": 14.389204513742502,
  "component_fraction_of_allowance": 0.06648521155280727
}
```

### N441 — NFI-028b-splice-and-seal

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/17`.

```json
{
  "id": "NFI-028b-splice-and-seal",
  "status": "OPEN",
  "issue": "Weigh and qualify the core splice, seals and intersection details.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "core_gap_m": 0.0005,
    "splice_density_kg_m3": 500,
    "seal_kg_per_hull_m": 0.002
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "MAINLINE-028 mass assumptions"
}
```

### C094 — NFI-037b-SPLICE

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/5`.

```json
{
  "id": "NFI-037b-SPLICE",
  "tag": "PROJECTION",
  "claim": "Whether 028's filled 0.5 mm core splice carries the core's in-plane force (no free edge) is not shown; the fill's modulus and its bond to the cut cell walls are unsourced.",
  "needed_to_ground": "Splice-fill properties and a splice coupon in in-plane tension."
}
```

### C191 — NFI-037b-SPLICE

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/5`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-SPLICE",
  "tag": "PROJECTION",
  "claim": "Whether 028's filled 0.5 mm core splice carries the core's in-plane force (no free edge) is not shown; the fill's modulus and its bond to the cut cell walls are unsourced.",
  "needed_to_ground": "Splice-fill properties and a splice coupon in in-plane tension."
}
```

## R031 — core-to-face brazing route

**Original question:** No structural data for brazing a Be face to the selected 16 kg/m3 Al core exist; coated CRIII properties may not carry over.

### N226 — NFI-028-05

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-05",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Core-to-face brazing",
  "today_value": "Generic Be brazing exists; no selected Be/16-kg/m3-Al-core structural data found",
  "required_or_budget_target": {
    "geometric_filler_g_m2": [
      5.6692913386,
      22.6771653543
    ],
    "fillet_leg_mm": [
      0.1,
      0.2
    ]
  },
  "needed_evidence": "Qualify wetting, residual stress and bare/metal-node core after joining. Do not retain coated H-39 CRIII properties without evidence.",
  "factor_to_216_427kg_allowance": null,
  "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill.",
  "modeled_component_kg": 14.248483216281267,
  "component_fraction_of_allowance": 0.06583500985313998
}
```

## R032 — electron-beam seam retention

**Original question:** Thin-sheet Be EB seam compression retention is unknown; 100 percent retention is a projection and 80 percent a sensitivity.

### N231 — NFI-028-10

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-10",
  "status": "OPEN",
  "tag": "QUESTIONABLE",
  "technology_state": "exists_today",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Electron-beam seam retention",
  "today_value": "Be EB process exists; matching thin-sheet compression evidence unknown. 100% retention is a projection; 80% is a sensitivity.",
  "required_or_budget_target": {
    "required_retention_at_original_gauge": 0.9998169145727672,
    "SF_with_assumed_80pct_reoptimized": 0.8529780485063345
  },
  "needed_evidence": "Establish weld/HAZ compression, ductility, full penetration, distortion and leak integrity; account reinforcement/repair mass.",
  "scenario": "lab8_eb_eta1",
  "scenario_joining_kg": 39.492661922586976,
  "factor_to_216_427kg_allowance": 0.18247554826252008,
  "mass_reduction_factor_to_fit": 1
}
```

### N440 — NFI-028b-lab-weld

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/16`.

```json
{
  "id": "NFI-028b-lab-weld",
  "status": "OPEN",
  "issue": "Ground parent compression retention, HAZ, brittle seam failure, distortion and final-hull access.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "retention_needed_at_selected_point": 0.9321170747737014,
    "retention_assumed": 1.0,
    "filler_mass_assumed_kg": 0
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "MAINLINE-028 ideal autogenous seam"
}
```

### N549 — NFI-036-lab-bond-weld

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/11`.

```json
{
  "id": "NFI-036-lab-bond-weld",
  "status": "OPEN",
  "issue": "Qualify the 8 g/m2 bond and weld strength retention.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "bond_each_interface_g_m2": 8,
    "assumed_weld_retention": 1
  },
  "today": {
    "matched_hull_bond_weld_properties": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "028b",
  "closure": "Matched bonded/welded thin-sheet specimens; HAZ, brittle failure, debonding, fatigue and leak integrity."
}
```

### N700 — NFI-036-lab-bond-weld

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/11`.

```json
{
  "id": "NFI-036-lab-bond-weld",
  "status": "OPEN",
  "issue": "Qualify the 8 g/m2 bond and weld strength retention.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "bond_each_interface_g_m2": 8,
    "assumed_weld_retention": 1
  },
  "today": {
    "matched_hull_bond_weld_properties": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "028b",
  "closure": "Matched bonded/welded thin-sheet specimens; HAZ, brittle failure, debonding, fatigue and leak integrity.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

## R033 — P2 seam and bond mass and capacity on the hull (016, 019, 020, 021b, 027, 028)

**030b source history:** 028b nominal/primer joining at the reoptimized R10 points is 215.742/227.880 kg, not the old frozen 214.240/226.806 kg. 033 main account charges actual joining; its comparison retains the unused 5% floor. Joint strengths remain unknown.

**Original question:** Net-section efficiencies are assumed screens applied only to compression; the enhanced aluminium optimum is joint-limited and no joint buckling, shear or peel allowables exist.

### N057 — NFI-016-SEAM

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-SEAM",
  "rank": 1,
  "gap": "Joint and seam mass at the 009 SiC point: 89.2 to 3004.3 kg across panel sizes 4 m to 0.25 m, against the 216.427 kg five percent allowance. Only 4 m panels, which do not exist in SiC today (PROJECTION), fit; today's 0.5 m Hexoloy plate size is 330 to 694 percent of the allowance; conservative 0.25 m tiling leaves the hull 966 to 2543 kg heavy.",
  "direction": "Pin the real maximum Hexoloy SA plate size from the manufacturer, and produce a seam parts list (doubler, adhesive, core splice) for a named panel size; or re-run the point on a face family whose sheet widths are 2 to 4 m today (aluminium, CFRP layup).",
  "effect": "Decides alone whether the 009 point floats; up to 1388 percent of the joint allowance."
}
```

### N072 — NFI-019-JOINTS

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-JOINTS",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "Two face strips, their bond lines, core splice and full-area face/core adhesive are now counted. Strip sizing and .015/.030 lb/ft2 film use are not qualified for Be, peel, thermal cycling or vacuum; .015 is only a mass lower choice.",
  "next_evidence": "Test a complete seam and bond architecture and measure its installed mass, leak rate and stiffness; do not infer that seam-only panel width closes the full joint allowance."
}
```

### N101 — NFI-027-SEAM-SCALING

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-SEAM-SCALING",
  "tag": "PROJECTION",
  "issue": "Frozen 020 kg/m 2 hides Be-doubler and core-gap masses that grow with optimized thickness. The corrected model holds widths/gaps fixed but resizes their depths. Neither seam is mechanically designed.",
  "next_evidence": "Weigh and load-test a curved two-skin splice; establish widths, gaps, taper, sealing, peel, fatigue and stiffness as functions of face/core thickness."
}
```

### N102 — NFI-027-JOINT-STRENGTH

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-JOINT-STRENGTH",
  "tag": "PROJECTION",
  "issue": "020's 0.9/0.6 net-section efficiencies are assumed screens, applied only to compression. The enhanced aluminium optimum is global/joint limited. No joint buckling, shear or peel allowables exist.",
  "next_evidence": "Measure the seam's biaxial compression, load eccentricity and failure envelope; do not count straps as structural stiffness without a model."
}
```

### N185 — NFI-020-JOINT-MASS-CAPACITY

Source `rpt-ref-3e02218a03708a878faa`; original file `unpublished-local-ref:3fe2376964ec428a; pointer `retained original identity`.

```json
{
  "id": "NFI-020-JOINT-MASS-CAPACITY",
  "rank": 1,
  "tag": "PROJECTION",
  "claim": "Installed bond/seam mass and capacity are not contained by an evidenced 5% allowance.",
  "optimistic": {
    "joining_kg": 968.1973614494823,
    "payload_kg": -507.29810905072463,
    "kg_per_hull_seam_m": 0.21832274825065098,
    "eta_assumed": 0.9
  },
  "conservative": {
    "joining_kg": 3721.9962746758147,
    "payload_kg": -3261.0970222770566,
    "kg_per_hull_seam_m": 0.48279897548325995,
    "eta_assumed": 0.6
  },
  "sources": [
    {
      "id": "S03",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6"
    },
    {
      "id": "S04",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74"
    },
    {
      "id": "S05",
      "url": "https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf?fn=AF163-2.pdf"
    },
    {
      "id": "S06",
      "url": "https://ntrs.nasa.gov/api/citations/19690025590/downloads/19690025590.pdf"
    }
  ],
  "needed_to_ground": "Ground first: weigh and load a representative curved two-skin/core seam with the intended film coverage, seal, manufacturing defects and post-thermal-cycle condition. Establish seam buckling, shear/peel and leak behavior.",
  "effect_on_lead": "The optimistic selected joint already consumes more than the payload; redesign or a much lighter demonstrated joint is needed. Cases are not bounding tests.",
  "closed_by_this_card": false
}
```

### N209 — NFI-021b-JOINT-PARAMETERS

Source `rpt-ref-1080d4f6a1af4cfa8c67`; original file `unpublished-local-ref:4edbd73193c8c843; pointer `retained original identity`.

```json
{
  "id": "NFI-021b-JOINT-PARAMETERS",
  "issue": "019's optimistic joint parameters (60 mm strips, 0.2 mm adhesive, 1.5 mm core splice) are owner assumptions, not validated joints; 020's own splice model weighs 0.218 kg per hull-seam metre in its optimistic case."
}
```

### N238 — NFI-028-17

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-17",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Installed bond strength and stiffness",
  "today_value": "Core Ec=103.421 MPa, G_W=46.884 MPa inherited; actual bonded effective values unknown",
  "required_or_budget_target": {
    "core_W_typical_strength_Pa": 241316.50526088,
    "core_W_min_average_strength_Pa": 172368.9323292,
    "illustrative_normal_at_0p1mm_Pa": 511648.1156583237
  },
  "needed_evidence": "Representative flatwise, shear, interface stiffness/toughness and wrinkle/disbond tests. Relative displacement is not established by the pressure alone.",
  "factor_to_216_427kg_allowance": null,
  "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."
}
```

### N410 — NFI-021B-CHECK-RESERVE-JOINTS

Source `rpt-ref-444ac46ffbede876f9cd`; original file `unpublished-local-ref:e116eab86edf378e; pointer `/rows/6`.

```json
{
  "id": "NFI-021B-CHECK-RESERVE-JOINTS",
  "status": "open",
  "tag": "PROJECTION",
  "field": "019 fixed reserve and unvaried seam/adhesive assumptions",
  "check_fixed_kg": 411.29894407164744,
  "check_reserve_kg": 775.729373623117,
  "issue": "The correct mass closure still assumes sealed service, zero payload, the chosen weather/water condition, 60 mm strips, 0.2 mm seam adhesive, 1.5 mm core splice and no demonstrated Be/core bond at the nominated film weight. These are explicit inputs, not measured capabilities.",
  "implication": "3M lists .030 and .015 lb/ft² films, with .015 unsupported; nominal areal mass does not qualify the joint. 775.729 kg reserve is spent on the declared condition rather than spare payload. Other service, seal, coating or handling loads need a new budget.",
  "source": "MAINLINE-019/020; 3M AF 163-2 technical datasheet",
  "needed_evidence": "Weighed sealed sandwich/seam specimen with load transfer and gas-load measurements; declared site and payload."
}
```

### N421 — NFI-028-LEGACY-09

Source `rpt-ref-68dff0680696fe9b4cb4`; original file `unpublished-local-ref:5ac789d6de7269e0; pointer `/rows/0`.

```json
{
  "id": "NFI-028-LEGACY-09",
  "issue": "METHOD.md states the 020 optimistic splice mass and does not state a 0.9 face-retention screen. Fixed legacy mass matches on every panel. The stored re-optimised factor, joining mass and core fraction match only after projected joint retention is set to 0.9 times face stress capacity over demand. That screen is in the owner's calculation and is absent from METHOD.md and CARD.md.",
  "consequence": "The legacy mass column stands. The legacy safety-factor column is the screened search, not the search under the stated modes. The other 64 combinations are unchanged. This does not stop the card.",
  "mismatches": [
    {
      "row": "small_planning/legacy020_optimistic",
      "field": "reoptimized.least_known_mode_SF",
      "card": 0.6299541781355524,
      "mine": 0.639505067711224
    },
    {
      "row": "small_planning/legacy020_optimistic",
      "field": "reoptimized.joining.total_kg",
      "card": 1467.6968689823811,
      "mine": 1467.8914866714408
    },
    {
      "row": "small_planning/legacy020_optimistic",
      "field": "reoptimized.core_mass_fraction",
      "card": 0.10815208007294574,
      "mine": 0.11007879393428102
    },
    {
      "row": "stock_envelope/legacy020_optimistic",
      "field": "reoptimized.least_known_mode_SF",
      "card": 0.7508506635092148,
      "mine": 0.7925494288963508
    },
    {
      "row": "stock_envelope/legacy020_optimistic",
      "field": "reoptimized.joining.total_kg",
      "card": 927.9106724326657,
      "mine": 928.2841394008699
    },
    {
      "row": "stock_envelope/legacy020_optimistic",
      "field": "reoptimized.core_mass_fraction",
      "card": 0.09563067036212788,
      "mine": 0.10180000940685648
    },
    {
      "row": "1m_projection/legacy020_optimistic",
      "field": "reoptimized.least_known_mode_SF",
      "card": 0.7604170345217105,
      "mine": 0.8048670458298006
    },
    {
      "row": "1m_projection/legacy020_optimistic",
      "field": "reoptimized.joining.total_kg",
      "card": 885.144031405966,
      "mine": 885.5080226698558
    },
    {
      "row": "1m_projection/legacy020_optimistic",
      "field": "reoptimized.core_mass_fraction",
      "card": 0.0948109501600442,
      "mine": 0.10124436898037081
    },
    {
      "row": "2m_projection/legacy020_optimistic",
      "field": "reoptimized.least_known_mode_SF",
      "card": 0.81492106071556,
      "mine": 0.8755239411748689
    },
    {
      "row": "2m_projection/legacy020_optimistic",
      "field": "reoptimized.joining.total_kg",
      "card": 641.3198974286786,
      "mine": 641.5683196771447
    },
    {
      "row": "2m_projection/legacy020_optimistic",
      "field": "reoptimized.core_mass_fraction",
      "card": 0.09052126825386655,
      "mine": 0.09830732502491321
    },
    {
      "row": "4m_projection/legacy020_optimistic",
      "field": "reoptimized.least_known_mode_SF",
      "card": 0.8445359574805592,
      "mine": 0.9142216438967713
    },
    {
      "row": "4m_projection/legacy020_optimistic",
      "field": "reoptimized.joining.total_kg",
      "card": 508.71676119210684,
      "mine": 508.8598451495485
    },
    {
      "row": "4m_projection/legacy020_optimistic",
      "field": "reoptimized.core_mass_fraction",
      "card": 0.08843502938056308,
      "mine": 0.0968606088681324
    }
  ],
  "next": "State the 0.9 screen in METHOD.md, or drop it from the stored search."
}
```

### N423 — NFI-028-HULL-SF

Source `rpt-ref-68dff0680696fe9b4cb4`; original file `unpublished-local-ref:5ac789d6de7269e0; pointer `/rows/2`.

```json
{
  "id": "NFI-028-HULL-SF",
  "issue": "The least modeled factor excludes unmeasured core-bond, seam, thermal and defect modes. Flatwise strength is not reported for AF 163-2U at 0.015 lb/ft². No source in the card qualifies the lightest joining mass.",
  "consequence": "Qualified lightest mass and overall installed-hull factor stay unknown. The modeled table is PROJECTION and the materials are QUESTIONABLE.",
  "next": "A weighed curved beryllium and aluminium panel tested for the missing allowables."
}
```

### N442 — NFI-028b-unmodelled-bond-seam

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/18`.

```json
{
  "id": "NFI-028b-unmodelled-bond-seam",
  "status": "OPEN",
  "issue": "Relevant flatwise, imperfection shear, peel/HAZ, local buckling, thermal/cycle and leak allowables are absent.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "overall_installed_SF": null
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "Unknown modes listed in every point"
}
```

### N491 — NFI-031-JOINTS

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/9`.

```json
{
  "id": "NFI-031-JOINTS",
  "tag": "PROJECTION",
  "issue": "P2 seams and bond films are a mass recipe, not checked structural joints. P3 percent joints are an allowance, not strength or rotational stiffness. Folded source joints sized at p0 cannot automatically take a larger float pressure.",
  "next_evidence": "Size and qualify seal, splice, node and load-introduction details at the maximum service pressure, including stiffness, eccentricity, fatigue and leakage."
}
```

### N550 — NFI-036-R20-joint

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/12`.

```json
{
  "id": "NFI-036-R20-joint",
  "status": "OPEN",
  "issue": "Qualify the inherited R20 0.9 joint efficiency and full-gauge splice model.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "eta": 0.9
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "027",
  "closure": "Compression qualification of actual splice geometry/process with the purchased face grade."
}
```

### N553 — 033-NFI-01

Source `rpt-ref-5b1ba7a48fcb57c8e35e`; original file `unpublished-local-ref:6bdf8f2e409f7e2b; pointer `/issues/0`.

```json
{
  "id": "033-NFI-01",
  "tag": "PROJECTION",
  "title": "Installed joints remain unqualified",
  "finding": "The six-mode shell result excludes scarf, peel and face/core bond capacities. The additional 10 MPa average-shear screen caps face stress at 300.333 MPa, but is not a qualified allowable. All installed-hull SF values remain null.",
  "next_evidence": "Measure compression/scarf/bond/peel capacity of the actual SR-200, AF163-2U, primer and honeycomb process, including seam imperfections and environmental conditioning.",
  "status": "open"
}
```

### N559 — 033-NFI-07

Source `rpt-ref-5b1ba7a48fcb57c8e35e`; original file `unpublished-local-ref:6bdf8f2e409f7e2b; pointer `/issues/6`.

```json
{
  "id": "033-NFI-07",
  "tag": "PROJECTION",
  "title": "Nominal adhesive and seam inventory",
  "finding": "Nominal film is .015 lb/ft2 per face/core interface; scarf film .07 kg/m2, splice gap .5 mm at 500 kg/m3, sealing .002 kg/m for both faces. Nominal primer is zero. No AF163 mass tolerance was independently verified; the inherited +/- .005 statement is unused.",
  "next_evidence": "Obtain an installed bill including primer, intersections, closeouts, rejected material, repairs and leak barriers; qualify sustained load, thermal cycling and leakage.",
  "status": "open"
}
```

### N701 — NFI-036-R20-joint

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/12`.

```json
{
  "id": "NFI-036-R20-joint",
  "status": "OPEN",
  "issue": "Qualify the inherited R20 0.9 joint efficiency and full-gauge splice model.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "eta": 0.9
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "027",
  "closure": "Compression qualification of actual splice geometry/process with the purchased face grade.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

## R034 — primer and surface prep mass

**Original question:** Be-compatible primer and surface preparation mass is not counted; zero is only a bookkeeping limit.

### N234 — NFI-028-13

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-13",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Primer and surface preparation mass",
  "today_value": "Zero is a bookkeeping lower limit, not proof of a primer-free process; 5 g/m2 per line is sensitivity",
  "required_or_budget_target": {
    "remaining_g_m2_per_line_at_nominal_stock": 0.8702381595960997,
    "5gsm_added_kg": 12.566370614359172
  },
  "needed_evidence": "Qualify Be-compatible preparation/primer and weigh it including core-side coverage.",
  "scenario": "af015_scarf_primer5",
  "scenario_joining_kg": 226.80636845652077,
  "factor_to_216_427kg_allowance": 1.047957124659267,
  "mass_reduction_factor_to_fit": 1.047957124659267
}
```

### N438 — NFI-028b-primer

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/14`.

```json
{
  "id": "NFI-028b-primer",
  "status": "OPEN",
  "issue": "Actual primer coverage, surface preparation and mass must be measured; 5 g/m² is a selected sensitivity.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "per_line_kg_m2": 0.005,
    "two_lines_kg": 12.566370614359172
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "MAINLINE-028 sensitivity"
}
```

### C097 — NFI-037b-RT-PASTE

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/8`.

```json
{
  "id": "NFI-037b-RT-PASTE",
  "tag": "PROJECTION",
  "claim": "Room-temperature pastes (EA 9394 class) carry no sourced honeycomb bond data, fillet mass or flatwise strength; they are priced at AF's areal weight.",
  "needed_to_ground": "Honeycomb flatwise and climbing-drum data for a room-temperature system at a weighed areal mass."
}
```

### C163 — 040-01-coating_inventory

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/0`.

```json
{
  "id": "040-01-coating_inventory",
  "tag": "PROJECTION",
  "open_issue": "0.20 kg/m² paint+primer remains assumed; the marginal R12/R15 results are sensitive to installed coating mass.",
  "grounding": "Weigh prepared, coated Be witnesses at the required optical performance, including primer, repairs and coverage variation."
}
```

### C194 — NFI-037b-RT-PASTE

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/8`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-RT-PASTE",
  "tag": "PROJECTION",
  "claim": "Room-temperature pastes (EA 9394 class) carry no sourced honeycomb bond data, fillet mass or flatwise strength; they are priced at AF's areal weight.",
  "needed_to_ground": "Honeycomb flatwise and climbing-drum data for a room-temperature system at a weighed areal mass."
}
```

## R035 — seam step effect on kd

**Original question:** A seam step is counted only as delta/t_eq; a real seam also breaks face continuity, and no joint failure model exists.

### N182 — NFI-015-SEAM-DISCONTINUITY

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-SEAM-DISCONTINUITY",
  "issue": "A seam step is counted only as delta/t_eq. A real seam also breaks face continuity. On P2-E the geometric reading is kd 0.950, 0.931 and 0.869 at steps of 1, 3 and 10 mm.",
  "consequence": "The geometric reading is not a joint failure mode.",
  "next": "A joint model belongs with the sandwich failure cards."
}
```

## R036 — selective cell-edge adhesive deposition

**Original question:** Selective cell-edge deposition is lab-only on CFRP/Nomex and not shown on Be/Al.

### N225 — NFI-028-04

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-04",
  "status": "OPEN",
  "tag": "QUESTIONABLE",
  "technology_state": "in_the_lab",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Selective cell-edge deposition",
  "today_value": "8-80 g/m2 deposited in CFRP/Nomex experiments; not a Be/Al strength limit",
  "required_or_budget_target": {
    "assumed_g_m2": 8,
    "less_aggressive_g_m2": 20
  },
  "needed_evidence": "Measure coverage, fillets, cured mass and mechanical performance after transfer to Be/Al.",
  "scenario": "lab8_scarf",
  "scenario_joining_kg": 50.28300529539905,
  "factor_to_216_427kg_allowance": 0.23233224890109164,
  "mass_reduction_factor_to_fit": 1,
  "modeled_component_kg": 20.106192982974676,
  "component_fraction_of_allowance": 0.0929005139038753
}
```

### N439 — NFI-028b-lab-bond

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/15`.

```json
{
  "id": "NFI-028b-lab-bond",
  "status": "OPEN",
  "issue": "8 g/m² deposition exists in laboratory work on other materials; transfer to Be/Al core is unqualified.",
  "state": "in_the_lab",
  "tag": "PROJECTION",
  "needed": {
    "per_line_kg_m2": 0.008,
    "matched_strength": null
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "https://infoscience.epfl.ch/server/api/core/bitstreams/28b8cc7a-f046-4da3-9fcc-5d5ad3c52a9d/content",
  "Be_hull_transfer": "PROJECTION"
}
```

## R037 — spherical layout and scarf edges

**Original question:** No polar-cap or intersection design; the mean-field rectangular layout ignores tessellation, tolerances and rejects.

### N237 — NFI-028-16

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-16",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Spherical layout and scarf feather edges",
  "today_value": "Mean-field rectangular layout with scarf overlap deducted; no polar-cap/intersection design",
  "required_or_budget_target": {
    "remaining_all_extra_installed_kg_AF_stock": 2.1871470472484873
  },
  "needed_evidence": "Finished spherical tessellation, machining/fit tolerances, edge waviness, intersections, curvature and installation rejects.",
  "scenario": "af015_scarf",
  "scenario_joining_kg": 214.2399978421616,
  "factor_to_216_427kg_allowance": 0.9898943034693449,
  "mass_reduction_factor_to_fit": 1
}
```

## R038 — 019's optimistic reserve embeds 4 m panels and 0.015 lb/ft2 film

**030b source history:** Do not mix the old 021b enlarged-panel reserve with 028b's stock-scarf account. 028b fixed non-joint reserve is 411.298944 kg; total excess is recomputed. 033 explicitly reports both actual-bill and retained-floor budgets.

**Original question:** The 019 reserve of 535.95 kg embeds 4 m panels and 0.015 lb/ft2 film; at today panel and film the reserve is larger.

### N208 — NFI-021b-RESERVE-HIDES-OPTIMISMS

Source `rpt-ref-1080d4f6a1af4cfa8c67`; original file `unpublished-local-ref:4edbd73193c8c843; pointer `retained original identity`.

```json
{
  "id": "NFI-021b-RESERVE-HIDES-OPTIMISMS",
  "issue": "019's 535.95 kg reserve embeds 4 m panels and 0.015 lb/ft2 films; at today's panel and film this point's reserve is 1229.4 kg.",
  "numbers": {
    "least_set_reserve_as_given": [
      "O1_gamma",
      "O2_wrinkle"
    ],
    "usage": 0.6656351070909744
  }
}
```

### N443 — NFI-028b-019-reserve

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/19`.

```json
{
  "id": "NFI-028b-019-reserve",
  "status": "OPEN",
  "issue": "Validate the optimistic service/environment assumptions behind the fixed mass-equivalent reserve.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "systems_excess_kg": 0.0,
    "retained_water_kg": 125.66370614359174,
    "contamination_kg": 5.0,
    "temperature_pressure_loss_kg": 213.036426543752,
    "humidity_loss_kg": 18.704389882434043,
    "internal_gas_kg": 48.89442150186961,
    "payload_kg": 0.0
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "Pinned MAINLINE-019 / 021b",
  "fixed_reserve_kg": 411.2989440716474
}
```

### N558 — 033-NFI-06

Source `rpt-ref-5b1ba7a48fcb57c8e35e`; original file `unpublished-local-ref:6bdf8f2e409f7e2b; pointer `/issues/5`.

```json
{
  "id": "033-NFI-06",
  "tag": "PROJECTION",
  "title": "Joining allowance policy",
  "finding": "028 uses actual joining; 027 retains unused 5% structural-mass allowance. Main results use 028, with the floor reported separately. The Q-plus-strength crossing shifts from 16.282 to 40.470 m; R50 six-mode endpoint payload shifts from 89.422 to 74.375 tonnes.",
  "next_evidence": "Keep both named accounts explicit in later cards and allocate any required repair, edge-block, primer or leak-barrier mass before claiming payload.",
  "status": "open"
}
```

### N601 — NFI-017b-JOINT-ALLOWANCE

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/1`.

```json
{
  "id": "NFI-017b-JOINT-ALLOWANCE",
  "tag": "QUESTIONABLE",
  "claim": "Explicit 028 joining replaces the 5% joint allowance, as 028 did. Under the 5% floor of 019, 021b and 027, sheet size and bond film stop being levers at all. The reserve is 019's optimistic (sealed-service) set, scaled with radius by 027's laws.",
  "needed_to_ground": "A ruling on whether the 5% allowance is a floor once joining is explicit."
}
```

### C015 — CHECK033-NFI-06

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/5`.

```json
{
  "id": "CHECK033-NFI-06",
  "inherited_id": "033-NFI-06",
  "tag": "PROJECTION",
  "title": "Joining allowance policy",
  "finding": "028 uses actual joining; 027 retains unused 5% structural-mass allowance. Main results use 028, with the floor reported separately. The Q-plus-strength crossing shifts from 16.282 to 40.470 m; R50 six-mode endpoint payload shifts from 89.422 to 74.375 tonnes.",
  "next_evidence": "Keep both named accounts explicit in later cards and allocate any required repair, edge-block, primer or leak-barrier mass before claiming payload.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Retained physical/model limitation. Arithmetic reproduction does not establish an installed-hull allowable."
}
```

### C017 — CHECK033-NFI-08

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/7`.

```json
{
  "id": "CHECK033-NFI-08",
  "inherited_id": "033-NFI-08",
  "tag": "PROJECTION",
  "title": "Weather and systems reserve laws",
  "finding": "The 019 optimistic temperature, pressure, humidity and internal-air losses scale with volume; .1 mm water and contamination scale with area; 100 kg systems remains reserved. Primary structural pressure is +1%; pressure at the reference value alone flips the R10 screen result to positive in the floor sensitivity.",
  "next_evidence": "Replace the projected climate, water retention, leak rate and systems estimates with mission measurements; couple pressure and buoyancy consistently.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Retained physical/model limitation. Arithmetic reproduction does not establish an installed-hull allowable."
}
```

### C049 — NFI-CHECK037-RESERVE-POINT-LOAD

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/11`.

```json
{
  "id": "NFI-CHECK037-RESERVE-POINT-LOAD",
  "tag": "QUESTIONABLE",
  "status": "open",
  "finding": "The 411.299 kg reserve contains environmental lift losses and distributed masses, not one suspended payload.",
  "proposed_fix": "Use the actual payload and equipment layout; label the 4.033 kN example as hypothetical. Do not convert buoyancy penalties into concentrated hardware weight."
}
```

### C182 — 040-20-joint_floor

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/19`.

```json
{
  "id": "040-20-joint_floor",
  "tag": "PROJECTION",
  "open_issue": "Actual joining and the retained 5% floor produce different margins and least sets; neither closes an unmeasured installed joining bill.",
  "grounding": "Close unlisted joining/edge/repair costs with a weighed assembly bill before releasing any retained allowance."
}
```

## R039 — design-day climate envelope for lift (site, temperature, pressure, humidity)

**030b source history:** 031 and CHECK-031 confirm altitude is conditional on a weather profile and terrain/clearance requirement. Spending all nominal lift gives below-sea-level hot/low/humid roots. This does not license deleting climate mass from an existing hull.

**Original question:** Lift depends on site temperature and pressure; no site is named so the 5% margin has no climate envelope. Hot afternoon and retained water each consume the margin.

### N058 — NFI-016-CLIMATE

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-CLIMATE",
  "rank": 2,
  "gap": "Lift at the site: dL/L = dp/p - dT/T. A QUESTIONABLE hot summer afternoon at +25.1 K takes the margin to -186.3 kg; 0.1 mm of retained water is 125.6 kg, 51 percent of the margin; 1 mm is 1257 kg. No site is named anywhere in the mainline, so the 5 percent margin has no climate envelope.",
  "direction": "Name the operating site and season windows; size a ballast or trim system for the hot-day deficit; require a hydrophobic coating and a shedding check before flight; weigh the hull after rain.",
  "effect": "Margin negative at the hot extreme without these; climbing does not recover it (lift falls about 9.4 percent per km)."
}
```

### N068 — NFI-019-SITE

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-SITE",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "No operating site, measured temperature/pressure/humidity envelope or cold-case minimum is specified. The selected weather cases are assumptions, not site return-period limits.",
  "next_evidence": "Replace the declared envelope with station data and operating constraints; recompute both mass and maximum differential-pressure cases."
}
```

### N108 — NFI-027-ENVIRONMENT

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-ENVIRONMENT",
  "tag": "QUESTIONABLE",
  "issue": "The optimistic +10 K/±1%/1000 Pa vapour and conservative +25.1 K/±2%/6000 Pa cases are owner scenarios, not a site distribution. Water is a full-area equivalent retained film, contamination an area load.",
  "next_evidence": "Specify site, gas composition, temperatures, weather exposure, water shedding/icing and mission duration; retain both low-density lift and high-pressure strength envelopes."
}
```

### N210 — NFI-021b-CLIMATE-SERVICE

Source `rpt-ref-1080d4f6a1af4cfa8c67`; original file `unpublished-local-ref:4edbd73193c8c843; pointer `retained original identity`.

```json
{
  "id": "NFI-021b-CLIMATE-SERVICE",
  "issue": "The fixed reserve items are 019's optimistic sealed-service day (0.1 mm water, +10 K, 1 percent, 1 kPa); 019's conservative day needs 4229 kg.",
  "grounding_card": "MAINLINE-019 follow-ups (site, gas-load measurement)"
}
```

### N408 — NFI-021B-CHECK-PRESSURE

Source `rpt-ref-444ac46ffbede876f9cd`; original file `unpublished-local-ref:e116eab86edf378e; pointer `/rows/4`.

```json
{
  "id": "NFI-021B-CHECK-PRESSURE",
  "status": "open",
  "tag": "QUESTIONABLE",
  "field": "019 pressure-swing service assumption versus scored reference pressure",
  "reference_pressure_Pa": 95460.83791390515,
  "plus_1pct_modes": {
    "global_buckling": 0.9900990099009901,
    "face_compression": 0.990103012633993,
    "core_shear_crimping": 3.0652409471788298,
    "core_crush": 5.00576441927028,
    "face_wrinkling": 0.9900990099009901,
    "intracell_dimpling": 4.9260486347682875
  },
  "issue": "The printed point scores the COMMON reference pressure. The inherited service package includes a 1% pressure swing; its high-pressure structural corner is separate from the low-pressure buoyancy corner.",
  "implication": "At +1% external pressure on the same geometry and needed values, global and wrinkle SF are 0.990099, compression 0.990103. This does not contradict the reference-case arithmetic but prevents treating that exact point as covering the complete service package.",
  "needed_evidence": "Retune against the specified pressure envelope and retain the separate low-pressure/hot buoyancy budget."
}
```

### N470 — NFI-015-CHECK-HYDROSTATIC

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/4`.

```json
{
  "id": "NFI-015-CHECK-HYDROSTATIC",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "not_revisited_outside_focused_map",
  "reported": "015b contains no hydrostatic-gradient recomputation.",
  "checked": "The old sea-level-density gradient is not corrected to the pinned 500 m density. The previous finding remains attached to the old card.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Use the pinned500m air density consistently."
}
```

### N560 — 033-NFI-08

Source `rpt-ref-5b1ba7a48fcb57c8e35e`; original file `unpublished-local-ref:6bdf8f2e409f7e2b; pointer `/issues/7`.

```json
{
  "id": "033-NFI-08",
  "tag": "PROJECTION",
  "title": "Weather and systems reserve laws",
  "finding": "The 019 optimistic temperature, pressure, humidity and internal-air losses scale with volume; .1 mm water and contamination scale with area; 100 kg systems remains reserved. Primary structural pressure is +1%; pressure at the reference value alone flips the R10 screen result to positive in the floor sensitivity.",
  "next_evidence": "Replace the projected climate, water retention, leak rate and systems estimates with mission measurements; couple pressure and buoyancy consistently.",
  "status": "open"
}
```

## R040 — float margin and payload: 0%, 5%, 10.96% and 86.49% budgets

**Current 030c:** 040 common bill: no R10 float in named ranges; ISA/optimistic/both-weather full gamma/Q endpoint deficits 109.649/257.973/596.529 kg (actual joining). First ISA floats occur at R12–15. R30 ranks least optimism among tested radii; ISA/optimistic usage .601233/.789568, conditional SF 1. Both-weather has no float. Coating+primer, assumed .20 kg/m2, and retained water are the largest assumed debits. Static/service closure is not qualified life.

**Original question:** Reserve is the explicit charge above baseline floors, not statistical contingency or free payload; climate plus internal air alone exceeds a 5% margin and larger radius alone cannot fix it.

### N003 — NFI-PAYLOAD-SENTENCE

Source `rpt-1228-mainline009c5-independent-check-1019`; original file `unpublished-local-ref:52f757339520e0fd; pointer `retained original identity`.

```json
{
  "id": "NFI-PAYLOAD-SENTENCE",
  "type": "text_mismatch",
  "row": "CARD.md opening",
  "field": "mass_fraction",
  "reported": "The mass is 5 percent of lift",
  "reported_fraction": 0.05,
  "independent_total_mass_fraction": 0.95,
  "independent_payload_fraction": 0.05,
  "proposed_fix": "Say payload reserve is 5% of lift and total mass is 95%.",
  "stops_owner": false
}
```

### N056 — NFI-MASS

Source `rpt-ref-d5b4aaa267b71d82fe25`; original file `unpublished-local-ref:1d727f2cb127351c; pointer `retained original identity`.

```json
{
  "id": "NFI-MASS",
  "value": "payload margin",
  "optimistic": 0.0,
  "main_point": 0.05,
  "conservative": 0.05,
  "factor": "zero margin raises the structural budget by (lift-100)/(0.95*lift-100), about 5 percent, which does not close a wrinkling gap of several times",
  "source": "CARD-009 default, kept because MAINLINE-006's P2-E knee is that same 0 to 5 percent step.",
  "direction": "MAINLINE-012's equal-margin geometry, when that card is the newer input."
}
```

### N069 — NFI-019-PAYLOAD

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-PAYLOAD",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "Zero payload is an unladen demonstrator choice. The former 009c5 payload/margin number cannot simultaneously be mission payload and contingency.",
  "next_evidence": "Set payload and remaining float reserve separately. The +100 kg case is supplied."
}
```

### N080 — NFI-019-RESERVE

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-RESERVE",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "The summed margin is consumed at the declared design condition; it is not an additional residual flight contingency or positive safety factor. The cases do not form a statistical confidence interval.",
  "next_evidence": "Specify residual operational lift reserve and contingency after the environmental/system charges; add that amount to the budget."
}
```

### N115 — NFI-027-RESERVE-MEANING

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-RESERVE-MEANING",
  "tag": "QUESTIONABLE",
  "issue": "Reserve is the explicit charge above retained baseline system/joint floors, not statistical contingency or free payload. Climate plus internal air alone is 5.7396% optimistic and 13.1183% conservative.",
  "next_evidence": "If a sub 5% requirement is mandatory, change/justify the climate or gas assumptions or definition. Increasing radius alone cannot meet it."
}
```

### N196 — NFI-021-MARGIN

Source `rpt-ref-769a7442efd5a04681e9`; original file `unpublished-local-ref:63c049a0d93b9857; pointer `retained original identity`.

```json
{
  "id": "NFI-021-MARGIN",
  "needed": 0.05,
  "state": "assumed",
  "grounding_card": "MAINLINE-019 (margin budget)",
  "note": "The 5 percent margin stands until 019 files; every number here moves with it."
}
```

### N212 — NFI-021b-MARGIN

Source `rpt-ref-1080d4f6a1af4cfa8c67`; original file `unpublished-local-ref:4edbd73193c8c843; pointer `retained original identity`.

```json
{
  "id": "NFI-021b-MARGIN",
  "issue": "No payload: 019's unladen case. 019's +100 kg payload sensitivity raises the reserve to 637.85 kg."
}
```

### N486 — NFI-031-RESERVE-MEANING

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/4`.

```json
{
  "id": "NFI-031-RESERVE-MEANING",
  "tag": "QUESTIONABLE",
  "issue": "Climate is absent mass; water, contamination and gas are carried mass. 021 rev1 has a 5% placeholder, no separate climate rows or explicit seam budget. Recasting that placeholder is a new budget assumption.",
  "next_evidence": "Approve one common itemised gross mass ledger, including payload status, before treating cross-card points as the same vehicle."
}
```

### N598 — NFI-022D-MASS

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/9`.

```json
{
  "id": "NFI-022D-MASS",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "MAINLINE-023",
    "MAINLINE-024",
    "MAINLINE-025"
  ],
  "finding": "The inherited mass contract omits independent barrier/seam/coating and some joint process masses; sag volume is first-order. Two reserve choices are carried assumptions, not an audited vehicle budget.",
  "next": "Close complete operating hardware, membrane and joint masses against measured loaded volume."
}
```

### N624 — NFI-026B-10

Source `rpt-ref-8befdd4c89803adc44a8`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/9`.

```json
{
  "id": "NFI-026B-10",
  "tag": "QUESTIONABLE",
  "status": "computed_correction",
  "owner": "sciences",
  "issue": "Source-dependent mass conventions",
  "evidence": "frequency 6 mass 4950.843 kg exceeds inherited lift61.401 kg; frequency 4/2 totals 4588.051/4399.690 kg. frequency 6 joints 5%tube systems 50; frequency 4/2 joints 5%(tube+film+nodes) systems 100.",
  "implication": "Compare each case with its stated source allowances. Do not treat the three masses as an optimization under one common budget."
}
```

### N650 — NFI-026B-10

Source `rpt-ref-4a20323946ecafd56a6b`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/9`.

```json
{
  "id": "NFI-026B-10",
  "tag": "QUESTIONABLE",
  "status": "computed_correction",
  "owner": "sciences",
  "issue": "Source-dependent mass conventions",
  "evidence": "frequency 6 mass 4950.843 kg exceeds inherited lift61.401 kg; frequency 4/2 totals 4588.051/4399.690 kg. frequency 6 joints 5%tube systems 50; frequency 4/2 joints 5%(tube+film+nodes) systems 100.",
  "implication": "Compare each case with its stated source allowances. Do not treat the three masses as an optimization under one common budget."
}
```

### C158 — NFI-041-06

Source `rpt-ref-c7dfc45babe1b96007db`; original file `unpublished-local-ref:cd543374666d8c21; pointer `/items/5`.

```json
{
  "id": "NFI-041-06",
  "status": "open",
  "topic": "Realized mass, volume and practical fabrication",
  "evidence": [
    "CARD.md",
    "RESULTS.json:selected_realization",
    "RESIZE.csv",
    "frame_tools.py:geometry"
  ],
  "finding": "Actual integer counts add 178.319 kg of tube mass to the selected continuum point and leave 174.444 kg closure deficit at the 5% reserve. Resizing closes the declared arithmetic, but the cap sag and pressure-fan surfaces are distinct approximations. Film mass uses 4 pi R squared; node and systems allowances are inherited.",
  "needed": "Manufactured curved-tube tolerances and joints, gas-barrier/adhesive/seam/attachment mass, continuous or segmented arc feasibility, a pressure-equilibrated volume, assembly access, damage protection and a complete bill of materials.",
  "prohibited_inference": "Near-zero numerical closure residual does not establish physical vehicle mass closure."
}
```

### C238 — NFI-044-MASS-CLOSURE

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/14`.

```json
{
  "id": "NFI-044-MASS-CLOSURE",
  "finding": "The quantified strict pad plus 60:1 scarf candidate adds 36.66 kg to an already balanced budget; lugs, fasteners, backing, monitoring and repair margins are additional unknowns.",
  "evidence_needed": "A complete installed bill of materials and a new floating equilibrium without silently consuming the fixed reserve or systems allocation."
}
```

## R041 — retained water and contamination

**Original question:** Water films are equivalent retained thickness, not rainfall; absorbed core moisture, corrosion, thermal gradients and derating are unquantified; 320 K gas temperature is an acceptance condition.

### N078 — NFI-019-ENVIRONMENT

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-ENVIRONMENT",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "Water films are equivalent retained thickness over the whole area, not rainfall depths. Moisture absorbed in core, corrosion, thermal gradients and property derating are not separately quantified here. Gas temperature <=320 K is an acceptance condition, not a thermal prediction.",
  "next_evidence": "Measure water shedding, conditioning, absorbed moisture and thermal response for the selected assembly."
}
```

### N094 — NFI-HULL-HUMIDITY

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-HULL-HUMIDITY",
  "state": "not in the case",
  "note": "The case has no exterior humidity. Water loads stay at the sheet condition and are not a hull rate."
}
```

## R042 — systems and allowance masses are owner allowances (100 kg P2, 50 kg P3, pump, battery)

**Original question:** Battery estimate assumes packaged energy density, usable fraction and conversion; catalog pump data are not installed duty measurements and the smaller pump misses the hot-gas flow.

### N035 — NFI-MASS

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-MASS",
  "gap": "Joint fraction 5 percent, systems 100 kg, and zero residual gas are unchanged inherited numbers.",
  "direction": "Replace them with a parts list.",
  "effect": "They set the structural mass on the ceiling."
}
```

### N073 — NFI-019-SYSTEMS

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-SYSTEMS",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "The battery estimate assumes 150 Wh/kg packaged, 80% usable and 90% conversion. Catalog pump speed/power are not installed duty measurements; the smaller SV220B cannot meet the stated hot-gas flow at the fixed pressure cap.",
  "next_evidence": "Measure the SV300B or alternative system's curve, input power, cooling, line conductance and duty cycle; procure a qualified power package. Passive and 8 h sensitivities isolate the endurance assumption."
}
```

### N079 — NFI-019-OTHER-MASS

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-OTHER-MASS",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "This closes the card's explicit budget, not every aircraft subsystem. Separate coating, hardpoint/spreader, mooring attachment, handling, navigation or propulsion masses are not individually sized. The optimistic case retains 70 kg of unused system allowance; the active case has no such spare allowance.",
  "next_evidence": "Allocate each needed item explicitly before calling this a complete vehicle mass statement; do not spend retained allowance twice."
}
```

### N109 — NFI-027-OTHER-MASS

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-OTHER-MASS",
  "tag": "QUESTIONABLE",
  "issue": "Extra coatings, lightning protection, mooring, hardpoints, navigation and propulsion are not independently sized. P2 retains a 100 kg system floor, including 70 kg above the passive package, but this is not a complete vehicle mass model.",
  "next_evidence": "Itemize additional vehicle masses. An extra 0.1 kg/m 2 is included as a P2 sensitivity; 209.84 kg payload at R = 20 is only 41.75 g/m 2 of additional areal mass."
}
```

### N145 — NFI-010-SYSTEMS

Source `rpt-ref-58b2bed18db2449100f2`; original file `unpublished-local-ref:9b713febb61ac916; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-010-SYSTEMS",
  "gap": "Systems at 100 kg per sphere in a cluster is the mass rule read literally. A shared-systems cluster would pay it once.",
  "direction": "Name the systems architecture before crediting any cluster margin.",
  "effect": "Cluster margins improve by up to (n-1) x 100 kg of lift; SFs unchanged."
}
```

### N250 — NFI-MASS

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-MASS",
  "linked_inputs_or_points": "joints nodes systems",
  "questionable_assumption_or_gap": "Allowances are round owner numbers.",
  "direction_of_further_investigation": "Replace with a parts list.",
  "how_it_affects_margin_or_SF": "Each kilogram reduces margin by 1/lift."
}
```

### N260 — NFI-MASS

Source `rpt-mainline002-grok-strength-card-1019`; original file `unpublished-local-ref:f02996967e2f160d; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-MASS",
  "gap": "Joint fractions, node mass and payload allowances are unchanged owner numbers.",
  "direction": "Replace with a parts list.",
  "effect": "They set how much margin the allocation can spend."
}
```

### N268 — NFI-MASS

Source `rpt-mainline003-grok-p2-targets-1019`; original file `unpublished-local-ref:c644022670e558c3; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-MASS",
  "gap": "Joint fraction, payload allowance and zero gas are unchanged inherited numbers.",
  "direction": "Replace them with a parts list.",
  "effect": "They set the structural mass on the ceiling."
}
```

### N413 — NFI-CHK024-PUMP-MASS

Source `rpt-ref-7d6892c4e55be16ad523`; original file `unpublished-local-ref:0d655e2d18e3e532; pointer `/open/2`.

```json
{
  "id": "NFI-CHK024-PUMP-MASS",
  "kind": "unclosed operations mass",
  "tag": "QUESTIONABLE",
  "finding": "The scan has 50 kg for all systems. The inherited pump alone is 150-400 kg, not debited from tube mass. Reallocating all 50 kg leaves 100-350 kg unbooked; keeping the original systems adds the full pump. No getter capacity is sourced.",
  "proposed_next": "Book a selected pumping system, power supply and operating internal-pressure allowance, then re-optimize. The inherited class is not a new product qualification.",
  "minimum_reallocation_gap_kg": [
    100,
    350
  ]
}
```

### N586 — NFI-034-MASS-ALLOCATION

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/14`.

```json
{
  "id": "NFI-034-MASS-ALLOCATION",
  "tag": "PROJECTION",
  "finding": "Both current lead models carry 100 kg systems. Identified sealed hardware is 30-50 kg. Zylon barrier and previously omitted joint adhesive may be funded from remaining allocation only by explicit reallocation; other installed hardware is unresolved.",
  "proposed_next": "Keep the whole 100 kg reserved, book all new masses once, and do not assign unused allowance to payload before a complete bill exists."
}
```

### C075 — NFI-034-MASS-ALLOCATION

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/14`.

```json
{
  "id": "NFI-034-MASS-ALLOCATION",
  "tag": "PROJECTION",
  "finding": "Both current lead models carry 100 kg systems. Identified sealed hardware is 30-50 kg. Zylon barrier and previously omitted joint adhesive may be funded from remaining allocation only by explicit reallocation; other installed hardware is unresolved.",
  "proposed_next": "Keep the whole 100 kg reserved, book all new masses once, and do not assign unused allowance to payload before a complete bill exists.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C183 — 040-21-additional_installation

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/20`.

```json
{
  "id": "040-21-additional_installation",
  "tag": "PROJECTION",
  "open_issue": "Local hardpoints, tolerances, penetrations, rejected parts and repairs are not independently itemized beyond retained allowances.",
  "grounding": "Reconcile the complete installed bill and load-path drawing; do not assign an installed-hull SF from the scored scalar screens."
}
```

## R043 — getter capacity nitrogen air

**030b source history:** 034 distinguishes dry-gas getter capacity from water sorbents. Nitrogen can be gettered in some systems; no matched complete-hull sizing result is admitted.

**Original question:** SAES offers room-temperature nitrogen sorption, so the blanket denial and unsourced N2 capacity band cannot support the mass result; all-air getter lifetime incl. noble gases is unsized.

### N076 — NFI-019-GETTERS

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-GETTERS",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "SAES explicitly offers room-temperature nitrogen sorption. The unfinished script's blanket denial and unsourced N2 capacity band cannot support its mass result. All-air getter lifetime including noble gases remains unsized.",
  "next_evidence": "Use measured species loads, sorption speeds and capacities with activation conditions; do not award a getter-only all-air system a mass credit."
}
```

### N096 — NFI-GETTER

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-GETTER",
  "state": "not in the 016 method",
  "note": "No getter capacity is stated. The pump band is the 150 to 400 kg catalog class, not scaled to the gas load."
}
```

### N583 — NFI-034-GETTER

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/11`.

```json
{
  "id": "NFI-034-GETTER",
  "tag": "QUESTIONABLE",
  "finding": "BASF capacity is a humid-equilibrium number; the 10 wt% usable vacuum capacity is assumed. The SAES UHV capacity illustration is not a mixed-gas rough-vacuum recommendation. COMBO removes N2 at room temperature, but the opened page supplies no sizing capacity. Getter-retained external gas still adds vehicle mass.",
  "proposed_next": "Obtain service-pressure mixed-gas capacity/rate and cartridge mass; do not treat a water bed as a complete air getter or as recovered lift."
}
```

### C072 — NFI-034-GETTER

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/11`.

```json
{
  "id": "NFI-034-GETTER",
  "tag": "QUESTIONABLE",
  "finding": "BASF capacity is a humid-equilibrium number; the 10 wt% usable vacuum capacity is assumed. The SAES UHV capacity illustration is not a mixed-gas rough-vacuum recommendation. COMBO removes N2 at room temperature, but the opened page supplies no sizing capacity. Getter-retained external gas still adds vehicle mass.",
  "proposed_next": "Obtain service-pressure mixed-gas capacity/rate and cartridge mass; do not treat a water bed as a complete air getter or as recovered lift.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

## R044 — vacuum-holding route mass and power (sealed service vs onboard pump)

**Current 030c:** CHECK-034: 30–50 kg is daily ground-serviced sealed planning, not continuous pumping. Edwards continuous 24 h installation is 292.333 kg; ten kg battery supports at most nine days at 5 W. Retain 100 kg systems and no payload credit; inventories are older geometries.

**030b source history:** 034 selects ground evacuation plus sealed 24-hour service at an estimated 30–50 kg, retaining 100 kg systems. Longer gas-only lives do not establish electrical endurance; the assumed 10 kg power package lasts at most nine days at 5 W.

**Original question:** Holding internal pressure at a 1000 Pa ceiling needs a pump whose mass and power are uncertain and can exceed the float margin; the ceiling itself is an owner assumption.

### N060 — NFI-016-PUMP

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-PUMP",
  "rank": 4,
  "gap": "Holding p_int at a 1000 Pa ceiling takes 46.3 L/s there, 527 to 844 W real, and a QUESTIONABLE 150 to 400 kg pump set: 61 to 164 percent of the whole 244.472 kg float margin. The ceiling itself is an owner assumption; commissioning pump-down is 506 kWh.",
  "direction": "Shop a real Roots or screw pump specification at this duty (mass, power, intake pressure curve); set the operational p_int ceiling from the leak budget; consider distributed smaller pumps or a ground-only pump.",
  "effect": "Trades directly against the margin; can exceed it entirely at the conservative end."
}
```

### N106 — NFI-027-PUMP-SCALE

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-PUMP-SCALE",
  "tag": "PROJECTION",
  "issue": "One SV300B catalog pumping speed is insufficient for 019's volume-proportional 1%/day gas load above R = 10. Modular counting gives 1,3,7,23,103 pumps at 10,15,20,30,50 m, with full rated power continuously budgeted. Installed conductance/manifolds are not sized.",
  "next_evidence": "Measure leak/outgas and installed speed at pressure; replace the assumed gas-load law and duty cycle with a measured area/seam/volume decomposition."
}
```

### N107 — NFI-027-PASSIVE-SERVICE

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-PASSIVE-SERVICE",
  "tag": "PROJECTION",
  "issue": "The 30 kg sealed-service package is held fixed. Its normalized gas-load limit grows with volume; this does not prove its seals, plumbing, monitoring or ground evacuation hardware scale at fixed mass.",
  "next_evidence": "Demonstrate 24 h hold at the temperature envelope, seal transients, pressure monitoring and ground-service capability; add supporting hardware mass."
}
```

### N251 — NFI-GAS

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-GAS",
  "linked_inputs_or_points": "I-PINT and gas masses",
  "questionable_assumption_or_gap": "Perfect vacuum.",
  "direction_of_further_investigation": "State a hold pressure and the pump mass.",
  "how_it_affects_margin_or_SF": "Residual gas adds mass and reduces differential pressure."
}
```

### N496 — NFI-031-SYSTEMS-GAS

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/14`.

```json
{
  "id": "NFI-031-SYSTEMS-GAS",
  "tag": "PROJECTION",
  "issue": "The calculation retains optimistic 019 nonclimate loads and the full 100kg system floor even on conservative weather. This isolates weather; it does not qualify the conservative pump/battery/rain/contamination hardware package.",
  "next_evidence": "Qualify 24h sealed service and internal gas inventory, or recalculate with measured leakage, pumping, rain/ice retention and all installed systems."
}
```

### N584 — NFI-034-PUMP-AND-CONDUCTANCE

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/12`.

```json
{
  "id": "NFI-034-PUMP-AND-CONDUCTANCE",
  "tag": "PROJECTION",
  "finding": "KNF inlet speed is read from the low-pressure curve, not its STP delivery rating. Installed speed is assumed 75% of nominal. E2M28 motor 750 W is mechanical; 1000 W electrical is an assumption. One E2M28 is 2.3% short of the Kapton hot constant-source envelope at the assumed installation factor.",
  "proposed_next": "Measure effective inlet speed and input power with water vapour and the actual plumbing. Kapton needs at least 21.112 m3/h at the hot source-rate envelope."
}
```

### N585 — NFI-034-POWER-ENDURANCE

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/13`.

```json
{
  "id": "NFI-034-POWER-ENDURANCE",
  "tag": "PROJECTION",
  "finding": "30 kg sealed hardware includes an assumed 10 kg power package. Even if all ten kilograms were battery, the stated pack factors support five-watt monitoring for only nine days. Gas-only lifetimes are not autonomous mission endurance.",
  "proposed_next": "Size the actual pack, controls, wiring and thermal duty for the chosen service interval; retain daily ground-service baseline until supported."
}
```

### N668 — NFI-038-SYSTEM_MASS

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/17`.

```json
{
  "id": "NFI-038-SYSTEM_MASS",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Sealed life and pumping hardware are not determined by a helium leak rate",
  "evidence": "034 example 91.6-111.6kg Zylon package; inventories differ from current points.",
  "resolution_needed": "Update complete bill and installed pump speed/power at measured service load; retain 100kg allowance.",
  "tests": [
    "T9"
  ]
}
```

### C073 — NFI-034-PUMP-AND-CONDUCTANCE

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/12`.

```json
{
  "id": "NFI-034-PUMP-AND-CONDUCTANCE",
  "tag": "PROJECTION",
  "finding": "KNF inlet speed is read from the low-pressure curve, not its STP delivery rating. Installed speed is assumed 75% of nominal. E2M28 motor 750 W is mechanical; 1000 W electrical is an assumption. One E2M28 is 2.3% short of the Kapton hot constant-source envelope at the assumed installation factor.",
  "proposed_next": "Measure effective inlet speed and input power with water vapour and the actual plumbing. Kapton needs at least 21.112 m3/h at the hot source-rate envelope.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C074 — NFI-034-POWER-ENDURANCE

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/13`.

```json
{
  "id": "NFI-034-POWER-ENDURANCE",
  "tag": "PROJECTION",
  "finding": "30 kg sealed hardware includes an assumed 10 kg power package. Even if all ten kilograms were battery, the stated pack factors support five-watt monitoring for only nine days. Gas-only lifetimes are not autonomous mission endurance.",
  "proposed_next": "Size the actual pack, controls, wiring and thermal duty for the chosen service interval; retain daily ground-service baseline until supported.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C178 — 040-16-service_hardware

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/15`.

```json
{
  "id": "040-16-service_hardware",
  "tag": "PROJECTION",
  "open_issue": "30–50 kg service is nested in 100 kg systems and held fixed with radius; there is no installed bill of materials.",
  "grounding": "Provide a weighed scalable hardware, support, controls and wiring bill with the remaining systems allocation."
}
```

## R045 — whole-hull gas load: leaks, permeation, outgassing (needs measurement)

**030b source history:** 034 requires measured assembly leakage, conditioning and vent paths. Unvented cells/bores retain substantial air. Outgassing changes phase of already carried mass; ingress adds mass; getters retain it.

**Original question:** Face permeation is negligible at the present budget; CFRP figure comes from a helium band divided by 50 for air and no measured air permeance exists.

### N061 — NFI-016-BAKEOUT

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-BAKEOUT",
  "rank": 5,
  "gap": "Resident moisture 0.5 to 3 percent of the 2208.2 kg PVC core is 11.0 to 66.2 kg of water, worth 347 to 2079 Pa inside if released, against the 954.6 Pa one-percent-per-day ceiling. Steady outgassing itself is only 0.00 to 0.03 percent of the leak budget.",
  "direction": "Measure water content of the core lot; specify a bake-out and vent procedure at commissioning with a dry-gas backfill during assembly.",
  "effect": "Without bake-out the moisture alone can exceed the one-percent ceiling after release."
}
```

### N062 — NFI-016-LEAKSPEC

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-LEAKSPEC",
  "rank": 6,
  "gap": "The 1 percent-per-day budget equals a 2.48 mm2 choked hole or 4.25 mm2 molecular aperture: vacuum integrity at this budget is a discrete-defect and detection problem, not a material one. No leak specification, no detection threshold, no in-service pressure telemetry is defined.",
  "direction": "Set an operational leak spec well inside 46.28 Pa m3/s with margin; specify seam leak testing per panel at assembly and a pressure sensor resolution able to see a fraction of the budget.",
  "effect": "Detection latency decides whether the trim pump is a convenience or a life-limit."
}
```

### N067 — NFI-016-PERM

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-PERM",
  "rank": 11,
  "gap": "Face permeation is nil against the 1-percent budget: metals and monolithic SiC are gas barriers; CFRP epoxy laminate passes 5.4e-5 percent of budget on a QUESTIONABLE NASA composite-cryotank helium band divided by 50 for air. No measured air permeance exists for the actual faces.",
  "direction": "Measure air permeance of the chosen face and seam coupon directly; matters only if the leak budget is tightened far below 1 percent per day.",
  "effect": "None at the current budget; decisive if the budget tightens by four or more orders."
}
```

### N070 — NFI-019-LEAK

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-LEAK",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "Whole-hull leakage, trapped core gas, moisture desorption and outgassing have not been measured. The 30-50 kg passive package is a bill-of-mass estimate, not demonstrated vacuum retention.",
  "next_evidence": "Measure normalized total gas load through a complete representative panel/valve assembly, then the hull. For the stated 24 h, pstart=10 Pa at T0 and Tint<=320 K, Qref must be <=40.71949 Pa m3/s."
}
```

### N233 — NFI-028-12

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-12",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Sealant and pressure integrity",
  "today_value": "Selected 0.002 kg/m TOTAL for both face seams; leak-tested geometry unknown",
  "required_or_budget_target": "Maintain the inherited evacuated condition and service leak allocation.",
  "needed_evidence": "Measure permeability, pinholes and seam leak rate over temperature/pressure cycles; add any required barrier mass.",
  "scenario": "af015_scarf",
  "scenario_joining_kg": 214.2399978421616,
  "factor_to_216_427kg_allowance": 0.9898943034693449,
  "mass_reduction_factor_to_fit": 1,
  "modeled_component_kg": 5.694923693261571,
  "component_fraction_of_allowance": 0.026313352219156993
}
```

### N572 — NFI-034-LEAK-RATES

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/0`.

```json
{
  "id": "NFI-034-LEAK-RATES",
  "tag": "PROJECTION",
  "finding": "No full-hull or seam/node leak rate is measured. The 1e-5/1e-3/0.1 mbar L/s per metre and per node values are scenarios, with a separate port allowance. They span four decades but are not bounds.",
  "proposed_next": "Measure assembled pressure rise and test gas-specific leaks at service load and temperature; compare with the 24 h acceptance budget."
}
```

### N573 — NFI-034-SOURCE-TO-SERVICE

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/1`.

```json
{
  "id": "NFI-034-SOURCE-TO-SERVICE",
  "tag": "PROJECTION",
  "finding": "500 m fixes nominal pressure, not humidity or membrane temperature. Water rates are source-condition values mapped to a chosen 1 kPa driving partial pressure. Temperature dependence and humidity-gradient dependence are not measured.",
  "proposed_next": "Measure permeance at the intended thermal/humidity envelope. Keep the constant-source and partial-pressure model results distinct."
}
```

### N574 — NFI-034-TML-NOT-RATE

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/2`.

```json
{
  "id": "NFI-034-TML-NOT-RATE",
  "tag": "QUESTIONABLE",
  "finding": "NASA E595 uses 125 C for 24 h. TML is neither kg/day at 284.9 K nor a certified finite flight inventory. Historical cures/lots and several material/gauge proxies differ. CVCM is a subset, not added to TML.",
  "proposed_next": "Obtain actual material inventory and service-temperature desorption curves; retain unmatched-data tags."
}
```

### N575 — NFI-034-CONDITIONING

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/3`.

```json
{
  "id": "NFI-034-CONDITIONING",
  "tag": "PROJECTION",
  "finding": "Reference calculations assume 90% of the chosen release inventory was removed and the residue releases exponentially with one-day time constant. Neither fraction nor kinetics is demonstrated.",
  "proposed_next": "Demonstrate the required residual gas load after conditioning; do not treat this as a prescribed bake process."
}
```

### N576 — NFI-034-CORE-AND-TUBE-VENTING

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/4`.

```json
{
  "id": "NFI-034-CORE-AND-TUBE-VENTING",
  "tag": "PROJECTION",
  "finding": "Unvented P2 honeycomb would retain about 43.388 kg of ambient air. P3 tube bores would retain about 88.153/76.110 kg. Base cases require these spaces to share the evacuation path. Trapped gas is onboard mass even before it leaks into the main cavity.",
  "proposed_next": "Establish and qualify internal vent paths, pressure equalization and residual gas inventory. Any geometric vent change requires structural review."
}
```

### N577 — NFI-034-P2-PERMEATION-PATH

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/5`.

```json
{
  "id": "NFI-034-P2-PERMEATION-PATH",
  "tag": "PROJECTION",
  "finding": "Intact Be bulk ambient-gas permeation is set to zero in the screen, not measured. AF full-area bonds are behind Be and do not see the full exterior-to-interior gradient. The outer 30:1 scarf is screened at an assumed 10 Barrer; its adhesive is the 028 70 g/m2 route, not silently replaced with AF163.",
  "proposed_next": "Measure scarf and metal/adhesive assembly permeance, pinholes and surface defects. Validate the actual panel boundary path."
}
```

### N578 — NFI-034-P3-RESIN-AND-SURFACES

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/6`.

```json
{
  "id": "NFI-034-P3-RESIN-AND-SURFACES",
  "tag": "PROJECTION",
  "finding": "SiC tubes remain SiC in both 022c rows; CFRP is only the end wrap. The wrap outgassing proxy uses a different graphite/epoxy. A 0.1 g/m2 SiC surface inventory and 1 wt% unspecified attachment/seal inventories are assumptions.",
  "proposed_next": "Measure actual end-wrap resin, cured joint adhesive, membrane attachment and cleaned ceramic surface gas release."
}
```

### N587 — NFI-034-PHASE-VERSUS-LIFT

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/15`.

```json
{
  "id": "NFI-034-PHASE-VERSUS-LIFT",
  "tag": "QUESTIONABLE",
  "finding": "Desorbed material was already aboard: gas-phase inventory consumes a pressure allowance without adding the same mass again to the vehicle. Net external ingress adds mass. Passive getters retain it; pumps can expel it.",
  "proposed_next": "Keep separate ledgers for free gas, net external uptake and material phase transfer."
}
```

### N666 — NFI-038-TRAPPED_GAS

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/15`.

```json
{
  "id": "NFI-038-TRAPPED_GAS",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Every core cell/tube bore must be evacuated or charged",
  "evidence": "034 estimates substantial ambient trapped gas.",
  "resolution_needed": "Measure communication, initial inventory, transient gas release and structural impact of vents.",
  "tests": [
    "T2",
    "T9"
  ]
}
```

### N667 — NFI-038-VACUUM_SPECIES

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/16`.

```json
{
  "id": "NFI-038-VACUUM_SPECIES",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Pressure, free gas and added mass are different constraints",
  "evidence": "034: water pressure, finite desorption and external uptake differ.",
  "resolution_needed": "Measure species and temperature, retain outgas pressure but do not double-count solid mass; use hot pressure limit.",
  "tests": [
    "T9"
  ]
}
```

### C061 — NFI-034-LEAK-RATES

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/0`.

```json
{
  "id": "NFI-034-LEAK-RATES",
  "tag": "PROJECTION",
  "finding": "No full-hull or seam/node leak rate is measured. The 1e-5/1e-3/0.1 mbar L/s per metre and per node values are scenarios, with a separate port allowance. They span four decades but are not bounds.",
  "proposed_next": "Measure assembled pressure rise and test gas-specific leaks at service load and temperature; compare with the 24 h acceptance budget.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C062 — NFI-034-SOURCE-TO-SERVICE

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/1`.

```json
{
  "id": "NFI-034-SOURCE-TO-SERVICE",
  "tag": "PROJECTION",
  "finding": "500 m fixes nominal pressure, not humidity or membrane temperature. Water rates are source-condition values mapped to a chosen 1 kPa driving partial pressure. Temperature dependence and humidity-gradient dependence are not measured.",
  "proposed_next": "Measure permeance at the intended thermal/humidity envelope. Keep the constant-source and partial-pressure model results distinct.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C063 — NFI-034-TML-NOT-RATE

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/2`.

```json
{
  "id": "NFI-034-TML-NOT-RATE",
  "tag": "QUESTIONABLE",
  "finding": "NASA E595 uses 125 C for 24 h. TML is neither kg/day at 284.9 K nor a certified finite flight inventory. Historical cures/lots and several material/gauge proxies differ. CVCM is a subset, not added to TML.",
  "proposed_next": "Obtain actual material inventory and service-temperature desorption curves; retain unmatched-data tags.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C064 — NFI-034-CONDITIONING

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/3`.

```json
{
  "id": "NFI-034-CONDITIONING",
  "tag": "PROJECTION",
  "finding": "Reference calculations assume 90% of the chosen release inventory was removed and the residue releases exponentially with one-day time constant. Neither fraction nor kinetics is demonstrated.",
  "proposed_next": "Demonstrate the required residual gas load after conditioning; do not treat this as a prescribed bake process.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C065 — NFI-034-CORE-AND-TUBE-VENTING

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/4`.

```json
{
  "id": "NFI-034-CORE-AND-TUBE-VENTING",
  "tag": "PROJECTION",
  "finding": "Unvented P2 honeycomb would retain about 43.388 kg of ambient air. P3 tube bores would retain about 88.153/76.110 kg. Base cases require these spaces to share the evacuation path. Trapped gas is onboard mass even before it leaks into the main cavity.",
  "proposed_next": "Establish and qualify internal vent paths, pressure equalization and residual gas inventory. Any geometric vent change requires structural review.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C066 — NFI-034-P2-PERMEATION-PATH

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/5`.

```json
{
  "id": "NFI-034-P2-PERMEATION-PATH",
  "tag": "PROJECTION",
  "finding": "Intact Be bulk ambient-gas permeation is set to zero in the screen, not measured. AF full-area bonds are behind Be and do not see the full exterior-to-interior gradient. The outer 30:1 scarf is screened at an assumed 10 Barrer; its adhesive is the 028 70 g/m2 route, not silently replaced with AF163.",
  "proposed_next": "Measure scarf and metal/adhesive assembly permeance, pinholes and surface defects. Validate the actual panel boundary path.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C067 — NFI-034-P3-RESIN-AND-SURFACES

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/6`.

```json
{
  "id": "NFI-034-P3-RESIN-AND-SURFACES",
  "tag": "PROJECTION",
  "finding": "SiC tubes remain SiC in both 022c rows; CFRP is only the end wrap. The wrap outgassing proxy uses a different graphite/epoxy. A 0.1 g/m2 SiC surface inventory and 1 wt% unspecified attachment/seal inventories are assumptions.",
  "proposed_next": "Measure actual end-wrap resin, cured joint adhesive, membrane attachment and cleaned ceramic surface gas release.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C070 — NFI-034-GAS-COVERAGE

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/9`.

```json
{
  "id": "NFI-034-GAS-COVERAGE",
  "tag": "PROJECTION",
  "finding": "Kapton has sourced CO2/O2/H2/N2/He data but not Ar; Ar is set to N2. Mylar has sourced O2 only: other gas ratios are assumed, including N2, and checked in a sensitivity. Outgassing is water-equivalent with a 5 mass% H2 sensitivity, not measured composition.",
  "proposed_next": "Measure a full gas spectrum, including noble gases and organics; distinguish pressure from gas mass.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C076 — NFI-034-PHASE-VERSUS-LIFT

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/15`.

```json
{
  "id": "NFI-034-PHASE-VERSUS-LIFT",
  "tag": "QUESTIONABLE",
  "finding": "Desorbed material was already aboard: gas-phase inventory consumes a pressure allowance without adding the same mass again to the vehicle. Net external ingress adds mass. Passive getters retain it; pumps can expel it.",
  "proposed_next": "Keep separate ledgers for free gas, net external uptake and material phase transfer.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C078 — NFI-CHECK034-INPUT-COMPLETENESS

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/17`.

```json
{
  "id": "NFI-CHECK034-INPUT-COMPLETENESS",
  "tag": "PROJECTION",
  "finding": "Kapton includes 0.1 kg of unconditioned seals/titanium-surface release inventory in RESULTS, but INPUTS has no scalar for it. At the reference 10% retained fraction this contributes 0.01 kg to the 1.0249312800972046 kg residual inventory. The full-area AF bond also uses 1250 kg/m3 in the solid-volume reconstruction although INPUTS names that density only for scarf adhesive; 019/021b carry the same generic adhesive-density assumption. These are reconstructed assumptions, not measured material properties.",
  "proposed_next": "Add named inputs for Kapton residual seals/surface inventory and AF bond density, with provenance and service-data tags. RECONSTRUCTION-ASSUMPTIONS.json makes both explicit here."
}
```

### C079 — NFI-CHECK034-CORE-VOID-CONVENTION

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/18`.

```json
{
  "id": "NFI-CHECK034-CORE-VOID-CONVENTION",
  "tag": "QUESTIONABLE",
  "finding": "The reported 37.31646143905225 m3 honeycomb void is recovered by subtracting full-area AF volume 0.2945010968475796 m3 and core splice volume 0.012181226862401973 m3 from A*t_core-core_mass/2700. Without that unstated placement convention the independent values are 37.62314376276223 m3, 43.744289548973256 kg trapped air, and 0.8946683119525318 of the gas allowance, versus filed 37.31646143905225 m3, 43.38771114998258 kg and 0.887375488189865. This is an unresolved manufactured-section convention, not a discrepancy in the quoted endurance calculation.",
  "exact_initial_differences": [
    {
      "path": "/geometry/P2/core_void_m3",
      "owner": 37.31646143905225,
      "independent": 37.62314376276223,
      "difference_independent_minus_owner": 0.3066823237099854,
      "tolerance": 9.46329228781045e-08,
      "pass": false,
      "category": "independently_derived"
    },
    {
      "path": "/geometry/P2/unvented_core_air_kg",
      "owner": 43.38771114998258,
      "independent": 43.744289548973256,
      "difference_independent_minus_owner": 0.35657839899067767,
      "tolerance": 1.0677542229996517e-07,
      "pass": false,
      "category": "independently_derived"
    },
    {
      "path": "/systems_ledger/P2_unvented_core_fraction_of_internal_gas_row",
      "owner": 0.887375488189865,
      "independent": 0.8946683119525318,
      "difference_independent_minus_owner": 0.007292823762666822,
      "tolerance": 2.177475097637973e-08,
      "pass": false,
      "category": "independently_derived"
    }
  ],
  "proposed_next": "Specify the reference core envelope and measured adhesive/fillet/splice displacements. Keep the two interpretations separate until a manufactured section establishes them."
}
```

### C177 — 040-15-unvented_cells

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/14`.

```json
{
  "id": "040-15-unvented_cells",
  "tag": "PROJECTION",
  "open_issue": "Ambient trapped gas consumes lift and changes inner/outer face load paths; late venting is a separate transient.",
  "grounding": "Specify and demonstrate cell venting or analyze/test the sealed-cell pressure distribution and failure transient."
}
```

### C179 — 040-17-leak_and_permeation

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/16`.

```json
{
  "id": "040-17-leak_and_permeation",
  "tag": "PROJECTION",
  "open_issue": "Reference .001 mbar L/(s m) seam leakage and 10 Barrer scarf permeability are scenarios, not measured acceptances.",
  "grounding": "Measure conditioned full-seam/port leakage and species permeation under mission pressure and temperature."
}
```

### C180 — 040-18-conditioning

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/17`.

```json
{
  "id": "040-18-conditioning",
  "tag": "PROJECTION",
  "open_issue": "90% inventory removal, one-day release kinetics and water-only desorption composition are unverified.",
  "grounding": "Measure finite species inventories and desorption rates after a validated conditioning process."
}
```

### C239 — NFI-044-VACUUM-SERVICE

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/15`.

```json
{
  "id": "NFI-044-VACUUM-SERVICE",
  "finding": "Gas-cycle amplitudes use assumed leak acceptance, permeability and 90% conditioning. Full venting can change release inventory; it is not equivalent to top-up.",
  "evidence_needed": "Whole-hull leak/outgassing tests and a defined vent/reconditioning/power service protocol."
}
```

## R046 — ground-side thermal environment

**Original question:** Thermal balance averages sky and ground radiation; a hot apron, heat island or hangar is not bounded and the core-limit conclusion could invert.

### N065 — NFI-016-THERMENV

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-THERMENV",
  "rank": 9,
  "gap": "The thermal balance averages sky (260 to 275 K) and ground radiation and gives a no-convection bound of 313.5 K, under the QUESTIONABLE H35 service limit 343 to 353 K; but a hot apron, heat island, or hangar radiates from the ground side and is not bounded here.",
  "direction": "Re-run the balance for named ground conditions (asphalt apron, hangar wall); measure emissivity of the actual face finish.",
  "effect": "The core-limit conclusion could invert on a hot-ground site."
}
```

## R047 — thermal mismatch, cycling and fatigue of bonded faces and joints

**Current 030c:** 044: original six-pad core static screen .7143; plate-only damage-one index949.846days is not hull life. 037b thermal-only core projection18816days uses dense-core/mean-stress transfers. A+36.661kg pad/scarf scenario does not close Be/scarf life or mass. Qualified hull life remains null.

**Original question:** Property loss at temperature is datasheet-class only; no derate curves pinned and daily-cycle fatigue of core and adhesive is unquantified.

### N059 — NFI-016-CTE

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-CTE",
  "rank": 3,
  "gap": "CTE mismatch SiC 4.5e-6 vs PVC 60e-6 per K drives sandwich shear-lag at 283 kPa per 30 K face-core difference (567 kPa at 60 K), against a QUESTIONABLE H35 shear strength of 0.40 to 0.55 MPa: one-off SF 1.41 to 1.94 at 30 K, 0.71 to 0.97 at 60 K, cycled daily. Not one of the five scored modes; no fatigue law.",
  "direction": "Bond-line and core shear coupon under thermal cycling over the full daily band; pin DIAB H35 shear strength and modulus; add the mismatch mode to the scored set.",
  "effect": "A new structural failure mode at the 009 point, unquantified for the life of the hull."
}
```

### N066 — NFI-016-PROPTEMP

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-PROPTEMP",
  "rank": 10,
  "gap": "Property loss at temperature is datasheet-class only: H35 derates above 50 to 60 C, SiC is flat far above this range, and the aluminium family derates above about 150 C, not reached. No derate curves are pinned and the daily cycle fatigue of core and adhesive is not quantified.",
  "direction": "Pin derate curves for the core and adhesive against the measured daily band; couple to NFI-016-CTE.",
  "effect": "The scored five modes use room-temperature properties for a cycling structure."
}
```

### N188 — NFI-020-THERMAL-FATIGUE

Source `rpt-ref-3e02218a03708a878faa`; original file `unpublished-local-ref:3fe2376964ec428a; pointer `retained original identity`.

```json
{
  "id": "NFI-020-THERMAL-FATIGUE",
  "rank": 4,
  "tag": "QUESTIONABLE",
  "claim": "Daily thermal-cycle life of the pressure-loaded Be/HRH10 joint is UNKNOWN.",
  "optimistic": {
    "assumed_delta_alpha_per_K": 5e-06,
    "assumed_delta_T_K": 30,
    "screen_peak_shear_MPa": 0.05770430820956852,
    "bulk_smooth_zero_mean_benchmark_cycles": 10000000
  },
  "conservative": {
    "assumed_delta_alpha_per_K": 2e-05,
    "assumed_delta_T_K": 60,
    "screen_peak_shear_MPa": 0.46163446567654814,
    "qualified_joint_cycles": null
  },
  "sources": [
    {
      "id": "S02",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/c2eca2d0f75e11ee9aa0f6c265376dea"
    },
    {
      "id": "S03",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6"
    },
    {
      "id": "S05",
      "url": "https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf?fn=AF163-2.pdf"
    },
    {
      "id": "S07",
      "url": "https://www-pub.iaea.org/MTCD/Publications/PDF/Pub23vol5_web.pdf"
    }
  ],
  "needed_to_ground": "Measure effective directional core/face/adhesive expansion, service temperature histories, restraint and fatigue under representative compressive mean load. Test the assumed 10,958 daily cycles if a 30-year target is adopted.",
  "effect_on_lead": "016 concerned SiC/PVC; only its scalar equation is reused. Gc is not shear strength. The upper elastic thermal screen may exceed yield; no fatigue margin or life can be inferred.",
  "closed_by_this_card": false
}
```

### N239 — NFI-028-18

Source `rpt-ref-2519e14e5d71b9eb18f3`; original file `unpublished-local-ref:fdfeeedfea497f71; pointer `retained original identity`.

```json
{
  "id": "NFI-028-18",
  "status": "OPEN",
  "tag": "PROJECTION",
  "technology_state": "PROJECTION",
  "hull_adoption_state": "PROJECTION",
  "assumption": "Thermal, cyclic and assembly compatibility",
  "today_value": "No post-form/post-join envelope established for the selected route",
  "required_or_budget_target": "Maintain the adopted properties and leak/shape limits through assembly and service.",
  "needed_evidence": "CTE residual stress, polymer heat exposure, corrosion, fatigue and final weld/braze access; do not equate a furnace coupon with a closed 20 m hull.",
  "factor_to_216_427kg_allowance": null,
  "factor_reason": "No complete quantified route, or this is a strength/geometric condition rather than an independent joining bill."
}
```

### N551 — NFI-036-environment

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/13`.

```json
{
  "id": "NFI-036-environment",
  "status": "OPEN",
  "issue": "Cover mission temperature and cycling in the strength basis.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "post_process_and_operating_envelope": true
  },
  "today": {
    "published_strengths": "mostly room-temperature"
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "sr200; nasa4397; 027/028b",
  "closure": "Temperature-dependent yield/fracture and cyclic/thermal durability for the actual face and joint."
}
```

### N702 — NFI-036-environment

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/13`.

```json
{
  "id": "NFI-036-environment",
  "status": "OPEN",
  "issue": "Cover mission temperature and cycling in the strength basis.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "post_process_and_operating_envelope": true
  },
  "today": {
    "published_strengths": "mostly room-temperature"
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "sr200; nasa4397; 027/028b",
  "closure": "Temperature-dependent yield/fracture and cyclic/thermal durability for the actual face and joint.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### C029 — N039-08

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/7`.

```json
{
  "id": "N039-08",
  "issue": "SiC on Be thermal mismatch",
  "detail": "11.3 ppm/C (SR-200) against 4.02 ppm/K (Hexoloy-SA). The 25.1 K climate swing is included (1.83e-4 strain). Every 100 K between a hot cure and service would lock in 7.3e-4 strain, of the order of the membrane strain (about 1e-3).",
  "to_close": "A room-temperature-cure route, or the CTE-matched Be frame (C2b).",
  "tag": "QUESTIONABLE"
}
```

### C055 — NFI-CHECK037-NONUNIFORM-BOW

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/17`.

```json
{
  "id": "NFI-CHECK037-NONUNIFORM-BOW",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "Saying uniform mismatch does not bow a member does not evaluate circumferential tube heating, asymmetric film traction or thermal imperfections.",
  "proposed_fix": "Calculate thermal curvature and load eccentricity for actual tube and attachment temperatures and add the resulting imperfection to the member stability calculation."
}
```

### C095 — NFI-037b-SUSTAINED-SHEAR

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/6`.

```json
{
  "id": "NFI-037b-SUSTAINED-SHEAR",
  "tag": "QUESTIONABLE",
  "claim": "The residual is a sustained shear on the core. On the minimum-average W strength (25 psi) it reads 0.83 at a free edge after the 250 F cure. Honeycomb creep and day-night fatigue under sustained shear are not sourced.",
  "needed_to_ground": "Sustained-load and cyclic shear data for CR-III 5056 3/8-1.0."
}
```

### C134 — C039-08

Source `rpt-ref-20ab4b33b504a00ad3b6`; original file `unpublished-local-ref:75b66f0986a98c9b; pointer `/rows/7`.

```json
{
  "id": "C039-08",
  "topic": "THERMAL-JOINT-EQUILIBRIUM",
  "status": "QUESTIONABLE",
  "objection": "SiC tube capacity uses the thermal compression envelope while line force and sleeve mass use only mechanical compression.",
  "evidence": "SUPPLEMENTARY.json: 55.521 kN mechanical versus 63.974 kN compression envelope; difference 8.454 kN. This does not affect the Be-on-Be thermal comparison.",
  "proposed_fix": "Build signed hot/cold equilibrium cases and propagate member forces through sleeve, bond, core-line and peel calculations. Do not combine incompatible hot-face and cold-tube envelopes as one physical load case.",
  "disposition": "Record for owner revision; check completed"
}
```

### C192 — NFI-037b-SUSTAINED-SHEAR

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/6`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-SUSTAINED-SHEAR",
  "tag": "QUESTIONABLE",
  "claim": "The residual is a sustained shear on the core. On the minimum-average W strength (25 psi) it reads 0.83 at a free edge after the 250 F cure. Honeycomb creep and day-night fatigue under sustained shear are not sourced.",
  "needed_to_ground": "Sustained-load and cyclic shear data for CR-III 5056 3/8-1.0."
}
```

### C210 — NFI-043-12

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/11`.

```json
{
  "id": "NFI-043-12",
  "status": "open",
  "topic": "Exposure and lifetime",
  "finding": "Service duration, cycles, environment, slow crack growth and post-proof damage are unspecified.",
  "needed": "Defined lifetime/load spectrum and matched environmental growth, aging, handling and fatigue evidence.",
  "effect": "Lifetime failure probability remains null. Ideal instantaneous proof truncation cannot establish lifetime survival.",
  "stops_other_work": false
}
```

### C219 — NFI-CHECK037b-CREEP-STATEMENT

Source `rpt-ref-4bf25e71ae0c2ca315e2`; original file `unpublished-local-ref:0360eb0aa78daa3e; pointer `/items/4`.

```json
{
  "id": "NFI-CHECK037b-CREEP-STATEMENT",
  "tag": "QUESTIONABLE",
  "status": "OPEN",
  "finding": "The statement that creep is none in service overstates a finite-duration displacement result. A zero table reading at one condition is not zero creep over all service histories, and no stress-relaxation fraction follows.",
  "exact": {
    "reported_180F_creep_in": 0.0002,
    "converted_displacement_um": 5.08,
    "duration_h": 192
  },
  "disposition": "Replace the absolute statement with the measured conditions and preserve the unmeasured relaxation/cyclic-life qualification.",
  "carries_owner_rows": [
    "NFI-037b-SUSTAINED-SHEAR",
    "NFI-037b-STRESS-FREE-T"
  ],
  "blocking": false
}
```

### C224 — NFI-044-SPECTRUM

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/0`.

```json
{
  "id": "NFI-044-SPECTRUM",
  "finding": "Annual occurrences, ordinary weather range, altitude mission and handling cycles are declared scenarios, not operating records.",
  "evidence_needed": "A defined mission plus measured pressure, face temperatures, accelerations, mooring forces and rainflow-counted histories; joint occurrence and dwell statistics."
}
```

### C227 — NFI-044-CORE-DENSITY

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/3`.

```json
{
  "id": "NFI-044-CORE-DENSITY",
  "finding": "The source 5056 fatigue coupons are 5.3 pcf, versus 1.0 pcf hull core. Normalization by static strength is not a validated density/cell/foil transfer.",
  "evidence_needed": "CR-III 5056 3/8-1.0 L/W/off-axis shear S-N tests, including actual depth, foil state, curved faces and node/splice manufacturing."
}
```

### C228 — NFI-044-MEAN-STRESS

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/4`.

```json
{
  "id": "NFI-044-MEAN-STRESS",
  "finding": "Goodman-style correction using absolute core shear mean is an assumed transfer from fully reversed tests; creep and residual-stress relaxation are not established.",
  "evidence_needed": "Core and adhesive fatigue under the actual residual mean, pressure-temperature sequence and sustained dwell."
}
```

### C229 — NFI-044-LOW-STRESS-HORIZON

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/5`.

```json
{
  "id": "NFI-044-LOW-STRESS-HORIZON",
  "finding": "The decade contains over one million pad cycles. Required low-amplitude core lives extend beyond the source test range; finite semilog extrapolation does not demonstrate them.",
  "evidence_needed": "Longer relevant-amplitude runouts and an accepted lower-bound extrapolation/scatter treatment."
}
```

### C240 — NFI-044-ENVIRONMENT-AGING

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/16`.

```json
{
  "id": "NFI-044-ENVIRONMENT-AGING",
  "finding": "Room-temperature S-N screens do not supply ten-year humidity, salt, corrosion, UV/coating damage, creep, fretting or vacuum/environmental bond retention.",
  "evidence_needed": "Relevant environmental conditioning and fatigue/dwell testing with documented acceleration and retention factors."
}
```

### S008 — NFI-030C-LIFE-AND-COMMON-BASIS

Source `rpt-1228-mainline030c-design-register-1020`; original file `unpublished-local-ref:3c01fd6db28be861; pointer `/rows/7`.

```json
{
  "id": "NFI-030C-LIFE-AND-COMMON-BASIS",
  "title": "040 common static/service account does not close 044 life or 043 reliability.",
  "finding": "040 adopts 037b but uses its own resized one-pad/wind/weather models. 044's six-pad spectrum and 60:1 scarf option belong to older R10 geometries, so its 36.661 kg cannot simply be added as a validated R30 retrofit. 043 uses 022d/026b stress/count cases, not 041's 750-member f5 frame. Carry each as an unresolved geometry-dependent requirement.",
  "status": "OPEN",
  "blocks_progress": false,
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## R048 — Be cost, supply and controlled processing

**030b source history:** CHECK-020 adds omitted Be doublers to the historical supply/cost comparison: its stated stock totals become $44.70m/$267.10m under those dated assumptions. No fresh price or purchase recommendation is made here.

**Original question:** Finished-sheet capacity, current S200F/SR200 prices and fabrication yields are unknown; the multipliers are owner stress cases.

### N190 — NFI-020-SUPPLY-QUOTE-YIELD

Source `rpt-ref-3e02218a03708a878faa`; original file `unpublished-local-ref:3fe2376964ec428a; pointer `retained original identity`.

```json
{
  "id": "NFI-020-SUPPLY-QUOTE-YIELD",
  "rank": 6,
  "tag": "QUESTIONABLE",
  "claim": "Finished-sheet capacity, current S200F/SR200 prices and fabrication yields are UNKNOWN.",
  "optimistic": {
    "historical_world_mine_output_t": 433,
    "year": 2024,
    "assumed_S200F_USD_kg": 4800,
    "assumed_SR200_USD_kg": 9600,
    "assumed_yield": 0.85,
    "actual_face_sheet_stock_USD": 39512092.5407217
  },
  "conservative": {
    "world_mine_output_estimate_t": 430,
    "year": 2025,
    "assumed_S200F_USD_kg": 9600,
    "assumed_SR200_USD_kg": 24000,
    "assumed_yield": 0.5,
    "actual_face_sheet_stock_USD": 167926393.2980672
  },
  "sources": [
    {
      "id": "S01",
      "url": "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-beryllium.pdf"
    },
    {
      "id": "S02",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/c2eca2d0f75e11ee9aa0f6c265376dea"
    },
    {
      "id": "S03",
      "url": "https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6"
    }
  ],
  "needed_to_ground": "Obtain grade/gauge/size-specific lot quotations, lead time, rolling capacity, scrap recovery and installed-panel yield. No vendor contact or purchase was made in this task.",
  "effect_on_lead": "USGS $1600/kg is contained Be in copper master alloy. Multipliers are owner stress cases, not supplier prices or confidence intervals. Mine-output shares do not prove availability.",
  "closed_by_this_card": false
}
```

### N191 — NFI-020-CONTROLLED-PROCESS-COST

Source `rpt-ref-3e02218a03708a878faa`; original file `unpublished-local-ref:3fe2376964ec428a; pointer `retained original identity`.

```json
{
  "id": "NFI-020-CONTROLLED-PROCESS-COST",
  "rank": 6,
  "tag": "QUESTIONABLE",
  "claim": "Controlled fabrication costs are an explicit open procurement item.",
  "optimistic": {
    "route": "existing equipped contractor",
    "owner_allowance_fraction_of_conversion_F": 0.1
  },
  "conservative": {
    "route": "dedicated controlled capacity",
    "owner_allowance_fraction_of_conversion_F": 0.3,
    "separate_capital_C_USD": null
  },
  "sources": [
    {
      "id": "S08",
      "url": "https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.1024"
    }
  ],
  "needed_to_ground": "Specify jurisdiction and process steps; get a contractor quote including enclosure/extraction or wet processing, exposure assessment, waste/hygiene and surveillance obligations. Price F and C separately.",
  "effect_on_lead": "Adds process and capital burdens without stopping this estimate card. Cost multipliers are assumptions, not OSHA charges or a substitute for the actual exposure-control specification.",
  "closed_by_this_card": false
}
```

### N403 — NFI-020C-DOUBLER-BERYLLIUM

Source `rpt-ref-35706d7a2ae7e951590b`; original file `unpublished-local-ref:1df5aace4f5947b0; pointer `/items/2`.

```json
{
  "id": "NFI-020C-DOUBLER-BERYLLIUM",
  "rank": 3,
  "kind": "NFI row",
  "tag": "PROJECTION",
  "against": "CARD.md sections 1 and 3",
  "claim": "Section 3's splice doublers are full-gauge Be, but section 1 buys and prices only the faces.",
  "numbers": {
    "Be_doubler_kg_opt_con": [
      459.11634213163603,
      2066.023539592362
    ],
    "Be_total_kg": [
      3957.5828691747024,
      5564.490066635428
    ],
    "share_of_mine_output_percent": [
      0.9139914247516633,
      1.2940674573570763
    ],
    "sheet_stock_cost_USDm": [
      44.69740652244371,
      267.09552319850053
    ],
    "card_cost_USDm": [
      39.51209254072168,
      167.92639329806718
    ],
    "cost_increase_percent": [
      13.12335958005255,
      59.05511811023621
    ]
  },
  "proposed_fix": "Count the doubler Be in the section 1 supply share and sheet cost, paired the way section 3 pairs panels and joints.",
  "effect_on_lead": "No SF effect; procurement and cost rise."
}
```

### C103 — NFI-CHECK038-COST_BASIS

Source `rpt-ref-2beb70a569266cf0297d`; original file `unpublished-local-ref:0746af9cb88f6eb1; pointer `/items/1`.

```json
{
  "id": "NFI-CHECK038-COST_BASIS",
  "status": "OPEN",
  "blocking": false,
  "issue": "Campaign and Be stock costs are projections without specimen-specific supplier evidence.",
  "evidence": "Cost sums reproduce. Official UW/UNR rates are partial service anchors and do not establish Be acceptance or turnkey costs.",
  "resolution_needed": "Before an authorized purchase, define quantities, fixtures, hours, process/yield, material cost, analysis and facility scope; retain quotes separately from assumptions.",
  "tests": [
    "T1",
    "T2",
    "T3",
    "T4",
    "T5",
    "T6",
    "T7",
    "T8",
    "T9"
  ],
  "classification": "inherited evidence gap"
}
```

### C147 — N042-11

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/10`.

```json
{
  "id": "N042-11",
  "issue": "Be dust limits where scarfs are cut",
  "detail": "OSHA 1910.1024 sets a PEL of 0.2 ug/m3, so scarfing and trimming Be is regulated-area work (sub-worker row). JPL had all dust-producing Be operations done at the supplier. The route puts every Be cut before assembly.",
  "to_close": "Supplier-side scarfing and handling plan.",
  "tag": "QUESTIONABLE"
}
```

### C151 — N042-15

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/14`.

```json
{
  "id": "N042-15",
  "issue": "Cost class is not scaled",
  "detail": "Reflector-grade surfaces cost GBP 2-5M to refurbish or replace a 15 m dish (JCMT, 2011 talk) and about $5-6M per 10 m SMT (1987). Nothing here scales that to a 20 m sphere. Be stock is 020's $39.5-167.9M.",
  "to_close": "Costed route after F1.",
  "tag": "QUESTIONABLE"
}
```

### C214 — NFI-043-16

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/15`.

```json
{
  "id": "NFI-043-16",
  "status": "open",
  "topic": "Qualification and recurring cost",
  "finding": "Geometry, loads, complete inspection and proof coverage imply high/custom qualification and recurring inspection cost classes, but no supplier quotation or process yield is available.",
  "needed": "Supplier capability and quotations, fixture design, throughput, inspection detection performance, scrap rate and surveillance plan for the qualified process.",
  "effect": "No dollar estimate, cycle time or scrap forecast is asserted. No supplier contact or purchase was made.",
  "stops_other_work": false
}
```

## R049 — brittle face buildability SiC Be

**Original question:** SiC and beryllium rank only on compressive membrane modes; flexure, fracture toughness, toxicity, joining and ductility are outside the formulas.

### N134 — NFI-008-BRITTLE-FACES

Source `rpt-ref-45da79edf548b064b228`; original file `unpublished-local-ref:20c691c11e9fda46; pointer `retained original identity`.

```json
{
  "id": "NFI-008-BRITTLE-FACES",
  "issue": "SiC and beryllium rank on compressive membrane modes only. SiC flexural strength (~380 MPa) and fracture toughness, and beryllium toxicity, joining and low ductility, are outside both formulas.",
  "effect": "A high least-SF here is not a buildable face; bending, impact, attachment and thermal paths can govern.",
  "needed": "A fracture/joining assessment before either is carried as a face material."
}
```

## R050 — ground handling and dent survey

**Original question:** Growth of diameter from 20 to 100 m raises ground area and wind force 25-fold and overturning moment 125-fold; point attachments, transport, launch and landing fall outside uniform-pressure modes.

### N064 — NFI-016-HANDLE

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-HANDLE",
  "rank": 8,
  "gap": "Ground handling of a 4645 kg, 20 m vacuum sphere has no concept, cradle, or transport plan; core-safe pad pressure target is 250 kPa or less, and any handling dent is an imperfection feeding the already-severe 0.20 knockdown.",
  "direction": "Specify cradle geometry and pad pressure; define a dimensional inspection and imperfection survey after every move, tied to the knockdown basis.",
  "effect": "A dent below the survey threshold enters the buckling knockdown unmeasured."
}
```

### N110 — NFI-027-HANDLING

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-HANDLING",
  "tag": "PROJECTION",
  "issue": "Diameters grow 20→100 m, projected ground area and wind force at fixed speed grow 25-fold, characteristic overturning moment 125-fold. Point attachments, transport, launch and landing are outside uniform-pressure modes.",
  "next_evidence": "Design and weigh handling/anchoring/assembly equipment and verify concentrated and asymmetric loads, gust response and damage tolerance."
}
```

## R051 — P3 member force: pRs/(2*sqrt3) on the equilateral frame (FIX-A), two-way 2V-4 members

**030b source history:** Equilateral membrane force remains pRs/(2sqrt(3)). 026 additionally corrects tributary line load to ps/(2sqrt(3)); CHECK-027 flags the inherited two-way member-force continuation. Grid and local loading must remain explicit.

**Original question:** P3 assumes tributary width equals spacing, pinned members, a real-valued equal triangulation, and ignores tube crippling; Euler pressure scales with I, E and 1/s^3.

### N018 — NFI-CHK011B-FORCE

Source `rpt-check011b-opus-1020`; original file `unpublished-local-ref:252e7a0b939c4177; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK011B-FORCE",
  "state": "demonstrated",
  "direction": "conservative",
  "proposed_fix": "FIX-A",
  "note": "The card's member force N = pRs/2 is the two-way arch resultant, but the frame it counts has M = 3V-6 members of length s. Statics fix their mean compression at 4*pi*R^3*p/(M*s) = pRs/(2*sqrt3) exactly (virial identity). The card's own Et=(2/sqrt3)EA/s with nu=1/3 gives the same strain. Geodesic trusses of 162 and 362 nodes solved by statics (rank complete, residual 6e-15) give mean C/(pRl/(2*sqrt3)) = 1.017 and 1.007, with a maximum of 600 kN at mean l 2.0 m. Each member carries 0.289*s^2 of film, not s^2/2. The force is inherited from MAINLINE-002's P3 rule (COMMON.md). Yield, Euler, local and Perry are sqrt3-conservative at a given tube. Re-optimised, SiC on the equilateral grid at k 0.2 is 1.408 and 6061 is 0.339. The member-end load at s 2.04 m is 562 kN, not 974 kN (022, 023).",
  "fix": "FIX-A: score the P3 members with N = pRs/(2*sqrt3) on the equilateral frame, or count a true two-way frame (M = 2V, V = 4*pi*R^2/s^2), then re-optimise."
}
```

### N213 — NFI-023-EQUILIBRIUM-FORCE

Source `rpt-ref-a4768f77870336c8cdbb`; original file `unpublished-local-ref:8fc6d5cd4b5f84d2; pointer `retained original identity`.

```json
{
  "id": "NFI-023-EQUILIBRIUM-FORCE",
  "value": "Equilateral N = p*R*s/(2*sqrt(3)) = 562166 N at s 2.04 m. p*R*s/2 = 973701 N is the two-way force.",
  "state": "exists today",
  "issue": "The first filing sized the equilateral grid at the two-way force. Yield, Euler, local and Perry were low by sqrt(3). Global was not. The sleeve total at equilibrium, with the radius held, does not depend on s.",
  "consequence": "Masses in the first report are the two-way masses. This card replaces them for the equilateral grid.",
  "next": "022b rescales with C*N^2/r for a sleeve and with the tube area for a braze."
}
```

### N247 — NFI-FRAME

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-FRAME",
  "linked_inputs_or_points": "P3",
  "questionable_assumption_or_gap": "Tributary width equals spacing, members are pinned, mesh is a real-valued equal triangulation, tube crippling ignored.",
  "direction_of_further_investigation": "Integer geodesic, end fixity, imperfection knockdown and local crippling.",
  "how_it_affects_margin_or_SF": "Euler pressure scales with I and E and inversely with s^3. Mass scales with edge count and area."
}
```

### N257 — NFI-FRAME

Source `rpt-mainline002-grok-strength-card-1019`; original file `unpublished-local-ref:f02996967e2f160d; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-FRAME",
  "gap": "Pinned Euler, tributary width equal to spacing, and no local crippling.",
  "direction": "Integer mesh, end fixity and crippling.",
  "effect": "Euler pressure scales with I. Section yield scales with area. Crippling could govern first."
}
```

### N374 — NFI-025-EQUILIBRIUM

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/6`.

```json
{
  "id": "NFI-025-EQUILIBRIUM",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "derived continuum equilibrium; discrete spherical application PROJECTION",
  "issue": "Uniform equilateral force correction is established for the stated continuum; full discrete topology and coupled film/load collection remain unresolved.",
  "factor": {
    "inherited_N_factor": 1,
    "consistent_uniform_triangular_N_factor": 0.5773502691896258,
    "fixed_point_stress_reduction_factor": 1.7320508075688772,
    "separate_optimistic_SiC_SF": 1.2057081881088565,
    "separate_mixed_CMC580_SF": 0.8711613194493811,
    "equilateral_mean_compression_at_original_Pa": 824658297.2240363,
    "inherited_mean_compression_at_original_Pa": 1428350069.6752675,
    "source_note_pin": {
      "path": "unpublished-local-ref:f1ad809d1efc520a",
      "sha256": "dc65f9c0d7585fbf3e57e3423fe48896a96425fd9f3abdcf49ce3b7cadaf7d8e",
      "matches": true
    }
  },
  "required_next_evidence": "MAINLINE-022b must reconcile discrete topology, load collection, actual member length/curvature, film spans and global stiffness together.",
  "note": "Amendment ord-admiral-rr2-mainline025-demand-082gpa-1020 and its pinned note confirm N=pRs/(2sqrt3). Both demands are scored in fixed and reoptimized principal tables. Extra arc rise must not reduce this equilibrium force; bending about the actual thrust line must be evaluated."
}
```

### N389 — NFI-CHECK-027-MEMBER-FORCE

Source `rpt-ref-7b45cb6b4d7f92067f8b`; original file `unpublished-local-ref:b86b45b7611fc7e9; pointer `/rows/0`.

```json
{
  "id": "NFI-CHECK-027-MEMBER-FORCE",
  "tag": "QUESTIONABLE",
  "issue": "The P3 continuation holds the 011b axial force p*R*s/2. On an equilateral grid the member force is p*R*s/(2*sqrt(3)). Yield, Euler, local and Perry are scored on the larger force. Global and film do not use it. The bay and radius bounds themselves are held."
}
```

### N391 — NFI-023-CHECK-OLD-FORCE

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/1`.

```json
{
  "id": "NFI-023-CHECK-OLD-FORCE",
  "status": "resolved_by_load_fix",
  "non_blocking": true,
  "field": "first filing member force",
  "reported": "973700.54672178N, pRs/2, applied to triangulated member count.",
  "check": {
    "equilateral_N": 562166.2727599056,
    "old_N": 973700.5467217801,
    "fixed_geometry_factors": {
      "yield": 1.732050807568877,
      "euler": 1.7320508075688772,
      "local": 1.732050807568877,
      "film": 1.0,
      "perry": 1.7320508075688772,
      "global": 1.0
    }
  },
  "evidence": [
    "independent global-cut/node/tributary derivations",
    "RESULTS.json"
  ],
  "next": "Carry the corrected force. The initial numbers are reproduced solely as superseded-load calculations."
}
```

### N499 — NFI-026-01

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/0`.

```json
{
  "id": "NFI-026-01",
  "tag": "QUESTIONABLE",
  "status": "open",
  "owner": "sciences",
  "issue": "011b local-member tributary share differs from equal triangular cell transfer",
  "evidence": "Two cells give w=2pA/(3s)=ps/(2sqrt(3)); inherited local checks used ps/2.",
  "implication": "Reconcile inherited local/Euler/Perry checks. This factor does not replace the separately inherited continuum global expression."
}
```

### C081 — NFI-C026B-RISE

Source `rpt-ref-b92330879d6ba35bd62c`; original file `unpublished-local-ref:21616ac9b36e6057; pointer `/rows/0`.

```json
{
  "id": "NFI-C026B-RISE",
  "issue": "Independent rise-8 force, pressure fan and geometry solve remains open.",
  "evidence": "simjob refused f6-m12-rise8 at PSI some avg10 7.89 >= 5.00. Nothing started; no retry; m24 rise8 not submitted.",
  "next_evidence": "A newly admitted independent rise8 m12/m24 calculation under fresh queue authority, including frozen spherical load.",
  "fields": {
    "rise8_m24.mean_compression_N": 538898.7411802687,
    "rise8_m24.mean_chord_thrust_N": 569787.8471557666,
    "rise8_m24.peak_moment_Nm": 177824.68854006825,
    "rise8_m24.bending_stress_Pa": 4248086375.1604,
    "rise8_m24.frozen_mean_compression_N": 513844.2503173434
  },
  "owner_numbers_not_independently_solved": true,
  "tag": "QUESTIONABLE",
  "status": "open",
  "blocks_card": false
}
```

### C084 — NFI-C026B-ENDPOINTS

Source `rpt-ref-b92330879d6ba35bd62c`; original file `unpublished-local-ref:21616ac9b36e6057; pointer `/rows/3`.

```json
{
  "id": "NFI-C026B-ENDPOINTS",
  "issue": "Endpoint chord-thrust statistics sample the first endpoint in the stored member orientation.",
  "evidence": "Independent first-end forces reproduce the owner. Both-end mean statistics differ by 8.697, 62.752 and 1331.327 N at f6/f4/f2; axial member compression is unaffected.",
  "next_evidence": "Name the sampled endpoint explicitly, or provide both ends and an orientation-invariant aggregate. Apply the same convention to any rise comparison.",
  "tag": "QUESTIONABLE",
  "status": "open",
  "blocks_card": false
}
```

### C206 — NFI-043-08

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/7`.

```json
{
  "id": "NFI-043-08",
  "status": "open",
  "topic": "Rise-8 force solution",
  "finding": "The owner reports large rise-8 moments and tensile stresses. The old independent 026b run was refused admission and produced no independently verified rise-8 force solution.",
  "needed": "An admitted independent geometry/load-path solution and verification, plus a separately defined selected-point rise case if transfer is intended.",
  "effect": "Owner rise-8 stresses remain attributed and unverified. Applying the same moment to another section is only a section conversion. No refusal was bypassed or retried for this card.",
  "stops_other_work": false
}
```

## R052 — P3 member shape: arcs vs straight chords, arc length

**Current 030c:** CHECK-037 corrects ten tube-mass fields to SiC density 3100 kg/m3 and arc lengths. Exact card/check pairs are in P3-TUBE-MASS-CORRECTIONS.json and LEDGER. They apply to historical 022c rows, not the already separate 022d lead.

**030b source history:** 026b eightfold rise retains538.899kN mean compression, rather than reducing it eightfold; elastic bending becomes4.248GPa. Fixed spherical nodal loads also fail the isolated-arch reduction. This controlled026 variant is not022's s1.1m rise8 section.

**Original question:** Members are scored as spherical arcs with N=p*R*s/2; straight chords would give sag 0.1125 m and bending stress 2.1-3.2 GPa, reported outside the least-SF minimiser.

### N309 — NFI-011B-ARC

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-ARC",
  "note": "Scored members are spherical arcs. N=p*R*s/2 is the 011 arch resultant. Straight chords are the alternative: at the rounded point the sag is 0.1125 m and the bending stress is 2.1065 to 3.1598 GPa. Those stresses are reported and are outside the least-SF minimiser."
}
```

### N313 — NFI-011B-LENGTH

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-LENGTH",
  "note": "Mass, Euler and Perry use the spacing s, as 011 did. The spherical arc is longer than the chord. That extra length was not substituted."
}
```

### N378 — NFI-025-CURVATURE

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/10`.

```json
{
  "id": "NFI-025-CURVATURE",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "PROJECTION",
  "issue": "Straight tubes cannot silently be scored as stress-free R10 m arcs.",
  "factor": {
    "original_arc_sag_if_s_is_chord_m": 0.05215601248190005,
    "cold_elastic_bend_outer_strain": 0.012368836237368609,
    "cold_elastic_bend_linear_stress_Pa": 5071222857.321129,
    "ratio_to_typical_380MPa_flexure": 13.345323308739813,
    "assumed_shape_error_m": 0.00204
  },
  "required_next_evidence": "Net-shape curved manufacture or a fully reanalyzed segmented/chord architecture; measured deviation from intended arc.",
  "note": "The cold-bending number is a kinematic linear-elastic warning for a finished straight member, not a claim that a stress-free manufactured curve carries that residual stress. Catalogue straightness of other products is not arc-error certification."
}
```

### N399 — NFI-023-CHECK-ARC-LENGTH

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/9`.

```json
{
  "id": "NFI-023-CHECK-ARC-LENGTH",
  "status": "open",
  "non_blocking": true,
  "field": "tube mass and Euler/Perry span",
  "reported": "011b and023 use chord spacing s as spherical-arc length.",
  "check": {
    "exact_arc_length_m": 2.043554024505062,
    "chord_m": 2.04,
    "length_ratio": 1.0017421688750303,
    "extra_tube_mass_at_unchanged_filed_area_kg": 7.856208800768033
  },
  "evidence": [
    "circular geometry derivation",
    "RESULTS.json"
  ],
  "next": "Carry the approximation explicitly or charge exact arc length and update Euler/Perry. Film sag and actual integer-node geometry remain outside this score."
}
```

### N617 — NFI-026B-03

Source `rpt-ref-8befdd4c89803adc44a8`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/2`.

```json
{
  "id": "NFI-026B-03",
  "tag": "QUESTIONABLE",
  "status": "computed_correction",
  "owner": "sciences",
  "issue": "Rise eightfold does not reduce lattice thrust eightfold",
  "evidence": "Frequency6 mean compression 538.899 kN at rise8 versus 550.519 kN at rise1; peak bending 4.248 GPa versus 0.059 GPa. Frozen spherical load gives513.844 kN and4.069 GPa.",
  "implication": "Reject isolated supported-arch thrust reduction as a lattice-equilibrium rule. Elastic stresses exceed plausible capability."
}
```

### N643 — NFI-026B-03

Source `rpt-ref-4a20323946ecafd56a6b`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/2`.

```json
{
  "id": "NFI-026B-03",
  "tag": "QUESTIONABLE",
  "status": "computed_correction",
  "owner": "sciences",
  "issue": "Rise eightfold does not reduce lattice thrust eightfold",
  "evidence": "Frequency6 mean compression 538.899 kN at rise8 versus 550.519 kN at rise1; peak bending 4.248 GPa versus 0.059 GPa. Frozen spherical load gives513.844 kN and4.069 GPa.",
  "implication": "Reject isolated supported-arch thrust reduction as a lattice-equilibrium rule. Elastic stresses exceed plausible capability."
}
```

### C042 — NFI-CHECK037-P3-ARC-MASS

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/4`.

```json
{
  "id": "NFI-CHECK037-P3-ARC-MASS",
  "tag": "QUESTIONABLE",
  "status": "open",
  "finding": "Every filed tube mass uses chord length; inherited capacities use arcs.",
  "proposed_fix": "Charge each SiC tube's inherited arc length. Eight unique corrected masses and ten exact result mismatches are supplied."
}
```

## R053 — P3 tube local buckling knockdown: SP-8007 gamma (FIX-B)

**030b source history:** 022d carries local gamma .552141 at its screened lead and flags the long-member shell/column transfer. 026's frame elastic instability exceeds the inherited local-wall screen, reached near lambda 2.03.

**Original question:** Local buckling keeps gamma = 1 at r/t 140.5, while the cited NASA report's curve gives 0.529; local capacity at the SiC point falls to 0.648.

### N019 — NFI-CHK011B-LOCAL-GAMMA

Source `rpt-check011b-opus-1020`; original file `unpublished-local-ref:252e7a0b939c4177; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK011B-LOCAL-GAMMA",
  "state": "demonstrated from the cited source",
  "direction": "optimistic",
  "proposed_fix": "FIX-B",
  "note": "Local buckling keeps gamma = 1 at r/t 140.5. NASA SP-8007, the source 011 cites for the 0.6, gives gamma = 1-0.901*(1-exp(-sqrt(r/t)/16)) = 0.529. Local at the card's SiC point is then 0.648. Re-optimised with gamma, SiC on the equilateral grid at k 0.2 is 1.075 (r/t 94), two-way is 0.967, and with FIX-A as well 1.205 and 1.083. At 100 kg systems and a 5% margin these are 1.130 and 1.015.",
  "fix": "FIX-B: apply SP-8007's gamma to the local mode and re-optimise."
}
```

### N150 — NFI-011-LOCAL-KD

Source `rpt-ref-f21d4bd21d2026511818`; original file `unpublished-local-ref:b5c9a6937c19e542; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-011-LOCAL-KD",
  "gap": "sigma_local = 0.6*E*t_w/r_o is SP-8007 classical with gamma=1 (no imperfection knockdown). At the aluminum best, local sits 3.9x above the least SF, so the answer is robust; at the T700 best the margin is 1.18x, and a gamma of 0.65 would pull that point's local to ~0.59.",
  "direction": "Re-optimise r_o under a knocked-down local curve: at s=1 the local margin is 2.6x, so the material conclusion (T700 least ~0.76, yield-bound) survives down to gamma ~0.29 after re-optimisation.",
  "effect": "The best-point geometry moves; the least SF per material does not."
}
```

### N373 — NFI-025-LOCAL

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/5`.

```json
{
  "id": "NFI-025-LOCAL",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "exists_today empirical guidance; application PROJECTION",
  "issue": "NASA axial cylinder knockdown is not a qualified curved-ceramic/CMC member curve.",
  "factor": {
    "baseline_gamma": 0.529082162,
    "original_gamma": 1,
    "baseline_length_to_midradius": 16.551964147878397,
    "published_length_caution_threshold": 5,
    "r_over_t_formula_limit": 1500
  },
  "required_next_evidence": "Measured local wall imperfections, ovality, thickness map and aligned compression tests plus shell/column interaction analysis.",
  "note": "Global k0.2 is independent of local gamma. Long-strut range cautions apply; scalar CMC modulus omits orthotropic shell stiffness. The 4 mm reoptimized section is thick (mean r/t about6.21), so thin-shell local theory is not established there."
}
```

### N493 — NFI-031-P3-LOCAL

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/11`.

```json
{
  "id": "NFI-031-P3-LOCAL",
  "tag": "QUESTIONABLE",
  "issue": "FIX-A triangular load sharing is used. FIX-B SP-8007 axial-cylinder knockdown is transferred to curved ceramic members; Perry and k=0.2 global continuum equations remain inherited idealisations.",
  "next_evidence": "Validate curved member local buckling, imperfections, ceramic tension/compression interaction and discrete-frame modes with actual node stiffness."
}
```

### N505 — NFI-026-07

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/6`.

```json
{
  "id": "NFI-026-07",
  "tag": "QUESTIONABLE",
  "status": "open",
  "owner": "sciences",
  "issue": "Frame elastic instability is beyond the inherited local-wall screen",
  "evidence": "Unit-load max axial stress 0.863586 GPa; inherited 0.6Et/r screen 1.750800 GPa reaches nominal unity at lambda 2.027360. At computed nonlinear limits, maximum axial stresses span 4.888–5.192 GPa, above the 3.9 GPa typical compression value.",
  "implication": "Do not use the larger frame-only eigenvalue or nonlinear limit as the structural allowable. Ceramic cracking, local wall buckling and ovalization are absent."
}
```

### C006 — NFI-022D-CHECK-06

Source `rpt-ref-4b8e7b08241bb7a45536`; original file `unpublished-local-ref:2fa44902593248ea; pointer `/rows/5`.

```json
{
  "id": "NFI-022D-CHECK-06",
  "owner": "MAINLINE-022d / MAINLINE-025",
  "state": "open model convention",
  "kind": "local shell and coupled failure",
  "evidence": "NASA SP-8007 equations 7-10; SOURCE-ARITHMETIC.best_details.local_source_conventions",
  "note": "The declared 0.6 coefficient and outer-radius gamma convention reproduce. NASA uses a Poisson-dependent coefficient and shell radius. At the fixed headline geometry, an illustrative nu=0.14/mid-radius evaluation gives local SF 1.229307846 rather than 1.258252477. L/midradius is 23.2469. Long curved ceramic shell/column interaction and bending/contact coupling are unqualified.",
  "settle": "Declare the material Poisson ratio, shell radius convention and valid coupled instability model; reoptimize only under an assigned model-change card. The diagnostic is not a replacement optimum.",
  "stops_other_work": false
}
```

### C030 — N039-09

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/8`.

```json
{
  "id": "N039-09",
  "issue": "Thin-wall tubes at the edge of the grid",
  "detail": "The frame-bay designs pick r/t 300 tubes (0.26-0.29 mm walls). Tube local buckling (026's coefficient 0.6 x SP-8007 gamma, FIX-B) fails there (0.65 SiC, 0.78 Be). Manufacturability is unknown.",
  "to_close": "Tube supply and local-buckling tests at r/t 150-300.",
  "tag": "PROJECTION"
}
```

## R054 — lattice knockdown k (0.2 floor; Wright 1965's 0.4 and its meaning)

**030b source history:** 026 prescribed imperfections give nonlinear elastic knockdowns .702–.790 against discrete perfect linear; these do not calibrate a general design k=.2 or .4.

**Original question:** Wright 1965 modified k 0.4 is applied to this card derived classical pressure, which may not match his Table 2 expression; thickness equation illegible; other sources gave no number.

### N022 — NFI-CHK011B-WRIGHT-K

Source `rpt-check011b-opus-1020`; original file `unpublished-local-ref:252e7a0b939c4177; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK011B-WRIGHT-K",
  "state": "asserted, unverified",
  "direction": "possibly optimistic at k 0.4",
  "note": "Wright's 'modified k of 0.4' may be the coefficient in p = k*E*(t/R)^2, where classical is 2/sqrt(3(1-nu^2)) = 1.2247 at nu 1/3. That would be about 0.327 of classical, not 0.4, and the k 0.4 global pressures would fall by about 18%. The citation is confirmed in Buchert 1965's bibliography. The Table 2 expression is needed."
}
```

### N307 — NFI-011B-WRIGHT

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-WRIGHT",
  "note": "Wright 1965, ASCE Journal of the Structural Division 91(ST1):173-201, is the cited paper. The extract shows a modified k of 0.4 used for his Table 2. The thickness equation in the extract is not legible. k=0.4 here multiplies the classical pressure derived in this card, which may not be the expression in that table. Buchert, Gioncu 1995 and Makowski contributed no number. A secondary E' and t' pair that cancels back to the two-way pressure was not scored."
}
```

### N308 — NFI-011B-KNOCKDOWN

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-KNOCKDOWN",
  "note": "Perfect is k=1. Design level is k=0.2, the floor of the brief's 0.2 to 0.5 lattice-dome band. k=0.5 is the top of that band. This is not the SP-8032 curve and it does not rescale 004's P2-E knockdown. P2-E stays the pinned pair 0.233885578993 and 0.164568553708."
}
```

### N360 — NFI-022-KNOCKDOWN

Source `rpt-mainline022-grok-p3-optimistic-floating-point-1020`; original file `unpublished-local-ref:62f20cec268319e4; pointer `retained original identity`.

```json
{
  "id": "NFI-022-KNOCKDOWN",
  "scored_design": 0.2,
  "wright": 0.4,
  "factor": 2.0,
  "recommendation": "Use k 0.2 for ceramic arcs. A brittle member does not shed load after first crack. Wright 1965 used a modified k of 0.4 for a reticulated-shell table. That factor is an optimism here.",
  "state": "Both values are in the catalog. k 0.2 is the brief's band floor."
}
```

### N503 — NFI-026-05

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/4`.

```json
{
  "id": "NFI-026-05",
  "tag": "PROJECTION",
  "status": "open",
  "owner": "sciences",
  "issue": "Specified nonlinear imperfections do not establish a design knockdown",
  "evidence": "Separate deterministic node, member and first-mode patterns at prescribed amplitudes; refined results in RESULTS.json.",
  "implication": "Measured k values apply only to this elastic model and these patterns; combined defects, joint compliance and a worst-case imperfection spectrum remain untested."
}
```

### C157 — NFI-041-05

Source `rpt-ref-c7dfc45babe1b96007db`; original file `unpublished-local-ref:cd543374666d8c21; pointer `/items/4`.

```json
{
  "id": "NFI-041-05",
  "status": "open",
  "topic": "Imperfections, nonlinear capacity and the global 0.2 factor",
  "evidence": [
    "RESULTS.json:selected_mesh_study",
    "NONLINEAR-AUDIT-M24.json",
    "METHODS.md"
  ],
  "finding": "The selected perfect f=4 frame has a verified first sampled elastic tangent loss near 5.430902; m12 to m24 changes it by about 0.35%. Smallest-algebraic values are checked along the sampled path and independently audited. The inherited 0.2 factor is not calibrated to this frame. Applying it to the nonlinear value would be an alternative arithmetic sensitivity near 1.086180. The primary resize retains 022d's 0.2-times-linear convention.",
  "needed": "Manufacturing and joint-imperfection distributions, path refinement as needed, measured stiffness, and validated nonlinear analyses for final resized candidates before adopting a capacity factor.",
  "prohibited_inference": "Perfect elastic first loss is not material/joint collapse, a global certification of every inter-step state, or a validated knockdown. The frozen 026b nonlinear paths remain unverified."
}
```

### C208 — NFI-043-10

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/9`.

```json
{
  "id": "NFI-043-10",
  "status": "open",
  "topic": "Coupled instability and fracture",
  "finding": "The source's 1.258252 stability multiplier is not a failure-probability distribution. No new nonlinear FE equilibrium or first-loss solve was performed here.",
  "needed": "Validated local/global instability, joint interaction, imperfection and fracture models with their uncertainties for the same actual design.",
  "effect": "Strength improvements and conditional tube Pf do not qualify stability. Linear target scaling of frozen 026b stresses is only a sensitivity.",
  "stops_other_work": false
}
```

## R055 — P3 continuum validity: smeared global mode vs member length (band s <= 3 m; buckle half-wave)

**Current 030c:** 041 directly models the selected 022d section: f4 gives .2-times-linear SF1.133451 but exceeds closure mass by174.444kg. Its resized f5 witnesses give1.143285/1.083205 at5%/019 reserves; local peak-compression sensitivities1.033223/.978132. These replace the transferred1.067 shortcut for these designs. Frozen026b rise8/nonlinear paths remain unverified.

**030b source history:** 022d screened SF1.258252 at s3.170759m passes only the requested one-member half-wave screen. 026b frequency4 gives discrete/continuum .848428913 (15.157% lower); frequency2 .317565955. Ordered .848 applied only to the current global mode gives SF1.066998; exact ratio gives1.067538. Both are QUESTIONABLE geometry transfers, not a solved 022d frame. CHECK-026 independently reproduces the earlier frequency6 linear model; it did not rerun nonlinear paths.

**Original question:** Optima stay within s<=3 m where 011 judged the equal-triangle continuum defensible; the unconstrained run to s=6.4 m was not repeated.

### N149 — NFI-011-BAND

Source `rpt-ref-f21d4bd21d2026511818`; original file `unpublished-local-ref:b5c9a6937c19e542; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-011-BAND",
  "gap": "The unconstrained optimum rides the node-mass saving to s=6.4 m (V=37 nodes), where the equal-triangle continuum behind V(s) is no longer a defensible reading; the reported optimum is cut at s<=3.0 m (V>=161), suppressing 0.0002 of SF.",
  "direction": "Re-run on real geodesic layouts (unequal members, real tributary areas) if a design point is ever picked.",
  "effect": "At most +0.1 percent on aluminum; no ranking change."
}
```

### N315 — NFI-011B-BAND

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-BAND",
  "note": "The reported optima stay inside s<=3 m, where 011 judged the equal-triangle continuum defensible. The unconstrained ride to s=6.4 m was not repeated."
}
```

### N363 — NFI-030-CONTINUUM

Source `rpt-mainline030-opus-register-1020`; original file `unpublished-local-ref:ef1ee16a8d48401a; pointer `/rows/0`.

```json
{
  "id": "NFI-030-CONTINUUM",
  "state": "demonstrated (CONTINUUM.json)",
  "owner": "MAINLINE-022c / MAINLINE-026",
  "note": "The smeared lattice buckle half-wave pi*sqrt(1.06*rg*R) is 0.57 of the member at 022b's s 6.15 m (40 nodes) and 0.64 at s 5.5 m, against 1.48 at 011b's s 2.04 m and 4.56 at the Mylar s 0.55 m frame. Where the half-wave is shorter than a member, the global formula does not describe the frame; 022b's 1.375 and 1.487 need a discrete geometrically nonlinear check before they count.",
  "settle": "one ccx/gmsh buckling run of the triangulated frame at s 2.2 m and 6.15 m"
}
```

### N365 — NFI-030-P3-INBAND

Source `rpt-mainline030-opus-register-1020`; original file `unpublished-local-ref:ef1ee16a8d48401a; pointer `/rows/2`.

```json
{
  "id": "NFI-030-P3-INBAND",
  "state": "computed (rpt-check011b-opus-1020)",
  "owner": "MAINLINE-022c",
  "note": "Inside s <= 3 m, SiC arcs with FIX-A and FIX-B at 100 kg and 5% are 1.130, film-limited at s 2.224 m (r_o 121.7 mm, wall 0.915 mm), on the carried 1.5 GPa film. 022c could report an in-band row beside the open band."
}
```

### N419 — NFI-CHK024-LATTICE-MODEL

Source `rpt-ref-7d6892c4e55be16ad523`; original file `unpublished-local-ref:0d655e2d18e3e532; pointer `/open/8`.

```json
{
  "id": "NFI-CHK024-LATTICE-MODEL",
  "kind": "inherited structural assumptions",
  "tag": "PROJECTION",
  "finding": "Retains 011b continuum coefficient, k=0.2, 3900 MPa SiC crush, local gamma=1, s as arc length, five-percent joints and steel-column Perry formula on ceramic arcs. They are not newly validated by this film check.",
  "proposed_next": "Carry the 011b NFI with the re-sized lattice."
}
```

### N463 — NFI-C022-DISCRETE-JOINTS

Source `rpt-ref-f6de390e1555b4ca8e78`; original file `unpublished-local-ref:a3c00555c78ad754; pointer `/rows/6`.

```json
{
  "id": "NFI-C022-DISCRETE-JOINTS",
  "kind": "OPEN structural qualification",
  "issue": "Uniform lattice equilibrium is correct, but smeared global stiffness and approximately40 continuum vertices at long spacing do not establish a real spherical frame.",
  "evidence": {
    "equilateral022c_projection5": {
      "nodes": 40.36445214851938,
      "members": 115.09335644555816,
      "n_coef": 17.753520777580995,
      "m_nodes": 0.8072890429703877,
      "m_film": 348.8563570154232,
      "m_joint": 207.21678204764845,
      "m_tube": 3794.671994894575,
      "m_end": 0.9002117430890411,
      "reserve": 437.88972718938203,
      "sag_kg": 193.417619679882,
      "vehicle": 4451.552423000618,
      "s_m": 6.15,
      "r_o_m": 0.16764011960487946,
      "t_film_m": 0.00028619697756719387,
      "t_w_m": 0.001623088408707305,
      "rt": 103.28465085792524,
      "A_m2": 0.0017013453789958654,
      "I_m4": 2.3676289932865346e-05,
      "length_m": 6.25129231047749,
      "N_N": 1694765.9693497152,
      "sigma_axial_Pa": 996132819.5160271,
      "k": 0.2,
      "gamma": 0.5763851730392059,
      "SF_local_gamma1": 2.3910137429040064,
      "SF_least": 1.3733213857843127,
      "eta": 0.07530548419597233,
      "Euler_stress_Pa": 1441003885.5529516,
      "mass_closure_kg": 4889.442150189999,
      "radius_cap_fraction": 0.6705604784195178,
      "NASA_L_over_midradius": 37.471352227693885,
      "SF_yield": 3.9151405551468748,
      "SF_euler": 1.4465981416545093,
      "SF_local": 1.3781448699428451,
      "SF_film": 1.4624665443017892,
      "SF_perry": 1.3868432138641869,
      "SF_global": 1.3733213857843127,
      "governing": "global",
      "k04_governing": "local",
      "k04_SF_least": 1.3781448699428451,
      "k04_SF_global": 2.7466427715686255,
      "on_ro_cap_0_25": false,
      "full_pressure": {
        "pressure_multiplier": 1.0,
        "mean_compression_Pa": 996132819.5160271,
        "bending_Pa": 242982415.75261784,
        "maximum_compression_Pa": 1239115235.2686448,
        "opposite_signed_compression_Pa": 753150403.7634093,
        "maximum_tension_Pa": 0.0
      },
      "reported_limit": {
        "pressure_multiplier": 1.3733213857843127,
        "mean_compression_Pa": 1368010504.1229851,
        "bending_Pa": 2033750657.4313748,
        "maximum_compression_Pa": 3401761161.55436,
        "opposite_signed_compression_Pa": -665740153.3083897,
        "maximum_tension_Pa": 665740153.3083897
      }
    }
  },
  "next": "Resolve discrete geometry, node stiffness, membrane load introduction, member curvature and coupled global/local modes.",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION"
}
```

### N480 — NFI-030-COEFF-106

Source `rpt-ref-490f8e9228d526b69dc8`; original file `unpublished-local-ref:67de0b610c731495; pointer `/rows/0`.

```json
{
  "id": "NFI-030-COEFF-106",
  "issue": "REGISTER.md writes the smeared half-wave as pi*sqrt(1.06*rg*R). The stored waves match pi*sqrt((3/4)*rg_section*R), which is pi*sqrt(1.06066*rg_thin*R). Using the printed 1.06 with the stored thin-ring rg shortens the 022b wave by 1.094 mm, from 3.514184 m to 3.513090 m.",
  "consequence": "The ratio stays 0.571 at s 6.15 m and 1.481 at s 2.04 m. The half-wave is still shorter than the 6.15 m member, so 022b's continuum optimum stays outside the band. This does not stop the card.",
  "next": "Write 1.06066, or 3/4 on the section radius of gyration, in the sentence that cites CONTINUUM.json."
}
```

### N502 — NFI-026-04

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/3`.

```json
{
  "id": "NFI-026-04",
  "tag": "QUESTIONABLE",
  "status": "open",
  "owner": "sciences",
  "issue": "Discrete perfect eigenvalue differs from smeared continuum",
  "evidence": "Primary finest lambda 6.46522244 versus inherited 6.12763973; 5.509% difference.",
  "implication": "Geometry, nonuniform spacing, torsion, pressure transfer and omitted initial-moment couplings differ. Agreement in scale is not validation of a global knockdown."
}
```

### N509 — NFI-026-11

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/10`.

```json
{
  "id": "NFI-026-11",
  "tag": "QUESTIONABLE",
  "status": "open",
  "owner": "sciences",
  "issue": "Symmetric eigenmode multiplicities and nonlinear collapse scope",
  "evidence": "Stored low Lanczos modes are representative; first constrained tangent instability is followed, with post-peak points where available.",
  "implication": "No full multiplicity census, post-collapse dynamics or damaged-state residual capacity is claimed."
}
```

### N562 — NFI-037-022D-UNFILED

Source `rpt-ref-8c5de04c9c33dbcf7447`; original file `unpublished-local-ref:cbdfc7fec44de4cc; pointer `/rows/0`.

```json
{
  "id": "NFI-037-022D-UNFILED",
  "tag": "QUESTIONABLE",
  "finding": "022d had not filed. The P3 rows are 022c. Projection at 6.15 m and CFRP/Zylon at 5.5 m fail the half-wave test, ratios 0.571 and 0.636. Their global factors are not in-band leads.",
  "next": "Use 022d's in-band points when that card is filed. Do not treat s 6.15 m as a continuum optimum."
}
```

### N570 — NFI-CHECK-031-HALF-WAVE

Source `rpt-ref-be337d7d2ce1259d0aff`; original file `unpublished-local-ref:d18fb2f2dcd28de0; pointer `/rows/0`.

```json
{
  "id": "NFI-CHECK-031-HALF-WAVE",
  "status": "open",
  "issue": "030's half-wave is pi*sqrt((3/4)*rg*R), rg=sqrt((ro^2+ri^2)/2), divided by bay side. Below 1, or a bay longer than 3 m, is outside the smeared band. The 019-reserve 022b point is s 6.15 m at ratio 0.567895. Every reoptimised SiC row is outside that band. The optimistic 100 m row is ratio 0.568724. The least factor on those rows is global.",
  "effect": "The passing P3 factors use a global formula the register says does not describe these bays. The Ti/Kapton rows are inside the band and remain below 1. This objection does not change the printed arithmetic."
}
```

### N592 — NFI-022D-CONTINUUM

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/3`.

```json
{
  "id": "NFI-022D-CONTINUUM",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "NFI-030-CONTINUUM",
    "NFI-030-P3-INBAND",
    "NFI-C022-DISCRETE-JOINTS"
  ],
  "finding": "Sixteen overall optima fail half-wave>=arc length. Their screened alternatives are filed, but a wavelength of exactly one member does not establish homogenization, an integer mesh or discrete stability.",
  "next": "Analyze an explicit imperfect curved frame and actual node rotational stiffness."
}
```

### N615 — NFI-026B-01

Source `rpt-ref-8befdd4c89803adc44a8`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/0`.

```json
{
  "id": "NFI-026B-01",
  "tag": "QUESTIONABLE",
  "status": "computed_departure",
  "owner": "sciences",
  "issue": "Coarse-bay continuum departure",
  "evidence": "Frequency4 linear 5.254643802 versus 6.193381346; frequency 2 2.183661359 versus 6.876245150. Last mesh changes below 0.0161%.",
  "implication": "Use discrete frame results for these cases; no continuum applicability threshold is validated."
}
```

### N641 — NFI-026B-01

Source `rpt-ref-4a20323946ecafd56a6b`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/0`.

```json
{
  "id": "NFI-026B-01",
  "tag": "QUESTIONABLE",
  "status": "computed_departure",
  "owner": "sciences",
  "issue": "Coarse-bay continuum departure",
  "evidence": "Frequency4 linear 5.254643802 versus 6.193381346; frequency 2 2.183661359 versus 6.876245150. Last mesh changes below 0.0161%.",
  "implication": "Use discrete frame results for these cases; no continuum applicability threshold is validated."
}
```

### N665 — NFI-038-TOPOLOGY

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/14`.

```json
{
  "id": "NFI-038-TOPOLOGY",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Fractional optimized node counts are not buildable frames",
  "evidence": "022d one-member half-wave screen does not validate continuum; two-way shear stiffness unresolved.",
  "resolution_needed": "Select integer topology and re-evaluate before manufacturing; test pressure-skin load sharing.",
  "tests": [
    "T8"
  ]
}
```

### N671 — NFI-CHECK-026-01

Source `rpt-check026-grok-p3-lattice-1020`; original file `unpublished-local-ref:1c3bb69a594eb057; pointer `/rows/0`.

```json
{
  "id": "NFI-CHECK-026-01",
  "tag": "QUESTIONABLE",
  "status": "no_fix_card",
  "issue": "3-segment reproduction agrees; finest-column gaps are the published segment count",
  "evidence": "Follower lambda 6.472325 beside the card 3-segment 6.472320. Gaps to the 24-segment column are 0.09 to 0.18 percent on compression, volume, axial stress and the fixed-direction factor.",
  "implication": "No fix card. The card's own mesh table already separates 3 segments from 24."
}
```

### B006 — NFI-030B-DISCRETE-TRANSFER

Source `rpt-ref-39745602983887568501`; original file `unpublished-local-ref:534f72d6d7dd0ad8; pointer `retained original identity`.

```json
{
  "id": "NFI-030B-DISCRETE-TRANSFER",
  "title": "The ordered 026b-to-022d fold is a sensitivity, not an exact-frame solution.",
  "finding": "Apply the ordered .848 only to the global mode of the held 022d screened lead, with all other modes and masses held. The frequency-4 section/topology differs, so the resulting 1.067 multiplier is QUESTIONABLE. The exact source ratio is also shown; no reoptimization, material qualification or verified nonlinear first loss follows.",
  "status": "OPEN",
  "blocks_progress": false
}
```

### C002 — NFI-022D-CHECK-02

Source `rpt-ref-4b8e7b08241bb7a45536`; original file `unpublished-local-ref:2fa44902593248ea; pointer `/rows/1`.

```json
{
  "id": "NFI-022D-CHECK-02",
  "owner": "MAINLINE-022d / MAINLINE-026",
  "state": "open applicability check",
  "kind": "discrete versus continuum evidence",
  "evidence": "Frozen mainline026b RESULTS/CARD; ARITHMETIC-CHECK.continuum_NFI",
  "note": "Frequency-4 ideal rigid-frame linear multiplier 5.254643802209333 is 15.1571087172215% below source continuum 6.1933813461115825 even though its nominal half-wave/spacing is 1.05829486. A one-member wavelength screen does not validate continuum capacity. The 022d section, spacing and joints differ, so this is not a universal 15.16% correction.",
  "settle": "Under a new routed card, solve a matched discrete frame for the 022d candidate with explicit joint stiffness, imperfections and relevant instability modes. Do not reuse the unverified new 026b nonlinear crossing as first loss.",
  "stops_other_work": false
}
```

### C082 — NFI-C026B-NONLINEAR

Source `rpt-ref-b92330879d6ba35bd62c`; original file `unpublished-local-ref:21616ac9b36e6057; pointer `/rows/1`.

```json
{
  "id": "NFI-C026B-NONLINEAR",
  "issue": "First nonlinear loss remains unverified for f4 and f2.",
  "evidence": "Nearest-zero spectral selection can switch families; raw f4 path shows the stated jump. This check performed no nonlinear solve.",
  "next_evidence": "Independent smallest-algebraic or inertia tracking across the precritical path, retaining eigenfamilies and earliest loss.",
  "tag": "QUESTIONABLE",
  "status": "open",
  "blocks_card": false
}
```

### C083 — NFI-C026B-RAW-LABELS

Source `rpt-ref-b92330879d6ba35bd62c`; original file `unpublished-local-ref:21616ac9b36e6057; pointer `/rows/2`.

```json
{
  "id": "NFI-C026B-RAW-LABELS",
  "issue": "Raw nonlinear result metadata still describes first loss and an m6 independent check without qualifying the new frequencies.",
  "evidence": "Raw interpretation and stability_solver fields conflict with the correctly qualified top-level CARD/RESULTS.",
  "next_evidence": "Keep raw receipts frozen; add an explicit downstream override or schema field verified_first_loss=false with frequency-specific verification scope.",
  "tag": "QUESTIONABLE",
  "status": "open",
  "blocks_card": false
}
```

### C088 — NFI-C026B-MODEL

Source `rpt-ref-b92330879d6ba35bd62c`; original file `unpublished-local-ref:21616ac9b36e6057; pointer `/rows/7`.

```json
{
  "id": "NFI-C026B-MODEL",
  "issue": "Agreement verifies the stated elastic beam/fan model only.",
  "evidence": "Initial-moment geometric terms, shear, local tube failure, self-weight, material failure and real film stiffness remain excluded.",
  "next_evidence": "Quantified model-scope corrections and mesh/eigenspace checks appropriate to any proposed physical reserve.",
  "tag": "QUESTIONABLE",
  "status": "open",
  "blocks_card": false
}
```

### C161 — /resolved_for_this_card_only/0

Source `rpt-ref-c7dfc45babe1b96007db`; original file `unpublished-local-ref:cd543374666d8c21; pointer `/resolved_for_this_card_only/0`.

```json
{
  "topic": "Cross-geometry global eigenvalue transfer",
  "finding": "The selected section is modeled directly; the transferred 026b ratio is not used. Its own perfect linear multiplier and explicit 0.2 screen replace that numerical shortcut, while material and model qualification remain open."
}
```

### C200 — NFI-043-02

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/1`.

```json
{
  "id": "NFI-043-02",
  "status": "open",
  "topic": "Integer frame and resolved member loads",
  "finding": "CHECK-022d uses continuum count 432.9863. Rounding to 433 does not define a closed triangular mesh; 435 is only a compatible counting example. The three independently recovered 026b meshes use different geometries.",
  "needed": "A physically specified selected integer mesh, all section properties, boundary conditions, member forces and nonlinear load paths.",
  "effect": "433-member probabilities are risk bookkeeping. The selected-point joint-moment estimate is a dimensional sensitivity, not an equilibrium solution.",
  "stops_other_work": false
}
```

## R056 — P3 global lattice mode added and its coefficient (sqrt(3/2), Buchert 1968)

**Original question:** Scored global pressure uses the equilateral continuum grid (nu 1/3); the brief two-way coefficient 4 is robotics arithmetic and a geodesic coefficient was not invented.

### N148 — NFI-011-GLOBAL

Source `rpt-ref-f21d4bd21d2026511818`; original file `unpublished-local-ref:b5c9a6937c19e542; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-011-GLOBAL",
  "gap": "No global frame mode: the model checks member Euler, member yield, tube local buckling and film only. Snap-through or general-instability of the whole stiffened sphere between nodes is unmodelled, and MAINLINE-004's spherical knockdown therefore neither applies to nor rescales any P3 number.",
  "direction": "Add an equivalent-stiffened-shell general-instability check (ribbed-sphere analogy) before any P3 number is read as a whole-vehicle figure.",
  "effect": "Could only lower the P3 rows; the aluminum plateau's flatness and the material ranking survive any such factor applied uniformly."
}
```

### N306 — NFI-011B-GRID

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-GRID",
  "note": "011 counts nodes with the equilateral continuum. The scored global pressure uses that grid: Et=(2/sqrt(3))*E*A/s, nu=1/3, D=(3*sqrt(3)/4)*E*I/s, and the classical sphere 4*sqrt(D*Et)/R^2. The product is 4*sqrt(3/2)*E*sqrt(I*A)/(s*R^2). The brief's two-way pressure, coefficient 4, is the robotics arithmetic and is re-optimised beside it. A geodesic coefficient was not invented."
}
```

### N348 — NFI-017-P3-MODES

Source `rpt-mainline017-improvement-directions-lead4f19-1019`; original file `unpublished-local-ref:b586b896a14aa878; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-017-P3-MODES",
  "gap": "The best P3 point (SiC, least SF 2.848476) is scored on 011's four modes only. Global lattice buckling and member bending are absent; 011b had not filed when this card started, and 009 carries P3 as PENDING-011b with an equivalent-continuum lattice estimate of about 0.70 perfect at the 6061 optimum, 0.14-0.35 knocked down, not recomputed here.",
  "direction": "011b. Do not admit the SiC point as passing until those two modes are scored.",
  "effect": "SiC's factor-1 ranking is conditional on the scored modes."
}
```

## R057 — two-way grid global coefficient 4 assumes isotropy; an unbraced two-way grid has no in-plane shear stiffness (022b's two-way rows rest on it)

**030b source history:** 022d retains two-way surrogate diagnostics up to SF1.867825 screened, but no qualified shear stiffness supports C=4. Square-cell sensitivity 1.728883 does not repair that missing mechanism.

**Original question:** Whether a two-way grid without diagonals has any smeared global buckling capacity near 4*E*sqrt(I*A)/(s*R^2); the lattice sum gives C1212 = 0. 022b's two-way rows (Ti + Kapton 0.986, SiC 1.98) are governed by it.

### N023 — NFI-CHK011B-TEXT

Source `rpt-check011b-opus-1020`; original file `unpublished-local-ref:252e7a0b939c4177; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK011B-TEXT",
  "state": "demonstrated",
  "direction": "documentation",
  "note": "M1: the report body says 'k 0.4 and 0.5 are in the card', but the CARD.md table carries k 1, 0.4 and 0.2 (k 0.5 is in RESULTS.json only). M2: INPUTS.json materials carry no source and 011's INPUTS.json, which holds them, is not pinned. M3: Buchert 1968 prints the card's Et and D, so it can be cited. M4: the 'two_way' rows are the triangulated frame scored with C = 4, not a two-way frame, which would have zero in-plane shear stiffness (C1212 = 0)."
}
```

### N364 — NFI-030-TWO-WAY

Source `rpt-mainline030-opus-register-1020`; original file `unpublished-local-ref:ef1ee16a8d48401a; pointer `/rows/1`.

```json
{
  "id": "NFI-030-TWO-WAY",
  "state": "demonstrated (lattice sum C1212 = 0, rpt-check011b-opus-1020 M4)",
  "owner": "MAINLINE-022c",
  "note": "022b re-counted the two-way grid at 2V-4 members but kept the isotropic C = 4. An unbraced two-way grid has no in-plane shear stiffness, so its two-way rows (Ti + Kapton 0.986, SiC 1.98) are not floating points until a discrete solve or diagonals settle it."
}
```

### N593 — NFI-022D-TWO-WAY

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/4`.

```json
{
  "id": "NFI-022D-TWO-WAY",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "NFI-030-TWO-WAY"
  ],
  "finding": "The unbraced two-way lattice has no demonstrated in-plane shear stiffness supporting inherited C=4. Primary half-wave and triangular-sag transfers are diagnostic only. Square-cell sensitivity does not repair shear.",
  "next": "Supply bracing and its mass or solve the actual frame and identify its shear/global modes."
}
```

### C007 — NFI-022D-CHECK-07

Source `rpt-ref-4b8e7b08241bb7a45536`; original file `unpublished-local-ref:2fa44902593248ea; pointer `/rows/6`.

```json
{
  "id": "NFI-022D-CHECK-07",
  "owner": "MAINLINE-022d / MAINLINE-030",
  "state": "open applicability",
  "kind": "two-way mechanism",
  "evidence": "Owner METHOD/NFI; upstream/030/NFI.json",
  "note": "The two-way numerical optima use an isotropic global surrogate despite missing in-plane shear stiffness in an unbraced pin grid. Square-cell sag/wavelength sensitivity changes a comparison, but cannot establish missing bracing or joint stiffness.",
  "settle": "Specify and count a shear-stable lattice or validate explicitly modeled moment-resisting joints; establish a matching continuum only afterward.",
  "stops_other_work": false
}
```

## R058 — P3 member imperfection: geometric Perry eta, brittle tube

**Original question:** The P3 pass relies on SiC compression 3900 MPa and a metal-style Perry interaction; a 380 MPa screen gives only about 0.24-0.25. Compressive strength is not a bending allowable.

### N112 — NFI-027-FRAME-BRITTLE

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-FRAME-BRITTLE",
  "tag": "QUESTIONABLE",
  "issue": "011b's SiC compression 3900 MPa and metal-style Perry interaction produce the P3 pass. A380 MPa strength screen gives only about 0.24–0.25 over 10–50 m. Compressive strength is not a ceramic bending/tensile allowable.",
  "next_evidence": "Use a brittle tension/compression interaction, statistical size effect and joint eccentricity rather than certifying on the inherited Perry score."
}
```

### N310 — NFI-011B-PERRY

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-PERRY",
  "note": "Geometric Perry-Robertson with a0=s/1000 and eta=a0*r_o/rg^2. This is not a code eta table. SF is sigma_cr divided by the arch stress at p_ext. When N exceeds Ne the pole of 1/(1-N/Ne) is passed and that factor is not the score. The formula is a steel-column interaction. On CFRP, CNT and SiC it is a projection. It is scored beside Euler and yield and can bind below both."
}
```

## R059 — SiC tube density 3100 vs 3150

**Current 030c:** All eight 022c tube families are SiC; Ti/CFRP labels fittings. CHECK-037's ten corrections include two repeated projection rows with alternate film CTE. See the exact correction table.

**Original question:** Tube density kept at 3100 kg/m3 though sheet density is 3150; brazed-socket mass about 1.6 percent light.

### N221 — NFI-023-DENSITY-3100

Source `rpt-ref-a4768f77870336c8cdbb`; original file `unpublished-local-ref:8fc6d5cd4b5f84d2; pointer `retained original identity`.

```json
{
  "id": "NFI-023-DENSITY-3100",
  "value": "Tube density 3100 kg/m3, kept so the 5 percent regression matches 011b. Hexoloy SA sheet density is 3.15 g/cm3.",
  "state": "exists today",
  "issue": "Substituting 3150 would raise the brazed-socket mass about 1.6 percent and would move the recovered safety factor. It was not substituted.",
  "consequence": "The socket mass is slightly light relative to the sheet density. The sleeve and wrap masses do not use the ceramic density.",
  "next": "None, unless the frame density is changed in a later card."
}
```

### C041 — NFI-CHECK037-P3-TUBE-IDENTITY

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/3`.

```json
{
  "id": "NFI-CHECK037-P3-TUBE-IDENTITY",
  "tag": "QUESTIONABLE",
  "status": "open",
  "finding": "Ti/CFRP fittings were treated as tube materials in thermal CTE and mass while SiC capacities were retained.",
  "proposed_fix": "Use SiC properties for all tubes, keep fittings separate, and rerun temperatures plus compatibility. Corrected fixed-temperature sensitivities are already tabulated."
}
```

## R060 — SiC tube design allowable: 3.9 GPa crush vs 380 MPa flexural vs Weibull; demand 0.82 GPa with FIX-A (025)

**Current 030c:** 043 supplies conditional weakest-link requirements, not frame probability: no matched compression m/scale/reference size for finished arcs. Its433-member022d bookkeeping is not041's750-member resized frame. Qualified Pf and lifetime remain null.

**030b source history:** 025/CHECK-025 leave full-size SiC/CMC compression allowable null. 022d screened lead assumes Fc3900 MPa; its calculated maximum compression is .947377 GPa at design pressure and 1.198096 GPa at its claimed multiplier. Neither 380 MPa flexure nor 3.9 GPa typical crush qualifies the arc.

**Original question:** SiC and T700 P3 values are 011 equal-mass swap properties from 008; SiC 3900 MPa is compressive, flexural about 380 MPa governs bending; 011 uses compressive sigma for member yield.

### N021 — NFI-CHK011B-SIC-FIBRE

Source `rpt-check011b-opus-1020`; original file `unpublished-local-ref:252e7a0b939c4177; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK011B-SIC-FIBRE",
  "state": "demonstrated",
  "direction": "informational (022)",
  "note": "At the SiC point the L/1000 imperfection adds +/-58.8 MPa (eta 0.0332, amplifier 1.240) to 1.428 GPa of compression. The fibres are at -1.487 and -1.370 GPa, so there is no tension, and with FIX-A they are -0.855 and -0.794 GPa. The 380 MPa flexural scan (0.262) is therefore not the arcs' allowable. The open number is the compressive design allowable of a 0.88 mm brittle wall at about 1.4 GPa of service stress (022's Weibull item)."
}
```

### N151 — NFI-011-SIC

Source `rpt-ref-f21d4bd21d2026511818`; original file `unpublished-local-ref:b5c9a6937c19e542; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-011-SIC",
  "gap": "SiC's 3900 MPa is a crushing value; 008's own NFI carries that flexural ~380 MPa governs any bending or tension path, with brittle fracture, joining and handling unresolved. A 0.04 m radius sintered SiC tube of 1.3 mm wall is undemonstrated.",
  "direction": "Treat the SiC row as a material-boundary statement (sigma/rho headroom), not a buildable tube.",
  "effect": "The P3 sigma/rho-bound conclusion stands; the SiC design point does not."
}
```

### N220 — NFI-023-FLEXURE-380

Source `rpt-ref-a4768f77870336c8cdbb`; original file `unpublished-local-ref:8fc6d5cd4b5f84d2; pointer `retained original identity`.

```json
{
  "id": "NFI-023-FLEXURE-380",
  "value": "Hexoloy SA flexural strength 380 MPa. Compressive strength 3900 MPa is the allowable 011b scored. Axial stress at the filed wall is 824.7 MPa at 562.2 kN.",
  "state": "exists today",
  "issue": "Against 3900 MPa the contact factor is 4.73. Against 380 MPa it is 0.461, and the member itself fails. This card does not replace the 011b allowable.",
  "consequence": "A joint sized to the flexural coupon rejects the tube that 011b accepted.",
  "next": "MAINLINE-025 owns the allowable. No change here."
}
```

### N312 — NFI-011B-SIC

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-SIC",
  "note": "The primary SiC row uses 011's 3900 MPa crush. A second scan uses 380 MPa, the flexural figure 011 carried from 008. Flexural strength, brittle fracture, joining and a sintered tube of this size remain open. Perry and yield at 3900 MPa are not a bending allowable."
}
```

### N352 — NFI-017-SIC-SIGMA

Source `rpt-mainline017-improvement-directions-lead4f19-1019`; original file `unpublished-local-ref:b586b896a14aa878; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-017-SIC-SIGMA",
  "gap": "SiC and T700 P3 values are 011's equal-mass swap properties from 008. SiC sigma 3900 MPa is compressive strength; flexural strength about 380 MPa governs bending paths (008's note), and 011 uses compressive sigma for member yield.",
  "direction": "Score member bending before the SiC direction is admitted (011b).",
  "effect": "P3 SiC strength is QUESTIONABLE as a tube direction."
}
```

### N355 — NFI-022-SIC-ALLOWABLE

Source `rpt-mainline022-grok-p3-optimistic-floating-point-1020`; original file `unpublished-local-ref:62f20cec268319e4; pointer `retained original identity`.

```json
{
  "id": "NFI-022-SIC-ALLOWABLE",
  "value_scored_today_Pa": 380000000.0,
  "sourced_today": "Saint-Gobain Hexoloy SA 4-point flexural strength 380 MPa on a 3 x 4 x 45 mm bar. Compressive strength on the same sheets is 3900 MPa.",
  "weibull_Pa": 190451148.77836347,
  "weibull_note": "Two-parameter Weibull at P_f = 0.001, m = 10, sigma_0 taken as 380 MPa, same volume as the bar. m = 10 is the seal-tube and structural-tile page. Sheet B-1003-2 lists 8 for standard SA and 12 for enhanced SA. This is not a volume-scaled tube allowable, and it is not a compression test.",
  "crush_Pa": 3900000000.0,
  "factor_crush_over_flexural": 10.263157894736842,
  "factor_flexural_over_weibull": 1.9952623149688795,
  "state": "PENDING-025. 380 and 3900 exist on the datasheet. The 190 MPa figure is a calculation. This card carries 3900 MPa as 011b did. Using it as a tube allowable is an optimism. MAINLINE-025 owns the row.",
  "scored_baseline_SF": 0.2438010340863489,
  "weibull_case_SF": 0.12408348691924517,
  "source": "https://www.ceramicsrefractories.saint-gobain.com/hexoloy-enhanced-sa-sic-technical-data-sheet and the Hexoloy seal-tube page"
}
```

### N356 — NFI-022-BENDING-CONTACT

Source `rpt-mainline022-grok-p3-optimistic-floating-point-1020`; original file `unpublished-local-ref:62f20cec268319e4; pointer `retained original identity`.

```json
{
  "id": "NFI-022-BENDING-CONTACT",
  "service_axial_Pa": 1544983685.500977,
  "flexural_Pa": 380000000.0,
  "SF_axial_over_flexural": 0.24595728975402162,
  "bearing_area_for_380_m2": 0.0007785723252585767,
  "tube_area_m2": 0.00019149553899808612,
  "note": "PENDING-025. At the sourced-today point the axial stress is the contact stress if the tube section bears the member force. Perry is the scored bending-imperfection mode. MAINLINE-025 owns the allowable."
}
```

### N362 — NFI-022-DATASHEET-SPREAD

Source `rpt-mainline022-grok-p3-optimistic-floating-point-1020`; original file `unpublished-local-ref:62f20cec268319e4; pointer `retained original identity`.

```json
{
  "id": "NFI-022-DATASHEET-SPREAD",
  "note": "This card keeps 011b's E of 410 GPa and density 3100 kg/m3 so the regression is the same material. Hexoloy pages also print E 430 GPa, density 3.10 to 3.15 g/cm3, and Poisson's ratio 0.14. The local-buckling coefficient stays 0.6."
}
```

### N368 — NFI-025-COMPRESSION

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/0`.

```json
{
  "id": "NFI-025-COMPRESSION",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "exists_today coupon/property data; target allowable PROJECTION",
  "issue": "No probability-qualified compression allowable for full-size Hexoloy SA or CVD arcs.",
  "factor": {
    "qualified_Fc_Pa": null,
    "required_extreme_compression_Pa_at_original_full_pressure": 1487180630.733,
    "required_extreme_compression_Pa_at_optimistic_reoptimized_full_pressure": 1520385084.385,
    "typical_coupon_compression_Pa": 3900000000.0,
    "qualified_available_to_required_ratio": null,
    "required_extreme_compression_Pa_at_original_full_pressure_by_force_rule": {
      "equilateral_equilibrium": 855498631.1352932,
      "legacy_pRs_over2": 1487180630.7109318
    },
    "required_equilateral_extreme_compression_Pa_at_optimistic_reoptimized_full_pressure": 856977622.5503811,
    "size_dependent_compression_allowable_function": null
  },
  "required_next_evidence": "Production-representative axial compression and combined compression/bending/contact tests; failure mode and distribution model, lower confidence bounds, environment and loading history.",
  "note": "ASTM C1424 separates compression from tensile weakest-link statistics; 380 MPa flexure is not a measured compression allowable. Zero continuum tensile hazard cannot establish compressive survival. Earlier unqualified required-stress keys denote the inherited force rule; explicitly named dual-demand fields distinguish the amendment. The requested tube-size interface is supplied in allowable.py with compression qualification null."
}
```

### N369 — NFI-025-WEIBULL

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/1`.

```json
{
  "id": "NFI-025-WEIBULL",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "exists_today typical product and coupon data; structural scaling PROJECTION",
  "issue": "Hexoloy SA fitted population, characteristic strength and test reference size are incomplete; current m8 and 2012 m10 differ.",
  "factor": {
    "m_alternatives": [
      8,
      10
    ],
    "SA_characteristic_strength_Pa_measured": null,
    "illustrative_uniform_tensile_caps_Pa": [
      7191893.634201991,
      15585636.721825296
    ],
    "assembly_to_assumed_effective_coupon_volume_ratio_order": 100000000.0,
    "size_interface": "allowable.py: tube_geometry, effective_measure, weibull_threshold; m-specific geometric measures and supplied hypothetical calibration are explicit"
  },
  "required_next_evidence": "Raw fracture samples and origins for the intended process, surface finish, flaw populations, specimen spans and gauge volumes; confidence-bounded fits.",
  "note": "The 40/20 mm bend spans and mean interpretation of typical380 MPa are explicit assumptions. Independent tensile SA data show m5; do not cherry-pick m10 as validated."
}
```

### N370 — NFI-025-CVD-REFERENCE

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/2`.

```json
{
  "id": "NFI-025-CVD-REFERENCE",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "exists_today commercial CVD; miniature tests in_the_lab; large-arc scaling PROJECTION",
  "issue": "Commercial CVD m11/beta424 MPa lack effective coupon size; miniature CVD hoop tests are distinct populations.",
  "factor": {
    "commercial_m": 11,
    "commercial_reported_beta_MPa": 424,
    "reference_area_or_volume": null,
    "large_tube_tensile_or_compression_allowable_Pa": null
  },
  "required_next_evidence": "Lot- and process-specific coupon geometry, test method and fracture origins; representative long-tube tests.",
  "note": "Do not borrow a reference area from the miniature TRISO tube paper for a commercial CVD strength distribution."
}
```

### N371 — NFI-025-RISK-LIFE

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/3`.

```json
{
  "id": "NFI-025-RISK-LIFE",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "PROJECTION",
  "issue": "Analyst-selected short-term system failure target has no demonstrated structural or lifetime qualification.",
  "factor": {
    "system_Pf_target": 1e-06,
    "alternative_target": 0.001,
    "integer_member_budget": 1047,
    "union_bound_member_budget": 9.551098376313275e-10
  },
  "required_next_evidence": "Allocate risk across failure mechanisms; define mission load cycles, environment and duration, batch correlations, proof testing and nondestructive inspection.",
  "note": "Target concerns first critical member loss in one load exposure. A uniform tensile illustration is not actual contact reliability, total failure probability or lifetime survival."
}
```

### N379 — NFI-025-CMC-PROPERTIES

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/11`.

```json
{
  "id": "NFI-025-CMC-PROPERTIES",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "in_the_lab measured panels and separate manufacturer coupons; target PROJECTION",
  "issue": "CMC compression, tensile damage onset, density and stiffness are not a coherent tube allowable set.",
  "factor": {
    "CVI_E_Pa": 272000000000.0,
    "bulk_density_kg_m3": 2440,
    "tensile_PLS_Pa": 128000000.0,
    "tensile_UTS_Pa": 357000000.0,
    "mixed_compression_screen_Pa": 580000000.0,
    "qualified_tube_compression_Pa": null,
    "inherited_load_mixed_screen_pressure_gap_factor": 1.9881682999246246,
    "triangular_force_mixed_screen_pressure_gap_factor": 1.147893022422129
  },
  "required_next_evidence": "Same layup, fiber, interphase, matrix process and direction data for tube E/rho/tensile/compression/shear; knockdown and reliability statistics.",
  "note": "128 MPa is tensile PLS, not measured compression onset. 580 MPa comes from another Hi-Nicalon CVI product; its E/density are not given. Do not use apparent Archimedes density as bulk mass density."
}
```

### N398 — NFI-023-CHECK-CONTACT-METRIC

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/8`.

```json
{
  "id": "NFI-023-CHECK-CONTACT-METRIC",
  "status": "open",
  "non_blocking": true,
  "field": "sigma_contact and flexural SF",
  "reported": "N/A called contact stress;380MPa flexure ratio used to say the tube fails.",
  "check": {
    "filed_mean_axial_Pa": 824658297.2240398,
    "flexural_ratio": 0.46079691586097404,
    "interpretation": "N/A is mean axial wall compression. Local bearing/peel/splitting is not resolved;380MPa flexure is not a compressive failure criterion."
  },
  "evidence": [
    "Hexoloy primary sheet",
    "CHECK.md"
  ],
  "next": "Retain both as explicit material sensitivities; use a suitable ceramic stress/failure model and geometry for contact acceptance."
}
```

### N454 — NFI-CHECK-025-SHEET-MODULUS

Source `rpt-ref-a8b77f7de2ffc56af7b4`; original file `unpublished-local-ref:d2a2bac9ac804106; pointer `/rows/0`.

```json
{
  "id": "NFI-CHECK-025-SHEET-MODULUS",
  "status": "objection",
  "note": "Hexoloy SA Form B-1045, opened this check, heads the table Typical Physical Properties. It prints compressive strength 3900 MPa, four-point flexure 380 MPa, Weibull modulus 10, elastic modulus 430 GPa, Poisson 0.14, density 3.10 g/cm3, and flexure bars 3 x 4 x 45 mm. The card scores the inherited 410 GPa and says so. Density matches. The same-bay factors at 430 GPa are recorded and are not a new optimum and not a qualified allowable."
}
```

### N455 — NFI-CHECK-025-NULL-ALLOWABLE

Source `rpt-ref-a8b77f7de2ffc56af7b4`; original file `unpublished-local-ref:d2a2bac9ac804106; pointer `/rows/1`.

```json
{
  "id": "NFI-CHECK-025-NULL-ALLOWABLE",
  "status": "stands",
  "note": "The filed decision leaves qualified Hexoloy SA, CVD SiC and CMC tube compression allowables null. The cited SA figures are typical flexural 380 MPa and typical compression 3900 MPa. Null is not zero strength, and 3.9 GPa is not a qualified tube allowable."
}
```

### N462 — NFI-C022-ALLOWABLE

Source `rpt-ref-f6de390e1555b4ca8e78`; original file `unpublished-local-ref:a3c00555c78ad754; pointer `/rows/5`.

```json
{
  "id": "NFI-C022-ALLOWABLE",
  "kind": "OPEN carried qualification",
  "issue": "Neither3900 MPa compression nor380 MPa flexure supplies a full-sized curved-tube compression allowable.",
  "evidence": {
    "qualified_compression_allowable_Pa": null,
    "qualified_failure_probability": null,
    "source": "inputs/025/CARD.md and ALLOWABLE-INTERFACE.md"
  },
  "next": "Retain null qualified allowable and propagate025's size-dependent tensile hypotheses only within their stated scope.",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION"
}
```

### N506 — NFI-026-08

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/7`.

```json
{
  "id": "NFI-026-08",
  "tag": "QUESTIONABLE",
  "status": "open",
  "owner": "sciences",
  "issue": "Material input editions and thin curved member fabrication",
  "evidence": "Dispatched E=410 GPa retained; archived current Hexoloy-SA sheet gives typical E=430 GPa and nu=0.14. Model uses nu=0.14 for torsion.",
  "implication": "Bulk typical data do not establish thin-wall curved SiC member strength, defects, residual stress or joint capability."
}
```

### N595 — NFI-022D-ALLOWABLE

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/6`.

```json
{
  "id": "NFI-022D-ALLOWABLE",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "NFI-C022-ALLOWABLE",
    "MAINLINE-025"
  ],
  "finding": "Neither 3900 MPa bulk crush nor 380 MPa flexure is a qualified full-size curved SiC compression allowable. No qualified assembly failure probability is known.",
  "next": "Use process/size-specific compression and failure data; keep qualified allowable and failure probability null."
}
```

### N605 — NFI-017b-SIC-ALLOWABLE

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/5`.

```json
{
  "id": "NFI-017b-SIC-ALLOWABLE",
  "tag": "QUESTIONABLE",
  "claim": "Every P3 route to SF 1 needs a qualified SiC design compressive strength of 0.83-1.20 GPa (projection row 0.91 GPa). No design compressive allowable exists; flexure is 380 MPa and 3900 MPa is an unqualified typical value.",
  "needed_to_ground": "Full-size curved tube compression tests with a Weibull (or other probabilistic) basis."
}
```

### N663 — NFI-038-CERAMIC_SIZE

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/12`.

```json
{
  "id": "NFI-038-CERAMIC_SIZE",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Small compression specimens do not establish full curved SiC reliability",
  "evidence": "025 and C1424 scope; no compression size law or full product specification. 022d also assumes an unqualified 15.586 MPa tensile ceiling.",
  "resolution_needed": "Stage process witnesses, representative stubs, loaded contacts and full arcs; qualify tensile/contact response where present and build statistical model.",
  "tests": [
    "T5"
  ]
}
```

### N672 — NFI-CHECK-026-02

Source `rpt-check026-grok-p3-lattice-1020`; original file `unpublished-local-ref:1c3bb69a594eb057; pointer `/rows/1`.

```json
{
  "id": "NFI-CHECK-026-02",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "Vendor typical modulus was not substituted and was not re-fetched",
  "evidence": "E is held at the dispatched 410 GPa. The owner records a sheet typical of 430 GPa and nu 0.14. This check used nu 0.14 for torsion and did not open the sheet again.",
  "implication": "Owner NFI-026-08 stands. Bulk typical data are not an allowable for these members."
}
```

### C003 — NFI-022D-CHECK-03

Source `rpt-ref-4b8e7b08241bb7a45536`; original file `unpublished-local-ref:2fa44902593248ea; pointer `/rows/2`.

```json
{
  "id": "NFI-022D-CHECK-03",
  "owner": "MAINLINE-022d / MAINLINE-025",
  "state": "open qualification",
  "kind": "compression, tension and reliability",
  "evidence": "upstream/025/CARD.md; ALLOWABLE-INTERFACE.md; SOURCE-ARITHMETIC.json",
  "note": "The 3.9 GPa bulk compression input and 15.586 MPa fixed reference tensile screen remain PROJECTION for full arcs. The headline extreme compression is 1.198096384 GPa and opposite-face tensile stress is zero at its target. Contact tension, size-dependent positive-stress exposure and failure statistics are unresolved. Original-continuum versus 1047-member reference counts explain small rounded tensile differences.",
  "settle": "Establish a matched compression/contact basis and calibrated failure populations; update effective stressed size when geometry changes. Preserve null qualified allowable/probability fields until supported.",
  "stops_other_work": false
}
```

### C087 — NFI-C026B-MATERIAL

Source `rpt-ref-b92330879d6ba35bd62c`; original file `unpublished-local-ref:21616ac9b36e6057; pointer `/rows/6`.

```json
{
  "id": "NFI-C026B-MATERIAL",
  "issue": "Thin curved ceramic sections, film strength and joint allowances remain projections.",
  "evidence": "Held E=410 GPa differs from the maker's typical 430 GPa; density 3.10 and nu=0.14 are typical, not allowables.",
  "next_evidence": "Geometry- and process-matched material limits, local wall/failure checks, actual joints, seals and fabrication mass.",
  "tag": "QUESTIONABLE",
  "status": "open",
  "blocks_card": false
}
```

### C153 — NFI-041-01

Source `rpt-ref-c7dfc45babe1b96007db`; original file `unpublished-local-ref:cd543374666d8c21; pointer `/items/0`.

```json
{
  "id": "NFI-041-01",
  "status": "open",
  "topic": "Full-size ceramic material and contact reliability",
  "evidence": [
    "SOURCES.md",
    "RESULTS.json:best_closure_by_reserve",
    "intake/technical/Hexoloy-SA.pdf"
  ],
  "finding": "The best 5% closure witness requires 1.164235 GPa extreme compression under the declared amplified-demand screen. The 3.9 GPa typical compression value and fixed 15.586 MPa tension reliability projection are not qualified allowables for long, thin curved arcs or their contacts. The vendor sheet gives E=430 GPa; the dispatched comparison retains E=410 GPa.",
  "needed": "Production-representative arc and joint/contact tests, defect/size statistics, environmental durability, and a stated reliability model. Resolve the modulus edition and geometry transfer before claiming capacity.",
  "prohibited_inference": "No qualified compression allowable or assembly failure probability follows from the reported required stress."
}
```

### C199 — NFI-043-01

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/0`.

```json
{
  "id": "NFI-043-01",
  "status": "open",
  "topic": "Compression distribution and calibration",
  "finding": "No retrieved SA, CVD SiC, reaction-bonded SiC or SiC/SiC population supplies matched compression m, characteristic strength, effective reference size and confidence bounds for finished P3 members.",
  "needed": "Raw compression failures, specimen and stress-field dimensions, processing/batch information, fracture modes, fit method, competing populations and confidence bounds; evidence of transfer to full curved tubes.",
  "effect": "Qualified compression parameters and actual member/frame Pf remain null. Catalogue 3.9 GPa is only a typical value; hypothetical scale assignments do not qualify it.",
  "stops_other_work": false
}
```

### C203 — NFI-043-05

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/4`.

```json
{
  "id": "NFI-043-05",
  "status": "open",
  "topic": "Flexure reference sizes and statistical meanings",
  "finding": "SA sources report m=10 and m=8; catalogue 380 MPa is typical rather than explicitly a fitted mean. Bend spans are absent. Commercial CVD reports m=11, scale 424 MPa and mean 415 MPa but no specimen dimensions.",
  "needed": "Applicable product revision, specimen spans and orientation, sample sizes, raw data, finish, fit definition and uncertainty. Clarify the CVD mean/scale relationship without replacing the reported scale.",
  "effect": "SA 40/20 mm spans and mean-to-scale conversions remain PROJECTION. Commercial CVD has no justified full-size probability here.",
  "stops_other_work": false
}
```

### C204 — NFI-043-06

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/5`.

```json
{
  "id": "NFI-043-06",
  "status": "open",
  "topic": "RBSC effective-size conventions",
  "finding": "The 2017 paper's labelled effective bend volume equals the 360 mm3 span prism. The normalized stress-power integral at m=8.6 instead gives 1.953125 mm3. Ring values likewise need stress-field interpretation.",
  "needed": "Reconcile the paper's geometric definitions and size-transfer convention with its full stress field and flaw populations before transferring its fitted data.",
  "effect": "Our explicitly defined three-point projection is retained; ring geometric sizes are not used as uniform tensile reference volumes.",
  "stops_other_work": false
}
```

### C205 — NFI-043-07

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/6`.

```json
{
  "id": "NFI-043-07",
  "status": "open",
  "topic": "SiC/SiC population, size and source consistency",
  "finding": "Mini-composite tensile gauge area is missing. The pilot appendix's specimen labels and stated strength range need reconciliation; the scale table header has a unit inconsistency. The compression study uses a different 2.5D architecture and only three coupons.",
  "needed": "Gauge area, full raw data, corrected labels/range/units, fitting details, anisotropic failure mechanisms and matched full-component compression/tension statistics.",
  "effect": "Reported tensile batch m/scale values are preserved separately, not combined with the 460 MPa compression mean or monolithic weakest-link scaling.",
  "stops_other_work": false
}
```

### C209 — NFI-043-11

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/10`.

```json
{
  "id": "NFI-043-11",
  "status": "open",
  "topic": "Lower-tail statistical confidence",
  "finding": "The 433-member targets allocate probabilities near 2.31e-6 and 2.31e-9 per member, well below the empirical resolution of the retrieved small samples.",
  "needed": "Physically justified tail extrapolation, parameter confidence bounds, competing failure populations, batch effects and validated proof-screen modelling.",
  "effect": "Point-estimate Weibull projections are not confidence-qualified reliability predictions. Zero-failure sample counts are illustrative, not a proposed testing campaign.",
  "stops_other_work": false
}
```

### C213 — NFI-043-15

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/14`.

```json
{
  "id": "NFI-043-15",
  "status": "open",
  "topic": "Closest qualified grade and improvement route",
  "finding": "SA is the closest catalogue compression comparison in the retrieved set, but no candidate is qualified for this geometry and target tail. CVD and CMC datasets describe different populations and modes.",
  "needed": "Matched full-member comparisons and evidence that strength, scatter or validated screening can deliver the required combined-stress lower quantile.",
  "effect": "The conditional 2.24427-times 3.9 GPa requirement at m=10 is not an established improvement factor over today's delivered SiC.",
  "stops_other_work": false
}
```

## R061 — SiC tube manufacture at hull scale (025)

**030b source history:** 022d screened lead requires 275.083 mm OD, 1.137365 mm wall, 3.184194 m curved members. Complete product/tolerance/process capability remains unsourced.

**Original question:** P3 needs metre-scale curved thin-walled SiC tubes and a film at 1.5 GPa allowable; the opened supplier example is about 12 in long; not demonstrated products.

### N111 — NFI-027-FRAME-PRODUCT

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-FRAME-PRODUCT",
  "tag": "PROJECTION",
  "issue": "P3 asks for metre-scale curved, thin-walled SiC tubes and a pressure membrane at 1.5 GPa allowable. The opened supplier seal-tube example is typically 12 in long. These components and their formed geometry are not demonstrated products.",
  "next_evidence": "Establish tube/film manufacturing, joints, porosity/leaks, defects, proof loads and installation tolerances; then replace bounds with physical ones."
}
```

### N357 — NFI-022-TUBE

Source `rpt-mainline022-grok-p3-optimistic-floating-point-1020`; original file `unpublished-local-ref:62f20cec268319e4; pointer `retained original identity`.

```json
{
  "id": "NFI-022-TUBE",
  "design_OD_mm": 281.8989450499424,
  "design_length_m": 0.62,
  "design_wall_mm": 0.2163958093517604,
  "exists": "Hexoloy SA process tubes: OD 25 to 381 mm, single piece to 1.4 m, bonded assemblies to 4.9 m. Seal tubes are about 0.30 m long. Silit SiSiC radiant tubes reach OD 300 mm, length 3.5 m, thinnest published wall about 4 mm, Amasic-3D about 2 mm.",
  "factor_length_over_hexoloy_single": 0.4428571428571429,
  "factor_wall_vs_2mm": 0.1081979046758802,
  "state": "PENDING-025. A 250 mm class diameter exists. A 2 m single Hexoloy piece does not. A wall near 0.9 mm is below the 2 mm SiSiC floor and is a PROJECTION for alpha-SiC. MAINLINE-025 owns the manufacture row. These factors are context at the sourced-today geometry, not a closed finding.",
  "source": "https://www.ceramicsrefractories.saint-gobain.com/products/shapes/tubes/hexoloy-sic-process-tubes and the ceramic radiant tube page"
}
```

### N375 — NFI-025-SA-FABRICATION

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/7`.

```json
{
  "id": "NFI-025-SA-FABRICATION",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "exists_today catalogue envelope; target PROJECTION",
  "issue": "Commercial SA large straight tubes do not establish the target thin, curved, long member.",
  "factor": {
    "one_piece_length_m_published": 1.4,
    "original_required_length_m": 2.04,
    "length_extension_factor": 1.4571428571428573,
    "reoptimized_length_extension_factor": 1.6693494474884292,
    "target_OD_m": 0.24737672474737216,
    "target_wall_m": 0.0008802990936851718,
    "certified_target_straightness_or_arc_error": null,
    "equilateral_reoptimized_length_extension_factor": 1.4894151040209567
  },
  "required_next_evidence": "A same-product drawing/process capability record combining diameter, wall, full length, R10 m curvature, thickness uniformity and arc-shape error; prototype measurement and qualification.",
  "note": "Large diameter, long bonded assemblies and thin small tubes cannot be combined into a demonstrated one-piece envelope."
}
```

### N376 — NFI-025-SISIC-WALL

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/8`.

```json
{
  "id": "NFI-025-SISIC-WALL",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "exists_today envelope; substitution PROJECTION",
  "issue": "Published infiltrated SiSiC walls are thicker; its properties differ from sintered SA.",
  "factor": {
    "Silit_minimum_wall_m": 0.004,
    "Amasic3D_minimum_wall_m": 0.002,
    "wall_ratio_to_target": [
      4.543910164958719,
      2.2719550824793595
    ],
    "fixed_OD_assembly_mass_kg": [
      21397.253,
      10863.174
    ],
    "four_mm_wall_SF_without_tensile_limit_upper_bound": 0.24776418112466275,
    "four_mm_wall_SF_with_Ft15p586MPa_projection": 0.213946780855,
    "four_mm_wall_SF_with_Ft380MPa_proxy": 0.233144783027
  },
  "required_next_evidence": "Same-geometry SiSiC mechanical data and process capability, including free-silicon effects and curved construction.",
  "note": "2/4 mm constraints are geometric borrowed screens only. Fixed-OD masses use inherited SA density; reoptimized small-OD cases preserve float mass and must score tensile bending separately. The unconstrained4mm row reaches3.192GPa tension at its limiting load and is an explicitly incomplete upper bound; scoring tensile proxies lowers its optimum."
}
```

### N377 — NFI-025-CVD-FABRICATION

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/9`.

```json
{
  "id": "NFI-025-CVD-FABRICATION",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "in_the_lab patent examples; target PROJECTION",
  "issue": "Historical CVD examples demonstrate relevant dimensions individually, not a current qualified complete arc.",
  "factor": {
    "example_mandrel_diameter_m": 0.2,
    "example_inferred_final_OD_m": 0.202,
    "example_length_m": 1.5,
    "example_wall_m": 0.001,
    "required_diameter_factor": 1.2246372512246146,
    "required_length_factor": 1.36,
    "example_wall_to_required_wall_factor": 1.1359775412396798,
    "other_example_OD_m": 0.6,
    "other_example_length_m": 0.24,
    "other_example_wall_m": 0.003
  },
  "required_next_evidence": "Current production capability and full-sized curved-tube example with deposition uniformity, residual stress, extraction method, defect yield and qualified properties.",
  "note": "Patent evidence is not a current purchase specification or proof of1047 repeatable members. OD202 mm is inferred from a200 mm mandrel plus two1 mm deposits."
}
```

### N380 — NFI-025-CMC-SCALE

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/12`.

```json
{
  "id": "NFI-025-CMC-SCALE",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "exists_today/supplied laboratory products at separate sizes; target PROJECTION",
  "issue": "Long small cladding and wide short rings do not prove the required large thin structural CMC arc.",
  "factor": {
    "wide_NITE_example_OD_m": 0.2,
    "wide_NITE_example_ID_m": 0.194,
    "wide_NITE_example_length_m": 0.08,
    "small_NITE_example_OD_m": 0.012,
    "small_NITE_example_wall_m": 0.001,
    "small_NITE_example_length_m": 0.2,
    "required_large_tube_length_factor_over_wide_example": 25.5
  },
  "required_next_evidence": "Full target-size tube or a different optimized geometry with a demonstrated layup, wall, curvature, joining and compression capacity.",
  "note": "Fiber bridging may improve damage tolerance but does not validate a monolithic isotropic shell model or guarantee a gas-tight matrix after tensile cracking."
}
```

### N465 — NFI-C022-MANUFACTURE

Source `rpt-ref-f6de390e1555b4ca8e78`; original file `unpublished-local-ref:a3c00555c78ad754; pointer `/rows/8`.

```json
{
  "id": "NFI-C022-MANUFACTURE",
  "kind": "OPEN manufacturing projection",
  "issue": "The long-span optimum increases the full-size manufacturing burden beyond025's original two-metre target.",
  "evidence": {
    "022c_projection5_arc_length_m": 6.25129231047749,
    "OD_m": 0.3352802392097589,
    "wall_m": 0.001623088408707305,
    "length_factor_over_025_documented_SA_one_piece_1p4m": 4.465208793198207,
    "status": "No combined curved-tube production qualification established; absence of evidence is not impossibility"
  },
  "next": "Carry the complete diameter/wall/length/curvature/tolerance specification into fabrication evidence and full-size compression/joint tests.",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION"
}
```

### N597 — NFI-022D-MANUFACTURE

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/8`.

```json
{
  "id": "NFI-022D-MANUFACTURE",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "NFI-C022-MANUFACTURE",
    "MAINLINE-025"
  ],
  "finding": "No complete diameter, wall, arc length, curvature and tolerance combination is production-qualified by this scan. Continuous film and fractional node counts are optimization surrogates.",
  "next": "Carry the full geometry, tolerance and process specification into fabrication evidence and full-size tests."
}
```

### N606 — NFI-017b-TUBE-MATERIAL

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/6`.

```json
{
  "id": "NFI-017b-TUBE-MATERIAL",
  "tag": "PROJECTION",
  "claim": "Tube specific stiffness x1.41 (186 MPa per kg/m3) is beyond SiC (best CVD 145). A carbon-fibre tube would need a sourced compressive strength near 0.8-1.2 GPa with that stiffness.",
  "needed_to_ground": "Sourced UHM carbon tube compressive strength and modulus."
}
```

### N620 — NFI-026B-06

Source `rpt-ref-8befdd4c89803adc44a8`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/5`.

```json
{
  "id": "NFI-026B-06",
  "tag": "PROJECTION",
  "status": "open",
  "owner": "sciences",
  "issue": "Actual thin curved SiC sections, film and joints ungrounded",
  "evidence": "E410 GPa comparison input; nu0.14. Film masses184.442/348.856 kg use the source projection; joints5% of tube+film+node mass.",
  "implication": "Fabrication, ceramic defects, residual stress, joint compliance, seals and film strength need separate evidence. No certification."
}
```

### N646 — NFI-026B-06

Source `rpt-ref-4a20323946ecafd56a6b`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/5`.

```json
{
  "id": "NFI-026B-06",
  "tag": "PROJECTION",
  "status": "open",
  "owner": "sciences",
  "issue": "Actual thin curved SiC sections, film and joints ungrounded",
  "evidence": "E410 GPa comparison input; nu0.14. Film masses184.442/348.856 kg use the source projection; joints5% of tube+film+node mass.",
  "implication": "Fabrication, ceramic defects, residual stress, joint compliance, seals and film strength need separate evidence. No certification."
}
```

### C008 — NFI-022D-CHECK-08

Source `rpt-ref-4b8e7b08241bb7a45536`; original file `unpublished-local-ref:2fa44902593248ea; pointer `/rows/7`.

```json
{
  "id": "NFI-022D-CHECK-08",
  "owner": "MAINLINE-022d / MAINLINE-025",
  "state": "open realization",
  "kind": "geometry, manufacture and complete mass",
  "evidence": "Primary counts/mass closure; upstream/025/CARD.md",
  "note": "Fractional area-based node/member counts and exact residual mass closure are model bookkeeping. No integer spherical layout, matched 275.083-mm OD/1.137365-mm wall/3.184194-m curved member process, flaw tolerance, installed equipment or complete attachment/barrier allowance is demonstrated.",
  "settle": "Build an integer geometric and installed-mass bill with matched manufacturing evidence; carry all dimensional and flaw tolerances into mechanics.",
  "stops_other_work": false
}
```

### C207 — NFI-043-09

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/8`.

```json
{
  "id": "NFI-043-09",
  "status": "open",
  "topic": "Manufacturing geometry and flaw population",
  "finding": "The selected tube is approximately 3.184 m long, 275.083 mm OD and 1.137 mm wall. Its L/1000 initial bow is an assumed imperfection, not a measured tolerance distribution or the spherical centerline curvature.",
  "needed": "Demonstrated fabrication capability, full-length section/bow measurements, surface and end preparation, machining/handling damage controls and strength data at this size.",
  "effect": "Current catalogue properties cannot establish the delivered-member lower tail. The actual material improvement factor remains unknown.",
  "stops_other_work": false
}
```

## R062 — P3 node and joint mass (5% assumed; 023 bill 31 to 859 kg)

**030b source history:** 026 discrete inherited mass overruns lift by 61.40 kg. 022d's separate continuum witness closes its own inherited mass contract; that does not repair the 026 mesh or include omitted process masses.

**Original question:** Joints carried at 5 percent (216.4 kg); a SiC pad bearing the member force gives bounds 1938-11620 kg; a 1 MN ceramic load introduction is not a catalog fitting.

### N113 — NFI-027-FRAME-NODES

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-FRAME-NODES",
  "tag": "PROJECTION",
  "issue": "P3 retains 20 g/node and 5% tube-mass joints without measured capacity or complete film-attachment masses. A load-linked node-mass sensitivity changes little numerically, but does not validate the 20 g anchor.",
  "next_evidence": "Size nodes and film attachment/seams from load paths. Same topology with truly similar solid nodes would make each node's mass scale as R^3."
}
```

### N153 — NFI-011-NODES

Source `rpt-ref-f21d4bd21d2026511818`; original file `unpublished-local-ref:b5c9a6937c19e542; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-011-NODES",
  "gap": "Node count is the equilateral-continuum formula (equal members, equal tributary area R*s per member, load N=p*R*s/2 — the 002 pinned load path), node hardware 0.02 kg each, and no separate joint or gusset mass exists for P3 in the pinned mass rules.",
  "direction": "Real geodesic load paths and joint masses before any design pick.",
  "effect": "Node and joint mass growth eats tube mass one-for-one at the ceiling; SF_yield falls in proportion."
}
```

### N311 — NFI-011B-JOINT

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-JOINT",
  "note": "011 had no separate joint mass. This card sets joint mass to 5 percent of tube mass and reduces the tube budget so film, nodes, joints, systems and tube still equal the lift mass. The 5 percent is the P2 sandwich fraction applied to tubes, not a measured fitting. RESULTS carries a 6061 scan with the joint term removed. Node mass remains 0.02 kg times V(s)."
}
```

### N358 — NFI-022-JOINTS

Source `rpt-mainline022-grok-p3-optimistic-floating-point-1020`; original file `unpublished-local-ref:62f20cec268319e4; pointer `retained original identity`.

```json
{
  "id": "NFI-022-JOINTS",
  "allowance_kg": 216.4271448895479,
  "lower_bound_kg": 1937.6527363866064,
  "upper_bound_kg": 11619.759954966023,
  "member_force_N": 295857.48359825916,
  "factor_lower_over_allowance": 8.9529099382403,
  "state": "PENDING-023. This card carries joints at 5 percent of film, nodes and tubes, 216.427144889 kg. The bounds are context only: a SiC pad at 380 MPa over one tube diameter of engagement. MAINLINE-023 owns the joint mass. A 1 MN ceramic load introduction is not a catalog fitting.",
  "tag": "PENDING-023"
}
```

### N381 — NFI-025-JOINT-MASS

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/13`.

```json
{
  "id": "NFI-025-JOINT-MASS",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "PROJECTION",
  "issue": "Fixed node mass and5% joint mass have no demonstrated force-transfer design.",
  "factor": {
    "node_mass_each_kg": 0.02,
    "joint_mass_fraction": 0.05,
    "original_joint_budget_per_member_end_kg": 0.1077761395507985,
    "original_member_end_force_N": 973700.5467217801,
    "equilateral_original_member_end_force_N": 562166.2727599056
  },
  "required_next_evidence": "Dimensioned fittings and load path with ceramic bearing, tensile splitting, assembly tolerance, preload and actual mass.",
  "note": "Any mass growth reduces available tube material and increases mean compressive demand; no permission to borrow the entire lift mass twice."
}
```

### N500 — NFI-026-02

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/1`.

```json
{
  "id": "NFI-026-02",
  "tag": "QUESTIONABLE",
  "status": "open",
  "owner": "sciences",
  "issue": "Discrete geometry exceeds inherited mass allowance",
  "evidence": "362 joints/1080 arcs; mass 4950.843078 kg versus allowance 4889.442150 kg; payload -61.400928 kg.",
  "implication": "The original just-floating point is not preserved by the actual geodesic realization; film shape and all real joints remain ungrounded."
}
```

### C033 — N039-12

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/11`.

```json
{
  "id": "N039-12",
  "issue": "Lattice joining is a projection",
  "detail": "Ribs: a 25 mm foot under one AF 0.015 lb/ft2 line, plus 5% of rib mass for splices and nodes. Frame: a 30 mm AF land plus two 5 mm paste fillets, 026's 0.02 kg nodes, and 023's Ti sleeves (157.7 kg at 562.2 kN, 030 register R064) scaled by member force.",
  "to_close": "A joint card for ribs or frames on the sandwich.",
  "tag": "PROJECTION"
}
```

## R063 — P3 node moment rigidity required by the smeared global mode

**030b source history:** 026 freely rolling curved ball-pin members have zero-strain mechanisms; actual anti-roll/film or joint rotational stiffness is required. The nominal rigid-joint solution is not a measured connection.

**Original question:** Smeared bending stiffness assumes members continuous through nodes; pinned or soft nodes lower the global mode. Member torsion omitted (would add 11.8-13.7%).

### N020 — NFI-CHK011B-JOINTS

Source `rpt-check011b-opus-1020`; original file `unpublished-local-ref:252e7a0b939c4177; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK011B-JOINTS",
  "state": "asserted",
  "direction": "optimistic (condition)",
  "note": "The smeared D (Buchert's t_B) presumes members continuous in bending through the nodes, which means moment-rigid joints. With pinned or soft nodes the bending stiffness and the global mode fall, so 023's joints must carry member-end moments as well as axial force. Member torsion is omitted; with torsion-rigid joints it would raise the global SF by 13.7% for SiC (nu 0.14) and 11.8% for 6061 (lattice sum D1111 1.454 or 1.407 against 1.125)."
}
```

### N393 — NFI-023-CHECK-NODE-LOAD-PATH

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/3`.

```json
{
  "id": "NFI-023-CHECK-NODE-LOAD-PATH",
  "status": "open",
  "non_blocking": true,
  "field": "m_joint_kg and smeared bending stiffness",
  "reported": "31.039kg of wrap,157.685kg Ti orthe re-closed socket mass plus.02kg/node described as fittings.",
  "check": {
    "sixfold_pressure_force_N": 344045.7589290622,
    "remaining_load_path": "No sized central receiver/hub, collector, load turning, film attachment or measured rotational stiffness. Braze model only extends a ceramic wall."
  },
  "evidence": [
    "CHECK.md",
    "joint formulas",
    "011b D=(3sqrt3/4)EI/s"
  ],
  "next": "Define a complete node geometry and its mass/stiffness. Preserve present values as partial end-material estimates; do not assume they establish the global D used in the score."
}
```

### N508 — NFI-026-10

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/9`.

```json
{
  "id": "NFI-026-10",
  "tag": "PROJECTION",
  "status": "open",
  "owner": "sciences",
  "issue": "Beam and joint idealizations",
  "evidence": "Euler–Bernoulli, circular undeformed cross-sections, stress-free initial curves, perfectly rigid or fully free ball joints.",
  "implication": "Shear flexibility, cross-section distortion, brittle failure, finite joint stiffness and construction stress require independent grounding."
}
```

### N664 — NFI-038-JOINT_STIFFNESS

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/13`.

```json
{
  "id": "NFI-038-JOINT_STIFFNESS",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Required P3 rotation/roll stiffness is unknown",
  "evidence": "026 free-roll mechanisms; 022d joints have axial/bond sizing only.",
  "resolution_needed": "Measure loaded stiffness matrix and define acceptance by exact discrete-frame sweeps.",
  "tests": [
    "T6",
    "T8"
  ]
}
```

## R064 — P3 tube-end joint routes at about 0.5 MN (023: CFRP wrap, Ti, Invar, braze, pin, bond to SiC)

**030b source history:** CHECK-022b/022c establishes that old joints sized at lambda1 did not support quoted multipliers. 022d charges lambda-squared joint mass and sizes nominal axial/bond capacities at its target. Adhesive mass, peel, bearing, moment transfer and actual SiC bonds remain open.

**Original question:** The rough 0.5 kg fitting was the pin at the two-way force; at the equilateral force the pin is 0.202 kg and the wall still cannot bear it.

### N214 — NFI-023-CFRP-WRAP

Source `rpt-ref-a4768f77870336c8cdbb`; original file `unpublished-local-ref:8fc6d5cd4b5f84d2; pointer `retained original identity`.

```json
{
  "id": "NFI-023-CFRP-WRAP",
  "value": "1470 MPa compression, ASTM D695, Torayca T700S with 250 F epoxy, normalized to 60 percent fiber volume. Tensile 2550 MPa on the same sheet is not used. Density 1550 kg/m3 is the 011b quasi-isotropic value.",
  "state": "PROJECTION",
  "issue": "The lightest joint is this wrap: 0.015 kg per end and 31.0 kg at 562.2 kN. The fiber and the coupon exist today. A wound transition on an SiC tube does not.",
  "consequence": "The mass is a sizing, not a qualified joint. Using the tensile allowable would understate it.",
  "next": "A compression coupon of the wrap, bonded to SiC, at the bond length this card sizes."
}
```

### N215 — NFI-023-ADHESIVE-TRANSFER

Source `rpt-ref-a4768f77870336c8cdbb`; original file `unpublished-local-ref:8fc6d5cd4b5f84d2; pointer `retained original identity`.

```json
{
  "id": "NFI-023-ADHESIVE-TRANSFER",
  "value": "28.9 MPa at 25 C, ASTM D1002, LOCTITE EA 9394 AERO, phosphoric-acid anodized 2024-T3 bare aluminum, cured 5 days at 25 C. 22.7 MPa at -55 C and 20.7 MPa at 82 C. Peel is low.",
  "state": "exists today",
  "issue": "The paste exists today. The adherend in the coupon is aluminum, not SiC. The bond at 562.2 kN on the 011b radius is 25.0 mm. It uses 28.9 MPa with no temperature knockdown and no peel length.",
  "consequence": "Every bonded sleeve and the wrap carry this transfer. A lower shear lengthens the bond and raises the mass in proportion.",
  "next": "Lap shear of EA 9394 on the SiC surface that would actually be bonded, at the service temperature."
}
```

### N216 — NFI-023-TI-SLEEVE

Source `rpt-ref-a4768f77870336c8cdbb`; original file `unpublished-local-ref:8fc6d5cd4b5f84d2; pointer `retained original identity`.

```json
{
  "id": "NFI-023-TI-SLEEVE",
  "value": "AMS 4911 annealed Ti-6Al-4V, minimum yield 827 MPa, minimum ultimate 896 MPa, density 4.43 g/cm3. The pin shear is 0.6 times that yield, derived here, not a handbook shear.",
  "state": "exists today",
  "issue": "The sheet exists today. At 562.2 kN the sleeve is 0.075 kg per end and 157.7 kg, 0.70 times the 225.5 kg allowance. Frozen least SF is 1.232 by the film. Re-optimised least SF is 1.431 at k 0.2 and 1.995 at k 0.4.",
  "consequence": "At the equilateral force the titanium sleeve fits inside the 5 percent allowance. The first filing's 473.1 kg was the two-way force.",
  "next": "None."
}
```

### N217 — NFI-023-INVAR

Source `rpt-ref-a4768f77870336c8cdbb`; original file `unpublished-local-ref:8fc6d5cd4b5f84d2; pointer `retained original identity`.

```json
{
  "id": "NFI-023-INVAR",
  "value": "Carpenter Invar 36, annealed bars and strip, yield 276 MPa, ultimate 448 MPa, density 8.05 g/cm3, linear CTE 1.3 µm/m-C near 93 C.",
  "state": "exists today",
  "issue": "The alloy exists today and is the expansion match. At 562.2 kN the sleeve is 0.410 kg per end and 858.6 kg, 3.81 times the allowance. Frozen least SF is 1.054, global. Re-optimised least SF is 1.245 at k 0.2 and 1.616 at k 0.4.",
  "consequence": "Invar now closes. It remains several times the 5 percent allowance. The CTE advantage is not scored as a stress.",
  "next": "None, unless a higher allowable or a shorter bonded detail is sourced."
}
```

### N218 — NFI-023-BRAZE

Source `rpt-ref-a4768f77870336c8cdbb`; original file `unpublished-local-ref:8fc6d5cd4b5f84d2; pointer `retained original identity`.

```json
{
  "id": "NFI-023-BRAZE",
  "value": "25 MPa compressive shear, the low end of 25-30 MPa, Cusil-ABA on monolithic SiC/Mo and SiC/Kovar. Singh and Asthana, J. Materials Engineering and Performance, 2020, doi 10.1007/s11665-020-04934-3.",
  "state": "in the lab",
  "issue": "The shear pair is a lab result. At 562.2 kN the socket is the tube wall continued for 28.9 mm, 0.062 kg per end and 130.6 kg, 0.58 times the allowance. Frozen least SF is 1.232. A solid node is not sized. A co-sintered frame is a PROJECTION. The 342 MPa bend result failed in the ceramic and is not a shear allowable.",
  "consequence": "This is the lightest metallic path, and it is not a catalog node.",
  "next": "A shear measurement on the tube diameter, and a socket section if the wall cannot simply continue."
}
```

### N219 — NFI-023-PIN-BEARING

Source `rpt-ref-a4768f77870336c8cdbb`; original file `unpublished-local-ref:8fc6d5cd4b5f84d2; pointer `retained original identity`.

```json
{
  "id": "NFI-023-PIN-BEARING",
  "value": "Pin mass 0.202 kg at 562.2 kN, diameter 26.9 mm, two-wall bearing 11.9 GPa on the 0.880 mm tube.",
  "state": "exists today",
  "issue": "The rough 0.5 kg titanium fitting was this pin at the two-way force. At 562.2 kN it is 0.202 kg and the wall still cannot bear it. The titanium sleeve is 0.075 kg.",
  "consequence": "The 0.5 kg figure is not the joint mass, and it is not a usable detail on this wall.",
  "next": "None. The pin is a reference, not a candidate."
}
```

### N372 — NFI-025-CONTACT

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/4`.

```json
{
  "id": "NFI-025-CONTACT",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "PROJECTION",
  "issue": "Unknown node/seat geometry and stress-weighted tensile regions.",
  "factor": {
    "original_member_end_force_N": 973700.5467217801,
    "Ct_screen_m8": 0.005035105985369126,
    "Ct_screen_m10_approx": 0.010912,
    "actual_Ct": null,
    "actual_stressed_effective_size": null,
    "end_forces_N_by_force_rule": {
      "equilateral_equilibrium": 562166.2727599056,
      "legacy_pRs_over2": 973700.5467217801
    },
    "uniform_tensile_contact_Ct_hypotheses_by_force_rule": {
      "equilateral_equilibrium": [
        {
          "m": 8,
          "flaw_measure": "volume",
          "Ct": 0.008721058962049048,
          "classification": "PROJECTION for this uniform tensile-field hypothesis only"
        },
        {
          "m": 8,
          "flaw_measure": "surface",
          "Ct": 0.009945655791219508,
          "classification": "PROJECTION for this uniform tensile-field hypothesis only"
        },
        {
          "m": 10,
          "flaw_measure": "volume",
          "Ct": 0.018899508770244062,
          "classification": "PROJECTION for this uniform tensile-field hypothesis only"
        },
        {
          "m": 10,
          "flaw_measure": "surface",
          "Ct": 0.021389725093776162,
          "classification": "PROJECTION for this uniform tensile-field hypothesis only"
        }
      ],
      "legacy_pRs_over2": [
        {
          "m": 8,
          "flaw_measure": "volume",
          "Ct": 0.005035105739357616,
          "classification": "PROJECTION for this uniform tensile-field hypothesis only"
        },
        {
          "m": 8,
          "flaw_measure": "surface",
          "Ct": 0.005742127048327943,
          "classification": "PROJECTION for this uniform tensile-field hypothesis only"
        },
        {
          "m": 10,
          "flaw_measure": "volume",
          "Ct": 0.010911636476052101,
          "classification": "PROJECTION for this uniform tensile-field hypothesis only"
        },
        {
          "m": 10,
          "flaw_measure": "surface",
          "Ct": 0.01234936354078376,
          "classification": "PROJECTION for this uniform tensile-field hypothesis only"
        }
      ]
    }
  },
  "required_next_evidence": "Resolved three-dimensional contact model with real seat radius, compliance, friction, misalignment, residual stress and bearing width; full joint tests.",
  "note": "Ct is positive principal tensile stress divided by mean axial compression, not bearing pressure. Full-volume caps only illustrate a hypothetical field; actual smaller hot spots require correct surface/volume/edge integration. Original unqualified force/Ct keys refer to the inherited case; the new branch-specific arrays score both demands."
}
```

### N392 — NFI-023-CHECK-JOINT-MARGIN

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/2`.

```json
{
  "id": "NFI-023-CHECK-JOINT-MARGIN",
  "status": "open",
  "non_blocking": true,
  "field": "reported least SF1.466/2.061 for wrap shell search",
  "reported": "The six scored modes exclude joint strength. End sections and bonds are sized at N/strength and N/shear.",
  "check": {
    "nominal_joint_strength_SF": 1.0,
    "frozen_joint_inclusive_nominal_SF": 1.0,
    "wrap_shell_k02": 1.4658145265725706,
    "wrap_shell_k04": 2.0607540827668074,
    "sleeve_scaling_for_target_q": "end mass scales q^2 at fixed section; braze overlap scales q"
  },
  "evidence": [
    "CHECK.md joint sizing derivation",
    "RESULTS.json nominal_joint_SF"
  ],
  "next": "Label existing factors shell-only. Include joint modes and resize at the desired load factor before quoting assembled-frame margin."
}
```

### N394 — NFI-023-CHECK-BOND-MASS-AND-TRANSFER

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/4`.

```json
{
  "id": "NFI-023-CHECK-BOND-MASS-AND-TRANSFER",
  "status": "open",
  "non_blocking": true,
  "field": "metal sleeve/CFRP mass and bond allowable",
  "reported": "EA9394 nominal shear28.9MPa and no adhesive mass in the budget.",
  "check": {
    "bond_area_m2_per_end": 0.019452120164702612,
    "additional_adhesive_mass_per_100um_gap_kg": 5.534469519646309,
    "gap_status": "100micron is a sensitivity assumption, not a selected design",
    "source_status": "Aluminum lap-shear typical datum; SiC, peel, environment and design basis unresolved"
  },
  "evidence": [
    "Henkel TDS pp1,3–5",
    "independent volume calculation"
  ],
  "next": "Specify bondline thickness and charge its mass, then establish SiC joint strength and load-transfer distribution for the required conditions."
}
```

### N395 — NFI-023-CHECK-BRAZE-PAIR

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/5`.

```json
{
  "id": "NFI-023-CHECK-BRAZE-PAIR",
  "status": "open",
  "non_blocking": true,
  "field": "Cusil-ABA socket",
  "reported": "25MPa coupon shear used on a continued SiC tube wall.",
  "check": "Primary publisher abstract identifies SiC/Mo and SiC/Kovar, not an all-SiC tubular node. Receiver metal, braze filler, residual stress and central connection are not sized.",
  "evidence": [
    "sources/braze2020-reading.json",
    "INPUTS.json"
  ],
  "next": "Name the actual material pair and include receiver/filler geometry and mass; retain in-the-lab evidence and PROJECTION assembly tag."
}
```

### N397 — NFI-023-CHECK-PIN-SPAN

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/7`.

```json
{
  "id": "NFI-023-CHECK-PIN-SPAN",
  "status": "open",
  "non_blocking": true,
  "field": "pin_clevis_reference.length_m and mass_kg",
  "reported": "A3d pin is assumed for a two-wall bearing calculation.",
  "check": {
    "length_3d_m": 0.08056850952246337,
    "tube_OD_m": 0.24737672474737216,
    "mass_for_2r_span_minimum_kg": 0.6207841105826379,
    "bearing_Pa": 11889414314.899754
  },
  "evidence": [
    "RESULTS.json supplements",
    "pin volume and diameter geometry"
  ],
  "next": "If used as a through-tube reference, include the full span plus lugs and pin bending. It is already rejected on bearing; keep it out of candidate mass ranking."
}
```

### N460 — NFI-C022-JOINT-MULTIPLIER

Source `rpt-ref-f6de390e1555b4ca8e78`; original file `unpublished-local-ref:a3c00555c78ad754; pointer `/rows/3`.

```json
{
  "id": "NFI-C022-JOINT-MULTIPLIER",
  "kind": "DEMONSTRATED model-scope omission",
  "issue": "023's sleeve/wrap dimensions consume the assumed axial and bond allowables at design force N; the frozen joint has no modeled pressure margin above1.",
  "evidence": {
    "GAMMA/cfrp_zylon_5": {
      "published_frame_multiplier": 1.4869170968607484,
      "frozen_joint_capacity_multiplier_under_023_sizing": 1.0,
      "published_joint_mass_kg": 23.11034020907313,
      "mass_factor_if_resized_for_reported_multiplier": 2.210922452936796,
      "joint_mass_if_resized_at_same_radius_kg": 51.095170063247835,
      "extra_mass_if_resized_at_same_radius_kg": 27.984829854174702,
      "scope": "Conditional sizing-law implication; structural reoptimization must charge changed joint mass. No physical joint qualification implied."
    },
    "FOLD/cfrp_zylon_019": {
      "published_frame_multiplier": 1.4182991741260802,
      "frozen_joint_capacity_multiplier_under_023_sizing": 1.0,
      "published_joint_mass_kg": 23.185496143546445,
      "mass_factor_if_resized_for_reported_multiplier": 2.011572547326721,
      "joint_mass_if_resized_at_same_radius_kg": 46.63930753850759,
      "extra_mass_if_resized_at_same_radius_kg": 23.453811394961143,
      "scope": "Conditional sizing-law implication; structural reoptimization must charge changed joint mass. No physical joint qualification implied."
    },
    "022c_cap/cfrp_zylon_5": {
      "published_frame_multiplier": 1.485116372061561,
      "frozen_joint_capacity_multiplier_under_023_sizing": 1.0,
      "published_joint_mass_kg": 23.111041059270214,
      "mass_factor_if_resized_for_reported_multiplier": 2.205570638565293,
      "joint_mass_if_resized_at_same_radius_kg": 50.97303358700331,
      "extra_mass_if_resized_at_same_radius_kg": 27.861992527733094,
      "scope": "Conditional sizing-law implication; structural reoptimization must charge changed joint mass. No physical joint qualification implied."
    },
    "022c_cap/cfrp_zylon_019": {
      "published_frame_multiplier": 1.4170465717478142,
      "frozen_joint_capacity_multiplier_under_023_sizing": 1.0,
      "published_joint_mass_kg": 23.18138839899542,
      "mass_factor_if_resized_for_reported_multiplier": 2.0080209865022334,
      "joint_mass_if_resized_at_same_radius_kg": 46.54871440144221,
      "extra_mass_if_resized_at_same_radius_kg": 23.36732600244679,
      "scope": "Conditional sizing-law implication; structural reoptimization must charge changed joint mass. No physical joint qualification implied."
    }
  },
  "next": "Add joint strength to the least-factor calculation, or size joints at lambda*N and charge their lambda^2 mass before reoptimization; qualify rotational stiffness separately.",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION"
}
```

### N579 — NFI-034-JOINT-ADHESIVE-MASS

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/7`.

```json
{
  "id": "NFI-034-JOINT-ADHESIVE-MASS",
  "tag": "PROJECTION",
  "finding": "The 023 end-material estimate omits adhesive mass. At nominal inherited bond area, assumed 0.2 mm gap and 1400 kg/m3 density, this card adds 12.565 kg for Ti sleeves and 4.078 kg for CFRP wraps. Shear-transfer and gap assumptions remain unqualified.",
  "proposed_next": "Book cured adhesive, primers and process losses against the complete assembly and qualify actual joints."
}
```

### N590 — NFI-022D-JOINT

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/1`.

```json
{
  "id": "NFI-022D-JOINT",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "NFI-C022-JOINT-MULTIPLIER",
    "NFI-C022-DISCRETE-JOINTS"
  ],
  "finding": "023 axial/bond dimensions now use each candidate's lambda and their lambda-squared mass. SiC adhesion, peel, moment transfer, local bearing, sleeve stability and adhesive mass remain unknown. Percent joints have no scored capacity.",
  "next": "Use qualified end-joint stiffness/capacity and complete mass in the discrete structure."
}
```

### C005 — NFI-022D-CHECK-05

Source `rpt-ref-4b8e7b08241bb7a45536`; original file `unpublished-local-ref:2fa44902593248ea; pointer `/rows/4`.

```json
{
  "id": "NFI-022D-CHECK-05",
  "owner": "MAINLINE-022d / MAINLINE-023",
  "state": "open qualification",
  "kind": "joint mass, material provenance and force transfer",
  "evidence": "upstream/023/INPUTS.json; web-sources Toray/Henkel PDFs; SOURCES.md",
  "note": "Candidate-multiplier joint sizing is correct, including quadratic mass. At the headline, 44.191468267 kg and 1.258252477 axial/bond multipliers are consequences of equal-stress design, without extra reserve. Legacy Toray supports 1470 MPa but does not establish 1550 kg/m3 composite density. Henkel's 28.9 MPa datum is prepared aluminum, not SiC. Percent-joint cases have unknown capacity; sub-unity Ti cases size below operating demand.",
  "settle": "Pin density and laminate/manufacturing specification; verify ceramic adhesion, peel, load spreading, moment transfer and rotational stiffness; include adhesive and attachment mass.",
  "stops_other_work": false
}
```

### C068 — NFI-034-JOINT-ADHESIVE-MASS

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/7`.

```json
{
  "id": "NFI-034-JOINT-ADHESIVE-MASS",
  "tag": "PROJECTION",
  "finding": "The 023 end-material estimate omits adhesive mass. At nominal inherited bond area, assumed 0.2 mm gap and 1400 kg/m3 density, this card adds 12.565 kg for Ti sleeves and 4.078 kg for CFRP wraps. Shear-transfer and gap assumptions remain unqualified.",
  "proposed_next": "Book cured adhesive, primers and process losses against the complete assembly and qualify actual joints.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C155 — NFI-041-03

Source `rpt-ref-c7dfc45babe1b96007db`; original file `unpublished-local-ref:cd543374666d8c21; pointer `/items/2`.

```json
{
  "id": "NFI-041-03",
  "status": "open",
  "topic": "Joint strength, density, rotational stiffness and mass",
  "evidence": [
    "MODES.csv",
    "RESULTS.json:selected_realization",
    "intake/joint/toray-legacy.pdf",
    "intake/joint/henkel-ea9394.pdf"
  ],
  "finding": "Actual member-end axial force, bending and torsion are included in the annular-sleeve and ring-bond demand. The selected frame reaches 3.356559 kN m end bending and 1.118657 kN m torsion. Equal-stress resized joints attain the requested scalar target by construction, without surplus reserve. The 1550 kg/m3 composite density is assumed; Toray's laminate strength and Henkel's prepared-aluminum shear result do not establish the proposed SiC joint.",
  "needed": "A joint architecture, laminate orientation/thickness, bondline and surface treatment, peel and transverse/torsional shear interaction, cyclic/environmental data, contact stress and measured rotational stiffness. Include all hardware mass.",
  "prohibited_inference": "Scalar sleeve/bond sizing does not establish a rigid joint, full multiaxial strength or a manufactured joint mass."
}
```

### C201 — NFI-043-03

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/2`.

```json
{
  "id": "NFI-043-03",
  "status": "open",
  "topic": "Joint and end-interface reliability",
  "finding": "The source's approximately 44.19 kg CFRP joining estimate and 44.02 mm overlap do not establish rotation, contact, adhesive peel, end damage or statistical reliability for roughly 866 end interfaces.",
  "needed": "Joint geometry and stiffness, local contact and bond stresses, combined-load tests, processing variability, failure distributions, environmental durability and allocation of joint risk.",
  "effect": "The tube-only risk budget omits an unresolved system contribution. The proxy moment is not a physical bound.",
  "stops_other_work": false
}
```

## R065 — fibre cross-ply membranes as film (Zylon, Dyneema): not a sourced film; resin, life, gas-tightness

**030b source history:** DEMONSTRATED source-contract correction: total Zylon 0/90 gauge must be shared between directions. Old published cap points fall to film SF .746876/.708523 at fixed geometry. 022d charges both plies and reoptimizes; an actual complete membrane remains unqualified.

**Original question:** A uniaxial filament needs a 0/90 build for both pillow directions, doubling thickness; resin not included so a real laminate is heavier.

### N085 — NFI-ZYLON-EXTRAPOLATION

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-ZYLON-EXTRAPOLATION",
  "state": "exists as a filament test note",
  "note": "The 19 year life is Toyobo's extrapolation of an HM filament at 60 percent of break, not a laminate test."
}
```

### N086 — NFI-CROSSPLY

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-CROSSPLY",
  "state": "assumption",
  "note": "A uniaxial filament needs a 0/90 build to carry both pillow directions. Total thickness is twice the one-direction thickness. No resin is included, so a real laminate is heavier."
}
```

### N087 — NFI-DYNEEMA-ROPE

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-DYNEEMA-ROPE",
  "state": "exists as a rope example",
  "note": "The 20 percent fraction and the 15 and 250 year lives are indicative rope numbers at 16 C, not a film."
}
```

### N088 — NFI-DYNEEMA-DENSITY

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-DYNEEMA-DENSITY",
  "state": "derived from the same row",
  "note": "Density is the printed GPa divided by the printed N/tex. The sheet does not print density."
}
```

### N098 — NFI-FABRIC-POROUS

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-FABRIC-POROUS",
  "state": "assumption",
  "note": "A filament crossply is not taken as gas-tight. The barrier is a separate layer."
}
```

### N412 — NFI-CHK024-COMPLETE-SYSTEM

Source `rpt-ref-7d6892c4e55be16ad523`; original file `unpublished-local-ref:0d655e2d18e3e532; pointer `/open/1`.

```json
{
  "id": "NFI-CHK024-COMPLETE-SYSTEM",
  "kind": "unclosed system mass",
  "tag": "PROJECTION",
  "finding": "The lightest Zylon row is 109.701010474 kg of ideal two-direction fibre only. Resin, barrier substrate/coating, attachments and installation losses are unbooked. No complete gas-tight film system mass is supplied. Fibre alone exceeds the 97.515 kg pin.",
  "proposed_next": "Retain a structural lower bound and separately book the full assembly before claiming a lightest system."
}
```

### N416 — NFI-CHK024-CREEP-TRANSFER

Source `rpt-ref-7d6892c4e55be16ad523`; original file `unpublished-local-ref:0d655e2d18e3e532; pointer `/open/5`.

```json
{
  "id": "NFI-CHK024-CREEP-TRANSFER",
  "kind": "filament and rope transfer",
  "tag": "PROJECTION",
  "finding": "Toyobo 19 years at 60% break is extrapolated HM filament performance. DSM 15/250 years at 20% break is an indicative 16 C rope comparison. Neither qualifies a resin-free 0/90 pressure membrane, joints or weather exposure. Toyobo calls for light protection outdoors.",
  "proposed_next": "Tag proposed membranes PROJECTION, while retaining sourced fibre inputs as QUESTIONABLE."
}
```

### N457 — NFI-C022-ZYLON-DIRECTION

Source `rpt-ref-f6de390e1555b4ca8e78`; original file `unpublished-local-ref:a3c00555c78ad754; pointer `/rows/0`.

```json
{
  "id": "NFI-C022-ZYLON-DIRECTION",
  "kind": "DEMONSTRATED source-contract mismatch",
  "issue": "022b and022c assign the full total0/90 thickness to both tensile directions.",
  "evidence": {
    "GAMMA/cfrp_zylon_5/equilateral": {
      "owner_film_SF": 1.493752313214508,
      "owner_least_SF": 1.4869170968607484,
      "corrected_fixed": {
        "nodes": 49.9682476491694,
        "members": 143.9047429475082,
        "n_coef": 15.877132402714711,
        "m_nodes": 0.999364952983388,
        "m_film": 220.89798035984265,
        "m_joint": 23.110340209073133,
        "m_tube": 4131.887783245819,
        "m_end": 0.08029735412370334,
        "reserve": 412.54668142228127,
        "sag_kg": 168.07457391278123,
        "vehicle": 4476.895468767718,
        "s_m": 5.5,
        "r_o_m": 0.16612890712314143,
        "t_film_m": 0.00011268270991437619,
        "t_w_m": 0.0016002518156523866,
        "rt": 103.81422817221703,
        "A_m2": 0.0016623277743038382,
        "I_m4": 2.2719238240518985e-05,
        "length_m": 5.571794047833012,
        "N_N": 1515644.3628330787,
        "sigma_axial_Pa": 911760235.4131461,
        "k": 0.2,
        "gamma": 0.575609423195937,
        "SF_local_gamma1": 2.5989479405321996,
        "SF_least": 0.746876156607254,
        "eta": 0.06772720582880326,
        "Euler_stress_Pa": 1781437526.0538108,
        "mass_closure_kg": 4889.44215019,
        "radius_cap_fraction": 0.6645156284925657,
        "NASA_L_over_midradius": 33.701295121607465,
        "SF_yield": 4.277440327536101,
        "SF_euler": 1.9538442858791574,
        "SF_local": 1.4959789249660078,
        "SF_film": 0.746876156607254,
        "SF_perry": 1.8527315163032803,
        "SF_global": 1.4869170968607397,
        "governing": "film",
        "k04_governing": "film",
        "k04_SF_least": 0.746876156607254,
        "k04_SF_global": 2.9738341937214794,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 911760235.4131461,
          "bending_Pa": 126490023.35532774,
          "maximum_compression_Pa": 1038250258.7684739,
          "opposite_signed_compression_Pa": 785270212.0578184,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 0.746876156607254,
          "mean_compression_Pa": 680971980.3726958,
          "bending_Pa": 74659752.83746427,
          "maximum_compression_Pa": 755631733.21016,
          "opposite_signed_compression_Pa": 606312227.5352316,
          "maximum_tension_Pa": 0.0
        }
      },
      "reason": "024 t_total=2*t_direction; original scalar film formula silently gives both directions the entire thickness",
      "corrected_continuous": {
        "nodes": 39.61919481919406,
        "members": 112.85758445758216,
        "n_coef": 17.92851195695453,
        "m_nodes": 0.7923838963838812,
        "m_film": 471.3732138668519,
        "m_joint": 22.6616377150998,
        "m_tube": 3860.3524261922958,
        "m_end": 0.10039926790927038,
        "reserve": 434.26248851936737,
        "sag_kg": 189.7903810098674,
        "vehicle": 4455.1796616706315,
        "s_m": 6.210618722710272,
        "r_o_m": 0.16941827463860343,
        "t_film_m": 0.00024045313150007253,
        "t_w_m": 0.0016494464590654891,
        "rt": 102.712200027753,
        "A_m2": 0.0017472660979960986,
        "I_m4": 2.4832552675057038e-05,
        "length_m": 6.315030609768604,
        "N_N": 1711470.7739602546,
        "sigma_axial_Pa": 979513524.5416272,
        "k": 0.2,
        "gamma": 0.5772273921292778,
        "SF_local_gamma1": 2.445133853603939,
        "SF_least": 1.4113982377227536,
        "eta": 0.07527892343097659,
        "Euler_stress_Pa": 1442098739.0231354,
        "mass_closure_kg": 4889.44215019,
        "radius_cap_fraction": 0.6776730985544137,
        "NASA_L_over_midradius": 37.457130222294154,
        "SF_yield": 3.9815683012902174,
        "SF_euler": 1.472260160673105,
        "SF_local": 1.411398237722813,
        "SF_film": 1.4113982384134245,
        "SF_perry": 1.4113982377229664,
        "SF_global": 1.4113982377227536,
        "governing": "global",
        "k04_governing": "local",
        "k04_SF_least": 1.411398237722813,
        "k04_SF_global": 2.8227964754455073,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 979513524.5416272,
          "bending_Pa": 229872535.51115158,
          "maximum_compression_Pa": 1209386060.0527787,
          "opposite_signed_compression_Pa": 749640989.0304756,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 1.4113982377227536,
          "mean_compression_Pa": 1382483662.3636558,
          "bending_Pa": 2517516337.626968,
          "maximum_compression_Pa": 3899999999.9906235,
          "opposite_signed_compression_Pa": -1135032675.263312,
          "maximum_tension_Pa": 1135032675.263312
        },
        "search": {
          "method": "independent differential evolution plus bounded-accepted simplex",
          "seed": 492,
          "spacing_upper_m": 8.0,
          "outer_radius_upper_m": 0.25,
          "evaluations": 6836,
          "DE_success": true,
          "DE_message": "Optimization terminated successfully.",
          "certified_global_optimum": false
        }
      }
    },
    "GAMMA/cfrp_zylon_5/two_way": {
      "owner_film_SF": 2.42605486452869,
      "owner_least_SF": 2.19141132446645,
      "corrected_fixed": {
        "nodes": 46.73610044271688,
        "members": 89.47220088543376,
        "n_coef": 26.5,
        "m_nodes": 0.9347220088543376,
        "m_film": 345.72194891053465,
        "m_joint": 37.1413523700397,
        "m_tube": 3999.2092481660266,
        "m_end": 0.2075580571534056,
        "reserve": 406.43487873454376,
        "sag_kg": 161.96277122504372,
        "vehicle": 4483.007271455455,
        "s_m": 5.3,
        "r_o_m": 0.17904181066731867,
        "t_film_m": 0.00017635691379639515,
        "t_w_m": 0.0024055937321098286,
        "rt": 74.42728515520776,
        "A_m2": 0.002687999559510375,
        "I_m4": 4.2508242157405395e-05,
        "length_m": 5.364078446395507,
        "N_N": 2529712.20471835,
        "sigma_axial_Pa": 941113325.6209099,
        "k": 0.2,
        "gamma": 0.6244788527303019,
        "SF_local_gamma1": 3.512052558138803,
        "SF_least": 1.213027432264345,
        "eta": 0.060730328323553046,
        "Euler_stress_Pa": 2224012960.7120204,
        "mass_closure_kg": 4889.44215019,
        "radius_cap_fraction": 0.7161672426692747,
        "NASA_L_over_midradius": 30.162551690653768,
        "SF_yield": 4.144028029171653,
        "SF_euler": 2.3631723195978585,
        "SF_local": 2.1932025522350416,
        "SF_film": 1.213027432264345,
        "SF_perry": 2.2006559178731484,
        "SF_global": 2.1914113244664506,
        "governing": "film",
        "k04_governing": "film",
        "k04_SF_least": 1.213027432264345,
        "k04_SF_global": 4.382822648932901,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 941113325.6209099,
          "bending_Pa": 99081411.32129431,
          "maximum_compression_Pa": 1040194736.9422042,
          "opposite_signed_compression_Pa": 842031914.2996156,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 1.213027432264345,
          "mean_compression_Pa": 1141596280.8476908,
          "bending_Pa": 142449527.17600572,
          "maximum_compression_Pa": 1284045808.0236964,
          "opposite_signed_compression_Pa": 999146753.6716851,
          "maximum_tension_Pa": 0.0
        }
      },
      "reason": "024 t_total=2*t_direction; original scalar film formula silently gives both directions the entire thickness"
    },
    "FOLD/cfrp_zylon_019/equilateral": {
      "owner_film_SF": 1.4295868068960254,
      "owner_least_SF": 1.4182991741260802,
      "corrected_fixed": {
        "nodes": 47.455070604976875,
        "members": 136.36521181493063,
        "n_coef": 16.31014510460693,
        "m_nodes": 0.9491014120995375,
        "m_film": 217.17480701365733,
        "m_joint": 23.185496143546462,
        "m_tube": 3964.1753756204644,
        "m_end": 0.08501250368390467,
        "reserve": 583.9573700002318,
        "sag_kg": 172.65842592858436,
        "vehicle": 4305.484780189768,
        "s_m": 5.65,
        "r_o_m": 0.16559039920506322,
        "t_film_m": 0.00011078347452324353,
        "t_w_m": 0.0015810621643113317,
        "rt": 104.73364232151489,
        "A_m2": 0.001637139451095658,
        "I_m4": 2.2232043894906983e-05,
        "length_m": 5.727985371419447,
        "N_N": 1556980.118183072,
        "sigma_axial_Pa": 951036954.8183942,
        "k": 0.2,
        "gamma": 0.5742702826382843,
        "SF_local_gamma1": 2.4697415433203216,
        "SF_least": 0.7147934034480126,
        "eta": 0.06984628892908738,
        "Euler_stress_Pa": 1674840749.686752,
        "mass_closure_kg": 4889.44215019,
        "radius_cap_fraction": 0.6623615968202529,
        "NASA_L_over_midradius": 34.757220601338844,
        "SF_yield": 4.1007870201476315,
        "SF_euler": 1.7610680018281437,
        "SF_local": 1.4182991741260735,
        "SF_film": 0.7147934034480126,
        "SF_perry": 1.6760444294834402,
        "SF_global": 1.4209484282674745,
        "governing": "film",
        "k04_governing": "film",
        "k04_SF_least": 0.7147934034480126,
        "k04_SF_global": 2.841896856534949,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 951036954.8183942,
          "bending_Pa": 153706910.06826183,
          "maximum_compression_Pa": 1104743864.886656,
          "opposite_signed_compression_Pa": 797330044.7501323,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 0.7147934034480126,
          "mean_compression_Pa": 679794941.7394737,
          "bending_Pa": 79919307.01174545,
          "maximum_compression_Pa": 759714248.7512192,
          "opposite_signed_compression_Pa": 599875634.7277282,
          "maximum_tension_Pa": 0.0
        }
      },
      "reason": "024 t_total=2*t_direction; original scalar film formula silently gives both directions the entire thickness",
      "corrected_continuous": {
        "nodes": 40.165043311449395,
        "members": 114.49512993434818,
        "n_coef": 17.79984060785588,
        "m_nodes": 0.8033008662289879,
        "m_film": 444.3019432617129,
        "m_joint": 23.01891616392852,
        "m_tube": 3721.5907736424397,
        "m_end": 0.10052356015984099,
        "reserve": 599.7272162556892,
        "sag_kg": 188.42827218404187,
        "vehicle": 4289.7149339343105,
        "s_m": 6.166045659886814,
        "r_o_m": 0.16678871997429784,
        "t_film_m": 0.00022664375158793726,
        "t_w_m": 0.0016039348547493043,
        "rt": 103.98721586505269,
        "A_m2": 0.001672784600117238,
        "I_m4": 2.3044485711880663e-05,
        "length_m": 6.268157299911284,
        "N_N": 1699187.6991597854,
        "sigma_axial_Pa": 1015783920.4406215,
        "k": 0.2,
        "gamma": 0.5753567242383184,
        "SF_local_gamma1": 2.328915989858388,
        "SF_least": 1.339957474951163,
        "eta": 0.07588912817027198,
        "Euler_stress_Pa": 1418831518.8709335,
        "mass_closure_kg": 4889.442150189999,
        "radius_cap_fraction": 0.6671548798971914,
        "NASA_L_over_midradius": 37.76299737016256,
        "SF_yield": 3.839399228044758,
        "SF_euler": 1.3967847790458034,
        "SF_local": 1.339957474951163,
        "SF_film": 1.3399574751760193,
        "SF_perry": 1.3399574750386782,
        "SF_global": 1.3399574749548062,
        "governing": "local",
        "k04_governing": "local",
        "k04_SF_least": 1.339957474951163,
        "k04_SF_global": 2.6799149499096124,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 1015783920.4406215,
          "bending_Pa": 271365971.3624963,
          "maximum_compression_Pa": 1287149891.8031178,
          "opposite_signed_compression_Pa": 744417949.0781252,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 1.339957474951163,
          "mean_compression_Pa": 1361107257.1296082,
          "bending_Pa": 2538892738.705734,
          "maximum_compression_Pa": 3899999995.835342,
          "opposite_signed_compression_Pa": -1177785481.5761256,
          "maximum_tension_Pa": 1177785481.5761256
        },
        "search": {
          "method": "independent differential evolution plus bounded-accepted simplex",
          "seed": 492,
          "spacing_upper_m": 8.0,
          "outer_radius_upper_m": 0.25,
          "evaluations": 6383,
          "DE_success": true,
          "DE_message": "Optimization terminated successfully.",
          "certified_global_optimum": false
        }
      }
    },
    "FOLD/cfrp_zylon_019/two_way": {
      "owner_film_SF": 2.399708131652155,
      "owner_least_SF": 2.0653432400289193,
      "corrected_fixed": {
        "nodes": 47.592274337811055,
        "members": 91.18454867562211,
        "n_coef": 26.250000000000004,
        "m_nodes": 0.9518454867562212,
        "m_film": 338.7413323893825,
        "m_joint": 37.7751447613769,
        "m_tube": 3840.240062927727,
        "m_end": 0.20713566777501616,
        "reserve": 571.7337646247568,
        "sag_kg": 160.43482055310938,
        "vehicle": 4317.708385565243,
        "s_m": 5.25,
        "r_o_m": 0.1760378423688781,
        "t_film_m": 0.0001727960175618749,
        "t_w_m": 0.002327513291992343,
        "rt": 75.6334423414572,
        "A_m2": 0.0025573931355057163,
        "I_m4": 3.9105482283034105e-05,
        "length_m": 5.312242991404062,
        "N_N": 2505846.9952398753,
        "sigma_axial_Pa": 979844264.2430695,
        "k": 0.2,
        "gamma": 0.6221971998091569,
        "SF_local_gamma1": 3.3194351254914074,
        "SF_least": 1.1998540658260775,
        "eta": 0.061156668310068274,
        "Euler_stress_Pa": 2192642808.644208,
        "mass_closure_kg": 4889.44215019,
        "radius_cap_fraction": 0.7041513694755124,
        "NASA_L_over_midradius": 30.377531178760385,
        "SF_yield": 3.980224350257082,
        "SF_euler": 2.2377462303542965,
        "SF_local": 2.065343240028911,
        "SF_film": 1.1998540658260775,
        "SF_perry": 2.086900962115312,
        "SF_global": 2.0696974707780327,
        "governing": "film",
        "k04_governing": "film",
        "k04_SF_least": 1.1998540658260775,
        "k04_SF_global": 4.139394941556065,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 979844264.2430695,
          "bending_Pa": 108337820.53396083,
          "maximum_compression_Pa": 1088182084.7770305,
          "opposite_signed_compression_Pa": 871506443.7091087,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 1.1998540658260775,
          "mean_compression_Pa": 1175670124.3284085,
          "bending_Pa": 155020060.13745007,
          "maximum_compression_Pa": 1330690184.4658585,
          "opposite_signed_compression_Pa": 1020650064.1909584,
          "maximum_tension_Pa": 0.0
        }
      },
      "reason": "024 t_total=2*t_direction; original scalar film formula silently gives both directions the entire thickness"
    },
    "022c_cap/cfrp_zylon_5/equilateral": {
      "owner_film_SF": 1.493752313214508,
      "owner_least_SF": 1.485116372061561,
      "corrected_fixed": {
        "nodes": 49.9682476491694,
        "members": 143.9047429475082,
        "n_coef": 15.877132402714711,
        "m_nodes": 0.999364952983388,
        "m_film": 220.89798035984265,
        "m_joint": 23.111041059270214,
        "m_tube": 4126.986549277615,
        "m_end": 0.08029978924218076,
        "reserve": 417.44721454028877,
        "sag_kg": 172.9751070307888,
        "vehicle": 4471.994935649711,
        "s_m": 5.5,
        "r_o_m": 0.16612386920741104,
        "t_film_m": 0.00011268270991437619,
        "t_w_m": 0.0015983933238201595,
        "rt": 103.93178370538676,
        "A_m2": 0.0016603559256522984,
        "I_m4": 2.2691159673744065e-05,
        "length_m": 5.571794047833012,
        "N_N": 1515644.3628330787,
        "sigma_axial_Pa": 912843047.3349458,
        "k": 0.2,
        "gamma": 0.5754376615782716,
        "SF_local_gamma1": 2.5929289352631275,
        "SF_least": 0.746876156607254,
        "eta": 0.06772852185197308,
        "Euler_stress_Pa": 1781348889.5469458,
        "mass_closure_kg": 4889.44215019,
        "radius_cap_fraction": 0.6644954768296442,
        "NASA_L_over_midradius": 33.7021326704853,
        "SF_yield": 4.272366439538635,
        "SF_euler": 1.951429541746099,
        "SF_local": 1.4920689631464517,
        "SF_film": 0.746876156607254,
        "SF_perry": 1.8504480324015014,
        "SF_global": 1.4851163720615552,
        "governing": "film",
        "k04_governing": "film",
        "k04_SF_least": 0.746876156607254,
        "k04_SF_global": 2.9702327441231104,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 912843047.3349458,
          "bending_Pa": 126807211.5673961,
          "maximum_compression_Pa": 1039650258.9023418,
          "opposite_signed_compression_Pa": 786035835.7675498,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 0.746876156607254,
          "mean_compression_Pa": 681780706.779178,
          "bending_Pa": 74807153.1328516,
          "maximum_compression_Pa": 756587859.9120296,
          "opposite_signed_compression_Pa": 606973553.6463264,
          "maximum_tension_Pa": 0.0
        }
      },
      "reason": "024 t_total=2*t_direction; original scalar film formula silently gives both directions the entire thickness",
      "corrected_continuous": {
        "nodes": 39.63680405393392,
        "members": 112.91041216180176,
        "n_coef": 17.924317335228753,
        "m_nodes": 0.7927360810786784,
        "m_film": 470.46745996755305,
        "m_joint": 22.673167279707787,
        "m_tube": 3855.758298415758,
        "m_end": 0.10040335007907379,
        "reserve": 439.7504884459021,
        "sag_kg": 195.27838093640207,
        "vehicle": 4449.6916617440975,
        "s_m": 6.209165663120757,
        "r_o_m": 0.16933212351030613,
        "t_film_m": 0.00023999109556962966,
        "t_w_m": 0.0016479461379610915,
        "rt": 102.7534332643972,
        "A_m2": 0.0017447925294686625,
        "I_m4": 2.477228141247378e-05,
        "length_m": 6.313501998795773,
        "N_N": 1711070.35185558,
        "sigma_axial_Pa": 980672671.9403414,
        "k": 0.2,
        "gamma": 0.5771665996723738,
        "SF_local_gamma1": 2.4412636929685485,
        "SF_least": 1.409015864573666,
        "eta": 0.07529869770727635,
        "Euler_stress_Pa": 1441335785.2557578,
        "mass_closure_kg": 4889.44215019,
        "radius_cap_fraction": 0.6773284940412245,
        "NASA_L_over_midradius": 37.46704229000561,
        "SF_yield": 3.976862118818433,
        "SF_euler": 1.4697419704823187,
        "SF_local": 1.4090158645742792,
        "SF_film": 1.409015864573666,
        "SF_perry": 1.4090158653323206,
        "SF_global": 1.4090158645748212,
        "governing": "film",
        "k04_governing": "film",
        "k04_SF_least": 1.409015864573666,
        "k04_SF_global": 2.8180317291496424,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 980672671.9403414,
          "bending_Pa": 231043241.62734824,
          "maximum_compression_Pa": 1211715913.5676897,
          "opposite_signed_compression_Pa": 749629430.312993,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 1.409015864573666,
          "mean_compression_Pa": 1381783352.717787,
          "bending_Pa": 2518216613.722103,
          "maximum_compression_Pa": 3899999966.43989,
          "opposite_signed_compression_Pa": -1136433261.004316,
          "maximum_tension_Pa": 1136433261.004316
        },
        "search": {
          "method": "independent differential evolution plus bounded-accepted simplex",
          "seed": 492,
          "spacing_upper_m": 8.0,
          "outer_radius_upper_m": 0.25,
          "evaluations": 7224,
          "DE_success": true,
          "DE_message": "Optimization terminated successfully.",
          "certified_global_optimum": false
        }
      }
    },
    "022c_cap/cfrp_zylon_5/two_way": {
      "owner_film_SF": 2.42605486452869,
      "owner_least_SF": 2.187583984297688,
      "corrected_fixed": {
        "nodes": 46.73610044271688,
        "members": 89.47220088543376,
        "n_coef": 26.5,
        "m_nodes": 0.9347220088543376,
        "m_film": 345.72194891053465,
        "m_joint": 37.142503153640924,
        "m_tube": 3994.485765468709,
        "m_end": 0.20756448810955644,
        "reserve": 411.1572106482601,
        "sag_kg": 166.6851031387601,
        "vehicle": 4478.284939541739,
        "s_m": 5.3,
        "r_o_m": 0.1790362634273064,
        "t_film_m": 0.00017635691379639515,
        "t_w_m": 0.002402808609801301,
        "rt": 74.51124600477927,
        "A_m2": 0.002684824752036731,
        "I_m4": 4.2456047304020186e-05,
        "length_m": 5.364078446395507,
        "N_N": 2529712.20471835,
        "sigma_axial_Pa": 942226192.9011526,
        "k": 0.2,
        "gamma": 0.6243191076286436,
        "SF_local_gamma1": 3.5039516772228976,
        "SF_least": 1.213027432264345,
        "eta": 0.060731290597194273,
        "Euler_stress_Pa": 2223908816.3792014,
        "mass_closure_kg": 4889.44215019,
        "radius_cap_fraction": 0.7161450537092257,
        "NASA_L_over_midradius": 30.163256365296473,
        "SF_yield": 4.139133500409007,
        "SF_euler": 2.3602706368538704,
        "SF_local": 2.1875839842976887,
        "SF_film": 1.213027432264345,
        "SF_perry": 2.197965565683537,
        "SF_global": 2.1887717905818356,
        "governing": "film",
        "k04_governing": "film",
        "k04_SF_least": 1.213027432264345,
        "k04_SF_global": 4.377543581163671,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 942226192.9011526,
          "bending_Pa": 99289692.01420525,
          "maximum_compression_Pa": 1041515884.9153578,
          "opposite_signed_compression_Pa": 842936500.8869474,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 1.213027432264345,
          "mean_compression_Pa": 1142946219.3870947,
          "bending_Pa": 142805395.19457296,
          "maximum_compression_Pa": 1285751614.5816677,
          "opposite_signed_compression_Pa": 1000140824.1925218,
          "maximum_tension_Pa": 0.0
        }
      },
      "reason": "024 t_total=2*t_direction; original scalar film formula silently gives both directions the entire thickness"
    },
    "022c_cap/cfrp_zylon_019/equilateral": {
      "owner_film_SF": 1.4170465717478142,
      "owner_least_SF": 1.4170465717478142,
      "corrected_fixed": {
        "nodes": 46.66111084602568,
        "members": 133.98333253807704,
        "n_coef": 16.454482671904337,
        "m_nodes": 0.9332222169205135,
        "m_film": 217.17480701365733,
        "m_joint": 23.18138839899543,
        "m_tube": 3957.588677565962,
        "m_end": 0.08650847818107323,
        "reserve": 590.5640549944649,
        "sag_kg": 179.26511092281746,
        "vehicle": 4298.878095195535,
        "s_m": 5.7,
        "r_o_m": 0.16561974184185138,
        "t_film_m": 0.00011078347452324353,
        "t_w_m": 0.0015917715876949345,
        "rt": 104.04742936873721,
        "A_m2": 0.0016484686302205892,
        "I_m4": 2.239241621676394e-05,
        "length_m": 5.7801285634700275,
        "N_N": 1570758.7032997361,
        "sigma_axial_Pa": 952859323.1947311,
        "k": 0.2,
        "gamma": 0.5752688455983976,
        "SF_local_gamma1": 2.481275369906352,
        "SF_least": 0.7085232858739072,
        "eta": 0.07047406631078297,
        "Euler_stress_Pa": 1645238547.9153113,
        "mass_closure_kg": 4889.44215019,
        "radius_cap_fraction": 0.6624789673674055,
        "NASA_L_over_midradius": 35.068519218398826,
        "SF_yield": 4.092944157721146,
        "SF_euler": 1.7266332058327167,
        "SF_local": 1.4274004176577642,
        "SF_film": 0.7085232858739072,
        "SF_perry": 1.6448737338327788,
        "SF_global": 1.418437478967196,
        "governing": "film",
        "k04_governing": "film",
        "k04_SF_least": 0.7085232858739072,
        "k04_SF_global": 2.836874957934392,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 952859323.1947311,
          "bending_Pa": 159566958.39404404,
          "maximum_compression_Pa": 1112426281.5887752,
          "opposite_signed_compression_Pa": 793292364.8006871,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 0.7085232858739072,
          "mean_compression_Pa": 675123018.6455182,
          "bending_Pa": 80689619.26806466,
          "maximum_compression_Pa": 755812637.9135828,
          "opposite_signed_compression_Pa": 594433399.3774536,
          "maximum_tension_Pa": 0.0
        }
      },
      "reason": "024 t_total=2*t_direction; original scalar film formula silently gives both directions the entire thickness",
      "corrected_continuous": {
        "nodes": 40.18355433680384,
        "members": 114.55066301041151,
        "n_coef": 17.795525487773283,
        "m_nodes": 0.8036710867360768,
        "m_film": 443.4192052726559,
        "m_joint": 23.031028281937935,
        "m_tube": 3717.0140570159765,
        "m_end": 0.10052769524277937,
        "reserve": 605.1741885326936,
        "sag_kg": 193.87524446104626,
        "vehicle": 4284.267961657306,
        "s_m": 6.16455085844205,
        "r_o_m": 0.16670100506056326,
        "t_film_m": 0.0002261934563494327,
        "t_w_m": 0.0016024267676900245,
        "rt": 104.03034224201758,
        "A_m2": 0.0016703362256456963,
        "I_m4": 2.298665168933666e-05,
        "length_m": 6.266585975854464,
        "N_N": 1698775.7741810016,
        "sigma_axial_Pa": 1017026241.8420049,
        "k": 0.2,
        "gamma": 0.5752937791851684,
        "SF_local_gamma1": 2.325106878183589,
        "SF_least": 1.3376195229585999,
        "eta": 0.07590972281693956,
        "Euler_stress_Pa": 1418056099.6816506,
        "mass_closure_kg": 4889.442150190001,
        "radius_cap_fraction": 0.666804020242253,
        "NASA_L_over_midradius": 37.77332034307728,
        "SF_yield": 3.834709311862442,
        "SF_euler": 1.3943161359468104,
        "SF_local": 1.337619522959666,
        "SF_film": 1.3376195229585999,
        "SF_perry": 1.3376195249495448,
        "SF_global": 1.3376195229589798,
        "governing": "film",
        "k04_governing": "film",
        "k04_SF_least": 1.3376195229585999,
        "k04_SF_global": 2.6752390459179596,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 1017026241.8420049,
          "bending_Pa": 272989704.58623254,
          "maximum_compression_Pa": 1290015946.4282374,
          "opposite_signed_compression_Pa": 744036537.2557724,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 1.3376195229585999,
          "mean_compression_Pa": 1360394156.4490802,
          "bending_Pa": 2539605748.5658727,
          "maximum_compression_Pa": 3899999905.0149527,
          "opposite_signed_compression_Pa": -1179211592.1167924,
          "maximum_tension_Pa": 1179211592.1167924
        },
        "search": {
          "method": "independent differential evolution plus bounded-accepted simplex",
          "seed": 492,
          "spacing_upper_m": 8.0,
          "outer_radius_upper_m": 0.25,
          "evaluations": 6164,
          "DE_success": true,
          "DE_message": "Optimization terminated successfully.",
          "certified_global_optimum": false
        }
      }
    },
    "022c_cap/cfrp_zylon_019/two_way": {
      "owner_film_SF": 2.399708131652155,
      "owner_least_SF": 2.06156937327851,
      "corrected_fixed": {
        "nodes": 47.592274337811055,
        "members": 91.18454867562211,
        "n_coef": 26.250000000000004,
        "m_nodes": 0.9518454867562212,
        "m_film": 338.7413323893825,
        "m_joint": 37.87585956559199,
        "m_tube": 3835.461566510869,
        "m_end": 0.20768792583670467,
        "reserve": 576.4115462374002,
        "sag_kg": 165.1126021657529,
        "vehicle": 4313.030603952599,
        "s_m": 5.25,
        "r_o_m": 0.17556974429712546,
        "t_film_m": 0.0001727960175618749,
        "t_w_m": 0.002330878775600134,
        "rt": 75.32341284111669,
        "A_m2": 0.0025542109141512537,
        "I_m4": 3.884727452648398e-05,
        "length_m": 5.312242991404062,
        "N_N": 2505846.9952398753,
        "sigma_axial_Pa": 981065025.3495415,
        "k": 0.2,
        "gamma": 0.6227809801139298,
        "SF_local_gamma1": 3.328950398969369,
        "SF_least": 1.1998540658260775,
        "eta": 0.061323058954009864,
        "Euler_stress_Pa": 2180878826.383098,
        "mass_closure_kg": 4889.442150190001,
        "radius_cap_fraction": 0.7022789771885019,
        "NASA_L_over_midradius": 30.459357033451393,
        "SF_yield": 3.9752716682673275,
        "SF_euler": 2.2229707206268796,
        "SF_local": 2.0732069922208014,
        "SF_film": 1.1998540658260775,
        "SF_perry": 2.0742321006091258,
        "SF_global": 2.0615693732785014,
        "governing": "film",
        "k04_governing": "film",
        "k04_SF_least": 1.1998540658260775,
        "k04_SF_global": 4.123138746557003,
        "on_ro_cap_0_25": false,
        "full_pressure": {
          "pressure_multiplier": 1.0,
          "mean_compression_Pa": 981065025.3495415,
          "bending_Pa": 109355161.64548083,
          "maximum_compression_Pa": 1090420186.9950223,
          "opposite_signed_compression_Pa": 871709863.7040607,
          "maximum_tension_Pa": 0.0
        },
        "reported_limit": {
          "pressure_multiplier": 1.1998540658260775,
          "mean_compression_Pa": 1177134859.5054111,
          "bending_Pa": 156840644.99314505,
          "maximum_compression_Pa": 1333975504.4985561,
          "opposite_signed_compression_Pa": 1020294214.5122662,
          "maximum_tension_Pa": 0.0
        }
      },
      "reason": "024 t_total=2*t_direction; original scalar film formula silently gives both directions the entire thickness"
    }
  },
  "next": "Use total thickness with sigma_effective=sigma_fiber/2, or explicitly account for both ply masses; rerun every Zylon pairing.",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION"
}
```

### N568 — NFI-037-FILM-CTE

Source `rpt-ref-8c5de04c9c33dbcf7447`; original file `unpublished-local-ref:cbdfc7fec44de4cc; pointer `/rows/6`.

```json
{
  "id": "NFI-037-FILM-CTE",
  "tag": "PROJECTION",
  "finding": "The projection film has no stated modulus or expansion. The two assumptions are 10 GPa with 4.5e-6 and with 17e-6. Neither moves the out-of-band global factor below 1.",
  "next": "The film card names the modulus and the expansion."
}
```

### N589 — NFI-022D-FILM

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/0`.

```json
{
  "id": "NFI-022D-FILM",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "NFI-C022-ZYLON-DIRECTION"
  ],
  "finding": "The doubled directional mass is corrected in this model; a complete 0/90 Zylon membrane with a barrier, seams, biaxial/creep allowables and this gauge is still unsourced. The 1.5 GPa film is also PROJECTION.",
  "next": "Qualify a complete membrane and its full mass, durability and boundary load transfer."
}
```

### N662 — NFI-038-FILM_EXISTS

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/11`.

```json
{
  "id": "NFI-038-FILM_EXISTS",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "No complete qualified high-strength gas-tight laminate supplied",
  "evidence": "024, 030, 022d; filament data are not a complete membrane.",
  "resolution_needed": "Identify and weigh both plies, barrier, attachment, seams; test sustained biaxial response and transport.",
  "tests": [
    "T4"
  ]
}
```

### C004 — NFI-022D-CHECK-04

Source `rpt-ref-4b8e7b08241bb7a45536`; original file `unpublished-local-ref:2fa44902593248ea; pointer `/rows/3`.

```json
{
  "id": "NFI-022D-CHECK-04",
  "owner": "MAINLINE-022d / MAINLINE-024",
  "state": "open qualification",
  "kind": "complete membrane",
  "evidence": "SOURCE-ARITHMETIC.best_details.zylon; upstream/024 source PDFs",
  "note": "The corrected two-ply charge is arithmetically sound: 214.541557545304 kg total, with 54.720111189054 micrometres per direction. The 0.6 filament knockdown, off-axis/biaxial response, continuous gauge, seams, attachments, coating/barrier mass, creep and environmental retention do not yet describe a qualified gas membrane. Cap/sag/lift and loaded surface-area approximations remain conditional.",
  "settle": "Provide a complete membrane layup and pressure-loaded cell model with measured retention, permeability and full installed mass.",
  "stops_other_work": false
}
```

### C156 — NFI-041-04

Source `rpt-ref-c7dfc45babe1b96007db`; original file `unpublished-local-ref:cd543374666d8c21; pointer `/items/3`.

```json
{
  "id": "NFI-041-04",
  "status": "open",
  "topic": "Complete membrane constitution and coupling",
  "evidence": [
    "film/rigid/RESULTS.json",
    "film/pinned/RESULTS.json",
    "intake/film/zylon-hp-fiber-data.pdf",
    "film.py"
  ],
  "finding": "A 270 GPa filament-derived axial tangent changes perfect linear multipliers, but the assumed taut, perfectly attached 0/90 skin has no qualified shear modulus, Poisson coupling, prestress, wrinkling, sagged equilibrium or free interior kinematics. The projected tangent can overstate restraint. No film-stiffness credit is used in primary resizing.",
  "needed": "An actual gas-tight laminate, biaxial and shear constitutive data, tension-only/wrinkling treatment, pressure-equilibrated geometry, seams and attachments, plus tear, creep, fatigue and permeability evidence.",
  "prohibited_inference": "Neither the fiber modulus nor the conditional pinned-film result proves a stable pressure vessel."
}
```

## R066 — film barrier: permeation data and coatings

**030b source history:** 034 adds a projected 57.546 kg barrier/attachment/seam bill to its older Zylon geometry. It is not a proven minimum and must be recomputed for the 022d assembly.

**Original question:** Alumina barrier numbers are coupon measurements; coating a 1257 m2 hull was not opened. PROJECTION at hull scale.

### N092 — NFI-MYLAR-PRESSURE

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-MYLAR-PRESSURE",
  "state": "assumption",
  "note": "The oxygen column does not print the test pressure. The scale uses 1 atm of oxygen."
}
```

### N093 — NFI-N2-MISSING

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-N2-MISSING",
  "state": "not opened",
  "note": "N2 is opened for Kapton only. PEN, Mylar and the ALD paper do not give N2."
}
```

### N095 — NFI-ALD-SCALE

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-ALD-SCALE",
  "state": "in the lab",
  "note": "The alumina numbers are coupon measurements. A 1257 m2 hull coating was not opened. Tagged PROJECTION at hull scale."
}
```

### N417 — NFI-CHK024-GAS-COVERAGE

Source `rpt-ref-7d6892c4e55be16ad523`; original file `unpublished-local-ref:0d655e2d18e3e532; pointer `/open/6`.

```json
{
  "id": "NFI-CHK024-GAS-COVERAGE",
  "kind": "incomplete service gas balance",
  "tag": "QUESTIONABLE",
  "finding": "N2 is available only for Kapton. Water retains source conditions, with no hull RH. Seams, defects, outgassing, thickness scaling and stressed/coated permeability are unqualified. Kapton source-condition sum is below the inherited allowance; it is not a complete service leak test.",
  "proposed_next": "Keep source and service rates distinct and close all gas paths before selecting the vacuum system."
}
```

### N418 — NFI-CHK024-ALD-AND-UNSOURCED

Source `rpt-ref-7d6892c4e55be16ad523`; original file `unpublished-local-ref:0d655e2d18e3e532; pointer `/open/7`.

```json
{
  "id": "NFI-CHK024-ALD-AND-UNSOURCED",
  "kind": "scale/form uncertainty",
  "tag": "PROJECTION",
  "finding": "ALD bound is a supported lab coupon, not a bare film, fibre coating or hull-scale result; substrate and fabrication mass remain necessary. CNT/graphene production allowables remain uncomputed.",
  "proposed_next": "Retain coupon bounds and absent allowables; do not use them to close hull mass."
}
```

### N580 — NFI-034-BARRIER-ASSEMBLY

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/8`.

```json
{
  "id": "NFI-034-BARRIER-ASSEMBLY",
  "tag": "PROJECTION",
  "finding": "The Zylon row needs a separate barrier. A 12 um PET substrate, assumed 50 nm Al, 25 g/m2 attachment/lamination and 5 kg seam installation total 57.546 kg. This is a worked bill, not a qualified lightest laminate or weather/UV protection system.",
  "proposed_next": "Test a complete load-bearing and gas-tight assembly; measure seam, resin, protective layer and processing mass."
}
```

### N581 — NFI-034-GAS-COVERAGE

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/9`.

```json
{
  "id": "NFI-034-GAS-COVERAGE",
  "tag": "PROJECTION",
  "finding": "Kapton has sourced CO2/O2/H2/N2/He data but not Ar; Ar is set to N2. Mylar has sourced O2 only: other gas ratios are assumed, including N2, and checked in a sensitivity. Outgassing is water-equivalent with a 5 mass% H2 sensitivity, not measured composition.",
  "proposed_next": "Measure a full gas spectrum, including noble gases and organics; distinguish pressure from gas mass."
}
```

### C069 — NFI-034-BARRIER-ASSEMBLY

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/8`.

```json
{
  "id": "NFI-034-BARRIER-ASSEMBLY",
  "tag": "PROJECTION",
  "finding": "The Zylon row needs a separate barrier. A 12 um PET substrate, assumed 50 nm Al, 25 g/m2 attachment/lamination and 5 kg seam installation total 57.546 kg. This is a worked bill, not a qualified lightest laminate or weather/UV protection system.",
  "proposed_next": "Test a complete load-bearing and gas-tight assembly; measure seam, resin, protective layer and processing mass.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C080 — NFI-CHECK034-AREA-SENSITIVITY-SCOPE

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/19`.

```json
{
  "id": "NFI-CHECK034-AREA-SENSITIVITY-SCOPE",
  "tag": "PROJECTION",
  "finding": "The +10% area case multiplies film transmission only, leaving film mass, area-dependent outgassing inventory and barrier/attachment mass unchanged. It is a rate sensitivity at fixed inherited geometry, not a complete larger-area assembly. At fixed gauges, 10% more Kapton adds 98.12569224663257 kg; 10% more Zylon adds 21.717480701365734 kg structural fiber and 5.254627872394289 kg barrier/attachment. The Zylon vacuum/barrier/joint-bond subtotal becomes 96.87893676870814–116.87893676870814 kg, leaving only 3.1210632312918616 kg of the 100 kg line at the low bill. These illustrations are not a structural reoptimization.",
  "numerical_detail": "AREA-SENSITIVITY-CHECK.json",
  "proposed_next": "Label the existing case permeation-only, or consistently propagate actual manufactured area through film, barrier, attachment and release inventories before taking mass or endurance credit."
}
```

## R067 — film pillow radius assumption

**030b source history:** 022c charges cap sag; 022d derives equilateral constant-tension mean s²/(40rho), 1.166003× the selected cap mean. Loaded nonlinear shape, edge motion and additional area remain open.

**Original question:** Pillow radius set to the bay side 2.04 m because that is the earlier film formula, not a measured cap.

### N083 — NFI-CURVATURE

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-CURVATURE",
  "state": "assumption",
  "note": "Pillow radius is set to the bay side, 2.04 m, because that is the 011b film formula. It is not a measured cap."
}
```

### N411 — NFI-CHK024-SAG-NOT-CHARGED

Source `rpt-ref-7d6892c4e55be16ad523`; original file `unpublished-local-ref:0d655e2d18e3e532; pointer `/open/0`.

```json
{
  "id": "NFI-CHK024-SAG-NOT-CHARGED",
  "kind": "missing physical accounting",
  "tag": "QUESTIONABLE",
  "finding": "The original filed card gives cap rise 0.374346974907 m but keeps full-sphere lift. All three closures spend the original 4889.44215019 kg. No sag-volume integral or lift deduction appears.",
  "proposed_next": "Integrate a boundary-compatible inward pillow, reduce displaced volume/lift, then re-run the mass-constrained scan in the separately assigned amendment. Cap rise alone does not uniquely determine volume.",
  "charged_volume_loss_m3": 0,
  "charged_lift_loss_kg": 0,
  "air_density_kg_m3": 1.1672683307469056,
  "linear_lift_loss_kg_per_mean_radial_mm": 1.4668326450569997
}
```

### N414 — NFI-CHK024-PILLOW-AREA-BOUNDARY

Source `rpt-ref-7d6892c4e55be16ad523`; original file `unpublished-local-ref:0d655e2d18e3e532; pointer `/open/3`.

```json
{
  "id": "NFI-CHK024-PILLOW-AREA-BOUNDARY",
  "kind": "geometric model substitution",
  "tag": "QUESTIONABLE",
  "finding": "Curvature equals bay side to preserve the 011b film equation. Circumscribed circular-cap rise does not establish compatibility with all three actual edge arcs. Film masses and gas rates use 4*pi*R^2 without pillow-area correction. Triangular tributary and scored arc line loads differ; the stated 011b load path is retained.",
  "proposed_next": "Specify boundary, shape, true area and load transfer consistently with the sag amendment."
}
```

### N456 — NFI-CHECK-025-SAG-UNCHARGED

Source `rpt-ref-a8b77f7de2ffc56af7b4`; original file `unpublished-local-ref:d2a2bac9ac804106; pointer `/rows/2`.

```json
{
  "id": "NFI-CHECK-025-SAG-UNCHARGED",
  "status": "scope",
  "note": "Zero-spare optima do not deduct the sag lift loss already filed on MAINLINE-024: 64.1580396987 kg at s 2.04 m and 94.3500583804 kg at s 3 m. 025 assigns that charge elsewhere. This is not a numerical mismatch."
}
```

### N464 — NFI-C022-SAG-GEOMETRY

Source `rpt-ref-f6de390e1555b4ca8e78`; original file `unpublished-local-ref:a3c00555c78ad754; pointer `/rows/7`.

```json
{
  "id": "NFI-C022-SAG-GEOMETRY",
  "kind": "OPEN geometry transfer",
  "issue": "022c correctly charges the selected circular-cap approximation; an exact triangular membrane is not integrated, and the same triangular cap law is used for two-way cells.",
  "evidence": {
    "lift_2_m_kg": 62.90003892028683,
    "lift_4_m_kg": 125.80007784057366,
    "lift_2_04_m_kg": 64.15803969869256,
    "crown_2_04_m": 0.08684870017707028,
    "old_charge_2_m_kg": 61.118026877374994,
    "membrane_over_cap_mean": 1.1660029709329083
  },
  "next": "Specify and solve the actual cell boundary-value problem, and use its volume/area changes for each grid. Keep the1.166 sensitivity ratio distinguished from the order's approximate1.19.",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION"
}
```

### N494 — NFI-031-P3-SAG

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/12`.

```json
{
  "id": "NFI-031-P3-SAG",
  "tag": "PROJECTION",
  "issue": "022b's s/(16R) displacement loss is applied as reduced volume at every altitude. Film shape may change with pressure, and the spherical arc/member model is approximate for 6m bays on R10m.",
  "next_evidence": "Solve coupled membrane shape, true enclosed volume, pressure and frame load path; verify the global continuum approximation and spacing bounds."
}
```

### N507 — NFI-026-09

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/8`.

```json
{
  "id": "NFI-026-09",
  "tag": "PROJECTION",
  "status": "open",
  "owner": "sciences",
  "issue": "Pressure fan omits film stiffness and solved membrane shape",
  "evidence": "Conservative pV line loads include follower stiffness; no film constitutive stiffness, wrinkling or prestress is present.",
  "implication": "Quantify membrane and connection restraint. Especially consequential for pinned member roll and actual enclosed volume."
}
```

### N582 — NFI-034-GEOMETRY

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/10`.

```json
{
  "id": "NFI-034-GEOMETRY",
  "tag": "QUESTIONABLE",
  "finding": "Uses 021b face/core geometry and re-sizes 028 scarfs to its panel width. Uses 022c cap sag for volume and the original sphere area for films; a 10% area sensitivity is supplied. A sphere cutting pattern and exact pillow area are absent. P3 internal solid volume is neglected in the pressure model.",
  "proposed_next": "Carry an actual surface-area, solid-volume, seam-length and node inventory with the manufactured layout."
}
```

### N594 — NFI-022D-SAG

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/5`.

```json
{
  "id": "NFI-022D-SAG",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "NFI-C022-SAG-GEOMETRY"
  ],
  "finding": "The exact equilateral mean is now derived for the linear constant-tension membrane. Cap is a circular surrogate; nonlinear shape, extra membrane area and loaded edge movement remain open. Primary two-way rows intentionally preserve 022c's geometry; square-cell alternatives are separate.",
  "next": "Close actual cell shape, tension distribution, loaded volume and film area consistently for each lattice."
}
```

### N619 — NFI-026B-05

Source `rpt-ref-8befdd4c89803adc44a8`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/4`.

```json
{
  "id": "NFI-026B-05",
  "tag": "PROJECTION",
  "status": "open",
  "owner": "sciences",
  "issue": "Film shape, sag and material stiffness unresolved",
  "evidence": "Fan load-transfer surface has no membrane material stiffness or solved equilibrium sag. Frequency4 omits sag charge; frequency 2 carries022b debit187.937933 kg.",
  "implication": "Remaining payload301.391/301.814 kg is conditional; do not interpret uncharged sag as physically zero or substitute fan volume for actual lift."
}
```

### N645 — NFI-026B-05

Source `rpt-ref-4a20323946ecafd56a6b`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/4`.

```json
{
  "id": "NFI-026B-05",
  "tag": "PROJECTION",
  "status": "open",
  "owner": "sciences",
  "issue": "Film shape, sag and material stiffness unresolved",
  "evidence": "Fan load-transfer surface has no membrane material stiffness or solved equilibrium sag. Frequency4 omits sag charge; frequency 2 carries022b debit187.937933 kg.",
  "implication": "Remaining payload301.391/301.814 kg is conditional; do not interpret uncharged sag as physically zero or substitute fan volume for actual lift."
}
```

### C085 — NFI-C026B-SAG

Source `rpt-ref-b92330879d6ba35bd62c`; original file `unpublished-local-ref:21616ac9b36e6057; pointer `/rows/4`.

```json
{
  "id": "NFI-C026B-SAG",
  "issue": "Payloads retain source sag and film assumptions, not solved film geometry.",
  "evidence": "f4 sag debit is uncharged; f2 carries 187.937932648 kg; fan volume is not actual lift volume.",
  "next_evidence": "A compatible membrane equilibrium and displaced-volume calculation using actual bays and admissible film properties.",
  "tag": "QUESTIONABLE",
  "status": "open",
  "blocks_card": false
}
```

## R068 — P3 film allowable and design stress (1.5 GPa carried, no datasheet; Kapton, Teonex, Mylar today)

**030b source history:** 022d screened equilateral Zylon/CFRP gives 1.258252 cap and 1.251857 membrane on the 5% reserve, 1.194121/1.187858 on 019. Mylar and Kapton remain below one. The new film capacity is a corrected projection, not a material demonstration.

**Original question:** Film allowable is an owner assumption with no datasheet; wrinkling, puncture, sag area and shear transfer are unmodelled, and it binds for SiC and CNT rows.

### N024 — NFI-CHK011B-FILM

Source `rpt-check011b-opus-1020`; original file `unpublished-local-ref:252e7a0b939c4177; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK011B-FILM",
  "state": "observed",
  "direction": "critical path",
  "note": "The film co-binds in most restated rows (SF 2.514/s). Its 1.5 GPa allowable has no datasheet (I-SIG), so it sits on the critical path of every SiC row at SF 1 or above."
}
```

### N082 — NFI-FILM-ALLOWABLE-011B

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-FILM-ALLOWABLE-011B",
  "state": "unsourced",
  "note": "1.5 GPa and 80 um at 970 kg/m3 are the 011b pin. They are not a candidate allowable."
}
```

### N084 — NFI-KNOCK-HALF

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-KNOCK-HALF",
  "state": "assumption",
  "note": "Where no creep-rupture fraction was opened, the design stress is half the opened ultimate. Kapton, Teonex and Vectran use it."
}
```

### N089 — NFI-PEN-THICKNESS

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-PEN-THICKNESS",
  "state": "exists today",
  "note": "The design thickness is above the 250 um row. The 210 MPa ultimate is the thickest opened gauge, not a measurement at the design thickness."
}
```

### N090 — NFI-PEN-NOT-DESIGN-DATA

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-PEN-NOT-DESIGN-DATA",
  "state": "exists today",
  "note": "The IEC Teonex sheet says its typical values are not design data."
}
```

### N091 — NFI-MYLAR-STRENGTH

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-MYLAR-STRENGTH",
  "state": "not opened",
  "note": "The barrier brochure has no PET strength, modulus, density or creep. The 12 um mass is not computed."
}
```

### N126 — NFI-005-FILM

Source `rpt-ref-eb07faa637b7487d6dc5`; original file `unpublished-local-ref:2ef2c84bad6b0b03; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-005-FILM",
  "gap": "Film allowable 1.5 GPa is inherited from MAINLINE-001 with no pinned datasheet (inherited NFI-FILM). The film passes at SF 2.51 on that value.",
  "direction": "Pin one film datasheet; required allowable 5.966e8 Pa is the bar it must clear.",
  "effect": "A real film below 5.966e8 Pa allowable would govern P3 and P3-A."
}
```

### N152 — NFI-011-FILM

Source `rpt-ref-f21d4bd21d2026511818`; original file `unpublished-local-ref:b5c9a6937c19e542; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-011-FILM",
  "gap": "The film allowable 1.5e9 Pa is an owner assumption with no datasheet, and wrinkling, puncture, sag area and shear transfer to members are unmodelled. For aluminum the film never binds (>=0.838 at the best point), but for SiC and the CNT projection it is the second limit and binds from s=1.0.",
  "direction": "Pin a real film (material, thickness, seaming) before crediting any SiC-family margin.",
  "effect": "SiC-family rows are film-capped in reality until the film is real."
}
```

### N248 — NFI-FILM

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-FILM",
  "linked_inputs_or_points": "P3 film",
  "questionable_assumption_or_gap": "Allowable, density and thickness are not one published film. Pocket radius set equal to spacing.",
  "direction_of_further_investigation": "Pin one film datasheet and a local pocket test.",
  "how_it_affects_margin_or_SF": "Film pressure scales with allowable and thickness. Film mass scales with density and thickness."
}
```

### N258 — NFI-FILM

Source `rpt-mainline002-grok-strength-card-1019`; original file `unpublished-local-ref:f02996967e2f160d; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-FILM",
  "gap": "Film allowable stays the owner value from MAINLINE-001 and is not aluminum yield.",
  "direction": "Pin one film datasheet.",
  "effect": "Film pressure is reported separately and can govern if it is the least."
}
```

### N314 — NFI-011B-LOCAL-FILM

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-LOCAL-FILM",
  "note": "Local buckling remains 0.6*E*t_w/r_o with gamma=1. The film allowable remains 1.5 GPa with no datasheet. Both are open, carried from 011."
}
```

### N359 — NFI-022-FILM

Source `rpt-mainline022-grok-p3-optimistic-floating-point-1020`; original file `unpublished-local-ref:62f20cec268319e4; pointer `retained original identity`.

```json
{
  "id": "NFI-022-FILM",
  "today": "Mylar 850H, tensile MD 22 kpsi, density 1.40 g/cc, O2 transmission 6.0 cc/100 in2/day at 48 gauge and 1 atm.",
  "scored_thickness_m": 4.793113556654862e-05,
  "scored_sigma_Pa": 151684660.449916,
  "permeation_kg_per_day": 0.03619834160684392,
  "permeation_pct_of_1pct_budget": 0.07403368420145287,
  "method": "MAINLINE-016: 1 percent of lift per day is 48.894 kg, and permeance is converted as scc to mol to kg at p_ext. Mylar transmission is scaled as 1/thickness from the 48-gauge line.",
  "projection": "The 011 film, 1.5 GPa at 970 kg/m3, has no datasheet. It is the film optimism.",
  "source": "https://polymerfilms.com/wp-content/uploads/2023/09/Mylar850H-Datasheets.pdf",
  "state": "PENDING-024. This card carries the 011b film: 1.5 GPa, 970 kg/m3. Mylar exists and is the sourced-today comparison. The 1.5 GPa film is a PROJECTION. MAINLINE-024 owns the film, its thickness and the vacuum permeation. Seams are not in the Mylar figure."
}
```

### N383 — NFI-025-FILM-MARGIN

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/15`.

```json
{
  "id": "NFI-025-FILM-MARGIN",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "PROJECTION",
  "issue": "Optimistic reoptimized SiC point is also limited by inherited film strength and has zero spare float mass.",
  "factor": {
    "inherited_film_strength_Pa": 1500000000.0,
    "film_thickness_m": 8e-05,
    "film_mass_kg": 97.515,
    "systems_mass_kg": 50,
    "payload_or_spare_mass_kg_at_all_mass_limited_optima": 0,
    "estimated_film_sag_lift_loss_at_spacing_2p04m_fraction": 0.013,
    "estimated_film_sag_lift_loss_at_spacing_2p04m_kg": 64,
    "estimated_film_sag_lift_loss_at_spacing_3m_fraction": 0.019,
    "estimated_film_sag_lift_loss_at_spacing_3m_kg": 94,
    "sag_loss_source": "Pinned NOTE-P3-EQUILIBRIUM.md; approximate values",
    "sag_loss_included_in_this_fixed_budget": false
  },
  "required_next_evidence": "Source-qualified membrane film strength, seams/creep/damage allowances, pressure-transfer span, gas tightness and an actual systems/payload mass budget.",
  "note": "A surrogate SF above1 at exactly the float mass is not demonstrated practical levitation margin. MAINLINE-024/022b owns the film-sag/lift correction. This card preserves the inherited budget for reproducible comparison; zero spare mass cannot absorb the cited loss without changing tube mass and demands."
}
```

### N415 — NFI-CHK024-ALLOWABLES-AND-GAUGE

Source `rpt-ref-7d6892c4e55be16ad523`; original file `unpublished-local-ref:0d655e2d18e3e532; pointer `/open/4`.

```json
{
  "id": "NFI-CHK024-ALLOWABLES-AND-GAUGE",
  "kind": "material design qualification gap",
  "tag": "QUESTIONABLE",
  "finding": "Half-ultimate Kapton/PEN/Vectran values are assumptions, not creep-rupture allowables. Kapton design gauge 843 um exceeds opened 12.7-125 um rows; PEN 927 um exceeds the 250 um strength row and transfers 25 um modulus/permeability. Kapton 115.5 MPa exceeds its 69 MPa stress at 3% yield and 90 MPa at 5% strain. Long-term shape is unqualified.",
  "proposed_next": "Retain gauge and sustained-load transfer assumptions; qualify the fabricated membrane and joints."
}
```

### N492 — NFI-031-P3-MATERIAL-FILM

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/10`.

```json
{
  "id": "NFI-031-P3-MATERIAL-FILM",
  "tag": "PROJECTION",
  "issue": "The passing P3 keeps a 3900MPa SiC tube compression value, 410GPa modulus, 1.5GPa/970kg/m3 film and metre-scale thin curved tubes. These are not a demonstrated assembly or a safe tensile/bending allowable.",
  "next_evidence": "Carry tube-scale brittle reliability, post-form flaw statistics, film biaxial/creep/UV/seam/barrier properties and manufacture into the model."
}
```

### N569 — NFI-037-P3-BASELINE

Source `rpt-ref-8c5de04c9c33dbcf7447`; original file `unpublished-local-ref:cbdfc7fec44de4cc; pointer `/rows/7`.

```json
{
  "id": "NFI-037-P3-BASELINE",
  "tag": "QUESTIONABLE",
  "finding": "In-band Mylar stays at 0.4105 by Perry and titanium/Kapton at 0.7412 by global after the flight gust. A proportional tube-wall increase is 5863 kg and 1634 kg. The lift does not have that margin. Sun and wind are not the gap.",
  "next": "None on this card. The baseline section is a different job."
}
```

### N571 — NFI-CHECK-031-PASS-CONDITIONS

Source `rpt-ref-be337d7d2ce1259d0aff`; original file `unpublished-local-ref:d18fb2f2dcd28de0; pointer `/rows/1`.

```json
{
  "id": "NFI-CHECK-031-PASS-CONDITIONS",
  "status": "open",
  "issue": "The P3 pass uses 3900 MPa, a typical property, and a 1.5 GPa film. The lapse with constant vapour fraction is a projection. The C=0 roots at -23.190 m and -1015.877 m are below sea-level ground.",
  "effect": "The card already tags these. They stay open."
}
```

### N610 — NFI-017b-FILM-RULE

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/10`.

```json
{
  "id": "NFI-017b-FILM-RULE",
  "tag": "QUESTIONABLE",
  "claim": "024's half-of-tensile design rule is carried to every film in the trend (Upilex-S comparison); barrier, creep and seaming are not scored. The 1975 Kapton H row prints no density; Kapton HN's 1420 is used.",
  "needed_to_ground": "Film design allowables with barrier and creep for Upilex-S class films."
}
```

## R069 — 015 tolerance map conventions (lambda, nu) and inversion range; Lee 2016 envelope (015b)

**Current 030c:** 029 changes the evidence state of the tolerance map: named 015 amplitudes do not support operating pressure in the weak-meridian model. No new validated amplitude limit is inferred.

**030b source history:** 015b/CHECK-015b repair the lambda/nu width mismatch: old/live RMS 2.6112627. Actual-gamma 021/021b RMS .139344/.654416 mm. The SF1 threshold .518304077 is unchanged. Rounding and wide-wave area qualifications remain.

**Original question:** Amplitudes at kd 0.5, 0.7 and 0.9 are lambda_I = 1 values; worst-width amplitudes are smaller, so the inverted table is optimistic in width.

### N172 — NFI-015-KD03-AMPLITUDE

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-KD03-AMPLITUDE",
  "issue": "Eq 3 floors at 0.45, so kd 0.3 has no lambda_I = 1 amplitude. The worst-width curve is pinned only at its plateau 0.2338 and by the one-thickness statement, kd about 0.20-0.25 at delta equal to t. kd 0.3 sits on the unretrieved rising branch between those pins. No pair is interpolated. The aluminium-honeycomb beryllium point has R/t_eq 136.7, inside the fit range 100-1550, so the missing amplitude is the floor, not the range. P2-E at R/t_eq 50.75 remains outside that range.",
  "consequence": "The kd 0.3 row is a ceiling: below 197.052 mm on P2-E, below 73.17 mm on the 014b beryllium point, below 39.05 mm on 014 beryllium with HRH-10. The true allowance is smaller, and the gap factor against manufacture is not known.",
  "next": "Digitise the worst-width envelope (Lee et al. 2016, or a recomputation) at delta/t below 1."
}
```

### N173 — NFI-015-BE-WRINKLING

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-BE-WRINKLING",
  "issue": "The 014b beryllium point on CR-III 5056 at 1.6 pcf has least SF 0.668649769508548 by global buckling at kd 0.20. Face wrinkling on that same split is 0.6688 and does not contain kd. Raising kd to 0.2991 brings only the global mode to SF 1. The least factor stays 0.6688. Re-optimising the mass split on the same core and the same structural mass reaches least SF 0.8536 at kd 0.3 and crosses 1 at kd 0.519 by face yield.",
  "consequence": "A shape tolerance bought at kd 0.3 does not put this point's least factor at 1. The global-only scaling is the order's 0.299, and it is not the least factor.",
  "next": "If a later card chases SF 1 on this core, use the re-optimised split and kd 0.519, not the frozen split at kd 0.3."
}
```

### N174 — NFI-015-GAP-DIRECTION

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-GAP-DIRECTION",
  "issue": "The gap factor is required tolerance divided by the achieved figure. Above 1, manufacture is already inside the allowance. The partial's sentence that kd 0.9 needs 1.8 times better than the GBT assembled surface reads the P2-E factor 1.82 the other way. On P2-E the 0.46 mm RMS allowance is looser than 0.25 mm. On the aluminium beryllium point the 0.10 mm RMS allowance is tighter than 0.25 mm and looser than 0.05 mm.",
  "consequence": "The shell that the kd 0.3 question is about is not free at kd 0.9 on a single-dimple RMS basis, even though P2-E is.",
  "next": "None. The arithmetic is in RESULTS.json."
}
```

### N175 — NFI-015-PRESSURE-RATIO

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-PRESSURE-RATIO",
  "issue": "The partial's prose says the gyration thickness and the bending thickness give classical pressures 3.42 times apart. On P2-E, Zoelly's pressure at t_eq divided by the COMMON sandwich pressure is 293.1. The 3.42 figure is not that ratio.",
  "consequence": "Safety factors stay on the sandwich pressure. t_eq is used only to scale the dimple.",
  "next": "None."
}
```

### N176 — NFI-015-WORST-WIDTH-RISING-BRANCH

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-WORST-WIDTH-RISING-BRANCH",
  "issue": "The kd-versus-amplitude relation is closed-form only at width lambda_I = 1. The worst-width curve is pinned at its plateau 0.2338 and by the one-thickness statement. Amplitudes at kd 0.5, 0.7 and 0.9 are lambda_I = 1 values. Worst-width amplitudes at those levels are smaller.",
  "consequence": "The inverted table is optimistic in width. The kd 0.2 row is the conservative anchor.",
  "next": "Retrieve the min-over-width envelope."
}
```

### N178 — NFI-015-FIT-RANGE-FLOOR

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-FIT-RANGE-FLOOR",
  "issue": "Eq 3 was fit over R/t 100-1550 and nu near 0.5. P2-E sits at R/t_eq 50.75 with nu 0.33. The aluminium beryllium point sits at 136.7 and is inside the R/t window. The Poisson mismatch remains on both.",
  "consequence": "P2-E amplitudes carry an unquantified range-floor error. The aluminium point does not carry that particular error.",
  "next": "A fit at R/t near 50 if P2-E stays the reference shell."
}
```

### N179 — NFI-015-HT-EQ32-UNRESOLVED

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-HT-EQ32-UNRESOLVED",
  "issue": "Hutchinson and Thompson 2018 Eq 3.2, the lower envelope over dimple width, was not resolved from the primary. It is not used. The rising branch is Baizhikova 2026 Eq 3, which meets Jimenez at the shared plateau (0.4470 against 0.45).",
  "consequence": "No number in this card comes from that unresolved print.",
  "next": "Resolve the print against the primary when it can be read."
}
```

### N183 — NFI-015-PNAS-EXTRAPOLATION

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-PNAS-EXTRAPOLATION",
  "issue": "The PNAS 2024 random-field design values are evaluated at R/t_eq 50.75 by scaling N with sqrt(R/t). Their fits span R/t 100-400. The reproduced anchors are 0.278 and 0.320 at R/t 100.",
  "consequence": "The P2-E readings are a cross-check, not a design number.",
  "next": "Recompute the chain at R/t 50 if that route is carried."
}
```

### N384 — NFI-015B-WIDTH-NU

Source `rpt-ref-74e882831c201b1a953c`; original file `unpublished-local-ref:71470bf7da8d8fcd; pointer `/rows/0`.

```json
{
  "id": "NFI-015B-WIDTH-NU",
  "issue": "The filed 015 prominent RMS paired a lambda_I = 1 amplitude with a lambda_I = 2.625 width, and the widths used nu 0.30 while COMMON and the 015 inputs declare 0.33. The live map carries nu 0.33 only and matches width to amplitude at lambda_I = 1. The filed column is 2.611 times the live single-dimple RMS.",
  "consequence": "The manufacturing conclusion that used the prominent RMS is replaced by the matched column. The retired mix is kept only as an audit.",
  "next": "None. The arithmetic is in RESULTS.json."
}
```

### N385 — NFI-015B-EQ3-REGIME

Source `rpt-ref-74e882831c201b1a953c`; original file `unpublished-local-ref:71470bf7da8d8fcd; pointer `/rows/1`.

```json
{
  "id": "NFI-015B-EQ3-REGIME",
  "issue": "Baizhikova 2026 Eq. 3 is a lambda_I = 1 fit over R/t 100 to 1550 at nu 0.5, and the paper excludes delta/t below about 0.07. The kd 0.9 inverse is delta/t 0.0323. P2-E is at R/t 50.75. The 015 beryllium point is at 136.67, the 021 point at 274.19, and the 021b point at 187.39.",
  "consequence": "Every kd 0.9 row is outside the small-amplitude regime. The P2-E rows are also outside the radius window. The other three shells are inside that window and still carry the source's nu 0.5.",
  "next": "A fit at nu 0.33 and at R/t near 50 if P2-E stays the reference shell."
}
```

### N386 — NFI-015B-LEE-RANGE

Source `rpt-ref-74e882831c201b1a953c`; original file `unpublished-local-ref:71470bf7da8d8fcd; pointer `/rows/2`.

```json
{
  "id": "NFI-015B-LEE-RANGE",
  "issue": "Lee 2016 Eq. 23 is the lower envelope over k from 1 to 5, computed at R/t 100 and 200. Section 7 gives no FEM result below delta/t 0.15 and no ODE result below 0.2. The envelope does not fix one width. None of these shells is at R/t 100 or 200. At kd 0.9 and 0.7 the inverse is below 0.15. At kd 0.595 it is between 0.15 and 0.2. At kd 0.5, 0.468, 0.3 and 0.2 it is at or above 0.2.",
  "consequence": "Lee amplitudes below the cutoff are not validated tolerances. Where the amplitude is in range, the single-dimple RMS is the span from k = 1 to k = 5, not one number. The radius transfer remains.",
  "next": "An envelope at this shell's R/t, or a statement that the 100 and 200 curves may be used outside that pair."
}
```

### N406 — NFI-021B-CHECK-TOLERANCE

Source `rpt-ref-444ac46ffbede876f9cd`; original file `unpublished-local-ref:e116eab86edf378e; pointer `/rows/2`.

```json
{
  "id": "NFI-021B-CHECK-TOLERANCE",
  "status": "open",
  "tag": "PROJECTION",
  "fields": [
    "floating_point.tolerance_015_at_needed_gamma.rms_worst_mm",
    "floating_point.tolerance_015_at_018_curve.rms_worst_mm"
  ],
  "exact_mismatches": [
    {
      "field": "floating_point.tolerance_015_at_needed_gamma.rms_worst_mm",
      "check": 1.7178419203992834,
      "card": 1.7088520330420545,
      "difference": 0.008989887357228943,
      "relative_difference": 0.005260775762559955,
      "pass_": false
    },
    {
      "field": "floating_point.tolerance_015_at_018_curve.rms_worst_mm",
      "check": 0.8175526580913995,
      "card": 0.8132742048661246,
      "difference": 0.004278453225274981,
      "relative_difference": 0.004278453225274981,
      "pass_": false
    }
  ],
  "inherited_nu03": {
    "kd": 0.46822856667720764,
    "nu_width": 0.3,
    "t_eq_mm": 53.364448806653826,
    "R_over_t_eq": 187.39067344687226,
    "delta_over_t_eq": 0.8586135991025216,
    "amplitude_mm": 45.819441454003304,
    "rms_lambda1_mm": 0.6509912506826875,
    "rms_worst_mm": 1.7088520330420547,
    "width_note": "Amplitude is from lambda_I=1; rms_worst changes only width to 2.625 and is not a coupled knockdown/tolerance pair."
  },
  "consistent_nu033": {
    "kd": 0.46822856667720764,
    "nu_width": 0.33,
    "t_eq_mm": 53.364448806653826,
    "R_over_t_eq": 187.39067344687226,
    "delta_over_t_eq": 0.8586135991025216,
    "amplitude_mm": 45.819441454003304,
    "rms_lambda1_mm": 0.6544159696759175,
    "rms_worst_mm": 1.7178419203992834,
    "width_note": "Amplitude is from lambda_I=1; rms_worst changes only width to 2.625 and is not a coupled knockdown/tolerance pair."
  },
  "issue": "The two filed RMS values use nu=.30 for angular width, while mechanics inherit nu=.33. More substantially, amplitude is inverted from a lambda_I=1 fit and then the RMS width is set to 2.625; that is not a single defect with a demonstrated knockdown/amplitude/RMS tuple.",
  "implication": "45.819441 mm amplitude reproduces. With width nu=.33, the same lambda_I=1 Gaussian gives 0.654416 mm whole-sphere RMS; merely changing width gives 1.717842 mm, not a validated tolerance at the same knockdown. The filed 1.708852 mm is reproduced with width nu=.30.",
  "source": "Baizhikova et al., doi:10.1016/j.jmps.2025.106468, Eq.2–3 and section 4.1; MAINLINE-015",
  "needed_evidence": "State width and nu together; calculate a coupled defect response for the sandwich, including seams and multiple defects."
}
```

### N466 — NFI-015-CHECK-SMALL-DEFECT

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/0`.

```json
{
  "id": "NFI-015-CHECK-SMALL-DEFECT",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "partly_addressed",
  "reported": "Every kd 0.9 Eq. 3 row is flagged below alpha 0.07; P2-E is flagged outside R/t 100–1550; source nu 0.5 is disclosed.",
  "checked": "No valid near-perfect replacement is supplied. The inherited 1/3/10 mm seam calculations are not revisited.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Mark these calculations outside the fitted regime; obtain a near-perfect branch before using them as tolerance requirements. Retain R/t and nu transfer limits."
}
```

### N467 — NFI-015-CHECK-LOW-KD-ENVELOPE

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/1`.

```json
{
  "id": "NFI-015-CHECK-LOW-KD-ENVELOPE",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "partly_addressed",
  "reported": "Primary Lee Eq. 23 now supplies kd 0.2/0.3 amplitudes, with FEM/ODE cutoffs and k 1–5 RMS bounds. Eq. 3 below its floor returns null.",
  "checked": "The old one-thickness bound and universal worst-width/plateau language are not explicitly repaired in the old 015 artifacts. Lee critical-width interpretation needs the new qualification below.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Replace sourced-bound language with the retrieved envelope and its range. Do not assign a unique RMS without the envelope width. k2.625 is tied to amplitude1, not all plateau minima."
}
```

### N477 — NFI-015B-CHECK-ROUNDING-PROSE

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/11`.

```json
{
  "id": "NFI-015B-CHECK-ROUNDING-PROSE",
  "provenance": "new",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "correction",
  "reported": "CARD: the difference between rounded levels and filed gammas is in the fourth digit of amplitude.",
  "checked": {
    "021": {
      "actual_gamma": 0.5953179642995181,
      "rounded_amplitude_mm": 11.821998252555694,
      "actual_amplitude_mm": 11.801408250115195,
      "rounded_minus_actual_mm": 0.02059000244049969,
      "excess_relative_to_actual_percent": 0.17447072420615495
    },
    "021b": {
      "actual_gamma": 0.46822856667720764,
      "rounded_amplitude_mm": 45.99298873860918,
      "actual_amplitude_mm": 45.819441454003304,
      "rounded_minus_actual_mm": 0.1735472846058741,
      "excess_relative_to_actual_percent": 0.37876342246574435
    },
    "interpretation": "021b changes the third significant digit: 45.9929887386 versus 45.8194414540 mm. Both stored numerical rows are correct; the blanket prose claim is false."
  },
  "evidence": [
    "owner-CARD.md, section The shells those gammas belong to",
    "RESULTS.json supplemental"
  ],
  "followup": "State the actual changes: 0.1744707242% for 0.595 and 0.3787634225% for 0.468 in Eq. 3, relative to the unrounded-gamma amplitude; retain full gammas."
}
```

### N478 — NFI-015B-CHECK-RMS-AREA

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/12`.

```json
{
  "id": "NFI-015B-CHECK-RMS-AREA",
  "provenance": "new",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "qualification",
  "reported": "CARD gives whole-sphere RMS = delta*beta0/sqrt(8) and k5/k1 = 5 without labeling the small-angle approximation.",
  "checked": {
    "model": "RMS/delta = sqrt(0.5*integral_0^pi exp(-2*(theta/beta0)^2)*sin(theta) dtheta), referenced to the undeformed sphere",
    "P2_E": {
      "1": {
        "beta0_rad": 0.07762716656262922,
        "exact_RMS_over_amplitude": 0.027438458108246803,
        "small_angle_RMS_over_amplitude": 0.027445347940366367,
        "exact_over_approx": 0.9997489617499281,
        "approx_overstatement_percent": 0.025110128609928672,
        "quadrature_absolute_error": 1.7605793792033294e-15
      },
      "5": {
        "beta0_rad": 0.38813583281314606,
        "exact_RMS_over_amplitude": 0.1363691330378657,
        "small_angle_RMS_over_amplitude": 0.13722673970183183,
        "exact_over_approx": 0.9937504405786397,
        "approx_overstatement_percent": 0.6288862038361875,
        "quadrature_absolute_error": 6.943192898576689e-16
      }
    },
    "P2_E_exact_RMS_k5_over_k1": 4.969999862961654,
    "interpretation": "Owner arithmetic is correct within its approximate area measure. At P2-E k5 the approximation exceeds the spherical-area value by 0.6288862038%; at k1 by 0.0251101286%."
  },
  "evidence": [
    "check.py independent quadrature and Dawson-function agreement",
    "RESULTS.json supplemental"
  ],
  "followup": "Label these values small-angle single-dimple whole-sphere RMS, or use the spherical-area integral. Qualify the exact five-times assertion."
}
```

### N479 — NFI-015B-CHECK-LEE-CRITICAL-WIDTH

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/13`.

```json
{
  "id": "NFI-015B-CHECK-LEE-CRITICAL-WIDTH",
  "provenance": "new",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "qualification",
  "reported": "CARD treats k1–k5 as the RMS span at an amplitude obtained by inverting the lower envelope.",
  "checked": {
    "valid": "These are broad conditional geometric RMS bounds at that fixed amplitude under the stated area approximation.",
    "limit": "Different widths generally have different knockdowns. The span is not an iso-knockdown curve and does not show that every width attains the requested kd.",
    "source": "Lee section 7 and Fig. 6(c) supply the minimizing width kc(alpha); Eq. 23 alone omits this information.",
    "radii": "Be-015 and Be-021b lie between the two computed R/t values; P2-E and Be-021 lie outside that interval. None exactly equals a computed radius."
  },
  "evidence": [
    "unpublished-local-ref:bae7bfd366ef3415 section 7, Fig. 6(b,c), Eq. 23"
  ],
  "followup": "Label the range conditional geometric bounds; use the source critical-width curve, or new calculations, when an envelope-associated RMS is required."
}
```

### C112 — NFI-029-DEFECT

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/2`.

```json
{
  "id": "NFI-029-DEFECT",
  "status": "open",
  "title": "Different defect construction",
  "issue": "Paper uses an indenter radius0.1R, contact and a stress-free reset. Present paper check uses a Gaussian of width0.1R and amplitude0.75total_thickness in every layer. Lead defects use015 lambda_I1, not a measured hull shape. Width and through-thickness deformation affect the result.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

## R070 — tolerance maps from monocoque shells transferred to sandwich (core shear, waviness, boundaries)

**Current 030c:** 042's map says 9.3–16.1 mm for the old 028b gamma; carry only as a PROJECTION, alongside 029's adverse numerical evidence and CHECK-035's unmatched S-II precedent. Shape control by itself does not establish knockdown.

**Original question:** Core shear cut to classical pressure is derived, but its cut to imperfection sensitivity has no coefficient; kd levels carry no shear correction.

### N180 — NFI-015-CORE-SHEAR-SENSITIVITY

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-CORE-SHEAR-SENSITIVITY",
  "issue": "Core shear's cut to the classical pressure is derived: 10.3, 7.0 and 0.8 percent on P2-E at 9, 14 and 138 MPa, and 11.4 percent on the aluminium core at 72.4 MPa. The cut to imperfection sensitivity has no retrieved coefficient.",
  "consequence": "The kd levels are applied with no shear-dependent correction.",
  "next": "A shear-flexible imperfection study."
}
```

### N181 — NFI-015-THICKNESS-WAVINESS-VALUES

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-THICKNESS-WAVINESS-VALUES",
  "issue": "The thickness sensitivity is derived. A locally 10 percent thin face costs 10.0 percent of P2-E classical pressure. No sourced cure tolerance for the faces or the core was retrieved.",
  "consequence": "The driver is a sensitivity, not a gap factor.",
  "next": "Source autoclave and core-machining tolerances when the build is chosen."
}
```

### N184 — NFI-015-BOUNDARY-AND-TRANSIENT

Source `rpt-ref-06668dbf12580ed0ffc3`; original file `unpublished-local-ref:d079dcc7cf300f3e; pointer `retained original identity`.

```json
{
  "id": "NFI-015-BOUNDARY-AND-TRANSIENT",
  "issue": "Full-sphere curves are used. A clamped equator can cap kappa near 0.8 for a small dimple. The static hydrostatic column is 240 Pa, 0.25 percent of the case pressure. Pump-down transients are not modelled.",
  "consequence": "The high-kd rows assume a complete sphere under uniform quasi-static pressure.",
  "next": "An equator, if the design keeps one, needs its own card."
}
```

### N387 — NFI-015B-SANDWICH

Source `rpt-ref-74e882831c201b1a953c`; original file `unpublished-local-ref:71470bf7da8d8fcd; pointer `/rows/3`.

```json
{
  "id": "NFI-015B-SANDWICH",
  "issue": "Both curves are monocoque results transferred through t_eq = sqrt(3)(core+tf). No sandwich measurement at this radius was retrieved. Core shear's effect on imperfection sensitivity has no coefficient. A single-dimple RMS is not an assembled-surface RMS.",
  "consequence": "The table is QUESTIONABLE. The 0.25 mm comparison is a numerical ratio, not a manufacturing proof.",
  "next": "A sandwich imperfection study at the floating-point geometry."
}
```

### N468 — NFI-015-CHECK-EFFECTIVE-MODULUS

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/2`.

```json
{
  "id": "NFI-015-CHECK-EFFECTIVE-MODULUS",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "partly_addressed",
  "reported": "The thin-face thickness is declared, and exact finite-face A/D-equivalent thickness is stored and reproduces.",
  "checked": "The simultaneous effective modulus Eeq/Ef = 2tf/teq is still absent. Thickness alone does not match extensional and bending stiffness; no new pressure rescore is claimed.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Include the effective modulus in the mapping. Keep Kirchhoff/shear-flexibility limitations; distinguish d and h in bending-only approximations."
}
```

### N476 — NFI-015-CHECK-MODEL-VALIDATION

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/10`.

```json
{
  "id": "NFI-015-CHECK-MODEL-VALIDATION",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "acknowledged_open",
  "reported": "The card and NFI explicitly retain QUESTIONABLE and identify the missing sandwich imperfection/core-shear study.",
  "checked": "No matching sandwich experiment or validated nonlinear imperfection model is supplied. The admission answers the request for qualification; the scientific validation remains open.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Retain QUESTIONABLE status; evaluate sandwich imperfections, seams, bonding and transverse shear in a suitable model or experiment. This is a follow-up, not a stop gate."
}
```

### N603 — NFI-017b-GAMMA-TRANSLATION

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/3`.

```json
{
  "id": "NFI-017b-GAMMA-TRANSLATION",
  "tag": "QUESTIONABLE",
  "claim": "The brief's translation of gamma into core shear stiffness per density cannot reach SF 1 (Kc caps at 1). As shape precision, MAINLINE-015's monocoque-equivalent map (t_eq = sqrt(3) h) gives a 2.47 mm dimple at R 10 and 13.1 mm at R 20; that map is a cylinder/monocoque fit applied to a sandwich sphere.",
  "needed_to_ground": "An imperfection-controlled sandwich-sphere or dome buckling test series."
}
```

### N660 — NFI-038-IMPERFECTION

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/9`.

```json
{
  "id": "NFI-038-IMPERFECTION",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Maximum dent alone does not preserve buckling similarity",
  "evidence": "021b localized amplitude map is not RMS or 028b qualification.",
  "resolution_needed": "Measure full spatial field, angular width, seams and as-built mode sensitivity.",
  "tests": [
    "T7",
    "T8"
  ]
}
```

### N676 — NFI-C035-TRANSFER

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/3`.

```json
{
  "id": "NFI-C035-TRANSFER",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "The 0.30–0.34 handbook ratio and SBKF-scaled sphere envelope are projections.",
  "next_evidence": "Resolve the lead's closed-sphere geometry, imperfections, loading and shear model directly; retain transfer estimates as PROJECTION.",
  "evidence": [
    "E09",
    "E10",
    "SOURCE-CORRECTIONS.json"
  ],
  "blocks_card": false
}
```

### N687 — NFI-C035-IMPERFECTION

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/14`.

```json
{
  "id": "NFI-C035-IMPERFECTION",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "The record does not establish that required imperfection control exceeds every recorded sandwich dome.",
  "next_evidence": "Quantify the lead geometry's admissible measured imperfection distribution; compare like geometry/material/boundary cases before any universal claim.",
  "evidence": [
    "E07",
    "E17",
    "E18",
    "E19",
    "E20"
  ],
  "blocks_card": false
}
```

### C138 — N042-02

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/1`.

```json
{
  "id": "N042-02",
  "issue": "S-II's shape and specimens are unpublished in the sources opened",
  "detail": "No as-built contour RMS or peak exists for the S-II or S-IVB bulkheads. The CR-1457 hemisphere specimen details (SDL 468) are unread.",
  "to_close": "Retrieve SDL 468 and S-II acceptance records.",
  "tag": "QUESTIONABLE"
}
```

### S002 — NFI-030C-042-MAP

Source `rpt-1228-mainline030c-design-register-1020`; original file `unpublished-local-ref:3c01fd6db28be861; pointer `/rows/1`.

```json
{
  "id": "NFI-030C-042-MAP",
  "title": "042's permissive dimple map must not override 029.",
  "finding": "Keep 042's 9.3–16.1 mm allowance and mapped gamma .69–.95 as conditional monocoque transfers. 029 supplies contradictory numerical evidence at related sandwich points. Neither historical S-II gamma about .2 nor a fabrication tolerance qualifies the new Be hull.",
  "status": "OPEN",
  "blocks_progress": false,
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## R071 — geometry levers at equal margin (radius, altitude, partial vacuum)

**Original question:** 11000 m is evaluated on the tropospheric lapse at the tropopause boundary; the isothermal stratosphere is not used; no effect inside this grid.

### N144 — NFI-010-FIXEDTHICK

Source `rpt-ref-58b2bed18db2449100f2`; original file `unpublished-local-ref:9b713febb61ac916; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-010-FIXEDTHICK",
  "gap": "Levers 1 and 4 hold face and core thickness fixed while radius changes. A real design re-optimizes thickness per radius; the mass-ceiling rows of 002/003 show how much that moves things at 10 m only.",
  "direction": "Re-run the levers with thickness re-solved at the float ceiling per radius.",
  "effect": "Margins improve at small radius; SF rankings are not expected to flip."
}
```

### N147 — NFI-010-007008

Source `rpt-ref-58b2bed18db2449100f2`; original file `unpublished-local-ref:9b713febb61ac916; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-010-007008",
  "gap": "MAINLINE-007 and 008 had not filed when this card closed, so lever 1 was not re-run on their best rows, as the brief's Then clause directs.",
  "direction": "Re-run lever 1 on their best rows when they file; the script here takes any tf/core row.",
  "effect": "None on this card's numbers."
}
```

### N319 — NFI-CORE-FIXED

Source `rpt-mainline012-grok-equal-margin-1019`; original file `unpublished-local-ref:e1f08cf5f095ddec; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-CORE-FIXED",
  "gap": "P2-A keeps the 0.1 m core while radius and altitude change. That fixed core can exhaust the mass budget.",
  "direction": "A core thickness that scales with radius.",
  "effect": "An infeasible row has no safety factor."
}
```

### N320 — NFI-TROPOPAUSE

Source `rpt-mainline012-grok-equal-margin-1019`; original file `unpublished-local-ref:e1f08cf5f095ddec; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-TROPOPAUSE",
  "gap": "11000 m is evaluated on the tropospheric lapse at the tropopause boundary. The isothermal stratosphere is not used.",
  "direction": "Hold T at 216.65 K above 11000 m if a later card climbs further.",
  "effect": "None inside this grid. 11000 m is the top row."
}
```

## R072 — P3 member cap bounded continuation

**Original question:** P3 re-optimisation holds bay 0.4-3 m and member radius at most 0.25 m, which governs large hulls; similarity rows hold 80 um film so film SF falls as 1/R.

### N114 — NFI-027-FRAME-BOUNDARY

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-FRAME-BOUNDARY",
  "tag": "QUESTIONABLE",
  "issue": "P3 reoptimization holds bay 0.4–3 m and radius≤0.25 m. The radius cap governs large hulls. Similarity rows separately scale members but hold 80 µm film, making film SF fall as 1/R.",
  "next_evidence": "Treat relaxed member caps or thicker film as separately costed designs; do not infer a universal radius optimum from this bounded continuation."
}
```

## R073 — thin-shell validity at low density

**Original question:** On the buckling split the core exceeds a tenth of the radius below about 1.8 kg/m3, so margins there are not physical.

### N165 — NFI-013-GEOMETRY-B

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-GEOMETRY-B",
  "issue": "On the buckling split the core exceeds a tenth of the radius below about 1.8 kg/m3 and the radius itself below about 0.18 kg/m3, so B-split margins there are not physical (external-area and thin-shell rules).",
  "numbers": "B core 1.81 m at 1 kg/m3, 18.1 m at 0.1 kg/m3; the Q split holds h = 0.18907 m and is valid at every density.",
  "closes_when": "a thick-shell sandwich model with the inner surface area replaces the external-area rule."
}
```

## R074 — face stress past yield elastic wrinkling

**Original question:** The 6061 face exceeds its questionable 276 MPa yield on every row, so elastic wrinkling forms flatter it.

### N164 — NFI-013-FACE-YIELD

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-FACE-YIELD",
  "issue": "The 6061 face is past its QUESTIONABLE 276 MPa on every row, so the elastic wrinkling forms (eta 1) flatter it.",
  "numbers": "Face stress 3.57e+08 Pa (Q, 0.1 kg/m3) to 7.09e+08 Pa.",
  "closes_when": "the face material changes (008b) or CR-1457 section 9 plasticity factors are applied."
}
```

### N448 — eta

Source `rpt-mainline032-grok-wrinkle-waviness-1020`; original file `unpublished-local-ref:e20bd8d3e1ca97e2; pointer `/open/2`.

```json
{
  "id": "eta",
  "tag": "QUESTIONABLE",
  "note": "The page says elastic cases use eta = 1, and inelastic cases use section 9. The map uses eta = 1. The 021 faces sit at compression safety factor about 1, so a plasticity factor may apply. It is not in this Q map."
}
```

### N531 — NFI-032-CHECK-ETA

Source `rpt-ref-a30a669ed3e245f1473b`; original file `unpublished-local-ref:46e93c1ee5674acc; pointer `/findings/3`.

```json
{
  "id": "NFI-032-CHECK-ETA",
  "status": "open",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "The map assumes elastic eta=1.",
  "checked": "Relative to sqrt(Ef*Ec*tf/tc), the effective coefficient is 0.82*sqrt(eta)/(1+0.64*Kdelta). For a fixed target Q, amplitude changes with eta. Plasticity in the nearly strength-limited faces is not calibrated.",
  "followup": "Use a measured constitutive/plasticity basis self-consistently; supplemental eta cases here are PROJECTION, not new material data.",
  "source_audit_ids": [
    "NASA-EQ2212",
    "NASA-DESIGN033"
  ],
  "owner_nfi_ids": [
    "eta"
  ],
  "sensitivity_projection": {
    "Be S-200F": {
      "minimum_eta_for_target_Q_even_at_zero_waviness": 0.20470107079119573,
      "eta_sensitivity_projection": [
        {
          "eta": 1.0,
          "delta_mm_at_60psi": 0.15286876684636114,
          "target_possible": true
        },
        {
          "eta": 0.9,
          "delta_mm_at_60psi": 0.13854210498572647,
          "target_possible": true
        },
        {
          "eta": 0.8,
          "delta_mm_at_60psi": 0.12339481628518875,
          "target_possible": true
        },
        {
          "eta": 0.6,
          "delta_mm_at_60psi": 0.08994037941380915,
          "target_possible": true
        },
        {
          "eta": 0.5,
          "delta_mm_at_60psi": 0.07109846696731308,
          "target_possible": true
        }
      ]
    },
    "SR-200": {
      "minimum_eta_for_target_Q_even_at_zero_waviness": 0.5515779298036882,
      "eta_sensitivity_projection": [
        {
          "eta": 1.0,
          "delta_mm_at_60psi": 0.06522290640394086,
          "target_possible": true
        },
        {
          "eta": 0.9,
          "delta_mm_at_60psi": 0.05221551281373981,
          "target_possible": true
        },
        {
          "eta": 0.8,
          "delta_mm_at_60psi": 0.038463059669461404,
          "target_possible": true
        },
        {
          "eta": 0.6,
          "delta_mm_at_60psi": 0.008089269043450881,
          "target_possible": true
        },
        {
          "eta": 0.5,
          "delta_mm_at_60psi": 0.0,
          "target_possible": false
        }
      ]
    }
  }
}
```

### N628 — NFI-032-CHECK-ETA

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/prior_032_findings_retained/3`.

```json
{
  "id": "NFI-032-CHECK-ETA",
  "status": "open",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "The map assumes elastic eta=1.",
  "checked": "Relative to sqrt(Ef*Ec*tf/tc), the effective coefficient is 0.82*sqrt(eta)/(1+0.64*Kdelta). For a fixed target Q, amplitude changes with eta. Plasticity in the nearly strength-limited faces is not calibrated.",
  "followup": "Use a measured constitutive/plasticity basis self-consistently; supplemental eta cases here are PROJECTION, not new material data.",
  "source_audit_ids": [
    "NASA-EQ2212",
    "NASA-DESIGN033"
  ],
  "owner_nfi_ids": [
    "eta"
  ],
  "sensitivity_projection": {
    "Be S-200F": {
      "minimum_eta_for_target_Q_even_at_zero_waviness": 0.20470107079119573,
      "eta_sensitivity_projection": [
        {
          "eta": 1.0,
          "delta_mm_at_60psi": 0.15286876684636114,
          "target_possible": true
        },
        {
          "eta": 0.9,
          "delta_mm_at_60psi": 0.13854210498572647,
          "target_possible": true
        },
        {
          "eta": 0.8,
          "delta_mm_at_60psi": 0.12339481628518875,
          "target_possible": true
        },
        {
          "eta": 0.6,
          "delta_mm_at_60psi": 0.08994037941380915,
          "target_possible": true
        },
        {
          "eta": 0.5,
          "delta_mm_at_60psi": 0.07109846696731308,
          "target_possible": true
        }
      ]
    },
    "SR-200": {
      "minimum_eta_for_target_Q_even_at_zero_waviness": 0.5515779298036882,
      "eta_sensitivity_projection": [
        {
          "eta": 1.0,
          "delta_mm_at_60psi": 0.06522290640394086,
          "target_possible": true
        },
        {
          "eta": 0.9,
          "delta_mm_at_60psi": 0.05221551281373981,
          "target_possible": true
        },
        {
          "eta": 0.8,
          "delta_mm_at_60psi": 0.038463059669461404,
          "target_possible": true
        },
        {
          "eta": 0.6,
          "delta_mm_at_60psi": 0.008089269043450881,
          "target_possible": true
        },
        {
          "eta": 0.5,
          "delta_mm_at_60psi": 0.0,
          "target_possible": false
        }
      ]
    }
  }
}
```

## R075 — tensile yield used as the compressive allowable (aluminium and others)

**Original question:** 276 MPa typical tensile yield is transferred to compression by owner assumption; source says typical values are not for design; no compressive yield was retrieved.

### N028 — NFI-AL-YIELD-CARRY

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-AL-YIELD-CARRY",
  "gap": "276 MPa remains the inherited AA typical tensile yield, transferred to compression. Strength safety factors are QUESTIONABLE.",
  "direction": "A compression yield or a design allowable can replace the transfer.",
  "effect": "Yield cannot reach safety factor 1 on this ceiling. The all-face factor on 276 MPa is 1.28636483585. At the named least-factor peak the factor is 1.35679953494. Where buckling safety factor first reaches 1 the strength factor is 2.57095082176."
}
```

### N123 — NFI-005-SIGMA

Source `rpt-ref-eb07faa637b7487d6dc5`; original file `unpublished-local-ref:2ef2c84bad6b0b03; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-005-SIGMA",
  "gap": "276 MPa is a QUESTIONABLE typical tensile yield transferred to compression (inherited NFI-AL-YIELD-CARRY). Required strengths here are membrane stresses and do not depend on it; only the x276 MPa multiples and SF labels do.",
  "direction": "Obtain a compressive design allowable and rescale the multiples only.",
  "effect": "No required Pa value in this card moves."
}
```

### N133 — NFI-008-SIGMA-TRANSFER

Source `rpt-ref-45da79edf548b064b228`; original file `unpublished-local-ref:20c691c11e9fda46; pointer `retained original identity`.

```json
{
  "id": "NFI-008-SIGMA-TRANSFER",
  "issue": "6061-T6, 7075-T6, 2195-T8 and AlBeMet 162 compressive strengths are tensile yields transferred to compression; AZ31 uses a compressive yield, Ti-6Al-4V and Be S-200F use compressive values, SiC a compressive ultimate, Vitreloy 1 a compressive ultimate.",
  "effect": "SF_y for transferred rows is QUESTIONABLE; the 6061 baseline itself is the pinned transfer, so ratios are consistent with 002/003.",
  "needed": "Measured compressive yield for each metal temper and product form."
}
```

### N243 — NFI-AL

Source `rpt-mainline-grok-estimates-card-1019`; original file `unpublished-local-ref:f21ed29fa04c48f4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-AL",
  "linked_inputs_or_points": "I-E I-RHO-AL I-NU",
  "questionable_assumption_or_gap": "Room-temperature typical properties, Poisson estimated.",
  "direction_of_further_investigation": "MMPDS allowables at about 285 K.",
  "how_it_affects_margin_or_SF": "E scales collapse linearly in all three models. Density scales metallic mass."
}
```

### N253 — NFI-AL-YIELD-CARRY

Source `rpt-mainline002-grok-strength-card-1019`; original file `unpublished-local-ref:f02996967e2f160d; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-AL-YIELD-CARRY",
  "gap": "276 MPa is the retrieved AA typical tensile yield. It is transferred to compression by owner assumption. The sheet says AA typical values are not for design. No compressive yield was in the retrieved snippet.",
  "direction": "Obtain a compression yield or design allowable and drop the transfer.",
  "effect": "Aluminum-strength pressure and its factor scale linearly with this value."
}
```

### N261 — NFI-AL-YIELD-CARRY

Source `rpt-mainline003-grok-p2-targets-1019`; original file `unpublished-local-ref:c644022670e558c3; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-AL-YIELD-CARRY",
  "gap": "276 MPa remains the inherited AA typical tensile yield, transferred to compression. Strength safety factors are QUESTIONABLE. The carry is parallel and is not a gate.",
  "direction": "A compression yield or design allowable can replace the transfer.",
  "effect": "Strength pressure and the required compressive strength scale linearly with this value."
}
```

### N274 — NFI-AL-YIELD-CARRY

Source `rpt-mainline004-grok-knockdown-card-1019`; original file `unpublished-local-ref:bd4eb9f1634108a4; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-AL-YIELD-CARRY",
  "gap": "003 strength safety factors stay QUESTIONABLE and unchanged. Buckling knockdown does not cure yield, shear, wrinkling or crush.",
  "direction": "Keep the carry parallel.",
  "effect": "Strength safety factor is not rescaled."
}
```

### N283 — NFI-STRENGTH

Source `rpt-mainline004b-grok-kd-range-1019`; original file `unpublished-local-ref:1b2ceafd06f5792e; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-STRENGTH",
  "gap": "Strength safety factors stay at the sealed 003 QUESTIONABLE values. Knockdown does not rescale yield.",
  "direction": "Leave strength on its own card.",
  "effect": "Strength safety factor is unchanged at every knockdown."
}
```

### N287 — NFI-YIELD

Source `rpt-mainline006-check-lead4f19-1019`; original file `unpublished-local-ref:5ea5fd1bf192b52a; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-YIELD",
  "gap": "Confirmed: yield is 276 MPa tensile yield transferred to compression, QUESTIONABLE.",
  "direction": "A compression allowable.",
  "effect": "Yield SF scales linearly with that allowable."
}
```

### N291 — NFI-YIELD

Source `rpt-mainline006-grok-float-margin-1019`; original file `unpublished-local-ref:50c93f23f6adae0f; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-YIELD",
  "gap": "Yield uses 276 MPa tensile yield transferred to compression. QUESTIONABLE.",
  "direction": "A compression allowable.",
  "effect": "Yield SF scales linearly with that allowable."
}
```

### N294 — NFI-AL-YIELD-CARRY

Source `rpt-mainline007-check-lead4f19-1019`; original file `unpublished-local-ref:a0b67c87ff180a29; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-AL-YIELD-CARRY",
  "gap": "Confirmed: 276 MPa is a typical tensile yield transferred to compression, QUESTIONABLE. Yield cannot reach SF 1 on this ceiling: all-face SF 0.7773844341284152, strength factor 1.28636483585 with no core, 1.35679953494 at the named peak, 2.57095082176 where buckling first reaches 1.",
  "direction": "A compression yield or design allowable.",
  "effect": "Owner statement stands."
}
```

## R076 — CNT and graphene materials (PROJECTION)

**Original question:** Cheapest P2 direction on all three leaders is lower face density alone, needing faces near 0.9-1.1 g/cc with CNT, Be and graphene E and sigma; all PROJECTION.

### N097 — NFI-CNT-GRAPHENE

Source `rpt-ref-4f09fd6b4c4dd848ebb0`; original file `unpublished-local-ref:37417375bae1d523; pointer `retained original identity`.

```json
{
  "id": "NFI-CNT-GRAPHENE",
  "state": "PROJECTION",
  "note": "No production allowable was opened. Thickness is not stated."
}
```

### N136 — NFI-008-PROJECTIONS

Source `rpt-ref-45da79edf548b064b228`; original file `unpublished-local-ref:20c691c11e9fda46; pointer `retained original identity`.

```json
{
  "id": "NFI-008-PROJECTIONS",
  "issue": "CNT-yarn and graphene QI rows are PROJECTION scenarios, not available materials; their assumed values are stated per row.",
  "effect": "They bound a direction, not a procurement option; the available-only best three are listed separately.",
  "needed": "A demonstrated QI CNT-yarn or graphene laminate card."
}
```

### N350 — NFI-017-FACE-DENSITY

Source `rpt-mainline017-improvement-directions-lead4f19-1019`; original file `unpublished-local-ref:b586b896a14aa878; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-017-FACE-DENSITY",
  "gap": "The cheapest P2 direction on all three leaders is face density alone (factors 1.459, 1.637, 1.655), requiring faces at 959.5, 1129.7 and 906.5 kg/m3 carrying CNT, Be and graphene E and sigma. The lightest QUESTIONABLE face today is T700 at 1550 kg/m3.",
  "direction": "A structural face at about 0.9-1.1 g/cc with those stiffness and strength values.",
  "effect": "All three are PROJECTION. Beryllium itself cannot get lighter; that direction is a different face carrying Be-like properties."
}
```

## R077 — 013 source quality (figure-read, second-hand, unopened sources)

**Original question:** A list of paywalled sources was not opened, so none of their values is used; the stiffer ultralight ceramic octet point may be among them.

### N160 — ref-ce7077da95749d9c1df0

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "ref-ce7077da95749d9c1df0",
  "issue": "Two values arrive second-hand: the vitreous carbon octet micro-lattice (Jacobsen 2011, via Zhang 2019) and the glassy carbon exponents (Bauer 2016, via Zhang 2019); Schaedler 2011's 10 kg/m3 nickel point also via Zhang 2019.",
  "numbers": "The 190 kg/m3 all-three pass rests on the secondary Jacobsen numbers (1.1 GPa, 10.2 MPa).",
  "closes_when": "the primary papers are opened and the values matched."
}
```

### N161 — NFI-013-FIGURE-READS

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-FIGURE-READS",
  "issue": "Maloney 2013, Zheng 2016, Meza 2014, Meza 2015 and Zhu 2015 values are read by eye from log plots (about 25 to 50 percent); the Meza densities are inferred from relative density.",
  "numbers": "None of these readings sits near a margin of 1 except the Meza 2015 crush point (1.34).",
  "closes_when": "tabulated values (journal SI or theses) replace the readings."
}
```

### N171 — NFI-013-NOT-OPENED

Source `rpt-ref-44f9940325e236cb80b3`; original file `unpublished-local-ref:b7e83d496df45316; pointer `retained original identity`.

```json
{
  "id": "NFI-013-NOT-OPENED",
  "issue": "Sources that were paywalled or blocked, so none of their values is used: Schaedler 2011 full text and SI, Torrents 2012, Valdevit 2013, Salari-Sharif 2014, Zheng 2014 (Science 344, 1373), Jang 2013, Deshpande-Ashby-Fleck 2001, Gross and Fricke 1995, Woignier 1989 full text, Ma 2000 full text, Sun 2013, Hu 2013, Zou 2010, Gui 2010, Worsley 2009 and 2012, Mecklenburg 2012, Eckel 2016, Bauer 2016, Jacobsen 2011.",
  "numbers": "Zheng 2014 (MIT DSpace HTTP 429, Science 403) is the likeliest source of a stiffer ultralight ceramic octet point.",
  "closes_when": "those texts are obtained and their values added through build_cores.py."
}
```

### N472 — NFI-015-CHECK-SOURCE-IDENTIFIERS

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/6`.

```json
{
  "id": "NFI-015-CHECK-SOURCE-IDENTIFIERS",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "partly_addressed",
  "reported": "Lee Eq. 23 is now cited and pinned directly, avoiding the later paper's printed coefficient ambiguity.",
  "checked": "The two incorrect DOI identifiers in the old 015 material are not expressly corrected. They are not repeated in this focused card.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Correct the identifiers; cite Lee directly for its equation instead of silently repairing the later printed equation."
}
```

### N522 — NFI-035-EYE-READ

Source `rpt-mainline035-opus-knockdown-tests-1020`; original file `unpublished-local-ref:4d5781abcddc2e1c; pointer `/rows/4`.

```json
{
  "id": "NFI-035-EYE-READ",
  "state": "open",
  "note": "CR-1457 Fig. 4.2-3 and Fig. 6.2-3 values are read by eye from page images, by the B and C researchers and independently by this seat; about +/-0.02 in gamma and +/-10% in R/rho.",
  "settle": "the primary reports behind them"
}
```

### N523 — ref-5e993e8eb72d4845aa62

Source `rpt-mainline035-opus-knockdown-tests-1020`; original file `unpublished-local-ref:4d5781abcddc2e1c; pointer `/rows/5`.

```json
{
  "id": "ref-5e993e8eb72d4845aa62",
  "state": "open",
  "note": "Not retrieved: FPL 1830 (March and Kuenzi 1957; DTIC 403, FPL 502 from here), Baker AIAA J 1968, the Hexcel summary of 25 Jul 1963, FPL PE-227, Kazimi 1960. Per-specimen geometry and Vc of the pre-1969 cylinders stay unknown.",
  "settle": "library retrieval"
}
```

### N524 — NFI-035-DESICOS

Source `rpt-mainline035-opus-knockdown-tests-1020`; original file `unpublished-local-ref:4d5781abcddc2e1c; pointer `/rows/6`.

```json
{
  "id": "NFI-035-DESICOS",
  "state": "open",
  "note": "Measured buckling of the Ariane 5 SYLDA/ISS sandwich shells (Bisagni 2016) is in a restricted paper; Alfano and Bisagni 2017 give only geometry, FE and SP-8007 0.57/0.64.",
  "settle": "the restricted paper"
}
```

### N525 — NFI-035-DOME-LEADS

Source `rpt-mainline035-opus-knockdown-tests-1020`; original file `unpublished-local-ref:4d5781abcddc2e1c; pointer `/rows/7`.

```json
{
  "id": "NFI-035-DOME-LEADS",
  "state": "open",
  "note": "Brix 1968 (GFP sandwich domes under external pressure) and Anderson 1966 (Georgia Tech, spherical sandwich shell) are unread leads; either may hold the only sandwich-dome test series.",
  "settle": "library retrieval"
}
```

### N611 — NFI-017b-TREND-GAPS

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/11`.

```json
{
  "id": "NFI-017b-TREND-GAPS",
  "tag": "QUESTIONABLE",
  "claim": "Eras not found: beryllium datasheets of about 2006 and 2016; Hexoloy datasheets of about 1996 and 2016; any carbon-honeycomb history; Wright 1965 and JGJ 7-2010 (the lattice 0.4 and 0.2) were not read; Krenzke 1963 not opened. Identical Hexcel tables may mean no re-testing rather than no progress.",
  "needed_to_ground": "The missing datasheets (Wayback rate limits blocked some)."
}
```

### N678 — ref-196608af78549ed7f1ff

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/5`.

```json
{
  "id": "ref-196608af78549ed7f1ff",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "Primary Baker, FPL, Hexcel and Kazimi specimen reports remain unread.",
  "next_evidence": "Acquire the named primary reports and recover dimensions, materials, core shear and test denominators; replace handbook graph estimates.",
  "evidence": [
    "E06",
    "E08",
    "DIGITIZATION-CYLINDERS.json"
  ],
  "blocks_card": false
}
```

### N679 — NFI-C035-BRIX

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/6`.

```json
{
  "id": "NFI-C035-BRIX",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "Brix 1968 sandwich-dome paper remains an unread experimental lead.",
  "next_evidence": "Retrieve Durchschlagen von GFP-Sandwichkuppeln, IfL 7(11), 408–413; extract actual loading, dimensions, moduli and test/prediction values.",
  "evidence": [
    "intake/owner/LIT-C.json",
    "EVIDENCE.md"
  ],
  "blocks_card": false
}
```

### N680 — NFI-C035-SIM

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/7`.

```json
{
  "id": "NFI-C035-SIM",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "035's Vc≈200, R/rho≈26 and crimp ratios 1.44–1.54 have no independently reconstructed chain here; Sim's uniform-pressure results are FE.",
  "next_evidence": "Recover the exact 018b/EUCASS2023-367 inputs and reduction formulas. Keep platen tests separate from uniform-pressure simulations.",
  "evidence": [
    "E15",
    "intake/owner/CARD.md"
  ],
  "blocks_card": false
}
```

### N682 — NFI-C035-TANG-MARINE

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/9`.

```json
{
  "id": "NFI-C035-TANG-MARINE",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "Tang's 2025 elliptical steel/resin pressure-hull experiment is an abstract-level lead.",
  "next_evidence": "Acquire DOI 10.1016/j.marstruc.2025.103855 full text and numerical tables; classify plasticity, curvature and Vc before comparison.",
  "evidence": [
    "E18"
  ],
  "blocks_card": false
}
```

### N683 — NFI-C035-TANG-JSSM

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/10`.

```json
{
  "id": "NFI-C035-TANG-JSSM",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "Tang's three sandwich ellipsoids use a stronger/stiffer core; applicability to a soft-core model is unresolved.",
  "next_evidence": "Acquire DOI 10.1177/10996362251383617 full text and recover geometry, effective properties and independent test/eigenvalue ratios.",
  "evidence": [
    "E19"
  ],
  "blocks_card": false
}
```

### N684 — NFI-C035-BARATHAN

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/11`.

```json
{
  "id": "NFI-C035-BARATHAN",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "The owner's C05 semi-ellipsoid hydrostatic experiment was omitted from its categorical conclusion.",
  "next_evidence": "Acquire DOI 10.1080/15376494.2022.2114049 full text and classify test pressures, theory, geometry and effective shear.",
  "evidence": [
    "E20",
    "intake/owner/LIT-C.json"
  ],
  "blocks_card": false
}
```

### N685 — NFI-C035-DENARDO

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/12`.

```json
{
  "id": "NFI-C035-DENARDO",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "A documented foam-core cylinder experiment contradicts the card's no-test claim; full thesis access failed.",
  "next_evidence": "Retrieve DeNardo 2017 URI thesis 1075 and reconstruct geometry, effective shear and test/perfect-shell ratios.",
  "evidence": [
    "E21",
    "intake/owner/LIT-D.json",
    "sources/FETCH-04.json"
  ],
  "blocks_card": false
}
```

### N688 — NFI-C035-RESTRICTED

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/15`.

```json
{
  "id": "NFI-C035-RESTRICTED",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "Restricted DESICOS and other abstract-only leads prevent an exhaustive claim about modern cylinder data.",
  "next_evidence": "Retain access limitations in the evidence ledger and inspect full specimen data when accessible.",
  "evidence": [
    "intake/owner/LIT-B.json",
    "intake/owner/NFI.json"
  ],
  "blocks_card": false
}
```

## R078 — 1/least SF is not property multiple

**Original question:** 1/least SF is the safety-factor gap and equals the property multiple only when the mode scales proportionally; wrinkling scales as a cube or square root.

### N328 — NFI-FACTOR

Source `rpt-mainline014-grok-balanced-sandwich-1019`; original file `unpublished-local-ref:8c5f980fe25f9829; pointer `retained original identity`.

```json
{
  "id": "NFI-FACTOR",
  "note": "1/least SF is the safety-factor gap. It is the property multiple only when that mode scales in proportion to the named property. Wrinkling scales as a cube root or a square root."
}
```

### N345 — NFI-FACTOR

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-FACTOR",
  "note": "1/least SF is the safety-factor gap. It is the property multiple only when that mode scales in proportion. Wrinkling scales as a square root or a cube root. Dimpling scales as tf cubed."
}
```

### C050 — NFI-CHECK037-RESTORATION

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/12`.

```json
{
  "id": "NFI-CHECK037-RESTORATION",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "Multiplying a tube mass by reciprocal least SF is not a demonstrated structural restoration and cannot repair a separate film failure.",
  "proposed_fix": "Recompute changed sections, Euler/local/Perry/global modes, film, fittings, sag and lift. Use the supplied corrected proportional masses only as sensitivities."
}
```

## R079 — documentation and provenance defects (no numeric effect)

**030b source history:** Every original 030 source row and both citations of N023 are preserved. CHECK-030 confirms 362 unique rows versus 363 original pointers. Source-file provenance mismatches from earlier rewritten artifacts remain in the baseline index.

**Original question:** Owner caveats stand: volume ignores intrusion; joints 5% and systems 100 kg inherited; no sourced Gc/Ec core at 8-1 kg/m3; datasheet disagreements kept; microlattice 0.9 kg/m3 is density only.

### N010 — NFI-CHECK013-MEZA-SPECIMEN-NOTE

Source `rpt-1228-mainline013-independent-check-1020`; original file `unpublished-local-ref:b1c8a108ddfdc4b1; pointer `retained original identity`.

```json
{
  "id": "NFI-CHECK013-MEZA-SPECIMEN-NOTE",
  "kind": "metadata correction",
  "row": "meza2015-hier-hollow-alumina-heaviest-halfcell",
  "field": "notes specimen geometry",
  "card_value": {
    "geometry": "octahedron-of-octahedra",
    "base_cell_um": 12,
    "N": 20,
    "relative_density": 0.000104
  },
  "checker_value": {
    "geometry": "octahedron-of-octets",
    "base_cell_um": 8,
    "N": 10,
    "relative_density": 0.00182
  },
  "source": "sources/meza2015-si.pdf Table S1 p10",
  "issue": "Architecture field is correct; notes copy the lightest specimen into the heaviest record.",
  "proposed_fix": "Correct notes only. The calculated high-density geometry and core margins do not change.",
  "nonblocking": true,
  "halts_owner": false,
  "halts_next_card": false
}
```

### N023 — NFI-CHK011B-TEXT

Source `rpt-check011b-opus-1020`; original file `unpublished-local-ref:252e7a0b939c4177; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK011B-TEXT",
  "state": "demonstrated",
  "direction": "documentation",
  "note": "M1: the report body says 'k 0.4 and 0.5 are in the card', but the CARD.md table carries k 1, 0.4 and 0.2 (k 0.5 is in RESULTS.json only). M2: INPUTS.json materials carry no source and 011's INPUTS.json, which holds them, is not pinned. M3: Buchert 1968 prints the card's Et and D, so it can be cited. M4: the 'two_way' rows are the triangulated frame scored with C = 4, not a two-way frame, which would have zero in-plane shear stiffness (C1212 = 0)."
}
```

### N026 — NFI-CHK019-TEXT

Source `rpt-check019-opus-1020`; original file `unpublished-local-ref:391c78ac32ab1335; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK019-TEXT",
  "state": "demonstrated",
  "direction": "documentation",
  "note": "M1: the order cites rpt-ref-ea73d14ec4d4d8963f76; the filing is rpt-ref-d7f99cd71e977826da48. M2: the brief asks every line item for an optimistic and a conservative value; payload is 0 kg on both lines, and the 100 kg payload is only a sensitivity on the optimistic case."
}
```

### N081 — NFI-019-PREDECESSOR-ARITHMETIC

Source `rpt-ref-d7f99cd71e977826da48`; original file `unpublished-local-ref:21eb8b67fc97f529; pointer `retained original identity`.

```json
{
  "id": "NFI-019-PREDECESSOR-ARITHMETIC",
  "tag": "QUESTIONABLE",
  "status": "open",
  "issue": "The inherited partial script was not runnable and omitted the 86400 divisor in gas throughput plus the g-to-kg conversion for getter mass. MAINLINE-016 used a linear temperature loss and a constant-final-ratio commissioning expression.",
  "next_evidence": "Use this script's normalized throughput, exact p/T climate calculation and variable-pressure reversible integral. Actual ground pump-down energy still needs measurement."
}
```

### N116 — NFI-027-PROVENANCE

Source `rpt-ref-2898e43e4928e833af6d`; original file `unpublished-local-ref:941e9f8f4af887fa; pointer `retained original identity`.

```json
{
  "id": "NFI-027-PROVENANCE",
  "tag": "QUESTIONABLE",
  "issue": "The dispatch names a nonmatching 019 report ID; actual verified ID uses lead-sci. Original 021 hashes are superseded by revision 1, which was used. Scientific uncertainty remains despite arithmetic checks.",
  "next_evidence": "Use INPUTS.json's 53 verified/measured pins and the actual 019/revised 021 filing IDs; freeze this card after filing."
}
```

### N117 — NFI-CHECK021-PINS

Source `rpt-ref-e92af61311c9bf4a89cd`; original file `unpublished-local-ref:e3324087b91fd866; pointer `retained original identity`.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

### N140 — NFI-008B-BASIS

Source `rpt-ref-cc9cef5e55adca018a8f`; original file `unpublished-local-ref:2bbb739a4c037482; pointer `retained original identity`.

```json
{
  "id": "NFI-008B-BASIS",
  "inherited": "NFI-CHECK-008-BASIS (from the 008 check)",
  "issue": "The quasi-isotropic moduli 54, 135, 210, 86 and 180 GPa are rounded products of their stated bases (53.6, 136.5, 211.15, 85.68, 179.2); the unidirectional compressive strengths behind 520, 350 and 220 MPa are unnamed.",
  "consequence": "Recomputing with the unrounded products does not change any rank order in this card (verified for P2-E by the checker; the light-core rows scale all candidates by the same ratios, so their order is unchanged too).",
  "next": "Write each QI modulus as its product and name the UD strengths when the material set is next touched."
}
```

### N284 — CHECK-NFI-1

Source `rpt-mainline006-check-lead4f19-1019`; original file `unpublished-local-ref:5ea5fd1bf192b52a; pointer `retained original identity`.

```json
{
  "NFI_id": "CHECK-NFI-1",
  "gap": "Owner report body calls every baseline a sealed 002 baseline. P2-E/baseline (face 0.000248148148148 m, core 0.08375 m) is an equal-mass split constructed at the 002 P2 counted mass, not a sealed 002 geometry.",
  "direction": "Relabel that one row as the equal-split row at the 002 P2 mass. No number changes.",
  "effect": "Provenance only. All P2-E baseline numbers reproduce."
}
```

### N293 — CHECK-NFI-1

Source `rpt-mainline007-check-lead4f19-1019`; original file `unpublished-local-ref:a0b67c87ff180a29; pointer `retained original identity`.

```json
{
  "NFI_id": "CHECK-NFI-1",
  "gap": "No numeric mismatch was found. At the equal-factor split (densities 8, 6, 4, 3, 1) SF_b and SF_y are equal; a checker's strict inequality can label that tie either way by the last bit.",
  "direction": "Keep the card's both_equal label. No fix card.",
  "effect": "None. Least SF is unchanged."
}
```

### N298 — NFI-GEOM/MASS/RULE/CORE-FLOOR/DATASHEET/MICROLATTICE

Source `rpt-mainline007-check-lead4f19-1019`; original file `unpublished-local-ref:a0b67c87ff180a29; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-GEOM/MASS/RULE/CORE-FLOOR/DATASHEET/MICROLATTICE",
  "gap": "Confirmed as stated by the owner: external area/volume ignore intrusion (the 1 kg/m3 buckling-peak core is 1.8145766829090553 m); joints 5% and systems 100 kg are inherited; the splits optimise only buckling and QUESTIONABLE yield; no catalog core with sourced Gc, Ec and strength exists at 8-1 kg/m3; the Plascore psi/MPa and Divinycell rev7/rev9 disagreements are kept visible; the 0.9 kg/m3 microlattice is density only.",
  "direction": "Owner directions stand.",
  "effect": "None inside the compared numbers."
}
```

### N317 — NFI-011B-SKIP

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-SKIP",
  "note": "The brief's last line names checks 006, 007 and 007b. The rotating order says those checks are already filed and are skipped here."
}
```

### N353 — NFI-017-UNFILED

Source `rpt-mainline017-improvement-directions-lead4f19-1019`; original file `unpublished-local-ref:b586b896a14aa878; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-017-UNFILED",
  "gap": "MAINLINE-014b, 011b and 013 had not filed at the start of this card. This card used 014, 009, 009b and 011 and named that. The 009b Kc restatement does not change the 014 leaders, which already carry Kc and sit on the crimping branch.",
  "direction": "Revisit if 014b or 011b lands a better point.",
  "effect": "The three best P2 points could change under 014b."
}
```

### N367 — NFI-030-HELD-020

Source `rpt-mainline030-opus-register-1020`; original file `unpublished-local-ref:ef1ee16a8d48401a; pointer `/rows/4`.

```json
{
  "id": "NFI-030-HELD-020",
  "state": "recorded",
  "owner": "ref-55cff924be25afe6f9dd",
  "note": "This seat finished a 020 check before it read the narrowing that moved 020 to ref-4189c1615990eb515921. The report was pulled from the outbox before ingest and is held unfiled at .ship/held/rpt-check020-opus-1020.json; its only new result (019's reserve at 020's stock and film, 1154.23 kg) is carried in R038 and agrees with 021b."
}
```

### N390 — NFI-023-CHECK-FIRST-PINS

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/0`.

```json
{
  "id": "NFI-023-CHECK-FIRST-PINS",
  "status": "open",
  "non_blocking": true,
  "field": "first report artifacts",
  "reported": "Five paths pinned under the initial973.7kN report.",
  "check": "All five now contain load-fix bytes. Current load-fix pins match; original full files unavailable at cited paths.43 preserved report quantities reconstruct.",
  "evidence": [
    "inputs/pin-audit.json",
    "REPORT-CHECK.csv"
  ],
  "next": "Preserve distinct immutable version paths on future fixes; restore original versions only if already archived, without substituting reconstructed data."
}
```

### N396 — NFI-023-CHECK-BRAZE-UNITS

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/6`.

```json
{
  "id": "NFI-023-CHECK-BRAZE-UNITS",
  "status": "open",
  "non_blocking": true,
  "field": "mass_coefficients.sic_braze.C_end_per_area_1_per_N",
  "reported": "Coefficient labelled1/N in JSON and CARD.",
  "check": {
    "value": 1.9735212943395024e-05,
    "correct_units": "kg/(N*m), equivalently s^2/m^2",
    "equation": "m_end=C*A*N/r"
  },
  "evidence": [
    "dimensional derivation CHECK.md"
  ],
  "next": "Correct units and field label. Numeric coefficient itself is reproduced."
}
```

### N420 — NFI-CHK024-INPUT-RECORD

Source `rpt-ref-7d6892c4e55be16ad523`; original file `unpublished-local-ref:0d655e2d18e3e532; pointer `/open/9`.

```json
{
  "id": "NFI-CHK024-INPUT-RECORD",
  "kind": "reproducibility gap repaired locally",
  "tag": "QUESTIONABLE",
  "finding": "Owner INPUTS primarily pins sources and upstream scripts; explicit gas constants and complete material/frame values are missing. This check supplies them and a fresh standalone calculation.",
  "proposed_next": "Carry explicit constants and non-code formula records with the next filing."
}
```

### N453 — kommers

Source `rpt-mainline032-grok-wrinkle-waviness-1020`; original file `unpublished-local-ref:e20bd8d3e1ca97e2; pointer `/open/7`.

```json
{
  "id": "kommers",
  "tag": "QUESTIONABLE",
  "note": "The card names Norris, Ericksen and Kommers. FPL Report 1810 is Norris, Ericksen and March. Kommers was not found on it."
}
```

### N474 — NFI-015-CHECK-PROJECTION-TAGS

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/8`.

```json
{
  "id": "NFI-015-CHECK-PROJECTION-TAGS",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "not_revisited_outside_focused_map",
  "reported": "015b maps only Al and Be, with QUESTIONABLE retained.",
  "checked": "The old CNT and graphene rows requiring PROJECTION tags are omitted rather than corrected. No new CNT or graphene result is claimed.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Retain per-material PROJECTION tags through the mapped tolerance results."
}
```

### N475 — NFI-015-CHECK-PNAS-CONSISTENCY

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/9`.

```json
{
  "id": "NFI-015-CHECK-PNAS-CONSISTENCY",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "not_revisited_outside_focused_map",
  "reported": "015b does not use the PNAS stochastic estimate.",
  "checked": "The earlier mean/quantile/support inconsistency is neither repeated nor reconciled. The earlier reliability claim remains unresolved.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Reconcile distribution parameters and count conventions before interpreting reliability. Preserve the below-range R/t extrapolation warning."
}
```

### N481 — NFI-030-DOUBLE-CITE

Source `rpt-ref-490f8e9228d526b69dc8`; original file `unpublished-local-ref:67de0b610c731495; pointer `/rows/1`.

```json
{
  "id": "NFI-030-DOUBLE-CITE",
  "issue": "Unique source ids are 362 and source pointers are 363. N023, row NFI-CHK011B-TEXT, is cited on R057 and on R079. The source note contains the two-way shear objection and the documentation defects together.",
  "consequence": "No source row is missing. The same note was filed under both subjects.",
  "next": "None."
}
```

### N504 — NFI-026-06

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/5`.

```json
{
  "id": "NFI-026-06",
  "tag": "QUESTIONABLE",
  "status": "diagnostic_resolved_by_replacement",
  "owner": "sciences",
  "issue": "Whole-tangent linearization failed mesh convergence",
  "evidence": "Exact and finite-difference derivatives agree while first lambda drifts 6.58993, 6.39856, 6.18053, 5.60237.",
  "implication": "Rejected as primary linear buckling. Standard initial-stress calculation converges; full nonlinear calculations receive their own mesh comparison."
}
```

### N510 — NFI-026-12

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/11`.

```json
{
  "id": "NFI-026-12",
  "tag": "QUESTIONABLE",
  "status": "execution_disclosed",
  "owner": "sciences",
  "issue": "Execution diagnostics and receipt exception",
  "evidence": "One 3 GiB mixed-factor benchmark was OOM-killed and released; 8 GiB check passed. Four diagnostic scopes were stopped/released. ref-60b5e906764ecf85edea child exited0/released while outer wrapper END was missing.",
  "implication": "All diagnostics retained; recovered child receipt distinguishes observed closure from unavailable exact outer end clock. No admission refusal was bypassed."
}
```

### N527 — NFI-035-PALETTE

Source `rpt-mainline035-opus-knockdown-tests-1020`; original file `unpublished-local-ref:4d5781abcddc2e1c; pointer `/rows/9`.

```json
{
  "id": "NFI-035-PALETTE",
  "state": "recorded",
  "note": "The chart uses the dataviz skill's documented passing slots 1-3; its validator could not run here (no JavaScript runtime). Marker shapes carry identity as well."
}
```

### N536 — NFI-032-CHECK-LEAD-RANGE

Source `rpt-ref-a30a669ed3e245f1473b`; original file `unpublished-local-ref:46e93c1ee5674acc; pointer `/findings/8`.

```json
{
  "id": "NFI-032-CHECK-LEAD-RANGE",
  "status": "correction",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "CARD says lead amplitudes span 0.0046–0.024 of the 9.525 mm cell.",
  "checked": "The lead-only ratios are 0.006847549228760197 and 0.01604921436707204. The printed endpoints are the two cross-Q rows among all four 60 psi cases. The underlying four rows are correct.",
  "followup": "Change the label to all four typical-strength cases, or use the lead-only range.",
  "source_audit_ids": [],
  "owner_nfi_ids": [],
  "exact_values": {
    "id": "NFI-032-CHECK-LEAD-RANGE",
    "field": "CARD lead amplitude / 9.525 mm cell range",
    "reported": [
      0.0046,
      0.024
    ],
    "checked": [
      0.006847549228760197,
      0.01604921436707204
    ],
    "all_four_typical_rows": [
      0.004594587314516719,
      0.02391896767621028
    ],
    "reason": "The reported endpoints round the two cross-Q rows; the lead-specific range uses Q .371 on S-200F and Q .609 on SR-200."
  }
}
```

### N651 — NFI-038-SOURCE_STATE

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/0`.

```json
{
  "id": "NFI-038-SOURCE_STATE",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "P3 optimum changed during the card",
  "evidence": "022d supersedes 022c; 034 uses older inventories.",
  "resolution_needed": "Use P3-LATEST for a buy; re-inventory vacuum at final selected geometry.",
  "tests": [
    "T4",
    "T5",
    "T6",
    "T8",
    "T9"
  ]
}
```

### N677 — NFI-C035-CTA83

Source `rpt-ref-d3afcdc3514000cb6fc2`; original file `unpublished-local-ref:c6b42f055193d816; pointer `/rows/4`.

```json
{
  "id": "NFI-C035-CTA83",
  "status": "open",
  "tag": "QUESTIONABLE",
  "issue": "The source's printed 0.864 conflicts with 432000/499246=0.8653048798.",
  "next_evidence": "Resolve the precise reference load or rounding convention in NASA/TM-20210024768. Retain both alternatives explicitly until then.",
  "evidence": [
    "E05",
    "AUXILIARY.json"
  ],
  "blocks_card": false
}
```

### B005 — NFI-030B-EVIDENCE-LABEL

Source `rpt-ref-39745602983887568501`; original file `unpublished-local-ref:534f72d6d7dd0ad8; pointer `retained original identity`.

```json
{
  "id": "NFI-030B-EVIDENCE-LABEL",
  "title": "A demonstrated source-contract correction is not a demonstrated hull capability.",
  "finding": "The Zylon directional factor is a demonstrated arithmetic/source mismatch in CHECK-022b/022c. New correction, measured coupon precedent, source absence and projected assembly capability remain distinct in this register.",
  "status": "OPEN",
  "blocks_progress": false
}
```

### C001 — NFI-022D-CHECK-01

Source `rpt-ref-4b8e7b08241bb7a45536`; original file `unpublished-local-ref:2fa44902593248ea; pointer `/rows/0`.

```json
{
  "id": "NFI-022D-CHECK-01",
  "owner": "MAINLINE-022d",
  "state": "open precision fix",
  "kind": "document/output numerical mismatch",
  "evidence": "SENSITIVITIES.two_way_square_cell[16:32], FIELD-CHECKS.json, MISMATCHES.csv",
  "note": "Sixteen square-membrane rows imply coefficient 0.07028850698306077; INPUTS/METHOD declare 0.07028850747757764. All 50 strict field mismatches arise from this difference. Maximum least-SF effect is 3.976191154109188e-9 and maximum sag-mass effect is 3.634157224041701e-6 kg. Primary witnesses are unaffected.",
  "settle": "State the actual coefficient and series truncation consistently, or regenerate square-membrane sensitivity rows with the declared coefficient.",
  "stops_other_work": false
}
```

### C058 — /resolved_source_findings/0

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/resolved_source_findings/0`.

```json
"FAA 78-to-70-knot history is resolved by Appendix B, not a remaining document conflict."
```

### C059 — /resolved_source_findings/1

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/resolved_source_findings/1`.

```json
"FAA VB lower bound includes the 0.65 VH alternative; design airspeeds are EAS."
```

### C060 — /resolved_source_findings/2

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/resolved_source_findings/2`.

```json
"The SR-200 manufacturer's own sheet supports typical 11.3 ppm/K thermal expansion."
```

### C102 — NFI-CHECK038-ROUNDING

Source `rpt-ref-2beb70a569266cf0297d`; original file `unpublished-local-ref:0746af9cb88f6eb1; pointer `/items/0`.

```json
{
  "id": "NFI-CHECK038-ROUNDING",
  "status": "OPEN",
  "blocking": false,
  "issue": "Two historical 022c end masses use rounded joint coefficients.",
  "evidence": "SUPPLEMENT.json lists owner and unrounded values, exact coefficients and assembly impact.",
  "resolution_needed": "Use 1550/(2π·1470e6·28.9e6) and 4430/(2π·827e6·28.9e6) in the next regeneration, or label the coefficient precision.",
  "tests": [
    "T6"
  ],
  "classification": "minor numerical precision"
}
```

### C105 — NFI-CHECK038-CSV_HEADING

Source `rpt-ref-2beb70a569266cf0297d`; original file `unpublished-local-ref:0746af9cb88f6eb1; pointer `/items/3`.

```json
{
  "id": "NFI-CHECK038-CSV_HEADING",
  "status": "OPEN",
  "blocking": false,
  "issue": "A P2 CSV heading describes fixed other modes but its values are conditional minima.",
  "evidence": "The gamma=0.2 row contains 0.354507, while the other modes stay at one. METHOD describes the correct min(affected,1) operation.",
  "resolution_needed": "Rename fixed_P2_all_other_named_modes_at_threshold_SF to conditional_least_P2_SF_with_other_modes_fixed_at_threshold. Keep the values.",
  "tests": [
    "T1",
    "T2",
    "T3",
    "T7"
  ],
  "classification": "presentation fix"
}
```

### C106 — NFI-CHECK038-STANDARD_EDITION

Source `rpt-ref-2beb70a569266cf0297d`; original file `unpublished-local-ref:0746af9cb88f6eb1; pointer `/items/4`.

```json
{
  "id": "NFI-CHECK038-STANDARD_EDITION",
  "status": "OPEN",
  "blocking": false,
  "issue": "F1249-20 is cited although ASTM identifies F1249-25 as active.",
  "evidence": "The official F1249-20 version list and the retrieved F1249-25 page confirm the edition difference. No procedural difference is asserted.",
  "resolution_needed": "Select and record the executing lab's controlled edition. Preserve C365 as compression/modulus evidence; it does not characterize compressive core crush.",
  "tests": [
    "T2",
    "T3",
    "T4"
  ],
  "classification": "protocol clarification"
}
```

### C133 — C039-07

Source `rpt-ref-20ab4b33b504a00ad3b6`; original file `unpublished-local-ref:75b66f0986a98c9b; pointer `/rows/6`.

```json
{
  "id": "C039-07",
  "topic": "STA8p1-MODEL-IDENTITY",
  "status": "REVISE",
  "objection": "LIT-STIFF treats the 759,000 and 754,000 lb predictions as conflicting source values.",
  "evidence": "STA8.1 PDF p4 distinguishes geometry refinement from the additional nonuniform-loading refinement. Relative errors against 743,000 lb are 2.153% and 1.480%.",
  "proposed_fix": "Assign separate model identities to the two predictions. Flag the intermediate model's incorrect 1.5% prose label. Clarify total versus web stiffener height instead of declaring an unexplained geometry contradiction.",
  "disposition": "Record for owner revision; check completed"
}
```

### C135 — C039-09

Source `rpt-ref-20ab4b33b504a00ad3b6`; original file `unpublished-local-ref:75b66f0986a98c9b; pointer `/rows/8`.

```json
{
  "id": "C039-09",
  "topic": "INPUT-COMPLETENESS",
  "status": "REVISE",
  "objection": "Several numeric choices are recoverable but missing from the supplied inputs or compact geometry.",
  "evidence": "METHOD.md: fillet density 1250 kg/m3 inferred from mass. SUPPLEMENTARY.json: calibration nu=.33/.35. Four gs5 compact rows omit shape and required psi-based recovery.",
  "proposed_fix": "Publish these inputs and each chosen section's shape with units and provenance. Keep all independent check limitations visible. Preserve measured elapsed values; their microsecond timestamp differences are harmless.",
  "disposition": "Record for owner revision; check completed"
}
```

### C220 — NFI-CHECK037b-INTERLAYER-COUNT

Source `rpt-ref-4bf25e71ae0c2ca315e2`; original file `unpublished-local-ref:0360eb0aa78daa3e; pointer `/items/5`.

```json
{
  "id": "NFI-CHECK037b-INTERLAYER-COUNT",
  "tag": "QUESTIONABLE",
  "status": "OPEN",
  "finding": "The inherited rigid screen adds one interlayer compliance while the symmetric edge/global model adds both interfaces. A consistent two-interface version halves the rigid-screen thickness requirement.",
  "exact": {
    "owner_rigid_screen_each_layer_m": 0.0055061042526840685,
    "symmetric_two_interface_each_layer_m": 0.0027530521263420342,
    "symmetric_total_mass_kg": 10309.570255398545,
    "note": "Changing the old screen to include both interfaces halves its required thickness. Both versions are far over budget."
  },
  "disposition": "State the topology explicitly. Neither 20.619 t nor the symmetric 10.310 t sensitivity can float; no change to the selected route.",
  "blocking": false
}
```

### C221 — NFI-CHECK037b-DIAGNOSTIC-SCHEMA

Source `rpt-ref-4bf25e71ae0c2ca315e2`; original file `unpublished-local-ref:0360eb0aa78daa3e; pointer `/items/6`.

```json
{
  "id": "NFI-CHECK037b-DIAGNOSTIC-SCHEMA",
  "tag": "QUESTIONABLE",
  "status": "OPEN",
  "finding": "Some rows set feasible=true while named usage exceeds one. Failed rows also contain zero geometry, NaN and Infinity. Several rejected nonmetal solutions have core depths of only 0.016–0.076 mm, outside the supplied core data.",
  "disposition": "Distinguish local-constraint feasibility from a design inside the named stretch, encode nonfinite values as null plus an infeasibility reason, and keep failed-solve trial coordinates out of build dimensions. Independent broader-envelope searches confirm the rejection.",
  "blocking": false
}
```

### C222 — NFI-CHECK037b-MASS-ALONE-WORDING

Source `rpt-ref-4bf25e71ae0c2ca315e2`; original file `unpublished-local-ref:0360eb0aa78daa3e; pointer `/items/7`.

```json
{
  "id": "NFI-CHECK037b-MASS-ALONE-WORDING",
  "tag": "QUESTIONABLE",
  "status": "OPEN",
  "finding": "The glass/aramid rejections involve their specified mechanical properties and the fixed scarf, not density alone. An artificial ideal-property core at the HFT density can pass the broader classical envelope.",
  "exact": {
    "HFT_density_kg_m3": 32.04,
    "actual_HFT_classical_maximum_minimum_SF": 0.9738619550030646,
    "ideal_properties_same_density_classical_maximum_minimum_SF": 1.0249018707576047
  },
  "disposition": "Narrow 'mass alone' to the metallic density bounds that were actually proven. No sourced nonmetal candidate becomes feasible.",
  "carries_owner_rows": [
    "NFI-037b-NONMETAL-CTE",
    "NFI-037b-RT-PASTE"
  ],
  "blocking": false
}
```

### C223 — NFI-CHECK037b-L-PRECISION

Source `rpt-ref-4bf25e71ae0c2ca315e2`; original file `unpublished-local-ref:0360eb0aa78daa3e; pointer `/items/8`.

```json
{
  "id": "NFI-CHECK037b-L-PRECISION",
  "tag": "ROUNDING",
  "status": "OPEN",
  "finding": "The L-direction branch mixes rounded 103.42 MPa/379.21 kPa inputs with exact-PSI conversions elsewhere. This produces 14 distinct precision differences, repeated twice in the verdict.",
  "disposition": "Use one stated conversion convention or reduce reported digits. All fourteen values reproduce when the published rounded L inputs are used. W remains governing.",
  "evidence": "EXACT-DIFFERENCES.csv; SUPPLEMENT.json/rounded_L_replication",
  "blocking": false
}
```

### S007 — NFI-030C-NONFINITE-SOURCE

Source `rpt-1228-mainline030c-design-register-1020`; original file `unpublished-local-ref:3c01fd6db28be861; pointer `/rows/6`.

```json
{
  "id": "NFI-030C-NONFINITE-SOURCE",
  "title": "Some 037b infeasible alternatives contain nonstandard JSON Infinity/NaN.",
  "finding": "Original source bytes remain pinned verbatim. The current selected finite points are exported as strict JSON. Infeasible alternatives remain referenced with their explicit source disposition; nonfinite entries are not interpreted as capabilities.",
  "status": "OPEN",
  "blocks_progress": false,
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## R080 — equal-mass separation convention

**Original question:** Whether face separation should follow face thickness when face density changes at equal mass; effect is second order against 0.1-0.16 m cores.

### N124 — NFI-005-SEP

Source `rpt-ref-eb07faa637b7487d6dc5`; original file `unpublished-local-ref:2ef2c84bad6b0b03; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-005-SEP",
  "gap": "P2 equal-mass figure holds face separation at the row value while face thickness follows 1/rho. A changed face density moves tf and so moves separation by the same amount, a second-order change against 0.1-0.16 m cores.",
  "direction": "Recompute E/rho with separation following tf if a candidate face material is far from 2700 kg/m3.",
  "effect": "Small optimistic or pessimistic shift in the P2 buckling figure for extreme densities."
}
```

### N141 — NFI-008B-SEP

Source `rpt-ref-cc9cef5e55adca018a8f`; original file `unpublished-local-ref:2bbb739a4c037482; pointer `retained original identity`.

```json
{
  "id": "NFI-008B-SEP",
  "inherited": "NFI-005-SEP (carried through 008)",
  "issue": "At equal face mass the face-thickness change moves the separation slightly; the first-order scaling drops that term. The 008 checker measured the effect at most 0.348 percent of SF_b on P2-E (worst tf/d 0.00722).",
  "consequence": "Negligible against the 2-10x gaps this card reports.",
  "next": "None alone; folds into any future exact recompute."
}
```

### N471 — NFI-015-CHECK-ONE-FACE

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/5`.

```json
{
  "id": "NFI-015-CHECK-ONE-FACE",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "not_revisited_outside_focused_map",
  "reported": "015b contains no thickness-loss sensitivity calculation.",
  "checked": "The prior both-faces versus one-face labeling and local-patch distinction remain unrepaired in the earlier sensitivity section.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Say both faces for the inherited sensitivity; separate one-face changes and local-patch spatial response."
}
```

## R081 — omitted failure modes scope

**Original question:** Core shear, wrinkling, crush, laminate anisotropy, bond and thermal stress are omitted; SF_b is a first-order thin-face scaling.

### N127 — NFI-005-OMITTED

Source `rpt-ref-eb07faa637b7487d6dc5`; original file `unpublished-local-ref:2ef2c84bad6b0b03; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-005-OMITTED",
  "gap": "Core shear, face wrinkling, core crush, local crippling and end fixity remain outside these two limits, as in 002/003. Core crush is worked next as MAINLINE-005b.",
  "direction": "005b for crush; later cards for shear, wrinkling and crippling.",
  "effect": "Any omitted mode can only lower a row's true SF below the figures here."
}
```

### N135 — NFI-008-OMITTED-MODES

Source `rpt-ref-45da79edf548b064b228`; original file `unpublished-local-ref:20c691c11e9fda46; pointer `retained original identity`.

```json
{
  "id": "NFI-008-OMITTED-MODES",
  "issue": "Core shear, face wrinkling, core crush, laminate anisotropy (nu, shear), face-core bond and thermal stress are omitted, as in 002/003; equal face mass holds the pinned core and separation fixed.",
  "effect": "SF_b is a first-order tf<<d scaling; a candidate whose tf approached d, or whose nu differs strongly, would need the full sandwich formulas.",
  "needed": "MAINLINE-004 knockdown for kd rescaling, and a sandwich failure check per candidate."
}
```

### N400 — NFI-023-CHECK-SOURCE-AND-TAGS

Source `rpt-ref-f4daf73c940b6f527d37`; original file `unpublished-local-ref:9c008dc949c3c4a8; pointer `/findings/10`.

```json
{
  "id": "NFI-023-CHECK-SOURCE-AND-TAGS",
  "status": "open",
  "non_blocking": true,
  "field": "material allowable transfer and result labels",
  "reported": "Nominal coupon strengths and inherited density are used as joint design values; overallRESULTS tagQUESTIONABLE.",
  "check": "1470MPa cited Toray coupon is verified, as are Henkel/TIMET/Invar values. The fabricated transition, its layup, complete node and film remain PROJECTION. Producer data vary by resin/version and typical/minimum basis.",
  "evidence": [
    "INPUTS.json source_audit",
    "primary PDFs"
  ],
  "next": "Keep source version, test basis, material density and joint state explicit in each downstream row; do not promote the sizing to a qualified joint."
}
```

### N552 — NFI-036-installed-hull

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/14`.

```json
{
  "id": "NFI-036-installed-hull",
  "status": "OPEN",
  "issue": "Establish installed capacity including unmodeled local failures.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "installed_SF": ">= project requirement"
  },
  "today": {
    "installed_SF": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "027; 028b; this card",
  "closure": "Close bond, peel, fracture, local instability, defect, thermal and leak modes and validate the joined geometry; model SF=1 is not certification."
}
```

### N588 — NFI-034-STRUCTURAL-CARRY

Source `rpt-ref-244f32e2449e729d312f`; original file `unpublished-local-ref:5604e2c976f39c2f; pointer `/open/16`.

```json
{
  "id": "NFI-034-STRUCTURAL-CARRY",
  "tag": "QUESTIONABLE",
  "finding": "This is a vacuum-maintenance estimate at fixed inherited points. The 022c Kapton equilateral row has filed least SF below one; Zylon structural assumptions and P2 optimism remain unqualified.",
  "proposed_next": "Carry the existing structural NFI; vacuum arithmetic does not establish a floating or certified hull."
}
```

### N618 — NFI-026B-04

Source `rpt-ref-8befdd4c89803adc44a8`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/3`.

```json
{
  "id": "NFI-026B-04",
  "tag": "QUESTIONABLE",
  "status": "unresolved",
  "owner": "sciences",
  "issue": "New nonlinear first instability not verified",
  "evidence": "Nearest-zero triplets can skip an already-negative family. Frequency4 has eta 0.000165 at lambda  5.059945, then reports positive nearest-zero modes at5.080744. Raw final zero 5.082444 is not accepted as first loss; frequency 2 zero 2.218113 lacks an independent smallest-algebraic check.",
  "implication": "Freshly authorized smallest-algebraic or inertia checks must find and refine earliest tangent loss. Do not use raw critical_lambda_estimate as a first-instability allowable."
}
```

### N644 — NFI-026B-04

Source `rpt-ref-4a20323946ecafd56a6b`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/3`.

```json
{
  "id": "NFI-026B-04",
  "tag": "QUESTIONABLE",
  "status": "unresolved",
  "owner": "sciences",
  "issue": "New nonlinear first instability not verified",
  "evidence": "Nearest-zero triplets can skip an already-negative family. Frequency4 has eta 0.000165 at lambda  5.059945, then reports positive nearest-zero modes at5.080744. Raw final zero 5.082444 is not accepted as first loss; frequency 2 zero 2.218113 lacks an independent smallest-algebraic check.",
  "implication": "Freshly authorized smallest-algebraic or inertia checks must find and refine earliest tangent loss. Do not use raw critical_lambda_estimate as a first-instability allowable."
}
```

### N670 — NFI-038-RELIABILITY

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/19`.

```json
{
  "id": "NFI-038-RELIABILITY",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Screening count is not a design allowable or mission qualification",
  "evidence": "Three to ten specimens only screen large errors; size/lot/lifetime transfer unresolved.",
  "resolution_needed": "Define required reliability and confidence, then qualify lots, environments, damage and life.",
  "tests": [
    "T1",
    "T2",
    "T3",
    "T4",
    "T5",
    "T6",
    "T7",
    "T8",
    "T9"
  ]
}
```

### N703 — NFI-036-installed-hull

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/14`.

```json
{
  "id": "NFI-036-installed-hull",
  "status": "OPEN",
  "issue": "Establish installed capacity including unmodeled local failures.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "installed_SF": ">= project requirement"
  },
  "today": {
    "installed_SF": null
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "027; 028b; this card",
  "closure": "Close bond, peel, fracture, local instability, defect, thermal and leak modes and validate the joined geometry; model SF=1 is not certification.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### C077 — NFI-034-STRUCTURAL-CARRY

Source `rpt-ref-025def9d3634f5e320d7`; original file `unpublished-local-ref:678c175adb0bf787; pointer `/open/16`.

```json
{
  "id": "NFI-034-STRUCTURAL-CARRY",
  "tag": "QUESTIONABLE",
  "finding": "This is a vacuum-maintenance estimate at fixed inherited points. The 022c Kapton equilateral row has filed least SF below one; Zylon structural assumptions and P2 optimism remain unqualified.",
  "proposed_next": "Carry the existing structural NFI; vacuum arithmetic does not establish a floating or certified hull.",
  "carried_from": "MAINLINE-034 owner NFI.json; independently retained, no physical closure claimed"
}
```

### C113 — NFI-029-AXISYMMETRY

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/3`.

```json
{
  "id": "NFI-029-AXISYMMETRY",
  "status": "open",
  "title": "Only axisymmetric lead modes",
  "issue": "Lead model excludes nonaxisymmetric and cell-scale modes. With L in the meridian the weaker W is circumferential and can trigger excluded modes. L orientation results are not full3D hull capacity.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C123 — NFI-029-RIBBON-FIELD

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/13`.

```json
{
  "id": "NFI-029-RIBBON-FIELD",
  "status": "open",
  "title": "Ribbon topology and bonding",
  "issue": "L/W meridian orientation is an ideal smooth spherical field, with unavoidable pole singularities and no manufacturable panel-ribbon layout. Shared solid nodes impose a perfect bond.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C159 — NFI-041-07

Source `rpt-ref-c7dfc45babe1b96007db`; original file `unpublished-local-ref:cd543374666d8c21; pointer `/items/6`.

```json
{
  "id": "NFI-041-07",
  "status": "open",
  "topic": "Beam idealization and initial bending coupling",
  "evidence": [
    "METHODS.md",
    "frame_tools.py:response",
    "run_verified_nonlinear.py"
  ],
  "finding": "The linear eigenproblem uses segment compression geometric stiffness plus the conservative pressure Hessian; it omits initial-moment coupling. The separate corotational nonlinear selected-frame calculation includes the elastic tangent. Euler-Bernoulli circular beams do not resolve local shell ovalization, shear deformation, joints, contact or composite/ceramic defects.",
  "needed": "Cross-check with independently formulated beam/shell models and benchmark problems; resolve the relevant local and joint physics rather than treating mesh convergence alone as model validation."
}
```

### C212 — NFI-043-14

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/13`.

```json
{
  "id": "NFI-043-14",
  "status": "open",
  "topic": "System risk budget and dependence",
  "finding": "Headline targets allocate the entire risk budget to tube fracture and use an independent series model. Joints, membrane, instability, shared batches and common-cause events are omitted.",
  "needed": "A whole-frame failure definition and allocated risk budget; valid component marginals and dependence/common-cause model.",
  "effect": "The conditional series probabilities are not whole-vehicle reliability claims. Union-bound allocations avoid independence but do not supply missing marginal probabilities.",
  "stops_other_work": false
}
```

## R082 — optimiser resolution and scope (grid vs continuous, splits, knees)

**Current 030c:** CHECK-039 supplies constructive points better than the filed grid: C2b/O6 fixed-mass SF .699691806 and +1127.071353 kg to SF 1.00000108. These are attained values, not certified global optima or a proof of impossibility.

**Original question:** General instability now includes transverse shear; the 007 thickness splits were not re-searched, which matters only for a named core whose Kc moves the equal-factor point.

### N005 — NFI-OPTIMUM-RESOLUTION

Source `rpt-1228-mainline009c5-independent-check-1019`; original file `unpublished-local-ref:52f757339520e0fd; pointer `retained original identity`.

```json
{
  "id": "NFI-OPTIMUM-RESOLUTION",
  "type": "estimate_resolution",
  "row": "optimum",
  "field": "least_SF",
  "reported": 0.6504118436805308,
  "independent_continuous_balance": 0.6504130224098148,
  "independent_fraction": 0.19176846298505057,
  "proposed_fix": "Label the filed point as a finite search result; optional refinement only.",
  "stops_owner": false
}
```

### N006 — NFI-OTHER-BRANCH-RESOLUTION

Source `rpt-1228-mainline009c5-independent-check-1019`; original file `unpublished-local-ref:52f757339520e0fd; pointer `retained original identity`.

```json
{
  "id": "NFI-OTHER-BRANCH-RESOLUTION",
  "type": "estimate_resolution",
  "row": "other_branch",
  "field": "least_SF",
  "reported": 0.175022781624177,
  "independent_boundary_limit": 0.17502890484090416,
  "proposed_fix": "Label grid resolution; the small refinement changes no decision.",
  "stops_owner": false
}
```

### N017 — NFI-GRID-RESOLUTION

Source `rpt-1228-mainline014b-independent-check-1019`; original file `unpublished-local-ref:8f2d079b76102928; pointer `retained original identity`.

```json
{
  "id": "NFI-GRID-RESOLUTION",
  "type": "estimate_resolution",
  "row": "all optima",
  "field": "optimality",
  "reported": "best",
  "independent": "Reproduced on j/8000 finite grid, not a continuous optimality proof.",
  "proposed_fix": "Label grid optima and retain the reported precision as computational precision.",
  "stops_owner": false
}
```

### N027 — NFI-CHK019-014B-GRID

Source `rpt-check019-opus-1020`; original file `unpublished-local-ref:391c78ac32ab1335; pointer `retained original identity`.

```json
{
  "id": "NFI-CHK019-014B-GRID",
  "state": "not reproduced",
  "direction": "minor",
  "note": "014b's grid value 0.668649769508548 needs 014b's unstated core-fraction grid. Seven regular grids land 5e-5 to 8e-4 away. The card's continuous 0.668710748 is reproduced."
}
```

### N037 — NFI-RULE

Source `rpt-ref-05310d05f1fb52d6522e`; original file `unpublished-local-ref:9fb5e0d7bd10917b; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-RULE",
  "gap": "The splits are an optimum of knocked-down buckling and QUESTIONABLE yield on the ceiling. They are not an optimum once shear, wrinkling, or crush enter the stated factor.",
  "direction": "Recompute after MAINLINE-007b.",
  "effect": "Another limit would move both thicknesses."
}
```

### N043 — NFI-SAND

Source `rpt-ref-3dd5ab5528276031581d`; original file `unpublished-local-ref:474808f25f6dc0cd; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SAND",
  "gap": "General instability now includes transverse shear and matches the kd 0.2 pressure when shear stiffness is infinite. The 007 splits were not searched again.",
  "direction": "A new split search would matter only for a named core whose Kc moves the equal-factor point.",
  "effect": "On the reported rows, buckling still governs after the trim except where honeycomb wrinkling is admitted."
}
```

### N254 — NFI-FLOAT-ALLOCATION-CARRY

Source `rpt-mainline002-grok-strength-card-1019`; original file `unpublished-local-ref:f02996967e2f160d; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-FLOAT-ALLOCATION-CARRY",
  "gap": "Each alternative spends the baseline margin on one thickness. Residual margin is numerical zero by that rule. It is not an optimum and not a search over families.",
  "direction": "A later card can compare other single changes, including core thickness and tube radius.",
  "effect": "The allocation changes both stiffness and strength pressures through the named thickness."
}
```

### N270 — NFI-RULE

Source `rpt-mainline003-grok-p2-targets-1019`; original file `unpublished-local-ref:c644022670e558c3; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-RULE",
  "gap": "Equal mass, core-only and proportional scale are stated rules. They are not an optimum and not the advisory search.",
  "direction": "Do not read the equal-mass point as a proved best split.",
  "effect": "Another rule would move both safety factors."
}
```

### N286 — NFI-KNEE

Source `rpt-mainline006-check-lead4f19-1019`; original file `unpublished-local-ref:5ea5fd1bf192b52a; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KNEE",
  "gap": "Confirmed: knee is the largest finite-difference drop per 100 kg on the tabulated margins, sorted by payload, not a fitted optimum.",
  "direction": "A denser margin grid if a smoother knee is needed.",
  "effect": "Owner statement stands."
}
```

### N290 — NFI-KNEE

Source `rpt-mainline006-grok-float-margin-1019`; original file `unpublished-local-ref:50c93f23f6adae0f; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-KNEE",
  "gap": "The knee is the tabulated interval with the largest drop in least SF per 100 kg of payload. It is a finite difference on these margins, not a fitted optimum.",
  "direction": "A denser margin grid if a later card needs a smoother knee.",
  "effect": "The named knee can move if margins are added between 0 and 5 percent."
}
```

### N301 — NFI-SAND

Source `rpt-mainline007b-check-lead4f19-1019`; original file `unpublished-local-ref:c88bee0b56cece84; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-SAND",
  "gap": "Confirmed: general instability includes transverse shear and restores the kd 0.2 classical pressure at infinite shear (Kc=1). The 007 splits were not re-searched.",
  "direction": "A new split search only for a named core whose Kc moves the equal-factor point.",
  "effect": "Owner statement stands."
}
```

### N354 — NFI-017-COMBO

Source `rpt-mainline017-improvement-directions-lead4f19-1019`; original file `unpublished-local-ref:b586b896a14aa878; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-017-COMBO",
  "gap": "The cheapest combination is a product-minimising differential-evolution search on a 900-point depth grid, seeded, not a proof of global optimality. In all three P2 points it returns face density alone, at products 1.474, 1.657 and 1.685 on the grid against continuous single factors 1.459, 1.637 and 1.655.",
  "direction": "An analytic product bound if a later card needs to beat these products.",
  "effect": "Split statements read as 'cheapest found'."
}
```

### N461 — NFI-C022-SEARCH-RESOLUTION

Source `rpt-ref-f6de390e1555b4ca8e78`; original file `unpublished-local-ref:a3c00555c78ad754; pointer `/rows/4`.

```json
{
  "id": "NFI-C022-SEARCH-RESOLUTION",
  "kind": "OPEN numerical integration improvement",
  "issue": "The reported optima are maxima of a grid with12 film gauges, not established continuous maxima.",
  "evidence": {
    "continuous": {
      "GAMMA/percent_crush_5": {
        "published": {
          "nodes": 40.364452148519376,
          "members": 115.09335644555813,
          "n_coef": 17.75352077758099,
          "m_nodes": 0.8072890429703875,
          "m_film": 348.8563570154232,
          "m_joint": 207.47771952536095,
          "m_tube": 3799.8907444488173,
          "reserve": 432.4100401574281,
          "sag_kg": 187.9379326479281,
          "vehicle": 4457.032110032572,
          "s_m": 6.15,
          "t_film_m": 0.00028619697756719387,
          "r_o_m": 0.16764593114772616,
          "t_w_m": 0.0016252746475689805,
          "rt": 103.14929319698926,
          "A_m2": 0.0017036852111210646,
          "I_m4": 2.3710194159910465e-05,
          "length_m": 6.251292310477491,
          "N_N": 1694765.969349715,
          "sigma_axial_Pa": 994764736.047993,
          "SF_least": 1.3752490300405402,
          "governing": "global",
          "k": 0.2,
          "SF_yield": 3.9205249831170557,
          "SF_euler": 1.4486696567430966,
          "SF_local": 1.3823277797176705,
          "SF_film": 1.4624665443017892,
          "SF_perry": 1.3888254730869978,
          "SF_global": 1.3752490300405402,
          "k04_SF_least": 1.3823277797176705,
          "k04_governing": "local",
          "k04_SF_global": 2.7504980600810804,
          "gamma": 0.5765839731705831,
          "SF_local_gamma1": 2.3974439874150075
        },
        "checker": {
          "nodes": 39.79828736770549,
          "members": 113.39486210311648,
          "n_coef": 17.88598787033534,
          "m_nodes": 0.7959657473541099,
          "m_film": 333.4229175126335,
          "m_joint": 207.41094379255415,
          "m_tube": 3813.999992591095,
          "m_end": 0.9145517704494558,
          "reserve": 433.81233054636164,
          "sag_kg": 189.34022303686163,
          "vehicle": 4455.629819643637,
          "s_m": 6.195887946996294,
          "r_o_m": 0.16854623707003225,
          "t_film_m": 0.0002735355951662727,
          "t_w_m": 0.0016342888242931817,
          "rt": 103.13124251028718,
          "A_m2": 0.0017223328180347105,
          "I_m4": 2.4227811394316333e-05,
          "length_m": 6.299535677779469,
          "N_N": 1707411.3890200634,
          "sigma_axial_Pa": 991336500.7863734,
          "k": 0.2,
          "gamma": 0.5766105003715992,
          "SF_local_gamma1": 2.406155884051259,
          "SF_least": 1.3874147482677335,
          "eta": 0.07547975705643792,
          "Euler_stress_Pa": 1434378046.166209,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.674184948280129,
          "NASA_L_over_midradius": 37.55779977077996,
          "SF_yield": 3.9340829243211988,
          "SF_euler": 1.4469133790881248,
          "SF_local": 1.387414748274864,
          "SF_film": 1.3874147482947616,
          "SF_perry": 1.3874147483075712,
          "SF_global": 1.3874147482677335,
          "governing": "global",
          "k04_governing": "local",
          "k04_SF_least": 1.387414748274864,
          "k04_SF_global": 2.774829496535467,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 991336500.7863734,
            "bending_Pa": 242253894.19448322,
            "maximum_compression_Pa": 1233590394.9808567,
            "opposite_signed_compression_Pa": 749082606.5918901,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.3874147482677335,
            "mean_compression_Pa": 1375394881.687142,
            "bending_Pa": 2524605116.510527,
            "maximum_compression_Pa": 3899999998.197669,
            "opposite_signed_compression_Pa": -1149210234.8233852,
            "maximum_tension_Pa": 1149210234.8233852
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6895,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.012165718227193256,
        "fractional_increase": 0.008846192915936468
      },
      "GAMMA/percent_crush_019": {
        "published": {
          "nodes": 40.364452148519376,
          "members": 115.09335644555813,
          "n_coef": 17.75352077758099,
          "m_nodes": 0.8072890429703875,
          "m_film": 344.14447412660274,
          "m_joint": 199.53358445097274,
          "m_tube": 3645.719925849878,
          "reserve": 599.2368767195755,
          "sag_kg": 187.9379326479281,
          "vehicle": 4290.205273470424,
          "s_m": 6.15,
          "t_film_m": 0.00028233141337633867,
          "r_o_m": 0.16557534691311998,
          "t_w_m": 0.0015787064452148225,
          "rt": 104.88038952079486,
          "A_m2": 0.0016345625543664846,
          "I_m4": 2.2193311326653455e-05,
          "length_m": 6.251292310477491,
          "N_N": 1694765.969349715,
          "sigma_axial_Pa": 1036831514.8431647,
          "SF_least": 1.2986375988562109,
          "governing": "local",
          "k": 0.2,
          "SF_yield": 3.761459739762954,
          "SF_euler": 1.3559896002849583,
          "SF_local": 1.2986375988562109,
          "SF_film": 1.4427135114359915,
          "SF_perry": 1.3013105709566732,
          "SF_global": 1.303259624628275,
          "k04_SF_least": 1.2986375988562109,
          "k04_governing": "local",
          "k04_SF_global": 2.60651924925655,
          "gamma": 0.574057435367821,
          "SF_local_gamma1": 2.2622084809756418
        },
        "checker": {
          "nodes": 40.352064989035384,
          "members": 115.05619496710615,
          "n_coef": 17.756387610681262,
          "m_nodes": 0.8070412997807077,
          "m_film": 314.1079387781873,
          "m_joint": 199.53213930050447,
          "m_tube": 3675.7278059321206,
          "m_end": 0.8671073268047386,
          "reserve": 599.267224879406,
          "sag_kg": 187.96828080775856,
          "vehicle": 4290.174925310594,
          "s_m": 6.150993100117297,
          "r_o_m": 0.16590681718903877,
          "t_film_m": 0.00025768985113894304,
          "t_w_m": 0.0015888018364025086,
          "rt": 104.42259908554624,
          "A_m2": 0.0016482737204869182,
          "I_m4": 2.246822983498277e-05,
          "length_m": 6.252335987104578,
          "N_N": 1695039.6396396263,
          "sigma_axial_Pa": 1028372665.6388679,
          "k": 0.2,
          "gamma": 0.5747222400996512,
          "SF_local_gamma1": 2.2908153472246613,
          "SF_least": 1.3165825280040278,
          "eta": 0.07609690900763422,
          "Euler_stress_Pa": 1411037349.1917076,
          "mass_closure_kg": 4889.442150189999,
          "radius_cap_fraction": 0.6636272687561551,
          "NASA_L_over_midradius": 37.867146083361376,
          "SF_yield": 3.79239951654798,
          "SF_euler": 1.3721070156168655,
          "SF_local": 1.3165825280116177,
          "SF_film": 1.3165825280121544,
          "SF_perry": 1.3165825291351312,
          "SF_global": 1.3165825280040278,
          "governing": "global",
          "k04_governing": "local",
          "k04_SF_least": 1.3165825280116177,
          "k04_SF_global": 2.6331650560080555,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 1028372665.6388679,
            "bending_Pa": 288561022.12910837,
            "maximum_compression_Pa": 1316933687.7679763,
            "opposite_signed_compression_Pa": 739811643.5097594,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.3165825280040278,
            "mean_compression_Pa": 1353937483.8570614,
            "bending_Pa": 2546062460.92588,
            "maximum_compression_Pa": 3899999944.7829413,
            "opposite_signed_compression_Pa": -1192124977.0688186,
            "maximum_tension_Pa": 1192124977.0688186
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6202,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.017944929147816868,
        "fractional_increase": 0.013818273214653676
      },
      "GAMMA/percent_mylar_5": {
        "published": {
          "nodes": 4798.824764916939,
          "members": 14390.474294750817,
          "n_coef": 1.5877132402714709,
          "m_nodes": 95.97649529833878,
          "m_film": 133.0872770003952,
          "m_joint": 215.62678977567703,
          "m_tube": 4083.47202321481,
          "reserve": 261.27956490077815,
          "sag_kg": 16.807457391278128,
          "vehicle": 4628.162585289221,
          "s_m": 0.55,
          "t_film_m": 7.564820713304718e-05,
          "r_o_m": 0.08519851782895568,
          "t_w_m": 0.0003114281748322345,
          "rt": 273.5735707755147,
          "A_m2": 0.00016640843593875376,
          "I_m4": 6.017580915276167e-07,
          "length_m": 0.550069346518747,
          "N_N": 151564.43628330785,
          "sigma_axial_Pa": 910797793.5631267,
          "SF_least": 0.4118375351025777,
          "governing": "perry",
          "k": 0.2,
          "SF_yield": 0.41721664532519803,
          "SF_euler": 53.09741086041229,
          "SF_local": 0.4141213140311618,
          "SF_film": 0.43710157106883774,
          "SF_perry": 0.4118375351025777,
          "SF_global": 0.765649812257583,
          "k04_SF_least": 0.4118375351025777,
          "k04_governing": "perry",
          "k04_SF_global": 1.531299624515166,
          "gamma": 0.4194580998485101,
          "SF_local_gamma1": 0.9872769513348872
        },
        "checker": {
          "nodes": 4402.449115800114,
          "members": 13201.34734740034,
          "n_coef": 1.6576792125854833,
          "m_nodes": 88.04898231600228,
          "m_film": 131.18008896771696,
          "m_joint": 215.59152041952518,
          "m_tube": 4092.601337106784,
          "m_end": 0.008165512002151064,
          "reserve": 262.02022137997085,
          "sag_kg": 17.548113870470825,
          "vehicle": 4627.4219288100285,
          "s_m": 0.5742369237697653,
          "r_o_m": 0.08733243707868987,
          "t_film_m": 7.456414140873842e-05,
          "t_w_m": 0.0003179101731586287,
          "rt": 274.707903213633,
          "A_m2": 0.00017412803031163733,
          "I_m4": 6.616204535647088e-07,
          "length_m": 0.5743158503452093,
          "N_N": 158243.44662586422,
          "sigma_axial_Pa": 908776412.061031,
          "k": 0.2,
          "gamma": 0.41877275325992114,
          "SF_local_gamma1": 0.9853871782195707,
          "SF_least": 0.4126533016402757,
          "eta": 0.01320037128703391,
          "Euler_stress_Pa": 46614629054.32951,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.4562529861648445,
          "NASA_L_over_midradius": 6.5881944511197394,
          "SF_yield": 0.41814465577753157,
          "SF_euler": 51.293836895052465,
          "SF_local": 0.4126533016500342,
          "SF_film": 0.4126533016407357,
          "SF_perry": 0.4126533016402757,
          "SF_global": 0.7865782289330907,
          "governing": "perry",
          "k04_governing": "perry",
          "k04_SF_least": 0.4126533016402757,
          "k04_SF_global": 1.5731564578661814,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 908776412.061031,
            "bending_Pa": 12234708.04600791,
            "maximum_compression_Pa": 921011120.1070389,
            "opposite_signed_compression_Pa": 896541704.0150231,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 0.4126533016402757,
            "mean_compression_Pa": 375009586.8897881,
            "bending_Pa": 4990413.110211957,
            "maximum_compression_Pa": 380000000.00000006,
            "opposite_signed_compression_Pa": 370019173.7795761,
            "maximum_tension_Pa": 0.0
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 7458,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.0008157665376979928,
        "fractional_increase": 0.001980796960371345
      },
      "GAMMA/percent_mylar_019": {
        "published": {
          "nodes": 4798.824764916939,
          "members": 14390.474294750817,
          "n_coef": 1.5877132402714709,
          "m_nodes": 95.97649529833878,
          "m_film": 131.2897129009967,
          "m_joint": 207.68265470128972,
          "m_tube": 3926.386885826449,
          "reserve": 428.10640146292553,
          "sag_kg": 16.807457391278128,
          "vehicle": 4461.335748727074,
          "s_m": 0.55,
          "t_film_m": 7.462645280467646e-05,
          "r_o_m": 0.08364834922137246,
          "t_w_m": 0.0003049959550587289,
          "rt": 274.26051996415964,
          "A_m2": 0.00016000694919575365,
          "I_m4": 5.577506578839194e-07,
          "length_m": 0.550069346518747,
          "N_N": 151564.43628330785,
          "sigma_axial_Pa": 947236585.9427944,
          "SF_least": 0.39589869899870395,
          "governing": "perry",
          "k": 0.2,
          "SF_yield": 0.4011669372142991,
          "SF_euler": 49.21432093110222,
          "SF_local": 0.3967999776307784,
          "SF_film": 0.4311977904096115,
          "SF_perry": 0.39589869899870395,
          "SF_global": 0.7228047694834333,
          "k04_SF_least": 0.39589869899870395,
          "k04_governing": "perry",
          "k04_SF_global": 1.4456095389668666,
          "gamma": 0.41904271101268376,
          "SF_local_gamma1": 0.9469201281937294
        },
        "checker": {
          "nodes": 4308.113288421604,
          "members": 12918.339865264812,
          "n_coef": 1.6757385763335182,
          "m_nodes": 86.16226576843208,
          "m_film": 127.59011033008771,
          "m_joint": 207.63828174647574,
          "m_tube": 3939.0132588309953,
          "m_end": 0.008036569865481681,
          "reserve": 429.0382335140098,
          "sag_kg": 17.73928944236238,
          "vehicle": 4460.40391667599,
          "s_m": 0.5804928708825581,
          "r_o_m": 0.08615353282213678,
          "t_film_m": 7.252355981669198e-05,
          "t_w_m": 0.000313544506399525,
          "rt": 274.7728984680667,
          "A_m2": 0.00016941862640720314,
          "I_m4": 6.264649647726012e-07,
          "length_m": 0.5805744058907716,
          "N_N": 159967.40862144352,
          "sigma_axial_Pa": 944213821.1943514,
          "k": 0.2,
          "gamma": 0.4187335713813264,
          "SF_local_gamma1": 0.9481801493518961,
          "SF_least": 0.3970348602103214,
          "eta": 0.013526808621660244,
          "Euler_stress_Pa": 44391872139.35458,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.44524336375304185,
          "NASA_L_over_midradius": 6.7511194846155815,
          "SF_yield": 0.4024512154665686,
          "SF_euler": 47.0146392087362,
          "SF_local": 0.3970348602509989,
          "SF_film": 0.3970348602103236,
          "SF_perry": 0.3970348602103214,
          "SF_global": 0.7468378375740797,
          "governing": "perry",
          "k04_governing": "perry",
          "k04_SF_least": 0.3970348602103214,
          "k04_SF_global": 1.4936756751481595,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 944213821.1943514,
            "bending_Pa": 13049767.837194199,
            "maximum_compression_Pa": 957263589.0315456,
            "opposite_signed_compression_Pa": 931164053.3571572,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 0.3970348602103214,
            "mean_compression_Pa": 374885802.50655276,
            "bending_Pa": 5114197.493447251,
            "maximum_compression_Pa": 380000000.0,
            "opposite_signed_compression_Pa": 369771605.0131055,
            "maximum_tension_Pa": 0.0
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 8606,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.0011361612116174702,
        "fractional_increase": 0.0028698281012062843
      },
      "GAMMA/cfrp_zylon_5": {
        "published": {
          "nodes": 49.9682476491694,
          "members": 143.9047429475082,
          "n_coef": 15.87713240271471,
          "m_nodes": 0.999364952983388,
          "m_film": 220.89798035984268,
          "m_joint": 23.11034020907313,
          "m_tube": 4131.88778324582,
          "m_end": 0.08029735412370333,
          "reserve": 412.54668142228127,
          "sag_kg": 168.07457391278123,
          "vehicle": 4476.895468767719,
          "s_m": 5.5,
          "t_film_m": 0.00011268270991437619,
          "r_o_m": 0.16612890712314143,
          "t_w_m": 0.0016002518156524037,
          "rt": 103.8142281722159,
          "A_m2": 0.0016623277743038386,
          "I_m4": 2.271923824051925e-05,
          "length_m": 5.571794047833012,
          "N_N": 1515644.3628330785,
          "sigma_axial_Pa": 911760235.4131458,
          "k": 0.2,
          "SF_yield": 4.277440327536103,
          "SF_euler": 1.9538442858791805,
          "SF_local": 1.4959789249660282,
          "SF_film": 1.493752313214508,
          "SF_perry": 1.8527315163033011,
          "SF_global": 1.4869170968607484,
          "gamma": 0.5756094231959386,
          "SF_local_gamma1": 2.598947940532228,
          "SF_least": 1.4869170968607484,
          "governing": "global",
          "k04_SF_least": 1.493752313214508,
          "k04_governing": "film",
          "k04_SF_global": 2.9738341937214967
        },
        "checker": {
          "nodes": 38.835545877448624,
          "members": 110.50663763234587,
          "n_coef": 18.118216215455647,
          "m_nodes": 0.7767109175489725,
          "m_film": 257.02188688740074,
          "m_joint": 22.148281914206635,
          "m_tube": 4073.224581628629,
          "m_end": 0.10021245053122364,
          "reserve": 436.2706888422143,
          "sag_kg": 191.79858133271432,
          "vehicle": 4453.171461347785,
          "s_m": 6.276334205537495,
          "r_o_m": 0.17334507376460032,
          "t_film_m": 0.00013110994801581995,
          "t_w_m": 0.001718495210050634,
          "rt": 100.87026879725364,
          "A_m2": 0.0018624370710604112,
          "I_m4": 2.7705705624289925e-05,
          "length_m": 6.384203027404153,
          "N_N": 1729580.101432606,
          "sigma_axial_Pa": 928664988.63655,
          "k": 0.2,
          "gamma": 0.579963584310357,
          "SF_local_gamma1": 2.6261096546899227,
          "SF_least": 1.5230479681068485,
          "eta": 0.0743927453391884,
          "Euler_stress_Pa": 1476922920.8577538,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.6933802950584013,
          "NASA_L_over_midradius": 37.01291386979135,
          "SF_yield": 4.1995768632625134,
          "SF_euler": 1.5903721351939268,
          "SF_local": 1.5230479681260014,
          "SF_film": 1.5230479683334703,
          "SF_perry": 1.5230479681195304,
          "SF_global": 1.5230479681068485,
          "governing": "global",
          "k04_governing": "perry",
          "k04_SF_least": 1.5230479681195304,
          "k04_SF_global": 3.046095936213697,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 928664988.63655,
            "bending_Pa": 186106938.63606903,
            "maximum_compression_Pa": 1114771927.272619,
            "opposite_signed_compression_Pa": 742558050.0004809,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.5230479681068485,
            "mean_compression_Pa": 1414401323.9948668,
            "bending_Pa": 2485598675.5044446,
            "maximum_compression_Pa": 3899999999.4993114,
            "opposite_signed_compression_Pa": -1071197351.5095778,
            "maximum_tension_Pa": 1071197351.5095778
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6445,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.03613087124610015,
        "fractional_increase": 0.02429918340597559
      },
      "FOLD/cfrp_zylon_019": {
        "published": {
          "nodes": 47.45507060497687,
          "members": 136.3652118149306,
          "n_coef": 16.310145104606928,
          "m_nodes": 0.9491014120995374,
          "m_film": 217.17480701365733,
          "m_joint": 23.185496143546445,
          "m_tube": 3964.1753756204644,
          "m_end": 0.08501250368390463,
          "reserve": 583.9573700002318,
          "sag_kg": 172.65842592858436,
          "vehicle": 4305.484780189768,
          "s_m": 5.65,
          "t_film_m": 0.00011078347452324353,
          "r_o_m": 0.16559039920506322,
          "t_w_m": 0.0015810621643113365,
          "rt": 104.73364232151457,
          "A_m2": 0.0016371394510956584,
          "I_m4": 2.2232043894907064e-05,
          "length_m": 5.727985371419447,
          "N_N": 1556980.1181830715,
          "sigma_axial_Pa": 951036954.8183937,
          "k": 0.2,
          "SF_yield": 4.100787020147633,
          "SF_euler": 1.7610680018281506,
          "SF_local": 1.4182991741260802,
          "SF_film": 1.4295868068960254,
          "SF_perry": 1.6760444294834462,
          "SF_global": 1.4209484282674771,
          "gamma": 0.5742702826382848,
          "SF_local_gamma1": 2.469741543320331,
          "SF_least": 1.4182991741260802,
          "governing": "local",
          "k04_SF_least": 1.4182991741260802,
          "k04_governing": "local",
          "k04_SF_global": 2.8418968565349543
        },
        "checker": {
          "nodes": 39.383572897331945,
          "members": 112.15071869199583,
          "n_coef": 17.984923298637984,
          "m_nodes": 0.787671457946639,
          "m_film": 241.8550856191549,
          "m_joint": 22.507340715827077,
          "m_tube": 3922.605559516183,
          "m_end": 0.10034416621814042,
          "reserve": 601.6864928808885,
          "sag_kg": 190.38754880924114,
          "vehicle": 4287.7556573091115,
          "s_m": 6.230160184694046,
          "r_o_m": 0.17057970600131955,
          "t_film_m": 0.0001233731807314169,
          "t_w_m": 0.0016697338319192024,
          "rt": 102.15981897261683,
          "A_m2": 0.0017808350473340687,
          "I_m4": 2.565649711503621e-05,
          "length_m": 6.3355918369860085,
          "N_N": 1716855.8479052044,
          "sigma_axial_Pa": 964073483.6588925,
          "k": 0.2,
          "gamma": 0.578043725820321,
          "SF_local_gamma1": 2.4977263439022517,
          "SF_least": 1.443795041899846,
          "eta": 0.0750137513284155,
          "Euler_stress_Pa": 1452388791.4049628,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.6823188240052782,
          "NASA_L_over_midradius": 37.32420891924741,
          "SF_yield": 4.045334786305453,
          "SF_euler": 1.5065125387463156,
          "SF_local": 1.4437950419088261,
          "SF_film": 1.4437950419165821,
          "SF_perry": 1.4437950419773715,
          "SF_global": 1.443795041899846,
          "governing": "global",
          "k04_governing": "local",
          "k04_SF_least": 1.4437950419088261,
          "k04_SF_global": 2.887590083799692,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 964073483.6588925,
            "bending_Pa": 215096613.20585093,
            "maximum_compression_Pa": 1179170096.8647435,
            "opposite_signed_compression_Pa": 748976870.4530416,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.443795041899846,
            "mean_compression_Pa": 1391924515.7338212,
            "bending_Pa": 2508075480.9564953,
            "maximum_compression_Pa": 3899999996.690316,
            "opposite_signed_compression_Pa": -1116150965.2226741,
            "maximum_tension_Pa": 1116150965.2226741
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6459,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.02549586777376578,
        "fractional_increase": 0.017976367919325442
      },
      "FOLD/ti_kapton_5": {
        "published": {
          "nodes": 425.97063298389315,
          "members": 1271.9118989516794,
          "n_coef": 5.340489990004039,
          "m_nodes": 8.519412659677863,
          "m_film": 1008.3107910285114,
          "m_joint": 189.309078279816,
          "m_tube": 3282.296585850922,
          "m_end": 0.07441910026781184,
          "reserve": 301.0062823710719,
          "sag_kg": 56.53417486157188,
          "vehicle": 4588.435867818927,
          "s_m": 1.85,
          "t_film_m": 0.0005650621357925588,
          "r_o_m": 0.10302682015515222,
          "t_w_m": 0.0006964763335891716,
          "rt": 147.9258019066077,
          "A_m2": 0.00044933070209509323,
          "I_m4": 2.3686495974377368e-06,
          "length_m": 1.8526483869264585,
          "N_N": 509807.64931658097,
          "sigma_axial_Pa": 1134593400.6723824,
          "k": 0.2,
          "SF_yield": 3.4373547366737576,
          "SF_euler": 5.477622113514928,
          "SF_local": 0.762617283247851,
          "SF_film": 0.739113638302939,
          "SF_perry": 3.16576241550582,
          "SF_global": 0.7420889405383613,
          "gamma": 0.5203022714065628,
          "SF_local_gamma1": 1.465719688646033,
          "SF_least": 0.739113638302939,
          "governing": "film",
          "k04_SF_least": 0.739113638302939,
          "k04_governing": "film",
          "k04_SF_global": 1.4841778810767225
        },
        "checker": {
          "nodes": 531.809210713301,
          "members": 1589.427632139903,
          "n_coef": 4.777373993109697,
          "m_nodes": 10.63618421426602,
          "m_film": 911.8950836853248,
          "m_joint": 193.5845411242513,
          "m_tube": 3378.281178148434,
          "m_end": 0.06089756375495421,
          "reserve": 295.0451630177241,
          "sag_kg": 50.5730555082241,
          "vehicle": 4594.396987172276,
          "s_m": 1.6549308965648404,
          "r_o_m": 0.10075139393053986,
          "t_film_m": 0.000511030317428581,
          "t_w_m": 0.0006558454784814524,
          "rt": 153.62062747435584,
          "A_m2": 0.0004138249069411394,
          "I_m4": 2.0867081824879224e-06,
          "length_m": 1.6568252886918358,
          "N_N": 456052.124410326,
          "sigma_axial_Pa": 1102041266.1512246,
          "k": 0.2,
          "gamma": 0.5142399635241838,
          "SF_local_gamma1": 1.4530739444216696,
          "SF_least": 0.747228692177341,
          "eta": 0.0331041686026488,
          "Euler_stress_Pa": 7433190541.995138,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.40300557572215945,
          "NASA_L_over_midradius": 16.49838697106684,
          "SF_yield": 3.5388874444061273,
          "SF_euler": 6.744929405370505,
          "SF_local": 0.7472286921773412,
          "SF_film": 0.7472286921773413,
          "SF_perry": 3.322164825384977,
          "SF_global": 0.747228692177341,
          "governing": "global",
          "k04_governing": "local",
          "k04_SF_least": 0.7472286921773412,
          "k04_SF_global": 1.494457384354682,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 1102041266.1512246,
            "bending_Pa": 42832483.3248237,
            "maximum_compression_Pa": 1144873749.4760482,
            "opposite_signed_compression_Pa": 1059208782.8264009,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 0.747228692177341,
            "mean_compression_Pa": 823476854.0316405,
            "bending_Pa": 30656791.48111267,
            "maximum_compression_Pa": 854133645.5127532,
            "opposite_signed_compression_Pa": 792820062.5505278,
            "maximum_tension_Pa": 0.0
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6246,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.008115053874402034,
        "fractional_increase": 0.010979440039876387
      },
      "FOLD/ti_kapton_019": {
        "published": {
          "nodes": 425.97063298389315,
          "members": 1271.9118989516794,
          "n_coef": 5.340489990004039,
          "m_nodes": 8.519412659677863,
          "m_film": 981.2569224663256,
          "m_joint": 191.44699282687972,
          "m_tube": 3140.385703303897,
          "m_end": 0.07525953369281,
          "reserve": 467.8331189332193,
          "sag_kg": 56.53417486157188,
          "vehicle": 4421.60903125678,
          "s_m": 1.85,
          "t_film_m": 0.0005499010199072409,
          "r_o_m": 0.10187630567438105,
          "t_w_m": 0.0006738401202686789,
          "rt": 151.18765210026396,
          "A_m2": 0.00042990378108964173,
          "I_m4": 2.216231448580831e-06,
          "length_m": 1.8526483869264585,
          "N_N": 509807.64931658097,
          "sigma_axial_Pa": 1185864539.3264825,
          "k": 0.2,
          "SF_yield": 3.288739877671883,
          "SF_euler": 5.1251474276927915,
          "SF_local": 0.709105068340859,
          "SF_film": 0.7192825669694961,
          "SF_perry": 3.019633077132913,
          "SF_global": 0.7021270288245686,
          "gamma": 0.5168052153094274,
          "SF_local_gamma1": 1.3720934838405137,
          "SF_least": 0.7021270288245686,
          "governing": "global",
          "k04_SF_least": 0.709105068340859,
          "k04_governing": "local",
          "k04_SF_global": 1.4042540576491371
        },
        "checker": {
          "nodes": 520.2095238602395,
          "members": 1554.6285715807185,
          "n_coef": 4.830546843370124,
          "m_nodes": 10.404190477204791,
          "m_film": 876.2315703119878,
          "m_joint": 195.65242229314129,
          "m_tube": 3244.719082245707,
          "m_end": 0.06292577721449098,
          "reserve": 462.4348848619594,
          "sag_kg": 51.13594079031203,
          "vehicle": 4427.00726532804,
          "s_m": 1.6733505122117025,
          "r_o_m": 0.09968653662999374,
          "t_film_m": 0.0004910443158743891,
          "t_w_m": 0.0006436976168475544,
          "rt": 154.86547413084847,
          "A_m2": 0.0004018776389032109,
          "I_m4": 1.9839583365135146e-06,
          "length_m": 1.675309001308822,
          "N_N": 461128.0492504567,
          "sigma_axial_Pa": 1147433956.536994,
          "k": 0.2,
          "gamma": 0.5129413404654657,
          "SF_local_gamma1": 1.3843719867253024,
          "SF_least": 0.7101016225737161,
          "eta": 0.033829277617496864,
          "Euler_stress_Pa": 7117581747.572641,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.398746146519975,
          "NASA_L_over_midradius": 16.860204948433886,
          "SF_yield": 3.398888430816856,
          "SF_euler": 6.203042630055864,
          "SF_local": 0.7101016225737165,
          "SF_film": 0.7101016225737165,
          "SF_perry": 3.17837948002615,
          "SF_global": 0.7101016225737161,
          "governing": "global",
          "k04_governing": "film",
          "k04_SF_least": 0.7101016225737165,
          "k04_SF_global": 1.4202032451474322,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 1147433956.536994,
            "bending_Pa": 46277277.7437878,
            "maximum_compression_Pa": 1193711234.2807817,
            "opposite_signed_compression_Pa": 1101156678.7932062,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 0.7101016225737161,
            "mean_compression_Pa": 814794714.3330983,
            "bending_Pa": 31127250.309321012,
            "maximum_compression_Pa": 845921964.6424193,
            "opposite_signed_compression_Pa": 783667464.0237772,
            "maximum_tension_Pa": 0.0
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6733,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.007974593749147552,
        "fractional_increase": 0.011357764936777537
      },
      "022c_cap/projection_5": {
        "published": {
          "nodes": 40.364452148519376,
          "members": 115.09335644555813,
          "n_coef": 17.75352077758099,
          "m_nodes": 0.8072890429703875,
          "m_film": 348.8563570154232,
          "m_joint": 207.21678204764885,
          "m_tube": 3794.671994894575,
          "reserve": 437.88972718938203,
          "sag_kg": 193.41761967988205,
          "vehicle": 4451.552423000618,
          "s_m": 6.15,
          "t_film_m": 0.00028619697756719387,
          "r_o_m": 0.16764011960487946,
          "t_w_m": 0.0016230884087073127,
          "rt": 103.28465085792475,
          "A_m2": 0.0017013453789958659,
          "I_m4": 2.3676289932865475e-05,
          "length_m": 6.251292310477491,
          "N_N": 1694765.969349715,
          "sigma_axial_Pa": 996132819.5160267,
          "SF_least": 1.3733213857843165,
          "governing": "global",
          "k": 0.2,
          "SF_yield": 3.9151405551468765,
          "SF_euler": 1.446598141654517,
          "SF_local": 1.378144869942854,
          "SF_film": 1.4624665443017892,
          "SF_perry": 1.3868432138641944,
          "SF_global": 1.3733213857843165,
          "k04_SF_least": 1.378144869942854,
          "k04_governing": "local",
          "k04_SF_global": 2.746642771568633,
          "gamma": 0.5763851730392067,
          "SF_local_gamma1": 2.391013742904019,
          "on_ro_cap_0_25": false
        },
        "checker": {
          "nodes": 39.81611445292934,
          "members": 113.44834335878802,
          "n_coef": 17.881771511491827,
          "m_nodes": 0.7963222890585868,
          "m_film": 332.7778392027734,
          "m_joint": 207.1502467497288,
          "m_tube": 3809.4307735027437,
          "m_end": 0.9129716689410008,
          "reserve": 439.28696844569413,
          "sag_kg": 194.81486093619415,
          "vehicle": 4450.155181744305,
          "s_m": 6.194427357448312,
          "r_o_m": 0.16845993476257798,
          "t_film_m": 0.0002730063817554706,
          "t_w_m": 0.001632792217105336,
          "rt": 103.17291630727449,
          "A_m2": 0.0017198778740050904,
          "I_m4": 2.416860322042203e-05,
          "length_m": 6.297999533703532,
          "N_N": 1707008.8918719161,
          "sigma_axial_Pa": 992517502.3600913,
          "k": 0.2,
          "gamma": 0.5765492624947824,
          "SF_local_gamma1": 2.4023220445393285,
          "SF_least": 1.385057003046346,
          "eta": 0.07549971457979254,
          "Euler_stress_Pa": 1433614207.502633,
          "mass_closure_kg": 4889.442150189999,
          "radius_cap_fraction": 0.6738397390503119,
          "NASA_L_over_midradius": 37.56780359248465,
          "SF_yield": 3.929401739240117,
          "SF_euler": 1.4444220924000484,
          "SF_local": 1.3850570030541078,
          "SF_film": 1.3850570030495801,
          "SF_perry": 1.3850570030738751,
          "SF_global": 1.385057003046346,
          "governing": "global",
          "k04_governing": "film",
          "k04_SF_least": 1.3850570030495801,
          "k04_SF_global": 2.770114006092692,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 992517502.3600913,
            "bending_Pa": 243546541.3059481,
            "maximum_compression_Pa": 1236064043.6660395,
            "opposite_signed_compression_Pa": 748970961.0541432,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.385057003046346,
            "mean_compression_Pa": 1374693317.2899127,
            "bending_Pa": 2525306681.461534,
            "maximum_compression_Pa": 3899999998.7514467,
            "opposite_signed_compression_Pa": -1150613364.1716213,
            "maximum_tension_Pa": 1150613364.1716213
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6575,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.01173561726202954,
        "fractional_increase": 0.008545426717670557
      },
      "022c_cap/projection_019": {
        "published": {
          "nodes": 40.364452148519376,
          "members": 115.09335644555813,
          "n_coef": 17.75352077758099,
          "m_nodes": 0.8072890429703875,
          "m_film": 344.14447412660274,
          "m_joint": 199.27264697326063,
          "m_tube": 3640.501176295637,
          "reserve": 604.7165637515294,
          "sag_kg": 193.41761967988205,
          "vehicle": 4284.725586438471,
          "s_m": 6.15,
          "t_film_m": 0.00028233141337633867,
          "r_o_m": 0.1655692772803688,
          "t_w_m": 0.0015764940543974704,
          "rt": 105.0237245224808,
          "A_m2": 0.0016322227222412863,
          "I_m4": 2.216020579405752e-05,
          "length_m": 6.251292310477491,
          "N_N": 1694765.969349715,
          "sigma_axial_Pa": 1038317838.7705247,
          "SF_least": 1.2945403446628159,
          "governing": "local",
          "k": 0.2,
          "SF_yield": 3.7560753117927757,
          "SF_euler": 1.3539668846454909,
          "SF_local": 1.2945403446628159,
          "SF_film": 1.4427135114359915,
          "SF_perry": 1.2993729363738948,
          "SF_global": 1.3013548041290857,
          "k04_SF_least": 1.2945403446628159,
          "k04_governing": "local",
          "k04_SF_global": 2.6027096082581713,
          "gamma": 0.5738497729022557,
          "SF_local_gamma1": 2.255887177781137,
          "on_ro_cap_0_25": false
        },
        "checker": {
          "nodes": 40.37079373188839,
          "members": 115.11238119566517,
          "n_coef": 17.75205364498719,
          "m_nodes": 0.8074158746377679,
          "m_film": 313.48004572621824,
          "m_joint": 199.27340810811904,
          "m_tube": 3671.180700561525,
          "m_end": 0.8655602726582428,
          "reserve": 604.7005799194994,
          "sag_kg": 193.40163584785208,
          "vehicle": 4284.7415702705,
          "s_m": 6.149491770361218,
          "r_o_m": 0.16581902501995016,
          "t_film_m": 0.00025717473627835576,
          "t_w_m": 0.0015872989623038568,
          "rt": 104.4661585233289,
          "A_m2": 0.0016458465081746977,
          "I_m4": 2.2411495564827567e-05,
          "length_m": 6.250758204575631,
          "N_N": 1694625.9156429798,
          "sigma_axial_Pa": 1029637883.743108,
          "k": 0.2,
          "gamma": 0.5746588802283152,
          "SF_local_gamma1": 2.2870463638416996,
          "SF_least": 1.3142715024749139,
          "eta": 0.07611768096569739,
          "Euler_stress_Pa": 1410261699.6486037,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.6632761000798006,
          "NASA_L_over_midradius": 37.877557825075506,
          "SF_yield": 3.787739419437523,
          "SF_euler": 1.3696676490979427,
          "SF_local": 1.3142715024755112,
          "SF_film": 1.3142715024756044,
          "SF_perry": 1.3142715024808835,
          "SF_global": 1.3142715024749139,
          "governing": "global",
          "k04_governing": "local",
          "k04_SF_least": 1.3142715024755112,
          "k04_SF_global": 2.6285430049498277,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 1029637883.743108,
            "bending_Pa": 290384756.1287504,
            "maximum_compression_Pa": 1320022639.8718584,
            "opposite_signed_compression_Pa": 739253127.6143577,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.3142715024749139,
            "mean_compression_Pa": 1353223728.4721453,
            "bending_Pa": 2546776271.2356987,
            "maximum_compression_Pa": 3899999999.707844,
            "opposite_signed_compression_Pa": -1193552542.7635534,
            "maximum_tension_Pa": 1193552542.7635534
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6653,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.019731157812098,
        "fractional_increase": 0.015241825326994585
      },
      "022c_cap/mylar_5": {
        "published": {
          "nodes": 4798.824764916939,
          "members": 14390.474294750817,
          "n_coef": 1.5877132402714709,
          "m_nodes": 95.97649529833878,
          "m_film": 133.0872770003952,
          "m_joint": 215.6034539036873,
          "m_tube": 4083.005305774999,
          "reserve": 261.7696182125789,
          "sag_kg": 17.297510703078878,
          "vehicle": 4627.6725319774205,
          "s_m": 0.55,
          "t_film_m": 7.564820713304718e-05,
          "r_o_m": 0.08519828596204942,
          "t_w_m": 0.00031139336565423614,
          "rt": 273.6034076482271,
          "A_m2": 0.00016638941640862286,
          "I_m4": 6.016862788913191e-07,
          "length_m": 0.550069346518747,
          "N_N": 151564.43628330785,
          "sigma_axial_Pa": 910901904.4281789,
          "SF_least": 0.4117904518929678,
          "governing": "perry",
          "k": 0.2,
          "SF_yield": 0.4171689598547343,
          "SF_euler": 53.09107431902106,
          "SF_local": 0.41401099676684927,
          "SF_film": 0.43710157106883774,
          "SF_perry": 0.4117904518929678,
          "SF_global": 0.765560371986085,
          "k04_SF_least": 0.4117904518929678,
          "k04_governing": "perry",
          "k04_SF_global": 1.53112074397217,
          "gamma": 0.4194400358692776,
          "SF_local_gamma1": 0.9870564594741731,
          "on_ro_cap_0_25": false
        },
        "checker": {
          "nodes": 4410.589660205443,
          "members": 13225.768980616329,
          "n_coef": 1.6561480373730015,
          "m_nodes": 88.21179320410886,
          "m_film": 131.04370964307734,
          "m_joint": 215.56795056211217,
          "m_tube": 4092.103508395058,
          "m_end": 0.008149543171291148,
          "reserve": 262.51518838564385,
          "sag_kg": 18.043080876143854,
          "vehicle": 4626.926961804355,
          "s_m": 0.5737065091171036,
          "r_o_m": 0.08728662917938446,
          "t_film_m": 7.448662196712439e-05,
          "t_w_m": 0.00031774463602091965,
          "rt": 274.70685350495637,
          "A_m2": 0.00017394607326303167,
          "I_m4": 6.60235913037266e-07,
          "length_m": 0.5737852171304202,
          "N_N": 158097.2793570877,
          "sigma_axial_Pa": 908886739.3863022,
          "k": 0.2,
          "gamma": 0.4187733861459849,
          "SF_local_gamma1": 0.9852713296113546,
          "SF_least": 0.4126054109714315,
          "eta": 0.013195096259003227,
          "Euler_stress_Pa": 46651907585.99517,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.4564352737449997,
          "NASA_L_over_midradius": 6.585561683211359,
          "SF_yield": 0.41809389831848937,
          "SF_euler": 51.32862607005955,
          "SF_local": 0.41260541097390374,
          "SF_film": 0.41260541097397446,
          "SF_perry": 0.4126054109714315,
          "SF_global": 0.7860702143055438,
          "governing": "perry",
          "k04_governing": "perry",
          "k04_SF_least": 0.4126054109714315,
          "k04_SF_global": 1.5721404286110876,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 908886739.3863022,
            "bending_Pa": 12231138.80371821,
            "maximum_compression_Pa": 921117878.1900204,
            "opposite_signed_compression_Pa": 896655600.582584,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 0.4126054109714315,
            "mean_compression_Pa": 375011586.6309696,
            "bending_Pa": 4988413.369030433,
            "maximum_compression_Pa": 380000000.0,
            "opposite_signed_compression_Pa": 370023173.26193917,
            "maximum_tension_Pa": 0.0
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 7513,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.000814959078463684,
        "fractional_increase": 0.0019790625904931858
      },
      "022c_cap/mylar_019": {
        "published": {
          "nodes": 4798.824764916939,
          "members": 14390.474294750817,
          "n_coef": 1.5877132402714709,
          "m_nodes": 95.97649529833878,
          "m_film": 131.2897129009967,
          "m_joint": 207.65931882929908,
          "m_tube": 3925.920168386639,
          "reserve": 428.5964547747263,
          "sag_kg": 17.297510703078878,
          "vehicle": 4460.845695415273,
          "s_m": 0.55,
          "t_film_m": 7.462645280467646e-05,
          "r_o_m": 0.08364810921899689,
          "t_w_m": 0.0003049605129959443,
          "rt": 274.2916071239339,
          "A_m2": 0.00015998792966562278,
          "I_m4": 5.576813900563458e-07,
          "length_m": 0.550069346518747,
          "N_N": 151564.43628330785,
          "sigma_axial_Pa": 947349194.405352,
          "SF_least": 0.3958516267571809,
          "governing": "perry",
          "k": 0.2,
          "SF_yield": 0.4011192517438354,
          "SF_euler": 49.208208936345756,
          "SF_local": 0.396690072455616,
          "SF_film": 0.4311977904096115,
          "SF_perry": 0.3958516267571809,
          "SF_global": 0.722716927636238,
          "k04_SF_least": 0.3958516267571809,
          "k04_governing": "perry",
          "k04_SF_global": 1.445433855272476,
          "gamma": 0.4190239380716442,
          "SF_local_gamma1": 0.9467002631906687,
          "on_ro_cap_0_25": false
        },
        "checker": {
          "nodes": 4316.285773645034,
          "members": 12942.857320935102,
          "n_coef": 1.6741506610730306,
          "m_nodes": 86.32571547290068,
          "m_film": 127.45367186693498,
          "m_joint": 207.61447589258356,
          "m_tube": 3938.510130511835,
          "m_end": 0.008020426662540993,
          "reserve": 429.53815644574456,
          "sag_kg": 18.239212374097168,
          "vehicle": 4459.903993744255,
          "s_m": 0.5799428009007024,
          "r_o_m": 0.08610704354945145,
          "t_film_m": 7.244600676012549e-05,
          "t_w_m": 0.0003133765700612667,
          "rt": 274.7717978169749,
          "A_m2": 0.0001692365125773033,
          "I_m4": 6.25116363177433e-07,
          "length_m": 0.5800241042844752,
          "N_N": 159815.8249001411,
          "sigma_axial_Pa": 944334189.2733754,
          "k": 0.2,
          "gamma": 0.4187342348216545,
          "SF_local_gamma1": 0.9480630886867628,
          "SF_least": 0.3969864719675677,
          "eta": 0.013521283550591762,
          "Euler_stress_Pa": 44428159040.22854,
          "mass_closure_kg": 4889.442150189999,
          "radius_cap_fraction": 0.4454251871859756,
          "NASA_L_over_midradius": 6.748361917761337,
          "SF_yield": 0.40239991765245064,
          "SF_euler": 47.0470724716788,
          "SF_local": 0.396986472003906,
          "SF_film": 0.3969864719675677,
          "SF_perry": 0.3969864719677651,
          "SF_global": 0.7463396881253662,
          "governing": "film",
          "k04_governing": "film",
          "k04_SF_least": 0.3969864719675677,
          "k04_SF_global": 1.4926793762507324,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 944334189.2733754,
            "bending_Pa": 13045905.065586796,
            "maximum_compression_Pa": 957380094.3389622,
            "opposite_signed_compression_Pa": 931288284.2077886,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 0.3969864719675677,
            "mean_compression_Pa": 374887898.15799063,
            "bending_Pa": 5112101.841820443,
            "maximum_compression_Pa": 379999999.99981105,
            "opposite_signed_compression_Pa": 369775796.3161702,
            "maximum_tension_Pa": 0.0
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 7882,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.0011348452103868145,
        "fractional_increase": 0.0028668448824713533
      },
      "022c_cap/cfrp_zylon_5": {
        "published": {
          "nodes": 49.9682476491694,
          "members": 143.9047429475082,
          "n_coef": 15.87713240271471,
          "m_nodes": 0.999364952983388,
          "m_film": 220.89798035984268,
          "m_joint": 23.111041059270214,
          "m_tube": 4126.986549277614,
          "m_end": 0.08029978924218076,
          "reserve": 417.4472145402888,
          "sag_kg": 172.97510703078882,
          "vehicle": 4471.994935649711,
          "s_m": 5.5,
          "t_film_m": 0.00011268270991437619,
          "r_o_m": 0.16612386920741104,
          "t_w_m": 0.0015983933238201686,
          "rt": 103.93178370538617,
          "A_m2": 0.001660355925652298,
          "I_m4": 2.2691159673744248e-05,
          "length_m": 5.571794047833012,
          "N_N": 1515644.3628330785,
          "sigma_axial_Pa": 912843047.3349459,
          "k": 0.2,
          "SF_yield": 4.272366439538634,
          "SF_euler": 1.951429541746115,
          "SF_local": 1.492068963146463,
          "SF_film": 1.493752313214508,
          "SF_perry": 1.8504480324015162,
          "SF_global": 1.485116372061561,
          "gamma": 0.5754376615782726,
          "SF_local_gamma1": 2.5929289352631426,
          "SF_least": 1.485116372061561,
          "governing": "global",
          "k04_SF_least": 1.492068963146463,
          "k04_governing": "local",
          "k04_SF_global": 2.970232744123122,
          "on_ro_cap_0_25": false
        },
        "checker": {
          "nodes": 38.85341152007831,
          "members": 110.56023456023493,
          "n_coef": 18.113824046564684,
          "m_nodes": 0.7770682304015663,
          "m_film": 256.5085551805508,
          "m_joint": 22.159991409109892,
          "m_tube": 4068.18144590888,
          "m_end": 0.10021682523220762,
          "reserve": 441.81508946105646,
          "sag_kg": 197.34298195155645,
          "vehicle": 4447.6270607289425,
          "s_m": 6.27481271360258,
          "r_o_m": 0.17325347701168295,
          "t_film_m": 0.0001308480913536694,
          "t_w_m": 0.001716869794929508,
          "rt": 100.91241486300157,
          "A_m2": 0.0018596961856887112,
          "I_m4": 2.7635817533827753e-05,
          "length_m": 6.382600607077543,
          "N_N": 1729160.8213100154,
          "sigma_axial_Pa": 929808231.3749791,
          "k": 0.2,
          "gamma": 0.579900522876977,
          "SF_local_gamma1": 2.6217852839346847,
          "SF_least": 1.520374657013453,
          "eta": 0.07441308539949029,
          "Euler_stress_Pa": 1476109515.9865496,
          "mass_closure_kg": 4889.442150189999,
          "radius_cap_fraction": 0.6930139080467318,
          "NASA_L_over_midradius": 37.02310999668326,
          "SF_yield": 4.194413286955708,
          "SF_euler": 1.58754188893737,
          "SF_local": 1.5203746570248873,
          "SF_film": 1.5203746570343473,
          "SF_perry": 1.520374657049157,
          "SF_global": 1.520374657013453,
          "governing": "global",
          "k04_governing": "local",
          "k04_SF_least": 1.5203746570248873,
          "k04_SF_global": 3.040749314026906,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 929808231.3749791,
            "bending_Pa": 186951544.29034448,
            "maximum_compression_Pa": 1116759775.6653237,
            "opposite_signed_compression_Pa": 742856687.0846347,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.520374657013453,
            "mean_compression_Pa": 1413656870.8650193,
            "bending_Pa": 2486343127.721749,
            "maximum_compression_Pa": 3899999998.586768,
            "opposite_signed_compression_Pa": -1072686256.8567295,
            "maximum_tension_Pa": 1072686256.8567295
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6650,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.035258284951892094,
        "fractional_increase": 0.02374109235826971
      },
      "022c_cap/cfrp_zylon_019": {
        "published": {
          "nodes": 46.66111084602568,
          "members": 133.98333253807704,
          "n_coef": 16.454482671904334,
          "m_nodes": 0.9332222169205135,
          "m_film": 217.17480701365733,
          "m_joint": 23.18138839899542,
          "m_tube": 3957.588677565962,
          "m_end": 0.08650847818107318,
          "reserve": 590.5640549944649,
          "sag_kg": 179.2651109228175,
          "vehicle": 4298.878095195535,
          "s_m": 5.7,
          "t_film_m": 0.00011078347452324353,
          "r_o_m": 0.16561974184185138,
          "t_w_m": 0.00159177158769494,
          "rt": 104.04742936873684,
          "A_m2": 0.001648468630220589,
          "I_m4": 2.239241621676398e-05,
          "length_m": 5.7801285634700275,
          "N_N": 1570758.703299736,
          "sigma_axial_Pa": 952859323.1947311,
          "k": 0.2,
          "SF_yield": 4.092944157721146,
          "SF_euler": 1.7266332058327198,
          "SF_local": 1.4274004176577701,
          "SF_film": 1.4170465717478142,
          "SF_perry": 1.6448737338327826,
          "SF_global": 1.4184374789671974,
          "gamma": 0.5752688455983981,
          "SF_local_gamma1": 2.4812753699063603,
          "SF_least": 1.4170465717478142,
          "governing": "film",
          "k04_SF_least": 1.4170465717478142,
          "k04_governing": "film",
          "k04_SF_global": 2.836874957934395,
          "on_ro_cap_0_25": false
        },
        "checker": {
          "nodes": 39.40235201850335,
          "members": 112.20705605551005,
          "n_coef": 17.98040776097936,
          "m_nodes": 0.788047040370067,
          "m_film": 241.35593674226024,
          "m_joint": 22.51963991231594,
          "m_tube": 3917.5901183800847,
          "m_end": 0.10034859082825963,
          "reserve": 607.1884081149684,
          "sag_kg": 195.889464043321,
          "vehicle": 4282.253742075031,
          "s_m": 6.228595956564401,
          "r_o_m": 0.17048654317414774,
          "t_film_m": 0.00012311855890097923,
          "t_w_m": 0.001668102312052558,
          "rt": 102.20388877968063,
          "A_m2": 0.00177812707970688,
          "I_m4": 2.5589616866010917e-05,
          "length_m": 6.333945725241885,
          "N_N": 1716424.7908966804,
          "sigma_axial_Pa": 965299280.6226363,
          "k": 0.2,
          "gamma": 0.5779784654014181,
          "SF_local_gamma1": 2.493478936411681,
          "SF_least": 1.4411771291774187,
          "eta": 0.07503492539858185,
          "Euler_stress_Pa": 1451563082.787847,
          "mass_closure_kg": 4889.442150189999,
          "radius_cap_fraction": 0.681946172696591,
          "NASA_L_over_midradius": 37.33482278919501,
          "SF_yield": 4.040197769011519,
          "SF_euler": 1.503744084271524,
          "SF_local": 1.4411771291779836,
          "SF_film": 1.4411771292426694,
          "SF_perry": 1.4411771291774187,
          "SF_global": 1.4411771291774476,
          "governing": "perry",
          "k04_governing": "perry",
          "k04_SF_least": 1.4411771291774187,
          "k04_SF_global": 2.882354258354895,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 965299280.6226363,
            "bending_Pa": 216216787.5099325,
            "maximum_compression_Pa": 1181516068.1325688,
            "opposite_signed_compression_Pa": 749082493.1127038,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.4411771291774187,
            "mean_compression_Pa": 1391167246.0447586,
            "bending_Pa": 2508832753.9552526,
            "maximum_compression_Pa": 3900000000.0000114,
            "opposite_signed_compression_Pa": -1117665507.910494,
            "maximum_tension_Pa": 1117665507.910494
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6324,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.02413055742960446,
        "fractional_increase": 0.017028768080530554
      },
      "022c_cap/ti_kapton_5": {
        "published": {
          "nodes": 425.97063298389315,
          "members": 1271.9118989516794,
          "n_coef": 5.340489990004039,
          "m_nodes": 8.519412659677863,
          "m_film": 1008.3107910285114,
          "m_joint": 189.31243251181044,
          "m_tube": 3280.6448704792338,
          "m_end": 0.07442041884655823,
          "reserve": 302.6546435107653,
          "sag_kg": 58.182536001265326,
          "vehicle": 4586.787506679234,
          "s_m": 1.85,
          "t_film_m": 0.0005650621357925588,
          "r_o_m": 0.10302499472904644,
          "t_w_m": 0.0006961370791092047,
          "rt": 147.99526963982427,
          "A_m2": 0.00044910459016150953,
          "I_m4": 2.367381266510696e-06,
          "length_m": 1.8526483869264585,
          "N_N": 509807.64931658097,
          "sigma_axial_Pa": 1135164637.558572,
          "k": 0.2,
          "SF_yield": 3.435624993029937,
          "SF_euler": 5.474689034033384,
          "SF_local": 0.7617656444937385,
          "SF_film": 0.739113638302939,
          "SF_perry": 3.1641560935928332,
          "SF_global": 0.7417035420242225,
          "gamma": 0.5202270891681058,
          "SF_local_gamma1": 1.464294459775012,
          "SF_least": 0.739113638302939,
          "governing": "film",
          "k04_SF_least": 0.739113638302939,
          "k04_governing": "film",
          "k04_SF_global": 1.483407084048445,
          "on_ro_cap_0_25": false
        },
        "checker": {
          "nodes": 532.9362174990175,
          "members": 1592.8086524970527,
          "n_coef": 4.772300885490936,
          "m_nodes": 10.65872434998035,
          "m_film": 910.5249309220741,
          "m_joint": 193.6620781490072,
          "m_tube": 3378.1319698676107,
          "m_end": 0.060792637535400866,
          "reserve": 296.4644469013274,
          "sag_kg": 51.992339391827365,
          "vehicle": 4592.977703288672,
          "s_m": 1.6531735205352487,
          "r_o_m": 0.10071105581478665,
          "t_film_m": 0.0005102624773403332,
          "t_w_m": 0.000655383440073799,
          "rt": 153.66737951670882,
          "A_m2": 0.0004133682134434941,
          "I_m4": 2.0827406903923105e-06,
          "length_m": 1.6550618716733827,
          "N_N": 455567.8413062117,
          "sigma_axial_Pa": 1102087258.9868019,
          "k": 0.2,
          "gamma": 0.5141910232550791,
          "SF_local_gamma1": 1.4525712366369987,
          "SF_least": 0.7468990905172728,
          "eta": 0.033082114367245154,
          "Euler_stress_Pa": 7443089797.589322,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.4028442232591466,
          "NASA_L_over_midradius": 16.487411899358193,
          "SF_yield": 3.5387397578531528,
          "SF_euler": 6.753630202051412,
          "SF_local": 0.7468990905172741,
          "SF_film": 0.7468990905172728,
          "SF_perry": 3.3224016520307025,
          "SF_global": 0.7468990905172728,
          "governing": "film",
          "k04_governing": "film",
          "k04_SF_least": 0.7468990905172728,
          "k04_SF_global": 1.4937981810345455,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 1102087258.9868019,
            "bending_Pa": 42796137.27029815,
            "maximum_compression_Pa": 1144883396.2571,
            "opposite_signed_compression_Pa": 1059291121.7165037,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 0.7468990905172728,
            "mean_compression_Pa": 823147971.4079163,
            "bending_Pa": 30617537.364144824,
            "maximum_compression_Pa": 853765508.7720611,
            "opposite_signed_compression_Pa": 792530434.0437715,
            "maximum_tension_Pa": 0.0
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6967,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.007785452214333799,
        "fractional_increase": 0.010533498248266326
      },
      "022c_cap/ti_kapton_019": {
        "published": {
          "nodes": 425.97063298389315,
          "members": 1271.9118989516794,
          "n_coef": 5.340489990004039,
          "m_nodes": 8.519412659677863,
          "m_film": 981.2569224663256,
          "m_joint": 191.45051984393825,
          "m_tube": 3138.733815147145,
          "m_end": 0.07526092019491813,
          "reserve": 469.4814800729127,
          "sag_kg": 58.182536001265326,
          "vehicle": 4419.960670117087,
          "s_m": 1.85,
          "t_film_m": 0.0005499010199072409,
          "r_o_m": 0.10187442884757343,
          "t_w_m": 0.0006734969813912556,
          "rt": 151.26189376102246,
          "A_m2": 0.00042967764550260926,
          "I_m4": 2.214991255657777e-06,
          "length_m": 1.8526483869264585,
          "N_N": 509807.64931658097,
          "sigma_axial_Pa": 1186488649.4624145,
          "k": 0.2,
          "SF_yield": 3.2870099530805024,
          "SF_euler": 5.122279418770031,
          "SF_local": 0.7082761781039622,
          "SF_film": 0.7192825669694961,
          "SF_perry": 3.018030701535017,
          "SF_global": 0.7017459107278406,
          "gamma": 0.5167263984505766,
          "SF_local_gamma1": 1.3706986525707894,
          "SF_least": 0.7017459107278406,
          "governing": "global",
          "k04_SF_least": 0.7082761781039622,
          "k04_governing": "local",
          "k04_SF_global": 1.4034918214556813,
          "on_ro_cap_0_25": false
        },
        "checker": {
          "nodes": 521.3644025701129,
          "members": 1558.093207710339,
          "n_coef": 4.82517315932249,
          "m_nodes": 10.42728805140226,
          "m_film": 874.8500880465396,
          "m_joint": 195.73466765147612,
          "m_tube": 3244.562800368427,
          "m_end": 0.06281224598209809,
          "reserve": 463.86730607215503,
          "sag_kg": 52.56836200050766,
          "vehicle": 4425.574844117845,
          "s_m": 1.6714890134528377,
          "r_o_m": 0.09964464954364027,
          "t_film_m": 0.0004902701266795304,
          "t_w_m": 0.0006432218602429293,
          "rt": 154.91489904588582,
          "A_m2": 0.0004014122867995369,
          "I_m4": 1.9800001108853035e-06,
          "length_m": 1.673440959980872,
          "N_N": 460615.072868585,
          "sigma_axial_Pa": 1147486233.0225923,
          "k": 0.2,
          "gamma": 0.5128899720870463,
          "SF_local_gamma1": 1.383867260688776,
          "SF_least": 0.7097716407068436,
          "eta": 0.03380569165517921,
          "Euler_stress_Pa": 7127502289.223848,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.3985785981745611,
          "NASA_L_over_midradius": 16.84846721708231,
          "SF_yield": 3.398733586308059,
          "SF_euler": 6.211405491505813,
          "SF_local": 0.7097716407068436,
          "SF_film": 0.7097716407068437,
          "SF_perry": 3.1786511690388375,
          "SF_global": 0.7097716407068443,
          "governing": "local",
          "k04_governing": "local",
          "k04_SF_least": 0.7097716407068436,
          "k04_SF_global": 1.4195432814136886,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 1147486233.0225923,
            "bending_Pa": 46235155.76629288,
            "maximum_compression_Pa": 1193721388.788885,
            "opposite_signed_compression_Pa": 1101251077.2562995,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 0.7097716407068436,
            "mean_compression_Pa": 814453186.3009608,
            "bending_Pa": 31085234.703471538,
            "maximum_compression_Pa": 845538421.0044323,
            "opposite_signed_compression_Pa": 783367951.5974892,
            "maximum_tension_Pa": 0.0
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 148,
            "spacing_upper_m": 8.0,
            "outer_radius_upper_m": 0.25,
            "evaluations": 6836,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_increase": 0.008025729979002971,
        "fractional_increase": 0.01143680334478736
      }
    },
    "bounds": {
      "GAMMA/percent_crush_5": {
        "bounds": "0.4<=s<=19.9 m; r_o<=min(1 m,s/3)",
        "checker": {
          "nodes": 39.798287366577235,
          "members": 113.39486209973171,
          "n_coef": 17.885987870602285,
          "m_nodes": 0.7959657473315447,
          "m_film": 333.42291751514597,
          "m_joint": 207.4109437924196,
          "m_tube": 3813.9999925859142,
          "m_end": 0.9145517704761613,
          "reserve": 433.8123305491875,
          "sag_kg": 189.3402230396875,
          "vehicle": 4455.629819640812,
          "s_m": 6.195887947088766,
          "r_o_m": 0.16854623707080174,
          "t_film_m": 0.0002735355951683339,
          "t_w_m": 0.001634288824307083,
          "rt": 103.1312425098808,
          "A_m2": 0.001722332818057191,
          "I_m4": 2.4227811394852864e-05,
          "length_m": 6.299535677876725,
          "N_N": 1707411.389045546,
          "sigma_axial_Pa": 991336500.7882295,
          "k": 0.2,
          "gamma": 0.5766105003721965,
          "SF_local_gamma1": 2.406155884056235,
          "SF_least": 1.3874147482714434,
          "eta": 0.07547975705726151,
          "Euler_stress_Pa": 1434378046.134962,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.674184948283207,
          "NASA_L_over_midradius": 37.55779977118905,
          "SF_yield": 3.9340829243138327,
          "SF_euler": 1.4469133790538957,
          "SF_local": 1.3874147482791706,
          "SF_film": 1.3874147482845096,
          "SF_perry": 1.3874147482760177,
          "SF_global": 1.3874147482714434,
          "governing": "global",
          "k04_governing": "perry",
          "k04_SF_least": 1.3874147482760177,
          "k04_SF_global": 2.774829496542887,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 991336500.7882295,
            "bending_Pa": 242253894.2104034,
            "maximum_compression_Pa": 1233590394.998633,
            "opposite_signed_compression_Pa": 749082606.577826,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.3874147482714434,
            "mean_compression_Pa": 1375394881.693395,
            "bending_Pa": 2524605118.099633,
            "maximum_compression_Pa": 3899999999.793028,
            "opposite_signed_compression_Pa": -1149210236.4062383,
            "maximum_tension_Pa": 1149210236.4062383
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 591,
            "spacing_upper_m": 19.9,
            "outer_radius_upper_m": 1.0,
            "evaluations": 5881,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_change_from_cap025": 3.709921259087423e-12,
        "within_original_limits": true
      },
      "GAMMA/cfrp_zylon_5": {
        "bounds": "0.4<=s<=19.9 m; r_o<=min(1 m,s/3)",
        "checker": {
          "nodes": 38.835545883119856,
          "members": 110.50663764935956,
          "n_coef": 18.118216214060897,
          "m_nodes": 0.7767109176623972,
          "m_film": 257.02188684601833,
          "m_joint": 22.148281914620323,
          "m_tube": 4073.224581684249,
          "m_end": 0.10021245051766664,
          "reserve": 436.2706888274496,
          "sag_kg": 191.79858131794958,
          "vehicle": 4453.17146136255,
          "s_m": 6.27633420505434,
          "r_o_m": 0.17334507376136254,
          "t_film_m": 0.0001311099479947103,
          "t_w_m": 0.0017184952099783925,
          "rt": 100.87026879960992,
          "A_m2": 0.0018624370709475482,
          "I_m4": 2.7705705621582397e-05,
          "length_m": 6.384203026895293,
          "N_N": 1729580.1012994624,
          "sigma_axial_Pa": 928664988.6213378,
          "k": 0.2,
          "gamma": 0.5799635843068308,
          "SF_local_gamma1": 2.6261096546715956,
          "SF_least": 1.5230479681035258,
          "eta": 0.07439274533463114,
          "Euler_stress_Pa": 1476922921.0383625,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.6933802950454502,
          "NASA_L_over_midradius": 37.012913867528226,
          "SF_yield": 4.1995768633313055,
          "SF_euler": 1.5903721354144604,
          "SF_local": 1.5230479681061122,
          "SF_film": 1.5230479682054934,
          "SF_perry": 1.5230479683225049,
          "SF_global": 1.5230479681035258,
          "governing": "global",
          "k04_governing": "local",
          "k04_SF_least": 1.5230479681061122,
          "k04_SF_global": 3.0460959362070517,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 928664988.6213378,
            "bending_Pa": 186106938.5779064,
            "maximum_compression_Pa": 1114771927.1992443,
            "opposite_signed_compression_Pa": 742558050.0434314,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.5230479681035258,
            "mean_compression_Pa": 1414401323.9686124,
            "bending_Pa": 2485598667.3859797,
            "maximum_compression_Pa": 3899999991.3545923,
            "opposite_signed_compression_Pa": -1071197343.4173672,
            "maximum_tension_Pa": 1071197343.4173672
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 591,
            "spacing_upper_m": 19.9,
            "outer_radius_upper_m": 1.0,
            "evaluations": 5971,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_change_from_cap025": -3.3226754680981685e-12,
        "within_original_limits": true
      },
      "022c_cap/projection_5": {
        "bounds": "0.4<=s<=19.9 m; r_o<=min(1 m,s/3)",
        "checker": {
          "nodes": 39.816114453016205,
          "members": 113.44834335904861,
          "n_coef": 17.881771511471293,
          "m_nodes": 0.7963222890603241,
          "m_film": 332.77783920192576,
          "m_joint": 207.1502467497395,
          "m_tube": 3809.4307735038033,
          "m_end": 0.9129716689389509,
          "reserve": 439.2869684454704,
          "sag_kg": 194.8148609359704,
          "vehicle": 4450.155181744529,
          "s_m": 6.194427357441198,
          "r_o_m": 0.16845993476266585,
          "t_film_m": 0.0002730063817547752,
          "t_w_m": 0.0016327922171031127,
          "rt": 103.17291630746878,
          "A_m2": 0.0017198778740036614,
          "I_m4": 2.4168603220427605e-05,
          "length_m": 6.29799953369605,
          "N_N": 1707008.8918699557,
          "sigma_axial_Pa": 992517502.3597761,
          "k": 0.2,
          "gamma": 0.576549262494497,
          "SF_local_gamma1": 2.402322044535567,
          "SF_least": 1.385057003047521,
          "eta": 0.07549971457966209,
          "Euler_stress_Pa": 1433614207.5075607,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.6738397390506634,
          "NASA_L_over_midradius": 37.567803592420084,
          "SF_yield": 3.929401739241365,
          "SF_euler": 1.4444220924054718,
          "SF_local": 1.3850570030512535,
          "SF_film": 1.3850570030476428,
          "SF_perry": 1.3850570030788762,
          "SF_global": 1.385057003047521,
          "governing": "global",
          "k04_governing": "film",
          "k04_SF_least": 1.3850570030476428,
          "k04_SF_global": 2.770114006095042,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 992517502.3597761,
            "bending_Pa": 243546541.30339232,
            "maximum_compression_Pa": 1236064043.6631684,
            "opposite_signed_compression_Pa": 748970961.0563838,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.385057003047521,
            "mean_compression_Pa": 1374693317.2906425,
            "bending_Pa": 2525306681.287275,
            "maximum_compression_Pa": 3899999998.577917,
            "opposite_signed_compression_Pa": -1150613363.9966323,
            "maximum_tension_Pa": 1150613363.9966323
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 591,
            "spacing_upper_m": 19.9,
            "outer_radius_upper_m": 1.0,
            "evaluations": 6162,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_change_from_cap025": 1.1750600492632657e-12,
        "within_original_limits": true
      },
      "022c_cap/cfrp_zylon_5": {
        "bounds": "0.4<=s<=19.9 m; r_o<=min(1 m,s/3)",
        "checker": {
          "nodes": 38.85341151984893,
          "members": 110.5602345595468,
          "n_coef": 18.11382404662105,
          "m_nodes": 0.7770682303969787,
          "m_film": 256.50855517870497,
          "m_joint": 22.159991409241645,
          "m_tube": 4068.1814459099846,
          "m_end": 0.10021682523342722,
          "reserve": 441.8150894616706,
          "sag_kg": 197.34298195217056,
          "vehicle": 4447.627060728329,
          "s_m": 6.274812713622108,
          "r_o_m": 0.17325347701065286,
          "t_film_m": 0.00013084809135272782,
          "t_w_m": 0.0017168697949454656,
          "rt": 100.91241486146366,
          "A_m2": 0.0018596961856947986,
          "I_m4": 2.763581753358542e-05,
          "length_m": 6.382600607098109,
          "N_N": 1729160.8213153966,
          "sigma_axial_Pa": 929808231.3748292,
          "k": 0.2,
          "gamma": 0.5799005228792777,
          "SF_local_gamma1": 2.621785283975064,
          "SF_least": 1.5203746570045436,
          "eta": 0.07441308540018374,
          "Euler_stress_Pa": 1476109515.9592617,
          "mass_closure_kg": 4889.44215019,
          "radius_cap_fraction": 0.6930139080426114,
          "NASA_L_over_midradius": 37.023109997025486,
          "SF_yield": 4.194413286956385,
          "SF_euler": 1.5875418889082782,
          "SF_local": 1.5203746570543353,
          "SF_film": 1.5203746570186751,
          "SF_perry": 1.5203746570225318,
          "SF_global": 1.5203746570045436,
          "governing": "global",
          "k04_governing": "film",
          "k04_SF_least": 1.5203746570186751,
          "k04_SF_global": 3.040749314009087,
          "on_ro_cap_0_25": false,
          "full_pressure": {
            "pressure_multiplier": 1.0,
            "mean_compression_Pa": 929808231.3748292,
            "bending_Pa": 186951544.2978874,
            "maximum_compression_Pa": 1116759775.6727166,
            "opposite_signed_compression_Pa": 742856687.0769417,
            "maximum_tension_Pa": 0.0
          },
          "reported_limit": {
            "pressure_multiplier": 1.5203746570045436,
            "mean_compression_Pa": 1413656870.856507,
            "bending_Pa": 2486343128.4314747,
            "maximum_compression_Pa": 3899999999.287982,
            "opposite_signed_compression_Pa": -1072686257.5749676,
            "maximum_tension_Pa": 1072686257.5749676
          },
          "search": {
            "method": "independent differential evolution plus bounded-accepted simplex",
            "seed": 591,
            "spacing_upper_m": 19.9,
            "outer_radius_upper_m": 1.0,
            "evaluations": 5874,
            "DE_success": true,
            "DE_message": "Optimization terminated successfully.",
            "certified_global_optimum": false
          }
        },
        "SF_change_from_cap025": -8.909539772616881e-12,
        "within_original_limits": true
      }
    }
  },
  "next": "Retain measured grid outputs, and label or add refined witnesses. Opening the radius/spacing upper bounds did not improve the four tested continuous branches.",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION"
}
```

### N561 — 033-NFI-09

Source `rpt-ref-5b1ba7a48fcb57c8e35e`; original file `unpublished-local-ref:6bdf8f2e409f7e2b; pointer `/issues/8`.

```json
{
  "id": "033-NFI-09",
  "tag": "QUESTIONABLE",
  "title": "Catalogue and numerical scope",
  "finding": "The 47-row honeycomb catalogue includes projected density-scaled rows. Winners are identified, and source tags remain intact. Radius crossings and noncrossing peaks are numerical searches, not interval proofs. Missing open-mode allowables and load cases are not silently assigned SF>=1.",
  "next_evidence": "Independent check should reproduce the packet and validate catalogue values, material directions, global search and additional load cases before design use.",
  "status": "open"
}
```

### N599 — NFI-022D-SEARCH

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/10`.

```json
{
  "id": "NFI-022D-SEARCH",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "NFI-C022-SEARCH-RESOLUTION"
  ],
  "finding": "The 12-film-gauge discretization is removed. Continuous DE, constrained refinements, independent residual checks and 16 expanded-domain cases agree, but no mathematical global certificate is claimed.",
  "next": "Preserve source-pinned witnesses and reoptimize when qualified physics or mass inputs change."
}
```

### N609 — NFI-017b-P3-SEARCH

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/9`.

```json
{
  "id": "NFI-017b-P3-SEARCH",
  "tag": "QUESTIONABLE",
  "claim": "P3 uses 022c's equilateral rows only; the two-way grid is not scored. The finer film grid and polish lift 022c's rows by 1.1 and 1.7 percent (0.7017 to 0.7097; 1.4170 to 1.4412).",
  "needed_to_ground": "022's owner's view on the two-way grid's stability with the film."
}
```

### N623 — NFI-026B-09

Source `rpt-ref-8befdd4c89803adc44a8`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/8`.

```json
{
  "id": "NFI-026B-09",
  "tag": "QUESTIONABLE",
  "status": "open",
  "owner": "sciences",
  "issue": "Finite grid, eigenvalue multiplicity and model scope",
  "evidence": "Ordered cases change section and frequency; actual arc lengths differ from nominal source bay. Twelve modes do not guarantee every degenerate eigenvector. Initial-moment couplings and shear deformation omitted.",
  "implication": "Coarse-grid discrepancy is established for these cases; do not infer a universal cutoff or uniquely attribute the difference to one mechanism."
}
```

### N634 — NFI-032-CHECK-ROUNDED-TARGET

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/prior_032_findings_retained/9`.

```json
{
  "id": "NFI-032-CHECK-ROUNDED-TARGET",
  "status": "qualification",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "The specified brief rounds both geometry and required Q; many decimal digits are displayed.",
  "checked": "Using the full pinned 021/021b geometry and required Q gives conditional 60 psi amplitudes 0.15313481918912647 and 0.06513526466329604 mm. The brief-based rows differ by -0.1737373278% and +0.1345534421%, respectively. This is intentional input precision, not an error in the requested calculation.",
  "followup": "Use the full-input supplemental rows when interpreting the precise upstream SF=1 threshold; do not interpret decimal output as metrological accuracy.",
  "source_audit_ids": [],
  "owner_nfi_ids": [],
  "exact_values": {
    "Be S-200F": {
      "tf_m": 0.0008434480441930918,
      "tc_m": 0.02021337638749162,
      "Q_needed": 0.37068071372338524,
      "Q_needed_from_membrane_stress": 0.37068071372338524,
      "pressure_Pa": 95460.83791390515,
      "radius_m": 10.0,
      "stress_Pa": 282948186.8240931,
      "intracell_uniaxial_critical_Pa": 5103736594.681676,
      "intracell_equibiaxial_factor": 0.5,
      "intracell_critical_Pa": 2551868297.340838,
      "intracell_SF": 9.018853684781929,
      "actual_input_amplitude_60psi": {
        "Q": 0.37068071372338524,
        "is_that_leads_Q": true,
        "delta_m": 0.00015313481918912647,
        "delta_mm": 0.15313481918912647,
        "delta_over_tf": 0.1815580938783576,
        "delta_over_cell_3_8_in": 0.016077146371561837,
        "delta_over_card_9_5_mm": 0.016119454651486998,
        "delta_over_tc": 0.007575914891877682,
        "K_delta": 1.8939787229694207
      },
      "brief_amplitude_60psi": {
        "Q": 0.371,
        "is_that_leads_Q": true,
        "delta_m": 0.00015286876684636114,
        "delta_mm": 0.15286876684636114,
        "delta_over_tf": 0.18125298416689725,
        "delta_over_cell_3_8_in": 0.01604921436707204,
        "delta_over_card_9_5_mm": 0.016091449141722225,
        "delta_over_tc": 0.007564016172506737,
        "K_delta": 1.8910040431266844
      },
      "brief_minus_actual_amplitude_mm": -0.00026605234276533274,
      "brief_over_actual_minus_one_percent": -0.17373732778352968
    },
    "SR-200": {
      "tf_m": 0.0006917479988347394,
      "tc_m": 0.030118230884842855,
      "Q_needed": 0.6092014443376216,
      "Q_needed_from_membrane_stress": 0.6092014443376215,
      "pressure_Pa": 95460.83791390515,
      "radius_m": 10.0,
      "stress_Pa": 344998605.25332373,
      "intracell_uniaxial_critical_Pa": 3432949414.9782996,
      "intracell_equibiaxial_factor": 0.5,
      "intracell_critical_Pa": 1716474707.4891498,
      "intracell_SF": 4.975309121115971,
      "actual_input_amplitude_60psi": {
        "Q": 0.6092014443376216,
        "is_that_leads_Q": true,
        "delta_m": 6.513526466329605e-05,
        "delta_mm": 0.06513526466329604,
        "delta_over_tf": 0.0941603947868551,
        "delta_over_cell_3_8_in": 0.006838347996146567,
        "delta_over_card_9_5_mm": 0.006856343648768005,
        "delta_over_tc": 0.002162652411834577,
        "K_delta": 0.5406631029586443
      },
      "brief_amplitude_60psi": {
        "Q": 0.609,
        "is_that_leads_Q": true,
        "delta_m": 6.522290640394087e-05,
        "delta_mm": 0.06522290640394086,
        "delta_over_tf": 0.09429363366190671,
        "delta_over_cell_3_8_in": 0.006847549228760197,
        "delta_over_card_9_5_mm": 0.006865569095151671,
        "delta_over_tc": 0.00216543513957307,
        "K_delta": 0.5413587848932675
      },
      "brief_minus_actual_amplitude_mm": 8.764174064482266e-05,
      "brief_over_actual_minus_one_percent": 0.13455344212980336
    }
  }
}
```

### N649 — NFI-026B-09

Source `rpt-ref-4a20323946ecafd56a6b`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/8`.

```json
{
  "id": "NFI-026B-09",
  "tag": "QUESTIONABLE",
  "status": "open",
  "owner": "sciences",
  "issue": "Finite grid, eigenvalue multiplicity and model scope",
  "evidence": "Ordered cases change section and frequency; actual arc lengths differ from nominal source bay. Twelve modes do not guarantee every degenerate eigenvector. Initial-moment couplings and shear deformation omitted.",
  "implication": "Coarse-grid discrepancy is established for these cases; do not infer a universal cutoff or uniquely attribute the difference to one mechanism."
}
```

### C009 — NFI-022D-CHECK-09

Source `rpt-ref-4b8e7b08241bb7a45536`; original file `unpublished-local-ref:2fa44902593248ea; pointer `/rows/8`.

```json
{
  "id": "NFI-022D-CHECK-09",
  "owner": "MAINLINE-022d",
  "state": "recorded numerical limitation",
  "kind": "optimization extent",
  "evidence": "INDEPENDENT-OPTIMA.json; ARITHMETIC-CHECK.active_roots",
  "note": "Independent searches recover all 176 reported optima to 1e-6 SF, and eight active-equation Zylon solutions agree. This supplies numerical corroboration of the specified surrogate, not a mathematical global certificate or structural qualification.",
  "settle": "Retain best-found terminology; any stronger optimization guarantee requires a separate mathematical bound or certified search.",
  "stops_other_work": false
}
```

### C018 — CHECK033-NFI-09

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/8`.

```json
{
  "id": "CHECK033-NFI-09",
  "inherited_id": "033-NFI-09",
  "tag": "QUESTIONABLE",
  "title": "Catalogue and numerical scope",
  "finding": "The 47-row honeycomb catalogue includes projected density-scaled rows. Winners are identified, and source tags remain intact. Radius crossings and noncrossing peaks are numerical searches, not interval proofs. Missing open-mode allowables and load cases are not silently assigned SF>=1.",
  "next_evidence": "Independent check should reproduce the packet and validate catalogue values, material directions, global search and additional load cases before design use.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Retained physical/model limitation. Arithmetic reproduction does not establish an installed-hull allowable."
}
```

### C019 — CHECK033-NFI-10

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/9`.

```json
{
  "id": "CHECK033-NFI-10",
  "tag": "PROJECTION",
  "title": "Search fraction range and tiny-core extrapolations",
  "finding": "224 differing paths arise in nonwinning projected 4/8/16 kg/m³ cores when the search extends below f=.00025. 220 recover within tolerance on the restricted range; four low-density handbook paths retain a precision residual. A representative wider-range core is only about 30 micrometres deep, far below its 4.8 mm cell scale. No physical validity or flotation is claimed.",
  "next_evidence": "Declare the fraction/thickness domain and impose a justified sandwich/honeycomb geometry range before calling each per-core value an unrestricted optimum.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Numerical/scope finding filed; does not block completion."
}
```

### C020 — CHECK033-NFI-11

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/10`.

```json
{
  "id": "CHECK033-NFI-11",
  "tag": "PROJECTION",
  "title": "Nearly vanishing scarf coverage is numerically ill-conditioned",
  "finding": "Fifteen last radius samples leave only 60.96 nm of short-side coverage. A relative thickness perturbation of 3e-13 explains the scale of their negative-budget discrepancies; 12/15 match the exact comparison tolerance under that perturbation. Both sets of margins remain enormously negative.",
  "next_evidence": "Exclude nonphysical overlap limits from performance tables or give a conditioning/error estimate. Retain raw values without treating their printed precision as meaningful.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Numerical/scope finding filed; does not block completion."
}
```

### C021 — CHECK033-NFI-12

Source `rpt-ref-d2ffe81a7858ecabf149`; original file `unpublished-local-ref:352148a346e66ea9; pointer `/issues/11`.

```json
{
  "id": "CHECK033-NFI-12",
  "tag": "PROJECTION",
  "title": "Active-mode intersection and crossing precision",
  "finding": "Direct active-constraint roots give 103.892078332461 m for the formal gamma-plus-strength crossing and 40.470082164560 m for retained-floor Q-plus-strength. Their reported values differ by -0.000197230237 m and -0.000030053061 m respectively. Four repeated nonwinning R15 handbook paths improve by 0.040833948 kg after active-mode polishing. Main least sets and rounded requested payloads/crossings do not change.",
  "next_evidence": "Polish active-mode intersections and outer roots together, or report fewer digits. The gamma-plus-strength crossing still exceeds the 99.897686 m compression ceiling of 6.35 mm stock.",
  "blocking_for_this_check": false,
  "status": "open",
  "check_disposition": "Numerical/scope finding filed; does not block completion."
}
```

### C127 — C039-01

Source `rpt-ref-20ab4b33b504a00ad3b6`; original file `unpublished-local-ref:75b66f0986a98c9b; pointer `/rows/0`.

```json
{
  "id": "C039-01",
  "topic": "GRID-EXTREMUM",
  "status": "REVISE",
  "objection": "The +1329.818726 kg and 0.689107645 values are correct at the filed grid points, but are not the best attainable values under the same continuous model.",
  "evidence": "CONSTRUCTIVE-POINTS.json: +1127.071353 kg at least SF 1.000001080; fixed-mass least SF 0.699691806. Two starts converge.",
  "proposed_fix": "Label the old results as attained grid values. Append the constructive designs, report the continuous search domain, and refine around the adequacy boundary. Do not assert a global optimum.",
  "disposition": "Record for owner revision; check completed"
}
```

### C160 — NFI-041-08

Source `rpt-ref-c7dfc45babe1b96007db`; original file `unpublished-local-ref:cd543374666d8c21; pointer `/items/7`.

```json
{
  "id": "NFI-041-08",
  "status": "open",
  "topic": "Search scope and best-found ranking",
  "evidence": [
    "resize/coarse-m3/RESULTS.json",
    "resize/f456-m12/RESULTS.json",
    "resize/f45-m24/CLOSED.json"
  ],
  "finding": "Frequency 5 ranks first at both reserves in the tested uniform-section family. Frequencies 1 through 10 were searched; 4/5/6 reoptimized at m6 and m12; 4/5 checked at m24. The final m24 witnesses keep the m12 gyration and solve exact mass closure. Multiple local starts and adaptive interpolation checks are not a global optimality certificate.",
  "needed": "Broader topology/nonuniform-section search and any necessary final exact optimizer refinement if a global optimum or minimum mass at the continuum target is required.",
  "prohibited_inference": "No claim of a globally lightest design attaining 022d's target is made; this card selected the brief's best-SF-at-closure option."
}
```

### C185 — 040-23-radius_scope

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/22`.

```json
{
  "id": "040-23-radius_scope",
  "tag": "PROJECTION",
  "open_issue": "The least-optimism ranking holds over R10/12/15/20/30 for the selected 3/8–1.0 core only.",
  "grounding": "Treat other radii/core grades and pressure/weather reserve policies as separate design choices requiring recomputation."
}
```

## R083 — optimism factor comparison 021 vs frame

**030b source history:** 017b P2 direction study uses nu=.08, variable scarf ratio and piecewise gamma, so its gamma-only and modulus-at-Vc2 results do not overturn033's flat-gamma singleton result. Its P3 leads/trend closure predate022d and are superseded for current design; all findings retained.

**Original question:** MAINLINE-021 P2 reaches SF 1 with gamma 2.90x0.20 and wrinkling 1.10x0.33; this frame least equilateral SF 1.354 needs a largest named factor of 8 (arc rise); both questionable.

### N361 — NFI-022-021

Source `rpt-mainline022-grok-p3-optimistic-floating-point-1020`; original file `unpublished-local-ref:62f20cec268319e4; pointer `retained original identity`.

```json
{
  "id": "NFI-022-021",
  "note": "MAINLINE-021 has filed (rpt-ref-fe49179fb6a8ad8c986e). Its P2 sandwich reaches SF 1 on gamma 2.90 times 0.20 and a wrinkling coefficient 1.10 times 0.33, at a face allowable of 283 MPa. Least mode 1.000. Full named set 1.111. This frame's least equilateral set is arc_rise_above_sphere, least SF 1.35387562843. The P2 sandwich needs less optimism. Its largest named factor is 2.90, and this frame's largest is 8 (arc rise over the spherical sagitta, factor 8). Both are QUESTIONABLE."
}
```

### N614 — NFI-017b-COMBINATION-METRIC

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/14`.

```json
{
  "id": "NFI-017b-COMBINATION-METRIC",
  "tag": "QUESTIONABLE",
  "claim": "The product of factors depends on how a property is parametrised (Q against Ec = Q^2; K_delta against physical waviness). Each lever's definition is stated so a reader can re-weight.",
  "needed_to_ground": "None; a reading note."
}
```

### B001 — NFI-030B-BASIS

Source `rpt-ref-39745602983887568501`; original file `unpublished-local-ref:534f72d6d7dd0ad8; pointer `retained original identity`.

```json
{
  "id": "NFI-030B-BASIS",
  "title": "P2 comparisons use distinct pressure, Poisson and joint-account conventions.",
  "finding": "028b uses p0, nu=.0752 and max(J,.05S); 033 uses 1.01p0, nu=.0768 and actual J as its main case. 036's 027 R20 point retains a separate eta=.9 splice law. Keep these bases attached; a changed threshold is not an arithmetic contradiction.",
  "status": "OPEN",
  "blocks_progress": false
}
```

### B007 — NFI-030B-017B-SUPERSESSION

Source `rpt-ref-39745602983887568501`; original file `unpublished-local-ref:534f72d6d7dd0ad8; pointer `retained original identity`.

```json
{
  "id": "NFI-030B-017B-SUPERSESSION",
  "title": "017b's P3 improvement factors and trend projection use superseded 022c physics.",
  "finding": "Retain its directional study as historical evidence, but use 022d for current P3 values and the ordered 026b global sensitivity. Its 1.441 Zylon optimum and projected 14–25 year closure are not current lead predictions. P2's variable scarf, nu=.08 and piecewise gamma also differ from 028b/033.",
  "status": "OPEN",
  "blocks_progress": false
}
```

### C057 — NFI-CHECK037-CURRENT-GEOMETRY

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/19`.

```json
{
  "id": "NFI-CHECK037-CURRENT-GEOMETRY",
  "tag": "QUESTIONABLE",
  "status": "open",
  "finding": "037 used 022c before 022d filed; several quoted high P3 factors are outside the half-wave band.",
  "proposed_fix": "Carry the now-filed 022d in-band geometry into the next thermal/load calculation, charging both film plies and fittings. Keep this audit tied to the original 022c record."
}
```

### S004 — NFI-030C-COMMON-ACCOUNT

Source `rpt-1228-mainline030c-design-register-1020`; original file `unpublished-local-ref:3c01fd6db28be861; pointer `/rows/3`.

```json
{
  "id": "NFI-030C-COMMON-ACCOUNT",
  "title": "040's common scalar account retains model and installed-qualification gaps.",
  "finding": "040 recomputes the 037b construction with its own loads, coating, pad and service bill. R10 does not float; R30 ranks least optimism among tested radii. Coating+primer at an assumed .20 kg/m2 and retained water are the largest assumed debits. Keep this account distinct from old 028b/033/037/034 variants and the 044 life spectrum. The original +0.120151 kg is a fixed-geometry allowance; 040 recomputes joining. Neither mass closure nor scalar SF closes installed qualification.",
  "status": "OPEN",
  "blocks_progress": false,
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## R084 — regressions recover filed points

**Original question:** With dimpling off, Be S-200F on HRH-10-4.8-32 at kd 0.20 recovers the filed 014 least SF, thicknesses and modes.

### N316 — NFI-011B-REGRESSION

Source `rpt-mainline011b-grok-p3-global-arcs-1019`; original file `unpublished-local-ref:4e90d1471135b741; pointer `retained original identity`.

```json
{
  "id": "NFI-011B-REGRESSION",
  "note": "With joints off and only yield, Euler, local and film, the 6061 banded optimum recovers the filed 011 point. The 011 tree was not rewritten."
}
```

### N346 — NFI-014-REGRESSION

Source `rpt-mainline014b-grok-metal-honeycomb-1019`; original file `unpublished-local-ref:092a55398f72361f; pointer `retained original identity`.

```json
{
  "id": "NFI-014-REGRESSION",
  "note": "With dimpling turned off, Be S-200F on HRH-10-4.8-32 at kd 0.20 recovers the filed 014 least SF, thicknesses and modes. The 014 tree was not rewritten."
}
```

## R085 — thin-wall section approximation P3

**Original question:** Answered here: exact annuli used, and tw/ro at optima is thin; only the fixed ro = 0.02 comparison rows are thick.

### N125 — NFI-005-THINWALL

Source `rpt-ref-eb07faa637b7487d6dc5`; original file `unpublished-local-ref:2ef2c84bad6b0b03; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-005-THINWALL",
  "gap": "P3 figures use thin-wall A and I at fixed outer radius. P3-A has tw/ro = 0.175, where thin-wall understates I for a given mass.",
  "direction": "Use exact annulus A and I for a named candidate section.",
  "effect": "P3-A's E/rho requirement is mildly pessimistic; exact section helps it."
}
```

### N142 — NFI-008B-THINWALL

Source `rpt-ref-cc9cef5e55adca018a8f`; original file `unpublished-local-ref:2bbb739a4c037482; pointer `retained original identity`.

```json
{
  "id": "NFI-008B-THINWALL",
  "inherited": "NFI-005-THINWALL",
  "issue": "The P3 columns use the thin-wall tube figures; the approximation is weakest on P3-A where tw/ro = 0.175.",
  "consequence": "P3 rows are order-of-magnitude readings; nothing in P3 passes anyway.",
  "next": "None unless a candidate family approaches P3 feasibility."
}
```

### N154 — NFI-011-TW-EXACT

Source `rpt-ref-f21d4bd21d2026511818`; original file `unpublished-local-ref:b5c9a6937c19e542; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-011-TW-EXACT",
  "gap": "NFI-005-THINWALL answered: all sections here are exact annuli, and at every reported optimum t_w/r_o lies in 0.019-0.076 (thin). Only the 005-frame comparison rows at fixed r_o=0.02 sit thick (t_w/r_o 0.175 aluminum, up to 0.38 for swaps), where the thin-cylinder local formula itself is weakest.",
  "direction": "None for this card's optima; the 005-frame rows are comparison only.",
  "effect": "None on the reported optima."
}
```

## R086 — mooring hardpoint load design

**Current 030c:** CHECK-037: pad masses depend on support and boss assumptions; preload/load direction can change sizing. Preserve proposed alternatives as sensitivities, not an installed load path.

**030b source history:** 037's R10 full-point 70-knot uniform excess falls to .998442; flight-gust screen is 1.003303. Its nominal single hardpoint pads weigh 8.65 or 33.14 kg at different wind cases and must be charged. Neither these values nor the thermal values are validated on the larger 033 hulls.

**Original question:** Mooring hardpoint patch stress exceeds the questionable core allowable and snatch loads need dynamic analysis.

### N063 — NFI-016-MOOR

Source `ref-0c9ab80606a173c6adb6`; original file `unpublished-local-ref:a420611badc594ad; pointer `retained original identity`.

```json
{
  "NFI_id": "NFI-016-MOOR",
  "rank": 7,
  "gap": "Mooring design load 48.3 kN at 20 m/s with a 1.4 gust factor; a bare 0.0707 m2 hardpoint patch sees 683 kPa against a 500.0 kPa QUESTIONABLE core allowable, SF 0.73. Added air mass 2445 kg equals hull mass, so snatch loads need a dynamic mooring analysis.",
  "direction": "Design spreaders of at least 0.145 m2 per hardpoint for core SF 1.5; run the mooring dynamics with the added mass; qualify six hardpoints, about 48 kg.",
  "effect": "Local design plus about 20 percent of the margin in fittings; not a hull-mode problem."
}
```

### N565 — NFI-037-MOORING-WIND

Source `rpt-ref-8c5de04c9c33dbcf7447`; original file `unpublished-local-ref:cbdfc7fec44de4cc; pointer `/rows/3`.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

### N567 — NFI-037-PATCH-BUCKLING

Source `rpt-ref-8c5de04c9c33dbcf7447`; original file `unpublished-local-ref:cbdfc7fec44de4cc; pointer `/rows/5`.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

### C045 — NFI-CHECK037-PAD-SUPPORT

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/7`.

```json
{
  "id": "NFI-CHECK037-PAD-SUPPORT",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "The filed thickness reproduces only a logarithmic term; support and boss-loading conditions are unspecified.",
  "proposed_fix": "Select edge support versus elastic foundation and finite boss loading. The supplied simply-supported uniform-patch solution includes the nonlogarithmic term and has independent boundary-condition checks."
}
```

### C046 — NFI-CHECK037-PAD-BOSS-FIT

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/8`.

```json
{
  "id": "NFI-CHECK037-PAD-BOSS-FIT",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "Under recovered 25 mm boss-radius assumptions the systems pad radius is only 14.683 mm.",
  "proposed_fix": "Define whether 25 mm is radius or diameter; enforce boss containment. The supplied 25 mm radius floor changes six-pad mass to 0.031809 kg before installation."
}
```

### C047 — NFI-CHECK037-PAD-PRELOAD-LOADPATH

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/9`.

```json
{
  "id": "NFI-CHECK037-PAD-PRELOAD-LOADPATH",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "Load-only F/crush sizing omits possible existing p/2 compression and does not address pull/oblique mooring transfer.",
  "proposed_fix": "Determine actual reaction direction and superpose compatible pressure loads; use available compression headroom when applicable, then check face bending, core shear, peel, local shell failure and hardware."
}
```

### C048 — NFI-CHECK037-P3-HARDPOINTS

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/10`.

```json
{
  "id": "NFI-CHECK037-P3-HARDPOINTS",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "7/2/1 member counts are scalar 5% sharing counts, without a vector load path or mass.",
  "proposed_fix": "Place attachment nodes and members, solve equilibrium and joint loads, size fittings/spreaders and weigh their mass into the same lift budget."
}
```

### C101 — NFI-037b-HARDPOINTS

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/12`.

```json
{
  "id": "NFI-037b-HARDPOINTS",
  "tag": "QUESTIONABLE",
  "claim": "Inserts, closeouts and 037's mooring pads constrain the mismatch locally; they are not scored here.",
  "needed_to_ground": "The hard-point design."
}
```

### C174 — 040-12-pad_load_path

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/11`.

```json
{
  "id": "040-12-pad_load_path",
  "tag": "PROJECTION",
  "open_issue": "Heavy pad is sized to mean crush and a plate formula; punching, peel and hull load distribution remain open.",
  "grounding": "Resolve the complete mooring attachment and validate with combined pressure/tether tests."
}
```

### C175 — 040-13-light_pad

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/12`.

```json
{
  "id": "040-13-light_pad",
  "tag": "PROJECTION",
  "open_issue": "The 20 m/s pad supplies only about 0.432 of the 70 kn capacity.",
  "grounding": "Resize the attachment for the actual required load; a mass-only lighter-pad result is not an assembly pass."
}
```

### C198 — NFI-037b-HARDPOINTS

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/12`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-HARDPOINTS",
  "tag": "QUESTIONABLE",
  "claim": "Inserts, closeouts and 037's mooring pads constrain the mismatch locally; they are not scored here.",
  "needed_to_ground": "The hard-point design."
}
```

### C236 — NFI-044-PAD-ASSEMBLY

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/12`.

```json
{
  "id": "NFI-044-PAD-ASSEMBLY",
  "finding": "The original pad area exceeds minimum core shear strength at its design load. The 950-day plate-only index excludes assembly support, cyclic plasticity, fasteners, backing and attachment notches.",
  "evidence_needed": "Detailed pad/insert load sharing and interaction solution, actual 6061-T6 properties/finish, local Be/core response and spectrum tests of the assembly."
}
```

### C237 — NFI-044-PAD-INTERACTION

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/13`.

```json
{
  "id": "NFI-044-PAD-INTERACTION",
  "finding": "The resized pad uses a scalar p/2 reserve against core capacity and an extra allocation of the sum of plate/core Miner indices. Neither is a validated multiaxial failure law.",
  "evidence_needed": "A calibrated local core shear/compression interaction and separate statistically supported component life requirements."
}
```

## R087 — Finished minimum gauge, forming and strength retention

**030b source history:** 036 distinguishes already etched finished stock from extra finishing. Require a minimum finished gauge and post-process compression basis; do not deduct etch twice.

**Original question:** Finished minimum gauge, forming and strength retention

### N436 — NFI-028b-gauge

Source `rpt-ref-d907de1e97319ecc3f9a`; original file `unpublished-local-ref:45bb70bc9cec9e78; pointer `/rows/12`.

```json
{
  "id": "NFI-028b-gauge",
  "status": "OPEN",
  "issue": "Map actual minimum thickness after forming and scarf preparation; nominal gauges sit at tight mode boundaries.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "scarf_face_m": 0.0007946240669858892
  },
  "today": {
    "datasheet_gauge_tolerance_in_this_band_m": 0.0001016
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched measured baseline or meaningful scalar ratio.",
  "source": "https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6"
}
```

### N543 — NFI-036-minimum-gauge

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/5`.

```json
{
  "id": "NFI-036-minimum-gauge",
  "status": "OPEN",
  "issue": "Specify minimum finished gauge rather than an unqualified nominal gauge.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "R10_scarf_finished_mm": 0.7946240669858892,
    "R20_027_finished_mm": 1.4231326177653179
  },
  "today": {
    "R10_catalog_tolerance_mm": 0.1016,
    "R20_catalog_tolerance_mm": 0.1524
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "sr200 pp2-3; RESULTS thickness",
  "closure": "Thickness map and guaranteed minimum after forming, machining and any new etch; mass accounting includes actual supplied gauge."
}
```

### N544 — NFI-036-forming-finish

Source `rpt-ref-5f14d083ceae03234596`; original file `unpublished-local-ref:0029aea733b20b58; pointer `/rows/6`.

```json
{
  "id": "NFI-036-forming-finish",
  "status": "OPEN",
  "issue": "Determine strength after the actual forming and finishing history.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "same_thermal_mechanical_history_as_hull": true
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "mmpds08; nasa4397; doe-ingot",
  "closure": "Matched finished coupons, defect inspection and compressive/rupture tests; do not transfer a tensile sanding result into a compression factor."
}
```

### N653 — NFI-038-GAUGE

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/2`.

```json
{
  "id": "NFI-038-GAUGE",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Nominal thickness is not finished minimum",
  "evidence": "036 shows catalog tolerances and processing alter demand.",
  "resolution_needed": "Measure thickness map and track additional removal without double-counting catalog etch.",
  "tests": [
    "T1",
    "T2"
  ]
}
```

### N694 — NFI-036-minimum-gauge

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/5`.

```json
{
  "id": "NFI-036-minimum-gauge",
  "status": "OPEN",
  "issue": "Specify minimum finished gauge rather than an unqualified nominal gauge.",
  "state": "exists_today",
  "tag": "QUESTIONABLE",
  "needed": {
    "R10_scarf_finished_mm": 0.7946240669858892,
    "R20_027_finished_mm": 1.4231326177653179
  },
  "today": {
    "R10_catalog_tolerance_mm": 0.1016,
    "R20_catalog_tolerance_mm": 0.1524
  },
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "sr200 pp2-3; RESULTS thickness",
  "closure": "Thickness map and guaranteed minimum after forming, machining and any new etch; mass accounting includes actual supplied gauge.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### N695 — NFI-036-forming-finish

Source `rpt-ref-f182f16ed5be422b7811`; original file `unpublished-local-ref:d5134460ede6a9f2; pointer `/rows/6`.

```json
{
  "id": "NFI-036-forming-finish",
  "status": "OPEN",
  "issue": "Determine strength after the actual forming and finishing history.",
  "state": "PROJECTION",
  "tag": "PROJECTION",
  "needed": {
    "same_thermal_mechanical_history_as_hull": true
  },
  "today": null,
  "improvement_factor": null,
  "null_factor_reason": "No matched qualified baseline; a scalar improvement ratio would be misleading.",
  "source": "mmpds08; nasa4397; doe-ingot",
  "closure": "Matched finished coupons, defect inspection and compressive/rupture tests; do not transfer a tensile sanding result into a compression factor.",
  "origin": "MAINLINE-036 owner NFI retained by independent check",
  "audit_disposition": "OPEN; check completion does not close qualification"
}
```

### C140 — N042-04

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/3`.

```json
{
  "id": "N042-04",
  "issue": "Doubly curved Be forming at blank size is unmeasured",
  "detail": "Solar's 0.003 in conformance was on a cylindrical 1 x 2 ft panel (10 ft radius). Lockheed's 39 in skins warped from thermal gradients, and it advised forming square sections and splicing. No doubly curved Be blank near 0.6 x 1.8 m has a measured contour.",
  "to_close": "Forming trial on one full blank (F1).",
  "tag": "QUESTIONABLE"
}
```

### C141 — N042-05

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/4`.

```json
{
  "id": "N042-05",
  "issue": "Forming residual stress is this card's estimate",
  "detail": "Conforming a flat blank elastically to R 10 m takes about 4.6e-4 strain across a 0.61 m width (67 MPa) and about 1.2e-3 over the half-diagonal disc, which is at Be's elastic limit. CSO saw 150 um panel rebound from the same effect in 1.0 mm Al.",
  "to_close": "Measure residual stress and springback on F1.",
  "tag": "PROJECTION"
}
```

## R088 — Waviness at the critical wavelength; metric and process transfer

**Current 030c:** The matched wavelength remains essential: panel RMS, fit gap, dimple amplitude and wrinkle-band amplitude are distinct. 042's reflector precedents are other-material transfers; cure waviness remains open.

**030b source history:** Combined CHECK-032/032b passes533 comparisons, corrects Woody3micrometres to template-adjustment RMS, recovers .008in face identity, and adds Rion carbon/Nomex measured depth near its own critical wavelength. Conditional full periods37–40mm approach/breach Woody's >40mm measurement band. None establishes actual Be/CR-III modal amplitude; retain all original Fc and metrology qualifications.

**Original question:** Waviness at the critical wavelength; metric and process transfer

### N449 — wavelength-versus-cell

Source `rpt-mainline032-grok-wrinkle-waviness-1020`; original file `unpublished-local-ref:e20bd8d3e1ca97e2; pointer `/open/3`.

```json
{
  "id": "wavelength-versus-cell",
  "tag": "QUESTIONABLE",
  "note": "Section 2.2.2 does not print the critical half-wavelength. FPL 1810-A says cell size changes that wavelength. Delta over the 9.525 mm cell is an amplitude ratio, not a separation of modes."
}
```

### N450 — shop-flatness-is-not-delta

Source `rpt-mainline032-grok-wrinkle-waviness-1020`; original file `unpublished-local-ref:e20bd8d3e1ca97e2; pointer `/open/4`.

```json
{
  "id": "shop-flatness-is-not-delta",
  "tag": "QUESTIONABLE",
  "note": "AMS7902H defines three flatness classes. The class numbers were not read. Bonded-panel numbers found here are long-wave bows or an architectural wave. Hexcel's design note that a large cell telegraphs into a thin face gives no depth. None of those is the Fourier component in equation 2.2-13."
}
```

### N473 — NFI-015-CHECK-MANUFACTURING-PROVENANCE

Source `rpt-ref-a5374575ee8867fc8d2e`; original file `unpublished-local-ref:f64006eca0195181; pointer `/findings/7`.

```json
{
  "id": "NFI-015-CHECK-MANUFACTURING-PROVENANCE",
  "provenance": "carried_from_015_check",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "status": "partly_addressed",
  "reported": "The comparison is narrowed to a 0.25 mm assembled-surface figure, and the card avoids a manufacturing-proof claim.",
  "checked": "The active-surface/benign-night conditions of the GBT benchmark remain unstated here. Old replica/MeerKAT/DVA-C/panel-target provenance errors are not repaired.",
  "evidence": [
    "COVERAGE.json",
    "evidence/72c698c144e8d4d8-CHECK.md"
  ],
  "followup": "Repair object, achievement/target, load-state and source attribution before comparing benchmarks; leave unlocated claims unverified."
}
```

### N512 — no-beryllium-face-at-wrinkle-wavelength

Source `rpt-mainline032b-grok-measured-flatness-1020`; original file `unpublished-local-ref:9a0f9d6404b3f821; pointer `/open/1`.

```json
{
  "id": "no-beryllium-face-at-wrinkle-wavelength",
  "tag": "QUESTIONABLE",
  "note": "No page read here gives a zero-to-peak amplitude of an as-bonded beryllium face on CR-III 3/8-1.0 at the CR-1457 wrinkle wavelength. That wavelength was not computed on 032 and is not computed here."
}
```

### N513 — optical-bench-and-space-mirror-unread

Source `rpt-mainline032b-grok-measured-flatness-1020`; original file `unpublished-local-ref:9a0f9d6404b3f821; pointer `/open/2`.

```json
{
  "id": "optical-bench-and-space-mirror-unread",
  "tag": "QUESTIONABLE",
  "note": "A space-mirror or optical-bench sandwich with a measured cell-print depth was not opened. The space sandwich that was opened is the aluminum solar-concentrator coupon, not an optical bench. Publisher gates blocked a 2025 panel-unit abstract on this pass."
}
```

### N514 — hexcel-telegraph-depth-still-unprinted

Source `rpt-mainline032b-grok-measured-flatness-1020`; original file `unpublished-local-ref:9a0f9d6404b3f821; pointer `/open/3`.

```json
{
  "id": "hexcel-telegraph-depth-still-unprinted",
  "tag": "QUESTIONABLE",
  "note": "A text extract of the local HexWeb attributes brochure contains no telegraphing depth. This pass does not add a depth Hexcel did not print."
}
```

### N515 — three-eighths-slope-is-not-a-depth

Source `rpt-mainline032b-grok-measured-flatness-1020`; original file `unpublished-local-ref:9a0f9d6404b3f821; pointer `/open/4`.

```json
{
  "id": "three-eighths-slope-is-not-a-depth",
  "tag": "PROJECTION",
  "note": "ER-1001 prints 0.5 to 1.6 milliradian on 3/8-inch cells and does not print the matching depth. The sine and the slope-times-cell sketches are labelled projections."
}
```

### N516 — transfer-to-the-lead-faces

Source `rpt-mainline032b-grok-measured-flatness-1020`; original file `unpublished-local-ref:9a0f9d6404b3f821; pointer `/open/5`.

```json
{
  "id": "transfer-to-the-lead-faces",
  "tag": "QUESTIONABLE",
  "note": "Leighton faces are 1 mm aluminum on a machined core. The ER-1001 faces are aluminum foil, 0.003 to 0.016 inch in the series, thinner than the lead sheets, and the core on the depth trace is 3/16 inch. Neither is S-200F or SR-200 on CR-III 3/8-1.0. Flatwise tension and the beryllium bond remain unprinted, so the 60 psi amplitudes stay an upper bound only if that F_c is real."
}
```

### N517 — panel-rms-is-not-delta

Source `rpt-mainline032b-grok-measured-flatness-1020`; original file `unpublished-local-ref:9a0f9d6404b3f821; pointer `/open/6`.

```json
{
  "id": "panel-rms-is-not-delta",
  "tag": "PROJECTION",
  "note": "Treating the 0.20 mm honeycomb rms, or a per-foot shop bow, as the wrinkle component exceeds the needed amplitudes only by using the wrong spatial piece."
}
```

### N532 — NFI-032-CHECK-WAVELENGTH

Source `rpt-ref-a30a669ed3e245f1473b`; original file `unpublished-local-ref:46e93c1ee5674acc; pointer `/findings/4`.

```json
{
  "id": "NFI-032-CHECK-WAVELENGTH",
  "status": "open",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "Amplitude/cell ratios are supplied beside inherited dimpling margins.",
  "checked": "Those ratios do not identify wavelength or mode separation. CR-1457 explicitly allows dimples to precipitate wrinkling. Dimpling uses a different biaxial factor (0.5) from wrinkling's cubic root.",
  "followup": "Measure the directional waveform spectrum and use a coupled assessment or matching experiment; do not apply the wrinkling multiplier to the dimpling formula.",
  "source_audit_ids": [
    "NASA-DIMPLING",
    "FPL1810A",
    "FPL1810"
  ],
  "owner_nfi_ids": [
    "wavelength-versus-cell"
  ]
}
```

### N533 — NFI-032-CHECK-SHOP-METRIC

Source `rpt-ref-a30a669ed3e245f1473b`; original file `unpublished-local-ref:46e93c1ee5674acc; pointer `/findings/5`.

```json
{
  "id": "NFI-032-CHECK-SHOP-METRIC",
  "status": "open",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "Commercial panel bows and core flatness are compared to the waviness amplitudes; Be class values were not read.",
  "checked": "Quoted product numbers reproduce, but geometry, material, ± convention, hold-down, wavelength and load state differ. The primary SAE public record does not verify the three-class claim or give flatness numbers.",
  "followup": "Obtain Be-specific finished/bonded-panel metrology near the relevant wavelengths; retain unverified SAE details as such.",
  "source_audit_ids": [
    "FLATIRON",
    "HONYLITE",
    "QC",
    "INDY",
    "SAE",
    "HEXCEL-TELEGRAPH"
  ],
  "owner_nfi_ids": [
    "shop-flatness-is-not-delta"
  ]
}
```

### N604 — NFI-017b-FLATNESS-TRANSLATION

Source `rpt-ref-6ba73ec8a89453b26832`; original file `unpublished-local-ref:7c9b732640b15383; pointer `/items/4`.

```json
{
  "id": "NFI-017b-FLATNESS-TRANSLATION",
  "tag": "QUESTIONABLE",
  "claim": "Q is translated to waviness with CR-1457 eq 2.2-12/13 using Fc = 60 psi (typical stabilised compression, taken as the lowest flatwise strength). The lever holds K_delta; physical waviness depends on Ec and Fc (0.347 mm today's equivalent at R 10; 0.099 mm in the Be-kept material combination).",
  "needed_to_ground": "Measured flatwise tension and bond strength for the Be/CR-III bond, and measured face waviness."
}
```

### N629 — NFI-032-CHECK-WAVELENGTH

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/prior_032_findings_retained/4`.

```json
{
  "id": "NFI-032-CHECK-WAVELENGTH",
  "status": "open",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "Amplitude/cell ratios are supplied beside inherited dimpling margins.",
  "checked": "Those ratios do not identify wavelength or mode separation. CR-1457 explicitly allows dimples to precipitate wrinkling. Dimpling uses a different biaxial factor (0.5) from wrinkling's cubic root.",
  "followup": "Measure the directional waveform spectrum and use a coupled assessment or matching experiment; do not apply the wrinkling multiplier to the dimpling formula.",
  "source_audit_ids": [
    "NASA-DIMPLING",
    "FPL1810A",
    "FPL1810"
  ],
  "owner_nfi_ids": [
    "wavelength-versus-cell"
  ]
}
```

### N630 — NFI-032-CHECK-SHOP-METRIC

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/prior_032_findings_retained/5`.

```json
{
  "id": "NFI-032-CHECK-SHOP-METRIC",
  "status": "open",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "Commercial panel bows and core flatness are compared to the waviness amplitudes; Be class values were not read.",
  "checked": "Quoted product numbers reproduce, but geometry, material, ± convention, hold-down, wavelength and load state differ. The primary SAE public record does not verify the three-class claim or give flatness numbers.",
  "followup": "Obtain Be-specific finished/bonded-panel metrology near the relevant wavelengths; retain unverified SAE details as such.",
  "source_audit_ids": [
    "FLATIRON",
    "HONYLITE",
    "QC",
    "INDY",
    "SAE",
    "HEXCEL-TELEGRAPH"
  ],
  "owner_nfi_ids": [
    "shop-flatness-is-not-delta"
  ]
}
```

### N633 — NFI-032-CHECK-LEAD-RANGE

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/prior_032_findings_retained/8`.

```json
{
  "id": "NFI-032-CHECK-LEAD-RANGE",
  "status": "correction",
  "disposition": "non_blocking",
  "blocks_progress": false,
  "tag": "QUESTIONABLE",
  "reported": "CARD says lead amplitudes span 0.0046–0.024 of the 9.525 mm cell.",
  "checked": "The lead-only ratios are 0.006847549228760197 and 0.01604921436707204. The printed endpoints are the two cross-Q rows among all four 60 psi cases. The underlying four rows are correct.",
  "followup": "Change the label to all four typical-strength cases, or use the lead-only range.",
  "source_audit_ids": [],
  "owner_nfi_ids": [],
  "exact_values": {
    "id": "NFI-032-CHECK-LEAD-RANGE",
    "field": "CARD lead amplitude / 9.525 mm cell range",
    "reported": [
      0.0046,
      0.024
    ],
    "checked": [
      0.006847549228760197,
      0.01604921436707204
    ],
    "all_four_typical_rows": [
      0.004594587314516719,
      0.02391896767621028
    ],
    "reason": "The reported endpoints round the two cross-Q rows; the lead-specific range uses Q .371 on S-200F and Q .609 on SR-200."
  }
}
```

### N635 — NFI-032B-CHECK-CSO-TEMPLATE

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/new_findings/0`.

```json
{
  "id": "NFI-032B-CHECK-CSO-TEMPLATE",
  "status": "correction_needed",
  "tag": "QUESTIONABLE",
  "blocks_progress": false,
  "claim": "CARD attributes 3 um to the completed CSO surface against its template.",
  "evidence": "Woody p.684 assigns 3 um to parabolic-template adjustment; the laboratory surface estimate is 10 um.",
  "disposition": "Relabel the 3 um result and its ratios. Numeric conversion passes; surface attribution does not."
}
```

### N636 — NFI-032B-CHECK-COUPON-IDENTITY

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/new_findings/1`.

```json
{
  "id": "NFI-032B-CHECK-COUPON-IDENTITY",
  "status": "resolved_in_this_check",
  "tag": "ADDITION",
  "blocks_progress": false,
  "claim": "The source text pages do not name the face thicknesses.",
  "evidence": "ER-1001 Fig.22 maps Fig.25 specimen30 to .008-in H19/Crest471/3/16-in core. Fig.30 gives .008-in face/APS/.015-in fillet for specimen32.",
  "disposition": "The report's figures fill the identity gap. They do not establish Be or CR-III equivalence."
}
```

### N637 — NFI-032B-CHECK-METRIC

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/new_findings/2`.

```json
{
  "id": "NFI-032B-CHECK-METRIC",
  "status": "open_qualification",
  "tag": "QUESTIONABLE",
  "blocks_progress": false,
  "claim": "Numerical depth/RMS/slope-to-delta comparisons can be mistaken for modal comparisons.",
  "evidence": "Dimple depth is not zero-to-peak Fourier amplitude; RMS requires a spatial model. A sine uses depth/2 or sqrt(2)*RMS.",
  "disposition": "Keep number-only labels and metrology bandwidth. Single-sine examples are projections, not fitted measurements."
}
```

### N638 — NFI-032B-CHECK-MISSED-RION

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/new_findings/3`.

```json
{
  "id": "NFI-032B-CHECK-MISSED-RION",
  "status": "omitted_evidence_added",
  "tag": "QUESTIONABLE",
  "blocks_progress": false,
  "claim": "032b did not retrieve the Rion thin-face waviness experiment.",
  "evidence": "Rion 2008 thesis has direct cell-depth measurements near its own calculated wrinkle half-wavelength; detailed values and material scope are in CHECK/RESULTS.",
  "disposition": "Evidence exists for a different system; no measured Be/CR-III modal amplitude follows. Preserve the empirical shape conversion."
}
```

### N639 — NFI-032B-CHECK-WAVELENGTH

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/new_findings/4`.

```json
{
  "id": "NFI-032B-CHECK-WAVELENGTH",
  "status": "partly_addressed",
  "tag": "PROJECTION",
  "blocks_progress": false,
  "claim": "The target wrinkle wavelength was not computed in 032/032b.",
  "evidence": "Elastic symmetric flat-panel Eq.19 gives full periods 38.5470 and 36.7051 mm at nu=0; alternative nu=.33 is only sensitivity.",
  "disposition": "A conditional band is now specified. Curvature, biaxiality, material tangent properties, other modes and actual measured spectrum remain unresolved."
}
```

### N640 — NFI-032B-CHECK-HISTORICAL-EVIDENCE

Source `rpt-ref-7427b639691bfaf71f29`; original file `unpublished-local-ref:0472a4dc2b497c9e; pointer `/new_findings/5`.

```json
{
  "id": "NFI-032B-CHECK-HISTORICAL-EVIDENCE",
  "status": "open_qualification",
  "tag": "QUESTIONABLE",
  "blocks_progress": false,
  "claim": "The 'exceeded today' field includes a 1969 honeycomb vendor RMS.",
  "evidence": "Von Hoerner p.2 attributes the .008-in figure to discussions with Rohr; no new honeycomb-cell measurements are supplied there.",
  "disposition": "Label it historical whole-surface capability evidence; do not infer a current production distribution or wrinkle-band exceedance."
}
```

### C099 — NFI-037b-WAVINESS

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/10`.

```json
{
  "id": "NFI-037b-WAVINESS",
  "tag": "QUESTIONABLE",
  "claim": "NASA/SDSU co-cured-panel studies report the face/core cure mismatch as cell-wall distortion and face waviness. That is a source of the wrinkle coefficient's waviness (MAINLINE-032), not of bond shear.",
  "needed_to_ground": "Measured face waviness after an AF 163-2U cure on CR-III."
}
```

### C148 — N042-12

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/11`.

```json
{
  "id": "N042-12",
  "issue": "Be face waviness at the wrinkle wavelength is unmeasured",
  "detail": "The precedents are whole-panel RMS (reflectors 5-60 um; vendor honeycomb 0.2 mm) or cell depths. Treated as wrinkle-band amplitude, they map to Q 0.19-0.75 (this card). Wrinkle periods are near 37-40 mm (CHECK-032).",
  "to_close": "Profilometry of a bonded Be/CR-III panel in the 20-60 mm band (F1, 038 T3).",
  "tag": "PROJECTION"
}
```

### C196 — NFI-037b-WAVINESS

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/10`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-WAVINESS",
  "tag": "QUESTIONABLE",
  "claim": "NASA/SDSU co-cured-panel studies report the face/core cure mismatch as cell-wall distortion and face waviness. That is a source of the wrinkle coefficient's waviness (MAINLINE-032), not of bond shear.",
  "needed_to_ground": "Measured face waviness after an AF 163-2U cure on CR-III."
}
```

## R089 — Sun, bond reference temperature and additional pressure/load interaction

**Current 030c:** CHECK-037 leaves 84 thermal/projection fields unrecovered. Its supplied polynomial maxima are 8.292853/14.851720 K; total flight pressure 479.847608 Pa gives conditional P2 minimum 1.001324769. 037b inherits the unresolved temperatures. 040 introduces its own resolved thermal balances and corrected128/256-zone projection; it does not retrospectively recover037's missing inputs.

**030b source history:** 037 coated reference thermal shear screen is 1.678; a cold-night stress-free bond reference gives .917, and bare Be gives .388. Coating, bond temperature, wind and local load requirements remain choices; no combined whole-vehicle closure is claimed.

**Original question:** Sun, bond reference temperature and additional pressure/load interaction

### N495 — NFI-031-ENVIRONMENT-LOADS

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/13`.

```json
{
  "id": "NFI-031-ENVIRONMENT-LOADS",
  "tag": "QUESTIONABLE",
  "issue": "Mode scores use uniform centre pressure, no internal-pressure relief and fixed material properties. Local bottom pressure is about a further 0.1% higher, while gradients, thermal mismatch, wind, attached loads and descent transients are unscored.",
  "next_evidence": "Set structural design factors and loads independently of the SF=1 screening threshold; include nonuniform pressure and thermal/wind/handling loads."
}
```

### N563 — NFI-037-BARE-BE

Source `rpt-ref-8c5de04c9c33dbcf7447`; original file `unpublished-local-ref:cbdfc7fec44de4cc; pointer `/rows/1`.

```json
{
  "id": "NFI-037-BARE-BE",
  "tag": "QUESTIONABLE",
  "finding": "Bare beryllium, absorptance 0.40 and emittance 0.05, reaches 356.9 K. The day rise from the air temperature produces 621 kPa of face-core shear and factor 0.388 on the 241 kPa sheet. The optical pair is an engineering band, not a measured SR-200 coupon.",
  "next": "A measured solar absorptance and infrared emittance for the bare sheet, or a required coating."
}
```

### N564 — NFI-037-ASSEMBLY-TEMPERATURE

Source `rpt-ref-8c5de04c9c33dbcf7447`; original file `unpublished-local-ref:cbdfc7fec44de4cc; pointer `/rows/2`.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

### N566 — NFI-037-PATTERN-BOUND

Source `rpt-ref-8c5de04c9c33dbcf7447`; original file `unpublished-local-ref:cbdfc7fec44de4cc; pointer `/rows/4`.

```json
{
  "id": "NFI-037-PATTERN-BOUND",
  "tag": "QUESTIONABLE",
  "finding": "A through-thickness-uniform solar pattern has no membrane stress on a complete sphere. Bending is 0.818 MPa coated. The constrained upper bounds are 20.51 MPa coated and 60.75 MPa bare. The table uses the bending value.",
  "next": "None, unless a later shell solution replaces the bending estimate."
}
```

### B003 — NFI-030B-LOAD-AND-MASS-TRANSFER

Source `rpt-ref-39745602983887568501`; original file `unpublished-local-ref:534f72d6d7dd0ad8; pointer `retained original identity`.

```json
{
  "id": "NFI-030B-LOAD-AND-MASS-TRANSFER",
  "title": "Weather, extra loads and vacuum bills have not been jointly optimized on every current lead.",
  "finding": "031 reoptimizes older seam/film geometry; 037 evaluates 028b's full endpoint and pre-022d P3; 034 estimates service at older geometries. Carry their requirements and evidence, but do not add their margins or copy their bills as validated values for 033/022d. Coating, pads, barriers and fittings require a complete reclosure.",
  "status": "OPEN",
  "blocks_progress": false
}
```

### C038 — NFI-CHECK037-HEAT-INPUTS

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/0`.

```json
{
  "id": "NFI-CHECK037-HEAT-INPUTS",
  "tag": "QUESTIONABLE",
  "status": "open",
  "finding": "84 thermal/projection fields are not independently recoverable from supplied inputs.",
  "proposed_fix": "Publish velocities, all optical properties, sky/ground/cavity boundary conditions, grid, weights, converged day/night profiles and residuals; rerun both P2 and P3. The declared P2 comparison supplies a reproducible starting model."
}
```

### C039 — NFI-CHECK037-PATTERN-DEFINITION

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/1`.

```json
{
  "id": "NFI-CHECK037-PATTERN-DEFINITION",
  "tag": "QUESTIONABLE",
  "status": "open",
  "finding": "Filed residual maxima do not equal extrema of the filed n=2..6 polynomial.",
  "proposed_fix": "State whether maxima use raw or truncated temperatures; retain raw samples, area weights and projection coefficients; use analytic extrema and constant/linear-mode consistency checks."
}
```

### C040 — NFI-CHECK037-SHELL-EQUILIBRIUM

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/2`.

```json
{
  "id": "NFI-CHECK037-SHELL-EQUILIBRIUM",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "The scalar bending estimate and a membrane-free kinematic trial do not establish full spherical-shell equilibrium.",
  "proposed_fix": "Solve both curvature components, membrane/bending coupling and force/moment equilibrium with compatible thermal strains and core restraint; compare with the rough gradient screen."
}
```

### C043 — NFI-CHECK037-STEADY-FLIGHT-LOAD

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/5`.

```json
{
  "id": "NFI-CHECK037-STEADY-FLIGHT-LOAD",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "The 290.634 Pa flight addition omits the selected VB baseline.",
  "proposed_fix": "For the same selected local-speed case add 189.214 Pa steady pressure; total 479.848 Pa gives conditional P2 least 1.001324769. Select EAS/TAS and dynamic-response treatment consistently."
}
```

### C044 — NFI-CHECK037-WIND-PATCH

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/6`.

```json
{
  "id": "NFI-CHECK037-WIND-PATCH",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "Negative mean Cp is not proof that uniform excess bounds a nonuniform buckling mode.",
  "proposed_fix": "Compute the prestressed nonuniform pressure and hardpoint equilibrium, then compare instability/imperfection response; retain uniform excess as a screening assumption until shown."
}
```

### C052 — NFI-CHECK037-CORE-CTE-LAG

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/14`.

```json
{
  "id": "NFI-CHECK037-CORE-CTE-LAG",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "Prescribed Al-versus-Be strain in an equivalent shear-lag formula does not include effective cellular in-plane stiffness or finite boundary conditions.",
  "proposed_fix": "Model both adherends/core compatibility and effective thermal expansion, then compare with representative measured thermal-cycle shear and peel."
}
```

### C053 — NFI-CHECK037-CONVECTION-OPTICS

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/15`.

```json
{
  "id": "NFI-CHECK037-CONVECTION-OPTICS",
  "tag": "QUESTIONABLE",
  "status": "open",
  "finding": "No speed or validity check is provided for Whitaker; bare optics and coating durability are assumptions.",
  "proposed_fix": "Select climate and flight/ground thermal cases, validate the applicable convection regime, and retain measured or explicitly assumed surface optics and their temperature dependence."
}
```

### C054 — NFI-CHECK037-FILM-CONSTITUTIVE

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/16`.

```json
{
  "id": "NFI-CHECK037-FILM-CONSTITUTIVE",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "Film nu is unstated, the frame is assumed rigid, and an isotropic law is applied even to the Zylon reinforcement case.",
  "proposed_fix": "Provide membrane/laminate stiffness and CTE tensors, prestress and slip/bond conditions; solve frame-film compatibility with both directions and barrier mass."
}
```

### C056 — NFI-CHECK037-COMPLETE-MODE-ACCOUNT

Source `rpt-ref-bba592d71d65b13cc2e5`; original file `unpublished-local-ref:578e88896b763bc7; pointer `/rows/18`.

```json
{
  "id": "NFI-CHECK037-COMPLETE-MODE-ACCOUNT",
  "tag": "PROJECTION",
  "status": "open",
  "finding": "The seven-screen minimum omits unresolved assembly modes; the filed coated swing is 0.917 and a separate scalar scarf interaction is 0.980.",
  "proposed_fix": "Maintain a complete mode/load-case ledger, distinguish day-rise from night-reference assembly and map core thermal shear to scarf/bond stresses before combining them. Do not present seven-screen unity as installed-hull unity."
}
```

### C170 — 040-08-thermal_model

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/7`.

```json
{
  "id": "040-08-thermal_model",
  "tag": "PROJECTION",
  "open_issue": "Corrected thermal quadrature does not qualify the 037b homogenized free-edge model, local hardpoint restraint or joint coincidence.",
  "grounding": "Compare thermal maps, strain and interface damage on curved instrumented panels."
}
```

### C176 — 040-14-aerodynamic_pressure

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/13`.

```json
{
  "id": "040-14-aerodynamic_pressure",
  "tag": "PROJECTION",
  "open_issue": "Uniform Cp=1 and aligned gust velocity are load surrogates; 70 kn is the governing modeled pressure.",
  "grounding": "Resolve pressure distribution and transient tether/flight loads for the chosen configuration."
}
```

### C225 — NFI-044-STATIC-ENVELOPE

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/1`.

```json
{
  "id": "NFI-044-STATIC-ENVELOPE",
  "finding": "028b has only 607 Pa pressure-screen headroom; +2 kPa weather, sea-level descent and 70 kn uniform-pressure cases fail the static screen.",
  "evidence_needed": "A complete operational pressure envelope and a new equilibrium, mass and buckling solution with adequate margin."
}
```

### C230 — NFI-044-THERMAL-BOUNDARY

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/6`.

```json
{
  "id": "NFI-044-THERMAL-BOUNDARY",
  "finding": "037's complete night inner-temperature and boundary history are absent; the opposite night gradient is a projection. Cure reference changes mean but cannot remove the thermal range.",
  "evidence_needed": "A reproducible transient thermal model and coated-panel thermal-cycle measurements."
}
```

## R090 — Terrain, weather, altitude floor/ceiling and passive equilibrium requirement

**030b source history:** 031's illustrative 100m centre floor needs 55.341 kg optimistic climate headroom or 441.770 kg for both weather sets on its own geometry; ISA equilibria are 617.075/1464.507 m. The Admiral must choose terrain-relative clearance, ceiling and weather envelope.

**Original question:** Terrain, weather, altitude floor/ceiling and passive equilibrium requirement

### N482 — NFI-031-REQUIREMENT

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/0`.

```json
{
  "id": "NFI-031-REQUIREMENT",
  "tag": "QUESTIONABLE",
  "issue": "No site elevation, terrain, minimum hull clearance, altitude ceiling or required 500m condition has been authorised. Centre 10m is ground tangency at sea level; 100m is only an illustrative 90m clearance.",
  "next_evidence": "Specify centre-height range relative to surveyed terrain, weather set, clearance and whether 500m means ISA free float or a minimum on every design day."
}
```

### N483 — NFI-031-PROFILE

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/1`.

```json
{
  "id": "NFI-031-PROFILE",
  "tag": "PROJECTION",
  "issue": "019 specifies conditions at one altitude, not a vertical profile. A 6.5K/km lapse and constant e/p were imposed. At the 100m floor, isothermal optimistic climate mass is 11.73kg versus 55.34kg with the chosen lapse; both-weather values are 403.66 versus 441.77kg.",
  "next_evidence": "Supply measured or approved temperature, pressure, humidity and inversion profiles, including joint extremes and occurrence probabilities."
}
```

### N484 — NFI-031-SATURATION

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/2`.

```json
{
  "id": "NFI-031-SATURATION",
  "tag": "QUESTIONABLE",
  "issue": "The conservative high-pressure humid day becomes supersaturated in the all-weather 500m-floor diagnostic. The 0/10/100m-floor main cases are unsaturated in the stated model. Continuing an unsaturated lapse through cloud is not a physical forecast.",
  "next_evidence": "Use a moist atmospheric profile with cloud/condensate treatment; do not treat that diagnostic height as an operational guarantee."
}
```

### N485 — NFI-031-CONTROL

Source `rpt-ref-9a0319231d2fe686eb92`; original file `unpublished-local-ref:69de0f6680e1695f; pointer `/rows/3`.

```json
{
  "id": "NFI-031-CONTROL",
  "tag": "PROJECTION",
  "issue": "A fixed evacuated hull has one passive equilibrium per weather profile and carried load. Positive C raises its ISA float altitude; C=0 cannot float at 500m ISA and satisfy the illustrative sea-level-ground clearance on both 019 hot-day extremes. Static equilibrium does not provide station keeping.",
  "next_evidence": "Resolve the mission requirement; size active altitude control, tethering, launch, landing, descent-rate and gust response if needed."
}
```

### C165 — 040-03-combined_weather_thermal

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/2`.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

### C181 — 040-19-weather_requirement

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/18`.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

## R091 — Tensile bending and coupled shell/column/curvature limits

**030b source history:** CHECK-022b/022c identifies omitted tensile bending and local/column interaction. 022d includes a projected Ft15.586 MPa ceiling; the screened lead has zero tension at its target, while coupled instability remains open.

**Original question:** Tensile bending and coupled shell/column/curvature limits

### N382 — NFI-025-MODEL

Source `rpt-ref-58c781cbea9c220eb5b4`; original file `unpublished-local-ref:9c7427840ddc3f05; pointer `/rows/14`.

```json
{
  "id": "NFI-025-MODEL",
  "status": "OPEN",
  "classification": "QUESTIONABLE",
  "target_transfer": "PROJECTION",
  "evidence_state": "PROJECTION",
  "issue": "Arc, shell, column and global instability are represented by separate surrogate minima.",
  "factor": {
    "a0_over_s": 0.001,
    "global_k": 0.2,
    "local_C": 0.6,
    "s_bounds_m": [
      0.4,
      3.0
    ],
    "ro_cap_m": 0.25,
    "additional_ro_cap": "s/3",
    "exact_arc_to_chord_length_factor_at_original": 1.0017421688750303
  },
  "required_next_evidence": "Discrete imperfect spherical frame analysis with real joints and curved members, boundary conditions and orthotropic CMC constitutive response.",
  "note": "Perry equation here is an elastic extreme-fiber stress criterion for an assumed bow; it is not a ceramic code allowable. No post-Euler finite stress is claimed. SourceE410 GPa is retained for reproduction, not treated as a qualified same-lot manufacturer property."
}
```

### N458 — NFI-C022-TENSILE-BENDING

Source `rpt-ref-f6de390e1555b4ca8e78`; original file `unpublished-local-ref:a3c00555c78ad754; pointer `/rows/1`.

```json
{
  "id": "NFI-C022-TENSILE-BENDING",
  "kind": "DEMONSTRATED omitted mode",
  "issue": "Long-span projected rows develop substantial tensile stress at their claimed least multipliers; Perry limits compression only.",
  "evidence": {
    "GAMMA/percent_crush_5": {
      "published_limit_stresses": {
        "pressure_multiplier": 1.3752490300405331,
        "mean_compression_Pa": 1368049238.3685298,
        "bending_Pa": 2032684954.1446717,
        "maximum_compression_Pa": 3400734192.5132017,
        "opposite_signed_compression_Pa": -664635715.7761419,
        "maximum_tension_Pa": 664635715.7761419
      },
      "full_pressure_stresses": {
        "pressure_multiplier": 1.0,
        "mean_compression_Pa": 994764736.0479934,
        "bending_Pa": 241868946.52114338,
        "maximum_compression_Pa": 1236633682.5691369,
        "opposite_signed_compression_Pa": 752895789.52685,
        "maximum_tension_Pa": 0.0
      },
      "fixed_tensile_screens": [
        {
          "Ft_assumed_Pa": 0.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 348.8563570154232,
            "m_joint": 207.4777195253605,
            "m_tube": 3799.8907444488163,
            "m_end": 0.9013453336183757,
            "reserve": 432.4100401574281,
            "sag_kg": 187.9379326479281,
            "vehicle": 4457.032110032571,
            "s_m": 6.15,
            "r_o_m": 0.16764593114772616,
            "t_film_m": 0.00028619697756719387,
            "t_w_m": 0.0016252746475689662,
            "rt": 103.14929319699017,
            "A_m2": 0.001703685211121064,
            "I_m4": 2.3710194159910224e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 994764736.0479934,
            "k": 0.2,
            "gamma": 0.5765839731705817,
            "SF_local_gamma1": 2.3974439874149858,
            "SF_least": 1.339579282627512,
            "eta": 0.0753038303852024,
            "Euler_stress_Pa": 1441085488.7107694,
            "mass_closure_kg": 4889.442150189999,
            "radius_cap_fraction": 0.6705837245909047,
            "NASA_L_over_midradius": 37.47029245298272,
            "SF_yield": 3.920524983117054,
            "SF_euler": 1.4486696567430821,
            "SF_local": 1.3823277797176547,
            "SF_film": 1.4624665443017892,
            "SF_perry": 1.3888254730869842,
            "SF_global": 1.3752490300405331,
            "SF_tension": 1.339579282627512,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.339579282627512,
            "k04_SF_global": 2.7504980600810662,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 994764736.0479934,
              "bending_Pa": 241868946.52114338,
              "maximum_compression_Pa": 1236633682.5691369,
              "opposite_signed_compression_Pa": 752895789.52685,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.339579282627512,
              "mean_compression_Pa": 1332566231.4983172,
              "bending_Pa": 1332566231.4983194,
              "maximum_compression_Pa": 2665132462.9966364,
              "opposite_signed_compression_Pa": -2.1457672119140625e-06,
              "maximum_tension_Pa": 2.1457672119140625e-06
            }
          }
        },
        {
          "Ft_assumed_Pa": 7192000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 348.8563570154232,
            "m_joint": 207.4777195253605,
            "m_tube": 3799.8907444488163,
            "m_end": 0.9013453336183757,
            "reserve": 432.4100401574281,
            "sag_kg": 187.9379326479281,
            "vehicle": 4457.032110032571,
            "s_m": 6.15,
            "r_o_m": 0.16764593114772616,
            "t_film_m": 0.00028619697756719387,
            "t_w_m": 0.0016252746475689662,
            "rt": 103.14929319699017,
            "A_m2": 0.001703685211121064,
            "I_m4": 2.3710194159910224e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 994764736.0479934,
            "k": 0.2,
            "gamma": 0.5765839731705817,
            "SF_local_gamma1": 2.3974439874149858,
            "SF_least": 1.3401646398232967,
            "eta": 0.0753038303852024,
            "Euler_stress_Pa": 1441085488.7107694,
            "mass_closure_kg": 4889.442150189999,
            "radius_cap_fraction": 0.6705837245909047,
            "NASA_L_over_midradius": 37.47029245298272,
            "SF_yield": 3.920524983117054,
            "SF_euler": 1.4486696567430821,
            "SF_local": 1.3823277797176547,
            "SF_film": 1.4624665443017892,
            "SF_perry": 1.3888254730869842,
            "SF_global": 1.3752490300405331,
            "SF_tension": 1.3401646398232967,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.3401646398232967,
            "k04_SF_global": 2.7504980600810662,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 994764736.0479934,
              "bending_Pa": 241868946.52114338,
              "maximum_compression_Pa": 1236633682.5691369,
              "opposite_signed_compression_Pa": 752895789.52685,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.3401646398232967,
              "mean_compression_Pa": 1333148524.194676,
              "bending_Pa": 1340340524.194678,
              "maximum_compression_Pa": 2673489048.3893538,
              "opposite_signed_compression_Pa": -7192000.000002146,
              "maximum_tension_Pa": 7192000.000002146
            }
          }
        },
        {
          "Ft_assumed_Pa": 15586000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 348.8563570154232,
            "m_joint": 207.4777195253605,
            "m_tube": 3799.8907444488163,
            "m_end": 0.9013453336183757,
            "reserve": 432.4100401574281,
            "sag_kg": 187.9379326479281,
            "vehicle": 4457.032110032571,
            "s_m": 6.15,
            "r_o_m": 0.16764593114772616,
            "t_film_m": 0.00028619697756719387,
            "t_w_m": 0.0016252746475689662,
            "rt": 103.14929319699017,
            "A_m2": 0.001703685211121064,
            "I_m4": 2.3710194159910224e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 994764736.0479934,
            "k": 0.2,
            "gamma": 0.5765839731705817,
            "SF_local_gamma1": 2.3974439874149858,
            "SF_least": 1.3408393059278276,
            "eta": 0.0753038303852024,
            "Euler_stress_Pa": 1441085488.7107694,
            "mass_closure_kg": 4889.442150189999,
            "radius_cap_fraction": 0.6705837245909047,
            "NASA_L_over_midradius": 37.47029245298272,
            "SF_yield": 3.920524983117054,
            "SF_euler": 1.4486696567430821,
            "SF_local": 1.3823277797176547,
            "SF_film": 1.4624665443017892,
            "SF_perry": 1.3888254730869842,
            "SF_global": 1.3752490300405331,
            "SF_tension": 1.3408393059278276,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.3408393059278276,
            "k04_SF_global": 2.7504980600810662,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 994764736.0479934,
              "bending_Pa": 241868946.52114338,
              "maximum_compression_Pa": 1236633682.5691369,
              "opposite_signed_compression_Pa": 752895789.52685,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.3408393059278276,
              "mean_compression_Pa": 1333819658.24407,
              "bending_Pa": 1349405658.2440708,
              "maximum_compression_Pa": 2683225316.488141,
              "opposite_signed_compression_Pa": -15586000.000000715,
              "maximum_tension_Pa": 15586000.000000715
            }
          }
        },
        {
          "Ft_assumed_Pa": 380000000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 348.8563570154232,
            "m_joint": 207.4777195253605,
            "m_tube": 3799.8907444488163,
            "m_end": 0.9013453336183757,
            "reserve": 432.4100401574281,
            "sag_kg": 187.9379326479281,
            "vehicle": 4457.032110032571,
            "s_m": 6.15,
            "r_o_m": 0.16764593114772616,
            "t_film_m": 0.00028619697756719387,
            "t_w_m": 0.0016252746475689662,
            "rt": 103.14929319699017,
            "A_m2": 0.001703685211121064,
            "I_m4": 2.3710194159910224e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 994764736.0479934,
            "k": 0.2,
            "gamma": 0.5765839731705817,
            "SF_local_gamma1": 2.3974439874149858,
            "SF_least": 1.3634541644184013,
            "eta": 0.0753038303852024,
            "Euler_stress_Pa": 1441085488.7107694,
            "mass_closure_kg": 4889.442150189999,
            "radius_cap_fraction": 0.6705837245909047,
            "NASA_L_over_midradius": 37.47029245298272,
            "SF_yield": 3.920524983117054,
            "SF_euler": 1.4486696567430821,
            "SF_local": 1.3823277797176547,
            "SF_film": 1.4624665443017892,
            "SF_perry": 1.3888254730869842,
            "SF_global": 1.3752490300405331,
            "SF_tension": 1.3634541644184013,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.3634541644184013,
            "k04_SF_global": 2.7504980600810662,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 994764736.0479934,
              "bending_Pa": 241868946.52114338,
              "maximum_compression_Pa": 1236633682.5691369,
              "opposite_signed_compression_Pa": 752895789.52685,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.3634541644184013,
              "mean_compression_Pa": 1356316121.9812083,
              "bending_Pa": 1736316121.9812088,
              "maximum_compression_Pa": 3092632243.962417,
              "opposite_signed_compression_Pa": -380000000.0000005,
              "maximum_tension_Pa": 380000000.0000005
            }
          }
        }
      ],
      "hypothetical_uniform_volume_caps": [
        {
          "m": 8,
          "volume_m3": 1.225771207886715,
          "reference_m3": 1.4814814814814816e-08,
          "tensile_cap_Pa": 7347459.70192971,
          "classification": "PROJECTION from025 hypotheses; actual stressed size and compression law unknown"
        },
        {
          "m": 10,
          "volume_m3": 1.225771207886715,
          "reference_m3": 1.1900826446280993e-08,
          "tensile_cap_Pa": 15854761.556220949,
          "classification": "PROJECTION from025 hypotheses; actual stressed size and compression law unknown"
        }
      ]
    },
    "GAMMA/percent_crush_019": {
      "published_limit_stresses": {
        "pressure_multiplier": 1.2986375988562082,
        "mean_compression_Pa": 1346468388.8543727,
        "bending_Pa": 2426883132.519814,
        "maximum_compression_Pa": 3773351521.3741865,
        "opposite_signed_compression_Pa": -1080414743.6654413,
        "maximum_tension_Pa": 1080414743.6654413
      },
      "full_pressure_stresses": {
        "pressure_multiplier": 1.0,
        "mean_compression_Pa": 1036831514.8431649,
        "bending_Pa": 301073241.13351405,
        "maximum_compression_Pa": 1337904755.9766788,
        "opposite_signed_compression_Pa": 735758273.7096509,
        "maximum_tension_Pa": 0.0
      },
      "fixed_tensile_screens": [
        {
          "Ft_assumed_Pa": 0.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 344.1444741266027,
            "m_joint": 199.53358445097257,
            "m_tube": 3645.719925849878,
            "m_end": 0.8668336323363574,
            "reserve": 599.2368767195755,
            "sag_kg": 187.9379326479281,
            "vehicle": 4290.205273470424,
            "s_m": 6.15,
            "r_o_m": 0.16557534691311998,
            "t_film_m": 0.00028233141337633867,
            "t_w_m": 0.0015787064452148203,
            "rt": 104.880389520795,
            "A_m2": 0.0016345625543664844,
            "I_m4": 2.2193311326653438e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 1036831514.8431649,
            "k": 0.2,
            "gamma": 0.5740574353678207,
            "SF_local_gamma1": 2.262208480975638,
            "SF_least": 1.2526179904975867,
            "eta": 0.07623333524508422,
            "Euler_stress_Pa": 1405932751.3750303,
            "mass_closure_kg": 4889.44215019,
            "radius_cap_fraction": 0.6623013876524799,
            "NASA_L_over_midradius": 37.93582312716548,
            "SF_yield": 3.7614597397629534,
            "SF_euler": 1.3559896002849576,
            "SF_local": 1.2986375988562082,
            "SF_film": 1.4427135114359915,
            "SF_perry": 1.3013105709566728,
            "SF_global": 1.3032596246282744,
            "SF_tension": 1.2526179904975867,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.2526179904975867,
            "k04_SF_global": 2.6065192492565488,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 1036831514.8431649,
              "bending_Pa": 301073241.13351405,
              "maximum_compression_Pa": 1337904755.9766788,
              "opposite_signed_compression_Pa": 735758273.7096509,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.2526179904975867,
              "mean_compression_Pa": 1298753808.607414,
              "bending_Pa": 1298753808.6074154,
              "maximum_compression_Pa": 2597507617.2148294,
              "opposite_signed_compression_Pa": -1.430511474609375e-06,
              "maximum_tension_Pa": 1.430511474609375e-06
            }
          }
        },
        {
          "Ft_assumed_Pa": 7192000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 344.1444741266027,
            "m_joint": 199.53358445097257,
            "m_tube": 3645.719925849878,
            "m_end": 0.8668336323363574,
            "reserve": 599.2368767195755,
            "sag_kg": 187.9379326479281,
            "vehicle": 4290.205273470424,
            "s_m": 6.15,
            "r_o_m": 0.16557534691311998,
            "t_film_m": 0.00028233141337633867,
            "t_w_m": 0.0015787064452148203,
            "rt": 104.880389520795,
            "A_m2": 0.0016345625543664844,
            "I_m4": 2.2193311326653438e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 1036831514.8431649,
            "k": 0.2,
            "gamma": 0.5740574353678207,
            "SF_local_gamma1": 2.262208480975638,
            "SF_least": 1.2531870132703653,
            "eta": 0.07623333524508422,
            "Euler_stress_Pa": 1405932751.3750303,
            "mass_closure_kg": 4889.44215019,
            "radius_cap_fraction": 0.6623013876524799,
            "NASA_L_over_midradius": 37.93582312716548,
            "SF_yield": 3.7614597397629534,
            "SF_euler": 1.3559896002849576,
            "SF_local": 1.2986375988562082,
            "SF_film": 1.4427135114359915,
            "SF_perry": 1.3013105709566728,
            "SF_global": 1.3032596246282744,
            "SF_tension": 1.2531870132703653,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.2531870132703653,
            "k04_SF_global": 2.6065192492565488,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 1036831514.8431649,
              "bending_Pa": 301073241.13351405,
              "maximum_compression_Pa": 1337904755.9766788,
              "opposite_signed_compression_Pa": 735758273.7096509,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.2531870132703653,
              "mean_compression_Pa": 1299343789.3508942,
              "bending_Pa": 1306535789.350896,
              "maximum_compression_Pa": 2605879578.70179,
              "opposite_signed_compression_Pa": -7192000.000001669,
              "maximum_tension_Pa": 7192000.000001669
            }
          }
        },
        {
          "Ft_assumed_Pa": 15586000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 344.1444741266027,
            "m_joint": 199.53358445097257,
            "m_tube": 3645.719925849878,
            "m_end": 0.8668336323363574,
            "reserve": 599.2368767195755,
            "sag_kg": 187.9379326479281,
            "vehicle": 4290.205273470424,
            "s_m": 6.15,
            "r_o_m": 0.16557534691311998,
            "t_film_m": 0.00028233141337633867,
            "t_w_m": 0.0015787064452148203,
            "rt": 104.880389520795,
            "A_m2": 0.0016345625543664844,
            "I_m4": 2.2193311326653438e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 1036831514.8431649,
            "k": 0.2,
            "gamma": 0.5740574353678207,
            "SF_local_gamma1": 2.262208480975638,
            "SF_least": 1.2538426318841922,
            "eta": 0.07623333524508422,
            "Euler_stress_Pa": 1405932751.3750303,
            "mass_closure_kg": 4889.44215019,
            "radius_cap_fraction": 0.6623013876524799,
            "NASA_L_over_midradius": 37.93582312716548,
            "SF_yield": 3.7614597397629534,
            "SF_euler": 1.3559896002849576,
            "SF_local": 1.2986375988562082,
            "SF_film": 1.4427135114359915,
            "SF_perry": 1.3013105709566728,
            "SF_global": 1.3032596246282744,
            "SF_tension": 1.2538426318841922,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.2538426318841922,
            "k04_SF_global": 2.6065192492565488,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 1036831514.8431649,
              "bending_Pa": 301073241.13351405,
              "maximum_compression_Pa": 1337904755.9766788,
              "opposite_signed_compression_Pa": 735758273.7096509,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.2538426318841922,
              "mean_compression_Pa": 1300023555.3914278,
              "bending_Pa": 1315609555.3914273,
              "maximum_compression_Pa": 2615633110.782855,
              "opposite_signed_compression_Pa": -15585999.999999523,
              "maximum_tension_Pa": 15585999.999999523
            }
          }
        },
        {
          "Ft_assumed_Pa": 380000000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 344.1444741266027,
            "m_joint": 199.53358445097257,
            "m_tube": 3645.719925849878,
            "m_end": 0.8668336323363574,
            "reserve": 599.2368767195755,
            "sag_kg": 187.9379326479281,
            "vehicle": 4290.205273470424,
            "s_m": 6.15,
            "r_o_m": 0.16557534691311998,
            "t_film_m": 0.00028233141337633867,
            "t_w_m": 0.0015787064452148203,
            "rt": 104.880389520795,
            "A_m2": 0.0016345625543664844,
            "I_m4": 2.2193311326653438e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 1036831514.8431649,
            "k": 0.2,
            "gamma": 0.5740574353678207,
            "SF_local_gamma1": 2.262208480975638,
            "SF_least": 1.2756882996643435,
            "eta": 0.07623333524508422,
            "Euler_stress_Pa": 1405932751.3750303,
            "mass_closure_kg": 4889.44215019,
            "radius_cap_fraction": 0.6623013876524799,
            "NASA_L_over_midradius": 37.93582312716548,
            "SF_yield": 3.7614597397629534,
            "SF_euler": 1.3559896002849576,
            "SF_local": 1.2986375988562082,
            "SF_film": 1.4427135114359915,
            "SF_perry": 1.3013105709566728,
            "SF_global": 1.3032596246282744,
            "SF_tension": 1.2756882996643435,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.2756882996643435,
            "k04_SF_global": 2.6065192492565488,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 1036831514.8431649,
              "bending_Pa": 301073241.13351405,
              "maximum_compression_Pa": 1337904755.9766788,
              "opposite_signed_compression_Pa": 735758273.7096509,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.2756882996643435,
              "mean_compression_Pa": 1322673832.2086825,
              "bending_Pa": 1702673832.2086816,
              "maximum_compression_Pa": 3025347664.417364,
              "opposite_signed_compression_Pa": -379999999.99999905,
              "maximum_tension_Pa": 379999999.99999905
            }
          }
        }
      ],
      "hypothetical_uniform_volume_caps": [
        {
          "m": 8,
          "volume_m3": 1.1760386857580252,
          "reference_m3": 1.4814814814814816e-08,
          "tensile_cap_Pa": 7385598.401354333,
          "classification": "PROJECTION from025 hypotheses; actual stressed size and compression law unknown"
        },
        {
          "m": 10,
          "volume_m3": 1.1760386857580252,
          "reference_m3": 1.1900826446280993e-08,
          "tensile_cap_Pa": 15920565.715653459,
          "classification": "PROJECTION from025 hypotheses; actual stressed size and compression law unknown"
        }
      ]
    },
    "022c_cap/projection_5": {
      "published_limit_stresses": {
        "pressure_multiplier": 1.3733213857843127,
        "mean_compression_Pa": 1368010504.1229851,
        "bending_Pa": 2033750657.4313748,
        "maximum_compression_Pa": 3401761161.55436,
        "opposite_signed_compression_Pa": -665740153.3083897,
        "maximum_tension_Pa": 665740153.3083897
      },
      "full_pressure_stresses": {
        "pressure_multiplier": 1.0,
        "mean_compression_Pa": 996132819.5160271,
        "bending_Pa": 242982415.75261784,
        "maximum_compression_Pa": 1239115235.2686448,
        "opposite_signed_compression_Pa": 753150403.7634093,
        "maximum_tension_Pa": 0.0
      },
      "fixed_tensile_screens": [
        {
          "Ft_assumed_Pa": 0.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 348.8563570154232,
            "m_joint": 207.21678204764845,
            "m_tube": 3794.671994894575,
            "m_end": 0.9002117430890411,
            "reserve": 437.88972718938203,
            "sag_kg": 193.417619679882,
            "vehicle": 4451.552423000618,
            "s_m": 6.15,
            "r_o_m": 0.16764011960487946,
            "t_film_m": 0.00028619697756719387,
            "t_w_m": 0.001623088408707305,
            "rt": 103.28465085792524,
            "A_m2": 0.0017013453789958654,
            "I_m4": 2.3676289932865346e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 996132819.5160271,
            "k": 0.2,
            "gamma": 0.5763851730392059,
            "SF_local_gamma1": 2.3910137429040064,
            "SF_least": 1.3376613681602227,
            "eta": 0.07530548419597233,
            "Euler_stress_Pa": 1441003885.5529516,
            "mass_closure_kg": 4889.442150189999,
            "radius_cap_fraction": 0.6705604784195178,
            "NASA_L_over_midradius": 37.471352227693885,
            "SF_yield": 3.9151405551468748,
            "SF_euler": 1.4465981416545093,
            "SF_local": 1.3781448699428451,
            "SF_film": 1.4624665443017892,
            "SF_perry": 1.3868432138641869,
            "SF_global": 1.3733213857843127,
            "SF_tension": 1.3376613681602227,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.3376613681602227,
            "k04_SF_global": 2.7466427715686255,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 996132819.5160271,
              "bending_Pa": 242982415.75261784,
              "maximum_compression_Pa": 1239115235.2686448,
              "opposite_signed_compression_Pa": 753150403.7634093,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.3376613681602227,
              "mean_compression_Pa": 1332488390.223109,
              "bending_Pa": 1332488390.223108,
              "maximum_compression_Pa": 2664976780.446217,
              "opposite_signed_compression_Pa": 9.5367431640625e-07,
              "maximum_tension_Pa": 0.0
            }
          }
        },
        {
          "Ft_assumed_Pa": 7192000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 348.8563570154232,
            "m_joint": 207.21678204764845,
            "m_tube": 3794.671994894575,
            "m_end": 0.9002117430890411,
            "reserve": 437.88972718938203,
            "sag_kg": 193.417619679882,
            "vehicle": 4451.552423000618,
            "s_m": 6.15,
            "r_o_m": 0.16764011960487946,
            "t_film_m": 0.00028619697756719387,
            "t_w_m": 0.001623088408707305,
            "rt": 103.28465085792524,
            "A_m2": 0.0017013453789958654,
            "I_m4": 2.3676289932865346e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 996132819.5160271,
            "k": 0.2,
            "gamma": 0.5763851730392059,
            "SF_local_gamma1": 2.3910137429040064,
            "SF_least": 1.3382459351089186,
            "eta": 0.07530548419597233,
            "Euler_stress_Pa": 1441003885.5529516,
            "mass_closure_kg": 4889.442150189999,
            "radius_cap_fraction": 0.6705604784195178,
            "NASA_L_over_midradius": 37.471352227693885,
            "SF_yield": 3.9151405551468748,
            "SF_euler": 1.4465981416545093,
            "SF_local": 1.3781448699428451,
            "SF_film": 1.4624665443017892,
            "SF_perry": 1.3868432138641869,
            "SF_global": 1.3733213857843127,
            "SF_tension": 1.3382459351089186,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.3382459351089186,
            "k04_SF_global": 2.7466427715686255,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 996132819.5160271,
              "bending_Pa": 242982415.75261784,
              "maximum_compression_Pa": 1239115235.2686448,
              "opposite_signed_compression_Pa": 753150403.7634093,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.3382459351089186,
              "mean_compression_Pa": 1333070696.5459094,
              "bending_Pa": 1340262696.5459082,
              "maximum_compression_Pa": 2673333393.091818,
              "opposite_signed_compression_Pa": -7191999.999998808,
              "maximum_tension_Pa": 7191999.999998808
            }
          }
        },
        {
          "Ft_assumed_Pa": 15586000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 348.8563570154232,
            "m_joint": 207.21678204764845,
            "m_tube": 3794.671994894575,
            "m_end": 0.9002117430890411,
            "reserve": 437.88972718938203,
            "sag_kg": 193.417619679882,
            "vehicle": 4451.552423000618,
            "s_m": 6.15,
            "r_o_m": 0.16764011960487946,
            "t_film_m": 0.00028619697756719387,
            "t_w_m": 0.001623088408707305,
            "rt": 103.28465085792524,
            "A_m2": 0.0017013453789958654,
            "I_m4": 2.3676289932865346e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 996132819.5160271,
            "k": 0.2,
            "gamma": 0.5763851730392059,
            "SF_local_gamma1": 2.3910137429040064,
            "SF_least": 1.3389196898920168,
            "eta": 0.07530548419597233,
            "Euler_stress_Pa": 1441003885.5529516,
            "mass_closure_kg": 4889.442150189999,
            "radius_cap_fraction": 0.6705604784195178,
            "NASA_L_over_midradius": 37.471352227693885,
            "SF_yield": 3.9151405551468748,
            "SF_euler": 1.4465981416545093,
            "SF_local": 1.3781448699428451,
            "SF_film": 1.4624665443017892,
            "SF_perry": 1.3868432138641869,
            "SF_global": 1.3733213857843127,
            "SF_tension": 1.3389196898920168,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.3389196898920168,
            "k04_SF_global": 2.7466427715686255,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 996132819.5160271,
              "bending_Pa": 242982415.75261784,
              "maximum_compression_Pa": 1239115235.2686448,
              "opposite_signed_compression_Pa": 753150403.7634093,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.3389196898920168,
              "mean_compression_Pa": 1333741845.7976594,
              "bending_Pa": 1349327845.7976618,
              "maximum_compression_Pa": 2683069691.595321,
              "opposite_signed_compression_Pa": -15586000.000002384,
              "maximum_tension_Pa": 15586000.000002384
            }
          }
        },
        {
          "Ft_assumed_Pa": 380000000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 348.8563570154232,
            "m_joint": 207.21678204764845,
            "m_tube": 3794.671994894575,
            "m_end": 0.9002117430890411,
            "reserve": 437.88972718938203,
            "sag_kg": 193.417619679882,
            "vehicle": 4451.552423000618,
            "s_m": 6.15,
            "r_o_m": 0.16764011960487946,
            "t_film_m": 0.00028619697756719387,
            "t_w_m": 0.001623088408707305,
            "rt": 103.28465085792524,
            "A_m2": 0.0017013453789958654,
            "I_m4": 2.3676289932865346e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 996132819.5160271,
            "k": 0.2,
            "gamma": 0.5763851730392059,
            "SF_local_gamma1": 2.3910137429040064,
            "SF_least": 1.3615036994282919,
            "eta": 0.07530548419597233,
            "Euler_stress_Pa": 1441003885.5529516,
            "mass_closure_kg": 4889.442150189999,
            "radius_cap_fraction": 0.6705604784195178,
            "NASA_L_over_midradius": 37.471352227693885,
            "SF_yield": 3.9151405551468748,
            "SF_euler": 1.4465981416545093,
            "SF_local": 1.3781448699428451,
            "SF_film": 1.4624665443017892,
            "SF_perry": 1.3868432138641869,
            "SF_global": 1.3733213857843127,
            "SF_tension": 1.3615036994282919,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.3615036994282919,
            "k04_SF_global": 2.7466427715686255,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 996132819.5160271,
              "bending_Pa": 242982415.75261784,
              "maximum_compression_Pa": 1239115235.2686448,
              "opposite_signed_compression_Pa": 753150403.7634093,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.3615036994282919,
              "mean_compression_Pa": 1356238518.8930058,
              "bending_Pa": 1736238518.893004,
              "maximum_compression_Pa": 3092477037.78601,
              "opposite_signed_compression_Pa": -379999999.9999981,
              "maximum_tension_Pa": 379999999.9999981
            }
          }
        }
      ],
      "reoptimized_tensile_screens": [
        {
          "Ft_assumed_Pa": 15586000.0,
          "result": {
            "nodes": 41.314846185279634,
            "members": 117.9445385558389,
            "n_coef": 17.53762189883066,
            "m_nodes": 0.8262969237055927,
            "m_film": 325.636362676227,
            "m_joint": 207.32878839474785,
            "m_tube": 3820.113108295024,
            "m_end": 0.8789249207015696,
            "reserve": 435.53759390029506,
            "sag_kg": 191.06548639079503,
            "vehicle": 4453.9045562897045,
            "s_m": 6.075210434541454,
            "r_o_m": 0.16749614634525517,
            "t_film_m": 0.00026714761221848817,
            "t_w_m": 0.0016161214220337203,
            "rt": 103.64081811036124,
            "A_m2": 0.001692615892148196,
            "I_m4": 2.3515149400385015e-05,
            "length_m": 6.17274417532397,
            "N_N": 1674156.0814795368,
            "sigma_axial_Pa": 989093916.2545433,
            "k": 0.2,
            "gamma": 0.5758630852579553,
            "SF_local_gamma1": 2.399754109052355,
            "SF_least": 1.381929805095042,
            "eta": 0.07442070326035428,
            "Euler_stress_Pa": 1475422403.0313873,
            "mass_closure_kg": 4889.44215019,
            "radius_cap_fraction": 0.6699845853810207,
            "NASA_L_over_midradius": 37.03170596648851,
            "SF_yield": 3.943002717849429,
            "SF_euler": 1.491690909007358,
            "SF_local": 1.3819298050993447,
            "SF_film": 1.381929805117712,
            "SF_perry": 1.4286160793414124,
            "SF_global": 1.381929805095042,
            "SF_tension": 1.3819298054166547,
            "governing": "global",
            "k04_governing": "local",
            "k04_SF_least": 1.3819298050993447,
            "k04_SF_global": 2.763859610190084,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 989093916.2545433,
              "bending_Pa": 223315035.5806854,
              "maximum_compression_Pa": 1212408951.8352287,
              "opposite_signed_compression_Pa": 765778880.6738579,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.381929805095042,
              "mean_compression_Pa": 1366858362.9103327,
              "bending_Pa": 1382444358.855985,
              "maximum_compression_Pa": 2749302721.7663174,
              "opposite_signed_compression_Pa": -15585995.945652246,
              "maximum_tension_Pa": 15585995.945652246
            },
            "search": {
              "method": "independent differential evolution plus bounded-accepted simplex",
              "seed": 835,
              "spacing_upper_m": 8.0,
              "outer_radius_upper_m": 0.25,
              "evaluations": 6634,
              "DE_success": true,
              "DE_message": "Optimization terminated successfully.",
              "certified_global_optimum": false
            }
          }
        },
        {
          "Ft_assumed_Pa": 380000000.0,
          "result": {
            "nodes": 40.61201925740656,
            "members": 115.83605777221968,
            "n_coef": 17.69651449192068,
            "m_nodes": 0.8122403851481312,
            "m_film": 328.9362639710256,
            "m_joint": 207.24635638289033,
            "m_tube": 3815.178623301633,
            "m_end": 0.8945675481740759,
            "reserve": 437.2686661493018,
            "sag_kg": 192.79655863980182,
            "vehicle": 4452.173484040697,
            "s_m": 6.13025244337711,
            "r_o_m": 0.16794341030235543,
            "t_film_m": 0.0002698548060472641,
            "t_w_m": 0.0016238480677555115,
            "rt": 103.42310566929295,
            "A_m2": 0.0017052322457962955,
            "I_m4": 2.3816631696578323e-05,
            "length_m": 6.230542701771417,
            "N_N": 1689324.1015542224,
            "sigma_axial_Pa": 990670980.8700314,
            "k": 0.2,
            "gamma": 0.576182044370325,
            "SF_local_gamma1": 2.400977501466651,
            "SF_least": 1.3834001252619486,
            "eta": 0.0749190118332651,
            "Euler_stress_Pa": 1455890300.2887123,
            "mass_closure_kg": 4889.442150189999,
            "radius_cap_fraction": 0.6717736412094217,
            "NASA_L_over_midradius": 37.27928734961861,
            "SF_yield": 3.936725790206275,
            "SF_euler": 1.46960022893788,
            "SF_local": 1.3834001252822101,
            "SF_film": 1.3834001252645491,
            "SF_perry": 1.408276978646805,
            "SF_global": 1.3834001252651573,
            "SF_tension": 1.3834001252619486,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.3834001252619486,
            "k04_SF_global": 2.7668002505303146,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 990670980.8700314,
              "bending_Pa": 232269611.28610206,
              "maximum_compression_Pa": 1222940592.1561334,
              "opposite_signed_compression_Pa": 758401369.5839293,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.3834001252619486,
              "mean_compression_Pa": 1370494359.0289788,
              "bending_Pa": 1750494359.028983,
              "maximum_compression_Pa": 3120988718.057962,
              "opposite_signed_compression_Pa": -380000000.0000043,
              "maximum_tension_Pa": 380000000.0000043
            },
            "search": {
              "method": "independent differential evolution plus bounded-accepted simplex",
              "seed": 835,
              "spacing_upper_m": 8.0,
              "outer_radius_upper_m": 0.25,
              "evaluations": 6466,
              "DE_success": true,
              "DE_message": "Optimization terminated successfully.",
              "certified_global_optimum": false
            }
          }
        }
      ],
      "hypothetical_uniform_volume_caps": [
        {
          "m": 8,
          "volume_m3": 1.2240877402885726,
          "reference_m3": 1.4814814814814816e-08,
          "tensile_cap_Pa": 7348722.04754574,
          "classification": "PROJECTION from025 hypotheses; actual stressed size and compression law unknown"
        },
        {
          "m": 10,
          "volume_m3": 1.2240877402885726,
          "reference_m3": 1.1900826446280993e-08,
          "tensile_cap_Pa": 15856940.68704671,
          "classification": "PROJECTION from025 hypotheses; actual stressed size and compression law unknown"
        }
      ]
    },
    "022c_cap/projection_019": {
      "published_limit_stresses": {
        "pressure_multiplier": 1.294540344662803,
        "mean_compression_Pa": 1344144332.8715324,
        "bending_Pa": 2334687151.0702324,
        "maximum_compression_Pa": 3678831483.941765,
        "opposite_signed_compression_Pa": -990542818.1987,
        "maximum_tension_Pa": 990542818.1987
      },
      "full_pressure_stresses": {
        "pressure_multiplier": 1.0,
        "mean_compression_Pa": 1038317838.7705252,
        "bending_Pa": 302782600.48988324,
        "maximum_compression_Pa": 1341100439.2604084,
        "opposite_signed_compression_Pa": 735535238.280642,
        "maximum_tension_Pa": 0.0
      },
      "fixed_tensile_screens": [
        {
          "Ft_assumed_Pa": 0.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 344.1444741266027,
            "m_joint": 199.27264697326052,
            "m_tube": 3640.501176295637,
            "m_end": 0.8657000418070226,
            "reserve": 604.7165637515294,
            "sag_kg": 193.417619679882,
            "vehicle": 4284.725586438471,
            "s_m": 6.15,
            "r_o_m": 0.1655692772803688,
            "t_film_m": 0.00028233141337633867,
            "t_w_m": 0.0015764940543974584,
            "rt": 105.0237245224816,
            "A_m2": 0.0016322227222412859,
            "I_m4": 2.216020579405737e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 1038317838.7705252,
            "k": 0.2,
            "gamma": 0.5738497729022546,
            "SF_local_gamma1": 2.2558871777811187,
            "SF_least": 1.2507470324784735,
            "eta": 0.0762351379029742,
            "Euler_stress_Pa": 1405847969.431958,
            "mass_closure_kg": 4889.44215019,
            "radius_cap_fraction": 0.6622771091214752,
            "NASA_L_over_midradius": 37.93696580773276,
            "SF_yield": 3.7560753117927743,
            "SF_euler": 1.353966884645482,
            "SF_local": 1.294540344662803,
            "SF_film": 1.4427135114359915,
            "SF_perry": 1.2993729363738866,
            "SF_global": 1.301354804129081,
            "SF_tension": 1.2507470324784735,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.2507470324784735,
            "k04_SF_global": 2.602709608258162,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 1038317838.7705252,
              "bending_Pa": 302782600.48988324,
              "maximum_compression_Pa": 1341100439.2604084,
              "opposite_signed_compression_Pa": 735535238.280642,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.2507470324784735,
              "mean_compression_Pa": 1298672955.6116965,
              "bending_Pa": 1298672955.6116984,
              "maximum_compression_Pa": 2597345911.223395,
              "opposite_signed_compression_Pa": -1.9073486328125e-06,
              "maximum_tension_Pa": 1.9073486328125e-06
            }
          }
        },
        {
          "Ft_assumed_Pa": 7192000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 344.1444741266027,
            "m_joint": 199.27264697326052,
            "m_tube": 3640.501176295637,
            "m_end": 0.8657000418070226,
            "reserve": 604.7165637515294,
            "sag_kg": 193.417619679882,
            "vehicle": 4284.725586438471,
            "s_m": 6.15,
            "r_o_m": 0.1655692772803688,
            "t_film_m": 0.00028233141337633867,
            "t_w_m": 0.0015764940543974584,
            "rt": 105.0237245224816,
            "A_m2": 0.0016322227222412859,
            "I_m4": 2.216020579405737e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 1038317838.7705252,
            "k": 0.2,
            "gamma": 0.5738497729022546,
            "SF_local_gamma1": 2.2558871777811187,
            "SF_least": 1.251315255038375,
            "eta": 0.0762351379029742,
            "Euler_stress_Pa": 1405847969.431958,
            "mass_closure_kg": 4889.44215019,
            "radius_cap_fraction": 0.6622771091214752,
            "NASA_L_over_midradius": 37.93696580773276,
            "SF_yield": 3.7560753117927743,
            "SF_euler": 1.353966884645482,
            "SF_local": 1.294540344662803,
            "SF_film": 1.4427135114359915,
            "SF_perry": 1.2993729363738866,
            "SF_global": 1.301354804129081,
            "SF_tension": 1.251315255038375,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.251315255038375,
            "k04_SF_global": 2.602709608258162,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 1038317838.7705252,
              "bending_Pa": 302782600.48988324,
              "maximum_compression_Pa": 1341100439.2604084,
              "opposite_signed_compression_Pa": 735535238.280642,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.251315255038375,
              "mean_compression_Pa": 1299262951.2320342,
              "bending_Pa": 1306454951.2320356,
              "maximum_compression_Pa": 2605717902.46407,
              "opposite_signed_compression_Pa": -7192000.0000014305,
              "maximum_tension_Pa": 7192000.0000014305
            }
          }
        },
        {
          "Ft_assumed_Pa": 15586000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 344.1444741266027,
            "m_joint": 199.27264697326052,
            "m_tube": 3640.501176295637,
            "m_end": 0.8657000418070226,
            "reserve": 604.7165637515294,
            "sag_kg": 193.417619679882,
            "vehicle": 4284.725586438471,
            "s_m": 6.15,
            "r_o_m": 0.1655692772803688,
            "t_film_m": 0.00028233141337633867,
            "t_w_m": 0.0015764940543974584,
            "rt": 105.0237245224816,
            "A_m2": 0.0016322227222412859,
            "I_m4": 2.216020579405737e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 1038317838.7705252,
            "k": 0.2,
            "gamma": 0.5738497729022546,
            "SF_local_gamma1": 2.2558871777811187,
            "SF_least": 1.2519699511228726,
            "eta": 0.0762351379029742,
            "Euler_stress_Pa": 1405847969.431958,
            "mass_closure_kg": 4889.44215019,
            "radius_cap_fraction": 0.6622771091214752,
            "NASA_L_over_midradius": 37.93696580773276,
            "SF_yield": 3.7560753117927743,
            "SF_euler": 1.353966884645482,
            "SF_local": 1.294540344662803,
            "SF_film": 1.4427135114359915,
            "SF_perry": 1.2993729363738866,
            "SF_global": 1.301354804129081,
            "SF_tension": 1.2519699511228726,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.2519699511228726,
            "k04_SF_global": 2.602709608258162,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 1038317838.7705252,
              "bending_Pa": 302782600.48988324,
              "maximum_compression_Pa": 1341100439.2604084,
              "opposite_signed_compression_Pa": 735535238.280642,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.2519699511228726,
              "mean_compression_Pa": 1299942733.8555412,
              "bending_Pa": 1315528733.855541,
              "maximum_compression_Pa": 2615471467.7110825,
              "opposite_signed_compression_Pa": -15585999.999999762,
              "maximum_tension_Pa": 15585999.999999762
            }
          }
        },
        {
          "Ft_assumed_Pa": 380000000.0,
          "result": {
            "nodes": 40.36445214851938,
            "members": 115.09335644555816,
            "n_coef": 17.753520777580995,
            "m_nodes": 0.8072890429703877,
            "m_film": 344.1444741266027,
            "m_joint": 199.27264697326052,
            "m_tube": 3640.501176295637,
            "m_end": 0.8657000418070226,
            "reserve": 604.7165637515294,
            "sag_kg": 193.417619679882,
            "vehicle": 4284.725586438471,
            "s_m": 6.15,
            "r_o_m": 0.1655692772803688,
            "t_film_m": 0.00028233141337633867,
            "t_w_m": 0.0015764940543974584,
            "rt": 105.0237245224816,
            "A_m2": 0.0016322227222412859,
            "I_m4": 2.216020579405737e-05,
            "length_m": 6.25129231047749,
            "N_N": 1694765.9693497152,
            "sigma_axial_Pa": 1038317838.7705252,
            "k": 0.2,
            "gamma": 0.5738497729022546,
            "SF_local_gamma1": 2.2558871777811187,
            "SF_least": 1.2737845631260436,
            "eta": 0.0762351379029742,
            "Euler_stress_Pa": 1405847969.431958,
            "mass_closure_kg": 4889.44215019,
            "radius_cap_fraction": 0.6622771091214752,
            "NASA_L_over_midradius": 37.93696580773276,
            "SF_yield": 3.7560753117927743,
            "SF_euler": 1.353966884645482,
            "SF_local": 1.294540344662803,
            "SF_film": 1.4427135114359915,
            "SF_perry": 1.2993729363738866,
            "SF_global": 1.301354804129081,
            "SF_tension": 1.2737845631260436,
            "governing": "tension",
            "k04_governing": "tension",
            "k04_SF_least": 1.2737845631260436,
            "k04_SF_global": 2.602709608258162,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 1038317838.7705252,
              "bending_Pa": 302782600.48988324,
              "maximum_compression_Pa": 1341100439.2604084,
              "opposite_signed_compression_Pa": 735535238.280642,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.2737845631260436,
              "mean_compression_Pa": 1322593234.6442912,
              "bending_Pa": 1702593234.6442926,
              "maximum_compression_Pa": 3025186469.2885838,
              "opposite_signed_compression_Pa": -380000000.00000143,
              "maximum_tension_Pa": 380000000.00000143
            }
          }
        }
      ],
      "reoptimized_tensile_screens": [
        {
          "Ft_assumed_Pa": 15586000.0,
          "result": {
            "nodes": 41.950451164473975,
            "members": 119.85135349342193,
            "n_coef": 17.397552232007467,
            "m_nodes": 0.8390090232894796,
            "m_film": 306.4892406455499,
            "m_joint": 199.45732017167055,
            "m_tube": 3681.8181537645714,
            "m_end": 0.8321029106384594,
            "reserve": 600.8384265849181,
            "sag_kg": 189.5394825132708,
            "vehicle": 4288.6037236050815,
            "s_m": 6.026688878634051,
            "r_o_m": 0.16483268110498572,
            "t_film_m": 0.00025143957553206553,
            "t_w_m": 0.0015704589689146153,
            "rt": 104.95828567804344,
            "A_m2": 0.0016187357220585415,
            "I_m4": 2.178185596486982e-05,
            "length_m": 6.121836792964786,
            "N_N": 1660784.913718274,
            "sigma_axial_Pa": 1025976563.7384334,
            "k": 0.2,
            "gamma": 0.5739445512590303,
            "SF_local_gamma1": 2.284446218521043,
            "SF_least": 1.3111454597644487,
            "eta": 0.07499048093210431,
            "Euler_stress_Pa": 1452911090.2765872,
            "mass_closure_kg": 4889.44215019,
            "radius_cap_fraction": 0.6593307244199429,
            "NASA_L_over_midradius": 37.31747572114505,
            "SF_yield": 3.8012564203116455,
            "SF_euler": 1.416125028219454,
            "SF_local": 1.3111454597644487,
            "SF_film": 1.3111454597695325,
            "SF_perry": 1.3571567005681893,
            "SF_global": 1.3111454597688381,
            "SF_tension": 1.311145460502161,
            "governing": "local",
            "k04_governing": "local",
            "k04_SF_least": 1.3111454597644487,
            "k04_SF_global": 2.6222909195376762,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 1025976563.7384334,
              "bending_Pa": 261831166.17049387,
              "maximum_compression_Pa": 1287807729.9089272,
              "opposite_signed_compression_Pa": 764145397.5679395,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.3111454597644487,
              "mean_compression_Pa": 1345204513.3703775,
              "bending_Pa": 1360790503.799066,
              "maximum_compression_Pa": 2705995017.1694436,
              "opposite_signed_compression_Pa": -15585990.428688526,
              "maximum_tension_Pa": 15585990.428688526
            },
            "search": {
              "method": "independent differential evolution plus bounded-accepted simplex",
              "seed": 835,
              "spacing_upper_m": 8.0,
              "outer_radius_upper_m": 0.25,
              "evaluations": 6482,
              "DE_success": true,
              "DE_message": "Optimization terminated successfully.",
              "certified_global_optimum": false
            }
          }
        },
        {
          "Ft_assumed_Pa": 380000000.0,
          "result": {
            "nodes": 41.22113604802986,
            "members": 117.66340814408959,
            "n_coef": 17.558560512876458,
            "m_nodes": 0.8244227209605972,
            "m_film": 309.6670187723478,
            "m_joint": 199.37379056050594,
            "m_tube": 3676.98436971681,
            "m_end": 0.8472208722543313,
            "reserve": 602.5925484193746,
            "sag_kg": 191.29360434772718,
            "vehicle": 4286.849601770625,
            "s_m": 6.0824637832149335,
            "r_o_m": 0.16528307767229655,
            "t_film_m": 0.0002540465811863397,
            "t_w_m": 0.0015781384513753377,
            "rt": 104.73293869004547,
            "A_m2": 0.0016310792156833264,
            "I_m4": 2.2067605873143465e-05,
            "length_m": 6.180357716229902,
            "N_N": 1676154.8991211045,
            "sigma_axial_Pa": 1027635496.1821362,
            "k": 0.2,
            "gamma": 0.5742713037988345,
            "SF_local_gamma1": 2.285665749591833,
            "SF_least": 1.3125922500664422,
            "eta": 0.07550258805056499,
            "Euler_stress_Pa": 1433298156.0086513,
            "mass_closure_kg": 4889.442150189999,
            "radius_cap_fraction": 0.6611323106891862,
            "NASA_L_over_midradius": 37.57193210010387,
            "SF_yield": 3.795119976381948,
            "SF_euler": 1.3947534523025236,
            "SF_local": 1.3125922500664422,
            "SF_film": 1.312592250079746,
            "SF_perry": 1.3374459793009164,
            "SF_global": 1.3125922500664948,
            "SF_tension": 1.312592250105854,
            "governing": "local",
            "k04_governing": "local",
            "k04_SF_least": 1.3125922500664422,
            "k04_SF_global": 2.6251845001329897,
            "on_ro_cap_0_25": false,
            "full_pressure": {
              "pressure_multiplier": 1.0,
              "mean_compression_Pa": 1027635496.1821362,
              "bending_Pa": 274140022.32416654,
              "maximum_compression_Pa": 1301775518.5063028,
              "opposite_signed_compression_Pa": 753495473.8579696,
              "maximum_tension_Pa": 0.0
            },
            "reported_limit": {
              "pressure_multiplier": 1.3125922500664422,
              "mean_compression_Pa": 1348866388.181855,
              "bending_Pa": 1728866387.341129,
              "maximum_compression_Pa": 3077732775.522984,
              "opposite_signed_compression_Pa": -379999999.1592741,
              "maximum_tension_Pa": 379999999.1592741
            },
            "search": {
              "method": "independent differential evolution plus bounded-accepted simplex",
              "seed": 835,
              "spacing_upper_m": 8.0,
              "outer_radius_upper_m": 0.25,
              "evaluations": 6155,
              "DE_success": true,
              "DE_message": "Optimization terminated successfully.",
              "certified_global_optimum": false
            }
          }
        }
      ],
      "hypothetical_uniform_volume_caps": [
        {
          "m": 8,
          "volume_m3": 1.1743552181598829,
          "reference_m3": 1.4814814814814816e-08,
          "tensile_cap_Pa": 7386921.002105608,
          "classification": "PROJECTION from025 hypotheses; actual stressed size and compression law unknown"
        },
        {
          "m": 10,
          "volume_m3": 1.1743552181598829,
          "reference_m3": 1.1900826446280993e-08,
          "tensile_cap_Pa": 15922846.49768159,
          "classification": "PROJECTION from025 hypotheses; actual stressed size and compression law unknown"
        }
      ]
    }
  },
  "next": "Score positive tensile bending and node stress separately, with explicit full-size evidence or clearly labeled sensitivity inputs.",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION"
}
```

### N459 — NFI-C022-LOCAL-INTERACTION

Source `rpt-ref-f6de390e1555b4ca8e78`; original file `unpublished-local-ref:a3c00555c78ad754; pointer `/rows/2`.

```json
{
  "id": "NFI-C022-LOCAL-INTERACTION",
  "kind": "OPEN structural qualification",
  "issue": "The separate minimum of shell, column and compression-only Perry factors does not establish their interaction.",
  "evidence": {
    "GAMMA/percent_crush_5": {
      "owner_least_SF": 1.3752490300405331,
      "local_stress_threshold_Pa": 1375090928.9226415,
      "amplified_extreme_compression_screen_multiplier": 1.0719323966315404,
      "classification": "PROJECTION diagnostic only; no validated shell/column/bending interaction law is supplied"
    },
    "GAMMA/percent_crush_019": {
      "owner_least_SF": 1.2986375988562082,
      "local_stress_threshold_Pa": 1346468388.8543727,
      "amplified_extreme_compression_screen_multiplier": 1.0038990459936852,
      "classification": "PROJECTION diagnostic only; no validated shell/column/bending interaction law is supplied"
    },
    "022c_cap/projection_5": {
      "owner_least_SF": 1.3733213857843127,
      "local_stress_threshold_Pa": 1372815334.9977148,
      "amplified_extreme_compression_screen_multiplier": 1.0693509460657717,
      "classification": "PROJECTION diagnostic only; no validated shell/column/bending interaction law is supplied"
    },
    "022c_cap/projection_019": {
      "owner_least_SF": 1.294540344662803,
      "local_stress_threshold_Pa": 1344144332.8715324,
      "amplified_extreme_compression_screen_multiplier": 1.0013829334691926,
      "classification": "PROJECTION diagnostic only; no validated shell/column/bending interaction law is supplied"
    }
  },
  "source": {
    "url": "https://ntrs.nasa.gov/api/citations/20205011530/downloads/20205011530%20Rev%202FINALa%201-2023.pdf",
    "locator": "printed pp.23-25, equations9-10 and L/r caution",
    "retrieved_on": "2026-10-20"
  },
  "next": "Evaluate coupled curved-member instability and measured imperfections. The long-strut application requires evidence; the diagnostic extreme-stress screen is not a validated replacement.",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION"
}
```

### N591 — NFI-022D-TENSION

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/2`.

```json
{
  "id": "NFI-022D-TENSION",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "NFI-C022-TENSILE-BENDING",
    "MAINLINE-025"
  ],
  "finding": "Amplified tensile bending is screened at assumed Ft=15.586 MPa. This fixed reference-volume ceiling is PROJECTION, not a full-stress-field weakest-link model or measured allowable. Eight overall equilateral witnesses bind it; no screened optimum has tensile stress at its target.",
  "next": "Calibrate full-size tensile surface/volume populations with the actual stress field and end-contact demands."
}
```

### N596 — NFI-022D-INTERACTION

Source `rpt-ref-6c81b0b188ad134a3ea2`; original file `unpublished-local-ref:e44d468b7f13771c; pointer `/rows/7`.

```json
{
  "id": "NFI-022D-INTERACTION",
  "status": "OPEN",
  "classification": "QUESTIONABLE; unvalidated transfers PROJECTION",
  "source_rows": [
    "NFI-C022-LOCAL-INTERACTION"
  ],
  "finding": "Separate local, Euler and Perry/tension minima leave shell-column-curvature interaction unresolved. The optional magnified-local diagnostic is not a validated law and is excluded from the primary least SF.",
  "next": "Resolve coupled instability with a justified theory or calibrated nonlinear model."
}
```

### N621 — NFI-026B-07

Source `rpt-ref-8befdd4c89803adc44a8`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/6`.

```json
{
  "id": "NFI-026B-07",
  "tag": "QUESTIONABLE",
  "status": "open",
  "owner": "sciences",
  "issue": "Beam-only instability omits earlier failure modes",
  "evidence": "No wall ovalization/local buckling, ceramic tensile fracture, bond failure, stress concentration or film failure. Unit-pressure stresses and prior026 material screens are retained.",
  "implication": "Elastic frame factors are not physical structural allowables."
}
```

### N647 — NFI-026B-07

Source `rpt-ref-4a20323946ecafd56a6b`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/6`.

```json
{
  "id": "NFI-026B-07",
  "tag": "QUESTIONABLE",
  "status": "open",
  "owner": "sciences",
  "issue": "Beam-only instability omits earlier failure modes",
  "evidence": "No wall ovalization/local buckling, ceramic tensile fracture, bond failure, stress concentration or film failure. Unit-pressure stresses and prior026 material screens are retained.",
  "implication": "Elastic frame factors are not physical structural allowables."
}
```

### C154 — NFI-041-02

Source `rpt-ref-c7dfc45babe1b96007db`; original file `unpublished-local-ref:cd543374666d8c21; pointer `/items/1`.

```json
{
  "id": "NFI-041-02",
  "status": "open",
  "topic": "Local shell buckling under bending",
  "evidence": [
    "RESULTS.json:best_closure_by_reserve",
    "ADDITIONAL-SCORES.json",
    "METHODS.md"
  ],
  "finding": "The matching-022d optimization retains its axial-stress local-wall formula. Substituting peak amplified compression into that formula lowers the selected frequency-5 witnesses from 1.143285/1.083205 to 1.033223/0.978132 at the 5%/019 reserves. This is a conservative sensitivity, not a calibrated interaction law.",
  "needed": "A verified local-shell model or tests for curved SiC tubes under combined axial force, end bending, contact and geometric imperfections. Reoptimize if the interaction changes the active local limit.",
  "prohibited_inference": "The 019 witness cannot be presented as robustly above unity across the displayed local-shell conventions."
}
```

### C202 — NFI-043-04

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/3`.

```json
{
  "id": "NFI-043-04",
  "status": "open",
  "topic": "Multiaxial and local tensile stresses",
  "finding": "Nominal beam normal stresses are compressive, but ideal beam shear produces small positive principal-stress estimates. Hoop stresses, pressure load path, membrane attachment, contact and residual stresses are not resolved.",
  "needed": "Validated three-dimensional joint/member stress fields and a suitable multiaxial fracture law, including tensile surface/volume flaw populations.",
  "effect": "Zero longitudinal tension cannot be reported as zero actual tensile or frame hazard. Uniform tensile levels and stressed fractions are sensitivity inputs.",
  "stops_other_work": false
}
```

## R092 — Discrete curved-member rolling mechanisms and restraint

**030b source history:** 026b reports1080/480/120 member-roll mechanisms at frequencies6/4/2. Its new nonlinear tangent zeros5.082444/2.218113 are not verified first-instability loads; the top-level fields remain null. Eightfold rise does not divide thrust by eight and introduces4.248GPa elastic bending.

**Original question:** Discrete curved-member rolling mechanisms and restraint

### N501 — NFI-026-03

Source `rpt-ref-7ce5b278fa083d87105b`; original file `unpublished-local-ref:b5af6e3d5ba37016; pointer `/rows/2`.

```json
{
  "id": "NFI-026-03",
  "tag": "PROJECTION",
  "status": "open",
  "owner": "sciences",
  "issue": "Freely rolling pinned curved members are mechanisms",
  "evidence": "1080 independent zero-strain roll coordinates; negative pressure-volume roll curvature for every member.",
  "implication": "Specify joint anti-roll stiffness and attached-film restraint before assigning a positive pinned buckling factor."
}
```

### N616 — NFI-026B-02

Source `rpt-ref-8befdd4c89803adc44a8`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/1`.

```json
{
  "id": "NFI-026B-02",
  "tag": "PROJECTION",
  "status": "open",
  "owner": "sciences",
  "issue": "Freely pinned curved members roll",
  "evidence": "Rigidity rank 3V-6; internal mechanisms1080/480/120 at frequencies 6/4/2, excluding six rigid motions.",
  "implication": "Specify joint and film anti-roll restraint before assigning positive pinned reserve."
}
```

### N642 — NFI-026B-02

Source `rpt-ref-4a20323946ecafd56a6b`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/1`.

```json
{
  "id": "NFI-026B-02",
  "tag": "PROJECTION",
  "status": "open",
  "owner": "sciences",
  "issue": "Freely pinned curved members roll",
  "evidence": "Rigidity rank 3V-6; internal mechanisms1080/480/120 at frequencies 6/4/2, excluding six rigid motions.",
  "implication": "Specify joint and film anti-roll restraint before assigning positive pinned reserve."
}
```

### C086 — NFI-C026B-JOINTS

Source `rpt-ref-b92330879d6ba35bd62c`; original file `unpublished-local-ref:21616ac9b36e6057; pointer `/rows/5`.

```json
{
  "id": "NFI-C026B-JOINTS",
  "issue": "Rigid-joint reserve and ball-pin mechanisms depend on unspecified joint/film restraint.",
  "evidence": "Endpoint rank and independent member rolls reproduce; no positive freely pinned factor is established.",
  "next_evidence": "Joint stiffness, anti-roll restraint and attached-film model, with fabricated load paths and mass.",
  "tag": "QUESTIONABLE",
  "status": "open",
  "blocks_card": false
}
```

## R093 — Ordered evidence route and grounding of the current leads

**Current 030c:** CHECK-038 preserves first T1 finished-sheet compression/specification, T2 weighed curved sealed scarf, T3 same-batch wrinkle. 042 F1 expands T2 to a full-blank forming-and-seam article after T1; it can supply T3 coupons. Costs remain projections, no purchases.

**030b source history:** 038 supplies nine physical test families. Its first purchase sequence is finished-sheet compression, weighed sealed scarf panel, then same-batch wrinkle coupons; retain original030 FE-first list as historical planning. Planning costs and providers are unverified projections; no contact or purchase was performed.

**Original question:** Ordered evidence route and grounding of the current leads

### N658 — NFI-038-MIN_SHELL

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/7`.

```json
{
  "id": "NFI-038-MIN_SHELL",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Smallest manufactured similarity shell not established",
  "evidence": "Planning floors 25 um/1 mm are assumptions; commercial microcore/formed foil combination unverified.",
  "resolution_needed": "Gate the surrogate on measured moduli, gauge and a fabrication trial; no Be-hull validation claim.",
  "tests": [
    "T7"
  ]
}
```

### N661 — NFI-038-VACUUM_LOAD

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/10`.

```json
{
  "id": "NFI-038-VACUUM_LOAD",
  "status": "OPEN",
  "tag": "QUESTIONABLE/PROJECTION",
  "issue": "Ambient evacuation gives little Be overload and censored survivals",
  "evidence": "101.325kPa maximum is only 1.06143 times the R10 design pressure.",
  "resolution_needed": "Use differential metrology and external-pressure facility where collapse/proof exceeds ambient.",
  "tests": [
    "T7",
    "T8"
  ]
}
```

### N669 — NFI-038-COST_AVAILABILITY

Source `rpt-ref-536c47263ffe5f46fd19`; original file `unpublished-local-ref:c45a445188ab781b; pointer `/items/18`.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

### C107 — NFI-CHECK038-TEST_TRANSFER

Source `rpt-ref-2beb70a569266cf0297d`; original file `unpublished-local-ref:0746af9cb88f6eb1; pointer `/items/5`.

```json
{
  "id": "NFI-CHECK038-TEST_TRANSFER",
  "status": "OPEN",
  "blocking": false,
  "issue": "Coupon, surrogate and axial-joint successes do not supply full installed-hull SF.",
  "evidence": "The owner already distinguishes biaxial transfer, yield-censored wrinkles, component size, contacts and unknown joint restraint.",
  "resolution_needed": "Retain those conditions in purchase acceptance tables and subsequent model updates; use effective capacities only for the tested mode and state.",
  "tests": [
    "T1",
    "T2",
    "T3",
    "T4",
    "T5",
    "T6",
    "T8"
  ],
  "classification": "inherited qualification gap"
}
```

### C108 — NFI-CHECK038-MINIATURE

Source `rpt-ref-2beb70a569266cf0297d`; original file `unpublished-local-ref:0746af9cb88f6eb1; pointer `/items/6`.

```json
{
  "id": "NFI-CHECK038-MINIATURE",
  "status": "OPEN",
  "blocking": false,
  "issue": "Minimum radii use hypothetical 25 µm/1 mm floors and a partly matched Al/core system.",
  "evidence": "0.361403286198 m and 0.430344116083 m reproduce. Custom core, foil compression, forming and defect-field transfer remain unverified.",
  "resolution_needed": "Demonstrate actual gauges/properties and the as-built dimensionless state before procurement. Keep the current dent ratio an imposed experiment parameter.",
  "tests": [
    "T7"
  ],
  "classification": "inherited manufacturing/model gap"
}
```

### C150 — N042-14

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/13`.

```json
{
  "id": "N042-14",
  "issue": "The first evacuation is the proof, and it is destructive",
  "detail": "Sea-level evacuation loads the hull to 1.061 of its 500 m design pressure (038). A buckle at proof ends the hull, and no subscale proof precedes it.",
  "to_close": "A subscale built shell evacuated first (T7).",
  "tag": "PROJECTION"
}
```

### C211 — NFI-043-13

Source `rpt-ref-8cb22d2e233e57207cf6`; original file `unpublished-local-ref:cdb76dd9a6f7e3f9; pointer `/items/12`.

```json
{
  "id": "NFI-043-13",
  "status": "open",
  "topic": "Proof fixture and acceptance specification",
  "finding": "The illustrative 1.25-times-target axial proof is 1.374281 MN, with pressure-equivalent multiplier 1.572816 exceeding the source's stability multiplier. Support, confinement and local loading can change which flaws are screened.",
  "needed": "Validated fixture, proof stress coverage and load sequence, instrumentation and inspection sensitivity, proof-damage assessment, handling limits, accept/reject criteria and subsequent life model.",
  "effect": "PROOF.md is a prospective qualification outline, not a ready test protocol. Proof rejection rate and residual reliability are unknown.",
  "stops_other_work": false
}
```

## R094 — Snapshot completeness and pending follow-on filings

**Current 030c:** Current coverage and pending jobs are recorded at INTAKE.sampled_at. Old pending statements inside source history are superseded by this register's PENDING.json.

**030b source history:** This is a measured-time snapshot. Any named running card/check lacking a filed report at final intake is PENDING for 030c, not silently complete.

**Original question:** Snapshot completeness and pending follow-on filings

### N366 — NFI-030-SNAPSHOT

Source `rpt-mainline030-opus-register-1020`; original file `unpublished-local-ref:ef1ee16a8d48401a; pointer `/rows/3`.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

### N622 — NFI-026B-08

Source `rpt-ref-8befdd4c89803adc44a8`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/7`.

```json
{
  "id": "NFI-026B-08",
  "tag": "QUESTIONABLE",
  "status": "disclosed_stop",
  "owner": "sciences",
  "issue": "One optional static refinement refused by simjob",
  "evidence": "frequency 6m24rise1 request:31 GiB charged+6 GiB requested exceeds36 GiB; exit75, nothing started. Other requests in the same already-submitted batch were admitted. All 16 admissions ended and released.",
  "implication": "No retry/fallback/subsequent scientific launch. Paired m12 force/rise comparison complete; m24 rise-8 refinement complete. New numerical work requires fresh authority."
}
```

### N648 — NFI-026B-08

Source `rpt-ref-4a20323946ecafd56a6b`; original file `unpublished-local-ref:2cf0b24908a9b40f; pointer `/rows/7`.

```json
{
  "id": "NFI-026B-08",
  "tag": "QUESTIONABLE",
  "status": "disclosed_stop",
  "owner": "sciences",
  "issue": "One optional static refinement refused by simjob",
  "evidence": "frequency 6m24rise1 request:31 GiB charged+6 GiB requested exceeds36 GiB; exit75, nothing started. Other requests in the same already-submitted batch were admitted. All 16 admissions ended and released.",
  "implication": "No retry/fallback/subsequent scientific launch. Paired m12 force/rise comparison complete; m24 rise-8 refinement complete. New numerical work requires fresh authority."
}
```

### B004 — NFI-030B-SNAPSHOT

Source `rpt-ref-39745602983887568501`; original file `unpublished-local-ref:534f72d6d7dd0ad8; pointer `retained original identity`.

```json
{
  "id": "NFI-030B-SNAPSHOT",
  "title": "Unfiled cards and checks remain pending for 030c.",
  "finding": "Coverage is through the recorded final queue intake. No result or check is inferred from a running seat, a brief, an elapsed time or an unfiled artifact.",
  "status": "OPEN",
  "blocks_progress": false
}
```

### C109 — NFI-CHECK038-CURRENT_HOLD

Source `rpt-ref-2beb70a569266cf0297d`; original file `unpublished-local-ref:0746af9cb88f6eb1; pointer `/items/7`.

```json
{
  "id": "NFI-CHECK038-CURRENT_HOLD",
  "status": "OPEN",
  "blocking": false,
  "issue": "The quoted 034 leakage and trapped-gas examples have older geometry inventories.",
  "evidence": "Current 028b seam length is 2841.518544 m versus 808.893916 m in 034 P2. Current 022d joints/plies also change the bill.",
  "resolution_needed": "Re-inventory final seams, adhesives, cells, bores and barriers, then evaluate initial/species gas, hot pressure and added mass separately; retain the 100 kg systems line.",
  "tests": [
    "T2",
    "T4",
    "T6",
    "T9"
  ],
  "classification": "inherited geometry-transfer gap"
}
```

### S006 — NFI-030C-SNAPSHOT

Source `rpt-1228-mainline030c-design-register-1020`; original file `unpublished-local-ref:3c01fd6db28be861; pointer `/rows/5`.

```json
{
  "id": "NFI-030C-SNAPSHOT",
  "title": "This register is a bounded filing snapshot.",
  "finding": "All discovered canonical mainline/check reports after the 030b snapshot are incorporated or explicitly dispositioned. Running work supplies no results. Later filings belong to 030d; no seat is polled, restored or contacted out of band.",
  "status": "OPEN",
  "blocks_progress": false,
  "tag": "QUESTIONABLE / PROJECTION"
}
```

## R095 — Unresolved FE benchmark, load-control endpoints and excluded spectra

**Current 030c:** 029: 79 native runs; benchmark unresolved, StVK/foam/defect differences explicit, load-control endpoints not proven collapse. CAX8R, initial shift/load-scale spectra and multicore eigen spectra excluded; physical capacity is null.

### C116 — NFI-029-LOAD-CONTROL

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/6`.

```json
{
  "id": "NFI-029-LOAD-CONTROL",
  "status": "open",
  "title": "Convergence endpoint is not proven collapse",
  "issue": "Native pressure control stops at minimum increment or can follow unstable branches. Last-converged pressure, local quadratic fold fits and eigenvalues must be reported separately. No Riks continuation or complete tangent stability proof is claimed.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C119 — NFI-029-CAX8R

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/9`.

```json
{
  "id": "NFI-029-CAX8R",
  "status": "excluded",
  "title": "Reduced-integration eigen discrepancy",
  "issue": "CAX8R eigenvalues are approximately twice CAX8 for both paper shell and homogeneous-sphere fixture, while small-load displacement is similar. Retain raw runs; use full integration. Root cause in this native build is not asserted.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C120 — NFI-029-EIGEN-SHIFT

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/10`.

```json
{
  "id": "NFI-029-EIGEN-SHIFT",
  "status": "resolved-by-subcritical-reference",
  "title": "ARPACK shift and load scale",
  "issue": "Initial1MPa lead load skips lower modes near a fixed shift of1. Correct eigenruns use0.001MPa. Sourcearpackbu.c fixes sigma=1 and its plausibility adjustment is commented out. Initial higher-mode results are excluded.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C124 — NFI-029-MULTICORE-EIGEN

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/14`.

```json
{
  "id": "NFI-029-MULTICORE-EIGEN",
  "status": "excluded-and-recomputed",
  "title": "Multicore eigenvalues fail identical-deck reproduction",
  "issue": "Identical CAX8 deck with four cores produces low near-shift modes absent with one core. The one-core replica exactly restores160.1382kPa. All multicore eigenvalue runs are excluded; accepted spectra and elastic-constant sensitivities use one core. Static one/four-core campaigns agree through independent mesh checks; no source-level cause is asserted. An identical-deck one-core021b W static check is retained separately; exact endpoint comparison is in RESULTS.json.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C125 — NFI-029-3D-RESOLUTION

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/15`.

```json
{
  "id": "NFI-029-3D-RESOLUTION",
  "status": "open",
  "title": "Full-resolution enlarged-shell 3D estimate exceeds the ceiling",
  "issue": "At1.04mm edge size, quadratic R_mid/tc40 model has582168 elements and8263917 free equations. Even10000bytes/equation implies76.96GiB, above32GiB maximum. Completed coarse3D runs are numerical crosschecks, not that full-resolution nonlinear result. This is a sizing projection, not a measured peak at that resolution; the full-resolution model was not launched.",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false,
  "completed_crosscheck": "The final48x128 graded3D endpoint is2.2539915MPa, -0.016435% from the matched axis48 graded result and +1.710861% from axis384. Linear3D48x128 is6.446068MPa, +1.151905% from axis384. The final native static run ended at the minimum increment after4327.637s with6868392kB peak RSS; full-resolution behavior remains unmeasured."
}
```

### C126 — NFI-029-FINITE-ELASTIC-LAW

Source `rpt-1228-mainline029-crimp-gamma-fe-1020`; original file `unpublished-local-ref:1a881bb5f01ae4e2; pointer `/16`.

```json
{
  "id": "NFI-029-FINITE-ELASTIC-LAW",
  "status": "open",
  "title": "Finite-strain elastic convention differs from Abaqus",
  "issue": "CalculiX2.21 manual6.8.1 identifies native *ELASTIC as linear PK2 stress versus Green-Lagrange strain (St.Venant-Kirchhoff). Abaqus linear elasticity instead relates logarithmic strain and Cauchy stress. Our decks specify no Ciarlet, hyperfoam or crushable-foam law. Large-compression behavior of this elastic approximation is not physical foam behavior. This adds a nonlinear constitutive mismatch; the separate roughly10% linear benchmark discrepancy remains unisolated.",
  "source": "https://www.dhondt.de/ccx_2.21.pdf",
  "tag": "QUESTIONABLE",
  "gates_other_cards": false
}
```

### C162 — /resolved_for_this_card_only/1

Source `rpt-ref-c7dfc45babe1b96007db`; original file `unpublished-local-ref:cd543374666d8c21; pointer `/resolved_for_this_card_only/1`.

```json
{
  "topic": "New nonlinear eigenvalue-family selection",
  "finding": "Smallest-algebraic eigenvalues at every recorded selected-frame equilibrium, independent shifted solves and finite-difference tangent checks establish the reported first sampled loss for the new m6/m12/m24 paths. This is not a retroactive claim about earlier cards."
}
```

## R096 — Frame/bay adequacy, cap knockdown and coupled modes

**Current 030c:** 039 frame-bay optimism is renamed P2-O6 to avoid P2-O5 bond-film collision. CHECK-039 improves attained C2b points but none floats at fixed lift. Clamping threshold and equal-area cap mapping remain unvalidated; the no-solution claim is finite-search scope.

### C022 — N039-01

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/0`.

```json
{
  "id": "N039-01",
  "issue": "Frame adequacy is assumed, not shown",
  "detail": "The bays are scored as clamped caps (O5) only when the stiffener rigidity EI_e/(a D_skin) is at least 10, a flat-plate order of magnitude. Mixed modes with wavelengths between a and 2a are not modelled.",
  "to_close": "Shell FE of frame plus sandwich bays (extend 026's beam model with shell bays), then a subscale frame-bay test.",
  "tag": "PROJECTION"
}
```

### C023 — N039-02

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/1`.

```json
{
  "id": "N039-02",
  "issue": "The frame-bay knockdown is a transfer, not a measurement",
  "detail": "SP-8032's clamped-cap lower bound (isotropic caps on rigid rings, Eq. 4/19) is applied to sandwich bays on a frame at lambda_p about 2.6, giving 0.57-0.60. No sandwich bay has been tested.",
  "to_close": "One bay test: a 2.04 m sandwich triangle (or a subscale bay at matched lambda_p and gamma_s) on a stiff frame ring, pressure-loaded, with the shape measured.",
  "tag": "PROJECTION"
}
```

### C024 — N039-03

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/2`.

```json
{
  "id": "N039-03",
  "issue": "The stiffened-dome record does not show a higher knockdown",
  "detail": "IDH CR-124075A p.4.1.012 gives 0.425 for heavily stiffened domes from one 1964 aluminium dome (C 0.26, plasticity suspected). CR-62257's plastic geodesic caps reached 0.57-0.64 of classical, while monocoque caps in the same program reached 0.78-0.82. SP-8032 p24 gives stiffened domes the isotropic cap curve (0.14 at a complete sphere).",
  "to_close": "Any stiffened-sphere test at a realistic scale; until then, 0.425 is a one-test handbook value.",
  "tag": "QUESTIONABLE"
}
```

### C025 — N039-04

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/3`.

```json
{
  "id": "N039-04",
  "issue": "The heavy threshold psi 28 is this seat's computation",
  "detail": "psi (composite over skin bending) of the IDH test dome is computed from CR-62257's design values (t 0.0375, d 0.166, b 0.10 in, side 1.65 in). As-built values were not extracted.",
  "to_close": "Read the as-built dimensions in CR-62257 Chapter V.",
  "tag": "QUESTIONABLE"
}
```

### C026 — N039-05

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/4`.

```json
{
  "id": "N039-05",
  "issue": "Stiffener one-sidedness",
  "detail": "SP-8032 warns that inside and outside stiffening can give seriously different dome results. The two-group model carries the offset in bending only, not the prebuckling-rotation coupling.",
  "to_close": "FE with eccentric stiffeners on both sides.",
  "tag": "QUESTIONABLE"
}
```

### C027 — N039-06

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/5`.

```json
{
  "id": "N039-06",
  "issue": "Transfer bending is a simply supported bound",
  "detail": "Bays carry the lattice's pressure share to the lines by bending, taken as the centre moment of a simply supported equilateral triangle, (1+nu) q a_t^2/54. It adds 45 MPa face stress at the Be-frame bay point. Continuous bays would see less.",
  "to_close": "Plate FE of a continuous bay over the frame.",
  "tag": "QUESTIONABLE"
}
```

### C028 — N039-07

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/6`.

```json
{
  "id": "N039-07",
  "issue": "Rib-skin separation is not driven in the membrane state, but peel is unmodelled",
  "detail": "The bond carries 0.16-0.21 MPa compression at the lattice lines. Peel in post-buckling, at rib ends and splices, and under thermal cycling is not modelled. No test exists of bonded Be ribs or tubes on a Be/aluminium-honeycomb sandwich.",
  "to_close": "A peel and post-buckling coupon of a rib or tube on the actual sandwich.",
  "tag": "QUESTIONABLE"
}
```

### C031 — N039-10

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/9`.

```json
{
  "id": "N039-10",
  "issue": "Rib material",
  "detail": "Tees are taken as SR-200 sheet (blade plus foot, bonded) at sheet values. A machined S-200F tee would have about 255 MPa compression (030 ledger), below the 354-377 MPa rib stress of the heavy rib designs.",
  "to_close": "A rib route decision and coupons.",
  "tag": "QUESTIONABLE"
}
```

### C032 — N039-11

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/10`.

```json
{
  "id": "N039-11",
  "issue": "The core at the lattice lines",
  "detail": "Crush and W-direction shear at the lines use a w_bond + 2h spread. Heavy rib designs fail core shear (0.65). Local core densification is not costed.",
  "to_close": "Local insert design and mass.",
  "tag": "QUESTIONABLE"
}
```

### C035 — N039-14

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/13`.

```json
{
  "id": "N039-14",
  "issue": "Smeared lattice idealisation",
  "detail": "Equal members in three directions (nu 1/3). The frequency-6 geodesic has length scatter (026's mean arc is 2.001 m) and 12 five-valent joints.",
  "to_close": "Discrete model (026 geometry).",
  "tag": "QUESTIONABLE"
}
```

### C036 — N039-15

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/14`.

```json
{
  "id": "N039-15",
  "issue": "026's frame knockdown does not transfer to a skin-dominated hull",
  "detail": "026's 0.70-0.79 of linear is computed for a frame with t_eq about 2.6 r_o = 320 mm, where 10 mm is 3% of t_eq. Here it enters only frame-dominated designs (psi >= 28), and none of them carries a skin within the lift: 026's members alone weigh 4,567 kg.",
  "to_close": "Measure a subscale frame if a frame-dominated hull is ever in reach.",
  "tag": "PROJECTION"
}
```

### C037 — N039-16

Source `rpt-mainline039-opus-stiffened-sandwich-1020`; original file `unpublished-local-ref:d2d754da784ace21; pointer `/rows/15`.

```json
{
  "id": "N039-16",
  "issue": "The core-shear correction in the bays is standard, not tested",
  "detail": "The thin cores of the heavy rib designs cut the plate load by about 60% (N/(1+kD/S)).",
  "to_close": "Bay test (N039-02).",
  "tag": "QUESTIONABLE"
}
```

### C128 — C039-02

Source `rpt-ref-20ab4b33b504a00ad3b6`; original file `unpublished-local-ref:75b66f0986a98c9b; pointer `/rows/1`.

```json
{
  "id": "C039-02",
  "topic": "HEAVY-DOME-GATE",
  "status": "QUESTIONABLE",
  "objection": "The handbook's .425 recommendation is represented as applying only for psi about 28 or more.",
  "evidence": "SOURCE-CHECK.md: IDH p4.1.012 supplies no numeric psi gate. CR-62257 p181 describes only a central accurately machined region and stronger surrounding support.",
  "proposed_fix": "Attribute psi>=28 to the model author, disclose calibration nu=.33/.35 and design versus as-built geometry, and seek a demonstrated transfer before calling it handbook credit.",
  "disposition": "Record for owner revision; check completed"
}
```

### C129 — C039-03

Source `rpt-ref-20ab4b33b504a00ad3b6`; original file `unpublished-local-ref:75b66f0986a98c9b; pointer `/rows/2`.

```json
{
  "id": "C039-03",
  "topic": "BAY-CLAMPING",
  "status": "PROJECTION",
  "objection": "gamma_s>=10 and equal-area circular-cap mapping are used to grant clamped-cap behavior to triangular sandwich bays.",
  "evidence": "SUPPLEMENTARY.json: composite gamma_s 10.400178 versus isolated-member EI/(a Dskin) 3.196840. Circumscribed-circle substitution gives panel SF .390794 versus .710384.",
  "proposed_fix": "Validate translational and rotational edge restraint, joint compliance, triangular geometry and shear-flexible skin together. Compare multiple bay/frame stiffness ratios including below and above 10; replace the abrupt gate with validated behavior.",
  "disposition": "Record for owner revision; check completed"
}
```

### C130 — C039-04

Source `rpt-ref-20ab4b33b504a00ad3b6`; original file `unpublished-local-ref:75b66f0986a98c9b; pointer `/rows/3`.

```json
{
  "id": "C039-04",
  "topic": "COUPLED-MODES-AND-LAYOUT",
  "status": "PROJECTION",
  "objection": "The global wavelength cutoff leaves intermediate frame/bay modes unverified; the continuum length is not the actual 026 frame length.",
  "evidence": "SUPPLEMENTARY.json: 3.427772 m unrestricted minimum versus 4.08 m cutoff; global SF 1.055069 versus 1.118206. 026 arc length 2161.451 m versus continuum 2133.882 m; unchanged Be tubes add 8.093 kg.",
  "proposed_fix": "Use a discrete, coupled frame/bay model covering the intervening wavelengths, eccentric constitutive coupling, real joint locations and arc lengths. Retain the continuum model as a screen.",
  "disposition": "Record for owner revision; check completed"
}
```

### C131 — C039-05

Source `rpt-ref-20ab4b33b504a00ad3b6`; original file `unpublished-local-ref:75b66f0986a98c9b; pointer `/rows/4`.

```json
{
  "id": "C039-05",
  "topic": "SEAM-OPERATING-POINT",
  "status": "REVISE",
  "objection": "The narrative says Q, scarf and tubes must move after adding the O5 mass deficit.",
  "evidence": "EXTENDED-ARITHMETIC.json: at the owner's +1329.818726 kg point, wrinkle/scarf/tube-local SF are 1.059449/1.109144/1.055118 using today's assumptions.",
  "proposed_fix": "Separate fixed-mass failures from mass-added feasibility. Keep the seam-dependent finite-search result qualified by its model and search domain; no impossibility theorem was proved.",
  "disposition": "Record for owner revision; check completed"
}
```

### C132 — C039-06

Source `rpt-ref-20ab4b33b504a00ad3b6`; original file `unpublished-local-ref:75b66f0986a98c9b; pointer `/rows/5`.

```json
{
  "id": "C039-06",
  "topic": "SOURCE-RATIOS",
  "status": "REVISE",
  "objection": "The source's printed plain-Ti .33 ratio and literal .14 at a sphere are repeated as checked values.",
  "evidence": "SOURCE-CHECK.md: 317/917=.345692475; SP-8032's .14+3.2/lambda^2 is greater than .14 for finite lambda. The filed C2b cap factor is .601013192, not the rounded-lambda .603.",
  "proposed_fix": "Record numerator, denominator, exact calculation and printed source value separately. Describe .14 as the large-lambda limit and use the full-precision bay factor.",
  "disposition": "Record for owner revision; check completed"
}
```

### C136 — C039-10

Source `rpt-ref-20ab4b33b504a00ad3b6`; original file `unpublished-local-ref:75b66f0986a98c9b; pointer `/rows/9`.

```json
{
  "id": "C039-10",
  "topic": "ALLOWABLES-AND-ASSEMBLY",
  "status": "QUESTIONABLE",
  "objection": "Unity in the scored factors does not close material, bond, peel, residual-stress or thin-wall validation.",
  "evidence": "The reconstruction retains 345 MPa tensile-as-compression, historical 379.2 MPa endpoint, typical core values, 10 MPa scarf, r/t=300 tube local rule and ideal composite action. A pin-ended Euler screen is 8.675 at the filed Be O5 point, but is not a full frame test.",
  "proposed_fix": "Keep an explicit unscored-mode/load-case ledger and ground formed-gauge compression, core at lines, scarf/bond/peel and imperfect thin tubes at representative boundaries. Do not convert the conditional mass-added point into a hull qualification.",
  "disposition": "Record for owner revision; check completed"
}
```

## R097 — Full-blank forming, in-place seams, closure tooling and inspection

**Current 030c:** 042 builds a chain of smaller/other-material precedents. Full-blank Be forming, kilometre-scale room-temperature scarfs, assembly closure and Be-specific seam/bond inspection remain projections. Carry F1 through the existing grounding sequence.

### C143 — N042-07

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/6`.

```json
{
  "id": "N042-07",
  "issue": "Seams must cure in place at room temperature",
  "detail": "A strip 100 K hotter than the cold shell carries about 354 MPa (this card), above 345 MPa, so heat-blanket cure is excluded on the shell. No room-temperature 30:1 scarf data in Be exist. EA 9394 and EA 9309.3NA give 29-33 MPa lap shear on aluminium (sub-worker rows).",
  "to_close": "Room-temperature scarf witnesses in SR-200 (038 T2 extended).",
  "tag": "QUESTIONABLE"
}
```

### C144 — N042-08

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/7`.

```json
{
  "id": "N042-08",
  "issue": "No inspection method for scarf seams",
  "detail": "No source inspects a 30:1 bonded scarf. E2580 UT assumes parallel surfaces, and shearography needs two shear directions on strip debonds.",
  "to_close": "Develop and validate a seam NDE on witness strips.",
  "tag": "QUESTIONABLE"
}
```

### C145 — N042-09

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/8`.

```json
{
  "id": "N042-09",
  "issue": "Bond NDE for Be on Al honeycomb is unproven",
  "detail": "Tap-test a90/95 is 28-43 mm on 0.5 mm Al skins, about the 29-55 mm disbond that buckles the inner face at 300 MPa (this card). Flash thermography likely cannot see the far bond under conductive Be (inference). Weak and kissing bonds escape commercial NDE.",
  "to_close": "PoD study on Be-faced panels with seeded disbonds.",
  "tag": "QUESTIONABLE"
}
```

### C146 — N042-10

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/9`.

```json
{
  "id": "N042-10",
  "issue": "Holding shape through closure is a projection",
  "detail": "There is no precedent for a 20 m thin-metal sandwich sphere. Large spheres held +/-6 mm (SNO 12 m) to under 2 cm (Moss R 18.3 m), which is global and cm-class. The S-II inflation technique smoothed welded skins to fit the core; using an inflated inner skin as the mandrel is this card's proposal.",
  "to_close": "Subscale assembly trial of either method.",
  "tag": "PROJECTION"
}
```

### C149 — N042-13

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/12`.

```json
{
  "id": "N042-13",
  "issue": "Jig support spacing is this card's estimate",
  "detail": "Self-weight is 34.2 Pa. A sandwich span sags 0.11 mm at 2 m and 4.2 mm at 5 m (simply supported strip), so supports belong 2 m apart or closer.",
  "to_close": "Jig design with measured sag.",
  "tag": "PROJECTION"
}
```

### C241 — NFI-044-INSPECTION-REPAIR

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/17`.

```json
{
  "id": "NFI-044-INSPECTION-REPAIR",
  "finding": "No defect detection threshold or crack/debond growth law supports an inspection interval. Plate replacement does not reset core, scarf or face damage.",
  "evidence_needed": "Qualified NDE probability of detection, initial-defect population, growth-to-critical size and tested repair procedures with a complete mass inventory."
}
```

## R098 — Stress-free temperature, cellular force balance and residual-stress stability

**Current 030c:** CHECK-037b reproduces principal residual/free-edge/scarf values;9 checker NFI remain. HexBond679 omitted30g/m2 support: corrected rejected-option mass519.653569kg, +75.398224kg. The selected200F/30.3414 fix remains conditional on product/cure/tooling and residual-state transfers.

### C089 — NFI-037b-SCREEN-PREMISE

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/0`.

```json
{
  "id": "NFI-037b-SCREEN-PREMISE",
  "tag": "QUESTIONABLE",
  "claim": "037's shear-lag screen holds each face at the core's expansion (0.227 after the 250 F cure). That needs the core to carry 47 times the in-plane force at which its walls yield. CR-1457, Hexcel AGU 075b and NASA TM-4585 treat the core's in-plane stiffness and thermal force as negligible; on that premise the continuous core carries no mismatch shear and a free core edge reads 1.17 / 0.83.",
  "needed_to_ground": "A curved Be/CR-III panel cured with AF 163-2U, cycled over 271-302 K, strain-gauged at a core splice, at a face scarf and in the field, then sectioned."
}
```

### C090 — NFI-037b-EDGE-MODEL

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/1`.

```json
{
  "id": "NFI-037b-EDGE-MODEL",
  "tag": "QUESTIONABLE",
  "claim": "The free-edge shear uses this seat's homogenised model: K_biax from wall stretching (uniform cell 0.5 E rho*/rho_s; doubled ribbon walls 0.45), a linear shear profile over half the core depth, and a 16 mm transfer length, about 1.7 cells. Homogenisation is marginal there and cell-scale peaks are not modelled. The W direction governs over L on both strengths.",
  "needed_to_ground": "A cell-resolved finite-element model of a free core edge, or the panel test above."
}
```

### C091 — NFI-037b-BALANCED-COMPRESSION

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/2`.

```json
{
  "id": "NFI-037b-BALANCED-COMPRESSION",
  "tag": "QUESTIONABLE",
  "claim": "The cure leaves the faces in compression balanced by core tension. This card takes it as not driving global buckling or crimping, because the wall's net membrane force is unchanged (this seat's argument). It adds it in full to yield, wrinkling, dimpling and the scarf; for wrinkling that is conservative, since the core's tension near the face resists the wrinkle.",
  "needed_to_ground": "A sandwich-shell buckling analysis with the layer-wise residual state."
}
```

### C096 — NFI-037b-STRESS-FREE-T

Source `rpt-ref-d6eac96dde8db1968e86`; original file `unpublished-local-ref:dfb86ca93b235443; pointer `/items/7`.

```json
{
  "id": "NFI-037b-STRESS-FREE-T",
  "tag": "QUESTIONABLE",
  "claim": "The cure-or-Tg rule (108-121 C for AF 163-2U) is sourced qualitatively; no measured stress-free temperature or relaxed fraction for AF 163 was found.",
  "needed_to_ground": "A bimaterial-strip or panel-curvature measurement with the actual cure cycle."
}
```

### C142 — N042-06

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/5`.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

### C152 — N042-16

Source `rpt-mainline042-opus-build-route-1020`; original file `unpublished-local-ref:c163eff390840ce4; pointer `/rows/15`.

```json
{
  "id": "N042-16",
  "issue": "The route rests on 037b",
  "detail": "The route adopts 037b's 200 F panel cure and 30.34:1 scarf. If CHECK-037b moves the stress-free temperature or the scarf rule, step 4 and the seam overlap change.",
  "to_close": "Re-read step 4 against CHECK-037b when it files.",
  "tag": "QUESTIONABLE"
}
```

### C164 — 040-02-cure_reference

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/findings/1`.

```json
{
  "id": "040-02-cure_reference",
  "tag": "PROJECTION",
  "open_issue": "Filed 037b's 200 F stress-free state, compliant-core/free-edge model and balanced-force argument are adopted conditionally.",
  "grounding": "Measure actual stress-free state and layer-wise residual strains; validate the free-edge and global/crimp assumptions on a curved matched panel."
}
```

### C186 — NFI-037b-SCREEN-PREMISE

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/0`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-SCREEN-PREMISE",
  "tag": "QUESTIONABLE",
  "claim": "037's shear-lag screen holds each face at the core's expansion (0.227 after the 250 F cure). That needs the core to carry 47 times the in-plane force at which its walls yield. CR-1457, Hexcel AGU 075b and NASA TM-4585 treat the core's in-plane stiffness and thermal force as negligible; on that premise the continuous core carries no mismatch shear and a free core edge reads 1.17 / 0.83.",
  "needed_to_ground": "A curved Be/CR-III panel cured with AF 163-2U, cycled over 271-302 K, strain-gauged at a core splice, at a face scarf and in the field, then sectioned."
}
```

### C187 — NFI-037b-EDGE-MODEL

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/1`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-EDGE-MODEL",
  "tag": "QUESTIONABLE",
  "claim": "The free-edge shear uses this seat's homogenised model: K_biax from wall stretching (uniform cell 0.5 E rho*/rho_s; doubled ribbon walls 0.45), a linear shear profile over half the core depth, and a 16 mm transfer length, about 1.7 cells. Homogenisation is marginal there and cell-scale peaks are not modelled. The W direction governs over L on both strengths.",
  "needed_to_ground": "A cell-resolved finite-element model of a free core edge, or the panel test above."
}
```

### C188 — NFI-037b-BALANCED-COMPRESSION

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/2`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-BALANCED-COMPRESSION",
  "tag": "QUESTIONABLE",
  "claim": "The cure leaves the faces in compression balanced by core tension. This card takes it as not driving global buckling or crimping, because the wall's net membrane force is unchanged (this seat's argument). It adds it in full to yield, wrinkling, dimpling and the scarf; for wrinkling that is conservative, since the core's tension near the face resists the wrinkle.",
  "needed_to_ground": "A sandwich-shell buckling analysis with the layer-wise residual state."
}
```

### C193 — NFI-037b-STRESS-FREE-T

Source `rpt-ref-b10363665c6202d8ef75`; original file `unpublished-local-ref:75bf4d644c11a92c; pointer `/inherited_037b/7`.

```json
{
  "source_report": "rpt-ref-d6eac96dde8db1968e86",
  "source_snapshot": "inputs/037b/NFI.json",
  "id": "NFI-037b-STRESS-FREE-T",
  "tag": "QUESTIONABLE",
  "claim": "The cure-or-Tg rule (108-121 C for AF 163-2U) is sourced qualitatively; no measured stress-free temperature or relaxed fraction for AF 163 was found.",
  "needed_to_ground": "A bimaterial-strip or panel-curvature measurement with the actual cure cycle."
}
```

### C216 — NFI-CHECK037b-200F-TRANSFER

Source `rpt-ref-4bf25e71ae0c2ca315e2`; original file `unpublished-local-ref:0360eb0aa78daa3e; pointer `/items/1`.

```json
{
  "id": "NFI-CHECK037b-200F-TRANSFER",
  "tag": "QUESTIONABLE",
  "status": "OPEN",
  "finding": "The detailed 200 F cure data use AF 163-2K at 0.060 lb/ft2 on metal, not the 2U 0.015 lb/ft2 Be/honeycomb joint. The family's six-hour guidance is not evidence that all two-to-six-hour cycles qualify the target assembly.",
  "exact": {
    "test_cycle_pressure_psi": 50,
    "core_stabilized_typical_compression_psi": 60,
    "core_stabilized_minimum_average_compression_psi": 35,
    "unbypassed_cure_pressure_SF_typical": 1.2,
    "unbypassed_cure_pressure_SF_minimum_average": 0.7
  },
  "disposition": "Keep the +0.12015 kg route as a process candidate; establish cure, pressure/tooling path, actual bond performance and stress-free temperature on target materials.",
  "evidence": "3M datasheet pp.15,19; Hexcel CR-III Table II; EVIDENCE.md",
  "blocking": false
}
```

### C217 — NFI-CHECK037b-FIELD-EDGE-RESIDUAL

Source `rpt-ref-4bf25e71ae0c2ca315e2`; original file `unpublished-local-ref:0360eb0aa78daa3e; pointer `/items/2`.

```json
{
  "id": "NFI-CHECK037b-FIELD-EDGE-RESIDUAL",
  "tag": "QUESTIONABLE",
  "status": "OPEN",
  "finding": "Zero mean mismatch shear is a homogeneous continuous-field idealization. The 16.092 mm edge length spans only 1.68948 cells; local peaks and the effect of balanced residuals on global/crimp modes are unresolved.",
  "exact": {
    "transfer_length_mm": 16.09228418994669,
    "transfer_length_cells": 1.6894786551125132,
    "028b_finite_face_residual_MPa": 4.36267358508647
  },
  "disposition": "Retain the calculated factors conditionally. A layer-wise/cell-resolved model and representative cured curved panel are the grounding steps; no debond survival is established by a zero mean shear argument.",
  "carries_owner_rows": [
    "NFI-037b-SCREEN-PREMISE",
    "NFI-037b-EDGE-MODEL",
    "NFI-037b-BALANCED-COMPRESSION",
    "NFI-037b-SPLICE",
    "NFI-037b-WAVINESS",
    "NFI-037b-HARDPOINTS"
  ],
  "blocking": false
}
```

### C231 — NFI-044-PRESSURE-CORE-EDGE

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/7`.

```json
{
  "id": "NFI-044-PRESSURE-CORE-EDGE",
  "finding": "The new coupled membrane/edge model balances pressure and thermal force but is homogenized over a short edge region. Pressure contraction may offset thermal residual extension; this is not validated relief.",
  "evidence_needed": "Cell-resolved and curved-panel validation of free edges, splices and hardpoints during thermal cycling, pressure hold and full vent/evacuation."
}
```

### C234 — NFI-044-CURE-SEQUENCE

Source `rpt-ref-29830021a6e140ff7411`; original file `unpublished-local-ref:b641867bdfe4e25e; pointer `/items/10`.

```json
{
  "id": "NFI-044-CURE-SEQUENCE",
  "finding": "HexBond312's cited cure is 120C. A later whole-panel scarf cure could invalidate an assumed 200F face/core stress-free state.",
  "evidence_needed": "An executable joining sequence and measured stress-free temperature/residual strain after every thermal operation."
}
```

### S003 — NFI-030C-THERMAL-DEPENDENCY

Source `rpt-1228-mainline030c-design-register-1020`; original file `unpublished-local-ref:3c01fd6db28be861; pointer `/rows/2`.

```json
{
  "id": "NFI-030C-THERMAL-DEPENDENCY",
  "title": "037b uses 037 temperatures whose recovery remains open.",
  "finding": "The 200 F/30.3414:1 fix supplies the selected P2 construction model used by 040's common account. CHECK-037's 84 missing thermal/projection inputs remain open; a mechanical reinterpretation does not supply them. Balanced residual compression is not independently established as harmless to global stability.",
  "status": "OPEN",
  "blocks_progress": false,
  "tag": "QUESTIONABLE / PROJECTION"
}
```
