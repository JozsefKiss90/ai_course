# excel_module

Budget templating: Claude Code skills that build blank Planning Workbooks for Horizon Europe and Erasmus+ proposals. The vocabulary is in [CONTEXT.md](CONTEXT.md), the decisions in [docs/adr/](docs/adr/).

## Building a Planning Workbook

Start Claude Code in this directory (`excel_module`) and run `/budget-planner`, or ask for a budget planning workbook. The skill asks only for Shape Parameters (Funding Profile, counts, duration, Estimation Methods, headroom), reads them back for you to confirm, then builds, checks and delivers the Handover Package. Microsoft Excel 2021 or 365 and [uv](https://docs.astral.sh/uv/) must be installed.

If you start Claude Code at the repository root instead, the skill appears only once Claude has read a file under `excel_module/`. To load it at once, run `/add-dir excel_module` or start with `claude --add-dir excel_module`.

Never type partner names, countries, titles, rates, effort or amounts into the conversation. You enter them yourself in the delivered workbook.

The engine is in [budget_engine/](budget_engine/) (`uv run pytest` runs its tests; the `excel` tests need Excel).
