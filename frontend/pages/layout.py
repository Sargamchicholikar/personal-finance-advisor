"""Layout UI rendering helpers."""

import streamlit as st


def render_header(app) -> None:
    """Render application header."""
    col1, col2, col3 = st.columns([2, 3, 2])

    with col1:
        st.markdown("# 💰 WealthWise India")
        st.markdown("*Your AI-Powered Financial Advisor*")

    with col2:
        if st.session_state.user:
            level, emoji, _ = app.GamificationEngine().get_wealth_level(st.session_state.user.wealth_score)
            st.metric(
                "Wealth Score",
                f"{st.session_state.user.wealth_score} pts",
                f"{emoji} {level}",
            )

    with col3:
        market = app.MarketDataManager.get_indian_market_sentiment()
        st.metric(
            "Market Sentiment",
            market["sentiment"],
            f"{market.get('avg_change', 0):.2f}%",
            delta_color="normal" if market.get("avg_change", 0) >= 0 else "inverse",
        )


def render_sidebar(app) -> None:
    """Render sidebar navigation."""
    with st.sidebar:
        st.markdown("## 🚀 Navigation")

        pages = [
            ("🏠 Dashboard", "Dashboard"),
            ("💬 AI Advisor Chat", "AI Chat"),
            ("🧠 Smart Features", "Smart Features"),
            ("📊 Portfolio Optimizer", "Portfolio"),
            ("🎮 Achievements & Rewards", "Gamification"),
            ("⚙️ Settings", "Settings"),
        ]

        for label, page in pages:
            if st.button(label, use_container_width=True, key=f"nav_{page}"):
                st.session_state.current_page = page

        st.markdown("---")
        st.markdown("### 💡 Daily Tip")
        tip = app.GamificationEngine().get_daily_tip()
        st.info(tip)

        st.markdown("---")

        if st.session_state.portfolio:
            st.markdown("### 📊 Quick Stats")
            portfolio = st.session_state.portfolio
            st.metric("Total Portfolio", f"₹{portfolio.total_value:,.0f}")

            st.markdown("**Asset Distribution:**")
            assets = {
                "Equity": sum(portfolio.stocks.values()) + sum(portfolio.mutual_funds.values()) + portfolio.elss,
                "Debt": portfolio.fixed_deposits + portfolio.ppf + portfolio.nps,
                "Gold": portfolio.gold,
                "Others": portfolio.real_estate + portfolio.crypto + portfolio.cash,
            }
            for asset, value in assets.items():
                if value > 0:
                    pct = (value / portfolio.total_value) * 100
                    st.progress(pct / 100)
                    st.caption(f"{asset}: {pct:.1f}%")

