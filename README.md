# Year Two

A small top-down game for our 2nd anniversary. Hannah follows notes from Nathan through the memories of our second year, and they lead her to him. Built with [Kaplay](https://kaplayjs.com) + Vite.

## Run it

```sh
npm install
npm run dev      # also serves on your network, so you can test on your phone
npm run build    # outputs to dist/ (Vercel picks this up automatically)
```

## Editing the story

Everything personal lives in `src/content.js`:

- **`PROLOGUE`**: the letter shown before chapter 1.
- **`AREAS`**: one entry per chapter. Each has a text `map` (the legend is at the top of the file), the `notes` hidden in it (map digits `1`-`9` pick which note goes where), optional characters in `npcs` (`at` puts one in a tile instead of on an `N`, like the Decker's worker in her window; `reach` lets one talk from further off, like a chef across the counter; `required: true` means she has to talk to them before the goal, and the goal's `lockedTalk` lines nudge her toward them, with `{who}` filled in from the `hint` of whoever's left), one-time `details` lines for walking up to a tile, boxes (`x`) to carry into a U-Haul, and an optional `goal`: a tile that, once every note is found (and box loaded), plays its `lines` and photo `cards`, then opens the exit or, with `advance: true`, moves straight on to the next chapter. `glimpse` shows Nathan slipping away right after the chapter's intro (he walks a `path` of `[column, row]` tiles and fades out, the camera follows him, then she says `lines`; `carry` puts a tile over his head), `player` swaps Hannah's outfit, `night` tints the chapter dark with glowing lights (`tint` picks any other color, like Yokocho's dim amber), and `objects` adds map characters just for that chapter (the Chinatown gate and shops, the chapel, the rooftop bar...). For the jazz club ending: `companion` has Nathan walk along a step behind her, `sway` makes a character bob to the music, and on the goal `meet` has the two of them take either side of the table, `ticket` shows the ticket card, and `fade` fades to black before moving on.
- **Photos**: put them in `public/photos/` and set `photo: "/photos/name.jpg"` on a note or goal card. Square-ish crops look best.
- **`ENDING`**: the closing lines on the last screen (the jazz club ticket itself is in the last area's `goal.ticket`). Before them, every note she found drops onto the screen as a scrapbook of polaroids: each note's `photo`, or until it has one, the spot in the map where she found it.

The game remembers which chapter she's on (in the browser's `localStorage`), so the title screen offers **Continue** / **Start over**; once she's seen the ending it offers **Play again** and a **Chapters** list instead. To reset while testing, run `localStorage.clear()` in the browser console.

Map mistakes (uneven rows, unknown characters, note/character count mismatches) show up as warnings in the browser console.

## Art

All pixel art is generated from text grids by small Python scripts (no dependencies):

```sh
python3 tools/hannah_sprite.py   # public/sprites/hannah.png + hannah_gown.png (+ tools/hannah_preview.png)
python3 tools/nathan_sprite.py   # public/sprites/nathan.png (+ tools/nathan_preview.png)
python3 tools/grad_sprite.py     # public/sprites/grads.png (Krisjanis, Lexi and Micheal in chapter 3, + tools/grads_preview.png)
python3 tools/local_sprite.py    # public/sprites/locals.png (Chinatown locals, the Decker's line and worker, Yokocho's chefs, the rooftop guests, the band at Andy's)
python3 tools/tiles.py           # public/sprites/tiles.png + src/tileset.js (+ tools/tiles_preview.png)
```

`tiles.png` is a grid (`COLS` tiles across) so it stays small enough for phones. A picture bigger than one tile, like the skyline view from the rooftop, is drawn whole and cut into `name_row_col` pieces; a block of its character in a map fills in piece by piece. `tools/tiles.py` also says which tiles hang above Hannah's head (`OVERHEAD`, like the lanterns) and which come in a few looks picked per cell (`VARIANTS`, like grass with flowers or the different skyline towers).

## Text

The font is [Jersey 10](https://fonts.google.com/specimen/Jersey+10) (`public/fonts`, SIL Open Font License). It's a pixel font, so it's only crisp at whole multiples of its 10px grid: keep every text size at 10, 20, 30 or 40 (and 5 or 10 for text in the world, which is zoomed 2x). It has no ♥ or ♪, so those use the system font.

## Code

- `src/main.js`: scenes (title, chapter list, prologue, chapters, ending), map building, movement, camera, triggers, Nathan's glimpses
- `src/save.js`: remembers how far she got
- `src/content.js`: all story text, maps and photos
- `src/ui.js`: dialogue box, photo cards, chapter titles, hearts
- `src/kaplay.js`: engine setup (320×480 portrait canvas, letterboxed)
