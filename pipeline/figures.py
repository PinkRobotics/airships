#!/usr/bin/env python3
"""The four hand-built SVG figures on the concept page, generated and inlined.

  python3 pipeline/figures.py            # rewrite the figures inside concept/index.html
  python3 pipeline/figures.py --print    # sizes only, touch nothing

These are diagrams, not renders: they carry structure and constraint rather than
measurement, every number in them is hard-coded WITH its provenance, and an annotation that
would leave the viewBox is a build error rather than a clipped label. (The photorealistic
vehicle figures are a different pipeline entirely — see 3d/scripts/figures.mjs, which
projects the parametric model.)

Vehicle dimensions here are the project's own demonstration assumptions: 4:1 prolate
spheroids sized to displace 220,000 / 2.2M / 22M cubic metres. References: LZ 129
Hindenburg 245 m (well documented); Boeing 747-400 70.7 m; Lions Gate Bridge main span
472 m (City of Vancouver / span record).
"""
import argparse
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
# The page's palette, as literals. These match the CSS custom properties the concept page
# sets (--warm and its dimmed pair); an inlined figure has no stylesheet to inherit from.
WARM, WARM_DIM = "#ff4fa3", "#8c2a58"
COOL, COOL_DIM = "#7aa2c8", "#47637d"
GREEN, RED, FAINT, MUTED, BONE = "#46d06e", "#d98b80", "#74747f", "#9a9aa5", "#c9c3b6"
W = 880


def _guard(x_end, label, fig):
    if x_end > W:
        raise SystemExit(f"{fig}: annotation overflows viewBox: {label!r}")


def fig_cycle():
    """The mission loop. Node coordinates are hand-placed on a rounded-rect track."""
    tint = {
        "approach · hose paying out": COOL_DIM, "fill": COOL,
        "outbound — hose up · climb · let down": MUTED,
        "drop run": WARM, "escape climb": WARM_DIM,
        "return — ballast · descend": MUTED,
    }
    # (label, x, y, anchor, dx, dy, big) — six phases; the hose rides the approaches
    nodes = [
        ("approach · hose paying out", 120, 210, "end", -14, 4, False),
        ("fill", 95, 130, "end", -14, 4, True),
        ("outbound — hose up · climb · let down", 430, 48, "middle", 0, -14, True),
        ("drop run", 748, 92, "start", 14, 4, True),
        ("escape climb", 772, 152, "start", 14, 4, False),
        ("return — ballast · descend", 430, 262, "middle", 0, 24, True),
    ]
    out = [
        # the track itself: one loop, direction marked by three small chevrons
        f'<rect x="95" y="48" width="677" height="214" rx="86" fill="none" '
        f'stroke="{FAINT}" stroke-opacity=".45"/>',
        # direction chevrons: top edge runs left->right, bottom right->left
        f'<path d="M330 42 l12 6 -12 6" fill="none" stroke="{FAINT}" stroke-opacity=".8"/>',
        f'<path d="M552 256 l-12 6 12 6" fill="none" stroke="{FAINT}" stroke-opacity=".8"/>',
        f'<path d="M89 160 l6 -12 6 12" fill="none" stroke="{FAINT}" stroke-opacity=".8"/>',
        # the two poles of the loop
        f'<text x="30" y="16" fill="{COOL}" font-size="11.5" font-weight="600">AT THE SOURCE</text>',
        f'<text x="30" y="30" fill="{FAINT}" font-size="10.5">hose down · pumps on · water pulls the ship down</text>',
        f'<text x="850" y="292" fill="{WARM}" font-size="11.5" font-weight="600" text-anchor="end">AT THE FIRE</text>',
        f'<text x="850" y="306" fill="{FAINT}" font-size="10.5" text-anchor="end">the drop is the escape manoeuvre</text>',
    ]
    for label, x, y, anchor, dx, dy, big in nodes:
        c = tint[label]
        r = 7 if big else 4.5
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{"none" if not big else c}" '
                   f'stroke="{c}" stroke-width="1.6"{" fill-opacity=\".85\"" if big else ""}/>')
        tx, ty = x + dx, y + dy
        est = len(label) * 6.6
        x_end = tx + (est if anchor == "start" else est / 2 if anchor == "middle" else 0)
        _guard(x_end, label, "cycle")
        out.append(f'<text x="{tx}" y="{ty}" fill="{c if big else MUTED}" font-size="11.5" '
                   f'text-anchor="{anchor}"{" font-weight=\"600\"" if big else ""}>{label}</text>')
    return (f'<svg viewBox="0 0 {W} 320" width="100%" '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,monospace" role="img" '
            f'aria-label="The mission cycle drawn as a loop of six phases: a flown final '
            f'approach with the hose paying out, pure pumping at the water, an outbound leg '
            f'that winds the hose up while climbing and lets down on arrival, the drop run '
            f'along the fire, the escape climb the drop itself powers, and a return that '
            f'makes nitrogen ballast while descending to hose range.">{"".join(out)}</svg>')


def fig_scale3():
    """Every vehicle and reference at ONE scale, one per row. 0.62 px/m."""
    S = 0.62
    rows = [
        # (kind, name, length_m, dia_m, note, colour)
        ("ship", "P-10000", 876, 219, "10,000 t of water · conceptual", WARM),
        ("bridge", "Lions Gate Bridge", 472, 111, "main span 472 m · Vancouver", FAINT),
        ("ship", "P-1000", 404, 102, "1,000 t of water · conceptual", WARM),
        ("airship", "LZ 129 Hindenburg", 245, 41, "the largest airship ever flown", FAINT),
        ("ship", "P-100", 190, 47, "100 t · the homepage ledger vehicle", WARM),
        ("jet", "Boeing 747-400", 71, 19, "70.7 m", MUTED),
        ("person", "a person", 1.8, 0, "1.1 px at this scale", BONE),
    ]
    out, y = [], 16
    for kind, name, length, dia, note, colour in rows:
        w = length * S
        h = max(dia * S, 2)
        label = f'{name} · {note}'
        _guard(16 + len(label) * 6.6, label, "scale3")
        out.append(f'<text x="16" y="{y + 10}" fill="{colour}" font-size="11.5" '
                   f'font-weight="600">{name}</text>'
                   f'<text x="{16 + len(name) * 7.2 + 8:.0f}" y="{y + 10}" fill="{FAINT}" '
                   f'font-size="10.5">{note}</text>')
        cy = y + 22 + h / 2
        if kind == "ship":
            out.append(f'<ellipse cx="{16 + w / 2:.1f}" cy="{cy:.1f}" rx="{w / 2:.1f}" '
                       f'ry="{h / 2:.1f}" fill="{WARM}" fill-opacity=".08" stroke="{WARM}" '
                       f'stroke-width="1.6"/>')
        elif kind == "airship":
            out.append(f'<ellipse cx="{16 + w / 2:.1f}" cy="{cy:.1f}" rx="{w / 2:.1f}" '
                       f'ry="{h / 2:.1f}" fill="{FAINT}" fill-opacity=".12" stroke="{FAINT}"/>'
                       f'<path d="M{16 + w - 14:.0f} {cy - h / 2 - 3:.0f} l14 5 v{h + 6:.0f} l-14 5 z" '
                       f'fill="{FAINT}" fill-opacity=".3"/>')
        elif kind == "bridge":
            t = 111 * S  # tower height above deck ~111 m
            x0, x1 = 16, 16 + w
            ydeck = y + 22 + t
            out.append(
                f'<line x1="{x0}" y1="{ydeck:.1f}" x2="{x1:.1f}" y2="{ydeck:.1f}" '
                f'stroke="{FAINT}" stroke-width="2"/>'
                f'<line x1="{x0 + 4}" y1="{ydeck:.1f}" x2="{x0 + 4}" y2="{y + 22:.1f}" stroke="{FAINT}" stroke-width="2"/>'
                f'<line x1="{x1 - 4:.1f}" y1="{ydeck:.1f}" x2="{x1 - 4:.1f}" y2="{y + 22:.1f}" stroke="{FAINT}" stroke-width="2"/>'
                f'<path d="M{x0} {ydeck:.0f} Q{16 + w / 2:.0f} {y + 26:.0f} {x1:.0f} {ydeck:.0f}" '
                f'fill="none" stroke="{FAINT}" stroke-opacity=".4"/>'
                f'<path d="M{x0 + 4} {y + 22:.0f} Q{16 + w / 2:.0f} {ydeck + 26:.0f} {x1 - 4:.0f} {y + 22:.0f}" '
                f'fill="none" stroke="{FAINT}" stroke-opacity=".7"/>')
            h = t
        elif kind == "jet":
            # simplified 747 silhouette matching the homepage vocabulary, at 0.62 px/m
            x0 = 16
            out.append(
                f'<path d="M{x0} {cy + 4:.0f} Q{x0 + 3} {cy - 2:.0f} {x0 + 10} {cy - 3:.0f} '
                f'L{x0 + 30} {cy - 3:.0f} L{x0 + 36} {cy - 14:.0f} L{x0 + 40} {cy - 14:.0f} '
                f'L{x0 + 39} {cy - 3:.0f} Q{x0 + 44} {cy - 1:.0f} {x0 + 41} {cy + 3:.0f} '
                f'L{x0 + 8} {cy + 5:.0f} Z" fill="{MUTED}" fill-opacity=".35" stroke="{MUTED}" '
                f'stroke-opacity=".8"/>'
                f'<path d="M{x0 + 16} {cy:.0f} L{x0 + 22} {cy:.0f} L{x0 + 34} {cy + 7:.0f} '
                f'L{x0 + 28} {cy + 7:.0f} Z" fill="{MUTED}" fill-opacity=".5"/>')
            h = 20
        elif kind == "person":
            out.append(f'<rect x="16" y="{y + 22:.0f}" width="1.5" height="2" fill="{BONE}"/>'
                       f'<text x="26" y="{y + 27:.0f}" fill="{FAINT}" font-size="10.5">'
                       f'← everything else on this figure is why the milestone is one small cell</text>')
            h = 6
        y += 22 + h + 18
    return (f'<svg viewBox="0 0 {W} {y:.0f}" width="100%" '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,monospace" role="img" '
            f'aria-label="All three conceptual airships and four references drawn to one scale, '
            f'one per row: the 876-metre P-10000, the 472-metre Lions Gate Bridge main span, the '
            f'404-metre P-1000, the 245-metre Hindenburg, the 190-metre P-100, a Boeing 747, and '
            f'a person, who is about one pixel.">{"".join(out)}</svg>')


def fig_cutaway():
    """Side cutaway of the P-class hull: a printed lattice of sealed voids with the machinery
    inside the load paths. Illustrative architecture, not a design."""
    cx, cy, rx, ry = 440, 175, 375, 92
    out = [
        f'<defs><clipPath id="hull"><ellipse cx="{cx}" cy="{cy}" rx="{rx - 6}" ry="{ry - 5}"/>'
        f'</clipPath></defs>',
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#0d0d10" stroke="{COOL}" '
        f'stroke-width="1.6"/>',
    ]
    # the lattice: offset rows of sealed voids, clipped to the hull
    lat = []
    yy = cy - ry + 12
    row = 0
    while yy < cy + ry - 8:
        x0 = 70 + (17 if row % 2 else 0)
        for xx in range(x0, 876, 34):
            lat.append(f'<circle cx="{xx}" cy="{yy:.0f}" r="10" fill="none" stroke="{FAINT}" '
                       f'stroke-opacity=".28"/>')
        yy += 26
        row += 1
    out.append(f'<g clip-path="url(#hull)">{"".join(lat)}</g>')
    # solar skin: the top arc
    out.append(f'<path d="M200 96 Q440 62 680 96" fill="none" stroke="{BONE}" stroke-width="3" '
               f'stroke-dasharray="10 5" stroke-opacity=".8"/>')
    # water tanks along the keel, symmetric about the centre of buoyancy
    for i, xx in enumerate((285, 345, 405, 475, 535, 595)):
        out.append(f'<rect x="{xx - 20}" y="228" width="40" height="15" rx="4" fill="{COOL}" '
                   f'fill-opacity=".55" stroke="{COOL}" stroke-opacity=".8"/>')
    # LN2 ballast tanks inboard
    for xx in (368, 512):
        out.append(f'<rect x="{xx - 16}" y="206" width="32" height="13" rx="6" fill="{BONE}" '
                   f'fill-opacity=".5" stroke="{BONE}" stroke-opacity=".8"/>')
    # machinery bay: generators, batteries, cryo plant
    out.append(f'<rect x="418" y="204" width="22" height="17" rx="2" fill="{FAINT}" fill-opacity=".6"/>')   # gensets
    out.append(f'<rect x="444" y="204" width="18" height="17" rx="2" fill="{GREEN}" fill-opacity=".45"/>')  # batteries
    out.append(f'<rect x="466" y="204" width="18" height="17" rx="2" fill="{COOL_DIM}" fill-opacity=".9"/>')  # cryo
    # vehicle Mind + deterministic kernel, physically separate boxes
    out.append(f'<rect x="180" y="168" width="16" height="12" rx="2" fill="none" stroke="{WARM}"/>')
    out.append(f'<rect x="202" y="168" width="12" height="12" rx="2" fill="none" stroke="{WARM}" '
               f'stroke-width="2.2"/>')
    # hose reel, hose, pump pod — the only thing that touches water
    out.append(f'<circle cx="440" cy="252" r="7" fill="none" stroke="{COOL}" stroke-width="1.6"/>')
    out.append(f'<line x1="440" y1="267" x2="440" y2="330" stroke="{COOL}" stroke-dasharray="4 4"/>')
    out.append(f'<rect x="431" y="330" width="18" height="10" rx="5" fill="{COOL}" fill-opacity=".6" '
               f'stroke="{COOL}"/>')
    out.append(f'<path d="M410 352 q15 6 30 0 t30 0" fill="none" stroke="{COOL}" stroke-opacity=".5"/>')
    # main vectorable rotors on pylons; small distributed fans along the hull
    for xx in (215, 665):
        out.append(f'<line x1="{xx}" y1="{cy + ry - 10}" x2="{xx}" y2="{cy + ry + 12}" '
                   f'stroke="{WARM}" stroke-opacity=".8"/>'
                   f'<ellipse cx="{xx}" cy="{cy + ry + 16}" rx="30" ry="5" fill="none" '
                   f'stroke="{WARM}" stroke-width="1.6"/>')
    for xx, yy in ((160, 116), (300, 92), (580, 92), (720, 116), (160, 234), (720, 234)):
        out.append(f'<circle cx="{xx}" cy="{yy}" r="3" fill="{WARM}" fill-opacity=".7"/>')
    # tail surfaces
    out.append(f'<path d="M796 148 L850 120 L842 160 Z" fill="{FAINT}" fill-opacity=".35"/>')
    out.append(f'<path d="M796 202 L850 230 L842 190 Z" fill="{FAINT}" fill-opacity=".35"/>')
    # callouts. (x, y, anchor, text, leader end)
    calls = [
        (16, 26, "start", "solar skin — hotel loads, slow charging, safe-drift recovery", (250, 88)),
        (864, 26, "end", "printed lattice of sealed vacuum voids — damage stays local", (620, 120)),
        (440, 54, "middle", "generators · batteries · cryo plant on one electrical bus", (450, 202)),
        (16, 330, "start", "vectorable rotors — downforce, gusts, fine positioning", (215, 262)),
        (16, 375, "start", "pump pod on a long hose — the only part that touches water", (428, 336)),
        (864, 330, "end", "water tanks distributed about the centre of buoyancy", (600, 236)),
        (864, 375, "end", "LN₂ ballast — mass, cold reservoir, partially recoverable battery", (528, 213)),
        (150, 148, "end", "Mind — proposes", (196, 172)),
        (150, 200, "end", "kernel — decides", (208, 182)),
    ]
    for tx, ty, anchor, text, (lx, ly) in calls:
        est = len(text) * 6.2
        x_end = tx + (est if anchor == "start" else est / 2 if anchor == "middle" else 0)
        _guard(x_end, text, "cutaway")
        sx = tx if anchor == "start" else tx - est if anchor == "end" else tx
        ax = tx if anchor != "start" else min(tx + est, tx + est)
        # leader from the text's near edge to the feature
        lead_x = tx if anchor == "end" else (tx + est if anchor == "start" else tx)
        out.append(f'<line x1="{lead_x:.0f}" y1="{ty - 4}" x2="{lx}" y2="{ly}" stroke="#33333c"/>')
        out.append(f'<text x="{tx}" y="{ty}" fill="{MUTED}" font-size="10.5" '
                   f'text-anchor="{anchor}">{text}</text>')
    return (f'<svg viewBox="0 0 {W} 400" width="100%" '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,monospace" role="img" '
            f'aria-label="Cutaway of the conceptual hull: a lattice of many sealed vacuum voids '
            f'fills the volume; water and nitrogen tanks, generators, batteries and the cryogenic '
            f'plant sit inside the load paths near the centre of buoyancy; a pump pod hangs on a '
            f'long hose below; vectorable rotors and small distributed fans provide force; solar '
            f'skin covers the top; the Mind and the deterministic safety kernel are separate '
            f'boxes.">{"".join(out)}</svg>')


def fig_ladder():
    """Five layers between an idea and an actuator — the fleet version of the homepage
    control split. Wording aligned with the animal-partnership ladder deliberately."""
    rows = [
        ("humans", "objectives · stop authority", BONE,
         ["SET what the fleet may want, where it may fly, what water it may touch —",
          "and can stop everything. No one silently edits the record."]),
        ("the strategic Mind", "generative · fleet-wide", COOL,
         ["may PROPOSE allocation: which incidents, which vehicles, what matters most.",
          "Must explain major decisions and escalate uncertainty to humans."]),
        ("regional fleet Minds", "coordination", COOL,
         ["may PLAN: airspace deconfliction, shared water sources, tanker and",
          "maintenance rendezvous, reassignment after failures."]),
        ("each vehicle Mind", "generative · aboard", COOL,
         ["may REQUEST manoeuvres as typed proposals carrying purpose, urgency,",
          "confidence and margins. It never addresses an actuator directly."]),
        ("the safety kernel", "deterministic · verified", WARM,
         ["DECIDES what is permitted: flight and structural envelope, terrain and",
          "water clearance, convection exclusion, comms-loss behaviour, release rules."]),
        ("actuators", "bounded local controllers", FAINT,
         ["EXECUTE bounded commands, and fail safe."]),
    ]
    ROW, GAP, PAD_L = 30, 12, 232
    out = []
    for i, (who, kind, colour, lines) in enumerate(rows):
        y = i * (ROW + GAP)
        if PAD_L - 14 - len(kind) * 5.8 < 0:
            raise SystemExit(f"ladder: kind label overflows left edge: {kind!r}")
        out.append(
            f'<text x="{PAD_L - 14}" y="{y + 13}" fill="{colour}" font-size="13" text-anchor="end" '
            f'font-weight="600">{who}</text>'
            f'<text x="{PAD_L - 14}" y="{y + 27}" fill="{FAINT}" font-size="10.5" '
            f'text-anchor="end">{kind}</text>'
            f'<rect x="{PAD_L}" y="{y}" width="4" height="{ROW}" fill="{colour}"/>')
        for j, line in enumerate(lines):
            _guard(PAD_L + 14 + len(line) * 6.2, line, "ladder")
            out.append(f'<text x="{PAD_L + 14}" y="{y + 12 + j * 14}" fill="{MUTED}" '
                       f'font-size="12">{line}</text>')
    h = len(rows) * (ROW + GAP) - GAP + 4
    return (f'<svg viewBox="0 0 {W} {h}" width="100%" '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'font-family="ui-monospace,SFMono-Regular,Menlo,monospace" role="img" '
            f'aria-label="Five layers between an idea and an actuator: humans set objectives and '
            f'hold stop authority; a strategic Mind proposes fleet allocation; regional Minds '
            f'plan and deconflict; each vehicle Mind requests manoeuvres as typed proposals; a '
            f'deterministic verified safety kernel decides what is permitted; bounded actuator '
            f'controllers execute and fail safe.">{"".join(out)}</svg>')


FIGS = {"CYCLE": fig_cycle, "SCALE3": fig_scale3, "CUTAWAY": fig_cutaway, "LADDER": fig_ladder}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--print", dest="dump", action="store_true")
    a = ap.parse_args()
    if a.dump:
        for k, fn in FIGS.items():
            print(f"{k}: {len(fn())} bytes")
        return
    page = ROOT / "concept" / "index.html"
    doc = page.read_text()
    done = 0
    for name, fn in FIGS.items():
        lo, hi = f"<!--{name}-->", f"<!--/{name}-->"
        if lo not in doc:
            print(f"  {name}: no marker on the page — skipped")
            continue
        i, j = doc.index(lo) + len(lo), doc.index(hi)
        doc = doc[:i] + fn() + doc[j:]
        done += 1
    page.write_text(doc)
    print(f"  -> inlined {done} figures")


if __name__ == "__main__":
    main()
