"""Read local basis, altitude and signed-margin words beside bound float quantities."""
import re

ALT = re.compile(r'sea[ -]level|(?:working|target) altitude|2,?500\s*m\b',re.I)
BASIS = re.compile(r'\b(record|favourable) basis\b|\bbest defensible world\b',re.I)


def check(binding, text, sources, ledger):
    row = sources.rows.get(binding.get('case'))
    field = binding.get('field','')
    errors = []
    if not row or not field.startswith('at.'):
        return errors
    # Binder tokens count as positions; their values are checked separately.
    if 'route' in binding:
        positions = [(m.start(),m.end()) for m in re.finditer(r'\[[^\]]*data-(?:n|cat)="'+re.escape(binding['route'])+r'"[^\]]*\]',text)]
    elif 'shown' in binding:
        shown = str(binding['shown']).replace(',','')
        positions = [(m.start(),m.end()) for m in re.finditer(r'(?<![\w.])[-−+]?\d[\d,]*(?:\.\d+)?',text)
                     if m[0].replace(',','').replace('−','-').lstrip('+') == shown]
    else:
        return errors
    altitude = field.split('.')[1]
    for lo, hi in positions:
        suffix = re.sub(r'[*`>]', '',text[hi:hi+100])
        stated = ALT.search(suffix)
        # A local "at" qualifier, before a sentence boundary, belongs to this figure.
        between = suffix[:stated.start()] if stated else ''
        if stated and not re.search(r'\.(?:\s|$)|[;|]',between):
            actual = 'seaLevel' if re.search('sea[ -]level',stated[0],re.I) else 'target'
            if actual != altitude:
                errors.append('figure qualifier names a different altitude from its bound field')
        scopes = list(BASIS.finditer(text[:lo]))
        if scopes and row['id'].startswith('hull-') and '/as-drawn/' in row['id']:
            scope = scopes[-1]
            next_scope = BASIS.search(text,scope.end())
            segment = text[scope.start():next_scope.start() if next_scope else len(text)]
            gamma = re.search(r'(?:knockdown|γ|gamma)\s*(\d+(?:\.\d+)?)',segment,re.I)
            chord = re.search(r'(\d[\d,]*(?:\.\d+)?)\s*MPa',segment,re.I)
            sf = re.search(r'(?:safety factor|\bSF)\s*(\d+(?:\.\d+)?)',segment,re.I)
            if gamma and float(gamma[1]) not in [k['value'] for k in row.get('knockdowns',[]) if k['id'] in ('gi-harsh','gi-frame')]:
                errors.append('basis qualifier knockdown differs from its bound row')
            if chord and float(chord[1].replace(',','')) not in [v['value'] for v in row.get('inputs',[]) if v.get('unit')=='MPa']:
                errors.append('basis qualifier chord allowable differs from its bound row')
            if sf and float(sf[1]) != row.get('safetyFactor',{}).get('value'):
                errors.append('basis qualifier safety factor differs from its bound row')
        if field.endswith('.margin'):
            words = list(re.finditer(r'\b(short(?:fall)?(?: by)?|deficit|over by|excess|surplus)\b',text[max(0,lo-160):lo],re.I))
            if words:
                direction = -1 if words[-1][1].lower().startswith(('short','deficit')) else 1
                value = sources.value(binding)
                if value*direction < 0:
                    errors.append('margin sign disagrees with shortfall or excess qualifier')
    return list(dict.fromkeys(errors))
