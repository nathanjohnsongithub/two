"""Generates classmates in cap and gown: public/sprites/grads.png

One front-facing 16x24 frame per look in LOOKS. Run:  python3 tools/grad_sprite.py
"""

import os

from pixel import check, render, root, write_png

BASE = {
    ".": None,
    "o": "#2b1d1a",  # outline
    "e": "#2b1d1a",  # eyes
    "m": "#a8604e",  # mouth
    "C": "#1f1a1e",  # mortarboard
    "Y": "#e8b83e",  # tassel / stole
    "M": "#7d1f2c",  # gown
    "n": "#5a1520",  # gown folds
    "F": "#2b2626",  # shoes
}

# (hair, skin) for each classmate.
LOOKS = [
    ("#6b4a2f", "#f1c9a5"),
    ("#d9b25a", "#f3d2b8"),
    ("#1e1a18", "#8d5a3b"),
]

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

if __name__ == "__main__":
    # Each look gets its own letters for hair/skin so they can share one sheet.
    palette = dict(BASE)
    frames = []
    for i, (hair, skin) in enumerate(LOOKS):
        h, s = str(i * 2), str(i * 2 + 1)
        palette[h], palette[s] = hair, skin
        rows = [r.replace("H", h).replace("S", s) for r in FRONT]
        frames.append(check(rows, 16, 24, palette))
    write_png(os.path.join(root(), "public/sprites/grads.png"), render(frames, palette, 16, 24))
    print(f"Wrote {len(frames)} classmates")
