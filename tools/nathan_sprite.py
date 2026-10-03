"""Generates Nathan's spritesheets: public/sprites/nathan.png and
public/sprites/nathan_gown.png (his cap and gown, for his glimpse in chapter 3).

Short, tousled brown hair swept to one side (ears showing), fair skin, a
long-sleeve henley and black jeans with a belt. Frames are 16x26 (two pixels taller than Hannah). Run:
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
    "H": "#74502f",  # hair, medium brown
    "d": "#4f3320",  # hair shadow (the waves)
    "h": "#a87d50",  # hair highlight (sun-lightened tips)
    "S": "#f1c9a5",  # skin, fair
    "s": "#d9a383",  # skin shadow (ears, jaw, nose)
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
    "M": "#7d1f2c",  # graduation gown, Loyola maroon
    "n": "#5a1520",  # gown folds
    "C": "#1f1a1e",  # mortarboard
    "Y": "#e8b83e",  # tassel / stole, gold
}

W, H = 16, 26

# Tousled hair, fuller on top and swept over, short at the sides so his ears
# show; a longer face that narrows to the chin.
FRONT = [
    ".....oooooo.....",
    "...ooHHHhhHHo...",
    "..oHHhhHHHHHHo..",
    "..oHHHHhhHHdHo..",
    "..oHdHHHHhhHHo..",
    "..oHHhhSSSSdHo..",
    "..oHSSShSSSSHo..",
    "..osSeSSSSeSso..",
    "..osSeSSSSeSso..",
    "...oSSSSsSSSo...",
    "...oSSSmmSSSo...",
    "....osSSSSso....",
    ".....oSSSSo.....",
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
    ".....oooooo.....",
    "...ooHHHhhHHo...",
    "..oHHhhHHHHHHo..",
    "..oHHHHhhHHdHo..",
    "..oHhhHHHHhhHo..",
    "..oHHHHdHHHHHo..",
    "..oHdHHHHHHdHo..",
    "..osHHHHHHHHso..",
    "..osHHHHHHHHso..",
    "...oHHHHHHHHo...",
    "...ooHHHHHHoo...",
    "....oSSSSSSo....",
    ".....oSSSSo.....",
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
    "....oHHHHhhHo...",
    "...oHHhhHHHHHo..",
    "...oHHHHhhHHHHo.",
    "...oHdHHHHhhHdo.",
    "...oHhHHHHSSSo..",
    "...oHHsSSSSeSo..",
    "...oHHsSSSSeSo..",
    "...oHHsSSSSSSSo.",
    "....oHSSSSSSmo..",
    "....ooSSSSSSo...",
    ".....osSSSSo....",
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


# ---------- graduation: a cap over the top of his hair, the gown over the rest ----------

CAP_FRONT = [
    "..oooooooooooo..",
    ".oCCCCCCCCCCCCo.",
    "..oooCCCCCCoooY.",
    "..oHHCCCCCCHHoY.",
    "..oHhHHhHHHhHoY.",
]
CAP_BACK = CAP_FRONT[:4] + ["..oHHHHHHHHHHoY."]
CAP_SIDE = [
    "...oooooooooo...",
    "..oCCCCCCCCCCo..",
    "..YooCCCCCCoo...",
    "..YoHCCCCCCHo...",
    "..YoHHhHHHhHHHo.",
]

GOWN_FRONT = [
    "...oMMYSSYMMo...",
    "..oMMYMMMMYMMo..",
    ".oMMMYMMMMYMMMo.",
    ".oMoMYMMMMYMoMo.",
    ".oMoMYMMMMYMoMo.",
    ".oMoMYMMMMYMoMo.",
    ".oSoMMMMMMMMoSo.",
    "..oMMMMMMMMMMo..",
    "..oMMMnMMnMMMo..",
]
GOWN_BACK = [
    "...oMMMMMMMMo...",
    "..oMMMMMMMMMMo..",
    ".oMMMMMMMMMMMMo.",
    ".oMoMMMMMMMMoMo.",
    ".oMoMMMMMMMMoMo.",
    ".oMoMMMMMMMMoMo.",
    ".oSoMMMMMMMMoSo.",
    "..oMMMMMMMMMMo..",
    "..oMMMnMMnMMMo..",
]
GOWN_SIDE = [
    "....oMMMMMMo....",
    "....oMYMMMMMo...",
    "...oMMYMMMMMo...",
    "...oMMYMMMMMo...",
    "...oMMMYMMMMo...",
    "...oMMMYSMMMo...",
    "..oMMMMMMMMMMo..",
    "..oMMnMMnMMnMo..",
    "..oMMnMMnMMnMo..",
]

# The gown reaches the ground, so walking just shows his shoes stepping out.
HEM = ["..oMMMnMMnMMMo..", "..onMMMMMMMMno..", "..oooooooooooo.."]
GOWN_LEGS_FRONT = {
    "idle": HEM + ["....oFo..oFo...."],
    "a": HEM + ["...oFFo........."],
    "b": HEM + [".........oFFo..."],
}
GOWN_LEGS_SIDE = {
    "idle": HEM + [".....oFFFo......"],
    "a": HEM + ["...oFFo..oFFo..."],
    "b": HEM + ["....oFFooFFo...."],
}


def frame(body, legs, step):
    """On a step his body dips a pixel (the knees bend), which gives the walk a bounce."""
    rows = ["." * W] + body + legs[1:] if step else body + legs
    return check(rows, W, H, PALETTE)


def build_frames(views):
    frames = []
    for body, legs in views:
        for key in ("idle", "a", "b"):
            frames.append(frame(body, legs[key], key != "idle"))
    return frames + [mirror(f) for f in frames[6:9]]


if __name__ == "__main__":
    outfits = {
        "nathan": build_frames(((FRONT, LEGS_FRONT), (BACK, LEGS_FRONT), (SIDE, LEGS_SIDE))),
        "nathan_gown": build_frames((
            (CAP_FRONT + FRONT[5:13] + GOWN_FRONT, GOWN_LEGS_FRONT),
            (CAP_BACK + BACK[5:13] + GOWN_BACK, GOWN_LEGS_FRONT),
            (CAP_SIDE + SIDE[5:13] + GOWN_SIDE, GOWN_LEGS_SIDE),
        )),
    }
    bg = (243, 230, 216, 255)
    preview = []
    for name, frames in outfits.items():
        write_png(os.path.join(root(), f"public/sprites/{name}.png"), render(frames, PALETTE, W, H))
        preview += render(frames, PALETTE, W, H, scale=8, gap=2, bg=bg)
    write_png(os.path.join(root(), "tools/nathan_preview.png"), preview)
    print(f"Wrote {len(outfits)} outfits")
