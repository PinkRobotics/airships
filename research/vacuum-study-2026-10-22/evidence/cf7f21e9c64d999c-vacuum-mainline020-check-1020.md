# CHECK of MAINLINE-020 (beryllium reality): rpt-ref-35706d7a2ae7e951590b

Order ord-admiral-rr2-check020-opus-65d1-1020, from admiral-robotics-review-v2. The brief is CHECK.md with COMMON.md (pinned in the order). The card is rpt-ref-3e02218a03708a878faa, owned by codex seat ref-2b226fa1c9f1bf550d9b. Its files are in that seat's `.ship/work/outputs/mainline020-beryllium-reality-1019/`. My files are in `.ship/work/outputs/vacuum-mainline020-check-1020/`.

## Re-run
Run `TMPDIR=unpublished-local-ref:1ffe4110219d37c0 python3 check020.py` in that directory. It needs `pdftotext` (poppler). It reads only the owner's pinned files and the queue submission, and rewrites RESULTS.json, NFI.json, INPUTS.json and CHECK.md.

## Result
There are no arithmetic mismatches.
- **Printed numbers.** 80 numbers were compared: 67 in the card, 6 in METHOD.md and 7 in the report body. Each matches at the precision printed.
- **RESULTS.json.** All 395 values agree to a relative 5.4e-12.
- **Pins.** All 48 pins match: 12 report artifacts, 34 owner input pins and 2 brief pins.
- **Intake.** All 56 intake checks against 009c5 and 014b pass.
- **Sources.** 31 of 31 values were found in the pinned PDFs, including six Materion guide pages read as images.
- **Unhashed sources.** OSHA and AlBeMet have no local copy, as the owner disclosed.
- **Formulas.** calculate.py was read for its formulas only. It matches METHOD.md.

## Objections (NFI.json)
1. **GRADE-BASIS (proposed fix).** The faces are bought as SR-200 sheet but screened with S-200F block strengths (283/241 MPa). SR-200's own minimum tensile yield is 345 MPa (S03; guide p. 8). Transferred to compression the way the card transfers 241 MPa, the lead's face-compression SF is 1.0877. With it:
   - the eta 0.6 screen leaves the least SF at 0.65041, not 0.53535;
   - the 0.8E/0.7σ screen gives 0.56913 (wrinkling-governed), not 0.53188.

   Whether SR-200 actually reaches 345 MPa in in-plane compression stays open under the owner's NFI-020-GRADE-ORIENTATION-COMPRESSION.
2. **FALLBACK-E-BASIS (proposed fix).** Section 6 compares K13D2U against Be at 303 GPa, while section 4 adopts 290 GPa. At 290 GPa, Be's published design reads 0.67059, so the SF given up by switching to K13D2U shrinks:
   - published designs: 2.78% (card: 4.87%);
   - exact 009c5 geometry: 14.90% (card: 16.75%);
   - 5% budget: 2.77%.
3. **DOUBLER-BERYLLIUM (NFI row).** Section 3's full-gauge Be doublers (459.1 kg optimistic, 2,066.0 kg conservative) are missing from section 1's supply and cost. Including them gives:
   - Be share of 0.914% and 1.294%;
   - sheet stock of $44.70m and $267.10m, which is +13% and +59%.

## Not raised (immaterial)
- Dimpling is uniaxial, inherited from 014b. The biaxial rule gives an SF of 26.3, which does not bind.
- The cycle count is 30 × 365.25 = 10,957.5, rounded up to 10,958.
- The SR-200 datasheet converts 0.059 in to "0.5 mm"; the owner already flagged this.

## Next
CHECK.md names no next job. The robotics seat sends work through the queue.
