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
- **`AREAS`**: one entry per chapter. Each has a text `map` (the legend is at the top of the file), the `notes` hidden in it (map digits `1`-`9` pick which note goes where), optional characters in `npcs` (`at` puts one in a tile instead of on an `N`, like the Decker's worker in her window; `reach` lets one talk from further off, like a chef across the counter; `required: true` means she has to talk to them before the goal, and the goal's `lockedTalk` lines nudge her toward them, with `{who}` filled in from the `hint` of whoever's left), one-time `details` lines for walking up to a tile, boxes (`x`) to carry into a U-Haul (they stack up in the back of the truck), and an optional `goal`: a tile that, once every note is found (and box loaded), plays its `lines` and photo `cards`, then opens the exit or, with `advance: true`, moves straight on to the next chapter. `glimpse` shows Nathan slipping away right after the chapter's intro (he walks a `path` of `[column, row]` tiles and fades out, the camera follows him, then she says `lines`; `carry` puts a tile over his head and `sprite` changes his outfit, like his cap and gown), `reveal` has the camera find him before she does (the rooftop: he turns around, and she says `lines`), `player` swaps Hannah's outfit, `night` tints the chapter dark with glowing lights (`tint` picks any other color and strength, like Valentine's evening blue, Yokocho's dim amber or Decker's morning gold), and `objects` adds map characters just for that chapter (the Chinatown gate and shops, the chapel, the rooftop bar...). To make a place busier: `people` are passersby (a `look` from `tools/crowd_sprite.py`, walking a `path` of `[column, row]` tiles back and forth, or round with `loop`, or standing `at` a tile facing `face`; give them `lines` and they turn around to talk), seated people are `npcs` with `sprite: "seated"` on a chair or stool (the ceremony chairs, the Yokocho counter), `traffic` drives cars along a map `row` (they stop for her), and `pigeons` puts a few birds at each `[column, row]` that scatter when she comes close. The stray cat (the `cat` tile) wanders on its own, and water glints. On the rooftop, the goal's `view` has her walk up beside Nathan for its `lines`, then both turn to the skyline for the `end`. For the jazz club ending: `companion` has Nathan walk along a step behind her, `sway` makes a character bob to the music, `spotlights` shines a beam on whoever's at each `[column, row]`, and on the goal `meet` has the two of them take either side of the table, `ticket` shows the ticket card, and `fade` fades to black before moving on.
- **Photos**: put them in `public/photos/` and set `photo: "/photos/name.jpg"` on a note or goal card. They show sharp at the phone's full resolution (as a regular image laid over the game), cropped to a square from the middle. A long caption shrinks the photo to make room, so the words always fit on the card.
- **`ENDING`**: the closing lines on the last screen (the jazz club ticket itself is in the last area's `goal.ticket`). Before them, every note she found drops onto the screen as a scrapbook of polaroids: each note's `photo`, or until it has one, the spot in the map where she found it.

The game remembers which chapter she's on (in the browser's `localStorage`), so the title screen offers **Continue** / **Start over**; once she's seen the ending it offers **Play again** and a **Chapters** list instead. To reset while testing, run `localStorage.clear()` in the browser console.

Map mistakes (uneven rows, unknown characters, note/character count mismatches) show up as warnings in the browser console.

## Art

All pixel art is generated from text grids by small Python scripts (no dependencies):

```sh
python3 tools/hannah_sprite.py   # public/sprites/hannah.png + hannah_gown.png (+ tools/hannah_preview.png)
python3 tools/nathan_sprite.py   # public/sprites/nathan.png + nathan_gown.png (+ tools/nathan_preview.png)
python3 tools/grad_sprite.py     # public/sprites/grads.png (Krisjanis, Lexi and Micheal in chapter 3, + tools/grads_preview.png)
python3 tools/local_sprite.py    # public/sprites/locals.png (Chinatown locals, the Decker's line and worker, Yokocho's chefs, the rooftop guests, the band at Andy's)
python3 tools/crowd_sprite.py    # public/sprites/crowd.png (the passersby in `people`, each with a full walk, + tools/crowd_preview.png)
python3 tools/seated_sprite.py   # public/sprites/seated.png (families in the ceremony chairs, diners at Yokocho, + tools/seated_preview.png)
python3 tools/critter_sprite.py  # public/sprites/critters.png (pigeons and the stray cat, + tools/critters_preview.png)
python3 tools/tiles.py           # public/sprites/tiles.png + src/tileset.js (+ tools/tiles_preview.png)
```

`tiles.png` is a grid (`COLS` tiles across) so it stays small enough for phones. A picture bigger than one tile, like the skyline view from the rooftop, is drawn whole and cut into `name_row_col` pieces; a block of its character in a map fills in piece by piece. `tools/tiles.py` also says which tiles hang above Hannah's head (`OVERHEAD`, like the lanterns) and which come in a few looks picked per cell (`VARIANTS`, like grass with flowers or the different skyline towers).

## Music and sound

Every song is written as text in `src/music.js` (chords, a melody, and which instruments play along) and played by a tiny synthesizer in `src/synth.js`, so there are no audio files and every song loops without a gap. Each chapter picks its song with `music` in `src/content.js` (the title screen's is in `CONFIG`, the ending's in `ENDING`). To use a real recording instead, put it in `public/music/` and set `music: "/music/name.mp3"`. The top of `src/music.js` explains how to write or change a song, and typos show up as warnings in the browser console.

Sound effects (typing blips, the note chime, doors, boxes, the ticket) are at the bottom of `src/synth.js`. The speaker button in the top right mutes everything, and the game remembers it. Music starts on the first tap, since browsers don't allow sound before that.

## Text

The font is [Jersey 10](https://fonts.google.com/specimen/Jersey+10) (`public/fonts`, SIL Open Font License). It's a pixel font, so it's only crisp at whole multiples of its 10px grid: keep every text size at 10, 20, 30 or 40 (and 5 or 10 for text in the world, which is zoomed 2x). It has no ♥ or ♪, so those use the system font.

## Code

- `src/main.js`: scenes (title, chapter list, prologue, chapters, ending), map building, movement, camera, triggers, Nathan's glimpses
- `src/save.js`: remembers how far she got
- `src/audio.js`: plays the music (crossfading between chapters), sound effects and the mute button; `src/synth.js` and `src/musicWorker.js` make the sounds, `src/music.js` has the songs
- `src/content.js`: all story text, maps and photos
- `src/ui.js`: dialogue box, photo cards, chapter titles, hearts
- `src/kaplay.js`: engine setup (320×480 portrait canvas, letterboxed)
