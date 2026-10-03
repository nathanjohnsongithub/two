"""Generates the people Hannah meets along the way: public/sprites/locals.png

One front-facing 16x24 frame each, in this order (the frame number in
content.js): 0 the auntie at the fruit stand and 1 the uncle at the xiangqi
tables (Chinatown), 2 the Decker's worker leaning out of the pop-up window
(just head and shoulders, so she fits in it), 3 and 4 two people in the bagel
line, 5 and 6 the chefs at Yokocho, then on the rooftop: 7-10 guests sitting
at tables facing right, 11-14 the same guests facing left, 15 the bartender,
16 the DJ, then at Andy's Jazz Club: 17 the pianist, 18 the drummer, 19 the
singer, 20 the sax player, 21 the host, 22 the bartender at Andy's. Then
more guests at tables: 23-37 facing right (guests 4-18 in GUESTS) and 38-52
the same ones facing left. Guest n faces right at frame n + 19 and left at
n + 34 (for n >= 4).
Run:  python3 tools/local_sprite.py
"""

import os

from pixel import check, render, root, write_png

PALETTE = {
    ".": None,
    "o": "#2b1d1a",  # outline
    "e": "#2b1d1a",  # eyes
    "m": "#a8604e",  # mouth
    "S": "#e9bd97",  # skin
    "H": "#1e1a18",  # black hair
    "h": "#b9b4ad",  # gray hair
    "R": "#c8323a", "r": "#8e1f26",  # red top
    "L": "#f1ece2", "l": "#d3cbbd",  # apron
    "B": "#33302e",  # dark pants
    "C": "#6b5a47", "c": "#54463a",  # flat cap
    "V": "#3d4f73", "v": "#2f3d5c",  # cardigan
    "I": "#f4f4f2",  # shirt
    "Y": "#e8b83e",  # buttons
    "T": "#b59b78", "t": "#937c5d",  # khakis
    "F": "#2b2626",  # shoes
    "K": "#2f6b4a", "k": "#24533a",  # green cap / apron
    "W": "#f4f4f2", "w": "#d6d6d2",  # chef whites
    "N": "#26324d",  # navy headband
    "G": "#5b7a3a", "g": "#46602c",  # olive jacket
    "D": "#8a4a5c", "d": "#6e3a4a",  # plum hoodie
    "Q": "#6a4a3a", "q": "#d8cdb6",  # coffee cup / sleeve
    "A": "#4a3526",  # brown hair
    "J": "#3d5a80",  # jeans
    "s": "#c89572",  # deeper skin
    "|": "#232329",  # bistro chair
    "y": "#e0c070",  # blonde
    "M": "#1f1c22",  # black dress
    "z": "#8a939c",  # microphone
    "$": "#c98f3a",  # brass
    # More guests
    "a": "#a0522d",  # auburn hair
    "x": "#f3d2b8",  # fair skin
    "u": "#7a4a2e",  # dark skin
    "P": "#2a9d8f",  # teal
    "E": "#e07a8a",  # pink
    "O": "#c8603a",  # rust
    "U": "#6a8cc4",  # sky blue
    "Z": "#9c7cc4",  # lavender
    "j": "#5a4636",  # brown pants
}

AUNTIE = [
    "......ooo.......",
    ".....oHHHo......",
    "....ooHHHoo.....",
    "...oHHHHHHHHo...",
    "..oHHHHHHHHHHo..",
    "..oHHSSSSSSHHo..",
    "..oHSSSSSSSSHo..",
    "..oHSeSSSSeSHo..",
    "..oSSeSSSSeSSo..",
    "..oSSSSSSSSSSo..",
    "...oSSSmmSSSo...",
    "....ooSSSSoo....",
    "...oRRoooRRRo...",
    "..oRRLLLLLLRRo..",
    ".oRRRLLLLLLRRRo.",
    ".oRoRLLLLLLRoRo.",
    ".oRoRLLLLLLRoRo.",
    ".oSoLLLllLLLoSo.",
    "..ooLLLLLLLLoo..",
    "...oBBBBBBBBo...",
    "...oBBBooBBBo...",
    "...oBBo..oBBo...",
    "...oooo..oooo...",
    "....oFo..oFo....",
]

UNCLE = [
    "................",
    "....oooooooo....",
    "...oCCCCCCCCo...",
    "..oCCCCCCCCCCo..",
    "..occcccccccco..",
    "..oooooooooooo..",
    "..ohSSSSSSSSho..",
    "..ohSeSSSSeSho..",
    "..oSSeSSSSeSSo..",
    "..oSSSSSSSSSSo..",
    "...oShhhhhhSo...",
    "....oSSmmSSo....",
    "...oVVoIIoVVo...",
    "..oVVVVIIVVVVo..",
    ".oVVVVVVVVVVVVo.",
    ".oVoVVVYVVVVoVo.",
    ".oVoVVVVVVVVoVo.",
    ".oSoVVVYVVVVoSo.",
    "..ooVVVVVVVVoo..",
    "...oTTTTTTTTo...",
    "...oTTTooTTTo...",
    "...oTto..otTo...",
    "...oooo..oooo...",
    "....oFo..oFo....",
]

# Leaning out of the window: the sprite is centered on the window tile, so
# rows 5-15 land in the opening and the rest is left empty.
BAKER = [
    "................",
    "................",
    "................",
    "................",
    "....oooooooo....",
    "...oKKKKKKKKo...",
    "..okkkkkkkkkko..",
    "..oAAAAAAAAAAo..",
    "..oASSSSSSSSAo..",
    "..oSSeSSSSeSSo..",
    "..oSSeSSSSeSSo..",
    "...oSSSmmSSSo...",
    "....ooSSSSoo....",
    "..ooKKoWWoKKoo..",
    ".oKKKKKWWKKKKKo.",
    ".oKKKKkKKkKKKKo.",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
    "................",
]

IN_LINE = [
    "....oooooooo....",
    "...oCCCCCCCCo...",
    "..oCCCCCCCCCCo..",
    "..ooooooooooo...",
    "..oAAAAAAAAAAo..",
    "..oASSSSSSSSAo..",
    "..oSSeSSSSeSSo..",
    "..oSSeSSSSeSSo..",
    "..oSSSSSSSSSSo..",
    "...oSSSmmSSSo...",
    "....ooSSSSoo....",
    "...oGGoooGGGo...",
    "..oGGGGGGGGGGo..",
    ".oGGGGGGGGGGGGo.",
    ".oGoGGGGGGGGoGo.",
    ".oGoGGggGGGGoGo.",
    ".oSoGGGGGGGGoSo.",
    "..ooGGGGGGGGoo..",
    "...oJJJJJJJJo...",
    "...oJJJooJJJo...",
    "...oJJo..oJJo...",
    "...oooo..oooo...",
    "....oFo..oFo....",
    "................",
]

IN_LINE_2 = [
    "................",
    "....oooooooo....",
    "...oHHHHHHHHo...",
    "..oHHHHHHHHHHo..",
    "..oHHssssssHHo..",
    "..oHssssssssHo..",
    "..oHsessssesHo..",
    "..oHsessssesHo..",
    "..oHssssssssHo..",
    "..oHHssmmssHHo..",
    "..oHHossssoHHo..",
    "...oDDoooDDDo...",
    "..oDDDDDDDDDDo..",
    ".oDDDDDDDDDDDoo.",
    ".oDoDDDDDDDoqqo.",
    ".oDoDDDDDDDoQqo.",
    ".osoDDddDDDoQQo.",
    "..ooDDDDDDDDoo..",
    "...oBBBBBBBBo...",
    "...oBBBooBBBo...",
    "...oBBo..oBBo...",
    "...oooo..oooo...",
    "....oFo..oFo....",
    "................",
]

CHEF = [
    "................",
    "....oooooooo....",
    "...oHHHHHHHHo...",
    "..oNNNNNNNNNNo..",
    "..oNNNNNNNNNNo..",
    "..oHSSSSSSSSHo..",
    "..oSSSSSSSSSSo..",
    "..oSSeSSSSeSSo..",
    "..oSSeSSSSeSSo..",
    "..oSSSSSSSSSSo..",
    "...oSSSmmSSSo...",
    "....ooSSSSoo....",
    "...oWWoWWoWWo...",
    "..oWWWWoWWWWWo..",
    ".oWWWWWWoWWWWWo.",
    ".oWoWWWWWoWWoWo.",
    ".oWoBBBBBBBBoWo.",
    ".oSoBBBBBBBBoSo.",
    "..ooBBBBBBBBoo..",
    "...oBBBBBBBBo...",
    "...oBBBooBBBo...",
    "...oBBo..oBBo...",
    "...oooo..oooo...",
    "....oFo..oFo....",
]

# Sitting on a bistro chair, facing right toward the table (mirrored for the
# other side). H hair, S skin, C top, J pants get swapped per guest.
SEATED = [
    "................",
    "................",
    "................",
    ".....oooooo.....",
    "....oHHHHHHo....",
    "...oHHHHHHSSo...",
    "...oHHHHSSSSo...",
    "...oHHHSSSeSo...",
    "...oHHHSSSSSo...",
    "....oHHSSSmo....",
    ".....ooSSSo.....",
    "..|.oCCCCCo.....",
    "..|oCCCCCCCo....",
    "..|oCCCCCCCSo...",
    "..|oCCCCCCoo....",
    "..|oCCCCCCo.....",
    "..|oJJJJJJJJJo..",
    "..|oJJJJJJJJJo..",
    "..||||||||oJJo..",
    "..|......|oJJo..",
    "..|......|oJJo..",
    "..|......|oFFFo.",
    "................",
    "................",
]

# The same guest with longer hair, down past the shoulders...
SEATED_LONG = SEATED[:9] + [
    "...oHHHSSSmo....",
    "...oHHHoSSo.....",
    "..|oHHoCCCo.....",
    "..|oHHCCCCCo....",
    "..|ooCCCCCCSo...",
] + SEATED[14:]

# ...or up in a bun.
SEATED_BUN = [
    "................",
    "....ooo.........",
    "...oHHHo........",
    "....oHHoooo.....",
    "....oHHHHHHo....",
] + SEATED[5:]

# (hair, skin, top, pants, hair style) for each guest, as palette letters.
GUESTS = [
    ("H", "S", "M", "M", "short"),
    ("y", "S", "K", "J", "short"),
    ("A", "s", "W", "V", "short"),
    ("H", "s", "D", "B", "short"),
    # More guests (frames 23 on), so nobody's sitting at two tables at once.
    ("a", "x", "P", "B", "long"),
    ("H", "u", "R", "M", "short"),
    ("h", "S", "V", "T", "short"),
    ("H", "S", "E", "J", "bun"),
    ("y", "x", "U", "B", "long"),
    ("A", "u", "Y", "M", "bun"),
    ("H", "s", "G", "J", "short"),
    ("A", "S", "O", "B", "long"),
    ("H", "x", "Z", "M", "long"),
    ("M", "u", "I", "B", "short"),
    ("h", "s", "R", "T", "bun"),
    ("a", "S", "W", "j", "short"),
    ("H", "u", "P", "J", "long"),
    ("y", "S", "D", "j", "bun"),
    ("A", "x", "U", "T", "short"),
]


# Andy's Jazz Club: the pianist (seen from behind, on the piano bench), the
# drummer (only his top half shows over the kit), the singer, the sax player
# and the host.
PIANIST = [
    "................",
    "................",
    "....oooooooo....",
    "...oHHHHHHHHo...",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    "..oHHHHHHHHHHo..",
    ".oSHHHHHHHHHHSo.",
    "..oHHHHHHHHHHo..",
    "...oHHHHHHHHo...",
    "....ooSSSSoo....",
    "...oVVVIIVVVo...",
    "..oVVVVVVVVVVo..",
    ".oVVVVVVVVVVVVo.",
    ".oVVVVVVvVVVVVo.",
    ".oVVVVVVvVVVVVo.",
    ".oVVVVVVvVVVVVo.",
    "..oVVVVVVVVVVo..",
    ".oooooooooooooo.",
    ".oTTTTTTTTTTTTo.",
    ".otttttttttttto.",
    ".oo..........oo.",
    ".oo..........oo.",
    "................",
]

DRUMMER = [
    "................",
    "................",
    "....oooooooo....",
    "...oHHHHHHHHo...",
    "..oHHHHHHHHHHo..",
    "..oHSSSSSSSSHo..",
    "..oSSSSSSSSSSo..",
    "..oSSeSSSSeSSo..",
    "..oSSeSSSSeSSo..",
    "..oSSSSSSSSSSo..",
    "...oSSSmmSSSo...",
    "....ooSSSSoo....",
    "...oMMMMMMMMo...",
    "..oMMMMMMMMMMo..",
    ".oMMMMMMMMMMMMo.",
    ".oSoMMMMMMMMoSo.",
    "TSooMMMMMMMMooST",
    "..ooMMMMMMMMoo..",
    "...oMMMMMMMMo...",
    "...oooooooooo...",
    "................",
    "................",
    "................",
    "................",
]

SINGER = [
    "................",
    ".....oooooo.....",
    "....oAAAAAAo....",
    "...oAAAAAAAAo...",
    "..oAAAAAAAAAAo..",
    "..oAASSSSSSAAo..",
    "..oASSSSSSSSAo..",
    "..oASeSSSSeSAo..",
    "..oASeSSSSeSAo..",
    "..oASSSSSSSSAo..",
    "..oAASSmmSSAAo..",
    "..oAAozzSSoAAo..",
    ".oAAoRSzSRRoAAo.",
    ".oAoRRSSRRRRoAo.",
    "..ooRRRRRRRRoSo.",
    "...oRRRRRRRRo...",
    "...oRRRrRRRRo...",
    "..oRRRRrRRRRRo..",
    "..oRRRRrRRRRRo..",
    ".oRRRRRrRRRRRRo.",
    ".oRRRRRRrRRRRRo.",
    ".oRRRRRRrRRRRRo.",
    ".oooooooooooooo.",
    "................",
]

SAX = [
    "................",
    "....oooooooo....",
    "...oCCCCCCCCo...",
    ".oocccccccccccoo",
    "..oooooooooooo..",
    "..osssssssssso..",
    "..ossessssesso..",
    "..ossessssesso..",
    "..osssssssssso..",
    "...osssYsssso...",
    "....oosYssoo....",
    "...oBBIYIBBBo...",
    "..oBBBBYBBBBBo..",
    ".oBBBBBBYBBBBBo.",
    ".oBoBBBBsYsBoBo.",
    ".osoBBBBBY$BoBo.",
    "...oBBBBBBY$so..",
    "...oBBB$YBY$o...",
    "...oBBBB$YY$o...",
    "...oBBBBBBBBo...",
    "...oBBBooBBBo...",
    "...oBBo..oBBo...",
    "...oooo..oooo...",
    "....oFo..oFo....",
]


def guest(hair, skin, top, pants, style):
    table = str.maketrans({"H": hair, "S": skin, "C": top, "J": pants})
    rows = {"short": SEATED, "long": SEATED_LONG, "bun": SEATED_BUN}[style]
    return [r.translate(table) for r in rows]


if __name__ == "__main__":
    chef2 = [r.replace("H", "h").replace("S", "s") for r in CHEF]
    guests = [guest(*g) for g in GUESTS]
    bartender = [r.replace("N", "H") for r in CHEF]
    # The DJ: headphones on over a cap, a black tee.
    dj = [r.replace("W", "M").replace("B", "M") for r in CHEF]
    dj[1:7] = [
        "...o||||||||o...",
        "..o|KKKKKKKK|o..",
        "..o|kkkkkkkk|o..",
        "..o|AAAAAAAA|o..",
        ".o||SSSSSSSS||o.",
        ".o||SSSSSSSS||o.",
    ]
    # The host at Andy's: a black suit and tie.
    host = [r.replace("N", "H").replace("W", "M") for r in CHEF]
    host[12] = "...oMMoIIoMMo..."
    # The bartender at Andy's: brown hair, a burgundy shirt.
    bartender2 = [r.replace("N", "A").replace("H", "A").replace("S", "s").replace("W", "r") for r in CHEF]
    frames = [check(rows, 16, 24, PALETTE, name) for name, rows in (
        ("auntie", AUNTIE), ("uncle", UNCLE), ("baker", BAKER),
        ("in line", IN_LINE), ("in line 2", IN_LINE_2), ("chef", CHEF), ("chef 2", chef2),
        *((f"guest {i}", g) for i, g in enumerate(guests[:4])),
        *((f"guest {i} left", [r[::-1] for r in g]) for i, g in enumerate(guests[:4])),
        ("bartender", bartender), ("dj", dj),
        ("pianist", PIANIST), ("drummer", DRUMMER), ("singer", SINGER), ("sax", SAX), ("host", host),
        ("andy's bartender", bartender2),
        *((f"guest {i}", g) for i, g in enumerate(guests[4:], 4)),
        *((f"guest {i} left", [r[::-1] for r in g]) for i, g in enumerate(guests[4:], 4)),
    )]
    write_png(os.path.join(root(), "public/sprites/locals.png"), render(frames, PALETTE, 16, 24))
    print(f"Wrote {len(frames)} locals")
