"""The build input contract: only Shape Parameters get in (ADR-0001)."""

import pytest

from budget_engine import ShapeError, build

HE = {"id": "he-lump-sum", "version": "1.0"}


def shape(**overrides: object) -> dict[str, object]:
    params: dict[str, object] = {
        "profile": HE,
        "beneficiaries": 2,
        "work_packages": 3,
        "duration_months": 36,
    }
    params.update(overrides)
    return params


def test_minimal_shape_builds_an_xlsx(tmp_path):
    result = build(shape(), tmp_path / "planning.xlsx")
    assert result.path.exists()
    assert result.path.suffix == ".xlsx"


@pytest.mark.parametrize(
    "field, value",
    [
        ("partner_names", ["Acme University"]),
        ("acronym", "ACME"),
        ("budget_ceiling", 4_000_000),
        ("countries", ["Belgium"]),
    ],
)
def test_fields_outside_the_contract_are_rejected(tmp_path, field, value):
    with pytest.raises(ShapeError, match=field):
        build(shape(**{field: value}), tmp_path / "x.xlsx")
    assert not (tmp_path / "x.xlsx").exists()


@pytest.mark.parametrize(
    "field, value",
    [
        ("beneficiaries", 0),
        ("beneficiaries", "2"),
        ("beneficiaries", True),
        ("work_packages", -1),
        ("duration_months", 2.5),
        ("headroom", -1),
        ("headroom", True),
        ("affiliated_entities", [1]),  # one entry per Beneficiary, and shape() has two
        ("affiliated_entities", [1, -1]),
        ("affiliated_entities", [1, 1.5]),
        ("affiliated_entities", [True, 0]),
        ("affiliated_entities", {"BE1": 1}),
        ("tasks", [2, 2]),  # one entry per WP, and shape() has three
        ("tasks", [2, 0, 1]),  # a WP with a Task List has at least one task
        ("tasks", [2, 1.5, 1]),
        ("tasks", [True, 1, 1]),
        ("tasks", 3),
        ("methods", ["staff_effort", "crystal_ball"]),
        ("profile", {"id": "he-lump-sum", "version": "1.0", "note": "ACME"}),
        ("profile", {"id": "no-such-profile", "version": "1.0"}),
    ],
)
def test_invalid_shape_values_are_rejected(tmp_path, field, value):
    with pytest.raises(ShapeError):
        build(shape(**{field: value}), tmp_path / "x.xlsx")


def test_mandatory_methods_are_switched_on_and_headroom_defaults_from_profile(tmp_path):
    result = build(shape(methods=[]), tmp_path / "planning.xlsx")
    assert "staff_effort" in result.shape.methods
    assert result.shape.headroom == 3


def test_affiliated_entities_default_to_none_and_are_listed_under_their_beneficiary(tmp_path):
    assert build(shape(), tmp_path / "none.xlsx").shape.entity_codes == ["BE1", "BE2"]

    result = build(shape(beneficiaries=3, affiliated_entities=[2, 0, 1]), tmp_path / "planning.xlsx")
    assert result.shape.entity_codes == ["BE1", "BE1-AE1", "BE1-AE2", "BE2", "BE3", "BE3-AE1"]


def test_blocks_are_built_up_to_count_plus_headroom(tmp_path):
    result = build(shape(affiliated_entities=[1, 0], headroom=2), tmp_path / "planning.xlsx")
    assert result.shape.slots == ["BE1", "BE1-AE1", "BE2", "SPARE1", "SPARE2"]

    default = build(shape(), tmp_path / "default.xlsx")
    assert default.shape.slots == ["BE1", "BE2", "SPARE1", "SPARE2", "SPARE3"]  # HE default headroom +3


def test_tasks_are_optional_and_coded_per_work_package(tmp_path):
    without = build(shape(), tmp_path / "none.xlsx").shape
    assert without.tasks is None
    assert without.effort_units == [("WP1", "WP1"), ("WP2", "WP2"), ("WP3", "WP3")]

    with_tasks = build(shape(tasks=[2, 1, 3]), tmp_path / "tasks.xlsx").shape
    assert with_tasks.tasks == (2, 1, 3)
    assert with_tasks.task_codes == ["T1.1", "T1.2", "T2.1", "T3.1", "T3.2", "T3.3"]
    assert with_tasks.effort_units[:3] == [("WP1", "T1.1"), ("WP1", "T1.2"), ("WP2", "T2.1")]


def test_the_travel_planner_is_on_by_default_and_can_be_switched_off(tmp_path):
    default = build(shape(), tmp_path / "default.xlsx").shape
    assert "travel_planner" in default.methods

    off = build(shape(methods=["staff_effort"]), tmp_path / "off.xlsx").shape
    assert off.methods == ("staff_effort",)


def test_equipment_depreciation_is_on_by_default_and_can_be_switched_off(tmp_path):
    default = build(shape(), tmp_path / "default.xlsx").shape
    assert "equipment_depreciation" in default.methods

    off = build(shape(methods=["staff_effort", "travel_planner"]), tmp_path / "off.xlsx").shape
    assert off.methods == ("staff_effort", "travel_planner")


def test_the_itemised_list_is_on_by_default_and_can_be_switched_off(tmp_path):
    default = build(shape(), tmp_path / "default.xlsx").shape
    assert default.methods == ("staff_effort", "travel_planner", "equipment_depreciation", "itemised_list")

    off = build(shape(methods=["staff_effort", "itemised_list"]), tmp_path / "off.xlsx").shape
    assert off.methods == ("staff_effort", "itemised_list")
