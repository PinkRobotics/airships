# MAINLINE-045 leak, descent and landing: sourced values (53 rows, leak.json)
All quotes were checked as substrings of the text actually read. Tag QUESTIONABLE on every row.

ORIFICE FLOW
- Flow chokes at Mach 1 [NASA Glenn mflchk]; critical pressure ratio p*/p0 = 0.528 for gamma 1.4 [Wikipedia Choked flow]; mdot = Cd A sqrt(gamma rho0 P0 (2/(gamma+1))^((gamma+1)/(gamma-1))) [same]. Sub-worker arithmetic for air: mdot = 0.0404 Cd A p0/sqrt(T0) (SI), about 241 kg/s per m2 effective area at 101325 Pa, 288 K.
- Discharge coefficient: sharp-edged 0.6 [LMNO, citing Shapiro]; 0.6 to 0.9 measured, higher with rounding [LMNO citing Kayser and Shambaugh 1991]; orifice plates 0.6 to 0.63, typical 0.6 to 0.85, first guess 0.62 [Wikipedia Orifice plate]; C = 0.60 for square-edged orifice, air seal flaw [NASA TM-103604]; 0.58 inferred for 0.5 mm hole [Mungan 2024]; 0.8 assumed for habitat leak [NASA NTRS 20250002458]; LMNO default 0.8.
- Breach time (OUTFLOW only): 1 cm2 hole, 30 m3 cabin, halves pressure in 500 s, scales as 1/area and with volume [spaceacademy.net.au].

SPHERE DRAG AND ADDED MASS
- Subcritical Cd about 0.5 (0.47); drag crisis near Re 3e5 to about 0.2, minimum about 0.1 [Wikipedia Drag crisis / Drag coefficient; MIT OCW via LibreTexts]; NASA Glenn: .07 to .5. Added mass of a sphere = half the displaced fluid volume times density [Wikipedia Added mass].

REGULATIONS AND AIRSHIP CRITERIA
- 14 CFR 101.19: moored balloon must have a device that "will automatically and rapidly deflate the balloon if it escapes from its moorings"; no time or size given. 101.13: not above 500 ft (152.4 m) AGL; 101.15: notice above 150 ft; 101.17: pennants every 50 ft from 150 ft; 101.1: applies above 6 ft diameter or 115 ft3.
- 14 CFR 31 (manned free balloons): deflation means (31.55); rip cord force 25 to 75 lbf (31.57); uncontrolled-descent vertical velocity must be determined (31.19), no number; drop test 36 in or the max vertical velocity, whichever higher (31.27(c)); envelope safety factor 5 (31.25).
- Transport Airship Requirements (TAR 2000, derived from FAA-P-8110-2): demonstrate descent of at least 7 m/s (TAR 65); lifting-gas valves sized for 15 m/s climb, two valves minimum (887(a)); ballonet air induction for descent not under 7.5 m/s (887(c)); landing limit vertical velocity floor 3 ft/s = 0.914 m/s (473); rapid and, if unattended, automatic deflation on mast breakaway (883(g)); disposable ballast to restore equilibrium (895).
- Aerostats: rip panel is a slit from the top, 1/5 circumference, reinforced cover [McGill thesis 2005]; ARDD and ground-tied rip line [LTA Solutions]; barrage balloons ripped a panel on breakaway [Wikipedia]. FAA AC 91-71 hot-air balloon approach: 26 to 27 fpm for 3 deg glidepath at 5 kt (guideline).

VACUUM BALLOON
- Akhmeteli and Gavrilin, Eng 2021 (doi 10.3390/eng2040030): "only rough vacuum is required"; leaks not studied; valve between interior and exterior for evacuation or altitude control; buoyancy loss from shell compression under 0.4 %. Nothing found on puncture inrush, implosion or descent.

GAPS
- FAA-P-8110-2 text itself not found (TAR used instead). No aerostat deflation times, no TCOM/ILC Dover/Lockheed hardware pages. No primary Cd source for torn holes or cracks (ISO 5167, Perry, Idelchik, Crane TP-410, Shapiro, Kayser and Shambaugh not opened; NRC ML070860286 HTTP 403; NASA TN D-5467 OCR unusable; NTRS 19750049854 404).
- No inflow/repressurisation time formula for an evacuated volume; no punctured-balloon descent speed data (search snippets not recorded); no airship/balloon landing impact limits beyond the above; Achenbach 1972 not opened; vacuum patent and Oregon thesis not opened (403). Full list in leak.json "gaps".
