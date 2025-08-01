import React, { useState } from 'react';
import styles from '../../styles/Budgeting.module.css';

const BudgetCreator = () => {
  const [income, setIncome] = useState('');
  const [expenses, setExpenses] = useState('');
  const [budget, setBudget] = useState({ income: 0, expenses: 0, balance: 0 });

  const handleIncomeChange = (e) => {
    setIncome(e.target.value);
  };

  const handleExpensesChange = (e) => {
    setExpenses(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const incomeValue = parseFloat(income) || 0;
    const expensesValue = parseFloat(expenses) || 0;
    const balance = incomeValue - expensesValue;

    setBudget({ income: incomeValue, expenses: expensesValue, balance });
    setIncome('');
    setExpenses('');
  };

  return (
    <div className={styles.budgetCreator}>
      <h2>Create Your Budget</h2>
      <form onSubmit={handleSubmit}>
        <div className={styles.inputGroup}>
          <label htmlFor="income">Monthly Income:</label>
          <input
            type="number"
            id="income"
            value={income}
            onChange={handleIncomeChange}
            placeholder="Enter your income"
            required
          />
        </div>
        <div className={styles.inputGroup}>
          <label htmlFor="expenses">Monthly Expenses:</label>
          <input
            type="number"
            id="expenses"
            value={expenses}
            onChange={handleExpensesChange}
            placeholder="Enter your expenses"
            required
          />
        </div>
        <button type="submit">Create Budget</button>
      </form>
      {budget.income > 0 && (
        <div className={styles.budgetOverview}>
          <h3>Budget Overview</h3>
          <p>Total Income: ${budget.income.toLocaleString()}</p>
          <p>Total Expenses: ${budget.expenses.toLocaleString()}</p>
          <p>Remaining Balance: ${budget.balance.toLocaleString()}</p>
        </div>
      )}
    </div>
  );
};

export default BudgetCreator;