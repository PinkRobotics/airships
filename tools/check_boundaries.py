#!/usr/bin/env python3
"""Enforce the repository's two structural rules. Run by CI and by `make check`.

RULE 1 — the dependency direction.
    sim/ imports nothing outside sim/. 3d/ imports nothing outside 3d/. app/ may import
    both. concept/ may import sim/. Nothing imports app/.

    The model is the part of this project that invites argument, so it has to be readable
    and runnable on its own: the moment it imports a canvas or a fetch, "read the physics"
    becomes "read the whole site".

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

Exit status is non-zero on any violation, with the file and line.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# who may import whom, by top-level directory
ALLOWED = {
    'sim': {'sim'},
    '3d': {'3d'},
    'app': {'app', 'sim', '3d'},
    'concept': {'concept', 'sim', '3d'},
    'tests': {'tests', 'sim', '3d', 'app'},
    'model-lab': {'model-lab', '3d', 'sim'},
}

IMPORT = re.compile(r"""^\s*import\s+(?:(?P<what>[\w${},\s*]+?)\s+from\s+)?['"](?P<spec>[^'"]+)['"]""",
                    re.M)
ASSIGN = re.compile(r'(?<![.\w$])(?P<name>[A-Za-z_$][\w$]*)\s*(?:=(?!=)|\+\+|--|\+=|-=|\*=|/=)')

# Calls that must not rely on a default, and the area the rule applies to. The value is the
# smallest number of arguments a correct call has.
REQUIRED_ARGS = {'planTargets': ('app', 2)}
CALL = re.compile(r'(?<![.\w$])(?P<fn>[A-Za-z_$][\w$]*)\s*\((?P<args>[^()]*)\)', re.S)


def area_of(path: pathlib.Path) -> str:
    return path.relative_to(ROOT).parts[0]


def resolve(src: pathlib.Path, spec: str) -> pathlib.Path | None:
    if not spec.startswith('.'):
        return None
    return (src.parent / spec.split('?')[0]).resolve()


def js_files():
    for area in ('sim', 'app', '3d', 'concept', 'tests', 'model-lab'):
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


def main() -> int:
    problems: list[str] = []

    for path in js_files():
        rel = path.relative_to(ROOT)
        area = area_of(path)
        raw = path.read_text()
        code = strip_comments_and_strings(raw)

        imported: dict[str, str] = {}
        for m in IMPORT.finditer(raw):
            spec, what = m.group('spec'), (m.group('what') or '')
            target = resolve(path, spec)
            if target is not None:
                try:
                    t_area = target.relative_to(ROOT).parts[0]
                except ValueError:
                    problems.append(f"{rel}: imports outside the repository: {spec}")
                    continue
                if t_area not in ALLOWED.get(area, {area}):
                    problems.append(
                        f"{rel}: {area}/ must not import {t_area}/  ({spec})")
            if '{' in what:
                for tok in re.findall(r'[A-Za-z_$][\w$]*', what[what.index('{'):]):
                    if tok != 'as':
                        imported[tok] = spec

        if imported:
            for n, line in enumerate(code.split('\n'), 1):
                for m in ASSIGN.finditer(line):
                    name = m.group('name')
                    if name in imported:
                        problems.append(
                            f"{rel}:{n}: assigns to `{name}`, which it imported from "
                            f"{imported[name]} — ask that module to change it instead")

        for fn, (only_area, need) in REQUIRED_ARGS.items():
            if area != only_area:
                continue
            # Scan the whole file, not line by line: a call split across lines would
            # otherwise slip past the rule, and reformatting is not a code review.
            for m in CALL.finditer(code):
                n = code[:m.start()].count('\n') + 1
                if True:
                    if m.group('fn') != fn:
                        continue
                    args = [a for a in m.group('args').split(',') if a.strip()]
                    if len(args) < need:
                        problems.append(
                            f"{rel}:{n}: {fn}() called with {len(args)} argument(s); "
                            f"{area}/ must pass all {need}. The default is a silent "
                            "fallback, not a convenience.")

    if problems:
        print(f"{len(problems)} boundary violation(s):")
        for p in problems:
            print("  " + p)
        return 1
    print(f"boundaries clean: {sum(1 for _ in js_files())} modules, "
          f"sim/ and 3d/ depend on nothing outside themselves")
    return 0


if __name__ == '__main__':
    sys.exit(main())
