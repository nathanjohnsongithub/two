"""Generates people sitting down: public/sprites/seated.png

Frames are 16x40 and line up with the map tile they sit on, so a seat in the
map can be taken by one of these. In this order (the frame number in
content.js):
  0-5   in a ceremony chair, seen from behind (graduation). The chair's back
        is part of the frame, so it covers them the way it should.
  6-8   on a stool at the Yokocho counter, seen from behind (facing up)
  9-11  on their own stool, facing right toward the counter
  12-14 the same three facing left
  15    one more ceremony chair family
  16-18 three more diners on their own stools, facing left (so the two
        sides of the counter aren't the same people)
Run:  python3 tools/seated_sprite.py
Also writes tools/seated_preview.png (6x scale).
"""

import os

from crowd_sprite import shade
from pixel import check, mirror, render, root, write_png

W, H = 16, 40

BASE = {
    ".": None,
    "o": "#2b1d1a",
    "e": "#2b1d1a",
    "m": "#a8604e",
    "I": "#f4f4f2", "i": "#cfd3d6",  # ceremony chair
    "P": "#8a5a3b", "p": "#6b4329",  # stool wood
}

BLANK = "." * 16

# From behind (13 rows, starting 3 rows down): the back of the head with the
# ears showing, then the neck. Short hair, or longer hair over the shoulders.
BACK_HEAD = {
    "short": [BLANK] * 3 + [
        "....oooooooo....",
        "...oHHHHHHHHo...",
        "..oHHHhHHhHHHo..",
        "..oHHHHHHHHHHo..",
        "..oHHhHHHHhHHo..",
        "..oHHHHHHHHHHo..",
        ".oSHHHHHHHHHHSo.",
        "..oHHHHHHHHHHo..",
        "...oHHHHHHHHo...",
        "....oSSSSSSo....",
    ],
    "long": [BLANK] * 3 + [
        "....oooooooo....",
        "...oHHHHHHHHo...",
        "..oHHHhhHHHHHo..",
        "..oHHHHHHHHHHo..",
        "..oHHhHHHHhHHo..",
        "..oHHHHHHHHHHo..",
        "..oHHHHHHHHHHo..",
        "..oHHHHHHHHHHo..",
        "..oHHHHHHHHHHo..",
        "..oHHHHHHHHHHo..",
    ],
}

# The frame's middle lines up with the middle of the map tile, so rows 12-27
# here are the tile's rows 0-15. The ceremony chair is drawn exactly where the
# map's is: its back (rows 15-19) covers their lower back, their shoulders and
# arms show above and beside it, their seat shows through the gap, and their
# legs are tucked under the chair.
IN_CHAIR = [
    "..ooCCCCCCCCoo..",
    ".oCCCCCCCCCCCCo.",
    ".oCCooooooooCCo.",
    ".oCCoIIIIIIoCCo.",
    ".oCCoIIIIIIoCCo.",
    ".oSCoiiiiiioCSo.",
    "..oooooooooooo..",
    ".....oJJJJo.....",
    "...oooooooooo...",
    "...oiiiiiiiio...",
    "...oooooooooo...",
    "....o.oJJo.o....",
    "....o.oJJo.o....",
    "....o.oFFo.o....",
] + [BLANK] * 13

# On a counter stool (the map's stool, its seat at rows 16-19): leaning on the
# counter with their elbows out, sitting on the seat, legs down to the footrest.
ON_STOOL = [
    "..ooCCCCCCCCoo..",
    ".oCCCCCCCCCCCCo.",
    "oCCoCCCCCCCCoCCo",
    "oCCoCCCCCCCCoCCo",
    ".oooJJJJJJJJooo.",
    "...opJJJJJJpo...",
    "....oooooooo....",
    ".....ooJJoo.....",
    ".....ooJJoo.....",
    ".....ooJJoo.....",
    ".....ooFFoo.....",
] + [BLANK] * 16

# Sideways on a stool of their own (a shorter one than the map's), reaching
# for the counter.
SIDE = [BLANK] * 8 + [
    "................",
    "................",
    "................",
    ".....oooooo.....",
    "....oHHHHHHo....",
    "...oHHHHHHSSo...",
    "...oHHHHSSSSo...",
    "...oHHHSSSeSo...",
    "...oHHHSSSSSo...",
    "....oHHSSSmo....",
    ".....ooSSSo.....",
    "....oCCCCCo.....",
    "...oCCCCCCCoo...",
    "...oCCCCCCCCSo..",
    "...oCCCCCCooo...",
    "...oCCCCCCo.....",
    "...oJJJJJJJJJo..",
    "...oJJJJJJJJJo..",
    "..oPPPPPPPoJJo..",
    "...oppppppoJJo..",
    "....o....ooFFFo.",
    "....o....o......",
    "....oooooo......",
    "....o....o......",
] + [BLANK] * 8

# hair, hair style, skin, top, pants
FAMILIES = [
    ("#b9b4ad", "short", "#f1c9a5", "#3d4f73", "#33302e"),
    ("#6b3a2a", "long", "#e9bd97", "#c8323a", "#33302e"),
    ("#1e1a18", "short", "#7a4a2e", "#5b7a3a", "#33302e"),
    ("#e0c070", "long", "#f3d2b8", "#9c7cc4", "#33302e"),
    ("#1e1a18", "long", "#c89572", "#2a9d8f", "#33302e"),
    ("#4a3526", "short", "#e9bd97", "#f4f4f2", "#33302e"),
]
DINERS = [
    ("#1e1a18", "short", "#e9bd97", "#3d4f73", "#33302e"),
    ("#4a3526", "long", "#f3d2b8", "#e07a8a", "#3d5a80"),
    ("#1e1a18", "long", "#c89572", "#f4f4f2", "#33302e"),
]
SIDE_DINERS = [
    ("#6b3a2a", "long", "#f1c9a5", "#2a9d8f", "#3d5a80"),
    ("#1e1a18", "short", "#8a5a3c", "#e8b83e", "#33302e"),
    ("#b9b4ad", "short", "#e9bd97", "#8a4a5c", "#b59b78"),
]
MORE_FAMILIES = [
    ("#a0522d", "long", "#f1c9a5", "#6a8cc4", "#33302e"),
]
MORE_SIDE_DINERS = [
    ("#1e1a18", "short", "#c89572", "#c8603a", "#33302e"),
    ("#e0c070", "short", "#f3d2b8", "#3d4f73", "#3d5a80"),
    ("#4a3526", "short", "#7a4a2e", "#9c7cc4", "#33302e"),
]


def palette(hair, skin, top, pants):
    pal = dict(BASE)
    pal["H"], pal["h"] = hair, shade(hair, 1.35 if hair != "#1e1a18" else 2.2)
    pal["S"], pal["C"], pal["J"], pal["F"] = skin, top, pants, "#2b2626"
    return pal


if __name__ == "__main__":
    frames, pals = [], []

    def add(rows, pal, name):
        frames.append(check(rows, W, H, pal, name))
        pals.append(pal)

    for hair, style, skin, top, pants in FAMILIES:
        add(BACK_HEAD[style] + IN_CHAIR, palette(hair, skin, top, pants), "chair")
    for hair, style, skin, top, pants in DINERS:
        add(BACK_HEAD[style] + ON_STOOL, palette(hair, skin, top, pants), "stool")
    side = [(SIDE, palette(h, sk, t, p)) for h, _, sk, t, p in SIDE_DINERS]
    for rows, pal in side:
        add(rows, pal, "side")
    for rows, pal in side:
        add(mirror(rows), pal, "side left")
    for hair, style, skin, top, pants in MORE_FAMILIES:
        add(BACK_HEAD[style] + IN_CHAIR, palette(hair, skin, top, pants), "chair")
    for hair, _, skin, top, pants in MORE_SIDE_DINERS:
        add(mirror(SIDE), palette(hair, skin, top, pants), "side left")

    # Each frame has its own colors, so render them one at a time and join the rows.
    def strip(scale=1, gap=0, bg=None):
        parts = [render([f], p, W, H, scale=scale, gap=gap, bg=bg) for f, p in zip(frames, pals)]
        return [sum((part[y] for part in parts), []) for y in range(len(parts[0]))]

    write_png(os.path.join(root(), "public/sprites/seated.png"), strip())
    write_png(os.path.join(root(), "tools/seated_preview.png"), strip(6, 2, (120, 150, 100, 255)))
    print(f"Wrote {len(frames)} seated")
