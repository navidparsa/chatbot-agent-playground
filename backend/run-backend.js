const { execSync } = require("child_process");
const path = require("path");

const isWin = process.platform === "win32";
const python = isWin
  ? path.join("venv", "Scripts", "python")
  : path.join("venv", "bin", "python");

execSync(`${python} -m uvicorn main:app --reload --port 8000`, { stdio: "inherit" });
