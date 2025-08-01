import React, { useState } from 'react';
import styles from './Investments.module.css';

const InvestmentCalculator = () => {
  const [initialInvestment, setInitialInvestment] = useState(0);
  const [monthlyContribution, setMonthlyContribution] = useState(0);
  const [years, setYears] = useState(0);
  const [interestRate, setInterestRate] = useState(0);
  const [futureValue, setFutureValue] = useState(null);

  const calculateInvestment = () => {
    const rate = interestRate / 100 / 12;
    const months = years * 12;
    const futureValue =
      initialInvestment * Math.pow(1 + rate, months) +
      monthlyContribution * ((Math.pow(1 + rate, months) - 1) / rate);
    setFutureValue(futureValue.toFixed(2));
  };

  return (
    <div className={styles.calculator}>
      <h2>Investment Calculator</h2>
      <div className={styles.inputGroup}>
        <label>Initial Investment ($):</label>
        <input
          type="number"
          value={initialInvestment}
          onChange={(e) => setInitialInvestment(Number(e.target.value))}
        />
      </div>
      <div className={styles.inputGroup}>
        <label>Monthly Contribution ($):</label>
        <input
          type="number"
          value={monthlyContribution}
          onChange={(e) => setMonthlyContribution(Number(e.target.value))}
        />
      </div>
      <div className={styles.inputGroup}>
        <label>Investment Duration (Years):</label>
        <input
          type="number"
          value={years}
          onChange={(e) => setYears(Number(e.target.value))}
        />
      </div>
      <div className={styles.inputGroup}>
        <label>Expected Annual Interest Rate (%):</label>
        <input
          type="number"
          value={interestRate}
          onChange={(e) => setInterestRate(Number(e.target.value))}
        />
      </div>
      <button onClick={calculateInvestment} className={styles.calculateButton}>
        Calculate
      </button>
      {futureValue !== null && (
        <div className={styles.result}>
          <h3>Future Value: ${futureValue}</h3>
        </div>
      )}
    </div>
  );
};

export default InvestmentCalculator;