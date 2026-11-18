// news-image-20261117 — entrypoint.
// Copies the front-page image drawn by draw.py (entry.png, in this repo)
// to /output/entry.png. Node stdlib only, no network, deterministic:
// the same bytes come out every run.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));

const outDir = process.env.OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
