"""Retail Basket Intelligence - Streamlit Dashboard."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd

from src.data_loading import load_file, map_columns
from src.cleaning import clean_data
from src.basket_matrix import build_basket_matrix
from src.mining import mine_itemsets, generate_rules
from src.time_compare import split_into_periods, label_rule_stability
from src.recommender import recommend
from src.evaluation import time_split_evaluation
from src.utils import cache_key, timestamp

st.set_page_config(page_title="Retail Basket Intelligence", layout="wide")
st.title("🛒 Retail Basket Intelligence")

# ---- Session state for caching ----
if "df_raw" not in st.session_state:
    st.session_state.df_raw = None
if "df_clean" not in st.session_state:
    st.session_state.df_clean = None
if "basket" not in st.session_state:
    st.session_state.basket = None
if "rules" not in st.session_state:
    st.session_state.rules = None
if "computed_at" not in st.session_state:
    st.session_state.computed_at = None


# ===================== TAB 1: Upload & Map =====================
tab_upload, tab_explore, tab_rules, tab_time, tab_recommend, tab_eval = st.tabs(
    ["1. Upload & Map", "2. Explore", "3. Rules", "4. Time Compare", "5. Recommend", "6. Evaluation"]
)

with tab_upload:
    st.header("Upload & Map Columns")
    uploaded = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])
    if uploaded is not None:
        df_raw = load_file(uploaded.name)
        st.session_state.df_raw = df_raw
        st.success(f"Loaded {len(df_raw)} rows")

        st.subheader("Column Mapping")
        cols = df_raw.columns.tolist()
        mapping = {}
        col1, col2, col3 = st.columns(3)
        with col1:
            mapping["invoice"] = st.selectbox("Invoice ID column", cols, index=0)
        with col2:
            mapping["product"] = st.selectbox("Product column", cols, index=1 if len(cols) > 1 else 0)
        with col3:
            mapping["date"] = st.selectbox("Date column", cols, index=2 if len(cols) > 2 else 0)
        if "quantity" in cols:
            mapping["quantity"] = st.selectbox("Quantity column (optional)", ["None"] + cols, index=0)
        if "price" in cols:
            mapping["price"] = st.selectbox("Price column (optional)", ["None"] + cols, index=0)

        if st.button("Apply Mapping & Clean"):
            df_mapped = map_columns(df_raw, mapping)
            df_clean = clean_data(df_mapped)
            st.session_state.df_clean = df_clean
            st.session_state.computed_at = timestamp()
            st.success(f"Cleaned: {len(df_clean)} rows remaining (removed {len(df_raw) - len(df_clean)})")
            st.dataframe(df_clean.head())

# ===================== TAB 2: Explore =====================
with tab_explore:
    st.header("Explore Data")
    if st.session_state.df_clean is None:
        st.info("Please upload and clean data first.")
    else:
        df = st.session_state.df_clean
        st.metric("Total transactions", len(df))
        st.metric("Unique products", df["product"].nunique())
        st.metric("Date range", f"{df['date'].min().date()} to {df['date'].max().date()}")

        st.subheader("Top Products")
        top = df["product"].value_counts().head(10)
        st.bar_chart(top)

        st.subheader("Sales Over Time")
        daily = df.set_index("date").resample("D").size()
        st.line_chart(daily)

# ===================== TAB 3: Rules =====================
with tab_rules:
    st.header("Association Rules")
    if st.session_state.df_clean is None:
        st.info("Please upload and clean data first.")
    else:
        min_support = st.slider("Min support", 0.001, 0.1, 0.01, step=0.001)
        min_confidence = st.slider("Min confidence", 0.1, 1.0, 0.5, step=0.05)
        min_lift = st.slider("Min lift", 1.0, 5.0, 1.0, step=0.1)
        use_fpgrowth = st.checkbox("Use FP-Growth (optional comparison)")

        if st.button("Mine Rules"):
            basket = build_basket_matrix(st.session_state.df_clean)
            st.session_state.basket = basket
            itemsets = mine_itemsets(basket, min_support=min_support, use_fpgrowth=use_fpgrowth)
            rules = generate_rules(itemsets, metric="lift", min_threshold=min_lift)
            rules = rules[rules["confidence"] >= min_confidence]
            st.session_state.rules = rules
            st.session_state.computed_at = timestamp()
            st.success(f"Mined {len(rules)} rules")

        if st.session_state.rules is not None:
            st.dataframe(st.session_state.rules.head(20))
            st.caption(f"Last computed: {st.session_state.computed_at}")

# ===================== TAB 4: Time Compare =====================
with tab_time:
    st.header("Time-Aware Rule Comparison")
    st.info("Coming soon: stable / emerging / fading rule labels over equal-length periods.")

# ===================== TAB 5: Recommend =====================
with tab_recommend:
    st.header("Explainable Cart Recommendations")
    if st.session_state.rules is None:
        st.info("Please mine rules first.")
    else:
        products = sorted(st.session_state.rules["antecedents"].explode().unique())
        cart = st.multiselect("Select products for cart", products)
        if st.button("Get Recommendations"):
            recs = recommend(cart, st.session_state.rules, top_k=5)
            for r in recs:
                st.write(f"• **{r['product']}** — {r['reason']}")

# ===================== TAB 6: Evaluation =====================
with tab_eval:
    st.header("Time-Split Evaluation")
    st.info("Coming soon: hit rate at K vs popularity baseline.")

st.divider()
st.caption(f"Retail Basket Intelligence — Last updated: {st.session_state.computed_at or 'not yet'}")