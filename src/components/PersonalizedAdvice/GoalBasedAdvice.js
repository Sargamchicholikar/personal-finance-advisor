import React from 'react';
import styles from './GoalBasedAdvice.module.css';

const GoalBasedAdvice = ({ goals, userProfile }) => {
  const renderAdvice = (goal) => {
    switch (goal.type) {
      case 'savings':
        return `To achieve your savings goal of ${goal.amount}, consider setting aside ${goal.amount / goal.timeframe} each month.`;
      case 'debt':
        return `To pay off your debt of ${goal.amount}, focus on making extra payments of ${goal.amount / goal.timeframe} monthly.`;
      case 'investment':
        return `For your investment goal of ${goal.amount}, consider diversifying your portfolio with a mix of stocks and bonds.`;
      default:
        return 'Set specific goals to receive tailored advice.';
    }
  };

  return (
    <div className={styles.adviceContainer}>
      <h3 className={styles.adviceTitle}>Goal-Based Financial Advice</h3>
      {goals.length === 0 ? (
        <p>No goals set. Please add your financial goals to receive personalized advice.</p>
      ) : (
        <ul className={styles.adviceList}>
          {goals.map((goal, index) => (
            <li key={index} className={styles.adviceItem}>
              {renderAdvice(goal)}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default GoalBasedAdvice;