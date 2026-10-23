# CHECK MAINLINE-007b — checker behind rpt-ref-3dd5ab5528276031581d

Checker: ref-9af2822b3fe57c40be31. Order: ord-admiral-rr2-check006-007-007b-muse-1019. Brief CHECK.md with COMMON.md, pinned and verified. Owner scripts were not used; numbers are from my arithmetic.py using the NASA CR-1457 equations as stated on the owner card, with geometries and material moduli taken as pinned inputs from 003/007 RESULTS.

## Verdict

Numeric PASS. Zero mismatches at relative 1e-9 across all 13 evaluated material/geometry comparisons and all 17 crimp-boundary rows. No text mismatch in the derived claims below.

Formulas I used: h = core + tf, tc = core, sigma_0 = E*h/(R*sqrt(1-nu^2)), crimp stress = h^2*Gc/(2*tf*tc), Vc = sigma_0/crimp, Kc = 1 - Vc/4 for Vc <= 2 (else 1/Vc), gamma_d = 0.20 for Vc < 2 (else 1), critical pressure = 4*gamma_d*Kc*sigma_0*tf/R. Classical pressure is the kd 0.2 sandwich pressure, so on this branch SF_general/SF_classical = Kc exactly. Foam wrinkling: uniaxial 0.50*(E*Ec*Gc/(1-nu^2))^(1/3); advisory uniaxial is the same without (1-nu^2). The equibiaxial factor is my own Newton solve of x^3 + x = 1, x = 0.6823278038280193. Honeycomb wrinkling: 0.33*E*sqrt(Ec*tf/(E*tc)), times the same factor, divided by membrane stress p*R/(4*tf). Crimp boundary at Vc = 2: Gc = sigma_0*tf*tc/h^2. Handbook-over-advisory crimp pressure ratio = h/tc.

## What reproduces

P2-E with Plascore 5052 3/8-1.0 at 16 kg/m3 (smaller W shear modulus): Vc 0.10135521292620196, Kc 0.9746611967684495, SF_general 0.22795919832772132 against classical 0.2338855789925097, ratio = Kc. Yield stays 0.3886922170642076, so general instability still governs.
On the 007 rows at 32 and 16 kg/m3, every material reproduces: ROHACELL 31 ratio 0.9056527530715882, Divinycell H35 0.8977904824942204, Plascore 3/16-2.0 0.9911054576838794, Hexcel HRH-10-4.8-32 0.9123918421379033, Hexcel HRH-10-6.4-24 0.863720643326 (the largest trim), Plascore 3/8-1.0 on the 16 row 0.9745863432732574. Duplicate max_least rows at 32 and 16 are the same points, as the card says. All Vc are below 2, so no sourced core enters the crimping branch, gamma_d stays 0.20, and infinite shear (Kc = 1) restores the classical pressure, as claimed.
Wrinkling: foam equibiaxial SF is 0.7090620695678252 of the advisory uniaxial SF (ROHACELL 0.12449046966262503, Divinycell 0.16122006551220763), both still above their trimmed general-instability factors. Hexcel honeycomb equibiaxial wrinkling SF 0.05652863640260287 and 0.0415196459641 are below their trimmed general-instability factors, so that local mode would govern if admitted, exactly as the card states. Plascore has no Ec, so no wrinkling stress is computed for it.
Boundaries: Gc for Vc = 2 reproduces on every row, about 2.453 MPa on the buckling-optimal rows (P2-E exact 2445868.5773324715 Pa; 1 kg/m3 equal split 4635858.192645354 Pa). Handbook/advisory crimp ratio = h/tc reproduces (1.002962962962963 on P2-E, up to 1.0059970014992503 on the 32 rows).

## Mismatch list (exact)

Numeric mismatches: none. RESULTS.json compares Vc, Kc, SF_general, SF_classical, ratio, crimp ratio, foam and honeycomb wrinkling fields for each comparison, plus every boundary row. Pins: 9 of 9 match, pin_bad 0. The Schaedler microlattice comparison carries no geometry or modulus and was skipped as the card does (no SF claimed).

Text claims checked and confirmed: gamma_d = 0.20 equals kd and the ratio is Kc on the moderate branch; the gamma_d jump at Vc = 2 is a discontinuity the card itself flags and no row is near it; using external R in both pressures leaves the ratio unchanged (both pressures scale as 1/R^2); densities 8-1 and the microlattice have no sourced Gc/Ec and are not revised.

## Sources and tags

Source is NASA CR-1457 (Sullins, Smith, Spier, December 1969), NTRS URL named on the card, equations listed; the pinned PDF in the owner unit hashes to the filing value (included in the owner's INPUTS pins). Yao 1962 and Plantema 1966 were not opened separately, as the card states. Material Gc/Ec values are the QUESTIONABLE datasheet values from 007, with the smaller plate-shear modulus used, and Hexcel Ec is the stabilised compressive modulus, QUESTIONABLE as Ec. The whole card is QUESTIONABLE, certification none. Owner NFI-SHEAR, NFI-WRINKLE, NFI-SAND, NFI-KD, NFI-GEOM, NFI-CORE-FLOOR and NFI-BIAX stand; checker rows are in NFI.json. One record note, not a mismatch: owner RESULTS started_at equals ended_at, so its elapsed is not a usable measurement; no number depends on it.

Files: RESULTS.json, INPUTS.json, NFI.json, arithmetic.py (my script; its stamps measure that script run only).
