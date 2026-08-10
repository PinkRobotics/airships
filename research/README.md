# research

Everything this project relies on, was informed by, or had to go and check — kept where a reader
can follow any published number back to whatever it actually rests on.

The reason this folder exists is the reason the rest of the repository exists. The page makes
quantitative claims about a vehicle nobody has built. Some of those claims are arithmetic on
physics that is not in doubt; some rest on a paper; some are assumptions with a number attached
and no evidence at all. **Those three are not the same thing, and the difference is the whole
value of the exercise.** A collection like this is how a reader tells them apart without taking
anyone's word for it.

```
research/
  figures.json        every published figure, GENERATED from the model — never hand-edited
  sources.json        the catalogue: one entry per source, with its licence and what we take
  papers/            source PDFs we are allowed to redistribute, plus a .prov.json each
  notes/             one note per source: what it says, what we used, where we disagree
  prior/             this project's own earlier documents, kept as written
  reports/           the three documents written from all of the above
```

## The rules

**1. `figures.json` is generated, not written.** `make factsheet` recomputes it from `sim/` by
running the real model in a real browser. The reports cite it by key. Every published number in
this project has moved at least once, several of them by 50% in a single day, and a report is
exactly the artefact that goes quietly stale — so no report may contain a figure that was typed
by hand. If a number is not in `figures.json`, either the model should produce it or the report
should not claim it.

**2. A source is catalogued whether or not we can host it.** `sources.json` carries the full
record — authors, venue, year, DOI, licence, and *what we take from it* — for every source,
including the ones behind a paywall. What varies is whether a PDF sits in `papers/`.

**3. Only redistributable PDFs are stored.** This repository is going public, and a folder of
scraped paywalled papers is both a licence breach and an embarrassment in front of exactly the
readers we are asking to check our work. The test is per-item and recorded in the entry's
`redistributable` field with the reason:

- **Yes** — public domain (US Government works: NASA NTRS, USGS, DOE, NIST, USDA FS), Crown/Open
  Government Licence works with attribution, and explicit open licences (CC BY, CC0).
- **No** — everything else: AIAA, Elsevier, Springer, Wiley, Science, most of Nature. Catalogued
  with a DOI and a note, never copied.

An arXiv posting is not automatically redistributable: the default arXiv licence grants arXiv a
licence to distribute, not us. Check the item's own licence line.

**4. A note is written from the source, not from its abstract.** `notes/` says what the source
actually establishes, which of our numbers touch it, and — the useful part — where it does *not*
support what we would like it to. A citation that does not survive being read is worse than no
citation, because it launders an assumption into a fact.

**5. Our own earlier documents are evidence too, and are kept as written.** `prior/` holds the
project's previous concept papers unedited, including the parts later work contradicts. They are
dated and superseded, not corrected in place: the record of what was believed and when is part of
what makes the current numbers checkable.

## What is deliberately not here

Nothing in this folder is a claim that the vehicle works. The strongest honest statement the
collection supports is that the *arithmetic* is checkable and the *assumptions* are visible. The
open questions in `docs/OPEN-QUESTIONS.md` are the live list of where it is weakest, and the
reports are required to carry them rather than bury them.
