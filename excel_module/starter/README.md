# Excel for Finance: starter workspace

Your personal copy of the course workspace for the *Excel for Finance* module.
Everything in it is **fictional training data**. Never add real institutional budgets or personnel data.

## First run (setup session)

```powershell
cd $HOME\Documents\ai-course\excel-finance     # the folder you cloned
.\check_setup.ps1                              # checks everything, writes setup_report.txt
```

When the last line says **READY FOR THE MODULE**, you are done. Open `output\setup_check.xlsx` in Excel: column G holds live formulas and column H the values Python calculated, and they must agree.

## Everyday commands

| What | Command |
|---|---|
| Open this folder in VS Code | `code .` |
| Run a Python script | `uv run python scripts\check_setup.py` |
| Run the budget-rule checks | `uv run pytest` |
| Start the AI agent (OpenCode) | `opencode` |
| Start the Google agent (Antigravity CLI) | `agy` |
| See what changed | `git status` |
| Save a snapshot | `git add .` then `git commit -m "what and why"` |
| Upload snapshots to GitHub | `git push` |

## Folder map

```
data/      source data (read-only for scripts and agents)
scripts/   Python scripts
tests/     automatic checks (uv run pytest)
output/    generated Excel files (not stored in Git)
AGENTS.md  standing instructions for the AI agents
```
