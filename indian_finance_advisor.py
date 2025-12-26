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
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.conversation_history = []
        
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
            self.conversation_history.append({"query": query, "response": response.text})
            return response.text
            
        except Exception as e:
            return f"Error getting advice: {str(e)}. Please check your API key."
    
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
    
    def render_header(self):
        """Render application header"""
        col1, col2, col3 = st.columns([2, 3, 2])
        
        with col1:
            st.markdown("# 💰 WealthWise India")
            st.markdown("*Your AI-Powered Financial Advisor*")
        
        with col2:
            if st.session_state.user:
                level, emoji, progress = GamificationEngine().get_wealth_level(st.session_state.user.wealth_score)
                st.metric(
                    "Wealth Score",
                    f"{st.session_state.user.wealth_score} pts",
                    f"{emoji} {level}"
                )
        
        with col3:
            market = MarketDataManager.get_indian_market_sentiment()
            st.metric(
                "Market Sentiment",
                market['sentiment'],
                f"{market.get('avg_change', 0):.2f}%",
                delta_color="normal" if market.get('avg_change', 0) >= 0 else "inverse"
            )
    
    def render_sidebar(self):
        """Render sidebar navigation"""
        with st.sidebar:
            st.markdown("## 🚀 Navigation")
            
            pages = [
                ("🏠 Dashboard", "Dashboard"),
                ("💬 AI Advisor Chat", "AI Chat"),
                ("📊 Portfolio Optimizer", "Portfolio"),
                ("🎮 Achievements & Rewards", "Gamification"),
                ("⚙️ Settings", "Settings")
            ]
            
            for label, page in pages:
                if st.button(label, use_container_width=True, key=f"nav_{page}"):
                    st.session_state.current_page = page
            
            st.markdown("---")
            
            # Daily Tip
            st.markdown("### 💡 Daily Tip")
            tip = GamificationEngine().get_daily_tip()
            st.info(tip)
            
            st.markdown("---")
            
            # Quick Stats
            if st.session_state.portfolio:
                st.markdown("### 📊 Quick Stats")
                portfolio = st.session_state.portfolio
                st.metric("Total Portfolio", f"₹{portfolio.total_value:,.0f}")
                
                # Asset distribution
                st.markdown("**Asset Distribution:**")
                assets = {
                    "Equity": sum(portfolio.stocks.values()) + sum(portfolio.mutual_funds.values()) + portfolio.elss,
                    "Debt": portfolio.fixed_deposits + portfolio.ppf + portfolio.nps,
                    "Gold": portfolio.gold,
                    "Others": portfolio.real_estate + portfolio.crypto + portfolio.cash
                }
                for asset, value in assets.items():
                    if value > 0:
                        pct = (value / portfolio.total_value) * 100
                        st.progress(pct / 100)
                        st.caption(f"{asset}: {pct:.1f}%")
    
    def render_dashboard(self):
        """Render main dashboard"""
        st.markdown("## 📊 Financial Dashboard")
        
        if not st.session_state.user:
            st.warning("Please complete your profile in Settings first!")
            return
        
        user = st.session_state.user
        portfolio = st.session_state.portfolio
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            savings_rate = ((user.income - user.expenses) / user.income) * 100
            st.metric(
                "Savings Rate",
                f"{savings_rate:.1f}%",
                "Good" if savings_rate > 20 else "Improve"
            )
        
        with col2:
            if portfolio:
                monthly_investment = portfolio.total_value / 12  # Simplified
                investment_rate = (monthly_investment / user.income) * 100
                st.metric(
                    "Investment Rate",
                    f"{investment_rate:.1f}%",
                    "Excellent" if investment_rate > 30 else "Good"
                )
            else:
                st.metric("Investment Rate", "0%", "Start Investing")
        
        with col3:
            emergency_months = 0
            if portfolio:
                emergency_funds = portfolio.cash + portfolio.fixed_deposits
                emergency_months = emergency_funds / user.expenses if user.expenses > 0 else 0
            st.metric(
                "Emergency Fund",
                f"{emergency_months:.1f} months",
                "Adequate" if emergency_months >= 6 else "Build More"
            )
        
        with col4:
            debt_ratio = 0  # Simplified - would need debt data
            st.metric(
                "Debt-to-Income",
                f"{debt_ratio:.1f}%",
                "Healthy" if debt_ratio < 30 else "High"
            )
        
        # Financial Health Score
        st.markdown("### 🏥 Financial Health Analysis")
        
        health_scores = {
            "Savings": min(100, savings_rate * 3),
            "Investments": min(100, (portfolio.total_value / (user.income * 12)) * 100) if portfolio else 0,
            "Emergency Fund": min(100, (emergency_months / 6) * 100),
            "Insurance": 100 if user.has_insurance else 30,
            "Debt Management": max(0, 100 - debt_ratio * 2)
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(health_scores.keys()),
                y=list(health_scores.values()),
                marker_color=['green' if v >= 70 else 'orange' if v >= 40 else 'red' 
                             for v in health_scores.values()]
            )
        ])
        fig.update_layout(
            title="Financial Health Scores",
            yaxis_title="Score (0-100)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
        
        overall_health = sum(health_scores.values()) / len(health_scores)
        if overall_health >= 70:
            st.success(f"🎉 Excellent Financial Health! Score: {overall_health:.0f}/100")
        elif overall_health >= 50:
            st.warning(f"⚠️ Good Financial Health. Room for improvement. Score: {overall_health:.0f}/100")
        else:
            st.error(f"🚨 Financial Health Needs Attention! Score: {overall_health:.0f}/100")
        
        # Recommendations
        st.markdown("### 💡 Personalized Recommendations")
        
        recommendations = []
        
        if savings_rate < 20:
            recommendations.append({
                "priority": "High",
                "action": "Increase savings rate to at least 20%",
                "how": "Review and cut unnecessary expenses, automate savings"
            })
        
        if emergency_months < 6:
            recommendations.append({
                "priority": "High",
                "action": f"Build emergency fund to 6 months (need ₹{(6-emergency_months)*user.expenses:,.0f} more)",
                "how": "Open high-yield savings account, set up automatic transfer"
            })
        
        if not user.has_insurance:
            recommendations.append({
                "priority": "Critical",
                "action": "Get adequate insurance coverage",
                "how": f"Term insurance: ₹{user.income*12*10:,.0f}, Health insurance: ₹5-10 lakhs"
            })
        
        if portfolio and portfolio.ppf == 0:
            recommendations.append({
                "priority": "Medium",
                "action": "Start PPF account for tax-free returns",
                "how": "Invest up to ₹1.5 lakhs annually for Section 80C benefit"
            })
        
        for rec in recommendations[:3]:  # Show top 3
            if rec["priority"] == "Critical":
                st.error(f"🚨 **{rec['priority']}**: {rec['action']}")
            elif rec["priority"] == "High":
                st.warning(f"⚠️ **{rec['priority']}**: {rec['action']}")
            else:
                st.info(f"ℹ️ **{rec['priority']}**: {rec['action']}")
            st.caption(f"How: {rec['how']}")
    
    def render_ai_chat(self):
        """Render AI Advisor Chat Interface"""
        st.markdown("## 💬 AI Financial Advisor Chat")
        
        if not st.session_state.api_key:
            st.warning("Please enter your Gemini API key in Settings first!")
            return
        
        if not st.session_state.gemini_advisor:
            st.session_state.gemini_advisor = GeminiFinanceAdvisor(st.session_state.api_key)
        
        # Create a fixed layout with columns
        chat_col, context_col = st.columns([4, 1])
        
        with context_col:
            st.markdown("### Context")
            portfolio_value = f"₹{st.session_state.portfolio.total_value:,.0f}" if st.session_state.portfolio else "N/A"
            st.info(f"""
            **Profile Loaded:**
            - Risk: {st.session_state.user.risk_profile if st.session_state.user else 'N/A'}
            - Goals: {len(st.session_state.user.financial_goals) if st.session_state.user else 0}
            - Portfolio: {portfolio_value}
            """)
        
        with chat_col:
            # Quick action buttons
            st.markdown("### Quick Actions")
            quick_actions = [
                "📊 Analyze my portfolio",
                "💰 Tax saving suggestions",
                "🏠 Home loan planning",
                "👶 Child education planning",
                "🎯 Retirement planning",
                "📈 Best investments this month",
                "🛡️ Insurance recommendations",
                "💎 Should I invest in gold?"
            ]
            
            # Create 2 rows of 4 buttons each
            for row in range(2):
                cols = st.columns(4)
                for col_idx in range(4):
                    action_idx = row * 4 + col_idx
                    if action_idx < len(quick_actions):
                        button_key = f"quick_action_{action_idx}_{quick_actions[action_idx][:10]}"
                        if cols[col_idx].button(quick_actions[action_idx], use_container_width=True, key=button_key):
                            st.session_state.chat_history.append({
                                "role": "user",
                                "content": quick_actions[action_idx]
                            })
                            
                            with st.spinner("🤔 Thinking..."):
                                response = st.session_state.gemini_advisor.get_advice(
                                    quick_actions[action_idx],
                                    st.session_state.user,
                                    st.session_state.portfolio
                                )
                            
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": response
                            })
                            st.rerun()
            
            # Chat history in a container with fixed height
            st.markdown("### Conversation")
            
            # Create a container for chat history with fixed height
            chat_container = st.container(height=300)
            with chat_container:
                if st.session_state.chat_history:
                    for message in st.session_state.chat_history:
                        if message["role"] == "user":
                            st.markdown(f"**🧑 You:** {message['content']}")
                        else:
                            st.markdown(f"**🤖 Advisor:** {message['content']}")
                        st.markdown("---")
                else:
                    st.info("Start a conversation by asking a question or clicking a quick action button above!")
            
            # Input area at the bottom
            st.markdown("### Ask your financial question...")
            with st.form("chat_input", clear_on_submit=True):
                user_input = st.text_area(
                    "Type your question here:",
                    placeholder="E.g., How should I invest ₹50,000 for my child's education in 10 years?",
                    height=100,
                    label_visibility="collapsed"
                )
                
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    submitted = st.form_submit_button("Send 📤", use_container_width=True, type="primary")
                with col2:
                    if st.form_submit_button("Clear Chat 🗑️", use_container_width=True):
                        st.session_state.chat_history = []
                        st.rerun()
                
                if submitted and user_input:
                    st.session_state.chat_history.append({
                        "role": "user",
                        "content": user_input
                    })
                    
                    with st.spinner("🤖 AI is analyzing..."):
                        response = st.session_state.gemini_advisor.get_advice(
                            user_input,
                            st.session_state.user,
                            st.session_state.portfolio
                        )
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": response
                    })
                    st.rerun()
    
    def render_portfolio(self):
        """Render Portfolio Optimizer"""
        st.markdown("## 📊 Portfolio Optimizer")
        
        if not st.session_state.portfolio:
            st.warning("Please set up your portfolio in Settings first!")
            return
        
        optimizer = PortfolioOptimizer()
        
        # Portfolio Overview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Current Portfolio Allocation")
            
            portfolio = st.session_state.portfolio
            
            # Pie chart
            labels = []
            values = []
            
            if sum(portfolio.stocks.values()) > 0:
                labels.append("Stocks")
                values.append(sum(portfolio.stocks.values()))
            if sum(portfolio.mutual_funds.values()) > 0:
                labels.append("Mutual Funds")
                values.append(sum(portfolio.mutual_funds.values()))
            if portfolio.elss > 0:
                labels.append("ELSS (Tax Saving)")
                values.append(portfolio.elss)
            if portfolio.fixed_deposits > 0:
                labels.append("Fixed Deposits")
                values.append(portfolio.fixed_deposits)
            if portfolio.ppf > 0:
                labels.append("PPF")
                values.append(portfolio.ppf)
            if portfolio.nps > 0:
                labels.append("NPS")
                values.append(portfolio.nps)
            if portfolio.gold > 0:
                labels.append("Gold")
                values.append(portfolio.gold)
            if portfolio.cash > 0:
                labels.append("Cash")
                values.append(portfolio.cash)
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### Portfolio Metrics")
            
            # Calculate metrics
            equity_allocation = (sum(portfolio.stocks.values()) + 
                               sum(portfolio.mutual_funds.values()) + 
                               portfolio.elss) / portfolio.total_value * 100
            debt_allocation = (portfolio.fixed_deposits + portfolio.ppf + portfolio.nps) / portfolio.total_value * 100
            
            st.metric("Total Value", f"₹{portfolio.total_value:,.0f}")
            st.metric("Equity %", f"{equity_allocation:.1f}%")
            st.metric("Debt %", f"{debt_allocation:.1f}%")
            st.metric("Liquidity", f"₹{portfolio.cash:,.0f}")
        
        # Optimization Section
        st.markdown("### 🎯 Portfolio Optimization")
        
        with st.form("optimize_portfolio"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                selected_stocks = st.multiselect(
                    "Select Stocks to Optimize",
                    list(Config.INDIAN_STOCKS.keys()),
                    default=list(Config.INDIAN_STOCKS.keys())[:5]
                )
            
            with col2:
                risk_tolerance = st.selectbox(
                    "Risk Tolerance",
                    ["Conservative", "Moderate", "Aggressive"],
                    index=1
                )
            
            with col3:
                investment_amount = st.number_input(
                    "Investment Amount (₹)",
                    min_value=10000,
                    value=100000,
                    step=10000
                )
            
            optimize_btn = st.form_submit_button("🚀 Optimize Portfolio", use_container_width=True)
            
            if optimize_btn and selected_stocks:
                with st.spinner("Optimizing portfolio..."):
                    stock_symbols = [Config.INDIAN_STOCKS[s] for s in selected_stocks]
                    result = optimizer.optimize_portfolio(stock_symbols, risk_tolerance)
                    
                    if result["success"]:
                        st.success("✅ Optimization Complete!")
                        
                        # Display results
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Expected Return", f"{result['expected_return']:.2f}%")
                        with col2:
                            st.metric("Risk (Std Dev)", f"{result['risk']:.2f}%")
                        with col3:
                            st.metric("Sharpe Ratio", f"{result['sharpe_ratio']:.2f}")
                        
                        # Allocation table
                        st.markdown("#### Recommended Allocation")
                        allocation_df = pd.DataFrame([
                            {
                                "Stock": stock,
                                "Allocation %": f"{weight*100:.1f}%",
                                "Amount (₹)": f"{investment_amount * weight:,.0f}"
                            }
                            for stock, weight in result['weights'].items()
                            if weight > 0.01
                        ])
                        st.dataframe(allocation_df, use_container_width=True)
                    else:
                        st.error(f"Optimization failed: {result.get('error', 'Unknown error')}")
    
    def render_gamification(self):
        """Render Achievements & Rewards Page"""
        st.markdown("## 🎮 Achievements & Rewards")
        
        if not st.session_state.user:
            st.warning("Please complete your profile in Settings first to start earning achievements!")
            return
        
        engine = GamificationEngine()
        user = st.session_state.user
        
        # Initialize empty portfolio if none exists
        if not st.session_state.portfolio:
            st.session_state.portfolio = Portfolio(
                user_id=user.user_id, stocks={}, mutual_funds={}, 
                fixed_deposits=0, ppf=0, nps=0, gold=0, 
                real_estate=0, crypto=0, cash=0, elss=0
            )
        
        portfolio = st.session_state.portfolio
        
        # Check for new achievements
        new_achievements = engine.check_achievements(user, portfolio)
        if new_achievements:
            st.balloons()
            for achievement in new_achievements:
                st.success(f"🎉 New Achievement Unlocked: {achievement['badge']} **{achievement['name']}** (+{achievement['points']} pts)")
        
        # Header with level and score
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        
        level_name, level_emoji, progress = engine.get_wealth_level(user.wealth_score)
        
        with col1:
            st.metric("Wealth Score", f"{user.wealth_score} pts", f"{level_emoji}")
        with col2:
            st.metric("Current Level", level_name, f"Progress: {progress:.0f}%")
        with col3:
            st.metric("Achievements", f"{len(user.badges)}/{len(engine.challenges)}", 
                     f"{len(user.badges)/len(engine.challenges)*100:.0f}% Complete")
        with col4:
            next_level_points = 0
            for threshold in [100, 500, 1000, 2000, 5000, 10000, 20000]:
                if user.wealth_score < threshold:
                    next_level_points = threshold - user.wealth_score
                    break
            st.metric("To Next Level", f"{next_level_points} pts", "Keep going!")
        
        # Level Progress Bar
        st.progress(progress / 100)
        
        # Tabs for different sections - REMOVED LEADERBOARD
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏆 Achievements", 
            "🎯 Daily Challenges", 
            "🎁 Rewards",
            "📈 Progress Tracker"
        ])
        
        with tab1:
            st.markdown("### 🏆 Achievement Categories")
            st.info("Complete tasks to unlock achievements and earn points! Each achievement has specific requirements.")
            
            # Achievement Categories with better organization
            categories = {}
            for ach_id, ach in engine.challenges.items():
                category = ach.get("category", "General")
                if category not in categories:
                    categories[category] = []
                categories[category].append((ach_id, ach))
            
            # Display achievements by category with progress indicators
            for category, achievements in categories.items():
                with st.expander(f"**{category} Achievements** ({sum(1 for a in achievements if a[0] in user.badges)}/{len(achievements)} completed)", expanded=True):
                    cols = st.columns(3)
                    for idx, (ach_id, achievement) in enumerate(achievements):
                        with cols[idx % 3]:
                            is_earned = ach_id in user.badges
                            
                            # Calculate progress for specific achievements
                            progress_text = ""
                            progress_percent = 0
                            
                            if not is_earned:
                                if ach_id == "first_investment" and portfolio:
                                    progress_percent = 100 if portfolio.total_value > 0 else 0
                                    progress_text = "Ready!" if progress_percent == 100 else "Add investments"
                                
                                elif ach_id == "emergency_fund" and portfolio:
                                    emergency_funds = portfolio.cash + portfolio.fixed_deposits
                                    months = emergency_funds / user.expenses if user.expenses > 0 else 0
                                    progress_percent = min(100, (months / 3) * 100)
                                    progress_text = f"{months:.1f}/3 months"
                                
                                elif ach_id == "emergency_master" and portfolio:
                                    emergency_funds = portfolio.cash + portfolio.fixed_deposits
                                    months = emergency_funds / user.expenses if user.expenses > 0 else 0
                                    progress_percent = min(100, (months / 6) * 100)
                                    progress_text = f"{months:.1f}/6 months"
                                
                                elif ach_id == "diversifier" and portfolio:
                                    stats = engine.calculate_user_stats(user, portfolio)
                                    progress_percent = min(100, (stats['asset_classes'] / 5) * 100)
                                    progress_text = f"{stats['asset_classes']}/5 classes"
                                
                                elif ach_id == "equity_investor" and portfolio:
                                    equity_value = sum(portfolio.stocks.values()) + sum(portfolio.mutual_funds.values())
                                    progress_percent = min(100, (equity_value / 100000) * 100)
                                    progress_text = f"₹{equity_value:,.0f}/₹1,00,000"
                                
                                elif ach_id == "tax_saver" and portfolio:
                                    tax_savings = portfolio.ppf + portfolio.elss
                                    progress_percent = min(100, (tax_savings / 150000) * 100)
                                    progress_text = f"₹{tax_savings:,.0f}/₹1,50,000"
                            
                            # Achievement card with progress
                            if is_earned:
                                st.success(f"{achievement['badge']} **{achievement['name']}**")
                                st.caption(f"✅ Completed • +{achievement['points']} pts")
                            else:
                                st.info(f"🔒 **{achievement['name']}**")
                                st.caption(achievement['description'])
                                if progress_text:
                                    st.progress(progress_percent / 100)
                                    st.caption(f"Progress: {progress_text}")
                                st.caption(f"Reward: {achievement['points']} pts")
        
        with tab2:
            st.markdown("### 🎯 Daily & Weekly Challenges")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📅 Today's Challenge")
                daily_challenge = engine.get_daily_challenge()
                
                st.info(f"""
                **Task:** {daily_challenge['task']}
                
                **Reward:** {daily_challenge['points']} points
                
                Complete daily challenges to maintain your streak!
                """)
                
                if st.button("✅ Mark as Complete", use_container_width=True, key="daily_challenge_complete"):
                    user.wealth_score += daily_challenge['points']
                    st.success(f"Great job! +{daily_challenge['points']} points earned!")
                    st.balloons()
                    st.rerun()
            
            with col2:
                st.markdown("#### 🔥 Your Streaks")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Current Streak", "7 days", "🔥")
                    st.metric("Longest Streak", "14 days", "⭐")
                with col_b:
                    st.metric("This Week", "5/7 days", "📅")
                    st.metric("Total Active", "45 days", "💪")
            
            # Weekly Challenges
            st.markdown("#### 📅 Weekly Challenges")
            
            weekly_challenges = [
                {"task": "Complete 5 daily challenges", "points": 50, "progress": 3, "total": 5},
                {"task": "Increase portfolio value by 2%", "points": 100, "progress": 1.2, "total": 2},
                {"task": "Ask AI advisor 3 questions", "points": 30, "progress": len(st.session_state.chat_history) // 2, "total": 3},
                {"task": "Review and update goals", "points": 40, "progress": 0, "total": 1}
            ]
            
            for challenge in weekly_challenges:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{challenge['task']}**")
                    progress_pct = min(100, (challenge['progress'] / challenge['total']) * 100)
                    st.progress(progress_pct / 100)
                    st.caption(f"Progress: {challenge['progress']}/{challenge['total']}")
                with col2:
                    if progress_pct >= 100:
                        st.success(f"✅ +{challenge['points']}")
                    else:
                        st.info(f"{challenge['points']} pts")
        
        with tab3:
            st.markdown("### 🎁 Rewards & Unlocks")
            st.info("Earn points to unlock premium features and rewards!")
            
            rewards = engine.get_unlocked_rewards(user.wealth_score)
            
            # Split rewards into unlocked and locked
            unlocked_rewards = [r for r in rewards if r['unlocked']]
            locked_rewards = [r for r in rewards if not r['unlocked']]
            
            if unlocked_rewards:
                st.markdown("#### ✅ Unlocked Rewards")
                cols = st.columns(3)
                for idx, reward in enumerate(unlocked_rewards):
                    with cols[idx % 3]:
                        st.success(f"{reward['icon']} **{reward['reward']}**")
                        st.caption(f"Unlocked at {reward['threshold']} pts")
            
            if locked_rewards:
                st.markdown("#### 🔒 Upcoming Rewards")
                for reward in locked_rewards[:3]:  # Show next 3 rewards
                    col1, col2, col3 = st.columns([1, 3, 1])
                    with col1:
                        st.markdown(f"### 🔒")
                    with col2:
                        st.markdown(f"**{reward['reward']}**")
                        points_needed = reward['threshold'] - user.wealth_score
                        st.caption(f"Need {points_needed} more points")
                        st.progress(min(100, user.wealth_score / reward['threshold'] * 100) / 100)
                    with col3:
                        st.info(f"{reward['threshold']} pts")
            
            # Special Offers
            st.markdown("#### 💎 Bonus Opportunities")
            col1, col2 = st.columns(2)
            with col1:
                st.info("""
                **🎯 Weekly Bonus**
                Complete all weekly challenges
                Reward: +200 bonus points
                """)
            with col2:
                st.info("""
                **📈 Growth Bonus**
                Grow portfolio by 5% this month
                Reward: +500 bonus points
                """)
        
        with tab4:
            st.markdown("### 📈 Your Progress Overview")
            
            # Progress metrics
            col1, col2 = st.columns(2)
            
            with col1:
                # Score progression chart
                st.markdown("#### 📊 Score Progress")
                dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
                scores = [max(0, user.wealth_score - (30-i)*20 + random.randint(-10, 30)) for i in range(30)]
                
                fig = go.Figure(data=[
                    go.Scatter(x=dates, y=scores, mode='lines+markers',
                              line=dict(color='#6C63FF', width=3),
                              marker=dict(size=5),
                              fill='tozeroy',
                              fillcolor='rgba(108, 99, 255, 0.2)')
                ])
                fig.update_layout(
                    title="Last 30 Days",
                    xaxis_title="Date",
                    yaxis_title="Score",
                    height=300,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Category completion
                st.markdown("#### 🏆 Category Progress")
                categories_data = []
                for category in ["Beginner", "Savings", "Investment", "Tax", "Goals"]:
                    category_achievements = [a for a_id, a in engine.challenges.items() 
                                           if a.get("category") == category]
                    completed = sum(1 for a_id, a in engine.challenges.items() 
                                  if a.get("category") == category and a_id in user.badges)
                    total = len(category_achievements)
                    percentage = (completed / total * 100) if total > 0 else 0
                    categories_data.append({
                        "Category": category,
                        "Completed": percentage
                    })
                
                df = pd.DataFrame(categories_data)
                fig = go.Figure(data=[
                    go.Bar(x=df['Category'], y=df['Completed'],
                          marker_color=['green' if v >= 60 else 'orange' if v >= 30 else 'red' 
                                       for v in df['Completed']])
                ])
                fig.update_layout(
                    title="Completion by Category (%)",
                    yaxis_title="Completion %",
                    height=300,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Key Statistics
            st.markdown("#### 📊 Your Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_daily_points = user.wealth_score / max(1, (datetime.now() - user.created_at).days)
                st.metric("Daily Average", f"{avg_daily_points:.1f} pts")
            
            with col2:
                completion_rate = (len(user.badges) / len(engine.challenges)) * 100
                st.metric("Completion", f"{completion_rate:.0f}%")
            
            with col3:
                total_possible = sum(a["points"] for a in engine.challenges.values())
                st.metric("Total Possible", f"{total_possible} pts")
            
            with col4:
                efficiency = (user.wealth_score / total_possible * 100) if total_possible > 0 else 0
                st.metric("Efficiency", f"{efficiency:.0f}%")
                    
    def render_settings(self):
        """Render Settings Page"""
        st.markdown("## ⚙️ Settings")
        
        tab1, tab2, tab3 = st.tabs(["Profile Setup", "Portfolio Setup", "API Configuration"])
        
        with tab1:
            st.markdown("### 👤 User Profile")
            
            with st.form("user_profile"):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input("Name", value="Demo User")
                    age = st.number_input("Age", min_value=18, max_value=100, value=30)
                    income = st.number_input("Monthly Income (₹)", min_value=10000, value=75000, step=5000)
                    expenses = st.number_input("Monthly Expenses (₹)", min_value=5000, value=45000, step=5000)
                    family_size = st.number_input("Family Size", min_value=1, max_value=10, value=3)
                
                with col2:
                    city_tier = st.selectbox("City Tier", [1, 2, 3], index=0)
                    investment_experience = st.selectbox(
                        "Investment Experience",
                        ["Beginner", "Intermediate", "Advanced"],
                        index=1
                    )
                    has_insurance = st.checkbox("Have Life Insurance?", value=True)
                    has_emergency_fund = st.checkbox("Have Emergency Fund?", value=False)
                
                financial_goals = st.multiselect(
                    "Financial Goals",
                    Config.FINANCIAL_GOALS,
                    default=["Retirement Planning", "Children's Education"]
                )
                
                # Risk Profile Questions
                st.markdown("#### Risk Assessment")
                profiler = RiskProfiler()
                answers = []
                
                for q in profiler.questions:
                    answer = st.radio(
                        q["question"],
                        options=list(q["options"].keys()),
                        horizontal=True
                    )
                    answers.append(q["options"][answer])
                
                save_profile = st.form_submit_button("💾 Save Profile", use_container_width=True)
                
                if save_profile:
                    risk_profile = profiler.calculate_risk_profile(answers)
                    
                    st.session_state.user = User(
                        user_id=hashlib.md5(name.encode()).hexdigest()[:8],
                        name=name,
                        age=age,
                        income=income,
                        expenses=expenses,
                        risk_profile=risk_profile,
                        financial_goals=financial_goals,
                        investment_experience=investment_experience,
                        family_size=family_size,
                        city_tier=city_tier,
                        has_insurance=has_insurance,
                        has_emergency_fund=has_emergency_fund
                    )
                    
                    st.success(f"✅ Profile saved! Risk Profile: {risk_profile}")
        
        with tab2:
            st.markdown("### 💼 Portfolio Setup")
            
            with st.form("portfolio_setup"):
                st.markdown("#### Equity Investments")
                col1, col2 = st.columns(2)
                
                with col1:
                    stock_investment = st.number_input(
                        "Direct Stock Investment (₹)",
                        min_value=0,
                        value=200000,
                        step=10000
                    )
                
                with col2:
                    mf_investment = st.number_input(
                        "Mutual Fund Investment (₹)",
                        min_value=0,
                        value=300000,
                        step=10000
                    )
                
                st.markdown("#### Fixed Income & Tax Saving")
                col1, col2 = st.columns(2)
                
                with col1:
                    fd_investment = st.number_input(
                        "Fixed Deposits (₹)",
                        min_value=0,
                        value=100000,
                        step=10000
                    )
                    ppf_investment = st.number_input(
                        "PPF Investment (₹)",
                        min_value=0,
                        value=150000,
                        step=10000
                    )
                    elss_investment = st.number_input(
                        "ELSS (Tax Saving MF) (₹)",
                        min_value=0,
                        value=50000,
                        step=10000
                    )
                
                with col2:
                    nps_investment = st.number_input(
                        "NPS Investment (₹)",
                        min_value=0,
                        value=50000,
                        step=10000
                    )
                    gold_investment = st.number_input(
                        "Gold Investment (₹)",
                        min_value=0,
                        value=50000,
                        step=10000
                    )
                
                st.markdown("#### Others")
                col1, col2 = st.columns(2)
                
                with col1:
                    real_estate = st.number_input(
                        "Real Estate (₹)",
                        min_value=0,
                        value=0,
                        step=100000
                    )
                
                with col2:
                    crypto = st.number_input(
                        "Cryptocurrency (₹)",
                        min_value=0,
                        value=0,
                        step=10000
                    )
                
                cash = st.number_input(
                    "Cash/Savings Account (₹)",
                    min_value=0,
                    value=100000,
                    step=10000
                )
                
                save_portfolio = st.form_submit_button("💾 Save Portfolio", use_container_width=True)
                
                if save_portfolio:
                    # Simplified stock distribution
                    stocks = {}
                    if stock_investment > 0:
                        top_stocks = list(Config.INDIAN_STOCKS.keys())[:5]
                        for stock in top_stocks:
                            stocks[stock] = stock_investment / len(top_stocks)
                    
                    # Simplified MF distribution
                    mutual_funds = {}
                    if mf_investment > 0:
                        categories = ["Large Cap", "Mid Cap", "ELSS"]
                        for category in categories:
                            mutual_funds[category] = mf_investment / len(categories)
                    
                    portfolio = Portfolio(
                        user_id=st.session_state.user.user_id if st.session_state.user else "demo",
                        stocks=stocks,
                        mutual_funds=mutual_funds,
                        fixed_deposits=fd_investment,
                        ppf=ppf_investment,
                        nps=nps_investment,
                        elss=elss_investment,
                        gold=gold_investment,
                        real_estate=real_estate,
                        crypto=crypto,
                        cash=cash
                    )
                    portfolio.calculate_total()
                    
                    st.session_state.portfolio = portfolio
                    st.success(f"✅ Portfolio saved! Total Value: ₹{portfolio.total_value:,.0f}")
        
        with tab3:
            st.markdown("### 🔑 API Configuration")
            
            api_key = st.text_input(
                "Gemini API Key",
                value=st.session_state.api_key,
                type="password",
                placeholder="Enter your Gemini API key"
            )
            
            st.info("""
            To get your Gemini API key:
            1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
            2. Sign in with your Google account
            3. Click "Create API Key"
            4. Copy and paste the key above
            """)
            
            if st.button("💾 Save API Key", use_container_width=True, key="save_api_key"):
                if api_key:
                    st.session_state.api_key = api_key
                    st.session_state.gemini_advisor = GeminiFinanceAdvisor(api_key)
                    st.success("✅ API Key saved successfully!")
                else:
                    st.error("Please enter a valid API key")
    
    def run(self):
        """Run the application"""
        self.render_header()
        self.render_sidebar()
        
        # Route to appropriate page
        if st.session_state.current_page == "Dashboard":
            self.render_dashboard()
        elif st.session_state.current_page == "AI Chat":
            self.render_ai_chat()
        elif st.session_state.current_page == "Portfolio":
            self.render_portfolio()
        elif st.session_state.current_page == "Gamification":
            self.render_gamification()
        elif st.session_state.current_page == "Settings":
            self.render_settings()
        else:
            st.info(f"Page '{st.session_state.current_page}' is under development 🚧")

# ======================== Main Entry Point ========================
if __name__ == "__main__":
    app = IndianFinanceAdvisorApp()
    app.run()