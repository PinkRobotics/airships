# MAINLINE-014b metal and carbon honeycomb — ESTIMATE_PENDING_UNA

QUESTIONABLE. Nothing here is a certification. The float ceiling, pressure, lift, nu 0.33 and the fifteen faces are the MAINLINE-014 set. Knockdowns 0.20 and 0.1407 are re-optimised separately. Gc is the W shear modulus, the lower direction, on every honeycomb row.

Hexcel CR-III 5052 and 5056 typical rows from 1.0 to 3.8 pcf are the aluminium sheet, including stabilised compressive modulus and the crush column. URL https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf. Plascore PAMG-XR1 5052 rows whose sheet prints 16 to 61 kg/m3 are added. That sheet has no Ec. Ec is transferred from the CR-III 5052 row of the same cell and nominal pcf. Crush there is the bare compressive typical. URL http://plascore.com/wp-content/uploads/dlm_uploads/2025/08/PLA_PAMG-XR1-5052_2023-06-02.pdf. No carbon-fiber honeycomb sheet with stabilised Ec and both shear moduli was found in this band. Hexcel HFT fiberglass and one HRH-49 Kevlar row are the other high-modulus sheets that do print those moduli. They are not carbon. URL https://www.hexcel.com/wp-content/uploads/2026/01/HexWebHoneycombAttributesandProperties-1.pdf. The 014 foam and aramid cores, including the projections, stay in the set.

Modes are shear-trimmed global buckling, face yield, wrinkling, core shear crimping, core crush at p/2, and intracell dimpling. Dimpling stress is 2*E_f/(1-nu^2)*(tf/s_cell)^2. Honeycomb wrinkling uses design coefficient 0.33. The theoretical coefficient 0.82 is a column on the same geometry. Foam keeps design 0.50 and theoretical 0.82. On the crimp branch, global buckling and crimping are the same pressure and count as one mode.

Checks passed. Equal face and core mass at 16 kg/m3 recovers the sealed P2-E thicknesses. Infinite shear modulus at knockdown 0.20 recovers buckling SF 0.233885578993. With dimpling off, Be S-200F on HRH-10 at 32 kg/m3 recovers the filed 014 least SF 0.685338231171. The Plascore 3/16-2.0 W modulus is 20 ksi and the bare compression is 187 psi, matching MAINLINE-007. Its transferred Ec is 34 ksi.

Best three at knockdown 0.20, by least safety factor:

CNT-yarn (PROJECTION): least SF 0.750340630448 governed by core_shear_crimping, second face_wrinkling at 0.750642458194. Core Hexcel HRH-10-4.8-32 at 32 kg/m3 (QUESTIONABLE), tf 0.0010280184873 m, core depth 0.0234804348692 m. The factor to reach 1 is 1.332728043. Theoretical coefficient 0.82 gives least SF 0.750340630448 by core_shear_crimping. Dimpling SF is 79.8235624602.

Be S-200F (QUESTIONABLE): least SF 0.685338231171 governed by core_shear_crimping, second face_wrinkling at 0.685454960252. Core Hexcel HRH-10-4.8-32 at 32 kg/m3 (QUESTIONABLE), tf 0.000792920704344 m, core depth 0.0217505960684 m. The factor to reach 1 is 1.45913354095. Theoretical coefficient 0.82 gives least SF 0.685338231171 by core_shear_crimping. Dimpling SF is 61.65775805.

graphene (PROJECTION): least SF 0.677880583214 governed by face_wrinkling, second core_shear_crimping at 0.677969580728. Core Hexcel HRH-10-4.8-32 at 32 kg/m3 (QUESTIONABLE), tf 0.000984892701244 m, core depth 0.0210983617665 m. The factor to reach 1 is 1.47518607962. Theoretical coefficient 0.82 gives least SF 0.677969580728 by core_shear_crimping. Dimpling SF is 58.4943396622.

Best three QUESTIONABLE faces at knockdown 0.20:

Be S-200F (QUESTIONABLE): least SF 0.685338231171 governed by core_shear_crimping, second face_wrinkling at 0.685454960252. Core Hexcel HRH-10-4.8-32 at 32 kg/m3 (QUESTIONABLE), tf 0.000792920704344 m, core depth 0.0217505960684 m. The factor to reach 1 is 1.45913354095. Theoretical coefficient 0.82 gives least SF 0.685338231171 by core_shear_crimping. Dimpling SF is 61.65775805.

K13D2U (QUESTIONABLE): least SF 0.651932173894 governed by face_wrinkling, second core_shear_crimping at 0.652252001599. Core Hexcel HRH-10-4.8-32 at 32 kg/m3 (QUESTIONABLE), tf 0.000849638482444 m, core depth 0.0205028434909 m. The factor to reach 1 is 1.53390189968. Theoretical coefficient 0.82 gives least SF 0.652252001599 by core_shear_crimping. Dimpling SF is 52.5748018938.

M55J (QUESTIONABLE): least SF 0.593494382917 governed by face_wrinkling, second core_shear_crimping at 0.593731307698. Core Hexcel HRH-49 Kevlar 1/4-2.1 at 33.6387730853 kg/m3 (QUESTIONABLE), tf 0.000799004311326 m, core depth 0.029997869915 m. The factor to reach 1 is 1.6849359131. Theoretical coefficient 0.82 gives least SF 0.593731307698 by core_shear_crimping. Dimpling SF is 16.0609780031.

Best three at knockdown 0.1407, re-optimised:

The best three faces, cores, least safety factors and governing modes match the knockdown 0.20 ranking. The QUESTIONABLE three match as well. Where a winner sits on the shear-crimping branch, gamma is 1 and the knockdown does not enter.

The best three overall stay on Hexcel HRH-10 at 32 kg/m3, with the same least safety factors as the filed 014 card. Dimpling sits far above those values. The best aluminium for Be S-200F is CR-III 5056 at 25.6295413983 kg/m3. The 1/4 and 3/8 cells at 1.6 pcf tie, with least SF 0.668649769509 governed by global buckling. That optimum is on the stiff branch, so gamma is the knockdown 0.20, and it finishes below the aramid crimp balance. Plascore PAMG-XR1 5052 3/16-2.0, W shear 20 ksi and transferred Ec 34 ksi, reaches 0.641722323466 for Be, also by global buckling. M55J is the QUESTIONABLE face that moves. HRH-49 is Kevlar, not carbon, and it puts M55J ahead of AlBeMet. AlBeMet stays at 0.553994420508 on HRH-10. 6061-T6 least SF is 0.145930331406, governed by face_wrinkling, second global_buckling at 0.145943583637, tf 0.000536071477779 m, core depth 0.0458870294293 m, on CR-III 5056 3/8-1.0 at 16.018463374 kg/m3. The factor to reach 1 is 6.85258499973. Its theoretical least SF is the adjacent global value 0.145943583637.

Start 2026-10-19T23:48:05.977783-07:00. End 2026-10-19T23:48:23.371530-07:00. Elapsed 17.39373135380447 s, a measurement. The 2026-10-20T07:00:00-07:00 deadline is a door check-in.
