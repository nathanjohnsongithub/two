// Prints the env vars for the password gate (middleware.js + api/login.js).
// Usage: node tools/make_password.js 'the password'
// Paste the output into the Vercel project's Environment Variables.

import { randomBytes, scryptSync } from "node:crypto";

const password = process.argv[2];
if (!password) {
  console.error("Usage: node tools/make_password.js '<password>'");
  process.exit(1);
}

const salt = randomBytes(16);
console.log(`SITE_PW_SALT=${salt.toString("base64")}`);
console.log(`SITE_PW_HASH=${scryptSync(password, salt, 64).toString("base64")}`);
console.log(`SESSION_SECRET=${randomBytes(32).toString("base64url")}`);
