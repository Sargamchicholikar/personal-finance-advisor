import React from 'react';
import styles from './PersonalizedTips.module.css';

const PersonalizedTips = ({ userProfile }) => {
  const tips = [];

  // Budgeting Tips
  if (userProfile.income > 0) {
    tips.push(`Consider saving at least 20% of your income each month for future goals.`);
  }

  if (userProfile.expenses > userProfile.income) {
    tips.push(`Your expenses exceed your income. Review your spending habits and identify areas to cut back.`);
  }

  // Saving Tips
  if (userProfile.savings < userProfile.expenses * 3) {
    tips.push(`Aim to build an emergency fund that covers at least 3-6 months of your expenses.`);
  }

  // Investment Tips
  if (userProfile.riskTolerance === 'aggressive') {
    tips.push(`Consider diversifying your investments across different asset classes to manage risk.`);
  } else if (userProfile.riskTolerance === 'conservative') {
    tips.push(`Focus on stable investments like bonds or dividend-paying stocks to preserve capital.`);
  }

  return (
    <div className={styles.tipsContainer}>
      <h3 className={styles.tipsTitle}>Personalized Financial Tips</h3>
      <ul className={styles.tipsList}>
        {tips.length > 0 ? (
          tips.map((tip, index) => (
            <li key={index} className={styles.tipItem}>
              {tip}
            </li>
          ))
        ) : (
          <li className={styles.tipItem}>No personalized tips available at this time.</li>
        )}
      </ul>
    </div>
  );
};

export default PersonalizedTips;