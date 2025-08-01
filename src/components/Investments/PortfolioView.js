import React, { useEffect, useState } from 'react';
import { fetchPortfolioData } from '../../services/investmentService';
import styles from '../../styles/Investments.module.css';
import ProgressBar from '../UI/ProgressBar';

const PortfolioView = () => {
  const [portfolio, setPortfolio] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPortfolioData = async () => {
      try {
        const data = await fetchPortfolioData();
        setPortfolio(data);
      } catch (err) {
        setError('Failed to load portfolio data.');
      } finally {
        setLoading(false);
      }
    };

    loadPortfolioData();
  }, []);

  if (loading) {
    return <div>Loading portfolio...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  const totalInvestment = portfolio.reduce((acc, asset) => acc + asset.value, 0);

  return (
    <div className={styles.portfolioView}>
      <h2>Your Investment Portfolio</h2>
      <div className={styles.portfolioSummary}>
        <h3>Total Investment Value: ${totalInvestment.toLocaleString()}</h3>
      </div>
      <div className={styles.assetList}>
        {portfolio.map((asset) => (
          <div key={asset.id} className={styles.assetItem}>
            <h4>{asset.name}</h4>
            <p>Value: ${asset.value.toLocaleString()}</p>
            <ProgressBar
              label={`Allocation: ${((asset.value / totalInvestment) * 100).toFixed(2)}%`}
              current={asset.value}
              target={totalInvestment}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default PortfolioView;