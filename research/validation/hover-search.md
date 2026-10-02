# Hover measurement search

Read-only web search on 2026-10-01, confined to a primary hover flight test. No emergency
feed was requested. Search queries, in order (three batches after the initial batch):

1. `"Airworthiness and Flight Characteristics Test" "CH-47D" "82-07"`
2. `site.dtic.mil CH-47D February 1984 hover power flight test`
3. `"82-07" "CH-47D" report dtic`
4. `"Airworthiness" "Flight Characteristics" "CH-47D" 1984 DTIC`
5. `site.dtic.mil "hover" "power" "gross weight" "CH-54B"`
6. `"An Assessment of the Hover Performance" "XH-59A" pdf`
7. `"AD" "82-07" "CH-47D"`
8. `"OUT-OF-GROUND-EFFECT HOVER DATA" "Total Engine Power"`

The named [CH-47D primary report](https://www.chinook-helicopter.com/Technical_Reports/Airworthiness_and_Flight_Characteristics_Test_%28A%26FC%29_of_the_CH-47D_helicopter.pdf)
was downloaded to disposable scratch and read: February 1984, USAAEFA 82-07,
244 PDF pages; printed p.3 and Table 1 p.4 describe testing, Appendix D p.74
explains the reduction, Appendix E Figure 10 p.90 (PDF page 100) plots OGE coefficients.
Its graph contains measured points but does not supply a tabulated dimensional point;
the coefficients are rotor horsepower after transmission correction. No point was
silently read off that crowded plot. The 53,950 lb capability statement uses an engine
power model, so it was not treated as a measured horsepower.

The NASA [1977 report index](https://ntrs.nasa.gov/api/citations/19780010046/downloads/19780010046.pdf)
identifies Arents' USAAMRDL-TN-25 as AD-A042063. Opening
[DTIC ADA042063](https://apps.dtic.mil/sti/pdfs/ADA042063.pdf) returned a non-retryable
fetch error. A [public mirror of the primary report](https://www.scribd.com/document/61264277/Advancing-Blade-Concept-Demonstration-Helicopter-Xh-59-A)
exposes its text, including Table 1 and Table 2. The Table 2 [page image](https://screenshots.scribd.com/Scribd/252_100_85/294/61264277/10.jpeg)
was also downloaded and inspected. An attempted larger image at the same URL with
`1400_100_85` returned HTTP 403; it supplied no evidence.

Selected before evaluating diskMW: Table 2, Flight 6, first **75 ft wheel-height** row
(the seventh row), 7.3 C, -132 ft pressure altitude, 10,600 lb gross weight,
1,291 hp total engine power, 315.7 rpm. Selection is positional, not closest agreement.
The report calls this OGE. Pressure altitude and temperature determine density; the
checker derives and labels the equivalent ISA density altitude rather than pretending
it was printed. Table 1's 1,018 ft2 is the overlapping coaxial disk footprint, used once.
The row is recorded at sources.json record 35 with medium confidence because the
available scan is small and the text is OCR. No mirrored PDF is added to the repository.

The prewritten 5% screening tolerance is not test-instrument uncertainty. Comparing
weight-supported ideal power divided by the project's unchanged efficiency to total
engine power tests an **effective aircraft** figure of merit. It includes losses the
model does not separately represent. It is not a rotor-only efficiency measurement.
Re-run when sim/physics.js:diskMW changes.
