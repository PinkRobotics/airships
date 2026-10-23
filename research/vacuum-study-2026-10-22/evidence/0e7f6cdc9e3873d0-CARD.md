# MAINLINE-030e — morning design register

**QUESTIONABLE / PROJECTION. Record version 7; snapshot 2026-10-20T17:36:07-07:00. Qualified installed-hull SF, life, failure probability and availability remain unknown.**

## Piece C, version 7

QUESTIONABLE / PROJECTION. Piece C is appended to version 6. No qualified hull safety factor is released.

With today's admissible gamma 0.20 and Q 0.33 taken as equation 2.2-14, every recomputed concept and TRL 7 payload is still negative. The favorable ramp and Q 0.82 are not admissible. T7 and T3 remain the tests that could show better. This restatement is UNREVIEWED.

BETA, 0.682327803828082, is the real root of b^3+b=1. model61.py and model63.py set it at line 33 and multiply it onto Q in the face-wrinkling margin. Equation 2.2-14's 0.33 stands. The product BETA times 0.33 stands only as the model line. Both values are kept.

The 064 review reproduced all eight cells and named no fix. Sciences admitted that review with limits: shared-model reproduction, so the independent-derivation requirement is unmet; NFI065-BETA-SCALE is not independently cleared; 2014-T6 on glass-fabric is the flight bulkhead and the SDL 468 specimen materials remain unverified. The one-round result stands with those limits.

**Preserved:** version 6, 119 rows and 2,357 stable claim records, at the other seat. **Current:** 120 rows, 2,272 attributed NFI findings and 2,363 stable claim records.

[Claim record](5234234ce0219906-CLAIM-RECORD.json) · delta [source link unavailable in this public projection] · [run](f945978fdd78508e-RUN.json)

## Changes since version 6

- **064-cells:** 064 reports gamma 0.20 as the only admissible sandwich knockdown, with the named CR-1457 hemisphere limit. All eight concept and TRL 7 payloads at that gamma are negative. The review half reproduced all eight cells and named no fix. [064 RESULTS](e79036da6905d92f-RESULTS.json), [064 review](74ebd836a8977050-rpt-ref-408ec9521c88e0a0d103.json), [Sciences admission](f687cd5e158bd388-rpt-sciences-g6-review-c064-admission-limits-1020.json)
- **065-sources:** 065's source check reproduces. The only admissible Q is 0.33, CR-1457 equation 2.2-14, with that named limit. Q 0.82 is not an installed value. The favorable gamma ramp is not admissible. T3 and T7 are the tests that could show a better coefficient. [065 RESULTS](d99c711f6f90d228-RESULTS.json), [065 review](4fa1a0068ddd1229-RESULTS.json)
- **beta-where:** BETA is the real root of b^3+b=1, value 0.682327803828082. model61.py and model63.py each set it at line 33 and multiply it onto Q in the face-wrinkling margin, model61.py line 123 and model63.py line 130. The model text cites no handbook for that root. Equation 2.2-14's coefficient 0.33 stands for the admissible published Q. The inherited product BETA times Q, 0.225, stands only as the model line. Both values are kept. [model63.py](2c44efb4bb78a17d-model63.py), [model61.py](194954ccad05e1d1-model61.py)
- **beta1-ramp:** UNREVIEWED. The four favorable-ramp rows at Q 0.33 recomputed with BETA set to 1 land on the filed Q 0.82 cap anchors, difference 0 kg, because face wrinkling no longer binds. R20 ISA: concept -2473.6 kg, TRL7 1194.6 kg, factor 1.0766, gamma 0.5939, filed concept -5925.8 kg. R20 optimistic: concept -3772.7 kg, TRL7 -29.9 kg, factor 1.1183, gamma 0.6035, filed concept -7069.3 kg. R30 ISA: concept -6582.7 kg, TRL7 5594.8 kg, factor 1.0593, gamma 0.5946, filed concept -18148.4 kg. R30 optimistic: concept -10973.6 kg, TRL7 1456.5 kg, factor 1.1001, gamma 0.6042, filed concept -22010.5 kg. Concept stays negative. TRL 7 is positive at R 20 ISA and at both R 30 weathers. The ramp is not admissible, so those positive cells are not the programme result. [RUN.json](f945978fdd78508e-RUN.json)
- **beta1-handbook:** UNREVIEWED. The four gamma 0.20 and Q 0.33 rows recomputed with BETA set to 1 stay negative at concept and at TRL 7. Vc stays below 2, so gamma stays 0.20. R20 ISA: concept -19594.2 kg, TRL7 -14403.0 kg, factor 1.7786, gamma 0.2000, filed concept -29388.8 kg. R20 optimistic: concept -21184.2 kg, TRL7 -15892.1 kg, factor 1.8626, gamma 0.2000, filed concept -31324.2 kg. R30 ISA: concept -64564.8 kg, TRL7 -47222.3 kg, factor 1.7432, gamma 0.2000, filed concept -97877.7 kg. R30 optimistic: concept -69947.2 kg, TRL7 -52262.2 kg, factor 1.8247, gamma 0.2000, filed concept -104441.2 kg [RUN.json](f945978fdd78508e-RUN.json)
- **piece-c-state:** With today's admissible gamma 0.20 and Q 0.33 taken as equation 2.2-14, every recomputed concept and TRL 7 payload is still negative. The favorable ramp and Q 0.82 are not admissible. T7 and T3 remain the tests that could show better. [RUN.json](f945978fdd78508e-RUN.json), [version 7](5234234ce0219906-CLAIM-RECORD.json)
