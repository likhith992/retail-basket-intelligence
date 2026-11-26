"""Data exploration for Retail Basket Intelligence — Phase 1 (Week 1).

Loads the sample dataset, inspects structure, cleans it, and prints summary stats.
Run with:  python notebooks/01_data_exploration.py
"""

import sys
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from src.data_loading import load_file, map_columns
from src.cleaning import clean_data


def main():
    data_path = Path("data/raw/sample_retail.csv")
    if not data_path.exists():
        print(f"❌ Data file not found: {data_path}")
        print("   Place your UCI Online Retail file at data/raw/ and update this path.")
        return

    print("=" * 60)
    print("RETAIL BASKET INTELLIGENCE — DATA EXPLORATION (Phase 1)")
    print("=" * 60)

    # 1. Load raw
    print("\n[1/4] Loading raw data...")
    df_raw = load_file(str(data_path))
    print(f"   Rows: {len(df_raw)}")
    print(f"   Columns: {list(df_raw.columns)}")
    print(f"   Memory: {df_raw.memory_usage(deep=True).sum() / 1024:.1f} KB")

    # 2. Map columns
    print("\n[2/4] Mapping columns...")
    mapping = {
        "invoice": "InvoiceNo",
        "product": "StockCode",
        "date": "InvoiceDate",
        "quantity": "Quantity",
        "price": "UnitPrice",
    }
    df_mapped = map_columns(df_raw, mapping)
    print(f"   Mapped columns: {list(df_mapped.columns)}")

    # 3. Clean
    print("\n[3/4] Cleaning data...")
    df_clean = clean_data(df_mapped)
    removed = len(df_raw) - len(df_clean)
    print(f"   Rows before cleaning: {len(df_raw)}")
    print(f"   Rows after cleaning:  {len(df_clean)}")
    print(f"   Rows removed:         {removed} ({removed / len(df_raw):.1%})")

    # 4. Inspect
    print("\n[4/4] Inspection summary...")
    print(f"   Unique invoices:   {df_clean['invoice'].nunique()}")
    print(f"   Unique products:   {df_clean['product'].nunique()}")
    print(f"   Date range:        {df_clean['date'].min()} → {df_clean['date'].max()}")
    print(f"   Top 5 products:")
    print(df_clean["product"].value_counts().head().to_string())

    print("\n✅ Phase 1 data exploration complete.")
    print(f"   Cleaned data ready for basket matrix (Week 2).")


if __name__ == "__main__":
    main()