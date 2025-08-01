import { v4 as uuidv4 } from 'uuid';

// Mock database for transactions
let transactions = [];

// Function to add a new transaction
export const addTransaction = (transaction) => {
  const newTransaction = { id: uuidv4(), ...transaction };
  transactions.push(newTransaction);
  return newTransaction;
};

// Function to update an existing transaction
export const updateTransaction = (id, updatedTransaction) => {
  const index = transactions.findIndex(transaction => transaction.id === id);
  if (index !== -1) {
    transactions[index] = { ...transactions[index], ...updatedTransaction };
    return transactions[index];
  }
  throw new Error('Transaction not found');
};

// Function to delete a transaction
export const deleteTransaction = (id) => {
  const index = transactions.findIndex(transaction => transaction.id === id);
  if (index !== -1) {
    transactions.splice(index, 1);
    return true;
  }
  throw new Error('Transaction not found');
};

// Function to retrieve all transactions
export const getTransactions = () => {
  return transactions;
};

// Function to get transactions by category
export const getTransactionsByCategory = (category) => {
  return transactions.filter(transaction => transaction.category === category);
};