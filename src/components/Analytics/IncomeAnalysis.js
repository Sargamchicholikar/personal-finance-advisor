import React, { useEffect, useState } from 'react';
import { fetchIncomeData } from '../../services/analyticsService';
import styles from '../../styles/Analytics.module.css';

const IncomeAnalysis = () => {
  const [incomeData, setIncomeData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadIncomeData = async () => {
      try {
        const data = await fetchIncomeData();
        setIncomeData(data);
      } catch (err) {
        setError('Failed to load income data.');
      } finally {
        setLoading(false);
      }
    };

    loadIncomeData();
  }, []);

  if (loading) {
    return <div className={styles.loading}>Loading income analysis...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.incomeAnalysis}>
      <h2 className={styles.title}>Income Analysis</h2>
      <ul className={styles.incomeList}>
        {incomeData.map((income, index) => (
          <li key={index} className={styles.incomeItem}>
            <span>{income.source}: </span>
            <span>${income.amount.toLocaleString()}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default IncomeAnalysis;