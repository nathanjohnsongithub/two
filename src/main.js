import { k } from "./kaplay.js";
import { AREAS, CONFIG, ENDING, PROLOGUE } from "./content.js";
import { SOLID, TILE_NAMES } from "./tileset.js";
import { COLORS, ui, say, showMemory, hearts, titleCard } from "./ui.js";

const TILE = 16;
const SPEED = 90;
// World zoom. At 2x the 320x480 screen shows 10x15 tiles, which reads well on a phone.
const ZOOM = 2;

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
k.loadSprite("hannah", "/sprites/hannah.png", WALK);
k.loadSprite("hannah_gown", "/sprites/hannah_gown.png", WALK);
k.loadSprite("nathan", "/sprites/nathan.png");
k.loadSprite("grads", "/sprites/grads.png", { sliceX: 3 });
k.loadSprite("tiles", "/sprites/tiles.png", { sliceX: TILE_NAMES.length });
const tileFrame = (name) => TILE_NAMES.indexOf(name);

// Map characters that place an object tile (see the legend in content.js).
const OBJECTS = {
  w: "window", H: "hedge", c: "counter", k: "sink", s: "stove", O: "stovePot", f: "fridge",
  T: "table", h: "chair", X: "tableCandle", Z: "tableEmptyPlate",
  "(": "couchL", C: "couchM", ")": "couchR", B: "bedTop", b: "bedBottom",
  u: "tub", t: "toilet", L: "washer", v: "tv", p: "plant",
  Y: "tree", n: "bench", "~": "water", l: "lantern", S: "storefront",
  W: "stoneWindow", d: "stoneDoor", G: "chairCap", U: "uhaul", Q: "dumpster", F: "fireEscape",
  r: "rail", K: "skyline", o: "bulbs", E: "elevator",
};
// Objects that cover their whole tile, so no floor is needed underneath.
const FULL_TILES = new Set([
  "wall", "window", "brick", "hedge", "water", "storefront", "stove", "stovePot", "counter", "sink",
  "stone", "stoneWindow", "stoneDoor", "fireEscape", "rail", "railV", "skyline", "decoWall", "elevator",
  ...["Back", "Body", "Cab"].flatMap((part) => [`uhaul${part}L`, `uhaul${part}R`]),
]);

// Works out what goes in every cell of an area's map: its floor and object tile.
function layout(area) {
  const rows = area.map;
  const defaultFloor = Object.values(area.floors)[0];
  // Objects sit on whichever floor is next to them (so a lantern in Chinatown
  // gets sidewalk under it, not park grass).
  const floorAt = (r, c) => {
    for (const [dr, dc] of [[0, -1], [0, 1], [-1, 0], [1, 0], [-1, -1], [1, 1], [-1, 1], [1, -1]]) {
      const ch = rows[r + dr]?.[c + dc];
      if (ch && area.floors[ch]) return area.floors[ch];
    }
    return defaultFloor;
  };
  const cells = [];
  rows.forEach((row, r) => {
    [...row].forEach((ch, c) => {
      if (ch === " ") return;
      if (area.floors[ch]) {
        cells.push({ r, c, ch, floor: area.floors[ch], object: null });
        return;
      }
      let object = ch === "#" ? area.wall : (OBJECTS[ch] ?? null);
      // Side-by-side beds join into one wide bed.
      if (ch === "B" || ch === "b") {
        if (row[c + 1] === ch) object += "L";
        else if (row[c - 1] === ch) object += "R";
      }
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
      const floor = object && FULL_TILES.has(object) ? null : floorAt(r, c);
      cells.push({ r, c, ch, floor, object });
    });
  });
  return cells;
}

// Each map's floors and furniture are painted into one image up front, so the
// game draws a single sprite per area instead of hundreds of tiles.
const tilesImage = new Promise((resolve, reject) => {
  const img = new Image();
  img.onload = () => resolve(img);
  img.onerror = reject;
  img.src = "/sprites/tiles.png";
});
k.load(
  tilesImage.then((img) => {
    AREAS.forEach((area, i) => {
      const canvas = document.createElement("canvas");
      canvas.width = area.map[0].length * TILE;
      canvas.height = area.map.length * TILE;
      const ctx = canvas.getContext("2d");
      ctx.imageSmoothingEnabled = false;
      const draw = (name, r, c) =>
        ctx.drawImage(img, tileFrame(name) * TILE, 0, TILE, TILE, c * TILE, r * TILE, TILE, TILE);
      for (const cell of layout(area)) {
        if (cell.floor) draw(cell.floor, cell.r, cell.c);
        if (cell.object) draw(cell.object, cell.r, cell.c);
      }
      k.loadSprite(`map-${i}`, canvas);
    });
  }),
);

// Photos are loaded up front (keyed by path) so cards open instantly.
const photoKey = (item) => (item?.photo ? item.photo : null);
AREAS.forEach((area) => {
  [...area.notes, ...(area.goal?.cards ?? [])].forEach((item) => {
    if (item.photo) k.loadSprite(item.photo, item.photo);
  });
});

// Catch typos in the maps early instead of getting a weird-looking level.
AREAS.forEach((area, a) => {
  const label = `Chapter ${a + 1}`;
  const width = area.map[0].length;
  const known = new Set([..."#PNDx 123456789", ...Object.keys(OBJECTS), ...Object.keys(area.floors)]);
  area.map.forEach((row, r) => {
    if (row.length !== width) console.warn(`${label} map row ${r + 1} is ${row.length} wide, expected ${width}`);
    for (const ch of row) if (!known.has(ch)) console.warn(`${label} map has unknown character "${ch}" in row ${r + 1}`);
  });
  const text = area.map.join("");
  const notes = [...text].filter((ch) => /[1-9]/.test(ch)).length;
  if (notes !== area.notes.length) console.warn(`${label} has ${notes} note tiles but ${area.notes.length} notes`);
  const npcs = [...text].filter((ch) => ch === "N").length;
  if (npcs !== area.npcs.length) console.warn(`${label} has ${npcs} N tiles but ${area.npcs.length} npcs`);
});

k.scene("title", () => {
  k.setBackground(COLORS.ink);
  k.add([
    k.text(CONFIG.title, { size: 36 }),
    k.pos(k.width() / 2, k.height() / 2 - 40),
    k.anchor("center"),
    k.color(COLORS.paper),
  ]);
  k.add([
    k.text(CONFIG.subtitle, { size: 14 }),
    k.pos(k.width() / 2, k.height() / 2),
    k.anchor("center"),
    k.color(COLORS.accent),
  ]);
  const prompt = k.add([
    k.text("tap to start", { size: 11 }),
    k.pos(k.width() / 2, k.height() / 2 + 80),
    k.anchor("center"),
    k.color(COLORS.muted),
    k.opacity(1),
  ]);
  prompt.onUpdate(() => { prompt.opacity = 0.5 + 0.5 * Math.sin(k.time() * 3); });
  k.loop(0.5, () => hearts(k.vec2(k.rand(20, k.width() - 20), k.height() - 20), 1));

  const start = () => k.go("prologue");
  k.onMousePress(start);
  k.onKeyPress(["space", "enter"], start);
});

// A handwritten-style letter that fills in one line per tap.
k.scene("prologue", () => {
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
      k.text(PROLOGUE[shown], { size: 13, width: W - 40, lineSpacing: 4 }),
      k.pos(-W / 2 + 20, y),
      k.color(COLORS.ink),
      k.opacity(0),
    ]);
    k.tween(0, 1, 0.6, (v) => { line.opacity = v; });
    y += line.height + 16;
    shown++;
  };
  k.add([
    k.text("tap", { size: 9 }),
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
  k.setBackground(k.Color.fromHex(area.background ?? "#1a1420"));
  k.camScale(ZOOM);

  const cols = area.map[0].length;
  const mapW = cols * TILE;
  const mapH = area.map.length * TILE;
  const cellCenter = (cell) => k.vec2(cell.c * TILE + TILE / 2, cell.r * TILE + TILE / 2);
  const cells = layout(area);

  k.add([k.sprite(`map-${index}`), k.pos(0, 0), k.z(0)]);
  // Night chapters get a blue tint over the world (under the HUD and popups).
  if (area.night) k.add([k.rect(k.width(), k.height()), k.color(11, 16, 48), k.opacity(0.4), k.fixed(), k.z(50)]);

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
  let npcIdx = 0;
  const npcs = [];
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
    if (area.details?.[ch]) details.push({ pos: center, lines: area.details[ch], seen: false });
    if (area.night && (cell.object === "bulbs" || cell.object === "tableCandle")) {
      // Warm light that shows through the night tint.
      const bulb = cell.object === "bulbs";
      const spots = bulb ? [k.vec2(-4, -2), k.vec2(4, -2)] : [k.vec2(0, -2)];
      for (const offset of spots) {
        const glow = k.add([k.circle(bulb ? 3.5 : 7), k.pos(center.add(offset)), k.color(255, 214, 122), k.opacity(0.22), k.z(51)]);
        const phase = k.rand(0, 6);
        glow.onUpdate(() => { glow.opacity = 0.2 + 0.05 * Math.sin(k.time() * 3 + phase); });
      }
    }
    if (cell.object === "stovePot") {
      // A little steam so it looks like someone was just cooking.
      k.loop(0.3, () => {
        k.add([
          k.rect(2, 2),
          k.pos(center.add(k.rand(-6, 6), k.rand(-6, 0))),
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
      const data = area.npcs[npcIdx++];
      if (!data) continue;
      const npc = k.add([
        k.sprite(data.sprite ?? "nathan", { frame: data.frame ?? 0 }),
        k.pos(center),
        k.anchor("center"),
        k.area({ scale: k.vec2(0.6, 0.35), offset: k.vec2(0, 7) }),
        k.body({ isStatic: true }),
        k.z(9),
        // An NPC standing on the goal tile is handled by the goal, not by chatting.
        { data, near: false, isGoal: ch === area.goal?.tile },
      ]);
      const tag = npc.add([k.rect(data.name.length * 6 + 8, 12, { radius: 3 }), k.pos(0, -20), k.anchor("center"), k.color(COLORS.paper), k.opacity(0.9)]);
      tag.add([k.text(data.name, { size: 8 }), k.anchor("center"), k.color(COLORS.ink)]);
      npcs.push(npc);
    } else if (ch === "D") {
      doors.push(k.add([
        k.sprite("tiles", { frame: tileFrame(area.door) }),
        k.pos(center),
        k.anchor("center"),
        k.area(),
        k.body({ isStatic: true }),
        k.z(1),
        { near: true, open: false },
      ]));
    }
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
  let facing = "down";
  const animate = (moving) => {
    const name = `${facing}-${moving ? "walk" : "idle"}`;
    if (player.getCurAnim()?.name !== name) player.play(name);
  };
  // Only turn to a new axis when clearly heading that way. Walking at a
  // diagonal otherwise flips between two directions every frame, which keeps
  // restarting the walk animation and makes it look stuck.
  const face = (dir) => {
    const ax = Math.abs(dir.x);
    const ay = Math.abs(dir.y);
    const horizontal = facing === "left" || facing === "right";
    const useX = horizontal ? !(ay > ax * 1.3) : ax > ay * 1.3;
    facing = useX ? (dir.x > 0 ? "right" : "left") : dir.y > 0 ? "down" : "up";
  };

  // HUD: a little pill per thing to collect (notes, boxes).
  const total = area.notes.length;
  let found = 0;
  let loaded = 0;
  let goalDone = !area.goal;
  let cutscene = false;
  let hudX = 4;
  const hudPill = (icon) => {
    k.add([k.rect(62, 22, { radius: 4 }), k.pos(hudX, 4), k.color(COLORS.paper), k.opacity(0.9), k.fixed(), k.z(89)]);
    k.add([k.sprite("tiles", { frame: tileFrame(icon) }), k.pos(hudX + 4, 7), k.fixed(), k.z(90)]);
    const text = k.add([k.text("", { size: 11 }), k.pos(hudX + 24, 9), k.color(COLORS.ink), k.fixed(), k.z(90)]);
    hudX += 68;
    return text;
  };
  const noteCounter = total > 0 ? hudPill("note") : null;
  const boxCounter = boxTotal > 0 ? hudPill("box") : null;
  const updateCounter = () => {
    if (noteCounter) noteCounter.text = `${found}/${total}`;
    if (boxCounter) boxCounter.text = `${loaded}/${boxTotal}`;
  };
  updateCounter();

  const openDoors = () => {
    for (const door of doors) {
      if (door.open) continue;
      door.open = true;
      if (area.door === "door") door.frame = tileFrame("doorOpen");
      hearts(door.pos, 10);
      k.loop(1.2, () => hearts(door.pos.add(0, -10), 2));
    }
  };
  const allFound = () => found === total;
  const boxesLeft = () => boxTotal - loaded;
  const maybeOpen = () => { if (allFound() && goalDone) openDoors(); };

  const nextScene = () => k.go(index + 1 < AREAS.length ? "area" : "ending", index + 1);

  // The goal plays its lines and cards in order, then the exit opens (or,
  // with `advance`, the story moves straight on to the next chapter).
  const runGoal = async () => {
    cutscene = true;
    const goal = area.goal;
    if (goal.lines?.length) await say(goal.lines, goal.speaker);
    for (const card of goal.cards ?? []) await showMemory(card, photoKey(card), card.label);
    if (goal.end?.length) await say(goal.end);
    if (goal.advance) {
      nextScene();
      return;
    }
    cutscene = false;
    goalDone = true;
    maybeOpen();
  };

  let goalNear = false;

  // Boxes: walk into one to pick it up, walk it to the back of the U-Haul.
  let carried = null;
  player.onCollide("box", (b) => {
    if (carried) return;
    k.destroy(b);
    carried = k.add([k.sprite("tiles", { frame: tileFrame("box") }), k.pos(player.pos), k.anchor("center"), k.z(12)]);
  });
  const loadBox = () => {
    k.destroy(carried);
    carried = null;
    loaded++;
    // Let the truck respond right away ("2 more boxes", or finishing the chapter).
    goalNear = false;
    updateCounter();
    const back = cellCenter(truckBack[0]).add(TILE / 2, 0);
    hearts(back, 6);
    if (boxesLeft() === 0) {
      // Pull the doors shut.
      for (const cell of truckBack) {
        k.add([k.sprite("tiles", { frame: tileFrame(cell.object.replace("Back", "Closed")) }), k.pos(cell.c * TILE, cell.r * TILE), k.z(1)]);
      }
    }
  };

  // Movement: arrows/WASD, or tap/hold anywhere to walk toward that spot.
  let target = null;
  let holding = false;
  let stuck = 0;
  const busy = () => ui.busy || cutscene;
  k.onMousePress(() => {
    if (busy()) return;
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
        // Give up on a tap target if a wall is in the way.
        if (target && !holding) {
          stuck = player.pos.dist(before) < 0.3 ? stuck + 1 : 0;
          if (stuck > 12) { target = null; stuck = 0; }
        }
      }
      animate(dir.len() > 0);
      if (carried && truckBack.some((cell) => player.pos.dist(cellCenter(cell)) < 26)) loadBox();
    } else {
      animate(false);
      holding = false;
      target = null;
    }

    if (carried) carried.pos = player.pos.add(0, -16);

    // Keep the camera on the player without showing space outside the map.
    // Snapping to whole screen pixels keeps the pixel art from shimmering.
    const clampAxis = (v, size, view) => (size <= view ? size / 2 : k.clamp(v, view / 2, size - view / 2));
    const snap = (v) => Math.round(v * ZOOM) / ZOOM;
    k.camPos(
      snap(clampAxis(player.pos.x, mapW, k.width() / ZOOM)),
      snap(clampAxis(player.pos.y, mapH, k.height() / ZOOM)),
    );

    // Proximity triggers fire once per approach. They only update while no
    // popup is open, so one trigger can't swallow another next to it.
    if (busy()) return;

    for (const npc of npcs) {
      if (npc.isGoal) continue;
      const close = player.pos.dist(npc.pos) < 22;
      if (close && !npc.near) {
        say(allFound() && npc.data.linesAfter ? npc.data.linesAfter : npc.data.lines, npc.data.name);
      }
      npc.near = close;
      if (busy()) return;
    }

    for (const detail of details) {
      if (!detail.seen && player.pos.dist(detail.pos) < 24) {
        detail.seen = true;
        say(detail.lines);
        return;
      }
    }

    if (area.goal && !goalDone && !carried) {
      const close = goalSpots.some((spot) => player.pos.dist(spot) < 24);
      if (close && !goalNear) {
        if (boxesLeft() > 0) {
          say([`${boxesLeft()} more ${boxesLeft() === 1 ? "box" : "boxes"} to load.`]);
        } else if (allFound()) {
          runGoal();
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
  titleCard(area.chapter, area.name).then(() => {
    if (area.intro?.length) say(area.intro);
  });
});

k.scene("ending", () => {
  k.setBackground(COLORS.ink);
  k.loop(0.4, () => hearts(k.vec2(k.rand(20, k.width() - 20), k.height() - 10), 1, true));

  const center = k.vec2(k.width() / 2, k.height() / 2);
  const show = (str, size, color, y = 0) =>
    k.add([
      k.text(str, { size, width: k.width() - 40, align: "center" }),
      k.pos(center.add(0, y)),
      k.anchor("center"),
      k.color(color),
      k.opacity(0),
      k.fixed(),
    ]);
  const fadeIn = (obj, dur = 0.8) =>
    new Promise((res) => k.tween(0, 1, dur, (v) => { obj.opacity = v; }).onEnd(res));

  (async () => {
    await say(ENDING.letter);
    const intro = show(ENDING.giftIntro, 14, COLORS.paper, -40);
    await fadeIn(intro);
    await new Promise((res) => k.wait(1.2, res));
    const gift = show(ENDING.gift, 22, COLORS.accent, 10);
    await fadeIn(gift, 1.2);
    hearts(gift.pos, 30, true);
    await new Promise((res) => k.wait(1.5, res));
    await fadeIn(show(ENDING.signoff, 12, COLORS.paper, 90));
  })();
});

// Dev-only handle for poking at the game from the console / tests.
if (import.meta.env.DEV) window.k = k;

k.go("title");
