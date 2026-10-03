// Music and sound effects. Songs come from src/music.js (rendered in a
// worker by src/synth.js) or, if a chapter's `music` is a path, from a real
// audio file in public/.
import { checkSong, EFFECT_NAMES, RATE } from "./synth.js";
import { SONGS } from "./music.js";

const FADE = 1.2;
const MUTE_KEY = "year-two-muted";

// Catch mistakes in the songs early, like the map checks in main.js.
Object.entries(SONGS).forEach(([name, song]) => checkSong(name, song).forEach((problem) => console.warn(problem)));

const effects = new Map();
let ctx = null;
let master = null;
let musicBus = null;
let sfxBus = null;
let muted = false;
try {
  muted = localStorage.getItem(MUTE_KEY) === "1";
} catch {
  // No storage (private browsing): start unmuted.
}

function setup() {
  if (ctx) return;
  ctx = new (window.AudioContext || window.webkitAudioContext)();
  master = ctx.createGain();
  master.gain.value = muted ? 0 : 1;
  master.connect(ctx.destination);
  musicBus = ctx.createGain();
  musicBus.gain.value = 0.55;
  musicBus.connect(master);
  sfxBus = ctx.createGain();
  sfxBus.gain.value = 0.6;
  sfxBus.connect(master);
  // Sound effects are small: render them all up front.
  for (const name of EFFECT_NAMES) effects.set(name, render({ effect: name }).then(toBuffer));
  // Go quiet while the phone is locked or she's in another app.
  document.addEventListener("visibilitychange", () => {
    if (unlocked) document.hidden ? ctx.suspend() : ctx.resume();
  });
}

// Browsers only allow sound after a tap, so the first tap on the title
// screen calls this.
let unlocked = false;
export function unlockAudio() {
  setup();
  unlocked = true;
  // Keep playing when an iPhone's silent switch is on, like a video would.
  try {
    if (navigator.audioSession) navigator.audioSession.type = "playback";
  } catch {
    // Older Safari: the silent switch mutes the game.
  }
  ctx.resume();
}

// The synthesizer runs in a worker; each request gets its samples back.
const worker = new Worker(new URL("./musicWorker.js", import.meta.url), { type: "module" });
const waiting = new Map();
let nextId = 0;
worker.onmessage = ({ data: { id, samples } }) => {
  waiting.get(id)(samples);
  waiting.delete(id);
};
const render = (request) =>
  new Promise((resolve) => {
    waiting.set(nextId, resolve);
    worker.postMessage({ id: nextId++, ...request });
  });
const toBuffer = (samples) => {
  const buffer = ctx.createBuffer(1, samples.length, RATE);
  buffer.copyToChannel(samples, 0);
  return buffer;
};

// Songs are kept around once rendered, but only the last few (they're big).
const songs = new Map();
function song(key) {
  if (!songs.has(key)) {
    const loading = SONGS[key]
      ? render({ song: key }).then(toBuffer)
      : fetch(key).then((res) => res.arrayBuffer()).then((data) => ctx.decodeAudioData(data));
    songs.set(key, loading.catch((err) => { console.warn(`Couldn't load music "${key}"`, err); return null; }));
    while (songs.size > 3) songs.delete([...songs.keys()].find((k) => k !== key && k !== wanted));
  }
  return songs.get(key);
}

// Get a song ready ahead of time (the next chapter's), so it starts right away.
export function preloadMusic(key) {
  setup();
  if (key) song(key);
}

// Crossfade to a song (or to silence with null). Asking for the song that's
// already playing keeps it going.
let wanted;
let current = null;
export async function playMusic(key) {
  setup();
  if (key === wanted) return;
  wanted = key;
  const buffer = key ? await song(key) : null;
  if (wanted !== key) return;
  const now = ctx.currentTime;
  if (current) {
    const { source, gain } = current;
    gain.gain.cancelScheduledValues(now);
    gain.gain.setValueAtTime(gain.gain.value, now);
    gain.gain.linearRampToValueAtTime(0, now + FADE);
    source.stop(now + FADE + 0.1);
    current = null;
  }
  if (!buffer) return;
  const gain = ctx.createGain();
  gain.gain.setValueAtTime(0, now);
  gain.gain.linearRampToValueAtTime(1, now + FADE);
  gain.connect(musicBus);
  const source = ctx.createBufferSource();
  source.buffer = buffer;
  source.loop = true;
  source.connect(gain);
  source.start(now);
  current = { source, gain };
}

// Play a sound effect. `rate` speeds it up (higher) or slows it down (lower).
export async function sfx(name, rate = 1, volume = 1) {
  if (!unlocked || muted || ctx.state !== "running") return;
  const buffer = await effects.get(name);
  if (!buffer) return;
  const source = ctx.createBufferSource();
  source.buffer = buffer;
  source.playbackRate.value = rate;
  const gain = ctx.createGain();
  gain.gain.value = volume;
  source.connect(gain).connect(sfxBus);
  source.start();
}

export const isMuted = () => muted;
export function toggleMute() {
  setup();
  muted = !muted;
  master.gain.setTargetAtTime(muted ? 0 : 1, ctx.currentTime, 0.05);
  try {
    localStorage.setItem(MUTE_KEY, muted ? "1" : "0");
  } catch {
    // It just won't be remembered.
  }
  return muted;
}
