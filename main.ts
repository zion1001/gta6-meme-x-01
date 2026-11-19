// main.ts — entrypoint for the gta6-meme-x-01 bounty ("Post a GTA 6 meme on X").
//
// The entry itself is a post on X, so this program has exactly one job:
// copy POST.json from the repository root into the harness output directory.
// It uses only the Node standard library and touches no network.
import {
  existsSync,
  mkdirSync,
  readFileSync,
  renameSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { join } from "node:path";

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? ".";
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// The shape the house's gate accepts: an X post address whose id is digits.
const POST_URL =
  /^(?:https?:\/\/)?(?:www\.|mobile\.)?(?:x\.com|twitter\.com)\/(?:i\/web\/status\/(\d+)|[^/]+\/status(?:es)?\/(\d+))\/?(?:[?#].*)?$/;

const source = join(BOT_DIR, "POST.json");
const target = join(OUT_DIR, "POST.json");

function fail(message: string): never {
  console.error(message);
  process.exit(1);
}

if (!existsSync(source)) {
  fail(`POST.json not found at ${source}`);
}

const text = readFileSync(source, "utf8");

let parsed: unknown;
try {
  parsed = JSON.parse(text);
} catch {
  fail("POST.json is not valid JSON");
}
if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
  fail("POST.json must be a JSON object");
}
const url = (parsed as Record<string, unknown>).url;
if (typeof url !== "string" || !POST_URL.test(url)) {
  fail(
    "POST.json must carry a url shaped like " +
      "https://x.com/<handle>/status/<digits>",
  );
}

mkdirSync(OUT_DIR, { recursive: true });

// Write to a temp file first, then rename, so a reader never sees a
// half-written POST.json.
const tmp = join(OUT_DIR, `.POST.json.tmp-${process.pid}`);
try {
  writeFileSync(tmp, text, "utf8");
  renameSync(tmp, target);
} catch (err) {
  try {
    unlinkSync(tmp);
  } catch {
    // Nothing to clean up.
  }
  throw err;
}
console.log(`wrote ${target}`);
