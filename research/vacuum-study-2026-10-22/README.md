# Vacuum-airship study: evidence and limits

**PUBLIC research evidence projection · 22 October 2026 · completed vacuum investigation: findings, limits and next tests.**

The studied designs have not established a buildable, floating aircraft. The best current sandwich result is a conditional model target using a hypothetical material. Numerical checks are not physical qualification. No aircraft was built or flown in this programme.

Start with the [numbered cards](index/CARDS.md), [reviews and admission limits](index/REVIEWS.md), or [claim index](index/CLAIMS.json). Each claim has its own JSON entry for stable linking.

## Current and historical records

- [Current record, version 10](record/CLAIM-RECORD-v10.json): 2,416 findings, 123 register rows and 2,299 NFI rows. It incorporates the E2 correction. The status **corrected** on the graphite review is a record correction; it does not independently revalidate every number.
- [Recovered admitted version 8](record/CLAIM-RECORD-v8.json) preserves the baseline before Piece E.
- [Incremental deltas](record/deltas/): version 9 was held for an omitted review limitation; version 10 resolves that omission. The changed original version-8 path was not accepted as the recovered baseline.
- Cards 074–076 and the half-wavelength supplement are later planning evidence in the report index, not an unrecorded version-10 append.

Original admitted v10 SHA256: `526dfde3aaa26711cc116f160d8af2a3efe4e944a774e94c0be2754b0299a180`, 21,902,372 bytes. Recovered v8 SHA256: `dede05e82b02973f6d4b2d79170dd9930563bc0500ce63717897c62da70040c7`, 21,796,723 bytes. These identify the **internal source bytes**. Public copies have different hashes because private instructions, principal quotations, addresses and host paths are removed or replaced; use MANIFEST.json for their published hashes.

## How to follow the evidence

[CARDS.json](index/CARDS.json) maps every numbered card 001–076 to its available reports, including revisions. Private task briefs are withheld. [REPORTS.json](index/REPORTS.json) indexes report and admission projections. [SOURCE-CROSSWALK.json](index/SOURCE-CROSSWALK.json) maps source hashes to packaged authored evidence. Paths beginning `evidence/` in JSON are relative to this study root, not to the containing JSON file.

[Source gaps](index/SOURCE-GAPS.json) explicitly lists references not packaged. The archive does not pretend that unavailable pinned bytes were recovered. Binary results, external source documents, archives, text extractions and out-of-scope runtime objects are not reproduced here. Their hashes/citations remain provenance. This is a text/data research publication, not a complete executable environment or a claim that every simulation can be replayed from this tree alone.

The private papers DOI 10.2514/3.5568 and DOI 10.2514/3.1932 are citation-only. No PDFs or extracted paper texts are included. Original authored reports are historical evidence: their stronger claims must be read with subsequent checks and Sciences admissions. Unpublished host paths become stable opaque references. Personal authority files and raw conversation transcripts are excluded.

## Reading statuses

- **reproduced**: the named check reproduced the scoped numerical result; read its limits.
- **unreviewed**: the result or correction has not received the indicated independent check.
- **QUESTIONABLE**: input, transfer or assumption remains unsupported or conditional.
- **PROJECTION**: estimated performance, cost or target; not a measured article.
- **physical qualification open**: no installed-hull safety factor, life or failure probability is established.

## Process evidence

The [night evaluation](night-evaluation/EVAL-NIGHT-1020.md), [Piece A measurement](night-evaluation/PIECE-A-MEASURED.md) and [job table](night-evaluation/jobs.csv) are dated assessments by the programme lead. Quota readings are provider-window observations, not audited monetary costs or complete per-task token accounting. Proposed efficiency savings are estimates. Their historical scientific figures do not override later corrections.

Publication preparation performs custody, coverage and link checks; it does not rerun science. Publication and deployment receipts belong to the landing process. The existence of this tree alone is not evidence that it has been pushed or deployed.

## Earlier publication revision 2

The first publication candidate was held before landing because it included private briefs, embedded instructions, principal quotations, an unrelated Desk letter and missed address/path tokens. This revision excludes task/authority files, substitutes explicit provenance stubs for embedded orders, withholds fields or paragraphs containing private authority quotations, and redacts address, credential and host-path tokens. Original admitted source hashes still identify private source bytes; MANIFEST.json identifies these public projections. The privacy projection changes prose and some administrative structure, not the scientific admission. Withheld source references are opaque identifiers, not downloadable links. The known dotted-number address hits were revision numbers and are preserved.

The publication contains scientific output cards and reviews, not the private prompts which requested them. Index counts refer to reports and findings; public copies are not asserted to be byte-identical originals. See [exclusion metadata](index/PUBLICATION-EXCLUSIONS.json).

Source-local Markdown links were remapped through recorded source paths and hashes. Unavailable or ambiguous targets are labelled inline rather than linked to invented locations; see [link projection counts](index/LINK-PROJECTION.json).

## Lossless packaging for repository file limits

Three large evidence JSON files retain their stable paths as reconstruction manifests:

- [First results record](evidence/a9458542ae7efde6-RESULTS.json)
- [Second results record](evidence/bb135ea1256fab45-RESULTS.json)
- [Final audit record](evidence/d3c77a11ad6c7b9d-FINAL-AUDIT.json)

Their `public-research-text-chunks-v1` schema lists ordered JSON text chunks, each below
the repository's 25 MiB limit. These files are packaging manifests; consumers must
reconstruct the original JSON before interpreting scientific fields. The decoded text
segments, encoded as UTF-8 and concatenated without separators, reproduce the exact
publication R3 bytes and SHA256. Source hashes still identify the earlier private
sources; `reconstructed_r2` retains the baseline identity; `reconstructed_r3` identifies the current public bytes; MANIFEST.json identifies
the packaged files. Historical evidence hashes remain historical provenance.

From this study directory, use the standard-library-only [reconstructor](reconstruct.py):

```sh
python3 reconstruct.py evidence/a9458542ae7efde6-RESULTS.json --verify-only
python3 reconstruct.py evidence/a9458542ae7efde6-RESULTS.json --output reconstructed-results.json
```

It verifies each chunk, the order, and the complete reconstructed byte count and hash
before writing a new output file. It refuses to overwrite an existing file. Apply the
same command to either of the other manifests. Keep reconstructed oversized files
outside tracked history. This packaging changes no scientific values, admission,
statuses or limits, and does not create a new version of the scientific record.

## Publication revision 3

This revision extends the privacy projection across file names and contents using stable opaque references. No science was rerun. Scientific numbers and booleans are unchanged. One operational status note replaces only its private identifier; all other status strings are unchanged. Internal source identities remain provenance.

Matched occurrences processed by class (file names, logical bodies and decoded JSON strings):

- absolute-local-path: 1852
- private-host: 180
- private-name: 173
- record-path: 6
- seat-id: 159155
- session-agent-id: 16
- subscription-pool: 1294

Counts include overlapping rule detections; replacement spans are merged before projection. Chunk packaging, reference paths, hashes and lengths are regenerated from these projected bytes. The same evidence bodies remain present.

### Additional exact-value privacy projection

The same revision also projects residual spellings of the private-record classes listed below. Counts are matched occurrences in logical bodies; no matched values are published. Two encoded private-path literals retain only an opaque unpublished-local reference. The underlying scientific values and all status fields remain unchanged in this additional projection.

- host-name-exact: 6 replacements; 0 additional occurrences removed with the two encoded path literals.
- pool-name-exact: 17 replacements; 0 additional occurrences removed with the two encoded path literals.
- seat-id-exact: 2582 replacements; 2 additional occurrences removed with the two encoded path literals.
- session-id-exact: 11 replacements; 2 additional occurrences removed with the two encoded path literals.

The authorized inventory contains 39 seat identifiers and nine native session identifiers. Host and pool capitalization variants use the same exact-value inventory. Hash-based evidence filenames are unchanged. No science was rerun.

Derived handles are not projected, namely receipt-id prefixes and short 8- or 4-character handles.
