#!/usr/bin/env python3
"""Render the three float documents into the three published float pages.

    python3 tools/gen_float_pages.py --write    write the pages under float/
    python3 tools/gen_float_pages.py --check    render again and compare; exit 1 on a difference

WHY PAGES. The site publishes pages; docs/ stays in the source tree. Served pages link the
float case, its ledger and the member census, so each of the three gets a page under float/:

    docs/FLOAT.md          ->  float/index.html
    docs/FLOAT-LEDGER.md   ->  float/ledger.html
    docs/MEMBER-CENSUS.md  ->  float/census.html

A page says what its document says. Inside <main> no word and no figure is changed, added or
dropped; `--check` holds the committed pages to a fresh render, byte for byte, and refuses any
other file under float/. A page is never edited by hand: edit the document, then write again.

WHAT IS RENDERED is the part of Markdown these three documents use, measured by reading them.
Blocks: headings to the third level, paragraphs, block quotes of one paragraph, tight flat
lists with "- " or "1. " markers, pipe tables, fenced and indented code, the rule "---" and
one details block. Inline: code spans, strong and plain emphasis written with stars, and
links. On any other construct the tool stops and prints the file and the line. It never
guesses, because a guess is a changed word. Where two readers of Markdown would disagree, it
stops as well.

One malformed shape is measured and allowed: a table whose rule line is one cell longer than
its header and its rows. The table is rendered by its header, and every run prints the line.

LINKS. A link among the three documents becomes a link among the three pages. A link to a
file that dist.manifest serves stays a link. A link to any other file becomes its own words
followed by the path in code style, and is counted. Heading ids follow GitHub's scheme, so a
fragment that works on the document works on the page; a fragment with no heading stops.

The output holds no date, no script, no request and no font of its own. Standard library only.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import html
from pathlib import Path
import posixpath
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent.parent
PAGES = (('docs/FLOAT.md', 'float/index.html', 'Float case'),
         ('docs/FLOAT-LEDGER.md', 'float/ledger.html', 'Float ledger'),
         ('docs/MEMBER-CENSUS.md', 'float/census.html', 'Member census'))
PAGE_OF = {doc: page for doc, page, _ in PAGES}
DOC_OF = {page: doc for doc, page, _ in PAGES}

# The look is the notices page's: the same tokens, type and footer. Tables keep their natural
# width and scroll inside their own container, so the page body never scrolls sideways. A short
# cell stays on one line, so a figure is never broken; a cell of more than WRAP characters wraps.
WRAP = 28
STYLE = '''\
:root{color-scheme:dark;--bg:#101014;--text:#ded9cd;--muted:#b0aeb9;--warm:#ff75b4;--line:#42424c}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 system-ui,sans-serif;
overflow-wrap:break-word}
main,header,footer{max-width:1240px;margin:auto;padding:24px}
h1{font-size:clamp(30px,5vw,48px);line-height:1.15}
h2{font-size:clamp(22px,3.4vw,30px);line-height:1.2;margin-top:2em}
h3{font-size:19px;line-height:1.3;margin-top:1.8em}
p,li,blockquote{max-width:85ch}a{color:var(--warm);text-underline-offset:3px}
header nav{margin-top:14px}header nav a[aria-current]{color:var(--text);font-weight:600}
.from{font-size:14px;color:var(--muted);margin-bottom:0}
code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.9em}
pre{overflow-x:auto;padding:14px 16px;border:1px solid var(--line)}
blockquote{margin:1.2em 0;padding:2px 0 2px 18px;border-left:3px solid var(--line)}
hr{border:0;border-top:1px solid var(--line);margin:2.4em 0}
.tablewrap{overflow-x:auto;margin:1.2em 0}
.tablewrap:focus-visible{outline:2px solid var(--warm);outline-offset:2px}
table{border-collapse:collapse;width:max-content;max-width:max(100%,46rem);font-size:15px;
line-height:1.45}
th,td{vertical-align:top;text-align:left;padding:10px 12px;border-top:1px solid var(--line)}
th{font-weight:600;vertical-align:bottom}td{white-space:nowrap}
td.w{white-space:normal;min-width:24ch}
.r{text-align:right}
details{margin:1.2em 0}summary{cursor:pointer;color:var(--warm)}
footer{border-top:1px solid var(--line)}
@media(max-width:900px){main,header,footer{padding:20px}th,td{padding:8px 10px}}
'''

BLOCK_START = re.compile(r'#|>|\||```|~~~|<|[-*+] |\d+[.)] | ')
RULE_LINE = re.compile(r'\|(?: *:?-+:? *\|)+')
REFERENCE = re.compile(r'&(?:[A-Za-z][A-Za-z0-9]*|#[0-9]+|#[xX][0-9A-Fa-f]+);')
ADDRESS = re.compile(r'(?i)\b(?:https?|ftp)://|\bwww\.|\b(?:mailto|xmpp):'
                     r'|[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+')


class Unknown(Exception):
    """A construct outside the measured subset, named by file and line."""

    def __init__(self, file: str, line: int, what: str):
        super().__init__(f'{file}:{line}: {what}')


@dataclass(frozen=True)
class Page:
    html: str
    kept: int               # links that stayed links
    as_text: int            # links rendered as their words and a path
    long_rules: tuple = ()  # lines of a table rule one cell longer than its table


@dataclass
class Mark:
    """A run of stars that can open or close emphasis."""
    count: int
    opens: bool
    closes: bool
    line: int
    length: int = 0
    closing: list = field(default_factory=list)
    opening: list = field(default_factory=list)


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def bracket_end(text: str, start: int) -> int:
    """The index of the ] that closes the [ at `start`, past code spans and nested pairs."""
    depth, i = 0, start + 1
    while i < len(text):
        if text[i] == '`':
            i = text.find('`', i + 1)
            if i < 0:
                return -1
        elif text[i] == '[':
            depth += 1
        elif text[i] == ']':
            if not depth:
                return i
            depth -= 1
        i += 1
    return -1


def published(root: Path) -> set[str]:
    """Every file dist.manifest serves, selected as tools/publish.py selects them."""
    served, partial = set(), set()
    for raw in (root / 'dist.manifest').read_text(encoding='utf-8').split('\n'):
        parts = raw.strip().split(None, 2)
        if len(parts) < 2 or parts[0].startswith('#'):
            continue
        if parts[0] == 'served':
            served.add(parts[1])
        elif parts[0] == 'PARTIAL':
            partial.add(parts[1])
    files = set()
    for name in served:
        source = root / name
        if source.is_file():
            files.add(name)
            continue
        for path in source.rglob('*'):
            rel = path.relative_to(root).as_posix()
            if (path.is_file() and '__pycache__' not in path.parts and path.name != '.DS_Store'
                    and not any(rel == x or rel.startswith(x + '/') for x in partial)):
                files.add(rel)
    return files


def flanks(text: str, start: int, end: int, edges: str, symbols: bool) -> tuple[bool, bool]:
    """Whether the run text[start:end] is left-flanking and right-flanking (CommonMark 6.2).

    `edges` holds the character before the text and the one after it. `symbols` chooses the
    newer definition of punctuation, which adds the Unicode symbol categories."""
    before = text[start - 1] if start else edges[0]
    after = text[end] if end < len(text) else edges[1]

    def mark(ch: str) -> bool:
        kinds = ('P', 'S') if symbols else ('P',)
        return (ch.isascii() and not ch.isalnum() and not ch.isspace()) or \
            unicodedata.category(ch).startswith(kinds)

    left = not after.isspace() and (not mark(after) or before.isspace() or mark(before))
    right = not before.isspace() and (not mark(before) or after.isspace() or mark(after))
    return left, right


class Document:
    """One document being rendered: its counts, its heading ids and its open questions."""

    def __init__(self, root: Path, doc: str, live: set[str]):
        self.root, self.doc, self.live = root, doc, live
        self.kept = self.as_text = 0
        self.title = None
        self.ids: list[str] = []
        self.bases: dict[str, int] = {}
        self.fragments: list[tuple[int, str, str]] = []
        self.long_rules: list[int] = []

    def stop(self, line: int, what: str):
        raise Unknown(self.doc, line, what)

    # ---- inline text ------------------------------------------------------------------------

    def link(self, words: str, dest: str, line: int) -> str:
        if not dest or re.search(r'''[\s<>"'()\\]''', dest):
            self.stop(line, 'a link destination with a space, a title, a bracket or a backslash')
        if re.match(r'[A-Za-z][A-Za-z0-9+.-]*:|/', dest):
            self.stop(line, 'a link with a scheme or a rooted path; measured links are relative')
        path, _, fragment = dest.partition('#')
        if not path:
            self.stop(line, 'a link to a heading of its own document')
        target = posixpath.normpath(posixpath.join(posixpath.dirname(self.doc), path))
        if target.startswith('..'):
            self.stop(line, 'a link that leaves the repository')
        inner = self.inline(words, line, edges='[]', inside_link=True)
        if target in PAGE_OF:
            href = posixpath.basename(PAGE_OF[target])
            if fragment:
                self.fragments.append((line, PAGE_OF[target], fragment))
                href += '#' + fragment
        elif fragment:
            self.stop(line, 'a fragment on a link to a file outside the three documents')
        elif target in self.live:
            href = posixpath.relpath(target, 'float')
        elif (self.root / target).is_file():
            self.as_text += 1
            return f'{inner} (<code>{esc(target)}</code>)'
        else:
            self.stop(line, f'a link to {target}, which is not a file in this tree')
        self.kept += 1
        return f'<a href="{html.escape(href)}">{inner}</a>'

    def inline(self, text: str, line: int, edges: str = '  ', inside_link: bool = False) -> str:
        """Render inline Markdown; `line` is the line of the first character."""
        def at(offset: int) -> int:
            return line + text.count('\n', 0, offset)

        address = ADDRESS.search(re.sub(r'`[^`\n]*`', lambda m: ' ' * len(m.group()), text))
        if address:
            self.stop(at(address.start()), 'an address that a Markdown reader would make a link')
        out, i, size = [], 0, len(text)
        while i < size:
            ch = text[i]
            if ch == '`':
                close = text.find('`', i + 1)
                if close < 0:
                    self.stop(at(i), 'a backtick without its closing backtick')
                if text.startswith('``', i) or text.startswith('``', close):
                    self.stop(at(i), 'a code span fenced by more than one backtick')
                code = text[i + 1:close].replace('\n', ' ')
                if len(code) > 1 and code[0] == code[-1] == ' ' and code.strip(' '):
                    code = code[1:-1]
                out.append(f'<code>{esc(code)}</code>')
                i = close + 1
            elif ch == '[':
                close = bracket_end(text, i)
                follows = text[close + 1:close + 2] if close > 0 else ''
                if follows not in ('(', '['):
                    out.append('[')         # no link follows: the bracket is a character
                    i += 1
                    continue
                end = text.find(')', close + 2)
                if follows == '[' or end < 0 or inside_link or (i and text[i - 1] == '!'):
                    self.stop(at(i), 'an image, a reference link, a link inside a link, '
                                     'or a link that does not close')
                out.append(self.link(text[i + 1:close], text[close + 2:end], at(i)))
                i = end + 1
            elif ch in '*~':
                end = i
                while end < size and text[end] == ch:
                    end += 1
                opens, closes = flanks(text, i, end, edges, False)
                if (opens, closes) != flanks(text, i, end, edges, True):
                    self.stop(at(i), f'a {ch} beside a symbol; two editions of the rules read it '
                                     'differently')
                if ch == '~':
                    if end - i > 1 or closes:
                        self.stop(at(i), 'a tilde that could mark struck-through text')
                    out.append('~')
                elif not (opens or closes):
                    out.append('*' * (end - i))     # a star with a space on both sides
                else:
                    out.append(Mark(end - i, opens, closes, at(i), end - i))
                i = end
            elif ch == '_':
                before = text[i - 1] if i else ' '
                after = text[i + 1] if i + 1 < size else ' '
                if not (before.isalnum() and after.isalnum()):
                    self.stop(at(i), 'an underscore that is not inside a word')
                out.append('_')
                i += 1
            elif ch == '&':
                reference = REFERENCE.match(text, i)
                if reference and reference.group() not in ('&lt;', '&gt;'):
                    self.stop(at(i), f'the character reference {reference.group()}')
                out.append(reference.group() if reference else '&amp;')
                i = reference.end() if reference else i + 1
            elif ch == '\\':
                self.stop(at(i), 'a backslash outside code and outside a table cell')
            elif ch == '<':
                self.stop(at(i), 'an angle bracket that opens raw markup')
            else:
                out.append('&gt;' if ch == '>' else ch)
                i += 1
        return self.emphasis(out)

    def emphasis(self, out: list) -> str:
        """Pair the star runs as CommonMark's delimiter rules do; an unpaired run stops."""
        marks = [item for item in out if isinstance(item, Mark)]
        at = 0
        while at < len(marks):
            closer = marks[at]
            opener_at = at - 1
            while closer.closes and opener_at >= 0:
                opener = marks[opener_at]
                odd = ((closer.opens or opener.closes) and closer.length % 3
                       and (opener.length + closer.length) % 3 == 0)
                if opener.opens and not odd:
                    break
                opener_at -= 1
            if not closer.closes or opener_at < 0:
                at += 1
                continue
            width = 2 if opener.count >= 2 and closer.count >= 2 else 1
            tag = 'strong' if width == 2 else 'em'
            opener.count -= width
            closer.count -= width
            opener.opening.insert(0, f'<{tag}>')
            closer.closing.append(f'</{tag}>')
            for skipped in marks[opener_at + 1:at]:
                self.stop(skipped.line, 'a star that pairs with nothing')
            if opener.count == 0:
                del marks[opener_at]
                at -= 1
            if closer.count == 0:
                del marks[at]
        for left in marks:
            self.stop(left.line, 'a star that pairs with nothing')
        return ''.join(item if isinstance(item, str) else ''.join(item.closing + item.opening)
                       for item in out)

    def prose(self, text: str, line: int) -> str:
        """The words of a paragraph, a list item or a quotation."""
        if re.match(r'\[[^\]\n]+\]:', text):
            self.stop(line, 'a link reference definition')
        return self.inline(text, line)

    # ---- blocks -----------------------------------------------------------------------------

    def heading_id(self, inner: str, line: int) -> str:
        """GitHub's scheme: lower case, drop punctuation, spaces to hyphens, number repeats."""
        kept = []
        for ch in html.unescape(re.sub(r'<[^>]+>', '', inner)).lower():
            if ch == ' ':
                kept.append('-')
            elif ch in '-_' or (ch.isascii() and ch.isalnum()):
                kept.append(ch)
            elif not ch.isascii() and ch != '—':
                self.stop(line, f'a heading character outside the measured set (U+{ord(ch):04X})')
        base = ''.join(kept)
        seen = self.bases.get(base, 0)
        self.bases[base] = seen + 1
        name = f'{base}-{seen}' if seen else base
        if not base or name in self.ids:
            self.stop(line, 'a heading whose id is empty or already taken')
        self.ids.append(name)
        return name

    def cells(self, row: str, line: int) -> list[str]:
        if len(row) < 2 or not row.endswith('|') or row.endswith('\\|'):
            self.stop(line, 'a table row without its closing pipe')
        return [cell.strip().replace('\\|', '|') for cell in re.split(r'(?<!\\)\|', row[1:-1])]

    def table(self, lines: list[str], i: int) -> tuple[str, int]:
        line = i + 1
        header = self.cells(lines[i], line)
        if i + 1 >= len(lines) or not RULE_LINE.fullmatch(lines[i + 1]):
            self.stop(line, 'a table row with no rule line under it')
        rules = self.cells(lines[i + 1], line + 1)
        if len(rules) == len(header) + 1 and re.fullmatch(r'-+', rules[-1]):
            # Measured once: a rule line one cell longer than its header and its rows. The
            # cell holds no word and no alignment, so the table is rendered by its header,
            # and every run names the line until the document is corrected.
            self.long_rules.append(line + 1)
            rules.pop()
        if len(rules) != len(header):
            self.stop(line + 1, 'a rule line whose cell count differs from the row above it')
        right = []
        for rule in rules:
            if not re.fullmatch(r'-+:?', rule):
                self.stop(line + 1, 'a column alignment other than the measured left and right')
            right.append(rule.endswith(':'))
        # A header cell with no words heads nothing, so it is a plain cell.
        head = ['<th scope="col"' + (' class="r">' if side else '>') + self.inline(cell, line)
                + '</th>' if cell else '<td></td>' for cell, side in zip(header, right)]
        # The container scrolls sideways on a narrow screen. It takes keyboard focus so that
        # it can be scrolled without a pointer, and it is named by the heading it sits under.
        wrap = f'<div class="tablewrap" role="group" aria-labelledby="{self.ids[-1]}" tabindex="0">'
        out = [wrap, '<table>', '<thead>', '<tr>', *head, '</tr>', '</thead>']
        j, body = i + 2, []
        while j < len(lines) and lines[j].startswith('|'):
            row = self.cells(lines[j], j + 1)
            if len(row) != len(header):
                self.stop(j + 1, f'a table row of {len(row)} cells under a header of {len(header)}')
            body.append('<tr>')
            for cell, side in zip(row, right):
                inner = self.inline(cell, j + 1)
                long = len(html.unescape(re.sub(r'<[^>]+>', '', inner))) > WRAP
                names = ' '.join(name for name, on in (('r', side), ('w', long)) if on)
                body.append(f'<td class="{names}">{inner}</td>' if names else f'<td>{inner}</td>')
            body.append('</tr>')
            j += 1
        if body:
            out += ['<tbody>', *body, '</tbody>']
        return '\n'.join(out + ['</table>', '</div>']), j

    def listing(self, lines: list[str], i: int) -> tuple[str, int]:
        ordered = lines[i][0].isdigit()
        items, j = [], i
        while j < len(lines):
            row = lines[j]
            item = re.fullmatch(r'(\d+\. |- )(\S.*)', row)
            if item and item.group(1)[0].isdigit() == ordered:
                marker, words = item.groups()
                if ordered and marker != f'{len(items) + 1}. ':
                    self.stop(j + 1, 'a list number out of sequence; a list counts from 1')
                if BLOCK_START.match(words) or re.match(r'\[[ xX]\] ', words):
                    self.stop(j + 1, 'a list item that opens another block, or a task item')
                items.append((j + 1, len(marker), [words]))
            elif (items and row.startswith(' ' * items[-1][1])
                  and not BLOCK_START.match(row[items[-1][1]:] or ' ')):
                items[-1][2].append(row[items[-1][1]:])
            else:
                break
            j += 1
        if not items:
            self.stop(i + 1, 'a list marker other than the measured two, "- " and "1. "')
        tag = 'ol' if ordered else 'ul'
        rows = [f'<li>{self.prose(chr(10).join(text), line)}</li>' for line, _, text in items]
        return '\n'.join([f'<{tag}>', *rows, f'</{tag}>']), j

    def paragraph(self, lines: list[str], i: int) -> tuple[str, int]:
        end = i + 1
        while end < len(lines) and lines[end] != '':
            row = lines[end]
            if re.fullmatch(r'=+|[ |:-]*-[ |:-]*', row):
                self.stop(end + 1, 'a heading made by underlining, or a table without its pipes')
            if re.match(r'1\. \S', row):
                break               # measured: a numbered list directly under a paragraph
            if BLOCK_START.match(row):
                self.stop(end + 1, 'a block directly under a paragraph line')
            end += 1
        return '<p>' + self.prose('\n'.join(lines[i:end]), i + 1) + '</p>', end

    def body(self, text: str) -> str:
        lines = text.split('\n')
        if lines[-1] != '' or '\r' in text:
            self.stop(len(lines), 'a file with a carriage return, or without a last line feed')
        lines.pop()
        for number, raw in enumerate(lines, 1):
            if '\t' in raw or raw != raw.rstrip():
                self.stop(number, 'a tab, or white space at the end of a line (a forced break)')
        out, i, blank, last, details = [], 0, True, '', 0
        while i < len(lines):
            raw, line = lines[i], i + 1
            if raw == '':
                blank, i = True, i + 1
                continue
            if not blank and not (last == 'p' and re.match(r'1\. \S', raw)):
                self.stop(line, 'a block directly under another; the measured form has a blank '
                                'line between')
            if self.title is None and not raw.startswith('# '):
                self.stop(line, 'a document that does not open with its first-level heading')
            if raw.startswith(('```', '~~~')):
                if not re.fullmatch(r'```[A-Za-z0-9]*', raw):
                    self.stop(line, 'a code fence of an unmeasured shape')
                end = i + 1
                while end < len(lines) and not lines[end].startswith('```'):
                    end += 1
                if end == len(lines) or lines[end] != '```':
                    self.stop(line, 'a code fence that does not close with a plain fence line')
                code = ''.join(esc(row) + '\n' for row in lines[i + 1:end])
                out.append(f'<pre><code>{code}</code></pre>')
                i, kind = end + 1, 'fence'
            elif raw.startswith('#'):
                head = re.fullmatch(r'(#{1,3}) (\S.*)', raw)
                if not head or re.search(r' #+$', raw):
                    self.stop(line, 'a heading below the third level, or of an unmeasured shape')
                level, inner = len(head.group(1)), self.inline(head.group(2), line)
                if level == 1 and self.title is not None:
                    self.stop(line, 'a second first-level heading')
                self.title = self.title or html.unescape(re.sub(r'<[^>]+>', '', inner))
                out.append(f'<h{level} id="{self.heading_id(inner, line)}">{inner}</h{level}>')
                i, kind = i + 1, 'h'
            elif re.fullmatch(r'[-*_ ]{3,}', raw):
                if raw != '---':
                    self.stop(line, 'a rule written other than as three hyphens')
                out.append('<hr>')
                i, kind = i + 1, 'hr'
            elif raw.startswith('>'):
                end, rows = i, []
                while end < len(lines) and lines[end].startswith('>'):
                    row = lines[end][2:]
                    if not lines[end].startswith('> ') or BLOCK_START.match(row or ' '):
                        self.stop(end + 1, 'a quotation line that is not plain paragraph text')
                    rows.append(row)
                    end += 1
                words = self.prose('\n'.join(rows), line)
                out.append(f'<blockquote>\n<p>{words}</p>\n</blockquote>')
                i, kind = end, 'quote'
            elif raw.startswith('|'):
                block, i = self.table(lines, i)
                out.append(block)
                kind = 'table'
            elif raw.startswith('<'):
                summary = re.fullmatch(r'<details><summary>([^<>&`*_~\[\]\\]+)</summary>', raw)
                if summary and not details:
                    details = line
                    out.append(f'<details>\n<summary>{esc(summary.group(1))}</summary>')
                elif raw == '</details>' and details:
                    details = 0
                    out.append('</details>')
                else:
                    self.stop(line, 'raw markup other than the one measured details block')
                i, kind = i + 1, 'details'
            elif re.match(r'(?:[-*+]|\d+[.)])(?: |$)', raw):
                block, i = self.listing(lines, i)
                kind = block[1:3]
                if kind == last and blank:
                    self.stop(line, 'a blank line inside a list')
                out.append(block)
            elif raw.startswith(' '):
                end = i
                while end < len(lines) and lines[end].startswith('    '):
                    end += 1
                if end == i or last in ('ul', 'ol', 'code'):
                    self.stop(line, 'an indented line that is not a measured code block')
                code = ''.join(esc(row[4:]) + '\n' for row in lines[i:end])
                out.append(f'<pre><code>{code}</code></pre>')
                i, kind = end, 'code'
            else:
                block, i = self.paragraph(lines, i)
                out.append(block)
                kind = 'p'
            blank, last = False, kind
        if details:
            self.stop(details, 'a details block that never closes')
        if self.title is None:
            self.stop(1, 'a document with no first-level heading')
        return '\n'.join(out)


def frame(doc: str, page: str, title: str, body: str) -> str:
    row = ' · '.join(f'<a href="{posixpath.basename(other)}"'
                     + (' aria-current="page"' if other == page else '') + f'>{name}</a>'
                     for _, other, name in PAGES)
    return '\n'.join([
        '<!doctype html>',
        f'<!-- Rendered from {doc} by tools/gen_float_pages.py. Edit the document, then run: '
        'make floatpages -->',
        '<html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        f'<title>{esc(title)} — Pink Robotics</title>',
        '<style>',
        f'{STYLE}</style></head><body><header><a href="../">← Fleet monitor</a>',
        f'<nav aria-label="Float case pages">{row}</nav>',
        f'<p class="from">This page is rendered from <code>{doc}</code>. '
        'Paths printed in code style name files of the project’s source.</p></header>',
        '<main>',
        body,
        '</main><footer><a href="../">Fleet monitor</a> · '
        '<a href="../notices.html">Data, licences and notices</a> · '
        '<a href="../LICENSE">Code licence</a></footer></body></html>',
        ''])


def render(root: Path = ROOT) -> dict[str, Page]:
    """Render all three documents, then confirm every fragment names a heading of its page."""
    live = published(root)
    parsed = {}
    for doc, page, _ in PAGES:
        document = Document(root, doc, live)
        parsed[page] = (document, document.body((root / doc).read_text(encoding='utf-8')))
    for document, _ in parsed.values():
        for line, target, fragment in document.fragments:
            if fragment not in parsed[target][0].ids:
                document.stop(line, f'a link to #{fragment}; {DOC_OF[target]} has no such heading')
    return {page: Page(frame(document.doc, page, document.title, body), document.kept,
                       document.as_text, tuple(document.long_rules))
            for page, (document, body) in parsed.items()}


def check(root: Path = ROOT, rendered: dict[str, Page] | None = None) -> list[str]:
    rendered = rendered or render(root)
    live = published(root)
    problems = []
    for page, result in rendered.items():
        path = root / page
        if not path.is_file():
            problems.append(f'{page} is missing; it is rendered from {DOC_OF[page]}')
        elif path.read_bytes() != result.html.encode('utf-8'):
            problems.append(f'{page} differs from a fresh render of {DOC_OF[page]}')
        elif page not in live:
            problems.append(f'{page} is not served by dist.manifest')
    if (root / 'float').is_dir():
        for path in sorted((root / 'float').rglob('*')):
            rel = path.relative_to(root).as_posix()
            if path.is_file() and rel not in rendered:
                problems.append(f'{rel} is not written by the generator; '
                                'float/ holds the three pages only')
    return problems


def write(root: Path = ROOT, rendered: dict[str, Page] | None = None) -> list[str]:
    """Write the pages that differ and name them. Nothing is written if a document stops."""
    rendered = rendered or render(root)
    written = []
    for page, result in rendered.items():
        path, data = root / page, result.html.encode('utf-8')
        if not path.is_file() or path.read_bytes() != data:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            written.append(page)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true', help='write the three pages under float/')
    mode.add_argument('--check', action='store_true',
                      help='render again and compare; change nothing; exit 1 on any difference')
    parser.add_argument('--root', type=Path, default=ROOT, help='the tree to read and write')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        rendered = render(root)
    except Unknown as stopped:
        print(stopped, file=sys.stderr)
        print('gen_float_pages: stopped on a construct it does not know. Nothing was written.',
              file=sys.stderr)
        return 2
    except OSError as missing:
        print(f'gen_float_pages: cannot read {missing.filename}', file=sys.stderr)
        return 2
    problems = [] if args.write else check(root, rendered)
    for problem in problems:
        print(problem)
    if problems:
        print('floatpagecheck: FAIL. Edit the document, never the page; then run: make floatpages')
        return 1
    written = write(root, rendered) if args.write else []
    for page, result in rendered.items():
        state = ' (written)' if page in written else ''
        print(f'{page} from {DOC_OF[page]}: {result.kept} links kept, '
              f'{result.as_text} rendered as text{state}')
        for line in result.long_rules:
            print(f'  {DOC_OF[page]}:{line}: the rule line is one cell longer than its table; '
                  'rendered by the header row')
    print(f'float pages: {len(written)} of {len(rendered)} written' if args.write else
          f'floatpagecheck: {len(rendered)} pages equal a fresh render of their documents')
    return 0


if __name__ == '__main__':
    sys.exit(main())
