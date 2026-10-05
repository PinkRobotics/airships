# The public claims register

`make claimscheck` inventories static public text and declared model bindings. Green means every occurrence has a checked owner or an explicit, reproduced defect. It does not verify those defects, the model's assumptions, structural feasibility, suppression or flight performance. The fleet is simulated and has never flown; nothing here says any fire would have burned differently.

Run `python3 -B tools/claims.py carry` after integrating text or model changes. It applies the same tested rules to every occurrence, retires source identities that no longer reproduce, revalidates placements, records new defects, and prints per-file and per-headline drift. Review its changes, including the append-only receipts. Run it again: the second invocation changes no file. `check` and `extract` are read-only. No command fetches an agency endpoint.

```sh
python3 -B tools/claims.py carry
make claimscheck
python3 -B tools/claims.py extract > "$TMPDIR/claims.json"
python3 -B research/claims/mutation_proof.py
```

Set `TMPDIR` to designated project scratch before tests. The mutation proof copies the complete local dependency tree, initializes only a disposable index, plants failures, restores exact bytes and checks green after every plant. It never commits or changes a page in the worker tree.

The scope includes manifest-served HTML, `README.md`, `GOALS.md`, reports, then `docs/PHYSICS.md`, `docs/ARCHITECTURE.md`, analysis Markdown, the simulator, test and tool READMEs, and `DATA-SOURCES.md`. Dated working, audit and landing records, source notes without dated occurrence reviews, PDFs, image pixels and other runtime-only strings remain outside scope. Dynamic table rows and strings assembled by external scripts are still held by their existing browser/model gates; this register makes no inventory claim about them.

Each static identity is the relative file, normalized sentence/cell digest and ordinal, including repeated identical sentences. Placement binds the surface, block and table context, generated region and figure marker. Accessibility text, controls, metadata, SVG text, inline templates and written-out numbers are included. A model span has a symbolic identity that includes its attribute, key and formatting; its computed value may change without changing that identity. Every `data-n` and `data-cat` span is inventoried. Unknown page contexts or keys are defects. Digests use original text; public excerpts scrub local paths, addresses and domains.

## Ownership rules

- Blocks detected by the ledger come from `check_float_ledger.source_blocks` and `inspect_block`, then `float_claims.apply` and `key_of`. An exact record key owns every contained occurrence only when its disposition passes. Allowance reasons travel with owners. A deferred block remains a defect carrying its own deferral reason, including inside a checked generated region. Ledger ownership does not establish flight or suppression. Records are read-only inputs to this gate.
- Energy markers delimit regions written by `energy-documents.mjs` and `gen_energy_pages.mjs`. The producer is rerun with `--emit` and the exact region is compared. Generated analysis Markdown is compared by the same producers' `--check` operations used by `energydoccheck`. Outside-region text gets no exemption, and a `data-energy-*` attribute alone grants no ownership.
- Other producers own the balanced monitor fallback regions, exact `f:` figure markers, the generated pages and notices, and the exact README regions held by `readmecheck`. Figure-marker values are compared at their printed precision; fallback membership is checked here and fresh browser regeneration remains `fallbackcheck`'s duty. Analysis manifest rows own exact tokens only where `check_analysis.CONTEXTS` names their quantity and location. Value-only searches leave a defect: identical digits elsewhere never establish ownership.
- Model spans execute the pages' own pure context declarations and `computeCtx`, excluding DOM tails. The gate checks the named key resolves to a finite computed number in the page default context and validates precision and scale. It does not assert it has observed a rendered page. A model key cannot clear a ledger deferral in its containing block: the span carries the record key and its physical-basis verdict as well. Existing browser gates continue to check those pages.
- A label owns only its numeric clause in the same sentence. Accepted words are `assumption`, `assumed`, `target`, `illustration`, `illustrative` and `vision`, followed by a colon or dash. Commas, semicolons and a previous number delimit scope. A nearby label, a label two sentences away, or a label attached to another number cannot pass. A label declares a role, not feasibility.
- Citations require a source record, local capture or an explicit capture reason, a locator, and a dated reviewer bound to the occurrence digest. No citation reviews are invented by carry.

For legacy throughput, delivered-tonnage and energy-per-tonne keys, all forms `deliver`, `delivers`, `delivered`, `delivering`, `delivery` and `deliveries` trigger a water-basis defect. An unrelated release mention cannot waive it. The reviewed energy generators instead bind exact-input plans and publish water requested, kept aboard and delivered per cycle over the planned lines, beside the boundary that released water is not suppression. Legacy marker arithmetic alone does not establish those reviewed plans.

## Nonclaims and residue

Token-specific rules recognize dates, identifiers, unit exponents, section/step labels, cross-references and versions. Section-symbol references resolve numbered headings in their own document; ranges check every section. A broken reference is an explicit reference defect.

Function-word rules accept only tested discourse ordinals, document/process order, the adjectives `first-party`, `one-way` and `one-off`, specific pronominal uses of `one`, and specified idioms using `single`. Physical counts, durations, fractions and rates remain claims. Every current occurrence handled by these additional rules is listed in `nonclaim-reclassifications.tsv`; exact before/after owner changes are in `carry-history.json`. The rules are deliberately narrow.

`page-defects.tsv` is generated and checked for staleness. It groups each remaining sentence and number by file, gives its reason and the owner a writer needs to supply: a dated citation review, generator, label, ledger entry or rewording. The count describes missing ownership, not a count of false statements.

`accepted-defects.json` preserves the original acceptance hashes and source digests. Additions need printed acceptance receipts. Carry adds digest-bound transitions for changed failures and verified owners; an owner retirement is rechecked every normal run. A narrower inventory cannot retire an unchanged source. Receipts are reviewable repository data, not a cryptographic signature. Tampered receipts, removed entries, stale placements, newly unregistered text and nonreproducing defects fail. The historical seed refuses to overwrite an existing register.

`rule-changes.json` and `carry-report.tsv` record this carry's old/new inventories, each ownership rule's movements and the exact remaining ledger dispositions. Earlier evidence and pending-carry files are retained as dated history, not current gate results. Current command outputs are in `check-evidence.json` and `mutation-evidence.json`.

The audit Markdown contains hand-written guidance. Quoted source sentences and generated lists live in TSV tables, which `claimscheck` regenerates and compares byte for byte, including missing files. `carry-report-baseline.json` retains the claims3 report as a historical snapshot; its TSV projection separates that snapshot from current counts. Hand-written audit prose remains in the ledger inventory.
