import React, { useEffect, useState } from 'react';
import { fetchSpendingData } from '../../services/analyticsService';
import styles from '../../styles/Analytics.module.css';
import Charts from '../UI/Charts';

const SpendingAnalysis = () => {
  const [spendingData, setSpendingData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadSpendingData = async () => {
      try {
        const data = await fetchSpendingData();
        setSpendingData(data);
      } catch (err) {
        setError('Failed to load spending data.');
      } finally {
        setLoading(false);
      }
    };

    loadSpendingData();
  }, []);

  if (loading) {
    return <div className={styles.loading}>Loading...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  const totalSpending = spendingData.reduce((acc, item) => acc + item.amount, 0);
  const categorizedSpending = spendingData.reduce((acc, item) => {
    acc[item.category] = (acc[item.category] || 0) + item.amount;
    return acc;
  }, {});

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Spending Analysis</h2>
      <div className={styles.summary}>
        <h3>Total Spending: ${totalSpending.toFixed(2)}</h3>
      </div>
      <Charts data={categorizedSpending} />
      <div className={styles.details}>
        <h3>Spending Breakdown</h3>
        <ul>
          {Object.entries(categorizedSpending).map(([category, amount]) => (
            <li key={category}>
              {category}: ${amount.toFixed(2)}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SpendingAnalysis;