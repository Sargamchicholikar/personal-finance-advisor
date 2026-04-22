# Indian Personal Finance Advisor System
# Complete LLM-Powered Financial Advisory Platform with Gemini 2.5 Pro

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time
import hashlib
import random
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import yfinance as yf
import requests
from scipy.optimize import minimize
import google.generativeai as genai
import warnings
from backend.smart_finance_engine import SmartFinanceEngine
from frontend.pages.ai_chat_page import render_ai_chat as render_ai_chat_page
from frontend.pages.dashboard_page import render_dashboard as render_dashboard_page
from frontend.pages.gamification_page import render_gamification as render_gamification_page
from frontend.pages.layout import render_header as render_header_page, render_sidebar as render_sidebar_page
from frontend.pages.portfolio_page import render_portfolio as render_portfolio_page
from frontend.pages.settings_page import render_settings as render_settings_page
from frontend.pages.smart_features_page import render_smart_features as render_smart_features_page
warnings.filterwarnings('ignore')

# ======================== Configuration ========================
class Config:
    """System Configuration"""
    APP_NAME = "WealthWise India"
    VERSION = "2.0.0"
    
    # Indian Market Indices
    INDIAN_INDICES = {
        "NIFTY50": "^NSEI",
        "SENSEX": "^BSESN",
        "BANKNIFTY": "^NSEBANK",
        "NIFTYIT": "^CNXIT"
    }
    
    # Indian Stock Universe
    INDIAN_STOCKS = {
        "RELIANCE": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "HDFCBANK": "HDFCBANK.NS",
        "INFY": "INFY.NS",
        "ICICIBANK": "ICICIBANK.NS",
        "HINDUNILVR": "HINDUNILVR.NS",
        "ITC": "ITC.NS",
        "SBIN": "SBIN.NS",
        "BHARTIARTL": "BHARTIARTL.NS",
        "KOTAKBANK": "KOTAKBANK.NS",
        "LT": "LT.NS",
        "ASIANPAINT": "ASIANPAINT.NS",
        "WIPRO": "WIPRO.NS",
        "MARUTI": "MARUTI.NS",
        "TITAN": "TITAN.NS"
    }
    
    # Indian Mutual Fund Categories
    MF_CATEGORIES = {
        "Large Cap": ["Axis Bluechip", "SBI Blue Chip", "Mirae Large Cap"],
        "Mid Cap": ["HDFC Mid-Cap", "DSP Midcap", "Kotak Emerging"],
        "Small Cap": ["Nippon Small Cap", "SBI Small Cap", "Axis Small Cap"],
        "ELSS": ["Axis Tax Saver", "Mirae Tax Saver", "DSP Tax Saver"],
        "Debt": ["HDFC Short Term", "ICICI Liquid", "Axis Banking"],
        "Hybrid": ["HDFC Balanced", "SBI Equity Hybrid", "Canara Hybrid"]
    }
    
    # Tax Slabs (Old Regime)
    TAX_SLABS = {
        250000: 0,
        500000: 0.05,
        1000000: 0.20,
        float('inf'): 0.30
    }
    
    # Indian Financial Goals
    FINANCIAL_GOALS = [
        "Retirement Planning",
        "Children's Education",
        "Children's Marriage",
        "Home Purchase",
        "Car Purchase",
        "Emergency Fund",
        "Vacation Planning",
        "Parent's Healthcare",
        "Gold Investment",
        "Starting Business"
    ]

# ======================== Data Models ========================
@dataclass
class User:
    """User Profile Model"""
    user_id: str
    name: str
    age: int
    income: float
    expenses: float
    risk_profile: str
    financial_goals: List[str]
    investment_experience: str
    family_size: int
    city_tier: int  # 1, 2, or 3
    has_insurance: bool
    has_emergency_fund: bool
    wealth_score: int = 0
    badges: List[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.badges is None:
            self.badges = []
        if self.created_at is None:
            self.created_at = datetime.now()

@dataclass
class Portfolio:
    """Investment Portfolio Model"""
    user_id: str
    stocks: Dict[str, float]
    mutual_funds: Dict[str, float]
    fixed_deposits: float
    ppf: float
    nps: float
    gold: float
    real_estate: float
    crypto: float
    cash: float
    elss: float = 0  # ELSS for tax saving
    total_value: float = 0
    
    def calculate_total(self):
        self.total_value = (
            sum(self.stocks.values()) +
            sum(self.mutual_funds.values()) +
            self.fixed_deposits +
            self.ppf +
            self.nps +
            self.gold +
            self.real_estate +
            self.crypto +
            self.cash +
            self.elss
        )
        return self.total_value

@dataclass
class FinancialAdvice:
    """Financial Advice Model"""
    category: str
    priority: str
    advice: str
    action_items: List[str]
    potential_savings: float
    risk_level: str
    timeline: str

# ======================== Market Data Manager ========================
class MarketDataManager:
    """Handles real-time market data for Indian markets"""
    
    @staticmethod
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_market_data(symbol: str) -> Dict:
        """Fetch real-time market data"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1mo")
            
            return {
                "symbol": symbol,
                "current_price": info.get("currentPrice", hist['Close'][-1]),
                "change_percent": ((hist['Close'][-1] - hist['Close'][-2]) / hist['Close'][-2] * 100),
                "volume": info.get("volume", hist['Volume'][-1]),
                "market_cap": info.get("marketCap", 0),
                "pe_ratio": info.get("trailingPE", 0),
                "dividend_yield": info.get("dividendYield", 0),
                "week_52_high": info.get("fiftyTwoWeekHigh", max(hist['High'])),
                "week_52_low": info.get("fiftyTwoWeekLow", min(hist['Low'])),
                "history": hist
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def get_indian_market_sentiment() -> Dict:
        """Analyze Indian market sentiment"""
        try:
            nifty = MarketDataManager.get_market_data("^NSEI")
            sensex = MarketDataManager.get_market_data("^BSESN")
            
            # Calculate sentiment score
            nifty_change = nifty.get("change_percent", 0)
            sensex_change = sensex.get("change_percent", 0)
            avg_change = (nifty_change + sensex_change) / 2
            
            if avg_change > 1:
                sentiment = "Bullish"
                color = "green"
            elif avg_change < -1:
                sentiment = "Bearish"
                color = "red"
            else:
                sentiment = "Neutral"
                color = "yellow"
            
            return {
                "sentiment": sentiment,
                "color": color,
                "nifty_change": nifty_change,
                "sensex_change": sensex_change,
                "avg_change": avg_change,
                "recommendation": "Consider investing" if sentiment == "Bearish" else "Book partial profits" if sentiment == "Bullish" else "Hold positions"
            }
        except:
            return {"sentiment": "Unknown", "color": "gray"}

# ======================== Portfolio Optimizer ========================
class PortfolioOptimizer:
    """Advanced portfolio optimization for Indian markets"""
    
    def __init__(self):
        self.risk_free_rate = 0.0625  # Indian 10-year bond yield
    
    def optimize_portfolio(self, stocks: List[str], risk_tolerance: str) -> Dict:
        """Optimize portfolio using Modern Portfolio Theory"""
        try:
            # Download historical data - try different column names
            data = yf.download(stocks, period="1y", progress=False)
            
            # Check if data is multi-level columns (multiple stocks)
            if len(stocks) > 1:
                # Try to get Close prices
                if 'Close' in data.columns.levels[0]:
                    prices = data['Close']
                elif 'Adj Close' in data.columns.levels[0]:
                    prices = data['Adj Close']
                else:
                    # If neither exists, try to get any price data
                    prices = data.iloc[:, :len(stocks)]
            else:
                # Single stock
                if 'Close' in data.columns:
                    prices = data[['Close']]
                elif 'Adj Close' in data.columns:
                    prices = data[['Adj Close']]
                else:
                    prices = data.iloc[:, [0]]
            
            # Ensure we have data
            if prices.empty or len(prices) < 30:
                return {"success": False, "error": "Insufficient historical data for selected stocks"}
            
            # Calculate returns and covariance
            returns = prices.pct_change().dropna()
            mean_returns = returns.mean() * 252  # Annualized
            cov_matrix = returns.cov() * 252
            
            # Define risk levels
            risk_levels = {
                "Conservative": 0.10,
                "Moderate": 0.15,
                "Aggressive": 0.25
            }
            target_risk = risk_levels.get(risk_tolerance, 0.15)
            
            # Optimization
            num_assets = len(stocks)
            
            def portfolio_stats(weights):
                portfolio_return = np.sum(mean_returns * weights)
                portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
                sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_std if portfolio_std > 0 else 0
                return portfolio_std, portfolio_return, sharpe_ratio
            
            def minimize_negative_sharpe(weights):
                return -portfolio_stats(weights)[2]
            
            # Constraints and bounds
            constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            bounds = tuple((0, 0.4) for _ in range(num_assets))  # Max 40% in single stock
            initial_guess = num_assets * [1. / num_assets]
            
            # Optimize
            result = minimize(minimize_negative_sharpe, initial_guess, 
                            method='SLSQP', bounds=bounds, constraints=constraints)
            
            if result.success:
                optimal_weights = result.x
                risk, returns_val, sharpe = portfolio_stats(optimal_weights)
                
                return {
                    "success": True,
                    "weights": dict(zip(stocks, optimal_weights)),
                    "expected_return": returns_val * 100,
                    "risk": risk * 100,
                    "sharpe_ratio": sharpe,
                    "allocation": {stock: f"{weight*100:.1f}%" 
                                 for stock, weight in zip(stocks, optimal_weights)}
                }
            else:
                return {"success": False, "error": "Optimization failed to converge"}
                
        except Exception as e:
            return {"success": False, "error": f"Error in optimization: {str(e)}"}

# ======================== Behavioral Analysis ========================
class BehavioralAnalyzer:
    """Analyzes and detects behavioral biases"""
    
    def __init__(self):
        self.bias_patterns = {
            "loss_aversion": {
                "indicators": ["holding losses", "selling winners early", "avoid risk"],
                "score_threshold": 0.7
            },
            "anchoring": {
                "indicators": ["fixated on purchase price", "ignores new info", "reference old data"],
                "score_threshold": 0.6
            },
            "recency": {
                "indicators": ["recent performance focus", "ignores long term", "momentum chasing"],
                "score_threshold": 0.65
            },
            "overconfidence": {
                "indicators": ["excessive trading", "ignores diversification", "timing market"],
                "score_threshold": 0.7
            }
        }
    
    def detect_biases(self, user_behavior: Dict) -> List[Dict]:
        """Detect behavioral biases from user actions"""
        detected_biases = []
        
        # Analyze trading frequency
        if user_behavior.get("monthly_trades", 0) > 20:
            detected_biases.append({
                "bias": "overconfidence",
                "severity": "high",
                "message": "Your high trading frequency suggests overconfidence bias",
                "intervention": "Consider reducing trades to 5-10 per month"
            })
        
        # Analyze holding patterns
        if user_behavior.get("avg_loss_holding_days", 0) > user_behavior.get("avg_profit_holding_days", 0):
            detected_biases.append({
                "bias": "loss_aversion",
                "severity": "medium",
                "message": "You hold losing positions longer than winning ones",
                "intervention": "Set stop-losses at 8-10% and let winners run"
            })
        
        # Analyze recent focus
        if user_behavior.get("queries_about_recent_performers", 0) > 5:
            detected_biases.append({
                "bias": "recency",
                "severity": "medium",
                "message": "You're focusing too much on recent market performers",
                "intervention": "Look at 3-5 year performance, not just recent months"
            })
        
        return detected_biases
    
    def get_behavioral_score(self, biases: List[Dict]) -> int:
        """Calculate behavioral score (0-100)"""
        if not biases:
            return 100
        
        total_penalty = sum(
            30 if b["severity"] == "high" else 15 
            for b in biases
        )
        return max(0, 100 - total_penalty)

# ======================== Gemini AI Advisor ========================
class GeminiFinanceAdvisor:
    """LLM-powered financial advisor using Gemini"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model_name = self._select_supported_model_name()
        self.model = genai.GenerativeModel(self.model_name)
        self.conversation_history = []

    def _select_supported_model_name(self) -> str:
        """Pick a model that supports generateContent for current account/version."""
        preferred = [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-1.5-flash-latest",
            "gemini-1.5-pro-latest",
        ]
        try:
            available = []
            for m in genai.list_models():
                if "generateContent" in getattr(m, "supported_generation_methods", []):
                    name = str(getattr(m, "name", ""))
                    if name.startswith("models/"):
                        name = name.split("/", 1)[1]
                    if name:
                        available.append(name)
            for candidate in preferred:
                if candidate in available:
                    return candidate
            if available:
                return available[0]
        except Exception:
            pass

        # Last resort fallback
        return "gemini-1.5-flash"
        
    def get_indian_context_prompt(self, user: User) -> str:
        """Create India-specific context for the LLM"""
        return f"""You are an expert Indian Personal Finance Advisor with deep knowledge of:
        - Indian tax laws (Old and New tax regimes)
        - Indian investment options (Stocks, MFs, FDs, PPF, NPS, Gold, Real Estate)
        - Indian market conditions and economic factors
        - Cultural financial preferences (gold investment, family support, festivals)
        - Indian regulatory framework (SEBI, RBI, IRDAI)
        
        User Profile:
        - Age: {user.age} years
        - Monthly Income: ₹{user.income:,.0f}
        - Monthly Expenses: ₹{user.expenses:,.0f}
        - City Tier: {user.city_tier}
        - Family Size: {user.family_size}
        - Risk Profile: {user.risk_profile}
        - Goals: {', '.join(user.financial_goals)}
        - Investment Experience: {user.investment_experience}
        
        Provide advice that is:
        1. Culturally relevant to Indian families
        2. Tax-optimized for Indian tax laws
        3. Considers Indian inflation (~6-7% annually)
        4. Includes Indian-specific instruments (PPF, NPS, ELSS)
        5. Accounts for family obligations and festivals
        """
    
    def get_advice(self, query: str, user: User, portfolio: Optional[Portfolio] = None) -> str:
        """Get personalized financial advice"""
        try:
            # Build comprehensive context
            context = self.get_indian_context_prompt(user)
            
            if portfolio:
                context += f"""
                
                Current Portfolio:
                - Stocks: ₹{sum(portfolio.stocks.values()):,.0f}
                - Mutual Funds: ₹{sum(portfolio.mutual_funds.values()):,.0f}
                - ELSS (Tax Saving): ₹{portfolio.elss:,.0f}
                - Fixed Deposits: ₹{portfolio.fixed_deposits:,.0f}
                - PPF: ₹{portfolio.ppf:,.0f}
                - NPS: ₹{portfolio.nps:,.0f}
                - Gold: ₹{portfolio.gold:,.0f}
                - Total Portfolio: ₹{portfolio.total_value:,.0f}
                """
            
            # Add market context
            market_sentiment = MarketDataManager.get_indian_market_sentiment()
            context += f"""
            
            Current Market Conditions:
            - Market Sentiment: {market_sentiment['sentiment']}
            - NIFTY Change: {market_sentiment.get('nifty_change', 0):.2f}%
            - SENSEX Change: {market_sentiment.get('sensex_change', 0):.2f}%
            """
            
            # Create prompt
            prompt = f"""{context}
            
            User Query: {query}
            
            Provide specific, actionable advice considering:
            1. Tax implications (Section 80C, 80D, LTCG, STCG)
            2. Indian market opportunities
            3. Risk management
            4. Family financial planning
            5. Emergency fund (6-12 months expenses)
            6. Insurance needs (term, health)
            
            Format your response with:
            - Clear action items
            - Specific investment amounts
            - Timeline for implementation
            - Expected returns/benefits
            - Risk considerations
            """
            
            response = self.model.generate_content(prompt)
            text = getattr(response, "text", None)
            if not text:
                text = "I could not generate a full response. Please try again with a shorter query."
            self.conversation_history.append({"query": query, "response": text})
            return text
            
        except Exception as e:
            err = str(e).lower()
            if "429" in err or "quota" in err or "rate limit" in err:
                return (
                    "Gemini API quota is exhausted for your current key/project.\n\n"
                    "Quick fix:\n"
                    "1) Open Google AI Studio billing/quota page and enable a plan.\n"
                    "2) Or create a new API key under a project with available quota.\n"
                    "3) Wait for cooldown and retry.\n\n"
                    f"Meanwhile, basic guidance from your profile:\n"
                    f"- Monthly income: ₹{user.income:,.0f}\n"
                    f"- Monthly expenses: ₹{user.expenses:,.0f}\n"
                    f"- Savings target: at least 20% of income."
                )
            return f"Error getting advice: {str(e)}. Please check API key/model access."
    
    def analyze_tax_savings(self, user: User, income_details: Dict) -> str:
        """Provide tax optimization strategies"""
        prompt = f"""As an Indian tax expert, analyze tax saving opportunities for:
        
        Annual Income: ₹{user.income * 12:,.0f}
        Age: {user.age}
        
        Provide:
        1. Comparison between Old and New tax regime
        2. Section 80C investments (₹1.5 lakh limit)
        3. Section 80D (Health Insurance)
        4. Section 80E (Education Loan)
        5. Section 80G (Donations)
        6. HRA benefits if applicable
        7. NPS additional ₹50,000 benefit
        
        Calculate exact tax liability in both regimes and recommend the best approach.
        Include specific investment products and amounts.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error analyzing tax: {str(e)}"


class OpenRouterFinanceAdvisor:
    """LLM advisor using OpenRouter (OpenAI-compatible API)."""

    def __init__(self, api_key: str, model: str = "meta-llama/llama-3.1-8b-instruct:free"):
        self.api_key = api_key
        self.model_name = model
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.conversation_history = []

    def _chat(self, system_prompt: str, user_prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
        }
        resp = requests.post(self.base_url, headers=headers, json=payload, timeout=45)
        if resp.status_code >= 400:
            raise ValueError(f"{resp.status_code} {resp.text}")
        data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            return "No response received from OpenRouter model."
        return choices[0]["message"]["content"]

    def get_advice(self, query: str, user: User, portfolio: Optional[Portfolio] = None) -> str:
        try:
            system_prompt = (
                "You are an Indian personal finance advisor. Give practical, responsible, "
                "actionable advice with clear monthly amounts, timeline, and risk notes."
            )
            context = (
                f"User profile: age={user.age}, monthly_income={user.income}, monthly_expenses={user.expenses}, "
                f"risk_profile={user.risk_profile}, goals={', '.join(user.financial_goals)}. "
            )
            if portfolio:
                context += f"Portfolio_total={portfolio.total_value}. "
            answer = self._chat(system_prompt, f"{context}\n\nUser query: {query}")
            self.conversation_history.append({"query": query, "response": answer})
            return answer
        except Exception as e:
            return f"Error getting advice: {e}. Please check OpenRouter key/model."


class OfflineFinanceAdvisor:
    """No-API fallback advisor for students/free usage."""

    def __init__(self):
        self.conversation_history = []
        self.knowledge_base = {
            "sip": "SIP (Systematic Investment Plan) means investing a fixed amount every month in a mutual fund. It helps with discipline and reduces timing risk.",
            "mutual fund": "A mutual fund pools money from many investors and invests in stocks/bonds. You get diversification and professional management.",
            "inflation": "Inflation means prices rise over time, so money buys less. Your investments should grow faster than inflation to protect purchasing power.",
            "emergency fund": "Emergency fund is money kept for unexpected events like medical/job loss. Target 6 months of expenses in safe, liquid options.",
            "fd": "FD (Fixed Deposit) gives fixed returns with lower risk. Good for safety goals, but long-term wealth growth is usually lower than equity.",
            "diversification": "Diversification means spreading money across asset types (equity, debt, gold, cash) to reduce risk from one bad investment.",
            "credit score": "Credit score reflects your loan repayment behavior. Pay EMIs/credit card on time and keep credit utilization low (ideally below 30%).",
            "ppf": "PPF is a long-term government-backed savings option with tax benefits and low risk. Useful for stable debt allocation.",
            "nps": "NPS is a retirement-focused investment with tax benefits. It has equity + debt exposure and is useful for long-term retirement corpus.",
            "term insurance": "Term insurance gives high life cover at low premium and protects family income. It is protection, not investment.",
            "health insurance": "Health insurance protects savings from hospital expenses. Even young people should have basic coverage.",
            "budget": "A budget is a plan for income allocation. A simple rule: needs, wants, savings/investments. Track monthly to improve control.",
        }

    def _knowledge_response(self, query: str) -> Optional[str]:
        q = query.lower()
        for keyword, explanation in self.knowledge_base.items():
            if keyword in q:
                return f"Basic concept:\n{explanation}\n\nIf you want, I can also explain this with a simple real-life example."
        if any(k in q for k in ["basic", "beginner", "learn finance", "financial knowledge"]):
            return (
                "Beginner financial roadmap:\n"
                "1) Track income/expenses and follow a budget.\n"
                "2) Build emergency fund (6 months expenses).\n"
                "3) Buy health + term insurance.\n"
                "4) Start SIP for long-term goals.\n"
                "5) Review and increase savings every 3-6 months."
            )
        return None

    def get_advice(self, query: str, user: User, portfolio: Optional[Portfolio] = None) -> str:
        knowledge = self._knowledge_response(query)
        if knowledge:
            self.conversation_history.append({"query": query, "response": knowledge})
            return knowledge

        savings = max(0, user.income - user.expenses)
        savings_rate = (savings / user.income * 100) if user.income > 0 else 0
        emergency_target = user.expenses * 6
        current_emergency = 0.0
        if portfolio:
            current_emergency = portfolio.cash + portfolio.fixed_deposits
        emergency_gap = max(0.0, emergency_target - current_emergency)
        invest_pct = 50 if "aggressive" in user.risk_profile.lower() else 35 if "moderate" in user.risk_profile.lower() else 20
        debt_pct = 100 - invest_pct

        advice = (
            f"Based on your profile, here is a free rule-based plan:\n\n"
            f"1) Savings: You currently save about {savings_rate:.1f}% (₹{savings:,.0f}/month). "
            f"Target at least 20%.\n"
            f"2) Emergency fund: Target ₹{emergency_target:,.0f}. "
            f"Current estimate ₹{current_emergency:,.0f}. Gap ₹{emergency_gap:,.0f}.\n"
            f"3) Investing split ({user.risk_profile}): ~{invest_pct}% equity and ~{debt_pct}% safer assets.\n"
            f"4) Action this month: automate savings on salary day, then invest remaining surplus via SIP.\n\n"
            f"Your question: {query}"
        )
        self.conversation_history.append({"query": query, "response": advice})
        return advice

# ======================== Gamification System ========================
class GamificationEngine:
    """Enhanced gamification system for financial literacy"""
    
    def __init__(self):
        self.challenges = {
            # Beginner Achievements
            "first_investment": {
                "name": "First Steps",
                "description": "Make your first investment",
                "points": 100,
                "badge": "🎯",
                "category": "Beginner",
                "progress_max": 1
            },
            "profile_complete": {
                "name": "Profile Master",
                "description": "Complete your financial profile",
                "points": 50,
                "badge": "✅",
                "category": "Beginner",
                "progress_max": 1
            },
            "first_chat": {
                "name": "Conversation Starter",
                "description": "Have your first chat with AI advisor",
                "points": 75,
                "badge": "💬",
                "category": "Beginner",
                "progress_max": 1
            },
            
            # Savings Achievements
            "emergency_fund": {
                "name": "Emergency Shield",
                "description": "Build 3 months emergency fund",
                "points": 500,
                "badge": "🛡️",
                "category": "Savings",
                "progress_max": 3
            },
            "super_saver": {
                "name": "Super Saver",
                "description": "Save 30% of income for 3 months",
                "points": 400,
                "badge": "💎",
                "category": "Savings",
                "progress_max": 3
            },
            "emergency_master": {
                "name": "Emergency Master",
                "description": "Build 6 months emergency fund",
                "points": 750,
                "badge": "🏆",
                "category": "Savings",
                "progress_max": 6
            },
            
            # Investment Achievements
            "diversifier": {
                "name": "Diversification Expert",
                "description": "Invest in 5+ different asset classes",
                "points": 300,
                "badge": "🎨",
                "category": "Investment",
                "progress_max": 5
            },
            "equity_investor": {
                "name": "Equity Champion",
                "description": "Invest ₹1 lakh in stocks/mutual funds",
                "points": 350,
                "badge": "📈",
                "category": "Investment",
                "progress_max": 100000
            },
            "sip_warrior": {
                "name": "SIP Warrior",
                "description": "Start 3 different SIPs",
                "points": 400,
                "badge": "🔄",
                "category": "Investment",
                "progress_max": 3
            },
            "gold_investor": {
                "name": "Golden Touch",
                "description": "Allocate 5-10% to gold",
                "points": 200,
                "badge": "🥇",
                "category": "Investment",
                "progress_max": 1
            },
            
            # Tax Achievements
            "tax_saver": {
                "name": "Tax Optimizer",
                "description": "Max out 80C limit (₹1.5 lakh)",
                "points": 400,
                "badge": "📊",
                "category": "Tax",
                "progress_max": 150000
            },
            "elss_investor": {
                "name": "ELSS Expert",
                "description": "Invest in ELSS funds",
                "points": 250,
                "badge": "📋",
                "category": "Tax",
                "progress_max": 1
            },
            "nps_contributor": {
                "name": "NPS Champion",
                "description": "Start NPS for extra ₹50k deduction",
                "points": 300,
                "badge": "🎖️",
                "category": "Tax",
                "progress_max": 1
            },
            
            # Goal Achievements
            "goal_setter": {
                "name": "Goal Setter",
                "description": "Set 3 financial goals",
                "points": 150,
                "badge": "🎯",
                "category": "Goals",
                "progress_max": 3
            },
            "goal_achiever": {
                "name": "Goal Crusher",
                "description": "Achieve your first financial goal",
                "points": 500,
                "badge": "🏅",
                "category": "Goals",
                "progress_max": 1
            },
            "retirement_planner": {
                "name": "Future Ready",
                "description": "Create retirement plan",
                "points": 350,
                "badge": "🌅",
                "category": "Goals",
                "progress_max": 1
            },
            
            # Consistency Achievements
            "regular_investor": {
                "name": "Consistent Investor",
                "description": "Invest for 6 consecutive months",
                "points": 600,
                "badge": "📅",
                "category": "Consistency",
                "progress_max": 6
            },
            "year_investor": {
                "name": "Annual Achiever",
                "description": "Complete 1 year of investing",
                "points": 1000,
                "badge": "🌟",
                "category": "Consistency",
                "progress_max": 12
            },
            "daily_checker": {
                "name": "Daily Discipline",
                "description": "Check portfolio for 30 days",
                "points": 200,
                "badge": "📱",
                "category": "Consistency",
                "progress_max": 30
            },
            
            # Knowledge Achievements
            "learner": {
                "name": "Knowledge Seeker",
                "description": "Ask 10 questions to AI advisor",
                "points": 150,
                "badge": "🎓",
                "category": "Knowledge",
                "progress_max": 10
            },
            "expert_learner": {
                "name": "Financial Scholar",
                "description": "Ask 50 questions to AI advisor",
                "points": 500,
                "badge": "🏫",
                "category": "Knowledge",
                "progress_max": 50
            },
            "optimizer": {
                "name": "Optimization Master",
                "description": "Use portfolio optimizer 5 times",
                "points": 250,
                "badge": "⚡",
                "category": "Knowledge",
                "progress_max": 5
            },
            
            # Special Achievements
            "millionaire": {
                "name": "Millionaire Club",
                "description": "Reach ₹10 lakh portfolio value",
                "points": 2000,
                "badge": "💰",
                "category": "Special",
                "progress_max": 1000000
            },
            "wealth_creator": {
                "name": "Wealth Creator",
                "description": "Achieve 20% portfolio growth",
                "points": 1000,
                "badge": "🚀",
                "category": "Special",
                "progress_max": 20
            },
            "insurance_wise": {
                "name": "Fully Protected",
                "description": "Get adequate life & health insurance",
                "points": 400,
                "badge": "🛡️",
                "category": "Special",
                "progress_max": 2
            }
        }
        
        self.daily_tips = [
            "💡 Start SIP in ELSS funds to save tax and build wealth",
            "💡 Keep 6-12 months expenses as emergency fund",
            "💡 Term insurance should be 10-15x your annual income",
            "💡 Invest in PPF for guaranteed tax-free returns",
            "💡 Use NPS for additional ₹50,000 tax benefit",
            "💡 Gold should be 5-10% of your portfolio",
            "💡 Review and rebalance portfolio quarterly",
            "💡 Avoid timing the market, invest regularly",
            "💡 Pay off high-interest debt before investing",
            "💡 Increase SIP by 10% every year",
            "💡 Diversify across large, mid, and small-cap funds",
            "💡 Keep credit utilization below 30%",
            "💡 Build multiple income streams",
            "💡 Automate your investments",
            "💡 Track expenses to find saving opportunities"
        ]
        
        # Rewards system
        self.rewards = {
            100: {"reward": "Unlock Basic Portfolio Analytics", "icon": "📊"},
            500: {"reward": "Unlock Advanced AI Suggestions", "icon": "🤖"},
            1000: {"reward": "Unlock Tax Optimization Tools", "icon": "💼"},
            2000: {"reward": "Unlock Retirement Calculator", "icon": "🏖️"},
            3000: {"reward": "Unlock Real-time Alerts", "icon": "🔔"},
            5000: {"reward": "Unlock Premium Insights", "icon": "💎"},
            10000: {"reward": "Unlock Wealth Master Status", "icon": "👑"}
        }
        
        # Daily Challenges
        self.daily_challenges = [
            {"task": "Check your portfolio performance", "points": 10},
            {"task": "Read a financial article", "points": 15},
            {"task": "Review your monthly expenses", "points": 20},
            {"task": "Ask AI advisor a question", "points": 15},
            {"task": "Update your financial goals", "points": 25},
            {"task": "Calculate your net worth", "points": 30},
            {"task": "Review insurance coverage", "points": 20}
        ]
    
    def check_achievements(self, user: User, portfolio: Portfolio, stats: Dict = None) -> List[Dict]:
        """Check and award achievements based on user progress"""
        new_achievements = []
        
        if not stats:
            stats = self.calculate_user_stats(user, portfolio)
        
        # Check each achievement
        for achievement_id, achievement in self.challenges.items():
            if achievement_id not in user.badges:
                achieved = False
                progress = 0
                
                # Check different achievement types
                if achievement_id == "first_investment" and portfolio.total_value > 0:
                    achieved = True
                    progress = 1
                
                elif achievement_id == "profile_complete" and user.name and user.risk_profile:
                    achieved = True
                    progress = 1
                
                elif achievement_id == "emergency_fund":
                    emergency_funds = portfolio.cash + portfolio.fixed_deposits
                    months_covered = emergency_funds / user.expenses if user.expenses > 0 else 0
                    progress = min(months_covered, 3)
                    achieved = months_covered >= 3
                
                elif achievement_id == "emergency_master":
                    emergency_funds = portfolio.cash + portfolio.fixed_deposits
                    months_covered = emergency_funds / user.expenses if user.expenses > 0 else 0
                    progress = min(months_covered, 6)
                    achieved = months_covered >= 6
                
                elif achievement_id == "diversifier":
                    asset_classes = stats.get("asset_classes", 0)
                    progress = asset_classes
                    achieved = asset_classes >= 5
                
                elif achievement_id == "equity_investor":
                    equity_value = sum(portfolio.stocks.values()) + sum(portfolio.mutual_funds.values())
                    progress = equity_value
                    achieved = equity_value >= 100000
                
                elif achievement_id == "tax_saver":
                    tax_savings = portfolio.ppf + portfolio.elss
                    progress = tax_savings
                    achieved = tax_savings >= 150000
                
                elif achievement_id == "millionaire":
                    progress = portfolio.total_value
                    achieved = portfolio.total_value >= 1000000
                
                elif achievement_id == "gold_investor":
                    if portfolio.total_value > 0:
                        gold_percent = (portfolio.gold / portfolio.total_value) * 100
                        achieved = 5 <= gold_percent <= 10
                        progress = 1 if achieved else 0
                
                if achieved:
                    new_achievements.append(achievement)
                    user.badges.append(achievement_id)
                    user.wealth_score += achievement["points"]
        
        return new_achievements
    
    def calculate_user_stats(self, user: User, portfolio: Portfolio) -> Dict:
        """Calculate detailed user statistics"""
        stats = {
            "asset_classes": 0,
            "total_investments": portfolio.total_value,
            "savings_rate": ((user.income - user.expenses) / user.income * 100) if user.income > 0 else 0,
            "emergency_months": 0,
            "portfolio_diversity": 0
        }
        
        # Count asset classes
        if portfolio.stocks and sum(portfolio.stocks.values()) > 0:
            stats["asset_classes"] += 1
        if portfolio.mutual_funds and sum(portfolio.mutual_funds.values()) > 0:
            stats["asset_classes"] += 1
        if portfolio.elss > 0:
            stats["asset_classes"] += 1
        if portfolio.fixed_deposits > 0:
            stats["asset_classes"] += 1
        if portfolio.ppf > 0:
            stats["asset_classes"] += 1
        if portfolio.nps > 0:
            stats["asset_classes"] += 1
        if portfolio.gold > 0:
            stats["asset_classes"] += 1
        if portfolio.real_estate > 0:
            stats["asset_classes"] += 1
        if portfolio.crypto > 0:
            stats["asset_classes"] += 1
        
        # Calculate emergency fund coverage
        emergency_funds = portfolio.cash + portfolio.fixed_deposits
        stats["emergency_months"] = emergency_funds / user.expenses if user.expenses > 0 else 0
        
        return stats
    
    def get_wealth_level(self, score: int) -> Tuple[str, str, int]:
        """Get wealth level based on score with progress"""
        levels = [
            (0, "Beginner", "🌱"),
            (100, "Novice Investor", "💰"),
            (500, "Smart Saver", "💎"),
            (1000, "Savvy Investor", "📈"),
            (2000, "Wealth Builder", "🏆"),
            (5000, "Financial Expert", "👑"),
            (10000, "Wealth Master", "🌟"),
            (20000, "Financial Guru", "🚀")
        ]
        
        current_level = None
        next_level = None
        
        for i, (threshold, name, emoji) in enumerate(levels):
            if score >= threshold:
                current_level = (name, emoji, threshold)
                if i + 1 < len(levels):
                    next_level = levels[i + 1]
        
        if next_level:
            progress = ((score - current_level[2]) / (next_level[0] - current_level[2])) * 100
            return current_level[0], current_level[1], min(100, progress)
        else:
            return current_level[0], current_level[1], 100
    
    def get_daily_tip(self) -> str:
        """Get daily financial tip"""
        return random.choice(self.daily_tips)
    
    def get_daily_challenge(self) -> Dict:
        """Get random daily challenge"""
        return random.choice(self.daily_challenges)
    
    def get_unlocked_rewards(self, score: int) -> List[Dict]:
        """Get list of unlocked rewards based on score"""
        unlocked = []
        for threshold, reward_info in sorted(self.rewards.items()):
            if score >= threshold:
                unlocked.append({
                    "threshold": threshold,
                    "reward": reward_info["reward"],
                    "icon": reward_info["icon"],
                    "unlocked": True
                })
            else:
                unlocked.append({
                    "threshold": threshold,
                    "reward": reward_info["reward"],
                    "icon": reward_info["icon"],
                    "unlocked": False
                })
        return unlocked

# ======================== Risk Profiler ========================
class RiskProfiler:
    """Comprehensive risk profiling system"""
    
    def __init__(self):
        self.questions = [
            {
                "question": "How would you react if your portfolio dropped 20% in a month?",
                "options": {
                    "Sell everything": 1,
                    "Sell some": 2,
                    "Hold": 3,
                    "Buy more": 4
                }
            },
            {
                "question": "What's your investment time horizon?",
                "options": {
                    "< 1 year": 1,
                    "1-3 years": 2,
                    "3-5 years": 3,
                    "> 5 years": 4
                }
            },
            {
                "question": "How much of monthly income can you invest?",
                "options": {
                    "< 10%": 1,
                    "10-20%": 2,
                    "20-30%": 3,
                    "> 30%": 4
                }
            },
            {
                "question": "Your age group?",
                "options": {
                    "> 50": 1,
                    "40-50": 2,
                    "30-40": 3,
                    "< 30": 4
                }
            },
            {
                "question": "Investment knowledge level?",
                "options": {
                    "Beginner": 1,
                    "Basic": 2,
                    "Intermediate": 3,
                    "Expert": 4
                }
            }
        ]
    
    def calculate_risk_profile(self, answers: List[int]) -> str:
        """Calculate risk profile from questionnaire"""
        avg_score = sum(answers) / len(answers)
        
        if avg_score < 1.5:
            return "Conservative"
        elif avg_score < 2.5:
            return "Moderately Conservative"
        elif avg_score < 3.5:
            return "Moderate"
        elif avg_score < 4:
            return "Moderately Aggressive"
        else:
            return "Aggressive"
    
    def get_allocation_recommendation(self, risk_profile: str, age: int) -> Dict:
        """Get asset allocation based on risk profile"""
        base_allocations = {
            "Conservative": {
                "Equity": 20,
                "Debt": 60,
                "Gold": 10,
                "Cash": 10
            },
            "Moderate": {
                "Equity": 50,
                "Debt": 35,
                "Gold": 10,
                "Cash": 5
            },
            "Aggressive": {
                "Equity": 70,
                "Debt": 20,
                "Gold": 5,
                "Cash": 5
            }
        }
        
        # Age-based adjustment
        if age > 50:
            equity_reduction = 10
        elif age > 40:
            equity_reduction = 5
        else:
            equity_reduction = 0
        
        allocation = base_allocations.get(
            risk_profile.replace("Moderately ", ""),
            base_allocations["Moderate"]
        )
        
        # Adjust for age
        if equity_reduction > 0:
            allocation["Equity"] -= equity_reduction
            allocation["Debt"] += equity_reduction
        
        return allocation

# ======================== Main Application ========================
class IndianFinanceAdvisorApp:
    """Main Streamlit Application"""
    
    def __init__(self):
        st.set_page_config(
            page_title="WealthWise India - AI Finance Advisor",
            page_icon="💰",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        self.init_session_state()
        self.apply_custom_css()
        self.Config = Config
        self.User = User
        self.Portfolio = Portfolio
        self.MarketDataManager = MarketDataManager
        self.GamificationEngine = GamificationEngine
        self.RiskProfiler = RiskProfiler
        self.PortfolioOptimizer = PortfolioOptimizer
        self.GeminiFinanceAdvisor = GeminiFinanceAdvisor
        self.OpenRouterFinanceAdvisor = OpenRouterFinanceAdvisor
        self.OfflineFinanceAdvisor = OfflineFinanceAdvisor
        self.SmartFinanceEngine = SmartFinanceEngine
    
    def init_session_state(self):
        """Initialize session state"""
        if 'user' not in st.session_state:
            st.session_state.user = None
        if 'portfolio' not in st.session_state:
            st.session_state.portfolio = None
        if 'gemini_advisor' not in st.session_state:
            st.session_state.gemini_advisor = None
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Dashboard"
        if 'api_key' not in st.session_state:
            st.session_state.api_key = ""
        if 'llm_provider' not in st.session_state:
            st.session_state.llm_provider = "Offline (No API Key)"
        if 'llm_model' not in st.session_state:
            st.session_state.llm_model = "meta-llama/llama-3.1-8b-instruct:free"
        if 'expense_analysis' not in st.session_state:
            st.session_state.expense_analysis = None
        if 'chat_memory' not in st.session_state:
            st.session_state.chat_memory = {}
    
    def apply_custom_css(self):
        """Apply custom CSS styling"""
        st.markdown("""
        <style>
        .main {
            padding: 0rem 1rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            padding-left: 20px;
            padding-right: 20px;
            background-color: #f0f2f6;
            border-radius: 10px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #6C63FF;
            color: white;
        }
        div[data-testid="metric-container"] {
            background-color: #f0f2f6;
            border: 2px solid #6C63FF;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .success-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            margin: 1rem 0;
        }
        .warning-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
            color: #856404;
            margin: 1rem 0;
        }
        .info-box {
            padding: 1rem;
            border-radius: 10px;
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            margin: 1rem 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Run the application"""
        render_header_page(self)
        render_sidebar_page(self)
        
        # Route to appropriate page
        if st.session_state.current_page == "Dashboard":
            render_dashboard_page(self)
        elif st.session_state.current_page == "AI Chat":
            render_ai_chat_page(self)
        elif st.session_state.current_page == "Smart Features":
            render_smart_features_page(self)
        elif st.session_state.current_page == "Portfolio":
            render_portfolio_page(self)
        elif st.session_state.current_page == "Gamification":
            render_gamification_page(self)
        elif st.session_state.current_page == "Settings":
            render_settings_page(self)
        else:
            st.info(f"Page '{st.session_state.current_page}' is under development 🚧")

# ======================== Main Entry Point ========================
if __name__ == "__main__":
    app = IndianFinanceAdvisorApp()
    app.run()