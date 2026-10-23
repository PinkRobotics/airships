CHECK MAINLINE-057 complete — QUESTIONABLE / PROJECTION.

The concept-stage negative-payload result reproduces for all 1,232 stored subset bills across 77 configurations. The R10 itemized allowances reproduce as 707.388727 kg for P2's three-axis least set and 680.594681 kg for P3's all-axis endpoint. Their payloads after allowance are −588.693902 and −649.731971 kg. These are conditional mass accounts; physical qualification remains unknown.

One correction changes the reported maturity threshold. The card says it uses direct 048 bills at R10–15, but its principal floating, flat-growth and maturity tables use the 040 transfer at those radii too. With direct 048 data, **P2 R12 ISA first floats at the TRL-7 allowance row**, with **+1.256483 kg**, rather than the card's TRL 8. The transferred bill has −0.839968 kg at TRL 7. This does not change the concept-stage negative-payload result or the tested R20 minimum for P2 to float in both weather cases at TRL 7.

There are 82,034 final comparisons: 77,407 arithmetic/source-transfer comparisons, 4,372 provenance/conservation checks, and 255 displayed-value/ancillary checks. The first two groups agree at the stated tolerances. Four printed table cells disagree with nearest-kilogram rounding. The 3,193 entries in DISCREPANCIES.json additionally enumerate corrections to the allowance basis and source selection; they are not 3,193 independent physical failures.

| Case and field | Owner | Independent result |
|---|---:|---:|
| R10 P2 finish additional MGA, kg | 1.047120477 | 0.951927707 |
| R10 P2 least-set total MGA, corrected finish basis, kg | 707.388727405 | 707.293534634 |
| P2 R12 ISA minimum maturity row, using stated direct048 source | TRL 8 | TRL 7 |
| P2 R12 ISA TRL-7 payload, kg | −0.839968088 | +1.256483119 |
| Full 96-case transfer maximum absolute error, kg | 9.2 implied range | 160.754743578 |
| CARD P2 R12 optimistic, flat20%, nearest kg | −1,441 | −1,440 |
| CARD P2 R30 optimistic, flat5%, nearest kg | 1,604 | 1,603 |
| CARD P3 R15 ISA, flat30%, nearest kg | −3,749 | −3,748 |
| CARD P3 R20 ISA, flat0%, nearest kg | 2,235 | 2,234 |

The finish is already 1.10 times its unburdened mass. To reach a 20% allowance without double counting, the additional mass is `charged_finish × (0.20−0.10)/1.10`. The card instead multiplies charged mass by 0.10, reaching 21% of the original mass. Correcting this adds 0.095193 kg to the R10 least-set payload, giving −588.598709 kg. Both sourced and all-estimated versions are listed for all 512 P2 bills in CBE-CREDIT-EXACT-FIELDS.json.

The transfer-error range 0.191100–9.191497 kg is correct for selected masks 11 and 15. Across all 96 comparisons, absolute errors span 0.154287–160.754744 kg. The maximum is R15 optimistic, mask0: direct048 −9,978.145886 kg versus transfer −9,817.391143 kg. It is a scope correction to the prose, not an error in the stored transfer table. The R20/R30 transferred bills themselves reproduce exactly from 040, the finish replacement, primer and area-scaled reference water.

At direct048 R10 ISA, the all-four-axis P2 result is +127.252671 kg before MGA and −578.811784 kg after the stated MGA. The −589 kg description belongs to the least three-axis endpoint. The main tables instead carry the transfer's +126.882560/−579.209122 kg. SOURCE-SELECTION-MISMATCHES.json and DIRECT048-EXACT-FIELDS.json preserve all compared fields.

| Radius / weather | P2 flat-growth tolerance | P3 flat-growth tolerance |
|---|---:|---:|
| R10 ISA, published table basis | 2.830304% | 0.692623% |
| R10 ISA, direct048 basis | 2.838794% | 0.692623% |
| R30 ISA | 9.880271% | 7.506909% |
| R30 optimistic | 6.332847% | 5.006628% |

All printed 2.8/0.7% and 9.9/7.5% headline tolerances round correctly. R10 optimistic payload is already negative before growth. The tested R30 endpoints have the greatest growth tolerance in the sampled radii, but this is not a proof of a globally optimal design radius.

The item-class audit is in SOURCE-CHECK.md. All 28 item classifications, including zero-allowance categories, are accounted for. Systems/service allocations are kept at zero growth as the brief's accounting convention; a breakdown establishing how much uncommitted reserve they contain is absent. A separate 30% sensitivity on these allocated hardware masses adds 30 kg for P2 and 45 kg for ground-serviced P3. Environmental mass and buoyancy debits have different uncertainty mechanisms.

Two additional sensitivities preserve distinctions the card compresses. Applying the material-water fractions to each transferred bill instead of area-scaling the R10 reference raises the all-axis ISA water charge from 0.547613 to 0.638377 kg at R20 and from 1.232128 to 1.882427 kg at R30. Classifying P3 attachment/seams as estimated hardware while retaining 20% on other protection components increases the R10 protection MGA by 4.303513 kg. Neither is presented as measured truth.

The 053 thermal mass account reproduces a 0.606248 kg R10 payload loss; the 054 seven-day SIOX/capture bill reproduces +1.115544 kg before MGA. The eight optimism-cost extrapolations reproduce, including P2 1.779698/2.130492/1.826595 and P3 4.644935–29.659494 usage. Extrapolation beyond the specified endpoints does not establish feasible designs.

The finite tested radii, inherited optimal geometries, maturity assignments, omitted system-level margin and physical service/material assumptions remain explicit limitations. No fresh FE or thermal qualification is claimed. NFI.json gives dispositions for all eight inherited issues and eight additional findings. Qualified hull SF, actual failure probability, qualified maturity and global reoptimized feasibility remain null.

All scientific invocations used simjob at one CPU core and 1 GiB, with numerical threads set to one. Six invocations admitted and released; no refusals. A first consolidation associated three correct rounding discrepancies with the wrong displayed-row labels; that checker locator was corrected, its history retained, and final locators verified. No owner code was read, copied, hashed or executed. No other seat was contacted out of band. The final package manifest and execution receipts pin the evidence. No successor; stop and file.
