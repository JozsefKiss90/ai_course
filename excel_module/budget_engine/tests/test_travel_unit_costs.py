"""HE travel and subsistence unit costs re-extracted from C(2024)5405 (ticket 02)."""

import pytest

from budget_engine.profiles import load_travel_unit_costs

TABLE_IDS = {
    "travel_bands",
    "intra_ms_land",
    "inter_ms_land",
    "ms_bordering_land",
    "subsistence",
    "subsistence_2024_07_31_to_2025_05_12",
}


@pytest.fixture(scope="module")
def data():
    return load_travel_unit_costs()


def table(data, table_id):
    return next(t for t in data["tables"] if t["id"] == table_id)


def test_source_is_the_decision_itself(data):
    assert data["source"]["decision"] == "C(2024)5405"
    assert data["source"]["date"] == "2024-07-31"


def test_every_table_carries_its_provenance(data):
    assert {t["id"] for t in data["tables"]} == TABLE_IDS
    for t in data["tables"]:
        assert t["annex"] and t["pages"] and t["unit"], t["id"]
        assert t["rows"], t["id"]


def test_travel_bands_cover_400_km_upwards_without_gaps(data):
    rows = table(data, "travel_bands")["rows"]
    assert rows[0]["from_km"] == 400
    for prev, nxt in zip(rows, rows[1:]):
        assert nxt["from_km"] == prev["to_km"] + 1
    assert rows[-1]["to_km"] is None


@pytest.mark.parametrize(
    "table_id, key",
    [
        ("intra_ms_land", ("country_code",)),
        ("inter_ms_land", ("country_code_a", "country_code_b")),
        ("ms_bordering_land", ("member_state",)),
        ("subsistence", ("country",)),
        ("subsistence_2024_07_31_to_2025_05_12", ("country",)),
    ],
)
def test_lookup_keys_are_unique(data, table_id, key):
    keys = [tuple(r[k] for k in key) for r in table(data, table_id)["rows"]]
    assert len(keys) == len(set(keys))


def test_inter_ms_pairs_are_listed_once_in_code_order(data):
    for r in table(data, "inter_ms_land")["rows"]:
        assert r["country_code_a"] < r["country_code_b"]


def test_subsistence_periods_meet_without_gap(data):
    old = table(data, "subsistence_2024_07_31_to_2025_05_12")["applies_to_calls_opening"]
    new = table(data, "subsistence")["applies_to_calls_opening"]
    assert old == {"from": "2024-07-31", "to": "2025-05-12"}
    assert new == {"from": "2025-05-13", "to": None}


def test_every_subsistence_table_has_an_other_countries_fallback(data):
    for table_id in ("subsistence", "subsistence_2024_07_31_to_2025_05_12"):
        assert any(r["country"] == "Other Countries" for r in table(data, table_id)["rows"])


# Spot-checks read off the source PDFs by hand; see the ticket for page references.
def test_spot_check_travel_bands(data):
    rows = {r["from_km"]: r["amount"] for r in table(data, "travel_bands")["rows"]}
    assert rows[4501] == 857
    assert rows[10001] == 1595


def test_spot_check_intra_member_state_land(data):
    rows = {r["country_code"]: r for r in table(data, "intra_ms_land")["rows"]}
    assert (rows["HU"]["amount_50_399_km"], rows["HU"]["amount_400_600_km"]) == (29, None)
    assert (rows["DE"]["amount_50_399_km"], rows["DE"]["amount_400_600_km"]) == (64, 157)


def test_spot_check_inter_member_state_land(data):
    rows = {(r["country_code_a"], r["country_code_b"]): r for r in table(data, "inter_ms_land")["rows"]}
    assert (rows["DE", "PL"]["amount_50_399_km"], rows["DE", "PL"]["amount_400_600_km"]) == (96, 240)


def test_spot_check_subsistence(data):
    new = {r["country"]: r for r in table(data, "subsistence")["rows"]}
    old = {r["country"]: r for r in table(data, "subsistence_2024_07_31_to_2025_05_12")["rows"]}
    assert new["Belgium"]["subsistence"] == 132
    assert new["Other Countries"]["accommodation"] == 145
    assert old["Belgium"]["accommodation"] == 148
    assert old["Hungary"]["subsistence"] == 64
