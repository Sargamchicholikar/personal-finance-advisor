import React, { useState, useEffect } from 'react';
import { getPersonalizedAdvice } from '../../services/api';
import styles from './AIAdvisor.module.css';

const AIAdvisor = ({ userProfile }) => {
  const [advice, setAdvice] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAdvice = async () => {
      try {
        const response = await getPersonalizedAdvice(userProfile);
        setAdvice(response);
      } catch (error) {
        console.error('Error fetching personalized advice:', error);
        setAdvice('Sorry, we could not retrieve personalized advice at this time.');
      } finally {
        setLoading(false);
      }
    };

    fetchAdvice();
  }, [userProfile]);

  return (
    <div className={styles.advisorContainer}>
      <h3 className={styles.advisorTitle}>Personalized Financial Advice</h3>
      {loading ? (
        <p>Loading advice...</p>
      ) : (
        <p>{advice}</p>
      )}
    </div>
  );
};

export default AIAdvisor;