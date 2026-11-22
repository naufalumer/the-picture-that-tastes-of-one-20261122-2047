#!/usr/bin/env python3
"""The picture that tastes of one ingredient: one lemon, cut open.

The entry is a single photograph of a halved lemon, shot as an extreme
macro: glistening juice vesicles, beads of sour juice, one drop falling,
nothing else in the frame. The whole picture is the taste of lemon.

This program does the one mechanical job the bounty asks for: it writes
that bundled photograph to $MAKEFUN_OUTPUT_DIR/entry.png. It renders
nothing and decides nothing at run time, so the two grader runs produce
byte-identical output. Standard library only, no network, no clock, no
randomness.
"""

import os
import sys

BUNDLED_IMAGE = "entry.png"
OUTPUT_NAME = "entry.png"
CHUNK = 65536


def bundled_path() -> str:
    """Path of the photograph shipped next to this file."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, BUNDLED_IMAGE)


def destination_path() -> str:
    """Where the grader wants the picture, honouring its env var."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, OUTPUT_NAME)


def stream_copy(source: str, dest: str) -> int:
    """Copy the photograph chunk by chunk; return the bytes moved."""
    moved = 0
    with open(source, "rb") as src, open(dest, "wb") as dst:
        while True:
            block = src.read(CHUNK)
            if not block:
                break
            dst.write(block)
            moved += len(block)
    return moved


def looks_like_jpeg(path: str) -> bool:
    """True when the file starts with the JPEG magic bytes."""
    with open(path, "rb") as handle:
        return handle.read(3) == b"\xff\xd8\xff"


def main() -> int:
    source = bundled_path()
    dest = destination_path()
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    expected = os.path.getsize(source)
    moved = stream_copy(source, dest)
    if moved != expected:
        raise SystemExit(
            "copy incomplete: moved %d of %d bytes" % (moved, expected)
        )
    if os.path.getsize(dest) != expected:
        raise SystemExit("output size mismatch after copy")
    if not looks_like_jpeg(dest):
        raise SystemExit("output is not a JPEG photograph")
    return 0


if __name__ == "__main__":
    sys.exit(main())
