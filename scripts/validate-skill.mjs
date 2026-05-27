import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const root = process.cwd();
const requiredFiles = [
  "SKILL.md",
  "agents/openai.yaml",
  "references/remotion-patterns.md",
  "references/tts.md",
  "references/three.md",
  "references/tutorial-video.md",
  "templates/audioConfig.ts",
  "templates/scenes.json",
  "scripts/generate_audio_edge.py",
  "scripts/generate_audio_minimax.py",
  "scripts/check-python-syntax.mjs",
  "README.md",
  "README_zh-CN.md",
  "LICENSE",
];

const forbiddenCommandExamples = [
  /^\s*(?:npm\s+(?:install|update|run|i)\b|npx\b|pip\s+(?:install|uninstall)\b)/,
];
const claudeOnlyPatterns = [/Claude Code/i, /\.claude/i];

const errors = [];

for (const relativePath of requiredFiles) {
  try {
    statSync(join(root, relativePath));
  } catch {
    errors.push(`Missing required file: ${relativePath}`);
  }
}

const skill = readFileSync(join(root, "SKILL.md"), "utf8");
const match = skill.match(/^---\n([\s\S]+?)\n---\n/);
if (!match) {
  errors.push("SKILL.md must start with YAML frontmatter.");
} else {
  if (!/^name:\s*motion-reel$/m.test(match[1])) {
    errors.push("SKILL.md frontmatter must include name: motion-reel.");
  }
  if (!/^description:\s*.+/m.test(match[1])) {
    errors.push("SKILL.md frontmatter must include description.");
  }
}

const textExtensions = new Set([
  ".md",
  ".yaml",
  ".yml",
  ".json",
  ".ts",
  ".py",
  ".mjs",
  ".js",
  ".txt",
]);

function extensionOf(fileName) {
  const index = fileName.lastIndexOf(".");
  return index === -1 ? "" : fileName.slice(index);
}

function walk(directory) {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    if (entry.name === ".git" || entry.name === "node_modules" || entry.name === "dist") {
      continue;
    }
    const fullPath = join(directory, entry.name);
    if (entry.isDirectory()) {
      walk(fullPath);
      continue;
    }

    if (!textExtensions.has(extensionOf(entry.name))) {
      continue;
    }

    const buffer = readFileSync(fullPath);
    const relativePath = fullPath.slice(root.length + 1).replaceAll("\\", "/");
    if (buffer.length >= 3 && buffer[0] === 0xef && buffer[1] === 0xbb && buffer[2] === 0xbf) {
      errors.push(`${relativePath} contains a UTF-8 BOM.`);
    }

    const content = buffer.toString("utf8");
    if (content.includes("\r\n")) {
      errors.push(`${relativePath} uses CRLF line endings.`);
    }

    if (
      [
        "CHANGELOG.md",
        "docs/git-commit-guidelines.md",
        "scripts/validate-skill.mjs",
      ].includes(relativePath)
    ) {
      continue;
    }

    for (const line of content.split("\n")) {
      for (const pattern of forbiddenCommandExamples) {
        if (pattern.test(line)) {
          errors.push(`${relativePath} contains forbidden command example: ${line.trim()}`);
        }
      }
    }

    for (const pattern of claudeOnlyPatterns) {
      if (pattern.test(content)) {
        errors.push(`${relativePath} contains forbidden pattern ${pattern}.`);
      }
    }
  }
}

walk(root);

if (errors.length > 0) {
  console.error(errors.join("\n"));
  process.exit(1);
}

console.log("Skill validation passed.");
