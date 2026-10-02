# Paper provenance and the notice gate

The sidecar is the decision record. A PDF in a working tree is not evidence that the
public repository may redistribute it. `decision` is exactly one of `redistributed`,
`link-only`, `withheld`, or `to-confirm`. The release rehearsal removes the last three
kinds from the public tree; their sidecars retain the original SHA-256 and source.
A nonstandard statement needs a person's confirmation. In this review EASA is
`to-confirm`; NREL, Rimpel and Zheng remain `link-only` under the prior release ruling.

`python3 tools/noticecheck.py --write` generates `NOTICE`, `DATA-SOURCES.md`,
`notices.html`, and `data/README.md`. Every record appears in each notice, with unresolved
terms first; an excluded record is explicitly an audit trail, not a permission claim.
The generator reads sidecars and never fetches data, changes hashes, or edits the monitor.
`make noticecheck` validates the repository and a temporary served copy.
`python3 tools/noticecheck.py --public` must pass on the final public repository.
Normal mode deliberately allows excluded originals to remain in the working tree.

## How third-party files are identified

The gate takes all tracked paths (including paths deleted without updating the index)
and all files present recursively in `data/`, `media/`, `research/papers/`, and
`research/prior/`. Every file there needs a sidecar, except the exact project-owned
paths below and provenance JSON itself, which is parsed and validated. New READMEs,
nested PDFs, and unstaged files get no implicit exception. A release export without
Git is scanned using the same folder rule. In addition, fonts (`.woff`, `.woff2`,
`.ttf`, `.otf`, case-insensitive) and files within a `vendor` directory anywhere in the
repository need records. Generated static SVGs retain their manifest check.
This is a declared classification policy, not a detector of ownership from file bytes;
new third-party storage locations must extend this rule and its tests.

| Exact project-owned path | Why exempt |
|---|---|
| `data/README.md` | Generated project index; separately checked for freshness. |
| `data/live/README.md` | Project documentation of the unbundled mirror. |
| `media/README.md` | Project render documentation. |
| `media/ballast.jpg` | Render of the project's WebGL model; documented in media/README.md. |
| `media/drop.jpg` | Render of the project's WebGL model; documented in media/README.md. |
| `media/intake.jpg` | Render of the project's WebGL model; documented in media/README.md. |
| `media/vacuum.jpg` | Render of the project's WebGL model; documented in media/README.md. |
| `research/papers/README.md` | This project-authored schema and classification explanation. |
| `research/prior/README.md` | Project explanation of retained and withheld documents. |
| `research/prior/Pink_Energy_As_Cargo_Deep_Dive.md` | Project-authored analysis retained by the release rehearsal. |
| `research/prior/pink_energy_reference_defaults.json` | Project model defaults retained by the release rehearsal. |

## Schema and evidence

Records use `file` relative to the sidecar's directory, `source`, `publisher`, `licence`,
`licenceUrl`, `licenceStatement`, `licenceEvidence`, `attribution`, `notes`, `sha256`,
`decision`, and `licenceReason`. The optional `redistributed` boolean and
`publicationStatus` preserve the rehearsal's shape; the boolean must agree with the
single authoritative `decision`. Never copy a rewritten release PDF's hash onto an
unmodified original: the hash is of the file beside the record.

Licence evidence distinguishes a quotation read from the local PDF, a publisher page
read during this repair, and inherited provenance that was not independently re-read.
Public availability and government sponsorship alone are not grants. An inherited keep
decision is recorded as such, not presented as a new legal determination. No public source
address is invented for the withheld author documents.

`measurements` contains byte counts and, for the data files, counts computed from their
contents by `python3 tools/noticecheck.py --counts`. The gate checks these values before
rendering. Sidecar hashes must be explicit, even for excluded originals no longer present.
The sole service exception is `data/wind.prov.json`: `kind: service`, a null hash,
`decision: link-only`, and no bundled `data/live/wind.json`. Adding a forecast file
requires a file record with a real hash; the service exception cannot license bundled bytes.

The notice HTML makes no foreign requests. Source and terms addresses are citations;
repository-only paper paths are plain text so a served copy has no broken paper links.
The data and paper notices apply to the public repository even though the web manifest
excludes the research directory.
