---
inclusion: auto
---

# Windows CMD Environment

All tasks and commands in this project run on Windows CMD (cmd.exe).

- Use `&` to separate commands (not `&&`)
- Use native Windows commands (e.g., `dir`, `type`, `del`, `mkdir`, `copy`)
- Do not use bash or PowerShell-specific commands

# Python Environment

- Use `uv` as the package manager and virtual environment tool (not pip/venv)
- Python version: 3.14t (free-threaded, no GIL)
- Create venv: `uv venv --python 3.14t`
- Install dependencies: `uv pip install -e ".[dev]"`
- Run scripts: `uv run <command>`
- Activate venv on Windows CMD: `.venv\Scripts\activate`
- Before running Python commands, verify that the venv is activated or use `uv run`
