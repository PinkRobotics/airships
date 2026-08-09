#!/usr/bin/env python3
"""Enforce the repository's four structural rules. Run by CI and by `make lint`.

RULE 1 — the dependency direction.
    sim/ imports nothing outside sim/. 3d/ imports nothing outside 3d/. app/ may import
    both. concept/ may import sim/. Nothing imports app/.

    The model is the part of this project that invites argument, so it has to be readable
    and runnable on its own: the moment it imports a canvas or a fetch, "read the physics"
    becomes "read the whole site".

    All three ways a module can name another are checked: `import … from '…'`,
    `export … from '…'` and `import('…')`. The re-export form matters most, because the
    index files are where a whole directory's public surface is assembled and where a
    single added line would quietly widen it.

RULE 2 — no module assigns to a binding it imported.
    ES modules make imported bindings read-only, so a cross-module write is a runtime
    TypeError in strict mode rather than a compile error you would notice. Where one
    module genuinely needs to change another's state, the owner exports a function that
    does it, and the change has a name.

RULE 3 — live data must be passed, not defaulted away.
    `planTargets(mission, heat)` takes satellite hotspots as an argument so that the model
    can run with no feed. The argument has a default of `[]`, which means an application
    call site that forgets it does not fail — it silently reverts to geometry-only scoring.
    That happened: all three call sites lost the argument during the extraction and no test
    noticed, because the golden files are recorded in replay mode where the sampled fleet
    carries no heat-derived targets. Inside app/, the argument is required.

RULE 4 — sim/ reaches for no environment.
    sim/README and the header of sim/index.js promise "no DOM, no network, no wall clock,
    no location, no globals". Rule 1 cannot see that promise: a module that calls `fetch`
    or reads `Date.now()` imports nothing at all. Without this rule the linter's success
    message asserted a property it never looked at. The one deliberate exception is
    `Math.random` in sim/rng.js, listed in ALLOWED_ENVIRONMENT with its reason.

The linter is the mechanism behind the repository's structural claims, so it carries its
own tests: `--selftest` runs them against constructed violating and non-violating trees,
and an ordinary run does the same before it looks at the working tree, so `make lint`
cannot pass with a broken checker.

Exit status is non-zero on any violation, with the file and line.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

AREAS = ('sim', 'app', '3d', 'concept', 'tests', 'model-lab')

# who may import whom, by top-level directory
ALLOWED = {
    'sim': {'sim'},
    '3d': {'3d'},
    'app': {'app', 'sim', '3d'},
    'concept': {'concept', 'sim', '3d'},
    'tests': {'tests', 'sim', '3d', 'app'},
    'model-lab': {'model-lab', '3d', 'sim'},
}

# Rule 1. Three forms, all of which create a real dependency at load time.
#   import a, { b as c } from './x.js'   import './x.js'   (side effect only)
#   export { b } from './x.js'           export * as ns from './x.js'
#   import('./x.js')                     import(new URL('./x.js', import.meta.url))
# The lookbehind keeps `foo.import(` and `myimport` out. Matching is done against the raw
# text, because the specifier is a string literal and the stripper blanks those; matches
# that fall inside a comment or a string are discarded by _in_code().
STATIC_IMPORT = re.compile(
    r"""(?<![.\w$])import\s+(?:(?P<what>[\w${},*\s]+?)\s+from\s+)?['"](?P<spec>[^'"]+)['"]""")
REEXPORT = re.compile(
    r"""(?<![.\w$])export\s+(?:\*(?:\s+as\s+[A-Za-z_$][\w$]*)?|\{[^}]*\})\s*"""
    r"""from\s*['"](?P<spec>[^'"]+)['"]""")
DYNAMIC_IMPORT = re.compile(r'(?<![.\w$])import\s*\(')
STRING_LITERAL = re.compile(r"""['"]([^'"]*)['"]""")

# Rule 2.
ASSIGN = re.compile(r'(?<![.\w$])(?P<name>[A-Za-z_$][\w$]*)\s*(?:=(?!=)|\+\+|--|\+=|-=|\*=|/=)')

# Rule 3. Calls that must not rely on a default, and the area the rule applies to. The
# value is the smallest number of arguments a correct call has.
REQUIRED_ARGS = {'planTargets': ('app', 2)}

# Rule 4. What sim/ must not name, and the promise each name would break. Matched as bare
# identifiers only, so `state.window` and `{ location: … }` on the right of a dot are not
# flagged; an object *key* called `document` would be, which has not come up and would be
# worth a second look if it did.
ENVIRONMENT = {
    'document': 'the DOM',
    'window': 'the DOM',
    'navigator': 'the DOM',
    'location': 'the page URL',
    'globalThis': 'globals',
    'self': 'globals',
    'process': 'globals',
    'require': 'a module system that is not ES modules',
    'fetch': 'the network',
    'XMLHttpRequest': 'the network',
    'WebSocket': 'the network',
    'EventSource': 'the network',
    'localStorage': 'browser storage',
    'sessionStorage': 'browser storage',
    'indexedDB': 'browser storage',
    'caches': 'browser storage',
    'Date': 'the wall clock',
    'performance': 'the wall clock',
    'setTimeout': 'the wall clock',
    'setInterval': 'the wall clock',
    'requestAnimationFrame': 'the wall clock',
    'crypto': 'unseeded entropy',
    'Math.random': 'unseeded entropy',
    'console': 'a host that has one',
    'alert': 'the DOM',
}
ENVIRONMENT_RE = re.compile(
    r'(?<![.\w$])(?:' + '|'.join(
        re.escape(k).replace(r'\.', r'\s*\.\s*') for k in sorted(ENVIRONMENT, key=len, reverse=True)
    ) + r')(?![\w$])')

# The exceptions, each with the reason it is one. Keyed by (repository-relative path,
# identifier); anything not listed here fails.
ALLOWED_ENVIRONMENT = {
    ('sim/rng.js', 'Math.random'):
        'the unseeded default seed, deliberate: setSeed() replaces it, and every published '
        'number is produced with a seed set. Nothing else in sim/ may reach for entropy.',
}

OUTSIDE = '\x00outside'          # resolve() sentinel: a specifier that leaves the repository


def area_of(rel: str) -> str:
    return rel.split('/')[0]


def resolve(rel_src: str, spec: str) -> str | None:
    """Repository-relative target of `spec` as written in `rel_src`.

    None for a bare specifier, which names a package rather than a file here and is not
    this rule's business. OUTSIDE when the path climbs past the repository root. Purely
    textual, so the self-tests can check trees that are not on disk.
    """
    if not spec.startswith('.'):
        return None
    parts = rel_src.split('/')[:-1] + spec.split('?')[0].split('/')
    out: list[str] = []
    for p in parts:
        if p in ('', '.'):
            continue
        if p == '..':
            if not out:
                return OUTSIDE
            out.pop()
        else:
            out.append(p)
    return '/'.join(out)


def js_files():
    for area in AREAS:
        d = ROOT / area
        if d.is_dir():
            yield from sorted(p for p in d.rglob('*.js') if 'node_modules' not in p.parts)


_REGEX_PRECEDERS = set('=(,:[!&|?{};+-*%~^<>') | {''}


def _regex_can_start(out: list) -> bool:
    """True if a `/` here begins a regex literal rather than a division.

    Decided by the previous meaningful character, which is the standard heuristic and
    is unambiguous for every occurrence in this codebase.
    """
    for chunk in reversed(out):
        s = chunk.rstrip()
        if s:
            return s[-1] in _REGEX_PRECEDERS
    return True


def strip_comments_and_strings(text: str) -> str:
    """Blank out anything a reference could hide in, keeping line structure intact.

    Comments and plain string literals become spaces. Template literals become spaces too —
    EXCEPT for their `${...}` interpolations, which are ordinary expressions and routinely
    the only place a helper is called from. Blanking those makes a real dependency
    invisible, and the module then loads fine and throws on first use.

    The result is the same length as the input, character for character. Rule 1 reads
    specifiers out of the raw text and uses this copy as a mask to tell code from
    commentary, so that correspondence is load-bearing; the self-tests assert it.
    """
    out: list[str] = []
    i, n = 0, len(text)

    def blank(s: str) -> str:
        return ''.join(ch if ch == '\n' else ' ' for ch in s)

    while i < n:
        c = text[i]
        two = text[i:i + 2]
        if two == '//':
            j = text.find('\n', i)
            j = n if j < 0 else j
            out.append(blank(text[i:j]))
            i = j
        elif two == '/*':
            j = text.find('*/', i + 2)
            j = n if j < 0 else j + 2
            out.append(blank(text[i:j]))
            i = j
        elif c == '`':
            out.append(' ')
            i += 1
            while i < n and text[i] != '`':
                if text[i] == '\\':
                    out.append('  ')
                    i += 2
                elif text[i:i + 2] == '${':
                    depth, j = 1, i + 2
                    while j < n and depth:
                        if text[j] == '{':
                            depth += 1
                        elif text[j] == '}':
                            depth -= 1
                        elif text[j] in '"\'`':          # a string inside the interpolation
                            q, j = text[j], j + 1
                            while j < n and text[j] != q:
                                j += 2 if text[j] == '\\' else 1
                        j += 1
                    out.append('  ' + text[i + 2:j - 1] + ' ')   # keep the expression
                    i = j
                else:
                    out.append(text[i] if text[i] == '\n' else ' ')
                    i += 1
            out.append(' ')
            i += 1
        elif c == '/' and _regex_can_start(out):
            # a regex literal, not division: `/[&<>"]/g` contains a quote that would
            # otherwise open a phantom string and swallow the rest of the file
            j = i + 1
            in_class = False
            while j < n:
                if text[j] == '\\':
                    j += 2
                    continue
                if text[j] == '[':
                    in_class = True
                elif text[j] == ']':
                    in_class = False
                elif text[j] == '/' and not in_class:
                    j += 1
                    break
                elif text[j] == '\n':
                    break                                    # not a regex after all
                j += 1
            out.append(blank(text[i:j]))
            i = j
        elif c in '"\'':
            j, q = i + 1, c
            while j < n:
                if text[j] == '\\':
                    j += 2
                    continue
                if text[j] == q:
                    j += 1
                    break
                j += 1
            out.append(blank(text[i:j]))
            i = j
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def line_of(text: str, pos: int) -> int:
    return text.count('\n', 0, pos) + 1


def _in_code(raw: str, code: str, pos: int) -> bool:
    """True if the character at `pos` is code rather than comment or string content."""
    return code[pos] == raw[pos]


def local_names(what: str) -> list[str]:
    """The bindings an import clause introduces into the importing module.

    `{ b as c }` binds `c` and not `b`, so only `c` can be assigned to; the previous
    version listed both and would have reported a write to a name that does not exist.
    """
    names: list[str] = []
    head, brace = what, ''
    if '{' in what:
        head, brace = what[:what.index('{')], what[what.index('{'):]
    for clause in head.split(','):
        toks = re.findall(r'[A-Za-z_$][\w$]*|\*', clause)
        if not toks:
            continue
        names.append(toks[-1] if len(toks) > 1 else toks[0])   # `* as ns` → ns
    for clause in brace.strip('{}').split(','):
        toks = [t for t in re.findall(r'[A-Za-z_$][\w$]*', clause)]
        if not toks:
            continue
        names.append(toks[-1] if 'as' in toks else toks[0])
    return [n for n in names if n not in ('as', '*')]


def calls(code: str, fn: str):
    """Yield (offset, [argument text]) for every call to `fn`, however its arguments nest.

    A regex that stops at the first `)` misses `planTargets(m, heat(x))` entirely — it
    matches the inner call instead — so the rule would have been silent on exactly the
    call sites that do something interesting. Arguments are split on top-level commas.
    """
    pat = re.compile(r'(?<![.\w$])' + re.escape(fn) + r'\s*\(')
    for m in pat.finditer(code):
        if code[:m.start()].rstrip().endswith('function'):
            continue                                          # the definition, not a call
        j, par, sq, br = m.end(), 1, 0, 0
        args: list[str] = []
        cur: list[str] = []
        while j < len(code):
            ch = code[j]
            if ch == '(':
                par += 1
            elif ch == ')':
                par -= 1
                if par == 0:
                    break
            elif ch == '[':
                sq += 1
            elif ch == ']':
                sq -= 1
            elif ch == '{':
                br += 1
            elif ch == '}':
                br -= 1
            elif ch == ',' and par == 1 and sq == 0 and br == 0:
                args.append(''.join(cur))
                cur = []
                j += 1
                continue
            cur.append(ch)
            j += 1
        args.append(''.join(cur))
        yield m.start(), [a for a in args if a.strip()]


def specifiers(raw: str, code: str):
    """Yield (offset, specifier or None, form) for every module reference in one file.

    A None specifier is a dynamic import whose argument holds no string literal: the
    target cannot be read off the source, which for sim/ and 3d/ is itself a finding.
    """
    for m in STATIC_IMPORT.finditer(raw):
        if _in_code(raw, code, m.start()):
            yield m.start(), m.group('spec'), 'static import'
    for m in REEXPORT.finditer(raw):
        if _in_code(raw, code, m.start()):
            yield m.start(), m.group('spec'), 're-export'
    for m in DYNAMIC_IMPORT.finditer(raw):
        if not _in_code(raw, code, m.start()):
            continue
        j, par = m.end(), 1
        while j < len(code) and par:                          # parens in `code` are real
            if code[j] == '(':
                par += 1
            elif code[j] == ')':
                par -= 1
            j += 1
        lit = STRING_LITERAL.search(raw[m.end():j])
        # `import(new URL("../../3d/index.js?v=" + v, import.meta.url))` resolves the
        # relative part against the importing module, exactly as a static import would,
        # so the first literal is the specifier.
        yield m.start(), (lit.group(1) if lit else None), 'dynamic import'


def check_files(files: dict[str, str]) -> list[str]:
    """Every violation in a tree given as {repository-relative path: source}."""
    problems: list[str] = []

    for rel in sorted(files):
        raw = files[rel]
        area = area_of(rel)
        code = strip_comments_and_strings(raw)
        if len(code) != len(raw):
            # Rule 1 reads specifiers from `raw` and uses `code` as a mask to tell code
            # from commentary; if the two ever fell out of step it would read the wrong
            # character and drop real imports without saying anything.
            problems.append(f"{rel}: the comment/string mask is misaligned with the source "
                            f"({len(code)} vs {len(raw)} characters) — this is a bug in the "
                            "linter, not in the file; imports here were not checked")
            continue

        # RULE 1 — the dependency direction.
        imported: dict[str, str] = {}
        for pos, spec, form in specifiers(raw, code):
            n = line_of(raw, pos)
            if spec is None:
                if area in ('sim', '3d'):
                    problems.append(
                        f"{rel}:{n}: dynamic import with a computed specifier; {area}/ must "
                        "name its dependencies in the source so they can be checked")
                continue
            target = resolve(rel, spec)
            if target is OUTSIDE:
                problems.append(f"{rel}:{n}: imports outside the repository: {spec}")
            elif target is not None:
                t_area = area_of(target)
                if t_area not in ALLOWED.get(area, {area}):
                    problems.append(
                        f"{rel}:{n}: {area}/ must not import {t_area}/ ({form} of {spec})")
            if form == 'static import':
                m = STATIC_IMPORT.match(raw, pos)
                for name in local_names(m.group('what') or ''):
                    imported[name] = spec

        # RULE 2 — no module assigns to a binding it imported.
        if imported:
            for n, line in enumerate(code.split('\n'), 1):
                for m in ASSIGN.finditer(line):
                    name = m.group('name')
                    if name in imported:
                        problems.append(
                            f"{rel}:{n}: assigns to `{name}`, which it imported from "
                            f"{imported[name]} — ask that module to change it instead")

        # RULE 3 — live data must be passed, not defaulted away.
        for fn, (only_area, need) in REQUIRED_ARGS.items():
            if area != only_area:
                continue
            for pos, args in calls(code, fn):
                if len(args) < need:
                    problems.append(
                        f"{rel}:{line_of(code, pos)}: {fn}() called with {len(args)} "
                        f"argument(s); {area}/ must pass all {need}. The default is a "
                        "silent fallback, not a convenience.")

        # RULE 4 — sim/ reaches for no environment.
        if area == 'sim':
            for m in ENVIRONMENT_RE.finditer(code):
                name = re.sub(r'\s+', '', m.group(0))
                if (rel, name) in ALLOWED_ENVIRONMENT:
                    continue
                problems.append(
                    f"{rel}:{line_of(code, m.start())}: sim/ names `{name}` — that is "
                    f"{ENVIRONMENT[name]}, and sim/ promises none of it. Take the value as "
                    "an argument instead, or add it to ALLOWED_ENVIRONMENT with the reason.")

    return problems


# --------------------------------------------------------------------------------------
# Self-tests. The linter is what makes the repository's structural claims checkable, and
# until now nothing checked the linter: an edit that made a rule match nothing would have
# looked exactly like a clean tree. Each case is a small tree and the exact set of
# violations it must produce — exact, so that a rule that starts over-reporting fails too.

CASES: list[tuple[str, dict[str, str], list[str]]] = [
    ('rule1 static import across the boundary',
     {'sim/a.js': "import { thing } from '../app/b.js';\n"},
     ['sim/a.js:1: sim/ must not import app/ (static import of ../app/b.js)']),

    ('rule1 re-export across the boundary',
     {'sim/index.js': "export { AirshipHUD } from '../3d/index.js';\n"},
     ['sim/index.js:1: sim/ must not import 3d/ (re-export of ../3d/index.js)']),

    ('rule1 star re-export across the boundary, over several lines',
     {'sim/index.js': "// header\nexport {\n  a,\n  b,\n} from '../app/x.js';\n"},
     ['sim/index.js:2: sim/ must not import app/ (re-export of ../app/x.js)']),

    ('rule1 dynamic import with a literal specifier',
     {'sim/a.js': "const m = await import('../3d/index.js');\n"},
     ['sim/a.js:1: sim/ must not import 3d/ (dynamic import of ../3d/index.js)']),

    ('rule1 dynamic import through new URL, the form this repository uses',
     {'sim/sub/a.js': 'const m = await import(new URL("../../app/x.js?v=" + v,\n'
                      '  import.meta.url));\n'},
     ['sim/sub/a.js:1: sim/ must not import app/ (dynamic import of ../../app/x.js?v=)']),

    ('rule1 dynamic import in app/, which may reach 3d/',
     {'app/bridge/v.js': 'const m = await import(new URL("../../3d/index.js?v=" + v,\n'
                         '  import.meta.url));\n'},
     []),

    ('rule1 dynamic import whose target cannot be read off the source',
     {'sim/a.js': 'const m = await import(pathFor(x));\n',
      'app/a.js': 'const m = await import(pathFor(x));\n'},
     ['sim/a.js:1: dynamic import with a computed specifier; sim/ must name its '
      'dependencies in the source so they can be checked']),

    ('rule1 a specifier that climbs out of the repository',
     {'sim/a.js': "import { x } from '../../elsewhere/y.js';\n"},
     ['sim/a.js:1: imports outside the repository: ../../elsewhere/y.js']),

    ('rule1 ignores bare specifiers, which name packages rather than files here',
     {'sim/a.js': "import { x } from 'three';\n"},
     []),

    ('rule1 ignores imports written inside comments and strings',
     {'sim/a.js': "// import { x } from '../app/b.js'\n"
                  "/* export { y } from '../app/b.js' */\n"
                  "const doc = `see import('../app/b.js') for the shape`;\n"
                  "const s = \"import { z } from '../app/b.js'\";\n"},
     []),

    ('rule1 allows the directions the matrix allows',
     {'app/a.js': "import { planCycle } from '../sim/index.js';\n"
                  "export { AirshipHUD } from '../3d/index.js';\n",
      'tests/a.js': "import { boot } from '../app/main.js';\n"},
     []),

    ('rule2 assignment to a named import',
     {'app/a.js': "import { CFG } from '../sim/index.js';\nCFG = {};\n"},
     ['app/a.js:2: assigns to `CFG`, which it imported from ../sim/index.js — ask that '
      'module to change it instead']),

    ('rule2 assignment to a default import',
     {'app/a.js': "import CFG from './c.js';\nCFG += 1;\n"},
     ['app/a.js:2: assigns to `CFG`, which it imported from ./c.js — ask that module to '
      'change it instead']),

    ('rule2 assignment to a namespace import',
     {'app/a.js': "import * as sim from '../sim/index.js';\nsim = null;\n"},
     ['app/a.js:2: assigns to `sim`, which it imported from ../sim/index.js — ask that '
      'module to change it instead']),

    ('rule2 an alias binds the new name, not the old one',
     {'app/a.js': "import { CSS as STYLES } from './c.js';\nCSS = 1;\nSTYLES = 2;\n"},
     ['app/a.js:3: assigns to `STYLES`, which it imported from ./c.js — ask that module '
      'to change it instead']),

    ('rule2 leaves property writes and same-named locals alone',
     {'app/a.js': "import { CFG } from '../sim/index.js';\n"
                  "CFG.rho = 1.2;\nconst CFGx = 2;\nif (CFG === null) {}\n"},
     []),

    ('rule3 the argument omitted in app/',
     {'app/a.js': 'planTargets(m);\n'},
     ['app/a.js:1: planTargets() called with 1 argument(s); app/ must pass all 2. The '
      'default is a silent fallback, not a convenience.']),

    ('rule3 the call nested inside another call, which a flat regex misses',
     {'app/a.js': 'const out = wrap(planTargets(m));\n'},
     ['app/a.js:1: planTargets() called with 1 argument(s); app/ must pass all 2. The '
      'default is a silent fallback, not a convenience.']),

    ('rule3 arguments that themselves contain parentheses and commas',
     {'app/a.js': 'planTargets(m, hotspots(a, b));\nplanTargets(m, [x, y]);\n'},
     []),

    ('rule3 a call split across lines',
     {'app/a.js': 'planTargets(\n  m\n);\n'},
     ['app/a.js:1: planTargets() called with 1 argument(s); app/ must pass all 2. The '
      'default is a silent fallback, not a convenience.']),

    ('rule3 applies to app/ only: sim/ owns the default',
     {'sim/targets.js': 'export function planTargets(m, heat = []) { return planTargets(m); }\n'},
     []),

    ('rule4 the DOM',
     {'sim/a.js': 'const el = document.querySelector("#x");\n'},
     ['sim/a.js:1: sim/ names `document` — that is the DOM, and sim/ promises none of it. '
      'Take the value as an argument instead, or add it to ALLOWED_ENVIRONMENT with the '
      'reason.']),

    ('rule4 the network',
     {'sim/a.js': 'const r = await fetch(url);\n'},
     ['sim/a.js:1: sim/ names `fetch` — that is the network, and sim/ promises none of '
      'it. Take the value as an argument instead, or add it to ALLOWED_ENVIRONMENT with '
      'the reason.']),

    ('rule4 the wall clock',
     {'sim/a.js': 'const t = Date.now();\n'},
     ['sim/a.js:1: sim/ names `Date` — that is the wall clock, and sim/ promises none of '
      'it. Take the value as an argument instead, or add it to ALLOWED_ENVIRONMENT with '
      'the reason.']),

    ('rule4 entropy outside the one place that is allowed it',
     {'sim/jitter.js': 'const r = Math.random();\n',
      'sim/rng.js': 'export let SEED = String(Math.floor(Math.random() * 1e9));\n'},
     ['sim/jitter.js:1: sim/ names `Math.random` — that is unseeded entropy, and sim/ '
      'promises none of it. Take the value as an argument instead, or add it to '
      'ALLOWED_ENVIRONMENT with the reason.']),

    ('rule4 the allowance is per file, not per identifier',
     {'sim/rng.js': 'const t = Date.now();\n'},
     ['sim/rng.js:1: sim/ names `Date` — that is the wall clock, and sim/ promises none '
      'of it. Take the value as an argument instead, or add it to ALLOWED_ENVIRONMENT '
      'with the reason.']),

    ('rule4 ignores members of other objects and mentions in prose',
     {'sim/a.js': '// nothing here touches document, window or fetch\n'
                  'const w = state.window, d = m.document;\n'
                  'const msg = `no location here`;\n'},
     []),

    ('rule4 applies to sim/ only: the 3D library is a renderer',
     {'3d/a.js': 'const el = document.createElement("canvas");\n'
                 'requestAnimationFrame(tick);\n'},
     []),

    ('a tree with nothing wrong in it',
     {'sim/plan.js': "import { CFG } from './config.js';\nexport const f = () => CFG.rho;\n",
      'app/main.js': "import { f } from '../sim/index.js';\nplanTargets(m, heat);\nf();\n"},
     []),
]


def selftest(verbose: bool = False) -> list[str]:
    """Run every case. Returns the failures, empty if the linter behaves as documented."""
    failures: list[str] = []

    for name, files, expected in CASES:
        got = check_files(files)
        if sorted(got) != sorted(expected):
            failures.append(
                f"{name}\n    expected: {expected or '(clean)'}\n    got:      {got or '(clean)'}")
        elif verbose:
            print(f"  ok  {name}")

    # The mask in specifiers() assumes the stripper is length-preserving. If that ever
    # stops being true, rule 1 starts reading the wrong character and silently ignores
    # real imports, so it is asserted rather than trusted.
    sample = ('import { a } from "./x.js"; // `t` \n'
              '/* "s" */ const r = /[&<>"]/g, s = \'q\\\'q\';\n'
              'const t = `lit ${ f("x") } end`;\n')
    if len(strip_comments_and_strings(sample)) != len(sample):
        failures.append('strip_comments_and_strings changed the length of its input; the '
                        'comment/string mask rule 1 depends on is no longer aligned')

    if verbose and not failures:
        print(f"  ok  strip_comments_and_strings preserves length")
    return failures


def main(argv: list[str]) -> int:
    only_selftest = '--selftest' in argv[1:]

    failures = selftest(verbose=only_selftest)
    if failures:
        print(f"{len(failures)} linter self-test failure(s) — the checker itself is wrong, "
              "so a clean tree would prove nothing:")
        for f in failures:
            print("  " + f)
        return 1
    if only_selftest:
        print(f"linter self-tests pass: {len(CASES)} cases")
        return 0

    files = {str(p.relative_to(ROOT)).replace('\\', '/'): p.read_text() for p in js_files()}
    problems = check_files(files)

    if problems:
        print(f"{len(problems)} boundary violation(s):")
        for p in problems:
            print("  " + p)
        return 1
    print(f"boundaries clean: {len(files)} modules, {len(CASES)} linter self-tests")
    print("  sim/ and 3d/ name nothing outside themselves — static import, re-export or "
          "dynamic import;")
    print("  sim/ additionally touches no DOM, network, storage, wall clock or location.")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
