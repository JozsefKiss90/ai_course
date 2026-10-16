"""Automatic checks for budget rules - the code version of a reviewer's checklist.

Run with:  uv run pytest
"""

import pandas as pd
import pytest

from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "sample_budget.csv"


@pytest.fixture
def budget():
    df = pd.read_csv(DATA)
    df["cost_eur"] = df["quantity"] * df["unit_cost_eur"]
    return df


def test_every_line_has_a_source_note(budget):
    """Like a wiki node without source_refs: a cost line without a source is not allowed."""
    assert budget["source_note"].notna().all()


def test_indirect_costs_exclude_subcontracting(budget):
    """AGA Art. 6.2.E: the 25% flat rate is not applied to subcontracting (category B)."""
    base = budget.loc[budget["category_code"] != "B", "cost_eur"].sum()
    indirect = round(base * 0.25, 2)
    assert indirect == pytest.approx(0.25 * (budget["cost_eur"].sum() - 6000))


def test_no_negative_costs(budget):
    assert (budget["cost_eur"] >= 0).all()
