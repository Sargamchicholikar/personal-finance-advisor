import React, { useEffect, useState } from 'react';
import styles from '../../styles/Budgeting.module.css';
import { getBudgetAlerts } from '../../services/budgetService';

const BudgetAlerts = ({ budget }) => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const fetchedAlerts = await getBudgetAlerts(budget);
        setAlerts(fetchedAlerts);
      } catch (error) {
        console.error('Error fetching budget alerts:', error);
      }
    };

    fetchAlerts();
  }, [budget]);

  return (
    <div className={styles.alertsContainer}>
      <h3 className={styles.alertsTitle}>Budget Alerts</h3>
      {alerts.length === 0 ? (
        <p>No alerts at this time. You're within your budget!</p>
      ) : (
        <ul className={styles.alertsList}>
          {alerts.map((alert, index) => (
            <li key={index} className={styles.alertItem}>
              {alert.message}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default BudgetAlerts;