# Known Limitations & Trade-offs

| Limitation | How we handle it |
|------------|-----------------|
| Apriori slow on large data | Filter rare products first; min-support guardrail; @st.cache_data |
| Cache may show stale results | Explicit cache-busting on dataset/threshold change; timestamp display |
| Seasonality overclaimed | Disclaimer: "1 year cannot confirm yearly seasonality" |
| Evaluation baseline strong | Report honestly whether hit rate beats popularity baseline |
| Co-occurrence ≠ causation | Stated clearly in UI and report |
| No customer personalization | Stated as future scope; cart-based only |

## Trade-offs to defend in viva
- Streamlit reruns on every interaction → caching required
- mlxtend is single-machine → fits in laptop RAM for UCI dataset
- StockCode instead of Description → stable key, but some StockCodes are non-product codes