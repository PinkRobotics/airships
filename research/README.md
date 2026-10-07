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
  papers/            source PDFs and per-file provenance / release decisions
  notes/             one note per source: what it says, what we used, where we disagree
  analysis/          questions about the VEHICLE, worked: a script and a note each

  reports/           the three documents written from all of the above
```

`notes/` reads sources. **`analysis/` answers questions**, and it is where `docs/OPEN-QUESTIONS.md`
stopped being a list of doubts and started being a list of results:

| | question | the short answer |
|---|---|---|
| `mass-budget` | Does `dryT = payloadT` close? | Not as specified. Growth alone does not establish a floating structure; the [float case](../docs/FLOAT.md) states the missing structural checks and mass terms. |
| `water-availability` | How close are mapped water and generated drafting stations? | Mapped shore proximity is distinct from reachable drafting stations; depth, access and permission remain unestablished. |
| `air-ballast` | Does a vacuum hull need a cryogenic plant? | **Yes — this one is a retraction.** Sealed cells cannot ballast with air. Kept in place, because a fix that erases its own argument cannot be audited. |
| `descent` | What does getting down cost? | The current force-owner ledger prices the prescribed letdown; its diagnostics do not establish an operational saving. See `analysis/descent.json`. |
| `delivery` | Does the water arrive? | Not from 450 m. And tonnes is the wrong metric — line is. |
| `vacuum-cell` | Can the shell exist? | No drawn hull floats. The [float ledger](../docs/FLOAT-LEDGER.md) separates the bench article, closed-form bounds and hull of record. |
| `helium` | Why not helium? | **The decision is vacuum; this note keeps it honest.** Vacuum never wins on pure lift (break-even against hydrogen: 0.067 kg/m³), so the case is what the mission needs: no feedstock at fleet scale, no gas logistics tail at remote bases, crush-safe fixed displacement over a fire, and the array being the airframe. The challenge that buys is structural — and it is the rest of this repository. |

Same rule as `figures.json`: the numbers are computed, not typed. `make analysis` regenerates
every one of them, two of them by running the live model in a browser. `docs/VERIFICATION-PLAN.md`
turns what is left into four experiments and six letters.

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

**3. Each file has a release decision in its sidecar.** Working-tree presence is not a
redistribution grant. Release decisions are recorded as `redistributed`,
`link-only`, `withheld`, or `to-confirm`. Public releases keep only `redistributed` files;
excluded originals leave their hashes and source records behind. Nonstandard terms need
a person's confirmation. The generated `NOTICE`, `DATA-SOURCES.md`, and `notices.html`
carry all file records, clearly distinguishing credits from exclusions.

`research/papers/README.md` documents the exact folder rule, project-owned exceptions,
and sidecar schema. `make noticecheck` checks records, hashes, notices and the served copy;
`python3 tools/noticecheck.py --public` also refuses excluded originals still present.
The sidecar decision is authoritative for release, not a catalogue's older permission claim.
An arXiv posting or a freely accessible government-hosted manuscript is not itself a grant.

**4. A note is written from the source, not from its abstract.** `notes/` says what the source
actually establishes, which of our numbers touch it, and — the useful part — where it does *not*
support what we would like it to. A citation that does not survive being read is worse than no
citation, because it launders an assumption into a fact.

**5. Superseded project documents remain in Git history.** The current tree holds the
maintained descriptions and the dated evidence they cite. The audits under `docs/audit/`
record corrections; they are not claims that an earlier design is the present one.

## Where this is published

`research/sources.json`, `research/notes/` and the three reports are the repository record. A page
written from the same material for a reader who has not cloned anything is live at
<https://pinkrobotics.ca/research/> — it distinguishes sources marked as contradicting the project from supporting and contextual evidence,
and it carries the descent anchor in enough detail to be built from, deliberately: we are not
patenting the mechanism, and a dated public description is what stops someone else doing so.

## What is deliberately not here

Nothing in this folder is a claim that the vehicle works. The strongest honest statement the
collection supports is that the *arithmetic* is checkable and the *assumptions* are visible. The
open questions in `docs/OPEN-QUESTIONS.md` are the live list of where it is weakest, and the
reports are required to carry them rather than bury them.
