import { k } from "./kaplay.js";

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
  const a = k.onMousePress(fn);
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
    body.onUpdate(() => {
      const full = lines[line];
      if (shown < full.length) {
        shown = Math.min(full.length, shown + k.dt() * 45);
        body.text = full.slice(0, Math.floor(shown));
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

// Full-screen card showing a photo and caption (notes, dinner courses...).
export function showMemory(memory, spriteName, label = "MEMORY FOUND") {
  return new Promise((resolve) => {
    ui.busy = true;
    const W = k.width() - 32;
    const H = k.height() - 96;
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

    const photoW = W - 64;
    const photoH = photoW;
    const photoY = top + 18;
    if (spriteName) {
      card.add([k.sprite(spriteName, { width: photoW, height: photoH }), k.pos(0, photoY), k.anchor("top")]);
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
      k.text(memory.title, { size: 30, width: W - 24, align: "center" }),
      k.pos(0, photoY + photoH + 8),
      k.anchor("top"),
      k.color(COLORS.ink),
    ]);
    card.add([
      k.text(memory.caption, { size: 20, width: W - 24, align: "center", lineSpacing: 2 }),
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
