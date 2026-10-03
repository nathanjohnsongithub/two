"""Favicon: a 16x16 pixel heart with a little "2" in it, for "Year Two".

Writes public/favicon.svg (crisp at any size), public/favicon-32.png
(fallback), public/apple-touch-icon.png (180x180, on the game's dark
background) and tools/favicon_preview.png.
"""

import os

from pixel import check, hex_rgba, render, root, write_png

PALETTE = {
    ".": None,
    "o": "#3a2e39",  # ink outline
    "r": "#e56b6f",  # accent heart
    "s": "#c4505a",  # shade
    "h": "#f6b0ae",  # highlight
    "c": "#fffaf4",  # paper "2"
}

W = H = 16
ICON = check([
    "................",
    "..oooo....oooo..",
    ".orrrro..orrrro.",
    "orhhrrroorrrrrro",
    "orhrrrrccrrrrrro",
    "orrrrrcrrcrrrrso",
    "orrrrrrrrcrrrrso",
    "orrrrrrrcrrrrrso",
    ".orrrrrcrrrrrso.",
    ".orrrrrccccrrso.",
    "..orrrrrrrrrso..",
    "...orrrrrrrso...",
    "....orrrrrso....",
    ".....orrrso.....",
    "......orso......",
    ".......oo.......",
], W, H, PALETTE, "favicon")

BG = "#1a1420"  # matches index.html


def svg(rows):
    rects = []
    for y, row in enumerate(rows):
        x = 0
        while x < len(row):
            ch = row[x]
            run = 1
            while x + run < len(row) and row[x + run] == ch:
                run += 1
            if PALETTE[ch]:
                rects.append(f'<rect x="{x}" y="{y}" width="{run}" height="1" fill="{PALETTE[ch]}"/>')
            x += run
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" shape-rendering="crispEdges">'
        + "".join(rects) + "</svg>\n"
    )


def on_background(rows, size, scale):
    """Center the icon at `scale` on a solid square of `size` px."""
    icon = render([rows], PALETTE, W, H, scale=scale)
    bg = hex_rgba(BG)
    pixels = [[bg] * size for _ in range(size)]
    off = (size - W * scale) // 2
    for y, row in enumerate(icon):
        for x, px in enumerate(row):
            if px[3]:
                pixels[off + y][off + x] = px
    return pixels


if __name__ == "__main__":
    out = os.path.join(root(), "public")
    with open(os.path.join(out, "favicon.svg"), "w") as f:
        f.write(svg(ICON))
    write_png(os.path.join(out, "favicon-32.png"), render([ICON], PALETTE, W, H, scale=2))
    # 9x = 144px heart on a 180px tile leaves iOS room to round the corners.
    write_png(os.path.join(out, "apple-touch-icon.png"), on_background(ICON, 180, 9))
    write_png(os.path.join(root(), "tools", "favicon_preview.png"),
              render([ICON], PALETTE, W, H, scale=12, gap=1, bg=hex_rgba("#ffffff")))
