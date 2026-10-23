# MAINLINE-006 float margin against safety factor — ESTIMATE_PENDING_UNA

Dependency label DEPENDENCY002_AND_003_ESTIMATE_PENDING_UNA. No map point. Nothing here is a certification. Every factor is QUESTIONABLE. Float margin is the share of lift kept as payload. Payload in kilograms is margin times lift. Lift is 4889.44215019 kg and external pressure is 95460.83791390515 Pa, the sealed 002 atmosphere. Buckling uses knockdown 0.2, the MAINLINE-002 value. Buckling safety factor scales linearly with knockdown. Yield uses 276 MPa transferred from tensile data.

P1 varies shell thickness. Joints are 10 percent of the shell and systems are 200 kg. P2-A varies face thickness with the core held at 0.1 m. Joints are 5 percent of the sandwich and systems are 100 kg. P2-E uses MAINLINE-003's equal face-mass and core-mass split at core density 16 kg/m3. P3 varies tube wall thickness with outer radius held at 0.02 m. Film, nodes and 50 kg of systems stay fixed. The least safety factor is the lesser of buckling and yield. On P3 the film safety factor stays 2.51411998098 and does not govern.

The safety factor lost per 100 kg is the drop in the least safety factor across a payload step, divided by that step in units of 100 kg. The knee of a curve is the step with the largest drop. It is a finite difference on these margins.

## P1

0 margin 1.8601195675e-16. thickness 0.00125647794368 m. Mass 4889.44215019 kg. Payload 9.09494701773e-13 kg. Buckling SF 0.00278766036714. Yield SF 0.726555349888. Least SF 0.00278766036714.

5pct margin 0.05. thickness 0.00119097467035 m. Mass 4644.97004268 kg. Payload 244.472107509 kg. Buckling SF 0.00250458152076. Yield SF 0.688678239579. Least SF 0.00250458152076.

10pct margin 0.1. thickness 0.00112547139702 m. Mass 4400.49793517 kg. Payload 488.944215019 kg. Buckling SF 0.00223665523826. Yield SF 0.65080112927. Least SF 0.00223665523826.

20pct margin 0.2. thickness 0.000994464850358 m. Mass 3911.55372015 kg. Payload 977.888430037 kg. Buckling SF 0.00174626036494. Yield SF 0.575046908653. Least SF 0.00174626036494.

30pct margin 0.3. thickness 0.000863458303698 m. Mass 3422.60950513 kg. Payload 1466.83264506 kg. Buckling SF 0.00131647574716. Yield SF 0.499292688035. Least SF 0.00131647574716.

baseline margin 0.424771095693. thickness 0.0007 m. Mass 2812.54845073 kg. Payload 2076.89369946 kg. Buckling SF 0.000865219307006. Yield SF 0.404773316937. Least SF 0.000865219307006.

From margin 0 to 30 percent, the least safety factor falls 0.000100296691987 per 100 kg of payload. The knee is 0 to 5pct, where the least safety factor falls 0.000115791878783 per 100 kg.

## P2-A

0 margin 0. face 0.000375893644493 m, core 0.1 m. Mass 4889.44215019 kg. Payload 0 kg. Buckling SF 0.23078902511. Yield SF 0.434719192277. Least SF 0.23078902511.

5pct margin 0.05. face 0.000341582406082 m, core 0.1 m. Mass 4644.97004268 kg. Payload 244.472107509 kg. Buckling SF 0.209651118615. Yield SF 0.395038410049. Least SF 0.209651118615.

10pct margin 0.1. face 0.000307271167671 m, core 0.1 m. Mass 4400.49793517 kg. Payload 488.944215019 kg. Buckling SF 0.188527614143. Yield SF 0.35535762782. Least SF 0.188527614143.

20pct margin 0.2. face 0.000238648690848 m, core 0.1 m. Mass 3911.55372015 kg. Payload 977.888430037 kg. Buckling SF 0.146323811272. Yield SF 0.275996063364. Least SF 0.146323811272.

30pct margin 0.3. face 0.000170026214026 m, core 0.1 m. Mass 3422.60950513 kg. Payload 1466.83264506 kg. Buckling SF 0.104177616497. Yield SF 0.196634498908. Least SF 0.104177616497.

baseline margin 0.256320745969. face 0.0002 m, core 0.1 m. Mass 3636.17669088 kg. Payload 1253.26545931 kg. Buckling SF 0.122579674043. Yield SF 0.23129903825. Least SF 0.122579674043.

From margin 0 to 30 percent, the least safety factor falls 0.00863161922666 per 100 kg of payload. The knee is 0 to 5pct, where the least safety factor falls 0.00864634690261 per 100 kg.

## P2-E

0 margin 0. face 0.000336094970395 m, core 0.113432052508 m. Mass 4889.44215019 kg. Payload 0 kg. Buckling SF 0.233885578993. Yield SF 0.388692217064. Least SF 0.233885578993.

5pct margin 0.05. face 0.000318939351189 m, core 0.107642031026 m. Mass 4644.97004268 kg. Payload 244.472107509 kg. Buckling SF 0.210618070987. Yield SF 0.36885182595. Least SF 0.210618070987.

10pct margin 0.1. face 0.000301783731983 m, core 0.101852009544 m. Mass 4400.49793517 kg. Payload 488.944215019 kg. Buckling SF 0.188569334256. Yield SF 0.349011434836. Least SF 0.188569334256.

20pct margin 0.2. face 0.000267472493572 m, core 0.0902719665807 m. Mass 3911.55372015 kg. Payload 977.888430037 kg. Buckling SF 0.148128174614. Yield SF 0.309330652608. Least SF 0.148128174614.

30pct margin 0.3. face 0.000233161255161 m, core 0.0786919236169 m. Mass 3422.60950513 kg. Payload 1466.83264506 kg. Buckling SF 0.112562100066. Yield SF 0.269649870379. Least SF 0.112562100066.

baseline margin 0.256320745969. face 0.000248148148148 m, core 0.08375 m. Mass 3636.17669088 kg. Payload 1253.26545931 kg. Buckling SF 0.127497448908. Yield SF 0.286982140051. Least SF 0.127497448908.

From margin 0 to 30 percent, the least safety factor falls 0.0082711193629 per 100 kg of payload. The knee is 0 to 5pct, where the least safety factor falls 0.00951744894019 per 100 kg.

## P3

0 margin 3.720239135e-16. wall 0.00349652633775 m. Mass 4889.44215019 kg. Payload 1.81898940355e-12 kg. Buckling SF 0.0960261390545. Yield SF 0.231864737953. Least SF 0.0960261390545.

5pct margin 0.05. wall 0.00329714051632 m. Mass 4644.97004268 kg. Payload 244.472107509 kg. Buckling SF 0.0919414754281. Yield SF 0.219837140045. Least SF 0.0919414754281.

10pct margin 0.1. wall 0.00310010689553 m. Mass 4400.49793517 kg. Payload 488.944215019 kg. Buckling SF 0.0877587106779. Yield SF 0.207809542136. Least SF 0.0877587106779.

20pct margin 0.2. wall 0.00271277549854 m. Mass 3911.55372015 kg. Payload 977.888430037 kg. Buckling SF 0.0790988778055. Yield SF 0.18375434632. Least SF 0.0790988778055.

30pct margin 0.3. wall 0.00233393436598 m. Mass 3422.60950513 kg. Payload 1466.83264506 kg. Buckling SF 0.0700466404376. Yield SF 0.159699150504. Least SF 0.0700466404376.

baseline margin 0.669363166472. wall 0.001 m. Mass 1616.62967026 kg. Payload 3272.81247993 kg. Buckling SF 0.0332095404582. Yield SF 0.0708481175364. Least SF 0.0332095404582.

From margin 0 to 30 percent, the least safety factor falls 0.00177112901765 per 100 kg of payload. The knee is 30pct to baseline, where the least safety factor falls 0.0020397293075 per 100 kg.

## Measurements

Start 2026-10-19T23:02:45.723264-07:00. End 2026-10-19T23:03:14.450564-07:00. Elapsed 28.72730285488069 s. These times are measurements only. The order deadline 2026-10-20T07:00:00-07:00 is a door check-in, not a work limit.
