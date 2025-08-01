import React from 'react';
import styles from './Transactions.module.css';

const TransactionCategories = ({ categories, onSelectCategory }) => {
  return (
    <div className={styles.transactionCategories}>
      <h3 className={styles.sectionTitle}>Transaction Categories</h3>
      <ul className={styles.categoryList}>
        {categories.map((category) => (
          <li key={category.id} className={styles.categoryItem} onClick={() => onSelectCategory(category)}>
            {category.name}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TransactionCategories;