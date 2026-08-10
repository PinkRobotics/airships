# reports

Three documents, one model, three audiences. They are written from `../figures.json`,
`../sources.json` and `../evidence-map.md`, and they say the same things at different depths —
including the things that are wrong.

| | for | length |
|---|---|---|
| `01-brief.md` | media and public | 2 pages |
| `02-paper.md` | technical readers | ~10 pages |
| `03-diligence.md` | investors doing full diligence | full |

## The rule these obey

**No report may type a model number.** It cites one:

    the P-10000 delivers 13,183 t/h<!--f:P10000.cycle.tph--> on a 15 km leg

The marker is an HTML comment, so it is invisible wherever the Markdown is rendered.
`tools/check_figures.py` reads the number in front of it, looks the key up in `../figures.json`,
and fails the build if they disagree at the precision the author wrote. `make factsheet`
regenerates `figures.json` from the live model in a real browser.

This exists because every published number in this project has moved at least once and several
have moved by half in a single day. Code that goes stale fails a test. Prose that goes stale just
sits there being wrong, in the document most likely to be forwarded to someone who will not check
it — and a report full of confidently-stated obsolete numbers is worse for this project than no
report at all, because the entire pitch is "our arithmetic is checkable".

Figures from **cited sources** are written plainly and are not markable. They are not ours to
regenerate, and `../sources.json` is where they are accounted for.

## What all three are required to carry

The defect list. Not a softened version of it, and not only in the long one. `01-brief.md` names
all four findings that contradict the project in its second half, because a two-page summary that
drops them is the exact artefact this repository exists to not produce.

**And what happened to them.** Two of the four were corrected on 2026-08-09 — the solar skin and
the nitrogen round trip — and all three reports keep them in place, marked as closed, rather than
quietly deleting them. What a project fixed, how fast, and in which direction the numbers moved is
evidence about the project. Both of these made the published figures worse.

A public version of the same material, written for a reader who has not cloned the repository,
is at <https://pinkrobotics.ca/research/>.
