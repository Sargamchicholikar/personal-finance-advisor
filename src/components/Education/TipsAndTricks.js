import React from 'react';
import styles from './Education.module.css';

const TipsAndTricks = () => {
  const tips = [
    {
      title: "Create a Budget",
      description: "Track your income and expenses to understand where your money goes. Use budgeting apps or spreadsheets to help you stay organized."
    },
    {
      title: "Build an Emergency Fund",
      description: "Aim to save at least 3-6 months' worth of living expenses to cover unexpected costs."
    },
    {
      title: "Automate Savings",
      description: "Set up automatic transfers to your savings account to ensure you save consistently."
    },
    {
      title: "Invest Early and Often",
      description: "Take advantage of compound interest by starting to invest as early as possible."
    },
    {
      title: "Educate Yourself",
      description: "Read books, take courses, and follow financial news to improve your financial literacy."
    },
    {
      title: "Review Your Financial Goals Regularly",
      description: "Check in on your financial goals periodically and adjust them as necessary based on your life changes."
    },
    {
      title: "Avoid Impulse Purchases",
      description: "Implement a waiting period before making non-essential purchases to avoid buyer's remorse."
    },
    {
      title: "Use Cash for Discretionary Spending",
      description: "Consider using cash for discretionary expenses to help limit your spending."
    }
  ];

  return (
    <div className={styles.tipsContainer}>
      <h2 className={styles.tipsTitle}>Tips and Tricks for Financial Success</h2>
      <ul className={styles.tipsList}>
        {tips.map((tip, index) => (
          <li key={index} className={styles.tipItem}>
            <h3 className={styles.tipTitle}>{tip.title}</h3>
            <p className={styles.tipDescription}>{tip.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TipsAndTricks;