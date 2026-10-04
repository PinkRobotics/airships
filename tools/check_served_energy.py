#!/usr/bin/env python3
"""Refuse stale controls or a served quantity without an exact-input feasible plan."""
import json,os,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
manifest=json.loads((ROOT/'tools/served_energy_surfaces.json').read_text())
owned=set(manifest['cycleConsumers'])
pattern=re.compile(r'\b(?:plan|p|record|fav|favourable|m\.plan|mm\.plan)\.(?:cycleMin|tph|eCycleMWh|kwhPerTonne|deliveredT|retainedT|dropsPerHour)\b')
paths=[*(ROOT/'app').rglob('*.js'),ROOT/'concept/index.html',ROOT/'sim/state.js',ROOT/'sim/narrate.js',ROOT/'sim/energy-view.js',ROOT/'sim/served-view.js',ROOT/'tools/fallback_dump.js']
for path in paths:
 text=path.read_text();rel=path.relative_to(ROOT).as_posix()
 if pattern.search(text) and rel not in owned:raise SystemExit('FAIL uninventoried cycle consumer: '+rel)
 if rel.startswith('app/') and re.search(r'\bplanCycle\s*\(',re.sub(r'/\*.*?\*/|//[^\n]*','',text,flags=re.S)):
  raise SystemExit('FAIL page bypasses feasible selector: '+rel)
print('PASS served cycle consumer inventory: '+str(len(owned))+' owned consumers')
node_args=['--mutation',sys.argv[sys.argv.index('--mutation')+1]] if '--mutation' in sys.argv else []
COMMANDS=[['node','tools/gen_served_candidates.mjs','--check'],['node','tests/node/served-energy.mjs',*node_args]]
# The producer owns the exact served sentence regions and the separately measured check count.
COMMANDS[1:1]=[['node','tools/gen_energy_page_checks.mjs','--check'],['node','tools/gen_energy_pages.mjs','--check']]
COMMANDS.append([sys.executable,'tools/gen_fallback.py','--check'])
COMMANDS.append([sys.executable,'tools/served_energy_browser.py',*sys.argv[1:]])
for command in COMMANDS:
 p=subprocess.run(command,cwd=ROOT)
 if p.returncode:sys.exit(p.returncode)
print('PASS served energy gate: generated inputs and sentences, exact route/basis/mode, inactive missions and rendered quantities')
