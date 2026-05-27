import { execFileSync } from "node:child_process";

const files = [
  "scripts/generate_audio_edge.py",
  "scripts/generate_audio_minimax.py",
];
const python = findPython();

for (const file of files) {
  execFileSync(python, ["-m", "py_compile", file], { stdio: "inherit" });
}

console.log("Python syntax checks passed.");

function findPython() {
  for (const command of ["python", "python3"]) {
    try {
      execFileSync(command, ["--version"], { stdio: "ignore" });
      return command;
    } catch {
      // Try the next common Python command.
    }
  }

  throw new Error("Python was not found. Install Python 3 before running tests.");
}
