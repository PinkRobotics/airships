#!/usr/bin/env python3
"""Regeneration and fail-closed prose binding for the float ledger.

--inventory prints every detected block and its interpretation as JSON.
--report prints the failing-sentence table for the hand-up. Neither mode writes files.

This is a lexical inventory, not a natural-language proof. It scans tables, paragraphs,
HTML display blocks, dynamic bindings and Python display strings/comments. New hits do
not pass by matching an unrelated number. A prose block can bind explicitly with:
  <!-- float-ledger: CASE_ID ; field=at.seaLevel.liftToMass ; value=0.558 -->
The stated value must occur in the visible text, match that exact field at its printed
precision, and have an altitude in the sentence/table/block, plus factors or a ledger
link. A ledger link does NOT replace an explicit altitude for a float ratio.

The three pages under float/ are not inventoried, exactly as the generated
docs/FLOAT-LEDGER.md is not: `make floatpagecheck` holds each to a fresh render of its
document, whose review it inherits.
"""
from __future__ import annotations
import argparse
import ast
import html
from html.parser import HTMLParser
import json
import pathlib
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode=True
ROOT=pathlib.Path(__file__).resolve().parent.parent
LEDGER=ROOT/'research/analysis/float-ledger.json'
CUE=re.compile(r'\b(?:float(?:s|ing)?|buoyan\w*|lift[ -](?:to|÷)[ -]mass|mass[ -](?:to|÷)[ -]lift|'
               r'crush floor|sink ceiling|displaced air|neutral buoyancy|scale is the lever|'
               r'two.thousand.tonne|few tonnes)\b',re.I)
DENSITY=re.compile(r'\b\d[\d,.]*\s*(?:kg\s*/\s*m[³3²2]|g\s*/\s*m[²2])',re.I)
MASS=re.compile(r'\b\d[\d,.]*\s*(?:t\b|tonnes?\b|kg\b|g\b)')
RATIO=re.compile(r'\bratio\b|lift\s*[÷/]\s*mass|mass\s*[÷/]\s*lift|\d[\d,.]*\s*[×x]\s*(?:over|the wall|too heavy)',re.I)
NUM=re.compile(r'(?<![\w])[-−+]?\d[\d,]*(?:\.\d+)?(?:\s*[×%])?')
ALT=re.compile(r'sea[ -]level|\b[\d,]+\s*m\s*(?:MSL|altitude)|(?:at|altitude|air at)\s*[\d,]+\s*m\b|working altitude|target altitude',re.I)
FACTORS=re.compile(r'\bSF\b|safety factor',re.I)
KD=re.compile(r'knockdown|γ|gamma|harsh|frame.practice|literature|assumed',re.I)
LINK=re.compile(r'FLOAT-LEDGER\.md|float-ledger\.json')
BIND=re.compile(r'float-ledger:\s*([^;]+);\s*field=([^;]+);\s*value=([-+\d.]+)')
# These are archival classes, not exemptions for live claims. Each hit remains inventoried.
ALLOWLIST=[
    (re.compile(r'^docs/working/\d{2}-\d{2}-\d{2}[^/]*\.md$'),
     'Dated working record; retained as the record of a claim, not endorsed as a current float result.'),
    (re.compile(r'^docs/audit/\d{2}-\d{2}-\d{2}[^/]*\.md$'),
     'Dated audit with current-status header; historical figures remain to explain the corrections.'),
]
# Dynamic figures whose exact routes are checked by executing the catalog, not guessed
# from the label. The field is a ledger row ID plus an exact pointer.
LIVE={
 'ship.ratio':('hull-52m/as-drawn/gamma-0.30/chord-1050/sf-1.2','at.seaLevel.liftToMass','ratio'),
 'ship.bestWorldRatio':('hull-52m/as-drawn/gamma-0.65/chord-1450/sf-1.2','at.seaLevel.liftToMass','bestWorldRatio'),
 'ship.massT':('hull-52m/as-drawn/gamma-0.30/chord-1050/sf-1.2','mass','massT'),
 'ship.liftT':('hull-52m/as-drawn/gamma-0.30/chord-1050/sf-1.2','at.seaLevel.lift','liftT'),
}


def dig(d,p):
    for k in p.split('.'):
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d


def clean(text):
    text=html.unescape(re.sub(r'<[^>]*>',' ',text))
    return re.sub(r'\s+',' ',text).strip()


class Blocks(HTMLParser):
    """Keep display blocks and their containing section's basis, with original line numbers."""
    def __init__(self):
        super().__init__(convert_charrefs=True);self.stack=[];self.out=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.skip+=1
        if self.skip:return
        if tag in ('section','table','p','li','tr','h1','h2','h3','div','span','text','figcaption'):
            self.stack.append({'tag':tag,'line':self.getpos()[0],'pieces':[],'attrs':dict(attrs)})
        token=' '.join(f'{k}="{v}"' for k,v in attrs)
        if tag=='a' and 'href' in dict(attrs):
            # Keep the destination for record checks; clean() removes this markup
            # from the visible text and therefore from its review key.
            link='<a href="'+html.escape(dict(attrs)['href'],quote=True)+'">'
            for frame in self.stack:frame['pieces'].append(link)
        if 'data-n' in dict(attrs) or 'data-cat' in dict(attrs):
            for frame in self.stack:frame['pieces'].append('['+token+']')
    def handle_data(self,data):
        if self.skip:return
        for frame in self.stack:frame['pieces'].append(data)
    def handle_comment(self,data):
        if self.skip:return
        for frame in self.stack:frame['pieces'].append('<!--'+data+'-->')
    def handle_endtag(self,tag):
        if tag in ('script','style'):
            self.skip=max(0,self.skip-1);return
        if self.skip:return
        idx=next((i for i in range(len(self.stack)-1,-1,-1) if self.stack[i]['tag']==tag),None)
        if idx is None:return
        frame=self.stack[idx];del self.stack[idx:]
        raw=' '.join(frame['pieces']);text=clean(raw)
        classes=set(frame['attrs'].get('class','').split())
        semantic=tag in ('p','li','tr','h1','h2','h3','text','figcaption') or (tag=='span' and 'fact' in classes) or \
                 (tag=='div' and bool(classes & {'metrics','keynum','big','eq'}))
        if semantic and interesting(text):
            self.out.append((frame['line'],self.getpos()[0],text,raw,tag))


def interesting(text):
    text=re.sub(r'(?:centre|center) of buoyancy|floating controls', '',text,flags=re.I)
    return bool(DENSITY.search(text) or CUE.search(text) or (RATIO.search(text) and NUM.search(text)) or
                (MASS.search(text) and re.search(r"mass|weigh|deficit|short",text,re.I)) or
                re.search(r'data-(?:n|cat)="(?:ship\.(?:ratio|bestWorldRatio|massT|liftT)|walls\.|stock\.(?:totalKg|massOver)|demo\.displacedAirKg|weigh\.)',text) or
                re.search(r'data-(?:n|cat)="[^" ]*(?:ratio|residual|totalKg|kgPerM3|filmGM2|arealGM2|displacedAir|nodesKg|tubeKg|pipeKg)',text,re.I))


def source_blocks(path):
    body=path.read_text(encoding='utf-8');rel=path.relative_to(ROOT).as_posix()
    if path.suffix=='.html':
        parser=Blocks();parser.feed(body)
        for ln,end,text,raw,tag in sorted(parser.out):
            # Prefer the enclosing semantic block at the SAME source location. Never
            # deduplicate identical claims at different locations.
            if any(other[0]<=ln and other[1]>=end and (other[0]<ln or other[1]>end)
                   for other in parser.out):continue
            yield ln,text,raw
        # Templates inside scripts also display text. Report them as unresolved dynamic
        # prose; no attempt to execute arbitrary HTML script is needed for this gate.
        for m in re.finditer(r'<script\b[^>]*>(.*?)</script>',body,re.S|re.I):
            for off,line in enumerate(m[1].splitlines()):
                if not line.lstrip().startswith(('//','/*','*')) and interesting(clean(line)) and ('`' in line or "'" in line or '"' in line):
                    yield body.count('\n',0,m.start())+off+1,clean(line),line
    elif path.suffix=='.md':
        start=1
        for m in re.finditer(r'\S[^\n]*(?:\n(?!\s*\n)[^\n]*)*',body):
            raw=m[0];text=clean(raw)
            if interesting(text) or (raw.lstrip().startswith('|') and NUM.search(text) and (re.search(r'kg/m|kg.m|density|mass|tube',text,re.I) or (rel=='docs/FLOAT.md'))):
                yield body.count('\n',0,m.start())+1,text,raw
    elif path.suffix=='.py':
        # Only display/documentation strings and comments, never float type annotations.
        tree=ast.parse(body)
        for n in ast.walk(tree):
            if isinstance(n,ast.Constant) and isinstance(n.value,str) and interesting(n.value):
                yield n.lineno,re.sub(r'\s+',' ',n.value).strip(),n.value
        for i,line in enumerate(body.splitlines(),1):
            if line.lstrip().startswith('#') and interesting(line):
                yield i,re.sub(r'\s+',' ',line).strip(),line


def paths():
    result=[ROOT/'README.md',ROOT/'index.html',ROOT/'tools/ship_scoping.py']
    for parent in ['docs','research','engineering','ship','cell','concept']:
        for p in (ROOT/parent).rglob('*'):
            if p.suffix in ('.md','.html') and p.name!='FLOAT-LEDGER.md':result.append(p)
    return sorted(set(result))


def interpretation(text):
    if re.search(r'Mission.?0|two.thousand|certified world',text,re.I):return 'mission'
    if re.search(r'scale is the lever',text,re.I):return 'size trend'
    if re.search(r'default hull|scoping tool|scoping.*(?:ratio|hull)',text,re.I):return 'scoping default hull'
    if re.search(r'ship\.(?:ratio|mass|lift|bestWorld)|walls\.|0\.558|0\.981|best defensible|harsh',text,re.I):return 'hull of record'
    if re.search(r'bench|article|218|stock\.|demo\.|weigh\.|2\.691',text,re.I):return 'bench article'
    if re.search(r'Jenett|Akhmeteli|hierarch|kg/m|kg.m|wallWork|level2',text,re.I):return 'density or closed-form bound'
    if re.search(r'P-?100|payload|fleet|float.up|buoyan',text,re.I):return 'assumed fleet or operational requirement'
    return 'float-related claim awaiting an explicit object/field binding'


def proposal(kind,rows,ledger):
    rec=rows[LIVE['ship.ratio'][0]];best=rows[LIVE['ship.bestWorldRatio'][0]]
    alt=ledger['atmosphere']['targetM'];rho=ledger['atmosphere']['rhoTarget']
    if kind in ('hull of record','scoping default hull'):
        if kind=='scoping default hull':
            rec=rows['hull-52m/tool-default-wall-4.0m/gamma-0.30/chord-1050/sf-1.2']
            best=rows['hull-52m/tool-default-wall-4.0m/gamma-0.65/chord-1450/sf-1.2']
        return (f"{kind.capitalize()}: lift/mass {rec['at']['seaLevel']['liftToMass']:.3f} at sea level and "
                f"{rec['at']['target']['liftToMass']:.3f} at {alt:,} m, SF 1.2, assumed γ 0.30, "
                f"1,050 MPa chords. With assumed γ 0.65 and the unverified 1,450 MPa carbon-laminate "
                f"ceiling, the ratios are {best['at']['seaLevel']['liftToMass']:.3f} and "
                f"{best['at']['target']['liftToMass']:.3f}; the working-altitude deficit is "
                f"{-best['at']['target']['margin']:.1f} t before equipment. See docs/FLOAT-LEDGER.md.")
    if kind=='mission':
        return ('The mission is a scenario, not a certified vehicle. Even with both favourable design credits '
                'and no safety margin, its hull mass exceeds working-altitude lift; the shear system mass '
                'is unpriced. See the Mission 0 rows in docs/FLOAT-LEDGER.md before adding payload or equipment.')
    if kind=='size trend':
        return (f'The air-density limit is {rho:.4f} kg/m³ at {alt:,} m. On the current sea-level-pressure '
                'sizing basis the record-world lift/mass ratio falls across the sampled hull sizes; '
                'scaling up alone does not close the mass budget. See docs/FLOAT-LEDGER.md.')
    if kind=='bench article':
        b=rows['bench-nominal']
        return (f"Article A is computed at {b['mass']:.3f} kg, displacing "
                f"{b['extras']['displacedSeaLevelG']:.1f} g of air at sea level and "
                f"{b['extras']['displacedTargetG']:.1f} g at {alt:,} m. It does not float at either altitude. "
                'The structure uses the model’s SF 1.5; mesh-integrated joint mass is not a physical weighing. '
                'See docs/FLOAT-LEDGER.md for the load checks and loaded-volume variant.')
    if kind=='density or closed-form bound':
        return (f'This density comparison has not been bound here to a named material, architecture, '
                f'film convention and structural basis. Air is 1.2250 kg/m³ at sea level and '
                f'{rho:.4f} kg/m³ at {alt:,} m. A formula or literature input below that limit '
                'does not establish a drawn floating hull; the current named cases and their '
                'safety factors and knockdowns are in docs/FLOAT-LEDGER.md.')
    if kind=='float-related claim awaiting an explicit object/field binding':
        return ('This passage has no checked binding to a current float result. Its figures remain unverified '
                'here until the named object, altitude, sizing pressure, safety factor and knockdown basis '
                'are supplied; a hypothetical result is not a demonstrated floating vehicle.')
    return ('This buoyancy scenario is conditional on the simulator’s assumed dry mass equalling payload, '
            'and on its evaluated altitude and loading. It is not a structural mass estimate or an '
            'operational result. The sea-level and working-altitude allowances in docs/FLOAT-LEDGER.md '
            'do not establish a buildable floating structure.')


def catalog_values():
    # Execute the engineering page's own declarations and the viewer's pure context
    # builder. Never run the DOM/mounting tail. Display values are inventory only;
    # passing still requires the exact LIVE ledger-field mapping above.
    prefix=(ROOT/'engineering/engineering.js').read_text().split('/* ---- the binder:')[0]
    if 'const VALUES =' not in prefix or 'document.' in prefix:return None
    prefix=prefix.replace("'../ship/", "'./ship/")
    js=(prefix+"\nimport { computeCtx } from './ship/explorer.js';\n"
        "import { BAND } from './ship/catalog.js';\n"
        "process.stdout.write(JSON.stringify({...SHIP, __engineering:VALUES, "
        "__ship:{...computeCtx(),ship:SHIP,band:BAND,grid:GRID,w:WALL}}));")
    try:
        p=subprocess.run(['node','--input-type=module','-e',js],cwd=ROOT,capture_output=True,text=True,timeout=30)
        if p.returncode:return None
        return json.loads(p.stdout)
    except (OSError,subprocess.TimeoutExpired,json.JSONDecodeError):return None


def inspect_block(path,line,text,raw,rows,ledger,cat):
    kind=interpretation(text)
    hit=dict(file=path,line=line,figure=NUM.findall(re.sub(r'\[data-[^]]+\]','',text)),sentence=text,raw=raw,meaning=kind,
             status='FAIL',reason='No explicit binding to a named ledger field.',
             proposedWording=proposal(kind,rows,ledger))
    hit['dynamicFigures']=[]
    for token in re.finditer(r'\[([^]]*data-(?:n|cat)="[^"]+"[^]]*)\]',raw):
        attrs=dict(re.findall(r'([\w-]+)="([^"]*)"',token[1]))
        route=attrs.get('data-n',attrs.get('data-cat'));value=None
        if cat is not None:
            context=cat.get('__engineering' if 'data-cat' in attrs else '__ship',{})
            try:value=dig(context,route)
            except (KeyError,TypeError,IndexError):pass
        if isinstance(value,(int,float)):
            value*=float(attrs.get('data-mul','1000' if 'data-mm' in attrs else '1'))
            rendered=f"{value:,.{int(attrs.get('data-f','0'))}f}"
        else:rendered='unresolved'
        hit['dynamicFigures'].append(dict(route=route,value=value,display=rendered,
            basis='default page context; not an accepted ledger binding'))
    for pattern,reason in ALLOWLIST:
        if pattern.fullmatch(path):
            hit.update(status='ALLOW',reason=reason);return hit
    bindings=list(BIND.finditer(raw));live=re.findall(r'data-(?:n|cat)="([^"]+)"',raw)
    bound=[]
    if bindings:
        for m in bindings:
            cid,field,value=m.groups();cid=cid.strip();field=field.strip()
            try:expected=dig(rows[cid],field)
            except (KeyError,TypeError):hit['reason']='Unknown named ledger field.';return hit
            dp=len(value.partition('.')[2])
            if round(expected,dp)!=float(value) or value not in clean(re.sub(r'<!--.*?-->','',raw,flags=re.S)):
                hit['reason']='Named value differs from the ledger or is absent from the visible text.';return hit
            bound.append((rows[cid],field))
        # Explicit bindings must cover every ratio/density/mass claim. Free prose remains
        # inventoried; this syntax is intended for one named figure per block.
        if len(bindings)!=1:
            hit['reason']='Use one named quantity per bound block.';return hit
        visible=clean(re.sub(r'<!--.*?-->','',raw,flags=re.S))
        remainder=visible.replace(bindings[0][3],'',1)
        remainder=re.sub(r'(?:SF|γ|gamma|knockdown)\s*[=:]?\s*[\d.]+|[\d,]+(?:\.\d+)?\s*(?:m\b|MPa\b|Pa\b)', '',remainder,flags=re.I)
        if NUM.search(remainder):
            hit['reason']='Additional numeric claim is not covered by the named field.';return hit
    elif live and all(x in LIVE for x in live):
        if cat is None:hit['reason']='Catalog could not be executed; dynamic value is unknown.';return hit
        for x in live:
            cid,field,key=LIVE[x]
            v=dig(rows[cid],field)
            if abs(cat[key]-v)>0.0005:hit['reason']='Catalog value differs from named ledger field.';return hit
            bound.append((rows[cid],field))
        hit['binding']=[{'case':LIVE[x][0],'field':LIVE[x][1]} for x in live]
    else:
        if live:hit['reason']='Dynamic display has no checked field binding: '+', '.join(live)
        return hit
    if not ALT.search(text):
        hit['reason']='Unbound altitude: no altitude in this sentence, table or enclosing display block.';return hit
    altitudes=set()
    if re.search(r'sea[ -]level',text,re.I):altitudes.add(0)
    if re.search(r'working altitude|target altitude',text,re.I):altitudes.add(ledger['atmosphere']['targetM'])
    for m in re.finditer(r'(?:at|altitude|air at)\s*([\d,]+)\s*m\b|([\d,]+)\s*m\s*(?:MSL|altitude)',text,re.I):
        altitudes.add(float((m[1] or m[2]).replace(',','')))
    for row,field in bound:
        if field.startswith('at.'):
            expected_alt=row['at'][field.split('.')[1]]['altitudeM']
            if expected_alt not in altitudes:
                hit['reason']='Stated altitude differs from the altitude of the named field.';return hit
        explicit_sf=re.findall(r'(?:\bSF\b|safety factor)\s*[=:]?\s*(\d+(?:\.\d+)?)',text,re.I)
        if explicit_sf and any(float(v)!=row['safetyFactor']['value'] for v in explicit_sf):
            hit['reason']='Stated safety factor differs from the named row.';return hit
        explicit_gamma=re.findall(r'(?:γ|gamma)\s*[=:]?\s*(\d+(?:\.\d+)?)',text,re.I)
        row_gamma=[k['value'] for k in row['knockdowns'] if k['id'] in ('gi-harsh','gi-frame')]
        if explicit_gamma and any(float(v) not in row_gamma for v in explicit_gamma):
            hit['reason']='Stated general-instability knockdown differs from the named row.';return hit
    if not (LINK.search(raw) or (FACTORS.search(text) and KD.search(text))):
        hit['reason']='Safety factor and knockdown status are missing; no basis link in the block.';return hit
    hit.update(status='PASS',reason='Named value and its altitude/basis are bound.')
    return hit


def inventory(ledger):
    rows={c['id']:c for d in ledger['designs'] for c in d['cases']}
    cat=catalog_values();hits=[]
    for path in paths():
        rel=path.relative_to(ROOT).as_posix()
        for line,text,raw in source_blocks(path):
            hits.append(inspect_block(rel,line,text,raw,rows,ledger,cat))
    return hits+generated_inventory(ledger)



def generated_inventory(ledger):
    """Machine figures have pointers as well as file/line; prose heuristics cannot see them."""
    keys={'totalT','ratioSL','ratio2500','residualSLT','residual2500T','liftSLT','lift2500T',
          'totalKg','kgPerM3','totalKgPerM3','latticeKgPerM3','nodesKgPerM3','filmKgPerM3',
          'displacedAirKg','massOverDisplaced','marginX','floats','densityAtN1','requiredKgPerM3',
          'requiredKgPerM2','allowanceT','overBy','shellAloneOverBy','shellBudgetLeftT',
          'requiredShellKgPerM3','arealKgM2'}
    hits=[]
    for artifact in ledger.get('sourceArtifacts',[]):
        path=ROOT/artifact['path'];raw=path.read_text();doc=json.loads(raw)
        changes={r['pointer']:r for r in artifact.get('changedNumbers',[])}
        # Locate each leaf through a single forward token walk, preserving duplicate keys.
        tokens=list(re.finditer(r'"([^"\\]*(?:\\.[^"\\]*)*)"\s*:\s*(true|false|-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)',raw))
        line_positions={}
        for token in tokens:
            line_positions.setdefault((token[1],token[2]),[]).append(raw.count('\n',0,token.start())+1)
        used={}
        def walk(value,pointer=''):
            if isinstance(value,dict):
                for key,v in value.items():
                    ptr=pointer+'/'+key if pointer else key
                    if key in keys and isinstance(v,(int,float,bool)):
                        literal=json.dumps(v);idx=used.get((key,literal),0);used[(key,literal)]=idx+1
                        positions=line_positions.get((key,literal),[1]);line=positions[min(idx,len(positions)-1)]
                        # The generated source object is independently rerun, but this is
                        # still inventory rather than a blanket endorsement of its basis.
                        hits.append(dict(file=artifact['path'],line=line,figure=[v],pointer=ptr,
                            sentence=ptr+' = '+literal,meaning='generated quantity, object named by JSON pointer',
                            status='FAIL' if ptr in changes else 'ALLOW',
                            reason=('Explicit generated-output allowance: source tool independently rerun; '
                                    'basis is supplied by the corresponding design section, not by a prose sentence.'
                                    if ptr not in changes else
                                    f"Committed value is stale: {changes[ptr]['old']} -> {changes[ptr]['fresh']} in a fresh run."),
                            proposedWording='Regenerate this source with its owning prose gate; retain old and new values. '
                                            'Until then cite the fresh float-ledger rows, not this committed value.'))
                    walk(v,ptr)
            elif isinstance(value,list):
                for i,v in enumerate(value):walk(v,pointer+'/'+str(i))
        walk(doc)
    return hits

def markdown(hits):
    def esc(s):return str(s).replace('|','\\|').replace('\n',' ').replace('<','&lt;').replace('>','&gt;')
    # Public hand-up must never copy a private source path out of historical prose.
    def public(s):
        return re.sub(r'(?:/home/[^\s`<>]+|~/[^\s`<>]+)', '[private path omitted]',esc(s))
    lines=['| Sentence / figure | Where | Ledger interpretation / failure | Proposed wording |',
           '| --- | --- | --- | --- |']
    priority={'mission':0,'size trend':1,'hull of record':2,'scoping default hull':3,'bench article':4}
    for h in sorted(hits,key=lambda h:(priority.get(h['meaning'],5),h['file'],h['line'])):
        if h['status']=='FAIL':
            lines.append('| '+' | '.join(public(x) for x in [h['sentence'],f"{h['file']}:{h['line']}",
                h['meaning']+' — '+h['reason'],h['proposedWording']])+' |')
    return '\n'.join(lines)


def main():
    if shutil.which('node') is None:
        print('ledgercheck: node is missing from PATH; install Node to run this gate.', file=sys.stderr)
        return 1
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inventory',action='store_true');ap.add_argument('--report',action='store_true')
    args=ap.parse_args()
    if not (args.inventory or args.report):
        p=subprocess.run([sys.executable,str(ROOT/'tools/float_ledger.py'),'--check'],cwd=ROOT)
        if p.returncode:return p.returncode
    if not LEDGER.exists():print('ledgercheck: no ledger',file=sys.stderr);return 1
    ledger=json.loads(LEDGER.read_text());hits=inventory(ledger)
    # A failing block passes only through its reviewed disposition in the float-claims record.
    sys.path.insert(0,str(ROOT/'tools'))
    import float_claims
    record_errors=float_claims.apply(hits,ledger)
    if args.inventory:print(json.dumps(hits,ensure_ascii=False,indent=2));return 0
    if args.report:print(markdown(hits));return 0
    record_errors.extend(float_claims.check_deferred(hits))
    deferred=float_claims.deferred_counts(hits)
    failed=[h for h in hits if h['status']=='FAIL']
    for h in failed:print(f"{h['file']}:{h['line']}: {h['reason']}\n  {h['sentence']}\n  Proposed: {h['proposedWording']}")
    for e in record_errors:print('float-claims record: '+e)
    if failed or record_errors:
        print('ledgercheck: every block above needs one reviewed disposition in research/analysis/float-claims/. '
              'Reword a sentence the ledger contradicts; class the rest. '
              'python3 tools/float_claims.py --help lists the classes; --propose FILE writes the skeleton.')
    print(f'ledgercheck: {len(hits)} inventoried blocks; {len(failed)} FAIL; '
          f'{sum(h["status"]=="ALLOW" for h in hits)} explicit allowances; '
          f'{sum(h["status"]=="PASS" for h in hits)} bound blocks; {len(record_errors)} record errors; '
          f'{sum(deferred.values())} deferred (' + ', '.join(
              f'{owner}={deferred.get(owner, 0)}' for owner in float_claims.DEFERRED_OWNERS) + ')')
    return 1 if failed or record_errors else 0


if __name__=='__main__':sys.exit(main())
