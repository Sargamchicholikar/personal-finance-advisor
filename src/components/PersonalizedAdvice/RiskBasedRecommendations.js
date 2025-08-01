import React from 'react';
import { useEffect, useState } from 'react';
import { getInvestmentSuggestions } from '../../services/investmentService';
import styles from '../../styles/Investments.module.css';

const RiskBasedRecommendations = ({ riskTolerance }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        setLoading(true);
        const data = await getInvestmentSuggestions(riskTolerance);
        setRecommendations(data);
      } catch (err) {
        setError('Failed to fetch recommendations. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    if (riskTolerance) {
      fetchRecommendations();
    }
  }, [riskTolerance]);

  if (loading) {
    return <div className={styles.loading}>Loading recommendations...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.recommendations}>
      <h3>Investment Recommendations for {riskTolerance} Risk Tolerance</h3>
      <ul>
        {recommendations.map((recommendation, index) => (
          <li key={index} className={styles.recommendationItem}>
            {recommendation}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RiskBasedRecommendations;