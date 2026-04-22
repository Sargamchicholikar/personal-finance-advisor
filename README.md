# Personal Finance Advisor

AI/ML-powered personal finance advisor with expense analytics, forecasting, smart alerts, and a free offline chatbot mode.

## Features

- Personalized financial analysis (salary, expenses, savings insights)
- Expense analyzer from CSV bank statement
  - spending categorization
  - category pie chart
  - monthly trend chart
- Expense prediction
  - linear regression baseline
  - deep-learning-style forecasting (NumPy MLP)
  - MAE comparison vs baseline
- Context-aware chatbot memory
- Smart alerts and insights (overspending, low savings, etc.)
- Goal-based planning
- Rule-based investment suggestions
- Gamification dashboard
- Multi-provider chatbot support:
  - Offline (No API Key) - fully free
  - Gemini API
  - OpenRouter API

## Project Structure

```text
personal-finance-advisor/
├─ indian_finance_advisor.py
├─ requirements.txt
├─ data/
│  └─ sample_bank_statement.csv
├─ backend/
│  ├─ smart_finance_engine.py
│  └─ features/
│     ├─ personalized_analysis.py
│     ├─ expense_analyzer.py
│     ├─ expense_prediction.py
│     ├─ deep_learning_forecast.py
│     ├─ smart_alerts.py
│     ├─ goal_planning.py
│     ├─ investment_suggestion.py
│     └─ chat_memory.py
└─ frontend/
   └─ pages/
      ├─ dashboard_page.py
      ├─ ai_chat_page.py
      ├─ smart_features_page.py
      ├─ portfolio_page.py
      ├─ gamification_page.py
      ├─ settings_page.py
      └─ layout.py
```

## Installation (Windows / PowerShell)

```powershell
cd "C:\Users\Sargam\Desktop\personal-finance-advisor"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
```

## Run App

```powershell
python -m streamlit run indian_finance_advisor.py
```

Open: `http://localhost:8501`

## How to Use

1. Go to **Settings** and complete profile + portfolio.
2. In **API Configuration**, choose one provider:
   - **Offline (No API Key)** (recommended free mode)
   - Gemini
   - OpenRouter
3. Upload `data/sample_bank_statement.csv` in **Smart Features -> Expense Analyzer**.
4. Check:
   - **Predictions & Alerts**
   - **Deep Learning Forecast**
   - **AI Advisor Chat**

## Dataset

Sample dataset included:

- `data/sample_bank_statement.csv`

Columns:
- `Date`
- `Description`
- `Amount`

## Tech Stack

- Python
- Streamlit
- Pandas / NumPy / SciPy
- Plotly
- yFinance
- Google Generative AI SDK
- OpenRouter (optional)

## Notes

- Offline chatbot mode works without any API key.
- For Gemini/OpenRouter providers, valid API keys are required.
- This project is suitable for AI/ML academic demos with practical fintech use cases.