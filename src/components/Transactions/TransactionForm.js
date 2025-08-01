import React, { useState } from 'react';
import styles from './Transactions.module.css';
import { addTransaction } from '../../services/transactionService';

const TransactionForm = ({ onTransactionAdded }) => {
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('');
  const [date, setDate] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!amount || !category || !date) {
      alert('Please fill in all fields.');
      return;
    }

    const transaction = {
      amount: parseFloat(amount),
      category,
      date,
      description,
    };

    try {
      await addTransaction(transaction);
      onTransactionAdded(transaction);
      resetForm();
    } catch (error) {
      console.error('Error adding transaction:', error);
      alert('Failed to add transaction. Please try again.');
    }
  };

  const resetForm = () => {
    setAmount('');
    setCategory('');
    setDate('');
    setDescription('');
  };

  return (
    <form className={styles.transactionForm} onSubmit={handleSubmit}>
      <h3>Add New Transaction</h3>
      <div className={styles.formGroup}>
        <label htmlFor="amount">Amount</label>
        <input
          type="number"
          id="amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
        />
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="category">Category</label>
        <input
          type="text"
          id="category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          required
        />
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="date">Date</label>
        <input
          type="date"
          id="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
        />
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="description">Description (optional)</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>
      <button type="submit" className={styles.submitButton}>
        Add Transaction
      </button>
    </form>
  );
};

export default TransactionForm;