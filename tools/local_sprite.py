"""Generates the people Hannah meets along the way: public/sprites/locals.png

One front-facing 16x24 frame each, in this order (the frame number in
content.js): 0 the auntie at the fruit stand and 1 the uncle at the xiangqi
tables (Chinatown), 2 the Decker's worker leaning out of the pop-up window
(just head and shoulders, so she fits in it), 3 and 4 two people in the bagel
line, 5 and 6 the chefs at Yokocho, then on the rooftop: 7-10 guests sitting
at tables facing right, 11-14 the same guests facing left, 15 the bartender,
16 the DJ.
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

# (hair, skin, top, pants) for each guest, as palette letters.
GUESTS = [
    ("H", "S", "M", "M"),
    ("y", "S", "K", "J"),
    ("A", "s", "W", "V"),
    ("H", "s", "D", "B"),
]


def guest(hair, skin, top, pants):
    table = str.maketrans({"H": hair, "S": skin, "C": top, "J": pants})
    return [r.translate(table) for r in SEATED]


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
    frames = [check(rows, 16, 24, PALETTE, name) for name, rows in (
        ("auntie", AUNTIE), ("uncle", UNCLE), ("baker", BAKER),
        ("in line", IN_LINE), ("in line 2", IN_LINE_2), ("chef", CHEF), ("chef 2", chef2),
        *((f"guest {i}", g) for i, g in enumerate(guests)),
        *((f"guest {i} left", [r[::-1] for r in g]) for i, g in enumerate(guests)),
        ("bartender", bartender), ("dj", dj),
    )]
    write_png(os.path.join(root(), "public/sprites/locals.png"), render(frames, PALETTE, 16, 24))
    print(f"Wrote {len(frames)} locals")
