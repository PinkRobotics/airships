# MAINLINE-023 checker return

The equilateral load correction and the reported numeric results reproduce:
665 raw numeric checks and 196 display/report checks pass. The 43 preserved
engineering quantities in the first report reconstruct at its superseded load.
Its five original artifact paths were overwritten, so the original full files
cannot be checked against their pins.

At 562.166273 kN, re-closed joint masses are Ti 157.685365 kg,
Invar 858.578420 kg, brazed wall extension 130.611003 kg,
and CFRP 31.038987 kg. The wrap remains the lightest sized end-material model.

Shell-only optima for the wrap are 1.465814527 at k 0.2 and 2.060754083 at
k 0.4. Bonds and end sections are sized to nominal SF 1, so these are not the
joint-inclusive assembly factors. Central node mass/stiffness, adhesive and
braze receiver/filler mass, and transferred coupon allowables remain open.

CHECK.md contains derivations and source evidence. NUMERIC-CHECK.csv and
REPORT-CHECK.csv preserve exact comparisons. INPUTS.json and source manifests
pin evidence. Eleven nonblocking NFI records include the resolved force error.
No successor job is named; stop and file.

Measured work: 2026-10-20T01:02:45-07:00 to 2026-10-20T01:19:38-07:00; 1013 seconds. No time cap.
