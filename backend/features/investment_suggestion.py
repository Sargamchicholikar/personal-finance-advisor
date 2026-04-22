"""Rule-based investment suggestion feature."""


def investment_suggestion(risk_profile: str) -> str:
    rp = risk_profile.lower()
    if "conservative" in rp:
        return "Low-risk mix: 60-70% FD/Bonds/PPF, 20-30% debt mutual funds, 10% gold."
    if "aggressive" in rp:
        return "High-risk mix: 70-80% equity index funds/stocks, 10-20% debt funds, 5-10% gold."
    return "Balanced mix: 50-60% equity SIP, 30-40% debt funds/PPF, 10% gold."

