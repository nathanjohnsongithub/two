import { k } from "./kaplay.js";
import { AREAS, CONFIG, ENDING, PROLOGUE } from "./content.js";
import { FULL, OVERHEAD, SOLID, TILE_COLS, TILE_NAMES, VARIANTS } from "./tileset.js";
import { COLORS, ui, say, showMemory, showTicket, hearts, titleCard, fadeOut, muteButton, overMute, photoOverlay, squareCrop } from "./ui.js";
import { playMusic, preloadMusic, sfx, unlockAudio } from "./audio.js";
import { loadProgress, saveProgress } from "./save.js";

const TILE = 16;
const SPEED = 90;
// World zoom. At 2x the 320x480 screen shows 10x15 tiles, which reads well on a phone.
const ZOOM = 2;
// Snapping the camera to whole screen pixels keeps the pixel art from shimmering.
const snap = (v) => Math.round(v * ZOOM) / ZOOM;

// 16x24 frames, see tools/hannah_sprite.py for the layout.
const WALK = {
  sliceX: 12,
  anims: {
    "down-idle": 0,
    "down-walk": { frames: [1, 0, 2, 0], loop: true, speed: 10 },
    "up-idle": 3,
    "up-walk": { frames: [4, 3, 5, 3], loop: true, speed: 10 },
    "right-idle": 6,
    "right-walk": { frames: [7, 6, 8, 6], loop: true, speed: 10 },
    "left-idle": 9,
    "left-walk": { frames: [10, 9, 11, 9], loop: true, speed: 10 },
  },
};
k.loadFont("pixel", "/fonts/Jersey10.ttf", { size: 10 });
k.loadSprite("hannah", "/sprites/hannah.png", WALK);
k.loadSprite("hannah_gown", "/sprites/hannah_gown.png", WALK);
k.loadSprite("nathan", "/sprites/nathan.png", WALK);
k.loadSprite("nathan_gown", "/sprites/nathan_gown.png", WALK);
k.loadSprite("grads", "/sprites/grads.png", { sliceX: 3 });
k.loadSprite("locals", "/sprites/locals.png", { sliceX: 53 });
// People sitting down (tools/seated_sprite.py), 16x40 so their chair lines up with the map's.
k.loadSprite("seated", "/sprites/seated.png", { sliceX: 19 });
// Pigeons and the stray cat (tools/critter_sprite.py).
k.loadSprite("critters", "/sprites/critters.png", { sliceX: 10 });
// The crowd (tools/crowd_sprite.py): one person per row, each with Hannah's
// 12-frame walk. Their animations are named "<look>-<direction>-<walk|idle>".
const crowdLoaded = new Promise((resolve, reject) => {
  const img = new Image();
  img.onload = () => {
    const looks = img.height / 24;
    const anims = {};
    for (let look = 0; look < looks; look++) {
      for (const [name, anim] of Object.entries(WALK.anims)) {
        const shift = (f) => look * 12 + f;
        anims[`${look}-${name}`] = typeof anim === "number" ? shift(anim) : { ...anim, frames: anim.frames.map(shift) };
      }
    }
    resolve(k.loadSprite("crowd", img, { sliceX: 12, sliceY: looks, anims }));
  };
  img.onerror = reject;
  img.src = "/sprites/crowd.png";
});
// tiles.png is a grid, TILE_COLS tiles across.
k.loadSprite("tiles", "/sprites/tiles.png", { sliceX: TILE_COLS, sliceY: Math.ceil(TILE_NAMES.length / TILE_COLS) });
const tileFrame = (name) => TILE_NAMES.indexOf(name);
const hasTile = (name) => TILE_NAMES.includes(name);

// Map characters that place an object tile (see the legend in content.js).
// A chapter can add its own characters, or change what one means, in `objects`.
const OBJECTS = {
  w: "window", H: "hedge", c: "counter", k: "sink", s: "stove", O: "stovePot", f: "fridge",
  T: "table", h: "chair", X: "tableCandle", Z: "tableEmptyPlate",
  "(": "couchL", C: "couchM", ")": "couchR", B: "bedTop", b: "bedBottom",
  u: "tub", t: "toilet", L: "washer", v: "tv", p: "plant",
  Y: "tree", n: "bench", "~": "water", l: "lantern", S: "storefront",
  W: "stoneWindow", d: "stoneDoor", G: "chairCap", U: "uhaul", Q: "dumpster", F: "fireEscape",
  r: "rail", K: "skyline", o: "bulbs", E: "elevator", "^": "roof", e: "lamppost", "*": "flowerBed",
  j: "nightstand", I: "brickWindow",
};
const objectFor = (area, ch) => {
  if (!ch || ch === " " || area.floors[ch]) return null;
  return ch === "#" ? area.wall : (area.objects?.[ch] ?? OBJECTS[ch] ?? null);
};

// Tiles that change along their bottom edge: walls show their front where
// there's floor in front of them, and roofs end in eaves.
const BOTTOMS = { wall: "wallFace", window: "windowFace", roof: "roofEave", roofCopper: "roofCopperEave" };

// Trim painted where two surfaces meet: shorelines around water, curbs along
// the road, rug borders, the stage's front, the ridge of a roof, and a cornice
// or gold trim along the tops of buildings.
const EDGES = [
  { tile: "rugEdge", on: (s) => s.startsWith("rug"), sides: "NSEW", meets: (s) => !s.startsWith("rug") },
  { tile: "shore", on: (s) => s.startsWith("water"), sides: "NSEW", meets: (s) => !s.startsWith("water") },
  { tile: "curb", on: (s) => s === "sidewalk", sides: "NSEW", meets: (s) => s.startsWith("road") || s === "crosswalk" },
  { tile: "stageSkirt", on: (s) => s === "stage", sides: "S", meets: (s) => s !== "stage" },
  { tile: "ridge", on: (s) => s.startsWith("roof"), sides: "N", meets: (s) => !s.startsWith("roof") },
  { tile: "decoTrim", on: (s) => s === "decoWall", sides: "N", meets: (s) => s !== "decoWall" && s !== "elevator" },
  { tile: "cornice", on: (s) => /^(brick|brickWindow|fireEscapeFront)/.test(s), sides: "N", meets: (s, cell) => !cell.object },
];
const SIDES = [["N", -1, 0], ["S", 1, 0], ["E", 0, 1], ["W", 0, -1]];

// Lights that glow through the night tint: [x, y, radius] from the tile's center.
const GLOWS = {
  bulbs: [[-4, -2, 3.5], [4, -2, 3.5]],
  tableCandle: [[0, -2, 7]],
  floorLamp: [[0, -6, 10]],
  desk: [[5, -5, 7]],
  nightstand: [[0, -4, 7]],
  stovePot: [[0, 0, 7]],
  lantern: [[0, 1, 8]],
  boxSign: [[0, 0, 9]],
  andon: [[0, -1, 8]],
  djBoothL: [[2, 6, 7]],
  djBoothR: [[-2, 6, 7]],
  bistroTable: [[0, -5, 5]],
  heater: [[0, -17, 11]],
  jazzTable: [[0, -4, 6]],
  reservedTable: [[0, -4, 6]],
  sconce: [[0, -2, 9]],
};

// Warm light that shows through a night tint, around a tile's center: a soft
// halo in two layers (a faint wide one, a brighter core) that flickers a little.
function addGlows(object, center) {
  for (const [x, y, radius] of GLOWS[object] ?? []) {
    const phase = k.rand(0, 6);
    for (const [scale, strength] of [[1.7, 0.08], [1, 0.16]]) {
      const glow = k.add([k.circle(radius * scale), k.pos(center.add(x, y)), k.color(255, 214, 122), k.opacity(strength), k.z(51)]);
      glow.onUpdate(() => { glow.opacity = strength * (1 + 0.25 * Math.sin(k.time() * 3 + phase)); });
    }
  }
}

// Where music notes drift up from: the DJ's decks, and the band at Andy's.
const MUSIC = new Set(["djBoothR", "drums", "pianoR"]);

// Things that steam: dinner on the stove, the bag of bagels. [x, y] from the
// tile's center, how far the puffs spread, and how often one rises.
const STEAM = {
  stovePot: { at: [0, -3], spread: 6, every: 0.3 },
  pickupTable: { at: [0, -9], spread: 3, every: 0.5 },
};

// Map tiles that come alive instead of being painted into the map (the stray cat).
const LIVE = new Set(["cat"]);

// Which way someone walking in `dir` faces. Only turn to a new axis when
// clearly heading that way: walking at a diagonal otherwise flips between two
// directions every frame, which keeps restarting the walk animation and makes
// it look stuck.
function turn(facing, dir) {
  const ax = Math.abs(dir.x);
  const ay = Math.abs(dir.y);
  const horizontal = facing === "left" || facing === "right";
  const useX = horizontal ? !(ay > ax * 1.3) : ax > ay * 1.3;
  return useX ? (dir.x > 0 ? "right" : "left") : dir.y > 0 ? "down" : "up";
}

// Some tiles come in a few looks (grass with flowers, different trees...).
// The look is picked from the cell's position, so a map looks the same every time.
function vary(name, r, c) {
  const looks = VARIANTS[name];
  if (!looks) return name;
  let h = Math.imul(r * 374761393 + c * 668265263, 1274126177) >>> 0;
  h = (h ^ (h >>> 15)) >>> 0;
  let roll = h % looks.reduce((sum, [, weight]) => sum + weight, 0);
  for (const [look, weight] of looks) if ((roll -= weight) < 0) return look;
  return name;
}

// Works out what goes in every cell of an area's map: its floor and object
// tile, trim along its edges, and the top half of anything tall.
function layout(area) {
  const rows = area.map;
  const defaultFloor = Object.values(area.floors)[0];
  // Objects sit on the floor most of the cells beside them have (so a lantern in
  // Chinatown gets sidewalk under it, and the last chair in a row stays on the
  // grass). Ties go to left, right, up, down in that order, and corners only
  // count when nothing beside it is floor. A rug only counts from two sides,
  // so furniture that just touches a rug's edge (the bed's corner) doesn't
  // drag a sliver of rug out under it.
  const floorAt = (r, c) => {
    for (const around of [[[0, -1], [0, 1], [-1, 0], [1, 0]], [[-1, -1], [1, 1], [-1, 1], [1, -1]]]) {
      const counts = new Map();
      for (const [dr, dc] of around) {
        const floor = area.floors[rows[r + dr]?.[c + dc]];
        if (floor) counts.set(floor, (counts.get(floor) ?? 0) + 1);
      }
      for (const [floor, n] of counts) if (floor.startsWith("rug") && n < 2) counts.delete(floor);
      let best = null;
      for (const [floor, n] of counts) if (!best || n > counts.get(best)) best = floor;
      if (best) return best;
    }
    return defaultFloor;
  };
  const counterish = (ch) => ["counter", "sink", "stove", "stovePot", "fridge"].includes(objectFor(area, ch));
  const cells = [];
  const grid = rows.map(() => []);
  rows.forEach((row, r) => {
    [...row].forEach((ch, c) => {
      if (ch === " ") return;
      if (area.floors[ch]) {
        cells.push((grid[r][c] = { r, c, ch, floor: area.floors[ch], object: null }));
        return;
      }
      let object = objectFor(area, ch);
      // A picture spread over a block of tiles (the skyline view): each cell
      // takes its piece, `name_row_col`, counted from the block's top left.
      if (object && hasTile(`${object}_0_0`)) {
        let top = r;
        let left = c;
        while (rows[top - 1]?.[c] === ch) top--;
        while (row[left - 1] === ch) left--;
        const piece = `${object}_${r - top}_${c - left}`;
        cells.push((grid[r][c] = { r, c, ch, floor: FULL.has(piece) ? null : floorAt(r, c), object: piece }));
        return;
      }
      // A row of the same piece joins up: beds, the taxi, the restaurant front
      // (which gets its door in the middle).
      let c0 = c;
      let c1 = c;
      while (row[c0 - 1] === ch) c0--;
      while (row[c1 + 1] === ch) c1++;
      if (c1 > c0 && hasTile(`${object}L`) && hasTile(`${object}R`)) {
        const door = c === Math.floor((c0 + c1) / 2) && hasTile(`${object}Door`);
        const piece = c === c0 ? "L" : c === c1 ? "R" : door ? "Door" : "M";
        if (hasTile(object + piece)) object += piece;
      }
      // Pieces stacked two high (tall windows, parked cars) share one look from their top half.
      const first = rows[r - 1]?.[c] !== ch;
      const look = object && vary(object, first ? r : r - 1, c);
      if (look && hasTile(`${look}N`) && hasTile(`${look}S`)) object = look + (first ? "N" : "S");
      // The U-Haul is a 2x3 block: back doors on top, cab at the bottom.
      if (ch === "U") {
        const part = rows[r - 1]?.[c] !== "U" ? "Back" : rows[r + 1]?.[c] !== "U" ? "Cab" : "Body";
        object = `uhaul${part}${row[c + 1] === "U" ? "L" : "R"}`;
      }
      // Couch pieces stacked vertically become an upright couch.
      const couch = (x) => x === "(" || x === "C" || x === ")";
      if (couch(ch) && !couch(row[c - 1]) && !couch(row[c + 1]) && (couch(rows[r - 1]?.[c]) || couch(rows[r + 1]?.[c]))) {
        object = { "(": "couchT", C: "couchMV", ")": "couchB" }[ch];
      }
      // Railings run vertically when there's railing above or below and none beside.
      if (ch === "r" && row[c - 1] !== "r" && row[c + 1] !== "r") object = "railV";
      // Counters along a side wall turn to face the room.
      if (object === "counter" && !counterish(row[c - 1]) && !counterish(row[c + 1])) {
        if (counterish(rows[r - 1]?.[c]) || counterish(rows[r + 1]?.[c])) object = "counterV";
      }
      const below = rows[r + 1]?.[c];
      if (BOTTOMS[object] && below && below !== " " && !BOTTOMS[objectFor(area, below)]) object = BOTTOMS[object];
      const floor = object && FULL.has(object) ? null : floorAt(r, c);
      cells.push((grid[r][c] = { r, c, ch, floor, object }));
    });
  });

  const surface = (cell) => (cell.object && FULL.has(cell.object) ? cell.object : cell.floor);
  for (const cell of cells) {
    const { r, c } = cell;
    cell.floorLook = cell.floor && vary(cell.floor, r, c);
    cell.objectLook = cell.object && vary(cell.object, r, c);
    // Tall things (lampposts, heaters) reach up into the cell above.
    if (cell.object && r > 0 && hasTile(`${cell.objectLook}Top`)) cell.top = `${cell.objectLook}Top`;
    cell.edges = [];
    for (const edge of EDGES) {
      if (!edge.on(surface(cell))) continue;
      for (const [side, dr, dc] of SIDES) {
        const next = grid[r + dr]?.[c + dc];
        if (edge.sides.includes(side) && next && edge.meets(surface(next), next)) cell.edges.push(edge.tile + side);
      }
    }
  }
  return cells;
}

// Each map is painted into two images up front: the ground (floors, walls,
// furniture) and whatever hangs above Hannah's head (lanterns, string lights,
// the tops of lampposts). The game then draws two sprites per area instead of
// hundreds of tiles.
const tilesImage = new Promise((resolve, reject) => {
  const img = new Image();
  img.onload = () => resolve(img);
  img.onerror = reject;
  img.src = "/sprites/tiles.png";
});
function bake(img, area, name) {
  const [ground, above] = [0, 1].map(() => {
    const canvas = document.createElement("canvas");
    canvas.width = area.map[0].length * TILE;
    canvas.height = area.map.length * TILE;
    const ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;
    return ctx;
  });
  const draw = (ctx, tile, r, c) =>
    ctx.drawImage(img, (tileFrame(tile) % TILE_COLS) * TILE, Math.floor(tileFrame(tile) / TILE_COLS) * TILE, TILE, TILE, c * TILE, r * TILE, TILE, TILE);
  for (const cell of layout(area)) {
    const { r, c } = cell;
    // Trim goes on whichever surface it belongs to: the floor, or an object covering it.
    const trimFloor = !cell.object || !FULL.has(cell.object);
    if (cell.floor) draw(ground, cell.floorLook, r, c);
    if (trimFloor) cell.edges.forEach((edge) => draw(ground, edge, r, c));
    if (cell.object && !LIVE.has(cell.object)) draw(OVERHEAD.has(cell.object) ? above : ground, cell.objectLook, r, c);
    if (!trimFloor) cell.edges.forEach((edge) => draw(ground, edge, r, c));
    if (cell.top) draw(above, cell.top, r - 1, c);
  }
  k.loadSprite(name, ground.canvas);
  k.loadSprite(`${name}-above`, above.canvas);
}

// The title screen is a little scene of its own: the two of them at the
// railing of the rooftop from chapter 5, looking out at the skyline.
const ROOFTOP = {
  floors: { ".": "deck" },
  objects: { V: "view", T: "bistroTable" },
  map: [
    "VVVVVVVVVVVVVV",
    "VVVVVVVVVVVVVV",
    "VVVVVVVVVVVVVV",
    "VVVVVVVVVVVVVV",
    "rrrrrrrrrrrrrr",
    "..............",
    "oooooooooooooo",
    "p..T......T..p",
  ],
};

k.load(crowdLoaded);
k.load(
  tilesImage.then((img) => {
    AREAS.forEach((area, i) => bake(img, area, `map-${i}`));
    bake(img, ROOFTOP, "map-title");
  }),
);

// Photos are loaded up front (keyed by path) so cards open instantly. Files in
// public/ are served from the top of the site, so "public/photos/a.jpg",
// "photos/a.jpg" and "/photos/a.jpg" all mean /photos/a.jpg.
const photoKey = (item) => (item?.photo ? `/${item.photo.replace(/^\/?(public\/)?/, "")}` : null);
AREAS.forEach((area) => {
  [...area.notes, ...(area.goal?.cards ?? [])].forEach((item) => {
    if (item.photo) k.loadSprite(photoKey(item), photoKey(item));
  });
});

// Catch typos in the maps early instead of getting a weird-looking level.
AREAS.forEach((area, a) => {
  const label = `Chapter ${a + 1}`;
  const width = area.map[0].length;
  const known = new Set([..."#PNDx 123456789", ...Object.keys(OBJECTS), ...Object.keys(area.objects ?? {}), ...Object.keys(area.floors)]);
  area.map.forEach((row, r) => {
    if (row.length !== width) console.warn(`${label} map row ${r + 1} is ${row.length} wide, expected ${width}`);
    for (const ch of row) if (!known.has(ch)) console.warn(`${label} map has unknown character "${ch}" in row ${r + 1}`);
  });
  const text = area.map.join("");
  const notes = [...text].filter((ch) => /[1-9]/.test(ch)).length;
  if (notes !== area.notes.length) console.warn(`${label} has ${notes} note tiles but ${area.notes.length} notes`);
  // Characters with `at` stand in the first tile with that character instead of on an N.
  const npcs = [...text].filter((ch) => ch === "N").length;
  const onN = area.npcs.filter((npc) => !npc.at).length;
  if (npcs !== onN) console.warn(`${label} has ${npcs} N tiles but ${onN} npcs`);
  const seats = {};
  for (const npc of area.npcs) if (npc.at) seats[npc.at] = (seats[npc.at] ?? 0) + 1;
  for (const [ch, n] of Object.entries(seats)) {
    const spots = [...text].filter((c) => c === ch).length;
    if (spots < n) console.warn(`${label} has ${n} people at "${ch}" but only ${spots} "${ch}" tiles`);
  }
});

// Text over the night sky, with a dark drop shadow so it stands out from the stars.
function skyText(label, size, pos, color) {
  const shadow = k.add([k.text(label, { size }), k.pos(pos.add(0, 2)), k.anchor("center"), k.color(10, 13, 34), k.opacity(1), k.fixed(), k.z(99)]);
  const text = k.add([k.text(label, { size }), k.pos(pos), k.anchor("center"), k.color(color), k.opacity(1), k.fixed(), k.z(100)]);
  text.onUpdate(() => { shadow.opacity = text.opacity; });
  return text;
}

// A button on a screen with no world behind it (the title, the chapter list).
function button(label, pos, onPick, { primary = false, width = 180 } = {}) {
  const b = k.add([
    k.rect(width, 30, { radius: 4 }),
    k.pos(pos),
    k.anchor("center"),
    k.color(primary ? COLORS.paper : COLORS.ink),
    k.outline(2, primary ? COLORS.ink : COLORS.paper),
    k.area(),
    k.fixed(),
    k.z(100),
  ]);
  b.add([k.text(label, { size: 20 }), k.pos(0, 1), k.anchor("center"), k.color(primary ? COLORS.ink : COLORS.paper)]);
  b.onClick(() => {
    unlockAudio();
    sfx("click");
    onPick();
  });
  return b;
}

k.scene("title", () => {
  playMusic(CONFIG.music);
  muteButton();
  const sky = k.Color.fromHex("#1b2340");
  k.setBackground(sky);
  k.setCamScale(ZOOM);
  const W = ROOFTOP.map[0].length * TILE;
  const H = ROOFTOP.map.length * TILE;
  // The rooftop fills the bottom of the screen; the sky above it holds the title.
  const camY = H - k.height() / ZOOM / 2;
  k.add([k.sprite("map-title"), k.pos(0, 0), k.z(0)]);
  k.add([k.sprite("map-title-above"), k.pos(0, 0), k.z(15)]);
  for (let i = 0; i < 30; i++) {
    const star = k.add([
      k.rect(1, 1),
      k.pos(Math.floor(k.rand(0, W)), Math.floor(k.rand(-110, -2))),
      k.color(k.choose([k.rgb(255, 250, 244), k.rgb(247, 214, 122)])),
      k.opacity(1),
      k.z(1),
    ]);
    const [phase, speed] = [k.rand(0, 6), k.rand(1, 3)];
    star.onUpdate(() => { star.opacity = 0.55 + 0.45 * Math.sin(k.time() * speed + phase); });
  }
  // The two of them at the railing, looking out at the city.
  const x = W / 2;
  const y = 5 * TILE + TILE / 2;
  k.add([k.sprite("hannah", { anim: "up-idle" }), k.pos(x - 7, y), k.anchor("center"), k.z(10)]);
  k.add([k.sprite("nathan", { anim: "up-idle" }), k.pos(x + 8, y - 1), k.anchor("center"), k.z(10)]);
  k.loop(1.4, () => hearts(k.toScreen(k.vec2(x, y - 14)), 1, true, 52));
  // Night, with the string lights and candles glowing.
  k.add([k.rect(k.width(), k.height()), k.color(11, 16, 48), k.opacity(0.4), k.fixed(), k.z(50)]);
  for (const cell of layout(ROOFTOP)) addGlows(cell.object, k.vec2(cell.c * TILE + TILE / 2, cell.r * TILE + TILE / 2));
  // Drift slowly along the skyline and back.
  const drift = (W - k.width() / ZOOM) / 2;
  const pan = () => k.setCamPos(snap(W / 2 + drift * Math.sin(k.time() * 0.15)), camY);
  pan();
  k.onUpdate(pan);

  skyText(CONFIG.title, 40, k.vec2(k.width() / 2, 64), COLORS.paper);
  skyText(CONFIG.subtitle, 20, k.vec2(k.width() / 2, 100), COLORS.accent);

  // First time: tap anywhere. After that, pick up where she left off, or
  // (once she's seen the ending) play again or jump to any chapter.
  const progress = loadProgress();
  const saved = AREAS[progress.chapter] ? progress.chapter : null;
  let primary = null;
  const start = (then) => () => {
    unlockAudio();
    then();
  };
  if (progress.done) {
    primary = start(() => k.go("prologue"));
    button("Play again", k.vec2(k.width() / 2, 148), primary, { primary: true });
    button("Chapters", k.vec2(k.width() / 2, 186), () => k.go("chapters"));
  } else if (saved !== null) {
    primary = start(() => k.go("area", saved));
    button("Continue", k.vec2(k.width() / 2, 134), primary, { primary: true });
    // Which chapter she's on, by name ("Chapter 5 · Decker's Bagels").
    skyText(`${AREAS[saved].chapter.split(" · ")[0]} · ${AREAS[saved].name}`, 20, k.vec2(k.width() / 2, 166), COLORS.paper);
    button("Start over", k.vec2(k.width() / 2, 200), () => k.go("prologue"));
  } else {
    primary = start(() => k.go("prologue"));
    const prompt = skyText("tap to start", 20, k.vec2(k.width() / 2, 160), COLORS.paper);
    prompt.onUpdate(() => { prompt.opacity = 0.7 + 0.3 * Math.sin(k.time() * 3); });
    k.onMousePress(() => { if (!overMute()) primary(); });
  }
  k.onKeyPress(["space", "enter"], primary);
});

// Once she's finished, any chapter can be replayed from the title screen.
k.scene("chapters", () => {
  k.setBackground(COLORS.ink);
  k.add([k.text("Chapters", { size: 30 }), k.pos(k.width() / 2, 34), k.anchor("center"), k.color(COLORS.paper)]);
  AREAS.forEach((area, i) => {
    const row = k.add([
      k.rect(k.width() - 40, 38, { radius: 4 }),
      k.pos(20, 62 + i * 44),
      k.color(COLORS.paper),
      k.opacity(0.08),
      k.outline(1, COLORS.muted),
      k.area(),
    ]);
    row.add([k.text(area.chapter, { size: 10 }), k.pos(10, 5), k.color(COLORS.accent)]);
    row.add([k.text(area.name, { size: 20 }), k.pos(10, 15), k.color(COLORS.paper)]);
    row.onClick(() => k.go("area", i));
  });
  button("Back", k.vec2(k.width() / 2, k.height() - 26), () => k.go("title"), { width: 120 });
  k.onKeyPress("escape", () => k.go("title"));
});

// A handwritten-style letter that fills in one line per tap.
k.scene("prologue", () => {
  playMusic(CONFIG.music);
  k.setBackground(COLORS.ink);
  const W = k.width() - 40;
  const card = k.add([
    k.rect(W, k.height() - 120, { radius: 6 }),
    k.pos(k.width() / 2, k.height() / 2),
    k.anchor("center"),
    k.color(COLORS.paper),
    k.outline(3, COLORS.muted),
  ]);
  let y = -card.height / 2 + 30;
  let shown = 0;
  const next = () => {
    if (shown >= PROLOGUE.length) {
      k.go("area", 0);
      return;
    }
    const line = card.add([
      k.text(PROLOGUE[shown], { size: 20, width: W - 40, lineSpacing: 2 }),
      k.pos(-W / 2 + 20, y),
      k.color(COLORS.ink),
      k.opacity(0),
    ]);
    k.tween(0, 1, 0.6, (v) => { line.opacity = v; });
    y += line.height + 12;
    shown++;
  };
  k.add([
    k.text("tap", { size: 10 }),
    k.pos(k.width() / 2, k.height() - 36),
    k.anchor("center"),
    k.color(COLORS.muted),
  ]);
  next();
  k.onMousePress(next);
  k.onKeyPress(["space", "enter"], next);
});

k.scene("area", (index) => {
  const area = AREAS[index];
  saveProgress({ chapter: index });
  if (area.music !== undefined) playMusic(area.music);
  // Get the next chapter's song ready while she plays this one.
  preloadMusic(AREAS[index + 1] ? AREAS[index + 1].music : ENDING.music);
  k.setBackground(k.Color.fromHex(area.background ?? "#1a1420"));
  k.setCamScale(ZOOM);

  const cols = area.map[0].length;
  const mapW = cols * TILE;
  const mapH = area.map.length * TILE;
  const cellCenter = (cell) => k.vec2(cell.c * TILE + TILE / 2, cell.r * TILE + TILE / 2);
  const cells = layout(area);

  k.add([k.sprite(`map-${index}`), k.pos(0, 0), k.z(0)]);
  k.add([k.sprite(`map-${index}-above`), k.pos(0, 0), k.z(15)]);
  // Night chapters get a blue tint over the world (under the HUD and popups);
  // `tint` sets any other color and strength, e.g. a dim restaurant.
  const tint = area.tint ?? (area.night ? [11, 16, 48, 0.4] : null);
  if (tint) k.add([k.rect(k.width(), k.height()), k.color(tint[0], tint[1], tint[2]), k.opacity(tint[3]), k.fixed(), k.z(50)]);

  // Walls and solid furniture become a few wide collision boxes (one per run
  // of solid tiles in a row) instead of one per tile.
  const solid = new Set(cells.filter((cell) => cell.object && SOLID.has(cell.object)).map((cell) => cell.r * cols + cell.c));
  area.map.forEach((row, r) => {
    for (let c = 0; c < cols; c++) {
      if (!solid.has(r * cols + c)) continue;
      const start = c;
      while (c + 1 < cols && solid.has(r * cols + c + 1)) c++;
      k.add([
        k.pos(start * TILE, r * TILE),
        k.area({ shape: new k.Rect(k.vec2(0), (c - start + 1) * TILE, TILE) }),
        k.body({ isStatic: true }),
      ]);
    }
  });

  let spawn = k.vec2(mapW / 2, mapH / 2);
  const tileCenter = ([c, r]) => k.vec2(c * TILE + TILE / 2, r * TILE + TILE / 2);
  const water = [];

  // The stray cat (the `cat` tile): sits and flicks its tail, wanders a couple
  // of tiles either way now and then, and trails after her a little while
  // she's carrying a box. Its frames are in tools/critter_sprite.py.
  const addCat = (home) => {
    const cat = k.add([k.sprite("critters", { frame: 4 }), k.pos(home), k.anchor("center"), k.z(8), { state: "sit", t: k.rand(2, 4), to: home.x }]);
    const [min, max] = [home.x - 2 * TILE, home.x + 2 * TILE];
    cat.onUpdate(() => {
      cat.t -= k.dt();
      // Keep an eye on her boxes.
      if (carried && cat.state !== "walk" && player.pos.dist(cat.pos) < 90) {
        const want = k.clamp(player.pos.x + (cat.pos.x < player.pos.x ? -22 : 22), min, max);
        if (Math.abs(want - cat.pos.x) > 8) Object.assign(cat, { state: "walk", to: want });
      }
      if (cat.state === "walk") {
        const d = cat.to - cat.pos.x;
        cat.pos.x += Math.sign(d) * Math.min(Math.abs(d), 22 * k.dt());
        // The walk frames face left.
        cat.flipX = d > 0;
        cat.frame = Math.floor(k.time() * 6) % 2 ? 7 : 8;
        if (Math.abs(d) < 0.5) Object.assign(cat, { state: "sit", t: k.rand(3, 7), flipX: false });
      } else if (cat.state === "loaf") {
        cat.frame = 9;
        if (cat.t < 0) Object.assign(cat, { state: "sit", t: k.rand(2, 5) });
      } else {
        // Sitting: flick the tail and blink now and then.
        const tick = (k.time() + home.x) % 4;
        cat.frame = tick < 0.5 ? 5 : tick > 3.85 ? 6 : 4;
        if (cat.t < 0) {
          const roll = k.rand();
          if (roll < 0.6) Object.assign(cat, { state: "walk", to: k.rand(min, max) });
          else if (roll < 0.85) Object.assign(cat, { state: "loaf", t: k.rand(4, 8) });
          else cat.t = k.rand(2, 4);
        }
      }
    });
    return cat;
  };

  const npcs = [];
  const addNpc = (data, center, isGoal) => {
    const npc = k.add([
      k.sprite(data.sprite ?? "nathan", { frame: data.frame ?? 0 }),
      k.pos(center),
      k.anchor("center"),
      k.area({ scale: k.vec2(0.6, 0.35), offset: k.vec2(0, 7) }),
      k.body({ isStatic: true }),
      k.z(9),
      // An NPC standing on the goal tile is handled by the goal, not by chatting.
      { data, near: false, isGoal },
    ]);
    // Musicians bob along to the music.
    if (data.sway) {
      const phase = k.rand(0, 6);
      npc.onUpdate(() => { npc.pos.y = center.y + Math.round(Math.sin(k.time() * 5 + phase)); });
    }
    // Name tag overhead, for named characters on an N (not for someone in a
    // window or a seat: it would cover their sign, or crowd the tables).
    if (data.name && !data.at) {
      // Size 10 in the world is 20 on screen at 2x zoom.
      const name = k.make([k.text(data.name, { size: 10 }), k.pos(0, 0.5), k.anchor("center"), k.color(COLORS.ink)]);
      const tag = npc.add([k.rect(Math.ceil(name.width) + 6, 11, { radius: 3 }), k.pos(0, -20), k.anchor("center"), k.color(COLORS.paper), k.opacity(0.9)]);
      tag.add(name);
    }
    npcs.push(npc);
  };
  const onN = area.npcs.filter((data) => !data.at);
  let npcIdx = 0;
  const goalSpots = [];
  const details = [];
  const truckBack = [];
  let boxTotal = 0;
  const doors = [];

  for (const cell of cells) {
    const { ch, c } = cell;
    const center = cellCenter(cell);
    if (ch === area.goal?.tile) goalSpots.push(center);
    if (cell.object?.startsWith("uhaulBack")) truckBack.push(cell);
    // The cat walks around, so its line goes wherever it is.
    const live = cell.object === "cat" ? addCat(center) : null;
    if (area.details?.[ch]) details.push({ at: live ?? { pos: center }, lines: area.details[ch], seen: false });
    if (cell.object?.startsWith("water")) water.push(center);
    if (tint) addGlows(cell.object, center);
    if (MUSIC.has(cell.object)) {
      // Music notes drifting up from the decks (or the band).
      k.loop(0.9, () => {
        k.add([
          k.text(k.choose(["♪", "♫"]), { size: 8, font: "monospace" }),
          k.pos(center.add(k.rand(-14, 4), -10)),
          k.color(k.choose([k.rgb(255, 214, 122), k.rgb(224, 80, 138), k.rgb(143, 194, 171)])),
          k.opacity(0.9),
          k.move(k.vec2(k.rand(-0.3, 0.3), -1), 10),
          k.lifespan(1.6, { fade: 0.8 }),
          k.z(52),
        ]);
      });
    }
    const steam = STEAM[cell.object];
    if (steam) {
      // A little steam so it looks like someone was just cooking.
      const from = center.add(...steam.at);
      k.loop(steam.every, () => {
        k.add([
          k.rect(2, 2),
          k.pos(from.add(k.rand(-steam.spread, steam.spread), k.rand(-3, 3))),
          k.color(255, 255, 255),
          k.opacity(0.7),
          k.move(k.vec2(k.rand(-0.2, 0.2), -1), k.rand(8, 14)),
          k.lifespan(1.2, { fade: 0.8 }),
          k.z(11),
        ]);
      });
    }

    if (ch === "P") {
      spawn = center;
    } else if (ch === "x") {
      boxTotal++;
      k.add([k.sprite("tiles", { frame: tileFrame("box") }), k.pos(center), k.anchor("center"), k.area({ scale: 0.7 }), k.z(5), "box"]);
    } else if (/[1-9]/.test(ch)) {
      const note = area.notes[Number(ch) - 1];
      if (!note) continue;
      const n = k.add([
        k.sprite("tiles", { frame: tileFrame("note") }),
        k.pos(center),
        k.anchor("center"),
        k.area({ scale: 0.7 }),
        k.z(5),
        "note",
        { note },
      ]);
      n.onUpdate(() => { n.pos.y = center.y + Math.sin(k.time() * 3 + c) * 2; });
    } else if (ch === "N") {
      const data = onN[npcIdx++];
      if (data) addNpc(data, center, ch === area.goal?.tile);
    } else if (ch === "D") {
      // Two exit doors side by side make one wide door, if the tile has halves.
      const row = area.map[cell.r];
      const half = row[c + 1] === "D" ? "L" : row[c - 1] === "D" ? "R" : "";
      const look = hasTile(area.door + half) ? area.door + half : area.door;
      doors.push(k.add([
        k.sprite("tiles", { frame: tileFrame(look) }),
        k.pos(center),
        k.anchor("center"),
        k.area(),
        k.body({ isStatic: true }),
        k.z(1),
        { near: true, open: false },
      ]));
    }
  }
  // Characters who stand in a tile (someone leaning out of a service window,
  // people sitting at tables). Several can share a character: each takes the
  // next tile with it, left to right, top to bottom.
  const taken = {};
  for (const data of area.npcs) {
    if (!data.at) continue;
    const cell = cells.filter((cell) => cell.ch === data.at)[(taken[data.at] = (taken[data.at] ?? -1) + 1)];
    if (cell) addNpc(data, cellCenter(cell), false);
  }

  const player = k.add([
    k.sprite(area.player ?? "hannah", { anim: "down-idle" }),
    k.pos(spawn),
    k.anchor("center"),
    // Only her feet collide, so her head can overlap walls above her.
    k.area({ scale: k.vec2(0.6, 0.35), offset: k.vec2(0, 7) }),
    k.body(),
    k.z(10),
    "player",
  ]);
  // The crowd (`people`): someone walking a `path` of [column, row] tiles back
  // and forth (or round and round, with `loop`), or standing `at` a tile facing
  // `face`. Anyone with `lines` stops, turns to her and says them when she
  // walks up. `look` picks who they are (a row in tools/crowd_sprite.py).
  // With `once`, they walk the path a single time and leave, and only talk to
  // her the first time.
  const toward = (d) => (Math.abs(d.x) > Math.abs(d.y) ? (d.x > 0 ? "right" : "left") : d.y > 0 ? "down" : "up");
  const people = (area.people ?? []).map((data) => {
    const points = (data.path ?? [data.at]).map(tileCenter);
    const facing = data.face ?? "down";
    return k.add([
      k.sprite("crowd", { anim: `${data.look}-${facing}-idle` }),
      k.pos(points[0]),
      k.anchor("center"),
      k.opacity(1),
      k.z(9),
      { data, facing, points, next: 1, dir: 1, rest: k.rand(0, 2), near: false, talking: false, said: false, gone: false },
    ]);
  });
  const pose = (person, walking) => {
    const name = `${person.data.look}-${person.facing}-${walking ? "walk" : "idle"}`;
    if (person.getCurAnim()?.name !== name) person.play(name);
  };
  const walkPeople = () => {
    for (const person of people) {
      const { points, data } = person;
      if (person.gone) continue;
      // Someone passing through only once waits out the intro and any popup,
      // so she doesn't miss them.
      if (data.once && busy() && !person.talking) {
        pose(person, false);
        continue;
      }
      if (person.talking || points.length < 2 || (person.rest -= k.dt()) > 0) {
        if (!person.talking && points.length < 2) person.facing = data.face ?? "down";
        pose(person, false);
        continue;
      }
      const to = points[person.next];
      const d = to.sub(person.pos);
      // Wait for her if she's right in the way.
      const ahead = player.pos.sub(person.pos);
      if (ahead.len() < 18 && d.len() > 0 && ahead.dot(d.unit()) > 4) {
        pose(person, false);
        continue;
      }
      const step = (data.speed ?? 32) * k.dt();
      if (d.len() <= step) {
        person.pos = to.clone();
        if (data.loop) {
          person.next = (person.next + 1) % points.length;
        } else if (data.once && !points[person.next + 1]) {
          // Off they go, for good.
          person.gone = true;
          k.tween(1, 0, 0.4, (v) => { person.opacity = v; }).onEnd(() => k.destroy(person));
          continue;
        } else {
          // The end of the path: stop for a moment, then head back.
          if (!points[person.next + person.dir]) {
            person.dir *= -1;
            person.rest = data.pause ?? k.rand(1, 3);
          }
          person.next += person.dir;
        }
      } else {
        person.pos = person.pos.add(d.unit().scale(step));
        person.facing = toward(d);
      }
      pose(person, true);
    }
  };

  // Traffic (`traffic`): cars along a map row, driving off one side and on
  // from the other. `car` is a two-tile vehicle facing the way it drives
  // ("taxi" goes west, "taxiEast" east). They stop for her, and for each other.
  const cars = [];
  for (const lane of area.traffic ?? []) {
    const dir = lane.car.endsWith("East") ? 1 : -1;
    const y = lane.row * TILE;
    const speed = lane.speed ?? 45;
    const spawnCar = (x) => {
      if (cars.some((car) => car.lane === lane && Math.abs(car.pos.x - x) < 3 * TILE)) return;
      const car = k.add([k.pos(x, y), k.z(4), { lane, dir, v: speed, speed }]);
      car.add([k.sprite("tiles", { frame: tileFrame(`${lane.car}L`) })]);
      car.add([k.sprite("tiles", { frame: tileFrame(`${lane.car}R`) }), k.pos(TILE, 0)]);
      cars.push(car);
    };
    // One already on the road, then another every few seconds.
    spawnCar(k.rand(0, mapW - 2 * TILE));
    const next = () => k.wait(k.rand(...(lane.every ?? [4, 9])), () => {
      spawnCar(dir > 0 ? -2 * TILE : mapW);
      next();
    });
    next();
  }
  const driveCars = () => {
    for (const car of [...cars]) {
      let want = car.speed;
      // Her feet in this lane, anywhere from beside the car to just ahead of it.
      const front = car.pos.x + (car.dir > 0 ? 2 * TILE : 0);
      const gap = (player.pos.x - front) * car.dir;
      if (Math.abs(player.pos.y + 7 - (car.pos.y + TILE / 2)) < 11 && gap > -2 * TILE - 6 && gap < 42) want = 0;
      for (const other of cars) {
        const ahead = (other.pos.x - car.pos.x) * car.dir;
        if (other !== car && other.lane === car.lane && ahead > 0 && ahead < 2 * TILE + 12) want = 0;
      }
      car.v += (want - car.v) * Math.min(1, k.dt() * 4);
      car.pos.x += car.v * car.dir * k.dt();
      if (car.pos.x < -3 * TILE || car.pos.x > mapW + TILE) {
        k.destroy(car);
        cars.splice(cars.indexOf(car), 1);
      }
    }
  };

  // Pigeons (`pigeons`: [column, row] tiles where a few of them peck around).
  // They scatter when she gets close, and come back once she's moved on.
  for (const home of (area.pigeons ?? []).map(tileCenter)) {
    for (let i = 0; i < 3; i++) {
      const spot = home.add(Math.round(k.rand(-10, 10)), Math.round(k.rand(-5, 5)));
      const bird = k.add([
        k.sprite("critters", { frame: 0, flipX: k.rand() < 0.5 }),
        k.pos(spot),
        k.anchor("center"),
        k.opacity(1),
        k.z(8),
        { state: "ground", t: k.rand(0, 1.5), vel: k.vec2(0, 0) },
      ]);
      const flap = () => { bird.frame = Math.floor(k.time() * 12 + i) % 2 ? 2 : 3; };
      bird.onUpdate(() => {
        bird.t -= k.dt();
        if (bird.state === "ground") {
          if (player.pos.dist(bird.pos) < 30) {
            // Off they go, away from her and up.
            const away = bird.pos.x >= player.pos.x ? 1 : -1;
            Object.assign(bird, { state: "fly", t: 1.4, vel: k.vec2(away * k.rand(45, 65), -k.rand(30, 45)), z: 20 });
            bird.flipX = away < 0;
          } else if (bird.t < 0) {
            // Peck, look around, or hop a step.
            const roll = k.rand();
            bird.frame = roll < 0.45 ? 1 : 0;
            if (roll > 0.8) {
              const hop = k.rand(-3, 3);
              bird.flipX = hop < 0;
              bird.pos.x = k.clamp(bird.pos.x + hop, spot.x - 8, spot.x + 8);
            }
            bird.t = k.rand(0.3, 1.2);
          }
        } else if (bird.state === "fly") {
          flap();
          bird.pos = bird.pos.add(bird.vel.scale(k.dt()));
          bird.opacity = Math.min(1, bird.t / 0.4);
          if (bird.t < 0) Object.assign(bird, { state: "gone", t: k.rand(5, 9), opacity: 0 });
        } else if (bird.state === "gone") {
          if (bird.t < 0 && player.pos.dist(spot) > 80) {
            const side = k.choose([-1, 1]);
            Object.assign(bird, { state: "back", pos: spot.add(side * 70, -50), opacity: 1 });
            bird.flipX = side > 0;
          }
        } else {
          // Gliding back down to where they were.
          flap();
          const d = spot.sub(bird.pos);
          if (d.len() < 2) Object.assign(bird, { state: "ground", pos: spot.clone(), frame: 0, z: 8, t: k.rand(0.5, 1.5) });
          else bird.pos = bird.pos.add(d.unit().scale(Math.min(d.len(), 60 * k.dt())));
        }
      });
    }
  }

  // Light glinting off the water.
  if (water.length) {
    k.loop(0.12, () => {
      const at = k.choose(water);
      k.add([
        k.rect(k.choose([2, 3, 4]), 1),
        k.pos(at.add(Math.round(k.rand(-7, 5)), Math.round(k.rand(-7, 7)))),
        k.color(255, 255, 255),
        k.opacity(0.8),
        k.lifespan(0.8, { fade: 0.6 }),
        k.z(1),
      ]);
    });
  }

  // Spotlights (`spotlights`: [column, row] of whoever's in them): a beam from
  // the top of the map down to them and a pool of light at their feet, bright
  // through the dim.
  for (const [c, r] of area.spotlights ?? []) {
    const at = tileCenter([c, r]);
    const light = [k.color(255, 236, 190), k.z(51)];
    const beam = k.add([k.polygon([k.vec2(at.x - 4, 0), k.vec2(at.x + 4, 0), k.vec2(at.x + 12, at.y + 9), k.vec2(at.x - 12, at.y + 9)]), k.opacity(0.12), ...light]);
    const pool = k.add([k.circle(12), k.pos(at.add(0, 9)), k.scale(1, 0.4), k.opacity(0.24), ...light]);
    beam.onUpdate(() => {
      const f = 1 + 0.08 * Math.sin(k.time() * 2.3 + c);
      beam.opacity = 0.12 * f;
      pool.opacity = 0.24 * f;
    });
  }

  // Someone who walks along with her (Nathan, at Andy's). He follows the path
  // she walked, a step behind.
  let companion = null;
  const trail = [];
  if (area.companion) {
    companion = k.add([k.pos(spawn.add(...(area.companion.from ?? [0, 18]))), k.z(9), { facing: "up" }]);
    // Nathan's frames are 2px taller than Hannah's; lift him 1px so their feet line up.
    companion.look = companion.add([k.sprite(area.companion.sprite, { anim: "up-idle" }), k.pos(0, -1), k.anchor("center")]);
  }
  // Walk (or stand) facing the way he just moved.
  const stride = (moved) => {
    const walking = moved.len() > 0.01;
    if (walking) companion.facing = turn(companion.facing, moved);
    const name = `${companion.facing}-${walking ? "walk" : "idle"}`;
    if (companion.look.getCurAnim()?.name !== name) companion.look.play(name);
  };
  const follow = () => {
    const last = trail[trail.length - 1];
    if (!last || player.pos.dist(last) > 4) trail.push(player.pos.clone());
    const before = companion.pos.clone();
    if (companion.pos.dist(player.pos) > 20) {
      let step = SPEED * k.dt();
      while (step > 0 && trail.length) {
        const d = trail[0].sub(companion.pos);
        if (d.len() <= step) {
          step -= d.len();
          companion.pos = trail.shift();
        } else {
          companion.pos = companion.pos.add(d.unit().scale(step));
          step = 0;
        }
      }
    } else {
      // Close enough: forget the path so far, and pick it up from here.
      trail.length = 0;
    }
    stride(companion.pos.sub(before));
    // Whoever is lower on screen is in front.
    companion.z = companion.pos.y > player.pos.y ? 11 : 9;
  };

  let facing = "down";
  const animate = (moving) => {
    const name = `${facing}-${moving ? "walk" : "idle"}`;
    if (player.getCurAnim()?.name !== name) player.play(name);
  };
  const face = (dir) => { facing = turn(facing, dir); };

  // HUD: a little pill per thing to collect (notes, boxes).
  const total = area.notes.length;
  let found = 0;
  let loaded = 0;
  let goalDone = !area.goal;
  let cutscene = false;
  let hudX = 4;
  const hudPill = (icon) => {
    k.add([k.rect(58, 24, { radius: 4 }), k.pos(hudX, 4), k.color(COLORS.paper), k.opacity(0.9), k.fixed(), k.z(89)]);
    k.add([k.sprite("tiles", { frame: tileFrame(icon) }), k.pos(hudX + 4, 8), k.fixed(), k.z(90)]);
    const text = k.add([k.text("", { size: 20 }), k.pos(hudX + 24, 6), k.color(COLORS.ink), k.fixed(), k.z(90)]);
    hudX += 64;
    return text;
  };
  const mute = muteButton();
  const noteCounter = total > 0 ? hudPill("note") : null;
  const boxCounter = boxTotal > 0 ? hudPill("box") : null;
  const updateCounter = () => {
    if (noteCounter) noteCounter.text = `${found}/${total}`;
    if (boxCounter) boxCounter.text = `${loaded}/${boxTotal}`;
  };
  updateCounter();

  const openDoors = () => {
    if (doors.some((door) => !door.open)) sfx("open");
    for (const door of doors) {
      if (door.open) continue;
      door.open = true;
      if (area.door === "door") door.frame = tileFrame("doorOpen");
      hearts(door.pos, 10);
      k.loop(1.2, () => hearts(door.pos.add(0, -10), 2));
    }
  };
  const allFound = () => found === total;
  // Characters marked `required` have to be talked to before the goal.
  const allTalked = () => npcs.every((npc) => !npc.data.required || npc.talked);
  const boxesLeft = () => boxTotal - loaded;
  const maybeOpen = () => { if (allFound() && goalDone) openDoors(); };

  const nextScene = () => k.go(index + 1 < AREAS.length ? "area" : "ending", index + 1);

  // The goal plays its lines and cards in order, then the exit opens (or,
  // with `advance`, the story moves straight on to the next chapter).
  const runGoal = async () => {
    cutscene = true;
    const goal = area.goal;
    if (goal.meet && companion) await meet(goalSpots[0]);
    const him = goal.view && npcs.find((npc) => npc.isGoal);
    if (him) await beside(him);
    if (goal.lines?.length) await say(goal.lines, goal.speaker);
    for (const card of goal.cards ?? []) await showMemory(card, photoKey(card), card.label);
    if (goal.ticket) await showTicket(goal.ticket);
    if (him) await lookOut(him);
    if (goal.end?.length) await say(goal.end, goal.endSpeaker);
    if (goal.advance) {
      if (goal.fade) await fadeOut();
      nextScene();
      return;
    }
    cutscene = false;
    goalDone = true;
    maybeOpen();
  };

  // Hannah and whoever came with her walk to either side of the goal (a table)
  // and face each other: she takes the side she's nearer.
  let scripted = false;
  const walkTo = (obj, to, dur, onStep, ease = k.easings.easeInOutQuad) =>
    new Promise((res) => k.tween(obj.pos.clone(), to, dur, (p) => { obj.pos = p; onStep?.(); }, ease).onEnd(res));
  const meet = async (spot) => {
    const left = spot.add(-TILE, 0);
    const right = spot.add(TILE, 0);
    const herSide = player.pos.x <= spot.x ? left : right;
    facing = herSide === left ? "right" : "left";
    scripted = true;
    let last = companion.pos.clone();
    const step = () => { stride(companion.pos.sub(last)); last = companion.pos.clone(); };
    await Promise.all([walkTo(player, herSide, 0.7), walkTo(companion, herSide === left ? right : left, 0.9, step)]);
    scripted = false;
    // Then he turns to face her.
    companion.facing = herSide === left ? "left" : "right";
    stride(k.vec2(0, 0));
    companion.z = 9;
  };

  // A glimpse of Nathan slipping away just ahead of her (`glimpse` in
  // content.js): the camera leaves her to follow him along his path until
  // he's gone, then comes back.
  let camFocus = null;
  let camAt = null;
  let camLag = 0;
  const wait = (t) => new Promise((res) => k.wait(t, res));
  const glimpse = async ({ path, carry, sprite, lines }) => {
    cutscene = true;
    const points = path.map(tileCenter);
    const him = k.add([k.pos(points[0]), k.z(9), { facing: "down" }]);
    const parts = [him.add([k.sprite(sprite ?? "nathan", { anim: "down-idle" }), k.pos(0, -1), k.anchor("center"), k.opacity(1)])];
    if (carry) parts.push(him.add([k.sprite("tiles", { frame: tileFrame(carry) }), k.pos(0, -19), k.anchor("center"), k.opacity(1)]));
    // She turns toward him.
    face(points[0].sub(player.pos));
    sfx("alert");
    const alert = player.add([k.text("!", { size: 10 }), k.pos(0, -20), k.anchor("center"), k.color(COLORS.accent)]);
    camFocus = him;
    await wait(1.1);
    for (const to of points.slice(1)) {
      const d = to.sub(him.pos);
      him.facing = turn(him.facing, d);
      parts[0].play(`${him.facing}-walk`);
      await walkTo(him, to, d.len() / (SPEED * 0.9), null, k.easings.linear);
    }
    // And he's gone.
    await new Promise((res) => k.tween(1, 0, 0.5, (v) => parts.forEach((part) => { part.opacity = v; })).onEnd(res));
    k.destroy(him);
    await wait(0.4);
    camFocus = null;
    await new Promise((res) => {
      const check = k.onUpdate(() => { if (camLag < 1) { check.cancel(); res(); } });
    });
    k.destroy(alert);
    cutscene = false;
    if (lines?.length) await say(lines);
  };

  // `reveal`: the camera finds him before she does. He's looking out at the
  // view, turns around when he feels someone watching, and she says `lines`.
  const NATHAN = { down: 0, up: 3, right: 6, left: 9 };
  const reveal = async ({ lines }) => {
    const him = npcs.find((npc) => npc.isGoal);
    if (!him) return;
    cutscene = true;
    camFocus = him;
    await wait(1.8);
    him.frame = NATHAN.down;
    hearts(him.pos.add(0, -14), 4);
    await wait(0.8);
    if (lines?.length) await say(lines);
    camFocus = null;
    await new Promise((res) => {
      const check = k.onUpdate(() => { if (camLag < 1) { check.cancel(); res(); } });
    });
    cutscene = false;
  };

  // A goal with `view`: she walks up beside him (whichever side she's nearer,
  // if there's room), they face each other for the `lines`, then both turn to
  // look out at the view before the `end`.
  const free = (spot) => cells.some((cell) => cell.floor && !cell.object && cellCenter(cell).dist(spot) < 1) && !npcs.some((npc) => npc.pos.dist(spot) < 1);
  const beside = async (him) => {
    const sides = [him.pos.add(TILE, 0), him.pos.add(-TILE, 0)].sort((a, b) => a.dist(player.pos) - b.dist(player.pos));
    const spot = sides.find(free) ?? sides[0];
    facing = toward(spot.sub(player.pos));
    scripted = true;
    await walkTo(player, spot, Math.max(0.3, player.pos.dist(spot) / SPEED));
    scripted = false;
    const herLeft = spot.x < him.pos.x;
    facing = herLeft ? "right" : "left";
    him.frame = herLeft ? NATHAN.left : NATHAN.right;
  };
  const lookOut = async (him) => {
    facing = "up";
    him.frame = NATHAN.up;
    await wait(0.6);
    hearts(player.pos.lerp(him.pos, 0.5).add(0, -16), 10);
    await wait(1.6);
  };

  let goalNear = false;

  // Boxes: walk into one to pick it up, walk it to the back of the U-Haul.
  let carried = null;
  player.onCollide("box", (b) => {
    if (carried) return;
    k.destroy(b);
    sfx("box");
    carried = k.add([k.sprite("tiles", { frame: tileFrame("box") }), k.pos(player.pos), k.anchor("center"), k.z(12)]);
  });
  // Where loaded boxes land in the back of the truck, from its top left corner:
  // three along the floor, then two stacked on top of them.
  const BOX_SLOTS = [[3, 3], [11, 3], [19, 3], [7, 0], [15, 0], [11, -3]];
  const loadBox = () => {
    const from = carried.pos.sub(4, 3);
    k.destroy(carried);
    carried = null;
    loaded++;
    // Let the truck respond right away (finishing the chapter after the last box).
    goalNear = false;
    updateCounter();
    const last = boxesLeft() === 0;
    const to = k.vec2(truckBack[0].c * TILE, truckBack[0].r * TILE).add(...BOX_SLOTS[Math.min(loaded, BOX_SLOTS.length) - 1]);
    // It goes up and over into the truck, and onto the stack.
    const box = k.add([k.sprite("tiles", { frame: tileFrame("miniBox") }), k.pos(from), k.z(12)]);
    k.tween(0, 1, 0.35, (t) => { box.pos = from.lerp(to, t).sub(0, Math.round(Math.sin(t * Math.PI) * 12)); }, k.easings.linear).onEnd(() => {
      box.pos = to;
      box.z = 0.5;
      sfx("load");
      hearts(to.add(4, 0), 6);
      if (last) {
        // Pull the doors shut.
        for (const cell of truckBack) {
          k.add([k.sprite("tiles", { frame: tileFrame(cell.object.replace("Back", "Closed")) }), k.pos(cell.c * TILE, cell.r * TILE), k.z(1)]);
        }
      }
    });
  };

  // Movement: arrows/WASD, or tap/hold anywhere to walk toward that spot.
  let target = null;
  let holding = false;
  let stuck = 0;
  const busy = () => ui.busy || cutscene;
  k.onMousePress(() => {
    unlockAudio();
    if (busy() || mute.isHovering()) return;
    holding = true;
    // Set the target right away: a quick tap can press and release within one frame.
    target = k.toWorld(k.mousePos());
  });
  k.onMouseRelease(() => { holding = false; });

  k.onUpdate(() => {
    if (!busy()) {
      let dir = k.vec2(0, 0);
      if (k.isKeyDown("left") || k.isKeyDown("a")) dir.x -= 1;
      if (k.isKeyDown("right") || k.isKeyDown("d")) dir.x += 1;
      if (k.isKeyDown("up") || k.isKeyDown("w")) dir.y -= 1;
      if (k.isKeyDown("down") || k.isKeyDown("s")) dir.y += 1;

      if (dir.len() > 0) target = null;
      else if (holding) target = k.toWorld(k.mousePos());

      if (dir.len() === 0 && target) {
        const d = target.sub(player.pos);
        if (d.len() < 3) target = null;
        else dir = d;
      }

      if (dir.len() > 0) {
        face(dir);
        const before = player.pos.clone();
        player.move(dir.unit().scale(SPEED));
        // Streets run off the sides of the map; stop at the edge.
        player.pos.x = k.clamp(player.pos.x, TILE / 2, mapW - TILE / 2);
        player.pos.y = k.clamp(player.pos.y, TILE / 2, mapH - TILE / 2);
        // Give up on a tap target if a wall is in the way.
        if (target && !holding) {
          stuck = player.pos.dist(before) < 0.3 ? stuck + 1 : 0;
          if (stuck > 12) { target = null; stuck = 0; }
        }
      }
      animate(dir.len() > 0);
      if (carried && truckBack.some((cell) => player.pos.dist(cellCenter(cell)) < 26)) loadBox();
    } else {
      animate(scripted);
      holding = false;
      target = null;
    }

    if (carried) carried.pos = player.pos.add(0, -16);
    if (companion && !cutscene) follow();
    walkPeople();
    driveCars();
    // Whoever is lower on screen is in front of her.
    for (const other of [...npcs, ...people]) other.z = other.pos.y > player.pos.y ? 11 : 9;

    // Keep the camera on the player (or whatever it's following for a moment)
    // without showing space outside the map.
    const clampAxis = (v, size, view) => (size <= view ? size / 2 : k.clamp(v, view / 2, size - view / 2));
    const look = camFocus?.pos ?? player.pos;
    const want = k.vec2(clampAxis(look.x, mapW, k.width() / ZOOM), clampAxis(look.y, mapH, k.height() / ZOOM));
    // Glide over to something and back; otherwise stay locked on her.
    camAt = camAt && (camFocus || camAt.dist(want) > 1) ? camAt.lerp(want, Math.min(1, k.dt() * 4)) : want;
    camLag = camAt.dist(want);
    k.setCamPos(snap(camAt.x), snap(camAt.y));

    // Proximity triggers fire once per approach. They only update while no
    // popup is open, so one trigger can't swallow another next to it.
    if (busy()) return;

    for (const npc of npcs) {
      if (npc.isGoal) continue;
      // `reach` lets someone talk from further off (a chef across the counter).
      const close = player.pos.dist(npc.pos) < (npc.data.reach ?? 22);
      // Some people are just there for company and don't say anything.
      if (close && !npc.near && npc.data.lines?.length) {
        say(allFound() && npc.data.linesAfter ? npc.data.linesAfter : npc.data.lines, npc.data.name).then(() => { npc.talked = true; });
      }
      npc.near = close;
      if (busy()) return;
    }

    for (const person of people) {
      if (person.gone) continue;
      const close = player.pos.dist(person.pos) < 22;
      if (close && !person.near && person.data.lines?.length && !(person.data.once && person.said)) {
        person.said = true;
        person.talking = true;
        person.facing = toward(player.pos.sub(person.pos));
        pose(person, false);
        say(person.data.lines, person.data.name).then(() => {
          person.talking = false;
          if (person.points.length < 2) person.facing = person.data.face ?? "down";
        });
      }
      person.near = close;
      if (busy()) return;
    }

    for (const detail of details) {
      if (!detail.seen && player.pos.dist(detail.at.pos) < 24) {
        detail.seen = true;
        say(detail.lines);
        return;
      }
    }

    if (area.goal && !goalDone && !carried) {
      const close = goalSpots.some((spot) => player.pos.dist(spot) < 24);
      // While there are boxes left to load the truck says nothing (the HUD counts them).
      if (close && !goalNear && boxesLeft() === 0) {
        if (allFound() && allTalked()) {
          runGoal();
        } else if (allFound()) {
          // "{who}" names whoever she still has to talk to (each one's `hint`).
          const who = npcs.filter((npc) => npc.data.required && !npc.talked).map((npc) => npc.data.hint ?? npc.data.name).join(", or ");
          say((area.goal.lockedTalk ?? area.goal.locked).map((line) => line.replace("{who}", who)), area.goal.speaker);
        } else {
          say(area.goal.locked, area.goal.speaker);
        }
      }
      goalNear = close;
      if (busy()) return;
    }

    for (const door of doors) {
      const close = player.pos.dist(door.pos) < 22;
      if (close && !door.near) {
        if (door.open) {
          nextScene();
        } else if (!allFound()) {
          const left = total - found;
          say([`It's locked. ${left} more ${left === 1 ? "note" : "notes"} to find here.`]);
        } else {
          say(["Not yet... there's still something to find here."]);
        }
      }
      door.near = close;
    }
  });

  player.onCollide("note", async (n) => {
    k.destroy(n);
    sfx("note");
    hearts(n.pos, 8);
    found++;
    updateCounter();
    await showMemory(n.note, photoKey(n.note), CONFIG.noteLabel);
    if (allFound()) {
      if (area.goal) await say(["That's all the notes here!"]);
      maybeOpen();
    }
  });

  maybeOpen();
  titleCard(area.chapter, area.name).then(async () => {
    if (area.intro?.length) await say(area.intro);
    if (area.glimpse) await glimpse(area.glimpse);
    if (area.reveal) await reveal(area.reveal);
  });
});

// The end: every note she found, dropped onto the page one by one like a
// scrapbook, then the sign-off over it.
k.scene("ending", () => {
  saveProgress({ done: true });
  playMusic(ENDING.music);
  k.setBackground(COLORS.ink);
  const center = k.vec2(k.width() / 2, k.height() / 2);
  const wait = (t) => new Promise((res) => k.wait(t, res));
  const fadeIn = (obj, dur = 0.8) =>
    new Promise((res) => k.tween(0, 1, dur, (v) => { obj.opacity = v; }).onEnd(res));
  const show = (str, size, color, pos, z = 100) =>
    k.add([
      k.text(str, { size, width: k.width() - 40, align: "center" }),
      k.pos(pos),
      k.anchor("center"),
      k.color(color),
      k.opacity(0),
      k.fixed(),
      k.z(z),
    ]);

  // A note's photo, or until there is one, the spot in the map where she found it.
  const SNAP = 64;
  const snapshot = (area, a, note, n) => {
    if (note.photo) return [k.sprite(photoKey(note), { width: SNAP, height: SNAP, quad: squareCrop(photoKey(note)) })];
    const mapW = area.map[0].length * TILE;
    const mapH = area.map.length * TILE;
    const r = area.map.findIndex((row) => row.includes(String(n + 1)));
    const c = area.map[r].indexOf(String(n + 1));
    const x = k.clamp(c * TILE + TILE / 2 - SNAP / 2, 0, mapW - SNAP);
    const y = k.clamp(r * TILE + TILE / 2 - SNAP / 2, 0, mapH - SNAP);
    const quad = k.quad(x / mapW, y / mapH, SNAP / mapW, SNAP / mapH);
    const parts = [k.sprite(`map-${a}`, { quad }), k.sprite(`map-${a}-above`, { quad })];
    const tint = area.tint ?? (area.night ? [11, 16, 48, 0.4] : null);
    if (tint) parts.push([k.rect(SNAP, SNAP), k.color(tint[0], tint[1], tint[2]), k.opacity(tint[3])]);
    return parts;
  };
  const memories = AREAS.flatMap((area, a) => area.notes.map((note, n) => ({ area, a, note, n })));
  // How far the page has dimmed for the sign-off (0 to 0.9).
  let dimmed = 0;
  const COLS = 3;
  const polaroid = ({ area, a, note, n }, i) => {
    const row = Math.floor(i / COLS);
    const inRow = Math.min(COLS, memories.length - row * COLS);
    const x = k.width() / 2 + (i % COLS - (inRow - 1) / 2) * 100 + k.rand(-6, 6);
    const y = 110 + row * 100 + k.rand(-5, 5);
    const card = k.add([
      k.rect(SNAP + 12, SNAP + 28, { radius: 2 }),
      k.pos(x, y),
      k.anchor("center"),
      k.color(COLORS.paper),
      k.outline(2, COLORS.muted),
      k.rotate(k.rand(-3, 3)),
      k.scale(1.5),
      k.fixed(),
      k.z(10 + i),
    ]);
    for (const part of snapshot(area, a, note, n)) card.add([...[part].flat(), k.pos(0, -8), k.anchor("center")]);
    // A real photo goes on top, sharp (see photoOverlay in ui.js), turned and
    // scaled with its polaroid, and fading with the page at the end.
    if (note.photo) {
      photoOverlay(card, photoKey(note), () => {
        const t = k.deg2rad(card.angle);
        const s = card.scale.x;
        return { x: card.pos.x + 8 * s * Math.sin(t), y: card.pos.y - 8 * s * Math.cos(t), w: SNAP * s, h: SNAP * s, angle: card.angle, opacity: 1 - dimmed / 0.9 };
      });
    }
    card.add([k.text(note.title, { size: 10, width: SNAP + 8, align: "center" }), k.pos(0, SNAP / 2 + 5), k.anchor("center"), k.color(COLORS.ink)]);
    // Dropped onto the page.
    k.tween(1.5, 1, 0.25, (v) => { card.scale = k.vec2(v); }, k.easings.easeOutQuad);
  };

  // A tap hurries the scrapbook along.
  let hurry = false;
  const skip = k.onMousePress(() => { hurry = true; });
  (async () => {
    await fadeIn(show("Year two", 30, COLORS.paper, k.vec2(k.width() / 2, 32)), 1);
    for (let i = 0; i < memories.length; i++) {
      polaroid(memories[i], i);
      if (!hurry) await wait(0.45);
    }
    await wait(hurry ? 0.6 : 2.2);
    skip.cancel();

    // Dim the scrapbook and sign off over it.
    const dim = k.add([k.rect(k.width(), k.height()), k.color(COLORS.ink), k.opacity(0), k.fixed(), k.z(90)]);
    k.tween(0, 0.9, 1.2, (v) => { dim.opacity = v; dimmed = v; });
    k.loop(0.4, () => hearts(k.vec2(k.rand(20, k.width() - 20), k.height() - 10), 1, true, 95));
    await fadeIn(show(ENDING.signoff, 30, COLORS.paper, center.add(0, -20)), 1.2);
    hearts(center.add(0, -20), 20, true, 101);
    await wait(1.5);
    await fadeIn(show(ENDING.closing, 20, COLORS.accent, center.add(0, 34)));
    await wait(2);
    const again = show("tap to play again", 20, COLORS.muted, center.add(0, 150));
    await fadeIn(again);
    again.onUpdate(() => { again.opacity = 0.5 + 0.5 * Math.sin(k.time() * 3); });
    const restart = () => k.go("title");
    k.onMousePress(restart);
    k.onKeyPress(["space", "enter"], restart);
  })();
});

// Dev-only handle for poking at the game from the console / tests.
if (import.meta.env.DEV) window.k = k;

k.go("title");
