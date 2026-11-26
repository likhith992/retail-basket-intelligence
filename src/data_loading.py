"""Data loading and column mapping for Retail Basket Intelligence."""

import pandas as pd


def load_file(file_path: str) -> pd.DataFrame:
    """Load a CSV or Excel file into a DataFrame.

    Args:
        file_path: Path to .csv or .xlsx file.

    Returns:
        Raw DataFrame as loaded from disk.
    """
    if file_path.endswith((".xlsx", ".xls")):
        return pd.read_excel(file_path, engine="openpyxl")
    return pd.read_csv(file_path)


def map_columns(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """Rename user-selected columns to standard names.

    Expected standard names: invoice, product, date, quantity, price.
    mapping keys are standard names; values are the user's column names.

    Args:
        df: Raw DataFrame.
        mapping: Dict like {"invoice": "InvoiceNo", "product": "StockCode", ...}

    Returns:
        DataFrame with renamed columns.
    """
    rename_map = {v: k for k, v in mapping.items() if v in df.columns}
    return df.rename(columns=rename_map)