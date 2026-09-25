"""Generates Hannah's spritesheets: public/sprites/hannah.png and
public/sprites/hannah_gown.png (graduation cap and gown, chapter 3).

Each frame is drawn as a 16x24 text grid (one character per pixel) using the
palette below, so tweaking her look is just editing letters and colors.
Run:  python3 tools/hannah_sprite.py
Also writes tools/hannah_preview.png (8x scale, both outfits) to eyeball the result.

Sheet layout (12 frames in one row):
  0-2  down  (idle, walk A, walk B)
  3-5  up
  6-8  right
  9-11 left  (mirror of right)
"""

import os

from pixel import check, mirror, render, root, write_png

PALETTE = {
    ".": None,          # transparent
    "o": "#2b1d1a",     # outline
    "H": "#3b2219",     # hair, dark brown
    "h": "#5e3a28",     # hair highlight
    "S": "#d9a066",     # skin, tan/golden
    "s": "#b8804e",     # skin shadow
    "e": "#2b1d1a",     # eyes
    "b": "#e8917e",     # blush
    "m": "#b05a4a",     # mouth
    "g": "#f2c14e",     # gold earrings
    "T": "#946144",     # top, warm brown
    "t": "#77492f",     # top shadow
    "J": "#6a8cc4",     # straight-leg jeans, medium wash
    "j": "#4f6ea3",     # jeans seams / shading
    "R": "#c8323a",     # red purse
    "r": "#8e1f26",     # purse strap / shading
    "F": "#4a2a2a",     # shoes
    "M": "#7d1f2c",     # graduation gown, Loyola maroon
    "n": "#5a1520",     # gown folds
    "C": "#1f1a1e",     # mortarboard
    "Y": "#e8b83e",     # tassel / stole, gold
}

W, H = 16, 24

FRONT = [
    "....oooooooo....",
    "...oHHHHHHHHo...",
    "..oHHhhHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHSSSSSSHHo..",
    "..oHSSSSSSSSHo..",
    "..oHSeSSSSeSHo..",
    "..oHSeSSSSeSHo..",
    "..oHSbSSSSbSHo..",
    "..gHHSSmmSSHHg..",
    "..oHHoSSSSoHHo..",
    "..oHHHoSSoHHHo..",
    "..oHHTTTTTTHHo..",
    ".oHHTTTTTTTTrHo.",
    ".oSoTTTTTTTroSo.",
    ".oSotTTTTTTroSo.",
    ".oSoJJJJJJJRRRo.",
    "..ooJJJJJJJRrRo.",
    "...oJJJjJJJRRRo.",
    "...oJJJJjJJJo...",
]

BACK = [
    "....oooooooo....",
    "...oHHHHHHHHo...",
    "..oHHHhhHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHhHHHHhHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..gHHHHHHHHHHg..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    ".oTHHHHHHHHHHTo.",
    ".oSorTTHHTTToSo.",
    ".oSorTTTTTTtoSo.",
    ".oRRRJJJJJJJoSo.",
    "..oRrRJJJJJJo...",
    "..oRRRJjJJJJo...",
    "...oJJJJjJJJo...",
]

SIDE = [
    ".....oooooo.....",
    "....oHHHHHHo....",
    "...oHHHHhhHHo...",
    "...oHHHHHHHHo...",
    "...oHHHHHHSSo...",
    "...oHHHHHSSSo...",
    "...oHHHHSSeSo...",
    "...oHHHHSSeSo...",
    "...oHHHHSSSbo...",
    "...oHHHHgSSmo...",
    "...oHHHHHoSSo...",
    "...oHHHHHoSo....",
    "...oHHHHTTTo....",
    "...oHHHTTTTTo...",
    "...oHHTTTsTTo...",
    "...otTTTTsTTo...",
    "...oJJJJJSJo....",
    "...oJJJJJJJo....",
    "...oJJJJjJJo....",
    "...oJJJJJJJo....",
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


# ---------- graduation outfit: cap replaces the top of her hair, gown replaces the body ----------

CAP_FRONT = [
    "..oooooooooooo..",
    ".oCCCCCCCCCCCCo.",
    "..oooCCCCCCoooY.",
    "..oHHCCCCCCHHoY.",
    "..oHHSSSSSSHHoY.",
]

CAP_BACK = CAP_FRONT[:4] + ["..oHHHHHHHHHHoY."]

CAP_SIDE = [
    "...oooooooooo...",
    "..oCCCCCCCCCCo..",
    "..YooCCCCCCoo...",
    "..YoHCCCCCCHo...",
    "..YoHHHHHHSSo...",
]

GOWN_FRONT = [
    "..oHHMYMMYMHHo..",
    ".oHHMYMMMMYMHHo.",
    ".oMoMYMMMMYMoMo.",
    ".oMoMYMMMMYMoMo.",
    ".oSoMYMMMMYMoSo.",
    "..oMMMMMMMMMMo..",
    "..oMMMnMMnMMMo..",
    "..oMMMnMMnMMMo..",
]

GOWN_BACK = [
    "..oHHHHHHHHHHo..",
    ".oMHHHHHHHHHHMo.",
    ".oMoMMHHHHMMoMo.",
    ".oMoMMMMMMMMoMo.",
    ".oSoMMMMMMMMoSo.",
    "..oMMMMMMMMMMo..",
    "..oMMMnMMnMMMo..",
    "..oMMMnMMnMMMo..",
]

GOWN_SIDE = [
    "...oHHHHMMMo....",
    "...oHHHMYMMMo...",
    "...oHHMMYMMMo...",
    "...onMMMYMMMo...",
    "...oMMMMYSMMo...",
    "..oMMMMMMMMMMo..",
    "..oMMnMMnMMnMo..",
    "..oMMnMMnMMnMo..",
]

# The gown reaches the ground, so walking just shows the shoes stepping out.
HEM_FRONT = ["..oMMMnMMnMMMo..", "..onMMMMMMMMno..", "..oooooooooooo.."]
GOWN_LEGS_FRONT = {
    "idle": HEM_FRONT + ["....oFo..oFo...."],
    "a": HEM_FRONT + ["...oFFo........."],
    "b": HEM_FRONT + [".........oFFo..."],
}
HEM_SIDE = ["..oMMnMMnMMnMo..", "..onMMMMMMMMno..", "..oooooooooooo.."]
GOWN_LEGS_SIDE = {
    "idle": HEM_SIDE + [".....oFFFo......"],
    "a": HEM_SIDE + ["...oFFo..oFFo..."],
    "b": HEM_SIDE + ["....oFFooFFo...."],
}


def frame(body, legs):
    return check(body + legs, W, H, PALETTE)


def build_frames(front, back, side, legs_front, legs_side):
    frames = []
    for body, legs in ((front, legs_front), (back, legs_front), (side, legs_side)):
        for key in ("idle", "a", "b"):
            frames.append(frame(body, legs[key]))
    frames += [mirror(f) for f in frames[6:9]]
    return frames


if __name__ == "__main__":
    outfits = {
        "hannah": build_frames(FRONT, BACK, SIDE, LEGS_FRONT, LEGS_SIDE),
        "hannah_gown": build_frames(
            CAP_FRONT + FRONT[5:12] + GOWN_FRONT,
            CAP_BACK + BACK[5:12] + GOWN_BACK,
            CAP_SIDE + SIDE[5:12] + GOWN_SIDE,
            GOWN_LEGS_FRONT,
            GOWN_LEGS_SIDE,
        ),
    }
    bg = (243, 230, 216, 255)
    preview = []
    for name, frames in outfits.items():
        write_png(os.path.join(root(), f"public/sprites/{name}.png"), render(frames, PALETTE, W, H))
        preview += render(frames, PALETTE, W, H, scale=8, gap=2, bg=bg)
    write_png(os.path.join(root(), "tools/hannah_preview.png"), preview)
    print(f"Wrote {len(outfits)} outfits")
