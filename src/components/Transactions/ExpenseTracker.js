import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import styles from '../../styles/Transactions.module.css';

const ExpenseTracker = ({ userId, onExpenseUpdate }) => {
  const [transactions, setTransactions] = useState([]);
  const [newTransaction, setNewTransaction] = useState({
    amount: '',
    category: '',
    description: '',
    type: 'expense',
    date: new Date().toISOString().split('T')[0]
  });
  const [filter, setFilter] = useState({ category: 'all', period: 'month' });
  const [analytics, setAnalytics] = useState({});
  const [loading, setLoading] = useState(false);

  const categories = [
    { name: 'Housing', icon: '🏠', color: '#2196F3' },
    { name: 'Food', icon: '🍽️', color: '#4CAF50' },
    { name: 'Transportation', icon: '🚗', color: '#FF9800' },
    { name: 'Entertainment', icon: '🎬', color: '#E91E63' },
    { name: 'Healthcare', icon: '⚕️', color: '#9C27B0' },
    { name: 'Shopping', icon: '🛍️', color: '#F44336' },
    { name: 'Education', icon: '📚', color: '#3F51B5' },
    { name: 'Utilities', icon: '⚡', color: '#607D8B' },
    { name: 'Investment', icon: '📈', color: '#009688' },
    { name: 'Savings', icon: '💰', color: '#795548' },
    { name: 'Other', icon: '📋', color: '#9E9E9E' }
  ];

  useEffect(() => {
    loadTransactions();
  }, [userId]);

  useEffect(() => {
    calculateAnalytics();
  }, [transactions, filter]);

  const loadTransactions = () => {
    try {
      const saved = localStorage.getItem(`transactions_${userId || 'default'}`);
      if (saved) {
        setTransactions(JSON.parse(saved));
      }
    } catch (error) {
      console.error('Error loading transactions:', error);
    }
  };

  const saveTransactions = (updatedTransactions) => {
    try {
      localStorage.setItem(`transactions_${userId || 'default'}`, JSON.stringify(updatedTransactions));
      setTransactions(updatedTransactions);
      if (onExpenseUpdate) {
        onExpenseUpdate(updatedTransactions);
      }
    } catch (error) {
      console.error('Error saving transactions:', error);
    }
  };

  const addTransaction = () => {
    if (!newTransaction.amount || !newTransaction.category) return;

    const transaction = {
      id: uuidv4(),
      ...newTransaction,
      amount: parseFloat(newTransaction.amount),
      timestamp: new Date().toISOString()
    };

    const updated = [transaction, ...transactions];
    saveTransactions(updated);
    setNewTransaction({
      amount: '',
      category: '',
      description: '',
      type: 'expense',
      date: new Date().toISOString().split('T')[0]
    });
  };

  const deleteTransaction = (id) => {
    const updated = transactions.filter(t => t.id !== id);
    saveTransactions(updated);
  };

  const calculateAnalytics = () => {
    let filteredTransactions = transactions;

    // Filter by category
    if (filter.category !== 'all') {
      filteredTransactions = filteredTransactions.filter(t => t.category === filter.category);
    }

    // Filter by period
    const now = new Date();
    const periodStart = new Date();
    if (filter.period === 'week') {
      periodStart.setDate(now.getDate() - 7);
    } else if (filter.period === 'month') {
      periodStart.setMonth(now.getMonth() - 1);
    } else if (filter.period === 'year') {
      periodStart.setFullYear(now.getFullYear() - 1);
    }

    if (filter.period !== 'all') {
      filteredTransactions = filteredTransactions.filter(t => 
        new Date(t.date) >= periodStart
      );
    }

    // Calculate analytics
    const totalIncome = filteredTransactions
      .filter(t => t.type === 'income')
      .reduce((sum, t) => sum + t.amount, 0);

    const totalExpenses = filteredTransactions
      .filter(t => t.type === 'expense')
      .reduce((sum, t) => sum + t.amount, 0);

    const categoryTotals = {};
    filteredTransactions
      .filter(t => t.type === 'expense')
      .forEach(t => {
        categoryTotals[t.category] = (categoryTotals[t.category] || 0) + t.amount;
      });

    const topCategory = Object.entries(categoryTotals)
      .sort(([,a], [,b]) => b - a)[0];

    setAnalytics({
      totalIncome,
      totalExpenses,
      netAmount: totalIncome - totalExpenses,
      categoryTotals,
      topCategory: topCategory ? { name: topCategory[0], amount: topCategory[1] } : null,
      transactionCount: filteredTransactions.length
    });
  };

  const getCategoryIcon = (categoryName) => {
    const category = categories.find(c => c.name === categoryName);
    return category ? category.icon : '📋';
  };

  if (loading) {
    return <div className={styles.loading}>Loading transactions...</div>;
  }

  return (
    <div className={styles.expenseTracker}>
      <h3 className={styles.sectionTitle}>💳 Expense & Income Tracker</h3>

      {/* Analytics Summary */}
      <div className={styles.analyticsGrid}>
        <div className={styles.analyticCard}>
          <span className={styles.analyticLabel}>Total Income</span>
          <span className={styles.analyticValue} style={{color: '#4CAF50'}}>
            ${analytics.totalIncome?.toFixed(2) || '0.00'}
          </span>
        </div>
        <div className={styles.analyticCard}>
          <span className={styles.analyticLabel}>Total Expenses</span>
          <span className={styles.analyticValue} style={{color: '#F44336'}}>
            ${analytics.totalExpenses?.toFixed(2) || '0.00'}
          </span>
        </div>
        <div className={styles.analyticCard}>
          <span className={styles.analyticLabel}>Net Amount</span>
          <span className={styles.analyticValue} style={{
            color: (analytics.netAmount || 0) >= 0 ? '#4CAF50' : '#F44336'
          }}>
            ${analytics.netAmount?.toFixed(2) || '0.00'}
          </span>
        </div>
        <div className={styles.analyticCard}>
          <span className={styles.analyticLabel}>Top Category</span>
          <span className={styles.analyticValue}>
            {analytics.topCategory ? 
              `${getCategoryIcon(analytics.topCategory.name)} $${analytics.topCategory.amount.toFixed(2)}` : 
              'No data'
            }
          </span>
        </div>
      </div>

      {/* Add Transaction Form */}
      <div className={styles.addTransactionForm}>
        <select
          value={newTransaction.type}
          onChange={(e) => setNewTransaction({...newTransaction, type: e.target.value})}
          className={styles.transactionInput}
        >
          <option value="expense">Expense</option>
          <option value="income">Income</option>
        </select>

        <input
          type="number"
          placeholder="Amount"
          value={newTransaction.amount}
          onChange={(e) => setNewTransaction({...newTransaction, amount: e.target.value})}
          className={styles.transactionInput}
        />

        <select
          value={newTransaction.category}
          onChange={(e) => setNewTransaction({...newTransaction, category: e.target.value})}
          className={styles.transactionInput}
        >
          <option value="">Select Category</option>
          {categories.map(cat => (
            <option key={cat.name} value={cat.name}>
              {cat.icon} {cat.name}
            </option>
          ))}
        </select>

        <input
          type="text"
          placeholder="Description"
          value={newTransaction.description}
          onChange={(e) => setNewTransaction({...newTransaction, description: e.target.value})}
          className={styles.transactionInput}
        />

        <input
          type="date"
          value={newTransaction.date}
          onChange={(e) => setNewTransaction({...newTransaction, date: e.target.value})}
          className={styles.transactionInput}
        />

        <button onClick={addTransaction} className={styles.addButton}>
          Add Transaction
        </button>
      </div>

      {/* Filters */}
      <div className={styles.filterSection}>
        <select
          value={filter.category}
          onChange={(e) => setFilter({...filter, category: e.target.value})}
          className={styles.filterSelect}
        >
          <option value="all">All Categories</option>
          {categories.map(cat => (
            <option key={cat.name} value={cat.name}>{cat.icon} {cat.name}</option>
          ))}
        </select>

        <select
          value={filter.period}
          onChange={(e) => setFilter({...filter, period: e.target.value})}
          className={styles.filterSelect}
        >
          <option value="week">Last Week</option>
          <option value="month">Last Month</option>
          <option value="year">Last Year</option>
          <option value="all">All Time</option>
        </select>
      </div>

      {/* Transactions List */}
      <div className={styles.transactionsList}>
        {transactions
          .filter(t => filter.category === 'all' || t.category === filter.category)
          .slice(0, 10) // Show recent 10 transactions
          .map(transaction => (
            <div key={transaction.id} className={styles.transactionItem}>
              <div className={styles.transactionIcon}>
                {getCategoryIcon(transaction.category)}
              </div>
              <div className={styles.transactionDetails}>
                <div className={styles.transactionDescription}>
                  {transaction.description || transaction.category}
                </div>
                <div className={styles.transactionDate}>
                  {new Date(transaction.date).toLocaleDateString()}
                </div>
              </div>
              <div className={styles.transactionAmount} style={{
                color: transaction.type === 'income' ? '#4CAF50' : '#F44336'
              }}>
                {transaction.type === 'income' ? '+' : '-'}${transaction.amount.toFixed(2)}
              </div>
              <button
                onClick={() => deleteTransaction(transaction.id)}
                className={styles.deleteButton}
              >
                ❌
              </button>
            </div>
          ))}
        {transactions.length === 0 && (
          <div className={styles.noTransactions}>
            No transactions yet. Add your first transaction above!
          </div>
        )}
      </div>
    </div>
  );
};

export default ExpenseTracker;