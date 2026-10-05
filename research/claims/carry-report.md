# Claims carry report

[The carry table](carry-report.tsv) includes the retained claims3 snapshot and current per-file and per-headline counts. The snapshot is historical; current rows are regenerated from the register and its receipts.

Run `python3 -B tools/claims.py carry` to regenerate the table; `make claimscheck` requires its exact contents.
