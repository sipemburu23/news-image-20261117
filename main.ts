// main.ts — news-image-20261117 round 3.
// Copies the baked front-page image (entry.png, rendered by draw.py in this
// repo) to /output/entry.png. Node 22+, stdlib only, no network, no
// timestamps: the output is a byte-for-byte copy of the baked image, so two
// runs from any working directory produce identical bytes.
// Entry point: the grader runs `node main.ts`. The file contains no
// TypeScript-only syntax, so Node 22+ runs it as-is.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")}`);
