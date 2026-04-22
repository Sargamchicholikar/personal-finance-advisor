"""Settings page renderer."""

import hashlib

import streamlit as st


def render_settings(app) -> None:
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
                investment_experience = st.selectbox("Investment Experience", ["Beginner", "Intermediate", "Advanced"], index=1)
                has_insurance = st.checkbox("Have Life Insurance?", value=True)
                has_emergency_fund = st.checkbox("Have Emergency Fund?", value=False)

            financial_goals = st.multiselect(
                "Financial Goals",
                app.Config.FINANCIAL_GOALS,
                default=["Retirement Planning", "Children's Education"],
            )

            st.markdown("#### Risk Assessment")
            profiler = app.RiskProfiler()
            answers = []
            for q in profiler.questions:
                answer = st.radio(q["question"], options=list(q["options"].keys()), horizontal=True)
                answers.append(q["options"][answer])

            save_profile = st.form_submit_button("💾 Save Profile", use_container_width=True)
            if save_profile:
                risk_profile = profiler.calculate_risk_profile(answers)
                st.session_state.user = app.User(
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
                    has_emergency_fund=has_emergency_fund,
                )
                st.success(f"✅ Profile saved! Risk Profile: {risk_profile}")

    with tab2:
        st.markdown("### 💼 Portfolio Setup")
        with st.form("portfolio_setup"):
            st.markdown("#### Equity Investments")
            col1, col2 = st.columns(2)
            with col1:
                stock_investment = st.number_input("Direct Stock Investment (₹)", min_value=0, value=200000, step=10000)
            with col2:
                mf_investment = st.number_input("Mutual Fund Investment (₹)", min_value=0, value=300000, step=10000)

            st.markdown("#### Fixed Income & Tax Saving")
            col1, col2 = st.columns(2)
            with col1:
                fd_investment = st.number_input("Fixed Deposits (₹)", min_value=0, value=100000, step=10000)
                ppf_investment = st.number_input("PPF Investment (₹)", min_value=0, value=150000, step=10000)
                elss_investment = st.number_input("ELSS (Tax Saving MF) (₹)", min_value=0, value=50000, step=10000)
            with col2:
                nps_investment = st.number_input("NPS Investment (₹)", min_value=0, value=50000, step=10000)
                gold_investment = st.number_input("Gold Investment (₹)", min_value=0, value=50000, step=10000)

            st.markdown("#### Others")
            col1, col2 = st.columns(2)
            with col1:
                real_estate = st.number_input("Real Estate (₹)", min_value=0, value=0, step=100000)
            with col2:
                crypto = st.number_input("Cryptocurrency (₹)", min_value=0, value=0, step=10000)
            cash = st.number_input("Cash/Savings Account (₹)", min_value=0, value=100000, step=10000)

            save_portfolio = st.form_submit_button("💾 Save Portfolio", use_container_width=True)
            if save_portfolio:
                stocks = {}
                if stock_investment > 0:
                    top_stocks = list(app.Config.INDIAN_STOCKS.keys())[:5]
                    for stock in top_stocks:
                        stocks[stock] = stock_investment / len(top_stocks)

                mutual_funds = {}
                if mf_investment > 0:
                    categories = ["Large Cap", "Mid Cap", "ELSS"]
                    for category in categories:
                        mutual_funds[category] = mf_investment / len(categories)

                portfolio = app.Portfolio(
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
                    cash=cash,
                )
                portfolio.calculate_total()
                st.session_state.portfolio = portfolio
                st.success(f"✅ Portfolio saved! Total Value: ₹{portfolio.total_value:,.0f}")

    with tab3:
        st.markdown("### 🔑 API Configuration")
        provider = st.selectbox(
            "LLM Provider",
            ["Offline (No API Key)", "Gemini", "OpenRouter"],
            index=["Offline (No API Key)", "Gemini", "OpenRouter"].index(st.session_state.llm_provider)
            if st.session_state.llm_provider in ["Offline (No API Key)", "Gemini", "OpenRouter"]
            else 0,
        )
        default_model = st.session_state.llm_model or "meta-llama/llama-3.1-8b-instruct:free"
        model_name = st.text_input(
            "Model Name (for OpenRouter)",
            value=default_model,
            placeholder="e.g. meta-llama/llama-3.1-8b-instruct:free",
        )

        if provider == "Gemini":
            key_label = "Gemini API Key"
            key_placeholder = "Enter your Gemini API key"
        elif provider == "OpenRouter":
            key_label = "OpenRouter API Key"
            key_placeholder = "Enter your OpenRouter API key"
        else:
            key_label = "API Key (Not required in Offline mode)"
            key_placeholder = "Leave blank for offline mode"
        api_key = st.text_input(
            key_label,
            value=st.session_state.api_key if provider != "Offline (No API Key)" else "",
            type="password",
            placeholder=key_placeholder,
        )
        if provider == "Offline (No API Key)":
            st.success("Offline mode is completely free and needs no API key.")
            st.info("Advice will be rule-based using your salary, expenses, goals, and risk profile.")
        elif provider == "Gemini":
            st.info(
                """
                To get your Gemini API key:
                1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
                2. Sign in with your Google account
                3. Click "Create API Key"
                4. Copy and paste the key above
                """
            )
        else:
            st.info(
                """
                To get your OpenRouter API key:
                1. Visit [OpenRouter Keys](https://openrouter.ai/keys)
                2. Create an API key
                3. Paste it above
                4. Keep a valid model in model field
                """
            )
        if st.button("💾 Save Configuration", use_container_width=True, key="save_api_key"):
            if provider == "Offline (No API Key)":
                st.session_state.api_key = ""
                st.session_state.llm_provider = provider
                st.session_state.gemini_advisor = app.OfflineFinanceAdvisor()
                st.success("✅ Offline mode enabled successfully!")
            elif api_key:
                st.session_state.api_key = api_key
                st.session_state.llm_provider = provider
                st.session_state.llm_model = model_name.strip() or "meta-llama/llama-3.1-8b-instruct:free"
                if provider == "OpenRouter":
                    st.session_state.gemini_advisor = app.OpenRouterFinanceAdvisor(
                        api_key,
                        st.session_state.llm_model,
                    )
                else:
                    st.session_state.gemini_advisor = app.GeminiFinanceAdvisor(api_key)
                st.success(f"✅ {provider} configuration saved successfully!")
            else:
                st.error("Please enter a valid API key")

