import { k } from "./kaplay.js";
import { isMuted, sfx, toggleMute, unlockAudio } from "./audio.js";

export const COLORS = {
  ink: k.Color.fromHex("#3a2e39"),
  paper: k.Color.fromHex("#fffaf4"),
  accent: k.Color.fromHex("#e56b6f"),
  muted: k.Color.fromHex("#9a8c98"),
};

// Shared "is a popup open" flag so the world knows to stop moving.
export const ui = { busy: false };

// Wait for a tap/click or space/enter, then resolve.
function onAdvance(fn) {
  const a = k.onMousePress(() => { if (!overMute()) fn(); });
  const b = k.onKeyPress(["space", "enter"], fn);
  return () => { a.cancel(); b.cancel(); };
}

// Let the tap that closed a popup finish before the world reacts to taps again.
function release(resolve) {
  k.wait(0.15, () => { ui.busy = false; resolve(); });
}

// Dialogue box at the bottom of the screen with a typewriter effect.
export function say(lines, speaker = null) {
  return new Promise((resolve) => {
    ui.busy = true;
    const W = k.width() - 16;
    const H = 108;
    const box = k.add([
      k.rect(W, H, { radius: 6 }),
      k.pos(8, k.height() - H - 8),
      k.color(COLORS.paper),
      k.outline(3, COLORS.ink),
      k.fixed(),
      k.z(100),
    ]);
    if (speaker) {
      box.add([k.text(speaker, { size: 20 }), k.pos(10, 6), k.color(COLORS.accent)]);
    }
    const body = box.add([
      k.text("", { size: 20, width: W - 20, lineSpacing: 2 }),
      k.pos(10, speaker ? 28 : 10),
      k.color(COLORS.ink),
    ]);
    const hint = box.add([
      k.text("tap", { size: 10 }),
      k.pos(W - 8, H - 5),
      k.anchor("botright"),
      k.color(COLORS.muted),
      k.opacity(0),
    ]);

    let line = 0;
    let shown = 0;
    // A blip for every other letter as it types out: lower for Nathan, higher
    // for everyone else, in between for Hannah's own thoughts.
    const pitch = speaker === "Nathan" ? 0.8 : speaker ? 1.2 : 1;
    body.onUpdate(() => {
      const full = lines[line];
      if (shown < full.length) {
        const before = Math.floor(shown);
        shown = Math.min(full.length, shown + k.dt() * 45);
        body.text = full.slice(0, Math.floor(shown));
        for (let i = before; i < Math.floor(shown); i++) if (i % 2 === 0 && full[i] !== " ") { sfx("blip", pitch * k.rand(0.97, 1.03), 0.25); break; }
      }
      hint.opacity = shown >= full.length ? 0.6 + 0.4 * Math.sin(k.time() * 5) : 0;
    });

    const stop = onAdvance(() => {
      const full = lines[line];
      if (shown < full.length) {
        shown = full.length;
        body.text = full;
        return;
      }
      line++;
      shown = 0;
      if (line >= lines.length) {
        stop();
        k.destroy(box);
        release(resolve);
      }
    });
  });
}

// Photos are shown as ordinary web images laid over the game, so they stay
// sharp at the phone's full resolution. (The game itself is drawn at 320x480
// and scaled up without smoothing, which keeps the pixel art crisp but turns
// photos blocky.) The game still draws its own copy underneath, which shows
// while the image loads. `place` returns where it goes each frame, in game
// pixels: its center, size, rotation and opacity. It goes away with `obj`.
const overlays = new Set();
export function photoOverlay(obj, src, place) {
  const img = document.createElement("img");
  img.src = src;
  img.alt = "";
  Object.assign(img.style, { position: "fixed", left: "0", top: "0", objectFit: "cover", pointerEvents: "none", zIndex: "1" });
  document.body.appendChild(img);
  overlays.add(img);
  const update = () => {
    // Where the 320x480 game sits on the page (it's letterboxed to fit).
    const r = k.canvas.getBoundingClientRect();
    const s = Math.min(r.width / k.width(), r.height / k.height());
    const ox = r.left + (r.width - k.width() * s) / 2;
    const oy = r.top + (r.height - k.height() * s) / 2;
    const { x, y, w, h, angle = 0, opacity = 1 } = place();
    img.style.width = `${w * s}px`;
    img.style.height = `${h * s}px`;
    img.style.transform = `translate(${ox + x * s}px, ${oy + y * s}px) translate(-50%, -50%) rotate(${angle}deg)`;
    img.style.opacity = String(opacity);
  };
  update();
  obj.onUpdate(update);
  obj.onDestroy(() => {
    img.remove();
    overlays.delete(img);
  });
}
k.onSceneLeave(() => {
  overlays.forEach((img) => img.remove());
  overlays.clear();
});

// Show the middle of a photo, cropped to a square, instead of squashing it.
export function squareCrop(spriteName) {
  const data = k.getSprite(spriteName)?.data;
  if (!data) return undefined;
  const { width: w, height: h } = data;
  return w > h ? k.quad((1 - h / w) / 2, 0, h / w, 1) : k.quad(0, (1 - w / h) / 2, 1, w / h);
}

// Full-screen card showing a photo and caption (notes, dinner courses...).
export function showMemory(memory, spriteName, label = "MEMORY FOUND") {
  return new Promise((resolve) => {
    ui.busy = true;
    const W = k.width() - 32;
    const H = k.height() - 64;
    const card = k.add([
      k.rect(W, H, { radius: 8 }),
      k.pos(k.width() / 2, k.height() / 2),
      k.anchor("center"),
      k.color(COLORS.paper),
      k.outline(3, COLORS.ink),
      k.fixed(),
      k.z(110),
      k.scale(0.8),
    ]);
    card.onUpdate(() => {
      card.scale = card.scale.lerp(k.vec2(1), k.dt() * 12);
    });

    const top = -H / 2 + 16;
    card.add([
      k.text(label, { size: 20 }),
      k.pos(0, top - 6),
      k.anchor("top"),
      k.color(COLORS.accent),
    ]);

    // The photo gets whatever room the words leave (up to W - 64 square), so
    // a long caption shrinks the photo instead of running off the card. If
    // it's still too long with a small photo, the caption drops a size.
    const textW = W - 24;
    const measure = (str, size) => k.make([k.text(str, { size, width: textW, align: "center", lineSpacing: 2 })]).height;
    const titleH = measure(memory.title, 30);
    const photoY = top + 18;
    const room = (size) => H / 2 - 14 - (photoY + 8 + titleH + 4 + measure(memory.caption, size));
    const captionSize = room(20) >= 120 ? 20 : 10;
    const photoW = Math.floor(Math.min(W - 64, room(captionSize)));
    const photoH = photoW;
    if (spriteName) {
      card.add([k.rect(photoW, photoH), k.pos(0, photoY), k.anchor("top"), k.color(COLORS.muted)]);
      const photo = card.add([k.sprite(spriteName, { width: photoW, height: photoH, quad: squareCrop(spriteName) }), k.pos(0, photoY), k.anchor("top")]);
      photoOverlay(photo, spriteName, () => ({
        x: card.pos.x,
        y: card.pos.y + (photoY + photoH / 2) * card.scale.y,
        w: photoW * card.scale.x,
        h: photoH * card.scale.y,
      }));
    } else {
      card.add([k.rect(photoW, photoH), k.pos(0, photoY), k.anchor("top"), k.color(COLORS.muted)]);
      card.add([
        k.text("photo goes here", { size: 20 }),
        k.pos(0, photoY + photoH / 2),
        k.anchor("center"),
        k.color(COLORS.paper),
      ]);
    }

    const title = card.add([
      k.text(memory.title, { size: 30, width: textW, align: "center", lineSpacing: 2 }),
      k.pos(0, photoY + photoH + 8),
      k.anchor("top"),
      k.color(COLORS.ink),
    ]);
    card.add([
      k.text(memory.caption, { size: captionSize, width: textW, align: "center", lineSpacing: 2 }),
      k.pos(0, title.pos.y + title.height + 4),
      k.anchor("top"),
      k.color(COLORS.ink),
    ]);

    // Ignore taps for a moment so she doesn't skip it by accident.
    k.wait(0.4, () => {
      const stop = onAdvance(() => {
        stop();
        k.destroy(card);
        release(resolve);
      });
    });
  });
}

// Little hearts that float up and fade out.
export function hearts(pos, count = 6, fixed = false, z = 50) {
  for (let i = 0; i < count; i++) {
    k.add([
      k.text("♥", { size: k.rand(8, 16), font: "monospace" }),
      k.pos(pos.add(k.rand(-12, 12), k.rand(-6, 6))),
      k.anchor("center"),
      k.color(COLORS.accent),
      k.move(k.vec2(k.rand(-0.4, 0.4), -1), k.rand(30, 60)),
      k.opacity(1),
      k.lifespan(k.rand(0.6, 1.2), { fade: 0.4 }),
      k.z(z),
      ...(fixed ? [k.fixed()] : []),
    ]);
  }
}

// Centered chapter title that fades in and out.
export function titleCard(chapter, name) {
  return new Promise((resolve) => {
    ui.busy = true;
    const bg = k.add([k.rect(k.width(), k.height()), k.color(COLORS.ink), k.opacity(1), k.fixed(), k.z(200)]);
    const a = k.add([
      k.text(chapter, { size: 20 }),
      k.pos(k.width() / 2, k.height() / 2 - 18),
      k.anchor("center"),
      k.color(COLORS.accent),
      k.opacity(1),
      k.fixed(),
      k.z(201),
    ]);
    const b = k.add([
      k.text(name, { size: 30, width: k.width() - 40, align: "center" }),
      k.pos(k.width() / 2, k.height() / 2 + 2),
      k.anchor("top"),
      k.color(COLORS.paper),
      k.opacity(1),
      k.fixed(),
      k.z(201),
    ]);
    k.wait(1.8, () => {
      k.tween(1, 0, 0.6, (v) => { bg.opacity = v; a.opacity = v; b.opacity = v; }).onEnd(() => {
        k.destroy(bg); k.destroy(a); k.destroy(b);
        ui.busy = false;
        resolve();
      });
    });
  });
}

// Fade the screen to black (before moving on to the next scene).
export function fadeOut(dur = 0.9) {
  ui.busy = true;
  const bg = k.add([k.rect(k.width(), k.height()), k.color(COLORS.ink), k.opacity(0), k.fixed(), k.z(300)]);
  return new Promise((resolve) => k.tween(0, 1, dur, (v) => { bg.opacity = v; }).onEnd(resolve));
}

// The final gift: a ticket that pops up over a dimmed screen, with a stub.
export function showTicket(ticket) {
  return new Promise((resolve) => {
    ui.busy = true;
    const mid = k.vec2(k.width() / 2, k.height() / 2);
    const dim = k.add([k.rect(k.width(), k.height()), k.color(COLORS.ink), k.opacity(0.75), k.fixed(), k.z(105)]);
    const heading = k.add([
      k.text(ticket.label, { size: 20 }),
      k.pos(mid.add(0, -120)),
      k.anchor("center"),
      k.color(COLORS.accent),
      k.fixed(),
      k.z(110),
    ]);

    const W = k.width() - 24;
    const H = 150;
    const stubW = 74;
    const card = k.add([
      k.rect(W, H, { radius: 6 }),
      k.pos(mid.add(0, -10)),
      k.anchor("center"),
      k.color(COLORS.paper),
      k.outline(3, COLORS.ink),
      k.rotate(-3),
      k.scale(0.3),
      k.fixed(),
      k.z(110),
    ]);
    card.onUpdate(() => { card.scale = card.scale.lerp(k.vec2(1), k.dt() * 10); });
    const left = -W / 2;
    const mainMid = left + (W - stubW) / 2;
    // The band across the top of the ticket.
    card.add([k.rect(W - stubW - 6, 26, { radius: 4 }), k.pos(left + 4, -H / 2 + 4), k.color(COLORS.accent)]);
    card.add([k.text(ticket.admit, { size: 20 }), k.pos(mainMid, -H / 2 + 17), k.anchor("center"), k.color(COLORS.paper)]);
    card.add([k.text(ticket.venue, { size: 30 }), k.pos(mainMid, -16), k.anchor("center"), k.color(COLORS.ink)]);
    card.add([k.text(ticket.detail, { size: 20 }), k.pos(mainMid, 12), k.anchor("center"), k.color(COLORS.muted)]);
    card.add([k.text(ticket.date, { size: 20, width: W - stubW - 20, align: "center" }), k.pos(mainMid, 44), k.anchor("center"), k.color(COLORS.accent)]);
    // Perforation, then the stub.
    const tear = W / 2 - stubW;
    for (let y = -H / 2 + 8; y < H / 2 - 8; y += 8) card.add([k.rect(2, 4), k.pos(tear, y), k.color(COLORS.muted)]);
    const stubMid = tear + stubW / 2;
    card.add([k.text("♥", { size: 22, font: "monospace" }), k.pos(stubMid, -30), k.anchor("center"), k.color(COLORS.accent)]);
    card.add([k.text(ticket.stub, { size: 20, width: stubW - 8, align: "center", lineSpacing: 2 }), k.pos(stubMid, 18), k.anchor("center"), k.color(COLORS.ink)]);

    const caption = k.add([
      k.text(ticket.caption, { size: 20, width: k.width() - 48, align: "center", lineSpacing: 2 }),
      k.pos(mid.add(0, 90)),
      k.anchor("top"),
      k.color(COLORS.paper),
      k.opacity(0),
      k.fixed(),
      k.z(110),
    ]);
    k.tween(0, 1, 1, (v) => { caption.opacity = v; });
    hearts(mid.add(0, -10), 30, true, 120);
    sfx("ticket");
    const burst = k.loop(0.5, () => hearts(mid.add(k.rand(-120, 120), k.rand(-70, 50)), 2, true, 106));

    // Ignore taps for a moment so she gets to take it in.
    k.wait(1.2, () => {
      const stop = onAdvance(() => {
        stop();
        burst.cancel();
        [dim, heading, card, caption].forEach((obj) => k.destroy(obj));
        release(resolve);
      });
    });
  });
}

// Speaker icons for the mute button, one character per pixel.
const SPEAKER = {
  on: [
    ".....#......",
    "....##..#...",
    "...###...#..",
    "######.#.#..",
    "######.#.#..",
    "######.#.#..",
    "...###...#..",
    "....##..#...",
    ".....#......",
  ],
  off: [
    ".....#......",
    "....##......",
    "...###.#...#",
    "######..#.#.",
    "######...#..",
    "######..#.#.",
    "...###.#...#",
    "....##......",
    ".....#......",
  ],
};
for (const [name, rows] of Object.entries(SPEAKER)) {
  const canvas = document.createElement("canvas");
  canvas.width = rows[0].length;
  canvas.height = rows.length;
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = `rgb(${COLORS.ink.r}, ${COLORS.ink.g}, ${COLORS.ink.b})`;
  rows.forEach((row, y) => [...row].forEach((ch, x) => { if (ch === "#") ctx.fillRect(x, y, 1, 1); }));
  k.loadSprite(`speaker-${name}`, canvas);
}

// The mute button in the top right corner. Returns it so a scene can ignore
// taps on it (they shouldn't also walk her there).
let mute = null;
// Is this tap on the mute button (and so not meant for anything else)?
export const overMute = () => Boolean(mute?.exists() && mute.isHovering());

export function muteButton() {
  const look = () => `speaker-${isMuted() ? "off" : "on"}`;
  const button = k.add([
    k.rect(32, 24, { radius: 4 }),
    k.pos(k.width() - 36, 4),
    k.color(COLORS.paper),
    k.opacity(0.9),
    k.area(),
    k.fixed(),
    k.z(95),
  ]);
  let icon = null;
  const draw = () => {
    if (icon) k.destroy(icon);
    icon = button.add([k.sprite(look()), k.pos(4, 3), k.scale(2)]);
  };
  draw();
  button.onClick(() => {
    unlockAudio();
    toggleMute();
    draw();
    sfx("click");
  });
  mute = button;
  return button;
}
