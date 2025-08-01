import React from 'react';
import styles from './ProgressBar.module.css';

const ProgressBar = ({ label, current = 0, target = 1, currency = '$' }) => {
  const safeCurrentValue = Number(current) || 0;
  const safeTargetValue = Number(target) || 1;

  const percentage = Math.min(100, (safeCurrentValue / safeTargetValue) * 100);

  return (
    <div className={styles.progressBar}>
      <div className={styles.progressBarLabel}>
        <span>{label}</span>
        <span>{currency}{safeCurrentValue.toLocaleString()} / {currency}{safeTargetValue.toLocaleString()}</span>
      </div>
      <div className={styles.progressBarTrack}>
        <div 
          className={styles.progressBarFill} 
          style={{ width: `${percentage}%` }}
        />
      </div>
      <div style={{ fontSize: '11px', color: '#6b7280', marginTop: '2px' }}>
        {percentage.toFixed(1)}% complete
      </div>
    </div>
  );
};

export default ProgressBar;