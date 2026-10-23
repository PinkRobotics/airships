# MAINLINE-021 source check

All material observations below remain QUESTIONABLE when transferred to this hull. The gamma interpolation remains PROJECTION. The arithmetic uses the exact pinned case and core catalogue; source changes are separate sensitivities.

S-200F: the current datasheet gives density 1850 kg/m³, typical E 290 GPa, and minimum tensile yield 241 MPa. It does not specify a compressive minimum. Its footnote offers SR-200 and PS-200 below 6.3 mm as additional options; it does not require that substitution. [Materion DS-HPP-610](https://hkvxni.files.cmp.optimizely.com/download/c2eca2d0f75e11ee9aa0f6c265376dea).

The design guide's page 4 gives S-200F compression about 255 MPa. That verifies the owner's sensitivity value, not its inherited 283-MPa starting strength. [Materion design guide](https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74).

SR-200: density 1850 kg/m³, typical E 290 GPa and minimum tensile yield 345 MPa are reproduced. Compression is unspecified. Maximum sheet dimensions are 24 by 72 inches; thinner stock from 0.020 to 0.058 inch has reduced dimensions. The printed inch/mm range has a unit inconsistency: 0.059 inch is 1.4986 mm, not 0.5 mm. [Materion DS-HPP-613](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6).

The sheet lot: Table 3 confirms 379.2/382.7 MPa compressive and 383.4/386.1 MPa tensile yield. Table 2 gives in-plane E 298.7/293.6 GPa and Poisson ratios 0.0768/0.0752. The 1.96-mm sheet measurements are quoted from Fenn et al. (1967); the original Fenn report was not opened. Neither a modern minimum nor transfer to the 0.84-mm faces is established. [NASA CR-194164, PDF p.22](https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf).

I-220H's 345-MPa number is a tensile minimum, not sourced compression. The owner correctly kept this distinction. [Materion instrument-grade datasheet](https://hkvxni.files.cmp.optimizely.com/download/a0b9e6e0f75f11eebf51367a729f0e29).

The wording “strongest sourced beryllium” needs a product-form scope. Table VIII also reports 450 MPa compression for type A tubing and 544 MPa for type PS tubing. These are not interchangeable with sheet face properties. [NASA TN D-4833, PDF p.35](https://ntrs.nasa.gov/api/citations/19680027581/downloads/19680027581.pdf).

The leading aluminium cores match Hexcel Table II. For 5056 3/8-1.0: 1 pcf, stabilized Ec 15 ksi, W shear modulus 6.8 ksi and crush strength 35 psi. For 1/4-1.6: 1.6 pcf, 30 ksi, 10.5 ksi and 50 psi. These are typical table values; the transfer to the shell remains QUESTIONABLE. [Hexcel CR III](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf).

The handbook supports the six equations cited in CHECK.md. In particular, equibiaxial honeycomb dimpling is half its uniaxial value; the wrinkle interaction gives β³+β=1. The smooth gamma curve is the owner's explicitly tagged projection. [NASA CR-1457](https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf).

The input audit confirms a QUESTIONABLE or PROJECTION tag and an inherited source reference for every eligible core row. Rechecking the whole vendor catalogue is outside this independent arithmetic check; the selected leading core values were checked directly. Source download hashes and access results are in INPUTS.json. Initial direct downloads failed; subsequent ordinary browser-header downloads succeeded for the three Materion PDFs. NASA PDFs were downloaded directly. The primary tables and guide page were visually read.
