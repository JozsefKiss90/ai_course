# AGENTS.md: instructions for every AI coding agent in this folder

OpenCode, Antigravity CLI and GitHub Copilot all read this file before they start work.
It does the job a Gem's system instructions did in the AGA Wiki lesson: it sets the role, the rules and the output format.

## Who you are working with
- An experienced Excel user who is new to programming, Git and the terminal.
- Explain what you are about to do in plain language **before** running a command, and say what each command does.
- Prefer small, readable Python scripts over clever ones. Add a short comment wherever an Excel user would ask "why?".

## Data rule (the course's two-lane rule; this one is not negotiable)
- This workspace is **Daily Driver** territory: only fictional or anonymised data goes in it.
- If a file looks like real institutional finance data (real names, salaries, real project budgets, bank details), **stop and tell the user**. Do not read further, summarise or upload it.
- Never send data to any website or API other than the model you are running on.

## How to work in this project
- Python is managed by `uv`. Run scripts with `uv run python <script>`, add libraries with `uv add <name>`. Never use `pip install`.
- Source data lives in `data/`. **Never overwrite or edit files in `data/`**; write new files to `output/`.
- Excel outputs must stay auditable: write **live Excel formulas** (e.g. `=D2*F2`) wherever the user would expect them, not pasted values. Put assumptions (rates, percentages) in labelled input cells and reference them from the formulas.
- Every number in an output must be traceable to a source line (the `source_note` column) or to a stated rule, like `source_refs` in the AGA wiki. If you apply a funding rule, cite it (e.g. "AGA Art. 6.2.E, 25% flat rate").
- After changing code, run `uv run pytest` and `uv run python scripts/check_setup.py`, then report the result.
- Close-the-workbook rule: if saving fails with a permission error, the file is open in Excel. Ask the user to close it.

## Git
- Do not commit or push unless the user asks. When asked, use a short commit message that says what changed and why.
- Never delete files or rewrite history (`git reset --hard`, `git push --force`) without explicit permission.

## Project map
- `data/sample_budget.csv`: fictional Horizon Europe-style budget (categories A, B, C1–C3).
- `scripts/check_setup.py`: setup check; also a worked example of pandas → openpyxl with live formulas.
- `tests/`: automatic checks for budget rules (`uv run pytest`).
- `output/`: generated files (ignored by Git).
