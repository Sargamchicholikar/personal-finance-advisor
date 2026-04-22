"""Smart features page renderer."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render_smart_features(app) -> None:
    st.markdown("## 🧠 Smart Financial Features")
    st.caption("Lightweight analytics designed to stay Vercel-friendly.")

    user = st.session_state.user
    if not user:
        st.warning("Please complete your profile in Settings first.")
        return

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Personalized Analysis",
            "Expense Analyzer (CSV)",
            "Predictions & Alerts",
            "Goal Planning",
            "Investment Suggestion",
            "Deep Learning Forecast",
        ]
    )

    with tab1:
        st.markdown("### Personalized Financial Analysis")
        col1, col2, col3 = st.columns(3)
        with col1:
            salary = st.number_input("Monthly Salary (₹)", min_value=0.0, value=float(user.income), step=1000.0)
        with col2:
            monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=float(user.expenses), step=1000.0)
        with col3:
            monthly_savings = st.number_input(
                "Monthly Savings (₹)",
                min_value=0.0,
                value=max(float(user.income - user.expenses), 0.0),
                step=1000.0,
            )

        if st.button("Analyze My Financial Health", use_container_width=True):
            result = app.SmartFinanceEngine.personalized_analysis(salary, monthly_expenses, monthly_savings)
            if "error" in result:
                st.error(result["error"])
            else:
                st.success(result["message"])
                m1, m2, m3 = st.columns(3)
                m1.metric("Savings %", f"{result['savings_rate']:.1f}%")
                m2.metric("Expense %", f"{result['expense_ratio']:.1f}%")
                m3.metric("Gap to Ideal", f"{result['gap']:.1f}%")

    with tab2:
        st.markdown("### Expense Analyzer")
        csv_file = st.file_uploader("Upload bank statement CSV", type=["csv"])
        if csv_file is not None:
            try:
                df = pd.read_csv(csv_file)
                analysis = app.SmartFinanceEngine.analyze_expense_csv(df)
                st.session_state.expense_analysis = analysis
                st.success("CSV analyzed successfully.")

                c1, c2, c3 = st.columns(3)
                c1.metric("Total Expenses", f"₹{analysis['total_expense']:,.0f}")
                c2.metric("Top Category", analysis["top_category"])
                c3.metric("Transactions", f"{len(analysis['clean_df'])}")

                if not analysis["by_category"].empty:
                    pie = px.pie(analysis["by_category"], names="Category", values="Amount", title="Spending by Category")
                    st.plotly_chart(pie, use_container_width=True)
                if not analysis["monthly_trend"].empty:
                    line = px.line(analysis["monthly_trend"], x="Month", y="Amount", markers=True, title="Monthly Expense Trend")
                    st.plotly_chart(line, use_container_width=True)
            except Exception as e:
                st.error(f"Could not process CSV: {e}")

    with tab3:
        st.markdown("### Future Expense Prediction & Smart Alerts")
        analysis = st.session_state.expense_analysis
        if analysis and not analysis["monthly_trend"].empty:
            pred = app.SmartFinanceEngine.predict_next_month_expense(analysis["monthly_trend"])
            if pred["predicted"] is not None:
                st.metric("Predicted Next Month Expense", f"₹{pred['predicted']:,.0f}", pred["message"])
        else:
            st.info("Upload CSV in the Expense Analyzer tab to enable prediction.")

        alerts = app.SmartFinanceEngine.generate_alerts(user, analysis)
        if alerts:
            st.markdown("#### Alerts")
            for alert in alerts:
                st.warning(f"⚠️ {alert}")
        else:
            st.success("No risk alerts detected right now.")

    with tab4:
        st.markdown("### Goal-Based Planning")
        goal_name = st.text_input("Goal name", value="Buy laptop")
        goal_amount = st.number_input("Target amount (₹)", min_value=1000.0, value=60000.0, step=1000.0)
        months = st.number_input("Target timeline (months)", min_value=1, value=12, step=1)
        if st.button("Create Goal Plan", use_container_width=True):
            plan = app.SmartFinanceEngine.goal_plan(goal_amount, int(months))
            st.info(f"For **{goal_name}**, save **₹{plan['monthly_needed']:,.0f}/month** for **{int(months)} months**.")

    with tab5:
        st.markdown("### Rule-Based Investment Suggestion")
        suggestion = app.SmartFinanceEngine.investment_suggestion(user.risk_profile)
        st.success(f"Risk profile: **{user.risk_profile}**")
        st.write(suggestion)

    with tab6:
        st.markdown("### Deep Learning Expense Forecast")
        st.caption("Tiny neural network (NumPy MLP) + baseline comparison for project submission.")
        analysis = st.session_state.expense_analysis
        if not analysis or analysis["monthly_trend"].empty:
            st.info("Upload CSV first in Expense Analyzer to train the DL model.")
        else:
            window = st.slider("Sequence window (months)", min_value=2, max_value=6, value=3, step=1)
            if st.button("Train DL Model & Forecast", use_container_width=True):
                result = app.SmartFinanceEngine.run_deep_learning_forecast(analysis["monthly_trend"], window=window)
                if "error" in result:
                    st.error(result["error"])
                else:
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Next Month (DL)", f"₹{result['predicted_next']:,.0f}")
                    c2.metric("DL MAE", f"{result['dl_mae']:.2f}")
                    c3.metric("Baseline MAE", f"{result['baseline_mae']:.2f}")

                    loss_df = pd.DataFrame({"Epoch": list(range(1, len(result["loss_curve"]) + 1)), "Loss": result["loss_curve"]})
                    loss_fig = px.line(loss_df, x="Epoch", y="Loss", title="DL Training Loss Curve")
                    st.plotly_chart(loss_fig, use_container_width=True)

                    if not result["comparison_df"].empty:
                        cmp = result["comparison_df"]
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(x=cmp["Index"], y=cmp["Actual"], mode="lines+markers", name="Actual"))
                        fig.add_trace(go.Scatter(x=cmp["Index"], y=cmp["DL_Prediction"], mode="lines+markers", name="DL Prediction"))
                        fig.update_layout(title="Test Set: Actual vs DL Prediction", xaxis_title="Test Sample", yaxis_title="Expense")
                        st.plotly_chart(fig, use_container_width=True)

                    if result["dl_mae"] <= result["baseline_mae"]:
                        st.success("DL model performs better (or equal) than baseline on test set.")
                    else:
                        st.warning("Baseline outperformed DL on this data. You can try a different window size.")

