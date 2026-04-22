"""Expense prediction feature."""

from typing import Any, Dict

import numpy as np
import pandas as pd


def predict_next_month_expense(monthly_trend_df: pd.DataFrame) -> Dict[str, Any]:
    """Predict next month expense using simple linear regression."""
    if monthly_trend_df is None or len(monthly_trend_df) < 2:
        return {"predicted": None, "message": "Need at least 2 months of data for prediction."}

    y = monthly_trend_df["Amount"].values.astype(float)
    x = np.arange(len(y))
    slope, intercept = np.polyfit(x, y, 1)
    next_x = len(y)
    prediction = max(0, slope * next_x + intercept)
    return {
        "predicted": float(prediction),
        "slope": float(slope),
        "message": "Prediction generated using linear trend.",
    }

