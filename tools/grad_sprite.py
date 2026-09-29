"""Generates Hannah's classmates in cap and gown: public/sprites/grads.png

One front-facing 16x24 frame each, in this order (the frame number in
content.js): 0 Krisjanis (blonde, glasses), 1 Lexi (long blonde hair),
2 Micheal (short black hair). Run:  python3 tools/grad_sprite.py
"""

import os

from pixel import check, render, root, write_png

PALETTE = {
    ".": None,
    "o": "#2b1d1a",  # outline
    "e": "#2b1d1a",  # eyes
    "C": "#1f1a1e",  # mortarboard
    "Y": "#e8b83e",  # tassel / stole
    "M": "#7d1f2c",  # gown
    "n": "#5a1520",  # gown folds
    "F": "#2b2626",  # shoes
    "g": "#3a3f4a",  # glasses frames
    # Krisjanis
    "0": "#e3c46a", "1": "#f1c9a5", "2": "#a8604e",  # hair, skin, mouth
    # Lexi
    "3": "#ecd07a", "4": "#f3d2b8", "5": "#c0686a",
    "6": "#c9a24e",  # her hair's shading
    # Micheal
    "7": "#1e1a18", "8": "#7a4a2e", "9": "#4e2a1e",
    "p": "#8e5040",  # his lower lip
}

FRONT = [
    "..oooooooooooo..",
    ".oCCCCCCCCCCCCo.",
    "..oooCCCCCCoooY.",
    "..oHHCCCCCCHHoY.",
    "..oHSSSSSSSSHoY.",
    "..oSSSSSSSSSSo..",
    "..oSSeSSSSeSSo..",
    "..oSSeSSSSeSSo..",
    "..oSSSSSSSSSSo..",
    "...oSSSmmSSSo...",
    "....oSSSSSSo....",
    ".....ooSSoo.....",
    "...oMYMMMMYMo...",
    "..oMMYMMMMYMMo..",
    ".oMMMYMMMMYMMMo.",
    ".oMoMYMMMMYMoMo.",
    ".oMoMYMMMMYMoMo.",
    ".oSoMMMMMMMMoSo.",
    "..oMMMMMMMMMMo..",
    "..oMMMnMMnMMMo..",
    "..oMMMnMMnMMMo..",
    "..onMMMMMMMMno..",
    "..oooooooooooo..",
    "....oFo..oFo....",
]


def look(rows, hair, skin, mouth):
    return [r.replace("H", hair).replace("S", skin).replace("m", mouth) for r in rows]


def krisjanis():
    """Short blonde hair and glasses."""
    rows = list(FRONT)
    rows[6] = "..oggggSSggggo.."
    rows[7] = "..ogSeggggeSgo.."
    rows[8] = "..oggggSSggggo.."
    return look(rows, "0", "1", "2")


def lexi():
    """Long blonde hair falling over her gown."""
    rows = list(FRONT)
    rows[4:17] = [
        "..oHSSSSSSSSHoY.",
        "..oHSSSSSSSSHo..",
        "..oHSeSSSSeSHo..",
        "..oHSeSSSSeSHo..",
        "..oHSSSSSSSSHo..",
        "..oHHSSmmSSHHo..",
        "..oHHoSSSSoHHo..",
        "..oHHHoSSoHHHo..",
        "..oHHMYMMYMHHo..",
        ".oHHMMYMMYMMHHo.",
        ".oHhoMYMMYMohHo.",
        ".oMoMYMMMMYMoMo.",
        ".oMoMYMMMMYMoMo.",
    ]
    return [r.replace("h", "6") for r in look(rows, "3", "4", "5")]


def micheal():
    """Short black hair and fuller lips."""
    rows = list(FRONT)
    rows[9] = "...oSSmmmmSSo..."
    rows[10] = "....oSppppSo...."
    return look(rows, "7", "8", "9")


if __name__ == "__main__":
    frames = [check(rows, 16, 24, PALETTE, name) for name, rows in (
        ("krisjanis", krisjanis()), ("lexi", lexi()), ("micheal", micheal()),
    )]
    write_png(os.path.join(root(), "public/sprites/grads.png"), render(frames, PALETTE, 16, 24))
    write_png(os.path.join(root(), "tools/grads_preview.png"), render(frames, PALETTE, 16, 24, scale=10, gap=2, bg=(243, 230, 216, 255)))
    print(f"Wrote {len(frames)} classmates")
