#!/usr/bin/env python3
"""Validate and emit the news-23 b156 front-page-dense entry image.

Reads entry.png next to this file, verifies it is a well-formed 1024x1024
PNG (manual header parse, stdlib only -- no PIL), then writes a byte-identical
copy to os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png").
Never writes next to main.py. Usage: python3 -P -s main.py
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "f9e2f2cf0ea5bf1facc1b79d4f165798d70504ca36ae6d675b6b4ff09806742c"
EXPECTED_SIZE = 159665
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def check_png(data):
    """Verify PNG structure: signature, IHDR 1024x1024, CRCs, IEND last."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    if len(data) < 33:
        fail("file too small")
    # first chunk must be IHDR, 13 bytes
    length = struct.unpack(">I", data[8:12])[0]
    ctype = data[12:16]
    if ctype != b"IHDR" or length != 13:
        fail("first chunk must be 13-byte IHDR")
    w, h, depth, ctype_col, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        fail("dimensions must be 1024x1024, got %dx%d" % (w, h))
    if depth != 8 or ctype_col not in (2, 6):
        fail("bit depth must be 8 and colour type 2 or 6")
    if comp != 0 or filt != 0 or inter != 0:
        fail("compression/filter/interlace must be 0")
    crc_stored = struct.unpack(">I", data[29:33])[0]
    crc_calc = zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF
    if crc_stored != crc_calc:
        fail("IHDR CRC mismatch")
    # walk chunks: CRC covers type+data, not length
    pos = 8
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + clen
        if end > len(data):
            fail("truncated chunk %r" % ctype)
        crc_stored = struct.unpack(">I", data[pos + 8 + clen:end])[0]
        crc_calc = zlib.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF
        if crc_stored != crc_calc:
            fail("CRC mismatch in chunk %r" % ctype)
        if ctype == b"IDAT":
            if clen == 0:
                fail("empty IDAT chunk")
            idat_total += clen
        if ctype == b"IEND":
            if clen != 0:
                fail("IEND must be 0 bytes")
            if end != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            break
        pos = end
    if not seen_iend:
        fail("missing IEND chunk")
    if idat_total < 1000:
        fail("IDAT payload too small")
    return True


def main():
    if not os.path.isfile(SRC):
        fail("source entry.png not found next to main.py")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) < 10000:
        fail("file too small: %d bytes" % len(data))
    if len(data) > 1024 * 1024:
        fail("file over 1 MiB: %d bytes" % len(data))
    check_png(data)
    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 != "PLACEHOLDER_SHA256" and sha != EXPECTED_SHA256:
        fail("sha256 mismatch: got %s" % sha)
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        fail("size mismatch: got %d bytes" % len(data))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    repo_abs = os.path.abspath(os.path.dirname(__file__))
    if out_dir_abs == repo_abs or out_dir_abs.startswith(repo_abs + os.sep):
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.exists(out_dir_abs) and not os.path.isdir(out_dir_abs):
        fail("MAKEFUN_OUTPUT_DIR exists and is not a directory")
    out_path = os.path.join(out_dir, "entry.png")
    if os.path.isfile(out_path):
        fail("output path already exists as a file: " + out_path)
    if os.path.abspath(out_path) == os.path.abspath(SRC):
        fail("output would overwrite the source image")
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    with open(out_path, "rb") as f:
        written = f.read()
    if written != data:
        fail("written output is not byte-identical to source")
    print("ok: wrote %s (%d bytes, sha256 %s)" % (out_path, len(data), sha))


if __name__ == "__main__":
    main()
