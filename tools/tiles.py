"""Generates the 16x16 tileset: public/sprites/tiles.png + src/tileset.js

Tiles are drawn either from text grids (one character per pixel) or with a
few shape helpers. Run:  python3 tools/tiles.py
Also writes tools/tiles_preview.png (6x scale) to eyeball the result.
"""

import math
import os

from pixel import check, render, root, write_png

PALETTE = {
    ".": None,
    "o": "#2b1d1a",  # outline
    "W": "#4a3f3b", "w": "#5c504b",  # interior wall
    "G": "#9fd3e6", "g": "#dff3fa",  # glass
    "A": "#c99a6b", "a": "#b0845a",  # hardwood
    "K": "#ece6da", "k": "#cfc6b6",  # kitchen tile
    "X": "#dcd6cc", "x": "#a39788",  # counter top / cabinet
    "Z": "#c3c9cf", "z": "#8a939c",  # stainless steel
    "B": "#33302e",  # burner / dark
    "R": "#c8323a", "r": "#8e1f26",  # red
    "Y": "#f2c14e",  # gold / flame
    "T": "#8a5a3b", "t": "#6b4329",  # furniture wood
    "C": "#7a8fa6", "c": "#5f7188",  # couch / blanket
    "L": "#f6f3ec", "l": "#dcd5c8",  # linen
    "I": "#f4f4f2", "i": "#cfd3d6",  # ceramic
    "V": "#5d9c59", "v": "#3f7a3f", "h": "#7dbb6f",  # leaves
    "U": "#8f5a36",  # trunk / pot
    "N": "#86c270", "n": "#72ad5e",  # grass
    "E": "#dccba5", "e": "#c7b489",  # park path
    "S": "#cfcac2", "s": "#b5afa6",  # sidewalk
    "D": "#55565c", "d": "#4a4b50",  # road
    "Q": "#5fa8d3", "q": "#8cc6e6",  # water
    "H": "#4f8f47",  # hedge
    "M": "#a0523d", "m": "#7d3f2f",  # brick
    "F": "#b07548", "f": "#85562f",  # bench wood
    "4": "#c46e55", "5": "#a4573f",  # terracotta floor
    "@": "#e6b760", "$": "#c98f3a", "&": "#a86a2c",  # golden food
    "1": "#d8cdb6", "2": "#bfb296",  # limestone
    "u": "#6e4a33", "b": "#5a3b28",  # stage wood
    "O": "#e8742a",  # U-Haul orange
    "j": "#c79a5f", "J": "#a47a45", "y": "#e6cf9c",  # cardboard / tape
    "p": "#3f7a52", "P": "#2d5c3c",  # dumpster green
    "6": "#1f4a3a", "7": "#2e6650",  # Art Deco green (Carbide & Carbon)
    "8": "#1b2340", "9": "#2c3557", "3": "#f7d67a",  # night sky / skyline / warm light
    "0": "#7d1f2c", ")": "#5a1520",  # Loyola maroon
    "!": "#e0508a",  # pink (dragon fruit, flowers)
    "%": "#6fa58f", "^": "#4f8573", "(": "#8fc2ab",  # copper patina
    "*": "#9c7cc4",  # purple
    "+": "#2a9d8f", "-": "#1d6f65",  # jade
    "=": "#fff3b0",  # bright bulb
    "{": "#eadcc4", "}": "#d8c6a8",  # wallpaper
    "/": "#3b6fb6",  # blue
    "|": "#232329",  # iron / tires
}


class Tile:
    def __init__(self, w=16, h=16):
        self.w, self.h = w, h
        self.g = [["."] * w for _ in range(h)]

    def px(self, x, y, ch):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = ch
        return self

    def rect(self, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, ch)
        return self

    def fill(self, ch):
        return self.rect(0, 0, self.w - 1, self.h - 1, ch)

    def box(self, x0, y0, x1, y1, inner, edge="o"):
        self.rect(x0, y0, x1, y1, edge)
        return self.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, inner)

    def circle(self, cx, cy, r, ch):
        return self.where(lambda x, y: (x - cx) ** 2 + (y - cy) ** 2 <= r * r, ch)

    def where(self, test, ch):
        for y in range(self.h):
            for x in range(self.w):
                if test(x, y):
                    self.px(x, y, ch)
        return self

    def art(self, rows, x0=0, y0=0):
        """Paint a text grid (any size) at x0, y0; "." leaves pixels as they are."""
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                assert ch in PALETTE, f"unknown pixel {ch!r} in {row!r}"
                if ch != ".":
                    self.px(x0 + x, y0 + y, ch)
        return self

    def paste(self, other, x0=0, y0=0):
        return self.art(other.rows(), x0, y0)

    def transpose(self):
        """Flip across the diagonal: turns a sideways piece into an upright one."""
        self.g = [list(col) for col in zip(*self.g)]
        self.w, self.h = self.h, self.w
        return self

    def mirror(self):
        self.g = [row[::-1] for row in self.g]
        return self

    def split(self):
        """Cut a wide piece into 16x16 tiles, left to right."""
        parts = []
        for x0 in range(0, self.w, 16):
            part = Tile()
            part.g = [row[x0:x0 + 16] for row in self.g]
            parts.append(part)
        return parts

    def rows(self):
        return ["".join(r) for r in self.g]


# ---------- floors ----------

def wood():
    t = Tile().fill("A").where(lambda x, y: y % 4 == 3, "a")
    return t.where(lambda x, y: y % 4 != 3 and x == (y // 4 * 5 + 3) % 16, "a")


def kitchen():
    return Tile().fill("K").where(lambda x, y: x % 8 == 0 or y % 8 == 0, "k")


def rug():
    return Tile().fill("R").where(lambda x, y: (x + y) % 8 == 0 or (x - y) % 8 == 0, "r")


def grass():
    return Tile().fill("N").where(lambda x, y: (x * 7 + y * 13) % 11 == 0, "n")


def path():
    return Tile().fill("E").where(lambda x, y: (x * 5 + y * 3) % 7 == 0, "e")


def sidewalk():
    return Tile().fill("S").where(lambda x, y: x == 15 or y == 15, "s")


def road():
    return Tile().fill("D").where(lambda x, y: (x * 3 + y * 7) % 13 == 0, "d")


def crosswalk():
    return road().where(lambda x, y: x % 6 in (1, 2, 3) and 1 <= y <= 14, "I")


def terracotta():
    t = Tile().fill("4").where(lambda x, y: x % 8 == 7 or y % 8 == 7, "5")
    return t


# ---------- walls ----------

def wall():
    return Tile().fill("W").where(lambda x, y: (x * 3 + y * 5) % 17 == 0, "w")


def window():
    t = wall().rect(1, 4, 14, 11, "w").rect(2, 5, 13, 10, "G")
    return t.px(3, 6, "g").px(4, 6, "g").px(3, 7, "g")


def brick():
    t = Tile().fill("M").where(lambda x, y: y % 4 == 3, "m")
    return t.where(lambda x, y: (x + (4 if (y // 4) % 2 else 0)) % 8 == 7, "m")


def hedge():
    """Leafy clumps lit from the top left. They wrap around, so hedges tile seamlessly."""
    t = Tile().fill("V")
    for y in range(16):
        for x in range(16):
            for cx, cy in ((4, 4), (12, 4), (0, 12), (8, 12)):
                dx, dy = (x - cx + 8) % 16 - 8, (y - cy + 8) % 16 - 8
                d = dx * dx + dy * dy
                if d <= 4 and dx + dy <= -1:
                    t.px(x, y, "h")
                elif 7 <= d <= 13 and dx + dy >= 2:
                    t.px(x, y, "v")
    return t


# ---------- doors ----------

def door():
    t = Tile().box(1, 0, 14, 15, "T").rect(4, 3, 11, 6, "t").rect(4, 9, 11, 13, "t")
    return t.px(11, 8, "Y").px(12, 8, "Y")


def door_open():
    return Tile().box(1, 0, 14, 15, "B").rect(2, 12, 13, 14, "d")


def subway():
    t = Tile().box(2, 2, 13, 15, "z")
    t.where(lambda x, y: 3 <= x <= 12 and y >= 3 and y % 3 == 0, "o")
    t.rect(1, 2, 1, 15, "v").rect(14, 2, 14, 15, "v")
    return t.circle(1, 1, 1.2, "V").circle(14, 1, 1.2, "V")


# ---------- kitchen ----------

def counter():
    t = Tile().rect(0, 0, 15, 10, "X").rect(0, 11, 15, 11, "o").rect(0, 12, 15, 15, "x")
    return t.rect(7, 12, 7, 15, "o").px(5, 13, "z").px(9, 13, "z")


def sink():
    t = counter().box(3, 2, 12, 9, "Z").rect(4, 3, 11, 3, "z")
    return t.px(7, 1, "o").px(8, 1, "o").px(7, 2, "o")


def stove():
    return Tile().art([
        "oooooooooooooooo",
        "oZZZZZZZZZZZZZZo",
        "oZZBBZZZZZZBBZZo",
        "oZBzzBZZZZBzzBZo",
        "oZBzzBZZZZBzzBZo",
        "oZZBBZZZZZZBBZZo",
        "oZZZZZZZZZZZZZZo",
        "oZZBBZZZZZZBBZZo",
        "oZBzzBZZZZBzzBZo",
        "oZBzzBZZZZBzzBZo",
        "oZZBBZZZZZZBBZZo",
        "oZZZZZZZZZZZZZZo",
        "oooooooooooooooo",
        "ozzzzzzzzzzzzzzo",
        "ozzoooooooooozzo",
        "oooooooooooooooo",
    ])


def stove_pot():
    """Stove with dinner still cooking: a pot of carbonara and a steak in the pan."""
    t = stove().circle(4.5, 4.5, 3.6, "o").circle(4.5, 4.5, 2.8, "Z").circle(4.5, 4.5, 2, "@")
    t.px(4, 4, "L").px(5, 3, "L").px(3, 5, "$")
    t.circle(10.5, 9, 3.2, "o").circle(10.5, 9, 2.4, "B").rect(9, 8, 12, 10, "t").rect(10, 8, 11, 9, "T")
    return t.rect(13, 9, 14, 9, "o")


def fridge():
    t = Tile().box(1, 0, 14, 15, "Z").rect(2, 5, 13, 5, "o")
    return t.rect(11, 2, 11, 3, "z").rect(11, 7, 11, 11, "z")


# ---------- furniture ----------

def table():
    return Tile().box(1, 2, 14, 12, "T").rect(2, 11, 13, 11, "t").px(2, 13, "o").px(13, 13, "o")


def table_candle():
    """Candlelit dinner for two: white tablecloth, two plates, candles and a rose."""
    t = table().rect(2, 3, 13, 10, "L").rect(2, 10, 13, 10, "l")
    for x0 in (2, 10):
        t.art([".ii.", "iIIi", "iIIi", ".ii."], x0, 5)
    for x in (6, 9):
        t.px(x, 3, "Y").px(x, 4, "3").px(x, 5, "I").px(x, 6, "i")
    return t.px(7, 7, "R").px(8, 7, "R").px(7, 8, "r").px(8, 8, "R").px(8, 9, "V")


def table_empty_plate():
    """A licked-clean dumpling plate: crumbs and a pair of chopsticks."""
    t = table().circle(6.5, 7, 4, "i").circle(6.5, 7, 3.2, "I")
    for x, y, ch in ((5, 6, "&"), (7, 8, "$"), (6, 5, "$"), (8, 6, "&"), (4, 8, "$")):
        t.px(x, y, ch)
    for i in range(5):
        t.px(9 + i, 3 + i, "t").px(10 + i, 3 + i, "t")
    return t


def chair():
    return Tile().art([
        "................",
        "................",
        "....oooooooo....",
        "....oTTTTTTo....",
        "....otttttto....",
        "....oooooooo....",
        "....oTTTTTTo....",
        "....oTTTTTTo....",
        "....oTTTTTTo....",
        "....otttttto....",
        "....oooooooo....",
        "....o......o....",
        "....o......o....",
        "................",
        "................",
        "................",
    ])


def couch(left, right):
    t = Tile().rect(0, 1, 15, 13, "o").rect(0, 2, 15, 6, "c").rect(0, 7, 15, 12, "C")
    t.where(lambda x, y: x % 5 == 4 and 7 <= y <= 12, "c")
    if left:
        t.rect(0, 1, 0, 13, "o").rect(1, 2, 3, 12, "c")
    if right:
        t.rect(15, 1, 15, 13, "o").rect(12, 2, 14, 12, "c")
    return t


# Beds join sideways: "left"/"right" halves drop the outline on the shared edge.
def bed_top(side="solo"):
    x0 = 0 if side == "right" else 1
    x1 = 15 if side == "left" else 14
    t = Tile().rect(x0, 0, x1, 15, "o").rect(x0 + (side != "right"), 1, x1 - (side != "left"), 2, "T")
    t.rect(x0 + (side != "right"), 3, x1 - (side != "left"), 15, "L")
    t.box(3, 4, 12, 8, "I", edge="l")
    return t.rect(x0 + (side != "right"), 11, x1 - (side != "left"), 15, "C").rect(x0 + (side != "right"), 11, x1 - (side != "left"), 11, "L")


def bed_bottom(side="solo"):
    x0 = 0 if side == "right" else 1
    x1 = 15 if side == "left" else 14
    t = Tile().rect(x0, 0, x1, 14, "o")
    return t.rect(x0 + (side != "right"), 0, x1 - (side != "left"), 13, "C").rect(x0 + (side != "right"), 13, x1 - (side != "left"), 13, "c")


def tub():
    t = Tile().box(0, 0, 15, 14, "I").rect(2, 2, 13, 12, "i").rect(3, 3, 12, 11, "Q")
    return t.px(5, 5, "q").px(6, 5, "q").px(9, 8, "q").px(10, 8, "q")


def toilet():
    return Tile().art([
        "................",
        "....oooooooo....",
        "....oIIIIIIo....",
        "....oiiiiiio....",
        "....oooooooo....",
        "....oIIIIIIo....",
        "...oIIIIIIIIo...",
        "...oIIiiiiIIo...",
        "...oIiQQQQiIo...",
        "...oIiQQQQiIo...",
        "...oIIiiiiIIo...",
        "....oIIIIIIo....",
        ".....oooooo.....",
        "................",
        "................",
        "................",
    ])


def washer():
    t = Tile().box(1, 1, 14, 15, "I").rect(2, 2, 13, 4, "i")
    return t.circle(7.5, 9.5, 3.6, "z").circle(7.5, 9.5, 2.6, "G").px(11, 3, "o")


def tv():
    t = Tile().box(1, 2, 14, 10, "B").px(3, 4, "z").px(4, 4, "z").px(3, 5, "z")
    return t.box(4, 11, 11, 14, "T")


def plant():
    return Tile().art([
        "................",
        "......v..v......",
        "....vVv.vVv.....",
        "...vVVvvVVVv....",
        "..vVVVVvVVVVv...",
        "..vVVhVVVVhVv...",
        "...vVVVVVVVv....",
        "....vvVVVvv.....",
        ".....oooooo.....",
        ".....oUUUUo.....",
        ".....oUUUUo.....",
        "......oUUo......",
        "......oooo......",
        "................",
        "................",
        "................",
    ])


# ---------- outside ----------

def tree():
    return Tile().art([
        "....oooooooo....",
        "..ooVVVVVVVVoo..",
        ".oVVhhVVVVVVVVo.",
        ".oVhhVVVVVVVVVo.",
        "oVVhVVVVVVVVVVvo",
        "oVVVVVVVVVVVVVvo",
        "oVVVVVVVVVVVVvvo",
        "oVVVVVVVVVVVvvvo",
        ".ovVVVVVVVvvvvo.",
        ".oovvVVVVvvvvoo.",
        "...oovvvvvvoo...",
        ".....ooUUoo.....",
        "......oUUo......",
        "......oUUo......",
        ".....ooUUoo.....",
        "................",
    ])


def bench():
    t = Tile()
    for y in (3, 7, 11):
        t.rect(0, y, 15, y + 1, "F").rect(0, y + 2, 15, y + 2, "f")
    return t.rect(1, 3, 1, 14, "o").rect(14, 3, 14, 14, "o")


def water():
    return Tile().fill("Q").where(lambda x, y: y % 4 == 1 and (x + 2 * y) % 9 in (0, 1, 2), "q")


# A round paper lantern, 8 wide. Hangs overhead (see OVERHEAD).
LANTERN = [
    "..oYYo..",
    ".rRRRRr.",
    "rR!RRRRr",
    "RR!RRrRr",
    "RRRRRrRr",
    "rRRRRRRr",
    ".rRRRRr.",
    "..oYYo..",
    "...YY...",
    "...Y....",
]


def lantern():
    return Tile().rect(7, 0, 8, 2, "o").art(LANTERN, 4, 3)


def lanterns():
    """One stretch of a string of lanterns across the street (a lantern per tile)."""
    t = Tile().where(lambda x, y: y == 1 + round(2 * (1 - ((x - 7.5) / 7.5) ** 2)), "o")
    return t.art(LANTERN, 4, 4)


def storefront():
    t = Tile().where(lambda x, y: y <= 5, "R").where(lambda x, y: y <= 5 and (x // 2) % 2 == 1, "L")
    t.rect(0, 6, 15, 6, "o").box(0, 7, 15, 12, "G").px(2, 8, "g").px(3, 8, "g").px(2, 9, "g")
    return t.rect(0, 13, 15, 15, "M").rect(0, 14, 15, 14, "m")


# ---------- Loyola (chapter 3) ----------

def stone():
    t = Tile().fill("1").where(lambda x, y: y % 8 == 7, "2")
    return t.where(lambda x, y: (x + (4 if (y // 8) % 2 else 0)) % 8 == 7, "2")


def stone_window():
    """Arched window with a keystone and a sill."""
    return stone().art([
        "................",
        ".......11.......",
        ".....oo22oo.....",
        "....oGgGGGGo....",
        "...oGgGGGGGGo...",
        "...oGGGGoGGGo...",
        "...ogGGGoGGGo...",
        "...oGGGGoGGGo...",
        "...ooooooooooo..",
        "...oGGGGoGGGo...",
        "...oGGGGoGGGo...",
        "...oGGGGoGGGo...",
        "...ooooooooooo..",
        "..11111111111...",
        "..22222222222...",
        "................",
    ])


def stone_door():
    t = stone().rect(3, 3, 12, 15, "o").rect(4, 4, 11, 15, "T").px(3, 3, "1").px(12, 3, "1")
    return t.rect(7, 4, 8, 15, "t").px(6, 10, "Y").px(9, 10, "Y")


def stage():
    return Tile().fill("u").where(lambda x, y: y % 4 == 3, "b").where(lambda x, y: y % 4 != 3 and x == (y // 4 * 7 + 2) % 16, "b")


def folding_chair():
    """White ceremony chair, seen from behind (facing the stage)."""
    return Tile().art([
        "................",
        "................",
        "................",
        "....oooooooo....",
        "....oIIIIIIo....",
        "....oIIIIIIo....",
        "....oiiiiiio....",
        "....oooooooo....",
        ".....o....o.....",
        "...oooooooooo...",
        "...oiiiiiiiio...",
        "...oooooooooo...",
        "....o......o....",
        "....o......o....",
        "....o......o....",
        "................",
    ])


def chair_cap():
    """His graduation cap left hanging on a ceremony chair, tassel and all."""
    return folding_chair().art([
        "..oooooooooooo..",
        "..oBBBBBBBBBBo..",
        "..oooooBYoooooo.",
        "....oBBBBBBoY...",
        "....oiiiiiio.Y..",
        "....oooooooo.Y..",
        ".............YY.",
    ], 0, 1)


def stage_skirt():
    """Front of the stage: maroon skirting with gold trim."""
    t = Tile().rect(0, 10, 15, 10, "Y").rect(0, 11, 15, 15, "0")
    return t.where(lambda x, y: y >= 11 and x % 4 == 1, ")")


def podium():
    """Lectern with the university seal on the front."""
    return Tile().art([
        "................",
        "..........oo....",
        ".........o......",
        "...oooooooooo...",
        "...oTTTTTTTTo...",
        "...oooooooooo...",
        "....o000000o....",
        "....o00YY00o....",
        "....o0Y00Y0o....",
        "....o0Y00Y0o....",
        "....o00YY00o....",
        "....o000000o....",
        "....o000000o....",
        "...oTTTTTTTTo...",
        "...oooooooooo...",
        "................",
    ])


def walkway():
    """Campus pavers in a running bond."""
    t = Tile().fill("1").where(lambda x, y: y % 4 == 3, "2")
    return t.where(lambda x, y: y % 4 != 3 and x % 8 == (0 if (y // 4) % 2 else 4), "2")


def roof(copper=False, eave=False):
    """Clay tile roof (barrel tiles running down the slope), or a copper one with
    standing seams. The bottom row of a roof gets eaves (see BOTTOMS in main.js)."""
    base, dark, light = ("%", "^", "(") if copper else ("M", "m", "4")
    t = Tile().fill(base).where(lambda x, y: x % 4 == 0, dark).where(lambda x, y: x % 4 == 1, light)
    if not copper:
        t.where(lambda x, y: y % 4 == 3 and x % 4 != 1, dark)
    if eave:
        t.rect(0, 13, 15, 13, dark).rect(0, 14, 15, 14, "o").rect(0, 15, 15, 15, "2")
    return t


def roof_cross(side, top=False):
    """A gold cross on the chapel's copper roof, two tiles wide so it sits in the
    middle; top=True is the part that rises above the roof."""
    t = Tile() if top else roof(copper=True)
    x = 15 if side == "L" else 0
    if top:
        t.rect(x, 6, x, 15, "Y")
        return t.rect(x - 3 if side == "L" else 0, 9, x if side == "L" else 3, 9, "Y")
    return t.rect(x, 0, x, 5, "Y").rect(x, 6, x, 6, "o")


def dome():
    """A copper dome on the roof, two tiles wide (like the one on Cudahy Science Hall)."""
    t = Tile(32, 16)
    t.paste(roof()).paste(roof(), 16, 0)
    t.box(8, 11, 23, 15, "1").where(lambda x, y: 12 <= y <= 14 and x % 3 == 1 and 9 <= x <= 22, "o")
    for y in range(3, 12):
        for x in range(32):
            dx, dy = (x - 15.5) / 7.5, (y - 11) / 8
            if dx * dx + dy * dy > 1:
                continue
            edge = dx * dx + dy * dy > 0.8
            t.px(x, y, "o" if edge else "(" if dx < -0.35 else "^" if dx > 0.45 else "^" if x % 4 == 3 else "%")
    return t.rect(15, 0, 16, 2, "Y").rect(14, 2, 17, 3, "o").split()


def chapel_window(part):
    """A tall stained-glass window, two tiles high (N is the top half)."""
    t = stone()
    for y in range(16):
        Y = y if part == "N" else y + 16
        for x in range(4, 12):
            half = {2: 0, 3: 1, 4: 2}.get(Y, 3)
            left, right = 8 - half, 7 + half
            if Y < 2 or Y > 30 or x < left - 1 or x > right + 1:
                continue
            if Y == 2 or Y == 29 or x in (left - 1, right + 1):
                t.px(x, y, "o")
            elif Y == 30:
                t.px(x, y, "1")
            elif Y % 5 == 0:
                t.px(x, y, "o")
            elif x in (7, 8):
                t.px(x, y, "R" if (Y // 5) % 2 else "Y")
            else:
                t.px(x, y, "*" if x in (5, 10) and (Y // 5) % 2 else "/")
    return t


def rose_window():
    """A round stained-glass window, two tiles wide."""
    t = Tile(32, 16)
    t.paste(stone()).paste(stone(), 16, 0)
    for y in range(16):
        for x in range(32):
            dx, dy = x - 15.5, y - 7.5
            d = math.hypot(dx, dy)
            if d > 7.6:
                continue
            if d > 6.6:
                t.px(x, y, "1")
            elif d > 5.8:
                t.px(x, y, "o")
            elif d < 1.6:
                t.px(x, y, "Y")
            elif 2.9 < d < 3.7:
                t.px(x, y, "o")
            else:
                sector = int((math.atan2(dy, dx) + math.pi) / (math.pi / 4)) % 8
                spoke = abs(math.atan2(dy, dx) * 4 / math.pi - round(math.atan2(dy, dx) * 4 / math.pi)) < 0.12
                t.px(x, y, "o" if spoke else "R" if d <= 2.9 else "/*"[sector % 2])
    return t.split()


def chapel_door():
    """Tall arched double doors, two tiles wide."""
    t = Tile(32, 16)
    t.paste(stone()).paste(stone(), 16, 0)
    for y in range(16):
        for x in range(32):
            dx = x - 15.5
            inside = abs(dx) <= 9.5 and (y >= 5 or dx * dx / 90.25 + (y - 5) ** 2 / 16 <= 1)
            frame = abs(dx) <= 10.5 and (y >= 4 or dx * dx / 110.25 + (y - 5) ** 2 / 25 <= 1)
            if inside:
                t.px(x, y, "t" if int(abs(dx)) % 3 == 0 else "T")
            elif frame:
                t.px(x, y, "o")
    t.rect(15, 3, 16, 15, "o").px(13, 10, "Y").px(18, 10, "Y")
    return t.split()


def lamppost_banner(top=False):
    """Campus lamppost with a maroon-and-gold banner for graduation day."""
    t = lamppost_top() if top else lamppost()
    if top:
        return t.rect(9, 11, 12, 11, "|").rect(9, 12, 12, 15, "0").rect(10, 13, 10, 15, "Y")
    return t.rect(9, 0, 12, 6, "0").rect(10, 0, 10, 5, "Y").px(9, 7, "0").px(12, 7, "0")


def stone_banner():
    """A maroon banner hanging on a stone wall."""
    t = stone().rect(4, 0, 11, 0, "|")
    t.rect(5, 1, 10, 12, "0").rect(5, 1, 5, 12, ")").rect(7, 2, 8, 11, "Y").rect(7, 4, 8, 4, "0")
    return t.px(6, 13, "0").px(9, 13, "0").px(5, 13, ")").px(10, 13, ")")


def flower_bed():
    """A low hedge with flowers, for along buildings and paths."""
    return Tile().art([
        "................",
        "................",
        "................",
        "..oooo.oooo.ooo.",
        ".oVhVVoVhVVoVhVo",
        "oVhVRVVhVYVVhVIo",
        "oVVYVVVVIVVRVVVo",
        "oVRVVIVVVVRVYVvo",
        "oVVVVVYVRVVVVVvo",
        "ovVIVVVVVVIVVvvo",
        "ovvVVRVvVVVVvvvo",
        "oovvvvvvvvvvvvoo",
        "oUUUUUUUUUUUUUUo",
        "otttttttttttttto",
        "oooooooooooooooo",
        "................",
    ])


def balloons(top=False):
    """Maroon and gold balloons tied to a weight; the balloons float in the tile above."""
    if not top:
        t = Tile().where(lambda x, y: y <= 11 and x in (6 + (y > 6), 8, 10 - (y > 6)), "o")
        return t.rect(6, 12, 9, 14, "z").rect(6, 12, 9, 12, "Z")
    t = Tile()
    for cx, cy, ch in ((5, 5, "0"), (10, 4, "Y"), (7.5, 9, "Y"), (3, 10, "I"), (12, 9.5, "0")):
        t.circle(cx, cy, 2.6, ch).px(int(cx) - 1, int(cy) - 1, "I" if ch != "I" else "l")
    return t.where(lambda x, y: y >= 12 and x in (6, 8, 10), "o")


def loyola_sign():
    """Stone monument sign with the school's initials on a maroon plaque."""
    t = Tile().box(1, 3, 14, 13, "0").rect(1, 3, 14, 4, "1").rect(1, 12, 14, 13, "1").rect(1, 14, 14, 14, "2")
    t.rect(1, 3, 14, 3, "o").rect(0, 3, 0, 14, "o").rect(15, 3, 15, 14, "o").rect(0, 15, 15, 15, "o")
    for i, letter in enumerate((["#..", "#..", "#..", "#..", "###"], ["#.#", "#.#", "#.#", "#.#", "###"],
                                ["###", "#..", "#..", "#..", "###"])):
        for dy, row in enumerate(letter):
            for dx, p in enumerate(row):
                if p == "#":
                    t.px(3 + i * 4 + dx, 6 + dy, "Y")
    return t


def sailboat():
    """A little sailboat out on the lake."""
    return water().art([
        "................",
        "................",
        "........o.......",
        "........oI......",
        "........oII.....",
        ".......IoIII....",
        "......IIoIIII...",
        ".....IIIoIIIII..",
        "....IIIIoIIIIII.",
        "........o.......",
        "...ooooooooooo..",
        "...oTTTTTTTTTo..",
        "....otttttttto..",
        "...qq.ooooooo.qq",
        "................",
        "................",
    ])


# ---------- moving day (chapter 4) ----------

def uhaul(part, side):
    """2-wide truck, cab facing down. part: back (open doors), closed, body, cab."""
    t = Tile().fill("I")
    edge = 0 if side == "L" else 15
    inner = 1 if side == "L" else 14
    if part in ("back", "closed"):
        t.rect(0, 0, 15, 0, "o")
    if part == "back":
        t.rect(0 if side == "R" else 2, 2, 15 if side == "L" else 13, 15, "B")
        t.rect(0 if side == "R" else 3, 10, 15 if side == "L" else 12, 15, "d")  # ramp
    if part == "closed":
        t.where(lambda x, y: y % 3 == 2, "i").rect(0, 1, 15, 2, "O")
    if part == "body":
        t.rect(inner, 0, inner, 15, "O").where(lambda x, y: y in (0, 8), "i")
    if part == "cab":
        t.rect(0, 0, 15, 2, "i").rect(0 if side == "R" else 2, 4, 15 if side == "L" else 13, 9, "G")
        t.px(3 if side == "L" else 12, 5, "g").rect(0, 11, 15, 14, "O").rect(0, 15, 15, 15, "o")
    t.rect(edge, 0, edge, 15, "o")
    return t


def dumpster():
    t = Tile().box(0, 3, 15, 14, "p").rect(1, 4, 14, 6, "P").rect(0, 7, 15, 7, "o")
    return t.rect(2, 9, 13, 9, "P").px(2, 15, "o").px(13, 15, "o")


def box():
    t = Tile().box(2, 4, 13, 13, "j").rect(3, 8, 12, 8, "J").rect(7, 5, 8, 12, "y")
    return t.rect(3, 12, 12, 12, "J")


def fire_escape():
    t = brick().rect(1, 2, 14, 13, "o")
    return t.where(lambda x, y: 2 <= x <= 13 and 3 <= y <= 12 and not (y % 2 == 0 or x % 4 == 1), "m")


def front_door():
    """Their building's front door: double doors with a transom window, a stone
    surround and steps down to the sidewalk. Two tiles wide."""
    t = Tile(32, 16)
    t.paste(brick()).paste(brick(), 16, 0)
    t.rect(6, 0, 25, 13, "1").rect(7, 1, 24, 12, "o")
    t.rect(8, 2, 23, 4, "G").rect(15, 2, 16, 4, "o").px(9, 2, "g").px(10, 2, "g")
    t.rect(8, 6, 23, 12, "T").rect(15, 6, 16, 12, "o").rect(9, 7, 14, 9, "t").rect(17, 7, 22, 9, "t")
    t.px(13, 10, "Y").px(18, 10, "Y")
    return t.rect(4, 13, 27, 13, "2").rect(3, 14, 28, 14, "1").rect(3, 15, 28, 15, "2").split()


def car(body, shade):
    """A parked car seen from above, facing up. Two tiles tall: N is the front half."""
    t = Tile(16, 32)
    for y0 in (6, 21):
        t.rect(1, y0, 2, y0 + 4, "|").rect(13, y0, 14, y0 + 4, "|")
    t.box(2, 2, 13, 29, body)
    for x, y in ((2, 2), (13, 2), (2, 29), (13, 29)):
        t.px(x, y, ".")
    t.rect(12, 3, 12, 28, shade).rect(3, 3, 11, 3, shade)
    t.rect(3, 10, 12, 13, "c").rect(3, 23, 12, 25, "c").px(4, 11, "C").px(5, 10, "C").px(4, 23, "C")
    t.rect(4, 14, 4, 22, shade).rect(11, 14, 11, 22, shade)
    t.px(3, 3, "I").px(12, 3, "I").px(3, 28, "R").px(12, 28, "R")
    t.px(1, 12, body).px(14, 12, body)
    top, bottom = Tile(), Tile()
    top.g, bottom.g = t.g[:16], t.g[16:]
    return top, bottom


def cone():
    return Tile().art([
        "................",
        "................",
        "................",
        ".......oo.......",
        "......oOOo......",
        "......oIIo......",
        ".....oOOOOo.....",
        ".....oOOOOo.....",
        "....oIIIIIIo....",
        "....oOOOOOOo....",
        "...oOOOOOOOOo...",
        "..oooooooooooo..",
        "..oOOOOOOOOOOo..",
        "..oooooooooooo..",
        "................",
        "................",
    ])


# ---------- Chateau Carbide rooftop (chapter 5) ----------

def deck():
    return Tile().fill("A").where(lambda x, y: x % 4 == 3, "a").where(lambda x, y: x % 4 != 3 and y == (x // 4 * 9 + 5) % 16, "a")


def rail(vertical=False):
    t = deck()
    if vertical:
        t.rect(6, 0, 9, 15, "o").rect(7, 0, 8, 15, "T")
    else:
        t.rect(0, 6, 15, 9, "o").rect(0, 7, 15, 8, "T")
    return t


def skyline(buildings=((0, 3, 6), (4, 7, 3), (8, 10, 8), (11, 15, 5)), stars=((2, 1), (12, 3), (7, 0)),
            seed=0, antenna=None):
    """City towers against the night sky, with lit windows (and maybe an antenna)."""
    t = Tile().fill("8")
    for x, y in stars:
        t.px(x, y, "L")
    for x0, x1, top in buildings:
        t.rect(x0, top, x1, 15, "9")
        t.where(lambda x, y, x0=x0, x1=x1, top=top:
                x0 < x < x1 and y > top and y % 3 == 0 and (x * 7 + y * 3 + seed) % 5 < 2, "3")
    if antenna:
        x, y0 = antenna
        t.rect(x, y0, x, y0 + 3, "9").px(x, y0, "R")
    return t


def night_sky(stars):
    t = Tile().fill("8")
    for x, y, ch in stars:
        t.px(x, y, ch)
    return t


def moon():
    t = night_sky(((2, 12, "9"), (13, 2, "L")))
    t.circle(8, 7.5, 5.2, "9").circle(8, 7.5, 4.4, "L").circle(10.2, 6, 4, "8")
    return t


def city_lights():
    """Looking down past the railing: dark streets far below, dotted with lights."""
    t = Tile().fill("8").where(lambda x, y: x % 8 == 3 or y % 8 == 5, "9")
    for x, y, ch in ((3, 5, "3"), (11, 13, "3"), (3, 13, "Y"), (11, 5, "L"), (7, 5, "3"), (3, 1, "Y"), (14, 13, "3")):
        t.px(x, y, ch)
    return t


def bulbs():
    t = Tile().where(lambda x, y: y == 3 + ((x - 8) ** 2) // 40, "o")
    for x in (3, 11):
        y = 4 + ((x - 8) ** 2) // 40
        t.rect(x, y, x + 1, y + 1, "3").px(x, y + 2, "Y").px(x + 1, y + 2, "Y")
    return t


def deco_wall():
    return Tile().fill("6").where(lambda x, y: x % 8 in (1, 5), "7").where(lambda x, y: x % 8 == 3, "Y")


def deco_trim():
    """Gold Art Deco zigzag along the top of the green wall."""
    t = Tile().rect(0, 0, 15, 0, "Y").rect(0, 1, 15, 3, "6")
    return t.where(lambda x, y: 1 <= y <= 3 and (x + y) % 4 == 0, "Y").rect(0, 4, 15, 4, "Y")


def bar(piece):
    """The rooftop bar: green marble counter with a gold edge, drinks on top.
    A row of them joins up (L and R are the ends)."""
    t = Tile().rect(0, 7, 15, 7, "Y").rect(0, 8, 15, 9, "7").rect(0, 10, 15, 10, "6")
    t.rect(0, 11, 15, 14, "t").where(lambda x, y: 11 <= y <= 14 and x % 4 == 2, "T").rect(0, 15, 15, 15, "o")
    t.rect(0, 12, 15, 12, "Y")
    if piece == "L":
        t.rect(0, 7, 0, 15, "o")
    if piece == "R":
        t.rect(15, 7, 15, 15, "o")
    items = {
        "L": ["...o......o.....", "..oVo....o$o....", "..oVo....o$o....", "..ohVo..o$@$o...",
              "..oVVo..o$$$o...", "..oVVo..o$$$o..."],
        "M": ["................", "..ggggg...gg.gg.", "...g!g....g!!!g.", "....g......g!g..",
              "....g.......g...", "...ggg.....ggg.."],
        "R": ["........oo......", "...o...oZZo.....", "..oIo..oZZo..Y..", "..oIo..oZZo.YYY.",
              "..oIo..oZZo.YYY.", "..ooo..oooo..Y.."],
    }[piece]
    return t.art(items, 0, 1)


def bistro_table():
    """A little marble cafe table with a candle."""
    return Tile().art([
        "................",
        "................",
        ".......Y........",
        ".......3........",
        ".......I........",
        "...oooooooooo...",
        "..oLLLLiLLLLLo..",
        "..olllllllllio..",
        "...oooooooooo...",
        "......o||o......",
        "......o||o......",
        "......o||o......",
        ".....o||||o.....",
        "....oooooooo....",
        "................",
        "................",
    ])


def heater(top=False):
    """A tall patio heater; its glowing head sits in the tile above (heaterTop)."""
    if top:
        return Tile().art([
            "................",
            "................",
            "......oooo......",
            "....ooZZZZoo....",
            "..ooZZZZZZZZoo..",
            "..oooooooooooo..",
            ".....oO3O3o.....",
            ".....o3O3Oo.....",
            "......oooo......",
            ".......zZ.......",
            ".......zZ.......",
            ".......zZ.......",
            ".......zZ.......",
            ".......zZ.......",
            ".......zZ.......",
            ".......zZ.......",
        ])
    return Tile().art([
        ".......zZ.......",
        ".......zZ.......",
        ".......zZ.......",
        ".......zZ.......",
        ".......zZ.......",
        ".......zZ.......",
        ".......zZ.......",
        "......ozZo......",
        "......ozZo......",
        ".....ozzZZo.....",
        ".....ozzZZo.....",
        "....ozzzZZZo....",
        "....ozzzZZZo....",
        "...oooooooooo...",
        "................",
        "................",
    ])


def elevator():
    t = deco_wall().box(2, 2, 13, 15, "$", edge="Y").rect(7, 3, 8, 15, "o")
    return t.rect(3, 3, 12, 4, "Y").px(5, 5, "Y").px(10, 5, "Y")


# ---------- items (not placed in maps) ----------

def note():
    t = Tile().box(1, 4, 14, 12, "L")
    t.where(lambda x, y: 5 <= y <= 8 and (x - 2 == y - 5 or 13 - x == y - 5), "l")
    return t.rect(6, 8, 9, 9, "R").px(7, 10, "R").px(8, 10, "R").px(6, 8, "R").px(9, 8, "R")


# ---------- variety (alternate looks picked per cell, see VARIANTS) ----------

def grass_tuft():
    t = grass()
    for x, y in ((3, 10), (11, 3)):
        t.px(x, y, "v").px(x + 2, y, "v").px(x + 1, y + 1, "v").px(x + 1, y, "h")
    return t


def grass_flowers():
    t = grass()
    for x, y, petal in ((4, 4, "I"), (11, 10, "!"), (12, 3, "Y")):
        for dx, dy in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            t.px(x + dx, y + dy, petal)
        t.px(x, y, "&" if petal == "Y" else "Y")
    return t


def tree_wide():
    return Tile().art([
        "................",
        "...oooo..oooo...",
        "..oVhhVooVVVVo..",
        ".oVhhVVVVVVVVvo.",
        ".oVhVVVVVVVvVvo.",
        "oVVVVVVVVVVVVvvo",
        "oVhVVVVvVVVVvvvo",
        "oVVVVVVVVVVvvvvo",
        ".oVVVVVVVVvvvvo.",
        ".oovVVVVvvvvvoo.",
        "...oovvvvvvoo...",
        ".....ooUUoo.....",
        "......oUUo......",
        "......oUUo......",
        ".....ooUUoo.....",
        "................",
    ])


def water_sparkle():
    return water().px(4, 6, "g").px(5, 6, "g").px(5, 5, "q").px(11, 12, "g").px(12, 12, "q")


# ---------- trim (painted where two surfaces meet, see EDGES in main.js) ----------

def edge(side, bands):
    """Bands of color along one side of an empty tile, outermost first."""
    t = Tile()
    for i, ch in enumerate(bands):
        if side == "N":
            t.rect(0, i, 15, i, ch)
        elif side == "S":
            t.rect(0, 15 - i, 15, 15 - i, ch)
        elif side == "W":
            t.rect(i, 0, i, 15, ch)
        else:
            t.rect(15 - i, 0, 15 - i, 15, ch)
    return t


def cornice():
    """A stone ledge along the top of a brick building."""
    t = Tile().rect(0, 0, 15, 1, "1").rect(0, 2, 15, 2, "2")
    return t.where(lambda x, y: y == 3 and x % 3 == 0, "2")


# ---------- apartment (chapter 1) ----------

def wall_face():
    """The front of an interior wall: wallpaper over a baseboard."""
    t = wall().rect(0, 2, 15, 2, "o")
    t.rect(0, 3, 15, 12, "{").where(lambda x, y: 3 <= y <= 12 and x % 4 == 1, "}")
    return t.rect(0, 13, 15, 14, "T").rect(0, 15, 15, 15, "t")


def window_face():
    t = wall_face().box(3, 4, 12, 11, "G").rect(4, 7, 11, 7, "o")
    t.px(4, 5, "g").px(5, 5, "g").px(4, 6, "g").px(4, 8, "g")
    return t.rect(2, 12, 13, 12, "L")


def counter_side():
    """A counter along a right-hand wall, cabinets facing into the room."""
    return counter().transpose().mirror()


def wood_petals():
    """Hardwood with a few rose petals scattered on it."""
    t = wood()
    for x, y in ((3, 3), (11, 5), (6, 10), (12, 12)):
        t.art([".RR", "R!R", ".R."], x, y)
    return t


def nightstand():
    return Tile().art([
        "................",
        "................",
        "......oooo......",
        ".....o3333o.....",
        "....o333333o....",
        "....oooooooo....",
        "......oTTo......",
        "..oooooooooooo..",
        "..oTTTTTTTTTTo..",
        "..otttttttttto..",
        "..oTTTTTTTTTTo..",
        "..oTTTTYTTTTTo..",
        "..otttttttttto..",
        "..oooooooooooo..",
        "...o........o...",
        "................",
    ])


def menu_board():
    """Chalkboard easel with tonight's menu (and a heart)."""
    return Tile().art([
        "................",
        "..oooooooooooo..",
        "..oTTTTTTTTTTo..",
        "..oTBBBBBBBBTo..",
        "..oTBIlBIlIBTo..",
        "..oTBBBBBBBBTo..",
        "..oTBllBlllBTo..",
        "..oTBlBllBlBTo..",
        "..oTBBRBRBBBTo..",
        "..oTBRRRRRBBTo..",
        "..oTBBRRRBBBTo..",
        "..oTBBBRBBBBTo..",
        "..oTTTTTTTTTTo..",
        "..oooooooooooo..",
        "..o.o......o.o..",
        ".o...o....o...o.",
    ])


# ---------- New York (chapter 2) ----------

def lamppost():
    """Iron park lamppost; the lamp itself is lamppostTop, drawn in the tile above."""
    return Tile().art([
        ".......|B.......",
        ".......|B.......",
        ".......|B.......",
        ".......|B.......",
        ".......|B.......",
        ".......|B.......",
        ".......|B.......",
        ".......|B.......",
        "......o|Bo......",
        "......o|Bo......",
        ".......|B.......",
        "......o|Bo......",
        ".....o||BBo.....",
        ".....o||BBo.....",
        "....oooooooo....",
        "................",
    ])


def lamppost_top():
    return Tile().art([
        "................",
        "................",
        ".......oo.......",
        "......oBBo......",
        ".....oBBBBo.....",
        "....oooooooo....",
        ".....ogIggo.....",
        ".....oIgggo.....",
        ".....ogggGo.....",
        ".....oggGGo.....",
        "....oooooooo....",
        "......o|Bo......",
        ".......|B.......",
        ".......|B.......",
        ".......|B.......",
        ".......|B.......",
    ])


def water_boat():
    """A rowboat out on the lake."""
    return water().art([
        "................",
        "................",
        "................",
        "......T.........",
        ".......T........",
        "...oooooooooo...",
        "q.oTTtTTTtTTToo.",
        ".oTTTtTTTtTTTTTo",
        "q.oTTtTTTtTTToo.",
        "...oooooooooo...",
        ".......T........",
        "......T.........",
        "................",
        "................",
        "................",
        "................",
    ])


DUCK = [
    "....vv.",
    "o...vvO",
    "olllTT.",
    ".llll..",
    "qq..qq.",
]


def water_ducks():
    """Two mallards paddling around."""
    return water().art(DUCK, 2, 3).art(Tile(7, 5).art(DUCK).mirror().rows(), 8, 9)


def road_line():
    """Road with the double yellow line along its bottom edge (the middle of the street)."""
    return road().rect(0, 12, 15, 12, "Y").rect(0, 14, 15, 14, "Y")


def taxi(east=False):
    """A yellow cab seen from above, two tiles long, facing west (or east)."""
    t = Tile(32, 16)
    for x0 in (4, 22):
        t.rect(x0, 1, x0 + 3, 1, "|").rect(x0, 14, x0 + 3, 14, "|")
    t.box(1, 2, 30, 13, "Y")
    for x, y in ((1, 2), (30, 2), (1, 13), (30, 13)):
        t.px(x, y, ".")
    t.rect(2, 12, 29, 12, "$").rect(2, 3, 29, 3, "@")
    t.rect(9, 4, 11, 11, "c").rect(21, 4, 23, 11, "c").px(9, 4, "C").px(10, 5, "C").px(21, 4, "C")
    t.box(14, 6, 18, 9, "I")
    t.rect(2, 3, 2, 4, "I").rect(2, 11, 2, 12, "I").rect(29, 3, 29, 4, "R").rect(29, 11, 29, 12, "R")
    t.px(10, 1, "o").px(10, 14, "o")
    return (t.mirror() if east else t).split()


def hot_dog_cart():
    return Tile().art([
        "................",
        "......oooo......",
        "....oo/YY/oo....",
        "...o//YYYY//o...",
        "..o///YYYY///o..",
        ".o////YYYY////o.",
        ".oooooooooooooo.",
        ".......oo.......",
        "..oooooooooooo..",
        "..oZZZZZZZZZZo..",
        "..oYYYYYYYYYYo..",
        "..o//////////o..",
        "..ozzzzzzzzzzo..",
        "..oooooooooooo..",
        "...o|o....o|o...",
        "....o......o....",
    ])


# The made-up characters on Chinatown signs (5x5).
GLYPHS = [
    ["#####", "#.#.#", "#####", "#.#.#", "#####"],
    ["#####", "..#..", ".###.", "..#..", "#####"],
    ["..#..", "#####", "#.#.#", "#####", "..#.."],
    ["..#..", "#####", "..#..", ".#.#.", "#...#"],
    ["..#..", "#.#.#", "#.#.#", "#.#.#", "#####"],
    ["#####", "#...#", "#####", "#...#", "#####"],
]


def glyph(t, x0, y0, n, ch):
    for dy, row in enumerate(GLYPHS[n]):
        for dx, p in enumerate(row):
            if p == "#":
                t.px(x0 + dx, y0 + dy, ch)
    return t


def shop(sign, ink, marks, window):
    """A narrow Chinatown shop: a signboard with two characters over its window."""
    t = Tile().rect(0, 0, 15, 7, "o").rect(1, 1, 14, 6, sign)
    glyph(t, 2, 1, marks[0], ink)
    glyph(t, 9, 1, marks[1], ink)
    t.rect(0, 8, 0, 12, "o").rect(15, 8, 15, 12, "o").art(window, 1, 8)
    return t.rect(0, 13, 15, 13, "X").rect(0, 14, 15, 15, "m").rect(1, 14, 14, 14, "M")


def shop_red():
    return shop("R", "Y", (2, 3), [
        "GgGGoGGGGGoGGG",
        "gGGRRRGGGRRRGG",
        "GGGRrRGGGRrRGG",
        "GGGGYGGGGGYGGG",
        "Y00YY00YY00YY0",
    ])


def shop_jade():
    return shop("+", "Y", (5, 1), [
        "lrrlrrlrrlrrll",
        "lIIlIIlIIlIIll",
        "TTTTTTTTTTTTTT",
        "llrrlrrlrrlrrl",
        "llIIlIIlIIlIIl",
    ])


def shop_market():
    return shop("Y", "R", (0, 4), [
        "BBBBBBBBBBBBBB",
        "B@OBBB!!BBVhVB",
        "OOYOO!R!!VVhVV",
        "OYOOO!!!RVhVVV",
        "jJjjJjjJjjJjjJ",
    ])


def shop_ducks():
    return shop("R", "Y", (3, 5), [
        "oooooooooooooo",
        "l&lll&lll&llll",
        "$&&l$&&l$&&lll",
        "$&&l$&&l$&&lll",
        "l&lll&lll&llll",
    ])


def shop_bakery():
    return shop("!", "I", (1, 2), [
        "LLLLLLLLLLLLLL",
        "L@$L@$L@$L@$LL",
        "zzzzzzzzzzzzzz",
        "LI!LI!LI!LI!LL",
        "zzzzzzzzzzzzzz",
    ])


DUMPLING = [
    "..ooo..",
    ".oIiIo.",
    "oIiIiIo",
    "oIIIIIo",
    ".ooooo.",
]


def restaurant(piece):
    """The dumpling house: one long red sign over windows full of steamer baskets.
    A row of them joins up: L and R are the ends, Door goes in the middle, and
    the rest are M (or M2, for a different character on the sign)."""
    t = Tile().rect(0, 0, 15, 7, "o").rect(0, 1, 15, 6, "R")
    t.rect(0, 8, 15, 12, "3").rect(0, 13, 15, 13, "X").rect(0, 14, 15, 15, "m").rect(0, 14, 15, 14, "M")
    if piece == "L":
        t.rect(0, 0, 0, 12, "o")
    if piece == "R":
        t.rect(15, 0, 15, 12, "o")
    if piece == "Door":
        t.art(DUMPLING, 4, 1)
        t.rect(3, 8, 12, 15, "r").rect(4, 9, 11, 15, "T").rect(5, 10, 10, 12, "G").px(5, 10, "g")
        return t.rect(7, 9, 8, 15, "t").px(6, 13, "Y").px(9, 13, "Y")
    glyph(t, 5, 1, {"L": 2, "M": 3, "M2": 5, "R": 0}[piece], "Y")
    return t.art([
        "..JJJJ....JJJJ..",
        "..jjjj....jjjj..",
        "..JJJJ....JJJJ..",
        "..jjjj....jjjj..",
    ], 0, 9)


def brick_window(extra=None):
    """A tenement window: stone lintel and sill in a brick wall."""
    t = brick().rect(3, 2, 12, 2, "1").rect(4, 3, 11, 11, "o").rect(5, 4, 10, 10, "9")
    t.rect(5, 7, 10, 7, "o").px(5, 4, "C").px(6, 4, "C").px(5, 5, "C")
    t.rect(3, 12, 12, 12, "1").rect(4, 13, 11, 13, "m")
    if extra == "ac":
        t.box(5, 8, 10, 12, "Z").rect(6, 9, 9, 9, "z").rect(6, 11, 9, 11, "z")
    if extra == "plant":
        t.rect(4, 12, 11, 13, "T").art(["V!VhRV!V"], 4, 11)
    return t


def fire_escape_front():
    """A tenement window behind a fire escape landing, with stairs down to the next one."""
    t = brick_window().rect(0, 6, 15, 6, "|")
    t.where(lambda x, y: 7 <= y <= 11 and x % 3 == 1, "|")
    t.rect(0, 12, 15, 12, "|").rect(0, 13, 15, 13, "o")
    return t.where(lambda x, y: 13 <= y and 2 <= x <= 5 and x - 2 == y - 13, "|")


def fruit_stand():
    """A sidewalk fruit stand: oranges, dragon fruit and bok choy."""
    return Tile().art([
        "................",
        "................",
        "................",
        "................",
        "...@O....V.hV...",
        "..O@OO.!.VhVVh..",
        ".OOOOO!!!VVVVVV.",
        ".OOOOO!R!!IVIVV.",
        "oJjjJjJjjJjJjjJo",
        "ojjjjjjjjjjjjjjo",
        "oooooooooooooooo",
        "oTTTTTTTTTTTTTTo",
        "otttttttttttttto",
        "oooooooooooooooo",
        ".o.o........o.o.",
        ".o.o........o.o.",
    ])


# name -> (builder, solid). Order is the frame index in tiles.png.
TILES = {
    "wood": (wood, False),
    "kitchen": (kitchen, False),
    "rug": (rug, False),
    "grass": (grass, False),
    "path": (path, False),
    "sidewalk": (sidewalk, False),
    "road": (road, False),
    "crosswalk": (crosswalk, False),
    "terracotta": (terracotta, False),
    "wall": (wall, True),
    "window": (window, True),
    "brick": (brick, True),
    "hedge": (hedge, True),
    "door": (door, True),
    "doorOpen": (door_open, True),
    "subway": (subway, True),
    "counter": (counter, True),
    "sink": (sink, True),
    "stove": (stove, True),
    "stovePot": (stove_pot, True),
    "fridge": (fridge, True),
    "table": (table, True),
    "tableCandle": (table_candle, True),
    "tableEmptyPlate": (table_empty_plate, True),
    "chair": (chair, False),
    "couchL": (lambda: couch(True, False), True),
    "couchM": (lambda: couch(False, False), True),
    "couchR": (lambda: couch(False, True), True),
    # Upright couch (facing right), used when couch pieces are stacked vertically.
    "couchT": (lambda: couch(True, False).transpose(), True),
    "couchMV": (lambda: couch(False, False).transpose(), True),
    "couchB": (lambda: couch(False, True).transpose(), True),
    "bedTop": (bed_top, True),
    "bedTopL": (lambda: bed_top("left"), True),
    "bedTopR": (lambda: bed_top("right"), True),
    "bedBottom": (bed_bottom, True),
    "bedBottomL": (lambda: bed_bottom("left"), True),
    "bedBottomR": (lambda: bed_bottom("right"), True),
    "tub": (tub, True),
    "toilet": (toilet, True),
    "washer": (washer, True),
    "tv": (tv, True),
    "plant": (plant, True),
    "tree": (tree, True),
    "bench": (bench, True),
    "water": (water, True),
    "lantern": (lantern, False),
    "storefront": (storefront, True),
    "stone": (stone, True),
    "stoneWindow": (stone_window, True),
    "stoneDoor": (stone_door, True),
    "stage": (stage, False),
    "chairCap": (chair_cap, False),
    **{f"uhaul{part.title()}{side}": (lambda part=part, side=side: uhaul(part, side), True)
       for part in ("back", "closed", "body", "cab") for side in "LR"},
    "dumpster": (dumpster, True),
    "box": (box, False),
    "fireEscape": (fire_escape, True),
    "deck": (deck, False),
    "rail": (rail, True),
    "railV": (lambda: rail(vertical=True), True),
    "skyline": (skyline, True),
    "bulbs": (bulbs, False),
    "decoWall": (deco_wall, True),
    "elevator": (elevator, True),
    "note": (note, False),
    # variety
    "grassTuft": (grass_tuft, False),
    "grassFlowers": (grass_flowers, False),
    "tree2": (tree_wide, True),
    "waterSparkle": (water_sparkle, True),
    # trim
    **{f"shore{s}": (lambda s=s: edge(s, "Eq"), False) for s in "NSEW"},
    **{f"curb{s}": (lambda s=s: edge(s, "sI"), False) for s in "NSEW"},
    "corniceN": (cornice, False),
    # apartment
    "wallFace": (wall_face, True),
    "windowFace": (window_face, True),
    "counterV": (counter_side, True),
    "woodPetals": (wood_petals, False),
    "nightstand": (nightstand, True),
    "menuBoard": (menu_board, True),
    # New York
    "lamppost": (lamppost, True),
    "lamppostTop": (lamppost_top, False),
    "waterBoat": (water_boat, True),
    "waterDucks": (water_ducks, True),
    "roadLine": (road_line, False),
    "taxiL": (lambda: taxi()[0], True),
    "taxiR": (lambda: taxi()[1], True),
    "taxiEastL": (lambda: taxi(east=True)[0], True),
    "taxiEastR": (lambda: taxi(east=True)[1], True),
    "hotDogCart": (hot_dog_cart, True),
    "shopRed": (shop_red, True),
    "shopJade": (shop_jade, True),
    "shopMarket": (shop_market, True),
    "shopDucks": (shop_ducks, True),
    "shopBakery": (shop_bakery, True),
    **{f"restaurant{p}": (lambda p=p: restaurant(p), True) for p in ("L", "M", "M2", "R", "Door")},
    "brickWindow": (brick_window, True),
    "brickWindowAC": (lambda: brick_window("ac"), True),
    "brickWindowPlant": (lambda: brick_window("plant"), True),
    "fireEscapeFront": (fire_escape_front, True),
    "fruitStand": (fruit_stand, True),
    "lanterns": (lanterns, False),
    # Loyola
    "walkway": (walkway, False),
    "foldingChair": (folding_chair, False),
    "stageSkirtS": (stage_skirt, False),
    "podium": (podium, True),
    "roof": (roof, True),
    "roofEave": (lambda: roof(eave=True), True),
    "roofCopper": (lambda: roof(copper=True), True),
    "roofCopperEave": (lambda: roof(copper=True, eave=True), True),
    "ridgeN": (lambda: edge("N", "o"), False),
    **{f"roofCross{s}": (lambda s=s: roof_cross(s), True) for s in "LR"},
    **{f"roofCross{s}Top": (lambda s=s: roof_cross(s, top=True), False) for s in "LR"},
    **{f"chapelWindow{p}": (lambda p=p: chapel_window(p), True) for p in "NS"},
    "domeL": (lambda: dome()[0], True),
    "domeR": (lambda: dome()[1], True),
    "roseWindowL": (lambda: rose_window()[0], True),
    "roseWindowR": (lambda: rose_window()[1], True),
    "stoneDoorL": (lambda: chapel_door()[0], True),
    "stoneDoorR": (lambda: chapel_door()[1], True),
    "lamppostBanner": (lamppost_banner, True),
    "lamppostBannerTop": (lambda: lamppost_banner(top=True), False),
    "stoneBanner": (stone_banner, True),
    "flowerBed": (flower_bed, True),
    "balloons": (balloons, True),
    "balloonsTop": (lambda: balloons(top=True), False),
    "loyolaSign": (loyola_sign, True),
    "waterSail": (sailboat, True),
    # moving day
    "frontDoorL": (lambda: front_door()[0], True),
    "frontDoorR": (lambda: front_door()[1], True),
    **{f"car{name}{half}": (lambda colors=colors, i=i: car(*colors)[i], True)
       for name, colors in (("Red", "Rr"), ("Blue", "Cc"), ("White", "Ii"), ("Green", "Vv"))
       for i, half in enumerate("NS")},
    "cone": (cone, True),
    # rooftop
    "skyline2": (lambda: skyline(((0, 5, 4), (6, 8, 9), (9, 13, 2), (14, 15, 7)), ((1, 1), (15, 2)), 1, (11, 0)), True),
    "skyline3": (lambda: skyline(((0, 2, 8), (3, 6, 5), (7, 11, 7), (12, 15, 3)), ((5, 1), (9, 3)), 2), True),
    "skyline4": (lambda: skyline(((0, 4, 3), (5, 9, 6), (10, 12, 4), (13, 15, 9)), ((7, 1), (14, 4)), 3, (2, 0)), True),
    "nightSky": (lambda: night_sky(((3, 4, "L"), (11, 9, "L"), (7, 13, "9"), (14, 2, "3"))), True),
    "nightSky2": (lambda: night_sky(((5, 10, "L"), (12, 3, "9"), (1, 1, "9"))), True),
    "nightSky3": (lambda: night_sky(((9, 6, "L"), (2, 13, "3"), (13, 12, "9"))), True),
    "moon": (moon, True),
    "cityLights": (city_lights, True),
    "decoTrimN": (deco_trim, False),
    "barL": (lambda: bar("L"), True),
    "barM": (lambda: bar("M"), True),
    "barR": (lambda: bar("R"), True),
    "bistroTable": (bistro_table, True),
    "heater": (heater, True),
    "heaterTop": (lambda: heater(top=True), False),
}

# Drawn above Hannah, so she walks under them.
OVERHEAD = {"lantern", "lanterns", "bulbs"}

# Alternate looks for a tile, picked per cell from its position: name -> [(look, weight)].
VARIANTS = {
    "grass": [("grass", 16), ("grassTuft", 3), ("grassFlowers", 1)],
    "tree": [("tree", 1), ("tree2", 1)],
    "water": [("water", 6), ("waterSparkle", 1)],
    "brickWindow": [("brickWindow", 3), ("brickWindowAC", 1), ("brickWindowPlant", 1)],
    "restaurantM": [("restaurantM", 1), ("restaurantM2", 1)],
    "car": [("carRed", 3), ("carBlue", 3), ("carWhite", 3), ("carGreen", 1)],
    "skyline": [("skyline", 1), ("skyline2", 1), ("skyline3", 1), ("skyline4", 1)],
    "nightSky": [("nightSky", 1), ("nightSky2", 1), ("nightSky3", 1)],
}


def js(value):
    return repr(value).replace("'", '"')


if __name__ == "__main__":
    names = list(TILES)
    frames = [check(TILES[n][0]().rows(), 16, 16, PALETTE, n) for n in names]
    for group in (OVERHEAD, *[[look for look, _ in looks] for looks in VARIANTS.values()]):
        for n in group:
            assert n in TILES or f"{n}N" in TILES and f"{n}S" in TILES, f"{n} is not a tile"
    write_png(os.path.join(root(), "public/sprites/tiles.png"), render(frames, PALETTE, 16, 16))
    # Preview wraps every 11 tiles so it stays readable.
    bg = (120, 110, 120, 255)
    chunks = [frames[i:i + 11] for i in range(0, len(frames), 11)]
    chunks[-1] += [["." * 16] * 16] * (11 - len(chunks[-1]))
    preview = [row for c in chunks for row in render(c, PALETTE, 16, 16, scale=6, gap=2, bg=bg)]
    write_png(os.path.join(root(), "tools/tiles_preview.png"), preview)
    solid = [n for n in names if TILES[n][1]]
    # Tiles with no see-through pixels don't need a floor painted under them.
    full = [n for n, rows in zip(names, frames) if "." not in "".join(rows)]
    variants = {name: [[look, weight] for look, weight in looks] for name, looks in VARIANTS.items()}
    with open(os.path.join(root(), "src/tileset.js"), "w") as f:
        f.write("// Generated by tools/tiles.py. Do not edit by hand.\n")
        f.write(f"export const TILE_NAMES = {js(names)};\n")
        f.write(f"export const SOLID = new Set({js(solid)});\n")
        f.write(f"export const FULL = new Set({js(full)});\n")
        f.write(f"export const OVERHEAD = new Set({js(sorted(OVERHEAD))});\n")
        f.write(f"export const VARIANTS = {js(variants)};\n")
    print(f"Wrote {len(names)} tiles")
