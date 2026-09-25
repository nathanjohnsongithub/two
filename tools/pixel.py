"""Tiny pixel-art helpers shared by the sprite/tile generators (no dependencies)."""

import os
import struct
import zlib


def hex_rgba(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


def check(rows, w, h, palette, name="frame"):
    assert len(rows) == h, f"{name}: {len(rows)} rows, expected {h}"
    for i, r in enumerate(rows):
        assert len(r) == w, f"{name}: row {i} is {len(r)} wide: {r!r}"
        for ch in r:
            assert ch in palette, f"{name}: unknown pixel {ch!r} in row {i}"
    return rows


def mirror(rows):
    return [r[::-1] for r in rows]


def write_png(path, pixels):
    height, width = len(pixels), len(pixels[0])
    raw = b"".join(b"\x00" + b"".join(bytes(px) for px in row) for row in pixels)

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9))
    png += chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)


def render(frames, palette, w, h, scale=1, gap=0, bg=None):
    """Lay frames out in one row and return a pixel grid."""
    n = len(frames)
    width = (w * n + gap * (n + 1)) * scale
    height = (h + gap * 2) * scale
    clear = (0, 0, 0, 0)
    pixels = [[bg or clear for _ in range(width)] for _ in range(height)]
    for i, rows in enumerate(frames):
        ox = gap + i * (w + gap)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                color = palette[ch]
                if color is None:
                    continue
                rgba = hex_rgba(color)
                for dy in range(scale):
                    for dx in range(scale):
                        pixels[(gap + y) * scale + dy][(ox + x) * scale + dx] = rgba
    return pixels


def root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
