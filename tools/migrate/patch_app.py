#!/usr/bin/env python3
"""The hand-written seams of the application extraction.

Two pieces of state were written from wherever happened to need them, which a single
file permits and separate modules do not. Both become a named operation on the module
that owns the state:

  * the 3D camera. `m3dCamMode` and `m3dAz` were assigned from the control wiring and
    from the drawer. They are now `setCamera(...)`, which also says what the assignment
    was FOR — "hold this preset", "resync", "the user took the wheel".

  * the tunables. The page's reset button rebuilt `CFG` wholesale; the model exports
    `resetConfig()` for exactly that.

Everything else moved unchanged.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
APP = ROOT / 'app'

CAMERA_API = '''
/**
 * Change the camera's mode, and optionally its azimuth, from outside this module.
 *
 * The mode is not a preference, it is a statement about who is steering:
 *
 *   "sync"        the camera follows the ship's heading, and owns the framing
 *   "syncManual"  heading still followed, but the viewer set the distance themselves
 *   "preset"      a named viewpoint, held until the viewer resyncs
 *   "presetHold"  the same, pinned to a subsystem the viewer is inspecting
 *   "free"        the viewer is dragging
 *
 * Passing `azimuth: null` re-seeds the follow angle, so the next frame snaps to the
 * ship's current heading instead of sweeping to it from wherever the camera was left.
 */
export function setCamera({ mode, azimuth, viewMode, phase, panel } = {}) {
  if (mode !== undefined) m3dCamMode = mode;
  if (azimuth !== undefined) m3dAz = azimuth;
  if (viewMode !== undefined) m3dVm = viewMode;
  if (phase !== undefined) m3dPhase = phase;
  if (panel !== undefined) m3dMode = panel;
}

/** What the camera is doing, for the controls that light up to match it. */
export function cameraMode() {
  return m3dCamMode;
}

/** Which button in the systems row is active ("shell", "auto", "water", "custom", …). */
export function panelMode() {
  return m3dMode;
}
'''


def patch(rel, pairs, *, must=True):
    p = APP / rel
    s = p.read_text()
    for old, new in pairs:
        if s.count(old) == 0:
            if must:
                sys.exit(f"patch_app: {rel}: not found: {old[:70]!r}")
            continue
        s = s.replace(old, new)
    p.write_text(s)


def main():
    # ── the owner gains an API ────────────────────────────────────────────────────────
    viz = APP / 'bridge' / 'viz3d.js'
    s = viz.read_text()
    anchor = 'export function m3dBreakSync() {'
    assert s.count(anchor) == 1, 'viz3d: m3dBreakSync not found'
    viz.write_text(s.replace(anchor, CAMERA_API.strip() + '\n\n' + anchor))

    # ── the drawer resyncs the follow angle when the focused ship changes ─────────────
    patch('cockpit/panels.js', [
        ('      m3dAz = null;', '      setCamera({ azimuth: null });'),
    ])
    p = APP / 'cockpit' / 'panels.js'
    s = p.read_text()
    s = re.sub(r"^(import \{[^}]*?)\} from '\.\./bridge/viz3d\.js';",
               lambda m: m.group(1).rstrip() + ', setCamera } from \'../bridge/viz3d.js\';',
               s, count=1, flags=re.M | re.S)
    p.write_text(s)

    # ── the controls say what each of their camera changes means ─────────────────────
    patch('main.js', [
        ('if (k === "auto") { m3dPhase = ""; m3dVm = ""; m3dCamMode = "sync"; m3dAz = null; }',
         'if (k === "auto") setCamera({ phase: "", viewMode: "", mode: "sync", azimuth: null });'),
        ('      m3dVm = "exterior"; m3dCamMode = "sync"; m3dAz = null;',
         '      setCamera({ viewMode: "exterior", mode: "sync", azimuth: null });'),
        ('      m3dCamMode = "presetHold";                     // hold this subject until resynced',
         '      setCamera({ mode: "presetHold" });              // hold this subject until resynced'),
        ('      m3dCamMode = "presetHold";', '      setCamera({ mode: "presetHold" });'),
        ('    if (b.dataset.m3c === "sync") { m3dCamMode = "sync"; m3dAz = null; }',
         '    if (b.dataset.m3c === "sync") setCamera({ mode: "sync", azimuth: null });'),
        ('      m3dCamMode = "preset";', '      setCamera({ mode: "preset" });'),
        ('    if (m3dCamMode === "sync") { m3dCamMode = "syncManual"; updSyncUI(); }',
         '    if (cameraMode() === "sync") { setCamera({ mode: "syncManual" }); updSyncUI(); }'),
        # the tunables belong to the model
        ('    CFG = Object.assign({}, DEFAULTS);', '    resetConfig();'),
        # the systems row and the custom panel also change bridge state
        ('    m3dMode = k;', '    setCamera({ panel: k });'),
        ('      m3dVm = "vacuum";', '      setCamera({ viewMode: "vacuum" });'),
        ('      m3dVm = "systems";', '      setCamera({ viewMode: "systems" });'),
        ('    m3dVm = $("m3cView").value;', '    setCamera({ viewMode: $("m3cView").value });'),
        ('if (m3dMode === "custom")', 'if (panelMode() === "custom")'),
    ])
    p = APP / 'main.js'
    s = p.read_text()
    s = re.sub(r"^(import \{[^}]*?)\} from '\./bridge/viz3d\.js';",
               lambda m: m.group(1).rstrip() + ', setCamera, cameraMode } from \'./bridge/viz3d.js\';',
               s, count=1, flags=re.M | re.S)
    s = re.sub(r"^(import \{[^}]*?)\} from '\.\./sim/index\.js';",
               lambda m: m.group(1).rstrip() + ', resetConfig } from \'../sim/index.js\';',
               s, count=1, flags=re.M | re.S)
    p.write_text(s)

    # ── the vehicle model moved from a sibling directory into this repository ────────
    # Both specifiers are resolved against THIS MODULE rather than against the page.
    # `import` already works that way; `fetch` does not, and a page-relative version.json
    # silently 404s, which leaves the viewer unpinned and — as it did here — unmounted.
    patch('bridge/viz3d.js', [
        ('await fetch("../airship3d/version.json?ts=" + Date.now(), { cache: "reload" })',
         'await fetch(new URL("../../3d/version.json?ts=" + Date.now(), import.meta.url),\n'
         '                                  { cache: "reload" })'),
        ('await import("../airship3d/airship3d.js?v=" + (m3dVer || "unpinned"))',
         'await import(new URL("../../3d/index.js?v=" + (m3dVer || "unpinned"),\n'
         '                                   import.meta.url).href)'),
    ])

    # ── the page reads the URL; the model is told ────────────────────────────────────
    # This lived in the page's inline script and would otherwise be dropped with it,
    # leaving the seed random and every golden comparison meaningless.
    s = (APP / 'main.js').read_text()
    anchor = 'export async function boot('
    assert s.count(anchor) == 1, 'main.js: boot not found'
    s = s.replace(anchor, """/* Deterministic replay. `?seed=N` pins every choice the model makes, and `?data=snapshot`
 * (read in feeds.js) pins its inputs. The URL is parsed here, in the application, so that
 * nothing in sim/ needs to know a browser exists.
 *
 * Together they make a run reproducible: the same link shows another person exactly what
 * you were looking at, and the golden-output tests have something stable to compare. */
{
  const seed = new URLSearchParams(location.search).get('seed');
  if (seed) setSeed(seed);
}

""" + anchor)
    (APP / 'main.js').write_text(s)
    s = (APP / 'main.js').read_text()
    s = re.sub(r"^(import \{[^}]*?)\} from '\.\./sim/index\.js';",
               lambda m: m.group(1).rstrip() + ', setSeed } from \'../sim/index.js\';',
               s, count=1, flags=re.M | re.S)
    (APP / 'main.js').write_text(s)

    # ── the console surface lives with the boot call ─────────────────────────────────
    s = (APP / 'main.js').read_text()
    boot = '\nboot();'
    assert s.count(boot) == 1, 'main.js: boot() not found'
    s = s.replace(boot, '''
/* Published deliberately. `APP` because the markup binds to it; `AIRSHIPS` so that anyone
 * reading the page can re-run the model in their own devtools console without cloning
 * anything — `AIRSHIPS.sim.selftest()` runs every assertion, and
 * `AIRSHIPS.sim.planCycle(AIRSHIPS.sim.CLASSES.P100, AIRSHIPS.sim.MODES.balanced, 15)`
 * recomputes a published figure from scratch. Arithmetic nobody can re-run is just a
 * claim. */
window.AIRSHIPS = { sim: SIM, app: S, stateAt };

boot();''')
    s = s.replace("import { ", "import * as SIM from '../sim/index.js';\nimport { ", 1)
    (APP / 'main.js').write_text(s)

    print("  app seams patched: setCamera/cameraMode, resetConfig, console surface")


if __name__ == '__main__':
    main()
