#!/usr/bin/env python3
"""Vision review of the printed joints: local gemma, multi-view, per-joint verdicts.

    python3 tools/joint_shots.py                 # first: capture the views
    python3 tools/review_joints.py [--joints 2,22] [--endpoint http://127.0.0.1:8010/v1]

The designer's brief, verbatim: the joints "are expected to change and vary in many
different ways over time. We need to make sure each one is fully correct... the pipe
fits where it needs to, there isn't overlap between pipes... verified visually by a
model automatically." So: for every joint, the six marked captures from
tools/joint_shots.py go to the local vision fleet (dual 5090, gemma-vision) with the
joint's own facts — arm count, per-arm SKU and engagement, the wrap census — and a
fixed checklist, and the model answers in strict JSON.

WHAT THE MODEL IS AND IS NOT ASKED. It checks what a careful eye checks: every seat
marker covered by a pipe end, no pipe through pipe, no pipe through body, counts, no
floating fragments. It is NOT the fit authority — 0.15 mm clearances are check_assembly's
(no render at any resolution shows them) — and it is briefed on the KNOWN, accepted
state (P5 partial sockets at mating planes, unequal tree/pilot spigots) so the standing
bill is acknowledged, not rediscovered, and NEW damage still stands out.

Verdicts land in research/geometry/nodes/vision/verdicts.json. Report-only for now:
exit 1 on hard failures of the checklist, 0 otherwise — gating against a frozen KNOWN
ledger (check_assembly-style) comes once the P5 geometry work settles.

NOT in `make check`: needs the fleet, which CI does not have. `make jointreview`.
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOTS = ROOT / "research" / "geometry" / "nodes" / "vision" / "shots"
OUT = ROOT / "research" / "geometry" / "nodes" / "vision" / "verdicts.json"

VIEW_ORDER = ["orbit0", "orbit1", "orbit2", "top", "joinery", "cutaway"]

CHECKLIST = """\
Answer with STRICT JSON only — no prose before or after, no markdown fences:
{"joint": "%(node)s",
 "checks": {
   "allSeated":        {"pass": true|false, "note": "in the pipes-ON views, is every green
                        seat marker covered by a pipe end entering the joint there? name
                        the arm indices that are not"},
   "noPipePipeOverlap":{"pass": true|false, "note": "does any pipe pass through another
                        pipe's volume?"},
   "noPipeBodyClash":  {"pass": true|false, "note": "does any pipe cut through the joint
                        body anywhere other than entering its own socket?"},
   "armCount":         {"pass": true|false, "note": "distinct pipes meeting this joint vs
                        the stated count"},
   "bodySane":         {"pass": true|false, "note": "one continuous printed body — no
                        floating fragments, no holes or spikes beyond the KNOWN list"}},
 "knownSeen": ["which KNOWN items are visible in these views"],
 "findings": ["anything else anomalous, one short line each; empty list if nothing"]}"""


def facts_for(idx: int, man: dict, end_classes: list) -> str:
    row = man["nodes"][idx]
    role, arms = row["role"], row["arms"]
    fams = {}
    for ec in end_classes:
        if ec["role"] == role and ec["arms"] == arms:
            k = ec["family"]
            fams.setdefault(k, []).append(f"wrap {ec['wrap']:.2f} x{ec['count']}")
    fam_txt = "; ".join(f"{k}: {', '.join(v)}" for k, v in sorted(fams.items()))
    eng = row.get("armEngagementMm", [])
    closing = row.get("armIsClosing", [])
    tree_n = sum(1 for c in closing if not c)
    return (
        f"FACTS — {row['file']}: role {role}, {arms} arms. Pipe SKUs: rim arms are the "
        f"thick 14 mm tubes, all others 10 mm. Engagement per arm: {tree_n} tree ends "
        f"with 20 mm spigots, {arms - tree_n} closing ends with 2 mm pilots (deliberately "
        f"unequal). End classes for this joint's family, from the assembly prover "
        f"(wrap 1.0 = full socket): {fam_txt or 'all wrap 1.0'}.")


KNOWN = """\
KNOWN AND ACCEPTED — acknowledge under knownSeen, do NOT report as findings:
- Sockets at the cell's mating planes are PARTIAL: the planes truncate the joint flat,
  so boundary sockets are half-open cradles and rim sockets at edges wrap only ~1/3 of
  the pipe (standing defect P5, fix in progress). Flat faces and sharp plane edges are
  the design's mating lands.
- Bare spigot stubs differ in length by design (20 mm tree / 2 mm pilot).
- In the cutaway view, pipes and body are sectioned by a vertical plane: open tube
  mouths and sliced faces at that plane are the section, not damage.
- Surfaces have a mild organic/blobby character: the joints are grown from a smoothed
  distance field; small surface lumps are the mesh, not cracks.
- Thin ghost centrelines in the joinery view are annotation, not hardware."""

LEGEND = """\
You are reviewing renders of ONE 3D-printed structural joint from a vacuum-airship cell
frame. The printed joint is the light bone-coloured body; carbon-fibre pipes are the
darker grey tubes. The single attached image is a CONTACT SHEET of six tiles, each
labelled in its corner:
orbit0 / orbit1 / orbit2 — three azimuths, pipes ON; top — overhead, pipes ON;
joinery — pipes HIDDEN, bare sockets and spigots; cutaway — sectioned, pipes ON.
MARKERS: the cyan circle is the joint's centre. Each SOLID GREEN crosshair with an index
is a NEAR-SIDE SEAT — the exact point where that arm's pipe end must butt into the
joint, visible in that tile; a correctly seated pipe covers it with tube entering the
body there. A HOLLOW ORANGE square is the same seat on the FAR side of the body in that
tile — occluded there by design, so judge that arm from the tiles where it is green.
Fail an arm as unseated ONLY if no pipes-ON tile shows its green marker covered by a
pipe end. Other joints of the frame appear at the edges and in the background — review
ONLY the joint at the cyan centre; background joints are not fragments of this one."""


def sheet_for(node_dir: pathlib.Path) -> bytes | None:
    """Six marked views as one labelled 3x2 contact sheet — the fleet engine accepts one
    image per prompt, and one sheet also keeps the cross-view checklist in one gaze."""
    from PIL import Image, ImageDraw
    tiles = []
    for v in VIEW_ORDER:
        p = node_dir / f"{v}.marked.png"
        if not p.exists():
            return None
        tiles.append((v, Image.open(p).convert("RGB")))
    w, h = tiles[0][1].size
    sheet = Image.new("RGB", (w * 3, h * 2), (8, 8, 10))
    for k, (name, im) in enumerate(tiles):
        x, y = (k % 3) * w, (k // 3) * h
        sheet.paste(im, (x, y))
        dr = ImageDraw.Draw(sheet)
        dr.rectangle([x + 6, y + 6, x + 6 + 8 * len(name) + 10, y + 26],
                     fill=(8, 8, 10))
        dr.text((x + 12, y + 10), name, fill=(255, 210, 80))
    out = node_dir / "sheet.png"
    sheet.save(out)
    return out.read_bytes()


def review_one(node_dir: pathlib.Path, brief: str, endpoint: str, model: str) -> dict:
    sheet = sheet_for(node_dir)
    if sheet is None:
        return {"error": "missing views"}
    b64 = base64.b64encode(sheet).decode()
    content = [{"type": "text", "text": brief},
               {"type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{b64}"}}]
    req = {"model": model, "temperature": 0, "max_tokens": 1100,
           "messages": [{"role": "user", "content": content}]}
    data = json.dumps(req).encode()
    r = urllib.request.urlopen(urllib.request.Request(
        f"{endpoint}/chat/completions", data=data,
        headers={"Content-Type": "application/json"}), timeout=600)
    body = json.load(r)
    txt = body["choices"][0]["message"]["content"].strip()
    if txt.startswith("```"):
        txt = txt.strip("`")
        txt = txt[txt.index("{"):txt.rindex("}") + 1]
    try:
        return json.loads(txt)
    except Exception:
        return {"error": "unparseable verdict", "raw": txt[:800]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--joints", default="", help="comma list of node indices; empty = all captured")
    ap.add_argument("--endpoint", default="http://127.0.0.1:8010/v1")
    ap.add_argument("--model", default="gemma-vision")
    args = ap.parse_args()

    man = json.loads((ROOT / "research/geometry/nodes/manifest.json").read_text())
    rep = json.loads((ROOT / "research/geometry/nodes/assembly.json").read_text())
    end_classes = rep["endClasses"]

    if args.joints:
        picks = [int(x) for x in args.joints.split(",")]
    else:
        picks = sorted(int(d.name.split("_")[1]) for d in SHOTS.glob("node_*"))
    verdicts = {}
    hard_fail = 0
    for i in picks:
        node = f"node_{i:02d}"
        node_dir = SHOTS / node
        if not node_dir.exists():
            print(f"  {node}: no shots — run tools/joint_shots.py", file=sys.stderr)
            continue
        brief = "\n\n".join([LEGEND, facts_for(i, man, end_classes), KNOWN,
                             CHECKLIST % {"node": node}])
        v = review_one(node_dir, brief, args.endpoint, args.model)
        verdicts[node] = v
        checks = v.get("checks", {})
        bad = [k for k, c in checks.items() if isinstance(c, dict) and not c.get("pass")]
        hard_fail += 1 if bad else 0
        finds = v.get("findings") or []
        state = "ERROR" if v.get("error") else ("FAIL " + ",".join(bad) if bad else "pass")
        print(f"  {node}: {state}" + (f" | findings: {len(finds)}" if finds else ""))
        for f in finds[:4]:
            print(f"      - {str(f)[:110]}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(verdicts, indent=1))
    print(f"review_joints: {len(verdicts)} joints reviewed, {hard_fail} with failed "
          f"checks -> {OUT.relative_to(ROOT)}")
    sys.exit(1 if hard_fail else 0)


if __name__ == "__main__":
    main()
