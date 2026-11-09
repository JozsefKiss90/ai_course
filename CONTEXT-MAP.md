# Context Map

This repo has two bounded contexts.

- **AI Course for Research Management** — `CONTEXT.md`, decisions in `docs/adr/`. The course itself: sessions, the KM System, tool rules.
- **Budget Templating** — `excel_module/CONTEXT.md`, decisions in `excel_module/docs/adr/`. Agent skills that build Excel Planning Workbooks for Horizon Europe and Erasmus+ proposals.

The course's *Optional Use-Case Phase* (detailed budgets) is where the two touch; the Budget Templating context does not reuse course vocabulary.
