# Labelled comparisons

Run with Python 3 and Node 22 (no package installation or network access):

    make labelledcheck
    python3 research/validation/check.py --update
    python3 research/validation/check.py --schema-only
    python3 -B -m unittest discover -s research/validation -p 'test_*.py' -v

For tests, set TMPDIR to an explicit writable scratch directory first. The checker imports the
project functions and runs the existing helium executable unchanged. Its temporary output is
removed. When CI does not set TMPDIR, the target uses a temporary directory inside
research/validation; it never falls back to the operating system's implicit scratch location.
The default target regenerates both reports in memory and compares bytes. A missing dependency,
failed function, bad source schema or stale report is a failure. A numerical MISS is a result,
and stays in the report; it never makes the target fail by itself.

The source hand-up supplied 35 records. The copy on disk was already normalized when read;
every record, quotation and printed digit is retained. No missing measurement has been filled.
schema.py checks required fields, allowed classes, normalized value/document shapes, printed
digits as strings, source coverage, quotations under 25 words, and absence of personal paths
and email addresses. The same public-text check runs on generated output.

Record 6 is deliberately retained: Table 2's gas-constant exponent is marked **do not use**.
Preserving it makes the source disagreement visible. The checker does not use it in any
calculation. Full source-file hashing records changes to contextual records as well as inputs;
the gate also reruns every model function and compares actual numerical outputs.

The citation conventions follow [the research guide](../README.md). Each comparison carries
its source record, document, locator, URL, confidence and limits. The three documents already
held here link to their catalogue entries and provenance:

| Source | Catalogue id in research/sources.json | Local document and provenance |
| --- | --- | --- |
| U.S. Standard Atmosphere, 1976, NOAA/NASA/USAF | noaa-1976-us-standard-atmosphere | [PDF](../papers/noaa-1976-us-standard-atmosphere.pdf), [provenance](../papers/noaa-1976-us-standard-atmosphere.pdf.prov.json) |
| Akhmeteli and Gavrilin, Eng 2021, 2, 480–491; DOI 10.3390/eng2040030; CC BY 4.0 | akhmeteli-gavrilin-2021-vacuum-balloon | [PDF](../papers/akhmeteli-gavrilin-2021-vacuum-balloon.pdf), [provenance](../papers/akhmeteli-gavrilin-2021-vacuum-balloon.pdf.prov.json) |
| Jenett, Gregg and Cheung, ARC-E-DAA-TN64902, 2019; NTRS 20190001133 | jenett-2019-lattice-vacuum-airship | [PDF](../papers/jenett-2019-lattice-vacuum-airship.pdf), [provenance](../papers/jenett-2019-lattice-vacuum-airship.pdf.prov.json) |

New source records are catalogued here with licences and short quotations; no additional
documents are copied. The supplied hand-up's not-found list controls these comparisons even
where older project notes assert more. In particular, no Jenett paper number, missing empty
weight, Hindenburg purity percentage or measured hover horsepower is supplied from older notes.

tolerances.json was written before the first model evaluation. Neither its thresholds nor
its reasons have been changed after observing results. A not-comparable row means the current
public function cannot express the requested conditions or uses a different architecture;
an execution failure cannot be excused with that label. Such rows still call the closest
available function and retain its diagnostic output, so changes remain visible.

The six source mutations and six model mutations in test_check.py exercise the real Makefile
target in a minimal disposable copy, restoring the changed bytes and proving green after each.
Model mutations never touch the lane's protected directories. The tests check changed row values
or model diagnostics as well as the red target, so a source hash alone cannot satisfy them.
They also prove schema rejection, failed execution, both report drift paths, and publication
of a fresh MISS through --update.

The gate is intentionally a standalone target in this lane. The lead owns adding labelledcheck
to the ordered make check prerequisites and matching CI gate list, then running CI parity.
