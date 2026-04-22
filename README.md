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

## HTML/CSS/JS + FastAPI Mode (Vercel-style architecture)

This repo now also includes:

- `api/main.py` (FastAPI backend)
- `web/index.html`, `web/style.css`, `web/app.js` (plain frontend)

### Run API backend

```powershell
python -m uvicorn api.main:app --reload --port 8000
```

### Run static frontend

Open `web/index.html` directly in browser, or serve with a static server.

Example (Python):

```powershell
cd web
python -m http.server 5500
```

Then open:
- Frontend: `http://127.0.0.1:5500`
- API docs: `http://127.0.0.1:8000/docs`

## Vercel Deployment (HTML/CSS/JS + FastAPI)

This project includes `vercel.json` and is ready for Vercel using:
- Static frontend from `web/`
- Python serverless API from `api/main.py`

### Steps

1. Push latest code to GitHub.
2. In Vercel, import your GitHub repository.
3. Use default settings (no special build command required).
4. Deploy.

### Routes after deployment

- `/` -> web frontend
- `/health` -> API health check
- `/analyze` -> personalized analysis
- `/chat` -> offline chat endpoint
- `/expense/analyze-csv` -> CSV analysis
- `/expense/predict` -> prediction endpoint

### Quick check

After deploy, open:
- `https://<your-app>.vercel.app/`
- `https://<your-app>.vercel.app/health` (should return status json)