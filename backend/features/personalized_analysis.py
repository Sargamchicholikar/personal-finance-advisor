"""Personalized financial analysis feature."""

from typing import Any, Dict


def personalized_analysis(income: float, expenses: float, savings: float) -> Dict[str, Any]:
    """Compute personalized savings insights."""
    if income <= 0:
        return {"error": "Income should be greater than 0."}

    savings_rate = (savings / income) * 100
    expense_ratio = (expenses / income) * 100
    ideal_rate = 20.0
    gap = ideal_rate - savings_rate
    status = "on_track" if savings_rate >= ideal_rate else "below_target"
    message = (
        f"You are saving {savings_rate:.1f}% of your income, ideal is {ideal_rate:.0f}%."
        if status == "below_target"
        else f"Great! You are saving {savings_rate:.1f}% of your income, above the {ideal_rate:.0f}% benchmark."
    )

    return {
        "savings_rate": savings_rate,
        "expense_ratio": expense_ratio,
        "ideal_rate": ideal_rate,
        "gap": max(0, gap),
        "status": status,
        "message": message,
    }

