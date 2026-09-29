// Remembers how far she got, so a phone call or a reload doesn't send her back
// to chapter 1: { chapter, done }. Private browsing can refuse storage, so
// every read and write is allowed to fail quietly.
const KEY = "year-two-progress";

export function loadProgress() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) ?? {};
  } catch {
    return {};
  }
}

export function saveProgress(changes) {
  try {
    localStorage.setItem(KEY, JSON.stringify({ ...loadProgress(), ...changes }));
  } catch {
    // Nothing to do: the game just won't remember.
  }
}
