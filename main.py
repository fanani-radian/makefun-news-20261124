#!/usr/bin/env python3
"""World News front page — Tuesday 24 November 2026.

make.fun competition news-image-20261124: the entry is a program that
writes one image summing up the day's world news to entry.png.

The front page is a pre-rendered 1024x1024 PNG (entry.png in this repo),
drawn from six verified stories for 24 November 2026: Nvidia reinstating
Jensen Huang, 14 nations backing the ICJ genocide ruling on Myanmar, the
escalating Gulf war, the UN probe into the Libya warship strike, the 24
confirmed dead in the Java candy factory fire, and NATO's space-defence
vow. This script is the harness entrypoint: it copies that image,
byte for byte, to $MAKEFUN_OUTPUT_DIR/entry.png.

The copy is deterministic — identical input bytes produce identical
output bytes on every run — and uses no network, no clock and no
randomness. Run with --verify-only to check an existing output copy
instead of writing one.
"""

import hashlib
import os
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
NAME = "entry.png"
MODE = 0o644


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def out_dir() -> Path:
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(raw) if raw else Path("/output")


def load() -> bytes:
    if not SOURCE.is_file():
        print(f"error: source image {SOURCE} is missing", file=sys.stderr)
        sys.exit(1)
    return SOURCE.read_bytes()


def check(data: bytes) -> int:
    target = out_dir() / NAME
    if not target.is_file():
        print(f"error: {target} does not exist", file=sys.stderr)
        return 1
    got = target.read_bytes()
    if digest(got) != digest(data):
        print(
            f"error: {target} differs from {SOURCE}",
            file=sys.stderr,
        )
        return 1
    print(f"verified {target}: {len(got)} bytes, sha256 {digest(got)}")
    return 0


def publish(data: bytes) -> int:
    directory = out_dir()
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / NAME
    target.write_bytes(data)
    os.chmod(target, MODE)
    return check(data)


def main(argv) -> int:
    verify_only = "--verify-only" in argv
    data = load()
    if verify_only:
        return check(data)
    return publish(data)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
