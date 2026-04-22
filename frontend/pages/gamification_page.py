"""Gamification page renderer."""

import random
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_gamification(app) -> None:
    st.markdown("## 🎮 Achievements & Rewards")

    if not st.session_state.user:
        st.warning("Please complete your profile in Settings first to start earning achievements!")
        return

    engine = app.GamificationEngine()
    user = st.session_state.user

    if not st.session_state.portfolio:
        st.session_state.portfolio = app.Portfolio(
            user_id=user.user_id,
            stocks={},
            mutual_funds={},
            fixed_deposits=0,
            ppf=0,
            nps=0,
            gold=0,
            real_estate=0,
            crypto=0,
            cash=0,
            elss=0,
        )

    portfolio = st.session_state.portfolio
    new_achievements = engine.check_achievements(user, portfolio)
    if new_achievements:
        st.balloons()
        for achievement in new_achievements:
            st.success(f"🎉 New Achievement Unlocked: {achievement['badge']} **{achievement['name']}** (+{achievement['points']} pts)")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    level_name, level_emoji, progress = engine.get_wealth_level(user.wealth_score)

    with col1:
        st.metric("Wealth Score", f"{user.wealth_score} pts", f"{level_emoji}")
    with col2:
        st.metric("Current Level", level_name, f"Progress: {progress:.0f}%")
    with col3:
        st.metric("Achievements", f"{len(user.badges)}/{len(engine.challenges)}", f"{len(user.badges)/len(engine.challenges)*100:.0f}% Complete")
    with col4:
        next_level_points = 0
        for threshold in [100, 500, 1000, 2000, 5000, 10000, 20000]:
            if user.wealth_score < threshold:
                next_level_points = threshold - user.wealth_score
                break
        st.metric("To Next Level", f"{next_level_points} pts", "Keep going!")

    st.progress(progress / 100)

    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Achievements", "🎯 Daily Challenges", "🎁 Rewards", "📈 Progress Tracker"])

    with tab1:
        st.markdown("### 🏆 Achievement Categories")
        st.info("Complete tasks to unlock achievements and earn points! Each achievement has specific requirements.")

        categories = {}
        for ach_id, ach in engine.challenges.items():
            category = ach.get("category", "General")
            if category not in categories:
                categories[category] = []
            categories[category].append((ach_id, ach))

        for category, achievements in categories.items():
            with st.expander(
                f"**{category} Achievements** ({sum(1 for a in achievements if a[0] in user.badges)}/{len(achievements)} completed)",
                expanded=True,
            ):
                cols = st.columns(3)
                for idx, (ach_id, achievement) in enumerate(achievements):
                    with cols[idx % 3]:
                        is_earned = ach_id in user.badges
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
                                progress_percent = min(100, (stats["asset_classes"] / 5) * 100)
                                progress_text = f"{stats['asset_classes']}/5 classes"
                            elif ach_id == "equity_investor" and portfolio:
                                equity_value = sum(portfolio.stocks.values()) + sum(portfolio.mutual_funds.values())
                                progress_percent = min(100, (equity_value / 100000) * 100)
                                progress_text = f"₹{equity_value:,.0f}/₹1,00,000"
                            elif ach_id == "tax_saver" and portfolio:
                                tax_savings = portfolio.ppf + portfolio.elss
                                progress_percent = min(100, (tax_savings / 150000) * 100)
                                progress_text = f"₹{tax_savings:,.0f}/₹1,50,000"

                        if is_earned:
                            st.success(f"{achievement['badge']} **{achievement['name']}**")
                            st.caption(f"✅ Completed • +{achievement['points']} pts")
                        else:
                            st.info(f"🔒 **{achievement['name']}**")
                            st.caption(achievement["description"])
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
            st.info(
                f"""
                **Task:** {daily_challenge['task']}

                **Reward:** {daily_challenge['points']} points

                Complete daily challenges to maintain your streak!
                """
            )
            if st.button("✅ Mark as Complete", use_container_width=True, key="daily_challenge_complete"):
                user.wealth_score += daily_challenge["points"]
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

        st.markdown("#### 📅 Weekly Challenges")
        weekly_challenges = [
            {"task": "Complete 5 daily challenges", "points": 50, "progress": 3, "total": 5},
            {"task": "Increase portfolio value by 2%", "points": 100, "progress": 1.2, "total": 2},
            {"task": "Ask AI advisor 3 questions", "points": 30, "progress": len(st.session_state.chat_history) // 2, "total": 3},
            {"task": "Review and update goals", "points": 40, "progress": 0, "total": 1},
        ]
        for challenge in weekly_challenges:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{challenge['task']}**")
                progress_pct = min(100, (challenge["progress"] / challenge["total"]) * 100)
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
        unlocked_rewards = [r for r in rewards if r["unlocked"]]
        locked_rewards = [r for r in rewards if not r["unlocked"]]

        if unlocked_rewards:
            st.markdown("#### ✅ Unlocked Rewards")
            cols = st.columns(3)
            for idx, reward in enumerate(unlocked_rewards):
                with cols[idx % 3]:
                    st.success(f"{reward['icon']} **{reward['reward']}**")
                    st.caption(f"Unlocked at {reward['threshold']} pts")

        if locked_rewards:
            st.markdown("#### 🔒 Upcoming Rewards")
            for reward in locked_rewards[:3]:
                col1, col2, col3 = st.columns([1, 3, 1])
                with col1:
                    st.markdown("### 🔒")
                with col2:
                    st.markdown(f"**{reward['reward']}**")
                    points_needed = reward["threshold"] - user.wealth_score
                    st.caption(f"Need {points_needed} more points")
                    st.progress(min(100, user.wealth_score / reward["threshold"] * 100) / 100)
                with col3:
                    st.info(f"{reward['threshold']} pts")

        st.markdown("#### 💎 Bonus Opportunities")
        col1, col2 = st.columns(2)
        with col1:
            st.info(
                """
                **🎯 Weekly Bonus**
                Complete all weekly challenges
                Reward: +200 bonus points
                """
            )
        with col2:
            st.info(
                """
                **📈 Growth Bonus**
                Grow portfolio by 5% this month
                Reward: +500 bonus points
                """
            )

    with tab4:
        st.markdown("### 📈 Your Progress Overview")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 Score Progress")
            dates = pd.date_range(end=datetime.now(), periods=30, freq="D")
            scores = [max(0, user.wealth_score - (30 - i) * 20 + random.randint(-10, 30)) for i in range(30)]
            fig = go.Figure(
                data=[
                    go.Scatter(
                        x=dates,
                        y=scores,
                        mode="lines+markers",
                        line=dict(color="#6C63FF", width=3),
                        marker=dict(size=5),
                        fill="tozeroy",
                        fillcolor="rgba(108, 99, 255, 0.2)",
                    )
                ]
            )
            fig.update_layout(title="Last 30 Days", xaxis_title="Date", yaxis_title="Score", height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### 🏆 Category Progress")
            categories_data = []
            for category in ["Beginner", "Savings", "Investment", "Tax", "Goals"]:
                category_achievements = [a for _, a in engine.challenges.items() if a.get("category") == category]
                completed = sum(1 for a_id, a in engine.challenges.items() if a.get("category") == category and a_id in user.badges)
                total = len(category_achievements)
                percentage = (completed / total * 100) if total > 0 else 0
                categories_data.append({"Category": category, "Completed": percentage})

            df = pd.DataFrame(categories_data)
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=df["Category"],
                        y=df["Completed"],
                        marker_color=["green" if v >= 60 else "orange" if v >= 30 else "red" for v in df["Completed"]],
                    )
                ]
            )
            fig.update_layout(title="Completion by Category (%)", yaxis_title="Completion %", height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

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

