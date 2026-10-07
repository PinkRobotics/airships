#!/usr/bin/env python3
"""Require a named builder from the first recorded builder on first-parent history."""
import argparse
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
BUILDER = re.compile(r"^Builder:\s*\S", re.IGNORECASE)
ATTESTATION = "docs/governance/landing-attestations.md"


def check(root=ROOT):
    # Check this root itself: an exported tree inside another repository has no history.
    # lstat accepts both .git directories and linked-worktree .git files, and exposes errors.
    try:
        (root / ".git").lstat()
    except FileNotFoundError:
        return 0, "buildercheck: no history; nothing checked (.git absent)"

    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args],
                                       stderr=subprocess.PIPE).decode("utf-8", errors="replace")

    shallow = git("rev-parse", "--is-shallow-repository").strip() == "true"
    commits = git("rev-list", "--first-parent", "--reverse", "HEAD").splitlines()
    start, checked, exempt, missing = None, 0, 0, []
    for commit in commits:
        # Metadata only: do not open historical files or emit a historical patch.
        message = git("show", "--stat", "--format=%B", commit)
        named = any(BUILDER.match(line) for line in message.splitlines())
        if start is None:
            if not named:
                continue
            start = commit
        parents = git("rev-list", "--parents", "-n", "1", commit).split()[1:]
        touched = (git("diff", "--name-only", "--no-renames", "-z", parents[0], commit)
                   if parents else git("diff-tree", "--root", "--no-commit-id", "--name-only",
                                       "--no-renames", "-r", "-z", commit))
        if touched.split("\0") == [ATTESTATION, ""]:
            exempt += 1
            continue
        checked += 1
        if not named:
            missing.append(commit)

    prefix = "buildercheck: shallow;" if shallow else "buildercheck:"
    if start is None:
        return (0 if shallow else 1), f"{prefix} checked 0 commits; 0 attestations exempted; no Builder record found"
    summary = f"{prefix} checked {checked} commits; {exempt} attestations exempted; record starts {start}"
    if missing:
        return 1, summary + "; missing Builder: " + ", ".join(missing)
    return 0, summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        code, summary = check(args.root.resolve())
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"buildercheck: could not check history ({type(exc).__name__})", file=sys.stderr)
        return 1
    print(summary)
    return code


if __name__ == "__main__":
    sys.exit(main())
