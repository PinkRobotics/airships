"""Shared local-link parsing for package notices and repository documentation.

Package mode preserves noticecheck's original parsing contract. Repository mode also
reads images, reference links and embedded HTML, and ignores Markdown code examples.
Neither mode fetches a URL.
"""
from html import unescape
from html.parser import HTMLParser
import re
import unicodedata


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('href', 'src', 'poster') and value:
                self.links.append(value)
            if key in ('id', 'name') and value:
                self.anchors.add(value)


def prose(content, *, inline=True):
    """Blank code and comments while retaining line boundaries for headings."""
    content = re.sub(r'<!--.*?-->', '', content, flags=re.S)
    lines, fence = [], None
    for line in content.splitlines(keepends=True):
        match = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= len(fence):
                fence = None
            lines.append('\n')
        elif match:
            fence = match[1]
            lines.append('\n')
        elif line.startswith(('    ', '\t')):
            # Indented code is not rendered as links or headings.
            lines.append('\n')
        else:
            lines.append(line)
    result = ''.join(lines)
    if inline:
        result = re.sub(r'(`+)(?!`)(.+?)(?<!`)\1(?!`)', '', result, flags=re.S)
    return result


def destination(text, start):
    """Read a Markdown destination, including balanced parentheses and escapes."""
    i = start
    while i < len(text) and text[i].isspace():
        i += 1
    if i < len(text) and text[i] == '<':
        end = text.find('>', i + 1)
        return text[i + 1:end] if end >= 0 else None
    value, depth = [], 0
    while i < len(text):
        c = text[i]
        if c == '\\' and i + 1 < len(text):
            value.append(text[i + 1]); i += 2; continue
        if c == '(':
            depth += 1
        elif c == ')':
            if depth == 0:
                break
            depth -= 1
        elif c.isspace() and depth == 0:
            break
        value.append(c); i += 1
    return ''.join(value)


def reference_id(label):
    return ' '.join(label.split()).casefold()


def parse_links(content, suffix, *, repository=False):
    if suffix == '.html':
        parser = Links(); parser.feed(content)
        return parser.links
    if not repository:
        return re.findall(r'(?<!!)\[[^]]+\]\(([^)]+)\)', content)
    body = prose(content)
    definitions = {}
    for m in re.finditer(r'^ {0,3}\[([^]\n]+)\]:\s*(.*)$', body, re.M):
        definitions.setdefault(reference_id(m[1]), destination(m[2], 0))
    body = re.sub(r'^ {0,3}\[[^]\n]+\]:.*$', '', body, flags=re.M)
    links = []
    pattern = r'(?<!!)(!?)\[((?:\\.|[^\[\]]|\[[^\[\]]*\])+)\](?:\[([^]\n]*)\])?'
    # Overlapping matches retain the image source inside a linked image.
    for match in re.finditer('(?=(' + pattern + '))', body):
        if match.start() and body[match.start() - 1] == ']' and not match[2]:
            continue  # the second bracket of an explicit reference, not a shortcut
        end = match.end(1)
        if end < len(body) and body[end] == '(':
            target = destination(body, end + 1)
        else:
            target = definitions.get(reference_id(match[4] or match[3]))
        if target is not None:
            links.append(unescape(target))
    parser = Links(); parser.feed(body)
    links.extend(parser.links)
    links.extend(re.findall(r'<((?:[A-Za-z][A-Za-z0-9+.-]*:|//)[^<>\s]+)>', body))
    return links


def heading_slug(text):
    text = re.sub(r'!?(\[([^]]*)\])\([^)]*\)', r'\2', text)
    text = re.sub(r'<[^>]*>', '', text)
    text = unescape(text).lower().replace('`', '')
    # GitHub preserves hyphens and underscores, drops other punctuation/symbols.
    text = ''.join(c for c in text if c in '-_' or c.isspace() or
                   unicodedata.category(c)[0] in ('L', 'N', 'M'))
    return text.replace(' ', '-')


def anchors(content, suffix):
    body = prose(content, inline=False) if suffix == '.md' else content
    parser = Links(); parser.feed(body)
    found = set(parser.anchors)
    if suffix != '.md':
        return found
    used = set()
    lines = body.splitlines()
    for i, line in enumerate(lines):
        atx = re.match(r'^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$', line)
        setext = (i + 1 < len(lines) and line.strip() and
                  re.fullmatch(r' {0,3}(?:=+|-+)\s*', lines[i + 1]))
        if not atx and not setext:
            continue
        base = heading_slug(atx[1] if atx else line.strip())
        slug, n = base, 0
        while slug in used:
            n += 1; slug = f'{base}-{n}'
        used.add(slug); found.add(slug)
    return found
