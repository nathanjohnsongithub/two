// Vercel Routing Middleware: runs before every request, static files included,
// so the photos and the game itself stay private until Hannah signs in.
// (Not used by `npm run dev`; the Vite dev server stays open.)

import { SESSION_COOKIE, readCookie, verifyToken } from "./lib/session.js";

// What the login page needs before anyone has signed in.
const OPEN = [
  "/login.html",
  "/api/login",
  "/fonts/Jersey10.ttf",
  "/sprites/hannah.png",
  "/sprites/nathan.png",
  "/favicon.svg",
  "/favicon-32.png",
  "/apple-touch-icon.png",
];

export default async function middleware(request) {
  const url = new URL(request.url);
  if (OPEN.includes(url.pathname)) return;

  const token = readCookie(request.headers.get("cookie"), SESSION_COOKIE);
  if (await verifyToken(token, process.env.SESSION_SECRET)) return;

  const login = new URL("/login.html", url);
  if (url.pathname !== "/") login.searchParams.set("return", url.pathname + url.search);
  return Response.redirect(login, 307);
}
