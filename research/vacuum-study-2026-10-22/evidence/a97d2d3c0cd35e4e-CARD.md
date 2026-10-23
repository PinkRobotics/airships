# MAINLINE-004b knockdown range — ESTIMATE_PENDING_UNA

Dependency label DEPENDENCY003_ESTIMATE_PENDING_UNA. This card adds no map point. Una004 is not opened. Nothing here is a certification. Every knockdown is QUESTIONABLE.

Geometry, atmosphere, masses and the strength safety factors stay on the sealed MAINLINE-004 rows. Those rows already carry NASA SP-8032. This card does not rerun that curve. Buckling safety factor and required face modulus are scaled from the sealed numbers.

Face separation d is the sealed 004 value, core thickness plus face thickness. Classical sandwich pressure is p_cl = 4*E*tf*d/(R^2*sqrt(1-nu^2)) with E = 68.9e9 Pa, nu = 0.33 and R = 10 m. External pressure is 95460.83791390515 Pa. Buckling SF = kd*p_cl/p. Required face modulus E_req = E*p/(kd*p_cl). E_req scales as 1/kd, so a larger knockdown lowers required E. The same numbers from the sealed row are SF_new = SF_sp*(kd_new/kd_sp) and E_new = E_sp*(kd_sp/kd_new). Both forms matched within a relative tolerance of 1e-12 on every row.

Conservative knockdown: the sealed per-row SP-8032 factor. The text form is rho = 0.14 + 3.2/lambda^2 for lambda above 2, NASA SP-8032 as filed on MAINLINE-004. That monocoque cap curve is transferred with phi = pi and t_eq = (6*tf*d^2)^(1/3). The transfer is QUESTIONABLE.

Central knockdown: 0.20. Source: Wagner, Huehne, Zhang and Tang, International Journal of Pressure Vessels and Piping 179 (2020) 104015, doi 10.1016/j.ijpvp.2019.104015. The paper says equation (7) equals about 0.2 for shells which buckle in the elastic region and seems independent of the R/t ratio. The same paper's numerical lower bound for one deep dome is 0.21. Equation (7) was not evaluated for this sandwich, and lambda_s was not computed. This is monocoque dome evidence transferred onto the sandwich. It is QUESTIONABLE.

Optimistic knockdown, and the factor the main line should carry as its optimistic estimate: 0.90. Source: Wagner 2020 Table 3 row 12, Krenzke and Kiernan, Tests of stiffened and unstiffened machined spherical shells under external hydrostatic pressure, David Taylor Model Basin Report 1741, 1963, as tabulated there. The row is reliable = yes, n = 70, aluminium, R/t 10-212, lambda 1.58-33.18, H/r 0.072-1, KDF 0.11-0.90. It is the highest reliable upper in that table. The range mixes thick and thin shells and stiffened with unstiffened specimens. No reliable row reaches this sphere's lambda near 65-68. Adam and King, the same table row 11, reliable = yes, reach 0.89 at lambda up to 43.11 on PVC and are not the carried factor. The carry is QUESTIONABLE.

Classical knockdown 1.0 is the perfect-shell bound, for reference only. It is not the carry.

Sandwich-specific source, not the carry: Sim, Lee, Kim, Park and Lee, International Journal of Aerospace Engineering, 2024, doi 10.1155/2024/8765733. Numerical postbuckling of small-scale hemispherical foam-core shells gives a dimple factor 0.20 and a flat factor 0.22. The dimple factor is numerically equal to the central 0.20 and is a different source. The paper says NASA SP-8032 quoted at 0.18 and NASA CR-1457 at 0.20 may not provide a suitable knockdown for hemispherical foam-core shells. Their 0.18 is not the sealed lambda formula on this card. These factors do not support carrying 0.90. The transfer from a small hemisphere to this R = 10 m complete sphere is QUESTIONABLE.

The gap from the carried 0.90 to the per-row SP-8032 factor is NFI-OPT-GAP.

## P2-A

Face 0.000375893644493 m, core 0.1 m, face separation 0.100375893644 m, lambda 67.9559890376. QUESTIONABLE strength SF stays 0.434719192277.

Conservative knockdown 0.140692938199. Buckling SF 0.162351930234. Required face modulus 424386700549 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Central knockdown 0.2. Buckling SF 0.23078902511. Required face modulus 298541059165 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Optimistic carry knockdown 0.9. Buckling SF 1.038550613. Required face modulus 66342457592.2 Pa, below the QUESTIONABLE alloy modulus 68.9 GPa.

Classical reference knockdown 1. Buckling SF 1.15394512555. Required face modulus 59708211833 Pa, below the QUESTIONABLE alloy modulus 68.9 GPa.

Sandwich flat knockdown 0.22. Buckling SF 0.253867927621. Required face modulus 271400962877 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Sandwich dimple uses knockdown 0.2, the same buckling SF and required modulus as the central row, from the Sim et al. 2024 dimple model. Optimistic over conservative is 6.39690955011.

## P2-C

Face 0.0002 m, core 0.159364105016 m, face separation 0.159564105016 m, lambda 64.6842147374. QUESTIONABLE strength SF stays 0.23129903825.

Conservative knockdown 0.140764809648. Buckling SF 0.137388392766. Required face modulus 501497969464 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Central knockdown 0.2. Buckling SF 0.19520275431. Required face modulus 352966331053 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Optimistic carry knockdown 0.9. Buckling SF 0.878412394393. Required face modulus 78436962456.1 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Classical reference knockdown 1. Buckling SF 0.976013771548. Required face modulus 70593266210.5 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Sandwich flat knockdown 0.22. Buckling SF 0.21472302974. Required face modulus 320878482775 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Sandwich dimple uses knockdown 0.2, the same buckling SF and required modulus as the central row, from the Sim et al. 2024 dimple model. Optimistic over conservative is 6.39364342729.

## P2-K

Face 0.000270882513452 m, core 0.135441256726 m, face separation 0.13571213924 m, lambda 64.9050739631. QUESTIONABLE strength SF stays 0.313274324201.

Conservative knockdown 0.14075961351. Buckling SF 0.158259023565. Required face modulus 435362221048 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Central knockdown 0.2. Buckling SF 0.224864248514. Required face modulus 306407089857 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Optimistic carry knockdown 0.9. Buckling SF 1.01188911831. Required face modulus 68090464412.6 Pa, below the QUESTIONABLE alloy modulus 68.9 GPa.

Classical reference knockdown 1. Buckling SF 1.12432124257. Required face modulus 61281417971.4 Pa, below the QUESTIONABLE alloy modulus 68.9 GPa.

Sandwich flat knockdown 0.22. Buckling SF 0.247350673365. Required face modulus 278551899870 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Sandwich dimple uses knockdown 0.2, the same buckling SF and required modulus as the central row, from the Sim et al. 2024 dimple model. Optimistic over conservative is 6.39387944851.

## P2-E

Face 0.000336094970395 m, core 0.113432052508 m, face separation 0.113768147479 m, lambda 66.4045460271. QUESTIONABLE strength SF stays 0.388692217064.

Conservative knockdown 0.140725695373. Buckling SF 0.164568553708. Required face modulus 418670508112 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Central knockdown 0.2. Buckling SF 0.233885578993. Required face modulus 294588491932 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Optimistic carry knockdown 0.9. Buckling SF 1.05248510547. Required face modulus 65464109318.2 Pa, below the QUESTIONABLE alloy modulus 68.9 GPa.

Classical reference knockdown 1. Buckling SF 1.16942789496. Required face modulus 58917698386.4 Pa, below the QUESTIONABLE alloy modulus 68.9 GPa.

Sandwich flat knockdown 0.22. Buckling SF 0.257274136892. Required face modulus 267807719938 Pa, above the QUESTIONABLE alloy modulus 68.9 GPa.

Sandwich dimple uses knockdown 0.2, the same buckling SF and required modulus as the central row, from the Sim et al. 2024 dimple model. Optimistic over conservative is 6.39542052083.

## Measurements

Start 2026-10-19T22:48:41.445118-07:00. End 2026-10-19T22:48:50.520370-07:00. Elapsed 9.075277327094227 s. These times are measurements only. There is no time budget and no phase cap on this card. The order deadline 2026-10-20T07:00:00-07:00 is a door check-in, not a work limit. Source reading in this session preceded the start stamp. Spend for this card is the elapsed value.
