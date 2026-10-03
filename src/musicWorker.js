// Renders songs and sound effects off the main thread, so the game never
// stutters while the synthesizer works (see src/audio.js).
import { renderEffect, renderSong } from "./synth.js";
import { SONGS } from "./music.js";

self.onmessage = ({ data: { id, song, effect } }) => {
  const samples = song ? renderSong(SONGS[song]) : renderEffect(effect);
  self.postMessage({ id, samples }, [samples.buffer]);
};
