"""Generates the animals: public/sprites/critters.png

16x16 frames, in this order:
  0 pigeon standing, 1 pecking, 2 flying (wings up), 3 flying (wings down)
     (all facing right; the game flips them to face left)
  4 the stray cat sitting, 5 tail up, 6 blinking, 7-8 walking (facing left),
  9 lying down
The cat is the same black cat as the `cat` map tile in tools/tiles.py.
Run:  python3 tools/critter_sprite.py
"""

import os

from pixel import check, render, root, write_png

PALETTE = {
    ".": None,
    "o": "#2b1d1a",
    "G": "#9aa3ab", "g": "#6b7480",  # pigeon gray
    "n": "#5f8f7a",  # the green sheen on its neck
    "e": "#e8742a",  # pigeon eye
    "f": "#d9787a",  # pink feet
    "@": "#38343e", "$": "#4b4653",  # black cat, with a bit of sheen
    "V": "#e8c547",  # yellow cat eyes
    "!": "#c9707e",  # nose
    "L": "#38343e",  # paws
}

BLANK = "................"

PIGEON = [BLANK] * 7 + [
    ".........oo.....",
    "........oGGo....",
    "........oGeGoo..",
    "........onGo....",
    "...oooooonno....",
    "..oggGGGGGGo....",
    "...oggGGGGGo....",
    "....ooooooo.....",
    "......f.f.......",
]

PECK = [BLANK] * 11 + [
    "...ooooooo......",
    "..oggGGGGGoo....",
    "...oggGGGGnnoo..",
    "....oooooooGeGo.",
    "......f.f...oo..",
]

FLY_UP = [BLANK] * 3 + [
    "...o.....o......",
    "..oGo...oGo.....",
    "..oGGo.oGGo.....",
    "...oGGoGGo..oo..",
    "....oGGGo..oGGo.",
    "..oooggGGooGeGoo",
    ".oggGGGGGGnnGo..",
    "..oooggGGGGoo...",
    ".....ooooo......",
    BLANK, BLANK, BLANK, BLANK,
]

FLY_DOWN = [BLANK] * 7 + [
    "...........oo...",
    "..........oGGo..",
    "..oooooooonGeoo.",
    ".oggGGGGGGnGo...",
    "..oogGGGGGoo....",
    "....oGGGGo......",
    ".....oGGo.......",
    "......oo........",
    BLANK,
]

CAT = [BLANK] * 4 + [
    "....o...o.......",
    "...o@o.o@o......",
    "...o@@o@@o......",
    "...o@V@V@o......",
    "...o@@!@@o......",
    "....o@@@o.......",
    "....o@$$@o......",
    "...o@$@@$@o.oo..",
    "...o@$@@$@o.o@o.",
    "...o@@@@@@oo@o..",
    "....oLoooLooo...",
    BLANK,
]

CAT_TAIL = CAT[:9] + [
    "....o@@@o...oo..",
    "....o@$$@o..o@o.",
    "...o@$@@$@o.o@o.",
    "...o@$@@$@o.o@o.",
    "...o@@@@@@ooo@o.",
    "....oLoooLoooo..",
    BLANK,
]

CAT_BLINK = CAT[:7] + ["...o@o@o@o......"] + CAT[8:]

# Walking, facing left.
CAT_BODY = [BLANK] * 6 + [
    "..o.o...........",
    ".o@o@o.......oo.",
    ".o@V@@o.....o@o.",
    "o!@@@@ooooooo@o.",
    ".o@@@@@@$@@$@o..",
    "..o@$@@$@@$@@o..",
    "..o@@@@@@@@@@o..",
]
CAT_WALK_A = CAT_BODY + [
    "..o@o.o@oo@o.o@o",
    "..oLo.oLo.oLo.oo",
    BLANK,
]
CAT_WALK_B = CAT_BODY + [
    "...o@oo@o..o@o@o",
    "...oLooLo..oLoLo",
    BLANK,
]

CAT_LOAF = [BLANK] * 8 + [
    "....o...o.......",
    "...o@o.o@o......",
    "...o@@o@@oooo...",
    "...o@V@V@@@@@o..",
    "..oo@@!@@$@@$@o.",
    "..o@@@@@@@@@@@@o",
    "..oLLoooooooo@o.",
    "...oo.......oo..",
]


if __name__ == "__main__":
    frames = [check(rows, 16, 16, PALETTE, name) for name, rows in (
        ("pigeon", PIGEON), ("peck", PECK), ("fly up", FLY_UP), ("fly down", FLY_DOWN),
        ("cat", CAT), ("cat tail", CAT_TAIL), ("cat blink", CAT_BLINK),
        ("cat walk a", CAT_WALK_A), ("cat walk b", CAT_WALK_B), ("cat loaf", CAT_LOAF),
    )]
    write_png(os.path.join(root(), "public/sprites/critters.png"), render(frames, PALETTE, 16, 16))
    write_png(os.path.join(root(), "tools/critters_preview.png"), render(frames, PALETTE, 16, 16, scale=8, gap=2, bg=(200, 196, 190, 255)))
    print(f"Wrote {len(frames)} critters")
