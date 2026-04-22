"""Goal planning feature."""

from typing import Dict


def goal_plan(goal_amount: float, months: int) -> Dict[str, float]:
    monthly_needed = goal_amount / max(months, 1)
    return {"monthly_needed": monthly_needed}

