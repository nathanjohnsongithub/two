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
    "~": "#f08a5d", ";": "#f7b89a",  # salmon
    "#": "#23302a",  # nori
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


def dumpster(piece=None):
    """A green dumpster with black lids. Two side by side join into one (L, R)."""
    t = Tile().rect(0, 2, 15, 13, "o").rect(0, 3, 15, 5, "B").rect(0, 4, 15, 4, "|")
    t.rect(0, 6, 15, 6, "o").rect(0, 7, 15, 12, "p").rect(0, 12, 15, 12, "P")
    t.where(lambda x, y: 7 <= y <= 11 and x % 5 == 2, "P")
    t.rect(0, 14, 15, 14, ".").px(3, 14, "|").px(3, 15, "o").px(12, 14, "|").px(12, 15, "o")
    if piece in (None, "L"):
        t.rect(0, 2, 0, 13, "o")
    if piece in (None, "R"):
        t.rect(15, 2, 15, 13, "o")
    if piece == "L":
        t.px(12, 14, ".").px(12, 15, ".")
    if piece == "R":
        t.px(3, 14, ".").px(3, 15, ".")
    return t


def box():
    t = Tile().box(2, 4, 13, 13, "j").rect(3, 8, 12, 8, "J").rect(7, 5, 8, 12, "y")
    return t.rect(3, 12, 12, 12, "J")


def mini_box():
    """A box as it looks stacked in the back of the U-Haul, in the top left corner
    (the game places it)."""
    return Tile().box(0, 0, 7, 6, "j").rect(1, 5, 6, 5, "J").rect(3, 1, 4, 4, "y")


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


# ---------- the alley (chapter 4) ----------

def alley(extra=None):
    """Worn concrete, poured in slabs. Variants: a crack, an asphalt patch,
    weeds in a crack, a puddle."""
    t = Tile().fill("s").where(lambda x, y: (x * 5 + y * 11) % 17 == 0, "x").rect(15, 0, 15, 15, "x")
    if extra == "crack":
        t.art([
            "xx..........",
            "..xo........",
            "....ox......",
            "......oxx...",
            "........xo..",
            "......x...ox",
            ".....x......",
        ], 2, 5)
    if extra == "patch":
        t.rect(3, 5, 11, 11, "D").rect(4, 4, 10, 12, "D").where(lambda x, y: 4 <= x <= 10 and 5 <= y <= 11 and (x + y) % 5 == 0, "d")
    if extra == "weeds":
        t.art(["x.o.x", ".oxo.", "..o.."], 4, 10).art(["v.h.v", ".vVv.", "..V.."], 4, 7)
    if extra == "puddle":
        t.rect(4, 7, 12, 10, "c").rect(3, 8, 13, 9, "c").rect(5, 8, 11, 9, "C").px(6, 8, "q").px(7, 8, "q")
    return t


def alley_drain(grate=False):
    """The shallow gutter down the middle of the alley (and now and then a drain grate)."""
    t = alley().rect(0, 7, 15, 8, "x").rect(0, 9, 15, 9, "S")
    if grate:
        t.box(4, 5, 11, 10, "B").where(lambda x, y: 5 <= y <= 9 and 5 <= x <= 10 and x % 2 == 0, "|")
    return t


def shingles(half):
    """Asphalt shingle garage roof. N is the top row (or a single row); S ends in a gutter."""
    t = Tile().fill("D").where(lambda x, y: y % 4 == 3, "d")
    t.where(lambda x, y: y % 4 != 3 and (x + (3 if (y // 4) % 2 else 0)) % 6 == 5, "d")
    if half == "N":
        return t.rect(0, 0, 15, 0, "o")
    return t.rect(0, 13, 15, 13, "o").rect(0, 14, 15, 14, "I").rect(0, 15, 15, 15, "i")


def garage(piece):
    """A garage facing the alley: vinyl siding and a roll-up door. A row joins
    up: L and R are siding and the door frame, M is door (M2 has a tag on it)."""
    t = Tile().fill("y").where(lambda x, y: y % 3 == 2, "j").rect(0, 0, 15, 1, "L").rect(0, 1, 15, 1, "l")
    x0, x1 = {"L": (6, 15), "R": (0, 9)}.get(piece, (0, 15))
    t.rect(x0, 3, x1, 15, "I").where(lambda x, y: x0 <= x <= x1 and y >= 3 and y % 3 == 0, "i")
    t.rect(x0, 3, x1, 3, "o")
    if piece == "L":
        t.rect(5, 3, 5, 15, "o").art([".o.", "oYo", ".o."], 1, 3)
    if piece == "R":
        t.rect(10, 3, 10, 15, "o")
    if piece == "M2":
        t.art([
            "!!.//.YY",
            "!..//.Y.",
            "!!./.YYY",
            "..//...Y",
            "!!/..YY.",
        ], 4, 6)
    return t.rect(0, 15, 15, 15, "x")


def fence(gate=False):
    """A wooden privacy fence (or its gate, with a Z brace and a latch)."""
    t = Tile().rect(0, 1, 15, 15, "F").where(lambda x, y: x % 4 == 3, "f")
    for x in range(0, 16, 4):
        t.px(x, 0, "o").px(x + 1, 0, "o").px(x + 2, 0, "o").px(x, 1, "o").px(x + 2, 1, "o")
        t.px(x, 0, ".").px(x + 2, 0, ".")
    t.rect(0, 4, 15, 4, "f").rect(0, 12, 15, 12, "f").rect(0, 15, 15, 15, "o")
    if gate:
        t.rect(0, 1, 0, 15, "o").rect(15, 1, 15, 15, "o")
        t.where(lambda x, y: 5 <= y <= 11 and abs(x - (y - 5) * 2 - 1) <= 1, "f")
        t.rect(12, 7, 13, 8, "Z").rect(1, 5, 2, 5, "|").rect(1, 11, 2, 11, "|")
    return t


def chain_link():
    """Chain-link fence: posts, a top rail and see-through mesh."""
    t = Tile().where(lambda x, y: y >= 2 and ((x + y) % 4 == 0 or (x - y) % 4 == 0), "z")
    return t.rect(0, 1, 15, 1, "Z").rect(0, 0, 0, 15, "Z").rect(1, 0, 1, 15, "z").rect(0, 15, 15, 15, "z")


def porch(piece):
    """A Chicago back porch: wooden decks stacked up the back of the building,
    one level per row. L and R have the corner posts; M shows a window behind."""
    t = brick_window() if piece == "M" else brick()
    t.rect(0, 0, 15, 1, "T").rect(0, 2, 15, 2, "t").rect(0, 3, 15, 3, "o")
    t.rect(0, 9, 15, 9, "T").rect(0, 10, 15, 10, "o")
    t.where(lambda x, y: 11 <= y <= 15 and x % 3 == 1, "T").where(lambda x, y: 11 <= y <= 15 and x % 3 == 2, "t")
    if piece == "L":
        t.rect(1, 0, 3, 15, "T").rect(3, 0, 3, 15, "t").rect(0, 0, 0, 15, "o").rect(4, 3, 4, 15, "o")
    if piece == "R":
        t.rect(12, 0, 14, 15, "T").rect(14, 0, 14, 15, "t").rect(15, 0, 15, 15, "o").rect(11, 3, 11, 15, "o")
    return t


def porch_stairs():
    """The porch stairs, coming down to the yard, with the shade underneath."""
    t = brick().rect(0, 0, 15, 1, "T").rect(0, 2, 15, 2, "t").rect(0, 3, 15, 3, "o")
    for i in range(6):
        x0, x1, y = round(i * 16 / 6), round((i + 1) * 16 / 6) - 1, 4 + 2 * i
        t.rect(x0, y, x1, y, "F").rect(x0, y + 1, x1, y + 1, "f").rect(x0, y + 2, x1, 15, "B")
        t.px(x0, y, "o")
    for x in range(16):
        y = round(x * 0.7)
        if y >= 4:
            t.px(x, y, "T").px(x, y + 1, "o")
    return t


def brick_tan(window=False, extra=None):
    """Tan brick (plain, or with a window), for a building that isn't red."""
    return recolor(brick_window(extra) if window else brick(), {"M": "j", "m": "J"})


def brick_green(window=False, extra=None):
    """Brick painted jade green, like a lot of the older Chinatown buildings."""
    return recolor(brick_window(extra) if window else brick(), {"M": "(", "m": "%"})


def downspout():
    """A metal downspout running down a brick wall."""
    t = brick().rect(10, 0, 12, 15, "o").rect(11, 0, 11, 15, "Z").px(12, 0, "z")
    for y in (3, 11):
        t.rect(9, y, 13, y, "o")
    return t


def meters():
    """Electric meters on the back wall, one per unit, with conduit running up."""
    t = brick().rect(7, 0, 8, 3, "z").rect(7, 0, 7, 3, "Z")
    for x0 in (2, 6, 10):
        t.box(x0, 4, x0 + 3, 10, "Z").circle(x0 + 1.5, 6.5, 1.2, "g").px(x0 + 1, 9, "z").px(x0 + 2, 9, "z")
    return t.rect(1, 11, 14, 11, "z").rect(2, 12, 13, 12, "o")


def glass_block():
    """A glass-block window, the kind every Chicago basement and bathroom has."""
    t = brick().box(3, 5, 12, 13, "g", edge="i")
    t.where(lambda x, y: 4 <= x <= 11 and 6 <= y <= 12 and (x % 3 == 0 or y % 3 == 0), "i")
    return t.where(lambda x, y: 4 <= x <= 11 and 6 <= y <= 12 and (x + y) % 5 == 0 and x % 3 and y % 3, "G").rect(3, 14, 12, 14, "1")


def dryer_vent():
    """A dryer vent: a little metal hood with louvers."""
    t = brick().box(5, 6, 10, 11, "Z").rect(6, 8, 9, 8, "z").rect(6, 10, 9, 10, "z")
    return t.rect(5, 12, 10, 12, "m")


def gangway():
    """The narrow, shady gap between two buildings."""
    return Tile().fill("|").rect(9, 0, 15, 15, "B").where(lambda x, y: x >= 9 and (x * 3 + y * 5) % 11 == 0, "d")


def grill():
    """A kettle grill in the yard."""
    return Tile().art([
        "................",
        "................",
        "................",
        "................",
        "......oZZo......",
        "....oo||||oo....",
        "...o|BBBBBB|o...",
        "..o|BBzBBBBB|o..",
        "..o|BBBBBBBB|o..",
        "..oooooooooooo..",
        "..o|BBBBBBBB|o..",
        "...o|BBBBBB|o...",
        "....oo||||oo....",
        ".....o.oo.o.....",
        "....o..oo..o....",
        "...o...oo...o...",
    ])


def back_door():
    """A steel back door with a little light over it."""
    t = brick().rect(4, 3, 11, 15, "o").rect(5, 4, 10, 15, "z").rect(5, 4, 10, 4, "Z")
    return t.rect(6, 6, 9, 8, "G").px(6, 6, "g").px(9, 10, "Y").rect(6, 1, 9, 2, "3").rect(6, 0, 9, 0, "o")


def cart(body, shade, lid):
    """A city garbage cart: lid, hinge handle, wheels."""
    t = Tile().art([
        "................",
        "................",
        "...oooooooooo...",
        "..oLLLLLLLLLLo..",
        "..oooooooooooo..",
        "...oBBBBBBBBo...",
        "...oBBBBBBBSo...",
        "...oBBBBBBBSo...",
        "...oBBIIIBBSo...",
        "...oBBBBBBBSo...",
        "....oBBBBBBSo...",
        "....oBBBBBBSo...",
        "....oBBBBBBSo...",
        "....oooooooo....",
        "...o|o....o|o...",
        "....o......o....",
    ])
    return recolor(t, {"B": body, "S": shade, "L": lid})


def utility_pole(top=False):
    """A wooden utility pole. Its top (crossarm, insulators and a transformer) goes in the tile above."""
    if top:
        return Tile().art([
            "................",
            "................",
            ".I............I.",
            "oIoooooooooooIIo",
            "ottttttttttttttto"[:16],
            "oooooooTtoooooo.",
            ".....ZZTtZ......",
            "....oZzTtzo.....",
            "....oZzTtzo.....",
            "....oZzTtzo.....",
            ".....ooTtoo.....",
            ".......Tt.......",
            ".......Tt.......",
            ".......Tt.......",
            ".......Tt.......",
            ".......Tt.......",
        ])
    return Tile().art([
        ".......Tt.......",
        ".......Tt.......",
        ".......Tt.......",
        ".......Tt.......",
        ".......Tt.......",
        "......oYYo......",
        ".......Tt.......",
        ".......Tt.......",
        ".......Tt.......",
        ".......Tt.......",
        ".......Tt.......",
        ".......Tt.......",
        "......oTto......",
        ".....ooTtoo.....",
        "....ooooooo.....",
        "................",
    ])


def wires():
    """Power lines strung between the poles, sagging a little."""
    t = Tile()
    for base in (3, 6):
        t.where(lambda x, y, base=base: y == base + round(1.2 * (1 - ((x - 7.5) / 7.5) ** 2)), "o")
    return t


def mattress(half):
    """An old mattress left leaning against the fence. Two tiles tall."""
    t = Tile(16, 32).box(3, 6, 12, 30, "L").where(lambda x, y: 4 <= x <= 11 and 7 <= y <= 29 and x % 3 == 0, "C")
    t.where(lambda x, y: 4 <= x <= 11 and 7 <= y <= 29 and (x * 2 + y) % 11 == 0, "l")
    t.rect(4, 7, 11, 7, "l").rect(3, 31, 12, 31, ".")
    t.rect(3, 30, 12, 30, "o").px(8, 20, "j").px(9, 20, "j").px(9, 21, "j")
    top, bottom = Tile(), Tile()
    top.g, bottom.g = t.g[:16], t.g[16:]
    return top if half == "N" else bottom


def trash_bags():
    return Tile().art([
        "................",
        "................",
        "................",
        "................",
        ".......o........",
        "......o|o.......",
        ".....oBBBo..o...",
        "....oBzBBBoo|o..",
        "...oBzBBBBBoBBo.",
        "...oBBBBBBBBzBBo",
        "..oooBBBBB|BBBBo",
        ".oBzBoBBB|BBBB|o",
        ".oBBBBoo||BBB||o",
        ".oBBBBBoooooooo.",
        "..ooooo.........",
        "................",
    ])


def cat():
    """A black cat who is supervising."""
    return Tile().art([
        "................",
        "................",
        "................",
        "................",
        "....o...o.......",
        "...o|o.o|o......",
        "...o||o||o......",
        "...o|Y|Y|o......",
        "...o||!||o......",
        "....o|||o.......",
        "....o|BB|o......",
        "...o|B||B|o.oo..",
        "...o|B||B|o.o|o.",
        "...o||||||oo|o..",
        "....o|ooo|ooo...",
        "................",
    ])


# ---------- Decker's Bagels (chapter 5, morning) ----------

# A tiny 3x5 font for signs.
LETTERS = {
    "D": ["##.", "#.#", "#.#", "#.#", "##."],
    "E": ["###", "#..", "##.", "#..", "###"],
    "C": [".##", "#..", "#..", "#..", ".##"],
    "K": ["#.#", "#.#", "##.", "#.#", "#.#"],
    "R": ["##.", "#.#", "##.", "#.#", "#.#"],
    "S": [".##", "#..", ".#.", "..#", "##."],
    "'": ["#", "#", ".", ".", "."],
}

BAGEL = [
    ".ooo.",
    "o@$@o",
    "o$.$o",
    "o@$@o",
    ".ooo.",
]


def write(t, x, y, text, ch):
    for letter in text:
        rows = LETTERS[letter]
        for dy, row in enumerate(rows):
            for dx, p in enumerate(row):
                if p == "#":
                    t.px(x + dx, y + dy, ch)
        x += len(rows[0]) + 1
    return t


def decker_sign():
    """The pop-up's signboard, three tiles wide: DECKER'S between two bagels."""
    t = Tile(48, 16)
    t.paste(brick()).paste(brick(), 16).paste(brick(), 32)
    t.rect(1, 3, 46, 13, "o").rect(2, 4, 45, 12, "B").rect(2, 4, 45, 4, "|")
    write(t, 9, 6, "DECKER'S", "I")
    t.art(BAGEL, 3, 6).art(BAGEL, 40, 6)
    return t.split()


def popup_window(piece):
    """The pop-up's service window, three tiles wide: glass on the sides (L, R)
    and the open window in the middle (M), with a steel ledge in front."""
    t = brick()
    if piece == "M":
        t.rect(0, 1, 15, 11, "o").rect(1, 2, 14, 10, "B").rect(1, 2, 14, 3, "3")
        t.rect(1, 6, 14, 6, "T").art(["@$.@$.@$"], 3, 5)
    else:
        t.rect(0, 1, 15, 11, "o").rect(1, 2, 14, 10, "G").px(3, 3, "g").px(4, 3, "g").px(3, 4, "g")
        t.art(BAGEL, 6 if piece == "L" else 5, 5)
    t.rect(0, 11, 15, 11, "o").rect(0, 12, 15, 12, "Z").rect(0, 13, 15, 13, "z").rect(0, 14, 15, 14, "o")
    if piece == "L":
        t.rect(0, 1, 0, 14, "o")
    if piece == "R":
        t.rect(15, 1, 15, 14, "o")
    return t


def pickup_table():
    """A little table by the window with a paper bag on it: HANNAH, and a heart."""
    return Tile().art([
        "................",
        ".....oooooo.....",
        "....ojjjjjjo....",
        "....oJJJJJJo....",
        "....ojjjjjjo....",
        "....ojRjjRjo....",
        "....ojRRRRjo....",
        "..ooojjRRjjooo..",
        ".oTTojjjjjjoTTo.",
        ".oTToooooooTTTo.",
        ".oTTTTTTTTTTTTo.",
        ".otttttttttttto.",
        ".oooooooooooooo.",
        "..o..........o..",
        "..o..........o..",
        "..o..........o..",
    ])


def bagel_menu():
    """A chalkboard sandwich board with bagels drawn on it."""
    t = menu_board().rect(4, 3, 11, 11, "B")
    t.art([".lll.", "l...l", "l.l.l", "l...l", ".lll."], 4, 3)
    return t.rect(10, 4, 11, 4, "l").rect(10, 6, 11, 6, "l").rect(4, 9, 11, 9, "l").rect(4, 11, 9, 11, "l")


def bike_rack():
    t = Tile()
    for x0 in (1, 6, 11):
        t.rect(x0, 5, x0, 13, "z").rect(x0 + 3, 5, x0 + 3, 13, "z").rect(x0, 4, x0 + 3, 4, "Z")
        t.px(x0, 4, "o").px(x0 + 3, 4, "o")
    return t.rect(0, 14, 15, 14, "o")


# ---------- Yokocho (chapter 5, dinner) ----------

def wood_dark():
    t = Tile().fill("u").where(lambda x, y: y % 4 == 3, "b")
    return t.where(lambda x, y: y % 4 != 3 and x == (y // 4 * 7 + 2) % 16, "b")


def slate():
    return Tile().fill("d").where(lambda x, y: x % 8 == 7 or y % 8 == 7, "|")


def slat_wall():
    """Dark wood slats, floor to ceiling."""
    return Tile().fill("b").where(lambda x, y: x % 3 == 0, "u").where(lambda x, y: x % 3 == 2, "|")


def box_sign(marks):
    """A lit box sign on the slats, the kind that flank the bar."""
    t = slat_wall().box(3, 1, 12, 14, "=", edge="o").rect(4, 2, 11, 2, "3")
    glyph(t, 5, 3, marks[0], "R")
    return glyph(t, 5, 9, marks[1], "B")


def sake_shelf():
    """Shelves of sake bottles against the back wall."""
    t = slat_wall()
    for shelf, bottles in ((7, ((1, "V"), (4, "I"), (7, "/"), (10, "@"), (13, "V"))),
                           (14, ((2, "@"), (5, "/"), (8, "I"), (11, "V")))):
        for x, ch in bottles:
            t.rect(x, shelf - 5, x + 1, shelf - 1, ch).rect(x, shelf - 5, x + 1, shelf - 5, "o")
        t.rect(0, shelf, 15, shelf, "T").rect(0, shelf + 1, 15, shelf + 1, "t") if shelf < 15 else None
    return t


def noren():
    """A doorway with a split indigo curtain."""
    t = Tile().fill("B").rect(0, 0, 15, 1, "T").rect(0, 0, 0, 15, "T").rect(15, 0, 15, 15, "T")
    t.rect(1, 2, 14, 9, "/").rect(7, 2, 8, 9, "B").rect(1, 9, 6, 9, "c").rect(9, 9, 14, 9, "c")
    return t.circle(4, 5, 1.6, "I").circle(11, 5, 1.6, "I")


def hinoki(piece, item=None):
    """The U-shaped counter in pale hinoki wood. "front" is the bottom of the U
    (its front faces the room), "L"/"R" are the arms, "BL"/"BR" the corners."""
    t = Tile()
    if piece in ("front", "BL", "BR"):
        t.rect(0, 0, 15, 8, "y").where(lambda x, y: y <= 8 and (x * 3 + y * 7) % 13 == 0, "e")
        t.rect(0, 9, 15, 9, "o").rect(0, 10, 15, 14, "u").where(lambda x, y: 10 <= y <= 14 and x % 4 == 3, "b")
        t.rect(0, 15, 15, 15, "o")
        if piece == "BL":
            t.rect(0, 0, 1, 15, ".").rect(2, 0, 2, 15, "o")
        if piece == "BR":
            t.rect(14, 0, 15, 15, ".").rect(13, 0, 13, 15, "o")
    else:
        x0, x1 = (2, 13)
        t.rect(x0, 0, x1, 15, "y").where(lambda x, y: x0 <= x <= x1 and (x * 3 + y * 7) % 13 == 0, "e")
        t.rect(x0 - 1, 0, x0 - 1, 15, "o").rect(x1 + 1, 0, x1 + 1, 15, "o")
        side = x0 - 2 if piece == "L" else x1 + 2
        t.rect(side, 0, side, 15, "u")
    if item == "handroll":
        t.art(["..oo.", ".oBVo", "oBIRo", "oBBo.", ".oo.."], 5, 2)
    if item == "sake":
        t.art(["oIo.oIo", "oio.oio", "ooo.ooo"], 4, 3).art([".oo.", "oIIo", "oIIo", ".oo."], 11, 1)
    if item == "case":
        t.box(1, 0, 14, 7, "g", edge="z").rect(2, 5, 13, 6, "I").art(["RRr.@@$.!!R"], 3, 4).px(3, 1, "I")
    if item == "nori":
        # A stack of nori sheets for the handrolls.
        t.art(["ooooooo", "o#####o", "o#7#7#o", "o77777o", "ooooooo"], 4 if piece != "front" else 3, 2)
    if item == "fish":
        # A little board with a slab of salmon on it.
        t.box(3, 2, 12, 8, "T").box(4, 3, 10, 6, "~").where(lambda x, y: 5 <= x <= 9 and 4 <= y <= 5 and (x + y) % 3 == 0, ";")
    if item == "empty":
        # His spot: an empty plate, his chopsticks laid across it, and his glass.
        t.art([".oooooo.", "oIIiiIIo", "oIIIIIIo", ".oooooo."], 2, 3).rect(3, 2, 9, 2, "T").rect(4, 1, 10, 1, "t")
        t.art(["oGo", "ogo", "ooo"], 12, 3)
    if item == "sando":
        t.rect(3, 6, 12, 7, "i").rect(2, 5, 13, 5, "I")
        t.art(["oLLLLLo", "oLL!!Lo", "o!!V!!o", "oLVVLLo", "oLLLLLo"], 4, 0)
    return t


def stool():
    return Tile().art([
        "................",
        "................",
        "................",
        "................",
        "....oooooooo....",
        "...oTTTTTTTTo...",
        "...otTTTTTTto...",
        "....oooooooo....",
        ".....oo..oo.....",
        ".....oo..oo.....",
        ".....oo..oo.....",
        "....oooooooo....",
        ".....oo..oo.....",
        ".....oo..oo.....",
        "................",
        "................",
    ])


def stool_jacket():
    """His jacket, left draped over the stool next to hers."""
    return stool().art([
        "...oooooooooo...",
        "..oCCCCCCCCCCo..",
        "..oCcCCCCCCcCo..",
        "..oCcCCCCCCcCo..",
        "..ooCCCCCCCCoo..",
        "..oCco.oo..oo...",
        "..oCCo..........",
        "..oCco..........",
        "..oCCo..........",
        "...oo...........",
    ], 0, 3)


def prep_island():
    """The chefs' steel prep table in the middle of the U, two by two: a cutting
    board with a slab of salmon and a knife, the rice tub with its paddle, a stack
    of nori and a bowl of pickled ginger."""
    t = Tile(32, 32)
    t.box(1, 3, 30, 22, "Z").rect(2, 20, 29, 21, "z")
    t.box(1, 22, 30, 26, "z").rect(2, 24, 29, 24, "o")
    for x in (2, 28):
        t.rect(x, 27, x + 1, 30, "o")
    t.rect(4, 27, 27, 27, "o")
    # Cutting board, salmon, knife.
    t.box(3, 5, 15, 15, "T").where(lambda x, y: 4 <= x <= 14 and 6 <= y <= 14 and (x * 2 + y) % 7 == 0, "t")
    t.box(5, 7, 11, 11, "~").where(lambda x, y: 6 <= x <= 10 and 8 <= y <= 10 and (x + y) % 3 == 0, ";")
    t.rect(5, 13, 11, 13, "i").rect(12, 13, 14, 13, "B")
    # Rice tub (hangiri) and paddle.
    t.circle(23, 10, 6, "o").circle(23, 10, 5, "T").circle(23, 10, 4, "I").px(21, 9, "i").px(24, 11, "i")
    t.rect(26, 5, 28, 6, "y").rect(28, 4, 29, 4, "y")
    # Nori and ginger.
    t.box(4, 16, 11, 19, "#").rect(5, 17, 10, 17, "7")
    t.circle(18, 18, 2, "o").circle(18, 18, 1, "!")
    return t


def island_pieces():
    island = prep_island()
    pieces = {}
    for r in range(2):
        for c in range(2):
            piece = Tile()
            piece.g = [row[c * 16:(c + 1) * 16] for row in island.g[r * 16:(r + 1) * 16]]
            pieces[f"prepIsland_{r}_{c}"] = piece
    return pieces


ISLAND = island_pieces()


def andon():
    """A standing lit sign on legs."""
    t = Tile().box(3, 1, 12, 12, "=", edge="o").rect(4, 2, 11, 2, "3")
    glyph(t, 5, 5, 3, "R")
    return t.rect(4, 13, 4, 15, "o").rect(11, 13, 11, 15, "o").rect(4, 13, 11, 13, "T")


def prep_counter():
    """The chefs' back counter: a wooden rice tub, a cutting board and a knife."""
    return Tile().art([
        "oooooooooooooooo",
        "oZZZZZZZZZZZZZZo",
        "oZ.oooo.ZZZZZZZo",
        "ZoTIIIIToTTTTTZo",
        "ZoTIIIITotttttZo",
        "Z.oTTTTo.ZzzzZZo",
        "ZZ.oooo.ZZZZZZZo",
        "oooooooooooooooo",
        "ozzzzzzzzzzzzzzo",
        "ozzzzzzozzzzzzzo",
        "ozzzzzzozzzzzzzo",
        "ozzzzzzozzzzzzzo",
        "ozzzzzzzzzzzzzzo",
        "oooooooooooooooo",
        "................",
        "................",
    ])


# ---------- the view from Chateau Carbide (chapter 5, drinks) ----------

VIEW_W, VIEW_H = 224, 64


def lit_windows(t, x0, x1, y0, y1, on, off, step=(2, 3), seed=0):
    """A grid of windows, some lit, picked from a hash so it's the same every time."""
    for y in range(y0, y1 + 1, step[1]):
        for x in range(x0, x1 + 1, step[0]):
            h = (x * 73856093 ^ y * 19349663 ^ seed * 83492791) & 0xFFFF
            t.px(x, y, on if h % 5 < 2 else off)


def skyline_view():
    """Looking out from the roof at night: stars, the moon, and (left to right)
    Willis Tower, Marina City's corncobs, Trump Tower, the Wrigley Building's
    lit clock tower, the Aon Center and the Hancock, with the rest of the city
    glowing in between. 14 tiles wide, 4 tall."""
    t = Tile(VIEW_W, VIEW_H).fill("8")
    t.where(lambda x, y: y >= 44 or (y >= 38 and (x + y) % 2 == 0), "9")
    t.where(lambda x, y: y < 36 and (x * 7 + y * 13) % 97 == 0, "L")
    t.where(lambda x, y: y < 30 and (x * 11 + y * 5) % 131 == 0, "3")
    t.circle(196, 9, 5, "L").circle(198, 8, 4.2, "8").px(191, 9, "i").px(192, 12, "i")

    # The city behind: low towers with scattered lights.
    x = 0
    for w, h in ((9, 18), (7, 26), (10, 14), (6, 22), (8, 30), (11, 17), (7, 24), (9, 20), (6, 28), (10, 16),
                 (8, 25), (7, 19), (9, 27), (6, 15), (10, 23), (8, 18), (7, 29), (9, 21), (6, 16), (11, 26),
                 (8, 20), (7, 24), (9, 17), (8, 22), (6, 19), (10, 25), (7, 18)):
        t.rect(x, VIEW_H - h, x + w - 1, VIEW_H - 1, "B")
        lit_windows(t, x + 1, x + w - 2, VIEW_H - h + 2, VIEW_H - 2, "3", "B", seed=x)
        x += w
        if x >= VIEW_W:
            break

    def tower(x0, x1, top, body, on, off, seed):
        t.rect(x0, top, x1, VIEW_H - 1, body)
        lit_windows(t, x0 + 1, x1 - 1, top + 2, VIEW_H - 2, on, off, seed=seed)

    # Willis Tower: black, stepped, with its two white antennas.
    tower(6, 25, 16, "|", "3", "B", 1)
    tower(9, 22, 10, "|", "3", "B", 2)
    tower(12, 19, 6, "|", "3", "B", 3)
    for ax in (13, 18):
        t.rect(ax, 0, ax, 5, "Z").px(ax, 0, "R")

    # Marina City: two round towers, balconies lit in rings.
    for x0 in (38, 49):
        t.rect(x0, 30, x0 + 8, VIEW_H - 1, "z").rect(x0 + 1, 29, x0 + 7, 29, "z")
        t.where(lambda x, y, x0=x0: x0 <= x <= x0 + 8 and y >= 31 and y % 3 == 0, "=")
        t.where(lambda x, y, x0=x0: x0 <= x <= x0 + 8 and y >= 31 and y % 3 == 1 and x in (x0, x0 + 8), "Z")
        t.px(x0, 29, "8").px(x0 + 8, 29, "8").rect(x0 + 2, 28, x0 + 6, 28, "Z")

    # Trump Tower: tall silver glass with setbacks and a spire.
    tower(66, 82, 20, "C", "=", "c", 4)
    tower(68, 80, 13, "C", "=", "c", 5)
    tower(71, 77, 8, "C", "=", "c", 6)
    t.rect(74, 0, 74, 7, "Z").px(74, 0, "R")
    t.where(lambda x, y: 66 <= x <= 82 and y >= 8 and x % 4 == 1 and t.g[y][x] == "C", "Z")

    # The Wrigley Building: bright white, clock tower and cupola.
    t.rect(94, 36, 116, VIEW_H - 1, "I")
    lit_windows(t, 95, 115, 38, VIEW_H - 2, "3", "i", seed=7)
    t.rect(101, 22, 109, 35, "I").rect(103, 17, 107, 21, "I").rect(104, 13, 106, 16, "i").px(105, 11, "Z").px(105, 12, "Z")
    t.circle(105, 27, 2.6, "L").px(105, 27, "o").px(105, 26, "o").px(106, 27, "o")
    t.where(lambda x, y: 101 <= x <= 109 and y in (31, 33), "i")

    # The Aon Center: a tall pale slab with vertical stripes.
    t.rect(134, 12, 146, VIEW_H - 1, "i").where(lambda x, y: 134 <= x <= 146 and y >= 12 and x % 3 == 1, "Z")
    lit_windows(t, 135, 145, 14, VIEW_H - 2, "=", "Z", step=(3, 2), seed=8)

    # The Hancock: dark, tapered, cross-braced, with two antennas.
    for y in range(8, VIEW_H):
        half = 5 + (y - 8) * 3 // (VIEW_H - 8)
        t.rect(170 - half, y, 170 + half, y, "|")
    t.where(lambda x, y: y >= 10 and abs(x - 170) <= 7 and t.g[y][x] == "|" and (x - 170 + y) % 12 == 0, "z")
    t.where(lambda x, y: y >= 10 and abs(x - 170) <= 7 and t.g[y][x] == "|" and (170 - x + y) % 12 == 0, "z")
    lit_windows(t, 166, 174, 12, VIEW_H - 2, "3", "|", step=(2, 4), seed=9)
    for ax in (168, 172):
        t.rect(ax, 0, ax, 7, "Z").px(ax, 0, "R")
    return t


def view_pieces():
    """The view cut into 16x16 tiles: name_row_col (see pictures in main.js)."""
    view = skyline_view()
    pieces = {}
    for r in range(VIEW_H // 16):
        for c in range(VIEW_W // 16):
            piece = Tile()
            piece.g = [row[c * 16:(c + 1) * 16] for row in view.g[r * 16:(r + 1) * 16]]
            pieces[f"view_{r}_{c}"] = piece
    return pieces


VIEW = view_pieces()


def dj_booth(piece):
    """The DJ's table, two tiles wide: a turntable on each side, the mixer in
    the middle, and a strip of light along the front."""
    t = Tile().rect(0, 2, 15, 15, "o").rect(0, 3, 15, 6, "z").rect(0, 7, 15, 7, "o")
    t.rect(0, 8, 15, 14, "|").rect(0, 11, 15, 11, "*").rect(0, 12, 15, 12, "!")
    if piece == "L":
        t.rect(0, 2, 0, 15, "o").circle(7, 4.5, 2.6, "B").circle(7, 4.5, 1.8, "|").px(7, 4, "R").rect(11, 3, 11, 5, "Z")
        t.rect(13, 3, 15, 6, "B").rect(14, 3, 14, 6, "z").px(14, 4, "I")
    else:
        t.rect(15, 2, 15, 15, "o").circle(8, 4.5, 2.6, "B").circle(8, 4.5, 1.8, "|").px(8, 4, "R").rect(4, 3, 4, 5, "Z")
        t.rect(0, 3, 2, 6, "B").rect(1, 3, 1, 6, "z").px(1, 5, "I")
    return t


def speaker():
    """A tall PA speaker: a small cone over a big one."""
    t = Tile().box(3, 1, 12, 14, "|").rect(3, 15, 12, 15, ".")
    t.circle(7.5, 4.5, 2.2, "o").circle(7.5, 4.5, 1.2, "B").px(7, 4, "z")
    return t.circle(7.5, 10, 3.2, "o").circle(7.5, 10, 2.2, "B").circle(7.5, 10, 1, "z")


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


# ---------- Andy's Jazz Club (the ending) ----------

def club_carpet():
    """Deep red carpet with a thin diamond lattice and gold dots."""
    t = Tile().fill("0").where(lambda x, y: (x + y) % 8 == 0 or (x - y) % 8 == 0, ")")
    return t.where(lambda x, y: x % 8 == 4 and y % 8 == 0, "$")


def curtain():
    """Red velvet stage curtain hanging in folds under a gold valance."""
    t = Tile().fill("R").where(lambda x, y: x % 4 == 0, "r").where(lambda x, y: x % 4 == 2 and y > 3, "!")
    t.rect(0, 0, 15, 2, "Y").rect(0, 3, 15, 3, "$")
    return t.where(lambda x, y: y == 4 and x % 4 == 1, "Y")


# A tiny neon alphabet for the club's sign (rows of 5, any width).
NEON = {
    "A": [".##.", "#..#", "####", "#..#", "#..#"],
    "N": ["#..#", "##.#", "#.##", "#..#", "#..#"],
    "D": ["###.", "#..#", "#..#", "#..#", "###."],
    "Y": ["#.#", "#.#", ".#.", ".#.", ".#."],
    "'": ["#", "#", ".", ".", "."],
    "S": [".###", "#...", ".##.", "...#", "###."],
    "J": ["###", "..#", "..#", "#.#", ".#."],
    "Z": ["####", "...#", ".##.", "#...", "####"],
}


def neon(t, word, y0, ch):
    """Write a word centered on a tile in neon letters."""
    width = sum(len(NEON[c][0]) for c in word) + len(word) - 1
    x = (t.w - width) // 2
    for c in word:
        for dy, row in enumerate(NEON[c]):
            for dx, p in enumerate(row):
                if p == "#":
                    t.px(x + dx, y0 + dy, ch)
        x += len(NEON[c][0]) + 1
    return t


def andys_sign():
    """The club's neon sign over the stage, two tiles wide (andysSign_0_0/_0_1)."""
    t = Tile(32, 16).fill("M").where(lambda x, y: y % 4 == 3, "m")
    t.box(1, 1, 30, 14, "|")
    neon(t, "ANDY'S", 3, "!")
    neon(t, "JAZZ", 9, "3")
    return {f"andysSign_0_{i}": part for i, part in enumerate(t.split())}


def jazz_photo(kind):
    """A framed black-and-white photo of a jazz great on the brick wall."""
    t = brick().box(3, 2, 12, 13, "L").rect(4, 3, 11, 12, "z")
    t.rect(4, 3, 11, 5, "i")
    # A silhouette: head, shoulders, and a horn.
    t.circle(7, 6.5, 1.6, "|").rect(5, 9, 9, 12, "|")
    if kind == "trumpet":
        t.rect(8, 7, 11, 7, "|").rect(10, 6, 11, 8, "|")
    else:
        t.rect(9, 8, 9, 11, "|").rect(9, 11, 11, 11, "|").rect(11, 10, 11, 11, "|")
    return t


def sconce():
    """A brass wall lamp with a warm shade."""
    t = brick().rect(7, 9, 8, 12, "$").rect(6, 12, 9, 13, "&")
    return t.rect(5, 4, 10, 8, "3").rect(6, 3, 9, 3, "3").rect(5, 8, 10, 8, "Y").rect(4, 5, 4, 8, "o").rect(11, 5, 11, 8, "o")


def back_bar():
    """Shelves of bottles behind the bar: whiskey, gin and vermouth."""
    return recolor(sake_shelf(), {"/": "$", "I": "@"})


def club_bar(piece):
    """The club's long bar: polished wood top with a brass edge, cocktails on top."""
    return recolor(bar(piece), {"7": "A", "6": "a"})


def piano(piece):
    """A black upright piano against the back of the stage, two tiles wide.
    Its keys face the pianist, who sits in front of it."""
    t = Tile(32, 16).rect(1, 0, 30, 13, "|").rect(0, 1, 31, 12, "|")
    t.rect(1, 0, 30, 0, "o").rect(0, 1, 0, 12, "o").rect(31, 1, 31, 12, "o")
    t.rect(2, 1, 29, 1, "z")
    # Sheet music on the stand.
    t.rect(10, 3, 21, 7, "L").rect(15, 3, 16, 7, "l")
    for y in (4, 6):
        t.rect(11, y, 14, y, "z").rect(17, y, 20, y, "z")
    # The keyboard.
    t.rect(1, 9, 30, 11, "I").where(lambda x, y: 9 <= y <= 11 and x % 2 == 0 and 1 <= x <= 30, "i")
    t.where(lambda x, y: 9 <= y <= 10 and x % 4 in (1, 2) and x % 28 not in (1, 2) and 1 <= x <= 30, "|")
    t.rect(0, 12, 31, 12, "o").rect(2, 13, 3, 15, "o").rect(28, 13, 29, 15, "o")
    parts = t.split()
    return parts[0] if piece == "L" else parts[1]


def drums():
    """A drum kit facing the room: cymbals, toms and a bass drum. It's drawn over
    the drummer (see OVERHEAD), who sits behind it."""
    t = Tile()
    # Cymbals on stands.
    t.rect(0, 3, 4, 4, "Y").rect(1, 2, 3, 2, "Y").rect(2, 5, 2, 12, "z")
    t.rect(11, 2, 15, 3, "Y").rect(12, 1, 14, 1, "Y").rect(13, 4, 13, 12, "z")
    # Toms.
    t.box(3, 6, 6, 9, "R").rect(4, 6, 5, 6, "I")
    t.box(9, 6, 12, 9, "R").rect(10, 6, 11, 6, "I")
    # The bass drum with the club's initial on the head.
    t.circle(7.5, 11.5, 4.4, "o").circle(7.5, 11.5, 3.6, "R").circle(7.5, 11.5, 2.8, "I")
    t.rect(7, 10, 7, 13, "r").rect(8, 12, 8, 13, "r").px(8, 10, "r").px(9, 11, "r")
    return t.rect(3, 15, 4, 15, "o").rect(11, 15, 12, 15, "o")


def jazz_table(reserved=False):
    """A little round table with a red candle glass (and a reserved card)."""
    t = Tile().art([
        "................",
        "................",
        "................",
        "................",
        "................",
        "...oooooooooo...",
        "..oTTTTTTTTTTo..",
        "..otttttttttto..",
        "...oooooooooo...",
        "......o||o......",
        "......o||o......",
        "......o||o......",
        ".....o||||o.....",
        "....oooooooo....",
        "................",
        "................",
    ])
    # Candle in a red glass.
    t.rect(7, 3, 8, 6, "R").rect(7, 3, 8, 3, "!").px(7, 2, "3").px(7, 1, "Y")
    if reserved:
        # A folded white card and a rose.
        t.rect(3, 3, 5, 6, "L").rect(3, 3, 5, 3, "l").px(4, 5, "o")
        return t.rect(11, 5, 12, 5, "R").px(11, 4, "R").px(12, 6, "v").px(13, 6, "v")
    # Two cocktails.
    t.art(["gggg", ".gg.", "..g."], 3, 3)
    return t.art(["o$o", "o$o", "ooo"], 11, 4)


def host_stand():
    """The host's lectern by the door, with the reservation book and a little lamp."""
    t = Tile().rect(3, 5, 12, 15, "o").rect(4, 6, 11, 14, "t").rect(4, 9, 11, 9, "T")
    t.rect(2, 4, 13, 5, "o").rect(3, 4, 12, 4, "T")
    t.rect(4, 2, 9, 4, "L").rect(6, 2, 7, 4, "l").px(5, 3, "z").px(8, 3, "z")
    return t.rect(11, 0, 12, 1, "3").rect(11, 2, 11, 3, "$")


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


def rug_blue():
    t = Tile().fill("C").where(lambda x, y: (x + y) % 8 == 4 or (x - y) % 8 == 4, "c")
    return t.where(lambda x, y: x % 8 == 0 and y % 8 == 0, "L")


def rug_cream():
    t = Tile().fill("y").where(lambda x, y: y % 8 in (3, 4), "j")
    return t.where(lambda x, y: y % 8 in (3, 4) and x % 4 == 1, "R")


def rug_runner():
    """A striped runner down the hall."""
    return Tile().fill("R").where(lambda x, y: y in (3, 12), "Y").where(lambda x, y: 6 <= y <= 9, "r")


def bath_tile():
    return Tile().fill("I").where(lambda x, y: (x // 4 + y // 4) % 2 == 0, "g").where(lambda x, y: x % 4 == 3 or y % 4 == 3, "i")


def wall_art(kind):
    """A wall face with something hanging on it: a lake painting or a clock."""
    t = wall_face()
    if kind == "lake":
        t.box(3, 4, 12, 10, "q", edge="T").rect(4, 8, 11, 9, "Q").px(10, 6, "Y").px(9, 6, "Y")
        return t.rect(4, 7, 11, 7, "V").px(5, 6, "V").px(6, 6, "V")
    return t.circle(7.5, 7, 3.6, "o").circle(7.5, 7, 2.8, "I").rect(7, 5, 7, 7, "o").rect(8, 7, 9, 7, "o")


def desk():
    """A desk with a monitor, keyboard, a mug and a lamp, against the wall."""
    return Tile().art([
        "................",
        "..oooooooo......",
        "..oBBBBBBo...o..",
        "..oBzBBBBo..oYo.",
        "..oBBBBBBo.oYYYo",
        "..oooooooo..ooo.",
        ".....oo......o..",
        "oooooooooooooooo",
        "oTTTTTTTTTTTTTTo",
        "oTLLLLLTTTTIiTTo",
        "otttttttttttttto",
        "oooooooooooooooo",
        "oTo..........oTo",
        "oTo..........oTo",
        "oto..........oto",
        "ooo..........ooo",
    ])


def desk_chair():
    """An office chair, pulled up to the desk (seen from behind)."""
    return Tile().art([
        "................",
        "................",
        ".....oooooo.....",
        "....oBBBBBBo....",
        "....oBBBBBBo....",
        "....oBBBBBBo....",
        "....oooooooo....",
        "...oBBBBBBBBo...",
        "...ozzzzzzzzo...",
        "....oooooooo....",
        ".......oo.......",
        ".......oo.......",
        "....oooooooo....",
        "...o|o.oo.o|o...",
        "................",
        "................",
    ])


def dresser():
    return Tile().art([
        "................",
        "..........oooo..",
        "...oVo....oCgo..",
        "..oVhVo...oggo..",
        "...oUo....oooo..",
        "oooooooooooooooo",
        "oTTTTTTTTTTTTTTo",
        "otttttttttttttto",
        "oTTTYTTTTTTYTTTo",
        "otttttttttttttto",
        "oTTTYTTTTTTYTTTo",
        "otttttttttttttto",
        "oTTTYTTTTTTYTTTo",
        "oooooooooooooooo",
        ".o............o.",
        "................",
    ])


def bookshelf():
    return Tile().art([
        "oooooooooooooooo",
        "oTTTTTTTTTTTTTTo",
        "oTRRCYIoRCCTYYTo",
        "oTRRCYIoRCCTYYTo",
        "oTRRCYIoRCCTYYTo",
        "otttttttttttttto",
        "oTVVoYYRRIICCTTo",
        "oTVVoYYRRIICCTTo",
        "oTVVoYYRRIICCTTo",
        "otttttttttttttto",
        "oTCCIIRRoYVVTTTo",
        "oTCCIIRRoYVVTTTo",
        "oTCCIIRRoYVVTTTo",
        "otttttttttttttto",
        "oooooooooooooooo",
        ".o............o.",
    ])


def floor_lamp():
    return Tile().art([
        ".....oooooo.....",
        "....o333333o....",
        "...o33333333o...",
        "...oooooooooo...",
        ".......oo.......",
        ".......oo.......",
        ".......oo.......",
        ".......oo.......",
        ".......oo.......",
        ".......oo.......",
        ".......oo.......",
        ".......oo.......",
        ".....oooooo.....",
        ".....oBBBBo.....",
        ".....oooooo.....",
        "................",
    ])


def coffee_table():
    """A low table with a magazine and a mug on it."""
    return Tile().art([
        "................",
        "................",
        "................",
        ".oooooooooooooo.",
        ".oTTTTTTTTTTTTo.",
        ".oTLLlTTTTIiTTo.",
        ".oTLlLTTTTIiTTo.",
        ".oTTTTTTTTTTTTo.",
        ".otttttttttttto.",
        ".oooooooooooooo.",
        ".oo..........oo.",
        "................",
        "................",
        "................",
        "................",
        "................",
    ])


def vanity():
    """A bathroom sink on a cabinet, soap on the side."""
    return Tile().art([
        "......oo........",
        ".....oZZo.......",
        "oooooooooooooooo",
        "oIIIIIIIIIIIIIIo",
        "oIIoooooooIIoYIo",
        "oIoiiiiiiiIoIIIo",
        "oIoiiiiiiiIoIIIo",
        "oIIoooooooIIIIIo",
        "oooooooooooooooo",
        "oTTTTTToTTTTTTTo",
        "oTTTTTzoTzTTTTTo",
        "oTTTTTToTTTTTTTo",
        "ottttttottttttto",
        "oooooooooooooooo",
        "................",
        "................",
    ])


def shower(half):
    """A glass shower stall, two tiles tall: showerhead on a tiled wall (N), glass door (S)."""
    t = Tile()
    if half == "N":
        t.fill("I").where(lambda x, y: (x + y) % 2 == 0, "i")
        t.rect(0, 0, 15, 0, "o").rect(0, 0, 0, 15, "z").rect(15, 0, 15, 15, "z")
        t.art(["ozzzo", ".oZZo", "oZZZZo"], 5, 2)
        for x, y in ((6, 6), (8, 7), (10, 6), (7, 9), (9, 10), (6, 11), (10, 12)):
            t.px(x, y, "Q")
        return t.rect(1, 13, 14, 13, "z").rect(1, 14, 14, 15, "G").px(3, 14, "g").px(4, 15, "g")
    t.rect(0, 0, 15, 15, "G").rect(0, 0, 0, 15, "z").rect(15, 0, 15, 15, "z")
    t.where(lambda x, y: 1 <= x <= 14 and y <= 11 and (x + y) % 9 == 0, "g")
    t.rect(12, 4, 12, 7, "Z")
    return t.rect(0, 12, 15, 12, "z").rect(0, 13, 15, 14, "Z").rect(0, 15, 15, 15, "o")


def trash_can():
    return Tile().art([
        "................",
        "................",
        "................",
        ".....oooooo.....",
        "....ozzzzzzo....",
        "....oooooooo....",
        "....oZZZZZZo....",
        "....oZzZZzZo....",
        "....oZzZZzZo....",
        "....oZzZZzZo....",
        "....oZzZZzZo....",
        "....oZZZZZZo....",
        ".....oooooo.....",
        "................",
        "................",
        "................",
    ])


def coat_rack():
    """A coat rack by the front door."""
    return Tile().art([
        ".......oo.......",
        "....oooTToooo...",
        "...oRRoTToCCo...",
        "..oRRRRoTCCCCo..",
        "..oRRrRoTCcCCo..",
        "..oRRrRoTCcCCo..",
        "..oRRrRoTCCCCo..",
        "..oRRRRoToCCo...",
        "...ooooTT.oo....",
        ".......TT.......",
        ".......TT.......",
        ".......TT.......",
        ".......TT.......",
        ".....oTTTTo.....",
        "....oooooooo....",
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


def recolor(t, swaps):
    """Swap palette letters, e.g. {"R": "Y"} turns red to gold."""
    t.g = [[swaps.get(ch, ch) for ch in row] for row in t.g]
    return t


def pavers():
    """Warm stone pavers laid in a running bond (the park plaza)."""
    t = Tile().fill("2").where(lambda x, y: y % 4 == 3, "x")
    return t.where(lambda x, y: (x + (4 if (y // 4) % 2 else 0)) % 8 == 7, "x")


def lanterns_gold():
    t = lanterns()
    return recolor(t, {"R": "Y", "r": "$", "!": "="}).art(["..oRRo..", "", "", "", "", "", "", "..oRRo..", "...RR...", "...R...."], 4, 4)


def pagoda(piece):
    """Green glazed tile roof with a gold ridge and red brackets under the eave.
    A row of them joins up, and the ends (L, R) curl up at the corners."""
    t = Tile().rect(0, 1, 15, 1, "o").rect(0, 2, 15, 2, "Y").rect(0, 3, 15, 3, "o")
    t.rect(0, 4, 15, 10, "+").where(lambda x, y: 4 <= y <= 10 and x % 4 == 0, "-")
    t.where(lambda x, y: y == 4 and x % 4 != 0, "(")
    t.rect(0, 11, 15, 11, "o").rect(0, 12, 15, 12, "R")
    t.where(lambda x, y: y == 13, "r").where(lambda x, y: y == 13 and x % 4 in (1, 2), "Y")
    t.rect(0, 14, 15, 14, "r").rect(0, 15, 15, 15, "o")
    if piece == "M":
        return t
    # The roof tapers in toward the top, and the eave tip swoops up past the ridge.
    for y in range(1, 11):
        edge = 3 if y <= 6 else 2 if y <= 8 else 1
        for x in range(edge):
            t.px(x, y, ".")
        t.px(edge, y, "o")
    for x in range(2):
        for y in range(13, 16):
            t.px(x, y, ".")
    t.px(2, 13, "o").px(2, 14, "o").px(2, 15, "o")
    t.art(["o...", "Yo..", "Yo..", "oYo.", ".oYo", "..oo"], 0, 6)
    t.art(["oo.", "YYo", "oo."], 0, 0)
    return t.mirror() if piece == "R" else t


def gate_beam(piece):
    """The gate's crossbeams, with a sign between the pillars (M) or the top of
    a pillar (L, R)."""
    t = Tile().rect(0, 0, 15, 1, "R").rect(0, 2, 15, 2, "r").rect(0, 3, 15, 3, "o")
    t.rect(0, 12, 15, 12, "o").rect(0, 13, 15, 13, "R").rect(0, 14, 15, 14, "r").rect(0, 15, 15, 15, "o")
    if piece in ("L", "R"):
        t.rect(0, 4, 15, 11, "o").rect(0, 5, 15, 10, "r")
        t.rect(4, 0, 11, 15, "o").rect(5, 0, 10, 15, "R").rect(9, 0, 10, 15, "r")
        t.rect(5, 6, 10, 7, "Y").rect(5, 8, 10, 8, "$")
        return t.mirror() if piece == "R" else t
    t.rect(0, 4, 15, 4, "$").rect(0, 11, 15, 11, "$").rect(0, 5, 15, 10, "-")
    return glyph(t, 5, 5, {"M": 2, "M2": 0, "M3": 4}[piece], "Y")


def gate_pillar():
    t = Tile().rect(4, 0, 11, 11, "o").rect(5, 0, 10, 11, "R").rect(9, 0, 10, 11, "r")
    t.rect(5, 2, 10, 3, "Y").rect(5, 4, 10, 4, "$").px(6, 0, "!").px(6, 1, "!")
    return t.box(3, 11, 12, 15, "1").rect(4, 14, 11, 14, "2")


def brick_sign(board, ink, marks):
    """A vertical sign mounted flat on a brick wall, two characters tall."""
    t = brick().box(4, 0, 11, 15, board).rect(12, 1, 12, 15, "m")
    glyph(t, 5, 2, marks[0], ink)
    return glyph(t, 5, 9, marks[1], ink)


def lion():
    """A stone guardian lion on its plinth, one paw on a ball (the other one mirrors it)."""
    return Tile().art([
        "....oooooo......",
        "...o212121o.....",
        "..o21111112o....",
        "..o2o1111o2o....",
        "..o21111112o....",
        "..o21oRRo12o....",
        "...o221122o.....",
        "..o2211112oo....",
        "..o21o11o122o...",
        ".oZZo1o1o1122o..",
        ".oZzo1o1o12222o.",
        "..oooooooooooo..",
        ".o111111111111o.",
        ".o222222222222o.",
        ".oooooooooooooo.",
        "................",
    ])


def phone_booth(top=False):
    """Mott Street's pagoda-topped phone booth; the roof goes in the tile above."""
    if top:
        return Tile().art([
            ".......YY.......",
            "......oYYo......",
            ".o...o++++o...o.",
            ".oYoo((((((ooYo.",
            "..o++++++++++o..",
            "..oooooooooooo..",
            "...oRRRRRRRRo...",
            "...orrrrrrrro...",
        ], 0, 8)
    return Tile().art([
        "...oYYYYYYYYo...",
        "...oRooooooRo...",
        "...oRoGGggoRo...",
        "...oRoGoogoRo...",
        "...oRoGoBGoRo...",
        "...oRoGGzGoRo...",
        "...oRoGgGGoRo...",
        "...oRoGGGgoRo...",
        "...oRooooooRo...",
        "...oRRRRRRRRo...",
        "...orYrrrrYro...",
        "...oRRRRRRRRo...",
        "...orrrrrrrro...",
        "...oooooooooo...",
        "................",
        "................",
    ])


def street_cart():
    """A steamed bun cart under a red and gold umbrella."""
    return Tile().art([
        "......oooo......",
        "....ooRYYRoo....",
        "..ooRRRYYRRRoo..",
        ".oRRRRYYYYRRRRo.",
        "oRRRRRYYYYRRRRRo",
        "oooooooooooooooo",
        ".......oo.......",
        "...oooooooooo...",
        "...oJJJJJJJJo...",
        "...ojjjjjjjjo...",
        ".ooooooooooooo..",
        ".oZZZZZZZZZZZo..",
        ".ozzzzYYYzzzzo..",
        ".ooooooooooooo..",
        "..o|o.....o|o...",
        "...o.......o....",
    ])


def fish_stand():
    """Whole fish and crabs laid out on ice."""
    return Tile().art([
        "................",
        "................",
        "................",
        "................",
        ".IiIIiIIiIIiIIi.",
        ".IzZZoIiIRRroIi.",
        ".IiIIiIzZZoIiII.",
        ".IRRroIiIIizZZo.",
        "oJjjJjJjjJjJjjJo",
        "ojjjjjjjjjjjjjjo",
        "oooooooooooooooo",
        "oZZZZZZZZZZZZZZo",
        "ozzzzzzzzzzzzzzo",
        "oooooooooooooooo",
        ".o.o........o.o.",
        ".o.o........o.o.",
    ])


def shop_tea():
    return shop("*", "I", (1, 4), [
        "zzzzzzzzzzzzzz",
        "IoIIoIIoIIoIIo",
        "yyoJJo**oVVoyy",
        "yyoJJo**oVVoyy",
        "BBoBBoBBoBBoBB",
    ])


def shop_herbs():
    return shop("T", "Y", (0, 3), [
        "TtTtTtTtTtTtTt",
        "tYtYtYtYtYtYtY",
        "TTTTTTTTTTTTTT",
        "oIoo@o&IooIo@o",
        "TTTTTTTTTTTTTT",
    ])


def chess_table():
    """A stone xiangqi table with a game going and four stools (Columbus Park)."""
    return Tile().art([
        "................",
        "................",
        "..oooooooooooo..",
        ".oZZZZZZZZZZZZo.",
        ".oZIIzZzZzZRRZo.",
        ".oZzZzZzZzZzZZo.",
        ".ozzzzzzzzzzzzo.",
        ".oZRRzZIIzZzZZo.",
        ".oZzZzZzZRRzIIo.",
        ".oZZZZZZZZZZZZo.",
        "..ozzzzzzzzzzo..",
        ".oooooZZzooooo..",
        "oZZo.oZZzo.oZZo.",
        "ozzo.ooooo.ozzo.",
        ".oo.........oo..",
        "................",
    ])


def lamppost_red():
    return recolor(lamppost(), {"|": "r", "B": "R"})


def lamppost_red_top():
    return recolor(lamppost_top(), {"|": "r", "B": "+", "g": "=", "G": "3", "I": "="})


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
    "dumpsterL": (lambda: dumpster("L"), True),
    "dumpsterR": (lambda: dumpster("R"), True),
    "box": (box, False),
    "miniBox": (mini_box, False),
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
    "rugBlue": (rug_blue, False),
    "rugCream": (rug_cream, False),
    "rugRunner": (rug_runner, False),
    **{f"rugEdge{s}": (lambda s=s: edge(s, "l"), False) for s in "NSEW"},
    "bathTile": (bath_tile, False),
    "wallFaceArt": (lambda: wall_art("lake"), True),
    "wallFaceClock": (lambda: wall_art("clock"), True),
    "desk": (desk, True),
    "deskChair": (desk_chair, False),
    "dresser": (dresser, True),
    "bookshelf": (bookshelf, True),
    "floorLamp": (floor_lamp, True),
    "coffeeTable": (coffee_table, True),
    "vanity": (vanity, True),
    "showerN": (lambda: shower("N"), True),
    "showerS": (lambda: shower("S"), True),
    "trashCan": (trash_can, True),
    "coatRack": (coat_rack, True),
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
    "lanternsGold": (lanterns_gold, False),
    "pavers": (pavers, False),
    **{f"pagoda{p}": (lambda p=p: pagoda(p), True) for p in "LMR"},
    **{f"gateRoof{p}": (lambda p=p: pagoda(p), False) for p in "LMR"},
    **{f"gateBeam{p}": (lambda p=p: gate_beam(p), False) for p in ("L", "M", "M2", "M3", "R")},
    "gatePillar": (gate_pillar, True),
    "brickSign": (lambda: brick_sign("R", "Y", (2, 5)), True),
    "brickSign2": (lambda: brick_sign("Y", "R", (3, 1)), True),
    "brickSign3": (lambda: brick_sign("+", "Y", (4, 0)), True),
    "brickSign4": (lambda: brick_sign("!", "I", (5, 2)), True),
    "lionL": (lion, True),
    "lionR": (lambda: lion().mirror(), True),
    "phoneBooth": (phone_booth, True),
    "phoneBoothTop": (lambda: phone_booth(top=True), False),
    "streetCart": (street_cart, True),
    "fishStand": (fish_stand, True),
    "shopTea": (shop_tea, True),
    "shopHerbs": (shop_herbs, True),
    "chessTable": (chess_table, True),
    "lamppostRed": (lamppost_red, True),
    "lamppostRedTop": (lamppost_red_top, False),
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
    "alley": (alley, False),
    **{f"alley{k.title()}": (lambda k=k: alley(k), False) for k in ("crack", "patch", "weeds", "puddle")},
    "alleyDrain": (alley_drain, False),
    "alleyGrate": (lambda: alley_drain(grate=True), False),
    "shinglesN": (lambda: shingles("N"), True),
    "shinglesS": (lambda: shingles("S"), True),
    **{f"garage{p}": (lambda p=p: garage(p), True) for p in ("L", "M", "M2", "R")},
    "fence": (fence, True),
    "fenceGate": (lambda: fence(gate=True), True),
    "chainLink": (chain_link, True),
    **{f"porch{p}": (lambda p=p: porch(p), True) for p in "LMR"},
    "porchStairs": (porch_stairs, True),
    "backDoor": (back_door, True),
    # Decker's Bagels
    **{f"deckerSign{p}": (lambda i=i: decker_sign()[i], True) for i, p in enumerate("LMR")},
    **{f"popupWindow{p}": (lambda p=p: popup_window(p), True) for p in "LMR"},
    "pickupTable": (pickup_table, True),
    "bagelMenu": (bagel_menu, True),
    "bikeRack": (bike_rack, True),
    # Yokocho
    "woodDark": (wood_dark, False),
    "slate": (slate, False),
    "slatWall": (slat_wall, True),
    "boxSign": (lambda: box_sign((3, 1)), True),
    "boxSign2": (lambda: box_sign((5, 2)), True),
    "boxSign3": (lambda: box_sign((0, 4)), True),
    "sakeShelf": (sake_shelf, True),
    "noren": (noren, True),
    "hinokiFront": (lambda: hinoki("front"), True),
    "hinokiFrontRoll": (lambda: hinoki("front", "handroll"), True),
    "hinokiFrontSake": (lambda: hinoki("front", "sake"), True),
    "hinokiFrontCase": (lambda: hinoki("front", "case"), True),
    "hinokiSando": (lambda: hinoki("front", "sando"), True),
    "hinokiEmpty": (lambda: hinoki("front", "empty"), True),
    "hinokiLNori": (lambda: hinoki("L", "nori"), True),
    "hinokiRFish": (lambda: hinoki("R", "fish"), True),
    "hinokiLFish": (lambda: hinoki("L", "fish"), True),
    "hinokiRNori": (lambda: hinoki("R", "nori"), True),
    "hinokiL": (lambda: hinoki("L"), True),
    "hinokiLRoll": (lambda: hinoki("L", "handroll"), True),
    "hinokiR": (lambda: hinoki("R"), True),
    "hinokiRSake": (lambda: hinoki("R", "sake"), True),
    "hinokiBL": (lambda: hinoki("BL"), True),
    "hinokiBR": (lambda: hinoki("BR"), True),
    "stool": (stool, False),
    "andon": (andon, True),
    "prepCounter": (prep_counter, True),
    "stoolJacket": (stool_jacket, False),
    **{name: (lambda piece=piece: piece, True) for name, piece in ISLAND.items()},
    # the view from the rooftop, and the DJ
    **{name: (lambda piece=piece: piece, True) for name, piece in VIEW.items()},
    "djBoothL": (lambda: dj_booth("L"), True),
    "djBoothR": (lambda: dj_booth("R"), True),
    "speaker": (speaker, True),
    "brickTan": (brick_tan, True),
    "brickTanWindow": (lambda: brick_tan(window=True), True),
    "brickTanWindowAC": (lambda: brick_tan(window=True, extra="ac"), True),
    "brickGreen": (brick_green, True),
    "brickGreenWindow": (lambda: brick_green(window=True), True),
    "brickGreenWindowPlant": (lambda: brick_green(window=True, extra="plant"), True),
    "backDoorTan": (lambda: recolor(back_door(), {"M": "j", "m": "J"}), True),
    "downspout": (downspout, True),
    "meters": (meters, True),
    "glassBlock": (glass_block, True),
    "dryerVent": (dryer_vent, True),
    "gangway": (gangway, True),
    "grill": (grill, True),
    "cartBlue": (lambda: cart("/", "c", "/"), True),
    "cartBlack": (lambda: cart("B", "|", "B"), True),
    "pole": (utility_pole, True),
    "poleTop": (lambda: utility_pole(top=True), False),
    "wires": (wires, False),
    "mattressN": (lambda: mattress("N"), True),
    "mattressS": (lambda: mattress("S"), True),
    "trashBags": (trash_bags, True),
    "cat": (cat, True),
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
    # Andy's Jazz Club
    "clubCarpet": (club_carpet, False),
    "curtain": (curtain, True),
    **{name: (lambda piece=piece: piece, True) for name, piece in andys_sign().items()},
    "jazzPhoto": (lambda: jazz_photo("trumpet"), True),
    "jazzPhoto2": (lambda: jazz_photo("sax"), True),
    "sconce": (sconce, True),
    "backBar": (back_bar, True),
    "clubBarL": (lambda: club_bar("L"), True),
    "clubBarM": (lambda: club_bar("M"), True),
    "clubBarR": (lambda: club_bar("R"), True),
    "pianoL": (lambda: piano("L"), True),
    "pianoR": (lambda: piano("R"), True),
    "drums": (drums, True),
    "jazzTable": (jazz_table, True),
    "reservedTable": (lambda: jazz_table(reserved=True), True),
    "hostStand": (host_stand, True),
}

# Drawn above Hannah, so she walks under them.
OVERHEAD = {"lantern", "lanterns", "bulbs", "wires", "drums", "gateRoofL", "gateRoofM", "gateRoofR", "gateBeamL", "gateBeamM", "gateBeamR"}

# Alternate looks for a tile, picked per cell from its position: name -> [(look, weight)].
VARIANTS = {
    "grass": [("grass", 16), ("grassTuft", 3), ("grassFlowers", 1)],
    "tree": [("tree", 1), ("tree2", 1)],
    "water": [("water", 6), ("waterSparkle", 1)],
    "brickWindow": [("brickWindow", 3), ("brickWindowAC", 1), ("brickWindowPlant", 1)],
    "restaurantM": [("restaurantM", 1), ("restaurantM2", 1)],
    "lanterns": [("lanterns", 3), ("lanternsGold", 1)],
    "wallFace": [("wallFace", 14), ("wallFaceArt", 2), ("wallFaceClock", 1)],
    "alley": [("alley", 30), ("alleyCrack", 4), ("alleyPatch", 2), ("alleyWeeds", 3), ("alleyPuddle", 1)],
    "alleyDrain": [("alleyDrain", 9), ("alleyGrate", 1)],
    "garageM": [("garageM", 3), ("garageM2", 1)],
    "boxSign": [("boxSign", 1), ("boxSign2", 1), ("boxSign3", 1)],
    "hinokiFront": [("hinokiFront", 3), ("hinokiFrontRoll", 2), ("hinokiFrontSake", 1), ("hinokiFrontCase", 2)],
    "hinokiL": [("hinokiL", 2), ("hinokiLRoll", 1), ("hinokiLNori", 1), ("hinokiLFish", 1)],
    "hinokiR": [("hinokiR", 2), ("hinokiRSake", 1), ("hinokiRFish", 1), ("hinokiRNori", 1)],
    "gateBeamM": [("gateBeamM", 1), ("gateBeamM2", 1), ("gateBeamM3", 1)],
    "brickSign": [("brickSign", 1), ("brickSign2", 1), ("brickSign3", 1), ("brickSign4", 1)],
    "car": [("carRed", 3), ("carBlue", 3), ("carWhite", 3), ("carGreen", 1)],
    "skyline": [("skyline", 1), ("skyline2", 1), ("skyline3", 1), ("skyline4", 1)],
    "nightSky": [("nightSky", 1), ("nightSky2", 1), ("nightSky3", 1)],
    "jazzPhoto": [("jazzPhoto", 1), ("jazzPhoto2", 1)],
    "brickTanWindow": [("brickTanWindow", 3), ("brickTanWindowAC", 1)],
    "brickGreenWindow": [("brickGreenWindow", 3), ("brickGreenWindowPlant", 1)],
}


# Tiles per row in tiles.png.
COLS = 32


def js(value):
    return repr(value).replace("'", '"')


if __name__ == "__main__":
    names = list(TILES)
    frames = [check(TILES[n][0]().rows(), 16, 16, PALETTE, n) for n in names]
    for group in (OVERHEAD, *[[look for look, _ in looks] for looks in VARIANTS.values()]):
        for n in group:
            assert n in TILES or f"{n}N" in TILES and f"{n}S" in TILES, f"{n} is not a tile"
    # Laid out in rows of COLS: one very wide strip is too big a texture for some phones.
    empty = ["." * 16] * 16
    rows_of = [frames[i:i + COLS] for i in range(0, len(frames), COLS)]
    rows_of[-1] = rows_of[-1] + [empty] * (COLS - len(rows_of[-1]))
    write_png(os.path.join(root(), "public/sprites/tiles.png"), [px for part in rows_of for px in render(part, PALETTE, 16, 16)])
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
        f.write(f"export const TILE_COLS = {COLS};\n")
        f.write(f"export const SOLID = new Set({js(solid)});\n")
        f.write(f"export const FULL = new Set({js(full)});\n")
        f.write(f"export const OVERHEAD = new Set({js(sorted(OVERHEAD))});\n")
        f.write(f"export const VARIANTS = {js(variants)};\n")
    print(f"Wrote {len(names)} tiles")
