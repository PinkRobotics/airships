# MAINLINE-011 P3 frame optimisation, frame plus film — ESTIMATE_PENDING_CHECKER

Unit vacuum-mainline011-p3-frame-1019, order ord-admiral-rr2-mainline011-rotated-glm-1019, rotated from ref-3f8a144b95b4cdc80c8e (muse wall). Own script (.ship/work/scripts/mainline011_p3_frame.py), own arithmetic from the COMMON.md pins and the sealed MAINLINE-002 geometry. Nothing here is a certification; every material value is QUESTIONABLE unless named PROJECTION.

Case: evacuated sphere R = 10 m, p_ext = 95460.8379139 Pa at 500 m ISA, lift mass L = 4889.44215019 kg held as the ceiling at margin 0: film 97.515 kg + nodes 0.02·V(s) kg + systems 50 kg + tubes = L exactly. V(s) = 8πR²/(√3 s²) + 2 (reproduces the pinned 29.061 kg at s = 1 within 1 g), members M = 3V − 6 of length s. Sections are EXACT annuli (answers NFI-005-THINWALL). Limits as pressures on p_ext: member Euler 2π²EI/(Rs³), member yield 2σA/(Rs), tube local buckling 2σ_loc A/(Rs) with σ_loc = 0.6 E t_w/r_o (NASA SP-8007 classical E·t/(r√(3(1−ν²))) ≈ 0.61 at ν = 0.33; γ = 1 assumed, QUESTIONABLE), film 2σ_f t_f/s. Scan: s 0.4–6.4 m at 0.02, r_o 4000 steps from solid to min(0.25 m, s/3); optimum reported inside a stated validity band s ≤ 3.0 m (V ≥ 161 nodes, the equal-triangle continuum still a defensible reading).

## 6061-T6, best point and two next-best

Best: SF 0.2331 (yield) at s = 3.0 m, r_o = 86.6 mm, t_w = 2.25 mm (t_w/r_o 0.026), V = 163 nodes, 484 members, tube mass 4738.7 kg. Every limit: Euler 0.2333 (tied — a fully-stressed corner), yield 0.2331, local 0.908, film 0.838. Next-best: s = 2.48 m, r_o = 71.8 mm, SF 0.2331 (yield; Euler 0.233, local 1.09, film 1.01); s = 1.96 m, r_o = 57.0 mm, SF 0.2329 (yield; Euler 0.233, local 1.38, film 1.28). Pinned-spacing s = 1.0 with r_o free gives 0.2319 (yield; Euler 0.232, local 2.62, film 2.51). The unconstrained scan rides to s = 6.4 m at 0.2333 — suppressed: V = 37 nodes is not a continuum (NFI-011-BAND); the whole band spans 0.2319–0.2333, a plateau.

Reading: aluminum P3 sits on a yield wall flat across the design space — geometry is free, σ/ρ is not. The pinned r_o = 0.02 frame (005's P3-A row, reproduced by cross-check) is Euler-bound at 0.096; freeing r_o doubles the least SF to the 0.233 wall and no further.

## Equal-mass tube swap (film, nodes, systems, tube mass unchanged; E/ρ and σ/ρ per MAINLINE-008 rows)

CFRP QI T700/epoxy: best 0.7651 (yield) at s = 3.0, r_o = 133.8 mm, t_w 2.53 mm (Euler 0.766, local 0.901, film 0.838); next-best 0.7649 (s 2.48) and 0.7644 (s 1.96). The best CFRP for P3 — the rank flips against 008's P2-E, where M55J led on E/ρ: P3 is σ/ρ-bound and T700's QI compression carries it. CFRP QI M55J/epoxy: 0.4867 (yield; s 3.0, r_o 71.1 mm; Euler 0.487, local 7.31, film 0.838). CFRP QI K13D2U/epoxy: 0.2867 (yield; s 3.0, r_o 47.0 mm; local 23.8 — compression-weak pitch fibre buys nothing here). SiC alpha (Hexoloy SA type, 008 rank 1): 2.8485 (yield) at s = 0.88 m, r_o = 39.3 mm, t_w 1.26 mm (Euler 2.85, local 5.77, film 2.857 — the film is now the second limit and binds from s = 1.0: 2.514). CNT-yarn QI [PROJECTION]: 1.9489 (yield) at s = 1.28 (film 1.96 beside it). In 005's fixed-r_o = 0.02 frame every swap row is Euler-bound (T700 0.113, M55J 0.272, SiC 0.510) — the swap pays only with the radius freed.

## Comparison with P2-E and MAINLINE-004's knockdown

Best aluminum P3 0.2331 equals P2-E's 0.2339 at kd 0.2 (−0.3%) and beats P2-E at 004's SP-8032 curve kd 0.1407, where P2-E falls to 0.1646 — P3 is 1.42× P2-E there. The P3 limits are member formulas with no spherical knockdown, so 004's curve does not rescale them (and must not be pasted onto them); the unmodelled global frame mode is NFI-011-GLOBAL.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]