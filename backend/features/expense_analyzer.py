"""Expense analyzer feature with CSV categorization."""

from typing import Any, Dict, List

import pandas as pd


CATEGORY_KEYWORDS: Dict[str, List[str]] = {
    "Food": ["swiggy", "zomato", "restaurant", "cafe", "food", "grocery", "blinkit", "zepto", "instamart"],
    "Travel": ["uber", "ola", "metro", "irctc", "flight", "petrol", "diesel", "rapido", "taxi"],
    "Shopping": ["amazon", "flipkart", "myntra", "ajio", "mall", "shopping"],
    "Rent": ["rent", "landlord", "housing"],
    "Utilities": ["electricity", "water", "gas", "wifi", "broadband", "mobile", "recharge"],
    "Healthcare": ["hospital", "pharmacy", "medicine", "clinic", "health"],
    "Entertainment": ["netflix", "prime", "spotify", "movie", "bookmyshow"],
    "Education": ["course", "udemy", "coursera", "fees", "school", "college"],
}


def categorize_expense(description: str) -> str:
    text = str(description).lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return category
    return "Others"


def analyze_expense_csv(df: pd.DataFrame) -> Dict[str, Any]:
    """Analyze uploaded statement CSV with flexible column mapping."""
    cols = {c.lower(): c for c in df.columns}
    amount_col = None
    desc_col = None
    date_col = None

    for key in ["amount", "amt", "debit", "transaction_amount", "value"]:
        if key in cols:
            amount_col = cols[key]
            break
    for key in ["description", "narration", "merchant", "details", "transaction"]:
        if key in cols:
            desc_col = cols[key]
            break
    for key in ["date", "transaction_date", "txn_date", "value_date"]:
        if key in cols:
            date_col = cols[key]
            break

    if amount_col is None:
        raise ValueError("CSV must contain an amount-like column (amount/debit/amt).")
    if desc_col is None:
        desc_col = amount_col

    clean_df = df.copy()
    clean_df[amount_col] = pd.to_numeric(clean_df[amount_col], errors="coerce").fillna(0)
    clean_df = clean_df[clean_df[amount_col] > 0]
    clean_df["Category"] = clean_df[desc_col].apply(categorize_expense)

    monthly_trend = pd.DataFrame()
    if date_col:
        clean_df[date_col] = pd.to_datetime(clean_df[date_col], errors="coerce")
        valid_dates = clean_df.dropna(subset=[date_col]).copy()
        if not valid_dates.empty:
            valid_dates["Month"] = valid_dates[date_col].dt.to_period("M").astype(str)
            monthly_trend = (
                valid_dates.groupby("Month")[amount_col]
                .sum()
                .reset_index()
                .rename(columns={amount_col: "Amount"})
            )

    by_category = (
        clean_df.groupby("Category")[amount_col]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={amount_col: "Amount"})
    )

    return {
        "clean_df": clean_df,
        "total_expense": float(clean_df[amount_col].sum()),
        "by_category": by_category,
        "monthly_trend": monthly_trend,
        "top_category": by_category.iloc[0]["Category"] if not by_category.empty else "N/A",
    }

