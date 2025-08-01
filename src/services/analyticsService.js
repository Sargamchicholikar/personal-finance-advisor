import { fetchUserData } from './api';

// Function to analyze spending patterns
export const analyzeSpending = (transactions) => {
  const totalSpent = transactions.reduce((acc, transaction) => acc + transaction.amount, 0);
  const categorizedSpending = transactions.reduce((acc, transaction) => {
    const category = transaction.category || 'Uncategorized';
    acc[category] = (acc[category] || 0) + transaction.amount;
    return acc;
  }, {});

  return {
    totalSpent,
    categorizedSpending,
  };
};

// Function to analyze income sources
export const analyzeIncome = (incomeSources) => {
  const totalIncome = incomeSources.reduce((acc, source) => acc + source.amount, 0);
  const incomeBreakdown = incomeSources.reduce((acc, source) => {
    const category = source.source || 'Other';
    acc[category] = (acc[category] || 0) + source.amount;
    return acc;
  }, {});

  return {
    totalIncome,
    incomeBreakdown,
  };
};

// Function to track savings progress
export const trackSavingsProgress = (savingsGoals, currentSavings) => {
  return savingsGoals.map(goal => ({
    ...goal,
    progress: (currentSavings / goal.target) * 100,
  }));
};

// Function to generate financial reports
export const generateFinancialReport = async (userId) => {
  const { profile, chat } = await fetchUserData(userId);
  const report = {
    totalIncome: profile.income,
    totalExpenses: profile.expenses,
    totalSavings: profile.savings,
    goals: profile.goals,
  };

  return report;
};

// Function to fetch spending data
export const fetchSpendingData = async (userId) => {
  try {
    // For now, return mock data. In a real app, this would fetch from API
    return [
      { category: 'Food', amount: 500, percentage: 25 },
      { category: 'Transportation', amount: 300, percentage: 15 },
      { category: 'Entertainment', amount: 200, percentage: 10 },
      { category: 'Utilities', amount: 400, percentage: 20 },
      { category: 'Shopping', amount: 300, percentage: 15 },
      { category: 'Healthcare', amount: 150, percentage: 7.5 },
      { category: 'Other', amount: 150, percentage: 7.5 }
    ];
  } catch (error) {
    console.error('Error fetching spending data:', error);
    throw error;
  }
};