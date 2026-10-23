# CHECK — MAINLINE-004 (rpt-mainline004-grok-knockdown-card-1019)

Independent check, glm seat ref-c713c40ee838487ac6d3, owner grok seat
ref-2543c559b19ffce7dfdd. Order ord-admiral-rr2-check012-004-004b-glm-1019.
Brief CHECK.md + COMMON.md (pinned in INPUTS.json). Owner files read-only;
the owner's script was never read. My script: check004.py (this directory,
covers both 004 and 004b).

## Method
Own arithmetic from the pins: the sealed 003 geometry re-solved from the mass
rules (P2-A core fixed 0.1; P2-C face fixed 0.0002; P2-K one factor k; P2-E
equal split), exact closure demanded against the sealed lift; t_eq, lambda,
kd = 0.14 + 3.2/lambda^2, classical p_cl, both SF sets, required moduli and
ratios recomputed; every card number regex-transcribed and diffed.

## Result — PASS, zero mismatches (tolerance 5e-9 relative)
- Mass closure: total mass equals the sealed lift 4889.442150186961 kg for
  all four families.
- t_eq hypothesis: the card's values match (6*tf*d^2)^(1/3) with d the face
  SEPARATION (core+tf); the core-only form is excluded on every row.
- COMMON.md invariant: 0.2 * p_cl at the P2 baseline = 11701.558395327309 Pa,
  the sealed 006 number, exactly.
- All kd/lambda/p_buck/SF/E_req/ratio and yield-SF-unchanged values agree.

## Sources (DOI confirmation)
- Wagner, Hühne, Zhang, Tang 2020, Int J Pressure Vessels Piping 179 (2020)
  104015, doi 10.1016/j.ijpvp.2019.104015: PDF sha256 equals the owner's pin
  (b54893a4...). Verified verbatim: eq (7) "equals to about 0.2 for shells
  which buckle in the elastic region and seems to be independent of the R/t
  ratio". Table 3 row 12 Krenzke & Kiernan: n=70, Aluminium, R/t 10–212,
  H/r 0.072–1, lambda 1.58–33.18, KDF 0.11–0.90, reliable=yes.
- NASA SP-8032: the monograph page itself remains unretrieved (the owner's
  NFI already records this gap). Wagner 2020 characterizes SP-8032 as "a
  statistical lower bound of different empirical data" and applies KDF 0.14
  to its design example; the 0.14+3.2/lambda^2 text form is not independently
  retrievable from my sources — recorded, arithmetic verified regardless.

Machine output: CHECK-OUT-004.json / RESULTS.json. No objection: no NFI row,
no fix card.
