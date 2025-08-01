import React from 'react';
import { useState, useEffect } from 'react';
import styles from '../../styles/Budgeting.module.css';
import { getBudgetData } from '../../services/budgetService';

const BudgetOverview = () => {
  const [budgetData, setBudgetData] = useState({
    totalIncome: 0,
    totalExpenses: 0,
    remainingBalance: 0,
  });

  useEffect(() => {
    const fetchBudgetData = async () => {
      try {
        const data = await getBudgetData();
        setBudgetData({
          totalIncome: data.totalIncome,
          totalExpenses: data.totalExpenses,
          remainingBalance: data.totalIncome - data.totalExpenses,
        });
      } catch (error) {
        console.error('Error fetching budget data:', error);
      }
    };

    fetchBudgetData();
  }, []);

  return (
    <div className={styles.budgetOverview}>
      <h2 className={styles.title}>Budget Overview</h2>
      <div className={styles.overviewItem}>
        <span>Total Income:</span>
        <span>${budgetData.totalIncome.toLocaleString()}</span>
      </div>
      <div className={styles.overviewItem}>
        <span>Total Expenses:</span>
        <span>${budgetData.totalExpenses.toLocaleString()}</span>
      </div>
      <div className={styles.overviewItem}>
        <span>Remaining Balance:</span>
        <span>${budgetData.remainingBalance.toLocaleString()}</span>
      </div>
    </div>
  );
};

export default BudgetOverview;