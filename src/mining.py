"""Association rule mining using mlxtend for Retail Basket Intelligence."""

import pandas as pd
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules


def mine_itemsets(basket: pd.DataFrame, min_support: float = 0.01, use_fpgrowth: bool = False):
    """Mine frequent itemsets from a boolean basket matrix.

    Args:
        basket: Boolean DataFrame (invoice x product).
        min_support: Minimum support threshold.
        use_fpgrowth: If True, use FP-Growth instead of Apriori.

    Returns:
        DataFrame of frequent itemsets with support values.
    """
    if use_fpgrowth:
        return fpgrowth(basket, min_support=min_support, use_colnames=True)
    return apriori(basket, min_support=min_support, use_colnames=True)


def generate_rules(itemsets, metric: str = "lift", min_threshold: float = 1.0):
    """Generate association rules from frequent itemsets.

    Args:
        itemsets: Output from mine_itemsets().
        metric: Metric to filter by (lift, confidence, support).
        min_threshold: Minimum threshold for the metric.

    Returns:
        DataFrame of association rules.
    """
    return association_rules(itemsets, metric=metric, min_threshold=min_threshold)