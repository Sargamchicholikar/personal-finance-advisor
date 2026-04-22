"""AI chat page renderer."""

import json

import streamlit as st


def render_ai_chat(app) -> None:
    st.markdown("## 💬 AI Financial Advisor Chat")

    if st.session_state.llm_provider != "Offline (No API Key)" and not st.session_state.api_key:
        st.warning("Please enter your API key in Settings first!")
        return

    if not st.session_state.gemini_advisor:
        try:
            if st.session_state.llm_provider == "OpenRouter":
                st.session_state.gemini_advisor = app.OpenRouterFinanceAdvisor(
                    st.session_state.api_key,
                    st.session_state.llm_model,
                )
            elif st.session_state.llm_provider == "Offline (No API Key)":
                st.session_state.gemini_advisor = app.OfflineFinanceAdvisor()
            else:
                st.session_state.gemini_advisor = app.GeminiFinanceAdvisor(st.session_state.api_key)
        except Exception as e:
            st.error(f"LLM initialization failed: {e}")
            st.info("Please re-save API key/provider in Settings and try again.")
            return

    chat_col, context_col = st.columns([4, 1])

    with context_col:
        st.markdown("### Context")
        portfolio_value = f"₹{st.session_state.portfolio.total_value:,.0f}" if st.session_state.portfolio else "N/A"
        st.info(
            f"""
            **Profile Loaded:**
            - Risk: {st.session_state.user.risk_profile if st.session_state.user else 'N/A'}
            - Goals: {len(st.session_state.user.financial_goals) if st.session_state.user else 0}
            - Portfolio: {portfolio_value}
            """
        )

    with chat_col:
        st.markdown("### Quick Actions")
        quick_actions = [
            "📊 Analyze my portfolio",
            "💰 Tax saving suggestions",
            "🏠 Home loan planning",
            "👶 Child education planning",
            "🎯 Retirement planning",
            "📈 Best investments this month",
            "🛡️ Insurance recommendations",
            "💎 Should I invest in gold?",
        ]

        for row in range(2):
            cols = st.columns(4)
            for col_idx in range(4):
                action_idx = row * 4 + col_idx
                if action_idx < len(quick_actions):
                    button_key = f"quick_action_{action_idx}_{quick_actions[action_idx][:10]}"
                    if cols[col_idx].button(quick_actions[action_idx], use_container_width=True, key=button_key):
                        st.session_state.chat_history.append({"role": "user", "content": quick_actions[action_idx]})

                        with st.spinner("🤔 Thinking..."):
                            response = st.session_state.gemini_advisor.get_advice(
                                quick_actions[action_idx],
                                st.session_state.user,
                                st.session_state.portfolio,
                            )

                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                        st.rerun()

        st.markdown("### Conversation")
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

        st.markdown("### Ask your financial question...")
        with st.form("chat_input", clear_on_submit=True):
            user_input = st.text_area(
                "Type your question here:",
                placeholder="E.g., How should I invest ₹50,000 for my child's education in 10 years?",
                height=100,
                label_visibility="collapsed",
            )

            col1, col2, _ = st.columns([1, 1, 4])
            with col1:
                submitted = st.form_submit_button("Send 📤", use_container_width=True, type="primary")
            with col2:
                if st.form_submit_button("Clear Chat 🗑️", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()

            if submitted and user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.chat_memory.update(app.SmartFinanceEngine.extract_memory_from_text(user_input))
                memory_context = ""
                if st.session_state.chat_memory:
                    memory_context = (
                        "Use this remembered context while responding: "
                        f"{json.dumps(st.session_state.chat_memory)}"
                    )

                with st.spinner("🤖 AI is analyzing..."):
                    response = st.session_state.gemini_advisor.get_advice(
                        f"{user_input}\n\n{memory_context}",
                        st.session_state.user,
                        st.session_state.portfolio,
                    )

                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

