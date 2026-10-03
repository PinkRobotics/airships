#!/usr/bin/env python3
"""Check tracked Markdown/HTML links and anchors without fetching external URLs."""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

from linkparse import anchors, parse_links

ROOT = Path(__file__).resolve().parent.parent


def tracked_documents(root):
    result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z'],
                            check=True, capture_output=True)
    return [Path(p) for p in result.stdout.decode().split('\0') if p and
            Path(p).suffix.lower() in ('.md', '.html') and (root / p).is_file()]


def check(root=ROOT, documents=None):
    root = root.resolve()
    documents = tracked_documents(root) if documents is None else documents
    errors, external, cache = [], [], {}
    for rel in sorted(documents):
        path = root / rel
        try:
            content = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append(f'{rel}: cannot read document ({type(exc).__name__})')
            continue
        for link in parse_links(content, path.suffix.lower(), repository=True):
            try:
                parsed = urlsplit(link)
            except ValueError:
                errors.append(f'{rel}: invalid URL: {link}')
                continue
            if parsed.scheme or parsed.netloc:
                external.append(f'{rel} -> {link}')
                continue
            target = ((root / unquote(parsed.path).lstrip('/')) if parsed.path.startswith('/')
                      else (path.parent / unquote(parsed.path)) if parsed.path else path).resolve()
            if root not in (target, *target.parents):
                errors.append(f'{rel}: link escapes tree: {link}')
                continue
            if not target.exists():
                errors.append(f'{rel}: broken link: {link}')
                continue
            if not parsed.fragment:
                continue
            if target.is_dir():
                target = next((target / n for n in ('index.html', 'README.md')
                               if (target / n).is_file()), target)
            if target not in cache:
                try:
                    cache[target] = anchors(target.read_text(encoding='utf-8'), target.suffix.lower())
                except (OSError, UnicodeError):
                    cache[target] = set()
            if unquote(parsed.fragment) not in cache[target]:
                errors.append(f'{rel}: broken anchor: {link}')
    return errors, sorted(set(external))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    args = ap.parse_args()
    try:
        documents = tracked_documents(args.root)
        errors, external = check(args.root, documents)
    except (OSError, UnicodeError, subprocess.SubprocessError) as exc:
        print(f'linkcheck: FAIL ({type(exc).__name__})')
        return 1
    for link in external:
        print(f'external (not fetched): {link}')
    for error in errors:
        print(error)
    print(f'linkcheck: {"FAIL" if errors else "PASS"}: {len(documents)} documents, '
          f'{len(errors)} errors, {len(external)} external links listed; no network requests')
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
