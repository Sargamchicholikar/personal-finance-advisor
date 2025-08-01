import React from 'react';
import styles from './Charts.module.css';

const Charts = ({ incomeData = [], expenseData = [], savingsData = [] }) => {
  // Calculate totals for simple bar chart visualization
  const totalIncome = incomeData.reduce((sum, item) => sum + item.amount, 0);
  const totalExpenses = expenseData.reduce((sum, item) => sum + item.amount, 0);
  const totalSavings = savingsData.reduce((sum, item) => sum + item.amount, 0);
  
  const maxValue = Math.max(totalIncome, totalExpenses, totalSavings);
  
  const getBarHeight = (value) => {
    return maxValue > 0 ? (value / maxValue) * 100 : 0;
  };

  return (
    <div className={styles.chartsContainer}>
      <h3 className={styles.chartTitle}>Financial Overview</h3>
      <div className={styles.barChart}>
        <div className={styles.barGroup}>
          <div className={styles.bar}>
            <div 
              className={`${styles.barFill} ${styles.incomeBar}`}
              style={{ height: `${getBarHeight(totalIncome)}%` }}
            ></div>
          </div>
          <span className={styles.barLabel}>Income</span>
          <span className={styles.barValue}>${totalIncome.toFixed(2)}</span>
        </div>
        
        <div className={styles.barGroup}>
          <div className={styles.bar}>
            <div 
              className={`${styles.barFill} ${styles.expenseBar}`}
              style={{ height: `${getBarHeight(totalExpenses)}%` }}
            ></div>
          </div>
          <span className={styles.barLabel}>Expenses</span>
          <span className={styles.barValue}>${totalExpenses.toFixed(2)}</span>
        </div>
        
        <div className={styles.barGroup}>
          <div className={styles.bar}>
            <div 
              className={`${styles.barFill} ${styles.savingsBar}`}
              style={{ height: `${getBarHeight(totalSavings)}%` }}
            ></div>
          </div>
          <span className={styles.barLabel}>Savings</span>
          <span className={styles.barValue}>${totalSavings.toFixed(2)}</span>
        </div>
      </div>
      
      {/* Simple trend indicators */}
      <div className={styles.trendSection}>
        <h4 className={styles.trendTitle}>Recent Trends</h4>
        <div className={styles.trendGrid}>
          <div className={styles.trendItem}>
            <span className={styles.trendLabel}>Income Trend</span>
            <div className={styles.trendIndicator}>
              <div className={`${styles.trendArrow} ${styles.trendUp}`}>↗</div>
              <span className={styles.trendText}>Growing</span>
            </div>
          </div>
          
          <div className={styles.trendItem}>
            <span className={styles.trendLabel}>Expense Control</span>
            <div className={styles.trendIndicator}>
              <div className={`${styles.trendArrow} ${styles.trendStable}`}>→</div>
              <span className={styles.trendText}>Stable</span>
            </div>
          </div>
          
          <div className={styles.trendItem}>
            <span className={styles.trendLabel}>Savings Rate</span>
            <div className={styles.trendIndicator}>
              <div className={`${styles.trendArrow} ${styles.trendUp}`}>↗</div>
              <span className={styles.trendText}>Improving</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Charts;