#!/usr/bin/env python3
"""Verify all repository third-party files and generated notices, without network access.

The folder rule and exact first-party exceptions are documented in research/papers/README.md.
--write generates NOTICE, DATA-SOURCES.md, notices.html and data/README.md only.
--public additionally refuses excluded files still present; --dest verifies a served copy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

import noticegen
from linkparse import Links, parse_links
from noticegen import esc, page

ROOT = Path(__file__).resolve().parent.parent
FOLDERS = ("data", "media", "research/papers", "research/prior")
# Exact paths, never a wildcard exemption for a new asset or a new README.
FIRST_PARTY = {
    "data/README.md": "Generated index, checked against sidecars",
    "data/live/README.md": "Project documentation of the unbundled server mirror",
    "media/README.md": "Project render documentation",
    "media/ballast.jpg": "Project WebGL model render; media/README.md",
    "media/drop.jpg": "Project WebGL model render; media/README.md",
    "media/intake.jpg": "Project WebGL model render; media/README.md",
    "media/vacuum.jpg": "Project WebGL model render; media/README.md",
    "research/papers/README.md": "Project provenance schema and classification rule",
}
DECISIONS = {"redistributed", "link-only", "withheld", "to-confirm"}
SERVICE_RECORD = "data/wind.prov.json"
DISPLAY = ("snapshot", "snapshot-heat", "water-bc", "terrain-bc", "roads-bc", "bc-outline", "wind")
CREDIT_START = "<!-- NOTICE-CREDIT START -->"
CREDIT_END = "<!-- NOTICE-CREDIT END -->"
REQUIRED = ("LICENSE", "NOTICE", "DATA-SOURCES.md", "notices.html")


def safe_path(value: object) -> bool:
    return (isinstance(value, str) and bool(value) and "\\" not in value and
            not PurePosixPath(value).is_absolute() and ".." not in value.split("/") and
            str(PurePosixPath(value)) == value)


def measure(path: Path, rel: str) -> dict:
    result = {"bytes": path.stat().st_size}
    if rel in {"data/roads-bc.json", "data/bc-outline.json"}:
        rows = json.loads(path.read_text())
        result.update({"polylines" if "roads" in rel else "rings": len(rows),
                       "vertices": sum(len(row) for row in rows)})
    elif rel == "data/snapshot.json":
        data = json.loads(path.read_text())
        result.update(fires=len(data["fires"]["features"]), perimeters=len(data["perimeters"]["features"]))
    elif rel == "data/snapshot-heat.json":
        result["hotspots"] = len(json.loads(path.read_text())["features"])
    elif rel == "data/water-bc.json":
        rows = json.loads(path.read_text())["water"]
        result.update(lakes=sum(r[3] == 0 for r in rows), reservoirs=sum(r[3] == 1 for r in rows))
    elif rel == "data/fire-history-bc.json":
        result["perimeters"] = len(json.loads(path.read_text())["fires"])
    return result


def inventory_paths(root: Path) -> set[str]:
    # Include tracked-but-deleted paths and untracked additions. A release export without
    # .git is scanned by the same folder rule using its actual files.
    paths = {p.relative_to(root).as_posix() for d in FOLDERS for p in (root / d).rglob("*")
             if p.is_file() or p.is_symlink()}
    if (root / ".git").exists():
        result = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached"],
                                capture_output=True, check=True)
        paths.update(p.decode("utf-8") for p in result.stdout.split(b"\0") if p)
    # Global font/vendor rule includes unstaged additions as well.
    for p in root.rglob("*"):
        if ".git" not in p.parts and (p.suffix.lower() in {".woff", ".woff2", ".ttf", ".otf"}
                                     or "vendor" in p.relative_to(root).parts):
            if p.is_file() or p.is_symlink():
                paths.add(p.relative_to(root).as_posix())
    return paths


def third_party(rel: str) -> bool:
    path = PurePosixPath(rel)
    if path.name.endswith(".prov.json"):
        return False
    if rel in FIRST_PARTY:
        return False
    return (any(rel.startswith(d + "/") for d in FOLDERS) or
            path.suffix.lower() in {".woff", ".woff2", ".ttf", ".otf"} or "vendor" in path.parts)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def records(root: Path) -> tuple[list[dict], list[str]]:
    errors, found = [], []
    paths = inventory_paths(root)
    sidecars = {p for p in paths if p.endswith(".prov.json") and
                any(p.startswith(d + "/") for d in FOLDERS)}
    for rel in paths:
        if third_party(rel):
            p = PurePosixPath(rel)
            for candidate in (rel + ".prov.json", str(p.with_suffix(".prov.json"))):
                if (root / candidate).is_file():
                    sidecars.add(candidate)
    for rel in sorted(sidecars):
        sidecar = root / rel
        if sidecar.is_symlink() or any(p.is_symlink() for p in sidecar.parents if p != root):
            errors.append(f"{rel}: symlink record refused")
            continue
        try:
            item = json.loads(sidecar.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        except (ValueError, OSError) as exc:
            errors.append(f"{rel}: invalid record ({type(exc).__name__})")
            continue
        if not isinstance(item, dict):
            errors.append(f"{rel}: record must be an object")
            continue
        invalid = False
        for key in ("file", "publisher", "licence", "licenceUrl", "licenceStatement", "licenceEvidence",
                    "licenceReason", "attribution", "notes"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{rel}: missing or invalid {key}")
                invalid = True
        src = item.get("source")
        if not (isinstance(src, str) and src.strip() or isinstance(src, list) and src and
                all(isinstance(s, str) and s.strip() for s in src)):
            errors.append(f"{rel}: missing or invalid source")
            invalid = True
        if not isinstance(item.get("decision"), str) or item["decision"] not in DECISIONS:
            errors.append(f"{rel}: missing or invalid decision")
            invalid = True
        if not safe_path(item.get("file")):
            errors.append(f"{rel}: invalid file path")
            invalid = True
        if invalid:
            continue
        item["sidecar"] = rel
        item["path"] = (PurePosixPath(rel).parent / item["file"]).as_posix()
        path = root / item["path"]
        kind = item.get("kind", "file")
        service = (rel == SERVICE_RECORD and kind == "service" and
                   item["path"] == "data/live/wind.json" and item["decision"] == "link-only")
        if kind != "file" and not service:
            errors.append(f"{rel}: unsupported kind or service identity")
        if service:
            if item.get("sha256", "missing") is not None or path.exists():
                errors.append(f"{rel}: service record must have null hash and no bundled file")
        elif not isinstance(item.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
            errors.append(f"{rel}: missing or invalid sha256")
        elif path.is_symlink() or any(p.is_symlink() for p in path.parents if p != root):
            errors.append(f"{rel}: symlink asset refused")
        elif path.is_file():
            with path.open("rb") as stream:
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
            if digest != item["sha256"]:
                errors.append(f"{item['path']}: hash mismatch")
            if item["path"].startswith("data/") or "measurements" in item:
                if item.get("measurements") != measure(path, item["path"]):
                    errors.append(f"{rel}: measurements differ from file")
        elif item["decision"] == "redistributed":
            errors.append(f"redistributed file missing: {item['path']}")
        if "redistributed" in item and (not isinstance(item["redistributed"], bool) or
                                       item["redistributed"] != (item["decision"] == "redistributed")):
            errors.append(f"{rel}: redistributed compatibility field disagrees with decision")
        if item['path'] in FIRST_PARTY:
            errors.append(f"{rel}: third-party record conflicts with first-party exception")
        found.append(item)
        if "outputs" in item:
            outputs = item["outputs"]
            if not isinstance(outputs, list) or not outputs or service:
                errors.append(f"{rel}: invalid outputs")
                continue
            seen = set()
            for output in outputs:
                if (not isinstance(output, dict) or not safe_path(output.get("file")) or
                        not isinstance(output.get("sha256"), str) or
                        not re.fullmatch(r"[0-9a-f]{64}", output["sha256"]) or
                        type(output.get("bytes")) is not int or output["bytes"] < 0):
                    errors.append(f"{rel}: invalid output")
                    continue
                name = output["file"]
                if name in seen:
                    errors.append(f"{rel}: duplicate output: {name}")
                    continue
                seen.add(name)
                output_rel = (PurePosixPath(rel).parent / name).as_posix()
                output_path = root / output_rel
                if name == item["file"]:
                    if output["sha256"] != item["sha256"]:
                        errors.append(f"{rel}: primary output hash disagrees")
                if output_path.is_symlink() or any(p.is_symlink() for p in output_path.parents if p != root):
                    errors.append(f"{rel}: symlink asset refused: {output_rel}")
                    continue
                if output_path.is_file():
                    data = output_path.read_bytes()
                    if hashlib.sha256(data).hexdigest() != output["sha256"]:
                        errors.append(f"{output_rel}: hash mismatch")
                    if len(data) != output["bytes"]:
                        errors.append(f"{output_rel}: output byte count mismatch")
                elif item["decision"] == "redistributed":
                    errors.append(f"redistributed file missing: {output_rel}")
                if name != item["file"]:
                    child = {k: v for k, v in item.items() if k not in ("outputs", "documentation")}
                    child.update(file=name, path=output_rel, sha256=output["sha256"],
                                 measurements={"bytes": output["bytes"]})
                    found.append(child)
            if item["file"] not in seen:
                errors.append(f"{rel}: outputs omit primary file")
    by_path = {r["path"]: r for r in found}
    if len(by_path) != len(found):
        errors.append("duplicate records for one file")
    for rel in sorted(paths):
        if third_party(rel) and rel not in by_path:
            errors.append(f"unrecorded third-party file: {rel}")
    for item in found:
        if "derivedFrom" not in item:
            continue
        components = item['derivedFrom']
        if (not isinstance(components, list) or not components or
                not all(isinstance(p, str) and p in by_path for p in components)):
            errors.append(f"{item['sidecar']}: missing or invalid component records")
            continue
        expected = " ".join(dict.fromkeys(by_path[p]["attribution"] for p in components))
        if item["attribution"] != expected:
            errors.append(f"{item['sidecar']}: attribution differs from component records")
    return found, errors


def asset_errors(root: Path, recs: list[dict], served: set[str], *, published=False) -> list[str]:
    errors = []
    by_path = {r['path']: r for r in recs}
    if published:
        for rel in inventory_paths(root):
            if (root / rel).is_file() and third_party(rel) and rel not in by_path:
                errors.append(f"unrecorded third-party file: {rel}")
        for r in recs:
            path = root / r['path']
            if PurePosixPath(r['path']).parts[0] not in served or r.get('kind') == 'service':
                continue
            if r['decision'] == 'redistributed' and not path.is_file():
                errors.append(f"published asset missing: {r['path']}")
            elif path.is_file():
                if r['decision'] != 'redistributed':
                    errors.append(f"excluded file in published output: {r['path']}")
                with path.open('rb') as stream:
                    if hashlib.file_digest(stream, 'sha256').hexdigest() != r['sha256']:
                        errors.append(f"published hash mismatch: {r['path']}")
    static = root / "3d/assets/static"
    if static.is_dir():
        try:
            generated = {row["file"] for row in json.loads((static / "manifest.json").read_text())["figures"]}
            for path in static.glob("*.svg"):
                if path.name not in generated:
                    errors.append(f"unclassified served map or figure: 3d/assets/static/{path.name}")
        except (OSError, ValueError, KeyError, TypeError):
            errors.append("3d/assets/static/manifest.json: invalid generator record")
    return errors


def map_credit(recs: list[dict]) -> str:
    by_name = {Path(r["path"]).stem: r for r in recs}
    selected = [by_name[key]["attribution"] for key in DISPLAY if key in by_name]
    credits = list(dict.fromkeys(selected))
    return (CREDIT_START + '\n<div class="mapcredit" aria-label="Map data credits">'
            + '<br>'.join(esc(s) for s in credits)
            + '<br><a href="notices.html">Data, licences and notices</a></div>\n' + CREDIT_END)


def embedded_credit(source: str) -> str | None:
    match = re.search(re.escape(CREDIT_START) + r".*?" + re.escape(CREDIT_END), source, re.S)
    return match.group(0) if match else None


def link_errors(dest: Path) -> list[str]:
    errors = []
    for path in sorted(dest.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in (".html", ".md"):
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        if path.suffix == ".html":
            links = parse_links(content, path.suffix)
            pointers = []
        else:
            links = parse_links(content, path.suffix)
            # Plain-text pointers to the public legal documents must also resolve.
            pointers = re.findall(r"`((?:\.\./)?(?:LICENSE|NOTICE|DATA-SOURCES\.md))`", content)
        for pointer in pointers:
            if not (path.parent / pointer).exists() and not (dest / pointer).exists():
                errors.append(f"broken documented pointer: {path.relative_to(dest)} -> {pointer}")
        for link in links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or link.startswith(("/", "#", "mailto:", "javascript:")):
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if dest.resolve() not in (target, *target.parents):
                continue  # this public package sits inside a larger website
            if not target.exists() and not (target.is_dir() and (target / "index.html").exists()):
                errors.append(f"broken relative link: {path.relative_to(dest)} -> {link}")
    return errors


def manifest(root: Path) -> set[str]:
    return {parts[1] for line in (root / "dist.manifest").read_text().splitlines()
            if (parts := line.split()) and parts[0] == "served" and len(parts) > 1}


def check(root: Path, dest: Path | None = None, public: bool = False) -> list[str]:
    recs, errors = records(root)
    served = manifest(root)
    errors += asset_errors(root, recs, served)
    if public:
        errors += [f"public tree contains {r['decision']} file: {r['path']}" for r in recs
                   if r['decision'] != 'redistributed' and (root / r['path']).exists()]
    for name in REQUIRED:
        if name not in served or not (root / name).is_file():
            errors.append(f"required publication missing: {name}")
        if dest and not (dest / name).is_file():
            errors.append(f"published output missing: {name}")
    # Refuse malformed inputs before rendering. No partial or guessed notice is generated.
    if errors:
        return errors
    for name, expected in noticegen.outputs(recs).items():
        path = root / name
        if not path.is_file() or path.read_text(encoding='utf-8') != expected:
            errors.append(f"{name} differs from fresh generation (missing, extra or changed row/content)")
        if dest and (name.split('/')[0] in served):
            path = dest / name
            if not path.is_file() or path.read_text(encoding='utf-8') != expected:
                errors.append(f"published {name} differs from fresh generation")
    if embedded_credit((root / 'index.html').read_text()) != map_credit(recs):
        errors.append("monitor map credit differs from provenance records")
    if dest:
        if (dest / 'index.html').is_file() and embedded_credit((dest / 'index.html').read_text()) != map_credit(recs):
            errors.append("published map credit differs from provenance records")
        errors += asset_errors(dest, recs, served, published=True)
        errors += link_errors(dest)
        for path in sorted(dest.rglob('*.html')):
            if not re.search(r'<footer\b[^>]*>.*?href=["\'][^"\']*notices\.html["\'].*?</footer>',
                             path.read_text(encoding='utf-8'), re.S):
                errors.append(f"served page lacks footer notice link: {path.relative_to(dest)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT, help='repository or release export to check')
    parser.add_argument('--dest', type=Path, help='additionally verify an already copied served tree')
    parser.add_argument('--public', action='store_true', help='refuse excluded files still present')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--write', action='store_true', help='generate notices and data README; never change hashes or index.html')
    modes.add_argument('--counts', action='store_true', help='measure local data counts without writing or fetching')
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        recs, errors = records(root)
        if args.counts:
            for r in recs:
                if r['path'].startswith('data/') and r.get('kind', 'file') == 'file' and (root / r['path']).is_file():
                    print(r['path'] + ': ' + json.dumps(measure(root / r['path'], r['path']), sort_keys=True))
        if args.write and not errors:
            if args.public:
                errors += [f"public tree contains {r['decision']} file: {r['path']}" for r in recs
                           if r['decision'] != 'redistributed' and (root / r['path']).exists()]
            if not errors:
                for name, content in noticegen.outputs(recs).items():
                    (root / name).write_text(content, encoding='utf-8')
                print('generated NOTICE, DATA-SOURCES.md, notices.html, data/README.md')
        elif not args.counts and not errors:
            errors = check(root, args.dest, args.public)
        if errors:
            print('noticecheck: FAIL')
            print('\n'.join(errors))
            return 1
        counts = []
        for folder in FOLDERS:
            files = [r for r in recs if r['path'].startswith(folder + '/') and r.get('kind', 'file') == 'file']
            present = sum((root / r['path']).is_file() for r in files)
            counts.append(f'{folder}: {present} files read, {len(files)} records')
        print(f"noticecheck: PASS ({len(recs)} provenance records; " + '; '.join(counts) + ')')
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(f'noticecheck: FAIL (cannot read/validate inventory: {type(exc).__name__})')
        return 1


if __name__ == '__main__':
    sys.exit(main())
