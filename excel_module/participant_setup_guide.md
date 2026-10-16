# Excel for Finance: Setup Guide

This guide gets your computer ready for the three-part *Excel for Finance* module. You need no programming experience. Every command is given in full: copy it, paste it, press **Enter**.

- **Part A: before the setup session (about 30 minutes, on your own).** Accounts and installs.
- **Part B: in the setup session (60 minutes, together).** Terminal basics, Git and GitHub, your first AI agent, final check.

> **The data rule for this module.** The AI agents you install here are *Daily Driver* tools on free tiers. They read every file in the folder you start them in, and free services may keep what they read. Budgets and strategic financial planning are **Sensitive Lane** material. So in this module we work **only with fictional or anonymised data**, and real institutional finance files never go into a project folder where an agent runs.

**How to paste in the terminal:** right-click, or `Ctrl+V`. If several lines are pasted at once, PowerShell runs them one after the other.

---

## Part A: Before the session

### A1. Create a GitHub account (5 min)
1. Go to <https://github.com/signup> and create a free account. Use a username you would be happy to show colleagues.
2. Confirm your e-mail address.
3. When GitHub asks you to turn on **two-factor authentication**, do it (an authenticator app on your phone is easiest). Save the recovery codes somewhere safe.
4. Go to **Settings → Emails**, tick **Keep my email addresses private**, and copy the address that ends in `@users.noreply.github.com`. You need it in step A4.

You also need your **Google account** (the one you use for Gemini). If you created a Gemini API key in Lesson 3, keep it handy, since it can serve as a backup later.

### A2. Open the terminal and allow scripts (2 min)
1. Press the **Windows key**, type `Terminal`, and open **Terminal** (on older Windows 10: **Windows PowerShell**).
2. Paste this and press Enter, then answer `Y` if asked:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

This lets your own user account run the scripts we install. It does not affect other users and needs no admin rights.

### A3. Install the programs (10–15 min)
Paste these four lines. Each one downloads and installs a program. Accept any Windows prompts.

```powershell
winget install --id Git.Git -e --source winget
winget install --id Microsoft.VisualStudioCode -e --source winget
winget install --id OpenJS.NodeJS.LTS -e --source winget
winget install --id astral-sh.uv -e --source winget
```

| Program | What it is for |
|---|---|
| Git | Keeps the history of your project ("version control") |
| VS Code | The editor where you will see files, code, tables and the AI agent |
| Node.js | Needed to install the OpenCode agent |
| uv | Installs Python and the Excel/finance libraries for you |

**Now close the terminal window and open a new one.** Windows only sees newly installed programs in a new window.

> If `winget` is "not recognized", or Windows asks for an administrator password you don't have: stop here and follow the alternative instructions your facilitator sent for your institution's machines.

### A4. Tell Git who you are (1 min)
Replace the name and the e-mail (use the `noreply` address from A1), then paste:

```powershell
git config --global user.name "Your Name"
git config --global user.email "12345678+yourname@users.noreply.github.com"
git config --global init.defaultBranch main
```

### A5. Install Python and the two AI agents (5 min)

```powershell
uv python install 3.12
npm install -g opencode-ai
irm https://antigravity.google/cli/install.ps1 | iex
```

The first line installs Python, the second **OpenCode** (our main AI agent), the third **Antigravity CLI** (Google's AI agent).
**Close the terminal and open a new one again.**

### A6. Add the VS Code extensions (2 min)

```powershell
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension ms-toolsai.datawrangler
code --install-extension GrapeCity.gc-excelviewer
code --install-extension sst-dev.opencode
```

Then open VS Code, click the **Accounts** icon (bottom left) → **Sign in with GitHub** to use GitHub Copilot Free. (Optional; we'll also do it together.)

### A7. Quick check (1 min)

```powershell
git --version; code --version; node --version; uv --version; opencode --version; agy --version
```

You should see six version numbers (VS Code prints three lines). Take a screenshot and post it in the course Teams channel. If a line says *"not recognized"*, open a new terminal and try again. If it still fails, post the screenshot anyway, and we will fix it at the start of the session.

**Part A done.**

---

## Part B: In the session

### B1. Terminal basics (we do this together)

```powershell
pwd                                  # where am I?
cd $HOME\Documents                   # go to your Documents folder
mkdir ai-course                      # make a folder for the course
cd ai-course                         # go into it
ls                                   # what is here? (empty for now)
```

Useful keys: **Tab** completes folder and file names. **↑** brings back the previous command. **Ctrl+C** stops a running command. `cls` clears the screen.

### B2. Your own copy of the project, first commit, first push

1. Open the course template on GitHub: **TEMPLATE-LINK** → click **Use this template** → **Create a new repository**. Name it `excel-finance`, choose **Private**, click **Create repository**.
2. On your new repository's page click the green **Code** button and copy the HTTPS address.
3. In the terminal (still in `ai-course`):

```powershell
git clone https://github.com/YOUR-USERNAME/excel-finance.git
cd excel-finance
code .
```

4. In VS Code, open `README.md`, add a line at the end: `Setup completed by <your first name>`, and save (`Ctrl+S`).
5. Click the **Source Control** icon on the left (the branching symbol). You will see your change in green: **always look at a change before you save it into history.**
6. Back in the terminal (in VS Code: **Terminal → New Terminal**):

```powershell
git status                           # what has changed?
git add README.md                    # choose the change for the snapshot
git commit -m "My first commit"      # take the snapshot, with a note
git push                             # upload it to GitHub
```

The first `git push` opens your browser to sign in to GitHub. Approve it. Refresh your repository page on GitHub: your line is there.

### B3. Your first AI agent

In the VS Code terminal, inside `excel-finance`:

```powershell
opencode
```

1. Type `/models` and choose the model the facilitator names (default: **deepseek-v4.1-flash-free**).
2. Ask: *Read AGENTS.md and README.md. In plain language, what is this project, and what does scripts/check_setup.py do?*
3. Ask: *Run the setup check and the tests, and tell me whether everything passed.* The agent asks before it runs a command. Read what it wants to do, then approve.
4. Open `output\setup_check.xlsx` in Excel. Column G has live formulas, column H the values Python computed, and column I should say **OK**.
5. Leave OpenCode with `Ctrl+C` (or `/exit`).

Then try the Google agent with the same question:

```powershell
agy
```

Choose **Google sign-in**, approve in the browser, then ask the question from step 2.

### B4. Final check

```powershell
.\check_setup.ps1
```

It checks every program, extension and setting, installs the project's Python libraries, builds the test workbook, and writes `setup_report.txt`. Every red **[FAIL]** line says how to fix it.

**Done when the last line says `READY FOR THE MODULE`.** Post a screenshot of it in the Teams channel. Yellow **[WARN]** lines are optional extras.

---

## Cheat sheets

### PowerShell
| Command | Does |
|---|---|
| `pwd` | Show the current folder |
| `ls` | List files |
| `cd name` / `cd ..` / `cd $HOME` | Into a folder / up one / to your home folder |
| `mkdir name` | New folder |
| `code .` | Open the current folder in VS Code |
| `cat file.txt` | Show a text file |
| `cls` | Clear the screen |
| Tab / ↑ / Ctrl+C | Complete a name / previous command / stop |

### Git
| Command | Does |
|---|---|
| `git status` | What changed since the last snapshot? |
| `git diff` | Show the changed lines |
| `git add file` / `git add .` | Choose one file / everything for the next snapshot |
| `git commit -m "note"` | Take the snapshot |
| `git push` | Upload snapshots to GitHub |
| `git pull` | Download changes from GitHub |
| `git log --oneline` | List snapshots |

### Python in this project
| Command | Does |
|---|---|
| `uv sync` | Install or repair the project's libraries |
| `uv run python scripts\check_setup.py` | Run a script |
| `uv run pytest` | Run the budget-rule checks |

### OpenCode
| Key / command | Does |
|---|---|
| `/models` | Choose a model (free ones are marked) |
| **Tab** | Switch between **Plan** (only reads and proposes) and **Build** (can change files) |
| `/undo` | Undo the agent's last change |
| `/connect` | Use another provider, e.g. Google with your own Gemini API key |
| `/exit` or Ctrl+C | Leave |

---

## Troubleshooting

| You see | Do this |
|---|---|
| `... is not recognized as the name of a cmdlet` | Close the terminal, open a new one, try again. Still failing: the install did not finish; repeat that step |
| `running scripts is disabled on this system` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then try again |
| winget asks for an administrator password | Stop; use your institution's alternative instructions |
| `git push` is rejected / asks for a password | Close the terminal, run `git push` again and complete the browser sign-in |
| `Permission denied` when a script saves the workbook | The file is open in Excel: close it and run again |
| OpenCode: "rate limit" / "too many requests" | `/models` → pick another free model, or wait a minute. Many people on the same office network share one free limit |
| Antigravity: "quota exceeded" | Free weekly limit reached. Use OpenCode instead |
