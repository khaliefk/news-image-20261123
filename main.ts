// news-image-20261123: the entry image sits beside this file as entry.png.
// The program copies it to /output/entry.png. No network, no dependencies,
// and the same bytes come out on every run.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = join(here, 'entry.png');
const target = join(outDir, 'entry.png');
mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);
