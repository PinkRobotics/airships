# Handoff — the vacuum cell, 2026-08-11

Written at the end of a long session. Everything below is verified rather than remembered:
`make check` exits 0, the tree is committed on `main`, and the site is live.

## Where things stand

**The article.** A Kelvin cell, 709 mm span, 178 L. 216 purchased carbon tubes on two SKUs
(10×8 for 180 members, 14×12 for the 36 rim edges) and **51 printed joints — the only designed
parts in the whole airship.** Everything else is stock: tube, film, tape. That framing is the
designer's and it should drive priorities.

**Mass.** 2.88 kg total: 2.39 kg tube, 0.465 kg joints, 28 g film. To float it would have to be
under 218 g, so it is 16.9× over. **The tube is five sixths of that** — printing is not the
lever, size is. Volume grows as the cube of the span while the frame inside grows far more
slowly.

**What is proven.** `tools/check_assembly.py` (3,300 lines, 16 proofs, ~120 s) proves all 432
member-ends against the SDF that generates them — it imports `gen_nodes`, never re-derives.
Its headline is `NOT PROVEN — 5 of 16 proofs fail (5 frozen in KNOWN, 0 new)`. Exit 0 means no
regression against a known-bad baseline; it does **not** mean the joints hold. The five
standing failures are P5 (216 ends cut by a land, worst wrap 0.304), P11 (13 landless nodes,
37 of 51 carry unprintable islands), P13, P14 (the bill of materials over-bills tube), P16
(2,296 of 3,888 margins fail).

**Assemblable: yes**, exhaustively — all 332 closing ends swept, inside-out build order emitted
as `buildOrder` in the contract. **Printable: no** — see P11, and A6's blocker: the extraction
grid is 5× the 0.15 mm clearance the capture depends on, so the STL cannot certify its own fit.

## The one thing that keeps costing time

**The explorer does not draw the parts.** Every joint on screen is `sphereGeom` plus twelve
`socketConeGeom`. `cell/nodes.generated.js` carries data only; `explorer.js` loads no STL.

Three separate design "bugs" the designer found by eye all traced to this and none were real:
the hub resized four times, the rim drawn with no receivers, and interference inside the
sockets. The prover says the real geometry is clean.

Fixing it is cheap and measured: re-run the same SDF coarser rather than decimating. Node 09 at
res 40 gives **3,716 triangles against 33,280 at res 112, mass within 0.1%**. All 51 nodes ≈
190k triangles, ~1 MB gzipped. **This is task #67 and it is the highest-value work left on the
page** — it retires an entire recurring class of complaint and would show the land truncations
and partial wraps the prover measures.

## Open work, in priority order

1. **#67 draw the real node meshes** — above.
2. **#60 the foldable net** — the designer will laser-cut from it. Full construction is spelled
   out in the task: face adjacency by shared vertex pairs, spanning tree (13 folds / 23 cuts),
   `T_child(t) = T_parent(t) · R(hinge, θt)`. **Gate that no two faces overlap at t=1** — an
   overlapping net cannot be cut and the animation will look perfect anyway.
3. **#65 clear the five frozen proofs.**
4. **#64 integrate the barrier and seam notes** into `research/notes/` + `sources.json`; both
   drafts are complete at `~/tmp/skin-barrier/`. Harmonise the budget figure first — 2.90
   cm³/(m²·day) is right for the 178 L article; `seams.md` deliberately used the stricter 1.6.
5. **#68 make `make check` skip unchanged work** — but read the safety constraints in the task
   before building a cache. This repo has twice shipped a gate that lied by comparing a stale
   file.

## Traps that have each cost real time

- **`main` is committed but NOT pushed.** Local commits do not survive a disk loss, which was
  the reason for committing. Ask before pushing; the remote is private.
- **Never write to `/tmp`** — it is a 45 GB RAM tmpfs and has OOM-killed a service. Use
  `~/tmp/`.
- **`pkill -f` matches your own shell** even with the bracket trick in some forms; it killed a
  session shell today. Prefer collecting PIDs from `pgrep` and killing them individually, and
  clean up `serve.py` after every screenshot — 13 orphans accumulated in one session.
- **The background-task notification fires when the *wrapper* exits**, not the work. A
  `make check` launched with `& sleep 2` reports "completed" immediately and its log looks
  truncated because it is still being written. Poll for a sentinel line.
- **`make stamp` before any check** after touching `cell/` — the site hash moves and
  `stampcheck` fails first, wasting a whole run.
- **Use the fast path.** For explorer-only edits `make stamp && make explorercheck` is **11 s**
  against ~4 min for the full chain; `check_assembly` alone is 122 s of it. Full chain once
  before commit, not once per edit.
- **Editorial sweeps break things.** Two defects were introduced today by find-and-replace over
  prose without reading the surroundings: a label string that was a concatenation got its first
  half replaced and the tail welded on, and a gated `data-n` binding was deleted with the
  paragraph around it. Every removed binding the gate reads will fail the build — check with
  `grep -c 'data-n="X"'` against `tools/check_explorer.py` before deleting copy.
- **Prose is not gated against the plan.** "crushed, sealed and pumped down" survived review
  and was wrong in all three respects — the documented order is bake out, bond the barrier in
  the chamber, seal last, and the crush is the atmosphere doing it afterwards. Nothing holds
  page copy to `VERIFICATION-PLAN.md`.

## Deploy path

```
make stamp && make check                      # or the fast path above
python3 tools/publish.py                      # -> pink-sites/pinkrobotics/airships
cd ../pink-sites && git add -A pinkrobotics/airships && git commit
./deploy.sh pinkrobotics                      # refuses a dirty tree, exit 65
# then purge Cloudflare (token at ~/.config/cloudflare/token-dns, zone pinkrobotics.ca)
```

Live behind Caddy basic auth `tyler/copper` at `pinkrobotics.ca/airships/cell/explorer.html`.
