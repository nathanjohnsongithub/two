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
  font: "monospace",
  background: [26, 20, 32],
  touchToMouse: true,
});
