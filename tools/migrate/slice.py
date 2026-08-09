#!/usr/bin/env python3
"""Cut a single-file page into modules by moving exact source lines.

The point of doing this mechanically rather than by hand is that a move cannot mistype
anything: every byte of a function body arrives in its new file exactly as it left the
old one, and the diff of the whole reorganisation is verifiable by eye. Only the seams —
the `export` keyword, the import header — are new text.

A top-level declaration owns the comment block immediately above it, so the prose travels
with the code it describes. Comment ownership is decided by scanning for real `/* … */`
spans rather than by looking for `*` at the start of a line: a comment whose continuation
lines are indented prose (which most of the good ones here are) would otherwise be cut in
half, stranding its opening in the previous file and leaving both unparseable.
"""
from __future__ import annotations

import pathlib
import re
import sys

DECL = re.compile(r'^(?:async\s+)?(?:function|const|let|class)\s+([A-Za-z_$][\w$]*)')


def read_region(path: str, start_marker: str, end_marker: str):
    """The file's lines plus the indices of the two marker lines."""
    lines = pathlib.Path(path).read_text().split('\n')
    a = next(i for i, l in enumerate(lines) if start_marker in l)
    b = next(i for i, l in enumerate(lines) if end_marker in l)
    return lines, a, b


def classify(lines):
    """Per line: 'code', 'line-comment', 'blank', or ('block', open_index).

    A single pass with just enough lexer to not be fooled by `/*` inside a string or a
    `//` inside a URL. It does not need to be a full JavaScript tokeniser — it only has
    to agree with one about where comments begin and end.
    """
    kind = [None] * len(lines)
    in_block = False
    block_start = 0
    for i, line in enumerate(lines):
        if in_block:
            kind[i] = ('block', block_start)
            if '*/' in line:
                in_block = False
            continue
        j, n = 0, len(line)
        opened_here = False
        while j < n:
            c = line[j]
            if c in '"\'`':                                  # skip a string literal
                quote = c
                j += 1
                while j < n:
                    if line[j] == '\\':
                        j += 2
                        continue
                    if line[j] == quote:
                        break
                    j += 1
            elif c == '/' and j + 1 < n and line[j + 1] == '/':
                break                                        # rest of the line is comment
            elif c == '/' and j + 1 < n and line[j + 1] == '*':
                if '*/' not in line[j + 2:]:
                    in_block, block_start, opened_here = True, i, True
                    break
                j = line.index('*/', j + 2) + 1              # a comment that closes here
            j += 1
        if opened_here:
            kind[i] = ('block', i)
        elif not line.strip():
            kind[i] = 'blank'
        elif line.lstrip().startswith('//'):
            kind[i] = 'line-comment'
        else:
            kind[i] = 'code'
    return kind



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


def top_level_symbols(lines, a, b):
    """[(name, decl_index, block_start, block_end_exclusive)] for the region (a, b)."""
    kind = classify(lines)
    hits = [(m.group(1), i)
            for i in range(a + 1, b)
            if kind[i] == 'code' and (m := DECL.match(lines[i]))]

    starts = []
    for _, i in hits:
        s = i
        while s - 1 > a:
            k = kind[s - 1]
            if k == 'blank' or k == 'line-comment':
                s -= 1
            elif isinstance(k, tuple):                       # jump the whole block comment
                s = k[1]
            else:
                break
        while s < i and kind[s] == 'blank':                  # blanks belong to whoever is above
            s += 1
        starts.append(s)

    out = []
    for k, (name, i) in enumerate(hits):
        end = starts[k + 1] if k + 1 < len(hits) else b
        while end - 1 > i and not lines[end - 1].strip():
            end -= 1
        out.append((name, i, starts[k], end))
    return out


def main():
    lines, a, b = read_region(sys.argv[1], sys.argv[2], sys.argv[3])
    syms = top_level_symbols(lines, a, b)
    print(f"region lines {a + 1}..{b + 1}, {len(syms)} top-level symbols")
    covered = set()
    for name, i, s, e in syms:
        covered |= set(range(s, e))
        print(f"  {s + 1:5d}-{e:5d} ({e - s:4d} lines)  {name}")
    gap = [i for i in range(a + 1, b) if i not in covered and lines[i].strip()]
    if gap:
        print(f"\nUNCOVERED non-blank lines ({len(gap)}) — these need a home:")
        for i in gap[:40]:
            print(f"  {i + 1:5d}| {lines[i][:100]}")
        sys.exit(1)


if __name__ == '__main__':
    main()
