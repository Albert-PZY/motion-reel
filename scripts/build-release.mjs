import {
  copyFileSync,
  cpSync,
  existsSync,
  mkdirSync,
  readFileSync,
  readdirSync,
  rmSync,
  statSync,
  writeFileSync,
} from "node:fs";
import { basename, dirname, join } from "node:path";
import { execFileSync } from "node:child_process";

const root = process.cwd();
const dist = join(root, "dist");
const staging = join(dist, "motion-reel");
const archive = join(dist, "motion-reel.zip");
const include = [
  "SKILL.md",
  "agents",
  "references",
  "templates",
  "scripts/generate_audio_edge.py",
  "scripts/generate_audio_minimax.py",
  "README.md",
  "README_zh-CN.md",
  "LICENSE",
];

rmSync(dist, { recursive: true, force: true });
mkdirSync(staging, { recursive: true });

for (const item of include) {
  const source = join(root, item);
  const target = join(staging, item);
  const stats = statSync(source);
  if (stats.isDirectory()) {
    cpSync(source, target, { recursive: true });
  } else {
    mkdirSync(dirname(target), { recursive: true });
    copyFileSync(source, target);
  }
}

writeFileSync(
  join(staging, "VERSION"),
  `${JSON.parse(readFileSyncUtf8(join(root, "package.json"))).version}\n`,
  { encoding: "utf8" },
);

if (existsSync(archive)) {
  rmSync(archive);
}

try {
  execFileSync(
    "powershell",
    [
      "-NoProfile",
      "-Command",
      `Compress-Archive -Path ${JSON.stringify(join(staging, "*"))} -DestinationPath ${JSON.stringify(archive)} -Force`,
    ],
    { stdio: "inherit" },
  );
} catch {
  execFileSync("zip", ["-r", archive, basename(staging)], {
    cwd: dist,
    stdio: "inherit",
  });
}

const entries = readdirSync(staging);
if (!entries.includes("SKILL.md") || !entries.includes("agents")) {
  throw new Error("Release staging is missing required skill files.");
}

console.log(`Built ${archive}`);

function readFileSyncUtf8(path) {
  return readFileSync(path, "utf8");
}
