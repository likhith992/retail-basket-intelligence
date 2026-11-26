"""Basket matrix builder for Retail Basket Intelligence."""

import pandas as pd


def build_basket_matrix(df: pd.DataFrame, min_frequency: int = 5) -> pd.DataFrame:
    """Convert cleaned transactions into a boolean basket matrix.

    One row per invoice, one column per product (StockCode).
    Cells are True/False indicating product presence in the invoice.

    Rare products below min_frequency are filtered out to save memory.

    Args:
        df: Cleaned DataFrame with invoice, product, date columns.
        min_frequency: Minimum number of baskets a product must appear in.

    Returns:
        Boolean DataFrame (invoice x product).
    """
    # Filter rare products
    product_counts = df["product"].value_counts()
    frequent_products = product_counts[product_counts >= min_frequency].index
    df = df[df["product"].isin(frequent_products)]

    # Build boolean matrix
    basket = (
        df.groupby(["invoice", "product"])
        .size()
        .unstack(fill_value=0)
        .astype(bool)
    )

    return basket