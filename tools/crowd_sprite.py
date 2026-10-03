"""Generates the people who walk around the chapters: public/sprites/crowd.png

Everyone here has the same 12-frame walk as Hannah (down, up, right, left;
idle and two steps each), one person per row of the sheet. They're built from
a few head shapes (short hair, a bob, a baseball cap, curls, a bun), an outfit (clothes or a
graduation gown with a mortarboard) and their own colors, so adding someone is
one line in PEOPLE. The row number is the `look` in content.js.
Run:  python3 tools/crowd_sprite.py
Also writes tools/crowd_preview.png (6x scale) to eyeball the result.
"""

import os

from pixel import check, mirror, render, root, write_png

W, H = 16, 24


def shade(hex_color, f):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    clamp = lambda v: max(0, min(255, int(v)))
    return "#%02x%02x%02x" % (clamp(r * f), clamp(g * f), clamp(b * f))


BASE = {
    ".": None,
    "o": "#2b1d1a",  # outline
    "e": "#2b1d1a",  # eyes
    "m": "#a8604e",  # mouth
    "M": "#7d1f2c", "n": "#5a1520",  # Loyola maroon gown
    "K": "#1f1a1e",  # mortarboard
    "Y": "#e8b83e",  # tassel / stole
}

# ---------- heads (12 rows) ----------

HEADS = {
    "short": {
        "front": [
            "................",
            "....oooooooo....",
            "...oHHHHHHHHo...",
            "..oHHhHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHSSSSSSSSHo..",
            "..oSSSSSSSSSSo..",
            "..oSSeSSSSeSSo..",
            "..oSSeSSSSeSSo..",
            "..oSSSSSSSSSSo..",
            "...oSSSmmSSSo...",
            "....ooSSSSoo....",
        ],
        "back": [
            "................",
            "....oooooooo....",
            "...oHHHHHHHHo...",
            "..oHHHhHHhHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            ".oSHHHHHHHHHHSo.",
            "..oHHHHHHHHHHo..",
            "...oHHHHHHHHo...",
            "....oSSSSSSo....",
            ".....oSSSSo.....",
        ],
        "side": [
            "................",
            ".....oooooo.....",
            "....oHHHHHHo....",
            "...oHHHhHHHHo...",
            "...oHHHHHHHSo...",
            "...oHHHHHSSSSo..",
            "...oHHHSSSSeSo..",
            "...oHHsSSSSeSo..",
            "...oHHSSSSSSSo..",
            "...oHSSSSSSSmo..",
            "....oSSSSSSSo...",
            ".....ooSSSoo....",
        ],
    },
    "bob": {
        "front": [
            "................",
            "....oooooooo....",
            "...oHHHHHHHHo...",
            "..oHHhhHHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHSSSSSSHHo..",
            "..oHSSSSSSSSHo..",
            "..oHSeSSSSeSHo..",
            "..oHSeSSSSeSHo..",
            "..oHSSSSSSSSHo..",
            "..oHHSSmmSSHHo..",
            "..oHHoSSSSoHHo..",
        ],
        "back": [
            "................",
            "....oooooooo....",
            "...oHHHHHHHHo...",
            "..oHHHhhHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHhHHHHhHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..ooHHHHHHHHoo..",
        ],
        "side": [
            "................",
            ".....oooooo.....",
            "....oHHHHHHo....",
            "...oHHHHhhHHo...",
            "...oHHHHHHHHo...",
            "...oHHHHHHSSo...",
            "...oHHHHSSeSo...",
            "...oHHHHSSeSo...",
            "...oHHHHSSSSo...",
            "...oHHHHSSSmo...",
            "...oHHHHHoSSo...",
            "...ooHHHooSo....",
        ],
    },
    "cap": {
        "front": [
            "................",
            "....oooooooo....",
            "...oCCCCCCCCo...",
            "..oCCCCCCCCCCo..",
            "..occcccccccco..",
            "..oHSSSSSSSSHo..",
            "..oSSSSSSSSSSo..",
            "..oSSeSSSSeSSo..",
            "..oSSeSSSSeSSo..",
            "..oSSSSSSSSSSo..",
            "...oSSSmmSSSo...",
            "....ooSSSSoo....",
        ],
        "back": [
            "................",
            "....oooooooo....",
            "...oCCCCCCCCo...",
            "..oCCCCCCCCCCo..",
            "..oCCCccccCCCo..",
            "..oHHHHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            ".oSHHHHHHHHHHSo.",
            "..oHHHHHHHHHHo..",
            "...oHHHHHHHHo...",
            "....oSSSSSSo....",
            ".....oSSSSo.....",
        ],
        "side": [
            "................",
            ".....oooooo.....",
            "....oCCCCCCo....",
            "...oCCCCCCCCo...",
            "...occccccccooo.",
            "...oHHHHHSSSSo..",
            "...oHHHSSSSeSo..",
            "...oHHsSSSSeSo..",
            "...oHHSSSSSSSo..",
            "...oHSSSSSSSmo..",
            "....oSSSSSSSo...",
            ".....ooSSSoo....",
        ],
    },
    "curly": {
        "front": [
            "....oooooooo....",
            "...oHHhHHhHHo...",
            "..oHHHHHHHHHHo..",
            ".oHHhHHHHHHhHHo.",
            ".oHHHHHHHHHHHHo.",
            ".oHHSSSSSSSSHHo.",
            ".oHSSSSSSSSSSHo.",
            ".oHSSeSSSSeSSHo.",
            ".oHSSeSSSSeSSHo.",
            "..oSSSSSSSSSSo..",
            "...oSSSmmSSSo...",
            "....ooSSSSoo....",
        ],
        "back": [
            "....oooooooo....",
            "...oHHhHHhHHo...",
            "..oHHHHHHHHHHo..",
            ".oHHhHHHHHHhHHo.",
            ".oHHHHHHhHHHHHo.",
            ".oHHHHHHHHHHHHo.",
            ".oHHhHHHHHHhHHo.",
            ".oHHHHHHHHHHHHo.",
            "..oHHHHHHHHHHo..",
            "...oHHHHHHHHo...",
            "....oSSSSSSo....",
            ".....oSSSSo.....",
        ],
        "side": [
            "....oooooo......",
            "...oHHhHHHoo....",
            "..oHHHHHHhHHo...",
            "..oHhHHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHHhHHSSSSo..",
            "..oHHHHSSSSeSo..",
            "..oHHHsSSSSeSo..",
            "..oHHHSSSSSSSo..",
            "...oHSSSSSSSmo..",
            "....oSSSSSSSo...",
            ".....ooSSSoo....",
        ],
    },
    # Hair pulled up in a bun on top.
    "bun": {
        "front": [
            "......oooo......",
            "....ooHhHHoo....",
            "...oHHHHHHHHo...",
            "..oHHhHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHSSSSSSSSHo..",
            "..oSSSSSSSSSSo..",
            "..oSSeSSSSeSSo..",
            "..oSSeSSSSeSSo..",
            "..oSSSSSSSSSSo..",
            "...oSSSmmSSSo...",
            "....ooSSSSoo....",
        ],
        "back": [
            "......oooo......",
            "....ooHhHHoo....",
            "...oHHHHHHHHo...",
            "..oHHHhHHhHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            "..oHHHHHHHHHHo..",
            ".oSHHHHHHHHHHSo.",
            "..oHHHHHHHHHHo..",
            "...oHHHHHHHHo...",
            "....oSSSSSSo....",
            ".....oSSSSo.....",
        ],
        "side": [
            "....ooo.........",
            "...oHhHoooo.....",
            "...oHHHHHHHo....",
            "...oHHHhHHHHo...",
            "...oHHHHHHHSo...",
            "...oHHHHHSSSSo..",
            "...oHHHSSSSeSo..",
            "...oHHsSSSSeSo..",
            "...oHHSSSSSSSo..",
            "...oHSSSSSSSmo..",
            "....oSSSSSSSo...",
            ".....ooSSSoo....",
        ],
    },
}

# A mortarboard in place of the top of the head (rows 0-4), tassel on the side.
BOARD = {
    "front": [
        "..oooooooooooo..",
        ".oKKKKKKKKKKKKo.",
        "..oooKKKKKKoooY.",
        "..oHHKKKKKKHHoY.",
        "..oHHSSSSSSHHoY.",
    ],
    "back": [
        "..oooooooooooo..",
        ".oKKKKKKKKKKKKo.",
        "..oooKKKKKKoooY.",
        "..oHHKKKKKKHHoY.",
        "..oHHHHHHHHHHoY.",
    ],
    "side": [
        "...oooooooooo...",
        "..oKKKKKKKKKKo..",
        "..YooKKKKKKoo...",
        "..YoHKKKKKKHo...",
        "..YoHHHHHHSSo...",
    ],
}

# ---------- bodies (8 rows) and legs (4 rows) ----------

CLOTHES = {
    "front": [
        "...oTToooTTTo...",
        "..oTTTTTTTTTTo..",
        ".oTTTTTTTTTTTTo.",
        ".oToTTTTTTTToTo.",
        ".oToTTTttTTToTo.",
        ".oSoTTTTTTTToSo.",
        "..ooTTTTTTTToo..",
        "...oJJJJJJJJo...",
    ],
    "back": [
        "...oTTTTTTTTo...",
        "..oTTTTTTTTTTo..",
        ".oTTTTTTTTTTTTo.",
        ".oToTTTTTTTToTo.",
        ".oToTTTTTTTToTo.",
        ".oSoTTTTTTTToSo.",
        "..ootttttttoo...",
        "...oJJJJJJJJo...",
    ],
    "side": [
        "....oTTTTTTo....",
        "....oTTTTTTTo...",
        "....oTTTtTTTo...",
        "....oTTTtTTTo...",
        "....oTTTtTTTo...",
        "....oTTTSTTTo...",
        "....ottttttto...",
        "....oJJJJJJJo...",
    ],
}

WALK_A = [
    "...oJJJooJJJo...",
    "...oJJJooJJjo...",
    "...oFFo.oJJJo...",
    ".........oFFo...",
]
LEGS = {
    "front": {
        "idle": [
            "...oJJJooJJJo...",
            "...ojJJooJJjo...",
            "...oJJJooJJJo...",
            "...oFFo..oFFo...",
        ],
        "a": WALK_A,
        "b": mirror(WALK_A),
    },
    "side": {
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
    },
}

GOWN = {
    "front": [
        "...oMYMMMMYMo...",
        "..oMMYMMMMYMMo..",
        ".oMMMYMMMMYMMMo.",
        ".oMoMYMMMMYMoMo.",
        ".oMoMYMMMMYMoMo.",
        ".oSoMMMMMMMMoSo.",
        "..oMMMMMMMMMMo..",
        "..oMMMnMMnMMMo..",
    ],
    "back": [
        "...oMMMMMMMMo...",
        "..oMMMMMMMMMMo..",
        ".oMMMMMMMMMMMMo.",
        ".oMoMMMMMMMMoMo.",
        ".oMoMMMMMMMMoMo.",
        ".oSoMMMMMMMMoSo.",
        "..oMMMMMMMMMMo..",
        "..oMMMnMMnMMMo..",
    ],
    "side": [
        "....oMMMMMMo....",
        "....oMYMMMMMo...",
        "...oMMYMMMMMo...",
        "...oMMYMMMMMo...",
        "...oMMMYSMMMo...",
        "..oMMMMMMMMMMo..",
        "..oMMnMMnMMnMo..",
        "..oMMnMMnMMnMo..",
    ],
}
# The gown reaches the ground, so walking just shows the shoes stepping out.
HEM = ["..oMMMnMMnMMMo..", "..onMMMMMMMMno..", "..oooooooooooo.."]
GOWN_LEGS = {
    "front": {
        "idle": HEM + ["....oFo..oFo...."],
        "a": HEM + ["...oFFo........."],
        "b": HEM + [".........oFFo..."],
    },
    "side": {
        "idle": HEM + [".....oFFFo......"],
        "a": HEM + ["...oFFo..oFFo..."],
        "b": HEM + ["....oFFooFFo...."],
    },
}

# ---------- the people ----------
# style: head shape; gown: cap and gown instead of clothes. Colors are hex.
PEOPLE = [
    # Chinatown (0-5)
    dict(style="short", hair="#1e1a18", skin="#e9bd97", top="#3d4f73", pants="#33302e", shoes="#2b2626"),
    dict(style="bob", hair="#1e1a18", skin="#f0c9a4", top="#e07a8a", pants="#3d5a80", shoes="#f4f4f2"),
    dict(style="cap", hair="#1e1a18", skin="#c89572", top="#f4f4f2", pants="#46602c", shoes="#2b2626", cap="#c8323a"),
    dict(style="bob", hair="#b9b4ad", skin="#e9bd97", top="#8a4a5c", pants="#33302e", shoes="#2b2626"),
    dict(style="short", hair="#4a3526", skin="#8a5a3c", top="#e8b83e", pants="#3d5a80", shoes="#f4f4f2"),
    dict(style="bob", hair="#6b3a2a", skin="#f3d2b8", top="#2a9d8f", pants="#b59b78", shoes="#6a4a3a"),
    # Graduation: classmates in gowns (6-8), then families (9-11)
    dict(style="short", gown=True, hair="#4a3526", skin="#e9bd97", shoes="#2b2626"),
    dict(style="bob", gown=True, hair="#1e1a18", skin="#c89572", shoes="#2b2626"),
    dict(style="bob", gown=True, hair="#a0522d", skin="#f3d2b8", shoes="#2b2626"),
    dict(style="short", hair="#b9b4ad", skin="#f1c9a5", top="#6a8cc4", pants="#b59b78", shoes="#6a4a3a"),
    dict(style="bob", hair="#6b4a2a", skin="#f1c9a5", top="#9c7cc4", pants="#33302e", shoes="#2b2626"),
    dict(style="cap", hair="#1e1a18", skin="#7a4a2e", top="#7d1f2c", pants="#3d5a80", shoes="#f4f4f2", cap="#e8b83e"),
    # Decker's: the line at the window (12-14)
    dict(style="cap", hair="#4a3526", skin="#e9bd97", top="#5b7a3a", pants="#3d5a80", shoes="#2b2626", cap="#6b5a47"),
    dict(style="bob", hair="#1e1a18", skin="#c89572", top="#8a4a5c", pants="#33302e", shoes="#2b2626"),
    dict(style="short", hair="#e0c070", skin="#f3d2b8", top="#c8603a", pants="#33302e", shoes="#f4f4f2"),
    # More of Chinatown (15-20)
    dict(style="curly", hair="#1e1a18", skin="#7a4a2e", top="#c8323a", pants="#33302e", shoes="#f4f4f2"),
    dict(style="bun", hair="#1e1a18", skin="#f0c9a4", top="#f4f4f2", pants="#3d5a80", shoes="#2b2626"),
    dict(style="short", hair="#b9b4ad", skin="#e9bd97", top="#5b7a3a", pants="#b59b78", shoes="#6a4a3a"),
    dict(style="bun", hair="#b9b4ad", skin="#e9bd97", top="#9c7cc4", pants="#33302e", shoes="#2b2626"),
    dict(style="cap", hair="#4a3526", skin="#f3d2b8", top="#3d4f73", pants="#3d5a80", shoes="#f4f4f2", cap="#2f6b4a"),
    dict(style="curly", hair="#4a3526", skin="#c89572", top="#e8b83e", pants="#33302e", shoes="#2b2626"),
    # More of graduation: two more classmates (21-22), two more family (23-24)
    dict(style="curly", gown=True, hair="#1e1a18", skin="#8a5a3c", shoes="#2b2626"),
    dict(style="short", gown=True, hair="#e0c070", skin="#f3d2b8", shoes="#2b2626"),
    dict(style="short", hair="#4a3526", skin="#c89572", top="#2a9d8f", pants="#33302e", shoes="#2b2626"),
    dict(style="bob", hair="#b9b4ad", skin="#7a4a2e", top="#e07a8a", pants="#b59b78", shoes="#6a4a3a"),
    # A neighbor in the alley on moving day (25), a jogger past Decker's (26)
    dict(style="cap", hair="#1e1a18", skin="#e9bd97", top="#8a939c", pants="#33302e", shoes="#2b2626", cap="#3d4f73"),
    dict(style="bun", hair="#6b3a2a", skin="#e9bd97", top="#e07a8a", pants="#1f1c22", shoes="#f4f4f2"),
]


def palette(p):
    pal = dict(BASE)
    pal["H"], pal["h"] = p["hair"], shade(p["hair"], 1.35 if p["hair"] != "#1e1a18" else 2.2)
    pal["S"], pal["s"] = p["skin"], shade(p["skin"], 0.85)
    top = p.get("top", "#7d1f2c")
    pal["T"], pal["t"] = top, shade(top, 0.8)
    pants = p.get("pants", "#33302e")
    pal["J"], pal["j"] = pants, shade(pants, 0.8)
    pal["F"] = p["shoes"]
    cap = p.get("cap", "#c8323a")
    pal["C"], pal["c"] = cap, shade(cap, 0.75)
    return pal


def frames_for(p):
    pal = palette(p)
    heads = HEADS[p["style"]]
    body = GOWN if p.get("gown") else CLOTHES
    legs = GOWN_LEGS if p.get("gown") else LEGS
    frames = []
    for view in ("front", "back", "side"):
        head = heads[view]
        if p.get("gown"):
            head = BOARD[view] + head[5:]
        for step in ("idle", "a", "b"):
            leg = legs["side" if view == "side" else "front"][step]
            # On a step the body dips a pixel (the knees bend), for a bit of bounce.
            rows = ["." * W] + head + body[view] + leg[1:] if step != "idle" else head + body[view] + leg
            frames.append(check(rows, W, H, pal, f"{p['style']} {view} {step}"))
    return frames + [mirror(f) for f in frames[6:9]], pal


if __name__ == "__main__":
    sheet, preview = [], []
    bg = (243, 230, 216, 255)
    for p in PEOPLE:
        frames, pal = frames_for(p)
        sheet += render(frames, pal, W, H)
        preview += render(frames, pal, W, H, scale=6, gap=2, bg=bg)
    write_png(os.path.join(root(), "public/sprites/crowd.png"), sheet)
    write_png(os.path.join(root(), "tools/crowd_preview.png"), preview)
    print(f"Wrote {len(PEOPLE)} people")
