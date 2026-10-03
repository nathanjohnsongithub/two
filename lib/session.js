// Signed session tokens shared by the login function (Node) and the middleware
// (Edge). Both runtimes have Web Crypto, so this file sticks to crypto.subtle.
// A token is "<expiry ms>.<base64url HMAC-SHA256 of the expiry>".

export const SESSION_COOKIE = "two_session";
export const SESSION_MAX_AGE = 60 * 60 * 24 * 365; // a year: it's a gift, not a bank

const enc = new TextEncoder();

function key(secret, usage) {
  return crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, [usage]);
}

function toBase64Url(bytes) {
  return btoa(String.fromCharCode(...new Uint8Array(bytes))).replace(/=+$/, "").replace(/\+/g, "-").replace(/\//g, "_");
}

function fromBase64Url(str) {
  const b64 = str.replace(/-/g, "+").replace(/_/g, "/").padEnd(Math.ceil(str.length / 4) * 4, "=");
  return Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
}

export async function issueToken(secret) {
  const exp = String(Date.now() + SESSION_MAX_AGE * 1000);
  const sig = await crypto.subtle.sign("HMAC", await key(secret, "sign"), enc.encode(exp));
  return `${exp}.${toBase64Url(sig)}`;
}

export async function verifyToken(token, secret) {
  if (!token || !secret) return false;
  const [exp, sig] = token.split(".");
  if (!exp || !sig || !(Number(exp) > Date.now())) return false;
  try {
    // subtle.verify compares in constant time
    return await crypto.subtle.verify("HMAC", await key(secret, "verify"), fromBase64Url(sig), enc.encode(exp));
  } catch {
    return false;
  }
}

export function readCookie(header, name) {
  const pair = (header || "").split(";").map((c) => c.trim()).find((c) => c.startsWith(`${name}=`));
  return pair ? pair.slice(name.length + 1) : null;
}

export function sessionCookie(token) {
  return `${SESSION_COOKIE}=${token}; Path=/; Max-Age=${SESSION_MAX_AGE}; HttpOnly; Secure; SameSite=Lax`;
}
