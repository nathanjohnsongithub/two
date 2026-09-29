"""Generates Nathan's spritesheet: public/sprites/nathan.png

Brown, jaw-length hair with a middle part, a long-sleeve henley and black
jeans with a belt. Frames are 16x26 (two pixels taller than Hannah). Run:
    python3 tools/nathan_sprite.py
Also writes tools/nathan_preview.png (8x scale) to eyeball the result.

Sheet layout (12 frames in one row, same as Hannah's):
  0-2  down  (idle, walk A, walk B)
  3-5  up
  6-8  right
  9-11 left  (mirror of right)
"""

import os

from pixel import check, mirror, render, root, write_png

PALETTE = {
    ".": None,
    "o": "#2b1d1a",  # outline
    "H": "#6b4428",  # hair, brown
    "h": "#9a6a40",  # hair highlight (the streaks show which way it flows)
    "S": "#e3b48c",  # skin
    "s": "#c9956d",  # skin shadow (cheekbones, jaw, nose)
    "e": "#2b1d1a",  # eyes
    "m": "#b06a55",  # mouth
    "G": "#6f7a4c",  # henley, olive
    "g": "#566039",  # henley shade
    "i": "#e6dcc4",  # henley buttons
    "B": "#1c1c20",  # belt
    "Z": "#c3c9cf",  # buckle
    "J": "#3a3a42",  # black jeans
    "j": "#27272d",  # jeans seams / shading
    "F": "#ececec",  # sneakers
}

W, H = 16, 26

# Hair parted in the middle, a couple of streaks following it out and down
# to his jaw.
FRONT = [
    "....oooooooo....",
    "...oHHHHHHHHo...",
    "..oHHhHHHHhHHo..",
    "..oHhHHSSHHhHo..",
    "..oHhHSSSSHhHo..",
    "..oHhSSSSSShHo..",
    "..oHSSSSSSSSHo..",
    "..oHSeSSSSeSHo..",
    "..oHSeSSSSeSHo..",
    "..oHSSSSSSSSHo..",
    "..oHSSSmmSSSHo..",
    "..oHosSSSSsoHo..",
    "...oooSSSSooo...",
    "...oGGGSSGGGo...",
    "..oGGGGgiGGGGo..",
    ".oGGGGGgiGGGGGo.",
    ".oGoGGGgGGGGoGo.",
    ".oGoGGGGGGGGoGo.",
    ".oGoGGGGGGGGoGo.",
    ".ogoGGGGGGGGogo.",
    ".oSoggggggggoSo.",
    "...oBBBZBBBBo...",
]

BACK = [
    "....oooooooo....",
    "...oHHHHHHHHo...",
    "..oHHHhHHhHHHo..",
    "..oHHhHHHHhHHo..",
    "..oHhHHHHHHhHo..",
    "..oHhHHHHHHhHo..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "...oooSSSSooo...",
    "...oGGGGGGGGo...",
    "..oGGGGGGGGGGo..",
    ".oGGGGGGGGGGGGo.",
    ".oGoGGGGGGGGoGo.",
    ".oGoGGGGGGGGoGo.",
    ".oGoGGGGGGGGoGo.",
    ".ogoGGGGGGGGogo.",
    ".oSoggggggggoSo.",
    "...oBBBBBBBBo...",
]

# Facing right; the left-facing frames are mirrored.
SIDE = [
    ".....oooooo.....",
    "....oHHHHHHo....",
    "...oHHHhhhHHo...",
    "...oHHhHHHHHHo..",
    "...oHhHHHHHSSo..",
    "...oHhHHHSSSSo..",
    "...oHhHSSSSeSo..",
    "...oHHhSSSSeSo..",
    "...oHHhsSSSSSo..",
    "...oHHHSSSSSmo..",
    "...oHhHoSSSSo...",
    "....oooSSSSo....",
    "......oSSSo.....",
    "....oGGGGGGo....",
    "....oGGGGGGGo...",
    "....oGGGgGGGo...",
    "....oGGGgGGGo...",
    "....oGGGgGGGo...",
    "....oGGGgGGGo...",
    "....oGGGSGGGo...",
    "....ogggggggo...",
    "....oBBBBBBBo...",
]

# Legs are the bottom 4 rows, swapped out per animation frame.
WALK_A_FRONT = [
    "...oJJJooJJJo...",
    "...oJJJooJJjo...",
    "...oFFo.oJJJo...",
    ".........oFFo...",
]

LEGS_FRONT = {
    "idle": [
        "...oJJJooJJJo...",
        "...ojJJooJJjo...",
        "...oJJJooJJJo...",
        "...oFFo..oFFo...",
    ],
    "a": WALK_A_FRONT,
    "b": [r[::-1] for r in WALK_A_FRONT],
}

LEGS_SIDE = {
    "idle": [
        "....oJJJJJJo....",
        "....ojJJJJJo....",
        "....oJJJJJJo....",
        "....oFFFFFFFo...",
    ],
    "a": [
        "....oJJJoJJJo...",
        "...oJJJo.oJJJo..",
        "...oJJJo.oJJJo..",
        "..oFFFo...oFFFo.",
    ],
    "b": [
        ".....oJJJJJo....",
        "....oJJJoJJJo...",
        "....oJJJoJJJo...",
        "...oFFFo.oFFFo..",
    ],
}


def frame(body, legs, step):
    """On a step his body dips a pixel (the knees bend), which gives the walk a bounce."""
    rows = ["." * W] + body + legs[1:] if step else body + legs
    return check(rows, W, H, PALETTE)


def build_frames():
    frames = []
    for body, legs in ((FRONT, LEGS_FRONT), (BACK, LEGS_FRONT), (SIDE, LEGS_SIDE)):
        for key in ("idle", "a", "b"):
            frames.append(frame(body, legs[key], key != "idle"))
    return frames + [mirror(f) for f in frames[6:9]]


if __name__ == "__main__":
    frames = build_frames()
    write_png(os.path.join(root(), "public/sprites/nathan.png"), render(frames, PALETTE, W, H))
    bg = (243, 230, 216, 255)
    write_png(os.path.join(root(), "tools/nathan_preview.png"), render(frames, PALETTE, W, H, scale=8, gap=2, bg=bg))
    print("Wrote nathan.png")
