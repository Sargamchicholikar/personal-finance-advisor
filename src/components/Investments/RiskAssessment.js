import React, { useState } from 'react';
import styles from './Investments.module.css';

const RiskAssessment = () => {
  const [riskTolerance, setRiskTolerance] = useState('moderate');
  const [investmentStrategy, setInvestmentStrategy] = useState('');

  const handleRiskChange = (event) => {
    setRiskTolerance(event.target.value);
    suggestInvestmentStrategy(event.target.value);
  };

  const suggestInvestmentStrategy = (riskLevel) => {
    let strategy;
    switch (riskLevel) {
      case 'conservative':
        strategy = 'Focus on low-risk investments like bonds and savings accounts.';
        break;
      case 'moderate':
        strategy = 'Consider a balanced portfolio with a mix of stocks and bonds.';
        break;
      case 'aggressive':
        strategy = 'Invest heavily in stocks and high-growth assets for maximum returns.';
        break;
      default:
        strategy = '';
    }
    setInvestmentStrategy(strategy);
  };

  return (
    <div className={styles.riskAssessment}>
      <h2>Risk Assessment</h2>
      <div className={styles.riskSelector}>
        <label htmlFor="riskTolerance">Select your risk tolerance:</label>
        <select id="riskTolerance" value={riskTolerance} onChange={handleRiskChange}>
          <option value="conservative">Conservative</option>
          <option value="moderate">Moderate</option>
          <option value="aggressive">Aggressive</option>
        </select>
      </div>
      {investmentStrategy && (
        <div className={styles.strategySuggestion}>
          <h3>Suggested Investment Strategy:</h3>
          <p>{investmentStrategy}</p>
        </div>
      )}
    </div>
  );
};

export default RiskAssessment;