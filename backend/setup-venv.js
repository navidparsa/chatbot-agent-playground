const { execSync } = require("child_process");
const path = require("path");

const isWin = process.platform === "win32";
const pythonCmd = isWin ? "python" : "python3";
const pip = isWin ? path.join("venv", "Scripts", "pip") : path.join("venv", "bin", "pip");

execSync(`${pythonCmd} -m venv venv`, { stdio: "inherit" });
execSync(`${pip} install -r requirements.txt`, { stdio: "inherit" });
