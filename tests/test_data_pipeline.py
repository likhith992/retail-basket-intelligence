"""End-to-end test for Retail Basket Intelligence data pipeline (Phase 1).

Tests: load → map → clean → basket matrix → mine → rules.
Run with:  pytest tests/test_data_pipeline.py -v
"""

import pandas as pd
import pytest

from src.data_loading import load_file, map_columns
from src.cleaning import clean_data
from src.basket_matrix import build_basket_matrix
from src.mining import mine_itemsets, generate_rules


@pytest.fixture
def clean_df():
    """Load and clean the sample dataset."""
    df_raw = load_file("data/raw/sample_retail.csv")
    mapping = {
        "invoice": "InvoiceNo",
        "product": "StockCode",
        "date": "InvoiceDate",
        "quantity": "Quantity",
        "price": "UnitPrice",
    }
    df_mapped = map_columns(df_raw, mapping)
    return clean_data(df_mapped)


def test_load_raw(clean_df):
    """Data loads without error and has expected columns."""
    assert clean_df is not None
    assert len(clean_df) > 0
    assert "invoice" in clean_df.columns
    assert "product" in clean_df.columns
    assert "date" in clean_df.columns


def test_cleaning_removes_cancelled(clean_df):
    """Cancelled invoices (prefix C) are removed."""
    assert not clean_df["invoice"].astype(str).str.startswith("C").any()


def test_cleaning_removes_bad_qty(clean_df):
    """Zero/negative quantity rows are removed."""
    if "quantity" in clean_df.columns:
        assert (clean_df["quantity"] > 0).all()


def test_cleaning_removes_duplicates(clean_df):
    """No duplicate rows remain."""
    assert clean_df.duplicated().sum() == 0


def test_basket_matrix(clean_df):
    """Basket matrix is boolean and non-empty."""
    basket = build_basket_matrix(clean_df, min_frequency=1)
    assert isinstance(basket, pd.DataFrame)
    assert basket.shape[0] > 0
    assert basket.shape[1] > 0
    # All values should be boolean
    assert basket.stack().isin([True, False]).all()


def test_mining_and_rules(clean_df):
    """Apriori mining produces itemsets and rules."""
    basket = build_basket_matrix(clean_df, min_frequency=1)
    itemsets = mine_itemsets(basket, min_support=0.05)
    assert len(itemsets) > 0
    rules = generate_rules(itemsets, metric="lift", min_threshold=1.0)
    assert len(rules) > 0
    assert "antecedents" in rules.columns
    assert "consequents" in rules.columns
    assert "lift" in rules.columns