# MAINLINE-032. Face waviness that makes the lead Q real.

QUESTIONABLE. Not a certification. The formula is NASA CR-1457 equation (2.2-12), printed page 2-33, https://ntrs.nasa.gov/citations/19700004831. With elastic eta equal to 1,

sigma_wr = 0.82 * sqrt(E_f * E_c * t_f / t_c) / (1 + 0.64 * K_delta)

K_delta = delta * E_c / (t_c * F_c)

The card's Q is 0.82 / (1 + 0.64 * K_delta). A perfect facing has Q 0.82. Equation (2.2-14) is the design value 0.33 when the amplitude is unknown. Figures 2.2-6 and 2.2-7 are taken from MIL-HDBK-23, as that page says.

F_c and E_c are Hexcel CR-III 5056 3/8-1.0, Table II, https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf. Stabilised compressive modulus 15 ksi typical. Stabilised compressive strength 60 psi typical and 35 psi minimum. The crush column is 35 psi and is not F_c. Flatwise tension and the beryllium bond are not on the sheet. The sheet's test thickness is 0.625 inch.

Q depends on delta/t_c and on F_c/E_c. It does not depend on face thickness except when the same amplitude is written as delta/t_f. The two cores therefore share one curve and differ in absolute amplitude by 30.12/20.21.

## Amplitudes at the stabilised typical 60 psi

Delta is the zero-to-peak amplitude in equation (2.2-13).

- Be S-200F core 20.21 mm, Q 0.371 (lead Q): delta 0.152868766846 mm, delta/t_f 0.181252984167, delta/(3/8 in) 0.0160492143671, delta/9.5 mm 0.0160914491417.
- Be S-200F core 20.21 mm, Q 0.609 (cross Q): delta 0.0437634441708 mm, delta/t_f 0.0518893101385, delta/(3/8 in) 0.00459458731452, delta/9.5 mm 0.00460667833377.
- SR-200 core 30.12 mm, Q 0.371 (cross Q): delta 0.227828167116 mm, delta/t_f 0.329374247674, delta/(3/8 in) 0.0239189676762, delta/9.5 mm 0.023981912328.
- SR-200 core 30.12 mm, Q 0.609 (lead Q): delta 0.0652229064039 mm, delta/t_f 0.0942936336619, delta/(3/8 in) 0.00684754922876, delta/9.5 mm 0.00686556909515.

At the stabilised minimum, 35 psi, every amplitude above scales by 35/60. A weaker bond would scale them down again. The 60 psi numbers are an upper amplitude only if F_c really is 60 psi.

The filed dimpling margins, not recomputed, are 9.0 on the S-200F row and 4.98 on the SR-200 row. The lead amplitudes are 0.0046 to 0.024 of the 9.525 mm cell. Equation (2.2-12) does not fold a one-cell dimple into Q. FPL Report 1810-A (Norris, Boller and Voss) says the cell size changes the wrinkle wavelength, so the modes are not shown to be separate. https://ir.library.oregonstate.edu/downloads/2f75rc704

FPL Report 1810 (Norris, Ericksen and March) treats the initial wave as Fourier components, and the component near the critical wavelength is the one that grows. https://www.fpl.fs.usda.gov/documnts/fplr/fplr1810.pdf. The card names Kommers. That report's third author is March.

## Shop flatness

These are not delta. Flatiron's 3/8-cell stock panel, faces 0.040 inch, holds 0.008 inch per radial foot (0.203 mm per foot). https://www.flatironpanelproducts.com/wp-content/uploads/2020/02/Flatiron-Stock-AHP04038-Data-Sheet-2-11-2020.pdf. Honylite states 0.7 mm per radial metre on a balanced aluminum honeycomb panel. https://www.honylite.com/materials/strength-flatness-inserts. QC Facades states a wave of 1 mm. https://qcfacades.com/wp-content/uploads/2019/05/190101_Honeycomb-Flatness-Guarantee.pdf. Indy Honeycomb's finished core, before bonding, allows 0.010 inch overall and a local step of 0.003 inch (0.076 mm). https://indyhoneycomb.com/wp-content/uploads/2023/04/IHSS-N1_C.pdf. SAE AMS7902H, the hot-rolled beryllium sheet specification, defines three flatness classes. The class numbers were not read. https://doi.org/10.4271/AMS7902H. Hexcel describes telegraphing of a large cell into a thin face and prints no depth.

A per-foot bow of 0.203 mm is larger than the Q 0.609 amplitudes and near the Q 0.371 amplitude on the thinner core. That comparison is a PROJECTION if the whole bow is treated as the wrinkle component. It is not that component.

## Biaxial

Equation (2.2-15) is R_x cubed plus R_y equals 1. Equal compression solves at 0.682327803828. The cards use b = 0.6823. The difference is -2.78038280193e-05. Waviness stays inside the uniaxial stress. Multiplying by b does not count it twice. The interaction is the handbook's recommendation for flat plates. Transfer to the 10 m hull is QUESTIONABLE.

## Design 0.33

PROJECTION. If equation (2.2-12) at Q 0.33 were the whole of the design knockdown, the 60 psi amplitudes would be 0.187554924242 mm on the 20.21 mm core and 0.279522727273 mm on the 30.12 mm core. The handbook selected 0.33 from tests, not from a measured wave. 0.33/0.82 is about 0.40, the knockdown the page calls approximately 0.4.

Start 2026-10-20T01:36:24.061173-07:00. End 2026-10-20T01:36:24.061448-07:00. Elapsed 0.000276322010905 s. A measurement of this script. The order's 07:00 field is a door check-in.
