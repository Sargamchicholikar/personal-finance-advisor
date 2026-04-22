from typing import Any, Dict, List
from io import StringIO

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.smart_finance_engine import SmartFinanceEngine


app = FastAPI(title="Personal Finance Advisor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    income: float
    expenses: float
    savings: float


class ChatRequest(BaseModel):
    message: str
    income: float
    expenses: float
    risk_profile: str = "Moderate"
    goals: List[str] = []


def _offline_chat_reply(payload: ChatRequest) -> str:
    q = payload.message.lower()
    knowledge: Dict[str, str] = {
        "sip": "SIP means investing a fixed amount monthly in a mutual fund. It builds discipline and reduces market timing risk.",
        "mutual fund": "A mutual fund pools investor money and invests in market instruments. It gives diversification and professional management.",
        "inflation": "Inflation increases prices over time. Your returns should beat inflation so your money keeps real value.",
        "emergency fund": "Keep at least 6 months of expenses in safe liquid options for emergencies.",
        "fd": "Fixed Deposit is low-risk and stable, useful for short-term safety but lower long-term growth than equity.",
        "credit score": "Pay bills on time and keep credit utilization below 30% to maintain a healthy credit score.",
    }
    for k, v in knowledge.items():
        if k in q:
            return v

    savings = max(0.0, payload.income - payload.expenses)
    savings_rate = (savings / payload.income * 100) if payload.income > 0 else 0
    target = max(0.0, payload.income * 0.2 - savings)
    return (
        f"Based on your profile: savings rate is {savings_rate:.1f}%. "
        f"Try to save at least 20% of income. "
        f"Current monthly savings estimate: ₹{savings:,.0f}. "
        f"Target gap to 20%: ₹{target:,.0f}. "
        f"Risk profile considered: {payload.risk_profile}."
    )


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(req: AnalysisRequest) -> Dict[str, Any]:
    return SmartFinanceEngine.personalized_analysis(req.income, req.expenses, req.savings)


@app.post("/chat")
def chat(req: ChatRequest) -> Dict[str, Any]:
    return {"reply": _offline_chat_reply(req)}


@app.post("/expense/analyze-csv")
async def expense_analyze_csv(file: UploadFile = File(...)) -> Dict[str, Any]:
    content = await file.read()
    df = pd.read_csv(StringIO(content.decode("utf-8")))
    analysis = SmartFinanceEngine.analyze_expense_csv(df)
    return {
        "total_expense": analysis["total_expense"],
        "top_category": analysis["top_category"],
        "by_category": analysis["by_category"].to_dict(orient="records"),
        "monthly_trend": analysis["monthly_trend"].to_dict(orient="records"),
    }


@app.post("/expense/predict")
def expense_predict(payload: Dict[str, Any]) -> Dict[str, Any]:
    trend = pd.DataFrame(payload.get("monthly_trend", []))
    if trend.empty:
        return {"predicted": None, "message": "monthly_trend is required"}
    return SmartFinanceEngine.predict_next_month_expense(trend)
