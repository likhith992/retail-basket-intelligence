"""Time-split hit-rate evaluation for Retail Basket Intelligence."""

from src.recommender import recommend


def time_split_evaluation(train_df, test_df, rules_df, k: int = 5):
    """Evaluate recommender on a time split.

    For each test basket with at least 2 items, hide one item and use the rest
    as the cart. Count a hit if the hidden item appears in top-K suggestions.

    Args:
        train_df: DataFrame used to mine rules (already mined into rules_df).
        test_df: DataFrame of test transactions (invoice, product).
        rules_df: Association rules mined from train data.
        k: Number of top suggestions.

    Returns:
        Dict with hit_rate, total_tested, hits, baseline_hit_rate.
    """
    hits = 0
    total = 0

    # Group test by invoice
    grouped = test_df.groupby("invoice")["product"].apply(list)

    for basket in grouped:
        if len(basket) < 2:
            continue
        total += 1
        hidden_item = basket[-1]
        cart = basket[:-1]
        suggestions = recommend(cart, rules_df, top_k=k)
        suggested_products = [s["product"] for s in suggestions]
        if hidden_item in suggested_products:
            hits += 1

    hit_rate = hits / total if total > 0 else 0.0

    # Popularity baseline: recommend top-k most frequent products in train
    from collections import Counter

    product_counts = Counter()
    for basket in grouped:
        product_counts.update(basket)
    baseline_products = [p for p, _ in product_counts.most_common(k)]

    baseline_hits = 0
    baseline_total = 0
    for basket in grouped:
        if len(basket) < 2:
            continue
        baseline_total += 1
        hidden_item = basket[-1]
        if hidden_item in baseline_products:
            baseline_hits += 1

    baseline_hit_rate = baseline_hits / baseline_total if baseline_total > 0 else 0.0

    return {
        "hit_rate": hit_rate,
        "baseline_hit_rate": baseline_hit_rate,
        "total_tested": total,
        "hits": hits,
        "beats_baseline": hit_rate > baseline_hit_rate,
    }