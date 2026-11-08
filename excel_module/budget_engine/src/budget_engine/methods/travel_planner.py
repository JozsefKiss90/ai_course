"""Travel planner: trips per BE/AE and WP, priced with the Commission's travel and subsistence unit costs.

A trip is a row of the `Trips` Excel Table: who travels (BE/AE nr), for which WP, how many
travellers, the one-way distance, nights, days and the destination country. Those are Human Inputs.
Its prices are calculated columns that look the unit costs up, by formula, in the profile's tables
on the `Travel unit costs` sheet:
- travel: the band of table 5.1 (return air and combined air/rail journeys, 400 km and more) that
  holds the one-way distance; shorter distances have no unit cost and show #N/A
- accommodation per night and subsistence per day of the destination country

Trip cost = travellers × (travel + nights × accommodation + days × subsistence). Because the
prices are calculated columns, a trip row a human adds to the Table is priced too.

The `Travel summary` sums the Table with SUMIFS per BE/AE block × WP: no PivotTable, so no hidden
row order and nothing to refresh. Output per BE × WP × cost line: items = person-trips (travellers
summed), total = the trips' cost.
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Mapping

from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableColumn, TableFormula
from openpyxl.worksheet.worksheet import Worksheet

from budget_engine.layout import BuildContext, Cell, Contribution, Key
from budget_engine.methods.base import Figures, number
from budget_engine.profiles import Profile, UnitCostTable
from budget_engine.shape import ShapeParameters, is_spare
from budget_engine.sheets import validation
from budget_engine.sheets.reference_lists import be_field, column_ref
from budget_engine.sheets.styles import MONEY, QUANTITY, TITLE, WRAP, put_derived, put_header, put_input

ID = "travel_planner"
SHEET = "Travel planner"
SUMMARY_SHEET = "Travel summary"
UNIT_COSTS_SHEET = "Travel unit costs"
TABLE = "Trips"
BANDS_TABLE = "TravelBands"
RATES_TABLE = "TravelRates"

HEADER_ROW = 3
FIRST_DATA_ROW = HEADER_ROW + 1
TRIP_ROWS = 20  # blank trip rows to start from; the Table grows beyond them

# (input key, Table column) per Human Input, in column order from A.
INPUTS = (
    ("be", "BE/AE nr"),
    ("wp", "WP"),
    ("travellers", "Travellers"),
    ("distance", "One-way distance (km)"),
    ("nights", "Nights"),
    ("days", "Days"),
    ("country", "Destination country"),
)
COLUMN = dict(INPUTS)  # input key -> Table column
TRAVEL = "Travel (EUR per traveller)"
ACCOMMODATION = "Accommodation (EUR per night)"
SUBSISTENCE = "Subsistence (EUR per day)"
PER_TRAVELLER = "Cost per traveller (EUR)"
TRIP_COST = "Trip cost (EUR)"
PRICES = (TRAVEL, ACCOMMODATION, SUBSISTENCE, PER_TRAVELLER, TRIP_COST)
HEADERS = tuple(name for _, name in INPUTS) + PRICES

FROM_KM, TO_KM, PER_RETURN_TRIP, COUNTRY = "From km", "To km", "EUR per return trip", "Country"
BANDS_HEADERS = (FROM_KM, TO_KM, PER_RETURN_TRIP)
RATES_HEADERS = (COUNTRY, ACCOMMODATION, SUBSISTENCE)  # same names as the Trips columns they price
BANDS_FIRST_COL = 1  # A:C
RATES_FIRST_COL = 5  # E:G
SUMMARY_HEADERS = ("BE/AE nr", "Acronym", "WP", "Person-trips", "Total (EUR)")


def _col(table: str, name: str) -> str:
    return f"{table}[[{name}]]"


def _this_row(name: str) -> str:
    return f"{TABLE}[[#This Row],[{name}]]"


def price_formulas() -> dict[str, str]:
    """The calculated column formulas of the Trips Table (without the leading "=")."""
    distance, country = _this_row(COLUMN["distance"]), _this_row(COLUMN["country"])

    def rate(column: str) -> str:
        found = f"MATCH({country},{_col(RATES_TABLE, COUNTRY)},0)"
        return f'IF({country}="",0,INDEX({_col(RATES_TABLE, column)},{found}))'

    band = f"MATCH({distance},{_col(BANDS_TABLE, FROM_KM)},1)"
    return {
        TRAVEL: f'IF({distance}="",0,INDEX({_col(BANDS_TABLE, PER_RETURN_TRIP)},{band}))',
        ACCOMMODATION: rate(ACCOMMODATION),
        SUBSISTENCE: rate(SUBSISTENCE),
        PER_TRAVELLER: (
            f"{_this_row(TRAVEL)}+{_this_row(COLUMN['nights'])}*{_this_row(ACCOMMODATION)}"
            f"+{_this_row(COLUMN['days'])}*{_this_row(SUBSISTENCE)}"
        ),
        TRIP_COST: f"{_this_row(COLUMN['travellers'])}*{_this_row(PER_TRAVELLER)}",
    }


def unit_cost_tables(profile: Profile) -> tuple[UnitCostTable, UnitCostTable]:
    """The profile's travel band table and accommodation/subsistence rate table."""
    settings = profile.method_settings[ID]
    return profile.unit_cost_tables[settings["travel_bands"]], profile.unit_cost_tables[settings["rates"]]


def unit_cost_rows(profile: Profile) -> tuple[list[tuple[object, ...]], list[tuple[object, ...]]]:
    """The rows the `Travel unit costs` sheet shows, in its column order: bands, then rates."""
    bands, rates = unit_cost_tables(profile)
    return (
        [(r["from_km"], r["to_km"], r["amount"]) for r in bands.rows],
        [(r["country"], r["accommodation"], r["subsistence"]) for r in rates.rows],
    )


def build(ctx: BuildContext) -> None:
    _build_trips(ctx)
    _build_summary(ctx)
    _build_unit_costs(ctx)


def _build_trips(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SHEET)
    ws["A1"] = "Travel planner: one row per trip, priced with the Commission's travel and subsistence unit costs"
    ws["A1"].font = TITLE
    shortest = unit_cost_tables(ctx.profile)[0].rows[0]["from_km"]
    ws["A2"] = (
        "Enter BE/AE nr, WP, travellers, the one-way distance (EC distance calculator), nights, days and the "
        f"destination country. Add rows at the bottom of the Table. Under {shortest} km there is no unit cost (#N/A)."
    )
    for i, header in enumerate(HEADERS, start=1):
        put_header(ws, f"{get_column_letter(i)}{HEADER_ROW}", header)
    formulas = price_formulas()
    last_row = FIRST_DATA_ROW + TRIP_ROWS - 1
    for n in range(1, TRIP_ROWS + 1):
        row = FIRST_DATA_ROW + n - 1
        for i, (key, _) in enumerate(INPUTS, start=1):
            fmt = QUANTITY if key == "distance" else None
            put_input(ctx, ws, f"{get_column_letter(i)}{row}", ("trip", str(n), key), fmt)
        for i, header in enumerate(PRICES, start=len(INPUTS) + 1):
            put_derived(ws, f"{get_column_letter(i)}{row}", "=" + formulas[header], MONEY)

    table = Table(displayName=TABLE, ref=f"A{HEADER_ROW}:{get_column_letter(len(HEADERS))}{last_row}")
    for i, header in enumerate(HEADERS, start=1):
        calculated = TableFormula(attr_text=formulas[header]) if header in formulas else None
        table.tableColumns.append(TableColumn(id=i, name=header, calculatedColumnFormula=calculated))
    ws.add_table(table)
    _add_validations(ctx, ws, last_row)

    for i, width in enumerate((12, 8, 11, 13, 9, 9, 24, 14, 14, 14, 14, 14), start=1):
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[HEADER_ROW].height = 45
    ws.freeze_panes = f"A{FIRST_DATA_ROW}"


def _add_validations(ctx: BuildContext, ws: Worksheet, last_row: int) -> None:
    def column_range(key: str) -> str:
        letter = get_column_letter(1 + [k for k, _ in INPUTS].index(key))
        return f"{letter}{FIRST_DATA_ROW}:{letter}{last_row}"

    lists = {
        "be": column_ref(ctx.profile, "be_list", "A"),
        "wp": column_ref(ctx.profile, "wp_list", "A"),
        "country": _col(RATES_TABLE, COUNTRY),
    }
    for key, source in lists.items():
        validation.apply(ws, validation.list_of(f'INDIRECT("{source}")'), column_range(key))
    validation.apply(ws, validation.non_negative(whole=True), *(column_range(k) for k in ("travellers", "nights", "days")))
    validation.apply(ws, validation.non_negative(), column_range("distance"))


def _sumifs(column: str, code: str, wp: str) -> str:
    """SUMIFS over a Trips column for one BE/AE code (a formula operand) and WP."""
    return f'SUMIFS({_col(TABLE, column)},{_col(TABLE, COLUMN["be"])},{code},{_col(TABLE, COLUMN["wp"])},"{wp}")'


def _build_summary(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(SUMMARY_SHEET)
    ws["A1"] = "Travel summary per BE/AE and work package (formulas over the Trips Table; nothing to refresh)"
    ws["A1"].font = TITLE
    for i, header in enumerate(SUMMARY_HEADERS, start=1):
        put_header(ws, f"{get_column_letter(i)}{HEADER_ROW}", header)
    cost_line = ctx.profile.method_settings[ID]["cost_line"]
    row = FIRST_DATA_ROW
    for slot in ctx.shape.slots:
        code = ctx.layout.slot_codes[slot]
        for wp in ctx.shape.wp_codes:
            put_derived(ws, f"A{row}", ctx.layout.slot_label(slot))
            put_derived(ws, f"B{row}", "=" + be_field(ctx, "be_acronym", code))
            put_derived(ws, f"C{row}", wp)
            for col, column, fmt in (("D", COLUMN["travellers"], QUANTITY), ("E", TRIP_COST, MONEY)):
                total = _sumifs(column, code, wp)
                # An unclaimed spare block has no code, and must not pick up trips without one.
                put_derived(ws, f"{col}{row}", f'=IF({code}="",0,{total})' if is_spare(slot) else "=" + total, fmt)
            if is_spare(slot):
                ws.row_dimensions[row].outline_level = 1
            ctx.contributions.append(
                Contribution(slot, wp, cost_line, Cell(SUMMARY_SHEET, f"D{row}"), Cell(SUMMARY_SHEET, f"E{row}"))
            )
            row += 1
    for col, width in zip("ABCDE", (12, 14, 8, 14, 16)):
        ws.column_dimensions[col].width = width
    ws.freeze_panes = f"A{FIRST_DATA_ROW}"


def _build_unit_costs(ctx: BuildContext) -> None:
    ws = ctx.wb.create_sheet(UNIT_COSTS_SHEET)
    ws["A1"] = "Travel unit costs (Funding Profile data: change only with a new profile version)"
    ws["A1"].font = TITLE
    sources = unit_cost_tables(ctx.profile)
    for first_col, name, headers, source, rows in zip(
        (BANDS_FIRST_COL, RATES_FIRST_COL),
        (BANDS_TABLE, RATES_TABLE),
        (BANDS_HEADERS, RATES_HEADERS),
        sources,
        unit_cost_rows(ctx.profile),
    ):
        provenance = ws.cell(row=2, column=first_col)
        provenance.value = f"{source.title}. Source: {source.source}; {source.annex}; {source.pages}."
        provenance.alignment = WRAP
        for j, header in enumerate(headers):
            put_header(ws, f"{get_column_letter(first_col + j)}{HEADER_ROW}", header)
        for i, values in enumerate(rows):
            for j, value in enumerate(values):
                put_derived(ws, f"{get_column_letter(first_col + j)}{FIRST_DATA_ROW + i}", value)
        last = f"{get_column_letter(first_col + len(headers) - 1)}{FIRST_DATA_ROW + len(rows) - 1}"
        ws.add_table(Table(displayName=name, ref=f"{get_column_letter(first_col)}{HEADER_ROW}:{last}"))
    ws.row_dimensions[2].height = 90
    for col, width in zip("ABCDEFG", (12, 12, 14, 3, 28, 16, 16)):
        ws.column_dimensions[col].width = width
    ws.freeze_panes = f"A{FIRST_DATA_ROW}"


def trip_rows(inputs: Mapping[Key, object]) -> dict[str, dict[Key, object]]:
    """Trip nr -> {(field,): value}, from the ("trip", n, field) inputs (rows added later included)."""
    trips: dict[str, dict[Key, object]] = defaultdict(dict)
    for key, value in inputs.items():
        if key[0] == "trip":
            trips[key[1]][(key[2],)] = value
    return trips


def trip_figures(profile: Profile, trip: Mapping[Key, object]) -> tuple[float, float]:
    """(travellers, trip cost) of one trip row, from its inputs and the profile's unit costs."""
    bands, rates = unit_cost_tables(profile)
    travellers = number(trip, ("travellers",))
    travel = 0.0
    if trip.get(("distance",)) is not None:
        distance = number(trip, ("distance",))
        band = [r for r in bands.rows if r["from_km"] <= distance]
        if not band:
            raise ValueError(f"no travel unit cost for {distance} km: the scenario must not use one")
        travel = float(band[-1]["amount"])
    country = trip.get(("country",))
    by_country = {r["country"]: r for r in rates.rows}
    rate = by_country[str(country)] if country is not None else {"accommodation": 0, "subsistence": 0}
    nights, days = number(trip, ("nights",)), number(trip, ("days",))
    return travellers, travellers * (travel + nights * rate["accommodation"] + days * rate["subsistence"])


def reference(profile: Profile, shape: ShapeParameters, inputs: Mapping[Key, object]) -> Figures:
    """Expected items and total per (BE, WP, cost line), from the trip inputs and the profile's data.

    Trips are the ("trip", n, field) inputs, including rows added to the Table after the build. A
    block's trips are those whose BE/AE nr is the block's code (for a spare block, the code typed in
    the Rate Table; none while it is blank).
    """
    cost_line = profile.method_settings[ID]["cost_line"]
    trips = trip_rows(inputs)
    figures: Figures = {}
    for slot in shape.slots:
        code = inputs.get(("slot_code", slot)) if is_spare(slot) else slot
        for wp in shape.wp_codes:
            items = total = 0.0
            for trip in trips.values():
                if code is not None and trip.get(("be",)) == code and trip.get(("wp",)) == wp:
                    trip_items, trip_total = trip_figures(profile, trip)
                    items, total = items + trip_items, total + trip_total
            figures[(slot, wp, cost_line)] = (items, total)
    return figures
