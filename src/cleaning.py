"""Data cleaning pipeline for Retail Basket Intelligence."""

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw transaction data.

    Removes:
    - Rows with missing invoice or product
    - Cancelled invoices (InvoiceNo starting with 'C')
    - Rows with zero or negative quantity or price
    - Duplicate rows

    Args:
        df: DataFrame with standard columns (invoice, product, date, quantity, price).

    Returns:
        Cleaned DataFrame.
    """
    df = df.copy()

    # Drop missing invoice or product
    df = df.dropna(subset=["invoice", "product"])

    # Remove cancelled invoices (prefix C)
    df = df[~df["invoice"].astype(str).str.startswith("C")]

    # Remove zero or negative quantity / price if columns exist
    if "quantity" in df.columns:
        df = df[df["quantity"] > 0]
    if "price" in df.columns:
        df = df[df["price"] > 0]

    # Remove duplicates
    df = df.drop_duplicates()

    # Convert date column
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

    return df.reset_index(drop=True)