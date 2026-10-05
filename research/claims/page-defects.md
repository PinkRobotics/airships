# Claims still awaiting an owner

[The writer table](page-defects.tsv) lists each remaining sentence, number or model key, reason and needed owner. Green records these defects; it does not verify them.

Run `python3 -B tools/claims.py carry` to regenerate the table; `make claimscheck` requires its exact contents.
