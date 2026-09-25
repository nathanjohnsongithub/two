"""Generates the 16x16 tileset: public/sprites/tiles.png + src/tileset.js

Tiles are drawn either from text grids (one character per pixel) or with a
few shape helpers. Run:  python3 tools/tiles.py
Also writes tools/tiles_preview.png (6x scale) to eyeball the result.
"""

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
}


class Tile:
    def __init__(self):
        self.g = [["."] * 16 for _ in range(16)]

    def px(self, x, y, ch):
        if 0 <= x < 16 and 0 <= y < 16:
            self.g[y][x] = ch
        return self

    def rect(self, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, ch)
        return self

    def fill(self, ch):
        return self.rect(0, 0, 15, 15, ch)

    def box(self, x0, y0, x1, y1, inner, edge="o"):
        self.rect(x0, y0, x1, y1, edge)
        return self.rect(x0 + 1, y0 + 1, x1 - 1, y1 - 1, inner)

    def circle(self, cx, cy, r, ch):
        for y in range(16):
            for x in range(16):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self.px(x, y, ch)
        return self

    def where(self, test, ch):
        for y in range(16):
            for x in range(16):
                if test(x, y):
                    self.px(x, y, ch)
        return self

    def art(self, rows):
        check(rows, 16, 16, PALETTE)
        for y, row in enumerate(rows):
            for x, ch in enumerate(row):
                if ch != ".":
                    self.g[y][x] = ch
        return self

    def transpose(self):
        """Flip across the diagonal: turns a sideways piece into an upright one."""
        self.g = [list(col) for col in zip(*self.g)]
        return self

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
    t = Tile().fill("H").where(lambda x, y: (x % 6 - 2) ** 2 + (y % 6 - 2) ** 2 <= 2, "h")
    return t.where(lambda x, y: y >= 14, "v")


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
    t = table().rect(2, 3, 13, 10, "L").rect(2, 10, 13, 10, "l")
    for x in (4, 11):
        t.px(x, 5, "Y").px(x, 6, "I").px(x, 7, "I").px(x, 8, "i")
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


def lantern():
    t = Tile().rect(7, 0, 8, 2, "o").rect(5, 3, 10, 10, "R").rect(5, 3, 10, 3, "Y").rect(5, 10, 10, 10, "Y")
    t.px(5, 3, ".").px(10, 3, ".").px(5, 10, ".").px(10, 10, ".")
    t.rect(4, 5, 4, 8, "R").rect(11, 5, 11, 8, "R").rect(7, 5, 8, 8, "r")
    return t.rect(7, 11, 8, 13, "Y")


def storefront():
    t = Tile().where(lambda x, y: y <= 5, "R").where(lambda x, y: y <= 5 and (x // 2) % 2 == 1, "L")
    t.rect(0, 6, 15, 6, "o").box(0, 7, 15, 12, "G").px(2, 8, "g").px(3, 8, "g").px(2, 9, "g")
    return t.rect(0, 13, 15, 15, "M").rect(0, 14, 15, 14, "m")


# ---------- Loyola (chapter 3) ----------

def stone():
    t = Tile().fill("1").where(lambda x, y: y % 8 == 7, "2")
    return t.where(lambda x, y: (x + (4 if (y // 8) % 2 else 0)) % 8 == 7, "2")


def stone_window():
    t = stone().rect(4, 3, 11, 13, "o").rect(5, 4, 10, 12, "G")
    t.px(4, 3, "1").px(11, 3, "1").px(5, 4, "o").px(10, 4, "o")
    return t.rect(7, 4, 7, 12, "o").rect(5, 8, 10, 8, "o").px(6, 6, "g").px(6, 7, "g")


def stone_door():
    t = stone().rect(3, 3, 12, 15, "o").rect(4, 4, 11, 15, "T").px(3, 3, "1").px(12, 3, "1")
    return t.rect(7, 4, 8, 15, "t").px(6, 10, "Y").px(9, 10, "Y")


def stage():
    return Tile().fill("u").where(lambda x, y: y % 4 == 3, "b").where(lambda x, y: y % 4 != 3 and x == (y // 4 * 7 + 2) % 16, "b")


def chair_cap():
    """His graduation cap left on a chair, tassel and all."""
    t = chair().rect(3, 6, 12, 7, "o").rect(4, 6, 11, 6, "B").rect(5, 8, 10, 9, "B").rect(5, 10, 10, 10, "o")
    return t.px(7, 6, "Y").rect(11, 7, 11, 10, "Y").px(12, 10, "Y")


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


def skyline():
    t = Tile().fill("8").px(2, 1, "L").px(12, 3, "L").px(7, 0, "L")
    for x0, x1, top in ((0, 3, 6), (4, 7, 3), (8, 10, 8), (11, 15, 5)):
        t.rect(x0, top, x1, 15, "9")
        t.where(lambda x, y, x0=x0, x1=x1, top=top: x0 < x < x1 and y > top and y % 3 == 0 and (x * 7 + y * 3) % 5 < 2, "3")
    return t


def bulbs():
    t = Tile().where(lambda x, y: y == 3 + ((x - 8) ** 2) // 40, "o")
    for x in (3, 11):
        y = 4 + ((x - 8) ** 2) // 40
        t.rect(x, y, x + 1, y + 1, "3").px(x, y + 2, "Y").px(x + 1, y + 2, "Y")
    return t


def deco_wall():
    return Tile().fill("6").where(lambda x, y: x % 8 in (1, 5), "7").where(lambda x, y: x % 8 == 3, "Y")


def elevator():
    t = deco_wall().box(2, 2, 13, 15, "$", edge="Y").rect(7, 3, 8, 15, "o")
    return t.rect(3, 3, 12, 4, "Y").px(5, 5, "Y").px(10, 5, "Y")


# ---------- items (not placed in maps) ----------

def note():
    t = Tile().box(1, 4, 14, 12, "L")
    t.where(lambda x, y: 5 <= y <= 8 and (x - 2 == y - 5 or 13 - x == y - 5), "l")
    return t.rect(6, 8, 9, 9, "R").px(7, 10, "R").px(8, 10, "R").px(6, 8, "R").px(9, 8, "R")


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
}


if __name__ == "__main__":
    names = list(TILES)
    frames = [check(TILES[n][0]().rows(), 16, 16, PALETTE, n) for n in names]
    write_png(os.path.join(root(), "public/sprites/tiles.png"), render(frames, PALETTE, 16, 16))
    # Preview wraps every 11 tiles so it stays readable.
    bg = (120, 110, 120, 255)
    chunks = [frames[i:i + 11] for i in range(0, len(frames), 11)]
    chunks[-1] += [["." * 16] * 16] * (11 - len(chunks[-1]))
    preview = [row for c in chunks for row in render(c, PALETTE, 16, 16, scale=6, gap=2, bg=bg)]
    write_png(os.path.join(root(), "tools/tiles_preview.png"), preview)
    solid = [n for n in names if TILES[n][1]]
    with open(os.path.join(root(), "src/tileset.js"), "w") as f:
        f.write("// Generated by tools/tiles.py. Do not edit by hand.\n")
        f.write(f"export const TILE_NAMES = {names!r};\n".replace("'", '"'))
        f.write(f"export const SOLID = new Set({solid!r});\n".replace("'", '"'))
    print(f"Wrote {len(names)} tiles")
