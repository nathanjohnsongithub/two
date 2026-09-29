import kaplay from "kaplay";

// Portrait-shaped canvas since she'll most likely play on her phone.
// Letterboxing keeps the aspect ratio on any screen.
export const k = kaplay({
  width: 320,
  height: 480,
  letterbox: true,
  crisp: true,
  texFilter: "nearest",
  global: false,
  // Jersey 10, a pixel font (public/fonts). It's only crisp at whole multiples
  // of its 10px grid, so every text size in the game is 10, 20, 30 or 40.
  font: "pixel",
  background: [26, 20, 32],
  touchToMouse: true,
});
