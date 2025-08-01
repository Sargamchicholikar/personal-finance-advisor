import React, { useState } from 'react';
import styles from '../../styles/Budgeting.module.css';

const BudgetCategories = () => {
  const [categories, setCategories] = useState([
    { name: 'Housing', budgeted: 0, spent: 0 },
    { name: 'Food', budgeted: 0, spent: 0 },
    { name: 'Transportation', budgeted: 0, spent: 0 },
    { name: 'Utilities', budgeted: 0, spent: 0 },
    { name: 'Entertainment', budgeted: 0, spent: 0 },
    { name: 'Savings', budgeted: 0, spent: 0 },
  ]);

  const handleBudgetChange = (index, value) => {
    const newCategories = [...categories];
    newCategories[index].budgeted = value;
    setCategories(newCategories);
  };

  const handleSpentChange = (index, value) => {
    const newCategories = [...categories];
    newCategories[index].spent = value;
    setCategories(newCategories);
  };

  return (
    <div className={styles.budgetCategories}>
      <h3 className={styles.sectionTitle}>Budget Categories</h3>
      <table className={styles.categoryTable}>
        <thead>
          <tr>
            <th>Category</th>
            <th>Budgeted</th>
            <th>Spent</th>
          </tr>
        </thead>
        <tbody>
          {categories.map((category, index) => (
            <tr key={index}>
              <td>{category.name}</td>
              <td>
                <input
                  type="number"
                  value={category.budgeted}
                  onChange={(e) => handleBudgetChange(index, parseFloat(e.target.value) || 0)}
                  className={styles.input}
                />
              </td>
              <td>
                <input
                  type="number"
                  value={category.spent}
                  onChange={(e) => handleSpentChange(index, parseFloat(e.target.value) || 0)}
                  className={styles.input}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default BudgetCategories;