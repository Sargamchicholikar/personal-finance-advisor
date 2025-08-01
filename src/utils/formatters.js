export const formatCurrency = (amount) => {
  return `$${amount.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;
};

export const formatPercentage = (value) => {
  return `${(value * 100).toFixed(2)}%`;
};

export const formatDate = (date) => {
  return new Date(date).toLocaleDateString();
};

export const formatTransactionType = (type) => {
  return type.charAt(0).toUpperCase() + type.slice(1).toLowerCase();
};

export const formatBudgetOverview = (income, expenses) => {
  const balance = income - expenses;
  return {
    totalIncome: formatCurrency(income),
    totalExpenses: formatCurrency(expenses),
    remainingBalance: formatCurrency(balance),
  };
};