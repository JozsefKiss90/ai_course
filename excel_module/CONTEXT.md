# Budget Templating (excel_module)

The ubiquitous language for the budget templating skills: agent skills that build project-specific Excel Planning Workbooks for Horizon Europe and Erasmus+ proposals without the agent ever handling project or consortium data.

## Language

**Submission Budget**:
Whatever budget the funder actually receives for a proposal, in the funder's own format. For Horizon Europe lump sum it is the Official Budget Table; for Erasmus+ KA220 it is the work-package budget section of the application form. A human transfers figures into it from the Planning Workbook.
_Avoid_: Final budget, official budget

**Official Budget Table**:
A Submission Budget that is a Commission-issued, macro-enabled detailed budget workbook (e.g. the Horizon Europe lump sum detailed budget table). Its structure is never modified.
_Avoid_: EC template, the xlsm

**Planning Workbook**:
The project-specific Excel workbook a templating skill builds for one proposal. It is where effort and costs are estimated, and its outputs roll up to the Submission Budget's categories. It is separate from the Submission Budget and is never submitted.
_Avoid_: Custom template, budget template, budget table

**Reference Lists**:
The `BE list` and `WP list` sheets, present in every Planning Workbook with exactly the same layout as in the Horizon Europe Official Budget Table, so a human can paste the same block into both. They are the only place partner and work package names are entered, always by a human.

**Beneficiary (BE)**:
A consortium partner that signs the grant agreement, identified in a Planning Workbook only by its placeholder code (BE1…BEn) until a human fills in the Reference Lists.
_Avoid_: Partner (in the workbook), participant

**Affiliated Entity (AE)**:
An entity linked to a Beneficiary that carries out part of its work and declares its own costs; listed under its Beneficiary in the `BE list`.

**Funding Profile**:
The definition of one funding model that a Planning Workbook is built from: its cost categories, effort unit, indirect cost rule, unit-cost tables and the layout of its Submission Budget. Exactly one Funding Profile per proposal. v1 covers Horizon Europe lump sum and Erasmus+ KA220 Cooperation Partnerships. Profiles are versioned against their source documents; old versions are kept so a proposal can be rebuilt under the rules it started with, and every Planning Workbook records the profile version it was built from.
_Avoid_: Programme, call type, template type

**Estimation Method**:
A reusable way of arriving at the figure for one cost category in a Planning Workbook — e.g. a travel planner priced with the Commission's travel and subsistence unit costs, a daily-rate staff calculation, or a plain items × cost-per-item entry. Methods form a catalogue independent of any Funding Profile; each profile declares which methods it allows and which is its default (or mandatory, where the method *is* the programme's rule). Whatever its internals, every method yields number of items and total cost per Beneficiary × work package × cost line, which is all the Transfer View consumes. v1 catalogue: staff effort, travel planner, equipment depreciation, itemised list; event planner and topic-specific D-lines follow later.
_Avoid_: Calculator, module, sheet type

**Staff Category**:
A personnel cost line defined by the Funding Profile — for Horizon Europe the A.1 lines (senior, junior, technical, administrative, others) plus A.2–A.4; for Erasmus+ its own categories with daily rates per country group. Effort is planned per Task (or WP) × Beneficiary × Staff Category.

**Task List**:
An optional sheet, alongside the Reference Lists, holding task codes and titles under each work package. Titles are filled in by a human only. When a Planning Workbook has no Task List, effort is planned at work-package level.
_Avoid_: Task breakdown, WBS

**Shape Parameters**:
The only things an agent may ask about a proposal: the Funding Profile, counts (Beneficiaries, Affiliated Entities per Beneficiary, work packages, tasks per work package), project duration in months, which Estimation Methods to switch on, and the spare-capacity headroom (a Funding Profile default the agent states and the human may override). Affiliated Entities count like Beneficiaries for capacity: each gets its own column block. Choices and counts — never identifiers or amounts.

**Human Inputs**:
Everything in a Planning Workbook that identifies the project or consortium or carries an amount: names, acronyms, countries, work package and task titles, salaries and daily rates, effort figures, call/topic ID, budget ceiling. Entered only by a human in designated input cells; derived values (country-group rates, unit costs) come from formulas over them. An agent never asks for, writes or reads Human Inputs, so it never opens a filled-in Planning Workbook.
_Avoid_: Sensitive data (too vague), project data

**Transfer View**:
The block of a Planning Workbook, one per Beneficiary (and Affiliated Entity), laid out row-for-row like the Submission Budget's own breakdown (for Horizon Europe: each work package and cost line with number of items and average cost per item, in the Official Budget Table's units; for KA220: the amount per work package). A human copies it across unchanged.
_Avoid_: Export, output sheet

**Check Summaries**:
The Planning Workbook's mirrors of the Submission Budget's own summaries (for Horizon Europe: lump sum breakdown, person-months overview, summary per work package), plus the percentage shares of effort and budget per work package and, where the profile has a Lump Sum Tier, the gap between estimated total and tier. Used to check figures before and after transfer.

**Rate Table**:
The sheet of personnel rates per Beneficiary (or Affiliated Entity) × Staff Category, in the Funding Profile's native unit (cost per person-month for Horizon Europe, daily rate for Erasmus+). Rates are Human Inputs, or derived from the Beneficiary's country where the profile publishes rates per country group, with the human able to override.

**Profile Constant**:
A fixed convention of a Funding Profile that a Planning Workbook relies on — e.g. the 25% indirect cost rate, 1,720 annual productive hours, the days-per-person-month factor. Always shown in a visible, labelled cell that formulas reference, never written into a formula as a bare number.
_Avoid_: Magic number, parameter

**Lump Sum Tier**:
A fixed total grant amount the applicant chooses rather than calculates — for KA220 one of €120,000, €250,000 or €400,000. A Human Input. The Planning Workbook estimates bottom-up with Estimation Methods and shows the gap to the tier; the human adjusts until it fits.

**Synthetic Check**:
The verification every newly built or rebuilt Planning Workbook must pass before handover: a disposable copy is filled with obviously fake inputs (BE1…BEn, round-number rates and effort), recalculated in Excel, and compared against expected figures computed independently of the workbook's formulas. A workbook without a passed Synthetic Check is not delivered. Expected figures come from a reference model of the Funding Profile and Estimation Methods, itself pinned to a Golden Scenario; expected figures change only with human approval.

**Golden Scenario**:
A small fixed synthetic proposal per Funding Profile (a couple of Beneficiaries, one Affiliated Entity, two work packages, a few trips) whose expected totals were worked out by hand once and committed. It anchors the Synthetic Check to reality.
_Avoid_: Test run, smoke test

**Input Guards**:
The checks a Planning Workbook runs on itself while a human fills it in, since no agent ever sees the filled workbook: data validation on inputs, completeness flags, soft plausibility warnings, the Funding Profile's rule checks, all summarised on a Checks panel (OK / warning / error per guard). Plausibility thresholds are human-filled Profile Constants with no defaults; a guard with no threshold stays silent.
_Avoid_: Validation (alone), error checks

**Cover Sheet**:
The first sheet of every Planning Workbook: provenance (Funding Profile version, build date, Shape Parameters), the Checks panel, the fill-in order and the cell colour legend (inputs light yellow, derived white, guards conditionally coloured). The primary guide for the human filling it in.

**Handover Package**:
What the human receives from a build: the blank Planning Workbook, an English fill-in guide (per sheet: what to enter, unit, source, and how to transfer the Transfer View into the Submission Budget), the Synthetic Check report, and — on a rebuild — a re-paste guide mapping old input blocks to new ones.
