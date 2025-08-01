import React, { useState, useEffect } from 'react';
import { getInvestmentSuggestions } from '../../services/investmentService';
import styles from '../../styles/Investments.module.css';

const InvestmentSuggestionsEnhanced = ({ userProfile }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [portfolio, setPortfolio] = useState([]);
  const [riskAssessment, setRiskAssessment] = useState(null);
  const [investmentGoals, setInvestmentGoals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [calculatorData, setCalculatorData] = useState({
    initialAmount: '',
    monthlyContribution: '',
    expectedReturn: '7',
    years: '10'
  });

  useEffect(() => {
    if (userProfile) {
      assessRiskProfile();
      generateSuggestions();
      loadPortfolio();
    }
  }, [userProfile]);

  const assessRiskProfile = () => {
    const { age, income, savings, riskTolerance } = userProfile;
    
    let riskScore = 0;
    
    // Age factor (younger = higher risk tolerance)
    if (age < 30) riskScore += 30;
    else if (age < 40) riskScore += 25;
    else if (age < 50) riskScore += 20;
    else if (age < 60) riskScore += 15;
    else riskScore += 10;

    // Income stability factor
    if (income > 100000) riskScore += 25;
    else if (income > 50000) riskScore += 20;
    else riskScore += 15;

    // Savings ratio factor
    const savingsRatio = savings / income;
    if (savingsRatio > 0.3) riskScore += 25;
    else if (savingsRatio > 0.2) riskScore += 20;
    else if (savingsRatio > 0.1) riskScore += 15;
    else riskScore += 10;

    // Risk tolerance preference
    if (riskTolerance === 'aggressive') riskScore += 20;
    else if (riskTolerance === 'moderate') riskScore += 15;
    else riskScore += 10;

    let riskLevel, recommendations;
    if (riskScore >= 80) {
      riskLevel = 'High Risk, High Reward';
      recommendations = [
        'Individual growth stocks',
        'Emerging market funds',
        'Technology sector ETFs',
        'Cryptocurrency (small allocation)'
      ];
    } else if (riskScore >= 60) {
      riskLevel = 'Moderate Risk';
      recommendations = [
        'S&P 500 index funds',
        'Balanced mutual funds',
        'Real estate investment trusts (REITs)',
        'Corporate bonds'
      ];
    } else {
      riskLevel = 'Conservative';
      recommendations = [
        'Government bonds',
        'High-yield savings accounts',
        'Certificate of deposits (CDs)',
        'Blue-chip dividend stocks'
      ];
    }

    setRiskAssessment({
      score: riskScore,
      level: riskLevel,
      recommendations
    });
  };

  const generateSuggestions = async () => {
    setLoading(true);
    try {
      const suggestions = await getInvestmentSuggestions(userProfile);
      
      // Enhanced suggestions with real calculations
      const enhancedSuggestions = [
        {
          id: 1,
          type: 'Emergency Fund',
          description: 'Build an emergency fund covering 3-6 months of expenses',
          targetAmount: userProfile.expenses * 6,
          priority: 'High',
          timeframe: '6-12 months',
          expectedReturn: '2-3%',
          riskLevel: 'Very Low'
        },
        {
          id: 2,
          type: 'Index Fund Investment',
          description: 'Low-cost diversified index fund for long-term growth',
          targetAmount: userProfile.income * 0.15,
          priority: 'High',
          timeframe: '5+ years',
          expectedReturn: '7-10%',
          riskLevel: 'Moderate'
        },
        {
          id: 3,
          type: 'Retirement Account',
          description: '401(k) or IRA contribution for tax advantages',
          targetAmount: userProfile.income * 0.2,
          priority: 'High',
          timeframe: '10+ years',
          expectedReturn: '8-12%',
          riskLevel: 'Moderate to High'
        }
      ];

      setSuggestions(enhancedSuggestions);
    } catch (error) {
      console.error('Error generating suggestions:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadPortfolio = () => {
    const saved = localStorage.getItem(`portfolio_${userProfile.id || 'default'}`);
    if (saved) {
      setPortfolio(JSON.parse(saved));
    }
  };

  const addToPortfolio = (suggestion) => {
    const portfolioItem = {
      id: Date.now(),
      ...suggestion,
      dateAdded: new Date().toISOString(),
      currentValue: 0,
      contributions: []
    };

    const updatedPortfolio = [...portfolio, portfolioItem];
    setPortfolio(updatedPortfolio);
    localStorage.setItem(`portfolio_${userProfile.id || 'default'}`, JSON.stringify(updatedPortfolio));
  };

  const calculateInvestmentGrowth = () => {
    const { initialAmount, monthlyContribution, expectedReturn, years } = calculatorData;
    
    if (!initialAmount && !monthlyContribution) return null;

    const principal = parseFloat(initialAmount) || 0;
    const monthly = parseFloat(monthlyContribution) || 0;
    const rate = parseFloat(expectedReturn) / 100 / 12;
    const months = parseInt(years) * 12;

    // Compound interest calculation
    const futureValuePrincipal = principal * Math.pow(1 + rate, months);
    const futureValueAnnuity = monthly * (Math.pow(1 + rate, months) - 1) / rate;
    const totalFutureValue = futureValuePrincipal + futureValueAnnuity;
    const totalContributions = principal + (monthly * months);
    const totalGains = totalFutureValue - totalContributions;

    return {
      futureValue: totalFutureValue,
      totalContributions,
      totalGains,
      roi: ((totalGains / totalContributions) * 100)
    };
  };

  const investmentProjection = calculateInvestmentGrowth();

  return (
    <div className={styles.investmentContainer}>
      <h3 className={styles.sectionTitle}>📈 Investment Suggestions & Portfolio</h3>

      {/* Risk Assessment */}
      {riskAssessment && (
        <div className={styles.riskAssessmentCard}>
          <h4>Your Risk Profile</h4>
          <div className={styles.riskLevel}>
            Risk Level: <span className={styles.riskScore}>{riskAssessment.level}</span>
            <span className={styles.scoreValue}>({riskAssessment.score}/100)</span>
          </div>
          <div className={styles.recommendations}>
            <h5>Recommended Investment Types:</h5>
            <ul>
              {riskAssessment.recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Investment Calculator */}
      <div className={styles.calculatorCard}>
        <h4>Investment Growth Calculator</h4>
        <div className={styles.calculatorInputs}>
          <input
            type="number"
            placeholder="Initial amount ($)"
            value={calculatorData.initialAmount}
            onChange={(e) => setCalculatorData({...calculatorData, initialAmount: e.target.value})}
            className={styles.calculatorInput}
          />
          <input
            type="number"
            placeholder="Monthly contribution ($)"
            value={calculatorData.monthlyContribution}
            onChange={(e) => setCalculatorData({...calculatorData, monthlyContribution: e.target.value})}
            className={styles.calculatorInput}
          />
          <select
            value={calculatorData.expectedReturn}
            onChange={(e) => setCalculatorData({...calculatorData, expectedReturn: e.target.value})}
            className={styles.calculatorInput}
          >
            <option value="3">3% (Conservative)</option>
            <option value="7">7% (Moderate)</option>
            <option value="10">10% (Aggressive)</option>
          </select>
          <select
            value={calculatorData.years}
            onChange={(e) => setCalculatorData({...calculatorData, years: e.target.value})}
            className={styles.calculatorInput}
          >
            <option value="5">5 years</option>
            <option value="10">10 years</option>
            <option value="20">20 years</option>
            <option value="30">30 years</option>
          </select>
        </div>

        {investmentProjection && (
          <div className={styles.projectionResults}>
            <div className={styles.projectionItem}>
              <span>Future Value:</span>
              <span className={styles.projectionValue}>
                ${investmentProjection.futureValue.toLocaleString('en-US', {maximumFractionDigits: 0})}
              </span>
            </div>
            <div className={styles.projectionItem}>
              <span>Total Contributions:</span>
              <span>${investmentProjection.totalContributions.toLocaleString('en-US', {maximumFractionDigits: 0})}</span>
            </div>
            <div className={styles.projectionItem}>
              <span>Total Gains:</span>
              <span className={styles.gainsValue}>
                ${investmentProjection.totalGains.toLocaleString('en-US', {maximumFractionDigits: 0})}
              </span>
            </div>
            <div className={styles.projectionItem}>
              <span>ROI:</span>
              <span className={styles.roiValue}>{investmentProjection.roi.toFixed(1)}%</span>
            </div>
          </div>
        )}
      </div>

      {/* Investment Suggestions */}
      <div className={styles.suggestionsSection}>
        <h4>Personalized Investment Suggestions</h4>
        {loading ? (
          <div className={styles.loading}>Generating suggestions...</div>
        ) : (
          <div className={styles.suggestionsList}>
            {suggestions.map(suggestion => (
              <div key={suggestion.id} className={styles.suggestionCard}>
                <div className={styles.suggestionHeader}>
                  <h5>{suggestion.type}</h5>
                  <span className={`${styles.priority} ${styles[suggestion.priority.toLowerCase()]}`}>
                    {suggestion.priority} Priority
                  </span>
                </div>
                <p className={styles.suggestionDescription}>{suggestion.description}</p>
                <div className={styles.suggestionMetrics}>
                  <div className={styles.metric}>
                    <span>Target Amount:</span>
                    <span>${suggestion.targetAmount.toLocaleString()}</span>
                  </div>
                  <div className={styles.metric}>
                    <span>Expected Return:</span>
                    <span>{suggestion.expectedReturn}</span>
                  </div>
                  <div className={styles.metric}>
                    <span>Risk Level:</span>
                    <span>{suggestion.riskLevel}</span>
                  </div>
                  <div className={styles.metric}>
                    <span>Timeframe:</span>
                    <span>{suggestion.timeframe}</span>
                  </div>
                </div>
                <button
                  onClick={() => addToPortfolio(suggestion)}
                  className={styles.addToPortfolioButton}
                >
                  Add to Portfolio
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Current Portfolio */}
      <div className={styles.portfolioSection}>
        <h4>Your Investment Portfolio</h4>
        {portfolio.length === 0 ? (
          <div className={styles.emptyPortfolio}>
            No investments in your portfolio yet. Add some from the suggestions above!
          </div>
        ) : (
          <div className={styles.portfolioList}>
            {portfolio.map(item => (
              <div key={item.id} className={styles.portfolioItem}>
                <div className={styles.portfolioHeader}>
                  <h6>{item.type}</h6>
                  <span className={styles.portfolioDate}>
                    Added: {new Date(item.dateAdded).toLocaleDateString()}
                  </span>
                </div>
                <div className={styles.portfolioMetrics}>
                  <div>Target: ${item.targetAmount.toLocaleString()}</div>
                  <div>Current: ${item.currentValue.toFixed(2)}</div>
                  <div>Expected Return: {item.expectedReturn}</div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default InvestmentSuggestionsEnhanced;
