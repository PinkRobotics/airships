#!/usr/bin/env python3
"""Verify or reconstruct exact projected publication bytes from ordered JSON text chunks."""
import argparse
import hashlib
import json
from pathlib import Path


def reconstruct(manifest_path):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schema") != "public-research-text-chunks-v1":
        raise ValueError("not a reconstruction manifest")
    chunks = manifest["chunks"]
    if not chunks:
        raise ValueError("empty chunk list")
    parts = []
    for number, entry in enumerate(chunks):
        path = (manifest_path.parent / entry["path"]).resolve()
        if manifest_path.parent.resolve() not in path.parents:
            raise ValueError("chunk path escapes manifest directory")
        raw = path.read_bytes()
        if len(raw) != entry["bytes"] or hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise ValueError(f"chunk {number}: size or hash mismatch")
        chunk = json.loads(raw)
        if chunk.get("schema") != "public-research-text-chunk-v1" or chunk["index"] != number:
            raise ValueError(f"chunk {number}: schema or order mismatch")
        part = chunk["text"].encode("utf-8")
        if len(part) != entry["decoded_bytes"]:
            raise ValueError(f"chunk {number}: decoded size mismatch")
        parts.append(part)
    result = b"".join(parts)
    original = manifest.get("reconstructed_r3", manifest["reconstructed_r2"])
    if len(result) != original["bytes"] or hashlib.sha256(result).hexdigest() != original["sha256"]:
        raise ValueError("reconstructed publication size or hash mismatch")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--verify-only", action="store_true")
    mode.add_argument("--output", type=Path, help="new output file; existing files are never overwritten")
    args = parser.parse_args()
    try:
        data = reconstruct(args.manifest)
        if args.output:
            with args.output.open("xb") as stream:
                stream.write(data)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f"reconstruction failed: {exc}\n")
    print(f"Verified {len(data)} projected bytes; sha256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
