"""Input Guards: the checks a Planning Workbook runs on itself while a human fills it in.

No agent ever sees a filled workbook (ADR-0001), so the workbook flags its own gaps and oddities:
- data validation on every Human Input but free text (see ``sheets/validation.py``), and a guard
  for negative values that got past it (Excel's validation does not check pasted values)
- completeness flags: a Beneficiary or AE with no country, a work package with no lead, effort
  without a rate
- plausibility warnings (soft): each compares a figure with a threshold the human fills in on the
  `Profile Constants` sheet; there are no defaults, and a guard stays silent while its threshold is blank
- profile rule checks: the Funding Profile's own rules, declared in its data (HE declares none)

Each guard is a count of offending entries; the Cover Sheet's Checks panel turns the counts into
OK / warning / error. The `Input Guards` sheet holds the work package leads (they have no place in
the Official Budget Table's `WP list`) and the per-entry flags behind two of the counts.
"""

from __future__ import annotations

from dataclasses import dataclass

from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext, Cell, box
from budget_engine.methods import equipment_depreciation, itemised_list, travel_planner
from budget_engine.profiles import PlausibilityThreshold, Profile, RuleCheck
from budget_engine.shape import ShapeParameters, is_spare
from budget_engine.sheets import constants, task_list, validation
from budget_engine.sheets.reference_lists import be_field, column_ref, lookup
from budget_engine.sheets.styles import BOLD, TITLE, WRAP, put_derived, put_header, put_input

SHEET = "Input Guards"
OK, WARNING, ERROR = "OK", "warning", "error"
MISSING_LEAD = "missing lead"
MISSING_RATE = "missing rate"
ERROR_FILL = PatternFill("solid", fgColor="FFF4B6B6")
WARNING_FILL = PatternFill("solid", fgColor="FFFFD966")
OK_FILL = PatternFill("solid", fgColor="FFC6EFCE")
STATUS_FILLS = {ERROR: ERROR_FILL, WARNING: WARNING_FILL, OK: OK_FILL}

# A plausibility measure -> the Estimation Method it needs (None: always there).
MEASURES: dict[str, str | None] = {"rate": None, "effort_per_block_wp": None, "trip_cost": travel_planner.ID}
RULE_KINDS = ("max_share_per_wp",)
# Numeric Human Inputs outside method Tables, then the numeric Table columns per input kind of a
# method's rows: (method, fields).
NUMERIC_KINDS = ("rate", "effort", "threshold")
NUMERIC_TABLE_FIELDS = {
    "trip": (travel_planner, ("travellers", "distance", "nights", "days")),
    "equipment": (equipment_depreciation, ("cost", "period", "usage")),
    "itemised": (itemised_list, ("number", "cost")),
}
FIRST_CATEGORY_COL = 3  # effort without a rate: A BE/AE nr, B acronym, then one column per Staff Category
THRESHOLDS_TITLE = "Plausibility thresholds (your own standards)"
THRESHOLDS_NOTE = (
    "Optional. Fill in the thresholds you want warnings for; there are no defaults, and a guard stays silent "
    "while its threshold is blank. See the Checks panel on the Cover Sheet."
)


@dataclass(frozen=True)
class GuardSpec:
    """One Input Guard: a row of the Checks panel."""

    id: str
    label: str
    severity: str  # what a non-zero count shows: "error" or "warning"
    kind: str  # data validation | completeness | plausibility | rule
    where: str  # where the human looks to fix it
    threshold: PlausibilityThreshold | None = None
    rule: RuleCheck | None = None


def thresholds(profile: Profile, shape: ShapeParameters) -> list[PlausibilityThreshold]:
    """The profile's plausibility thresholds whose measure this build has."""
    for t in profile.plausibility:
        if t.measure not in MEASURES:
            raise ValueError(f"{profile.id} {profile.version}: unknown plausibility measure {t.measure!r}")
    return [t for t in profile.plausibility if MEASURES[t.measure] in (None, *shape.methods)]


def guard_specs(profile: Profile, shape: ShapeParameters) -> list[GuardSpec]:
    """Every Input Guard of a build, in Checks panel order."""
    specs = [
        GuardSpec("negative_values", "Negative values in numeric inputs", ERROR, "data validation",
                  "Rate Table, Staff effort, method sheets, plausibility thresholds (a pasted value skips validation)"),
        GuardSpec("be_without_country", "Beneficiary or AE with no country", ERROR, "completeness", "BE list: Country"),
        GuardSpec("wp_without_lead", "Work package with no lead", ERROR, "completeness", f"{SHEET}: work package leads"),
        GuardSpec("effort_without_rate", "Effort without a rate", ERROR, "completeness",
                  f"{SHEET}: effort without a rate, then the Rate Table"),
    ]
    for t in thresholds(profile, shape):
        specs.append(GuardSpec(t.id, f"Plausibility: {t.label}", WARNING, "plausibility",
                               f"{constants.SHEET}: plausibility thresholds", threshold=t))
    for rule in profile.rule_checks:
        if rule.kind not in RULE_KINDS:
            raise ValueError(f"{profile.id} {profile.version}: unknown rule check kind {rule.kind!r}")
        if rule.params.get("limit_constant") not in {c.id for c in profile.constants}:
            raise ValueError(f"{profile.id} {profile.version}: rule check {rule.id!r} names no Profile Constant as its limit")
        specs.append(GuardSpec(rule.id, f"Rule: {rule.label}", rule.severity, "rule", "Check Summaries", rule=rule))
    return specs


def build_thresholds(ctx: BuildContext) -> None:
    """The plausibility thresholds, blank and labelled, under the Profile Constants."""
    ws = ctx.wb[constants.SHEET]
    available = thresholds(ctx.profile, ctx.shape)
    if not available:
        return
    row = ws.max_row + 2
    ws[f"A{row}"] = THRESHOLDS_TITLE
    ws[f"A{row}"].font = BOLD
    ws[f"A{row + 1}"] = THRESHOLDS_NOTE
    ws[f"A{row + 1}"].alignment = WRAP
    ws.row_dimensions[row + 1].height = 45
    first = row + 2
    for i, t in enumerate(available):
        r = first + i
        put_derived(ws, f"A{r}", t.label)
        put_input(ctx, ws, f"B{r}", ("threshold", t.id))
        put_derived(ws, f"C{r}", t.unit)
        put_derived(ws, f"D{r}", "Your own standard (no default)")
    validation.apply(ws, validation.non_negative(), f"B{first}:B{first + len(available) - 1}")


def build_input_guards(ctx: BuildContext) -> list[tuple[GuardSpec, str]]:
    """Write the `Input Guards` sheet after the work package and task lists; return each guard with
    its count formula (without "=") for the Checks panel."""
    anchor = task_list.SHEET if ctx.shape.tasks is not None else str(ctx.profile.reference_lists["wp_list"]["sheet"])
    ws = ctx.wb.create_sheet(SHEET, ctx.wb.sheetnames.index(anchor) + 1)
    ws["A1"] = SHEET
    ws["A1"].font = TITLE
    ws["A2"] = "Enter each work package's lead. The flags below feed the Checks panel on the Cover Sheet."
    lead_flags = _build_leads(ctx, ws, 4)
    rate_flags = _build_effort_without_rate(ctx, ws, ws.max_row + 2)
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["B"].width = 40
    for j in range(len(ctx.profile.staff_categories)):  # the lead column C included
        ws.column_dimensions[get_column_letter(FIRST_CATEGORY_COL + j)].width = 16
    counts = {
        "negative_values": "+".join(f'COUNTIF({r},"<0")' for r in _numeric_ranges(ctx)),
        "be_without_country": (
            f'COUNTIFS({column_ref(ctx.profile, "be_list", "A")},"<>",'
            f'{column_ref(ctx.profile, "be_list", _country_column(ctx.profile))},"")'
        ),
        "wp_without_lead": f'COUNTIF({lead_flags},"{MISSING_LEAD}")',
        "effort_without_rate": f'COUNTIF({rate_flags},"{MISSING_RATE}")',
    }
    guards = []
    for spec in guard_specs(ctx.profile, ctx.shape):
        if spec.threshold is not None:
            counts[spec.id] = _plausibility_count(ctx, spec.threshold)
        elif spec.rule is not None:
            counts[spec.id] = _rule_count(ctx, spec.rule)
        guards.append((spec, counts[spec.id]))
    return guards


def _country_column(profile: Profile) -> str:
    return str(profile.reference_lists["be_list"]["country_list"]["column"])


def colour_when(ws: Worksheet, cells: str, text: str, fill: PatternFill) -> None:
    """Conditionally fill ``cells`` while they show ``text``."""
    rule = CellIsRule(operator="equal", formula=[f'"{text}"'], fill=fill)  # type: ignore[no-untyped-call]
    ws.conditional_formatting.add(cells, rule)


def _build_leads(ctx: BuildContext, ws: Worksheet, row: int) -> str:
    """WP | WP name | lead (BE/AE nr) | flag, one row per WP; returns the flags' range."""
    ws[f"A{row}"] = "Work package leads"
    ws[f"A{row}"].font = BOLD
    for col, header in zip("ABCD", ("WP", "WP name", "Lead (BE/AE nr)", "Flag")):
        put_header(ws, f"{col}{row + 1}", header)
    first = row + 2
    for i, wp in enumerate(ctx.shape.wp_codes):
        r = first + i
        put_derived(ws, f"A{r}", wp)
        put_derived(ws, f"B{r}", "=" + lookup(ctx.profile, "wp_list", "B", f'"{wp}"'))
        put_input(ctx, ws, f"C{r}", ("wp_lead", wp))
        put_derived(ws, f"D{r}", f'=IF(C{r}="","{MISSING_LEAD}","")')
    last = first + len(ctx.shape.wp_codes) - 1
    validation.apply(ws, validation.list_of(f'INDIRECT("{column_ref(ctx.profile, "be_list", "A")}")'), f"C{first}:C{last}")
    colour_when(ws, f"D{first}:D{last}", MISSING_LEAD, ERROR_FILL)
    return f"'{SHEET}'!$D${first}:$D${last}"


def _build_effort_without_rate(ctx: BuildContext, ws: Worksheet, row: int) -> str:
    """A flag per BE/AE block × Staff Category with effort planned but no rate; returns the flags' range."""
    ws[f"A{row}"] = "Effort without a rate"
    ws[f"A{row}"].font = BOLD
    ws[f"A{row + 1}"] = "Effort is planned on the staff effort sheet, but the Rate Table has no rate for it."
    put_header(ws, f"A{row + 2}", "BE/AE nr")
    put_header(ws, f"B{row + 2}", "Acronym")
    categories = ctx.profile.staff_categories
    for j, category in enumerate(categories):
        put_header(ws, f"{get_column_letter(FIRST_CATEGORY_COL + j)}{row + 2}", category.label)
    first = row + 3
    for i, slot in enumerate(ctx.shape.slots):
        r = first + i
        put_derived(ws, f"A{r}", ctx.layout.slot_label(slot))
        put_derived(ws, f"B{r}", "=" + be_field(ctx, "be_acronym", ctx.layout.slot_codes[slot]))
        if is_spare(slot):
            ws.row_dimensions[r].outline_level = 1
        for j, category in enumerate(categories):
            efforts = [ctx.layout.inputs[("effort", unit, slot, category.id)].ref for _, unit in ctx.shape.effort_units]
            rate = ctx.layout.inputs[("rate", slot, category.id)].ref
            formula = f'=IF(AND(SUM({",".join(efforts)})>0,{rate}=0),"{MISSING_RATE}","")'
            put_derived(ws, f"{get_column_letter(FIRST_CATEGORY_COL + j)}{r}", formula)
    first_col = get_column_letter(FIRST_CATEGORY_COL)
    last_col = get_column_letter(FIRST_CATEGORY_COL + len(categories) - 1)
    last = first + len(ctx.shape.slots) - 1
    colour_when(ws, f"{first_col}{first}:{last_col}{last}", MISSING_RATE, ERROR_FILL)
    return f"'{SHEET}'!${first_col}${first}:${last_col}${last}"


def _inputs_of(ctx: BuildContext, kind: str) -> list[Cell]:
    return [cell for key, cell in ctx.layout.inputs.items() if key[0] == kind]


def _numeric_ranges(ctx: BuildContext) -> list[str]:
    """Every range of numeric Human Inputs: Rate Table, staff effort, thresholds, numeric Table columns."""
    ranges = [box(_inputs_of(ctx, kind)) for kind in NUMERIC_KINDS if _inputs_of(ctx, kind)]
    for method, fields in NUMERIC_TABLE_FIELDS.values():
        if method.ID in ctx.shape.methods:
            ranges += [f"{method.TABLE}[[{method.COLUMN[field]}]]" for field in fields]
    return ranges


def _plausibility_count(ctx: BuildContext, t: PlausibilityThreshold) -> str:
    threshold = ctx.layout.inputs[("threshold", t.id)].ref
    if t.measure == "rate":
        compared = box(_inputs_of(ctx, "rate"))
    elif t.measure == "effort_per_block_wp":
        compared = box([c for k, c in ctx.layout.outputs.items() if k[0] == "pm" and k[2] in ctx.shape.wp_codes and k[1] in ctx.shape.slots])
    elif t.measure == "trip_cost":
        compared = f"{travel_planner.TABLE}[[{travel_planner.TRIP_COST}]]"
    else:
        raise ValueError(f"no guard formula for plausibility measure {t.measure!r}")
    return f'IF({threshold}="",0,COUNTIF({compared},">"&{threshold}))'


def _rule_count(ctx: BuildContext, rule: RuleCheck) -> str:
    """max_share_per_wp: the WPs whose share (of the lump sum or the person-months) is above the
    Profile Constant ``limit_constant``; ``wps`` limits the WPs checked (default: all)."""
    limit = ctx.layout.constants[rule.params["limit_constant"]].ref
    grid = rule.params["grid"]
    wps = rule_wps(rule, ctx.shape)
    return "+".join(f"N({ctx.layout.outputs[(grid, 'share', wp)].ref}>{limit})" for wp in wps) or "0"


def rule_wps(rule: RuleCheck, shape: ShapeParameters) -> list[str]:
    """The WPs a max_share_per_wp rule checks: those it lists that this build has, else all."""
    listed = rule.params.get("wps")
    return [wp for wp in shape.wp_codes if not listed or wp in listed]
