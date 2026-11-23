#!/usr/bin/env python3
"""news-image-20261123: write the day's front page to /output/entry.png.

The entry image sits next to this file as entry.png. The program copies
it to the output directory, byte for byte, so both grading runs produce
identical output. Standard library only, no network.

Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SOURCE = os.path.join(HERE, "entry.png")
TARGET = os.path.join(OUT_DIR, "entry.png")

# The competition gate: at most 1 MiB and at most 1024x1024 pixels.
MAX_BYTES = 1048576
MAX_SIDE = 1024


def _jpeg_size(path: str) -> tuple:
    """Read width/height out of a JPEG header without any dependency."""
    with open(path, "rb") as fh:
        data = fh.read(2)
        if data != b"\xff\xd8":
            raise ValueError("entry.png is not a JPEG")
        while True:
            marker = fh.read(2)
            if len(marker) < 2 or marker[0] != 0xFF:
                raise ValueError("bad JPEG marker")
            code = marker[1]
            if code in (0xC0, 0xC1, 0xC2):
                fh.read(3)
                raw = fh.read(4)
                height, width = struct.unpack(">HH", raw)
                return width, height
            length = struct.unpack(">H", fh.read(2))[0]
            fh.seek(length - 2, 1)


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    size = os.path.getsize(TARGET)
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, over the 1 MiB gate")
    width, height = _jpeg_size(TARGET)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit(f"entry.png is {width}x{height}, over 1024x1024")
    print(f"wrote {TARGET}: {width}x{height}, {size} bytes")


if __name__ == "__main__":
    main()
