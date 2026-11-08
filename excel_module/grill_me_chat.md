
❯ /grill-with-docs budget_planner_prompt.md

● Skill(grilling)
Successfully loaded skill

● Skill(domain-modeling)
Successfully loaded skill

  Searched for 1 pattern, ran 4 shell commands

Still reading the official EC workbook so I can ground my questions in facts, not ask you things I can look up.

  Ran 2 shell commands

I've read the prompt and both reference workbooks. A few facts I found, so I won't ask you about them:

- The official EC workbook (detailed-budget-table_he-ls-euratom_en.xlsm, v3.6) is macro-driven. It has a BE list with Role, Name, Acronym, Country and a 70%/100% funding-rate dropdown, plus a WP list. VBA buttons then generate one BEx sheet per beneficiary, with a section per WP and the fixed A–E cost categories. Effort is in person-months, and indirect costs are 25% × (A+C). Its own instructions say: "You must not change the structure of this workbook."
- Your manual template works on a different model. Tasks (T1.1…) are rows and up to 9 partners are columns. Effort is in working days, with a 215-day year used for daily rates. Travel is calculated with unit costs from C(2024)5405 (distance bands, accommodation and subsistence per country). Summaries are budget_sum and a travel PivotTable.
- The existing CONTEXT.md covers the course. "Detailed budgets" appears there only under the Optional Use-Case Phase.

Question 1: Who runs these skills, and where?

Some options:
- (a) You, in Claude Code, for real consortium work
- (b) Course participants, as material for the Optional Use-Case Phase
- (c) Both: you build it, and a simplified version goes to participants

This sets the tooling and the sensitivity model. Participants have Copilot/Gemini and no Claude Code. Your "the agent must never see partner names" rule also works very differently in each case.

My recommendation: (a) first, with (b) as a later spin-off. The skills would write the workbook with Python/openpyxl in Claude Code. The agent only ever handles structure: placeholders such as BE1…BEn and WP1…WPn, task codes, cost categories and formulas. A human fills in the real names and rates in Excel afterwards.

Which is it?

✻ Brewed for 1m 19s · done 11:05 AM

❯ a, I'll use it in Claude Code for real projects

Got it: (a), Claude Code, real projects.

Question 2: How does the custom workbook relate to the official EC detailed budget table?

The EC .xlsm is the submission document and must not be restructured. You also said its BE list and WP list must be part of every custom table. Some options:

- (a) Separate planning workbook. The skill builds a new workbook that contains copies of BE list and WP list, laid out exactly like the EC versions (same columns, same order), plus your planning sheets: task × partner effort, travel planner, summaries. Its outputs roll up to the EC cost categories (A.1 senior/junior…, B, C.1–C.3, D, E). A human then copies the numbers into the official workbook per BE and WP.
- (b) Extend the EC workbook. Add planning sheets inside the official .xlsm, linked to its BEx sheets. This breaks the "do not modify structure" rule, and the EC macros regenerate sheets, which would break the links.
- (c) Bidirectional. The custom workbook reads BE list/WP list from the filled-in EC file, so partners are entered once.

My recommendation: (a), with a twist. Make the BE list and WP list layouts match the EC ones so closely that a human can paste the same block into both files. They then stay the single, human-filled source of partner and WP names inside each file, and the agent never sees them. (c) sounds appealing, but cross-workbook links are fragile and tie you to one EC template version.

Do you agree?

✻ Worked for 10s · done 11:07 AM

❯ a, with identical BE list and WP list layouts

  Ran 2 shell commands

I added a Budget templating section to CONTEXT.md with five terms: Official Budget Table, Planning Workbook, Reference Lists, Beneficiary, Affiliated Entity.

Question 3: Which funding models must the skills cover?

The two models pull in different directions:
- Horizon Europe lump sum (your EC file and the LS guidance PDF): person-months, cost categories A–E, flat 25% indirect costs on A+C, per-WP lump sum shares.
- Horizon Europe actual costs (the AGA/MGA PDF): same categories, but real staff costs, time-sheets and the 215-day/1720-hour productive-time conventions.
- Erasmus+ lump sum (cooperation partnerships, CBHE…): its own Official Budget Table, different categories (staff cost per day by country group, travel and subsistence unit costs), and WP-level lump sums.

Your manual template mixes models: it budgets effort in working days with a 215-day year, and its travel tables use Erasmus+ unit costs (C(2024)5405).

The options:
- (a) Horizon Europe lump sum only, for now
- (b) Horizon Europe lump sum and Erasmus+ lump sum, both in v1
- (c) All three

My recommendation: (b). Introduce a Funding Profile concept: a per-programme definition of the cost categories, effort unit, indirect cost rule, unit-cost tables and Official Budget Table layout. The skill builds the Planning Workbook from one profile, so adding HE actual costs later is a new profile, not a new skill.

One sub-point: should the Funding Profile be chosen per proposal, or are mixed cases real? For example, an HE project budgeting travel with Erasmus+ unit costs as an internal estimate, like your manual template does.

✻ Brewed for 27s · done 11:11 AM

❯ b, one Funding Profile per proposal

  Ran 1 shell command

I added Funding Profile to the glossary.

Question 4: Can a Funding Profile include estimation aids from outside its own rules?

Under Horizon Europe lump sum, you can estimate travel however you like. The Official Budget Table only wants C.1 items × average cost per item. Your manual template estimates travel with the Commission's travel and subsistence unit costs (C(2024)5405): distance bands, inter-Member State rail, and accommodation and subsistence per country. That is a sound, defensible method for an HE proposal too. With "one Funding Profile per proposal", the question is whether the HE profile may still offer that travel planner.

I'd split two things:
- Funding Profile rules: what the Official Budget Table needs (categories, effort unit, indirect rate). Fixed per profile.
- Estimation Method: how the Planning Workbook arrives at a category's number. For example, a travel planner using C(2024)5405 unit costs, a daily-rate staff calculation, or a plain items × cost-per-item entry. These are reusable modules that any profile may switch on.

My recommendation: make Estimation Methods a separate, profile-independent catalogue. Each profile declares which methods it allows and which one is the default. So the HE lump sum profile defaults to the C(2024)5405 travel planner, and the Erasmus+ profile uses it as mandatory, since there the unit costs are the actual rules.

Do you agree with that split?

✻ Brewed for 17s · done 11:12 AM

❯ yes, separate Estimation Method catalogue

  Ran 1 shell command

I added Estimation Method to the glossary.

Question 5: At what grain is effort planned?

The two reference files plan effort at different levels of detail:
- Official Budget Table (HE): person-months per BE × WP × staff category (senior, junior, technical, administrative, others, A.2–A.4). There are no tasks.
- Your manual template: working days per Task × partner. Tasks are rows under WPs, partners are columns, and there is no staff category. Each partner has one daily rate (AA$1 × days).

The options:
- (a) WP × BE × staff category, mirroring the Official Budget Table exactly. Easy to transfer, but it loses the task detail evaluators and partners actually discuss.
- (b) Task × BE, as in your template, with one blended rate per BE. Familiar, but the Official Budget Table's staff-category split must then be guessed at transfer time.
- (c) Task × BE × staff category. Tasks roll up to WPs, staff categories map 1:1 to the Official Budget Table's A-lines, and a summary sheet produces exactly the BE × WP × category grid a human types into each BEx sheet.

My recommendation: (c), with the staff categories coming from the Funding Profile. HE gives its five A.1 lines plus A.2–A.4. Erasmus+ lump sum gives its own staff categories (manager, researcher/teacher, technician, administrative), each with a daily rate per country group. To keep the sheet usable, show BEs as column blocks with a category sub-column only where the profile has more than one category. Tasks get a Task List sheet: human-filled task codes and titles, but no sensitive data.

Two sub-points:
1. Do you want task-level planning at all, or is WP-level enough for some proposals? If so, Task List would become an optional Estimation Method.
2. Are task titles sensitive in your context? Unsubmitted proposal content arguably is.

✻ Cogitated for 17s · done 11:13 AM

❯ c, task planning optional, task titles human-filled only

  Ran 1 shell command

I added Staff Category and Task List to the glossary.

Question 6: Where exactly is the sensitivity line, i.e. what may the agent ask?

To build a Planning Workbook, the agent needs some shape information. I'd sort it like this:

┌─────────────────────────────────┬───────────────────────────────────────────────────────┬────────────────────────────────────────────────────────────────────┐
│            Parameter            │                      Needed for                       │                           Proposed class                           │
├─────────────────────────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Funding Profile                 │ everything                                            │ Ask                                                                │
├─────────────────────────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Number of BEs, AEs per BE       │ sheet sizing, column blocks                           │ Ask (a count reveals nothing)                                      │
├─────────────────────────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Number of WPs, tasks per WP     │ rows, Task List                                       │ Ask                                                                │
├─────────────────────────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Project duration (months)       │ timelines, daily-rate maths                           │ Ask                                                                │
├─────────────────────────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Estimation Methods to switch on │ which sheets exist                                    │ Ask                                                                │
├─────────────────────────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ BE countries                    │ Erasmus+ country-group rates, HE A.4 rate, travel     │ Never ask: human picks from a dropdown in BE list; formulas look   │
│                                 │ unit costs                                            │ up the rest                                                        │
├─────────────────────────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Names, acronyms, WP and task    │ labels                                                │ Never ask: human-filled in the Reference Lists and Task List       │
│ titles                          │                                                       │                                                                    │
├─────────────────────────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Salaries, daily rates, PM       │ costs                                                 │ Never ask: human-filled input cells                                │
│ figures                         │                                                       │                                                                    │
├─────────────────────────────────┼───────────────────────────────────────────────────────┼────────────────────────────────────────────────────────────────────┤
│ Call/topic ID, budget ceiling   │ caps, checks                                          │ Never ask: human-filled input cell on a cover sheet                │
└─────────────────────────────────┴───────────────────────────────────────────────────────┴────────────────────────────────────────────────────────────────────┘

So the rule becomes: the agent asks only for counts and choices, never identifiers or amounts. Anything country-, rate- or name-dependent must be resolved by formulas from human-filled cells.

There's a second side to this: the agent must also never read a filled-in workbook. Your earlier sanitisation session showed that filled workbooks leak names through comments, document metadata and pivot caches. So the skills only build or rebuild blank workbooks, and any later "add a WP" operation either works on the blank structure or is a macro the human runs.

My recommendation: adopt the table and the rule above, including the "never read a filled workbook" side.

Do you agree, or is anything misclassified? Country is the debatable one: knowing "BE3 is in Hungary" is mildly identifying.

✻ Brewed for 19s · done 11:13 AM

❯ yes, adopt the table, country stays human-filled

  Ran 1 shell command

I added Shape Parameters and Human Inputs to the glossary.

ADR offer: "The agent never opens a filled-in Planning Workbook" meets all three ADR tests. It is hard to reverse, because it shapes every later skill. A future reader would ask why the agent can't simply add a WP. And it is a real trade-off: convenience against confidentiality. I'd write it as docs/adr/0001-agent-never-reads-filled-planning-workbooks.md. Shall I? You can answer together with the question below.

Question 7: How does a filled-in workbook change shape after the agent hands it over?

This follows directly from the rule. Consortia change mid-proposal: a partner joins, a WP is split, tasks get added. Since the agent can't touch a filled-in workbook, something else has to absorb those changes:

- (a) Spare capacity. Build with headroom (e.g. 15 BE slots, 10 WPs, 8 tasks per WP). Unused slots stay blank and are hidden or greyed out, and all formulas already cover them. No macros, stays .xlsx, robust. But the sheets get wide, and there is a hard ceiling.
- (b) VBA macros, EC style: "Add BE", "Add WP", "Add task" buttons. Flexible, but .xlsm means security prompts, Mac/Excel-online gaps and fragile code. The agent also has to write VBA it can't test against filled data.
- (c) Excel Tables with structured references and dynamic arrays. The Reference Lists and Task List are real Excel Tables, so adding a row auto-extends them, and summaries use FILTER/UNIQUE/SUMIFS over those Tables. Needs Excel 365/2021, but no macros. The BE column blocks remain the hard part, since columns don't auto-extend the way rows do.
- (d) Rebuild and re-paste. The human asks the agent for a fresh blank workbook with the new Shape Parameters and pastes their inputs back in, block by block, into identical layouts.

My recommendation: (c) + (a) + (d), no macros.
- Rows grow via Tables: BEs, AEs, WPs and tasks.
- Per-BE columns get spare capacity up to a profile-defined maximum.
- Big reshapes go through (d). That works because the Reference Lists and input blocks keep stable, documented layouts.

Do you have colleagues on Excel 2016 or Mac who would break (c)? And on macros, your prompt lists them as a component. Is that a hard requirement, or one candidate tool?

✻ Sautéed for 22s · done 11:14 AM

❯ yes write the ADR, c+a+d, no macros

  Read 1 file, ran 1 shell command

I wrote two ADRs:
- docs/adr/0001-agent-never-reads-filled-planning-workbooks.md
- docs/adr/0002-no-macros-tables-spare-capacity-rebuild.md

I recorded "no macros" separately because it deliberately departs from the EC pattern and from your original component list. Someone will suggest macros again unless the reason is written down.

Question 8: What must the Planning Workbook output so the transfer into the Official Budget Table is mechanical?

Every HE BEx sheet asks, per WP and per cost line, for ITEMS and COST PER ITEM. Total and indirect costs are calculated there. The Erasmus+ table is structured differently but has the same idea. Your manual template's outputs (budget_sum, the travel pivot) are organised by task × partner, so the transfer means mental re-aggregation.

I propose a Transfer View: one block per Beneficiary (and AE), laid out row-for-row like that profile's BEx section. For each WP it shows the cost category lines with ITEMS and COST PER ITEM, already in the Official Budget Table's units:
- PM for the A-lines
- subcontract count for B
- trip count × average cost for C.1
- and so on

The human copies the block straight across. Because COST PER ITEM is an average, it is computed as total ÷ items, exactly the way the EC instructions describe.

Next to the Transfer View I'd add the internal summaries you already rely on. These mirror the EC's own summary sheets so you can check your figures against them after transfer:
- Lump sum breakdown: BE × WP
- Person-months overview: BE × WP
- Summary per WP

The travel PivotTable would become a formula-based summary. PivotTables need a manual refresh, and your earlier session showed that their caches hold data and break blank-state guards.

My recommendation: the Transfer View plus the three EC-mirroring summaries, all formula-based, with no PivotTables anywhere.

Do you agree? And is there any summary from your manual template you'd miss, such as the % share of effort and budget per WP that budget_sum shows?

✻ Baked for 35s · done 11:17 AM

❯ yes, Transfer View plus EC summaries, keep % shares


Question 9: How are staff effort and rates entered?

The units differ between sources:
- HE lump sum wants person-months × cost per PM. The AGA defines the annual productive time as 1,720 hours, so 1 PM = 143.33 hours. Some partners think in days (≈ 17.9 days per PM at 215 days a year).
- Erasmus+ lump sum wants days × the daily rate of the Staff Category in the BE's country group.
- Your manual template uses days per task × one daily rate per partner (a "daily rate" helper converts monthly cost with 215/12).

My proposal:
- A Rate Table sheet: one row per Beneficiary/AE (driven by the BE list Table), one column per Staff Category. All rates are Human Inputs in the profile's native unit: monthly cost for HE, daily rate for Erasmus+. For Erasmus+, the rate can instead be derived from the country dropdown via the profile's country-group table, with the human only overriding.
- Effort is entered in the profile's native unit: PM for HE, days for Erasmus+. The HE profile gets an optional "days → PM" helper column with the conversion factor (215 days or 1,720 h) as a visible, editable Profile Constant, not buried in formulas like the manual template's 215/12.

The alternative is to always plan in days and convert. That's familiar to you, but it introduces rounding (your template rounds to whole days) and a hidden convention reviewers may question.

My recommendation: native units, a human-filled Rate Table, and visible Profile Constants.

Do you agree?

✻ Brewed for 18s · done 11:18 AM

❯ yes, native units with visible Profile Constants

  Ran 1 shell command

I added Rate Table and Profile Constant to the glossary.

Question 10: How are Funding Profiles stored and kept current?

A profile's reference data changes over time:
- The Official Budget Table is versioned. Yours is v3.6, valid for topics opening from 12 Dec 2025.
- Unit-cost decisions get amended (C(2024)5405 replaced an earlier decision).
- Erasmus+ daily rates and country groups change with the Programme Guide year.

One fact: docs/ holds the HE lump sum Official Budget Table but no Erasmus+ Official Budget Table and no Erasmus+ Programme Guide. That's a gap for building the v1 profile.

My proposal:
- Each Funding Profile is a data definition inside the skill, not code. It holds:
  - a small manifest: name, Official Budget Table version, valid-from date, source documents with links
  - the cost category / Staff Category list
  - the Profile Constants
  - the reference tables as CSV (country list, country groups, unit costs)
- Each built Planning Workbook carries a provenance cell on its cover sheet, e.g. "HE-LS profile v3.6 / C(2024)5405, built 2026-11-02". A reviewer then knows which rules it embodies.
- Updating a profile is its own skill step. The agent extracts the new tables from the official document, diffs them against the stored version, and a human approves before the profile version bumps. Old versions are kept, since a proposal in progress must be rebuildable under the rules it started with.

My recommendation: that design, plus a ticket to obtain the Erasmus+ lump sum budget table and Programme Guide as source documents.

Two sub-questions:
1. Which Erasmus+ action(s) matter to you? KA2 Cooperation Partnerships and CBHE use different lump sum models, so this may really be two profiles.
2. Do you agree with keeping old profile versions?

✻ Cogitated for 18s · done 11:18 AM

❯  KA2 Cooperation Partnerships, keep the  old profile versions

● Web Search("Erasmus+ 2026 Programme Guide KA220 cooperation partnerships lump sum 120000 250000 400000 budget distribution work packages")
Did 1 search in 10s

  Ran 1 shell command

I updated the Funding Profile entry: v1 is now HE lump sum + KA220, versions are kept, and each workbook records which version it was built from.

KA220 changes the picture, so I checked it. KA220 Cooperation Partnerships has no detailed Official Budget Table at all. The applicant picks one fixed lump sum (€120,000, €250,000 or €400,000) and splits it across work packages in the application form. National agency guidance also asks for the split per WP and activity, with project management as its own WP. The Programme Guide prevails over the lump sum handbook. I didn't find any official per-WP share limits, so the 2026 Programme Guide still needs checking (CMEPIUS 2026 (https://www.cmepius.si/wp-content/uploads/2026/02/Cooperation-Partnerships-2026.pdf), Commission lump sum handbook (https://www.erasmusplus.it/wp-content/uploads/2026/07/Handbook-on-the-lump-sum-funding.pdf), NL NA protocol 2026 (https://www.erasmusplus.nl/sites/default/files/2026-02/Protocol%20KA220%20Call%202026%20-%20SCH-VET-HED-ADU.pdf)).

This means:
- For KA220, staff daily rates, country groups and travel unit costs are not rules. They are just Estimation Methods for an internal estimate.
- The target is a fixed total to allocate, not a sum that comes out of the calculation.

Question 11: How does the KA220 profile plan against a fixed tier?

- (a) Top-down. Pick the tier, then distribute percentages across WP × BE. Fast, but you can't defend the figures.
- (b) Bottom-up, then fit. Estimate costs per WP × BE with Estimation Methods (staff days × rate, travel planner, other costs). The Check Summaries then compare the total against the chosen tier and show the gap. The human adjusts until it fits, and the Transfer View outputs the per-WP amounts the application form wants.
- (c) Both views side by side.

My recommendation: (b). It reuses the same Estimation Methods as HE and gives you a cost-reasonableness justification for evaluators. The tier becomes a Human Input with a dropdown of the three values.

This also forces a naming fix. "Official Budget Table" is wrong for KA220. I'd rename the general concept Submission Budget: whatever budget the funder actually receives. For HE lump sum that is the Official Budget Table; for KA220 it is the application form's WP budget section. The Transfer View targets the Submission Budget.

Do you agree with (b) and the rename?

Sources:
- CMEPIUS – Cooperation Partnerships 2026 (https://www.cmepius.si/wp-content/uploads/2026/02/Cooperation-Partnerships-2026.pdf)
- Handbook on the lump sum funding (2026) (https://www.erasmusplus.it/wp-content/uploads/2026/07/Handbook-on-the-lump-sum-funding.pdf)
- Erasmus+ NL – Protocol KA220 Call 2026 (https://www.erasmusplus.nl/sites/default/files/2026-02/Protocol%20KA220%20Call%202026%20-%20SCH-VET-HED-ADU.pdf)
- Erasmus+ NL – Handbook on the lump sum funding model 2025 (https://www.erasmusplus.nl/sites/default/files/2025-01/Handbook%20on%20the%20lump%20sum%20funding%20model%202025%20final.pdf)

✻ Cooked for 48s · done 11:21 AM

❯ b, rename to Submission Budget

  Ran 1 shell command

I updated the glossary:
- Added Submission Budget.
- Official Budget Table is now one kind of Submission Budget.
- Added Lump Sum Tier.
- Planning Workbook, Transfer View and Check Summaries now point at the Submission Budget.

Question 12: How do the skills break down?

Your prompt says "skills", plural. Based on what we've settled, I see these jobs:

1. Build: interview for Shape Parameters, then generate a blank Planning Workbook from a Funding Profile and the chosen Estimation Methods.
2. Rebuild: same as Build, with new Shape Parameters and the same profile version, plus a re-paste guide that maps old input blocks to new ones (ADR-0002, option d).
3. Profile update: extract tables from a new official document, diff them, get human approval, bump the version.
4. Verify: fill a disposable copy with synthetic data (fake BEs, round-number rates), recalculate in Excel, and assert that totals reconcile, no #N/A appears, and the Transfer View matches the Check Summaries. Your earlier session had this, but its expectations got edited to match the outputs, so it proved nothing. Here the expectations come from an independent hand calculation.

Packaging options:
- (a) One skill, budget-planner, with sub-commands (build / rebuild / update-profile / verify) and shared reference folders: profiles/, methods/, a Python generator library.
- (b) Four skills sharing a library.
- (c) Two skills: budget-planner (build, rebuild, verify) and budget-profile-maintainer (update). Maintenance is rare, happens at a different time, and needs the official PDFs.

My recommendation: (c).
- Build always ends by running Verify automatically, so there's no workbook without a passed synthetic check.
- The Estimation Methods and Funding Profiles live as data plus Python modules in one shared folder, which both skills read.
- Rebuild is just Build with a "previous shape" input, not a separate skill.

Do you agree? And where should the skills live: this repo's .claude/skills/, or your user-level ~/.claude/skills/ so they work in any project folder?

✻ Cooked for 25s · done 11:22 AM

❯ In the repo's .claude/skills. But wouldn't a single 'budget planner' be too large a monolith to cover all the build, rebuild and verification steps, and should it not be broken down into more specialised skills?

Fair challenge. Here's why I'd still keep build, rebuild and verify together, and where the split should happen instead.

What actually makes a skill too big is the instruction text the agent has to load and follow, not the number of jobs it does. Skills support progressive disclosure: a short SKILL.md holds the workflow and the hard rules (the Shape Parameters / Human Inputs boundary, the no-macros rule), and links to BUILD.md, REBUILD.md and VERIFY.md. Each of those loads only when that step runs. The heavy lifting (sheet builders, formulas, Excel recalculation, assertions) sits in a Python package, not in prose. That package is where modularity matters, and it would be split by concept:
- profiles/
- methods/ (one module per Estimation Method)
- sheets/ (Reference Lists, Task List, Rate Table, Transfer View, Check Summaries)
- verify/

Where splitting skills pays off: when jobs have different triggers, inputs or timing. Profile maintenance passes all three tests: it is rare, needs official PDFs, and needs a human approval gate. That's why it's separate.

Where splitting hurts: build, rebuild and verify share the same inputs and must always run in sequence. Separate skills invite exactly the failure from your last session: a workbook delivered without an independent check, or a check run on its own and bent to fit. Keeping verify inside the build flow makes "no workbook without a passed check" structural, not a matter of discipline. Verify is still callable on its own, but as a script that both skills use (the profile maintainer needs it too, to regenerate and check after a version bump), not as a third skill.

So my recommendation stands: two skills in .claude/skills/, budget-planner and budget-profile-maintainer, with a thin SKILL.md, per-step reference files and a modular shared Python package.

If you still prefer finer skills, the split I'd accept is three: planner (build + rebuild), verifier and profile maintainer, with planner required to call verifier before handing over. Two or three?

✻ Crunched for 15s · done 11:25 AM

❯ two skills, verify stays inside the build flow

  Ran 1 shell command

I added Synthetic Check to the glossary.

Question 13: What is the Synthetic Check's independent oracle?

Your earlier session failed this way: the expectations came from reading the workbook's own outputs, then got edited to match them. The oracle has to be computed from a different source than the formulas under test. Options:

- (a) Python reference model. A small pure-Python implementation of each Funding Profile's arithmetic, e.g. total = Σ(items × cost) + 25% × (A+C), and each Estimation Method, e.g. travel = trips × band amount + nights × accommodation + days × subsistence. It's fed the same synthetic inputs, and its results are compared cell by cell with Excel's recalculated values. It's independent because it never looks at a formula string.
- (b) Hand-computed golden fixtures. For each profile, one small fixed scenario (2 BEs, 2 WPs, 1 AE, a few trips) with expected totals worked out by hand once and committed. Fully independent, but it only covers that one shape.
- (c) Both. Golden fixtures pin the reference model to reality. The reference model then checks every shape you actually build, e.g. 9 BEs × 6 WPs with spare capacity.

Beyond the numbers, the check also asserts structural invariants:
- no error values anywhere
- blank workbook shows blanks, not 0s or dashes
- the Transfer View equals the Check Summaries
- Reference List layout matches the EC BE list/WP list cell-for-cell
- no identifiers in document properties
- no PivotTables or VBA

My recommendation: (c), plus the invariants. One more rule: a failing check may never be fixed by editing the expected values unless a human approves it. Do you agree?

✻ Worked for 18s · done 11:26 AM

❯ c, with human approval for expectation changes

  Ran 1 shell command

I updated Synthetic Check and added Golden Scenario to the glossary.

Question 14: What does the workbook check live, for the human filling it in?

The Synthetic Check proves the formulas are right. It doesn't stop a human from entering nonsense later, and the agent will never see the filled workbook. So the workbook has to guard itself. Candidate Input Guards, all formula-based:

1. Data validation: dropdowns for country, funding rate (70%/100%), Lump Sum Tier and Staff Category; non-negative decimals for effort and rates; task and WP codes only from the Task List / WP list.
2. Completeness flags (conditional formatting): a BE with effort but no rate, a BE with a rate but no country, a task with effort but no WP, a trip with no destination country.
3. Plausibility warnings (soft, never blocking):
   - a PM cost far outside the band for its country
   - a BE's effort exceeding duration × 1 FTE per Staff Category
   - one WP over ~X% of the total
   - travel per trip far above unit costs
4. Rule checks per profile:
   - HE: indirect = 25% × (A+C), and subcontracting share shown
   - KA220: gap to the tier, project management WP share shown
5. A Checks panel on the cover sheet: one line per guard with OK / ⚠ / ✖, so the human sees overall readiness at a glance before transferring.

The thresholds in (3) would be Profile Constants, visible and editable, not hidden.

My recommendation: all five, with plausibility warnings kept soft. Do you agree? And do you have real thresholds from experience to seed (3)? For example, "evaluators question a WP over 30%" or "PM costs above €X raise flags". Otherwise I'd leave them as human-filled Profile Constants with no default.

✻ Baked for 17s · done 11:27 AM

❯ all five, thresholds human-filled with no defaults

  Ran 1 shell command

I added Input Guards to the glossary.

Question 15: What does the handover package contain?

The human receives the blank workbook and fills it in alone. Last time you got four files: the workbook, INSTRUCTIONS.md, REPORT.md and changelog.json. Proposal:

1. The Planning Workbook (.xlsx), whose Cover sheet holds:
   - provenance (profile version, build date, Shape Parameters)
   - the Checks panel
   - a short fill-in order: Reference Lists → Task List → Rate Table → effort → Estimation Method sheets → Checks → Transfer View
   - a colour legend for input / derived / check cells

   So the essential guidance travels inside the file.
2. A fill-in guide (Markdown, or a PDF/Word copy for colleagues). Per sheet: what to enter, in what unit, which source (e.g. "PM cost from your finance office, in € per PM"), and how to transfer the Transfer View into the Submission Budget, field by field.
3. A Synthetic Check report: which shape was checked, Golden Scenario pass, invariants pass, and the reference-model diff count.
4. On Rebuild only, a re-paste guide: old block → new block mappings.

No separate changelog, since a generated workbook has nothing to change from. Also a consistent cell colour convention across all profiles: inputs in light yellow, derived in white, guards in conditional colours. If your office already has a convention, it should go into the skill instead.

My recommendation: items 1–4, with the Cover sheet as the primary guide and the Markdown fill-in guide as backup.

Do you agree? Do you have a colour convention? And who fills these in: you alone, or also partners' finance officers? That decides whether the guide needs to be bilingual (HU/EN).

✻ Churned for 17s · done 11:27 AM

❯ yes 1–4, use your colours, English only

  Ran 1 shell command

I added Cover Sheet and Handover Package to the glossary.

Question 16: Which Estimation Methods go into the v1 catalogue?

Mapped against the HE cost categories and what your manual template already does:

┌─────┬────────────────────────────────────────────────────────────────┬────────────────┬────────────────────┬──────────────┬─────────────────────────────────┐
│  #  │                       Estimation Method                        │     Covers     │       HE LS        │    KA220     │             Source              │
├─────┼────────────────────────────────────────────────────────────────┼────────────────┼────────────────────┼──────────────┼─────────────────────────────────┤
│ 1   │ Staff effort (Task/WP × BE × Staff Category × Rate Table)      │ A.1–A.4 /      │ default            │ default      │ both files                      │
│     │                                                                │ staff          │                    │              │                                 │
├─────┼────────────────────────────────────────────────────────────────┼────────────────┼────────────────────┼──────────────┼─────────────────────────────────┤
│ 2   │ Travel planner: trips with C(2024)5405 distance bands, rail,   │ C.1 / travel   │ default            │ default      │ your template                   │
│     │ accommodation and subsistence per country                      │                │                    │              │                                 │
├─────┼────────────────────────────────────────────────────────────────┼────────────────┼────────────────────┼──────────────┼─────────────────────────────────┤
│     │ Event planner: meetings or conferences with organiser costs,   │                │                    │              │ your template's top block       │
│ 3   │ attendees, registration fees, feeding trips into #2 and        │ C.1 + C.3      │ optional           │ optional     │ (organiser, min. attendees,     │
│     │ meeting services into C.3                                      │                │                    │              │ reg. fee)                       │
├─────┼────────────────────────────────────────────────────────────────┼────────────────┼────────────────────┼──────────────┼─────────────────────────────────┤
│ 4   │ Equipment depreciation: purchase cost × % project use × %      │ C.2            │ optional           │ optional     │ EC Depreciation costs sheet     │
│     │ useful life                                                    │                │                    │              │                                 │
├─────┼────────────────────────────────────────────────────────────────┼────────────────┼────────────────────┼──────────────┼─────────────────────────────────┤
│ 5   │ Itemised list: free rows of description × qty × unit cost,     │ B, C.3, D.2,   │ default for the    │ default for  │ EC BEx lines                    │
│     │ tagged with category, BE and WP                                │ anything else  │ rest               │ the rest     │                                 │
├─────┼────────────────────────────────────────────────────────────────┼────────────────┼────────────────────┼──────────────┼─────────────────────────────────┤
│ 6   │ Financial support to third parties and other topic-specific    │ D.1, D.3–D.5   │ optional (only if  │ n/a          │ EC                              │
│     │ D-lines                                                        │                │ the topic allows)  │              │                                 │
└─────┴────────────────────────────────────────────────────────────────┴────────────────┴────────────────────┴──────────────┴─────────────────────────────────┘

Every method outputs (items, total) per BE × WP × category line. The Transfer View can then compute ITEMS and COST PER ITEM uniformly, whichever method produced them.

My recommendation: #1, #2, #4 and #5 in v1. #3 is valuable but complex, since it cross-feeds two categories. #6 is rare. Both go to v2 as separate tickets, with #5 covering those lines meanwhile.

Do you agree? And is the event planner something you use on most proposals? If so, it belongs in v1.

✻ Baked for 18s · done 11:28 AM

❯ yes #1, #2, #4, #5 in v1, rest v2

  Ran 1 shell command

I updated Estimation Method with the common output (items + total per BE × WP × line) and the v1 list.

Question 17: How are Affiliated Entities and spare capacity sized?

Two related sizing questions, since columns can't auto-grow (ADR-0002):

AEs. The HE BEx sheet puts the AE beside its BE (BE / AE / BE+AE column groups), and the Lump sum breakdown shows BE+AE together. Options:
- (a) An AE is a row in the BE list Table and gets its own column block in effort sheets, exactly like a BE. The Transfer View shows it in the AE columns of its parent's block.
- (b) An AE is merged into its BE for planning.

My recommendation: (a). AEs have their own rates and countries, and HE requires separate AE figures.

Spare capacity. Column blocks per BE/AE are pre-built up to a maximum. Rows (WPs, tasks, trips, items) grow via Tables, so they need no maximum. I'd make the maximum a Shape Parameter with a profile default, built as asked count + headroom:
- HE LS: asked + 3 (consortia grow during drafting)
- KA220: asked + 2 (smaller, more stable consortia; minimum 3 partners from 3 countries)

Unused blocks are greyed out and collapsed via outline grouping, which is not hidden, so nobody misses them. Formulas already include them.

My recommendation: (a), and headroom as a profile default the agent states and lets you override at build time.

Do you agree, or would you rather fix a hard maximum, e.g. always 15 slots?

✻ Cogitated for 19s · done 11:29 AM

❯ a, headroom as profile default with override

  Ran 1 shell command

I added headroom to Shape Parameters. I think we've covered the decision tree. Here's the shared understanding to confirm before you run to-spec.

Goal: two skills in .claude/skills/, used by you in Claude Code for real proposals.
- budget-planner: asks for Shape Parameters, builds or rebuilds a blank Planning Workbook from one Funding Profile and the chosen Estimation Methods, and always runs the Synthetic Check before handover.
- budget-profile-maintainer: extracts reference tables from new official documents, diffs them, and bumps the profile version only after your approval. Old versions are kept.

Main decisions:
1. Separate Planning Workbook. It never modifies the Submission Budget, and a human transfers the figures.
2. Reference Lists (BE list, WP list) match the HE Official Budget Table cell for cell. The Task List is optional.
3. Funding Profiles in v1: HE lump sum and Erasmus+ KA220. KA220 is estimated bottom-up against a Lump Sum Tier.
4. Estimation Method catalogue in v1: staff effort, C(2024)5405 travel planner, equipment depreciation, itemised list. The event planner and D-lines come in v2.
5. Effort grain: Task (or WP) × BE/AE × Staff Category, in native units. Rates come from a human-filled Rate Table, and conventions are visible Profile Constants.
6. Sensitivity: the agent asks only Shape Parameters, never Human Inputs, and never opens a filled workbook (ADR-0001).
7. No macros: Tables and dynamic arrays, spare column capacity (profile headroom with override), and rebuild-and-re-paste (ADR-0002). Requires Excel 2021 or 365.
8. Outputs: a Transfer View per BE/AE, Check Summaries mirroring the EC sheets plus % shares, all formula-based with no PivotTables.
9. Synthetic Check: a Python reference model pinned to hand-computed Golden Scenarios, plus structural invariants. Expected values change only with your approval.
10. Input Guards: five kinds, with plausibility thresholds human-filled and no defaults. A Checks panel sits on the Cover Sheet.
11. Handover Package: workbook with Cover Sheet, an English fill-in guide, the check report, and a re-paste guide on rebuild. Light-yellow inputs.

Open items for tickets, not decisions:
- Source documents: add the Erasmus+ 2026 Programme Guide and the KA220 application form budget section to excel_module/docs/. Also confirm from the Guide whether any per-WP share limits exist.
- Golden Scenarios: you need to hand-compute one per profile.
- Your manual Blank_Project_Budget_Template: it stays a reference only, and the travel tables are re-extracted from C(2024)5405 itself.

Files written this session:
- CONTEXT.md, new "Budget templating" section (a