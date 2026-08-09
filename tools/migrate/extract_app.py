#!/usr/bin/env python3
"""Move the monitor application out of index.html into app/*.js, byte for byte.

Same machinery as extract_sim.py, three differences:

  * app modules import from `sim/` as well as from each other, so the reference scan
    resolves against the model's public surface too;
  * the region ends in three top-level statements (the visibility handler, the console
    surface, the boot call) which belong to `main.js`;
  * two functions write to `let` bindings that live in another module, which an ES module
    cannot do. Those two writes go through exported setters, added by patch_app.py.

After this the page is markup and one import.
"""
from __future__ import annotations

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from slice import DECL, classify, strip_comments_and_strings                                       # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGE = ROOT / 'index.html'

# Which symbol lives in which file. Grouped so that everything which mutates a piece of
# state sits with that state: the alternative is a web of setters that documents nothing.
MODULES = {
    'dom':            ['$', 'esc', 'kvRows', 'barRows', 'cycleBar', 'SHORT'],
    'store':          ['S'],
    'net':            ['FIRES_URL', 'PERIMS_URL', 'fetchJSON', 'cachedJSON', 'mirrorJSON'],
    'feeds':          ['REPLAY', 'normalize', 'loadLive', 'needsShip', 'fetchWind',
                       'fetchHeat', 'applyHeat'],
    'fleet':          ['FLEET', 'rebuildMissions', 'replanAll'],
    'map/projection': ['mercY', 'canvas', 'W', 'resize', 'px', 'latOfY'],
    'map/basemap':    ['TERRAIN', 'terrainImg', 'terrainReady', 'tileCache',
                       'drawSatLevel', 'drawSat'],
    'map/heat':       ['heatSprite', 'heatLayer', 'renderHeatLayer'],
    'map/render':     ['COL', 'statusColor', 'fireVisible', 'hitShips', 'draw',
                       'updateScalebar'],
    'map/interact':   ['drag', 'endPointer', 'clickAt', 'select', 'focusMission',
                       'fitFleet', 'fitFires'],
    'cockpit/gauges': ['SVGNS', 'svgEl', 'polar', 'makeGauge', 'makeDualGauge',
                       'makePhaseDial'],
    'cockpit/shipviz': ['shipViz'],
    'cockpit/panels': ['phaseDialObj', 'gGen', 'forceAcc', 'cockpitShip', 'renderDrawer',
                       'updateCockpit', 'updateCockpitText', 'timeSinceDrop'],
    'cockpit/tables': ['renderFires', 'updateFires', 'renderRoster', 'updateRoster',
                       'renderStats', 'renderTable'],
    'bridge/viz3d':   ['m3d', 'm3dCamMode', 'm3dAz', 'm3dSideSign', 'M3D_AUTO',
                       'M3D_SYS_CAM', 'm3dFading', 'm3dFadeTo', 'M3D_SYS', 'ensureM3D',
                       'm3dWindKey', 'updateM3D', 'sizeAvatar', 'm3dBreakSync', 'updSyncUI'],
    'worked':         ['DIALS', 'renderAsm', 'renderWorked', 'renderClassCards'],
    'loop':           ['frame'],
    'main':           ['wire', 'renderStatus', 'boot'],
}

HEADERS = {
    'dom': 'The three DOM conveniences the whole application uses, and nothing else.',
    'store': 'S — the application\'s state, in one object.\n *\n * Everything mutable that is not owned by a single module lives here, so that "what is\n * the page currently showing" has one answer you can print.',
    'net': 'Fetching, with a cache and a timeout. Knows about HTTP; knows nothing about fires.',
    'feeds': 'The live data: what we ask for, how we fall back, and how it becomes model input.\n *\n * Three tiers, in order: our own mirror of the public feeds, then the public feeds\n * directly, then the dated snapshot committed to this repository. The mirror exists so\n * that traffic to this page does not become traffic to an emergency service.',
    'fleet': 'Allocating sixteen hulls to the fires that most need them.',
    'map/projection': 'Web Mercator, the canvas, and the one function that turns a coordinate into a pixel.',
    'map/basemap': 'The terrain image and the satellite tiles underneath everything else.',
    'map/heat': 'The satellite heat overlay, drawn once into an offscreen canvas and composited.',
    'map/render': 'Drawing the map: the layer order, and every layer.',
    'map/interact': 'Pointer, wheel and keyboard on the map; selection; framing.',
    'cockpit/gauges': 'The SVG instruments: round gauges, the dual generation/consumption dial, the phase dial.',
    'cockpit/shipviz': 'The 2D schematic avatar — the same state as the 3D model, drawn as a wire diagram.\n *\n * It exists because a wireframe with labelled force arrows says things a rendered\n * vehicle cannot: which way the rotors are pushing, and how hard.',
    'cockpit/panels': 'The focused ship: forces, instruments, the power ledger and the mission trace.',
    'cockpit/tables': 'The fleet roster and the top-fires list.',
    'bridge/viz3d': 'The bridge to the 3D model: mounting it, feeding it state, and the synced camera.\n *\n * The 3D library knows nothing about this page. Everything page-specific — which view\n * suits which phase, how the camera follows a heading, how the model is framed — is here.',
    'worked': 'The worked example and the class cards. Shared with the how-it-works page.',
    'loop': 'The frame loop: advance the clock, integrate the energy ledger, redraw.',
    'main': 'Wiring the controls, reporting status, and starting the application.',
}



def declared_names(block: str) -> list[str]:
    """Every name a declaration introduces, including `let a = 1, b = 2;` forms.

    The import scan resolves references by name, so a companion declarator that is never
    seen here becomes a silently missing import — the module loads and then throws on the
    first use. Walk the declaration at depth zero and collect each declarator.
    """
    import re as _re
    m = _re.match(r'^(?:export\s+)?(?:async\s+)?(function|const|let|var|class)\s+', block)
    if not m:
        return []
    kw = m.group(1)
    if kw in ('function', 'class'):
        return [_re.match(r'^(?:export\s+)?(?:async\s+)?(?:function|class)\s+([A-Za-z_$][\w$]*)',
                          block).group(1)]
    names, depth, i, n = [], 0, m.end(), len(block)
    expect = True
    while i < n:
        c = block[i]
        if c in '"\'`':
            q = c
            i += 1
            while i < n and block[i] != q:
                i += 2 if block[i] == '\\' else 1
        elif c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif depth == 0 and c == ';':
            break
        elif depth == 0 and c == ',':
            expect = True
        elif expect and (c.isalpha() or c in '_$'):
            j = i
            while j < n and (block[j].isalnum() or block[j] in '_$'):
                j += 1
            names.append(block[i:j])
            expect = False
            i = j
            continue
        i += 1
    return names

def main():
    lines = PAGE.read_text().split('\n')
    a = next(i for i, l in enumerate(lines) if l.startswith('import * as SIM'))
    a = next(i for i in range(a, len(lines)) if lines[i].strip() == '}')
    b = max(i for i, l in enumerate(lines) if l.strip() == '</script>')

    kind = classify(lines)
    hits = [(m.group(1), i) for i in range(a + 1, b)
            if kind[i] == 'code' and (m := DECL.match(lines[i]))]

    # a declaration owns the comment block above it, exactly as in the model extraction
    starts = []
    for _, i in hits:
        s = i
        while s - 1 > a:
            k = kind[s - 1]
            if k in ('blank', 'line-comment'):
                s -= 1
            elif isinstance(k, tuple):
                s = k[1]
            else:
                break
        while s < i and kind[s] == 'blank':
            s += 1
        starts.append(s)

    # the block after the last declaration is main.js's trailing statements
    last_name, last_i = hits[-1]
    depth, opened, last_end = 0, False, last_i
    for i in range(last_i, b):
        depth += lines[i].count('{') - lines[i].count('}')
        if '{' in lines[i]:
            opened = True
        if opened and depth <= 0:
            last_end = i + 1
            break
    trailing = [lines[i] for i in range(last_end, b) if lines[i].strip()
                and 'window.AIRSHIPS' not in lines[i]]

    blocks = {}
    for k, (name, i) in enumerate(hits):
        end = starts[k + 1] if k + 1 < len(hits) else last_end
        while end - 1 > i and not lines[end - 1].strip():
            end -= 1
        block = lines[starts[k]:end]
        block[i - starts[k]] = 'export ' + block[i - starts[k]]
        blocks[name] = '\n'.join(block).rstrip()

    placed = {}
    for mod, names in MODULES.items():
        for n in names:
            # parse the DECLARATION LINE, not the whole block: the block begins with the
            # comment that documents it, which no declaration regex will match
            decl_line = next((l for l in blocks[n].split('\n') if l.startswith('export ')), '')
            for alias in declared_names(decl_line) or [n]:
                placed[alias] = mod
    missing = sorted(set(blocks) - set(placed))
    unknown = []
    if missing or unknown:
        sys.exit(f"MAPPING ERROR  unplaced={missing}  unknown={unknown}")

    # The model's public surface, so app modules import what they use from sim/.
    # Parse only what is inside `export { ... } from '...'` braces: taking every token on
    # the line also picks up the module path, and then subtracting module names to undo
    # that quietly deletes real exports whose name matches their file (narrate, assign,
    # plan, state, selftest — five of the most-used functions in the model).
    sim_index = (ROOT / 'sim' / 'index.js').read_text()
    sim_names = set()
    for block in re.findall(r'export\s*\{([^}]*)\}\s*from', sim_index):
        sim_names.update(re.findall(r'[A-Za-z_$][\w$]*', block))

    strip = re.compile(r'//[^\n]*|/\*.*?\*/', re.S)
    for mod, names in MODULES.items():
        body = '\n\n'.join(blocks[n] for n in names)
        if mod == 'main':
            body += '\n\n' + '\n'.join(trailing)
        scan = strip_comments_and_strings(body).replace('...', ' ')

        local, from_sim = {}, set()
        for name, own in placed.items():
            if own != mod and re.search(r'(?<![.\w$])' + re.escape(name) + r'(?![\w$])', scan):
                local.setdefault(own, []).append(name)
        for name in sim_names:
            if re.search(r'(?<![.\w$])' + re.escape(name) + r'(?![\w$])', scan):
                from_sim.add(name)

        depth_up = '../' * mod.count('/')
        imports = ''
        if from_sim:
            imports += (f"import {{ {', '.join(sorted(from_sim))} }} "
                        f"from '{depth_up}../sim/index.js';\n")
        for other in sorted(local):
            rel = relative(mod, other)
            imports += f"import {{ {', '.join(sorted(local[other]))} }} from '{rel}';\n"

        path = ROOT / 'app' / f'{mod}.js'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"/* {HEADERS[mod]}\n */\n" + (imports + '\n' if imports else '')
                        + body + '\n')
        print(f"  app/{mod}.js  {len(body.splitlines()):4d} lines  "
              f"sim: {len(from_sim):2d}  local: {', '.join(sorted(local)) or 'none'}")


def relative(frm: str, to: str) -> str:
    """A module specifier from one app module to another, both given as posix-ish keys."""
    up = '../' * frm.count('/')
    return f"./{to}.js" if '/' not in frm and '/' not in to else f"{up or './'}{to}.js"


if __name__ == '__main__':
    main()
