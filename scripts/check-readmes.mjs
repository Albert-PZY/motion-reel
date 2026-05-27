import { readFileSync } from "node:fs";

const english = readFileSync("README.md", "utf8");
const chinese = readFileSync("README_zh-CN.md", "utf8");
const errors = [];

if (!english.startsWith("[中文](README_zh-CN.md)\n\n# Motion Reel")) {
  errors.push("README.md must start with a Chinese README link and title.");
}

if (!chinese.startsWith("[English](README.md)\n\n# Motion Reel")) {
  errors.push("README_zh-CN.md must start with an English README link and title.");
}

const requiredEnglishSections = [
  "## Attribution",
  "## Links",
  "## Release Status",
  "## Highlights",
  "## Install",
  "## Usage",
  "## Development",
  "## License",
];

const requiredChineseSections = [
  "## 来源与致谢",
  "## 快速入口",
  "## 发布状态",
  "## 主要能力",
  "## 安装",
  "## 使用方式",
  "## 开发",
  "## 许可证",
];

for (const section of requiredEnglishSections) {
  if (!english.includes(section)) {
    errors.push(`README.md missing section: ${section}`);
  }
}

for (const section of requiredChineseSections) {
  if (!chinese.includes(section)) {
    errors.push(`README_zh-CN.md missing section: ${section}`);
  }
}

if (errors.length > 0) {
  console.error(errors.join("\n"));
  process.exit(1);
}

console.log("README checks passed.");

