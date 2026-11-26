"""Time-aware association rule comparison for Retail Basket Intelligence."""

import pandas as pd


def split_into_periods(df: pd.DataFrame, period_length: str = "M") -> dict:
    """Split data into equal-length time periods.

    Args:
        df: Cleaned DataFrame with a 'date' column.
        period_length: Pandas offset alias (e.g., 'M' monthly, 'Q' quarterly).

    Returns:
        Dict mapping period label to DataFrame for that period.
    """
    df = df.copy()
    df["period"] = df["date"].dt.to_period(period_length)
    periods = {}
    for period, group in df.groupby("period"):
        periods[str(period)] = group.drop(columns=["period"])
    return periods


def label_rule_stability(rule_presence: dict) -> str:
    """Label a rule as stable, emerging, fading, or seasonal.

    rule_presence: Dict mapping period label to bool (rule present?).

    Returns:
        One of: 'stable', 'emerging', 'fading', 'seasonal', 'single_period'.
    """
    periods = sorted(rule_presence.keys())
    present = [rule_presence[p] for p in periods]

    if not any(present):
        return "absent"
    if all(present):
        return "stable"
    if present == [False] * (len(present) - 1) + [True]:
        return "emerging"
    if present == [True] + [False] * (len(present) - 1):
        return "fading"
    return "seasonal"