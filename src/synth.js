// A tiny synthesizer. It turns the songs in music.js (chords plus a melody
// written as text) and the game's sound effects into audio, right in the
// browser: the game ships no audio files, and every song loops without a gap.
// No browser APIs in here, so it also runs in Node for checking the songs.

export const RATE = 22050;
const TAU = Math.PI * 2;

// ---- Notes and chords ------------------------------------------------------

const LETTERS = { C: 0, D: 2, E: 4, F: 5, G: 7, A: 9, B: 11 };

// "C#5" -> its MIDI number (A4 = 69), or null if it isn't a note.
export function midi(name) {
  const m = /^([A-G])([#b]?)(\d)$/.exec(name);
  if (!m) return null;
  return 12 * (Number(m[3]) + 1) + LETTERS[m[1]] + (m[2] === "#" ? 1 : m[2] === "b" ? -1 : 0);
}
const pitchClass = (name) => (LETTERS[name[0]] + (name[1] === "#" ? 1 : name[1] === "b" ? -1 : 0) + 12) % 12;
const hz = (n) => 440 * 2 ** ((n - 69) / 12);

// Semitones above the root for each kind of chord.
const QUALITIES = {
  "": [0, 4, 7], m: [0, 3, 7], 7: [0, 4, 7, 10], maj7: [0, 4, 7, 11], m7: [0, 3, 7, 10],
  6: [0, 4, 7, 9], m6: [0, 3, 7, 9], 9: [0, 4, 7, 10, 14], maj9: [0, 4, 7, 11, 14], m9: [0, 3, 7, 10, 14],
  "7b9": [0, 4, 7, 10, 13], sus2: [0, 2, 7], sus4: [0, 5, 7], dim: [0, 3, 6], dim7: [0, 3, 6, 9],
  m7b5: [0, 3, 6, 10], aug: [0, 4, 8],
};

// "Am7", "C/E", "Bb" -> { root, bass, intervals }, or null if it isn't a chord.
export function chord(name) {
  const m = /^([A-G][#b]?)(maj9|maj7|m7b5|m9|m7|m6|dim7|dim|aug|sus2|sus4|7b9|9|7|6|m)?(?:\/([A-G][#b]?))?$/.exec(name);
  if (!m) return null;
  const root = pitchClass(m[1]);
  return { root, bass: m[3] ? pitchClass(m[3]) : root, intervals: QUALITIES[m[2] ?? ""] };
}
// The chord's notes stacked up from its root in `octave`.
const stack = (ch, octave) => ch.intervals.map((i) => 12 * (octave + 1) + ch.root + i);

// ---- Sounds ----------------------------------------------------------------

// A little pseudo-random generator, so noise (drums) sounds the same every time.
function rng(seed) {
  return () => {
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Smooths the corners of a square wave so it doesn't buzz (PolyBLEP).
function blep(t, dt) {
  if (t < dt) { t /= dt; return t + t - t * t - 1; }
  if (t > 1 - dt) { t = (t - 1) / dt; return t * t + t + t + 1; }
  return 0;
}
const square = (duty) => (p, dt) => (p < duty ? 1 : -1) + blep(p, dt) - blep((p - duty + 1) % 1, dt);
const triangle = (p) => 4 * Math.abs(p - 0.5) - 1;

// Instruments. `wave(phase, phaseStep, time)` is one cycle of the sound;
// the envelope: `attack`, then either `decay` (dies away, like a piano) or
// `sustain` (holds, like an organ), then `release` after the note ends.
// `voices` layers slightly detuned copies, `vibrato` wobbles held notes, and
// `lowpass` (0-1, smaller is darker) softens the tone.
export const INSTRUMENTS = {
  // Music box.
  bell: { gain: 0.5, attack: 0.003, decay: 2.2, release: 0.9,
    wave: (p, dt, t) => Math.sin(TAU * p) + 0.3 * Math.exp(-t * 7) * Math.sin(TAU * 3 * p) + 0.12 * Math.exp(-t * 14) * Math.sin(TAU * 6 * p) },
  // Electric piano (a little FM for the bark on each note).
  epiano: { gain: 0.45, attack: 0.004, decay: 1.4, release: 0.25,
    wave: (p, dt, t) => Math.sin(TAU * p + 1.3 * Math.exp(-t * 4) * Math.sin(TAU * p)) },
  // Plucked string: koto, guitar.
  pluck: { gain: 0.5, attack: 0.002, decay: 2.6, release: 0.2,
    wave: (p, dt, t) => Math.sin(TAU * p) + 0.5 * Math.exp(-t * 9) * Math.sin(TAU * 2 * p) + 0.3 * Math.exp(-t * 14) * Math.sin(TAU * 3 * p) + 0.18 * Math.exp(-t * 20) * Math.sin(TAU * 4 * p) },
  // Chiptune leads.
  lead: { gain: 0.16, attack: 0.01, sustain: 0.7, sustainAfter: 0.12, release: 0.06, vibrato: 0.004, lowpass: 0.35, wave: square(0.25) },
  chip: { gain: 0.14, attack: 0.004, sustain: 0.5, sustainAfter: 0.08, release: 0.04, wave: square(0.125) },
  // A breathy, reedy lead for the jazz band's sax.
  sax: { gain: 0.26, attack: 0.04, sustain: 0.8, sustainAfter: 0.2, release: 0.09, vibrato: 0.006, lowpass: 0.16, wave: square(0.42) },
  // Soft chords that swell in and hang in the air.
  pad: { gain: 0.1, attack: 0.35, sustain: 1, release: 0.6, voices: [0.996, 1.004], lowpass: 0.3, wave: triangle },
  // Basses.
  bass: { gain: 0.42, attack: 0.005, sustain: 0.75, sustainAfter: 0.15, release: 0.05, wave: triangle },
  upright: { gain: 0.6, attack: 0.006, decay: 2.4, release: 0.07,
    wave: (p, dt, t) => Math.sin(TAU * p) + 0.45 * Math.exp(-t * 8) * Math.sin(TAU * 2 * p) + 0.2 * Math.exp(-t * 12) * Math.sin(TAU * 3 * p) },
};

// Drums, made from noise and falling tones.
const DRUMS = {
  kick: { length: 0.3, sound: (t, noise, st) => { st.p = (st.p ?? 0) + (45 + 70 * Math.exp(-t * 30)) / RATE; return Math.sin(TAU * st.p) * Math.exp(-t * 16); } },
  snare: { length: 0.25, sound: (t, noise, st) => { const n = noise(); const hp = n - (st.lp = (st.lp ?? 0) + 0.3 * (n - (st.lp ?? 0))); return 0.8 * hp * Math.exp(-t * 20) + 0.4 * Math.sin(TAU * 185 * t) * Math.exp(-t * 28); } },
  hat: { length: 0.07, sound: (t, noise, st) => { const n = noise(); const hp = n - (st.lp = (st.lp ?? 0) + 0.5 * (n - (st.lp ?? 0))); return 0.45 * hp * Math.exp(-t * 65); } },
  ride: { length: 0.9, sound: (t, noise, st) => {
    const n = noise(); const hp = n - (st.lp = (st.lp ?? 0) + 0.45 * (n - (st.lp ?? 0)));
    const ping = Math.sin(TAU * 523 * t) + Math.sin(TAU * 797 * t) + Math.sin(TAU * 1213 * t);
    return (0.3 * hp + 0.06 * ping) * Math.exp(-t * 5.5);
  } },
  brush: { length: 0.22, sound: (t, noise, st) => { const n = noise(); st.lp = (st.lp ?? 0) + 0.25 * (n - (st.lp ?? 0)); return 0.5 * st.lp * Math.exp(-t * 14) * Math.min(1, t * 60); } },
  block: { length: 0.12, sound: (t) => (Math.sin(TAU * 880 * t) + 0.4 * Math.sin(TAU * 1760 * t)) * Math.exp(-t * 45) },
};

// Adds one note of an instrument into `buf`, starting at sample `at`.
function addNote(buf, at, freq, dur, vel, inst) {
  const { attack = 0.005, decay, sustain = 1, sustainAfter = 0.1, release, voices = [1], vibrato, lowpass, wave, gain } = inst;
  const length = Math.min(Math.floor((dur + release) * RATE), buf.length - at);
  for (const detune of voices) {
    let phase = 0;
    let low = 0;
    for (let i = 0; i < length; i++) {
      const t = i / RATE;
      let f = freq * detune;
      if (vibrato && t > 0.18) f *= 1 + vibrato * Math.sin(TAU * 5.2 * t) * Math.min(1, (t - 0.18) * 4);
      const dt = f / RATE;
      let env = t < attack ? t / attack : 1;
      if (decay) env *= Math.exp(-(t - attack) * decay * (t > attack ? 1 : 0));
      else if (t > attack) env *= t < attack + sustainAfter ? 1 - ((1 - sustain) * (t - attack)) / sustainAfter : sustain;
      if (t > dur) env *= Math.max(0, 1 - (t - dur) / release);
      let x = wave(phase, dt, t) * env;
      if (lowpass) x = low += lowpass * (x - low);
      buf[at + i] += (x * vel * gain) / voices.length;
      phase += dt;
      if (phase >= 1) phase -= 1;
    }
  }
}

function addDrum(buf, at, name, vel, noise) {
  const drum = DRUMS[name];
  const length = Math.min(Math.floor(drum.length * RATE), buf.length - at);
  const state = {};
  for (let i = 0; i < length; i++) buf[at + i] += drum.sound(i / RATE, () => noise() * 2 - 1, state) * vel * 0.5;
}

// ---- Songs -----------------------------------------------------------------

// How each accompaniment part plays a chord. `seg` is one chord's stretch of
// a bar: its first step and how many steps it lasts. Each returns notes as
// [step, length in steps, MIDI note].
const STYLES = {
  // Root on the downbeat, the fifth halfway through.
  bass: (ch, seg, o) => {
    const root = 12 * (o + 1) + ch.bass;
    if (seg.len < 4) return [[seg.at, seg.len, root]];
    return [[seg.at, seg.len / 2, root], [seg.at + seg.len / 2, seg.len / 2, root + (ch.bass === ch.root ? 7 : 0)]];
  },
  // A walking bass line, one note a beat, stepping into the next chord.
  walk: (ch, seg, o, { beat, next }) => {
    const root = 12 * (o + 1) + ch.root;
    const third = root + ch.intervals[1];
    const fifth = root + ch.intervals[2];
    const into = next ? 12 * (o + 1) + next.root : root;
    const approach = into + (into > root ? -1 : 1);
    const line = seg.len / beat >= 4 ? [root, third, fifth, approach] : [root, approach];
    return line.map((n, i) => [seg.at + i * beat, beat * 0.9, n]);
  },
  // Chords held for as long as they last.
  pad: (ch, seg, o) => stack(ch, o).slice(0, 4).map((n) => [seg.at, seg.len, n]),
  // The chord's notes one at a time, up and back down.
  arp: (ch, seg, o) => {
    const notes = stack(ch, o).slice(0, 4);
    const pattern = [...notes, notes[0] + 12, ...notes.slice(1).reverse()];
    return Array.from({ length: seg.len }, (_, i) => [seg.at + i, 1, pattern[i % pattern.length]]);
  },
  // Waltz: bass on one (in `octave`), the chord two octaves up on two and three.
  waltz: (ch, seg, o) => [[seg.at, 2, 12 * (o + 1) + ch.bass], ...[2, 4].flatMap((s) => stack(ch, o + 2).slice(0, 3).map((n) => [seg.at + s, 1.5, n]))],
  // Oom-pah: bass on the beat (in `octave`), the chord two octaves up in between.
  oompah: (ch, seg, o, { beat }) => Array.from({ length: seg.len / beat }, (_, i) =>
    i % 2 === 0
      ? [[seg.at + i * beat, beat * 0.8, 12 * (o + 1) + ch.bass + (i % 4 === 2 && ch.bass === ch.root ? 7 : 0)]]
      : stack(ch, o + 2).slice(0, 3).map((n) => [seg.at + i * beat, beat * 0.5, n])).flat(),
  // Chords on beats two and four.
  backbeat: (ch, seg, o, { beat }) => Array.from({ length: seg.len / beat }, (_, i) => i).filter((i) => i % 2 === 1)
    .flatMap((i) => stack(ch, o).slice(0, 4).map((n) => [seg.at + i * beat, beat * 0.6, n])),
  // Jazz piano: short chords on the downbeat and just before beat three
  // (the "Charleston"), leaving out the root for the bass to play.
  comp: (ch, seg, o, { beat }) => {
    const notes = stack(ch, o).slice(ch.intervals.length > 3 ? 1 : 0, 5);
    const hits = seg.len / beat >= 4 ? [[0, 1.5], [3, 1]] : [[0, 1.2]];
    return hits.flatMap(([s, len]) => notes.map((n) => [seg.at + s, len, n]));
  },
};

// Splits "F | C/E | Am7 D7 |" into bars of chords.
const bars = (text) => text.split("|").map((bar) => bar.trim()).filter(Boolean).map((bar) => bar.split(/\s+/));
// Splits a melody into bars of steps.
const melodyBars = (text) => text.split("|").map((bar) => bar.trim().split(/\s+/).filter(Boolean)).filter((bar) => bar.length);

// Everything that's wrong with a song, as readable messages (see music.js).
export function checkSong(name, song) {
  const problems = [];
  const steps = song.steps ?? (song.beats ?? 4) * 2;
  const chords = bars(song.chords);
  chords.flat().forEach((c) => { if (!chord(c)) problems.push(`${name}: "${c}" isn't a chord I know`); });
  chords.forEach((bar, b) => { if (steps % bar.length) problems.push(`${name}: bar ${b + 1} splits ${steps} steps between ${bar.length} chords`); });
  for (const line of [song.melody, ...(song.parts ?? [])].filter((part) => part?.notes)) {
    const tune = melodyBars(line.notes);
    if (tune.length !== chords.length) problems.push(`${name}: the melody is ${tune.length} bars long, the chords are ${chords.length}`);
    tune.forEach((bar, b) => {
      if (bar.length !== steps) problems.push(`${name}: melody bar ${b + 1} has ${bar.length} steps, expected ${steps}`);
      bar.forEach((token) => { if (token !== "-" && token !== "." && midi(token) === null) problems.push(`${name}: "${token}" in melody bar ${b + 1} isn't a note`); });
    });
  }
  for (const part of song.parts ?? []) {
    if (part.style && !STYLES[part.style]) problems.push(`${name}: no part style called "${part.style}"`);
    if (part.inst && !INSTRUMENTS[part.inst]) problems.push(`${name}: no instrument called "${part.inst}"`);
  }
  if (song.melody && !INSTRUMENTS[song.melody.inst]) problems.push(`${name}: no instrument called "${song.melody.inst}"`);
  return problems;
}

// Every note of a song as { step, len, note, inst, vol } (drums as { step, drum, vol }).
export function score(song) {
  const beats = song.beats ?? 4;
  const steps = song.steps ?? beats * 2;
  const beat = steps / beats;
  const chords = bars(song.chords).map((bar) => bar.map(chord));
  const events = [];
  const tune = (line, inst, vol, octaveShift = 0) => {
    let held = null;
    melodyBars(line).flat().forEach((token, step) => {
      if (token === "-") { if (held) held.len++; return; }
      held = null;
      const n = midi(token);
      if (n !== null) events.push((held = { step, len: 1, note: n + 12 * octaveShift, inst, vol }));
    });
  };
  if (song.melody) tune(song.melody.notes, song.melody.inst, song.melody.vol ?? 1);
  const flatChords = chords.flatMap((bar, b) => bar.map((ch, i) => ({ ch, b, i, n: bar.length })));
  for (const part of song.parts ?? []) {
    if (part.notes) { tune(part.notes, part.inst, part.vol ?? 1); continue; }
    if (part.drums) {
      for (let b = 0; b < chords.length; b++) {
        for (const [drum, pattern] of Object.entries(part.drums)) {
          [...pattern].forEach((hit, s) => {
            if (hit === "x" || hit === "o") events.push({ step: b * steps + s, drum, vol: (part.vol ?? 1) * (hit === "x" ? 1 : 0.45) });
          });
        }
      }
      continue;
    }
    flatChords.forEach(({ ch, b, i, n }, k) => {
      const seg = { at: b * steps + (i * steps) / n, len: steps / n };
      const next = flatChords[(k + 1) % flatChords.length].ch;
      for (const [step, len, note] of STYLES[part.style](ch, seg, part.octave ?? 3, { beat, next })) {
        events.push({ step, len, note, inst: part.inst, vol: part.vol ?? 1 });
      }
    });
  }
  return { events, steps, totalSteps: chords.length * steps, beat };
}

// Renders a song to samples that loop seamlessly.
export function renderSong(song) {
  const beats = song.beats ?? 4;
  const { events, steps, totalSteps } = score(song);
  const barDur = (60 / song.bpm) * beats;
  const stepDur = barDur / steps;
  const swing = song.swing ?? 0.5;
  // Swing delays every other step: the off-beat lands `swing` of the way
  // through each pair of steps instead of halfway.
  const time = (step) => {
    const whole = Math.floor(step);
    const bar = Math.floor(whole / steps);
    const s = whole % steps;
    const pair = Math.floor(s / 2);
    const offbeat = s % 2 ? 2 * stepDur * swing : 0;
    return bar * barDur + pair * 2 * stepDur + offbeat + (step - whole) * stepDur;
  };
  const loop = Math.round((totalSteps / steps) * barDur * RATE);
  const tail = 2 * RATE;
  const buf = new Float32Array(loop + tail);
  const noise = rng(7);
  for (const e of events) {
    const at = Math.round(time(e.step) * RATE);
    if (e.drum) addDrum(buf, at, e.drum, e.vol, noise);
    else addNote(buf, at, hz(e.note), time(e.step + e.len) - time(e.step), e.vol, INSTRUMENTS[e.inst]);
  }
  // Whatever rings past the end of the loop wraps around to its start.
  for (let i = 0; i < tail; i++) buf[i] += buf[loop + i];
  return finish(buf.subarray(0, loop), { rms: 0.17 });
}

// Evens out the volume: songs to the same average loudness (`rms`), sound
// effects to the same peak, rounding off anything too loud.
function finish(samples, { rms, peak: top = 0.7 } = {}) {
  let peak = 0;
  let sum = 0;
  for (const s of samples) { peak = Math.max(peak, Math.abs(s)); sum += s * s; }
  if (!peak) return new Float32Array(samples.length);
  const scale = rms ? rms / Math.sqrt(sum / samples.length) : top / peak;
  const out = new Float32Array(samples.length);
  for (let i = 0; i < samples.length; i++) out[i] = 0.9 * Math.tanh(samples[i] * scale / 0.9);
  return out;
}

// ---- Sound effects ---------------------------------------------------------

// Each is a few notes: [delay in seconds, note or drum, length, instrument, volume].
const EFFECTS = {
  // Typewriter blip for dialogue (played faster or slower per speaker).
  blip: [[0, "A5", 0.025, "chip", 0.5]],
  // Picking up a note.
  note: [[0, "C6", 0.2, "bell"], [0.07, "E6", 0.2, "bell"], [0.14, "G6", 0.2, "bell"], [0.21, "C7", 0.5, "bell"]],
  // A door opening (the chapter's done).
  open: [[0, "G5", 0.1, "pluck"], [0.06, "C6", 0.1, "pluck"], [0.12, "E6", 0.1, "pluck"], [0.18, "G6", 0.4, "bell", 0.7]],
  // Picking up a box, and loading it into the truck.
  box: [[0, "kick", 0, "", 0.9], [0, "brush", 0, "", 0.6]],
  load: [[0, "kick", 0, "", 1], [0.02, "snare", 0, "", 0.35], [0.08, "E6", 0.15, "bell", 0.5], [0.14, "G6", 0.3, "bell", 0.5]],
  // She spots Nathan.
  alert: [[0, "E6", 0.06, "chip", 0.8], [0.08, "B6", 0.12, "chip", 0.8]],
  // A button press.
  click: [[0, "block", 0, "", 0.6]],
  // The ticket.
  ticket: [[0, "C5", 1.4, "bell"], [0.08, "E5", 1.3, "bell"], [0.16, "G5", 1.2, "bell"], [0.24, "C6", 1.1, "bell"], [0.32, "E6", 1.0, "bell"], [0.4, "G6", 1.2, "bell"], [0, "C4", 1.6, "pad", 3]],
};

export function renderEffect(name) {
  const notes = EFFECTS[name];
  const length = Math.max(...notes.map(([at, , len, inst]) => at + len + (INSTRUMENTS[inst]?.release ?? 0.9))) + 0.05;
  const buf = new Float32Array(Math.ceil(length * RATE));
  const noise = rng(3);
  for (const [at, what, len, inst, vol = 1] of notes) {
    const start = Math.round(at * RATE);
    if (DRUMS[what]) addDrum(buf, start, what, vol, noise);
    else addNote(buf, start, hz(midi(what)), len, vol, INSTRUMENTS[inst]);
  }
  return finish(buf);
}

export const EFFECT_NAMES = Object.keys(EFFECTS);
