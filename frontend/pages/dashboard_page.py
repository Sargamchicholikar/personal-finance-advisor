"""Dashboard page renderer."""

import plotly.graph_objects as go
import streamlit as st


def render_dashboard(app) -> None:
    st.markdown("## 📊 Financial Dashboard")

    if not st.session_state.user:
        st.warning("Please complete your profile in Settings first!")
        return

    user = st.session_state.user
    portfolio = st.session_state.portfolio

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        savings_rate = ((user.income - user.expenses) / user.income) * 100
        st.metric("Savings Rate", f"{savings_rate:.1f}%", "Good" if savings_rate > 20 else "Improve")

    with col2:
        if portfolio:
            monthly_investment = portfolio.total_value / 12
            investment_rate = (monthly_investment / user.income) * 100
            st.metric("Investment Rate", f"{investment_rate:.1f}%", "Excellent" if investment_rate > 30 else "Good")
        else:
            st.metric("Investment Rate", "0%", "Start Investing")

    with col3:
        emergency_months = 0
        if portfolio:
            emergency_funds = portfolio.cash + portfolio.fixed_deposits
            emergency_months = emergency_funds / user.expenses if user.expenses > 0 else 0
        st.metric("Emergency Fund", f"{emergency_months:.1f} months", "Adequate" if emergency_months >= 6 else "Build More")

    with col4:
        debt_ratio = 0
        st.metric("Debt-to-Income", f"{debt_ratio:.1f}%", "Healthy" if debt_ratio < 30 else "High")

    expense_analysis = st.session_state.expense_analysis
    if expense_analysis:
        st.markdown("### 📌 Expense Snapshot")
        c1, c2, c3 = st.columns(3)
        c1.metric("Monthly Expense (CSV)", f"₹{expense_analysis['total_expense']:,.0f}")
        c2.metric("Top Expense Category", expense_analysis["top_category"])
        top_pct = 0.0
        if not expense_analysis["by_category"].empty and expense_analysis["total_expense"] > 0:
            top_amt = float(expense_analysis["by_category"].iloc[0]["Amount"])
            top_pct = (top_amt / expense_analysis["total_expense"]) * 100
        c3.metric("Top Category Share", f"{top_pct:.1f}%")

    st.markdown("### 🏥 Financial Health Analysis")

    health_scores = {
        "Savings": min(100, savings_rate * 3),
        "Investments": min(100, (portfolio.total_value / (user.income * 12)) * 100) if portfolio else 0,
        "Emergency Fund": min(100, (emergency_months / 6) * 100),
        "Insurance": 100 if user.has_insurance else 30,
        "Debt Management": max(0, 100 - debt_ratio * 2),
    }

    fig = go.Figure(
        data=[
            go.Bar(
                x=list(health_scores.keys()),
                y=list(health_scores.values()),
                marker_color=["green" if v >= 70 else "orange" if v >= 40 else "red" for v in health_scores.values()],
            )
        ]
    )
    fig.update_layout(title="Financial Health Scores", yaxis_title="Score (0-100)", showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

    overall_health = sum(health_scores.values()) / len(health_scores)
    if overall_health >= 70:
        st.success(f"🎉 Excellent Financial Health! Score: {overall_health:.0f}/100")
    elif overall_health >= 50:
        st.warning(f"⚠️ Good Financial Health. Room for improvement. Score: {overall_health:.0f}/100")
    else:
        st.error(f"🚨 Financial Health Needs Attention! Score: {overall_health:.0f}/100")

    st.markdown("### 💡 Personalized Recommendations")

    recommendations = []
    if savings_rate < 20:
        recommendations.append(
            {
                "priority": "High",
                "action": "Increase savings rate to at least 20%",
                "how": "Review and cut unnecessary expenses, automate savings",
            }
        )
    if emergency_months < 6:
        recommendations.append(
            {
                "priority": "High",
                "action": f"Build emergency fund to 6 months (need ₹{(6-emergency_months)*user.expenses:,.0f} more)",
                "how": "Open high-yield savings account, set up automatic transfer",
            }
        )
    if not user.has_insurance:
        recommendations.append(
            {
                "priority": "Critical",
                "action": "Get adequate insurance coverage",
                "how": f"Term insurance: ₹{user.income*12*10:,.0f}, Health insurance: ₹5-10 lakhs",
            }
        )
    if portfolio and portfolio.ppf == 0:
        recommendations.append(
            {
                "priority": "Medium",
                "action": "Start PPF account for tax-free returns",
                "how": "Invest up to ₹1.5 lakhs annually for Section 80C benefit",
            }
        )

    for rec in recommendations[:3]:
        if rec["priority"] == "Critical":
            st.error(f"🚨 **{rec['priority']}**: {rec['action']}")
        elif rec["priority"] == "High":
            st.warning(f"⚠️ **{rec['priority']}**: {rec['action']}")
        else:
            st.info(f"ℹ️ **{rec['priority']}**: {rec['action']}")
        st.caption(f"How: {rec['how']}")

