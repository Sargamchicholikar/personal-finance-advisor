"""Portfolio page renderer."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_portfolio(app) -> None:
    st.markdown("## 📊 Portfolio Optimizer")

    if not st.session_state.portfolio:
        st.warning("Please set up your portfolio in Settings first!")
        return

    optimizer = app.PortfolioOptimizer()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Current Portfolio Allocation")
        portfolio = st.session_state.portfolio
        labels, values = [], []

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

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Portfolio Metrics")
        equity_allocation = (sum(portfolio.stocks.values()) + sum(portfolio.mutual_funds.values()) + portfolio.elss) / portfolio.total_value * 100
        debt_allocation = (portfolio.fixed_deposits + portfolio.ppf + portfolio.nps) / portfolio.total_value * 100
        st.metric("Total Value", f"₹{portfolio.total_value:,.0f}")
        st.metric("Equity %", f"{equity_allocation:.1f}%")
        st.metric("Debt %", f"{debt_allocation:.1f}%")
        st.metric("Liquidity", f"₹{portfolio.cash:,.0f}")

    st.markdown("### 🎯 Portfolio Optimization")
    with st.form("optimize_portfolio"):
        col1, col2, col3 = st.columns(3)

        with col1:
            selected_stocks = st.multiselect(
                "Select Stocks to Optimize",
                list(app.Config.INDIAN_STOCKS.keys()),
                default=list(app.Config.INDIAN_STOCKS.keys())[:5],
            )

        with col2:
            risk_tolerance = st.selectbox("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"], index=1)

        with col3:
            investment_amount = st.number_input("Investment Amount (₹)", min_value=10000, value=100000, step=10000)

        optimize_btn = st.form_submit_button("🚀 Optimize Portfolio", use_container_width=True)
        if optimize_btn and selected_stocks:
            with st.spinner("Optimizing portfolio..."):
                stock_symbols = [app.Config.INDIAN_STOCKS[s] for s in selected_stocks]
                result = optimizer.optimize_portfolio(stock_symbols, risk_tolerance)

                if result["success"]:
                    st.success("✅ Optimization Complete!")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Expected Return", f"{result['expected_return']:.2f}%")
                    with col2:
                        st.metric("Risk (Std Dev)", f"{result['risk']:.2f}%")
                    with col3:
                        st.metric("Sharpe Ratio", f"{result['sharpe_ratio']:.2f}")

                    st.markdown("#### Recommended Allocation")
                    allocation_df = pd.DataFrame(
                        [
                            {
                                "Stock": stock,
                                "Allocation %": f"{weight*100:.1f}%",
                                "Amount (₹)": f"{investment_amount * weight:,.0f}",
                            }
                            for stock, weight in result["weights"].items()
                            if weight > 0.01
                        ]
                    )
                    st.dataframe(allocation_df, use_container_width=True)
                else:
                    st.error(f"Optimization failed: {result.get('error', 'Unknown error')}")

