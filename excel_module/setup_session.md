# Excel for Finance: Setup Session and Toolchain
## Facilitator plan (60 minutes, online via Teams) and tool decisions

**Purpose:** before Part 1 of the three-part *Excel for Finance* module, every participant has a working, tested coding environment on their own Windows machine: VS Code, Git + GitHub, Python (via uv) with the Excel/finance libraries, and two free-tier AI coding agents that can read, write and run code in a project folder. The session also teaches the minimum PowerShell and version control needed to work safely with agents.

**Who:** advanced Excel users with no experience of VS Code, GitHub, terminals, programming languages or AI coding tools.

**Status of this plan:** tool facts checked on 16 October 2026. Free tiers in this market change monthly (two of the obvious candidates disappeared in 2026), so the facilitator re-verifies them in the dry run the week before (see *Facilitator preparation*).

**Files in this folder:**
- `setup_session.md`: this plan (tool decisions, software list, session plan, risks)
- `participant_setup_guide.md`: the step-by-step guide participants follow (pre-work + in-session steps + cheat sheets)
- `starter/`: the course template repository. Publish it on GitHub as a **template repo**; each participant creates their own copy from it. It contains `check_setup.ps1` (full environment check), `scripts/check_setup.py` (Python + Excel round trip), `AGENTS.md` (agent instructions), fictional budget data and three budget-rule tests. Tested: Python check and tests pass (pandas 3.0, openpyxl 3.1, Python 3.12); the formulas in the generated workbook were recalculated and match the Python values; `check_setup.ps1` runs under PowerShell 7 and is written for Windows PowerShell 5.1 (ASCII only, no 7-only syntax). It still needs one run on a real Windows machine (dry run).

---

## 1. Tool decision: free-tier AI coding agents

Requirement: something that does what Claude Code or Codex does (an agent that reads the project, edits files, runs commands, and asks before acting) at zero cost to the participant, usable on Windows by a beginner.

| Candidate | Status (Oct 2026) | Verdict |
|---|---|---|
| **OpenCode** (open source, terminal + VS Code extension) | Free; built-in free models work with **no account and no API key**; can also use the participant's own Gemini API key (from Lesson 3) or GitHub Copilot sign-in | **Primary agent.** Closest equivalent to Claude Code; model-agnostic, so it survives any single provider's free tier ending |
| **Antigravity CLI** (`agy`, Google) | Google's successor to Gemini CLI; free with a personal Google account; weekly rate limits, figures not published; Gemini models (and some others) | **Second agent**: the Google/Gemini lineage participants know from the Daily Driver lane |
| **GitHub Copilot Free** (inside VS Code) | Free with the GitHub account participants need anyway; 2,000 completions/month plus a limited allowance of "GitHub AI Credits" for chat/agent; auto model selection only | **In-editor helper**: autocomplete and chat next to the code. Not relied on for heavy agent work (allowance too small) |
| Gemini CLI | Login with Google for personal/free accounts **stopped 18 June 2026**; Google says it stays available on *paid* API keys; free AI Studio keys are not confirmed either way | **Not used.** Named once as "what Antigravity CLI replaced" |
| Qwen Code | Free Qwen OAuth tier **shut down 15 April 2026**; remaining free routes need OpenRouter or a local model | Not used |
| Codex CLI | ChatGPT Free includes "limited" Codex access, enough to try, not to work | Mentioned only |
| Claude Code | Paid plans only | Mentioned only, as the reference point |

**Lane rule for all three agents:** they are **Daily Driver** tools. Free tiers may log or train on what is sent to them, and an agent reads *every file in the folder it is started in*. "Strategic financial planning" is explicitly Sensitive Lane in the course's two-lane rule, so **the module works with fictional or anonymised budgets only**, and real institutional finance files never sit in (or under) a project folder an agent is started in. `.gitignore` keeps files out of GitHub, not out of the agent's reach. This is taught in the session (Segment 4) and written into `AGENTS.md`.

**OpenCode model choice:** OpenCode's free model list rotates and the data policy differs per model. On 16 October 2026 its free list included `deepseek-v4.1-flash-free`, `space-bunny-free` and `longcat-2.5-preview-free`, which OpenCode Zen documents as **zero-retention, not used for training**. Others (Big Pickle, MiMo, Nemotron trial endpoints, Muse Spark "contributor") may be logged or used for training. Course default: **`opencode/deepseek-v4.1-flash-free`**, falling back to another zero-retention model. Re-check `/models` and the Zen page in the dry run.

**Known limit to plan around:** OpenCode's no-login free models are rate-limited **per IP address**. If several participants work from the same office network, they share one limit. Mitigations, in order: (1) each participant signs in to OpenCode Zen for a personal key (free; check in the dry run whether it asks for billing details); (2) switch to the participant's own Gemini API key via `/connect` → Google (Lesson 3 key; free tier, Daily Driver); (3) switch agent (`agy`).

---

## 2. Software, accounts and libraries

### Accounts (pre-work)
| Account | Why | Notes |
|---|---|---|
| GitHub (personal, free) | Stores each participant's project; version history; Copilot Free | Use a private e-mail setting (GitHub "noreply" address); turn on two-factor authentication when asked (GitHub requires it for code contributors) |
| Google (already exists) | Antigravity CLI sign-in; Gemini API key from Lesson 3 | Personal account, Daily Driver lane |
| OpenCode Zen (optional) | Personal key, higher limits than the shared per-IP free tier | Only if the shared limit bites |

### Programs (Windows 10/11)
| Program | winget ID | Why | Admin rights? |
|---|---|---|---|
| Windows Terminal + PowerShell | built in (Win 11) / `Microsoft.WindowsTerminal` | The terminal | No |
| Git for Windows | `Git.Git` | Version control; includes Git Credential Manager (browser sign-in to GitHub on first push) | Usually yes; check with IT |
| Visual Studio Code | `Microsoft.VisualStudioCode` | Editor; Source Control panel; runs notebooks; hosts Copilot and the OpenCode extension | No (user installer) |
| Node.js LTS | `OpenJS.NodeJS.LTS` | Needed to install OpenCode via `npm` (and future MCP servers) | Yes; check with IT |
| uv | `astral-sh.uv` | Installs and manages Python itself (no separate Python install), creates the project environment from the lock file in one command (`uv sync`) | No |
| OpenCode | `npm install -g opencode-ai` | Primary AI agent | No |
| Antigravity CLI | `irm https://antigravity.google/cli/install.ps1 \| iex` | Second AI agent | No |

No-admin fallback for managed machines: **Scoop** (`irm get.scoop.sh | iex`, then `scoop install git nodejs-lts uv opencode`) installs everything into the user profile. Decide with IT which path the cohort uses *before* sending the pre-work.

### VS Code extensions
| Extension | ID | Why |
|---|---|---|
| Python | `ms-python.python` | Run and debug Python, choose the project's environment |
| Jupyter | `ms-toolsai.jupyter` | Notebooks: code + tables + charts step by step, the most Excel-like way to start coding |
| Data Wrangler | `ms-toolsai.datawrangler` | Spreadsheet-style viewer/cleaner for DataFrames and CSV files; generates the pandas code for each step |
| Excel Viewer | `GrapeCity.gc-excelviewer` | Preview `.xlsx`/`.csv` inside VS Code (optional) |
| OpenCode | `sst-dev.opencode` | Runs OpenCode in a VS Code panel (optional; the terminal works too) |
| GitHub Copilot Chat | built into VS Code (sign in with GitHub) | Autocomplete + chat on Copilot Free |

### Python libraries (pinned by `starter/uv.lock`, installed by `uv sync`)
| Library | Excel equivalent / role |
|---|---|
| `pandas` | A sheet as a table (DataFrame): filters, lookups, pivots, group-bys |
| `openpyxl` | Read/write `.xlsx` with **live formulas**, styles, several sheets |
| `xlsxwriter` | Formatted reports with native Excel charts |
| `numpy` | Fast numeric arrays under pandas |
| `numpy-financial` | `NPV`, `IRR`, `PMT`, `FV`: Excel's financial functions |
| `matplotlib` | Charts as images |
| `ipykernel` | Lets VS Code run notebooks in the project environment |
| `pytest` | Automatic checks of budget rules: the code version of a reviewer's checklist |

**Deliberately left out (add per module part if needed):** `xlwings` (drives a *running* Excel from Python; Windows-only, worth adding if a part needs live workbook automation); **Python in Excel** (`=PY()`; needs a Microsoft 365 licence add-on and runs in Microsoft's cloud; would belong in the Sensitive Lane discussion, not this toolchain).

---

## 3. How the setup carries the AGA Wiki methods forward

The module re-uses the AGA Wiki's operating discipline. The tools change; the method doesn't:

| AGA Wiki (Lesson 3 / ops manual) | In the coding environment |
|---|---|
| Gem system instructions (role isolation, fixed knowledge) | `AGENTS.md`: standing instructions every agent reads first |
| NotebookLM grounding: every node carries `source_refs` | `source_note` column on every cost line; rules cited in code (e.g. AGA Art. 6.2.E) |
| One ticket = one pass, ≤ 15 nodes, explicit scope | One agent task = one small, scoped change, reviewed, then committed |
| Graph Health Dashboard / Dataview lint | `pytest` budget-rule checks + `check_setup.py`: run after every change |
| Snapshot per milestone | Git commit (and tag) per milestone; GitHub is the history |
| Human ratifies the schema; human gate on every paste | Human reads the diff in VS Code's Source Control panel before every commit |
| G8 Budget Assistant | The agent building budget workbooks with live, auditable formulas |

---

## 4. Timeline

| When | Who | What |
|---|---|---|
| 3 weeks before | Facilitator | Ask IT: winget/Scoop allowed? Admin rights for Git + Node.js? Are github.com, opencode.ai, antigravity.google, astral.sh, pypi.org, registry.npmjs.org reachable from the institutional network? |
| 2 weeks before | Facilitator | Publish `starter/` as a public **template repository** on GitHub; put its link into the guide. Dry run on a clean Windows machine (or Windows Sandbox) following `participant_setup_guide.md` word for word; time it |
| 1 week before | Facilitator | Re-verify the free tiers (OpenCode `/models` + Zen data table, Antigravity free quota, Copilot Free allowance); fix the guide; send it with the pre-work deadline |
| 1 week before → session | Participants | **Pre-work, Part A of the guide (≈ 30 min):** accounts + installs + `check_setup.ps1` first run |
| Setup session (60 min) | Everyone | Part B of the guide, below |
| Session → Part 1 | Facilitator | Anyone not "READY" gets a 15-minute fix call or uses the next Practice Week drop-in |

---

## 5. The 60-minute session

Shape: the installs happen in pre-work so the live hour goes on *understanding and verifying*, not on download bars. Participants who skipped pre-work install during Segment 2 while the others continue; the facilitator's screen stays the reference throughout.

| # | Segment | Min | Mode |
|---|---|---|---|
| 1 | Why code for Excel work, and the map of the toolchain | 5 | Presentation |
| 2 | PowerShell basics + `check_setup.ps1` first pass | 12 | Hands-on, follow-along |
| 3 | Git and GitHub: your own copy, first commit, first push | 15 | Hands-on, follow-along |
| 4 | First agent run: OpenCode, then Antigravity CLI, and the data rule | 18 | Demo, then hands-on |
| 5 | Final check, green-light screenshot, what Part 1 starts with | 7 | Hands-on + close |
| | Buffer | 3 | |

### Segment 1: Why code, and the map (5 min)
- One slide, one sentence: *"Excel is where you check the numbers; Python is how you make the same workbook again next month without retyping it; the agent is a colleague who writes the Python while you review it."*
- The map (one diagram): **VS Code** (the desk) → **Terminal / PowerShell** (where you give typed instructions) → **Git** (the save history) → **GitHub** (the history online) → **Python + libraries** (the engine that reads/writes Excel) → **Agents** (OpenCode, Antigravity) that use all of the above on your behalf, **under `AGENTS.md`**.
- 7 Levels link: this module is where participants move from *orchestrating tools* to *directing an agent that builds tools* (Level 5 territory).

### Segment 2: PowerShell basics + first check (12 min)
Follow-along, everyone typing (guide §B1). Commands taught, each with its Excel analogy:

| Command | What it does | Analogy |
|---|---|---|
| `pwd` | Where am I? | The path in the title bar |
| `ls` | What is in this folder? | File Explorer view |
| `cd folder` / `cd ..` | Go into / up one folder | Double-click / Back |
| `mkdir name` | New folder | New folder |
| `code .` | Open this folder in VS Code | Open workbook |
| `cat file` | Show a text file | Preview pane |
| `Tab` | Completes names: type `cd Doc` + Tab | Autocomplete |
| `↑` | Previous command | Ctrl+Y (repeat) |
| `Ctrl+C` | Stop the running command | Esc |
| `cls` | Clear the screen | — |

Then: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (why: Windows blocks scripts by default, including the ones npm installs), and the most common beginner fix: **"command not found" after an install → close and reopen the terminal.**

### Segment 3: Git and GitHub (15 min)
Guide §B2. Concepts in three sentences: a **repository** is a project folder with a memory; a **commit** is a named snapshot (like *Save As* with a version note); **push** uploads snapshots to GitHub.
1. On GitHub: open the template link → *Use this template* → *Create a new repository* → name `excel-finance`, **Private**.
2. Terminal: `cd $HOME\Documents\ai-course` → `git clone <your repo URL>` → `cd excel-finance` → `code .`
3. In VS Code: add one line to `README.md` ("Setup completed by …"), save. Show the **Source Control** panel: the changed line in green, *before* committing. This is the human gate from the AGA Wiki.
4. Terminal: `git status` → `git add README.md` → `git commit -m "My first commit"` → `git push` (browser sign-in to GitHub opens once, via Git Credential Manager).
5. Refresh the repo page on GitHub: the commit is there.
Mention once: the same actions exist as buttons in VS Code's Source Control panel; the course uses the commands so participants can read what an agent does.

### Segment 4: First agent run (18 min)
Facilitator demo first (6 min), then participants (12 min), guide §B3.
1. In the VS Code terminal, inside `excel-finance`: `opencode` → `/models` → pick `deepseek-v4.1-flash-free` (or the current zero-retention free model the facilitator names).
2. First prompt: *"Read AGENTS.md and README.md. In plain language, what is this project, and what does scripts/check_setup.py do?"* Point out: it **read files on its own**. That is why the data rule exists.
3. Second prompt (an agent that acts): *"Run the setup check and the tests, and tell me whether everything passed."* The agent asks permission to run commands; participants approve. Then open `output\setup_check.xlsx` in Excel: formulas in column G, Python values in H, "OK" in I.
4. Antigravity CLI, 3 minutes: `agy` → sign in with Google → same first prompt. Two agents, one `AGENTS.md`, one project.
5. The data rule, on one slide: *agents read everything in the folder; free tiers may keep what they read; strategic financial planning is Sensitive Lane → fictional or anonymised budgets only, and real finance files never live in an agent's folder.*
6. If the free model is rate-limited (shared office IP): switch model in `/models`, or `/connect` → Google with the Lesson 3 Gemini API key, or use `agy`.

### Segment 5: Green light (7 min)
- Everyone: `.\check_setup.ps1` → screenshot of the final line → post in the Teams channel.
- Green = **READY FOR THE MODULE**. Yellow warnings (Antigravity, optional extensions) are acceptable. Red = a fix call before Part 1.
- Close: what Part 1 starts from: this repo, this terminal, this agent.

---

## 6. Facilitator preparation checklist

- [ ] IT answers (admin rights, winget vs Scoop, network reachability), then fix the install path in the guide
- [ ] `starter/` published as a GitHub template repo; link inserted in `participant_setup_guide.md` (search for `TEMPLATE-LINK`)
- [ ] Dry run on a clean Windows machine, timing Part A (target ≤ 30 min) and Part B
- [ ] `check_setup.ps1` runs green on that machine under **Windows PowerShell 5.1** and PowerShell 7
- [ ] OpenCode: free model list and Zen data table re-checked; course default model confirmed; a test prompt answered without login
- [ ] Antigravity CLI: Windows install command confirmed on antigravity.google/docs; free sign-in works with a personal Google account; current quota noted
- [ ] Copilot Free: sign-in in VS Code works; note the current allowance
- [ ] Slides: toolchain map; Git in three sentences; the data rule
- [ ] Fallback demo machine ready (if a participant's machine cannot be fixed, they pair with a neighbour for Part 1)

---

## 7. Risks

| Risk | Mitigation |
|---|---|
| No admin rights on institutional machines | Ask IT 3 weeks before; Scoop path needs no admin; personal laptop as last resort |
| A free tier disappears or shrinks before the module (happened twice in 2026) | Three independent agents (OpenCode, Antigravity, Copilot); OpenCode can switch provider in one command; re-verify 1 week before |
| Shared per-IP limit on OpenCode free models | Personal Zen key; own Gemini API key via `/connect`; switch to `agy` |
| Real budget data enters an agent's context | Data rule in `AGENTS.md` and Segment 4; fictional sample data supplied; real files never in project folders |
| "Command not found" after install | New terminal; `check_setup.ps1` names the fix per line |
| Scripts blocked by execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` taught in Segment 2 |
| Workbook open in Excel when a script saves it | Script reports it plainly; rule in `AGENTS.md` |
| Participants skip pre-work | Segment 2 doubles as install time; fix calls before Part 1 |

---

## Sources (checked 16 October 2026)

- Gemini CLI → Antigravity CLI transition: [Google Developers Blog](https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/); [Gemini Code Assist consumer deprecation](https://developers.google.com/gemini-code-assist/docs/deprecations/code-assist-individuals); [gemini-cli discussion #28017](https://github.com/google-gemini/gemini-cli/discussions/28017); free tier limited to Flash models from 25 March 2026: [discussion #22970](https://github.com/google-gemini/gemini-cli/discussions/22970)
- Antigravity CLI install and sign-in: [Real Python](https://realpython.com/antigravity-cli/); free plan with weekly limits: [CodeAgentSwarm](https://www.codeagentswarm.com/en/guides/antigravity-plans-and-pricing)
- OpenCode install: [opencode.ai/docs](https://opencode.ai/docs/); free models and data handling: [OpenCode Zen docs](https://opencode.ai/docs/zen/); no-login free models and per-IP limits: [learnopencode.com](https://learnopencode.com/en/1-start/04a-free-models); free model list confirmed with `opencode models` (v1.19.2) on 16 Oct 2026
- Qwen Code free tier shutdown: [InventiveHQ](https://inventivehq.com/blog/qwen-code-still-free-2026-shutdown)
- GitHub Copilot plans: [GitHub Docs](https://docs.github.com/en/copilot/get-started/plans)
- Codex on ChatGPT Free: [CodeAgentSwarm](https://www.codeagentswarm.com/en/guides/codex-plans-and-pricing)
