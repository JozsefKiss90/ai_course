"""The reference model against the human-owned Golden Scenario, and how the Synthetic Check fills a copy from it.

The expected figures come from ``golden/he-lump-sum-1.0.md`` (as transcribed for the engine) and are
never edited to make a test pass. Amounts compare to the cent. Shares compare as the worksheet
shows them, in % to two decimals. No Excel needed: the workbook side is in test_synthetic_check.py.
"""

import pytest

from budget_engine import build
from budget_engine.verify.golden import load_golden, synthetic_scenario
from budget_engine.verify.reference import expected_check_summaries, expected_transfer_view

CENT = 0.005


@pytest.fixture(scope="module")
def golden():
    from budget_engine.profiles import load_profile

    scenario = load_golden(load_profile("he-lump-sum", "1.0"))
    assert scenario is not None
    return scenario


@pytest.fixture(scope="module")
def at_golden_shape(golden, tmp_path_factory):
    """A build with the Golden Scenario's Shape Parameters and the reference model's figures for it."""
    result = build(golden.shape_parameters, tmp_path_factory.mktemp("golden") / "planning.xlsx")
    scenario = golden.scenario(result.shape, result.layout)
    tv = expected_transfer_view(result.profile, result.shape, scenario.inputs)
    return result, scenario, tv, expected_check_summaries(result.profile, result.shape, scenario.inputs, tv)


def _differences(pairs):
    """(figure, signed-off, reference) -> the ones that differ by more than half a cent."""
    return [(name, want, got) for name, want, got in pairs if got is None or abs(got - want) > CENT]


def _pct(share: float) -> float:
    return round(share * 100, 2)


def test_the_reference_model_reproduces_every_transfer_view_figure(golden, at_golden_shape):
    result, _, tv, _ = at_golden_shape
    lines = [r.id for r in result.profile.transfer_view_rows if r.kind == "line"]
    pairs = []
    for block, wps in golden.expected["transfer_view"].items():
        for wp, figures in wps.items():
            for line in lines:
                listed = figures["lines"].get(line)
                for field, want in zip(("items", "avg", "total"), listed or (0.0, 0.0, 0.0)):
                    pairs.append((f"{block} {wp} {line} {field}", want, tv.get(("tv", block, wp, line, field), 0.0)))
            for row_id in ("AC", "direct", "E", "F"):
                pairs.append((f"{block} {wp} {row_id}", figures[row_id], tv.get(("tv", block, wp, row_id, "total"))))
    for slot in result.shape.spare_slots:
        for wp in result.shape.wp_codes:
            pairs.append((f"{slot} {wp} F", 0.0, tv.get(("tv", slot, wp, "F", "total"))))
    assert _differences(pairs) == []


def test_the_reference_model_reproduces_every_trip_total(golden, at_golden_shape):
    """Each Golden trip is alone on its BE/AE x WP, so its total is that block's C.1 line."""
    _, scenario, tv, _ = at_golden_shape
    pairs = []
    for n, want in golden.expected["trip_totals"].items():
        be, wp = scenario.inputs[("trip", n, "be")], scenario.inputs[("trip", n, "wp")]
        pairs.append((f"trip {n}", want, tv.get(("tv", be, wp, "C1", "total"))))
    assert _differences(pairs) == []


def test_the_reference_model_reproduces_the_lump_sum_breakdown_and_person_months(golden, at_golden_shape):
    _, _, _, summaries = at_golden_shape
    pairs, shares = [], []
    for kind, section in (("ls", "lump_sum"), ("pm", "person_months")):
        grid = golden.expected[section]
        for row, cells in grid["rows"].items():
            for col, want in cells.items():
                if col == "share_pct":
                    got = summaries[(kind, row, "share")] if row != "total" else 1.0  # the grand total is 100%
                    shares.append((f"{kind} {row} share", want, _pct(got)))
                else:
                    pairs.append((f"{kind} {row} {col}", want, summaries.get((kind, row, col))))
        for wp, want in grid["wp_share_pct"].items():
            shares.append((f"{kind} share {wp}", want, _pct(summaries[(kind, "share", wp)])))
    for block, want in golden.expected["lump_sum"]["rates"].items():
        pairs.append((f"ls {block} rate", want, summaries.get(("ls", block, "rate"))))
    assert _differences(pairs) == []
    assert [s for s in shares if s[1] != s[2]] == []


def test_the_reference_model_reproduces_the_cost_categories_and_category_e(golden, at_golden_shape):
    result, _, tv, summaries = at_golden_shape
    group = {r.id: r.group for r in result.profile.transfer_view_rows if r.kind == "line"}
    blocks = list(golden.expected["cost_categories"])[:-1]

    def per_block(block: str, field: str) -> float:
        wps = result.shape.wp_codes
        if field in ("A", "B", "C", "D"):
            return sum(tv.get(("tv", block, wp, line, "total"), 0.0) for wp in wps for line, g in group.items() if g == field)
        return sum(tv[("tv", block, wp, field, "total")] for wp in wps)

    pairs = []
    for block in blocks:
        for field, want in golden.expected["cost_categories"][block].items():
            pairs.append((f"{block} {field}", want, per_block(block, field)))
        for field, want in golden.expected["category_e"][block].items():
            pairs.append((f"{block} {field} (category E table)", want, per_block(block, field)))
    for field, want in golden.expected["cost_categories"]["total"].items():
        if field in ("E", "F"):
            pairs.append((f"total {field} (Check Summaries)", want, summaries[("wps", "all", field, "all", "total")]))
        pairs.append((f"total {field}", want, sum(per_block(b, field) for b in blocks)))
    assert _differences(pairs) == []


def test_the_reference_model_reproduces_the_summary_per_wp_and_its_shares(golden, at_golden_shape):
    result, _, tv, summaries = at_golden_shape
    total_f = summaries[("wps", "all", "F", "all", "total")]
    total_pm = summaries[("pm", "total", "total")]
    pairs, shares = [], []
    for wp, want in golden.expected["per_wp_summary"]["wps"].items():
        f, pm = summaries[("wps", wp, "F", "all", "total")], summaries[("pm", "total", wp)]
        pairs += [(f"{wp} F", want["F"], f), (f"{wp} pm", want["pm"], pm)]
        shares += [(f"{wp} % of F", want["F_share_pct"], _pct(f / total_f)), (f"{wp} % of PM", want["pm_share_pct"], _pct(pm / total_pm))]
    for blocks, want in golden.expected["per_wp_summary"]["blocks"].items():
        members = blocks.split("+")
        f = sum(tv[("tv", b, wp, "F", "total")] for b in members for wp in result.shape.wp_codes)
        pm = sum(summaries[("pm", b, "total")] for b in members)
        pairs += [(f"{blocks} F", want["F"], f), (f"{blocks} pm", want["pm"], pm)]
        shares += [(f"{blocks} % of F", want["F_share_pct"], _pct(f / total_f)), (f"{blocks} % of PM", want["pm_share_pct"], _pct(pm / total_pm))]
    assert _differences(pairs) == []
    assert [s for s in shares if s[1] != s[2]] == []


def test_at_the_golden_shape_the_check_fills_the_golden_inputs_and_pins_the_signed_off_figures(golden, at_golden_shape):
    result, scenario, _, _ = at_golden_shape
    assert scenario.human_owned and scenario.name == "Golden Scenario he-lump-sum 1.0"
    assert {k: v for k, v in scenario.inputs.items() if v is not None} == golden.inputs
    assert scenario.late_rows == ()
    assert set(scenario.pinned) <= set(result.layout.outputs)
    assert scenario.pinned[("tv", "BE2", "WP2", "F", "total")] == 68750.0
    assert scenario.pinned[("ls", "total", "total")] == 197593.0


@pytest.mark.parametrize(
    "overrides",
    [
        {"beneficiaries": 1, "work_packages": 1},
        {"beneficiaries": 4, "affiliated_entities": [0, 2, 0, 1], "work_packages": 3, "tasks": [1, 0, 3]},
        {"beneficiaries": 2, "affiliated_entities": [1, 0], "work_packages": 2, "tasks": [2, 0], "duration_months": 24, "headroom": 1},
    ],
)
def test_any_other_shape_gets_the_golden_inputs_scaled_and_no_pinned_figures(tmp_path, overrides):
    shape = {"profile": {"id": "he-lump-sum", "version": "1.0"}, "duration_months": 36, **overrides}
    result = build(shape, tmp_path / "planning.xlsx")

    scenario = synthetic_scenario(result.profile, result.shape, result.layout)

    assert not scenario.human_owned and "scaled" in scenario.name and scenario.pinned == {}
    assert set(scenario.inputs) == set(result.layout.inputs)
    codes, wps = set(result.shape.entity_codes), set(result.shape.wp_codes)
    for key, value in scenario.inputs.items():
        if key[0] in ("trip", "equipment", "itemised") and value is not None:
            assert value in codes if key[2] == "be" else value in wps if key[2] == "wp" else True, key
    for slot in result.shape.spare_slots:
        assert all(v is None for k, v in scenario.inputs.items() if slot in k)  # spare blocks stay empty
    if result.shape.beneficiaries == 1:
        efforts = [v for k, v in scenario.inputs.items() if k[0] == "effort" and v is not None]
        assert sum(efforts) == 2 + 4 + 1 + 3 + 1.5 + 2  # BE1's effort, both WPs folded onto WP1


def test_the_check_uses_the_provisional_scenario_only_for_a_profile_version_without_a_golden_scenario(tmp_path, monkeypatch):
    from budget_engine.verify import golden

    result = build({"profile": {"id": "he-lump-sum", "version": "1.0"}, "beneficiaries": 1, "work_packages": 1, "duration_months": 12}, tmp_path / "p.xlsx")
    monkeypatch.setattr(golden, "GOLDEN_DIR", tmp_path / "none")

    scenario = synthetic_scenario(result.profile, result.shape, result.layout)

    assert scenario.name.startswith("provisional") and not scenario.human_owned
