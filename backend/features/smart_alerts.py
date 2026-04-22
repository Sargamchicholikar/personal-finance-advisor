"""Smart alerts feature."""

from typing import Any, Dict, List, Optional


def generate_alerts(user: Any, expense_summary: Optional[Dict[str, Any]] = None) -> List[str]:
    alerts: List[str] = []
    savings = user.income - user.expenses
    savings_rate = (savings / user.income) * 100 if user.income > 0 else 0

    if savings_rate < 20:
        alerts.append(f"Your savings rate is {savings_rate:.1f}%. Aim for at least 20%.")
    if user.expenses > user.income * 0.8:
        alerts.append("Your expenses are above 80% of income. Consider reducing discretionary spending.")

    if expense_summary and not expense_summary["by_category"].empty:
        top = expense_summary["by_category"].iloc[0]
        if expense_summary["total_expense"] > 0 and (top["Amount"] / expense_summary["total_expense"]) > 0.35:
            alerts.append(
                f"You are overspending on {top['Category']} "
                f"({(top['Amount'] / expense_summary['total_expense']) * 100:.1f}% of expenses)."
            )

    return alerts

