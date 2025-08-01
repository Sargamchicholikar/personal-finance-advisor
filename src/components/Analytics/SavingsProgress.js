import React from 'react';
import { useEffect, useState } from 'react';
import { ProgressBar } from '../UI/ProgressBar';
import { fetchSavingsData } from '../../services/analyticsService';
import styles from '../../styles/Analytics.module.css';

const SavingsProgress = () => {
  const [savingsGoal, setSavingsGoal] = useState(0);
  const [currentSavings, setCurrentSavings] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadSavingsData = async () => {
      setLoading(true);
      try {
        const data = await fetchSavingsData();
        setSavingsGoal(data.goal);
        setCurrentSavings(data.current);
      } catch (error) {
        console.error('Error fetching savings data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadSavingsData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.savingsProgress}>
      <h3 className={styles.sectionTitle}>Savings Progress</h3>
      <ProgressBar
        label="Current Savings"
        current={currentSavings}
        target={savingsGoal}
      />
      <div className={styles.savingsDetails}>
        <p>Goal: ${savingsGoal.toLocaleString()}</p>
        <p>Current Savings: ${currentSavings.toLocaleString()}</p>
      </div>
    </div>
  );
};

export default SavingsProgress;