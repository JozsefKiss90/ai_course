# 01 — Confirm Claude Code discovers skills stored in excel_module

**What to build:** A definitive answer to whether Claude Code discovers skills placed in `excel_module`'s own skills directory when a session is started from the repo root as well as from `excel_module`, and a decision on where the two budget templating skills (`budget-planner`, `budget-profile-maintainer`) will live.

**Blocked by:** None — can start immediately.

**Status:** done

- [x] Discovery behaviour verified for both start locations (repo root, `excel_module`), using current Claude Code documentation plus a throwaway test skill
- [x] Throwaway test skill removed afterwards
- [x] Decision recorded under `## Answer`: the skills' home directory and any consequence for how users start a session
- [x] If the answer forces a location other than `excel_module`'s skills directory, the spec's Implementation Decisions note is flagged for update (not needed: the location stays `excel_module/.claude/skills/`)

## Answer

**Short version:** Both start locations work. From `excel_module` the skills load at startup. From the repo root they load lazily, the first time Claude reads or edits a file under `excel_module/`.

### Findings per start location

- **Started in `C:\elte_ai_course\excel_module`:** the skills load at startup. They show up in the skill list and the `/` menu right away. The root's `.claude/skills/` also loads, because Claude Code walks parent directories up to the repo root.
- **Started in `C:\elte_ai_course` (repo root):** the skills do not load at startup. They load the first time Claude reads or edits a file under `excel_module/`, and then stay loaded for the rest of the session. Until then you can't invoke them by name and they don't appear in the `/` menu. To load them earlier, run `/add-dir excel_module` (needs v2.1.257 or later) or start with `--add-dir excel_module`.

### Evidence

- Docs: https://code.claude.com/docs/en/skills, sections "Parent directories" and "Nested directories and monorepos". Quote: "Skills in a `.claude/skills/` directory below where you started don't load at startup. They load the first time Claude reads or edits a file in that subdirectory and stay available for the rest of the session."
- Empirical test with Claude Code 2.1.300 and a throwaway skill at `excel_module/.claude/skills/zz-discovery-probe/`:
  - `claude -p` from the repo root, no file access: probe **not** listed.
  - `claude -p` from `excel_module`: probe listed at startup.
  - `claude -p` from the repo root, after a Read of `excel_module/CONTEXT.md`: the harness reported "New skills discovered in excel_module\.claude\skills, now available via the Skill tool: zz-discovery-probe".
- The probe skill and the empty `excel_module/.claude/` directory were deleted afterwards. Deletion was verified.

### Decision

`budget-planner` and `budget-profile-maintainer` live in `excel_module/.claude/skills/`, as the spec already says. The spec's Implementation Decisions note needs no change.

### Consequence for how users start a session

- Recommended: start Claude Code in `excel_module`. Both skills are then available immediately by name or slash command.
- If a user starts at the repo root, the skills appear only after Claude touches a file in `excel_module/`, or after `/add-dir excel_module`. User-facing docs should mention this.
- A nested skill with the same name as a root skill gets a path-qualified command (for example `/excel_module:budget-planner`). Our two names don't clash with any root skill.
