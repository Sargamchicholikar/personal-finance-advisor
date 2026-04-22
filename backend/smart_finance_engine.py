"""Facade over feature-specific backend modules."""

from typing import Any, Dict, List, Optional

import pandas as pd

from backend.features.chat_memory import extract_memory_from_text
from backend.features.deep_learning_forecast import run_deep_learning_forecast
from backend.features.expense_analyzer import analyze_expense_csv, categorize_expense
from backend.features.expense_prediction import predict_next_month_expense
from backend.features.goal_planning import goal_plan
from backend.features.investment_suggestion import investment_suggestion
from backend.features.personalized_analysis import personalized_analysis
from backend.features.smart_alerts import generate_alerts


class SmartFinanceEngine:
    """Facade class to keep frontend API stable."""

    @staticmethod
    def personalized_analysis(income: float, expenses: float, savings: float) -> Dict[str, Any]:
        return personalized_analysis(income, expenses, savings)

    @staticmethod
    def categorize_expense(description: str) -> str:
        return categorize_expense(description)

    @staticmethod
    def analyze_expense_csv(df: pd.DataFrame) -> Dict[str, Any]:
        return analyze_expense_csv(df)

    @staticmethod
    def predict_next_month_expense(monthly_trend_df: pd.DataFrame) -> Dict[str, Any]:
        return predict_next_month_expense(monthly_trend_df)

    @staticmethod
    def generate_alerts(user: Any, expense_summary: Optional[Dict[str, Any]] = None) -> List[str]:
        return generate_alerts(user, expense_summary)

    @staticmethod
    def goal_plan(goal_amount: float, months: int) -> Dict[str, float]:
        return goal_plan(goal_amount, months)

    @staticmethod
    def investment_suggestion(risk_profile: str) -> str:
        return investment_suggestion(risk_profile)

    @staticmethod
    def extract_memory_from_text(text: str) -> Dict[str, float]:
        return extract_memory_from_text(text)

    @staticmethod
    def run_deep_learning_forecast(monthly_trend_df: pd.DataFrame, window: int = 3) -> Dict[str, Any]:
        return run_deep_learning_forecast(monthly_trend_df, window)
