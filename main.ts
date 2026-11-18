#!/usr/bin/env node
// news-image-20261117 round 2: copy the baked front-page image to /output.
// Node 22, stdlib only. No network, no timestamps, deterministic:
// the output is a byte copy of entry.png shipped in this repository.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");

const outDir = process.env.OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
