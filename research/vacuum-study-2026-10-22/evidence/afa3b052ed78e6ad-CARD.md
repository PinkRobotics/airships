# MAINLINE-032b. Measured panel flatness against the needed waviness.

QUESTIONABLE. Not a certification. Nothing here says a hull floats. The four needed amplitudes are the lead rows of the 032 RESULTS file. They were not recomputed.

- Be S-200F, Q 0.371, 60 psi: 0.152868766846 mm
- SR-200, Q 0.609, 60 psi: 0.0652229064039 mm
- Be S-200F, Q 0.371, 35 psi: 0.089173447327 mm
- SR-200, Q 0.609, 35 psi: 0.0380466954023 mm

Each is a zero-to-peak wrinkle component. The smallest is 0.0380466954023 mm. The largest is 0.152868766846 mm.

## Cell scale

NASA Engineering Report ER-1001, A. Pintz, C.H. Castle and R.R. Reimer, 31 December 1992, NASA Lewis grant NCC 3-77, NTRS 19950020773. https://ntrs.nasa.gov/citations/19950020773

Figure 25 prints a print-through dimple depth of 0.000065 inch, which is 0.001651 mm. Specimens through number 30 use 3/16-inch cells. Figure 24 is specimen 28, a 0.005 inch face, and one cell peak sits 0.000057 inch (0.0014478 mm) off the neighbouring peaks. That offset is node mismatch, not the dimple depth. Figure 25 does not name its face thickness.

0.001651 mm is 0.0108001 of the largest needed amplitude and 0.043394 of the smallest. It exceeds none of the four.

The same report's 3/8-inch cells, specimen 32, are maximum slopes of 0.5 to 1.6 milliradian. The page does not print a depth, and it does not name the face thickness. PROJECTION: a rise held at 1.6 milliradian across one 9.525 mm cell is 0.01524 mm, still under 0.0380466954023 mm. A sine of wavelength one cell at that slope has zero-to-peak 0.00242552133272 mm. The page describes sharp peaks and rounded valleys, so the sine is a sketch of the shape, not their measurement.

Process: vacuum-bag aluminum foil on aluminum honeycomb, Dektak II profilometer, back-face vacuum 0.25 psig after a higher vacuum had bitten the foil. Not a beryllium face. Not CR-III 3/8-1.0. The series considers faces from 0.003 to 0.016 inch, thinner than the lead sheets, and the report's own thickness plot says faces under 0.008 inch raise the slope. A thinner foil that still sits under the needed amplitude does not show the lead faces exceeding it. The transfer is QUESTIONABLE.

## Short wave, longer than a cell

Woody et al., Proceedings of the IEEE, vol. 82, no. 5, May 1994, pages 675 and 684. http://www.cso.caltech.edu/wiki/_media/cso/publications/1994-woody-procieee.pdf

Process: machine the parabola into the exposed aluminum honeycomb core, then epoxy a 1 mm aluminum sheet. Worst-case fabrication error on six antennas is 24 micrometres rms (0.024 mm). The combined techniques measure scale sizes greater than 40 mm, with an accuracy of about 5 micrometres. Laboratory points are spaced under 40 mm and each point averages a 10 mm diameter. Scales under 10 mm are attributed to the commercial sheet finish, about 2 micrometres. A 9.5 mm cell sits inside that average, so cell telegraphing is not a separate published amplitude. Deviation from the parabolic track is typically 10 to 15 micrometres rms. The installed estimate, with the known contributions added, is 24 micrometres rms. The CSO copy, after a three-disc sander for small-scale defects, reached about 3 micrometres rms against the template and an estimated 10 micrometres rms in the laboratory.

0.024 mm is under the smallest needed amplitude. It is an rms of a machined-and-bonded aluminum reflector. It is not the wrinkle component, and it is not a beryllium face.

## Whole-panel rms

S. von Hoerner, Small Surface Plates for Large Radio Telescopes, NRAO report 30, 19 September 1969, page 2. https://library.nrao.edu/public/memos/65/65R/65R_030.pdf

From discussions with Rohr: honeycomb yields an rms of 0.008 inch, printed as 0.20 mm. The inch converts to 0.2032 mm. Curved skin with ribs is 0.013 inch, printed as 0.33 mm. A milled surface is 0.003 inch, printed as 0.076 mm. Table 1 lists honeycomb at 0.20 mm rms.

0.2032 mm is 1.329 times the largest needed amplitude and 5.341 times the smallest. It is the manufacturing rms of a 1969 honeycomb surface type. The cell size is unstated. Treating that rms as the wrinkle component is a PROJECTION.

Shop bows already recorded on the 032 card, and not remeasured here, are the same kind of mismatch. Flatiron holds 0.008 inch per radial foot (0.203 mm per foot) on 0.040 inch faces over a 3/8-inch cell. Honylite states 0.7 mm per radial metre. QC Facades states a wave of 1 mm. Indy Honeycomb's finished core, before a face is bonded, allows a local step of 0.003 inch (0.0762 mm). A per-foot bow is not delta.

## AMS7902

AMS7902G section 1.3 says there are three sheet and plate classifications based on flatness tolerances and points to 3.5.5. The file obtained has three pages. Its header says page 3 of 9. Section 3.5.5 is not in the file. Revision H, https://doi.org/10.4271/AMS7902H, was not opened. No class number is stated. Sheet is 0.020 to 0.250 inch, which contains both lead faces. Section 3.2.1 limits a machined sheet finish to 55 Ra, 1.6 micrometres, under ASME B46.1. That is roughness, not flatness, and not delta. A class tolerance, once the table is in hand, would be a rolled-sheet allowance. It would not be cell telegraphing of a bonded panel.

A text extract of the HexWeb attributes brochure prints no telegraphing depth.

## What is exceeded, and by which process

The printed cell-scale depth does not exceed the needed amplitudes. The process is adhesive-bonded aluminum foil, not the lead beryllium faces. The Leighton rms, on scales the instruments measured, does not exceed them either. The process is a machined core plus an epoxied aluminum sheet, with a sander on the CSO copy. The 1969 commercial honeycomb panel rms does exceed them as a number. The process is that era's honeycomb surface, and the quantity is a whole-surface rms. Per-foot stock bows exceed them as numbers at the wrong gauge length. The process is an architectural bonded panel. No page gives an as-bonded beryllium face on CR-III 3/8-1.0 at the wrinkle wavelength. That wavelength remains unprinted.

Start and end are in RESULTS.json. Elapsed 0.000121840741485 s. A measurement of this script. The order's 07:00 field is a door check-in.
