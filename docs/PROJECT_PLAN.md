# Project Plan — Retail Basket Intelligence

## Scope
College mini project, 4 students, 6 weeks, demo to lecturers.

## Pipeline
1. Upload & map columns
2. Clean data
3. Build basket matrix (StockCode key)
4. Mine frequent itemsets (Apriori / optional FP-Growth)
5. Generate association rules
6. Time-aware comparison (stable/emerging/fading)
7. Explainable cart recommendations
8. Time-split hit-rate evaluation
9. Streamlit dashboard presentation

## Stack
Python, Pandas, NumPy, mlxtend, Plotly, Streamlit, openpyxl

## Limitations (honest disclosure)
- Rules show co-occurrence, not causation
- Not personalized to individual customers
- Batch-only (no real-time updates)
- ~1 year of UCI data (seasonality cannot be confirmed)
- Streamlit is single-user demo grade, not production multi-user