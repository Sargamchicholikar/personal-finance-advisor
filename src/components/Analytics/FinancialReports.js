import React, { useEffect, useState } from 'react';
import { fetchIncomeData, fetchExpenseData, fetchSavingsData } from '../../services/analyticsService';
import styles from '../../styles/FinanceAdvisor.module.css';

const FinancialReports = () => {
  const [incomeData, setIncomeData] = useState([]);
  const [expenseData, setExpenseData] = useState([]);
  const [savingsData, setSavingsData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFinancialData = async () => {
      try {
        const income = await fetchIncomeData();
        const expenses = await fetchExpenseData();
        const savings = await fetchSavingsData();

        setIncomeData(income);
        setExpenseData(expenses);
        setSavingsData(savings);
      } catch (error) {
        console.error('Error fetching financial data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadFinancialData();
  }, []);

  if (loading) {
    return <div>Loading financial reports...</div>;
  }

  return (
    <div className={styles.financialReports}>
      <h2>Financial Reports</h2>
      <div className={styles.reportSection}>
        <h3>Income Overview</h3>
        <ul>
          {incomeData.map((item, index) => (
            <li key={index}>{item.source}: ${item.amount.toLocaleString()}</li>
          ))}
        </ul>
      </div>
      <div className={styles.reportSection}>
        <h3>Expense Overview</h3>
        <ul>
          {expenseData.map((item, index) => (
            <li key={index}>{item.category}: ${item.amount.toLocaleString()}</li>
          ))}
        </ul>
      </div>
      <div className={styles.reportSection}>
        <h3>Savings Overview</h3>
        <p>Total Savings: ${savingsData.total.toLocaleString()}</p>
        <p>Target Savings: ${savingsData.target.toLocaleString()}</p>
      </div>
    </div>
  );
};

export default FinancialReports;