"""Generates Nathan's sprite: public/sprites/nathan.png (front-facing, 16x24).

PLACEHOLDER look until the real details are in. Run:  python3 tools/nathan_sprite.py
"""

import os

from pixel import check, render, root, write_png

PALETTE = {
    ".": None,
    "o": "#2b1d1a",  # outline
    "H": "#2e211c",  # hair
    "h": "#4a352c",  # hair highlight
    "S": "#e3b48c",  # skin
    "e": "#2b1d1a",  # eyes
    "m": "#b06a55",  # mouth
    "G": "#8a8f98",  # hoodie
    "g": "#6d727b",  # hoodie shade
    "J": "#3d4f73",  # jeans
    "j": "#2f3d5c",  # jeans shade
    "F": "#ececec",  # sneakers
}

FRONT = [
    "....oooooooo....",
    "...oHHHHHHHHo...",
    "..oHHHhhHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHSSSSSSSSHo..",
    "..oSSSSSSSSSSo..",
    "..oSSeSSSSeSSo..",
    "..oSSeSSSSeSSo..",
    "..oSSSSSSSSSSo..",
    "...oSSSmmSSSo...",
    "....oSSSSSSo....",
    ".....ooSSoo.....",
    "...oGGGGGGGGo...",
    "..oGGGgGGgGGGo..",
    ".oGGGGgGGgGGGGo.",
    ".oGoGGGGGGGGoGo.",
    ".oGoGGGGGGGGoGo.",
    ".oSoggggggggoSo.",
    "...oJJJJJJJJo...",
    "...oJJJJjJJJo...",
    "...oJJJooJJJo...",
    "...ojJJooJJjo...",
    "...oJJJooJJJo...",
    "...oFFo..oFFo...",
]

if __name__ == "__main__":
    frames = [check(FRONT, 16, 24, PALETTE)]
    write_png(os.path.join(root(), "public/sprites/nathan.png"), render(frames, PALETTE, 16, 24))
    print("Wrote nathan.png")
