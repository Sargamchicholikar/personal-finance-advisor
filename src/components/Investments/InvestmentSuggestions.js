import React, { useState, useEffect } from 'react';
import { getInvestmentSuggestions } from '../../services/investmentService';
import styles from '../../styles/Investments.module.css';

const InvestmentSuggestions = ({ userProfile }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const data = await getInvestmentSuggestions(userProfile);
        setSuggestions(data);
      } catch (error) {
        console.error('Error fetching investment suggestions:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSuggestions();
  }, [userProfile]);

  if (loading) {
    return <div>Loading investment suggestions...</div>;
  }

  return (
    <div className={styles.investmentSuggestions}>
      <h3 className={styles.sectionTitle}>Investment Suggestions</h3>
      {suggestions.length === 0 ? (
        <p>No suggestions available based on your profile.</p>
      ) : (
        <ul className={styles.suggestionsList}>
          {suggestions.map((suggestion, index) => (
            <li key={index} className={styles.suggestionItem}>
              {suggestion}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default InvestmentSuggestions;