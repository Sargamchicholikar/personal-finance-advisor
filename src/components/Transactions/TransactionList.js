import React, { useState, useEffect } from 'react';
import { getTransactions } from '../../services/transactionService';
import styles from '../../styles/Transactions.module.css';

const TransactionList = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTransactions = async () => {
      try {
        const data = await getTransactions();
        setTransactions(data);
      } catch (err) {
        setError('Failed to load transactions');
      } finally {
        setLoading(false);
      }
    };

    fetchTransactions();
  }, []);

  if (loading) {
    return <div>Loading transactions...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className={styles.transactionList}>
      <h3>Your Transactions</h3>
      <ul>
        {transactions.map((transaction) => (
          <li key={transaction.id} className={styles.transactionItem}>
            <span>{transaction.date}</span>
            <span>{transaction.category}</span>
            <span>{transaction.amount}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TransactionList;