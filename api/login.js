// POST /api/login {password} → sets the session cookie the middleware checks.
// The password is stored as a scrypt hash (see tools/make_password.js).

import { scryptSync, timingSafeEqual } from "node:crypto";

import { issueToken, sessionCookie } from "../lib/session.js";

const WINDOW_MS = 5 * 60 * 1000;
const MAX_FAILS = 10;
const fails = new Map(); // ip -> { count, first }; per instance, but slows guessing

function clientIp(req) {
  return req.headers["x-forwarded-for"]?.split(",")[0]?.trim() || req.socket?.remoteAddress || "unknown";
}

function limited(ip) {
  const entry = fails.get(ip);
  if (entry && Date.now() - entry.first > WINDOW_MS) fails.delete(ip);
  return (fails.get(ip)?.count ?? 0) >= MAX_FAILS;
}

function recordFail(ip) {
  const entry = fails.get(ip) ?? { count: 0, first: Date.now() };
  entry.count += 1;
  fails.set(ip, entry);
}

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).end();

  const { SITE_PW_SALT, SITE_PW_HASH, SESSION_SECRET } = process.env;
  if (!SITE_PW_SALT || !SITE_PW_HASH || !SESSION_SECRET) {
    return res.status(500).json({ error: "Password isn't set up yet" });
  }

  const ip = clientIp(req);
  if (limited(ip)) return res.status(429).json({ error: "Too many tries. Wait a few minutes." });

  const password = typeof req.body?.password === "string" ? req.body.password : "";
  const expected = Buffer.from(SITE_PW_HASH, "base64");
  const derived = scryptSync(password, Buffer.from(SITE_PW_SALT, "base64"), expected.length);
  if (!timingSafeEqual(derived, expected)) {
    recordFail(ip);
    return res.status(401).json({ error: "That's not it. Try again?" });
  }

  fails.delete(ip);
  res.setHeader("Set-Cookie", sessionCookie(await issueToken(SESSION_SECRET)));
  return res.status(200).json({ ok: true });
}
