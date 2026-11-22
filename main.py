#!/usr/bin/env python3
"""Write the entry photograph to the output directory.

The entry is a single photograph, entry.png, bundled next to this
file. Running this program copies it to
$MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when that
variable is unset) and verifies the copy before finishing: the byte
count must match the source, and the first three bytes must be the
JPEG magic bytes FF D8 FF.

The run is deterministic: the output is a byte-for-byte copy of the
bundled file, so two runs always produce identical bytes.

Standard library only. No network, no clock, no randomness.
"""

import os
import shutil
import sys
from pathlib import Path

JPEG_MAGIC = b"\xff\xd8\xff"
SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def fail(message):
    """Print an error and stop with a non-zero exit code."""
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    source = Path(__file__).resolve().parent / SOURCE_NAME
    if not source.is_file():
        fail(f"bundled photograph not found next to main.py: {source}")

    with source.open("rb") as handle:
        source_head = handle.read(len(JPEG_MAGIC))
    if source_head != JPEG_MAGIC:
        fail(
            f"bundled photograph is not a JPEG: first bytes are "
            f"{source_head.hex()}, expected ffd8ff"
        )

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        fail(f"cannot create output directory {out_dir}: {exc}")

    destination = out_dir / OUTPUT_NAME
    try:
        shutil.copyfile(source, destination)
    except OSError as exc:
        fail(f"cannot write {destination}: {exc}")

    source_size = source.stat().st_size
    dest_size = destination.stat().st_size
    if dest_size != source_size:
        fail(
            f"copy incomplete: wrote {dest_size} bytes, "
            f"expected {source_size} bytes from {source}"
        )

    with destination.open("rb") as handle:
        head = handle.read(len(JPEG_MAGIC))
    if head != JPEG_MAGIC:
        fail(
            f"output is not a JPEG: first bytes are {head.hex()}, "
            "expected ffd8ff"
        )

    print(f"wrote {destination} ({dest_size} bytes, JPEG verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
