// The game's music, written out as text and played by src/synth.js.
//
// Each song has:
//   bpm      tempo            beats  beats per bar (4, or 3 for a waltz)
//   steps    steps per bar (default: two per beat, so each step is an eighth note)
//   swing    where the off-beat lands in each pair of steps: 0.5 is straight,
//            about 0.64 swings like jazz
//   chords   one bar per "|", e.g. "F | C/E | Am7 D7 |" (two chords split the bar)
//   melody   { inst, notes, vol }: one token per step, bars split by "|" like
//            the chords. A note ("C5", "F#4", "Bb3") starts a note, "-" holds
//            it, "." is silence. Every bar needs exactly `steps` tokens.
//   parts    the band, played from the chords: { style, inst, octave, vol }.
//            Styles (src/synth.js): bass, walk (walking bass), pad, arp,
//            waltz, oompah, backbeat, comp (jazz piano).
//            Drums: { drums: { kick: "x...x...", hat: ".o.o.o.o" }, vol } with
//            one character per step: x hit, o soft hit, . nothing. Drums:
//            kick, snare, hat, ride, brush, block (woodblock).
//            A part can also have its own `notes`, like a second melody.
// Instruments: bell (music box), epiano, pluck (koto/guitar), lead, chip,
// sax, pad, bass, upright.
//
// A chapter picks its song with `music` in content.js. That can also be a
// path to a real audio file instead ("/music/something.mp3" in public/music).
// Mistakes (wrong number of steps, a typo in a chord) show up as warnings in
// the browser console.

export const SONGS = {
  // The title screen, the letter, and the very end. A music box.
  title: {
    bpm: 76,
    chords: "F | C/E | Dm | Bb | F | C | Bb | C | Dm | Bb | F | C | Bb | C | F | F",
    melody: {
      inst: "bell",
      notes: `C5 - - - A4 - C5 - | G4 - - - - - . . | F4 - A4 - D5 - C5 - | D5 - - - - - . . |
              C5 - - - A4 - C5 - | E5 - - - D5 - C5 - | D5 - - - F5 - D5 - | C5 - - - - - . . |
              A5 - - - F5 - D5 - | F5 - - - D5 - Bb4 - | C5 - A4 - C5 - F5 - | E5 - - - - - . . |
              D5 - - - Bb4 - D5 - | C5 - - - E5 - G5 - | F5 - - - - - - - | . . . . . . . .`,
    },
    parts: [
      { style: "pad", inst: "pad", octave: 3, vol: 0.8 },
      { style: "bass", inst: "bass", octave: 2, vol: 0.5 },
      { style: "arp", inst: "pluck", octave: 4, vol: 0.22 },
    ],
  },

  // Chapter 1: Valentine's Day. A slow waltz on electric piano.
  valentine: {
    bpm: 100,
    beats: 3,
    chords: "G | Em | Am | D | G | Em | C | D | Bm | Em | Am | D | G | C | D | G",
    melody: {
      inst: "epiano",
      notes: `D5 - - - B4 - | G5 - - - E5 - | C5 - E5 - A5 - | F#5 - - - - - |
              D5 - - - B4 - | E5 - G5 - B5 - | A5 - G5 - E5 - | D5 - - - - - |
              F#5 - - - D5 - | G5 - - - B4 - | C5 - D5 - E5 - | A4 - - - - - |
              B4 - D5 - G5 - | E5 - - - C5 - | A4 - C5 - F#5 - | G5 - - - . .`,
    },
    parts: [
      { style: "waltz", inst: "pluck", octave: 2, vol: 0.45 },
      { style: "pad", inst: "pad", octave: 3, vol: 0.4 },
    ],
  },

  // Chapter 2: Chinatown. Bustling, pentatonic, plucked strings and woodblock.
  chinatown: {
    bpm: 116,
    chords: "D | Bm | G | A | D | Bm | G | A | Bm | A | G | D | Bm | A | G | A",
    melody: {
      inst: "pluck",
      notes: `F#5 - A5 - B5 A5 F#5 - | E5 - F#5 - D5 - . . | B4 - D5 - E5 - D5 B4 | A4 - - - . . . . |
              F#5 - A5 - B5 A5 F#5 - | E5 - F#5 - A5 - B5 - | D6 - B5 - A5 - F#5 - | E5 - - - . . . . |
              B5 - A5 B5 - A5 F#5 - | E5 - F#5 - A5 - . . | B5 - A5 - F#5 - E5 - | D5 - - - . . . . |
              F#5 - F#5 A5 B5 - A5 - | E5 - - - A4 - B4 - | D5 - E5 - F#5 - A5 - | E5 - - - . . A4 -`,
    },
    parts: [
      { style: "arp", inst: "chip", octave: 4, vol: 0.35 },
      { style: "bass", inst: "bass", octave: 2, vol: 0.7 },
      { drums: { kick: "x...x...", block: "x..x..x.", hat: ".o.o.o.o" }, vol: 0.8 },
    ],
  },

  // Chapter 3: Graduation. A proud little march.
  graduation: {
    bpm: 104,
    chords: "C | F | C | G | Am | F | G | C | F | G | Em | Am | Dm | G | C | C",
    melody: {
      inst: "lead",
      notes: `G4 - C5 - E5 - G5 - | A5 - - - F5 - . . | G5 - E5 - C5 - E5 - | D5 - - - - - . . |
              E5 - A5 - C6 - B5 A5 | A5 - F5 - C5 - F5 - | G5 - - - B4 - D5 - | C5 - - - - - . . |
              A5 - - - C6 - A5 - | G5 - - - D5 - G5 - | E5 - G5 - B5 - G5 - | A5 - - - E5 - . . |
              F5 - A5 - D6 - C6 - | B5 - - - D5 - G5 - | C6 - - - G5 - E5 - | C5 - - - . . G4 -`,
    },
    parts: [
      { style: "pad", inst: "pad", octave: 3, vol: 0.6 },
      { style: "bass", inst: "bass", octave: 2, vol: 0.8 },
      { drums: { kick: "x...x...", snare: "..x...xo" }, vol: 0.7 },
    ],
  },

  // Chapter 4: Moving day. Bouncy and busy.
  moving: {
    bpm: 132,
    chords: "F | Dm | Gm | C | F | Dm | Gm | C | Bb | C | Am | Dm | Gm | C | F | C",
    melody: {
      inst: "chip",
      notes: `C5 . A4 . C5 . F5 . | E5 . D5 . A4 - . . | Bb4 . D5 . G5 . F5 . | E5 - - . C5 . . . |
              C5 . A4 . C5 . F5 . | A5 . G5 . F5 . D5 . | G5 . F5 . E5 . D5 . | C5 - - - . . . . |
              D5 . F5 . Bb5 - A5 . | G5 . E5 . C5 - . . | E5 . A5 . C6 - A5 . | F5 . D5 . A4 - . . |
              Bb4 . D5 . G5 . Bb5 . | A5 . G5 . E5 . C5 . | F5 . . . A5 . C6 . | . . G5 . E5 . C5 .`,
    },
    parts: [
      { style: "oompah", inst: "bass", octave: 2, vol: 0.7 },
      { drums: { kick: "x...x...", snare: "..x...x.", hat: ".o.o.o.o" }, vol: 0.7 },
    ],
  },

  // Chapter 5, morning: Decker's. Breezy.
  morning: {
    bpm: 98,
    chords: "D | A | Bm | G | D | A | Bm | G | D | A | Bm | G | D | A | Bm | G",
    melody: {
      inst: "pluck",
      notes: `F#5 - - A5 - F#5 E5 - | E5 - - - C#5 - . . | D5 - - F#5 - D5 B4 - | B4 - - - . . . . |
              F#5 - - A5 - B5 A5 - | A5 - - - E5 - C#5 - | D5 - F#5 - B5 - A5 - | G5 - - - . . . . |
              A5 - - F#5 - A5 D6 - | C#6 - - - A5 - E5 - | F#5 - - D5 - F#5 B5 - | B5 - - - G5 - . . |
              F#5 - E5 - D5 - E5 - | E5 - - - C#5 - E5 - | D5 - - - B4 - D5 - | E5 - - - . . . .`,
    },
    parts: [
      { style: "backbeat", inst: "epiano", octave: 4, vol: 0.5 },
      { style: "bass", inst: "bass", octave: 2, vol: 0.7 },
      { drums: { kick: "x...x.x.", brush: "..x...x.", hat: ".o.o.o.o" }, vol: 0.6 },
    ],
  },

  // Chapter 5, dinner: Yokocho. Calm, koto over a soft pad.
  yokocho: {
    bpm: 72,
    chords: "Am | F | Esus4 | E | Am | Dm | F | E | Am | F | E | Am | Dm | F | E | Am",
    melody: {
      inst: "pluck",
      notes: `E5 - - - A5 - B5 - | C6 - - - A5 - - - | B5 - - - - - . . | . . B4 - E5 - B5 - |
              A5 - - - C6 - B5 - | A5 - - - F5 - D5 - | E5 - F5 - A5 - C6 - | B5 - - - - - . . |
              E6 - - - C6 - B5 - | A5 - - - F5 - A5 - | B5 - - - E5 - - - | A5 - - - - - . . |
              D5 - F5 - A5 - C6 - | C6 - A5 - F5 - . . | E5 - - - B5 - - - | A5 - - - - - . .`,
    },
    parts: [
      { style: "pad", inst: "pad", octave: 3, vol: 0.5 },
      { style: "arp", inst: "pluck", octave: 3, vol: 0.3 },
      { style: "bass", inst: "bass", octave: 2, vol: 0.5 },
    ],
  },

  // Chapter 5, drinks: the rooftop at night. Dreamy.
  rooftop: {
    bpm: 70,
    chords: "Fmaj7 | Em7 | Dm7 | Cmaj7 | Fmaj7 | Em7 | Am7 | G | Dm7 | Em7 | Fmaj7 | G | Fmaj7 | Em7 | Dm7 | Cmaj7",
    melody: {
      inst: "bell",
      notes: `E5 - - - - - C5 - | D5 - - - G5 - - - | F5 - - - E5 - D5 - | E5 - - - - - . . |
              A5 - - - G5 - E5 - | G5 - - - B5 - - - | C6 - - - B5 - A5 - | B5 - - - - - . . |
              A5 - - - F5 - A5 - | G5 - - - E5 - G5 - | A5 - C6 - E6 - - - | D6 - - - - - . . |
              C6 - - - A5 - F5 - | G5 - - - E5 - D5 - | C5 - D5 - F5 - E5 - | C5 - - - - - . .`,
    },
    parts: [
      { style: "pad", inst: "pad", octave: 3, vol: 0.7 },
      { style: "arp", inst: "epiano", octave: 4, vol: 0.28 },
      { style: "bass", inst: "bass", octave: 2, vol: 0.5 },
      { drums: { brush: "..o...o." }, vol: 0.5 },
    ],
  },

  // The ending: Andy's Jazz Club. Swing, with a walking bass, piano, ride
  // cymbal and sax.
  andys: {
    bpm: 132,
    swing: 0.64,
    chords: "Gm7 | C7 | Fmaj7 | D7 | Gm7 | C7 | Am7 D7 | Gm7 C7 | Fmaj7 | F7 | Bbmaj7 | Bbm7 Eb7 | Am7 | D7 | Gm7 C7 | Fmaj7",
    melody: {
      inst: "sax",
      notes: `. . Bb4 D5 F5 - A5 - | G5 - E5 - - C5 Bb4 - | A4 - - - - - . . | . . F#4 A4 C5 - D5 - |
              Bb4 - - - D5 - F5 - | E5 - - G5 - E5 C5 - | E5 - C5 - F#5 - A5 - | G5 - - F5 - - E5 - |
              F5 - - - - - . . | . . A4 C5 Eb5 - D5 - | D5 - - - F5 - A5 - | Ab5 - F5 - G5 - Db5 - |
              C5 - - E5 - G5 - . | F#5 - - A5 - C6 A5 . | G5 - Bb5 - E5 - G5 - | F5 - - - . . . .`,
    },
    parts: [
      { style: "walk", inst: "upright", octave: 2, vol: 1 },
      { style: "comp", inst: "epiano", octave: 4, vol: 0.5 },
      { drums: { ride: "x.xox.xo", hat: "..o...o." }, vol: 0.7 },
    ],
  },
};
