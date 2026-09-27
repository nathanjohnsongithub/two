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
- **`AREAS`**: one entry per chapter. Each has a text `map` (the legend is at the top of the file), the `notes` hidden in it (map digits `1`-`9` pick which note goes where), optional characters in `npcs`, one-time `details` lines for walking up to a tile, boxes (`x`) to carry into a U-Haul, and an optional `goal`: a tile that, once every note is found (and box loaded), plays its `lines` and photo `cards`, then opens the exit or, with `advance: true`, moves straight on to the next chapter. `player` swaps Hannah's outfit, `night` tints the chapter dark with glowing lights, and `objects` adds map characters just for that chapter (the Chinatown shops, the chapel, the rooftop bar...).
- **Photos**: put them in `public/photos/` and set `photo: "/photos/name.jpg"` on a note or goal card. Square-ish crops look best.
- **`ENDING`**: the final letter and the gift reveal.

Map mistakes (uneven rows, unknown characters, note/character count mismatches) show up as warnings in the browser console.

## Art

All pixel art is generated from text grids by small Python scripts (no dependencies):

```sh
python3 tools/hannah_sprite.py   # public/sprites/hannah.png + hannah_gown.png (+ tools/hannah_preview.png)
python3 tools/nathan_sprite.py   # public/sprites/nathan.png
python3 tools/grad_sprite.py     # public/sprites/grads.png (classmates in chapter 3)
python3 tools/tiles.py           # public/sprites/tiles.png + src/tileset.js (+ tools/tiles_preview.png)
```

`tools/tiles.py` also says which tiles hang above Hannah's head (`OVERHEAD`, like the lanterns) and which come in a few looks picked per cell (`VARIANTS`, like grass with flowers or the different skyline towers).

## Code

- `src/main.js`: scenes (title, prologue, chapters, ending), map building, movement, camera, triggers
- `src/content.js`: all story text, maps and photos
- `src/ui.js`: dialogue box, photo cards, chapter titles, hearts
- `src/kaplay.js`: engine setup (320×480 portrait canvas, letterboxed)
