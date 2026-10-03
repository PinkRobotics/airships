"""Shared lexical and structural float-language rules (not a language proof)."""
import re

# These phrases carry a lift verdict even without the original float/buoyancy cues.
RELATION = re.compile(
    r'\b(?:lighter|heavier) than (?:the )?air\b'
    r'|\blift (?:exceeds?|exceeded|surpasses?|falls short of|is less than) (?:its )?(?:mass|weight)\b'
    r'|\bnet lift\b|\b(?:surplus|shortfall|deficit) (?:of|in) lift\b'
    r'|\b(?:rises?|sinks?) (?:unaided|on (?:its|their) own)\b'
    r'|\bcarries? (?:its|their) own structure\b|\blift to spare\b'
    r'|\bneeds? ballast to stay down\b|\bweighs? less than nothing in air\b'
    r'|\bdeficit is closed\b|\b(?:lifts?|holds?) (?:itself|themselves) up\b', re.I)

# Subject / relation / air or lift: this rule does not depend on a single verdict phrase.
STRUCTURAL_RELATION = re.compile(
    r'\b(?:hull|vehicle|airship|cell|structure)\b[^.!?\n]{0,180}'
    r'\b(?:rises?|sinks?|lighter|heavier|holds?|lifts?|supports?|carries?|weighs?)\b'
    r'[^.!?\n]{0,100}\b(?:air|itself|themselves|own|lift|unaided)\b'
    r'|\b(?:lift|displacement)\b[^.!?\n]{0,100}'
    r'\b(?:exceeds?|exceeded|surplus|shortfall|deficit|less|greater|positive|negative)\b'
    r'[^.!?\n]{0,100}\b(?:mass|weight|hull|vehicle|structure|air)\b', re.I)


def relation(text):
    return bool(RELATION.search(text) or STRUCTURAL_RELATION.search(text))


def verdict_relation(text):
    # Merely naming net lift is inventory, not an affirmative structural verdict.
    return bool(RELATION.search(re.sub(r'\bnet lift\b(?!\s+(?:(?:is|was)\s+)?(?:positive|negative))', '', text, flags=re.I)))


def js_strings(body):
    """Lex quoted and template strings; skip comments, regex and interpolation code.

    Nested interpolation strings are inventoried too. Expression placeholders remain
    visible as ${...}; this gate does not guess their rendered numeric values.
    """
    found = []
    def string(i):
        quote, start = body[i], i
        i += 1
        chars = []
        while i < len(body):
            c = body[i]
            if c == "\\" and i+1 < len(body):
                match = re.match(r'\\(?:u\{([0-9a-fA-F]+)\}|u([0-9a-fA-F]{4})|x([0-9a-fA-F]{2}))', body[i:])
                if match:
                    chars.append(chr(int(next(g for g in match.groups() if g),16)))
                    i += len(match[0]); continue
                nxt = body[i+1]
                chars.append({'n':'\n','r':'\r','t':'\t'}.get(nxt,nxt))
                i += 2; continue
            if c == quote:
                i += 1; break
            if quote == '`' and body.startswith('${',i):
                end = code(i+2, nested=True)
                chars.append('${'+body[i+2:end-1]+'}')
                i = end; continue
            chars.append(c); i += 1
        found.append((start,i,body.count('\n',0,start)+1,''.join(chars)))
        return i
    def code(i, nested=False):
        depth = 0
        previous = ''
        while i < len(body):
            c = body[i]
            if body.startswith('//',i):
                end = body.find('\n',i+2)
                i = len(body) if end < 0 else end+1; continue
            if body.startswith('/*',i):
                end = body.find('*/',i+2)
                i = len(body) if end < 0 else end+2; continue
            if c in "'\"`":
                i = string(i); previous = 'literal'; continue
            if c == '/' and (not previous or previous in '=(:,[!&|?;{' or body[max(0,i-7):i].strip()=='return'):
                # Regex literals may themselves contain quotes and comment-like text.
                i += 1; bracket = False
                while i < len(body):
                    if body[i]=='\\': i += 2; continue
                    if body[i]=='[': bracket=True
                    elif body[i]==']': bracket=False
                    elif body[i]=='/' and not bracket:
                        i += 1; break
                    i += 1
                previous = 'literal'; continue
            if c == '{': depth += 1
            elif c == '}':
                if nested and depth == 0:return i+1
                depth -= 1
            if not c.isspace():previous=c
            i += 1
        return i
    code(0)
    grouped = []
    for start,end,line,text in sorted(found):
        if grouped and re.fullmatch(r'\s*\+\s*',body[grouped[-1][1]:start]):
            a,_,ln,prior = grouped.pop()
            grouped.append((a,end,ln,prior+text))
        else:
            grouped.append((start,end,line,text))
    for _,_,line,text in grouped:
        yield line,text
