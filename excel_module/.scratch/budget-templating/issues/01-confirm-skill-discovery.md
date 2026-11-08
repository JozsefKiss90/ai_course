# 01 — Confirm Claude Code discovers skills stored in excel_module

**What to build:** A definitive answer to whether Claude Code discovers skills placed in `excel_module`'s own skills directory when a session is started from the repo root as well as from `excel_module`, and a decision on where the two budget templating skills (`budget-planner`, `budget-profile-maintainer`) will live.

**Blocked by:** None — can start immediately.

**Status:** ready-for-agent

- [ ] Discovery behaviour verified for both start locations (repo root, `excel_module`), using current Claude Code documentation plus a throwaway test skill
- [ ] Throwaway test skill removed afterwards
- [ ] Decision recorded under `## Answer`: the skills' home directory and any consequence for how users start a session
- [ ] If the answer forces a location other than `excel_module`'s skills directory, the spec's Implementation Decisions note is flagged for update
