"""Entrypoint for the 21 November 2026 news-image entry.

Copies the rendered poster (entry.png, shipped in this repo) to
/output/entry.png, the path the grader reads. No network, no
timestamps: the output bytes are exactly the shipped file's bytes,
so two runs are byte-identical by construction.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DEST = os.path.join(DEST_DIR, "entry.png")


def check_png(path):
    """Minimal PNG sanity check: signature + IHDR size 1024x1024."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("not a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit("missing IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit("expected 1024x1024, got %dx%d" % (width, height))
    size = os.path.getsize(path)
    if size > 1024 * 1024:
        raise SystemExit("image over 1 MiB: %d bytes" % size)
    return size


def run():
    size = check_png(SOURCE)
    os.makedirs(DEST_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, DEST)
    digest = hashlib.sha256(open(DEST, "rb").read()).hexdigest()
    print("entry.png: %d bytes, sha256 %s -> %s" % (size, digest, DEST))


if __name__ == "__main__":
    run()
