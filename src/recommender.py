"""Explainable cart recommendations for Retail Basket Intelligence."""


def recommend(cart: list, rules_df, top_k: int = 5):
    """Recommend products based on rules whose antecedent is in the cart.

    Args:
        cart: List of product codes (antecedents must be subsets of cart).
        rules_df: DataFrame from generate_rules() with antecedents, consequents, support, confidence, lift.
        top_k: Number of top recommendations to return.

    Returns:
        List of dicts with product, reason, support, confidence, lift, triggered_by.
    """
    cart_set = set(cart)
    suggestions = {}

    for _, rule in rules_df.iterrows():
        antecedents = set(rule["antecedents"])
        consequents = set(rule["consequents"])

        # Rule applies only if full antecedent is in cart
        if not antecedents.issubset(cart_set):
            continue

        # Skip items already in cart
        new_items = consequents - cart_set
        for item in new_items:
            reason = (
                f"Customers who bought {', '.join(antecedents)} also bought {item} "
                f"in {rule['support']:.0%} of baskets "
                f"(confidence {rule['confidence']:.0%}, lift {rule['lift']:.2f}). "
                f"Triggered by: {', '.join(antecedents)}."
            )

            if item not in suggestions or rule["lift"] > suggestions[item]["lift"]:
                suggestions[item] = {
                    "product": item,
                    "reason": reason,
                    "support": rule["support"],
                    "confidence": rule["confidence"],
                    "lift": rule["lift"],
                    "triggered_by": ", ".join(antecedents),
                }

    ranked = sorted(suggestions.values(), key=lambda x: x["lift"], reverse=True)
    return ranked[:top_k]