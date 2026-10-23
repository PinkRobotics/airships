# CHECK-006 — MAINLINE-006 float margin — PASS

Unit vacuum-check006-1019. Order ord-admiral-rr2-check006-007-007b-after-011-1019. Owner ref-2543c559b19ffce7dfdd (grok); checker ref-3dada7412231c2ce03cc (glm) — different provider. Own script .ship/work/scripts/check006_float_margin.py; owner files read read-only; owner code never imported.

## What was re-derived

Every number in the owner's RESULTS.json (452 fields, tolerance 1e-9 relative / 1e-9 absolute) from the COMMON.md pins alone: R=10 m, p_ext=95460.83791390515 Pa, L=4889.442150186961 kg, Al 6061-T6 (E=68.9 GPa, ν=0.33, σ=276 MPa, ρ=2700, QUESTIONABLE per NFI-YIELD), kd=0.2, core ρ=16 (P2-E), film σ_f=1.5 GPa / t_f=80 µm / ρ_f=970.

- P1: t = ((1−m)L−200)/(1.1·4πR²ρ); p_b = 0.2·2(t/R)²E/√(3(1−ν²)); p_y = 2σt/R. Baseline t pinned 0.0007 → margin 0.424771095693.
- P2-A: core held 0.1 m (2010.619298 kg); sandwich = ((1−m)L−100)/1.05; p_b = 0.2·4t_f(d+t_f)E/(R²√(1−ν²)), p_y = 4σt_f/R. Baseline t_f pinned 0.0002 → margin 0.256320745969.
- P2-E: equal face/core split ((1−m)L−100)/2.1 → t_f 0.000336094970395, core 0.113432052508 at m=0; baseline at the P2-A baseline total (3636.176691 kg) → t_f 0.000248148148148, core 0.08375 — the 003-sealed row.
- P3: s=1, r_o=0.02 fixed; V=8πR²/√3+2=1453.039491, M=3V−6=4353.118474, nodes 29.060790 kg, film 97.515036 kg (4πR²t_fρ_f), systems 50; A=π(2r_o·t_w−t_w²), I=π/4(r_o⁴−r_i⁴); Euler 2π²EI/(Rs³), yield 2σA/(Rs), film 2σ_f t_f/s (SF 2.514119981 constant). Baseline t_w pinned 0.001 → margin 0.669363166472.
- Mass splits, payloads, all six margin points per family, all five SF-per-100-kg segments, knee selection (P1/P2-A/P2-E 0→5%; P3 30%→baseline), and the 0→30% secants (0.000100296692, 0.00863161923, 0.00827111936, 0.00177112902).

## Result

**0 mismatches.** The stated formulas are the ones used; sources and QUESTIONABLE tags are in INPUTS.json with sha256+bytes pins, and all four pins hash-match the files as they stand (CARD-006 brief 52b5ed16…, COMMON 8f359d6c…, results_002 d728af6c…, results_003 df5d2682…). Every row tagged QUESTIONABLE; status ESTIMATE_PENDING_UNA; certification false.

## Notes (no objection, no NFI opened)

1. Label-"0" rows print solver residues (float_margin 1.86e-16, payload 9.1e-13 kg); mass is conserved — cosmetic.
2. M = 4353.118474 is a non-integer continuum edge count inherited from the sealed 002 V(s); recorded in the line's NFI set (cf. NFI-011-NODES on my 011 card), inherited, not an 006 defect.
3. P2-A's knee (0→5%, 0.00864635) sits 0.07% above the next segment (0.00864046) — a monotone family; the owner's NFI-KNEE already names this tabulated-interval caveat.
